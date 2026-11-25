# The Mox — Leadership, Internal Politics and External Relations

Status: faction politics research run, 2026-11-25. One faction, one document.
Scope: Cyberpunk 2077 2.5 + Phantom Liberty, campaign disabled. Who a player can
join under, climb past, ally with or remove among the Mox; the internal blocs;
and the external relations matrix needed for wars, alliances and "guarantor"
support when a player founds a gang.

Method: this document follows [`METHOD.md`](./METHOD.md) (the politics playbook,
including its §1.1 and §1.2 corrections) and the evidence rules in
[`../METHOD.md`](../METHOD.md). The location catalog for the Mox is
[`../the-mox.md`](../the-mox.md); this document maps people and politics onto
those places and does not repeat the coordinates.

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/comic/tabletop lore or a writer statement | Tertiary |
| `[inferred]` | My reasoning links a named person, place or stance to a record; reasoning stated | Weak, flagged |

Extra conventions for this document:

- **Presence class** (METHOD §1.2 item 2). `ambient` = persists in free roam
  without a quest; `world-activity` = gig, scanner hustle, side/minor job or
  NCPD activity, i.e. free-roam content but still activity-gated; `story` =
  gated by the main/side job chain; `prologue` = a lifepath intro; `off-map` =
  alive in lore but never spawned; `mentioned` = named only in shards or
  dialogue; `historical` = not present in 2077. The JSON `open_world` flag is
  `true` for `ambient` + `world-activity`, `false` for everything else.
- **"Leader" is not a rank.** The World of Cyberpunk 2077 sourcebook says the
  Mox "did not have strict hierarchy", while the wiki lists Susie Q as
  "Leader" and Anna Nox as a "Mox leader" and warehouse manager. Both are
  true: the Mox are a **loose collective of asset-owners**, not a chain of
  command. In this document "leader" means a person with recognised authority
  over an asset (the club, the warehouse, the studio, the door, the bar), not
  a rank in a ladder.
- **Mox / Moxes.** The singular and the faction name are "Mox"; the plural
  used by the wiki and in-game text is "Moxes".

---

## 1. Leadership and ranks

### 1.1 The 2077 leadership

The Mox are an **establishment faction**, not a turf gang. Their political
centre of gravity is Lizzie's Bar in Kabuki, and their authority is
proprietary: whoever owns or runs an establishment speaks for it. The wiki's
own leadership list has exactly one "Main Leader" (Susie Q), but the member
pages add a second leader (Anna Nox) and several functional leads.

| Name | 2077 role | Character record (entry name → record) | Location / influence point | Presence class | Source | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| **Susanna "Susie Q" Quinn** | Leader of the Mox; owner/operator of Lizzie's Bar; business-first line | registry entry `lizzy_boss` → `Character.q105_lizzies_boss` (inferred identity) | Lizzie's Bar, Kabuki; Susie's office and chair in the nightclub prefab | `story` | Raw `always_loaded_1` community `3789178373769127985`, entry `lizzy_boss`, phases `start`/`end` at `#q105_ws_02_lizzy_boss_start`/`#q105_ws_02_lizzy_boss_end`; the same prefab carries `#q105_susieq_chair`, `#q105_tr_lizzies_susie_nocrowd` and `#q004_dvc_susies_office_door`; wiki *Susanna Quinn*; wiki *Moxes Members* | `[game-data]` `[wiki]` `[inferred]` |
| **Anna Nox** | Mox leader; manager of the Longshore North warehouse; bouncer at Lizzie's; cyberpsychotic in 2077 | registry entry `psycho` → `Character.sts_wat_nid_01_cyberpsycho` (inferred identity) | Autowerks, Longshore North (Northside); Lizzie's Bar before the gig | `world-activity` | Roster site 407 `sts_wat_nid_01`, entry `psycho`, phase `default`, spot `#nid_01_ws_psycho_spawn`; community `{nid_01_com_psycho}` (`10576547466556538143`, 2 Mox); `Gig: Occupational Hazard`, `baseid sts_wat_nid_01`; wiki *Anna Nox* | `[game-data]` `[wiki]` `[inferred]` |
| **Judy Álvarez** | Senior member; braindance editor and techie; de facto leader of the activist wing `[inferred]`; **not** a formal leader | registry entry `judy` → `Character.Judy`; holocall entry `judy_holo` → `Character.Judy` | Lizzie's Bar basement studio; Judy's Apartment, Northside | `story` | Raw `always_loaded_1` community `3864252685526531440`, entry `judy` (phases `default` `#ws_judy_default`, `default_left` `#ws_judy_default_left`, plus `q004`/`q105`/`sq026`/`sq030` phases); community `13782668940352178673`, entry `judy_holo`; wiki *Judy Álvarez*; wiki *Moxes Members* | `[game-data]` `[wiki]` `[inferred]` |
| **Rita Wheeler** | Bouncer and security lead at Lizzie's Bar | registry entry `lizzies_bouncer` → `Character.lizzies_bouncer` (role join, inferred) | Lizzie's Bar front door; the Growl FM stand at night | `ambient` | Raw `always_loaded_1` communities `13241371001841348961` and `8827996557901730299`, entry `lizzies_bouncer` (phase `default` `#ws_lizzies_default_bouncer_quest_01`, plus `q000`/`q004`/`q105` phases); community `656698676211196519`, entry `bouncer`, phase `spawn`, spot `#growl_stand_ws_bouncer`; wiki *Rita Wheeler* | `[game-data]` `[wiki]` `[inferred]` |
| **Mateo Thiago** | Bartender at Lizzie's Bar; information gatekeeper | registry entry `lizzies_barman` → `Character.lizzies_barman` (role join, inferred) | Lizzie's Bar | `ambient` | Raw `always_loaded_1` community `9389127170327817986`, entry `lizzies_barman` (phases `default` `#q004_ws_bartender_def`, `dialogue` `#q004_ws_bartender_dial`, `q105_01_start` `#q105_ws_01_bartender_start`); wiki *Mateo Thiago* | `[game-data]` `[wiki]` `[inferred]` |

**The two identity cautions that matter.**

- **Susie has no named character record.** The record is the generic quest
  actor `Character.q105_lizzies_boss`, entry `lizzy_boss`. The identity is
  proven by the prefab, not by a name: `#q105_susieq_chair`,
  `#q105_tr_lizzies_susie_nocrowd` and `#q004_dvc_susies_office_door` are all
  in the Lizzie's nightclub prefab, and the q105 boss marker
  `q105_01c_sm_lizzies_boss` sits inside the club. Treat the record as
  `[inferred]` and verify in-game before seeding it as an exact actor.
- **Rita and Mateo are role joins, not name joins.** The registry entry names
  are `lizzies_bouncer` and `lizzies_barman`; neither record carries a personal
  name. The roles are unique at Lizzie's, which makes the join strong, but the
  bouncer slot is shared: Anna Nox "can be seen working as a bouncer at
  Lizzie's Bar" before `Occupational Hazard`, and the second ambient bouncer
  entry uses the generic `Character.q004_lizzies_female`. Do not seed Rita as a
  unique actor without an in-game check.

### 1.2 The power base: a club, not a district

The location document (`../the-mox.md`) is the authority on places; this
section only records what the politics needs.

- **HQ / seat:** Lizzie's Bar, Kabuki, Watson. The wiki's organisation infobox
  gives `headquarters = Lizzie's Bar`; the in-game database entry says "The
  gang's main headquarters is Lizzie's Bar"; and `data/faction_headquarters.json`
  already has `hq_the_mox` anchored on the front-entrance marker
  `q000_corpo_mp_lizzies_front_entrance`. `[game-data]` `[wiki]`
- **Economy:** "Most of the Moxes' income was generated by Lizzie's Bar, which
  was an exclusive braindance club." The gang also runs smaller brothels,
  charges protection fees, runs clinics (lore-only; no localized clinic in the
  extract), sells the BITCH V.13 clothing brand and operates the Autowerks
  warehouse/autoshop in Northside. `[wiki]` `[game-data]`
- **Territory:** "Their territory wasn't so much a patch of land as it was a
  profession." The artbook calls the few blocks around Lizzie's "the only
  'turf' they control beyond their dollhouses and clinics." `[wiki]` `[lore]`
- **The seed's only holding:** `kab_creek_loop` / display name "Autowerks",
  `cc_kab_creek_loop` (active, Mox-owned) at the Autowerks site in Northside.
  Its `gamedata_subdistrict` is still `Kabuki`, which is a label conflict, not a
  location claim. The location document's §8.1 described an older "Creek Loop
  Warehouse" anchor 384 m from Lizzie's; the seed has since been retargeted onto
  Autowerks. `[game-data]`
- **Presence proxies:** 20 `areas.jsonl` rows contain Mox entries (15
  Mox-dominant); 46 Mox entries sit in the Lizzie's cluster across ten rows;
  `data/spawn_points.json` has 15 Mox spawn points (9 of them physically at
  Lizzie's); `data/sites/rosters.json` has **3 units at one site** (407,
  Autowerks), and that site is a gig crime scene, not a standing garrison.
  `[game-data]`

That is the political fact the rest of the document builds on: **the Mox's seat
is a business, and their "territory" is a profession.** A leader who loses
Lizzie's loses the faction; a leader who gains a district would be playing a
different game.

### 1.3 Succession history: a founding martyr, no dynasty

