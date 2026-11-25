# Scavengers — Lore-Relevant Control Points

Status: faction research run, 2026-11-25. One faction, one document.
Scope: turn the generic ~5-control-centres-per-sub-district grid into the dens,
chop/ripper sites, squats and stash houses the Scavengers actually run, with
verified coordinates, an economic map, an honest HQ answer, a ranked capture
list and per-sub-district counts. Method: this doc conforms to
[`METHOD.md`](./METHOD.md), applying **§1.2 (batch 2) first** and then §1.1;
where they conflict, §1.2 wins. `AGENTS.md` was read first. No commits, no game
launch; helper scripts ran outside the repo under `python3 -I`.

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Position, site, community, roster, area, spawn or marker record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page via the MediaWiki API (cited inline) | Secondary, high |
| `[lore]` | Book/artbook/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My reasoning links a named place to a game record; reasoning stated | Weak, flagged |

No coordinate below is guessed. Every `(x, y, z)` is copied from a local site,
marker or area record, or marked `TBD`. No coordinate in this document came
from the wiki.

---

## 1. Summary

The **Scavengers** (`data/factions.json` fid **7**, `affiliation_enum =
Scavengers`, `category = gang`) are not one organisation but a label for
**dozens of independent cells** that harvest chrome and organs from kidnapped
people and sell the parts on the black market. The 2077 World Book calls them
the NCPD's body-count leader; the wiki's own summary is that they "tend to
operate in small groups, with no official hierarchy to unite them, nor do they
have a designated piece of turf". Threat level *Medium*. `[wiki]`

This shapes everything below:

- **There is no headquarters.** The organization infobox leaves `headquarters`
  and `faction_locations` blank, and `data/faction_headquarters.json` has **no
  Scavengers row**. `[wiki]` `[game-data]` §5 therefore derives a *placeholder*
  seat and says so.
- **Their footprint is a set of premises, not a map.** Every scav site in the
  extract is a building or a fenced yard where victims are processed: an
  abandoned hotel, an old power plant, a dead motel, a museum, an expo hall, a
  parking garage, a housing block, a ripper clinic, an unfinished amusement
  ride. The extract agrees with the lore: 24 scav-occupied sites and 210 roster
  units spread over 14 sub-districts, with **nothing** that reads as a district
  capital. `[game-data]`

**Economic model.** Four streams, in order of weight:

1. **`cyberware`** — the core business. "Scavengers are the main suppliers for
   low-end cyberware for other gangs, small-time criminals, and shady
   ripperdocs", and victims are stripped of implants and organs. `[wiki]` Every
   named place below has a harvesting or ripper work surface except the two
   smuggling venues.
2. **`mercenary`** — "frequently hired to perform unpleasant or inconvenient
   tasks … heists, hit jobs, and abductions … no questions asked". Kidnapping is
   the input to stream 1, so this is both a service and the sourcing method.
   `[wiki]`
3. **`braindance`** — illegal XBD production in at least two venues: the old
   power plant is explicitly a scav XBD base and the prologue den is the set of
   the *Sweet Dreams* snuff BD. `[wiki]` `[game-data]`
4. **`arms` / `smuggling`** — the Terra Cognita venues: the ESC Explorer is
   "a base for their weapons smuggling operations", and the Eden Beach
   ringleader is a scav "captain … with multiple smuggling priors". `[wiki]`

There is **no** `drugs`, `gambling`, `protection`, `finance`, `manufacturing`,
`rnd` or `real_estate` line anywhere in the scav material. Giving them any of
those would mis-model the faction.

**Where the weight sits.** Northern Pacifica dominates: Dogtown (34 areas /
240 entries), Coastview (10 / 46), West Wind Estate (11 / 44), plus the
Charter Hill power plant (5 / 39). Watson is second (Kabuki 9 / 33, Northside
5 / 30, Little China 2 / 14), and Japan Town holds the canon den. That is
exactly the lore's "more concentrated presence in northern Pacifica and
southern Wellsprings" — except that the extract puts the southern-Heywood
presence at only 3 areas / 10 entries (§8.7). `[wiki]` `[game-data]`

**Canon base.** The only place the wiki gives a proper address for is the
**Scavenger Den**, "apartments 1235 and 1237 of an apartment building on
Crescent Street in Japantown" — the prologue den of *The Rescue*, reused for
*Sweet Dreams*. `[wiki]` It is a two-apartment floor, not a seat.

---

## 2. Territory

### 2.1 Districts

| Evidence kind | Result |
| --- | --- |
| (a) Wiki/lore | "Scavengers can be found all over Night City"; no designated turf; "more concentrated presence in **northern Pacifica** and **southern Wellsprings**". Dogtown's scavs are separately described as "much better organized and equipped … the scav oligarchy secures business in Hansen's backyard". `[wiki]` |
| (b) Vanilla map gang panel | `data/districts.json` `vanilla_gangs` lists **Scavengers in no district** — Pacifica is `["VoodooBoys","Animals"]`, Heywood `["Valentinos"]`, Watson `["Maelstrom","TygerClaws"]`. Consistent with "no turf". `[game-data]` |
| (c) Game-data counts | 104 community areas contain Scavengers (92 dominant), **560 entries**; **24 candidate sites / 210 roster units**; 5 seeded sub-territories (all fid 7); **89 spawn points**. `[game-data]` |

**Units.** 210 roster entries at 24 sites: **206 human, 4 machine** (three
droids at the two machine-only sites 110 and 301, one `android2` inside the
Ross Street Parking garrison). 132 distinct character records. Almost all are
`Character.<sub>_scavenger_*` or `Character.sts_ep1_0*_scavenger_*`, but three
sites use generic records (`ma_wat_kab_06_merc_*`, `sts_wat_kab_05_enemy_ganger_*`,
`ma_cct_dtn_03_scav_driver`) — §1.2 item 5 applies, the faction id is the join.
`[game-data]`

The five seeded sub-territories and what actually justifies each (§1.2 item 13
check):

| # | Sub-territory | Display name | Real scav record inside | Verdict |
| ---: | --- | --- | --- | --- |
| 14 | `nid_oil_refinery` | Northside Oil Wharf | `ma_wat_nid_27` **illegal ripperdoc clinic**, 5.8 m away, 7 units | **Name wrong, place right.** The seed labels a scav ripper clinic as an oil wharf. Keep the CC, rename it. |
| 62 | `cvi_pacifica_pier` | Pacifica Pier Boardwalk | `ma_pac_cvi_12` **Eden Beach Mega Ride**, 48 m away, 16 units | **Solid, mislabelled.** 48 m off the site centroid; rename to Eden Beach. |
| 66 | `wwd_apartments_north` | West Wind North Towers | `ma_pac_wwd_04` SOCA den, **9.5 m** away, 4 units | **Solid.** |
| 67 | `wwd_central_courtyard` | West Wind Central Plaza | **Nothing.** Nearest scav record is `{cs_handcuffed_gangoons_com}_025` (2 handcuffed prisoners) 30 m away; the area is a `q305` 6th Street ambush scene | **Wrong.** No scav site, no den, no garrison within 180 m. Drop it or move it (§8.6). |
| 68 | `wwd_south_projects` | West Wind South Projects | `ma_pac_wwd_02` scav den, **24.8 m** away, 8 units | **Solid but contested** — the den the Wraiths raid (`wraiths.md` site 112). |

All five CCs are inactive and sit exactly on their sub-territory centroids, so
every distance above is "distance from the seed grid point to the real place".
`[game-data]`

### 2.2 Sub-district presence

Area counts are `dist/extract/areas.jsonl` rows whose `faction_counts` contains
`scavengers`; "dominant" is `dominant_faction == scavengers`. "Sites" is the
deduped occupied-site set from §2.3. Spawn points are grouped by
`spawn_points.sub_territory_id` (§1.1 item 15). `named`/`filler` are §7's
numbers.

| Sub-district | District | (a) Lore | (b) Panel | (c) Areas (dominant) | (c) Entries | Spawn pts | Occupied sites | Named | Filler |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Dogtown | Pacifica | PL scav "oligarchy", better equipped | Barghest | **34 (31)** | **240** | 19 | 3 | 4 | 1 |
| Coastview | Pacifica | northern Pacifica core | Voodoo Boys, Animals | 10 (10) | 46 | 9 | 3 | 2 | 1 |
| WestWindEstate | Pacifica | northern Pacifica core | Voodoo Boys, Animals | 11 (11) | 44 | **23** | 3 | 2 | 1 |
| JapanTown | Westbrook | **canon Scavenger Den** | Tyger Claws (+Mox) | 7 (6) | 42 | 6 | 2 | 1 | 2 |
| CharterHill | Westbrook | *Disasterpiece* XBD plant | — | 5 (5) | 39 | 5 | 0 | 1 | 0 |
| Kabuki | Watson | 3 dens + trafficking | Maelstrom, Tyger Claws | 9 (7) | 33 | 7 | 4 | 2 | 2 |
| Northside | Watson | 2 dens, one on the seeded CC | Maelstrom | 5 (4) | 30 | 4 | 2 | 2 | 0 |
| Arroyo | SantoDomingo | cyberware buyers (*Gun Music*) | 6th Street | 8 (7) | 27 | 6 | 0 | 0 | 0 |
| RanchoCoronado | SantoDomingo | incidental | 6th Street | 4 (3) | 17 | 4 | 0 | 0 | 0 |
| LittleChina | Watson | rooftop outpost | Tyger Claws | 2 (2) | 14 | 2 | 2 | 1 | 1 |
| Badlands | Badlands | one harvesting warehouse | Aldecaldos, Wraiths | 4 (2) | 13 | 0 | 1 | 1 | 0 |
| Wellsprings | Heywood | lore: "southern Wellsprings" | Valentinos | 3 (2) | 10 | 1 | 1 | 0 | 1 |
| CorpoPlaza | CityCenter | one ambient event | — | 1 (1) | 3 | 1 | 0 | 0 | 0 |
| Downtown | CityCenter | one cyberpsycho scene | — | 1 (1) | 2 | 1 | 1 | 0 | 1 |
| Glen | Heywood | one fight crowd | — | 0 | 0 | 1 | 0 | 0 | 0 |
| **Total** | | | | **104 (92)** | **560** | **89** | **22** | **16** | **10** |

