# Biotechnica — Lore-Relevant Control Points

Status: faction research run, 2026-11-25. One faction, one document.
Scope: replace the generic control-centre grid with places Biotechnica actually
owns, runs, protects or garrisons in Night City, with verified coordinates, an
economic map, an HQ pick, a ranked capture list and honest per-sub-district
counts. Method: this doc conforms to [`METHOD.md`](./METHOD.md); snippets, wiki
rules, the revenue-code vocabulary and the JSON contract live there. §1.1
(batch-1 corrections) was read first and overrides later sections.
`AGENTS.md` was read first. No commits, no game launch.

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Position, site, community, roster or spawn record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/artbook/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My reasoning links a named place to a game record; reasoning stated | Weak, flagged |

No coordinate below is guessed. Every `(x, y, z)` is copied from a local
marker, site, seed anchor or guard-area record, or marked `TBD`.

---

## 1. Summary

Biotechnica (faction id 23, `affiliation_enum = Biotechnica`) is the world's
largest biotech megacorp: genetic engineering, pharmaceutical and
microbiological research, and — since the 2070s — industrial food production.
Its fortune is the CHOOH2 patent, the synthetic grain alcohol that replaced oil
as the world's vehicle fuel; it licenses production to Petrochem and SovOil
rather than refining it itself, and that royalty stream funds everything else.
The Night City regional HQ is the **Biotechnica Building** in Corpo Plaza.
`[wiki]`

The Night City footprint is **thin and agricultural, not corporate-tower**:

- **Badlands — Biotechnica Flats (Protein Farms).** The single most important
  Night City asset: a vast greenhouse expanse in the Southern Desert that
  supplies "more than half" of the city's alternative protein, mostly
  cricket-derived and worm-derived SCOP paste. Dedicated `gamedataDistrict`
  sub-district (`Badlands_BiotechnicaFlats`). Seeded to Biotechnica with an
  **active** control centre. `[wiki]` `[game-data]`
- **Downtown (City Center) — Biotechnica Hotel**, a corporate hotel on Republic
  Way, staff apartments only, run end-to-end by Biotechnica including security.
  It is the **only** Biotechnica-owned building with a real interior in the
  extract (lobby, floor 19, roof). `[wiki]` `[game-data]`
- **Corpo Plaza (City Center) — Biotechnica Building**, the 2077 regional HQ.
  `[wiki]` No marker and no site row: coordinate `TBD`.
- **Northside (Watson) — All Foods Factory**, a Biotechnica subsidiary's protein
  plant. **Lost by 2077**: shut down and overrun by Maelstrom. `[wiki]`
- **Dogtown (Pacifica) — Biotechnica Venture Center** at Luxor Heights, an
  abandoned, never-finished investment. `[wiki]` Coordinate `TBD`.

Game-data scale: **2 roster sites / 25 units**, **5 community areas** (all five
Biotechnica-dominant, 29 entries), **2 seeded sub-territories**, and **5 spawn
points**. This is a small footprint — the METHOD appendix's "2 roster sites / 25
units / 5 areas" is exactly right, and it does not grow when you look harder.
The weight sits in **Downtown** (24 of 29 area entries, all at the hotel) and
**Badlands** (territory ownership, no roster at all). `[game-data]`

---

## 2. Territory

### 2.1 Districts

| Evidence kind | Result |
| --- | --- |
| (a) Wiki/lore | Global HQ La Jolla, SoCal (formerly Rome). Night City regional HQ at the Biotechnica Building, Corporate Plaza, City Center. Facilities: Biotechnica Hotel (Downtown), Biotechnica Flats (Badlands), Biotechnica Venture Center (Dogtown, abandoned), All Foods Factory (Northside, lost). `[wiki]` |
| (b) Vanilla map gang panel | **Structurally empty.** `data/districts.json` `vanilla_gangs` lists gangs only; megacorps never appear. As with Arasaka, evidence (b) is inapplicable by design, not missing. |
| (c) Game-data counts | 5 community areas contain Biotechnica units, all 5 Biotechnica-dominant (29 entries). 2 owned sub-territories. 2 roster sites / 25 units. 5 spawn points. District enum `gamedataDistrict.Badlands_BiotechnicaFlats = 13`; `gamedataAffiliation.Biotechnica = 5` (`refs/cyberpunk/orphans.swift`). `[game-data]` |

The 2 owned sub-territories (`data/sub_territories.json`,
`initial_owner_faction_id = 23`, both `owner_kind = corp`):

| Code | Display name | Sub-district | Anchor (x, y, z) | CC | CC active |
| --- | --- | --- | --- | --- | --- |
| `bls_biotechnica_flats` | Biotechnica Protein Flats | Badlands | `-1809.5, -4283.5, 74.1` | `cc_bls_biotechnica_flats` | **yes** |
| `dtn_central_concourse` | Downtown Central Concourse | Downtown | `-2147.3, 273.2, 7.5` | `cc_dtn_central_concourse` | no |

`[game-data]`

The Downtown holding is **misplaced in the seed** — see §8.1. The Flats holding
is correct and is the faction's best-anchored point.

### 2.2 Sub-district presence

Counts are from `dist/extract/areas.jsonl` (areas whose `faction_counts`
contains `biotechnica`; all five are dominant) and `data/sites/rosters.json`
(`faction_id == 23`). Occupied sites are deduped `sites.json` rows with
`default_faction_id == 23` **or** ≥ 1 Biotechnica roster entry; the two are not
within 25 m. Attribution follows METHOD §3.3 exactly (verified in §2.3).

| Sub-district | District | (a) Lore | (b) Panel | (c) Areas (dominant) | (c) Biotech entries | Occupied sites |
| --- | --- | --- | --- | ---: | ---: | ---: |
| Downtown | CityCenter | Hotel | — (corp) | 3 (3) | 24 | 1 |
| Dogtown | Dogtown | Venture Center; Roads to Redemption agents | Barghest | 1 (1) | 4 | 0 |
| JapanTown | Westbrook | Alex Pushkin held in a Claw garage | Tyger Claws | 1 (1) | 1 | 1 |
| Badlands | Badlands | **Protein Flats** | Wraiths/Aldecaldos/Militech | 0 | 0 | 0 |

