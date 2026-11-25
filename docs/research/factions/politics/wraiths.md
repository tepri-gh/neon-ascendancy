# Wraiths — Leadership, Internal Politics and External Relations

Status: faction research run, 2026-11-25. One faction, one document.
Scope: Cyberpunk 2077 2.5 + Phantom Liberty, campaign disabled. Who a player can
join under, climb past, ally with or remove among the Raffen Shiv of the eastern
Badlands; the cells that pass for an organisation; and the external relations
matrix needed for wars, alliances and "guarantor" support when a player founds a
gang.

Method: this document follows [`METHOD.md`](./METHOD.md) (the politics
playbook, including its §1.1 and §1.2 corrections) and the evidence rules in
[`../METHOD.md`](../METHOD.md) (tags, local-data precedence, wiki usage). The
location catalog for the Wraiths is [`../wraiths.md`](../wraiths.md); this
document does not repeat it — it maps people and politics onto those places.

New here, beyond the worked examples: the Wraiths are the first faction in the
batch that is **acephalous in 2077**. There is no boss to join, climb past or
remove. The document therefore treats the gang as a **confederation of cells**
and states that structure explicitly, because a `leaders[]` array with one name
would be a lie.

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/comic/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My reasoning links a named person, place or stance to a record; reasoning stated | Weak, flagged |

Extra conventions for this document:

- **Presence class** (METHOD §1.2 item 2). `ambient` = persists in free roam
  without a quest; `world-activity` = NCPD scanner hustle, gig, Assault in
  Progress or minor job, i.e. free-roam content but still activity-gated;
  `story` = gated by a main or side job; `prologue` = a lifepath intro (none
  here); `off-map` = alive in lore but never spawned; `mentioned` = named only
  in shards or dialogue with no actor at all; `historical` = not present in
  2077. The JSON `open_world` flag is `true` for `ambient` + `world-activity`.
- **Cell, not rank.** The Wraiths have no attested rank ladder. What the game
  and the wiki describe is a set of **place-bound cells**, each with a boss who
  is a boss only where he stands. "Chain of command" below means "who answers
  to whom, if anyone", not a rank table.
- **Coercion is the membership test.** Raffen Shiv are defined by expulsion,
  and every internal relationship in the sources is exploitative: a coerced
  techie, a skimmed weapons deal, a desert scout "left for dead by their fellow
  Wraiths". The document records that rather than inventing a creed.
- **`Character.*_outpost_miniboss` is the named cell boss by elimination.**
  Three Wraith members named on the wiki (Ward, Craven, McBride) have no
  self-named record. Each is the sole `miniboss` entry of the community of the
  activity the wiki names them in. That is METHOD §1.2 item 4 applied three
  times; all three are tagged `[inferred]`.

---

## 1. Leadership and ranks

### 1.1 The 2077 problem: there is no leader

The wiki's `Leadership` section is two lines long, and this is the most
important political fact about the faction:

| Section | Entry | Period | 2077 status |
| --- | --- | --- | --- |
| Main Leaders | **Dogkiller** | 2020 | Long dead or gone; no 2077 record. `[wiki]` |
| Secondary Leaders | **Nash** | "unknown – 2077" | Alive at the start; **dies on every branch**. `[wiki]` |

There is no 2077 boss. The organisation's own database entry says so in
advance: the Raffen Shiv "have no common identity or ethos, **no leaders** and
no recognizable style… in essence no more than rural criminals who sometimes
form loose equivalents of urban gangs outside major cities, the Wraiths outside
Night City being a prime example." `[wiki]` (2077DAB)

That is not a gap in the wiki. It is corroborated by the game data: there is no
`Character.wraiths_boss`, no `*_wraith_leader` record, and no community anywhere
in the 55 Wraith areas whose template contains a named commander above the
`*_outpost_miniboss` level. The highest-rank records that exist are
`Character.q103_raffen_nash` (one man, one quest) and three generic
`*_outpost_miniboss` actors. `[game-data]`

**Consequence for the design.** The Wraiths cannot be joined "under a leader".
A player joins **a cell**, and the cell's boss is the only authority that
exists. Removing a cell boss decapitates that cell and nothing else. This is the
opposite of Barghest (one founder, one succession) and of Maelstrom (one boss,
one coup), and it is the cleanest expression of the design's stated Politics
weakness in the whole set.

### 1.2 Succession history: none, and that is the pattern

| Period | Leader | How the position was held |
| --- | --- | --- |
| ~2020 | **Dogkiller** | Leader of the largest Raffen Shiv group in North America; "rumored to wear clothing of human skin"; travelled at night and preyed on "the sleeping and unwary". `[wiki]` `[lore]` |
| 2020s–2070s | *(unrecorded)* | The Raffen model is fission, not inheritance: "many of the smaller Raffen groups have given up on the open road, opting instead to move into cities, terrorize them for a few weeks, and then move on." `[wiki]` |
| mid-2070s | **No one** | The Wraiths take the Corp-Bud Cement Factory and become a fixed stronghold gang rather than a road pack. `[wiki]` |
| 2077 | **Nash**, one chief among several | A merc who ran a crew out of the Corp-Bud Mine with "a secret office room in the ghost town of Rocky Ridge". He is never called *the* leader; the wiki calls him a "Secondary Leader" and a "Member". `[wiki]` |
| 2077 | **Vacancy** | Nash dies at the mine (`Ghost Town`) or leading the assault on the Aldecaldo camp (`Queen of the Highway`). Both are V-dependent but both end in his death. `[wiki]` |

**No succession event exists in the sources**, because no office exists to
succeed to. Dogkiller is a 2020 name with no institutional residue; Nash is a
crew boss with a debt. Between them is fifty-seven years and no line. For a
simulation this is a **design opportunity, not a defect**: the Wraiths are the
one faction where "internal war with no single leader" (design §5) is the
*default* state rather than a crisis state.

### 1.3 Rank structure, recruitment and advancement

What exists instead of ranks:

1. **Cell boss.** A named or generic `*_outpost_miniboss`, or a named actor
   who holds a place: Nash at the mine, Ward on I-9, Craven at Sequoia & Gray,
   McBride at Tango Tors, Blackdust at the cement factory (shard-only).
   `[game-data]` `[wiki]`
