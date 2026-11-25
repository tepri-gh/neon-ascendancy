# Biotechnica — Leadership, Internal Politics and External Relations

Status: faction politics research run, 2026-11-25. One faction, one document.
Scope: Cyberpunk 2077 2.5 + Phantom Liberty, campaign disabled, with the mod's
alternate timeline (`docs/design/gameplay-systems.md` §7) applied. Who a player
can join under, climb past, ally with or remove inside Biotechnica; the corporate
blocs; and the external-relations matrix needed for wars, alliances and
"guarantor" support when a player founds an organisation.

Method: this document follows [`METHOD.md`](./METHOD.md), including the §1.1–§1.3
corrections (read first), and the data pitfalls in
[`../METHOD.md`](../METHOD.md) §1.1–§1.2. The location catalogue is
[`../biotechnica.md`](../biotechnica.md); this document maps people and politics
onto those places and does not repeat the coordinates. `AGENTS.md` and the
location doc were read first. No commits, no game launch; helper scripts ran
outside the repo under `python3 -I`.

**The footprint is thin, and that is the finding.** Biotechnica is the largest
biotech company in the world and one of the largest economic actors in Night
City, but the game gives it almost no politics: no 2077 CEO is ever named, no
leader is ambient, and only **two** named employees have character records —
both are gig actors. The faction's political weight in 2077 is carried by
institutions (the CHOOH2 patent, the Petrochem licence, the protein supply) more
than by people. This document says so plainly rather than padding a leader list.

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Position, site, community, roster or raw-registry record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/comic/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My reasoning links a named person, place or stance to a record; reasoning stated | Weak, flagged |

Extra conventions for this document:

- **Presence class** (METHOD §1.2 item 2). `ambient` = persists in free roam
  without a quest; `world-activity` = gig, scanner hustle, side/minor job or
  NCPD activity; `story` = gated by the main/side job chain; `prologue` = a
  lifepath intro; `off-map` = alive or existing in 2077 but never spawned;
  `mentioned` = named only in shards, computers or dialogue; `historical` = not
  present in 2077. The JSON `open_world` flag is `true` only for `ambient` and
  `world-activity`.
- **Corp, not gang.** "Leadership" is an org chart, not a leader list. The
  2077 apex is unnamed; the named people are middle managers and specialists,
  and that asymmetry is itself a political fact (§2.6, §5).
- **The mod's timeline matters.** `docs/design/gameplay-systems.md` §7 removes
  the Konpeki heist and Phantom Liberty's Songbird/Space Force One chain. Two of
  this faction's attested appearances depend on those events: Tina Caruso is
  cited only to *The Heist* background chatter, and the Dogtown agent cell
  exists only inside *Roads to Redemption*, whose prerequisite is *Firestarter*.
  Both are flagged where they appear and in §5.

---

## 1. Leadership and ranks

### 1.1 The 2077 chain of command

Biotechnica is an Italian-founded, Southern-California-headquartered
megacorporation: global HQ **La Jolla, SoCal** (formerly Rome), 36,256 employees
as of 2020, and a Night City **regional HQ** in the Biotechnica Building,
Corporate Plaza. The 2077 corporate hierarchy is documented only down to the
regional director level; the global apex is never named in game, on the wiki, or
in any shard. `[wiki]`

| Name | 2077 role | Character record | Location / influence point | Presence class | Source | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| **The 2077 CEO (unnamed)** | Global chief executive; the wiki's CEO line stops at the 2040s | — (no record, no name) | La Jolla HQ; Rome (former HQ) | `off-map` | Wiki *Biotechnica* (Leadership list: Loggagia 2020s–2040s, then the 2070s entries are a branch head and a regional director) | `[wiki]` |
| **The Board of Directors** | Collective sovereign; sold the CHOOH2 licences in the 1990s | — (no individual records) | Rome / La Jolla; regional board seats | `off-map` | Wiki *Biotechnica* (1991 licence sale, 14 manufacturers); wiki *Petrochem* (licence structure) | `[wiki]` |
| **Tina Caruso** | Head of the West Coast branch, 2070s | — (no record; red link, no page) | West Coast branch → Night City regional HQ | `mentioned` | Wiki *Biotechnica* leadership list, cited to "background dialogue during *The Heist*" | `[wiki]` |
| **Dr. Joanne Koch** | Regional Director for Technology and Development; genetics engineer; head of the Nightingale field programme | `Character.sts_dtn_04_target` (entry `dtn_04_target_s`, phase `default`) | Biotechnica Hotel, floor 19, apartment 193; Badlands field trials | `world-activity` | Roster site 353 `sts_cct_dtn_04` (`faction_id 23`); raw registry entry `dtn_04_target_s`; prefab nodes `#sts_cct_dtn_04_koch_path`, `#sts_cct_dtn_04_koch_bd_editor`, `#dtn_04_ws_joanne_koch_hide`; wiki *Joanne Koch* | `[game-data]` `[wiki]` `[inferred]` |
| **Dr. Diana Cuno** | Genetics engineer; Nightingale co-researcher; scapegoated and killed | — (no record) | North Oak (corpse, Lilac Street); formerly the Nightingale team | `mentioned` | Wiki *Diana Cuno*; shard *Archived Conversation: Diana Cuno and Wakako Okada*; shard *Target for liquidation* | `[wiki]` |
| **Alex (Aleksander) Pushkin** | Senior Quality Control Assistant; Nightingale field-team member | `Character.sts_wbr_jpn_01_alex` (entry `alex`, phase `0_default`) | A car trunk in the Tyger Claws garage on Redwood St., Japantown | `world-activity` | Roster site 418 `sts_wbr_jpn_01` (`faction_id 23`, 1 unit); raw registry entry `alex`; wiki *Gig: Olive Branch*; wiki *Joanne Koch* (notes) | `[game-data]` `[wiki]` |
| **Emilia Morton** | Corp staff; framed by Koch, fired, then killed | — (no record) | Corpo Plaza (corpse); former Biotechnica employee | `mentioned` | Wiki *Emilia Morton*; shards *Archived Conversation: Emilia Morton and Joanne Koch*, *Archived Conversation: SERGEANT #1919 and Joanne Koch* | `[wiki]` |
| **Emilia Weiss** | Biotechnica employee handling the new Badlands research centre's missing parts shipment; negotiates with Saul Bright | — (no record) | Rocky Ridge, northern Badlands (corpse) | `mentioned` | Shard *Archived Conversation: Saul Bright and Emilia Weiss*; wiki *Biotechnica* (Saul negotiation) | `[wiki]` |
| **Brandon Murphy** | Soldier; Nightingale sample collection; lost an arm to the test subjects | — (no record) | Formerly the Nightingale site; last seen leaving the corp | `mentioned` | Wiki *List of Biotechnica employees*; shard *Archived Conversation: Brandon Murphy and Dave Arbus*; shard *Notes (Downtown)* | `[wiki]` |
| **Linda Sherman** | Biotechnica intelligence operative; runs the Dogtown pursuit of Nele Springer | — (no record; red link) | Dogtown; the Nighthawks Rehabilitation Center operation | `mentioned` | Shard *Archived Conversation: Linda Sherman and Miriam Levy*; wiki *Biotechnica* (*Roads to Redemption*); shard *The Crimson Harvest: Freedom Fighters or Terrorists?* (found on "the Biotechnica agent") | `[wiki]` |
| **Dr. Isaacson** | R&D physician; performed the Nightingale autopsies | — (no record) | Nightingale programme | `mentioned` | Computer message *Joanne Koch/Computers*, "Nightingale [WORK IN PROGRESS]" | `[wiki]` |
| **Biotechnica Sergeant #1919** | Security dispatcher; receives Koch's kill order | — (callsign only, no record) | Downtown / hotel security net | `mentioned` | Shard *Archived Conversation: SERGEANT #1919 and Joanne Koch* | `[wiki]` |
| **James Scherer** | Researcher, German branch; implant/organic-muscle programme | — (no record) | German branch | `off-map` | Netpage *Biotechnica/Netpage*, news item "New implant type!" | `[wiki]` |
| **Nicolo Loggagia** | CEO, 2020s–2040s; biochemist; the company's builder | — (no 2077 record) | Monte-Carlo; Rome HQ | `historical` | Wiki *Nicolo Loggagia* (alive as of 2045); wiki *Biotechnica* leadership list | `[wiki]` `[lore]` |
| **Epione Song** | Division manager, Night City branch, 2045; Home and Garden division | — (no 2077 record) | Biotechnica Campus, University District (2045) | `historical` | Wiki *Biotechnica Campus* | `[wiki]` `[lore]` |
| **Annabel Cruz** | Junior engineer, bioweapons black site (Columbia-1/2), RED era | — (no 2077 record) | Biotechnica black site | `historical` | Wiki *List of Biotechnica employees* (Cyberpunk RED table) | `[wiki]` `[lore]` |
| **Francis Young** | Cloning scientist; first self-aware clone (2020) | — (no 2077 record) | Night City cloning station | `historical` | Wiki *Biotechnica* (2000s history) | `[wiki]` `[lore]` |

Notes:

- **The apex is a hole, not a person.** The wiki's Leadership section names
  Loggagia (2020s–2040s), Caruso (2070s branch head) and Koch (2070s regional
  director). No 2077 CEO, chair or board member is named anywhere. Treat the
  board as a collective and the CEO as `off-map` with `character_record_id:
  null`; do not invent a name. `[wiki]` `[inferred]`
- **Caruso outranks Koch, and the relationship is inferred.** "Head of the West
  Coast branch" is a line role above "Regional Director for Technology and
  Development"; the Night City Building is the regional HQ under that branch.
  The game never shows them together, and Caruso has no page. `[wiki]`
  `[inferred]`
- **Koch's record is generic.** `Character.sts_dtn_04_target` is the gig's
  target-elimination actor, not a person-named record. The identity is proven by
  the prefab itself: the street-story path, the hide workspot and the BD editor
  all carry `joanne_koch`, and the wiki's `baseid` `sts_cct_dtn_04` is site 353's
  code. Tagged `[inferred]` for the record join, `[game-data]` for the place.
- **Pushkin is the only named employee in a roster.** His record is `alex`, not
  `pushkin`; the identity comes from the wiki (`baseid sts_wbr_jpn_01`) and the
  fact that he is the only faction-23 unit at that site. `[game-data]` `[wiki]`
  `[inferred]`
- **`Character.sts_ep1_07_agent_01`–`04`** are the Dogtown Biotechnica agents in
  *Roads to Redemption*. They are unnamed, and they are **not** in
  `data/sites/rosters.json`; the only local evidence is
  `areas.jsonl` `{sts_ep1_07_agents}` (4 Biotechnica entries, dominant). Treat
  them as a generic field team, not named leadership. `[game-data]` `[wiki]`

### 1.2 The Night City / West Coast branch

The Night City structure is the only part of Biotechnica the game builds at all.
It is also the only part where the 2077 internal politics happen.

