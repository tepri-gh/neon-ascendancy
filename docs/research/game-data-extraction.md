# Ground-Truth World Data Extraction (Research Step 0.2c)

**Status:** research complete (2026-11-23). Findings below were produced by
read-only inspection of the installed Cyberpunk 2077 **2.5** build on Linux
(`/home/suvikyi/Games/Cyberpunk 2077`), with trial extractions into `/tmp` only.
Nothing in the game directory, `refs/`, or the repository was modified.

**Goal:** determine where spawn coordinates, faction affiliations, landmarks
(POIs, vendors, fast travel), and the road graph actually live in CP2077 2.5,
which Linux-side tools can extract them reproducibly, and what the cleanest
pipeline is to feed Step 0.4 (`data/` seeds → `world.db`).

---

## 0. TL;DR — recommended pipeline

1. **Use WolvenKit Console (native Linux build) 10.0.0-beta.1** as the only
   external binary. It is a `linux-x64` ELF launcher plus .NET assemblies and
   runs on this host's .NET 10 runtime with `DOTNET_ROLL_FORWARD=Major`. Version
   9.1.1 (also the current AUR package) and 8.20.0 **fail** on a large class of
   `worldStreamingSector` files (`Unable to cast ... DynamicBaseClass ... to
   worldNode`), so the version pin is load-bearing.
2. **Do not parse `tweakdb.bin`.** Names are hashed; only 56 `Character.*`
   strings exist in the file. The same data is shipped in plain text as
   `tools/redmod/tweaks/**/*.tweak` (2,748 files, 74,963 records) with
   `affiliation = "Factions.X"` and inheritance. That gives **98.5 % coverage**
   of the character records referenced by the world and **83.4 % affiliation
   resolution** (the remainder are vehicles, quest-only puppets, and
   unaffiliated civilians — expected).
3. **Extract the world in this order and let ep1 win:** `archive/pc/content` →
   `archive/pc/ep1` → (mods ignored). The Phantom Liberty archives ship
   **updated copies of base-game world files**; extracting the base archive
   alone yields an outdated, smaller world.
4. **Coordinates** come from `worldStreamingSector.nodeData[i].transform.position`
   (world-space metres), joined via `nodeIdx`/`globalNodeId`, **not** by
   indexing `nodeRefs` (their lengths do not match `nodes`).
5. **Spawn identity** comes from the global
   `worldCommunityRegistryNode` inside
   `base\worlds\03_night_city\_compiled\default\always_loaded_1.streamingsector`
   (ep1 version): **10,324 communities, 27,411 spawn entries, 5,439 distinct
   character records**, each entry a `characterRecordId` TweakDBID.
6. **Control-centre anchors** come from `worldCompiledCommunityAreaNode`
   instances in `always_loaded_0/1/2` (**3,378**, all with transforms) and, per
   sector, `worldCompiledCommunityAreaNode_Streamable` in **889** sector files
   covering the six urban districts.
7. **Road graph:** `all.traffic_persistent` (ep1): **33,953 lanes**,
   279,916 outline points, per-lane `length`, `maxSpeed`, `inLanes`/`outLanes`,
   `neighborGroupIndex`, `subGraphId`, `roadMaterials`, `crowdCreationInfo`
   (traffic density by time period). This is the source for the deferred
   Road-Chunk Vehicle Transit Ledger.
8. **CET is a validator, not a source.** It can dump TweakDB records
   (`TweakDB:GetRecords`) and live POI mappins
   (`Game.GetMappinSystem():GetMappinEntries`), but exposes no API to enumerate
   communities or their spawn points — those exist only in archive data.

---

## 1. Where the data actually lives

### 1.1 TweakDB binaries (`r6/cache/`)

| File | Size | Notes |
| --- | --- | --- |
| `tweakdb.bin` | 44,143,434 B | magic `47 DB B1 0B`, header version word `8` |
| `tweakdb_ep1.bin` | 50,350,405 B | same header; the EP1 delta/override layer |

Verified by scanning the binaries: only **13,621** printable dotted tokens
(`PhotoModePoses` 7,061, `Items` 5,206, `BaseStatusEffect` 117, `Character`
**56**). Record identity is stored as `TweakDBID` hashes, so `strings`,
grep, or naive parsers cannot recover `Character.*` records, their
`affiliation` flat, or the item/vehicle records.

Consequence: an offline TweakDB reader would need a full parser (community
010-template / `WolvenKit.RED4.TweakDB`), and it is **not required** — see 1.2.

### 1.2 The shipped `.tweak` sources — the practical affiliation source

`<game>/tools/redmod/tweaks/` contains the vanilla REDmod tweak sources as
plain text:

- **2,748 files, 37 MB**, split `base/…` and `ep1/…` (EP1 changes use `[ EP1 ]`
  blocks inside the same record).
- Parsed by a 60-line Python pass: **74,963 record definitions**, of which
  **7,837** are `package Character`.
- **42 distinct affiliation values**, e.g. `Factions.Maelstrom`,
  `Factions.TygerClaws`, `Factions.Valentinos`, `Factions.SixthStreet`,
  `Factions.VoodooBoys`, `Factions.Animals`, `Factions.Scavengers`,
  `Factions.Wraiths`, `Factions.Aldecaldos`, `Factions.Barghest`,
  `Factions.TheMox`, `Factions.Arasaka`, `Factions.Militech`,
  `Factions.KangTao`, `Factions.Biotechnica`, `Factions.NetWatch`,
  `Factions.TraumaTeam`, `Factions.NCPD`, `Factions.NUSA`, `Factions.News54`,
  plus android/rogue variants (`Factions.MaelstromAndroid`,
  `Factions.ScavengersAndroid`, `Factions.SixthStreetAndroid`,
  `Factions.AfterlifeMercRogue`) and civilian buckets.
