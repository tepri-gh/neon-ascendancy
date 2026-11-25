# Arasaka — Lore-Relevant Control Points

Status: faction research run, 2026-11-25. One faction, one document.
Scope: replace the generic control-centre grid with places Arasaka actually
owns, runs, protects or garrisons in Night City, with verified coordinates, an
economic map, an HQ pick, a ranked capture list and honest per-sub-district
counts. Method: this doc conforms to [`METHOD.md`](./METHOD.md); snippets, wiki
rules, the revenue-code vocabulary and the JSON contract live there.
`AGENTS.md` was read first. No commits, no game launch.

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Position, site, community, roster or spawn record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/artbook/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My reasoning links a named place to a game record; reasoning stated | Weak, flagged |

No coordinate below is guessed. Every `(x, y, z)` is copied from a local marker,
site, seed anchor or community-area record, or marked `TBD`.

---

## 1. Summary

Arasaka (荒坂社) is the world's largest corporate-security and manufacturing
megacorp: 595,000+ employees and ¥98 trillion / €$890 billion in 2077, with a
Tokyo headquarters and a Night City **North American Division HQ** in
**Corpo Plaza**. Its declared business is corporate security, banking and
manufacturing; its armed forces are the largest of any corporation, and it
licenses guards, couriers and mercenaries to other firms. `[wiki]`

The Night City footprint is a corporate campus, not a street gang:

- **Corpo Plaza (City Center)** — Arasaka Tower, the Arasaka Memorial, the
  Arasaka Port section of the Corpo Plaza Docks, and the Memorial Ring West
  holding. This is the administrative, financial and military heart.
- **Arasaka Waterfront (Watson)** — Konpeki Plaza and a walled port/logistics
  complex (North Cargo Pier, Freight Terminal, South Quay). `[wiki]` `[game-data]`
- **Arroyo (Santo Domingo)** — the Arasaka Industrial Park: warehouses,
  manufacturing, vehicle/AV retrofit and one of the city's largest supply
  depots. `[wiki]`
- **North Oak (Westbrook)** — the Arasaka Estate and the Arasaka-guarded
  North Oak Columbarium. `[wiki]`
- **Charter Hill (Westbrook)** — a seeded power substation and a seeded luxury
  terrace block; the latter is Kiroshi Campus in lore and is **not** an Arasaka
  business. `[wiki]` `[game-data]`

Game-data scale: **146 community areas** contain Arasaka spawns, **126** are
Arasaka-dominant, the faction owns **12 seeded sub-territories**, and its
security units occupy **8 sites / 68 roster entries**. The weight sits in
Corpo Plaza (54 areas, 630 Arasaka entries), then Arroyo (the Industrial Park),
the Waterfront (Konpeki) and North Oak. `[game-data]`

---

## 2. Territory

### 2.1 Districts

| Evidence kind | Result |
| --- | --- |
| (a) Wiki/lore | Global HQ Tokyo; Night City North American HQ at Arasaka Tower, Corporate Plaza, City Center. Facilities in Watson (Arasaka Waterfront), Santo Domingo (Arroyo), Westbrook (North Oak, Charter Hill) and City Center (Corpo Plaza Docks). `[wiki]` |
| (b) Vanilla map gang panel | **Not applicable.** `data/districts.json` `vanilla_gangs` lists gangs only; megacorps are absent from the gang panel by design. This is the first faction in the set where evidence (b) is structurally empty, not missing. |
| (c) Game-data counts | 146 community areas contain Arasaka; 126 are Arasaka-dominant. 12 owned sub-territories. 8 roster sites / 68 units. 21 distinct security character records. `[game-data]` |

The 12 owned sub-territories (`data/sub_territories.json`,
`initial_owner_faction_id = 20`): Konpeki Plaza Approach, Arasaka North Cargo
Pier, Waterfront Freight Terminal, Waterfront South Quay (ArasakaWaterfront);
Charter Hill Substation, Charter Hill Terraces (CharterHill); Arasaka Estate
Gate, North Oak Columbarium, North Oak Villa Ridge (NorthOaks); Arasaka
Industrial Park (Arroyo); Arasaka Tower Plaza, Memorial Ring West (CorpoPlaza).
`[game-data]`

### 2.2 Sub-district presence

Counts are from `dist/extract/areas.jsonl` (areas whose `faction_counts`
contains `arasaka`; "dominant" means `dominant_faction == arasaka`) and
`data/sites/rosters.json` (`faction_id == 20`). Occupied sites are deduped
`data/sites/sites.json` rows with `default_faction_id == 20` **or** at least one
Arasaka roster entry; no pair is within 25 m. Site attribution follows §3.3.

| Sub-district | District | (a) Lore | (b) Panel | (c) Areas (dominant) | (c) Arasaka entries | Occupied sites |
| --- | --- | --- | --- | ---: | ---: | ---: |
| CorpoPlaza | CityCenter | HQ, memorial, port | — (corp) | 54 (52) | 630 | 1 |
| JapanTown | Westbrook | Dashi Parade + 2023 flashback | Tyger Claws | 19 (18) | 97 | 0 |
| Arroyo | SantoDomingo | Industrial Park | 6th Street | 14 (13) | 84 | 0 |
| LittleChina | Watson | **Konpeki misattribution** | Tyger Claws | 14 (13)* | 59* | 1 |
| WestWindEstate | Pacifica | border set pieces | Voodoo Boys, Animals | 7 (5) | 61 | 2 |
| NorthOaks | Westbrook | Estate, Columbarium | Tyger Claws | 6 (4) | 27 | 0 |
| Badlands | Badlands | scav ambush | Aldecaldos, Wraiths | 5 (2) | 16 | 1 |
| CharterHill | Westbrook | substation; Kiroshi/Yaiba event | Tyger Claws, 6th Street | 4 (4) | 79 | 1 |
| Northside | Watson | All Foods scanner hustle | Maelstrom | 3 (3) | 10 | 1 |
| MorroRock | MorroRock | spaceport passengers | — | 4 (2) | 20 | 0 |
| Glen | Heywood | Hanako guard scene | Valentinos | 3 (2) | 8 | 0 |
| Coastview | Pacifica | incidental | Voodoo Boys, Animals | 3 (1) | 3 | 0 |
| Downtown | CityCenter | incidental | — (corp) | 2 (1) | 4 | 0 |
| Dogtown | Dogtown | KGB hologram set piece | Barghest | 2 (1) | 2 | 1 |
| RanchoCoronado | SantoDomingo | incidental | 6th Street | 2 (1) | 10 | 0 |
| VistaDelRey | Heywood | incidental | Valentinos | 2 (2) | 37 | 0 |
| ArasakaWaterfront | Watson | Konpeki, port | — (corp) | **2 (2)*** | **6*** | 0 |

\* **The raw counts understate ArasakaWaterfront and overstate LittleChina.**
The 14 q005 "Arasaka hotel" areas (≈50 Arasaka entries) sit at `(-2227, 1737)`,
i.e. Konpeki Plaza in ArasakaWaterfront, but the §3.3 nearest-site fallback
attributes them to LittleChina because `awf` is missing from the METHOD
sub-district token map. Reassign q005 to ArasakaWaterfront and the Waterfront
becomes ≈16 areas / ≈56 entries, while LittleChina drops to incidental. This is
a METHOD defect, not a game-data defect; see §8.1.

### 2.3 Attribution caveat

`areas.jsonl.district_code` is not safe to aggregate for Arasaka. Four distinct
failure modes were observed:

1. **`awf` is absent from METHOD §3.3.** Konpeki's q005 communities resolve to
   LittleChina by nearest-site. Any Waterfront count taken from the raw file is
   wrong.
