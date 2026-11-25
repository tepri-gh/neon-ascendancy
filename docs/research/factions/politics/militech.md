# Militech — Leadership, Internal Politics and External Relations

Status: faction politics research run, 2026-11-25. One faction, one document.
Scope: Cyberpunk 2077 2.5 + Phantom Liberty, campaign disabled. Who a player can
join under, climb past, ally with or remove inside Militech; the corporate blocs;
and the external-relations matrix needed for wars, alliances and "guarantor"
support when a player founds an organisation.

Method: this document follows the evidence rules in
[`METHOD.md`](./METHOD.md), including the §1.1 corrections (applied first), and
the data pitfalls in [`../METHOD.md`](../METHOD.md) §1.1–§1.2. The location
catalogue for Militech is [`../militech.md`](../militech.md); this document maps
people and politics onto those places and does not repeat the coordinates.
`AGENTS.md` was read first. No commits, no game launch; helper scripts ran
outside the repo under `python3 -I`.

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Position, site, community, roster or raw-registry record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/comic/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My reasoning links a named person, place or stance to a record; reasoning stated | Weak, flagged |

Extra convention for this document only: **presence class**.
`ambient` = persists in free roam without a quest (Militech patrols, convoys and
executions spawn this way); `world-activity` = gig, scanner hustle, assault in
progress or cyberpsycho sighting, i.e. free-roam content but activity-gated;
`story` = gated by a main or side job; `off-map` = alive and named in 2077 but
never spawned (an executive, a shard author, a prison); `historical` = not
present in 2077. Militech has **no `prologue` class**: the Corpo lifepath
(`q000_corpo_*`) belongs to Arasaka, not to this faction. The JSON `open_world`
flag is `true` only for `ambient` and `world-activity`.

A corporation is not a gang, and Militech is not even a normal corporation.
Four adjustments are used throughout and are flagged again in §5:

- **Leadership is an org chart plus a state.** The CEO, the board and the Night
  City branch are "leadership"; the NUSA president is Militech's former CEO and
  its political sovereign at the same time. The hierarchy cannot be read without
  the nationalisation.
- **The best wiki source is the employee list**, and even it is thin: the 2077
  table has three entries with rank "Unknown".
- **"Dependent" is the normal 2077 state** for the two Night City figures who
  actually have records (Stout, Gilchrist) and for the Phantom Liberty cast
  (Myers, Hansen).
- **The decisive evidence is often in another faction's location doc.** Militech
  is the most-raided, most-infiltrated and most-executed-against corp in the
  game; the Wraiths, 6th Street, Animals and Night Corp documents carry incidents
  this faction's own page does not.

---

## 1. Leadership and ranks

### 1.1 The 2077 chain of command

Militech is a **nationalised public corporation**: the NUSA government
nationalised it in 2023–24 after the Night City Holocaust, ex-Militech officials
staffed the re-formed Department of Defense, and several board members still
hold high-ranking ministry posts in 2077. Over 60% of its contracts come from
the NUSA, and Washington D.C. is its largest single customer. `[wiki]`

That produces a top that is simultaneously corporate and governmental:

| Name | 2077 role | Character record | Location / influence point | Presence class | Source | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| **Lucas Harford** | CEO (2069–2077); Myers's successor and political ally | — (mentioned only) | Rosslyn HQ, Virginia; Militech Tower, Washington D.C. | `off-map` | Wiki *Militech* CEO infobox; wiki *Lucas Harford*; netpage `NETdir://militech.corp/leadership` | `[wiki]` |
| **Rosalind Myers** | Former CEO (2060–2069); NUSA President (2065–, third term in 2077); Militech's political patron | `Character.myers`; also `Character.myers_hallucination`, `Character.q302_spidertank_myers_follower` | Space Force One crash site, Dogtown; Kress Street Hideout; border crossing; Militech advertorials | `story` | Raw `always_loaded_1` registry entry `myers` (phases `myers_default_dialog`, `q301_06a_myers`, `q302_01_start`, `q302_07_myers_oath_combat`, `q305_11_border_crossing`, `q306_myers_epilogue_bench`); wiki *Rosalind Myers* | `[game-data]` `[wiki]` |
| **The Board of Directors** | Collective owner: 430M shares; Lundee held 8%, Roland Yee and the board 22%; DoD seats | — (no individual records) | Rosslyn; Militech Tower; Hong Kong (Yee's office, 2020) | `off-map` | Wiki *Militech* (share structure, nationalisation); wiki *List of Militech employees*; wiki *Roland Yee* | `[wiki]` |
| **Meredith Stout** | Senior Operations Manager, Night City; later Government Relations Executive | `Character.Stout`; holocall variant in a separate community | Watson (Northside/waterfront); All Foods Plant; N54 City Hall signing | `story` | Raw registry entry `stout` (phases `start`, `talk`, `interrogation`, `maelstrom_van`, `maelstrom_end`, `end`, `q003_stout_sex_no_tell`); separate `meredith_holo` community; markers `q003_08_sm_stout`, `{q003_mp_no_tell_stout}`; wiki *Meredith Stout* | `[game-data]` `[wiki]` |
| **Anthony Gilchrist** | Corp; Militech's mole inside the Maelstrom convoy leak | `Character.Gilchrist`; holocall variant | All Foods Plant (held by Stout's team); Northside storm channel (corpse) | `story` | Raw registry entry `gilchrist` (phases `attack`, `holocall`, `meeting`, `meeting_suv`, `start`, `leaving`); separate `anthony_gilchrist_holo` community; wiki *Anthony Gilchrist* | `[game-data]` `[wiki]` |
| **Keenan Thorston** | Deputy Director of Operations, Investigations Department, Night City Branch | — (shard author only) | Militech Offices, Corpo Plaza | `off-map` | Shard *Extraction #NC/EX/56/882* (`baseid ma_hey_gle_13_onscreen_01`); wiki *List of Militech employees* | `[wiki]` |
| **Elizabeth W. Roider** | Senior Armed Engagement Specialist, Department of Intervention, Night City Branch | `Character.ma_hey_gle_13_militech_ranged2_ranged2_ajax_ma_Elizabeth_Roider` | Valentino Alley, Ventura St, the Glen | `world-activity` | Roster site 59 `ma_hey_gle_13` (`faction_id 21`, phase `A`); site anchor `(-1602.629, -1119.905, 9.120)`; shard *Extraction #NC/EX/56/882*; wiki *Elizabeth W. Roider* | `[game-data]` `[wiki]` |
| **Lt. Mower** | Lieutenant; cyberpsycho after military-grade implants; killed by her own hit squad | `Character.ma_wat_kab_08_cyberpsycho` | Allen & Abraham St arena, Kabuki | `world-activity` | Roster site 177 `ma_wat_kab_08` (`faction_id 21`, phase `default`); site anchor `(-1093.120, 1532.005, -0.090)`; shard *ORDERS*; wiki *Mower* | `[game-data]` `[wiki]` `[inferred]` |
| **Kurt Hansen** | Ex-Colonel (Militech Armed Forces); founder and head of BARGHEST; holds Dogtown | `Character.kurtz` | Dogtown (Black Sapphire, stadium, borders); Kress St bunker | `story` | Raw registry entry `kurtz` (phases `q301_01_start`, `q301_04_start`, `q303_casino`, `q304_01_start`); wiki *Kurt Hansen*; wiki *Dogtown – Analytical Summary* | `[game-data]` `[wiki]` |
| **Donald Lundee Sr.** | CEO (2020–d.); rebuilt the corp, nationalised under him, personal Arasaka vendetta | — (no 2077 record) | Rosslyn HQ | `historical` | Wiki *Donald Lundee*; wiki *Militech* history; *Cyberpunk RED* | `[wiki]` `[lore]` |
| **Elizabeth Kress** | CEO/president of Militech (?–2020); US/NUSA President; nationalised her own former employer | — | Washington D.C. | `historical` | Wiki *Elizabeth Kress*; wiki *Militech*; wiki *NUSA* | `[wiki]` `[lore]` |
| **Antonio Luccessi** | Co-founder (1996); executive VP; chief designer | — | Armatech/Militech R&D | `historical` | Wiki *List of Militech employees*; wiki *Militech* history | `[wiki]` `[lore]` |
| **Roland Yee** | Chairman of the board (2020); original investor | — | Militech Hong Kong office | `historical` | Wiki *List of Militech employees*; wiki *Militech* (share structure) | `[wiki]` `[lore]` |
| **Mels Engelsson** | VP and director of the Special Projects Department ("Dr Death") | — | SPD, New Mexico Proving Grounds | `historical` | Wiki *List of Militech employees*; wiki *Militech* (Special Projects) | `[wiki]` `[lore]` |
| **Donald Lundee Jr. ("Dixie")** | Employee; son and namesake of the former CEO | — (mentioned only) | — | `off-map` | Wiki *Donald Lundee Jr.*; *The World of Cyberpunk 2077* p.137 | `[wiki]` |
| **Samantha Lee Young** | General; "the face of the company" (2045) | — | — | `historical` | Wiki *Samantha Lee Young*; *Cyberpunk RED* p.273 | `[wiki]` `[lore]` |

Notes:

- **The CEO line is clean, the dates are not.** The infobox gives
  Kress (?–2020) → Lundee (2020–?) → Myers (2060–2069) → Harford (2069–2077).
  The article body says Myers left "in 2065" to run for president, while the
  employee list and *Lucas Harford* put the handover in 2069. Both are `[wiki]`;
  the document uses 2069 and flags the conflict in §5. `[wiki]`
- **Myers is not Militech leadership in 2077.** She is the head of state that
  owns the company. She is in the table because the faction's politics cannot be
  modelled without her, not because she holds a Militech title. `[inferred]`
- **Harford has no actor and no page depth.** He exists as three wiki sentences
  and four netpage lines: pragmatic, level-headed, patriotic, "spiritual
  successor to Gen. Lundee", faithful ally of Myers, once paid a Unification War
  veteran's medical bill. That is the entire 2077 CEO. `[wiki]`
- **The board has no members you can name.** Roland Yee is a 2020 chairman;
  Anderson Bennett, Carson Dominguez, Bradley David Parker Jr and Margaret Ellen
  Goldstein are 2020 board figures only. The 2077 board is a collective with
  Defence Ministry day jobs. `[wiki]`
- **Hansen is ex-Militech, not Militech.** He is listed because the deserter wing
  is the faction's most important loyalty rupture (§2.6). Do not seed him as a
  Militech officer. `[wiki]`

### 1.2 The Night City branch

The Corpo Plaza tower is the **regional HQ**, not a sales office. The wiki is
explicit: regional offices "handle all local bulk arms contracts, mercenary
contracting, distribution, and other paperwork" and contain "the headquarters
for the local ranking Militech Officer," who coordinates all local military
endeavours and black operations and answers to a district operations coordinator
in Rosslyn. `[wiki]`

The branch is the only part of Militech the game actually builds:

| Layer | Who | Evidence |
| --- | --- | --- |
| Regional HQ / local ranking officer | Unnamed "local ranking Militech Officer" | Wiki *Militech* Regional Offices; site 11 `ma_cct_cpz_06` (`faction_id 21`, 4 rangers) under the Corpo Plaza concourse |
| Operations | **Meredith Stout**, Senior Operations Manager | `Character.Stout`; she owns the convoy-leak investigation and can have a peer killed |
| Investigations | **Keenan Thorston**, Deputy Director of Operations | Shard *Extraction #NC/EX/56/882*: political investigations, extrajudicial extraction, NCPD approval |
| Intervention (field) | **Elizabeth W. Roider**, Senior Armed Engagement Specialist | Site 59; leads the Valentino Alley snatch squad |
| Counter-intelligence (informal) | **Anthony Gilchrist**, corp — and the leak itself | `Character.Gilchrist`; the man Stout is hunting is inside the branch |
| Security contract line | **Militech SiteSecure** | Night Corp's maglev tunnel: "Night Corp hired a subgroup of Militech called 'Militech SiteSecure'" `[wiki]`; site 350 garrison is Militech `[game-data]` |
| Garrison officers | Lt. **Mower** (Kabuki), Cpt. **Ian Cochran**, Sgts **Martin Figgs** and **Martha Irving** (Detention Center) | `Character.ma_wat_kab_08_cyberpsycho`; Detention Center computer messages `[game-data]` `[wiki]` |