- Records inherit via `child : parent { … }`, so `affiliation` is usually set on
  a base record (e.g. `maelstrom_grunt1_melee1_knife_ma : maelstrom_base_ma`).
  A tiny resolver walks parents with cycle protection.
- `base/gameplay/static_data/database/factions/factions.tweak` gives
  `enumName`, `localizedName`, `iconPath` (e.g. `logo_arasaka`) per affiliation
  — directly reusable for map overlay colours/icons.

**Measured against the world data:** of the 5,439 distinct character records
referenced by the community registry, **5,355 (98.5 %)** exist in these sources
and **4,535 (83.4 %)** resolve to an affiliation through inheritance. The
missing/affiliation-less remainder is dominated by `Vehicle.*`, quest-only
puppets (`Character.q305_upgrade_hallucination_fa`), and explicit
`Unaffiliated` civilians — not gangs.

### 1.3 Archives and (critical) load order

Archives are `RDAR` **version 12**. Entry payloads are compressed and a raw byte
scan finds no `.community`/`.streamingsector` path strings, so entries can only
be addressed through WolvenKit's path resolution (its `archive -l` / `-w`
support) — no plain `grep`/`strings` enumeration of archive contents is possible.

| Archive dir | Size | Entries | Contents relevant here |
| --- | --- | --- | --- |
| `archive/pc/content/basegame_4_gamedata.archive` | 3.4 GB | 57,033 | 4,033 `.community`, 2,860 `.questphase`, 7,837 … |
| `archive/pc/content/basegame_3_nightcity.archive` | 8.4 GB | 103,917 | 23,642 `.streamingsector`, 5,734 `_inplace` |
| `archive/pc/ep1/ep1_2_gamedata.archive` | 5.5 GB | 30,891 | 1,378 `.community` |
| `archive/pc/ep1/ep1_1_nightcity.archive` | 5.1 GB | 43,411 | 24,188 `.streamingsector`, 2,186 under `default/ep1/` |

**The ep1 archives re-ship base-game paths.** Verified by hash comparison:

| Resource | basegame | ep1 |
| --- | --- | --- |
| `…\_compiled\default\always_loaded_0.streamingsector` | 9,760,322 B | **11,029,057 B** |
| `…\_compiled\default\always_loaded_1.streamingsector` | 35 MB, `448b56…` | **43,770,178 B**, `2bcb42…` |
| `…\_compiled\default\always_loaded_2.streamingsector` | 6,074,522 B | **6,916,912 B** |
| `…\_compiled\default\03_night_city.mappins` | 366 KB | **542,676 B** |
| `…\_generated\traffic\all.traffic_persistent` | 9.6 MB | **10,671,998 B** |

Extraction therefore has to be `basegame → ep1` with ep1 overwriting by
resource path (and `archive/pc/mod` skipped entirely; Neon Ascendancy ships no
world archives). Base-only extraction silently loses Dogtown content and the
2.5-era updates. This is the single biggest correctness trap in the pipeline.

### 1.4 Streaming sector anatomy — where coordinates live

A `worldStreamingSector` (converted to JSON) has:

- `nodes` — **deduplicated node prototypes** (e.g. 359 entries).
- `nodeData.Data` — **instances**, one per placement
  (`worldCompiledNodeInstanceSetupInfo` in 2.5 sectors):
  `nodeIdx` (→ index into `nodes`), `globalNodeId.hash`,
  `transform.position` (`Vector4`, W=0) and `transform.orientation`
  (quaternion), `scale`, `nodeFlags`, `streamingDistance`.
- `nodeRefs` — human paths such as
  `$/03_night_city/#c_heywood/wellsprings/hw_01/…`.
- `variantIndices`, `persistentNodes`, `variantNodes` for level variants.

Sector files are `_compiled/default/<hash>.streamingsector`; grid cells are named
`exterior_<x>_<y>_<z>_<variant>` and interior/quest sectors are opaque hashes.

**District tokens are not uniform.** Verified top-level prefixes under
`$/03_night_city/` across the three `always_loaded_*` files:

| Prefix family | Count (node paths) | Meaning |
| --- | --- | --- |
| `c_watson`, `c_westbrook`, `c_heywood`, `c_santo_domingo`, `c_city_center`, `c_pacifica` | 22,454 / 15,759 / 13,330 / 13,137 / 11,666 / 7,565 | urban districts, spelled **with or without** a leading `#` (`c_watson/…` vs `#c_heywood/…`) |
| `se1`, `se2`, `se5`, `sw1`, `sw2`, `ne1`, `ne2`, `ne3`, `nw2`, `nw6` | 4,947 / 320 / 2,998 / 38 / 1,377 / 101 / 700 / 1,925 / 1 / 1 | **Badlands quadrants** — no `c_badlands` token exists anywhere |

Practical rule: district attribution may not use a `c_*`-only regex. Either map
both spellings **and** the Badlands quadrant tokens explicitly, or attribute
purely spatially / via `DistrictManager` at runtime.

Example verified instance (Little China, Watson):

```
nodeRef : $/03_night_city/c_watson/little_china/wlc_02/…
type    : worldPopulationSpawnerNode
position: X -1604.23  Y 997.37  Z 23.84
```

`nodeRefs` lengths do **not** equal `nodes` lengths (e.g. 902 refs vs 292
nodes vs 2,790 instances), so the only safe joins are
`nodeData.nodeIdx → nodes[i]` and `nodeData.globalNodeId → worldGlobalNodeID`.
Do not index `nodeRefs` by node index. Node paths are usable as a *sector-level*
label only for ordinary sectors; **never** for `always_loaded_*` (see 4.1).

