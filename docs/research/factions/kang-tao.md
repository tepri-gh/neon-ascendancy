# Kang Tao — Lore-Relevant Control Points

Status: faction research run, 2026-11-25. One faction, one document.
Scope: replace the generic control-centre grid with places Kang Tao actually
owns, runs, protects or garrisons in Night City, with verified coordinates, an
economic map, an HQ pick, a ranked capture list and honest per-sub-district
counts. Method: this doc conforms to [`METHOD.md`](./METHOD.md) §1.1 (batch-1
corrections) and the corp method in §5. `AGENTS.md` was read first. No commits,
no game launch.

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Position, site, community, roster or spawn record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/artbook/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My reasoning links a named place to a game record; reasoning stated | Weak, flagged |

No coordinate below is guessed. Every `(x, y, z)` is copied from a local marker,
site or seed anchor record, or marked `TBD`.

**Up front, because it shapes every section:** Kang Tao is one of the thinnest
corp footprints in the extract — **4 roster sites / 24 units, 17 community
areas, 2 seeded sub-territories**. There is exactly **one** wiki-documented
Kang Tao building in Night City (the Corporate Plaza headquarters) and no
Kang Tao retail storefront, factory, lab or warehouse anywhere in the game. Most
of the in-game Kang Tao presence is them **appearing as the enemy in someone
else's story**: Panam's Badlands AV ambush, a 6th Street gig, and an NCPD hustle
in Corpo Plaza. This doc reports that honestly rather than padding the catalog
with set pieces dressed up as holdings.

---

## 1. Summary

Kang Tao (康陶) is a Chinese weapons megacorp: 1,000,000 employees and €$525
billion in 2077, restructured in 2050 by Colonel Shiming Xu, headquarters in
Shenyang, China. Its business is firearms — above all Smart-class weapons
("gyrojet technology… caseless guided ammunition") — plus a growing mercenary
and security arm. It is the world's leading Smart-weapon manufacturer and
Arasaka's closest competitor in that niche. `[wiki]`

Its Night City presence is a single Corporate Plaza office tower plus contract
security details, not a business empire:

- **Corpo Plaza (City Center)** — the **Kang Tao Building**, explicitly the
  *North American Division HQ / Regional HQ*, next to Petrochem Tower, reached
  by a bridge from Memorial Park. This is the only wiki-documented Kang Tao
  address in the city. `[wiki]`
- **Glen (Heywood)** — a seeded holding, "Hanford Overpass", with 9 armed Kang
  Tao rangers, androids and an officer standing on it. The seed name is ours,
  not lore (§8.1). `[game-data]`
- **Arroyo (Santo Domingo)** — Kang Tao agents appear as the third party in the
  *Nasty Hangover* gig: Karl Ginsky's stolen datashard, a 6th Street warehouse,
  and a Kang Tao kill team that arrives to clean up. `[game-data]` `[wiki]`
- **Badlands (Jackson Plains / Biotechnica Flats)** — the *Lightning Breaks* and
  *Life During Wartime* AV ambush: Satwave Power Plant, the crashed AV site, and
  the SovOil fuel station where Hellman's Kang Tao escort holes up. `[wiki]`

Game-data scale: **17 community areas** contain Kang Tao spawns (**16**
Kang Tao-dominant), **14 spawn points**, **4 roster sites / 24 units**, **2
owned sub-territories**, and **10 distinct security character records**
(`cpz_kangtao_*`, `gle_kangtao_*`, `sts_std_arr_06_*`). `[game-data]`

For scale: Arasaka has 146 areas and 12 owned sub-territories; Militech 136 and
10. Kang Tao's 17 areas are the smallest of the five megacorps studied. `[game-data]`

---

## 2. Territory

### 2.1 Districts

| Evidence kind | Result |
| --- | --- |
| (a) Wiki/lore | Global HQ Shenyang, China. Night City **North American Division HQ** is the Kang Tao Building, Corporate Plaza, City Center. Retreats to a Badlands fuel station in *Life During Wartime*; runs an AV-extraction corridor through the southern Badlands. `[wiki]` |
| (b) Vanilla map gang panel | **Not applicable.** `data/districts.json` `vanilla_gangs` lists street gangs only; megacorps are absent by design. `[game-data]` |
| (c) Game-data counts | 17 areas contain Kang Tao (16 dominant); 4 roster sites / 24 units; 2 owned sub-territories; 14 faction-22 spawn points across 8 sub-territories. `[game-data]` |

The two owned sub-territories (`data/sub_territories.json`,
`initial_owner_faction_id = 22`): **`cpz_kang_tao_sector`** "Kang Tao North
Tower" (CorpoPlaza, income 1250, defence 85) and **`gle_hanford_overpass`**
"Hanford Overpass" (Glen, income 880, defence 60). Only the first is
lore-plausible; the second is a seed invention around a real Kang Tao encounter
(§8.1). `[game-data]`

### 2.2 Sub-district presence

Counts are from `dist/extract/areas.jsonl` (areas whose `faction_counts`
contains `kang_tao`; "dominant" means `dominant_faction == kang_tao`) and
`data/sites/rosters.json` (`faction_id == 22`). Occupied sites are deduped
`data/sites/sites.json` rows with `default_faction_id == 22` **or** at least one
Kang Tao roster entry; no pair is within 25 m. Attribution follows METHOD §3.3
plus the `awf`/`morro` additions from §1.1.

| Sub-district | District | (a) Lore | (b) Panel | (c) Areas (dominant) | (c) KT entries | Occupied sites |
| --- | --- | --- | --- | ---: | ---: | ---: |
| CorpoPlaza | CityCenter | **North American HQ** | — (corp) | 3 (3) | 11 | 2 |
| Badlands | Badlands | AV ambush, fuel station | — | 7 (7) | 31 | 0 |
| Glen | Heywood | seeded holding | Valentinos | 2 (2) | 10 | 1 |
| Arroyo | SantoDomingo | *Nasty Hangover* warehouse | 6th Street | 2 (2) | 7 | 1 |
| RanchoCoronado | SantoDomingo | Satwave approach | 6th Street | 2 (2) | 7 | 0 |
| Downtown | CityCenter | PL courier scene | — | 1 (1) | 4 | 0 |

\* **RanchoCoronado is an attribution artefact, not a holding.** The two rows
(`{q104_com_pplant_drones}` 3 entries, `{#q104_com_av_drones}` 3 entries) are
the Satwave power-plant drone fight and the AV drone chase. They sit at
`(-206, -2794)` and `(-257, -3341)`, 655 m from the nearest seeded sub-territory
centroid (`rcr_almunecar_strip`) and outside every geocoded site, so §3.3's
third fallback files them under RanchoCoronado. The wiki puts Satwave in
**Jackson Plains**, and `data/districts.json` puts both points in **Badlands**.
Treat them as `Badlands`.