This is the best model for **joining Militech as an employee**, and it is
strictly worse than Arasaka's for the mod's purposes: Arasaka's Corpo lifepath
gives a player a desk, a boss, a rival department and a purge. Militech gives a
player a *field* job and a paperwork chain, and the game only shows it from the
outside — as the corp that raids you. There is no `q000_*` prologue for Militech.
`[game-data]` `[inferred]`

The formal 2020 hierarchy still describes the org that the 2077 branch sits in:
CEO and Chairman → President and executive VPs (Rosslyn) → board → national
directors → regional VPs (with a Regional Security Director, Sales Director and
Bank Director beneath) → area/local/district/site managers. Militech differs from
Arasaka in one structural way: **it has no bank**, so no Regional Bank Director
and no finance arm — the state is its balance sheet. `[wiki]`

### 1.3 Succession history

| Period | Leader | How the change happened |
| --- | --- | --- |
| 1996–2002 | **Antonio Luccessi** (founder); **Donald Lundee** (CEO from 1998/2002) | Luccessi built the rifle; Lundee resigned his USMC commission to run the company and renamed it Militech. `[wiki]` |
| 2002–2020s | **Donald Lundee** | Nearly forty years of expansion and a personal war with Arasaka. Nationalised in 2023–24; Lundee stayed on the board, ran the 4th Corporate War, and was ordered to stand down by President Kress. `[wiki]` |
| 2020s–2060 | **Elizabeth Kress** (as CEO/president) → the post-Lundee board | Kress was an ex-Militech president before she was US/NUSA president; she nationalised the company. Lundee's death opened the seat. `[wiki]` |
| 2060–2069 | **Rosalind Myers** | Succeeded Lundee on his death; "proponent of peace," reformist, interventionist. Resigned the CEO post (honorary resignation, before a confidence vote) to run for president. `[wiki]` |
| 2069–2077 | **Lucas Harford** | Myers's chosen successor; pragmatic, level-headed, faithful ally of the president. `[wiki]` |

The pattern is the opposite of Arasaka's: **succession is institutional and
political, not dynastic.** Every 21st-century handover went through the board,
the state, or an election. Nobody murdered a Militech CEO to take the chair. The
one dynastic flicker is Donald Lundee Jr., who is merely an employee. `[wiki]`
`[inferred]`

Two historical succession details matter for the simulation:

- **Military rank is a route to the top.** Lundee was a Marine general, Kress
  was a Militech executive who became president, Myers was a Marine who rose to
  CEO, Hansen was a colonel. Militech's executive pipeline runs through the
  officer corps, not a corporate academy. `[wiki]`
- **The board can be captured from outside.** The 2020 sourcebook notes that
  8% (Lundee) + 22% (Yee and the board) left a controlling bloc vulnerable to a
  leveraged buyout, and that hostile takeovers of arms firms were a known move.
  A player organisation cannot buy Militech shares in 2077, but the *logic* —
  the state owns the controlling interest — is the lever a political bloc would
  pull. `[wiki]`

### 1.4 Rank structure, entry and advancement

Militech publishes a **patriotic, military-industrial culture**, not a corporate
cult: dark uniforms, US flags, weapon discounts, "No American soldier deserves
to suffer alone." Its ranks are two ladders that share a ceiling.

**Corporate ladder.**

1. **CEO and Chairman.** Board-appointed; in practice a Pentagon-adjacent
   figure who is also the president's ally. `[wiki]`
2. **President, executive VPs, board.** Rosslyn; several board seats double as
   Ministry of Defense posts. `[wiki]`
3. **National Director / Regional VP.** Rosslyn-appointed; the regional VP sits
   above Security, Sales and (for Arasaka only) Bank directors. `[wiki]`
4. **Regional HQ staff.** The local ranking Militech Officer, operations
   managers (Stout), investigations deputies (Thorston), sales and contracts. `[wiki]`
5. **Employees and interns.** Up to 50% off Militech weapons; the corp is
   ranked the second-best employer in Night City. `[wiki]`

**Military ladder.**

1. **Recruit / guard.** The mass of the army; line infantry and facility
   security. `[wiki]`
2. **Soldier / ranger / specialist.** Pilots, gunners, technicians — 90% of the
   force in 2020. `[wiki]`
3. **Officer.** The game's `Officer` enemy is Tier 1 with a flashbang; on the
   corporate side, officers run sites (Mower, Cochran). `[wiki]` `[game-data]`
4. **Special ops, solos and agents — 10% of the force, never subcontracted.**
   Retained for the corporation's own use: Roider's Intervention squad, the
   Mower termination team, the "Special Projects" security. `[wiki]`
5. **Colonel and above.** Hansen reached colonel "at a very young age" and was
   given Operation Midnight Storm. `[wiki]`

**Entry and advancement.**

- **The showroom is the recruiting station.** 2020 lore: "showrooms also serve
  as recruiting stations, and any promising youngster or solo who wants to try
  his or her hand with the Militech Corporate forces is welcome to come on down
  for a personal interview, no appointment necessary." `[wiki]` The 2077 netpage
  keeps the same funnel — "Currently we are actively seeking: Netrunners,
  Recruits" — and the Corpo Plaza HQ concourse is the surviving showroom site. `[wiki]`
  `[game-data]`
- **The military academy is the officer route**, as it was for Hansen. `[wiki]`
- **Advancement is measured in deniable results.** Stout's career turns on
  recovering a convoy *and* on killing the man who leaked it; Thorston's turns on
  an extraction that must leave no witnesses; Gilchrist's turns on being
  unprovable. Competence is not the metric — *unattributable* competence is. `[wiki]`
- **The failure states are brutal and documented.** A wavering executive who
  loses a political case is tortured and dumped with concrete shoes (Stout). A
  damaged officer is terminated by a hit squad rather than treated (Mower). A
  retiree is "often discovered without proper medication, or even massacred by
  Militech themselves." `[wiki]`

**Practical consequence for the mod:** a player joining Militech should enter as
a **recruit or a contract specialist**, not as a Corpo. The ladder is
recruit → specialist → officer → special ops → regional staff, and the political
currency is *deniability*, not loyalty (contrast Arasaka) or chrome (contrast
Maelstrom). Promotion should be gated on completing black operations without
attribution, and the failure state should be disposal, not demotion. `[inferred]`

### 1.5 Named members mapped to game data

`data/sites/rosters.json` contains **159 Militech units across 65 distinct
records**, of which exactly **two are named people** (Roider at site 59,
Mower's cyberpsycho at site 177). The rest are `ranger*`, `soldier*`,
`enforcer*`, `sniper*`, `tech*`, `android*` and `drone*` variants. Named
Militech people live in the raw community registry and in shard text.

| Name | Role / note | Character record | Community / marker | Location | Presence class | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| Lucas Harford | CEO | — | — | Rosslyn / D.C. | `off-map` | `[wiki]` |
| Rosalind Myers | Ex-CEO; NUSA President | `Character.myers` | registry `myers` (31 phases, `myers_default_dialog` → `q306_myers_epilogue_spawn`) | Dogtown crash corridor; border; epilogue bench | `story` | `[game-data]` `[wiki]` |
| Meredith Stout | Senior Operations Manager | `Character.Stout` | `stout` (10 phases, init `end`); `meredith_holo` | All Foods; Watson waterfront; No-Tell Motel | `story` | `[game-data]` `[wiki]` |
| Anthony Gilchrist | Corp; the mole | `Character.Gilchrist` | `gilchrist` (init `attack`); `anthony_gilchrist_holo` | All Foods holding room; Northside storm channel | `story` | `[game-data]` `[wiki]` |
| Keenan Thorston | Deputy Director, Investigations | — | shard author | Militech Offices | `off-map` | `[wiki]` |
| Elizabeth W. Roider | Senior Armed Engagement Specialist | `Character.ma_hey_gle_13_..._Elizabeth_Roider` | site 59 `ma_hey_gle_13`, phase `A` | Valentino Alley, the Glen | `world-activity` | `[game-data]` `[wiki]` |
| Lt. Mower | Lieutenant; cyberpsycho | `Character.ma_wat_kab_08_cyberpsycho` | site 177 `ma_wat_kab_08`, `faction_id 21` | Allen & Abraham St, Kabuki | `world-activity` | `[game-data]` `[wiki]` `[inferred]` |
| Kurt Hansen | Ex-Colonel; BARGHEST head | `Character.kurtz` | `kurtz` (9 phases) | Dogtown | `story` | `[game-data]` `[wiki]` |
| Archibald Crane | Employee; border-wall fixer; betrays the corp's line for a friend | `Character.sts_bls_ina_05_archibald` | site 343 `sts_bls_ina_05`, phase `A_spawn` | Militech Detention Center | `world-activity` | `[game-data]` `[wiki]` |
| Bruce Welby | Smuggler; the detainee Crane frees | `Character.sts_bls_ina_05_bruce` | site 343, phases `A_spawn`, `car`, `scared`, `q114_party` | Detention Center | `world-activity` | `[game-data]` `[wiki]` |
| Cpt. Ian Cochran | Compound commander | — (computer message author) | Detention Center computers | Detention Center | `off-map` | `[wiki]` |
| Sgt. Martin Figgs; Sgt. Martha Irving | Shift NCOs | — | Detention Center computers | Detention Center | `off-map` | `[wiki]` |
| Donald Lundee Jr. | Employee, son of the ex-CEO | — | — | — | `off-map` | `[wiki]` |
| Anderson Bennett; Carson Dominguez; Bradley David Parker Jr; Margaret Ellen Goldstein | 2020 board members and investors | — | — | — | `historical` | `[wiki]` `[lore]` |
| Melissa Cruz; Gale Gibbs | 2077 employees, rank "Unknown/TBA" | — | — | — | `off-map` | `[wiki]` |
| Morgan Blackhand | 2020 Militech mercenary | — | — | — | `historical` | `[wiki]` `[lore]` |
| Thomas Star | Engineer, SKL-1903 project | — (shard author) | — | — | `off-map` | `[wiki]` |

Data cautions:

- **`Character.ma_wat_kab_08_cyberpsycho` is the only record at the Mower arena
  and it is Militech-tagged.** The site's `default_faction_id` is 21, the wiki's
  cyberpsycho sighting for that `baseid` is Lt. Mower, and the shard on the body
  is a Militech termination order. Three independent signals, but the record
  itself is a *generic psycho slot* — treat the mapping as `[inferred]` until
  seen in game. `[game-data]` `[wiki]` `[inferred]`
- **The Detention Center entry name `joshua` does not match its record.**
  `Character.sts_bls_ina_101_arden_bentzen` is an entry named `joshua` in the
  site-348 variant community, next to six `sts_bls_ina_101_miltech_security`
  guards. No wiki page exists for an "Arden Bentzen," and the `joshua` slot may be
  reused. Do not seed him; see §5. `[game-data]`
- **`Character.kurtz` is Hansen; `kurtz_*` is his whole army.** There is no
  `Character.Hansen`. A substring search for `hansen` returns nothing; a search
  for `kurt` returns 200+ Barghest soldiers. Use the exact `kurtz` entry. `[game-data]`
- **Stout and Gilchrist each have a second, separate community for their
  holocalls** (`meredith_holo`, `anthony_gilchrist_holo`). Holocall actors are
  not world spawns; only `stout` and `gilchrist` are. `[game-data]`
- **Tucker Albach is Kiroshi, not Militech.** She is the *client* of a Militech
  executive-protection detail (`sts_hey_gle_01`, 8 Militech guards). Do not list
  her as leadership. `[game-data]` `[wiki]`

### 1.6 What the game actually spawns (campaign disabled)

A wiki infobox does not mean an actor in free roam. This is the part other
systems must not assume.

**`ambient` — persists in free roam, no quest required.**

- **Generic patrols, convoys and executions across the Badlands.** `[game-data]`
  The `cs_*` dynamic events (`cs_heavy_militech_patrol*`,
  `cs_bls_assaulted_conv_militech_attacker*`, `cs_militech_execution*`,
  `cs_handcuffed_wraiths_militech*`) are open-world spawns, plus the fixed
  garrisons at the Sunshine Motel (`ina_04_com_outpost_crew`, 13) and the
  Detention Center (`ina_05_combat_com`, 14). There is **no named leader among
  them.** `[game-data]`

**`world-activity` — free-roam content, activity-gated.**

- **Elizabeth W. Roider** — Assault in Progress at Valentino Alley
  (`baseid ma_hey_gle_13`, site 59). The only named Militech officer with a
  garrison record. `[game-data]` `[wiki]`
- **Lt. Mower** — Cyberpsycho Sighting: Lt. Mower (`baseid ma_wat_kab_08`, site
  177). `[game-data]` `[wiki]`
- **Archibald Crane** and **Bruce Welby** — *Gig: Goodbye, Night City*
  (`baseid sts_bls_ina_05`). Crane is a Militech employee who defies the corp.
  `[game-data]` `[wiki]`
- **The Sunshine Motel garrison** — *Gig: Radar Love* (`baseid sts_bls_ina_04`).
  `[game-data]` `[wiki]`
- **The Gold Beach Marina security detail** — *Gig: The Frolics of Councilwoman
  Cole* (`baseid sts_cct_dtn_05`, `enemies = Militech`). `[game-data]` `[wiki]`
- **The Kabuki raid** — *Gig: Concrete Cage Trap* (`baseid sts_wat_kab_01`).
  `[game-data]` `[wiki]`
- **Tucker Albach's guard detail** — *Gig: Eye for an Eye* (`baseid sts_hey_gle_01`,
  8 Militech guards, `enemies = Militech Guards`). `[game-data]` `[wiki]`
