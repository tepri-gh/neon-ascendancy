# Voodoo Boys — Lore-Relevant Control Points

Status: faction research run, 2026-11-25. One faction, one document.
Scope: replace the generic ~5-control-centres-per-sub-district grid with
lore-relevant, capturable places for the **Voodoo Boys**, with an honest count
per sub-district. Method: this doc conforms to [`METHOD.md`](./METHOD.md);
research snippets, wiki rules, the revenue-code vocabulary and the JSON-block
contract live there.

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Position, site, community, roster or spawn record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/artbook lore with no verified in-game artifact | Tertiary |
| `[inferred]` | Reasoning links a named place to a game record; reasoning stated | Weak, flagged |

No coordinate below is guessed. Every `(x, y, z)` is either copied from a named
record in the local extracts or marked `TBD`.

---

## 1. Summary

The Voodoo Boys are the Haitian-diaspora gang of **Pacifica**, and the strangest
faction in the city: a netrunner collective that treats the Net as a religion.
They do not call themselves Voodoo Boys — the name was applied by outsiders — and
their real name is only told to initiated members. `[wiki]` Membership is
estimated at 50–250 in 2077; the threat level is *low in meatspace, extreme on
the Net*. `[wiki]`

Origins: Haitian refugees moved to Night City in 2062 to build the Pacifica
resort, the Unification War killed the project, and the workers stayed. The
collective that emerged became the district's self-appointed leadership, holding
it against NCPD and corporate eviction. `[wiki]`

**Canon bases (two, and the doc has to model both):**

- **Batty's Hotel**, Coastview — the derelict hotel turned communal marketplace
  with the gang's operational floors. Explicitly "Coastview HQ" in the wiki's
  faction-locations list. `[wiki]`
- **Eventide Resort & Spa / Luxor High Wellness Spa**, Luxor Heights (Dogtown) —
  the Phantom Liberty-era Voodoo Boys cluster led by Slider, with Milko Alexis
  and Ayo Zarin running the spa's two wings. Explicitly "Dogtown HQ". `[wiki]`

Their economy is **not** a street economy in the Tyger Claws sense:

- **Primary income: corporate data theft.** "Hacking databanks and accounts
  within various corporations in search of restricted and top-secret data." `[wiki]`
- **Mercenary netrunning.** Hired out for "hit-and-run netrunning operations or
  exploring any ruined parts of the Old Net." `[wiki]`
- **Information and virtual-currency brokering** — "probable", per the sourcebook. `[wiki]`
- **Extortion by implant blackmail** — Milko Alexis threatens to brick victims'
  implants and organs remotely; he extorts cash and favours from corporate
  employees. `[wiki]`
- **Turf sovereignty** — "enforcing sovereignty on their turf with machetes …
  They do, however, have an aversion to firearms, preferring needles wielded by
  'shadows'." `[wiki]`
- **Dogtown pragmatists** sell bootleg netrunner hardware and hacks made at
  Eventide "under the counter in Kabuki". `[wiki]`

The weight sits in **Coastview** — Batty's Hotel, the chapel, the maglev data
fortress and the butcher shop are all inside a 242 m radius. Dogtown is a second,
smaller, wealthier cluster on the Luxor Heights hill.

---

## 2. Territory

### 2.1 Districts

| Evidence kind | Result |
| --- | --- |
| (a) Wiki/lore | Pacifica: Coastview and West Wind Estate. HQ Batty's Hotel (Coastview) and Eventide (Dogtown). "Neither the NCPD nor the corporations have any power in this area … the Voodoo Boys or one of the locals must give an okay" to enter. `[wiki]` |
| (b) Vanilla map gang panel | `data/districts.json`: Pacifica `["VoodooBoys","Animals"]`, Dogtown `["Barghest"]`. `docs/research/factions-gangs-territories.md` §2.2 records the sub-district panel as VDB+Animals in Coastview and West Wind Estate. Treat the per-sub-district split as `[wiki]`-level; the exact `District_Record.Gangs` arrays were never dumped. |
| (c) Game-data counts | 40 community areas contain Voodoo Boys spawns, **35 of them VDB-dominant**. 3 roster sites / 38 units. 4 owned sub-territories. `[game-data]` |

Owned sub-territories (`sub_territories.initial_owner_faction_id == 5`),
`[game-data]`:

| Sub-territory | Sub-district | Seed display name | Landmark anchor |
| --- | --- | --- | --- |
| `cvi_rollercoaster_beach` (64) | Coastview | Coastview Amusement Strip | `(-2015.1, -1860.7, 18.0)` |
| `cvi_south_boulevard` (65) | Coastview | Coastview South Boulevard | `(-1975.7, -2173.1, 24.3)` |
| `wwd_coastline_ruins` (69) | WestWindEstate | West Wind Coastal Ruins | `(-2573.3, -2422.8, 43.0)` |
| `dt_terra_cognita` (94) | Dogtown | Terra Cognita Ruins | `(-1664.4, -2753.0, 103.0)` |

### 2.2 Sub-district presence

Counts from `dist/extract/areas.jsonl` (any area whose `faction_counts` contains
`voodoo_boys`; "dominant" = `dominant_faction == voodoo_boys`), attributed by the
§3.3 function.

| Sub-district | District | (a) Lore | (b) Vanilla panel | (c) VDB areas (dominant) | VDB-occupied sites* |
| --- | --- | --- | --- | ---: | ---: |
| Coastview | Pacifica | core; HQ Batty's Hotel | VDB + Animals | 20 (16) | 2 |
| Dogtown | Dogtown | PL-era business, Eventide/Luxor | Barghest | 17 (16) | 1 |
| WestWindEstate | Pacifica | core (combat-zone favela) | VDB + Animals | 2 (2) | 0 |
| RanchoCoronado | SantoDomingo | none | 6th Street | 1 (1) | 0 |

\* Deduped `data/sites/sites.json` rows with `default_faction_id == 5` **or** at
least one roster entry resolving to Voodoo Boys. Variants within 25 m collapsed;
none of the three collapsed.

