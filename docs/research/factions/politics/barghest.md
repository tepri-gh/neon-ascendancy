# Barghest — Leadership, Internal Politics and External Relations

Status: faction research run, 2026-11-25. One faction, one document.
Scope: Cyberpunk 2077 2.5 + Phantom Liberty, campaign disabled. Who a player can
join under, climb past, ally with or remove inside Kurt Hansen's militia; the
internal blocs; the Dogtown civil/economic layer the militia governs; and the
external relations matrix needed for wars, alliances and "guarantor" support
when a player founds a gang.

Method: this document follows
[`METHOD.md`](./METHOD.md) (the politics playbook, including its §1.1
corrections) and the evidence rules in
[`../METHOD.md`](../METHOD.md) (tags, local-data precedence, wiki usage). The
location catalog for Barghest is [`../barghest.md`](../barghest.md); this
document does not repeat it — it maps people and politics onto those places.
New here: the raw sector extracts
(`dist/extract/raw/**/always_loaded_*.streamingsector.json`) are parsed for
`worldCommunityRegistryItem` entries to recover the named-NPC character
records that `data/sites/rosters.json` does not contain (Barghest has 4 roster
sites / 87 units for 1,449 area records, so rosters are nearly useless here).

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/comic/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My reasoning links a named person, place or stance to a record; reasoning stated | Weak, flagged |

Extra conventions for this document:

- **Presence class** (METHOD §1.2 item 2, which superseded the four-class list
  while this doc was being written). `ambient` = persists in free roam without
  a quest; `world-activity` = gig, scanner hustle, side/minor job or NCPD
  activity, i.e. free-roam content but still activity-gated; `story` = gated by
  the Phantom Liberty chain (`q301`–`q304`, `mq301`, `mq304`); `prologue` =
  a lifepath intro (none here); `off-map` = alive in lore but never spawned;
  `mentioned` = named only in shards or dialogue; `historical` = not present in
  2077. The JSON `open_world` flag is `true` for `ambient` + `world-activity`,
  `false` for everything else. Fae Nesheim and Leonardo Ware are `mentioned`:
  they act in 2077 text but have no actor record at all.
- **Rank is literal.** Barghest is the one Night City gang whose members hold
  real military ranks and are addressed by them. `Colonel`, `Lieutenant
  Colonel`, `Major`, `Captain`, `Sergeant` and `Private` all appear in game
  text, so a "rank ladder" here is not an inference.

---

## 1. Leadership and ranks

### 1.1 The 2077 chain of command

Barghest is a **militia**, not a street gang and not a corporation. It has one
commander, a small veteran elite, a conventional officer corps, and a mass of
recruits. The chain below is the 2077 state, before Hansen's death.

| Name | 2077 role | Character record | Location / influence point | Presence class | Source | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| **Kurt Hansen** | Colonel; founder, commander and de facto ruler of Dogtown | `Character.kurtz`; boss variant `Character.q304_kurt_miniboss`; memory variant `Character.kurt_hallucination` | Black Sapphire (floor 99), EBM Stadium deal room, Dogtown north gate, stadium market | `story` | Raw registry entry `kurtz` (phases `q301_01_start`, `q301_04_start`, `q301_blackmarket_announcement`, `q303_casino`, `q303_restaurant_host`; spots `#q301_ws_01_kurtz`, `#q301_ws_04_kurtz`, `#q301_ws_02a_kurt_announcement`, `#q303_ws_kurt_paradise_casino`, `#q304_07_ws_kurt_deal_start`); entry `kurtz_miniboss` → `Character.q304_kurt_miniboss`; `#q305_ws_hallucination_kurt`; wiki *Kurt Hansen* | `[game-data]` `[wiki]` |
| **Chester Bennett** | Lieutenant Colonel; commander of the armed forces; Hansen's chief aide; successor claimant | `Character.mq304_bennett`; party variant `Character.q303_paradise_bennett` | Black Sapphire (party, Hansen's wake), Stadium escape | `story` | Registry entry `bennett` (phases `mq304_01_meeting`, `mq304_after_combat_alley`, `mq304_wake_booth`, `mq304_wake_start`; spots `#mq304_ws_bennett_meeting`, `#mq304_ws_bennett_wake_booth`); entry `25_kurt_bennett` → `Character.q303_paradise_bennett`; wiki *Chester Bennett* | `[game-data]` `[wiki]` |
| **Jago Szabó** | Chief accountant ("treasurer"); successor claimant | `Character.mq304_jago`; party variant `Character.q303_paradise_jago` | Luxor Heights (Voodoo Boys meeting), Black Sapphire (party, wake), Stadium | `story` | Registry entry `jago` (phases `meeting_arrive`, `meeting_spawn`, `q301_border`, `wake_bennett`, `wake_booth`; spots `#mq304_ws_jago_vdb_arrive`, `#q301_ws_01_jago_gate_cargo`, `#mq304_ws_jago_wake_booth`); wiki *Jago Szabó* | `[game-data]` `[wiki]` |
| **Albert Murphy** | High-ranking old-guard officer; Hansen's "approachable side", negotiator and enforcer of the district's order | `Character.kruger_combat` (registry entry **`murphy`**) | EBM Stadium (market escape) | `story` | Registry entry `murphy` → `Character.kruger_combat`, phase `q304_01_start`, spot `#q304_ws_escape_murphy_boss`; wiki *Albert Murphy*; FIA photo board | `[game-data]` `[wiki]` |
| **Yuri Bychkov** | Lieutenant; old guard; convoy/generator command; out of favour in 2077 | No character record found (appearance and photo only) | Black Sapphire garrison, Stadium | `story` | Wiki *Yuri Bychkov*; `Balls to the Wall`; FIA photo board | `[wiki]` |
| **Leon Rinder** | Old guard; founding member; cyberpsychotic ex-member | No character record found | Longshore Stacks (crime scene), Los Osos Motel (West Wind Estate) | `world-activity` | Wiki *Leon Rinder*; `Gig: The Man Who Killed Jason Foreman` (`baseid sts_ep1_03`); FIA photo board | `[wiki]` `[game-data]` |
| **Carl "Dodger" Robinson** | High-ranking non-veteran; drug revenue; airdrop/smuggling logistics; claims to be "Hansen's right hand" | `Character.sts_ep1_10_dodger` | Former Pacifica NCPD Precinct (Coastview); Black Sapphire wake | `world-activity` | Registry entry `dodger` (phase `mq304_wake_dodger`); community `9529329004064786977` with `sts_ep1_10_dodger_goon_01/02`; wiki *Carl Robinson* | `[game-data]` `[wiki]` |
| **Ross Ulmer** | Lieutenant in charge of the Dogtown Tunnel; private side deals; helped Rinder escape | `Character.we_ep1_01_mini_boss_1st_phase` `[inferred]` | Dogtown Tunnel (Longshore Stacks → West Wind Estate) | `world-activity` | Wake entry `mq304_ws_wake_ross_ulmer` → `Character.we_ep1_01_mini_boss_1st_phase`; `Increased Criminal Activity: BARGHEST` (`baseid we_ep1_01`); wiki *Ross Ulmer* | `[game-data]` `[wiki]` |

The wiki marks nearly every Phantom Liberty character "dependent", including
Hansen, Bennett and Jago. That is not a leadership property — it means their
survival depends on V. The branches are in §1.8.

### 1.2 Succession history: one founder, no institution

Barghest has had exactly one change of leadership, and it happens inside the
Phantom Liberty story. The line is short and that is the political fact.

| Period | Leader | How the position was held |
| --- | --- | --- |
| 2067–2070 | **Colonel Kurt Hansen** (Militech) | Given command of the Barghest urban-combat and pacification unit. `[wiki]` |
| 2070 | **Hansen, mutineer** | Ordered to withdraw from Pacifica on 9 June 2070; refused with the entire unit; ignored the Arvin Accord and kept the stadium foothold. `[wiki]` |
| 2070–2077 | **Hansen, warlord** | Founded Barghest from the veterans, then mercenaries, then renegade gangers and street kids. Ran Dogtown as army, customs, police and arms dealer. `[wiki]` |
| 2077 | **Vacancy** | Hansen dies in `Firestarter` on every branch (killed by Alex, killed in the boss fight, or assassinated in hospital / "caught a stray bullet"). `[wiki]` |
| 2077 | **Chester Bennett** or **Jago Szabó** | Open contest decided in `Run This Town`, with Mr. Hands backing Bennett. `[wiki]` |

There is no council, no vote and no designated deputy. The succession is an
armed contest between the commander of the forces and the chief accountant,
arbitrated from outside by a fixer and a mercenary. For a simulation this is
the cleanest possible succession event: **remove the founder and the faction
splits into two named blocs with different external policies** (§2.3).

### 1.3 Rank structure, recruitment and advancement

Barghest is explicitly modelled on an army, and the game text uses the ranks.

1. **Colonel** — Hansen. He is still addressed as "Colonel" after seven years
   as a warlord; the title is the source of legitimacy. `[wiki]`
2. **Lieutenant Colonel** — Bennett, commander of the armed forces. `[wiki]`
3. **Major / Captain / Sergeant / Private** — attested in shards. A sergeant
   reports to a major about airdrops; a sergeant reports to a captain named
   "Tom" who says "this isn't the fucking army"; a private's corpse carries
   the airdrop-code shard. `[wiki]`
4. **Functional archetypes** — the record namespace shows the specialisations:
   `grunt`, `soldier`, `elite`, `enforcer`, `ranger`, `recon_sniper`,
   `netrunner`, `tech`, `strongarms`, `exo`, plus `minotaur`, `wyvern` and
   `bombus` machines. `[game-data]`
5. **The Prevention Unit** — the red-armoured law-enforcement division that
   replaces NCPD inside the wall. It is a Barghest subunit, not a separate
   faction, and it has no `data/factions.json` code. `[wiki]`
6. **Recruits** — the mass. Not a rank so much as a pipeline.

**Recruitment is deliberately broad.** The database entry says the core is
well-trained veterans and mercs, "constantly reinforced by dozens of street
kids dazed by the allure of becoming part of something bigger"; the wiki adds
"veterans who'd been forgotten by the megacorps, mercs without contracts,
renegade gangers", and residents "at the end of their ropes". Hansen offers "a
gun, a salary, medical care via his ripper contacts" and "asked no questions in
exchange for their absolute loyalty". `[wiki]`

**The written rules.** `New Recruit Directives` is the onboarding document and
it is a political text, not a combat manual:

1. Orders of a superior officer take highest priority.
2. Insubordination is severely punished; a third instance means discharge;
   gross misconduct may mean "discharge in a body bag".
