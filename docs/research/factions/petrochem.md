# Petrochem — Lore-Relevant Control Points

Status: faction research run, 2026-11-25. One faction, one document.
Scope: replace the generic control-centre grid with places Petrochem actually
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
site, seed or enum record, or marked `TBD`.

**Up front, because it shapes every section:** Petrochem is the emptiest
faction of the sixteen studied. The 2.5 extract contains **zero** roster
entries, **zero** community areas, **zero** spawn points, **zero** faction-owned
sites, and **no `gamedataAffiliation` value at all**. There is no Petrochem
guard, drone, office NPC or world story anywhere in the game. The faction's
entire Night City existence has to be reconstructed from three things: a
handful of *place* markers, prefab folders and district enums (`[game-data]`),
a small number of wiki infoboxes (`[wiki]`), and one seeded sub-territory that
turns out to sit on Arasaka's property. This doc is therefore marker-, prefab-
and enum-driven, as predicted.

---

## 1. Summary

Petrochemical Associates International ("Petrochem") is a petrochemical and
agribusiness megacorporation headquartered in the Dallas–Fort Worth Metroplex
(Irving, Texas). It is the world's largest producer of **CHOOH2**, the synthetic
grain-alcohol fuel that replaced gasoline — "60% of world supplies" — under
licence from Biotechnica, and it is one of the two largest remaining oil
producers next to SovOil. `[wiki]`

Its Night City presence in 2077 is four places, of which only two have a
verified in-game coordinate:

- **Badlands — North Sunrise Oil Fields.** The in-game **Oil Fields** north of
  Night City (Johnny Silverhand's grave, *Chippin' In*). Canonically owned by
  **Petrochem, SovOil and Night Corp** jointly. A dedicated district sub-area
  exists: `gamedataDistrict.Badlands_NorthSunriseOilField = 18`. `[wiki]`
  `[game-data]`
- **Badlands — Petrochem Fuel Station (Interstate 9).** A CHOOH2 station and
  workshop beside the Sunset Motel on the eastern Badlands, with Petrochem as
  the infobox owner; the only 2077 Petrochem *business* with an in-game
  footprint. `[wiki]` `[game-data]`
- **Arroyo — Petrochem Nuclear Power Plant.** A fenced, guarded power-plant
  compound on Republic Way, explicitly a 2077 Petrochem location. **No local
  record of any kind**; coordinate `TBD`. `[wiki]`
- **Corpo Plaza — Petrochem Tower.** The 2077 regional HQ, next to the Kang Tao
  Building, reached by a bridge from Memorial Park. **No local record of any
  kind**; coordinate `TBD`. `[wiki]`

Everything else that carries the Petrochem name in 2077 is a leftover, not a
holding: the **EBM Petrochem Stadium** in Dogtown (Petrochem was a construction
sponsor in the 2060s; Barghest holds it in 2077), and the **`q104` "petrochem
operator"** community, whose NPCs are actually Kang Tao. `[wiki]` `[game-data]`

Game-data scale: **0 roster sites / 0 units**, **0 areas**, **0 spawn points**,
**0 sites with `default_faction_id = 43`**, **1 owned sub-territory** (seed-only,
and misplaced — §8.1). `gamedataAffiliation` has 44 values and `Petrochem` is
not one of them (`refs/cyberpunk/orphans.swift`); `data/factions.json` records
`affiliation_enum: null` for this faction, which is the same fact seen from the
other side. `[game-data]`

For scale: Biotechnica has 2 roster sites / 25 units and 5 areas; Kang Tao 4 / 24
and 17. Petrochem has **none**. That is the finding, not a research failure.

---

## 2. Territory

### 2.1 Districts

| Evidence kind | Result |
| --- | --- |
| (a) Wiki/lore | Global HQ Dallas–Fort Worth, Texas. Night City **regional HQ** is Petrochem Tower, Corporate Plaza, City Center. Assets: the Northern Oil Fields (with SovOil and Night Corp), a fuel station on Interstate 9, a nuclear power plant in Arroyo. Regional offices exist in every major city; Night City's is one of them. `[wiki]` |
| (b) Vanilla map gang panel | **Structurally empty.** `data/districts.json` `vanilla_gangs` lists street gangs only; megacorps never appear. Evidence (b) is inapplicable by design, not missing. `[game-data]` |
| (c) Game-data counts | 0 areas contain Petrochem. 0 roster sites. 0 sites whose `default_faction_id` or `initial_owner_faction_id` is 43. 0 spawn points. 1 owned sub-territory. No `gamedataAffiliation.Petrochem`. `gamedataDistrict.Badlands_NorthSunriseOilField = 18` exists. `[game-data]` |

The one owned sub-territory (`data/sub_territories.json`,
`initial_owner_faction_id = 43`, `owner_kind = corp`):

| Code | Display name | Sub-district | Anchor (x, y, z) | CC | CC active |
| --- | --- | --- | --- | --- | --- |
| `arr_petrochem_yard` | Petrochem Freight Yard | Arroyo | `-255.9, -1480.0, 7.6` | `cc_arr_petrochem_yard` | **yes** |

`[game-data]` — the name and the anchor are ours, not lore; see §8.1.

### 2.2 Sub-district presence

There is almost nothing to tabulate. Counts are from `dist/extract/areas.jsonl`
(areas whose `faction_counts` contains `petrochem`), `data/sites/rosters.json`
(`faction_id == 43`) and `data/sites/sites.json`. All three are empty.

| Sub-district | District | (a) Lore | (b) Panel | (c) Areas (dominant) | (c) Petrochem entries | Occupied sites |
| --- | --- | --- | --- | ---: | ---: | ---: |
| Badlands | Badlands | Oil Fields; I-9 fuel station | — | 0 (0) | 0 | 0 |
| Arroyo | SantoDomingo | Nuclear power plant | 6th Street | 0 (0) | 0 | 0 |
| CorpoPlaza | CityCenter | Petrochem Tower (regional HQ) | — (corp) | 0 (0) | 0 | 0 |

`[game-data]`

**Reading the zeroes.** These are not a missing join. I checked the faction id
(43), the code (`petrochem`), the corp token in `character_record_id`, the
`areas.jsonl` `faction_counts` map and the raw sector prefabs; there is no
Petrochem actor anywhere. The only `areas.jsonl` rows whose *names* contain
"petrochem" are `{q104_com_petrochem_operators}` and `{q104_com_petro_gas_station}`
(both `kang_tao`, §3.4). The `gamedataAffiliation` enum is 44 values long and
has no Petrochem entry.

### 2.3 Attribution caveat

Normally this section corrects sub-district mis-attribution. Here it records
four attribution hazards instead:

