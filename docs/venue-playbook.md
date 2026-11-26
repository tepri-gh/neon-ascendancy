# Venue Playbook

How to make a quest-only venue accessible and populated in the clean-slate
world, and the rules we learned the hard way. Read this before changing
`data/clean-slate/venue_phases.json`, `data/clean-slate/cast_and_hubs.json`,
or the venue code in `tools/build-clean-slate.py`.

Background research: [`research/world-access.md`](research/world-access.md)
(lock mechanisms, options). This playbook supersedes its §5 open probes where
they overlap.

## 1. What a venue needs

Every venue fix so far came down to four ingredients. Vanilla quest phases
already define all four; we copy them, never invent them.

| Ingredient | Vanilla source | Spec key |
| --- | --- | --- |
| Building sections (interiors, props) | a phase's `phasePrefabs` | `prefabs` |
| People: crowds, staff, guards | `questCommunityTemplate_NodeType` (spawner ref + entry + phase) | `communities` |
| Named NPCs (Woodman, Hansen, Dexter) | `questSpawnSet_NodeType` (reference + entry + phase), sometimes a community | `spawn_sets` |
| Door and device state | `questDeviceManager_NodeType` (controller class + action) | `doors` |
| Baked geometry states (shutters, barricades, dataterms) | `questTogglePrefabVariant_NodeType` | `variant_toggles` |

## 2. How the builder wires a venue

- **One quest phase per venue**: `mod\neon_ascendancy\venue_<code>.questphase`.
  All venue phases fan out from one gate pause (`gate` in the spec). A broken
  venue can then only empty itself.
- **Parallel branches, never serial chains.** Per venue:
  hub → branch fact →
  1. every community and spawn-set activation as its own leaf, at boot;
  2. variant toggles at boot, with no proximity wait;
  3. `_prewait` → proximity wait on a device → `_prox` → communities and spawn
     sets re-issued as leaves, plus the device actions as a leaf.
- **Debug breadcrumbs.** `debug_fact_prefix` makes the builder set
  `<prefix>_branch`, `_prewait`, `_prox`, `_reached` and `_done`. Add the
  prefix to `VenueProbe.reds`, and the probe logs them once a minute to
  `red4ext/logs/neonascendancy-*.log` as `VariantToggle[<prefix>]: ...`. That
  shows exactly where a branch stops.
- `--check` enforces the topology: one owner per prefab, leaves with exactly
  one incoming edge, and re-issue counts.

## 3. Rules, each learned from a real failure

**Phases and prefabs**

1. **A phase that fails to instantiate runs nothing, silently.** Symptom:
   `branch=0`. Usually one of rules 2–3.
2. **A prefab declared twice breaks the phase**, whether in one phase, across
   venue phases, or against a kept vanilla phase or `cast_and_hubs`. Each
   prefab gets one owner. If another phase already owns it, give the venue no
   `prefabs` and set `deferred_prefab_owner` to the owner.
   Declaring a prefab a *kept vanilla phase* already loads is redundant
   rather than fatal: hand-built Totentanz declares `#loc_pre_quest_totentanz`,
   which `wat_nid_phase` also loads, and it works. Omit such prefabs; activate
   only the people. Which vanilla loads are live in the clean slate is decided
   by `tools/mine-venues.py` gate analysis: traversal from a phase's inputs
   stops at pause nodes, and at a condition node's True branch, whose fact
   condition needs a fact the clean slate never sets (`q000_done`, the
   `_default_on` facts). Note that a phase node's `phaseInstancePrefabs`
   load when the node itself is reached. A `q000_done` pause *inside* the
   node gates only its contents: the border crossing's open-world section
   loads, while its guards inside wait on `q000_done`.