3. Dogtown is your new home; treat its residents with respect.
4. Report all irregularities; watch for "agents of influence".
5. Stay patient; loyalty and devotion will be rewarded.

Signed "Col. Kurt Hansen". `[wiki]`

**Advancement is favour, not seniority.** Veterans are fast-tracked to the
inner circle; non-veterans can reach it "should they prove useful enough"
(Jago the accountant, Dodger the drug dealer). Failure is handled personally:
Bychkov "messed up big-time, started making deals behind Kurt's back" and was
given a second chance because of his record; Rinder was expelled after a
psychotic break; Ulmer ran private deals until V killed him. `[wiki]`

**Discipline is theatrical.** Bennett's "favourite pastime remains hanging
people from lampposts"; Yuri Bychkov executes a recruit and displays the body
at The Needle "to send a message"; soldiers shake down civilians. The same
organisation claims to be the district's law and advertises humanitarian aid
to its poorest residents (the NUSA white paper says so explicitly). `[wiki]`

**Practical consequence for the mod:** advancement should be a function of
(a) veteran status, (b) loyalty to the current commander, and (c) revenue
delivered. That is exactly the axis that separates Bennett (a), Jago (c) and
Dodger (b+c). Cyberpsychosis is the failure state (Rinder), and corruption is
tolerated until it becomes visible (Ulmer, Paco).

### 1.4 Named members mapped to game data

**The roster check comes first (METHOD §1.2 item 1), and it almost fails.** Of
Barghest's 87 roster units across 4 sites, only two records are named:
`Character.sts_ep1_10_dodger` (Dodger) and `Character.sts_ep1_12_courier`
(Kyle Araujo). Every other roster record is a generic archetype
(`sts_ep1_06_enemy_*`, `sts_ep1_07_kurtz_*`, `sts_ep1_10_kurtz_*`). The rest of
the leadership lives in the raw sector community registry, which is why this
table names exact records. All 10,324 `worldCommunityRegistryItem` rows are in
`always_loaded_1`, matching METHOD §1.2 item 1. Rows marked `[inferred]` are
one-signal deductions; verify in-game before seeding them.

| Name | Role / note | Character record | Community / site | Location | Presence class | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| Kurt Hansen | Colonel, commander | `Character.kurtz` | `{q301_*}` gate/market, `{q303_*}` Sapphire, `{q304_*}` deal | Dogtown | `story` | `[game-data]` `[wiki]` |
| Chester Bennett | Lt. Col., forces commander | `Character.mq304_bennett`, `Character.q303_paradise_bennett` | wake `3323591791502479431`; Sapphire `747996165102223435` | Black Sapphire / Stadium | `story` | `[game-data]` `[wiki]` |
| Jago Szabó | Chief accountant | `Character.mq304_jago`, `Character.q303_paradise_jago` | `{mq304_com_ce_ma_sc_}06`; wake; Sapphire | Dogtown | `story` | `[game-data]` `[wiki]` |
| Albert Murphy | Old-guard officer | `Character.kruger_combat` (entry `murphy`) | `12776600799207924370` | Stadium | `story` | `[game-data]` `[wiki]` |
| Yuri Bychkov | Lieutenant, old guard | no record | — | Black Sapphire / Stadium | `story` | `[wiki]` |
| Leon Rinder | Ex-member, cyberpsycho | no record | — | Longshore Stacks / Los Osos | `world-activity` | `[wiki]` `[game-data]` |
| Carl "Dodger" Robinson | Revenue wing | `Character.sts_ep1_10_dodger` | `9529329004064786977` | Former NCPD Precinct | `world-activity` | `[game-data]` `[wiki]` |
| Ross Ulmer | Tunnel commander | `Character.we_ep1_01_mini_boss_1st_phase` `[inferred]` | `3323591791502479431` (wake), `we_ep1_01` | Dogtown Tunnel | `world-activity` | `[game-data]` `[wiki]` |
| Charles "Charlie" Graham | Jago's bodyguard | `Character.mq304_jago_bodyguard_01` `[inferred]`; registry entry `boulder` also uses this record | `4323906256378075111`, wake | Black Sapphire / Dogtown | `story` | `[inferred]` `[wiki]` |
| Paco Torres | New recruit; Balls to the Wall | `Character.paco` | `15955641788856784119` | Black Sapphire garrison tent | `story` | `[game-data]` `[wiki]` |
| Barbara "Babs" Okoye | Soldier; Paco's friend | no record | — | Black Sapphire garrison tent | `story` | `[wiki]` |
| Kyle Araujo | Courier and implant supplier | `Character.sts_ep1_12_courier` | wake entry `kyle_araujo` | Luxor High Wellness Spa / Dogtown | `world-activity` | `[game-data]` `[wiki]` |
| Fae Nesheim | Soldier; airdrop-coordinate hunt | no record | — | Akebono Hotel, Luxor Heights | `mentioned` | `[wiki]` |
| Leonardo Ware | Ex-member; arrested for theft | no record | — | — | `mentioned` | `[wiki]` |
| The "unidentified" member | Eighth photo on the FIA board | no record | — | — | — | `[wiki]` |

**Two data cautions, both real collisions.**

- **`kurtz` is Hansen; `kurtz_*` is everyone else.** `Character.kurtz` is the
  Colonel. `Character.kurtz_grunt1_*`, `kurtz_soldier1_*`, `kurtz_elite3_*`,
  `kurtz_minotaur`, and the whole `bou_/con_/mon_/high_/hpark_/sta_/combat_tower_/we_ep1_01_`
  namespaces are his soldiers, machines and patrols. A substring search for
  `kurt` also hits `Character.kurt_hallucination` (a Cynosure memory of him) and
  the playable `Character.mq301_kurt_initiation_*` proxies used in
  `Balls to the Wall`'s Deep Dive. **Match exact records.** `[game-data]`
- **`murphy` is ambiguous.** `Character.q101_spider_murphy` is the legendary
  netrunner Spider Murphy in the base-game Arasaka heist records, not Albert
  Murphy. Albert Murphy's actor is the registry entry `murphy` whose record is
  `Character.kruger_combat` — an entry-name join, not a name join. This is the
  single weakest identity link in the document; flagged in §5.2. `[game-data]`

**The FIA board is the best single roster of the elite.** In
`Birds with Broken Wings`, the FIA safehouse in The Moth has a photo board of
"Barghest's top echelon": Hansen, Jago, Murphy, Bennett, one unidentified
member, Bychkov, Dodger and Rinder. Photos of Bychkov, Dodger and Rinder get a
red X if V has already killed them. That is an in-fiction confirmation of the
eight-person elite and of their killability. `[wiki]` `[game-data]`

### 1.5 What the game actually spawns (open world vs story-only)

A wiki infobox does not mean an actor in free roam. With the campaign disabled,
expect this:

**`world-activity` — gig or scanner content; free-roam but activity-gated.**
- **Carl "Dodger" Robinson** at the former NCPD precinct in Coastview
  (`Gig: Waiting for Dodger`, `baseid sts_ep1_10`). He has his own goons
  (`sts_ep1_10_dodger_goon_01/02`). `[game-data]` `[wiki]`
- **Ross Ulmer** at the Dogtown Tunnel (`Increased Criminal Activity:
  BARGHEST`, `baseid we_ep1_01`). The record is the activity's only
  `mini_boss_1st_phase`; the wake entry naming him confirms the join.
  `[game-data]` `[wiki]`
- **Leon Rinder** at the Los Osos Motel (`Gig: The Man Who Killed Jason
  Foreman`, `baseid sts_ep1_03`), plus `Addicted To Chaos` if spared.
  `[game-data]` `[wiki]`
- **Kyle Araujo** as the courier at the Luxor spa (`Gig: Treating Symptoms`,
  `baseid sts_ep1_12`). `[game-data]` `[wiki]`

**`story` — gated by the Phantom Liberty chain; do not expect them in free
roam with the campaign disabled.**
- Hansen, Bennett, Jago, Murphy, Bychkov, Graham, Paco, Babs. Their communities
  are initial-phase quest states (`q301_01_start`, `mq304_01_meeting`,
  `mq304_wake_start`, …). `[game-data]`

**`mentioned` — no actor at all.**
- Fae Nesheim and Leonardo Ware exist in shards and member tables only. `[wiki]`

**`historical` — not in 2077.**
- None of the leadership is historical: the militia is only seven years old
  and the founder is alive until `Firestarter`. The dead are 2077 dead, not
  historical dead. `[wiki]`

Caveat: "campaign disabled" is a heuristic. If the mod disables gigs and
scanner activities along with the main quest, the `world-activity` rows drop
out too. The `story` rows are the ones to replace with simulation agents,
never expect the game to provide.

### 1.6 Player-path hooks

This is the design-facing summary: who a player can join under, climb past,
ally with or remove.

| Person | Join under | Climb past | Ally with | Remove |
| --- | --- | --- | --- | --- |
| **Kurt Hansen** | The only legitimate ladder in 2077: the militia itself, the market, the gates, the Tunnel | His officers are the rungs: Murphy (patronage), Bennett (command), Jago (money), Dodger (logistics) | Nobody inside the faction is his equal; outside, only transactional partners (§3.4) | Killing Hansen is the campaign's decapitation; it starts the Bennett/Jago contest |
| **Chester Bennett** | The army: obedience, force, anti-outsider line | He is already Lt. Col.; climbing past means the succession or a coup | Murphy and the old guard by sentiment; Arasaka by deal | Removing Bennett leaves Jago unopposed but the forces leaderless |
| **Jago Szabó** | The money: contracts, smuggling, the stadium's books | He has no troops of his own beyond Graham and hired guards; a player under him climbs by delivering revenue | The Voodoo Boys (he negotiates with them), Mr. Hands (after the fact), the market vendors | Removing Jago leaves the revenue wing without an accountant and Bennett unopposed |
| **Albert Murphy** | The district's day-to-day order: negotiations, shakedowns, "the fist" | He is Hansen's approachable face, not a claimant; climbing past him means replacing his role | The old guard; anyone Hansen needs handled | Removing Murphy decapitates the old guard's political voice, not its muscle |
| **Yuri Bychkov** | The old guard's second chance: convoy and garrison duty | He is already a lieutenant; his star is falling | Murphy and the veterans; nobody else | Removing Bychkov shrinks the old guard and removes a Hansen loyalist |
| **Leon Rinder** | Not a ladder: he is out | — | No ally left; even Ulmer only helped him flee | Removing Rinder closes a cyberpsycho liability and a public scandal |
| **Carl "Dodger" Robinson** | The revenue wing: drugs, airdrops, courier runs, guest security | He is a non-veteran who reached the top by money; a player can out-earn him | The Voodoo Boys' netrunners (he hires them), Bennett (secret deal), the market | Removing Dodger cuts the drug revenue and the airdrop logistics brain |
| **Ross Ulmer** | The Tunnel: the border franchise | He is a lieutenant with a private racket; climbing past means taking the Tunnel | His tunnel crew; Rinder (he helped him escape); nobody at court | Removing Ulmer opens the Tunnel to a new boss and exposes his side deals |

