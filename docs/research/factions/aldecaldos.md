# Aldecaldos — Lore-Relevant Control Points

Status: batch-3 research run, 2026-11-25. One faction, one document.
Scope: lore-relevant, capturable places for the Aldecaldos (`aldecaldos`, faction
id 9, affiliation enum `Aldecaldos`), with honest per-sub-district counts.
Method: [`METHOD.md`](./METHOD.md), including the §1.1 and §1.2 corrections.
Nearest-control-centre distances were recomputed after the parallel seed
retarget of 2026-11-25 01:28 (`data/{sub_territories,landmarks,control_centers}.json`).

Evidence tags:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Position, site, community, roster or marker record read from `dist/extract/` or `data/sites/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/artbook/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | Reasoning links a named place to a game record; reasoning stated | Weak, flagged |

No coordinate below is guessed. Every `(x, y, z)` is copied from a named marker,
site or community record, or is `TBD`.

---

## 1. Summary

The Aldecaldos are one of the largest nomad nations in North America and a
member of the Seven Nations; the Night City branch in 2077 is the **Bright
Family** led by Saul Bright and, later, Panam Palmer. `[wiki]` They are not a
corner gang: they are a mobile clan whose economic base is **salvage and
reconstruction of dead cities, seasonal farm labour, bootlegging, and
long-haul smuggling / passenger transport across state borders in armed
convoys**. `[wiki]` In the city their visible presence is a Badlands camp, a
fixer autoshop, and the border route — not urban real estate.

The 2077 game footprint is correspondingly thin:

- **One seeded holding**: sub-territory 83 `bls_aldecaldos_camp`
  ("Aldecaldos Nomad Camp"), owner 9, seed centroid `(3412.9, -360.1, 120.3)`,
  with active capital control centre `cc_bls_aldecaldos_camp`. `[game-data]`
- **Five roster sites / eight units** across the whole map, and every one of
  them is a quest scene, not a base. `[game-data]`
- **61 community areas / 265 Aldecaldos entries**, 40 of them in the Badlands;
  the rest are race scenes, the Phantom Liberty border cameo, and a handful of
  city crowd scenes. `[game-data]`
- **No `faction_headquarters.json` row** and no urban storefront. `[game-data]`

The named catalog therefore has **three places**: the old **Mobile Camp**
(Act 2), the later **Nomad Camp** (post-*Riders on the Storm*), and
**DaKota**, Dakota Smith's autoshop/fixer hub. The SoCal Border Crossing is the
faction's main route node, but it is Militech/SoCal Border Patrol property and
is treated as a corridor, not a holding (§1.2 item 9).

The weight sits in **Badlands / Badlands** only. The old camp is the only place
the seed already owns, and it is the expected HQ.

---

## 2. Territory

### 2.1 Districts

| Evidence kind | Result |
| --- | --- |
| Wiki/lore | A mobile Badlands clan; the 2077 campsites are in the eastern Badlands / Rocky Ridge Plains. No 2077 city base. `[wiki]` |
| Vanilla panel | `data/districts.json`: `Badlands` `vanilla_gangs = ["Aldecaldos", "Wraiths"]`; no city district lists them. |
| Game-data counts | 61 areas (50 dominant) / 265 entries; 40 areas / 224 entries in the Badlands. 1 owned sub-territory, 5 roster sites / 8 units. |

### 2.2 Sub-district presence

Counts are from `dist/extract/areas.jsonl` (any area whose `faction_counts`
contains `aldecaldos`; "dominant" means `dominant_faction == aldecaldos`). The
left half groups by the raw `district_code`; the right half attributes the five
roster sites by their `source_path` and the catalog points by their records.
The two do **not** line up, which is the point of the caveat in §2.3.

| Raw `district_code` | Areas (dominant) | Entries | Catalog points (named / filler) |
| --- | ---: | ---: | --- |
| Badlands | 40 (40) | 224 | **3 / 3** |
| Heywood | 5 (1) | 7 | 0 / 0 |
| Watson | 5 (2) | 8 | 0 / 1 (site 409 is Northside) |
| Pacifica | 4 (3) | 11 | 0 / 0 |
| SantoDomingo | 3 (3) | 4 | 0 / 1 (site 388 is RanchoCoronado) |
| Westbrook | 3 (0) | 6 | 0 / 0 |
| Dogtown | 1 (1) | 5 | 0 / 0 |
| **Total** | **61 (50)** | **265** | **3 / 5** |

Roster sites (5): `sts_wat_nid_03` (Northside), `sts_bls_ina_08`,
`ma_bls_ina_07`, `sts_bls_ina_09` (Badlands), `sts_std_rcr_03`
(RanchoCoronado).

Two raw labels are misleading: `nid_03_com_nomads` (3 Aldecaldos, the Northside
meet-up) is labelled `badlands`, and `rcr_03_com_nomad` (2 Aldecaldos, the
RanchoCoronado meeting) is labelled `santo_domingo`. The roster sites are
separately attributed by `source_path`. The 61 areas do **not** become filler:
they are communities/quest scenes, not sites (see §7).

**Reading the counts.** Almost all of the 265 entries are story scenes:

- `q114` (7 areas, the *Star* ending and the new camp) and `sq027`
  (5 areas, the old camp defence / *Riders on the Storm*) dominate the Badlands.
- `sq004` (2), `q103` (1) and `mq001` (1) are the old camp's other quest scenes.
- `q000` (4 areas) is the Nomad prologue/border route, and `q305` (1) is the
  Phantom Liberty border-crossing scene.
- `sq024` and `mq056` (7 areas) are the Badlands/Night City races, where a
  handful of Aldecaldos appear as racers/crowd.
- `q301` (3 areas) is the Phantom Liberty border community in Pacifica; those
  entries are civilian cameos.
- The `cs_*`, `ma_bls_ina_se1_*` and `sa_ep1_*` rows are dynamic events,
  scanner hustles and Dogtown civilian cameos.

### 2.3 Attribution caveat

`areas.jsonl.district_code` is the sector path, not a world-space classifier.
For `always_loaded_*` quest communities it is routinely wrong (§1.1 item 4).
This faction is a good illustration: `q301_com_border_community` is labelled
`pacifica` but sits on the Dogtown wall, and the `sq024`/`mq056` race rows are
split across `heywood`, `westbrook` and `santo_domingo` because the race crosses
districts. The 40 `badlands` rows are the real weight; the city-district rows
are cameos.

Two more traps apply here:

- **`sub_territory_id` is a coarse bucket.** The new Nomad Camp is bucketed into
  `bls_canyon_depot` (Militech, 621.5 m away). The old camp is the only
  Aldecaldos-owned bucket. Do not read `sub_territory_id` as a geocode (§1.2
  item 1).
- **`gamedata_subdistrict` is only `"Badlands"` for every Badlands row.** The
  per-sub-district table therefore collapses to one row for this faction; the
  useful spatial split is the seeded sub-territory (`bls_aldecaldos_camp`,
  `bls_canyon_depot`, `bls_rocky_ridge`, `bls_border_crossing`), not the
  gamedata enum.

### 2.4 The two camps, and what is available in a campaign-disabled world

The wiki treats both campsites as one page, **Aldecaldo Camp (2077)**, with two
fast-travel points: the first camp's is **"Mobile Camp"**, in the central-eastern
Rocky Ridge Plains inside the Wind Farms; the second's is **"Nomad Camp"**, in a
valley in the northern plains, with an unlockable V apartment. `[wiki]`

| Camp | Fast-travel dataterm `[game-data]` | Seed ownership | Story gate | Available in an Act-2 sandbox? |
| --- | --- | --- | --- | --- |
| **Old / Mobile Camp** | `{bls_bls_dataterm_}03` `(3427.930, -360.963, 134.071)` | Sub-territory 83, owner 9; capital CC active | Act 2 camp through `sq004`/`q103`/`sq027` | **Yes, as a location.** `docs/research/campaign-sanitizer.md` sets the Act-2 switches (`q101_enable_activities_flat`, `q101_enable_side_content`, `watson_prolog_lock = 0`) and suppresses quests, but does not fake story completion. The camp geometry, dataterm and vendor placements are present; the 20-nomad `sq004` community is a scene, so ambient population may be thin (verify in-game). |
| **New / Nomad Camp** | `{bls_bls_dataterm_}06` `(1802.307, 2248.608, 180.136)` | None: bucketed into Militech's `bls_canyon_depot`, no CC | Post-`sq027_09` (*Riders on the Storm*) and `q114` (*We Gotta Live Together* / the *Star* ending) | **Geometry and vendors yes; active population no.** Its Aldecaldos communities are `q114_*`, `sq027_09_*` and `mq021_*` story communities; they do not become the active seat in an Act-2 sanitizer state without faking `sq027`/`q114` completion. |

Both camps have persistent vendor and dataterm placements in
`dist/extract/raw/.../always_loaded_*.streamingsector.json`:

- Old camp: `bls_sm_ina_se1_gunsmith_01` `(3428.069, -369.990, 133.570)`,
  `bls_sm_ina_se1_ripperdoc_01` `(3441.101, -387.137, 135.580)`,
  `{bls_bls_dataterm_}03`. The wiki names a dedicated **Weapon Vendor
  (Aldecaldos)** whose home is "Nomad Camp / Mobile Camp". `[wiki]`
- New camp: `bls_sm_ina_se1_gunsmith_01_02` `(1793.584, 2257.763, 180.309)`,
  `bls_sm_ina_se1_ripperdoc_01b` `(1813.485, 2276.430, 182.142)`,
  `{bls_bls_dataterm_}06`; `q114_03c_sm_dakota_trailer` `(1810.631, 2238.694,
  180.205)` is Dakota's trailer during the finale. `[game-data]` `[wiki]`

So the camp is **mobile**: the same vendors and dataterm are placed at both
sites, and only one is active depending on story state. This is why the seed
owns only one bucket.

### 2.5 Routes and corridors (not holdings)

These are places the faction passes through, uses or is attacked at. They are
**not** counted as `named` and are **not** in the JSON `control_points`
(§1.2 item 9).

| Corridor / node | What it is | Coordinates | Evidence |
| --- | --- | --- | --- |
| **SoCal Border Crossing** | NUSA/SoCal checkpoint on Highway 101; security provider SoCal Border Patrol + Militech. The nomads' smuggling route. | `-2823.058, -5645.812, 101.404` (`markers.jsonl` `q000_nomad_mp_border_crossing_checkpoint`) | `[game-data]` `[wiki]` |
| **Union Railroad Station** (Gig: Flying Drugs) | Wraith-occupied station on a smuggler-drone route; the drones are the client's, not an Aldecaldo property. | site 341 `sts_bls_ina_03` anchor `1882.6, -553.1, 54.9` | `[game-data]` `[wiki]` |
| **q104 camp, Biotechnica Flats** | Story staging camp (20 Aldecaldos) at the flats; not owned by the faction. | `-1809.5, -4283.5, 74.1` (`areas.jsonl` `q104_com_nomads_background`) | `[game-data]` |
| **q202 staging camp** | Story staging camp in the south-west (`q202_*`, `loc_q202_staging_camp` prefab); not a seeded holding. | `-707.887, -3940.922, 67.492` (`markers.jsonl` `q202_spwn_player_nomad_camp`) | `[game-data]` |
| **Sunset Motel** | Panam's story lodging; Noah's motel in Wraith country. Not an Aldecaldo holding. | `1663.500, -794.990, 49.817` (`markers.jsonl` `mirror_sm_scene_sunset_single`; the pre-retarget seed landmark was `1634.2, -738.7, 49.8`) | `[game-data]` `[wiki]` |
| **Nomad prologue garage** | V's lifepath pack (Bakkers), not the Aldecaldos. Do not seed as Aldecaldo. | `-3968.139, -6481.421, 75.850` (`markers.jsonl` `q000_nomad_01_garage_export`) | `[game-data]` `[wiki]` |

The **Nomad Trail** (the long-haul smuggling network to Chicago/Phoenix) has no
route geometry in the extract. It is `[wiki]`/`[lore]`, not a map location.

---

## 3. Location catalog

### 3.1 Master table

Coordinates are world-space metres, `Z` up. "Interior?" means the game has a
distinct interior cell/sector. The Aldecaldos have **no extracted interior
cells** at any of their three places; all three are outdoor/cluster anchors.

| # | Name | Type | District / sub-district | Interior? | Business? (what it earns) | Coordinates (x, y, z) | Coordinate source record | Linked communities / sites | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **Aldecaldo Camp (Mobile Camp)** | Mobile nomad camp / clan seat | Badlands / Badlands | No — trailer/tent cluster; no `is_interior` site | Camp economy: convoy staging, vehicle repair, bar, weapon vendor, ripperdoc; Basilisk assembly | `3427.930, -360.963, 134.071` | `markers.jsonl` `{bls_bls_dataterm_}03`; corroborated by `panam_sm_default` `(3413.410, -361.571, 133.590)`, `sq027_08_sm_camp_saved_bar` `(3411.921, -370.595, 133.565)` | `sq004_com_nomads` (20 Aldecaldos, 28 entries); `sq027_com_nomad_defense` (9); `q103_com_dlg_nomads` (6); `mq001_com_funeral_nomads` (13); sub-territory 83 / `cc_bls_aldecaldos_camp` | `[game-data]` `[wiki]` |
| 2 | **Nomad Camp (new camp)** | Mobile nomad camp / post-story seat | Badlands / Badlands | No — trailer/tent cluster; no `is_interior` site | Camp economy: finale staging, party/initiation, Dakota's trailer, weapon vendor, ripperdoc; V apartment | `1802.307, 2248.608, 180.136` | `markers.jsonl` `{bls_bls_dataterm_}06`; corroborated by `mirror_sm_scene_new_nomad_camp` `(1792.029, 2250.486, 180.272)`, `q114_03c_sm_dakota_trailer` `(1810.631, 2238.694, 180.205)` | `q114_com_nomad_party_mood_scenes` (25); `q114_com_nomad_party_dakota_boys` (7); `q114_com_nomad_party_singer` (5); `q114_com_morning_deco_nomads_02` (5); `mq021_com_nomads` (2); no owned sub-territory | `[game-data]` `[wiki]` |
| 3 | **DaKota (Dakota's autoshop)** | Autoshop / fixer hub | Badlands / Badlands (Rocky Ridge Plains, Interstate 9) | No extracted cell; two-building autoshop with office, but no `sites.json` row; gate doors only, no interior node | Vehicle repair/modification, secure delivery, mercenary contracts, fixer brokerage | `2421.772, -772.367, 66.700` | `markers.jsonl` `ina_07_mp_workshop`; corroborated by `spots.json` `#ina_06_ws_dakota_work` `(2419.652, -768.568, 66.477)`, `triggers.json` `#ina_07_tr_inside_workshop` `(2421.94, -771.31, 66.70)`, `#ina_06_tr_dakota_workshop` `(2386.912, -759.249, 65.800)` | Sites 342 `sts_bls_ina_04` (*Radar Love*) and 344 `sts_bls_ina_06` (*No Fixers*); workshop gates `bls_ina_se1_dakotas_workshop_gate_01/02` | `[game-data]` `[wiki]` |

