# Militech — Lore-Relevant Control Points

Status: faction research run, 2026-11-25. One faction, one document.
Scope: replace the generic control-centre grid with places Militech actually
owns, runs, protects or garrisons in Night City, the Badlands and Dogtown, with
verified coordinates, an economic map, an HQ pick, a ranked capture list and
honest per-sub-district counts. Method: this doc conforms to
[`METHOD.md`](./METHOD.md) — including the batch-1 corrections in §1.1, which
were applied first. `AGENTS.md` was read first. No commits, no game launch.

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Position, site, community, roster or spawn record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/artbook/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My reasoning links a named place to a game record; reasoning stated | Weak, flagged |

No coordinate below is guessed. Every `(x, y, z)` is copied from a local site,
marker, seed anchor or sub-territory record, or marked `TBD`. No coordinate in
this document came from the wiki.

---

## 1. Summary

Militech International Armaments is the NUSA's arms manufacturer and private
military: 300,000 employees plus 647,000 contractors in 2077, €$432 billion
(nationalised), headquartered in Rosslyn, Virginia, with a Night City **regional
HQ in Corpo Plaza**. Its declared business is arms manufacturing, military
vehicle production and mercenary contracting, and — uniquely among the
megacorps — it is **nationalised**: the NUSA government owns it, a former CEO
(Rosalind Myers) is president, and ex-Militech officials staff the Ministry of
Defense. `[wiki]`

That single fact drives the whole footprint, and it is why a Militech control
point is not always a Militech *building*:

- **Corpo Plaza (City Center)** — the **Militech Offices**, the regional HQ,
  opposite Arasaka Tower across the Plaza. Administrative, contract-sales and
  command seat. `[wiki]`
- **The Badlands** — the real weight: the **Sunshine Motel outpost**, the
  **Militech Detention Center**, the **SoCal Border Crossing**, plus patrol,
  convoy and execution encounters across the eastern and southern desert.
  `[wiki]` `[game-data]`
- **Downtown (City Center)** — **Gold Beach Marina**, where Militech is the
  marina's new security contractor. `[wiki]` `[game-data]`
- **Pacifica / Dogtown** — the **Cynosure** black sites (Sites C and D),
  abandoned Militech AI-research facilities now under Dogtown. `[wiki]`

Game-data scale: **136 community areas** contain Militech spawns, **121** are
Militech-dominant, the seed gives it **10 sub-territories**, and its units stand
in **23 deduped sites / 133 deduped roster entries** (raw join says 25 sites /
159 units — see §8.1). The weight is Badlands (67 areas, 400 entries), then
Watson's prologue roadblocks (Northside, LittleChina, Kabuki — 26 areas), then
Corpo Plaza and Downtown. `[game-data]`

Two cautions that shape every number below:

1. **Many "Militech" entities are Militech-brand hardware, not Militech
   personnel.** Wyvern/Griffin/Octant/Centaur drones and security droids carry
   `faction_id 21` because they are Militech products, and they appear on other
   factions' turf (`kab_militech_drone_wyvern_hard`, `hil_militech_drone_griffin_easy`,
   `q113_com_arasaka_estate_mech_drones` at Arasaka's estate). Presence of a
   Militech drone is not ownership. `[game-data]`
2. **Militech is the NUSA's army.** In Phantom Liberty the NUSA/FIA presence in
   Dogtown and the `q302`–`q305` set pieces carry Militech-tagged drones,
   androids and robots. Those are state/military assets in a story, not
   capturable corporate property. `[game-data]` `[wiki]`

---

## 2. Territory

### 2.1 Districts

| Evidence kind | Result |
| --- | --- |
| (a) Wiki/lore | Global HQ Rosslyn, Virginia (across the Potomac from Washington D.C.). A Night City regional HQ in **Corpo Plaza** ("regional offices… contain the headquarters for the local ranking Militech Officer"). Regional offices handle local bulk arms contracts, mercenary contracting and distribution. `[wiki]` |
| (b) Vanilla map gang panel | **Not applicable.** `data/districts.json` `vanilla_gangs` lists gangs only (`Watson: [Maelstrom, TygerClaws]`, `Badlands: [Aldecaldos, Wraiths]`, `CityCenter: []`). Militech is a megacorp, absent from the gang panel by design. |
| (c) Game-data counts | 136 community areas contain Militech; 121 Militech-dominant. 23 deduped occupied sites / 133 deduped units. 10 seeded sub-territories. 65 distinct character records (many are drones/droids). `[game-data]` |

The 10 seeded sub-territories (`data/sub_territories.json`,
`initial_owner_faction_id = 21`) and what actually justifies each:

| Sub-territory | Display name | Seed owner evidence |
| --- | --- | --- |
| `cpz_militech_hq` | Militech HQ Concourse | **Solid.** Contains site 11 `ma_cct_cpz_06` (4 Militech units, `default_faction_id 21`). `[game-data]` |
| `cpz_ring_road_north` | Corpo Plaza North Overpass | **Weak but real.** Site 12 `ma_cct_cpz_10`, 4 Militech drones only. `[game-data]` |
| `dtn_goldsmith_dock` | Downtown West Pier | **Solid.** Site 40 `ma_cct_dtn_15`, 6 units incl. a netrunner workspot. `[game-data]` |
| `dtn_skyline_west` | Skyline & Salinas Plaza | **Unexplained.** No Militech site or unit inside it (site 23 there is Animals-default). See §8.7. `[game-data]` |
| `hil_gold_beach` | Gold Beach Marina | **Wrong on both counts.** Gold Beach Marina is Downtown/City Center, not Charter Hill (`[wiki]`), and no Militech site or unit sits at `(344.5, -504.4)`. See §8.6. `[game-data]` |
| `bls_militech_outpost` | Red Peaks Militech Outpost | **Solid.** Contains sites 342, 345 and two Badlands scanner hustles. The place is the **Sunshine Motel** per the wiki; "Red Peaks" is the neighbouring hill region. `[game-data]` `[wiki]` |
| `bls_solar_station` | Jackson Plains Solar Arrays | **Artifact.** Owned only because the two detention-centre sites were bucketed here; the arrays themselves are the **Night Corp Solar Farm**. See §8.4. `[game-data]` `[wiki]` |
| `bls_north_oil_fields` | North Sunrise Oil Fields | **Artifact.** Owned only because site 354 (the Downtown marina) was bucketed here. The oil fields belong to Petrochem, SovOil and Night Corp. See §8.5. `[game-data]` `[wiki]` |
| `bls_border_crossing` | SoCal Border Checkpoint | **Lore-solid, data-empty.** Militech is the checkpoint's security provider; no Militech site or roster entry sits inside the sub-territory. `[wiki]` `[game-data]` |
| `bls_canyon_depot` | Badlands Canyon Depot | **Artifact.** No site, no roster, no marker. The area at its anchor is a `q114` set piece. See §8.8. `[game-data]` |

### 2.2 Sub-district presence

Counts are `dist/extract/areas.jsonl` rows whose `faction_counts` contains
`militech` (attributed per §2.3) and deduped `data/sites/sites.json` rows with
`default_faction_id == 21` **or** a Militech roster entry, collapsed within 25 m
and by facility identity.

| Sub-district | District | (a) Lore | (b) Panel | (c) areas (dominant) | (c) entries | Occupied sites |
| --- | --- | --- | --- | ---: | ---: | ---: |
| Badlands | Badlands | outpost, detention centre, border, patrols | Aldecaldos, Wraiths | **67 (66)** | **400** | 7 |
| Northside | Watson | All Foods raid (`q003`) + prologue roadblocks | Maelstrom | 7 (7) | 71 | 1 |
| LittleChina | Watson | prologue roadblocks only | Tyger Claws | 7 (7) | 47 | 1 |
| Kabuki | Watson | prologue roadblocks, *Concrete Cage Trap* raid | Tyger Claws | 12 (9) | 44 | 3 |
| Downtown | CityCenter | Gold Beach Marina, yachts | — (corp) | 5 (4) | 27 | 2 |
| CorpoPlaza | CityCenter | regional HQ | — (corp) | 9 (5) | 22 | 2 |
| Glen | Heywood | *Eye for an Eye* executive protection | Valentinos | 4 (2) | 16 | 2 |
| Coastview | Pacifica | Phantom Liberty set pieces only | Voodoo Boys, Animals | 6 (4) | 16 | 0 |
| CharterHill | Westbrook | execution scene, no facility | Tyger Claws, 6th Street | 2 (2) | 16 | 0 |
| JapanTown | Westbrook | netrunner parking lot raid | Tyger Claws | 5 (5) | 11 | 2 |
| VistaDelRey | Heywood | drones only | Valentinos | 4 (3) | 9 | 1 |
| Dogtown | Dogtown | Heavy Hearts contact, PL set pieces | Barghest | 4 (3) | 9 | 1 |
| NorthOaks | Westbrook | Arasaka estate mech drones | Tyger Claws | 2 (2) | 5 | 0 |
| Arroyo | SantoDomingo | Kendachi factory droids | 6th Street | 1 (1) | 4 | 1 |
| RanchoCoronado | SantoDomingo | drones only | 6th Street | 1 (1) | 4 | 0 |