**The civil ladder is separate and more important than it looks.** A player
who does not want to enlist can buy into Dogtown instead: pay the market's
"registration fee", rent a stall, use the Tunnel, hire Barghest muscle. That
is a **franchise**, not membership, and it is the only faction in the pilot set
that offers one. Jacob Long's punishment for skipping the fee — Barghest
amputated his leg — is the price list. `[wiki]`

### 1.7 The Dogtown civil/economic layer

Barghest does not just own buildings; it **is** the district's government. The
civil layer is where most of its political leverage actually sits, and it has
no faction id, so it needs modelling explicitly.

| Layer | What Barghest provides / extracts | Evidence | Simulation note |
| --- | --- | --- | --- |
| **The market** (EBM Stadium) | The largest black market on the West Coast; tax-free goods; a "registration fee" to trade; vendors for weapons, cyberware, meds, netrunning, clothing, food | `[wiki]` stadium page, `Lucretia My Reflection` (Jacob Long), location catalog §3–§4 | A business cluster with one owner and many tenants. The fee is the tax base. |
| **Airdrops** | AVs drop weapons, gear and shards into Dogtown; couriers and patrols collect them; the sender is unknown | `[wiki]` Airdrops; `[game-data]` 15 `sa_ep1_*` drop communities; courier-loop records | **Events, not holdings.** Model as supply convoys with a contest roll, not as control points. |
| **Protection / shakedowns** | Soldiers extort civilians and businesses; the gates charge in kind; "no taxes" is a slogan | `[wiki]` `You Know My Name` dialogue, Jacob Long, New Recruit Directives #3 | A revenue stream and a legitimacy cost. Respect for residents is written policy and routinely violated. |
| **The gates** | Customs, scanners, turrets, the Prevention Unit; the only legal entry; NCPD vehicles are refused | `[wiki]` Dogtown Gate; `[game-data]` `{q302_cz_gate}`, `{q301_com_border_*}` | Checkpoint capture points (§ location doc). Closing a gate is a political act, not a tactical one. |
| **The Tunnel** | Export of "any goods others might require, including people"; 48-hour delivery to 6th Street; Ulmer's private racket | `[wiki]` Dogtown Tunnel; `[game-data]` `we_ep1_01` | A chokepoint and a corruption node. Whoever holds it can trade without the market. |
| **The Sapphire** | Elite venue, casino, restaurant, AV pads; guest anonymity bought from Voodoo Boys netrunners; floor 1 is barracks and warehouses | `[wiki]` Black Sapphire; Ayo Zarin shard; `[game-data]` `{q303_com_tower_lobby}` | The political salon: the one place where rival factions are physically co-located (§3.2). |
| **Heavy Hearts** | "Neutral ground" for the district's elite; Mr. Hands keeps a suite and runs gigs from it | `[wiki]` Heavy Hearts, `Run This Town` | A diplomatic asset. Attacking it should cost more than attacking a normal business. |
| **Longshore Stacks** | Barghest "influential presence", but the neighbourhood is "more autonomous", with **Briana Dolson** as chosen representative | `[wiki]` Longshore Stacks; `Gig: The Man Who Killed Jason Foreman` | A **client community**, not a holding. It supplies legitimacy and labour, and it can turn (Briana bans V from her area). |
| **Utilities and aid** | The captured aerozep reactor powers the district "with no bills"; water, roofs, humanitarian aid to the poorest | `[wiki]` stadium page; NUSA white paper | The welfare side of the bargain: cheap power and aid buy quiescence. Losing the reactor is a legitimacy crisis. |
| **Population** | ≈6,000–8,000 residents and transients, many undocumented or wanted; most live in makeshift dwellings | `[wiki]` `Dogtown – Analytical Summary` (NUSA estimate) | The manpower and tax base; also the recruiting pool and the intelligence risk. |

The political reading: Barghest's authority rests on **four monopolies** —
violence (the Prevention Unit), entry (the gates), trade (the market) and
logistics (the Tunnel and the airdrops) — plus **one welfare bargain** (power,
water, aid). Every internal bloc in §2 is a claim on one of those monopolies.

### 1.8 Phantom Liberty branches that change the leadership

Every row below is a V-dependent outcome. A simulation must choose a branch or
model the branches explicitly; it must not silently pick one.

| Quest | Branch | Effect on the leadership |
| --- | --- | --- |
| `Dog Eat Dog` | V ignores Songbird | Myers dies; Hansen unchanged. `[wiki]` |
| `Lucretia My Reflection` | V walks away | Myers and Reed are killed and delivered to Hansen; the PL chain ends; Hansen unchanged. `[wiki]` |
| `Firestarter` | V betrays Reed | Alex kills Hansen; no boss fight. `[wiki]` |
| `Firestarter` | V betrays Songbird, defeats Hansen | Hansen dies; V loots Fang, Bald Eagle and Wild Dog. `[wiki]` |
| `Firestarter` | V betrays Songbird, spares or skips Hansen | Hansen still dies: assassinated in hospital, or "caught the proverbial stray bullet". `[wiki]` |
| Before `Firestarter` | V kills Bychkov in `Balls to the Wall` | Old guard shrinks; his FIA photo is crossed out. `[wiki]` |
| Before `Firestarter` | V kills Rinder, or sends him to Regina | Rinder leaves the board (dead, or in treatment); Ulmer's help is exposed. `[wiki]` |
| Before `Firestarter` | V kills Dodger in `Waiting for Dodger` | Revenue wing loses its head; his photo is crossed out. `[wiki]` |
| `Run This Town` | Bennett wins | Bennett leads Dogtown; Jago is killed, or survives if V forces peace. `[wiki]` |
| `Run This Town` | Jago wins | Jago leads; Bennett is killed, or survives with Terra Cognita as compensation. `[wiki]` |
| `Run This Town` | V forces peace | Bennett leads with Jago beside him; Mr. Hands pays full rate. `[wiki]` |
| `Run This Town` | Jago wins, nobody dies | Mr. Hands later concedes Jago is "the more competent leader" — reversing his own briefing. `[wiki]` |
| `Balls to the Wall` | V tells Paco to frame Yuri | Paco is executed; his body is hung at The Needle. `[wiki]` |
| `Balls to the Wall` | V helps Paco leave | Paco flees (or joins the Scavengers); Babs stays or leaves. `[wiki]` |

**One structural note.** Hansen dies on *every* branch. Phantom Liberty is not
a story in which the player can keep him; it is a story about who inherits.
That makes Barghest the most simulation-ready faction in the set: the
succession is canonical, not hypothetical.

---

## 2. Internal political factions

### 2.1 The blocs

"Members" counts below are **presence proxies** from `areas.jsonl` and the
community registry, not membership rolls. The wake and party communities are
overlapping quest phases of single sites, so do not sum them.

| Bloc | Leader(s) | What it wants | Presence / members hint | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- |
| **The Midnight Storm old guard** | Kurt Hansen; Albert Murphy, Yuri Bychkov, Leon Rinder | Keep the founding squad's primacy, Hansen's personal rule, and the army's identity; resist being treated as obsolete | Six survivors in lore; three explicitly labelled "former squadmate"; FIA photo board has four of them | Barghest database entry ("only six soldiers remain"); member pages; `Birds with Broken Wings` | `[game-data]` `[wiki]` |
| **Bennett's command corps** | Chester Bennett | Military continuity, command of the forces, the succession, outside backing | 13 `wake_bennett_guard_*` entries (11 Barghest records + 2 VDB non-reaction actors) plus 3 bodyguards; `kurtz_soldier*`/`elite*` records; the Arasaka dummy deal | Bennett's rank and DB entry; `Run This Town`; wake community `3323591791502479431` | `[game-data]` `[wiki]` |
| **Jago's finance and administration wing** | Jago Szabó; Charles Graham | Monetise the district, professionalise it, and take the chair with the accountants' leverage | 9 `wake_jago_guard_*` entries plus 2 bodyguards; `{mq304_com_ce_ma_sc_}06`; the VDB meeting | Jago's DB entry; `Awaiting Your Signal`; `Run This Town` | `[game-data]` `[wiki]` |
| **Dodger's revenue wing** | Carl "Dodger" Robinson | Autonomy, drug money, control of airdrop and courier logistics, indispensability | `sts_ep1_10_dodger_goon_01/02`; 12 VDB netrunners hired for the party; courier-loop records; the precinct base | `Gig: Waiting for Dodger`; Ayo Zarin shard; `Run This Town` | `[game-data]` `[wiki]` |
| **Ulmer's Tunnel fief** | Ross Ulmer | Private profit from the border, control of the Tunnel, protection of old comrades | `we_ep1_01_*` garrison (10+ records incl. a Centaur); the wake entry | `Increased Criminal Activity: BARGHEST`; Ulmer's wiki biography | `[game-data]` `[wiki]` |
| **The new recruits** | No single leader; Paco Torres and Babs Okoye as the face | A fresh start, a salary, survival, a chance to rise | `New Recruit Directives`; Paco's tent in front of the Sapphire; the mass of generic `*_kurtz_*` records | `Balls to the Wall`; `New Recruit Directives`; Paco/Babs DB entries | `[game-data]` `[wiki]` |
| **The civil layer (non-member power centres)** | Briana Dolson (Stacks); the market vendors; Mr. Hands (fixer) | Keep trading, keep autonomy, keep the district stable enough to profit | Stacks community and vendors; Heavy Hearts suite; market stalls | Longshore Stacks page; `Gig: The Man Who Killed Jason Foreman`; `Run This Town` | `[wiki]` `[game-data]` |

### 2.2 The old guard versus the new men

This is the deepest internal fault line, and it predates the succession.

- The database entry is explicit: "Only six soldiers remain from that squad,
  and as Hansen's most trusted men they now sit at the top of the food chain."
  `[wiki]`
- The member table labels **Murphy, Bychkov and Rinder** "former squadmate";
  with Hansen himself that is four of the six named, and two are unnamed.
  `[wiki]`
- Bychkov's entry states the grievance plainly: after years of service "he's
  getting increasingly annoyed with being treated as an inferior", and has
  begun "making deals behind Kurt's back". `[wiki]`
- Rinder's entry is the failure case: a founding member whose insecurity and
  aggression ended in cyberpsychosis and expulsion. `[wiki]`