### 1.5 Community registry and the spawn chain

The community data is split across the three `always_loaded_*` level files
under `base\worlds\03_night_city\_compiled\default\` (ep1 versions):

| File | Community registry | Community areas | Spawn entries |
| --- | --- | --- | --- |
| `always_loaded_0.streamingsector` | — | **1,317** | 6,699 |
| `always_loaded_1.streamingsector` | **1** (10,324 communities) | **1,498** | 4,998 |
| `always_loaded_2.streamingsector` | — | **563** | 2,733 |

`always_loaded_1` (43.7 MB in ep1) holds the single master
`worldCommunityRegistryNode`; **all three** files hold
`worldCompiledCommunityAreaNode` instances. Verified node census for
`always_loaded_1`:

| Node type | Count |
| --- | --- |
| `worldStaticMarkerNode` | 4,714 |
| `worldCompiledCommunityAreaNode` | **1,498** (all have instances with transforms, all `sourceObjectId` resolve into the registry) |
| `worldCommunityRegistryNode` | 1 |
| `worldTrafficPersistentNode` | 1 (points at `…\traffic\all.traffic_persistent`) |

`worldCommunityRegistryNode.communitiesData` → **10,324** items:

```
communityId.entityId.hash  ──  joins to area node sourceObjectId
template (inline communityCommunityTemplateData)
  entries[] → characterRecordId  (e.g. Character.nid_maelstrom_grunt1_melee1_knife_ma)
              entryName (CName, e.g. "goon_gun")
              phases[] → timePeriods[] → markings[] / spotNodeRefs[]
```

Registry statistics (ep1): **4,606 non-empty** communities, **27,411** spawn
entries, **5,439** distinct character records. 5,155 communities have zero
entries (crowd/vendor-only shells — they still matter as POI anchors).
Base-game-only registry (for comparison): 8,575 communities / 18,524 entries /
3,891 characters — i.e. ep1 adds **1,749 communities and 8,887 spawn entries**,
mostly Dogtown.

Per-sector placement uses `worldCompiledCommunityAreaNode_Streamable` (a
subclass found in ordinary sectors; 889 sector files contain it):

```
area.entriesData[].entryName
  → phasesData[].timePeriodsData[].spotNodeIds[]  (worldGlobalNodeID.hash)
     → resolve to worldAISpotNode instances and their transforms
```

Spot resolution is **partial by design**: a community area can reference
workspots that live inside nested prefab sectors. Measured over a 57-sector
sample: **3,692 / 7,078** referenced spots resolve inside the same sector
(52 %), with wide per-sector variance (Westbrook/Japan Town 69/93, Watson/
Kabuki 0/107). The area node itself always has a position, which is the correct
anchor for a **Control Center**; individual spot positions are an optional
refinement.

`.community` resources (4,033 base + 1,378 ep1, 28 MB total) are the authoring
templates. Their paths encode faction and place
(`…/cs_cct_cpz_goons_gun_maelstrom.community`,
`…/watson/kabuki/ma_wat_kab_05/…`), which makes them excellent **labels and
audit material**, but the compiled registry already contains their content, so
they are not needed for the coordinate join.

### 1.6 Mappins, POIs, journal

| Resource | What it gives |
| --- | --- |
| `…\_compiled\default\03_night_city.mappins` | `gameMappinResource.cookedData`: 3,247 `gameCookedMappinData` entries in the base file — `journalPathHash` (u32) + `position` (Vector3, world) |
| `…\_compiled\default\03_night_city.poimappins` | `gamePointOfInterestMappinResource.cookedData`: 554 POIs with `entityID`, `journalPathHash`, `position` |
| `base\journal\cooked_journal.journal` (4.8 MB) | full cooked journal tree (→ 69 MB JSON): quests, gigs, scanner hustles, their children and localisation keys |

Mappin *variants* (fast travel, vendor, ripperdoc, scanner hustle) are **not**
stored in these cooked arrays — they are resolved at runtime by `MappinSystem`
from TweakDB. Offline, classify POIs by joining `journalPathHash` to the journal
tree, or by resource path (`…/fasttravel/…`, `…/vendors/…`) and by the
`worldStaticMarkerNode` markers present in `always_loaded_*` (4,714 in the ep1
file, with debug names such as `{dead_zone_marker}`).

`MappinSystem` API confirmed in `refs/cyberpunk` (`MappinSystem`,
`MappinData`, `MappinEntry`): `RegisterMappin`, `GetMappinEntries(targetType,
out mappins)`, `GetMappins`, `DebugDiscoverAllPoiMappins`. `MappinEntry` is only
`{ id, worldPosition }` — no variant.

### 1.7 Road graph (deferred transit ledger source)

`base\worlds\03_night_city\sectors\_generated\traffic\`:

| Resource | Contents (ep1) |
| --- | --- |
| `all.traffic_persistent` | `worldTrafficPersistentData.lanes`: **33,953** `worldTrafficLanePersistent` |
| `all.lane_polygons` | 33,953 lane outlines, **279,916** `Vector3` points |
| `all.lane_connections` | 33,953 lane connectivity records (`inLanes`, `outLanes`, exit probabilities, sharp-angle flags) |
| `all.lane_spots` | tiny (334 B) — effectively empty in 2.5 |
| `traffic.null_areas` | 1.6 MB crowd-null areas |

Each lane carries: `outline` (spline points), `length`, `accumulatedLengths`,
`width`, `area`, `maxSpeed`, `flags`, `isReversed`, `deadEndStart`,
`laneNumber`, `seqNumber`, `subGraphId`, `neighborGroupIndex`, `nodeRefHash`,
`inLanes`/`outLanes`, `roadMaterials`, `playerGPSInfo`, and
`crowdCreationInfo` (desired slot counts per time period → traffic density).

This is a complete, connected drivable graph in world coordinates — enough for
road-chunk partitioning, convoy routing, and per-time-of-day traffic volume,
without touching `.streamingsector` navigation data.

### 1.8 Districts and faction ownership

`base|ep1/gameplay/static_data/database/fasttravel/districts.tweak` defines the
district tree and each district's gangs:

| District | Gangs (vanilla) |
| --- | --- |
| Watson | Maelstrom |
| Westbrook | The Mox, Tyger Claws |
| Heywood | Valentinos |
| Santo Domingo | Sixth Street |
| Pacifica | Voodoo Boys, Animals |
| City Center | — (corporate) |
| Badlands (+ sub-areas) | Aldecaldos |
| Dogtown (ep1) | Barghest |

Sub-districts are `parentDistrict`-linked (e.g. `Kabuki`, `LittleChina`,
`Northside`, `ArasakaWaterfront` under Watson; `Glen`, `VistaDelRey`,
`Wellsprings` under Heywood; `Dogtown_Akebono`, `Dogtown_Expo`,
`Dogtown_Hideout`, `Dogtown_CapitanCaliente`, `Dogtown_Cynosure` under
Dogtown). `enumName` values match `gamedataDistrict` names used in scripts and
in the glossary. `crimeMultiplier` per district is also present.

### 1.9 Verified inventory summary

| Quantity | Value |
| --- | --- |
| Communities (ep1 registry) | 10,324 (4,606 non-empty) |
| Spawn entries (ep1 registry) | 27,411 |
| Distinct character records | 5,439 |
| Prefab community areas (`always_loaded_0/1/2`) | 3,378 (1,317 / 1,498 / 563) |
| Sector-level community areas | 889 sectors (`santo_domingo` 206, `watson` 185, `heywood` 163, `westbrook` 132, `city_center` 71, `pacifica` 69, unattributed 63) |
| Dogtown sectors (`default/ep1/`) | 2,186 (648 contain `worldAISpotNode`, none contain community areas) |
| `.community` templates | 4,033 base + 1,378 ep1 |
| Cooked quest mappins | 3,247 (base file; ep1 larger) |
| POI mappins | 554 (base file; ep1 larger) |
| Traffic lanes | 33,953 (ep1) |
| `.tweak` records | 74,963 (7,837 `Character`) |
| Affiliation values | 42 |

---

## 2. Linux tooling evaluation

### 2.1 WolvenKit Console — the workhorse

`WolvenKit.ConsoleLinux-10.0.0-beta.1.zip` (35,687,755 B,
sha256 `561ff1387cb09e529c40a115cb55e12be0215653415dd2c6131c9c3f320f07d4`)
contains a native `linux-x64` ELF (`WolvenKit.CLI`) plus assemblies, requiring a
.NET runtime. This host has **.NET 10.0.14 runtime only (no SDK)**, so run:

```bash
DOTNET_ROLL_FORWARD=Major ./WolvenKit.CLI <command>
```

Verified working commands (all read-only against the game):

```bash
# index / list / pattern filter (index-only, seconds)
WolvenKit.CLI archive -l  "$GAME/archive/pc/content/basegame_3_nightcity.archive"
WolvenKit.CLI archive -l -w "*.community" <archive>

