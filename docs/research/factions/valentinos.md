# Valentinos — Lore-Relevant Control Points

Status: research run, 2026-11-25. One faction, one document.
Scope: turn the generic per-sub-district control-centre grid into lore-relevant,
capturable places for the Valentinos, with an honest count per sub-district.
Method: this doc conforms to [`METHOD.md`](./METHOD.md); the research snippets,
wiki rules, revenue-code vocabulary and JSON contract live there.

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Position, site, community, roster or spawn record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/artbook/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My inference linking a named place to a game record; reasoning stated | Weak, flagged |

No coordinate below is guessed. Every `(x, y, z)` is either copied from a named
record in the local extracts or marked `TBD`.

---

## 1. Summary

The Valentinos are Night City's largest Latino gang and the only gang the
vanilla district record assigns to **Heywood**: about **6,000 members in 2077**,
Chicano culture, Santa Muerte and Jesús Malverde iconography, and a strict
"protect the barrio" code that makes them a community institution as much as a
crime syndicate. Their 2077 leadership is split: main leader **Campo Orta** is
serving a prison term, with **El Sombrerón** and **Gustavo Orta** as secondary
leaders. `[wiki]`

They are **strictly territorial**. The wiki names only the three Heywood
barrios — **the Glen, Vista del Rey and Wellsprings** — as their turf, and the
game data agrees: 70 of 87 Valentino community areas and 60 of 77 gang spawn
points fall in those three sub-districts. `[wiki]` `[game-data]`

Their economic model is protection plus contraband, laundered through ordinary
barrio businesses:

- **Gun smuggling and illegal weapon modification** — the first-listed income
  stream. `[wiki]`
- **Car theft and chop shops** — stolen vehicles, pimped-out lowriders, vehicle
  bays. `[wiki]`
- **Drug trafficking** — wholesale and retail; the funeral home is the canonical
  hiding place ("caskets… full of… drugs and guns"). `[wiki]`
- **Prostitution** — including the Dicky Twister back rooms. `[wiki]`
- **Robbery, burglary and hit jobs** — the gang hires out muscle. `[wiki]`
- **Protection rackets** — "the Valentinos protected the whole neighborhood";
  local businesses pay in kind. `[wiki]`
- **Legal fronts** — restaurants, auto shops, construction companies,
  nightclubs, braindance studios and sports-betting parlors. `[wiki]`