2. **`q108` is a 2023 flashback, not a facility.** `q108_com_atlantis_memory*`
   (66 Arasaka entries) is the Johnny Silverhand Atlantis scene. It inflates
   JapanTown; it is not an Arasaka holding.
3. **`q112` spans two places.** `q112_infiltration_*` is the Arroyo Industrial
   Park; `q112_parade_*` is the Japantown Dashi Parade. The prefix alone cannot
   attribute them.
4. **`q306` is the Morro Rock spaceport, not an Arasaka site.** It contributes
   20 "corpo passengers" entries at the Orbital Air gate.

`sts_ep1_08` is the reverse case: its area path token says `dogtown`, but the
site record is `sub_territory_id = 70` (WestWind South Highway) and the nearest
sub-territory centroid is WestWindEstate (274 m) rather than Dogtown (339 m).
This doc attributes it to WestWindEstate and flags it as a KGB hologram set
piece, not a facility.

---

## 3. Location catalog

Coordinates are world-space metres, `Z` up. "Interior?" means the game has a
distinct interior cell or room volume. "Business?" is what the place earns or
provides, not a vendor inventory (the extract has no vendor data).

| # | Name | Type | District / sub-district | Interior? | Business? (what it earns) | Coordinates (x, y, z) | Coordinate source record | Linked communities / sites | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **Arasaka Tower** | Corporate HQ / skyscraper | CityCenter / CorpoPlaza | Yes — lobby, atrium, jungle, CEO floor, rooftop, basement manufacturing, netrunner nest, Mikoshi | Corporate security contracts, banking, manufacturing, R&D, arms, cyberware; Arasaka Academy inside | `-1443.505, 158.475, 15.351` (lobby); rooftop `-1428.349, 188.423, 616.705`; CEO `-1441.450, 207.100, 564.350` | `dist/extract/markers.jsonl` `q115_12b_sm_tower_lobby`, `q101_mk_arasaka_rooftop`, `q113_12_sm_ceo_floor` | `q115_com_solo_nest_combat` (48), `q000_corpo_com_arasaka_office_bg` (39), `q115_com_solo_lobby_wave_` (35), `q113_com_top_atrium_combat` (31); CC `cc_cpz_arasaka_plaza` | `[game-data]` `[wiki]` |
| 2 | **Konpeki Plaza** | Luxury hotel | Watson / ArasakaWaterfront | Yes — lobby, booked rooms, penthouse, AV pad, garage | Hotel rooms, lobby bar, elite hospitality; Arasaka staff housing | `-2228.021, 1768.814, 20.090` (lobby); room `-2205.080, 1774.864, 163.016`; AV pad `-2212.965, 1763.951, 321.224` | `markers.jsonl` `q005_mrk_lobby_elevator_front`, `mirror_sm_scene_konpeki_room`, `q005_mrk_saburo_av_open_int` | `q005_com_arasaka_hotel_combat_floor_` (18), `q005_com_arasaka_hotel_reinf` (7), `q005_com_arasaka_hotel_garage` (5); CC `cc_awf_konpeki_approach` | `[game-data]` `[wiki]` |
| 3 | **Arasaka Industrial Park** | Warehouse / logistics / manufacturing | SantoDomingo / Arroyo | Yes — main warehouse and infiltration interior | Weapons, vehicles, uniforms, AV retrofit, supply depot | park anchor `-513.200, -1552.900, 6.600`; warehouse `-264.818, -1427.495, 10.300`; infiltration `-258.918, -1484.295, 7.800` | `data/sub_territories.json` `arr_arasaka_industrial`; `markers.jsonl` `q112_06_sm_warehouse`, `q112_05_sm_infiltration` | `q112_infiltration_exterior_reinforcements` (14), `std_arr_com_arasaka_compund` (14), `q112_infiltration_interior_guards` (13); CC `cc_arr_arasaka_industrial` | `[game-data]` `[wiki]` |
| 4 | **Arasaka Estate** | Family villa / compound | Westbrook / NorthOaks | Yes — villa interior, AV pads, garden, pool, netrunner den | Prestige residence and security; no direct revenue | `287.779, 1017.908, 230.300` (interior); compound `294.844, 1030.274, 230.608`; gate `320.800, 1054.300, 225.900` | `markers.jsonl` `q113_04_sm_hanako_estate`, `q113_mp_estate`; `data/landmarks.json` `lm_nok_arasaka_estate` | `q113_com_estate_guards` (14); CC `cc_nok_arasaka_estate` | `[game-data]` `[wiki]` |
| 5 | **Waterfront Freight Terminal** | Logistics terminal | Watson / ArasakaWaterfront | No verified interior cell | Freight handling, automated warehousing, shipments | `-2075.200, 2303.600, 18.300` | `data/sub_territories.json` `awf_central_terminal`; CC `cc_awf_central_terminal` | CC is `is_active=1` (the only active Arasaka CC) | `[game-data]` `[inferred]` |
| 6 | **Arasaka Memorial** | Memorial / tourism | CityCenter / CorpoPlaza | Yes — preserved lobby exhibit and glass walkway | Image control and tourism; no direct revenue | `-1317.810, -84.292, 0.000` | `markers.jsonl` `mq061_03_sm_arasaka_memorial_scene` | CC `cc_cpz_militech_hq` (31 m, Militech-owned) | `[game-data]` `[wiki]` |
| 7 | **North Oak Columbarium** | Columbarium / cemetery | Westbrook / NorthOaks | Partly — walled columbarium structures | Arasaka security contract (turrets); the site is government-owned | `203.839, 575.686, 120.949` | `markers.jsonl` `mq010_03_sm_columbarium` | CC `cc_nok_columbarium` (48 m) | `[game-data]` `[wiki]` |
| 8 | **Arasaka Port** | Port / checkpoint | CityCenter / CorpoPlaza | No — docks and checkpoint | Cargo handling and checkpoint; the cargo ship *Akuma* moors here | `TBD` | `areas.jsonl` `mq060_communityArea_docks` (`-1156.100, 339.200, 4.500`, 8 Arasaka entries) is a community centroid, not a marker; no site/marker found | Corpo Plaza Docks, supervised by Night City Port Authority | `[wiki]` `[game-data]` (area only); coordinate `TBD` |
| 9 | **Charter Hill Substation** | Utility substation / power plant | Westbrook / CharterHill | No — fenced yard, no doors, `is_interior=0` | Power/utility; Arasaka security presence | `570.098, -459.562, 6.800` | `data/sites/sites.json` site 254 `ma_wbr_hil_06` | 3 guard areas, 3 patrol splines, 2 security devices, 7-entry community; CC `cc_hil_power_plant` | `[game-data]` |
| 10 | **Arasaka North Cargo Pier** | Cargo pier | Watson / ArasakaWaterfront | No verified interior cell | Freight and cargo | `-2274.600, 2761.600, 6.800` | `data/sub_territories.json` `awf_north_pier`; CC `cc_awf_north_pier` | Seeded compound; no marker | `[game-data]` `[inferred]` |
| 11 | **Waterfront South Quay** | Quay | Watson / ArasakaWaterfront | No verified interior cell | Freight and cargo | `-2158.700, 1993.100, 18.200` | `data/sub_territories.json` `awf_south_quay`; CC `cc_awf_south_quay` | Seeded compound; no marker | `[game-data]` `[inferred]` |
| 12 | **Arasaka Orbital Station** | Space station / clinic / R&D | Low Earth orbit / — | Yes (lore) | Medical research, rehabilitation, Mikoshi engram stations | `TBD` | No ground coordinate; wiki only | Not reachable on the Night City map | `[wiki]` (not counted in §7) |