# extract by wildcard or regex (paths use backslashes in the index)
WolvenKit.CLI extract <archive> -o <dir> -w "*.community"
WolvenKit.CLI extract <archive> -o <dir> -r "(_compiled.default.[0-9a-f]{16}.streamingsector)$"

# CR2W binary -> JSON  (sub-command "s"/"serialize"; accepts files or folders)
WolvenKit.CLI convert s <file-or-dir>
```

There is **no TweakDB command** in the CLI (9.x or 10.x beta) — another reason
1.2 matters.

### 2.2 Measured version matrix

| Version | Result on 2.5 sectors |
| --- | --- |
| 9.1.1 (AUR `wolvenkit-cli-bin`, current) | `archive`, `extract` OK; **`convert` fails** on many sectors: `Unable to cast object of type 'WolvenKit.RED4.Types.DynamicBaseClass' to type 'WolvenKit.RED4.Types.worldNode'` |
| 8.20.0 | same failure |
| **10.0.0-beta.1** | converts the same files successfully (25 MB JSON for the failing test sector) |

Failure rate was not exhaustively measured; in the 156-sector partial run of
the batch extractor there were **0 parse failures**, but the earlier spot checks
(3 of 5 hand-picked `exterior_*` files) all failed on 9.1.1. Treat 9.1.1 as
unsuitable and pin 10.0.0-beta.1 (or a later release that reproduces the test in
§7).

### 2.3 Alternatives considered

| Option | Verdict |
| --- | --- |
| Wine + Windows WolvenKit/GUI | Works in principle but adds a Wine layer for zero benefit; the Linux console build is native |
| `cp77tools` / older ArchiveDump | Dead, pre-2.x formats |
| Python/Rust `RDAR`/CR2W parsers | Archives are hash-indexed and CR2W is schema-driven; re-implementing both is weeks of work versus one pinned binary |
| TweakDB binary parser (`gibbed` schema, 010 template) | Unnecessary for this task (see 1.2); only revisit if item/vehicle flats are ever needed |
| Community TweakDB dumps from the web | Version-mismatched (2.2 era), not reproducible, not needed |
| `redMod.exe` (ships with game) | Mod packaging/export only; cannot dump base-game archives |

---

## 3. CET runtime alternative

CET is **not installed** in the current baseline stack (`docs/modding.md`);
this section evaluates it as a dev-only complement.

### 3.1 What CET can dump reliably

| Need | CET Lua |
| --- | --- |
| Character records incl. `affiliation` | `TweakDB:GetRecords("gamedataCharacter_Record")`, then per record `GetRecord`/flats. Also `TweakDB:GetFlat("…")`, `TweakDB:Query("Query.…")` |
| Live POI / fast-travel / vendor mappins | `Game.GetMappinSystem():GetMappinEntries(targetType, out)`; `Game.GetMappinSystem():DebugDiscoverAllPoiMappins()` |
| Type/field discovery | `DumpType`, `Dump(obj, detailed)`, `DumpAllTypeNames()`, `GameDump` |
| Writing the dump | `io.open(path, "w")` inside the mod folder (`…/cyber_engine_tweaks/mods/<mod>/`) |
| Player/position sanity checks | `Game.GetPlayer():GetWorldPosition()` |

### 3.2 What CET cannot do

- **Enumerate communities or their spawn points.** The script-side
  `CommunitySystem` exposes only `EnableDynamicCrowdNullArea`,
  `DisableCrowdNullArea`, `ChangeDensityModifier`, `ResetDensityModifier`
  (verified in `refs/cyberpunk/orphans.swift`). Community templates, area
  placement, and workspot binding are native and not exposed.
- **Enumerate all world entities** — no documented, stable Lua iteration over
  streamed `NPCPuppet`s; only currently streamed objects are even reachable.
- **Give historical/complete coverage** — a dump reflects the loaded save's
  era (quest-phased communities differ), and requires the graphical session
  (this repo forbids launching the game for research).

**Conclusion:** offline archive extraction is strictly necessary for the spawn
map. CET is the cheapest way to *validate* the offline affiliation table
(compare `gamedataCharacter_Record.affiliation` against the `.tweak` resolver)
and to resolve POI *variants* that only exist at runtime.

### 3.3 Suggested dev-only validation script (not part of the mod)

One-shot CET mod that, on load, writes:

1. `characters.json` — `{ recordId, affiliation, archetype }` for every
   `gamedataCharacter_Record`;
2. `mappins.json` — `{ id, worldPosition, variant }` for POI mappins;
3. `districts.json` — results of sampling `GetDistrictID`/name for a grid of
   known control centres.

That is enough to (a) diff `.tweak` affiliation resolution and (b) classify
POIs, without making CET a dependency.

---

## 4. Coordinate and affiliation join model

### 4.1 The four joins (all verified on real data)

```
(1) area → community
    worldCompiledCommunityAreaNode[_Streamable].sourceObjectId.hash
      == worldCommunityRegistryNode.communitiesData[].communityId.entityId.hash