### 2.3 Attribution caveat

Four distinct failure modes for this faction:

1. **Badlands rows have no geocoded site or token**, so §3.3's
   `nearest-subterritory` fallback decides them. Nine of the 17 rows needed it.
   They are Badlands in fact; two land in RanchoCoronado and are wrong.
2. **`{ma_cct_cpz_16_com}` is labelled `watson`** in `district_code` but sits at
   `(-1118, 554)` in Corpo Plaza, 3.4 km from the Watson bbox. Path token
   inheritance, exactly the §2.2 defect.
3. **`{sa_ep1_201_com_combat}` / `{sa_ep1_203_com_combat}`** are Phantom Liberty
   *courier-loop* combat areas labelled `city_center`; they resolve to Downtown
   (122 m) and VistaDelRey (156 m) by nearest site. Neither has a Kang Tao unit
   in `sites.json` — the `sa_ep1_courier_loop_enemies_kangtao_*` records exist
   only in the raw sector (§2.2). Presence, not ownership.
4. **`q104` is one quest, four places.** `q104_com_petro_gas_station`,
   `q104_com_gas_station_reinforcements`, `q104_com_gas_station_paramedic`,
   `q104_com_airstrip_combat`, `q104_com_av_pilot`,
   `q104_com_petrochem_operators`, `q104_com_pplant_drones` and
   `{#q104_com_av_drones}` span Satwave (Jackson Plains), the AV crash site, the
   fuel station and the old airstrip — hundreds of metres to kilometres apart.
   Never aggregate `q104` by prefix.

---

## 3. Location catalog

Coordinates are world-space metres, `Z` up. "Interior?" means the game has a
distinct interior cell or room volume. "Business?" is what the place earns or
provides, not a vendor inventory (the extract has no vendor data).

| # | Name | Type | District / sub-district | Interior? | Business? (what it earns) | Coordinates (x, y, z) | Coordinate source record | Linked communities / sites | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **Kang Tao Building** (North American Division HQ) | Corporate HQ / office skyscraper | CityCenter / CorpoPlaza | No distinct cell found; office tower interior, no doors/nodes in extract | Arms sales, Smart-weapon R&D, regional administration, security contracts | `-1127.822, 546.952, 17.890` (site anchor); community `-1118.182, 554.060, 18.601` | `data/sites/sites.json` site 20 `ma_cct_cpz_16`; `data/sites/communities.json` `{ma_cct_cpz_16_com}` | CC `cc_cpz_kang_tao_sector` (12.0 m); 5-entry Kang Tao community; roster `Character.cpz_kangtao_soldier2_*`, `cpz_kangtao_ranger1_*` | `[game-data]` `[wiki]` |
| 2 | **Hanford Overpass** (seeded holding) | Overpass / street encounter | Heywood / Glen | No (`is_interior=0`, `has_doors=0`) | None documented — an ambush site, not a business | `-1410.732, -1208.607, 26.723` | `data/sites/sites.json` site 60 `ma_hey_gle_15`; CC `cc_gle_hanford_overpass` (5.3 m, `is_active=1`) | 9-entry Kang Tao community (rangers, 3 androids, officer); 7 patrol splines | `[game-data]` (name `[inferred]`, §8.1) |
| 3 | **6th Street warehouse (Nasty Hangover)** | Warehouse interior | SantoDomingo / Arroyo | **Yes** (`is_interior=1`, `has_doors=1`, main gate + roof door) | None for Kang Tao — a 6th Street stash holding a stolen Kang Tao shard | `-573.614, -1182.899, 7.701` | `data/sites/sites.json` site 382 `sts_std_arr_06` | 11-entry 6th Street community + `arr_06_com_corpo` (Kang Tao detail) + `arr_06_reinforcements_kang_tao_com`; `#arr_06_guard_area_kang_tao` | `[game-data]` `[wiki]` |
| 4 | **Satwave Power Plant** | Power plant / microwave receiver | Badlands / Badlands | Partly — control station and terminal rooms | None for Kang Tao. City power infrastructure; the EMP is fired here | `-195.302, -2838.326, 22.799` (`q104_pplant_cooling_terminal_marker`); antenna `-207.899, -2832.157, 20.662` | `dist/extract/markers.jsonl` `q104_pplant_cooling_terminal_marker` | `{q104_com_pplant_drones}` (4 KT); `#q104_pr_power_plant` prefab | `[game-data]` `[wiki]` |
| 5 | **SovOil Fuel Station (Highway 101)** | Fuel station + workshop + store | Badlands / Badlands | Yes — workshop and store rooms | Fuel retail (`SovOil`, not Kang Tao); Kang Tao escort uses it as a safehouse | `-1815.323, -4282.463, 74.249` (`q104_07_sm_gas_station_chats`); building `-1836.568, -4269.404, 74.025` | `dist/extract/markers.jsonl` `q104_07_sm_gas_station_chats`, `q104_mp_gas_station_building` | `{q104_com_petro_gas_station}` (10 KT), `{q104_com_gas_station_reinforcements}` (5), `{q104_com_gas_station_paramedic}` (1); CC `cc_bls_biotechnica_flats` (5.9 m, **Biotechnica**) | `[game-data]` `[wiki]` |
| 6 | **AV crash site** (Life During Wartime) | Crash site | Badlands / Badlands | No — open plains | None; the Kang Tao AV is brought down here | `-669.654, -5006.292, 74.518` (`q104_mp_av_crash`) | `dist/extract/markers.jsonl` `q104_mp_av_crash` | `{q104_com_petroleum_operators}` cluster (7 KT at `-661, -4985`), `{q104_com_av_pilot}` | `[game-data]` `[wiki]` |
| 7 | **Old airstrip** (Jackson Plains Regional Airport) | Abandoned airfield | Badlands / Badlands | No — open runway and ruins | None; Kang Tao agents are tracked through it | `-1276.796, -5208.874, 83.391` (`q104_mp_airstrip_tracks_}000`) | `dist/extract/markers.jsonl` `q104_mp_airstrip_tracks_}000` | `{q104_com_airstrip_combat}` (4 KT); `loc_q104_old_airstrip` prefab | `[game-data]` `[wiki]` `[inferred]` (airport name link) |
| 8 | Corpo Plaza scanner hustle (Militech concourse) | Street encounter | CityCenter / CorpoPlaza | No | None; Kang Tao detail guarding a resource crate near Militech's tower | `-1070.084, 71.217, 7.352` | `data/sites/sites.json` site 19 `ma_cct_cpz_15` | 3-entry Kang Tao community; prefab nodes `#ma_cct_cpz_15_dvc_security_area/_002`, `_security_system/_002` (no `devices.json` rows) | `[game-data]` |