### 3.2 How the name→coordinate links were proven

- **Old camp / Mobile Camp.** The raw sector contains the placed asset
  `$/03_night_city/se1/#loc_sq004_mobile_camp/loc_sq004_mobile_camp_questdesign_prefabLJB57YI/…`
  with the open-world branch `#loc_sq004_mobile_camp_openworld` and
  `mirror_sm_scene_old_nomad_camp`. `[game-data]` The camp's work/life markers
  cluster at `x 3379–3480, y −466…−322, z 129–138`: Panam (`panam_sm_default`),
  Saul (`saul_sm_default`), Mitch (`mitch_sm_default`), Cassidy, Bob, Carol,
  Teddy, the bar (`sq027_08_sm_camp_saved_bar`), the gunsmith
  (`bls_sm_ina_se1_gunsmith_01`) and the ripperdoc
  (`bls_sm_ina_se1_ripperdoc_01`). The dataterm `{bls_bls_dataterm_}03` is the
  camp's fast-travel point and the cleanest single anchor. Note the record's
  debug name: the closing brace sits **before** the numeric suffix, so
  `.strip('{}#')` yields `bls_bls_dataterm_}03`, not `bls_bls_dataterm_03`;
  normalize with `replace('{','').replace('}','')`. `[game-data]` The
  community area's own origin is `(3412.854, -360.108, 120.333)` — the seed
  centroid — but that is the **terrain base 13.7 m below the camp floor**, not
  the walkable camp. This is the correction to the seed anchor (see §8.1).