The commercial weight sits in **Vista del Rey** (5 of 11 named places and the
densest Valentino spawn presence) and **the Glen** (the community heart,
El Coyote Cojo, plus the gang's fixer). **Wellsprings** holds the two industrial
fronts: the auto shop and the bus depot.

The wiki leaves the organisation **headquarters field blank**. The five named
2077 faction locations are *La Catrina*, *El Coyote Cojo*, *Moto Cielo*,
*Nuestra Señora De Los Desamparados Cathedral* and *Sugar Skull Planet*; only
the first two have verified in-game anchors. `[wiki]` `[game-data]`

---

## 2. Territory

### 2.1 Districts

Wiki locations are Heywood. Evidence in three kinds:

| Evidence kind | Result |
| --- | --- |
| (a) Wiki/lore | "Strictly territorial", operating in the Latino barrios of **the Glen, Vista del Rey and Wellsprings** (Heywood). `[wiki]` |
| (b) Vanilla map gang panel | `data/districts.json`: Heywood `vanilla_gangs = ["Valentinos"]`; every other district lists other gangs. `[game-data]` |
| (c) Game-data counts | 87 community areas contain Valentino spawns (77 Valentino-dominant); 24 roster sites with 177 Valentino units; **13 owned sub-territories** (5 Vista del Rey, 4 Wellsprings, 3 the Glen, 1 Downtown); 77 faction spawn points. `[game-data]` |

The 13 seeded holdings:

| Sub-district | Owned sub-territories (`data/sub_territories.json`) |
| --- | --- |
| VistaDelRey | College Street Tenements, Delamain Industrial Block, Skyline & Republic Yard, Vista East Canals, La Catrina Crossing |
| Wellsprings | Palm View Plaza, Wellsprings North Pier, Cannery Row Promenade, Berkeley & Bay Yard |
| Glen | Ventura & Skyline, Reconciliation Park West, Glen Canal Promenade |
| Downtown | Downtown South Quay |

### 2.2 Sub-district presence

Counts follow `METHOD.md` §3.3: `areas` is every `areas.jsonl` row whose
`faction_counts` contains `valentinos`, attributed by geocode token first, then
nearest geocoded site within 400 m, then nearest sub-territory centroid
("dominant" = `dominant_faction == valentinos`). `spawn pts` is
`data/spawn_points.json` with `faction_id == 3`, bucketed by
`sub_territory_id`. `Occupied sites` is the deduped roster/ownership set from
§3.2 below.

| Sub-district | District | (a) Lore | (b) Vanilla panel | (c) Areas (dominant) | (c) Spawn pts | Occupied sites | Named places |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| VistaDelRey | Heywood | core ("kings") | Valentinos | 26 (25) | 22 | 9 | 5 |
| Glen | Heywood | core | Valentinos | 27 (23) | 22 | 5 | 4 |
| Wellsprings | Heywood | core | Valentinos | 17 (17) | 16 | 5 | 2 |
| Downtown | CityCenter | peripheral | — | 3 (3) | 3 | 1 | 0 |
| Arroyo | SantoDomingo | peripheral | 6th Street | 6 (4) | 4 | 0 | 0 |
| CorpoPlaza | CityCenter | peripheral | — | 0 (0) | 2 | 0 | 0 |
| JapanTown | Westbrook | peripheral | Tyger Claws | 0 (0) | 3 | 0 | 0 |
| Badlands | Badlands | incidental | Aldecaldos | 2 (1) | 1 | 0 | 0 |
| LittleChina | Watson | incidental | Maelstrom | 2 (1) | 1 | 0 | 0 |
| Northside | Watson | incidental | Maelstrom | 1 (1) | 1 | 0 | 0 |
| NorthOaks | Westbrook | incidental | — | 1 (1) | 1 | 0 | 0 |
| RanchoCoronado | SantoDomingo | incidental | 6th Street | 1 (1) | 1 | 1 | 0 |
| Kabuki | Watson | incidental | Tyger Claws | 1 (0) | 0 | 0 | 0 |

**Reading the counts.** Community areas measure *presence*, not places. A single
NCPD scanner hustle supplies several areas (`ma_hey_rey_06` / Mercado Sonora
alone has `_enemies`, `_victims`, plus the open-world crowd sheets). The counts
that matter for yield are in §7.

### 2.3 Attribution caveat

`areas.jsonl.district_code` is wrong for `always_loaded_*` quest communities
(`METHOD.md` §2.2). Two Valentino cases:

1. `{sq018_com_valentinos_el_coyote}` and `{benchmark_community}` are labelled
   `heywood` and sit at `(-1258, -997)`; the raw world prefab path is
   `#c_heywood/glen/loc_sq022_el_coyote_cojo_bar/…`, i.e. **the Glen**. The
   district token alone would not settle Glen vs Vista del Rey, so §3.1 proves
   it from the prefab path.
2. `{benchmark_community}` also carries the Aldecaldos as a one-unit noise entry
   — these are the El Coyote crowd sheets, not a second faction's turf.

The mirror of the pilot's `rey_09` anomaly exists here too: `ma_hey_rey_01`
(carries a `rey` token) is physically placed at `(-837.6, 227.6)`, inside
`jpn_silk_road` (JapanTown). Treat it as a cross-border street-violence scene,
not as a Heywood holding (see §3.2).

---

## 3. Location catalog

Coordinates are world-space metres, `Z` up. "Interior?" means the game has a
distinct interior cell/sector for it, proven by interior node names in §3.1 —
`is_interior` is set on only one of the 24 Valentino sites, so the flag cannot
be used as evidence of absence.

| # | Name | Type | District / sub-district | Interior? | Business? (what it earns) | Coordinates (x, y, z) | Coordinate source record | Linked communities / sites | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **La Catrina** | Funeral home (gang front) | Heywood / VistaDelRey | Yes — lobby, chapel, morgue basement, garage | Yes: funeral services; caskets used for gun/drug trafficking and body disposal | `-1124.234, -663.598, 8.253` | `data/sites/sites.json` site 371 `sts_hey_rey_06` (anchor; node median z 8.3) | `rey_06_com_combat_com`; `Gig: Jeopardy` (`baseid = sts_hey_rey_06`) | `[game-data]` `[wiki]` |
| 2 | **Dicky Twister** | Gay club / bar | Heywood / VistaDelRey | Yes — 1st floor bar, 2nd floor, backstage, office | Yes: drinks, back rooms, sex trade; laundering front for gang "sidebiz" | `-815.978, -81.593, 8.605` | site 370 `sts_hey_rey_02` | `rey_02_com_enemies`; `Gig: Sr. Ladrillo's Private Collection` (`baseid = sts_hey_rey_02`) | `[game-data]` `[wiki]` |
| 3 | **Mercado Sonora** | Open-air market (underpass) | Heywood / VistaDelRey | No — underpass with vendor cells | Yes: hawker stalls, drugs, smuggling, protection fees | `-829.646, -400.347, 8.200` | site 66 `ma_hey_rey_06` (anchor; nearest node 4.3 m) | `ma_hey_rey_06_enemies` (12), `_victims` (6), `_community_after` (14, civilians/vendors); NCPD hustle `ma_hey_rey_06` | `[game-data]` `[wiki]` |
| 4 | **El Coyote Cojo** | Bar (community heart) | Heywood / Glen | Yes — bar, second floor, ofrenda room | Yes: food and drink; Padre meets V here; gang/community hub | `-1260.347, -984.175, 13.267` (entrance) | `dist/extract/markers.jsonl` `sq018_mp_el_coyote_entrance` | `loc_sq022_el_coyote_cojo_bar` prefab (Glen); `{sq018_com_valentinos_el_coyote}` 14 Valentinos; `{q000_kid_com_bar_crowd}` 19 | `[game-data]` `[wiki]` |
| 5 | **El Pinche Pollo** | Restaurant | Heywood / Glen | Yes — bar/kitchen, VIP 2nd floor with pool tables and office | Yes: food and drink; second floor is gang-only, office holds leverage evidence | `-1525.170, -1106.365, 13.098` | site 366 `sts_hey_gle_04` | `gle_04_com` (12 Valentinos); `Gig: Fifth Column` (`baseid = sts_hey_gle_04`) | `[game-data]` `[wiki]` |
| 6 | **Jacked and Coke** | Dive bar | Heywood / VistaDelRey | Yes — bar, kitchen, back rooms | Yes: drinks, pachinko machines, drug retail | `-926.445, -212.448, 7.673` | site 372 `sts_hey_rey_08` | `rey_08_combat_com` (9 Valentinos); `Character.sts_hey_rey_08_karubo`; `Gig: Old Friends` (`baseid = sts_hey_rey_08`) | `[game-data]` `[wiki]` |
| 7 | **Valentino Alley** | Gang alley / shrine corner | Heywood / Glen | No | Yes: extortion, kidnapping and robbery base; small stash | `-1636.997, -1228.885, 24.740` | site 42 `ma_hey_gle_02` | `ma_hey_gle_02_com` (11 Valentinos, incl. `_Rogelio_Cruz`); SOCA "Chapel" (`baseid = ma_hey_gle_02`) | `[game-data]` coords; name `[wiki]`; identity `[inferred]` |
| 8 | **Valentinos Auto Shop** | Auto shop / chop shop | Heywood / Wellsprings | Yes — garage, workshop | Yes: vehicle repair, stolen-vehicle stripping, weapon and vehicle modification | `-2345.589, -1007.419, 8.157` | site 375 `sts_hey_spr_03` | `spr_03_com` (11 Valentinos); `Gig: The Lord Giveth and Taketh Away` (`baseid = sts_hey_spr_03`) | `[game-data]` `[wiki]` |
| 9 | **Bus Depot** | Defunct bus depot / staging base | Heywood / Wellsprings | Yes — garage, workshop, office, locker room, balcony | Yes: arms cache and staging for an anti-Arasaka op; abandoned after the gig | `-2078.184, -981.131, 7.450` | site 374 `sts_hey_spr_01` | `spr_01_com` (20 Valentinos, incl. `_jose`); `Gig: On a Tight Leash` (`baseid = sts_hey_spr_01`) | `[game-data]` `[wiki]` |
| 10 | **Padre's Glen corner** | Fixer office (open-air) | Heywood / Glen | No — plaza/food-shop frontage | Yes: fixer brokerage, contract hand-offs, protection | `-1804.750, -1279.139, 21.870` | `markers.jsonl` `padre_sm_default` (world-space row) | `loc_hey_gle_fixer_01` prefab; `#hey_gle_fixer_com`; `#padre_tr_prevention_clear` | `[game-data]` coords; role `[wiki]` |
| 11 | **Gustavo Orta's Apartment** | Gang command apartment | Heywood / VistaDelRey (seed says CorpoPlaza) | Yes — 32nd floor, four apartment floors, lift | No (not a business); a secondary leader's base of operations | `-975.638, 86.231, 48.350` (floor level); ground door `-969.561, 82.722, 8.411` | site 369 `sts_hey_rey_01`; `markers.jsonl` `rey_01_mp_apartment_door` | `rey_01_apartment_com`; `Character.sts_hey_rey_01_gustavo`; `Gig: Bring Me the Head of Gustavo Orta` (`baseid = sts_hey_rey_01`) | `[game-data]` `[wiki]` |
| 12 | Megabuilding H5 | Megabuilding (host landmark) | Heywood / VistaDelRey | Yes (megabuilding) | No direct revenue; hosts Mercado Sonora at its foot | `TBD` | — (no mappin resolves offline) | hosts Mercado Sonora (3) | `[wiki]` |
| 13 | The View | Luxury shopping mall | CityCenter / CorpoPlaza (borders the Glen) | Yes (multi-level mall) | Yes: retail, dining, luxury goods; Valentino-tagged turf | `TBD` | — (only `#cct_cpz_the_view_tr_codex` node ref exists in the raw sector; no position) | `corpo_plaza_rpg_hub_001`; `#cct_cpz_the_view_tr_codex` | `[wiki]` + node existence `[game-data]` |
| 14 | Eric's Motorcycles | Motorcycle repair shop | Heywood / Glen | TBD | Yes: bike repair (Stephenson/Fuyutsuki/SoftSys parts); Valentino ties | `TBD` | — (no prefab/marker found) | none found | `[wiki]` |
| 15 | Tirempire Auto Shop | Auto shop | SantoDomingo / Arroyo | Yes — single-floor garage + corner office | Yes: garage; Valentino garrison during *Small Man, Big Mouth* | `TBD` | — (no site/marker found) | none found | `[wiki]` |
| 16 | Moto Cielo | Lore site (biker bar / "Bike Heaven") | Heywood (sub-district unstated) | TBD | TBD | `TBD` | — | mentioned only | `[wiki]` `[lore]` |
| 17 | Nuestra Señora De Los Desamparados Cathedral | Cathedral | Heywood (sub-district unstated) | TBD | TBD (ceremonial/institutional) | `TBD` | — | listed as a faction location only | `[lore]` |
| 18 | Sugar Skull Planet | Shop / venue (unclassified) | TBD | TBD | TBD | `TBD` | — | listed as a faction location only | `[lore]` |

### 3.1 How the name→coordinate links were proven

Two independent mechanisms were used, and the second is the one that makes this
faction tractable:

1. **Wiki `baseid` → site code.** Every gig and NCPD-hustle infobox carries a
   `baseid` equal to a `sites.json` code. This is a direct join, not an
   inference:
   - `Gig: Jeopardy` → `sts_hey_rey_06` → site 371, and its node names are
     `#rey_06_tr_funeral_house`, `#rey_06_tr_enter_furneral_house`,
     `#rey_06_tr_chapel_talking`, `#rey_06_tr_furnace_talking`,
     `#rey_06_tr_bodies_room`, `#sts_hey_rey_06_basement`,
     `#rey_06_tr_garage` → **La Catrina**.
   - `Gig: Sr. Ladrillo's Private Collection` → `sts_hey_rey_02` → site 370, with
     `#rey_02_tr_strip_club_enter`, `#rey_02_RMA_backstage`, `#rey_02_RMA_club`,
     `#rey_02_dvc_door_stripper_001/002`, `#rey_02_tr_office_room`,
     `#rey_02_dvc_locked_door_bouncer` → **Dicky Twister**.
   - `Gig: Old Friends` → `sts_hey_rey_08` → site 372, with `#rey_08_ga_bar`,
     `#rey_08_ga_bar_kitchen`, `#rey_08_ws_enemy_002_pachinko` and the named
     record `Character.sts_hey_rey_08_karubo` → **Jacked and Coke**.
   - `Gig: Bring Me the Head of Gustavo Orta` → `sts_hey_rey_01` → site 369, with
     `#sts_hey_rey_01_apartment_floor_gustavo` and
     `Character.sts_hey_rey_01_gustavo` → **Gustavo Orta's Apartment**.
   - `Gig: Fifth Column` → `sts_hey_gle_04` → site 366, with
     `#gle_04_ws_enemy_07_bar`, `#gle_04_tr_bilard_scene`, `#gle_04_tr_office`,
     `#gle_04_office_doors` → **El Pinche Pollo**.
   - `Gig: The Lord Giveth and Taketh Away` → `sts_hey_spr_03` → site 375, with
     `#spr_03_tr_workshop`, `#spr_03_tr_end_garage`, gate and door nodes →
     **Valentinos Auto Shop**.
   - `Gig: On a Tight Leash` → `sts_hey_spr_01` → site 374, with
     `#spr_01_tr_conference`, `#spr_01_tr_jose_jukebox`, `#spr_01_tr_inside`,
     `#spr_01_ws_backup_car` → **Bus Depot**.
   - `Suspected Organized Crime Activity (Vista del Rey)` → `ma_hey_rey_06` →
     site 66 → **Mercado Sonora** (the NCPD dispatcher names Martin Luther King
     Boulevard, matching the market address).
   - `Suspected Organized Crime Activity: Chapel` → `ma_hey_gle_02` → site 42,
     which the wiki places at **Valentino Alley**; the site itself is unnamed in
     the extract, so that name link stays `[inferred]`.
2. **Raw sector prefab paths.** `dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_*.streamingsector.json`
   contains `$/03_night_city/#c_heywood/<sub-district>/loc_<name>_prefab…`
   strings. Grepping them settles both identity and sub-district for places that
   have no site record:
   - `#c_heywood/glen/loc_sq022_el_coyote_cojo_bar…` proves **El Coyote Cojo is
     in the Glen**, not Vista del Rey. This contradicts
     `data/clean-slate/cast_and_hubs.json`, which labels it
     `heywood_vista_del_rey`.
   - `#c_heywood/vista_del_rey/loc_sq025_delamain_garage…` (Delamain HQ) and
     `#c_heywood/glen/loc_hey_gle_fixer_01…` (Padre's spot) are the same kind of
     proof.
3. **Markers for marker-only places.** `sq018_mp_el_coyote_entrance` gives the
   bar's door; `padre_sm_default` gives Padre's standing spot. Note that
   `padre_sm_default` appears **twice**: once at `(-1804.750, -1279.139, 21.870)`
   and once at `(6013.192, 6115.871, -0.510)` (a test-space copy). The second is
   outside the playable bounds; the doc uses the first.

### 3.2 Valentino-occupied generic sites (filler pool)

`data/sites/suitabilities.json` tags these sites with business affordances. They
are unnamed but honest control points; they should not receive iconic-business
yield multipliers.

| Site | Code | Sub-district | Interior | Suitability tags | Units | Coordinates (x, y, z) | Note |
| --- | --- | --- | --- | --- | ---: | --- | --- |
| 61 | `ma_hey_rey_01` | VistaDelRey* | no | club, hostage_site, raid_target, rooftop_access | 5 | `-837.6, 227.6, 10.6` | ***Anomaly:*** physically in `jpn_silk_road` (JapanTown); a cross-border street-violence scene, not turfy |
| 62 | `ma_hey_rey_02` | VistaDelRey | no | raid_target | 6 | `-1094.1, -195.9, -1.6` | Underground (z −1.6) Valentino hangout/stash |
| 63 | `ma_hey_rey_03` | VistaDelRey | no | club, hostage_site, market_stall, raid_target, rooftop_access | 6 | `-953.9, -506.2, 18.1` | Street execution scene (`la_execution_01`) with civilian witnesses |
| 64 | `ma_hey_rey_04` | VistaDelRey | no | hostage_site, raid_target | 6 | `-495.3, -129.6, 7.9` | Second execution scene (`la_execution_03`) |
| 43 | `ma_hey_gle_03` | Glen | no | raid_target | 6 | `-1973.5, -1039.8, 7.6` | "Xavi Velez" outpost |
| 44 | `ma_hey_gle_05` | Glen | no | club, hostage_site, raid_target, sewer_access | 6 | `-1730.2, -222.7, -13.5` | "Danilo Ruiz" outpost in the canal/sewer level; seed puts it in CorpoPlaza |
| 57 | `ma_hey_gle_11` | Glen | no | raid_target, rooftop_access | 1 | `-1567.8, -1045.1, 9.2` | 6th Street-owned site; the single Valentino is a combatant in a gang fight |
| 91 | `ma_hey_spr_12` | Wellsprings | no | raid_target, rooftop_access | 7 | `-2198.5, -996.6, 36.2` | Rooftop outpost; best Wellsprings filler (7 units) |
| 77 | `ma_hey_spr_02` | Wellsprings | no | arms_cache, raid_target, rooftop_access | 5 | `-2451.9, -827.1, 12.9` | Execution scene with an arms cache |
| 78 | `ma_hey_spr_03` | Wellsprings | no | hostage_site, raid_target | 4 | `-2255.9, -626.3, 7.4` | Street violence, cowering onlookers |
| 24 | `ma_cct_dtn_02` | Downtown | no | camera_net, hostage_site, raid_target, rooftop_access, stealth_entry | 5 | `-2250.7, -9.2, 11.0` | "Claudio Moreno" organ-harvesting site, in the Valentino-owned Downtown South Quay |
| 150 | `ma_std_rcr_05` | RanchoCoronado | no | raid_target, rooftop_access | 4 | `292.5, -986.7, 20.5` | Valentino vs 6th Street street fight |

Excluded from occupancy (present in the raw 24-site roster but not in the
counts):

| Site | Code | Sub-district | Units | Why excluded |
| --- | --- | --- | ---: | --- |
| 128 | `ma_std_arr_06` | Arroyo | 1 | The only "Valentino" entry is `Character.ma_std_arr_06_cyberpsycho` — a cyberpsycho, not a garrison |
| 234 | `ma_wat_nid_22` | Northside | 1 | `Character.ma_wat_nid_22_monk` — a monk bystander |
| 376 | `sts_hey_spr_06` | Wellsprings | 1 | **Data Inc.** junk store is Animals-owned; the single Valentino is a customer (`Character.sts_hey_spr_06_valentinos`) |

---

## 4. Economic structure

### 4.1 Revenue streams → catalog locations

| Revenue stream | Code(s) | Catalog locations that produce it | Evidence / notes |
| --- | --- | --- | --- |
| Gun smuggling, weapon modification | `arms` | La Catrina (1); Valentinos Auto Shop (8); Bus Depot (9) | Wiki lists gun smuggling first and "illegal modification of weapons"; the depot stored Militech equipment for an Arasaka frame-up. `[wiki]` `[game-data]` |
| Vehicle theft / chop shops | `vehicles_chop` | Valentinos Auto Shop (8); Bus Depot (9) | Wiki: car theft and chop shops; autoshop has garage/workshop nodes and 6 doors. `[wiki]` `[game-data]` |
| Drug trafficking | `drugs` | La Catrina (1); Mercado Sonora (3); Jacked and Coke (6); Valentino Alley (7) | Wiki: caskets used for drugs and guns; market is a trafficking hub (NCPD dispatch). `[wiki]` |
| Smuggling / contraband logistics | `smuggling` | La Catrina (1); Mercado Sonora (3); Valentinos Auto Shop (8); Bus Depot (9) | Funeral home is a legal front for illicit goods; auto shop/depot are vehicle logistics. `[wiki]` `[inferred]` |
| Prostitution | `sex_work` | Dicky Twister (2) | Wiki: back-room "quickies"; gang income includes prostitution. `[wiki]` |
| Protection / extortion | `protection` | Mercado Sonora (3); El Pinche Pollo (5); El Coyote Cojo (4); Valentino Alley (7); Padre's corner (10) | Wiki: the gang protects the neighbourhood and collects from local business. SOCA "Chapel" record lists extortion. `[wiki]` |
| Gambling (sports betting, pachinko) | `gambling` | Jacked and Coke (6) | Wiki: sports-betting parlors; the bar has `pachinko` workspots (`#rey_08_ws_enemy_002_pachinko`). `[wiki]` + `[inferred]` |
| Fixer brokerage | `fixer_brokerage` | Padre's corner (10); El Coyote Cojo (4) | Padre is a Heywood fixer and former Valentino; `sq018_03c_sm_padre` is inside El Coyote. `[wiki]` `[game-data]` |
| Food and drink / nightlife | `food_drink` | El Coyote Cojo (4); El Pinche Pollo (5); Jacked and Coke (6); Dicky Twister (2); Mercado Sonora stalls (3) | Wiki: restaurants, bars, nightclubs as fronts. `[wiki]` |
| Retail | `retail` | Mercado Sonora (3); La Catrina (1, funeral services); The View (13, if seeded) | Market stalls; the mall's stores. `[wiki]` |
| Legal-funeral cash flow / body disposal | `retail` (services) | La Catrina (1) | Wiki DB entry: "completely legal enterprise in the eyes of both God and state". `[wiki]` |

**Not mapped to any verified place** (do not invent a venue):

- `braindance` — the wiki says they operate BD recording studios, but no
  Valentino-owned BD venue exists in the extract. Data Inc. is Animals-owned.
- `media`, `cyberware`, `energy`, `manufacturing`, `rnd`, `security_services` —
  no Valentino evidence.
- **Robbery, burglary and hit jobs** have no §7 code. `protection` is the
  nearest fit but is not the same business; see §8.

### 4.2 Suppliers, customers, rivals

| Role | Party | Detail |
| --- | --- | --- |
| Supplier (arms, Staging) | Militech (unwitting) | Bus Depot held Militech equipment staged by José Luis for a false-flag Arasaka attack. `[wiki]` |
| Customer / client | Arasaka (via Yorinobu) | Orchestrated the frame-up through a Valentino crew. `[wiki]` |
| Customer | Heywood residents, tourists, corpos | Local barrio trade, plus corpos who imitate Valentino style and buy from their chop shops. `[wiki]` |
| Fixer / broker | Sebastian "Padre" Ibarra | Former Valentino priest turned Heywood fixer; runs gigs from the Glen and uses El Coyote Cojo. `[wiki]` |
| Leader (in prison) | Campo Orta | Main leader with "four more years" as of 2077. `[wiki]` |
| Secondary leaders | El Sombrerón, Gustavo Orta | Gustavo runs from the Vista del Rey apartment. `[wiki]` `[game-data]` |
| Rival | 6th Street | Escalating turf war over Vista del Rey; the Glen is contested (see `cc_gle_senate_market` ownership). `[wiki]` `[game-data]` |
| Rival | Tyger Claws | Heywood/Westbrook overlap; a Valentino street scene sits in south JapanTown. `[wiki]` `[game-data]` |
| Rival | Scavengers | Listed alongside Valentinos in Vista del Rey; organ harvesting in the same district. `[wiki]` `[game-data]` |
| Law | NCPD | Three of the catalog sites are NCPD scanner hustles (`ma_hey_gle_02`, `ma_hey_rey_06`, `ma_cct_dtn_02`). `[game-data]` |

---

## 5. Headquarters recommendation

### Primary HQ: **La Catrina** — Vista del Rey

Coordinates: `-1124.234, -663.598, 8.253`. `[game-data]`
`data/sites/sites.json` site 371 `sts_hey_rey_06`.

Rationale:

1. **Canonically Valentino-controlled.** The wiki calls it "a Valentino-run
   funeral home" and one of the five 2077 faction locations. It is the gang's
   cleanest legal-front institution. `[wiki]`
2. **It is a functional seat, not just a venue.** The interior has a lobby, a
   chapel, a restroom/refrigerated closet, a guarded morgue in the basement, and
   a garage — real rooms to assign to org roles (chapel = assembly/ceremony,
   morgue = clinic/forensics, garage = vehicle bay). `[wiki]` `[game-data]`
3. **It maps 1:1 onto the gang's core economy.** The database entry is explicit
   that the caskets carry drugs and guns; this is where smuggling, arms and
   vehicle logistics meet. `[wiki]`
4. **Strong record support.** Site 371 carries 4 guard areas, 29 triggers, 34
   workspots, 3 patrol routes and 4 doors; the wiki gig *Jeopardy* uses
   `baseid = sts_hey_rey_06`, proving the place is a real, enterable encounter.
   `[game-data]` `[wiki]`
5. **Already inside seeded Valentino territory.** It is 206 m from
   `cc_rey_la_catrina` (Valentino-owned, `is_active = 0`), in a sub-district the
   seed gives them. `[game-data]`

Trade-off: La Catrina is a **front, not a fortress**. It has no executive office
or boardroom (Dicky Twister has both), and its canonical state is a gig target,
so the seat is deliberately exposed. With Campo Orta in prison, any 2077 seat is
a proxy; La Catrina is the most institution-shaped proxy the data supports.

### Alternate 1: **Dicky Twister** — Vista del Rey

Coordinates `-815.978, -81.593, 8.605` `[game-data]` site 370.

The strongest *operational* seat: a Valentino-owned club with a **named
Valentino owner** (Señor Ladrillo), 14 Valentino units, 10 doors, 5 patrol
routes, a backstage, a second floor and an office. It loses to La Catrina only on
institutional weight — a nightclub reads as a business front, and the wiki's DB
entry frames it as exactly that ("a respectable front for the gang's other,
shadier sidebiz"). Good HQ if the mod wants a social/recruitment seat instead of
a logistics seat.

### Alternate 2: **El Coyote Cojo** — the Glen

Coordinates `-1260.347, -984.175, 13.267` `[game-data]` `markers.jsonl`
`sq018_mp_el_coyote_entrance`.

The most **lore-central** Valentino-adjacent place in the game: Jackie Welles'
home bar, the site of *Heroes* and Mama Welles' ofrenda, a faction location, and
only 44 m from `cc_gle_senate_market`. It loses because **Mama Welles owns it**
and it is a community bar, not a gang operation: the Valentinos are regulars and
protectors, not proprietors. Use it as a legitimacy/hub control point, not the
org seat.

### Overruled / downgraded suggestions

- **Mercado Sonora as HQ** — best control-centre overlap in the whole faction
  (24.8 m from the only active Valentino CC) but it is an open-air underpass
  market with no enclosed seat. It is the test point instead.
- **Gustavo Orta's Apartment as HQ** — the wiki literally calls it "his base of
  operations", but the game makes it a decapitation target and the seed places it
  in a **Militech-owned Corpo Plaza sub-territory** (`cpz_militech_hq`), not
  Valentino turf. Unstable seat, bad map ownership.
- **The View as HQ** — a Valentino-tagged luxury mall between Corpo Plaza and
  the Glen, but no verified coordinate exists in the extract, so it cannot be
  seeded yet. Revisit if a mappin is resolved.
- **Moto Cielo as HQ** — mentioned-only lore (the bloodbath that made Padre a
  fixer); no in-game artifact and no coordinates.

---

## 6. Priority list of control points

Ranked by how well each place serves as a capturable Valentino control point.
"CC" = nearest entry in `data/control_centers.json` (all CCs, active or not);
distance is horizontal metres; owner is the CC's
`sub_territories.initial_owner_faction_id`.

| Rank | Control point | Rel. (1–5) | District / sub-district | Coordinates | Existing CC overlap | Why |
| ---: | --- | :---: | --- | --- | --- | --- |
| 1 | **La Catrina** | 5 | Heywood / VistaDelRey | `-1124.234, -663.598, 8.253` | `cc_rey_la_catrina`, 205.7 m (owner Valentinos) | HQ; funeral-home front for arms/drug/body logistics; chapel + morgue + garage |
| 2 | **Mercado Sonora** | 5 | Heywood / VistaDelRey | `-829.646, -400.347, 8.200` | `cc_rey_college_street`, **24.8 m** (Valentinos, **active**) | Test point; the barrio's market and meeting hub; 12 units, 7 patrols, 123 workspots |
| 3 | **Dicky Twister** | 5 | Heywood / VistaDelRey | `-815.978, -81.593, 8.605` | `cc_rey_college_street`, 299.8 m (Valentinos) | Named Valentino owner; club front with office/backstage; 14 units, 10 doors |
| 4 | **El Coyote Cojo** | 5 | Heywood / Glen | `-1260.347, -984.175, 13.267` | `cc_gle_senate_market`, 44.0 m (**owner 6th Street**) | Community heart, Jackie's bar, Padre's meeting place; not gang-owned — legitimacy anchor |
| 5 | **Valentino Alley** | 4 | Heywood / Glen | `-1636.997, -1228.885, 24.740` | `cc_gle_ventura_skyline`, **6.1 m** (Valentinos) | Gang alley/shrine corner, SOCA "Chapel"; 11 units incl. named bosses; nearly coincides with a CC |
| 6 | **El Pinche Pollo** | 4 | Heywood / Glen | `-1525.170, -1106.365, 13.098` | `cc_gle_hanford_overpass`, 154.4 m (**owner Kang Tao**) | Restaurant with gang-only 2nd floor and an office; 12 units; CC ownership is a seed artefact |
| 7 | **Jacked and Coke** | 4 | Heywood / VistaDelRey | `-926.445, -212.448, 7.673` | `cc_rey_delamain_block`, 176.8 m (Valentinos) | Dive bar with pachinko and back rooms; 13 units; Padre contract target |
| 8 | **Valentinos Auto Shop** | 4 | Heywood / Wellsprings | `-2345.589, -1007.419, 8.157` | `cc_spr_palm_view`, 144.8 m (Valentinos) | Chop shop / weapon mods; 11 units, 6 doors, garage + workshop |
| 9 | **Padre's Glen corner** | 4 | Heywood / Glen | `-1804.750, -1279.139, 21.870` | `cc_gle_ventura_skyline`, 175.7 m (Valentinos) | Fixer brokerage; the faction's contract economy; open plaza, no interior |
| 10 | **Bus Depot** | 3 | Heywood / Wellsprings | `-2078.184, -981.131, 7.450` | `cc_gle_reconciliation_park`, 115.4 m (Valentinos) | Arms staging base, 20 units (largest garrison); canonically abandoned after the gig |
| 11 | **Gustavo Orta's Apartment** | 3 | Heywood / VistaDelRey | `-975.638, 86.231, 48.350` | `cc_rey_delamain_block`, 300.4 m (Valentinos) | Secondary leader's base; 12 units; seed ownership says Militech/Corpo Plaza |

### Test control point for the first in-game test: **Mercado Sonora**

Why Mercado Sonora and not the HQ:

- **Closest usable CC overlap in the faction.** It is 24.8 m from
  `cc_rey_college_street`, the only `is_active = 1` Valentino control centre in
  Heywood, so a capture radius can be validated with zero new map plumbing.
  `[game-data]`
- **Clean ownership.** `default_faction_id = 3`, 12 Valentino roster units, 4
  guard areas and 7 patrol routes — every hook a capture/defence prototype
  needs. `[game-data]`
- **Proven fightable.** The NCPD scanner hustle `ma_hey_rey_06` ("Suspected
  Organized Crime Activity (Vista del Rey)") is the same site, with a named
  leader (Miguel Rodriguez) and an extracted victim community. `[game-data]`
  `[wiki]`
- **Not the HQ**, so the first test exercises capture on a non-seat.
- **Downside:** it is an open-air underpass market with no door records, so it
  tests area capture rather than interior gating. Fallback enclosed interior:
  **Dicky Twister** (10 doors, 5 patrols, 14 units, 300 m from its CC).

---

## 7. Per-sub-district count of lore-relevant locations

This is the number for yield balancing. It counts **distinct named places** the
gang owns, runs, protects or habitually occupies — not quest variants, not
generic occupied blocks. `Filler` is the deduped occupied-site count minus any
site already counted as a named place (`METHOD.md` §8).

| Sub-district | Named lore-relevant places | Which ones | Occupied sites (deduped) | Filler | Interiors |
| --- | ---: | --- | ---: | ---: | ---: |
| VistaDelRey | **5** (+1 landmark) | La Catrina, Mercado Sonora, Dicky Twister, Jacked and Coke, Gustavo Orta's Apartment (+ Megabuilding H5 as host landmark) | 9 | 4 | 4 |
| Glen | **4** | El Coyote Cojo, El Pinche Pollo, Valentino Alley, Padre's corner | 5 | 3 | 2 |
| Wellsprings | **2** | Valentinos Auto Shop, Bus Depot | 5 | 3 | 2 |
| RanchoCoronado | **0** | — | 1 | 1 | 0 |
| Downtown | **0** | — | 1 | 1 | 0 |
| **Total** | **11** | | 21 | 12 | 8 |

Reconciliation, in the pilot's accounting style:

- 24 raw roster sites (177 units). Three are single-unit cameos — a cyberpsycho,
  a monk and a bar customer — and are excluded: **21 occupied sites**.
- Nine of the eleven named places are site-backed (all five in Vista del Rey,
  El Pinche Pollo and Valentino Alley in the Glen, the auto shop and bus depot in
  Wellsprings). Two are marker-only: **El Coyote Cojo** and **Padre's corner**.
- 21 occupied sites − 9 site-backed named = **12 filler**. 9 site-backed + 2
  marker-only = **11 named**. `named + filler = 23 = 21 sites + 2 marker-only`,
  which reconciles.
- Vista del Rey's 9 sites include the `ma_hey_rey_01` anomaly (physically in
  JapanTown); it is counted as filler under its geocode token and flagged in
  §2.3/§3.2.

Interpretation for yield: Vista del Rey is the only sub-district with more than
two named places and should carry the faction's baseline business yield. The Glen
has fewer named places but the densest *community* value (El Coyote, Padre,
Valentino Alley). Wellsprings is industrial: only two named places, but each is a
full garage/workshop interior with high unit counts. Rancho Coronado and Downtown
are single contested outposts, not economy.

Unlocated named places **not** counted above (no verified coordinate):
The View, Eric's Motorcycles, Tirempire Auto Shop, Moto Cielo, Nuestra Señora De
Los Desamparados Cathedral, Sugar Skull Planet. If The View and Eric's are
resolved later, they most likely belong to Vista del Rey/the Glen and would
raise the named totals to 6 and 5 respectively.

---

## 8. Gaps and uncertainties

1. **El Coyote Cojo's sub-district is disputed between our own files.** The wiki
   says the Glen (corner of Los Lobos and M. Ebunike); the raw prefab path says
   `#c_heywood/glen/…`; the nearest seeded sub-territory is Senate & Market Plaza
   (Glen, 54 m). But `data/clean-slate/cast_and_hubs.json` labels it
   `heywood_vista_del_rey`. I follow the wiki + prefab path (Glen). The clean-slate
   string should be corrected.
2. **Three named places have no verified coordinate.** *The View* (a real mall in
   the world — `#cct_cpz_the_view_tr_codex` exists — but the raw extract has no
   position for it), *Eric's Motorcycles* and *Tirempire Auto Shop* (both named
   only by the wiki). They are catalogued but not counted. The View is the
   biggest omission: it is a Valentino-tagged luxury mall and would be a strong
   Vista del Rey/Corpo Plaza point if a mappin can be resolved.
3. **Moto Cielo, Nuestra Señora De Los Desamparados Cathedral and Sugar Skull
   Planet are lore-only.** They appear on the wiki's faction-location list
   (sourced to *The World of Cyberpunk 2077*) with no page and no game record
   found. Keep them `[lore]`/`TBD`; do not seed.
4. **Control-centre ownership conflicts with lore at two points.**
   `cc_gle_senate_market` (44 m from El Coyote) is owned by **6th Street**
   (faction 4), and `cc_gle_hanford_overpass` (154 m from El Pinche Pollo) is
   owned by **Kang Tao** (faction 22). The first is plausible contested turf; the
   second looks like a seed artefact and should be re-owned.
5. **Gustavo Orta's Apartment is seed-owned by Militech.** Site 369 sits in
   `cpz_militech_hq` (`sub_territory_id 77`, owner 21), while the wiki places it
   in Vista del Rey and even notes that the border makes it "appear as Corpo
   Plaza". This is a real engine ambiguity, but the seed should not read
   "Militech owns a Valentino leader's flat".
6. **`ma_hey_gle_05` (Danilo Ruiz) is seed-owned by Arasaka.** Site 44 sits in
   `cpz_ring_road_west` (`sub_territory_id 79`) at `(-1730, -223, -13.5)` — a
   sewer/underground level on the Glen/Corpo Plaza boundary. Geocode and prefab
   path say Glen.
7. **`ma_hey_rey_01` is a cross-border anomaly.** Five Valentino units at
   `(-837.6, 227.6)`, inside `jpn_silk_road` (JapanTown), on a `rey`-token site.
   It mirrors the pilot's `rey_09` anomaly. Do not treat it as a Vista del Rey
   holding.
8. **The Bus Depot is canonically abandoned after *On a Tight Leash*.** The wiki
   infobox says "Valentinos (formerly)" and the gig ends with the gang leaving.
   For a pre-campaign seed this is ambiguous: either seed it as an arms-staging
   point or as a contested/empty site. I counted it as named but ranked it 10.
9. **No vendor or interior inventory proves "what a business sells".** Business
   descriptions come from wiki infoboxes and named rooms (chapel, morgue, bar,
   garage, pachinko workspots), not from vendor data.
10. **The sub-district presence table is presence, not ownership.** The three
    core barrios dominate; the peripheral rows are single scenes. JapanTown and
    Corpo Plaza appear only through two reused/border prefabs.
11. **Interior coverage is partial.** `is_interior` is set on only one Valentino
    site (site 234, not counted). Every "Interior? Yes" above is proven from
    interior node names, not from the flag — absence of the flag is not evidence.

---

## 9. Sources

- Local: `dist/extract/areas.jsonl`, `dist/extract/markers.jsonl`,
  `dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_{0,1,2}.streamingsector.json`,
  `data/sites/{sites,communities,rosters,guards,triggers,spots,patrols,doors,suitabilities}.json`,
  `data/{districts,factions,control_centers,sub_territories,landmarks,spawn_points}.json`,
  `data/clean-slate/cast_and_hubs.json` (used only for the El Coyote discrepancy).
- Wiki: [Valentinos](https://cyberpunk.fandom.com/wiki/Valentinos),
  [La Catrina](https://cyberpunk.fandom.com/wiki/La_Catrina),
  [Dicky Twister](https://cyberpunk.fandom.com/wiki/Dicky_Twister),
  [El Coyote Cojo](https://cyberpunk.fandom.com/wiki/El_Coyote_Cojo),
  [El Pinche Pollo](https://cyberpunk.fandom.com/wiki/El_Pinche_Pollo),
  [Mercado Sonora](https://cyberpunk.fandom.com/wiki/Mercado_Sonora),
  [Jacked and Coke](https://cyberpunk.fandom.com/wiki/Jacked_and_Coke),
  [Gustavo Orta's Apartment](https://cyberpunk.fandom.com/wiki/Gustavo_Orta%27s_Apartment),
  [Valentinos Auto Shop](https://cyberpunk.fandom.com/wiki/Valentinos_Auto_Shop),
  [Bus Depot](https://cyberpunk.fandom.com/wiki/Bus_Depot),
  [Eric's Motorcycles](https://cyberpunk.fandom.com/wiki/Eric%27s_Motorcycles),
  [The View](https://cyberpunk.fandom.com/wiki/The_View),
  [Tirempire Auto Shop](https://cyberpunk.fandom.com/wiki/Tirempire_Auto_Shop),
  [Reconciliation Park](https://cyberpunk.fandom.com/wiki/Reconciliation_Park),
  [Megabuilding H5](https://cyberpunk.fandom.com/wiki/Megabuilding_H5),
  [Moto Cielo](https://cyberpunk.fandom.com/wiki/Moto_Cielo),
  [Sebastian Ibarra](https://cyberpunk.fandom.com/wiki/Sebastian_Ibarra).
- Gig / activity pages used for the `baseid` join:
  [Gig: Jeopardy](https://cyberpunk.fandom.com/wiki/Gig:_Jeopardy),
  [Gig: Sr. Ladrillo's Private Collection](https://cyberpunk.fandom.com/wiki/Gig:_Sr._Ladrillo%27s_Private_Collection),
  [Gig: Old Friends](https://cyberpunk.fandom.com/wiki/Gig:_Old_Friends),
  [Gig: Bring Me the Head of Gustavo Orta](https://cyberpunk.fandom.com/wiki/Gig:_Bring_Me_the_Head_of_Gustavo_Orta),
  [Gig: Fifth Column](https://cyberpunk.fandom.com/wiki/Gig:_Fifth_Column),
  [Gig: The Lord Giveth and Taketh Away](https://cyberpunk.fandom.com/wiki/Gig:_The_Lord_Giveth_and_Taketh_Away),
  [Gig: On a Tight Leash](https://cyberpunk.fandom.com/wiki/Gig:_On_a_Tight_Leash),
  [Suspected Organized Crime Activity (Vista del Rey)](https://cyberpunk.fandom.com/wiki/Suspected_Organized_Crime_Activity_(Vista_del_Rey)),
  [Suspected Organized Crime Activity: Chapel](https://cyberpunk.fandom.com/wiki/Suspected_Organized_Crime_Activity:_Chapel).

---

## 10. Machine-readable block

Strict JSON for seeding (contract in [`METHOD.md`](./METHOD.md) §10). Every
coordinate was re-verified against the local record named in `source` on
2026-11-25; none came from the wiki.

```json
{
  "faction_code": "valentinos",
  "hq": {"name": "La Catrina", "district": "Heywood", "sub_district": "VistaDelRey", "x": -1124.234, "y": -663.598, "z": 8.253, "source": "data/sites/sites.json site 371 sts_hey_rey_06", "confidence": "game-data+wiki"},
  "alternate_hqs": [
    {"name": "Dicky Twister", "district": "Heywood", "sub_district": "VistaDelRey", "x": -815.978, "y": -81.593, "z": 8.605, "source": "data/sites/sites.json site 370 sts_hey_rey_02", "confidence": "game-data+wiki"},
    {"name": "El Coyote Cojo", "district": "Heywood", "sub_district": "Glen", "x": -1260.347, "y": -984.175, "z": 13.267, "source": "dist/extract/markers.jsonl sq018_mp_el_coyote_entrance", "confidence": "game-data+wiki"}
  ],
  "test_control_point": {"name": "Mercado Sonora", "district": "Heywood", "sub_district": "VistaDelRey", "x": -829.646, "y": -400.347, "z": 8.2, "source": "data/sites/sites.json site 66 ma_hey_rey_06", "confidence": "game-data+wiki"},
  "control_points": [
    {"rank": 1, "name": "La Catrina", "type": "funeral_home", "relevance": 5, "district": "Heywood", "sub_district": "VistaDelRey", "x": -1124.234, "y": -663.598, "z": 8.253, "source": "data/sites/sites.json site 371 sts_hey_rey_06", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["smuggling", "drugs", "arms", "retail"], "nearest_cc_code": "cc_rey_la_catrina", "nearest_cc_m": 205.7},
    {"rank": 2, "name": "Mercado Sonora", "type": "market", "relevance": 5, "district": "Heywood", "sub_district": "VistaDelRey", "x": -829.646, "y": -400.347, "z": 8.2, "source": "data/sites/sites.json site 66 ma_hey_rey_06", "confidence": "game-data+wiki", "interior": false, "revenue_streams": ["retail", "drugs", "protection", "smuggling"], "nearest_cc_code": "cc_rey_college_street", "nearest_cc_m": 24.8},
    {"rank": 3, "name": "Dicky Twister", "type": "club", "relevance": 5, "district": "Heywood", "sub_district": "VistaDelRey", "x": -815.978, "y": -81.593, "z": 8.605, "source": "data/sites/sites.json site 370 sts_hey_rey_02", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["food_drink", "sex_work", "protection"], "nearest_cc_code": "cc_rey_college_street", "nearest_cc_m": 299.8},
    {"rank": 4, "name": "El Coyote Cojo", "type": "bar", "relevance": 5, "district": "Heywood", "sub_district": "Glen", "x": -1260.347, "y": -984.175, "z": 13.267, "source": "dist/extract/markers.jsonl sq018_mp_el_coyote_entrance", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["food_drink", "protection", "fixer_brokerage"], "nearest_cc_code": "cc_gle_senate_market", "nearest_cc_m": 44.0},
    {"rank": 5, "name": "Valentino Alley", "type": "alley", "relevance": 4, "district": "Heywood", "sub_district": "Glen", "x": -1636.997, "y": -1228.885, "z": 24.74, "source": "data/sites/sites.json site 42 ma_hey_gle_02", "confidence": "game-data+inferred+wiki", "interior": false, "revenue_streams": ["protection", "drugs"], "nearest_cc_code": "cc_gle_ventura_skyline", "nearest_cc_m": 6.1},
    {"rank": 6, "name": "El Pinche Pollo", "type": "restaurant", "relevance": 4, "district": "Heywood", "sub_district": "Glen", "x": -1525.17, "y": -1106.365, "z": 13.098, "source": "data/sites/sites.json site 366 sts_hey_gle_04", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["food_drink", "protection"], "nearest_cc_code": "cc_gle_hanford_overpass", "nearest_cc_m": 154.4},
    {"rank": 7, "name": "Jacked and Coke", "type": "bar", "relevance": 4, "district": "Heywood", "sub_district": "VistaDelRey", "x": -926.445, "y": -212.448, "z": 7.673, "source": "data/sites/sites.json site 372 sts_hey_rey_08", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["food_drink", "gambling", "drugs"], "nearest_cc_code": "cc_rey_delamain_block", "nearest_cc_m": 176.8},
    {"rank": 8, "name": "Valentinos Auto Shop", "type": "autoshop", "relevance": 4, "district": "Heywood", "sub_district": "Wellsprings", "x": -2345.589, "y": -1007.419, "z": 8.157, "source": "data/sites/sites.json site 375 sts_hey_spr_03", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["vehicles_chop", "arms", "smuggling"], "nearest_cc_code": "cc_spr_palm_view", "nearest_cc_m": 144.8},
    {"rank": 9, "name": "Padre's Glen corner", "type": "fixer_hq", "relevance": 4, "district": "Heywood", "sub_district": "Glen", "x": -1804.75, "y": -1279.139, "z": 21.87, "source": "dist/extract/markers.jsonl padre_sm_default", "confidence": "game-data+wiki", "interior": false, "revenue_streams": ["fixer_brokerage", "protection"], "nearest_cc_code": "cc_gle_ventura_skyline", "nearest_cc_m": 175.7},
    {"rank": 10, "name": "Bus Depot", "type": "depot", "relevance": 3, "district": "Heywood", "sub_district": "Wellsprings", "x": -2078.184, "y": -981.131, "z": 7.45, "source": "data/sites/sites.json site 374 sts_hey_spr_01", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["smuggling", "arms", "vehicles_chop"], "nearest_cc_code": "cc_gle_reconciliation_park", "nearest_cc_m": 115.4},
    {"rank": 11, "name": "Gustavo Orta's Apartment", "type": "apartment", "relevance": 3, "district": "Heywood", "sub_district": "VistaDelRey", "x": -975.638, "y": 86.231, "z": 48.35, "source": "data/sites/sites.json site 369 sts_hey_rey_01", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["protection"], "nearest_cc_code": "cc_rey_delamain_block", "nearest_cc_m": 300.4}
  ],
  "subdistrict_counts": {
    "VistaDelRey": {"named": 5, "filler": 4},
    "Glen": {"named": 4, "filler": 3},
    "Wellsprings": {"named": 2, "filler": 3},
    "RanchoCoronado": {"named": 0, "filler": 1},
    "Downtown": {"named": 0, "filler": 1}
  }
}
```
