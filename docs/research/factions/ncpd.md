# NCPD — Lore-Relevant Control Points

Status: faction research run, 2026-11-25. One faction, one document.
Scope: replace the generic control-centre grid with places the **Night City
Police Department** actually *holds* — not places it merely *responds to* —
with verified coordinates, an economic map, an HQ pick, a ranked capture list,
an honest per-sub-district count, and a holdings-vs-response audit that the
other fifteen docs did not need.
Method: this doc conforms to [`METHOD.md`](./METHOD.md). §1.1 (batch-1) and
§1.2 (batch-2) corrections were read first and override the later sections.
`AGENTS.md` was read first. No commits, no game launch. Helper scripts ran
outside the repo with `python3 -I`.

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Position, site, community, roster, marker or spawn record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/artbook lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My reasoning links a named place to a game record; reasoning stated | Weak, flagged |

No coordinate below is guessed. Every `(x, y, z)` is copied from a local
marker, node, area, site or seed record, or marked `TBD`.

**Up front, because it reshapes every section:** NCPD in this game is not a
turf faction and barely a garrison faction. It has **zero owned
sub-territories** (no `sub_territories.initial_owner_faction_id == 50`),
**98 roster units across 28 sites**, and **273 community areas of which 193
are `cs_*` dynamic scanner/crime-scene events** (`dominant_faction == ncpd`;
194 rows by name). Only **15 sites** carry `default_faction_id = 50`, and every
one of them is a scanner hustle, a miniworld story or a fixer gig — **not one
is a police building**. The buildings that *are* NCPD — the Little China
precinct, the Glen lab, the Arroyo prison — have **no `sites.json` row at all**.
They exist only as markers, prefab folders, community nodes and district
enums. This doc is therefore marker-, prefab- and enum-driven, and it is the
first doc that has to separate "what NCPD holds" from "where NCPD shows up".

That distinction is the design requirement. NCPD is being reframed as a
**weakened faction**: the city is at war, NCPD has pulled back to fortified
holdings, and the mod should let police *response* scale with who controls a
sub-district. So this doc delivers two different things: a short list of real
holdings (§6) and a measured map of response presence (§11) that the
simulation can consume as a heat/density table.

---

## 1. Summary

The Night City Police Department is the city's municipal law-enforcement
agency, founded 1994, reporting to the Government of Night City. `[wiki]` In
2077 it is **underfunded, underequipped and understaffed**: after Mayor Rhyne
privatised it in 2076, Commissioner Jerry Fawlter fired half the officers, cut
patrols, charged 5€$ per minute for 911 calls and ran a drones-for-cops
replacement programme. `[wiki]` The wiki's own database entry calls it "an
underfunded, underequipped, understaffed organization where every officer puts
their life on line each day", with "an atmosphere of apathy and corruption". `[wiki]`

**Canon structure.** Patrol (beat, traffic, cruiser, airborne), Investigation
(vice, robbery, homicide, special investigations), Tactical (SWAT, **MaxTac**,
Riot), NetSec, Internal Affairs, Administration. `[wiki]` **MaxTac** is the
C-SWAT unit that answers cyberpsychos and the most dangerous crimes and turns up
at maximum wanted level. `[wiki]`