- **New camp / Nomad Camp.** `{bls_bls_dataterm_}06` is the fast-travel dataterm;
  the camp scene markers (`mirror_sm_scene_new_nomad_camp`,
  `sq027_09_sm_new_camp_wakeup`, `dlc6_apart_panam_camp_*`) and the q114 party
  communities cluster around it. `[game-data]` The wiki names the second
  campsite "Nomad Camp" in the northern plains, with a V apartment; the
  `dlc6_apart_panam_camp_*` markers are that apartment/camp content. `[wiki]`
- **DaKota.** The autoshop is **not** at the isolated
  `dakota_sm_smith_defaut` marker `(2804.620, 252.290, 147.480)`. That marker is
  a scene default 1.1 km north-east of the real workshop (and has an off-map
  duplicate at `6013.581, 6114.200, -0.510`). The real workshop is the
  `(2390–2422, −812…−759)` cluster: `ina_07_mp_workshop`,
  `#ina_07_tr_inside_workshop`, `#ina_06_ws_dakota_work`,
  `#ina_06_ws_tanner_with_dakota`, `#ina_06_tr_dakota_workshop` and the two
  `bls_ina_se1_dakotas_workshop_gate_*` doors. `[game-data]` The wiki's
  **DaKota** page calls it a two-building autoshop on Interstate 9 in the Rocky
  Ridge Plains, owned by Aldecaldo fixer Dakota Smith; *Gig: No Fixers* ends by
  delivering Iris Tanner there, and *Gig: Radar Love* ends by delivering the
  Militech radar there. `[wiki]`

### 3.3 Generic occupied sites (the filler pool)

These are the five sites with Aldecaldos units that are not a named catalog
point. Every one is a gig scene, not a base; the "units" are quest NPCs.
Suitability tags say what gameplay a site can host; they are not lore.