2. **Specialists.** A ripperdoc (McBride), a mechanic (Big Pete, a client not
   a member), a netrunner relationship (b&#64;d, freelance), a scout ("desert
   scout", Spite Vondell's own job title). `[wiki]` `[game-data]`
3. **The crew.** Five to twenty-one actors per community. The squads carry
   functional names, not ranks: `grunt`, `warrior`, `operator`, `strong_gunner`,
   `ghost`/sniper, `android`. Tiers 1–3 are literal in the record IDs
   (`grunt1`, `grunt2`, `warrior3`, `strong_gunner3`). `[game-data]`
4. **Hangers-on.** The 2020 text is explicit and ugly: "Weaker members or
   hangers-on are called 'bitch' and sometimes traded like cattle." `[wiki]`
   `[lore]` No 2077 record contradicts it; the coerced techie at the landfill
   outpost is the same relationship in modern dress.

**Recruitment is not a pipeline; it is a market.** The Raffen Shiv are "a motley
crew of those exiled from other Nomad groups for violating customs and other
transgressions" — murder, rape, human trafficking, poisoning the water supply or
betrayal of the clan. `[wiki]` The Wraiths do not train; they **buy, coerce or
absorb**:

- They hire outside specialists when their own are broken: Kojo recruits Iris
  Tanner because "our mechanic also has collision damage, can't work atm. And
  you're the cheapest". `[wiki]` `[game-data]`
- They coerce when hiring fails: Tanner was given "an ultimatum; Either stick
  around or be chopped into pieces". `[wiki]`
- They buy services from freelance netrunners rather than growing their own:
  b&#64;d supplied both a Maelstrom stash tip and the KI113R drone-jamming
  virus. `[wiki]` `[game-data]`
- They take on non-Raffen clients who need deniable work: Big Pete runs a
  licensed autoworks and fixes "clunkers for the Raffen Shiv". `[wiki]`

**Advancement is possession.** A Wraith rises by holding a place and delivering
loot; the record tiers (`warrior3`, `strong_gunner3`, `ghost2`) are combat
quality, not authority. There is no attested promotion ceremony, oath or
initiation anywhere in the sources — a striking absence next to Maelstrom's
chrome rite and Barghest's written directives. `[wiki]` `[game-data]`

**Internal discipline is criminal, not military.** Crews skim from each other:
a Wraith "numbers guy" charged the Tyger Claws an extra five percent on a
weapons sale and pocketed it, and his crew's response was "we'll get the eddies
off him" — not a trial. `[wiki]` A cement-factory crew member complains about
the basement draught in writing and gets "BLOW THAT FUCKING DRAFT UP YOUR
FUCKING ASS, PRINCESS" back. `[wiki]` That is the texture of authority here.

### 1.4 Named members mapped to game data

The roster check (METHOD §1.2 item 1) nearly fails for this faction: **12 roster
sites / 85 units** carry `faction_id 8`, and exactly **two** of them are
person-named records — `Character.ina_02_new_big_pete` (a client, with
`faction_id` `null`) and `Character.ma_std_rcr_18_outpost_miniboss` (Craven by
elimination). Everything else is a tier archetype
(`rcr_wraiths_grunt1_ranged1_nova_ma` and 80-odd siblings). The named people
live in the raw community registry, which is why this table names exact records.

| Name | Role / note | Character record | Community / site | Location | Presence class | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| **Nash** | Crew boss; the only 2077 name in the wiki's leadership list; owed a debt to "a Hungarian" | `Character.q103_raffen_nash` | entry `nash` in `{q005_com_slice_of_afterlife}` (spot `#q005_ws_nash_scene`); entry `miniboss_bear` in `{q103_com_mine_ambush_raffen_shiv}` (phase `bossfight`, spot `#q103_ws_mine_ambush_bear`); entry `nash` in `{sq027_com_nash_group}` (spot `#sq027_ws_raffen_shiv_nash_group_nash`) | Afterlife (cameo) / Corp-Bud Mine / Aldecaldo camp | `story` | `[game-data]` `[wiki]` |
| **Dogkiller** | 2020 leader; no 2077 presence | — | — | — | `historical` | `[wiki]` `[lore]` |
| **Blackdust** | Cement-factory chief: receives scouting reports, sets strategy, claims primacy over other Raffen | — (shard-only; `Corp-Bud Cement Factory/Computers`) | `sq004` camp | Corp-Bud Cement Factory | `mentioned` | `[wiki]` |
| **Bruce Ward** | "High-ranking member and cell leader"; multiple robberies; planned a Biotechnica radioactive-waste convoy robbery | `Character.ma_bls_ina_se1_17_outpost_miniboss` `[inferred]` | `{ma_bls_ina_se1_17_com}` (9 Wraiths incl. one `mini_boss` and one HMG gunner) | I-9, south-east of DaKota, Rocky Ridge | `world-activity` | `[game-data]` `[wiki]` `[inferred]` |
| **Paul Craven** | Cell leader; "known leader within a NC human trafficking ring"; corporate convoy hijacker | `Character.ma_std_rcr_18_outpost_miniboss` `[inferred]` | `{ma_std_rcr_18_com_wraiths}` (20 Wraiths) + `hostage_01..10`; roster site 170 (33 units) | Sequoia & Gray, Rancho Coronado | `world-activity` | `[game-data]` `[wiki]` `[inferred]` |
| **Rufus McBride** | Unlicensed ripperdoc sheltering among the gang; 3 counts of permanent disability, 1 staged suicide | `Character.ma_bls_ina_se5_07_outpost_miniboss` `[inferred]` | `{ma_bls_ina_se5_07_com}` (10 Wraiths incl. `#ma_bls_ina_se5_07_npc_06` and an android bodyguard `_npc_07`) | Tango Tors Motel, Sage Gulch Rd, Jackson Plains | `world-activity` | `[game-data]` `[wiki]` `[inferred]` |
| **Michael Marcinkowsky** | Stash guard / smuggler pilot; crew downed crossing the SoCal border | `Character.ma_bls_ina_se5_11_michael` | `{ma_bls_ina_se5_11_com}` entry `ganger_05` | Assault in Progress south-south-east of Lake Farm, Laguna Bend | `world-activity` | `[game-data]` `[wiki]` |
| **Arnold Haponik** | Crew enforcer; collecting a debt from a "numbers guy" who skimmed a Tyger Claws weapons sale | `Character.ma_bls_ina_se5_13_arnold` | `{ma_bls_ina_se5_13_com}` entry `ganger_03` | Fuel station west of Jackson Plains Regional Airport | `world-activity` | `[game-data]` `[wiki]` |
| **Kojo** | Outpost boss who hires and then coerces outside techies | — (shard-only; `Wraiths Outpost/Computers`, `Message from Kojo to Iris Tanner`) | `{ina_06_com}` | Wraiths Outpost, Municipal Landfill | `mentioned` | `[wiki]` |
| **George** | Highway-cell boss; no wiki page, record name only | `Character.ma_bls_ina_se5_12_george` | `{ma_bls_ina_se5_12_com}` entry `ganger_03` | Badlands, se5 highway cell | `world-activity` | `[game-data]` |
| **Desi** | Highway-cell boss; no wiki page, record name only | `Character.ma_bls_ina_se5_03_desi` | `{ma_bls_ina_se5_03_com}` entry `ganger_003` | Badlands, se5 highway cell | `world-activity` | `[game-data]` |
| **Timothy** | Highway-cell boss; no wiki page, record name only | `Character.ma_bls_ina_se5_16_timothy` | `{ma_bls_ina_se5_16_com}` entry `ganger_02` | Badlands, se5 highway cell | `world-activity` | `[game-data]` |
| **Dove Vondell** | **Deserter.** Former Wraith; glamdoc; co-owner of Hoisted Colors | `Character.std_rcr_glamdoc_01` `[inferred]` | Rancho Coronado glamdoc pair | Coronado Dam, Rancho Coronado | `ambient` | `[wiki]` `[inferred]` |
| **Spite Vondell** | **Deserter.** Former "Wraith enforcer and desert scout"; glamdoc; co-owner | `Character.std_rcr_glamdoc2_01` `[inferred]` | Rancho Coronado glamdoc pair | Coronado Dam, Rancho Coronado | `ambient` | `[wiki]` `[inferred]` |
| **Big Pete** (Pete Kowalski) | **Client, not a member.** Manager of New American Autoworks; fixes clunkers for the Wraiths; sold them a faulty Militech cloaking device | `Character.ina_02_new_big_pete` (roster site 340 entry `big_pete`, `faction_id` **null**) | `{ina_02_com_gangers}` (9 Wraiths) | New American Autoworks, Sage Gulch Rd | `world-activity` | `[game-data]` `[wiki]` |
| **Iris Tanner** | **Captive, not a member.** Nomad techie coerced into repairs | — (nav record not found) | `{ina_06_com}` | Wraiths Outpost, Municipal Landfill | `world-activity` | `[wiki]` |
| **Susan Parker** | Crew member who exposes the skim; talks to the Tyger Claws | — (shard-only) | se5_13 | Badlands fuel station | `mentioned` | `[wiki]` |
| **Marley Anderson** | Crew member on the doomed border run | — (shard-only) | se5_11 | Laguna Bend | `mentioned` | `[wiki]` |
| **Plumber Joe**, **viper**, **Morris**, **karl** | Cement-factory crew names in shards | — (shard-only) | `sq004` camp | Corp-Bud Cement Factory | `mentioned` | `[wiki]` |
| **Rita Sweden**, **Rip Turman** | Wraiths killed by b&#64;d's mined bunker | — (shard-only) | `ma_bls_ina_se1_11` | south-east of Edgewood Farm | `mentioned` | `[wiki]` |

### 1.5 Name collisions and data traps (four real ones)

- **`mws_se5_07` ≠ `ma_bls_ina_se5_07`.** These are two different places with
  one shared token. `mws_se5_07` is site 324, the *Shape of a Pony* chop-shop
  camp in the Badlands (`-1101.19, -2426.75`). `ma_bls_ina_se5_07` is **not a
  site at all** — it is the community-only NCPD hustle *Suspects Organized Crime
  Activity: Jackson Plains* at the Tango Tors Motel (`-269.3, -4884.4`), whose
  boss is Rufus McBride. The wiki uses `ma_bls_ina_se5_07` as the gig's
  `baseid`, and `sites.json` has no such code. Anyone who "joins Rufus McBride to
  the Shape-of-a-Pony garage" has joined 2.5 km and two districts of wrong.
  `[game-data]` `[wiki]`
- **`bruce` is not Bruce Ward.** `Character.sts_bls_ina_05_bruce` is the
  Militech Detention Center prisoner of *Gig: Goodbye, Night City* — Bruce
  **Welby**, an Aldecaldo smuggler with `affiliation = Aldecaldos`. Bruce
  **Ward**, the Wraith cell leader, has no name-bearing record at all and is the
  `Character.ma_bls_ina_se1_17_outpost_miniboss` by elimination. Two Bruces, one
  substring, opposite factions. `[game-data]` `[wiki]`
- **`nash` exists in three communities.** The registry entry name `nash` appears
  in the Afterlife cameo, the mine boss fight and the Aldecaldo-camp raid, all
  pointing at the same `Character.q103_raffen_nash`. Counting entries rather
  than deduplicating records would give Nash three bodies. `[game-data]`
- **The wiki member table is wrong about Michael Marcinkowsky's location.** It
  places him "at the Poppy Farm… guarding a stash of equipment". His shard is
  `ma_bls_ina_se5_11_onscreen_01`, and his actor
  `Character.ma_bls_ina_se5_11_michael` sits in `{ma_bls_ina_se5_11_com}` at
  `732.5, -3949.3` — the *Assault in Progress* south-south-east of Lake Farm,
  not Poppy Farm (`877.6, -3612.7`). The shard's own text describes a crashed
  Zetatech Valgus and a border crossing, which matches the assault, not the
  farmstead. **Read the shard's `location=` field, not the member table.** This
  is the strongest single instance I found of the batch's "titles can invert the
  stance" warning applied to a *place*. `[wiki]` `[game-data]`

### 1.6 What the game actually spawns (open world vs story-only)

**`world-activity` — free-roam but activity-gated. This is most of the named
cast, unusually for this batch.**

- **Bruce Ward** — SOCA *Rocky Ridge*, `baseid ma_bls_ina_se1_17`, on I-9.
- **Paul Craven** — SOCA *Desperate Sons-of-Bitches*, `baseid ma_std_rcr_18`, at
  Sequoia & Gray. Ten hostages are spawned with him.
- **Rufus McBride** — SOCA *Jackson Plains*, `baseid ma_bls_ina_se5_07`, at
  Tango Tors Motel.
- **Michael Marcinkowsky**, **Arnold Haponik**, **George**, **Desi**,
  **Timothy** — Assault-in-Progress / crime-scene communities in the se5 and
  se1 highway band.
- **Big Pete** — *Gig: Big Pete's Got Big Problems*, `baseid sts_bls_ina_02`.
- **Iris Tanner** — *Gig: No Fixers*, `baseid sts_bls_ina_06`.

**`story` — gated; do not expect them in free roam with the campaign disabled.**

- **Nash**, in the Corp-Bud Mine boss phase of `Ghost Town` and in the Aldecaldo
  camp assault of `Queen of the Highway`, plus a scripted Afterlife cameo
  (`{q005_com_slice_of_afterlife}`, `The Heist`). `[game-data]` `[wiki]`

**`ambient` — persists.** Dove and Spite Vondell (Update 2.5) at Hoisted Colors,
Coronado Dam. Vendors persist regardless of quests; their records are
`[inferred]` from the only two-glamdoc community in Rancho Coronado. `[wiki]`
`[game-data]`

**`mentioned` — no actor at all.** Blackdust, Kojo, Susan Parker, Marley
Anderson, Plumber Joe, viper, Morris, karl, Rita Sweden, Rip Turman. These are
shard voices, not NPCs; the mod must synthesise them if it wants them to speak.

**`historical`.** Dogkiller (2020 only).

**Caveat, and it bites harder here than elsewhere.** Almost all Wraith political
content is NCPD scanner content. If the mod disables scanner hustles with the
campaign, the entire named 2077 leadership disappears — Ward, Craven, McBride,
Haponik, Marcinkowsky and the three record-named cell bosses are all
`world-activity`. Only the two deserter-vendors survive. **Under a strict
"campaign disabled" reading, the Wraiths keep no named member who is still a
member.** Plan to seed a synthetic roster; do not plan to reuse the game's.

### 1.7 Player-path hooks

Because there is no ladder, the hooks are per-cell and per-place.

| Person / cell | Join under | Climb past | Ally with | Remove |
| --- | --- | --- | --- | --- |
| **Nash** (mine, Rocky Ridge) | The only crew with a name, a stash and a debt | He is a crew boss, not a chief; out-earning him is enough | The "Hungarian" creditor, Rogue (as a merc channel), the 6th Street fence | Killing him removes the one named chief, the mine and the Rocky Ridge office, and starts the Aldecaldo war's scripted set-piece |
| **Blackdust** (cement factory) | The largest concentration and the only true stronghold | His authority is shard-voice only; a player who takes the factory takes his seat | The gate crew, the drone operators, the basement chrome room | Removing him should fracture the factory cell — it is the one cell whose loss hurts the faction |
| **Bruce Ward** (I-9) | A raider cell with a plan and a bounty | He is a "cell leader"; take his cell | The radioactive-waste buyer ("Boss already has some ideas") | His death closes a NCPD bounty and a Biotechnica grievance |
| **Paul Craven** (Rancho Coronado) | The city-facing wing: trafficking, convoy hijack | He is a ringleader; the ring is the ladder | Nobody inside; buyers outside | Killing him removes the faction's only permanent city foothold |
| **Rufus McBride** (Tango Tors) | The service economy: patch-ups, chrome, parts | Not a ladder; he is a specialist | The clinic buyer from `Current needs`, Big Pete | Killing him removes unlicensed medical capacity the crews depend on |
| **Kojo** (landfill outpost) | Hostage work, forced labour, drug plans | Small; one building | Nobody | Killing him frees Tanner and closes the outpost |
| **Dove / Spite Vondell** (Hoisted Colors) | Not a ladder — they are out | — | Both twins, as civilians and as a cautionary tale | Killing them costs nothing politically and destroys a defection story |
| **Big Pete** (New American Autoworks) | A client relationship, not membership | He is the shop's manager and the Wraiths' fence | Dakota's enemies, the Wraiths, his brother Tiny Mike | Killing him removes the faction's best-equipped garage and its Militech-parts channel |

**The real join path is economic, not military.** The Wraiths accept anyone who
brings loot and asks no questions, which is precisely how they recruit in lore
(exiles, fugitives, broken techies). A player can therefore **be the cell**:
take a highway community, hold it against the ambient spawns, and be a Wraith
long before any named Wraith acknowledges them. This is the faction's most
distinctive player path and the one the design's "found a gang" rules already
support.

### 1.8 Places as political structure

The Wraiths' politics *is* their real estate. Each cell is a place, and the
place's function determines the cell's politics. Mapped from
[`../wraiths.md`](../wraiths.md) §3:

| Place | What it is politically | Cell / function |
| --- | --- | --- |
| **Corp-Bud Cement Factory** | The seat. Walled, gated, guardhouse, drone overwatch, prison, basement gutting room | The only plausible capital; Blackdust's command |
| **Corp-Bud Mine** | A bunker and a stronghold; Nash's hideout and office | Nash's crew; the Vendetta cell |
| **Rocky Ridge** | A lookout and a meeting ground: bar, fuel-station roof, secret office | Nash's forward post; the I-9 raiders' haunt |
| **Union Railroad Station** | A signals-intrusion base: antenna, turrets, cameras, 16 units | The technical wing; drone hijacking |
| **New American Autoworks** | A licensed shop the gang garrisons; the only `is_interior` site | A client asset (Big Pete) with a Wraith garrison |
| **Wraiths Outpost (landfill)** | A hostage box in a dump | Kojo's crew; forced labour |
| **Sequoia & Gray** | The only city foothold; trafficking and convoy hijack | Craven's ring |
| **Poppy Farm / Highway 101 / Shape-of-a-Pony garage** | Smuggling stash, corpse freezer, chop shop | The logistics and chrome wing |
| **16 ambient highway communities** (`ma_bls_ina_se1_11..21`, `se5_03..16`) | Encounters, not holdings: 87 entries, no `sites.json` row | The un-named mass of the faction |

The political reading: the Wraiths hold **one capital, two strongholds, three
field outposts, one city racket and a swarm of roadside cells**, and no place
has authority over another. Losing the factory costs the faction its prestige
and its chrome room; losing the mine costs it Nash; losing Sequoia & Gray costs
it the city. None of those losses decapitates the faction, because there is
nothing to decapitate.

---

## 2. Internal political factions

### 2.1 The blocs

"Members" counts are **presence proxies** from `areas.jsonl` and the raw
community registry, not membership rolls. `sq004`'s five communities are
overlapping phases of one camp; do not sum them into a garrison.

| Bloc | Leader(s) | What it wants | Presence / members hint | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- |
| **The cement-factory cell** | **Blackdust** (shard-voice) | Hold the seat, raid the city's outskirts, keep other Raffen out, sell chrome through a clinic buyer | `sq004_com_wall` 18, `sq004_com_raiders` 10, `sq004_com_chase_enemies` 10, `sq004_com_main` 8, `sq004_com_reinforcements` 5; drone records; prison and basement | Scouting report, "regarding the Breakers", "Current needs", the basement draft exchange | `[game-data]` `[wiki]` |
| **Nash's crew (mine and Rocky Ridge)** | **Nash** | The big score: the Warhorse, the 6th Street shipment, the debt paid; keep the mine and the town office | `q103_com_mine_ambush_raffen_shiv` 11 + 3 reinforcements; `sq027_com_nash_group` 7; `q103_com_raffen_shiv` 7 at Rocky Ridge | Nash's wiki page; the Aldecaldos? Panam Palmer? shard; Ghost Town | `[game-data]` `[wiki]` |
| **Ward's I-9 raiders** | **Bruce Ward** | Rob a Biotechnica radioactive-waste convoy; repeat the robberies that earned the bounty | `{ma_bls_ina_se1_17_com}` 9 incl. a `mini_boss`, 2 snipers and an HMG gunner | SOCA dispatcher text; `get ready` and Official Order #912317 AJ-98 | `[game-data]` `[wiki]` |
| **Craven's trafficking ring** | **Paul Craven** | Move people, hijack corporate convoys, sell bodies and chrome; hold the city corner | `{ma_std_rcr_18_com_wraiths}` 20 (19 human + 1 android) + 10 hostages; roster site 170, 33 units | SOCA dispatcher text; Craven's wiki page; `Tonight` | `[game-data]` `[wiki]` |
| **The service wing** | **Rufus McBride** (ripperdoc); Big Pete (client) | Monetise the loot: patch-ups, chrome extraction, chop work, parts | Tango Tors cell; New American Autoworks garrison (9 units, 11 doors, 4 devices); Union Railroad antenna crew (16 units) | McBride and Big Pete pages; `Current needs`; the Simon Diaz shard; Flying Drugs | `[game-data]` `[wiki]` |
| **Kojo's outpost crew** | **Kojo** | Forced labour now; drug manufacture and cross-country distribution later | `{ina_06_com}` 9 entries / 7 Wraith roster units; the hostage building; the garage | `Message from Kojo to Iris Tanner`; `Note #44` ("we got the trade routes, all we gotta do is use em") | `[game-data]` `[wiki]` |
| **The highway cells** | **George**, **Desi**, **Timothy** (record names only) | Ambush travellers and convoys; survive | 16 ambient communities / 87 entries across the se1 and se5 highway bands; 5–7 Wraiths each | `areas.jsonl` `ma_bls_ina_se1_11..21`, `se5_03..16`; `la_sm_execution_03` scenes | `[game-data]` |
| **The deserters** (splinter) | **Dove Vondell**; **Spite Vondell** | Leave. Run a glamdoc shop, serve whoever pays, never go back | Two glamdoc actors at Coronado Dam, Rancho Coronado | Both database entries: "Ambushed by the Aldecaldos and left for dead by their fellow Wraiths" | `[wiki]` `[game-data]` |

### 2.2 Blackdust and the cement factory: the strongest claim to a seat

The cement factory is the only place in the faction with a documented command
voice, and that voice is a shard.

- **He receives intelligence.** "Scouting report", from Plumber Joe to
  Blackdust: the land is good for raids, there is "little to no Caldo activity
  out here", Militech "patrols stick to their facility", **but** "we did come
  cross some heavy ironed Breakers. They're pushing in deeper. What's our
  strat??" `[wiki]`
- **He sets strategy and asserts primacy.** "regarding the Breakers", from
  Blackdust to viper: they have had to "work with other raffen groups because of
  the weak hauls down south. BUT – that's as far as it goes. Outside NC ain't no
  one stronger than us. If any soul out there mistakes us for a fucking
  charity… you know what to do. This is OUR backyard!!!" `[wiki]`
- **He is not a member of the wiki's leadership list.** The faction page does
  not know he exists; only the location's computer does. That is the METHOD's
  "decisive incidents live in location docs" warning in its purest form.
- **His cell has a commercial relationship the rest lack.** The "Current needs"
  shopping list is addressed to a clinic: limbs, chip sockets, processors, bio
  adapters, optics, exoskels — and "DO NOT send any more p links or thrusters".
  The factory cell is a **supplier to a ripperdoc or clinic buyer**, not just a
  raider. `[wiki]`

For a simulation: Blackdust is the natural "declared leader" a player-appointed
Wraith hierarchy would elevate, and the factory is the natural capital. Neither
is true in the game, which is exactly why the mod has to choose.

### 2.3 Nash and the vendetta cell

Nash is the only Wraith with a biography, and it is a story about a bad decision.

- He had "a hideout in the Corp-Bud Mine as well as a secret office room in the
  ghost town of Rocky Ridge". `[wiki]`
- He and his crew "got indebted to 'a Hungarian'", so he devised a plan: become
  a merc for **Rogue Amendiares**, get paired with **Panam Palmer**, and steal
  her Thorton Warhorse plus "a shipment for the 6th Street gang". `[wiki]`
- His own note (the shard in his mine room) is a risk assessment: "girl is
  Aldecaldos, could be a problem… job goes south - risk of retaliation. but fuck
  it." And: "wheels look worth at least as much as we owe the Hungarian." `[wiki]`
- He misjudged the fixer: "if she's like the rest, couldn't give a flying fuck
  so long as the merch gets moved". Rogue did care, because Panam was her
  recruit. `[wiki]`

That is the faction's whole strategic repertoire in one episode: **steal from a
partner, underprice the retaliation, and let a creditor set the tempo.** The
cell is not a political programme; it is a debt.

### 2.4 Craven and the city foothold

The Rancho Coronado ring is the only Wraith operation that lives permanently
inside Night City, and it is the faction's most exposed asset.

- Craven is "a known leader within a NC human trafficking ring" and a corporate
  convoy hijacker; the NCPD dispatcher wants him for both. `[wiki]`
- The site spawns **twenty** Wraiths — the largest single Wraith community in
  the game — plus ten hostages in two groups of five, matching Craven's own
  message about "Eddie Friedman's group" and "Marta's group". `[game-data]`
  `[wiki]`
- It sits at Sequoia & Gray in **Rancho Coronado**, 6th Street's home district
  and 22 m from a 6th Street control centre. The faction is camped inside a
  rival's turf with twenty guns. `[game-data]`

For a simulation: this cell is the faction's **escalation trigger**. It is the
one place a War with a city gang would start, and the one place whose loss the
Wraiths would feel economically.

### 2.5 The service wing: the faction's actual strategic depth

The Wraiths do not manufacture. They **convert loot into money**, and that
conversion is done by a handful of specialists who are more valuable than any
raider.

- **Rufus McBride**, unlicensed ripperdoc: "mutilating three people and faking a
  patient's suicide"; operates on his associates at the Tango Tors Motel; his
  intake conversation is about which *hardware brand* a patient runs, because
  "least we won't be short on parts". `[wiki]`
- **Big Pete**, garage manager and fence: fixes "clunkers for the Raffen Shiv",
  and sold them a Militech cloaking device that failed — which is why a
  smuggling run was marked, shot down over the border, and why he now has a
  contract on him. `[wiki]` A **client's failure cost a Wraith crew**, and the
  faction's response was to let Dakota's favour economy handle it. `[wiki]`
- **The Union Railroad antenna crew**: "the perfect use for the station's old
  antenna", running b&#64;d's KI113R virus to drop cargo drones. `[wiki]`
- **b&#64;d**, freelance: sold them a Maelstrom stash tip and the virus, then
  "took them on" — the Wraiths "would use another netrunner to locate b&#64;d's
  hideout", walked into a mined bunker, and were killed. `[wiki]`

This wing is why the gang survives its own incompetence. It is also the faction's
**cheapest capture target**: kill one ripperdoc or close one garage and the loot
stops converting.

### 2.6 The deserters: a splinter written in prose

METHOD's instruction is that a splinter or deserter wing is a bloc, described in
prose. This is the only one the Wraiths have, and it is a complete political
statement in two sentences:

> "Ambushed by the Aldecaldos and **left for dead by their fellow Wraiths**,
> Dove Vondell and her twin sister, Spite, had to do unspeakable things to
> survive." — Dove's database entry. `[wiki]`

> "In her last day as a **Wraith enforcer and desert scout**, Spite Vondell
> experienced the bitter taste of betrayal… But Spite managed to claw her way
> back to life, guided by a new philosophy – **compassion gets you killed**." —
> Spite's database entry. `[wiki]`

Politically this is worth more than a whole cell:

1. **The Raffen "family" abandoned its own wounded.** That is the empirical
   disproof of any Culture-based cohesion. The gang is not a tribe; it is a
   predation pact with an exit wound.
2. **They defected to the civilian economy**, not to a rival gang: a glamdoc
   shop at Coronado Dam, in 6th Street territory, where Spite argues they
   should court **NUSA** clients and Dove argues they should serve everyone.
   That is the same Dove/Spite axis the design wants (a faction's internal
   policy split) in miniature. `[wiki]`
3. **Dove later disappears** and Spite "dodged any questions regarding her fate
   or whereabouts" — an open thread the mod can resolve either way. `[wiki]`

### 2.7 The Raffen context: why "Tribe" is the wrong word

The design puts the Wraiths in the **Tribe** archetype, whose strength is
**Culture**. The lore says the opposite, in the plainest possible terms:

- Raffen are "the most-hated nomads", considered "subhuman" even by the
  permissive nomad society. `[wiki]`
- "Nobody would call these groups family – not even in jest." `[wiki]`
- "They thus have **no common identity or ethos**, no leaders and no recognizable
  style." `[wiki]`
- "The Raffen culture is oppressive. Stronger members are physically abusive to
  weaker ones, either for cause or sport. Weaker members or hangers-on are called
  'bitch' and sometimes traded like cattle." `[wiki]` `[lore]`

What the Wraiths *do* share is **style and exclusion**: skull-and-crossbones
bandanas "meant to inspire fear", combat-modded rigs with guns and missile
launchers, a recognisable vehicle set (Specter, Wendigo, Reaver, Ghoul,
Revenant). `[wiki]` That is a brand, not a culture, and it is **exported to
outsiders** rather than binding insiders. See §4.

### 2.8 What could drive internal conflict in a simulation

Evidence-based drivers, in rough order of plausibility:

1. **A debt comes due.** Nash's "Hungarian" is the model: an external creditor
   sets a cell's tempo and forces a bad job. Any cell can be given one.
2. **The stronghold versus the swarm.** Blackdust claims primacy over other
   Raffen and expects obedience; the highway cells and Kojo's outpost run their
   own rackets and have never met him. Centralisation is a live grievance.
3. **Skimming.** A "numbers guy" overcharged the Tyger Claws by five percent and
   kept it. Enforcement is personal ("we'll get the eddies off him"), so
   skimming is rational until someone is made an example.
4. **Coerced labour.** Kojo's crew holds a specialist against her will. That is
   a permanent escape risk, an NCPD lead, and — as the Vondells show — a
   defection in waiting.
5. **The city foothold.** Craven's nineteen-gun cell inside 6th Street's
   district is either the faction's best asset or the war it cannot win,
   depending on who is arguing.
6. **Expansion into manufacturing.** `Note #44` is a Wraith trying to
   reverse-engineer glitter/cathinone and arguing for cross-country
   distribution: "we got the trade routes, all we gotta do is use em". A wing
   that wants to become a drug producer is a different faction from one that
   wants to stay a looter.
7. **Betrayal and desertion.** The Vondells are the template. Every hard
   reversal should be able to produce a deserter, and every deserter is a
   competitor with inside knowledge.

---

## 3. External relations matrix

### 3.1 Stance vocabulary

One stance per row. Use the first that fits; do not average two stances into a
non-answer.

| Stance | Meaning |
| --- | --- |
| `war` | Open, active armed conflict over turf or existence |
| `hostile` | Actively targets or raids the other side, but not a declared turf war |
| `rival` | Turf or economic competition, with skirmishes |
| `neutral` | No attested interaction; not an ally |
| `trade` | Transactional exchange, no loyalty |
| `ally` | Coordinated support or shared operations |
| `patron` | Protects or supplies the gang |
| `client` | Hires the gang |

### 3.2 The matrix

Every row is a faction code from `data/factions.json`, plus `city_council`, the
eight fixers, `afterlife`, and the two extra political actors `nusa` and
`netwatch` (METHOD §1.1 item 7).

There is **no usable offline attitude matrix**. `refs/RED4ext.SDK/.../game/data/
Affiliation.hpp` is an identity enum (`Wraiths` = 8), not a relation table;
`Attitude_Record.hpp` is opaque. Every stance below is judged from quests,
shards, the wiki and co-location records. Rows with no attested interaction are
`neutral` + `[inferred]`; they are placeholders, not friendships.

| Faction | Code | Stance | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| Tyger Claws | `tyger_claws` | `trade` | The Wraiths **sold weapons to the Tyger Claws**: "remember when we sold them that iron?… that time mikey almost bit the dust carrying them over", and a Wraith "numbers guy" overcharged them five percent `[wiki]` (Haponik/Parker shard); the Tyger Claws' own doc records the pair as `neutral` — an asymmetry this document corrects `[inferred]` | `wiki+inferred` |
| Valentinos | `valentinos` | `neutral` | No attested interaction; different district. Do not infer a rivalry from both being gangs `[inferred]` | `inferred` |
| Arasaka | `arasaka` | `neutral` | Only co-location is the Phantom Liberty **courier-loop enemy pool** (`{sa_ep1_159_narrative_com}` mixes 5 Wraiths with 4 Arasaka bodyguards and 2 Scavs as interchangeable obstacles for one courier job) — a crowd pool, not an alliance `[game-data]`; Wraiths raid "weakly guarded corp transports" generically `[wiki]` | `game-data+inferred` |
| Militech | `militech` | `hostile` | Militech **executes captured Wraiths**: `cs_militech_execution*`, `cs_handcuffed_wraiths_militech*`, and a Wraith corpse with role `victim` at the `ma_bls_ina_se1_04` scene alongside five Tyger Claws and five Militech units `[game-data]`; Wraiths prey on corp convoys and their own scout reports say Militech "patrols stick to their facility" `[wiki]`; the SoCal border is Militech-policed `[wiki]` | `game-data+wiki` |
| Kang Tao | `kang_tao` | `neutral` | No attested interaction. The `q104` AV chase through Jackson Plains is removed by the design's §7 alternate timeline `[wiki]` `[inferred]` | `inferred` |
| Biotechnica | `biotechnica` | `hostile` | Bruce Ward's cell planned to **rob a Biotechnica convoy carrying radioactive waste**: "Got some info off one gonk about the Biotechnica drop. Here's the route… jump the transport and take the cargo. Shit's radioactive." `[wiki]`; the Highway 101 nest sits in Biotechnica Flats; Poppy Farm was a Biotechnica TradFarm before it became a Wraith stash `[wiki]` | `game-data+wiki` |
| Petrochem | `petrochem` | `neutral` | Only the Shape-of-a-Pony camp's description ("a makeshift garage south of the EBM Petrochem Stadium") — a landmark, not a relation `[wiki]` `[inferred]` | `inferred` |
| Barghest | `barghest` | `neutral` | No attested interaction. The `ma_pac_wwd_08_com` area is labelled `dogtown` in `areas.jsonl` but sits in **West Wind Estate** (Pacifica); it is a district-code artifact, not a Dogtown presence `[game-data]` | `game-data+inferred` |
| 6th Street | `sixth_street` | `rival` | Nash stole "a shipment for the 6th Street gang" while betraying Panam `[wiki]`; Panam then delivered a package to the 6th Street lieutenant **Boz** at the Sunset Motel — inside Wraith country `[wiki]`; the twenty-strong Craven cell operates at Sequoia & Gray in 6th Street's own district, 22 m from a 6th Street control centre `[game-data]`; 6th Street's doc records `neutral` and missed the Nash theft `[inferred]` | `game-data+wiki` |
| Aldecaldos | `aldecaldos` | `war` | "A long history of frequent conflict and warring" `[wiki]`; the Wraiths **kidnapped Saul Bright** and held him at the cement factory (`Riders on the Storm`) `[wiki]`; `sq027` spawns 30 Wraith entries assaulting the Aldecaldo camp, with Nash leading the `nash_group` (7) and four reinforcement cars `[game-data]` `[wiki]`; the Aldecaldos retaliate at the cement factory and the mine, and Cassidy deliberately left incriminating Militech gear outside the factory to frame them `[wiki]`; Trevor Brass was killed at a Wraith nest and his family are Aldecaldo `[wiki]`; the Vondell twins were "ambushed by the Aldecaldos and left for dead by their fellow Wraiths" `[wiki]` | `game-data+wiki` |
| Animals | `animals` | `neutral` | No attested interaction; only spatial (a Wraith hustle 6.7 m from an Animals community in West Wind Estate) `[game-data]` `[inferred]` | `inferred` |
| The Mox | `the_mox` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Maelstrom | `maelstrom` | `hostile` | b&#64;d sold the Wraiths intel on a **Maelstrom drug stash**, and the Wraiths **raided it** at the Megapax Export warehouse on Leru Street, Northside; Maelstrom was "caught off-guard", one member escaped wounded into the sewers, and the warehouse was abandoned (`Reported Crime: Dredged Up`, Grizzle/Ryder and Kenton/Wrey shards) `[wiki]` `[game-data]`; `{ma_wat_nid_10_com}` still holds 6 Wraiths `[game-data]`; Maelstrom's doc records `neutral` and missed the raid `[inferred]` | `game-data+wiki` |
| Voodoo Boys | `voodoo_boys` | `neutral` | No attested interaction; the Shape-of-a-Pony camp is 288 m from a Voodoo Boys control centre (`cc_dt_terra_cognita`) — adjacency only `[game-data]` `[inferred]` | `inferred` |
| NCPD | `ncpd` | `hostile` | NCPD dispatches **three SOCAs** against named Wraith cells (Ward, Craven, McBride) and posts the bounties, explicitly naming each cell leader `[wiki]` `[game-data]`; Wraiths are the subject of Assault-in-Progress, Reported Crime and `la_sm_execution_03` scenes across 16 highway communities `[game-data]`; "the Wraiths ignored the law" `[wiki]` | `game-data+wiki` |
| Night Corp | `night_corp` | `neutral` | No attested interaction; a corp, not a turf actor `[inferred]` | `inferred` |
| City Council | `city_council` | `neutral` | No attested interaction. The Badlands lie outside the Council's writ, which is why the only city instrument against the Wraiths is an NCPD bounty `[inferred]` | `inferred` |
| Scavengers | `scavengers` | `rival` | Same trade — "similar to the Scavengers, the Wraiths would also kidnap people and kill them for their bodyparts and chrome" `[wiki]`; the Wraiths **hit a Scav den** in West Wind Estate (`ma_pac_wwd_02_wraiths_com` beside `ma_pac_wwd_02_scavs_com`, 3 Wraiths vs 8 Scavs) `[game-data]`; Scav and Wraith actors share Phantom Liberty courier pools as interchangeable enemies, which is not an alliance `[game-data]` | `game-data+wiki` |
| Regina Jones | `fixer_regina` | `neutral` | No Wraith-specific gig found. Her district is Watson/Northside, where the Wraiths raided a Maelstrom stash, but that is not her operation `[inferred]` | `inferred` |
| Wakako Okada | `fixer_wakako` | `neutral` | No Wraith-specific gig or lore link found `[inferred]` | `inferred` |
| Sebastian Ibarra (Padre) | `fixer_padre` | `neutral` | No Wraith-specific gig or lore link found `[inferred]` | `inferred` |
| Muamar Reyes (El Capitán) | `fixer_el_capitan` | `hostile` | *Shape of a Pony*: Muamar sends V to recover a Porsche from "several Wraiths surrounding the car" after the seller vanished; the Wraiths stole an AUTOFIXER vehicle `[wiki]` `[game-data]` | `game-data+wiki` |
| Dakota Smith | `fixer_dakota` | `hostile` | She issues **every Badlands gig against the gang**: *Flying Drugs*, *Big Pete's Got Big Problems*, *No Fixers*, *Trevor's Last Ride* `[wiki]` `[game-data]`; she is an Aldecaldo, so the hostility is structural, and the Wraiths are the "Raffen Shiv" in her ecosystem speech `[wiki]` | `game-data+wiki` |
| Dino Dinovic | `fixer_dino` | `neutral` | No Wraith-specific gig or lore link found `[inferred]` | `inferred` |
| Rogue Amendiares | `fixer_rogue` | `trade` | **Nash worked for Rogue as a merc** and was paired with Panam, which is how the betrayal happened `[wiki]`; his registry entry appears in the Afterlife `{q005_com_slice_of_afterlife}` community `[game-data]`; a hiring channel, not loyalty — she backs Panam against him afterwards `[wiki]` | `game-data+wiki` |
| Mr. Hands | `fixer_mr_hands` | `neutral` | No Wraith-specific gig or lore link found `[inferred]` | `inferred` |
| Afterlife | `afterlife` | `neutral` | Neutral merc marketplace; Nash appears there as a working solo, which is a personal employment, not a faction welcome `[game-data]` `[wiki]` `[inferred]` | `game-data+inferred` |
| NUSA | `nusa` | `hostile` | The Wraiths' smuggling economy is defined by the **border**: Poppy Farm stored "equipment slated to be smuggled across the border with South California" `[wiki]`; a Wraith crew crossing the state line was marked and shot down by "socal drones" `[wiki]` (Marcinkowsky/Anderson shard); Militech holds handcuffed Wraiths (`cs_handcuffed_wraiths_militech_com`) and the SoCal Border Patrol, a NUSA state force, polices the crossing `[game-data]` `[wiki]`; the mod's alt timeline removes the PL NUSA campaign, so this is the border relationship only `[inferred]` | `game-data+wiki+inferred` |
| NetWatch | `netwatch` | `neutral` | No attested interaction. The Wraiths' net capability is hired freelance (b&#64;d), not NetWatch-facing `[inferred]` | `inferred` |

### 3.3 The three relations that define the faction

1. **Aldecaldos — `war`.** This is the axis the whole faction is built around.
   The Wraiths are "the other nomad group" in the Badlands; the two have "a long
   history of frequent conflict and warring". `[wiki]` The war is symmetrical and
   generational: Wraiths kidnap Aldecaldo leaders and raid camps, Aldecaldos
   assault Wraith strongholds and frame them for Militech theft. Both sides'
   quest content is *about* the other. For a simulation this should be the
   Wraiths' default war target, and it should be a **standing** war rather than
   an event — the sources describe it as a condition, not a campaign.
2. **NCPD — `hostile`.** The city's only lever. Because the Badlands are outside
   the Council's writ, the NCPD bounty is the whole of Night City's policy toward
   the Wraiths: three named cells, three scanner hustles, one dispatcher voice
   naming each boss. `[wiki]` This is **the cleanest "quest-giver against the
   faction" case in the batch** and should be modelled as a bounty board, not a
   patrol war.
3. **Militech — `hostile`.** The predator-prey inversion. The Wraiths' income is
   robbing corp transports; Militech's border policy is to execute captured
   Wraiths. `[game-data]` `[wiki]` Neither side is trying to hold ground. Model
   it as an interdiction loop: each Wraith convoy raid raises the chance of a
   Militech execution scene, and each execution raises Wraith hostility.

The rest of the matrix is thin by design. There is exactly **one** `trade` row
that is a sale (Tyger Claws), **one** that is a hiring channel (Rogue), **one**
`rival` that is a theft (6th Street), and **one** `rival` that is competition in
the same crime (Scavengers). Everything else is either a war, a predation, or
silence. **The Wraiths have no ally, no patron and no client among the coded
factions.**

### 3.4 Actors outside `data/factions.json`

These are real relationships with no faction code, so they are prose only.

- **The Breakers** — the rival Raffen Shiv gang "pressing down on Wraith
  territory" around the cement factory. `[wiki]` This is the Wraiths' most
  important *peer* relationship and it has no code. Blackdust's answer is
  doctrinal: cooperate only while the hauls are weak, then "this is OUR
  backyard". `[wiki]`
- **Raffen Shiv generally** — the supra-group. Wraiths are one gang within it;
  Blackdust admits working "with other raffen groups because of the weak hauls
  down south". `[wiki]` Treat as a shared identity and a recruitment pool, never
  as an alliance.
- **The Toecutters** — another Raffen gang, 2045 Night City/Badlands, leader
  Mohawk. `[wiki]` `[lore]` No attested 2077 contact; keep in prose.
- **"The Hungarian"** — Nash's unnamed creditor. The only attested *external
  principal* in Wraith politics. Do not invent a faction for him. `[wiki]`
- **b&#64;d** — the freelance netrunner who supplied intel and malware, then
  turned on them and killed a pursuing crew with a mined bunker. A supplier who
  became an enemy. `[wiki]`
- **Big Pete and New American Autoworks** — a licensed business and its manager,
  garrisoned by the gang. A client/asset, not a member; his roster `faction_id`
  is `null`. `[game-data]` `[wiki]`
- **Iris Tanner** — a coerced nomad techie. A captive asset, not a member. `[wiki]`
- **"The clinic" of `Current needs`** — the buyer for the factory cell's chrome
  and body parts ("clinic needs… limbs, not picky… optics, FUNCTIONAL"). Unnamed,
  and deliberately so. `[wiki]`
- **Kojo's drug ambition** — `Note #44` wants a lab and "the trade routes" to
  take a glitter analogue cross-country. A plan, not a faction. `[wiki]`
- **Boz** — the 6th Street lieutenant who was Nash's client, and whom Panam
  eventually paid. The only named 6th Street channel. `[wiki]`

### 3.5 Guarantor assessment

The design question: if a player founds a gang, which factions would guarantee
the Wraiths' support, and which would the Wraiths guarantee?

- **Nobody guarantees the Wraiths.** The matrix has no `ally`, `patron` or
  `client` row for a coded faction. Their supply lines are a freelance netrunner,
  a corrupt garage and a named clinic buyer; their protection is distance and
  terrain. A player who takes over a Wraith cell inherits **a customer list and a
  list of creditors**.
- **The Wraiths are a poor guarantor, but a useful one.** They cannot defend a
  client's ground and would not try. What they *can* sell is what they actually
  do: **deniable violence, stolen vehicles, chrome, and cross-border movement**.
  That is a real product for a player-founded gang on a Badlands point, and it is
  cheap. The price is that they will also rob the client if the client looks
  weak — which is the entire Nash/Panam story.
- **The one genuine guarantor is the Aldecaldo war.** A player who fights the
  Aldecaldos has a natural, free ally in the Wraiths, because the Wraiths are
  already at war with them. That is an *alignment of enemies*, not a treaty, and
  it should not require trust.
- **Who might guarantee the Wraiths?** Only their own kind: the Breakers (as a
  rival, not a friend), other Raffen groups (transactionally), and a Militech
  insider of the Gilchrist type. None is attested for the Wraiths in 2077.
- **A player founding on a Wraith point gets a specific war.** The Wraiths are
  more likely to be the **pre-emptive attacker** than the guarantor, exactly as
  the Maelstrom and Barghest docs conclude for their factions — but with one
  difference: the Wraiths have no single leader to negotiate with, so a player
  must **buy, coerce or kill each cell separately**. That is a distinct and
  attractive political problem, and it is the faction's strongest design feature.

---

## 4. Pillar notes

Design claims from `docs/design/gameplay-systems.md`: the Wraiths are a
**Tribe** (archetype strength **Culture**, weakness **Espionage**); faction
strength **Military**, weakness **Politics**.

| Pillar | Design claim | Lore verdict | Evidence |
| --- | --- | --- | --- |
| Military (faction strength) | The Wraiths are militarily strong | **Strongly supported.** The only thing the faction reliably does is violence. Records give a literal tier ladder (`grunt1`→`grunt2`→`warrior3`/`operator3`/`strong_gunner3`, plus `ghost2` snipers and `android2`), a named enemy-tier roster (Marauder, Ravager, Outlaw, Hunter, Ghoul, Skewer, Devil, Revenant, Goliath, Bane, Sniper, Boss Hunter — tier 1 Weak to tier 3 Elite), combat-modified vehicles (Specter, Wendigo, Reaver, Ghoul, Revenant), Wyvern drones over the factory gate, turrets and cameras at the station and autoworks, a Centaur-class garrison in one activity, 300–1,200 members, and an economy that is entirely raid, hijack, ambush and ransom. | `[game-data]` `[wiki]` |
| Politics (faction weakness) | The Wraiths cannot do politics | **Strongly supported — the strongest case in the set.** No 2077 leader; one 2020 name and one killable crew boss; no ally, patron or client; no institution, oath or succession; every internal relationship is exploitative; their one peer relationship (the Breakers) is managed by a shard-voice threat. "No leaders and no recognizable style" is the faction's own description. | Leadership list; 2077DAB; the Breakers shard; Vondell entries `[wiki]` |
| Culture (archetype strength) | A Tribe binds through Culture | **Contradicted, and this is the important correction.** The lore says the Raffen have "no common identity or ethos" and that "nobody would call these groups family – not even in jest". What they share is a **brand** (skull-and-crossbones, combat rigs, a vehicle set) and a **shared exclusion**, both of which repel outsiders more than they bind insiders. Cohesion is predatory hierarchy: hangers-on "traded like cattle", a coerced techie, wounded members "left for dead". Model Culture as **low internal cohesion, high external intimidation** — the inverse of Maelstrom, where the creed genuinely binds. | 2077DAB; Raffen Shiv page; Iris Tanner; Vondell entries `[wiki]` |
| Espionage (archetype weakness) | The Wraiths are bad at espionage | **Half-contradicted, and the useful half is the other one.** Offensively they are competent: they hire freelance netrunners, run a signals-intrusion operation (KI113R at Union Railroad), buy convoy route intel ("got some info off one gonk about the Biotechnica drop"), run "desert scouts", and reconnoitre targets before striking (Nash's note on Panam is a genuine risk assessment). Defensively they are hopeless: b&#64;d turned on them and killed a pursuing crew; an Aldecaldo ambush left two of their own for dead; V walks into every base; a failed client-supplied cloak destroyed a border run. **Model them as good offensive intelligence, no counter-intelligence, no institutional memory.** | Flying Drugs; Haponik and Marcinkowsky shards; Vondell entries; `get ready` `[wiki]` `[game-data]` |
| Overall fit | The pillars fit the faction's identity | **Two of four fit, one is inverted, one needs splitting.** Military and Politics are exactly right. Culture is inverted (intimidation brand, not binding creed). Espionage should be split into offense (fine) and defence (absent). That makes the Wraiths the mirror image of Maelstrom and the cleanest "predator pack" in the model. | Synthesis `[inferred]` |

Design cautions, not redesigns:

- Do **not** give the Wraiths a leader to inherit. Their Politics weakness is
  *structural*, not a missing NPC. A player should have to buy, coerce or kill
  each cell.
- Do **not** model Culture as cohesion. Model it as a **fear brand** that raises
  recruitment from outcasts and lowers every other faction's willingness to
  negotiate. Losing it should cost intimidation, not unity.
- Espionage weakness should be **mechanical and defensive only**: infiltration
  events should reveal a cell's stash, turn a coerced specialist, or let a
  creditor call in a debt. Their offensive intel should work normally.
- The Economy is not a listed pillar for this faction, but note that it is the
  **thinnest in the set**: no shopfront, no licence, no manufacturing, one
  ripperdoc and one garage. Any disruption to the service wing (McBride, Big
  Pete, Union Railroad) should halve their income.

---

## 5. Gaps and uncertainties

### 5.1 Gaps in the politics METHOD

These are improvements the next agent should fold into
[`METHOD.md`](./METHOD.md), not faction trivia.

1. **M13 — The schema cannot express an acephalous faction.** `leaders[]` with a
   `role` string assumes somebody is in charge. The Wraiths have no 2077 leader
   at all, only cells, and the honest representation is eight co-equal
   `role: "cell boss"` rows plus prose. Add a `leadership_model` field
   (`single` | `junta` | `council` | `acephalous` | `confederation`) and say
   that `leaders[]` may legitimately contain peers, not a chain.
2. **M14 — Cell and franchise structures need a home.** METHOD §5's template
   has "internal political factions (blocs)". For a confederation, the blocs
   *are* the command structure. Say explicitly that for acephalous factions
   `internal_factions[]` carries the org chart, and that `members_hint` should
   name places rather than counts.
3. **M15 — Exact-name matching must cover site and community codes, not only
   character records.** `mws_se5_07` (site 324, *Shape of a Pony*) and
   `ma_bls_ina_se5_07` (a community-only SOCA at Tango Tors) differ by two
   characters and by 2.5 km. §2 item 3 warns about `Character.*` collisions
   only. Generalise the rule to every ID namespace and add the worked example.
4. **M16 — Wiki member tables can be wrong about *location*, and the shard's own
   `location=` field is the tiebreaker.** Michael Marcinkowsky is listed "at the
   Poppy Farm"; his shard and actor are at the se5_11 Assault in Progress near
   Lake Farm. The batch rule "read dialogue and descriptions, not titles" needs a
   companion: **trust the shard's `location=` over the member table's prose.**
5. **M17 — A wiki "secondary leader" may be a crew boss, not a deputy.** Nash is
   the sole 2077 name in the Wraiths' leadership list and is never called the
   leader; the wiki also lists him as a plain "Member". Do not promote a
   leadership list into a chain of command. Ask what the person *commands*, not
   what section they are filed under.
6. **M18 — Extend the crowd-pool filter to Phantom Liberty courier communities.**
   `sa_ep1_*_com_combat` and `sa_ep1_*_narrative_com` mix Wraiths, Scavengers
   and Arasaka bodyguards as interchangeable obstacles for one courier job
   (`{sa_ep1_159_narrative_com}`: 5 Wraiths + 4 Arasaka + 2 Scavs). §1.2 item 6
   lists respawn pools, customer crowds and set dressing; add
   `sa_ep1_courier_loop_*` and `sa_ep1_1xx_com_combat` to the list.
7. **M19 — Cross-doc symmetry was not applied to this faction at all.** Every
   sibling doc defaults the Wraiths to `neutral` with "no attested interaction":
   `maelstrom.md`, `sixth-street.md`, `tyger-claws.md`, `biotechnica.md`,
   `valentinos.md`, `arasaka.md`, `voodoo-boys.md`, `barghest.md`, `animals.md`,
   `the-mox.md`, `kang-tao.md`. The Wraith-side evidence contradicts four of
   them: a Maelstrom stash raid (`hostile`), a theft from 6th Street (`rival`), a
   weapons sale to the Tyger Claws (`trade`), and a planned Biotechnica convoy
   robbery (`hostile`). M11 in `barghest.md` already asks for a grep-the-siblings
   step; this faction shows it was never run. Make it a gate: **no doc is
   complete until every faction that defaults you to `neutral` has been checked
   against your own evidence.**
8. **M20 — "Campaign disabled" can leave a faction with zero named NPCs.** Every
   Wraith cell boss is `world-activity` (NCPD scanner or gig) or `story`. Under a
   strict reading the mod must synthesise the entire leadership. The METHOD's
   `open_world` flag cannot express this; add a `named_npc_persistence` note
   (`story-gated` | `scanner-gated` | `ambient` | `none`) so seeders know before
   they plan.
9. **M21 — Peer groups outside `factions.json` are the faction's real rivals.**
   The Breakers are the Wraiths' most important peer and have no code; the
   Raffen Shiv as a whole are their identity and have no code. The METHOD has
   extra rows for `nusa`/`netwatch` but no rule for uncoded **peer** groups that
   carry a war. Add: if an uncoded peer is a war or a primary rivalry, say so in
   prose *and* in the `internal_factions` narrative, and flag the missing code.
10. **M22 — The stance vocabulary hides direction in predation.** Militech,
    NCPD, Biotechnica and 6th Street are all `hostile`, but the Wraiths are the
    aggressor against Militech and Biotechnica, the *target* of NCPD, and the
    thief against 6th Street. `hostile` is correct but directionless. Add an
    `aggressor` / `target` sub-field (an extension of barghest.md's M6
    `revenue_role` idea) so a simulation knows who escalates.

### 5.2 Faction uncertainties

1. **No offline attitude matrix.** `Attitude_Record.hpp` is opaque and the
   `Affiliation` enum is identity only (`Wraiths` = 8). Every stance above is
   judged from quests, shards, the wiki and co-location; none is read from a
   TweakDB relation row.
2. **Three cell bosses are inferred by elimination.** Ward
   (`Character.ma_bls_ina_se1_17_outpost_miniboss`), Craven
   (`Character.ma_std_rcr_18_outpost_miniboss`) and McBride
   (`Character.ma_bls_ina_se5_07_outpost_miniboss`) are each the sole `miniboss`
   of the community of the activity the wiki names them in. Strong by context,
   weak by name. Verify in-game before seeding them as canon.
3. **Nash's Afterlife cameo is odd.** `Character.q103_raffen_nash` appears as
   registry entry `nash` in `{q005_com_slice_of_afterlife}` at the Afterlife
   (`-1431.0, 1056.0`, spot `#q005_ws_nash_scene`). That is a scripted scene in
   `The Heist` (`q005_heist`), not a free-roam appearance, and the design's §7
   alternate timeline deletes `The Heist`. Do not cite it as open-world presence.
4. **The Vondell records are inferred.** No `vondell`/`dove`/`spite` record exists
   in the registry or rosters. The only Rancho Coronado glamdoc pair is
   `Character.std_rcr_glamdoc_01` and `Character.std_rcr_glamdoc2_01`, which
   matches Hoisted Colors' two owners. Plausible, not proven.
5. **Blackdust, Kojo, Susan Parker, Marley Anderson, viper, Plumber Joe, Morris,
   karl, Rita Sweden and Rip Turman have no actors at all.** They are shard
   voices. Any simulation that wants them must synthesise them, and any seeding
   must not look for their records.
6. **George, Desi and Timothy are record names with no lore.** They are the only
   named actors in otherwise generic highway communities of five to seven
   Wraiths, so they are cell bosses by elimination — but no wiki page, shard or
   quest names them. Do not write them into dialogue as if they were characters.
7. **The cement factory's cell has no actor records.** It is marker-only (no
   `sites.json` row), so its "garrison" is five overlapping `sq004` quest-phase
   communities, not a persistent roster. 51 entries is an upper bound, not a
   headcount.
8. **The Breakers have no 2077 records and no page beyond three sentences.** The
   "pressing down on Wraith territory" line is from the factory's own computer.
   Treat the Breakers as an off-map pressure, not a modelled faction.
9. **"The Hungarian" is deliberately unnamed.** Do not assign him to a corp or a
   gang. He is the model for an external creditor, not a character.
10. **The clinic buyer in `Current needs` is unnamed.** The shopping list proves a
    chrome/body-part buyer exists and says what they want; it does not say who.
11. **The Wraiths' economy has no `raid`/`loot` revenue code** (the location doc
    flagged this too). `mercenary` is the closest fit and is used everywhere.
