# Tyger Claws — Lore-Relevant Control Points (Pilot)

Status: pilot research run, 2026-11-25. One faction, one document.
Scope: turn the current generic ~5-control-centres-per-sub-district grid into
lore-relevant, capturable places for the Tyger Claws, with an honest count per
sub-district. Method: this doc conforms to
[`METHOD.md`](./METHOD.md); research snippets, the wiki rules, the revenue-code
vocabulary, and the JSON-block contract live there.

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Position, site, community, roster or spawn record read from `dist/extract/` or `data/sites/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/artbook/tabletop lore with no in-game artifact verified here | Tertiary |
| `[inferred]` | My inference linking a named place to a game record; reasoning stated | Weak, flagged |

No coordinate below is guessed. Every `(x, y, z)` is either copied from a named
record in the local extracts or marked `TBD`.

---

## 1. Summary

The Tyger Claws (虎鉤衆) are Night City's largest and most business-like gang:
≈5,500 members in 2077, a Yakuza-style structure, and a 2077 headquarters in
**Japantown** (Westbrook), with a second power base in **Kabuki / Little China**
(Watson) and a foothold in **Charter Hill** and **North Oak**. `[wiki]`
*The World of Cyberpunk 2077* describes them as owning more businesses than any
other gang — bars, restaurants, braindance clubs, brothels and casinos, many of
them legal fronts for laundering. `[wiki]`

Their economic model is entertainment plus exploitation:

- **Prostitution / dollhouses / human trafficking** — the single largest income
  stream. Clouds is the flagship; Jig-Jig Street is the retail strip. `[wiki]`
- **Gambling** — pachinko, mahjong, chō-han, blackjack and roulette in
  Tyger-run parlors and hidden casinos. `[wiki]`
- **Nightlife and braindance** — clubs and BD venues, including illegal XBD
  production out of Ho-Oh's top floor. `[wiki]`
- **Drugs** — manufacture and distribution, notably "glitter". `[wiki]`
- **Protection / security rackets** — inherited from the Kimen-Gumi
  guardian-gang era; protection fees on market stalls and local businesses.
  `[wiki]`
- **Contract violence** — the gang hires out for hits, and its Arasaka ties pay
  in cybertechnology and military-grade automatics. `[wiki]`

The gang is materially concentrated in **JapanTown (Westbrook)**, **Kabuki** and
**LittleChina (Watson)** — together 95 of the 135 community areas containing
Tyger Claws spawns in the extract. The richest single point is the
Jig-Jig Street / Megabuilding H8 cluster: Clouds, Jig-Jig Street, Wakako's
pachinko parlor and Fingers' clinic all sit within ~180 m of one another.

---

## 2. Territory

### 2.1 Districts

Wiki locations are Westbrook and Watson. Evidence in three kinds:

| Evidence kind | Result |
| --- | --- |
| (a) Wiki/lore | Operates out of Japantown (HQ 2077), with major presence in Little China, Kabuki and Charter Hill. `[wiki]` |
| (b) Vanilla map gang panel | `District_Record.Gangs` data in `data/districts.json`: Watson `["Maelstrom","TygerClaws"]`, Westbrook `["TheMox","TygerClaws"]`. The earlier research (`docs/research/factions-gangs-territories.md` §2.2) records the sub-district panel as TC in Kabuki, Little China, Japantown and Charter Hill. Exact per-record arrays were never dumped, so treat the sub-district list as `[wiki]`-level. |
| (c) Game-data counts | 135 community areas in `dist/extract/areas.jsonl` contain Tyger Claws spawns; 122 of them are TC-dominant. 122 TC spawn points in `data/spawn_points.json`. |

### 2.2 Sub-district presence

Counts are from `dist/extract/areas.jsonl` (any area whose `faction_counts`
contains `tyger_claws`; "dominant" means `dominant_faction == tyger_claws`)
and `data/spawn_points.json` (`faction_id == 2`).

| Sub-district | District | (a) Lore | (b) Vanilla panel | (c) TC areas (dominant) | (c) TC spawn pts | TC-occupied sites* |
| --- | --- | --- | --- | ---: | ---: | ---: |
| JapanTown | Westbrook | HQ, core | Tyger Claws | 35 (34) | 36 | 14 |
| LittleChina | Watson | core | Tyger Claws | 32 (30) | 28 | 7 |
| Kabuki | Watson | core | Tyger Claws (+Maelstrom, Mox) | 28 (27) | 31 | 7 |
| Northside | Watson | raids/pressure | Maelstrom (+Mox, Scavs) | 10 (10) | 7 | 4 |
| CharterHill | Westbrook | presence | Tyger Claws (+6th Street) | 6 (5) | 5 | 1 |
| NorthOaks | Westbrook | shrine presence | — | 2 (1) | 2 | 3 |
| Glen | Heywood | minor | Valentinos | 5 (3) | 2 | 1 |
| VistaDelRey | Heywood | minor | Valentinos (+6th Street) | 5 (4)† | 3 | 2† |
| Downtown | CityCenter | minor | — (corp) | 4 (4) | 5 | 3 |
| CorpoPlaza | CityCenter | incidental | — (corp) | 2 (2) | 1 | 0 |
| Wellsprings | Heywood | incidental | Valentinos | 1 (1) | 1 | 0 |
| Arroyo | SantoDomingo | incidental only | 6th Street | 2 (0) | 0 | 0 |
| Coastview | Pacifica | incidental only | Voodoo Boys, Animals | 2 (0) | 0 | 0 |
| Badlands | Badlands | incidental only | Aldecaldos, Wraiths | 1 (1) | 1 | 1 |

\* Deduped `data/sites/sites.json` rows with `default_faction_id == 2` **or** at
least one roster entry resolving to Tyger Claws; variants within 25 m of a kept
site are collapsed.  
† Data anomaly: `rey_09_com_enemies` and `sts_hey_rey_09` carry Heywood/Vista
del Rey codes but their world coordinates are `(-537, 1292)` — inside
JapanTown. They are a reused prefab, not a real Vista del Rey holding. Do not
use them as Heywood evidence.

**Reading the counts.** Community-area counts measure *presence*, not
"lore-relevant places". A single quest scene can contribute five areas (Ho-Oh
alone has `kab_07_com_enemies`, `_enemy_2nd_floor`, `_enemy_ground_floor`,
`_backup`, `_jotaro`, `_enemies_hard_mode`). The per-sub-district counts that
matter for yield balancing are in §7.

**Attribution caveat (important for the next 14 agents).** `areas.jsonl`
`district_code` is derived from the sector path and is **wrong for quest
communities in `always_loaded_*`**. Example: `q105_com_dollhouse` and
`q105_com_jigjig` are labelled `watson` but sit at `(-663, 818)` /
`(-648, 840)`, i.e. JapanTown, Westbrook. This is defect B from
`docs/research/game-data-extraction.md` §5.5. Classify by world position or by
the geocode token, not by `district_code`, for these rows.

---

## 3. Location catalog

Coordinates are world-space metres, `Z` up. "Interior?" means the game has a
distinct interior cell/sector for it.

| # | Name | Type | District / sub-district | Interior? | Business? (what it earns) | Coordinates (x, y, z) | Coordinate source record | Linked communities / sites | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **Clouds** | Dollhouse + BD nightclub | Westbrook / JapanTown | Yes — Megabuilding H8, floor 12 | Yes: dolls, braindance sessions, bar, VIP lounges; managed on behalf of the gang | `-662.7, 806.9, 129.9` (entrance); `-647.2, 788.8, 128.3` (bar/mood) | `markers.jsonl` `q105_mp_dollhouse_entrance`, `q105_03_sm_dollhouse_mood` | `q105_com_dollhouse` (hash `16387341840722333952`, 40 entries, TC-dominant); `q105_com_dollhouse_combat` (`9072495238026906025`); `sq026_com_hiromi` (`960242555655014674`, z 326 penthouse); enum `JapanTown_Clouds` | `[game-data]` `[wiki]` |
| 2 | **Megabuilding H8** | Megabuilding / landmark | Westbrook / JapanTown | Yes | No (hosts Clouds; residential/commercial) | `-685.8, 804.6, 36.3` (ground lift) | `markers.jsonl` `q105_dvc_dollhouse_lift_marker_ground` | lifts `q105_dvc_dollhouse_lift_marker_{start,ground,dollhouse,penthouse}`; enum `JapanTown_MegabuildingH8` | `[game-data]` |
| 3 | **Jig-Jig Street** | Red-light market street | Westbrook / JapanTown | No (open street + shop interiors) | Yes: joytoy brothels, sex shops, cheap food, drug dealers, exotic/illegal goods | `-628.7, 814.9, 18.4` | `markers.jsonl` `q105_04_sm_jigjig_street` | `q105_com_jigjig` (`15061672145614503587`, 41 entries, unaffiliated crowd); `wbr_jpn_jig_jig_com` (`9775908478804321095`); `wbr_jpn_jig_bar_com}_001` (`9162784245789098864`) | `[game-data]` `[wiki]` |
| 4 | **Pachinko Parlor (Wakako's Den)** | Gambling hall + fixer office | Westbrook / JapanTown | Yes | Yes: pachinko receipts; backroom is Wakako Okada's fixer office | `-657.3, 826.7, 19.5`; shop spawn `-642.3, 831.8, 18.8` | `markers.jsonl` `q112_mp_wakakos_pachinko_parlor`, `q112_spwn_wakakos_shop`; enum `JapanTown_Wakakos_Pachinko_Parlor` | `wakako_sm_okada_default` marker; no community area resolves to it | `[game-data]` `[wiki]` |
| 5 | **Fingers M.D.** | Ripperdoc clinic | Westbrook / JapanTown | Yes — 2nd floor flophouse | Yes: ripperdoc vendor, second-hand cyberware; receives "orphaned" chrome | `-580.3, 801.5, 20.9` (entrance); `-568.8, 800.3, 24.9` (office) | `markers.jsonl` `q105_05_sm_fingers_enter`, `mirror_sm_scene_fingers` | `wbr_jpn_jig_fingers_com` (`7240679868225457420`) | `[game-data]` coords; `[wiki]` role; **not TC-owned**, TC-turf fixture |
| 6 | **Ho-Oh** | Casino + club + XBD studio | Watson / Kabuki | Yes — 3 floors + garage | Yes: pachinko, mahjong, chō-han, blackjack, bar, private rooms; top floor is Jotaro Shobo's XBD studio and surgery room | `-1040.2, 1349.6, 9.2` (site anchor); casino floor `-1029.5, 1343.0, 4.6`; 2nd floor `-1036.8, 1342.2, 13.0` | `data/sites/sites.json` site 397 `sts_wat_kab_07` (`is_interior=1`); `guards.json` `#kab_07_guard_area_casino_floor`, `#kab_07_guard_area_2nd_floor_jotaro` | `kab_07_com_enemies` (`2775412478900225177`, 15 TC); `kab_07_com_jotaro` (`3594897492421537272`); rosters `Character.kab_07_enemy_*`, `Character.sts_wat_kab_07_jotaro`, `Character.kab_07_hologram_girl` | `[game-data]` `[wiki]` |
| 7 | **Kabuki Market (Kabuki Roundabout)** | Marketplace / black market | Watson / Kabuki | No (open-air, vendor cells) | Yes: street stalls selling high-end brands cheap; vendor hub (Buck-A-Slice, Edge Net, Straight Shooters; Bucks' Clinic, Dr. Chrome nearby) | `-1231.5, 1965.0, 8.0`; area node `-1231.3, 1959.9, 3.8` | `triggers.json` `#kab_08_tr_marketplace` (site 398); `areas.jsonl` `kab_08_com_tyger_claws` | `kab_08_com_marketplace` (`12651732976986022281`, 22 entries, no dominant faction); `kab_08_com_tyger_claws` (`526896125729211230`, 9 TC) | `[game-data]` `[wiki]` |
| 8 | Kabuki pachinko parlor (unnamed) | Gambling hall | Watson / Kabuki | Yes | Yes: pachinko receipts | `-1180.7, 1764.0, 23.4`; parlor volume `-1172.7, 1772.8, 23.4` | `data/sites/sites.json` site 402 `sts_wat_kab_107`; `triggers.json` `#kab_107_tr_pachinko_parlor` | 4 TC roster units; `kab_107_combat_com` (`-1176.7, 1755.1`) | `[game-data]` (no wiki name) |
| 9 | **Deravaja Dojo** | Dojo / fight venue | Watson / LittleChina | Yes — hall + basement | Yes: MMA lessons, underground fight ring, betting; owner office | `-1887.3, 1256.3, 18.2`; inside `-1893.6, 1258.0, 18.2` | `data/sites/sites.json` site 404 `sts_wat_lch_03`; `triggers.json` `#lch_03_tr_inside_dojo`, `#lch_03_tr_dojo_entrance_gate` | `lch_03_com_enemies` (`15537654311864148586`, 11 TC); `#lch_03_com_dojo` (`10367989482001701624`); spots `#lch_03_ws_dojo_owner_*` | `[game-data]` `[wiki]` |
| 10 | **Tyger Claws Casino** | Illegal casino | Westbrook / CharterHill | Yes — sewer/culvert complex | Yes: roulette, blackjack, bar, arcade; server room + netrunner office | `-65.3, -282.3, -1.5`; inside `-68.0, -294.0, -1.5` and `-37.8, -278.0, 2.5` | `data/sites/sites.json` site 417 `sts_wbr_hil_07`; `triggers.json` `#hil_07_tr_casino_inside_01/02`, `#hil_07_tr_barman_*` | `hil_07_com_enemies` (`3085020491175162508`, 15 TC); spots `#hil_07_ws_client_slacker_*`, `#hil_07_waitress_001` | `[game-data]` `[wiki]` |
| 11 | **Chram Denya Jinja** | Shinto shrine | Westbrook / NorthOaks | Partly (compound, halls, gift shop) | Minor: gift shop; TC bosses use the hoden for meetings (not a revenue line) | `31.1, 1600.3, 128.3` (site anchor); shrine-side guard spots `56.3, 1598.5, 126.7` / `53.3, 1593.6, 126.7` | `data/sites/sites.json` site 420 `sts_wbr_jpn_03`; `spots.json` `#jpn_03_ws_smoke_near_shrine_001/002`; trigger `#jpn_03_tr_shopk_scene_001` | `jpn_03_com_enemies` (`5942507499451973288`, 20 entries / 17 TC); `jpn_03_com_openworld` (`12713625468159423114`, 14) | coords `[game-data]`; name link `[inferred]`; ownership `[wiki]` |
| 12 | Little Macao Casino | Casino | TBD | TBD | Yes: casino | `TBD` | — | — | `[lore]` only (World of Cyberpunk 2077); no wiki page, no game record found |
| 13 | Tank Girls Club | Club | TBD | TBD | Yes: club | `TBD` | — | — | `[lore]` only (World of Cyberpunk 2077); no wiki page, no game record found |

### 3.1 How the name→coordinate links were proven

The site extractor keeps interior node names (`data/sites/{guards,triggers,spots,patrols,slots}.json`),
which is what makes interiors identifiable without a map:

- `site 397` (`sts_wat_kab_07`) has guard areas `casino_floor`,
  `casino_and_garage_floor`, `2nd_floor_jotaro`, and a roster entry
  `Character.sts_wat_kab_07_jotaro` → **Ho-Oh**. Its `kab_106` sibling (site 401)
  repeats the *same* guard-area coordinates (`-1029.529, 1342.969`) and is a
  quest variant, not a second casino.
- `site 404` (`sts_wat_lch_03`) has `inside_dojo`, `dojo_entrance_gate`,
  `dojo_owner_office`, `fighter_*` workspots → **Deravaja Dojo**.
- `site 417` (`sts_wbr_hil_07`) has `casino_inside_01/02`, `barman_*`,
  `client_slacker_*` workspots → **Tyger Claws Casino**.
- `site 420` (`sts_wbr_jpn_03`) has `ws_smoke_near_shrine_001/002` plus a
  `shopk_scene` trigger; the wiki's only Tyger Claws shrine (Chram Denya Jinja,
  North Oak) also has a gift shop and is the setting of *Gig: A Shrine Defiled*
  → **Chram Denya Jinja**, but this is a name inference, not a direct label.