`[game-data]`

**Reading the counts.** These numbers are tiny and that is the honest result.
24 of the 29 area entries are the hotel's three communities
(`{dtn_04_com_area}` 18, `{dtn_04_com_area_after_alarm}` 5,
`{dtn_04_com_npc}` 1). The Dogtown entry is the "Roads to Redemption" agent
squad; the JapanTown entry is one NPC. The Badlands — where the faction's real
physical asset is — has **zero** Biotechnica units in the extract, because the
farms are a landscape with no garrison, not a compound with guards. There is no
Biotechnica roster site in the Badlands at all.

### 2.3 Attribution caveat

The §3.3 attribution function was run unchanged on all five areas. Four resolve
by geocode token (`dtn_04_*` → Downtown, `jpn_01_*` → JapanTown). One does not:

- `{sts_ep1_07_agents}` at `(-1499.9, -2381.2)` has no geographic token, and
  the nearest geocoded site is 501 m away (over the 400 m limit), so it falls
  through to `nearest-subterritory`. That gives `Dogtown` at 140 m from
  `dt_terra_cognita` (the Luxor High Wellness Spa anchor). The wiki places the
  gig at the **Nighthawks Rehabilitation Center**, a section of the EBM
  Petrochem Stadium in Dogtown, so Dogtown is right — but this row is
  `[inferred]`, not `[game-data]`. `[game-data]` `[wiki]` `[inferred]`

`areas.jsonl.district_code` agrees with position for all five rows here
(`city_center`, `dogtown`, `watson`), which is unusual — batch 1 found it
routinely wrong for `always_loaded_*` quest communities. Do not generalise from
this faction.

---

## 3. Location catalog

Coordinates are world-space metres, `Z` up. "Interior?" means the game has a
distinct interior cell or room volume. "Business?" is what the place earns or
provides — the extract has no vendor inventory.

| # | Name | Type | District / sub-district | Interior? | Business? (what it earns) | Coordinates (x, y, z) | Coordinate source record | Linked communities / sites | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **Biotechnica Flats** (Protein Farms) | Protein farm landscape / greenhouses | Badlands / Badlands | No — open landscape, no interior cell | Protein (cricket, worm/SCOP) production and shipping; "more than half" of the city's alternative protein | `-1809.500, -4283.500, 74.100` | `data/sub_territories.json` `bls_biotechnica_flats` (identical to `cc_bls_biotechnica_flats`) | CC `cc_bls_biotechnica_flats` (`is_active=1`); LM `lm_bls_biotechnica_flats`; no roster site | `[game-data]` `[wiki]` |
| 2 | **Biotechnica Hotel** (Republic Way Hotel) | Corporate hotel / staff housing | CityCenter / Downtown | **Yes** — lobby, floor 19 (apartments 191–194, security room), roof/AV pad | Staff accommodation; corporate hospitality; in-house security (a cost centre, not a storefront) | `-2156.769, 467.990, 11.511` (entrance); floor 19 `-2130.031, 482.704, 89.495`; security room `-2163.610, 481.277, 89.472`; roof `-2138.881, 481.217, 93.467` | `dist/extract/markers.jsonl` `{dtn_04_mp_sm_entrance}`, `{dtn_04_mp_sm_room}`; `data/sites/triggers.json` `#dtn_04_security_room`; `data/sites/guards.json` `#dtn_04_roof_floor_guard_area` | Site 353 `sts_cct_dtn_04` (`default_faction_id=23`); communities `#dtn_04_com_area` (19), `#dtn_04_com_area_after_alarm` (5), `#dtn_04_com_npc` (3) | `[game-data]` `[wiki]` |
| 3 | **Biotechnica Building** | Regional HQ / skyscraper | CityCenter / CorpoPlaza | Yes (wiki + *Edgerunners*) — offices, database room, skybridge | R&D, CHOOH2 licence royalties, corporate administration; skybridge to Wellsprings | `TBD` | No marker, no site row, no seed anchor. Wiki: `owner = Biotechnica`, `type = Regional HQ`, `sub_district = Corporate Center`, `location = Corporate Plaza` | None found | `[wiki]` only; coordinate `TBD` |
| 4 | **All Foods Factory** (All Foods Plant) | Protein processing factory / gang hideout | Watson / Northside | **Yes** — main hall, lab, garage, transition floor | Protein slurry processing and forging (formerly); now Maelstrom's hideout | `-771.825, 2202.015, 50.508` (factory marker); intercom `-769.763, 2203.538, 52.384` | `dist/extract/markers.jsonl` `q003_01b_sm_meat_factory`, `{q003_mp_allfoods_intercom}` | Communities `{q003_com_main_hall}`, `{q003_com_lab}`, `{q003_com_garage}` (Maelstrom/Militech); CC `cc_nid_all_foods_plant` | `[game-data]` `[wiki]` — **not Biotechnica-held** |
| 5 | **Biotechnica Venture Center** | Abandoned mixed-use tower | Dogtown / Dogtown | Yes (wiki + ArtStation: explorable interior) | None realised; abandoned investment. Was to be Dogtown/Serenisands commercial development | `TBD` | No marker, no site row. Wiki: `owner = Biotechnica (formerly)`, `location = Luxor Heights & Golden Pacific`, `gangs = Scavengers (formerly)` | No local record of the prefab in the three extracted sectors | `[wiki]` only; coordinate `TBD` |

### 3.1 Interior sub-locations (the reason to capture a building)

**Biotechnica Hotel** is the only Biotechnica building whose interior is
provable from the extract. All rows `[game-data]`:

