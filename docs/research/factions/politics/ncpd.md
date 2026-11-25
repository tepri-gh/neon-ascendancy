# NCPD (incl. MaxTac) — Leadership, Internal Politics and External Relations

Status: faction research run, 2026-11-25. One document, one faction.
Scope: Cyberpunk 2077 2.5 + Phantom Liberty, campaign disabled, alternate timeline
(`gameplay-systems.md` §7). Who a player can join under, climb past, ally with or
remove in the NCPD and MaxTac; the blocs; the relations matrix.

Method: [`METHOD.md`](./METHOD.md) incl. §1.1–§1.3, plus [`../METHOD.md`](../METHOD.md).
Locations live in [`../ncpd.md`](../ncpd.md) and are not repeated. `AGENTS.md` read
first. No commits, no game launch; helper scripts ran outside the repo under
`python3 -I`.

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/comic/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My reasoning links a person, place or stance to a record | Weak, flagged |

Conventions: **presence class** per METHOD §1.2 item 2 (`ambient`,
`world-activity`, `story`, `prologue`, `off-map`, `mentioned`, `historical`; JSON
`open_world` true only for the first two). **Rank is inferred from role text** — the
game has no rank field. **Not a turf faction:** zero sub-territories, 91 roster units
across 22 sites, one real garrison (Night City Prison, `mq062_*`), and no offline
attitude matrix — every stance in §3 is judged, not read.

---

## 1. Leadership and ranks

### 1.1 The 2077 chain of command

A municipal department under the **Government of Night City**: the mayor appoints
and removes the commissioner, who runs the divisions, which are organised into
precincts. `[wiki]` The top is thin, and the one figure who matters politically —
the commissioner — is never spawned.

| Name | Role | Record | Class | Source | Conf. |
| --- | --- | --- | --- | --- | --- |
| **Jerry Fawlter** | Commissioner from 2076; ex-dataterm sales head; mayor's appointee; corrupt | none | `mentioned` | Wiki *Fawlter*, *NCPD*; `You Know My Name`; `06_ncpd_chief` → `Character.q303_paradise_ncpd_chief` `[inferred]` | `[wiki]` `[game-data]` |
| **Claudia Feldman** | Deputy Commissioner; disbanded the Pacifica precinct, 17 Oct 2072 | none | `mentioned` | Wiki *Feldman*; shard *Pacifica Precinct Restructuring* | `[wiki]` |
| **Commissioner Ramos** | Commissioner to 2071; ordered the Pacifica withdrawal | none | `historical` | Wiki *Ramos*; *2077SC* | `[wiki]` `[lore]` |
| **Coleridge** | Commissioner in an N54 report after *The Pickup* | none | `mentioned` | Wiki *Members* | `[wiki]` |
| **Det. River Ward** | Homicide; suspended for re-opening the Rhyne inquest; *I Fought the Law*, *The Hunt* | `Character.Sobchak` (13 phases); `Character.sq029_sobchak_vr` | `world-activity` | Registry `sobchak`, `river_holo`; wiki *Ward* | `[game-data]` `[wiki]` |
| **Det. Harold Han** | Ward's partner; executed Holt's Rhyne cover-up | none found | `story` | Wiki *Han*; *I Fought the Law* | `[wiki]` |
| **Det. Gonaghal** | "Peter Pan" abductions; called lazy by Ward | none | `mentioned` | Wiki *Members*; *The Hunt* | `[wiki]` |
| **Insp. Henry Stints** | Heywood inspector; Streetkid arresting officer; drops a case on a corpo's word | `Character.q000_kid_parking_stints` (`officer4`) | `prologue` | Registry `officer4`; wiki *Stints* | `[game-data]` `[wiki]` |
| **Sgt. Aaron McCarlson** | Corrupt sergeant; had a lover shot; bought the footage | none | `world-activity` | Wiki *McCarlson*; *Scrolls Before Swine* | `[wiki]` `[game-data]` |
| **Sgt. Anna Hamill** | Honest undercover officer; killed her corrupt colleagues | none (`dd_annaHamillKid` = her children) | `world-activity` | Wiki *Hamill*; registry `anna_hamill_child_01/02` | `[wiki]` `[game-data]` |
| **Capt. Robert Kowalsky** | Hamill's superior; paid a fixer to silence her | none | `mentioned` | Wiki *Members*; *Hamill/Kowalsky* shard | `[wiki]` |
| **Sgt. Jasmine Dixon** | 2061 veteran; committed for reporting corruption | none | `world-activity` | Wiki *Dixon*; *Cuckoo's Nest* | `[wiki]` |
| **Lt. Sara Krakosky** | Department spokesperson | none | `mentioned` | Wiki *Members* | `[wiki]` |
| **Lt. Melissa Rory** | MaxTac SPAR lieutenant; reconditioned cyberpsycho | `Character.mq030_melisa` | `world-activity` | Registry `mq030_melisa`; wiki *Rory*; *Bullets* | `[game-data]` `[wiki]` |

- **Fawlter is reformer, destroyer and criminal in one office.** Fired half the
  force, cut patrols, ordered tickets over cases, charged 5€$/min for 911, ran
  drones-for-cops; conspired with Maelstrom to ambush officer Reggie Loeb; organised
  a homeless clearance with a Scavenger; dealt with a 6th Street officer at the
  Sapphire. `[wiki]`
- **Ward's record is `Character.Sobchak`; no `Character.River*` exists** (13-phase
  River set, `river_holo` → same record, VR variant). **Han has no record** — eight
  named 2077 figures (Han, Gonaghal, Kowalsky, Krakosky, McCarlson, Hamill, Dixon,
  Coleridge) have zero `Character.*` records. `[game-data]`
- **"Han Dao Tzu" does not exist.** Wiki `insource`, an all-pages prefix scan and a
  registry scan for `tzu`/`dao`/`han_dao` return only **Dao Hyunh** (a cyberpsycho
  actor in *Seaside Cafe*) and **Harold Han**. Do not seed it.

### 1.2 Succession history

Appointment plus catastrophe: the commissioner is a mayoral appointment, and the
department's history is a sequence of losses. Founded 1994; nearly extinguished by
the Fourth Corporate War and the Holocaust (Hammerman's MaxTac was briefly the only
policing in the city); **Ramos** (to 2070) withdrew from Pacifica rather than fight;
**Deputy Commissioner Feldman**, with Mayor Rhyne, disbanded the Coastview precinct
on 17 Oct 2072 and lost the district; **2076** brought privatisation, Rhyne calling
the force "not profitable" and installing **Fawlter**; in **2077** an N54 report
names a second commissioner, **Coleridge** (§5), while Acting Mayor **Holt** used the
police to cover up Rhyne's death. `[wiki]`

**No internal ladder to commissioner** — every holder was appointed from outside the
command track or elevated by a patron. **The big events are losses** (Pacifica 2072,
Dogtown walled off, Badlands unpatrolled). **MaxTac's succession is separate and
older:** Hammerman took it *out* of the NCPD and ran it on contracts.

### 1.3 Rank structure, entry and advancement

Divisions `[wiki]`: Patrol (beat pairs, traffic as punishment, cruiser, airborne);
Investigation (vice, robbery, homicide, S.IN.); Tactical (SWAT, MaxTac, riot);
NetSec; Internal Affairs; Administration.