### 3.2 Tyger-occupied generic sites with business-like suitability tags

`data/sites/suitabilities.json` tags sites with `club`, `market_stall`,
`chop_shop`, `warehouse`, `clinic`, `vehicle_bay`, etc. These are unnamed but
useful as filler control points or business slots. Top Tyger sites by roster
strength:

| Site | Sub-district | Interior | Suitability tags | Units (TC) | Coordinates | Note |
| --- | --- | --- | --- | ---: | --- | --- |
| `sts_wat_kab_07` | Kabuki | yes | chop_shop, clinic, club, lab, officer_site, raid_target, safehouse, vehicle_bay, warehouse | 22 | `-1040.2, 1349.6, 9.2` | Ho-Oh (see §3) |
| `sts_wbr_hil_07` | CharterHill | no | club, branch_office, raid_target, vehicle_bay | 15 | `-65.3, -282.3, -1.5` | TC Casino (see §3) |
| `ma_wbr_jpn_20` | JapanTown | no | club, market_stall, officer_site, vehicle_bay, camera_net | 13 | `-571.6, 499.5, 18.3` | unnamed TC club/market/stash; best generic JapanTown business candidate |
| `sts_wat_lch_03` | LittleChina | no | club, branch_office, hostage_site, raid_target | 11 | `-1887.3, 1256.3, 18.2` | Deravaja Dojo (see §3) |
| `sts_wbr_jpn_12` | JapanTown | no | club, branch_office, officer_site, raid_target | 12 | `-524.2, 668.1, 17.2` | unnamed |
| `ma_wat_lch_08` | LittleChina | no | club, market_stall, arms_cache, hostage_site, vehicle_bay | 13 | `-1604.7, 1516.2, 18.2` | unnamed market/club lot |
| `ma_wbr_jpn_15` | JapanTown | no | club, market_stall, hostage_site, raid_target | 6 | `-730.1, 879.7, 20.3` | unnamed |
| `sts_wbr_jpn_01` | JapanTown | yes | chop_shop, arms_cache, safehouse, stealth_entry, vehicle_bay, warehouse | 4 | `-528.2, 989.6, 34.5` | unnamed interior |
| `sts_wbr_jpn_02` | JapanTown | yes | market_stall, officer_site, safehouse, stealth_entry | 9 | `-260.6, 1633.6, 41.2` | unnamed interior |