**Reading the counts.** They are a footprint, not a territory. Two facts matter
for yield:

1. **274 of the 560 entries sit in the 16 named places** (49%). The rest are
   quest corridors, persons of interest and ambient events: PL side activities
   (`sa_ep1_*`), criminal events (`ce_easy_*`, `ce_medium_com`, `cz_ce_sc_*`,
   `hp_ce_sc_*`), handcuffed-prisoner and police-execution scenes (`cs_*`), and
   quest crowds (`mq303`, `mq304`, `q305`, `mq044`). They are presence, never
   ownership (§1.2 item 9). `[game-data]`
2. **Dogtown + Coastview + West Wind Estate = 330 of 560 entries (59%) and 8 of
   the 16 named places.** Northern Pacifica is the faction. Arroyo's 27 entries
   are almost entirely the `Gun Music` meeting and ambient `ce_easy_*` events —
   zero holdings. `[game-data]`

### 2.3 Attribution caveat

Six failure modes were hit; four are new relative to §1.2 item 1.

1. **The Dogtown bbox swallows Coastview and West Wind Estate.** `districts.json`
   gives Dogtown `x −2640…−1165, y −3245…−1770`, which contains
   `ma_pac_cvi_12`/Eden Beach (`−2433, −2199`) and the Los Osos motel
   (`−2555, −2435`). Both are **Coastview** and **West Wind Estate** in the seed
   (`source_path`) and on the wiki. A bbox test is therefore worthless for
   southern Pacifica; use `source_path`, city tokens, or the wiki. `[game-data]`
   `[wiki]`
2. **`district_code` is only half-reliable for PL rows.** `dogtown` is
   trustworthy (34 rows used it). `pacifica` covers real Dogtown street stories
   (`sts_ep1_03`, `sts_ep1_04`) whose coordinates are inside Dogtown. I
   attributed those by `sts_ep1_*` prefix plus the verified site anchor, not by
   the field. `[game-data]`
3. **`sites.json.sub_territory_id` mis-buckets the two PL gigs.** `sts_ep1_04`
   (The Scraper, Longshore Stacks/Dogtown) carries sub-territory 70 =
   *West Wind South Highway*; `sts_ep1_08` (Organitopia, Terra Cognita/Dogtown)
   also carries 70. `sts_ep1_01` (Haven Clinic, Dogtown) carries 94 =
   *dt_terra_cognita*, which is at least in the right district. `[game-data]`
4. **Site anchors miss whole buildings for PL gigs.** `sts_ep1_03`'s anchor is
   **83 m** from its own scav community cluster (`{sts_ep1_03_combat_com}`,
   `−2554.542, −2435.019`). §1.1 item 7 (prefer community/guard coords for
   interiors) applies; Los Osos is anchored on the community in §3. `sts_ep1_04`
   is better behaved (anchor is 13 m from its nearest community). `[game-data]`
5. **Marker floors share x/y.** At the Scavenger Den, `q000_vr_mp_scav_elevator`
   sits at `z = 24.4` (street lift) while the den markers sit at `z = 132`;
   picking by distance alone in 2D gives you the lobby 108 m below the den.
   §3.6 warns about `spwn_player` teleports but not about this. `[game-data]`
6. **The wiki infobox can lose to the wiki's own walkthrough.** The
   *Electric Corporation Power Plant* infobox says `sub_district = Arroyo`; its
   *Disasterpiece* objectives say "Ride with Judy to the old power plant in
   **Charter Hill**", and the studio markers are at `(32, −511)`, 245 m from
   the Lele Park sub-territory and 850 m from Arroyo. The walkthrough and the
   markers win; the plant is catalogued as **Charter Hill** (§8.3). `[wiki]`
   `[game-data]`

---

## 3. Location catalog

World-space metres, `Z` up. "Interior?" means the game has a distinct interior
cell or volume — proven from node names or the wiki's building layout, not the
sparse `is_interior` flag (§1.2 item 15; **all 21 site rows below read
`is_interior = 0`**). "Business?" is what the place earns; the extract has no
vendor inventory.

| # | Name | Type | District / sub-district | Interior? | Business? (what it earns) | Coordinates (x, y, z) | Coordinate source record | Linked communities / sites | Confidence |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **The Scraper** (formerly Breeze Hotel) | Unfinished hotel → scav hideout | Pacifica / Dogtown (Longshore Stacks) | **Yes** — lift + lift doors, prison gate, upper loot room, armory door (keycode 2045) | `cyberware`, `arms`, `mercenary` | `−2465.287, −2713.544, 21.820` | `data/sites/sites.json` site 357 `sts_ep1_04` | `sts_ep1_04_combat_com` (16), `…_lower_after_com` (14), `…_upper_com` (13); 43 roster units; **9 doors** | `[game-data]` `[wiki]` |
| 2 | **Electric Corporation Power Plant** | Abandoned power plant → XBD studio | Westbrook / CharterHill | **Yes** — warehouse ground floor plus sub-levels −1, −2, −3 (studio markers at `z ≈ −16.6`) | `braindance`, `cyberware` | `31.935, −510.770, 1.304` | `dist/extract/areas.jsonl` `{q105_com_braindance_combat_floor_}0` | 32 entries across 3 combat-floor communities + `{q105_com_braindance_investigation}` (2); no `sites.json` row | `[game-data]` `[wiki]` |
| 3 | **Digimmortal** | Exhibition hall → scav-garrisoned venue | Pacifica / Dogtown (Terra Cognita) | **Yes** per wiki — three exhibition levels | `cyberware`, `mercenary` | `−2347.550, −3063.500, 129.540` | `dist/extract/areas.jsonl` `{mq306_com_scavengers}` | `mq306_com_scavengers` (24) + `…_exit` (13); `mq306_com_damir` 30 m; no site | `[game-data]` `[wiki]` |
| 4 | **Organitopia** | Abandoned natural-history museum → scav den | Pacifica / Dogtown (Terra Cognita) | **Yes** per wiki — two exhibition halls, stairwell, shuttered window | `cyberware`, `mercenary` | `−2227.138, −3019.134, 115.270` | `data/sites/sites.json` site 360 `sts_ep1_08` | `sts_ep1_08_front_building_com` (4) 13 m, `…_enemies_com` (12) 60 m; 16 roster units; 9 doors | `[game-data]` `[wiki]` |
| 5 | **Eden Beach Mega Ride** | Abandoned amusement ride → scav den | Pacifica / Coastview | No — open-air ride deck (guard volumes on the wheel) | `cyberware`, `smuggling` | `−2433.580, −2199.374, 15.980` | `data/sites/sites.json` site 107 `ma_pac_cvi_12` (has a real `bbox`) | `ma_pac_cvi_12_com` (16); 16 roster units; 5 guard volumes, 31 spots, 9 patrols | `[game-data]` `[wiki]` |
| 6 | **Scavenger Den** (Crescent St.) | Apartment den — apartments 1235/1237 | Westbrook / JapanTown | **Yes** — two apartment interiors on a high floor, lift terminal | `cyberware`, `sex_work`, `braindance` | `−455.188, 400.266, 136.266` | `dist/extract/markers.jsonl` `mq036_sm_scavengers` | `{mq036_com_scavengers}` (16), `{q001_scavengers_community_area}` (10), `…_boss` (1); no site | `[game-data]` `[wiki]` |
| 7 | **Los Osos motel** (West Wind Estate) | Defunct motel → cyberware-acquisition hideout | Pacifica / WestWindEstate | **Yes** — motel rooms/doors (`#sts_ep1_03_miniboss_doors`, `#sts_ep1_03_dvc_exit_gate`); anchor is 83 m off, so anchored on the community | `cyberware`, `mercenary` | `−2554.542, −2435.019, 16.950` | `dist/extract/areas.jsonl` `{sts_ep1_03_combat_com}` (site anchor `−2486.188, −2493.572` is 83 m away) | `…_combat_first_floor_com` (5), `…_friendly_com` (5), `…_boss_com` (1); 18 roster units; 7 doors | `[game-data]` `[wiki]` |
| 8 | **ESC Explorer** | Abandoned space-expo hall → weapons-smuggling base | Pacifica / Dogtown (Terra Cognita) | **Yes** per wiki — three floors, escalators, roof catwalk, three entrances | `arms`, `smuggling` | `−2272.990, −2947.700, 111.470` | `dist/extract/areas.jsonl` `{we_ep1_17_com}` | `we_ep1_17_com` (17) + `…_2nd_loop` (12); no site | `[game-data]` `[wiki]` |
| 9 | **Ross Street Parking Facility** | Parking garage → scav chop/cache site | Watson / Northside | **Yes** — multi-level parking structure (wiki interior shots) | `cyberware` | `−1734.613, 2431.407, 7.260` | `data/sites/sites.json` site 215 `ma_wat_nid_01` | `ma_wat_nid_01_scavs_com` (12); 12 roster units (11 human + 1 android); 6 guard volumes, 33 spots, 7 patrols, 3 devices | `[game-data]` `[wiki]` |
| 10 | **Illegal ripperdoc clinic** (Offshore St.) | Unlicensed clinic | Watson / Northside | **Yes** — clinic room + stash (`#ma_wat_nid_27_tr_stash`); no door node | `cyberware` | `−1111.159, 3318.479, 8.531` | `data/sites/sites.json` site 237 `ma_wat_nid_27` | `ma_wat_nid_27_com` (7); 7 roster units; 2 devices | `[game-data]` `[wiki]` |
| 11 | **Opposites Attract rooftop outpost** | Rooftop outpost above the MedCenter block | Watson / LittleChina | No — rooftop garrison volumes | `cyberware`, `mercenary` | `−1534.236, 1818.981, 32.380` | `data/sites/sites.json` site 192 `ma_wat_lch_01` | `ma_wat_ich_01_outpost_com` (12); 12 roster units; AV-spawn triggers, 6 guard volumes, 24 spots, 7 patrols | `[game-data]` `[wiki]` |
| 12 | **Eisenhower St. housing block** | Housing block → chop den with joytoy brothel + ripper clinic | Watson / Kabuki | **Yes** — 1st floor, 2nd floor, basement; separate entrances for `ripper` and `solo` | `cyberware`, `sex_work`, `braindance` | `−1111.469, 2146.427, 12.157` | `data/sites/sites.json` site 395 `sts_wat_kab_05` | `{kab_05_com_1st_floor}` (4), `…_1st_floor_prostitutes`, `…_2nd_floor` (2); 6 roster units; 5 doors, 20 triggers | `[game-data]` `[wiki]` |
| 13 | **Allen St. rooftop slums** | Rooftop shantytown + processing building | Watson / Kabuki | **Yes** — at least one enterable building (`#kab_101_tr_boss_enter_building`); the rest is rooftop shacks | `cyberware`, `sex_work` | `−1097.405, 1440.894, 16.600` | `data/sites/sites.json` site 399 `sts_wat_kab_101` | `kab_101_com` (8); 8 roster units; 4 guard volumes, 22 spots, 4 patrols | `[game-data]` `[wiki]` |
| 14 | **Wild Blue bunkhouse** | Hotel parking lot + bunkhouse den | Pacifica / Coastview | **Yes** — bunkhouse interior per wiki; no door node | `cyberware`, `mercenary` | `−1971.236, −2165.879, 24.839` | `data/sites/sites.json` site 97 `ma_pac_cvi_09` | `ma_pac_cvi_09_com` (7); 7 roster units; 2 guard volumes, 15 spots, 4 patrols | `[game-data]` `[wiki]` |
| 15 | **Pacific Blvd scav den** (Anton Kolev) | Street-level den | Pacifica / WestWindEstate | No — 4 melee scavs, one guard volume, no doors | `cyberware`, `mercenary` | `−2887.351, −2153.889, 1.320` | `data/sites/sites.json` site 114 `ma_pac_wwd_04` | `ma_pac_wwd_04_com` (4); 4 roster units; 8 spots, 2 patrols | `[game-data]` `[wiki]` |
| 16 | **Badlands harvesting warehouse** | Warehouse with a vehicle bay | Badlands / Badlands | **Yes** — warehouse + `vehicle_bay` suitability | `cyberware`, `vehicles_chop` | `1056.978, −714.063, 22.271` | `data/sites/sites.json` site 1 `ma_bls_ina_01` | `ma_bls_ina_se1_01_com` (7); 7 roster units; 3 guard volumes, 15 spots, 4 patrols, 3 devices | `[game-data]` `[inferred]` |