| Sub-location | Coordinates (x, y, z) | Record | Note |
| --- | --- | --- | --- |
| Street entrance | `-2156.769, 467.990, 11.511` | marker `{dtn_04_mp_sm_entrance}` | Lobby doors, police cordon on the side |
| Lobby / reception | `-2144.181, 470.637, 9.475` | trigger `#dtn_04_tr_recept_scene` | Reception desk, 3 workspots, lobby security + droids |
| Bottom-floor guard area | `-2153.566, 466.358, 9.473` | guard area `#dtn_04_bottom_floor_guard_area` | Lobby patrols, balcony spline |
| Lift | `-2127.590, 482.810, 9.720` | trigger `#dtn_04_tr_elevator` | Elevator to floor 19 only |
| Floor 19 apartment floor | `-2135.032, 481.835, 89.472` | guard area `#dtn_04_appartment_floor_guard_area` | 4 apartments, corridor patrol |
| Floor 19 security room | `-2163.610, 481.277, 89.472` | trigger `#dtn_04_security_room` | 2 guards, camera terminal, back door |
| Koch's apartment (193) | `-2130.031, 482.704, 89.495` | marker `{dtn_04_mp_sm_room}` | Living room, kitchen, bedroom, bathroom |
| Koch's hide spot | `-2166.015, 480.398, 89.492` | workspot `#dtn_04_ws_joanne_koch_hide` | Where the target waits |
| Roof / AV pad | `-2138.881, 481.217, 93.467` | guard area `#dtn_04_roof_floor_guard_area` | 4 guards, landing pad, skylight into 193 |

Site-level facts (`data/sites/sites.json` site 353): `is_interior = 0` (the flag
is unreliable, §2.2 of METHOD), but `has_doors = 1`, `has_guard_areas = 1`,
`patrol_count = 8`, `spot_count = 45`, `radius_m = 200.2`,
`control_center_id = 72`. `[game-data]`

**All Foods Factory** also has a proveable interior, but no `sites.json` row.
Its quest communities name the rooms: `{q003_com_main_hall}`,
`{q003_factory_combat_lab}`, `{q003_factory_combat_main}`,
`{q003_com_garage}`, `{q003_com_transition}`, `{q003_com_spiderbot_area}`.
`[game-data]`

### 3.2 How the name→coordinate links were proven

- **Biotechnica Flats** — the seed sub-territory and landmark are both named
  "Biotechnica Protein Flats" and both owned by faction 23; the CC at the same
  coordinate is `is_active = 1`. Independently, `gamedataDistrict` carries a
  dedicated `Badlands_BiotechnicaFlats = 13`
  (`refs/cyberpunk/orphans.swift`, `refs/RED4ext.SDK/.../game/data/District.hpp`
  line 26) — one of only a handful of sub-districts named after a corporation.
  The wiki infobox gives `type = Protein farms`, `owner = Biotechnica`,
  `region = Badlands`, `subregion = Southern Desert`. Three independent
  confirmations; the name is not in doubt. `[game-data]` `[wiki]`
- **Biotechnica Hotel** — wiki `baseid` on *Gig: Guinea Pigs* is
  `sts_cct_dtn_04`, which is exactly the `code` of site 353
  (`data/sites/sites.json`). The site's node names match the wiki's layout
  floor-for-floor (`#dtn_04_guard_area`,
  `#dtn_04_roof_floor_guard_area`, `#dtn_04_tr_elevator`,
  `#dtn_04_security_room`, `#dtn_04_ws_joanne_koch_hide`), the roster contains
  `Character.sts_dtn_04_target` (Koch) and `Character.dtn_04_receptionist`, and
  the wiki gives `sub_district = Downtown`, `street = Republic Way`. This is the
  cleanest identity join in the whole doc. `[game-data]` `[wiki]`
- **All Foods Factory** — *The Pickup*'s `baseid` is `q003_maelstrom`, and the
  factory marker is `q003_01b_sm_meat_factory`. The wiki gives
  `sub_district = Northside`, `street = Talbot Place`, `gangs = Maelstrom`,
  `owner = All Foods (formerly)`. All Foods' own infobox says
  `parent = Biotechnica (2077)`. `[game-data]` `[wiki]`
- **Biotechnica Building** — no local record. The 2.5 extract has no
  Biotechnica-named prefab, no mappin and no site row anywhere in Corpo Plaza;
  the only Corpo Plaza prefab directories are Arasaka Tower, the Militech and
  Kang Tao scanner sites and `mq061`. Coordinate left `TBD` per METHOD §6.
  `[wiki]`
- **Biotechnica Venture Center** — no local record. The three extracted
  `always_loaded_*` sectors contain no `venture`/`luxor` prefab beyond
  `#cz_luxor_heights_chat_*` ambient chat nodes. The wiki names it and puts it
  at Luxor Heights / Golden Pacific. Coordinate `TBD`. `[wiki]`

### 3.3 Biotechnica-occupied generic sites (the filler pool)

`data/sites/suitabilities.json` tags sites with gameplay affordances. This is
the entire pool — one unnamed site, one named.

| Site | Sub-district | Interior | Suitability tags | Units | Coordinates | Note |
| --- | --- | --- | --- | ---: | --- | --- |
| `sts_cct_dtn_04` (353) | Downtown | yes (3 levels) | raid_target 95, rooftop_access 80, elevator 70, officer_site 70, vehicle_bay 65, warehouse 65, arms_cache 56, branch_office 45 | 24 | `-2147.893, 475.315, 89.472` | **Named catalog point:** Biotechnica Hotel; not filler |
| `sts_wbr_jpn_01` (418) | JapanTown | yes | raid_target 75, stealth_entry 65, vehicle_bay 65, warehouse 65, safehouse 63, arms_cache 56, chop_shop 55 | 1 | `-528.188, 989.625, 34.525` | **Filler.** Olive Branch garage (Redwood St.); the single Biotechnica unit is Alex Pushkin, held in a car trunk. `default_faction_id = 2` (Tyger Claws) |

`[game-data]`

Treat the tags as gameplay affordances, not lore. The garage's `chop_shop` tag
describes the Tyger Claws' business, not Biotechnica's.

---

## 4. Economic structure

### 4.1 Revenue streams → catalog locations

