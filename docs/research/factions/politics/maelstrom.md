# Maelstrom — Leadership, Internal Politics and External Relations

Status: pilot research run, 2026-11-25. One faction, one document.
Scope: Cyberpunk 2077 2.5 + Phantom Liberty, campaign disabled. This is the
first document in the `politics/` research type: who a player can join under,
climb past, ally with or remove; the internal blocs; and the external relations
matrix needed for wars, alliances and "guarantor" support when a player founds
a gang.

Method: this document follows the evidence rules in
[`../METHOD.md`](../METHOD.md) (tags, local-data precedence, wiki usage). The
location catalog for Maelstrom is
[`../maelstrom.md`](../maelstrom.md); this document does not repeat it — it maps
people and politics onto those places. New here: the raw sector extracts
(`dist/extract/raw/**/always_loaded_*.streamingsector.json`) are used to recover
named-NPC character records that `data/sites/rosters.json` does not contain.

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/comic/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My reasoning links a named person, place or stance to a record; reasoning stated | Weak, flagged |

Extra convention for this document only: **presence class**.
`ambient` = persists in free roam without a quest; `world-activity` = gig,
scanner hustle or NCPD activity, i.e. free-roam content but still activity-
gated; `story` = gated by the *Pickup* / *Second Conflict* quest chain;
`historical` = not present in 2077. The JSON `open_world` flag is `true` for
`ambient` + `world-activity`, `false` for `story` + `historical`.

---

## 1. Leadership and ranks

### 1.1 The 2077 chain of command

Maelstrom is a **boostergang**, not a corporate hierarchy. Lore gives a boss,
one or more lieutenants, and functional crews — not a formal rank ladder.
The 2077 top is unusually unstable because the boss took power in a coup.

| Name | 2077 role | Character record | Location / influence point | Presence class | Source | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| **Simon "Royce" Randall** | Boss (2077, after coup) | `Character.Royce` (also `Character.q003_royce_boss`, `Character.q003_maelstrom_royce_boss`) | All Foods Plant (boss fight) and Totentanz (club floor) | `story` | Raw sector community registry, `always_loaded_1`; markers `q003_mp_royce_bossfight_start`, `royce_sm_default`, `sq011_07a_sm_royce`; wiki *Simon Randall* | `[game-data]` `[wiki]` |
| **Declan "the Brick" Griffin** | Deposed boss / rival claimant (2070s–2077) | `Character.Brick` | All Foods Plant, makeshift cell | `story` | Raw sector registry entry `brick`, initial phase `q003_brick_hiding`; marker `q003_mp_brick_prison_door_terminal`; wiki *Declan Griffin* | `[game-data]` `[wiki]` |
| **Dum Dum** | Royce's lieutenant; deal-maker and gatekeeper | `Character.DumDum` | All Foods Plant (deal room) and Totentanz entrance | `story` | Raw sector registry entry `DumDum`; markers `dumdum_sm_default`, `q003_spwn_player_walk_dumdum`; wiki *Dum Dum* | `[game-data]` `[wiki]` |
| **Ofelia "Patricia" Sirawian** | Brick's lieutenant; succession leader if Royce falls and Brick is not freed | `Character.sq011_patricia` | Totentanz | `story` | Raw sector registry entry `sq011_patricia`; area `{sq011_patricia}` at `(-1734.0, 2217.8, 82.2)`; wiki *Patricia* | `[game-data]` `[wiki]` |

The wiki marks every 2077 leadership entry "dependent": the actual boss depends
on player choices in *The Pickup* and *Second Conflict*. That is not a bug in
the sources — it is the canonical picture of a gang whose succession is decided
by violence.

### 1.2 Succession history: why the top keeps changing

The full leadership line, from the wiki's *Maelstrom* page and the individual
pages:

| Period | Leader | How the change happened |
| --- | --- | --- |
| 2010s–2023 | **Hammer** | Founder; ex-Metal Warrior; killed in the 2023 Night City Holocaust. `[wiki]` |
| 2023–2027 | **Crusher** | Took over the survivors, seized Burleson Tower/Totentanz; went cyberpsycho in 2027 and vanished into the Hot Zone. `[wiki]` |
| 2027–2030s | **Hextra** | Succeeded Crusher; killed by MAX-TAC. No dedicated wiki page survives. `[wiki]` |
| 2030s–2045 | **Warlock** | Rose with Quake and Flenser backing; reorganized the gang around Totentanz and Hot Zone scavenging; made deals with corporate agents. `[wiki]` |
| unknown–2070s | **Caliber** | Led in the 2070s (comics *XOXO*, *Kickdown*); assassinated, possibly by NCPD/MaxTac. `[wiki]` `[lore]` |
| 2070s–2077 | **Declan "Brick" Griffin** | Led until Royce's coup; imprisoned at All Foods. `[wiki]` |
| 2077 | **Royce** | Mutinied against Brick, purged Brick loyalists, took the All Foods crew. `[wiki]` |

The pattern is consistent: **succession is violent and often external.** Hammer
died in a nuclear event; Crusher left via cyberpsychosis; Hextra was killed by
MAX-TAC; Caliber was assassinated; Brick was deposed by his own lieutenant.
Warlock is the exception — a leader who consolidated power through deals and
lieutenants — and even he inherited a gang that had just lost its leader to
MAX-TAC.

Historical secondary leaders worth knowing for a succession model: **Quake**
(Warlock's brutal enforcer), **Flenser** (Warlock's netrunner/intelligence
chief), **Ripper** (Hot Zone scavenging overseer who nearly broke away with the
scavengers), and **Joe Pitt** (HQ maintenance and equipment). `[wiki]` `[lore]`

### 1.3 Rank structure, initiation and advancement

Lore does not name formal ranks beyond **boss** and **lieutenant**. What it
does describe is a cell structure and a chrome-based entry requirement:

1. **Boss.** Single leader. In 2077, Royce. Commands through fear and a small
   loyal core; the database entry calls him "polarizing … either his goons love
   him … or they hate him." `[wiki]`