| Layer | Who / what | Evidence |
| --- | --- | --- |
| Global HQ | La Jolla, SoCal (formerly Rome) | Wiki *Biotechnica* infobox and history `[wiki]` |
| West Coast branch | **Tina Caruso**, Head of the West Coast branch (2070s) | Wiki *Biotechnica* leadership list `[wiki]` |
| Night City regional HQ | **Biotechnica Building**, Corporate Plaza; skybridge to Wellsprings. No local record, no coordinate, no interior in the extract | Wiki *Biotechnica Building*; location doc §8.6 `[wiki]` `[game-data]` |
| Regional function | **Dr. Joanne Koch**, Regional Director for Technology and Development; genetics engineer | Wiki *Joanne Koch*; `Character.sts_dtn_04_target` `[game-data]` `[wiki]` |
| R&D / field programme | Nightingale team: Koch, Cuno, Pushkin, Isaacson, Murphy; **Emilia Weiss** on Badlands logistics | Shards and wiki `[wiki]` |
| Security / intelligence | Hotel security (12 guards, 1 officer, 9 droids), "Biotechnica's intelligence agency", **Linda Sherman**, **Sergeant #1919** | Roster site 353; shards `[game-data]` `[wiki]` |
| Staff housing | **Biotechnica Hotel**, Republic Way, Downtown; employees only; lobby, floor 19 (apartments 191–194, security room), roof AV pad | Site 353; wiki *Biotechnica Hotel* `[game-data]` `[wiki]` |
| Subsidiary | **All Foods** (Mexico City HQ; Night City office on Eisenhower St.; Northside factory lost to Maelstrom) | Wiki *All Foods*; wiki *All Foods Factory* `[wiki]` `[game-data]` |

The branch is a **functional** bureaucracy, not a dynastic court. The Building is
where the regional HQ and the CHOOH2/database records live; the Hotel is where
the staff sleep and where the regional director keeps an apartment; the Badlands
R&D facility is where the science happens; the All Foods subsidiary handles the
food business. Each function has its own chain, and the game shows only the two
ends: the lab director and the security guards. `[inferred]`

**The Building has no interior in the extract.** No marker, site, community,
mappin or prefab; the wiki gives only "Corporate Plaza, accessed by a bridge from
Memorial Park". A regional HQ this important with zero local geometry is a
structural gap, not a research failure (location doc §8.6). For politics it means
the apex has no stage: the only Biotechnica interiors a player can enter are the
Hotel and the All Foods plant. `[wiki]` `[game-data]`

### 1.3 Succession history

| Period | Leader | How the change happened |
| --- | --- | --- |
| 1991–2020s | **The founding board / early management** | Biotechnica is a small Rome company with one office; it invents CHOOH2 in 1991, sells the exclusive licence to Petrochem because it cannot meet demand, then the board licenses 14 more manufacturers. The company becomes a megacorp on royalties. `[wiki]` |
| 2020s–2040s | **Nicolo Loggagia** | Brilliant, erratic biochemist; builds the company into the world's largest biotech firm; pursues biosphere restoration; leaves the business side to his grandson Mario and Mario's wife Luchessia. Alive as of 2045. `[wiki]` `[lore]` |
| 2040s | **Division managers** (e.g. **Epione Song**, Night City) | The company is large enough to run by divisions (Home and Garden, cloning, cyberpets). The wiki notes Biotechnica promotes science and engineering graduates into management, not business majors. `[wiki]` `[lore]` |
| 2050s–2070s | **Unnamed executives** | New regional HQ in Corporate Plaza (2052); Pacifica Venture Center investment abandoned after the Unification War; the food-production expansion (the Flats, and the All Foods acquisition at some point). No leader is named for this entire period. `[wiki]` |
| 2070s | **Tina Caruso** (West Coast branch) → **Dr. Joanne Koch** (regional technology and development) | The only 2070s names. Caruso is attested once, in background dialogue; Koch is the operational face of the Night City branch. `[wiki]` `[game-data]` |
| 2077 | **Unnamed CEO** | No name, no record, no scene. `[wiki]` `[inferred]` |

The pattern is **managerial, not dynastic and not political**: a founder-scientist
era, then an institutional era with no visible sovereign. Unlike Arasaka
(dynastic murder) and Militech (board/state/electoral succession), Biotechnica
has no documented succession event at all — only a silence where the top should
be. That silence is the most important fact for a simulation: the mod must either
invent the apex or model the company as a board/committee with no single leader.
`[wiki]` `[inferred]`

### 1.4 Rank structure, entry and advancement

There is **no lifepath and no prologue** for Biotechnica. The Corpo lifepath
(`q000_corpo_*`) is Arasaka's; the Nomad lifepath drives *through* the Biotechnica
Flats as scenery but has no Biotechnica actor (the pursuers are Arasaka). The
ladder below is reconstructed from rosters, shards, the 2045 campus page and the
2077 netpage. `[game-data]` `[wiki]`

**Corporate ladder.**

1. **Board and CEO.** Global; unnamed in 2077. Owns the patents and the licence
   strategy. `[wiki]`
2. **Branch head / regional director.** Caruso (West Coast branch) and Koch
   (regional technology and development). The branch head is a line role; Koch's
   is a functional directorate. `[wiki]`
3. **Division / department manager.** Epione Song ran the 2045 Night City branch
   and the Home and Garden division; the 2077 equivalents are unnamed. `[wiki]`
   `[lore]`
4. **Technical specialist.** Genetics engineer (Cuno), Senior Quality Control
   Assistant (Pushkin), cloning technician (Hugh Hunter, 2045), medtech,
   researcher. This is the company's core career track. `[wiki]`
5. **Corporate staff.** "Corp" (Morton), receptionist, secretary, analyst; the
   hotel's receptionist and maid are the 2077 examples. `[game-data]` `[wiki]`
6. **Contract labour, manual workers and test subjects.** The netpage advertises
   "manual workers" for the remote Badlands R&D facility with free room, board
   and healthcare, and separately seeks drug-test volunteers whose "compensation
   does not cover insurance". This is the bottom of the ladder and the source of
   the corp's human cost. `[wiki]`

**Security ladder.**

1. **Guard.** `Character.sts_dtn_04_security` (12 at the hotel); the public face
   of the company. `[game-data]`
2. **Security officer.** `Character.sts_dtn_04_security_officer` (1); runs the
   floor/guard areas. `[game-data]`
3. **Sergeant / dispatcher.** "Biotechnica Sergeant #1919", a callsign on the
   security net, receives kill orders directly from the regional director.
   `[wiki]`
4. **Agent / operative.** The Dogtown field agents (`sts_ep1_07_agent_01`–`04`)
   and **Linda Sherman**, who runs an off-books pursuit and contracts a merc to
   kill a witness. `[game-data]` `[wiki]`
5. **Droids.** `Character.sts_dtn_04_security_droids` (9 at the hotel) are
   machines, not a garrison (METHOD §1.1 item 4). `[game-data]`

**Entry and advancement.**

- **The netpage is the recruiting station.** Public advertisements for "manual
  workers" at the Badlands facility, "testers wanted" for a cold-cure drug, and
  "partners in research" for licensed findings. The pitch is free room and board,
  free healthcare, competitive salary — the classic remote-company lure.
  `[wiki]`
- **The corp is a good employer on paper and a ruthless one in practice.** The
  *Big 5 Employers in Night City – 2077* shard ranks Biotechnica third, and its
  selling point is "up to six (yes, six!) paid vacation days a year"; the wiki
  repeats the six days. The same corp runs NDAs, reads employee email during a
  leak investigation, and scapegoats a scientist to a hit list. `[wiki]`
  `[game-data]`
- **Advancement is scientific output plus internal politics.** The 2045 campus
  note is explicit: Biotechnica promotes people with science and engineering
  degrees into management, not business majors, which produces brilliant
  managers with no socialisation training. In 2077 the same culture appears as
  Koch's method: plant forged papers on a rival, order her killed, and pin a
  mass-casualty trial on a subordinate when it leaks. `[wiki]` `[lore]`
- **Loyalty is enforced by NDA and surveillance, not by an academy or an oath.**
  There is no Biotechnica Academy, no loyalty pledge, no uniform culture. The
  controls are the NDA Koch invokes in her Nightingale memo, the email audit in
  the Murphy shard, and the kill orders. `[wiki]`

**Practical consequence for the mod:** a player joining Biotechnica should enter
as a **lab technician, a manual worker at the Badlands facility, or a hotel
security guard**, not as a Corpo. The science ladder (technician → specialist →
division manager → regional director) is the real career; the security ladder
(guard → officer → sergeant → agent) is the parallel one. The failure states are
whistleblowing and scapegoating, not demotion: Morton is fired and killed, Cuno
is blamed and killed, Murphy loses an arm and walks. `[inferred]`

### 1.5 Named members mapped to game data

`data/sites/rosters.json` contains **25 Biotechnica units across 2 sites**, of
which **9 are droids**. Of the 16 humans, exactly **two are named people**: Koch
(`Character.sts_dtn_04_target`, at site 353) and Pushkin
(`Character.sts_wbr_jpn_01_alex`, at site 418). Every other named person in this
document is shard-, computer- or wiki-only. `[game-data]`

| Name | Role / note | Character record | Community / marker | Location | Presence class | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| Joanne Koch | Regional Director, tech & development; Nightingale lead | `Character.sts_dtn_04_target` | site 353 `sts_cct_dtn_04`, phase `default`; `#dtn_04_tr_target`, `#dtn_04_tr_find_joanne_koch` | Biotechnica Hotel, floor 19 | `world-activity` | `[game-data]` `[wiki]` `[inferred]` |
| Alex Pushkin | Senior Quality Control Assistant; Nightingale field team | `Character.sts_wbr_jpn_01_alex` | site 418 `sts_wbr_jpn_01`, entry `alex`, phase `0_default`; `{jpn_01_com_alex}` | Tyger Claws garage, Redwood St. | `world-activity` | `[game-data]` `[wiki]` `[inferred]` |
| Tina Caruso | Head of West Coast branch | — | — | West Coast / Night City | `mentioned` | `[wiki]` |
| Diana Cuno | Genetics engineer; scapegoat | — | corpse scene, North Oak | Lilac St., North Oak | `mentioned` | `[wiki]` |
| Emilia Morton | Corp; framed and killed | — | corpse scene, Corpo Plaza | Senate Ave., Downtown | `mentioned` | `[wiki]` |
| Emilia Weiss | Badlands research logistics | — | shard scene, Rocky Ridge | Rocky Ridge | `mentioned` | `[wiki]` |
| Brandon Murphy | Soldier; Nightingale samples | — | shard, Rocky Ridge | Rocky Ridge | `mentioned` | `[wiki]` |
| Linda Sherman | Intelligence operative | — | shard, Dogtown | Dogtown | `mentioned` | `[wiki]` |
| Dr. Isaacson | R&D autopsy physician | — | Koch's computer | Hotel | `mentioned` | `[wiki]` |
| Sergeant #1919 | Security dispatcher | — | shard, Downtown | Downtown | `mentioned` | `[wiki]` |
| James Scherer | German branch researcher | — | netpage | Germany | `off-map` | `[wiki]` |
| Nicolo Loggagia | CEO 2020s–2040s | — | — | Rome / Monte-Carlo | `historical` | `[wiki]` `[lore]` |
| Epione Song | 2045 Night City division manager | — | — | University District (2045) | `historical` | `[wiki]` `[lore]` |