**Canon bases (this is the hard part).** The wiki infobox lists historical
headquarters — MuCJuC (2010) and NCPD HQ (2020) — but *no 2077 headquarters*.
Its `faction_locations` field says only "See Precincts". `[wiki]` The
disambiguation page lists five 2077 precincts: **The Glen**, **Arroyo**,
**Little China**, a coordinate-less **Precinct #5**, and the **abandoned
Pacifica precinct** (now Barghest's; see `barghest.md` §3 #9). `[wiki]` So NCPD
has no single seat in 2077 — it has a set of precincts, and the game models
exactly **one** of them as a building.

**Economic model.** NCPD does not earn from storefronts. Its revenue is
municipal funding plus fines, fees and seized assets, and the wiki's whole
2076–77 arc is that this model is *failing*. `[wiki]` In the shared vocabulary
(`METHOD.md` §7) that is `security_services` plus `finance` (fines/fees) — the
same codes a licensed security contractor would use. Its real "product" is
**response**: patrol coverage, heat escalation and MaxTac retaliation.

**Where the weight actually is.** Of 273 NCPD-flagged community areas and 696
NCPD records: **183 areas / 440 records are response** (`cs_*` scanner events,
follow-up police groups at gang sites, dynamic events), **34 areas / 68 records
are patrol or dragnet**, **50 areas / 160 records are quest set-pieces**, and
**6 areas / 28 records are the Night City Prison garrison** — the only place in
the entire extract where NCPD stands still on its own property. Everything else
is a reaction. `[game-data]`

**One structural finding worth stating plainly.** The vanilla police system is
already a **per-district heat machine**, and its data model is exactly the hook
this mod needs: `District_Record.PreventionPreset()`, `CrimeMultiplier()`,
`GunShotStimRange()` and a `PreventionHeatData_Matrix` keyed by district, with
an owner-keyed **Dogtown override**. `[script]` §11.4 lays that out with
file:line references.

---

## 2. Territory

### 2.1 Districts

| Evidence kind | Result |
| --- | --- |
| (a) Wiki/lore | NCPD is city-wide municipal. It is **absent** from Pacifica (withdrawn 2072, `[wiki]`) and **absent** from Dogtown (Barghest's Prevention Unit polices it, `[wiki]`). The Badlands are outside city limits and not patrolled. `[wiki]` |
| (b) Vanilla map gang panel | `data/districts.json`: NCPD appears in **no** district's `vanilla_gangs` list. Correct — it is not a gang. `[game-data]` |
| (c) Game-data counts | 273 community areas contain NCPD records (696 records). **0 owned sub-territories.** 28 roster sites / 98 units. 15 sites with `default_faction_id == 50`. `[game-data]` |

Owned sub-territories: **none**. This is the first faction in the project with
zero. NCPD holds no seeded polygon, so every holding in §3 had to be found from
markers, prefabs and `gamedataDistrict` enums.

`data/districts.json` crime multipliers are the closest thing to a civic
territory model already in the repo — City Center 1.2, Watson/Westbrook 0.85,
Heywood/Santo Domingo 0.8, Pacifica 0.7, Badlands/Dogtown/Morro Rock 1.0. `[game-data]`
Those numbers are the seeding pipeline's own reading of the same
`CrimeMultiplier()` field the prevention system reads at runtime, so §11.4 can
use them directly.

### 2.2 Sub-district presence

Counts are from `dist/extract/areas.jsonl` (any area whose `faction_counts`
contains `ncpd`). Attribution follows §1.2 item 1, with one addition forced by
the data (§2.3): project-id token → bbox-gated nearest geocoded site within
150 m (same district bbox) → nearest sub-territory inside the same district
bbox. Every nearest-sub row is flagged `[inferred]` in the JSON.

| Sub-district | District | (a) Lore | Areas | Records | `cs_*` areas |
| --- | --- | --- | ---: | ---: | ---: |
| LittleChina | Watson | precinct + Megabuilding H10 `[wiki]` | 46 | 127 | 30 |
| Glen | Heywood | NCPD Lab, City Hall, a precinct `[wiki]` | 37 | 84 | 29 |
| Downtown | CityCenter | — | 24 | 62 | 18 |
| Arroyo | SantoDomingo | **Night City Prison**, a precinct `[wiki]` | 22 | 59 | 15 |
| JapanTown | Westbrook | safe neighbourhood `[wiki]` | 21 | 51 | 15 |
| RanchoCoronado | SantoDomingo | — | 17 | 45 | 15 |
| Wellsprings | Heywood | — | 17 | 43 | 15 |
| Kabuki | Watson | — | 16 | 45 | 12 |
| CorpoPlaza | CityCenter | city hall *hologram* only (§8) | 12 | 28 | 8 |
| CharterHill | Westbrook | safest district `[wiki]` | 12 | 29 | 12 |
| Northside | Watson | "rarely travelled to" `[wiki]` | 10 | 17 | 6 |
| VistaDelRey | Heywood | — | 10 | 25 | 7 |
| Badlands | Badlands | not patrolled `[wiki]` | 6 | 25 | 2 |
| Coastview | Pacifica | abandoned precinct `[wiki]` | 5 | 7 | 1 |
| NorthOaks | Westbrook | — | 5 | 14 | 3 |
| Dogtown | Dogtown | Barghest, not NCPD `[wiki]` | 4 | 8 | 0 |
| WestWindEstate | Pacifica | Barghest territory `[wiki]` | 4 | 14 | 1 |
| ArasakaWaterfront | Watson | — | 4 | 10 | 4 |
| MorroRock | MorroRock | — | 1 | 3 | 1 |

**Two honest readings.** First, NCPD presence tracks **crime density and
authored scanner placement, not police priority**: Little China and the Glen
top the list because that is where the events were authored, and Northside —
which the wiki says the NCPD "rarely travelled to" `[wiki]` — has only 10
areas. Second, Dogtown and West Wind are artefacts of `district_code`
inheritance; every one of those rows is a quest set-piece (`q301_com_border`,
`q303_com_paradise…`, `sts_ep1_10_*`) where NCPD is the antagonist inside
Barghest's zone. `[game-data]`

### 2.3 `district_code` is unusable for this faction

Two independent failures.

`{mq062_prison_openworld_combat_com_area}` and its five sibling communities are
labelled `district_code: westbrook` but sit at `(-522.4, -651.0)` — and the
`westbrook` and `santo_domingo` bboxes **overlap** along `y ∈ [-750, -565]`
(`data/districts.json`), so the seam is genuinely ambiguous by bbox alone. The
authority is the prefab path: every `mq062` node lives under
`#c_santo_domingo/arroyo/`, and the wiki puts the prison in Arroyo. `[game-data]`
`[wiki]` I attribute by project id (`mq062_* → Arroyo`) and resolve bbox ties in
favour of Santo Domingo. Doing this moved **6 areas / 28 records** from
VistaDelRey/Downtown into Arroyo — a class-changing correction, not a rounding
one.

`{mq061_04_sm_city_hall_scene}` sits at `(-1317.8, -84.3, 0.0)`, exactly the
METHOD §1.2 item 7 snapped-marker coordinate shared by all eleven `mq061_*_sm_*`
markers. `[game-data]` Both cases are attributed by position and project id in
this doc, never by `district_code`.

---

## 3. Location catalog

Coordinates are world-space metres, Z up. "Interior?" means the game has a
distinct interior cell/sector, proven from node names (§1.2 item 15), never from
`is_interior` (which is 0 for every candidate here).

| # | Name | Type | District / sub-district | Interior? | Business? | Coordinates (x, y, z) | Coordinate source record | Linked records | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **Little China NCPD Precinct** | Police station (sizable building, AV pads, elevated NCART access) | Watson / LittleChina | Yes — front desk, offices, lockup, roof pads | No — civic; `security_services`/`finance` | `(-1395.511, 1284.071, 119.086)` | `dist/extract/markers.jsonl {mq010_spwn_police_station}` | `#lch_ncpd_guard`, `#lch_ncpd_investigate` (×3), `#ncpd_security_area`, `#ncpd_security_system` in `#c_watson/little_china/little_china_community_prefabYXM4BXA`; street community `{de_wat_lch_05_police_com}` at `(-1449.250, 1211.810, 18.120)`; doors `#mq010_01_sm_ncpd_door`, `#mq010_sm_policeman_door`, `#mq010_sm_policewoman_door` | `[game-data]` `[wiki]` `[inferred]` |
| 2 | **NCPD Lab** (forensic / cyberpsych research) | Subcontracted laboratory | Heywood / Glen | Yes — lab floor, offices, secure room | No — `rnd` for the department | `(-1518.258, -602.782, 7.850)` | `markers.jsonl mirror_sm_scene_police_lab` | Prefab `#c_heywood/glen/#loc_sq021_police_lab` (`_env`, `_gameplay`, `_questdesign`, `_surrounding`; 188 nodes); enum `gamedataDistrict.Glen_NCPDLab`; gig baseid `sq021_sick_dreams` = *The Hunt* | `[game-data]` `[wiki]` |
| 3 | **Night City Prison** | Maximum-security penitentiary | SantoDomingo / Arroyo | Yes — visitor centre, cellblock, monitoring, yard, armory, garage | No — `security_services`; custody contract | `(-518.190, -677.850, 7.520)` visitor entrance | `markers.jsonl mq062_02_sm_hook_entrance_visitor` | 6 communities / 28 NCPD records (§11.1); `#std_arr_prison_ncpd_002…020` (19 named NCPD slots) in `arroyo_openworld_prefabPTAJFCA`; job baseid `mq062_clampdown` = *Clampdown* | `[game-data]` `[wiki]` |
| 4 | **Night City Hall** | Seat of municipal government | Heywood / Glen | Yes — conference room, council chamber | Yes: `finance`, `real_estate` (permits, zoning) | `(-1771.830, -1010.775, 94.700)` conference-room floor | `markers.jsonl sq012_02a_sm_braindance` | `#c_heywood/glen/loc_sq012_city_hall_conference_room_prefabSADQP6Y`; `{sq012_com_braindance}` (1 NCPD + 2 City Council); `#mq061_city_hall_drone_com` at `(-1775.1, -933.1, 13.9)` | `[game-data]` `[wiki]` |
| 5 | **Tactical Coffee** (Tom's Diner, MaxTac hangout) | Diner; incidental MaxTac post | Watson / LittleChina | No — street-level diner frontage | Yes: `food_drink` | `(-1496.860, 1142.577, 18.630)` | `areas.jsonl {tactical_coffee_community}` (hash `7049771620113915695`, 20 NCPD / 4 Arasaka) | Site 325 `mws_tactical_coffee` (20 units, `officer_site` 90); spots `#nws_tactical_coffee_maxtac1…4`, `#nws_tactical_coffee_agent1…15`; wiki: "Tom's Diner is occasionally visited by NCPD officers, including MaxTac operators" | `[game-data]` `[wiki]` |
| 6 | **Abandoned Pacifica NCPD Precinct** | Former precinct → Barghest base | Pacifica / Coastview | Yes — front desk, lockup, garage | No — lost | `(-2215.200, -2289.278, 12.030)` | `data/sites/sites.json` site 361 `sts_ep1_10` | **Not an NCPD holding in 2077.** Listed so the next agent does not seed it twice. Its 3 NCPD records are the hostages in `sts_ep1_10_tv_crew_com`. See `barghest.md` §3 #9 | `[game-data]` `[wiki]` |

Named places the wiki lists but which have **no** verified in-game record —
precincts in the Glen and Arroyo, and Precinct #5 — are in §8, gaps 2.

### 3.1 How the name→coordinate links were proven

- **Little China precinct — proven by the block's own security nodes, then
  pinned by the NCART clue.** The `mq010` marker set
  (`#mq010_03_police_station`, `#mq010_spwn_police_station`,
  `#mq010_sm_policeman_door`, `#mq010_sm_policewoman_door`,
  `#mq010_04_sm_police_talk`) sits at z ≈ 119, on **Megabuilding H10's upper
  floors** — that is the two-cops-knocking-on-Barry's-door scene from *Happy
  Together*, not the station. `[game-data]` `[wiki]` The station itself is the
  adjacent building that carries a *permanent guard post with its own alarm
  system*: `#lch_ncpd_guard`, `#lch_ncpd_investigate` ×3,
  `#ncpd_security_area`, `#ncpd_security_system`. `[game-data]` The wiki
  identifies which building that is: "a sizable precinct right next to
  Megabuilding H10 … AV landing pads on the roof and an elevated access to a
  nearby NCART station". `[wiki]` The standing 4-unit community
  `{de_wat_lch_05_police_com}` at `(-1449.250, 1211.810, 18.120)` is **31 m
  from the elevated NCART station marker** `{wat_lch_metro_ftp_08_exit}` at
  `(-1456.6, 1181.3, 46.0)`, which matches the wiki's description exactly.
  `[game-data]` `[wiki]` I therefore seed the **H10 marker** (`-1395.511,
  1284.071, 119.086`) as the named anchor, because it is the only record
  literally named `police_station`, and cite the street community as the
  horizontal fallback. Confidence: `[game-data]` for both positions,
  `[inferred]` for which one is the door.
- **NCPD Lab — proven by enum plus prefab plus gig.** `gamedataDistrict` has a
  dedicated value `Glen_NCPDLab` (`refs/cyberpunk/orphans.swift:4896`) `[enum]`;
  the asset tree is `#c_heywood/glen/#loc_sq021_police_lab/…`; the gig is
  *The Hunt* (`baseid sq021_sick_dreams`), whose wiki infobox location is "NCPD
  Lab". `[game-data]` `[wiki]` Marker `mirror_sm_scene_police_lab` is the
  in-lab mirror scene and is the coordinate.
- **Night City Prison — proven by job, prefab and 19 named NCPD slots.** Job
  *Clampdown* (`baseid mq062_clampdown`) has location "NC Prison". `[wiki]` The
  prefab is `#c_santo_domingo/arroyo/loc_mq062_prefab…`, and the Arroyo
  openworld community prefab contains `#std_arr_prison_ncpd_002` through
  `#std_arr_prison_ncpd_020`, plus `#std_arr_prison_dvc_sec_area` and
  `#std_arr_prison_dvc_sec_sys`. `[game-data]` Nineteen individually named NCPD
  slots is the strongest garrison signal in the whole faction — and the only one.
- **City Hall — proven by the section prefab; the `mq061` marker is a trap.**
  The real City Hall interior asset is
  `#c_heywood/glen/loc_sq012_city_hall_conference_room_prefab…`, i.e. **the
  Glen**. `[game-data]` The wiki agrees: "Night City Hall … in the Glen, in the
  Heywood district", on Ventura/Palms View/Scofield. `[wiki]` The
  `mq061_04_sm_city_hall_scene` marker at `(-1317.8, -84.3, 0.0)` is the
  **hologram set**: the whole `mq061` cluster lives under
  `#c_city_center/corpo_plaza/loc_mq061_prefab…/#04_city_hall_v/#04_city_hall_holo`,
  a holographic `_v` variant for the Arasaka parade. `[game-data]` METHOD §1.2
  item 1 warns about hologram/vista prefabs; this is the load-bearing example.
- **Tactical Coffee — proven by wiki caption plus node prefix.** The wiki's
  *Mini-World Stories* page names it "Tactical Coffee" and says Tom's Diner "is
  occasionally visited by NCPD officers, including MaxTac operators". `[wiki]`
  Site 325 is `mws_tactical_coffee`, `default_faction_id = 50`, 20 NCPD units
  including four `#nws_tactical_coffee_maxtac1…4` spots, and its community
  `{tactical_coffee_community}` is **11 m** from Tom's Diner's own community
  `{q101_com_tom_diner}`. `[game-data]`

**A trap worth recording.** Tom's Diner and Tactical Coffee are the same 11 m
of pavement — `{q101_com_tom_diner}` at `(-1505.1, 1150.0)` and
`{tactical_coffee_community}` at `(-1496.9, 1142.6)`. `[game-data]` One place,
two labels, one of which is the wiki's. Anything that name-matches "coffee" or
"diner" in Little China lands on this corner.

### 3.2 Generic occupied sites (the filler pool)

Every site with `default_faction_id == 50`, with suitability tags as business
affordances. These are the honest "occupied block" tier of METHOD §8 — each is
a scanner hustle, miniworld story or fixer gig, i.e. a place NCPD *attends*.

| Site | Code | Kind | Units | Top suitability | Anchor |
| --- | --- | --- | ---: | --- | --- |
| 325 | `mws_tactical_coffee` | mini_world_story | 20 | `officer_site` 90, `raid_target` 75, `rooftop_access` 68 | `(-1500.7, 1150.9, 18.8)` |
| 65 | `ma_hey_rey_05` | scanner_hustle | 5 | `raid_target` 87, `officer_site` 80, `vehicle_bay` 65 | `(-959.8, -785.9, 8.2)` |
| 96 | `ma_pac_cvi_08` | scanner_hustle | 5 | `raid_target` 81, `rooftop_access` 62, `camera_net` 61 | `(-2005.7, -1567.3, 12.1)` |
| 25 | `ma_cct_dtn_03` | scanner_hustle | 4 | `raid_target` 75, `rooftop_access` 58 | `(-2150.8, 279.3, 8.0)` |
| 80 | `ma_hey_spr_06` | scanner_hustle | 4 | `raid_target` 87, `rooftop_access` 62, `camera_net` 61 | `(-2403.3, -1086.9, 12.8)` |
| 128 | `ma_std_arr_06` | scanner_hustle | 4 | `raid_target` 72, `rooftop_access` 58 | `(-646.0, -1317.5, 8.0)` |
| 164 | `ma_std_rcr_11` | scanner_hustle | 4 | `raid_target` 72, `vehicle_bay` 65, `sewer_access` 61 | `(309.9, -1908.5, -6.3)` |
| 197 | `ma_wat_lch_06` | scanner_hustle | 4 | `raid_target` 81, `officer_site` 60 | `(-2056.8, 1226.4, 3.9)` |
| 365 | `sts_hey_gle_03` | fixer_gig | 3 | `raid_target` 87, `rooftop_access` 80, `elevator` 70 | `(-1451.1, -1031.0, 77.7)` |
| 405 | `sts_wat_lch_05` | fixer_gig | 3 | `raid_target` 81, `rooftop_access` 62, `club` 55 | `(-1925.4, 1148.8, 12.2)` |
| 145 | `ma_std_arr_14` | scanner_hustle | 2 | `raid_target` 87, `vehicle_bay` 65 | `(-26.4, -442.3, 7.4)` |
| 172 | `ma_wat_kab_02` | scanner_hustle | 2 | `rooftop_access` 80 | `(-787.5, 1872.4, 50.4)` |
| 293 | `mws_arr_03` | mini_world_story | 1 | — | `(-545.4, -670.8, 1.6)` |
| 330 | `mws_wat_04` | mini_world_story | 1 | `sewer_access` 80 | `(-1577.4, 2364.9, -135.1)` |
| 398 | `sts_wat_kab_08` | fixer_gig | 1 | `raid_target` 69, `stealth_entry` 60, `safehouse` 57 | `(-1234.1, 1974.2, 8.0)` |

Thirteen further roster sites carry NCPD units but a **rival's**
`default_faction_id` — NCPD at someone else's crime scene:

| Site | Code | dfid | Units | What it is |
| --- | --- | ---: | ---: | --- |
| 26 | `ma_cct_dtn_07` | 2 | 4 | Tyger Claws site; hazmat/enforcer/inspector cyberpsycho team |
| 176 | `ma_wat_kab_07` | 2 | 3 | Ho-Oh / Tyger Claws den; NCPD detective + 2 patrol at the aftermath |
| 198 | `ma_wat_lch_07` | 1 | 3 | Maelstrom scanner; one `Character.ma_wat_lch_07_police_man` + 2 follow-up |
| 263 | `ma_wbr_jpn_01` | 2 | 4 | robbery; `constable`, `coroner`, `investigator` — a forensic team |
| 265 | `ma_wbr_jpn_06` | 2 | 4 | same forensic team template |
| 279 | `ma_wbr_jpn_12` | 2 | 1 | execution scene; 1 `jpn_ncpd_police_melee2_baton` |
| 282 | `ma_wbr_jpn_16` | 2 | 3 | execution scene; inspector + 2 police |
| 285 | `ma_wbr_jpn_20` | 2 | 4 | Tyger Claws site; 4 police incl. `ma_wbr_jpne_20_ws_after_police_*` |
| 372 | `sts_hey_rey_08` | 3 | 2 | Valentinos bar; 2 NCPD inspectors at the aftermath |
| 385 | `sts_std_arr_12` | 24 | 2 | Petrochem gas station; 2 `cpz_ncpd_police` |
| 413 | `sts_wat_nid_07` | 1 | 1 | Maelstrom site; 1 NCPD |
| 358 | `sts_ep1_06` | 10 | 1 | Heavy Hearts; 1 NCPD (hostage/Barghest disguise scene) |
| 361 | `sts_ep1_10` | 10 | 3 | Abandoned Pacifica precinct; the 3 NCPD are **hostages** |

That last row matters: the only "NCPD" at the Pacifica precinct is people
Barghest captured. It is not an NCPD holding in 2077 and must not be seeded as
one. `[game-data]` `[wiki]`

---

## 4. Economic structure

NCPD is a **budget-consuming** faction, not a revenue faction. Its streams are
public funding and coercion, and the wiki's 2076–77 arc is that the funding
model is failing. `[wiki]`

### 4.1 Revenue streams → catalog locations

| Revenue stream | Code(s) | Catalog locations | Evidence / notes |
| --- | --- | --- | --- |
| Municipal police funding | `security_services` | All precincts (1, plus the Glen/Arroyo precincts in §8) | The city pays the department; Rhyne privatised it in 2076 to chase profit. `[wiki]` |
| Fines, fees and citations | `finance` | Little China precinct (1); any patrol beat | Fawlter "ordered beat cops to prioritize writing tickets instead of stopping or solving crimes" and charged 5€$ per minute for 911 calls. `[wiki]` The single most design-relevant line about NCPD income. |
| Seized assets / evidence chain | `finance`, `information` | NCPD Lab (2) | The lab holds the case evidence River Ward needs (*The Hunt*); the department's forensic monopoly is leverage. `[wiki]` |
| Custody and corrections | `security_services` | Night City Prison (3) | "the NCPD's primary maximum-security penitentiary, housing many of the city's most violent offenders". `[wiki]` |
| Licensing, permits and zoning | `finance`, `real_estate` | Night City Hall (4) | City Council is the licensing gate; NCPD enforces it. `[wiki]` See `factions-corps-fixers-independents.md` §4.2. |
| MaxTac retaliation | `mercenary` | No fixed site — deploys from wherever (§11.3) | Not income; it is the department's force-projection product. `[wiki]` `[script]` |
| Corporate sponsorship | `finance` | — | Official sponsor Night Corp; also "beholden to the interests of Arasaka and Militech". `[wiki]` No place record, so prose only. |

Only two catalog points earn anything in the game-world sense (Tactical Coffee
and, weakly, the Prison), and **neither earns for NCPD**. That is the honest
answer: NCPD has no economic holdings, only coercive ones. The design question
is therefore not "how much does this precinct earn" but "how much heat does
this sub-district generate, and who is willing to pay NCPD to suppress it".

### 4.2 Suppliers, customers, rivals

| Role | Party | Detail |
| --- | --- | --- |
| Sponsor | Night Corp | "The police force's official sponsor is Night Corp". `[wiki]` |
| Sponsor / creditor | Arasaka, Militech | "the NCPD is also beholden to the interests of Arasaka and Militech". `[wiki]` |
| Supplier (equipment) | Militech | M-10AF Lexington sidearm, Saratoga, Ajax, Tactician, Defender; Minotaur mechs, Wyvern and Bombus recon drones, Griffin combat drones, Robot R Mk.2 patrol robots. `[wiki]` |
| Supplier (forensics) | Subcontracted labs | "These laboratories are subcontracted by the NCPD" — the Glen lab. `[wiki]` |
| Supplier (vehicles) | Archer, Chevillon, Brennan, Thorton, Villefort, Zetatech | NCPD Enforcer, Ironclad, Overlord, Manticore, Atlus, Hellhound, Behemoth. `[wiki]` |
| Customer | The city | Municipal contract, via City Hall. `[wiki]` |
| Customer (off-book) | Mercenaries | "when official investigations get stonewalled, the NCPD will hire mercenaries on the sly" — NCPD *buys* access. `[wiki]` |
| Rival | Barghest | Runs its own Prevention Unit inside Dogtown; NCPD is barred. `[wiki]` |
| Rival | Voodoo Boys | Expelled the NCPD task force from Pacifica in 2072. `[wiki]` |
| Rival (structural) | Corporate security firms | "the Mayor's Office began considering … hiring firms from the corporate security industry to police Night City instead". `[wiki]` |
| Rival (internal) | MaxTac | Formally NCPD's C-SWAT, but "MAX-TAC are just criminals with a badge" and answers only at max heat. `[wiki]` |

---

## 5. Headquarters recommendation

### Primary HQ: **Little China NCPD Precinct**

Coordinates: `(-1395.511, 1284.071, 119.086)` (`[game-data]`
`markers.jsonl {mq010_spwn_police_station}`); the precinct's standing street
community anchor is `(-1449.250, 1211.810, 18.120)` (`{de_wat_lch_05_police_com}`).
`[game-data]`

Rationale:

1. **It is the only precinct the game actually builds.** The wiki names five
   2077 precincts; only Little China has a modelled building, and it is the one
   the wiki illustrates with four exterior photos and describes in terms of
   AV pads and NCART access. `[wiki]` Every other precinct is a text mention (§8).
2. **The whole block is a police installation.** The Little China community
   prefab carries `#lch_ncpd_guard`, `#lch_ncpd_investigate` ×3,
   `#ncpd_security_area` and `#ncpd_security_system`, and there is a standing
   4-unit NCPD community outside. `[game-data]` That is a permanent guard post
   with an alarm system — a defensible holding, not a scene.
3. **It has the transit and air access a seat needs.** Elevated NCART access at
   `(-1456.6, 1181.3, 46.0)` and roof AV pads, both per the wiki and consistent
   with the community's position. `[wiki]` `[game-data]` A weakened NCPD that
   has "pulled back to fortified holdings" would pick a building it can resupply
   by air — this is it.
4. **It is where the department is still doing police work in Act 2.** The
   *Happy Together* officers work out of this block, and in *The Hunt* River
   Ward is detained in the Little China precinct. `[wiki]` Recent, datable NCPD
   activity, not history.
5. **It sits in the highest-density NCPD sub-district.** Little China has 46
   NCPD areas / 127 records, the most of any sub-district (§2.2), and the
   neighbours are all accounted for: Tactical Coffee 174 m, Tom's Diner 173 m,
   Afterlife 274 m. `[game-data]`
6. **The nearest CC is rival-owned, which is the point.**
   `cc_lch_bradbury_market` is 119.8 m away and owned by the **Tyger Claws**
   (fid 2). `[game-data]` A capture here reads as taking a police station back
   from the gang that surrounds it — exactly the "weakened NCPD, fortified
   holdings" fiction.

Trade-off: the *named marker* is a **roof/upper-floor point** (z ≈ 119 at H10),
while the *street community* is z ≈ 18, **101 m lower** and **90 m away
horizontally**.
A capture radius must be horizontal; seed the horizontal anchor at the street
community (`-1449.250, 1211.810`) and treat the H10 marker as an interior
sub-point, or the trigger fires in the wrong place. Also note the precinct has
**no `sites.json` row**, so it carries no suitability tags and no garrison
count — its defenders are the 4 roster units at `{de_wat_lch_05_police_com}`
plus the prefab's `#lch_ncpd_guard` markers. `[game-data]`

### Alternate 1: **NCPD Lab, the Glen**

Coordinates `(-1518.258, -602.782, 7.850)` `[game-data]`
`markers.jsonl mirror_sm_scene_police_lab`.

The best-identified NCPD interior in the game: a dedicated `gamedataDistrict`
enum, a complete five-part asset tree, a named gig, and a wiki page describing
its function ("research and experiments concerning neuroscience, including
cyberpsychosis"). `[enum]` `[game-data]` `[wiki]` It loses because it is a
**subcontracted lab**, not a police station — the wiki is explicit that the
department subcontracts it, so holding it is holding a supplier, not a seat. It
also has no garrison: the only NCPD record nearby is `{sq021_com_doctor_mitsuko}`
(1 unit), and the lab is infiltrated, not defended. `[game-data]`

### Alternate 2: **Night City Prison, Arroyo**

Coordinates `(-518.190, -677.850, 7.520)` `[game-data]`.

The **only genuine NCPD garrison in the extract**: six communities, 28 NCPD
records, and 19 individually named `#std_arr_prison_ncpd_0NN` slotted posts.
`[game-data]` A defensible, self-contained, walled facility with a documented
function ("the NCPD's primary maximum-security penitentiary"). `[wiki]` It loses
on fiction: a prison is where the department *stores* people, not where it
*governs*, and it has no civilian or economic surface — zero gang links, zero
businesses, one job. Keep it as the faction's fortress, not its seat.

### Overruled / downgraded suggestions

- **The abandoned Pacifica precinct as HQ.** The most evocative NCPD building
  in the game, but **Barghest's** since 2072, and its "NCPD" roster entries are
  the three hostages in `sts_ep1_10_tv_crew_com`. `[game-data]` `[wiki]` It
  belongs in `barghest.md` (§3 #9); this doc only cross-references it.
- **City Hall as HQ.** The municipal seat and licensing gate, but it is **City
  Council's** building (fid 51), not NCPD's; NCPD is present only as the `mq061`
  hologram set and one area record. `[game-data]` Count it under City Council;
  treat NCPD's interest as a *legal* dependency.
- **The `mq030` MaxTac shootout as HQ.** Nine NCPD records at one spot looks like
  a garrison, but it is Jinguji's suit-store car park and the records are MaxTac
  arriving to kill Melisa Corey. `[game-data]` `[wiki]` It is a scene.
- **Any Dogtown or Pacifica holding.** NCPD is barred from both. `[wiki]`
  Everything NCPD-labelled there is a quest antagonist inside someone else's
  territory.

---

## 6. Priority list of control points

"CC" = nearest entry in `data/control_centers.json`; distance is horizontal
metres over **all** CCs regardless of `is_active`, with the current owner id in
brackets (2 = Tyger Claws, 3 = Valentinos, 4 = 6th Street, 20 = Arasaka, 22 =
Kang Tao).

| Rank | Control point | Rel. (1–5) | District / sub-district | Coordinates | Existing CC overlap | Why |
| ---: | --- | :---: | --- | --- | --- | --- |
| 1 | **Little China NCPD Precinct** | 5 | Watson / LittleChina | `-1395.511, 1284.071, 119.086` | `cc_lch_bradbury_market`, 119.8 m (2) | The only built precinct; whole-block police install; NCART + AV access; densest NCPD sub-district |
| 2 | **Night City Prison** | 5 | SantoDomingo / Arroyo | `-518.190, -677.850, 7.520` | `cc_arr_kendachi_plant`, 153.9 m (4) | The only real garrison: 6 communities / 28 units / 19 named slots; walled and self-contained |
| 3 | **NCPD Lab** | 4 | Heywood / Glen | `-1518.258, -602.782, 7.850` | `cc_gle_embers_promenade`, 103.2 m (3) | Dedicated district enum + full asset tree + named function; the forensic monopoly |
| 4 | **Night City Hall** | 4 | Heywood / Glen | `-1771.830, -1010.775, 94.700` | `cc_gle_reconciliation_park`, 203.4 m (3) | Licensing and permits; the civic lever NCPD exists to enforce. Shared with City Council |
| 5 | **Tactical Coffee (Tom's Diner)** | 2 | Watson / LittleChina | `-1496.860, 1142.577, 18.630` | `cc_lch_farrier_alley`, 171.6 m (2) | The only residual MaxTac presence; 20 NCPD units; a diner, so low relevance |

Five points, and only two of them are really NCPD's. Say it plainly: **NCPD has
two holdings worth capturing and three civic dependencies.**

### Test control point for the first in-game test: **Night City Prison**

Why this and not the HQ:

- **Clean ownership, by construction.** Six `mq062_*` communities at one walled
  site, 28 NCPD records, and 19 individually named `#std_arr_prison_ncpd_0NN`
  slots. `[game-data]` Who is being evicted is unambiguous — unlike the Little
  China precinct, which has no site row and whose garrison is a 4-unit
  community outside the building.
- **It is a genuine interior with real rooms.** Visitor centre, cellblock,
  yard, monitoring room, armory, garage, all named in the marker set
  (`mq062_Stealth_Cells_*`, `mq062_Stealth_Monitoring_*`,
  `mq062_Escape_FinalChoice_CommunityArea_Armory_*`,
  `mq062_Escape_Yard_CommunityArea_Reinforcement_*`). `[game-data]` A capture
  radius can be validated against geometry rather than guessed.
- **It is not the HQ**, so the first test exercises capture on a fortress.
- **It has a settled bbox.** The prison sits at `(-518, -678)` inside the Santo
  Domingo bbox despite six areas labelled `westbrook` (§2.3). Attribution is
  resolved by project id, so the seed is safe.

Trade-off: the nearest CC is `cc_arr_kendachi_plant`, 153.9 m away and owned by
**6th Street** (fid 4), and it is "Dewdrop Inn" — a gang bar, not a prison gate.
The seed relocates the faction's active CC onto the test point, which is fine
here because NCPD has no active CC to strand. Fallback if the test must be in the
HQ sub-district: the Little China street community
`{de_wat_lch_05_police_com}` at `(-1449.250, 1211.810, 18.120)` — but budget for
the fact that it has no site row and therefore no interior geometry.

---

## 7. Per-sub-district counts

This is the number to feed yield balancing. It counts **distinct named places**
NCPD owns or garrisons as a base — not scanner events, patrol beats or quest
corridors (`METHOD.md` §1.2 item 9). `Filler` is the deduped faction-occupied
site count minus any site already counted as a named place.

| Sub-district | Named lore-relevant places | Which ones | Filler | Noteworthy interiors |
| --- | ---: | --- | ---: | ---: |
| LittleChina | **2** | Little China NCPD Precinct; Tactical Coffee (Tom's Diner) | 1 | 1 (precinct, from `#ncpd_security_area`) |
| Arroyo | **1** | Night City Prison | 0 | 1 (cellblock / monitoring / armory / yard) |
| Glen | **2** | NCPD Lab; Night City Hall | 0 | 2 (lab floor; conference room) |
| **Total** | **5** | | **1** | 4 |

Reconciliation, stated honestly because the template's arithmetic does not apply:

- **2 of the 5 named places are site-backed** (Tactical Coffee = site 325; Night
  City Prison = the six `mq062` communities, not a site). **3 are record-only**
  (precinct, lab, City Hall) — corroborated by a `gamedataDistrict` enum, a
  prefab tree and a quest/job id each, but invisible to `sites.json`.
- 5 named (2 site-backed + 3 record-only) + 1 filler = 6 = the 5 catalog places
  plus the one leftover 1-unit miniworld story (site 293 or 330).
- The other 13 `default_faction_id == 50` sites are scanner hustles, which are
  **response**, counted in §11.1, not holdings. `named + filler = deduped
  occupied sites` cannot be made to close for this faction; §8, gap 4 explains
  why the rule needs a third column.

**Reading the numbers.** **Five** named points is the smallest catalog in the
project after Petrochem, and it is the honest answer: NCPD does not own places,
it owns *authority*. The one filler and the 15 `default_faction_id` sites are
places it attends. If the mod needs more NCPD capture points, inventing
precincts is not the answer — capture **response capacity** (§11.2), not map
polygons.

---

## 8. Gaps and uncertainties

1. **NCPD has zero owned sub-territories and the seed has no NCPD row
   anywhere.** `initial_owner_faction_id == 50` appears zero times in
   `sub_territories.json`; `landmarks.json` and `faction_headquarters.json` have
   no NCPD entry; `sites.json` has no police-building site. `[game-data]` The
   seed's grid cannot express this faction, which is why §11 exists.
2. **Two of the five wiki precincts have no in-game building.** The Glen and
   Arroyo precincts are treated as real in the wiki ("This large NCPD precinct
   is located not too far from City Hall and Coyoacan"; "located in Arroyo"),
   and the Glen one is datably active on 13 March 2077. `[wiki]` But there is no
   enum, no prefab and no marker for either. The closest candidates are
   speculative: `sts_hey_gle_03` is a Glen fixer gig with 3 NCPD units
   (`inspector` + 2 `police`) at `(-1451.1, -1031.0, 77.7)`, 200 m from City
   Hall, and `ma_std_arr_06` is an Arroyo scanner with 4 NCPD at
   `(-646.0, -1317.5, 8.0)`. `[game-data]` **Neither is a precinct.** Both stay
   `TBD` and unseeded. Precinct #5 is a book-only mention with no district or
   street at all. `[wiki]` If the mod wants a Glen or Arroyo precinct, someone
   has to pick a building on purpose and say so.
3. **The `mq061` City Hall marker is a hologram.** All eleven `mq061_*_sm_*`
   markers sit at `(-1317.810, -84.292, 0.000)` and the cluster lives under
   `#04_city_hall_v/#04_city_hall_holo` in **Corpo Plaza**, not the Glen.
   `[game-data]` METHOD §1.2 item 7 documents the snapping but not *why* — here
   the cause is a holographic set piece. The real City Hall is
   `#c_heywood/glen/loc_sq012_city_hall_conference_room_prefab…`. Any agent
   searching "city hall" will find the hologram first.
4. **The Little China precinct's exact building is `[inferred]`.** The wiki says
   "next to Megabuilding H10", and the block has a permanent
   `#ncpd_security_area` guard post, but no single marker names the precinct
   door. I anchored on the `police_station` marker plus the standing 4-unit
   community 31 m from the elevated NCART station. The precise footprint is
   unresolved.
5. **`district_code` is wrong for the prison, and the bbox cannot settle it.**
   Six `mq062_*` areas are labelled `westbrook`, and the Westbrook and Santo
   Domingo bboxes genuinely overlap along `y ∈ [-750, -565]`. Only the prefab
   path (`#c_santo_domingo/arroyo/…`) and the wiki disambiguate. `[game-data]`
   This is METHOD §2.2's `always_loaded_*` path-token bug, now confirmed on a
   **quest prefab** as well. Getting it wrong moves 6 areas / 28 records — a
   class-changing error.
6. **The Prison garrison is the only one, and it is a quest garrison.** All 28
   records are `mq062_*` communities authored for *Clampdown*. `[game-data]`
   They may despawn after the job, in which case NCPD has **no** persistent
   garrison anywhere and the faction is literally pure response. Test in-game
   before the mod relies on the prison as a capture point.
7. **`mws_se5_03` is an 18-unit NCPD area that is not police work.** It sits in
   the Badlands at `(-3460.1, -4041.3, 65.2)` and is a miniworld story; METHOD
   §1.1 item 11 names it as a scav/ambush set. `[game-data]` It is the largest
   single non-quest NCPD concentration after Tactical Coffee and must not be
   mistaken for a holding.
8. **NCPD has no vendors, no shops and no service counter.** None of the five
   catalog points is a business in the sim sense. The `security_services` /
   `finance` mapping is `[inferred]` from the wiki's funding and ticketing
   prose, not from any in-game income record. If the economy model needs NCPD to
   *earn*, the only defensible lever is `finance` on the ticketing line.
9. **MaxTac has no base on the map.** The wiki's only 2077 faction location for
   MaxTac is **Los Padres Penitentiary**, and it is `2077PL (mentioned)` only —
   no coordinates, no prefab, no enum. `[wiki]` Hammerman's MAX-TAC HQ is
   Cyberpunk RED lore in "South Night City", which is not a 2077 district.
   `[wiki]` MaxTac's in-game presence is entirely the prevention system's top
   heat tier (§11.3).
10. **`gamedataDistrict` has no precinct value but does have `Glen_NCPDLab`.**
    `refs/cyberpunk/orphans.swift:4896`. `[enum]` A dedicated NCPD lab enum and
    *no* precinct enum is primary-source confirmation that the game models
    exactly one NCPD facility as a location.
11. **The 15 `default_faction_id == 50` sites are all scanner hustles,
    miniworld stories or fixer gigs.** Not one has a police `site_kind`.
    `[game-data]` Treating `default_faction_id` as ownership, as METHOD §1.1
    item 5 warns, would invent fifteen police stations.
12. **Two of the three 1-unit miniworld stories are unusable as holdings.** Site
    330 `mws_wat_04` anchors at z = −135.1 (below the map) and site 293
    `mws_arr_03` has no suitability tags at all. `[game-data]` They are filler
    only.
13. **One NCPD "unit" is an android.** `Character.kab_ncpd_android_android2_ajax_ma`
    at site 172 (`ma_wat_kab_02`). `[game-data]` Per METHOD §1.2 item 4 it is a
    machine, not a garrison, and is reported separately here.
14. **NCPD roster records cluster by geocode, not by function.** The records are
    `ncpd_police_*`, `ncpd_inspector_*`, `ncpd_investigator_*`,
    `ncpd_constable_*`, `ncpd_hazmat_*`, plus geocode-prefixed variants
    (`gle_ncpd_*`, `rey_ncpd_*`, `nid_ncpd_*`, `jpn_ncpd_*`, `kab_ncpd_android_*`).
    `[game-data]` The geocode prefix is the **costume**, not the station —
    `nid_ncpd_*` constables appear at JapanTown sites 263 and 265. Do not derive
    garrisons from record prefixes.
15. **NCPD's wiki organisation page never names a 2077 headquarters.** Its
    infobox carries 2010 and 2020 addresses only, and `faction_locations` is
    "See Precincts". `[wiki]` METHOD §4's "read `headquarters=`" gives a
    historical answer for this faction; the 2077 answer has to be assembled from
    the precinct list, and only one of those is in the world data.

---

## 9. Sources

- Local: `dist/extract/areas.jsonl` (273 NCPD rows, 696 records; 193 dominant
  `cs_*`), `dist/extract/markers.jsonl` (40,738 rows; 99 police/civic names
  screened), `data/sites/{sites,communities,rosters,suitabilities,spots,guards,doors,devices}.json`,
  `data/{districts,factions,control_centers,sub_territories,landmarks,faction_headquarters}.json`.
- Raw sectors: `dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_{0,1,2}.streamingsector.json`
  — prefab/node-name strings, plus `nodeIdx → nodeData[i].transform.position`
  resolution used to confirm the police-lab and City Hall node positions and to
  read `#lch_ncpd_*`, `#ncpd_security_area`, `#mq062_*` and
  `#std_arr_prison_ncpd_*`.
- Enums / script: `refs/cyberpunk/orphans.swift` (`gamedataDistrict` at 4826ff,
  `Glen_NCPDLab` 4896, `gamedataNPCRarity.MaxTac` 5095, `District_Record`
  18392ff, `DistrictPreventionData_Record` 32827ff, `PreventionHeatData_Record`
  33503ff);
  `refs/cyberpunk/core/systems/preventionSystem.swift` (3052, 3057, 3078–3099,
  3104–3117); `refs/cyberpunk/core/systems/prevention/districtManager.swift`
  (10–56); `refs/cyberpunk/core/systems/preventionSpawnSystem.swift` (32, 36,
  44–76); `refs/cyberpunk/core/systems/prevention/policeAgentsRegistry.swift`
  (88–126); `refs/RED4ext.SDK/include/RED4ext/Scripting/Natives/Generated/game/data/DistrictPreventionData_Record.hpp`.
- Wiki: [NCPD](https://cyberpunk.fandom.com/wiki/NCPD),
  [NCPD Precinct (disambiguation)](https://cyberpunk.fandom.com/wiki/NCPD_Precinct_(disambiguation)),
  [Little China NCPD Precinct](https://cyberpunk.fandom.com/wiki/Little_China_NCPD_Precinct),
  [Glen NCPD Precinct](https://cyberpunk.fandom.com/wiki/Glen_NCPD_Precinct),
  [Arroyo NCPD Precinct](https://cyberpunk.fandom.com/wiki/Arroyo_NCPD_Precinct),
  [NCPD Precinct 5](https://cyberpunk.fandom.com/wiki/NCPD_Precinct_5),
  [Pacifica NCPD Precinct](https://cyberpunk.fandom.com/wiki/Pacifica_NCPD_Precinct),
  [NCPD Lab](https://cyberpunk.fandom.com/wiki/NCPD_Lab),
  [Night City Prison](https://cyberpunk.fandom.com/wiki/Night_City_Prison),
  [Night City Hall](https://cyberpunk.fandom.com/wiki/Night_City_Hall),
  [Night City Police Headquarters](https://cyberpunk.fandom.com/wiki/Night_City_Police_Headquarters),
  [MaxTac](https://cyberpunk.fandom.com/wiki/MaxTac),
  [MAX-TAC Headquarters](https://cyberpunk.fandom.com/wiki/MAX-TAC_Headquarters),
  [Los Padres Penitentiary](https://cyberpunk.fandom.com/wiki/Los_Padres_Penitentiary),
  [NCPD Patrol Officer](https://cyberpunk.fandom.com/wiki/NCPD_Patrol_Officer),
  [Cyberpunk 2077 Mini-World Stories](https://cyberpunk.fandom.com/wiki/Cyberpunk_2077_Mini-World_Stories),
  [Happy Together](https://cyberpunk.fandom.com/wiki/Happy_Together),
  [The Hunt](https://cyberpunk.fandom.com/wiki/The_Hunt),
  [Clampdown](https://cyberpunk.fandom.com/wiki/Clampdown),
  [Black Steel In The Hour of Chaos](https://cyberpunk.fandom.com/wiki/Black_Steel_In_The_Hour_of_Chaos).
- Earlier repo research: `docs/research/factions/METHOD.md`,
  `docs/research/factions/barghest.md` (§3 #9, the Pacifica precinct),
  `docs/research/factions-corps-fixers-independents.md` §4.1–4.3 (NCPD, City
  Council, NCPrison), `docs/research/factions-gangs-territories.md` (district
  table, prevention data).

---

## 10. Findings about METHOD.md for this faction

Recorded here rather than in `METHOD.md` (other agents are writing sibling files)
so the method owner can fold them in.

1. **§2's source ranking (rosters first) does not work for civic factions.**
   The best source here was `markers.jsonl` plus raw-sector node positions,
   because the four real holdings have **no site row**. Add: "if a faction's
   named buildings have no `sites.json` row, go to raw-sector node names and
   resolve positions through `nodeIdx → nodeData[i].transform.position`."
2. **§1.2 item 7 needs the *cause* of snapping, not just the symptom.** The
   `mq061` cluster snaps because it is a **holographic set piece**
   (`#04_city_hall_holo`). Naming the cause would stop the next agent reporting
   "City Hall is in Corpo Plaza".
3. **§1.2 item 1's hologram warning should name `mq061` explicitly.** It
   mentions `mq061_*` in passing; the City Hall case is the concrete example.
4. **§8's two-tier count has no place for a faction whose named places are
   record-only.** Three of NCPD's five named points have no site, so
   `named + filler = deduped sites` cannot reconcile. Add a `record-only`
   column, or state the identity as "named = site-backed + record-only".
5. **The template needs an optional "response vs holdings" section.** NCPD —
   and probably MaxTac and Trauma Team — are pressure factions, and §9's
   template assumes turf. The §11 pattern (classify every area, count per class,
   separate the capture map from the density map) should be an optional section.
6. **§4's "read `headquarters=` from the org infobox" fails for NCPD.** The
   infobox carries only historical HQ addresses. Add: "for civic factions read
   `faction_locations=` and the linked disambiguation page, not
   `headquarters=`."
7. **§2.2's `district_code` warning must extend to quest prefabs, and bbox
   overlap must be handled.** `mq062_*` is an Arroyo asset labelled `westbrook`,
   and the Westbrook/Santo Domingo bboxes overlap by 185 m on Y, so "inside the
   bbox" does not disambiguate. Between districts the **prefab path** is
   authoritative.
8. **A dedicated `gamedataDistrict` value is an *identity* signal, not just an
   existence check.** `Glen_NCPDLab` (`orphans.swift:4896`) is primary-source
   proof the game has exactly one NCPD facility. Add to §1.1 item 3: enum values
   that are asset names (`<Subdistrict>_<Place>`) identify the place.

---

## 11. Holdings vs response presence

This section exists because NCPD is the first faction where "what it holds" and
"where it appears" are almost completely different things. The mod reframes NCPD
as **weakened**: pulled back to fortified holdings, streets abandoned. The data
supports that reading harder than the brief expected — **67% of NCPD's area rows
(183 of 273) are dynamic response**, and only **6 rows are a garrison**. Of the
194 `cs_*` rows, 34 are patrol and 160 are crime response.

### 11.1 Classification of every NCPD-affiliated area

Rules, applied in order (first match wins), so the classes are mutually
exclusive and total the 273 rows:

1. **holding** — a permanent NCPD facility the faction owns and stands in:
   precinct, station, lab, prison, City Hall security, MaxTac base, armory,
   impound. Match in the raw areas: `mq062_*` (the prison's own communities).
   The three record-only buildings (precinct, lab, City Hall) have no
   holding-shaped area rows and are covered in §3/§7.
2. **response** — NCPD arrives *after* an event: all other `cs_*` scanner crimes
   and crime scenes, `post_ma_police_com` / `*_after_police_com` / `*_after_com`
   follow-ups, and `de_*`/`ma_*` police groups at a **rival's** site.
3. **patrol/roadblock** — transient presence with no crime attached:
   `cs_patrol_*`, `cs_highway_patrol_*`, `cs_dragnet_*`,
   `cs_bls_highway_patrol_*`.
4. **quest-only** — appears only inside a scripted job or world story:
   `mq*`/`sq*`/`sa_ep1_*`/`sts_*`/`wst_*`/`mws_*` scenes.

| Class | Areas | Records | What it is |
| --- | ---: | ---: | --- |
| **holding** | **6** | **28** | The Night City Prison garrison (`mq062_*`), Arroyo. Nothing else in the raw areas. |
| **response** | **183** | **440** | `cs_*` scanner events minus patrol (160 areas), plus 7 follow-up groups and 16 other police/dynamic-event rows |
| **patrol/roadblock** | **34** | **68** | `cs_patrol` 15, `cs_dragnet` 10, `cs_highway_patrol` 8, `cs_bls_highway_patrol` 1 |
| **quest-only** | **50** | **160** | Job and world-story set pieces |
| **Total** | **273** | **696** | |

Sub-district detail (areas; records in the class column are marked only where
nonzero):

| Sub-district | Areas | Records | `cs_*` | holding | response | patrol | quest |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| LittleChina | 46 | 127 | 30 | 0 | 33 | 4 | 9 |
| Glen | 37 | 84 | 29 | 0 | 25 | 6 | 6 |
| Downtown | 24 | 62 | 18 | 0 | 14 | 4 | 6 |
| Arroyo | 22 | 59 | 15 | **6 (28)** | 12 | 3 | 1 |
| JapanTown | 21 | 51 | 15 | 0 | 16 | 3 | 2 |
| RanchoCoronado | 17 | 45 | 15 | 0 | 13 | 2 | 2 |
| Wellsprings | 17 | 43 | 15 | 0 | 13 | 3 | 1 |
| Kabuki | 16 | 45 | 12 | 0 | 14 | 1 | 1 |
| CorpoPlaza | 12 | 28 | 8 | 0 | 6 | 2 | 4 |
| CharterHill | 12 | 29 | 12 | 0 | 11 | 1 | 0 |
| Northside | 10 | 17 | 6 | 0 | 6 | 2 | 2 |
| VistaDelRey | 10 | 25 | 7 | 0 | 7 | 2 | 1 |
| Badlands | 6 | 25 | 2 | 0 | 2 | 0 | 4 |
| Coastview | 5 | 7 | 1 | 0 | 2 | 1 | 2 |
| NorthOaks | 5 | 14 | 3 | 0 | 3 | 0 | 2 |
| Dogtown | 4 | 8 | 0 | 0 | 0 | 0 | 4 |
| WestWindEstate | 4 | 14 | 1 | 0 | 1 | 0 | 3 |
| ArasakaWaterfront | 4 | 10 | 4 | 0 | 4 | 0 | 0 |
| MorroRock | 1 | 3 | 1 | 0 | 1 | 0 | 0 |

**Important caveat.** Area-row classes and *place* classes are different counts.
The six "holding" areas are six communities inside **one building** (the
prison), which is why §7 says 1 named place for Arroyo, not 6. Conversely, the
Little China precinct, the Glen lab and City Hall are holdings that appear in
**zero** holding-shaped area rows — the precinct's rows are `mq010_com_ncpd` (a
2-unit apartment-door scene, classed quest) and `{de_wat_lch_05_police_com}`
(4 units, classed response because it carries a `de_` prefix). Read §11.1 as the
**response-density map** and §7 as the **capture map**; they are not meant to
agree.

### 11.2 The response mix (what the mod should model)

`cs_*` alone is 194 areas / 442 records. Breaking it down by authored event
family shows what "police presence" actually consists of in this game:

| Family | Areas | Records | Meaning for the sim |
| --- | ---: | ---: | --- |
| `cs_heavy_*` | 27 | 69 | Heavily armed response (enforcers, Centaurs). The closest thing to a "raid". |
| `cs_crime_scene_*` | 19 | 60 | Static crime scene with forensic officers. |
| `cs_handcuffed_*` | 16 | 32 | Arrest in progress — NCPD already on scene. |
| `cs_patrol_*` | 15 | 30 | Pure patrol beat, no crime. **The only true ambient presence.** |
| `cs_cyberpsycho_disposal_*` | 12 | 44 | Hazmat + enforcer + investigator at a psych scene. MaxTac-adjacent. |
| `cs_cars_*` | 12 | 24 | Crashed vehicles. |
| `cs_biohazard_*` | 11 | 22 | Contamination response. |
| `cs_car_*` (flipped/execution) | 10 | 16 | Vehicle incidents. |
| `cs_dragnet_*` | 10 | 20 | Dragnet / cordon (classed patrol). |
| `cs_corp_*` | 8 | 9 | Corporate-death response. |
| `cs_body_*` | 8 | 16 | Body found. |
| `cs_disposed_body_*` | 8 | 32 | Body-disposal scene. |
| `cs_highway_patrol_*` | 8 | 16 | Highway patrol (classed patrol). |
| `cs_police_*` | 7 | 14 | Police-execution scenes — **NCPD as the victim**. |
| `cs_riots_*` | 6 | 6 | Riot response. |
| `cs_escaping_*` | 6 | 12 | Escaping-suspect chase. |
| `cs_interior_*` | 4 | 8 | Interior intervention. |
| `cs_drowner_*` | 4 | 8 | Drowned body. |
| `cs_drones_*` | 2 | 2 | Drone recon. |
| `cs_bls_highway_patrol_*` | 1 | 2 | Badlands highway. |

The single most important number in this table: **`cs_patrol_*` is 15 areas,
30 records — 5.5% of NCPD's area rows.** NCPD has roughly one twentieth of its
map presence as ordinary patrolling. Everything else is a crime it is responding
to. A "weakened NCPD" is not a fiction imposed on the data; it is what the data
already says.

Two derived numbers the sim can use directly:

- **Escalation mass.** `cs_heavy` + `cs_cyberpsycho` = 39 areas / 113 records =
  the armed/psychotic tier. This is the pool MaxTac pressure should be built
  from (§11.3).
- **Forensic mass.** `cs_crime_scene` + `cs_disposed_body` + `cs_body` +
  `cs_handcuffed` = 51 areas / 140 records. This is what the NCPD Lab (§3 #2)
  exists to service and is the natural consumer of a lab control point.

### 11.3 MaxTac, separately

MaxTac is a **heat-tier unit, not a place**. The evidence:

- `gamedataNPCRarity.MaxTac = 2` (`refs/cyberpunk/orphans.swift:5095`) — MaxTac
  is an NPC *rarity*, i.e. a spawn class. `[enum]`
- The prevention system tracks MaxTac agents explicitly:
  `policeAgentsRegistry.GetMaxTacNPCCount()`, `GetMaxTacNPCList()`,
  `IsPreventionMaxTac(puppet)`, `DistanceSquaredToTClosestMaxTacAgent(position)`
  (`refs/cyberpunk/core/systems/prevention/policeAgentsRegistry.swift:88–126`). `[script]`
- Heat values are tunable per action: `HeatKillMaxTac()` and
  `HeatShootMaxTac()` (`refs/cyberpunk/orphans.swift:32309, 32315`). `[script]`
- The wiki confirms the deployment rule: at maximum wanted rating "the
  deployment MaxTac officers … serve as the final enemy type to hunt V down";
  they operate in squads of four. `[wiki]`

On the map, MaxTac appears in exactly three ways, none of them a base:

| Presence | Record | Coordinates |
| --- | --- | --- |
| Residual off-duty operators at Tom's Diner | site 325 spots `#nws_tactical_coffee_maxtac1…4`; wiki: "including MaxTac operators" | `(-1497.8, 1150.3, 18.8)` and neighbours `[game-data]` `[wiki]` |
| `mq030` Midtown shootout (Jinguji car park) | `{mq030_max_tac}` 9 units; markers `q001_00ff_sm_max_tac` | `(-1877.956, 83.043, 7.520)` `[game-data]` |
| `q305` / coalition ambush in Dogtown | `{q305_com_ambush_maxtac}` 5/24; `{q305_com_wtp_dead_max_tac}` | `(-2742.0, -2469.5, 17.7)`; `(-2446.0, -2554.5, -7.0)` `[game-data]` |

Vehicles: MaxTac uses the same NCPD fleet (Archer Hella EC-H i860 NCPD
Enforcer, Militech Manticore, Zetatech Atlus, Militech Behemoth, Militech
Hellhound "Man o' War"), plus the `IsAVMaxTac` flag (`orphans.swift:2244`) and
`SpawnMaxTacAVWithDelayRequest` (`orphans.swift:58350`) for AV deployment.
`[wiki]` `[script]`

**Bases: none.** The wiki's 2077 "faction location" for MaxTac is Los Padres
Penitentiary, and it is `(mentioned)` only — no marker, no prefab, no enum.
`[wiki]` The RED-era MAX-TAC HQ in "South Night City" is not a 2077 district.
`[wiki]` Do not seed a MaxTac base; seed MaxTac as a **heat-5 consequence** and
use the Tom's Diner spots as the only physical trace.

### 11.4 The vanilla police system as a hook

The game already has a **per-district police-pressure model**, and its public
surface is small. All references are `[script]` unless tagged otherwise.

| Hook | Where | What it gives the mod |
| --- | --- | --- |
| `District_Record.PreventionPreset()` → `DistrictPreventionData_Record` | `refs/cyberpunk/orphans.swift:18400` | Per-district heat table: `Heat1()`…`Heat5()`, `Recon()`, `InputLockTime()`, `SpawnOriginMaxDistance()` (`orphans.swift:32827–32858`). **The per-district police-response knob.** |
| `District_Record.CrimeMultiplier()` | `orphans.swift:18426`; `districtManager.swift:26-27` | A float the prevention system reads on every district entry (`preventionSystem.swift:3057`). Already mirrored in `data/districts.json` (City Center 1.2 … Pacifica 0.7). Multiply heat gain by it and a poor district escalates faster. |
| `District_Record.GunShotStimRange()`, `ExplosiveDeviceStimRangeMultiplier()` | `orphans.swift:18424, 18428` | How far a firefight pulls patrols. Directly reusable as mission "noise". |
| `PreventionHeatData_Matrix_Record` | `orphans.swift` (`Heat0..Heat5`, `Recon`, `MinimapData`) | Unit and vehicle pools per heat band. |
| `PreventionHeatData_Record.UnitRecordsPool()` / `VehicleRecordPool()` / `AvRecord()` / `FallbackUnitData()` | `orphans.swift` (`PreventionHeatData_Record`) | The exact NPC/vehicle pools per band — the template for a mod-owned "response tier". |
| `OnDistrictAreaEntered` re-sync | `preventionSystem.swift:3052–3058` | The single place the vanilla system refreshes preset + multiplier on crossing a district boundary. A mod hook here can swap the preset by **sub-territory** instead of district. |
| `GetPreventionMatrixPresetForCurrentDistrict` Dogtown branch | `preventionSystem.swift:3078–3099` | **Proof the game already lets ownership change the police model.** Dogtown uses `PreventionData.DogTownDataMatrix` and switches to `DogTown_Kurt_DataMatrix` or `DogTown_Bennet_DataMatrix` on the `mq304_city_scenes_active` / `mq304_bennett_prevention` facts. An owner-driven prevention preset, implemented upstream. **The mod's "police response depends on who controls the sub-district" is this mechanism, generalised.** |
| `PreventionSystem` fallbacks | `preventionSystem.swift:3104–3117` | `PreventionData.NCPDDataMatrix` and `PreventionData.NCPD` are the safe defaults for a district with no record — the exact records a synthetic sub-territory should point at. |
| `PreventionSpawnSystem.TogglePreventionActive(isActive)` | `preventionSpawnSystem.swift:76` | Turns police response off entirely — the blunt instrument for a captured precinct. |
| `ToggleFreeArea(areaRef, enable)` / `IsPointInPreventionFreeArea(point)` | `preventionSpawnSystem.swift:64`, and `IsPointInPreventionFreeArea` | Mark a captured holding as a no-police zone. |
| `TogglePreventionQuestTrigger(areaRef, enable)` | `preventionSpawnSystem.swift:66` | Force de-escalation at a trigger (quests use this today). |
| `RequestRoadBlockadeSpawn(...)`, `RequestAVSpawn*` | `preventionSpawnSystem.swift:36, 44–48` | Spawn roadblocks and AVs on demand — the "fortified holding" reinforcement path. |
| `IsPlayerInDogTown()` | `preventionSpawnSystem.swift:32` | The existing special-case query a mod would clone for "is player in a captured holding". |

**Recommended model, in one sentence:** keep `PreventionSystem` as the engine,
but make the **preset lookup** sub-territory-aware. Vanilla reads
`District_Record.PreventionPreset()` per district
(`preventionSystem.swift:3104`), and the Dogtown branch already demonstrates an
owner-keyed substitution (`preventionSystem.swift:3078–3099`). A sub-district
held by a gang should point at a preset with a higher `CrimeMultiplier` and
thinner heat pools; a sub-district held by NCPD or a corp should point at the
`NCPDDataMatrix` default. That gives "who controls the sub-district changes
police response" without replacing the vanilla system.

Two caveats. First, `CrimeMultiplier()` is read into `m_districtMultiplier`
(`preventionSystem.swift:65, 982–987`) but that field is **set only**, never
consumed, in the shipped script — consumption is in native code. Treat it as a
real knob but verify behaviour in-game. Second, Dogtown's override is gated on
**quest facts**, not ownership; the mod would be the first thing in the game to
key police response to a mutable ownership model, so it inherits whatever
assumptions are baked into the native heat path.

---

## 12. Machine-readable block

Strict JSON for seeding (contract in [`METHOD.md`](./METHOD.md) §10). Every
coordinate was re-verified against the local record named in `source` on
2026-11-25; none came from the wiki. **`control_points` contains holdings only**
— the four places NCPD owns or garrisons. City Hall is included because NCPD's
policing authority is exercised from it, and it is flagged `shared_with` so the
City Council doc can also claim it. Tactical Coffee is deliberately **excluded**:
it is a diner NCPD visits, i.e. response presence, not a holding (§11.1).

```json
{
  "faction_code": "ncpd",
  "hq": {"name": "Little China NCPD Precinct", "district": "Watson", "sub_district": "LittleChina", "x": -1395.511, "y": 1284.071, "z": 119.086, "source": "dist/extract/markers.jsonl {mq010_spwn_police_station}; street anchor dist/extract/areas.jsonl {de_wat_lch_05_police_com} (-1449.250, 1211.810, 18.120); guard post #lch_ncpd_guard / #ncpd_security_area", "confidence": "game-data+wiki+inferred"},
  "alternate_hqs": [
    {"name": "Night City Prison", "district": "SantoDomingo", "sub_district": "Arroyo", "x": -518.19, "y": -677.85, "z": 7.52, "source": "dist/extract/markers.jsonl mq062_02_sm_hook_entrance_visitor", "confidence": "game-data+wiki"},
    {"name": "NCPD Lab", "district": "Heywood", "sub_district": "Glen", "x": -1518.258, "y": -602.782, "z": 7.85, "source": "dist/extract/markers.jsonl mirror_sm_scene_police_lab", "confidence": "game-data+wiki"}
  ],
  "test_control_point": {"name": "Night City Prison", "district": "SantoDomingo", "sub_district": "Arroyo", "x": -518.19, "y": -677.85, "z": 7.52, "source": "dist/extract/markers.jsonl mq062_02_sm_hook_entrance_visitor; garrison dist/extract/areas.jsonl {mq062_prison_openworld_combat_com_area} (-522.370, -651.050, 7.370)", "confidence": "game-data+wiki"},
  "control_points": [
    {"rank": 1, "name": "Little China NCPD Precinct", "type": "police_station", "relevance": 5, "district": "Watson", "sub_district": "LittleChina", "x": -1395.511, "y": 1284.071, "z": 119.086, "source": "dist/extract/markers.jsonl {mq010_spwn_police_station}; permanent guard post #lch_ncpd_guard / #ncpd_security_area in #c_watson/little_china/little_china_community_prefabYXM4BXA; street anchor {de_wat_lch_05_police_com} (-1449.250, 1211.810, 18.120)", "confidence": "game-data+wiki+inferred", "interior": true, "revenue_streams": ["security_services", "finance"], "nearest_cc_code": "cc_lch_bradbury_market", "nearest_cc_m": 119.8},
    {"rank": 2, "name": "Night City Prison", "type": "prison", "relevance": 5, "district": "SantoDomingo", "sub_district": "Arroyo", "x": -518.19, "y": -677.85, "z": 7.52, "source": "dist/extract/markers.jsonl mq062_02_sm_hook_entrance_visitor; 19 named slots #std_arr_prison_ncpd_002..020 in #c_santo_domingo/arroyo/arroyo_openworld_prefabPTAJFCA", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["security_services", "finance"], "nearest_cc_code": "cc_arr_kendachi_plant", "nearest_cc_m": 153.9},
    {"rank": 3, "name": "NCPD Lab", "type": "laboratory", "relevance": 4, "district": "Heywood", "sub_district": "Glen", "x": -1518.258, "y": -602.782, "z": 7.85, "source": "dist/extract/markers.jsonl mirror_sm_scene_police_lab; prefab #c_heywood/glen/#loc_sq021_police_lab; enum gamedataDistrict.Glen_NCPDLab (refs/cyberpunk/orphans.swift:4896)", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["rnd", "information"], "nearest_cc_code": "cc_gle_embers_promenade", "nearest_cc_m": 103.2},
    {"rank": 4, "name": "Night City Hall", "type": "city_hall", "relevance": 4, "district": "Heywood", "sub_district": "Glen", "x": -1771.83, "y": -1010.775, "z": 94.7, "source": "dist/extract/markers.jsonl sq012_02a_sm_braindance; prefab #c_heywood/glen/loc_sq012_city_hall_conference_room_prefabSADQP6Y; NOT the mq061 hologram at (-1317.810,-84.292,0.000)", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["finance", "real_estate"], "nearest_cc_code": "cc_gle_reconciliation_park", "nearest_cc_m": 203.4, "shared_with": "city_council"}
  ],
  "subdistrict_counts": {
    "LittleChina": {"named": 2, "filler": 1},
    "Arroyo": {"named": 1, "filler": 0},
    "Glen": {"named": 2, "filler": 0}
  }
}
```