### 3.1 Interior sub-locations (the reason to capture a building)

The extractor keeps no `sites.json` rows for Arasaka Tower, Konpeki Plaza or the
Industrial Park warehouse. Their interiors are provable from quest-community
names and named markers instead:

**Arasaka Tower** `[game-data]`

| Sub-location | Coordinates (x, y, z) | Marker / area | Note |
| --- | --- | --- | --- |
| Public lobby | `-1443.505, 158.475, 15.351` | `q115_12b_sm_tower_lobby` | Security gates, elevators, lobby crowd |
| Atrium (bottom) | `-1447.390, 77.206, 243.346` | `q115_mp_atrium_bottom` | Mid-tower atrium and security |
| Top atrium | `-1442.100, 187.700, 388.350` | `q113_11_sm_top_atrium` | Upper atrium combat volume |
| Arasaka jungle | `-1485.750, 157.500, 324.220` | `q113_09_sm_jungle_start` | Interior garden/executive level |
| Mikoshi access | `-1365.478, 121.800, 417.346` | `q113_07_sm_mikoshi` | Engram server chamber |
| Saburo's office | `-1359.664, 123.544, 549.378` | `q113_06_sm_saburo_office` | Executive office |
| CEO floor | `-1441.450, 207.100, 564.350` | `q113_12_sm_ceo_floor` | Yorinobu's floor, turrets and doors |
| Rooftop / AV pads | `-1428.349, 188.423, 616.705` | `q101_mk_arasaka_rooftop` | Saburo's AV landing, rooftop battle |
| Underground manufacturing | `-1481.698, 81.271, -23.812` | `q114_11_sm_arasaka_manufacturing_infiltration` | Manufacturing floor below the tower |
| Netrunner nest | `-1448.117, 147.110, -27.652` | `q114_mp_netrunners_nest` | Server/netrunner room |

**Konpeki Plaza** `[game-data]`

| Sub-location | Coordinates (x, y, z) | Marker / area | Note |
| --- | --- | --- | --- |
| Lobby / reception | `-2228.021, 1768.814, 20.090` | `q005_mrk_lobby_elevator_front` | Elevators, reception, lobby bar |
| Booked room | `-2199.400, 1776.300, 164.400` | `q005_mrk_booked_room` | Guest room floor |
| Yorinobu's room | `-2205.080, 1774.864, 163.016` | `mirror_sm_scene_konpeki_room` | The room used in The Heist |
| Penthouse entrance | `-2228.300, 1769.300, 308.000` | `q005_mrk_penthouse_entrance` | Penthouse level |
| AV landing pad | `-2212.965, 1763.951, 321.224` | `q005_mrk_saburo_av_open_int` | Saburo's AV |
| Garage | `-2248.325, 1726.026, 7.110` | `q005_mrk_garage_mappin` | Vehicle level |

**Arasaka Industrial Park** `[game-data]`

| Sub-location | Coordinates (x, y, z) | Marker / area | Note |
| --- | --- | --- | --- |
| Main warehouse | `-264.818, -1427.495, 10.300` | `q112_06_sm_warehouse` | Supply depot, parade floats |
| Infiltration route | `-258.918, -1484.295, 7.800` | `q112_05_sm_infiltration` | Guarded interior route |
| Recon rooftop | `-290.694, -1574.997, 43.400` | `q112_03_sm_reconnaissance` | Overwatch point |
| Park compound | `-513.200, -1552.900, 6.600` | `std_arr_com_arasaka_compund` (area) | Seeded park anchor |

**Arasaka Estate** `[game-data]`

| Sub-location | Coordinates (x, y, z) | Marker / area | Note |
| --- | --- | --- | --- |
| Villa interior | `287.779, 1017.908, 230.300` | `q113_04_sm_hanako_estate` | Kitchen, dining, office, bedrooms |
| Compound | `294.844, 1030.274, 230.608` | `q113_mp_estate` | Garden, pool, AV pads |
| Estate gate | `320.800, 1054.300, 225.900` | `lm_nok_arasaka_estate` | Seeded gate anchor |

### 3.2 How the name→coordinate links were proven

- **Arasaka Tower** — `q115_12b_sm_tower_lobby` is a tower-lobby scene marker at
  the same coordinates as `q000_corpo_com_arasaka_lobby_elevators` and
  `q115_com_solo_lobby_wave_`; `q113_12_sm_ceo_floor`, `q101_mk_arasaka_rooftop`
  and `q114_11_sm_arasaka_manufacturing_infiltration` name the upper and lower
  floors. The wiki infobox gives `owner = Arasaka`, `district = City Center`,
  `sub_district = Corporate Center`, `location = Corporate Plaza`. `[game-data]` `[wiki]`
- **Konpeki Plaza** — `q005_mrk_lobby_elevator_front` and
  `mirror_sm_scene_konpeki_room` are inside the `q005_com_arasaka_hotel_*`
  community cluster; the wiki infobox gives `type = Hotel`, `owner = Arasaka`,
  `sub_district = Arasaka Waterfront`. `[game-data]` `[wiki]`
- **Arasaka Industrial Park** — `q112_06_sm_warehouse` and
  `q112_05_sm_infiltration` are the q112 infiltration scene; the park's seeded
  anchor is `std_arr_com_arasaka_compund`; the wiki infobox gives
  `type = Warehouse`, `owner = Arasaka`, `sub_district = Arroyo`. Note that the
  warehouse marker falls inside the seeded `arr_petrochem_yard` sub-territory
  (see §8.3). `[game-data]` `[wiki]`
- **Arasaka Estate** — `q113_04_sm_hanako_estate` and `q113_mp_estate` are the
  Hanako estate scene; the wiki infobox gives `type = Villa`, `owner = Arasaka`,
  `sub_district = North Oak`. `[game-data]` `[wiki]`
- **Arasaka Memorial** — `mq061_03_sm_arasaka_memorial_scene` is the memorial
  scene marker; the wiki infobox gives `type = Memorial`, `owner = Arasaka`,
  `location = Corporate Plaza`. `[game-data]` `[wiki]`
- **North Oak Columbarium** — `mq010_03_sm_columbarium` is the columbarium
  scene marker; the wiki infobox gives `owner = Government of Night City` and
  says it is guarded by Arasaka security turrets. The seed gives the
  sub-territory to Arasaka; that is an ownership conflict, not a name conflict.
  `[game-data]` `[wiki]`
- **Arasaka Port** — no marker or site. The only Arasaka record is the
  community area `mq060_communityArea_docks` (8 Arasaka entries, dominant) at
  `(-1156.100, 339.200, 4.500)`. The wiki names the place and places it at the
  Corpo Plaza Docks. Coordinate left `TBD` per the §6 coordinate rule.
  `[game-data]` `[wiki]`