| Site | Sub-district | Units (Aldecaldos) | Suitability tags | Coordinates | Note |
| --- | --- | ---: | --- | --- | --- |
| `sts_wat_nid_03` (site 409) | Northside | 3 (`Character.aldecaldos_grunt2_melee2__ma`) | raid_target 95, rooftop_access 68, vehicle_bay 65, hostage_site 50 | `-1417.545, 2268.007, 18.210` | *Gig: Flight of the Cheetah*: the Aldecaldo smuggling crew waiting at the meet-up; the 3 grunts are at `nid_03_com_nomads` `(-426.5, 2535.3)`, ~1 km from the motel anchor. Filler |
| `sts_bls_ina_08` (site 346) | Badlands | 2 (`ina_08_guide`, `ina_08_nomad_01`) | raid_target 95, rooftop_access 80, vehicle_bay 65, arms_cache 62, market_stall 60, officer_site 60, club 55 | `-1380.131, -3615.641, 55.158` | *Gig: Trevor's Last Ride*: Wraith outpost where Trevor Brass's remains are recovered for his Aldecaldo family. Wraith-held, not an Aldecaldo base. Filler |
| `ma_bls_ina_07` (site 7) | Badlands | 1 (`ma_bls_ina_se1_07_cyberpsycho_1`) | raid_target 93, rooftop_access 80, camera_net 61, stealth_entry 60 | `2655.674, -1566.405, 65.831` | Cyberpsycho scanner hustle; the Aldecaldos tag is the psycho's, not a garrison. Filler |
| `sts_bls_ina_09` (site 347) | Badlands | 1 (`ina_09_nomad`) | raid_target 81, rooftop_access 80, vehicle_bay 65, arms_cache 56, club 55 | `-2628.575, -4948.809, 68.020` | *Gig: MIA*: abandoned house / Jason Wildriver's hideout; the nomad contact is at `ina_09_com_nomad` `(-2928.8, -4725.6)`, ~360 m from the house. Filler |
| `sts_std_rcr_03` (site 388) | RanchoCoronado | 1 (`sts_std_rcr_03_nomad`) | raid_target 95, rooftop_access 78, vehicle_bay 65, officer_site 60, club 55, hostage_site 50 | `446.939, -1267.613, 28.730` | *Gig: Going-away Party*: the Aldecaldo smuggler who extracts Flavio; safehouse is 6th Street-owned. Filler |

Excluded from both tiers: the two camps and DaKota are named (above); the
routes/corridors in §2.5 are not holdings; the 61 areas are not sites.

---

## 4. Economic structure

### 4.1 Revenue streams → catalog locations

| Revenue stream | Code(s) | Catalog locations that produce it | Evidence / notes |
| --- | --- | --- | --- |
| Border and convoy smuggling | `smuggling` | Mobile Camp (1), Nomad Camp (2), SoCal Border Crossing (route), Union Railroad Station drone route | Wiki: the Aldecaldos smuggle/deliver "packages" along the Nomad Trail and transport passengers and merchandise over state borders in armed convoys; *Gig: Flying Drugs* is a smuggler-drone route. `[wiki]` `[game-data]` |
| Passenger and freight transport | `logistics` | Mobile Camp (1), Nomad Camp (2), DaKota (3) | Same wiki description; the camp is the convoy staging point, the autoshop the secure delivery point. `[wiki]` |
| Mercenary work / convoy escort | `mercenary`, `protection` | DaKota (3), camps as mustering points; Dakota's gigs (*No Fixers*, *MIA*, *Trevor's Last Ride*, *Radar Love*, *Sparring Partner*) | Wiki: "involved in mercenary work"; *No Fixers* is an extraction, *MIA* a rescue, *Trevor's* a body recovery. `security_services` is wrong (not licensed); `protection` is the closest code for escort. `[wiki]` `[game-data]` |
| Fixer brokerage | `fixer_brokerage` | DaKota (3) | Dakota Smith is an Aldecaldo fixer and the Badlands' main gig broker; her autoshop is the hub. `[wiki]` |
| Vehicle repair / modification / salvage | `vehicles_chop` | DaKota (3), Mobile Camp (1) | Wiki: DaKota is an autoshop; the camp assembles the stolen Basilisk (`sq027_sm_basilisk_camp_assembled` `(3477.622, -350.210, 134.675)`); nomads use heavily modified cars and bikes. `[wiki]` `[game-data]` |
| Salvage / reconstruction / reverse engineering | `manufacturing` | Mobile Camp (1), Nomad Camp (2), DaKota (3) | Wiki: the Aldecaldos specialise in salvaging and reconstructing destroyed cities; *Radar Love* has them reverse-engineer a Militech radar into a jamming signal. `[wiki]` `[game-data]` |
| Farm labour | `agriculture` | No mapped location | Wiki: manual farm labour. The extract has no Aldecaldo farm site; treat as off-map seasonal work. `[wiki]` `[lore]` |
| Camp bar / food | `food_drink` | Mobile Camp (1) | `sq027_08_sm_camp_saved_bar` marker; the camp is a lived-in settlement, not a commercial venue. `[game-data]` `[wiki]` |
| Camp retail / chrome | `retail`, `cyberware` | Mobile Camp (1), Nomad Camp (2) | Weapon Vendor (Aldecaldos) at "Nomad Camp / Mobile Camp"; the camp ripperdoc is `bls_sm_ina_se1_ripperdoc_01`. The extract has no vendor inventory, so the stock is `[wiki]`/`[inferred]`. `[game-data]` `[wiki]` |
| Bootlegging / stolen goods / drug running | `drugs` | Mobile Camp (1) (staging), Union Railroad Station drone route | Wiki: bootlegging and transporting stolen goods; *Flying Drugs* is a drone cargo route. `[wiki]` `[game-data]` |

No code exists for **salvage** or **convoy escort**; `manufacturing`/
`logistics` and `protection` are the closest fits. That is a vocabulary gap,
not a missing revenue line.

### 4.2 Suppliers, customers, rivals

| Role | Party | Detail |
| --- | --- | --- |
| Customer | Corporations needing deniable logistics | The 2045 **Aldecaldo Depot** in the Heywood Industrial Zone existed specifically so corporate reps would not have to drive to the Badlands. 2077 has no equivalent verified location. `[wiki]` `[lore]` |
| Customer | Night Citizens, refugees, defectors needing passage | *Flight of the Cheetah* smuggles a former Tyger Claw out; *Going-away Party* extracts Flavio from 6th Street. `[wiki]` `[game-data]` |
| Customer | Nomad packs and Dakota's fixer clients | Dakota's gigs are the faction's contract interface; nomad packs stop at her shop. `[wiki]` |
| Supplier (involuntary) | Militech | The Basilisk tank and the P9D/2.161 mobile radar are stolen/reverse-engineered from Militech. `[wiki]` `[game-data]` |
| Supplier / rival | Kang Tao | The q104 gas-station scene at the Biotechnica Flats camp has 10 Kang Tao entries (`q104_com_petro_gas_station`), so Kang Tao is present at the staging area. `[game-data]` |
| Rival | **Wraiths (Raffen Shiv)** | The main enemy: the old camp is attacked by Raffen in `sq027`; the Wraiths hold the Rocky Ridge / Corp-Bud area and hit convoys. `[wiki]` `[game-data]` |
| Rival | Militech / SoCal Border Patrol | Border enforcement and detention; the radar prototype is an anti-nomad surveillance system. `[wiki]` |
| Rival | Arasaka | The Nomad prologue chase and the *Star* ending assault; Arasaka is the corporate antagonist, not a local turf rival. `[wiki]` `[game-data]` |
| Rival | 6th Street, Tyger Claws | City gangs that appear as obstacles in the smuggling gigs (Flavio, Hwangbo). `[wiki]` |
| Ally | Seven Nations / other nomad nations | The Aldecaldos are a Seven Nations member; the wiki notes the Jodes split in 2041. `[wiki]` `[lore]` |