**Reading the counts.** 40 areas is a *presence* number, and most of it is quest
scenery: `q303_com_voodoo_boys_guards` alone contributes 21 entries, and the
`sts_ep1_12` files contribute six separate communities (combat, reinforcement,
after-combat, patrol, main, droids). The numbers that matter for yield are in §7.

**Attribution caveat.** 17 of the 40 VDB areas resolve via
`nearest-subterritory`, not a geocode token — every one of them is a Dogtown
`q30x`/`we_ep1_05`/`sts_ep1_12` quest community with no `cvi`/`wwd`/`dtn` token.
They are all correctly Dogtown by position. Two rows attributed to Coastview by
`nearest-site` are genuinely marginal: `{cs_police_execution_com}_002`
`(-2002, -1781)` and `{cs_highway_patrol_com}_011` `(-1915, -1728)` are
street-crime scenes on the Coastview/West Wind seam, not owned places.

One row is a reused-prefab defect: `{cs_handcuffed_netrunners_com}_015` sits at
`(-98, -2176)` in **Santo Domingo**, 1.8 km from the Coastview cluster. It is a generic
"handcuffed netrunner" crime-scene spawner, not a VDB holding. Do not use it as
evidence anywhere.

---

## 3. Location catalog

Coordinates are world-space metres, `Z` up. "Interior?" means the game has a
distinct interior cell/sector.