(2) community → character + phase entry
    template.entries[] .characterRecordId  (TweakDBID name string)
                        .entryName         (CName, e.g. "goon_gun")
                        .phases[].timePeriods[].markings[]  (workspot tag)

(3) character → affiliation
    .tweak: Character.<name> (: parent)* → affiliation = "Factions.X"

(4) area/spot → world position
    nodeData[].nodeIdx == nodes index
    nodeData[].transform.position  (Vector4, metres, W=0)
    nodeData[].transform.orientation (Quaternion)
```

Area nodes resolved **3,777 / 3,777** into the registry in the validation pass
(1,498 / 1,498 for `always_loaded_1` alone), so registry and area sets are
consistent. `worldGlobalNodeID` values are also present on every instance,
enabling a global spot index if exact per-NPC positions are ever needed.

**Attribution rules (non-negotiable for the real extractor):**

1. `always_loaded_0/1/2` are **city-wide** files. Their areas span Watson,
   Westbrook, Heywood, Santo Domingo, City Center, Pacifica, Dogtown and the
   Badlands quadrants in one file (verified prefix census in 1.4). Any
   "majority district of the file" attribution is wrong by construction; each
   area must be labelled **per area** from its `(x, y)` using district bounds,
   the owning `.community` resource path where known, or `DistrictManager` at
   runtime.
2. Ordinary sectors may use sector majority vote as a *hint*, but the 63
   unattributed sectors and the Badlands quadrants must fall back to spatial
   attribution.
3. Every area may have **more than one instance** (`nodeData` can contain
   several entries with the same `nodeIdx`, e.g. repeated placements). Iterate
   all instances and emit one row per placement; never `break` after the first.
4. Record `DistrictSource` (`path`, `spatial`, `manual`) on every seed row so
   later corrections are auditable.

### 4.2 Coverage measured

| Metric | Result |
| --- | --- |
| Registry communities resolvable to an area node | 3,378 prefab areas + 889 sector files |
| Character records present in `.tweak` sources | 5,355 / 5,439 (98.5 %) |
| Character records with resolved affiliation | 4,535 / 5,439 (83.4 %) |
| Spots resolvable inside the same sector (57-sector sample) | 3,692 / 7,078 (52 %) |
| Numeric (unresolved-name) TweakDBIDs in templates | present but rare (e.g. `143693218045`) |

### 4.3 Sample extraction result (validation run)

A 60-file validation pass (57 ordinary sectors + the three `always_loaded_*`
files, 10 sectors sampled per district) converted with 10.0.0-beta.1 produced:

| Group | Area nodes | Spawn entries | Notes |
| --- | --- | --- | --- |
| `always_loaded_0` | 1,317 | 6,699 | quest/combat-zone communities dominate (q301/q303/q305) |
| `always_loaded_1` | 1,498 | 4,998 | mixed world/quest, registry lives here |
| `always_loaded_2` | 563 | 2,733 | — |
| 57 ordinary sectors | 399 | 667 | 1.7 entries/area — mostly ambient crowd/vendor areas |
| **Total** | **3,777** | **15,097** | every area had a transform |

Two practical conclusions:

1. **Density is not in the sectors.** Ordinary sector areas are small
   (`1.7` entries on average); the gang/quest weight sits in the
   `always_loaded_*` prefab areas and in quest sectors. Ranking control centres
   by spawn count must therefore aggregate across all sources, not per sector.
2. **Quest communities must be filtered.** Top entries by size are quest
   scenes (`{q305_com_border_crossing_}002`: 136 entries, mostly `Vehicle.*` and
   NUSA agents). Exclude communities whose name/`entryName` matches
   `^(q|mq|sq)\d+` (and `cs_` city-scene templates) before computing territory
   seeds, or the biggest "hub" in a district will be a scripted set piece.

### 4.4 Coordinate semantics

Positions are world-space metres (samples: Little China `(-1604, 997, 24)`,
Japan Town `(-1491, -1385, 47)`). `Z` is up; some quest/cyberspace mappins have
large negative Z (`-554`) and must be filtered or flagged. Before Step 0.4
freezes seeds, cross-check 3–5 known landmarks (Afterlife, V's apartment,
Megabuilding H10, Arasaka Tower) against in-game coordinates; the extraction
itself preserves whatever the game uses, and the map overlay in Step 0.5 will
also confirm the projection.

---

## 5. Recommended pipeline (`tools/`)

### 5.1 Shape

```
tools/
  fetch-wolvenkit.sh          # pinned version + sha256 -> tools/.cache/wolvenkit-<ver>/
  extract-world.sh            # stages A–C, idempotent, re-runnable
  lib/versions.sh             # add NEON_WOLVENKIT_VERSION / _URL / _SHA
  build-world-seeds.py        # JSON -> data/ seeds (deterministic)
  validate-world-seeds.py     # schema + bounds + coverage gate