### 3.1 How the name→coordinate links were proven

Join order was **wiki `baseid` → `sites.json` code → node names → markers**
(§1.1 item 1), with the wiki's own walkthrough used to resolve two locations the
infobox gets wrong. The baseid join is what did the work here: sixteen of the
twenty-four candidate sites have a wiki page carrying the exact code.

- **`sts_ep1_04` → The Scraper** (*Gig: Prototype in the Scraper*). The wiki
  infobox carries `baseid = sts_ep1_04`, `location = Construction site, the
  Scraper, Longshore Stacks`, and the article says "the Scavengers were using
  the location as one of their hideouts … a keycode-locked door to an armory on
  the ground floor near the elevator. The code is **2045**." The site's doors
  match: `#sts_ep1_04_lift`, `#lift_door_1`, `#lift_door_2`,
  `#sts_ep1_04_upper_loot_room_door`, `#ep1_04_dvc_prison_gate`. 43 roster units
  — the faction's largest garrison. `[game-data]` `[wiki]`
- **`sts_ep1_03` → Los Osos (West Wind Estate)** (*The Man Who Killed Jason
  Foreman*). The gig's shard "leads the merc to a former motel in Pacifica, Los
  Osos", and the motel's own page gives `gangs = Scavengers` and the street
  "Catalina & Santa Maria", `sub_district = West Wind Estate`. 18 roster units.
  The site anchor is 83 m from the community cluster, so the community position
  is used (§2.3 item 4). `[game-data]` `[wiki]`
- **`sts_ep1_08` → Organitopia** (*Gig: Spy in the Jungle*). `baseid =
  sts_ep1_08`; the walkthrough says Mark Bana "is being hunted by Scavengers led
  by Boris Ribakov at **Organitopia** in Terra Cognita", and Organitopia's
  page gives `type = Natural history museum`, `gangs = Scavengers`. 16 roster
  units, including `Character.sts_ep1_08_kgb_boss`. `[game-data]` `[wiki]`
- **`sts_wat_kab_101` → Allen St. rooftop slums** (*Gig: Small Man, Big Evil*).
  `baseid` match; `location = Rooftop slums near Allen St.`; the journal entry
  explains Jae-Hyun "kidnaps them, and delivers them to scaves for biomon or
  other cyberware removal". 8 roster units. `[game-data]` `[wiki]`
- **`sts_wat_kab_05` → Eisenhower St. housing block** (*Gig: Last Login*).
  `baseid` match; `location = Housing block on Eisenhower St.`; "The building is
  guarded by several Scavengers. In the center of the main floor a joytoy is
  seen watching TV with a Scav … Turns out Alois didn't skip town … was killed
  and ravaged for parts." Node names confirm the layout: `#kab_05_ga_1st_floor`,
  `#kab_05_ga_2nd_floor`, `#kab_05_tr_basement`,
  `#kab_05_tr_ripperdoc_clinic`, `#kab_05_ws_prostitute_male/female_001`,
  `#kab_05_entrance_door_ripper`. `[game-data]` `[wiki]`