- **Charter Hill Substation** — site 254 `ma_wbr_hil_06` has
  `default_faction_id = 20`, `initial_owner_faction_id = 20`,
  `sub_territory_id = 28` (`hil_power_plant`, display name "Charter Hill
  Substation") and `control_center_id = 28`. There is no wiki page and no
  marker; the name is the seed sub-territory name. `[game-data]`
- **Waterfront port zones** — the names come from
  `data/sub_territories.json` display names; each has a CC at the same anchor.
  There is no marker or wiki page for any of the three. Treat the names as
  seed-only. `[game-data]` `[inferred]`

### 3.3 Arasaka-occupied generic sites (the filler pool)

`data/sites/suitabilities.json` tags sites with gameplay affordances. These are
unnamed or non-facility sites; they are useful as filler control points or
business slots, not as lore businesses.

| Site | Sub-district | Interior | Suitability tags | Units | Coordinates | Note |
| --- | --- | --- | --- | ---: | --- | --- |
| `ma_wbr_hil_06` | CharterHill | no | raid_target 93, vehicle_bay 65, camera_net 61, stealth_entry 60 | 6 | `570.098, -459.562, 6.800` | **Named catalog point:** Charter Hill Substation; not filler |
| `sts_ep1_08` | WestWindEstate | no | officer_site 90, rooftop_access 80 | 27 | `-2227.100, -3019.100, 115.300` | KGB hologram set piece; 27 "units" are holograms. Presence, not ownership. Filler only |
| `mws_se5_03` | Badlands | yes | raid_target 75, club 70, stealth_entry 55, safehouse 51 | 15 | `-3464.100, -4005.700, 55.200` | Scav/ambush mini-world-story; `is_interior=1` but not an Arasaka facility. Filler only |
| `ma_wat_nid_20` | Northside | no | raid_target 90, rooftop_access 80 | 6 | `-376.100, 2300.300, 36.300` | Scanner hustle at the All Foods Plant (Maelstrom turf); Arasaka guards. Filler only |
| `ma_cct_cpz_01` | CorpoPlaza | no | raid_target 81, hostage_site 50, branch_office 45 | 5 | `-1657.500, 35.300, 7.500` | Scanner hustle on Memorial Ring West; `default_faction_id=1`, Arasaka units only. Filler only |
| `mws_tactical_coffee` | LittleChina | no | officer_site 90, raid_target 75, rooftop_access 68, vehicle_bay 65 | 4 | `-1500.700, 1150.900, 18.800` | "Tactical Coffee" corporate scene; 4 Arasaka corpos. Filler only |
| `ma_pac_wwd_05` | WestWindEstate | no | rooftop_access 80, raid_target 57 | 3 | `-2567.900, -2432.900, 43.000` | Scanner hustle at the West Wind Coastal Ruins; Arasaka security. Filler only |
| `sts_ep1_06` | Dogtown | no | officer_site 90, rooftop_access 80, elevator 70 | 2 | `-1606.400, -2341.500, 43.100` | Fixer gig "Zembinsky"; Arasaka business contact + ranger. Filler only |

Treat the tags as gameplay affordances, not lore. A `raid_target` tag says the
site can host a raid; it does not prove Arasaka owns a business there.

---

## 4. Economic structure

### 4.1 Revenue streams → catalog locations

| Revenue stream | Code(s) | Catalog locations that produce it | Evidence / notes |
| --- | --- | --- | --- |
| Corporate security contracts | `security_services` | Arasaka Tower (command), North Oak Columbarium (turrets), Arasaka Waterfront (wall/turrets), Arasaka Estate (agents/ACPA), Arasaka Port (checkpoint) | Wiki: largest armed forces of any corporation; licenses guards, couriers and mercenaries. Game-data: guard records at every site. `[wiki]` `[game-data]` |
| Manufacturing | `manufacturing` | Arasaka Industrial Park (warehouses, AV retrofit, uniforms), Arasaka Tower underground manufacturing, Waterfront automated warehouses | Wiki: Industrial Park is one of the largest supply depots and retrofits Zetatech Atlus AVs; Waterfront sorts hundreds of shipments/month. `[wiki]` |
| Arms | `arms` | Arasaka Industrial Park (weapons, vehicles, uniforms), Arasaka Tower manufacturing | Wiki: Arasaka-branded weapons and military vehicles are among the most sought after. `[wiki]` |
| R&D / prototypes | `rnd` | Arasaka Tower netrunner nest and Mikoshi, Arasaka Orbital Station | Wiki: Orbital Station is a medical/research facility with Mikoshi engram stations; Tower has a netrunner nest and Mikoshi access. `[wiki]` `[game-data]` |
| Cyberware | `cyberware` | Arasaka Tower / Industrial Park R&D and manufacturing; no retail storefront | Wiki: Arasaka cyberware (e.g. Sandevistan) is manufactured, not sold from a shop. `[wiki]` `[inferred]` |
| Real estate / hospitality | `real_estate` | Konpeki Plaza, Arasaka Estate | Wiki: Konpeki is a luxury hotel for executives and elite guests; the Estate houses the family when visiting. `[wiki]` |
| Food & drink / retail | `food_drink`, `retail` | Konpeki Plaza lobby bar and hotel services | Wiki: lobby bar is a place to mingle with the powerful; hotel service staff. `[wiki]` |
| Logistics / contraband | `smuggling` | Waterfront Freight Terminal, North Cargo Pier, South Quay, Arasaka Port; the *Akuma* | Wiki: Waterfront is a walled logistics hub and "what really goes on is unknown"; Arasaka Port is a checkpoint on the Corpo Plaza Docks. `[wiki]` `[inferred]` |
| Energy / utilities | `energy` | Charter Hill Substation | Seed-only: the sub-territory and CC are named "Charter Hill Substation"; no wiki page and no Arasaka energy business is documented. `[game-data]` `[inferred]` |
| Media / image control | `media` | Arasaka Memorial | Wiki: the memorial is described as "a carefully curated act of image control" as much as a tribute. `[wiki]` |
| Banking / finance | — (no code) | Arasaka Tower | Wiki infobox lists banking as a core business. §7 has no `finance` code; this income is not representable. `[wiki]` |
| Education | — (no code) | Arasaka Academy (inside Arasaka Tower) | Wiki: the Academy prepares the next generation of Arasaka executives. Not a capture point; a pipeline. `[wiki]` |

### 4.2 Suppliers, customers, rivals

| Role | Party | Detail |
| --- | --- | --- |
| Supplier / partner (vehicles) | Yaiba | Yaiba and Arasaka co-developed the Kusanagi; Yaiba's Muramasa showroom event is at Kiroshi Campus in Charter Hill. `[wiki]` |
| Supplier / partner (optics) | Kiroshi | Kiroshi Campus hosts the Yaiba showcase; Kiroshi is a separate Charter Hill corporation, not an Arasaka subsidiary. `[wiki]` |
| Supplier (AV platforms) | Zetatech | Arasaka's Industrial Park retrofits Zetatech Atlus AVs with military upgrades. `[wiki]` |
| Customer | NCPD, other corporations, wealthy individuals | Arasaka licenses security services; Konpeki's guests are executives, entertainment icons and the elite. `[wiki]` |
| Customer | Arasaka's own divisions | Tower administration, Academy, Orbital Station and field security consume the Industrial Park's output. `[inferred]` |
| Rival | Militech | The primary corporate-security and arms rival. The Arasaka Memorial's nearest CC is `cc_cpz_militech_hq` (31 m). `[wiki]` `[game-data]` |
| Rival | Kang Tao | Japanese competitor in arms and corporate security; the Kang Tao North Tower is also in Corpo Plaza. `[wiki]` |
| Rival | Petrochem | Adjacent to the Industrial Park warehouse; the warehouse marker is 5 m from the Petrochem Freight Yard CC. `[game-data]` |
| Regulator / landlord | Night City Port Authority | Supervises the Corpo Plaza Docks, including Arasaka Port. `[wiki]` |
| Labour / community | Japanese communities in Night City | Arasaka supports Japanese communities despite its business practices; the Academy is the executive pipeline. `[wiki]` |

---

## 5. Headquarters recommendation

### Primary HQ: **Arasaka Tower** — Corpo Plaza

Coordinates: lobby `(-1443.505, 158.475, 15.351)` `[game-data]`
`markers.jsonl q115_12b_sm_tower_lobby`.

Rationale:

1. **Canonical North American HQ.** The wiki gives the tower `type = North
   American Division HQ / Regional HQ`, `owner = Arasaka`, `location =
   Corporate Plaza`; it is the tallest structure in Night City at 620 m and the
   heart of Arasaka's financial and military operations in both Americas.
   `[wiki]`
2. **A real management seat with rooms to assign.** The game gives it a public
   lobby, reception/security gates, an atrium, the Arasaka jungle, Saburo's
   office, the CEO floor, a rooftop AV pad, an underground manufacturing floor,
   a netrunner nest and Mikoshi access. This is the only Arasaka place that can
   plausibly host org management, R&D, security and manufacturing at once.
   `[game-data]`
3. **It maps 1:1 to the economic core.** Security contracts, banking,
   manufacturing, R&D, arms and cyberware all run through the tower. Owning the
   HQ and owning the economy are the same action. `[wiki]` `[inferred]`
4. **Heavy, verified game data.** Corpo Plaza has 54 Arasaka areas (52
   dominant) and 630 Arasaka entries; the tower's own communities include
   48-, 39-, 35-, 33- and 31-entry combat/mood areas. `[game-data]`
5. **No new map plumbing.** `cc_cpz_arasaka_plaza` is 27.9 m from the lobby
   marker and already owned by Arasaka (`initial_owner_faction_id = 20`).
   `[game-data]`

Trade-off: the tower is an endgame quest space with strong verticality. A
capture volume at the lobby is easy to define; capturing the whole tower means
handling the atrium, jungle, CEO floor, rooftop and basement as separate
sub-zones. Use the lobby as the seat and the upper floors as upgrade slots,
not as separate control points.

### Alternate 1: **Konpeki Plaza** — Arasaka Waterfront

Coordinates: lobby `(-2228.021, 1768.814, 20.090)` `[game-data]`
`markers.jsonl q005_mrk_lobby_elevator_front`.

The strongest enclosed non-HQ building: a luxury hotel with a lobby, guest
floors, penthouse, AV pad and garage. It is canonically Arasaka-owned, sits
31.6 m from `cc_awf_konpeki_approach`, and is the Waterfront's only wiki-named
location. It loses only because it is a hotel, not a command seat, and because
the wiki says it was closed indefinitely after The Heist; a post-quest capture
state needs to be defined. `[wiki]` `[game-data]`

### Alternate 2: **Arasaka Estate** — North Oak

Coordinates: interior `(287.779, 1017.908, 230.300)` `[game-data]`
`markers.jsonl q113_04_sm_hanako_estate`.

The family seat: a North Oak villa with AV pads, garden, pool, office, bedrooms
and a netrunner den, guarded by elite agents and an ACPA. It is a better
*prestige* seat than the tower for a family-led org, and it is 49.1 m from
`cc_nok_arasaka_estate`. It loses on geography (peripheral hills, z≈230), on
revenue (residential, no business) and on scale (a villa, not a corporate
headquarters). `[wiki]` `[game-data]`

### Overruled / downgraded suggestions

- **Arasaka Industrial Park as HQ** — it is the logistics and manufacturing
  engine, not a management seat. Keep it as a high-value capture point and a
  source of `manufacturing`/`arms` yield. `[wiki]`
- **Arasaka Memorial as HQ** — a memorial and image-control site; no command
  functions. Its nearest CC is Militech-owned, so it is also a poor first
  capture. `[wiki]` `[game-data]`
- **Charter Hill Substation as HQ** — a fenced utility yard; excellent test
  point, wrong seat. `[game-data]`
- **Arasaka Orbital Station as HQ** — canonically owned and a research/clinic
  facility, but it has no Night City ground coordinate and is off-map. `[wiki]`
- **North Oak Villa Ridge / Charter Hill Terraces as HQ or business** — both
  are seeded to Arasaka but conflict with lore: the ridge area contains Denny's
  mansion and Kerry Eurodyne's villa nearby, and the terraces anchor hosts the
  `mq060` Kiroshi/Yaiba showcase, whose wiki-named campus is Kiroshi-owned. Do
  not seed either as an Arasaka seat. `[wiki]` `[game-data]` `[inferred]`

---

## 6. Priority list of control points

Ranked by how well each place serves as a capturable Arasaka control point.
"CC" = nearest entry in `data/control_centers.json`; distance is horizontal
metres. Relevance reflects lore + revenue + record richness, not raw unit count.

| Rank | Control point | Rel. (1–5) | District / sub-district | Coordinates | Existing CC overlap | Why |
| ---: | --- | :---: | --- | --- | --- | --- |
| 1 | **Arasaka Tower** | 5 | CityCenter / CorpoPlaza | `-1443.505, 158.475, 15.351` | `cc_cpz_arasaka_plaza`, 27.9 m (Arasaka) | Canon HQ; lobby/atrium/CEO/rooftop/basement; security, manufacturing, R&D, banking; 630 Arasaka entries in Corpo Plaza |
| 2 | **Konpeki Plaza** | 5 | Watson / ArasakaWaterfront | `-2228.021, 1768.814, 20.090` | `cc_awf_konpeki_approach`, 31.6 m (Arasaka) | Iconic Arasaka hotel; enclosed 3-level interior; elite clientele; the Waterfront's only wiki-named place |
| 3 | **Arasaka Industrial Park** | 5 | SantoDomingo / Arroyo | `-513.200, -1552.900, 6.600` | `cc_arr_arasaka_industrial`, 0.0 m (Arasaka) | Largest supply depot; weapons, vehicles, uniforms, AV retrofit; q112 infiltration interior |
| 4 | **Arasaka Estate** | 4 | Westbrook / NorthOaks | `287.779, 1017.908, 230.300` | `cc_nok_arasaka_estate`, 49.1 m (Arasaka) | Family seat; elite guards and ACPA; AV pads, garden, pool, netrunner den; prestige |
| 5 | **Waterfront Freight Terminal** | 4 | Watson / ArasakaWaterfront | `-2075.200, 2303.600, 18.300` | `cc_awf_central_terminal`, 0.0 m (Arasaka, active) | The only active Arasaka CC; logistics hub; seed-named, no marker/wiki |
| 6 | **Arasaka Memorial** | 3 | CityCenter / CorpoPlaza | `-1317.810, -84.292, 0.000` | `cc_cpz_militech_hq`, 31.1 m (**Militech**) | Canon memorial and image-control site; preserved lobby exhibit; CC ownership conflict is a feature to fix |
| 7 | **North Oak Columbarium** | 3 | Westbrook / NorthOaks | `203.839, 575.686, 120.949` | `cc_nok_columbarium`, 48.0 m (Arasaka) | Arasaka-guarded public cemetery; `security_services`; government-owned per wiki |
| 8 | **Arasaka Port** | 3 | CityCenter / CorpoPlaza | `TBD` | Unknown; no marker | Canon port/checkpoint on the Corpo Plaza Docks; the *Akuma*; coordinate pending |
| 9 | **Charter Hill Substation** | 3 | Westbrook / CharterHill | `570.098, -459.562, 6.800` | `cc_hil_power_plant`, 5.1 m (Arasaka) | **Test control point.** Clean `default_faction_id=20`; 6 Arasaka units; 3 guard areas, 3 patrols, 2 security devices; fenced yard |
| 10 | **Arasaka North Cargo Pier** | 2 | Watson / ArasakaWaterfront | `-2274.600, 2761.600, 6.800` | `cc_awf_north_pier`, 0.0 m (Arasaka) | Waterfront logistics; seed-named, no marker/wiki |
| 11 | **Waterfront South Quay** | 2 | Watson / ArasakaWaterfront | `-2158.700, 1993.100, 18.200` | `cc_awf_south_quay`, 0.0 m (Arasaka) | Waterfront logistics; seed-named, no marker/wiki |

### Test control point for the first in-game test: **Charter Hill Substation**

Site 254 `ma_wbr_hil_06`, coordinates `(570.098, -459.562, 6.800)`,
`[game-data]` `data/sites/sites.json`.

Why this and not the HQ or Konpeki:

- **The cleanest Arasaka-default facility site.** It has
  `default_faction_id = 20`, `initial_owner_faction_id = 20` and
  `control_center_id = 28`; eviction has no ambiguity. The other
  `default_faction_id = 20` sites (`sts_ep1_08`, `mws_se5_03`,
  `ma_wat_nid_20`, `ma_pac_wwd_05`) are a hologram set piece, a scav ambush and
  two scanner hustles, not facilities. `[game-data]`
- **Complete capture-relevant records.** 3 guard areas
  (`#ma_wbr_hill_06_ga`, `_2`, `_3`), 3 patrol splines, 2 security devices
  (`sec_area`, `sec_sys`), 14 workspots, a 7-entry community, and 6 Arasaka
  units including an agent, ninja, sniper, two rangers and a security guard.
  Every hook a capture/defence prototype needs is present. `[game-data]`
- **No new map plumbing.** `cc_hil_power_plant` is 5.1 m away and already
  Arasaka-owned. `[game-data]`
- **Not the HQ.** The first test exercises capture on a non-seat, as METHOD §3.8
  recommends. `[game-data]`

Trade-off: it is a **fenced yard, not an enclosed interior** (`is_interior=0`,
`has_doors=0`). It tests the capture volume and trigger on an outdoor site
first, which is the cheapest failure mode. Follow-up test: **Konpeki Plaza
lobby** (`q005_mrk_lobby_elevator_front`, 31.6 m from
`cc_awf_konpeki_approach`) once the CC is retargeted, to validate a multi-floor
interior. Fallback if the substation is too small or quest-gated: the
Industrial Park warehouse (`q112_06_sm_warehouse`), but note its nearest CC is
Petrochem-owned. `[game-data]`

---

## 7. Per-sub-district counts

This is the number to feed yield balancing. It counts **distinct named places**
Arasaka owns, runs, protects or habitually occupies — not quest-scene variants
and not generic occupied blocks. `Filler` is the deduped occupied-site count
minus any site already counted as a named place (METHOD §8).

| Sub-district | Named lore-relevant places | Which ones | Arasaka-occupied sites (deduped) | Filler | Noteworthy interiors |
| --- | ---: | --- | ---: | ---: | --- |
| CorpoPlaza | **3** | Arasaka Tower, Arasaka Memorial, Arasaka Port | 1 | 1 (`ma_cct_cpz_01`) | Tower lobby/atrium/CEO/rooftop/basement; Memorial exhibit |
| ArasakaWaterfront | **4** | Konpeki Plaza, Waterfront Freight Terminal, Arasaka North Cargo Pier, Waterfront South Quay | 0 | 0 | Konpeki (3 levels); port interiors unverified |
| Arroyo | **1** | Arasaka Industrial Park | 0 | 0 | Main warehouse; infiltration route |
| NorthOaks | **2** | Arasaka Estate, North Oak Columbarium | 0 | 0 | Estate villa; columbarium structures |
| CharterHill | **1** | Charter Hill Substation | 1 | 0 | None (fenced yard) |
| WestWindEstate | **0** | KGB hologram / coastal-ruin scanner hustles only | 2 | 2 (`sts_ep1_08`, `ma_pac_wwd_05`) | None Arasaka-owned |
| Northside | **0** | All Foods scanner hustle only | 1 | 1 (`ma_wat_nid_20`) | None |
| LittleChina | **0** | Tactical Coffee corporate scene only | 1 | 1 (`mws_tactical_coffee`) | None |
| Dogtown | **0** | Zembinsky fixer-gig contact only | 1 | 1 (`sts_ep1_06`) | None |
| Badlands | **0** | Scav ambush set piece only | 1 | 1 (`mws_se5_03`) | None Arasaka-owned |
| **Total** | **11** | | 8 | 7 | |

Reconciliation: 8 deduped occupied sites − 1 site-backed named place (Charter
Hill Substation) = 7 filler. 11 named = 1 site-backed + 10 marker/anchor-only
(Tower, Konpeki, Industrial Park, Estate, Memorial, Columbarium, Arasaka Port,
Freight Terminal, North Cargo Pier, South Quay). `named + filler = 18`, which
is the 8 sites plus the 10 marker/anchor-only named places. `[game-data]`

Caveat on "named": 4 of the 11 are **seed-named only** — Charter Hill
Substation and the three Waterfront port zones — with no wiki page or marker to
confirm the name. They are distinct, Arasaka-seeded places, so they count, but
they should not receive iconic-business yield multipliers until the names are
verified in-game. The 7 wiki/marker-verified named places are the Tower,
Konpeki, Industrial Park, Estate, Memorial, Columbarium and Arasaka Port.
`[game-data]` `[wiki]` `[inferred]`

Interpretation for yield: CorpoPlaza and ArasakaWaterfront are the two
commercial multi-named sub-districts and should carry the high-yield modifiers.
NorthOaks has two named places but both are prestige/security rather than
commerce. Arroyo has one huge manufacturing point. CharterHill has one utility
point and one seed conflict. WestWindEstate, Northside, LittleChina, Dogtown and
Badlands are presence-only: no named Arasaka business, so they should be filler
or contested turf, not owned economy. `[inferred]`

---

## 8. Gaps and uncertainties

1. **`awf` is missing from METHOD §3.3.** The `SD` map and the `_SITE`/`_TOKEN`
   regexes omit `ArasakaWaterfront`. Konpeki's 14 q005 areas (≈50 Arasaka
   entries) therefore attribute to LittleChina by nearest-site, and
   ArasakaWaterfront shows only 2 areas. Add `awf` to the token map; consider
   `mrr`/`morro` for MorroRock too. This is the single biggest attribution error
   for this faction.
