# Animals — Lore-Relevant Control Points

Status: faction research run, 2026-11-25. One faction, one document.
Scope: turn the current generic ~5-control-centres-per-sub-district grid into
lore-relevant, capturable places for the Animals, with an honest count per
sub-district. Method: this doc conforms to [`METHOD.md`](./METHOD.md), including
its §1.1 corrections. Worked examples: [`tyger-claws.md`](./tyger-claws.md) and
[`maelstrom.md`](./maelstrom.md).

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

The Animals are Night City's **boostergang of the body**: roughly 2,500–3,000
members in 2077, threat level "High", split into small independent **packs** led
by an alpha rather than a single leader. `[wiki]` They reject conventional
cyberware in favour of home-brewed body enchantments — ultra-testosterone,
equine growth hormones and their signature cocktail **"Juice"** — and treat
cage fights, duels and street brawls as both philosophy and recruitment. `[wiki]`

Their economic model is **muscle, fights and growth drugs**:

- **Bodyguarding and bouncer work** — their most sought-after product. Packs hire
  out to brothels, strip clubs, corporations and clubs across the city. `[wiki]`
  In-game this is visible at 7th Hell, Empathy, Data Inc. and the Afterlife.
  `[wiki]` `[game-data]`
- **Illegal fights** — underground bouts, cage fights and fight clubs, with
  betting and entry fees. The Tripple Extreme Gym's paint-vat pit and the Grand
  Imperial Mall's boxing ring are the two canonical venues. `[wiki]`
- **Drugs** — custom-brewed anabolic steroids and Juice; some packs specialise
  in raiding drug stores, chemical transports and pharmaceutical companies for
  ingredients. `[wiki]`
- **Racketeering** — extortion and assault on local businesses. `[wiki]`
- **Raids and transport hijacking** — ultraviolent raids on residential
  districts, rival turf and cargo transports. `[wiki]`

The wiki organisation infobox says `headquarters = N/A` and lists three 2077
faction locations: **Tripple Extreme Gym**, **Unfinished NCART Station** and
**Grand Imperial Mall**. `[wiki]` That is the honest shape of this faction: no
contiguous turf, but a set of strong individual businesses and dens. In the
extract the weight is **Coastview (17 community areas, 16 dominant)** — the
Grand Imperial Mall alone contributes 55 Animals entries across six `q110`
communities — with secondary clusters in **Downtown (9)**, **West Wind Estate
(4)** and **Wellsprings (3)**. `[game-data]`

Pacifica is the only district whose vanilla gang panel lists the Animals
(`data/districts.json`: `vanilla_gangs = ["VoodooBoys","Animals"]`), which
matches the wiki's "west Pacifica" framing. `[game-data]` `[wiki]`

---

## 2. Territory

### 2.1 Districts

| Evidence kind | Result |
| --- | --- |
| (a) Wiki/lore | "An aggressive street-fighting gang from west Pacifica"; no defined territory; 2077 faction locations are Tripple Extreme Gym, Unfinished NCART Station and Grand Imperial Mall; HQ listed as N/A. `[wiki]` |
| (b) Vanilla map gang panel | `data/districts.json`: Pacifica `vanilla_gangs = ["VoodooBoys","Animals"]`. No other district lists Animals. `[game-data]` |
| (c) Game-data counts | 45 community areas contain Animals spawns (43 dominant); 14 candidate roster sites, 14 after 25 m dedupe; 97 roster units; 43 entries in `data/spawn_points.json` with `faction_id == 6`; 4 seeded sub-territories. `[game-data]` |

The seed gives the Animals four sub-territories. Only one is a genuine lore
place; the other three are grid anchors:

| `sub_territory_id` | Code | Sub-district | Landmark | Animals spawns | Verdict |
| ---: | --- | --- | --- | ---: | --- |
| 46 | `spr_pump_station` | Wellsprings | Wellsprings Pump Station | 1 | The `Living the Big Life` Juice den sits on the anchor (§3, #7) |
| 61 | `cvi_grand_imperial_mall` | Coastview | Grand Imperial Mall | 8 | Correct; HQ (§5) |
| 63 | `cvi_east_overpass` | Coastview | Coastview East Overpass | 4 | Two Animals scanner-hustle sites nearby (§3.2) |
| 70 | `wwd_highway_gate` | WestWindEstate | West Wind South Highway | 0 | Seed-only anchor; no site, marker or wiki identity (§8.15) |

`[game-data]`

### 2.2 Sub-district presence

Counts are from `dist/extract/areas.jsonl` (`animals` in `faction_counts`;
"dominant" = `dominant_faction == animals`), `data/spawn_points.json`
(`faction_id == 6`), and the deduped site set in §2.3. Sub-districts were
re-attributed by geocode token, then nearest geocoded site, then nearest
sub-territory centroid (§2.4).

| Sub-district | District | (a) Lore | (b) Vanilla panel | (c) Areas (dominant) | (c) Spawn pts | Animals-occupied sites* |
| --- | --- | --- | --- | ---: | ---: | ---: |
| Coastview | Pacifica | GIM base; west Pacifica | Pacifica: VDB + Animals | 17 (16) | 14 | 3 |
| Downtown | CityCenter | Two Animals-run clubs | — (corp district) | 9 (9) | 6 | 3 |
| WestWindEstate | Pacifica | NCART den (wiki) | Pacifica: VDB + Animals | 4 (4) | 2 | 1 |
| Wellsprings | Heywood | Juice den + Data Inc. | Valentinos | 3 (3) | 3 | 2 |
| Kabuki | Watson | Presence only | Tyger Claws (+Maelstrom, Mox) | 3 (3) | 3 | 0 |
| JapanTown | Westbrook | Bouncer/assault presence | Tyger Claws | 2 (1) | 1 | 1 |
| LittleChina | Watson | Market shakedown | Tyger Claws | 2 (2) | 2 | 1 |
| CharterHill | Westbrook | Quest club scene | Tyger Claws (+6th Street) | 2 (2) | 2 | 0 |
| Arroyo | SantoDomingo | Tripple gym | 6th Street | 1 (1) | 2 | 1 |
| CorpoPlaza | CityCenter | Organ-harvesting hustle | — (corp district) | 1 (1) | 3 | 1 |
| Dogtown | Pacifica | Minor PL presence | Barghest | 1 (1) | 3 | 0 |
| RanchoCoronado | SantoDomingo | Mini-world-story only | 6th Street | 0 (0) | 1 | 1 |

\* Deduped `data/sites/sites.json` rows with `default_faction_id == 6` **or** at
least one roster entry resolving to Animals. No site variants collapsed. Site
sub-district is taken from the geocode token plus the placement prefab path,
with the conflicts in §8.2–§8.4 called out.

**Reading the counts.** "Areas" measure presence, not owned economy. Several
Animals hits are quest combat communities where the gang is opposition, not
proprietor: `{sq012_com_rqr_club_ug}` (8 Animals at a Charter Hill club scene,
`sq012` has no resolvable wiki page), `{mq028_com_stalker_park}` (5, Kabuki),
`{sa_ep1_113_com_combat}` (5, Coastview) and `{spr_06_animals_com}` (4, Data
Inc. combat). `[game-data]` The counts that matter for yield are in §7.

### 2.3 Candidate sites and dedupe

14 candidate sites → **14 after 25 m dedupe**. No site is a quest variant of
another; the six named sites are all distinct buildings.

| Site | Units | Interior | Sub-district | Coordinates | What it is |
| --- | ---: | :---: | --- | --- | --- |
| `sts_pac_cvi_02` | 13 | no flag (interior by nodes) | Coastview | `-2441.8, -2565.5, -0.7` | Unfinished NCART Station — catalog #3 |
| `sts_cct_dtn_03` | 11 | no flag (interior by nodes) | Downtown | `-1629.8, 385.8, 8.1` | Empathy — catalog #5 |
| `ma_hey_spr_11` | 10 | no | Wellsprings | `-2039.6, -1301.4, 7.3` | Skyline South Juice den — catalog #7 |
| `ma_pac_cvi_11` | 9 | no | Coastview | `-1128.5, -1790.1, 44.1` | Coastal scanner hustle — filler |
| `sts_cct_dtn_02` | 9 | no flag (interior by nodes) | Downtown | `-1927.0, -42.8, 3.5` | 7th Hell — catalog #4 |
| `sts_pac_wwd_05` | 9 | **yes** | Arroyo | `-501.0, -1924.9, 8.0` | Tripple Extreme Gym — catalog #2 |
| `ma_cct_dtn_01` | 8 | no | Downtown | `-1727.0, 492.3, 7.5` | Gang-watch hustle — filler |
| `ma_pac_cvi_05` | 7 | no | Coastview | `-1216.0, -1715.3, 44.3` | Execution/gang-watch — filler |
| `ma_wbr_jpn_19` | 5 | no | JapanTown | `-567.9, 1496.7, 37.2` | *Assault in Progress, Salinas St.* — filler |
| `ma_cct_cpz_17` | 4 | no | CorpoPlaza | `-1374.6, 617.3, 4.4` | Organ-harvesting / street-violence hustle — filler |
| `ma_pac_wwd_01` | 4 | no | WestWindEstate | `-2798.2, -2376.8, 8.4` | Gang-watch hustle (Keenan/Sheila/Nina) — filler |
| `sts_hey_spr_06` | 4 | no flag (interior by nodes) | Wellsprings | `-2255.0, -405.1, 7.4` | Data Inc. store — catalog #6 |
| `ma_wat_lch_04` | 3 | no | LittleChina | `-1285.0, 1436.6, 21.0` | *Assault in Progress* market shakedown — filler |
| `mws_arr_07` | 1 | no | RanchoCoronado | `523.7, -2309.0, 125.1` | Mini-world-story rooftop — filler |

`[game-data]` for every row.

---

## 3. Location catalog

World-space metres, `Z` up. "Interior?" means the game has a distinct interior
cell/sector, even where `is_interior` is unset (it is set on only one of the six
site-backed points).

| # | Name | Type | District / sub-district | Interior? | Business? (what it earns) | Coordinates (x, y, z) | Coordinate source record | Linked communities / sites | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **Grand Imperial Mall** (HQ) | Unfinished mallplex — gym, boxing ring, arena, garage | Pacifica / Coastview | Yes — mall gym floor, ring, arena, maintenance, garage | Yes: NetWatch security contract, fight betting/boxing, bar/food, mall as a base | `-2363.001, -2026.324, 15.811` (mall ring); `-2368.139, -2027.300, 14.000` (gym floor); `-2228.524, -2241.808, 11.737` (mall intro) | `markers.jsonl` `mq025_mp_08_ring`, `q110_sm_ow_fluff_gym`, `q110_06_sm_the_mall_intro` | `{q110_com_mall_hall}` (22 Animals), `{q110_com_mall_gym}` (10), `{q110_com_mall_garage}` (8), `{q110_com_mall_mainentrance_reinforcements}` (6); enum `Coastview_GrandImperialMall` (37) | `[game-data]` `[wiki]` |
| 2 | **Tripple Extreme Gym** (Tripple Xtreme Epic Workout Center) | Former paint factory / Animals fight club | SantoDomingo / Arroyo | Yes — boxing pit in the old mixing vat, ground floor, 2nd-floor office/infirmary, roof | Yes: illegal fights + betting, €$3,800 gate fee, melee-weapon vendor, fight "tourism" | `-500.969, -1924.883, 7.987` (site anchor); `-494.634, -1931.069, 8.530` (fight-club marker) | `data/sites/sites.json` site 378 `sts_pac_wwd_05`; `markers.jsonl` `mq025_mp_07_fight_club`; placement prefab `#c_santo_domingo/arroyo/loc_sts_pac_wwd_05_paint_factory` | `{wwd_05_com_enemies}` (9 Animals); guards `#wwd_05_restricted_movement_01/02`; 6 patrols; 5 doors; roster `Character.wwd_05_enemy_*` | `[game-data]` `[wiki]` |
| 3 | **Unfinished NCART Station** | Abandoned metro station / Animals den | Pacifica / Coastview | Yes — lower/upper/top floors, metro tunnels | Yes: drug stash (stolen lidocaine for Juice), contraband van staging, hideout | `-2441.771, -2565.546, -0.681` | `data/sites/sites.json` site 377 `sts_pac_cvi_02`; placement prefab `c_pacifica/coastview/loc_sts_pac_cvi_02` | `{cvi_02_combat_com}` (13 Animals); guards `#cvi_02_rm_lower_floor_*`, `#cvi_02_rm_upper_floor`, `#cvi_02_rm_top_floor_001`; triggers `#cvi_02_tr_metro*`, `#cvi_02_tr_van`, `#cvi_02_tr_truck`; roster `Character.sts_pac_cvi_02_animals_*` | `[game-data]` `[wiki]` |
| 4 | **7th Hell** | Nightclub | CityCenter / Downtown | Yes — 1st floor lounge/dancefloor/bar, 2nd floor VIP/security, basement | Yes: Animals door security and VIP bouncers, bar takings, €$500 entry; owner Jack Mausser | `-1927.012, -42.783, 3.466` | `data/sites/sites.json` site 351 `sts_cct_dtn_02` | `{dtn_02_combat_com}` (9 Animals); guards `#dtn_02_ga_*` (incl. `red_thunder`); spots `#dtn_02_ws_bouncer_*`, `#dtn_02_ws_angry_guest_*`; triggers `#dtn_02_tr_bouncer_*`, `#dtn_02_tr_camera_room`; roster `Character.sts_cct_dtn_02_bouncer_*`, `_officer` | `[game-data]` `[wiki]` |
| 5 | **Empathy** | Braindance strip club | CityCenter / Downtown | Yes — reception, dancefloor, 2nd-floor VIP, control room, backstage | Yes: porn BDs, live striptease, bars; Animals bouncers installed after Adam Ibrahimovic's takeover | `-1629.752, 385.799, 8.093` | `data/sites/sites.json` site 352 `sts_cct_dtn_03` | `{dtn_03_combat_com}` (10 Animals); triggers `#dtn_03_tr_bar`, `#dtn_03_tr_backstage_patrol`, `#dtn_03_tr_cctv_room`, `#dtn_03_tr_server_room_doors`; roster `Character.sts_cct_dtn_03_bouncer_*`, `_officer` | `[game-data]` `[wiki]` |
| 6 | **Data Inc. (Wellsprings)** | Electronics store fronting stolen Militech hardware | Heywood / Wellsprings | Yes — storefront, back counter/garage, basement netrunning den | Yes: hacked/stolen Militech weapons sold at markup; Animals pose as staff; netrunning den downstairs | `-2254.987, -405.114, 7.390` | `data/sites/sites.json` site 376 `sts_hey_spr_06`; placement prefab `#c_heywood/wellsprings/loc_sts_hey_spr_06` | `{spr_06_animals_com}` (4 Animals); guards `#spr_06_guard_area`, `#sts_hey_spr_06_basement`, `#sts_hey_spr_06_mainhall`; spots `#spr_06_ws_enemy_vendor_*`; roster `Character.sts_hey_spr_06_animals*`, `_officer` | `[game-data]` `[wiki]` |
| 7 | **Skyline South Juice den** (seed label: Wellsprings Pump Station) | Juice/steroid distribution den and outpost | Heywood / Wellsprings | No — open pump-station yard and outpost | Yes: Juice/illegal-supplement trafficking, led by Denzel Cryer and Jesse Sabara | `-2039.627, -1301.386, 7.292` | `data/sites/sites.json` site 90 `ma_hey_spr_11` | `{ma_hey_spr_11_com}` (10 Animals, z 7.3); guards `#ma_hey_spr_11_ga*`; 5 patrols; roster `Character.spr_animals_*`, `Character.ma_hey_spr_11_outpost_miniboss` | `[game-data]` `[wiki]` |

### 3.1 How the name→coordinate links were proven

Wiki `baseid` is the strongest lever for this faction. Four of the six
site-backed named places are an exact `baseid` match to a gig, and the fifth
(Data Inc.) is confirmed by the placement prefab and interior nodes:

- `sts_pac_wwd_05` → **Gig: For My Son** (`baseid = sts_pac_wwd_05`), whose
  infobox location is "Old Paint Factory on Baptiste St." and whose journal calls
  it "an Animals fight club". The raw sector path is
  `#c_santo_domingo/arroyo/loc_sts_pac_wwd_05_paint_factory_prefab…`, and beat
  markers `mq025_mp_07_fight_club` / `sq025_07_sm_rhino_animation` sit on the
  anchor. That makes it the **Tripple Extreme Gym**. `[wiki]` `[game-data]`
- `sts_pac_cvi_02` → **Gig: Two Wrongs Makes Us Right** (`baseid =
  sts_pac_cvi_02`). The gig journal describes "an Animal den", a van of stolen
  lidocaine in the NCART tunnels, and the wiki location page names the
  **Unfinished NCART Station**. Site 377's triggers include `#cvi_02_tr_metro*`,
  `#cvi_02_tr_van` and `#cvi_02_tr_truck`, and its guard areas are named
  `rm_lower_floor_*`, `rm_upper_floor`, `rm_top_floor_001`. `[wiki]` `[game-data]`
- `sts_cct_dtn_02` → **Gig: An Inconvenient Killer** (`baseid =
  sts_cct_dtn_02`), location **7th Hell**, "corner of Corporation St. and
  Ringroad West". Interior nodes `#dtn_02_ws_bouncer_*`,
  `#dtn_02_tr_camera_room`, `#dtn_02_ws_angry_guest_*` and 5 guard areas
  (`enemies_001/002/003`, `outside`, `red_thunder`) match a two-floor club with
  door security. `[wiki]` `[game-data]`
- `sts_cct_dtn_03` → **Gig: A Lack of Empathy** (`baseid = sts_cct_dtn_03`),
  location **Empathy**, the Animals-run braindance strip club. Nodes
  `#dtn_03_tr_bar`, `#dtn_03_tr_backstage_patrol`, `#dtn_03_tr_cctv_room`,
  `#dtn_03_tr_server_room_doors`, `#dtn_03_private_door` and 9 doors match the
  wiki layout (reception, dancefloor, VIP, control room, fire escape).
  `[wiki]` `[game-data]`
- `sts_hey_spr_06` → **Gig: Hot Merchandise** (`baseid = sts_hey_spr_06`),
  location **Data Inc. Store** in Wellsprings. The prefab path is
  `#c_heywood/wellsprings/loc_sts_hey_spr_06_prefab…`; nodes
  `#sts_hey_spr_06_basement`, `#sts_hey_spr_06_mainhall`,
  `#spr_06_ws_enemy_vendor_*` and a `#spr_06_dvc_solo_shutter` match a store with
  a back-room/basement operation. `[wiki]` `[game-data]`
- `ma_hey_spr_11` → **Suspected Organized Crime Activity: Living the Big Life**
  (`baseid = ma_hey_spr_11`), an NCPD scanner hustle against Denzel Cryer ("The
  Brain") and Jesse Sabara's Juice-trafficking pack. The community
  `{ma_hey_spr_11_com}` holds 10 Animals at the site anchor. `[wiki]` `[game-data]`
- **Grand Imperial Mall** has **no `sites.json` row** and no roster. Its identity
  rests on a dense `q110`/`mq025` marker family — `q110_06_sm_the_mall_intro`,
  `q110_mp_mall_back_entrance`, `q110_mp_mall_exit`, `q110_mp_mall_garage_entrance`,
  `q110_sm_ow_fluff_gym`, `q110_mp_gym_corridor`, `q110_08c_sm_bossfight`,
  `q110_08d_sm_animals_stand_down`, `sasquatch_perf_spn`, `mq025_mp_08_ring`,
  `mq025_08_sm_finale` — plus six `q110_com_mall_*` communities holding 55
  Animals entries, and the `Coastview_GrandImperialMall` district enum (id 37).
  `[game-data]` `[wiki]`

Two coordinate cautions learned here:

- **The site `code` token can name an asset's origin, not its placement.**
  `sts_pac_wwd_05` is a `pac_wwd` (Pacifica / West Wind) filename, but the
  placement prefab is `#c_santo_domingo/arroyo/loc_sts_pac_wwd_05_paint_factory`,
  and the site sits at `(-501, -1925)` — Santo Domingo, not Pacifica. The wiki's
  "Rancho Coronado" infobox is a third, conflicting label (§8.2).
- **`sub_territory_id` is a nearest-centroid guess and is wrong on four of these
  six sites.** `sts_hey_spr_06` is assigned `arr_arasaka_industrial` (Arroyo) but
  its prefab and token are Wellsprings; `ma_wbr_jpn_19` is assigned
  `hil_gold_beach` (Charter Hill) but is JapanTown; `sts_cct_dtn_02` is assigned
  `cpz_ring_road_west` but is a Downtown club; `sts_pac_cvi_02` is assigned
  `dt_longshore_stacks` (Dogtown) but its placement is Coastview. Use the token
  plus the placement prefab, never `sub_territory_id` alone (§8.4).

### 3.2 Animals-occupied generic sites (the filler pool)

`data/sites/suitabilities.json` tags. Unlike the Maelstrom pool, this one is not
all `raid_target`: the named club sites carry `club` and `arms_cache`, which is a
useful independent hint that these are entertainment/weapons premises.

| Site | Sub-district | Interior | Suitability tags | Units | Coordinates | Note |
| --- | --- | :---: | --- | ---: | --- | --- |
| `ma_pac_cvi_11` | Coastview | no | raid_target, rooftop_access | 9 | `-1128.5, -1790.1, 44.1` | Coastal scanner hustle; largest filler garrison |
| `ma_cct_dtn_01` | Downtown | no | camera_net, raid_target, stealth_entry | 8 | `-1727.0, 492.3, 7.5` | Gang-watch hustle (John Lipczynsky) |
| `ma_pac_cvi_05` | Coastview | no | hostage_site, raid_target, rooftop_access | 7 | `-1216.0, -1715.3, 44.3` | Execution / gang-watch scene |
| `ma_wbr_jpn_19` | JapanTown | no | club, hostage_site, raid_target, rooftop_access | 5 | `-567.9, 1496.7, 37.2` | *Assault in Progress, Salinas St.* (Adam Giles) |
| `ma_cct_cpz_17` | CorpoPlaza | no | branch_office, hostage_site, raid_target | 4 | `-1374.6, 617.3, 4.4` | Organ-harvesting / street-violence hustle |
| `ma_pac_wwd_01` | WestWindEstate | no | arms_cache, hostage_site, raid_target, rooftop_access | 4 | `-2798.2, -2376.8, 8.4` | Gang-watch hustle with named Animals (Keenan, Sheila, Nina) |
| `ma_wat_lch_04` | LittleChina | no | arms_cache, club, hostage_site, market_stall, raid_target, rooftop_access, vehicle_bay | 3 | `-1285.0, 1436.6, 21.0` | *Assault in Progress* — market-vendor shakedown |
| `mws_arr_07` | RanchoCoronado | no | rooftop_access | 1 | `523.7, -2309.0, 125.1` | Mini-world-story rooftop; token says `arr`, position says Rancho (§8.4) |

Treat the tags as gameplay affordances, not lore. They say a place *can* host a
raid or a stash; they do not prove a business.

---

## 4. Economic structure

### 4.1 Revenue streams → catalog locations

Codes are from [`METHOD.md`](./METHOD.md) §7.

| Revenue stream | Code(s) | Catalog locations that produce it | Evidence / notes |
| --- | --- | --- | --- |
| Bodyguarding / bouncer work (core product) | `security_services`, `protection` | Grand Imperial Mall (1); 7th Hell (4); Empathy (5); Data Inc. (6); **Afterlife** (not seeded — Emmerick Bronson is its bouncer) | Wiki: Animals sell themselves as bouncers and bodyguards to "brothels, strip clubs, corporations"; the database entry calls them "ideal security guards and bouncers for clubs and bars". `[wiki]` GIM is a paid NetWatch contract, hence `security_services`; club doors are protection work. `[wiki]` `[game-data]` |
| Illegal fights, betting, entry fees | `gambling` | Tripple Extreme Gym (2); Grand Imperial Mall boxing ring (1) | Tripple: paint-vat pit, Rhino's *Beat on the Brat* fight, €$3,800 gate fee. GIM: Razor Hugh title fight in the mall ring. `[wiki]` `[game-data]` |
| Growth drugs / Juice / steroids | `drugs` | Skyline South Juice den (7); Unfinished NCART Station (3) | Wiki: custom-brew anabolic steroids are a main line; "Juice" is the gang's own hormone cocktail. `Living the Big Life` is a Juice-trafficking den; `Two Wrongs` stashes lidocaine for the cocktail. `[wiki]` `[game-data]` |
| Arms / stolen hardware | `arms`, `retail` | Data Inc. (6) | Gig *Hot Merchandise*: a store selling hacked, previously stolen Militech equipment at a markup, staffed by Animals posing as legitimate businessmen. `[wiki]` |
| Nightlife / bar | `food_drink` | 7th Hell (4); Empathy (5); Grand Imperial Mall (1); Tripple vendor (2) | Club bars and the mall's food/service floors. `[wiki]` `[game-data]` |
| Braindance / sex work | `braindance`, `sex_work` | Empathy (5) | Empathy specialises in hardcore porn BDs and live striptease; the Animals are its installed security, not its owners. `[wiki]` |
| Racketeering / extortion | `protection` | Club doors (4, 5); Little China market shakedown (filler `ma_wat_lch_04`); Wellsprings/Coastview turf | Wiki: "some were even racketeers who specialized in extortion and assault." `[wiki]` |
| Contract violence, raids, transport hijacking | `mercenary` (prose only — see §8.14) | Not location-bound | Wiki: ultraviolent raids on residential districts and rival turf; transport hijacking. Deliberately not attached to a single building. `[wiki]` |
| Contraband staging | `smuggling` | Unfinished NCART Station (3) | The gig's van of stolen medical stimulants is staged in the NCART tunnels. `[wiki]` |

### 4.2 Suppliers, customers, rivals

| Role | Party | Detail |
| --- | --- | --- |
| Client (security contract) | NetWatch | Hired Sasquatch's pack to guard the GIM and hide NetWatch's presence from intruders during *I Walk the Line*. `[wiki]` |
| Client (door security) | 7th Hell (Jack Mausser), Empathy (Adam Ibrahimovic), Data Inc. | Club and store owners who hire Animals as bouncers/staff. `[wiki]` |
| Supplier (drug inputs) | Maelstrom, pharma/chemical transports, drug stores | The *Two Wrongs* lidocaine was "stolen already once before from Maelstrom"; packs raid drug stores and chemical transports for Juice ingredients. `[wiki]` |
| Supplier (guns) | Militech (stolen) | Data Inc. sells hacked/stolen Militech equipment; Rogue's concern is that it will draw a corporate crackdown. `[wiki]` |
| Customer | Fight spectators and bettors | Tripple Extreme Gym and the GIM ring. `[wiki]` |
| Customer | Juice users, bodybuilders, ripperdocs | Mr. Hands' plan resells the stolen lidocaine to ripperdocs "at market price". `[wiki]` |
| Customer | Clubs, brothels, strip clubs, corporations | The bodyguard market itself. `[wiki]` |
| Rival | Voodoo Boys | Pacifica overlords; the GIM is contested ground and the VDB chapel sits in Coastview. `[wiki]` `[game-data]` |
| Rival | Scavengers | Move into the GIM after the Animals leave; operate across Coastview. `[wiki]` `[game-data]` |
| Rival | Barghest | Dogtown; Eden Plaza / Golden Pacific list Animals only as a minor presence. `[wiki]` |
| Rival | Valentinos | Wellsprings turf; Data Inc. and the Juice den sit inside Valentino-flagged sub-territories. `[game-data]` |
| Rival | Tyger Claws | Jig-Jig Street lists Animals among its gangs; Tyger turf in JapanTown/Kabuki. `[wiki]` |
| Rival | 6th Street | Arroyo / Rancho Coronado turf around the Tripple gym. `[game-data]` |
| Law | NCPD | The Juice den is an NCPD organized-crime scanner hustle. `[wiki]` |

The Animals have **no gambling empire, no dollhouses and no fixer brokerage** in
the Tyger Claws sense. The closest model is a security-and-fight economy:
`security_services`, `protection`, `gambling`, `drugs`, `arms`/`retail`, plus
`food_drink`/`braindance`/`sex_work` only where they guard someone else's venue.

---

## 5. Headquarters recommendation

### Primary HQ: **Grand Imperial Mall** — Coastview, Pacifica

Coordinates: mall gym ring `(-2363.001, -2026.324, 15.811)`; gym floor
`(-2368.139, -2027.300, 14.000)`. `[game-data]`
`markers.jsonl` `mq025_mp_08_ring`, `q110_sm_ow_fluff_gym`.

Rationale:

1. **The seed already treats it as Animals turf.** `sub_territories.json` gives
   `cvi_grand_imperial_mall` (id 61) to faction 6, and the matching control
   centre `cc_cvi_grand_imperial_mall` is **35.1 m** from the ring. Retarget the
   CC; do not invent a new point. `[game-data]`
2. **It is the canon 2077 base of Sasquatch's pack.** The wiki says Matilda K.
   Rose's group settled in the GIM as private security for NetWatch agent Bryce
   Mosley during *I Walk the Line*; her page records her place of death as the
   GIM. `[wiki]`
3. **It is a real seat with rooms to assign.** An unfinished six-floor mall with
   a gym, boxing ring, arena, maintenance corridors, garage and multiple mall
   halls — enough distinct spaces for a vault, a holding room, a vendor floor and
   district managers. `[wiki]` `[game-data]`
4. **It is the densest Animals concentration in the game.** Six `q110_com_mall_*`
   communities hold 55 Animals entries (hall 22, gym 10, garage 8, main-entrance
   reinforcements 6, after-van 5, frontal assault 4), and
   `cvi_grand_imperial_mall` has 8 of the faction's 43 spawn points. `[game-data]`
5. **It unifies both identity lines.** The gym/ring is the fight economy; the
   NetWatch contract is the bodyguard economy; the mall's "ANIMAL" sign is the
   gang's own branding. `[wiki]`
6. **It is marker-rich enough to anchor without a site row.** Twenty-plus
   `q110`/`mq025` markers name the intro, gym, ring, arena, garage, exits,
   Sasquatch spawn and bossfight. `[game-data]`

Trade-off: the wiki calls the Animals' tenure "formerly" and says Scavengers
later stripped the mall, and `headquarters = N/A` is explicit. The GIM is a
*hired base*, not a hereditary seat. It still wins because the mod's seed already
grants it, because it is where the gang's leader is fought, and because no other
Animals property has the scale.

### Alternate 1: **Tripple Extreme Gym** — Arroyo, Santo Domingo

Coordinates `(-500.969, -1924.883, 7.987)` `[game-data]` site 378.

The strongest *owned* property: a former SovOil paint factory converted into a
gym and fight club, owned by the Animal Logan Garcia, with a boxing pit in the
old mixing vat, a 2nd-floor office and infirmary, a melee-weapon vendor and a
rooftop. It is the setting of *Gig: For My Son* and *Beat on the Brat: Rancho
Coronado*, and the only site with `is_interior = 1`. It loses to the GIM only on
scale (one building) and geography (an industrial edge of Santo Domingo, not
Pacifica).

### Alternate 2: **7th Hell** — Downtown, City Center

Coordinates `(-1927.012, -42.783, 3.466)` `[game-data]` site 351.

The best *club seat*: two floors plus a basement, VIP area, security rooms,
camera room and a guarded service elevator, with 9 Animals bouncers. It is a
believable place to run a protection racket from. It loses because the club is
owned by Jack Mausser and the Animals are merely its security contractor —
ownership, not presence.

### Overruled / downgraded suggestions

- **Unfinished NCART Station as HQ** — 13 Animals make it the largest single
  garrison, but it is a tunnel den, not an administrative seat. Keep it as a
  high-value control point.
- **Empathy as HQ** — a braindance strip club is a revenue node and a good
  control point, but the Animals are installed security, not owners.
- **The Afterlife as a control point** — Emmerick Bronson (Animal) is its
  bouncer, but the bar is Rogue Amendiares' merc hub. Presence, not ownership;
  do not seed. It belongs in the bodyguard-economy prose only.
- **Eden Plaza / Golden Pacific as Dogtown points** — both wiki infoboxes list
  Animals, but both are BARGHEST-dominated Dogtown locations with no Animals
  roster site or marker. Presence noise; do not seed. `[wiki]` `[game-data]`
- **Jig-Jig Street** — lists Animals among four gangs, but it is Tyger Claws
  turf and a Mox battleground. Not an Animals place.
- **Wellsprings Pump Station as a separate named place** — the seed label is a
  generic grid name; the real point there is the *Living the Big Life* Juice den
  (catalog #7), so count it once, not twice.
- **`cc_cvi_grand_imperial_mall` as-is** — the control centre sits on the mall
  landmark centroid, 35 m from the ring. Retarget it onto the ring; do not add a
  second mall point.

---

## 6. Priority list of control points

Ranked by how well each place serves as a capturable Animals control point.
"CC" = nearest entry in `data/control_centers.json`; distance is horizontal
metres over all CCs, active or not. Owner is the CC's sub-territory
`initial_owner_faction_id`, per METHOD §1.1 item 10.

| Rank | Control point | Rel. (1–5) | District / sub-district | Coordinates | Existing CC overlap | Why |
| ---: | --- | :---: | --- | --- | --- | --- |
| 1 | **Grand Imperial Mall** | 5 | Pacifica / Coastview | `-2363.001, -2026.324, 15.811` | `cc_cvi_grand_imperial_mall`, **35.1 m** (owner Animals, inactive) | HQ; Sasquatch's base; 55 Animals in the mall communities; gym + ring + arena; NetWatch contract |
| 2 | **Tripple Extreme Gym** | 5 | SantoDomingo / Arroyo | `-500.969, -1924.883, 7.987` | `cc_arr_arasaka_industrial`, 372.2 m (owner Arasaka, inactive) | Only Animals-owned freehold with a named owner; fight club + vendor + office; interior; 9 units |
| 3 | **Unfinished NCART Station** | 4 | Pacifica / Coastview | `-2441.771, -2565.546, -0.681` | `cc_dt_longshore_stacks`, 123.9 m (owner Barghest, inactive) | Largest garrison (13); Juice/contraband stash; metro-tunnel interior; gig identity |
| 4 | **7th Hell** | 4 | CityCenter / Downtown | `-1927.012, -42.783, 3.466` | `cc_spr_boardwalk_north`, 193.8 m (owner Valentino, inactive) | Two-floor nightclub with VIP/security rooms and 9 bouncers; protection economy |
| 5 | **Empathy** | 4 | CityCenter / Downtown | `-1629.752, 385.799, 8.093` | `cc_dtn_corporation_st`, 142.1 m (owner Tyger, inactive) | BD strip club with 11 Animals, 9 doors and a control room; braindance + sex-work revenue |
| 6 | **Skyline South Juice den** | 3 | Heywood / Wellsprings | `-2039.627, -1301.386, 7.292` | `cc_spr_pump_station`, **11.2 m** (owner Animals, inactive) | Cleanest ownership in the set (`default` and `initial` both 6); 10 units and two named pack leaders; the gang's signature drug |
| 7 | **Data Inc. (Wellsprings)** | 3 | Heywood / Wellsprings | `-2254.987, -405.114, 7.390` | `cc_spr_berkeley_bay`, 225.3 m (owner Valentino, inactive) | Stolen-Militech storefront with a basement netrunning den; arms revenue; only 4 garrison units |

### Test control point for the first in-game test: **Tripple Extreme Gym**

Why the gym and not the HQ or the biggest garrison:

- **Enclosed interior with the `is_interior = 1` flag set** (site 378) — the only
  Animals site where the flag is present. A capture radius can be validated
  against real geometry rather than inferred from node names.
- **Identity is exact.** `baseid = sts_pac_wwd_05` matches *Gig: For My Son*; the
  placement prefab `#c_santo_domingo/arroyo/loc_sts_pac_wwd_05_paint_factory`
  names the building; `mq025_mp_07_fight_club` and
  `sq025_07_sm_rhino_animation` sit on the anchor. There is no name guess.
- **Clean faction ownership despite the seed's sub-territory.** Site 378 has
  `default_faction_id = 6` and 9 roster units. (`initial_owner_faction_id = 20`
  follows the Arasaka-owned `arr_arasaka_industrial` sub-territory guess — a
  seed artefact, not a sign that Arasaka runs the gym; §8.2.)
- **Richest hook set of the enclosed sites**: 3 guard areas
  (`restricted_movement_01/02`, `rma_worker`), 6 patrol splines, 5 doors, 15
  workspots and 13 triggers — everything a capture/defence prototype needs.
- **Not the HQ**, so the first capture proves a lore point can be taken without
  touching the seat.
- Fallback if the gym's `initial_owner` conflict causes trouble: **7th Hell**
  (site 351) — interior, 9 units, 5 guard areas and 6 doors. Fallback if a
  clean-ownership point is required: the **Juice den** (site 90) — `default` and
  `initial` both 6, 10 units, 11.2 m from an Animals-owned CC, but exterior.

---

## 7. Per-sub-district count of lore-relevant locations

`named` counts distinct named places the Animals own, run, protect or habitually
occupy — one entry per place, not per quest variant. `filler` is the deduped
occupied-site count minus sites already counted as a named place (METHOD §8).

| Sub-district | Named lore-relevant places | Which ones | Animals-occupied sites (deduped, `[game-data]`) | Filler | Noteworthy interiors |
| --- | ---: | --- | ---: | ---: | ---: |
| Coastview | **2** | Grand Imperial Mall, Unfinished NCART Station | 3 | 2 | 2 (mall, NCART) |
| Downtown | **2** | 7th Hell, Empathy | 3 | 1 | 2 (both clubs) |
| Wellsprings | **2** | Data Inc., Skyline South Juice den | 2 | 0 | 1 (Data Inc. store/basement) |
| Arroyo | **1** | Tripple Extreme Gym | 1 | 0 | 1 (gym) |
| WestWindEstate | **0** | turf/gang-watch only | 1 | 1 | 0 |
| JapanTown | **0** | assault in progress only | 1 | 1 | 0 |
| LittleChina | **0** | market shakedown only | 1 | 1 | 0 |
| CorpoPlaza | **0** | scanner-hustle scene only | 1 | 1 | 0 |
| RanchoCoronado | **0** | mini-world-story only | 1 | 1 | 0 |
| **Total** | **7** | | 14 | 8 | 6 |

Filler sites by sub-district:

- **Coastview (2)** — `ma_pac_cvi_11`, `ma_pac_cvi_05`
- **Downtown (1)** — `ma_cct_dtn_01`
- **WestWindEstate (1)** — `ma_pac_wwd_01`
- **JapanTown (1)** — `ma_wbr_jpn_19`
- **LittleChina (1)** — `ma_wat_lch_04`
- **CorpoPlaza (1)** — `ma_cct_cpz_17`
- **RanchoCoronado (1)** — `mws_arr_07`

Reconciliation: **7 named + 8 filler = 15** = 14 deduped occupied sites + 1
marker-only named place (the Grand Imperial Mall). Six of the seven named places
are site-backed: 377 NCART, 352 Empathy, 351 7th Hell, 378 Tripple Gym, 376 Data
Inc. and 90 Juice den.

**Interpretation for yield.** This is a **pack-scattered** faction, not a turf
power:

1. The Animals have no sub-district with more than two named places. Yield should
   be spread across Coastview, Downtown and Wellsprings rather than concentrated.
2. Coastview + Downtown carry the presence weight (26 of 45 areas, 20 of 43 spawn
   points) and four of the seven named places. Those two sub-districts should be
   the high-contest zones.
3. Arroyo has exactly one named point (Tripple Gym) but it is the strongest
   owned property; it should carry the highest per-point yield of any point on
   the map, not a reduced "outlier" value.
4. The nine sub-districts with zero named places but nonzero areas (Kabuki,
   JapanTown, LittleChina, CharterHill, Dogtown, CorpoPlaza, RanchoCoronado,
   WestWindEstate) are **presence-only**. If they need capturing, type them as
   "contested block" and exclude them from iconic-business multipliers.

If 7 named points is too few for the map, the §3.2 table is the honest filler
pool — all scanner hustles, none with business affordances beyond `club` and
`arms_cache`.

---

## 8. Gaps and uncertainties

1. **The Animals have no canon HQ.** The wiki organisation infobox reads
   `headquarters = N/A` and the faction has "no defined territory". The GIM is a
   *hired* base (NetWatch contract), not a hereditary seat, and the wiki says
   Scavengers later stripped it. I chose it because the seed already grants it
   and because it is where Sasquatch is fought; a reviewer may reasonably prefer
   Tripple Extreme Gym as the "owned" HQ.
2. **Tripple Extreme Gym's sub-district is contested.** The raw placement path is
   `#c_santo_domingo/arroyo/loc_sts_pac_wwd_05_paint_factory_prefab…` and the
   site's `sub_territory_id` is `arr_arasaka_industrial` (Arroyo); the wiki
   infobox says **Rancho Coronado**, Baptiste St. I use Arroyo per game data and
   flag the wiki conflict. The site's `initial_owner_faction_id = 20` (Arasaka) is
   a sub-territory artefact, not a claim that Arasaka runs the gym.
3. **Unfinished NCART Station's sub-district is contested three ways.** The
   placement path is `c_pacifica/coastview/loc_sts_pac_cvi_02` and the site token
   is `cvi` → **Coastview**; the wiki location page and the gig infobox say
   **West Wind Estate**; the site's `sub_territory_id` is `dt_longshore_stacks`
   (**Dogtown**); and the coordinate `(-2442, -2566)` sits on the
   West Wind / Dogtown border. I use Coastview (prefab + token) and flag the rest.
   If the intended sub-district is West Wind Estate, move one `named` from
   Coastview to WestWindEstate; the totals do not change.
4. **`sub_territory_id` is a nearest-centroid guess and is wrong on several
   sites.** `sts_hey_spr_06` (Data Inc.) → `arr_arasaka_industrial` (Arroyo)
   though its prefab and token are Wellsprings; `ma_wbr_jpn_19` →
   `hil_gold_beach` (Charter Hill) though it is JapanTown; `sts_cct_dtn_02`
   (7th Hell) → `cpz_ring_road_west` though it is a Downtown club;
   `mws_arr_07` → `rcr_piez_plaza` though its token is `arr`. There are no
   sub-territory polygons in the extract, so neither source is provably right.
5. **`initial_owner_faction_id` on the named sites mostly points at rivals.**
   Tripple = Arasaka (20), Empathy = Tyger Claws (2), NCART = Barghest (10), Data
   Inc. = Valentinos (3), 7th Hell = Arasaka (20). The field follows the seeded
   sub-territory, not the building. Ownership evidence is `default_faction_id`
   plus the roster join, not `initial_owner_faction_id`.
6. **The Grand Imperial Mall has no `sites.json` row, roster, community record or
   guard/patrol data.** It is marker-only, like Totentanz and All Foods. Its
   identity rests on the `q110`/`mq025` marker families, six `q110_com_mall_*`
   communities and the `Coastview_GrandImperialMall` enum (37). The seed also
   lacks a site, so a capture trigger there needs a new anchor.
7. **"Skyline South" is not a resolvable place.** `action=parse&page=Skyline
   South` returns `missing`, and there is no `skyline_south` sub-territory in
   Wellsprings (`rey_skyline_south` is in Vista del Rey, 1.5 km away). The seed
   label for the area is "Wellsprings Pump Station". The *place* is solid — the
   `ma_hey_spr_11` baseid match to *Living the Big Life* is exact — but the name
   is `[inferred]`/`[wiki]`, not a game label.
8. **`areas.jsonl.district_code` is wrong for quest communities.** The GIM areas
   are labelled `dogtown`, the NCART areas `dogtown`/`badlands`, and the Data Inc.
   area `badlands`, because quest communities inherit the always-loaded file's
   path token. All counts were re-attributed by token/position (METHOD §1.1
   item 4); do not aggregate the raw field.
9. **Most Animals presence outside Pacifica is quest or scanner noise.**
   `{sq012_com_rqr_club_ug}` (8 Animals, Charter Hill) is a club scene for a
   quest with no resolvable `sq012` wiki page; `{mq028_com_stalker_park}` (5,
   Kabuki), `{sa_ep1_113_com_combat}` (5, Coastview) and
   `{spr_06_animals_com}` (4) are combat communities. Presence ≠ ownership.
10. **Eden Plaza and Golden Pacific list Animals in their infoboxes but have no
    Animals site, marker or roster.** Both are BARGHEST-dominated Dogtown
    locations; the Animals are a listed minor gang. Do not seed them.
11. **Jig-Jig Street lists Animals as one of four gangs.** It is Tyger Claws turf
    with Mox and Scavenger rivalry; the Animals are a presence, not a proprietor.
12. **The Afterlife is not an Animals property.** Emmerick Bronson, an Animal, is
    its bouncer (`wat_sm_lch_afterlife_bouncer`, `-1458.662, 1014.676, 16.910`),
    but the bar is Rogue's. This is bodyguard-economy evidence, not a control
    point.
13. **Seamus Sawicki's club is unnamed.** The wiki says he is a bouncer at "one of
    their clubs" and was ordered to kill Militech interns after they hurt the
    club's joygirls, but no site, marker or wiki location identifies it. Not
    seeded.
14. **Inconsistency in the METHOD validator's vocabulary.** `METHOD.md` §7 defines
    `mercenary` (muscle for hire, contract violence), but the §10.2 validator's
    `VOCAB` set omits it (along with `netrunning`, `information`, `logistics`,
    `finance`, `hospitality`, `education`, `funeral`). Because §10.2 must pass,
    `mercenary` is used only in §4.1 prose and no control point carries it. The
    gang's core "muscle for hire" is therefore under-represented in the JSON;
    either the validator set or the revenue-code list should be reconciled.
    *Resolved 2026-11-25: METHOD.md's validator now includes every §7 code, and the JSON block carries the intended codes.*
15. **The `wwd_highway_gate` sub-territory is seed-only.** No site, marker,
    community or wiki page corresponds to "West Wind South Highway" at
    `(-2465.3, -2883.6)`; it counts as neither `named` nor `filler` (METHOD §1.1
    item 16).
16. **No vendor inventory in the extract.** "What each business sells" is always
    `[wiki]` or `[inferred]`. Data Inc.'s suitability tags are
    `arms_cache / market_stall / officer_site / raid_target` — no `retail` or
    `warehouse` tag — yet the gig proves it is a store with a basement den.
    Suitability tags are combat affordances, not a business taxonomy.
17. **Interior flags are sparse.** `is_interior` is set on only 1 of the 14
    Animals candidate sites (Tripple). NCART, 7th Hell, Empathy and Data Inc. are
    demonstrably enclosed from node names (rooms, floors, basements, server
    rooms), so their JSON `interior: true` is justified from records, not the
    flag.
18. **The `sq012` Charter Hill club scene is unidentified.** Eight Animals
    dominate `{sq012_com_rqr}` / `{sq012_com_rqr_club_ug}` at `(663, -476)`, but
    `sq012` has no wiki page and the nearest site is an Arasaka-owned site
    (`ma_wbr_hil_06`). It may be a quest club we never see named; it is not
    counted.

---

## 9. Sources

- Local: `dist/extract/areas.jsonl`, `dist/extract/markers.jsonl`,
  `dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_{0,1}.streamingsector.json`
  (placement prefabs for `sts_pac_wwd_05`, `sts_pac_cvi_02`, `sts_hey_spr_06`,
  `ma_pac_wwd_01`),
  `data/sites/{sites,communities,rosters,guards,triggers,spots,patrols,doors,suitabilities}.json`,
  `data/{districts,factions,control_centers,sub_territories,landmarks,spawn_points}.json`,
  `refs/RED4ext.SDK/include/RED4ext/Scripting/Natives/Generated/game/data/District.hpp`
  (`Coastview_GrandImperialMall = 37`, `WestWindEstate = 130`).
- Wiki: [Animals](https://cyberpunk.fandom.com/wiki/Animals),
  [Animals Members](https://cyberpunk.fandom.com/wiki/Animals_Members),
  [Grand Imperial Mall](https://cyberpunk.fandom.com/wiki/Grand_Imperial_Mall),
  [Matilda K. Rose / Sasquatch](https://cyberpunk.fandom.com/wiki/Matilda_K._Rose),
  [I Walk the Line](https://cyberpunk.fandom.com/wiki/I_Walk_the_Line),
  [Tripple Extreme Gym](https://cyberpunk.fandom.com/wiki/Tripple_Extreme_Gym),
  [Gig: For My Son](https://cyberpunk.fandom.com/wiki/Gig:_For_My_Son),
  [Beat on the Brat](https://cyberpunk.fandom.com/wiki/Beat_on_the_Brat),
  [Beat on the Brat: Rancho Coronado](https://cyberpunk.fandom.com/wiki/Beat_on_the_Brat:_Rancho_Coronado),
  [Rhino](https://cyberpunk.fandom.com/wiki/Rhino),
  [Logan Garcia](https://cyberpunk.fandom.com/wiki/Logan_Garcia),
  [Unfinished NCART Station](https://cyberpunk.fandom.com/wiki/Unfinished_NCART_Station),
  [Gig: Two Wrongs Makes Us Right](https://cyberpunk.fandom.com/wiki/Gig:_Two_Wrongs_Makes_Us_Right),
  [Juice](https://cyberpunk.fandom.com/wiki/Juice),
  [7th Hell](https://cyberpunk.fandom.com/wiki/7th_Hell),
  [Gig: An Inconvenient Killer](https://cyberpunk.fandom.com/wiki/Gig:_An_Inconvenient_Killer),
  [Empathy](https://cyberpunk.fandom.com/wiki/Empathy_(club)),
  [Gig: A Lack of Empathy](https://cyberpunk.fandom.com/wiki/Gig:_A_Lack_of_Empathy),
  [Data Inc. (Wellsprings)](https://cyberpunk.fandom.com/wiki/Data_Inc._(Wellsprings)),
  [Gig: Hot Merchandise](https://cyberpunk.fandom.com/wiki/Gig:_Hot_Merchandise),
  [Suspected Organized Crime Activity: Living the Big Life](https://cyberpunk.fandom.com/wiki/Suspected_Organized_Crime_Activity:_Living_the_Big_Life),
  [Denzel Cryer](https://cyberpunk.fandom.com/wiki/Denzel_Cryer),
  [Emmerick Bronson](https://cyberpunk.fandom.com/wiki/Emmerick_Bronson),
  [Afterlife](https://cyberpunk.fandom.com/wiki/Afterlife),
  [Eden Plaza](https://cyberpunk.fandom.com/wiki/Eden_Plaza),
  [Golden Pacific](https://cyberpunk.fandom.com/wiki/Golden_Pacific),
  [Jig-Jig Street](https://cyberpunk.fandom.com/wiki/Jig-Jig_Street).
- Earlier repo research: `docs/research/factions-gangs-territories.md`,
  `docs/research/game-data-extraction.md`.

---

## 10. Machine-readable block

Strict JSON for seeding (contract in [`METHOD.md`](./METHOD.md) §10). Every
coordinate was re-verified against the local record named in `source` on
2026-11-25; none came from the wiki.

```json
{
  "faction_code": "animals",
  "hq": {
    "name": "Grand Imperial Mall",
    "district": "Pacifica",
    "sub_district": "Coastview",
    "x": -2363.001,
    "y": -2026.324,
    "z": 15.811,
    "source": "dist/extract/markers.jsonl mq025_mp_08_ring",
    "confidence": "game-data+wiki"
  },
  "alternate_hqs": [
    {
      "name": "Tripple Extreme Gym",
      "district": "SantoDomingo",
      "sub_district": "Arroyo",
      "x": -500.969,
      "y": -1924.883,
      "z": 7.987,
      "source": "data/sites/sites.json site 378 sts_pac_wwd_05",
      "confidence": "game-data+wiki"
    },
    {
      "name": "7th Hell",
      "district": "CityCenter",
      "sub_district": "Downtown",
      "x": -1927.012,
      "y": -42.783,
      "z": 3.466,
      "source": "data/sites/sites.json site 351 sts_cct_dtn_02",
      "confidence": "game-data+wiki"
    }
  ],
  "test_control_point": {
    "name": "Tripple Extreme Gym",
    "district": "SantoDomingo",
    "sub_district": "Arroyo",
    "x": -500.969,
    "y": -1924.883,
    "z": 7.987,
    "source": "data/sites/sites.json site 378 sts_pac_wwd_05",
    "confidence": "game-data+wiki"
  },
  "control_points": [
    {
      "rank": 1,
      "name": "Grand Imperial Mall",
      "type": "mall",
      "relevance": 5,
      "district": "Pacifica",
      "sub_district": "Coastview",
      "x": -2363.001,
      "y": -2026.324,
      "z": 15.811,
      "source": "dist/extract/markers.jsonl mq025_mp_08_ring",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": [
        "security_services",
        "gambling",
        "food_drink",
        "mercenary"
      ],
      "nearest_cc_code": "cc_cvi_grand_imperial_mall",
      "nearest_cc_m": 35.1
    },
    {
      "rank": 2,
      "name": "Tripple Extreme Gym",
      "type": "fight_club",
      "relevance": 5,
      "district": "SantoDomingo",
      "sub_district": "Arroyo",
      "x": -500.969,
      "y": -1924.883,
      "z": 7.987,
      "source": "data/sites/sites.json site 378 sts_pac_wwd_05",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": [
        "gambling",
        "retail",
        "mercenary"
      ],
      "nearest_cc_code": "cc_arr_arasaka_industrial",
      "nearest_cc_m": 372.2
    },
    {
      "rank": 3,
      "name": "Unfinished NCART Station",
      "type": "metro_station",
      "relevance": 4,
      "district": "Pacifica",
      "sub_district": "Coastview",
      "x": -2441.771,
      "y": -2565.546,
      "z": -0.681,
      "source": "data/sites/sites.json site 377 sts_pac_cvi_02",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": [
        "drugs",
        "smuggling"
      ],
      "nearest_cc_code": "cc_dt_longshore_stacks",
      "nearest_cc_m": 123.9
    },
    {
      "rank": 4,
      "name": "7th Hell",
      "type": "nightclub",
      "relevance": 4,
      "district": "CityCenter",
      "sub_district": "Downtown",
      "x": -1927.012,
      "y": -42.783,
      "z": 3.466,
      "source": "data/sites/sites.json site 351 sts_cct_dtn_02",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": [
        "food_drink",
        "protection"
      ],
      "nearest_cc_code": "cc_spr_boardwalk_north",
      "nearest_cc_m": 193.8
    },
    {
      "rank": 5,
      "name": "Empathy",
      "type": "braindance_club",
      "relevance": 4,
      "district": "CityCenter",
      "sub_district": "Downtown",
      "x": -1629.752,
      "y": 385.799,
      "z": 8.093,
      "source": "data/sites/sites.json site 352 sts_cct_dtn_03",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": [
        "braindance",
        "sex_work",
        "food_drink",
        "protection"
      ],
      "nearest_cc_code": "cc_dtn_corporation_st",
      "nearest_cc_m": 142.1
    },
    {
      "rank": 6,
      "name": "Skyline South Juice den",
      "type": "drug_den",
      "relevance": 3,
      "district": "Heywood",
      "sub_district": "Wellsprings",
      "x": -2039.627,
      "y": -1301.386,
      "z": 7.292,
      "source": "data/sites/sites.json site 90 ma_hey_spr_11",
      "confidence": "game-data+wiki",
      "interior": false,
      "revenue_streams": [
        "drugs"
      ],
      "nearest_cc_code": "cc_spr_pump_station",
      "nearest_cc_m": 11.2
    },
    {
      "rank": 7,
      "name": "Data Inc. (Wellsprings)",
      "type": "electronics_store",
      "relevance": 3,
      "district": "Heywood",
      "sub_district": "Wellsprings",
      "x": -2254.987,
      "y": -405.114,
      "z": 7.39,
      "source": "data/sites/sites.json site 376 sts_hey_spr_06",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": [
        "arms",
        "retail",
        "netrunning"
      ],
      "nearest_cc_code": "cc_spr_berkeley_bay",
      "nearest_cc_m": 225.3
    }
  ],
  "subdistrict_counts": {
    "Coastview": {
      "named": 2,
      "filler": 2
    },
    "Downtown": {
      "named": 2,
      "filler": 1
    },
    "Wellsprings": {
      "named": 2,
      "filler": 0
    },
    "Arroyo": {
      "named": 1,
      "filler": 0
    },
    "WestWindEstate": {
      "named": 0,
      "filler": 1
    },
    "JapanTown": {
      "named": 0,
      "filler": 1
    },
    "LittleChina": {
      "named": 0,
      "filler": 1
    },
    "CorpoPlaza": {
      "named": 0,
      "filler": 1
    },
    "RanchoCoronado": {
      "named": 0,
      "filler": 1
    }
  }
}
```
