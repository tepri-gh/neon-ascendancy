# 6th Street — Lore-Relevant Control Points

Status: faction research run, 2026-11-25. One faction, one document.
Scope: replace the generic ~5-control-centres-per-sub-district grid with places
6th Street actually owns, runs or garrisons, with an honest count per
sub-district. Method: this doc conforms to [`METHOD.md`](./METHOD.md); snippets,
wiki rules, revenue codes and the JSON contract live there.

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

6th Street is Night City's patriotic ex-military gang: ≈2,300 members in 2077,
"Medium" threat, founded in the late 2020s by Fourth Corporate War veterans and
taken over in a late-2076 coup by Will Gunner, who killed "General" Rick Morton
and purged his loyalists. `[wiki]` Its 2077 headquarters is in **Arroyo, Santo
Domingo**, and it controls most of the district; subordinate districts have
their own local HQs that patrol and watch the gang's facilities. `[wiki]`

Its economy is a protection-and-logistics racket wearing a uniform:

- **Protection / ersatz law** — the founding business. Rancho Coronado's
  security is explicitly overseen by the gang because the NCPD is spread too
  thin; local businesses pay tribute. `[wiki]`
- **Arms** — gun smuggling and military hardware, historically supplied by
  **Militech** and **Kendachi**; in 2077 a secret Kendachi joint project
  ("Arsenal") designs a new weapon line. `[wiki]`
- **Drugs** — drug manufacturing and distribution, including a beta-acid lab in
  the Dewdrop Inn and Darius Miles' drug ring. `[wiki]` `[game-data]`
- **Vehicles** — stolen and modified cars; the gang's techies run "many garages
  and workshops around the city". `[wiki]`
- **Smuggling / robbery** — nomad logistics, container freight, extortion,
  robbery, murder. `[wiki]`
- **Combat Cab** — a combat-taxi service affiliated with the gang, popular with
  edgerunners. `[wiki]`
- **Propaganda** — a server farm pumping out pro-Peralez / anti-Holt material,
  which is `media` revenue in practice. `[wiki]`

The weight sits in **RanchoCoronado (32 community areas, 27 spawn points, 12
sites)** and **Arroyo (27 areas, 25 spawn points, 7 sites)** — 132 of 183 roster
units. Everything else is either a Heywood/Westbrook outpost or a quest cameo.
The single richest interior cluster is in northern Arroyo: the Megabuilding H6
hideout, the Dewdrop Inn lab and the Red White warehouse all sit inside a
~500 m triangle.

---

## 2. Territory

### 2.1 Districts

Wiki locations are Santo Domingo, Heywood and Westbrook. Evidence in three
kinds:

| Evidence kind | Result |
| --- | --- |
| (a) Wiki/lore | HQ in Arroyo (2077); controls most of Santo Domingo; Vista del Rey is in an escalating turf war with the Valentinos; Charter Hill is contested; "other districts under their control had their own local HQs". `[wiki]` |
| (b) Vanilla map gang panel | `data/districts.json`: SantoDomingo `["SixthStreet"]`; Heywood `["Valentinos"]`; Westbrook `["TheMox","TygerClaws"]`; Watson `["Maelstrom","TygerClaws"]`; Pacifica `["VoodooBoys","Animals"]`; Dogtown `["Barghest"]`. The sub-district panel from earlier repo research (`docs/research/factions-gangs-territories.md` §2.2) lists 6th Street on **Arroyo, RanchoCoronado, CharterHill and VistaDelRey**. |
| (c) Game-data counts | 96 community areas contain 6th Street spawns (86 dominant); 79 spawn points; 29 occupied sites / 183 roster units. |

### 2.2 Sub-district presence

Counts are from `dist/extract/areas.jsonl` (any area whose `faction_counts`
contains `sixth_street`; "dominant" means `dominant_faction == sixth_street`),
`data/spawn_points.json` (`faction_id == 4`, counted by `sub_territory_id`), and
`data/sites/{sites,rosters}.json` (deduped sites that are faction-owned or hold
at least one 6th Street roster entry).

| Sub-district | District | (a) Lore | (b) Vanilla panel | (c) 6th areas (dominant) | (c) 6th spawn pts | 6th-occupied sites* |
| --- | --- | --- | --- | ---: | ---: | ---: |
| Arroyo | SantoDomingo | **HQ district**, industrial heart | 6th Street | 27 (26) | 25 | 7 |
| RanchoCoronado | SantoDomingo | security overseen by 6th | 6th Street | 32 (32) | 27 | 12 |
| Glen | Heywood | minor; one 6th autoshop | Valentinos | 11 (9) | 9 | 3 |
| VistaDelRey | Heywood | turf war with Valentinos | Valentinos, 6th Street | 3 (2) | 3 | 1 |
| CharterHill | Westbrook | contest with Tyger Claws | Tyger Claws, 6th Street | 6 (5) | 5 | 1 |
| Northside | Watson | incidental only (hidden stashes) | Maelstrom, Mox, Scavs | 0 | 0 | 4 |
| Dogtown | Dogtown | Phantom Liberty quest cameo | Barghest | 8 (6) | 3 | 0 |
| Coastview | Pacifica | Phantom Liberty quest cameo | Voodoo Boys, Animals | 1 (1) | 3 | 1 |
| WestWindEstate | Pacifica | Phantom Liberty ambush cameo | Voodoo Boys, Animals | 5 (4) | 2 | 0 |
| Badlands | Badlands | one quest community | Aldecaldos, Wraiths | 1 (1) | 1 | 0 |
| Kabuki | Watson | single stray Lizzie's area | Tyger Claws, Maelstrom, Mox | 1 (0) | 0 | 0 |
| NorthOaks | Westbrook | single race area | — | 1 (0) | 0 | 0 |
| Wellsprings | Heywood | incidental | Valentinos | 0 | 1 | 0 |

\* Deduped `data/sites/sites.json` rows with `default_faction_id == 4` **or** at
least one roster entry resolving to 6th Street; variants within 25 m are
collapsed. No 6th Street site variants were found (29 candidates → 29 kept).

**Reading the counts.** RanchoCoronado leads on raw presence because the gang
polices the whole suburb (32 of 32 areas are 6th-dominant). Arroyo leads on
*interiors and named places*. The per-sub-district numbers that matter for yield
balancing are in §7, not here.

**Attribution caveat.** `areas.jsonl.district_code` is derived from the sector
path and is wrong for quest communities in `always_loaded_*` (METHOD §2.2/§2.3).
I attributed 96 rows as follows: 38 by geocode token, 49 by nearest geocoded
site within 400 m, 8 Dogtown rows by `district_code == "dogtown"`, and 1 by
nearest sub-territory centroid (`{q103_com_maelstrom_roadhouse}`, a Badlands
quest community). Rows that move across district lines this way include
`{mq008_com_6th_street_party}` (labelled `santo_domingo`, correctly Rancho),
`{sa_ep1_135_*}` (labelled `heywood`, sits in the Glen) and
`{wat_kab_com_lizzies_default}` (labelled `watson`, correctly Kabuki). Do not
aggregate the raw file by `district_code`.

---

## 3. Location catalog