12. **The Aldecaldo war is entirely quest-gated.** `Ghost Town` is a main job,
    `Riders on the Storm` and `Queen of the Highway` are side jobs in Panam's
    chain. The design removes the Relic plot, which may remove the chain. The
    war is canonical in lore and must be modelled regardless; the *set pieces*
    may not exist.
13. **`open_world` is a heuristic, and here it is load-bearing.** All named
    Wraiths are scanner- or gig-gated. If the mod disables scanner content, the
    faction has no named NPCs. This is a spawn-check item, not a paperwork item.
14. **Co-location with Scavengers in Phantom Liberty pools is not an alliance.**
    `{sa_ep1_124_com_combat}` (3 Scavs + 3 Wraiths) and
    `{sa_ep1_159_narrative_com}` are courier-job obstacle pools. Excluded from
    the relation judgement.
15. **`areas.jsonl.district_code` mislabels one Wraith area.** `ma_pac_wwd_08_com`
    reads `dogtown` but is in West Wind Estate (Pacifica). It is not a Dogtown
    foothold and gives no Barghest relation. Same class of artifact the location
    doc documents at §2.3.
16. **The 20-strong Rancho Coronado cell is the faction's largest single
    community.** Twenty of 327 Wraith entries sit at one city corner. That is a
    deliberate exposure, not an accident: it is the only place the gang lives
    inside a rival's district.