**What the areas actually are** (this matters more than the counts):

- **Badlands (67 areas / 400 entries).** Four clusters: the `q114` canyon
  entrance and construction scenes (Militech canyon guards, drone swarms, gun
  trucks, a tank battle — a set piece, ~140 entries across the clusters); `cs_heavy_militech_patrol*`,
  `cs_bls_assaulted_conv_militech_attacker*`, `cs_militech_execution*`,
  `cs_handcuffed_wraiths_militech*` dynamic open-world events across the desert;
  the Sunshine Motel outpost (`ina_04_com_outpost_crew`, 13); and the detention
  centre (`ina_05_combat_com`, 14). `[game-data]`
- **Watson (26 areas).** Almost entirely `*_prolog_ow_roadblocks_*` — the Act-1
  Militech roadblocks in Northside, LittleChina and Kabuki — plus the `q003`
  All Foods Plant assault (23 + 13 entries). Presence, not ownership. `[game-data]`
- **Corpo Plaza (9 areas / 22).** The HQ scanner hustle `ma_cct_cpz_06_com` (4),
  the overpass drone patrol `ma_cct_cpz_10_com` (4), plus Militech team/drone
  cameos inside Arasaka set pieces (`q113_com_top_atrium_combat`,
  `sa_ep1_203_com_combat`). `[game-data]`
- **Downtown (5 areas / 27).** Gold Beach Marina (`dtn_05_com_combat` 12,
  `dtn_05_com_reinforcements` 4) and the West Pier scanner hustle (6). `[game-data]`
- **Dogtown / Coastview (10 areas / 25).** Phantom Liberty only:
  `q302_com_sec}2` (6), `q303_com_paradise_technical_floor_guards` (4 of 39),
  `q304_com_stadium_escape_drones_sewers*` (7), `q305_com_outer_bunker_control_room_robot` (1),
  and the Heavy Hearts contact (`sts_ep1_06_com_deal`, 1). No Militech facility
  in Dogtown; these are NUSA military assets in a story. `[game-data]`

### 2.3 Attribution caveat

`areas.jsonl.district_code` and `sites.json.sub_territory_id` are both unsafe
for this faction. Four failure modes were observed:

1. **Token first, always.** METHOD §3.3 puts the geocode token before the
   nearest-site fallback; running it in the other order put
   `lch_prolog_ow_roadblocks_com_A` (12 Militech entries at `(-1689, 945)`,
   clearly Little China) into **Downtown**, and `nid_prolog_*` into Kabuki.
   Token-first fixes all 26 Watson roadblock areas. `[game-data]`
2. **`q114` has no token and no site.** `q114_com_canyon_*` and
   `q114_com_construction_*` sit at `(196–255, 2340–2435)` and `(554, 2713)`,
   outside every city district bbox. The §3.3 nearest-sub-territory fallback
   assigns them to **NorthOaks** (22 areas / 112 entries — a phantom). A bbox
   test ("outside all city districts → Badlands") is required. `[game-data]`
3. **`sub_territory_id` on sites is a bucket, not a geocode.** Site 354 (Gold
   Beach Marina, Downtown) carries `sub_territory_id 86` = *North Sunrise Oil
   Fields*, whose centroid is 3.7 km away in the northern Badlands. Sub-territory
   86 is a catch-all holding six sites, four Downtown and two Little China. Two of the seed's ten
   Badlands sub-territories exist only because of this bucket (§8.4, §8.5).
   `[game-data]`
4. **`district_code` is still wrong for quest communities.**
   `q307_com_cabride`, `sa_ep1_2xx_com_*` and the PL `q30x` rows inherit their
   file's path token. All counts above are re-attributed by token, then by the
   nearest site's `source_path` (authoritative — it contains
   `<district>/<sub_district>/`), then by bbox.

---

## 3. Location catalog

Coordinates are world-space metres, `Z` up. "Interior?" means the game has a
distinct interior cell or volume. "Business?" is what the place earns or
provides, not a vendor inventory (the extract has no vendor data).

| # | Name | Type | District / sub-district | Interior? | Business? (what it earns) | Coordinates (x, y, z) | Coordinate source record | Linked communities / sites | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **Militech Offices** (Night City Regional HQ) | Corporate HQ / office tower | CityCenter / CorpoPlaza | Yes — lobby, showroom floors, offices; in-game only a small unfinished area behind barred elevators | Arms and vehicle contract sales, mercenary contracting, security contracts, executive offices | `-1308.475, -56.376, 2.150` | `data/sites/sites.json` site 11 `ma_cct_cpz_06` | `ma_cct_cpz_06_com` (4), CC `cc_cpz_militech_hq` (1.8 m) | `[game-data]` `[wiki]` |
| 2 | **Sunshine Motel** (Militech outpost) | Motel converted to military outpost | Badlands / Badlands | Yes — guard booth, office, workshop, garage, upper floor, roof, water tank | Weapons/tech depot; field testing of a mobile radar drone (P9D/2.161); patrol base | outpost `3637.395, -924.529, 120.505`; site anchor `3582.485, -916.844, 120.577` | `markers.jsonl` `Ina_04_mp_outpost`; site 342 `sts_bls_ina_04` | `ina_04_com_outpost_crew` (13); seeded `bls_militech_outpost`; CC `cc_bls_militech_outpost` (9.8 m) | `[game-data]` `[wiki]` |
| 3 | **Militech Detention Center** | Detention centre / border prison | Badlands / Badlands (Jackson Plains) | Yes — guard floors, barn, parking, gate house | Detention and deportation contracts for illegal border crossers; guard garrison | `-112.566, -5246.731, 87.160` | `data/sites/sites.json` site 343 `sts_bls_ina_05` | `ina_05_combat_com` (14), `ina_05_refugees_com` (4), `ina_05_bruce_com` (3) | `[game-data]` `[wiki]` |
| 4 | **SoCal Border Crossing** | Border checkpoint / customs | Badlands / Badlands (Southern Desert) | Yes — checkpoint office, hall, inspection room | Customs and immigration inspection; Militech is the security provider alongside the SoCal Border Patrol | `-2823.058, -5645.812, 101.404` | `markers.jsonl` `q000_nomad_mp_border_crossing_checkpoint` | `q305_com_border_crossing` (76, 6 Militech), `q000_ow_com` (5); CC `cc_bls_border_crossing` (211 m) | `[game-data]` `[wiki]` |
| 5 | **Gold Beach Marina** | Private marina (security contract) | CityCenter / Downtown | Yes — docks' security room, berths, patrol routes | Marina security contract (the "new security company" that closed the marina in 2077); elite clientele, celebrity yachts | `-2468.996, 47.517, 4.134` | `data/sites/sites.json` site 354 `sts_cct_dtn_05` | `dtn_05_com_combat` (12), `dtn_05_com_reinforcements` (4); `sq028_mp_wait_kerry_marina` 72 m; CC `cc_dtn_south_waterfront` (237.9 m, **Valentinos**) | `[game-data]` `[wiki]` |
| 6 | **Cynosure Facility** (Cynosure Site C) | Underground research facility | Pacifica / Dogtown (inferred) | Yes — underground bunkers, labs, storage | R&D: Project Cynosure, rogue-AI capture and containment | `TBD` | No marker, site or extract record; wiki only | Abandoned; no live garrison | `[wiki]` `[inferred]` |
| 7 | **Cynosure Site D** | Underground research facility / reloading station | Pacifica / Dogtown | Yes — underground tunnels below Longshore Stacks | R&D support for Site C; Militech Special Agent present in 2077 | `TBD` (access: elevator at Kress St, Longshore Stacks `-2319.8, -2544.0`) | No marker or site; longshore anchor from `data/landmarks.json` `lm_dt_longshore_stacks` | Dogtown tunnels | `[wiki]` `[inferred]` |
| 8 | Downtown West Pier | Pier / logistics front | CityCenter / Downtown | Unverified | Guarded pier with a netrunner intrusion point; likely freight/security | `-2164.836, 587.743, 7.250` | `data/sites/sites.json` site 40 `ma_cct_dtn_15` | `ma_cct_dtn_15_com` (6), netrunner workspot, drone; CC `cc_dtn_goldsmith_dock` (7.0 m) | `[game-data]` `[inferred]` |
| 9 | Corpo Plaza North Overpass | Drone patrol point | CityCenter / CorpoPlaza | No | Airborne surveillance of Corpo Plaza traffic | `-1289.845, 340.535, 9.581` | `data/sites/sites.json` site 12 `ma_cct_cpz_10` | `ma_cct_cpz_10_com` (4); CC `cc_cpz_ring_road_north` (7.7 m) | `[game-data]` `[inferred]` |