Ranks, attested in 2077 text: **commissioner** (Ramos, Fawlter, Coleridge — mayoral
appointment, never internal) and **deputy commissioner** (Teal, Feldman); **captain**
(Kowalsky, precinct or division command); **lieutenant** (Krakosky, Rory, Brasso in
RED — unit command or a public-facing role); **sergeant** (McCarlson, Hamill, Dixon,
Hammerman in 2020 — squad supervision and corruption's usual home); **inspector**
(Stints); **detective** (Ward, Han, Gonaghal, Escobar in RED — plain clothes, reached
from patrol); and **officer/cadet** (entry). The roster's `constable`, `corporal`,
`enforcer`, `hazmat` and `investigator` are enemy specialisations, not rungs.
`[wiki]` `[game-data]`

**Advancement is political.** McCarlson "slept his way up the NCPD ladder"; Hamill
was honest and her captain paid to have her killed. **Loyalty to the precinct's
arrangements beats casework**; being right is a career risk (Ward suspended, Dixon
committed), and traffic/administration is the punishment posting. `[wiki]` For the
mod: score advancement on clearance rates that do not embarrass a patron, willingness
to bury the right case, and visible public credit (PR is a funding lever). Honest
casework should raise public standing and lower internal standing at once.
`[inferred]`

### 1.4 The roster and the people it does not contain

`rosters.json` holds **91 NCPD units across 22 sites / 46 records**, and **not one is
a named person** — all `ncpd_police_*`, `ncpd_inspector_*`, `ncpd_constable_*`,
`ncpd_hazmat_*`, `ncpd_enforcer_*` plus geocode costumes (`gle_`, `nid_`, `jpn_`,
`cpz_`, …). The geocode is the costume, not the station: `nid_ncpd_*` constables
appear in JapanTown. `[game-data]` The remaining named people are **Barry Lewis**
(ex-cop, `Character.mq010_barry`, `world-activity`), **Nadia Petrova / Juan Mendez**
(patrol partners, `story`), **Ayden Daniels** (bribed, evidence-fabricating officer,
`world-activity`), **Felipe Alva / Mark Winston** (undercover officer and handler),
**David Beemer / Wesley Avedon** (immigrant names, blackmail) and **Reggie Loeb**
(ambushed at Fawlter's request) — the last four `mentioned`. Cautions:
`mq030_max_tac_1…9` are squad actors, not Rory (four combat, five `no_combat`);
`officer4` is the only named parking officer; `barry` is a *former* cop.
`[game-data]`

### 1.5 MaxTac's command

Formally `affiliations = NCPD`, functionally separate. SPAR (Special Purpose Assault
Rescue) teams are the unit: four operators in 2077 (Assault, Mantis, Heavy,
Netrunner, plus Snipers), six-plus-officer in 2020; a lieutenant commands a team.
`[wiki]` `[game-data]`

| Name | Role | Record | Class |
| --- | --- | --- | --- |
| **Melissa Rory** | Lieutenant; SPAR commander; the only named 2077 MaxTac officer | `Character.mq030_melisa` | `world-activity` |
| Max Hammerman | Sergeant/Commander 2020–2045; seceded, then reincorporated | none | `historical` |
| Ares | Squad leader 2010–2020; captured cyberpsycho, reconditioned into command | none | `historical` |
| Bubba McCarty; Garrison | SPAR lieutenants, 2020 | none | `historical` |
| Mason; Hook | SPAR Delta commander, killed; his replacement | none | `mentioned` |
| Russo, Peterson, Foster, Collins | The `q305` convoy squad (Assault, Mantis, Heavy, Netrunner) | none by name | `story` |

**No 2077 commander above lieutenant exists.** Its own entry calls it "a state within
a state": other divisions keep it at arm's length, "any internal investigations are
sure to be dropped", and its officers are "chromed-out loners". It is the one NCPD
unit allowed in Dogtown, and it recruits its own targets (Ares, Rory). `[wiki]`

### 1.6 What the game actually spawns (campaign disabled)

Nothing above a lieutenant. **`ambient`:** only the `cs_*` layer — `cs_patrol_*`
(15 areas / 30 records), dragnets, highway patrol, crime scenes, `cs_heavy_*` — and
the prison garrison (`mq062_*`: 6 areas / 28 records / 19 named slots), which is
quest-authored and may despawn; **no named officer.** **`world-activity`:** Ward
(`sq012_*`, `sq021_*`), Rory (`mq030_melisa`), Barry (`mq010_barry`) and the gigs where
the NCPD are the enemy (*Scrolls Before Swine*, *Cuckoo's Nest*, *Clampdown*, *The
Hunt*) — all side-job gated, per METHOD §1.2 item 2. **`prologue`:** Stints in the
Streetkid opening (`q000_parking_*`) — the best "working cop" scene in the game is a
scene *with* cops. **`story`:** Han (no record) and Ward's Phantom Liberty variants. **`mentioned`:** Fawlter, Feldman,
Coleridge, Ramos, Gonaghal, Kowalsky, Krakosky, McCarlson, Hamill, Dixon, Daniels.
`[game-data]` `[wiki]` **The highest-ranked named NCPD person in free roam is a
MaxTac *lieutenant* (Rory); the next is a *detective* (Ward). Every commissioner,
deputy, captain and spokesperson is `mentioned`-only — a simulation agent the mod must
supply.** `[inferred]`

### 1.7 Player-path hooks

| Person | Join under | Climb past | Ally with | Remove |
| --- | --- | --- | --- | --- |
| Fawlter | Tickets, drones, prison contracts, 911 fees | No internal ladder; become the mayor's next appointee | Night Corp, the corps buying his blind eye, Maelstrom/Scav intermediaries | A mayoral act or a fixer-delivered scandal, not an assassination |
| Ward | Homicide, casework, the lab, the inquest | His ceiling is detective; promotion is what he refuses | Regina, the Peralezes, the media | Suspending or killing him removes the only clean-cop protagonist |
| Han | Follow orders, bury the case, keep the pension | Loyalty over partnership | Holt's office | Exposing him decapitates the cover-up and Holt's acting mayoralty |
| Stints | A normal patrol shift; selective enforcement | The anti-ladder: let the right person go | Arasaka (Fujioka), the Heywood network | Only NCPD officer reachable pre-campaign |
| McCarlson | Buy footage, sell favours, consult for fixers | Already influential; climb by becoming his fixer | Regina, Valentinos (Moreno), Maelstrom (CCTV) | Regina can blackmail him into an asset or kill him |
| Hamill | Honest undercover work in Kabuki | Her captain is the ceiling, and the ceiling hired a hit | Regina, the honest remnant, the Aldecaldos later | Kowalsky pays for her death; saving her creates a martyr |
| Dixon | Reporting the wrong thing | Reporting is the anti-ladder | Muamar (who brokers the escape) | Proof that corruption punishes reporting, not crime |
| Rory | MaxTac: SPAR, hunts, no questions | No named commander above her | MaxTac, whoever signs for prototypes | Removes the only named MaxTac leader |
| Daniels | Fabricate what courts need, sell what the budget needs | A source, not a ladder | Muamar, the Santo Domingo networks | The model for a "bought but functional" cop to keep |

**Two ladders, one goes up.** The public ladder is gated on selective enforcement;
the clean ladder ends in suspension, a hit contract or a psych ward. To *run* the
NCPD a player must buy the mayor's office: the commissioner is an appointee and the
department is privatised property. `[inferred]`

---

## 2. Internal political factions

### 2.1 The blocs

| Bloc | Leader(s) | Wants | Presence hint | Evidence |
| --- | --- | --- | --- | --- |
| **Commissioner's office (privatisation)** | Fawlter | Revenue, visibility, the mayor's favour; MaxTac protected because it "gains points for public relations" | HQ; the 2076 reorganisation; `06_ncpd_chief` at the Sapphire | *Anatomy of a Disaster*; wiki *Fawlter* |
| **Precinct machine (corrupt cops)** | Kowalsky, McCarlson, precinct captains | Keep the arrangement: smuggling, blind eyes, seized-goods resale, fixer fees | Named sergeants/captains; Hamill, McCarlson, Beemer, Loeb scandals | *Scrolls Before Swine*; *Hamill/Kowalsky* shard |
| **Clean cops (reform remnant)** | Ward, Hamill, Dixon | Do the job; the badge as a promise | Individuals with no institution; all punished | *I Fought the Law*, *The Hunt*, *Cuckoo's Nest* |
| **MaxTac (autonomous unit)** | Rory; SPAR lieutenants | Prototypes, a free hand, no investigations | 4 operators at Tom's Diner; `mq030_max_tac_1…9`; `q305` convoy | *Bullets*; MaxTac entry; *Black Steel* |
| **Internal Affairs** | Unnamed | Investigate the others; survive being hated | A division only — no named 2077 officer | Wiki *NCPD* (IAD) |
| **Corp-bought liaison layer** | Unnamed; the commissioner | Keep Arasaka/Militech/Night Corp money flowing; keep corporate crime out of jurisdiction | No records; sponsorship and the Militech extraction | Database entry; *Extraction* |
| **Prison garrison** | Unnamed wardens | Custody, quiet, privatised-prison contracts | 28 records / 19 named slots — the only real garrison | `mq062_*`; *Clampdown* |

- **There is no police union in the sources** — no collective bargaining, no labour
  action, no union page. What exists is a privatised department and a 2076 mass
  redundancy. Model the labour interest as **the fired half**: a resentful pool of
  trained ex-officers, not an organisation. `[wiki]` `[inferred]`
- **MaxTac is a faction-within-a-faction** ("a state within a state"), not a bloc in a
  hierarchy: a vassal with independent foreign policy, per design §5. `[wiki]`

### 2.2 Clean cops, the precinct machine, and MaxTac

The machine is the institution — "an atmosphere of apathy and corruption pervades the
department", corporate crimes "are removed from police jurisdiction sooner or later"
— while the clean cops are individuals: Hamill is "a really bad fit for Night City",
Ward is suspended, Dixon is committed. Corruption is vertical, not conspiratorial: one
captain and one compliant sergeant per precinct (Kowalsky/Adams vs Hamill; Holt/Han vs
Ward). The clean cops' one institutional ally is the lab, where forensic truth lives
and which needs a budget line. `[wiki]` Simulation axis: **competence** (does the case
get solved) vs **loyalty** (does it stay buried). Both high = a stable precinct;
divergence produces a Hamill, a Ward or a whistleblower. `[inferred]`

**MaxTac is the exception to all of it.** Structural privileges ("their pick of
weapons, the best cyberware, fresh, prototype gear and a free hand" — Patrol buys its
own gear; the Centaur order is the belated correction), exemption from accountability
("any internal investigations are sure to be dropped", so IAD cannot touch it), a
history of secession (Hammerman took MAX-TAC away and ran it on city-wide contracts),
cross-jurisdiction rights (Dogtown, the Los Padres convoy), and recruitment from its
own targets (Ares, Rory) — "a fine, fading blur". `[wiki]` `[game-data]` It is a
**vassal with a private army and a separate foreign policy**: obedient while its
funding and impunity are protected, and a prepared internal war — the best the faction
offers — the moment a reform commissioner imposes IAD. `[inferred]`

### 2.3 Budget and the commissioner's war on his own department

Fawlter's moves and what each cost: **fired half the force** (a resentful ex-officer
pool, overextended survivors); **cut patrols** (response falls — the 15 `cs_patrol_*`
areas are the residue); **ordered tickets over cases** (fines become the only growth
line); **5€$/min for 911 calls** (the poor stop calling and intelligence dries up);
**drones-for-cops** — Wyvern, Bombus, Griffin, Robot R (bodies out, machines in);
**privatised-prison partnerships** (the prison becomes the only garrison and a contract
asset); **kept Night Corp sponsorship and Arasaka/Militech beholden** (corporate crimes
leave jurisdiction); and **protected MaxTac's funding for visibility** (the one unit
never cut is the one on the news). `[wiki]`