1. **The oil-fields prefab is filed under Watson/Northside.** The placement
   prefab is `#c_watson/northside/loc_sq031_oilfield_barracks…`, but its marker
   sits at `y = 3855.3`, which is **330 m north of the Watson bbox** (`y ≤ 3525`)
   and inside the `Badlands` bbox. The wiki puts the fields in the northern
   Badlands and the game has a dedicated `Badlands_NorthSunriseOilField` enum.
   METHOD §1.2 item 1's "placement prefab first" rule is the *wrong* first
   signal here: it would file the faction's best asset in Northside. Use
   position + enum + wiki, and say so.
2. **The seed's Arroyo holding is on Arasaka ground.** `arr_petrochem_yard`
   (`-255.9, -1480.0`) is 5.2 m from `q112_05_sm_infiltration`, a marker inside
   `#c_santo_domingo/arroyo/loc_q112_arasaka_industrial_park_warehouse…`, and
   267 m from the `arr_arasaka_industrial` centroid. All nine sites inside the
   sub-territory carry `initial_owner_faction_id = 20` (Arasaka), not 43.
   The seed relabelled a grid cell; it did not move an asset. §8.1.
3. **`{q104_com_petrochem_operators}` is not Petrochem.** The community at
   `(-661.5, -4985.2, 69.0)` is `kang_tao`, 7 entries, at the *Life During
   Wartime* AV crash site. "Petrochem operators" is a staging label inherited
   from the spaceport/oil story, not a faction. A seeder that greps the areas
   file for "petrochem" will hand Petrochem a Kang Tao quest scene in the
   southern Badlands. `[game-data]`
4. **The oil fields are joint-owned.** The wiki infobox lists `owner =
   Petrochem, SovOil, Night Corp`. Any claim on this place is a claim on a
   shared asset, and the seed currently gives the sub-territory to **Militech**
   (faction 21). Report it; do not quietly reassign without a decision. `[wiki]`
   `[game-data]`

---

## 3. Location catalog

Coordinates are world-space metres, `Z` up. "Interior?" means the game has a
distinct interior cell or room volume. "Business?" is what the place earns or
provides — the extract has no vendor inventory.

| # | Name | Type | District / sub-district | Interior? | Business? (what it earns) | Coordinates (x, y, z) | Coordinate source record | Linked communities / sites | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **North Sunrise Oil Fields** (Northern Oil Fields; the in-game "Oil Fields") | Active and abandoned oil field; barracks, derricks, oil pools | Badlands / Badlands | No — open landscape; the barracks and pumps are separate static meshes | Crude oil extraction, CHOOH2 feedstock, freight out; jointly held with SovOil and Night Corp | `-1835.695, 3719.295, 6.742` (fast-travel dataterm, also the seeded sub-territory/CC anchor); pumps and barracks `-1845.399, 3855.277, 7.442` | `dist/extract/markers.jsonl {bls_bls_dataterm_}05`; `data/sub_territories.json bls_north_oil_fields`; marker `{sq031_mp_oil_fields}` | CC `cc_bls_north_oil_fields` (0.0 m, **Militech**, inactive); prefab `loc_sq031_oilfield_barracks`; no `sites.json` row | `[game-data]` `[wiki]` |
| 2 | **Petrochem Fuel Station (Interstate 9)** | CHOOH2 fuel station + vehicle workshop | Badlands / Badlands | **Yes** — workshop/garage interior (`#loc_q103_tr_interior_roadhouse_garage`) | Fuel retail (`energy`, `retail`); the wiki adds a small Hundred Under Haven store in the 2045 layout | `1706.187, -755.859, 49.801` (workshop marker; the motel room is 56 m west-south-west at `1662.681, -791.510, 49.820`) | `dist/extract/markers.jsonl {q104_mp_sunset_garage}`; motel marker `{q103_mp_motel_room}` | Prefab `se1/loc_q103_roadhouse` (Sunset Motel complex); no `sites.json` row; nearest site `sts_bls_ina_03` 268.7 m | `[game-data]` `[wiki]` `[inferred]` |
| 3 | **Petrochem Nuclear Power Plant** | Nuclear power plant; fenced compound, checkpoint, three main buildings | SantoDomingo / Arroyo | Believed yes (three buildings, guard post) — **not provable** from the extract | Power generation; regional `energy` supply | `TBD` | No marker, site, community or prefab. Wiki: `owner = Petrochem`, `type = Nuclear power plant`, `district = Santo Domingo`, `sub_district = Arroyo`, `street = Republic Way`; neighbours NC Prison (NW), Megabuilding H6 (S), Electric Corporation Power Plant (NE) | None found; NC Prison has a record (`#c_santo_domingo/arroyo/loc_mq062`), the plant does not | `[wiki]` only |
| 4 | **Petrochem Tower** | Regional HQ / office skyscraper | CityCenter / CorpoPlaza | **Yes** (`[wiki]`: a hidden NCART location was built inside it in patch 2.1) — no local record | Regional administration, wholesale CHOOH2 distribution, energy trading | `TBD` | No marker, site, community or prefab. Wiki: `owner = Petrochem`, `type = Regional HQ`, `sub_district = Corporate Center`, `location = Corporate Plaza`; next to the Kang Tao Building; bridge from Memorial Park | None found; the wiki puts it next to the Kang Tao Building (site 20, `ma_cct_cpz_16`) | `[wiki]` only |

### 3.1 Interior sub-locations

Only one catalog point has a provable interior, and it is a garage:

**Petrochem Fuel Station (Interstate 9)** `[game-data]`

| Sub-location | Coordinates (x, y, z) | Node / marker | Note |
| --- | --- | --- | --- |
| Workshop / garage | `1706.187, -755.859, 49.801` | marker `{q104_mp_sunset_garage}` | Panam's workshop in *Ghost Town*; the wiki's "fuel station and workshop east of the parking lot" |
| Garage interior trigger | `TBD` | `#loc_q103_tr_interior_roadhouse_garage` | `triggers.json` has no position for it |
| Garage radio (device) | `TBD` | `#q104_dvc_panam_garage_radio` | Device node, no extracted position |
| Sunset Motel room | `1662.681, -791.510, 49.820` | marker `{q103_mp_motel_room}` | 56 m west-south-west; the motel is owned by Noah, not Petrochem |

The station's *forecourt* has no node of its own; the only modelled interior is
the workshop. If the capture volume must avoid a quest interior, anchor on the
forecourt coordinates above rather than the garage trigger.

The oil fields have no interior: the pumps, derricks, barracks and oil pools are
landscape and static meshes. The barracks prefab
(`loc_sq031_oilfield_barracks`) contains only quest markers
(`#sq031_mp_oil_fields_area`, `#sq031_05_sm_grave`,
`#sq031_spn_composting_plant`, `holofixer_sm_scene`) — no doors, guard areas or
patrols. `[game-data]`

The nuclear plant and the Tower are described by the wiki as buildings with
rooms, but the extract contains neither, so their interiors cannot be tagged
`[game-data]`.