2. **Corp HQs are not `sites.json` rows.** Arasaka Tower, Konpeki Plaza, the
   Industrial Park warehouse, the Estate and the Memorial are quest
   communities/markers only. METHOD §3.1's "candidate sites" query returns none
   of them. §5.3's trial found the markers, but §3/§5 do not state the general
   rule: for a corp, the building may be marker/area-only, and `is_interior`
   cannot be read from a site row.
3. **`nearest_cc` is not ownership proof.** The Arasaka Memorial's nearest CC is
   `cc_cpz_militech_hq` (31 m, Militech); the Industrial Park warehouse's
   nearest CC is `cc_arr_petrochem_yard` (5 m, Petrochem). If a seeder retargets
   by nearest CC, it can hand an Arasaka point to a rival. Check the CC's
   `sub_territory_id` owner before retargeting.
4. **The Industrial Park warehouse sits in the Petrochem sub-territory.** The
   seeded `arr_arasaka_industrial` anchor is `(-513.2, -1552.9)`, but the q112
   warehouse/infiltration markers are at `(-264.8, -1427.5)`, inside seeded
   `arr_petrochem_yard` (owner 43). The park is large and the boundary is
   ambiguous; verify before seeding the park polygon. `[game-data]`
5. **No `logistics`/`freight` revenue code.** The Waterfront and Industrial Park
   are primarily logistics; the closest §7 code is `smuggling`, which mislabels
   legitimate freight as contraband. Add `logistics` (or allow a `logistics`
   tag) before seeding the port economy.