There is exactly one documented leadership change in the Mox's history, and it
is the founding itself. Lizzie Borden is the cause of the gang, not a Mox
leader; Susie Q is the first named leader; no source explains how she rose.

| Period | Leader / centre of power | How the position was held |
| --- | --- | --- |
| 2040s–2067 | **Elizabeth "Lizzie" Borden**, owner of the Kabuki strip club | Ex-stripper at Delphi X; ran the club, treated her workers fairly and defended them from violent clients. Not a Mox; the gang did not exist yet. `[wiki]` |
| 13 May 2067 | **Lizzie's death and the riots** | A Tyger Claws gang raped and murdered one of Lizzie's girls; Lizzie killed three of the assailants with an axe and displayed the bodies; the Claws demolished the bar and killed her. The riots that followed founded the Mox. `[wiki]` |
| 2067–2070s | **No named leader** | The gang is described as a mutual-self-defence collective of sex workers, anarchists, punks and sexual minorities, with "no strict hierarchy." `[wiki]` `[lore]` |
| 2077 | **Susanna "Susie Q" Quinn** | Leader and owner/operator of Lizzie's Bar; runs the gang "like a business" and says the protector/activist role is in the past. `[wiki]` |
| 2077 | **Anna Nox** | A second "Mox leader" and manager of the Longshore North warehouse; becomes cyberpsychotic during `Occupational Hazard`. `[wiki]` `[game-data]` |

The pattern is **founding martyr → collective → proprietor-leader**, with no
recorded election, coup, inheritance or appointment. The simulation consequence
is sharp: **removing Susie forces the Mox to invent a succession rule they have
never had.** The plausible claimants are Judy (the activist wing), Rita (the
door/security), Mateo (the bar/information) or a compromise among the club
staff. Anna Nox is not a claimant in 2077; she is a casualty.

### 1.4 Rank structure, initiation and advancement

The Mox have **roles, not ranks**. The wiki's member list gives leader, member,
bouncer, bartender, BD editor, warehouse manager, radio host and enforcer; the
game records add combat archetypes. There is no council, no vote and no
designated deputy.

1. **Leader / owner.** Susie Q, by ownership of Lizzie's Bar. `[wiki]`
2. **Asset managers.** Anna Nox (warehouse), Judy Álvarez (BD studio),
   Rita Wheeler (door/security), Mateo Thiago (bar/hospitality). Their authority
   is functional, not hierarchical. `[wiki]` `[game-data]`
3. **Members.** The `Moxes Members` list: Dollie "Doll" Radcliff, James Morran,
   Evelyn Parker (former), Judy Álvarez, Rita Wheeler, Anna Nox, Mateo Thiago,
   Patty Sonn, Ash. `[wiki]`
4. **Associates and non-members.** Hal Cantos (freelance BD tuner), Lil Bex
   (Mox associate, killed by Anna), Tom Caldera and Roxanne Sumner (Clouds
   dolls, Judy's allies), Maiko Maeda (Tyger associate, Clouds manager, Judy's
   ex), Fingers (ripperdoc who sold Evelyn to the Scavs). `[wiki]` `[game-data]`

**Initiation.** No ceremony is described. Mateo says "gender is not relevant
when joining the Mox" — at least for staffing the bar — and that all one needs
is "knowing how to make drinks or have additional talents." The gang formed
from outcasts and sexual minorities; membership is adoption into the protection
network, not a blood-in. `[wiki]`

**Advancement.** Reputation and asset competence, not seniority. Susie owns the
club, Anna ran a warehouse, Judy runs the studio, Rita runs the door, Mateo runs
the bar. A member who wants to rise must take responsibility for an
establishment or a beat, and that is exactly what makes the faction a
**franchise of assets** rather than a ladder.

**Combat tiers, not ranks.** The 2077 sourcebook names **Mox Cleavers** and
**Mox Inciters** and says they carry weapons pilfered from fallen Tyger Claws.
The record namespace shows the archetypes:
`Character.the_mox_1_ranged1_lexington_wa`,
`Character.the_mox_1_ranged1_pulsar_wa`,
`Character.the_mox_1_melee2_baseball_wa`,
`Character.the_mox_elite2_fmelee2_machete_wa_rare`. These are combat roles, not
authority. `[game-data]` `[wiki]`

**The netrunners are a real capability.** `Gig: Monster Hunt` says "Mox
netrunners connected a few dots and tracked down Jotaro's studio" and that
Kabuki is "a no-go for Moxes which is why they need a helping hand." The Mox
have netrunners; they have no named netrunner record and no netrunning revenue
line. Treat it as an intelligence capability, not a rank. `[wiki]`

### 1.5 What the game actually spawns (campaign disabled)

A wiki infobox is not an actor in free roam. This is the part other systems must
not assume.

**`ambient` — persists in free roam.**
- **Rita Wheeler** at Lizzie's door (`#ws_lizzies_default_bouncer_quest_01`)
  and at the Growl FM stand at night (`#growl_stand_ws_bouncer`). `[game-data]`
- **Mateo Thiago** behind the bar (`#q004_ws_bartender_def`,
  `#q105_ws_01_bartender_start`). `[game-data]`
- The rest of the Lizzie's staff: waitresses, reception, DJ and generic Mox
  crowd entries in `{wat_kab_com_lizzies_default}`. `[game-data]`

**`world-activity` — free-roam but activity-gated.**
- **Anna Nox** at Autowerks in `Gig: Occupational Hazard`
  (`baseid sts_wat_nid_01`). If the mod disables gigs, she drops out. `[game-data]` `[wiki]`

**`story` — gated by the main/side job chain.**
- **Susie Q** in the q105 Lizzie's sequence (`#q105_ws_02_lizzy_boss_start`).
  No `default` phase was found, so she is not an ambient club fixture. `[game-data]`
- **Judy Álvarez** across the main and side jobs (`q004`, `q105`, `sq026`,
  `sq030`). A `default` phase at `#ws_judy_default` exists, so she can persist
  in her apartment after her arc; that is conditional, not a free-roam guarantee.
  `[game-data]`
- **Evelyn Parker** in the main jobs (`q004`, `q105`, `sq026`) and the
  holocall community. She dies in `Double Life`. `[game-data]` `[wiki]`
- **Tom Caldera**, **Roxanne Sumner**, **Maiko Maeda** in the Clouds side jobs
  (`sq026`). Not Mox members (Tom/Roxanne are dolls, Maiko is a Tyger associate).
  `[game-data]` `[wiki]`

**`prologue` — lifepath intro.**
- The Corpo lifepath's Lizzie's scene uses `q000_corpo_*` Mox records: a
  bouncer (`Character.q000_corpo_mox_bouncer`), a guard
  (`Character.q000_corpo_mox`), a waitress (`Character.MoxWaitress`) and
  background Mox. These are prologue-only, not free-roam actors. `[game-data]`

**`off-map` / `mentioned` / `historical`.**
- **Dollie Radcliff** and **James Morran** are book-only members (World of
  Cyberpunk 2077); no records. `[wiki]` `[lore]`
- **Ash** is an unseen radio DJ (89.7 Growl FM); no named actor. `[wiki]`
- **Patty Sonn** appears only in the shard *Archived Conversation: Norris
  Stones and Patty Sonn*; no record. `[wiki]`
- **Lizzie Borden** is historical (died 2067); **Kali** is a 2070s Mox killed by
  Caliber in the comic *XOXO*. `[wiki]` `[lore]`

Caveat: "campaign disabled" is a heuristic. If the mod disables gigs and side
jobs along with the main quest, Anna Nox, Judy and the Clouds cast drop out too.
The `story` rows are the ones to replace with simulation agents, never expect
the game to provide.

### 1.6 Player-path hooks

| Person | Join under | Climb past | Ally with | Remove |
| --- | --- | --- | --- | --- |
| **Susie Q** | The club: bar, door, BD studio, the Lizzie's brand | There is no ladder; climbing past her means taking the club or the leadership | Rita and Mateo (the staff), the NCPD tolerance, the Tyger deal | Removing Susie creates a succession crisis with no rule; the club and its income become the prize |
| **Judy Álvarez** | The protection/activist path: sheltering sex workers, BD work, the Clouds operation | She has no rank to climb; a player under her rises by taking over her personal following, not an office | Rita and Mateo (sympathy), Tom and Roxanne (Clouds dolls), Maiko (a dangerous double agent) | Removing Judy collapses the activist wing; she may leave Night City anyway in her ending |
| **Anna Nox** | The warehouse/BD production path at Autowerks | She is a manager, not a ladder; climbing past her means taking the warehouse | Hal Cantos (freelance tuner), Lil Bex (associate, dead), the Mox subnet | Removing Anna closes a cyberpsycho liability and a public scandal; the warehouse is already a gig crime scene |
| **Rita Wheeler** | The door: security, crowd control, the club's public face | She is a functional lead; climbing past her means taking security | The staff; the club's regulars; Judy's wing by sentiment | Removing Rita leaves the club without its bouncer and its most visible Mox |
| **Mateo Thiago** | The bar: hospitality, information, the club's social hub | He is a functional lead; climbing past him means taking the bar | The staff; customers; anyone who needs gossip | Removing Mateo removes the club's information gatekeeper and its best de-escalator |
| **Maiko / Tom / Roxanne / Hal** | Not membership paths; they are **assets or allies** | — | Maiko: a Tyger channel and a trap. Tom/Roxanne: the Clouds dolls. Hal: a BD tuner | Killing Maiko or Tom closes the Clouds operation; killing Hal closes a BD supplier |

