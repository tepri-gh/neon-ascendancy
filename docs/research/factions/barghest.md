# Barghest — Lore-Relevant Control Points

Status: faction research run, 2026-11-25. One faction, one document.
Scope: replace the generic ~5-control-centres-per-sub-district grid with
lore-relevant, capturable places for **Barghest**, with an honest count per
sub-district. Method: this doc conforms to [`METHOD.md`](./METHOD.md); research
snippets, wiki rules, the revenue-code vocabulary and the JSON-block contract
live there.

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Position, site, community, roster or spawn record read from `dist/extract/` or `data/sites/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/artbook lore with no verified in-game artifact | Tertiary |
| `[inferred]` | Reasoning links a named place to a game record; reasoning stated | Weak, flagged |

No coordinate below is guessed. Every `(x, y, z)` is either copied from a named
record in the local extracts or marked `TBD`.

---

## 1. Summary

Barghest is **Kurt Hansen's militia**: a former NUSA/Militech urban-combat unit
that refused its 2070 withdrawal orders, seized the unfinished Pacifica
sub-district of Serenisands and turned it into **Dogtown**, a walled combat
zone. `[wiki]` It is not a street gang and not a corporation — it is the
district's army, arms dealer, customs service and police force at once. `[wiki]`

**Canon base:** the wiki infobox names **Black Sapphire** as headquarters, and
Kurt Hansen's residence. `[wiki]` Dogtown itself is the territory; there is no
second seat.

**Economic model** (from the wiki's *Source of Income* section, confirmed by
name against game records in §4):

- **Arms dealing, globally.** A captured Unification-War stockpile plus their
  own factory, **Hansen Armory**, whose HQ is the **Nighthawks Rehabilitation
  Center** inside the stadium. `[wiki]`
- **Smuggling.** AV **airdrop** runs into Dogtown and the **Dogtown Tunnel** to
  West Wind Estate — "the money from his large-scale smuggling operation".
  `[wiki]`
- **The stadium black market.** The largest black-market trade location on the
  West Coast; the wiki calls it Dogtown's "beating heart". `[wiki]`
- **Protection and graft.** A "registration fee" to trade in the stadium
  market, plus soldiers shaking down civilians. `[wiki]`
- **The Black Sapphire club.** A floor-99 club, casino and restaurant that
  lures "elite players … from around the world" to make deals "secure from all
  except the watchful eye of Kurt". `[wiki]`

The weight sits in **Dogtown's Golden Pacific** quarter (Black Sapphire +
Heavy Hearts + the gates) and in the **stadium complex** (market, armory,
underground parking). Two more holdings — the north gate and Dodger's former
NCPD precinct — are technically outside the wall in **Coastview**.

---

## 2. Territory

### 2.1 Districts

| Evidence kind | Result |
| --- | --- |
| (a) Wiki/lore | Pacifica's walled **Dogtown** combat zone; the fandom wiki types Dogtown as "Sub-district / Combat Zone" under Pacifica, but `gamedataDistrict` gives it its own district. `[wiki]` |
| (b) Vanilla map gang panel | `data/districts.json`: Dogtown `["Barghest"]`, bbox x −2640…−1165, y −3245…−1770. No other gang is listed. `[game-data]` |
| (c) Game-data counts | 187 community areas contain Barghest spawns (**185 Barghest-dominant**, 1,449 Barghest records); 4 roster sites / 87 units; 4 owned sub-territories. 177 of the 187 areas are inside the Dogtown bbox. `[game-data]` |

Owned sub-territories (`sub_territories.initial_owner_faction_id == 10`),
`[game-data]`:

| Sub-territory | Sub-district | Seed display name | Landmark anchor |
| --- | --- | --- | --- |
| `dt_main_gate` (91) | Dogtown | Dogtown Checkpoint Gate | `(-2062.2, -2310.4, 19.0)` |
| `dt_black_sapphire` (92) | Dogtown | Black Sapphire Plaza | `(-1928.5, -2313.6, 44.4)` |
| `dt_longshore_stacks` (93) | Dogtown | Longshore Stacks | `(-2319.8, -2544.0, 17.0)` |
| `dt_luxor_heights` (95) | Dogtown | Luxor High Wellness Spa | `(-2134.3, -2692.7, 78.6)` |

`dt_terra_cognita` (94) is owned by the Voodoo Boys, not Barghest, and its
"Luxor High Wellness Spa" display name is the only correct use of that name
(see §8, gaps 3–4). The seed has **no** Dogtown sub-territory for the stadium
or for Terra Cognita proper.

### 2.2 Sub-district presence

`gamedata_subdistrict` has exactly one Dogtown value, so the contract's
sub-district dimension is almost meaningless here. Counts are from
`dist/extract/areas.jsonl` (any area whose `faction_counts` contains
`barghest`).

| Sub-district | District | (a) Lore | (b) Vanilla panel | Barghest areas (dominant) | Barghest-occupied sites* |
| --- | --- | --- | --- | ---: | ---: |
| Dogtown | Dogtown | the entire district | Barghest | 177 (175) | 3 |
| Coastview | Pacifica | both gates and the NCPD precinct sit just outside the wall `[wiki]` | VDB + Animals | 10 (10) | 1 |

\* Deduped `data/sites/sites.json` rows with `default_faction_id == 10` or at
least one Barghest roster entry, attributed per §3.1 rather than by
`district_code`. None of the four collapses within 25 m.

**Where the mass actually is.** The 187 areas hold 1,449 Barghest records, but
they are not evenly distributed and most of them are not holdings:

| Cluster | Areas | Barghest records | What it is |
| --- | ---: | ---: | --- |
| Unnamed quest corridors (`q301_*`, `q302_*`, `mq301_*`, `sa_ep1_*`, `wtc_run_off`) | 101 | 681 | Firestarter / Dog Eat Dog staging, road ambushes, sandbox activity waves. **Corridors, not holdings** (METHOD §1.2 item 9) |
| Stadium complex (`*_stadium*`, `sts_ep1_07`) | 32 | 201 | Market, factory, garages, escape routes |
| Black Sapphire (`*_paradise*`, `*_tower_*`, `kurts_wake`) | 11 | 209 | Lobby, floor 67, floor 99, wake |
| Space Force One crash site (`*_crashsite*`, `*_shuttle*`) | 13 | 102 | The `q301` crash scene, snapped to a centroid (§2.3) |
| Gates (`*_border_*`, `cz_gate`, `combat_zone_gate`) | 10 | 94 | North and west checkpoints |
| Dogtown Tunnel (`we_ep1_01_*`) | 4 | 46 | ICA: BARGHEST defence of the smuggling tunnel |
| Heavy Hearts (`sts_ep1_06_*`) | 3 | 37 | The club |
| Stadium parking (`*car_retrieval*`, `*_garage`) | 3 | 34 | Firestarter car retrieval + stadium garage |
| NCPD precinct (`sts_ep1_10_*`) | 5 | 17 | Dodger's base |
| q302 Lucretia clusters | 5 | 28 | Oath, basketball, hotel, protest scenes |

**Attribution caveat (this is the worst case in the project so far).** Dogtown
has no geocode token of its own. `METHOD.md` §3.3's token map has no
`ep1`/`q30x`/`sa_ep1` entries at all, so **every** Phantom Liberty row falls
through to `nearest-subterritory`, and the nearest sub-territory is one of five
seeded centroids that were themselves taken from quest communities. Twelve
Dogtown area rows sit exactly (< 1 m) on a centroid, including the four biggest
Barghest anchors:

- `{q303_com_tower_lobby_combat}` (78 Barghest) = `dt_black_sapphire` centroid
- `{combat_zone_gate_com}` (30) = `dt_main_gate` centroid
- `we_ep1_01_combat_com_1st/2nd_loop` (23 + 19) = `dt_longshore_stacks` centroid
- five `q301_com_crashsite_*` rows (17 + 16 + 10 + 9 + 6) = `dt_luxor_heights` centroid

This is not a data defect to be filtered out: it is **circular seed
provenance**. The seed named the sub-territory after the community and snapped
the community onto the sub-territory. Where that happens I used the nearest
non-snapped sibling node and said so; see §3.1 and §8, gap 2.

`district_code` is also unusable here: all 177 in-district rows say `dogtown`
because they live under `ep1\…`, but `sts_ep1_07` (the stadium factory) and
`sts_ep1_12` (the Luxor spa) are `district_id 5` / sub-territories 63 and 94.
The stadium factory is in Dogtown; the Luxor spa is the Voodoo Boys'. Nothing
in the seed's Dogtown sub-territory list describes the stadium at all.

### 2.3 Dogtown has no `c_dogtown` prefab tree

`METHOD.md` §1.1 item 2 tells you to grep the raw sector JSON prefab paths.
For Dogtown that yields only five placement groups, all under
`/03_night_city/c_pacifica/combat_zone_prefabUEX7DCY/`:
`container_zone` (Longshore Stacks), `high_peak` (Luxor Heights),
`monument_av` and `boulevard_av` (Golden Pacific blocks), and
`#loc_pr_stadium` (the stadium).