| Revenue stream | Code(s) | Catalog locations that produce it | Evidence / notes |
| --- | --- | --- | --- |
| Protein agriculture | `agriculture` | Biotechnica Flats (1); All Foods Factory (4, formerly) | Wiki: the Flats' greenhouses mass-produce synthetic protein derivatives, mostly crickets and SCOP worms, and supply "more than half" of Night City's alternative protein. `[wiki]` |
| Food processing / manufacturing | `manufacturing` | All Foods Factory (4); Biotechnica Flats processing | All Foods' protein slurries were "marketed as meat"; All Foods is a Biotechnica subsidiary in 2077. `[wiki]` |
| Logistics / distribution | `logistics` | Biotechnica Flats (1) | SCOP paste is "shipped off to facilities where it is molded, flavored, and dyed"; the Flats are the origin point of the city's meat supply chain. `[wiki]` |
| R&D / pharmaceutical | `rnd` | Biotechnica Building (3); Biotechnica Flats (1, field trials) | Securicine, Project Nightingale, immunossuppressant prototype 0.091, cloned organs. The Koch team's Badlands trials are the field-research arm. `[wiki]` |
| Fuel licence royalties | `energy`, `finance` | Biotechnica Building (3) | Wiki: Biotechnica holds global CHOOH2 patents and licenses production to Petrochem and SovOil — "annual fees from their fuel and crop licences" made the corp wealthy. `energy` because the product is fuel; `finance` for the royalty stream. Neither is production — that is Petrochem's. `[wiki]` `[inferred]` |
| Staff accommodation / real estate | `hospitality`, `real_estate` | Biotechnica Hotel (2) | "Only employees of the corporation are able to get apartments in this hotel"; owned and operated by Biotechnica including security. `[wiki]` |
| Abandoned development | `real_estate` | Biotechnica Venture Center (5) | Unfinished Pacifica investment, abandoned after the Unification War. No current revenue; a write-down, not an earner. `[wiki]` |

No `security_services` line: unlike Arasaka, Biotechnica's guards exist to
protect its own property, and the extract shows no licensed-security business.

### 4.2 Suppliers, customers, rivals

| Role | Party | Detail |
| --- | --- | --- |
| Licensee (fuel) | Petrochem | Produces CHOOH2 under Biotechnica licence; listed partner. `[wiki]` |
| Licensee (fuel) | SovOil | Second major CHOOH2 licensee. `[wiki]` |
| Licensee (crops) | National and local governments | FrostCorn cultivation licences. `[wiki]` |
| Subsidiary | All Foods | Synthetic food and beverage producer; "under the Biotechnica umbrella". `[wiki]` |
| Partner (research) | Militech | Implied by the Nightingale cover-up notes; Militech is also the seeded owner of the pier district the hotel sits in. `[wiki]` `[game-data]` |
| Partner (network) | Impala Automatics | Biotechnica's net was hacked through Impala's servers (Mendoza/DOUBLE O). `[wiki]` |
| Labour | Aldecaldos | Saul Bright negotiated a work-for-xerophytes deal in 2077; the clan rejected a permanent relationship. `[wiki]` |
| Customer | Night City food chain | Restaurants, markets, kebab stands and burger joints citywide run on SCOP. `[wiki]` |
| Hostile | Crimson Harvest | Anti-corporate group; bombed the Paris research facility in 2076. `[wiki]` |
| Hostile | Red Ocher | Nomad clan that lost ≥70 members to Project Nightingale; hired Dino Dinovic to kill Koch. `[wiki]` |
| Occupier | Maelstrom | Holds the All Foods Factory (a Biotechnica subsidiary asset) by 2077. `[wiki]` `[game-data]` |
| Rival (food) | Petrochem, smaller protein producers | Not documented as direct rivals; Petrochem is a licensee and customer, not a competitor in protein. `[inferred]` |

---

## 5. Headquarters recommendation

### Primary HQ: **Biotechnica Protein Flats** — Badlands

Coordinates: `(-1809.500, -4283.500, 74.100)` `[game-data]`
`data/sub_territories.json bls_biotechnica_flats` (= `data/control_centers.json
cc_bls_biotechnica_flats`, the seeded landmark anchor).

Rationale:

1. **Canonically the faction's most important Night City asset.** It is the
   origin of more than half the city's alternative protein and the reason the
   corp diversified out of licensing into food. `[wiki]`
2. **Already seeded, already owned, already active.** Both the sub-territory
   and the control centre are Biotechnica's (`initial_owner_faction_id = 23`),
   `owner_kind = corp`, and `cc_bls_biotechnica_flats` is one of the few
   `is_active = 1` control centres in the seed. The mod needs no relabelling to
   start here. `[game-data]`
3. **Dedicated district enum.** `gamedataDistrict.Badlands_BiotechnicaFlats`
   exists as a first-class sub-district — the strongest possible proof that the
   game treats this as a place, not scenery. `[game-data]`
4. **Land for an economy.** A territory-scale holding (the wiki describes the
   farms as running from the Pacifica border to the SoCal border wall) is the
   right shape for a corp that earns from acreage and throughput, and unlike a
   tower it has room to add capture sub-zones — greenhouses, the compound, the
   old Prosperity settlement — without conflicting with a quest interior.
   `[wiki]`
5. **Nothing else in the faction is both canon and seat-shaped.** The Building
   (the true HQ) has no coordinate; the Hotel is a residence; the All Foods
   Factory is held by Maelstrom. `[game-data]` `[wiki]`

Trade-off: **this is a territory anchor, not a building anchor.** The point is
the seeded sub-territory centroid, and it sits 16.8 m from the Kang Tao gas
station used by the `q104`/`mq018` questline — the nearest built structure is
somebody else's. It also has no interior cell and no garrison (zero Biotechnica
units in the whole Badlands). Use it as the org seat and treat "the HQ building"
as a later detail; the fast-travel dataterm at `{bls_bls_dataterm_}10`
`(-1795.661, -4323.811, 74.413)`, 42.6 m from the CC, is a better
point-scale anchor for a capture volume if the centroid feels arbitrary.
`[game-data]` `[inferred]`