---

## 5. Headquarters recommendation

### Primary HQ: **Aldecaldo Camp (Mobile Camp)** — Badlands

Coordinates: `3427.930, -360.963, 134.071` (camp fast-travel dataterm).
`[game-data]` `markers.jsonl` `{bls_bls_dataterm_}03`.

Rationale:

1. **It is the only seeded holding.** Sub-territory 83 `bls_aldecaldos_camp`
   is owner 9, `is_capital = 1`, with active control centre
   `cc_bls_aldecaldos_camp` and a 45 m capture radius. `[game-data]` No other
   Aldecaldo place has seed ownership; the new camp is inside Militech's
   `bls_canyon_depot`.
2. **It is the canon Act-2 camp.** The wiki's first campsite ("Mobile Camp") is
   in the central-eastern Rocky Ridge Plains inside the Wind Farms; the raw
   sector places the `loc_sq004_mobile_camp` asset in Badlands `se1`, and the
   marker cluster contains Saul, Panam, Mitch, Cassidy, Bob, Carol and Teddy.
   `[game-data]` `[wiki]`
3. **It is a real lived-in seat, not a quest stub.** It has a fast-travel
   dataterm, a weapon vendor, a ripperdoc, a bar, a Dakota workshop visit
   marker, vehicle work and the Basilisk assembly point. `[game-data]` `[wiki]`
4. **It is the available camp in an Act-2 campaign-disabled world.** The
   sanitizer sets the Act-2 switches and suppresses quests; it does not fake
   `sq027`/`q114` completion, so the old camp is the active seat and the new
   camp remains geometry/story content. `[game-data]` `[wiki]`
   `docs/research/campaign-sanitizer.md`.
5. **The seed anchor is nearly right.** The centroid is 15.1 m from the
   dataterm horizontally; only the Z is wrong (120.3 vs 134.071). Retargeting
   the capital CC onto the dataterm fixes it without moving the territory.

Trade-off: the camp is an outdoor trailer/tent cluster, not an enclosed
building. There is no `sites.json` row, no `is_interior`, and no guard/patrol
records. The capture volume is the camp circle; the "rooms to assign" are
trailers and the bar, not floors of a building. That is honest for a nomad
clan.

### Alternate 1: **Nomad Camp (new camp)** — the post-story seat

Coordinates `1802.307, 2248.608, 180.136` `[game-data]` `{bls_bls_dataterm_}06`.

