# Maelstrom — Lore-Relevant Control Points

Status: faction research run, 2026-11-25. One faction, one document.
Scope: turn the current generic ~5-control-centres-per-sub-district grid into
lore-relevant, capturable places for Maelstrom, with an honest count per
sub-district. Method: this doc conforms to [`METHOD.md`](./METHOD.md); research
snippets, wiki rules, the revenue-code vocabulary and the JSON-block contract
live there. Worked example: [`tyger-claws.md`](./tyger-claws.md).

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Position, site, community, roster or spawn record read from `dist/extract/` or `data/sites/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/artbook/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My inference linking a named place to a game record; reasoning stated | Weak, flagged |

No coordinate below is guessed. Every `(x, y, z)` is either copied from a named
record in the local extracts or marked `TBD`.

---

## 1. Summary

Maelstrom is Night City's flagship **boostergang**: ≈1,300 members in 2077,
threat level "Extreme", obsessed with chrome and the Net, and structured as a
loose set of crews (4–5 for turf patrols, up to 30 for raids and cargo
protection). `[wiki]` The wiki's organization infobox names the 2077 seat of
power as **Totentanz's Building** in Watson, with factions locations in *Watson*
and *City Center*. `[wiki]`

Their economic model is **smuggling plus chrome**, not nightlife:

- **Drugs and illegal meds** — the stated main revenue stream; manufacture,
  wholesale and retail. `[wiki]`
- **Smuggling** — contraband moving through the Northside docks and warehouses;
  they run stolen corporate cargo through the district. `[wiki]` `[game-data]`
- **Cyberware** — reclaimed and scavenged implants traded to ripperdocs across
  the city, and two Maelstrom-payroll clinics in Northside. `[wiki]`
- **Chop shops / vehicle theft** — Malorian Arms vans and similar cargo are
  stolen and broken down at Wicked Tires. `[wiki]`
- **Illegal braindance** — "Numbness" and other XBD; the NCPD never proved it,
  but Maelstrom guards at least one XBD tuning studio. `[wiki]`
- **The Totentanz** — the "most popular gang club and drink-and-riot venue in
  Night City", explicitly a significant income source. `[wiki]`
- **Contract violence and corporate heists** — messy, public hit jobs; heists on
  heavily guarded corporate transports. `[wiki]`
- **Protection rackets** — a 2020-era staple, still implicit in their turf
  behaviour. `[wiki]`

The gang's footprint is almost entirely in **Northside (Watson)**: 46 of the 73
community areas containing Maelstrom spawns, 11 of 21 deduped occupied sites,
and 45 of 68 Maelstrom spawn points. Little China (9 areas / 7 spawn points /
4 sites) and Kabuki (7 / 8 / 1) are pressure zones, not owned economy. Every
named place in this catalog except one sits in Northside.

---

## 2. Territory

### 2.1 Districts

| Evidence kind | Result |
| --- | --- |
| (a) Wiki/lore | Territory is "the industrial part of Watson"; the 2077 database entry says Maelstrom "controls the districts of Watson and the Northside Industrial District (NID)". HQ = Totentanz's Building, Watson. Faction locations listed as Watson + City Center. `[wiki]` |
| (b) Vanilla map gang panel | `data/districts.json`: Watson `vanilla_gangs = ["Maelstrom","TygerClaws"]`. Earlier research (`docs/research/factions-gangs-territories.md` §2.2) records the sub-district panel as Maelstrom in **Northside** and as a listed (non-owning) presence in **Kabuki**. Exact `District_Record.Gangs` arrays were never dumped, so treat the sub-district split as `[wiki]`-level. |
| (c) Game-data counts | 73 community areas contain Maelstrom spawns (68 dominant); 22 candidate roster sites, 21 after 25 m dedupe; 134 roster units; 68 `data/spawn_points.json` entries with `faction_id == 1`; 7 seeded sub-territories. |

The seed already assigns Maelstrom seven sub-territories — and they are the
right ones:

| `sub_territory_id` | Code | Sub-district | Landmark | Units |
| ---: | --- | --- | --- | ---: |
| 1 | `lch_dockside_yard` | LittleChina | Little China Dockside Yard | 4 spawns |
| 2 | `lch_goldsmith_plaza` | LittleChina | Goldsmith Street Plaza | 1 spawn |
| 11 | `nid_all_foods_plant` | Northside | All Foods Plant | 12 spawns |
| 12 | `nid_totentanz_yard` | Northside | Totentanz Industrial Yard | 14 spawns |
| 13 | `nid_martin_st_docks` | Northside | Martin Street Depot | 9 spawns |
| 15 | `nid_pershing_warehouses` | Northside | Pershing Street Warehouses | 10 spawns |
| 17 | `awf_ebunike_docks` | ArasakaWaterfront | Ebunike Container Docks | 2 spawns |

`[game-data]`. 49 of the 68 Maelstrom spawn points fall in the two Northside
clusters around All Foods / Totentanz and Martins/Pershing — a good match to the
lore claim that they hold the NID.

### 2.2 Sub-district presence

Counts are from `dist/extract/areas.jsonl` (`maelstrom` in `faction_counts`,
"dominant" = `dominant_faction == maelstrom`), `data/spawn_points.json`
(`faction_id == 1`), and the deduped site set from §2.3.

| Sub-district | District | (a) Lore | (b) Vanilla panel | (c) Areas (dominant) | (c) Spawn pts | Maelstrom-occupied sites* |
| --- | --- | --- | --- | ---: | ---: | ---: |
| Northside | Watson | Core territory / HQ | Maelstrom (+Mox, Scavs) | 46 (45) | 45 | 12 |
| LittleChina | Watson | Turf, not named places | Tyger Claws (+Maelstrom) | 9 (9) | 7 | 4 |
| Kabuki | Watson | Pressure/raids only | Tyger Claws (+Maelstrom, Mox) | 7 (7) | 8 | 1 |
| ArasakaWaterfront | Watson | Docks contact | Arasaka (+Maelstrom) | 1 (1) | 2 | 0 |
| CorpoPlaza | CityCenter | Incidental | — (corp) | 4 (3) | 2 | 1 |
| RanchoCoronado | SantoDomingo | Incidental | 6th Street | 0 (0) | 0 | 2 |
| Arroyo | SantoDomingo | Incidental | 6th Street | 0 (0) | 0 | 1 |
| Coastview | Pacifica | Incidental (Dogtown thug communities) | Voodoo Boys, Animals | 2 (1) | 1 | 0 |
| CharterHill | Westbrook | Incidental | Tyger Claws (+6th Street) | 2 (1) | 0 | 0 |
| Glen / VistaDelRey | Heywood | Incidental | Valentinos | 0 (0) | 1 / 1 | 0 |
| JapanTown | Westbrook | Incidental | Tyger Claws | 1 (1) | 1 | 0 |
| Badlands | Badlands | Incidental (border crossing) | Aldecaldos, Wraiths | 1 (0) | 0 | 0 |

\* Deduped `data/sites/sites.json` rows with `default_faction_id == 1` **or** at
least one roster entry resolving to Maelstrom; variants within 25 m collapse
(§2.3). Sub-district for a **site** is taken from the geocode token in the site
code, with two deliberate exceptions recorded in §8.1/§8.2.

**Reading the counts.** Community-area counts measure *presence*, not
"lore-relevant places". The nine CorpoPlaza/Coastview/CharterHill area hits are
worth discounting: `{q115_com_nest_dead_people}`, `{sa_ep1_203_com_combat}`,
`{sq025_com_thugs_mean}`, `{q301_com_border_community}` and
`{q305_com_border_crossing_}002` are quest/combat communities whose
`faction_counts` list Maelstrom as generic opposition, not as turf. The one real
CorpoPlaza datum is `ma_cct_cpz_01` — 9 Maelstrom at Memorial Ring West
`[game-data]`.

**Attribution caveat.** `areas.jsonl.district_code` is not safe: Maelstrom's
Northside areas are correctly labelled `watson`, but `{mq032_com_maelstrom}`
sits in Arasaka Waterfront geography while carrying a Watson path token, and the
Dogtown/Pacifica thug communities are labelled `dogtown`. All counts above were
re-attributed by geocode token, then nearest geocoded site, then nearest
sub-territory centroid.

### 2.3 Candidate sites and dedupe

22 candidate sites → **21 after 25 m dedupe**. The single collapse is
`sts_wat_kab_02` (gig *Hippocratic Oath*, 9 units) sitting 11.5 m from
`ma_wat_nid_06` (scanner hustle, 10 units): **both are the Clean Cut clinic**
(§3.1). Neither is a quest variant of the other, so the dedupe rule collapses
two different activity records for one building — worth noting.

| Site | Units | Interior | Sub-district | Coordinates | What it is |
| --- | ---: | :---: | --- | --- | --- |
| `ma_wat_nid_02` | 13 | no | Northside | `-1811.7, 2544.2, 26.0` | Maelstrom outpost 01 (`#ma_outpost_01_ga`, netrunner, sniper) — filler |
| `sts_wat_nid_04` | 12 | yes | Northside | `-1811.7, 2659.2, 10.8` | Gottfrid & Fredrik's XBD studio (*Dirty Biz*) — catalog #9 |
| `ma_wat_nid_06` | 10 | no | Northside | `-1170.0, 2419.6, 7.1` | Clean Cut clinic — catalog #4 (kept from dedupe) |
| `sts_wat_nid_06` | 10 | no | Northside | `-1347.4, 2767.4, 7.2` | Wicked Tires Autoshop (*Lousy Kleppers*) — catalog #5 |
| `ma_cct_cpz_01` | 9 | no | CorpoPlaza | `-1657.5, 35.3, 7.5` | Memorial Ring West hold-out — filler |
| `sts_wat_nid_07` | 6 | no | Northside | `-815.7, 2434.7, 57.1` | Maelstrom torture warehouse (*Scrolls before Swine*) — catalog #6 |
| `ma_wat_lch_02` | 6 | no | LittleChina | `-1934.9, 1561.0, 8.9` | Homeless-camp shakedown — filler |
| `ma_std_rcr_04` | 5 | no | RanchoCoronado | `633.4, -941.7, 28.6` | Gang-watch execution — filler |
| `ma_std_rcr_06` | 5 | no | RanchoCoronado | `-46.2, -1418.0, -1.9` | Gang-watch robbery — filler |
| `ma_std_rcr_17` | 5 | no | RanchoCoronado | `1091.6, -1039.1, 29.6` | Gang-watch street violence — filler |
| `ma_wat_kab_03` | 5 | no | Kabuki | `-876.9, 1865.7, 35.7` | Robbery hold-up — filler |
| `ma_wat_lch_07` | 5 | no | LittleChina | `-1865.0, 1587.8, 10.2` | Police vs. Maelstrom shoot-out — filler |
| `ma_wat_lch_12` | 5 | no | LittleChina | `-1267.1, 1759.4, 18.2` | Street execution — filler |
| `ma_wat_nid_13` | 5 | no | Northside | `-1346.8, 2161.4, 15.8` | Resource-grab defend — filler |
| `ma_wat_nid_14` | 5 | no | Northside | `-1239.4, 2688.9, 7.2` | Gang-watch ambush — filler |
| `ma_wat_lch_15` | 4 | no | LittleChina | `-1445.0, 1861.4, 18.2` | Hidden-stash guard — filler |
| `ma_wat_nid_15` | 4 | no | Northside | `-1529.4, 2509.8, 7.1` | Cyberpsycho den (Johnny cameo area) — filler |
| `ma_wat_nid_22` | 4 | yes | Northside | `-1060.4, 2789.5, 7.1` | Cyberpsycho apartment block — filler |
| `ma_wat_nid_23` | 4 | no | Northside | `-1313.3, 2415.3, 11.1` | Gang-watch shakedown — filler |
| `sts_wat_nid_05` | 2 | no | Northside | `-1489.0, 2917.8, 7.2` | HeavenMed clinic (*Rite of Passage*) — catalog #3 |
| `ma_wat_nid_03` | 1 | no | Northside | `-1702.7, 2231.4, 18.2` | Cyberpsycho lair 41 m from Totentanz — filler |