### Alternate 1: **Biotechnica Hotel** — Downtown

Coordinates: entrance `(-2156.769, 467.990, 11.511)` `[game-data]`
`markers.jsonl {dtn_04_mp_sm_entrance}`.

The only Biotechnica building in the extract with a real, three-level interior
and a clean `default_faction_id = 23`. It has a reception, a floor-19 security
room, four staff apartments, a regional director's apartment and a roof AV pad —
genuinely a seat with rooms to assign. It loses to the Flats because it is a
residence, not a production or command asset, and because the wiki says it
belongs to the *staff*, not the corporation's business. Excellent second seat,
and the recommended first test point. `[wiki]` `[game-data]`

### Alternate 2: **Biotechnica Building** — Corpo Plaza

Coordinates: `TBD`.

The canonical 2077 regional HQ, and the setting of Sasha Yakovleva's
infiltration in *Edgerunners*. It would be the obvious primary HQ if it had a
coordinate: the extract contains no marker, no site, no community and no prefab
for it, and the wiki gives only "Corporate Plaza, accessed by a bridge from
Memorial Park". A seeder that needs a Corpo Plaza point must place it by hand
from the map and then move this doc's `TBD` to `[game-data]`. `[wiki]`

### Overruled / downgraded suggestions

- **All Foods Factory as HQ or as an owned business** — a subsidiary asset, but
  the game state in 2077 is Maelstrom occupation, with 13+ Militech and 5+
  Maelstrom entries in its own communities and a `default_faction_id`-free site
  row. Catalogued as a contested subsidiary asset, not a Biotechnica seat.
  `[wiki]` `[game-data]`
- **Biotechnica Venture Center as a working point** — abandoned and unfinished;
  the wiki's own infobox says `owner = Biotechnica (formerly)`. No coordinate
  either. Keep it in the catalog for lore completeness, seed nothing. `[wiki]`
- **"Biotechnica Farms tour stop" as a facility** — the `mq061_05` biofarms
  prefab is a **hologram vista** on a Pacifica hillside, not a farm. Its scene
  marker is one of eleven tour stops pinned to the Militech HQ centroid at
  `(-1317.810, -84.292, 0.000)`. See §8.4. `[game-data]` `[wiki]`
- **The Olive Branch garage as a Biotechnica point** — one employee in a car
  trunk in a Tyger Claws garage. Presence, not ownership. Filler only. `[game-data]`

---

## 6. Priority list of control points

Ranked by how well each place serves as a capturable Biotechnica control point.
"CC" = nearest entry in `data/control_centers.json` (all CCs, active or not);
distance is horizontal metres; the owner column is the CC's sub-territory owner
per METHOD §1.1 item 10.

| Rank | Control point | Rel. (1–5) | District / sub-district | Coordinates | Existing CC overlap | Why |
| ---: | --- | :---: | --- | --- | --- | --- |
| 1 | **Biotechnica Protein Flats** | 5 | Badlands / Badlands | `-1809.500, -4283.500, 74.100` | `cc_bls_biotechnica_flats`, **0.0 m** (Biotechnica, active) | HQ. Dedicated district enum, seeded ownership, active CC, the city's protein supply |
| 2 | **Biotechnica Hotel** | 5 | CityCenter / Downtown | `-2156.769, 467.990, 11.511` | `cc_dtn_goldsmith_dock`, 126.9 m (**Militech**) | **Test control point.** Only clean `default_faction_id=23` facility; 3-level interior; 24 units; 4 guard areas, 8 patrols, 8 doors |
| 3 | **All Foods Factory** | 4 | Watson / Northside | `-771.825, 2202.015, 50.508` | `cc_nid_all_foods_plant`, 20.8 m (**Maelstrom**) | Subsidiary protein plant; large interior; the obvious contested-food point; not Biotechnica-held in 2077 |
| 4 | **Biotechnica Building** | 4 | CityCenter / CorpoPlaza | `TBD` | Unknown; no marker | Canonical regional HQ; needs a hand-placed coordinate before it can be seeded |
| 5 | **Biotechnica Venture Center** | 2 | Dogtown / Dogtown | `TBD` | Unknown; no marker | Lore-only abandoned asset; no coordinate, no current revenue |

### Test control point for the first in-game test: **Biotechnica Hotel**

Site 353 `sts_cct_dtn_04`, coordinates `(-2156.769, 467.990, 11.511)`
`[game-data]` `dist/extract/markers.jsonl {dtn_04_mp_sm_entrance}`.

Why this and not the HQ:

- **Clean ownership on the site row.** `default_faction_id = 23`,
  `control_center_id = 72`, and 24 of the site's roster entries are faction 23
  (`Character.sts_dtn_04_security` ×12, `..._security_droids` ×9,
  `..._security_officer`, `..._receptionist`, `..._target`). Eviction has no
  ambiguity. It is the only site in the extract with
  `default_faction_id = 23`. `[game-data]`
- **A genuinely enclosed, multi-floor interior.** Lobby → lift → floor 19 →
  roof, with 4 guard areas, 8 patrol splines, 8 doors and 45 workspots. This is
  rare for a corp (METHOD §3.8 expects corps to have no enclosed site) and lets
  the first test exercise a vertical capture volume, not just a radius on a
  fence. `[game-data]`
- **Complete capture-relevant records.** Guard areas
  (`#dtn_04_guard_area`, `#dtn_04_bottom_floor_guard_area`,
  `#dtn_04_appartment_floor_guard_area`, `#dtn_04_roof_floor_guard_area`),
  patrols (`#dtn_04_spl_patrol_*`, `#dtn_04_spl_guard_after`,
  `#dtn_04_spl_roof_guard_patrol_*`), doors
  (`#dtn_04_dvc_lift_door`, `#dtn_04_dvc_back_enter_door`, ...), a receptionist,
  a maid, and an officer. Everything a capture/defence prototype needs is
  present and named. `[game-data]`