6. **No `finance`/`banking` or `education` code.** Arasaka's infobox lists
   banking, and Arasaka Academy is a named institution inside the Tower. §7
   cannot represent either. Either add `finance` and `education`, or state that
   they are out of scope for control-point yield.
7. **No `hospitality` code.** Konpeki Plaza is a hotel; `real_estate` +
   `food_drink` + `retail` is a three-code workaround. Add `hospitality`.
8. **Seed display names are not lore-verified.** METHOD §3.0 says to verify
   seed names, but for the three Waterfront port zones and Charter Hill
   Substation there is no wiki page or marker to verify against. This doc marks
   them `[game-data]`/`[inferred]` and counts them as named with a caveat. The
   playbook should say explicitly what to do when a seed name cannot be
   verified.
9. **The two-tier count is ambiguous for seed-only anchors.** The port zones are
   not `sites.json` rows, so they cannot be `filler` under §8's site-based
   definition; they are also not wiki-named. §8 should define a third category
   ("seed-only holding") or say whether a seed-named anchor counts as `named`.
   This doc counts them as `named` and flags them.
10. **`is_interior` is useless for corp buildings.** The Tower, Konpeki and the
    Industrial Park have no site row, so the flag is absent. §10's `interior`
    field needs a marker/area rule: `*_lobby`, `*_room`, `*_atrium`, `*_floor`,
    `*_jungle`, `*_penthouse`, or an area named `*_com_*` proves an interior
    cell. This doc uses those markers.