Coordinates are world-space metres, `Z` up. "Interior?" means the game has a
distinct interior cell/sector for it — either the `is_interior` flag or named
interior node refs/doors (the flag is sparse: only 1 of these 29 sites has it
set).

| # | Name | Type | District / sub-district | Interior? | Business? (what it earns) | Coordinates (x, y, z) | Coordinate source record | Linked communities / sites | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **6th Street hideout, Megabuilding H6 floor 19** | Fortified hideout / netrunner den | SantoDomingo / Arroyo | Yes — whole 19th floor via lift | No retail: weapons jailbreaking, stolen Militech hardware, netrunning | `-199.0, -843.5, 259.2` (floor anchor); lift ground `-168.8, -871.2, 11.5`; lift 19F `-168.1, -871.0, 263.2` | `data/sites/sites.json` site 384 `sts_std_arr_11`; `markers.jsonl` `sts_std_arr_11_elevator_marker`, `sts_std_arr_11_elevator_marker_}001` | `#arr_11_com` (hash `2974118600773013074`, 12 entries); `#arr_11_reinforcement` (`1021270802476162406`); `#arr_11_tenant_com` (`16933611079945276002`); gig *Hacking the Hacker* baseid `sts_std_arr_11` | `[game-data]` `[wiki]` |
| 2 | **Dewdrop Inn** | Motel + second-floor drug lab | SantoDomingo / Arroyo | Yes — reception, rooms 103/203, lab | Yes: rooms for rent; beta-acid production; a place to lay low if you are on good terms with the gang | `-573.5, -821.5, 8.2` | `data/sites/sites.json` site 379 `sts_std_arr_01` | `#arr_01_com_crowd` (`14361855172917626796`, 9); `#arr_01_com_combat` (`14857625174971282591`, 8); gig *Serious Side Effects* baseid `sts_std_arr_01`; wiki infobox `gangs = 6th Street` | `[game-data]` `[wiki]` |
| 3 | **Red White Used Warehouse** | Warehouse / stash + netrunner den | SantoDomingo / Arroyo | Yes — flag `is_interior=1`; two floors, roof door | Yes: fencing "larger items", storing hot hardware; netrunner chair | `-573.6, -1182.9, 7.7` | `data/sites/sites.json` site 382 `sts_std_arr_06` | `#arr_06_com` (`11345424928675936529`, 7); `#arr_06_com_corpo` (`15970220439262687998`, 7); `#arr_06_reinforcements_kang_tao_com` (`10180939200453154933`); gig *Nasty Hangover* baseid `sts_std_arr_06` | `[game-data]` `[wiki]` |
| 4 | **Wicked Tires Autoshop** | Autoshop / vehicle workshop | Heywood / Glen | Yes — garage, two lifts, office upstairs | Yes: car repair and custom builds for the gang; bootleg parts | `-1398.9, -1279.7, 46.9` | `data/sites/sites.json` site 368 `sts_hey_gle_06` | `#gle_06_community` (`13612149369523800131`, 8); `#gle_06_com_jake` (`12157566390393856893`, 2); gig *Life's Work* baseid `sts_hey_gle_06` | `[game-data]` `[wiki]` |
| 5 | **Kendachi Factory (Almunecar)** | Weapons factory — "Arsenal" partner site | SantoDomingo / Arroyo | Yes — garage, office, factory floor | Yes: Kendachi monoweapons; secret 6th Street product line | `-282.1, -1721.0, 7.5` | `data/sites/sites.json` site 381 `sts_std_arr_05` | `#arr_05_com_enemies` (`16483904473891227462`, 8); `#arr_05_com` (`2263445092403245155`); gig *Breaking News* baseid `sts_std_arr_05`; shard `[IMPORTANT] "Arsenal"` | `[game-data]` `[wiki]` |
| 6 | **Red Dirt Bar** | Rock bar / landmark | SantoDomingo / Arroyo | Yes — bar interior | Yes: beer, food, live music; gang hangs out in a 6th-owned crossroads; protection income | `-725.1, -991.9, 9.3` (mappin); interior scene `-732.7, -988.5, 8.0`; behind-bar `-724.5, -997.8, 8.4` | `markers.jsonl` `sq011_mp_red_dirt`; `mirror_sm_scene_red_dirt`; `std_arr_foodshop_01_beer_behind_bar` | Sub-territory 55 `arr_red_dirt_cross` "Red Dirt Crossroads" (seed owner 6th Street); quest *A Like Supreme* | coords `[game-data]`; name `[wiki]`; ownership `[inferred]` (not 6th-run, 6th-controlled crossroads) |
| 7 | **Darius Miles' drug lab (Hargreaves St)** | Drug lab / industrial outpost | SantoDomingo / Arroyo | No — outdoor outpost with guard areas | Yes: drug manufacture and wholesale | `-614.2, -1038.1, 7.4` | `data/sites/sites.json` site 125 `ma_std_arr_03` | `#ma_std_arr_03_com` (`13349619226231133820`, 8); `#ma_std_arr_03_reinforcements` (`17899161144350988837`, 5); NCPD *Suspected Organized Crime Activity (Arroyo)* baseid `ma_std_arr_03` | `[game-data]` `[wiki]` |
| 8 | **Propaganda garage, Oak St** | Garage / server farm | SantoDomingo / RanchoCoronado | Yes — enclosed garage with server room | Yes: political propaganda for Peralez, anti-Holt media | `245.2, -1074.7, 21.4` | `data/sites/sites.json` site 389 `sts_std_rcr_04` | `#rcr_04_com_combat` (`5509003469920229578`, 19); gig *Error 404* baseid `sts_std_rcr_04` | `[game-data]` `[wiki]` |
| 9 | **Kendal Park (Rancho Coronado Public Park)** | Public park / hangout | SantoDomingo / RanchoCoronado | No — open park | Partial: neighborhood control, street-level dealing and betting; contested with Tyger Claws | `292.5, -986.7, 20.5` (6th Street community anchor); park centre CC `531.6, -954.9, 28.6` | `data/sites/sites.json` site 150 `ma_std_rcr_05`; `data/control_centers.json` `cc_rcr_kendal_park` | `#ma_std_rcr_05_sixthstreet_com` (`15166712447540804229`, 2); `#ma_std_rcr_05_tyger_com` (`13132044448851607433`, 4); sub-territory 60 `rcr_kendal_park` | coords `[game-data]`; name link `[inferred]` (sub-territory name + park streets); ownership contested |
| 10 | **Acorn Towers parking lot (Crockett St)** | Parking lot / fencing yard | Westbrook / CharterHill | No — open parking lot | Yes: stolen car + bootleg Samurai recording; goods holding | `375.3, -400.1, 2.6` | `data/sites/sites.json` site 416 `sts_wbr_hil_06` | `#hil_06_com` (`16968409223605646142`, 12); `#hil_06_client_com` (`17154026491449163062`, 2); gig *Family Heirloom* baseid `sts_wbr_hil_06` | `[game-data]` `[wiki]` |
| 11 | **Stadium Love rooftop (Captain Sherman's party)** | Rooftop party / recruitment and betting site | SantoDomingo / RanchoCoronado | No — residential rooftops | Yes: drinking, shooting contest with betting; recruitment pitch | `503.0, -2128.7, 27.4` (shooting contest); party `495.7, -2143.4, 27.3` | `markers.jsonl` `mq008_02_sm_shooting_contest`, `mq008_01_sm_party_chats`; `areas.jsonl` `{mq008_com_6th_street_party}` (`445098964158899642`, 6) | `{std_rcr_6th_street_party_com}` (`16158794172041309344`, 2); minor job *Stadium Love* baseid `mq008_party` | coords `[game-data]`; place name `[inferred]` from job/community |
| 12 | Megabuilding H4 Plaza | Megabuilding / landmark | SantoDomingo / Arroyo | Building yes; plaza no | No — residential/industrial; 6th Street turf around a quarantined megablock | `-943.9, -1508.7, 25.6` (occupied site); plaza CC `-951.7, -1502.8, 25.6` | `data/sites/sites.json` site 129 `ma_std_arr_07`; `data/control_centers.json` `cc_arr_megabuilding_h4` | Seeded sub-territory 54 `arr_megabuilding_h4` (owner 6th); sites 127, 129 | coords `[game-data]`; **landmark row, not counted in §7** |
| 13 | Megabuilding H7 | Megabuilding / sealed 6th Street post | SantoDomingo / RanchoCoronado | Unknown — "closed state" | No | `TBD` | — | No marker, site or community record found | `[wiki]` only; **catalog-only, not seeded** |

### 3.1 How the name→coordinate links were proven

The extractor keeps interior node names (`data/sites/{guards,triggers,spots,patrols,doors}.json`),
and the wiki's gig pages carry a `baseid` that is the site code. Joining those
two is what turns `sts_std_arr_06` into "Red White Used Warehouse":

- **Site 384** (`sts_std_arr_11`) matches gig *Hacking the Hacker* baseid
  `sts_std_arr_11` ("6th Street hideout on MLK Blvd", Megabuilding H6, 19th
  floor). Nodes: `#arr_11_inside_lab`, `#arr_11_rma_lucius_offcie`,
  `#arr_11_elevator_down`, `#arr_11_rma_sniper_nest`, `#arr_rma_balcony`; its two
  lift markers sit at z=11.5 (ground) and z=263.2 (floor 19). Roster includes
  `Character.sts_std_arr_11_lucius` (Lucius Thoran) and a netrunner.
- **Site 379** (`sts_std_arr_01`) matches gig *Serious Side Effects* baseid
  `sts_std_arr_01` at the **Dewdrop Inn** ("rooms 103/203", "the lab"). Nodes:
  `#arr_01_rma_chem_lab`, `#arr_01_ws_drug_producer_001`,
  `#arr_01_ws_cleaner`, `#arr_01_spl_receptionist_patrol`, nine door refs.
  The wiki infobox independently says `gangs = 6th Street`.
- **Site 382** (`sts_std_arr_06`) matches gig *Nasty Hangover* baseid
  `sts_std_arr_06` ("Enter the 6th Street warehouse", Hargreaves St). Its
  computer subpage names it **Red White Used Warehouse** and describes a
  portable terminal by a netrunner chair on the second floor — matching
  `#arr_06_roof_door`, `#arr_06_main_gate`, `#arr_06_tr_factory`. `is_interior=1`.
- **Site 368** (`sts_hey_gle_06`) matches gig *Life's Work* baseid
  `sts_hey_gle_06` at **Wicked Tires Autoshop**. Nodes: `#gle_06_tr_jake`,
  `#gle_06_ws_jake`, `#gle_06_tr_inside_garage`, `#gle_06_tr_enter_office`.
- **Site 389** (`sts_std_rcr_04`) matches gig *Error 404* baseid
  `sts_std_rcr_04` ("garage on Oak St."). Nodes: `#rcr_04_tr_server_garage`,
  `#rcr_04_tr_garage_area`, `#rcr_04_ga_roof`.
- **Site 416** (`sts_wbr_hil_06`) matches gig *Family Heirloom* baseid
  `sts_wbr_hil_06` (Acorn Towers parking lot on Crockett St.). Nodes:
  `#hil_06_tr_bootleg`, `#hil_06_tr_car_deliver`, `#hil_06_tr_car_mappins`.
- **Site 125** (`ma_std_arr_03`) matches NCPD *Suspected Organized Crime
  Activity (Arroyo)* baseid `ma_std_arr_03`, whose dispatcher names Darius Miles
  and his drug-manufacturing ring on Hargreaves Street.
- **Site 381** (`sts_std_arr_05`) matches gig *Breaking News* baseid
  `sts_std_arr_05` at **Kendachi Factory (Almunecar)**. Nodes:
  `#arr_05_ws_fox_car`, `#arr_05_tr_garage`, `#arr_05_tr_factory_parking`; the
  shard `[IMPORTANT] "Arsenal"` is on the garage office desk.
- **Red Dirt** is marker-only: `sq011_mp_red_dirt` is the quest mappin,
  `mirror_sm_scene_red_dirt` the interior scene and
  `std_arr_foodshop_01_beer_behind_bar` the bar workspot. The seed sub-territory
  `arr_red_dirt_cross` is 6th-owned and named after the bar. The bar itself is
  not 6th-run — it is a fixture of their crossroads.
- **Kendal Park** is a name inference: site 150 `ma_std_rcr_05` carries the
  `#ma_std_rcr_05_sixthstreet_com` community at `(293.8, -989.6)`, and its
  sub-territory is `rcr_kendal_park` ("Kendal Park Courts"). The wiki park sits
  on Kendal/Pheasant/Manzanita/Sequoia. No record literally says "Kendal Park".

### 3.2 6th-occupied generic sites (filler pool)

`data/sites/suitabilities.json` tags sites with gameplay affordances. These
sites are unnamed but are the honest filler pool. Top sites by roster strength:

| Site | Code | Sub-district | Interior | Suitability tags | Units | Coordinates | Note |
| --- | --- | --- | --- | --- | ---: | --- | --- |
| 129 | `ma_std_arr_07` | Arroyo | no | raid_target, rooftop_access, vehicle_bay | 6 | `-943.9, -1508.7, 25.6` | H4 Plaza scanner hustle |
| 127 | `ma_std_arr_05` | Arroyo | no | raid_target | 5 | `-848.9, -1354.0, 7.8` | H4 Plaza scanner hustle |
| 131 | `ma_std_arr_09` | Arroyo | no | raid_target, rooftop_access, vehicle_bay | 5 | `-883.5, -1008.3, 11.6` | Red Dirt Crossroads car hustle |
| 153 | `ma_std_rcr_08` | RanchoCoronado | no | arms_cache, branch_office, officer_site, raid_target, vehicle_bay | 13 | `-157.0, -2169.7, 5.8` | Almunecar highway outpost |
| 154 | `ma_std_rcr_09` | RanchoCoronado | no | officer_site, raid_target, rooftop_access, vehicle_bay | 6 | `998.3, -856.4, 29.9` | Rancho East Ridge |
| 152 | `ma_std_rcr_07` | RanchoCoronado | no | hostage_site, raid_target, vehicle_bay | 6 | `-78.5, -1897.3, 2.6` | execution scene |
| 388 | `sts_std_rcr_03` | RanchoCoronado | no | club, hostage_site, officer_site, raid_target, rooftop_access, vehicle_bay | 6 | `446.9, -1267.6, 28.7` | Flavio's house (*Going-away Party*) — 6th hit scene |
| 146 | `ma_std_rcr_01` | RanchoCoronado | no | hostage_site, raid_target, rooftop_access | 5 | `242.1, -1442.8, 9.6` | gang-watch robbery |
| 166 | `ma_std_rcr_13` | RanchoCoronado | no | arms_cache, market_stall, raid_target, rooftop_access, vehicle_bay | 5 | `178.8, -1966.9, 14.9` | hidden stash |
| 147 | `ma_std_rcr_02` | RanchoCoronado | no | raid_target, rooftop_access | 4 | `464.7, -1433.3, 19.8` | asset recovery |
| 167 | `ma_std_rcr_14` | RanchoCoronado | no | arms_cache, hostage_site, raid_target, rooftop_access, vehicle_bay | 4 | `189.1, -1507.6, 8.8` | scanner hustle |
| 155 | `ma_std_rcr_10` | RanchoCoronado | no | arms_cache, raid_target, rooftop_access | 3 | `574.8, -2133.4, 38.5` | southeastern stash |
| 165 | `ma_std_rcr_12` | RanchoCoronado | no | arms_cache, raid_target, sewer_access | 3 | `49.3, -1804.5, -10.2` | sewer stash |
| 47 | `ma_hey_gle_09` | Glen | no | raid_target, rooftop_access | 6 | `-1249.5, -946.6, 31.4` | Quincy Rivers scanner hustle |
| 57 | `ma_hey_gle_11` | Glen | no | raid_target, rooftop_access | 4 | `-1567.8, -1045.1, 9.2` | 6th vs Valentinos shootout |
| 65 | `ma_hey_rey_05` | VistaDelRey | no | club, hostage_site, officer_site, raid_target, rooftop_access, vehicle_bay | 4 | `-959.8, -785.9, 8.2` | bar robbery; NCPD-owned site |
| 225/231/236/238 | `ma_wat_nid_12/19/26/30` | Northside | no | arms_cache, camera_net, … | 3 each | various Watson | reused `rcr_sixthstreet_*` records in hidden-stash activities |
| 359 | `sts_ep1_07` | Coastview | no | officer_site, rooftop_access | 5 | `-1401.3, -2013.2, 85.2` | *Roads to Redemption* weapons factory (Phantom Liberty) |

Treat the tags as gameplay affordances, not lore. They tell you a place *can*
host a stash/club/chop-shop; they do not prove the gang runs one there.

---

## 4. Economic structure

### 4.1 Revenue streams → catalog locations

| Revenue stream | Code(s) | Catalog locations that produce it | Evidence / notes |
| --- | --- | --- | --- |
| Protection, tribute, "security" | `protection` | Dewdrop Inn (2); Red Dirt (6); Kendal Park (9); Oak St garage (8); Rancho neighborhoods | Wiki: extortion, protection money, forced tribute from small businesses. Rancho's security is "overseen by the 6th Street gang". `[wiki]` |
| Licensed/ersatz security services | `security_services` | Rancho Coronado and Arroyo patrol areas; 2045 private-law-enforcement heritage | The gang began as a deputized security contractor; in 2077 it is the de facto law in its neighborhoods. `[wiki]` |
| Arms dealing, gun running, weapons R&D | `arms`, `rnd` | Kendachi Factory Almunecar (5); Megabuilding H6 hideout (1); Red White warehouse (3) | Militech/Kendachi supply; the H6 cell "jumped a Militech transport" and jailbreaks corpo weapons; "Arsenal" is a Kendachi joint project. `[wiki]` |
| Drugs (manufacture and wholesale) | `drugs` | Dewdrop Inn beta-acid lab (2); Darius Miles lab (7) | Wiki: drug manufacturing and distribution; Dewdrop Inn room 203 lab; Darius Miles leads "one of its drug-manufacturing rings". `[wiki]` `[game-data]` |
| Stolen/modified vehicles, chop work | `vehicles_chop` | Wicked Tires Autoshop (4); Acorn Towers parking lot (10) | Wiki: stolen and modified cars, "many garages and workshops"; Wicked Tires is a 6th Street autoshop. `[wiki]` |
| Smuggling, fencing, hot cargo | `smuggling` | Red White warehouse (3); Acorn parking (10); nomad routes | Wiki: smuggling, nomad connections, robbery; warehouse inventory shard describes moving "larger items" under cover. `[wiki]` |
| Political propaganda / media | `media` | Oak St garage (8) | *Error 404*: servers "pumping out anti-Holt propaganda" for Peralez. `[wiki]` |
| Bars, food, nightlife | `food_drink` | Red Dirt Bar (6); Stadium Love rooftop (11) | Bar + rooftop party. `[wiki]` |
| Retail, repairs, storefront fronts | `retail` | Wicked Tires (4); local shops under protection | Autoshop retail and protection rackets on local businesses. `[wiki]` `[inferred]` for the racket locations |
| Betting | `gambling` | Stadium Love rooftop (11) | Shooting contest with a prize and a named rival (Walker). `[wiki]` |
| Motel rooms / property | `real_estate` | Dewdrop Inn (2); H6 floor squat | Motel rooms and a squatted megabuilding floor. `[inferred]` from the place type |
| Combat taxi | `fixer_brokerage` (adjacent) | Not location-bound | Combat Cab is an affiliation, not a building in the extract. `[wiki]` |

### 4.2 Suppliers, customers, rivals

| Role | Party | Detail |
| --- | --- | --- |
| Supplier (arms) | **Militech** | Historical supplier of weaponry; also a target — the H6 cell hijacked a Militech transport. `[wiki]` |
| Supplier / partner (arms) | **Kendachi** | Supplies the gang and runs the top-secret "Arsenal" product line with it at the Almunecar factory. `[wiki]` |
| Supplier (vehicles, logistics) | Nomad groups | Wiki: "extensive connections with nomad groups inside and outside Night City"; vehicles purchased from nomads in the 2040s. `[wiki]` |
| Affiliate | **Combat Cab** | Combat-taxi service affiliated with 6th Street; popular with edgerunners. `[wiki]` |
| Affiliate | **FIA** | Listed in the organization infobox; no game-data footprint found. `[wiki]` |
| Customer | Rancho/Arroyo residents and shops | Buy protection and ersatz policing; pay tribute. `[wiki]` |
| Customer | Edgerunners and mercs | Combat Cab rides. `[wiki]` |
| Customer | Gun, drug and bootleg-goods buyers | Kendachi product line, beta acid, stolen cars and recordings. `[wiki]` |
| Customer (political) | Peralez campaign | Propaganda server farm. `[wiki]` |
| Rival | **Valentinos** | Long turf war, escalating in 2077 over Vista del Rey. `[wiki]` `[game-data]` (`ma_hey_gle_11`, `ma_hey_rey_05`) |
| Rival | **Tyger Claws** | Charter Hill contest and a shared Kendal Park community (`#ma_std_rcr_05_tyger_com`). `[wiki]` `[game-data]` |
| Rival | **Animals**, **Scavengers** | Santo Domingo co-residents; not a turf war in the data. `[wiki]` |
| Rival (fixer economy) | Muamar "El Capitán" Reyes, Rogue, Sebastian Ibarra | Several Santo Domingo gigs are hired *against* 6th Street: Breaking News, Hacking the Hacker, Error 404, Going-away Party, Nasty Hangover, Family Heirloom, Life's Work. `[wiki]` |
| Law | NCPD | Mostly tolerated; NCPD benefits from the gang's ersatz law, but runs scanner hustles against its drug rings. `[wiki]` `[game-data]` |

---

## 5. Headquarters recommendation

### Primary HQ: **6th Street hideout, Megabuilding H6, floor 19** — Arroyo

Coordinates: floor anchor `(-199.0, -843.5, 259.2)` `[game-data]` site 384
`sts_std_arr_11`; lift entrance at ground `(-168.8, -871.2, 11.5)`; lift door at
floor 19 `(-168.1, -871.0, 263.2)` `[game-data]` markers
`sts_std_arr_11_elevator_marker`, `sts_std_arr_11_elevator_marker_}001`.

Rationale:

1. **Canon HQ district.** The wiki's 2077 HQ is "Arroyo"; this is the largest
   6th Street interior in Arroyo and the tied-largest 6th garrison anywhere
   (15 roster units, level with the Oak St garage, including an officer, a
   netrunner and a named lieutenant, Lucius Thoran). `[wiki]` `[game-data]`
2. **A real command post, not just a venue.** The gig has V ride the lift to a
   hostile 19th floor with an office (`#arr_11_rma_lucius_offcie`), a lab
   (`#arr_11_inside_lab`), a second room (`#arr_rma_2nd_room`), a balcony and a
   sniper nest — six assignable subspaces for org management. `[game-data]`
3. **It maps to the gang's strategic business.** This is the cell that
   "jumped a Militech transport" and jailbreaks corpo weapons; an HQ that owns
   the arms pipeline is more coherent than one that owns a bar. `[wiki]`
4. **One choke point.** The floor is reached by lift (`#arr_11_lift_door`,
   `#lift_1`), so a capture trigger radius and a defence state are trivial to
   model and test.
5. **Verified geometry.** Two lift markers bracket the floor (z 11.5 vs 263.2),
   which also proves the 19-storey stack height and that the interior is a
   distinct cell despite `is_interior=0`.

Trade-off: the wiki calls this floor a *hideout*, not the HQ, and Megabuilding
H6 is a residential megablock — so it reads as a fortified den, not a
parade-ground headquarters. The world book's "Arroyo HQ" and "Old C-Team HQ"
have **no in-game building or record** (§8.1); this is the best verified
substitute. It is also gig-gated (`Hacking the Hacker`), which matters with the
campaign disabled (§8.7).

### Alternate 1: **Red White Used Warehouse** — Arroyo

Coordinates `(-573.6, -1182.9, 7.7)` `[game-data]` site 382.

The best *building* in the catalog: `is_interior=1`, two floors plus a roof
door, a netrunner chair and terminals, 10 units, and storage for hot cargo. It
loses because it is a stash/warehouse rather than a command post, and its
strongest records are inventory and netrunning, not leadership.

### Alternate 2: **Dewdrop Inn** — Arroyo

Coordinates `(-573.5, -821.5, 8.2)` `[game-data]` site 379.

The only location whose wiki infobox explicitly says `gangs = 6th Street`, with
a reception, rooms 103/203 and a second-floor beta-acid lab. It is a textbook
gang front and the best *business* seat. It loses on garrison size (6 units),
on command rooms, and because a motel front reads as a revenue site rather than
the org's brain.

### Overruled / downgraded suggestions

- **"Arroyo HQ" / "Old C-Team HQ" / "Pig Boy's Delight Irish Pub"** — the wiki's
  2077 faction-location list links all three, but all are red links with no
  page, no marker, no site and no community record. They are world-book names,
  not game places. Do not invent coordinates.
- **Red Dirt Bar as HQ** — the most lore-central landmark in Arroyo (one of the
  oldest buildings in Night City, Samurai's early venue), but the bar is not
  6th-run and has no gang-owned interior. Excellent control point, wrong seat.
- **Kendachi Factory (Almunecar)** — a strategic arms site and the "Arsenal"
  proof, but owned by Kendachi and guarded by independent security. A capture
  target, not a seat.
- **Megabuilding H7** — the wiki says the sealed megablock "looks to be guarded
  by the 6th Street", which is HQ-adjacent in feel, but there is no interior,
  no site and no marker coordinate. `TBD` (§8.3).
- **Kendal Park** — open ground, and the park's own site is Valentinos-flagged
  while carrying both a Tyger Claws and a 6th Street community. Contested, not
  a seat (§8.4).

---

## 6. Priority list of control points

Ranked by how well each place serves as a capturable 6th Street control point.
"CC" = nearest entry in `data/control_centers.json` (all entries, active or
not); distance is horizontal metres.

| Rank | Control point | Rel. (1–5) | District / sub-district | Coordinates | Existing CC overlap | Why |
| ---: | --- | :---: | --- | --- | --- | --- |
| 1 | **6th Street hideout, Megabuilding H6 floor 19** | 5 | SantoDomingo / Arroyo | `-199.0, -843.5, 259.2` | `cc_arr_kendachi_plant`, 449.9 m (owner 6th) | HQ; largest garrison, office + lab + netrunner den, single lift choke point |
| 2 | **Dewdrop Inn** | 5 | SantoDomingo / Arroyo | `-573.5, -821.5, 8.2` | `cc_arr_kendachi_plant`, 218.3 m (6th) | Explicitly 6th-owned motel + beta-acid lab; reception and rooms; best business front |
| 3 | **Red White Used Warehouse** | 5 | SantoDomingo / Arroyo | `-573.6, -1182.9, 7.7` | `cc_arr_kendachi_plant`, 148.7 m (6th) | Enclosed `is_interior=1` warehouse, netrunner den, hot-cargo stash; clean ownership |
| 4 | **Wicked Tires Autoshop** | 5 | Heywood / Glen | `-1398.9, -1279.7, 46.9` | `cc_gle_hanford_overpass`, 68.2 m (**owner Kang Tao**) | Named 6th autoshop; vehicle economy; the gang's local Glen HQ per lore pattern |
| 5 | **Kendachi Factory (Almunecar)** | 4 | SantoDomingo / Arroyo | `-282.1, -1721.0, 7.5` | `cc_arr_petrochem_yard`, 242.4 m (**owner Petrochem**) | "Arsenal" joint weapons line; high-value strategic target; corp-owned, so capture is a story beat |
| 6 | **Red Dirt Bar** | 4 | SantoDomingo / Arroyo | `-725.1, -991.9, 9.3` | `cc_arr_kendachi_plant`, 128.4 m (6th) | Iconic Arroyo landmark inside a 6th-owned crossroads; social hub and protection income |
| 7 | **Darius Miles' drug lab** | 4 | SantoDomingo / Arroyo | `-614.2, -1038.1, 7.4` | `cc_arr_kendachi_plant`, **9.3 m** (6th) | Named NCPD target, 13 units, drug manufacturing; effectively on top of an existing CC |
| 8 | **Propaganda garage, Oak St** | 4 | SantoDomingo / RanchoCoronado | `245.2, -1074.7, 21.4` | `cc_rcr_kendal_park`, 310.5 m (6th) | `media` revenue and the gang's political operation; 15 units |
| 9 | **Kendal Park** | 3 | SantoDomingo / RanchoCoronado | `292.5, -986.7, 20.5` | `cc_rcr_kendal_park`, 241.3 m (6th) | Neighborhood-control showpiece; contested with Tyger Claws |
| 10 | **Acorn Towers parking lot** | 3 | Westbrook / CharterHill | `375.3, -400.1, 2.6` | `cc_hil_gold_beach`, 108.7 m (**owner Militech**) | Vehicle + bootleg-goods fencing in a rival district; 12 units |
| 11 | **Stadium Love rooftop** | 2 | SantoDomingo / RanchoCoronado | `503.0, -2128.7, 27.4` | `cc_rcr_piez_plaza`, 305.0 m (6th) | Recruitment, drinking and betting with a named captain; social rather than economic |

### Test control point for the first in-game test: **Dewdrop Inn**

Why the Dewdrop Inn and not the HQ:

- **Fully enclosed interior with the richest door topology of any 6th site** —
  nine door refs (`#arr_01_dvc_door_016`, `_start_001/006/009/015/018/019`,
  `#arr_01_dvc_shutter_generic_room`, `#door1`) plus a reception patrol, so door
  state, room occupancy and a capture radius can all be exercised.
- **Clean ownership**: `default_faction_id = 4`, six roster units, no NCPD or
  corporate garrison. Who is being evicted is unambiguous.
- **Five guard/restricted-movement volumes plus a ground-floor volume**
  (`#arr_01_restrict_movement_area`, `#arr_01_rma_chem_lab`,
  `#arr_01_rma_gang_001_002`, `#arr_01_rma_gang_003_004`, `#arr_01_rma_gang_005`,
  `#std_arr_01_rma_ground_floor`), enough to model a defence without the
  15-unit HQ garrison overwhelming a first test.
- **218 m from `cc_arr_kendachi_plant`** (6th-owned, inactive) — close enough
  that no new map plumbing is needed; the CC can be retargeted if desired.
- **Not the HQ**, so the first test proves capture on a non-seat and leaves the
  HQ seat for the second pass.

Fallback if the motel geometry is awkward: **Red White Used Warehouse**
(`sts_std_arr_06`, `is_interior=1`, 10 units, 149 m from the same CC).

---

## 7. Per-sub-district count of lore-relevant locations

This is the number to feed yield balancing. It counts **distinct named places**
the gang owns, runs, protects or habitually occupies — not quest-scene variants
and not generic occupied blocks. `Filler` is the deduped occupied-site count
minus any site already counted as a named place (METHOD §8).

| Sub-district | Named lore-relevant places | Which ones | 6th-occupied sites (deduped) | Filler | Sites behind the filler count |
| --- | ---: | --- | ---: | ---: | --- |
| Arroyo | **6** | Megabuilding H6 hideout (1), Dewdrop Inn (2), Red White warehouse (3), Kendachi Almunecar (5), Red Dirt Bar (6), Darius Miles lab (7) | 7 | 3 | `ma_std_arr_07`, `ma_std_arr_05`, `ma_std_arr_09` |
| RanchoCoronado | **3** | Oak St propaganda garage (8), Kendal Park (9), Stadium Love rooftop (11) | 12 | 10 | `ma_std_rcr_08`, `ma_std_rcr_07`, `ma_std_rcr_09`, `sts_std_rcr_03`, `ma_std_rcr_01`, `ma_std_rcr_13`, `ma_std_rcr_02`, `ma_std_rcr_14`, `ma_std_rcr_10`, `ma_std_rcr_12` |
| Glen | **1** | Wicked Tires Autoshop (4) | 3 | 2 | `ma_hey_gle_09`, `ma_hey_gle_11` |
| CharterHill | **1** | Acorn Towers parking lot (10) | 1 | 0 | — |
| VistaDelRey | **0** | turf war only | 1 | 1 | `ma_hey_rey_05` |
| Northside | **0** | hidden-stash cameos only | 4 | 4 | `ma_wat_nid_12`, `ma_wat_nid_19`, `ma_wat_nid_26`, `ma_wat_nid_30` |
| Coastview | **0** | *Roads to Redemption* cameo | 1 | 1 | `sts_ep1_07` |
| Dogtown / WestWindEstate / Badlands / Kabuki / NorthOaks / Wellsprings | **0** | quest cameos / stray areas only | 0 | 0 | — |
| **Total** | **11** | | 29 | 21 | |

Accounting details for the JSON block:

- Eight named places are site-backed: sites 384, 379, 382, 125, 389, 150, 368,
  416. `29 − 8 = 21` filler.
- Three named places are not occupied sites: **Red Dirt Bar** (marker-only),
  **Stadium Love rooftop** (marker/community-only) and **Kendachi Factory
  (Almunecar)** (site 381, but zero 6th Street roster units — it is a partner
  facility). So `named + filler = 32`, while there are 29 occupied sites.
- Megabuilding H4 Plaza (catalog row 12) is a **landmark row, not counted**;
  Megabuilding H7 (row 13) has no verified coordinate and is not counted.

Interpretation for yield: Arroyo is the only sub-district with a deep named
pool (six), and it also holds the HQ and the best test point. RanchoCoronado has
more raw presence (12 sites) but only three named places, so its per-point yield
should be low and its filler high. Glen and CharterHill have exactly one named
place each and should carry the highest per-point yield outside Arroyo.

---

## 8. Gaps and uncertainties

1. **The book HQ has no in-game building.** The wiki's 2077 HQ is "Arroyo"; its
   faction-location list links "Arroyo HQ", but that is a red link with no page,
   marker, site or community record. My HQ is a reasoned substitution. State it
   as such in any UI text.
2. **"Old C-Team HQ" and "Pig Boy's Delight Irish Pub" are book-only names.**
   No page, no marker, no site, no community. They may be unused or tabletop
   content. Do not seed them without a game record.
3. **Megabuilding H7 has no verified coordinate.** The wiki says it is in a
   "closed state" and "looks to be guarded by the 6th Street" in Rancho
   Coronado; there is no marker, site or community to anchor it. `TBD`.
4. **Kendal Park ownership is contested.** The sub-territory `rcr_kendal_park`
   is seeded to 6th Street, but the park site 150 has `default_faction_id = 3`
   (Valentinos) and two communities: `#ma_std_rcr_05_tyger_com` (Tyger Claws, 4
   entries, primary) and `#ma_std_rcr_05_sixthstreet_com` (6th Street, 2). Three
   gangs are represented in one park. Pick an owner deliberately.
5. **Kendachi Almunecar's district label conflicts inside the wiki itself.**
   *Breaking News* says `sub_district = Rancho Coronado` but `location =
   Kendachi Factory, Arroyo`. The extract puts site 381 in Arroyo
   (`district_id = 4`, sub-territory 52 Petrochem Freight Yard). I used Arroyo.
   The separate "Almunecar Highway Strip" sub-territory 57 is in Rancho
   Coronado, ~470 m south, which is probably the source of the confusion.
6. **Site 384's `sub_territory_id` is a seed artifact.** It says 53 "Kendachi
   Foundry", but the hideout is the Megabuilding H6 floor on MLK Blvd, ~450 m
   from the Kendachi cluster. Attribute by coordinates, not by that field.
7. **All named 6th interiors are gig-gated.** H6 (Hacking the Hacker), Dewdrop
   Inn (Serious Side Effects), Red White (Nasty Hangover), Wicked Tires (Life's
   Work), Oak St garage (Error 404), Acorn parking (Family Heirloom). The mod
   disables the campaign, so these interiors *should* be open, but that is
   unverified in-game. Check before seeding a capture volume.
8. **Areas are mis-districted in the raw file.** 49 of 96 rows resolved by
   nearest site, not geocode token; one (`{q103_com_maelstrom_roadhouse}`) by
   nearest sub-territory. Several `always_loaded_*` rows carry the sector's
   path token. Never aggregate `areas.jsonl` by `district_code` except for
   Dogtown, where that field was the most reliable signal.
9. **Northside's four "sites" are reused character records.** Sites 225, 231,
   236 and 238 are Watson hidden-stash activities that spawn
   `Character.rcr_sixthstreet_*` (Rancho Coronado records). They have no local
   turf, no areas and no spawn points. Treat them as a data anomaly, not a
   Northside claim.
10. **Site 359 (Roads to Redemption) is district-ambiguous.** The wiki places
    the gig in Dogtown; the extract puts the site in Coastview East Overpass
    (`sub_territory_id = 63`, `district_id = 5`). Spawn points in Dogtown (3)
    and Coastview (3) do not match the site list (0 and 1). It is a Phantom
    Liberty cameo either way.
11. **The 2045 lore is not the 2077 map.** The Armory (North Heywood),
    6th Street Station, the Maquiladoras and the long guarded-location list are
    Cyberpunk RED. Only the four 2077 names (Arroyo HQ, Old C-Team HQ, Pig Boy's
    Delight, Wicked Tires) are game-era, and only Wicked Tires is a real place.
12. **No vendor inventories.** "What each business sells" comes from the wiki
    and from named rooms (`chem_lab`, `server_garage`, `garage`, `bar`), not
    from vendor records. The Kendachi product line in particular is wiki lore.
13. **`is_interior` is sparse.** Only site 382 is flagged among the 29. Dewdrop
    Inn, H6, Wicked Tires and Kendachi Almunecar have interiors proven by node
    refs, doors and gig text, not by the flag.
14. **Combat Cab and FIA affiliations have no location.** Both appear in the
    organization infobox; neither has a site, marker or community in the
    extract. Do not invent a depot or an FIA office.
15. **The gang's per-district local HQs are lore, not records.** The wiki says
    other districts had their own local HQs; Wicked Tires is the only plausible
    Glen seat, and I found no equivalent for Rancho or Charter Hill except the
    generic sites above.

---

## 9. Sources

Local:

- `dist/extract/areas.jsonl`, `dist/extract/markers.jsonl`.
- `data/sites/{sites,communities,rosters,guards,triggers,spots,patrols,doors,suitabilities}.json`.
- `data/{districts,factions,sub_territories,landmarks,control_centers,spawn_points}.json`.
- Earlier repo research: `docs/research/factions-gangs-territories.md` (§2.2
  sub-district gang panel), `docs/research/game-data-extraction.md` (§5.5
  district-code defect).

Wiki (MediaWiki API, infoboxes and gig bodies only):

- Organization: [6th Street](https://cyberpunk.fandom.com/wiki/6th_Street),
  [Will Gunner](https://cyberpunk.fandom.com/wiki/Will_Gunner),
  [Kendachi](https://cyberpunk.fandom.com/wiki/Kendachi).
- Districts: [Santo Domingo](https://cyberpunk.fandom.com/wiki/Santo_Domingo_(2077)),
  [Arroyo](https://cyberpunk.fandom.com/wiki/Arroyo),
  [Rancho Coronado](https://cyberpunk.fandom.com/wiki/Rancho_Coronado_(2077)).
- Places: [Dewdrop Inn](https://cyberpunk.fandom.com/wiki/Dewdrop_Inn),
  [Wicked Tires Autoshop](https://cyberpunk.fandom.com/wiki/Wicked_Tires_Autoshop),
  [Megabuilding H6](https://cyberpunk.fandom.com/wiki/Megabuilding_H6),
  [Megabuilding H7](https://cyberpunk.fandom.com/wiki/Megabuilding_H7),
  [Red Dirt](https://cyberpunk.fandom.com/wiki/Red_Dirt),
  [Rancho Coronado Public Park](https://cyberpunk.fandom.com/wiki/Rancho_Coronado_Public_Park),
  [Kendachi Factory (Almunecar)](https://cyberpunk.fandom.com/wiki/Kendachi_Factory_(Almunecar)),
  [Kendachi Factory (El Camino)](https://cyberpunk.fandom.com/wiki/Kendachi_Factory_(El_Camino)),
  [Red White Used Warehouse/Computers](https://cyberpunk.fandom.com/wiki/Red_White_Used_Warehouse/Computers),
  [The Armory](https://cyberpunk.fandom.com/wiki/The_Armory).
- Gigs / jobs: [Hacking the Hacker](https://cyberpunk.fandom.com/wiki/Gig:_Hacking_the_Hacker),
  [Serious Side Effects](https://cyberpunk.fandom.com/wiki/Gig:_Serious_Side_Effects),
  [Nasty Hangover](https://cyberpunk.fandom.com/wiki/Gig:_Nasty_Hangover),
  [Life's Work](https://cyberpunk.fandom.com/wiki/Gig:_Life%27s_Work),
  [Error 404](https://cyberpunk.fandom.com/wiki/Gig:_Error_404),
  [Family Heirloom](https://cyberpunk.fandom.com/wiki/Gig:_Family_Heirloom),
  [Going-away Party](https://cyberpunk.fandom.com/wiki/Gig:_Going-away_Party),
  [Breaking News](https://cyberpunk.fandom.com/wiki/Gig:_Breaking_News),
  [Race to the Top](https://cyberpunk.fandom.com/wiki/Gig:_Race_to_the_Top),
  [Stadium Love](https://cyberpunk.fandom.com/wiki/Stadium_Love),
  [Suspected Organized Crime Activity (Arroyo)](https://cyberpunk.fandom.com/wiki/Suspected_Organized_Crime_Activity_(Arroyo)),
  [`[IMPORTANT] "Arsenal"`](https://cyberpunk.fandom.com/wiki/IMPORTANT_%22Arsenal%22).

---

## 10. Machine-readable block

Strict JSON for seeding (contract in [`METHOD.md`](./METHOD.md) §10). Every
coordinate was re-verified against the local record named in `source` on
2026-11-25; none came from the wiki.

```json
{
  "faction_code": "sixth_street",
  "hq": {"name": "6th Street hideout, Megabuilding H6 floor 19", "district": "SantoDomingo", "sub_district": "Arroyo", "x": -199.039, "y": -843.481, "z": 259.17, "source": "data/sites/sites.json site 384 sts_std_arr_11; markers.jsonl sts_std_arr_11_elevator_marker z=11.47 / sts_std_arr_11_elevator_marker_}001 z=263.18", "confidence": "game-data+wiki"},
  "alternate_hqs": [
    {"name": "Red White Used Warehouse", "district": "SantoDomingo", "sub_district": "Arroyo", "x": -573.614, "y": -1182.899, "z": 7.701, "source": "data/sites/sites.json site 382 sts_std_arr_06", "confidence": "game-data+wiki"},
    {"name": "Dewdrop Inn", "district": "SantoDomingo", "sub_district": "Arroyo", "x": -573.481, "y": -821.454, "z": 8.203, "source": "data/sites/sites.json site 379 sts_std_arr_01", "confidence": "game-data+wiki"}
  ],
  "test_control_point": {"name": "Dewdrop Inn", "district": "SantoDomingo", "sub_district": "Arroyo", "x": -573.481, "y": -821.454, "z": 8.203, "source": "data/sites/sites.json site 379 sts_std_arr_01", "confidence": "game-data+wiki"},
  "control_points": [
    {"rank": 1, "name": "6th Street hideout, Megabuilding H6 floor 19", "type": "hideout", "relevance": 5, "district": "SantoDomingo", "sub_district": "Arroyo", "x": -199.039, "y": -843.481, "z": 259.17, "source": "data/sites/sites.json site 384 sts_std_arr_11", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["arms", "rnd", "smuggling"], "nearest_cc_code": "cc_arr_kendachi_plant", "nearest_cc_m": 449.9},
    {"rank": 2, "name": "Dewdrop Inn", "type": "motel_drug_lab", "relevance": 5, "district": "SantoDomingo", "sub_district": "Arroyo", "x": -573.481, "y": -821.454, "z": 8.203, "source": "data/sites/sites.json site 379 sts_std_arr_01", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["drugs", "real_estate", "protection"], "nearest_cc_code": "cc_arr_kendachi_plant", "nearest_cc_m": 218.3},
    {"rank": 3, "name": "Red White Used Warehouse", "type": "warehouse", "relevance": 5, "district": "SantoDomingo", "sub_district": "Arroyo", "x": -573.614, "y": -1182.899, "z": 7.701, "source": "data/sites/sites.json site 382 sts_std_arr_06", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["smuggling", "arms"], "nearest_cc_code": "cc_arr_kendachi_plant", "nearest_cc_m": 148.7},
    {"rank": 4, "name": "Wicked Tires Autoshop", "type": "autoshop", "relevance": 5, "district": "Heywood", "sub_district": "Glen", "x": -1398.909, "y": -1279.724, "z": 46.863, "source": "data/sites/sites.json site 368 sts_hey_gle_06", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["vehicles_chop", "retail"], "nearest_cc_code": "cc_gle_hanford_overpass", "nearest_cc_m": 68.2},
    {"rank": 5, "name": "Kendachi Factory (Almunecar)", "type": "factory", "relevance": 4, "district": "SantoDomingo", "sub_district": "Arroyo", "x": -282.083, "y": -1720.973, "z": 7.54, "source": "data/sites/sites.json site 381 sts_std_arr_05", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["manufacturing", "arms", "rnd"], "nearest_cc_code": "cc_arr_petrochem_yard", "nearest_cc_m": 242.4},
    {"rank": 6, "name": "Red Dirt Bar", "type": "bar", "relevance": 4, "district": "SantoDomingo", "sub_district": "Arroyo", "x": -725.063, "y": -991.851, "z": 9.296, "source": "dist/extract/markers.jsonl sq011_mp_red_dirt", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["food_drink", "protection"], "nearest_cc_code": "cc_arr_kendachi_plant", "nearest_cc_m": 128.4},
    {"rank": 7, "name": "Darius Miles' drug lab", "type": "drug_lab", "relevance": 4, "district": "SantoDomingo", "sub_district": "Arroyo", "x": -614.238, "y": -1038.144, "z": 7.39, "source": "data/sites/sites.json site 125 ma_std_arr_03", "confidence": "game-data+wiki", "interior": false, "revenue_streams": ["drugs"], "nearest_cc_code": "cc_arr_kendachi_plant", "nearest_cc_m": 9.3},
    {"rank": 8, "name": "Propaganda garage, Oak St", "type": "garage", "relevance": 4, "district": "SantoDomingo", "sub_district": "RanchoCoronado", "x": 245.16, "y": -1074.692, "z": 21.357, "source": "data/sites/sites.json site 389 sts_std_rcr_04", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["media", "protection"], "nearest_cc_code": "cc_rcr_kendal_park", "nearest_cc_m": 310.5},
    {"rank": 9, "name": "Kendal Park", "type": "park", "relevance": 3, "district": "SantoDomingo", "sub_district": "RanchoCoronado", "x": 292.457, "y": -986.732, "z": 20.49, "source": "data/sites/sites.json site 150 ma_std_rcr_05", "confidence": "game-data+inferred+wiki", "interior": false, "revenue_streams": ["protection", "drugs"], "nearest_cc_code": "cc_rcr_kendal_park", "nearest_cc_m": 241.3},
    {"rank": 10, "name": "Acorn Towers parking lot", "type": "parking_lot", "relevance": 3, "district": "Westbrook", "sub_district": "CharterHill", "x": 375.332, "y": -400.129, "z": 2.646, "source": "data/sites/sites.json site 416 sts_wbr_hil_06", "confidence": "game-data+wiki", "interior": false, "revenue_streams": ["vehicles_chop", "smuggling"], "nearest_cc_code": "cc_hil_gold_beach", "nearest_cc_m": 108.7},
    {"rank": 11, "name": "Stadium Love rooftop", "type": "rooftop_party", "relevance": 2, "district": "SantoDomingo", "sub_district": "RanchoCoronado", "x": 503.017, "y": -2128.698, "z": 27.38, "source": "dist/extract/markers.jsonl mq008_02_sm_shooting_contest", "confidence": "game-data+inferred+wiki", "interior": false, "revenue_streams": ["gambling", "food_drink"], "nearest_cc_code": "cc_rcr_piez_plaza", "nearest_cc_m": 305.0}
  ],
  "subdistrict_counts": {
    "Arroyo": {"named": 6, "filler": 3},
    "RanchoCoronado": {"named": 3, "filler": 10},
    "Glen": {"named": 1, "filler": 2},
    "CharterHill": {"named": 1, "filler": 0},
    "VistaDelRey": {"named": 0, "filler": 1},
    "Northside": {"named": 0, "filler": 4},
    "Coastview": {"named": 0, "filler": 1},
    "Dogtown": {"named": 0, "filler": 0},
    "WestWindEstate": {"named": 0, "filler": 0},
    "Badlands": {"named": 0, "filler": 0},
    "Kabuki": {"named": 0, "filler": 0},
    "NorthOaks": {"named": 0, "filler": 0},
    "Wellsprings": {"named": 0, "filler": 0}
  }
}
```