Presence ledgers, so the thinness is quantified rather than asserted:

| Signal | Result |
| --- | --- |
| Roster sites / units | 2 sites / 25 units: site 353 (24 units: 12 guards, 9 droids, 1 receptionist, 1 officer, 1 target), site 418 (1 unit: Pushkin) `[game-data]` |
| Community areas | 5: hotel 3 (`{dtn_04_com_area}` 18, `{dtn_04_com_area_after_alarm}` 5, `{dtn_04_com_npc}` 1), Dogtown agents 4, Japantown 1 `[game-data]` |
| Owned sub-territories | 2: `dtn_central_concourse` (renamed "Biotechnica Hotel", sub 75, active CC), `bls_biotechnica_flats` (sub 88, inactive CC) `[game-data]` |
| Biotechnica units in the Badlands | **0**; the Flats is ownership without a garrison `[game-data]` |
| Named people with records | 2 (Koch, Pushkin); both gig actors `[game-data]` |
| Ambient named leaders | **0** `[game-data]` |

### 1.6 What the game actually spawns (campaign disabled)

A wiki infobox does not mean an actor in free roam. This is the part a simulation
must not assume.

**`ambient` — persists in free roam, no quest required.**

- Generic Biotechnica security (12 guards, 1 officer) and 9 droids at the
  Biotechnica Hotel; the hotel is the only faction-23 site staffed by its own guards.
  `[game-data]`
- **No named person.** There is no ambient Biotechnica manager, executive or
  scientist anywhere. `[game-data]`

**`world-activity` — free-roam content, activity-gated.**

- **Dr. Joanne Koch** — *Gig: Guinea Pigs* (`baseid sts_cct_dtn_04`, site 353).
  `world-activity` by METHOD §2.5 (a gig with a `baseid`), not `story`: her
  record is phase `default` and the site is a `fixer_gig`. She does not walk the
  city; she exists in the gig. `[game-data]` `[wiki]`
- **Alex Pushkin** — *Gig: Olive Branch* (`baseid sts_wbr_jpn_01`, site 418). He
  is in a car trunk; his only scene is the gig. `[game-data]` `[wiki]`
- **The unnamed Dogtown agent team** — *Gig: Roads to Redemption*
  (`baseid sts_ep1_07`); 4 Biotechnica entries in `{sts_ep1_07_agents}`, records
  `Character.sts_ep1_07_agent_01`–`04`. `[game-data]` `[wiki]`

**`mentioned` — named only in shards, computers or dialogue.**

- Caruso, Cuno, Morton, Weiss, Murphy, Sherman, Isaacson, Sergeant #1919. None
  has a character record; none can be met. `[wiki]`

**`off-map` / `historical` — alive or existing in the setting, not in 2077.**

- The 2077 CEO and board (`off-map`); Scherer (`off-map`); Loggagia, Song, Cruz,
  Young (`historical`). `[wiki]`

**The finding.** **No named Biotechnica leader is ambient.** The highest-ranking
named person a player can meet in the game is Dr. Joanne Koch, a regional
director — and only as a gig target. The next is a Senior Quality Control
Assistant in a car trunk. Everything above them (branch head, CEO, board) is
`mentioned` or `off-map`. With the campaign disabled the game provides hotel
guards and droids, not leadership; the mod must spawn the leadership it wants.
`[game-data]` `[inferred]`

Caveat: "campaign disabled" may also suppress gigs and hustles. The
`world-activity` rows are the best reuse candidates, but they need an in-game
spawn check. In the mod's timeline, *Roads to Redemption* is downstream of
*Firestarter*, a Phantom Liberty main job that §7 removes; the Dogtown agent cell
should be treated as **unavailable unless the mod re-enables that gig**.
`[inferred]`

### 1.7 Player-path hooks

| Person | Join under | Climb past | Ally with | Remove |
| --- | --- | --- | --- | --- |
| **The 2077 CEO / board** | The licence establishment: CHOOH2 royalties, Petrochem diplomacy, quiet money | There is no visible ladder to the apex; the branch head is the ceiling the game documents | Petrochem, the board, the licence licensees | No actor to remove. A coup must be built as fiction, not played against an NPC |
| **Tina Caruso** | The West Coast branch: regional administration, the Building, staff housing | The global executive tier is `off-map`; she is the top named line manager | The branch staff, the board, the hotel | No record, no scene; she can only be removed in simulation |
| **Dr. Joanne Koch** | The R&D / field-science wing: Nightingale, field trials, "results at any cost" | Cuno and Pushkin are her peers/subordinates; Caruso is above her; the security apparatus is her instrument | The security apparatus, Sergeant #1919, the Badlands team | *Guinea Pigs*: kill her in the apartment or deliver her to the Red Ocher |
| **Dr. Diana Cuno** | The science ladder's cautionary rung: competent, complicit, expendable | She has already been climbed past; her only move is flight | Wakako (refused), no one else | She is killed by Arasaka goons before the player can act |
| **Alex Pushkin** | The technical staff rung: quality control, field sampling | No ladder; he is a captive | The Tyger Claws (if delivered) or V (if freed) | Free him, deliver him, or kill him in *Olive Branch* |
| **Emilia Morton** | The corporate-staff rung: the employee who learns too much | No ladder; she is already purged | N54, the reporter Mendoza (too late) | She is killed by Animals before the player arrives |
| **Emilia Weiss** | Badlands research logistics: cargo, contractors, discretion | No ladder shown; she is a field fixer for the R&D wing | Saul Bright / the Aldecaldos (one job, no alliance) | She is already dead at the Rocky Ridge scene |
| **Linda Sherman** | The intelligence wing: surveillance, witness elimination, deniable contracts | The unnamed intelligence chief is above her; the branch head above that | Miriam Levy and the hired mercs | No record, no scene; simulation-only |
| **Hotel security officer / guards** | The security ladder: lobby, floor 19, roof | Sergeant, then agent, then the intelligence wing | The hotel staff; the droids | Capture the hotel; the gig puts the player against them |

The design consequence: Biotechnica has **two ladders and no apex**. A player can
join the science track (technician → specialist → director) or the security track
(guard → officer → sergeant → agent), but the top is unoccupied in the game and
must be invented. The most playable political story is not a succession: it is a
**cover-up** — a director, a scapegoat, a whistleblower, and a security
apparatus that kills all three. That is the story the shards already tell.
`[inferred]`

---

## 2. Internal political factions

### 2.1 The blocs

"Members" counts are **presence proxies**, not membership rolls. The hotel
communities are overlapping variants of one site and must not be summed.

| Bloc | Leader(s) | What it wants | Presence / members hint | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- |
| **The licence establishment (CHOOH2 / FrostCorn royalties)** | The board and the unnamed CEO | Protect the patents; keep the licence revenue flowing; keep Petrochem cordial; stay out of the news | No named 2077 actor; 14 other licensees plus Petrochem (60% of world supply); FrostCorn licences to governments | Wiki *Biotechnica* (1991 licence sale, royalties funded food expansion); wiki *Petrochem* (licence structure, "strongest ally") | `[wiki]` |
| **The West Coast / Night City branch** | **Tina Caruso** (branch head); **Joanne Koch** (regional technology and development) | Run the regional HQ, the staff hotel and the local business; keep the branch clean enough to function | Caruso `mentioned`; Koch `world-activity`; Building (no interior), Hotel (24 units) | Wiki *Biotechnica* leadership; wiki *Biotechnica Hotel*; roster site 353 | `[game-data]` `[wiki]` |
| **The R&D / field-science wing (Nightingale)** | **Dr. Joanne Koch**; **Dr. Diana Cuno**; **Alex Pushkin**; **Dr. Isaacson**; **Brandon Murphy**; **Emilia Weiss** (logistics) | Breakthroughs at any cost: field trials on nomads, immunosuppressants, cloning, new species; conceal the side effects | Koch (record), Pushkin (record), four `mentioned` specialists; the Badlands R&D facility is "the most expensive investment in the corporation's history" | Wiki *Project Nightingale*, *Joanne Koch*, *Diana Cuno*; shards; netpage "Come work in the Badlands" | `[game-data]` `[wiki]` |
| **The security and intelligence apparatus** | Unnamed intelligence chief; **Sergeant #1919**; hotel security officer | Protect the corp's property and reputation; surveil employees; eliminate leaks; use deniable contractors | 12 guards, 9 droids, 1 officer at the hotel; "Biotechnica's intelligence agency"; Linda Sherman's Dogtown operation | Roster site 353; shards *SERGEANT #1919*, *Linda Sherman*, *Target for liquidation*; wiki *Sasha Yakovleva* | `[game-data]` `[wiki]` |
| **The All Foods commercial wing** | Unnamed subsidiary management | Market share in synthetic food; retail expansion; local political influence; keep the brand clean | All Foods HQ Mexico City; Night City office on Eisenhower St.; the Northside factory (lost) | Wiki *All Foods*, *All Foods Factory*; shard *All Foods – Eat What You Know* | `[wiki]` |
| **The European / founder-science old guard** | **Nicolo Loggagia** (historical); **James Scherer** (German branch); **Annabel Cruz** (RED-era bioweapons) | Biosphere restoration, pure research, new species — the company Loggagia built, not the 2070s food-and-licence business | Rome, Berlin, Paris, London, Bonn; the 2076 Paris lab attack | Wiki *Nicolo Loggagia*, *Biotechnica Campus*, *Crimson Harvest*; netpage | `[wiki]` `[lore]` |
| **The NDA-bound workforce** | No leader | Survive the audit, keep the job, avoid becoming the scapegoat | Receptionist, maid, "Corp" staff, manual workers, test volunteers; 6 vacation days; third-best employer | *Big 5 Employers* shard; netpage careers; shards *Murphy/Arbus*, *Morton/Koch* | `[game-data]` `[wiki]` |

### 2.2 The Nightingale scapegoat chain

This is the only Biotechnica internal conflict the game actually dramatises, and
it is a complete political machine: a director, a project, a leak, a scapegoat,
and a kill chain.

1. **Koch runs an illegal field trial.** Her team uses Red Ocher nomads as test
   subjects for *Project Nightingale*, allegedly antibiotics research. At least
   70 die; Dr. Isaacson's autopsies find "electromagnetic overstimulation" and
   "drastic neuralgic growth". `[wiki]`
2. **Koch enforces secrecy internally.** She circulates a memo to Biotechnica
   R&D: the side effects "should never leave the company", and she reminds staff
   of the NDA and its penalties. `[wiki]`
3. **A subordinate is purged.** Koch plants incriminating papers on **Emilia
   Morton**; Morton is fired, her accounts and house frozen. Morton threatens to
   leak the poisoning to N54. Koch calls **Sergeant #1919**: "Find and neutralize
   EMILIA MORTON… Sharing this information with any other corporation or the
   NCPD is strictly forbidden." Morton is killed by Animals. `[wiki]`