dist/extract/                 # gitignored cache (raw JSON, sector JSONL)
data/                         # committed seeds only
```

`dist/extract/` layout (all gitignored, deletable at any time):

```
dist/extract/tweaks/          # copied .tweak text (or read in place from game dir)
dist/extract/registry.json    # always_loaded_1 registry (ep1)
dist/extract/areas.jsonl      # one row per community area instance
dist/extract/spots.jsonl      # optional: node instances with globalNodeId
dist/extract/mappins.jsonl    # cooked mappins + poimappins
dist/extract/traffic.jsonl    # lanes + connections
dist/extract/manifest.json    # archive paths, sizes, sha256, wkit version, timestamps
```

### 5.2 Stages

**A. Inputs (seconds).**

```bash
# affiliation + districts (plain text, no parsing risk)
rsync -a "$GAME/tools/redmod/tweaks/base/" dist/extract/tweaks/base/
rsync -a "$GAME/tools/redmod/tweaks/ep1/"  dist/extract/tweaks/ep1/

# world resources from BOTH archive sets, ep1 last (overwrite)
for A in "$GAME/archive/pc/content" "$GAME/archive/pc/ep1"; do
  WolvenKit.CLI extract "$A"/*.archive -o dist/extract/raw \
    -r "(always_loaded_[0-9]+\.streamingsector|03_night_city\.(mappins|poimappins)|cooked_journal\.journal|traffic\.(all|traffic)…)$"
done
```

Use explicit `-w`/`-r` patterns per resource family rather than extracting whole
archives (61 GB + 14 GB).

**B. Sector candidate set (minutes).**

1. `archive -l` both nightcity archives; collect `_compiled/default/*.streamingsector`.
2. Extract them **from ep1 where present, base otherwise** into
   `dist/extract/sectors/` (verified: 908 files / 473 MB in 5.8 s; full 23,642
   set / 4.7 GB in ~90 s).
3. Binary-scan each sector for `worldCompiledCommunityAreaNode` (a plain
   `grep -la` over the extracted CR2W is enough) → ~889 candidates; add all
   three `always_loaded_*` files from `dist/extract/raw/`.
4. Convert only candidates, **in batches of 12–16**, parse, append JSONL rows,
   delete the JSON. Measured: 45 MB JSON per sector, ~2.4 s (10.0 beta) up to
   ~11 s under load; a 60-file validation pass took **1 m 37 s** with 12-way
   parallelism, so 889 sectors ≈ **20–25 min** with a peak disk of ~1 GB when
   batched.

**C. Rows → seeds (seconds).**

- `areas.jsonl` row: `{ sector, district, subdistrict, area_name, community_hash,
  matched, entries, chars[], x, y, z, spots, spots_resolved }`.
- `build-world-seeds.py` then:
  1. resolves affiliation per character (inheritance resolver, 4.2 numbers);
  2. maps `district` token → `Districts.*` record via a small fixed table
     (`c_watson→Watson`, `#c_heywood→Heywood`, `c_santo_domingo→SantoDomingo`,
     `c_westbrook→Westbrook`, `c_pacifica→Pacifica`, `c_city_center→CityCenter`,
     Badlands quadrants `se*/sw*/ne*/nw*→Badlands`, `Dogtown_*→Dogtown`), and
     replaces token lookup with per-area spatial attribution for
     `always_loaded_0/1/2` rows (see 4.1);
  3. drops rows with no position or non-finite coordinates;
  4. clusters areas into ~5 sub-territories per district (k-means on X/Y with a
     deterministic seed, or fixed district polygons) and emits
     `data/spawns/*.json`, `data/territories/*.json`, `data/landmarks/*.json`;
  5. writes `data/MANIFEST.json` (source archive hashes, wkit version, row
     counts) so seeds are reproducible and diffable.

**D. Gate.** `tools/verify.sh` gains a data stage:
`validate-world-seeds.py` (schema, coordinate bounds, ≥N spawns per district,
no duplicate `(community_hash, entry_idx)`), run only when `data/` exists.

### 5.3 Throughput measured on this host

| Operation | Time / size |
| --- | --- |
| List archive index (103,917 entries) | ~4 s |
| Extract 5,411 `.community` (28 MB) | 7.5 s |
| Extract 908 sectors (473 MB) | 5.8 s |
| Convert 235 `.community` → JSON | 1.3 s |
| Convert 1 sector (45 MB JSON) | 2.4 s (beta) / ~11 s under 12-way load |
| Convert 60 sectors incl. `always_loaded_*` (12-way) | 1 m 37 s wall |
| Convert `always_loaded_1` (435 MB JSON) | 11.5 s |

Peak disk is the only real resource concern; keep JSON batches small and delete
after parsing.

### 5.4 Determinism and provenance

- Pin WolvenKit in `tools/lib/versions.sh` (`NEON_WOLVENKIT_VERSION`,
  `_URL`, `_SHA256`) like the other frameworks.
- Record per-row `archive` + `resource_path`; record per-run
  `manifest.json` with archive SHA-256s and the wkit version.
- Sort all emitted JSON by stable keys; round coordinates to 3 decimals; never
  emit hash-ordered output.
- Never commit raw extracts (`dist/` is already gitignored) or game binaries.
- Seeds are the committed artifact; `world.db` is generated by `tools/build-db`
  in Step 0.4.

### 5.5 Bugs in the throwaway validation scripts (must not be repeated)

The ad-hoc `/tmp` scripts used for the numbers in this report contained four
defects. The production extractor must fix all of them, and `tools/verify.sh`
should assert the resulting invariants:

| # | Defect (observed in throwaway scripts) | Requirement for `tools/` |
| --- | --- | --- |
| A | District regex only matched `/c_x/`, missing `#c_x/` and all Badlands quadrant prefixes | Match both `c_*` spellings **and** the `se*/ne*/sw*/nw*` quadrants; unit-test the classifier on `c_watson/…`, `#c_heywood/…`, `se5/…` |
| B | Every area inside a city-wide `always_loaded_*` file was attributed to that file's majority district | Attribute `always_loaded_*` areas **per area** (spatial bounds, owning `.community` path, or runtime `DistrictManager`); forbid sector-majority attribution for these three files |
| C | `break` after the first `nodeData` instance for a node dropped duplicate placements | Iterate **all** instances for a `nodeIdx` and emit one row per placement; assert `rows >= distinct (area, instance)` |
| D | `subprocess.run(..., DEVNULL)` ignored non-zero exits and `chars[:8]` / `[:10]` truncated spawn lists | Check return codes and abort on failure; never truncate `entries`/`characters`; emit full lists plus counts |