### 3.1 Interior sub-locations (the reason to capture a building)

The extractor keeps node names per site (`data/sites/{guards,triggers,spots,
patrols,doors}.json`), which is what makes these interiors legible without a
map.

**Sunshine Motel outpost** — site 342 `[game-data]`

| Sub-location | Node evidence | Note |
| --- | --- | --- |
| Guard booth (inside) | `#ina_04_ws_booth_guard_inside`, `#ina_04_ws_gate_guard_06_b` | Front gate line |
| Outpost office | `#ina_04_tr_in_office`, `#ina_04_tr_office_phone_talk`, `#ina_04_ws_officer_phone` | Officer's office with a phone scene |
| Workshop | `#ina_04_tr_inside_workshop`, `#ina_04_ws_orders_techie*` | Six technician patrol splines |
| Garage | `#ina_04_tr_exit_garage_objective`, `#ina_04_ws_garage_techie_01..004`, `#ina_04_dvc_shutters` | Vehicles and the radar van |
| Radar van | `#ina_04_ws_radar_van` | The stolen-prototype objective |
| Courtyard / outpost yard | `#ina_04_tr_in_courtyard`, `#loc_sts_bla_ina_04_RMA_outpost` | Crowd fighters, forklift, containers |
| Upper floor | `#loc_sts_bla_ina_04_RMA_upper` | — |
| Roof | `#loc_sts_bla_ina_04_RMA_roof` | Overwatch |
| Water tank | `#loc_sts_bla_ina_04_RMA_watertank` | — |
| Indoor guard volume | `#loc_sts_bla_ina_04_RMA_indoor_001` | Proves an interior cell despite `is_interior=0` |

**Militech Detention Center** — site 343 `[game-data]`

| Sub-location | Node evidence | Note |
| --- | --- | --- |
| Main gate | `#ina_05_main_gate`, `#ina_05_tr_car_gate` | Vehicle control point |
| Refugee gate | `#ina_05_gate_refugee`, `#ina_05_tr_rma_refugees` | 22 refugee workspots |
| Parking gate / lot | `#ina_05_gate_parking`, `#ina_05_tr_parking`, `#ina_05_parking_door` | Detainee transport |
| Barn | `#ina_101_tr_barn`, `#ina_05_tr_barn` | Detention hall |
| Cell floor 1 | `#sts_bls_ina_05_RMA_floor_1` | — |
| Cell floor 0 | `#sts_bls_ina_05_RMA_floor_}0` | — |
| Outside / yard | `#sts_bls_ina_05_RMA_outside`, `_RMA_patrol_left`, `_RMA_patrol_right` | Patrol flanks |
| Rear building (variant site 348) | `#ina_101_tr_enter`, `#ina_101_tr_target`, `#ina_05_gates_00x` | Quest variant, 32 m away |

**Gold Beach Marina** — site 354 `[game-data]` `[wiki]`

| Sub-location | Node evidence | Note |
| --- | --- | --- |
| Docks' security room | `#dtn_05_restrictMovementArea`, `#dtn_05_ws_guard_001..012` (24 workspots) | The gig's objective room; the marina's new security systems |
| Berths / quay | `#dtn_05_spl_patrol_guard_001..011` | 8 patrol splines over the docks |
| Reinforcement entry | `#dtn_05_ws_reinforcments_001..004` | Security response |
| Moored yachts | `sq028_mp_wait_kerry_marina` 68 m away | Celebrity yachts, incl. the *GEIshhhhA* `[wiki]` |

**Militech Offices** — no site interior records `[wiki]`

The wiki gives the building a lobby, a showroom floor, an open-air cafeteria and
a small military-technology museum, and notes that in 2077 the street-level
roundabout has **barred-off elevators that lead to an unfinished small area** of
the building. So the building is a real interior in lore, a stub in the game.
Treat the capture volume as the plaza concourse, not the tower. `[wiki]`

### 3.2 How the name→coordinate links were proven

- **Militech Offices** — the seed's `cpz_militech_hq` sub-territory, landmark
  (`lm_cpz_militech_hq` "Militech HQ Concourse") and CC `cc_cpz_militech_hq` all
  sit at `(-1307.3, -55.0, 7.0)`; site 11 `ma_cct_cpz_06` anchors at
  `(-1308.475, -56.376, 2.150)`, 1.8 m away, `default_faction_id 21`, with 4
  Militech rangers, and its `source_path` is
  `base/open_world/minor_activities/city_center/corpo_plaza/loc_ma_cct_cpz_06/…`
  — Corpo Plaza, confirmed independently of the seed. The raw sector contains
  `c_city_center/corpo_plaza/loc_ma_cct_cpz_06_prefabAZTRELQ`. The wiki infobox
  gives `type = Regional HQ`, `owner = Militech`, `district = City Center`,
  `sub_district = Corporate Center`, `location = Corporate Plaza`, and says the
  building fronts Arasaka Tower across the Plaza and is reached by a bridge from
  Memorial Park. `[game-data]` `[wiki]`