- Against them stand the **new men who rose on revenue**: Jago (an embezzler
  who helped lay the organisation's foundations in 2072, two years after the
  mutiny) and Dodger (a fugitive who bought his rank with drug money and claims
  to be Hansen's right hand). `[wiki]`

The political axis is therefore **veteran legitimacy versus revenue
legitimacy**. Bennett straddles it: a Midnight Storm Marine and the commander
of the forces, but not labelled one of the six squadmates. That ambiguity is
exactly why he is the "obvious" successor and exactly why Jago can contest him.

### 2.3 Bennett versus Jago: the 2077 succession

`Run This Town` is the faction's internal war, and it is unusually
well-instrumented.

- **Bennett's case:** commander of the armed forces, Hansen's chief aide,
  military continuity. Mr. Hands prefers him and calls Jago "immature": "a
  bookkeeper is unlikely to be a good leader in a place like Dogtown".
  `[wiki]`
- **Bennett's liability:** his DB entry is a catalogue of sadism and
  indiscipline — war crimes, lamppost hangings, "respect mixed with fear".
  Jago's recruiting shard says Bennett "excels at one thing and one thing
  alone — doing the dirty work" and that his reign "would drown Dogtown in
  blood and destroy what Hansen built". `[wiki]`
- **Bennett's secret:** he has already opened a channel to **Arasaka** through
  a dummy company, negotiating "collaboration" without Hansen's knowledge.
  `[wiki]`
- **Jago's case:** chief accountant, "a real numbers whisperer", the man who
  "steers Barghest's finances"; he can pay people. "His friendly disposition
  is only a facade, behind which lies a cold, calculating intellect." `[wiki]`
- **Jago's coalition:** he recruits Barghest members directly (the
  `Awaiting Your Signal` shard), meets the **Voodoo Boys** for support, and
  keeps a capable bodyguard (Graham). He is the candidate of the revenue wing.
  `[wiki]` `[game-data]`
- **The outcome:** V, disguised as the Cuban cartel mercenary **Aguilar
  Nubiola**, decides. Mr. Hands's preference is Bennett; the shard's argument
  and the "more competent leader" line later suggest Jago. Both outcomes are
  canonical branches. `[wiki]`

The policy difference is real, not personal:

- **Bennett:** military rule, external corporate backing (Arasaka), force as
  the default instrument.
- **Jago:** commercial rule, netrunner and fixer channels, the books as the
  instrument.
- **Mr. Hands:** stability and predictability, whichever candidate provides it.

That is a simulation-ready axis: **force versus finance**, with an external
patron on each side (Arasaka for Bennett, the Voodoo Boys for Jago).

### 2.4 Dodger and the revenue wing

Dodger is the most important non-veteran in the faction and the clearest
example of money buying rank.

- He "was not a member of Kurt Hansen's military unit but rather joined up to
  escape a tumultuous past" and "earned his high position by bringing in large
  amounts of revenue … via drug dealing". `[wiki]`
- He claims to be "Hansen's right hand" and tells the Voodoo Boys lieutenant
  Ayo Zarin, "I'm Hansen's right hand and you're Slider's". `[wiki]`
- He runs the **guest-anonymity contract** for the Black Sapphire: twelve
  Voodoo Boys netrunners for personal-data protection, facial-recognition
  security, subnet encryption, money-transfer encryption and biomon jamming.
  "Money's not a problem." `[wiki]`
- He runs the **airdrop and courier logistics**, and he holds two NCPD officers
  prisoner in his base — one of whom he blackmails afterwards. `[wiki]`
- He has a **secret channel to Bennett**; a cut shard has Bennett saying "Fuck
  Hansen" while Dodger routes a package through the Tunnel for him. `[wiki]`
  (Cut content: treat as intent, not canon.)

For a simulation: Dodger is the bloc that can **defect without leaving**. He
is loyal to the revenue, not the man. If Bennett wins, Dodger is fine; if Jago
wins, Dodger is fine; if the market closes, he is not.

### 2.5 Ulmer and the Tunnel fief

Ulmer is the model of a **corridor lord**.

- Hansen placed him in charge of the Tunnel, "responsible for monitoring and
  guarding the smuggling tunnel between Dogtown and West Wind Estate". `[wiki]`
- He "conducted deals outside of Hansen's control for personal gain" and
  "assisted Leon Rinder when the latter needed to escape Dogtown without
  Hansen's knowledge". `[wiki]`
- He commands a real garrison, including a **Centaur** in the second phase of
  the activity. `[game-data]` `[wiki]`

The Tunnel is the faction's single most valuable chokepoint after the market,
and Ulmer treats it as a personal franchise. That is a permanent corruption
node: any player who wants to move goods or people without the market must
deal with him, and any commander who wants to centralise must remove him.

### 2.6 The civil layer as a political actor

The district's civilians are not passive. Three non-member power centres
matter:

1. **The market tenants.** Vendors pay the registration fee and depend on
   Barghest's security. They are the tax base and the reason the "no taxes"
   claim is hollow. `[wiki]`
2. **Longshore Stacks.** The neighbourhood is "more autonomous", with Briana
   Dolson as the chosen representative; she runs the community's problems and
   can ban even V from her area. `[wiki]` A commander who alienates the Stacks
   loses the district's largest residential bloc.
3. **Mr. Hands.** A fixer with a suite in Heavy Hearts who brokers Dogtown
   contracts, hires V for the district's gigs, and kingmakes the successor.
   He is not a member, but he is the closest thing the faction has to a
   foreign minister. `[wiki]`

The Stacks' grievance is concrete: Leon Rinder, "one of Hansen's former
triggermen", killed eight civilians there and was expelled; the community
wants him dead. That is the civil layer's price for the militia's protection.
`[wiki]`

### 2.7 What could drive internal conflict in a simulation

Evidence-based drivers, in rough order of plausibility:

1. **The succession.** Hansen's death opens a two-way contest (Bennett vs
   Jago) with a peace branch. Each candidate has a different external policy.
2. **Veteran versus revenue legitimacy.** The six old guard versus the men who
   bought their rank. Bychkov's resentment, Rinder's expulsion and Dodger's
   "right hand" claim are all expressions of it.
3. **Corridor autonomy.** Ulmer's Tunnel racket and Dodger's logistics empire
   are private franchises. Centralising them creates enemies; leaving them
   alone creates a parallel power.
4. **Corruption and skimming.** Paco steals generators; Ulmer deals behind
   Hansen's back; Bychkov makes private deals. Enforcement is theatrical and
   selective, so skimming is a rational strategy until someone is made an
   example.
5. **The civil bargain.** Market fees, shakedowns and the Stacks' autonomy.
   Push too hard and the tax base shrinks or turns; push too little and the
   revenue wing outgrows the commander.
6. **External pressure.** The NUSA/FIA campaign, Voodoo Boys and Scavenger
   encroachment, and Arasaka's courtship of Bennett. External actors decide
   the succession more than internal ones do.
7. **Counter-intelligence failure.** The FIA has a safehouse in The Moth, a
   photo board of the elite, and two sleeper agents; Songbird manipulated
   Hansen into shooting down Space Force One. Any commander who ignores
   infiltration loses the initiative.

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

Every row is a faction code from `data/factions.json`. Rows with no attested
interaction are marked `neutral` and `[inferred]`; they are placeholders, not
findings. Do not promote them without evidence.

There is **no usable offline attitude matrix**. `Affiliation.hpp` is an
identity enum (Barghest = 10), not a relation table; `Attitude_Record.hpp` is
opaque. The stances below are judged from quests, shards, the wiki and the
game's own co-location records.

The Black Sapphire party is the strongest co-location signal and it survives
METHOD §1.2 item 6's crowd-pool filter: it is a **scripted quest scene**, not a
respawn pool or time-of-day set dressing. The guest list names specific NPCs,
and the community places them (`q303_paradise_jotaro`, `q303_paradise_6th_street_leader`,
`q303_paradise_arasaka_contact`, `q303_paradise_scav_tzar`, …). `[game-data]`
`[wiki]`