Additional invariant worth testing: `sum(entries)` from the emitted rows must
reconcile with the registry total (27,411 for ep1) when restricted to matched
communities.

### 5.6 Mapping to Step 0.4 schema

| Seed file | `world.db` table (architecture §3.3) | Source |
| --- | --- | --- |
| `data/factions.json` | `factions` | `.tweak` `Factions.*` + `Districts.*.gangs` |
| `data/districts.json` | `districts` | `fasttravel/districts.tweak` |
| `data/territories/*.json` | `sub_territories` | clustered area nodes per district |
| `data/spawns/*.json` | `spawn_points` | `areas.jsonl` + registry entries + affiliation |
| `data/landmarks/*.json` | `landmarks` | mappins/poimappins + area names + markers |
| `data/roads/*.json` (deferred) | `road_chunks`, `road_edges` | `all.lane_polygons`, `all.lane_connections` |

---

## 6. Risks and mitigations

| # | Risk | Evidence | Mitigation |
| --- | --- | --- | --- |
| 1 | **Base-only extraction loses 2.5/ep1 world data** | same resource path differs: `always_loaded_1` 35 MB vs 43.7 MB; registry 8,575 vs 10,324 communities | Fixed merge order `content → ep1`, verify counts in `manifest.json`; fail the build if registry < 10,000 communities |
| 2 | **WolvenKit version fragility** | 9.1.1/8.20.0 `DynamicBaseClass → worldNode` cast failure | Pin 10.0.0-beta.1 in `versions.sh`; keep one known-good sector as a smoke test in `tools/verify.sh` |
| 3 | Spot positions are not always in the referencing sector | 0/107 (Watson) vs 69/93 (Westbrook) | Use area-node transforms as control-centre anchors; build a global `globalNodeId` index only if exact spots are needed |
| 4 | `nodeRefs` do not align with `nodes` | 902 refs / 292 nodes / 2,790 instances | Join on `nodeIdx`/`globalNodeId`; use path strings only for sector-level labels |
| 5 | District attribution by path token | two spellings (`c_watson`, `#c_heywood`) **plus** Badlands quadrant prefixes (`se1`, `ne3`, `sw2`, …); 63 unattributed sectors | Match both spellings and map the quadrant tokens; use spatial/`DistrictManager` attribution inside `always_loaded_*`; allow `unknown` + spatial fallback |
| 6 | TweakDB names are hashed | 56 `Character.*` strings in 44 MB file | Use `.tweak` text sources; treat numeric TweakDBIDs as unresolved and log them |
| 7 | Affiliation gaps | 83.4 % resolved | Vehicles/quest puppets are legitimately unaffiliated; treat `Unaffiliated*` explicitly; add `AffiliationSource` column (tweak / inferred / none) |
| 8 | Dogtown has essentially no sector-level community areas | 2,186 ep1 sectors, 0 `worldCompiledCommunityAreaNode`, 648 with `worldAISpotNode` | Take Dogtown areas from the ep1 `always_loaded_*` files (registry + 3,378 prefab area nodes); do not expect per-sector areas |
| 9 | Badlands has no `c_badlands` token | 0 `c_badlands` sectors among the 889; Badlands uses `se*/ne*/sw*/nw*` quadrant prefixes | Map quadrant tokens to Badlands sub-areas or attribute spatially; Aldecaldos/Wraith coverage still needs a check against prefab/quest data |
| 10 | Journal path hash → title mapping unresolved | `cookedMappinData.journalPathHash` is a u32, journal entries carry string ids | Defer; classify POIs by path/variant, or resolve at runtime via CET if titles are needed |
| 11 | Disk/RAM blow-up | 45 MB JSON per sector; 889 sectors | Batch convert/parse/delete; never convert the whole world at once |
| 12 | Legal/ToS hygiene | game assets | Only derived coordinate/metadata seeds enter Git; raw blobs stay in `dist/` |