### 3.2 How the name→coordinate links were proven

- **North Sunrise Oil Fields** — three independent confirmations. (1) The
  in-game marker `{sq031_mp_oil_fields}` and `{sq031_05_sm_grave}` sit together
  at `(-1845, 3855)`: this is the *Chippin' In* / Johnny's-grave part of the
  northern oil fields, matching the wiki's "Oil Fields" database entry.
  *Chippin' In*'s own infobox (`baseid = sq031_rogue`) lists
  `sub_districts = Little China, Northside, Northern Oil Fields` — an independent
  wiki confirmation that the `sq031_*` markers in the north are the Northern Oil
  Fields.
  (2) `gamedataDistrict.Badlands_NorthSunriseOilField = 18`
  (`refs/cyberpunk/orphans.swift` line 4845) is a first-class district sub-area
  named after the field. (3) The seeded sub-territory `bls_north_oil_fields`
  "North Sunrise Oil Fields" has its centroid at `(-1835.695, 3719.295)`, which
  is **0.005 m** from the game's fast-travel dataterm `{bls_bls_dataterm_}05`
  — the seed generator took the anchor from the dataterm, so the anchor is a
  genuine map point, not an arbitrary centroid. `[game-data]` `[wiki]`
- **Petrochem Fuel Station (I-9)** — the wiki links it from the Sunset Motel
  page ("a neighboring [[Petrochem Fuel Station (Interstate 9)|fuel station]]
  and workshop east of the parking lot"), and its own infobox gives
  `owner = Petrochem`, `region = Badlands`, `subregion = Red Peaks`,
  `street = Interstate 9`, `appears_games = RED, 2077`. The only modelled
  workshop east of the Sunset Motel parking lot is the roadhouse garage, whose
  marker is `{q104_mp_sunset_garage}` inside `se1/loc_q103_roadhouse`. The
  station-building link is therefore `[inferred]`; the coordinate is
  `[game-data]`. `[game-data]` `[wiki]` `[inferred]`
- **Petrochem Nuclear Power Plant** — no local record. The 2.5 extract has no
  `nuclear` prefab (the single "nuclear" token in all three sectors is
  `q101_vfx_nuclear_mushroom`, a VFX), no marker, no site, no community and no
  device. The nearest recordable neighbour is Night City Prison (`mq062`,
  prefab `#c_santo_domingo/arroyo/loc_mq062`, markers `mq062_01…mq062_18` at
  roughly `(-517, -600)`), which the wiki puts *northwest* of the plant. That
  constrains the plant to the prison's south-east but supplies no coordinate.
  `TBD` per METHOD §6. `[wiki]` `[game-data]`
- **Petrochem Tower** — no local record. No Corpo Plaza prefab, mappin or site
  carries the name; the only Corpo Plaza corporate sites are Arasaka Tower,
  the Militech and Kang Tao scanner sites and the generic ring-road hustles.
  The wiki's note that patch 2.1 hid an NCART location *inside* the tower is a
  hint (`ue_metro_station_09_city_center_arrival` is at `-1473.390, 462.536,
  5.828`), but it is an `[inferred]` hint, not a tower anchor. `TBD`.
  `[wiki]` `[game-data]` `[inferred]`

### 3.3 Petrochem-occupied generic sites (the filler pool)

**Empty.** There is no site in `data/sites/sites.json` with
`default_faction_id = 43`, `initial_owner_faction_id = 43`, or a single roster
entry for faction 43. Filler = 0. `[game-data]`

### 3.4 What looks like Petrochem and is not (energy-site disambiguation)

This is the most useful table for a seeder, because Petrochem's business is the
one thing Night City is full of.

| Place | Who it really is | Evidence | Petrochem? |
| --- | --- | --- | --- |
| **EBM Petrochem Stadium** (Dogtown; Nighthawks Stadium) | **Barghest** in 2077; stadium built 2060s with HFS, Zhirafa, **Petrochem** (sponsor/participant), Corp-Bud, Aurochs | Wiki infobox `affiliation = BARGHEST`, `owner` blank; `{q301_com_stadium}` at `(-1413,-2012,72)`, metro `{ue_metro_station_19_pacifica_stadium_arrival}` `(-1539.833,-1940.146,62.589)`; nearest CC `cc_cvi_east_overpass` 347 m, **Animals** | **No** — name and sponsorship only, not a holding |
| SovOil Fuel Station (Highway 101) | **SovOil**; manager Marty Jenklow | `{q104_07_sm_gas_station_chats}` `(-1815.3,-4282.5,74.2)`; nearest CC `cc_bls_biotechnica_flats` (Biotechnica, active) | No |
| Rocky Ridge Fuel Station | **Corp-Bud** (formerly); built for the Pol-Bud company town of Pol-Bud Miasto; **Wraiths** in 2077 | Wiki infobox; `bls_rocky_ridge` sub, Wraith-owned | No |
| Laguna Bend Fuel Station | Independent, flooded in 2062 | Wiki infobox, owner blank | No |
| Medeski Fuel Station | Unnamed manager; **Wraiths** extort it | Wiki infobox; Municipal Landfill, east Badlands | No |
| Northside Oil Wharf / `nid_oil_refinery` | **Scavengers** (fid 7); seed name | `ma_wat_nid_27` `(-1111.2,3318.5)` 7 Scavengers, `#ma_gang_watch_ga` | No — the Petrochem/SovOil refineries are RED-era (2040s), not this site |
| Satwave Power Plant | City power infrastructure; attacked by V and Panam to EMP Kang Tao | `{q104_pplant_cooling_terminal_marker}` `(-195.3,-2838.3,22.8)`; 4 Kang Tao drones | No |
| Wind Farms | **Government of Night City** | Wiki infobox | No |
| Coronado Dam | **Government of Night City**, nonoperational | Wiki infobox | No |
| Arroyo `sts_std_arr_12` gas station | Zetatech guards a diner/motel/gas-station fixer gig inside 6th Street-owned turf | Site 385, `default_faction_id = 24` (**Zetatech**), `initial_owner_faction_id = 4` (6th Street), `#arr_12_diner`, `loc_sts_std_arr_12_gas_station` | No proven brand |
| Badlands `ina_*` service stations | Inland Avenue roadside stops with no brand data; the fuel-dispenser sites are Militech, Wraith and Aldecaldo property depending on the stretch | `sts_bls_ina_05` (Militech, `#ina_05_dvc_fuel_tank`), `sts_bls_ina_08` (Wraiths, `#ina_08_dvc_fuel_dispener`), `sts_bls_ina_09` (Aldecaldos, `#ina_09_dvc_fuel_disp`) | No proven brand |
| `{q104_com_petrochem_operators}` | **Kang Tao**, 7 entries, AV crash site | `areas.jsonl`, `(-661.5,-4985.2,69.0)`, `dominant_faction = kang_tao` | **No** — staging label |
| `bls_com_test_se1_gas_station` | A test-asset marker, not a place | `markers.jsonl` `(1453.5,-1368.5,51.4)` | No |

`[game-data]` `[wiki]`

**"Sunrise" is a field name, not an operator.** The oil fields are the
"North Sunrise Oil Fields" (aka Northern Oil Fields); no company called Sunrise
has a page, a record or a prefab. The operators named in the wiki infobox are
Petrochem, SovOil and Night Corp. `[wiki]`

**Pipelines do not exist as assets.** The word `pipeline` appears once in the
whole extract (`vehicle_pipeline_test`, a vehicle rig). There is no pipeline,
derrick, pumpjack or refinery prefab with a Petrochem identity. The lore's
"thousands of miles of pipeline" is not modelled. `[game-data]` `[wiki]`

---

## 4. Economic structure

### 4.1 Revenue streams → catalog locations

Petrochem's economy is **fuel and power**, and almost none of it is a building
in Night City. This is the central modelling problem for the faction, and it is
worse than Kang Tao's (which at least has an HQ tower volume).

| Revenue stream | Code(s) | Catalog locations that produce it | Evidence / notes |
| --- | --- | --- | --- |
| Crude oil extraction | `energy` | North Sunrise Oil Fields (1) | Wiki: "Petrochem has more fertile oilfields than any other company"; the 2070s fields are blackened, with active drills and abandoned barracks. Jointly held with SovOil and Night Corp. `[wiki]` `[game-data]` |
| CHOOH2 production and wholesale | `energy` | Oil Fields (1); Petrochem Tower (4); Petrochem Fuel Station (3) | Wiki/netpage: "Wholesale CHOOH2 Distribution… direct access to CHOOH2, natural gas and oil"; "satisfies 60% of the world's energy needs"; "supply power to the NUSA and the Free States". Production is licensed from Biotechnica. `[wiki]` |
| Power generation | `energy` | Petrochem Nuclear Power Plant (3) | Wiki infobox `type = Nuclear power plant`, `owner = Petrochem`; a TV crew outside the gates asks the manager about poisoning the neighbourhood. `[wiki]` |
| Fuel retail | `retail`, `energy` | Petrochem Fuel Station (I-9) (2) | Wiki: CHOOH2 station + workshop beside the Sunset Motel, with a small Hundred Under Haven store (2045 layout). `[wiki]` |
| Distribution / freight | `logistics` | Oil Fields (1) → refinery/terminal (off-map); Tower (4) as the wholesale desk; I-9 station (2) as a highway node | Wiki describes sea-front refineries and oil terminals connected by roadways and pipes; none of that plant exists in the 2077 game world. `[wiki]` `[inferred]` |
| Petrochemicals, plastics, fertiliser, food, weapons | `manufacturing`, `agriculture`, `arms` | **None in Night City** | The company's product lines are real (plastics plant in Heywood, weapons, XOMA pharma, Good Earth Foods) but every one is either 2020/RED-era or outside the map. No factory, lab or farm of Petrochem's exists in the 2077 extract. Model in prose only (§1.2 item 10). `[wiki]` |

**Why `smuggling` is not used.** METHOD §5.4 hypothesises `energy`,
`manufacturing`, `smuggling` for this corp. `manufacturing` has no place (above).
`smuggling` has no evidence either: the Badlands fuel stations are held by
Wraiths and Scavengers, which is *someone else's* black market, not Petrochem's.
Do not credit it. `[game-data]` `[inferred]`

**Do not credit the Biotechnica Flats.** The greenhouses outside the city are
Biotechnica's protein farms. Petrochem's wheat farms are in Brazil, Colombia and
(latterly) Kazakhstan — off-map. `[wiki]`

### 4.2 Suppliers, customers, rivals

| Role | Party | Detail |
| --- | --- | --- |
| Licensor / affiliate | **Biotechnica** | Owns the CHOOH2 patents and the *T. vulgaris megasuavis* wheat; licenses production to Petrochem and SovOil. The org infobox lists `affiliations = Biotechnica`. `[wiki]` |
| Co-owner (oil fields) | **SovOil** | Joint owner of the Northern Oil Fields; historic rival of Petrochem, including a leased-field dispute that SovOil won in 2021. `[wiki]` |
| Co-owner / broker | **Night Corp** | Joint owner; brokered the Petrochem–SovOil peace after the Fourth Corporate War. `[wiki]` |
| Landlord (seed) | **Militech** | The seed currently assigns `bls_north_oil_fields` to faction 21. Not lore; a seed conflict (§8.4). `[game-data]` |
| Customer | NUSA, Free States, industry | "We supply power to the NUSA and the Free States"; wholesale CHOOH2, natural gas and oil. `[wiki]` |
| Customer | Night City drivers | CHOOH2 is the standard vehicle fuel; retail at roadside stations. `[wiki]` |
| Occupier (I-9 station turf) | **Wraiths** | The Sunset Motel sub-territory (`bls_sunset_motel`) is Wraith-owned and its CC is the station's nearest CC (74 m, active); the station sits in gang country. `[game-data]` `[wiki]` |
| Occupier (Northside refinery) | **Scavengers** | The Northside Oil Wharf (`nid_oil_refinery`) is a Scavenger stash. `[game-data]` |
| Rival | **SovOil** | The other oil major and the other major CHOOH2 licensee; the two shared the fields under an uneasy Night Corp-brokered peace. `[wiki]` |
| Rival (fuel retail) | Corp-Bud, independents | Competing Badlands stations at Rocky Ridge and Laguna Bend; not Petrochem. `[wiki]` |
| Regulator | Night City government | Owns the wind farms and Coronado Dam; the Arroyo plant is a live safety controversy. `[wiki]` |
| Sponsor (sport) | **EBM Petrochem Stadium** / Night City Nighthawks | Petrochem sponsored the stadium in the 2060s; the arena was never opened and is now Barghest's. `[wiki]` |

---

## 5. Headquarters recommendation

### Primary HQ: **North Sunrise Oil Fields** — Badlands

Coordinates: `(-1835.695, 3719.295, 6.742)` `[game-data]`
`dist/extract/markers.jsonl {bls_bls_dataterm_}05` (= `data/sub_territories.json
bls_north_oil_fields` = `cc_bls_north_oil_fields`, to 0.005 m).

Rationale:

1. **The canon Petrochem production asset with a verified coordinate.**
   It is the landscape the faction was built on; the game's own "Oil Fields"
   database entry, the `Chippin' In` grave site and the dedicated
   `Badlands_NorthSunriseOilField` district enum all point at the same place.
   `[game-data]` `[wiki]`
2. **It is already a seeded sub-territory and control centre with the right
   name.** `bls_north_oil_fields` "North Sunrise Oil Fields" exists, with
   `cc_bls_north_oil_fields` at the same anchor. The mod needs no new map row,
   only an owner change from Militech to Petrochem (§8.4). This is the same
   shape as Biotechnica's Flats pick. `[game-data]`
3. **The anchor is a real map point, not a centroid artefact.** It is the
   fast-travel dataterm `{bls_bls_dataterm_}05`, so a player can actually stand
   on it; a capture volume there is playable. `[game-data]`
4. **It has room for an economy.** An oil field is an acreage asset: derricks,
   barracks, pumping stations, tank farm. Unlike a tower it can host capture
   sub-zones without fighting a quest interior, and the existing CC gives the
   simulation a 45 m capture radius to grow from. `[game-data]` `[inferred]`
5. **Nothing else in the faction is both canon and seedable.** The Tower and the
   Arroyo plant are the true seats and both have no coordinate; the fuel station
   is a retail point, not a seat. `[wiki]` `[game-data]`

**Trade-off:** this is a **joint-owned Badlands landscape, not a building.** The
wiki gives three owners (Petrochem, SovOil, Night Corp), the seed gives it to
Militech, and there is no garrison, no interior and no door. The field marker
`{sq031_mp_oil_fields}` is 1.2 m from `{sq031_05_sm_grave}` — Johnny
Silverhand's grave, a quest-critical scene — so the capture volume must sit on
the dataterm/CC anchor 136 m south, never on the marker. If the mod requires a
fenced, guarded seat, the honest answer is that Petrochem cannot supply one from
verified data (§8.6).

### Alternate 1: **Petrochem Nuclear Power Plant** — Arroyo

Coordinates: `TBD` (no marker, site, community or prefab).

This is the **best seat-shaped asset** the faction owns in 2077: a fenced
compound with a security checkpoint on Republic Way, three main buildings, a
parking area and a live TV safety controversy. It is also in **Arroyo** — the
district where the seed currently (wrongly) puts the Petrochem Freight Yard.
If a human places its coordinate from the in-game map, this should become the
primary HQ and the seed's Arroyo holding should move here. `[wiki]`

### Alternate 2: **Petrochem Tower** — Corpo Plaza

Coordinates: `TBD` (no marker, site, community or prefab).

The canonical 2077 **regional HQ**, next to the Kang Tao Building and reached by
a bridge from Memorial Park. It would be the obvious primary HQ if it had a
coordinate; 2.5 does not model it. The patch-2.1 note that an NCART location was
built inside it puts `ue_metro_station_09_city_center_arrival`
(`-1473.390, 462.536, 5.828`) in the neighbourhood, but that is a station
entrance, not a tower anchor. `[wiki]` `[game-data]` `[inferred]`

### Overruled / downgraded suggestions

- **"Petrochem Freight Yard" (`arr_petrochem_yard`) as an HQ or a holding** —
  there is no freight yard. The anchor is 5.2 m from an Arasaka Industrial Park
  warehouse marker (`q112_05_sm_infiltration`), 267 m from the Arasaka
  sub-territory centroid, and every site in the sub-territory is Arasaka-owned
  by `initial_owner_faction_id`. The name comes from
  `tools/generate-world-seeds.py` line 167. Retire it, or move the ownership to
  the Arroyo nuclear plant. `[game-data]`
- **EBM Petrochem Stadium as a Petrochem point** — the name is a 2060s
  sponsorship; in 2077 it is a Barghest-held ruin and black market. Counting it
  would invert the history. Not `named`, not seeded. `[wiki]` `[game-data]`
- **Northside Oil Wharf (`nid_oil_refinery`) as the Petrochem refinery** — the
  visible 2077 site is a Scavenger stash. The wiki's Petrochem Oil Refinery and
  SovOil Oil Refinery are RED-era (2040s) facilities with no 2077 record.
  `[game-data]` `[wiki]`
- **SovOil Fuel Station (Highway 101) as a Petrochem station** — SovOil-owned,
  with its own manager; Kang Tao merely falls back to it. `[wiki]`
- **`{q104_com_petrochem_operators}` as a Petrochem area** — Kang Tao, 7
  entries. `[game-data]`
- **Satwave Power Plant / Wind Farms / Coronado Dam as Petrochem energy** —
  all city or NCPD infrastructure, not Petrochem. `[wiki]`

---

## 6. Priority list of control points

Ranked by how well each place serves as a capturable Petrochem control point.
"CC" = nearest entry in `data/control_centers.json` (all CCs, active or not);
distance is horizontal metres; the owner column is the CC's sub-territory owner
per METHOD §1.1 item 10.

| Rank | Control point | Rel. (1–5) | District / sub-district | Coordinates | Existing CC overlap | Why |
| ---: | --- | :---: | --- | --- | --- | --- |
| 1 | **North Sunrise Oil Fields** | 5 | Badlands / Badlands | `-1835.695, 3719.295, 6.742` | `cc_bls_north_oil_fields`, **0.0 m** (**Militech**, inactive) | HQ. Canon oil asset, dedicated district enum, existing seeded sub-territory and CC, real dataterm anchor; no garrison |
| 2 | **Petrochem Fuel Station (Interstate 9)** | 4 | Badlands / Badlands | `1706.187, -755.859, 49.801` | `cc_bls_sunset_motel`, 74.0 m (**Wraiths**, active) | **Test control point.** The only canon Petrochem *business* with an in-game anchor; small, bounded, workshop interior; sits in Wraith turf |
| 3 | **Petrochem Nuclear Power Plant** | 4 | SantoDomingo / Arroyo | `TBD` | Unknown; no marker | Canon 2077 Petrochem industrial seat, fenced compound with checkpoint; needs a hand-placed coordinate |
| 4 | **Petrochem Tower** | 4 | CityCenter / CorpoPlaza | `TBD` | Unknown; no marker | Canon regional HQ; no local record at all; a station-inside-tower hint only |

### Test control point for the first in-game test: **Petrochem Fuel Station (Interstate 9)**

Marker `{q104_mp_sunset_garage}`, coordinates
`(1706.187, -755.859, 49.801)` `[game-data]` `dist/extract/markers.jsonl`.

Why this and not the HQ or the Tower:

- **It is the cleanest non-HQ Petrochem place that can be seeded today.** The
  HQ is the oil fields; the Tower and the Arroyo plant have no coordinate. The
  station is a single, small, bounded retail site with a canonical owner in its
  wiki infobox and a `[game-data]` position. `[game-data]` `[wiki]`
- **It exercises a real business, not a landscape.** A fuel station is the one
  place where the faction's actual product (CHOOH2) is sold, so the economy hook
  (`energy` + `retail`) is tested, not just a radius on dirt. `[wiki]`
- **It has a small interior.** The roadhouse garage
  (`#loc_q103_tr_interior_roadhouse_garage`) gives the test one enclosed room
  without a multi-floor vertical volume, which is the right first step. Rare for
  this faction — it otherwise has no interior at all. `[game-data]`
- **It is not the HQ**, so the first test exercises capture on a non-seat, as
  METHOD §3.8 requires. `[game-data]`

Trade-offs, stated plainly:

- **There is no `sites.json` row and no roster.** `default_faction_id` does not
  exist for this point, so "clean ownership" cannot be proven from the site
  table; the capture volume must be placed by hand around the marker. This is
  the §1.2 item 12 case ("no interior/site at all"): the richest outdoor retail
  site is the test point, and the doc says so.
- **The anchor is a quest workshop.** `{q104_mp_sunset_garage}` is Panam's
  garage in *Ghost Town*. Place the capture volume on the station forecourt
  (same marker, outside the garage trigger), or accept that the first test runs
  inside a quest building.
- **The station is on Wraith turf.** Its nearest CC
  (`cc_bls_sunset_motel`, 74 m, active) is Wraith-owned, so this test exercises
  capturing a Petrochem business from a **gang**, not from the corp. That is
  arguably a better test than the HQ, but it is a different scenario and should
  be labelled as such.
- **Fallback if the quest volume is unacceptable:** the Oil Fields barracks
  marker `{sq031_mp_oil_fields}` (`-1845.399, 3855.277, 7.442`), 136 m north of
  the HQ anchor. It is outdoor-only, has no site row either, and is 1.2 m from
  Johnny's grave — so it is a worse first test, not a better one.

---

## 7. Per-sub-district counts

This is the number to feed yield balancing. It counts **distinct named places**
Petrochem owns, runs or is documented as owning — not quest-scene variants, not
sponsorships, and not generic occupied blocks. `Filler` is the deduped
occupied-site count minus any site already counted as a named place (METHOD §8).

| Sub-district | Named lore-relevant places | Which ones | Petrochem-occupied sites (deduped) | Filler | Noteworthy interiors |
| --- | ---: | --- | ---: | ---: | --- |
| Badlands | **2** | North Sunrise Oil Fields; Petrochem Fuel Station (I-9) | 0 | 0 | Station workshop/garage |
| Arroyo | **1** | Petrochem Nuclear Power Plant (coordinate `TBD`) | 0 | 0 | Supposed three buildings; no local record |
| CorpoPlaza | **1** | Petrochem Tower (coordinate `TBD`) | 0 | 0 | Offices + hidden NCART location (wiki only) |
| **Total** | **4** | | 0 | **0** | 1 |

Reconciliation: **0 deduped occupied sites − 0 site-backed named places = 0
filler.** All four named places are non-site records: two are marker-only (the
oil fields and the fuel station) and two are wiki-only (the Arroyo plant and the
Tower). `named + filler = 4`, which is the 2 marker-only places plus the 2
coordinate-less wiki places. `[game-data]` `[wiki]`

**Not counted, deliberately:**

- **EBM Petrochem Stadium.** A sponsor's name on a Barghest ruin. Counting it
  would add a Dogtown "named" point Petrochem does not hold (§1.2 item 9).
- **`{q104_com_petrochem_operators}`.** Kang Tao.
- **Any "Petrochem Freight Yard" point.** Seed-only, on Arasaka ground.

Interpretation for yield: this is a deliberately tiny faction. **Two of the four
named places cannot be placed by a seeder at all**, and only the oil fields is a
production asset. A sensible model is: high per-point multiplier on the oil
fields (it is the origin of the fuel economy), modest yield at the fuel station,
and **no yield** from the Tower or the plant until someone places their
coordinates. Filling the map with "Petrochem blocks" would be fabrication: the
faction has no occupied site anywhere in the game.

---

## 8. Gaps and uncertainties

1. **The seed's only Petrochem holding is on Arasaka's property.**
   `arr_petrochem_yard` (`-255.9, -1480.0, 7.6`) is 5.2 m from
   `q112_05_sm_infiltration`, a marker inside the Arasaka Industrial Park
   **warehouse** prefab used in *Down on the Street*; 267 m from the
   `arr_arasaka_industrial` centroid; and all nine sites in the sub-territory
   carry `initial_owner_faction_id = 20` (Arasaka). There is no freight yard,
   no oil infrastructure and no Petrochem record within 180 m — the nearest
   sites are `ma_std_rcr_109` (183.5 m, Wraiths), `ma_std_arr_103` (200.4 m, no
   faction) and `ma_std_rcr_06` (218.7 m, Maelstrom). The name is generated
   (`tools/generate-world-seeds.py` line 167). **Recommend retiring the zone or
   re-anchoring Petrochem's Arroyo ownership on the nuclear plant.**
   METHOD §5.3 offers "use the owned sub-territory anchor" as the fallback for
   this faction; here that advice lands a Petrochem capital on an Arasaka
   warehouse. An owned sub-territory must be checked against the faction's real
   assets, not assumed to represent one. `[game-data]`
2. **`gamedataAffiliation` has no Petrochem value.** The enum is 44 entries long
   and contains Arasaka, Biotechnica, Kang Tao, Militech, Zetatech, corpbud,
   NCPrison and even `crimson_harvest` — but not Petrochem or SovOil. This is
   primary-source confirmation that the game never assigns a Petrochem
   affiliation to any NPC, and it matches `data/factions.json`
   `affiliation_enum: null`. Do not expect to find a Petrochem guard, drone or
   crowd entry, and do not write one into a seed expecting it to render with the
   corp's colours. `[game-data]`
3. **There are literally zero presence rows.** 0 rosters, 0 areas, 0 spawns, 0
   sites. The METHOD appendix's "0 / 0 / 1 / 0" is exactly right and does not
   improve with more searching. This doc is assembled from markers, prefabs and
   enums, and a future agent should budget accordingly. `[game-data]`
4. **The oil fields are seeded to Militech.** `bls_north_oil_fields` has
   `initial_owner_faction_id = 21` and `owner_kind = corp`. The wiki gives the
   field three owners (Petrochem, SovOil, Night Corp) and no Militech share.
   Either reassign the sub-territory or model it as contested; do not present
   the current seed as lore. `[game-data]` `[wiki]`
5. **METHOD §1.2 item 1's attribution precedence fails on the faction's best
   asset.** The oil-field placement prefab is `#c_watson/northside/…`, but the
   marker is 330 m outside the Watson bbox, in the Badlands, with a dedicated
   `Badlands_NorthSunriseOilField` enum. "Placement prefab first" would file it
   in Northside. The rule needs a bbox sanity check before it is trusted.
   `[game-data]`
6. **The Arroyo nuclear plant has no record of any kind.** No marker, site,
   community, device, prefab or spawn. The only "nuclear" token in the three
   extracted sectors is `q101_vfx_nuclear_mushroom`. The wiki page cites only
   the game's "Layout" and the physical-edition map label. Its coordinate is
   `TBD` until a human places it; the extract cannot. `[wiki]` `[game-data]`
7. **Petrochem Tower has no record either.** No Corpo Plaza prefab, mappin or
   site carries the name; the tower is generic scenery. The patch-2.1
   station-inside-the-tower note is a hint, not an anchor, and the Memorial Park
   station marker is 117.6 m from the nearest generic ring-road site
   (`ma_cct_cpz_18`), which has no tower identity. `TBD`. `[wiki]` `[game-data]`
8. **The stadium is a naming trap.** "EBM Petrochem Stadium" is the game's
   largest object bearing the corp's name, and it is not Petrochem's: the wiki
   infobox leaves `owner` blank, gives `affiliation = BARGHEST`, and the 2077
   occupant communities are Barghest (`q301`/`q302`/`q304`, up to 38 entries).
   Petrochem's involvement was sponsorship/construction in the 2060s. A seeder
   ranking by name will get this backwards. `[wiki]` `[game-data]`
9. **The visible Northside refinery is not the wiki's Petrochem refinery.** The
   `nid_oil_refinery` sub-territory ("Northside Oil Wharf") is Scavenger-held
   (`ma_wat_nid_27`, 7 Scavengers); the Petrochem and SovOil refineries are
   RED-era (2040s) facilities with no 2077 record. Do not map the 2045 plant
   onto the 2077 wharf. `[game-data]` `[wiki]`
10. **The other 2077 fuel stations are not Petrochem.** Rocky Ridge
    (Corp-Bud, Wraiths), Laguna Bend (independent, flooded), Medeski
    (landfill, Wraiths) and the SovOil station on Highway 101 all look like the
    faction's business and are not. Only the Interstate 9 station has a
    Petrochem owner in its infobox. `[wiki]`
11. **The `q104` "petrochem operator" community is Kang Tao.** Seven entries,
    `dominant_faction = kang_tao`, at the AV crash site. Any grep-based
    attribution will hand Petrochem a southern-Badlands quest scene. `[game-data]`
12. **The I-9 station has no site row and no roster.** Its walkable anchor is
    the quest workshop `{q104_mp_sunset_garage}`; the station forecourt itself
    has no node. A capture volume there is hand-placed, and the workshop is
    quest-critical to *Ghost Town*. `[game-data]`
13. **"Sunrise" is not an operator.** The field's name is "North Sunrise Oil
    Fields"; no company, prefab or record uses "Sunrise" separately. The
    operators in the infobox are Petrochem, SovOil and Night Corp. `[wiki]`
14. **The seed pays 900/cycle for an empty cell.** `arr_petrochem_yard` has
    `base_income_per_cycle = 900` and `defense_rating = 70`, the same band as
    real facilities, while containing nothing Petrochem owns. If the zone is
    kept, its yield is fiction; if it moves to the Arroyo plant, the yield has a
    wiki-documented facility behind it. `[game-data]`
15. **There is no pipeline, derrick or refinery asset to capture.** The lore's
    pipeline network and tank farms are not modelled; the oil-field drills are
    static meshes with no gameplay nodes. A Petrochem base is necessarily an
    open landscape or a roadside building, never an industrial interior.
    `[game-data]`

---

## 9. Sources

Local:

- `dist/extract/markers.jsonl` — `{bls_bls_dataterm_}05` (oil-field dataterm
  anchor), `{sq031_mp_oil_fields}`, `{sq031_05_sm_grave}`,
  `{q104_mp_sunset_garage}`, `{q103_mp_motel_room}`,
  `{q112_05_sm_infiltration}`, `{ue_metro_station_09_city_center_arrival}`,
  `{ue_metro_station_19_pacifica_stadium_arrival}`.
- `dist/extract/areas.jsonl` — 0 Petrochem areas; the Kang Tao
  `{q104_com_petrochem_operators}` and `{q104_com_petro_gas_station}` rows;
  the `q301`/`q302`/`q304` stadium communities.
- `data/sites/sites.json` — no site has faction 43; the nine sites inside
  `arr_petrochem_yard` (all `initial_owner_faction_id = 20`); sites 385
  (`sts_std_arr_12`) and 341 (`sts_bls_ina_03`).
- `data/sites/{rosters,guards,triggers,spots,patrols,doors,suitabilities,communities}.json`
  — empty for faction 43; the roadhouse garage nodes; the oil-field barracks
  markers.
- `data/{factions,districts,sub_territories,landmarks,control_centers,spawn_points,faction_headquarters}.json`
  — faction id 43, `affiliation_enum: null`, sub 52 `arr_petrochem_yard`,
  sub 86 `bls_north_oil_fields`, CC anchors and owners.
- `dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_{0,1,2}.streamingsector.json`
  — `loc_sq031_oilfield_barracks`, `se1/loc_q103_roadhouse`,
  `#c_santo_domingo/arroyo/loc_mq062` (NC Prison),
  `#c_santo_domingo/arroyo/loc_q112_arasaka_industrial_park_warehouse`; absence
  checks for `petrochem`, `nuclear`, `refinery`, `derrick`, `pumpjack`,
  `pipeline`, `sovoil`, `chooh`.
- `refs/cyberpunk/orphans.swift` — `gamedataDistrict.Badlands_NorthSunriseOilField = 18`
  (line 4845); the full `gamedataAffiliation` enum (no Petrochem, no SovOil).
- `tools/generate-world-seeds.py` — line 167 proves "Petrochem Freight Yard" is a
  generated grid name; line 113 the "Northside Oil Wharf" seed name.

Wiki (MediaWiki API, wikitext only):

- [Petrochem](https://cyberpunk.fandom.com/wiki/Petrochem)
- [Petrochem/Netpage](https://cyberpunk.fandom.com/wiki/Petrochem/Netpage)
- [Petrochem Tower](https://cyberpunk.fandom.com/wiki/Petrochem_Tower)
- [Northern Oil Fields](https://cyberpunk.fandom.com/wiki/Northern_Oil_Fields)
- [Chippin' In (quest)](https://cyberpunk.fandom.com/wiki/Chippin%27_In_(quest)) (`baseid = sq031_rogue`)
- [Petrochem Fuel Station (Interstate 9)](https://cyberpunk.fandom.com/wiki/Petrochem_Fuel_Station_(Interstate_9))
- [Petrochem Nuclear Power Plant](https://cyberpunk.fandom.com/wiki/Petrochem_Nuclear_Power_Plant)
- [Petrochem Refinery Terminal](https://cyberpunk.fandom.com/wiki/Petrochem_Refinery_Terminal) (2020, not in game)
- [Petrochem Oil Refinery](https://cyberpunk.fandom.com/wiki/Petrochem_Oil_Refinery) (RED, not in game)
- [Petrochem Plastics Plant](https://cyberpunk.fandom.com/wiki/Petrochem_Plastics_Plant) (RED, not in game)
- [Petrochem Offices (2020)](https://cyberpunk.fandom.com/wiki/Petrochem_Offices_(2020)) /
  [(RED)](https://cyberpunk.fandom.com/wiki/Petrochem_Offices_(RED)) (not in game)
- [EBM Petrochem Stadium](https://cyberpunk.fandom.com/wiki/EBM_Petrochem_Stadium)
- [CHOOH2](https://cyberpunk.fandom.com/wiki/CHOOH2)
- [SovOil](https://cyberpunk.fandom.com/wiki/SovOil)
- [Sunset Motel](https://cyberpunk.fandom.com/wiki/Sunset_Motel)
- [Interstate 9](https://cyberpunk.fandom.com/wiki/Interstate_9)
- [Red Peaks](https://cyberpunk.fandom.com/wiki/Red_Peaks)
- [Night City Prison](https://cyberpunk.fandom.com/wiki/Night_City_Prison)
- [Megabuilding H6](https://cyberpunk.fandom.com/wiki/Megabuilding_H6)
- [Electric Corporation Power Plant](https://cyberpunk.fandom.com/wiki/Electric_Corporation_Power_Plant)
- [Rocky Ridge Fuel Station](https://cyberpunk.fandom.com/wiki/Rocky_Ridge_Fuel_Station)
- [Laguna Bend Fuel Station](https://cyberpunk.fandom.com/wiki/Laguna_Bend_Fuel_Station)
- [Medeski Fuel Station](https://cyberpunk.fandom.com/wiki/Medeski_Fuel_Station)
- [Wind Farms](https://cyberpunk.fandom.com/wiki/Wind_Farms)
- [Coronado Dam](https://cyberpunk.fandom.com/wiki/Coronado_Dam)

Earlier repo research:

- [`docs/research/factions/METHOD.md`](./METHOD.md)
- [`docs/research/factions/kang-tao.md`](./kang-tao.md)
- [`docs/research/factions/biotechnica.md`](./biotechnica.md)
- [`docs/research/factions/arasaka.md`](./arasaka.md)

---

## 10. Machine-readable block

Strict JSON for seeding (contract in [`METHOD.md`](./METHOD.md) §10). Every
coordinate was verified against the local record named in `source` on
2026-11-25; none came from the wiki. `null` means `TBD`, never `0`.

```json
{
  "faction_code": "petrochem",
  "hq": {
    "name": "North Sunrise Oil Fields",
    "district": "Badlands",
    "sub_district": "Badlands",
    "x": -1835.695,
    "y": 3719.295,
    "z": 6.742,
    "source": "dist/extract/markers.jsonl {bls_bls_dataterm_}05 (fast-travel dataterm; equals data/sub_territories.json bls_north_oil_fields and cc_bls_north_oil_fields)",
    "confidence": "game-data+wiki"
  },
  "alternate_hqs": [
    {
      "name": "Petrochem Nuclear Power Plant",
      "district": "SantoDomingo",
      "sub_district": "Arroyo",
      "x": null,
      "y": null,
      "z": null,
      "source": "no local record; wiki infobox only (type = Nuclear power plant, owner = Petrochem, street = Republic Way) - coordinate TBD",
      "confidence": "wiki"
    },
    {
      "name": "Petrochem Tower",
      "district": "CityCenter",
      "sub_district": "CorpoPlaza",
      "x": null,
      "y": null,
      "z": null,
      "source": "no local record; wiki infobox only (type = Regional HQ, owner = Petrochem, location = Corporate Plaza) - coordinate TBD",
      "confidence": "wiki"
    }
  ],
  "test_control_point": {
    "name": "Petrochem Fuel Station (Interstate 9)",
    "district": "Badlands",
    "sub_district": "Badlands",
    "x": 1706.187,
    "y": -755.859,
    "z": 49.801,
    "source": "dist/extract/markers.jsonl {q104_mp_sunset_garage} (station workshop east of the Sunset Motel; no sites.json row)",
    "confidence": "game-data+wiki+inferred"
  },
  "control_points": [
    {
      "rank": 1,
      "name": "North Sunrise Oil Fields",
      "type": "oil_field",
      "relevance": 5,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": -1835.695,
      "y": 3719.295,
      "z": 6.742,
      "source": "dist/extract/markers.jsonl {bls_bls_dataterm_}05 (fast-travel dataterm; equals data/sub_territories.json bls_north_oil_fields and cc_bls_north_oil_fields)",
      "confidence": "game-data+wiki",
      "interior": false,
      "revenue_streams": ["energy", "logistics"],
      "nearest_cc_code": "cc_bls_north_oil_fields",
      "nearest_cc_m": 0.0
    },
    {
      "rank": 2,
      "name": "Petrochem Fuel Station (Interstate 9)",
      "type": "fuel_station",
      "relevance": 4,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": 1706.187,
      "y": -755.859,
      "z": 49.801,
      "source": "dist/extract/markers.jsonl {q104_mp_sunset_garage} (station workshop east of the Sunset Motel; no sites.json row)",
      "confidence": "game-data+wiki+inferred",
      "interior": true,
      "revenue_streams": ["energy", "retail"],
      "nearest_cc_code": "cc_bls_sunset_motel",
      "nearest_cc_m": 74.0
    },
    {
      "rank": 3,
      "name": "Petrochem Nuclear Power Plant",
      "type": "power_plant",
      "relevance": 4,
      "district": "SantoDomingo",
      "sub_district": "Arroyo",
      "x": null,
      "y": null,
      "z": null,
      "source": "no local record; wiki infobox only (type = Nuclear power plant, owner = Petrochem, street = Republic Way) - coordinate TBD",
      "confidence": "wiki",
      "interior": false,
      "revenue_streams": ["energy"],
      "nearest_cc_code": null,
      "nearest_cc_m": null
    },
    {
      "rank": 4,
      "name": "Petrochem Tower",
      "type": "corporate_hq",
      "relevance": 4,
      "district": "CityCenter",
      "sub_district": "CorpoPlaza",
      "x": null,
      "y": null,
      "z": null,
      "source": "no local record; wiki infobox only (type = Regional HQ, owner = Petrochem, location = Corporate Plaza) - coordinate TBD",
      "confidence": "wiki",
      "interior": true,
      "revenue_streams": ["energy", "logistics"],
      "nearest_cc_code": null,
      "nearest_cc_m": null
    }
  ],
  "subdistrict_counts": {
    "Badlands": {"named": 2, "filler": 0},
    "Arroyo": {"named": 1, "filler": 0},
    "CorpoPlaza": {"named": 1, "filler": 0}
  }
}
```