| Faction | Code | Stance | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| Tyger Claws | `tyger_claws` | `trade` | High-ranking Tyger Claws (Jotaro Shobo, Maiko Maeda, Marcus Ichida, Jun Azegami) attend Hansen's Black Sapphire party `[wiki]`; 6 Tyger Claws records in the floor-99 community `{q303_com_paradise_quest_interactions}` `[game-data]`; Dodger's past includes "gravely insulting a prominent Tyger Claws boss", sheltered by Hansen `[wiki]` | `game-data+wiki` |
| Valentinos | `valentinos` | `neutral` | No attested interaction; different district. The Valentinos' Hector Sacristán is hunted by a D.A. who frequents Heavy Hearts, but that is not a Barghest relationship `[inferred]` | `inferred` |
| Arasaka | `arasaka` | `trade` | Bennett negotiates with a dummy company backed by Arasaka in `Run This Town`, seeking "collaboration" behind Hansen's back `[wiki]`; two `q303_paradise_arasaka_contact` actors at the Sapphire party `[game-data]`; the FIA white paper lists "covert Arasaka and Zetatech operations" in Dogtown `[wiki]` | `game-data+wiki` |
| Militech | `militech` | `neutral` | The unit **was** Militech and deserted in 2070; Militech's Cynosure bunkers still sit under Dogtown and the stadium bunker holds the neural matrix; the FIA white paper lists "Militech deserters" as a subject of interest `[wiki]` `[game-data]`; no 2077 Militech operation against Dogtown is attested | `wiki+game-data+inferred` |
| Kang Tao | `kang_tao` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Biotechnica | `biotechnica` | `neutral` | Abandoned Biotechnica Venture Center in Luxor Heights; Biotechnica agents pursue a Crimson Harvest defector **inside the Nighthawks armory** in `Gig: Roads to Redemption`, with no Barghest response attested `[game-data]` `[wiki]` | `game-data+wiki` |
| Petrochem | `petrochem` | `neutral` | The stadium bears Petrochem's name as a historic sponsor; Jago was imprisoned for embezzling Petrochem funds in 2066 before helping found Barghest in 2072 `[wiki]`; no current relation | `wiki` |
| 6th Street | `sixth_street` | `trade` | The Tunnel's own database entry uses 6th Street as the worked customer: sixty Militech M251s Ajax rifles delivered in 48 hours `[wiki]`; an unnamed 6th Street leader attends the Sapphire party `[game-data]`; a scripted 10-strong 6th Street protest community (`{q302_com_protesters}`) and a 6th Street reinforcement record at the armory (`sts_ep1_07_reinforcements`) show friction `[game-data]` `[wiki]` | `game-data+wiki` |
| Aldecaldos | `aldecaldos` | `neutral` | No attested interaction; Paco can be smuggled out with Panam's help only as a personal favour to V `[wiki]` `[inferred]` | `wiki+inferred` |
| Wraiths | `wraiths` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Animals | `animals` | `neutral` | Animals appear as the Scav boss Tzar's hired bodyguards at the Sapphire party and as airdrop competitors, not as Barghest counterparts `[game-data]` `[wiki]` | `game-data+inferred` |
| The Mox | `the_mox` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Maelstrom | `maelstrom` | `neutral` | No attested interaction; Maelstrom's own doc records Barghest as neutral `[inferred]` | `inferred` |
| Voodoo Boys | `voodoo_boys` | `trade` | Dogtown VDB "do business in the Stadium … protect the data of Hansen's guests"; the "symbiotic relationship between BARGHEST and the Voodoo Boys can seem shaky" but Hansen keeps it "a little rumble here and there and not a full-blown earthquake" `[wiki]`; Dodger hires 12 VDB netrunners for the Sapphire party `[wiki]`; Jago meets them for support `[wiki]`; a VDB tip led to the netrunner selling airdrop coordinates `[wiki]` | `game-data+wiki` |
| NCPD | `ncpd` | `hostile` | NCPD is forbidden in Dogtown and cannot drive through the gate `[wiki]`; the Pacifica precinct was disbanded in 2072 after local groups — Barghest and the Voodoo Boys among them — expelled the NCPD from the district `[wiki]`; Dodger holds two NCPD officers prisoner and blackmails one `[wiki]`; yet the NCPD commissioner attends Hansen's party — a corrupt elite channel `[wiki]` `[game-data]`; MaxTac is the one NCPD unit allowed in `[wiki]` | `game-data+wiki` |
| Night Corp | `night_corp` | `neutral` | No attested interaction; a corp, not a turf actor `[inferred]` | `inferred` |
| City Council | `city_council` | `neutral` | The Council ordered the Serenisands wall built and later decided to "look the other way" rather than confront Hansen `[wiki]`; deputy mayor Weldon Holt attends the Sapphire party `[wiki]` `[game-data]`; one City Council record in the floor-99 community `[game-data]` | `game-data+wiki` |
| Scavengers | `scavengers` | `rival` | "In business with BARGHEST as frequently as they clash" `[wiki]`; the Scav oligarchy "secures business in Hansen's backyard … It's all about the money" `[wiki]`; Scavs steal airdrops (sergeant/major shard), ambush Paco's convoy, and fight Barghest in the airdrop arena `{sa_ep1_113_com_combat}` `[game-data]` `[wiki]`; Tzar attends the party `[game-data]` | `game-data+wiki` |
| Regina Jones | `fixer_regina` | `neutral` | She takes in the cyberpsychotic Rinder at V's request; no anti-Barghest campaign `[wiki]` | `wiki+inferred` |
| Wakako Okada | `fixer_wakako` | `neutral` | No Barghest-specific gig or lore link found `[inferred]` | `inferred` |
| Sebastian Ibarra (Padre) | `fixer_padre` | `neutral` | No Barghest-specific gig or lore link found `[inferred]` | `inferred` |
| Muamar Reyes (El Capitán) | `fixer_el_capitan` | `neutral` | No Barghest-specific gig or lore link found `[inferred]` | `inferred` |
| Dakota Smith | `fixer_dakota` | `neutral` | No Barghest-specific gig or lore link found `[inferred]` | `inferred` |
| Dino Dinovic | `fixer_dino` | `neutral` | No Barghest-specific gig or lore link found `[inferred]` | `inferred` |
| Rogue Amendiares | `fixer_rogue` | `neutral` | No Barghest-specific gig or lore link found; Afterlife is neutral ground `[inferred]` | `inferred` |
| Mr. Hands | `fixer_mr_hands` | `trade` | Keeps a suite at Heavy Hearts and runs Dogtown gigs from it `[wiki]` `[game-data]`; brokers the succession in `Run This Town`, preferring Bennett and paying V to steer it `[wiki]`; "he operates out of there" is the reason a gig tells V not to cause trouble at the club `[wiki]` | `game-data+wiki` |
| Afterlife | `afterlife` | `neutral` | Neutral merc marketplace; no Barghest-specific link `[inferred]` | `inferred` |
| NUSA | `nusa` | `war` | Hansen arranged with Songbird to shoot down Space Force One and kill President Myers `[wiki]` `[game-data]`; FIA agents Reed and Alex run a safehouse and a leadership photo board in The Moth `[wiki]`; the NUSA white paper rates Dogtown "a Level 2 threat to NUS security interests" and names Militech deserters and covert Arasaka/Zetatech operations as subjects of interest `[wiki]`; the crash site holds 45 NUSA records `[game-data]` | `game-data+wiki` |
| NetWatch | `netwatch` | `neutral` | An undercover NetWatch agent (Alan Noël) runs an operation against the Dogtown Voodoo Boys from the Luxor spa without Barghest interference `[wiki]` `[game-data]`; NetWatch's Blackwall mandate intersects the Blackwall AI and neural matrix Hansen held `[wiki]`; no direct contact is attested. One NetWatch area in Coastview (`ma_pac_cvi_10_drone_com`) `[game-data]` | `game-data+inferred` |

### 3.3 The hub-and-spoke economy behind the matrix

Barghest is the only faction in the set whose relations are mostly **sales
relationships**. The stadium database entry describes the model exactly:

> "Imagine you're a corp CEO — you need to equip a gang to do some dirty work
> for you, and you need it done quietly. You go to the stadium in Dogtown,
> choose a supplier, pay up front, then let Hansen's people take care of the
> rest. Within 48 hours, 6th Street will have their hands on those sixty
> Militech M251s Ajax rifles you ordered." `[wiki]`

That is why the matrix has five `trade` rows and no `ally`. The customers are
whoever can pay: 6th Street, Tyger Claws, Arasaka (through Bennett), the
Voodoo Boys (in the other direction, as service providers), and Mr. Hands (as
broker). The `neutral` rows are not friendships; they are uncontacted markets.

### 3.4 Actors outside `data/factions.json`

These are real relationships but have no faction code, so they are prose only.

- **Hansen Armory** — the militia's own arms manufacturer, HQ at the Nighthawks
  Rehabilitation Center; branded weapons sold worldwide. A subsidiary, not a
  separate faction. `[wiki]`
- **The airdrop supplier** — "Who sends the airdrops to Dogtown? It's a
  mystery." An unnamed external patron or market; do not invent a faction for
  it. `[wiki]`
- **Aguilar Nubiola's cartel** — the Cuban cartel mercenary Aguilar is "highly
  respected" and his organisation "has a close relationship with Dogtown
  leadership". A named external channel, used as V's disguise in
  `Run This Town`. `[wiki]`
- **The Cassel twins' netrunner collective** — Aurore and Aymeric Cassel are
  the French netrunners Hansen brings in to help activate the neural matrix;
  Dodger has used their collective before. An external contractor channel, not
  a faction. `[wiki]`
- **Crimson Harvest** — the anti-corporate cell that Nele Springer defected
  from; the gig happens inside Barghest's armory. Not a 2077 faction. `[wiki]`
- **The six unnamed old guard** — two of the founder squad are never named
  (and one face on the FIA board is unidentified). `[wiki]`
- **Zetatech** — the FIA white paper names "covert Zetatech operations" in
  Dogtown, but there is no game record or wiki page tying Zetatech to Barghest.
  `[wiki]` (Zetatech has a `factions.json` code but is outside the design's
  named set; see §5.1, gap M9.)
- **Briana Dolson and the Stacks community** — a client community, not a
  faction. `[wiki]`

### 3.5 Guarantor assessment

This is the design question: if a player founds a gang, which factions would
guarantee Barghest's support, and which would Barghest itself guarantee?

- **Barghest has no allies.** The matrix contains no `ally`, `patron` or
  `client` row for a full faction. Its relationships are purchases, tolerances
  and one war. A player who takes over Barghest inherits a customer list, not a
  bloc.
- **Barghest is an excellent commercial guarantor — for a price.** It can
  supply weapons, move goods through the Tunnel, host deals at the Sapphire,
  provide market access and rent muscle. That is more useful to a player-founded
  gang than any of the pilot factions' offerings, and it is the only guarantee
  Barghest actually sells. The price is the registration fee, a cut, and
  submission to the district's rules (Jacob Long's leg is the enforcement).
- **Barghest is a poor military guarantor.** It is at war with the NUSA and
  surrounded by rivals inside its own wall. A player who calls on it for a war
  gets a partner that is already fighting one.
- **Who guarantees Barghest?** Nobody, by treaty. The Voodoo Boys supply
  netrunner services, Mr. Hands supplies brokerage, Arasaka supplies a
  succession candidate, 6th Street supplies demand, and the Scavs supply a
  paid tolerance. All of them are replaceable; none of them would fight for
  Hansen.
- **A player founding a gang on a Barghest point has a unique third option.**
  Maelstrom's doc concludes that the gang is more likely to be the pre-emptive
  attacker than the guarantor. Barghest offers the same war *or* a franchise:
  pay the fee, take a stall or a corridor, and become a client. That is a
  distinct political path worth modelling.

---

## 4. Pillar notes

Design claims from `docs/design/gameplay-systems.md`: Barghest is a
**Paramilitary Organization** (archetype strength **Military**, weakness
**Economy**); faction strength **Politics**, weakness **Espionage**.

| Pillar | Design claim | Lore verdict | Evidence |
| --- | --- | --- | --- |
| Military (archetype strength) | Barghest is a professional army | **Strongly supported.** Real ranks from private to colonel, a veteran core, an officer corps, combined arms (Minotaurs, Centaurs, Chimeras, Wyverns, a Basilisk, an armed aerozep), an organic weapons factory, fortified gates, and a dedicated law-enforcement division. | Ranks and shards; `Barghest` weapons list; Nighthawks armory; Prevention Unit `[wiki]` `[game-data]` |
| Economy (archetype weakness) | Barghest is economically weak | **Complicates the design.** The lore shows a large, diversified illegal economy: global arms sales, the West Coast's largest black market, smuggling, protection, gambling, hospitality and deal brokerage. It is not poor. Its weakness is structural: one market, one Tunnel, one power plant, an airdrop supply line it does not control, no legitimate finance or real estate, and a population that "teeters on the brink of poverty". Model it as **high illegal cash flow, low legitimacy, extreme chokepoint concentration** — a war economy, not a weak one. | Revenue streams in `../barghest.md` §4; stadium and Tunnel database entries; NUSA white paper `[wiki]` |
| Politics (faction strength) | Barghest is politically strong | **Strongly supported externally, weak internally.** Externally: Hansen carved out a district, is tolerated by Night City and trades with the NUSA and other countries, hosts the city's political and criminal elite, and keeps rivals inside the wall on a leash. Internally: no institution, no deputy, no council; the succession is an armed contest decided by a fixer and a merc. Model **strong external politics, brittle institutional politics**. | Dogtown and Black Sapphire pages; `Run This Town`; City Council row `[wiki]` `[game-data]` |
| Espionage (faction weakness) | Barghest is bad at espionage | **Strongly supported.** The FIA runs two sleeper agents (Reed, Alex) and a safehouse in The Moth with a photo board of the elite; Songbird manipulated Hansen into shooting down Space Force One; NetWatch runs an undercover operation in the Luxor spa; Bennett negotiates with Arasaka behind Hansen's back; Ulmer runs private deals; Paco skims cargo. The New Recruit Directives make counter-intelligence a written priority ("report all observed irregularities … agents of influence"), which is an admission that it is a problem. | `Birds with Broken Wings`; `You Know My Name`; `Treating Symptoms`; `Run This Town`; New Recruit Directives `[wiki]` `[game-data]` |
| Overall fit | The pillars fit the faction's identity | **Good, with two cautions.** Military and Espionage fit cleanly. Politics is strong only in the external, personal sense. Economy is not weak in output; it is fragile in structure. That is the same correction the Maelstrom doc makes, and it should be applied consistently. | Synthesis `[inferred]` |

