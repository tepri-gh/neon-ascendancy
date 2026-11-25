# Night Corp — Lore-Relevant Control Points

Status: faction research run, 2026-11-25. One faction, one document.
Scope: replace the generic control-centre grid with places Night Corp actually
owns, runs, protects or garrisons in Night City, with verified coordinates, an
economic map, an HQ pick, a ranked capture list and honest per-sub-district
counts. Method: this doc conforms to [`METHOD.md`](./METHOD.md); §1.1 (batch-1)
and §1.2 (batch-2) corrections were read first and override the later sections.
`AGENTS.md` was read first. No commits, no game launch.

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Position, site, community, roster or spawn record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/artbook/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My reasoning links a named place to a game record; reasoning stated | Weak, flagged |

No coordinate below is guessed. Every `(x, y, z)` is copied from a local marker,
site or seed record, or marked `TBD`.

**Up front, because it changes the whole doc:** Night Corp is the **emptiest
faction in `data/factions.json`**. It has `affiliation_enum: null`, and
`gamedataAffiliation` (44 values, verified in `refs/cyberpunk/orphans.swift`)
has **no Night Corp entry at all** — not even a `corpbud`-style stand-in. The
2.5 extract contains **zero** roster sites, **zero** roster units, **zero**
community areas, **zero** spawn points, **zero** faction-owned sub-territories,
**zero** `default_faction_id = 40` sites and **no** `Character.*` record.
Grepping all three `always_loaded_*` sectors for the corp turns up only
**4 vehicles, 9 guard workspots, 1 AV spawn and 1 tunnel gate** — all inside one
quest (`q114`). Every other megacorp studied in this series at least fields
security NPCs; Night Corp fields none.

So this faction is **marker-, prefab- and wiki-driven by construction**. That
is not a research failure — it is the finding. The doc below gives it six named
points, all but one carried by *place* records rather than faction records, and
says plainly where the map cannot supply an anchor.

---

## 1. Summary

Night Corporation — "Night Corp" — faction id **40**, category `megacorp`,
`income_multiplier 1.45`, `hostility_bias 0.25`. It is not an arms or cyberware
house. It is **Night City's founding civic contractor**: a development firm and
public-works corporation that builds and maintains roads, bridges, tunnels,
metro lines, power plants, net transmitters, waterworks and sewerage, and acts
as the city's largest public-procurement contractor. `[wiki]`

Founded by **Richard Night** as Night International, restructured by his widow
**Miriam Night** into Night's Foundation in 1999, then into Night Corp in the
early 2010s. Its 2077 position is *declining but structurally embedded*: it lost
the corporate-power race to Arasaka and Militech, yet still runs much of the
local infrastructure and funds the NCPD and MaxTac. `[wiki]`

Night City holdings documented below:

- **Downtown (City Center) — Night Corp Headquarters / Night Corp Tower.** The
  global HQ, on Republic Way in 2045, second-tallest building in Night City
  after Arasaka Tower, "not far from Corporate Plaza". This is **not** City
  Hall and **not** the same building: City Hall is in the **Glen** (Heywood),
  1,134 m away. `[wiki]` `[game-data]`
- **Corpo Plaza (City Center) — Memorial Park Station.** NCART's central hub,
  built underneath Memorial Park. NCART has been a Night Corp subsidiary since
  the 2068 buyout. `[wiki]` `[game-data]`
- **Badlands / Jackson Plains — Night Corp Solar Farm.** A large photovoltaic
  array built with PacCon Electric; "more than half"-scale contributor to city
  power in its day, **inactive by 2077**. No marker; coordinate `TBD`. `[wiki]`
- **Badlands / Rocky Ridge Plains — Maglev Tunnel Construction Site.** Night
  Corp's revived-maglev tunnel bore, guarded by Militech SiteSecure. Site of
  *Forward to Death*. `[wiki]` `[game-data]`
- **Badlands / North Sunrise — Northern Oil Fields**, jointly held with
  Petrochem and SovOil. `[wiki]` `[game-data]`
- **Coastview (Pacifica) — Old Maglev Tunnel**, Night Corp's **de jure** but
  Voodoo Boys-held. `[wiki]` `[game-data]`

Game-data scale: **0 / 0 / 0 / 0 / 0**. No roster, no areas, no spawns, no
seed ownership, no interior of its own. The weight sits entirely in **Downtown**
(one tower) and the **Badlands** (three infrastructure sites), with the civic
transit hub in **Corpo Plaza**.

---

## 2. Territory

### 2.1 Districts

| Evidence kind | Result |
| --- | --- |
| (a) Wiki/lore | Global HQ is the Night Corp Headquarters, Downtown, City Center (2077); it was in Little Europe in 2045. Infrastructure footprint: NCART (subsidiary), the maglev revival (Badlands → Corporate Plaza), the Jackson Plains solar farm, the Northern Oil Fields (joint), waterworks and power. `[wiki]` |
| (b) Vanilla map gang panel | **Inapplicable by design.** `data/districts.json` `vanilla_gangs` lists street gangs; megacorps never appear. |
| (c) Game-data counts | **All zero.** 0 roster sites, 0 units, 0 areas, 0 spawn points, 0 owned sub-territories, 0 sites with `default_faction_id = 40`, 0 `Character.*` records, no `gamedataAffiliation` value, no `gamedataDistrict` value. `affiliation_enum = null`. `[game-data]` |

The seed gives Night Corp **nothing**. `data/sub_territories.json`,
`data/landmarks.json`, `data/control_centers.json` and
`data/faction_headquarters.json` contain **zero** rows for faction id 40, and
`tools/generate-world-seeds.py` has **zero** `CURATED_ZONES` rows with owner 40.
This faction has never been placed on the map. `[game-data]`

### 2.2 Sub-district presence

Counts are from `dist/extract/areas.jsonl` (`night_corp` in `faction_counts`),
`data/sites/rosters.json` (`faction_id == 40`) and `data/sites/sites.json`
(`default_faction_id == 40`). Attribution follows METHOD §3.3 / §1.2.

| Sub-district | District | (a) Lore | (b) Panel | (c) Areas | (c) Roster units | Occupied sites |
| --- | --- | --- | --- | ---: | ---: | ---: |
| Downtown | CityCenter | **HQ tower** | — (corp) | 0 | 0 | 0 |
| CorpoPlaza | CityCenter | **NCART Memorial Park Station** | — (corp) | 0 | 0 | 0 |
| Badlands | Badlands | **Solar farm, maglev site, oil fields** | Wraiths/Aldecaldos/Militech | 0 | 0 | 0 |
| Coastview | Pacifica | Old Maglev Tunnel (de jure) | Voodoo Boys | 0 | 0 | 0 |

`[game-data]`

**Reading the counts.** Every game-data column is zero, so this table says
nothing about Night Corp — it is included to show the zeros are real and were
measured, not skipped. The only Night Corp-attributable records in the whole
extract are inside `q114`:

| Record | Count | What it is |
| --- | ---: | --- |
| `car_nightcorp_001..004` | 4 | Night Corp fleet sedans; four more as bridge wrecks (`q114_ws_bridge_wreck_car_nightcorp_001..004`) |
| `q114_ws_nightcorp_security_001..009` | 9 | Guard workspots at the construction site **tunnel gate** |
| `q114_spwn_nightcorp_av` | 1 | Night Corp AV spawn inside the Arasaka facility |
| `q114_nightcorp_tunnel_gate_a_damaged_dst` | 1 | Damaged blast door on the tunnel route |

`[game-data]`

That is the entire physical presence of the corporation in Cyberpunk 2077:
**four cars, nine guard stands, one AV and one blast door**, all in the Badlands
construction-site block of one main job. There is no Night Corp office NPC, no
corporate drone, no patrol, no vendor and no interior.

### 2.3 Attribution caveat

There is nothing to mis-attribute: no Night Corp row exists in `areas.jsonl` or
`rosters.json` to attribute in the first place. Two adjacent hazards matter
instead:

1. **The `q114` workers are not Night Corp.** `{loc_q114_tunnel_site_com_workers}`
   at `(217.7, 2394.3, 67.1)` resolves to two `Character.WorkerMale` — generic
   labourers with no faction. The site's "Night Corp security" is
   `{q114_com_construction_nc_security}` at `(195.9, 2390.4, 65.4)`, and its six
   entries are `Character.q114_militech_medium_drone`. **The site's garrison is
   Militech contract security, exactly as the wiki describes** ("Night Corp
   hired a subgroup of Militech called 'Militech SiteSecure'"). Do not read the
   drones as Night Corp units. `[game-data]` `[wiki]`
2. **The NCART station's garrison is Militech too.** Site 350
   (`sts_cct_cpz_01`, Memorial Park Station) carries
   `default_faction_id = null`, `initial_owner_faction_id = 21`, and 15 roster
   entries led by `Character.sts_cct_cpz_01_enemy_security*`. Its sub-territory
   is `cpz_militech_hq`. The fiction agrees: after Zoli Barnes' death, "Militech
   temporarily took over security operations in the station". `[game-data]` `[wiki]`

---

## 3. Location catalog

Coordinates are world-space metres, `Z` up. "Interior?" means the game has a
distinct interior cell or room volume.

| # | Name | Type | District / sub-district | Interior? | Business? (what it earns) | Coordinates (x, y, z) | Coordinate source record | Linked communities / sites | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **Night Corp Headquarters** (Night Corp Tower) | Corporate HQ skyscraper | CityCenter / Downtown | No cell in extract; tower is scenery + a tour scene | Corporate administration; public-works contracting; real-estate development; the corp's civic-influence seat | `-1809.430, 233.868, 27.770` | `dist/extract/markers.jsonl` `mq061_01_sm_nc_tower_scene` | No `sites.json` row. Prefab `#c_city_center/corpo_plaza/loc_mq061_prefab…/#loc_mq061_openworld/#01_nc_tower_v/` (`#01_nc_tower_holo_start`, `#01_nc_tower_holo_drone`); quest folder `#01_mq061_nctower` | `[game-data]` `[wiki]` |
| 2 | **NCART Memorial Park Station** | Metro hub station (underground) | CityCenter / CorpoPlaza | **Yes** — concourse at z ≈ −4 to −8, doors, guard volumes, 28 workspots | Transit fares, NCART City Pass, advertising; the central hub of the network Night Corp owns | `-1339.983, -17.944, -3.900` | `data/sites/sites.json` site 350 `sts_cct_cpz_01` (anchor); node positions `data/sites/triggers.json` `#cpz_01_tr_entrance` | Site 350, 15 roster entries, 3 guard areas, 7 patrols, 4 doors, 5 communities | `[game-data]` `[wiki]` |
| 3 | **Maglev Tunnel Construction Site** | Tunnel bore / construction site | Badlands / Badlands | No — open site + control room; no door or room records | Maglev-network revival (the corp's flagship 2077 project); no direct revenue in 2077 | `249.137, 2428.782, 67.081` | `dist/extract/markers.jsonl` `q114_mp_construction` | 16 `q114` community areas within 120 m; `{q114_com_construction_nc_security}` (6 Militech drones), `{q114_com_construction_combat_nc_control_room}` (2 Militech snipers), `{loc_q114_tunnel_site_com_workers}`; prefab `#loc_q114_tunnel_site` | `[game-data]` `[wiki]` |
| 4 | **Night Corp Solar Farm** (Jackson Plains Solar Farm) | Photovoltaic power station | Badlands / Badlands | No — open array field | Electricity generation (historic); **inactive by 2077** | `TBD` | **No marker, no site, no area, no prefab node.** Wiki: `owner = Night Corp`, `manager = PacCon Electric`, `region = Badlands`, `subregion = Jackson Plains` | None found | `[wiki]` only; coordinate `TBD` |
| 5 | **Northern Oil Fields** (North Sunrise) | Oil field; active and abandoned rigs | Badlands / Badlands | No — open field; barracks are separate meshes | Crude extraction and CHOOH2 feedstock; **jointly** Petrochem / SovOil / Night Corp | `-1845.399, 3855.277, 7.442` (pumps/barracks) | `dist/extract/markers.jsonl` `sq031_mp_oil_fields`; fast-travel dataterm `-1835.695, 3719.295, 6.742` | Seeded sub-territory `bls_north_oil_fields` (owner 21); no `sites.json` row | `[game-data]` `[wiki]` |
| 6 | **Old Maglev Tunnel** (Rezo Agwe) | Abandoned maglev tunnel | Pacifica / Coastview | **Yes** — tunnel and vault below the chapel | None for Night Corp. Held by Voodoo Boys as a netrunning data fortress | `-1665.273, -1860.944, 55.021` | `dist/extract/markers.jsonl` `q110_sm_sitting_in_maglev_temp` | `q110_lairs_escape_voodoo_boys` (7 VDB); enum `Coastview_VDBMaglev = 40` | `[game-data]` `[wiki]` |

### 3.1 Interior sub-locations (the reason to capture a building)

**NCART Memorial Park Station** is the only catalog point with a provable
interior, and it is the *station*, not the corporation's tower. All rows
`[game-data]`:

| Sub-location | Coordinates (x, y, z) | Record | Note |
| --- | --- | --- | --- |
| Site anchor (concourse) | `-1339.983, -17.944, -3.900` | site 350 `sts_cct_cpz_01` | `radius_m = 41.9`, `tier = 5`, `loot_tier = 3` |
| Station entrance trigger | `-1342.477, -21.395, -4.000` | trigger `#cpz_01_tr_entrance` | Matches `#cpz_01_tr_end` exactly |
| Inside guard area | `-1337.2, -16.0, -5.8` | guard area `#cpz_01_ga_inside` | The enclosed garrison volume |
| Outer guard area | `-1332.9, -15.3, -5.8` | guard area `#cpz_01_ga_01` | Lobby / platform edge |
| Server room | `-1338.300, -4.800, -8.000` | trigger `#cpz_01_tr_server_room` | The CCTV servers; lowest floor |
| Prisoner room | `-1341.600, -13.200, -4.000` | trigger `#cpz_01_tr_prisoner_room` | Works with `#cpz_01_ws_prisoner_001/_002` |
| Lower reinforcement spawn | `-1335.5, -49.4, 2.1` | workspot `#cpz_01_ws_reinforcement_001` | Second-level response route |
| Four doors | `TBD` | `#cpz_01_door_01..03`, `#cpz_01_dvc_shutters_002` | `doors.json` carries **no** positions (METHOD §1.2 item 14) |

Site-level facts (`data/sites/sites.json` site 350): `is_interior = 0` (the flag
is wrong — the concourse is at negative Z with doors and guard volumes),
`has_doors = 1`, `has_guard_areas = 1`, `patrol_count = 7`, `spot_count = 28`,
`community_count = 5`. `[game-data]`

**Night Corp Tower has no interior of its own.** The only local records are the
tour-hologram scene and the `#01_nc_tower_v` vista prefab; there is no lobby,
entrance, lift or floor marker for it. Compare Arasaka Tower, whose
lobby/atrium/CEO/rooftop are all named. `[game-data]`

### 3.2 How the name→coordinate links were proven

- **Night Corp Headquarters** — the wiki infobox gives `type = Corporate HQ`,
  `owner = Night Corp`, `district = City Center (2077)`,
  `sub_district = Downtown (2077)`, and the page states the tower is "not far
  from Corporate Plaza", "second tallest building in Night City after Arasaka
  Tower". The local anchor is the only real (non-centroid) `mq061` scene marker,
  `mq061_01_sm_nc_tower_scene`, and the *Welcome to Paradise* page describes the
  first holotour stop as "Crunch Plaza, Downtown, in front of the Night
  Corporation Tower". The prefab tree confirms the identity:
  `#01_mq061_nctower`, `#loc_mq061_openworld/#01_nc_tower_v/`,
  `#01_nc_tower_holo_start`. Cross-check: the marker is **373.6 m** from the
  Arasaka Tower lobby marker and **1,134.4 m** from City Hall — consistent with
  "Downtown, near Corporate Plaza, distinct from City Hall". `[game-data]` `[wiki]`
  **Caveat:** the marker sits at `z = 27.770`, ~20 m above street level. The
  nearby `{marker_}1..4` stack at `(-1800.7, 227.4)` reads z = 7.7 / 16.6 /
  27.7 / 39.7 — four storeys, i.e. the elevated Crunch Plaza decks, not the
  tower's base. The marker is a **tour-viewpoint anchor in front of the tower**,
  not its lobby. A capture volume wants the `z ≈ 7.7` street level; for the
  HQ record the tour anchor is the only named local record and is used as-is.
- **NCART Memorial Park Station** — the wiki infobox on *Gig: Serial Suicide*
  gives `baseid = sts_cct_cpz_01`, `location = NCART Memorial Park Station`,
  `district = City Center`, `sub_district = Corpo Plaza`, `enemies = Militech`.
  `sts_cct_cpz_01` is exactly site 350's `code`, and the site's node names are
  the station's (`#cpz_01_tr_entrance`, `#cpz_01_tr_server_room`,
  `#cpz_01_dvc_shutters_002`, `#cpz_01_ws_prisoner_*`). The station's
  sub-territory is `cpz_militech_hq`, matching the wiki's note that Militech
  took over station security. Cleanest `baseid` join in this doc. `[game-data]` `[wiki]`
- **Maglev Tunnel Construction Site** — *Forward to Death*'s `baseid` is
  `q114_02_maglev_line_assault`, and the marker `q114_mp_construction` carries
  the `q114` prefix. The wiki gives `owner = Night Corp`,
  `security_provider = Militech SiteSecure`, `region = Badlands`,
  `subregion = Rocky Ridge Plains`, "embedded in a hill … bordering on the
  northern parts of the North Oak district", tunnel running southwest to
  Corporate Plaza "pretty close to foundations of the new Arasaka Tower". The
  marker at `(249.1, 2428.8)` sits in the north-eastern Badlands, 851 m from
  the nearest sub-territory centroid (`nok_north_canyon`) and 638 m from the
  nearest site — position and description agree. `[game-data]` `[wiki]`
- **Northern Oil Fields** — wiki infobox `owner = Petrochem, SovOil, Night
  Corp`, `region = Badlands`, and the page records that Night Corp **brokered
  the Petrochem–SovOil peace** over these fields after the Fourth Corporate War.
  Local anchors are `{sq031_mp_oil_fields}` (barracks/pumps) and
  `{bls_bls_dataterm_}05` (the fast-travel term, which is also the seeded
  sub-territory anchor). `[game-data]` `[wiki]`
- **Old Maglev Tunnel** — wiki infobox `owner = Planetran (formerly)`,
  `Night Corp (de jure)`, `district = Pacifica`, `sub_district = Coastview`,
  `location = Beneath Pacifica Serenity Bible Church`, `gangs = Voodoo Boys`.
  The local record is the `q110` maglev cluster under the chapel, and
  `gamedataDistrict.Coastview_VDBMaglev = 40` is the game's own name for the
  place — with a **VDB** prefix, which is the whole story of the ownership.
  `[game-data]` `[wiki]`
- **Night Corp Solar Farm** — no local record at all. The three extracted
  sectors contain **no** `solar_array`, `solar_farm`, `photovolt` or `satwave`
  prefab node, and `areas.jsonl` has no solar-related community. The wiki gives
  only `region = Badlands`, `subregion = Jackson Plains`, "neighboring much of
  the functional Satwave Power Plant". Coordinate `TBD` per METHOD §6. `[wiki]`

### 3.3 Night Corp-occupied generic sites (the filler pool)

**Empty.** There is no site in the extract with `default_faction_id = 40` and
no site that carries a single faction-40 roster entry, so the filler pool is
zero by construction (METHOD §8: filler = deduped occupied sites minus
site-backed named places; 0 − 0 = 0). The nearest thing to a Night Corp site
row is site 350, which is a named catalog point (Memorial Park Station) and is
owned by nobody (`default_faction_id = null`).

---

## 4. Economic structure

### 4.1 Revenue streams → catalog locations

Night Corp earns from **civic infrastructure**, not from a product. Every
stream below is a contract with the city or a monopoly utility, which is why
the corp is politically embedded and militarily weak.

| Revenue stream | Code(s) | Catalog locations that produce it | Evidence / notes |
| --- | --- | --- | --- |
| Public-works construction and development | `real_estate` | HQ Tower (1); Maglev Tunnel Construction Site (3) | Wiki: "the largest contractor of public procurements within Night City's boundaries, building and renovating facilities such as roads, bridges, tunnels, metro lines, power plants, net transmitters, waterworks, sewerage". The vocabulary has no `construction`/`public_works` code; `real_estate` is the closest and is used deliberately. `[wiki]` `[inferred]` |
| Electricity generation | `energy` | Solar Farm (4); Northern Oil Fields (5, feedstock, joint) | Wiki: the arrays "began fulfilling a substantial amount of the city's energy needs"; the oil fields are "a joint project of Petrochem and Night Corp". **Both are dead or shared in 2077** — the arrays are inactive and the fields are three-way owned. `[wiki]` |
| Mass transit | `logistics` | Memorial Park Station (2); the maglev tunnel (3); Old Maglev Tunnel (6, de jure) | NCART (subsidiary since 2068) runs the metro and streetcars citywide; the maglev revival is planned to reach Corporate Plaza in 2078 and Chicago by 2080. `[wiki]` |
| Water, sewerage, net transmitters | `energy` *(closest)* | No mapped site | Wiki lists waterworks and sewerage among its builds, but the 2077 map has no Night Corp water or sewer facility with a marker. The Night City Department of Water is a **government** body, not Night Corp. Recorded here and left out of the JSON. `[wiki]` |
| Fuel/energy royalties | — *(not Night Corp)* | Northern Oil Fields (5) | The CHOOH2 **patents** are Biotechnica's; the fields are extraction. Do not credit `energy` royalties to Night Corp beyond its field share. `[wiki]` |

Not claimed, and why:

- **`finance`** — the wiki mentions orbital projects and "shares", but nothing
  in Night City is a bank or exchange. Not modelled.
- **`security_services`** — Night Corp **buys** security (Lazarus at the solar
  farm in 2045, Militech SiteSecure at the tunnel) and never sells it. Counting
  its garrisons as a security business would invert the relationship.
- **`information` / `netrunning`** — the corp does run a covert AI-conditioning
  programme (*Dream On*, and the Sandra Dorsett databank theft). That is a
  liability and an intelligence capability, not a revenue line, and it has no
  Night Corp-owned site. Kept in §8, not in the economy.

### 4.2 Suppliers, customers, rivals

| Role | Party | Detail |
| --- | --- | --- |
| Subsidiary | **NCART** | Bought out in 2068 after poison-gas attacks bankrupted the transit corporation. NCART is Night Corp's only known subsidiary and the source of its transit revenue. `[wiki]` |
| Joint-venture partner (power) | **PacCon Electric** | Manages the Jackson Plains solar farm; also manages the city-owned Wind Farms. `[wiki]` |
| Joint-venture partner (oil) | **Petrochem**, **SovOil** | Three-way ownership of the Northern Oil Fields; Night Corp brokered the peace between the two rivals there. `[wiki]` |
| Contractor (security) | **Militech** ("SiteSecure") | Hired to protect the maglev tunnel works. This is the garrison the extract actually records. `[wiki]` `[game-data]` |
| Contractor (security, historic) | **Lazarus** | Provided the solar-farm patrols and drone surveillance in the 2040s. `[wiki]` |
| Customer | **City of Night City** | Public procurement is the business model; the corp also funds the NCPD and MaxTac. `[wiki]` |
| Political instrument | **Thomas Star / Holt / Peralez administrations** | The corp's AI programme targets mayoral candidates; Jefferson Peralez was a Night Corp scholarship recipient before being conditioned. `[wiki]` |
| Estranged partner | **Orbital Air** | Night Corp cut all ties after OA abandoned the mass-driver project at the NCX Spaceport, and the two are in a cold war by 2077. `[wiki]` |
| Rival | **Arasaka**, **Militech** | Lost the corporate-power race to both; Arasaka Tower is 374 m from Night Corp Tower and both now outrank it. `[wiki]` `[game-data]` |
| Counterparty (de facto) | **Voodoo Boys** | Hold Night Corp's de jure maglev tunnel under the Coastview chapel as a data fortress. `[wiki]` `[game-data]` |

---

## 5. Headquarters recommendation

### Primary HQ: **Night Corp Headquarters (Night Corp Tower)** — Downtown

Coordinates: `(-1809.430, 233.868, 27.770)` `[game-data]`
`dist/extract/markers.jsonl mq061_01_sm_nc_tower_scene`.

Rationale:

1. **It is the canon seat, and the only one.** The wiki gives
   `type = Corporate HQ`, `owner = Night Corp`, `district = City Center (2077)`,
   `sub_district = Downtown (2077)`; the corp's own page names it as the
   headquarters. There is no competing candidate — Night Corp has one tower,
   one transit hub and three infrastructure sites. `[wiki]`
2. **Downtown is the right neighbourhood and it is the corp's own.** The tower
   sits in `dtn_corporation_st` (Corporation Street Arcade), the seeded
   sub-territory named for the corporate street it fronts, 143 m from that
   centroid. Downtown, not Corpo Plaza — the seeded map agrees with the wiki.
   `[game-data]`
3. **The local anchor is real, not centroid-snapped.** Unlike ten of the twelve
   `mq061_*_sm_*` tour markers (all pinned at `(-1317.810, -84.292, 0.000)`),
   `mq061_01_sm_nc_tower_scene` has a distinct position, and the prefab tree
   names the tower explicitly (`#01_mq061_nctower`, `#01_nc_tower_v`). This is
   the one tour stop where the marker means something. `[game-data]`
4. **Scale is right.** The tower is the second-tallest building in the city — a
   better seat for a corp whose whole business is the city's skyline than any
   of its Badlands works. `[wiki]`
5. **The city's weight sits within 400 m.** The tower is 374 m from Arasaka
   Tower's lobby, i.e. embedded in the corporate core the corp is losing to
   Arasaka — which is the faction's actual story. `[game-data]`

Trade-off — **this is a scenery anchor, not a building anchor**, and the worst
kind for a capture prototype:

- **No `sites.json` row, no interior, no doors, no guard volumes, no roster, no
  community.** Nothing to evict and nothing to defend. Every other HQ in this
  series at least had a scanner-hustle volume; this one has none.
- **The marker is a tour viewpoint, ~20 m above street level**, on the elevated
  Crunch Plaza decks in front of the tower (see §3.2). It is not the lobby and
  not the base. For a point-scale capture volume, use the `z ≈ 7.7` bottom of
  the `{marker_}` stack at `(-1800.7, 227.4)` instead.
- **The nearest control centre is a rival's.** `cc_dtn_corporation_st`,
  143.0 m, is seeded to **Valentinos** (`initial_owner_faction_id = 2`,
  `is_active = 0`). Per METHOD §1.1 item 10, do not retarget by nearest CC;
  move the CC onto the tower's own coordinates.
- **`dtn_corporation_st` is also the wrong owner for the block.** The seed gives
  the arcade to Tyger Claws; there is no evidence either way in the extract
  (site `ma_cct_dtn_07`, 92 m away, is `default_faction_id = 2`). Night Corp
  taking the block means taking it from the Claws, which is plausible for a corp
  reclaiming its own street — but it is a design decision, not a data one.

### Alternate 1: **NCART Memorial Park Station** — Corpo Plaza

Coordinates: `(-1339.983, -17.944, -3.900)` `[game-data]`
`data/sites/sites.json` site 350 `sts_cct_cpz_01`.

A genuine, enclosed, well-recorded seat: an underground concourse with a
server room, a prisoner room, 3 guard areas, 7 patrol splines and 28 workspots,
on a site row that already exists. It loses as HQ only because the wiki's HQ is
the Downtown tower, and because the station is a *facility* — the corp's hub, not
its boardroom. It is the recommended **test point** (§6) precisely because it is
the best-instrumented Night Corp-relevant place in the game. `[game-data]` `[wiki]`

### Alternate 2: **Maglev Tunnel Construction Site** — Badlands

Coordinates: `(249.137, 2428.782, 67.081)` `[game-data]`
`dist/extract/markers.jsonl q114_mp_construction`.

The faction's flagship 2077 project and the only place with Night Corp-branded
assets (workspots, cars, an AV spawn, a tunnel gate). It loses as HQ because it
is a construction site in the Badlands with no permanent building, because its
garrison is Militech's, and because it has no `sites.json` row at all —
16 community areas, zero site-keyed capture records. Good *raid target*, poor
*seat*. `[game-data]` `[wiki]`

### Overruled / downgraded suggestions

- **City Hall as a Night Corp seat** — a trap worth naming. The corp is the
  city's contractor and the `mq061` tour visits City Hall, which makes it look
  like a holding. It is not: the wiki infobox gives
  `owner = Government of Night City`, `district = Heywood`,
  `sub_district = The Glen`, 1,134 m from the tower and in a different district.
  The only local record is `{mq061_city_hall_drone_com}` at
  `(-1775.1, -933.1, 13.9)`, one entry, no faction. **City Hall is the City
  Council's, and the two buildings are not the same.** `[wiki]` `[game-data]`
- **The Night Corp Solar Farm as an HQ** — no coordinate, no garrison, and
  inactive in 2077 (§8.2). It is the corp's most iconic *asset* and its worst
  *seat*.
- **The Old Maglev Tunnel as a Night Corp point of any weight** — de jure only;
  `gamedataDistrict.Coastview_VDBMaglev` is the game's own naming and it says
  VDB. Rank 6 at relevance 2; the Voodoo Boys doc already claims it. `[game-data]`
- **The `mq061` tour stops as holdings** — a holotour is not a lease. Ten of the
  twelve scene markers are the same centroid; the stops named in the quest
  (Memorial Park, Arasaka Memorial, City Hall, Biotechnica Farms, an NCART
  station, the Coronado Dam viewpoint, the Med Center, Bellevue Overwalk) are
  places the tour *points at*, not places Night Corp owns. Do not seed them.
  `[game-data]` `[wiki]`
- **`NC Dam Ltd.` as a Night Corp subsidiary** — different corporation. It built
  the Laguna Bend dam in 2062; the Coronado Dam's infobox names the *Government
  of Night City* and NCDW/Petrochem as owners/managers, not Night Corp. The
  "NC Dam" link on the Night Corp wiki page comes from the shared corporation
  navbox, not from the article. `[wiki]`
- **Night City Ferry Corp** — 2020-era private ferry operator, unrelated; also
  navbox noise. `[wiki]`

---

## 6. Priority list of control points

Ranked by how well each place serves as a capturable Night Corp control point.
"CC" = nearest entry in `data/control_centers.json` (all CCs, active or not);
distance is horizontal metres; the owner column is the CC's sub-territory owner
per METHOD §1.1 item 10.

| Rank | Control point | Rel. (1–5) | District / sub-district | Coordinates | Existing CC overlap | Why |
| ---: | --- | :---: | --- | --- | --- | --- |
| 1 | **Night Corp Headquarters (Tower)** | 5 | CityCenter / Downtown | `-1809.430, 233.868, 27.770` | `cc_dtn_corporation_st`, 143.0 m (**Valentinos**, inactive) | HQ. Canon seat, real marker, second-tallest building, 374 m from Arasaka Tower. No interior, no site row |
| 2 | **NCART Memorial Park Station** | 5 | CityCenter / CorpoPlaza | `-1339.983, -17.944, -3.900` | `cc_cpz_militech_hq`, 49.4 m (**Militech**, inactive) | **Test point.** Subsidiary's central hub; real site 350; enclosed concourse; 3 guard areas, 7 patrols, 4 doors, 28 spots, 15 roster entries |
| 3 | **Maglev Tunnel Construction Site** | 4 | Badlands / Badlands | `249.137, 2428.782, 67.081` | `cc_nok_north_canyon`, 851.2 m (**Tyger Claws**, inactive) | Flagship project; the only Night Corp-branded assets (9 workspots, 4 cars, AV, gate); garrison is Militech |
| 4 | **Night Corp Solar Farm** | 4 | Badlands / Badlands | `TBD` | Unknown; no marker | Iconic `energy` asset, inactive by 2077; **no local record of any kind** |
| 5 | **Northern Oil Fields** (joint) | 3 | Badlands / Badlands | `-1845.399, 3855.277, 7.442` | `cc_bls_north_oil_fields`, 136.3 m (**Militech**, inactive) | One of three owners; Petrochem's doc already claims it; `energy` feedstock |
| 6 | **Old Maglev Tunnel** (Rezo Agwe) | 2 | Pacifica / Coastview | `-1665.273, -1860.944, 55.021` | `cc_cvi_rollercoaster_beach`, 349.8 m (**Voodoo Boys**, inactive) | De jure only; VDB data fortress; contested with Voodoo Boys doc |

### Test control point for the first in-game test: **NCART Memorial Park Station**

Site 350 `sts_cct_cpz_01`, coordinates `(-1339.983, -17.944, -3.900)`
`[game-data]` `data/sites/sites.json`.

METHOD §3.8's first criterion (`default_faction_id == FID`) **cannot be met by
any Night Corp site** — none exists. This doc therefore uses the documented
fallback (criteria 2 and 3: record richness and enclosure) on a place the
faction de jure owns through NCART. Why this and not the HQ:

- **It is the only Night Corp-relevant place with a full capture record set.**
  Site 350 carries 3 guard areas (`#cpz_01_ga_01`, `#cpz_01_ga_inside`,
  `#cpz_01_rma_workers`), 7 patrol splines
  (`#cpz_01_spl_patrol_guard_001..003`, `#cpz_01_spl_guard_005*`,
  `#cpz_01_spl_worker_spline`), 4 doors (`#cpz_01_door_01..03`,
  `#cpz_01_dvc_shutters_002`), 28 workspots, 15 triggers and 15 roster entries
  including droids and an officer. The construction site has none of this in
  `sites.json`; the tower has nothing at all. `[game-data]`
- **It is genuinely enclosed and multi-level.** Concourse at `z ≈ −4`, server
  room at `z ≈ −8`, reinforcement spawns at `z ≈ +2`: a vertical capture volume
  with a real ceiling, not a radius on a fence. `[game-data]`
- **The garrison story is unambiguous.** `Character.sts_cct_cpz_01_enemy_security*`
  (including `_droid_shotgun` and `_officer`) plus
  `Character.sts_cct_cpz_01_workers`: Militech's temporary station security,
  exactly as the wiki describes. Capturing it exercises "take a Night Corp asset
  from its contract security" rather than "evict Night Corp from Night Corp".
  `[game-data]` `[wiki]`
- **It is not the HQ**, so the first test exercises capture on a non-seat, as
  METHOD §3.8 requires. `[game-data]`

Trade-off: `default_faction_id` is **null** and the site's own sub-territory
(`cpz_militech_hq`) is Militech's, so a seeder cannot find this point by either
faction field. It must retarget by coordinates. The station is also 49.4 m from
`cc_cpz_militech_hq` — a nearest-CC retarget would hand it straight back to
Militech. `[game-data]`

Second test, when an outdoor volume is wanted: **Maglev Tunnel Construction
Site** (`q114_mp_construction`), which has the richest *area* evidence anywhere
in the faction (16 `q114` community areas within 120 m) and no site row at all —
a useful contrast case for area-only capture. Its nearest CC is 851 m away, so
it also tests a from-scratch control-centre placement.

---

## 7. Per-sub-district counts

| Sub-district | Named lore-relevant places | Which ones | Night Corp-occupied sites (deduped) | Filler | Noteworthy interiors |
| --- | ---: | --- | ---: | ---: | --- |
| Downtown | **1** | Night Corp Headquarters (Tower) | 0 | 0 | None (scenery; tour-deck marker only) |
| CorpoPlaza | **1** | NCART Memorial Park Station | 1 | 0 | Station concourse, server room, prisoner room |
| Badlands | **3** | Night Corp Solar Farm, Maglev Tunnel Construction Site, Northern Oil Fields | 0 | 0 | None (all open sites) |
| Coastview | **1** | Old Maglev Tunnel (de jure) | 0 | 0 | Maglev tunnel + vault (Voodoo Boys) |
| **Total** | **6** | | 1 | **0** | 2 |

Reconciliation: **1** deduped occupied site − **1** site-backed named place
(Memorial Park Station, site 350) = **0 filler**. The other five named places are
not `sites.json` rows: two are marker-only (the tower, the oil fields), one is
marker-only with no marker at all (the solar farm → `TBD`), one is a
marker/community cluster (the construction site), and one is another faction's
site (the Old Maglev Tunnel). `named + filler = 6`, which is the 1 site plus the
5 non-site named places. `[game-data]`

Caveat on "named": **two of the six have no seedable coordinate** (the solar
farm is `TBD`) or no capture record at all (the tower). A seeder reading this
table should place **four** points confidently (tower, station, construction
site, oil fields) and treat the solar farm as a survey task and the tunnel as
contested. Do not synthesise coordinates for the missing two.

Interpretation for yield: Night Corp is a **six-point faction with a
high-multiplier core and no filler**. The honest read is that its value is
concentrated in the tower (prestige/civic control) and transit (NCART), with the
Badlands contributing infrastructure scale rather than business density.
Filling the map with "Night Corp blocks" is impossible: the faction has zero
occupied sites, so a filler count above zero would be fabrication.

---

## 8. Gaps and uncertainties

1. **Night Corp has no affiliation value in the game at all.** `data/factions.json`
   gives `affiliation_enum = null`, and the full `gamedataAffiliation` enum
   (44 values, `refs/cyberpunk/orphans.swift`) contains no Night Corp entry —
   not even `corpbud` or `UnaffiliatedCorpo` as a stand-in. This is stronger than
   "no ganger roster": the game has **no way to tag an NPC as Night Corp**.
   Anything claiming Night Corp presence must come from place records. `[game-data]`
2. **The extract contains no Night Corp character record whatsoever.** No
   `Character.*night*` record exists except unrelated `Nightlife*`,
   `q004_nightclub_patron`, `q303_nighthawks_*` and `reed_night_city`. The
   `night_corpo_male` / `night_corpo_female` / `night_corpo_ma_static` CName
   entries in `always_loaded_1` are **Vista del Rey metro ambient workspot and
   crowd entry names** (`#vista_del_rey_metro_ws_night_corpo_001`), referring to
   "night" corporate commuters, not to Night Corp. I checked the community
   registry: zero communities contain a `night_corpo` entry. Do not read these
   as Night Corp presence. `[game-data]`
3. **The Night Corp Solar Farm has no coordinate and no record.** No marker, no
   site, no community area, no prefab node in the three extracted sectors. The
   wiki puts it "neighboring much of the functional Satwave Power Plant" on the
   Jackson Plains, and the arrays are static scenery. **The seed's numbers are
   not evidence**: `tools/generate-world-seeds.py` typed
   `(50.4, -5595.4, 212.8)` for `bls_solar_station`, which no marker or area
   corroborates and whose `z = 212.8` is ~120 m above the surrounding terrain
   (nearby markers read z ≈ 85–100); the shipped seed then moved the same zone
   onto the **Militech Detention Center** at `(-112.566, -5246.731, 87.160)`
   via `LORE_TEST_POINTS`. Two different "solar" coordinates in one repo,
   neither of them the arrays. `[game-data]` `[wiki]`
4. **The seed credits the solar arrays to Militech.** Sub-territory 89
   (`bls_solar_station`, owner 21, CC `is_active = 1`) is the bucket the two
   detention-centre sites fell into; its display name is now "Militech Detention
   Center" but its code still says solar. The Militech doc §8.4 already flags
   this. For Night Corp the consequence is that its single most iconic energy
   asset currently sits inside a rival's active control centre. `[game-data]`
5. **Night Corp Tower has no interior, no site row and no lobby.** The tower is
   scenery plus a `mq061` tour scene; the only records are the hologram deck and
   a vista prefab. A corp HQ with zero gameplay nodes is the extreme version of
   the pattern the Arasaka and Kang Tao docs recorded — and unlike them, Night
   Corp does not even get a scanner-hustle volume at its base. `[game-data]`
6. **The HQ marker is a tour viewpoint, not a building anchor.** `z = 27.770`
   is ~20 m above the street, on the Crunch Plaza decks; the `{marker_}` stack
   10 m away spans z = 7.7 → 39.7. The wiki's tour text confirms the stop is
   "Crunch Plaza, Downtown, in front of the Night Corporation Tower". Use it for
   the HQ *record*, not for a capture volume. `[game-data]` `[wiki]`
7. **"Night Corp Tower" and "City Hall" are frequently conflated and must not
   be.** City Hall is in the **Glen, Heywood** (`owner = Government of Night
   City`), 1,134 m from the tower and in a different district. Night Corp is the
   city's contractor and funds the NCPD, which is why the confusion is
   tempting. The only local City Hall record is one
   `{mq061_city_hall_drone_com}` area with 1 entry and no faction. `[wiki]` `[game-data]`
8. **North Corp's visible "security" at its own flagship site is Militech's.**
   `{q114_com_construction_nc_security}` is **six Militech medium drones**, and
   `{q114_com_construction_combat_nc_control_room}` is **two Militech snipers**.
   The corp's actual on-site employees are two generic `Character.WorkerMale`.
   This is METHOD §2.3 item 4 ("machines are not a garrison") plus a stronger
   rule: **the garrison may be a third-party contractor**, and here it is. A
   capture design that assumes "garrison faction = owner faction" will invert
   the lore at this site. `[game-data]` `[wiki]`
9. **The Northern Oil Fields are jointly owned, and the schema has no place to
   say so.** The wiki lists `owner = Petrochem, SovOil, Night Corp`, and Night
   Corp brokered the peace between the other two. The JSON contract allows one
   owner per point, so the same place is claimed by this doc, by the Petrochem
   doc and implicitly by SovOil. It needs a `co_owners` field or an explicit
   rule; the alternative is three docs each asserting exclusive ownership.
   `[wiki]`
10. **The Old Maglev Tunnel is contested with the Voodoo Boys doc.** Both docs
    cite the same marker (`q110_sm_sitting_in_maglev_temp`) with different
    rationale: de jure (Night Corp) versus de facto (VDB). The Voodoo Boys doc
    ranks it 5th at relevance 4 as their data fortress; this doc ranks it 6th at
    relevance 2. Whatever owns capture resolution needs an explicit
    "de jure vs de facto" precedence rule. `[game-data]` `[wiki]`
11. **`mq061` tour stops are not holdings, but they look like them.** The quest
    names nine Night City landmarks; ten of the twelve `mq061_*_sm_*_scene`
    markers are pinned to the same point `(-1317.810, -84.292, 0.000)`. Only
    `mq061_01` (tower) and `mq061_13` (end scene) are real. A future agent
    grepping `mq061` will find a tidy list of "Night Corp" landmarks and seed
    all of them; that would be a fabrication. `[game-data]` `[wiki]`
12. **The corp's covert capability has no site.** The AI-conditioning programme
    (*Dream On*: `baseid = sq006_dream_on`) runs out of the Peralezes'
    apartment's roof transmitter and a Maelstrom compound near All Foods, and
    the Sandra Dorsett databank theft happens in a scav den. All are quest
    corridors where Night Corp operates covertly, not holdings — METHOD §1.2
    item 9 puts them under Gaps, and I have not counted them. `[wiki]`
13. **NCART's 2077 asset list is real but mostly not mappable.** The network is
    a subsidiary asset with 5 lines and 19 stations, but the extract has no
    Night Corp-tagged station beyond the one Memorial Park site row. Other
    documented stations (City Center, Plaza Center, Reclamation Zone, the
    unfinished West Wind Estate station held by Animals) have their own records
    and their own owners; claiming them for Night Corp would be a stretch of the
    subsidiary relationship into a claim on the city's whole metro. `[wiki]`
14. **`income_multiplier 1.45` is the highest in the megacorp group and is not
    supported by any extract data.** It is a seed design value. With zero
    occupied sites, there is nothing to multiply; the multiplier only becomes
    real once the six points above are placed. Worth confirming that a
    zero-footprint faction should carry the top income multiplier. `[game-data]`

---

## 9. Sources

Local:

- `dist/extract/markers.jsonl` — `mq061_01_sm_nc_tower_scene` (HQ),
  `q114_mp_construction` (tunnel site), `q110_sm_sitting_in_maglev_temp` (old
  tunnel), `sq031_mp_oil_fields` and `{bls_bls_dataterm_}05` (oil fields), the
  ten centroid-snapped `mq061` tour stops, `{mq061_city_hall_drone_com}`.
- `dist/extract/areas.jsonl` — confirms zero `night_corp` areas; supplies the 16
  `q114` construction-site communities and their character records.
- `data/sites/sites.json` — site 350 `sts_cct_cpz_01` (Memorial Park Station)
  and the 92 m-away `ma_cct_dtn_07`; no site anywhere with
  `default_faction_id = 40`.
- `data/sites/{guards,triggers,spots,patrols,doors,communities,rosters}.json` —
  the station's interior sub-locations and its 15 roster entries.
- `data/{factions,districts,sub_territories,landmarks,control_centers,faction_headquarters,spawn_points}.json`
  — faction id 40 with `affiliation_enum: null`; zero ownership rows; CC owners
  and distances.
- `dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_{0,1,2}.streamingsector.json`
  — the `q114_nightcorp_*` node and prefab inventory, the
  `#01_mq061_nctower` / `#01_nc_tower_v` tour prefab tree, the absence checks for
  a solar-farm prefab, and the `#vista_del_rey_metro_ws_night_corpo_*` decoy.
- `refs/cyberpunk/orphans.swift` — full `gamedataAffiliation` (44 values, no
  Night Corp) and `gamedataDistrict` (no Night Corp entry; `Coastview_VDBMaglev
  = 40`, `Badlands_JacksonPlains = 15`).
- `tools/generate-world-seeds.py` — the `bls_solar_station` zone row
  (`50.4, -5595.4, 212.8`) and the `LORE_TEST_POINTS` override that moves it to
  the Militech Detention Center; zero zones owned by 40.

Wiki (MediaWiki API, wikitext only):

- [Night Corp](https://cyberpunk.fandom.com/wiki/Night_Corp)
- [Night Corp Headquarters](https://cyberpunk.fandom.com/wiki/Night_Corp_Headquarters)
- [NCART](https://cyberpunk.fandom.com/wiki/Night_City_Area_Rapid_Transit) ·
  [NCART Memorial Park Station](https://cyberpunk.fandom.com/wiki/NCART_Memorial_Park_Station) ·
  [NCART Rail Network](https://cyberpunk.fandom.com/wiki/NCART_Rail_Network) ·
  [NCART Yards](https://cyberpunk.fandom.com/wiki/NCART_Yards)
- [Maglev Tunnel Construction Site](https://cyberpunk.fandom.com/wiki/Maglev_Tunnel_Construction_Site) ·
  [Old Maglev Tunnel](https://cyberpunk.fandom.com/wiki/Old_Maglev_Tunnel)
- [Night Corp Solar Farm](https://cyberpunk.fandom.com/wiki/Night_Corp_Solar_Farm) ·
  [Satwave Power Plant](https://cyberpunk.fandom.com/wiki/Satwave_Power_Plant) ·
  [Jackson Plains](https://cyberpunk.fandom.com/wiki/Jackson_Plains)
- [Northern Oil Fields](https://cyberpunk.fandom.com/wiki/Northern_Oil_Fields)
- [Night City Hall](https://cyberpunk.fandom.com/wiki/Night_City_Hall) ·
  [Crunch Plaza](https://cyberpunk.fandom.com/wiki/Crunch_Plaza)
- [Welcome to Paradise](https://cyberpunk.fandom.com/wiki/Welcome_to_Paradise) (`baseid = mq061`)
- [Forward to Death](https://cyberpunk.fandom.com/wiki/Forward_to_Death) (`baseid = q114_02_maglev_line_assault`)
- [Gig: Serial Suicide](https://cyberpunk.fandom.com/wiki/Gig:_Serial_Suicide) (`baseid = sts_cct_cpz_01`)
- [Dream On](https://cyberpunk.fandom.com/wiki/Dream_On) (`baseid = sq006_dream_on`)
- [Night City Department of Water](https://cyberpunk.fandom.com/wiki/Night_City_Department_of_Water) ·
  [NC Dam](https://cyberpunk.fandom.com/wiki/NC_Dam) ·
  [Night City Ferry Corp](https://cyberpunk.fandom.com/wiki/Night_City_Ferry_Corp) —
  consulted and **not** attributed to Night Corp (see §5).
- [PacCon Electric](https://cyberpunk.fandom.com/wiki/PacCon_Electric) ·
  [Lazarus](https://cyberpunk.fandom.com/wiki/Lazarus)

Earlier repo research:

- [`docs/research/factions/METHOD.md`](./METHOD.md)
- [`docs/research/factions/militech.md`](./militech.md) (§8.4, the solar-artifact finding)
- [`docs/research/factions/petrochem.md`](./petrochem.md) (joint oil-field ownership)
- [`docs/research/factions/voodoo-boys.md`](./voodoo-boys.md) (Old Maglev Tunnel)
- [`docs/research/factions/biotechnica.md`](./biotechnica.md) (§8.4, `mq061` tour markers)
- [`docs/research/factions/kang-tao.md`](./kang-tao.md) (corp with no interior)

---

## 10. Machine-readable block

Strict JSON for seeding (contract in [`METHOD.md`](./METHOD.md) §10). Every
coordinate was verified against the local record named in `source` on
2026-11-25; none came from the wiki. `null` means `TBD`, never `0`.

```json
{
  "faction_code": "night_corp",
  "hq": {
    "name": "Night Corp Headquarters (Night Corp Tower)",
    "district": "CityCenter",
    "sub_district": "Downtown",
    "x": -1809.43,
    "y": 233.868,
    "z": 27.77,
    "source": "dist/extract/markers.jsonl mq061_01_sm_nc_tower_scene (tour-viewpoint marker in front of the tower; street level is z 7.7)",
    "confidence": "game-data+wiki"
  },
  "alternate_hqs": [
    {
      "name": "NCART Memorial Park Station",
      "district": "CityCenter",
      "sub_district": "CorpoPlaza",
      "x": -1339.983,
      "y": -17.944,
      "z": -3.9,
      "source": "data/sites/sites.json site 350 sts_cct_cpz_01",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Maglev Tunnel Construction Site",
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": 249.137,
      "y": 2428.782,
      "z": 67.081,
      "source": "dist/extract/markers.jsonl q114_mp_construction",
      "confidence": "game-data+wiki"
    }
  ],
  "test_control_point": {
    "name": "NCART Memorial Park Station",
    "district": "CityCenter",
    "sub_district": "CorpoPlaza",
    "x": -1339.983,
    "y": -17.944,
    "z": -3.9,
    "source": "data/sites/sites.json site 350 sts_cct_cpz_01; node positions data/sites/triggers.json #cpz_01_tr_entrance",
    "confidence": "game-data+wiki"
  },
  "control_points": [
    {
      "rank": 1,
      "name": "Night Corp Headquarters (Night Corp Tower)",
      "type": "corporate_hq",
      "relevance": 5,
      "district": "CityCenter",
      "sub_district": "Downtown",
      "x": -1809.43,
      "y": 233.868,
      "z": 27.77,
      "source": "dist/extract/markers.jsonl mq061_01_sm_nc_tower_scene (tour-viewpoint marker in front of the tower; street level is z 7.7)",
      "confidence": "game-data+wiki",
      "interior": false,
      "revenue_streams": ["real_estate", "energy", "logistics"],
      "nearest_cc_code": "cc_dtn_corporation_st",
      "nearest_cc_m": 143.0
    },
    {
      "rank": 2,
      "name": "NCART Memorial Park Station",
      "type": "metro_hub_station",
      "relevance": 5,
      "district": "CityCenter",
      "sub_district": "CorpoPlaza",
      "x": -1339.983,
      "y": -17.944,
      "z": -3.9,
      "source": "data/sites/sites.json site 350 sts_cct_cpz_01",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["logistics"],
      "nearest_cc_code": "cc_cpz_militech_hq",
      "nearest_cc_m": 49.4
    },
    {
      "rank": 3,
      "name": "Maglev Tunnel Construction Site",
      "type": "construction_site",
      "relevance": 4,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": 249.137,
      "y": 2428.782,
      "z": 67.081,
      "source": "dist/extract/markers.jsonl q114_mp_construction",
      "confidence": "game-data+wiki",
      "interior": false,
      "revenue_streams": ["real_estate", "logistics"],
      "nearest_cc_code": "cc_nok_north_canyon",
      "nearest_cc_m": 851.2
    },
    {
      "rank": 4,
      "name": "Night Corp Solar Farm",
      "type": "solar_power_station",
      "relevance": 4,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": null,
      "y": null,
      "z": null,
      "source": "no local record; wiki infobox only (owner = Night Corp, manager = PacCon Electric, subregion = Jackson Plains) - coordinate TBD",
      "confidence": "wiki",
      "interior": false,
      "revenue_streams": ["energy"],
      "nearest_cc_code": null,
      "nearest_cc_m": null
    },
    {
      "rank": 5,
      "name": "Northern Oil Fields",
      "type": "oil_field",
      "relevance": 3,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": -1845.399,
      "y": 3855.277,
      "z": 7.442,
      "source": "dist/extract/markers.jsonl sq031_mp_oil_fields",
      "confidence": "game-data+wiki",
      "interior": false,
      "revenue_streams": ["energy"],
      "nearest_cc_code": "cc_bls_north_oil_fields",
      "nearest_cc_m": 136.3
    },
    {
      "rank": 6,
      "name": "Old Maglev Tunnel (Rezo Agwe)",
      "type": "abandoned_maglev_tunnel",
      "relevance": 2,
      "district": "Pacifica",
      "sub_district": "Coastview",
      "x": -1665.273,
      "y": -1860.944,
      "z": 55.021,
      "source": "dist/extract/markers.jsonl q110_sm_sitting_in_maglev_temp",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["logistics"],
      "nearest_cc_code": "cc_cvi_rollercoaster_beach",
      "nearest_cc_m": 349.8
    }
  ],
  "subdistrict_counts": {
    "Downtown": {"named": 1, "filler": 0},
    "CorpoPlaza": {"named": 1, "filler": 0},
    "Badlands": {"named": 3, "filler": 0},
    "Coastview": {"named": 1, "filler": 0}
  }
}
```