- **Sunshine Motel** — `Ina_04_mp_outpost` (`3637.395, -924.529, 120.505`) sits
  9.9 m from the seeded `bls_militech_outpost` anchor (`3646.4, -920.5, 120.5`);
  site 342 `sts_bls_ina_04` anchors at `(3582.485, -916.844, 120.577)`, 64 m
  further west, with `default_faction_id 21` and 19 units. Its guard-area names
  (`RMA_outpost`, `RMA_roof`, `RMA_watertank`, `RMA_indoor_001`) and workspots
  (`ws_radar_van`, `ws_forklift`, `ws_officer_phone`) match the wiki's
  *Gig: Radar Love* description of a motel "converted into a heavily guarded
  outpost" testing a mobile radar. The wiki infobox gives `owner = Block Clan
  (formerly) / Militech`, `type = Defunct motel / Military facility`,
  `subregion = Rocky Ridge Plains`, `street = Interstate 9`. The seed name
  "Red Peaks Militech Outpost" uses the adjacent hill region. `[game-data]` `[wiki]`
- **Militech Detention Center** — site 343 `sts_bls_ina_05`
  (`-112.566, -5246.731, 87.160`) carries 18 Militech units (security, rangers,
  snipers, a tech grenadier, an officer, a Wyvern drone), 22 `refugee` workspots,
  `Bruce`/`Archibald` actor spots, three gate doors and a barn trigger — the exact
  cast of *Gig: Goodbye, Night City*. The wiki infobox gives `owner = Militech`,
  `type = Detention center`, `subregion = Jackson Plains`, `street = Coachwhip
  Ln.`, "used to hold illegal border crossers". `[game-data]` `[wiki]`
- **SoCal Border Crossing** — `q000_nomad_mp_border_crossing_checkpoint`
  (`-2823.058, -5645.812, 101.404`), with `…_border_office`,
  `…_border_office_hall` and `q000_sm_nomad_05_border_crossing` within 30 m.
  The wiki infobox gives `type = Border checkpoint`,
  `security_provider = SoCal Border Patrol / Militech`, `street = Highway 101`.
  The seeded `bls_border_crossing` compound anchor is 233 m north of the actual
  crossing (§8.9). `[game-data]` `[wiki]`
- **Gold Beach Marina** — site 354 `sts_cct_dtn_05` (`-2468.996, 47.517, 4.134`)
  is the only Militech-default site in Downtown with 16 units (security, SMG,
  shotgun, officer), 24 guard workspots, 8 dock patrols and a
  `restrictMovementArea`. Raw sector: `c_city_center/downtown/loc_sts_cct_dtn_05_luxury_yacht`
  — a yacht, in Downtown. The wiki infobox for *Gold Beach Marina* gives
  `type = Private marina`, `district = City Center`, `sub_district = Downtown`,
  `street = Gold Beach`; the gig *The Frolics of Councilwoman Cole* names the
  location "Marina, Cannery Row" and lists `enemies = Militech`, and the wiki
  says the marina "had contracted a new security company, which installed new
  security systems". `sq028_mp_wait_kerry_marina` (`-2462.745, -20.012, 3.536`)
  is 68 m away, confirming this is the marina with the celebrity yachts.
  `[game-data]` `[wiki]`
- **Cynosure** — no marker, site or roster record anywhere in the extract
  (`grep -i cynosure` over `markers.jsonl` and the raw sectors: no hits). The
  wiki gives Site C as `owner = Militech (formerly)`, `type = Research facility`,
  `district = Pacifica`, `location = Underground`; and Site D as
  `sub_district = Dogtown`, `location = Beneath Longshore Stacks`, accessed via
  the Kress Street elevator. Coordinates stay `TBD`. `[wiki]` `[inferred]`
- **Downtown West Pier / Corpo Plaza North Overpass** — seed display names over
  `ma_` scanner-hustle sites 40 and 12, both `default_faction_id 21`, 6 and 4
  Militech units. No marker or wiki page names either. `[game-data]` `[inferred]`

### 3.3 Militech-occupied generic sites (the filler pool)

Sites with Militech-tagged units that are **not** a named catalog point. Their
`suitability` tags say what gameplay a site can host; they are not lore.

| Site | Sub-district | Units | Suitability tags | Coordinates | Note |
| --- | --- | ---: | --- | --- | --- |
| `sts_wat_kab_01` | Kabuki | 6 | raid_target 88, officer_site 85, stealth_entry 60 | `-1186.713, 1760.468, 23.353` | *Concrete Cage Trap*: Militech raid on a Kabuki housing block hunting Tiny Mike. Filler |
| `sts_hey_gle_01` | Glen | 8 | raid_target 90, officer_site 80, stealth_entry 60 | `-1680.965, -979.899, 10.790` | *Eye for an Eye*: Tucker Albach's condo, 8 Militech guards. Executive protection, not a Militech facility. Filler |
| `sts_bls_ina_07` | Badlands | 3 | raid_target 80, vehicle_bay 65 | `4800.558, -1502.990, 138.058` | *Dancing on a Minefield*: Militech drone/car encounter at the minefield. Filler |
| `ma_bls_ina_04` | Badlands | 6 | raid_target 90, rooftop_access 80 | `4334.851, -1276.551, 134.970` | Badlands patrol/convoy scene (rangers, enforcer, recon sniper, Octant drone). Filler |
| `ma_bls_ina_03` | Badlands | 3 | raid_target 85, rooftop_access 75 | `4481.470, -756.345, 150.775` | Badlands patrol. Filler |
| `ma_bls_ina_05` | Badlands | 6 | raid_target 80 | `2295.803, 608.376, 101.762` | Badlands patrol inside Wraith turf. Filler |
| `ma_hey_gle_13` | Glen | 5 | raid_target 85, officer_site 60 | `-1602.629, -1119.905, 9.120` | Glen scanner hustle (Elizabeth Roider, an MG gunner, rangers). Filler |
| `ma_wat_kab_08` | Kabuki | 3 | raid_target 90, club 70 | `-1093.120, 1532.005, -0.090` | Unnamed Kabuki arena scene with a cyberpsycho, two reused Militech rangers and a drone. No place identity found. Filler |
| `ma_wat_kab_15` | Kabuki | 1 | raid_target 75 | `-1106.880, 1399.439, 19.890` | A single `kab_militech_drone_wyvern_hard` — brand hardware, not troops. Filler |
| `sts_wbr_jpn_09` | JapanTown | 4 | raid_target 70, vehicle_bay 65 | `-392.925, 1404.522, 41.616` | *…netrunner parking lot*; trigger `jpn_09_tr_netrunner`, 4 enemies. Filler |
| `ma_wbr_jpn_09` | JapanTown | 1 | rooftop_access 70 | `-489.970, 286.741, 29.850` | Single Griffin drone. Filler |
| `ma_wat_nid_16` | Northside | 3 | raid_target 70, rooftop_access 65 | `-978.472, 2803.044, 30.054` | Three Wyvern drones. Filler |
| `ma_wat_lch_103` | LittleChina | 2 | raid_target 70 | `-1954.306, 1097.760, 12.099` | Two easy Wyvern drones. Filler |
| `ma_hey_rey_109` | VistaDelRey | 1 | raid_target 60 | `-945.060, -344.012, 14.855` | One drone. Filler |
| `sts_std_arr_03` | Arroyo | 4 | raid_target 85, officer_site 60 | `-598.610, -1713.347, 8.270` | *Race to the Top* at the Kendachi Factory; 4 `security_droids`. The gig's enemies are independent guards and robots, so the droid tag is a supplier label, not a Militech garrison. Filler |
| `ma_cct_dtn_15` | Downtown | 6 | raid_target 80, netrunner 60 | `-2164.836, 587.743, 7.250` | Named in the seed as "Downtown West Pier"; netrunner intrusion + tech + soldiers + drone. Filler (ranked #8 as a seed-named holding) |
| `ma_cct_cpz_10` | CorpoPlaza | 4 | raid_target 75, rooftop_access 70 | `-1289.845, 340.535, 9.581` | Drone patrol over the North Overpass. Filler (ranked #9) |
| `sts_ep1_06` | Dogtown | 2 | club 80, officer_site 75 | `-1606.430, -2341.452, 43.070` | *Heaviest of Hearts* at the Heavy Hearts club: one Militech business contact plus a ranger. Filler |

Excluded from both tiers (see §8): site 344 `sts_bls_ina_06` (a Wraith outpost
that inherits the outpost squad through a shared community hash) and site 172
`ma_wat_kab_02` (an NCPD-default cyberpsycho whose character record is tagged
Militech).

---

## 4. Economic structure

### 4.1 Revenue streams → catalog locations

| Revenue stream | Code(s) | Catalog locations that produce it | Evidence / notes |
| --- | --- | --- | --- |
| Contract security for governments and corporations | `security_services` | Militech Offices (contract desk), SoCal Border Crossing, Militech Detention Center, Gold Beach Marina | Wiki: regional offices "handle all local bulk arms contracts, mercenary contracting, distribution"; Militech contracts police services to US cities; the marina hired a new security company in 2077. `[wiki]` `[game-data]` |
| Border enforcement and detention | `security_services` | SoCal Border Crossing, Militech Detention Center | Wiki: the checkpoint's `security_provider` is SoCal Border Patrol + Militech; the detention centre held "illegal border crossers". `[wiki]` |
| Executive protection | `security_services` | Tucker Albach's condo (filler), Heavy Hearts contact (filler) | Wiki: 8 Militech guards protect a corporate executive in the Glen. `[wiki]` `[game-data]` |
| Arms sales and contracting | `arms` | Militech Offices, Sunshine Motel outpost | Wiki: arms manufacturing, military vehicle production, contract sales; the outpost holds weapons and tech. `[wiki]` |
| Field testing / prototypes | `rnd` | Sunshine Motel outpost (mobile radar P9D/2.161) | Wiki: the outpost tested "a new kind of mobile radar drone"; Dakota wants it to make border crossings harder. `[wiki]` |
| Black-site research (rogue AI) | `rnd` | Cynosure Facility, Cynosure Site D | Wiki: Project Cynosure captured and contained rogue AIs; Militech's answer to Soulkiller. `[wiki]` |
| Retail (showroom) | `retail` | Militech Offices | Wiki: 2020-era regional offices had a showroom selling weapons, accessories and vehicles; the 2077 office is described as a regional HQ. No vendor record exists in the extract. `[wiki]` |
| Property / facility ownership | `real_estate` | Militech Offices, Gold Beach Marina, Cynosure sites | The marina is a private facility with its own security detail; the HQ is a Corpo Plaza tower. `[wiki]` `[inferred]` |
| Manufacture (NC plant) | `manufacturing` | — no verified location | Wiki: a "Cyberware/Computer/Accessory plant in Night City" exists in 2020-era lore. No 2077 game record found. `[wiki]` `[lore]` |
| Patrol, convoy escort, executions | `protection` (closest fit) | Badlands `cs_*` dynamic events; prologue roadblocks | The Badlands open-world events are Militech patrols, convoy attacks and prisoner handovers. "Protection" is the nearest code; the vocabulary has no `patrol` or `policing` term. `[game-data]` `[inferred]` |

### 4.2 Suppliers, customers, rivals

| Role | Party | Detail |
| --- | --- | --- |
| Owner / regulator | NUSA government | Nationalised in 2023; over 60% of contracts come from the NUSA; board members hold Ministry of Defense posts; former CEO Rosalind Myers became president. `[wiki]` |
| Customer | NCPD, US police departments, NUSA military | Militech contracts police services and supplies the federal army; "worked closely with American military and police agencies for decades". `[wiki]` |
| Customer | Corporations and wealthy individuals | Showrooms and regional offices sell to corporates and high-end solos; executives get up to 50% off Militech weapons. `[wiki]` |
| Subsidiary | Nova Arms | Listed subsidiary. `[wiki]` |
| Historic partner | Lazarus Group | Closest corporate ally in the 2010s; also provided security at the Night Corp Solar Farm in 2045. `[wiki]` |
| Supplier (AV platforms) | Zetatech | Zetatech Atlus/Surveyor airframes are the AVs Militech arms and retrofits; the 2020 showroom displayed AVX Viper assault aerodynes. `[wiki]` `[inferred]` |
| Rival | Arasaka | The primary rival in arms and corporate security, and the literal neighbour: Arasaka Tower faces the Militech Offices across Corpo Plaza. `[wiki]` |
| Rival | Kang Tao | The Kang Tao North Tower is the third Corpo Plaza megacorp (seeded sub-territory `cpz_kang_tao_sector`). `[wiki]` `[game-data]` |
| Rival (lore) | Sternmeyer Waffenfabrik, Federated Arms, Schumann-Stein, IEC | Named arms-industry and conglomerate rivals in the 2020 sourcebooks. `[wiki]` |
| Landlord / counterparty | Night Corp, PacCon Electric | Night Corp owns the Jackson Plains solar farm the seed credits to Militech; PacCon manages it. `[wiki]` |
| Local hostile | Wraiths, Aldecaldos | The Wraiths hold the Rocky Ridge / Sunset Motel area and attack Militech convoys; the Aldecaldos want the radar prototype so nomads can cross the border unseen. `[wiki]` `[game-data]` |

---

## 5. Headquarters recommendation

### Primary HQ: **Militech Offices — Corpo Plaza**

Coordinates: `(-1308.475, -56.376, 2.150)` `[game-data]`
`data/sites/sites.json` site 11 `ma_cct_cpz_06`.

Rationale:

1. **It is the canon regional HQ.** The wiki gives it `type = Regional HQ`,
   `owner = Militech`, `district = City Center`, `location = Corporate Plaza`,
   and the Militech article says regional offices contain "the headquarters for
   the local ranking Militech Officer", who runs local contracts and black ops.
   `[wiki]`
2. **A management seat, not a venue.** Lobby, showroom floors, offices,
   conference rooms and a small military-technology museum: exactly the rooms an
   org-management layer wants to assign. `[wiki]`
3. **It maps 1:1 to the economic core.** Arms contract sales, mercenary
   contracting and distribution all run through the regional office, so owning
   the HQ and owning the economy are the same action. `[wiki]` `[inferred]`
4. **It is already a clean control point.** Site 11 has
   `default_faction_id = 21`, `initial_owner_faction_id = 21`,
   `control_center_id = 77`, 4 Militech rangers, and the seeded CC
   `cc_cpz_militech_hq` is **1.8 m** away. No new map plumbing. `[game-data]`
5. **It sits in the corp district the seed already treats as Militech's**
   (`cpz_militech_hq`, `cpz_ring_road_north`), next door to Arasaka — the
   rivalry the mod wants to express. `[game-data]` `[wiki]`

Trade-off: the in-game building is a **stub**. The wiki notes only a small
unfinished area behind barred elevators above the street-level roundabout, and
the extract has no interior site, no doors and no guard volumes for it. So the
capture volume must be the plaza concourse around site 11, and the tower's
"rooms" are narrative upgrades rather than geometry. If that is unacceptable,
use the Sunshine Motel outpost (below) as the functional seat and keep Corpo
Plaza as the prestige flag. `[wiki]` `[game-data]`

### Alternate 1: **Sunshine Motel outpost** — the Badlands

Coordinates: `(3637.395, -924.529, 120.505)` `[game-data]`
`markers.jsonl` `Ina_04_mp_outpost`.

The only Militech facility with a complete gameplay set *and* a co-located
control centre: 19 units, 7 guard areas (outpost, outpost interior,
reinforcements, upper, roof, water tank, indoor), 9 patrol splines, 6 doors, 55
workspots (booth, office, workshop, garage, radar van), and
`cc_bls_militech_outpost` 9.8 m away. A converted motel reads as a believable
field command post, which is how the wiki describes it. It loses on geography
(remote eastern Badlands, `z≈120`), on prestige, and because the mod's HQ should
be visible from the city. `[game-data]` `[wiki]`

### Alternate 2: **Gold Beach Marina** — Downtown

Coordinates: `(-2468.996, 47.517, 4.134)` `[game-data]`
`data/sites/sites.json` site 354 `sts_cct_dtn_05`.

The most *commercially* interesting seat: Downtown waterfront, 16 Militech
security units, a security room, 8 dock patrols, and an elite clientele of
yachts. It is also the cleanest demonstration of Militech's business model —
they are not the landlord, they are the contractor — which makes it a good
"corporate client" HQ if the mod's Militech org is a security-services company
rather than a weapons house. It loses because the marina is privately owned (the
wiki infobox has no `owner`), the nearest CC is Valentinos-owned, and a marina is
a contract site, not a headquarters. `[game-data]` `[wiki]`

### Overruled / downgraded suggestions

- **Militech Detention Center as HQ** — a walled prison in the Jackson Plains is
  a garrison, not a seat; keep it as a high-value capture point and the test
  point. `[wiki]`
- **Cynosure Site D as HQ** — lore-perfect (a secret underground Militech city
  under Dogtown) but impossible to seed today: no marker, no site, no interior
  record, coordinate `TBD`. Keep it as a late-game unlock idea. `[wiki]`
- **The Badlands "Canyon Depot" as HQ** — the seed anchor overlays a `q114`
  ending set piece with Militech canyon guards and drones. It is not a facility
  and has no site record. Rejected. `[game-data]`
- **The "North Sunrise Oil Fields" / "Jackson Plains Solar Arrays" as HQ** — both
  are seed artifacts of `sub_territory_id` bucketing, and both are owned by
  other corporations in lore (Petrochem/SovOil/Night Corp; Night Corp/PacCon).
  Rejected; see §8.4 and §8.5. `[wiki]`
- **The planned Pacifica HQ** — in the 2060s Militech planned a three-tower
  Pacifica headquarters shaped like its logo; the wiki says it never got past
  planning. Do not seed it. `[wiki]`

---

## 6. Priority list of control points

Ranked by how well each place serves as a capturable Militech control point.
"CC" = nearest entry in `data/control_centers.json` (active or not); distance is
horizontal metres. Relevance reflects lore + revenue + record richness, not raw
unit count.

| Rank | Control point | Rel. (1–5) | District / sub-district | Coordinates | Existing CC overlap | Why |
| ---: | --- | :---: | --- | --- | --- | --- |
| 1 | **Militech Offices** | 5 | CityCenter / CorpoPlaza | `-1308.475, -56.376, 2.150` | `cc_cpz_militech_hq`, 1.8 m (Militech) | Canon regional HQ; contract sales, mercenary contracting, command; faces Arasaka Tower |
| 2 | **Sunshine Motel outpost** | 5 | Badlands / Badlands | `3637.395, -924.529, 120.505` | `cc_bls_militech_outpost`, 9.8 m (Militech) | 19 units; 7 guard areas incl. `RMA_indoor_001`; 9 patrols; 6 doors; radar-prototype R&D |
| 3 | **Gold Beach Marina** | 4 | CityCenter / Downtown | `-2468.996, 47.517, 4.134` | `cc_dtn_south_waterfront`, 237.9 m (**Valentinos**) | 16 security units; docks' security room; 8 patrol splines; elite waterfront contract |
| 4 | **Militech Detention Center** | 4 | Badlands / Badlands | `-112.566, -5246.731, 87.160` | `cc_bls_solar_station`, 384.9 m (Militech) | Wiki-named Militech-owned prison; 18 units; 8 guard areas; 4 gates; 22 refugee workspots |
| 5 | **SoCal Border Crossing** | 4 | Badlands / Badlands | `-2823.058, -5645.812, 101.404` | `cc_bls_border_crossing`, 211.0 m (Militech) | Militech is the security provider at the NUSA border; customs revenue; office interior |
| 6 | **Cynosure Site D** | 3 | Pacifica / Dogtown | `TBD` | none | Militech black site under Longshore Stacks; rogue-AI research; no coordinate |
| 7 | **Cynosure Facility (Site C)** | 3 | Pacifica / Dogtown | `TBD` | none | The main Project Cynosure site; "cyberspace equivalent of a nuke"; no coordinate, no records |
| 8 | **Downtown West Pier** | 2 | CityCenter / Downtown | `-2164.836, 587.743, 7.250` | `cc_dtn_goldsmith_dock`, 7.0 m (Militech) | Seed-named holding; 6 units, netrunner intrusion point, drone; no wiki identity |
| 9 | **Corpo Plaza North Overpass** | 2 | CityCenter / CorpoPlaza | `-1289.845, 340.535, 9.581` | `cc_cpz_ring_road_north`, 7.7 m (Militech) | Seed-named holding; drone surveillance only; cheap rename of an existing CC |

### Test control point for the first in-game test: **Militech Detention Center**

Site 343 `sts_bls_ina_05`, coordinates `(-112.566, -5246.731, 87.160)`,
`[game-data]` `data/sites/sites.json`.

Why this and not the HQ:

- **Clean, unambiguous ownership.** `default_faction_id = 21` and
  `initial_owner_faction_id = 21`, and the place is independently named as
  Militech-owned by the wiki. Eviction has no ambiguity. `[game-data]` `[wiki]`
- **The richest capture-relevant record set of any Militech site.** 8 guard
  areas (`RMA_floor_1`, `RMA_floor_}0`, `RMA_outside`, `RMA_patrol_left`,
  `RMA_patrol_right`, `RMA_reinforcements`, `ina_05_tr_rma_refugees`,
  `cs_goons_shooting_ga`), 7 patrol splines, 3 gate doors, and 72
  workspots (22 refugees, 28 guard workspots, 4 reinforcements, Bruce and
  Archibald actor spots). Every hook a capture/defence prototype needs is
  present and named. `[game-data]`
- **A fenced compound with a single gate line.** The main gate, car gate
  and refugee gate (`#ina_05_main_gate`, `#ina_05_tr_car_gate`,
  `#ina_05_gate_refugee`) give a natural capture volume and a natural
  reinforcement lane — easier to validate than a street or a tower. `[game-data]`