### 3.1 Interior sub-locations (the reason to capture a building)

Only one catalog point has a real interior, and it is **not** Kang Tao's:

**6th Street warehouse (Nasty Hangover)** `[game-data]`

| Sub-location | Coordinates (x, y, z) | Node / marker | Note |
| --- | --- | --- | --- |
| Site anchor / gate | `-573.614, -1182.899, 7.701` | site 382 `sts_std_arr_06` | Fenced yard, `has_doors=1` |
| Karl Ginsky's meeting point | `-508.983, -1216.394, 7.237` | `arr_06_mp_karl` | Where the confrontation happens |
| Shard pickup | `-522.189, -1215.522, 7.169` | `arr_06_mp_chip` | The stolen Kang Tao datashard |
| Main gate | `TBD` | `#arr_06_main_gate` (`door_role: interior`) | `doors.json` carries no position; node name only |
| Roof door | `TBD` | `#arr_06_roof_door` (`door_role: roof`) | Two-storey route; no position in the extract |

Kang Tao has **no** interior of its own in the extract. The Kang Tao Building has
no site node named for a lobby, entrance, floor or atrium, and `ma_cct_cpz_16`
reports `is_interior=0`, `has_doors=0`, `devices=0`, `slots=0`. Its entire
gameplay record is 2 guard areas, 3 triggers and 7 enemy workspots on the plaza
outside. That is the single most important fact for the capture design: **a Kang
Tao HQ control point will be an outdoor plaza volume, not an interior.**

### 3.2 How the name→coordinate links were proven

