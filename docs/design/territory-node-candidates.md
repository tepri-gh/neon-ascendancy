# Territory Node Candidates (Superseded)

> **Superseded (2026-11-28):** Replaced by [`venue-classification.md`](venue-classification.md),
> [`data/venues/classification.json`](../../data/venues/classification.json), and
> [`node-garrison-and-assault.md`](node-garrison-and-assault.md). Kept only as
> historical reference for pending open-world HQ sites not yet in
> `data/venues/approved/` (Militech Offices, Kang Tao Building, Biotechnica
> Protein Flats, Petrochem North Sunrise Oil Fields, NCPD Little China
> Precinct). Do not use this file's retired scale names, `culture` node type,
> or old Tyger Claws HQ pick (Clouds → now **Ho-Oh**).

Status: historical draft, 2026-11-26. A shortlist of venues likely to become territory
nodes (see [`territory-data-model.md`](territory-data-model.md) for scale and
type). Sources: the per-faction research in
[`../research/factions/`](../research/factions/) (each faction's "Priority
list of control points"), the venue research waves
([`../venue-playbook.md`](../venue-playbook.md) section 6), and the venue
catalogue's count of each faction's fighters per venue.

**Rules applied**
- **Fixers are never nodes** (owner 2026-11-26): fixer places stay venues,
  neutral, uncapturable. Struck through below.
- **One HQ (scale 5) per territorial faction**, as in
  `tools/generate-world-seeds.py` `FACTION_HEADQUARTERS`.
- Scales are suggestions: hangout 1, outpost 2, landmark 3, stronghold 3–4,
  business 3–4, HQ 5. Types: economy, technology, military, espionage,
  culture.
- **Status** is the venue work: `hand-built` and `approved` venues are
  populated in the clean slate; `pending` means not researched yet; `—`
  means no catalogue venue (open-world site only).

## Test control points

One active control point per faction stays for testing the sim until the
node list replaces it (`ACTIVE_TEST_CONTROL_CENTERS` and `LORE_TEST_POINTS`
in `tools/generate-world-seeds.py`). Owner 2026-11-26: move rather than
remove. Two sat on fixer places and moved:
- **Barghest**: Heavy Hearts (Mr. Hands) moved to the **EBM Petrochem
  Stadium market**.
- **Aldecaldos**: DaKota (Dakota Smith) moved to the **Mobile Camp**, the
  clan's only other base in the zone.

**Tyger Claws #4, Wakako's pachinko parlour**, and **Valentinos #9,
Padre's Glen corner**, are fixer places and drop out of the candidates.

## Tyger Claws (HQ: Clouds)

| Candidate | Sub-district | Scale / type | Why | Status |
| --- | --- | --- | --- | --- |
| Clouds | JapanTown | HQ 5 / economy+culture | Flagship dollhouse; management floors; canon seat | hand-built + additions |
| Jig-Jig Street | JapanTown | business 4 / economy | The red-light economy itself; Mox pressure makes it contested | approved |
| Ho-Oh | Kabuki | business 4 / economy | Owned casino/club/XBD studio; 3 floors, guards | hand-built (`sts_wat_kab_07`) |
| Kabuki Market | Kabuki | business 3 / economy | Black-market retail + protection racket | pending |
| Deravaja Dojo | LittleChina | stronghold 3 / military | Recruitment, fight betting, basement ring | pending |
| Tyger Claws Casino | CharterHill | business 3 / economy | Hidden gambling den in a rival district | pending |
| Chram Denya Jinja | NorthOaks | landmark 3 / culture | Ceremonial meeting ground; prestige seat | pending |
| ~~Wakako's pachinko parlour~~ | JapanTown | — | Fixer (Wakako) | — |

## Valentinos (HQ: La Catrina)

| Candidate | Sub-district | Scale / type | Why | Status |
| --- | --- | --- | --- | --- |
| La Catrina | VistaDelRey | HQ 5 / economy+military | Funeral-home front; arms, drugs, body logistics | pending |
| Mercado Sonora | VistaDelRey | business 3 / economy | Barrio market and meeting hub | pending |
| Dicky Twister | VistaDelRey | business 3 / culture | Valentino-owned club with office and backstage | pending |
| El Coyote Cojo | Glen | landmark 3 / culture | Community heart; legitimacy anchor (owner's example) | approved |
| Valentino Alley | Glen | hangout 2 / culture | Gang shrine corner with named bosses | pending |
| El Pinche Pollo | Glen | business 3 / economy | Restaurant with gang-only floor and office | pending |
| Valentinos Auto Shop | Wellsprings | business 3 / economy | Chop shop / weapon mods (owner's chop-shop example) | pending |
| Bus Depot | Wellsprings | stronghold 3 / military | Arms staging base, largest garrison | pending |
| ~~Padre's Glen corner~~ | Glen | — | Fixer (Padre) | — |

## Maelstrom (HQ: Totentanz)

| Candidate | Sub-district | Scale / type | Why | Status |
| --- | --- | --- | --- | --- |
| Totentanz | Northside | HQ 5 / culture+military | Canon HQ club | hand-built + additions |
| All Foods Plant | Northside | stronghold 4 / military | Main hideout: production floor, lab, cells | hand-built (`q003_meat_factory`) |
| HeavenMed | Northside | business 3 / technology | Chrome clinic on the payroll; the gang's cyberware line | pending |
| Wicked Tires Autoshop | Northside | business 3 / economy | Their only chop shop | pending |
| Ebunike Docks | Northside | outpost 2 / economy | Smuggling gateway | pending |
| Maelstrom Warehouse (Industrial & Eisenhower) | Northside | outpost 2 / military | Torture den and stash | pending |

## 6th Street (HQ: Megabuilding H6 hideout)

| Candidate | Sub-district | Scale / type | Why | Status |
| --- | --- | --- | --- | --- |
| H6 hideout | Arroyo | HQ 5 / military | Largest garrison; office, lab, netrunner den | pending |
| Dewdrop Inn | Arroyo | business 3 / economy | 6th-owned motel + drug lab front | pending |
| Red White Used Warehouse | Arroyo | outpost 2 / espionage | Netrunner den, hot-cargo stash | pending |
| Wicked Tires Autoshop (Glen) | Glen | business 3 / economy | Named 6th autoshop; vehicle economy | pending |
| Red Dirt Bar | Arroyo | landmark 3 / culture | Iconic Arroyo crossroads bar | pending |
| Kendal Park | RanchoCoronado | hangout 2 / culture | Neighbourhood showpiece contested with the Tygers | pending |

## Animals (HQ: Grand Imperial Mall)

| Candidate | Sub-district | Scale / type | Why | Status |
| --- | --- | --- | --- | --- |
| Grand Imperial Mall | Coastview | HQ 5 / military | Sasquatch's base; gym and ring | approved |
| Tripple Extreme Gym | Arroyo | business 3 / culture | Only Animals-owned freehold with a named owner | approved |
| Unfinished NCART Station | Coastview | stronghold 3 / military | Largest garrison; contraband stash | pending |
| 7th Hell | Downtown | business 3 / economy | Two-floor nightclub; protection economy | pending |
| Empathy | Downtown | business 3 / economy | BD strip club with a control room | approved |

## Voodoo Boys (HQ: Batty's Hotel)

| Candidate | Sub-district | Scale / type | Why | Status |
| --- | --- | --- | --- | --- |
| Batty's Hotel / netrunners' den | Coastview | HQ 5 / espionage | Canon Coastview HQ; Placide's office; Brigitte's den | hand-built + approved |
| Old Maglev Tunnel (Elders' lair) | Coastview | stronghold 4 / espionage | The data fortress, their crown jewel | approved |
| Pacifica Serenity Bible Church | Coastview | landmark 3 / culture | Public face and community seat | approved |
| Eventide Resort & Spa | Dogtown | stronghold 3 / espionage | Slider's den (alive in our timeline) | approved |
| Luxor High Wellness Spa | Dogtown | business 3 / economy | Extortion and implant economy; 33 units | pending |
| Rolland's Butcher Shop | Coastview | hangout 2 / economy | Placide's retail front | approved |

## The Mox (HQ: Lizzie's Bar)

| Candidate | Sub-district | Scale / type | Why | Status |
| --- | --- | --- | --- | --- |
| Lizzie's Bar | Kabuki | HQ 5 / culture+economy | Canon HQ; the only staffed Mox interior | approved |
| Autowerks | Northside | business 3 / economy | Mox workshop + yard | pending |
| Jig-Jig Street (Mox beat) | JapanTown | — | Presence on Tyger turf, not a node | — |

## Wraiths (HQ: Corp-Bud Cement Factory)

| Candidate | Sub-district | Scale / type | Why | Status |
| --- | --- | --- | --- | --- |
| Corp-Bud Cement Factory (Raffen Shiv camp) | Badlands | HQ 5 / military | Walled stronghold, prison, chop room | approved |
| Corp-Bud Mine | Badlands | stronghold 3 / military | Nash's stronghold | approved |
| Union Railroad Station | Badlands | outpost 2 / espionage | Drone-hijack antenna, turrets | approved |
| New American Autoworks | Badlands | business 3 / economy | Chop shop interior (owner's example type) | pending |
| Sequoia & Gray outpost | RanchoCoronado | outpost 2 / military | Their foothold inside the city | pending |
| Rocky Ridge | Badlands | hangout 2 / culture | Bar + fuel-station lookout | approved |

## Aldecaldos (HQ: Mobile Camp)

| Candidate | Sub-district | Scale / type | Why | Status |
| --- | --- | --- | --- | --- |
| Mobile Camp | Badlands | HQ 5 / military+economy | Clan home, vendors, convoy staging; Panam, Saul | approved |
| Marianne's garage (sq024) | Arroyo | outpost 2 / economy | Aldecaldo mechanic workshop in the city | wave 4 |
| ~~DaKota~~ | Badlands | — | Fixer (Dakota Smith) | — |

## Arasaka (HQ: Arasaka Tower)

| Candidate | Sub-district | Scale / type | Why | Status |
| --- | --- | --- | --- | --- |
| Arasaka Tower | CorpoPlaza | HQ 5 / all | Canon HQ | hand-built + additions |
| Konpeki Plaza | ArasakaWaterfront | business 4 / economy | Iconic hotel, elite clientele | hand-built |
| Arasaka Industrial Park | Arroyo | stronghold 4 / military | Largest supply depot | approved |
| Arasaka Estate | NorthOaks | landmark 3 / culture | Family seat; prestige | approved |
| Waterfront Freight Terminal | ArasakaWaterfront | business 3 / economy | Logistics hub | — |
| Charter Hill Substation | CharterHill | outpost 2 / technology | Current test control point | — |

## Militech (HQ: Militech Offices)

| Candidate | Sub-district | Scale / type | Why | Status |
| --- | --- | --- | --- | --- |
| Militech Offices | CorpoPlaza | HQ 5 / military | Regional HQ facing the Tower | pending |
| Sunshine Motel outpost | Badlands | stronghold 3 / technology | Radar-prototype R&D, 19 units | pending |
| Militech Detention Center | Badlands | stronghold 3 / military | Prison with refugees | pending |
| SoCal Border Crossing | Badlands | business 3 / economy | Customs at the NUSA border (NUSA tie-in) | approved |
| Maglev tunnel construction site | Badlands | outpost 2 / technology | Ongoing project with Militech crew | approved |
| Gold Beach Marina | Downtown | business 3 / economy | Elite waterfront security contract | pending |

## Kang Tao, Biotechnica, Petrochem

| Faction | Candidate | Scale / type | Why | Status |
| --- | --- | --- | --- | --- |
| Kang Tao | Kang Tao Building (HQ) | HQ 5 / technology | The only canon address | pending |
| Kang Tao | SovOil Fuel Station | outpost 2 / economy | Largest Kang Tao concentration | pending |
| Kang Tao | Hanford Overpass | outpost 2 / military | Androids, patrols | — |
| Biotechnica | Protein Flats (HQ) | HQ 5 / economy | The city's protein supply | pending |
| Biotechnica | Biotechnica Hotel | business 3 / economy | Current test control point | pending |
| Biotechnica | All Foods plant | — | Contested with Maelstrom; Maelstrom node | hand-built |
| Petrochem | North Sunrise Oil Fields (HQ) | HQ 5 / economy | Canon oil asset | pending |
| Petrochem | Fuel Station (I-9) | business 3 / economy | Current test control point | pending |

## Barghest (HQ: Black Sapphire)

| Candidate | Sub-district | Scale / type | Why | Status |
| --- | --- | --- | --- | --- |
| Black Sapphire | Dogtown | HQ 5 / military+economy | Hansen's tower; floor-99 club | hand-built |
| EBM Petrochem Stadium market | Dogtown | business 4 / economy | Black market, cash engine; guards verified neutral | approved |
| Nighthawks Rehab Center (Hansen Arms) | Dogtown | stronghold 3 / technology | Their own arms factory | pending |
| The Tunnel | Dogtown | outpost 2 / economy | Smuggling artery | — |
| Dogtown west gate | Dogtown | outpost 2 / military | Customs and extortion checkpoint | — |
| Spider-tank arena (q302) | Dogtown | stronghold 3 / military | 45 Barghest; armoured staging | wave 4 |
| ~~Heavy Hearts~~ | Dogtown | — | Fixer (Mr. Hands); approved as a venue only | approved |

## NCPD and Scavs

| Faction | Candidate | Scale / type | Why | Status |
| --- | --- | --- | --- | --- |
| NCPD | Little China Precinct | stronghold 4 / military | The only built precinct | pending |
| NCPD | Night City Prison | stronghold 3 / military | The only real garrison | pending |
| NCPD | NCPD Lab | business 3 / technology | Forensic monopoly | pending |
| Scavs | The Scraper | stronghold 3 / military | Placeholder Scav seat; lift, armory, prison | pending |
| Scavs | Electric Corporation Power Plant | stronghold 3 / technology | XBD base, three sub-levels | pending |
| Scavs | Digimmortal / Organitopia | outpost 2 / economy | Dogtown expo dens | pending |

## From the hustle research (owner pick pending)

The hustle pass (2026-11-26, `data/venues/hustle_sites.json`) classified
all 333 NCPD scanner sites: 162 reported crime (many are loot-only
caches), 93 assault in progress, 13 organized crime, 13 cyberpsycho and 44
other (Hidden Gems, cut content, story scenes). These are the sites the
agents judged node-worthy, ranked best first within each group. The design
behind them is `hustle-sites.md`. Pick the ones you want; the rest become
encounter data.

**Strongest (real organised operations)**

| Site | Holder | What it is | Note |
| --- | --- | --- | --- |
| `wbr_jpn_20` Willow St, Japantown | Tyger Claws | Fenced trafficking and forced-labour outpost, named boss, netrunner, 13 captives | Clear of every venue |
| `std_arr_03` Hargreaves St, Arroyo | 6th Street | Darius Miles's drug lab, 10 fighters, a five-car reinforcement, miniboss | Canon organized crime |
| `std_rcr_08` Rancho Coronado | 6th Street | Drug production station with four captive NCPD officers | 15 m from control centre `cc_rcr_almunecar_strip` |
| `wat_nid_02` Northside | Maelstrom | Outpost with boss, netrunner, two androids, drug and chemical stash | |
| `wat_lch_08` Drake & Cartwright, Little China | Tyger Claws | Extortion market corner, 12 Claws, netrunner, 16 cameras | Protection racket |
| `wat_lch_01` Little China rooftop | Scavengers | Fortified illegal cyberware trade, netrunner and sniper | |
| `bls_ina_se1_17` I-9, Badlands | Wraiths | Outpost with named leader Bruce Ward, nine hostiles | |

**Chop shops and arms caches (economy)**

| Site | Holder | What it is | Note |
| --- | --- | --- | --- |
| `cct_dtn_12` Corpo Plaza garage | Scavs (corporate guard) | Chop shop in a parking garage: lift, stripped cars, netrunner, two androids | |
| `bls_ina_se5_09` Badlands | none (turrets, mines) | Defended wrecker and salvage yard | Unoccupied; a garrison would be invented |
| `bls_ina_se5_14` Badlands | Wraiths | Roadside garage front with a trapped car lift, Aldecaldo hostage | |
| `hey_gle_109` the Glen | unknown | Arms lock-up: LMG, grenades, shard case | Holder not in the data |
| `hey_gle_105` behind Megabuilding H1 | unknown | Small arms cache in a service row | Holder not in the data |
| `bls_ina_se1_19` Badlands ridge | Wraiths | Lookout over an arms cache, sniper | |
| `wat_nid_27` Northside | Scavengers | Stripping den by a body freezer | Weakest; confirm it is a place |

**Corporate posts (Militech, Kang Tao)**

| Site | Holder | What it is | Note |
| --- | --- | --- | --- |
| `bls_ina_se1_23` Badlands | Militech | Largest garrison in its group (10 and a drone), garage yard | |
| `bls_ina_se1_05` Badlands | Militech | Restricted roadside compound, drug stash | |
| `cct_dtn_15` Downtown | Militech | Fenced freight yard and guard post | |
| `wbr_hil_01` Charter Hill | Militech | Industrial black site, HMG gunner, sniper | 36 m from the approved Acorn Towers lot |
| `cct_cpz_16` Corpo Plaza roof | Kang Tao | Guarded rooftop cache, five caches | |

**Weaker or already covered**

- `std_rcr_18` Wraith trafficking yard: already the "Sequoia & Gray outpost"
  candidate, but its anchor sits at the Mallagra & Manzanita Depot control
  centre; one of the two positions is wrong.
- `std_rcr_05` Kendal Park: already a candidate.
- `wat_nid_06` Maelstrom outpost: may coincide with the approved North Kabuki
  ripperdoc lab; check in game.
- `wat_nid_01` Hobotown harvesting: strong operation, weak physical site.
- `std_arr_02` container-terminal arms handoff and `wat_kab_06`
  trafficking container: transfer points rather than held places.
- `bls_ina_se1_01` roadside organ harvesting: marginal.
- `mq304_ce` Barghest-held Dogtown block: a quest scene; the approved
  container-yard lanes venue may already cover it.

## Next

1. Owner: confirm or trim, and settle the two test-point conflicts.
2. Prioritise `pending` candidates in the next research waves; most are
   individual-tier venues already in the catalogue.
3. Feed confirmed nodes into `tools/generate-world-seeds.py` as the node
   seed list (influence and pillar output come from scale and type).