- **`ma_pac_cvi_12` → Eden Beach Mega Ride** (*SOCA: Wipe the Gonk, Take the
  Implants*). `baseid` match; `location = Eden Beach Mega Ride`; the dispatcher
  calls Stanislaus Zbyszko "a known captain amongst scavengers with multiple
  smuggling priors". The guard volumes are `_restrict_movement_wheel_*`
  (the ride's wheel), which is why the point is the Mega Ride, not the whole
  park. `[game-data]` `[wiki]`
- **`ma_wat_nid_01` → Ross Street Parking Facility** (*SOCA: Vice Control*).
  `baseid` match; the location page gives `gangs = Scavengers`, `street = Ross &
  Shipyard Way`. 12 roster units. `[game-data]` `[wiki]`
- **`ma_wat_nid_27` → illegal ripperdoc clinic** (*Reported Crime: Don't Forget
  the Parking Brake!*). `baseid` match; `location = Illegal ripperdoc clinic
  north of Offshore Street`. This is the holding the seed calls "Northside Oil
  Wharf". `[game-data]` `[wiki]`
- **`ma_wat_lch_01` → Opposites Attract rooftop outpost** (*SOCA: Opposites
  Attract*). `baseid` match; `location = Rooftop near the intersection of
  Goldsmith and Cortes Street, west of the MedCenter`. 12 roster units. The
  node names use the internal `ich_01` prefix (`#wat_ich_01_tr_av_spawn`), which
  is why a plain `lch_01` grep finds nothing. `[game-data]` `[wiki]`
- **`ma_pac_cvi_09` → Wild Blue bunkhouse**. No wiki page carries the code. The
  link is Misha Orlova's biography: she "witnessed the attack on mercenary Ellen
  Verde in the parking lot and bunkhouse near the **Wild Blue** hotel on Pacific
  Boulevard, Coastview", and the site's roster contains
  `Character.ma_pac_cvi_09_scavenger_fast3_fmelee3_machete_wa_elite_Misha_Orlova`
  plus `la_organ_harvesting_01_*` workspots. `[game-data]` `[wiki]` `[inferred]`
- **`ma_pac_wwd_04` → Pacific Blvd scav den** (*SOCA (West Wind Estate)*).
  `baseid` match; the dispatcher names "Anton Kolev, a known leader amongst
  scavengers". The page says Pacific Boulevard; the site anchors on West Wind
  North Towers. I keep the site anchor and flag the mismatch (§8.4). `[game-data]`
  `[wiki]`

**Area/marker-only places** (§1.1 item 3 — main-quest and PL interiors have no
site row):

- **Scavenger Den.** The wiki article names it and the address ("apartments 1235
  and 1237 … on Crescent Street in JapanTown"). There is no site and no marker
  called "den"; the identification is the *Sweet Dreams* area name
  `{mq036_com_scavengers}` plus the *Rescue* markers
  (`q001_00c_sm_rescuing_girl`, `q001_mp_boss_door_hack_icon`,
  `q001_mp_lift_terminal`) at the same x/y/z. `mq036_overload` and `q001_intro`
  both name `[[Scavenger Den]]` as their location in their infoboxes, and the
  den page says the *Sweet Dreams* branch returns V to it. `[game-data]` `[wiki]`
- **Electric Corporation Power Plant.** `Disasterpiece` has `baseid =
  q105_03_braindance_studio` and its objectives read "Ride with Judy to the old
  power plant in **Charter Hill** … Get to level-1 … Lead Judy through the
  sub-levels". The plant's page says "the Scavengers use it as a base of
  operations for their illegal braindance (XBD) activities" and puts the Errata
  katana "at the forge inside the Electric Corporation Power Plant". The studio
  markers (`q105_07_sm_blackmarket_braindance` at `z = −16.65`,
  `q105_08a_sm_braindance_investigation`, `q105_09_sm_braindance_evelyn`) and
  three `q105_com_braindance_combat_floor_*` communities (32 entries) sit at
  `(32, −511)`. The anchor used is the ground-floor combat community, because
  the street-level markers are 16 m below. `[game-data]` `[wiki]`
- **Digimmortal.** `mq306` = *No Easy Way Out*: V meets Aaron "at the
  Digimmortal exposition in Terra Cognita", the scavs there "can turn hostile if
  V strays too far from the path to the exit", and the venue's page gives
  `gangs = Scavengers`. `{mq306_com_scavengers}` (24) + `…_exit` (13) sit on it.
  `[game-data]` `[wiki]`
- **ESC Explorer.** `we_ep1_17` = *Increased Criminal Activity: SCAVENGERS*:
  "A group of Scavengers are hiding out at the ESC Explorer in Terra Cognita",
  and the venue's page says the building "had been taken over by the
  Scavengers, who used it as a base for their weapons smuggling operations".
  `{we_ep1_17_com}` (17) + `…_2nd_loop` (12). `[game-data]` `[wiki]`

### 3.2 Scavenger-occupied generic sites (the filler pool)

Deduped `sites.json` rows with Scavenger units that are **not** a named catalog
point. `suitability` tags are gameplay affordances, not lore. Ten sites, no
two within 25 m.

| Site | Sub-district | Units | Suitability tags | Coordinates | Note |
| --- | --- | ---: | --- | --- | --- |
| `sts_ep1_01` | Dogtown | 16 | rooftop_access 80, elevator 70, officer_site 60 | `−1633.425, −2509.814, 39.350` | **Haven Clinic** — scavs storm a ripper clinic, they do not own it (§8.2) |
| `ma_pac_wwd_02` | WestWindEstate | 8 | raid_target 87, rooftop_access 72, officer_site 60, branch_office 45 | `−2799.222, −2711.590, 22.840` | Scav den **raided by Wraiths** (`_scav_*` + `_wraith_*` workspots); `wraiths.md` counts it as a Wraith point |
| `ma_wat_kab_06` | Kabuki | 6 | raid_target 81, rooftop_access 80, stealth_entry 65, camera_net 61 | `−1000.250, 2009.897, 44.360` | *Assault in Progress, Charter St.* — Tyger Claws vs Scavengers at an industrial site; generic `merc_01…03` records |
| `ma_wat_kab_09` | Kabuki | 4 | raid_target 72, rooftop_access 68, camera_net 61, stealth_entry 60 | `−1164.983, 1479.155, 18.096` | *Assault in Progress, Adams St.* |
| `ma_hey_spr_10` | Wellsprings | 4 | raid_target 84, hostage_site 50 | `−2106.440, −756.753, 7.615` | Execution scene (`la_execution_01_*`); the lore's "southern Wellsprings" |
| `ma_pac_cvi_07` | Coastview | 3 | rooftop_access 80, raid_target 69 | `−1551.150, −1849.488, 73.580` | Rooftop squat with homeless workspots; netrunner Michal Glowinski |
| `ma_wbr_jpn_07` | JapanTown | 3 | raid_target 81, stealth_entry 65, rooftop_access 62, camera_net 61, club 55, hostage_site 50 | `−550.195, 1170.515, 12.110` | *Reported Crime: Lost and Found* — an alley scrap with Tyger Claws, 400 m from the den |
| `ma_wbr_jpn_08` | JapanTown | 3 | rooftop_access 70, camera_net 69, raid_target 63, stealth_entry 60, hostage_site 50 | `−661.351, 287.662, 20.170` | Street-violence workspots; the only scav site in Japan Town besides the den |
| `ma_cct_dtn_03` | Downtown | 2 | raid_target 75, rooftop_access 58 | `−2150.783, 279.315, 8.010` | *Cyberpsycho Sighting: On Deaf Ears* — two scavs in a car, not a holding |
| `ma_wat_lch_05` | LittleChina | 2 | rooftop_access 66, raid_target 51 | `−1260.724, 1305.992, 16.978` | *Reported Crime: Paranoia* — crime scene |

Excluded from both tiers (§1.2 item 4, machines are not a garrison):
`ma_pac_cvi_15` (Coastview, **2 droids only**) and `mws_cz_04` (Dogtown,
**1 droid only**). Both carry `default_faction_id = 7`, so a faction-id filter
without a roster check would seed two robotic "dens". `[game-data]`

---

## 4. Economic structure

### 4.1 Revenue streams → catalog locations

| Revenue stream | Code(s) | Catalog locations that produce it | Evidence / notes |
| --- | --- | --- | --- |
| Harvested chrome and organs | `cyberware` | All 16; strongest at the Scavenger Den (6), the Power Plant (2), Los Osos (7), Organitopia (4), the ripper clinic (10) | "Scavengers are the main suppliers for low-end cyberware for other gangs, small-time criminals, and shady ripperdocs"; victims "stripped of identities". `[wiki]` |
| Illegal braindance (XBD) | `braindance` | Power Plant (2) — "base of operations for their illegal braindance (XBD) activities"; Scavenger Den (6) — the *Sweet Dreams* BD; Eisenhower block (12) — a scav scrolling a BD | `[wiki]` `[game-data]` |
| Abduction and contract violence | `mercenary` | Every den; the business model is "assault, abduction, mutilation, and dismemberment" plus hired "heists, hit jobs, and abductions" | `[wiki]` |
| Weapons | `arms` | The Scraper armory (1, keycode 2045); ESC Explorer (8) — "weapons smuggling operations" | `[wiki]` `[game-data]` |
| Contraband logistics | `smuggling` | ESC Explorer (8); Eden Beach Mega Ride (5) — Zbyszko has "multiple smuggling priors" | `[wiki]` |
| Trafficking / joytoy trade | `sex_work` | Scavenger Den (6) — Sandra Dorsett's abduction; Allen St. (13) — Jae-Hyun "delivers them to scaves"; Eisenhower block (12) — joytoy + prostitute workspots | `[wiki]` `[game-data]` |
| Vehicle stripping | `vehicles_chop` | Badlands warehouse (16) — `vehicle_bay` + `warehouse` suitability, `ws_car_01/02` workspots | `[game-data]` |

Three modelling cautions:

- **`cyberware` is the economy, not a side line.** Eight of the ten filler sites
  also carry `raid_target` suitability ≥ 63 — they are places to be raided, not
  shops. Only the two named trafficking sites and the Scraper's armory have a
  second strong stream. `[game-data]`
- **No `drugs` line, despite the "junkies" flavour.** The only drug reference
  near a scav site is *Lost and Found*'s Tyger stash, which the scavs stumbled
  onto rather than ran. Do not give the Scavengers a drug lab. `[wiki]`
- **No `protection`.** Scavs do not tax businesses; they prey on people. There
  is no extortion record anywhere in the extract. `[wiki]` `[game-data]`

### 4.2 Suppliers, customers, rivals

| Role | Party | Detail |
| --- | --- | --- |
| Customer (bulk chrome) | Other gangs, small-time criminals, shady ripperdocs | "the main suppliers for low-end cyberware"; the whole point of the dens. `[wiki]` |
| Customer (contracts) | Fixers — Mr. Hands, Regina Jones, Wakako Okada | Mr. Hands gives the three Dogtown gigs (Scraper, Los Osos, Organitopia); Regina gives the two Kabuki gigs (Allen St., Eisenhower); Wakako gives *The Rescue*. The scavs are the *target*, which is why the fixers know the addresses. `[wiki]` |
| Supplier (rare, inverted) | **Aldecaldos** | *Gun Music*: Cassidy, Carol and Teddy "went into Night City to deliver cyberware to a group of Scavengers" — scavs as buyers, at an Arroyo industrial complex. `[wiki]` |
| Buyer (bribed tolerance) | **Barghest / Kurt Hansen** | "the scav oligarchy secures business in Hansen's backyard … why would Hansen tolerate them? Simple. It's all about the money." `[wiki]` |
| Rival | **Wraiths** | Same trade, competing: they raid scav dens at `ma_pac_wwd_02` and the SOCA at `ma_pac_wwd_04` lists both gangs. `[wiki]` `[game-data]` |
| Rival | **Tyger Claws** | *Lost and Found* is a scav-vs-Tyger scrap in a Japantown alley; the Opposites Attract outpost and both Kabuki dens sit inside Tyger turf. `[wiki]` |
| Rival (internal) | Night City scavs vs Dogtown scavs | "a bit of disdain for their poorer NC kind … only those without a knack for business end up in Night City". `[wiki]` |
| Rival | **Maelstrom** | *Paranoia* pairs scavs with Maelstrom at a Little China scene. `[wiki]` |
| Law | NCPD, Mr. Hands, BARGHEST | Thirteen of the sixteen named places are NCPD scanner activities or fixer gigs; the other three are main/side jobs. Dogtown scavs operate only with Barghest's tolerance. `[game-data]` `[wiki]` |

The scavs are **price-takers, not a brand**. They have no product line of their
own beyond second-hand chrome, and they buy tolerance in Dogtown rather than
holding ground. Model each den as an independent cell with its own yield and no
faction-wide multiplier beyond the `cyberware` tag.

---

## 5. Headquarters recommendation

### Primary (PLACEHOLDER) HQ: **The Scraper** — Dogtown, Longshore Stacks

Coordinates: `−2465.287, −2713.544, 21.820` `[game-data]`
`data/sites/sites.json` site 357 `sts_ep1_04`.

> **Placeholder, not canon.** The Scavengers have no headquarters. The wiki
> organization infobox leaves `headquarters` and `faction_locations` blank, the
> faction text says they "have no designated piece of turf", and
> `data/faction_headquarters.json` has no fid-7 row. `[wiki]` `[game-data]`
> The Scraper is nominated because it is the most *seat-like* den in the game
> data, not because any source calls it an HQ. Treat it as the org layer's
> spawn seat and expect to move it if a later pass prefers the canon den.

Rationale:

1. **It is the faction's largest garrison by a wide margin.** 43 roster units at
   one site — more than the next two (Eden Beach 16, Organitopia 16) combined,
   and 20% of all 210 scav units. `[game-data]`
2. **It is a whole building, not a room.** An unfinished 4-star hotel: ground
   floor, upper floors, a working lift (`#sts_ep1_04_lift`, `#lift_door_1/2`), a
   keycode-locked **armory** (2045), a **prison gate**
   (`#ep1_04_dvc_prison_gate`), a **shutter window** entry and an upper loot
   room. That is exactly the room set an org layer wants: lobby, vault, cells,
   boss floor, roof. `[game-data]` `[wiki]`
3. **It covers three of the four revenue streams in one building** — chrome
   (the stolen Zetatech prototype carried in Hasan Demir's eye), arms (the
   armory), and hired violence (the garrison). `[wiki]`
4. **It fits the faction's self-image.** The lore calls it a hideout the
   Scavengers took over after the Unification War killed the hotel project; the
   Dogtown database entry says these scavs are the organised, well-equipped
   wing. A squat in an unfinished tower is the most honest possible "HQ" for a
   gang with no hierarchy. `[wiki]`
5. **The records are already rich enough to hook a prototype into:** 9 doors, 43
   roster units across 5 communities, rooftop access and an elevator suitability
   tag. Only Organitopia matches it on doors (9), with 16 units to its 43.
   `[game-data]`

Trade-off: **Dogtown, outside the seeded footprint.** The seed gives the
Scavengers five sub-territories, none in Dogtown, and the nearest CC
(`cc_wwd_highway_gate`, Animals-owned) is 170 m away. Choosing the Scraper means
adding one Dogtown point and relocating an active CC there rather than reusing a
seeded one. It is also quest-gated behind a Mr. Hands gig, and its site anchor
has no `bbox` (§1.1 item 7).

### Alternate 1: **Electric Corporation Power Plant** — Charter Hill

Coordinates `31.935, −510.770, 1.304` `[game-data]`
`areas.jsonl` `{q105_com_braindance_combat_floor_}0`.

The best *interior* after the Scraper: a warehouse ground floor plus three
sub-levels, a forge (Errata), three combat-floor communities totalling 32
entries. It is the faction's most famous set piece and its clearest
`braindance` revenue site. It loses on three counts: it has **no `sites.json`
row** (no doors, no guard volumes, only areas and quest markers), its only
entrance is a main-quest route, and it is a single-purpose XBD studio rather
than a place scavs live. It also sits in Tyger Claws-contested Charter Hill, 245 m
from a Tyger-owned CC. `[game-data]` `[wiki]`

### Alternate 2: **Scavenger Den** — Japan Town

Coordinates `−455.188, 400.266, 136.266` `[game-data]`
`markers.jsonl` `mq036_sm_scavengers`.

The **canon** den and the only place the wiki gives a street address for. It is
the faction's first impression in *The Rescue*, reused by *Sweet Dreams*, with
two apartment interiors, a lift terminal, a boss door and 27 entries. It loses
on capacity: two apartments on one corridor is a hideout, not a seat, and it
sits in Tyger Claws' Japan Town with a Tyger-owned CC 140 m away. Keep it as the
faction's **prestige/identity** point even if the Scraper takes the org seat.

### Overruled / downgraded suggestions

- **Eden Beach Mega Ride as HQ** — the strongest *seed-aligned* candidate: its
  nearest CC is the scav-held `cc_cvi_pacifica_pier` at **48.1 m**, 16 units, a
  named captain and nine patrols. But it is an open-air ride deck with no
  interior, so it is a capture point, not a seat. Rank 5.
- **Digimmortal as HQ** — 37 entries (the second-largest concentration) in a
  three-level expo hall, and the venue's page lists Scavengers as its gang. It
  loses because it is area-only (no site, no doors) and because the scavs share
  it with Aaron's Animals storyline. Rank 3.
- **Los Osos as HQ** — a dead motel with 18 units and a boss; the most
  *classically scav* venue (rooms, chrome, a corpse). Too small and on the coast
  edge. Rank 7.
- **Organitopia as HQ** — a museum with a dinosaur hall; great flavour, but a
  quest set piece with one entrance. Rank 4.
- **Haven Clinic as HQ or holding** — 16 roster units and
  `default_faction_id = 7` make it *look* like the faction's biggest Watson den.
  It is Nika Yankovich's crew occupying someone else's clinic during *Dogtown
  Saints* (§8.2). Not a holding.
- **"Scavengers Badlands Compound" or any territorial seat** — no such thing
  exists in any source. Do not invent one.

---

## 6. Priority list of control points

Ranked by how well each place serves as a capturable Scavenger control point.
"CC" = nearest entry in `data/control_centers.json` (active or not); distance is
horizontal metres; the owner is the owning faction of that CC's sub-territory.
Relevance reflects lore + revenue + record richness, not raw unit count.

| Rank | Control point | Rel. (1–5) | District / sub-district | Coordinates | Existing CC overlap | Why |
| ---: | --- | :---: | --- | --- | --- | --- |
| 1 | **The Scraper** | 5 | Pacifica / Dogtown | `−2465.287, −2713.544, 21.820` | `cc_wwd_highway_gate`, 170.1 m (**Animals**) | Placeholder HQ; 43 units; lift, armory, prison, 9 doors |
| 2 | **Electric Corporation Power Plant** | 4 | Westbrook / CharterHill | `31.935, −510.770, 1.304` | `cc_hil_le_le_park`, 245.2 m (**Tyger Claws**) | *Disasterpiece* XBD base; 3 sub-levels; 32 entries |
| 3 | **Digimmortal** | 4 | Pacifica / Dogtown | `−2347.550, −3063.500, 129.540` | `cc_wwd_highway_gate`, 215.2 m (**Animals**) | 37 entries, 3 expo levels; scav-garrisoned |
| 4 | **Organitopia** | 4 | Pacifica / Dogtown | `−2227.138, −3019.134, 115.270` | `cc_wwd_highway_gate`, 274.0 m (**Animals**) | Scav museum den; 16 units; 9 doors |
| 5 | **Eden Beach Mega Ride** | 4 | Pacifica / Coastview | `−2433.580, −2199.374, 15.980` | `cc_cvi_pacifica_pier`, **48.1 m** (**Scavengers**) | 16 units, named captain, real `bbox`; seed-aligned |
| 6 | **Scavenger Den** (Crescent St.) | 4 | Westbrook / JapanTown | `−455.188, 400.266, 136.266` | `cc_jpn_cherry_blossom`, 140.4 m (**Tyger Claws**) | Canon den; 27 entries; two apartment interiors |
| 7 | **Los Osos motel** | 3 | Pacifica / WestWindEstate | `−2554.542, −2435.019, 16.950` | `cc_wwd_coastline_ruins`, **22.4 m** (Voodoo Boys) | 18 units; motel rooms + doors; a CC already sits on it |
| 8 | **ESC Explorer** | 3 | Pacifica / Dogtown | `−2272.990, −2947.700, 111.470` | `cc_wwd_highway_gate`, 202.8 m (**Animals**) | Weapons-smuggling base; 3 floors + catwalk; 29 entries |
| 9 | **Ross Street Parking Facility** | 3 | Watson / Northside | `−1734.613, 2431.407, 7.260` | `cc_nid_totentanz_yard`, 62.9 m (Maelstrom) | 12 units, 6 guard volumes, 33 spots, 7 patrols, 3 devices |
| 10 | **Illegal ripperdoc clinic** | 3 | Watson / Northside | `−1111.159, 3318.479, 8.531` | `cc_nid_oil_refinery`, **5.8 m** (**Scavengers**) | 7 units; the seeded Northside CC stands on it |
| 11 | **Opposites Attract rooftop outpost** | 3 | Watson / LittleChina | `−1534.236, 1818.981, 32.380` | `cc_lch_canal_overpass`, 340.5 m (Tyger Claws) | 12 units, AV-spawn triggers, 7 patrols, 3 devices |
| 12 | **Eisenhower St. housing block** | 2 | Watson / Kabuki | `−1111.469, 2146.427, 12.157` | `cc_kab_pinewood_block`, 162.6 m (Tyger Claws) | **Test point** — 5 doors, 2 floors + basement, ripper clinic |
| 13 | **Allen St. rooftop slums** | 2 | Watson / Kabuki | `−1097.405, 1440.894, 16.600` | `cc_kab_allen_street`, 107.7 m (Tyger Claws, **active**) | 8 units; trafficking processing site; its CC is one of 15 active CCs |
| 14 | **Wild Blue bunkhouse** | 2 | Pacifica / Coastview | `−1971.236, −2165.879, 24.839` | `cc_cvi_south_boulevard`, **8.5 m** (Voodoo Boys) | 7 units, organ-harvest workspots, Misha Orlova |
| 15 | **Pacific Blvd scav den** | 2 | Pacifica / WestWindEstate | `−2887.351, −2153.889, 1.320` | `cc_wwd_apartments_north`, **9.5 m** (**Scavengers**) | 4 melee units; Anton Kolev; the seeded West Wind CC stands on it |
| 16 | **Badlands harvesting warehouse** | 2 | Badlands / Badlands | `1056.978, −714.063, 22.271` | `cc_rcr_tama_viewpoint`, 146.2 m (6th Street) | Only Badlands holding; warehouse + vehicle bay; 7 units |

### Test control point for the first in-game test: **Eisenhower St. housing block**

Site 395 `sts_wat_kab_05` (*Gig: Last Login*), coordinates
`−1111.469, 2146.427, 12.157`, `[game-data]` `data/sites/sites.json`.

Why this and not the HQ:

- **Clean, provable ownership.** `default_faction_id = 7` **and** six
  `faction_id == 7` roster entries. The wiki independently says "The building is
  guarded by several Scavengers." Eviction has no ambiguity. `[game-data]`
  `[wiki]`
- **The best enclosed interior of any scav site.** Node names give three levels:
  `#kab_05_ga_1st_floor`, `#kab_05_ga_2nd_floor`, `#kab_05_tr_basement`,
  `#kab_05_tr_inside`, `#kab_05_tr_entrance`. Two floors and a basement is enough
  to validate a vertical capture volume. `[game-data]`
- **Five doors and 20 triggers** — more than any other scav site except the
  Scraper (9 doors, but marker-only and quest-gated). Doors are exactly what a
  lock/alarm/defence prototype needs. `[game-data]`
- **It exercises the METHOD §1.2 item 8 trap on purpose.** The first floor is a
  joytoy brothel (`#kab_05_ws_prostitute_male/female_001`,
  `{kab_05_com_1st_floor_prostitutes}`) and a ripper clinic
  (`#kab_05_tr_ripperdoc_clinic`, `#kab_05_entrance_door_ripper`) inside a
  housing block. A glance at the roster would file it under the Mox; the
  faction id and the gig text say Scavengers. Capturing it proves the seed reads
  ownership from the right field. `[game-data]` `[wiki]`
- **Not the HQ and not an alternate HQ.** Rank 12 on lore relevance, first on
  capture-fitness — which is the priority order §3.8 sets for the test point.
- **Fallback if the gig scene interferes: Ross Street Parking Facility**
  (`ma_wat_nid_01`, 12 units, 6 guard volumes, 33 spots, 7 patrols, 3 devices,
  `default_faction_id = 7`, named facility page). It is a garage, so there are
  no interior doors, but the guard/device record is the richest of any open
  scav site.

Do **not** use the seeded CC on `wwd_central_courtyard` as the test point: it
has no Scavenger holding at all (§8.6).

---

## 7. Per-sub-district counts

This is the number to feed yield balancing. `named` counts distinct lore-relevant
places the Scavengers own, run or habitually occupy — one entry per place, not
per quest variant. `filler` is the deduped occupied-site count minus any site
already counted as a named place (`METHOD.md` §8). Machine-only sites (110, 301)
are excluded from both.

| Sub-district | Named lore-relevant places | Which ones | Occupied sites (deduped) | Filler | Noteworthy interiors |
| --- | ---: | --- | ---: | ---: | --- |
| Dogtown | **4** | The Scraper, Digimmortal, Organitopia, ESC Explorer | 3 | 1 | Scraper (lift/armory/prison); Organitopia (2 halls); Digimmortal (3 levels); ESC Explorer (3 floors) |
| Coastview | **2** | Eden Beach Mega Ride, Wild Blue bunkhouse | 3 | 1 | Wild Blue bunkhouse |
| WestWindEstate | **2** | Los Osos motel, Pacific Blvd den | 3 | 1 | Los Osos rooms |
| JapanTown | **1** | Scavenger Den (Crescent St.) | 2 | 2 | Scavenger Den (2 apartments) |
| CharterHill | **1** | Electric Corporation Power Plant | 0 | 0 | Power plant (3 sub-levels) |
| Kabuki | **2** | Eisenhower St. housing block, Allen St. rooftop slums | 4 | 2 | Eisenhower block (2 floors + basement) |
| Northside | **2** | Ross Street Parking Facility, illegal ripperdoc clinic | 2 | 0 | Parking garage; clinic |
| LittleChina | **1** | Opposites Attract rooftop outpost | 2 | 1 | None (rooftop) |
| Badlands | **1** | Badlands harvesting warehouse | 1 | 0 | Warehouse |
| Wellsprings | 0 | execution scene only | 1 | 1 | None |
| Downtown | 0 | cyberpsycho scene only | 1 | 1 | None |
| Arroyo / RanchoCoronado / CorpoPlaza / Glen | 0 | ambient events and quest crowds only | 0 | 0 | None |
| **Total** | **16** | | **22** | **10** | |

Reconciliation (`named + filler = 26`, §1.1 item 17):

- **24 candidate sites − 2 machine-only = 22 occupied sites.**
- **12 of the 16 named places are site-backed** (Scraper, Organitopia, Eden
  Beach, Los Osos, Ross Street, ripper clinic, Opposites Attract, Eisenhower,
  Allen St., Wild Blue, Pacific Blvd, Badlands warehouse), so
  **22 − 12 = 10 filler**. ✓
- **4 named places are marker/area-only** (Scavenger Den, Power Plant,
  Digimmortal, ESC Explorer).
- `22 occupied + 4 area-only = 26 = 16 named + 10 filler`. ✓

Interpretation for yield:

1. **Dogtown is the only four-name sub-district and should carry the high-yield
   scav economy** — but it is Barghest's district, so these points should read as
   *enclaves inside hostile turf*, not as Dogtown ownership. `[inferred]`
2. **Northern Pacifica (Dogtown + Coastview + West Wind) holds 8 of 16 named
   places and 59% of all entries.** Yield weights should follow the entries, not
   the sub-district count.
3. **Japan Town and Charter Hill each have exactly one named place** (the canon
   den and the power plant) and **zero filler**. They are high-per-point,
   low-count zones — exactly where a named-place multiplier is justified.
4. **Wellsprings and Downtown are presence-only.** The lore's "southern
   Wellsprings" concentration is real (4 units at `ma_hey_spr_10`) but it is an
   execution scene, not a den. Do not give the faction a Wellsprings holding on
   the strength of the wiki sentence.

---

## 8. Gaps and uncertainties

1. **The faction has no HQ and this document invents a placeholder.** The
   organization infobox leaves `headquarters` blank, the text says "no
   designated piece of turf", and `faction_headquarters.json` has no fid-7 row.
   The Scraper in §5 is the most seat-like den, not a canon seat. If the mod
   needs a *canon* anchor instead, use the Japan Town Scavenger Den and accept
   that it is two apartments. `[wiki]` `[game-data]`
2. **Haven Clinic (`sts_ep1_01`, 16 units) is a false positive.**
   `default_faction_id = 7` with sixteen scav roster units is exactly the signal
   the method tells you to trust, but *Gig: Dogtown Saints* has Nika Yankovich's
   scavengers **storm** the clinic and barricade the ripperdoc in his office —
   they are occupiers of someone else's business during a quest, not its owners.
   §1.2 item 9 applies; it is filler, not named. This is the sharpest "presence
   ≠ ownership" trap for this faction, sharper than the KGB-hologram case.
   `[game-data]` `[wiki]`
3. **METHOD §1.1 item 11 is wrong about `sts_ep1_08`.** It is listed as a "KGB
   holograms" presence trap. It *is* the site of *Spy in the Jungle*, which
   contains an Arasaka hologram scene (`{sts_ep1_08_holograms_*}`, 23 Arasaka
   entries, `sts_ep1_08_kgb_boss`), but the gig's actual location is
   **Organitopia**, the scav-garrisoned natural-history museum, with **16 human
   scav roster units** and `gangs = Scavengers` in the location infobox. It is a
   named holding and should be counted. Worse, its `default_faction_id` is **20
   (Arasaka)**, so a `default_faction_id == 7` filter drops a real scav den.
   `[game-data]` `[wiki]`
4. **The SOCA (West Wind Estate) page and its site disagree on the location.**
   `ma_pac_wwd_04` is catalogued at "Pacific Boulevard" but its anchor
   (`−2887.351, −2153.889`) is on West Wind North Towers. I kept the site anchor
   because the wiki gives no coordinate and §6 forbids inventing one. Worth a
   quick in-game check before renaming the seeded `wwd_apartments_north` CC.
   `[game-data]` `[wiki]`
5. **The Scavenger Den has no site and no dedicated marker.** Its evidence is an
   area (`{mq036_com_scavengers}`) plus *Rescue* scene markers. The address
   ("apartments 1235 and 1237, Crescent Street") comes from the wiki and is
   identity evidence, not a coordinate — a useful pattern the method does not
   mention: wiki street addresses can pin a place when the coordinate still has
   to come from a record. `[wiki]` `[game-data]`
6. **The seed's `wwd_central_courtyard` holding is empty.** 0 scav sites within
   180 m; the nearest scav record is `{cs_handcuffed_gangoons_com}_025` (2
   handcuffed prisoners) 30 m away, on a `q305` 6th Street ambush set. Either
   move `cc_wwd_central_courtyard` onto Los Osos (which is 700 m west) or drop
   the sub-territory. This is the §1.2 item 13 check failing for one of five
   seeded points. `[game-data]`
7. **The lore's "southern Wellsprings" concentration is thin in the extract.**
   Three areas / 10 entries, one site (`ma_hey_spr_10`, 4 units) which is an
   execution scene. Either the 2.5 build diverges from the World Book sentence,
   or the real Wellsprings scav activity is in the unextracted sectors. Do not
   seed a Wellsprings holding. `[wiki]` `[game-data]`
8. **`ma_bls_ina_01` has no wiki identity.** The Badlands harvesting warehouse is
   proven only by its own records: 7 scav units, `#la_organ_harvesting_01_*`
   workspots, `warehouse`/`vehicle_bay`/`hostage_site` suitability and a
   `source_path` of `badlands/inland_avenue_se1`. No wiki page carries
   `ma_bls_ina_01` or `ma_bls_ina_se1_01`. The name in §3 is descriptive and
   flagged `[inferred]`. If a later pass finds the activity's title, rename it.
   `[game-data]` `[inferred]`
9. **The Electric Corporation Power Plant's district is contested by the wiki
   itself.** Its infobox says Arroyo; the *Disasterpiece* objectives say "the old
   power plant in **Charter Hill**"; the markers are at `(32, −511)` (Charter
   Hill). There is also a real `#c_santo_domingo/arroyo/loc_q104_power_plant`
   prefab — that is the *Lightning Breaks* (q104) power station at
   `(−36, −2645)`, a different building. I catalogued the scav plant as Charter
   Hill and flagged the prefab confusion so nobody seeds the q104 station by
   mistake. `[wiki]` `[game-data]`
10. **Two sites are machine-only but faction-tagged.** `ma_pac_cvi_15` (2 droids,
    `default_faction_id 7`) and `mws_cz_04` (1 droid, fid 7, owned by Barghest's
    sub-territory). §1.2 item 4 applies; excluded. One more machine sits inside a
    real garrison (`Character.nid_scavenger_android_android2_pulsar_ma` at Ross
    Street). Raw units are 210; humans in garrison roles are 206. `[game-data]`
11. **`is_interior` is 0 on all 21 site-backed points**, including the Scraper
    (a hotel with a lift and an armory) and the Eisenhower housing block (two
    floors plus a basement). Every interior above is proven from node names or
    the wiki layout, per §1.2 item 15. `[game-data]`
12. **The Scraper's site anchor has no `bbox` and its communities spread 230 m.**
    The anchor is 13 m from the nearest community, so it is usable, but treat the
    exact capture radius with care. For Los Osos I switched to the community
    position because the anchor is 83 m off. `[game-data]`
13. **Allegiance to Barghest is inferred.** "It's all about the money" is the
    only statement of the relationship. No record models a scav-Barghest tribute;
    if the economy sim wants it, it must be a new mechanic, not a seeded value.
    `[wiki]` `[inferred]`
14. **The Dogtown scav "oligarchy" is not locatable as one place.** The database
    entry implies an organised Dogtown wing, but the data shows four separate
    venues (Scraper, Digimmortal, Organitopia, ESC Explorer) with no shared
    community hash. Model Dogtown as a *cluster*, not a headquarters. `[game-data]`
15. **No vendor or loot records.** "What a den sells" is `[wiki]`/`[inferred]`;
    the extract has suitabilities only. The extract also has no price or
    inventory data for black-market chrome. `[game-data]`

---

## 9. Sources

Local:

- `dist/extract/areas.jsonl` — 104 areas / 560 entries; `{q105_com_braindance_*}`,
  `{mq036_com_scavengers}`, `{q001_scavengers_*}`, `{mq306_com_scavengers}`,
  `{we_ep1_17_com}`, `{sts_ep1_0*_*}`, `{kab_05_com_*}`.
- `dist/extract/markers.jsonl` — `mq036_sm_scavengers`,
  `mq036_mrk_hideout_elevator`, `q001_00c_sm_rescuing_girl`,
  `q001_mp_boss_door_hack_icon`, `q001_mp_lift_terminal`,
  `q105_07_sm_blackmarket_braindance`, `q105_08a_sm_braindance_investigation`,
  `q105_09_sm_braindance_evelyn`, `q105_10_sm_transition`,
  `q000_vr_mp_scav_elevator`.
- `data/sites/sites.json` (sites 1, 25, 81, 95, 97, 107, 110, 112, 114, 175, 178,
  192, 196, 215, 237, 266, 267, 301, 355, 356, 357, 360, 395, 399),
  `rosters.json`, `communities.json`,
  `guards/triggers/spots/patrols/doors/devices.json`, `suitabilities.json`.
- `data/{factions,districts,sub_territories,landmarks,control_centers,spawn_points,faction_headquarters}.json`.
- `dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_0.streamingsector.json`
  — `#c_santo_domingo/arroyo/loc_q104_power_plant_prefab` (the *other* power
  plant, q104; used to rule it out).
- `docs/research/factions/METHOD.md`, `docs/research/factions/wraiths.md`,
  `docs/research/factions/the-mox.md`, `docs/research/factions/tyger-claws.md`.

Wiki (MediaWiki API, `action=parse&prop=wikitext`, 2026-11-25):

- Faction: [Scavengers](https://cyberpunk.fandom.com/wiki/Scavengers) ·
  [Scavengers Members](https://cyberpunk.fandom.com/wiki/Scavengers_Members) ·
  [Scavenger Den](https://cyberpunk.fandom.com/wiki/Scavenger_Den)
- Locations: [The Scraper](https://cyberpunk.fandom.com/wiki/The_Scraper) ·
  [Electric Corporation Power Plant](https://cyberpunk.fandom.com/wiki/Electric_Corporation_Power_Plant) ·
  [Digimmortal](https://cyberpunk.fandom.com/wiki/Digimmortal) ·
  [Organitopia](https://cyberpunk.fandom.com/wiki/Organitopia) ·
  [ESC Explorer](https://cyberpunk.fandom.com/wiki/ESC_Explorer) ·
  [Eden Beach](https://cyberpunk.fandom.com/wiki/Eden_Beach) ·
  [Los Osos (West Wind Estate)](https://cyberpunk.fandom.com/wiki/Los_Osos_(West_Wind_Estate)) ·
  [Ross Street Parking Facility](https://cyberpunk.fandom.com/wiki/Ross_Street_Parking_Facility) ·
  [Wild Blue](https://cyberpunk.fandom.com/wiki/Wild_Blue) ·
  [Dream Gig](https://cyberpunk.fandom.com/wiki/Dream_Gig) ·
  [Haven Clinic](https://cyberpunk.fandom.com/wiki/Haven_Clinic)
- Gigs / jobs (baseid-verified): [The Rescue](https://cyberpunk.fandom.com/wiki/The_Rescue)
  (`q001_intro`), [Sweet Dreams](https://cyberpunk.fandom.com/wiki/Sweet_Dreams)
  (`mq036_overload`), [Disasterpiece](https://cyberpunk.fandom.com/wiki/Disasterpiece)
  (`q105_03_braindance_studio`), [No Easy Way Out](https://cyberpunk.fandom.com/wiki/No_Easy_Way_Out)
  (`mq306`), [Gun Music](https://cyberpunk.fandom.com/wiki/Gun_Music)
  (`mq002_veterans`), [Gig: Prototype in the Scraper](https://cyberpunk.fandom.com/wiki/Gig:_Prototype_in_the_Scraper)
  (`sts_ep1_04`), [Gig: The Man Who Killed Jason Foreman](https://cyberpunk.fandom.com/wiki/Gig:_The_Man_Who_Killed_Jason_Foreman)
  (`sts_ep1_03`), [Gig: Spy in the Jungle](https://cyberpunk.fandom.com/wiki/Gig:_Spy_in_the_Jungle)
  (`sts_ep1_08`), [Gig: Dogtown Saints](https://cyberpunk.fandom.com/wiki/Gig:_Dogtown_Saints)
  (`sts_ep1_01`), [Gig: Last Login](https://cyberpunk.fandom.com/wiki/Gig:_Last_Login)
  (`sts_wat_kab_05`), [Gig: Small Man, Big Evil](https://cyberpunk.fandom.com/wiki/Gig:_Small_Man,_Big_Evil)
  (`sts_wat_kab_101`).
- NCPD activities (baseid-verified): [SOCA: Wipe the Gonk, Take the Implants](https://cyberpunk.fandom.com/wiki/Suspected_Organized_Crime_Activity:_Wipe_the_Gonk,_Take_the_Implants)
  (`ma_pac_cvi_12`), [SOCA: Vice Control](https://cyberpunk.fandom.com/wiki/Suspected_Organized_Crime_Activity:_Vice_Control)
  (`ma_wat_nid_01`), [SOCA: Opposites Attract](https://cyberpunk.fandom.com/wiki/Suspected_Organized_Crime_Activity:_Opposites_Attract)
  (`ma_wat_lch_01`), [SOCA (West Wind Estate)](https://cyberpunk.fandom.com/wiki/Suspected_Organized_Crime_Activity_(West_Wind_Estate))
  (`ma_pac_wwd_04`), [Reported Crime: Don't Forget the Parking Brake!](https://cyberpunk.fandom.com/wiki/Reported_Crime:_Don%27t_Forget_the_Parking_Brake!)
  (`ma_wat_nid_27`), [Reported Crime: Lost and Found](https://cyberpunk.fandom.com/wiki/Reported_Crime:_Lost_and_Found)
  (`ma_wbr_jpn_07`), [Reported Crime: Paranoia](https://cyberpunk.fandom.com/wiki/Reported_Crime:_Paranoia)
  (`ma_wat_lch_05`), [Increased Criminal Activity: SCAVENGERS](https://cyberpunk.fandom.com/wiki/Increased_Criminal_Activity:_SCAVENGERS)
  (`we_ep1_17`).
- Characters: [Misha Orlova](https://cyberpunk.fandom.com/wiki/Misha_Orlova),
  [Nika Yankovich](https://cyberpunk.fandom.com/wiki/Nika_Yankovich).

---

## 10. Machine-readable block

Strict JSON for seeding (contract in [`METHOD.md`](./METHOD.md) §10). Every
coordinate was verified against the local record named in `source` on
2026-11-25; none came from the wiki. `null` means `TBD`, never `0`. The `hq` is
a **placeholder** — see §5.

```json
{
  "faction_code": "scavengers",
  "hq": {
    "name": "The Scraper (placeholder HQ, no canon headquarters)",
    "district": "Pacifica",
    "sub_district": "Dogtown",
    "x": -2465.287,
    "y": -2713.544,
    "z": 21.82,
    "source": "data/sites/sites.json site 357 sts_ep1_04",
    "confidence": "game-data+wiki"
  },
  "alternate_hqs": [
    {
      "name": "Electric Corporation Power Plant",
      "district": "Westbrook",
      "sub_district": "CharterHill",
      "x": 31.935,
      "y": -510.77,
      "z": 1.304,
      "source": "dist/extract/areas.jsonl {q105_com_braindance_combat_floor_}0",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Scavenger Den (Crescent St.)",
      "district": "Westbrook",
      "sub_district": "JapanTown",
      "x": -455.188,
      "y": 400.266,
      "z": 136.266,
      "source": "dist/extract/markers.jsonl mq036_sm_scavengers",
      "confidence": "game-data+wiki"
    }
  ],
  "test_control_point": {
    "name": "Eisenhower St. housing block",
    "district": "Watson",
    "sub_district": "Kabuki",
    "x": -1111.469,
    "y": 2146.427,
    "z": 12.157,
    "source": "data/sites/sites.json site 395 sts_wat_kab_05",
    "confidence": "game-data+wiki"
  },
  "control_points": [
    {
      "rank": 1,
      "name": "The Scraper",
      "type": "abandoned_hotel_hideout",
      "relevance": 5,
      "district": "Pacifica",
      "sub_district": "Dogtown",
      "x": -2465.287,
      "y": -2713.544,
      "z": 21.82,
      "source": "data/sites/sites.json site 357 sts_ep1_04",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["cyberware", "arms", "mercenary"],
      "nearest_cc_code": "cc_wwd_highway_gate",
      "nearest_cc_m": 170.1
    },
    {
      "rank": 2,
      "name": "Electric Corporation Power Plant",
      "type": "power_plant_xbd_studio",
      "relevance": 4,
      "district": "Westbrook",
      "sub_district": "CharterHill",
      "x": 31.935,
      "y": -510.77,
      "z": 1.304,
      "source": "dist/extract/areas.jsonl {q105_com_braindance_combat_floor_}0",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["braindance", "cyberware"],
      "nearest_cc_code": "cc_hil_le_le_park",
      "nearest_cc_m": 245.2
    },
    {
      "rank": 3,
      "name": "Digimmortal",
      "type": "exposition_hall_den",
      "relevance": 4,
      "district": "Pacifica",
      "sub_district": "Dogtown",
      "x": -2347.55,
      "y": -3063.5,
      "z": 129.54,
      "source": "dist/extract/areas.jsonl {mq306_com_scavengers}",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["cyberware", "mercenary"],
      "nearest_cc_code": "cc_wwd_highway_gate",
      "nearest_cc_m": 215.2
    },
    {
      "rank": 4,
      "name": "Organitopia",
      "type": "museum_den",
      "relevance": 4,
      "district": "Pacifica",
      "sub_district": "Dogtown",
      "x": -2227.138,
      "y": -3019.134,
      "z": 115.27,
      "source": "data/sites/sites.json site 360 sts_ep1_08",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["cyberware", "mercenary"],
      "nearest_cc_code": "cc_wwd_highway_gate",
      "nearest_cc_m": 274.0
    },
    {
      "rank": 5,
      "name": "Eden Beach Mega Ride",
      "type": "amusement_ride_den",
      "relevance": 4,
      "district": "Pacifica",
      "sub_district": "Coastview",
      "x": -2433.58,
      "y": -2199.374,
      "z": 15.98,
      "source": "data/sites/sites.json site 107 ma_pac_cvi_12",
      "confidence": "game-data+wiki",
      "interior": false,
      "revenue_streams": ["cyberware", "smuggling"],
      "nearest_cc_code": "cc_cvi_pacifica_pier",
      "nearest_cc_m": 48.1
    },
    {
      "rank": 6,
      "name": "Scavenger Den (Crescent St.)",
      "type": "apartment_den",
      "relevance": 4,
      "district": "Westbrook",
      "sub_district": "JapanTown",
      "x": -455.188,
      "y": 400.266,
      "z": 136.266,
      "source": "dist/extract/markers.jsonl mq036_sm_scavengers",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["cyberware", "sex_work", "braindance"],
      "nearest_cc_code": "cc_jpn_cherry_blossom",
      "nearest_cc_m": 140.4
    },
    {
      "rank": 7,
      "name": "Los Osos motel (West Wind Estate)",
      "type": "defunct_motel_den",
      "relevance": 3,
      "district": "Pacifica",
      "sub_district": "WestWindEstate",
      "x": -2554.542,
      "y": -2435.019,
      "z": 16.95,
      "source": "dist/extract/areas.jsonl {sts_ep1_03_combat_com} (site 356 anchor is 83 m off)",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["cyberware", "mercenary"],
      "nearest_cc_code": "cc_wwd_coastline_ruins",
      "nearest_cc_m": 22.4
    },
    {
      "rank": 8,
      "name": "ESC Explorer",
      "type": "expo_hall_smuggling_base",
      "relevance": 3,
      "district": "Pacifica",
      "sub_district": "Dogtown",
      "x": -2272.99,
      "y": -2947.7,
      "z": 111.47,
      "source": "dist/extract/areas.jsonl {we_ep1_17_com}",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["arms", "smuggling"],
      "nearest_cc_code": "cc_wwd_highway_gate",
      "nearest_cc_m": 202.8
    },
    {
      "rank": 9,
      "name": "Ross Street Parking Facility",
      "type": "parking_garage_den",
      "relevance": 3,
      "district": "Watson",
      "sub_district": "Northside",
      "x": -1734.613,
      "y": 2431.407,
      "z": 7.26,
      "source": "data/sites/sites.json site 215 ma_wat_nid_01",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["cyberware"],
      "nearest_cc_code": "cc_nid_totentanz_yard",
      "nearest_cc_m": 62.9
    },
    {
      "rank": 10,
      "name": "Illegal ripperdoc clinic (Offshore St.)",
      "type": "unlicensed_clinic",
      "relevance": 3,
      "district": "Watson",
      "sub_district": "Northside",
      "x": -1111.159,
      "y": 3318.479,
      "z": 8.531,
      "source": "data/sites/sites.json site 237 ma_wat_nid_27",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["cyberware"],
      "nearest_cc_code": "cc_nid_oil_refinery",
      "nearest_cc_m": 5.8
    },
    {
      "rank": 11,
      "name": "Opposites Attract rooftop outpost",
      "type": "rooftop_outpost",
      "relevance": 3,
      "district": "Watson",
      "sub_district": "LittleChina",
      "x": -1534.236,
      "y": 1818.981,
      "z": 32.38,
      "source": "data/sites/sites.json site 192 ma_wat_lch_01",
      "confidence": "game-data+wiki",
      "interior": false,
      "revenue_streams": ["cyberware", "mercenary"],
      "nearest_cc_code": "cc_lch_canal_overpass",
      "nearest_cc_m": 340.5
    },
    {
      "rank": 12,
      "name": "Eisenhower St. housing block",
      "type": "housing_block_chop_den",
      "relevance": 2,
      "district": "Watson",
      "sub_district": "Kabuki",
      "x": -1111.469,
      "y": 2146.427,
      "z": 12.157,
      "source": "data/sites/sites.json site 395 sts_wat_kab_05",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["cyberware", "sex_work", "braindance"],
      "nearest_cc_code": "cc_kab_pinewood_block",
      "nearest_cc_m": 162.6
    },
    {
      "rank": 13,
      "name": "Allen St. rooftop slums",
      "type": "rooftop_slum_den",
      "relevance": 2,
      "district": "Watson",
      "sub_district": "Kabuki",
      "x": -1097.405,
      "y": 1440.894,
      "z": 16.6,
      "source": "data/sites/sites.json site 399 sts_wat_kab_101",
      "confidence": "game-data+wiki",
      "interior": true,
      "revenue_streams": ["cyberware", "sex_work"],
      "nearest_cc_code": "cc_kab_allen_street",
      "nearest_cc_m": 107.7
    },
    {
      "rank": 14,
      "name": "Wild Blue bunkhouse",
      "type": "hotel_bunkhouse_den",
      "relevance": 2,
      "district": "Pacifica",
      "sub_district": "Coastview",
      "x": -1971.236,
      "y": -2165.879,
      "z": 24.839,
      "source": "data/sites/sites.json site 97 ma_pac_cvi_09",
      "confidence": "game-data+wiki+inferred",
      "interior": true,
      "revenue_streams": ["cyberware", "mercenary"],
      "nearest_cc_code": "cc_cvi_south_boulevard",
      "nearest_cc_m": 8.5
    },
    {
      "rank": 15,
      "name": "Pacific Blvd scav den",
      "type": "street_den",
      "relevance": 2,
      "district": "Pacifica",
      "sub_district": "WestWindEstate",
      "x": -2887.351,
      "y": -2153.889,
      "z": 1.32,
      "source": "data/sites/sites.json site 114 ma_pac_wwd_04",
      "confidence": "game-data+wiki",
      "interior": false,
      "revenue_streams": ["cyberware", "mercenary"],
      "nearest_cc_code": "cc_wwd_apartments_north",
      "nearest_cc_m": 9.5
    },
    {
      "rank": 16,
      "name": "Badlands harvesting warehouse",
      "type": "warehouse_den",
      "relevance": 2,
      "district": "Badlands",
      "sub_district": "Badlands",
      "x": 1056.978,
      "y": -714.063,
      "z": 22.271,
      "source": "data/sites/sites.json site 1 ma_bls_ina_01",
      "confidence": "game-data+inferred",
      "interior": true,
      "revenue_streams": ["cyberware", "vehicles_chop"],
      "nearest_cc_code": "cc_rcr_tama_viewpoint",
      "nearest_cc_m": 146.2
    }
  ],
  "subdistrict_counts": {
    "Dogtown": {"named": 4, "filler": 1},
    "Coastview": {"named": 2, "filler": 1},
    "WestWindEstate": {"named": 2, "filler": 1},
    "JapanTown": {"named": 1, "filler": 2},
    "CharterHill": {"named": 1, "filler": 0},
    "Kabuki": {"named": 2, "filler": 2},
    "Northside": {"named": 2, "filler": 0},
    "LittleChina": {"named": 1, "filler": 1},
    "Badlands": {"named": 1, "filler": 0},
    "Wellsprings": {"named": 0, "filler": 1},
    "Downtown": {"named": 0, "filler": 1}
  }
}
```