- **Not the HQ.** The first test exercises capture on a non-seat, as METHOD §3.8
  recommends. `[game-data]`

Trade-off: the hotel is **126.9 m from `cc_dtn_goldsmith_dock`, whose
sub-territory (`dtn_goldsmith_dock`) is seeded to Militech (fid 21)** and which
is also `initial_owner_faction_id = 21` on site 353. Nearest-CC retargeting
would hand this point to Militech, so follow METHOD §1.1 item 10: retarget onto
the hotel's own coordinates, not by nearest CC. The seed currently gives
Biotechnica the *wrong* Downtown sub-territory (Central Concourse, 195 m north);
see §8.1. Second-choice test if the hotel's three floors complicate the volume:
the Flats itself — but it has no roster and no interior, so it tests far less.
`[game-data]`

---

## 7. Per-sub-district counts

This is the number to feed yield balancing. It counts **distinct named places**
Biotechnica owns, runs or is documented as owning — not quest variants and not
generic occupied blocks. `Filler` is the deduped occupied-site count minus any
site already counted as a named place (METHOD §8).

| Sub-district | Named lore-relevant places | Which ones | Biotechnica-occupied sites (deduped) | Filler | Noteworthy interiors |
| --- | ---: | --- | ---: | ---: | --- |
| Badlands | **1** | Biotechnica Flats | 0 | 0 | None (open landscape) |
| Downtown | **1** | Biotechnica Hotel | 1 | 0 | Hotel: lobby, floor 19, roof |
| Northside | **1** | All Foods Factory | 0 | 0 | Factory: main hall, lab, garage |
| CorpoPlaza | **1** | Biotechnica Building | 0 | 0 | Offices (lore only; no local record) |
| Dogtown | **1** | Biotechnica Venture Center | 0 | 0 | Abandoned interior (lore only) |
| JapanTown | **0** | Olive Branch garage is a Claw site, not a Biotechnica place | 1 | 1 (`sts_wbr_jpn_01`) | Garage (Tyger Claws) |
| **Total** | **5** | | 2 | 1 | |

Reconciliation: 2 deduped occupied sites − 1 site-backed named place
(Biotechnica Hotel) = **1 filler** (`sts_wbr_jpn_01`). The 4 other named places
are not `sites.json` rows: the Flats is a seed sub-territory anchor, the All
Foods Factory is a main-quest interior with quest communities, and the Building
and Venture Center have no local record at all. `named + filler = 6`, which is
the 2 sites plus the 4 non-site named places. `[game-data]`

Caveat on "named": **2 of the 5 are coordinate-less** (the Building and the
Venture Center), so a seeder that reads this table will see `named: 1` for
CorpoPlaza and Dogtown with nothing to place. That is deliberate and honest —
they are real, wiki-documented Biotechnica properties whose positions the extract
cannot supply. Do not synthesise a coordinate for them. `[wiki]`

Interpretation for yield: the honest read is that Biotechnica has **three
seedable points** (Flats, Hotel, All Foods) and one of those (All Foods) is not
even theirs in 2077. This faction should carry a high per-point multiplier on
the Flats — it is the city's food supply — and modest yield everywhere else.
Filling the map with "Biotechnica blocks" would be fabrication: there are only
two occupied sites, and one of them is a garage.

---

## 8. Gaps and uncertainties

1. **The seed gives Biotechnica the wrong Downtown sub-territory.** It owns
   `dtn_central_concourse` (sub 75, anchor `-2147.3, 273.2`), but there is no
   Biotechnica anything within 195 m of that anchor — the site there is
   `ma_cct_dtn_03`, `default_faction_id = 50` (NCPD), a cyberpsycho scanner
   hustle. The actual facility, the hotel, is at `-2156.8, 468.0`, inside
   `dtn_goldsmith_dock` (sub 72, **Militech**). Either move the seeded ownership
   to sub 72 or retarget the holding at the hotel. `[game-data]`
2. **The Flats has no Biotechnica presence, only ownership.** Zero roster
   entries, zero spawn points, zero community areas in the Badlands. The only
   Biotechnica-area records in the whole extract are in Downtown, Dogtown and
   JapanTown. A capture point there will have no defenders unless the mod adds
   them. This is the opposite of every gang faction in batch 1 and worth saying
   plainly rather than padding. `[game-data]`
3. **The Flats anchor is a sub-territory centroid on somebody else's building.**
   `(-1809.5, -4283.5)` is 16.8 m from `{q104_com_petro_gas_station}` (Kang Tao,
   10 entries) and 42.6 m from the fast-travel dataterm. METHOD §1.1 item 6
   treats centroid-coincident rows as fake anchors; this one is a legitimate
   *territory* anchor by construction (§3.0 uses it deliberately), but it is not
   a *building* anchor. The playbook does not distinguish the two, which is
   exactly the ambiguity that hurt batch 1's port zones.
4. **`mq061_05_sm_biotechnica_farms_scene` is a centroid-snapped tour marker,
   not a farm.** Eleven `mq061_*_sm_*` tour stops — Arasaka Memorial, City Hall,
   Biotechnica Farms, NCART, Rancho, Charter Hill, North Oak, Med Center, Oil
   Fields, Kabuki — all sit at exactly `(-1317.810, -84.292, 0.000)`, the
   Militech HQ anchor. The real tour stop is the area
   `{mq061_05_com_area}` at `(-2235.5, -3168.2, 106.1)`, a vista hologram
   (`#05_biofarms_v`, with `mq061_05_hazmat_*` squatters) on a Pacifica
   hillside. Do not read the marker as a facility. `[game-data]`
5. **The `mq061_05` prefab lives under a Corpo Plaza path.** The biofarms vista
   prefab is filed at
   `#c_city_center/corpo_plaza/loc_mq061_prefab.../#05_biofarms_v`. Path-based
   attribution would put it in Corpo Plaza; the area node puts it in Pacifica.
   METHOD §1.1 item 2 says prefab paths "name the place and its sub-district" —
   for hologram/vista prefabs they name the quest's staging folder instead.