17. **The `sq027` numbers are an assault, not a garrison.** 30 Wraith entries at
    the Aldecaldo camp are attackers in `Queen of the Highway`; three separate
    communities (`raffen_shiv_raid`, `raffen_reinf`, `nash_group`). Do not count
    them as Wraith territory.

### 5.3 Sources consulted

- Local: `data/factions.json`, `data/sites/rosters.json`,
  `data/sites/sites.json`, `data/sites/phases.json`,
  `data/factions.json`, `dist/extract/areas.jsonl`,
  `dist/extract/markers.jsonl`,
  `dist/extract/raw/**/always_loaded_{0,1,2}.streamingsector.json`
  (`worldCommunityRegistryItem` templates: 27,411 entries parsed, 10,324 in
  `always_loaded_1`), `refs/RED4ext.SDK/.../game/data/Affiliation.hpp`,
  `refs/RED4ext.SDK/.../game/data/Attitude_Record.hpp`.
- Wiki: [Wraiths](https://cyberpunk.fandom.com/wiki/Wraiths),
  [Wraiths Members](https://cyberpunk.fandom.com/wiki/Wraiths_Members),
  [Raffen Shiv](https://cyberpunk.fandom.com/wiki/Raffen_Shiv),
  [Nash](https://cyberpunk.fandom.com/wiki/Nash),
  [Dogkiller](https://cyberpunk.fandom.com/wiki/Dogkiller),
  [Breakers](https://cyberpunk.fandom.com/wiki/Breakers),
  [Toecutters](https://cyberpunk.fandom.com/wiki/Toecutters),
  [Bruce Ward](https://cyberpunk.fandom.com/wiki/Bruce_Ward),
  [Paul Craven](https://cyberpunk.fandom.com/wiki/Paul_Craven),
  [Rufus McBride](https://cyberpunk.fandom.com/wiki/Rufus_McBride),
  [Arnold Haponik](https://cyberpunk.fandom.com/wiki/Arnold_Haponik),
  [Michael Marcinkowsky](https://cyberpunk.fandom.com/wiki/Michael_Marcinkowsky),
  [Dove Vondell](https://cyberpunk.fandom.com/wiki/Dove_Vondell),
  [Spite Vondell](https://cyberpunk.fandom.com/wiki/Spite_Vondell),
  [Big Pete](https://cyberpunk.fandom.com/wiki/Big_Pete),
  [Iris Tanner](https://cyberpunk.fandom.com/wiki/Iris_Tanner),
  [b@d](https://cyberpunk.fandom.com/wiki/B@d),
  [Corp-Bud Cement Factory](https://cyberpunk.fandom.com/wiki/Corp-Bud_Cement_Factory),
  [Corp-Bud Cement Factory/Computers](https://cyberpunk.fandom.com/wiki/Corp-Bud_Cement_Factory/Computers),
  [Union Railroad Station](https://cyberpunk.fandom.com/wiki/Union_Railroad_Station),
  [Union Railroad Station/Computers](https://cyberpunk.fandom.com/wiki/Union_Railroad_Station/Computers),
  [Rocky Ridge](https://cyberpunk.fandom.com/wiki/Rocky_Ridge),
  [Poppy Farm](https://cyberpunk.fandom.com/wiki/Poppy_Farm),
  [Wraiths Outpost](https://cyberpunk.fandom.com/wiki/Wraiths_Outpost),
  [Wraiths Outpost/Computers](https://cyberpunk.fandom.com/wiki/Wraiths_Outpost/Computers),
  [New American Autoworks (Jackson Plains)](https://cyberpunk.fandom.com/wiki/New_American_Autoworks_(Jackson_Plains)),
  [Megapax Export](https://cyberpunk.fandom.com/wiki/Megapax_Export),
  [SoCal Border Patrol](https://cyberpunk.fandom.com/wiki/SoCal_Border_Patrol),
  [Tango Tors Motel](https://cyberpunk.fandom.com/wiki/Tango_Tors_Motel),
  Wraith enemy-tier pages: [Marauder](https://cyberpunk.fandom.com/wiki/Marauder_(Wraiths)),
  [Ravager](https://cyberpunk.fandom.com/wiki/Ravager_(Wraiths)),
  [Outlaw](https://cyberpunk.fandom.com/wiki/Outlaw_(Wraiths)),
  [Hunter](https://cyberpunk.fandom.com/wiki/Hunter_(Wraiths)),
  [Ghoul](https://cyberpunk.fandom.com/wiki/Ghoul_(Wraiths)),
  [Skewer](https://cyberpunk.fandom.com/wiki/Skewer_(Wraiths)),
  [Devil](https://cyberpunk.fandom.com/wiki/Devil_(Wraiths)),
  [Revenant](https://cyberpunk.fandom.com/wiki/Revenant_(Wraiths)),
  [Goliath](https://cyberpunk.fandom.com/wiki/Goliath_(Wraiths)),
  [Bane](https://cyberpunk.fandom.com/wiki/Wraiths_Bane),
  [Sniper](https://cyberpunk.fandom.com/wiki/Wraiths_Sniper),
  [Boss Hunter](https://cyberpunk.fandom.com/wiki/Wraiths_Boss_Hunter);
  quests and activities: [Ghost Town](https://cyberpunk.fandom.com/wiki/Ghost_Town),
  [Riders on the Storm](https://cyberpunk.fandom.com/wiki/Riders_on_the_Storm),
  [Queen of the Highway](https://cyberpunk.fandom.com/wiki/Queen_of_the_Highway),
  [The Hunt](https://cyberpunk.fandom.com/wiki/The_Hunt),
  [With a Little Help from My Friends](https://cyberpunk.fandom.com/wiki/With_a_Little_Help_from_My_Friends),
  [The Heist](https://cyberpunk.fandom.com/wiki/The_Heist),
  [Gig: Flying Drugs](https://cyberpunk.fandom.com/wiki/Gig:_Flying_Drugs),
  [Gig: Big Pete's Got Big Problems](https://cyberpunk.fandom.com/wiki/Gig:_Big_Pete%27s_Got_Big_Problems),
  [Gig: No Fixers](https://cyberpunk.fandom.com/wiki/Gig:_No_Fixers),
  [Gig: Trevor's Last Ride](https://cyberpunk.fandom.com/wiki/Gig:_Trevor%27s_Last_Ride),
  [Shape of a Pony](https://cyberpunk.fandom.com/wiki/Shape_of_a_Pony),
  [Killing In The Name](https://cyberpunk.fandom.com/wiki/Killing_In_The_Name),
  [Suspected Organized Crime Activity (Rocky Ridge)](https://cyberpunk.fandom.com/wiki/Suspected_Organized_Crime_Activity_(Rocky_Ridge)),
  [Suspected Organized Crime Activity (Jackson Plains)](https://cyberpunk.fandom.com/wiki/Suspected_Organized_Crime_Activity_(Jackson_Plains)),
  [Suspected Organized Crime Activity: Desperate Sons-of-Bitches](https://cyberpunk.fandom.com/wiki/Suspected_Organized_Crime_Activity:_Desperate_Sons-of-Bitches),
  [Reported Crime: Dredged Up](https://cyberpunk.fandom.com/wiki/Reported_Crime:_Dredged_Up);
  shards: [Current needs](https://cyberpunk.fandom.com/wiki/Current_needs),
  [Aldecaldos? Panam Palmer?](https://cyberpunk.fandom.com/wiki/Aldecaldos%3F_Panam_Palmer%3F),
  [get ready](https://cyberpunk.fandom.com/wiki/Get_ready),
  [Official Order #912317 AJ-98](https://cyberpunk.fandom.com/wiki/Official_Order_912317_AJ-98),
  [Hello gonk!](https://cyberpunk.fandom.com/wiki/Hello_gonk!),
  [Message from Kojo to Iris Tanner](https://cyberpunk.fandom.com/wiki/Message_from_Kojo_to_Iris_Tanner),
  [Archived Conversation: Arnold Haponik and Susan Parker](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Arnold_Haponik_and_Susan_Parker),
  [Archived Conversation: Michael Marcinkowsky and Marley Anderson](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Michael_Marcinkowsky_and_Marley_Anderson),
  [Archived Conversation: Simon Diaz and Rufus McBride](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Simon_Diaz_and_Rufus_McBride),
  [Archived Conversation: Rita Sweden and Rip Turman](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Rita_Sweden_and_Rip_Turman);
  institutions: [Aldecaldos](https://cyberpunk.fandom.com/wiki/Aldecaldos),
  [Dakota Smith](https://cyberpunk.fandom.com/wiki/Dakota_Smith),
  [Boz](https://cyberpunk.fandom.com/wiki/Boz),
  [Saul Bright](https://cyberpunk.fandom.com/wiki/Saul_Bright),
  [Carol Emeka](https://cyberpunk.fandom.com/wiki/Carol_Emeka),
  [Militech Detention Center](https://cyberpunk.fandom.com/wiki/Militech_Detention_Center).
- Earlier repo research: `docs/research/factions/wraiths.md`,
  `docs/research/factions/aldecaldos.md`,
  `docs/design/gameplay-systems.md`,
  `docs/research/factions/politics/{METHOD,maelstrom,barghest,militech}.md`.

---

## 6. Machine-readable block

```json
{
  "faction_code": "wraiths",
  "leaders": [
    {
      "name": "Nash",
      "role": "Crew boss at the Corp-Bud Mine; the only 2077 name in the wiki's leadership list ('Secondary Leader'); indebted to an unnamed Hungarian creditor; dies on every branch",
      "character_record_id": "Character.q103_raffen_nash",
      "location_name": "Corp-Bud Mine (boss fight) / Aldecaldo camp assault / Afterlife (scripted cameo only)",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_1 registry entries: nash in {q005_com_slice_of_afterlife} (spot #q005_ws_nash_scene, The Heist cameo); miniboss_bear in {q103_com_mine_ambush_raffen_shiv} (phase bossfight, spot #q103_ws_mine_ambush_bear); nash in {sq027_com_nash_group} (spot #sq027_ws_raffen_shiv_nash_group_nash); wiki Nash; Ghost Town; Queen of the Highway",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Dogkiller",
      "role": "2020 leader of the Wraiths; rumored to wear clothing of human skin; no 2077 presence",
      "character_record_id": null,
      "location_name": null,
      "presence_class": "historical",
      "open_world": false,
      "source": "wiki Dogkiller; Cyberpunk 2020 Night City sourcebook p.35 (via wiki); Wraiths Members",
      "confidence": "wiki+lore"
    },
    {
      "name": "Blackdust",
      "role": "Cement-factory chief: receives scouting reports, sets strategy, claims primacy over other Raffen Shiv; shard voice only, absent from the wiki leadership list",
      "character_record_id": null,
      "location_name": "Corp-Bud Cement Factory",
      "presence_class": "mentioned",
      "open_world": false,
      "source": "Corp-Bud Cement Factory/Computers: 'Scouting report' (Plumber Joe to Blackdust) and 'regarding the Breakers' (Blackdust to viper)",
      "confidence": "wiki"
    },
    {
      "name": "Bruce Ward",
      "role": "High-ranking member and cell leader; multiple robberies; planned a Biotechnica radioactive-waste convoy robbery",
      "character_record_id": "Character.ma_bls_ina_se1_17_outpost_miniboss",
      "location_name": "I-9, south-east of DaKota, Rocky Ridge",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "raw registry entry mini_boss in {ma_bls_ina_se1_17_com} -> Character.ma_bls_ina_se1_17_outpost_miniboss (sole miniboss; inferred by elimination per METHOD 1.2 item 4); {ma_bls_ina_se1_17_com} cluster at 2868.0,-1010.4; wiki Bruce Ward; Suspected Organized Crime Activity (Rocky Ridge) baseid ma_bls_ina_se1_17; get ready",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "name": "Paul Craven",
      "role": "Cell leader; known leader of a Night City human trafficking ring; corporate convoy hijacker",
      "character_record_id": "Character.ma_std_rcr_18_outpost_miniboss",
      "location_name": "Sequoia and Gray, Rancho Coronado",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "raw registry entry miniboss in {ma_std_rcr_18_com_wraiths} -> Character.ma_std_rcr_18_outpost_miniboss (sole miniboss; inferred); roster site 170 (33 units incl. 10 hostages hostage_01..10 and one android); wiki Paul Craven; SOCA Desperate Sons-of-Bitches baseid ma_std_rcr_18",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "name": "Rufus McBride",
      "role": "Unlicensed ripperdoc sheltering among the gang; three counts of permanent disability and one staged suicide; NCPD bounty",
      "character_record_id": "Character.ma_bls_ina_se5_07_outpost_miniboss",
      "location_name": "Tango Tors Motel, Sage Gulch Road, Jackson Plains",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "raw registry entry #ma_bls_ina_se5_07_npc_06 in {ma_bls_ina_se5_07_com} -> Character.ma_bls_ina_se5_07_outpost_miniboss (sole miniboss; inferred); community at -269.3,-4884.4; wiki Rufus McBride; SOCA Jackson Plains baseid ma_bls_ina_se5_07 (note: NOT site 324 mws_se5_07)",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "name": "Michael Marcinkowsky",
      "role": "Stash guard and smuggler pilot; his crew was marked and shot down crossing the SoCal border after a faulty client-supplied cloaking device",
      "character_record_id": "Character.ma_bls_ina_se5_11_michael",
      "location_name": "Assault in Progress south-south-east of Lake Farm, Laguna Bend Reservoir",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "raw registry entry ganger_05 in {ma_bls_ina_se5_11_com} -> Character.ma_bls_ina_se5_11_michael; community at 732.5,-3949.3; shard baseid ma_bls_ina_se5_11_onscreen_01; wiki Michael Marcinkowsky (member table wrongly places him at Poppy Farm)",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Arnold Haponik",
      "role": "Crew enforcer; collecting a debt from a 'numbers guy' who skimmed a Tyger Claws weapons sale",
      "character_record_id": "Character.ma_bls_ina_se5_13_arnold",
      "location_name": "Fuel station west of Jackson Plains Regional Airport",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "raw registry entry ganger_03 in {ma_bls_ina_se5_13_com} -> Character.ma_bls_ina_se5_13_arnold; community at -1687.2,-4983.6; shard baseid ma_bls_ina_se5_13_onscreen_01; wiki Arnold Haponik",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Kojo",
      "role": "Wraiths Outpost boss; hires then coerces outside specialists; wants to move into drug manufacture",
      "character_record_id": null,
      "location_name": "Wraiths Outpost, Night City Municipal Landfill (Edgewood Ln.)",
      "presence_class": "mentioned",
      "open_world": false,
      "source": "Wraiths Outpost/Computers 'Job' and 'Note #44'; Message from Kojo to Iris Tanner (baseid sts_bls_ina_06_shard_02); Gig: No Fixers",
      "confidence": "wiki"
    },
    {
      "name": "George",
      "role": "Highway-cell boss; record name only, no wiki page, shard or quest names him",
      "character_record_id": "Character.ma_bls_ina_se5_12_george",
      "location_name": "Badlands se5 highway cell",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "raw registry entry ganger_03 in {ma_bls_ina_se5_12_com} -> Character.ma_bls_ina_se5_12_george; community at -804.3,-5709.1 (6 Wraiths)",
      "confidence": "game-data+inferred"
    },
    {
      "name": "Desi",
      "role": "Highway-cell boss; record name only, no wiki page, shard or quest names him",
      "character_record_id": "Character.ma_bls_ina_se5_03_desi",
      "location_name": "Badlands se5 highway cell",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "raw registry entry ganger_003 in {ma_bls_ina_se5_03_com} -> Character.ma_bls_ina_se5_03_desi; community at -755.0,-3642.7 (7 Wraiths)",
      "confidence": "game-data+inferred"
    },
    {
      "name": "Timothy",
      "role": "Highway-cell boss; record name only, no wiki page, shard or quest names him",
      "character_record_id": "Character.ma_bls_ina_se5_16_timothy",
      "location_name": "Badlands se5 highway cell",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "raw registry entry ganger_02 in {ma_bls_ina_se5_16_com} -> Character.ma_bls_ina_se5_16_timothy; community at -470.8,-5663.7 (5 Wraiths)",
      "confidence": "game-data+inferred"
    },
    {
      "name": "Dove Vondell",
      "role": "Deserter. Former Wraith; left for dead by her own crew in an Aldecaldo ambush; now co-owner of the Hoisted Colors glamdoc shop",
      "character_record_id": "Character.std_rcr_glamdoc_01",
      "location_name": "Hoisted Colors, Coronado Dam, Rancho Coronado",
      "presence_class": "ambient",
      "open_world": true,
      "source": "wiki Dove Vondell database entry ('Ambushed by the Aldecaldos and left for dead by their fellow Wraiths'); record inferred from the only two-actor Rancho Coronado glamdoc pair, std_rcr_glamdoc_01 and std_rcr_glamdoc2_01 at #std_rcr_glamdoc_01_aispot / #std_rcr_glamdoc2_01_aispot_02",
      "confidence": "wiki+inferred"
    },
    {
      "name": "Spite Vondell",
      "role": "Deserter. Former 'Wraith enforcer and desert scout'; left for dead with her twin; co-owner of Hoisted Colors; 'compassion gets you killed'",
      "character_record_id": "Character.std_rcr_glamdoc2_01",
      "location_name": "Hoisted Colors, Coronado Dam, Rancho Coronado",
      "presence_class": "ambient",
      "open_world": true,
      "source": "wiki Spite Vondell database entry; record inferred from the Rancho Coronado glamdoc pair (see Dove Vondell)",
      "confidence": "wiki+inferred"
    },
    {
      "name": "Big Pete (Pete Kowalski)",
      "role": "Client, not a member. Manager of New American Autoworks; fixes clunkers for the Wraiths; sold them a faulty Militech cloaking device; contract out on him",
      "character_record_id": "Character.ina_02_new_big_pete",
      "location_name": "New American Autoworks, Sage Gulch Rd., Jackson Plains",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "roster site 340 entry big_pete -> Character.ina_02_new_big_pete, faction_id null; {ina_02_com_gangers} (9 Wraith units); wiki Big Pete; Gig: Big Pete's Got Big Problems baseid sts_bls_ina_02",
      "confidence": "game-data+wiki"
    }
  ],
  "internal_factions": [
    {
      "name": "The cement-factory cell",
      "leader": "Blackdust",
      "goals": "Hold the one true stronghold, raid Night City's outskirts, keep the Breakers and other Raffen out, and sell chrome and body parts to an unnamed clinic buyer",
      "members_hint": "sq004_com_wall 18, sq004_com_raiders 10, sq004_com_chase_enemies 10, sq004_com_main 8, sq004_com_reinforcements 5; drone records at the gate; prison and basement gutting room. Quest-phase communities, not a headcount",
      "source": "Corp-Bud Cement Factory/Computers ('Scouting report', 'regarding the Breakers', 'Current needs'); Riders on the Storm; 2077 World Book p.183 via wiki",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Nash's crew (mine and Rocky Ridge)",
      "leader": "Nash",
      "goals": "Pull one big score to clear the Hungarian debt: the Thorton Warhorse plus a 6th Street shipment; keep the mine hideout and the secret Rocky Ridge office",
      "members_hint": "q103_com_mine_ambush_raffen_shiv 11 plus 3 reinforcements; sq027_com_nash_group 7; q103_com_raffen_shiv 7 at Rocky Ridge",
      "source": "wiki Nash; Aldecaldos? Panam Palmer? shard (q103_nash_shard); Ghost Town; Queen of the Highway",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Ward's I-9 raiders",
      "leader": "Bruce Ward",
      "goals": "Rob a Biotechnica convoy carrying radioactive waste; keep robbing convoys in the I-9 corridor",
      "members_hint": "{ma_bls_ina_se1_17_com}: 9 Wraiths including one mini_boss, two Achilles snipers and one HMG gunner",
      "source": "SOCA Rocky Ridge dispatcher text; get ready; Official Order #912317 AJ-98; wiki Bruce Ward",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Craven's trafficking ring",
      "leader": "Paul Craven",
      "goals": "Move people and hijack corporate convoys; hold a permanent city corner inside 6th Street's district",
      "members_hint": "{ma_std_rcr_18_com_wraiths}: 20 Wraiths (19 human plus 1 android) plus 10 hostages; roster site 170 with 33 units",
      "source": "SOCA Desperate Sons-of-Bitches dispatcher text; wiki Paul Craven; Tonight; roster site 170",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The service wing",
      "leader": "Rufus McBride",
      "goals": "Convert loot into money: unlicensed surgery, chrome extraction, chop work, parts, and drone cargo theft; keep outside specialists paid enough not to flee",
      "members_hint": "Tango Tors cell; New American Autoworks garrison (9 units, 11 doors, 4 devices); Union Railroad antenna crew (16 units); b@d as a freelance supplier; Big Pete as a client",
      "source": "wiki Rufus McBride and Big Pete; Current needs; Simon Diaz shard; Gig: Flying Drugs; Union Railroad Station/Computers",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Kojo's outpost crew",
      "leader": "Kojo",
      "goals": "Forced labour now, drug manufacture and cross-country distribution later: 'we got the trade routes, all we gotta do is use em'",
      "members_hint": "{ina_06_com}: 9 entries / 7 Wraith roster units; the hostage building; the garage",
      "source": "Message from Kojo to Iris Tanner; Wraiths Outpost/Computers 'Job' and 'Note #44'; Gig: No Fixers",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The highway cells",
      "leader": "George",
      "goals": "Ambush travellers and convoys and survive; no programme beyond the next haul",
      "members_hint": "16 ambient communities across ma_bls_ina_se1_11..21 and se5_03..16, 87 entries, 5-7 Wraiths each; records George, Desi and Timothy are their only named actors; several carry la_sm_execution_03 Militech execution scenes",
      "source": "areas.jsonl; raw registry; wraiths.md section 2.2",
      "confidence": "game-data+inferred"
    },
    {
      "name": "The deserters (Vondell twins)",
      "leader": "Dove Vondell",
      "goals": "Leave the gang and stay out: run a glamdoc shop, serve whoever pays, never go back. Split between Dove's serve-everyone line and Spite's court-NUSA line",
      "members_hint": "Two glamdoc actors at Coronado Dam, Rancho Coronado; explicitly 'left for dead by their fellow Wraiths'",
      "source": "wiki Dove Vondell and Spite Vondell database entries; Update 2.5 vendor content",
      "confidence": "wiki+game-data+inferred"
    }
  ],
  "relations": [
    {
      "faction_code": "tyger_claws",
      "stance": "trade",
      "evidence": "The Wraiths sold weapons to the Tyger Claws ('remember when we sold them that iron? ... that time mikey almost bit the dust carrying them over'), and a Wraith numbers guy overcharged them five percent and pocketed it [wiki] (Haponik/Parker shard, baseid ma_bls_ina_se5_13_onscreen_01). The Tyger Claws doc records this pair as neutral and missed the sale [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "valentinos",
      "stance": "neutral",
      "evidence": "No attested interaction; different district. Do not infer a rivalry from both being gangs [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "arasaka",
      "stance": "neutral",
      "evidence": "Only co-location is the Phantom Liberty courier-loop enemy pool sa_ep1_159_narrative_com (5 Wraiths, 4 Arasaka bodyguards, 2 Scavs as interchangeable obstacles for one courier job), which is a crowd pool not an alliance [game-data]; Wraiths raid weakly guarded corp transports generically [wiki]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "militech",
      "stance": "hostile",
      "evidence": "Militech executes captured Wraiths: cs_militech_execution*, cs_handcuffed_wraiths_militech*, and a Wraith corpse with role victim at the ma_bls_ina_se1_04 scene alongside five Tyger Claws and five Militech units [game-data]; the Wraiths' own scouting report says Militech patrols stick to their facility [wiki]; Wraiths prey on corp convoys and the SoCal border is Militech-policed [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "kang_tao",
      "stance": "neutral",
      "evidence": "No attested interaction. The q104 AV chase through Jackson Plains is removed by the design's section 7 alternate timeline [wiki] [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "biotechnica",
      "stance": "hostile",
      "evidence": "Bruce Ward's cell planned to rob a Biotechnica convoy carrying radioactive waste: 'Got some info off one gonk about the Biotechnica drop. Here's the route ... jump the transport and take the cargo. Shit's radioactive.' [wiki] (get ready shard, held by Ward); the Highway 101 nest sits in Biotechnica Flats; Poppy Farm was a Biotechnica TradFarm before it became a Wraith stash [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "petrochem",
      "stance": "neutral",
      "evidence": "Only the Shape-of-a-Pony camp's description ('a makeshift garage south of the EBM Petrochem Stadium'), a landmark not an interaction [wiki] [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "barghest",
      "stance": "neutral",
      "evidence": "No attested interaction. ma_pac_wwd_08_com is labelled dogtown in areas.jsonl but sits in West Wind Estate (Pacifica): a district-code artifact, not a Dogtown presence [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "sixth_street",
      "stance": "rival",
      "evidence": "Nash stole 'a shipment for the 6th Street gang' while betraying Panam [wiki]; Panam then delivered a package to 6th Street lieutenant Boz at the Sunset Motel, inside Wraith country [wiki]; the 20-strong Craven cell operates at Sequoia and Gray in Rancho Coronado, 6th Street's district, 22 m from a 6th Street control centre [game-data]. The 6th Street doc records neutral and missed the theft [inferred]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "aldecaldos",
      "stance": "war",
      "evidence": "A long history of frequent conflict and warring [wiki]; the Wraiths kidnapped Saul Bright and held him at the cement factory (Riders on the Storm) [wiki]; sq027 spawns 30 Wraith entries assaulting the Aldecaldo camp, with Nash's group (7) and four reinforcement cars [game-data] [wiki]; the Aldecaldos retaliate at the cement factory and the mine and Cassidy left incriminating Militech gear outside the factory to frame them [wiki]; Trevor Brass was killed at a Wraith nest and his family are Aldecaldo [wiki]; the Vondell twins were ambushed by the Aldecaldos and left for dead by their own crew [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "animals",
      "stance": "neutral",
      "evidence": "No attested interaction; only spatial (a Wraith hustle 6.7 m from an Animals community in West Wind Estate) [game-data] [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "the_mox",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "maelstrom",
      "stance": "hostile",
      "evidence": "b@d sold the Wraiths intel on a Maelstrom drug stash and the Wraiths raided it at the Megapax Export warehouse on Leru Street, Northside; Maelstrom was caught off-guard, one member escaped wounded into the sewers, and the warehouse was abandoned (Reported Crime: Dredged Up; Grizzle/Ryder and Kenton/Wrey shards) [wiki] [game-data]; {ma_wat_nid_10_com} still holds 6 Wraiths [game-data]. The Maelstrom doc records neutral and missed the raid [inferred]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "voodoo_boys",
      "stance": "neutral",
      "evidence": "No attested interaction; the Shape-of-a-Pony camp is 288 m from a Voodoo Boys control centre (cc_dt_terra_cognita), adjacency only [game-data] [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "ncpd",
      "stance": "hostile",
      "evidence": "NCPD dispatches three SOCAs against named Wraith cells (Ward, Craven, McBride) and names each cell leader in the bounty text [wiki] [game-data]; Wraiths are the subject of Assault in Progress, Reported Crime and la_sm_execution_03 scenes across 16 highway communities [game-data]; 'the Wraiths ignored the law' [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "night_corp",
      "stance": "neutral",
      "evidence": "No attested interaction; a corp, not a turf actor [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "city_council",
      "stance": "neutral",
      "evidence": "No attested interaction. The Badlands lie outside the Council's writ, which is why the only city instrument against the Wraiths is an NCPD bounty [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "scavengers",
      "stance": "rival",
      "evidence": "Same trade: 'similar to the Scavengers, the Wraiths would also kidnap people and kill them for their bodyparts and chrome' [wiki]; the Wraiths hit a Scav den in West Wind Estate (ma_pac_wwd_02_wraiths_com beside ma_pac_wwd_02_scavs_com, 3 Wraiths vs 8 Scavs) [game-data]; shared Phantom Liberty courier pools are interchangeable enemies, not an alliance [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_regina",
      "stance": "neutral",
      "evidence": "No Wraith-specific gig found. Her district is Watson/Northside, where the Wraiths raided a Maelstrom stash, but that is not her operation [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_wakako",
      "stance": "neutral",
      "evidence": "No Wraith-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_padre",
      "stance": "neutral",
      "evidence": "No Wraith-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_el_capitan",
      "stance": "hostile",
      "evidence": "Shape of a Pony: Muamar sends V to recover a Porsche from 'several Wraiths surrounding the car' after the seller vanished; the Wraiths stole an AUTOFIXER vehicle [wiki] [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_dakota",
      "stance": "hostile",
      "evidence": "She issues every Badlands gig against the gang: Flying Drugs, Big Pete's Got Big Problems, No Fixers, Trevor's Last Ride [wiki] [game-data]; she is an Aldecaldo, so the hostility is structural, and the Wraiths are the Raffen Shiv in her 'ecosystem' speech [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_dino",
      "stance": "neutral",
      "evidence": "No Wraith-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_rogue",
      "stance": "trade",
      "evidence": "Nash worked for Rogue as a merc and was paired with Panam, which is how the betrayal happened [wiki]; his registry entry appears in the Afterlife {q005_com_slice_of_afterlife} community [game-data]; a hiring channel, not loyalty, since she backs Panam against him afterwards [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_mr_hands",
      "stance": "neutral",
      "evidence": "No Wraith-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "afterlife",
      "stance": "neutral",
      "evidence": "Neutral merc marketplace; Nash appears there as a working solo (scripted The Heist cameo), which is personal employment, not a faction welcome [game-data] [wiki] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "nusa",
      "stance": "hostile",
      "evidence": "The Wraiths' smuggling economy is defined by the border: Poppy Farm stored 'equipment slated to be smuggled across the border with South California' [wiki]; a Wraith crew crossing the state line was marked and shot down by 'socal drones' [wiki] (Marcinkowsky/Anderson shard); Militech holds handcuffed Wraiths (cs_handcuffed_wraiths_militech_com) and the SoCal Border Patrol, a NUSA state force, polices the crossing [game-data] [wiki]. The design's alt timeline removes the PL NUSA campaign, so this is the border relationship only [inferred]",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "faction_code": "netwatch",
      "stance": "neutral",
      "evidence": "No attested interaction; the Wraiths' net capability is hired freelance (b@d), not NetWatch-facing [inferred]",
      "confidence": "inferred"
    }
  ]
}
```