11. **`q`/`mq` quest prefixes are ambiguous.** `q112` covers both the Japantown
    Dashi Parade and the Arroyo infiltration; `q108` is a 2023 flashback, not a
    facility; `q306` is the Morro Rock spaceport; `mq060` is the Kiroshi/Yaiba
    showcase. Aggregating by prefix overstates sub-districts. Split by
    coordinates and area name.
12. **Corp presence is not ownership.** `sts_ep1_08` (27 KGB holograms),
    `mws_se5_03` (15 scav ambush enemies), `mws_tactical_coffee` (4 Arasaka
    corpos at a coffee shop) and the `mq060` Kiroshi/Yaiba cluster (75 Arasaka
    entries; `mq060_communityarea_yaiba` alone has 56) are set pieces or
    events. METHOD §2.3.2 covers
    this for gangs; add the corp equivalents, including `mws_tactical_coffee`
    and `mq060`.
13. **Seed vs. wiki ownership conflicts.** The North Oak Columbarium is
    government-owned per wiki but seeded to Arasaka; Charter Hill Terraces is
    Kiroshi Campus per wiki but seeded to Arasaka; North Oak Villa Ridge
    contains Kerry Eurodyne's villa and Denny's mansion. The playbook says to
    report conflicts but not what to do. Recommendation: keep a seeded point
    only if the corp has a security/ownership stake; otherwise mark it
    "protected/adjacent", not owned.
14. **The Arasaka Estate wiki page is suspect.** Its infobox says
    `owner = Arasaka`, `type = Villa`, `sub_district = North Oak`, but the page
    carries a Russian interwiki link to Kerry Eurodyne's villa, suggesting page
    conflation. The game markers (`q113_04_sm_hanako_estate`,
    `q113_mp_estate`) and the seed both place the Arasaka Estate on the North
    Oak ridge, so the coordinate is solid; the wiki page text is the weak part.
15. **The first test cannot satisfy every §3.8 criterion.** No Arasaka-default
    *facility* site is an enclosed interior with doors. `ma_wbr_hil_06` is the
    cleanest site (default faction, guards, patrols, devices, 5 m from a CC) but
    is a fenced yard. The playbook should say what to do when no corp site meets
    the "enclosed interior" preference: use the cleanest fenced site for test
    #1, then an enclosed quest interior (Konpeki) for test #2.
16. **Arasaka Port has no coordinate.** The only local record is the
    `mq060_communityArea_docks` community centroid at `(-1156.100, 339.200,
    4.500)`; §6's coordinate rule allows site anchor or marker, not an area
    centroid. The doc leaves it `TBD`. If area centroids are acceptable for
    large open sites, say so in §6; otherwise keep `TBD`.
17. **The `data/faction_headquarters.json` seed has no Arasaka row.** Only
    Tyger Claws/Clouds is present. This doc supplies the Arasaka row from
    markers; a seeder that reads only `faction_headquarters.json` will find
    nothing for Arasaka.

---

## 9. Sources

Local:

- `dist/extract/markers.jsonl` — all named coordinates (Tower, Konpeki,
  Industrial Park, Estate, Memorial, Columbarium, interior sub-locations).
- `dist/extract/areas.jsonl` — presence density and Arasaka-dominant areas.
- `data/sites/sites.json`, `data/sites/rosters.json` — 8 occupied sites / 68
  units; site 254 records.
- `data/sites/{guards,triggers,spots,patrols,doors,devices,communities,suitabilities}.json`
  — interior identification and test-point richness.
- `data/{factions,districts,sub_territories,landmarks,control_centers}.json` —
  faction id 20, district/sub-district spelling, 12 owned sub-territories,
  CC anchors and owners.

Wiki:

- [Arasaka](https://cyberpunk.fandom.com/wiki/Arasaka)
- [Arasaka Tower](https://cyberpunk.fandom.com/wiki/Arasaka_Tower)
- [Konpeki Plaza](https://cyberpunk.fandom.com/wiki/Konpeki_Plaza)
- [Arasaka Industrial Park](https://cyberpunk.fandom.com/wiki/Arasaka_Industrial_Park)
- [Arasaka Estate](https://cyberpunk.fandom.com/wiki/Arasaka_Estate)
- [Arasaka Waterfront](https://cyberpunk.fandom.com/wiki/Arasaka_Waterfront)
- [Arasaka Memorial](https://cyberpunk.fandom.com/wiki/Arasaka_Memorial)
- [North Oak Columbarium](https://cyberpunk.fandom.com/wiki/North_Oak_Columbarium)
- [Arasaka Port](https://cyberpunk.fandom.com/wiki/Arasaka_Port)
- [Known Arasaka Facilities](https://cyberpunk.fandom.com/wiki/Known_Arasaka_Facilities)
- [Arasaka Orbital Station](https://cyberpunk.fandom.com/wiki/Arasaka_Orbital_Station)
- [Arasaka Academy](https://cyberpunk.fandom.com/wiki/Arasaka_Academy)
- [Yaiba](https://cyberpunk.fandom.com/wiki/Yaiba)
- [Kiroshi Campus](https://cyberpunk.fandom.com/wiki/Kiroshi_Campus)
- [Charter Hill (2077)](https://cyberpunk.fandom.com/wiki/Charter_Hill_(2077))
- [Arasaka Towers](https://cyberpunk.fandom.com/wiki/Arasaka_Towers)

Earlier repo research:

- [`docs/research/factions/METHOD.md`](./METHOD.md)
- [`docs/research/factions/tyger-claws.md`](./tyger-claws.md)

---

## 10. Machine-readable block

Strict JSON for seeding (contract in [`METHOD.md`](./METHOD.md) §10). Every
coordinate was verified against the local record named in `source` on
2026-11-25; none came from the wiki. `null` means `TBD`, never `0`.

```json
{
  "faction_code": "arasaka",
  "hq": {
    "name": "Arasaka Tower",
    "district": "CityCenter",
    "sub_district": "CorpoPlaza",
    "x": -1443.505,
    "y": 158.475,
    "z": 15.351,
    "source": "dist/extract/markers.jsonl q115_12b_sm_tower_lobby",
    "confidence": "game-data+wiki"
  },
  "alternate_hqs": [
    {
      "name": "Konpeki Plaza",
      "district": "Watson",
      "sub_district": "ArasakaWaterfront",
      "x": -2228.021,
      "y": 1768.814,
      "z": 20.09,
      "source": "dist/extract/markers.jsonl q005_mrk_lobby_elevator_front",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Arasaka Estate",
      "district": "Westbrook",
      "sub_district": "NorthOaks",
      "x": 287.779,
      "y": 1017.908,
      "z": 230.3,
      "source": "dist/extract/markers.jsonl q113_04_sm_hanako_estate",
      "confidence": "game-data+wiki"
    }
  ],
  "test_control_point": {
    "name": "Charter Hill Substation",
    "district": "Westbrook",
    "sub_district": "CharterHill",
    "x": 570.098,
    "y": -459.562,
    "z": 6.8,
    "source": "data/sites/sites.json site 254 ma_wbr_hil_06",
    "confidence": "game-data"
  },
  "control_points": [
    {
      "rank": 1,
      "name": "Arasaka Tower",
      "type": "corporate_hq",
      "relevance": 5,
      "district": "CityCenter",
      "sub_district": "CorpoPlaza",
      "x": -1443.505,
      "y": 158.475,
      "z": 15.351,
      "source": "dist/extract/markers.jsonl q115_12b_sm_tower_lobby",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["security_services", "manufacturing", "rnd", "arms", "cyberware"],
      "nearest_cc_code": "cc_cpz_arasaka_plaza",
      "nearest_cc_m": 27.9
    },
    {
      "rank": 2,
      "name": "Konpeki Plaza",
      "type": "hotel",
      "relevance": 5,
      "district": "Watson",
      "sub_district": "ArasakaWaterfront",
      "x": -2228.021,
      "y": 1768.814,
      "z": 20.09,
      "source": "dist/extract/markers.jsonl q005_mrk_lobby_elevator_front",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["real_estate", "food_drink", "retail"],
      "nearest_cc_code": "cc_awf_konpeki_approach",
      "nearest_cc_m": 31.6
    },
    {
      "rank": 3,
      "name": "Arasaka Industrial Park",
      "type": "industrial_park",
      "relevance": 5,
      "district": "SantoDomingo",
      "sub_district": "Arroyo",
      "x": -513.2,
      "y": -1552.9,
      "z": 6.6,
      "source": "data/sub_territories.json arr_arasaka_industrial",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["manufacturing", "arms", "rnd"],
      "nearest_cc_code": "cc_arr_arasaka_industrial",
      "nearest_cc_m": 0.0
    },
    {
      "rank": 4,
      "name": "Arasaka Estate",
      "type": "villa",
      "relevance": 4,
      "district": "Westbrook",
      "sub_district": "NorthOaks",
      "x": 287.779,
      "y": 1017.908,
      "z": 230.3,
      "source": "dist/extract/markers.jsonl q113_04_sm_hanako_estate",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["real_estate", "security_services"],
      "nearest_cc_code": "cc_nok_arasaka_estate",
      "nearest_cc_m": 49.1
    },
    {
      "rank": 5,
      "name": "Waterfront Freight Terminal",
      "type": "logistics_terminal",
      "relevance": 4,
      "district": "Watson",
      "sub_district": "ArasakaWaterfront",
      "x": -2075.2,
      "y": 2303.6,
      "z": 18.3,
      "source": "data/sub_territories.json awf_central_terminal",
      "confidence": "game-data+inferred",
      "interior": false,
      "revenue_streams": ["smuggling", "manufacturing"],
      "nearest_cc_code": "cc_awf_central_terminal",
      "nearest_cc_m": 0.0
    },
    {
      "rank": 6,
      "name": "Arasaka Memorial",
      "type": "memorial",
      "relevance": 3,
      "district": "CityCenter",
      "sub_district": "CorpoPlaza",
      "x": -1317.81,
      "y": -84.292,
      "z": 0.0,
      "source": "dist/extract/markers.jsonl mq061_03_sm_arasaka_memorial_scene",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["media"],
      "nearest_cc_code": "cc_cpz_militech_hq",
      "nearest_cc_m": 31.1
    },
    {
      "rank": 7,
      "name": "North Oak Columbarium",
      "type": "columbarium",
      "relevance": 3,
      "district": "Westbrook",
      "sub_district": "NorthOaks",
      "x": 203.839,
      "y": 575.686,
      "z": 120.949,
      "source": "dist/extract/markers.jsonl mq010_03_sm_columbarium",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["security_services"],
      "nearest_cc_code": "cc_nok_columbarium",
      "nearest_cc_m": 48.0
    },
    {
      "rank": 8,
      "name": "Arasaka Port",
      "type": "port",
      "relevance": 3,
      "district": "CityCenter",
      "sub_district": "CorpoPlaza",
      "x": null,
      "y": null,
      "z": null,
      "source": "dist/extract/areas.jsonl mq060_communityArea_docks (community centroid; coordinate TBD)",
      "confidence": "game-data+wiki",
      "interior": false,
      "revenue_streams": ["smuggling"],
      "nearest_cc_code": null,
      "nearest_cc_m": null
    },
    {
      "rank": 9,
      "name": "Charter Hill Substation",
      "type": "utility_substation",
      "relevance": 3,
      "district": "Westbrook",
      "sub_district": "CharterHill",
      "x": 570.098,
      "y": -459.562,
      "z": 6.8,
      "source": "data/sites/sites.json site 254 ma_wbr_hil_06",
      "confidence": "game-data",
      "interior": false,
      "revenue_streams": ["energy", "security_services"],
      "nearest_cc_code": "cc_hil_power_plant",
      "nearest_cc_m": 5.1
    },
    {
      "rank": 10,
      "name": "Arasaka North Cargo Pier",
      "type": "cargo_pier",
      "relevance": 2,
      "district": "Watson",
      "sub_district": "ArasakaWaterfront",
      "x": -2274.6,
      "y": 2761.6,
      "z": 6.8,
      "source": "data/sub_territories.json awf_north_pier",
      "confidence": "game-data+inferred",
      "interior": false,
      "revenue_streams": ["smuggling"],
      "nearest_cc_code": "cc_awf_north_pier",
      "nearest_cc_m": 0.0
    },
    {
      "rank": 11,
      "name": "Waterfront South Quay",
      "type": "quay",
      "relevance": 2,
      "district": "Watson",
      "sub_district": "ArasakaWaterfront",
      "x": -2158.7,
      "y": 1993.1,
      "z": 18.2,
      "source": "data/sub_territories.json awf_south_quay",
      "confidence": "game-data+inferred",
      "interior": false,
      "revenue_streams": ["smuggling"],
      "nearest_cc_code": "cc_awf_south_quay",
      "nearest_cc_m": 0.0
    }
  ],
  "subdistrict_counts": {
    "CorpoPlaza": {"named": 3, "filler": 1},
    "ArasakaWaterfront": {"named": 4, "filler": 0},
    "Arroyo": {"named": 1, "filler": 0},
    "NorthOaks": {"named": 2, "filler": 0},
    "CharterHill": {"named": 1, "filler": 0},
    "WestWindEstate": {"named": 0, "filler": 2},
    "Northside": {"named": 0, "filler": 1},
    "LittleChina": {"named": 0, "filler": 1},
    "Dogtown": {"named": 0, "filler": 1},
    "Badlands": {"named": 0, "filler": 1}
  }
}
```