Treat the tags as gameplay affordances, not lore. They tell you a place *can*
host a club/chop-shop business; they do not prove the Tyger Claws run one there.

---

## 4. Economic structure

### 4.1 Revenue streams → catalog locations

| Revenue stream | Code(s) | Catalog locations that produce it | Evidence / notes |
| --- | --- | --- | --- |
| Prostitution, dollhouses, human trafficking | `sex_work` | Clouds (1); Jig-Jig Street brothels and joytoy trade (3) | Wiki: "made most of its money from human trafficking and prostitution"; Clouds is a high-end dollhouse. `[wiki]` |
| Gambling | `gambling` | Ho-Oh (6); Pachinko Parlor (4); Tyger Claws Casino (10); Kabuki pachinko parlor (8); Little Macao Casino (12) | Ho-Oh = pachinko/mahjong/chō-han/blackjack; Pachinko Parlor = pachinko; Casino = roulette/blackjack. `[wiki]` `[game-data]` |
| Nightlife / bars / food | `food_drink` | Ho-Oh bar (6); Clouds bar (1); Jig-Jig food stalls (3); Kabuki Market stalls (7) | Wiki lists bars, restaurants, clubs. `[wiki]` |
| Braindance (legal and XBD) | `braindance` | Clouds BD venue (1); Ho-Oh top-floor XBD studio (6); Jig-Jig BD/sex shops (3) | Ho-Oh's manager Jotaro Shobo runs an illegal XBD operation on the top floor. `[wiki]` |
| Drugs (e.g. glitter) | `drugs` | Jig-Jig Street dealers (3); Kabuki Market black market (7) | Wiki: manufacture and distribution of drugs, "most notably glitter". `[wiki]` |
| Protection / security fees | `protection` | Kabuki Market stalls (7); Japantown businesses around Jig-Jig (3); North Oak shrine (11) | Kimen-Gumi legacy: security contracts and protection fees. `[wiki]` |
| Fencing / second-hand cyberware | `cyberware` | Fingers M.D. (5); Kabuki Market (7) | Fingers receives "orphaned" chrome from Jotaro's victims and serves sex workers. `[wiki]` `[inferred]` for the Jotaro link |
| Contract killing / enforcer work | `fixer_brokerage`, `protection` | Not location-bound; recruits from Deravaja Dojo (9) and Jig-Jig (3) | Wiki: Tygers hire out for hit jobs. `[wiki]` |
| Bike/vehicle work | `vehicles_chop` | Ho-Oh ground-floor garage (6) | Game layout: garage where Tygers work on hardware. `[wiki]` |
| Money laundering | `retail`, `food_drink` | All legal-front businesses: Ho-Oh, Clouds, restaurants/clubs, pachinko parlors | Wiki: many businesses registered legally as fronts. `[wiki]` |