The second campsite from the wiki, in the northern plains, with a V apartment
and the q114 finale content. It is a stronger "endgame capital" than the old
camp but loses on seed ownership (none), on story availability (post-`sq027`),
and on geography (inside Militech's `bls_canyon_depot`, 621.5 m from its CC).
Use it as a **second seat** or a post-story upgrade, not the Act-2 HQ.

### Alternate 2: **DaKota (Dakota's autoshop)** — the fixer/business seat

Coordinates `2421.772, -772.367, 66.700` `[game-data]` `ina_07_mp_workshop`.

The faction's only permanent non-camp base: a two-building autoshop on
Interstate 9, Dakota Smith's fixer hub and the delivery point for two gigs. It
is a believable "business HQ" and the best place to model `fixer_brokerage` and
`vehicles_chop`. It loses on canon (Dakota is a fixer, not the clan leader), on
ownership (the nearest CC is Petrochem's `cc_bls_rocky_ridge`, 715.8 m), and on
interior evidence (no extracted cell).

### Overruled / downgraded suggestions

- **Sunset Motel as HQ** — Noah's motel, Wraith country; Panam's room is a
  story lodging, not an Aldecaldo property. `[game-data]` `[wiki]`
- **Rocky Ridge ghost town as HQ** — Wraith-held; only DaKota's autoshop is an
  Aldecaldo enclave there. `[wiki]`
- **The new camp as the Act-2 HQ** — correct only after *Riders on the Storm*;
  not the Act-2 seat. `[wiki]` `[game-data]`
- **Aldecaldo Depot / Peacekeepers HQ / Radio Tent / 2045 Aldecaldo Camp** —
  2045 RED locations in Heywood/Santo Domingo, no 2077 records. `[wiki]`
  `[lore]`
- **The Nomad prologue garage** — V's Bakker pack, not the Aldecaldos. `[wiki]`

---

## 6. Priority list of control points

Ranked by how well each place serves as a capturable Aldecaldo control point.
"CC" = nearest current entry in `data/control_centers.json` (2026-11-25 01:28
retarget); distance is horizontal metres. Control-centre ownership is the
seeded sub-territory owner.

| Rank | Control point | Rel. (1–5) | District / sub-district | Coordinates | Existing CC overlap | Why |
| ---: | --- | :---: | --- | --- | --- | --- |
| 1 | **Aldecaldo Camp (Mobile Camp)** | 5 | Badlands / Badlands | `3427.930, -360.963, 134.071` | `cc_bls_aldecaldos_camp`, 15.1 m (Aldecaldos) | HQ; the only seeded holding; dataterm, vendors, leadership, convoy staging, Basilisk assembly |
| 2 | **DaKota (Dakota's autoshop)** | 5 | Badlands / Badlands | `2421.772, -772.367, 66.700` | `cc_bls_rocky_ridge`, 715.8 m (**Petrochem**) | Permanent fixer/autoshop; two-building compound with gates and deliveries; **test point** |
| 3 | **Nomad Camp (new camp)** | 4 | Badlands / Badlands | `1802.307, 2248.608, 180.136` | `cc_bls_canyon_depot`, 621.5 m (**Militech**) | Post-story seat; q114 finale; no seed ownership; story-gated population |
| 4 | `sts_wat_nid_03` (Flight of the Cheetah meet-up) | 2 | Watson / Northside | `-1417.545, 2268.007, 18.210` | `cc_kab_creek_loop`, 193.5 m (The Mox) | Filler: 3 Aldecaldo smugglers at the meet-up; not a base |
| 5 | `sts_bls_ina_08` (Trevor's Last Ride) | 2 | Badlands / Badlands | `-1380.131, -3615.641, 55.158` | `cc_bls_biotechnica_flats`, 794.0 m (Biotechnica) | Filler: Wraith outpost, Aldecaldo remains/family; not a base |
| 6 | `sts_bls_ina_09` (MIA) | 2 | Badlands / Badlands | `-2628.575, -4948.809, 68.020` | `cc_bls_border_crossing`, 519.1 m (Militech) | Filler: abandoned house, Aldecaldo driver; not a base |
| 7 | `sts_std_rcr_03` (Going-away Party) | 2 | SantoDomingo / RanchoCoronado | `446.939, -1267.613, 28.730` | `cc_rcr_kendal_park`, 324.0 m (6th Street) | Filler: Aldecaldo smuggler contact; not a base |
| 8 | `ma_bls_ina_07` (cyberpsycho) | 1 | Badlands / Badlands | `2655.674, -1566.405, 65.831` | `cc_bls_wraith_compound`, 898.0 m (Wraiths) | Filler: single Aldecaldo-tagged cyberpsycho; not a garrison |

### Test control point for the first in-game test: **DaKota (Dakota's autoshop)**

Why DaKota and not the HQ or a gig scene:

- **It is not the HQ**, so the test exercises capture away from the clan seat.
- **It is a persistent open-world placement.** The raw sector puts the workshop
  in `se1_openworld_prefab` / `se1_community_prefab` with
  `bls_ina_se1_ws_dakota_workshop_night_static_*` workspots and
  `bls_ina_se1_dakota_workshop_com`; it is not a quest-only interior.
  `[game-data]`
- **Dakota is a fixer, and fixers are preserved by the sanitizer** (the mappin
  deny list keeps `FixerVariant`). A capture test therefore does not fight the
  campaign suppressor. `docs/research/campaign-sanitizer.md`.
- **It has enough geometry to validate a capture radius**: two workshop gates,
  `#ina_07_tr_inside_workshop`, `#ina_07_tr_deliver_car_mp`,
  `#ina_06_tr_stop_car_garage`, and the `ina_07_mp_workshop` map point. There
  are no guard/patrol records, so this tests the volume and ownership flow, not
  a garrison fight.
- **Ownership handling:** the nearest existing CC is `cc_bls_rocky_ridge`
  (715.8 m, **Petrochem**, owner 43), not an Aldecaldo CC. Do **not** retarget
  `cc_bls_rocky_ridge` onto the autoshop; add a new `cc_bls_dakota_autoshop`
  (45 m) and leave the camp's capital CC in place. The autoshop is an Aldecaldo
  enclave inside a Petrochem/Wraith-adjacent stretch of Interstate 9; that
  conflict is the point of the test.

Fallback if a camp capture is preferred: the **new Nomad Camp** (rank 3) has a
clean dataterm and a dense q114 community cluster, but its population is
story-gated. Fallback if an interior is required: **none** of the three named
places has an extracted interior; the nearest enclosed Aldecaldo-related
interior is not part of this faction's holdings (the Militech detention centre
is `sts_bls_ina_05`, a different faction). Say so rather than inventing one.

---

## 7. Per-sub-district counts

This is the number to feed yield balancing. `named` counts distinct named
places the faction owns, runs or habitually occupies; `filler` is the deduped
occupied-site count not already counted as a named place (`METHOD.md` §8). The
61 community areas are quest scenes and do **not** add filler.

| Sub-district | Named | Which ones | Occupied sites (deduped) | Filler | Noteworthy interiors |
| --- | ---: | --- | ---: | ---: | --- |
| Badlands | **3** | Aldecaldo Camp (Mobile Camp), Nomad Camp (new camp), DaKota (Dakota's autoshop) | 3 (`sts_bls_ina_08`, `ma_bls_ina_07`, `sts_bls_ina_09`) | **3** | 0 confirmed; camps/autoshop are outdoor |
| Northside | **0** | — | 1 (`sts_wat_nid_03`) | **1** | 0 |
| RanchoCoronado | **0** | — | 1 (`sts_std_rcr_03`) | **1** | 0 |
| **Total** | **3** | | **5** | **5** | **0** |

Reconciliation:

- `named + filler = 8`.
- 5 deduped occupied sites + 3 marker-only named places = 8. All three named
  places are marker/community-only (no `sites.json` row); all five filler
  points are site-backed.
- The 61 areas / 265 entries are not sites and are not counted. They are
  quest scenes, races, the PL border cameo and dynamic events; counting them
  would inflate the faction by ~10×.
- The border crossing, Sunset Motel, the q104/q202 staging camps and the
  prologue garage are corridors/story locations, not `named` (§2.5).

Interpretation for yield: the Aldecaldos are a **three-point faction** with a
camp, a second camp and a fixer autoshop; the Badlands should carry the high
yield, and the two city sub-districts are one-off gig scenes with no owned
business. If three named points is too few for the map, the §3.3 filler pool is
the honest filler — but those points should be tagged "gig scene", not "lore
business".

---

## 8. Gaps and uncertainties

1. **The seed camp anchor is at the terrain base, not the camp.** Sub-territory
   83's centroid `(3412.9, -360.1, 120.3)` is also the community area's origin,
   but the camp floor/dataterm is at z ≈ 133.5–134.1. The 45 m capture radius
   still covers the camp horizontally, but a map pin at z = 120.3 is 13.7 m
   below it. Retarget `cc_bls_aldecaldos_camp` to `{bls_bls_dataterm_}03`
   `(3427.930, -360.963, 134.071)`. `[game-data]`
2. **`dakota_sm_smith_defaut` is a decoy.** The marker at
   `(2804.620, 252.290, 147.480)` is 1.1 km north-east of the real autoshop and
   has an off-map duplicate at `(6013.581, 6114.200, -0.510)`. The real workshop
   is `(2390–2422, −812…−759)`, proven by the `.spots`, `.triggers` and
   `.doors` records and by the two gig deliverables. Do not use the "default"
   marker for the autoshop. `[game-data]`
3. **Site anchors can be ~1 km from the sub-scene.** Site 344
   `sts_bls_ina_06` anchors at `(2169.7, -1637.9)` but its Dakota workshop
   nodes are at `(2386–2422, −812…−759)`; site 342 `sts_bls_ina_04` anchors at
   `(3582.5, -916.8)` but its `#ina_04_tr_near_dakota` is at
   `(2412.1, -796.7)`; site 409's three grunts stand at the meet-up area
   `(-426.5, 2535.3)`, ~1 km from the motel anchor. Roster counts are per site,
   not per anchor. `[game-data]`
4. **The new camp has no seed ownership.** It is bucketed into Militech's
   `bls_canyon_depot` (621.5 m); a post-story camp capture would need a new
   sub-territory/CC. The old camp is the only seeded Aldecaldo holding.
   `[game-data]`
5. **Which camp is "live" depends on story state.** The old camp is the Act-2
   seat; the new camp's population is `q114`/`sq027_09` story content. The
   sanitizer sets Act-2 flags, not `sq027`/`q114` completion, so the old camp
   is the safe Act-2 HQ. Verify in-game that the old camp's vendors and
   dataterm spawn while vanilla quests are suppressed. `[game-data]` `[wiki]`
   `docs/research/campaign-sanitizer.md`.
6. **No camp or autoshop interior.** There is no `sites.json` row for either
   camp or the autoshop; `is_interior` is absent, not false. The autoshop's
   office is likely a walk-in, but there is no doors/rooms record to prove a
   distinct cell. Do not promise an interior capture volume. `[game-data]`
7. **The wiki's 2045 Aldecaldo locations are red herrings.** **Aldecaldo Camp
   (RED)** (Coronado Dam, Santo Domingo), **Aldecaldo Peacekeepers
   Headquarters** (Santo Domingo), **Aldecaldo Depot** (Heywood Industrial
   Zone) and **Aldecaldo Camp Radio Tent** are 2045 RED locations with no 2077
   marker/site record. Do not seed them. `[wiki]` `[lore]`
8. **No 2077 urban storefront or city contact.** Dakota's autoshop is the only
   permanent non-camp base, and it is on Interstate 9 in the Badlands, not in a
   city sub-district. The 2045 Aldecaldo Depot is the only "corporate-facing"
   property in lore. `[wiki]` `[lore]`
9. **The border crossing is not theirs.** SoCal Border Crossing is NUSA/SoCal
   property with SoCal Border Patrol + Militech security. The Aldecaldo
   presence is the q305/ambient nomad traffic and the smuggling business, not
   ownership. Counted as a route, not `named` (§1.2 item 9). `[game-data]`
   `[wiki]`
10. **The q104 and q202 camps are story staging, not holdings.** `q104_com_nomads_background`
    at Biotechnica Flats has 20 Aldecaldos, and `q202_spwn_player_nomad_camp`
    is a staging camp in the south-west; both are scene communities. Do not
    seed them as bases. `[game-data]`
11. **The prologue garage is not Aldecaldo.** `q000_nomad_01_garage` at
    `(-3968.139, -6481.421, 75.850)` is the Nomad lifepath's Bakker pack
    garage, not the Aldecaldos. `[game-data]` `[wiki]`
12. **Sunset Motel is a story lodging.** Panam's room at the Sunset Motel is
    Noah's business in Wraith country; the `mirror_sm_scene_sunset_panam` /
    `mirror_sm_scene_sunset_single` markers are scene anchors, not a holding.
    `[game-data]` `[wiki]`
13. **`areas.jsonl.district_code` is unreliable for quest communities.** The
    61 areas include the PL q301 border cameo (Pacifica/Dogtown), the
    sq024/mq056 race (split across Heywood/Westbrook/SantoDomingo) and city
    crowd scenes. The 40 `badlands` rows are the real weight; all per-sub-district
    counts in §7 come from the 8 catalog points, not the 61 areas. `[game-data]`
14. **No vendor inventory, no `is_interior`, no guard records at the camps.**
    The extract has suitability tags and vendor placements, not stock lists.
    "What the camp weapon vendor sells" is `[wiki]`/`[inferred]`. `[game-data]`
15. **`faction_headquarters.json` has no Aldecaldos row.** The seeder reading
    only that file finds nothing for fid 9; supply the row from the camp
    dataterm (`{bls_bls_dataterm_}03`) or from `sub_territories` 83. `[game-data]`
16. **The parallel seed retarget moved the Badlands context.** As of
    2026-11-25 01:28, `bls_rocky_ridge` is "Petrochem Fuel Station (I-9)" at
    `(1706.187, -755.859)` and `bls_sunset_motel` is "New American Autoworks"
    at `(-142.756, -4419.236)`. The DaKota autoshop is ~716 m east of the
    Petrochem CC and has no Aldecaldo CC of its own. Any seeder that joins
    nearest CC blindly will hand the autoshop to Petrochem. `[game-data]`
17. **The old camp's 20-nomad community is a quest community, not ambient
    population.** `sq004_com_nomads` (28 entries) is a scene; in the open
    world the persistent presence is the dataterm/vendors, not 20 idle nomads.
    Presence via `areas.jsonl` can overstate. `[game-data]`
18. **Marker-name normalization: `.strip('{}#')` is not enough.** The dataterm
    records are `{bls_bls_dataterm_}03` / `{bls_bls_dataterm_}06`: the closing
    brace is before the numeric suffix, so `strip('{}#')` returns
    `bls_bls_dataterm_}03`. This is a counterexample to `METHOD.md` §2.3
    item 4; normalize with `replace('{','').replace('}','')` or a regex, not
    `strip`. `[game-data]`

---

## 9. Sources

### Local

- `data/factions.json` — faction 9 `aldecaldos`, enum `Aldecaldos`, category
  `gang`.
- `data/sub_territories.json`, `data/landmarks.json`,
  `data/control_centers.json`, `data/faction_headquarters.json` — seed
  ownership, centroids, CC ownership (2026-11-25 01:28 retarget).
- `data/sites/sites.json`, `data/sites/rosters.json`,
  `data/sites/communities.json`, `data/sites/suitabilities.json`,
  `data/sites/{spots,triggers,doors,guards,patrols}.json` — sites, units,
  node names, workshop workspots/gates.
- `dist/extract/areas.jsonl` — 61 Aldecaldo areas / 265 entries.
- `dist/extract/markers.jsonl` — camp dataterms, Dakota workshop, border
  crossing, Sunset Motel, prologue garage.
- `dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_{0,1,2}.streamingsector.json`
  — prefab paths: `loc_sq004_mobile_camp`, `mirror_scene_{old,new}_nomad_camp`,
  `bls_ina_se1_dakota_workshop_com`, `bls_ina_se1_ws_dakota_workshop_night_static_*`.
- `docs/research/campaign-sanitizer.md` — Act-2 switches, quest suppression,
  fixer preservation.

### Wiki (MediaWiki API, infobox/lead only)

- [Aldecaldos](https://cyberpunk.fandom.com/wiki/Aldecaldos)
- [Aldecaldo Camp (2077)](https://cyberpunk.fandom.com/wiki/Aldecaldo_Camp_(2077))
- [DaKota](https://cyberpunk.fandom.com/wiki/DaKota)
- [Dakota Smith](https://cyberpunk.fandom.com/wiki/Dakota_Smith)
- [Rocky Ridge](https://cyberpunk.fandom.com/wiki/Rocky_Ridge)
- [Sunset Motel](https://cyberpunk.fandom.com/wiki/Sunset_Motel)
- [SoCal Border Crossing](https://cyberpunk.fandom.com/wiki/SoCal_Border_Crossing)
- [Gig: No Fixers](https://cyberpunk.fandom.com/wiki/Gig:_No_Fixers)
- [Gig: Radar Love](https://cyberpunk.fandom.com/wiki/Gig:_Radar_Love)
- [Gig: Dancing on a Minefield](https://cyberpunk.fandom.com/wiki/Gig:_Dancing_on_a_Minefield)
- [Gig: MIA](https://cyberpunk.fandom.com/wiki/Gig:_MIA)
- [Gig: Trevor's Last Ride](https://cyberpunk.fandom.com/wiki/Gig:_Trevor%27s_Last_Ride)
- [Gig: Flight of the Cheetah](https://cyberpunk.fandom.com/wiki/Gig:_Flight_of_the_Cheetah)
- [Gig: Going-away Party](https://cyberpunk.fandom.com/wiki/Gig:_Going-away_Party)
- [Gig: Flying Drugs](https://cyberpunk.fandom.com/wiki/Gig:_Flying_Drugs)
- [Gig: Big Pete's Got Big Problems](https://cyberpunk.fandom.com/wiki/Gig:_Big_Pete%27s_Got_Big_Problems)
- [Gig: Sparring Partner](https://cyberpunk.fandom.com/wiki/Gig:_Sparring_Partner)
- [We Gotta Live Together](https://cyberpunk.fandom.com/wiki/We_Gotta_Live_Together)
- [Every Grain of Sand](https://cyberpunk.fandom.com/wiki/Every_Grain_of_Sand)
- [Weapon Vendor (Aldecaldos)](https://cyberpunk.fandom.com/wiki/Weapon_Vendor_(Aldecaldos))
- [Iris Tanner](https://cyberpunk.fandom.com/wiki/Iris_Tanner),
  [Jason Wildriver](https://cyberpunk.fandom.com/wiki/Jason_Wildriver)
- 2045-only: [Aldecaldo Camp (RED)](https://cyberpunk.fandom.com/wiki/Aldecaldo_Camp_(RED)),
  [Aldecaldo Peacekeepers Headquarters](https://cyberpunk.fandom.com/wiki/Aldecaldo_Peacekeepers_Headquarters),
  [Aldecaldo Depot](https://cyberpunk.fandom.com/wiki/Aldecaldo_Depot),
  [Aldecaldo Camp Radio Tent](https://cyberpunk.fandom.com/wiki/Aldecaldo_Camp_Radio_Tent)

### Earlier repo research

- `docs/research/factions/METHOD.md` (§1.1, §1.2, §3, §8, §10).
- `docs/research/factions/tyger-claws.md` (pilot format).
- `docs/research/factions/militech.md` (Badlands/`bls` attribution and the
  `q114` bbox warning).
- `docs/research/campaign-sanitizer.md` (Act-2 state, fixer preservation).

---

## 10. Machine-readable block

Strict JSON for seeding (contract in `METHOD.md` §10). Every coordinate was
verified against the local record named in `source` on 2026-11-25; none came
from the wiki.

```json
{
  "faction_code": "aldecaldos",
  "hq": {
    "name": "Aldecaldo Camp (Mobile Camp)",
    "district": "Badlands",
    "sub_district": "Badlands",
    "x": 3427.930,
    "y": -360.963,
    "z": 134.071,
    "source": "dist/extract/markers.jsonl {bls_bls_dataterm_}03",
    "confidence": "game-data+wiki"
  },
  "alternate_hqs": [
    {
      "name": "Nomad Camp (new camp)",
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": 1802.307,
      "y": 2248.608,
      "z": 180.136,
      "source": "dist/extract/markers.jsonl {bls_bls_dataterm_}06",
      "confidence": "game-data+wiki"
    },
    {
      "name": "DaKota (Dakota's autoshop)",
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": 2421.772,
      "y": -772.367,
      "z": 66.700,
      "source": "dist/extract/markers.jsonl ina_07_mp_workshop",
      "confidence": "game-data+wiki"
    }
  ],
  "test_control_point": {
    "name": "DaKota (Dakota's autoshop)",
    "district": "Badlands",
    "sub_district": "Badlands",
    "x": 2421.772,
    "y": -772.367,
    "z": 66.700,
    "source": "dist/extract/markers.jsonl ina_07_mp_workshop",
    "confidence": "game-data+wiki"
  },
  "control_points": [
    {
      "rank": 1,
      "name": "Aldecaldo Camp (Mobile Camp)",
      "type": "nomad_camp",
      "relevance": 5,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": 3427.930,
      "y": -360.963,
      "z": 134.071,
      "source": "dist/extract/markers.jsonl {bls_bls_dataterm_}03",
      "confidence": "game-data+wiki",
      "interior": false,
      "revenue_streams": ["logistics", "smuggling", "mercenary", "vehicles_chop", "retail", "food_drink"],
      "nearest_cc_code": "cc_bls_aldecaldos_camp",
      "nearest_cc_m": 15.1
    },
    {
      "rank": 2,
      "name": "DaKota (Dakota's autoshop)",
      "type": "fixer_autoshop",
      "relevance": 5,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": 2421.772,
      "y": -772.367,
      "z": 66.700,
      "source": "dist/extract/markers.jsonl ina_07_mp_workshop",
      "confidence": "game-data+wiki",
      "interior": false,
      "revenue_streams": ["fixer_brokerage", "vehicles_chop", "mercenary", "logistics"],
      "nearest_cc_code": "cc_bls_rocky_ridge",
      "nearest_cc_m": 715.8
    },
    {
      "rank": 3,
      "name": "Nomad Camp (new camp)",
      "type": "nomad_camp",
      "relevance": 4,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": 1802.307,
      "y": 2248.608,
      "z": 180.136,
      "source": "dist/extract/markers.jsonl {bls_bls_dataterm_}06",
      "confidence": "game-data+wiki",
      "interior": false,
      "revenue_streams": ["logistics", "smuggling", "mercenary", "food_drink"],
      "nearest_cc_code": "cc_bls_canyon_depot",
      "nearest_cc_m": 621.5
    }
  ],
  "subdistrict_counts": {
    "Badlands": {"named": 3, "filler": 3},
    "Northside": {"named": 0, "filler": 1},
    "RanchoCoronado": {"named": 0, "filler": 1}
  }
}
```