Everything else — Black Sapphire, Heavy Hearts, the armory, the precinct — is
loaded from **quest** sectors. `data/sites/sites.json` has a null
`quest_prefab_ref` for every `ep1` site, and `quest_sector_path` points at
`quest_*.streamingsector` files that are **not** in the extract. So for
Phantom Liberty, prefab archaeology cannot identify interiors; node names and
community names must (§3.1).

---

## 3. Location catalog

Coordinates are world-space metres, `Z` up. "Interior?" means the game has a
distinct interior cell/sector.

| # | Name | Type | District / sub-district | Interior? | Business? (what it earns) | Coordinates (x, y, z) | Coordinate source record | Linked communities / sites | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **Black Sapphire** | Unfinished 99-floor hotel → BARGHEST HQ | Dogtown / Dogtown (Golden Pacific) | Yes — ground floor, floor 67, floor 99 club/casino/restaurant, AV pads | Yes: floor-99 club, casino and restaurant; Hansen's private deal-making venue | `(-1881.135, -2316.233, 41.005)` lobby; `(-1922.437, -2314.250, 439.766)` floor 99; `(-1887.597, -2316.295, 344.264)` floor 67 | `areas.jsonl` `{q303_com_tower_lobby}` (hash `8039314437540013265`, 13 entries, 9 Barghest); `{q303_com_paradise_quest_interactions}` (57); `{q303_com_paradise_technical_floor_guards}` (48) | `{q303_com_tower_lobby_combat}` (78 Barghest, centroid-snapped); `{mq304_com_kurts_wake}` (47); enum-shaped name "Paradise" from the dev name; CC/landmark `dt_black_sapphire` | `[game-data]` `[wiki]` |
| 2 | **EBM Petrochem Stadium** (Nighthawks Stadium) | Defunct stadium → black market + power plant | Dogtown / Dogtown | Yes — bowl, stands, market level, garages | Yes: the black market (largest on the West Coast), plus the crashed aerozep's reactor that powers Dogtown | `(-1412.888, -2012.373, 71.860)` bowl; `(-1403.125, -1999.162, 72.523)` market | `areas.jsonl` `{q301_com_stadium}` (21 entries, 5 Barghest); `{q304_com_stadium_escape_kurts_soldiers_market}` (5) / `_market_end` (4) | 32 stadium-cluster areas / 201 Barghest; prefab `cz_stadium_black_market_01`, `#loc_pr_stadium`; vendors `{cz_stadium_clothing_01_tommie_walker_com}`, `{cz_stadium_ws_vendor_06_robot_com}` | `[game-data]` `[wiki]` |
| 3 | **Nighthawks Rehabilitation Center** (Hansen Armory) | Weapons factory + test range | Dogtown / Dogtown | Yes — top stadium level, production area in the old swimming pool | Yes: Hansen Armory's HQ and production line; weapons "developed and modified to suit buyers' needs" | `(-1379.057, -1939.644, 87.477)` factory floor; `(-1373.646, -1941.066, 63.803)` deal room / lab | `areas.jsonl` `{sts_ep1_07_enemies_com}` (16 entries, 8 Barghest); `{q304_com_stadium_lab_kurt_soldiers}` (6); site 359 `sts_ep1_07` | Gig baseid `sts_ep1_07` = *Roads to Redemption*; `{q304_com_stadium_deal_kurts_soldiers}` (38 Barghest); doors `#sts_ep1_07_main_door` | `[game-data]` `[wiki]` |
| 4 | **Heavy Hearts** | Egyptian-themed elite nightclub | Dogtown / Dogtown (Golden Pacific) | Yes — entrance, bar, VIP booths, staff room, backroom elevator | Yes: 24/7 club, "XXX BDs", imported liquors and stimulants, discreet VIP rooms; Mr. Hands operates out of it | `(-1606.430, -2341.452, 43.070)` site anchor; `(-1587.910, -2354.529, 43.070)` ground floor | **Site 358** `sts_ep1_06` (49 Barghest roster units); `areas.jsonl` `{sts_ep1_06_com_ground_floor}` (hash `17927932051716558365`, 10); `{sts_ep1_06_com_fake_barghest_guard}` (18) | Doors `#sts_ep1_06_heavy_hearts_entrance_doors`, `#sts_ep1_06_vip_doors`, `#sts_ep1_06_booth_6_doors`, `#sts_ep1_06_doors_staff_room`, `#sts_ep1_06_techie_doors`, `#q303_dvc_backroom_elevator`; gig baseid `sts_ep1_06` = *Heaviest of Hearts* | `[game-data]` `[wiki]` |
| 5 | **The Tunnel** (Dogtown Tunnel) | Smuggling tunnel to West Wind Estate | Dogtown / Dogtown (Longshore Stacks) | Yes — tunnel, vehicle-sized | Yes: the BARGHEST smuggling artery; a 48-hour pipeline from the stadium to 6th Street | `(-2326.107, -2557.094, 14.179)` | `areas.jsonl` `{we_ep1_01_q302_combat_com}` (hash `12713071501951577929`, 3 Barghest) | `we_ep1_01_*` (46 Barghest across 4 areas, two of them centroid-snapped); baseid `we_ep1_01` = *Increased Criminal Activity: BARGHEST*; lieutenant Ross Ulmer | `[game-data]` `[wiki]` |
| 6 | **Stadium Underground Parking** | Derelict parking garage → smuggling staging | Dogtown / Dogtown | Yes — bays 1A–9A / 1B–8B | Yes: an "illicit smuggling route to get goods out and into Dogtown" | `(-1454.540, -2139.720, 30.350)`; second level `(-1411.454, -2148.039, 32.796)` | `areas.jsonl` `{q304_com_stadium_escape_kurts_soldiers_garage}` (hash `3090696465833105295`, 9 Barghest); `_delivery` (7) | `{q304_car_retrieval_community_inner_garage}` (17) is the Firestarter garage; doors `#sts_ep1_10_garage_gate` at the precinct, not here | `[game-data]` `[wiki]` |
| 7 | **Dogtown west gate** | Checkpoint into Dogtown | Dogtown / Dogtown | No — open-air gate, shutters, turrets, scanners | Yes: customs and extortion on everything crossing the wall; the Prevention Unit mans it | `(-2033.521, -2349.511, 18.794)` | `areas.jsonl` `{q302_cz_gate}` (hash `17435183680842590867`, 10 entries, 8 Barghest) | `{combat_zone_gate_com}` (30, centroid-snapped); `{q304_com_combat_zone_gate_cars}` (22); CC `cc_dt_main_gate` (active, owner Barghest) | `[game-data]` `[wiki]` |
| 8 | **Dogtown north gate** | Main access for outsiders and cargo | Pacifica / Coastview | No — open-air checkpoint | Yes: customs, cargo inspection, protection money | `(-1302.500, -1726.000, 45.750)` | `areas.jsonl` `{q301_com_border_combat_gate}` (hash `7242737884370904763`, 11 Barghest) | `{q301_com_border_combat_front}` (10), `{q301_pr_ep1_teaser_combat_community}` (33), `{q301_com_border_reinforcements}` (18) | `[game-data]` `[wiki]` |
| 9 | **Pacifica NCPD Precinct** (Dodger's base) | Abandoned police station → BARGHEST base | Pacifica / Coastview | Yes — front desk, side rooms, storage, garage | Partly: a base of operations, not a business; Dodger runs the local shakedown from it | `(-2215.200, -2289.278, 12.030)` | **Site 361** `sts_ep1_10` (17 Barghest roster units); `areas.jsonl` `{sts_ep1_10_enemies_ground_floor_com}` (8) | `{sts_ep1_10_dodger_com}` (4); `{sts_ep1_10_tv_crew_com}` (NCPD hostages, 7); gig baseid `sts_ep1_10` = *Waiting for Dodger*; doors `#sts_ep1_10_garage_gate` | `[game-data]` `[wiki]` |

Named places the wiki lists but which are **not** Barghest holdings — shops,
monuments and other factions' buildings inside Dogtown — are in §3.3.

### 3.1 How the name→coordinate links were proven

The site extractor's node names are the whole method for Dogtown, because the
prefab tree does not reach quest interiors (§2.3).

- **Heavy Hearts — proven by a door name.** Site 358 (`sts_ep1_06`) has a door
  literally called `#sts_ep1_06_heavy_hearts_entrance_doors`, plus
  `#sts_ep1_06_vip_doors`, `#sts_ep1_06_booth_6_doors`,
  `#sts_ep1_06_doors_staff_room`, `#sts_ep1_06_techie_doors` and
  `#q303_dvc_backroom_elevator`. The gig has `baseid = sts_ep1_06`
  (*Heaviest of Hearts*), and its NPCs are `Character.sts_ep1_06_golden_pacific_ma/wa`.
  That is a direct name→record join, not an inference. The anchor
  `(-1606.430, -2341.452)` is 22 m from the club's own ground-floor community
  `(-1587.910, -2354.529)`, which is the normal site-anchor error here
  (METHOD §1.1 item 7).
- **Black Sapphire — proven by the development name.** The wiki records that
  the tower was called **Paradise Hotel** during development, and the game's
  floor-99 nodes are `{q303_com_paradise_quest_interactions}`,
  `{q303_com_paradise_casino_crowd}`, `{q303_com_paradise_guests_audience}`,
  with `q303_paradise_casino`, `q303_paradise_restaurant`,
  `q303_paradise_dealer` and `q303_paradise_barman_*` prefab strings. The
  floor split matches the wiki layout exactly: floor 1
  (`tower_lobby`, z ≈ 41–44), floor 67 (`paradise_technical_floor_*`,
  z ≈ 344), floor 99 (`paradise_*`, z ≈ 440), and the
  `mq304_com_kurts_wake` community at z ≈ 440, which is the wake Hansen hosts
  there in *Run This Town*. `Character.q303_paradise_guest_*` and
  `Character.q303_kurtz_guard_paradise_*` complete the join.
- **Stadium / black market / armory — proven by quest id and room names.**
  The stadium's market nodes are `{q304_com_stadium_escape_kurts_soldiers_market}`,
  `_market_end` and `_market_reinforcements`, and the prefab tree contains
  `cz_stadium_black_market_01`, `{cz_stadium_clothing_01_tommie_walker_com}`
  and `{cz_stadium_ws_vendor_06_robot_com}` (Tommie Walker is the wiki's
  clothing vendor). The armory is `sts_ep1_07` whose gig *Roads to Redemption*
  is set in "the weapons factory - top stadium level"; its enemies community
  sits at z ≈ 87 while the deal room sits at z ≈ 64, which is the multi-level
  split the wiki describes.
- **The Tunnel — proven by the activity id.** `we_ep1_01` is
  *Increased Criminal Activity: BARGHEST*, whose infobox location is The
  Tunnel. Its four communities are the tunnel defence. Three of the four sit on
  the `dt_longshore_stacks` centroid, so the map anchor here is
  `{we_ep1_01_q302_combat_com}` at 14 m from the centroid — the least-bad
  non-snapped node, still `[inferred]` as a precise tunnel mouth.
- **North gate — proven by position plus the wiki.** All five `q301_com_border_*`
  and `q301_pr_ep1_teaser_*` communities sit at
  `(-1302.5…-1324.4, -1726…-1769)`, i.e. **north of the stadium and outside the
  Dogtown bbox** — exactly where the wiki puts the northern gate ("due north of
  the EBM Petrochem Stadium", in Coastview). 86 Barghest records guard it.
- **West gate — the seed's own anchor, with a caveat.** `{combat_zone_gate_com}`
  is 0 m from the `dt_main_gate` centroid and 30 records strong, so its
  coordinate is circular. I used `{q302_cz_gate}` instead (10 records, 49 m
  away), which is a normal reading of the same checkpoint.
- **NCPD precinct — proven by gig baseid.** `sts_ep1_10` = *Waiting for
  Dodger*; the wiki's location is "Former NCPD station", and the site's
  communities are named `sts_ep1_10_dodger_com`, `_enemies_lockup_com`,
  `_tv_crew_com` (the hostage officers) and `_garage_gate`.

**A trap worth recording.** `los_osos`, `eden_plaza` and `wild_blue` appear in
the extract — but at `#c_pacifica/coastview/pac_cvi_los_osos_*` and
`#c_westbrook/charter_hill/wbr_hil_eden_plaza_*` /
`wbr_hil_wild_blue_hotel_*`. Those are **Coastview and Charter Hill** assets
with the same names as Dogtown businesses. Name-matching would put a Dogtown
bar in Westbrook. I did not use them.

### 3.2 Barghest-occupied sites (the whole site footprint)

Every Barghest-occupied site, with the suitability tags that make it useful as
a business slot.

| Site | Code | Sub-district (attributed) | Interior | Suitability tags | Units (Barghest) | Coordinates | Note |
| --- | --- | --- | --- | --- | ---: | --- | --- |
| 358 | `sts_ep1_06` | Dogtown (Golden Pacific; seed 92) | yes | `officer_site` 90, `rooftop_access` 80, `elevator` 70 | 49 | `(-1606.430, -2341.452, 43.070)` | **Heavy Hearts** (named) |
| 359 | `sts_ep1_07` | Dogtown (Stadium; seed says Pacifica/63) | yes | `rooftop_access` 80, `officer_site` 60 | 20 | `(-1401.314, -2013.167, 85.220)` | **Nighthawks Armory** (named). Anchor is 78 m from its own enemies community; use §3 #3 |
| 361 | `sts_ep1_10` | Coastview (seed 91) | yes | `vehicle_bay` 65, `rooftop_access` 62 | 17 | `(-2215.200, -2289.278, 12.030)` | **NCPD precinct** (named) |
| 362 | `sts_ep1_12` | Dogtown (Luxor Heights; seed 94) | yes | `rooftop_access` 80, `officer_site` 60 | 1 | `(-1386.757, -2463.720, 85.000)` | The Voodoo Boys' Luxor spa. Its single Barghest record is `Character.sts_ep1_12_courier` — a courier, not a garrison. **Filler at most** |

Four sites is the entire site footprint. There is no site row for the Black
Sapphire, the stadium, the market, any gate or the tunnel: for this faction
sites are the exception, communities are the rule.

### 3.3 Airdrop drop zones (`sa_ep1_*`) — Barghest's inbound supply footprint

The eight-digit `sa_ep1_*` sandbox communities are the **airdrop metaquest**
locations; each wiki *Airdrops* section names one. They are where AVs drop
Barghest gear, and they are the physical map of the `smuggling` stream. They
are **events on other people's property**, not holdings, so they are not
counted in §7 and not seeded as control points.

| Airdrop | Wiki drop location `[wiki]` | `areas.jsonl` record (Barghest) | Coordinates `[game-data]` |
| --- | --- | --- | --- |
| `sa_ep1_3` | Wild Blue Hotel, behind the Akebono Hotel (Luxor Heights) | `{sa_ep1_3_barghest_com}` (6) | `(-2255.6, -2836.2, 109.2)` |
| `sa_ep1_30` | South of the Akebono Hotel | `{sa_ep1_30_enemies_com}` (9) | `(-2065.8, -2785.8, 86.0)` |
| `sa_ep1_31` | Wild Blue Hotel, behind the Akebono | `{sa_ep1_31_var_01_enemies_com}` (12) | `(-2241.5, -2858.5, 108.0)` |
| `sa_ep1_32` | Construction site at the Kress Street Hideout | `{sa_ep1_32_com}` (12) | `(-2180.2, -2566.0, 17.7)` |
| `sa_ep1_33` | Swimming pool of the Los Osos Motel (Golden Pacific) | `{sa_ep1_33_faction2_com}` (4) | `(-1968.7, -2620.3, 45.1)` |
| `sa_ep1_34` | Terra Cognita parking lot, across from the Akebono | `{sa_ep1_34_var_02_com}` (14) | `(-2090.1, -3000.6, 108.0)` |
| `sa_ep1_35` | High Peak hotel construction site (Luxor Heights) | `{sa_ep1_35_enemies_com}` (7) | `(-1877.8, -2846.2, 97.7)` |
| `sa_ep1_36` | Parking lot south of the EBM Petrochem Stadium | `{sa_ep1_36_com}` (11) | `(-1391.1, -2311.5, 72.8)` |
| `sa_ep1_37` | Tranquil Terrace (Luxor Heights) | `{sa_ep1_37_faction_2_com}` (7) | `(-1761.3, -2637.5, 45.0)` |
| `sa_ep1_38` | Brave Atlas (after the Garry Bates cyberjunkie fight) | `{sa_ep1_38_com}` (15) | `(-1826.5, -2630.5, 39.8)` |
| `sa_ep1_39` | Undersea Reverie, atop the Lions of Eden | `{sa_ep1_39_kurt_com}` (8) | `(-1805.1, -2524.7, 49.9)` |
| `sa_ep1_300` | Near the Black Sapphire | `{sa_ep1_300_com}` (2) | `(-1795.0, -2223.3, 41.3)` |
| `sa_ep1_301` | Close to the Founding Our Future Expo | `{sa_ep1_301_av_com}` (AV node only) | `(-2069.5, -2509.5, 180.0)` |
| `sa_ep1_303` | Brave Atlas | `{sa_ep1_303_reinforcement_com}` (5) | `(-1862.3, -2629.4, 39.9)` |
| `sa_ep1_304` | Roof of the north tower, Montezuma's Throne / Capitán Caliente | `{sa_ep1_304_av_com}` (AV node) | `(-1648.0, -2376.2, 183.9)` |

Two cautions. First, an airdrop description locates a *neighbourhood*, not a
building: the three Akebono-relative drops bracket the hotel over a 200 m
spread, so the **Akebono Hotel stays `TBD`**. Second, `sa_ep1_33` puts the
Los Osos **Motel** in Golden Pacific at `(-1968.7, -2620.3)`; the
`pac_cvi_los_osos` assets in the extract are a Coastview homeless camp and are
unrelated (§3.1).

### 3.4 Wiki-only places, no verified coordinate

Named in the wiki's Dogtown/Golden Pacific/Longshore/Luxor/Stadium location
lists, but with no marker, site, community or prefab record that names them.
Not seeded; listed so the next agent does not re-chase them.

| Place | Wiki area | Type | Why `TBD` |
| --- | --- | --- | --- |
| The Needle (*To Our Mothers and Fathers Before Us*) | Golden Pacific | Obelisk + underground mall | No marker or prefab string. The only Barghest mass at the roundabout is `{mq301_com_initiation}` (42 units, `(-1834.6, -2314.9, 39.8)`), which is a quest scene, not a named record — plausible but `[inferred]` only |
| Brave Atlas | Golden Pacific | Building | Only the airdrop zones that sit on it (§3.3) |
| Coronado Bay Cinema | Golden Pacific | Cinema | Nothing |
| Dream Gig | Golden Pacific | Bar | Mentioned on a shard only |
| Eden Plaza (+ Brainporium, Capitán Caliente, De-votion, Jason Exiled, Montezuma's Throne) | Golden Pacific | Mall | `eden_plaza` in the extract is a **Charter Hill** asset; the Dogtown vendors' coordinates come only from `sa_ep1_304` roof data |
| Farida's Clinic | Golden Pacific | Clinic/ripperdoc | `q304_04d_at_faridas` appears as a string but carries no marker row |
| Founding Our Future Expo | Golden Pacific | Expo hall | Only `sa_ep1_301`'s AV node |
| Haven Clinic | Golden Pacific | Clinic | Nothing |
| Lions of Eden (+ Pride/Roar, Undersea Reverie) | Golden Pacific | Towers | Only `sa_ep1_39`'s roof zone |
| Los Osos (Dogtown) | Golden Pacific | Motel | Only `sa_ep1_33`'s pool zone; the extract's `los_osos` is in Coastview |
| The Dirty Deck, Orion | Golden Pacific | Bar, building | Nothing |
| Akebono Hotel | Luxor Heights | Hotel | Prefab names exist (`#high_peak_akebono_hotel_outcast_*`, `#cz_terra_cognita_akebono_hotel_roof_group_*`) but no coordinates; the airdrops only bracket it |
| Biotechnica Venture Center | Luxor Heights | Corp lab | Not Barghest; no record |
| Eventide Resort & Spa, Wild Blue, Tranquil Terrace, Mysterium, Gracefall | Luxor Heights | Resort, hotel, terrace | Only airdrop zones; see the Voodoo Boys doc for Eventide |
| High Peak | Luxor Heights | Hotel resort | Prefab group `high_peak_prefabAMBSEZY` exists (36 placement hits) but no coordinates; `sa_ep1_35` is its construction site |
| Lahovary's Clinic, Tree of the Lost, Paradise Hotel, The Scraper, Rindo Hotel, Kress Street Hideout, Cynosure Site D | Longshore Stacks | Clinic, memorial, hotel, hideout | `The Scraper` = `sts_ep1_04` (Scavengers), `x` at `(-2465.3, -2713.5)`; the rest have no coordinate record |
| Anatomicon, Digimmortal, ESC Explorer, Organitopia (Terra Cognita) | Terra Cognita | Exhibitions | Scavenger ground, not Barghest |

---

## 4. Economic structure

### 4.1 Revenue streams → catalog locations

| Revenue stream | Code(s) | Catalog locations that produce it | Evidence / notes |
| --- | --- | --- | --- |
| Global arms sales | `arms` | Nighthawks Rehabilitation Center (3); Black Sapphire (1, for the deals) | "Set themselves up as arms dealers on a global scale"; Hansen Armory sells HA-branded weapons worldwide. `[wiki]` |
| Weapons manufacture and customisation | `manufacturing`, `rnd` | Nighthawks Rehabilitation Center (3) | "Most of the weaponry used and sold by BARGHEST is developed and modified to suit buyers' needs"; production area in the old swimming pool. `[wiki]` |
| Black-market retail | `retail`, `arms`, `cyberware` | EBM Petrochem Stadium (2) | "Unique, tax-free, and hard to find items … to many of Night City's largest corporations"; vendor list includes a weapon, cyberware, ripperdoc and netrunner vendor. `[wiki]` |
| Contraband logistics (airdrop + tunnel) | `smuggling` | The Tunnel (5); Stadium Underground Parking (6); Stadium (2) | AVs "regularly airdrop equipment into Dogtown"; the Tunnel exports "any goods others might require … including people"; the garage is "an illicit smuggling route". `[wiki]` |
| Protection / market fees | `protection` | EBM Petrochem Stadium market (2); Dogtown west gate (7); Dogtown north gate (8) | A "registration fee" to do business in the stadium market; soldiers shake down civilians. `[wiki]` |
| Law enforcement / security contracts | `security_services` | West gate (7); North gate (8); NCPD precinct (9) | The Prevention Unit replaces NCPD inside the wall; the precinct is Dodger's base. `[wiki]` |
| Gambling | `gambling` | Black Sapphire (1) | Floor 99: "a club and a casino" in the northern tower. `[wiki]` |
| Nightlife / food | `food_drink` | Black Sapphire (1); Heavy Hearts (4) | Floor-99 restaurant; Heavy Hearts "imported liquors and stimulants", open 24/7. `[wiki]` |
| Sex work and braindance | `sex_work`, `braindance` | Heavy Hearts (4) | The club's own pamphlet advertises "XXX BDs" and "discreet VIP rooms". `[wiki]` |
| Hospitality | `hospitality` | Black Sapphire (1, AV pads and guest floors); Heavy Hearts (4, VIP rooms) | The tower is a 99-floor hotel with 2,792 rooms. `[wiki]` |
| Deal brokerage and intelligence | `fixer_brokerage`, `information` | Black Sapphire (1); Heavy Hearts (4) | Elite deals made at the Sapphire "secure from all except the watchful eye of Kurt"; Mr. Hands operates out of Heavy Hearts. `[wiki]` |
| Power (cost avoidance, not income) | `energy` | EBM Petrochem Stadium (2) | The downed aerozep's fission reactor "feeds the district's energy demand without depending on exterior suppliers". Not revenue, but it removes Dogtown's largest cost — modelled here because §7 has no better code. `[wiki]` |
| Contract muscle | `mercenary` | NCPD precinct (9) | Dodger's crew; the wiki's only explicit "muscle for hire" read is the shakedown operation. `[inferred]` |

Three catalog points earn **in kind**, not in eddies: the two gates (customs
leverage) and the tunnel (access). They still map to `protection` /
`security_services` / `smuggling`, so no point is left with an empty stream.

### 4.2 Suppliers, customers, rivals

| Role | Party | Detail |
| --- | --- | --- |
| Supplier (hardware) | Militech (historic) | The unit's original equipment and doctrine; "formerly" affiliated. `[wiki]` |
| Supplier (hardware, inbound) | Unknown AV operators | "Who sends the airdrops to Dogtown? It's a mystery." `[wiki]` |
| Supplier (power) | NUSA aerozep | Captured Zhirafa cargo airship with a live reactor. `[wiki]` |
| Customer | Night City's largest corporations and "most influential players" | The stadium market's off-the-books clientele. `[wiki]` |
| Customer | 6th Street and other gangs | The Tunnel database entry's worked example: "within 48 hours, 6th Street will have their hands on those sixty Militech M251s Ajax rifles". `[wiki]` |
| Customer / guest | Global elite at the Black Sapphire | The club exists to put them in Hansen's debt and under his eye. `[wiki]` |
| Tenant / partner | Mr. Hands (fixer) | Operates out of Heavy Hearts; brokers Dogtown and Pacifica contracts. `[wiki]` |
| Subordinate lieutenants | Chester Bennett, Jago Szabó | The succession fight after Hansen; both have dedicated `mq304` communities. `[wiki]` `[game-data]` |
| Rival | Voodoo Boys | Operate the Luxor spa inside Dogtown; "in business with BARGHEST as frequently as they clash". `[wiki]` |
| Rival | Scavengers | Terra Cognita, the Scraper, High Peak, and the container zone. `[wiki]` |
| Rival | Animals | Hold parts of the container zone and the Grand Imperial Mall on the Coastview seam. `[game-data]` |
| Rival (external) | NCPD, NUSA/FIA, NetWatch | NCPD is barred from the district; the FIA operation in 2077 is the campaign's main threat. `[wiki]` |
| Rival (internal) | Carl "Dodger" Robinson | A lieutenant with his own base and his own racket, loyal but independent. `[wiki]` |
| Law | Barghest itself | They are the district's police; the Prevention Unit is their red-armoured division. `[wiki]` |

---

## 5. Headquarters recommendation

### Primary HQ: **Black Sapphire** — Dogtown (Golden Pacific)

Coordinates: lobby `(-1881.135, -2316.233, 41.005)`; floor 67
`(-1887.597, -2316.295, 344.264)`; floor 99 club/casino
`(-1922.437, -2314.250, 439.766)`. `[game-data]`
`areas.jsonl` `{q303_com_tower_lobby}`, `{q303_com_paradise_technical_floor_guards}`,
`{q303_com_paradise_quest_interactions}`.

Rationale:

1. **It is the canon HQ, named as such in the organisation infobox.**
   `|headquarters = [[Black Sapphire]], [[Dogtown]]`, and it is Hansen's
   listed residence. No other faction candidate has that. `[wiki]`
2. **The game gives it three real management levels.** Ground floor =
   warehouses, barracks and mess hall; floor 67 = maintenance and the
   unlicensed bridges between the four towers; floor 99 = club, casino,
   restaurant and AV pads. That is an org seat with rooms to assign, not a
   single venue. `[wiki]` `[game-data]`
3. **It maps 1:1 to the faction's elite revenue.** Gambling, hospitality,
   food and the deal-brokering that *is* Barghest's power play all happen on
   floor 99, with 154 Barghest records on the tower's own areas.
4. **The densest cluster in Dogtown is in range.** Heavy Hearts is 322 m,
   the west gate 200 m, the north gate 600 m, the stadium 700 m. The Sapphire
   is the geometric centre of the faction's whole economy.
5. **The nearest CC is already Barghest-owned and 47.5 m away**
   (`cc_dt_black_sapphire`, owner fid 10), and the sub-territory display name
   is already correct.
6. **It is a fortress by lore.** "An impenetrable fortress, a palace where he
   can play King of Dogtown". A capture here is a decapitation, not a raid.
   `[wiki]`

Trade-off: the tower is 99 floors and 415 m tall, so the anchor is a lobby
point, not a building centroid; a capture radius has to be horizontal and the
floor-99 club (z ≈ 440) is effectively a separate interior. Recommend treating
floor 99 as an interior sub-point (see §7).

### Alternate 1: **EBM Petrochem Stadium** — Dogtown

Coordinates `(-1412.888, -2012.373, 71.860)` (bowl);
`(-1403.125, -1999.162, 72.523)` (market).
`[game-data]` `areas.jsonl` `{q301_com_stadium}`,
`{q304_com_stadium_escape_kurts_soldiers_market}`.

The economy itself: the West Coast's largest black market, the armory, the
power plant and the main smuggling garage, with 201 Barghest records in the
stadium cluster. It loses only because the wiki is explicit that the Sapphire
is the seat and because the stadium complex has **no occupancy site row at
all** — its ownership is proven by quest communities, which is weaker than a
`default_faction_id` + roster join.

### Alternate 2: **Heavy Hearts** — Dogtown (Golden Pacific)

Coordinates `(-1606.430, -2341.452, 43.070)` `[game-data]` site 358.

The best-recorded interior Barghest holds: 49 roster units and eight named
doors (§3 #4). It is also the faction's diplomatic face — Mr. Hands operates
out of it, and it is "neutral ground" for the district's elite. It loses
because the club is not Hansen's seat and because ownership is a garrison,
not title.

### Overruled / downgraded suggestions

- **The stadium as HQ.** It is Dogtown's "beating heart", but it is also the
  battlefield of *Firestarter* and the place where Hansen dies. A seat that
  the campaign destroys is a poor persistent HQ; keep it as rank 2.
- **Dogtown west gate as HQ.** It is the seed's active Barghest control
  centre (`cc_dt_main_gate`, `is_active=1`), so it is *cheap* — but a
  checkpoint has no rooms and no economy of its own. Keep as rank 6.
- **Terra Cognita.** Not Barghest ground: the wiki lists Scavengers and the
  seed gives it to the Voodoo Boys. Do not seed.
- **Longshore Stacks as HQ.** The faction has "an influential presence" there,
  but the wiki is explicit that the neighbourhood is "more autonomous", with
  Briana Dolson as the locally chosen representative. A seat there would
  misrepresent both.

---

## 6. Priority list of control points

Ranked by how well each place serves as a capturable Barghest control point.
"CC" = nearest entry in `data/control_centers.json`; distance is horizontal
metres, computed over **all** CCs regardless of `is_active`, with the CC's
current owner id in brackets (10 = Barghest, 5 = Voodoo Boys, 6 = Animals).

| Rank | Control point | Rel. (1–5) | District / sub-district | Coordinates | Existing CC overlap | Why |
| ---: | --- | :---: | --- | --- | --- | --- |
| 1 | **Black Sapphire** | 5 | Dogtown / Dogtown | `-1881.135, -2316.233, 41.005` | `cc_dt_black_sapphire`, 47.5 m (10) | Canon HQ; floor-99 club/casino/restaurant; 154 records in the tower; fortress |
| 2 | **EBM Petrochem Stadium** | 5 | Dogtown / Dogtown | `-1412.888, -2012.373, 71.860` | `cc_cvi_east_overpass`, 347.2 m (6) | The black market and the faction's cash engine; 201 records in the cluster |
| 3 | **Nighthawks Rehabilitation Center (Hansen Armory)** | 5 | Dogtown / Dogtown | `-1379.057, -1939.644, 87.477` | `cc_cvi_east_overpass`, 268.6 m (6) | The faction's own factory; the one place that proves "arms dealer" rather than "gang" |
| 4 | **Heavy Hearts** | 5 | Dogtown / Dogtown | `-1606.430, -2341.452, 43.070` | `cc_dt_terra_cognita`, 251.4 m (5) | Richest owned interior (49 units, 8 named doors); fixer brokerage; elite nightlife |
| 5 | **The Tunnel** (Dogtown Tunnel) | 4 | Dogtown / Dogtown | `-2326.107, -2557.094, 14.179` | `cc_dt_longshore_stacks`, 14.5 m (10) | The smuggling artery; nearly free (CC is 15 m away and Barghest-owned) |
| 6 | **Dogtown west gate** | 4 | Dogtown / Dogtown | `-2033.521, -2349.511, 18.794` | `cc_dt_main_gate`, 48.5 m (10) | The Prevention Unit's checkpoint; customs and extortion; already an active CC |
| 7 | **Dogtown north gate** | 4 | Pacifica / Coastview | `-1302.500, -1726.000, 45.750` | `cc_cvi_east_overpass`, 88.8 m (6) | The cargo/outsider entrance; 86 records; outside the wall, so captures read as a border fight |
| 8 | **Stadium Underground Parking** | 3 | Dogtown / Dogtown | `-1454.540, -2139.720, 30.350` | `cc_dt_terra_cognita`, 331.0 m (5) | Enclosed smuggling staging under the stadium; adds a second stadium level without duplicating rank 2 |
| 9 | **Pacifica NCPD Precinct** | 3 | Pacifica / Coastview | `-2215.200, -2289.278, 12.030` | `cc_dt_main_gate`, 154.5 m (10) | Dodger's base; a real garrison interior; low economic weight |

### Test control point for the first in-game test: **Heavy Hearts (site 358)**

Why this and not the HQ or a gate:

- **Clean ownership.** `default_faction_id = 10`, 49 roster units, and the
  doors themselves are named after the club (`#sts_ep1_06_heavy_hearts_entrance_doors`).
  Who is being evicted is unambiguous. `[game-data]`
- **The richest record set of any Barghest interior.** Eight named doors
  (entrance, VIP, booth 6, staff room, techie room, backroom elevator) plus a
  10-entry ground-floor and an 18-entry guard community. That is a real
  multi-room building, so a capture trigger radius can be validated against
  geometry.
- **It is a distinct, enclosed interior** with a correct seed
  (`sub_territory_id 92`, Black Sapphire Plaza / Golden Pacific), unlike the
  stadium factory whose seed sub-territory is the wrong one (63, Coastview).
- **It is not the HQ**, so the first test exercises capture on a non-seat.
- **Fallback:** if the test must be on indisputably *owned* property rather
  than a garrisoned club, use the **Nighthawks Rehabilitation Center**
  (site 359, 20 elite units including `Character.sts_ep1_07_kurt_officer`,
  a sniper and an enforcer) — but budget for fixing that site's sub-territory.

Trade-off: the nearest CC is `cc_dt_terra_cognita`, 251 m away and owned by
the **Voodoo Boys**. The seed relocates the faction's active CC
(`cc_dt_main_gate`) onto the test point, which strands the west gate without a
control centre; retarget `cc_dt_terra_cognita` (the misplaced VDB one) instead
and the cost disappears.

---

## 7. Per-sub-district count of lore-relevant locations

This is the number to feed yield balancing. It counts **distinct named places**
Barghest owns, runs or garrisons as a base — not quest corridors and not
generic occupied blocks (`METHOD.md` §1.2 item 9). `Filler` is the deduped
occupied-site count minus any site already counted as a named place.

| Sub-district | Named lore-relevant places | Which ones | Barghest-occupied sites (deduped) | Filler | Noteworthy interiors |
| --- | ---: | --- | ---: | ---: | ---: |
| Dogtown | **7** | Black Sapphire, EBM Petrochem Stadium, Nighthawks Rehabilitation Center, Heavy Hearts, The Tunnel, Stadium Underground Parking, Dogtown west gate | 3 | 1 | 7 (tower ×3 levels, stadium market, factory, club, garage) |
| Coastview | **2** | Dogtown north gate, Pacifica NCPD Precinct | 1 | 0 | 1 (precinct) |
| **Total** | **9** | | 4 | 1 | 8 |

Reconciliation:

- 9 named + 1 filler = 10.
- 4 deduped occupied sites + 6 area/community-only named places = 10. ✓
- 3 of the 9 named are site-backed (Heavy Hearts = 358, Armory = 359,
  precinct = 361); the other 6 are community-only (Black Sapphire, Stadium,
  Tunnel, Parking, West gate, North gate).
- The single filler is site 362, the Luxor spa, whose only Barghest record is
  a courier. It is arguably not a holding at all; counting it as filler is the
  generous reading.

**Neighbourhood breakdown (for yield tuning, not for the JSON contract).**
Dogtown's single `gamedata_subdistrict` hides four very different economies:

| Dogtown neighbourhood `[wiki]` | Named holdings | Character |
| --- | ---: | --- |
| Golden Pacific | 2 (Black Sapphire, Heavy Hearts) | The elite/deal-making economy; highest per-point value |
| Stadium | 3 (Stadium, Armory, Underground Parking) | The industrial and smuggling economy; biggest unit mass |
| Longshore Stacks | 1 (The Tunnel) | Logistics only; the neighbourhood itself is autonomous |
| Gates (wall) | 2 (west, north) | Tolls, customs, security |
| Luxor Heights / Terra Cognita | 0 | Barghest presence is airdrop zones and patrols only; scavengers and the Voodoo Boys hold the buildings |

**Reading the numbers.** Nine named points is a *small* catalog for a faction
with 1,449 NPCs, and that is the honest answer: Barghest does not run shops, it
runs one army with one market, one factory, one tunnel and one club. The
remaining 681 records are quest corridors (the *Dog Eat Dog* run-off tunnels,
*Firestarter*'s stadium escape, sandbox-activity waves) that a capture model
should treat as **defence density**, not as places to own.

If more capture points are needed, the honest lever is **interior sub-points,
not new names**: Black Sapphire alone has three distinct levels 300 m apart
vertically (z ≈ 41, 344, 440), the stadium has four (bowl 72, factory 87,
garage 30, deal room 64), and the market is a separate 60 m-wide level from
the bowl.

---

## 8. Gaps and uncertainties

1. **The method's sub-district attribution does not work for Phantom Liberty
   at all.** `METHOD.md` §3.3's token map has no `ep1`, `q30x`, `sa_ep1` or
   `sts_ep1` entries, and `SD` has no Dogtown value, so every Dogtown row
   resolves to `nearest-subterritory` — i.e. to one of five seeded centroids.
   This doc attributed by hand: quest-id/community-name, then the wiki
   neighbourhood, then seed sub-territory. A `dtn`/`ep1` token rule is needed
   before any other Dogtown faction is run.
2. **Dogtown's centroid snapping is circular, not incidental.** Twelve rows
   sit exactly on a `dt_*` centroid, and in every case the sub-territory was
   evidently seeded *from* that row (the Sapphire lobby, the gate, the ICA
   loops, the crash site). METHOD §1.1 item 6 says "a coordinate equal to a
   centroid is not evidence: use `TBD`". Applied literally here, it discards
   the four best Dogtown anchors. The rule needs an exception: when the
   sub-territory's display name matches the place, treat the match as seed
   provenance and fall back to the nearest non-snapped sibling node — which is
   what I did for the Sapphire (47.5 m), the west gate (48.5 m) and the tunnel
   (14.5 m).
3. **`dt_luxor_heights` (95) is misnamed and misplaced.** Its display name is
   "Luxor High Wellness Spa" but its centroid is the *Space Force One crash
   site* at `(-2134.3, -2692.7)`, 780 m from the real spa. The real spa is
   `dt_terra_cognita` (94), which the seed gives to the Voodoo Boys, and 94's
   display name is the correct one. Two sub-territories share one name; one is
   wrong.
4. **The seed has no Dogtown sub-territory for the stadium.** `sts_ep1_07`
   (the armory) is seeded `district_id 5`, `sub_territory_id 63` (Coastview
   East Overpass) and `sts_ep1_12` (the spa) to sub 94. The stadium's own
   communities are all `district_code dogtown`, and the wiki says the main
   entrance is "in Dogtown proper". Either add a stadium sub-territory or
   retarget 63.
5. **Both gates are documented in Coastview, but only the north gate lands
   there by position.** The wiki says both main entrances are "located in the
   Coastview sub-district". The wiki's west gate (east of the abandoned NCPD
   precinct) sits inside the Dogtown bbox and inside the seeded
   `dt_main_gate`, so I attributed it to Dogtown. One of the two sources is
   wrong; the map will show which.
6. **`sts_ep1_10` (Dodger's precinct) is a Coastview building seeded as a
   Dogtown holding.** The site is `district_id 8`, `sub_territory_id 91`
   (Dogtown), but the wiki, the position (west of the western gate) and the
   gig infobox all put it in Coastview. It is a real Barghest base; only its
   seed placement is wrong.
7. **The stadium factory's site anchor is 78 m from its garrison.**
   `sts_ep1_07` anchors at `(-1401.314, -2013.167)`, while its enemies and
   reinforcement communities are at `(-1379…-1407, -1939…-1947)`. I used the
   community. This is METHOD §1.1 item 7 again, and it is the third faction in
   a row where a site anchor is the worst available coordinate.
8. **No wiki infobox carries a coordinate, and Dogtown location pages have no
   `baseid`.** METHOD §1.1 item 1's "wiki `baseid` is the best identity join"
   works only for *gigs* here. The useful chain turned out to be: gig
   `baseid` → `sites.json` code → the site's door node names. That is how
   Heavy Hearts was proven, and it should be written into the method.
9. **The airdrop metaquest ids are an undocumented coordinate source.**
   `sa_ep1_*` communities in `areas.jsonl` are the wiki's named airdrop
   locations. They are the only way I could put Wild Blue, Los Osos Motel,
   High Peak, Tranquil Terrace, Brave Atlas, Undersea Reverie and
   Montezuma's Throne on the map at all. They locate a *zone*, not a building.
10. **The single biggest Barghest concentration is unnamed.** `{q301_com_wtc_run_off_}01`
    holds 95 entries (50 Barghest) at `(-1970.068, -2362.305, 3.438)`, under
    the Golden Pacific near the Sapphire, plus a second run-off node 26
   entries/16 units at `(-1716.5, -2668.9)`. It is a *Dog Eat Dog* escape
   corridor, so per METHOD it belongs here, not in the catalog — but it means
   681 of 1,449 Barghest records are invisible to the §7 count. If capture
   difficulty should scale with troop density, this table is the input.
11. **`{mq301_com_initiation}` (42 Barghest) is the only mass at the Golden
    Pacific roundabout** — `(-1834.646, -2314.871, 39.791)`. It is very likely
    the Needle/roundabout initiation scene, but the record names a scene, not
    the obelisk. The Needle stays `TBD` and is not seeded.
12. **`sts_ep1_06` contains an `_com_fake_barghest_guard` community (18
    records).** In *Heaviest of Hearts* the player can impersonate Barghest.
    Those 18 records are part of a disguise set-piece, not extra garrison, so
    the 49-unit roster count overstates the club's defenders by up to 18.
13. **No vendor inventory exists in the extract.** "What Heavy Hearts sells"
    comes from its in-game pamphlet (XXX BDs, liquors, stimulants, VIP rooms)
    and "what the market sells" from the wiki vendor list, not from vendor
    data. Every price-sensitive claim in §4 is `[wiki]`.
14. **`is_interior` is 0 for every Dogtown site.** All nine `interior: true`
    values rest on node names (rooms, floors, lifts, doors), not the flag.
15. **Two Dogtown business names collide with existing Night City assets.**
    `los_osos` (Coastview homeless camp) and `eden_plaza`/`wild_blue`
    (Charter Hill) exist in the extract; none of them is the Dogtown business
    of the same name. This is a new trap for METHOD §2.3 and it is the
    easiest way to misplace a Golden Pacific bar by 4 km.

---

## 9. Sources

- Local: `dist/extract/areas.jsonl` (510 `dogtown` rows, 187 with Barghest),
  `dist/extract/markers.jsonl` (checked; carries almost no Dogtown names),
  `data/sites/{sites,communities,rosters,doors,suitabilities}.json`,
  `data/{districts,factions,control_centers,sub_territories,landmarks,faction_headquarters}.json`,
  `dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_{0,1,2}.streamingsector.json`
  (prefab and node-name strings only; `combat_zone_prefabUEX7DCY` subtree).
- Wiki: [BARGHEST](https://cyberpunk.fandom.com/wiki/BARGHEST),
  [Dogtown](https://cyberpunk.fandom.com/wiki/Dogtown),
  [Black Sapphire](https://cyberpunk.fandom.com/wiki/Black_Sapphire),
  [EBM Petrochem Stadium](https://cyberpunk.fandom.com/wiki/EBM_Petrochem_Stadium),
  [Nighthawks Rehabilitation Center](https://cyberpunk.fandom.com/wiki/Nighthawks_Rehabilitation_Center),
  [Hansen Armory](https://cyberpunk.fandom.com/wiki/Hansen_Armory),
  [Kurt Hansen](https://cyberpunk.fandom.com/wiki/Kurt_Hansen),
  [Heavy Hearts](https://cyberpunk.fandom.com/wiki/Heavy_Hearts),
  [Heavy Hearts pamphlet](https://cyberpunk.fandom.com/wiki/Heavy_Hearts_pamphlet),
  [Dogtown Gate](https://cyberpunk.fandom.com/wiki/Dogtown_Gate),
  [Dogtown Tunnel](https://cyberpunk.fandom.com/wiki/Dogtown_Tunnel),
  [Stadium Underground Parking](https://cyberpunk.fandom.com/wiki/Stadium_Underground_Parking),
  [Pacifica NCPD Precinct](https://cyberpunk.fandom.com/wiki/Pacifica_NCPD_Precinct),
  [Golden Pacific](https://cyberpunk.fandom.com/wiki/Golden_Pacific),
  [Longshore Stacks](https://cyberpunk.fandom.com/wiki/Longshore_Stacks),
  [Luxor Heights](https://cyberpunk.fandom.com/wiki/Luxor_Heights),
  [Terra Cognita](https://cyberpunk.fandom.com/wiki/Terra_Cognita),
  [Airdrops](https://cyberpunk.fandom.com/wiki/Cyberpunk_2077_Airdrops),
  [Gig: Heaviest of Hearts](https://cyberpunk.fandom.com/wiki/Gig:_Heaviest_of_Hearts),
  [Gig: Roads to Redemption](https://cyberpunk.fandom.com/wiki/Gig:_Roads_to_Redemption),
  [Gig: Waiting for Dodger](https://cyberpunk.fandom.com/wiki/Gig:_Waiting_for_Dodger),
  [Increased Criminal Activity: BARGHEST](https://cyberpunk.fandom.com/wiki/Increased_Criminal_Activity:_BARGHEST),
  [You Know My Name](https://cyberpunk.fandom.com/wiki/You_Know_My_Name),
  [Firestarter](https://cyberpunk.fandom.com/wiki/Firestarter),
  [Run This Town](https://cyberpunk.fandom.com/wiki/Run_This_Town),
  [Lucretia My Reflection](https://cyberpunk.fandom.com/wiki/Lucretia_My_Reflection),
  [The Needle](https://cyberpunk.fandom.com/wiki/The_Needle),
  [The Scraper](https://cyberpunk.fandom.com/wiki/The_Scraper),
  [Paradise Hotel](https://cyberpunk.fandom.com/wiki/Paradise_Hotel).
- Earlier repo research: `docs/research/factions/voodoo-boys.md` (Dogtown
  Luxor/Eventide cluster), `docs/research/factions/METHOD.md`,
  `docs/research/factions-gangs-territories.md`.

---

## 10. Machine-readable block

Strict JSON for seeding (contract in [`METHOD.md`](./METHOD.md) §10). Every
coordinate was re-verified against the local record named in `source` on
2026-11-25; none came from the wiki.

```json
{
  "faction_code": "barghest",
  "hq": {"name": "Black Sapphire", "district": "Dogtown", "sub_district": "Dogtown", "x": -1881.135, "y": -2316.233, "z": 41.005, "source": "dist/extract/areas.jsonl {q303_com_tower_lobby} (hash 8039314437540013265)", "confidence": "game-data+wiki"},
  "alternate_hqs": [
    {"name": "EBM Petrochem Stadium", "district": "Dogtown", "sub_district": "Dogtown", "x": -1412.888, "y": -2012.373, "z": 71.86, "source": "dist/extract/areas.jsonl {q301_com_stadium} (hash 3228696072169438974)", "confidence": "game-data+wiki"},
    {"name": "Heavy Hearts", "district": "Dogtown", "sub_district": "Dogtown", "x": -1606.43, "y": -2341.452, "z": 43.07, "source": "data/sites/sites.json site 358 sts_ep1_06", "confidence": "game-data+wiki"}
  ],
  "test_control_point": {"name": "Heavy Hearts", "district": "Dogtown", "sub_district": "Dogtown", "x": -1606.43, "y": -2341.452, "z": 43.07, "source": "data/sites/sites.json site 358 sts_ep1_06", "confidence": "game-data+wiki"},
  "control_points": [
    {"rank": 1, "name": "Black Sapphire", "type": "hotel_hq", "relevance": 5, "district": "Dogtown", "sub_district": "Dogtown", "x": -1881.135, "y": -2316.233, "z": 41.005, "source": "dist/extract/areas.jsonl {q303_com_tower_lobby} (hash 8039314437540013265); floor 99 {q303_com_paradise_quest_interactions} -1922.437,-2314.250,439.766", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["gambling", "food_drink", "hospitality", "fixer_brokerage", "information"], "nearest_cc_code": "cc_dt_black_sapphire", "nearest_cc_m": 47.5},
    {"rank": 2, "name": "EBM Petrochem Stadium", "type": "stadium_black_market", "relevance": 5, "district": "Dogtown", "sub_district": "Dogtown", "x": -1412.888, "y": -2012.373, "z": 71.86, "source": "dist/extract/areas.jsonl {q301_com_stadium} (hash 3228696072169438974); market {q304_com_stadium_escape_kurts_soldiers_market} -1403.125,-1999.162,72.523", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["retail", "arms", "cyberware", "smuggling", "protection", "energy"], "nearest_cc_code": "cc_cvi_east_overpass", "nearest_cc_m": 347.2},
    {"rank": 3, "name": "Nighthawks Rehabilitation Center (Hansen Armory)", "type": "weapons_factory", "relevance": 5, "district": "Dogtown", "sub_district": "Dogtown", "x": -1379.057, "y": -1939.644, "z": 87.477, "source": "dist/extract/areas.jsonl {sts_ep1_07_enemies_com} (hash 14963247986057934468)", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["arms", "manufacturing", "rnd"], "nearest_cc_code": "cc_cvi_east_overpass", "nearest_cc_m": 268.6},
    {"rank": 4, "name": "Heavy Hearts", "type": "nightclub", "relevance": 5, "district": "Dogtown", "sub_district": "Dogtown", "x": -1606.43, "y": -2341.452, "z": 43.07, "source": "data/sites/sites.json site 358 sts_ep1_06 (doors #sts_ep1_06_heavy_hearts_entrance_doors)", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["food_drink", "braindance", "sex_work", "drugs", "fixer_brokerage", "hospitality"], "nearest_cc_code": "cc_dt_terra_cognita", "nearest_cc_m": 251.4},
    {"rank": 5, "name": "The Tunnel", "type": "smuggling_tunnel", "relevance": 4, "district": "Dogtown", "sub_district": "Dogtown", "x": -2326.107, "y": -2557.094, "z": 14.179, "source": "dist/extract/areas.jsonl {we_ep1_01_q302_combat_com} (hash 12713071501951577929)", "confidence": "game-data+wiki+inferred", "interior": true, "revenue_streams": ["smuggling", "logistics"], "nearest_cc_code": "cc_dt_longshore_stacks", "nearest_cc_m": 14.5},
    {"rank": 6, "name": "Dogtown west gate", "type": "checkpoint", "relevance": 4, "district": "Dogtown", "sub_district": "Dogtown", "x": -2033.521, "y": -2349.511, "z": 18.794, "source": "dist/extract/areas.jsonl {q302_cz_gate} (hash 17435183680842590867)", "confidence": "game-data+wiki", "interior": false, "revenue_streams": ["protection", "security_services"], "nearest_cc_code": "cc_dt_main_gate", "nearest_cc_m": 48.5},
    {"rank": 7, "name": "Dogtown north gate", "type": "checkpoint", "relevance": 4, "district": "Pacifica", "sub_district": "Coastview", "x": -1302.5, "y": -1726.0, "z": 45.75, "source": "dist/extract/areas.jsonl {q301_com_border_combat_gate} (hash 7242737884370904763)", "confidence": "game-data+wiki", "interior": false, "revenue_streams": ["protection", "security_services"], "nearest_cc_code": "cc_cvi_east_overpass", "nearest_cc_m": 88.8},
    {"rank": 8, "name": "Stadium Underground Parking", "type": "garage", "relevance": 3, "district": "Dogtown", "sub_district": "Dogtown", "x": -1454.54, "y": -2139.72, "z": 30.35, "source": "dist/extract/areas.jsonl {q304_com_stadium_escape_kurts_soldiers_garage} (hash 3090696465833105295)", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["smuggling", "logistics"], "nearest_cc_code": "cc_dt_terra_cognita", "nearest_cc_m": 331.0},
    {"rank": 9, "name": "Pacifica NCPD Precinct", "type": "base", "relevance": 3, "district": "Pacifica", "sub_district": "Coastview", "x": -2215.2, "y": -2289.278, "z": 12.03, "source": "data/sites/sites.json site 361 sts_ep1_10", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["security_services", "mercenary"], "nearest_cc_code": "cc_dt_main_gate", "nearest_cc_m": 154.5}
  ],
  "subdistrict_counts": {
    "Dogtown": {"named": 7, "filler": 1},
    "Coastview": {"named": 2, "filler": 0}
  }
}
```