- **The HQ concourse and West Pier hustles** — sites 11, 12 and 40
  (`ma_cct_cpz_06`, `ma_cct_cpz_10`, `ma_cct_dtn_15`). Four to six units each. `[game-data]`

**`story` — gated by a main or side job.**

- **Meredith Stout** and **Anthony Gilchrist** in *The Pickup*; Stout again in
  *Venus in Furs*. **Rosalind Myers** and **Kurt Hansen** across the Phantom
  Liberty chain (`q301`–`q306`). Do not expect any of them with the campaign
  disabled. `[game-data]` `[wiki]`

**`off-map` — alive in 2077, never spawned.**

- Lucas Harford, Donald Lundee Jr., Keenan Thorston, Melissa Cruz, Gale Gibbs,
  Thomas Star, and the board. `[wiki]`

**`historical` — not in 2077.**

- Lundee Sr., Kress, Luccessi, Roland Yee, Mels Engelsson, Samantha Lee Young,
  Morgan Blackhand, the 2020 board. `[wiki]` `[lore]`

**The finding.** **No named Militech leader is open-world.** The highest-ranking
named Militech person a player can meet without a quest is a *Senior Armed
Engagement Specialist* (Roider); the next is a *Lieutenant* (Mower), and both are
enemies in a scanner activity. Everything above them is `story` or `off-map`.
`[game-data]` `[inferred]`

Caveat: "campaign disabled" may also suppress gigs and scanner hustles. The
`world-activity` rows are the best reuse candidates, but they need an in-game
spawn check. The `story` and `off-map` rows are the ones to replace with
simulation agents, not expect the game to provide. `[inferred]`

### 1.7 Player-path hooks