- **Not the HQ and not an alternate HQ.** The first test exercises capture on a
  non-seat, per METHOD §3.8. `[game-data]`

Trade-off: it is a **high-security prison** and the site of *Gig: Goodbye, Night
City*, so it may be quest-gated; it is also 385 m from its nearest CC, so the
seed must relocate `cc_bls_solar_station` onto it (§3.8 says that is fine, but
it is not free). **Fallback if the prison is gated: the Sunshine Motel outpost**
(`Ina_04_mp_outpost`, 9.8 m from `cc_bls_militech_outpost`), which has an indoor
guard volume and needs no CC move. Second fallback: the Gold Beach Marina
security room, which is an enclosed interior in a city district. `[game-data]`

---

## 7. Per-sub-district counts

This is the number to feed yield balancing. It counts **distinct named places**
Militech owns, runs, protects or habitually occupies — not set pieces, not
drone-only scan sites and not generic occupied blocks. `Filler` is the deduped
occupied-site count minus any site already counted as a named place (METHOD §8).

| Sub-district | Named lore-relevant places | Which ones | Occupied sites (deduped) | Filler | Noteworthy interiors |
| --- | ---: | --- | ---: | ---: | --- |
| Badlands | **3** | Sunshine Motel outpost, Militech Detention Center, SoCal Border Crossing | 7 | 4 | Outpost booth/office/workshop/garage/roof; detention gate line, barn, floors |
| CorpoPlaza | **1** | Militech Offices | 2 | 1 | HQ lobby/showroom (lore; stub in game) |
| Downtown | **1** | Gold Beach Marina | 2 | 1 | Marina security room, berths |
| Dogtown | **2** | Cynosure Facility (Site C), Cynosure Site D | 1 | 1 | Underground bunkers, labs (no coordinates) |
| Glen | 0 | *Eye for an Eye* executive protection only | 2 | 2 | Tucker Albach's condo |
| Kabuki | 0 | *Concrete Cage Trap* raid and an arena scene only | 3 | 3 | None Militech-owned |
| JapanTown | 0 | netrunner parking lot and a drone only | 2 | 2 | None |
| Northside | 0 | Prologue roadblocks and one drone site | 1 | 1 | None |
| LittleChina | 0 | Prologue roadblocks and drones | 1 | 1 | None |
| VistaDelRey | 0 | A single drone | 1 | 1 | None |
| Arroyo | 0 | Kendachi factory droids (supplier label) | 1 | 1 | None |
| **Total** | **7** | | **23** | **18** | |