### 4.2 Suppliers, customers, rivals

| Role | Party | Detail |
| --- | --- | --- |
| Supplier (arms/cyberware) | Arasaka | Outsources side jobs to the Claws, pays in cybertechnology and military-grade automatics. `[wiki]` |
| Supplier (legacy money/cover) | Nakagawa Foundation / NCCS | 2040s sponsor bloc; explains the legal-business portfolio and Kimen-Gumi security contracts. `[wiki]` |
| Supplier (chrome, indirect) | Scavengers / Jotaro's victims | Fingers' stock of retread implants; Scavengers operate on Jig-Jig Street. `[wiki]` |
| Customer | Arasaka upper management, corpos | Visit Tyger establishments "to blow off steam"; nightlife and dollhouse clients. `[wiki]` |
| Customer | Night Citizens, tourists, gamblers, BD consumers | Jig-Jig Street, Kabuki Market, casinos. `[wiki]` `[game-data]` |
| Fixer / broker | Wakako Okada (TC member by obligation) | Runs the Jig-Jig pachinko parlor; nine sons are high-ranking Claws. `[wiki]` |
| Rival | The Mox | Direct rivalry over sex work; formed after Lizzie Borden's murder by Claws. Lizzie's Bar is a Mox enclave in Kabuki. `[wiki]` |
| Rival | Maelstrom | Kabuki/Northside pressure; 2045 attempt to move into Old Japantown. `[wiki]` |
| Rival | Valentinos | Heywood overlap (Glen / Vista del Rey presence). `[wiki]` `[game-data]` |
| Rival | 6th Street | Charter Hill contest. `[wiki]` `[game-data]` |
| Rival | Scavengers, Animals | Both listed as Jig-Jig Street gangs on the wiki. `[wiki]` |
| Law | NCPD | Kabuki Market site 398 is an NCPD-flavoured gig (`default_faction_id=50`), a reminder that the market is contested ground. `[game-data]` |