4. **The leak happens anyway.** Reporter **Manuel Mendoza** works the story,
   talks to Morton, Murphy and others, and hires **DOUBLE O** to hack Biotechnica
   through Impala Automatics. Both are found and killed. `[wiki]`
5. **The company picks a scapegoat.** With the project exposed, "corporate
   higher-ups" pin everything on **Diana Cuno**. Koch signs a "Target for
   liquidation" order; Cuno tries to flee and is murdered by **Arasaka** goons on
   Biotechnica's behalf. `[wiki]`
6. **Koch survives — unless V intervenes.** The Red Ocher pool money, hire
   **Dino Dinovic**, and Dino puts out *Guinea Pigs*. Koch can be killed in her
   apartment or delivered to the clan. Her death is dependent. `[wiki]`
7. **The security apparatus absorbs the blame.** The workers who saw the bodies
   are the next risk: Murphy is out, Weiss is dead, and the email audit is
   running. The corp's answer to a leak is another leak investigation. `[wiki]`

For a simulation this is the cleanest possible internal machine: **the R&D wing
creates the risk; the security wing removes the witnesses; the executive wing
chooses the scapegoat.** Every actor is deniable, and the director who ordered
the killings is a middle manager, not the CEO. `[inferred]`

### 2.3 Licence revenue vs food production

Biotechnica's 2070s strategy has two engines with different politics:

- **The licence engine.** CHOOH2 is patented; Biotechnica licenses it to
  Petrochem (60% of world supply) and 14 other manufacturers, including SovOil,
  and licenses FrostCorn to governments. The income is rent — no farms, no
  factories, no local enemies, but total dependence on Petrochem's goodwill and
  on the patents remaining enforceable. The 2077 netpage announces a licence
  extension, which is the establishment's main diplomatic win. `[wiki]`
- **The food engine.** The licence income funded a move into food production:
  the Biotechnica Flats supply more than half of Night City's alternative
  protein; the corp acquired All Foods; the Badlands R&D facility is its most
  expensive investment. This engine needs land, water, labour, logistics and
  local political cover — and it generates the scandals (Nightingale, the
  All Foods bribery, Crimson Harvest). `[wiki]`

The two engines imply opposite instincts. The licence establishment wants
quiet, legalistic, global diplomacy; the food/R&D wing wants acreage, field
trials and local influence. The 2070s record shows the second outrunning the
first: a regional director running illegal trials, a subsidiary bribing a
councillor, and a security apparatus killing witnesses. `[inferred]`

### 2.4 Europe vs North America

The company is Italian-founded and still runs Rome, Berlin, Paris, London and
Bonn; its global HQ moved to La Jolla, and its Night City regional HQ was built
in 2052. The only dated 2076 event is the **Crimson Harvest bombing
of the Paris research facility** — the deadliest attack in the corporation's
history, which killed ordinary residents and tourists as well as staff. `[wiki]`

That produces a real regional split:

- **Europe** holds the legacy science (biosphere restoration, cloning, the
  Campus, the black-site bioweapons work) and the terrorist war.
- **North America** holds the food business, the CHOOH2 licence relationship and
  the Night City scandals.

It is not an attested power struggle, but it is the natural axis for one: the
European old guard can plausibly regard the Night City food-and-licence branch
as reckless, and the branch can regard Rome as a museum. `[inferred]`

### 2.5 The subsidiary problem: All Foods

All Foods is a Biotechnica subsidiary in 2077, with its own HQ (Mexico City), its
own brand, its own Night City office and its own local politics. It is not a
faction in `data/factions.json`, and it is not run by any named person. In
practice it is a **semi-autonomous commercial bloc**:

- It tried to bribe councilman **Tim Hutchinson** to back a Heywood demolition
  and store opening; the Valentinos threatened him out of the deal. `[wiki]`
- Its Northside factory was shut down and overrun by Maelstrom, and Biotechnica
  in 2077 it is still Maelstrom's main Watson hideout. `[wiki]` `[game-data]`
- Its brand is the public face of the parent's food strategy (EEZYBEEF, feeding
  services, "Eat What You Know"). `[wiki]`

For a simulation, All Foods is the parent's **liability buffer**: a subsidiary
that can absorb a scandal, lose a factory, or bribe a councillor without the
Biotechnica name on the paperwork. `[inferred]`

### 2.6 What could drive internal conflict in a simulation

Evidence-based drivers, in rough order of plausibility:

1. **A Nightingale-style exposure.** A field trial leaks; the R&D director
   scapegoats a subordinate; the security wing kills witnesses; the executive
   wing pretends it knew nothing. Repeatable, and already documented. `[wiki]`
2. **Licence renewal.** The Petrochem relationship is the company's income and
   its leash. A renewal that costs too much splits the establishment from the
   food wing, which wants capital for acreage. `[wiki]` `[inferred]`
3. **Food expansion vs licence caution.** The Flats and All Foods generate
   local political risk the licence business does not want. `[inferred]`
4. **European vs North American priorities.** The Paris bombing and the Night
   City scandals pull security and money in different directions. `[wiki]`
   `[inferred]`
5. **The subsidiary's autonomy.** All Foods can commit the parent to a bribery
   scandal or lose a factory without a board vote. `[wiki]` `[inferred]`
6. **The workforce.** Six vacation days, NDA surveillance, test-subject
   recruitment and scapegoating produce whistleblowers (Morton, Murphy) and
   defectors. Each one is a security problem. `[wiki]`
7. **The intelligence wing's methods.** Killing a reporter, a scientist and a
   witness creates more witnesses; Cuno's murder is witnessed by an Arasaka
   netrunner, Morton's by an Animals Mauler. The cover-up is the leak. `[wiki]`
8. **The empty apex.** With no named CEO, every bloc can claim to speak for the
   company. A board/committee model is the honest simulation. `[inferred]`

---

## 3. External relations matrix

### 3.1 Stance vocabulary and direction

One stance per row, read **from Biotechnica's side**, following the precedence in
`METHOD.md` §3: explicit violence first, then explicit transaction, then
quest-giver role, then adjacency, then a neutral placeholder.