3. **`#` short refs only resolve for authored (tagged) node names.** Untagged
   nodes (`..._prefabXXXXXXX`) need the full `$/03_night_city/...` path. Take
   it from the streaming block (`all.streamingblock`, a descriptor's
   `questPrefabNodeRef` or a variant's `nodeRef`). The builder rejects untagged
   `#` refs.
4. **A serial chain stalls if any spawn or device node never completes.** Use
   parallel leaves (§2).

**Timing and streaming**

5. **Variant toggles work at boot, without proximity** (the Watson barricades
   proved it).
6. **Communities need activating twice: at boot, and again after
   proximity.** On a fresh start, a one-shot boot activation misses venues
   that haven't streamed in yet.
7. **Device actions need the entity streamed in**, so they run after the
   proximity wait.
8. **Proximity anchors must be device entities** (a door, an alarm, a
   dataterm), not workspots. A workspot anchor never fired at Clouds.

**People**

9. **Pick community phases by their workspot, not by their name.** A phase is
   a set of spots, and each spot plays a workspot animation.
   - `start`, `bar`, `end` and similar phases usually use `routine\...`
     workspots (sit, lean, use a tablet).
   - `hostile`, `after_*` and lockdown phases use
     `generic__stand_ground_gun__nervous__*` or `patrolling\..._agitated_shuffle`.
     NPCs on those look alert, crouched or "sheltering", even when not hostile.

   At Clouds, `after_woodman` looked harmless by name but is the
   post-interrogation lockdown. See §4.2 for how to check.
9a. **Entry `None` with phase `None` and `Activate` switches on a whole
    community**, every entry in its initial phase (`entriesInitialState`).
    It is not a reset. The Totentanz DJ and crowd run this way
    (`#com_totentanz`). The catalogue marks these `whole_community: true` and
    lists each entry's initial phase, so check their postures there.
10. **Drop combat, hostile, scene, cutscene and interrogation phases** unless
    one is chosen on purpose and its workspot is checked. Example: Woodman's
    `q105_interrogation_friendly_start` spawn set is idle behind his desk.
11. **Named NPCs often come from spawn sets, not communities.** Woodman is
    `#woodman`, Hansen is `#kurtz` / `q303_restaurant_host`. Copy vanilla's
    exact reference, entry and phase. The cast layer (`cast_and_hubs.json`)
    holds city-wide named NPCs; venue phases hold venue staff.

11a. **Population priority (owner rule).** When an area has to cap how many
    groups are active (spawn budget, performance, overlapping venues),
    keep combat groups first: netrunners above all, then other fighting
    groups (guards, security, gangers, soldiers, police), then civilians
    (staff, patrons, crowds). Combat groups still use relaxed, non-hostile
    phases. The catalogue tags each entry with `role` (`netrunner`,
    `combat`, `civilian`, `vehicle`) from its character record name.

**Doors and devices**

12. **Door policy** (the owner's, recorded as `door_policy` in the spec):
    - Doors are closed by default but usable: enable and power them, and
      unlock only where there is otherwise no way through.
    - Never `ForceOpen`.
    - Doors with an in-world way through stay exactly vanilla: a terminal, a
      keycard somewhere in the world, a quickhack, or a Technical or Body
      check.

    The engine's own "no way to open" test is `doorController.swift:84`:
    `IsLocked() && !IsAuthorizationValid() && !canPlayerToggleLockState() &&
    !HasAnySkillCheckActive() && !CanCreateAnyQuickHackActions()`. The
    look-at logger prints those inputs. The only exception so far is the
    Black Sapphire sneak-in route.

    **The runtime door policy applies this automatically**
    (`World/DoorPolicy.reds`, gated by fact `na_door_policy`, which dev
    debug sets). On every door that streams in, it acts only on
    quest-driven doors in scope (`World/DoorScope.reds`, generated by
    `tools/venue-proposals.py door-scope`). It enables and powers the door,
    re-checks a second later (skill checks and quickhacks only register on a
    live device), then unlocks or unseals only if `DoorControllerPS.IsStatic()`
    says the door is impassable and there is no authorization module and no
    controlling terminal. Every decision is logged as `DoorPolicy: ...` in
    `red4ext/logs/neonascendancy-*.log`. Venue specs and research proposals
    therefore do not list door actions any more; they list
    `door_exclusions` (rooms that must stay shut) and `door_notes`.
13. **Lift floor access comes from its floor terminals**, the slave
    `ElevatorFloorTerminalControllerPS` devices
    (`liftController.swift`, `GetFloorAuthorizationFromSlaves`).
    `AuthorizationDisable` on the `LiftControllerPS` does nothing for floor
    access. A hackable lift stays vanilla under rule 12.
14. **Baked shutters are mesh (`worldCookedStaticMeshNode`), not devices.**
    Only a variant toggle opens them (Black Sapphire tower gate).
15. **Never touch journal, map pin, phone or holocall controllers.** The
    spec's `forbidden_*` lists enforce this, and `allowed_device_controllers`
    lists the non-door devices we may drive.

**Content that lives elsewhere**

16. The Dogtown vendors are in `ep1_vendors.questphase`, gated by facts; see
    the spec's `notes` entry `dogtown_vendors`.

## 4. Finding the data

Extracting game data uses the pinned WolvenKit CLI
(`~/.cache/neon-ascendancy/wolvenkit-10.0.0-beta.1/WolvenKit.CLI`, run with
`DOTNET_ROLL_FORWARD=Major`). Never commit extracted files. Local extract
locations are listed in `AGENTS-LOCAL.md`.

### 4.1 Quest phases

Extract the `.questphase` files from the base and EP1 archives, then
`convert serialize` them to JSON. For a venue:
- collect the prefabs it instantiates. A phase declares them in two places:
  its own `phasePrefabs`, and `phaseInstancePrefabs` on each
  `questPhaseNodeDefinition` in a parent graph (instantiated while that node
  runs). Open-world sections such as `#loc_q000_border_crossing_openworld`
  load the second way, often behind `q000_done`, which the clean slate never
  sets. The catalogue marks each prefab's `kinds` (`phase`, `instance`);
- collect every `questCommunityTemplate_NodeType`
  (`spawnerReference`, `communityEntryName`, `communityEntryPhaseName`,
  `action`);
- collect every spawn set, device action (`deviceControllerClass`,
  `deviceAction`, `objectRef`) and variant toggle;
- note which phase owns each item. That phase's name says what it's for
  (setup, mood, combat, leave).

### 4.2 Community definitions and their workspots

1. **Entries and records.** Community templates live in
   `always_loaded_1.streamingsector` as `worldCommunityRegistryItem` (entries,
   `characterRecordId`, phases, `entriesInitialState`). Find the right one by
   searching for an entry name.
2. **Spots.** The matching `worldCompiledCommunityAreaNode` (same sector,
   same `communityId` hash) maps each entry and phase to `spotNodeIds`
   (`worldGlobalNodeID` hashes).
3. **Workspots.** Convert the venue's sectors and match the
   `nodeData[*].globalNodeId.hash` values. `nodes[nodeIdx]` is a
   `worldAISpotNode` whose `spot` names the `.workspot` file. That path
   decides rule 9.

Sector buffers are compressed, so byte-grepping `.streamingsector` files for
hashes or names finds nothing. Convert them first.

If a scan over the extracted sectors hangs at 100% CPU (mostly kernel time),
suspect one damaged copy, not the tool. On 2026-11-25 one file's reads ended
at 36 KB of its 194 KB, and every reader (grep, ripgrep, Python) spun on it
forever. Find such files with a per-file timeout:
`find . -name '*.streamingsector' -print0 | xargs -0 -P8 -n1 sh -c 'n=$(timeout 5 cat "$1" | wc -c); [ "$n" = "$(stat -c %s "$1")" ] || echo "$1"' _`.
Move the bad file aside and re-extract it from the game archive.

### 4.3 Which sectors belong to a venue

`all.streamingblock` (base and EP1) lists every sector with its category,
`questPrefabNodeRef` and variants. Filter by the venue's prefab path.

### 4.4 Mapping an in-game object to a ref

The look-at logger prints an entity's 64-bit id. Static entity ids are the
FNV-1a 64 hash of the node's full ref path with the `#` characters removed
(`NcHashNodeRefPath` in `native/plugin/Main.cpp`). Hash the `nodeRefs` of the venue's sectors and match the id. The
Afterlife back-room door was found this way.

### 4.5 In-game evidence

- `lookat.log` (in the CET probe folder): class, id, appearance, position,
  PS state, door open/locked/sealed, `skillCheck`, `quickhack`, `authValid`,
  and NPC record and affiliation.
- `red4ext/logs/neonascendancy-*.log`: `VariantToggle[...]` breadcrumbs,
  `VenueProbe[...]` and `Dataterm[...]` lines.

## 5. Checklist for a new venue

1. Find the vanilla phases that own the venue (§4.1). List prefabs,
   communities, spawn sets, devices and toggles.
2. Check prefab ownership against kept vanilla phases, `cast_and_hubs` and
   other venues (rule 2).
3. Resolve every ref; use full `$/` paths for untagged nodes (rule 3).
4. Choose community phases by workspot (rules 9–10).
5. Classify each door against the door policy (rules 12–13).
6. Pick a device as the proximity anchor (rule 8).
7. Set `debug_fact_prefix` and add it to `VenueProbe.reds`.
8. Build, run `--check` and `tools/verify.sh`, deploy, then read the
   breadcrumbs and the look-at log in game.

## 6. Venue catalogue and walkthroughs

Two local tools feed venue research. Their output is never committed;
`AGENTS-LOCAL.md` records where it lives.

- **`tools/fetch-wiki-walkthroughs.py`** downloads the Cyberpunk wiki's quest
  and location pages (main jobs, side jobs, gigs, minor jobs, minor
  activities, district locations, stores, vendors, apartments) as raw
  wikitext, plus `index.json`. GameFAQs guides are from 2021 and refuse
  automated downloads, so the wiki is the walkthrough source. Quest pages
  carry `baseid` (e.g. `q105_02_jigjig`), which joins them to quest phases.
- **`tools/mine-venues.py`** builds `catalog.json` from the extracted quest
  phases, the community registry, the streaming blocks and (after the
  `sectors` stage) every converted sector. One record per venue (top-level
  location prefab, sibling sub-prefabs merged):
  - owning quests and phases, and matching wiki pages;
  - prefabs, community activations (with character record, spot count,
    workspots and posture), spawn sets, device actions and variant toggles,
    each with the phases that own it;
  - `community_options`: every phase each used community entry defines, with
    its posture and workspots and whether vanilla activates it. Pick ambient
    phases here (rule 9). The relaxed choice is often a phase no quest
    activates, such as Clouds' `guard_vipentrance_01/start`;
  - `posture: unknown` means no spot map was found. About 1,700
    communities, mostly Phantom Liberty, have no community area node in any
    converted sector (where their spots live is still open), and some
    vanilla quests activate phases that do not exist. Check those on the dev
    tour;
  - `venue_inferred: true` on items whose ref is not yet resolved to a path
    and was attached to the venues its phase touches. Treat those as
    unverified until the `sectors` stage has run;
  - `tier`: `individual` (one research agent each: an authored location used
    by a main job, side job, minor job or gig, with people, devices or
    sections to restore) or `batch` (open-world areas, hustles, apartments,
    small sites; several per agent). Owner decisions in
    `data/venues/triage_overrides.json` replace the tier with `excluded`
    (no research) or `deferred` (a later dedicated pass).

  Stages: `phases`, `communities`, `sectors` (slow: converts every sector
  holding spots, devices or community areas; resumable), `catalog`.

  Four sectors refuse WolvenKit 10.0.0-beta.1 conversion. Three hold device
  data cooked with older class names (`APChallangeContainer`,
  `DemolitionContainer`) where the current game classes declare
  `HackingContainer` and `EngDemoContainer`. The game tolerates the
  mismatch; WolvenKit's strict RTTI check refuses the file. The fourth (EP1
  `exterior_-40_-38_0_0`) fails inside WolvenKit's own JSON step. None of
  the four holds community areas; they cost a few devices and spots.