The design consequence: the Mox have **no ladder at all**. A player joins a
**function** (the club, the door, the bar, the studio, the warehouse, the
Jig-Jig beat), and the only way up is to own or take over that function. That is
a different political game from the Valentinos' place-crews or Barghest's
officer corps, and it is the faction's signature.

---

## 2. Internal political factions

### 2.1 The blocs

"Members" counts are **presence proxies** from `areas.jsonl`, the community
registry and site rosters, not membership rolls. The Lizzie's quest communities
are overlapping phases of one site, so do not sum them.

| Bloc | Leader(s) | What it wants | Presence / members hint | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- |
| **Susie Q's business wing** | Susanna "Susie Q" Quinn | Preserve the gang by running Lizzie's as a business; protect only the sex workers who work for the Mox; avoid an open war with the Tyger Claws; keep the NCPD tolerant | Lizzie's Bar staff and income; Susie's office; no formal membership list | Wiki *Moxes Members* ("disillusioned… seeks to run it like a business"); wiki *Susanna Quinn* ("prioritizing the gang's business interests over its history"); the quote "Can't help everyone in this city — gotta take care of our own. Moxes come first." | `[wiki]` |
| **Judy Álvarez's activist wing** | Judy Álvarez | Keep the founding promise to protect vulnerable sex workers; shelter those in need; take the fight to the Tyger Claws at Clouds; avenge Evelyn | Judy's basement BD studio; sympathetic Lizzie's staff; Clouds dolls Tom and Roxanne, and Maiko as a non-member ally; no formal Mox roster | Wiki *Susanna Quinn* (Judy shelters sex workers while Susie complains about the cost); wiki *Judy Álvarez*; Judy's computer messages; side jobs *Ex-Factor*, *Talkin' 'bout a Revolution*, *Pisces* | `[game-data]` `[wiki]` |
| **The Lizzie's floor staff** | Rita Wheeler and Mateo Thiago | Keep the club safe and commercially viable; preserve the old Lizzie's culture; manage customers and information; keep the Tyger Claws at arm's length | Bouncers, bartenders, waitresses, reception and DJ; `{wat_kab_com_lizzies_default}` (54 entries, 16 Mox, 5 6th Street, 5 Valentinos); 46 Mox entries across the Lizzie's area rows | Wiki *Rita Wheeler* (bouncer, bat, sculptures); wiki *Mateo Thiago* (bartender, information cannot be bought, nostalgic for the pre-Tyger era); raw registry entries `lizzies_bouncer`, `lizzies_barman`, `waitress_ground/upstairs` | `[game-data]` `[wiki]` |
| **The Northside braindance and warehouse node** | Anna Nox | Produce and tune braindances; run the Longshore North warehouse; investigate the death of a protected Mox; keep the Mox subnet secure | Site 407 Autowerks: 3 roster units, `{nid_01_com_psycho}` 2 Mox, `{nid_01_com_dead}` 1; Hal Cantos (freelance tuner) and Lil Bex (associate, killed) | Wiki *Anna Nox*; `Gig: Occupational Hazard`; site 407 node names (`#nid_01_ws_lizzie_001`, `#nid_01_ws_psycho_spawn`, `#nid_01_tr_warehouse`); `areas.jsonl` | `[game-data]` `[wiki]` |
| **The Jig-Jig protection beat** | Patty Sonn | Protect the sex workers on Jig-Jig Street; collect the protection fee; punish exploiters and illegal recorders | Jig-Jig ambient Mox (`{cs_goons_cars_com}_047`, 3 Mox); the Little China sex-shop workspots (`#wat_lch_ws_sexshop_01_mox_day/night`); Patty Sonn (shard only); no roster | Shard *Archived Conversation: Norris Stones and Patty Sonn* ("the boys and girls on Jig-Jig do this work because it pays the bills… you're stealing the scop straight off their table"); `data/spawn_points.json` faction 11; wiki *Jig-Jig Street* | `[game-data]` `[wiki]` |
| **The Lizzie Borden legacy** | none (historical figurehead) | Legitimise the gang through the founding martyr; remember May 13; keep the anti-Tyger identity; sell the Mox brand | No 2077 actors; the May 13 anniversary party (Maiko's computer), BITCH V.13, the labrys, the "Moxie" name | Wiki *Elizabeth Borden*; wiki *The Mox*; Maiko Maeda's computer ("Mox is doing a party — it's May 13, anniversary of Lizzy's death and the gang's creation"); wiki *BITCH V.13* | `[wiki]` `[lore]` |
| **Judy's Clouds coalition (non-member)** | Judy Álvarez | Free Clouds from the Tyger Claws; install a doll-run management; avenge Evelyn; neutralize Woodman | Tom Caldera and Roxanne Sumner (Clouds dolls), Maiko Maeda (Tyger manager and double agent), V (mercenary); no Mox members besides Judy | Side jobs *Ex-Factor*, *Talkin' 'bout a Revolution*, *Pisces*; Judy's computer; wiki *Tom Caldera*, *Roxanne Sumner*, *Maiko Maeda* | `[game-data]` `[wiki]` |
| **The protected sex workers and club clientele (non-member base)** | none | Earn a living under Mox protection; keep the club open; avoid Tyger and Scav predation | The Jig-Jig and Little China sex workers; Lizzie's customers (16 Mox, 5 6th Street, 5 Valentinos in the default crowd); the fee payers | Wiki *The Mox* ("demanded substantial fee from their charges"); shard *Patty Sonn*; `areas.jsonl` | `[game-data]` `[wiki]` |

### 2.2 The leader versus the activist

This is the faction's central internal conflict, and it is unusually well
documented for a gang of this size.

- **Susie's position:** "Can't help everyone in this city — gotta take care of
  our own. Moxes come first." She "insists the gang's role as protectors and
  activists is in the past" and "seeks to run it like a business in order to
  preserve themselves." She argues with Judy over Judy offering shelter to sex
  workers in need, complaining about the cost; Judy insists they will pay for
  themselves. `[wiki]`
- **Judy's position:** she joined the Mox "thinking they could improve people's
  life in the city." Her database entry: "Her biggest flaw is that she can't
  keep her mouth shut in the face of injustice — something that always gets her
  in trouble. For some, though, it's her greatest virtue." She runs the Clouds
  operation without Susie's authorization and against Susie's caution. `[wiki]`
- **The split is policy, not personality.** Susie wants **preservation**:
  protect the paying clientele, keep the Tyger deal, keep the NCPD tolerant,
  keep the club open. Judy wants **mission**: protect the vulnerable, punish the
  predators, take the fight to the Tyger Claws. Both are legible responses to
  the same founding story.
- **The evidence that Susie's caution is not irrational** is the Clouds
  operation's outcome. If Judy wins, the Tyger Claws retaliate: Tom Caldera is
  killed, Roxanne Sumner is forced into hiding, and Clouds is closed
  indefinitely. If Maiko wins, working conditions are "just as bad" as under
  Woodman. If V backs Maiko and takes her bribe, Judy leaves Night City; if V
  backs Maiko without the bribe, Judy stays but is disappointed. The activist
  wing is costly, and its victories are fragile. `[wiki]` `[game-data]`

For the simulation this is the cleanest possible internal axis: **business
preservation versus founding mission**, with the club's income and the
protection network as the two things at stake.

### 2.3 The asset-franchise structure

The Mox are not a chain of command; they are a set of **assets with leads**:

| Asset | Lead | What it gives the holder | What it costs |
| --- | --- | --- | --- |
| Lizzie's Bar (club, BD booths, brothel, bar, door) | Susie Q (owner), Rita (door), Mateo (bar), Judy (studio) | The faction's main income, its seat, its public face and its intelligence | Tyger attention, NCPD tolerance, the cost of protection |
| The BD studio in the basement | Judy Álvarez | Braindance production and editing, the Mox's cultural product, a link to the dolls | Judy's independence; Susie owns the building |
| Autowerks warehouse | Anna Nox | BD tuning, vehicle/warehouse logistics, a fortified site | The gig crime scene; Anna's cyberpsychosis; no standing garrison |
| The Jig-Jig beat | Patty Sonn | Protection income, intelligence, the moral claim to protect sex workers | Tyger turf; Wakako's shadow; the risk of a war |
| BITCH V.13 | The Mox brand (no single lead) | Retail margin, recruitment, a visible identity | No premises; sold through cheap stores and street vendors |
| The Lizzie myth | No lead | Legitimacy, recruitment, the anti-Tyger coalition | It constrains any leader who wants to abandon protection |

The political reading: **a bloc's power is its asset, not its rank.** Losing the
club loses the faction; losing the studio loses the culture; losing the door
loses the security; losing the Jig-Jig beat loses the moral claim. That is why
the Mox have no succession rule: there is no office to inherit, only assets to
seize.

### 2.4 The Lizzie Borden legacy

The founding story is the faction's constitution:

- On 13 May 2067 a Tyger Claws gang raped and murdered one of Lizzie's girls.
  Lizzie killed three of the assailants with an axe and displayed the bodies in
  front of her club. The Claws demolished the bar and killed her that same
  night. `[wiki]`
- The riots that followed made Tyger Claws members and businesses the main
  targets. Lizzie's successors rebuilt the bar as "Lizzie's Bar" and founded
  the Mox. `[wiki]`
- The symbols: the **labrys** (double-headed axe) on walls, clothes, tattoos
  and jewellery; the name **Mox** from "moxie"; **BITCH V.13**, whose "V.13"
  is 13 May, the date of Lizzie's death; the **May 13 anniversary party**, which
  Judy calls "our national holiday." `[wiki]` `[lore]`

The legacy is a **legitimacy resource**, not a bloc. A leader who invokes
Lizzie gains standing; a leader who betrays the protection code loses it.
Susie's business line is legitimate only because she still runs Lizzie's;
Judy's activism is legitimate because it invokes Lizzie. The myth is also a
constraint: the Mox cannot openly abandon protection without losing their
identity, and they cannot openly make war without losing their "defensive"
brand.

### 2.5 The Jig-Jig beat and the protection economy

The Mox's protection mandate is not confined to Kabuki. Patty Sonn's shard is
the clearest in-game statement of it:

> "the boys and girls on Jig-Jig do this work because it pays the bills and
> feeds our families… and you're stealing the scop straight off their table…
> shut down your cams, stop selling your recordings of them… You fuck with the
> Mox, the Mox will find you!" — Patty Sonn `[wiki]`

She then kills Norris Stones with a baseball bat, and the shard is found on his
body on a Jig-Jig rooftop. Three things follow:

1. **The protection beat is real and violent.** The Mox enforce their code
   outside Kabuki, on Tyger turf, with a bat.
2. **Protection is also extraction.** The Mox "demanded substantial fee from
   their charges"; the workers pay for the protection. The moral claim and the
   revenue stream are the same relationship.
3. **Jig-Jig is contested ground.** The street's infobox lists Tyger Claws, the
   Mox, Animals and Scavengers; Wakako Okada, a Tyger-affiliated fixer, runs her
   pachinko parlor there. The Mox have a beat, not ownership. `[wiki]`

### 2.6 What could drive internal conflict in a simulation

Evidence-based drivers, in rough order of plausibility:

1. **Business versus mission.** Susie's preservation line versus Judy's
   activism. This is the main policy axis and the faction's signature.
2. **The Clouds operation and its blowback.** Judy's unauthorized raid can
   provoke a Tyger retaliation that kills Tom, forces Roxanne into hiding and
   closes Clouds. The leader who authorized or forbade it owns the outcome.
3. **Succession.** Susie has no designated heir and the Mox have no succession
   rule. Removing her forces the faction to invent one.
4. **Asset ownership.** Who owns the club, the studio, the warehouse and the
   Jig-Jig beat? A bloc's power is its asset, so a transfer of an asset is a
   transfer of political power.
5. **The protection fee.** Extraction versus care. Push the fee too hard and
   the workers stop paying; push too little and the gang cannot fund the club.
6. **The Tyger deal.** Accommodation versus revenge. Susie's caution keeps the
   club open; Judy's raids feel like justice and invite retaliation.
7. **Cyberpsychosis and chrome.** Anna Nox's rampage is the failure state of
   the gang's combat cyberware. A leader who pushes chrome risks another Anna;
   a leader who refuses it risks being unable to defend the club.
8. **NCPD tolerance.** The Mox are the only gang V cannot attack, and Judy's
   NCPD call about Evelyn's suicide is ignored. A raid or a crackdown would
   expose how thin that tolerance is.
9. **Judy's departure.** In her endings Judy can leave Night City. The activist
   wing then loses its leader and the Mox revert to Susie's business line.
10. **The Evelyn trauma.** The Voodoo Boys' attack and the Scavs' abuse of
    Evelyn are personal wounds. A leader who avenges her gains standing; a
    leader who does nothing looks weak.

---

## 3. External relations matrix

### 3.1 Stance vocabulary

One stance per row, chosen by the precedence in `METHOD.md` §3: explicit
violence first, then explicit transaction, then quest-giver role, then
adjacency, then a neutral placeholder. The Mox are a small faction with a
**defensive** doctrine, so most rows are neutral; the exceptions are the
founding enemy, the predators and the one fixer they hired.

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

There is **no usable offline attitude matrix**: `Attitude_Record.hpp` is opaque
and `Affiliation.hpp` is identity only. Every stance below is judged from
quests, shards, the wiki and co-location. The neutral rows are placeholders,
not claims of friendship.

### 3.2 The matrix

| Faction | Code | Stance | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| Tyger Claws | `tyger_claws` | `rival` | 2067: Tyger Claws raped and murdered one of Lizzie Borden's girls; Lizzie killed three of them with an axe; the Claws demolished the bar and killed her, touching off the riots that founded the Mox. The Tyger page adds that a later deal left the Mox alone but "there was always bad blood"; the 2077 artbook calls it a "fierce rivalry." 2077: Mox netrunners locate Jotaro Shobo and hire Regina Jones to take him (*Monster Hunt*); Judy's Clouds operation kills Hiromi Sato and can kill Jun Azegami and Marcus Ichida; on the anti-Maiko branch the Tygers retaliate, kill Tom Caldera and force Roxanne Sumner into hiding (*Pisces*) `[game-data]` `[wiki]` `[lore]` | `game-data+wiki+lore` |
| Valentinos | `valentinos` | `neutral` | Five Valentino-tagged customers in the Lizzie's default crowd (`{wat_kab_com_lizzies_default}`: 16 Mox, 5 Valentinos); no conflict or deal attested `[game-data]` `[inferred]` | `game-data+inferred` |
| Arasaka | `arasaka` | `neutral` | Arasaka agents enter Lizzie's in the Corpo lifepath prologue to confront V (*The Corpo-Rat*); the Mox bouncer admits V but the gang is not a party. Evelyn Parker's Arasaka/Yorinobu affair is personal, not a Mox-Arasaka relationship `[game-data]` `[wiki]` `[inferred]` | `game-data+wiki+inferred` |
| Militech | `militech` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Kang Tao | `kang_tao` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Biotechnica | `biotechnica` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Petrochem | `petrochem` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Barghest | `barghest` | `neutral` | No attested interaction; different district `[inferred]` | `inferred` |
| 6th Street | `sixth_street` | `neutral` | Five 6th Street-tagged customers in the Lizzie's default crowd (`{wat_kab_com_lizzies_default}`: 16 Mox, 5 6th Street); no conflict or deal attested `[game-data]` `[inferred]` | `game-data+inferred` |
| Aldecaldos | `aldecaldos` | `neutral` | No institutional link. Judy can leave Night City with the Aldecaldos in the Star ending (Carol Emeka gives her a ride to the camp), but that is a personal, V-dependent ending, not a Mox-Aldecaldo alliance `[wiki]` `[inferred]` | `wiki+inferred` |
| Wraiths | `wraiths` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Animals | `animals` | `neutral` | Jig-Jig Street lists Animals among the gangs on the street; no Mox-Animal conflict or deal is attested, and the Mox's Jig-Jig presence is a protection beat, not ownership `[wiki]` `[inferred]` | `wiki+inferred` |
| Maelstrom | `maelstrom` | `rival` | 2070s comic *XOXO*: Caliber's crew stole a shard from a Mox convoy; Screw killed the Moxes and fled with Kali; Caliber later shot Kali after Dino failed to vouch for her. The Mox are also a Northside presence next to Maelstrom, and `maelstrom.md` records the pair as `rival` `[wiki]` `[lore]` | `wiki+lore` |
| Voodoo Boys | `voodoo_boys` | `neutral` | The VDB hired Evelyn Parker (a former Mox) to scroll Yorinobu's penthouse, then attacked her with a virus to silence her; Judy and V uncover it and rescue her (*The Space in Between*, *Disasterpiece*, *Double Life*). Evelyn was no longer a Mox and the VDB did not target the gang; `voodoo-boys.md` records the pair as neutral, and this doc keeps that stance, with the grievance in the evidence `[game-data]` `[wiki]` `[inferred]` | `game-data+wiki+inferred` |
| NCPD | `ncpd` | `neutral` | No NCPD raid, scanner hustle or SOCA against the Mox is attested; the Mox are the only gang V cannot attack under normal circumstances, and Judy's NCPD call about Evelyn's suicide is brushed off (*Both Sides, Now*). Tolerance and neglect, not an alliance `[game-data]` `[wiki]` `[inferred]` | `game-data+wiki+inferred` |
| Night Corp | `night_corp` | `neutral` | No attested interaction; a corp, not a turf actor `[inferred]` | `inferred` |
| City Council | `city_council` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Scavengers | `scavengers` | `hostile` | Fingers sold Evelyn to the Scavengers; they held her in an XBD studio at the abandoned power plant and tortured her; Judy and V raid it and kill Scavs (*Disasterpiece*, *Double Life*). The Mox's protection mandate is anti-Scav; Jig-Jig Street also lists Scavengers among its gangs `[game-data]` `[wiki]` | `game-data+wiki` |
| Regina Jones | `fixer_regina` | `client` | Mox netrunners chose Regina Jones as their fixer to hit Jotaro Shobo, because the Mox lacked access in Kabuki (*Monster Hunt*); she also brokers the Autowerks rescue (*Occupational Hazard*). The Mox depend on her brokerage for access they lack `[wiki]` `[game-data]` | `game-data+wiki` |
| Wakako Okada | `fixer_wakako` | `neutral` | Tyger-affiliated fixer and the Jig-Jig broker; Judy and V consult her in *Disasterpiece*, but no Mox-specific deal is attested. The Mox's Jig-Jig beat operates in her shadow `[wiki]` `[inferred]` | `wiki+inferred` |
| Sebastian Ibarra (Padre) | `fixer_padre` | `neutral` | No Mox-specific gig or lore link found `[inferred]` | `inferred` |
| Muamar Reyes (El Capitán) | `fixer_el_capitan` | `neutral` | No Mox-specific gig or lore link found `[inferred]` | `inferred` |
| Dakota Smith | `fixer_dakota` | `neutral` | No Mox-specific gig or lore link found `[inferred]` | `inferred` |
| Dino Dinovic | `fixer_dino` | `hostile` | Comic *XOXO*: Dino (Kali's boyfriend) sold Screw's whereabouts to Maelstrom; Caliber then shot the Mox woman Kali when Dino failed to vouch for her. A historical betrayal that led to a Mox death; no 2077 record, so the current stance is unknown `[wiki]` `[lore]` | `wiki+lore` |
| Rogue Amendiares | `fixer_rogue` | `neutral` | No Mox-specific gig or lore link found; Afterlife is neutral ground `[inferred]` | `inferred` |
| Mr. Hands | `fixer_mr_hands` | `neutral` | No Mox-specific gig or lore link found `[inferred]` | `inferred` |
| Afterlife | `afterlife` | `neutral` | One Mox-tagged background merc in the Afterlife crowd (`Character.q005_afterlife_gang_mox_female`); neutral merc ground `[game-data]` `[inferred]` | `game-data+inferred` |

### 3.3 Actors outside `data/factions.json`

Real relationships with no faction code, so prose only:

- **Elizabeth "Lizzie" Borden** — the founder/martyr, murdered 13 May 2067.
  Not a Mox leader; the gang formed after her death. `[wiki]` `[lore]`
- **Maiko Maeda** — Tyger Claws associate, Clouds' unofficial manager, Judy's
  ex-girlfriend and the double agent in *Pisces*. She offers Judy a way into
  Clouds and then tries to take Clouds for herself under Tyger protection. `[wiki]`
- **Tom Caldera and Roxanne Sumner** — Clouds dolls, not Mox members. Judy's
  allies in the Clouds operation; Tom is killed in the Tyger retaliation, and
  Roxanne goes into hiding. `[wiki]` `[game-data]`
- **Hal Cantos and Lil Bex** — the BD production chain at Autowerks. Hal is a
  freelance tuner and former WNS employee; Lil Bex is the Mox associate who
  contracted him and was the first to die in Anna Nox's rampage. `[wiki]`
- **Norris Stones** — an XBD recorder on Jig-Jig Street who filmed Mox-protected
  workers; Patty Sonn kills him with a baseball bat. `[wiki]`
- **Oswald "Woodman" Forrest, Hiromi Sato, Jun Azegami, Marcus Ichida and
  Jotaro Shobo** — the Tyger Claws antagonists of the Clouds and Jotaro arcs.
  Woodman is the caretaker who raped Evelyn and sold her to the Scavs; Hiromi
  runs Clouds; Jun and Marcus are his bosses; Jotaro is the XBD scroller the
  Mox netrunners hunted. `[wiki]`
- **Finn "Fingers" Gerstatt** — the Jig-Jig ripperdoc who failed to fix Evelyn
  and sold her to the Scavengers. A Scav-adjacent asset, not a faction. `[wiki]`
- **Caliber, Screw and Kali** — the Maelstrom/Mox comic cast. Kali was a Mox;
  Caliber killed her after Dino's betrayal; Screw was sold to the Scavengers. `[wiki]` `[lore]`
- **The protected sex workers and the Lizzie's clientele** — the non-member base.
  They pay the fee, fill the club and justify the gang's existence. They are not
  a faction and have no leader. `[wiki]` `[game-data]`

### 3.4 Guarantor assessment

The design question: if a player founds a gang, which factions would guarantee
the Mox's support, and which would the Mox guarantee?

- **No `ally` row.** The Mox have no faction that would fight for them. Their
  only `client` row is Regina Jones, a fixer who sells access, not a bloc.
- **The Mox are a soft-power guarantor.** They can offer a safe venue
  (Lizzie's), BD production and editing, protection for sex workers, a cultural
  brand and an introduction to the Jig-Jig network. That is genuinely useful to
  a player-founded gang of sex workers, artists or small-time criminals. It is
  also all they have.
- **The Mox are a poor military guarantor.** They have ~200–250 members, threat
  level "Low", no armour, air or heavy weapons, no standing garrison, and one
  roster site that is a gig crime scene. They fight defensively and lose to a
  Tyger retaliation (Tom killed, Roxanne hidden, Clouds closed).
- **Who guarantees the Mox?** Nobody, by treaty. Their security is three
  fragile things: the 2067 deal with the Tyger Claws, NCPD tolerance, and their
  social utility as a protection racket that keeps the peace. All three can be
  withdrawn.
- **A player who takes over the Mox inherits** the Susie/Judy split, the Tyger
  rivalry, the Scav/VDB trauma, the Autowerks liability and a succession crisis
  with no precedent. The faction is a **cause**, not a war machine; a player who
  wants a war should found a different gang, and a player who wants a base
  should take Lizzie's and make peace with the Tygers.

---

## 4. Pillar notes

Design claims from `docs/design/gameplay-systems.md`: the Mox are an
**Ideological Collective** (archetype strength **Culture**, weakness
**Economy**); faction strength **Politics**, weakness **Military**.

| Pillar | Design claim | Lore verdict | Evidence |
| --- | --- | --- | --- |
| Culture (faction strength) | The Mox are a culture, not a business | **Strongly supported, and contested.** The Lizzie martyrdom, the labrys, the May 13 anniversary, BITCH V.13, the "Moxie" name, the punk/fetish aesthetic and the "sex and killing" motto are a real identity. But the culture is split: Susie says the activist role is in the past; Judy says it is the point. Culture is the faction's recruitment engine and its main export. | World of Cyberpunk 2077 quote; wiki *The Mox* philosophy and Behind the Scenes; wiki *Elizabeth Borden*; wiki *BITCH V.13*; Maiko's computer `[wiki]` `[lore]` |
| Politics (faction strength) | The Mox are politically strong | **Supported externally, weak internally.** Externally: the 2067 deal with the Tyger Claws, NCPD tolerance, the ability to hire Regina Jones and the netrunners' reach into Kabuki are real political assets. Internally: no strict hierarchy, no council, no succession rule, and a leader who is disillusioned. Model **strong soft power, brittle institutional authority**. | Tyger Claws page ("reaching a deal… left the Mox alone"); Mox page ("only gang V cannot attack"); *Monster Hunt*; *Susanna Quinn*; *Moxes Members* `[game-data]` `[wiki]` |
| Economy (archetype weakness) | The Mox are economically weak | **Complicates the design.** The lore shows a concentrated but high-margin economy: Lizzie's is the main income, plus brothels, protection fees, clinics (lore-only; no localized clinic in the extract), BITCH V.13 and the Autowerks warehouse. It is not poor; it is **undiversified and politically fragile**: one club, one warehouse, a profession instead of territory, no gambling, drugs, arms or manufacturing. Model **high-margin nightlife income, low resilience**. | Wiki *The Mox* "Source of Income"; wiki *Lizzie's Bar*; location doc §4; `areas.jsonl` `[wiki]` `[game-data]` |
| Military (archetype weakness) | The Mox cannot project force | **Strongly supported.** ~200–250 members, threat level "Low"; bats, clubs and pilfered Tyger weapons; some combat cyberware (optical camo, augmented limbs); bouncers and netrunners; no armour, air or heavy weapons; one roster site / three units at a gig crime scene. On the anti-Maiko branch, the Tyger retaliation after *Pisces* kills Tom and closes Clouds. | World of Cyberpunk 2077; enemy tier list; site 407 roster; *Pisces*; wiki *Anna Nox* `[wiki]` `[game-data]` |
| Overall fit | The pillars fit the faction's identity | **Good for identity, precise for balance.** Keep Culture strong, Politics strong only in the soft-power sense, Economy "rich but concentrated/raidable", Military weak. The Mox are the clearest "culture is the army" faction in the set. | Synthesis `[inferred]` |

Design cautions, not redesigns:

- **Do not model the Mox as a turf gang.** Their power is the club and the
  protection network, not a district. A Mox takeover should paint a building
  and a beat, not a sub-district.
- **Do not model their economy as zero.** Lizzie's is a high-yield point; losing
  it should hurt more than losing a generic block. But the economy has no
  second leg: one club, one warehouse, one brand.
- **Do not model their politics as an institution.** It is a brand, a deal and
  a set of personal relationships. Removing Susie should cost more than
  removing a business, but less than losing the club.
- **The Susie/Judy split is the signature internal mechanic.** Any succession
  system should treat "leader alive but opposed" as a distinct state from
  "leader dead."
- **The vanilla non-hostility is a design decision.** The Mox are the only gang
  V cannot attack under normal circumstances. If the mod lets the player capture
  Mox points, that is a deliberate override, not an accident.

---

## 5. Gaps and uncertainties

### 5.1 Gaps in the politics METHOD

These are improvements for the next agent to fold into
[`METHOD.md`](./METHOD.md), not faction trivia.

1. **P1 — No `structure` or `authority` field.** The Mox have no strict
   hierarchy; the `leaders` array flattens a proprietor, a warehouse manager, a
   BD editor, a bouncer and a bartender into one list. Add `structure` (`strict`,
   `loose`, `collective`, `franchise`) and `authority` (`formal`, `functional`,
   `informal`) per leader. Otherwise a parser cannot tell Susie from Rita.
2. **P2 — No `former_members` / `status` field.** Evelyn Parker is a former Mox
   whose death drives the faction's external relations, and Judy's membership is
   ending-dependent. The schema cannot represent either. Add `former_members` or
   a `status` field (`current`, `former`, `dead`, `dependent`).
3. **P3 — No `non_member_assets` array.** Maiko Maeda, Tom Caldera, Roxanne
   Sumner, Hal Cantos and Regina Jones are central to the Mox's politics but have
   no slot. The worked examples put them in prose; a parser cannot read prose.
   Add `non_member_assets` with `role`, `relation`, `source`.
4. **P4 — Relation scope is undefined.** The Voodoo Boys' attack on Evelyn and
   the Scav raid are mediated through Judy, not ordered by the Mox leadership.
   The METHOD's precedence says a violent event is a relation, but does not say
   whether the event must be **institutional**. Add `scope`
   (`institutional`, `personal`, `historical`) or require the evidence string to
   state it. This doc uses `neutral` for the VDB and `hostile` for the Scavs; a
   stricter institutional rule would make both neutral.
5. **P5 — The stance vocabulary has no `truce` / `non_aggression`.** The 2067
   Tyger deal and the NCPD tolerance are neither `neutral` nor `ally`; `rival`
   captures the bad blood but not the negotiated non-aggression. Add `truce`.
6. **P6 — `patron`/`client` direction is still ambiguous.** The Valentinos
   doc's table defines `client` as "Hires the gang" — the opposite of the
   METHOD's prose ("this faction depends on or works for the other"). The
   Mox–Regina case is a client relationship (the Mox hires the fixer). Add a
   direction arrow (`this faction -> other`) and a worked example.
7. **P7 — Customer/respawn crowds are still used as relation evidence.** The
   Valentinos doc uses the Lizzie's customer crowd to justify `neutral`; this
   doc does the same for 6th Street and Valentinos. The METHOD says presence is
   not a relation. Add a rule: crowds are corroboration only, never the sole
   basis for a stance.
8. **P8 — No `seat` / `power_base` field.** The Mox's leader is the club owner;
   the HQ is the power base. The JSON has no place for "who owns the seat." Add
   `seat` or `power_base` to each leader/bloc.
9. **P9 — No `identity_basis` field.** Susie's record is inferred from prefab
   nodes, Rita's and Mateo's are role joins, and Anna's is a `*_cyberpsycho`
   record. The METHOD says tag `[inferred]`, but a parser cannot see **why**.
   Add `identity_basis` (`name`, `role`, `prefab`, `elimination`) and
   `verify_in_game`.
10. **P10 — No cross-doc consistency check.** The Maelstrom doc records the
    pair as `rival`, the Voodoo Boys doc as `neutral`, and the Valentinos/6th
    Street docs as `neutral`; this doc has to reconcile them. Add the grep step
    from the Barghest doc (M11) to the main METHOD.
11. **P11 — `open_world` is too coarse.** The Mox have an ambient staff, a
    world-activity gig leader and a story-only leader. The bool collapses
    "always there" and "there only during a gig." Add `spawn_gate` or use
    `presence_class` alone.
12. **P12 — No `founders` field.** Lizzie Borden is the founder/martyr, not a
    member or leader; `leaders` cannot represent her. Add `founders` or allow
    `historical` leaders with a `role` note.
13. **P13 — No `record_variants` field.** Judy has `Character.Judy` plus a
    holocall entry; Evelyn has `Character.Evelyn` plus `evelyn_holo`; Anna has
    the dead variant. METHOD §1.1 item 1 says list all variants under one entry,
    but the JSON has one `character_record_id`. Add `record_variants`.
14. **P14 — The location doc and the seed have diverged.** The politics METHOD
    tells the agent to read the location doc, but the seed's Mox sub-territory
    has been retargeted to Autowerks (`display_name = "Autowerks"`, centroid at
    the site) while still labelled `Kabuki`. The politics doc needs a rule to
    re-check the seed against the location doc, or it will repeat stale
    conflicts.
15. **P15 — No `presence_proxy` / `count_source` for member counts.** The Mox
    have 3 roster units and 46 area entries at Lizzie's; the METHOD says not to
    sum overlapping quest communities but gives no alternative. Add a
    `presence_proxy` field or require a prose caveat.

### 5.2 Faction uncertainties

1. **Susie Q has no named actor record.** `Character.q105_lizzies_boss` is a
   generic quest actor; the identity is inferred from `#q105_susieq_chair`,
   `#q105_tr_lizzies_susie_nocrowd` and `#q004_dvc_susies_office_door` in the
   Lizzie's prefab. Verify in-game before seeding her as an exact actor.
2. **Rita Wheeler's actor is unresolved.** Two generic bouncer entries
   (`Character.lizzies_bouncer`, `Character.q004_lizzies_female`) share the
   door, and Anna Nox also worked the door before her gig. Do not seed Rita as a
   unique actor without a check.
3. **Mateo Thiago's actor is a role join.** `Character.lizzies_barman` is the
   only bartender record at Lizzie's, and the wiki says Mateo is the bartender;
   strong, but still a role join, not a name match.
4. **Anna Nox's record is the gig's cyberpsycho.** `Character.sts_wat_nid_01_cyberpsycho`
   is the Anna actor at Autowerks; the pre-gig bouncer is generic. Her "Mox
   leader" title may mean warehouse manager, not co-leader.
5. **There is no documented succession from Lizzie to Susie.** The gap is real,
   not a missing source. Any seat mechanic must be invented.
6. **The 2067 Tyger "deal" is mentioned only on the Tyger page.** Its terms,
   duration and whether the Mox leadership signed it are unknown.
7. **"No strict hierarchy" vs "Leader" is not a contradiction, but the sources
   do not reconcile them.** The sourcebook describes a collective; the wiki
   names a leader. The asset-franchise model is my synthesis, not a quote.
8. **The seed's only holding is Autowerks, labelled Kabuki but physically
   Northside.** `data/sub_territories.json` says `kab_creek_loop` /
   `gamedata_subdistrict = Kabuki`; `data/control_centers.json` has
   `cc_kab_creek_loop` active and Mox-owned at the Autowerks coordinates. The
   Autowerks site itself has `sub_territory_id = 13` (Northside), while the Mox
   CC uses sub-territory 9 (Kabuki), so the CC and the site do not share a
   sub-territory. The location doc's §8.1 described an older "Creek Loop
   Warehouse" anchor 384 m from Lizzie's; that conflict is now stale. Treat the
   label as a seed bug.
9. **The Mox have no standing garrison.** The only roster site is a gig crime
   scene (3 units, one of them the dead variant). Presence is social, not
   military; do not read the roster as an army.
10. **The Voodoo Boys row is neutral despite the Evelyn attack.** If another
    doc or the design wants institutional hostility, align it or flag the
    conflict. The evidence string carries the nuance.
11. **The Scavengers row is hostile based on Judy's raid.** The Mox leadership
    did not order it. If the design wants institutional-only relations,
    downgrade it to `rival` or `neutral`.
12. **The Dino row is hostile based on a comic betrayal.** The Mox's current
    knowledge and stance are unknown; other docs may call Dino neutral. The
    evidence string says "historical."
13. **The Maelstrom row is rival based on a comic.** No game record; the
    `maelstrom.md` row is the source for the Caliber/Kali incident.
14. **`Character.sts_wat_nid_01_lizzie` is not Elizabeth Borden.** It is a
    wounded Mox at the Autowerks warehouse; the record name is a trap. Also,
    `Character.q004_lizzies_female` is a generic Mox actor used for a bouncer
    and a BD "Lizzie solo," not a unique Rita.
15. **`mws_wbr_04` and `mws_wbr_05` are unidentified Mox mini-world-story
    spawners in Westbrook.** They have triggers and `rooftop_access`
    suitability but no entry names or area rows. Do not count them as holdings.
16. **The `Moxes Members` list is the only compact roster.** It includes
    book-only members (Dollie Radcliff, James Morran) and an unseen DJ (Ash); it
    has no member count per clique and no ranks.
17. **The Mox are the only gang V cannot attack.** If the mod lets the player
    capture Mox points, the vanilla non-hostility is overridden. That is a
    deliberate design decision, not a bug.
18. **`open_world` is a heuristic.** If "campaign disabled" suppresses gigs and
    side jobs, Anna Nox, Judy and the Clouds cast drop out. Only Rita and Mateo
    are reliably ambient.
19. **`areas.jsonl` counts are presence proxies.** The 46 Mox entries at
    Lizzie's include quest phases and customer-crowd variants; do not sum them
    as members.
20. **The Mox's culture is contested, not unified.** Susie's business line and
    Judy's activism are both legitimate readings of the founding story. A
    simulation that treats the faction as ideologically monolithic will miss
    the main internal conflict.

### 5.3 Sources consulted

- Local: `data/factions.json`, `data/districts.json`,
  `data/sub_territories.json`, `data/control_centers.json`,
  `data/faction_headquarters.json`, `data/spawn_points.json`,
  `data/sites/{sites,rosters,communities,guards,triggers,spots,patrols,doors,suitabilities}.json`,
  `dist/extract/areas.jsonl`, `dist/extract/markers.jsonl`,
  `dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_{0,1,2}.streamingsector.json`
  (community registry entries, character records, phase names and spot refs;
  Lizzie's prefab node names).
- Wiki: [The Mox](https://cyberpunk.fandom.com/wiki/The_Mox),
  [Moxes Members](https://cyberpunk.fandom.com/wiki/Moxes_Members),
  [Susanna Quinn](https://cyberpunk.fandom.com/wiki/Susanna_Quinn),
  [Judy Álvarez](https://cyberpunk.fandom.com/wiki/Judy_%C3%81lvarez),
  [Elizabeth Borden](https://cyberpunk.fandom.com/wiki/Elizabeth_Borden),
  [Rita Wheeler](https://cyberpunk.fandom.com/wiki/Rita_Wheeler),
  [Mateo Thiago](https://cyberpunk.fandom.com/wiki/Mateo_Thiago),
  [Evelyn Parker](https://cyberpunk.fandom.com/wiki/Evelyn_Parker),
  [Maiko Maeda](https://cyberpunk.fandom.com/wiki/Maiko_Maeda),
  [Oswald Forrest](https://cyberpunk.fandom.com/wiki/Oswald_Forrest),
  [Hiromi Sato](https://cyberpunk.fandom.com/wiki/Hiromi_Sato),
  [Clouds](https://cyberpunk.fandom.com/wiki/Clouds),
  [Lizzie's Bar](https://cyberpunk.fandom.com/wiki/Lizzie%27s_Bar),
  [Jig-Jig Street](https://cyberpunk.fandom.com/wiki/Jig-Jig_Street),
  [Tyger Claws](https://cyberpunk.fandom.com/wiki/Tyger_Claws),
  [Maelstrom](https://cyberpunk.fandom.com/wiki/Maelstrom),
  [Caliber](https://cyberpunk.fandom.com/wiki/Caliber),
  [Anna Nox](https://cyberpunk.fandom.com/wiki/Anna_Nox),
  [Hal Cantos](https://cyberpunk.fandom.com/wiki/Hal_Cantos),
  [Dollie Radcliff](https://cyberpunk.fandom.com/wiki/Dollie_Radcliff),
  [James Morran](https://cyberpunk.fandom.com/wiki/James_Morran),
  [Ash](https://cyberpunk.fandom.com/wiki/Ash),
  [Roxanne Sumner](https://cyberpunk.fandom.com/wiki/Roxanne_Sumner),
  [Tom Caldera](https://cyberpunk.fandom.com/wiki/Tom_Caldera),
  [Regina Jones](https://cyberpunk.fandom.com/wiki/Regina_Jones),
  [Wakako Okada](https://cyberpunk.fandom.com/wiki/Wakako_Okada),
  [Afterlife](https://cyberpunk.fandom.com/wiki/Afterlife),
  [BITCH V.13](https://cyberpunk.fandom.com/wiki/BITCH_V.13).
- Quests and shards: [Both Sides, Now](https://cyberpunk.fandom.com/wiki/Both_Sides,_Now),
  [Ex-Factor](https://cyberpunk.fandom.com/wiki/Ex-Factor),
  [Talkin' 'bout a Revolution](https://cyberpunk.fandom.com/wiki/Talkin%27_%27bout_a_Revolution),
  [Pisces](https://cyberpunk.fandom.com/wiki/Pisces),
  [Pyramid Song](https://cyberpunk.fandom.com/wiki/Pyramid_Song),
  [The Space in Between](https://cyberpunk.fandom.com/wiki/The_Space_in_Between),
  [Automatic Love](https://cyberpunk.fandom.com/wiki/Automatic_Love),
  [Disasterpiece](https://cyberpunk.fandom.com/wiki/Disasterpiece),
  [Double Life](https://cyberpunk.fandom.com/wiki/Double_Life),
  [The Information](https://cyberpunk.fandom.com/wiki/The_Information),
  [The Corpo-Rat](https://cyberpunk.fandom.com/wiki/The_Corpo-Rat),
  [Gig: Occupational Hazard](https://cyberpunk.fandom.com/wiki/Gig:_Occupational_Hazard),
  [Gig: Monster Hunt](https://cyberpunk.fandom.com/wiki/Gig:_Monster_Hunt),
  [Archived Conversation: Norris Stones and Patty Sonn](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Norris_Stones_and_Patty_Sonn),
  [Judy Álvarez/Computers](https://cyberpunk.fandom.com/wiki/Judy_%C3%81lvarez/Computers),
  [Maiko Maeda/Computers](https://cyberpunk.fandom.com/wiki/Maiko_Maeda/Computers).
- Earlier repo research: `docs/research/factions/the-mox.md`,
  `docs/research/factions/METHOD.md`, `docs/research/factions/politics/maelstrom.md`,
  `docs/research/factions/politics/valentinos.md`,
  `docs/research/factions/politics/barghest.md`,
  `docs/research/factions/politics/voodoo-boys.md`,
  `docs/research/factions/politics/sixth-street.md`,
  `docs/design/gameplay-systems.md`.

---

## 6. Machine-readable block

```json
{
  "faction_code": "the_mox",
  "leaders": [
    {
      "name": "Susanna \"Susie Q\" Quinn",
      "role": "Leader of the Mox; owner/operator of Lizzie's Bar; business-first line",
      "character_record_id": "Character.q105_lizzies_boss",
      "location_name": "Lizzie's Bar, Kabuki",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_1 community 3789178373769127985, entry lizzy_boss -> Character.q105_lizzies_boss (phases start/end; spots #q105_ws_02_lizzy_boss_start/#q105_ws_02_lizzy_boss_end); the Lizzie's prefab carries #q105_susieq_chair, #q105_tr_lizzies_susie_nocrowd and #q004_dvc_susies_office_door; wiki Susanna Quinn; wiki Moxes Members; identity inferred from prefab, verify in-game",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "name": "Anna Nox",
      "role": "Mox leader; manager of the Longshore North warehouse; bouncer at Lizzie's; cyberpsychotic in 2077",
      "character_record_id": "Character.sts_wat_nid_01_cyberpsycho",
      "location_name": "Autowerks, Longshore North (Northside) / Lizzie's Bar",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "roster site 407 sts_wat_nid_01, entry psycho -> Character.sts_wat_nid_01_cyberpsycho (phase default; spot #nid_01_ws_psycho_spawn); community {nid_01_com_psycho} 10576547466556538143; Gig: Occupational Hazard baseid sts_wat_nid_01; wiki Anna Nox",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "name": "Judy Álvarez",
      "role": "Senior member; braindance editor and techie; de facto leader of the activist wing (inferred); not a formal leader",
      "character_record_id": "Character.Judy",
      "location_name": "Lizzie's Bar basement / Judy's Apartment, Northside",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_1 community 3864252685526531440, entry judy -> Character.Judy (default #ws_judy_default, default_left #ws_judy_default_left, plus q004/q105/sq026/sq030 phases); community 13782668940352178673 entry judy_holo -> Character.Judy; wiki Judy Álvarez; wiki Moxes Members",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "name": "Rita Wheeler",
      "role": "Bouncer and security lead at Lizzie's Bar",
      "character_record_id": "Character.lizzies_bouncer",
      "location_name": "Lizzie's Bar, Kabuki / Growl FM stand, Coastview",
      "presence_class": "ambient",
      "open_world": true,
      "source": "raw always_loaded_1 communities 13241371001841348961 and 8827996557901730299, entry lizzies_bouncer -> Character.lizzies_bouncer (default #ws_lizzies_default_bouncer_quest_01; q004/q105 phases); community 656698676211196519 entry bouncer -> same record (phase spawn, #growl_stand_ws_bouncer); wiki Rita Wheeler; role join, verify in-game",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "name": "Mateo Thiago",
      "role": "Bartender at Lizzie's Bar; information gatekeeper",
      "character_record_id": "Character.lizzies_barman",
      "location_name": "Lizzie's Bar, Kabuki",
      "presence_class": "ambient",
      "open_world": true,
      "source": "raw always_loaded_1 community 9389127170327817986, entry lizzies_barman -> Character.lizzies_barman (default #q004_ws_bartender_def, dialogue #q004_ws_bartender_dial, q105_01_start #q105_ws_01_bartender_start); wiki Mateo Thiago; role join, verify in-game",
      "confidence": "game-data+wiki+inferred"
    }
  ],
  "internal_factions": [
    {
      "name": "Susie Q's business wing",
      "leader": "Susanna \"Susie Q\" Quinn",
      "goals": "Preserve the gang by running Lizzie's Bar as a business; protect only the sex workers who work for the Mox; avoid an open war with the Tyger Claws; keep the NCPD tolerant",
      "members_hint": "Lizzie's Bar staff and the club's income; Susie's office; no formal membership list",
      "source": "wiki Moxes Members (leader description); wiki Susanna Quinn (prioritises business over activism); wiki The Mox (fee and protection model)",
      "confidence": "wiki"
    },
    {
      "name": "Judy Álvarez's activist wing",
      "leader": "Judy Álvarez",
      "goals": "Keep the founding promise to protect vulnerable sex workers; shelter those in need; take the fight to the Tyger Claws at Clouds; avenge Evelyn",
      "members_hint": "Judy's basement BD studio; sympathetic Lizzie's staff; Clouds dolls Tom Caldera and Roxanne Sumner and Maiko Maeda as non-member allies; no formal Mox roster",
      "source": "wiki Susanna Quinn (Judy shelters sex workers); wiki Judy Álvarez; Judy's computer messages; side jobs Ex-Factor, Talkin' 'bout a Revolution, Pisces",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The Lizzie's floor staff",
      "leader": "Rita Wheeler and Mateo Thiago",
      "goals": "Keep the club safe and commercially viable; preserve the old Lizzie's culture; manage customers and information; keep the Tyger Claws at arm's length",
      "members_hint": "Bouncers, bartenders, waitresses, reception and DJ; {wat_kab_com_lizzies_default} has 54 entries (16 Mox, 5 6th Street, 5 Valentinos); 46 Mox entries across the Lizzie's area rows",
      "source": "wiki Rita Wheeler; wiki Mateo Thiago; raw registry bouncer/barman/waitress entries; areas.jsonl Lizzie's cluster",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The Northside braindance and warehouse node",
      "leader": "Anna Nox",
      "goals": "Produce and tune braindances; run the Longshore North warehouse; investigate the death of a protected Mox; keep the Mox subnet secure",
      "members_hint": "Autowerks site 407: 3 roster units, {nid_01_com_psycho} 2 Mox, {nid_01_com_dead} 1; Hal Cantos (freelance tuner) and Lil Bex (associate, killed)",
      "source": "wiki Anna Nox; Gig: Occupational Hazard; site 407 nodes; areas.jsonl",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The Jig-Jig protection beat",
      "leader": "Patty Sonn",
      "goals": "Protect the sex workers on Jig-Jig Street; collect the protection fee; punish exploiters and illegal recorders",
      "members_hint": "Jig-Jig ambient Mox ({cs_goons_cars_com}_047, 3 Mox); the Little China sex-shop workspots (#wat_lch_ws_sexshop_01_mox_day/night); Patty Sonn (shard only); no roster",
      "source": "shard Archived Conversation: Norris Stones and Patty Sonn; data/spawn_points.json faction 11; areas.jsonl; wiki Jig-Jig Street",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The Lizzie Borden legacy",
      "leader": null,
      "goals": "Legitimise the gang through the founding martyr; remember May 13; keep the anti-Tyger identity; sell the Mox brand",
      "members_hint": "No 2077 actors; the May 13 anniversary party (Maiko's computer), BITCH V.13, the labrys, the 'Moxie' name",
      "source": "wiki Elizabeth Borden; wiki The Mox; Maiko Maeda/Computers ('Mox is doing a party - May 13'); wiki BITCH V.13",
      "confidence": "wiki+lore"
    },
    {
      "name": "Judy's Clouds coalition (non-member)",
      "leader": "Judy Álvarez",
      "goals": "Free Clouds from the Tyger Claws; install a doll-run management; avenge Evelyn; neutralize Woodman",
      "members_hint": "Tom Caldera and Roxanne Sumner (Clouds dolls), Maiko Maeda (Tyger manager and double agent), V (mercenary); no Mox members besides Judy",
      "source": "side jobs Ex-Factor, Talkin' 'bout a Revolution, Pisces; Judy's computer messages; wiki Tom Caldera; wiki Roxanne Sumner; wiki Maiko Maeda",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The protected sex workers and club clientele (non-member base)",
      "leader": null,
      "goals": "Earn a living under Mox protection; keep the club open; avoid Tyger and Scav predation",
      "members_hint": "The Jig-Jig and Little China sex workers; Lizzie's customers (16 Mox, 5 6th Street, 5 Valentinos in the default crowd); the fee payers",
      "source": "wiki The Mox ('substantial fee from their charges'); shard Patty Sonn; areas.jsonl",
      "confidence": "game-data+wiki"
    }
  ],
  "relations": [
    {
      "faction_code": "tyger_claws",
      "stance": "rival",
      "evidence": "2067: Tyger Claws raped and murdered one of Lizzie Borden's girls; Lizzie killed three with an axe; the Claws demolished the bar and killed her, touching off the riots that founded the Mox. The Tyger page adds that a later deal left the Mox alone but there was always bad blood; the 2077 artbook calls it a fierce rivalry. 2077: Mox netrunners locate Jotaro Shobo and hire Regina Jones to take him (Monster Hunt); Judy's Clouds operation kills Hiromi Sato and can kill Jun Azegami and Marcus Ichida; on the anti-Maiko branch the Tygers retaliate, kill Tom Caldera and force Roxanne Sumner into hiding (Pisces) [game-data] [wiki] [lore]",
      "confidence": "game-data+wiki+lore"
    },
    {
      "faction_code": "valentinos",
      "stance": "neutral",
      "evidence": "Five Valentino-tagged customers in the Lizzie's default crowd ({wat_kab_com_lizzies_default}: 16 Mox, 5 Valentinos); no conflict or deal attested [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "arasaka",
      "stance": "neutral",
      "evidence": "Arasaka agents enter Lizzie's in the Corpo lifepath prologue to confront V (The Corpo-Rat); the Mox bouncer admits V but the gang is not a party. Evelyn Parker's Arasaka/Yorinobu affair is personal, not a Mox-Arasaka relationship [game-data] [wiki] [inferred]",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "faction_code": "militech",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
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
      "evidence": "No attested interaction; different district [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "sixth_street",
      "stance": "neutral",
      "evidence": "Five 6th Street-tagged customers in the Lizzie's default crowd ({wat_kab_com_lizzies_default}: 16 Mox, 5 6th Street); no conflict or deal attested [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "aldecaldos",
      "stance": "neutral",
      "evidence": "No institutional link. Judy can leave Night City with the Aldecaldos in the Star ending (Carol Emeka gives her a ride to the camp), but that is a personal, V-dependent ending, not a Mox-Aldecaldo alliance [wiki] [inferred]",
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
      "evidence": "Jig-Jig Street lists Animals among the gangs on the street; no Mox-Animal conflict or deal is attested, and the Mox's Jig-Jig presence is a protection beat, not ownership [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "maelstrom",
      "stance": "rival",
      "evidence": "2070s comic XOXO: Caliber's crew stole a shard from a Mox convoy; Screw killed the Moxes and fled with Kali; Caliber later shot Kali after Dino failed to vouch for her. The Mox are also a Northside presence next to Maelstrom, and maelstrom.md records the pair as rival [wiki] [lore]",
      "confidence": "wiki+lore"
    },
    {
      "faction_code": "voodoo_boys",
      "stance": "neutral",
      "evidence": "The VDB hired Evelyn Parker (a former Mox) to scroll Yorinobu's penthouse, then attacked her with a virus to silence her; Judy and V uncover it and rescue her (The Space in Between, Disasterpiece, Double Life). Evelyn was no longer a Mox and the VDB did not target the gang; voodoo-boys.md records the pair as neutral, and this doc keeps that stance, with the grievance in the evidence [game-data] [wiki] [inferred]",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "faction_code": "ncpd",
      "stance": "neutral",
      "evidence": "No NCPD raid, scanner hustle or SOCA against the Mox is attested; the Mox are the only gang V cannot attack under normal circumstances, and Judy's NCPD call about Evelyn's suicide is brushed off (Both Sides, Now). Tolerance and neglect, not an alliance [game-data] [wiki] [inferred]",
      "confidence": "game-data+wiki+inferred"
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
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "scavengers",
      "stance": "hostile",
      "evidence": "Fingers sold Evelyn to the Scavengers; they held her in an XBD studio at the abandoned power plant and tortured her; Judy and V raid it and kill Scavs (Disasterpiece, Double Life). The Mox's protection mandate is anti-Scav; Jig-Jig Street also lists Scavengers among its gangs [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_regina",
      "stance": "client",
      "evidence": "Mox netrunners chose Regina Jones as their fixer to hit Jotaro Shobo, because the Mox lacked access in Kabuki (Monster Hunt); she also brokers the Autowerks rescue (Occupational Hazard). The Mox depend on her brokerage for access they lack [wiki] [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_wakako",
      "stance": "neutral",
      "evidence": "Tyger-affiliated fixer and the Jig-Jig broker; Judy and V consult her in Disasterpiece, but no Mox-specific deal is attested. The Mox's Jig-Jig beat operates in her shadow [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "fixer_padre",
      "stance": "neutral",
      "evidence": "No Mox-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_el_capitan",
      "stance": "neutral",
      "evidence": "No Mox-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_dakota",
      "stance": "neutral",
      "evidence": "No Mox-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_dino",
      "stance": "hostile",
      "evidence": "Comic XOXO: Dino (Kali's boyfriend) sold Screw's whereabouts to Maelstrom; Caliber then shot the Mox woman Kali when Dino failed to vouch for her. A historical betrayal that led to a Mox death; no 2077 record, so the current stance is unknown [wiki] [lore]",
      "confidence": "wiki+lore"
    },
    {
      "faction_code": "fixer_rogue",
      "stance": "neutral",
      "evidence": "No Mox-specific gig or lore link found; Afterlife is neutral ground [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_mr_hands",
      "stance": "neutral",
      "evidence": "No Mox-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "afterlife",
      "stance": "neutral",
      "evidence": "One Mox-tagged background merc in the Afterlife crowd (Character.q005_afterlife_gang_mox_female); neutral merc ground [game-data] [inferred]",
      "confidence": "game-data+inferred"
    }
  ]
}
```