| # | Name | Type | District / sub-district | Interior? | Business? (what it earns) | Coordinates (x, y, z) | Coordinate source record | Linked communities / sites | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **Batty's Hotel** | Derelict hotel → gang HQ + communal market | Pacifica / Coastview | Yes — hotel floors above a street-level market | Partly: the squatted hotel is the local marketplace; the upper floors are the gang's operations and Placide's office | `(-1904.1, -1899.2, 59.0)` (den/HQ marker); `(-1901.0, -1889.4, 57.9)` (Placide default); `(-1880.3, -1911.9, 1.2)` (street market level) | `markers.jsonl` `q110_mp_netrunners_den`, `placide_sm_default`; `areas.jsonl` `{pac_cvi_hotel_com}` (hash `4080294110297864769`, 39 entries) | `q110_com_netrunners_den_vdb_bg` (`12741036404421686328`, 6 VDB); `q110_mp_placide_office_sit_down`; enum `Coastview_BattysHotel` | `[game-data]` `[wiki]` |
| 2 | **Pacifica Serenity Bible Church** | Church → community seat + hideout | Pacifica / Coastview | Yes — nave, altar, unfinished basement | No direct revenue; it is the seat of community authority and Placide's fallback. Its basement breaks into the maglev tunnel (3) | `(-1751.1, -1930.3, 63.0)` (entrance); `(-1741.2, -1908.8, 63.3)` (altar) | `markers.jsonl` `q110_mp_chapel_entrance`, `q110_mp_chapel_altar`; prefab `#loc_q110_chapel_of_the_black_madonna` | `q110_com_voodoo_boys_chapel` (`12776738608555617976`, 5 VDB); `sq032_*_church` markers (same building); enum `Coastview_VDBChapel` | `[game-data]` `[wiki]` |
| 3 | **Old Maglev Tunnel / Rezo Agwe** | Abandoned maglev tunnel → netrunning centre + data fortress | Pacifica / Coastview (sub-level under 2) | Yes — tunnel and vault below the chapel | Yes, in the sense that matters: the gang's data fortress is here. No retail revenue | `(-1665.3, -1860.9, 55.0)` (maglev sitting marker); `(-1654.2, -1857.6, 56.7)` (Blackwall vault) | `markers.jsonl` `q110_sm_sitting_in_maglev_temp`, `q110_mp_blackwall_touch` | `q110_lairs_escape_voodoo_boys` (`1855248394112820676`, 7 VDB); `q110_lairs_escape_voodoo_boys_reinforcement` (`17372977922171755686`, 6); `q110_13_sm_alt_intro`; enum `Coastview_VDBMaglev` | `[game-data]` `[wiki]` |
| 4 | **Rolland's Butcher Shop** | Butcher shop → gang front | Pacifica / Coastview | Yes — shop, back room, cold room | Yes: retail butcher counter as cover (open since 2032 per its sign); the back room is where Placide receives visitors | `(-1818.2, -1977.1, 53.5)` (entrance); `(-1820.6, -1962.4, 51.5)` (Placide at the block) | `markers.jsonl` `q110_butcher_shop_enterance`, `q110_02_sm_placide_butcher`; prefab `#loc_q110_butcher_shop` | cold-room and front-door device records under `loc_q110_butcher_shop_devices`; enum `Coastview_ButcherShop` | `[game-data]` `[wiki]` |
| 5 | **Grand Imperial Mall** | Unfinished mallplex | Pacifica / Coastview | Yes — atrium, gallery, cinema, garage | **Not VDB-owned.** Held by Animals then Scavengers; the setting of the gang's NetWatch operation. No revenue to the gang | `(-2228.5, -2241.8, 11.7)` (mall intro); `(-2351.2, -2190.6, 13.3)` (garage entrance) | `markers.jsonl` `q110_06_sm_the_mall_intro`, `q110_mp_mall_garage_entrance`; prefab `#loc_q110_pacifica_mall` | `q110_com_mall_hall` (`areas.jsonl`, snapped to the mall anchor); Animals/Scavenger `de_pac_cvi_04_*`; enum `Coastview_GrandImperialMall` | `[game-data]` `[wiki]` |
| 6 | **Luxor High Wellness Spa** | Unfinished luxury spa → netrunning den | Dogtown / Dogtown | Yes — reception, offices, two wings, changing room | Yes: implant-blackmail extortion, and an implant supply chain via Kyle Araujo. Alexis holds the north wing, Zarin the south | `(-1386.8, -2463.7, 85.0)` (north wing, site 362); `(-1501.9, -2577.6, 103.5)` (south wing, `we_ep1_05`) | `data/sites/sites.json` site 362 `sts_ep1_12`; `areas.jsonl` `{we_ep1_05_com}` (hash `5160266592583725383`, 20 VDB) | `sts_ep1_12_combat_com` (`14942863090746794860`, 15); `sts_ep1_12_droids_den` (`59754140765284077`, 23); rosters `Character.sts_ep1_12_voodoo*`, `Character.sts_ep1_12_milko_alexis`, `Character.sts_ep1_12_alan_noel` | `[game-data]` `[wiki]` |
| 7 | **Eventide Resort & Spa** | Unfinished brutalist resort → Dogtown VDB seat | Dogtown / Dogtown | Yes — basement netrunning den under the resort | Yes: bootleg decks, processors and hacks made here and sold "under the counter in Kabuki"; data protection for Hansen's guests | `(-1638.6, -2782.3, 115.1)` (**area node only**, see §3.1) | `areas.jsonl` `{q303_com_voodoo_boys_rooftop_guards}` (hash `7301818333235257509`, 5 VDB) | `q303_com_voodoo_boys_guards` (21 VDB); `q303_com_voodoo_boys_reinforcements` (10); `q303_com_hill_park_spa_scrappers` (20) | coords `[game-data]`; name link `[inferred]`; ownership `[wiki]` |
| 8 | **The Moth** | Bar | Dogtown / Dogtown | Yes | **Not VDB-owned** (Daphne's bar). Plot location where Reed briefs V before the Eventide infiltration | `(-2425.0, -2660.5, 17.0)` | `areas.jsonl` `{q303_com_nighthawks}` (hash `14460316708907940547`, 9 entries, no faction) — the bar's development name was "Nighthawks" | `q303_com_nighthawks_droid` | `[game-data]` `[wiki]` |
| 9 | J. Edgar Hoover Elementary School | School | TBD | TBD | Unknown | `TBD` | — | — | `[wiki]` only; no wiki page, no game record found |
| 10 | Oceanview I. | TBD | TBD | TBD | Unknown | `TBD` | — | — | `[wiki]` only; no wiki page, no game record found |
| 11 | Skinny Frank's Titties "N" Beer | Bar | TBD | TBD | Yes: bar | `TBD` | — | — | `[wiki]` only; no wiki page, no game record found |

Items 9–11 come from the wiki's explicit *Faction Locations (2077)* list, which
cites the 2077 sourcebook rather than an in-game artifact. They are honest lore
but unseedable.

### 3.1 How the name→coordinate links were proven

The site extractor keeps interior node names, which is what makes interiors
identifiable without a map:

- **Batty's Hotel.** The true proof is in the prefab tree, not in `sites.json`:
  `#loc_q110_netrunners_den` contains `q110_hotel_elevator_prefab`,
  `q110_hotel_front_elevator_prefab` and a trigger named
  `q110_tr_entering_hotel_floor_with_placide`. The "netrunners' den" *is* Batty's
  Hotel's operational floor. `gamedataDistrict` in
  `refs/cyberpunk/orphans.swift` carries a first-class `Coastview_BattysHotel`
  entry (id 35), so the place exists as a mappin target even though no marker is
  named after it.
- **Chapel.** Prefab `#loc_q110_chapel_of_the_black_madonna`; the `sq032_*`
  side-job markers (`sq032_05_sm_fifth_episode_church`,
  `sq032_spwn_player_chapel`) reuse the same doorway at `(-1751.3, -1931.5)`.
  `Coastview_VDBChapel` (id 39) confirms the enum.
- **Maglev.** `q110_sm_sitting_in_maglev_temp`, `q110_spwn_cybermaglev` and
  `q110_mp_blackwall_touch` all sit at z≈55 under the chapel; `Coastview_VDBMaglev`
  (id 40) confirms the enum. This is the "Rezo Agwe" data fortress of
  *Transmission*.
- **Butcher shop.** `q110_butcher_shop_enterance`,
  `#q110_dvc_butcher_shop_front_door`, `_cold_room_door_001/002`; the wiki's
  gig walkthrough names the shop and the vendor. `Coastview_ButcherShop` (id 36).
- **Luxor High Wellness Spa.** Proven by quest id, not by geometry:
  the wiki's *Gig: Treating Symptoms* infobox carries `baseid = sts_ep1_12`,
  and site 362 **is** `sts_ep1_12`. *Increased Criminal Activity: Voodoo Boys*
  carries `baseid = we_ep1_05`, and the `we_ep1_05` communities sit 162 m away.
  The wing split matches the wiki (Alexis north, Zarin south): `sts_ep1_12` at
  y = −2464 is north of `we_ep1_05` at y = −2578. Roster room names
  (`reception_guard_*`, `guard_left_wing_upper_01`, `guard_changing_room`,
  `guard_office`) describe a spa, not a hotel.
- **Eventide.** The weakest link in this doc. `q303_com_voodoo_boys_*` and
  `q303_com_hill_park_spa_scrappers` cluster on the Luxor Heights hilltop at
  z ≈ 103–115, which matches "Eventide as the tallest building in the area"
  and *The Damned*'s "meet Reed near Slider's hideout". But **no marker or
  prefab string in the extract says "Eventide"**, and `hill_park_spa` in the
  same cluster names the *spa*. The cluster may be the spa's outbuildings rather
  than the resort. Treat the name as `[inferred]` and confirm in-game.
- **The Moth.** `{q303_com_nighthawks}` — the wiki records that the bar was
  called *Nighthawks* during development, "visible in concept art and game
  files". That is a clean development-name match, not a guess.

### 3.2 VDB-occupied generic sites with business-like suitability tags

Only two occupied sites are unnamed — the faction's footprint is markers and
quest communities, not sites. These are the whole filler pool.

| Site | Sub-district | Interior | Suitability tags | Units (VDB) | Coordinates | Note |
| --- | --- | --- | --- | ---: | --- | --- |
| `mws_pac_06` | Coastview | no | officer_site (60), rooftop_access (64) | 4 | `(-2109.2, -2033.2, 14.8)` | Mini-world-story ambush with a Trauma Team AV; VDB presence, not ownership. `default_faction_id = 5` is a seed artefact, not a claim on the location |
| `ma_pac_cvi_15` | Coastview | no | raid_target (95), vehicle_bay (65) | 1 | `(-2219.6, -1952.5, 5.7)` | Cyberpsycho scanner hustle in a garage. `default_faction_id = 7` (Scavengers); the single VDB-tagged record is `Character.ma_pac_cvi_15_cyberpsycho`. Not a VDB holding |

`sts_ep1_12` carries `officer_site` (60) and `rooftop_access` (80) but is a named
catalog point, so it is not filler.

---

## 4. Economic structure

### 4.1 Revenue streams → catalog locations

The Voodoo Boys do not run storefronts. Their economy is data, contract
netrunning and coercion, and the shared vocabulary in `METHOD.md` §7 has **no
code for any of those** (see §8, gap 1). The mapping below is the closest honest
fit; every `[inferred]` cell says so.

| Revenue stream | Code(s) | Catalog locations that produce it | Evidence / notes |
| --- | --- | --- | --- |
| Corporate databank and account hacking | `fixer_brokerage` *(closest available)* | Batty's Hotel (1); Old Maglev Tunnel / Rezo Agwe (3); Eventide (7) | "The gang's primary source of income involves hacking databanks and accounts within various corporations." `[wiki]` No exact code exists; `fixer_brokerage` is used only because it is the vocabulary's term for contracted work. `[inferred]` |
| Mercenary netrunning for private contractors | `fixer_brokerage` | Batty's Hotel (1, Placide's office); Luxor (6); Eventide (7) | "The Voodoo Boys also hire themselves out as mercenary netrunners for private contractors." `[wiki]` `[inferred]` |
| Implant-blackmail extortion | `protection` | Luxor High Wellness Spa (6) | Milko Alexis "threatens to fatally damage the implants and synthetic organs of his victims … extorts money and favors from highly placed victims such as corporate employees." `[wiki]` |
| Turf sovereignty / community levy | `protection` | Batty's Hotel (1); Pacifica Serenity Bible Church (2) | "Enforcing sovereignty on their turf with machetes"; the gang is the district's de facto authority. `[wiki]` `[inferred]` for the levy |
| Bootleg netrunner hardware and hacks | `cyberware` *(closest available)* | Eventide (7) | "Overclocked decks, processors with stripped-down safety features, bootleg drivers – these things and more are made in batches … sent off to be sold under the counter in Kabuki." Decks and processors are hardware, so `cyberware` fits better than any other code. `[wiki]` `[inferred]` |
| Implant supply chain | `cyberware` | Luxor High Wellness Spa (6) | Supplier Kyle Araujo "supplies them with implants used for research purposes". `[wiki]` |
| Retail cover | `retail` | Rolland's Butcher Shop (4); Batty's Hotel street market (1) | The butcher shop "served as a front for the Voodoo Boys, in particular for Placide" and has been "open since 2032" on its sign. `[wiki]` |
| Hospitality / market floor | `food_drink` | Batty's Hotel street market (1) | The hotel was "subsequently settled by the locals, turning it into a communal marketplace". `[wiki]` |
| Contract violence ("shadows") | — | Not location-bound | Hologram-skulled assassins using needles; no dedicated site in the extract. `[wiki]` |