Design cautions, not redesigns:

- Do **not** model Barghest as poor. Model it as rich in illegal cash and
  poor in resilience: one market, one tunnel, one reactor, one airdrop line.
- Do **not** model Politics as an institution. It is Hansen's personal
  authority plus a customer list. Losing Hansen should cost more than losing a
  business, but less than losing the market.
- Espionage weakness should be **mechanical**: infiltration events (FIA,
  NetWatch, Arasaka, VDB) should be able to reveal the leadership board, steal
  a succession, or turn a corridor lord.

---

## 5. Gaps and uncertainties

### 5.1 Gaps in the politics METHOD

These are improvements the next agent should fold into
[`METHOD.md`](./METHOD.md), not faction trivia.

1. **M1 — The schema changed mid-batch.** §1.2 added `presence_class`, the
   six-class list and the `mentioned`/`off-map` distinction while this doc was
   being written. The batch-1 docs (Maelstrom, Arasaka, Voodoo Boys) are now
   missing `presence_class` and use the old four-class prose. Add a version
   marker to the METHOD or run a migration pass; otherwise every new doc is
   validated against a schema its predecessors fail.
2. **M2 — The entry-name/record-name split is undocumented.** Albert Murphy's
   registry entry is `murphy` but its character record is
   `Character.kruger_combat`. METHOD §2 item 2 says to collect
   `(entryName, characterRecordId)` pairs but assumes the record names the
   person. Add: when the entry name is the only signal, tag the identity
   `[inferred]` and say so.
3. **M3 — The exact-name rule needs a positive form.** "Never substring match"
   is right but insufficient. For each faction, state its **record
   namespace**: here `Character.kurtz` = Hansen, `Character.kurtz_*` = his
   soldiers, `Character.q304_kurt_miniboss` = his boss actor,
   `Character.kurt_hallucination` = his memory, and
   `Character.q101_spider_murphy` = a different Murphy. A one-line namespace
   note per faction would prevent the trap.