`[game-data]` for every row.

---

## 3. Location catalog

World-space metres, `Z` up. "Interior?" means the game has a distinct interior
cell/sector, even where `is_interior` is unset.

| # | Name | Type | District / sub-district | Interior? | Business? (what it earns) | Coordinates (x, y, z) | Coordinate source record | Linked communities / sites | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **Totentanz** (HQ) | Club / drink-and-riot venue, upper floors of an unfinished hotel | Watson / Northside | Yes — elevator from street level (z≈19) to 1st floor (z≈23) and 3rd floor (z≈91) | Yes: bar, live neo-death-metal, drug retail, Maelstrom XBD sales, gang "court" | `-1731.746, 2218.427, 91.111` (3rd-floor club entrance); `-1749.289, 2247.528, 19.413` (street door); `-1718.632, 2205.353, 87.201` (dancefloor) | `markers.jsonl` `sq011_mp_totentanz_entrance`, `sq011_mp_totentanz_door`, `dancefloor_sm_totentanz` | `sq011_club_gangers` (`15677093351520050684`, 14 Maelstrom); `sq011_thugs` (`11140609030971206231`, 5); `sq011_patricia`; enum `Northside_Totentaz` | `[game-data]` `[wiki]` |
| 2 | **All Foods Plant** | Defunct protein-processing factory used as main hideout | Watson / Northside | Yes — production floor, lab, corridors, makeshift cell block (z≈50–60) | Yes: drug/arms depot, contraband staging, deal venue; not a working factory | `-769.763, 2203.538, 52.384` (street intercom/entrance); `-856.355, 2229.063, 55.915` (main hall); `-876.235, 2265.387, 59.308` (Brick's cell terminal) | `markers.jsonl` `q003_mp_allfoods_intercom`, `q003_mp_main_hall`, `q003_mp_brick_prison_door_terminal`; `data/sites/sites.json` site 413 anchor is the northern approach | `q003_com_main_hall` (`3827570806657794214`, 5 Maelstrom); `q003_factory_combat_main` (7); `q003_com_lab`; enum `Northside_All_Foods` | `[game-data]` `[wiki]` |
| 3 | **HeavenMed** | Ripperdoc clinic in a converted fish cannery ("Meaty Fish") | Watson / Northside | Yes — lobby, makeshift OR, offices (1st floor); lockers + server room (2nd floor) | Yes: cyberware surgery and sales on the Maelstrom payroll; server room holds the initiation-rite recordings | `-1489.039, 2917.785, 7.240` (site anchor); `-1480.100, 2909.600, 11.200` (upstairs restricted area) | `data/sites/sites.json` site 411 `sts_wat_nid_05`; `data/sites/guards.json` `#nid_05_restricted_movement_upstairs` | `{#nid_05_com}` (`15783662965541787457`, 10 Maelstrom); `{nid_05_com_reinforcement}`; roster `Character.nid_05_maelstrom_*` | `[game-data]` `[wiki]` |
| 4 | **Clean Cut** | Ripperdoc clinic | Watson / Northside | Yes — reception, back office, surgery room | Yes: cyberware repair/sales; held a Maelstrom patient and an unpaid ripperdoc | `-1158.526, 2419.501, 7.109` (gig site anchor); `-1160.080, 2420.670, 5.270` (community centre) | `data/sites/sites.json` site 392 `sts_wat_kab_02`; sister record site 219 `ma_wat_nid_06` (`-1170.0, 2419.6`) | `kab_02_com_ar` (`15093778234644979055`, 6 Maelstrom); guard areas `reception`, `back_office`, `reinf`; enum `Northside_CleanCut` | `[game-data]` `[wiki]` |
| 5 | **Wicked Tires Autoshop** | Chop shop / stolen-vehicle warehouse | Watson / Northside | Yes — warehouse interior, garage bay | Yes: vehicle chopping and fencing; Malorian Arms transport stashed here | `-1347.384, 2767.438, 7.221` | `data/sites/sites.json` site 412 `sts_wat_nid_06`; guard area `#nid_06_guard_area_inside` | `sts_wat_nid_06_enemies_inside_ground_floor` (5); `_enemies_outside` (5); workspots `#nid_05_ws_garage_*`-style garage nodes; `Character.sts_wat_nid_06_*` | `[game-data]` `[wiki]` |
| 6 | **Maelstrom Warehouse** (Industrial & Eisenhower) | Torture den / stash warehouse, 2 floors | Watson / Northside | Yes — ground floor + second-floor computer room, roof hatch | No (not a business): torture and evidence storage | `-896.700, 2363.300, 53.000` (guard area); `-815.677, 2434.696, 57.109` (site anchor — 110 m off, see §3.1) | `data/sites/guards.json` `#nid_07_ga_01`; `{nid_07_com}` (`17888136387075270937`, 6 Maelstrom) | `nid_07_com` (6 Maelstrom); triggers `#nid_07_tr_inside_001/002`, `#nid_07_tr_terminal_room`, `#nid_07_tr_roof*` | `[game-data]` `[wiki]` |
| 7 | **Ebunike Docks** | Container docks and moored freighter (`DV Ebunike`) | Watson / Northside | No (open docks; ship decks/interiors are quest cells) | Yes: container smuggling and cargo handling — the docks' whole 2045–2077 economy | `-1530.033, 2984.774, 7.305` (dock marker); `-1574.684, 3068.235, 9.233` (ship deck) | `markers.jsonl` `sq031_03_sm_ebunike`, `sq031_mp_to_ebumike_deck` | `sq031_maelstrom` (14 Maelstrom); `sq031_maelstrom_boat` (3); `mq032_com_maelstrom` (5); seed sub-territory 17 | `[game-data]` `[wiki]` |
| 8 | **Abandoned Warehouse** (Northside Docks, Bennett St) | Warehouse stash | Watson / **ArasakaWaterfront** by position (wiki says Northside) | Yes — warehouse interior below dock level | Yes: contraband/artifact stash; *Sacrum Profanum* raid site | `-2152.954, 2876.865, 7.110` (dock-level scene marker); interior community at `z = -44` | `markers.jsonl` `mq032_02_sm_maelstrom`; `{mq032_com_maelstrom}` | `mq032_com_maelstrom` (5 Maelstrom, z=-44); `mq032_01_sm_hook`; seed sub-territory 17 | `[game-data]` `[wiki]` `[inferred]` |
| 9 | **Gottfrid & Fredrik's XBD studio** (unnamed) | Illegal braindance tuning studio | Watson / Northside | Yes | Yes: XBD editing and distribution; raw BD masters on site | `-1841.550, 2638.670, 14.890` (studio marker); `-1811.684, 2659.179, 10.850` (site anchor) | `markers.jsonl` `sts_sm_wat_nid_04_gottfrid_fredrik`; `data/sites/sites.json` site 410 `sts_wat_nid_04` | 12 Maelstrom units; `#nid_04_tr_gaf_studio`, `#nid_04_ws_fredrik_bd`; `Character.sts_wat_nid_04_enemy_*` | `[game-data]` `[wiki]` |
| 10 | Maelstrom outpost 01 | Fortified rooftop outpost / lair | Watson / Northside | No (roof + yard) | No — forward operating base | `-1811.700, 2544.190, 26.011` | `data/sites/sites.json` site 216 `ma_wat_nid_02` | `ma_outpost_01_com` (13 Maelstrom); `#ma_outpost_02_ga_netrunner/sniper` | `[game-data]` (no wiki name) |

### 3.1 How the name→coordinate links were proven

Interior node names in `data/sites/{guards,triggers,spots,patrols,devices}.json`
do most of the work. Wiki `baseid` is the second lever — three of the five
site-backed points are confirmed by an exact `baseid` match, which is much
stronger evidence than the pilot's inferred name links:

- `sts_wat_nid_05` → **Gig: Rite of Passage** (`baseid = sts_wat_nid_05`), whose
  journal explicitly sends V to **HeavenMed**, "the place they put all the new
  recruits under the knife". Site 411 has `#nid_05_tr_operation_VO`,
  `#nid_05_ws_checking_servers_*`, `#nid_05_tr_reception_VO`,
  `#nid_05_ws_garage_*` and `#nid_05_restricted_movement_upstairs` — the exact
  two-floor lobby/OR/server-room layout. `[wiki]` `[game-data]`
- `sts_wat_kab_02` → **Gig: Hippocratic Oath** (`baseid = sts_wat_kab_02`),
  location **Clean Cut**. Guard areas `reception`, `back_office`, and spots
  `#kab_02_ws_gang_anest*` (anaesthetic), `#kab_02_door_surgery_002a` plus the
  roster entry `Character.sts_wat_kab_02_maelstrom_patient` match the gig's
  "ripperdoc forced to treat a Maelstrom patient". `[wiki]` `[game-data]`
- `sts_wat_nid_06` → **Gig: Lousy Kleppers** (`baseid = sts_wat_nid_06`),
  location **Wicked Tires Autoshop**, Offshore St. `#nid_06_guard_area_inside`,
  `#nid_06_tr_explosive_tank` and 7 doors sit inside a chop-shop warehouse.
  `[wiki]` `[game-data]`
- `sts_wat_nid_07` → **Gig: Scrolls before Swine** (`baseid = sts_wat_nid_07`),
  "Maelstrom warehouse on the corner of Industrial and Eisenhower". 6 roster
  units matches the wiki's "six gang members, three outside and three inside".
  `#nid_07_tr_inside_001/002`, `#nid_07_tr_terminal_room` and
  `#nid_07_tr_warehouse_area` match the described layout. `[wiki]` `[game-data]`
- `sts_wat_nid_04` → **Gig: Dirty Biz** (`baseid = sts_wat_nid_04`) — the
  Gottfrid/Fredrik XBD studio, "buildings off Shipyard Way". Marker
  `sts_sm_wat_nid_04_gottfrid_fredrik` names the two tuners directly.
  `[wiki]` `[game-data]`
- **Totentanz** has no `sites.json` record at all. The name is proven by marker
  names alone (`sq011_mp_totentanz_*`, `dancefloor_sm_totentanz`,
  `totentanz_sm_bouncer_default`), and `sq011`'s wiki page is **Second
  Conflict**, whose location infobox is Totentanz and whose walkthrough says
  "travel to the third floor and go to the proper entrance to the club" — the
  z≈91 entrance marker. The gamedata enum is `Northside_Totentaz` (id 108).
  `[game-data]` `[wiki]`
- **All Foods Plant** has no `sites.json` record either. `q003`'s wiki page is
  **The Pickup** and its markers name the intercom, meat factory, main hall,
  Brick's prison door and the Royce bossfight — all inside the factory. The
  distance to the seed landmark/control centre is 0.5 m. Enum
  `Northside_All_Foods` (id 105). `[game-data]` `[wiki]`
- **Ebunike Docks** is proven by `sq031_03_sm_ebunike`,
  `sq031_mp_to_ebumike_deck` and `sq031_ps_ebinike`. `sq031` is **Chippin' In**
  (Grayson aboard the freighter). The wiki infobox lists
  `affiliation = Tyger Claws (formerly), Maelstrom`. `[game-data]` `[wiki]`
- **Abandoned Warehouse** is the weakest link: `mq032` is **Sacrum Profanum**
  (location "Cargo Bay / Abandoned Warehouse", enemies Maelstrom), and the only
  Maelstrom marker is `mq032_02_sm_maelstrom`. I take it as the warehouse
  because the Maelstrom community is underground at `z = -44` while the marker
  is at dock level — the warehouse has a lower level, the open vendor hub does
  not. Flagged `[inferred]`. `[wiki]` `[game-data]`

Two coordinate cautions learned here:

- **Site anchors can be well off the building.** `sts_wat_nid_07`'s anchor is
  `(-815.7, 2434.7)` but all three guard areas and the 6-unit Maelstrom
  community cluster at `(-890, 2360)`, 110 m away. Use guard-area or community
  coordinates for interiors, not `anchor_*`.
- **`sub_territory_id` is a nearest-centroid guess, not a polygon test.** Three
  sites carry a sub-territory that contradicts their geocode token (§8.1).

### 3.2 Maelstrom-occupied generic sites (the filler pool)

`data/sites/suitabilities.json` tags. Note what is *missing*: **no filler site
carries `club`, `market_stall`, `chop_shop`, `clinic`, `warehouse` or
`factory`** — every generic Maelstrom site is tagged `raid_target`, usually with
`rooftop_access`, `stealth_entry` or `camera_net`. In plain terms: Maelstrom's
non-named footprint is combat outposts, not businesses. That is a real
distinction from the Tyger Claws, whose filler pool was full of `club` and
`market_stall` affordances.

| Site | Sub-district | Interior | Suitability tags | Units | Coordinates | Note |
| --- | --- | :---: | --- | ---: | --- | --- |
| `ma_wat_nid_02` | Northside | no | lab, officer_site, raid_target, rooftop_access | 13 | `-1811.7, 2544.2, 26.0` | largest non-named garrison; best generic "occupied block" |
| `ma_cct_cpz_01` | CorpoPlaza | no | branch_office, hostage_site, raid_target | 9 | `-1657.5, 35.3, 7.5` | only real Maelstrom point outside Watson; sub-territory is Arasaka-owned |
| `ma_wat_lch_02` | LittleChina | no | raid_target, rooftop_access | 6 | `-1934.9, 1561.0, 8.9` | shakedown of a homeless camp |
| `ma_wat_nid_13` | Northside | no | camera_net, raid_target, rooftop_access, stealth_entry | 5 | `-1346.8, 2161.4, 15.8` | seed says Kabuki, token says Northside (§8.1) |
| `ma_wat_nid_14` | Northside | no | camera_net, raid_target, stealth_entry | 5 | `-1239.4, 2688.9, 7.2` | |
| `ma_wat_lch_07` | LittleChina | no | raid_target, rooftop_access | 5 | `-1865.0, 1587.8, 10.2` | NCPD shoot-out at the dockside yard |
| `ma_wat_lch_12` | LittleChina | no | hostage_site, raid_target, rooftop_access | 5 | `-1267.1, 1759.4, 18.2` | public execution |
| `ma_wat_kab_03` | Kabuki | no | camera_net, hostage_site, raid_target, rooftop_access, stealth_entry | 5 | `-876.9, 1865.7, 35.7` | only Kabuki site with Maelstrom |
| `ma_std_rcr_04` | RanchoCoronado | no | hostage_site, raid_target, rooftop_access, vehicle_bay | 5 | `633.4, -941.7, 28.6` | gang-watch, not turf |
| `ma_std_rcr_06` | RanchoCoronado | no | hostage_site, raid_target, vehicle_bay | 5 | `-46.2, -1418.0, -1.9` | seed says Arroyo, token says Rancho (§8.2) |
| `ma_std_rcr_17` | RanchoCoronado | no | hostage_site, raid_target, rooftop_access, vehicle_bay | 5 | `1091.6, -1039.1, 29.6` | gang-watch, not turf |
| `ma_wat_lch_15` | LittleChina | no | raid_target, rooftop_access | 4 | `-1445.0, 1861.4, 18.2` | seed says Kabuki, token says Little China (§8.1) |
| `ma_wat_nid_15` | Northside | no | raid_target | 4 | `-1529.4, 2509.8, 7.1` | cyberpsycho den |
| `ma_wat_nid_22` | Northside | yes | camera_net, raid_target, stealth_entry | 4 | `-1060.4, 2789.5, 7.1` | only non-named interior (apartment block) |
| `ma_wat_nid_23` | Northside | no | camera_net, raid_target, rooftop_access, stealth_entry | 4 | `-1313.3, 2415.3, 11.1` | |
| `ma_wat_nid_03` | Northside | no | camera_net, raid_target, rooftop_access, stealth_entry | 1 | `-1702.7, 2231.4, 18.2` | ground level under Totentanz's block |

Treat the tags as gameplay affordances, not lore. They say a place *can* host a
raid or a stash; they do not prove a business.

---

## 4. Economic structure

### 4.1 Revenue streams → catalog locations

| Revenue stream | Code(s) | Catalog locations that produce it | Evidence / notes |
| --- | --- | --- | --- |
| Drugs / illegal meds (main stream) | `drugs` | Totentanz (1); All Foods (2); HeavenMed (3) | Wiki: "The main revenue stream for Maelstromers came from smuggling illegal meds and drugs." The Totentanz is where they "buy drugs"; All Foods stages product; HeavenMed is a medclinic on the payroll. `[wiki]` |
| Smuggling / contraband logistics | `smuggling` | Ebunike Docks (7); Abandoned Warehouse (8); Wicked Tires (5); All Foods (2) | Wiki: contraband through the Northside docks; stolen corporate cargo warehoused locally. `[wiki]` `[game-data]` |
| Cyberware sales and servicing | `cyberware` | HeavenMed (3); Clean Cut (4) | Wiki: HeavenMed's ripperdoc is "a first-rate cyberware specialist"; Clean Cut is where a Maelstrom patient is treated. Deals with ripperdocs across the city trade cheap parts for discounted service. `[wiki]` |
| Illegal braindance (XBD) | `braindance` | XBD studio (9); Totentanz (1) | Wiki: rumoured XBD production ("Numbness"); the NCPD never proved it, but a Maelstrom-guarded XBD tuning studio exists and the Totentanz sells the gang's custom BDs. `[wiki]` `[game-data]` |
| Nightlife / bar | `food_drink` | Totentanz (1) | Wiki: the club is "the most popular gangster club and drink & riot venue in Night City" and "a significant source of the boostergang's income". `[wiki]` |
| Arms / black-market technology | `arms` | All Foods (2); Maelstrom Warehouse (6); Ebunike Docks (7) | Wiki: traffic in "reclaimed weapons and technology"; heists on corporate transports; the Malorian van theft. `[wiki]` |
| Chop shop / vehicle theft | `vehicles_chop` | Wicked Tires (5) | Gig *Lousy Kleppers*: Malorian Arms van chopped for its transport-route databank. `[wiki]` |
| Protection / extortion | `protection` | Totentanz (1); Little China filler turf | 2020-era "small-time crimes and protection rackets" carried into 2077 turf behaviour; no named 2077 racket is attested, so weight this low. `[wiki]` |
| Contract violence | — | Not location-bound | Wiki: hit jobs "executed in a bizarre and brutal fashion". Deliberately given no location and no revenue code (it is not brokerage; Maelstrom does the work, it does not broker it). `[wiki]` |

### 4.2 Suppliers, customers, rivals

| Role | Party | Detail |
| --- | --- | --- |
| Supplier (product) | Scavengers / Hot Zone salvage | 2040s salvage pipeline; in 2077 the scav/ripperdoc grey market feeds the same chrome trade. `[wiki]` |
| Supplier (cargo to steal) | Malorian Arms, Militech, Arasaka logistics | Heists on "heavily-guarded corporate transports"; the Malorian van on Sir Francis Drake Ave. `[wiki]` |
| Customer | Night City ripperdocs | Cheap reclaimed parts traded for discounted service. `[wiki]` |
| Customer | Night City gangers of every stripe | The Totentanz is open to all gangs "so long as they obeyed Maelstrom's authority and customs". `[wiki]` |
| Customer | Overstimulated BD users | "Numbness" and similar emotional-void XBDs. `[wiki]` |
| Customer | NCPD officers, middlemen | *Scrolls before Swine* has an NCPD sergeant buying Maelstrom CCTV footage — evidence they will deal with anyone. `[wiki]` |
| Rival | Tyger Claws | Kawuki / Little China pressure; 2045 attempt to expand into Old Japantown; Kimen-Gumi formerly secured the Ebunike Docks. `[wiki]` |
| Rival | Scavengers | Compete for the same chrome and salvage; also listed alongside Maelstrom as Northside gangs. `[wiki]` |
| Rival | The Mox | Listed as a Northside gang; conflict is territorial rather than economic. `[wiki]` `[game-data]` |
| Law | NCPD / MAX-TAC | Killed leader Hextra in the 2030s; the gang has been a standing NCPD target since. `[wiki]` |

Maelstrom has **no gambling, no sex work, no fixer brokerage and no real
estate**. Do not model them like the Tyger Claws. The closest analogue in the
shared vocabulary is a scav/smuggler economy: `drugs`, `smuggling`, `cyberware`,
`braindance`, `arms`, with `food_drink` only at the Totentanz.

---

## 5. Headquarters recommendation

### Primary HQ: **Totentanz** — Northside, Watson

Coordinates: club entrance `(-1731.746, 2218.427, 91.111)`; street door
`(-1749.289, 2247.528, 19.413)`. `[game-data]`
`markers.jsonl` `sq011_mp_totentanz_entrance`, `sq011_mp_totentanz_door`.

Rationale:

1. **It is the canon HQ, not an inference.** The wiki's organization infobox
   reads `headquarters = Burleson Tower (2045) / Totentanz's Building (2077)`,
   and the 2077 faction-locations list opens with "Totentanz's Building (HQ)".
   `[wiki]`
2. **It is a real seat with rooms to assign.** A converted unfinished hotel with
   a lobby, elevator bank, 1st floor (z≈23), 3rd-floor club entrance (z≈91), a
   dancefloor, a bar (bartender Dietlinde), bouncer post and back rooms. That is
   a believable org HQ layout for assigning district managers, a vault and a
   holding room.
3. **It maps to the gang's identity and one of its income lines at once.** The
   club is both the "all gangs welcome" neutral ground that makes Maelstrom
   politically powerful and a stated income source. Owning the HQ and owning the
   nightlife economy are the same action.
4. **The marker coverage is exceptional for a place with no site record.**
   Nine distinct `totentanz`/`sq011` markers, three `sq011` community areas with
   a combined 19 Maelstrom entries, and the `Northside_Totentaz` district enum
   (id 108) as an independent existence check. `[game-data]`
5. **The seed already points here.** The nearest control centre,
   `cc_nid_totentanz_yard`, is owned by Maelstrom (`initial_owner_faction_id = 1`)
   and is 155.5 m away — it needs a coordinate correction, not a new point.
6. **14 of 68 Maelstrom spawn points** sit in `nid_totentanz_yard`, the joint
   highest of any sub-territory. `[game-data]`

Trade-off: unlike Clouds, the Totentanz is a single vertical venue rather than a
multi-department office — but that is exactly the "unfinished hotel the gang
keeps standing" fantasy, and it is the only place in the game that the game
itself calls Maelstrom's headquarters.

### Alternate 1: **All Foods Plant** — Northside

Coordinates `(-769.763, 2203.538, 52.384)` `[game-data]` `q003_mp_allfoods_intercom`.

The stronger *building*: a full protein-processing factory with a production
floor, lab, corridors, a makeshift cell block and a street intercom, occupied by
30–40 gangers in lore and 7 Maelstrom in the `q003_factory_combat_main`
community. `[wiki]` `[game-data]` It is described as "the gang's main hideout in
the industrial Watson district", and it is where the leadership coup happened —
so it reads as a seat of power. It loses to the Totentanz only because the wiki
calls Totentanz's Building the HQ and because a factory is a depot, not a place
to hold court.

### Alternate 2: **HeavenMed** — Northside

Coordinates `(-1489.039, 2917.785, 7.240)` `[game-data]` site 411.

Thematically the best small seat for a chrome cult: a two-floor clinic with an
operating room, lockers and a server room, guarded by cameras and Maelstrom
crew, on the payroll rather than merely tolerated. `[wiki]` It loses on size
(one clinic), on revenue mix (one line) and on geography (a waterfront strip far
from the Totentanz/All Foods core), but it is the most defensible 200 m² in the
catalog.

### Overruled / downgraded suggestions

- **Burleson Tower as HQ** — it is the 2045 HQ and the original Totentanz
  location, but it does not exist in the 2077 map. Do not seed it. `[wiki]`
- **Clean Cut as HQ** — best *capture* target in the set (§6), but a forced-labour
  ripperdoc clinic is not a plausible org seat. Keep it as a control point.
- **Ebunike Docks as HQ** — canonically Maelstrom-affiliated, and a moored
  freighter is a great fortress, but it is open docks with no enclosed
  administrative space. Good second-tier point, poor HQ.
- **`cc_nid_totentanz_yard` as-is** — the control centre sits on the *landmark
  centroid* `(-1755.5, 2372.1)`, 155 m north of the actual club. Retarget it onto
  `sq011_mp_totentanz_entrance`, do not add a second point.
- **Bouncing Benny's as a location** — the wiki lists it as a Maelstrom bar in
  Northside, but its infobox has an empty `appears_games` and only
  `appears_books = CEMKKN`. It is an *Edgerunners Mission Kit* location, not a
  2077 asset. No game record exists. `[lore]` `[wiki]`
- **"Factory Hall"** — the wiki's 2077 faction-locations list names it, but the
  page is a redlink and no extract record carries that string. Most likely the
  All Foods production hall (`q003_mp_main_hall`, `-856.355, 2229.063, 55.915`),
  which is already inside catalog #2. Not counted separately; see §8.4.

---

## 6. Priority list of control points

Ranked by how well each place serves as a capturable Maelstrom control point.
"CC" = nearest entry in `data/control_centers.json`; distance is horizontal
metres over all CCs, active or not.

| Rank | Control point | Rel. (1–5) | District / sub-district | Coordinates | Existing CC overlap | Why |
| ---: | --- | :---: | --- | --- | --- | --- |
| 1 | **Totentanz** | 5 | Watson / Northside | `-1731.746, 2218.427, 91.111` | `cc_nid_totentanz_yard`, 155.5 m (owner Maelstrom, inactive) | Canon HQ; club + bar + dancefloor + back rooms; 19 Maelstrom in the `sq011` communities; highest-value single point |
| 2 | **All Foods Plant** | 5 | Watson / Northside | `-769.763, 2203.538, 52.384` | `cc_nid_all_foods_plant`, **22.5 m** (Maelstrom, inactive) | Main hideout; factory with production floor, lab and cell block; 30–40 gangers in lore; cheap retarget of an existing CC |
| 3 | **HeavenMed** | 4 | Watson / Northside | `-1489.039, 2917.785, 7.240` | `cc_nid_pershing_warehouses`, 179.5 m (Maelstrom, inactive) | Two-floor chrome clinic on the payroll; server room; 10-unit community; the gang's `cyberware` economy |
| 4 | **Clean Cut** | 4 | Watson / Northside | `-1158.526, 2419.501, 7.109` | `cc_nid_martin_st_docks`, **3.6 m** (Maelstrom, **active**) | Enclosed clinic with 8 guard areas and a full security system across two site records; nearest CC is 3.6 m and already active — zero new plumbing |
| 5 | **Wicked Tires Autoshop** | 3 | Watson / Northside | `-1347.384, 2767.438, 7.221` | `cc_nid_pershing_warehouses`, 28.9 m (Maelstrom, inactive) | Chop shop: the only `vehicles_chop` site; 8 patrols and 7 doors make it the richest patrol network in the set |
| 6 | **Ebunike Docks** | 3 | Watson / Northside | `-1530.033, 2984.774, 7.305` | `cc_nid_pershing_warehouses`, 257.4 m (Maelstrom, inactive) | Smuggling gateway; 14 Maelstrom at the dock + 3 on the boat; the gang's 2077 logistics story |
| 7 | **Maelstrom Warehouse** (Industrial & Eisenhower) | 3 | Watson / Northside | `-896.700, 2363.300, 53.000` | `cc_nid_all_foods_plant`, 187.8 m (Maelstrom, inactive) | Torture den / evidence stash; two floors with a roof-hatch stealth entry; only 6 guards, so a good low-difficulty capture |
| 8 | **Abandoned Warehouse** (Bennett St) | 2 | Watson / ArasakaWaterfront | `-2152.954, 2876.865, 7.110` | `cc_awf_ebunike_docks`, **3.2 m** (Maelstrom, inactive) | Contraband stash with an underground level; coincides with an existing CC, so it is a rename rather than a new point; coordinate link is `[inferred]` |
| 9 | **Gottfrid & Fredrik's XBD studio** | 2 | Watson / Northside | `-1841.550, 2638.670, 14.890` | `cc_nid_totentanz_yard`, 280.1 m (Maelstrom, inactive) | The only `braindance` production site; 12 Maelstrom guard it; unnamed and hard to reach, so low priority |

### Test control point for the first in-game test: **Clean Cut**

Why Clean Cut and not the HQ or the biggest site:

- **Enclosed, verifiable interior with a set `is_interior = 1` flag** (site 392)
  plus a sister scanner-hustle record (site 219) covering the same building — so
  a capture radius can be validated against real geometry and the dedupe
  assumption gets exercised at the same time.
- **Clean ownership**: both records have `default_faction_id = 1` and
  `initial_owner_faction_id = 1`. No ambiguity about who is evicted — unlike
  `ma_cct_cpz_01` (Maelstrom-occupied, Arasaka-owned sub-territory) or the
  Dockyards, which the wiki disputes.
- **Richest record set in the catalog**: 5 + 3 guard areas (reception, back
  office, reinforcements, melee, restricted movement), 2 + 6 patrols, 3 doors,
  5 devices including `#ma_wat_nid_06_dvc_malestrom_access_point`, two
  `security_area` devices and a security system, 23 + 4 triggers, 60 workspots.
  Every hook a capture/defence prototype needs is present and named.
- **3.6 m from `cc_nid_martin_st_docks`, which is `is_active = 1`** — the only
  active Maelstrom-aligned control centre in the whole set. The test needs no new
  map plumbing and no activation flag.
- **Not the HQ**, so the first capture proves a lore point can be taken without
  touching the seat.
- Fallback if Clean Cut's two overlapping site records cause trouble:
  **Wicked Tires Autoshop** (`sts_wat_nid_06`) — single record, interior,
  `default_faction_id = 1`, 8 patrols, 28.9 m from an inactive Maelstrom CC.

---

## 7. Per-sub-district count of lore-relevant locations

`named` counts distinct named places Maelstrom owns, runs, protects or
habitually occupies — one entry per place, not per quest variant. `filler` is
the deduped occupied-site count minus sites already counted as a named place
(the two tiers from `METHOD.md` §8).

| Sub-district | Named lore-relevant places | Which ones | Maelstrom-occupied sites (deduped, `[game-data]`) | Filler | Noteworthy interiors |
| --- | ---: | --- | ---: | ---: | ---: |
| Northside | **8** | Totentanz, All Foods Plant, HeavenMed, Clean Cut, Wicked Tires Autoshop, Maelstrom Warehouse, Ebunike Docks, Gottfrid & Fredrik's XBD studio | 12 | 7 | 7 (all but Totentanz Industrial Yard and Ebunike open docks) |
| ArasakaWaterfront | **1** | Abandoned Warehouse | 0 | 0 | 1 |
| LittleChina | **0** | turf, executions and shakedowns only | 4 | 4 | 0 |
| Kabuki | **0** | one robbery hold-up only | 1 | 1 | 0 |
| RanchoCoronado | **0** | gang-watch encounters | 2 | 2 | 0 |
| Arroyo | **0** | gang-watch encounter | 1 | 1 | 0 |
| CorpoPlaza | **0** | one 9-unit hold-out at Memorial Ring West | 1 | 1 | 0 |
| **Total** | **9** | | 21 | 16 | 9 |

Filler sites by sub-district:

- **Northside (7)** — `ma_wat_nid_02`, `ma_wat_nid_13`, `ma_wat_nid_14`,
  `ma_wat_nid_15`, `ma_wat_nid_22`, `ma_wat_nid_23`, `ma_wat_nid_03`
- **LittleChina (4)** — `ma_wat_lch_02`, `ma_wat_lch_07`, `ma_wat_lch_12`,
  `ma_wat_lch_15`
- **Kabuki (1)** — `ma_wat_kab_03`
- **RanchoCoronado (2)** — `ma_std_rcr_04`, `ma_std_rcr_17`
- **Arroyo (1)** — `ma_std_rcr_06`
- **CorpoPlaza (1)** — `ma_cct_cpz_01`

Reconciliation: **9 named + 16 filler = 25** = 21 deduped occupied sites + 4
marker-only named places (Totentanz, All Foods Plant, Ebunike Docks, Abandoned
Warehouse). Five of the nine named places are site-backed: 411 HeavenMed, 392
Clean Cut (deduped against 219), 412 Wicked Tires, 413 Maelstrom Warehouse, 410
XBD studio.

**Interpretation for yield.** This is a much flatter faction than the Tyger
Claws: 8 of 9 named places are in one sub-district. Two consequences:

1. Northside should be a high-yield, high-contest district, not a five-way
   split. Consider a reduced per-point yield in Northside and letting the
   Totentanz / All Foods pair carry most of it.
2. Little China and Kabuki have **zero** named places despite real presence
   (13 areas, 15 spawn points, 5 sites). These are raid-and-robbery turf, not
   owned economy. If they need to be capturable, they should be typed as
   "contested block" and excluded from iconic-business multipliers.

If 9 named points is too few for the map, the §3.2 table is the honest filler
pool — but note the tag gap: none of those sites is a business affordance, so
they should never get a business yield multiplier.

---

## 8. Gaps and uncertainties

1. **`sub_territory_id` on a site is a nearest-centroid guess and disagrees
   with the geocode token three times.** `ma_wat_nid_13` is `nid`-tokened at
   `(-1346.8, 2161.4)` but assigned `kab_creek_loop` (Kabuki); `ma_wat_lch_15`
   is `lch`-tokened but assigned `kab_creek_loop`; `ma_std_rcr_06` is
   `rcr`-tokened but assigned an Arroyo sub-territory. Because there are no
   sub-territory polygons in the extract, neither source is provably right. This
   doc uses the geocode token (METHOD §3.3) and flags the three. A polygon dump
   would settle it.
2. **The quest filename token can lie outright.** `sts_wat_kab_02` is a
   `kab_02` file, and its community is literally named `{kab_02_com_ar}`, but it
   sits at `(-1160, 2420)` — Martin Street Depot, Northside — and the gamedata
   enum `Northside_CleanCut` (107) confirms Northside. Token-first attribution
   mis-assigns this whole building to Kabuki. **METHOD §3.3 should add:
   cross-check a site's token against `sub_territory_id`, the gamedata enum, and
   the wiki `sub_district` before trusting it.**
3. **Maelstrom has almost no site records for its two most important places.**
   Totentanz and All Foods Plant are both *marker-only* — no `sites.json` row,
   no community `site_id`, no guard/patrol/device records. Every other faction
   doc that leans on §3.1/§3.5 will be fine; this one had to be rebuilt from
   §3.6 and the `q003`/`sq011` marker families. Worth flagging in the playbook:
   the extract is complete for *street stories* but not for *main-quest
   interiors*.
4. **"Factory Hall" is unresolved.** The wiki's 2077 faction-locations list
   names it; `action=query&titles=Factory Hall` returns `missing`, and no local
   extract record contains the string. Best guess is the All Foods production
   hall (`q003_mp_main_hall`, `-856.355, 2229.063, 55.915`), but I did **not**
   count it as a second named place, because that would double-count catalog #2.
   Confirm in-game before seeding a tenth point.
5. **The Abandoned Warehouse's coordinate link is inferred.** `mq032` is
   *Sacrum Profanum* (location "Cargo Bay / Abandoned Warehouse"), and the only
   Maelstrom marker is `mq032_02_sm_maelstrom` at dock level while the Maelstrom
   community sits at `z = -44`. I read that as the warehouse's lower floor. It
   could equally be the Cargo Bay vendor hub next door (Corpo Snack / Iron &
   Lead / ParaMED). If the interior is wrong, the point is wrong by ~50 m
   vertically.
6. **The seed's `awf_ebunike_docks` sub-territory is not the Ebunike Docks.**
   The seed places "Ebunike Container Docks" at `(-2155.7, 2875.2)` in
   ArasakaWaterfront. The actual Ebunike (Chippin' In, `sq031_03_sm_ebunike`,
   `sq031_ps_ebinike`, `DV Ebunike`) is at `(-1530, 2985)`, ~630 m east and
   firmly in Northside — matching the wiki's `sub_district = Northside` and
   `street = Daniels St.`. The seed anchor instead sits on the Abandoned
   Warehouse / Cargo Bay cluster. One of the two names is wrong. Both are
   Maelstrom-owned, so this is a naming collision, not a loss of territory.
7. **`ma_cct_cpz_01` is Maelstrom-held but Arasaka-owned in the seed.**
   `default_faction_id = 1` but `initial_owner_faction_id = 20`. Nine Maelstrom
   at Memorial Ring West `[game-data]`. Either it is a raid-in-progress
   snapshot, or the site is genuinely Maelstrom-occupied in Arasaka territory.
   Keep as filler and do not grant it business yield.
8. **Area-level presence outside Watson is mostly noise.** The CorpoPlaza (4),
   Coastview (2), CharterHill (2) and Badlands (1) area hits are quest/combat
   communities (`{q115_com_nest_dead_people}`, `{sq025_com_thugs_mean}`,
   `{q301_com_border_community}`, `{q305_com_border_crossing_}002`) that list
   Maelstrom as generic opposition. Only `ma_cct_cpz_01` is a real out-of-Watson
   site. Do not treat the area counts as territory.
9. **No vendor inventory in the extract.** "What each business sells" is always
   `[wiki]` or `[inferred]`. HeavenMed's suitability tags, for instance, are
   `warehouse / vehicle_bay / raid_target` — no `clinic` tag at all, despite it
   demonstrably being a clinic. Suitability tags are combat affordances, not a
   business taxonomy.
10. **Bouncing Benny's is not a 2077 location.** Its infobox has an empty
    `appears_games` and `appears_books = CEMKKN`. No marker, node or area
    matches it. It appears on the wiki's Northside locations list and inflates
    the apparent count of Maelstrom bars; it should not be seeded. `[lore]`
11. **The vanilla per-sub-district gang panel was never dumped.** Evidence (b) in
    §2.2 is `data/districts.json` plus the earlier wiki-derived table, not
    `District_Record.Gangs()`. A TweakDB dump would settle Kabuki and Little
    China exactly.
12. **Interior coverage is sparse.** `is_interior` is set on only 5 of the 22
    Maelstrom candidate sites, yet at least 9 named/near-named places are
    enclosed. Absence of the flag proves nothing; every `interior` value in the
    JSON block is justified from node names, not from the flag.

---

## 9. Sources

- Local: `dist/extract/areas.jsonl`, `dist/extract/markers.jsonl`,
  `data/sites/{sites,communities,rosters,guards,triggers,spots,patrols,devices,suitabilities,meta}.json`,
  `data/{districts,factions,control_centers,sub_territories,landmarks,spawn_points}.json`,
  `refs/RED4ext.SDK/include/RED4ext/Scripting/Natives/Generated/game/data/District.hpp`
  (`Northside_All_Foods = 105`, `Northside_CleanCut = 107`,
  `Northside_Totentaz = 108`).
- Wiki: [Maelstrom](https://cyberpunk.fandom.com/wiki/Maelstrom),
  [Totentanz](https://cyberpunk.fandom.com/wiki/Totentanz),
  [Second Conflict](https://cyberpunk.fandom.com/wiki/Second_Conflict_(quest)),
  [All Foods Plant](https://cyberpunk.fandom.com/wiki/All_Foods_Plant),
  [HeavenMed](https://cyberpunk.fandom.com/wiki/HeavenMed),
  [Gig: Rite of Passage](https://cyberpunk.fandom.com/wiki/Gig:_Rite_of_Passage),
  [Clean Cut](https://cyberpunk.fandom.com/wiki/Clean_Cut),
  [Gig: Hippocratic Oath](https://cyberpunk.fandom.com/wiki/Gig:_Hippocratic_Oath),
  [Gig: Lousy Kleppers](https://cyberpunk.fandom.com/wiki/Gig:_Lousy_Kleppers),
  [Gig: Scrolls before Swine](https://cyberpunk.fandom.com/wiki/Gig:_Scrolls_before_Swine),
  [Gig: Dirty Biz](https://cyberpunk.fandom.com/wiki/Gig:_Dirty_Biz),
  [Ebunike Docks](https://cyberpunk.fandom.com/wiki/Ebunike_Docks),
  [Chippin' In](https://cyberpunk.fandom.com/wiki/Chippin%27_In_(quest)),
  [Sacrum Profanum](https://cyberpunk.fandom.com/wiki/Sacrum_Profanum),
  [Abandoned Warehouse](https://cyberpunk.fandom.com/wiki/Abandoned_Warehouse_(Northside)),
  [Bouncing Benny's](https://cyberpunk.fandom.com/wiki/Bouncing_Benny%27s),
  [Northside](https://cyberpunk.fandom.com/wiki/Northside_(2077)).
- Earlier repo research: `docs/research/factions-gangs-territories.md`
  (§2.2 sub-district gangs, §4.1 Watson table),
  `docs/research/game-data-extraction.md` (`Factions.Maelstrom` records).

---

## 10. Machine-readable block

Strict JSON for seeding (contract in [`METHOD.md`](./METHOD.md) §10). Every
coordinate was re-verified against the local record named in `source` on
2026-11-25; none came from the wiki.

```json
{
  "faction_code": "maelstrom",
  "hq": {"name": "Totentanz", "district": "Watson", "sub_district": "Northside", "x": -1731.746, "y": 2218.427, "z": 91.111, "source": "dist/extract/markers.jsonl sq011_mp_totentanz_entrance", "confidence": "game-data+wiki"},
  "alternate_hqs": [
    {"name": "All Foods Plant", "district": "Watson", "sub_district": "Northside", "x": -769.763, "y": 2203.538, "z": 52.384, "source": "dist/extract/markers.jsonl q003_mp_allfoods_intercom", "confidence": "game-data+wiki"},
    {"name": "HeavenMed", "district": "Watson", "sub_district": "Northside", "x": -1489.039, "y": 2917.785, "z": 7.24, "source": "data/sites/sites.json site 411 sts_wat_nid_05", "confidence": "game-data+wiki"}
  ],
  "test_control_point": {"name": "Clean Cut", "district": "Watson", "sub_district": "Northside", "x": -1158.526, "y": 2419.501, "z": 7.109, "source": "data/sites/sites.json site 392 sts_wat_kab_02", "confidence": "game-data+wiki"},
  "control_points": [
    {"rank": 1, "name": "Totentanz", "type": "club", "relevance": 5, "district": "Watson", "sub_district": "Northside", "x": -1731.746, "y": 2218.427, "z": 91.111, "source": "dist/extract/markers.jsonl sq011_mp_totentanz_entrance", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["food_drink", "drugs", "braindance", "protection"], "nearest_cc_code": "cc_nid_totentanz_yard", "nearest_cc_m": 155.5},
    {"rank": 2, "name": "All Foods Plant", "type": "factory_hideout", "relevance": 5, "district": "Watson", "sub_district": "Northside", "x": -769.763, "y": 2203.538, "z": 52.384, "source": "dist/extract/markers.jsonl q003_mp_allfoods_intercom", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["drugs", "arms", "smuggling"], "nearest_cc_code": "cc_nid_all_foods_plant", "nearest_cc_m": 22.5},
    {"rank": 3, "name": "HeavenMed", "type": "clinic", "relevance": 4, "district": "Watson", "sub_district": "Northside", "x": -1489.039, "y": 2917.785, "z": 7.24, "source": "data/sites/sites.json site 411 sts_wat_nid_05", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["cyberware", "drugs"], "nearest_cc_code": "cc_nid_pershing_warehouses", "nearest_cc_m": 179.5},
    {"rank": 4, "name": "Clean Cut", "type": "clinic", "relevance": 4, "district": "Watson", "sub_district": "Northside", "x": -1158.526, "y": 2419.501, "z": 7.109, "source": "data/sites/sites.json site 392 sts_wat_kab_02", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["cyberware"], "nearest_cc_code": "cc_nid_martin_st_docks", "nearest_cc_m": 3.6},
    {"rank": 5, "name": "Wicked Tires Autoshop", "type": "chop_shop", "relevance": 3, "district": "Watson", "sub_district": "Northside", "x": -1347.384, "y": 2767.438, "z": 7.221, "source": "data/sites/sites.json site 412 sts_wat_nid_06", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["vehicles_chop", "smuggling"], "nearest_cc_code": "cc_nid_pershing_warehouses", "nearest_cc_m": 28.9},
    {"rank": 6, "name": "Ebunike Docks", "type": "docks", "relevance": 3, "district": "Watson", "sub_district": "Northside", "x": -1530.033, "y": 2984.774, "z": 7.305, "source": "dist/extract/markers.jsonl sq031_03_sm_ebunike", "confidence": "game-data+wiki", "interior": false, "revenue_streams": ["smuggling", "arms"], "nearest_cc_code": "cc_nid_pershing_warehouses", "nearest_cc_m": 257.4},
    {"rank": 7, "name": "Maelstrom Warehouse", "type": "warehouse", "relevance": 3, "district": "Watson", "sub_district": "Northside", "x": -896.7, "y": 2363.3, "z": 53.0, "source": "data/sites/guards.json #nid_07_ga_01 (site 413 sts_wat_nid_07)", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["arms", "drugs"], "nearest_cc_code": "cc_nid_all_foods_plant", "nearest_cc_m": 187.8},
    {"rank": 8, "name": "Abandoned Warehouse", "type": "warehouse", "relevance": 2, "district": "Watson", "sub_district": "ArasakaWaterfront", "x": -2152.954, "y": 2876.865, "z": 7.11, "source": "dist/extract/markers.jsonl mq032_02_sm_maelstrom", "confidence": "game-data+wiki+inferred", "interior": true, "revenue_streams": ["smuggling"], "nearest_cc_code": "cc_awf_ebunike_docks", "nearest_cc_m": 3.2},
    {"rank": 9, "name": "Gottfrid & Fredrik's XBD studio", "type": "xbd_studio", "relevance": 2, "district": "Watson", "sub_district": "Northside", "x": -1841.55, "y": 2638.67, "z": 14.89, "source": "dist/extract/markers.jsonl sts_sm_wat_nid_04_gottfrid_fredrik", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["braindance"], "nearest_cc_code": "cc_nid_totentanz_yard", "nearest_cc_m": 280.1}
  ],
  "subdistrict_counts": {
    "Northside": {"named": 8, "filler": 7},
    "ArasakaWaterfront": {"named": 1, "filler": 0},
    "LittleChina": {"named": 0, "filler": 4},
    "Kabuki": {"named": 0, "filler": 1},
    "RanchoCoronado": {"named": 0, "filler": 2},
    "Arroyo": {"named": 0, "filler": 1},
    "CorpoPlaza": {"named": 0, "filler": 1}
  }
}
```