Two catalog points have **no revenue code at all**: the Old Maglev Tunnel (data
fortress — the gang's crown jewel and its biggest single asset) and the Grand
Imperial Mall (not theirs). That is a vocabulary failure, not an absence of
value.

### 4.2 Suppliers, customers, rivals

| Role | Party | Detail |
| --- | --- | --- |
| Supplier (implants) | Kyle Araujo | Independent supplier who "has a deal with the Voodoo Boys and supplies them with implants used for research purposes". `[wiki]` |
| Supplier (hardware) | Scavengers / salvage | Terra Cognita and the spa are filled with salvage; scavengers work the same buildings. `[wiki]` `[game-data]` |
| Customer | Private contractors, corporate data buyers | Mercenary netrunning and stolen data. `[wiki]` |
| Customer | Kabuki netrunner market | Bootleg hacks from Eventide sold under the counter at the Kabuki Roundabout. `[wiki]` |
| Customer / protectorate | Kurt Hansen's guests | Dogtown VDB "protect the data of Hansen's guests, covering their tracks through the district's subnets". `[wiki]` |
| Rival | NetWatch | The defining adversary; hunts rogue netrunners and AI contact. Agent Bryce Mosley is the 2077 case. `[wiki]` |
| Rival | Animals | Held the Grand Imperial Mall against the gang. `[wiki]` `[game-data]` |
| Rival | Scavengers | Same buildings in Coastview, West Wind and Luxor Heights. `[game-data]` |
| Rival | Barghest | Territorial host in Dogtown; the VDB cluster is inside Barghest's district and depends on Hansen's tolerance. `[wiki]` `[game-data]` |
| Rival (community) | Pacifica locals / The Mox | `{growl_stand_comm}` is Mox-dominant with 2 VDB records — a shared corner, not a holding. `[game-data]` |
| Fixer | Mr. Hands | The Pacifica/Dogtown fixer who brokers access to the gang in *M'ap Tann Pèlen* and *The Damned*. `[wiki]` |

---

## 5. Headquarters recommendation

### Primary HQ: **Batty's Hotel** — Coastview

Coordinates: den/HQ marker `(-1904.1, -1899.2, 59.0)`; Placide's default
`(-1901.0, -1889.4, 57.9)`; street-market level `(-1880.3, -1911.9, 1.2)`.
`[game-data]` `markers.jsonl` `q110_mp_netrunners_den`, `placide_sm_default`.

Rationale:

1. **It is the canon Coastview HQ, named as such.** The wiki's faction-location
   list opens with "Batty's Hotel (Coastview HQ)" and the infobox lists Batty's
   first. `[wiki]`
2. **The game gives it real management space, at two elevations.** Placide's
   office (`q110_mp_placide_office_sit_down`, z≈58.6), the confrontation room,
   the front and utility elevators, and a 39-entry civilian market community at
   street level (z≈1.2). That is a believable org seat with rooms to assign — and
   a natural "ground floor" for a market economy.
3. **It is the centre of the densest cluster in the game.** The chapel is 156 m
   away, the butcher shop 116 m, the maglev fortress 242 m — the entire Pacifica
   power structure fits inside one control-centre radius.
4. **It is the point where the gang's non-corporate income lives.** The market
   floor and Placide's job-brokering office are the only places in the catalog
   that map to `retail`, `food_drink` and `fixer_brokerage`.
5. **The nearest existing CC is already VDB-owned and 118 m away**
   (`cc_cvi_rollercoaster_beach`, owner fid 5), so retargeting costs no new
   plumbing.
6. **A first-class mappin enum exists** (`Coastview_BattysHotel`, id 35) even
   though no marker carries the name — so the map layer can address it without
   inventing a location.

Trade-off: Batty's is a squatted ruin, not a fortress — the gang's real
fortification is the maglev data fortress *under* the chapel, 242 m away. That is
arguably correct: the Voodoo Boys' power is not physical security on their own
premises, it is the Blackwall. The HQ reads as "communal seat + operations" rather
than "bunker".

### Alternate 1: **Luxor High Wellness Spa** — Dogtown

Coordinates `(-1386.8, -2463.7, 85.0)` `[game-data]` site 362 `sts_ep1_12`;
south wing `(-1501.9, -2577.6, 103.5)`.

The strongest *building* in the catalog after Batty's: two wings, reception,
offices, a changing room, 33 VDB roster units, six door records (three named —
`corridor_door`, `final_room_door`, `glass_droid_door`), a dedicated droid den and
a 20-unit second-wave community. Proven by quest id (`baseid = sts_ep1_12`) rather
than by name inference. It loses because the wiki calls Eventide the "Dogtown HQ"
and because Dogtown is Barghest's district — the VDB hold it at Hansen's pleasure.

### Alternate 2: **Eventide Resort & Spa** — Dogtown

Coordinates `(-1638.6, -2782.3, 115.1)` (area node) `[game-data]` `[inferred]`.

Lore-strong: the wiki's second named HQ, and the seat of Slider, "the real tech
wizards". It loses on coordinate certainty — no marker or prefab string names it,
the cluster it sits in also contains `hill_park_spa` (the *other* spa), and the
guards community's recorded position is degenerate (see §8, gap 2).

### Overruled / downgraded suggestions

- **Pacifica Serenity Bible Church as HQ.** The most iconic VDB space in the game
  (*Transmission*, the funeral, the Hermit tarot), and a strong capture target.
  But it is a chapel the gang *uses*, not where it administers from, and it has
  no site row, no guard records and only a 5-entry VDB community. Keep
  it as the rank-3 control point.
- **Old Maglev Tunnel / Rezo Agwe as HQ.** This is where the gang's actual power
  lives, so it is tempting. Rejected on two grounds: it is a sub-level of the
  chapel (so it would double-count the seat), and it has no revenue code — a HQ
  with zero economy is useless to the simulation.
- **`dt_terra_cognita` as the Dogtown seat.** The seed owns this sub-territory
  and the `q303` VDB cluster is 0 m from its centroid — but that 0 m is an
  artefact, not a fact. Terra Cognita is a Scavenger-occupied tech park in lore;
  see §8, gap 3.
- **Grand Imperial Mall as an HQ or holding.** Not VDB-owned at any point; Animals
  held it, then Scavengers picked it over. It is a mission site.

---

## 6. Priority list of control points

Ranked by how well each place serves as a capturable Voodoo Boys control point.
"CC" = nearest entry in `data/control_centers.json`; distance is horizontal
metres, computed over **all** CCs regardless of `is_active`.

| Rank | Control point | Rel. (1–5) | District / sub-district | Coordinates | Existing CC overlap | Why |
| ---: | --- | :---: | --- | --- | --- | --- |
| 1 | **Batty's Hotel** | 5 | Pacifica / Coastview | `-1904.1, -1899.2, 59.0` | `cc_cvi_rollercoaster_beach`, 117.7 m (**owner VDB**) | Canon Coastview HQ; market floor + Placide's office; centre of the chapel/butcher/maglev cluster |
| 2 | **Luxor High Wellness Spa** | 5 | Dogtown / Dogtown | `-1386.8, -2463.7, 85.0` | `cc_dt_terra_cognita`, 401.0 m (VDB) | Only building proven by quest id; 33 units; two wings; extortion and implant economy; richest record set |
| 3 | **Pacifica Serenity Bible Church** | 5 | Pacifica / Coastview | `-1751.1, -1930.3, 63.0` | `cc_cvi_rollercoaster_beach`, 273.0 m (VDB) | The gang's public face and community seat; iconography; the funeral; doorway to the data fortress |
| 4 | **Eventide Resort & Spa** | 5 | Dogtown / Dogtown | `-1638.6, -2782.3, 115.1` (`[inferred]`) | `cc_dt_terra_cognita`, 39.0 m (VDB) | Canon Dogtown HQ; Slider's den; bootleg-hardware production; nearly free — the CC is 39 m away |
| 5 | **Old Maglev Tunnel / Rezo Agwe** | 4 | Pacifica / Coastview | `-1665.3, -1860.9, 55.0` | `cc_cvi_rollercoaster_beach`, 349.8 m (VDB) | The data fortress, the gang's actual crown jewel; enclosed sub-level; no revenue code, which caps relevance at 4 |
| 6 | **Rolland's Butcher Shop** | 4 | Pacifica / Coastview | `-1818.2, -1977.1, 53.5` | `cc_cvi_rollercoaster_beach`, 228.7 m (VDB) | Placide's front; retail cover; small interior with a cold room and working front doors |
| 7 | **Grand Imperial Mall** | 3 | Pacifica / Coastview | `-2228.5, -2241.8, 11.7` | `cc_dt_main_gate`, 179.9 m (owner Barghest) | Not theirs, but the setting of their biggest operation (*I Walk the Line*); contested ground with Animals and Scavengers |
| 8 | **The Moth** | 2 | Dogtown / Dogtown | `-2425.0, -2660.5, 17.0` | `cc_dt_longshore_stacks`, 157.0 m (owner Barghest) | Not VDB-owned; a plot point where the gang's Dogtown operation is planned. Adjacency/modifier only |

### Test control point for the first in-game test: **Luxor High Wellness Spa (site 362)**

Why this and not the HQ or a street:

- **Fully enclosed, verifiable interior.** Three doors
  (`#sts_ep1_12_corridor_door`, `#sts_ep1_12_final_room_door`,
  `#sts_ep1_12_glass_droid_door`) and roster room names
  (`reception_guard_01/02`, `guard_left_wing_upper_01`,
  `guard_left_wing_down_01/02`, `guard_changing_room`, `guard_office`,
  `guard_main_hall`) describe a real multi-room building, so a capture radius can
  be validated against geometry. `is_interior` is unset, which proves nothing
  either way (§2.2 of METHOD).
- **Clean ownership.** `default_faction_id = 5` and `sub_territory_id 94` — who
  is being evicted is unambiguous.
- **The richest record set the faction has.** 33 roster units across a
  15-entry combat community, an 8-entry reinforcement, a 4-entry after-combat
  patrol, a 23-entry droid den, plus doors and devices. Every hook a
  capture/defence prototype needs is present and named.
- **It is not the HQ**, so the first test exercises capture on a non-seat.
- **It is distinct from the existing grid**, unlike the rank-1 HQ or Eventide —
  which is exactly what a first test should prove.

Trade-off: the nearest CC (`cc_dt_terra_cognita`) is 401 m away, so this test
needs a CC retarget or a new anchor. If avoiding new map plumbing matters more
than distinctness, **Eventide** (39 m from its CC, 26 VDB units) is the fallback —
but its coordinate is the weakest in the contract.

---

## 7. Per-sub-district count of lore-relevant locations

This is the number to feed yield balancing. It counts **distinct named places**
the gang owns, runs, protects or habitually occupies — not quest-scene variants
and not generic occupied blocks. `Filler` is the deduped occupied-site count minus
any site already counted as a named place (METHOD §8).

| Sub-district | Named lore-relevant places | Which ones | VDB-occupied sites (deduped, `[game-data]`) | Filler | Noteworthy interiors |
| --- | ---: | --- | ---: | ---: | ---: |
| Coastview | **5** | Batty's Hotel, Pacifica Serenity Bible Church, Old Maglev Tunnel, Rolland's Butcher Shop, Grand Imperial Mall | 2 | 2 | 5 (hotel floors, chapel nave, maglev tunnel, butcher shop, mall) |
| Dogtown | **3** | Luxor High Wellness Spa, Eventide Resort & Spa, The Moth | 1 | 0 | 3 |
| WestWindEstate | **0** | presence only | 0 | 0 | 0 |
| RanchoCoronado | **0** | reused-prefab anomaly (§2.2) | 0 | 0 | 0 |
| **Total** | **8** | | 3 | 2 | 8 |

Plus three wiki-only named places with no coordinate (**J. Edgar Hoover Elementary
School**, **Oceanview I.**, **Skinny Frank's Titties "N" Beer**). They are real
lore but cannot be counted or seeded until located — see §8.

Reconciliation:

- 8 named + 2 filler = 10.
- 3 deduped occupied sites + 7 marker/area-only named places = 10. ✓
- 1 of the 8 named is site-backed (Luxor = `sts_ep1_12`); the other 7 are
  marker/area-only (Batty's, Chapel, Maglev, Butcher, Mall, Eventide, Moth).
- The 2 filler sites are both Coastview (`mws_pac_06`, `ma_pac_cvi_15`), which is
  why Dogtown's filler is zero despite 17 VDB areas: every Dogtown VDB area
  belongs to a named place.

Interpretation for yield: **Coastview is the economy and Dogtown is the wealth.**
Coastview has five named points but two of them (chapel, data fortress) earn
almost nothing — they are authority and infrastructure. Dogtown has three named
points and all three are runnable businesses (extortion, hardware, data
protection). If per-point yield should reflect money rather than lore, Dogtown's
three points should out-earn Coastview's five.

If 8 named points is too few for the map, the §3.2 filler table is the honest
pool — but it is only two sites, both generic. The better lever for this faction
is **interior sub-points**: Batty's Hotel alone has a market floor and an office
floor at z = 1 and z = 58, and the Luxor has two wings 162 m apart.

---

## 8. Gaps and uncertainties

1. **The revenue vocabulary has no code for this faction's actual business.** No
   `data_theft`, `hacking`, `information_brokering`, `netrunning` or
   `blackmail`. The gang's stated primary income — corporate databank and account
   hacking — maps to nothing. I used `fixer_brokerage` (contract netrunning) and
   `cyberware` (bootleg decks/processors) as the closest fits and tagged them
   `[inferred]`, but the Old Maglev Tunnel/Rezo Agwe — the single most important
   Voodoo Boys asset — ends up with an empty `revenue_streams` list. This is a
   playbook gap, not a data gap.
2. **Eventide's coordinate is an area node, and one of its sibling areas is
   degenerate.** `{q303_com_voodoo_boys_guards}` (21 units, the largest single VDB
   Dogtown garrison) is recorded at `(-1664.435, -2752.964)`, which is *exactly*
   the `dt_terra_cognita` sub-territory centroid to the millimetre. That is a
   snapped coordinate, not a real position. I therefore anchored Eventide on
   `{q303_com_voodoo_boys_rooftop_guards}` `(-1638.6, -2782.3, 115.1)`, which is
   not centroid-snapped. **This is a METHOD blind spot**: §3.3 assigns a row to
   `nearest-subterritory` and flags it `[inferred]`, but it never warns that the
   *coordinate itself* may have been replaced by the centroid. Any agent that
   uses such a row as an anchor will silently produce a 0 m nearest-CC.
3. **`dt_terra_cognita` is seeded to the Voodoo Boys but Terra Cognita is
   Scavenger ground.** The wiki lists Terra Cognita's gang as Scavengers, and the
   `sts_ep1_01` site inside the sub-territory is Scavenger-occupied. The seed
   almost certainly assigned it because the Luxor spa gigs (sub_territory 94) had
   no closer cell. Recommend moving the `sts_ep1_12` anchor out of
   `dt_terra_cognita` into a Luxor-specific sub-territory.
4. **The seeded `dt_luxor_heights` landmark is 782 m from the real spa.**
   `data/landmarks.json` anchor 95 ("Luxor High Wellness Spa") sits at
   `(-2134.3, -2692.7, 78.6)`, while the verified spa interior (`sts_ep1_12`, proven
   by `baseid`) is at `(-1386.8, -2463.7, 85.0)`. Seven `q301_com_crashsite_*`
   communities are snapped to that same landmark centroid. Do not use the landmark
   anchor as the spa's position.
5. **Eventide's name link is inferred, not proven.** See §3.1. No marker, prefab
   string or community name in the extract says "Eventide"; the cluster also
   contains `q303_com_hill_park_spa_scrappers`, which names the *other* spa on the
   same hill.
6. **Three wiki-named locations have no coordinate at all.** J. Edgar Hoover
   Elementary School, Oceanview I. and Skinny Frank's Titties "N" Beer appear only
   in the faction-location list (citing the 2077 sourcebook) and have no wiki page
   and no game record I could find. Keep them `TBD`/`[wiki]` and do not seed.
7. **No vendor or shop record proves what any Voodoo Boys business sells.** The
   extract has suitability tags but no inventories. All "what it earns" statements
   come from wiki database entries, not vendor data.
8. **Only two occupied sites exist, so the filler pool is thin.** `mws_pac_06` is
   a Trauma Team ambush and `ma_pac_cvi_15` is a cyberpsycho scanner hustle whose
   single VDB record is arguably a mislabelled gang assignment. Neither is a
   business. This faction genuinely has almost no *site* footprint — the pilot's
   43 sites collapse to 3 here.
9. **`is_interior` is unset for every VDB site.** All `interior: true` values in
   this doc rest on node names and prefab structure, not the flag. That flag is set
   for 17 of 424 sites and is silent on these three.
10. **Grand Imperial Mall's gang attribution moved between builds.** Animals held
   it in 2077's main job, Scavengers "scoured the place for valuables" after. The
   extract still carries `de_pac_cvi_04_animals_com` and `de_pac_cvi_04_scavengers_com`
   at the same coordinate. Treat mall ownership as contested, never as stable.

---

## 9. Sources

- Local: `dist/extract/areas.jsonl`, `dist/extract/markers.jsonl`,
  `data/sites/{sites,communities,rosters,guards,triggers,spots,patrols,doors,devices,suitabilities,meta}.json`,
  `data/{districts,factions,control_centers,sub_territories,landmarks}.json`,
  `dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_{0,1}.streamingsector.json`
  (prefab and node-name strings only),
  `refs/cyberpunk/orphans.swift` (`gamedataDistrict` enum, ids 34–41).
- Wiki: [Voodoo Boys](https://cyberpunk.fandom.com/wiki/Voodoo_Boys),
  [Batty's Hotel](https://cyberpunk.fandom.com/wiki/Batty%27s_Hotel),
  [Pacifica Serenity Bible Church](https://cyberpunk.fandom.com/wiki/Pacifica_Serenity_Bible_Church),
  [Old Maglev Tunnel](https://cyberpunk.fandom.com/wiki/Old_Maglev_Tunnel),
  [Rolland's Butcher Shop](https://cyberpunk.fandom.com/wiki/Rolland%27s_Butcher_Shop),
  [Grand Imperial Mall](https://cyberpunk.fandom.com/wiki/Grand_Imperial_Mall),
  [Luxor High Wellness Spa](https://cyberpunk.fandom.com/wiki/Luxor_High_Wellness_Spa),
  [Eventide Resort & Spa](https://cyberpunk.fandom.com/wiki/Eventide_Resort_%26_Spa),
  [Slider's Hideout](https://cyberpunk.fandom.com/wiki/Slider%27s_Hideout),
  [Luxor Heights](https://cyberpunk.fandom.com/wiki/Luxor_Heights),
  [The Moth](https://cyberpunk.fandom.com/wiki/The_Moth),
  [Terra Cognita](https://cyberpunk.fandom.com/wiki/Terra_Cognita),
  [Coastview](https://cyberpunk.fandom.com/wiki/Coastview_(2077)),
  [West Wind Estate](https://cyberpunk.fandom.com/wiki/West_Wind_Estate),
  [M'ap Tann Pèlen](https://cyberpunk.fandom.com/wiki/M%27ap_Tann_P%C3%A8len),
  [Transmission](https://cyberpunk.fandom.com/wiki/Transmission),
  [I Walk the Line](https://cyberpunk.fandom.com/wiki/I_Walk_the_Line),
  [The Damned](https://cyberpunk.fandom.com/wiki/The_Damned),
  [Gig: Treating Symptoms](https://cyberpunk.fandom.com/wiki/Gig:_Treating_Symptoms),
  [Increased Criminal Activity: Voodoo Boys](https://cyberpunk.fandom.com/wiki/Increased_Criminal_Activity:_Voodoo_Boys),
  [Milko Alexis](https://cyberpunk.fandom.com/wiki/Milko_Alexis),
  [Ayo Zarin](https://cyberpunk.fandom.com/wiki/Ayo_Zarin).
- Earlier repo research: `docs/research/factions-gangs-territories.md`
  (§2.2 Pacifica sub-districts, §4.5),
  `docs/research/game-data-extraction.md`.

---

## 10. Machine-readable block

Strict JSON for seeding (contract in [`METHOD.md`](./METHOD.md) §10). Every
coordinate was re-verified against the local record named in `source` on
2026-11-25; none came from the wiki.

```json
{
  "faction_code": "voodoo_boys",
  "hq": {"name": "Batty's Hotel", "district": "Pacifica", "sub_district": "Coastview", "x": -1904.122, "y": -1899.187, "z": 59.007, "source": "dist/extract/markers.jsonl q110_mp_netrunners_den", "confidence": "game-data+wiki"},
  "alternate_hqs": [
    {"name": "Luxor High Wellness Spa", "district": "Dogtown", "sub_district": "Dogtown", "x": -1386.757, "y": -2463.72, "z": 85.0, "source": "data/sites/sites.json site 362 sts_ep1_12", "confidence": "game-data+wiki"},
    {"name": "Eventide Resort & Spa", "district": "Dogtown", "sub_district": "Dogtown", "x": -1638.649, "y": -2782.33, "z": 115.079, "source": "dist/extract/areas.jsonl {q303_com_voodoo_boys_rooftop_guards} (name link inferred)", "confidence": "game-data+inferred+wiki"}
  ],
  "test_control_point": {"name": "Luxor High Wellness Spa", "district": "Dogtown", "sub_district": "Dogtown", "x": -1386.757, "y": -2463.72, "z": 85.0, "source": "data/sites/sites.json site 362 sts_ep1_12", "confidence": "game-data+wiki"},
  "control_points": [
    {"rank": 1, "name": "Batty's Hotel", "type": "hotel_hq", "relevance": 5, "district": "Pacifica", "sub_district": "Coastview", "x": -1904.122, "y": -1899.187, "z": 59.007, "source": "dist/extract/markers.jsonl q110_mp_netrunners_den", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["fixer_brokerage", "retail", "food_drink", "protection"], "nearest_cc_code": "cc_cvi_rollercoaster_beach", "nearest_cc_m": 117.7},
    {"rank": 2, "name": "Luxor High Wellness Spa", "type": "wellness_spa", "relevance": 5, "district": "Dogtown", "sub_district": "Dogtown", "x": -1386.757, "y": -2463.72, "z": 85.0, "source": "data/sites/sites.json site 362 sts_ep1_12", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["protection", "cyberware", "fixer_brokerage"], "nearest_cc_code": "cc_dt_terra_cognita", "nearest_cc_m": 401.0},
    {"rank": 3, "name": "Pacifica Serenity Bible Church", "type": "church", "relevance": 5, "district": "Pacifica", "sub_district": "Coastview", "x": -1751.102, "y": -1930.32, "z": 62.992, "source": "dist/extract/markers.jsonl q110_mp_chapel_entrance", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["protection"], "nearest_cc_code": "cc_cvi_rollercoaster_beach", "nearest_cc_m": 273.0},
    {"rank": 4, "name": "Eventide Resort & Spa", "type": "resort", "relevance": 5, "district": "Dogtown", "sub_district": "Dogtown", "x": -1638.649, "y": -2782.33, "z": 115.079, "source": "dist/extract/areas.jsonl {q303_com_voodoo_boys_rooftop_guards} (name link inferred)", "confidence": "game-data+inferred+wiki", "interior": true, "revenue_streams": ["cyberware", "protection"], "nearest_cc_code": "cc_dt_terra_cognita", "nearest_cc_m": 39.0},
    {"rank": 5, "name": "Old Maglev Tunnel (Rezo Agwe)", "type": "data_fortress", "relevance": 4, "district": "Pacifica", "sub_district": "Coastview", "x": -1665.273, "y": -1860.944, "z": 55.021, "source": "dist/extract/markers.jsonl q110_sm_sitting_in_maglev_temp", "confidence": "game-data+wiki", "interior": true, "revenue_streams": [], "nearest_cc_code": "cc_cvi_rollercoaster_beach", "nearest_cc_m": 349.8},
    {"rank": 6, "name": "Rolland's Butcher Shop", "type": "butcher_shop", "relevance": 4, "district": "Pacifica", "sub_district": "Coastview", "x": -1818.236, "y": -1977.06, "z": 53.545, "source": "dist/extract/markers.jsonl q110_butcher_shop_enterance", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["retail", "protection"], "nearest_cc_code": "cc_cvi_rollercoaster_beach", "nearest_cc_m": 228.7},
    {"rank": 7, "name": "Grand Imperial Mall", "type": "mall", "relevance": 3, "district": "Pacifica", "sub_district": "Coastview", "x": -2228.524, "y": -2241.808, "z": 11.737, "source": "dist/extract/markers.jsonl q110_06_sm_the_mall_intro", "confidence": "game-data+wiki", "interior": true, "revenue_streams": [], "nearest_cc_code": "cc_dt_main_gate", "nearest_cc_m": 179.9},
    {"rank": 8, "name": "The Moth", "type": "bar", "relevance": 2, "district": "Dogtown", "sub_district": "Dogtown", "x": -2424.977, "y": -2660.504, "z": 17.032, "source": "dist/extract/areas.jsonl {q303_com_nighthawks}", "confidence": "game-data+wiki", "interior": true, "revenue_streams": [], "nearest_cc_code": "cc_dt_longshore_stacks", "nearest_cc_m": 157.0}
  ],
  "subdistrict_counts": {
    "Coastview": {"named": 5, "filler": 2},
    "Dogtown": {"named": 3, "filler": 0},
    "WestWindEstate": {"named": 0, "filler": 0},
    "RanchoCoronado": {"named": 0, "filler": 0}
  }
}
```