6. **The Biotechnica Building has no coordinate and no record of any kind.** No
   marker, site, community, mappin or prefab. The wiki gives only "Corporate
   Plaza, bridge from Memorial Park". A regional HQ this important with zero
   extract presence is worth a note: 2.5 does not model the building's interior.
7. **The Biotechnica Venture Center is unfindable in the extract.** It should be
   in Dogtown/Luxor Heights; the three extracted sectors are `always_loaded_*`
   for the whole city and contain only `#cz_luxor_heights_chat_*` ambient nodes.
   No `venture`, `luxor_heights` building, or `serenisands` prefab. Either the
   building is in a Pacfica sector that was not extracted, or it is a static
   mesh with no gameplay nodes. `[game-data]`
8. **Biotechnica's security records carry no corp token.** Every guard at the
   hotel is `Character.sts_dtn_04_security` / `..._security_droids`, not
   `dtn_biotechnica_*`. METHOD §2.3 item 6 warns about this for Dogtown; it is
   also true in Downtown. A `character_record_id` containing "biotech" appears
   **zero** times in `data/sites/rosters.json`. Joining on the corp token finds
   nothing for this faction.
9. **All Foods is ambiguously Biotechnica's.** The org infobox says
   `parent = Biotechnica (2077)`, but the factory infobox says
   `owner = All Foods (formerly)` and `gangs = Maelstrom`, and the in-game
   database calls the plant defunct and Maelstrom-occupied. I count it as a
   named subsidiary asset but not as Biotechnica-held. A seeder should treat it
   as contested, with the CC's owner (`cc_nid_all_foods_plant`, Maelstrom) as
   the starting state.
10. **There is no `agriculture`-specific interior to capture.** The Flats are
   greenhouses on a landscape with no door/guard/patrol records. If the mod
   needs an interior for the faction's signature business, the only options are
   the hotel (wrong business) and the All Foods Factory (not theirs). This is a
   structural gap for the economy prototype, not a research failure.
11. **Wiki-only facilities with no coordinate are excluded from `named`.**
   *All Foods Building* on Eisenhower Street (the All Foods main office) and a
   *Biotechnica R&D facility* mentioned on the corp's netpage both appear in
   lore with no page-level coordinate and no local record. METHOD §1.1 item 12
   says: no page, no record → `[lore]`, `TBD`, not seeded. They are noted here
   and counted nowhere.
12. **The hotel's `is_interior = 0`.** Site 353 reports `is_interior = 0`
   despite an unmistakable three-level interior (lobby, floor 19, roof) with
   doors and guard areas. METHOD §2.2 hedges this ("its absence proves nothing"),
   but for a doc where the test point is an interior, the flag being wrong is
   worth calling out.
13. **The `rcr`/`ina` Badlands geocodes are not in the §3.3 token map.** The
   Badlands roster/area records use `ina_*` / `se5_*` / `bls_*`, none of which
   are tokens in METHOD's `SD` dict. Badlands attribution therefore only works
   through `nearest-subterritory`, which is fine at 3 km scale but will silently
   mis-attribute anything near the Pacifica/Badlands seam — as item 5 shows.
14. **`dtn_goldsmith_dock`'s display name is wrong for what is there.** The
   sub-territory and CC are named "Downtown West Pier" (anchor `-2164.5, 594.7`),
   but the hotel is at `-2156.8, 468.0`, 126.9 m inland, on Republic Way. The
   seeded name describes a pier, not a hotel block. Same class of defect as
   batch 1's `awf_ebunike_docks`.

---

## 9. Sources

Local:

- `dist/extract/markers.jsonl` — hotel entrance/floor-19/roof markers, All Foods
  factory marker, the eleven centroid-snapped `mq061` tour stops, and the
  `{bls_bls_dataterm_}10` fast-travel dataterm.
- `dist/extract/areas.jsonl` — the 5 Biotechnica community areas and their
  entry counts (hotel cluster, Dogtown agents, JapenTown NPC).
- `data/sites/sites.json` — sites 353 (`sts_cct_dtn_04`) and 418
  (`sts_wbr_jpn_01`); all other Biotechnica-relevant places have no site row.
- `data/sites/{guards,triggers,spots,patrols,doors,communities,suitabilities,rosters,spawn_points}.json`
  — hotel interior sub-locations, capture-record richness, and the 5 Biotechnica
  spawn points.
- `data/{factions,districts,sub_territories,landmarks,control_centers}.json` —
  faction id 23, the 2 owned sub-territories, the active CC, CC owners.
- `dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_{0,1,2}.streamingsector.json`
  — absence checks for a Biotechnica Building / Venture Center prefab, and the
  `#05_biofarms_v` vista prefab path.
- `refs/cyberpunk/orphans.swift` — `gamedataDistrict.Badlands_BiotechnicaFlats = 13`,
  `gamedataAffiliation.Biotechnica = 5`.
- `refs/RED4ext.SDK/include/RED4ext/Scripting/Natives/Generated/game/data/District.hpp`
  — same enum in the generated SDK headers.

Wiki (MediaWiki API, wikitext only):