---

## 7. Open questions / follow-ups

1. **Cross-check coordinates** against 3–5 in-game landmarks (the report's
   numbers are internally consistent, but a landmark check is cheap insurance).
2. **District polygons.** `Districts.*` has no geometry. If the Step 0.5 overlay
   needs exact borders, derive them from sector path majorities per grid cell or
   from runtime `DistrictEnteredEvent` sampling; otherwise pre-partition
   sub-territories geometrically (Voronoi around control centres).
3. **Scanner hustles / gigs.** Positions are in `cookedMappinData`; titles need
   the journal hash join (risk 10). For Step 0.4 only positions + faction matter,
   which the community areas already provide.
4. **`data/` ownership map.** Initial owners can be seeded straight from
   `Districts.*.gangs` plus per-district spawn density (faction with the most
   entries in a cluster owns it).
5. **Road chunking.** Decide cell size after looking at 33,953 lane lengths;
   R-Tree over lane outlines (`all.lane_polygons`) is the natural index.
6. **Reproducibility test.** Commit a `tools/verify.sh` check that re-extracts
   one sector and asserts a fixed position hash, guarding against silent
   WolvenKit/game-version drift.

---

## Appendix A — commands used for this research

```bash
GAME='/home/suvikyi/Games/Cyberpunk 2077'
WK=./WolvenKit.CLI            # WolvenKit.ConsoleLinux-10.0.0-beta.1

# inventory
$WK archive -l "$GAME/archive/pc/content/basegame_4_gamedata.archive" | awk -F. '{print $NF}' | sort | uniq -c | sort -rn | head
$WK archive -l "$GAME/archive/pc/content/basegame_3_nightcity.archive" | grep -c '\.streamingsector$'

# community templates (base + ep1)
$WK extract "$GAME/archive/pc/content/basegame_4_gamedata.archive" -o /tmp/w -w "*.community"
$WK extract "$GAME/archive/pc/ep1/ep1_2_gamedata.archive"        -o /tmp/w -w "*.community"

# registry + areas
$WK extract "$GAME/archive/pc/ep1/ep1_1_nightcity.archive" -o /tmp/w -w "*always_loaded_1.streamingsector"
$WK convert s /tmp/w/base/worlds/03_night_city/_compiled/default/always_loaded_1.streamingsector

# sectors
$WK extract "$GAME/archive/pc/ep1/ep1_1_nightcity.archive" -o /tmp/s -r '(_compiled.default.[0-9a-f]{16}.streamingsector)$'
grep -la 'worldCompiledCommunityAreaNode' /tmp/s/**/*.streamingsector
$WK convert s <sector>.streamingsector

# traffic + mappins
$WK extract "$GAME/archive/pc/ep1/ep1_1_nightcity.archive" -o /tmp/t -w "*all.traffic_persistent"
$WK extract "$GAME/archive/pc/content/basegame_3_nightcity.archive" -o /tmp/t -w "*.mappins"
$WK convert s /tmp/t

# affiliation text sources (read-only)
grep -rn 'affiliation *=' "$GAME/tools/redmod/tweaks" | head
```

All commands require `DOTNET_ROLL_FORWARD=Major` on this host.

## Appendix B — verified output shapes

`worldStreamingSector` instance (sector JSON):

```json
{ "$type": "worldCompiledNodeInstanceSetupInfo",
  "nodeIdx": "353", "globalNodeId": { "hash": "1205414192146705736" },
  "transform": { "position": { "X": -1604.23096, "Y": 997.372253, "Z": 23.8440132 },
                 "orientation": { "i": 0, "j": 0, "k": -0.7604, "r": 0.6494 } } }
```

`worldCommunityRegistryItem`:

```json
{ "communityId": { "entityId": { "hash": "6810260498045666404" } },
  "template": { "Data": { "entries": [
    { "Data": { "characterRecordId": { "$value": "Character.nid_maelstrom_grunt1_melee1_knife_ma" },
                "entryName": { "$value": "goon_gun" },
                "phases": [ { "Data": { "timePeriods": [ { "hour": "Day", "quantity": 1,
                                                            "markings": [ "cs_goons_gun" ] } ] } } ] } } ] } } }
```

`communityArea`:

```json
{ "entriesData": [ { "entryName": { "$value": "car_poor_colby" },
    "phasesData": [ { "entryPhaseName": { "$value": "default" },
      "timePeriodsData": [ { "periodName": { "$value": "Day" },
        "spotNodeIds": [ { "hash": "4665778363092172528" } ] } ] } ] } ] }
```

`trafficLanePersistent` (abridged): `outline[Vector3…]`, `length`, `width`,
`maxSpeed`, `inLanes[]`, `outLanes[]`, `subGraphId`, `neighborGroupIndex`,
`roadMaterials`, `crowdCreationInfo.desiredSlotCountsPerTimePeriod`.