Reconciliation (`named + filler = 25`):

- 23 deduped occupied sites − 5 site-backed named sites (`ma_cct_cpz_06`,
  `sts_bls_ina_04`, `sts_bls_ina_05`, `sts_bls_ina_101`, `sts_cct_dtn_05`).
- 7 named places = 4 site-backed places (Offices, Sunshine Motel, Detention
  Center, Gold Beach Marina) + 3 named places with no Militech site (SoCal
  Border Crossing, Cynosure C, Cynosure D).
- `23 + 3 − 1 = 25`: the −1 is `sts_bls_ina_101` (site 348), a quest variant of
  the Detention Center 32 m away, which is excluded from filler but does not add
  a second named place.
- Sites excluded from both tiers and why: `sts_bls_ina_06` (Wraith outpost
  inheriting the outpost squad through a shared community hash, §8.1) and
  `ma_wat_kab_02` (an NCPD cyberpsycho site whose record is Militech-tagged).

Area-only presence that is **not** counted anywhere above (no site, no named
place): the `q114` canyon and construction set pieces, the Watson prologue
roadblocks (26 areas), the Charter Hill execution scene (12 Militech entries at
`(345, -504)`), `mq056`/`sq024` street races with one Militech driver each, and
the `<50` Phantom Liberty set pieces in Dogtown, Coastview and West Wind. These
should be contested turf or event spawns, never owned economy.

Interpretation for yield: the **Badlands** carries three named places and 400
entries and should hold the faction's high-yield military economy. **Corpo
Plaza** has one named place but it is the HQ, so it should get the org-management
multiplier. **Downtown** has one named place that is a *contract*, not an asset,
and should yield less than its footprint suggests. The Watson and Heywood
sub-districts are presence-only — Militech raiding someone else's turf — and
should not be owned territory at all. `[inferred]`

---

## 8. Gaps and uncertainties

1. **`rosters.json` double-counts units across sites.** Community hash
   `550901676395883698` (the Sunshine Motel outpost squad, 15 entries at
   `(3646, -920)`) is attached to sites **342, 344 and 345**. The naive join
   therefore credits 25 sites / 159 units; deduping by
   `(community_hash, character_record_id)` gives **24 sites / 133 units**; one of
   those (site 172) is an NCPD cyberpsycho whose record is Militech-tagged,
   leaving **23 occupied sites**, and site 344 (a Wraith outpost, *Gig: No Fixers*) with **zero**
   Militech units. METHOD §1.1 item 15 says to group spawn points by
   `sub_territory_id`; it must also say to dedupe roster units by community hash
   before counting. This is the single biggest numeric error for this faction.
2. **Militech-brand hardware is tagged as Militech.** Wyvern, Griffin, Octant
   and Centaur drones and `security_droids` carry `faction_id 21`. Six of the 18
   filler sites have **no human Militech NPC at all** — only drones or droids
   (sites 12, 229, 204, 190, 268, 69). `q113_com_arasaka_estate_mech_drones`
   even tags Arasaka's estate mechs as Militech. METHOD should add a corp
   equivalent of "presence ≠ ownership": *drone presence ≠ garrison*. For
   Militech specifically, treat drone-only sites as relevance 1–2.
3. **Corp HQs are not `sites.json` rows, again.** The Militech Offices have no
   interior site, no doors, no guard volumes — only a scanner-hustle site
   (`ma_cct_cpz_06`) on the concourse. §3.1's candidate query would have returned
   nothing named. The batch-1 note (§1.1 item 3) is right but undersells it: for
   *this* corp the HQ is a **decorative building**, and `is_interior` is
   meaningless for it.
4. **"Jackson Plains Solar Arrays" is a seed artifact.** Sub-territory 89
   (`bls_solar_station`, owner 21) contains four sites, two of them the
   detention-centre sites. The arrays themselves are the **Night Corp Solar
   Farm** (owner Night Corp, manager PacCon Electric) and are described as
   inactive in 2077. Do not seed the solar farm as Militech. `[wiki]`
5. **"North Sunrise Oil Fields" is a seed artifact.** Sub-territory 86
   (`bls_north_oil_fields`, owner 21) contains six sites, four of them
   **Downtown** and two **Little China** — including `sts_cct_dtn_05` (Gold Beach
   Marina) — and its
   centroid is in the northern Badlands. The oil fields are owned by Petrochem,
   SovOil and Night Corp. Do not seed them as Militech. `[wiki]`
6. **"Gold Beach Marina" is placed in the wrong sub-district.** The seed puts
   `hil_gold_beach` at `(344.5, -504.4)` in **CharterHill**; the wiki puts the
   marina in **Downtown, City Center**, and the actual site is 2.9 km away at
   `(-2469.0, 47.5)`. The Charter Hill location is a back-alley area with a
   Militech execution scene (`la_sm_execution_01`), not a marina. This is a
   concrete instance of METHOD §1.1 item 13 ("seed display names can be wrong")
   that no batch-1 agent hit at this distance. `[game-data]` `[wiki]`
7. **`dtn_skyline_west` ("Skyline & Salinas Plaza") has no Militech presence.**
   The seeded sub-territory is Militech-owned, but the only site inside it is
   `ma_cct_dtn_01`, `default_faction_id 6` (Animals), and no Militech roster
   entry or area falls there. Either the owner is stale or the site join is
   wrong. Not seeded as a Militech point. `[game-data]`