---

## 5. Headquarters recommendation

### Primary HQ: **Clouds, Megabuilding H8 floor 12** — JapanTown

Coordinates: entrance `(-662.7, 806.9, 129.9)`; interior bar `(-647.2, 788.8, 128.3)`.
`[game-data]` `markers.jsonl` `q105_mp_dollhouse_entrance`, `q105_03_sm_dollhouse_mood`.

Rationale:

1. **Canonically Tyger-owned and inside the canon HQ district.** The wiki's 2077
   HQ is "Japantown"; Clouds is explicitly owned by the Tyger Claws and is the
   district's flagship dollhouse. `[wiki]`
2. **It is a real management seat, not just a venue.** The game gives it a
   reception, manager offices (Hiromi Sato / Maiko Maeda), a security room,
   locker room, VIP floor and bar — a believable org HQ with rooms to assign.
   `[wiki]`
3. **It maps 1:1 to the top revenue stream** (prostitution/dolls), so owning the
   HQ and owning the economy are the same action.
4. **Verified coordinates and heavy game data**: 40-entry TC-dominant
   community `q105_com_dollhouse`, 12-entry combat community, and the Hiromi
   penthouse community at z=326.
5. **Densest possible catchment**: Jig-Jig Street is 125 m away, Wakako's
   parlor 95 m, Fingers 174 m, and the nearest existing control centre
   (`cc_jpn_crescent_alley`) is 104 m.

Trade-off: Clouds is a single floor inside a residential megabuilding, so it
reads as "a business HQ" rather than "a fortified gang house". That is arguably
correct for a Yakuza-style gang whose power is commercial.

### Alternate 1: **Ho-Oh** — Kabuki

Coordinates `(-1040.2, 1349.6, 9.2)` `[game-data]` site 397.

The strongest *building* in the catalog: three floors plus a garage, a manager's
office, a casino, a bar, a BD studio and a security room, with full guard-area,
patrol, door and device records. It is also a genuine TC property with a
named manager (Jotaro Shobo). It loses to Clouds only because it is in Kabuki,
not the canon HQ district, and its manager is a mid-tier XBD scroller rather
than gang leadership.

### Alternate 2: **Chram Denya Jinja** — North Oak

Coordinates `31.1, 1600.3, 128.3` (site 420, inferred name link) `[game-data]` `[inferred]`.

Lore-strong: the 2077 artbook says Tyger big shots meet in the *hoden* of
Japantown's Shinto shrine — the sacred space "they've appropriated for their
decidedly secular purposes" `[lore]`/`[wiki]`. It is also the setting of
*Gig: A Shrine Defiled*. It loses on geography (North Oak periphery, z≈128 on
the hills), on revenue (gift shop only) and on coordinate certainty (the name
link is inferred). Good as a *second* seat / ceremonial meeting ground, not the
operational HQ.

### Overruled / downgraded suggestions

- **Jig-Jig Street as HQ** — it is a street, not a building; no enclosed seat of
  control. Excellent capture target, poor HQ.
- **"Japantown HQ" as a literal building** — no such building exists in the
  data. The wiki only names the district. Clouds is the best real substitute.
- **Wakako's Pachinko Parlor as HQ** — it is a *fixer* office, and Wakako's
  loyalty to the gang is personal/obligatory, not administrative. Keep it as a
  high-value control point, not the org seat.
- **Ho-Oh as the only HQ** — viable, but Kabuki is a business district for the
  gang, not its stated home.

---

## 6. Priority list of control points

Ranked by how well each place serves as a capturable Tyger Claws control point.
"CC" = nearest existing entry in `data/control_centers.json`; distance is
horizontal metres. Control-centre anchors were retargeted onto the landmark
table after the pilot run, so distances here are recomputed from the current
file (Ho-Oh is now co-located with its CC).