- [Biotechnica](https://cyberpunk.fandom.com/wiki/Biotechnica)
- [Biotechnica Building](https://cyberpunk.fandom.com/wiki/Biotechnica_Building)
- [Biotechnica Hotel](https://cyberpunk.fandom.com/wiki/Biotechnica_Hotel)
- [Biotechnica Flats](https://cyberpunk.fandom.com/wiki/Biotechnica_Flats)
- [Biotechnica Venture Center](https://cyberpunk.fandom.com/wiki/Biotechnica_Venture_Center)
- [Biotechnica Campus](https://cyberpunk.fandom.com/wiki/Biotechnica_Campus) (2045 era, lore only)
- [All Foods](https://cyberpunk.fandom.com/wiki/All_Foods)
- [All Foods Factory](https://cyberpunk.fandom.com/wiki/All_Foods_Factory)
- [Project Nightingale](https://cyberpunk.fandom.com/wiki/Project_Nightingale)
- [Impala Automatics](https://cyberpunk.fandom.com/wiki/Impala_Automatics)
- [Gig: Guinea Pigs](https://cyberpunk.fandom.com/wiki/Gig:_Guinea_Pigs) (`baseid = sts_cct_dtn_04`)
- [Gig: Olive Branch](https://cyberpunk.fandom.com/wiki/Gig:_Olive_Branch) (`baseid = sts_wbr_jpn_01`)
- [Gig: Roads to Redemption](https://cyberpunk.fandom.com/wiki/Gig:_Roads_to_Redemption) (`baseid = sts_ep1_07`)
- [The Pickup](https://cyberpunk.fandom.com/wiki/The_Pickup) (`baseid = q003_maelstrom`)
- [Welcome to Paradise](https://cyberpunk.fandom.com/wiki/Welcome_to_Paradise) (`baseid = mq061`)

Earlier repo research:

- [`docs/research/factions/METHOD.md`](./METHOD.md)
- [`docs/research/factions/arasaka.md`](./arasaka.md)
- [`docs/research/factions/tyger-claws.md`](./tyger-claws.md)

---

## 10. Machine-readable block

Strict JSON for seeding (contract in [`METHOD.md`](./METHOD.md) §10). Every
coordinate was verified against the local record named in `source` on
2026-11-25; none came from the wiki. `null` means `TBD`, never `0`.

```json
{
  "faction_code": "biotechnica",
  "hq": {
    "name": "Biotechnica Protein Flats",
    "district": "Badlands",
    "sub_district": "Badlands",
    "x": -1809.5,
    "y": -4283.5,
    "z": 74.1,
    "source": "data/sub_territories.json bls_biotechnica_flats (territory anchor; equals cc_bls_biotechnica_flats)",
    "confidence": "game-data+wiki"
  },
  "alternate_hqs": [
    {
      "name": "Biotechnica Hotel",
      "district": "CityCenter",
      "sub_district": "Downtown",
      "x": -2156.769,
      "y": 467.99,
      "z": 11.511,
      "source": "dist/extract/markers.jsonl {dtn_04_mp_sm_entrance}",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Biotechnica Building",
      "district": "CityCenter",
      "sub_district": "CorpoPlaza",
      "x": null,
      "y": null,
      "z": null,
      "source": "no local record; wiki infobox only (location = Corporate Plaza) - coordinate TBD",
      "confidence": "wiki"
    }
  ],
  "test_control_point": {
    "name": "Biotechnica Hotel",
    "district": "CityCenter",
    "sub_district": "Downtown",
    "x": -2156.769,
    "y": 467.99,
    "z": 11.511,
    "source": "dist/extract/markers.jsonl {dtn_04_mp_sm_entrance}; data/sites/sites.json site 353 sts_cct_dtn_04",
    "confidence": "game-data+wiki"
  },
  "control_points": [
    {
      "rank": 1,
      "name": "Biotechnica Protein Flats",
      "type": "protein_farm",
      "relevance": 5,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": -1809.5,
      "y": -4283.5,
      "z": 74.1,
      "source": "data/sub_territories.json bls_biotechnica_flats (territory anchor; equals cc_bls_biotechnica_flats)",
      "confidence": "game-data+wiki",
      "interior": false,
      "revenue_streams": ["agriculture", "logistics", "rnd"],
      "nearest_cc_code": "cc_bls_biotechnica_flats",
      "nearest_cc_m": 0.0
    },
    {
      "rank": 2,
      "name": "Biotechnica Hotel",
      "type": "corporate_hotel",
      "relevance": 5,
      "district": "CityCenter",
      "sub_district": "Downtown",
      "x": -2156.769,
      "y": 467.99,
      "z": 11.511,
      "source": "dist/extract/markers.jsonl {dtn_04_mp_sm_entrance}; data/sites/sites.json site 353 sts_cct_dtn_04",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["hospitality", "real_estate"],
      "nearest_cc_code": "cc_dtn_goldsmith_dock",
      "nearest_cc_m": 126.9
    },
    {
      "rank": 3,
      "name": "All Foods Factory",
      "type": "food_processing_plant",
      "relevance": 4,
      "district": "Watson",
      "sub_district": "Northside",
      "x": -771.825,
      "y": 2202.015,
      "z": 50.508,
      "source": "dist/extract/markers.jsonl q003_01b_sm_meat_factory",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["manufacturing", "agriculture", "logistics"],
      "nearest_cc_code": "cc_nid_all_foods_plant",
      "nearest_cc_m": 20.8
    },
    {
      "rank": 4,
      "name": "Biotechnica Building",
      "type": "corporate_hq",
      "relevance": 4,
      "district": "CityCenter",
      "sub_district": "CorpoPlaza",
      "x": null,
      "y": null,
      "z": null,
      "source": "no local record; wiki infobox only (type = Regional HQ, location = Corporate Plaza) - coordinate TBD",
      "confidence": "wiki",
      "interior": true,
      "revenue_streams": ["rnd", "finance", "energy", "manufacturing"],
      "nearest_cc_code": null,
      "nearest_cc_m": null
    },
    {
      "rank": 5,
      "name": "Biotechnica Venture Center",
      "type": "abandoned_development",
      "relevance": 2,
      "district": "Dogtown",
      "sub_district": "Dogtown",
      "x": null,
      "y": null,
      "z": null,
      "source": "no local record; wiki infobox only (owner = Biotechnica (formerly), location = Luxor Heights & Golden Pacific) - coordinate TBD",
      "confidence": "wiki",
      "interior": true,
      "revenue_streams": ["real_estate"],
      "nearest_cc_code": null,
      "nearest_cc_m": null
    }
  ],
  "subdistrict_counts": {
    "Badlands": {"named": 1, "filler": 0},
    "Downtown": {"named": 1, "filler": 0},
    "Northside": {"named": 1, "filler": 0},
    "CorpoPlaza": {"named": 1, "filler": 0},
    "Dogtown": {"named": 1, "filler": 0},
    "JapanTown": {"named": 0, "filler": 1}
  }
}
```