8. **"Badlands Canyon Depot" is a set piece, not a depot.** Sub-territory 87
   contains no site and no roster. The area at its anchor,
   `q114_com_canyon_entrance_drones` (29 Militech) and `…_cars` (23 Militech), is
   the `q114` mission's canyon entrance — the raw sector contains
   `q114_militech_canyon_guard_rifle`, `q114_militech_large_drone` and
   `q114_militech_medium_drone`. Militech canyon guards and drones exist there
   in a story, not as a garrison. Excluded from both tiers. `[game-data]`
9. **Seed compound anchors can be >200 m off, not ~110 m.** The SoCal Border
   Crossing markers sit at `(-2823.1, -5645.8)`; the seeded
   `bls_border_crossing` anchor is at `(-2810.0, -5435.2)`, **233 m** north.
   METHOD §1.1 item 7 says site anchors can be ~110 m off; for Badlands
   compounds the error is larger. Use the marker.
10. **`sub_territory_id` is not a geocode.** Six sites are bucketed into a
    Badlands sub-territory 3.7 km away (§8.5), and the detention centre drags its
    own Badlands sub-territory's owner with it (§8.4). Any per-sub-district count
    built by joining `sites.sub_territory_id` to `sub_territories` will be wrong
    for this faction; use the site's `source_path`, which contains the real
    `<district>/<sub_district>/` pair. This is the cheapest reliable geocode in
    the extract and METHOD does not mention it.
11. **`sites.json` `source_path` is the best sub-district key, and it is
    undocumented.** `base/open_world/.../city_center/downtown/loc_sts_cct_dtn_05_…`
    names both district and sub-district. It resolved every ambiguous site in
    this doc (the marina, the detention centre, Corpo Plaza) without a wiki
    lookup. Add it to METHOD §2.1 and §3.3.
12. **`q114` inflates the Badlands and NorthOaks.** The canyon entrance, canyon
    bridge and construction clusters (~140 Militech entries) are the Aldecaldos
    ending's staging area and tank battle. They are outside every city bbox, so
    the §3.3 nearest-sub-territory fallback assigns them to **NorthOaks** — a
    false 22-area cluster. A bbox test is required.
13. **§10.2's validator vocabulary is a subset of §7's.** The `VOCAB` set in
    §10.2 omits `logistics`, `finance`, `hospitality`, `education`, `netrunning`,
    `information`, `mercenary` and `funeral`, although §7 defines them. Any doc
    that uses them fails its own validator. This one needed `netrunning`
    (Cynosure) and `hospitality` (the marina) and used `rnd` and `real_estate`
    instead. Fix §10.2 to import the §7 table rather than re-listing it.
    *Resolved 2026-11-25: METHOD.md's validator now includes every §7 code, and the JSON block carries the intended codes.*
14. **There is no `patrol`/`policing`/`customs` revenue code.** Militech's
    largest Badlands activity is patrol, convoy escort and border enforcement.
    `security_services` covers the contracts and `protection` is the closest fit
    for open-world patrol presence, but neither says "customs revenue". Add
    `logistics` or `customs`, or state that border fees are out of scope.