| Rank | Control point | Rel. (1–5) | District / sub-district | Coordinates | Existing CC overlap | Why |
| ---: | --- | :---: | --- | --- | --- | --- |
| 1 | **Clouds / Megabuilding H8** | 5 | Westbrook / JapanTown | `-662.7, 806.9, 129.9` | `cc_jpn_crescent_alley`, 104 m (owner TC) | Flagship dollhouse, canon HQ district, densest revenue cluster, interior with management rooms |
| 2 | **Jig-Jig Street** | 5 | Westbrook / JapanTown | `-628.7, 814.9, 18.4` | `cc_jpn_crescent_alley`, 126 m (TC) | The red-light economy itself; brothels, dealers, sex shops; rival pressure from Mox/Scavs/Animals |
| 3 | **Ho-Oh** | 5 | Watson / Kabuki | `-1040.2, 1349.6, 9.2` | `cc_kab_allen_street`, **0 m** (TC) | Owned casino/club/XBD studio; 3 floors, guards, patrols, devices; cleanest first test |
| 4 | **Pachinko Parlor (Wakako's Den)** | 4 | Westbrook / JapanTown | `-657.3, 826.7, 19.5` | `cc_jpn_crescent_alley`, 95 m (TC) | Gambling revenue + fixer brokerage; links the gang to the contract economy |
| 5 | **Kabuki Market** | 4 | Watson / Kabuki | `-1231.5, 1965.0, 8.0` | `cc_kab_creek_loop`, 56 m (**owner The Mox**) | Black-market retail + protection racket; existing CC ownership conflicts with lore and should be corrected |
| 6 | **Deravaja Dojo** | 4 | Watson / LittleChina | `-1887.3, 1256.3, 18.2` | `cc_lch_farrier_alley`, 246 m (TC) | Recruitment, fight betting, melee-culture identity; interior with basement ring |
| 7 | **Tyger Claws Casino** | 4 | Westbrook / CharterHill | `-65.3, -282.3, -1.5` | `cc_hil_le_le_park`, **7 m** (TC) | Hidden gambling den; nearly coincides with an existing CC, so it is a cheap rename/upgrade rather than a new point |
| 8 | **Chram Denya Jinja** | 3 | Westbrook / NorthOaks | `31.1, 1600.3, 128.3` (`[inferred]`) | `cc_nok_north_canyon`, **6 m** (TC) | Ceremonial meeting ground + prestige; peripheral and low-revenue; good second seat |
| 9 | Kabuki pachinko parlor (unnamed) | 2 | Watson / Kabuki | `-1180.7, 1764.0, 23.4` | `cc_kab_creek_loop`, 184 m (Mox) | Another gambling room; useful filler, no lore name |
| 10 | Fingers M.D. | 2 | Westbrook / JapanTown | `-580.3, 801.5, 20.9` | `cc_jpn_crescent_alley`, 174 m (TC) | Not TC-owned, but a fixture of TC turf and a chrome-fencing node; better as an adjacency/modifier than an owned point |

### Test control point for the first in-game test: **Ho-Oh**

Why Ho-Oh and not the HQ or a street:

- **Fully enclosed, verifiable interior** (`site 397`, `is_interior=1`) with a
  known anchor and three interior floors, so a capture trigger radius can be
  validated against real geometry.
- **Rich gameplay records already extracted**: guard areas
  (`#kab_07_guard_area_casino_floor`), patrol routes
  (`#kab_07_spl_casino_patrol_route_001`), doors, and 22 TC roster units — every
  hook a capture/defence prototype needs is present and named.
- **Clean ownership**: `default_faction_id = 2`, `initial_owner_faction_id = 2`;
  no ambiguity about who is being evicted.
- **Already an active CC anchor**: `cc_kab_allen_street` (`is_active=1`) was
  retargeted onto Ho-Oh, so the test needs no new map plumbing. It no longer
  proves that a lore point is *distinct* from the generic grid — Deravaja Dojo
  is the fallback if that distinctness needs to be demonstrated.
- **Fallback if Ho-Oh is quest-gated**: Deravaja Dojo (`sts_wat_lch_03`) is a
  smaller interior with the same properties and 11 TC units.

---

## 7. Per-sub-district count of lore-relevant locations

This is the number to feed yield balancing. It counts **distinct named places**
the gang owns, runs, protects or habitually occupies — not quest-scene variants
and not generic occupied blocks. `Filler` is the deduped occupied-site count
minus any site already counted as a named place (the two tiers from
`METHOD.md` §8).

| Sub-district | Named lore-relevant places | Which ones | TC-occupied sites (deduped, `[game-data]`) | Filler | Noteworthy interiors |
| --- | ---: | --- | ---: | ---: | ---: |
| JapanTown | **4** (+1 landmark) | Clouds, Jig-Jig Street, Pachinko Parlor, Fingers M.D. (+ Megabuilding H8 as the Clouds host landmark) | 14 | 13 | 3 (Clouds floor 12, Pachinko Parlor, Fingers clinic) |
| Kabuki | **3** | Ho-Oh, Kabuki Market, Kabuki pachinko parlor | 7 | 5 | 2 (Ho-Oh, pachinko parlor) |
| LittleChina | **1** | Deravaja Dojo | 7 | 6 | 1 (Deravaja) |
| CharterHill | **1** | Tyger Claws Casino | 1 | 0 | 1 (Casino) |
| NorthOaks | **1** | Chram Denya Jinja | 3 | 3 | 0 confirmed |
| Northside | **0** | turfs/raids only | 4 | 4 | 0 |
| Glen | **0** | TC ambush scene only (`mws_hey_07`) | 1 | 1 | 0 |
| VistaDelRey | **0** | anomaly only — see §2 note | 2 | 2 | 0 |
| Downtown | **0** | generic TC scanner-hustle sites | 3 | 3 | 0 |
| CorpoPlaza | **0** | incidental mixed combat area | 0 | 0 | 0 |
| Wellsprings / Arroyo / Coastview | **0** | incidental mixed spawns | 0 | 0 | 0 |
| Badlands | **0** | incidental mixed spawn at `ma_bls_ina_04` | 1 | 1 | 0 |
| **Total** | **10** | | 43 | 38 | 6 |

Two accounting details for the JSON block:

- JapanTown's 14 sites include the shrine site (`sts_wbr_jpn_03`), whose geocode
  is `jpn`; the named place *Chram Denya Jinja* is catalogued under NorthOaks by
  lore. The site is therefore excluded from JapanTown's filler (`14 − 1 = 13`)
  so it is not double-counted as both a named NorthOak place and JapanTown filler.
- Four of the ten named places are marker-only and have no roster site:
  Clouds, Jig-Jig Street, Pachinko Parlor, Fingers M.D. Kabuki Market's site
  (398) is NCPD-owned, so it is named but not filler. That is why `named + filler
  = 48` while there are 43 occupied sites.

Interpretation for yield: JapanTown and Kabuki are the only sub-districts with
more than one named place; LittleChina, CharterHill and NorthOaks have exactly
one each and therefore should carry the highest per-point yield. Northside is
the outlier: heavy Tyger *presence* (10 areas, 4 sites) but no named business,
so it reads as raided/contested turf rather than owned economy.

If 10 named points is too few for the map, the §3.2 generic site table is the
honest filler pool — but those points should be tagged as "occupied block"
rather than "lore business" so yield math does not pretend they are iconic.

---

## 8. Gaps and uncertainties

1. **Chram Denya Jinja name link is inferred.** Site `sts_wbr_jpn_03` is
   Tyger-guarded, has a `near_shrine` workspot pair and a `shopk_scene` trigger,
   and sits at the North Oak hillside; the wiki places the shrine in North Oak
   and the gig *A Shrine Defiled* there. But no record in the extract says
   "Chram Denya Jinja", and the site's own geocode is `jpn` (Japantown), not
   `nok`. Confirm in-game before seeding the name.
2. **No coordinate for Little Macao Casino or Tank Girls Club.** They appear
   only in the 2077 sourcebook summary, have no wiki page and no game record.
   They may be lore-only. Keep them as `TBD`/`[lore]` and do not seed.
3. **Tyger Claws Casino vs. `cc_hil_le_le_park`.** They are 7 m apart; the
   existing CC is almost certainly the same physical site. Decide whether to
   rename the CC or keep both.
4. **Kabuki Market's existing CC is Mox-owned.** `cc_kab_creek_loop`
   (`sub_territory_id 9`) has `initial_owner_faction_id = 11` (The Mox). The
   wiki describes Kabuki Market as Tyger Claws territory with Mox rivalry; the
   seed and lore conflict. One of them is wrong.
5. **The `rey_09` Vista del Rey anomaly.** `rey_09_com_enemies`,
   `sts_hey_rey_09` and neighbours carry Heywood codes but sit at
   `(-537, 1292)` in JapanTown. It is a reused prefab. Do not treat it as a
   Heywood holding; find the real Vista del Rey TC presence before seeding
   Heywood.
6. **Glen's Tyger content is a crime scene, not a business.** `mws_hey_07`
   (24 TC units, Trauma Team AV, dead bodies, approach triggers) is the Tyger
   ambush mini-world-story. It proves presence, not ownership of a place.
7. **No vendor/shop record proves "what a business sells".** The extract has
   suitability tags (`club`, `market_stall`, `chop_shop`, …) but not vendor
   inventories. Business descriptions in §3/§4 come from the wiki and from
   named game rooms (casino floor, bar, doll booths), not from vendor data.
8. **The per-sub-district vanilla gang panel was not dumped.** Evidence (b) is
   the district-level `data/districts.json` plus the earlier wiki-derived
   sub-district table, not `District_Record.Gangs()`. A TweakDB dump would settle
   Kabuki/Charter Hill exactly.
9. **Some TC areas are mis-districted in `areas.jsonl`.** Quest communities
   from `always_loaded_*` inherit the file's path token; e.g. Clouds and Jig-Jig
   are labelled `watson`. All counts in §2/§7 were re-attributed by position or
   geocode; the raw file is not safe to aggregate by `district_code`.
10. **Interior coverage is partial.** `is_interior` is set for 17 of 424 sites;
    absence of the flag does not prove a site is exterior-only. Conversely,
    `sts_wat_kab_07` and `sts_wat_kab_106` are the same interior.

---

## Appendix — method

Reproducible extraction snippets, the wiki API rules, the sub-district
attribution function, and the JSON-block validator are **not** repeated here.
They live in [`METHOD.md`](./METHOD.md) and are parameterised by faction code, so
they apply unchanged to the next 14 factions. This doc keeps only the Tyger
Claws evidence and conclusions.

---

## 9. Sources

- Local: `dist/extract/areas.jsonl`, `dist/extract/markers.jsonl`,
  `data/sites/{sites,communities,rosters,guards,triggers,spots,patrols,slots,doors,suitabilities,meta}.json`,
  `data/{districts,factions,control_centers,sub_territories,landmarks,spawn_points}.json`.
- Wiki: [Tyger Claws](https://cyberpunk.fandom.com/wiki/Tyger_Claws),
  [Clouds](https://cyberpunk.fandom.com/wiki/Clouds),
  [Jig-Jig Street](https://cyberpunk.fandom.com/wiki/Jig-Jig_Street),
  [Pachinko Parlor](https://cyberpunk.fandom.com/wiki/Pachinko_Parlor),
  [Wakako Okada](https://cyberpunk.fandom.com/wiki/Wakako_Okada),
  [Finn Gerstatt / Fingers](https://cyberpunk.fandom.com/wiki/Finn_Gerstatt),
  [Ho-Oh](https://cyberpunk.fandom.com/wiki/Ho-Oh),
  [Kabuki Market](https://cyberpunk.fandom.com/wiki/Kabuki_Market),
  [Deravaja Dojo](https://cyberpunk.fandom.com/wiki/Deravaja_Dojo),
  [Tyger Claws Casino](https://cyberpunk.fandom.com/wiki/Tyger_Claws_Casino),
  [Chram Denya Jinja](https://cyberpunk.fandom.com/wiki/Chram_Denya_Jinja).
- Earlier repo research: `docs/research/factions-gangs-territories.md`,
  `docs/research/game-data-extraction.md`,
  `docs/research/factions-corps-fixers-independents.md`.

---

## 10. Machine-readable block

Strict JSON for seeding (contract in [`METHOD.md`](./METHOD.md) §10). Every
coordinate was re-verified against the local record named in `source` on
2026-11-25; none came from the wiki.

```json
{
  "faction_code": "tyger_claws",
  "hq": {"name": "Clouds", "district": "Westbrook", "sub_district": "JapanTown", "x": -662.718, "y": 806.865, "z": 129.893, "source": "dist/extract/markers.jsonl q105_mp_dollhouse_entrance", "confidence": "game-data+wiki"},
  "alternate_hqs": [
    {"name": "Ho-Oh", "district": "Watson", "sub_district": "Kabuki", "x": -1040.161, "y": 1349.624, "z": 9.221, "source": "data/sites/sites.json site 397 sts_wat_kab_07", "confidence": "game-data+wiki"},
    {"name": "Chram Denya Jinja", "district": "Westbrook", "sub_district": "NorthOaks", "x": 31.118, "y": 1600.287, "z": 128.317, "source": "data/sites/sites.json site 420 sts_wbr_jpn_03 (name link inferred)", "confidence": "game-data+inferred+wiki"}
  ],
  "test_control_point": {"name": "Ho-Oh", "district": "Watson", "sub_district": "Kabuki", "x": -1040.161, "y": 1349.624, "z": 9.221, "source": "data/sites/sites.json site 397 sts_wat_kab_07", "confidence": "game-data+wiki"},
  "control_points": [
    {"rank": 1, "name": "Clouds", "type": "dollhouse", "relevance": 5, "district": "Westbrook", "sub_district": "JapanTown", "x": -662.718, "y": 806.865, "z": 129.893, "source": "dist/extract/markers.jsonl q105_mp_dollhouse_entrance", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["sex_work", "braindance", "food_drink"], "nearest_cc_code": "cc_jpn_crescent_alley", "nearest_cc_m": 103.7},
    {"rank": 2, "name": "Jig-Jig Street", "type": "red_light_street", "relevance": 5, "district": "Westbrook", "sub_district": "JapanTown", "x": -628.711, "y": 814.856, "z": 18.435, "source": "dist/extract/markers.jsonl q105_04_sm_jigjig_street", "confidence": "game-data+wiki", "interior": false, "revenue_streams": ["sex_work", "drugs", "retail", "food_drink"], "nearest_cc_code": "cc_jpn_crescent_alley", "nearest_cc_m": 125.5},
    {"rank": 3, "name": "Ho-Oh", "type": "casino_club", "relevance": 5, "district": "Watson", "sub_district": "Kabuki", "x": -1040.161, "y": 1349.624, "z": 9.221, "source": "data/sites/sites.json site 397 sts_wat_kab_07", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["gambling", "braindance", "food_drink", "protection"], "nearest_cc_code": "cc_kab_allen_street", "nearest_cc_m": 0.0},
    {"rank": 4, "name": "Pachinko Parlor (Wakako's Den)", "type": "gambling_hall", "relevance": 4, "district": "Westbrook", "sub_district": "JapanTown", "x": -657.332, "y": 826.691, "z": 19.522, "source": "dist/extract/markers.jsonl q112_mp_wakakos_pachinko_parlor", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["gambling", "fixer_brokerage"], "nearest_cc_code": "cc_jpn_crescent_alley", "nearest_cc_m": 95.0},
    {"rank": 5, "name": "Kabuki Market", "type": "market", "relevance": 4, "district": "Watson", "sub_district": "Kabuki", "x": -1231.458, "y": 1965.025, "z": 7.949, "source": "data/sites/triggers.json #kab_08_tr_marketplace (site 398)", "confidence": "game-data+wiki", "interior": false, "revenue_streams": ["retail", "protection", "drugs", "food_drink"], "nearest_cc_code": "cc_kab_creek_loop", "nearest_cc_m": 55.8},
    {"rank": 6, "name": "Deravaja Dojo", "type": "dojo", "relevance": 4, "district": "Watson", "sub_district": "LittleChina", "x": -1887.309, "y": 1256.31, "z": 18.227, "source": "data/sites/sites.json site 404 sts_wat_lch_03", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["gambling", "protection"], "nearest_cc_code": "cc_lch_farrier_alley", "nearest_cc_m": 246.1},
    {"rank": 7, "name": "Tyger Claws Casino", "type": "casino", "relevance": 4, "district": "Westbrook", "sub_district": "CharterHill", "x": -65.344, "y": -282.317, "z": -1.472, "source": "data/sites/sites.json site 417 sts_wbr_hil_07", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["gambling", "food_drink"], "nearest_cc_code": "cc_hil_le_le_park", "nearest_cc_m": 7.3},
    {"rank": 8, "name": "Chram Denya Jinja", "type": "shrine", "relevance": 3, "district": "Westbrook", "sub_district": "NorthOaks", "x": 31.118, "y": 1600.287, "z": 128.317, "source": "data/sites/sites.json site 420 sts_wbr_jpn_03 (name link inferred)", "confidence": "game-data+inferred+wiki", "interior": true, "revenue_streams": ["retail"], "nearest_cc_code": "cc_nok_north_canyon", "nearest_cc_m": 5.9},
    {"rank": 9, "name": "Kabuki pachinko parlor (unnamed)", "type": "gambling_hall", "relevance": 2, "district": "Watson", "sub_district": "Kabuki", "x": -1180.748, "y": 1763.951, "z": 23.39, "source": "data/sites/sites.json site 402 sts_wat_kab_107", "confidence": "game-data", "interior": true, "revenue_streams": ["gambling"], "nearest_cc_code": "cc_kab_creek_loop", "nearest_cc_m": 183.6},
    {"rank": 10, "name": "Fingers M.D.", "type": "clinic", "relevance": 2, "district": "Westbrook", "sub_district": "JapanTown", "x": -580.271, "y": 801.537, "z": 20.858, "source": "dist/extract/markers.jsonl q105_05_sm_fingers_enter", "confidence": "game-data+wiki", "interior": true, "revenue_streams": ["cyberware"], "nearest_cc_code": "cc_jpn_crescent_alley", "nearest_cc_m": 174.3}
  ],
  "subdistrict_counts": {
    "JapanTown": {"named": 4, "filler": 13},
    "Kabuki": {"named": 3, "filler": 5},
    "LittleChina": {"named": 1, "filler": 6},
    "CharterHill": {"named": 1, "filler": 0},
    "NorthOaks": {"named": 1, "filler": 3},
    "Northside": {"named": 0, "filler": 4},
    "Glen": {"named": 0, "filler": 1},
    "VistaDelRey": {"named": 0, "filler": 2},
    "Downtown": {"named": 0, "filler": 3},
    "CorpoPlaza": {"named": 0, "filler": 0},
    "Wellsprings": {"named": 0, "filler": 0},
    "Arroyo": {"named": 0, "filler": 0},
    "Coastview": {"named": 0, "filler": 0},
    "Badlands": {"named": 0, "filler": 1}
  }
}
```