- **Kang Tao Building** — the wiki infobox gives `type = North American Division
  HQ / Regional HQ`, `owner = Kang Tao`, `district = City Center`,
  `sub_district = Corporate Center`, `location = Corporate Plaza`, and says it is
  next to Petrochem Tower and reached by a bridge from Memorial Park. The
  in-game side is site 20 `ma_cct_cpz_16`: `default_faction_id = 22`,
  `sub_territory_id = 78` (`cpz_kang_tao_sector`, display name "Kang Tao North
  Tower"), CC `cc_cpz_kang_tao_sector` 12 m away and Kang Tao-owned. Site 20 is
  inside that sub-territory, 12 m from its centroid. `[game-data]` `[wiki]`
  It does **not** prove the seed's "North Tower" name: no wiki page, marker,
  prefab path or `gamedataDistrict` enum uses it (§8.1).
- **Hanford Overpass** — site 60 `ma_hey_gle_15` has `default_faction_id = 22`,
  `initial_owner_faction_id = 22`, `control_center_id = 42`, and its prefab is
  `#ma_hey_gle_15_openworld_prefab…`. Its `spots.json` names a
  `#ma_hey_gle_15_ws_6th_street_after` workspot and a
  `#ma_hey_gle_15_6th_street_com` community, and the roster holds one
  `Character.ma_hey_gle_15_6th_street_victim`. So the encounter is **Kang Tao
  versus 6th Street at an overpass**, not a Kang Tao facility. The name
  "Hanford Overpass" is the seed's; there is no Hanford marker or prefab. `[game-data]`
- **Nasty Hangover warehouse** — the wiki infobox gives `baseid = sts_std_arr_06`,
  which is exactly `sites.json` site 382's `code`. Cross-checks: `Objective:
  Retrieve the Kang Tao Datashard stolen from Karl Ginsky`, `location =
  Hargreaves St.`, enemies `6th Street` and `Kang Tao`. The site's own records
  carry `arr_06_mp_karl`, `arr_06_mp_chip`, `#arr_06_guard_area_kang_tao` and a
  `Vehicle.sts_std_arr_06_kangtao_car`. This is the cleanest `baseid` join in
  the set (§1.1 item 1). `[game-data]` `[wiki]`
- **Satwave Power Plant** — `Lightning Breaks` (`baseid = q104_01_sabotage`)
  names [[Satwave Power Plant]] and the objective list reads "Go to the Satwave
  Power Plant / Take out the power plant security / Overheat the terminals". The
  local record is the `q104_pr_power_plant` prefab and
  `q104_pplant_cooling_terminal_marker`; the wiki places the plant in Jackson
  Plains, Santo Domingo's southern Badlands. `[game-data]` `[wiki]`
- **SovOil Fuel Station** — `Life During Wartime` (`baseid = q104_02_av_chase`)
  lists `location = Regional Airport / Fuel Station / Sunset Motel` and says
  Hellman "was brought here by his Kang Tao escort". The local records are
  `q104_07_sm_gas_station_chats` and `q104_mp_gas_station_building`, with
  `q104_courier_gas_station_loc` 17 m away; the wiki page names it
  "SovOil Fuel Station (Highway 101)" on the Biotechnica Flats outskirts.
  `[game-data]` `[wiki]`
- **AV crash site / old airstrip** — `Life During Wartime` says V chases the
  crashing AV "deep into the Jackson Plains", and the wiki's airport page says V
  and Panam "tracked Kang Tao agents through the airport". Local anchors are
  `q104_mp_av_crash` (crash) and `q104_mp_airstrip_tracks_}000` (tracks), with
  `loc_q104_old_airstrip` prefabs. The airport-to-airstrip name link is
  `[inferred]`; the position is `[game-data]`. `[game-data]` `[wiki]` `[inferred]`

### 3.3 Kang Tao-occupied generic sites (the filler pool)

`data/sites/suitabilities.json` tags sites with gameplay affordances. Both of
these are Kang Tao-default sites that are **not** named catalog points; both are
already used as catalog points above, so the honest filler pool for this faction
is **empty** (§7).

| Site | Sub-district | Interior | Suitability tags | Units | Coordinates | Note |
| --- | --- | --- | --- | ---: | --- | --- |
| `ma_cct_cpz_16` | CorpoPlaza | no | rooftop_access 67, raid_target 66, branch_office 45 | 5 | `-1127.822, 546.952, 17.890` | **Named catalog point:** Kang Tao Building; not filler |
| `ma_cct_cpz_15` | CorpoPlaza | no | raid_target 63, branch_office 45 | 3 | `-1070.084, 71.217, 7.352` | **Named catalog point:** Corpo Plaza hustle; not filler |
| `ma_hey_gle_15` | Glen | no | raid_target 95, rooftop_access 76, officer_site 60, hostage_site 50 | 9 | `-1410.732, -1208.607, 26.723` | **Named catalog point:** Hanford Overpass; not filler |
| `sts_std_arr_06` | Arroyo | **yes** | raid_target 93, vehicle_bay 65, branch_office 60, officer_site 60, stealth_entry 60, safehouse 57 | 7 KT (+10 6th Street) | `-573.614, -1182.899, 7.701` | **Named catalog point:** Nasty Hangover warehouse; 6th Street-owned |

There is no unnamed Kang Tao block. Every site Kang Tao stands in is accounted
for as a named catalog point (§7).

---

## 4. Economic structure

### 4.1 Revenue streams → catalog locations

Kang Tao's economy is **corporate arms manufacturing and sales**. Almost none of
that is physically present in Night City — the factories and labs are in China,
and the Night City building is a sales and administration office. This is the
central modelling problem for this faction.

| Revenue stream | Code(s) | Catalog locations that produce it | Evidence / notes |
| --- | --- | --- | --- |
| Arms manufacturing and sales | `arms` | Kang Tao Building (1) — sales, distribution and the Smart-weapon line | Wiki: Kang Tao's products are pistols (A-22B Chao), SMGs (G-58 Dian), shotguns (L-69 Zhuo), grenades, weapon mods, armour and cyberware. "Leading weapon exporter in Asia", €$525bn. `[wiki]` |
| R&D on Smart weapons | `rnd` | Kang Tao Building (1) | Wiki: "specialization in the development, patenting and production of Smart-class weaponry"; new research facilities funded by government backing. No lab record exists in Night City. `[wiki]` |
| Corporate security / mercenary contracts | `security_services`, `mercenary` | Kang Tao Building (1) — contract desk; every guard detail is a contract in the field | Wiki: "becoming important players in the mercenary and security markets". Game-data: ranger/soldier/android/officer records appear as contracted details rather than turf holders. `[wiki]` `[game-data]` |
| Cyberware (via subsidiary) | `cyberware` | Kang Tao Building (1) — brand licensing | Wiki: [[QianT]] is a Kang Tao-owned cyberware manufacturer, used as a shell company for sensitive operations (it carried the Hellman extraction traffic). Products include Mantis Blades, Gorilla Arms, Projectile Launch System, NeoFiber, Optical Camo. `[wiki]` |
| Intelligence / data brokering | `information`, `netrunning` | Nasty Hangover warehouse (3) — the stolen datashard; Kang Tao Building (1) — the extraction operation | Wiki: slogan "This is Kang Tao. This is intelligence."; QianT servers carried the Hellman extraction plan; Karl Ginsky's shard is "top-secret corporate data". `[wiki]` |
| Logistics (extraction corridor) | `logistics` | Yet unreached: fuel station (5), AV crash site (6), airstrip (7) are waypoints, not Kang Tao facilities | Wiki: Hellman was moved by AV through the southern Badlands with a Kang Tao escort and a fallback fuel station. Kang Tao owns none of these locations. `[wiki]` |
| Fuel / energy retail | — (not Kang Tao) | SovOil Fuel Station (5) | `SovOil`-owned, `Marty Jenklow` manager. Listed only because Kang Tao uses it. **Do not credit `energy` to Kang Tao.** `[wiki]` |

**Why the list is short, stated plainly.** Four of the five §5.4 corp streams
hypothesised for Kang Tao (`arms`, `manufacturing`, `rnd`) are correct in lore
but **do not exist as places in Night City**. There is no Kang Tao factory, no
Kang Tao lab, no Kang Tao warehouse, and no Kang Tao gun shop. Modelling
`manufacturing` for this faction means either (a) accepting that the HQ produces
no manufacturing yield, or (b) inventing a plant that does not exist. This doc
recommends (a) and flags it in §8.3.

### 4.2 Suppliers, customers, rivals

| Role | Party | Detail |
| --- | --- | --- |
| Parent / owner | Chinese state and QianT | Restructured 2050 with "alleged government connections" and government-funded research; QianT is a subsidiary shell. `[wiki]` |
| Customer | National and paramilitary buyers | "Quality weapons and equipment that suits both military and paramilitary needs"; leading arms exporter in Asia. `[wiki]` |
| Customer | Night City street market | Kang Tao pistols are "popular among the streets of Asia with many gangers opting for the reliable and inexpensive brand". No Night City storefront though — the guns arrive through other vendors. `[wiki]` |
| Competitor / partner (airframes) | Zetatech | The Hellman extraction used a **Zetatech Surveyor** AV; the escape drones in *Life During Wartime* are **Militech Griffins**. Kang Tao leases, does not build, its airframes. `[wiki]` |
| Rival | Arasaka | Primary Smart-weapon and corporate-security rival; both are in Corpo Plaza, 535 m apart. `[wiki]` `[game-data]` |
| Rival | Militech | Arms rival; the Corpo Plaza hustle `ma_cct_cpz_15` sits in the **Militech HQ Concourse** sub-territory, 269 m from Militech's own CC. It is Kang Tao standing on Militech's doorstep. `[wiki]` `[game-data]` |
| Rival | Tsunami Arms | Named as a peer in the top tier of weapon manufacturers. `[wiki]` |
| Victim / counterparty | 6th Street | The Arroyo gig is 6th Street beating a Kang Tao employee and stealing his shard; the Glen encounter is Kang Tao versus 6th Street. `[game-data]` `[wiki]` |
| Regulator / landlord | Night City council | In 2077 Kang Tao expressed interest in buying **Pacifica** cheap in exchange for clearing its crime; "no official deals had been made". This is the only lore thread that would justify a Pacifica footprint, and it did not happen. `[wiki]` |

---

## 5. Headquarters recommendation

### Primary HQ: **Kang Tao Building** — Corpo Plaza

Coordinates: site anchor `(-1127.822, 546.952, 17.890)`; community centre
`(-1118.182, 554.060, 18.601)`. `[game-data]`
`data/sites/sites.json` site 20 `ma_cct_cpz_16`.

Rationale:

1. **It is the only canonically-owned Kang Tao building in Night City.** The wiki
   gives it `type = North American Division HQ / Regional HQ`,
   `owner = Kang Tao`, `location = Corporate Plaza`, and cites the 2077 sourcebook
   and the Cyberpunk Edgerunners Mission Kit. There is no competing candidate.
   `[wiki]`
2. **It is already the faction's seeded seat.** `sub_territory_id = 78`
   (`cpz_kang_tao_sector`) has `initial_owner_faction_id = 22`, and
   `cc_cpz_kang_tao_sector` is 12 m from the site anchor. No re-seeding needed.
   `[game-data]`
3. **It maps to the whole economy.** Arms sales, R&D, security contracts,
   cyberware licensing and intelligence all run through this one address,
   because it is the only Kang Tao address. Owning the HQ and owning the economy
   are the same action — trivially true here, unlike for Arasaka. `[wiki]` `[inferred]`
4. **Verified garrison.** 5 Kang Tao units on the site (2 rangers, 3 shotgun
   soldiers) plus a 5-entry Kang Tao community and `#ma_resource_ga` guard areas.
   The prefab tree also names `#ma_cct_cpz_16_security_area`,
   `#ma_cct_cpz_16_security_system` and four `#ma_cct_cpz_16_main_loot`
   containers, but `devices.json` has **no rows** for site 20 — those nodes are
   prefab names only, not extracted device records. `[game-data]`
5. **Corporate Plaza is the right neighbourhood.** The wiki says every plaza
   building has "strict checkpoints" with NCPD and private corporate security on
   constant patrol — a defensible, high-value, hostile-to-outsiders seat. `[wiki]`

**Trade-off — the biggest one in this document:** the game gives the Kang Tao
Building **no interior**. Site 20 is a scanner-hustle volume on the plaza with
`is_interior=0`, `has_doors=0`, zero devices and zero workslots, and there is no
lobby/entrance/atrium marker anywhere near it (I checked 400 m). An HQ control
point here must be an **outdoor plaza volume at the tower's base**, not a
capturable lobby. Contrast Arasaka Tower, whose lobby/atrium/CEO/rooftop are all
named markers. If the mod needs an enclosed corp HQ, Kang Tao cannot supply one
and the design has to accept a plaza-floor seat.

### Alternate 1: **Hanford Overpass** — Glen

Coordinates `(-1410.732, -1208.607, 26.723)` `[game-data]`
site 60 `ma_hey_gle_15`.

Mechanically this is the **better** control point of the two: it has the richest
records Kang Tao owns anywhere — 9 units (4 rangers, 3 androids, an elite
grenadier officer, a shotgun soldier), 4 guard areas, 7 patrol splines, 3
triggers, 24 workspots, and it already sits on an **active** control centre 5.3 m
away (`cc_gle_hanford_overpass`, `is_active=1`, Kang Tao-owned). It loses as HQ
because it is an overpass in Valentinos turf with no building, no revenue and a
seed-invented name, and because the canon seat is in Corpo Plaza. `[game-data]`

### Alternate 2: **Nasty Hangover warehouse** — Arroyo

Coordinates `(-573.614, -1182.899, 7.701)` `[game-data]` site 382
`sts_std_arr_06`.

The only **enclosed interior** with a Kang Tao presence, and it is a genuinely
named, wiki-documented place (`baseid = sts_std_arr_06`). It loses badly as HQ:
`default_faction_id = 4` (6th Street owns it), it is a 6th Street stash, and
Kang Tao only arrives at the end of the gig to kill Karl and recover the shard.
Using it as a Kang Tao seat would invert the quest. Good *raid target*, wrong
*seat*. `[game-data]` `[wiki]`

### Overruled / downgraded suggestions

- **Satwave Power Plant as Kang Tao infrastructure** — Kang Tao does not own or
  run it. V and Panam attack its security (which is generic site security, not a
  Kang Tao detail) to fire an EMP *at* Kang Tao's AV. Counting it as an `energy`
  asset would be a category error. `[wiki]`
- **SovOil Fuel Station as a Kang Tao asset** — `SovOil`-owned with its own
  manager and weapon vendor. Kang Tao merely falls back to it. Its nearest CC is
  **Biotechnica**'s (`cc_bls_biotechnica_flats`, 5.9 m). `[wiki]` `[game-data]`
- **The 6th Street warehouse as Kang Tao turf** — 6th Street owns and guards it;
  Kang Tao are the avengers. `[game-data]`
- **A Pacifica holding** — the wiki records only that Kang Tao *asked* about
  buying Pacifica in 2077 and that no deal was made. Zero roster sites, zero
  areas, zero seed rows in Pacifica. Do not seed one. `[wiki]` `[game-data]`
- **"Kang Tao North Tower" as a lore name** — no wiki page, marker, prefab or
  game enum uses it; the seed generator invented it (§8.1). Keep the
  coordinates, drop or qualify the name. `[game-data]` `[inferred]`

---

## 6. Priority list of control points

Ranked by how well each place serves as a capturable Kang Tao control point.
"CC" = nearest entry in `data/control_centers.json`; distance is horizontal
metres. Relevance reflects lore + revenue + record richness, not raw unit count.

| Rank | Control point | Rel. (1–5) | District / sub-district | Coordinates | Existing CC overlap | Why |
| ---: | --- | :---: | --- | --- | --- | --- |
| 1 | **Kang Tao Building** | 5 | CityCenter / CorpoPlaza | `-1127.822, 546.952, 17.890` | `cc_cpz_kang_tao_sector`, 12.0 m (Kang Tao) | The only canon Kang Tao address; NA Division HQ; 5 units; plaza-floor volume only, no interior |
| 2 | **Hanford Overpass** | 4 | Heywood / Glen | `-1410.732, -1208.607, 26.723` | `cc_gle_hanford_overpass`, 5.3 m (Kang Tao, **active**) | Richest records Kang Tao owns: 9 units incl. 3 androids, 7 patrols, 4 guard areas; seed-named |
| 3 | **Nasty Hangover warehouse** | 3 | SantoDomingo / Arroyo | `-573.614, -1182.899, 7.701` | `cc_arr_red_dirt_cross`, 355.7 m (**6th Street**) | Only enclosed interior with Kang Tao presence; 6th Street-owned; the shard is the prize |
| 4 | **Corpo Plaza scanner hustle** | 2 | CityCenter / CorpoPlaza | `-1070.084, 71.217, 7.352` | `cc_rey_delamain_block`, 259.7 m (**Valentinos**) | 3 units on a Militech-concourse site; presents Kang Tao pressure on a rival's doorstep |
| 5 | **SovOil Fuel Station** | 2 | Badlands / Badlands | `-1815.323, -4282.463, 74.249` | `cc_bls_biotechnica_flats`, 5.9 m (**Biotechnica**, active) | 16 Kang Tao entries across three communities — the largest Kang Tao concentration in the game — but it is SovOil's station |
| 6 | **AV crash site** | 2 | Badlands / Badlands | `-669.654, -5006.292, 74.518` | `cc_bls_solar_station`, 606.8 m (**Militech**) | 7 Kang Tao "petrochem operators" + query cluster; a crash site, no structures |
| 7 | **Satwave Power Plant** | 1 | Badlands / Badlands | `-195.302, -2838.326, 22.799` | `cc_rcr_almunecar_strip`, 654.6 m (6th Street) | 4 Kang Tao drone units; a city asset Kang Tao is attacking, not holding |
| 8 | **Old airstrip** | 1 | Badlands / Badlands | `-1276.796, -5208.874, 83.391` | `cc_bls_biotechnica_flats`, 1067.8 m (Biotechnica) | 4 Kang Tao units in an abandoned airfield; pursuit waypoint |

### Test control point for the first in-game test: **Hanford Overpass**

Site 60 `ma_hey_gle_15`, coordinates `(-1410.732, -1208.607, 26.723)`,
`[game-data]` `data/sites/sites.json`.

Why this and not the HQ or the warehouse:

- **Cleanest Kang Tao-default facility site, and it is not the HQ.** It has
  `default_faction_id = 22`, `initial_owner_faction_id = 22`,
  `control_center_id = 42`. Eviction has no ambiguity: the only non-Kang Tao
  roster entry is one `Character.ma_hey_gle_15_6th_street_victim` (a corpse
  prop), which is exactly the "Kang Tao cleared out 6th Street here" story.
  `[game-data]`
- **The richest capture-relevant record set Kang Tao owns.** 4 guard areas
  (`#ma_hey_gle_15_ga`, `_002`, `_003`, `_addition…`), 7 patrol splines
  (`#ma_hey_gle_15_spl_ganger_002/003/004/005/006/008/009`), 3 triggers
  (`start`, `cleanup`, `voice`), 24 workspots, and 9 units across four combat
  roles including **3 androids** — a useful test of mixed unit behaviour.
  `[game-data]`
- **It already has an active CC 5.3 m away.** `cc_gle_hanford_overpass` is
  `is_active=1` and Kang Tao-owned, so no map plumbing is needed and the seed's
  existing active point is exercised. `[game-data]`
- **It is not the HQ**, so the first test exercises capture on a non-seat, as
  METHOD §3.8 requires. `[game-data]`
- **It needs no name verification to test.** The capture volume is what is being
  tested; the seed name being unverified (§8.1) does not block a trigger test.

Trade-off: it is a **road overpass, not an enclosed interior** (`is_interior=0`,
`has_doors=0`, zero devices), with 20 m of Z spread across the guard areas. That
is a *better* first test than the HQ because a flat outdoor volume with rich
patrol data isolates capture logic from interior streaming. It is a *worse*
first test than Arasaka's substation if you need to prove interior capture
works, because Kang Tao has no interior to offer.

Follow-up test: **Nasty Hangover warehouse**
(`#arr_06_main_gate`, `-573.614, -1182.899`) once the CC is retargeted, to
validate a two-storey interior with a main gate and roof door. It is 6th
Street-owned, so this second test also exercises capturing a site from a *rival
gang* rather than from the corp itself — worth doing on purpose.

Fallback if Hanford Overpass proves too small or the seed row is rejected: the
**Kang Tao Building** plaza volume itself (`ma_cct_cpz_16`, 2 guard areas, 3
triggers), which is the one place that cannot be argued away.

---

## 7. Per-sub-district counts

This is the number to feed yield balancing. It counts **distinct named places**
Kang Tao owns, runs, protects or habitually occupies — not quest-scene variants
and not generic occupied blocks. `Filler` is the deduped occupied-site count
minus any site already counted as a named place (METHOD §8).

| Sub-district | Named lore-relevant places | Which ones | Kang Tao-occupied sites (deduped) | Filler | Noteworthy interiors |
| --- | ---: | --- | ---: | ---: | --- |
| CorpoPlaza | **2** | Kang Tao Building, Corpo Plaza scanner hustle | 2 | 0 | None (plaza volumes only) |
| Glen | **1** | Hanford Overpass (seeded) | 1 | 0 | None |
| Arroyo | **1** | Nasty Hangover warehouse (6th Street-owned) | 1 | 0 | Warehouse: main gate + roof door |
| Badlands | **4** | SovOil Fuel Station, Satwave Power Plant, AV crash site, Old airstrip | 0 | 0 | Fuel station workshop/store |
| RanchoCoronado | **0** | attribution artefact only (§2.2) — the points are Badlands | 0 | 0 | None |
| Downtown | **0** | PL courier-loop combat area only; no roster unit | 0 | 0 | None |
| **Total** | **8** | | 4 | **0** | 1 |

Reconciliation: 4 deduped occupied sites − 4 site-backed named places = **0
filler**. All 4 sites are named catalog points, so nothing is left over. The
other 4 named places are **marker-only** (the four Badlands points, none of which
has a `sites.json` row). `named + filler = 8`, which is the 4 sites plus the 4
marker-only named places. `[game-data]`

Caveat on "named": only **three** of the eight are wiki-verified Kang Tao
places — Kang Tao Building, the Nasty Hangover warehouse, and the SovOil fuel
station (which is SovOil's, not Kang Tao's). The other five are one
seed-invented name (Hanford Overpass), one unnamed Kang Tao encounter
(the Corpo Plaza hustle), and three quest locations Kang Tao merely passes
through or attacks (Satwave, crash site, airstrip). **Only the HQ should receive
an iconic-business yield multiplier.** The rest are encounter sites.

Interpretation for yield: this is a deliberately small faction. CorpoPlaza holds
the only real economy, and it is one building. Glen and Arroyo are single
combat sites. The four Badlands points are a quest corridor, not holdings. If the
map needs more Kang Tao points than 6, the honest expansion is not in game data —
it does not exist — and would have to be a design decision (§8.3).

---

## 8. Gaps and uncertainties

1. **The seed name "Kang Tao North Tower" is ours, not lore.** It appears in
   `tools/generate-world-seeds.py` line 204 alongside every other grid name and
   has no wiki page, marker, prefab path or `gamedataDistrict` enum entry. The
   wiki calls the building simply "Kang Tao Building" and gives it
   `type = North American Division HQ`. The *coordinates* are sound (site 20 is
   in the Kang Tao-seeded sub-territory, 12 m from its CC); only the name is
   invented. This doc uses the coordinates and calls the place "Kang Tao
   Building", flagging the seed name. **Recommend renaming the seed row.**
2. **`gamedataDistrict` has no Kang Tao entry at all.** I dumped the full enum
   from `refs/cyberpunk/orphans.swift` (134 values): Arasaka and Militech both
   have interior mappings (`CorpoPlaza_ArasakaTowerLobby` etc.), and Kang Tao has
   none. That is primary-source confirmation that the game never built a Kang Tao
   interior. Do not expect to find one.
3. **Kang Tao has no manufacturable asset in Night City.** §5.4 predicts
   `arms`, `manufacturing`, `rnd` for this corp. All three are true of the
   *company* and none is a *place*: the factories are in China, and the Night
   City site is sales and administration. Seeding `manufacturing` yield here
   would invent a plant. Decide explicitly whether a megacorp HQ is allowed to
   produce manufacturing yield with no factory, and if so, at what discount.
4. **"Hanford Overpass" is unverified and probably wrong in spirit.** There is
   no Hanford marker, prefab or wiki location in Night City (`Hanford` on the
   wiki is a 2020 toxic town in Washington state, unrelated). The site is a real
   Kang Tao-versus-6th Street encounter (`#ma_hey_gle_15_ws_6th_street_after`,
   `Character.ma_hey_gle_15_6th_street_victim`) at a genuine overpass. The name
   is a plausible-looking seed invention. Rename to something honest, or accept
   a seed-only name.
5. **The largest Kang Tao concentration in the game is on someone else's
   property.** The three `q104_com_gas_station_*` communities put **16** Kang Tao
   entries at the SovOil fuel station — more than the HQ (5) and Hanford (9)
   combined. But the station is SovOil's, and its nearest CC is Biotechnica's. If
   a seeder retargets by "most units" it will hand Kang Tao a SovOil asset and
   a Biotechnica-owned control point. Do not rank by unit count for this faction.
6. **`ma_cct_cpz_15` is owned by Militech's sub-territory.** The site carries
   `default_faction_id = 22` (Kang Tao) but `initial_owner_faction_id = 21`
   (Militech) and `sub_territory_id = 77` (`cpz_militech_hq`). This is exactly
   METHOD §1.1 item 5's warning, in corp form: a Kang Tao garrison standing in
   Militech's precinct. It is a good *pressure* point and a bad *ownership*
   claim; do not read `default_faction_id` alone.
7. **The Corpo Plaza hustle has no name and no business.** It is 3 units and a
   crate beside Militech's concourse. I count it as a named place because it is a
   distinct, persistent Kang Tao position, but it is the weakest "named" entry in
   this doc and could reasonably be demoted to a contested point.
8. **`q104` prefix aggregation is unsafe.** Eight `q104_com_*` areas span the
   power plant (Jackson Plains), the crash site, the fuel station (Biotechnica
   Flats) and the airstrip — up to 2.5 km apart. The `district_code` on all of
   them is `badlands`, which is at least not *wrong*, but the areas are not one
   place. Any per-prefix roll-up will merge four sites into one.
9. **Two Badlands rows land in RanchoCoronado and should not.** The §3.3
   nearest-sub-territory fallback chose `rcr_almunecar_strip` (655 m) over any
   Badlands sub-territory, because no Badlands centroid is closer. RanchoCoronado
   therefore shows 2 areas / 7 entries it does not have. Either add explicit
   Badlands-area sub-territories or special-case the `q104` map to `Badlands`.
10. **`areas.jsonl.district_code` is wrong for at least one site's community.**
    `{ma_cct_cpz_16_com}` is labelled `watson` but sits at `(-1118, 554)` in
    Corpo Plaza. This is the same path-token inheritance defect Arasaka's doc
    records; it is not corp-specific but it does hit the one site that matters
    most for this faction.
11. **No Kang Tao storefront means no `retail` point.** Kang Tao guns are sold
    in Night City (gangers use them) but through other vendors — there is no
    Kang Tao shop, and the extract has no vendor inventory anyway. If the mod
    wants an arms-retail control point for Kang Tao, none exists in game data.
12. **QianT has no address.** The wiki confirms QianT is a Kang Tao subsidiary,
    a cyberware manufacturer, and the shell company that carried the Hellman
    extraction traffic — but no QianT building, office or lab appears in Night
    City or in the extract. `cyberware` revenue is therefore attributed to the
    HQ as a licensing line, not to a factory. `[wiki]` `[game-data]`
13. **Pacifica is a trap.** Kang Tao's 2077 interest in buying Pacifica is
    prominently on the wiki and reads like a territorial hook, but the article
    says explicitly "no official deals had been made", and the extract has zero
    Kang Tao rows in Pacifica/Dogtown. A future agent should not seed Pacifica
    on the strength of that sentence.
14. **The test point cannot be the HQ, and the HQ cannot be an interior.** This
    faction cannot satisfy both §3.8's "prefer an interior" and "not the HQ" at
    once, because there is exactly one Kang Tao site with (weak) interior claims
    and it is a rival's building. The playbook should say what to do when a corp
    has **zero** interiors of its own: use the richest outdoor site for the test
    (Hanford Overpass) and treat the plaza base as the seat.

---

## 9. Sources

Local:

- `dist/extract/markers.jsonl` — all named coordinates (HQ community, Satwave
  terminal, fuel station, crash site, airstrip tracks, Nasty Hangover pickups).
- `dist/extract/areas.jsonl` — 17 Kang Tao areas, entries and dominance.
- `data/sites/sites.json` — sites 20, 19, 60, 382 (anchors, default factions,
  sub-territories, prefab refs).
- `data/sites/{rosters,guards,triggers,spots,patrols,doors,devices,suitabilities,communities}.json`
  — the 24 roster units, guard areas, patrol splines and suitability tags.
- `data/{factions,districts,sub_territories,landmarks,control_centers,faction_headquarters,spawn_points}.json`
  — faction id 22, sub-district spelling, 2 owned sub-territories, CC anchors,
  14 faction-22 spawn points.
- `dist/extract/raw/base/worlds/03_night_city/_compiled/default/*.streamingsector.json`
  — `#q104_pr_power_plant`, `loc_q104_old_airstrip`, `loc_q104_gas_station`,
  `#arr_06_*_kang_tao*` prefab paths and the Kang Tao character record list.
- `refs/cyberpunk/orphans.swift` — the full `gamedataDistrict` enum (no Kang Tao
  entry) and `gamedataAffiliation.KangTao = 9`.
- `tools/generate-world-seeds.py` — proves both seed names are generated grid
  names, not lore.

Wiki:

- [Kang Tao](https://cyberpunk.fandom.com/wiki/Kang_Tao)
- [Kang Tao Building](https://cyberpunk.fandom.com/wiki/Kang_Tao_Building)
- [Corporate Plaza (2077)](https://cyberpunk.fandom.com/wiki/Corporate_Plaza_(2077))
- [Petrochem Tower](https://cyberpunk.fandom.com/wiki/Petrochem_Tower)
- [QianT](https://cyberpunk.fandom.com/wiki/QianT)
- [Gig: Nasty Hangover](https://cyberpunk.fandom.com/wiki/Gig:_Nasty_Hangover)
- [Lightning Breaks](https://cyberpunk.fandom.com/wiki/Lightning_Breaks)
- [Life During Wartime](https://cyberpunk.fandom.com/wiki/Life_During_Wartime)
- [Ghost Town](https://cyberpunk.fandom.com/wiki/Ghost_Town)
- [Satwave Power Plant](https://cyberpunk.fandom.com/wiki/Satwave_Power_Plant)
- [SovOil Fuel Station (Highway 101)](https://cyberpunk.fandom.com/wiki/SovOil_Fuel_Station_(Highway_101))
- [Jackson Plains Regional Airport](https://cyberpunk.fandom.com/wiki/Jackson_Plains_Regional_Airport)

Earlier repo research:

- [`docs/research/factions/METHOD.md`](./METHOD.md)
- [`docs/research/factions/arasaka.md`](./arasaka.md)
- [`docs/research/factions/tyger-claws.md`](./tyger-claws.md)
- [`docs/research/factions/militech.md`](./militech.md)

---

## 10. Machine-readable block

Strict JSON for seeding (contract in [`METHOD.md`](./METHOD.md) §10). Every
coordinate was verified against the local record named in `source` on
2026-11-25; none came from the wiki. `null` means `TBD`, never `0`.

```json
{
  "faction_code": "kang_tao",
  "hq": {
    "name": "Kang Tao Building",
    "district": "CityCenter",
    "sub_district": "CorpoPlaza",
    "x": -1127.822,
    "y": 546.952,
    "z": 17.89,
    "source": "data/sites/sites.json site 20 ma_cct_cpz_16",
    "confidence": "game-data+wiki"
  },
  "alternate_hqs": [
    {
      "name": "Hanford Overpass",
      "district": "Heywood",
      "sub_district": "Glen",
      "x": -1410.732,
      "y": -1208.607,
      "z": 26.723,
      "source": "data/sites/sites.json site 60 ma_hey_gle_15",
      "confidence": "game-data+inferred"
    },
    {
      "name": "Nasty Hangover warehouse",
      "district": "SantoDomingo",
      "sub_district": "Arroyo",
      "x": -573.614,
      "y": -1182.899,
      "z": 7.701,
      "source": "data/sites/sites.json site 382 sts_std_arr_06",
      "confidence": "game-data+wiki"
    }
  ],
  "test_control_point": {
    "name": "Hanford Overpass",
    "district": "Heywood",
    "sub_district": "Glen",
    "x": -1410.732,
    "y": -1208.607,
    "z": 26.723,
    "source": "data/sites/sites.json site 60 ma_hey_gle_15",
    "confidence": "game-data+inferred"
  },
  "control_points": [
    {
      "rank": 1,
      "name": "Kang Tao Building",
      "type": "corporate_hq",
      "relevance": 5,
      "district": "CityCenter",
      "sub_district": "CorpoPlaza",
      "x": -1127.822,
      "y": 546.952,
      "z": 17.89,
      "source": "data/sites/sites.json site 20 ma_cct_cpz_16",
      "confidence": "game-data+wiki",
      "interior": false,
      "revenue_streams": ["arms", "rnd", "security_services", "cyberware", "information"],
      "nearest_cc_code": "cc_cpz_kang_tao_sector",
      "nearest_cc_m": 12.0
    },
    {
      "rank": 2,
      "name": "Hanford Overpass",
      "type": "overpass_encounter",
      "relevance": 4,
      "district": "Heywood",
      "sub_district": "Glen",
      "x": -1410.732,
      "y": -1208.607,
      "z": 26.723,
      "source": "data/sites/sites.json site 60 ma_hey_gle_15",
      "confidence": "game-data+inferred",
      "interior": false,
      "revenue_streams": ["security_services", "mercenary"],
      "nearest_cc_code": "cc_gle_hanford_overpass",
      "nearest_cc_m": 5.3
    },
    {
      "rank": 3,
      "name": "Nasty Hangover warehouse",
      "type": "warehouse",
      "relevance": 3,
      "district": "SantoDomingo",
      "sub_district": "Arroyo",
      "x": -573.614,
      "y": -1182.899,
      "z": 7.701,
      "source": "data/sites/sites.json site 382 sts_std_arr_06",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["information", "netrunning"],
      "nearest_cc_code": "cc_arr_red_dirt_cross",
      "nearest_cc_m": 355.7
    },
    {
      "rank": 4,
      "name": "Corpo Plaza scanner hustle",
      "type": "street_encounter",
      "relevance": 2,
      "district": "CityCenter",
      "sub_district": "CorpoPlaza",
      "x": -1070.084,
      "y": 71.217,
      "z": 7.352,
      "source": "data/sites/sites.json site 19 ma_cct_cpz_15",
      "confidence": "game-data",
      "interior": false,
      "revenue_streams": ["security_services"],
      "nearest_cc_code": "cc_rey_delamain_block",
      "nearest_cc_m": 259.7
    },
    {
      "rank": 5,
      "name": "SovOil Fuel Station (Highway 101)",
      "type": "fuel_station",
      "relevance": 2,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": -1815.323,
      "y": -4282.463,
      "z": 74.249,
      "source": "dist/extract/markers.jsonl q104_07_sm_gas_station_chats",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["logistics"],
      "nearest_cc_code": "cc_bls_biotechnica_flats",
      "nearest_cc_m": 5.9
    },
    {
      "rank": 6,
      "name": "AV crash site",
      "type": "crash_site",
      "relevance": 2,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": -669.654,
      "y": -5006.292,
      "z": 74.518,
      "source": "dist/extract/markers.jsonl q104_mp_av_crash",
      "confidence": "game-data+wiki",
      "interior": false,
      "revenue_streams": ["mercenary"],
      "nearest_cc_code": "cc_bls_solar_station",
      "nearest_cc_m": 606.8
    },
    {
      "rank": 7,
      "name": "Satwave Power Plant",
      "type": "power_plant",
      "relevance": 1,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": -195.302,
      "y": -2838.326,
      "z": 22.799,
      "source": "dist/extract/markers.jsonl q104_pplant_cooling_terminal_marker",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["mercenary"],
      "nearest_cc_code": "cc_rcr_almunecar_strip",
      "nearest_cc_m": 654.6
    },
    {
      "rank": 8,
      "name": "Old airstrip (Jackson Plains Regional Airport)",
      "type": "airfield",
      "relevance": 1,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": -1276.796,
      "y": -5208.874,
      "z": 83.391,
      "source": "dist/extract/markers.jsonl q104_mp_airstrip_tracks_}000",
      "confidence": "game-data+wiki+inferred",
      "interior": false,
      "revenue_streams": ["logistics"],
      "nearest_cc_code": "cc_bls_biotechnica_flats",
      "nearest_cc_m": 1067.8
    }
  ],
  "subdistrict_counts": {
    "CorpoPlaza": {"named": 2, "filler": 0},
    "Glen": {"named": 1, "filler": 0},
    "Arroyo": {"named": 1, "filler": 0},
    "Badlands": {"named": 4, "filler": 0},
    "RanchoCoronado": {"named": 0, "filler": 0},
    "Downtown": {"named": 0, "filler": 0}
  }
}
```