2. **Lieutenants.** Dum Dum (Royce's representative and negotiator) and
   Patricia (Brick's main lieutenant and Militech contact). They handle deals,
   discipline and the club. `[wiki]`
3. **Crews.** "Partitioned … into smaller groups, each responsible for a
   different part of their criminal empire": 4–5 members for turf patrols, up to
   30 for raids, hit jobs or cargo protection. `[wiki]`
4. **Functional specialists.** Netrunners (Flenser, Dixie), ripperdocs (Kaiser
   Herzog), braindance editors (Gottfrid and Fredrik Persson), scavenging
   overseers (Ripper), negotiators (Dum Dum). `[wiki]` `[lore]`
5. **Members.** The mass of gangers. No formal probationary rank is described.

**Initiation and chrome requirements.** Entry is not a ceremony alone; it is a
surgical transformation:

- "No one joined them without undergoing an extensive cyberware implantation
  that not only changed their looks to appear less human and more machine-like,
  but also enhanced their bodies." `[wiki]`
- **HeavenMed** in Northside is where Maelstrom performs its initiation
  procedures — ocular implants. The gig *Rite of Passage* sends V to steal a
  recording of the initiation rite from the clinic's server room. `[wiki]`
  `[game-data]`
- The gang's creed is that metal is better than meat; members use pain editors,
  cyberoptics and reflex boosters, and many sit on the edge of cyberpsychosis.
  In 2020 about a third were registered cyberpsychos; the rest were "hovering
  near the edge." `[wiki]`
- Wearing the chrome of fallen members is a mark of honour, at least in the
  2045 Burleson Tower period. `[wiki]` `[lore]`
- Advancement is reputational: survive, perform violence, show loyalty to the
  current boss, and receive better chrome and a crew role. Royce's takeover
  explicitly promoted his followers and treated Brick's loyalists as traitors.
  `[wiki]`

**Practical consequence for the mod:** "chrome" is both the entry gate and the
promotion currency. A simulation can model advancement as a threshold on
`technology`/cyberware investment plus loyalty to the current bloc, with
cyberpsychosis as the failure state.

### 1.4 Named members mapped to game data

Most named NPCs are **not in `data/sites/rosters.json`**. The exceptions are
Gottfrid and Fredrik Persson, who are roster entries at site 410. Royce, Brick,
Dum Dum, Patricia and the named gig bosses live in the raw sector community
templates, which is why this section names the exact record. Rows marked
`[inferred]` are one-record deductions (e.g. the only "miniboss"/"psycho"
record at a gig's `baseid`); verify in-game before treating them as canonical.

| Name | Role / note | Character record | Community / site | Location | Presence class | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| Simon "Royce" Randall | Boss | `Character.Royce` | `{q003_factory_combat_main}` (7), `{sq011_club_gangers}` (14) | All Foods Plant; Totentanz | `story` | `[game-data]` `[wiki]` |
| Declan "Brick" Griffin | Deposed boss | `Character.Brick` | Raw registry entry `brick`; cell terminal marker | All Foods Plant cell | `story` | `[game-data]` `[wiki]` |
| Dum Dum | Royce's lieutenant | `Character.DumDum` | `{q003_com_deal}` (6), `{sq011_club_gangers}` (14) | All Foods; Totentanz | `story` | `[game-data]` `[wiki]` |
| Ofelia "Patricia" Sirawian | Brick's lieutenant / successor | `Character.sq011_patricia` | `{sq011_patricia}` (1) | Totentanz | `story` | `[game-data]` `[wiki]` |
| Kurt | Deal-room member; welcomed V and Jackie | `Character.q003_maelstrom_deal_01` (inferred) | `{q003_com_deal}` (6) | All Foods | `story` | `[inferred]` `[wiki]` |
| Lars | Deal-room member; welcomed V and Jackie | `Character.q003_maelstrom_deal_03` (inferred) | `{q003_com_deal}` (6) | All Foods | `story` | `[inferred]` `[wiki]` |
| Brandon Frost | HeavenMed guard; cast Animals in concrete for an XBD | `Character.nid_05_maelstrom_officer` (inferred; no named record found) | `{#nid_05_com}` (10) | HeavenMed | `world-activity` | `[inferred]` `[wiki]` |
| Othmar Brasi | HeavenMed guard; Rite of Passage enemy | `Character.nid_05_maelstrom_othmar_brasi` | `{#nid_05_com}` (10) | HeavenMed | `world-activity` | `[game-data]` `[wiki]` |
| Ellis Carter | Totentanz bouncer; Brick supporter; cyberpsycho | `Character.ma_wat_nid_03_shard_psycho` (inferred; only psycho record at `baseid=ma_wat_nid_03`) | Site 217 `ma_wat_nid_03` | Totentanz environs / cyberpsycho lair | `world-activity` | `[inferred]` `[wiki]` |
| Dietlinde | Totentanz bartender/vendor; remains regardless of quests | `Character.sq011_bar_owner` (inferred; entry `sq011_barowner`) | `{sq011_club_gangers}` (14) | Totentanz bar | `ambient` | `[inferred]` `[wiki]` |
| Kaiser "the Surgeon" Herzog | Unlicensed ripperdoc; NCPD target | `Character.ma_wat_nid_06_outpost_miniboss` (inferred; only miniboss at `baseid=ma_wat_nid_06`) | `{ma_wat_nid_06_com}` (10) | Clean Cut clinic | `world-activity` | `[inferred]` `[wiki]` |
| Tom "Ymir" Ayer | Serial killer; runs a stim racket near Megabuilding H12 | `Character.ma_wat_nid_02_outpost_miniboss` (inferred; only miniboss at `baseid=ma_wat_nid_02`) | `{ma_outpost_01_com}` (13) | Maelstrom outpost 01, Richmond St | `world-activity` | `[inferred]` `[wiki]` |
| Gottfrid Persson | XBD editor; works for Maelstrom but scan says not officially affiliated | `Character.sts_wat_nid_04_gottfrid` | `{nid_04_com}` (9) | Gottfrid & Fredrik's XBD studio | `world-activity` | `[game-data]` `[wiki]` |
| Fredrik Persson | XBD editor; Gottfrid's son | `Character.sts_wat_nid_04_fredrik` | `{nid_04_com}` (9) | Gottfrid & Fredrik's XBD studio | `world-activity` | `[game-data]` `[wiki]` |
| Zaria Hughes | Cyberpsycho after a botched Net connection | no 2077 record found | — | — | `historical` | `[wiki]` `[lore]` |
| Mat Duda | Raided an Arasaka warehouse on Dum Dum's orders | no 2077 record found | — | — | `historical` | `[wiki]` `[lore]` |
| Hans Otto | Critically injured by Scavengers; Lucy Thackery tries to save him | no 2077 record found | — | — | `historical` | `[wiki]` `[lore]` |
| Bertie Thackery | Ex-member; left in exchange for his sister's service | no 2077 record found | — | — | `historical` | `[wiki]` `[lore]` |
| Karla; Dixie | Novel characters (*No Coincidence*); Dixie is a netrunner | no 2077 record found | — | — | `historical` | `[wiki]` `[lore]` |

Two data cautions:

- **`Patricia` is a name collision.** `Character.sts_std_arr_06_sixthstreet_patrol2_ranged2_ajax_wa_Patricia`
  is a 6th Street NPC in Arroyo, not Maelstrom's Patricia. Use
  `Character.sq011_patricia`.
- **`kurt` is a substring trap.** Barghest's Colonel Kurt Hansen uses
  `kurtz_*`; a substring search for `kurt` matches thousands of records. The
  Maelstrom deal-room members are `Character.q003_maelstrom_deal_01/03`, and
  the wiki calls them Kurt and Lars; there is no `Character.Kurt` for the
  Maelstrom member.

### 1.5 What the game actually spawns (open world vs story-only)

This is the part other agents must not assume. A named NPC in a wiki infobox
does not mean an actor in free roam.

**`ambient` — persists in free roam.**
- **Dietlinde** at the Totentanz bar. The wiki says she "will remain a vendor in
  this location regardless of quests involving it." Her record is a quest-named
  `Character.sq011_bar_owner`, but the behavior is ambient. `[wiki]`
  `[game-data]`

**`world-activity` — gig, scanner hustle or NCPD activity; free-roam content but
activity-gated.**
- **Othmar Brasi** and **Brandon Frost** at HeavenMed (*Gig: Rite of Passage*,
  `baseid=sts_wat_nid_05`). Othmar has a named record; Brandon does not. `[wiki]`
  `[game-data]`
- **Ellis Carter** at the Totentanz environs (*Cyberpsycho Sighting: Where the
  Bodies Hit the Floor*, `baseid=ma_wat_nid_03`). `[wiki]` `[game-data]`
- **Kaiser Herzog** at Clean Cut (*Suspected Organized Crime Activity: No
  License, No Problem*, `baseid=ma_wat_nid_06`). `[wiki]` `[game-data]`
- **Tom Ayer** at the Richmond St yard (*Suspected Organized Crime Activity:
  Just Say No*, `baseid=ma_wat_nid_02`). `[wiki]` `[game-data]`
- **Gottfrid and Fredrik Persson** at the XBD studio (*Gig: Dirty Biz*,
  `baseid=sts_wat_nid_04`). `[game-data]` `[wiki]`

**`story` — gated by *The Pickup* / *Second Conflict*; do not expect them in
free roam with the campaign disabled.**
- Royce, Brick, Dum Dum, Patricia, Kurt, Lars. Their communities are initial-
  phase quest states (`q003_brick_hiding`, `q003_bossfight`,
  `sq011_patricia_by_brick`, etc.), and their markers are quest markers. `[game-data]`

**`historical` — not in 2077 at all.**
- Hammer, Crusher, Hextra, Warlock, Quake, Flenser, Ripper, Joe Pitt, Caliber.
  `[wiki]` `[lore]`

Caveat: "campaign disabled" may also suppress gigs and scanner hustles if the
mod disables all quest content. The `world-activity` rows are the best reuse
candidates, but they still need an in-game spawn check. The `story` rows are
the ones to replace with simulation agents, not expect the game to provide.

### 1.6 Player-path hooks

This is the design-facing summary of who a player can join under, climb past,
ally with or remove.

| Person | Join under | Climb past | Ally with | Remove |
| --- | --- | --- | --- | --- |
| **Royce** | Violent expansion, corporate heists, no outside deals | Dum Dum is the gatekeeper; the All Foods garrison is his power base | Dum Dum (pragmatic), the XBD techies (product), a ripperdoc (chrome) | Killing Royce opens the Brick/Patricia succession |
| **Brick** | Restoration of the old boss; revenge on Royce | Patricia is his lieutenant and the practical gatekeeper | Patricia, Ellis Carter (if still alive), Brick loyalists in hiding | Freeing Brick restores him; leaving him in the cell lets Patricia take over |
| **Dum Dum** | Transactional business, smuggling, outside deals | He is already a lieutenant; climbing past him means a coup or a promotion under a new boss | Dum Dum is the most plausible **ally** for a business-minded player | Removing Dum Dum decapitates the deal wing |
| **Patricia** | Order, control of Totentanz, protection from media enemies | She is Brick's lieutenant; a player under her climbs past her only by removing her | Patricia is the natural ally of a Totentanz-based player | Removing Patricia leaves the club without a political operator |
| **Gottfrid & Fredrik** | Not a joinable path; they are a **power centre** | — | Ally for XBD product and distribution | Removing them cuts the XBD supply |

The design consequence: Maelstrom has **no single legitimate ladder**. A player
can back Royce, back Brick, back Patricia, or back Dum Dum's business wing, and
each choice changes which locations and crews are friendly.

---

## 2. Internal political factions

### 2.1 The blocs

"Members" counts below are **presence proxies** from
`dist/extract/areas.jsonl`, not membership rolls. The All Foods communities are
overlapping quest phases of one site, so do not sum them.

| Bloc | Leader(s) | What it wants | Presence / members hint | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- |
| **Royce's All Foods loyalists** | Simon "Royce" Randall; Dum Dum as lieutenant | Violent expansion, corporate heists, control of the Militech/Flathead loot, no concessions to outsiders | All Foods: `{q003_factory_combat_main}` 7, `{q003_com_deal}` 6, `{q003_com_main_hall}` 5, `{q003_com_lab}` 5. Outpost 01: `{ma_outpost_01_com}` 13 | Royce's coup; Dum Dum's promotion; Brick loyalists "treated as traitors" | `[game-data]` `[wiki]` |
| **Brick's old guard** | Declan "Brick" Griffin (imprisoned); Ofelia "Patricia" Sirawian as lieutenant | Restore Brick, punish Royce, return to the old arrangement | All Foods cell; Patricia at Totentanz; Ellis Carter as the last open supporter; other supporters told to hide | *All Foods Factory* page; *Archived Conversation: Brick and Ellis*; *Second Conflict* | `[game-data]` `[wiki]` |
| **Patricia's Totentanz clique / succession** | Ofelia "Patricia" Sirawian | Control the gang and the Totentanz cash cow; eliminate media enemies; punish Royce | Totentanz: `{sq011_club_gangers}` 14, `{sq011_thugs}` 5, `{sq011_patricia}` 1 | *Second Conflict* branch where Patricia takes over and attacks V; she kidnapped and beat Bes Isis | `[game-data]` `[wiki]` |
| **Dum Dum's deal-makers / business wing** | Dum Dum | Transactional business, outside deals, survival; less ideology | All Foods deal room (`{q003_com_deal}` 6); Totentanz entrance; Kurt and Lars | Dum Dum handles the Flathead deal; prefers Samurai/anti-corp oldies; shows concern for Royce | `[game-data]` `[wiki]` |
| **Chrome cult / cyberpsycho current** | No single leader; Ellis Carter as martyr, Zaria Hughes as example, Crusher as historical case | More chrome, rituals, transcendence; contempt for "weak flesh" | Diffuse: Totentanz, HeavenMed, cyberpsycho dens; about a third of the gang were registered cyberpsychos in 2020 | Gang philosophy; initiation; *Cyberpsycho Sighting: Where the Bodies Hit the Floor*; Zaria Hughes | `[wiki]` `[lore]` |
| **XBD workshop (non-member power centre)** | Gottfrid and Fredrik Persson | Profit, autonomy, protection for their studio | XBD studio: `{nid_04_com}` 9; 12 roster units at site 410 | Works for Maelstrom and "appear to have substantial power," but scanning shows them not officially affiliated | `[game-data]` `[wiki]` |

### 2.2 Royce vs Brick: the 2077 split

This is the cleanest internal conflict in the game and the pilot's reason for
choosing Maelstrom.

- **Brick** was the boss. He used **Patricia** as his messenger to Militech's
  **Anthony Gilchrist**, trading convoy routes for a cut of the stolen
  shipments. He ignored Patricia's warning that **Royce** was a "feral animal"
  and should be shot in the back of the head. `[wiki]`
- **Royce** provoked Brick into a show-off on the All Foods production floor,
  then captured him when Brick arrived alone. Brick told his supporters to go
  into hiding; Royce and Dum Dum took the gang. Everyone else was told Brick had
  died. `[wiki]` `[game-data]`
- **Ellis Carter** was Brick's last open supporter. He tried to take revenge on
  Royce alone, was tortured by fellow Maelstrom members (Hoof and Sanders),
  had his cyberware replaced, was drugged, and became a cyberpsycho bouncer at
  the Totentanz. `[wiki]`
- **Patricia** survived the purge because she was useful: she was Brick's
  Militech contact and the gang's link to the Gilchrist channel. `[wiki]`

The split is therefore **not just personal**. It maps onto a policy difference:

- **Royce's line:** violence, heists, no outside deals except on his terms.
- **Brick's line:** transactional deals with corporate insiders (Gilchrist),
  which brought in money but also dependency and exposure.
- **Dum Dum's line:** keep the deals working, keep the boss alive, avoid
  unnecessary fights.

That is a real, simulation-ready axis: **ideological violence vs. transactional
crime**.

### 2.3 Patricia and the succession

Patricia is the swing piece. She is Brick's lieutenant, but she is also the
person who can lead the gang if Royce is removed and Brick is not freed.

- If **Brick is freed** and Royce is defeated, Brick retakes control and
  Patricia stands beside him, frustrated with his methods but loyal. `[wiki]`
- If **Brick is killed or left in his cell** and Royce is defeated, Patricia
  takes over. She thanks V for removing Royce, then attacks V to protect the
  gang from the media (she had kidnapped and beaten Bes Isis). `[wiki]`
- If **Royce survives** and Brick is not freed, Patricia does not appear in
  *Second Conflict* at all. `[wiki]`

For a simulation, Patricia is the **continuity candidate**: she preserves the
gang's external relationships (Militech channel, Totentanz) better than Royce
and is more pragmatic than Brick. She is also the most likely to purge Royce's
remaining loyalists, which creates a second round of internal conflict.

### 2.4 Dum Dum and the business wing

Dum Dum is Royce's lieutenant, but he is written as the gang's **diplomat**:

- He handles the original Flathead deal with V and Jackie, offers S-keef, and
  keeps the negotiation controlled. `[wiki]`
- He openly shows concern for Royce's welfare, and the two "get along
  remarkably well" despite divergent methods. `[wiki]`
- He prefers anti-corporate oldies like Samurai to the gang's neo-death metal,
  and "respects differences in taste." `[wiki]`
- He leads V and Jackie out after a peaceful deal and warns them not to return:
  "repeat business deals are not Maelstrom's nature." `[wiki]`

That is enough to model a **deal-makers' wing**: members who value the
Militech/Gilchrist channel, the drug and cyberware trade, and survival over
Royce's pure violence. It is not an organized faction in lore, but it is the
most plausible internal opposition to a leader who kills every customer.

### 2.5 The chrome cult and cyberpsychosis

Maelstrom's ideology is genuinely held by some members, not just a costume:

- "Metal is better than meat"; extensive cyberware is an entry requirement and
  a status marker. `[wiki]`
- Occult-inspired tattoos and rituals; initiation at HeavenMed; the gang's
  "creepy rituals" were developed by Ripper and Quake in the 2040s. `[wiki]`
- Cyberpsychosis is an occupational hazard and a political event: Ellis Carter
  becomes a bouncer-turned-monster; Zaria Hughes becomes a cyberpsycho after a
  botched Net connection; Crusher disappears into the Hot Zone after an
  episode. `[wiki]`
- In 2020, about a third of the gang were registered cyberpsychos. `[wiki]`

For simulation, this is a **membership-quality** pressure, not a conventional
bloc: high-chrome members are powerful but unstable, and a leader who pushes
chrome too hard risks losing them to psychosis or to a MAX-TAC response.

### 2.6 The XBD workshop: a non-member power centre

Gottfrid and Fredrik Persson run an illegal braindance studio in Northside.
The wiki's member list says they "are working for Maelstrom and appear to have
substantial power within the gang," but "scanning them in the game shows that
they are not officially affiliated with Maelstrom." `[wiki]`

This is a useful design wrinkle: a **client/asset** with leverage but no vote.
They can supply product, demand protection, or defect to another buyer. Their
site is a real interior with 9-12 Maelstrom guards (`{nid_04_com}` 9, roster 12),
so they are also a capture target.

### 2.7 Historical precedents for internal conflict

- **Warlock vs. Ripper (2040s).** Warlock worried that Ripper, the Hot Zone
  scavenging overseer, would break away with the scavengers he forced to dig
  out tech. Ripper was killed before it happened, but the fear was real. `[wiki]`
- **Warlock's lieutenants.** Quake (brutality) and Flenser (netrunning/
  intelligence) were essential to Warlock's rule; a leader without lieutenants
  could not hold the gang. `[wiki]`
- **Crusher's disappearance.** A cyberpsychotic episode removed the boss and
  created a succession crisis. `[wiki]`
- **Caliber's assassination.** External violence (possibly NCPD/MaxTac) removed
  a leader; the gang did not fracture, but the succession was set by an outside
  actor. `[wiki]` `[lore]`
- **The 2045 Tyger Claws clash.** Expansion into Old Japantown was a leadership
  project; failure or success would have strengthened or weakened the boss. `[wiki]`

### 2.8 What could drive internal conflict in a simulation

Evidence-based drivers, in rough order of plausibility:

1. **Succession after removing the boss.** Royce's death opens a three-way
   contest: Dum Dum (Royce's man), Patricia (Brick's lieutenant), Brick (if
   freed). Each has a different external policy.
2. **Ideology vs. business.** Royce's no-deals line vs. Dum Dum's deal-making
   and the Gilchrist channel. A player who brings in outside contracts can
   strengthen the business wing and weaken the boss.
3. **Distribution of loot.** The Flathead, the Malorian Arms van, Arasaka cargo,
   and the XBD masters are all contested resources. A leader who keeps too much
   loses the crews; one who shares too much looks weak.
4. **Treatment of Brick loyalists.** Purge (Royce), reintegrate (Brick), or
   use-and-discard (Patricia). Each choice creates or removes a bloc.
5. **Control of Totentanz.** The club is the cash cow and the only neutral
   ground where all gangs obey Maelstrom's customs. Whoever holds it has
   political leverage; whoever loses it loses the gang's public face.
6. **Cyberpsychosis attrition.** High-chrome members become liabilities; a
   leader who ignores it loses crews to MAX-TAC or to internal violence.
7. **External pressure.** NCPD/MAX-TAC, Tyger Claws, Scavengers, the Mox and
   Animals can unite the gang or expose a leader's failure. The historical
   pattern is that external violence often decides the succession.

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

There is **no usable offline attitude matrix**. `refs/RED4ext.SDK/.../game/data/Affiliation.hpp`
is an identity enum (Maelstrom = 10, MaelstromAndroid = 11), not a relation
table; `Attitude_Record.hpp` is opaque. The stances below are therefore judged
from quests, wiki and spatial adjacency, not from a TweakDB relation row. That
is why every row carries a tag and why the neutral rows are not claims of
friendship.

| Faction | Code | Stance | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| Tyger Claws | `tyger_claws` | `rival` | 2045 expansion into Old Japantown clashed with the Tyger Claws `[wiki]`; adjacent Little China and Kabuki turf: 9 + 7 areas, 7 + 8 spawn points `[game-data]`; Kimen-Gumi formerly secured the Ebunike Docks `[wiki]` | `game-data+wiki` |
| Valentinos | `valentinos` | `neutral` | No attested interaction; different district (Heywood). Do not infer a rivalry from both being gangs `[inferred]` | `inferred` |
| Arasaka | `arasaka` | `hostile` | Maelstrom raids corporate transports and sells stolen tech `[wiki]`; 9 Maelstrom hold Memorial Ring West (`ma_cct_cpz_01`) inside an Arasaka-owned sub-territory `[game-data]`; Arasaka merc Jeremiah Grayson guards the Ebunike, a Maelstrom-affiliated dock `[wiki]` `[game-data]` | `game-data+wiki` |
| Militech | `militech` | `hostile` | *The Pickup*: Militech raids the All Foods Plant `[wiki]`; corrupt Militech employee Anthony Gilchrist leaked convoy routes to Brick and Patricia, and Maelstrom stole the Flathead `[wiki]`; 2 distinct `q003_meat_factory_militech_*` character records placed 21 times in the raw sector `[game-data]` | `game-data+wiki` |
| Kang Tao | `kang_tao` | `neutral` | No attested interaction; only generic "corporate transports" in lore. `[inferred]` | `inferred` |
| Biotechnica | `biotechnica` | `neutral` | No attested interaction. `[inferred]` | `inferred` |
| Petrochem | `petrochem` | `neutral` | No attested interaction. `[inferred]` | `inferred` |
| Barghest | `barghest` | `neutral` | No attested interaction; Dogtown Maelstrom presence is generic opposition (`sq025_com_thugs_mean`), not a relationship `[game-data]` `[inferred]` | `game-data+inferred` |
| 6th Street | `sixth_street` | `neutral` | Maelstrom has gang-watch encounters in Rancho Coronado and Arroyo (`ma_std_rcr_*`) but no lore conflict `[game-data]` `[inferred]` | `game-data+inferred` |
| Aldecaldos | `aldecaldos` | `neutral` | No attested interaction; possible smuggling overlap only `[inferred]` | `inferred` |
| Wraiths | `wraiths` | `neutral` | No attested interaction; both are smugglers, but no shared operation or feud is attested `[inferred]` | `inferred` |
| Animals | `animals` | `rival` | Brandon Frost cast several Animals alive in concrete and made an XBD; the Animals forced the recordings off the market `[wiki]`; both are heavy-chrome gangs `[wiki]` | `wiki` |
| The Mox | `the_mox` | `rival` | Caliber's crew stole a Mox convoy shard and killed Moxes in the 2070s `[wiki]` `[lore]`; the Mox are listed as a Northside gang alongside Maelstrom `[wiki]` `[game-data]` | `game-data+wiki` |
| Voodoo Boys | `voodoo_boys` | `neutral` | No attested interaction; both are Net-obsessed, but different districts and no shared operation `[inferred]` | `inferred` |
| NCPD | `ncpd` | `hostile` | Hextra killed by MAX-TAC `[wiki]`; Caliber assassinated, possibly by NCPD/MaxTac `[wiki]`; Maelstrom is a standing NCPD target and the subject of scanner hustles and organized-crime activities `[wiki]` `[game-data]`; but an NCPD sergeant buys Maelstrom CCTV footage in *Scrolls before Swine* — a corrupt trade channel `[wiki]` | `game-data+wiki` |
| Night Corp | `night_corp` | `neutral` | No attested interaction; a corp, not a turf actor `[inferred]` | `inferred` |
| City Council | `city_council` | `neutral` | No attested interaction; political, not territorial `[inferred]` | `inferred` |
| Scavengers | `scavengers` | `rival` | Compete for the same chrome and salvage `[wiki]`; Caliber sold the traitor Screw to the Scavengers for a painful death `[wiki]`; Maelstrom's Hot Zone operations pushed scavver groups to bolder violence `[wiki]`; the scav/ripperdoc grey market also feeds the chrome trade `[wiki]` | `wiki` |
| Regina Jones | `fixer_regina` | `hostile` | Regina gives V the gigs *Rite of Passage* and *Hippocratic Oath*, and the cyberpsycho sighting that targets Ellis Carter; she warns V about Maelstrom `[wiki]` `[game-data]` | `game-data+wiki` |
| Wakako Okada | `fixer_wakako` | `neutral` | No Maelstrom-specific gig or lore link found `[inferred]` | `inferred` |
| Sebastian Ibarra (Padre) | `fixer_padre` | `neutral` | No Maelstrom-specific gig or lore link found `[inferred]` | `inferred` |
| Muamar Reyes (El Capitan) | `fixer_el_capitan` | `neutral` | No Maelstrom-specific gig or lore link found `[inferred]` | `inferred` |
| Dakota Smith | `fixer_dakota` | `neutral` | No Maelstrom-specific gig or lore link found `[inferred]` | `inferred` |
| Dino Dinovic | `fixer_dino` | `trade` | In the 2070s Dino sold out Screw's whereabouts to Maelstrom "to stay in good graces with Maelstrom"; Caliber then captured Screw `[wiki]` `[lore]`. A precedent, not a 2077 standing arrangement | `wiki+lore` |
| Rogue Amendiares | `fixer_rogue` | `neutral` | *Chippin' In* is Rogue's operation against Arasaka's Ebunike/Grayson, not against Maelstrom; Afterlife is neutral ground `[wiki]` `[inferred]` | `wiki+inferred` |
| Mr. Hands | `fixer_mr_hands` | `neutral` | No Maelstrom-specific gig or lore link found `[inferred]` | `inferred` |
| Afterlife | `afterlife` | `neutral` | Neutral merc marketplace and neutral ground; Maelstrom's own neutral ground is the Totentanz `[wiki]` `[inferred]` | `wiki+inferred` |

### 3.3 Actors outside `data/factions.json`

These are real relationships but have no faction code, so they are prose only.

- **Red Cab** — the Maelstrom infobox lists `affiliations = Red Cab`; in 2020,
  Red Cab's headquarters was a Maelstrom-guarded location. In 2077 Red Cab is a
  taxi company; no game-data link survives. Treat as `[lore]`/historical
  affiliate, not a current guarantor. `[wiki]`
- **Dexter DeShawn** — the fixer who bought the Flathead from Brick's
  Maelstrom; the deal is the inciting incident of *The Pickup*. A one-off
  **client**, not a faction. `[wiki]`
- **Inquisitors** — the gang's defining enemy from the 2010s to the 2040s;
  Maelstrom was formed partly from anti-Inquisitor remnants and kept stomping
  them. No 2077 presence. `[wiki]`
- **Warrior Heart** — the rival gang Crusher destroyed to take Burleson Tower in
  2023. `[wiki]`
- **StormTech** — the convoy Crusher slaughtered in 2027 before disappearing. `[wiki]`
- **Rocklin Augmentics** — involved in the death of Ripper, the Hot Zone
  scavenging overseer. `[wiki]`
- **Anthony Gilchrist** — the corrupt Militech employee who leaked convoys to
  Brick and Patricia. An individual channel, not a faction. `[wiki]`

### 3.4 Guarantor assessment

This is the design question: if a player founds a gang, which factions would
guarantee Maelstrom's support, and which would Maelstrom itself guarantee?

- **No faction is an ally.** The matrix has no `ally`, `patron` or `client` row
  for a full faction. The matrix's only `trade` row is a 2070s precedent with
  Dino Dinovic; its only `hostile`-with-a-channel relationships are Militech
  (Gilchrist) and NCPD (a corrupt sergeant).
- **Maelstrom is a poor guarantor.** A player who takes over Maelstrom inherits
  its enemies (NCPD, Tyger Claws, the Mox, Scavengers, Animals) and its
  transactional channels, not a bloc of allies. The gang's political capital is
  the Totentanz neutral ground and fear, both of which are fragile.
- **Plausible guarantors for a player-founded gang** are therefore
  transactional, not ideological: a corrupt Militech officer (Gilchrist-type),
  Dino Dinovic (a fixer with a favor economy), the Scavengers (paid, unreliable),
  or a revived Red Cab arrangement (`[lore]`, no 2077 data).
- **Maelstrom as an aggressor.** For a player founding a gang on a Scav-held or
  Maelstrom-held point, Maelstrom is more likely to be the **pre-emptive
  attacker** than the guarantor: it wars low-respect upstarts and preys on
  Scav-held points. That is consistent with its `hostile`/`rival` rows.

---

## 4. Pillar notes

Design claims from `docs/design/gameplay-systems.md`: Maelstrom is an
**Ideological Collective** (archetype strength Culture, weakness Economy);
faction strength **Technology**, weakness **Politics**.

| Pillar | Design claim | Lore verdict | Evidence |
| --- | --- | --- | --- |
| Technology (strength) | Maelstrom is a tech-obsessed chrome cult | **Strongly supported.** Chrome is the entry requirement, the status marker and the gang's main product. Netrunners, ripperdocs, XBD editors, bot hacking and Hot Zone salvage are all attested. | Extensive cyberware, ocular implants at HeavenMed, Flathead demo, `nid_maelstrom_netrunner_*`, Gottfrid/Fredrik, Kaiser Herzog `[wiki]` `[game-data]` |
| Politics (weakness) | Maelstrom cannot do politics | **Supported, with one complication.** No codes, coup-based succession, no allies, a boss who is "impossible to control," and a Royce/Brick split. But the Totentanz is a real political asset: all gangs are welcome "so long as they obeyed Maelstrom's authority and customs," and Warlock was an explicit deal-maker with corporate agents. The weakness is **fragile, personalized politics**, not the absence of politics. | Coup, Royce database entry, Totentanz rules, Warlock's corporate deals `[wiki]` |
| Culture (archetype strength) | Ideological Collective binds through culture | **Supported but inward-facing.** "Metal is better than meat," occult rituals, initiation, wearing fallen chrome, the Totentanz as a cultural venue, XBD of suffering. It binds members and repels outsiders; it has little export beyond the club and XBD. The business wing is pragmatic, not ideological. | Gang philosophy, rituals, Totentanz, XBD `[wiki]` |
| Economy (archetype weakness) | Maelstrom is economically weak | **Complicates the design.** The lore shows a diversified illegal economy: drugs (main stream), smuggling, cyberware, XBD, chop shops, arms, Totentanz nightlife and contract violence. It is not poor. Its weakness is structural: no legitimate front, no finance/real-estate, no political protection, and revenue concentrated in raid-able docks, warehouses and clinics. Model it as **high illegal income, low legitimacy and low resilience**, not "low output." | Revenue streams in `../maelstrom.md` §4; wiki sources-of-income `[wiki]` |
| Overall fit | The pillars fit the gang's identity | **Good for identity, imperfect for balance sheet.** Keep Technology strong and Politics weak. Treat Economy as "illegal-only and fragile," and Culture as "high internal cohesion, low external legitimacy." | Synthesis of the rows above `[inferred]` |

Design cautions, not redesigns:

- Do **not** model Maelstrom as a poor gang. Model it as a gang whose income is
  illegal, geographically concentrated and politically unprotected.
- Do **not** model Politics as zero. The Totentanz is a genuine political
  institution; losing it should hurt more than losing a generic business.
- The chrome cult is a **membership-quality** mechanic, not a conventional
  faction: it produces powerful but unstable members and a MAX-TAC response.

---

## 5. Gaps and uncertainties

1. **No offline attitude matrix.** `refs/RED4ext.SDK/.../game/data/Attitude_Record.hpp`
   is opaque (no field names), and the `Affiliation` enum only gives identity,
   not pairwise relations. Every stance in §3.2 is judged from quests, wiki and
   spatial adjacency; none is read from a TweakDB relation table. A TweakDB dump
   would settle the neutral rows.
2. **The 2077 leadership is not in `data/sites/rosters.json`.** Royce, Brick,
   Dum Dum and Patricia exist only in the raw sector community registry; the
   named-gig bosses are represented by generic records. This is the same "rosters
   miss quest communities" problem as METHOD §1.2 item 6, but worse for named
   characters.
3. **Several character-record mappings are inferred, not exact.** Ellis Carter
   (`ma_wat_nid_03_shard_psycho`), Tom Ayer (`ma_wat_nid_02_outpost_miniboss`),
   Kaiser Herzog (`ma_wat_nid_06_outpost_miniboss`), Dietlinde
   (`sq011_bar_owner`), Brandon Frost (`nid_05_maelstrom_officer`) and Kurt/Lars
   (`q003_maelstrom_deal_01/03`) are one-record deductions from the gig's
   `baseid` or the only named slot. Verify in-game before seeding them.
4. **Brick has no character marker.** The cell terminal marker
   `q003_mp_brick_prison_door_terminal` is a proxy for his location, not his
   actor position. Patricia has no marker either; `{sq011_patricia}` is a
   community-area anchor at `z=82.2`, which is a floor-level position, not an
   exact actor position.
5. **Kurt and Lars have no distinct records.** The wiki names them, but the
   raw sector only has `Character.q003_maelstrom_deal_01` and `_03` in the deal
   community. They may be those two bodyguards, or one may be a generic
   `q003_maelstrom_rifle_*`. Flagged `[inferred]`.
6. **Grayson is Arasaka, not Maelstrom.** `Jeremiah Grayson` is an Arasaka
   mercenary guarding Adam Smasher's Ebunike. The Ebunike *location* infobox
   lists `affiliation = Tyger Claws (formerly), Maelstrom`, which is about the
   dock, not Grayson. Do not list him as Maelstrom leadership.
7. **"Open world with the campaign disabled" is a heuristic.** I classify
   `ambient` and `world-activity` as `open_world: true`, but the mod may disable
   gigs and scanner hustles along with the campaign. The `story` rows are
   definitely not ambient; the `world-activity` rows need an in-game spawn
   check.
8. **Brandon Frost has no named record.** The wiki lists him as a HeavenMed
   enemy alongside Othmar Brasi, but only Othmar has a named record
   (`Character.nid_05_maelstrom_othmar_brasi`). Brandon is inferred to be the
   generic `nid_05_maelstrom_officer` or one of the rifle/shotgun records.
9. **Gottfrid and Fredrik are a contradiction in the sources.** Their own wiki
   pages say `affiliation = Maelstrom`; the *Maelstrom Members* page says
   scanning shows they are "not officially affiliated." I treat them as a
   non-member power centre and flag both readings.
10. **No member counts per clique.** The community counts are presence proxies,
    not rolls. The All Foods communities are overlapping quest phases of one
    site (`q003_com_deal`, `q003_factory_combat_main`, `q003_com_main_hall`,
    `q003_com_lab`, `q003_com_garage`, `q003_com_transition`), so summing them
    overstates the garrison.
11. **Historical leaders are book/comic lore.** Hammer, Crusher, Hextra,
    Warlock, Quake, Flenser, Ripper and Caliber have no 2077 records. **Hextra
    has no dedicated wiki page**; the name comes from the *Maelstrom* leadership
    list and the Warlock page. Caliber is from the *XOXO* and *Kickdown* comics.
12. **Several factions have zero direct evidence.** Kang Tao, Biotechnica,
    Petrochem, Barghest, Voodoo Boys, Aldecaldos, Wraiths, Wakako, Padre, El
    Capitan, Dakota, Rogue and Mr. Hands are `neutral`/`[inferred]` placeholders.
    Do not promote them to `rival` or `trade` without a source.
13. **Red Cab has no `factions.json` code.** It is an attested affiliate in the
    infobox and a 2020 guarded location, but it is not in the JSON matrix. If a
    later design needs it, add a code first; do not smuggle it in as a gang.
14. **Historic actors have no 2077 codes.** Inquisitors, Warrior Heart,
    StormTech and Rocklin Augmentics are real lore relationships but not
    2077 factions; they stay in prose.
15. **Phantom Liberty adds no Maelstrom leadership content.** The only
    Phantom Liberty-era Maelstrom presence is generic Dogtown opposition
    (`sq025_com_thugs_mean`); the Corpo Plaza hold-out (`ma_cct_cpz_01`) is
    base-game. No new leader, bloc or relation is introduced.
16. **Machines are not members.** The roster has
    `Character.nid_maelstrom_android_android2_pulsar_ma` and the Affiliation enum
    has `MaelstromAndroid = 11`. Report machines separately; they do not vote in
    a succession.
17. **Name collisions.** `Patricia` also names a 6th Street NPC
    (`Character.sts_std_arr_06_sixthstreet_patrol2_ranged2_ajax_wa_Patricia`);
    `kurt` is a substring of Barghest's `kurtz_*` records. Use exact records.
18. **`areas.jsonl.district_code` is still unsafe.** The Maelstrom Dogtown,
    Corpo Plaza and Charter Hill hits include generic opposition communities;
    this document uses the geocoded names and the location catalog's
    re-attribution, not `district_code`.
19. **`sub_territory_id` is a nearest-centroid guess.** It is not used for any
    political claim here. The one politically relevant exception is
    `ma_cct_cpz_01`: Maelstrom-held at Memorial Ring West inside an
    Arasaka-owned sub-territory, which is evidence of a forward hold-out, not of
    Arasaka ownership.
20. **The wiki's "dependent" statuses are choices, not canon.** Royce, Brick,
    Dum Dum, Patricia, Ellis, Othmar and others are marked "dependent" because
    their survival depends on V. A simulation must choose a branch or model the
    branches explicitly.

### 5.1 Sources consulted

- Local: `data/sites/rosters.json`, `data/sites/sites.json`,
  `data/sites/{guards,triggers,spots,patrols,doors,communities}.json`,
  `data/factions.json`, `data/control_centers.json`,
  `data/sub_territories.json`, `data/districts.json`,
  `dist/extract/areas.jsonl`, `dist/extract/markers.jsonl`,
  `dist/extract/raw/**/always_loaded_{0,1,2}.streamingsector.json` (community
  registry templates and `characterRecordId` values),
  `refs/RED4ext.SDK/.../game/data/Affiliation.hpp`,
  `refs/RED4ext.SDK/.../game/data/Attitude_Record.hpp`.
- Wiki: [Maelstrom](https://cyberpunk.fandom.com/wiki/Maelstrom),
  [Maelstrom Members](https://cyberpunk.fandom.com/wiki/Maelstrom_Members),
  [Simon Randall](https://cyberpunk.fandom.com/wiki/Simon_Randall),
  [Declan Griffin](https://cyberpunk.fandom.com/wiki/Declan_Griffin),
  [Dum Dum](https://cyberpunk.fandom.com/wiki/Dum_Dum),
  [Patricia](https://cyberpunk.fandom.com/wiki/Patricia),
  [Totentanz](https://cyberpunk.fandom.com/wiki/Totentanz),
  [All Foods Factory](https://cyberpunk.fandom.com/wiki/All_Foods_Factory),
  [Second Conflict](https://cyberpunk.fandom.com/wiki/Second_Conflict_(quest)),
  [The Pickup](https://cyberpunk.fandom.com/wiki/The_Pickup),
  [Jeremiah Grayson](https://cyberpunk.fandom.com/wiki/Jeremiah_Grayson),
  [Anthony Gilchrist](https://cyberpunk.fandom.com/wiki/Anthony_Gilchrist),
  [Hammer](https://cyberpunk.fandom.com/wiki/Hammer_(Maelstrom)),
  [Crusher](https://cyberpunk.fandom.com/wiki/Crusher_(character)),
  [Warlock](https://cyberpunk.fandom.com/wiki/Warlock),
  [Quake](https://cyberpunk.fandom.com/wiki/Quake_(character)),
  [Flenser](https://cyberpunk.fandom.com/wiki/Flenser),
  [Caliber](https://cyberpunk.fandom.com/wiki/Caliber),
  [Ellis Carter](https://cyberpunk.fandom.com/wiki/Ellis_Carter),
  [Brandon Frost](https://cyberpunk.fandom.com/wiki/Brandon_Frost),
  [Kaiser Herzog](https://cyberpunk.fandom.com/wiki/Kaiser_Herzog),
  [Tom Ayer](https://cyberpunk.fandom.com/wiki/Tom_Ayer),
  [Dietlinde](https://cyberpunk.fandom.com/wiki/Dietlinde),
  [Othmar Brasi](https://cyberpunk.fandom.com/wiki/Othmar_Brasi),
  [Gottfrid Persson](https://cyberpunk.fandom.com/wiki/Gottfrid_Persson),
  [Fredrik Persson](https://cyberpunk.fandom.com/wiki/Fredrik_Persson),
  [Cyberpsycho Sighting: Where the Bodies Hit the Floor](https://cyberpunk.fandom.com/wiki/Cyberpsycho_Sighting:_Where_the_Bodies_Hit_the_Floor),
  [Suspected Organized Crime Activity: Just Say No](https://cyberpunk.fandom.com/wiki/Suspected_Organized_Crime_Activity:_Just_Say_No),
  [Suspected Organized Crime Activity: No License, No Problem](https://cyberpunk.fandom.com/wiki/Suspected_Organized_Crime_Activity:_No_License,_No_Problem),
  [Gig: Rite of Passage](https://cyberpunk.fandom.com/wiki/Gig:_Rite_of_Passage),
  [Gig: Hippocratic Oath](https://cyberpunk.fandom.com/wiki/Gig:_Hippocratic_Oath).
- Earlier repo research: `docs/research/factions/maelstrom.md`,
  `docs/research/factions/METHOD.md`, `docs/design/gameplay-systems.md`.

---

## 6. Machine-readable block

```json
{
  "faction_code": "maelstrom",
  "leaders": [
    {
      "name": "Simon \"Royce\" Randall",
      "role": "Boss (2077, after coup)",
      "character_record_id": "Character.Royce",
      "location_name": "All Foods Plant / Totentanz",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_1 community registry (Character.Royce, Character.q003_royce_boss); markers q003_mp_royce_bossfight_start, royce_sm_default, sq011_07a_sm_royce; wiki Simon Randall",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Declan \"the Brick\" Griffin",
      "role": "Deposed boss / rival claimant (2070s-2077)",
      "character_record_id": "Character.Brick",
      "location_name": "All Foods Plant (cell)",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_1 community registry entry brick, initial phase q003_brick_hiding; marker q003_mp_brick_prison_door_terminal; wiki Declan Griffin",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Dum Dum",
      "role": "Royce's lieutenant; deal-maker and gatekeeper",
      "character_record_id": "Character.DumDum",
      "location_name": "All Foods Plant / Totentanz",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_1 community registry entry DumDum; markers dumdum_sm_default, q003_spwn_player_walk_dumdum; wiki Dum Dum",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Ofelia \"Patricia\" Sirawian",
      "role": "Brick's lieutenant; succession leader",
      "character_record_id": "Character.sq011_patricia",
      "location_name": "Totentanz",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_1 community registry entry sq011_patricia; area {sq011_patricia} at -1734.0,2217.8,82.2; wiki Patricia",
      "confidence": "game-data+wiki"
    }
  ],
  "internal_factions": [
    {
      "name": "Royce's All Foods loyalists",
      "leader": "Simon \"Royce\" Randall",
      "goals": "Violent expansion, corporate heists, control of Militech/Flathead loot, no concessions to outsiders",
      "members_hint": "All Foods garrison: q003_factory_combat_main 7, q003_com_deal 6, q003_com_main_hall 5, q003_com_lab 5; outpost ma_outpost_01_com 13",
      "source": "Royce coup; Dum Dum promotion; Brick loyalists treated as traitors; wiki Simon Randall and Dum Dum",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Brick's old guard",
      "leader": "Declan \"Brick\" Griffin (imprisoned); Ofelia \"Patricia\" Sirawian (lieutenant)",
      "goals": "Restore Brick, punish Royce, return to the old arrangement",
      "members_hint": "All Foods cell; Patricia at Totentanz; Ellis Carter as last open supporter; other supporters told to hide",
      "source": "wiki All Foods Factory; Archived Conversation: Brick and Ellis; wiki Second Conflict",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Patricia's Totentanz clique",
      "leader": "Ofelia \"Patricia\" Sirawian",
      "goals": "Control the gang and the Totentanz cash cow, eliminate media enemies, punish Royce",
      "members_hint": "Totentanz: sq011_club_gangers 14, sq011_thugs 5, sq011_patricia 1; her Maelstromer posse",
      "source": "wiki Second Conflict branch where Patricia takes over and attacks V; she kidnapped Bes Isis",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Dum Dum's deal-makers",
      "leader": "Dum Dum",
      "goals": "Transactional business, outside deals, survival; less ideology",
      "members_hint": "q003_com_deal 6; Kurt and Lars; Totentanz entrance crew",
      "source": "wiki Dum Dum; The Pickup deal; Dum Dum's preference for Samurai/anti-corp oldies",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Chrome cult / cyberpsycho current",
      "leader": null,
      "goals": "More chrome, rituals, transcendence; contempt for weak flesh",
      "members_hint": "Diffuse across Totentanz, HeavenMed and cyberpsycho dens; about a third of the gang were registered cyberpsychos in 2020",
      "source": "wiki Maelstrom philosophy; Cyberpsycho Sighting: Where the Bodies Hit the Floor; Zaria Hughes; Crusher",
      "confidence": "wiki+lore"
    },
    {
      "name": "XBD workshop (non-member power centre)",
      "leader": "Gottfrid Persson",
      "goals": "Profit, autonomy, protection for the studio",
      "members_hint": "nid_04_com 9; site 410 roster 12; Fredrik Persson",
      "source": "wiki Maelstrom Members note; wiki Gottfrid Persson and Fredrik Persson; site sts_wat_nid_04",
      "confidence": "game-data+wiki"
    }
  ],
  "relations": [
    {
      "faction_code": "tyger_claws",
      "stance": "rival",
      "evidence": "2045 Old Japantown clash [wiki]; adjacent Little China/Kabuki turf: 9+7 areas, 7+8 spawns [game-data]; Kimen-Gumi formerly held Ebunike Docks [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "valentinos",
      "stance": "neutral",
      "evidence": "No attested interaction; different district (Heywood) [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "arasaka",
      "stance": "hostile",
      "evidence": "Raids corporate transports and sells stolen tech [wiki]; 9 Maelstrom hold ma_cct_cpz_01 inside an Arasaka-owned sub-territory [game-data]; Arasaka merc Grayson guards the Ebunike [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "militech",
      "stance": "hostile",
      "evidence": "Militech raids All Foods in The Pickup [wiki]; corrupt Militech employee Gilchrist leaked convoy routes to Brick/Patricia [wiki]; 2 distinct q003_meat_factory_militech_* character records placed 21 times [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "kang_tao",
      "stance": "neutral",
      "evidence": "No attested interaction; only generic corporate transports in lore [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "biotechnica",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "petrochem",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "barghest",
      "stance": "neutral",
      "evidence": "No attested interaction; Dogtown Maelstrom presence is generic opposition (sq025_com_thugs_mean) [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "sixth_street",
      "stance": "neutral",
      "evidence": "Gang-watch encounters in Rancho Coronado/Arroyo (ma_std_rcr_*) but no lore conflict [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "aldecaldos",
      "stance": "neutral",
      "evidence": "No attested interaction; possible smuggling overlap only [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "wraiths",
      "stance": "neutral",
      "evidence": "No attested interaction; both smugglers, but no shared operation or feud [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "animals",
      "stance": "rival",
      "evidence": "Brandon Frost cast Animals in concrete and made an XBD; the Animals forced it off the market [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "the_mox",
      "stance": "rival",
      "evidence": "Caliber's crew stole a Mox convoy shard and killed Moxes in the 2070s [wiki] [lore]; the Mox are listed as a Northside gang [wiki] [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "voodoo_boys",
      "stance": "neutral",
      "evidence": "No attested interaction; different districts, no shared operation [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "ncpd",
      "stance": "hostile",
      "evidence": "Hextra killed by MAX-TAC [wiki]; Caliber assassinated, possibly by NCPD/MaxTac [wiki]; standing NCPD target and scanner-hustle subject [wiki] [game-data]; corrupt sergeant buys Maelstrom CCTV footage in Scrolls before Swine [wiki]",
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
      "evidence": "No attested interaction; political, not territorial [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "scavengers",
      "stance": "rival",
      "evidence": "Compete for the same chrome and salvage [wiki]; Caliber sold the traitor Screw to the Scavengers [wiki]; Maelstrom's Hot Zone operations pushed scavver groups to bolder violence [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "fixer_regina",
      "stance": "hostile",
      "evidence": "Regina gives the gigs Rite of Passage and Hippocratic Oath and the Ellis Carter cyberpsycho sighting; she warns V about Maelstrom [wiki] [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_wakako",
      "stance": "neutral",
      "evidence": "No Maelstrom-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_padre",
      "stance": "neutral",
      "evidence": "No Maelstrom-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_el_capitan",
      "stance": "neutral",
      "evidence": "No Maelstrom-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_dakota",
      "stance": "neutral",
      "evidence": "No Maelstrom-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_dino",
      "stance": "trade",
      "evidence": "In the 2070s Dino sold out Screw's whereabouts to Maelstrom to stay in good graces; Caliber then captured Screw [wiki] [lore]",
      "confidence": "wiki+lore"
    },
    {
      "faction_code": "fixer_rogue",
      "stance": "neutral",
      "evidence": "Chippin' In targets Arasaka's Ebunike/Grayson, not Maelstrom; Afterlife is neutral ground [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "fixer_mr_hands",
      "stance": "neutral",
      "evidence": "No Maelstrom-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "afterlife",
      "stance": "neutral",
      "evidence": "Neutral merc marketplace and neutral ground; Maelstrom's own neutral ground is the Totentanz [wiki] [inferred]",
      "confidence": "wiki+inferred"
    }
  ]
}
```