15. **Cynosure is unmappable from the extract.** No marker, site, community or
    raw-sector string contains "cynosure" (`grep -i cynosure` over
    `markers.jsonl` and the three `always_loaded_*` sectors: zero hits). Site C's
    sub-district is not stated by the wiki either (it says only "underground,
    Pacifica"). I placed both in **Dogtown** by inference from Site D's explicit
    Dogtown/Longshore Stacks location; this is `[inferred]`, not verified.
16. **The Militech Offices' interior is a stub.** The wiki's layout detail is
    2020-era (lobby, showroom, cafeteria, museum, war rooms) plus a note about
    barred elevators to an unfinished area in 2077. Do not promise a multi-floor
    capture volume.
17. **The "Militech lab in the Badlands" has no location.** *Gig: Concrete Cage
    Trap* says Tiny Mike stole data from a Militech lab in the Badlands; no site,
    marker or wiki page names it. Catalogued nowhere; noted here so the economy
    model does not pretend it is mapped. `[wiki]`
18. **`faction_headquarters.json` has no Militech row.** Only Maelstrom, Tyger
    Claws, Valentinos, 6th Street, Voodoo Boys and Arasaka are present. A seeder
    reading only that file finds nothing for Militech; this doc supplies the row
    from site 11.
19. **The Gold Beach Marina's nearest CC is Valentinos-owned.**
    `cc_dtn_south_waterfront` (`sub_territory_id 74`) has
    `initial_owner_faction_id 3`. Retargeting by nearest CC would hand a Militech
    security contract to the Valentinos. METHOD §1.1 item 10 covers this; it is
    the second corp instance after the Arasaka Memorial.
20. **No 2077 showroom exists.** The 2020 regional office and every "major city"
    had Militech showrooms; the 2077 Night City office is described only as a
    regional HQ, and the extract has no vendor inventory. `retail` is therefore
    an `[inferred]` stream at one site, not a catalogued shop.

---

## 9. Sources

Local:

- `dist/extract/markers.jsonl` — `Ina_04_mp_outpost`,
  `q000_nomad_mp_border_crossing_checkpoint`, `q000_nomad_mp_border_office`,
  `sq028_mp_wait_kerry_marina`, `q114_mp_*`.
- `dist/extract/areas.jsonl` — 136 areas / 121 dominant; Badlands events and
  `q114` clusters; PL set pieces.
- `dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_{0,1,2}.streamingsector.json`
  — prefab paths proving sub-districts: `c_city_center/corpo_plaza/loc_ma_cct_cpz_06_prefabAZTRELQ`,
  `c_city_center/downtown/loc_sts_cct_dtn_05_luxury_yacht_prefabNYWJWMA`,
  `c_watson/kabuki/loc_sts_wat_kab_01_street_maze_prefab4TMOWAQ`,
  `c_heywood/glen/loc_sts_hey_gle_01_prefabW3U6XOY`,
  `c_santo_domingo/arroyo/loc_sts_std_arr_03_prefabSLUWFZI`,
  `c_westbrook/japan_town/loc_sts_wbr_jpn_09_netrunner_parking_lot_prefabDQJWZUQ`.
- `data/sites/sites.json` (sites 11, 12, 40, 342–345, 348, 354, 358, 364, 380,
  391, 422, and the drone sites), `rosters.json`, `communities.json`,
  `guards/triggers/spots/patrols/doors/devices.json`, `suitabilities.json`.
- `data/{factions,districts,sub_territories,landmarks,control_centers,faction_headquarters}.json`
  — faction id 21, sub-district spelling, the 10 seeded sub-territories and their
  CCs.
- `docs/research/factions/METHOD.md`, `docs/research/factions/arasaka.md`,
  `docs/research/factions/tyger-claws.md`.

Wiki (MediaWiki API, `action=parse&prop=wikitext` on 2026-11-25):

- [Militech](https://cyberpunk.fandom.com/wiki/Militech)
- [Militech Offices (2077)](https://cyberpunk.fandom.com/wiki/Militech_Offices_(2077))
- [Militech Offices (disambiguation)](https://cyberpunk.fandom.com/wiki/Militech_Offices_(disambiguation))
- [Militech Offices (2020)](https://cyberpunk.fandom.com/wiki/Militech_Offices_(2020))
- [Militech Detention Center](https://cyberpunk.fandom.com/wiki/Militech_Detention_Center)
- [Sunshine Motel](https://cyberpunk.fandom.com/wiki/Sunshine_Motel)
- [SoCal Border Crossing](https://cyberpunk.fandom.com/wiki/SoCal_Border_Crossing)
- [NorCal-SoCal Border Wall](https://cyberpunk.fandom.com/wiki/NorCal-SoCal_Border_Wall)
- [Gold Beach Marina](https://cyberpunk.fandom.com/wiki/Gold_Beach_Marina)
- [Cynosure](https://cyberpunk.fandom.com/wiki/Cynosure)
- [Cynosure Facility](https://cyberpunk.fandom.com/wiki/Cynosure_Facility)
- [Cynosure Site D](https://cyberpunk.fandom.com/wiki/Cynosure_Site_D)
- [Longshore Stacks](https://cyberpunk.fandom.com/wiki/Longshore_Stacks)
- [Heavy Hearts](https://cyberpunk.fandom.com/wiki/Heavy_Hearts)
- [Rocky Ridge](https://cyberpunk.fandom.com/wiki/Rocky_Ridge) · [Red Peaks](https://cyberpunk.fandom.com/wiki/Red_Peaks)
- [Jackson Plains](https://cyberpunk.fandom.com/wiki/Jackson_Plains) · [Night Corp Solar Farm](https://cyberpunk.fandom.com/wiki/Night_Corp_Solar_Farm) · [Northern Oil Fields](https://cyberpunk.fandom.com/wiki/Northern_Oil_Fields)
- Gigs (baseid-verified): [Radar Love](https://cyberpunk.fandom.com/wiki/Gig:_Radar_Love) (`sts_bls_ina_04`), [Goodbye, Night City](https://cyberpunk.fandom.com/wiki/Gig:_Goodbye,_Night_City) (`sts_bls_ina_05`), [No Fixers](https://cyberpunk.fandom.com/wiki/Gig:_No_Fixers) (`sts_bls_ina_06`), [Dancing on a Minefield](https://cyberpunk.fandom.com/wiki/Gig:_Dancing_on_a_Minefield) (`sts_bls_ina_07`), [Eye for an Eye](https://cyberpunk.fandom.com/wiki/Gig:_Eye_for_an_Eye) (`sts_hey_gle_01`), [Concrete Cage Trap](https://cyberpunk.fandom.com/wiki/Gig:_Concrete_Cage_Trap) (`sts_wat_kab_01`), [Race to the Top](https://cyberpunk.fandom.com/wiki/Gig:_Race_to_the_Top) (`sts_std_arr_03`), [The Frolics of Councilwoman Cole](https://cyberpunk.fandom.com/wiki/Gig:_The_Frolics_of_Councilwoman_Cole) (`sts_cct_dtn_05`), [Heaviest of Hearts](https://cyberpunk.fandom.com/wiki/Gig:_Heaviest_of_Hearts) (`sts_ep1_06`).

---

## 10. Machine-readable block

Strict JSON for seeding (contract in [`METHOD.md`](./METHOD.md) §10). Every
coordinate was verified against the local record named in `source` on
2026-11-25; none came from the wiki. `null` means `TBD`, never `0`.

```json
{
  "faction_code": "militech",
  "hq": {
    "name": "Militech Offices (Night City Regional HQ)",
    "district": "CityCenter",
    "sub_district": "CorpoPlaza",
    "x": -1308.475,
    "y": -56.376,
    "z": 2.15,
    "source": "data/sites/sites.json site 11 ma_cct_cpz_06",
    "confidence": "game-data+wiki"
  },
  "alternate_hqs": [
    {
      "name": "Sunshine Motel (Militech outpost)",
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": 3637.395,
      "y": -924.529,
      "z": 120.505,
      "source": "dist/extract/markers.jsonl Ina_04_mp_outpost",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Gold Beach Marina",
      "district": "CityCenter",
      "sub_district": "Downtown",
      "x": -2468.996,
      "y": 47.517,
      "z": 4.134,
      "source": "data/sites/sites.json site 354 sts_cct_dtn_05",
      "confidence": "game-data+wiki"
    }
  ],
  "test_control_point": {
    "name": "Militech Detention Center",
    "district": "Badlands",
    "sub_district": "Badlands",
    "x": -112.566,
    "y": -5246.731,
    "z": 87.16,
    "source": "data/sites/sites.json site 343 sts_bls_ina_05",
    "confidence": "game-data+wiki"
  },
  "control_points": [
    {
      "rank": 1,
      "name": "Militech Offices (Night City Regional HQ)",
      "type": "corporate_hq",
      "relevance": 5,
      "district": "CityCenter",
      "sub_district": "CorpoPlaza",
      "x": -1308.475,
      "y": -56.376,
      "z": 2.15,
      "source": "data/sites/sites.json site 11 ma_cct_cpz_06",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": [
        "security_services",
        "arms",
        "retail",
        "real_estate",
        "mercenary"
      ],
      "nearest_cc_code": "cc_cpz_militech_hq",
      "nearest_cc_m": 1.8
    },
    {
      "rank": 2,
      "name": "Sunshine Motel (Militech outpost)",
      "type": "military_outpost",
      "relevance": 5,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": 3637.395,
      "y": -924.529,
      "z": 120.505,
      "source": "dist/extract/markers.jsonl Ina_04_mp_outpost",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": [
        "security_services",
        "arms",
        "rnd"
      ],
      "nearest_cc_code": "cc_bls_militech_outpost",
      "nearest_cc_m": 9.8
    },
    {
      "rank": 3,
      "name": "Gold Beach Marina",
      "type": "private_marina_security",
      "relevance": 4,
      "district": "CityCenter",
      "sub_district": "Downtown",
      "x": -2468.996,
      "y": 47.517,
      "z": 4.134,
      "source": "data/sites/sites.json site 354 sts_cct_dtn_05",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": [
        "security_services",
        "hospitality"
      ],
      "nearest_cc_code": "cc_dtn_south_waterfront",
      "nearest_cc_m": 237.9
    },
    {
      "rank": 4,
      "name": "Militech Detention Center",
      "type": "detention_center",
      "relevance": 4,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": -112.566,
      "y": -5246.731,
      "z": 87.16,
      "source": "data/sites/sites.json site 343 sts_bls_ina_05",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": [
        "security_services"
      ],
      "nearest_cc_code": "cc_bls_solar_station",
      "nearest_cc_m": 384.9
    },
    {
      "rank": 5,
      "name": "SoCal Border Crossing",
      "type": "border_checkpoint",
      "relevance": 4,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": -2823.058,
      "y": -5645.812,
      "z": 101.404,
      "source": "dist/extract/markers.jsonl q000_nomad_mp_border_crossing_checkpoint",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": [
        "security_services",
        "smuggling"
      ],
      "nearest_cc_code": "cc_bls_border_crossing",
      "nearest_cc_m": 211.0
    },
    {
      "rank": 6,
      "name": "Cynosure Site D",
      "type": "research_facility",
      "relevance": 3,
      "district": "Dogtown",
      "sub_district": "Dogtown",
      "x": null,
      "y": null,
      "z": null,
      "source": "wiki only; access elevator at Kress St, Longshore Stacks (data/landmarks.json lm_dt_longshore_stacks -2319.8,-2544.0); coordinate TBD",
      "confidence": "wiki+inferred",
      "interior": true,
      "revenue_streams": [
        "rnd",
        "netrunning"
      ],
      "nearest_cc_code": null,
      "nearest_cc_m": null
    },
    {
      "rank": 7,
      "name": "Cynosure Facility (Site C)",
      "type": "research_facility",
      "relevance": 3,
      "district": "Dogtown",
      "sub_district": "Dogtown",
      "x": null,
      "y": null,
      "z": null,
      "source": "wiki only (owner Militech formerly, underground Pacifica); coordinate TBD",
      "confidence": "wiki+inferred",
      "interior": true,
      "revenue_streams": [
        "rnd",
        "netrunning"
      ],
      "nearest_cc_code": null,
      "nearest_cc_m": null
    },
    {
      "rank": 8,
      "name": "Downtown West Pier",
      "type": "pier",
      "relevance": 2,
      "district": "CityCenter",
      "sub_district": "Downtown",
      "x": -2164.836,
      "y": 587.743,
      "z": 7.25,
      "source": "data/sites/sites.json site 40 ma_cct_dtn_15",
      "confidence": "game-data+inferred",
      "interior": false,
      "revenue_streams": [
        "security_services",
        "smuggling"
      ],
      "nearest_cc_code": "cc_dtn_goldsmith_dock",
      "nearest_cc_m": 7.0
    },
    {
      "rank": 9,
      "name": "Corpo Plaza North Overpass",
      "type": "drone_patrol",
      "relevance": 2,
      "district": "CityCenter",
      "sub_district": "CorpoPlaza",
      "x": -1289.845,
      "y": 340.535,
      "z": 9.581,
      "source": "data/sites/sites.json site 12 ma_cct_cpz_10",
      "confidence": "game-data+inferred",
      "interior": false,
      "revenue_streams": [
        "security_services"
      ],
      "nearest_cc_code": "cc_cpz_ring_road_north",
      "nearest_cc_m": 7.7
    }
  ],
  "subdistrict_counts": {
    "Badlands": {
      "named": 3,
      "filler": 4
    },
    "CorpoPlaza": {
      "named": 1,
      "filler": 1
    },
    "Downtown": {
      "named": 1,
      "filler": 1
    },
    "Dogtown": {
      "named": 2,
      "filler": 1
    },
    "Glen": {
      "named": 0,
      "filler": 2
    },
    "Kabuki": {
      "named": 0,
      "filler": 3
    },
    "JapanTown": {
      "named": 0,
      "filler": 2
    },
    "Northside": {
      "named": 0,
      "filler": 1
    },
    "LittleChina": {
      "named": 0,
      "filler": 1
    },
    "VistaDelRey": {
      "named": 0,
      "filler": 1
    },
    "Arroyo": {
      "named": 0,
      "filler": 1
    }
  }
}
```