**The plan failed:** "no closer to becoming profitable"; capitalization fell 17%; the
Mayor's Office began considering **replacing the police with corporate security
firms**. The loop is fines → resentment → lower call volume → fewer solved cases →
lower capitalization → privatisation pressure → more fines. The `Economy` weakness is
not poverty; it is **a privatised monopoly that cannot price its own service**.
`[inferred]`

### 2.4 What could drive internal conflict in a simulation

Commissioner vs precincts (both extract from patrol, 58 of 91 roster units); MaxTac vs
Internal Affairs (impunity plus a precedent of secession); the clean cop as trigger
(backing one costs more loyalty than it gains competence); corporate jurisdiction
(every dropped corporate case is a favour banked and a detective lost); the
privatisation threat (a district policed by a corp is a precinct that loses its
revenue); the prison contract (the only growing line item and the only garrison); the
fired half (armed, trained, aggrieved, unorganised); and MaxTac's own cyberpsychosis
(Rory's record notes a relapse risk). `[inferred]`

---

## 3. External relations matrix

### 3.1 Stance vocabulary and direction

Read **from the NCPD's side**, precedence per METHOD §3: `war` / `hostile` / `rival`
(conflict, targeting, competition); `neutral` (no attested interaction); `trade` /
`ally` (transaction, coordination); `patron` / `client` (the NCPD protects or funds
the other / depends on or works for the other).

**`patron` is almost never right; `client` almost always is** — the NCPD protects
nobody; it is funded by Night Corp, sponsored by Arasaka and Militech, and hired by
the city. One stance per row also loses the defining "hostile with a bought channel"
structure, so the matrix assigns the dominant stance and puts the bought channel in
the evidence. `[inferred]`

### 3.2 The matrix

| Faction | Code | Stance | Evidence | Conf. |
| --- | --- | --- | --- | --- |
| Tyger Claws | `tyger_claws` | `hostile` | Two SOCAs, three Reported Crimes, multiple Assaults in Progress against Tyger crews `[game-data]`; **but** Hamill's captain and colleague paid Regina to silence her over a Kabuki smuggling ring tied to Jotaro Shobo, and the 2045 Kimen-Gumi "collaborat[ed] with the NCPD" `[wiki]` | `game-data+wiki` |
| Valentinos | `valentinos` | `hostile` | SOCA at Valentino Alley and Mercado Sonora; Assaults in Progress; Zoe Alonzo's record `[game-data]`; **but** Sgt. McCarlson helped Valentino Claudio Moreno murder his ex-superior and guaranteed "the police would not interfere"; Padre has informants in command `[wiki]` | `game-data+wiki` |
| Arasaka | `arasaka` | `client` | "Beholden to the interests of Arasaka and Militech"; corps "put their interests in the PD expecting something in return"; corporate crimes "removed from police jurisdiction sooner or later"; Stints orders V beaten on Arasaka exec Fujioka's word `[wiki]` | `wiki` |
| Militech | `militech` | `client` | The equipment supplier (Lexington, Saratoga, Ajax, Minotaur, Wyvern, Griffin, Centaur, Enforcer, Hellhound, Behemoth) and a creditor `[wiki]`; its Investigations Dept ran an extraction with NCPD approval and "no police intervention"; Coleridge held a joint press conference with Stout over a Centaur purchase `[wiki]` | `wiki` |
| Kang Tao | `kang_tao` | `neutral` | No attested interaction; Corpo Plaza is jointly patrolled with corporate security but no Kang Tao arrangement exists `[wiki]` `[inferred]` | `wiki+inferred` |
| Biotechnica | `biotechnica` | `neutral` | No interaction; Biotechnica's own order forbids sharing information with the NCPD — corporate policy, not a police relation `[wiki]` | `wiki+inferred` |
| Petrochem | `petrochem` | `neutral` | No interaction; two `cpz_ncpd_police` records at a Petrochem gas-station scanner site are response presence `[game-data]` | `game-data+inferred` |
| Barghest | `barghest` | `hostile` | "Forbidden to enter Dogtown proper"; the Pacifica precinct fell in 2072 after Barghest/VDB riots; Dodger holds two officers prisoner `[wiki]`; **but** Fawlter attends Hansen's gala and deals with a 6th Street officer there, and **MaxTac is the one unit allowed inside** `[wiki]` `[game-data]` | `game-data+wiki` |
| 6th Street | `sixth_street` | `hostile` | Founded to replace a corrupt NCPD; NCPD runs SOCA against Darius Miles and Olga Longmead `[game-data]` `[wiki]`; **but** Fawlter deals with a 6th Street officer at the Sapphire, and 6th Street fights beside the NCPD in the `q305` convoy ambush — the only attested joint operation `[wiki]` `[game-data]` | `game-data+wiki` |
| Aldecaldos | `aldecaldos` | `hostile` | *Fortunate Son*: NCPD ambush the pickup and try to kill V, unable to tell nomads from Raffen Shiv `[wiki]`; "cops don't like nomads" `[lore]`; **but** Hamill ends up with the Aldecaldos and Ward's sister married one `[wiki]` | `wiki+lore` |
| Wraiths | `wraiths` | `hostile` | Three SOCAs against named Wraith cells (Ward, Craven, McBride) with bounties naming each leader `[wiki]`; Assault-in-Progress and Reported Crime scenes across 16 highway communities `[game-data]` | `game-data+wiki` |
| Animals | `animals` | `hostile` | APB names Denzel Cryer's Juice ring; Assaults in Progress at Corpo Plaza, JapanTown, Little China, Coastview `[game-data]` `[wiki]`; **but** Holt hired the Animals to wreck the Red Queen's Race `[wiki]` | `game-data+wiki` |
| The Mox | `the_mox` | `neutral` | No raid, hustle or SOCA attested; Judy's NCPD call about Evelyn is brushed off (*Both Sides, Now*). Tolerance and neglect `[wiki]` | `wiki+inferred` |
| Maelstrom | `maelstrom` | `hostile` | MaxTac killed Hextra; Caliber possibly assassinated by NCPD/MaxTac; standing target of hustles and organised-crime activities `[wiki]` `[game-data]`; **but** Fawlter conspired with Maelstrom's Zaytsova to ambush officer Loeb, and McCarlson bought Maelstrom footage — a channel that reaches the commissioner `[wiki]` | `game-data+wiki` |
| Voodoo Boys | `voodoo_boys` | `hostile` | De facto law in western Pacifica; expelled an NCPD task force in 2072 `[wiki]`; VDB records appear in NCPD crime-scene and patrol areas `[game-data]` | `game-data+wiki` |
| Night Corp | `night_corp` | `client` | "Partly financed by Night Corp's shrinking coffers"; "the police force's official sponsor is Night Corp"; MaxTac's funding likewise `[wiki]`; the design also assigns Night Corp places to NCPD `[game-data]` | `wiki+game-data` |
| City Council | `city_council` | `client` | The Council grants its powers (year-long detention, limb shots as warning shots, firing on fleeing vehicles, unofficial collateral), legislates its remit, walled off Serenisands, and the mayor appoints/directs its commissioner `[wiki]` | `wiki` |
| Scavengers | `scavengers` | `hostile` | Standing target; APBs name Zbyszko, Kolev, Yelena, Barry; hustles at Ross Street, Eden Beach, West Wind, Northside, Coastview `[game-data]` `[wiki]`; **but** Fawlter hires Yelena Sidorova to clear the homeless and promises to ignore calls there `[wiki]` | `game-data+wiki` |
| Regina Jones | `fixer_regina` | `trade` | The most active counterpart: buys NCPD footage for McCarlson then blackmails him; Kowalsky and Adams paid her to have Hamill killed; McCarlson consulted on her show *Cops 'n' Chops* `[wiki]` | `wiki` |
| Wakako Okada | `fixer_wakako` | `trade` | *Clampdown* is a prison break whose enemies include the NCPD; she also brokers NCPD-adjacent data. Transactional `[wiki]` `[game-data]` | `wiki` |
| Sebastian Ibarra (Padre) | `fixer_padre` | `trade` | "Padre has informants in NCPD command"; his Heywood turf is the department's densest area by records `[wiki]` `[game-data]` | `wiki` |
| Muamar Reyes (El Capitán) | `fixer_el_capitan` | `trade` | "Not keen on NCPD… they do the people a disservice", yet works with them when it pays; his friend **Ayden Daniels** is a bribed, evidence-fabricating officer who has "worked closely with Muamar Reyes"; he brokers Dixon's escape `[wiki]` | `wiki` |
| Dakota Smith | `fixer_dakota` | `hostile` | *Fortunate Son* is her anti-NCPD Badlands gig: the ambush assumes Dakota is helping Raffen Shiv `[wiki]` `[game-data]` | `wiki` |
| Dino Dinovic | `fixer_dino` | `trade` | His bar hosts corrupt Sgt. McCarlson; he runs the two gigs that put the department's political masters in play (*Serial Suicide*, *Cole*). Bought, not hostile `[wiki]` `[game-data]` | `wiki` |
| Rogue Amendiares | `fixer_rogue` | `neutral` | No NCPD-specific gig or link; Afterlife is neutral ground `[inferred]` | `inferred` |
| Mr. Hands | `fixer_mr_hands` | `neutral` | His Dogtown work runs through Barghest and the FIA — the two bodies NCPD cannot act against; no NCPD channel `[wiki]` | `wiki+inferred` |
| Afterlife | `afterlife` | `neutral` | Neutral marketplace; NCPD hires mercs "on the sly" but no Afterlife-specific arrangement `[wiki]` | `inferred` |
| NUSA | `nusa` | `neutral` | The NUSA is the *city's* adversary, not the department's; the federal analogue is the FIA, aimed at Dogtown `[wiki]` | `wiki+inferred` |
| NetWatch | `netwatch` | `neutral` | No interaction; Night City has its own NetSec division, which is why it would not use NetWatch `[wiki]` | `wiki+inferred` |
| Zetatech | `zetatech` | `client` | Zetatech supplies the Bombus recon drones and the Atlus vehicle in the post-2076 inventory — both named in the drones-for-cops policy — so the department depends on Zetatech airframes as it does on Militech small arms `[wiki]` | `wiki` |
| Trauma Team | `trauma_team` | `trade` | Co-response and hand-off: *The Hunt* ends with Ward parting from Trauma Team; the `sq021` community mixes 7 NCPD officers with a Trauma Team actor and an AV `[game-data]` `[wiki]` | `game-data+wiki` |

**Counts (31 rows): hostile 11, neutral 9, trade 6, client 5; war/rival/ally/patron
0.** **No `ally`, no `patron` — and that is the finding:** nobody coordinates with the
NCPD out of loyalty and it funds no one; the nearest `ally` candidate, Trauma Team, is
a hand-off. **Symmetry conflict, flagged not smoothed:** `arasaka.md` and `militech.md`
read this pair as `trade` from *their* side; this doc reads `client` from *NCPD's*
side because the department is the dependent party (§5).

The three that matter most:

- **`night_corp` — `client`.** Night Corp pays the department and MaxTac. The
  sponsorship is the switch that turns the faction off: cheaper than any raid, and the
  two docs already agree on direction.
- **`city_council` — `client`.** The Council and mayor define powers, budget and remit.
  NCPD has no independent political existence, which makes it the natural target of the
  controller/title-holder split: a gang can *control* a precinct while the Council still
  *holds title*.
- **`barghest` — `hostile`.** The wall is the department's largest territorial defeat
  and its clearest boundary. Take Dogtown from Barghest and the NCPD gets its first
  territorial gain in five years; lose a precinct to Barghest and you reproduce
  Pacifica. Fawlter at the gala is why the row is not a simple war.

### 3.3 Guarantor assessment

**Worst ally, best silent partner.** No `ally`, no `patron`, `hostile` with eleven
factions, and redeployable at will by the Mayor's Office — the real appointing
authority, above the Council row, which directed the Rhyne cover-up through a
detective. What it sells is *impunity*, not protection: a blind eye, a lost file, a
delayed response, a patrol schedule. Every corrupt channel here is exactly that, and
should be bought per sub-district from a named officer. The plausible guarantors for a
player-founded organisation are a corrupt sergeant or captain (McCarlson/Kowalsky
type), a fixer with a badge (Regina's asset, Muamar's friend Daniels, Padre's
informants), the commissioner at a corp-scale price, and **MaxTac as a contract, not an
alliance** — the most expensive and most decisive purchase in the matrix. It is a poor
military guarantor (no ground, one quest-owned prison) but a strong political one: a
non-intervention agreement or a Council title outweighs a squad. And who guarantees the
NCPD? Night Corp pays, the Council legislates, Arasaka and Militech equip, the mayor
appoints — every one a switch, in a paramilitary body whose Military strength is
entirely borrowed. Also outside `data/factions.json`: the corporate security industry
(its competitor for its own contract), privatised prison operators (the only growing
line item), Los Padres Penitentiary (`2077PL (mentioned)` only — a custody destination,
not a holding), the Harbor Police (a separate waterfront force), Dr. Yawen Packard (the
lab's only named staffer) and the anonymous ex-cop author of *Anatomy of a Disaster*
(the department's only labour voice). `[inferred]`

---

## 4. Pillar notes

Design (`gameplay-systems.md`): **Paramilitary Organization** (archetype strength
**Military**, weakness **Economy**); faction strength **Technology**, weakness
**Politics**. Row marked *tentative*.

**Military (strength) — supported, but sharp not large.** "Resources of a small
army": AVs, Minotaurs, Wyvern/Griffin/Bombus drones, Robot R, MaxTac — yet 91 roster
units, 15 `cs_patrol_*` areas of 273, and a MaxTac tier of four operators.
**Economy (weakness) — supported and structural:** a privatised monopoly that cannot
price its own service (ticketing over casework, 5€$/min calls, half the force fired,
"no closer to becoming profitable", capitalization −17%). Not poor cash flow — it
**cannot convert authority into revenue**. **Technology (strength) — supported only at
the top and only recently:** Patrol gear is "basic or outdated", cutting-edge kit is
"reserved strictly for MaxTac", and the Centaur order is the first modern Patrol
procurement and is called belated. **Politics (weakness) — overwhelmingly supported and
defining:** corporate crimes removed, Dogtown closed, Pacifica lost, Badlands
unpatrolled; the commissioner is an appointee and a criminal, and the only political
asset is a sponsorship the department does not control. **Overall fit — good, one
correction:** the causal order is inverted. The NCPD is not militarily strong and
therefore politically weak; it is **politically weak and therefore militarily thin**.
Funding came first; the guns are what is left. `[wiki]` `[game-data]` `[inferred]`

Cautions, not redesigns: **not a garrison faction** (express Military as *response
capability* — the location doc's §11.4 prevention hook already models it); **the
commissioner is not a boss in a room**; **MaxTac is a vassal, not a sub-unit**;
**Politics = dependency, not skill**.

---

## 5. Gaps and uncertainties

1. **No offline attitude matrix** — `Attitude_Record.hpp` is opaque, the NCPD has no
   relation rows, and every stance is judged.
2. **No political leadership in the extract** — commissioner, deputy, captain and
   spokesperson are `mentioned` only; **`Character.Sobchak` is River Ward**, and no
   `Character.River*` exists.
3. **"Han Dao Tzu" is not real** — only Dao Hyunh and Harold Han. Do not seed it.
4. **Two 2077 commissioners** — Fawlter (2076–) and Coleridge (an N54 report).
   `06_ncpd_chief` → Fawlter is a role join, inferred from venue plus the guest list.
5. **No MaxTac commander above lieutenant, and no MaxTac base** — Los Padres is
   `mentioned` only; Tom's Diner is the only physical trace.
6. **The lab has one named person** (Dr. Packard) and no garrison; **the prison
   garrison may despawn** — all 28 records are `mq062_*` communities.
7. **`client` conflicts with `arasaka.md` and `militech.md`** on direction (§3.2);
   **`night_corp client` rests on one wiki sentence** plus the funding line.
8. **No union, no labour politics**; **`trauma_team trade` is one co-location and one
   hand-off**; **`fixer_wakako`/`fixer_dino` are `trade` on gig mechanics**, not
   campaigns; **`sixth_street` fights beside the NCPD once** (`q305`).
9. **Rory's "Dependent" status is survival, not rank** — killable in a Patch 2.0 boss
   fight; **the `Members` page has no records**, so eight of its 2077 names have no
   actor.
10. **`District_Record.PreventionPreset()` is already owner-keyed** (the Dogtown branch
    switches on `mq304_*` facts) — upstream proof that police response can depend on
    who controls a sub-district.

### Sources consulted

Local: `data/factions.json`; `data/sites/rosters.json` (91 units / 22 sites / 46
records, zero named); `dist/extract/areas.jsonl` (273 NCPD areas); `markers.jsonl`;
`dist/extract/raw/**/always_loaded_{0,1,2}.streamingsector.json` (27,411 registry
entries parsed); `docs/research/factions/ncpd.md`; `docs/design/gameplay-systems.md`
§1, §5–§7; `politics/METHOD.md`; `../METHOD.md`; sibling politics docs.

Wiki (MediaWiki API, `action=parse&prop=wikitext`, 2026-11-25; base
`https://cyberpunk.fandom.com/wiki/`): NCPD, `Night_City_Police_Members`,
`Night_City_Police_Headquarters`, `NCPD_Precinct_%28disambiguation%29`,
`Little_China_NCPD_Precinct`, `Glen_NCPD_Precinct`, `Arroyo_NCPD_Precinct`,
`NCPD_Precinct_5`, `Pacifica_NCPD_Precinct`, `NCPD_Lab`, `Night_City_Prison`,
`Jerry_Fawlter`, `Commissioner_Ramos`, `Claudia_Feldman`, `River_Ward`,
`Harold_Han`, `Henry_Stints`, `Aaron_McCarlson`, `Anna_Hamill`, `Jasmine_Dixon`,
`Barry_Lewis`, `Ayden_Daniels`, `Dao_Hyunh`, `List_of_Cops`, `MaxTac`,
`MaxTac_Members`, `Melissa_Rory`, `Max_Hammerman`, `Ares`,
`Los_Padres_Penitentiary`, `NCPD_Beat_Cop`, `NCPD_Police_Corporal`, `Cop`,
`I_Fought_the_Law`, `The_Hunt`, `Happy_Together`, `Clampdown`, `Bullets`,
`Black_Steel_In_The_Hour_of_Chaos`, `You_Know_My_Name`, `Gig:_Cuckoo%27s_Nest`,
`Suspected_Organized_Crime_Activity:_Vice_Control`,
`Cyberpsycho_Sighting:_Seaside_Cafe`, `NCPD_-_Anatomy_of_a_Disaster`,
`Shard_with_MaxTac_Convoy_Intel`, `Government_of_Night_City`, `Night_City_Hall`,
`Night_Corp`, `Trauma_Team`, `Dogtown`.

---

## 6. Machine-readable block

```json
{
  "faction_code": "ncpd",
  "leaders": [
    {"name": "Jerry Fawlter", "role": "Commissioner from 2076; ex-dataterm sales head; mayor's appointee; personally corrupt (Loeb ambush, Northside clearance, Sapphire deal)", "character_record_id": null, "location_name": "NCPD HQ / Black Sapphire gala (Dogtown)", "presence_class": "mentioned", "open_world": false, "source": "wiki Jerry Fawlter and Night City Police Department; You Know My Name guest list; raw registry entry 06_ncpd_chief -> Character.q303_paradise_ncpd_chief is the party's NCPD chief, identity inferred by role and venue", "confidence": "wiki+game-data+inferred"},
    {"name": "Claudia Feldman", "role": "Deputy Commissioner; disbanded the Pacifica precinct on 17 Oct 2072 with Mayor Rhyne's support", "character_record_id": null, "location_name": "NCPD HQ", "presence_class": "mentioned", "open_world": false, "source": "wiki Claudia Feldman; shard Pacifica Precinct Restructuring", "confidence": "wiki"},
    {"name": "Commissioner Ramos", "role": "Commissioner before and during the Unification War; ordered the withdrawal from Pacifica; still in post 2071", "character_record_id": null, "location_name": "NCPD HQ", "presence_class": "historical", "open_world": false, "source": "wiki Commissioner Ramos; 2077SC", "confidence": "wiki+lore"},
    {"name": "Coleridge", "role": "Commissioner named in an N54 report after The Pickup at a joint press conference with Militech; unreconciled with Fawlter", "character_record_id": null, "location_name": "NCPD HQ", "presence_class": "mentioned", "open_world": false, "source": "wiki Night City Police Members; wiki The Pickup", "confidence": "wiki"},
    {"name": "River Ward", "role": "Detective, Homicide; suspended for re-opening the Rhyne inquest; gig-giver of I Fought the Law and The Hunt", "character_record_id": "Character.Sobchak", "location_name": "Megabuilding H10 (Little China) / NCPD Lab (the Glen) / Edgewood Farm", "presence_class": "world-activity", "open_world": true, "source": "raw always_loaded_1 registry entry sobchak -> Character.Sobchak (13 phases incl. default, dlc3_river_sleep, q200_river_attacks, q203_sobchak_coffee); entry river_holo -> same record; VR variant Character.sq029_sobchak_vr; gig-giver of I Fought the Law and The Hunt; wiki River Ward", "confidence": "game-data+wiki"},
    {"name": "Harold Han", "role": "Detective, Homicide; Ward's partner; executed Deputy Mayor Holt's cover-up of Rhyne's death", "character_record_id": null, "location_name": "Little China / the Glen diner", "presence_class": "story", "open_world": false, "source": "wiki Harold Han; wiki I Fought the Law; no Character.* record found in the registry", "confidence": "wiki"},
    {"name": "Gonaghal", "role": "Detective assigned the Peter Pan abductions; called lazy and incompetent by Ward", "character_record_id": null, "location_name": "NCPD HQ", "presence_class": "mentioned", "open_world": false, "source": "wiki Night City Police Members; wiki The Hunt", "confidence": "wiki"},
    {"name": "Henry Stints", "role": "Inspector, Heywood; Streetkid-lifepath arresting officer; orders V and Jackie beaten on an Arasaka executive's word", "character_record_id": "Character.q000_kid_parking_stints", "location_name": "Embers parking garage, the Glen", "presence_class": "prologue", "open_world": false, "source": "raw always_loaded_1 registry entry officer4 -> Character.q000_kid_parking_stints (phases q000_parking_arrival, q000_parking_moved_closer, q000_parking_point_gun); wiki Henry Stints", "confidence": "game-data+wiki"},
    {"name": "Aaron McCarlson", "role": "Sergeant; corrupt; had a former lover shot and bought the Maelstrom footage; former consultant on Regina Jones's show", "character_record_id": null, "location_name": "Dino Dinovic's bar, Downtown (City Center)", "presence_class": "world-activity", "open_world": true, "source": "wiki Aaron McCarlson; gig Scrolls Before Swine (baseid sts_wat_lch_08)", "confidence": "wiki+game-data"},
    {"name": "Anna Hamill", "role": "Sergeant; honest undercover officer; investigated a Kabuki smuggling ring tied to Jotaro Shobo; killed her corrupt colleagues", "character_record_id": null, "location_name": "Kabuki Market apartment, Watson", "presence_class": "world-activity", "open_world": true, "source": "wiki Anna Hamill; gig Scrolls Before Swine; registry anna_hamill_child_01/02 -> Character.dd_annaHamillKid are her children, not her", "confidence": "wiki+game-data"},
    {"name": "Robert Kowalsky", "role": "Captain; Hamill's superior; shut down her investigation and paid a fixer to have her silenced", "character_record_id": null, "location_name": "Kabuki precinct, Watson", "presence_class": "mentioned", "open_world": false, "source": "wiki Night City Police Members; shard Archived Conversation: Anna Hamill and Robert Kowalsky", "confidence": "wiki"},
    {"name": "Jasmine Dixon", "role": "Sergeant since 2061; involuntarily committed to a psychiatric facility for reporting corruption", "character_record_id": null, "location_name": "Night City Center for Psychiatric Health, Rancho Coronado", "presence_class": "world-activity", "open_world": true, "source": "wiki Jasmine Dixon; gig Cuckoo's Nest (baseid sts_std_rcr_02)", "confidence": "wiki"},
    {"name": "Sara Krakosky", "role": "Lieutenant; the department's official spokesperson", "character_record_id": null, "location_name": "NCPD HQ", "presence_class": "mentioned", "open_world": false, "source": "wiki Night City Police Members; Night After Night with Ziggy Q", "confidence": "wiki"},
    {"name": "Melissa Rory", "role": "Lieutenant, MaxTac SPAR commander; captured as a cyberpsycho on 10 Jan 2077 and reconditioned into the unit; psych record notes relapse risk", "character_record_id": "Character.mq030_melisa", "location_name": "Jinguji, Downtown (City Center)", "presence_class": "world-activity", "open_world": true, "source": "raw always_loaded_1 registry entry mq030_melisa -> Character.mq030_melisa (phases mq030_melisa_av_intro, mq030_melisa_call_zane, mq030_melisa_talk_witness, mq030_melisa_testimony, mq030_melisa_aftermath); wiki Melissa Rory; job Bullets", "confidence": "game-data+wiki"},
    {"name": "Max Hammerman", "role": "Sergeant/Commander of MaxTac 2020-2045; kept the unit alive after the Holocaust and took it independent of the NCPD", "character_record_id": null, "location_name": "MuCJuC (2020) / MAX-TAC HQ (2045)", "presence_class": "historical", "open_world": false, "source": "wiki Max Hammerman; Cyberpunk RED", "confidence": "wiki+lore"},
    {"name": "Ares", "role": "Cyberpsycho squad leader 2010-2020; captured alive and reconditioned into command", "character_record_id": null, "location_name": "MuCJuC", "presence_class": "historical", "open_world": false, "source": "wiki Ares; 2020NC", "confidence": "wiki+lore"}
  ],
  "internal_factions": [
    {"name": "The commissioner's office (privatisation bloc)", "leader": "Jerry Fawlter", "goals": "Revenue, visibility and the mayor's favour; run the department as a profit centre; protect MaxTac because its visibility wins public relations", "members_hint": "HQ staff; the 2076 reorganisation; the Black Sapphire NCPD chief actor; no serving officer below him is attested as his ally", "source": "NCPD - Anatomy of a Disaster; wiki Jerry Fawlter; wiki Night City Police Department", "confidence": "wiki+game-data"},
    {"name": "The precinct machine (corrupt cops)", "leader": "Robert Kowalsky; Aaron McCarlson", "goals": "Keep the local arrangement: smuggling rings, bought blind eyes, seized-goods resale, fixer consulting fees", "members_hint": "Named captains and sergeants; the Hamill, McCarlson, Beemer and Loeb scandals; 58 of 91 roster units are patrol ranged", "source": "Scrolls Before Swine; Archived Conversation: Anna Hamill and Robert Kowalsky; wiki Henry Stints", "confidence": "wiki+game-data"},
    {"name": "The clean cops (reform remnant)", "leader": "River Ward; Anna Hamill; Jasmine Dixon", "goals": "Solve the case, refuse the bribe, report what they see; treat the badge as a promise", "members_hint": "Three named individuals with no institutional base; all three are suspended, targeted or committed", "source": "I Fought the Law; The Hunt; Scrolls Before Swine; Cuckoo's Nest", "confidence": "wiki+game-data"},
    {"name": "MaxTac (autonomous unit)", "leader": "Melissa Rory", "goals": "Prototypes, a free hand, no internal investigations, and the hunt", "members_hint": "Four operator spots at Tom's Diner; mq030_max_tac_1-9; the q305 convoy squad (maxtac_av_01-04, miniboss_1/2); q001 hologram pair", "source": "Bullets; MaxTac database entry; Black Steel In The Hour of Chaos", "confidence": "wiki+game-data"},
    {"name": "Internal Affairs Division", "leader": null, "goals": "Investigate officers suspected of corruption or gross misconduct; survive being hated by every other division", "members_hint": "No named 2077 officer; a division only; cannot investigate MaxTac", "source": "wiki Night City Police Department (Internal Affairs)", "confidence": "wiki"},
    {"name": "The corp-bought liaison layer", "leader": null, "goals": "Keep Arasaka, Militech and Night Corp money flowing; keep corporate crime out of police jurisdiction", "members_hint": "No records; attested through the sponsor model, the Militech-approved extraction and the Centaur purchase", "source": "wiki NCPD database entry; shard Extraction #NC/EX/56/882; wiki The Pickup", "confidence": "wiki"},
    {"name": "The Night City Prison garrison", "leader": null, "goals": "Custody, quiet, and the privatised-prison partnership that is the only growing budget line", "members_hint": "6 mq062 communities, 28 records, 19 named #std_arr_prison_ncpd_002-020 slots - the only real garrison in the extract", "source": "dist/extract/areas.jsonl mq062_*; wiki Clampdown; wiki Night City Prison", "confidence": "game-data+wiki"}
  ],
  "relations": [
    {"faction_code": "tyger_claws", "stance": "hostile", "evidence": "Two SOCAs (Tygers by the Tail, Modern Labor Market), three Reported Crimes (Protect and Serve, One Thing Led to Another, Crash Test) and multiple Assaults in Progress are NCPD-issued against Tyger crews [game-data] [wiki]. Bought channel: Hamill's captain Kowalsky and colleague Bill Adams paid Regina Jones to silence her over a Kabuki smuggling ring tied to Jotaro Shobo; the 2045 Kimen-Gumi collaborated with the NCPD on occasion [wiki]", "confidence": "game-data+wiki"},
    {"faction_code": "valentinos", "stance": "hostile", "evidence": "SOCA at Valentino Alley and Mercado Sonora, Assault in Progress in Downtown and Arroyo, Zoe Alonzo's NCPD record [game-data] [wiki]. Bought channel: Sgt. Aaron McCarlson conspired with Valentino Claudio Moreno to murder his former superior Dario Sanchez and guaranteed the police would not interfere; Padre has informants in NCPD command [wiki]", "confidence": "game-data+wiki"},
    {"faction_code": "arasaka", "stance": "client", "evidence": "The NCPD is beholden to the interests of Arasaka and Militech, and corps put their interests in the Police Department expecting something in return; corporate crimes are removed from police jurisdiction sooner or later; Inspector Stints orders V and Jackie beaten on the word of Arasaka executive Kaoru Fujioka. Direction: the department serves Arasaka's interest [wiki]", "confidence": "wiki"},
    {"faction_code": "militech", "stance": "client", "evidence": "Militech is the NCPD's equipment supplier (Lexington, Saratoga, Ajax, Tactician, Defender; Minotaur, Wyvern, Bombus, Griffin, Robot R Mk.2; Enforcer, Ironclad, Overlord, Manticore, Atlus, Hellhound, Behemoth) and one of its creditors; its Investigations Department ran an extraction with explicit NCPD approval and no police intervention, and Commissioner Coleridge held a joint press conference with Stout after a Centaur purchase. Direction: the department depends on Militech [wiki]", "confidence": "wiki"},
    {"faction_code": "kang_tao", "stance": "neutral", "evidence": "No attested interaction. Corpo Plaza is jointly patrolled by NCPD and private corporate security, but no Kang Tao-specific arrangement is attested [wiki] [inferred]", "confidence": "wiki+inferred"},
    {"faction_code": "biotechnica", "stance": "neutral", "evidence": "No attested interaction. Biotechnica's own internal order forbids sharing information with the NCPD; that is a corporate policy, not a police relationship [wiki] [inferred]", "confidence": "wiki+inferred"},
    {"faction_code": "petrochem", "stance": "neutral", "evidence": "No attested interaction. A Petrochem gas station hosts two cpz_ncpd_police records at a scanner site, which is response presence, not a relationship [game-data] [inferred]", "confidence": "game-data+inferred"},
    {"faction_code": "barghest", "stance": "hostile", "evidence": "The NCPD is forbidden to enter Dogtown proper and cannot drive through the gate; Barghest's Prevention Unit polices the district; the Pacifica precinct was disbanded in 2072 after Barghest- and VDB-led riots; Dodger holds two NCPD officers prisoner and blackmails one [wiki]. Corrupt channel: Commissioner Fawlter attends Hansen's Black Sapphire gala and deals with a 6th Street officer there [wiki] [game-data]; MaxTac is the one NCPD unit allowed inside [wiki]", "confidence": "game-data+wiki"},
    {"faction_code": "sixth_street", "stance": "hostile", "evidence": "The gang was founded to replace a corrupt NCPD it considered useless, and its ersatz law is tolerated in its own turf; NCPD runs SOCA and scanner activity against Darius Miles and Olga Longmead [game-data] [wiki]. Exceptions: Fawlter deals with a 6th Street officer at the Sapphire, and 6th Street fights alongside the NCPD in the q305 MaxTac convoy ambush - the only attested joint operation [wiki] [game-data]", "confidence": "game-data+wiki"},
    {"faction_code": "aldecaldos", "stance": "hostile", "evidence": "Fortunate Son: the NCPD ambush the implant pickup and try to kill V, as they believed Dakota was helping Raffen Shiv and could not tell them from nomads [wiki]; cops do not like nomads is standing lore [lore]. Exceptions: Hamill ends up with the Aldecaldos and River Ward's sister is married to one [wiki]", "confidence": "wiki+lore"},
    {"faction_code": "wraiths", "stance": "hostile", "evidence": "The NCPD dispatches three SOCAs against named Wraith cells (Ward, Craven, McBride) and posts bounties naming each cell leader [wiki] [game-data]; Wraiths are the subject of Assault-in-Progress, Reported Crime and la_sm_execution_03 scenes across 16 highway communities [game-data]", "confidence": "game-data+wiki"},
    {"faction_code": "animals", "stance": "hostile", "evidence": "An NCPD APB names Denzel Cryer and his Juice ring (SOCA: Living the Big Life); Assault in Progress and scanner-hustle sites at Corpo Plaza, JapanTown, Little China and Coastview [game-data] [wiki]. Bought channel: Acting Mayor Holt hired the Animals to wreck the Red Queen's Race, then failed to pay them [wiki]", "confidence": "game-data+wiki"},
    {"faction_code": "the_mox", "stance": "neutral", "evidence": "No NCPD raid, scanner hustle or SOCA against the Mox is attested; the Mox are the only gang V cannot attack under normal circumstances, and Judy's NCPD call about Evelyn's suicide is brushed off (Both Sides, Now). Tolerance and neglect, not an alliance [wiki] [inferred]", "confidence": "wiki+inferred"},
    {"faction_code": "maelstrom", "stance": "hostile", "evidence": "MaxTac killed Hextra, Maelstrom's 2030s leader [wiki]; Caliber was assassinated, possibly by NCPD or MaxTac [wiki]; Maelstrom is a standing target of scanner hustles and organised-crime activities [game-data] [wiki]. Corrupt channel: Commissioner Fawlter conspired with Maelstrom's Aleksandra Zaytsova to ambush officer Reggie Loeb, and Sgt. McCarlson bought Maelstrom CCTV footage [wiki]", "confidence": "game-data+wiki"},
    {"faction_code": "voodoo_boys", "stance": "hostile", "evidence": "The Voodoo Boys are the de facto law in western Pacifica and hold it against NCPD and corporate eviction; an NCPD task force was expelled in 2072 [wiki]; VDB records appear in NCPD crime-scene and patrol areas (cs_police_execution_com, cs_highway_patrol_com) [game-data]", "confidence": "game-data+wiki"},
    {"faction_code": "night_corp", "stance": "client", "evidence": "The NCPD is partly financed by Night Corp's shrinking coffers; the police force's official sponsor is Night Corp, and MaxTac's funding is likewise [wiki]; the design also assigns Night Corp places to NCPD [game-data]. Direction: Night Corp pays, the NCPD depends", "confidence": "wiki+game-data"},
    {"faction_code": "city_council", "stance": "client", "evidence": "The Council grants the department its powers (detention without charge up to a year, limb shots as warning shots, firing on fleeing vehicles, unofficial collateral against cyberpsychos), legislates its remit, decided to wall off Serenisands, and the mayor appoints and directs the commissioner. Direction: the department answers to the Council and the mayor [wiki]", "confidence": "wiki"},
    {"faction_code": "scavengers", "stance": "hostile", "evidence": "Standing target: NCPD APBs name Zbyszko, Kolev, Yelena Sidorova and Barry; scanner hustles and reported crimes at Ross Street, Opposites Attract, Eden Beach, West Wind, Northside and Coastview [game-data] [wiki]. Corrupt channel reaching the top: Commissioner Fawlter hires Yelena Sidorova to clear the homeless in Northside and promises to ignore calls from the area [wiki]", "confidence": "game-data+wiki"},
    {"faction_code": "fixer_regina", "stance": "trade", "evidence": "The department's most active fixer counterpart: she retrieves Maelstrom footage for Sgt. McCarlson and then blackmails him into an asset; Kowalsky and Adams paid her to have Hamill killed; McCarlson formerly consulted on her show Cops 'n' Chops [wiki]", "confidence": "wiki"},
    {"faction_code": "fixer_wakako", "stance": "trade", "evidence": "She gives Clampdown, a prison break whose enemy list includes the NCPD; she also brokers the return of NCPD-adjacent data. Transactional, not an anti-NCPD campaign [wiki] [game-data]", "confidence": "wiki"},
    {"faction_code": "fixer_padre", "stance": "trade", "evidence": "Padre has informants in NCPD command [wiki]; his Heywood turf is the department's densest area by recorded presence (Glen 84, Wellsprings 43, Vista del Rey 25) [game-data]. A standing intelligence channel, not hostility", "confidence": "wiki"},
    {"faction_code": "fixer_el_capitan", "stance": "trade", "evidence": "He is not keen on the NCPD, saying they do the people a disservice by always intruding where they do not belong, yet works with them when it pays; his friend Ayden Daniels is an NCPD officer who fabricates evidence and takes bribes and has worked closely with Reyes for years; he also brokers Dixon's escape from the psych ward [wiki]", "confidence": "wiki"},
    {"faction_code": "fixer_dakota", "stance": "hostile", "evidence": "Fortunate Son is her anti-NCPD Badlands gig: the NCPD ambush the implant pickup and try to kill V because they believed Dakota was helping Raffen Shiv [wiki] [game-data]", "confidence": "wiki"},
    {"faction_code": "fixer_dino", "stance": "trade", "evidence": "His Downtown bar is where corrupt Sgt. McCarlson can be found after Scrolls Before Swine resolves, and he runs the two gigs that put the department's political masters in play (Serial Suicide, The Frolics of Councilwoman Cole). Bought, not hostile [wiki] [game-data]", "confidence": "wiki"},
    {"faction_code": "fixer_rogue", "stance": "neutral", "evidence": "No NCPD-specific gig or lore link found; Afterlife is neutral ground [inferred]", "confidence": "inferred"},
    {"faction_code": "fixer_mr_hands", "stance": "neutral", "evidence": "His Dogtown work runs through Barghest and the FIA, the two bodies the NCPD cannot act against; no NCPD-specific channel is attested [wiki] [inferred]", "confidence": "wiki+inferred"},
    {"faction_code": "afterlife", "stance": "neutral", "evidence": "Neutral merc marketplace; the NCPD hires mercenaries on the sly, but no Afterlife-specific arrangement is attested [wiki] [inferred]", "confidence": "inferred"},
    {"faction_code": "nusa", "stance": "neutral", "evidence": "The NUSA is the city's adversary (Unification War, Arvin Accord), not the department's; the federal analogue is the FIA, aimed at Dogtown, not at the NCPD [wiki] [inferred]", "confidence": "wiki+inferred"},
    {"faction_code": "netwatch", "stance": "neutral", "evidence": "No attested interaction. Night City has its own NetSec division, which is the institutional reason it would not use NetWatch, though many other municipalities rely on it [wiki] [inferred]", "confidence": "wiki+inferred"},
    {"faction_code": "zetatech", "stance": "client", "evidence": "Zetatech supplies the Bombus reconnaissance drone and the Atlus vehicle in the post-2076 inventory, both named in Commissioner Fawlter's drones-for-cops policy; the department depends on Zetatech airframes as it does on Militech small arms [wiki]", "confidence": "wiki"},
    {"faction_code": "trauma_team", "stance": "trade", "evidence": "Co-response and hand-off: The Hunt ends with River Ward parting from Trauma Team after the police work the scene; the sq021 community mixes seven NCPD officers with a Trauma Team actor and an AV [game-data] [wiki]. Professional division of labour, no loyalty", "confidence": "game-data+wiki"}
  ]
}
```