| Person | Join under | Climb past | Ally with | Remove |
| --- | --- | --- | --- | --- |
| **Lucas Harford** | The patriotic-executive line: NUSA partnership, veteran paternalism, "no soldier left behind" | The board and the Pentagon seats are the ceiling; there is no ladder to CEO without the state | Myers, the board's DoD bloc, NN54 | Removing him means removing the Myers alignment — a political act, not an assassination |
| **Rosalind Myers** | The state: FIA channels, NUSA contracts, the border | She is the sovereign her own former company answers to; climbing past her is a constitutional coup | Harford, the FIA, the Federalist Party | She is `story`-gated and dies on several Phantom Liberty branches |
| **Meredith Stout** | Night City Operations: convoys, contract enforcement, corporate liaison | Gilchrist is the rival; the regional officer above her is the ceiling | A deniable merc (V's role), the NCPD liaison desk | If she loses the leak case she is tortured and drowned; if she wins she has a peer killed |
| **Anthony Gilchrist** | The mole's path: sell route data, take a cut, stay unprovable | He is the cautionary tale — his own blackmailers (Smasher, Maelstrom) own him | Maelstrom's deal-makers; nobody at Militech | Exposing him (Stout, or a Nomad-lifepath data trail) is the cleanest way to decapitate the leak ring |
| **Keenan Thorston** | Investigations: political dirt, extrajudicial extraction, "permanently neutralized" witnesses | NCPD liaison and Ministry cover are his ladder | The NCPD (approved operations), City Hall clients | Removing him severs Militech's domestic political-policing channel |
| **Elizabeth W. Roider** | Department of Intervention: field snatch squads | She is a squad lead, not a ladder — climbing past means the branch | Thorston; the Glen operation's chain | Killing her ends Militech's only open-world named officer |
| **Lt. Mower** | Not a path; she is a **failure state** | — | — | Her own employer already sent the hit squad; the player finishes it |
| **Archibald Crane** | The employee who bends the line: border fixes, smuggling friends out | He has no rank to climb; he has a conscience and a badge | Bruce Welby; the nomad underground | He is the one Militech employee who proves the corp can be beaten from inside |

The design consequence: Militech has **one ladder and two exits**. The ladder is
corporate-military (recruit → specialist → officer → black ops → branch staff),
and both exits are loyalty failures: the *quiet* exit (Crane — help the person,
not the corp) and the *loud* exit (Hansen — take the hardware and the district).
A player who wants to run Militech has to buy the state, not the company.
`[inferred]`

---

## 2. Internal political factions

### 2.1 The blocs

"Members" counts below are **presence proxies** from `dist/extract/areas.jsonl`
and site rosters, not membership rolls. The Corpo Plaza and Detention Center
communities are overlapping phases/sites, so do not sum them.

| Bloc | Leader(s) | What it wants | Presence / members hint | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- |
| **The NUSA-captive board (the Pentagon bloc)** | Lucas Harford; the board's Defence Ministry seats | Keep the state-corporate fusion; 60%+ of contracts from Washington; no independence | Rosslyn HQ, Militech Tower; no in-game actors | Nationalisation; board members in the Ministry of Defense; D.C. is the largest customer `[wiki]` | `[wiki]` |
| **The Myers/Harford reformist-executive line** | Rosalind Myers (ex-CEO, president); Lucas Harford | Legitimacy and stability: "pragmatic and level-headed" policy, public patriotism, veteran philanthropy, peace on Militech's terms | Myers: `Character.myers` (31 phases); Harford: netpage only | Netpage leadership page; *Lucas Harford*; *Rosalind Myers*; `myers_default_dialog` `[game-data]` `[wiki]` | `[game-data]` `[wiki]` |
| **The Lundee martial wing (with a living heir)** | Donald Lundee Sr. (d.); Donald Lundee Jr. | Arms supremacy, a personal war with Arasaka, "make Militech the largest force on Earth"; contempt for the board's caution | Historical; Lundee Jr. is a current employee | *Donald Lundee* ("made more enemies than friends"; "personal power goals"); Lazarus disagreed with him; *Donald Lundee Jr.* `[wiki]` | `[wiki]` |
| **The Night City operations wing (Stout vs Gilchrist)** | Meredith Stout; Anthony Gilchrist | Stout: recover the convoy, prove the leak, keep the branch clean. Gilchrist: survive, keep the cut, be unprovable | Site 59 (Roider's squad, `faction_id 21`); All Foods communities; `{q003_*}` | *The Pickup* both branches; `Character.Stout`, `Character.Gilchrist`; shards on the convoy and Mallory `[game-data]` `[wiki]` | `[game-data]` `[wiki]` |
| **The Investigations / Intervention black-ops wing** | Keenan Thorston (Investigations); Elizabeth W. Roider (Intervention) | Protect Militech's political assets; bury scandals; use NCPD cover; leave no witnesses | Site 59 `ma_hey_gle_13` (5 units, ranger + MG gunner) | Shards *Extraction* and *Report, Extraction*; Roider's wiki biography `[game-data]` `[wiki]` | `[game-data]` `[wiki]` |
| **The Special Projects / Cynosure wing** | Mels Engelsson (2020); Dr. Evan McRay and the 2068 team | Weaponise the frontier; capture and harness rogue AIs; deniability above all — including killing its own exposed executives | Cynosure Site C and D (no coordinates); the Proving Grounds SPD (off-map) | *Project Cynosure*; *Cynosure Facility*; SPD assassination policy `[wiki]` `[inferred]` | `[wiki]` |
| **The seceded deserter wing (BARGHEST)** | Kurt Hansen; Albert Murphy and the ex-Militech inner circle | Independence, Dogtown, and the hardware they walked away with (Minotaurs, Centaurs, Behemoths, Chimeras, a Basilisk, a Blackwall AI) | Dogtown; `kurtz` community + 200+ Barghest records | *Dogtown – Analytical Summary* ("Militech deserters" a subject of interest); *BARGHEST* arsenal list; *Kurt Hansen* `[game-data]` `[wiki]` | `[game-data]` `[wiki]` |
| **Militech SiteSecure (commercial line)** | Unnamed | Contract security as a product: sell the army in small pieces | Night Corp maglev tunnel (site 350, Militech garrison) | *Maglev Tunnel Construction Site*: "Night Corp hired a subgroup of Militech called 'Militech SiteSecure'" `[game-data]` `[wiki]` | `[game-data]` `[wiki]` |

### 2.2 The nationalisation fault line

Militech's central internal contradiction is that **it is owned by its largest
customer.** That is not a metaphor:

- The NUSA nationalised it in 2023–24, using an ex-Militech president (Kress) to
  do it, and gave prominent Militech officials ministry posts. `[wiki]`
- Over 60% of contracts come from the NUSA; Washington is the largest consumer;
  if the capital runs out of money "the corporation would risk losing
  everything." `[wiki]`
- The last several US presidents were ex-Militech executives, and Myers is one of
  them. In the NUSA database entry's own words: "it's hard to tell where the
  state ends and the corporation begins." `[wiki]`
- The FIA — the president's intelligence service — is described by skeptics as
  "a secret weapon in her political games **against Militech**." `[wiki]`

That last line is the political fault line. Two readings coexist inside the
company and they imply opposite strategies:

1. **The fusionist reading (Harford).** The state is the customer, the owner and
   the shield. Serve it, staff it, and the company is unassailable. This is the
   board's position and the reason Militech is "itching for an excuse to send the
   armed cavalry into the city." `[wiki]`
2. **The sovereign reading (the Lundee wing, and Myers in her FIA mode).** A
   company that can be ordered to stand down — as Lundee was in 2023 — is not
   sovereign. The FIA exists partly to keep Militech honest; the deserter wing is
   what happens when the order to stand down is refused. `[wiki]`

For a simulation this is the cleanest driver: **every Militech internal conflict
can be scored as "serve the state" vs "own the state."** `[inferred]`

### 2.3 Stout vs Gilchrist: the branch war

This is the only Militech internal conflict the game dramatises, and it is a
near-perfect mirror of Arasaka's Jenkins/Abernathy feud.

- A company leak let **Maelstrom** hijack a convoy carrying a Flathead. Militech
  suspected inside knowledge. **Meredith Stout** found evidence pointing at
  **Anthony Gilchrist** but could not prove it. `[wiki]`
- Gilchrist was not a lone embezzler. He was Maelstrom's mole: he fed Brick's
  gang shipment details through Patricia and took a cut of the resale, and he
  finally leaked the security protocols of the Flathead convoy. He was also being
  blackmailed — Adam Smasher and Maelstrom held a woman named Mallory hostage to
  force his cooperation, and executed her aboard the *Ebunike*. `[wiki]`
- **The branch decides the outcome.** If V follows Stout's plan, she recovers
  most of the convoy, proves Gilchrist's guilt, and has him killed. If V refuses
  the chip or warns Royce, Gilchrist is promoted to head the investigation,
  replaces Stout's team with his own, and has Stout tortured, bound and drowned
  with concrete shoes in the Watson waterfront. `[wiki]` `[game-data]`
- **Either way the branch is decapitated.** One of the two senior operational
  figures dies, and the survivor inherits an investigation that has just killed a
  colleague. `[inferred]`

The bloc structure is therefore: **two managers, one investigation, one corpse.**
Militech does not purge by department (Arasaka) or by coup (Maelstrom); it purges
by *case closure*. `[inferred]`

### 2.4 The Investigations and Intervention wing

This is the bloc a player employee is most likely to meet, and the one that shows
how Militech actually does politics.

- **Keenan Thorston**, Deputy Director of Operations in the Investigations
  Department, ordered the detention and transfer of **Gerardo Estevez** because
  Estevez had information on **Javier Alvarado** — an advisor to interim mayor
  **Weldon Holt** — collaborating with the **Valentinos**. The stated purpose was
  to cover up the advisor's corruption. The order adds: "Any potential witnesses
  are to be permanently neutralized," and "The operation has been approved by the
  NCPD. There will be no police intervention." `[wiki]`
- **Elizabeth W. Roider**'s Intervention squad executed it at Valentino Alley.
  Estevez was armed and under Valentino protection, was repeatedly wounded in the
  shootout, and died despite Militech medical attention. The squad preserved his
  brain as evidence and began "eliminating traces of the incident, as well as
  executing the captured Valentino members." `[wiki]`
- The internal logic is explicit: Militech is **not** investigating a crime. It
  is managing a political asset (Alvarado) and a police relationship (the NCPD
  approval) by removing the person who could expose them. `[inferred]`

This is why Militech's *Espionage* weakness is not "bad at spying": it is that
the intelligence apparatus points **inward at domestic politicians** rather than
outward at rival corps, and that its tradecraft is loud enough (a street
firefight in the Glen, a massacre in Kabuki) to be handed to a fixer. `[inferred]`

### 2.5 Special Projects and Cynosure: the deniable wing

The Special Projects Department is the oldest and most paranoid bloc:

- It develops "ideas considered too exotic, sensitive, potentially dangerous, or
  PR-damaging for regular development channels," and "Militech has been known to
  order the assassination of some of its own lower executives who have been
  accidentally exposed to sensitive SPD data." `[wiki]`
- **Project Cynosure** is its 2077 descendant: Militech's answer to Soulkiller,
  built to capture and harness rogue AIs, run from a bunker under Night City
  (Site C). It was shuttered after the DataKrash, partially reactivated in 2068 by
  a team including Dr. Evan McRay and the Cassel twins, then cancelled again —
  partly because reactivation "would have been a breach of extant corporate
  treaties alongside international laws designed to keep rogue AIs from spilling
  out." `[wiki]`
- The program's own security is the internal-politics story: NetWatch and EBM
  logos appear on Cynosure decals, and one theory for the cancellation is that
  "Arasaka or NetWatch caught wind of the project's existence, forcing Militech
  to cover its tracks." `[wiki]`

The bloc's politics is therefore **deniability as a career**: an SPD executive's
success is invisible, and being *seen* is a death sentence. Model it as a
high-value, low-visibility faction that rewards secrecy and punishes exposure —
the opposite of the Lundee wing's public pride. `[inferred]`

### 2.6 The deserter wing: Hansen and BARGHEST

The most important thing that has happened to Militech's internal politics in
the 2070s is a **secession**:

- **Kurt Hansen** was a Militech colonel who rose "at a rapid pace," was given
  covert operations, and secured the NUSA's foothold in Night City as part of
  Operation Midnight Storm. When the war ended and the NUS government abandoned
  the unit, Hansen and his soldiers **deserted** and kept the district — Dogtown —
  as their own. `[wiki]`
- His inner circle is "mostly former Militech soldiers who served under him."
  Albert Murphy, a former Militech soldier, is one of the few surviving originals. `[wiki]`
- Dogtown is described by the FIA as "a former site of significant Militech
  investment," and its primary subjects of interest include "**Militech
  deserters**" and "remnants of Project Cynosure." `[wiki]`
- BARGHEST's arsenal is "predominately manufactured by Militech": Minotaurs,
  Centaurs, Mobile Missile Systems, Behemoth MT-3s, a Basilisk, at least two
  Chimeras, Wyverns and Manticores. Hansen also took a neural matrix and a
  Blackwall AI from an abandoned Militech bunker. `[wiki]`
- **Militech's records are still classified around him.** "Only top Militech execs
  and certain members of Congress in Washington have clearance to learn just who
  this former Colonel truly is." `[wiki]`

That is the strongest internal-politics fact in the whole faction: a Militech
colonel refused a stand-down order, walked off with a division's equipment and a
black site, and the company's response was to classify him rather than fight him.
For a simulation, this is the template for **the loyalty rupture**: a high-ranking
officer with a private army, legitimate grievances, and the corp's own hardware.
`[inferred]`

### 2.7 The veterans: the culture the corp sells and discards

Militech's public culture is patriotic paternalism, and its record is disposal:

- The CEO "footed the medical bill" of a Unification War veteran because "No
  American soldier deserves to suffer alone and die on the streets." `[wiki]`
- In the same 2077, Militech "has been shown to disregard veterans of their corp
  military after they retire, these veterans were often discovered without proper
  medication or were even massacred by Militech themselves," and its "rapid-response
  division" killed a network of extremists of whom "approximately 75% … were
  Japanese citizens." `[wiki]`
- Lt. Mower — a Militech lieutenant with military-grade implants — called a
  doctor for help with her cyberpsychosis and got a hit squad instead. She killed
  the squad. `[wiki]` `[game-data]`
- Employees get 50% off Militech weapons and the corp is ranked the second-best
  employer in Night City; it is also the corp that kills its own interns'
  killers' club and dumps its executives in the waterfront. `[wiki]`

This is a **legitimacy bloc** rather than an organised faction: the gap between
the slogan and the body count is a resource for anyone who wants to move against
the current leadership, and it is why Harford's paternalism reads as policy
rather than sentiment. `[inferred]`

### 2.8 What could drive internal conflict in a simulation

Evidence-based drivers, in rough order of plausibility:

1. **State vs company.** The board's fusionist line versus the Lundee/Myers
   sovereign line. Any NUSA order that costs Militech money (a stand-down, a
   treaty, a withdrawal) splits the company. Precedent: Kress ordering Lundee to
   cease hostilities in 2023. `[wiki]`
2. **A loyalty rupture.** A senior officer with a private army and a grievance
   leaves and takes the hardware (Hansen). The corp's answer is classification,
   not confrontation — which invites the next one. `[wiki]`
3. **Case closure as purge.** Stout vs Gilchrist shows that one investigation can
   kill a senior manager. Whoever controls the case controls the branch. `[wiki]`
4. **Deniability.** SPD/Cynosure rewards invisibility and assassinates exposed
   executives. A leak (NetWatch, EBM, Arasaka) is an internal death sentence. `[wiki]`
5. **Political-policing blowback.** Thorston's NCPD-approved extraction executed
   Valentinos and left a brain in a jar; the same operation is handed to fixers.
   Every clean-up creates a witness. `[game-data]` `[wiki]`
6. **The veterans' ledger.** Harford's public paternalism versus the documented
   disposal record. A player who publicises the gap damages the reformist bloc
   without firing a shot. `[wiki]`
7. **Board capture.** 8% + 22% left a controlling bloc exposed in 2020; in 2077
   the state holds the controlling interest. Whoever moves the state moves the
   company. `[wiki]`
8. **Which Arasaka policy to have.** Lundee's personal vendetta versus the board's
   caution is the oldest split in the company, and the Fourth Corporate War is
   what happened when the vendetta won. `[wiki]`

---

## 3. External relations matrix

### 3.1 Stance vocabulary and direction

One stance per row, read **from Militech's side**, following the precedence in
`METHOD.md` §3: explicit violence first, then explicit transaction, then
quest-giver role, then adjacency, then a neutral placeholder.

| Stance | Meaning (from Militech's side) |
| --- | --- |
| `war` | Open, active armed conflict over turf or existence |
| `hostile` | Actively targets or raids the other side, but not a declared turf war |
| `rival` | Turf or economic competition, with skirmishes |
| `neutral` | No attested interaction; not an ally |
| `trade` | Transactional exchange, no loyalty |
| `ally` | Coordinated support or shared operations |
| `patron` | This faction protects or funds the other |
| `client` | This faction depends on or works for the other |

Two direction notes, because the generic vocabulary is broken for a
nationalised arms dealer:

- **`patron` is used for the NUSA only, and it is a poor fit.** The NUSA funds,
  owns and protects Militech; Militech in turn supplies, staffs and effectively
  runs the NUSA. `patron` records the formal dependency (the state can order a
  stand-down), not the real leverage. Read the evidence string for the circularity.
- **Militech has no `client` row.** It works for Night Corp (SiteSecure) and
  Kiroshi (executive protection), but those are commercial contracts, not
  dependencies. The vocabulary has no `supplier`/`contractor`, so all buyer-side
  relationships collapse into `trade`. This is a METHOD gap (§5).

There is **no usable offline attitude matrix**: `Attitude_Record.hpp` is opaque
and `Affiliation.hpp` is identity only. Every stance below is judged from quests,
wiki and spatial adjacency, which is why each row carries a tag and why the
neutral rows are placeholders, not claims of friendship.

### 3.2 The matrix

| Faction | Code | Stance | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| Tyger Claws | `tyger_claws` | `neutral` | No attested interaction. The Claws are Arasaka's proxy (close ties to Arasaka management, sleeper agents), and no Militech gig targets them. The JapanTown netrunner parking-lot site is adjacency only `[game-data]` `[inferred]` | `game-data+inferred` |
| Valentinos | `valentinos` | `hostile` | Thorston's Intervention squad executed Valentino members and killed a Valentino-protected informant at Valentino Alley; Militech was investigating a Valentino–City Hall corruption link; the gang fences stolen Militech vehicles `[game-data]` `[wiki]` | `game-data+wiki` |
| Arasaka | `arasaka` | `rival` | Fourth Corporate War (2022–25); Unification War (2069–70) on opposite sides; Militech Offices faces Arasaka Tower across Corpo Plaza; 2077 mutual sabotage and Smasher's blackmail of a Militech employee `[game-data]` `[wiki]` | `game-data+wiki` |
| Kang Tao | `kang_tao` | `rival` | Arms-manufacturing competitors; Kang Tao's Corpo Plaza North Tower is a neighbour; a Kang Tao detail stands on Militech's own HQ-concourse sub-territory (`ma_cct_cpz_15`, 269 m from Militech's CC) `[game-data]` `[wiki]` `[inferred]` | `game-data+wiki+inferred` |
| Biotechnica | `biotechnica` | `trade` | Biotechnica supplied both sides in the Fourth Corporate War, with Arasaka getting the exclusives; Militech remained a customer. A supplier relationship, no 2077 conflict `[wiki]` | `wiki` |
| Petrochem | `petrochem` | `trade` | Petrochem sells Militech rocket propellants, advanced materials and CHOOH2 at bulk discount while competing with it in chemical weapons — "stiff competition … has not stopped it from marketing" `[wiki]` | `wiki` |
| Barghest | `barghest` | `hostile` | A Militech colonel's deserter army holds a former Militech investment site, a Militech bunker, a Blackwall AI and a Militech-manufactured arsenal; Militech deserters are an FIA subject of interest. Doctrinal hostility, not a 2077 firefight `[game-data]` `[wiki]` | `game-data+wiki+inferred` |
| 6th Street | `sixth_street` | `trade` | The gang was historically "supplied by Militech and Kendachi" with cyberware and weapons; in 2077 the Megabuilding H6 cell "jumped a Militech transport" and jailbreaks corpo weapons. A supply channel with a predation problem `[wiki]` | `wiki` |
| Aldecaldos | `aldecaldos` | `hostile` | The Sunshine Motel outpost field-tests an anti-nomad mobile radar (`P9D/2.161`) that the Aldecaldos want to reverse-engineer so nomads can cross unseen; Militech's detention centre holds border crossers; Militech's veteran massacres have "lend to a poor relationship with the various nomads" `[game-data]` `[wiki]` | `game-data+wiki` |
| Wraiths | `wraiths` | `hostile` | Militech executes captured Wraiths (`cs_militech_execution*`, `cs_handcuffed_wraiths_militech*`, an execution scene with a Wraith `victim`); Wraith cells prey on Militech convoys and hold the outpost's neighbourhood `[game-data]` `[wiki]` | `game-data+wiki` |
| Animals | `animals` | `hostile` | An Animals club boss ordered Seamus Sawicki to kill a group of Militech interns who had hurt the club's joygirls; Animals-run Data Inc. sells hacked, previously stolen Militech hardware at markup, which is exactly the crackdown trigger Rogue fears `[game-data]` `[wiki]` | `game-data+wiki` |
| The Mox | `the_mox` | `neutral` | No attested interaction; the Mox are a Watson sex-worker collective with no Militech contract or incident `[inferred]` | `inferred` |
| Maelstrom | `maelstrom` | `hostile` | Maelstrom hijacked a Militech convoy through Gilchrist, stole the Flathead, and Militech raided All Foods in *The Pickup*; Smasher and Maelstrom held Mallory hostage to blackmail Gilchrist `[game-data]` `[wiki]` | `game-data+wiki` |
| Voodoo Boys | `voodoo_boys` | `rival` | Voodoo Boys espionage targets corporate databanks, and Militech combat robots were found at the Luxor spa; a NetWatch report flagged possible corporate sabotage. No direct firefight attested `[game-data]` `[wiki]` | `game-data+wiki` |
| NCPD | `ncpd` | `trade` | Militech is an NCPD sponsor and creditor ("beholden to the interests of Arasaka and Militech") and its equipment supplier (Lexington sidearm, Saratoga, Ajax, Minotaur mechs, Wyvern/Griffin drones, Centaur exoskeletons); an illegal Militech extraction proceeded with explicit NCPD approval and "no police intervention" `[game-data]` `[wiki]` | `game-data+wiki` |
| Night Corp | `night_corp` | `trade` | Night Corp lost the influence race to Arasaka and Militech but still hired **Militech SiteSecure** to protect its maglev tunnel (site 350 garrison is Militech). Commercial security contract inside a rivalry `[game-data]` `[wiki]` | `game-data+wiki` |
| City Council | `city_council` | `trade` | A Night City councillor assassinated by a merc had "deep ties to Militech," and Militech moved to scapegoat the killer to bury the corruption; the branch also runs an NCPD-approved extraction against a mayoral advisor. Purchased influence, no loyalty `[game-data]` `[wiki]` | `game-data+wiki` |
| Scavengers | `scavengers` | `neutral` | No attested interaction; Militech security would treat scavs as criminals, but no specific event or site is shared `[inferred]` | `inferred` |
| Regina Jones | `fixer_regina` | `hostile` | Regina gives *Concrete Cage Trap* (Militech's armoured raid on a Kabuki block hunting a data thief) and the Lt. Mower cyberpsycho sighting, where Militech's own hit squad is the villain `[game-data]` `[wiki]` | `game-data+wiki` |
| Wakako Okada | `fixer_wakako` | `neutral` | No Militech-specific gig or lore link found `[inferred]` | `inferred` |
| Sebastian Ibarra (Padre) | `fixer_padre` | `hostile` | *Eye for an Eye* targets a Kiroshi executive whose apartment is held by eight Militech guards, so the contract puts V against Militech personnel. Incidental executive protection, not an anti-Militech campaign `[game-data]` `[wiki]` | `game-data+wiki` |
| Muamar Reyes (El Capitán) | `fixer_el_capitan` | `neutral` | No Militech-specific gig or lore link found; his antipathy is toward Arasaka `[inferred]` | `inferred` |
| Dakota Smith | `fixer_dakota` | `hostile` | Dakota gives all three anti-Militech Badlands gigs: *Radar Love* (outpost radar), *Goodbye, Night City* (detention centre), and *MIA* (Militech buying a merc to bury a councillor's corruption) `[game-data]` `[wiki]` | `game-data+wiki` |
| Dino Dinovic | `fixer_dino` | `hostile` | *The Frolics of Councilwoman Cole* has Militech as the enemy at the Militech-contracted Gold Beach Marina; the client is a corpo who wants dirt on an anti-corporate councilwoman `[game-data]` `[wiki]` | `game-data+wiki` |
| Rogue Amendiares | `fixer_rogue` | `neutral` | *Hot Merchandise* is not an attack on Militech: Rogue kills a business selling stolen Militech guns **to prevent** "Militech cracking down on the city." She treats Militech as a force to be placated, not an enemy `[game-data]` `[wiki]` | `game-data+wiki` |
| Mr. Hands | `fixer_mr_hands` | `neutral` | No anti-Militech gig found; his Dogtown work runs through BARGHEST and the FIA. The Heavy Hearts Militech "business contact" is a club fixture, not a channel `[game-data]` `[inferred]` | `game-data+inferred` |
| Afterlife | `afterlife` | `neutral` | Neutral merc marketplace; Militech hires mercenaries as a business, but no Afterlife-specific arrangement is attested `[inferred]` | `inferred` |
| NUSA | `nusa` | `patron` | The NUSA nationalised Militech, owns the controlling interest, provides 60%+ of contracts, staffs its board with Defence Ministry officials, and has supplied its last several presidents — while retaining the power to order it to stand down. Owner, customer and regulator in one `[wiki]` | `wiki` |
| NetWatch | `netwatch` | `rival` | NetWatch is the enforcement body for the Blackwall regime that a Cynosure reactivation would breach; NetWatch (and EBM) logos appear on Cynosure decals, and one explanation for the project's burial is that NetWatch caught wind of it. Regulatory rivalry, no attested skirmish `[wiki]` | `wiki+inferred` |
| Zetatech | `zetatech` | `trade` | Militech arms and retrofits Zetatech airframes; the Valgus remains in service with Militech. Supplier relationship `[wiki]` | `wiki` |
| Trauma Team | `trauma_team` | `trade` | Trauma Team partners with Militech and gives its employees memberships without their paying; during the 4CW it refused to respond to Militech *or* Arasaka alerts `[wiki]` | `wiki` |
| News 54 | `news54` | `ally` | NN54 has "a noticeable pro-Militech bias," explicitly opposed to the pro-Arasaka WNS, and ran Militech's NCPD partnership signing and Harford's veteran story. Editorial alignment, not an operational alliance `[wiki]` | `wiki` |
| Kiroshi Optics | `kiroshi` | `trade` | Militech provides the executive-protection detail for a Kiroshi vice managing director (8 Militech guards at site 364 `sts_hey_gle_01`); Kiroshi is the customer `[game-data]` `[wiki]` | `game-data+wiki` |

Stance counts (**33 rows**): **hostile 10, trade 9, neutral 8, rival 4,
patron 1, ally 1, client 0, war 0.**

The three that matter most for the mod:

- **`arasaka` — `rival`.** The defining relationship: two wars, adjacent towers,
  mutual sabotage, and a 2077 cold war that neither side wants to heat up. This
  is the axis every other Militech stance is read against.
- **`nusa` — `patron`.** The relationship that makes Militech unlike every other
  corp: its owner is its customer and its regulator, and the FIA may be aimed at
  it. Any player organisation dealing with Militech is dealing with the NUSA.
- **`barghest` — `hostile`.** The relationship that shows the faction's fracture:
  its own deserters hold its own black site with its own arsenal. This is the
  best template for a player-founded splinter.

### 3.3 Actors outside `data/factions.json`

Real relationships with no faction code, so prose only:

- **Lazarus Group** — Militech's closest corporate ally in the 2010s: it bought
  "millions of dollars' worth" of Militech equipment annually, and Emile Lazarus
  and Donald Lundee were personal friends. Lazarus disagreed with Lundee's
  Arasaka vendetta, and by 2045 Lazarus had become "the heir to Arasaka and
  Militech's status as the largest security service in Night City." Militech also
  refers contract overflow to Lazarus. Treat as a friendly supplier-client
  relationship, not an alliance. `[wiki]`
- **Nova Arms** — a revolver manufacturer that was an Arasaka subsidiary until
  Militech "captured and forcefully subsidised" it during the Fourth Corporate
  War. A captured competitor now inside the company: a piece of internal politics
  as much as an asset. `[wiki]`
- **Silva-Scherer** — Militech signed a deal to buy 35 Manticore AVs from it,
  justified publicly by nomad "ecoterrorists" in the Amazon Plains. `[wiki]`
- **Emile Lazarus** — founder of the Lazarus Group and Lundee's friend; the
  personal brake on the Arasaka vendetta. `[wiki]`
- **Javier Alvarado** — advisor to interim mayor Weldon Holt; the Valentinos
  corruption link Militech was covering up. `[wiki]`
- **Gerardo Estevez** — the Valentino-protected informant Militech killed and
  whose brain it preserved. `[wiki]`
- **Anthony Gilchrist's blackmailers** — Adam Smasher and Maelstrom, holding
  Mallory hostage. An Arasaka employee personally owning a Militech employee is
  the sharpest single fact about Militech's counter-intelligence. `[wiki]`
- **Albert Murphy and Hansen's inner circle** — ex-Militech soldiers, now
  BARGHEST's leadership. `[wiki]`
- **Dr. Martin Sypura** — the physician Mower called for help; whether he sent the
  hit squad is not stated. `[wiki]`
- **Michael Maldonado** — the Heavy Hearts client; his club contact is a Militech
  "business contact," not a channel. `[wiki]`
- **Tiny Mike** — stole data from a "Militech lab in the Badlands" for Regina;
  the lab has no location record (§5). `[wiki]`
- **Night Corp Solar Farm / PacCon Electric** — the seed credits the Jackson
  Plains arrays to Militech; they belong to Night Corp and PacCon. Not a
  relationship, a data error inherited from the location doc. `[wiki]`
- **The NorCal-SoCal Border Patrol** — Militech's partner at the border crossing
  and detention centre ("security_provider = SoCal Border Patrol / Militech"). `[wiki]`

### 3.4 Guarantor assessment

The design question: if a player founds an organisation, which factions would
guarantee Militech's support, and which would Militech guarantee?

- **Militech is the best-armed guarantor in the game and the worst ally to have.**
  It has one `ally` (a television network) and one `patron` (the state that owns
  it). Everything else is a contract, a rivalry or an active hostility. A player
  who takes Militech's support inherits Arasaka, the Aldecaldos, the Wraiths,
  Maelstrom, the Animals, four fixers and possibly the NCPD. `[inferred]`
- **The plausible guarantors for a player-founded organisation** are therefore
  *branch-level and individual*, not corporate:
  - a corrupt NCPD channel approved at deputy-director level (Thorston-type);
  - `Militech SiteSecure` as a paid contract — the one Militech relationship
    that is designed to be sold to a third party (Night Corp's maglev tunnel);
  - a Night City operations manager who owes the player a case (Stout-type);
  - NN54 editorial cover, which is free if the player's enemy is Arasaka.
  All four are transactional. None is a corporate alliance. `[inferred]`
- **Militech as an aggressor is the more likely configuration.** For a player
  founding an organisation on any Militech-held point, Militech is the
  **pre-emptive attacker**: it raids (All Foods), it extracts (Valentino Alley),
  it sends hit squads at its own people (Mower), and it hires mercs to bury
  scandals (MIA). Its hostility rows are the ones to model, not its ally row. `[inferred]`
- **The one structural exception is the state.** If the player's organisation can
  obtain NUSA sanction, Militech's `patron` row means the corp cannot move
  against it openly — which is exactly why Myers's FIA is the more interesting
  lever than Militech's board. `[inferred]`

---

## 4. Pillar notes

Design claims from `docs/design/gameplay-systems.md`: Militech is a
**Corporation** (archetype strength **Technology**, weakness **Culture**);
faction strength **Military**, weakness **Espionage**.

| Pillar | Design claim | Lore verdict | Evidence |
| --- | --- | --- | --- |
| Technology (archetype strength) | Corporations are technology-led | **Strongly supported, with a specific shape.** Militech's edge is *applied* military technology at scale — the world's largest small-arms catalogue, drones, mechs, APCs, AVs, the Flathead, and the Cynosure rogue-AI program. It is not a consumer-tech or cyberware innovator; Arasaka owns the Relic/Soulkiller frontier. Militech's technology is *deniable weapons*, not transcendent ones. | Products list (82 countries, 250+ corps); Cynosure; the Flathead convoy; Wyvern/Griffin/Centaur/Minotaur/Behemoth/Chimera; the P9D radar `[wiki]` `[game-data]` |
| Culture (archetype weakness) | Corporations are culturally weak | **Supported, with a sharp twist.** Militech has a *loud* culture — flags, veterans, "no soldier left behind," 50%-off weapons, best-employer awards — but it is **borrowed national identity**, not a company identity. It binds in-group Americans and repels everyone else (75% of a massacre's victims were Japanese), and internally it is instrumental: veterans dumped, officers executed, a colonel's whole division allowed to walk away. It does not survive contact with a payroll decision. | Netpage careers and newsroom; Big 5 shard; veterans massacre; Mower; Hansen; 75%-Japanese massacre `[wiki]` |
| Military (faction strength) | Militech is a military power | **Strongly supported, but read it as mass, not elite.** 100,000 corporate troops in 2020, 90% line infantry and specialists, only 10% special ops — and those are **never subcontracted**, retained for the corp's own use. Militech hires out "all-purpose, line soldiers" from 100 to 10,000 and refers anyone wanting specialists to Lazarus. So: enormous firepower and logistics, deliberately shallow special-ops bench. | *Militech* Human Resources and Mercenary Troops sections; BARGHEST's Militech arsenal; the NUSA's army `[wiki]` |
| Espionage (faction weakness) | Militech is weak at espionage | **Supported, and precisely diagnosable.** Militech is penetrated constantly: Gilchrist the mole, Smasher blackmailing Gilchrist through Mallory, Tiny Mike stealing lab data, Voodoo Boys stealing corporate data, the Aldecaldos stealing the radar, a whole deserter division taking a bunker, and Cynosure leaking to NetWatch/EBM. Its counter-intelligence is *domestic political policing* (Thorston's Investigations, Roider's Intervention), not foreign tradecraft — it is loud, NCPD-approved and gets handed to fixers. Model it as **high internal surveillance, low operational secrecy**. | *The Pickup*; Gilchrist/Mallory; *Project Cynosure*; *Concrete Cage Trap*; *Radar Love*; Thorston's extraction order `[game-data]` `[wiki]` |
| Overall fit | The pillars fit the corp's identity | **Good for identity, excellent for the mod's theme.** A state-owned arms dealer that is unbeatable in a firefight and porous in a conspiracy is the cleanest possible "Corporation / Military / Espionage" fit. Keep Military strong, Espionage weak, Technology strong, Culture as borrowed patriotism. | Synthesis `[inferred]` |

Design cautions, not redesigns:

- **Do not model Militech as a normal megacorp.** It has no bank, no independent
  board, and a head of state as its patron. Any economy or politics layer that
  treats it like Arasaka will get the incentives backwards: Arasaka competes for
  the state, Militech *is* the state's supplier and is partly owned by it.
- **Do not model Culture as zero.** The patriotism is real and it recruits. Model
  it as **high internal pride, low external legitimacy, zero resilience under
  cost pressure** — the exact inverse of Arasaka's coercive samurai culture.
- **Do not model Espionage as "no spies."** Militech has an Investigations
  Department that can order an NCPD-approved kidnapping. It is weak at *secrecy*,
  not at *surveillance*. The distinction is the whole faction.
- **The deserter wing is the best splinter template in the game.** A player who
  founds a rival organisation out of Militech should get the Hansen pattern: an
  officer, a grievance, a stand-down order, and the corp's own hardware.

---

## 5. Gaps and uncertainties

1. **No offline attitude matrix.** `Attitude_Record.hpp` is opaque and
   `Affiliation.hpp` is identity only. Every stance in §3.2 is judged from quests,
   wiki and spatial adjacency; none is read from a TweakDB relation row.
2. **No named Militech leader is ambient.** The only named Militech people with
   records are Roider and Mower, both `world-activity` enemies, and both
   mid-level. The CEO, the board and the branch's directors are `story` or
   `off-map`. A simulation must supply the leadership, not find it.
3. **Harford exists only in prose.** Three sentences and four netpage lines, no
   record, no location, no scene. He is the least-characterised 2077 megacorp CEO
   in the game and cannot be seeded as an actor.
4. **The Myers handover date conflicts inside the wiki.** The CEO infobox says
   Myers 2060–2069; the *Rosalind Myers* body says she left Militech "in 2065" to
   run for president; the *Militech* article says 2069. This document uses 2069
   and flags it; do not build a timeline on either date without a third source.
5. **Kress's title conflicts.** The CEO infobox lists her as CEO ("?–2020"); the
   body calls her "an ex-president of Militech." She is also the US/NUSA president
   who nationalised the company. Treat "CEO" as uncertain and "president of
   Militech, then of the NUSA" as established.
6. **The 2077 board has no individual records.** Roland Yee and the 2020 board
   are the only named directors, and they are `historical`. The JSON entry uses
   `character_record_id: null`.
7. **`Character.ma_wat_kab_08_cyberpsycho` → Lt. Mower is inferred.** Three
   signals agree (site baseid, `faction_id 21`, the ORDERS shard) but the record
   is a generic psycho slot. Verify in game.
8. **Arden Bentzen is unresolved.** `Character.sts_bls_ina_101_arden_bentzen` is
   the only capitalised named record in a Militech-faction community besides
   Roider, but it sits in a slot named `joshua`, has no wiki page, and appears
   with six `sts_bls_ina_101_miltech_security` guards at the Detention Center
   variant (site 348). He may be a detainee, an officer, or a reused slot. Do not
   seed him.
9. **`Character.kurtz` is Hansen, and the name is a substring trap.** `hansen`
   appears nowhere in the raw registry; `kurt*` matches 200+ Barghest soldiers.
   Use the exact entry `kurtz`.
10. **Militech's Corpo Plaza HQ has no interior.** The wiki describes a lobby,
    showroom, cafeteria and a small military-technology museum, but in 2077 only
    "a couple of barred off elevators" lead to "an unfinished small area." The
    extract has no interior site, doors or guard volumes for the tower — only the
    concourse scanner hustle (`ma_cct_cpz_06`). Do not promise a multi-floor
    capture volume (this is also the location doc's §8.3).
11. **The Special Projects Department and the proving grounds are off-map.**
    Engelsson's SPD, the New Mexico Proving Grounds, the Laconia small-arms R&D
    and the Norfolk facility are all 2020 lore with no 2077 records. Prose only.
12. **Cynosure has no coordinates.** No marker, site, community or raw-sector
    string contains "cynosure"; the location doc places Sites C and D in Dogtown
    by inference from Site D's Longshore Stacks access. The internal-politics
    chapter treats it as `TBD` real estate.
13. **The "Militech lab in the Badlands" has no location.** *Concrete Cage Trap*
    says Tiny Mike stole data from one; no site, marker or wiki page names it.
14. **The veterans massacres are unquantified.** The wiki gives one number (75%
    of one operation's victims were Japanese) and no place, date or unit. Do not
    build a mechanic on a body count that is not stated.
15. **Militech's `client` row is missing by vocabulary, not by evidence.**
    SiteSecure works for Night Corp; the Corpo Plaza detail works for Kiroshi;
    the company sells police services to US cities. All read as `trade`. The
    stance set needs `supplier`/`contractor`.
16. **The `nusa` `patron` row is directionally ambiguous.** The NUSA owns and
    funds Militech; Militech also staffs and effectively runs the NUSA. `patron`
    records the formal dependency only. This is the strongest example of the
    METHOD's §1.1 item 6 problem.
17. **The `barghest` `hostile` row is doctrinal, not a 2077 firefight.** No
    in-game Militech-vs-Barghest combat is attested; the stance is the corporate
    view of deserters holding Militech property. It was assigned against
    METHOD §3's precedence ladder and is flagged.
18. **`sixth_street` is `trade`, not `rival`.** The Arasaka doc reads 6th Street
    as `rival` on ideology and adjacency; for Militech there is an attested supply
    relationship plus one cell's hijack, so `trade` is the better fit. The two
    documents are not inconsistent — they read the same gang from different sides.
19. **`fixer_padre` is `hostile` on mechanical grounds only.** *Eye for an Eye*'s
    enemies are Militech guards protecting a Kiroshi executive; Padre is not
    running an anti-Militech campaign. Flagged in the evidence string.
20. **`fixer_rogue` is `neutral` and it matters.** *Hot Merchandise* looks like an
    anti-Militech gig but is the opposite: Rogue kills a business to *prevent*
    Militech's crackdown. Reading the quest title rather than the dialogue
    inverts this row.
21. **Co-occurrence is weak evidence.** The Corpo Plaza and Detention Center
    communities are overlapping quest phases and sites (`sts_bls_ina_05` and
    `sts_bls_ina_101` are 32 m apart, same control centre 89); do not sum them.
22. **"Open world with the campaign disabled" is a heuristic.** The `story` rows
    are definitely not ambient; the `world-activity` rows need an in-game spawn
    check, and the mod may suppress gigs and hustles along with the campaign.
23. **Militech has no prologue presence at all.** The Corpo lifepath is Arasaka's
    `q000_corpo_*`. Any "join Militech as an employee" path has to be built, not
    reused — the best available template is the branch's documented chain
    (Stout → Thorston → Roider) rather than a playable intro.
24. **Several rows are omitted for lack of evidence.** Kendachi, Budget Arms,
    Orbital Air and Delamain have no attested Militech interaction and are not in
    the matrix, rather than being added as neutral padding.

### 5.1 Sources consulted

Local:

- `data/sites/rosters.json` — 159 Militech units, 65 distinct records; two named
  people (`Elizabeth_Roider`, `ma_wat_kab_08_cyberpsycho`); the `bruce`,
  `archibald`, `joshua`/`arden_bentzen` detention-centre slots.
- `data/sites/sites.json` — sites 11, 12, 40, 59, 177, 342, 343, 348, 354, 364,
  and their `default_faction_id`, `control_center_id`, `source_path`.
- `dist/extract/markers.jsonl` — `q003_01_sm_call_militech`,
  `q003_03a_sm_militech_invades`, `q003_08_sm_stout`, `{q003_mp_militech_meeting}`,
  `{q003_mp_no_tell_stout}`, `Ina_04_mp_outpost`, `ina_05_*`.
- `dist/extract/areas.jsonl` — 136 Militech areas / 701 entries; Badlands
  `cs_*` events, the `q114` set pieces, `q301`–`q307` Phantom Liberty.
- `dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_1.streamingsector.json`
  — the `worldCommunityRegistryNode`: entries and phases for `myers`, `stout`,
  `gilchrist`, `meredith_holo`, `anthony_gilchrist_holo`, `kurtz`, `bruce`,
  `archibald`, and the `q114_militech_*` / `q30x_militech_*` records.
- `data/factions.json` — faction codes used in the matrix.
- `docs/design/gameplay-systems.md` — archetype and pillar claims.
- `docs/research/factions/militech.md` — location catalogue, HQ, sub-territories.
- `docs/research/factions/METHOD.md` §1.1–§1.2 — data pitfalls.
- `docs/research/factions/politics/METHOD.md` — politics method.
- Other faction docs read for cross-incidents: `politics/arasaka.md`,
  `politics/maelstrom.md`, `politics/valentinos.md`, `politics/voodoo-boys.md`,
  `wraiths.md`, `sixth-street.md`, `animals.md`, `night-corp.md`,
  `aldecaldos.md`, `barghest.md`, `ncpd.md`, `biotechnica.md`, `petrochem.md`,
  `kang-tao.md`.

Wiki (MediaWiki API, `action=parse&prop=wikitext`, 2026-11-25):

- [Militech](https://cyberpunk.fandom.com/wiki/Militech) ·
  [Militech/Netpage](https://cyberpunk.fandom.com/wiki/Militech/Netpage) ·
  [List of Militech employees](https://cyberpunk.fandom.com/wiki/List_of_Militech_employees)
- [Lucas Harford](https://cyberpunk.fandom.com/wiki/Lucas_Harford) ·
  [Rosalind Myers](https://cyberpunk.fandom.com/wiki/Rosalind_Myers) ·
  [Donald Lundee](https://cyberpunk.fandom.com/wiki/Donald_Lundee) ·
  [Donald Lundee Jr.](https://cyberpunk.fandom.com/wiki/Donald_Lundee_Jr.) ·
  [Elizabeth Kress](https://cyberpunk.fandom.com/wiki/Elizabeth_Kress) ·
  [Roland Yee](https://cyberpunk.fandom.com/wiki/Roland_Yee) ·
  [Samantha Lee Young](https://cyberpunk.fandom.com/wiki/Samantha_Lee_Young)
- [Meredith Stout](https://cyberpunk.fandom.com/wiki/Meredith_Stout) ·
  [Anthony Gilchrist](https://cyberpunk.fandom.com/wiki/Anthony_Gilchrist) ·
  [Elizabeth W. Roider](https://cyberpunk.fandom.com/wiki/Elizabeth_W._Roider) ·
  [Mower](https://cyberpunk.fandom.com/wiki/Mower) ·
  [Archibald Crane](https://cyberpunk.fandom.com/wiki/Archibald_Crane) ·
  [Bruce Welby](https://cyberpunk.fandom.com/wiki/Bruce_Welby) ·
  [Kurt Hansen](https://cyberpunk.fandom.com/wiki/Kurt_Hansen) ·
  [Albert Murphy](https://cyberpunk.fandom.com/wiki/Albert_Murphy)
- [Militech Offices (2077)](https://cyberpunk.fandom.com/wiki/Militech_Offices_(2077)) ·
  [Militech Detention Center](https://cyberpunk.fandom.com/wiki/Militech_Detention_Center) ·
  [Sunshine Motel](https://cyberpunk.fandom.com/wiki/Sunshine_Motel) ·
  [Gold Beach Marina](https://cyberpunk.fandom.com/wiki/Gold_Beach_Marina) ·
  [Cynosure Facility](https://cyberpunk.fandom.com/wiki/Cynosure_Facility) ·
  [Project Cynosure](https://cyberpunk.fandom.com/wiki/Project_Cynosure) ·
  [Dogtown](https://cyberpunk.fandom.com/wiki/Dogtown) ·
  [BARGHEST](https://cyberpunk.fandom.com/wiki/BARGHEST) ·
  [Maglev Tunnel Construction Site](https://cyberpunk.fandom.com/wiki/Maglev_Tunnel_Construction_Site) ·
  [Nova Arms](https://cyberpunk.fandom.com/wiki/Nova_Arms) ·
  [Lazarus Group](https://cyberpunk.fandom.com/wiki/Lazarus_Group)
- [NUSA](https://cyberpunk.fandom.com/wiki/NUSA) ·
  [Federal Intelligence Agency](https://cyberpunk.fandom.com/wiki/Federal_Intelligence_Agency) ·
  [NetWatch](https://cyberpunk.fandom.com/wiki/NetWatch) ·
  [Night City Police Department](https://cyberpunk.fandom.com/wiki/Night_City_Police_Department) ·
  [Night Corp](https://cyberpunk.fandom.com/wiki/Night_Corp) ·
  [Unification War](https://cyberpunk.fandom.com/wiki/Unification_War) ·
  [Network News 54](https://cyberpunk.fandom.com/wiki/Network_News_54) ·
  [Petrochem](https://cyberpunk.fandom.com/wiki/Petrochem) ·
  [Biotechnica](https://cyberpunk.fandom.com/wiki/Biotechnica) ·
  [Zetatech](https://cyberpunk.fandom.com/wiki/Zetatech) ·
  [Trauma Team](https://cyberpunk.fandom.com/wiki/Trauma_Team) ·
  [6th Street](https://cyberpunk.fandom.com/wiki/6th_Street) ·
  [Seamus Sawicki](https://cyberpunk.fandom.com/wiki/Seamus_Sawicki)
- Quests and shards: [The Pickup](https://cyberpunk.fandom.com/wiki/The_Pickup) ·
  [Gig: Radar Love](https://cyberpunk.fandom.com/wiki/Gig:_Radar_Love) ·
  [Gig: Goodbye, Night City](https://cyberpunk.fandom.com/wiki/Gig:_Goodbye,_Night_City) ·
  [Gig: MIA](https://cyberpunk.fandom.com/wiki/Gig:_MIA) ·
  [Gig: Concrete Cage Trap](https://cyberpunk.fandom.com/wiki/Gig:_Concrete_Cage_Trap) ·
  [Gig: Eye for an Eye](https://cyberpunk.fandom.com/wiki/Gig:_Eye_for_an_Eye) ·
  [Gig: The Frolics of Councilwoman Cole](https://cyberpunk.fandom.com/wiki/Gig:_The_Frolics_of_Councilwoman_Cole) ·
  [Gig: Hot Merchandise](https://cyberpunk.fandom.com/wiki/Gig:_Hot_Merchandise) ·
  [Cyberpsycho Sighting: Lt. Mower](https://cyberpunk.fandom.com/wiki/Cyberpsycho_Sighting:_Lt._Mower) ·
  [Extraction #NC/EX/56/882](https://cyberpunk.fandom.com/wiki/Extraction_NC/EX/56/882) ·
  [Detainee Management Handbook](https://cyberpunk.fandom.com/wiki/Detainee_Management_Handbook) ·
  [Big 5 Employers in Night City – 2077](https://cyberpunk.fandom.com/wiki/Big_5_Employers_in_Night_City_%E2%80%93_2077) ·
  [ORDERS](https://cyberpunk.fandom.com/wiki/ORDERS_(ma_wat_kab_08)) ·
  [Dogtown – Analytical Summary](https://cyberpunk.fandom.com/wiki/Dogtown_%E2%80%93_Analytical_Summary)

---

## 6. Machine-readable block

```json
{
  "faction_code": "militech",
  "leaders": [
    {
      "name": "Lucas Harford",
      "role": "CEO (2069-2077); Myers's successor and political ally",
      "character_record_id": null,
      "location_name": "Rosslyn HQ, Virginia / Militech Tower, Washington D.C.",
      "open_world": false,
      "source": "wiki Militech CEO infobox; wiki Lucas Harford; netpage NETdir://militech.corp/leadership",
      "confidence": "wiki"
    },
    {
      "name": "Rosalind Myers",
      "role": "Former CEO (2060-2069); NUSA President (2065-, third term in 2077); Militech's political patron",
      "character_record_id": "Character.myers",
      "location_name": "Dogtown crash corridor / Kress Street Hideout / border crossing",
      "open_world": false,
      "source": "raw always_loaded_1 registry entry myers (phases myers_default_dialog, q301_06a_myers, q302_01_start, q302_07_myers_oath_combat, q305_11_border_crossing, q306_myers_epilogue_bench); Character.myers_hallucination; Character.q302_spidertank_myers_follower; wiki Rosalind Myers",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Militech Board of Directors",
      "role": "Collective owner: 430M shares; Lundee held 8%, Roland Yee and the board 22%; several seats double as Ministry of Defense posts",
      "character_record_id": null,
      "location_name": "Rosslyn HQ / Militech Tower, Washington D.C.",
      "open_world": false,
      "source": "wiki Militech (nationalisation, share structure, board members in the Ministry of Defense); wiki List of Militech employees; wiki Roland Yee",
      "confidence": "wiki"
    },
    {
      "name": "Meredith Stout",
      "role": "Senior Operations Manager, Night City; later Government Relations Executive",
      "character_record_id": "Character.Stout",
      "location_name": "All Foods Plant / Watson waterfront / N54 City Hall signing",
      "open_world": false,
      "source": "raw always_loaded_1 registry entry stout (phases start, talk, interrogation, maelstrom_van, maelstrom_end, end, q003_stout_sex_no_tell); separate meredith_holo community; markers q003_08_sm_stout, {q003_mp_no_tell_stout}; wiki Meredith Stout",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Anthony Gilchrist",
      "role": "Corp; Militech's mole in the convoy leak",
      "character_record_id": "Character.Gilchrist",
      "location_name": "All Foods Plant (held) / Northside storm channel (corpse)",
      "open_world": false,
      "source": "raw always_loaded_1 registry entry gilchrist (phases attack, holocall, meeting, meeting_suv, start, leaving); separate anthony_gilchrist_holo community; wiki Anthony Gilchrist",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Keenan Thorston",
      "role": "Deputy Director of Operations, Investigations Department, Night City Branch",
      "character_record_id": null,
      "location_name": "Militech Offices, Corpo Plaza",
      "open_world": false,
      "source": "shard Extraction #NC/EX/56/882 (baseid ma_hey_gle_13_onscreen_01); shard Report, Extraction #NC/EX/56/882; wiki List of Militech employees",
      "confidence": "wiki"
    },
    {
      "name": "Elizabeth W. Roider",
      "role": "Senior Armed Engagement Specialist, Department of Intervention, Night City Branch",
      "character_record_id": "Character.ma_hey_gle_13_militech_ranger2_ranged2_ajax_ma_Elizabeth_Roider",
      "location_name": "Valentino Alley, Ventura St, the Glen",
      "open_world": true,
      "source": "roster site 59 ma_hey_gle_13 (faction_id 21, phase A); site anchor -1602.629,-1119.905,9.120; shard Extraction #NC/EX/56/882; wiki Elizabeth W. Roider",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Lt. Mower",
      "role": "Lieutenant; cyberpsycho after military-grade implants; terminated by her own hit squad",
      "character_record_id": "Character.ma_wat_kab_08_cyberpsycho",
      "location_name": "Allen & Abraham St arena, Kabuki",
      "open_world": true,
      "source": "roster site 177 ma_wat_kab_08 (faction_id 21, phase default); site anchor -1093.120,1532.005,-0.090; shard ORDERS (baseid ma_wat_kab_08_onscreen_02); wiki Mower",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "name": "Kurt Hansen",
      "role": "Ex-Colonel, Militech Armed Forces; founder and head of BARGHEST; holds Dogtown",
      "character_record_id": "Character.kurtz",
      "location_name": "Dogtown (Black Sapphire, stadium, borders)",
      "open_world": false,
      "source": "raw always_loaded_1 registry entry kurtz (phases q301_01_start, q301_04_start, q303_casino, q304_01_start); wiki Kurt Hansen; shard Dogtown - Analytical Summary",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Donald Lundee Sr.",
      "role": "CEO (2020-d.); rebuilt the corp, nationalised under him, personal Arasaka vendetta",
      "character_record_id": null,
      "location_name": null,
      "open_world": false,
      "source": "wiki Donald Lundee; wiki Militech history; Cyberpunk RED",
      "confidence": "wiki+lore"
    },
    {
      "name": "Elizabeth Kress",
      "role": "CEO or president of Militech (?-2020); US/NUSA President; nationalised her former employer",
      "character_record_id": null,
      "location_name": null,
      "open_world": false,
      "source": "wiki Elizabeth Kress; wiki Militech; wiki NUSA",
      "confidence": "wiki+lore"
    },
    {
      "name": "Antonio Luccessi",
      "role": "Co-founder (1996); executive VP; chief designer",
      "character_record_id": null,
      "location_name": null,
      "open_world": false,
      "source": "wiki List of Militech employees; wiki Militech history",
      "confidence": "wiki+lore"
    },
    {
      "name": "Roland Yee",
      "role": "Chairman of the board (2020); original investor",
      "character_record_id": null,
      "location_name": "Militech Hong Kong office",
      "open_world": false,
      "source": "wiki List of Militech employees; wiki Militech (share structure)",
      "confidence": "wiki+lore"
    },
    {
      "name": "Mels Engelsson",
      "role": "VP and director of the Special Projects Department",
      "character_record_id": null,
      "location_name": "Special Projects Department, New Mexico Proving Grounds",
      "open_world": false,
      "source": "wiki List of Militech employees; wiki Militech (Special Projects)",
      "confidence": "wiki+lore"
    },
    {
      "name": "Donald Lundee Jr.",
      "role": "Employee; son and namesake of the former CEO",
      "character_record_id": null,
      "location_name": null,
      "open_world": false,
      "source": "wiki Donald Lundee Jr.; The World of Cyberpunk 2077 p.137",
      "confidence": "wiki"
    },
    {
      "name": "Samantha Lee Young",
      "role": "General; the face of the company (2045)",
      "character_record_id": null,
      "location_name": null,
      "open_world": false,
      "source": "wiki Samantha Lee Young; Cyberpunk RED p.273",
      "confidence": "wiki+lore"
    }
  ],
  "internal_factions": [
    {
      "name": "The NUSA-captive board (Pentagon bloc)",
      "leader": "Lucas Harford",
      "goals": "Keep the state-corporate fusion; 60%+ of contracts from Washington; no independent corporate policy",
      "members_hint": "Rosslyn HQ and Militech Tower; board seats doubling as Ministry of Defense posts; no in-game actors",
      "source": "wiki Militech (nationalisation, board in the Ministry of Defense, Washington as largest customer)",
      "confidence": "wiki"
    },
    {
      "name": "The Myers/Harford reformist-executive line",
      "leader": "Rosalind Myers; Lucas Harford",
      "goals": "Legitimacy and stability: pragmatic policymaking, public patriotism, veteran philanthropy, peace on Militech's terms",
      "members_hint": "Myers (Character.myers, 31 phases); Harford (netpage only); NN54 editorial support",
      "source": "netpage NETdir://militech.corp/leadership; wiki Lucas Harford; wiki Rosalind Myers",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The Lundee martial wing",
      "leader": "Donald Lundee Sr. (d.); Donald Lundee Jr. (employee)",
      "goals": "Arms supremacy; a personal war with Arasaka; make Militech the largest force on Earth; contempt for board caution",
      "members_hint": "historical core; one living heir inside the company; no 2077 actors",
      "source": "wiki Donald Lundee (personal power goals, more enemies than friends); wiki Lazarus Group (Emile Lazarus disagreed); wiki Donald Lundee Jr.",
      "confidence": "wiki"
    },
    {
      "name": "Night City operations (Stout vs Gilchrist)",
      "leader": "Meredith Stout; Anthony Gilchrist",
      "goals": "Stout: recover the convoy, prove the leak. Gilchrist: survive, keep the cut, stay unprovable",
      "members_hint": "site 59 ma_hey_gle_13 (5 units, faction_id 21); All Foods q003 communities; Character.Stout and Character.Gilchrist",
      "source": "wiki Meredith Stout; wiki Anthony Gilchrist; shard The Pickup convoy trail; wiki The Pickup",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Investigations / Intervention black-ops wing",
      "leader": "Keenan Thorston; Elizabeth W. Roider",
      "goals": "Protect Militech's political assets, bury scandals, use NCPD cover, leave no witnesses",
      "members_hint": "site 59 ma_hey_gle_13 (ranger, MG gunner, officer); shard-authors and Militech Offices staff",
      "source": "shard Extraction #NC/EX/56/882; shard Report, Extraction #NC/EX/56/882; wiki Elizabeth W. Roider",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Special Projects / Cynosure wing",
      "leader": "Mels Engelsson (2020); Dr. Evan McRay and the 2068 team",
      "goals": "Weaponise the frontier; capture and harness rogue AIs; deniability above all, including killing its own exposed executives",
      "members_hint": "Cynosure Sites C and D (no coordinates); Project Cynosure research team; SPD at the Proving Grounds (off-map)",
      "source": "wiki Project Cynosure; wiki Cynosure Facility; wiki Militech (Special Projects assassination policy)",
      "confidence": "wiki"
    },
    {
      "name": "The seceded deserter wing (BARGHEST)",
      "leader": "Kurt Hansen",
      "goals": "Independence, Dogtown, and the hardware they walked away with: Minotaurs, Centaurs, Behemoths, Chimeras, a Basilisk, a Blackwall AI",
      "members_hint": "kurtz community plus 200+ Barghest records; Albert Murphy and Hansen's ex-Militech inner circle; Dogtown",
      "source": "wiki Kurt Hansen; wiki BARGHEST (arsenal); shard Dogtown - Analytical Summary (Militech deserters as a subject of interest)",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Militech SiteSecure (commercial line)",
      "leader": null,
      "goals": "Sell contract security as a product; protect client infrastructure; keep the parent's brand off the payroll",
      "members_hint": "Night Corp maglev tunnel site 350, Militech garrison",
      "source": "wiki Maglev Tunnel Construction Site (Night Corp hired Militech SiteSecure); site 350 garrison",
      "confidence": "game-data+wiki"
    }
  ],
  "relations": [
    {
      "faction_code": "tyger_claws",
      "stance": "neutral",
      "evidence": "No attested interaction; the Claws are Arasaka's proxy with sleeper agents, and no Militech gig targets them. The JapanTown netrunner parking-lot site is adjacency only [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "valentinos",
      "stance": "hostile",
      "evidence": "Thorston's Intervention squad executed Valentino members and killed a Valentino-protected informant at Valentino Alley; Militech was investigating a Valentino-City Hall corruption link; the gang fences stolen Militech vehicles [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "arasaka",
      "stance": "rival",
      "evidence": "Fourth Corporate War 2022-25; Unification War 2069-70 on opposite sides; Militech Offices faces Arasaka Tower across Corpo Plaza; 2077 mutual sabotage and Smasher's blackmail of Gilchrist [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "kang_tao",
      "stance": "rival",
      "evidence": "Arms-manufacturing competitors; Kang Tao's Corpo Plaza North Tower is a neighbour and a Kang Tao detail stands on Militech's own HQ-concourse sub-territory (ma_cct_cpz_15, 269 m from Militech's CC) [game-data] [wiki] [inferred]",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "faction_code": "biotechnica",
      "stance": "trade",
      "evidence": "Biotechnica supplied both sides in the Fourth Corporate War, with Arasaka getting the exclusives; Militech remained a customer. Supplier relationship, no 2077 conflict [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "petrochem",
      "stance": "trade",
      "evidence": "Petrochem sells Militech rocket propellants, advanced materials and CHOOH2 at bulk discount while competing with it in chemical weapons [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "barghest",
      "stance": "hostile",
      "evidence": "A Militech colonel's deserter army holds a former Militech investment site, a Militech bunker, a Blackwall AI and a Militech-manufactured arsenal; Militech deserters are an FIA subject of interest. Doctrinal hostility, not a 2077 firefight [game-data] [wiki]",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "faction_code": "sixth_street",
      "stance": "trade",
      "evidence": "The gang was historically supplied by Militech and Kendachi with cyberware and weapons; in 2077 the Megabuilding H6 cell jumped a Militech transport and jailbreaks corpo weapons. A supply channel with a predation problem [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "aldecaldos",
      "stance": "hostile",
      "evidence": "The Sunshine Motel outpost field-tests an anti-nomad mobile radar that the Aldecaldos want to reverse-engineer; Militech's detention centre holds border crossers; Militech's veteran massacres have worsened nomad relations [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "wraiths",
      "stance": "hostile",
      "evidence": "Militech executes captured Wraiths (cs_militech_execution, cs_handcuffed_wraiths_militech, a Wraith victim at an execution scene); Wraith cells prey on Militech convoys and hold the outpost's neighbourhood [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "animals",
      "stance": "hostile",
      "evidence": "An Animals club boss ordered Seamus Sawicki to kill Militech interns who had hurt the club's joygirls; Animals-run Data Inc. sells hacked, previously stolen Militech hardware, the crackdown trigger Rogue fears [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "the_mox",
      "stance": "neutral",
      "evidence": "No attested interaction; the Mox are a Watson sex-worker collective with no Militech contract or incident [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "maelstrom",
      "stance": "hostile",
      "evidence": "Maelstrom hijacked a Militech convoy through Gilchrist and stole the Flathead; Militech raided All Foods in The Pickup; Smasher and Maelstrom held Mallory hostage to blackmail Gilchrist [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "voodoo_boys",
      "stance": "rival",
      "evidence": "Voodoo Boys espionage targets corporate databanks, and Militech combat robots were found at the Luxor spa; a NetWatch report flagged possible corporate sabotage. No direct firefight attested [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "ncpd",
      "stance": "trade",
      "evidence": "Militech is an NCPD sponsor and creditor and its equipment supplier (Lexington, Saratoga, Ajax, Minotaur, Wyvern/Griffin, Centaur); an illegal Militech extraction proceeded with explicit NCPD approval and no police intervention [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "night_corp",
      "stance": "trade",
      "evidence": "Night Corp lost the influence race to Arasaka and Militech but hired Militech SiteSecure to protect its maglev tunnel (site 350 garrison is Militech). Commercial security contract inside a rivalry [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "city_council",
      "stance": "trade",
      "evidence": "A Night City councillor assassinated by a merc had deep ties to Militech and Militech moved to scapegoat the killer to bury the corruption; the branch also runs an NCPD-approved extraction against a mayoral advisor. Purchased influence, no loyalty [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "scavengers",
      "stance": "neutral",
      "evidence": "No attested interaction; Militech security would treat scavs as criminals, but no specific event or shared site [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_regina",
      "stance": "hostile",
      "evidence": "Regina gives Concrete Cage Trap (Militech's armoured raid on a Kabuki block hunting a data thief) and the Lt. Mower sighting, where Militech's own hit squad is the villain [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_wakako",
      "stance": "neutral",
      "evidence": "No Militech-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_padre",
      "stance": "hostile",
      "evidence": "Eye for an Eye targets a Kiroshi executive whose apartment is held by eight Militech guards, so the contract puts V against Militech personnel. Incidental executive protection, not an anti-Militech campaign [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_el_capitan",
      "stance": "neutral",
      "evidence": "No Militech-specific gig or lore link found; his antipathy is toward Arasaka [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_dakota",
      "stance": "hostile",
      "evidence": "Dakota gives all three anti-Militech Badlands gigs: Radar Love (outpost radar), Goodbye, Night City (detention centre), and MIA (Militech buying a merc to bury a councillor's corruption) [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_dino",
      "stance": "hostile",
      "evidence": "The Frolics of Councilwoman Cole has Militech as the enemy at the Militech-contracted Gold Beach Marina; the client is a corpo who wants dirt on an anti-corporate councilwoman [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_rogue",
      "stance": "neutral",
      "evidence": "Hot Merchandise is not an attack on Militech: Rogue kills a business selling stolen Militech guns to prevent Militech cracking down on the city. She treats Militech as a force to be placated, not an enemy [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_mr_hands",
      "stance": "neutral",
      "evidence": "No anti-Militech gig found; his Dogtown work runs through BARGHEST and the FIA. The Heavy Hearts Militech business contact is a club fixture, not a channel [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "afterlife",
      "stance": "neutral",
      "evidence": "Neutral merc marketplace; Militech hires mercenaries as a business, but no Afterlife-specific arrangement is attested [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "nusa",
      "stance": "patron",
      "evidence": "The NUSA nationalised Militech, owns the controlling interest, provides 60%+ of contracts, staffs its board with Defence Ministry officials, and has supplied its last several presidents, while retaining the power to order it to stand down. Owner, customer and regulator in one [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "netwatch",
      "stance": "rival",
      "evidence": "NetWatch enforces the Blackwall regime that a Cynosure reactivation would breach; NetWatch and EBM logos appear on Cynosure decals, and one explanation for the project's burial is that NetWatch caught wind of it. Regulatory rivalry, no attested skirmish [wiki]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "zetatech",
      "stance": "trade",
      "evidence": "Militech arms and retrofits Zetatech airframes; the Valgus remains in service with Militech. Supplier relationship [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "trauma_team",
      "stance": "trade",
      "evidence": "Trauma Team partners with Militech and gives its employees memberships without their paying; during the Fourth Corporate War it refused to respond to Militech or Arasaka alerts [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "news54",
      "stance": "ally",
      "evidence": "NN54 has a noticeable pro-Militech bias, explicitly opposed to the pro-Arasaka WNS, and ran Militech's NCPD partnership signing and Harford's veteran story. Editorial alignment, not an operational alliance [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "kiroshi",
      "stance": "trade",
      "evidence": "Militech provides the executive-protection detail for a Kiroshi vice managing director (8 Militech guards at site 364 sts_hey_gle_01); Kiroshi is the customer [game-data] [wiki]",
      "confidence": "game-data+wiki"
    }
  ]
}
```
