# Wraiths — Lore-Relevant Control Points

Status: faction research run, 2026-11-25. One faction, one document.
Scope: replace the generic control-centre grid with Badlands/industrial places the
Wraiths actually own, run or garrison, with verified coordinates, an economic map,
an HQ pick, a ranked capture list and honest per-sub-district counts. Method:
this doc conforms to [`METHOD.md`](./METHOD.md), applying **§1.2 (batch 2)
first** and then §1.1 (batch 1); where they conflict, §1.2 wins. `AGENTS.md` was
read first. No commits, no game launch.

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Position, site, community, roster, area or marker record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page via the MediaWiki API (cited inline) | Secondary, high |
| `[lore]` | Book/artbook/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My reasoning links a named place to a game record; reasoning stated | Weak, flagged |

No coordinate below is guessed. Every `(x, y, z)` is copied from a local site,
marker or area record, or marked `TBD`. No coordinate in this document came from
the wiki.

---

## 1. Summary

The **Wraiths** are Night City's Raffen Shiv gang (`data/factions.json` fid **8**,
`affiliation_enum = Wraiths`, `category = gang`): nomads expelled from their
families for murder, trafficking, poisoning water or betrayal, who prowl the
Badlands robbing travellers, convoys and other nomad camps. The 2077 World Book
puts them at ≈300–1,200 members and threat level *High*. `[wiki]`

Their economy is **predation, not commerce**. The Wraiths run no shopfront, venue
or licensed business of their own; every location below is a base, a garage or a
stash:

- **Raiding** — "the main source of income for the Wraiths were the spoils from
  their raids"; they ransack towns, hit weakly guarded corp transports and raid
  small nomad groups. `[wiki]`
- **Vehicle theft and chop work** — the Corp-Bud Cement Factory is a "garage and
  hideout for their vehicles"; Nash's crew stole Panam's Thorton; a Wraith
  garage south of the EBM Petrochem Stadium was holding a stolen Porsche. `[wiki]`
  `[game-data]`
- **Kidnap, ransom and chrome harvesting** — "similar to the Scavengers, the
  Wraiths would also kidnap people and kill them for their bodyparts and chrome";
  the cement factory basement is used "to hold and gut victims to sell their
  bodyparts and chrome"; human-trafficking leader Paul Craven is Wraith-affiliated.
  `[wiki]`
- **Contraband logistics** — Poppy Farm stored "equipment slated to be smuggled
  across the border"; transport contracts were taken and then broken, the cargo
  kept. `[wiki]`
- **Drone hijacking** — at Union Railroad Station they installed the **KI113R**
  virus on the station antenna to drop cargo drones, with help from the netrunner
  `b@d`. `[wiki]`
- **Drug-stash raids** — `b@d` sold them intel on a Maelstrom stash, which they
  hit (the Northside *Reported Crime: Dredged Up* scene). `[wiki]` `[game-data]`

**Where the weight sits.** Almost everything is **Badlands**: 48 of 55 community
areas and 291 of 327 Wraith entries. Unlike the city gangs there is no
sub-district where they run an economy — they hold three strongholds (cement
factory, mine, Rocky Ridge), five field outposts and one smuggling stash. The
only city footholds are a Rancho Coronado trafficking cell, a Northside crime
scene and two West Wind Estate hustles.

**Canon base.** The wiki's organization infobox leaves `headquarters` **blank**.
Its 2077 "Faction Locations" list is only four entries: **Corp-Bud Cement
Factory**, **Poppy Farm**, **Rocky Ridge** and **Union Railroad Station**; the
cement factory is called "this stronghold" in its own article. `[wiki]` The
in-game evidence agrees: the seed's `bls_wraith_compound` anchor
(`3003.6, -2394.3`) sits on the `sq004` Wraith camp, which is the Corp-Bud Cement
Factory (§5). `[game-data]`

---

## 2. Territory

### 2.1 Districts

| Evidence kind | Result |
| --- | --- |
| (a) Wiki/lore | Badlands only. All four 2077 faction locations are Badlands sites (Sierra Sonora, Rocky Ridge Plains, Red Peaks, Laguna Bend Reservoir). City appearances are crimes and ambushes, never businesses. `[wiki]` |
| (b) Vanilla map gang panel | `data/districts.json` `vanilla_gangs` = `Badlands: ["Aldecaldos","Wraiths"]`. No city district lists them. |
| (c) Game-data counts | 55 community areas contain Wraiths (51 dominant), 327 entries, **12 roster sites / 85 units**, 3 seeded sub-territories (`bls_sunset_motel`, `bls_rocky_ridge`, `bls_wraith_compound`), 46 spawn points. `[game-data]` |

The three seeded sub-territories and what actually justifies each:

| Sub-territory | Display name | Verdict |
| --- | --- | --- |
| `bls_wraith_compound` | Wraiths Badlands Compound | **Solid.** The centroid sits on the `sq004` Wraith camp — the **Corp-Bud Cement Factory** (Saul's prison, the walled compound, the basement). Anchored here on real markers. `[game-data]` `[wiki]` |
| `bls_rocky_ridge` | Rocky Ridge Ghost Town | **Solid, but it is a haunt, not a base.** The Wraiths use the bar and watch from the fuel-station roof; Nash kept a secret office in the town. No site or roster record — marker/area only. `[game-data]` `[wiki]` |
| `bls_sunset_motel` | Sunset Motel | **Wrong.** The motel is neutral, owned by Noah; it is a *Ghost Town* quest location, not a Wraith property. The real Wraith point inside this sub-territory is **Union Railroad Station**, 310 m north-east. See §8.1. `[game-data]` `[wiki]` |

`data/faction_headquarters.json` has **no Wraiths row** (only Maelstrom, Tyger
Claws, Valentinos, 6th Street, Voodoo Boys and Arasaka). The HQ in §5 is derived,
not read from that file. `[game-data]`

### 2.2 Sub-district presence

Counts are `dist/extract/areas.jsonl` rows whose `faction_counts` contains
`wraiths`, attributed per §2.3, plus deduped occupied sites (§3.2, §7).

| Sub-district | District | (a) Lore | (b) Panel | (c) areas (dominant) | (c) entries | Occupied sites |
| --- | --- | --- | --- | ---: | ---: | ---: |
| Badlands | Badlands | everything | Aldecaldos, Wraiths | **48 (45)** | **291** | 6 |
| RanchoCoronado | SantoDomingo | trafficking cell at Sequoia & Gray | 6th Street | 2 (2) | 21 | 1 |
| WestWindEstate | Pacifica | scav-den hit + hustle | Voodoo Boys, Animals | 2 (2) | 7 | 2 |
| Northside | Watson | *Dredged Up* stash raid | Maelstrom | 2 (2) | 7 | 1 |
| LittleChina | Watson | one stray crowd entry | Tyger Claws | 1 (0) | 1 | 0 |

Spawn points (`data/spawn_points.json`, `faction_id 8`, grouped by
`sub_territory_id` per §1.1 item 15): Badlands 38, RanchoCoronado 2, Northside 2,
WestWindEstate 2, plus **Arroyo 1 and Dogtown 1 that are bucketing artifacts**
(site 163's `source_path` is Rancho Coronado but its `sub_territory_id` 52 is
Arroyo's petrochem yard; site 324's path is Badlands but its `sub_territory_id`
57 is Dogtown's `dt_terra_cognita`). Total 46.

**What the areas actually are** (louder than the counts):

- **Quest strongholds.** `sq004` (Riders on the Storm) supplies 51 Wraith entries
  across five communities at the cement factory; `q103` (Ghost Town) adds the
  mine ambush (11 + 3) and Rocky Ridge (7). That is 72 of the 327 entries in two
  quests.
- **Aldecaldo-camp assault.** `sq027` (Queen of the Highway) contributes 30
  entries at the Aldecaldo camp — Wraiths attacking, not living there. Not a
  holding (§1.2 item 9).
- **Sites.** 7 entries at the landfill outpost, 9 at the Highway 101 nest, 9 at
  Big Pete's garage, 14 at Union Railroad, 7 at the Shape-of-a-Pony garage.
- **Ambient road gangs.** `ma_bls_ina_se1_11…21` and `ma_bls_ina_se5_03…16` are
  open-world Wraith community areas along the eastern and southern highways with
  a `*_spawn_point` marker each and **no `sites.json` row at all** (only
  `dead_zone_marker*` and `top` noise nearby). Several carry
  `la_sm_execution_03`, a Militech execution scene where the Wraith is the
  victim. These are encounters, not places. 16 areas / 87 entries.
- **Dynamic events.** `cs_bls_assaulted_conv_wraiths_attacker`,
  `cs_handcuffed_wraiths_*`, `cs_broken_convoy_com`,
  `cs_bls_car_execution_wraiths_com`, `cs_militech_execution_com_victim` — convoy
  ambushes and prisoner handovers. Presence, not ownership.
- **`sa_ep1_101_com`** (10 Wraiths, `-2032, -4582`) and `sa_ep1_159_*` (5) are
  Phantom Liberty-era side-activity communities in the far south with no site, no
  marker and no wiki page. Unexplained; excluded.

### 2.3 Attribution caveat

Four failure modes were hit, all covered by §1.2 item 1 but worth naming:

1. **Token first, then bbox — never `district_code`.** `areas.jsonl` labels
   `{ma_bls_ina_se1_06_com}` (a Badlands highway community at `1031, -1493`)
   `santo_domingo`, because its sector sits under Santo Domingo's path. Token
   (`bls`/`se1`) plus the site's `source_path` (`badlands/inland_avenue_se1`) say
   Badlands. `[game-data]`
2. **`data/districts.json` bboxes are rectangles around irregular district
   polygons, so they over-claim.** `(1031, -1493)` and `(-913, -2362)` fall
   inside the Santo Domingo bbox but are Badlands road/outskirts geometry. A bbox
   test is a fallback only, and it must exclude the (map-wide) Badlands box.
3. **`sites.json.sub_territory_id` is a bucket.** Site 324 `mws_se5_07` carries
   `sub_territory_id 57` = *Dogtown's* `dt_terra_cognita`, 1.4 km away; site 340
   carries 89 = the Militech Detention Center; site 344 carries 81 = Sunset
   Motel. `source_path` resolved every one of them (`badlands/se5`,
   `badlands/inland_avenue`). `[game-data]`
4. **Site anchors can be far off for camps.** Site 324's anchor
   (`-913.211, -2362.664`) is **201 m** from its own Wraith community
   (`-1101.190, -2426.750`) and from the `mws_sm_se5_07_camp` marker. For
   camp-type points I used the community/marker position, not the anchor, per
   §1.2 item 7. `[game-data]`

---

## 3. Location catalog

Coordinates are world-space metres, `Z` up. "Interior?" means the game has a
distinct interior cell or volume — proven from node names (or, where marked,
the wiki's building layout), not the sparse `is_interior` flag (§1.2 item 15).
"Business?" is what the place earns or provides; the extract has no vendor
inventory.

| # | Name | Type | District / sub-district | Interior? | Business? (what it earns) | Coordinates (x, y, z) | Coordinate source record | Linked communities / sites | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **Corp-Bud Cement Factory** | Abandoned cement plant → gang stronghold | Badlands / Badlands (Sierra Sonora) | Yes — walled yard, gate + guardhouse, basement, prison | `vehicles_chop` (garage/hideout for their vehicles), `cyberware` (basement gutting room), `mercenary`, `smuggling` | `3007.724, -2385.058, 124.630` | `markers.jsonl` `sq004_mp_raffen_shiv_camp` | `sq004_com_wall` (18 W), `sq004_com_raiders` (10), `sq004_com_main` (8), `sq004_com_chase_enemies` (10), `sq004_com_reinforcements` (5); `sq004_mp_raffen_shiv_prison`, `sq004_mp_basement_entrance`, `sq004_mp_drone_01_gate`, `sq004_mp_drone_01a_guardhouse` | `[game-data]` `[wiki]` |
| 2 | **Corp-Bud Mine** | Abandoned limestone mine → stronghold | Badlands / Badlands (Rocky Ridge Plains) | Yes — main tunnel section, both entrances | `mercenary` (Nash's seat), `vehicles_chop`, `smuggling` | `1871.475, 1.355, 55.074` | `markers.jsonl` `q103_12_sm_tunnel_ambush` | `q103_com_mine_ambush_raffen_shiv` (11), `…_reinforcements` (3); `q103_spwn_player_mine` 30 m | `[game-data]` `[wiki]` |
| 3 | **Union Railroad Station** | Abandoned rail station → outpost | Badlands / Badlands (Red Peaks) | Yes — station building, interior guard volume, roof; armed gate | `netrunning` (KI113R drone-hijack virus), `smuggling` (stolen drone cargo), `mercenary` | `1882.553, -553.140, 54.852` | `sites.json` site 341 `sts_bls_ina_03` | `ina_03_comm` (14), `ina_03_comm_reinforcements` (2); 16 roster units; 4 guard areas, 9 patrols | `[game-data]` `[wiki]` |
| 4 | **New American Autoworks (Jackson Plains)** | Auto workshop + fuel station, Wraith-garrisoned | Badlands / Badlands (Jackson Plains) | Yes — `is_interior=1`; workshop, office, basement, utility tunnel | `vehicles_chop` (repair/chop shop), `mercenary`, `smuggling` | `-142.756, -4419.236, 58.870` | `sites.json` site 340 `sts_bls_ina_02` | `ina_02_com_gangers` (9); 9 roster units; 7 guard areas, 6 patrols, 11 doors, 4 devices | `[game-data]` `[wiki]` |
| 5 | **Wraiths Outpost (Municipal Landfill)** | Makeshift outpost in the city dump | Badlands / Badlands (Rocky Ridge Plains) | Yes — sheds, garage, roof, main path | `mercenary` (hostage-holding), `smuggling` | `2169.702, -1637.889, 67.000` | `sites.json` site 344 `sts_bls_ina_06` | `ina_06_com` (7); 7 roster units; 3 guard areas, 6 patrols, 3 doors, 3 devices | `[game-data]` `[wiki]` |
| 6 | **Poppy Farm** | Abandoned farmstead → smuggling stash | Badlands / Badlands (Laguna Bend Reservoir) | No proven interior — no node record; farmstead walls only | `smuggling` (equipment staged for the border) | `874.946, -3579.587, 180.395` | `markers.jsonl` `sq021_13_sm_wrong_farm` | `sq021_com_wrong_farm_wraiths` (10); `sq021_spwn_setup_wrong` 20 m | `[game-data]` `[inferred]` `[wiki]` |
| 7 | **Rocky Ridge (bar + fuel station)** | Ghost town | Badlands / Badlands (Rocky Ridge Plains) | Yes per wiki layout — bar ground floor + three upper booths; fuel-station workshop and store | `mercenary`, `smuggling`, `vehicles_chop` (workshop); Nash's secret office | `2580.302, -41.797, 80.810` | `markers.jsonl` `q103_mp_ghost_town` | `q103_com_raffen_shiv` (7); `q103_08_sm_ghost_town_plan` (bar plan scene), `q103_09_sm_raffen_shiv` (30 m), `q103_mp_power_station` | `[game-data]` `[wiki]` |
| 8 | **Wraiths' nest, Highway 101** | Roadside outpost with a body freezer | Badlands / Badlands (Biotechnica Flats) | Yes — outpost building, freezer room, camp gates | `mercenary`, `cyberware` (corpse harvesting), `vehicles_chop` | `-1380.131, -3615.641, 55.158` | `sites.json` site 346 `sts_bls_ina_08` | `ina_08_com_wraiths` (9); 9 roster units; 3 guard areas, 9 patrols | `[game-data]` `[wiki]` (gig *Trevor's Last Ride*) |
| 9 | **Wraiths' makeshift garage (EBM Petrochem Stadium)** | Chop-shop camp | Badlands / Badlands (edge of Arroyo) | No — open camp + garage shack | `vehicles_chop`, `mercenary` | `-1101.190, -2426.750, 25.230` | `markers.jsonl` `mws_sm_se5_07_camp` | `mws_se5_07_wraith_community` (7); 7 roster units; `#mws_se5_07_restrict_movement_area` | `[game-data]` `[wiki]` (gig *Shape of a Pony*) |
| 10 | **Sequoia & Gray outpost** | Street-corner trafficking cell | SantoDomingo / RanchoCoronado | No | `sex_work` (trafficking ring), `mercenary`, `vehicles_chop` | `787.639, -1578.047, 47.430` | `sites.json` site 170 `ma_std_rcr_18` | `ma_std_rcr_18_com_wraiths` (20); 20 roster units (19 human + 1 android) | `[game-data]` `[wiki]` |
| 11 | **Megapax Export warehouse** | Crime scene (Maelstrom stash hit) | Watson / Northside | No | `drugs` (stolen stash), `mercenary` | `-516.052, 2421.512, 56.531` | `sites.json` site 223 `ma_wat_nid_10` | `ma_wat_nid_10_com` (6); 6 roster units | `[game-data]` `[wiki]` |
| 12 | West Wind Estate hustle | Open-world ambush site | Pacifica / WestWindEstate | No | `mercenary` | `-2472.005, -2883.819, 42.965` | `sites.json` site 116 `ma_pac_wwd_08` | `ma_pac_wwd_08_com` (4); 4 roster units | `[game-data]` |
| 13 | West Wind Estate scav-den hit | Raid on a Scavenger den | Pacifica / WestWindEstate | No | `mercenary` | `-2799.222, -2711.590, 22.840` | `sites.json` site 112 `ma_pac_wwd_02` | `ma_pac_wwd_02_wraiths_com` (3); 3 roster units; 8 scav workspots | `[game-data]` |
| 14 | Badlands SE1 roadside hustle | Open-world ambush site | Badlands / Badlands | No | `mercenary` | `1031.367, -1493.523, 49.470` | `sites.json` site 6 `ma_bls_ina_06` | `ma_bls_ina_se1_06_com` (2); 2 roster units | `[game-data]` |

### 3.1 How the name→coordinate links were proven

Join order was **wiki `baseid` → `sites.json` code → node names → markers**, per
§1.1 item 1. That settled four gigs and one NCPD activity in one pass:

- `sts_bls_ina_03` → **Union Railroad Station** (*Gig: Flying Drugs*). Triggers
  `#ina_03_tr_near_antenna`, `#ina_03_tr_near_drone`, `#ina_03_tr_main_gate_chat`,
  `#ina_03_tr_turret_chat`, `#ina_03_tr_roof_patrol_start` and workspots
  `#ina_03_ws_js_antenna`, `#ina_03_ws_guard_10_fixing_turret` match the gig text
  (antenna, turrets, gateways, cameras). `[game-data]` `[wiki]`
- `sts_bls_ina_02` → **New American Autoworks**, Big Pete's garage
  (*Gig: Big Pete's Got Big Problems*). Triggers `#ina_02_tr_basement`,
  `…_petes_basement`, `…_by_pete_door`, `…_around_workshop`, `…_area_upper_floor`;
  the roster carries `Character.ina_02_officer`. The wiki gives the layout:
  workshop + basement + second-floor office, two `Militech Aegis X2` turrets at the
  front, six cameras, nine Wraiths (five outside, four inside) — exactly the 9
  roster units. `[game-data]` `[wiki]`
- `sts_bls_ina_06` → **Wraiths Outpost** at the Municipal Landfill, Edgewood Ln
  (*Gig: No Fixers*). Triggers `#ina_06_tr_camp_area`, `…_hostage_scene`,
  `…_garage_entrance`, `…_entering_through_main_path`. `[game-data]` `[wiki]`
- `sts_bls_ina_08` → **Wraiths' nest, Highway 101** (*Gig: Trevor's Last Ride*).
  Triggers `#ina_08_tr_camp_gates`, `…_in_freezer`, `…_find_body`, `…_outpost`.
  `[game-data]` `[wiki]`
- `ma_std_rcr_18` → **Sequoia & Gray**, *Suspected Organized Crime Activity:
  Desperate Sons-of-Bitches*. The raw sector carries the placement prefab
  `#c_santo_domingo/rancho_coronado/loc_ma_std_rcr_18_prefabQ5CFJTQ` — Rancho
  Coronado confirmed independently of any seed field. `[game-data]` `[wiki]`
- `ma_wat_nid_10` → **Megapax Export warehouse**, Northside (*Reported Crime:
  Dredged Up*). `[wiki]`
- `mws_se5_07` → the Wraith camp of *Shape of a Pony* (Update 2.1). Triggers
  `#mws_se5_07_car_search`, `…_chase`, `…_combat`, `…_investigation`,
  `…_tr_corpse`; the marker `mws_sm_se5_07_camp` is the camp itself.
  `[game-data]` `[wiki]`

**Marker/area-only places** (no `sites.json` row anywhere within 500 m):

- **Corp-Bud Cement Factory.** `sq004` = *Riders on the Storm*; the wiki lists the
  factory as a quest location and says Saul Bright "was briefly held here". The
  markers name it exactly: `sq004_mp_raffen_shiv_camp`,
  `sq004_mp_raffen_shiv_prison`, `sq004_mp_basement_entrance`,
  `sq004_mp_drone_01_gate`, `sq004_mp_drone_01a_guardhouse`,
  `sq004_mp_raffen_camp_lookout`. The five `sq004_com_*` Wraith communities sit on
  the same wall line. The seed centroid `(3003.6, -2394.3)` equals
  `sq004_com_wall` — a centroid, so it is **not** used as the anchor (§1.1 item 6);
  the camp marker 10 m away is. `[game-data]` `[wiki]`
- **Corp-Bud Mine.** `q103` = *Ghost Town*; wiki: "occupied by … the Wraiths, who
  had transformed a small section of the main tunnel into one of their
  strongholds", north entrance on Rocky Ridge's outskirts and south entrance due
  north of Union Railroad Station. `q103_12_sm_tunnel_ambush` (`1871.5, 1.4`) is
  due north of the station (`1882.6, -553.1`), which confirms the identification.
  `[game-data]` `[wiki]`
- **Poppy Farm.** The `sq021` area is literally `sq021_com_wrong_farm_wraiths`
  with 10 Wraiths, and markers `sq021_13_sm_wrong_farm` /
  `sq021_spwn_setup_wrong`. *The Hunt* presents Poppy Farm as the wrong choice
  where River and V "defeat some Wraiths"; Edgewood Farm (the correct one) is a
  separate area at `2398.8, -1328.0` with no Wraiths. The name link is therefore
  an inference from quest logic, not a label — hence `[inferred]`. Nearby
  `sq030_spwn_player_dam` (`z 183.5`) confirms the Laguna Bend dam/reservoir
  setting the wiki gives. `[game-data]` `[inferred]` `[wiki]`
- **Rocky Ridge.** `q103` = *Ghost Town*; `q103_mp_ghost_town` names the town.
  `q103_08_sm_ghost_town_plan` is the bar planning scene, `q103_mp_power_station`
  the fuel-station power point, `q103_09_sm_raffen_shiv` the Wraiths standing
  around. Which building is the bar vs the fuel station is `[inferred]` from the
  scene names; the wiki confirms both exist in the town with Wraiths on the
  fuel-station roof. `[game-data]` `[inferred]` `[wiki]`

### 3.2 Wraith-occupied generic sites (the filler pool)

Deduped `sites.json` rows with Wraith units that are **not** a named catalog
point. `suitability` tags are gameplay affordances, not lore.

| Site | Sub-district | Units | Suitability tags | Coordinates | Note |
| --- | --- | ---: | --- | --- | --- |
| `ma_std_rcr_18` | RanchoCoronado | 20 (19 + 1 android) | rooftop_access 80, officer_site 60 | `787.639, -1578.047, 47.430` | Largest Wraith garrison; ranked §6 #8 |
| `sts_bls_ina_08` | Badlands | 9 | raid_target 95, rooftop_access 80, vehicle_bay 65, arms_cache 62, market_stall 60, officer_site 60, club 55 | `-1380.131, -3615.641, 55.158` | Ranked §6 #9 |
| `mws_se5_07` | Badlands | 7 | raid_target 72, rooftop_access 66 | `-1101.190, -2426.750, 25.230` (community; anchor is 201 m off) | Ranked §6 #10 |
| `ma_wat_nid_10` | Northside | 6 | raid_target 87, rooftop_access 80, camera_net 61, stealth_entry 60, arms_cache 56 | `-516.052, 2421.512, 56.531` | Crime scene, not a holding |
| `ma_pac_wwd_08` | WestWindEstate | 4 | rooftop_access 80, raid_target 69 | `-2472.005, -2883.819, 42.965` | Hustle; 6.7 m from an Animals CC |
| `ma_pac_wwd_02` | WestWindEstate | 3 | raid_target 87, rooftop_access 72, officer_site 60, branch_office 45 | `-2799.222, -2711.590, 22.840` | Wraiths attacking a Scav den (`ma_pac_wwd_02_scav_*` workspots) |
| `ma_bls_ina_06` | Badlands | 2 | rooftop_access 80, camera_net 69, stealth_entry 65, raid_target 63 | `1031.367, -1493.523, 49.470` | Roadside hassle; anchor sits inside the Santo Domingo bbox |

Excluded from both tiers: site 163 `ma_std_rcr_109` (**one Wraith android, no
human** — §1.2 item 4) and site 4 `ma_bls_ina_04` (**one Wraith tagged
`victim`** at a Militech execution scene, `ma_bls_ina_se1_04_com_victim`).

---

## 4. Economic structure

### 4.1 Revenue streams → catalog locations

| Revenue stream | Code(s) | Catalog locations that produce it | Evidence / notes |
| --- | --- | --- | --- |
| Raiding, robbery, murder for hire | `mercenary` | Every holding; concentrated at the Cement Factory (1), Mine (2), Rocky Ridge (7) | "Wraiths happily hire themselves out for murder and even ransack entire towns"; income is "the spoils from their raids". `[wiki]` |
| Vehicle theft, garages, chop work | `vehicles_chop` | Cement Factory garage (1), New American Autoworks (4), Highway 101 nest (8), Shape-of-a-Pony garage (9), Mine (2) | "turning the facility into a garage and hideout for their vehicles"; Panam's Thorton stolen; a stolen Porsche held at a makeshift garage. `[wiki]` `[game-data]` |
| Contraband logistics, border running | `smuggling` | Poppy Farm (6), Union Railroad Station (3), Cement Factory (1) | Poppy Farm stored "equipment slated to be smuggled across the border"; transport contracts taken then broken with the cargo kept. `[wiki]` |
| Body-part and chrome harvesting | `cyberware` | Cement Factory basement (1), Highway 101 freezer (8) | "the basement of the complex as a location to hold and gut victims to sell their bodyparts and chrome". `[wiki]` |
| Drone hijacking / signal intrusion | `netrunning` | Union Railroad Station roof antenna (3) | The `b@d`-supplied **KI113R** virus drops cargo drones within antenna range. `[wiki]` |
| Drug-stash raiding | `drugs` | Megapax Export warehouse (11) | `b@d` sold them intel on a Maelstrom stash; the Northside scene is the aftermath. `[wiki]` `[game-data]` |
| Human trafficking | `sex_work` | Sequoia & Gray outpost (10) | Paul Craven is "a known leader within a NC human trafficking ring", Wraith-affiliated. Mapped to `sex_work` because §7's definition includes trafficking. `[wiki]` |

Two cautionary notes for the economy model:

- **There is no `robbery`/`raid` code.** `mercenary` ("muscle for hire, contract
  violence, robbery and heists") is the closest fit and is the Wraiths' largest
  stream. Reported in §8.4.
- **No listed place is a Wraith-run business.** Nothing here should receive a
  "legitimate business" yield multiplier based on a shopfront; the revenue is
  loot, ransom and fees. Big Pete's autoworks is a licensed shop the Wraiths
  garrison, and the Rocky Ridge bar is not theirs (formerly Jax's). `[wiki]`

### 4.2 Suppliers, customers, rivals

| Role | Party | Detail |
| --- | --- | --- |
| Supplier (intel, malware, fencing) | `b@d`, an independent netrunner | Provided intel on a Maelstrom stash and the KI113R drone-jamming virus. `[wiki]` |
| Customer (contract violence) | Rogue Amendiares (via Nash), unnamed city clients | Nash worked for Rogue as a merc and was paired with Panam; "Wraiths happily hire themselves out for murder". `[wiki]` |
| Customer (fenced goods) | Badlands black market, border buyers | Stolen cargo, chrome and vehicles; no vendor record exists in the extract. `[wiki]` `[inferred]` |
| Rival | **Aldecaldos** | Long war; the Wraiths attack Aldecaldo camps and the Aldecaldos assault the cement factory and the mine. `[wiki]` `[game-data]` |
| Rival | **The Breakers** (Raffen Shiv) | "pressing down on Wraith territory" around the cement factory. `[wiki]` |
| Rival / predator | **Militech** | Executes captured Wraiths (`cs_militech_execution*`, `la_sm_execution_03`, and a Wraith corpse tagged `victim` at an `ma_bls_ina_04` scene); convoys are Wraith targets. `[wiki]` `[game-data]` |
| Rival | **Maelstrom** | Stash raided on `b@d`'s intel (Northside). `[wiki]` |
| Rival | **6th Street** | Nash stole "a shipment for the 6th Street gang"; the Rancho Coronado cell operates inside 6th Street turf. `[wiki]` `[game-data]` |
| Rival | **Scavengers** | Wraiths hit a scav den in West Wind Estate (`ma_pac_wwd_02_scav_*` workspots) — the same trade, competing. `[game-data]` |
| Law | NCPD / SoCal Border Patrol | NCPD posts bounties on their cells; the border is Militech-policed. `[wiki]` `[game-data]` |

---

## 5. Headquarters recommendation

### Primary HQ: **Corp-Bud Cement Factory** — Badlands (Sierra Sonora)

Coordinates: `3007.724, -2385.058, 124.630` `[game-data]`
`markers.jsonl` `sq004_mp_raffen_shiv_camp`.

Rationale:

1. **The wiki calls it "this stronghold".** Of the four locations on the faction
   page, the cement factory's own article says the Wraiths installed rudimentary
   defences, "turning the facility into a garage and hideout for their vehicles.
   From this stronghold, the roadgang was planning to raid different places on
   the outskirts of Night City." `[wiki]`
2. **It is a real seat with rooms to assign, not a single venue.** Node and marker
   evidence gives a perimeter wall, gate + guardhouse, drone overwatch, an
   infiltration route, a basement entrance, a prison and a yard: `sq004_com_wall`,
   `sq004_mp_raffen_shiv_camp`, `sq004_mp_raffen_shiv_prison`,
   `sq004_mp_basement_entrance`, `sq004_mp_drone_01_gate`,
   `sq004_mp_drone_01a_guardhouse`, `sq004_mp_drone_03_main`,
   `sq004_mp_drone_05_passage`. That is exactly the structure an org layer wants.
   `[game-data]`
3. **It covers the two defining revenue streams in one building:** vehicles
   (garage) and chrome (the basement gutting room), plus planning space for raids.
   `[wiki]`
4. **Heaviest single-place game data of any Wraith point:** five Wraith
   communities totalling **51 entries**, plus a chase corridor and a lookout
   (`sq004_mp_raffen_camp_lookout` at `3079.7, -2292.9`). `[game-data]`
5. **The seed already puts the faction here.** `bls_wraith_compound` owns it and
   `cc_bls_wraith_compound` is **10.1 m** away, so no new map plumbing is needed —
   only an activation. (The seed anchor is a centroid; this doc anchors on the
   camp marker instead.) `[game-data]`

Trade-off: **remote and marker-only.** It sits 2.4 km south of Rocky Ridge in
Sierra Sonora at `z ≈ 125`, at the far edge of the playable map, and it has no
`sites.json` row — so there are no guard volumes, doors or patrol splines to hook
a prototype into, only markers and communities. It is also quest-gated
(*Riders on the Storm*). If the mod needs a *site-backed* seat with full records,
the functional HQ is Union Railroad Station (below) and the factory stays the
prestige flag.

### Alternate 1: **Union Railroad Station** — Red Peaks

Coordinates `1882.553, -553.140, 54.852` `[game-data]` site 341 `sts_bls_ina_03`.

The best-instrumented Wraith property: 16 roster units, 4 guard areas
(`#sts_bls_ina_03_RMA_inside`, `_leftside`, `_rightside`, `#ina_03_ga`), 9 patrol
splines, 56 workspots, 20 triggers and always-present world geometry with
turrets and cameras. Clean ownership (`default_faction_id = 8`,
`initial_owner_faction_id = 8`). It loses on identity: a rail station with an
antenna is a forward operations base, not a seat, and its economy is one
technique (`netrunning`), not the gang's whole model. `[game-data]` `[wiki]`

### Alternate 2: **Corp-Bud Mine** — Rocky Ridge Plains

Coordinates `1871.475, 1.355, 55.074` `[game-data]` `q103_12_sm_tunnel_ambush`.

The other canonical "stronghold": the mine tunnel Nash used as a hideout, target
of the *Ghost Town* assault, with 14 area entries. It reads as a bunker, which is
fitting, but the capture volume is a tunnel mouth and the wiki says the Wraiths
only "transformed a small section of the main tunnel". It loses to the factory on
capacity and to the station on records. `[wiki]` `[game-data]`

### Overruled / downgraded suggestions

- **Rocky Ridge as HQ** — a ghost town they *visit*: the bar and fuel station are
  third-party buildings, the Wraiths position on the roof and keep a secret
  office. It is a haunt and a lookout, not a seat. Keep as a high-relevance point.
  `[wiki]`
- **Sunset Motel as HQ** — the seed gives this sub-territory to the Wraiths, but
  the motel is Noah's, neutral, and a *Ghost Town* meeting place. It is not a
  Wraith holding at all (§8.1). `[wiki]`
- **Poppy Farm as HQ** — a stash with a farmhouse; too small and too far south.
  `[wiki]`
- **Wraiths Outpost (landfill) as HQ** — a fenced dump outpost built to hold one
  hostage; good capture point, poor seat. `[wiki]`
- **The "Wraiths Badlands Compound" as a separate place** — there is no second
  compound. The seed name points at the cement factory; do not seed it twice.

---

## 6. Priority list of control points

Ranked by how well each place serves as a capturable Wraith control point.
"CC" = nearest entry in `data/control_centers.json` (active or not); distance is
horizontal metres. Relevance reflects lore + revenue + record richness, not raw
unit count.

| Rank | Control point | Rel. (1–5) | District / sub-district | Coordinates | Existing CC overlap | Why |
| ---: | --- | :---: | --- | --- | --- | --- |
| 1 | **Corp-Bud Cement Factory** | 5 | Badlands / Badlands | `3007.724, -2385.058, 124.630` | `cc_bls_wraith_compound`, **10.1 m** (Wraiths) | Canon "stronghold"; wall, gate, guardhouse, prison, basement chop room; 51 entries |
| 2 | **Corp-Bud Mine** | 5 | Badlands / Badlands | `1871.475, 1.355, 55.074` | `cc_bls_rocky_ridge`, 685.9 m (Wraiths) | Nash's stronghold; *Ghost Town* assault; 14 entries |
| 3 | **Union Railroad Station** | 4 | Badlands / Badlands | `1882.553, -553.140, 54.852` | `cc_bls_sunset_motel`, 310.0 m (Wraiths) | 16 units; drone-hijack antenna; turrets/cameras; 9 patrols; the richest site record |
| 4 | **New American Autoworks** | 4 | Badlands / Badlands | `-142.756, -4419.236, 58.870` | `cc_bls_solar_station`, 828.0 m (**Militech**) | Only Wraith site with `is_interior=1`; 11 doors, 4 devices, 7 guard areas, 6 patrols; Big Pete's Wraith-guarded garage |
| 5 | **Wraiths Outpost (landfill)** | 4 | Badlands / Badlands | `2169.702, -1637.889, 67.000` | `cc_bls_sunset_motel`, 1046.6 m (Wraiths) | Named Wraith outpost; hostage-holding room; 3 doors, 3 devices, 6 patrols |
| 6 | **Poppy Farm** | 3 | Badlands / Badlands | `874.946, -3579.587, 180.395` | `cc_rcr_piez_plaza`, 1641.7 m (**6th Street**) | Cross-border smuggling stash; 10 Wraiths; named in the faction list |
| 7 | **Rocky Ridge** | 3 | Badlands / Badlands | `2580.302, -41.797, 80.810` | `cc_bls_rocky_ridge`, 29.5 m (Wraiths) | Named Wraith haunt; bar + fuel-station lookout; Nash's secret office; cheap rename of an existing CC |
| 8 | **Sequoia & Gray outpost** | 3 | SantoDomingo / RanchoCoronado | `787.639, -1578.047, 47.430` | `cc_rcr_mallagra_depot`, 22.2 m (**6th Street**) | Largest garrison (20); a Wraith foothold *inside* the city; trafficking revenue |
| 9 | **Wraiths' nest, Highway 101** | 2 | Badlands / Badlands | `-1380.131, -3615.641, 55.158` | `cc_bls_biotechnica_flats`, 794.0 m (**Biotechnica**) | Corpse-freezer outpost; 9 units; no proper name in the wiki |
| 10 | **Shape-of-a-Pony garage** | 2 | Badlands / Badlands | `-1101.190, -2426.750, 25.230` | `cc_dt_terra_cognita`, 288.0 m (**Voodoo Boys**) | Chop-shop camp from a 2.1 mini-world-story; 7 units; camp marker |

### Test control point for the first in-game test: **New American Autoworks (Jackson Plains)**

Site 340 `sts_bls_ina_02`, coordinates `-142.756, -4419.236, 58.870`,
`[game-data]` `data/sites/sites.json`.

Why this and not the HQ:

- **Clean ownership.** `default_faction_id = 8` with **9 Wraith roster units**
  confirmed. `initial_owner_faction_id` reads 21 (Militech) but that field is a
  seeded sub-territory row, not a per-site owner (§2.2) — the same artifact that
  puts site 344 under Militech. The wiki independently says the area "was heavily
  guarded by Wraiths". Eviction has no ambiguity. `[game-data]` `[wiki]`
- **The only Wraith site with `is_interior` set** (and here the flag is
  reliable), plus node evidence: `#ina_02_tr_basement`,
  `#ina_02_tr_petes_basement`, `#ina_02_tr_by_pete_door`,
  `#ina_02_tr_around_workshop`, `#ina_02_tr_area_upper_floor`,
  `#ina_02_tr_interior_area`, `#ina_02_tr_area_ground_floor`. It is the garage
  from *Big Pete's Got Big Problems*: first-floor workshop, staircase, basement,
  second-floor office. `[game-data]` `[wiki]`
- **The richest capture-relevant record set of any Wraith site:** 7 guard areas,
  19 triggers, 39 workspots, 6 patrol splines, **11 doors** and **4 devices**.
  Doors and devices are exactly what a lock/alarm/defence prototype needs; only
  the landfill outpost comes close (3 doors, 3 devices). `[game-data]`
- **A natural two-tier capture volume with an escape route.** Two front turrets
  and six cameras, a main workshop floor, a basement, and a utility tunnel that
  exits behind the communications tower — so the test can validate both a ground
  capture and a reinforcement/egress lane. `[wiki]` `[game-data]`
- **Not the HQ and not an alternate HQ**, per §3.8. `[game-data]`

Trade-off: every Wraith holding is a quest location, and this one is
quest-gated behind a Dakota gig; the nearest CC is 828 m away and **Militech-owned**
(`cc_bls_solar_station`), so the seed must relocate the faction's active CC onto
the garage (§3.8 says that is allowed, but it is not free). **Fallback 1 if the
garage is gated: Union Railroad Station** (`sts_bls_ina_03`, 16 units, 310 m from
a Wraith-owned active CC, always-present geometry). **Fallback 2: Wraiths
Outpost** (`sts_bls_ina_06`, 3 doors, 3 devices, hostage room).

---

## 7. Per-sub-district counts

This is the number to feed yield balancing. It counts **distinct named places**
the Wraiths own, run or habitually occupy — not quest corridors, not ambient
spawn areas and not crime scenes. `Filler` is the deduped occupied-site count
minus any site already counted as a named place (§8).

| Sub-district | Named lore-relevant places | Which ones | Occupied sites (deduped) | Filler | Noteworthy interiors |
| --- | ---: | --- | ---: | ---: | --- |
| Badlands | **7** | Corp-Bud Cement Factory, Corp-Bud Mine, Union Railroad Station, New American Autoworks, Wraiths Outpost, Poppy Farm, Rocky Ridge | 6 | 3 | Cement-factory yard/basement/prison; mine tunnel; Autoworks garage + basement; landfill sheds; railroad building |
| RanchoCoronado | 0 | Sequoia & Gray is an unnamed trafficking cell | 1 | 1 | None |
| Northside | 0 | Megapax Export warehouse is a crime scene | 1 | 1 | None |
| WestWindEstate | 0 | Hustle + scav-den hit only | 2 | 2 | None |
| **Total** | **7** | | **10** | **7** | |

Reconciliation (`named + filler = 14`):

- **12 roster sites − 2 excluded = 10 occupied sites.** Excluded: site 163
  (one android, no human) and site 4 (one Wraith corpse at a Militech execution).
- **7 filler = 10 occupied − 3 site-backed named places** (`sts_bls_ina_03`,
  `sts_bls_ina_02`, `sts_bls_ina_06`).
- **7 named = 3 site-backed + 4 marker/area-only** (Cement Factory, Mine, Poppy
  Farm, Rocky Ridge).
- `10 + 4 = 14 = 7 named + 7 filler`. ✓

Area-only presence **not** counted anywhere above (no site, no named place): the
`sq027` Aldecaldo-camp assault (30 entries), the `ma_bls_ina_se1_*` /
`ma_bls_ina_se5_*` ambient highway communities (16 areas / 87 entries), the
dynamic `cs_*` events (convoy ambush, handcuffed prisoners, executions), the
`sa_ep1_101` / `sa_ep1_159` Phantom Liberty communities, and the races
(`mq056`/`sq024`, one Wraith driver each). These should be contested turf or
event spawns, never owned economy.

Interpretation for yield: **Badlands is the faction.** All seven named places are
there, and the HQ plus the two strongholds should carry the faction's high-yield
military/loot economy. Rancho Coronado is the only *city* holding and should read
as a racket (trafficking) rather than a district. West Wind Estate and Northside
are presence-only — the Wraiths raiding someone else's turf — and should not be
owned territory. `[inferred]`

---

## 8. Gaps and uncertainties

1. **The seed's "Sunset Motel" sub-territory is mis-attributed, like Militech's
   Gold Beach Marina.** `bls_sunset_motel` (`initial_owner_faction_id 8`) is
   anchored on the motel's dataterm (`cc_bls_sunset_motel`, `is_active=1`,
   `1634.2, -738.7`), but the motel is Noah's and neutral in lore, and the only
   Wraith properties bucketed into this sub-territory are **Union Railroad
   Station** (310 m) and the landfill outpost (1.0 km). Either move that CC onto
   Union Railroad Station or treat the motel as contested ground. `[game-data]`
   `[wiki]`
2. **The cement factory is marker-only and quest-gated.** No `sites.json` row, no
   doors, no guard volumes; its evidence is markers and `sq004` communities. The
   seed anchor (`3003.6, -2394.3`) is a **centroid** equal to `sq004_com_wall`, so
   it cannot be used as a coordinate source; the camp marker 10 m away can. `[game-data]`
3. **`sites.json` does not represent the Badlands minor activities.** **16 of the
   55 areas** are `ma_bls_ina_se1_11…21` / `ma_bls_ina_se5_03…16` highway
   communities, each with a `*_spawn_point` or `*_lookat` marker and several with
   `la_sm_execution_03`, yet there is **no** corresponding `sites.json` code (the
   file's SE1 rows stop at `ma_bls_ina_08`, and it has no SE5 rows at all). They
   are ambient spawns, so they are excluded — but a later pass that wants a
   complete "encounter" layer will need a Badlands sector extract. `[game-data]`
4. **There is no `robbery`/`raid` revenue code.** The Wraiths' dominant income is
   raiding — loot from convoys, towns and camps — and the vocabulary offers only
   `mercenary` ("robbery and heists") and `protection`. I used `mercenary`
   everywhere. A future `raid`/`loot` code would describe this faction far better
   than any existing one. `[inferred]`
5. **Poppy Farm's name link is inferred, and one farm record is a trap.**
   `sq021_com_wrong_farm_wraiths` + `sq021_13_sm_wrong_farm` say "wrong farm with
   Wraiths"; the wiki says choosing Poppy is the wrong choice and the duo "defeat
   some Wraiths" there, while Edgewood Farm (`2398.8, -1328.0`) has no Wraiths.
   Convincing, but no record says "Poppy Farm". Do **not** use
   `mirror_sm_scene_farmhouse` (`1819.6, -1080.6`) or `fb_sm_farmhouse_teleport`
   as Poppy Farm evidence: they belong to **Ingalls Farm**, the third location of
   *Riders on the Storm*, 2.7 km away and Aldecaldo-friendly. Poppy Farm also has
   no proven interior. `[inferred]` `[game-data]`
6. **Rocky Ridge bar vs fuel station is unseparated.** `q103_08_sm_ghost_town_plan`
   looks like the bar scene and `q103_mp_power_station` like the fuel station, but
   no node name says "bar" or "fuel_station". Only the town anchor
   (`q103_mp_ghost_town`, 29.5 m from the CC) is safe to seed. `[inferred]`
7. **`roster` units at two sites are not garrisons.** Site 170 lists one
   `rcr_wraiths_android_android2_pulsar_ma` among 20, and site 163 is a single
   `rcr_wraiths_android` with no human at all — §1.2 item 4 applies. Site 4's one
   Wraith is a `victim` at a Militech execution. Of the raw 85 units, **82 are
   humans in a garrison role**. `[game-data]`
8. **Site 324's anchor is 201 m from its community.** The `mws_se5_07` anchor
   (`-913.211, -2362.664`) is the questphase anchor; the Wraith camp is at
   `-1101.190, -2426.750`. Using the anchor would place the point in the wrong
   spot and inside the Santo Domingo bbox. This is a larger error than the ~110 m
   §1.1 item 7 warns about, and it is a *camp*, not an interior. `[game-data]`
9. **`ma_bls_ina_06` (site 6) is a Badlands token inside a city bbox.** Its
   `source_path` is `badlands/inland_avenue_se1`, but `(1031, -1493)` is inside
   the Santo Domingo bbox and `areas.jsonl` labels its community `santo_domingo`.
   I followed `source_path` (§1.2 item 1). The point contributes 2 units; if the
   seeder disagrees, move it to RanchoCoronado and nothing else changes. `[game-data]`
10. **Shape of a Pony's district is contested.** The quest infobox says
    `district = Badlands`, `sub_district = Biotechnica Flats`, but the wiki text
    says the car is near "a makeshift garage south of the EBM Petrochem Stadium"
    in Arroyo. The site's `source_path` (`badlands/se5`) and its community
    (`-1101, -2427`, outside every city bbox) say Badlands. Treated as Badlands;
    expect it to read as an Arroyo-adjacent camp on the map. `[game-data]` `[wiki]`
11. **`sa_ep1_101` is unexplained.** Ten Wraiths at `-2032, -4582`, no site, no
    marker beyond `dead_zone_marker*`, no wiki page, and `sa_ep1_159` (5) 100 m
    away. Phantom Liberty-era content the extractor does not model. Excluded. `[game-data]`
12. **No vendor or loot records.** "What they fence" is `[wiki]`/`[inferred]`;
    the extract has suitabilities only. `[game-data]`
13. **The wiki gives the Wraiths no headquarters and an incomplete location list.**
    Its four 2077 locations omit the mine, Big Pete's autoworks and the landfill
    outpost, all of which have their own wiki articles and in-game sites. The HQ
    in §5 is therefore derived from the "this stronghold" wording, not from an
    infobox. `[wiki]`
14. **`faction_headquarters.json` has no Wraiths row.** A seeder reading only that
    file finds nothing; this doc supplies the row from `sq004_mp_raffen_shiv_camp`.
    `[game-data]`
15. **Three named points land on rival-owned existing CCs.** Poppy Farm's nearest
    CC is 6th Street (`cc_rcr_piez_plaza`), the Shape-of-a-Pony camp's is Voodoo
    Boys (`cc_dt_terra_cognita`), and the Highway 101 nest's is Biotechnica
    (`cc_bls_biotechnica_flats`). None of those is a retarget candidate (§1.1
    item 10); they are new points or nothing. `[game-data]`
16. **`is_interior` is unset for the two strongest points.** The cement factory
    and the mine have no site record at all, and Union Railroad reads
    `is_interior = 0` despite an inside guard volume and interior workspots. Only
    New American Autoworks has the flag set. Interiors were proven from node names
    throughout (§1.2 item 15). `[game-data]`

---

## 9. Sources

Local:

- `dist/extract/markers.jsonl` — `sq004_mp_raffen_shiv_camp`,
  `sq004_mp_raffen_shiv_prison`, `sq004_mp_basement_entrance`,
  `sq004_mp_drone_01_gate`, `sq004_mp_drone_01a_guardhouse`,
  `sq004_mp_raffen_camp_lookout`, `q103_12_sm_tunnel_ambush`,
  `q103_mp_ghost_town`, `q103_08_sm_ghost_town_plan`, `q103_mp_power_station`,
  `q103_09_sm_raffen_shiv`, `sq021_13_sm_wrong_farm`, `mws_sm_se5_07_camp`,
  `mirror_sm_scene_farmhouse`, `mirror_sm_scene_sunset_panam`.
- `dist/extract/areas.jsonl` — 55 areas / 51 dominant / 327 entries; `sq004_com_*`,
  `q103_com_*`, `sq027_com_*`, `sq021_com_wrong_farm_wraiths`, `ma_*_com`, `cs_*`.
- `dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_0.streamingsector.json`
  — `#c_santo_domingo/rancho_coronado/loc_ma_std_rcr_18_prefabQ5CFJTQ` (Rancho
  Coronado placement, site 170). No Badlands prefabs are present in the three
  `always_loaded` sectors.
- `data/sites/sites.json` (sites 4, 6, 112, 116, 163, 170, 223, 324, 340, 341,
  344, 346), `rosters.json`, `communities.json`,
  `guards/triggers/spots/patrols/doors/devices.json`, `suitabilities.json`.
- `data/{factions,districts,sub_territories,landmarks,control_centers,spawn_points,faction_headquarters}.json`.
- `docs/research/factions/METHOD.md`, `docs/research/factions/tyger-claws.md`,
  `docs/research/factions/militech.md`.

Wiki (MediaWiki API, `action=parse&prop=wikitext`, 2026-11-25):

- [Wraiths](https://cyberpunk.fandom.com/wiki/Wraiths) ·
  [Raffen Shiv](https://cyberpunk.fandom.com/wiki/Raffen_Shiv) ·
  [Nash](https://cyberpunk.fandom.com/wiki/Nash)
- [Corp-Bud Cement Factory](https://cyberpunk.fandom.com/wiki/Corp-Bud_Cement_Factory) ·
  [Corp-Bud Mine](https://cyberpunk.fandom.com/wiki/Corp-Bud_Mine) ·
  [Corp-Bud Railroad Station](https://cyberpunk.fandom.com/wiki/Corp-Bud_Railroad_Station)
- [Union Railroad Station](https://cyberpunk.fandom.com/wiki/Union_Railroad_Station) ·
  [Poppy Farm](https://cyberpunk.fandom.com/wiki/Poppy_Farm) ·
  [Rocky Ridge](https://cyberpunk.fandom.com/wiki/Rocky_Ridge) ·
  [Rocky Ridge Bar](https://cyberpunk.fandom.com/wiki/Rocky_Ridge_Bar) ·
  [Rocky Ridge Fuel Station](https://cyberpunk.fandom.com/wiki/Rocky_Ridge_Fuel_Station) ·
  [Sunset Motel](https://cyberpunk.fandom.com/wiki/Sunset_Motel) ·
  [Night City Municipal Landfill](https://cyberpunk.fandom.com/wiki/Night_City_Municipal_Landfill)
- [Wraiths Outpost](https://cyberpunk.fandom.com/wiki/Wraiths_Outpost) ·
  [New American Autoworks (Jackson Plains)](https://cyberpunk.fandom.com/wiki/New_American_Autoworks_(Jackson_Plains)) ·
  [Edgewood Farm](https://cyberpunk.fandom.com/wiki/Edgewood_Farm)
- Gigs / quests (baseid-verified): [Flying Drugs](https://cyberpunk.fandom.com/wiki/Gig:_Flying_Drugs)
  (`sts_bls_ina_03`), [Big Pete's Got Big Problems](https://cyberpunk.fandom.com/wiki/Gig:_Big_Pete%27s_Got_Big_Problems)
  (`sts_bls_ina_02`), [No Fixers](https://cyberpunk.fandom.com/wiki/Gig:_No_Fixers)
  (`sts_bls_ina_06`), [Trevor's Last Ride](https://cyberpunk.fandom.com/wiki/Gig:_Trevor%27s_Last_Ride)
  (`sts_bls_ina_08`), [Shape of a Pony](https://cyberpunk.fandom.com/wiki/Shape_of_a_Pony)
  (`mws_se5_07`), [Desperate Sons-of-Bitches](https://cyberpunk.fandom.com/wiki/Suspected_Organized_Crime_Activity:_Desperate_Sons-of-Bitches)
  (`ma_std_rcr_18`), [Dredged Up](https://cyberpunk.fandom.com/wiki/Reported_Crime:_Dredged_Up)
  (`ma_wat_nid_10`), [Ghost Town](https://cyberpunk.fandom.com/wiki/Ghost_Town)
  (`q103_warhead`), [Riders on the Storm](https://cyberpunk.fandom.com/wiki/Riders_on_the_Storm)
  (`sq004_riders_on_the_storm`), [Queen of the Highway](https://cyberpunk.fandom.com/wiki/Queen_of_the_Highway)
  (`sq027`), [The Hunt](https://cyberpunk.fandom.com/wiki/The_Hunt)
  (`sq021_sick_dreams`).

---

## 10. Machine-readable block

Strict JSON for seeding (contract in [`METHOD.md`](./METHOD.md) §10). Every
coordinate was verified against the local record named in `source` on
2026-11-25; none came from the wiki. `null` means `TBD`, never `0`.

```json
{
  "faction_code": "wraiths",
  "hq": {
    "name": "Corp-Bud Cement Factory",
    "district": "Badlands",
    "sub_district": "Badlands",
    "x": 3007.724,
    "y": -2385.058,
    "z": 124.63,
    "source": "dist/extract/markers.jsonl sq004_mp_raffen_shiv_camp",
    "confidence": "game-data+wiki"
  },
  "alternate_hqs": [
    {
      "name": "Union Railroad Station",
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": 1882.553,
      "y": -553.14,
      "z": 54.852,
      "source": "data/sites/sites.json site 341 sts_bls_ina_03",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Corp-Bud Mine",
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": 1871.475,
      "y": 1.355,
      "z": 55.074,
      "source": "dist/extract/markers.jsonl q103_12_sm_tunnel_ambush",
      "confidence": "game-data+wiki"
    }
  ],
  "test_control_point": {
    "name": "New American Autoworks (Jackson Plains)",
    "district": "Badlands",
    "sub_district": "Badlands",
    "x": -142.756,
    "y": -4419.236,
    "z": 58.87,
    "source": "data/sites/sites.json site 340 sts_bls_ina_02",
    "confidence": "game-data+wiki"
  },
  "control_points": [
    {
      "rank": 1,
      "name": "Corp-Bud Cement Factory",
      "type": "gang_stronghold",
      "relevance": 5,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": 3007.724,
      "y": -2385.058,
      "z": 124.63,
      "source": "dist/extract/markers.jsonl sq004_mp_raffen_shiv_camp",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["mercenary", "vehicles_chop", "cyberware", "smuggling", "drugs"],
      "nearest_cc_code": "cc_bls_wraith_compound",
      "nearest_cc_m": 10.1
    },
    {
      "rank": 2,
      "name": "Corp-Bud Mine",
      "type": "gang_stronghold",
      "relevance": 5,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": 1871.475,
      "y": 1.355,
      "z": 55.074,
      "source": "dist/extract/markers.jsonl q103_12_sm_tunnel_ambush",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["mercenary", "vehicles_chop", "smuggling"],
      "nearest_cc_code": "cc_bls_rocky_ridge",
      "nearest_cc_m": 685.9
    },
    {
      "rank": 3,
      "name": "Union Railroad Station",
      "type": "rail_station_outpost",
      "relevance": 4,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": 1882.553,
      "y": -553.14,
      "z": 54.852,
      "source": "data/sites/sites.json site 341 sts_bls_ina_03",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["netrunning", "smuggling", "mercenary"],
      "nearest_cc_code": "cc_bls_sunset_motel",
      "nearest_cc_m": 310.0
    },
    {
      "rank": 4,
      "name": "New American Autoworks (Jackson Plains)",
      "type": "autoworks_garage",
      "relevance": 4,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": -142.756,
      "y": -4419.236,
      "z": 58.87,
      "source": "data/sites/sites.json site 340 sts_bls_ina_02",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["vehicles_chop", "mercenary", "smuggling"],
      "nearest_cc_code": "cc_bls_solar_station",
      "nearest_cc_m": 828.0
    },
    {
      "rank": 5,
      "name": "Wraiths Outpost (Municipal Landfill)",
      "type": "gang_outpost",
      "relevance": 4,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": 2169.702,
      "y": -1637.889,
      "z": 67.0,
      "source": "data/sites/sites.json site 344 sts_bls_ina_06",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["mercenary", "smuggling"],
      "nearest_cc_code": "cc_bls_sunset_motel",
      "nearest_cc_m": 1046.6
    },
    {
      "rank": 6,
      "name": "Poppy Farm",
      "type": "smuggling_stash",
      "relevance": 3,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": 874.946,
      "y": -3579.587,
      "z": 180.395,
      "source": "dist/extract/markers.jsonl sq021_13_sm_wrong_farm",
      "confidence": "game-data+inferred+wiki",
      "interior": false,
      "revenue_streams": ["smuggling"],
      "nearest_cc_code": "cc_rcr_piez_plaza",
      "nearest_cc_m": 1641.7
    },
    {
      "rank": 7,
      "name": "Rocky Ridge (bar and fuel station)",
      "type": "ghost_town_haunt",
      "relevance": 3,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": 2580.302,
      "y": -41.797,
      "z": 80.81,
      "source": "dist/extract/markers.jsonl q103_mp_ghost_town",
      "confidence": "game-data+inferred+wiki",
      "interior": true,
      "revenue_streams": ["mercenary", "smuggling", "vehicles_chop"],
      "nearest_cc_code": "cc_bls_rocky_ridge",
      "nearest_cc_m": 29.5
    },
    {
      "rank": 8,
      "name": "Sequoia and Gray outpost",
      "type": "trafficking_cell",
      "relevance": 3,
      "district": "SantoDomingo",
      "sub_district": "RanchoCoronado",
      "x": 787.639,
      "y": -1578.047,
      "z": 47.43,
      "source": "data/sites/sites.json site 170 ma_std_rcr_18",
      "confidence": "game-data+wiki",
      "interior": false,
      "revenue_streams": ["sex_work", "mercenary", "vehicles_chop"],
      "nearest_cc_code": "cc_rcr_mallagra_depot",
      "nearest_cc_m": 22.2
    },
    {
      "rank": 9,
      "name": "Wraiths' nest, Highway 101",
      "type": "roadside_outpost",
      "relevance": 2,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": -1380.131,
      "y": -3615.641,
      "z": 55.158,
      "source": "data/sites/sites.json site 346 sts_bls_ina_08",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["mercenary", "cyberware", "vehicles_chop"],
      "nearest_cc_code": "cc_bls_biotechnica_flats",
      "nearest_cc_m": 794.0
    },
    {
      "rank": 10,
      "name": "Wraiths' makeshift garage (EBM Petrochem Stadium)",
      "type": "makeshift_garage",
      "relevance": 2,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": -1101.19,
      "y": -2426.75,
      "z": 25.23,
      "source": "dist/extract/markers.jsonl mws_sm_se5_07_camp",
      "confidence": "game-data+wiki",
      "interior": false,
      "revenue_streams": ["vehicles_chop", "mercenary"],
      "nearest_cc_code": "cc_dt_terra_cognita",
      "nearest_cc_m": 288.0
    }
  ],
  "subdistrict_counts": {
    "Badlands": {"named": 7, "filler": 3},
    "RanchoCoronado": {"named": 0, "filler": 1},
    "Northside": {"named": 0, "filler": 1},
    "WestWindEstate": {"named": 0, "filler": 2}
  }
}
```