4. **M4 — Leaders are often "borrowed" into another faction's community.** The
   single best roster of Barghest's elite is another quest's community,
   `{mq304_com_kurts_wake}` (Hansen's funeral), not a Barghest site. The METHOD
   should say: for a faction with a succession quest, read the funeral/wake/
   party community first.
5. **M5 — Shared social venues are direct relation evidence.** The Sapphire
   party appears as one area row containing Barghest, Tyger Claws, 6th Street,
   NCPD and City Council actors (`{q303_com_paradise_quest_interactions}`), and
   the party community behind it adds an Arasaka contact and the Scav boss Tzar.
   That is stronger than spatial adjacency and should sit between precedence 2
   (transaction) and 3 (quest-giver hostility).
6. **M6 — The stance vocabulary has no "hub" or "recognised authority".**
   Barghest is a de facto government that sells services to everyone. Five
   `trade` rows and twenty-one `neutral` rows describe the data but not the
   structure. Consider a `revenue_role` field (`customer`, `supplier`,
   `broker`, `tolerated`) or a `hub` note.
7. **M7 — The JSON has no `dependent` or `branches` field.** Every Phantom
   Liberty leader is V-dependent. `role` prose is the only place to put it, and
   a parser cannot read that. Add `dependent: true` and an optional `branches`
   list.
8. **M8 — The JSON has no divisions field.** The Prevention Unit is a real
   institution (red armour, replaces NCPD inside the wall) with no faction code
   and no slot in the JSON. Add `sub_units`.
9. **M9 — "Attested relation" is not defined against mere presence.** §1.2
   item 7 now says to add every `factions.json` code with an attested relation.
   Zetatech is named as a covert operator in Dogtown and News 54's Gillean
   Jordan attends the Sapphire party, but neither is a Barghest relation.
   State whether presence alone qualifies; otherwise a parser cannot tell
   whether to expect a row. This document keeps both in prose.
10. **M10 — The template has no civil/governance layer.** For a faction that
    governs a district, the market, airdrops, protection, gates and utilities
    are the substance of its politics. Add a "governance layer" section to §5
    of the playbook; otherwise the doc becomes a list of interiors.
11. **M11 — Cross-doc consistency is unchecked.** `arasaka.md` records Barghest
    as `neutral` with "no attested interaction", but `Run This Town` and the
    Sapphire party are explicit. By contrast, `voodoo-boys.md` (`trade`) and
    `valentinos.md` (`neutral`) already agree with this doc, so the batch is
    only one pair out of step. Add a step: after writing a row, grep the sibling
    docs for the same pair and either align or flag the conflict.
12. **M12 — "Dependent" is the norm in Phantom Liberty, not an exception.**
    The METHOD warns to record V-dependent leaders, but in PL nearly every
    named character is marked "Dependent". The useful distinction is *what*
    depends on V (survival, succession, location), not *that* it does.

### 5.2 Faction uncertainties

1. **No offline attitude matrix.** `Attitude_Record.hpp` is opaque and the
   `Affiliation` enum is identity only. Every stance in §3.2 is judged from
   quests, shards, the wiki and co-location; none is read from a TweakDB
   relation row. A TweakDB dump would settle the neutral rows.
2. **Murphy's record is the weakest link.** `Character.kruger_combat` is the
   actor the registry entry `murphy` points at, and the community is the
   stadium escape boss with reinforcements at `#q304_ws_escape_murphy_boss`.
   The join is strong by context, weak by name. Verify in-game.
3. **Bychkov and Rinder have no character records.** They exist in wiki text,
   photos and quest scripts only. Their JSON rows use `null` records and
   `[wiki]` confidence.
4. **The unidentified FIA-board member and the unnamed old guard.** The board
   has eight photos; the members list names seven of them. The two unnamed
   original soldiers (and the eighth photo) cannot be identified. Do not invent
   a name.
5. **Charles Graham's record is inferred.** The registry has
   `mq304_jago_bodyguard_01` and `_03`, and a wake entry named `boulder` also
   points at `_01`. The wiki says Graham is Jago's bodyguard but does not name
   his record. `[inferred]`.
6. **Ross Ulmer's record is inferred from two signals.** The activity has one
   `mini_boss_1st_phase`, and the wake entry `mq304_ws_wake_ross_ulmer` uses
   the same record. Good, but still a join, not a name.
7. **Dodger's base is in Coastview, not Dogtown.** The former NCPD precinct is
   outside the wall. The gig's infobox says Coastview; the seed puts it in
   `dt_main_gate`. Use the location catalog's placement, not the seed.
8. **The civil layer has no faction id.** Market vendors, Stacks residents,
   Heavy Hearts staff and Mr. Hands are modelled only through prose and the
   fixer codes. A "Dogtown civil" pseudo-faction would be more honest than
   pretending they are neutral parties.
9. **The airdrop supplier is deliberately unidentified.** Do not assign it to
   the NUSA, Militech or anyone else. The wiki's own database entry says it is
   a mystery, and the sergeant/major shard shows Barghest does not know either.
10. **The Prevention Unit has no wiki page and no code.** It is attested only
    in the Barghest notes and the gate text (red armour, replaces NCPD, MaxTac
    exception). Treat it as a Barghest division.
11. **`kurtz` is both a person and a prefix.** The exact-record rule in §1.4 is
    the only safe way to count Hansen; any aggregate by token will overcount by
    hundreds of soldiers.
12. **`Character.kurtz` is not the only Hansen actor.** The boss variant and
    the Cynosure hallucination are separate records. List all three under one
    leader entry, per METHOD §1.1 item 1.
13. **`open_world` is a heuristic.** `world-activity` rows are classified
    `true`, but if the mod disables gigs and scanner activities with the
    campaign, Dodger, Ulmer, Rinder and Araujo disappear too. They need an
    in-game spawn check.
14. **The NUSA row is time-bounded.** Before 2077, Dogtown had "trade
    relations with Night City, the NUSA and other countries". The `war` stance
    is the 2077 state created by the Space Force One conspiracy, not a
    permanent condition. Put the history in the evidence, as the METHOD says.
15. **The City Council row is a tolerance, not a friendship.** The Council
    walled the district and looks away because confronting Hansen is expensive.
    The deputy mayor's attendance is a corrupt social channel, not an alliance.
16. **The Biotechnica and Animals rows are one-record deductions.** Biotechnica
    appears only through the Venture Center and the `Roads to Redemption`
    agents; Animals only as Tzar's bodyguards and airdrop competitors. Keep
    them `neutral`.
17. **Mr. Hands' stance is a judgement call.** He is a fixer with his own code,
    not a faction. `trade` captures the suite, the gigs and the kingmaking; a
    stricter reading would say `neutral` because he serves whoever pays. The
    evidence string carries the nuance.
18. **The `Arasaka` row contradicts `arasaka.md`.** That doc calls the pair
    neutral; this doc calls it `trade` on the strength of `Run This Town` and
    the Sapphire party. One of the two needs correcting. (See §5.1, M11.)
    `voodoo-boys.md` and `valentinos.md` are already symmetric with this doc.
19. **Population is an estimate.** 6,000–8,000 is the NUSA white paper's
    estimate, not a census. Do not use it as a hard number in balance.
20. **Hansen's playable segments are not open-world Hansen.** `Balls to the
    Wall`'s Deep Dive uses `Character.mq301_kurt_initiation_*` proxies; the
    Cynosure memory uses `Character.kurt_hallucination`. Neither is a free-roam
    actor.

### 5.3 Sources consulted

- Local: `data/factions.json`, `data/districts.json`,
  `data/sub_territories.json`, `dist/extract/areas.jsonl`,
  `dist/extract/raw/**/always_loaded_{0,1,2}.streamingsector.json`
  (`worldCommunityRegistryItem` templates, entry names, character record ids
  and spot refs), `refs/RED4ext.SDK/.../game/data/Affiliation.hpp`,
  `refs/RED4ext.SDK/.../game/data/Attitude_Record.hpp`. The roster/site/area
  counts in the front matter are from `docs/research/factions/barghest.md`
  (4 roster sites, 87 units, 187 areas, 1,449 records).
- Wiki: [BARGHEST](https://cyberpunk.fandom.com/wiki/BARGHEST),
  [BARGHEST Members](https://cyberpunk.fandom.com/wiki/BARGHEST_Members),
  [Kurt Hansen](https://cyberpunk.fandom.com/wiki/Kurt_Hansen),
  [Chester Bennett](https://cyberpunk.fandom.com/wiki/Chester_Bennett),
  [Jago Szabó](https://cyberpunk.fandom.com/wiki/Jago_Szab%C3%B3),
  [Albert Murphy](https://cyberpunk.fandom.com/wiki/Albert_Murphy),
  [Yuri Bychkov](https://cyberpunk.fandom.com/wiki/Yuri_Bychkov),
  [Leon Rinder](https://cyberpunk.fandom.com/wiki/Leon_Rinder),
  [Carl Robinson](https://cyberpunk.fandom.com/wiki/Carl_Robinson),
  [Ross Ulmer](https://cyberpunk.fandom.com/wiki/Ross_Ulmer),
  [Charles Graham](https://cyberpunk.fandom.com/wiki/Charles_Graham),
  [Paco Torres](https://cyberpunk.fandom.com/wiki/Paco_Torres),
  [Barbara Okoye](https://cyberpunk.fandom.com/wiki/Barbara_Okoye),
  [Kyle Araujo](https://cyberpunk.fandom.com/wiki/Kyle_Araujo),
  [Fae Nesheim](https://cyberpunk.fandom.com/wiki/Fae_Nesheim),
  [Briana Dolson](https://cyberpunk.fandom.com/wiki/Briana_Dolson),
  [Dogtown](https://cyberpunk.fandom.com/wiki/Dogtown),
  [Black Sapphire](https://cyberpunk.fandom.com/wiki/Black_Sapphire),
  [Heavy Hearts](https://cyberpunk.fandom.com/wiki/Heavy_Hearts),
  [EBM Petrochem Stadium](https://cyberpunk.fandom.com/wiki/EBM_Petrochem_Stadium),
  [Nighthawks Rehabilitation Center](https://cyberpunk.fandom.com/wiki/Nighthawks_Rehabilitation_Center),
  [Dogtown Gate](https://cyberpunk.fandom.com/wiki/Dogtown_Gate),
  [Dogtown Tunnel](https://cyberpunk.fandom.com/wiki/Dogtown_Tunnel),
  [Longshore Stacks](https://cyberpunk.fandom.com/wiki/Longshore_Stacks),
  [Golden Pacific](https://cyberpunk.fandom.com/wiki/Golden_Pacific),
  [Terra Cognita](https://cyberpunk.fandom.com/wiki/Terra_Cognita),
  [Airdrops](https://cyberpunk.fandom.com/wiki/Cyberpunk_2077_Airdrops),
  [Dog Eat Dog](https://cyberpunk.fandom.com/wiki/Dog_Eat_Dog),
  [Lucretia My Reflection](https://cyberpunk.fandom.com/wiki/Lucretia_My_Reflection),
  [You Know My Name](https://cyberpunk.fandom.com/wiki/You_Know_My_Name),
  [Birds with Broken Wings](https://cyberpunk.fandom.com/wiki/Birds_with_Broken_Wings),
  [Firestarter](https://cyberpunk.fandom.com/wiki/Firestarter),
  [Run This Town](https://cyberpunk.fandom.com/wiki/Run_This_Town),
  [Balls to the Wall](https://cyberpunk.fandom.com/wiki/Balls_to_the_Wall),
  [Gig: Waiting for Dodger](https://cyberpunk.fandom.com/wiki/Gig:_Waiting_for_Dodger),
  [Gig: Heaviest of Hearts](https://cyberpunk.fandom.com/wiki/Gig:_Heaviest_of_Hearts),
  [Gig: Roads to Redemption](https://cyberpunk.fandom.com/wiki/Gig:_Roads_to_Redemption),
  [Gig: Treating Symptoms](https://cyberpunk.fandom.com/wiki/Gig:_Treating_Symptoms),
  [Gig: The Man Who Killed Jason Foreman](https://cyberpunk.fandom.com/wiki/Gig:_The_Man_Who_Killed_Jason_Foreman),
  [Increased Criminal Activity: BARGHEST](https://cyberpunk.fandom.com/wiki/Increased_Criminal_Activity:_BARGHEST),
  [New Recruit Directives](https://cyberpunk.fandom.com/wiki/New_Recruit_Directives),
  [Awaiting Your Signal](https://cyberpunk.fandom.com/wiki/Awaiting_Your_Signal),
  [Dogtown – Analytical Summary](https://cyberpunk.fandom.com/wiki/Dogtown_%E2%80%93_Analytical_Summary),
  [Dogtown - a splinter in the eye of Night City](https://cyberpunk.fandom.com/wiki/Dogtown_-_a_splinter_in_the_eye_of_Night_City),
  [Archived Conversation: BARGHEST SERGEANT #2615 and BARGHEST CAPTAIN #482](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_BARGHEST_SERGEANT_2615_and_BARGHEST_CAPTAIN_482),
  [Archived Conversation: BARGHEST SERGEANT #278 and BARGHEST MAJOR #78](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_BARGHEST_SERGEANT_278_and_BARGHEST_MAJOR_78),
  [Archived Conversation: Ayo Zarin and Carl "Dodger" Robinson](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Ayo_Zarin_and_Carl_%22Dodger%22_Robinson),
  [Archived Conversation: Fyodor Vasiliev and Carl "Dodger" Robinson](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Fyodor_Vasiliev_and_Carl_%22Dodger%22_Robinson),
  [Archived Conversation: Carl "Dodger" Robinson and Chester Bennett](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Carl_%22Dodger%22_Robinson_and_Chester_Bennett),
  [Scavengers](https://cyberpunk.fandom.com/wiki/Scavengers),
  [Voodoo Boys](https://cyberpunk.fandom.com/wiki/Voodoo_Boys),
  [NCPD](https://cyberpunk.fandom.com/wiki/NCPD),
  [Night City Council](https://cyberpunk.fandom.com/wiki/Night_City_Council),
  [NetWatch](https://cyberpunk.fandom.com/wiki/NetWatch),
  [MaxTac](https://cyberpunk.fandom.com/wiki/MaxTac),
  [Rosalind Myers](https://cyberpunk.fandom.com/wiki/Rosalind_Myers),
  [Solomon Reed](https://cyberpunk.fandom.com/wiki/Solomon_Reed),
  [Song So Mi](https://cyberpunk.fandom.com/wiki/Song_So_Mi),
  [Wade Bleecker](https://cyberpunk.fandom.com/wiki/Wade_Bleecker),
  [Space Force One](https://cyberpunk.fandom.com/wiki/Space_Force_One).
- Earlier repo research: `docs/research/factions/barghest.md`,
  `docs/research/factions/politics/maelstrom.md`,
  `docs/research/factions/politics/arasaka.md`,
  `docs/research/factions/politics/voodoo-boys.md`,
  `docs/design/gameplay-systems.md`.

---

## 6. Machine-readable block

```json
{
  "faction_code": "barghest",
  "leaders": [
    {
      "name": "Kurt Hansen",
      "role": "Colonel; founder, commander and de facto ruler of Dogtown",
      "character_record_id": "Character.kurtz",
      "location_name": "Black Sapphire (floor 99) / EBM Stadium deal room / Dogtown north gate",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_1 registry entry kurtz -> Character.kurtz (phases q301_01_start, q301_04_start, q301_blackmarket_announcement, q303_casino, q303_restaurant_host; spots #q301_ws_01_kurtz, #q301_ws_04_kurtz, #q301_ws_02a_kurt_announcement, #q303_ws_kurt_paradise_casino, #q304_07_ws_kurt_deal_start); boss variant Character.q304_kurt_miniboss; memory variant Character.kurt_hallucination; wiki Kurt Hansen",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Chester Bennett",
      "role": "Lieutenant Colonel; commander of the armed forces; Hansen's chief aide; successor claimant",
      "character_record_id": "Character.mq304_bennett",
      "location_name": "Black Sapphire (party and Hansen's wake) / Stadium escape",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_1 registry entry bennett -> Character.mq304_bennett (phases mq304_01_meeting, mq304_after_combat_alley, mq304_wake_booth, mq304_wake_start); party variant Character.q303_paradise_bennett; wiki Chester Bennett",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Jago Szabó",
      "role": "Chief accountant (treasurer); successor claimant",
      "character_record_id": "Character.mq304_jago",
      "location_name": "Luxor Heights (Voodoo Boys meeting) / Black Sapphire / Stadium",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_1 registry entry jago -> Character.mq304_jago (phases meeting_arrive, meeting_spawn, q301_border, wake_bennett, wake_booth; spots #mq304_ws_jago_vdb_arrive, #q301_ws_01_jago_gate_cargo, #mq304_ws_jago_wake_booth); party variant Character.q303_paradise_jago; wiki Jago Szabo",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Albert Murphy",
      "role": "High-ranking old-guard officer; Hansen's negotiator and enforcer of the district's order",
      "character_record_id": "Character.kruger_combat",
      "location_name": "EBM Petrochem Stadium (market escape)",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_1 registry entry murphy -> Character.kruger_combat (phase q304_01_start; spot #q304_ws_escape_murphy_boss); entry-name join, verify in-game; wiki Albert Murphy; FIA photo board",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "name": "Yuri Bychkov",
      "role": "Lieutenant; old guard; convoy and generator command; out of favour in 2077",
      "character_record_id": null,
      "location_name": "Black Sapphire garrison / Stadium",
      "presence_class": "story",
      "open_world": false,
      "source": "wiki Yuri Bychkov; Balls to the Wall; FIA photo board; no character record found",
      "confidence": "wiki"
    },
    {
      "name": "Leon Rinder",
      "role": "Old guard; founding member; cyberpsychotic ex-member",
      "character_record_id": null,
      "location_name": "Longshore Stacks / Los Osos Motel (West Wind Estate)",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "wiki Leon Rinder; Gig: The Man Who Killed Jason Foreman (baseid sts_ep1_03); FIA photo board; no character record found",
      "confidence": "wiki"
    },
    {
      "name": "Carl \"Dodger\" Robinson",
      "role": "High-ranking non-veteran; drug revenue; airdrop and smuggling logistics; claims to be Hansen's right hand",
      "character_record_id": "Character.sts_ep1_10_dodger",
      "location_name": "Former Pacifica NCPD Precinct (Coastview) / Black Sapphire wake",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "raw always_loaded_1 registry entry dodger -> Character.sts_ep1_10_dodger (phase mq304_wake_dodger); community 9529329004064786977 with sts_ep1_10_dodger_goon_01/02; wiki Carl Robinson",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Ross Ulmer",
      "role": "Lieutenant in charge of the Dogtown Tunnel; private side deals; helped Rinder escape",
      "character_record_id": "Character.we_ep1_01_mini_boss_1st_phase",
      "location_name": "Dogtown Tunnel (Longshore Stacks to West Wind Estate)",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "wake entry mq304_ws_wake_ross_ulmer -> Character.we_ep1_01_mini_boss_1st_phase; Increased Criminal Activity: BARGHEST baseid we_ep1_01; wiki Ross Ulmer",
      "confidence": "game-data+wiki+inferred"
    }
  ],
  "internal_factions": [
    {
      "name": "The Midnight Storm old guard",
      "leader": "Kurt Hansen",
      "goals": "Keep the founding squad's primacy, Hansen's personal rule and the army's identity; resist being treated as obsolete",
      "members_hint": "Six survivors in lore; Murphy, Bychkov and Rinder are explicitly labelled former squadmates; the FIA photo board shows four of them",
      "source": "Barghest database entry ('only six soldiers remain'); member pages; Birds with Broken Wings",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Bennett's command corps",
      "leader": "Chester Bennett",
      "goals": "Military continuity, command of the forces, the succession, and outside corporate backing",
      "members_hint": "13 wake_bennett_guard_* entries (11 Barghest records plus 2 VDB non-reaction actors) and 3 bodyguards; kurtz_soldier*/elite* records; the Arasaka dummy deal",
      "source": "Bennett's rank and DB entry; Run This Town; wake community 3323591791502479431",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Jago's finance and administration wing",
      "leader": "Jago Szabó",
      "goals": "Monetise the district, professionalise it, and take the chair with the accountants' leverage",
      "members_hint": "9 wake_jago_guard_* entries and 2 bodyguards; mq304_com_ce_ma_sc_06; the Voodoo Boys meeting; Charles Graham",
      "source": "Jago's DB entry; Awaiting Your Signal; Run This Town",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Dodger's revenue wing",
      "leader": "Carl \"Dodger\" Robinson",
      "goals": "Autonomy, drug money, control of airdrop and courier logistics, indispensability",
      "members_hint": "sts_ep1_10_dodger_goon_01/02; 12 Voodoo Boys netrunners hired for the Sapphire party; courier-loop records; the former NCPD precinct base",
      "source": "Gig: Waiting for Dodger; Ayo Zarin shard; Run This Town",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Ulmer's Tunnel fief",
      "leader": "Ross Ulmer",
      "goals": "Private profit from the border, control of the Tunnel, protection of old comrades",
      "members_hint": "we_ep1_01_* garrison of 10+ records including a Centaur; the wake entry",
      "source": "Increased Criminal Activity: BARGHEST; Ulmer's wiki biography",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The new recruits",
      "leader": null,
      "goals": "A fresh start, a salary, survival, and a chance to rise",
      "members_hint": "New Recruit Directives; Paco's tent in front of the Sapphire; the mass of generic kurtz_* records",
      "source": "Balls to the Wall; New Recruit Directives; Paco Torres and Barbara Okoye database entries",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The civil layer (non-member power centres)",
      "leader": "Briana Dolson",
      "goals": "Keep trading, keep autonomy, and keep the district stable enough to profit",
      "members_hint": "Longshore Stacks community and vendors; the market tenants; Mr. Hands's suite at Heavy Hearts",
      "source": "Longshore Stacks page; Gig: The Man Who Killed Jason Foreman; Run This Town",
      "confidence": "wiki+game-data"
    }
  ],
  "relations": [
    {
      "faction_code": "tyger_claws",
      "stance": "trade",
      "evidence": "Jotaro Shobo, Maiko Maeda, Marcus Ichida and Jun Azegami attend Hansen's Black Sapphire party [wiki]; 6 Tyger Claws records in the floor-99 community q303_com_paradise_quest_interactions [game-data]; Dodger's past includes gravely insulting a prominent Tyger Claws boss, sheltered by Hansen [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "valentinos",
      "stance": "neutral",
      "evidence": "No attested interaction; different district. The Valentinos' Hector Sacristan is hunted by a D.A. who frequents Heavy Hearts, but that is not a Barghest relationship [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "arasaka",
      "stance": "trade",
      "evidence": "Bennett negotiates with a dummy company backed by Arasaka in Run This Town, seeking collaboration behind Hansen's back [wiki]; two q303_paradise_arasaka_contact actors at the Sapphire party [game-data]; the FIA white paper lists covert Arasaka and Zetatech operations in Dogtown [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "militech",
      "stance": "neutral",
      "evidence": "The unit was Militech and deserted in 2070; Militech's Cynosure bunkers sit under Dogtown and the stadium bunker holds the neural matrix; the FIA white paper lists Militech deserters as a subject of interest [wiki] [game-data]; no 2077 Militech operation against Dogtown is attested",
      "confidence": "wiki+game-data+inferred"
    },
    {
      "faction_code": "kang_tao",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "biotechnica",
      "stance": "neutral",
      "evidence": "Abandoned Biotechnica Venture Center in Luxor Heights; Biotechnica agents pursue a Crimson Harvest defector inside the Nighthawks armory in Gig: Roads to Redemption, with no Barghest response attested [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "petrochem",
      "stance": "neutral",
      "evidence": "The stadium bears Petrochem's name as a historic sponsor; Jago was imprisoned for embezzling Petrochem funds in 2066 before helping found Barghest in 2072 [wiki]; no current relation",
      "confidence": "wiki"
    },
    {
      "faction_code": "sixth_street",
      "stance": "trade",
      "evidence": "The Tunnel database entry uses 6th Street as the worked customer: sixty Militech M251s Ajax rifles delivered in 48 hours [wiki]; an unnamed 6th Street leader attends the Sapphire party [game-data]; a scripted 10-strong 6th Street protest community q302_com_protesters and a 6th Street reinforcement record at the armory sts_ep1_07_reinforcements show friction [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "aldecaldos",
      "stance": "neutral",
      "evidence": "No attested interaction; Paco can be smuggled out with Panam's help only as a personal favour to V [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "wraiths",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "animals",
      "stance": "neutral",
      "evidence": "Animals appear as the Scav boss Tzar's hired bodyguards at the Sapphire party and as airdrop competitors, not as Barghest counterparts [game-data] [wiki]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "the_mox",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "maelstrom",
      "stance": "neutral",
      "evidence": "No attested interaction; maelstrom.md records Barghest as neutral [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "voodoo_boys",
      "stance": "trade",
      "evidence": "Dogtown VDB do business in the Stadium and protect the data of Hansen's guests; the symbiotic relationship can seem shaky but Hansen keeps it a little rumble and not a full-blown earthquake [wiki]; Dodger hires 12 VDB netrunners for the Sapphire party [wiki]; Jago meets them for support [wiki]; a VDB tip led to the netrunner selling airdrop coordinates [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "ncpd",
      "stance": "hostile",
      "evidence": "NCPD is forbidden in Dogtown and cannot drive through the gate [wiki]; the Pacifica precinct was disbanded in 2072 after local groups, Barghest and the Voodoo Boys among them, expelled the NCPD [wiki]; Dodger holds two NCPD officers prisoner and blackmails one [wiki]; yet the NCPD commissioner attends Hansen's party, a corrupt elite channel [wiki] [game-data]; MaxTac is the one NCPD unit allowed in [wiki]",
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
      "evidence": "The Council built the Serenisands wall and later decided to look the other way rather than confront Hansen [wiki]; deputy mayor Weldon Holt attends the Sapphire party [wiki] [game-data]; one City Council record in the floor-99 community [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "scavengers",
      "stance": "rival",
      "evidence": "In business with Barghest as frequently as they clash; the Scav oligarchy secures business in Hansen's backyard because it is all about the money [wiki]; Scavs steal airdrops, ambush Paco's convoy and fight Barghest in the airdrop arena sa_ep1_113_com_combat [game-data] [wiki]; Tzar attends the party [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_regina",
      "stance": "neutral",
      "evidence": "She takes in the cyberpsychotic Rinder at V's request; no anti-Barghest campaign [wiki]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "fixer_wakako",
      "stance": "neutral",
      "evidence": "No Barghest-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_padre",
      "stance": "neutral",
      "evidence": "No Barghest-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_el_capitan",
      "stance": "neutral",
      "evidence": "No Barghest-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_dakota",
      "stance": "neutral",
      "evidence": "No Barghest-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_dino",
      "stance": "neutral",
      "evidence": "No Barghest-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_rogue",
      "stance": "neutral",
      "evidence": "No Barghest-specific gig or lore link found; Afterlife is neutral ground [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_mr_hands",
      "stance": "trade",
      "evidence": "He keeps a suite at Heavy Hearts and runs Dogtown gigs from it [wiki] [game-data]; he brokers the succession in Run This Town, preferring Bennett and paying V to steer it [wiki]; a gig warns V not to cause trouble at the club because he operates out of there [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "afterlife",
      "stance": "neutral",
      "evidence": "Neutral merc marketplace; no Barghest-specific link [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "nusa",
      "stance": "war",
      "evidence": "Hansen arranged with Songbird to shoot down Space Force One and kill President Myers [wiki] [game-data]; FIA agents Reed and Alex run a safehouse and a leadership photo board in The Moth [wiki]; the NUSA white paper rates Dogtown a Level 2 threat to NUS security interests and names Militech deserters and covert Arasaka/Zetatech operations [wiki]; the crash site holds 45 NUSA records [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "netwatch",
      "stance": "neutral",
      "evidence": "An undercover NetWatch agent, Alan Noël, runs an operation against the Dogtown Voodoo Boys from the Luxor spa without Barghest interference [wiki] [game-data]; NetWatch's Blackwall mandate intersects the Blackwall AI and neural matrix Hansen held [wiki]; no direct contact is attested; one NetWatch area in Coastview, ma_pac_cvi_10_drone_com [game-data]",
      "confidence": "game-data+inferred"
    }
  ]
}
```