| Stance | Meaning (from Biotechnica's side) |
| --- | --- |
| `war` | Open, active armed conflict over turf or existence |
| `hostile` | Actively targets or raids the other side, but not a declared turf war |
| `rival` | Turf or economic competition, with skirmishes |
| `neutral` | No attested interaction; not an ally |
| `trade` | Transactional exchange, no loyalty |
| `ally` | Coordinated support or shared operations |
| `patron` | This faction protects or funds the other |
| `client` | This faction depends on or works for the other |

Two direction notes:

- **Biotechnica is a supplier, and the vocabulary has no `supplier`.** It sells
  licences, biological weapons and protein; its buyers (Arasaka, Militech,
  Petrochem, All Foods' customers) are recorded as `trade`, with the direction
  stated in the evidence string. This is the same vocabulary gap the Militech
  doc records (§5), and it matters more here because almost every Biotechnica
  relationship is a sale.
- **`client` is used only for hired violence.** Biotechnica is the client of
  Animals (it hired them to kill Morton). It is not a `client` of Arasaka for the
  Cuno killing, because the same relationship also carries the long-running
  troops-for-bioweapons exchange; that row is `trade` and the contract is noted
  in the evidence.

There is **no usable offline attitude matrix**: `Attitude_Record.hpp` is opaque
and `Affiliation.hpp` is identity only. Every stance below is judged from quests,
wiki and spatial adjacency, which is why each row carries a tag and why the
neutral rows are placeholders, not claims of friendship.

### 3.2 The matrix

| Faction | Code | Stance | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| Tyger Claws | `tyger_claws` | `neutral` | No attested conflict. A Claw offer to Alex Pushkin was refused; a fixer's client then kidnapped Pushkin and delivered him to a Claw restaurant as a peace offering. The Claws are Arasaka's proxy; no Biotechnica operation targets them `[wiki]` `[game-data]` `[inferred]` | `game-data+wiki+inferred` |
| Valentinos | `valentinos` | `rival` | All Foods (Biotechnica subsidiary) tried to bribe councilman Tim Hutchinson to back a Heywood demolition; a Valentino group under Danilo Ruiz threatened Hutchinson out of the deal `[wiki]` | `wiki` |
| Arasaka | `arasaka` | `trade` | Declared partner in the corp infobox. Biotechnica provided troops in exchange for exclusive biological weapons, supplied both sides in the Fourth Corporate War with Arasaka getting the exclusives, and in 2077 hired Arasaka goons to murder the scapegoated Diana Cuno `[wiki]` | `wiki` |
| Militech | `militech` | `trade` | Supplied Militech with biological weapons and equipment during the Fourth Corporate War; Militech remained a customer. Mendoza's notes ask whether Nightingale was "on behalf of Militech" — a hypothesis, not proof `[wiki]` `[inferred]` | `wiki+inferred` |
| Kang Tao | `kang_tao` | `neutral` | No attested interaction; a fellow megacorp with no shared site or incident `[inferred]` | `inferred` |
| Petrochem | `petrochem` | `ally` | Biotechnica's largest CHOOH2 licensee (60% of world supply), described as its "strongest ally", and a partner in Xoma's genetic-drug venture. The 2077 netpage announces a licence extension. Asymmetric and conditional: Petrochem has wanted to absorb Biotechnica, Biotechnica holds the virus that can destroy the wheat, and the relationship strains at renewal `[wiki]` | `wiki` |
| Barghest | `barghest` | `neutral` | No attested deal. Biotechnica owns an abandoned Venture Center in Dogtown and its agents operate there during *Roads to Redemption* in Barghest-held turf, but no relationship is documented `[wiki]` `[inferred]` | `wiki+inferred` |
| 6th Street | `sixth_street` | `neutral` | 6th Street is anti-corporate and appears as a separate enemy faction in *Roads to Redemption*; no attested Biotechnica–6th Street incident `[wiki]` `[inferred]` | `wiki+inferred` |
| Aldecaldos | `aldecaldos` | `trade` | Saul Bright negotiated a work-for-xerophytes deal with Biotechnica's Emilia Weiss to recover Biotechnica cargo; the clan rejected a permanent relationship and the deal never concluded `[wiki]` | `wiki` |
| Wraiths | `wraiths` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Animals | `animals` | `client` | Koch ordered Emilia Morton killed; the hit was carried out by Biotechnica-associated Animals mercenaries (the scene is an Animals Mauler; the manifest lists Animals as the enemy). A hired contract, not an alliance `[wiki]` | `wiki` |
| The Mox | `the_mox` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Maelstrom | `maelstrom` | `hostile` | Maelstrom overran and occupies the All Foods Factory, a Biotechnica subsidiary's Northside protein plant, and uses it as its main Watson hideout in 2077 `[wiki]` `[game-data]` | `game-data+wiki` |
| Voodoo Boys | `voodoo_boys` | `neutral` | No attested interaction; the VDBs hack corporate databanks but no Biotechnica operation is documented `[inferred]` | `inferred` |
| NCPD | `ncpd` | `neutral` | Koch's kill order forbids sharing information with the NCPD. No attested cooperation `[wiki]` `[inferred]` | `wiki+inferred` |
| Night Corp | `night_corp` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Scavengers | `scavengers` | `neutral` | No attested interaction. Cedric Muller's scav attack is a Nightingale victim's story, not a Biotechnica–Scav relation `[wiki]` `[inferred]` | `wiki+inferred` |
| City Council | `city_council` | `trade` | All Foods tried to bribe councilman Tim Hutchinson for a Heywood demolition permit; in the 2030s Biotechnica bought a University District HQ permit with cash and two of five NCU trustee seats. Purchased influence, no loyalty `[wiki]` | `wiki` |
| Afterlife | `afterlife` | `neutral` | Neutral merc marketplace; Mendoza met the Biotechnica soldier Brandon Murphy there. No Biotechnica contract `[wiki]` `[inferred]` | `wiki+inferred` |
| Regina Jones | `fixer_regina` | `neutral` | Regina handles *Cyberpsycho Sighting: On Deaf Ears*, a Nightingale victim; she helps the victim, not the corp. No anti-Biotechnica contract `[wiki]` `[inferred]` | `wiki+inferred` |
| Wakako Okada | `fixer_wakako` | `hostile` | Wakako refused Diana Cuno's plea for extraction ("I won't dirty my hands"), and brokers *Olive Branch*, which delivers a kidnapped Biotechnica employee to the Tyger Claws for a fee `[wiki]` | `wiki` |
| Sebastian Ibarra (Padre) | `fixer_padre` | `neutral` | No Biotechnica-specific gig or lore link found `[inferred]` | `inferred` |
| Muamar Reyes (El Capitán) | `fixer_el_capitan` | `neutral` | No Biotechnica-specific gig or lore link found `[inferred]` | `inferred` |
| Dakota Smith | `fixer_dakota` | `neutral` | No Biotechnica-specific gig found; the Flats sit in her Badlands but she runs no contract against them `[inferred]` | `inferred` |
| Dino Dinovic | `fixer_dino` | `hostile` | Dino takes the Red Ocher's contract and puts out *Guinea Pigs*, the hit on Koch; he also supplies the extraction AV if she is taken alive `[wiki]` | `wiki` |
| Rogue Amendiares | `fixer_rogue` | `neutral` | No Biotechnica-specific gig or lore link found `[inferred]` | `inferred` |
| Mr. Hands | `fixer_mr_hands` | `neutral` | Hands gives *Roads to Redemption*, which targets Crimson Harvest; Biotechnica agents are an optional obstacle, not the client `[wiki]` `[inferred]` | `wiki+inferred` |
| Network 54 | `news54` | `hostile` | Sasha Yakovleva uploaded the Securicine files to N54 before Biotechnica security killed her; Morton threatened to leak the Nightingale poisoning to N54; Mendoza's notes list N54's Bes Isis as a contact `[wiki]` | `wiki` |

Stance counts (**28 rows**): **neutral 17, hostile 4, trade 4, rival 1,
client 1, ally 1; war 0, patron 0.**

The three that matter most for the mod:

- **`petrochem` — `ally`.** The only alliance Biotechnica has, and the one that
  keeps the world's fuel running. It is a licence entente, not a friendship: the
  weapon that guarantees it is Biotechnica's virus that can destroy the CHOOH2
  wheat. Modelling Petrochem as a guarantor means modelling leverage, not trust.
  `[wiki]`
- **`maelstrom` — `hostile`.** The faction's one demonstrated territorial loss:
  its own subsidiary's factory is Maelstrom's main hideout. It is also the
  clearest example of Biotechnica's Military weakness — it did not retake the
  plant. `[wiki]` `[game-data]`
- **`arasaka` — `trade`.** A long-running bioweapons-for-troops exchange, plus a
  deniable assassination contract in 2077. Arasaka is the corp Biotechnica calls
  when it needs violence it cannot do itself, which is the strategic shape of the
  faction. `[wiki]`

Militech is a close fourth: a customer and a possible silent sponsor of
Nightingale, but the evidence is a note, not a contract. `[wiki]` `[inferred]`

### 3.3 Actors outside `data/factions.json`

Real relationships with no faction code, so prose only:

- **Crimson Harvest** — the anti-Biotechnica terrorist organisation. Farmers and
  agricultural entrepreneurs ruined by FrostCorn licence fees; Biotechnica
  raised prices and (per rumour) released a virus that killed unlicensed crops;
  the movement radicalised and bombed the Paris research facility in 2076, the
  deadliest attack in the corp's history. It is banned as a terrorist
  organisation and remains at large. **Hostile**, and the faction's most
  important non-faction enemy. `[wiki]`
- **Red Ocher** — the nomad clan used as Nightingale test subjects; at least 70
  dead. It hired Dino Dinovic to kill Koch. **Hostile**, and the source of the
  only gig in which a player can remove a Biotechnica director. `[wiki]`
- **SovOil** — the second major CHOOH2 licensee. A licence relationship on the
  same model as Petrochem, with no 2077 incident. `[wiki]`
- **Impala Automatics** — a Biotechnica business partner whose servers were the
  route DOUBLE O used to hack the corp's net; both the netrunner and the reporter
  were killed. A security failure, not an alliance. `[wiki]`
- **All Foods** — the subsidiary, not a faction (see §2.5). `[wiki]`
- **Xoma Corporation** — Petrochem's pharmaceutical subsidiary, in a cooperative
  genetic-drug and custom-bacteria venture with Biotechnica. The joint venture is
  the concrete content of the Petrochem alliance. `[wiki]`
- **The Aldecaldo Bright family** — Saul Bright's family, not the whole clan; the
  xerophyte negotiation was with Emilia Weiss and died in the family council. `[wiki]`
- **Dr. Emilia Weiss** — a Biotechnica employee, not an external actor; listed
  here because her shard is the only source for the Badlands research centre's
  logistics and for the Aldecaldo negotiation. `[wiki]`
- **The University District / NCU board** — the 2030s deal that gave Biotechnica
  two of five trustee seats is a historical model of municipal capture; the 2077
  equivalent is the All Foods bribery. `[wiki]` `[lore]`
- **The Paris research facility** — a 2076 target, off-map, no local record;
  the only attested mass-casualty attack on the corp. `[wiki]`
- **Biotechnica's intelligence agency** — named once in a shard, never
  structured; the operational face is Linda Sherman and the hotel security
  apparatus. Prose only, because it is a department rather than a faction. `[wiki]`

### 3.4 Guarantor assessment

The design question: if a player founds an organisation, which factions would
guarantee Biotechnica's support, and which would Biotechnica guarantee?

- **Biotechnica is a strong economic guarantor and a weak military one.** It can
  guarantee food, fuel licences, pharmaceuticals and cloned organs; it cannot
  guarantee a firefight. Its Military weakness is documented: 25 roster units,
  one real garrison, no units at the Flats, a factory lost to Maelstrom, and
  violence outsourced to Animals and Arasaka. `[game-data]` `[inferred]`
- **The only `ally` is Petrochem, and it is conditional.** The relation survives
  because Biotechnica holds the patents and the crop-killing virus; Petrochem
  would absorb Biotechnica if it could. A player who takes Biotechnica's support
  inherits the licence diplomacy, not a mutual-defence pact. `[wiki]`
- **The plausible guarantors for a player-founded organisation are therefore
  issue-specific, not corporate:**
  - a food-supply contract (the Flats or an All Foods franchise) that makes the
    player's org a customer of the corp; `[inferred]`
  - a research partnership under the netpage's "partners in research" scheme,
    which is explicitly selective and licence-based; `[wiki]`
  - a corrupt municipal channel (the All Foods/Hutchinson pattern) rather than a
    corporate alliance; `[wiki]`
  - a Petrochem-mediated fuel/crop deal, where Biotechnica is the licensor and
    Petrochem the enforcer. `[wiki]` `[inferred]`
  None is a formal alliance except the Petrochem entente.
- **Biotechnica as an aggressor is unlikely to be kinetic.** For a player holding
  a Biotechnica point, the likely response is economic and legal first (licence
  withdrawal, supply cut, a bought councillor), then deniable: a hired Animals
  hit, an Arasaka contractor, or an "intelligence agency" operation. The one
  place it will fight openly is its own hotel, with its security guards and droids.
  `[inferred]`
- **The food lever is the real guarantor asset.** The Flats supply more than half
  of Night City's alternative protein. A player who controls or protects that
  supply has leverage over every restaurant, market and food stall in the city,
  and Biotechnica has every reason to guarantee a partner who keeps it running.
  That is a stronger political guarantee than any of its 25 guards. `[wiki]`
  `[inferred]`

---

## 4. Pillar notes

Design claims from `docs/design/gameplay-systems.md`: Biotechnica is a
**Corporation** (archetype strength **Technology**, weakness **Culture**);
faction strength **Economy**, weakness **Military**. The seed agrees with the
design's shape: `income_multiplier 1.35` (mid-table megacorp) and
`hostility_bias 0.3` (low). `[game-data]`

| Pillar | Design claim | Lore verdict | Evidence |
| --- | --- | --- | --- |
| Technology (archetype strength) | Corporations are technology-led | **Strongly supported, but it is bio-technology, not weapons or cyberware.** Biotechnica's edge is CHOOH2, cloning (first self-aware clone, 2020), cloned organs and limbs, de-extinct species (beaver, swift fox, eastern cottontail), FrostCorn, Securicine, the immunosuppressant prototype 0.091, and the Nightingale neural research. It is the world's largest biotech company, not an arms or cyberware house. | CHOOH2 patent; cloning history; Securicine; prototype 0.091; species restoration; Nightingale; netpage products `[wiki]` |
| Culture (archetype weakness) | Corporations are culturally weak | **Supported, sharply.** Biotechnica has no street culture, no uniform, no loyalty oath and no visible iconography beyond a logo and a slogan ("Adapting You to the Future"). Its soft power is a **job listing**: third-best employer in Night City, six paid vacation days, free healthcare at remote sites. That is a brand, not a culture. Internally, the culture is a laboratory meritocracy that produces brilliant managers with no socialisation and a habit of scapegoating; externally it produces no friends, only customers and enemies. | *Big 5 Employers*; netpage careers; 2045 campus note on science graduates promoted to management; Morton/Cuno/Murphy `[wiki]` `[game-data]` |
| Economy (faction strength) | Biotechnica is an economic power | **Strongly supported. This is the faction.** CHOOH2 is the world's standard fuel and Biotechnica owns the patent; it licenses Petrochem (60% of supply) and 14 other manufacturers, including SovOil; FrostCorn licences fund governments and ruin small farmers; the Flats supply over half of Night City's alternative protein; All Foods is a subsidiary. The royalty stream is rent on the world's fuel supply, and it funded the food expansion. | Licence structure; Petrochem page; Flats; All Foods; protein report shard `[wiki]` `[game-data]` |
| Military (faction weakness) | Biotechnica is militarily weak | **Strongly supported, with one nuance.** It has 25 roster units, one real garrison, zero units at the Flats, lost its All Foods factory to Maelstrom (still Maelstrom-held in 2077), and hires Animals and Arasaka when it needs a killing. The nuance: its **defensive** security is competent (8 patrols, 4 guard areas, doors, cameras, droids at the hotel), and its **bioweapon deterrent** is strategic — the virus that can destroy all CHOOH2 wheat is why Petrochem has not tried to absorb it. Model it as **weak force projection, strong site defence, strong deterrent**. | Roster 2 sites/25 units; hotel site records; All Foods; Petrochem "what it created, it can destroy" `[game-data]` `[wiki]` |
| Overall fit | The pillars fit the corp's identity | **Good for identity, and unusually clean for the mod.** A rentier biotech giant that is rich, legally entangled, militarily thin and politically invisible is exactly the "Corporation / Economy / Military" fit. Keep Economy strong, Military weak, Technology strong, Culture as a job advert. | Synthesis `[inferred]` |

Design cautions, not redesigns:

- **Do not model Biotechnica as a normal territorial corp.** It has no street
  presence and almost no garrison; its power is contractual. An economy layer
  that treats it like Arasaka will get the map wrong: its most valuable asset
  (the Flats) has no defenders at all. `[game-data]` `[inferred]`
- **Do not model Military as zero.** The hotel security is real, and the
  bioweapon deterrent is the reason the licence relationship exists. It is weak
  at *projection*, not at *defence*. `[inferred]`
- **Do not model Culture as a gang culture.** There is no Biotechnica street
  identity to recruit from. A player joining the corp joins a workplace, not a
  tribe; the political game is the office, the lab and the audit. `[inferred]`
- **The food supply is the faction's real political lever.** Whoever controls
  the Flats controls more than half the city's alternative protein. That should
  be the highest-value economic point in the faction, and the reason other
  factions want a partner there rather than a war. `[wiki]` `[inferred]`
- **The cover-up is the internal-politics template.** Koch → Cuno → Morton →
  Murphy is a complete, evidenced machine that can be reskinned for any leak.
  Use it instead of inventing a dynastic feud the faction does not have.
  `[wiki]`

---

## 5. Gaps and uncertainties

1. **No 2077 CEO or board members are named anywhere.** The wiki's CEO line
   stops at the 2040s; no shard, computer or dialogue names the 2077 apex.
   The JSON uses `character_record_id: null` and `presence_class: off-map`. A
   simulation must invent the apex or model a board/committee. This is the
   single largest gap in the faction's politics.
2. **Tina Caruso is a red link with one citation.** The Biotechnica page cites
   "background dialogue during *The Heist*"; there is no page, no local dialogue
   transcript in the extract, and no character record. She is `[wiki]` only, and
   `mentioned` is generous. Worse, the mod's §7 timeline removes the Konpeki
   heist, so the scene that attests her will not occur; she survives as a name
   for the West Coast branch, not as a scene.
3. **No named leader is ambient.** The only named records are Koch (a gig target)
   and Pushkin (a gig captive). Everything above them is `mentioned` or
   `off-map`. The mod must spawn leadership; the game will not provide it.
4. **The Dogtown cell may not exist in this mod's timeline.** *Roads to
   Redemption* is a Phantom Liberty gig whose prerequisite is *Firestarter*;
   §7 removes the PL main chain. The 4-agent `{sts_ep1_07_agents}` presence,
   Linda Sherman's pursuit and the *One Way or Another* follow-up should be
   treated as unavailable unless the mod re-enables the gig. This is a
   timeline-specific gap, not a data gap.
5. **The Flats has ownership but no garrison.** Zero Biotechnica units, spawns or
   communities in the Badlands; the "HQ" is a sub-territory centroid. A capture
   point there has no defenders unless the mod adds them (location doc §8.2).
   This is also the clearest evidence for the Military weakness.
6. **The hotel's title is doubled in the seed.** Site 353 `sts_cct_dtn_04` sits
   in `dtn_goldsmith_dock` (sub 72, **Militech**, `initial_owner_faction_id 21`,
   `control_center_id 72`), while the seeded `dtn_central_concourse` (sub 75) has
   been renamed "Biotechnica Hotel" with its centroid on the hotel and an **active**
   CC. One physical place, two titles. The location doc's §8.1 conflict has been
   half-fixed: the name and anchor moved, the site row did not. A seeder needs an
   explicit rule for which title wins. `[game-data]`
7. **Rosters miss quest communities.** The 4 Dogtown agents are not in
   `data/sites/rosters.json`; the only local evidence is `areas.jsonl`. The
   25-unit roster count therefore undercounts operational presence and should
   not be read as total manpower.
8. **Koch's record is generic.** `Character.sts_dtn_04_target` is the
   target-elimination actor; the identity is inferred from the prefab
   (`#sts_cct_dtn_04_koch_path`, `#dtn_04_ws_joanne_koch_hide`) and the wiki
   `baseid`. Do not seed a `Character.Koch`.
9. **Pushkin's record is `alex`, not `pushkin`.** Identity via site 418,
   `faction_id 23`, the wiki `baseid` and the *Olive Branch* page. Do not search
   for `pushkin` in rosters; it returns nothing.
10. **A trigger names "Lauren".** `#dtn_04_tr_av_kill_lauren` and
    `#dtn_04_tr_av_kills_lauren` sit in the hotel prefab, but there is no
    character record, no page and no other mention. She may be the receptionist
    (`Character.dtn_04_receptionist`) under a development name, or a cut
    character. Do not seed her.
11. **Most named people have no records at all.** Cuno, Morton, Weiss, Murphy,
    Sherman, Isaacson, Caruso and Sergeant #1919 are shard-, computer-, netpage-
    or dialogue-only. Their `character_record_id` is `null` and their presence
    class is `mentioned` or `off-map`.
12. **The Militech link to Nightingale is a hypothesis.** Mendoza's notes ask
    "studies tied to militech?"; the Project Nightingale page says the study
    "may have been done on behalf of Militech." No contract, order or payment is
    attested. The `trade` stance rests on the Fourth Corporate War supply
    relationship, not on Nightingale. Tag `[inferred]`.
13. **The Petrochem "ally" row is conditional and asymmetric.** The phrase
    "strongest ally" is 2020/RED lore; the 2077 evidence is a netpage licence
    extension. Petrochem wanted to absorb Biotechnica, and Biotechnica's leverage
    is a virus that can destroy the CHOOH2 wheat. Treat `ally` as a licence
    entente, not a mutual-defence pact.
14. **Crimson Harvest and Red Ocher are not in `data/factions.json`.** They are
    the faction's two most important enemies and appear in prose only. A
    simulation that needs them must add them as special factions or model them
    as events.
15. **The "70 dead" number is the wiki's, not the game's.** The *Notes
    (Downtown)* shard lists 12 confirmed names and says "allegedly over 70
    total." Do not build a precise casualty mechanic on 70.
16. **The 2077 intelligence agency has no structure.** It is named once in a
    shard ("Biotechnica's intelligence agency"), and its only named operative is
    Linda Sherman, who has no page or record. The security apparatus is a
    department, not a faction; §2.1 treats it as a bloc with a null leader.
17. **The University District municipal capture is RED-era.** The HQ deal (cash
    plus two of five NCU trustee seats) is 2030s lore; the 2077 city_council
    relation rests on the All Foods bribery of Tim Hutchinson. Do not present the
    2030s deal as a 2077 arrangement.
18. **"Third-best employer" and "six vacation days" are satire.** The Big 5
    shard is an in-world list; do not read it as a satisfaction metric or as
    evidence of good working conditions. The same corp kills its own staff.
19. **The seed's `income_multiplier` and `hostility_bias` are tuning, not lore.**
    `1.35` and `0.3` happen to match the design pillars; they are not evidence.
20. **The 2077 netpage is marketing.** The Badlands R&D recruitment, the "pet to
    order" service, the embryo modification and the drug-test volunteers are all
    corporate advertising; treat them as evidence of what the corp *says*, not
    what it does. The shards show what it does.
21. **There is no Biotechnica lifepath or prologue.** The Corpo lifepath is
    Arasaka's; the Nomad lifepath passes through the Flats as scenery and is
    chased by Arasaka, not Biotechnica. Any "join Biotechnica" path must be
    built, not reused.
22. **No offline attitude matrix.** `Attitude_Record.hpp` is opaque and
    `Affiliation.hpp` is identity only. Every stance is judged from quests, wiki
    and adjacency; a TweakDB dump would settle the neutral rows.

### 5.1 Sources consulted

Local:

- `data/factions.json` — faction id 23, `affiliation_enum = Biotechnica`,
  `category = megacorp`, `income_multiplier 1.35`, `hostility_bias 0.3`.
- `data/sites/rosters.json` — 25 units across sites 353 (`sts_cct_dtn_04`: 12
  `sts_dtn_04_security`, 9 `sts_dtn_04_security_droids`, 1 `dtn_04_receptionist`,
  1 `sts_dtn_04_security_officer`, 1 `sts_dtn_04_target`) and 418
  (`sts_wbr_jpn_01`: 1 `sts_wbr_jpn_01_alex`).
- `data/sites/sites.json` — site 353 (gig site, `default_faction_id 23`,
  `initial_owner_faction_id 21`, `control_center_id 72`, sub 72); site 418
  (`default_faction_id 2`, sub 24); site 359 `sts_ep1_07`
  (`default_faction_id 10`, sub 63).
- `data/sites/{guards,triggers,spots}.json` — hotel guard areas
  (`#dtn_04_guard_area`, `#dtn_04_bottom_floor_guard_area`,
  `#dtn_04_appartment_floor_guard_area`, `#dtn_04_roof_floor_guard_area`),
  triggers (`#dtn_04_tr_target`, `#dtn_04_tr_find_joanne_koch`,
  `#dtn_04_tr_av_kill_lauren`), and the receptionist/security workspots.
- `data/sub_territories.json` — sub 75 `dtn_central_concourse` ("Biotechnica
  Hotel", owner 23), sub 88 `bls_biotechnica_flats` (owner 23), sub 72
  `dtn_goldsmith_dock` (owner 21).
- `data/control_centers.json` — `cc_dtn_central_concourse` (active, at the
  hotel), `cc_bls_biotechnica_flats` (inactive).
- `data/landmarks.json` — `lm_dtn_central_concourse`, `lm_bls_biotechnica_flats`.
- `dist/extract/areas.jsonl` — `{dtn_04_com_area}` 18, `{dtn_04_com_area_after_alarm}`
  5, `{dtn_04_com_npc}` 1, `{sts_ep1_07_agents}` 4, `{jpn_01_com_alex}` 1.
- `dist/extract/markers.jsonl` — `q000_mp_protein_farm_meeting`,
  `q000_nomad_wp_protein_farm_test`, `mq018_07_sm_protein`,
  `mq018_mp_protein_gate`, `mq061_05_sm_biotechnica_farms_scene`,
  `q003_mp_allfoods_*`.
- `dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_1.streamingsector.json`
  — registry entries `dtn_04_target_s` (`Character.sts_dtn_04_target`),
  `alex` (`Character.sts_wbr_jpn_01_alex`), `client`
  (`Character.sts_ep1_07_client`), `agent_01` (`Character.sts_ep1_07_agent_01`);
  prefab paths `#c_city_center/downtown/loc_sts_cct_dtn_04_prefab*`.
- `docs/design/gameplay-systems.md` — archetype/pillar table (§1) and the
  alternate timeline (§7).
- `docs/research/factions/biotechnica.md` — location catalogue, HQ, ownership.
- `docs/research/factions/METHOD.md` — data pitfalls (§1.1–§1.2).
- `docs/research/factions/politics/METHOD.md` — politics method.
- Other politics docs read for cross-incidents: `arasaka.md`, `militech.md`,
  `maelstrom.md`.

Wiki (MediaWiki API, `action=parse&prop=wikitext`, 2026-11-25):

- [Biotechnica](https://cyberpunk.fandom.com/wiki/Biotechnica) ·
  [Biotechnica/Netpage](https://cyberpunk.fandom.com/wiki/Biotechnica/Netpage) ·
  [List of Biotechnica employees](https://cyberpunk.fandom.com/wiki/List_of_Biotechnica_employees)
- [Joanne Koch](https://cyberpunk.fandom.com/wiki/Joanne_Koch) ·
  [Diana Cuno](https://cyberpunk.fandom.com/wiki/Diana_Cuno) ·
  [Emilia Morton](https://cyberpunk.fandom.com/wiki/Emilia_Morton) ·
  [Nele Springer](https://cyberpunk.fandom.com/wiki/Nele_Springer) ·
  [Nicolo Loggagia](https://cyberpunk.fandom.com/wiki/Nicolo_Loggagia)
- [Project Nightingale](https://cyberpunk.fandom.com/wiki/Project_Nightingale) ·
  [Gig: Guinea Pigs](https://cyberpunk.fandom.com/wiki/Gig:_Guinea_Pigs) ·
  [Gig: Olive Branch](https://cyberpunk.fandom.com/wiki/Gig:_Olive_Branch) ·
  [Gig: Roads to Redemption](https://cyberpunk.fandom.com/wiki/Gig:_Roads_to_Redemption) ·
  [One Way or Another](https://cyberpunk.fandom.com/wiki/One_Way_or_Another)
- [Biotechnica Flats](https://cyberpunk.fandom.com/wiki/Biotechnica_Flats) ·
  [Biotechnica Hotel](https://cyberpunk.fandom.com/wiki/Biotechnica_Hotel) ·
  [Biotechnica Building](https://cyberpunk.fandom.com/wiki/Biotechnica_Building) ·
  [Biotechnica Campus](https://cyberpunk.fandom.com/wiki/Biotechnica_Campus) ·
  [Biotechnica Mono-clonal Research Station](https://cyberpunk.fandom.com/wiki/Biotechnica_Mono-clonal_Research_Station)
- [All Foods](https://cyberpunk.fandom.com/wiki/All_Foods) ·
  [All Foods Factory](https://cyberpunk.fandom.com/wiki/All_Foods_Factory) ·
  [Petrochem](https://cyberpunk.fandom.com/wiki/Petrochem) ·
  [Crimson Harvest](https://cyberpunk.fandom.com/wiki/Crimson_Harvest) ·
  [Red Ocher](https://cyberpunk.fandom.com/wiki/Red_Ocher)
- [Securicine](https://cyberpunk.fandom.com/wiki/Securicine) ·
  [Sasha Yakovleva](https://cyberpunk.fandom.com/wiki/Sasha_Yakovleva) ·
  [The Nomad](https://cyberpunk.fandom.com/wiki/The_Nomad) ·
  [Welcome to Paradise](https://cyberpunk.fandom.com/wiki/Welcome_to_Paradise)
- Shards and computers: [Notes (Downtown)](https://cyberpunk.fandom.com/wiki/Notes_(Downtown)) ·
  [Target for liquidation](https://cyberpunk.fandom.com/wiki/Target_for_liquidation) ·
  [Archived Conversation: Emilia Morton and Joanne Koch](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Emilia_Morton_and_Joanne_Koch) ·
  [Archived Conversation: SERGEANT 1919 and Joanne Koch](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_SERGEANT_1919_and_Joanne_Koch) ·
  [Archived Conversation: Linda Sherman and Miriam Levy](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Linda_Sherman_and_Miriam_Levy) ·
  [Archived Conversation: Diana Cuno and Wakako Okada](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Diana_Cuno_and_Wakako_Okada) ·
  [Archived Conversation: Saul Bright and Emilia Weiss](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Saul_Bright_and_Emilia_Weiss) ·
  [Archived Conversation: Brandon Murphy and Dave Arbus](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Brandon_Murphy_and_Dave_Arbus) ·
  [Joanne Koch/Computers](https://cyberpunk.fandom.com/wiki/Joanne_Koch/Computers) ·
  [Protein Farms: A Report](https://cyberpunk.fandom.com/wiki/Protein_Farms:_A_Report) ·
  [The Crimson Harvest: Freedom Fighters or Terrorists?](https://cyberpunk.fandom.com/wiki/The_Crimson_Harvest:_Freedom_Fighters_or_Terrorists%3F) ·
  [Big 5 Employers in Night City – 2077](https://cyberpunk.fandom.com/wiki/Big_5_Employers_in_Night_City_%E2%80%93_2077)

---

## 6. Machine-readable block

```json
{
  "faction_code": "biotechnica",
  "leaders": [
    {
      "name": "The 2077 CEO (unnamed)",
      "role": "Global chief executive; unnamed in every 2077 source; the wiki CEO line stops at the 2040s",
      "character_record_id": null,
      "location_name": "La Jolla HQ, SoCal / Rome (former HQ)",
      "open_world": false,
      "presence_class": "off-map",
      "source": "wiki Biotechnica (Leadership: Loggagia 2020s-2040s, then Caruso and Koch in the 2070s); no 2077 CEO named in any shard, computer or dialogue",
      "confidence": "wiki"
    },
    {
      "name": "Biotechnica Board of Directors",
      "role": "Collective sovereign; sold the CHOOH2 licences in the 1990s",
      "character_record_id": null,
      "location_name": "Rome / La Jolla; regional board seats",
      "open_world": false,
      "presence_class": "off-map",
      "source": "wiki Biotechnica (1991 licence sale to 14 manufacturers); wiki Petrochem (licence structure)",
      "confidence": "wiki"
    },
    {
      "name": "Tina Caruso",
      "role": "Head of the West Coast branch, 2070s",
      "character_record_id": null,
      "location_name": "West Coast branch to Night City regional HQ",
      "open_world": false,
      "presence_class": "mentioned",
      "source": "wiki Biotechnica leadership list, cited to background dialogue during The Heist; red link, no page, no local record; the mod's alternate timeline removes The Heist",
      "confidence": "wiki"
    },
    {
      "name": "Dr. Joanne Koch",
      "role": "Regional Director for Technology and Development; genetics engineer; head of the Nightingale field programme",
      "character_record_id": "Character.sts_dtn_04_target",
      "location_name": "Biotechnica Hotel, floor 19, apartment 193",
      "open_world": true,
      "presence_class": "world-activity",
      "source": "roster site 353 sts_cct_dtn_04 (faction_id 23); raw always_loaded_1 entry dtn_04_target_s phase default; prefab nodes #sts_cct_dtn_04_koch_path, #sts_cct_dtn_04_koch_bd_editor, #dtn_04_ws_joanne_koch_hide; wiki Joanne Koch; wiki Gig: Guinea Pigs (baseid sts_cct_dtn_04)",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "name": "Dr. Diana Cuno",
      "role": "Genetics engineer; Nightingale co-researcher; scapegoated and killed",
      "character_record_id": null,
      "location_name": "North Oak (corpse, Lilac Street)",
      "open_world": false,
      "presence_class": "mentioned",
      "source": "wiki Diana Cuno; shard Archived Conversation: Diana Cuno and Wakako Okada; shard Target for liquidation",
      "confidence": "wiki"
    },
    {
      "name": "Alex (Aleksander) Pushkin",
      "role": "Senior Quality Control Assistant; Nightingale field-team member",
      "character_record_id": "Character.sts_wbr_jpn_01_alex",
      "location_name": "Tyger Claws garage, Redwood St., Japantown (in a car trunk)",
      "open_world": true,
      "presence_class": "world-activity",
      "source": "roster site 418 sts_wbr_jpn_01 (faction_id 23, 1 unit); raw always_loaded_1 entry alex phase 0_default; wiki Gig: Olive Branch (baseid sts_wbr_jpn_01); wiki Joanne Koch notes",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "name": "Emilia Morton",
      "role": "Corp staff; framed by Koch, fired, then killed",
      "character_record_id": null,
      "location_name": "Corpo Plaza (corpse)",
      "open_world": false,
      "presence_class": "mentioned",
      "source": "wiki Emilia Morton; shards Archived Conversation: Emilia Morton and Joanne Koch and Archived Conversation: SERGEANT 1919 and Joanne Koch",
      "confidence": "wiki"
    },
    {
      "name": "Emilia Weiss",
      "role": "Biotechnica employee handling the new Badlands research centre's missing parts shipment; negotiates with Saul Bright",
      "character_record_id": null,
      "location_name": "Rocky Ridge, northern Badlands (corpse)",
      "open_world": false,
      "presence_class": "mentioned",
      "source": "shard Archived Conversation: Saul Bright and Emilia Weiss; wiki Biotechnica (Saul Bright negotiation)",
      "confidence": "wiki"
    },
    {
      "name": "Brandon Murphy",
      "role": "Soldier; Nightingale sample collection; lost an arm to the test subjects",
      "character_record_id": null,
      "location_name": "Formerly the Nightingale site; last seen leaving the corp",
      "open_world": false,
      "presence_class": "mentioned",
      "source": "wiki List of Biotechnica employees; shard Archived Conversation: Brandon Murphy and Dave Arbus; shard Notes (Downtown)",
      "confidence": "wiki"
    },
    {
      "name": "Linda Sherman",
      "role": "Biotechnica intelligence operative; runs the Dogtown pursuit of Nele Springer",
      "character_record_id": null,
      "location_name": "Dogtown / Nighthawks Rehabilitation Center operation",
      "open_world": false,
      "presence_class": "mentioned",
      "source": "shard Archived Conversation: Linda Sherman and Miriam Levy; wiki Biotechnica; shard The Crimson Harvest: Freedom Fighters or Terrorists?; tied to a Phantom Liberty gig removed by the mod's alternate timeline",
      "confidence": "wiki"
    },
    {
      "name": "Dr. Isaacson",
      "role": "R&D physician; performed the Nightingale autopsies",
      "character_record_id": null,
      "location_name": "Nightingale programme",
      "open_world": false,
      "presence_class": "mentioned",
      "source": "computer message Joanne Koch/Computers, Nightingale [WORK IN PROGRESS]",
      "confidence": "wiki"
    },
    {
      "name": "Biotechnica Sergeant #1919",
      "role": "Security dispatcher; receives Koch's kill order for Emilia Morton",
      "character_record_id": null,
      "location_name": "Downtown / hotel security net",
      "open_world": false,
      "presence_class": "mentioned",
      "source": "shard Archived Conversation: SERGEANT 1919 and Joanne Koch",
      "confidence": "wiki"
    },
    {
      "name": "James Scherer",
      "role": "Researcher, German branch; implant and organic-muscle programme",
      "character_record_id": null,
      "location_name": "German branch",
      "open_world": false,
      "presence_class": "off-map",
      "source": "netpage Biotechnica/Netpage, news item New implant type!",
      "confidence": "wiki"
    },
    {
      "name": "Nicolo Loggagia",
      "role": "CEO, 2020s-2040s; biochemist; the company's builder",
      "character_record_id": null,
      "location_name": "Monte-Carlo / Rome HQ",
      "open_world": false,
      "presence_class": "historical",
      "source": "wiki Nicolo Loggagia (alive as of 2045); wiki Biotechnica leadership list",
      "confidence": "wiki+lore"
    },
    {
      "name": "Epione Song",
      "role": "Division manager, Night City branch, 2045; Home and Garden division",
      "character_record_id": null,
      "location_name": "Biotechnica Campus, University District (2045)",
      "open_world": false,
      "presence_class": "historical",
      "source": "wiki Biotechnica Campus",
      "confidence": "wiki+lore"
    },
    {
      "name": "Annabel Cruz",
      "role": "Junior engineer, bioweapons black site (Columbia-1/2), RED era",
      "character_record_id": null,
      "location_name": "Biotechnica black site",
      "open_world": false,
      "presence_class": "historical",
      "source": "wiki List of Biotechnica employees (Cyberpunk RED table)",
      "confidence": "wiki+lore"
    },
    {
      "name": "Francis Young",
      "role": "Cloning scientist; first self-aware clone (2020)",
      "character_record_id": null,
      "location_name": "Night City cloning station",
      "open_world": false,
      "presence_class": "historical",
      "source": "wiki Biotechnica (2000s history)",
      "confidence": "wiki+lore"
    }
  ],
  "internal_factions": [
    {
      "name": "The licence establishment (CHOOH2 / FrostCorn royalties)",
      "leader": null,
      "goals": "Protect the patents; keep licence revenue flowing; keep Petrochem cordial; stay out of the news",
      "members_hint": "Board and unnamed CEO; 14 other licensees plus Petrochem (60% of world supply); FrostCorn licence governments",
      "source": "wiki Biotechnica (1991 licence sale); wiki Petrochem (licence structure, strongest ally)",
      "confidence": "wiki"
    },
    {
      "name": "The West Coast / Night City branch",
      "leader": "Tina Caruso",
      "goals": "Run the regional HQ, the staff hotel and the local business; keep the branch functional",
      "members_hint": "Caruso; Joanne Koch; the Biotechnica Building; the hotel receptionist and maid; 24 hotel units",
      "source": "wiki Biotechnica leadership; wiki Biotechnica Hotel; roster site 353",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The R&D / field-science wing (Nightingale)",
      "leader": "Dr. Joanne Koch",
      "goals": "Breakthroughs at any cost: field trials on nomads, immunosuppressants, cloning, new species; conceal the side effects",
      "members_hint": "Koch; Diana Cuno; Alex Pushkin; Dr. Isaacson; Brandon Murphy; Emilia Weiss (logistics); the Badlands R&D facility",
      "source": "wiki Project Nightingale; wiki Joanne Koch; wiki Diana Cuno; shards; netpage Come work in the Badlands",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The security and intelligence apparatus",
      "leader": null,
      "goals": "Protect the corp's property and reputation; surveil employees; eliminate leaks; use deniable contractors",
      "members_hint": "Unnamed intelligence chief; Sergeant #1919; hotel security officer, 12 guards and 9 droids; Linda Sherman; hired Animals and Arasaka contractors",
      "source": "roster site 353; shards SERGEANT 1919, Linda Sherman, Target for liquidation; wiki Sasha Yakovleva",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The All Foods commercial wing",
      "leader": null,
      "goals": "Market share in synthetic food; retail expansion; local political influence; keep the brand clean",
      "members_hint": "All Foods HQ Mexico City; Night City office on Eisenhower St.; the Northside factory (lost to Maelstrom)",
      "source": "wiki All Foods; wiki All Foods Factory; shard All Foods - Eat What You Know",
      "confidence": "wiki"
    },
    {
      "name": "The European / founder-science old guard",
      "leader": "Nicolo Loggagia",
      "goals": "Biosphere restoration, pure research, new species; the company Loggagia built rather than the 2070s food-and-licence business",
      "members_hint": "Loggagia (historical); James Scherer; Annabel Cruz; Rome, Berlin, Paris, London and Bonn facilities",
      "source": "wiki Nicolo Loggagia; wiki Biotechnica Campus; wiki Crimson Harvest; netpage",
      "confidence": "wiki+lore"
    },
    {
      "name": "The NDA-bound workforce",
      "leader": null,
      "goals": "Survive the audit, keep the job, avoid becoming the scapegoat",
      "members_hint": "Receptionist, maid, Corp staff, manual workers, test volunteers; six vacation days; third-best employer",
      "source": "shard Big 5 Employers in Night City - 2077; netpage careers; shards Murphy/Arbus and Morton/Koch",
      "confidence": "game-data+wiki"
    }
  ],
  "relations": [
    {
      "faction_code": "tyger_claws",
      "stance": "neutral",
      "evidence": "No attested conflict. A Claw offer to Alex Pushkin was refused; a fixer's client then kidnapped Pushkin and delivered him to a Claw restaurant as a peace offering. The Claws are Arasaka's proxy; no Biotechnica operation targets them [wiki] [game-data] [inferred]",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "faction_code": "valentinos",
      "stance": "rival",
      "evidence": "All Foods (Biotechnica subsidiary) tried to bribe councilman Tim Hutchinson to back a Heywood demolition; a Valentino group under Danilo Ruiz threatened Hutchinson out of the deal [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "arasaka",
      "stance": "trade",
      "evidence": "Declared partner in the corp infobox. Biotechnica provided troops in exchange for exclusive biological weapons, supplied both sides in the Fourth Corporate War with Arasaka getting the exclusives, and in 2077 hired Arasaka goons to murder the scapegoated Diana Cuno [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "militech",
      "stance": "trade",
      "evidence": "Supplied Militech with biological weapons and equipment during the Fourth Corporate War; Militech remained a customer. Mendoza's notes ask whether Nightingale was on behalf of Militech, a hypothesis rather than proof [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "kang_tao",
      "stance": "neutral",
      "evidence": "No attested interaction; a fellow megacorp with no shared site or incident [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "petrochem",
      "stance": "ally",
      "evidence": "Biotechnica's largest CHOOH2 licensee (60% of world supply), described as its strongest ally, and a partner in Xoma's genetic-drug venture. The 2077 netpage announces a licence extension. Asymmetric and conditional: Petrochem has wanted to absorb Biotechnica, Biotechnica holds the virus that can destroy the wheat, and the relationship strains at renewal [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "barghest",
      "stance": "neutral",
      "evidence": "No attested deal. Biotechnica owns an abandoned Venture Center in Dogtown and its agents operate there during Roads to Redemption in Barghest-held turf, but no relationship is documented [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "sixth_street",
      "stance": "neutral",
      "evidence": "6th Street is anti-corporate and appears as a separate enemy faction in Roads to Redemption; no attested Biotechnica-6th Street incident [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "aldecaldos",
      "stance": "trade",
      "evidence": "Saul Bright negotiated a work-for-xerophytes deal with Biotechnica's Emilia Weiss to recover Biotechnica cargo; the clan rejected a permanent relationship and the deal never concluded [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "wraiths",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "animals",
      "stance": "client",
      "evidence": "Koch ordered Emilia Morton killed; the hit was carried out by Biotechnica-associated Animals mercenaries (the scene is an Animals Mauler; the manifest lists Animals as the enemy). A hired contract, not an alliance [wiki]",
      "confidence": "wiki"
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
      "evidence": "Maelstrom overran and occupies the All Foods Factory, a Biotechnica subsidiary's Northside protein plant, and uses it as its main Watson hideout in 2077 [wiki] [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "voodoo_boys",
      "stance": "neutral",
      "evidence": "No attested interaction; the VDBs hack corporate databanks but no Biotechnica operation is documented [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "ncpd",
      "stance": "neutral",
      "evidence": "Koch's kill order forbids sharing information with the NCPD. No attested cooperation [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "night_corp",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "scavengers",
      "stance": "neutral",
      "evidence": "No attested interaction. Cedric Muller's scav attack is a Nightingale victim's story, not a Biotechnica-Scav relation [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "city_council",
      "stance": "trade",
      "evidence": "All Foods tried to bribe councilman Tim Hutchinson for a Heywood demolition permit; in the 2030s Biotechnica bought a University District HQ permit with cash and two of five NCU trustee seats. Purchased influence, no loyalty [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "afterlife",
      "stance": "neutral",
      "evidence": "Neutral merc marketplace; Mendoza met the Biotechnica soldier Brandon Murphy there. No Biotechnica contract [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "fixer_regina",
      "stance": "neutral",
      "evidence": "Regina handles Cyberpsycho Sighting: On Deaf Ears, a Nightingale victim; she helps the victim, not the corp. No anti-Biotechnica contract [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "fixer_wakako",
      "stance": "hostile",
      "evidence": "Wakako refused Diana Cuno's plea for extraction (I won't dirty my hands with it), and brokers Olive Branch, which delivers a kidnapped Biotechnica employee to the Tyger Claws for a fee [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "fixer_padre",
      "stance": "neutral",
      "evidence": "No Biotechnica-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_el_capitan",
      "stance": "neutral",
      "evidence": "No Biotechnica-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_dakota",
      "stance": "neutral",
      "evidence": "No Biotechnica-specific gig found; the Flats sit in her Badlands but she runs no contract against them [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_dino",
      "stance": "hostile",
      "evidence": "Dino takes the Red Ocher's contract and puts out Guinea Pigs, the hit on Koch; he also supplies the extraction AV if she is taken alive [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "fixer_rogue",
      "stance": "neutral",
      "evidence": "No Biotechnica-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_mr_hands",
      "stance": "neutral",
      "evidence": "Hands gives Roads to Redemption, which targets Crimson Harvest; Biotechnica agents are an optional obstacle, not the client [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "news54",
      "stance": "hostile",
      "evidence": "Sasha Yakovleva uploaded the Securicine files to N54 before Biotechnica security killed her; Morton threatened to leak the Nightingale poisoning to N54; Mendoza's notes list N54's Bes Isis as a contact [wiki]",
      "confidence": "wiki"
    }
  ]
}
```
