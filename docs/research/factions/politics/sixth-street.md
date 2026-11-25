# 6th Street — Leadership, Internal Politics and External Relations

Status: faction politics research, 2026-11-25. One faction, one document.
Scope: Cyberpunk 2077 2.5 + Phantom Liberty, campaign disabled. This document
maps the people and politics of 6th Street onto the places catalogued in
[`../sixth-street.md`](../sixth-street.md); it does not repeat that location
catalog.

Method: this document follows
[`./METHOD.md`](./METHOD.md), including its §1.1 corrections, and uses
[`./maelstrom.md`](./maelstrom.md) as the worked example. The location rules
and data-source pitfalls are in [`../METHOD.md`](../METHOD.md).

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/comic/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My reasoning links a named person, place or stance to a record; reasoning stated | Weak, flagged |

**Presence class** (this document only): `ambient` = persists in free roam
without a quest; `world-activity` = gig, side job, scanner hustle, assault in
progress or minor job — free-roam content but activity-gated; `story` = gated
by a main or Phantom Liberty quest; `prologue` = lifepath intro; `mentioned` =
named in quest text, shards or dialogue but with no world actor; `historical` =
no 2077 actor and not part of the 2077 story. The JSON `open_world` flag is
`true` for `ambient` + `world-activity`, `false` for everything else.

---

## 1. Leadership and ranks

### 1.1 The 2077 chain of command

6th Street is a **paramilitary militia with a gang's revenue model**, not a
corporate hierarchy or a street crew. It uses military ranks — General,
Captain, Lieutenant, Sergeant, Officer — and it still calls itself an
"organization." The 2077 top is a **coup regime**: Will Gunner killed
"General" Rick Morton in late 2076 and purged Morton's people.

| Name | 2077 role | Character record | Location / influence point | Presence class | Source | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| **Will Gunner** | General (2076–present; seized power in a coup) | `Character.q305_gunner` | Pre-ambush staging in an abandoned hotel overlooking a skybridge, West Wind Estate, Pacifica | `story` | Raw `always_loaded_1` community registry, entry `gunner`, appearance `man_average__q305__6thstreet_officer`, phase `start`, spot `#q305_ws_pre_ambush_gunner_start`; area `{q305_com_6th_street_pre_ambush}` at `(-2758.2, -2466.5, 17.3)`; wiki *Will Gunner* | `[game-data]` `[wiki]` |
| **Rick Morton** | Former General (unknown–2076); killed in Gunner's coup for siding with corporations | no 2077 record | — | `historical` | Wiki *Rick Morton*; *6th Street Members* | `[wiki]` |
| **Captain Sherman** | Captain of a Rancho Coronado company; Walker's CO; hosts Gunner's ascension party | `Character.mq008_6th_street_representative` `[inferred]` | Stadium Love rooftop, Rancho Coronado | `world-activity` | Raw `mq008` community template uses the generic representative/male records; markers `mq008_01_sm_party_chats` `(495.7, -2143.4, 27.3)` and `mq008_02_sm_shooting_contest` `(503.0, -2128.7, 27.4)`; wiki *Stadium Love* | `[game-data]` `[inferred]` `[wiki]` |
| **Walker** | Sharpshooter; Sherman's subordinate and the shooting-contest rival | no named record (generic `Character.mq008_6th_street_male`) | Stadium Love rooftop, Rancho Coronado | `world-activity` | Wiki *Stadium Love*; 6th Street Members; generic `mq008` spawn entries | `[wiki]` `[inferred]` |
| **Lucius Thoran** | Techie and H6 cell technical chief; stole a corporate weapon El Capitán was hired to sabotage | `Character.sts_std_arr_11_lucius` | 6th Street hideout, Megabuilding H6 floor 19, Arroyo | `world-activity` | `data/sites/rosters.json` site 384 `sts_std_arr_11`; site anchor `(-199.039, -843.481, 259.170)`; wiki *Lucius Thoran*; *Gig: Hacking the Hacker* | `[game-data]` `[wiki]` |
| **Darius Miles** | Drug-ring leader (beta acid); NCPD most-wanted | `Character.ma_std_arr_03_outpost_miniboss` `[inferred]` | Darius Miles' drug lab, Hargreaves St, Arroyo | `world-activity` | `data/sites/rosters.json` site 125 `ma_std_arr_03`, entry `#enemy05`, role `boss`; site anchor `(-614.238, -1038.144, 7.390)`; NCPD dispatch names Darius; wiki *Darius Miles* | `[game-data]` `[inferred]` `[wiki]` |
| **Olga Elisabeth Longmead** | Rogue cell leader; kidnapping and two murders; operates outside Gunner's control | `Character.ma_std_rcr_08_outpost_miniboss` `[inferred]` | Two-storey house on Carnitas St, Rancho Coronado | `world-activity` | `data/sites/rosters.json` site 153 `ma_std_rcr_08`, entry `miniboss`, role `boss`; site anchor `(-156.981, -2169.689, 5.782)`; NCPD dispatch *New Boss, New Rules*; wiki *Olga Elisabeth Longmead* | `[game-data]` `[inferred]` `[wiki]` |
| **Nolan Frakes** | Senior member; Valentinos-war hardliner; ordered the hit on Gustavo Orta | no 2077 record | — | `mentioned` | Wiki *Nolan Frakes*; *Gig: Bring Me the Head of Gustavo Orta* | `[wiki]` |
| **Wyatt Alken** | Car thief and fence; guards a Samurai bootleg at the Acorn Towers lot | `Character.sts_wbr_hil_06_wyatt_alken` | Acorn Towers parking lot, Crockett St, Charter Hill | `world-activity` | `data/sites/rosters.json` site 416 `sts_wbr_hil_06`; site anchor `(375.332, -400.129, 2.646)`; wiki *Wyatt Alken*; *Gig: Family Heirloom* | `[game-data]` `[wiki]` |
| **Flavio dos Santos** | Ex-member and Morton loyalist; fugitive from Gunner's purge | `Character.sts_std_rcr_03_flavio` (faction `null`) | Flavio's house, Mallagra St, Rancho Coronado | `world-activity` | `data/sites/rosters.json` site 388 `sts_std_rcr_03`, entry `flavio`, phase `#rcr_03_ws_flavio_appear`; site anchor `(446.939, -1267.613, 28.730)`; wiki *Flavio dos Santos*; *Gig: Going-away Party* | `[game-data]` `[wiki]` |
| **Hilary McKenna** | Auto-shop owner on Mission Street; Assault in Progress target | `Character.ma_std_arr_09_hilary` | Mission Street autoshop, Arroyo | `world-activity` | `data/sites/rosters.json` site 131 `ma_std_arr_09`; site anchor `(-883.503, -1008.289, 11.553)`; wiki *Hilary McKenna* | `[game-data]` `[wiki]` |
| **Sam Carter** | Member in the Streetkid prologue; tried to push the Valentinos out of Vista del Rey; executed by Padre | no 2077 record | Vista del Rey / the prologue ride through the Glen | `prologue` | Wiki *Sam Carter*; *The Streetkid*; *6th Street Members* | `[wiki]` |
| **Pablo Silva** | Former high-ranking member; scapegoated for Morton's death and murdered | no 2077 record | — | `historical` | Wiki *Pablo Silva*; shard *Sent to 47 users* | `[wiki]` |
| **Boz** | Lieutenant; the gang's contact for nomad couriers | no 2077 record | — | `mentioned` | Wiki *Boz*; *6th Street Members* | `[wiki]` |

Two rank details matter for the simulation:

- **Captain is a real 2077 rank.** Sherman is a captain, Walker is his
  subordinate, and the data also carries `captain` records at sites 153 and 154
  (`Character.ma_std_rcr_08_captain`, `Character.ma_std_rcr_09_captain`) plus
  `sergeant_01`, `sergeant_02` and `captain_sergeant_03` at site 153. The
  wiki's infobox only names General, Captain and Lieutenant; the records add
  Sergeant and Officer.
- **The "General" is a political title, not a staff rank.** The gang has no
  general staff, no written succession rule and no council. Gunner's authority
  is personal, performative and violent.

### 1.2 Succession history: one coup and one founding

| Period | Leader | How the change happened |
| --- | --- | --- |
| 2020s–unknown | **Solomon "X" Wright** | Founder; former US Army colonel and intelligence officer; organized Fourth Corporate War veterans. `[wiki]` |
| unknown–2076 | **Rick Morton** | "General"; corporate-friendly; killed in Gunner's coup. `[wiki]` |
| late 2076–2077 | **Will Gunner** | Killed Morton, blamed Pablo Silva and "corporate traitors," purged Morton's lieutenants and loyalists. `[wiki]` |

Two mechanisms are attested, and only one is institutional:

1. **X's 2/3 command-staff vote (2040s).** Wright divided operations into the
   "3-I's" — Investigations (detectives), Impact (troopers), Internal
   (management) — and could be overruled if two-thirds of the command staff
   disagreed. This is Cyberpunk RED lore, not 2077 practice. `[wiki]` `[lore]`
2. **The coup (2076).** Gunner killed the boss and purged the losers. No vote,
   no council, no heir. `[wiki]`

The historical lesson is the opposite of Maelstrom's: 6th Street's succession
is **rare and ideological**, not chronically violent. The gang changed leaders
twice in fifty years, and the second change was a single decisive coup followed
by a purge. That makes the 2076 schism the central political fact of 2077, not
a permanent succession crisis.

**The veteran-founders vs young-recruits hint.** The sources support a
tenure-and-ideology divide, but not a simple age divide:

- The founders were Fourth Corporate War veterans; by the 2070s the ranks were
  Unification War veterans, retired military, discharged corporate security
  officers and civilians given crash military training after joining. `[wiki]`
- The 2076 coup is framed as **anti-corporate purists vs members willing to
  deal with corporations**, not as old vs young. Gunner's faction is the
  anti-corporate one; Morton's was the corporate-friendly one. `[wiki]`
- Tenure still matters: Morton's loyalists were the old guard, and Gunner's
  purge targeted them by loyalty, not by age. A simulation should model
  **loyalty to the Morton settlement vs loyalty to Gunner's coup**, with
  veteran status as a modifier, not the axis itself. `[inferred]`

### 1.3 Rank structure, entry and advancement

1. **General.** Single leader. Gunner. Commands through a personal company,
   the "General" myth and the purge.
2. **Captain.** Company commander. Sherman is the only named 2077 captain;
   the data adds captain records at Rancho sites 153 and 154.
3. **Lieutenant.** Staff or functional rank. Boz is the nomad-courier contact;
   the wiki's Members page lists the rank but gives no 2077 staff list.
4. **Sergeant / Officer.** The data shows sergeants and officers at the
   Almunecar outpost and at the H6, Wicked Tires and Acorn Towers sites. These
   are the people who actually run a site's guard shift.
5. **Members.** ≈2,300 by 2077. Veterans and ex-corporate security are
   fast-tracked; civilians receive military training after joining. `[wiki]`

**Entry is a training pipeline, not a chrome ritual.** Unlike Maelstrom, 6th
Street has no cyberware requirement. The gang's 2045 rule — a monthly
cyberware report, with release from service above a chrome threshold — is a
RED-era safety rule, not a 2077 entry gate. `[wiki]` `[lore]`

**Advancement is reputational and political.** A member rises by military
competence, by running a revenue racket, and by loyalty to the current boss.
Gunner's purge made the last criterion explicit: Morton's loyalists were killed
or driven out regardless of competence. Gunner is also "largely disinterested
in the day-to-day operations of the gang, such as overseeing extortion
rackets," which delegates real power to captains and site officers. `[wiki]`

### 1.4 Named members mapped to game data

Most named 6th Street NPCs are **not in `data/sites/rosters.json`**. The
exceptions are the site-level named records listed above. Rows marked
`[inferred]` are one-record deductions (the only boss record at a gig's
`baseid`, or the generic quest record); verify in-game before treating them as
canonical.

| Name | Role / note | Character record | Community / site | Location | Presence class | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| Will Gunner | General | `Character.q305_gunner` | `{q305_com_6th_street_pre_ambush}` (26) | West Wind Estate | `story` | `[game-data]` `[wiki]` |
| Rick Morton | Former General | none | — | — | `historical` | `[wiki]` |
| Captain Sherman | Captain, Rancho company | `Character.mq008_6th_street_representative` (inferred) | `{mq008_com_representative}` (1), `{mq008_com_shooting}` (14) | Stadium Love rooftop | `world-activity` | `[inferred]` `[wiki]` |
| Walker | Sharpshooter | none (generic `mq008_6th_street_male`) | `{mq008_com_shooting}` (14) | Stadium Love rooftop | `world-activity` | `[wiki]` |
| Buck Arnold | Arroyo fighting champion | none | — | Arroyo (*Beat on the Brat*) | `world-activity` | `[wiki]` |
| Lucius Thoran | Techie, H6 cell | `Character.sts_std_arr_11_lucius` | Site 384 `{arr_11_com}` (15) | Megabuilding H6 floor 19 | `world-activity` | `[game-data]` `[wiki]` |
| Darius Miles | Drug-ring leader | `Character.ma_std_arr_03_outpost_miniboss` (inferred) | Site 125 `{ma_std_arr_03_com}` (13) | Hargreaves St lab | `world-activity` | `[inferred]` `[wiki]` |
| Olga Longmead | Rogue cell leader | `Character.ma_std_rcr_08_outpost_miniboss` (inferred) | Site 153 (13) | Carnitas St house | `world-activity` | `[inferred]` `[wiki]` |
| Nolan Frakes | Senior member, war hardliner | none | — | — | `mentioned` | `[wiki]` |
| Wyatt Alken | Car fence / guard | `Character.sts_wbr_hil_06_wyatt_alken` | Site 416 (12) | Acorn Towers lot | `world-activity` | `[game-data]` `[wiki]` |
| Flavio dos Santos | Ex-member, Morton loyalist | `Character.sts_std_rcr_03_flavio` (faction `null`) | Site 388 (6) | Flavio's house | `world-activity` | `[game-data]` `[wiki]` |
| Hilary McKenna | Autoshop owner | `Character.ma_std_arr_09_hilary` | Site 131 (5) | Mission St | `world-activity` | `[game-data]` `[wiki]` |
| Sam Carter | Prologue member | none | — | The Glen / Vista del Rey | `prologue` | `[wiki]` |
| Pablo Silva | Former high-ranking member | none | — | — | `historical` | `[wiki]` |
| Boz | Lieutenant, nomad contact | none | — | — | `mentioned` | `[wiki]` |
| Jake Estevez | Ex-techie (two weeks with the gang) | none | — | Wicked Tires Autoshop | `world-activity` | `[wiki]` |
| Matt Dodges; Patricia Gerville | Members named only in the world book | none | — | — | `historical` | `[wiki]` |
| Martha Frakes | Ex-member, comatose; appears as "Martha Young" in *Heroes* | none | — | Jackie's funeral (*Heroes*) | `story` | `[wiki]` |

Three data cautions:

- **`Patricia` is a name collision.** `Character.sts_std_arr_06_sixthstreet_patrol2_ranged2_ajax_wa_Patricia`
  is a 6th Street NPC at the Red White warehouse, not Maelstrom's Patricia
  Sirawian. `Patricia Gerville` is a separate 6th Street member with no record.
- **`Sherman` is a place name.** The wiki page *Sherman* is a Texas prison
  city. There is no *Sherman (6th Street)* page and no `Character.*sherman`
  record; the captain is the generic `mq008_6th_street_representative`.
- **`Boz` has no 2077 actor.** A raw registry entry named `boz` exists inside
  `{sts_ep1_03_boss_com}`, but that community is a Scavenger site and the entry
  is not a 6th Street spawn. Treat Boz as a mentioned lieutenant, not a world
  actor.

### 1.5 What the game actually spawns (open world vs story-only)

This is the part other agents must not assume. A named NPC on the wiki does
not mean an actor in free roam.

**`ambient` — persists in free roam without a quest.**
- No named 6th Street NPC is confirmed ambient. The gang's street patrols are
  ambient, but every named person is tied to an activity or a quest. `[game-data]`

**`world-activity` — gig, side job, scanner hustle, assault in progress or
minor job; free-roam content but activity-gated.**
- **Captain Sherman, Walker and the Stadium Love party** in Rancho Coronado
  (`mq008`; *Stadium Love*). `[game-data]` `[wiki]`
- **Lucius Thoran** at the Megabuilding H6 hideout (*Hacking the Hacker*,
  `baseid=sts_std_arr_11`). `[game-data]` `[wiki]`
- **Darius Miles** at the Hargreaves St lab (*Suspected Organized Crime
  Activity (Arroyo)*, `baseid=ma_std_arr_03`). `[game-data]` `[wiki]`
- **Olga Longmead** at the Carnitas St house (*Suspected Organized Crime
  Activity: New Boss, New Rules*, `baseid=ma_std_rcr_08`). `[game-data]` `[wiki]`
- **Wyatt Alken** at the Acorn Towers lot (*Family Heirloom*,
  `baseid=sts_wbr_hil_06`). `[game-data]` `[wiki]`
- **Flavio dos Santos** at his house (*Going-away Party*,
  `baseid=sts_std_rcr_03`). He has `faction_id = null`; he is a quest ally,
  not a 6th Street unit. `[game-data]` `[wiki]`
- **Hilary McKenna** at the Mission Street autoshop (Assault in Progress,
  site 131 `ma_std_arr_09`). `[game-data]` `[wiki]`
- **Buck Arnold** at the Arroyo fistfight (*Beat on the Brat: Arroyo*). No
  record found; marker-only. `[wiki]`
- **Jake Estevez** at Wicked Tires (*Life's Work*), an ex-member and asset,
  not a member. `[wiki]`

**`story` — gated by a main or Phantom Liberty quest; do not expect them in
free roam with the campaign disabled.**
- **Will Gunner** in *Black Steel In The Hour of Chaos* (PL main job,
  `q305_prison_convoy`). His community is the pre-ambush staging community,
  not a turf spawn. `[game-data]` `[wiki]`
- **Martha Frakes** as "Martha Young" at Jackie's funeral in *Heroes*; she is
  comatose after the 6th Street hit on Gustavo. `[wiki]`

**`mentioned` — named in quest text, shards or dialogue, but no world actor.**
- **Nolan Frakes** is the client who pays for the *Bring Me the Head of
  Gustavo Orta* contract; he has no actor record. `[wiki]`
- **Boz** is the nomad-courier lieutenant in the Members page and Panam's
  backstory; he has no 2077 actor. `[wiki]`

**`prologue` — lifepath intro.**
- **Sam Carter** in *The Streetkid* (`q000_street_kid`). He confronts Padre on
  the ride to Embers and is later executed by the Valentinos. `[wiki]`

**`historical` — not in 2077 at all.**
- Solomon "X" Wright, Arbiter, Rick Morton, Pablo Silva, Matt Dodges and
  Patricia Gerville. `[wiki]` `[lore]`

Caveat: "campaign disabled" may also suppress gigs, side jobs and scanner
hustles if the mod disables all quest content. The `world-activity` rows are
the best reuse candidates, but they still need an in-game spawn check. The
`story` rows are the ones to replace with simulation agents.

### 1.6 Player-path hooks

This is the design-facing summary of who a player can join under, climb past,
ally with or remove.

| Person | Join under | Climb past | Ally with | Remove |
| --- | --- | --- | --- | --- |
| **Will Gunner** | The anti-corporate coup line; military expansion; the "General" cult | He is the top; climbing past him means a coup or a succession after his death | His personal company, the anti-corp purists, the Kendachi channel (quietly) | Killing Gunner opens a three-way contest: captains, techies, rogue cells |
| **Captain Sherman** | A Rancho Coronado company; patriotic street culture, parties, contests | He is a captain; a player under him climbs by winning fights and running rackets | Walker, Buck Arnold, the Rancho party network | Removing Sherman decapitates the Rancho social-recruitment machine |
| **Lucius Thoran** | The technical wing: arms jailbreaking, netrunning, the H6 cell | He is a cell chief; a player can take his lab and his El Capitán contract | Techies, Kendachi, the arms pipeline | Removing Lucius cuts the H6 arms jailbreak |
| **Darius Miles** | The drug ring: beta-acid production and wholesale | He is a ring boss; a player under him climbs by controlling the lab | Drug distributors, the Dewdrop Inn lab | Removing Darius opens the lab and collects the NCPD reward |
| **Olga Longmead** | A rogue cell: kidnapping, ransom, private violence | She is a rogue boss outside Gunner's control | The hostage/ransom network, corrupt military contacts | Removing Olga frees the hostages and embarrasses Gunner |
| **Nolan Frakes** | The Valentinos war; Vista del Rey revanchism | He is a senior member, not a formal rank; climbing past him means taking the war policy | The war hardliners, Sam Carter's memory | Removing Nolan ends the private vendetta or escalates it |
| **Flavio dos Santos** | The Morton restoration; the old guard's revenge | He is a fugitive, not a ladder | Morton loyalists, the Aldecaldos, El Capitán | Gunner's men are already trying; helping him is a direct challenge to Gunner |
| **Wyatt Alken** | The vehicle/fence economy | He is a fence, not a ladder | Car thieves, the Acorn Towers lot | Removing him opens the lot and the bootleg-Samurai stash |
| **Hilary McKenna** | The autoshop economy | She is a shop owner, not a ladder | Vehicle repairs, the Mission Street trade | Removing her opens the shop and the local vehicle racket |
| **Jake Estevez** | Not a membership path; he is an **asset** | — | Ally for vehicle software and custom builds | Cutting him off costs the gang a techie |

The design consequence: 6th Street has **a formal ladder with a captured top**.
A player can join as a soldier, rise through a captain's company or a revenue
wing, and then face a single illegitimate General whose removal has no
institutional successor.

---

## 2. Internal political factions

### 2.1 The blocs

"Members" counts below are **presence proxies** from `data/sites/rosters.json`
and `dist/extract/areas.jsonl`, not membership rolls. Several `mq008`
communities are overlapping phases of one party; do not sum them.

| Bloc | Leader(s) | What it wants | Presence / members hint | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- |
| **Gunner's coup regime (anti-corporate patriots)** | Will Gunner | Anti-corporate purity, purge Morton loyalists, territorial expansion, patriotic legitimacy | `{q305_com_6th_street_pre_ambush}` 26; Gunner's officer appearance `man_average__q305__6thstreet_officer`; the prison and Militech channels used by the purge | Gunner killed Morton and purged the old guard; he calls himself General and lets the gang throw parties in his honor | `[game-data]` `[wiki]` |
| **Morton's purged old guard (corporate pragmatists)** | Rick Morton (dead); Pablo Silva (dead); Flavio dos Santos (fugitive) | Restore the old arrangement, keep corporate deals, survive the purge | No active community; Flavio at site 388 (1 of 6, faction `null`); Pablo dead; Tina Agron's protein channel cancelled | Morton "sided with the corporations"; Gunner scapegoated Pablo, killed incarcerated loyalists in a Militech prison and hunted Flavio | `[game-data]` `[wiki]` |
| **Field captains and the patriotic street culture** | Captain Sherman; Walker; Buck Arnold | Prestige, fighting, turf, recruitment, Gunner's cult of personality | `{mq008_com_shooting}` 14, `{mq008_com_6th_street_party}` 6, `{mq008_com_representative}` 1, `{mq008_com_background}` 1; captain records at sites 153 and 154 | *Stadium Love* (party, shooting contest, membership offer); *Beat on the Brat*; the Members page's captains and champions | `[game-data]` `[wiki]` |
| **Technical-economic wing (techies, garages, labs)** | Lucius Thoran; site officers | Arms jailbreaking, the Kendachi "Arsenal," vehicle work, drug production, fencing | Sites 384 (15), 389 (15), 125 (13), 416 (12), 382 (10), 368 (8), 379 (6), 131 (5) | *Hacking the Hacker*, *Serious Side Effects*, *Error 404*, *Nasty Hangover*, *Family Heirloom*, *Life's Work* | `[game-data]` `[wiki]` |
| **Rogue frontier cells** | Olga Longmead; Darius Miles | Personal profit, kidnapping and ransom, drug rings, autonomy outside Gunner's control | Site 153 (13, Olga); site 125 (13, Darius); separate communities with their own bosses | Olga holds hostages "outside the control of 6th Street's General Will Gunner"; Darius runs a drug ring the NCPD treats as a separate target | `[game-data]` `[wiki]` |
| **Valentinos-war hardliners** | Nolan Frakes; Sam Carter (dead) | Escalate the Vista del Rey war, avenge Martha, push the Valentinos out | Site 57 `ma_hey_gle_11` 4; site 65 `ma_hey_rey_05` 4; `sa_ep1_135_com_combat` 4 vs 4 vs 4 | Nolan ordered the hit on Gustavo; Sam Carter threatened Padre; the war "intensifying" in 2077 | `[game-data]` `[wiki]` |
| **Outlying chapters (Glen, Charter Hill, Vista del Rey)** | Local officers (Wicked Tires, Acorn Towers) | Hold revenue outposts in rival districts; survive without heartland support | Site 368 Glen 8; site 416 Charter Hill 12; site 65 Vista del Rey 4; site 47 Glen 6 | Wiki: "other districts under their control had their own local HQs"; the data shows officer-led cells far from Arroyo | `[game-data]` `[wiki]` |

### 2.2 The 2076 coup: the split that defines 2077

The cleanest political fact in the faction is the late-2076 coup. It was a
**schism between members willing to deal with corporations and members who
considered such deals a betrayal of the gang's founding principles.** `[wiki]`

- **Morton's line:** work with corporations. Morton "sided with the
  corporations"; the gang had been supplied by Militech and Kendachi; a
  corporate-friendly arrangement was the status quo. `[wiki]`
- **Gunner's line:** anti-corporate purity. Gunner's faction seized power,
  killed Morton, and presented the coup as a restoration of the founding
  mission. `[wiki]`
- **The purge:** Gunner killed Morton's lieutenants, loyalists and associates;
  he ordered the deaths of 6th Streeters incarcerated in a Militech prison; he
  hunted Flavio dos Santos; he scapegoated Pablo Silva, falsely claiming Silva
  and "corporate traitors" killed Morton. `[wiki]`
- **The contradiction:** despite Gunner's anti-corporate stance, 6th Street
  "continued to work with some corporations, and even secretly cooperated with
  Kendachi to design a new line of weapons." `[wiki]`

That contradiction is the faction's central political vulnerability. Gunner's
legitimacy rests on anti-corporate purity, but his revenue rests on the
Kendachi "Arsenal" project and on corporate-grade weapons. A player who
exposes the Kendachi deal can collapse the regime without firing a shot; a
player who protects it can keep the revenue and lose the ideology.

The human cost is also a political weapon. Gunner tried to coerce **Tina
Agron**, a Biotechnica Flats worker stealing proteins for the gang, into a
partnership; when she demanded the cut she had under Morton, Gunner broke
negotiations and ordered her death. `[wiki]` That is the old corporate channel
being run by the new anti-corporate boss — evidence that the purge was about
power, not principle. `[inferred]`

### 2.3 Gunner's governing style

Gunner is a **war leader and figurehead, not an administrator**:

- He is "largely disinterested in the day-to-day operations of the gang, such
  as overseeing extortion rackets," but he occasionally sends people to
  collect due debts. `[wiki]`
- He delegates revenue to captains and site officers, which is why the
  technical-economic wing has real power despite having no political voice.
- He governs through spectacle: the gang throws parties in his honor, and the
  Stadium Love shooting contest is an ascension celebration. `[wiki]`
- He governs through fear: the purge, the prison killings, the hunt for
  Flavio, the order to kill V after Flavio escapes. `[wiki]`

The consequence for a simulation: Gunner's authority is high on **loyalty and
fear**, low on **administration and legitimacy**. Removing him does not produce
a clear successor; it produces a contest between the captains (Sherman), the
technical wing (Lucius), the rogue cells (Olga, Darius) and any surviving
Morton loyalist (Flavio).

### 2.4 The captains and the patriotic street culture

Sherman's world is the gang's public face:

- *Stadium Love*: a rooftop party with drinking, a shooting contest, betting
  and a membership offer. Sherman suppresses hostilities while V is polite and
  warns that the next encounter will be hostile. `[wiki]`
- *Beat on the Brat: Arroyo*: Buck Arnold, the "fighting champion of Arroyo,"
  is an arrogant ex-soldier who bets his rifle on a fistfight. `[wiki]`
- Walker is the sharpshooter and Sherman's subordinate; beating him is the
  test of skill. `[wiki]`

This bloc is Gunner's base, but it is also a **rival power center**. A captain
who wins fights, throws better parties and recruits more soldiers can become
more popular than the General. The 2076 coup proves that popularity plus
violence is enough to take the gang; nothing in the structure prevents a
captain from doing to Gunner what Gunner did to Morton.

### 2.5 The technical-economic wing

The techies and site bosses are the revenue engine:

- **Lucius Thoran** runs the H6 cell's arms jailbreak; the cell "jumped a
  Militech transport" and cracks corporate weapons. `[wiki]` `[game-data]`
- **Darius Miles** runs a beta-acid ring through the Dewdrop Inn lab. `[wiki]`
- **Hilary McKenna** runs an auto shop on Mission Street and uses the gang to
  kill a troublesome customer. `[wiki]`
- **Wyatt Alken** steals and sells cars and fences a bootleg Samurai
  recording. `[wiki]`
- **Jake Estevez** is an ex-member techie; the gang chased him off after two
  weeks, and Padre hires V to recover his car from Wicked Tires. `[wiki]`

They have money and skills but no formal political role. That is a classic
civil-military gap: the people who generate revenue are not the people who
decide policy. A player who controls the labs, garages and fences can starve
the General's company without ever challenging him in a firefight.

### 2.6 The rogue frontier cells

The clearest limit on Gunner's authority is **Olga Longmead**:

- She holds hostages in a house on Carnitas Street and demands ransom from
  their families, "primarily other military personnel, outside the control of
  6th Street's General Will Gunner." `[wiki]`
- She is wanted for kidnapping and two counts of first-degree murder, and she
  collaborates with Clarence and Anne Brown. `[wiki]`

**Darius Miles** is a softer version: a high-ranking member running a drug ring
that the NCPD treats as a separate organized-crime target. `[wiki]` He is not
described as disloyal, but his operation has its own economy, its own lab and
its own NCPD file.

These cells show that 6th Street's "company" structure is real but uneven. The
heartland is policed; the frontier is franchised. A player can build a power
base in a rogue cell before the General notices.

### 2.7 The Valentinos-war hardliners

The war with the Valentinos is both policy and personal vendetta:

- **Sam Carter** tried to remove the Valentinos from Vista del Rey by
  threatening their members; Padre executed him. `[wiki]`
- **Nolan Frakes** ordered the execution of Gustavo Orta, the Valentinos'
  interim leader. Martha Frakes, Nolan's daughter and Gustavo's girlfriend,
  was in the car and was shot into a coma. Nolan blamed Gustavo, not himself,
  and hired Padre to finish the job. `[wiki]`
- The war has been running since at least 2071 and escalated over Vista del Rey
  in 2074; by 2077 it is "intensifying." `[wiki]`

The hardliners are a policy bloc because they keep choosing escalation over
containment. The Valentinos' own politics doc describes the mirror-image
debate: Gustavo wants a private war, while the frontage bloc and Padre want it
contained. `[wiki]` On the 6th Street side, Nolan is the escalation engine; a
player who removes him can de-escalate, and a player who backs him inherits a
war the gang cannot win quickly.

### 2.8 The outlying chapters

The wiki says the Arroyo HQ was the main headquarters, but "the other districts
under their control had their own local HQs that were responsible for
patrolling the neighborhood and monitoring the gang's facilities." `[wiki]`

The data shows the pattern:

- **Glen (Heywood):** Wicked Tires Autoshop (site 368, 8 units) and two
  outposts (site 47, a scanner hustle; site 57, a 6th-vs-Valentinos shootout).
- **Charter Hill (Westbrook):** Acorn Towers parking lot (site 416, 12 units),
  a fence and vehicle operation inside Tyger Claws territory.
- **Vista del Rey (Heywood):** site 65, a 4-unit presence at a bar robbery in
  the contested Valentinos district; the site itself is NCPD-owned.

These chapters are revenue outposts with local officers, not a separate
command. They are also the most exposed: the Glen and Vista del Rey presences
sit in Valentinos turf, and Charter Hill sits in Tyger Claws turf. The heartland
vs frontier tension is therefore real: the Arroyo/Rancho heartland sets policy,
while the frontier pays the price.

### 2.9 What could drive internal conflict in a simulation

Evidence-based drivers, in rough order of plausibility:

1. **Succession after Gunner.** No heir, no council, no vote. The captains, the
   technical wing and the rogue cells all have a claim, and Flavio is a living
   Morton claimant.
2. **Anti-corporate purity vs the Kendachi secret.** Gunner's legitimacy is
   anti-corporate; his revenue is corporate. Exposing "Arsenal" is a
   regime-ending move.
3. **Revenue control.** The labs, garages, fences and arms pipeline are run by
   people with no political voice. A player who controls them can starve the
   General's company.
4. **The Valentinos war.** Escalate (Nolan) or contain (a business-minded
   captain). The war costs lives and turf and has already wounded Nolan's
   daughter.
5. **Treatment of Morton loyalists.** Purge (Gunner), reintegrate (a
   legitimacy-seeking successor), or use-and-discard. Flavio is the test case.
6. **Frontier autonomy.** Olga and Darius show that a cell can run its own
   economy. A captain who tolerates them loses control; one who crushes them
   loses revenue.
7. **NCPD and fixer pressure.** El Capitán, Rogue and Mr. Hands all run
   contracts against 6th Street. A captain who loses a racket to a fixer looks
   weak; a captain who retaliates brings NCPD attention.
8. **The Peralez political investment.** The propaganda server farm is a
   political asset, but it is also a visible entanglement with a mayoral
   campaign. A player can sell the servers, protect them, or expose them.
9. **Veterans vs recruits.** Military competence and tenure are status markers;
   Gunner's purge replaced competence with loyalty. A veteran captain and a
   Gunner loyalist will not agree on promotion.

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
identity enum and `Attitude_Record.hpp` is opaque. The stances below are judged
from quests, gigs, shards, wiki and spatial adjacency, not from a TweakDB
relation row. That is why every row carries a tag and why the neutral rows are
not claims of friendship.

| Faction | Code | Stance | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| Tyger Claws | `tyger_claws` | `rival` | Acorn Towers lot sits in Tyger Claws-flagged Charter Hill `[game-data]`; Kendal Park carries both a 6th Street community (2 entries) and a Tyger Claws community (4 entries) `[game-data]`; no lore feud attested `[inferred]` | `game-data+inferred` |
| Valentinos | `valentinos` | `war` | Turf war since at least 2071, escalated over Vista del Rey in 2074, "intensifying" in 2077 `[wiki]`; Sam Carter threatened them and was executed by Padre `[wiki]`; Nolan Frakes ordered the hit that wounded Martha `[wiki]`; game data: `ma_hey_gle_11`, `ma_hey_rey_05`, `sa_ep1_141_com_combat` (4 vs 4), `sa_ep1_135_com_combat` (4 vs 4 vs 4) `[game-data]` | `game-data+wiki` |
| Arasaka | `arasaka` | `neutral` | No 6th Street-specific Arasaka operation found; the Streetkid prologue's Arasaka car theft is Kirk Sawyer's job, not the gang's `[inferred]` | `inferred` |
| Militech | `militech` | `hostile` | Historical arms supplier `[wiki]`; the H6 cell "jumped a Militech transport" and jailbreaks corporate weapons `[wiki]` `[game-data]`; Gunner ordered the deaths of 6th Streeters held in a Militech prison `[wiki]` | `game-data+wiki` |
| Kang Tao | `kang_tao` | `hostile` | 6th Street mugged Karl Ginsky for a top-secret Kang Tao shard; Kang Tao agents move to recover it and kill the witnesses `[wiki]` `[game-data]` | `game-data+wiki` |
| Biotechnica | `biotechnica` | `trade` | Tina Agron stole proteins from Biotechnica Flats and sold them to 6th Street; Gunner tried to coerce a partnership, then ordered her death when she asked for Morton-era terms `[wiki]` | `wiki` |
| Petrochem | `petrochem` | `neutral` | No attested interaction; the Kendachi Almunecar factory sits in the Petrochem Freight Yard sub-territory, which is adjacency, not conflict `[game-data]` `[inferred]` | `game-data+inferred` |
| Barghest | `barghest` | `neutral` | No attested interaction; both appear as enemies in *Roads to Redemption*, but not against each other `[wiki]` `[inferred]` | `wiki+inferred` |
| Aldecaldos | `aldecaldos` | `trade` | "Extensive connections with nomad groups inside and outside Night City" `[wiki]`; Boz is the nomad-courier lieutenant `[wiki]`; *Going-away Party* uses an Aldecaldo smuggler `[wiki]` `[game-data]` | `game-data+wiki` |
| Wraiths | `wraiths` | `neutral` | No attested interaction; the Wraiths are the Aldecaldos' enemy, not 6th Street's `[inferred]` | `inferred` |
| Animals | `animals` | `neutral` | Santo Domingo co-residents; no attested conflict or deal `[inferred]` | `inferred` |
| The Mox | `the_mox` | `neutral` | No attested interaction; different districts `[inferred]` | `inferred` |
| Maelstrom | `maelstrom` | `neutral` | No attested interaction; the Maelstrom politics doc records only gang-watch encounters in Rancho/Arroyo `[game-data]` `[inferred]` | `game-data+inferred` |
| Voodoo Boys | `voodoo_boys` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| NCPD | `ncpd` | `hostile` | NCPD runs SOCA/scanner hustles against Darius Miles and Olga Longmead `[game-data]` `[wiki]`; the gang's founding goal was to replace the corrupt NCPD `[wiki]`; but the NCPD tolerates the gang's ersatz law unless it causes trouble outside its turf `[wiki]` | `game-data+wiki` |
| Night Corp | `night_corp` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| City Council | `city_council` | `trade` | 6th Street runs a server farm pumping pro-Peralez / anti-Holt propaganda (*Error 404*) `[game-data]` `[wiki]`; a political investment, payment not attested `[inferred]` | `game-data+wiki+inferred` |
| Scavengers | `scavengers` | `rival` | `{sa_ep1_135_com_combat}` is a four-way Glen street fight with 4 Scavengers, 4 6th Streeters, 4 Valentinos and 1 Arasaka `[game-data]`; both compete for Santo Domingo/Arroyo salvage `[wiki]` `[inferred]` | `game-data+wiki+inferred` |
| Regina Jones | `fixer_regina` | `neutral` | No 6th Street-specific gig found; her gigs are Watson `[inferred]` | `inferred` |
| Wakako Okada | `fixer_wakako` | `neutral` | No 6th Street-specific gig found `[inferred]` | `inferred` |
| Sebastian Ibarra (Padre) | `fixer_padre` | `hostile` | Padre executed Sam Carter for threatening him `[wiki]`; he is the Valentinos' patron and gig-runner `[wiki]`; he also accepted Nolan Frakes' contract on Gustavo, so a transactional channel exists `[wiki]` | `wiki` |
| Muamar Reyes (El Capitán) | `fixer_el_capitan` | `hostile` | He gives *Hacking the Hacker*, *Error 404*, *Breaking News*, *Serious Side Effects* and *Going-away Party*, all against 6th Street `[game-data]` `[wiki]` | `game-data+wiki` |
| Dakota Smith | `fixer_dakota` | `neutral` | No 6th Street-specific gig or lore link found; nomad logistics overlap only `[inferred]` | `inferred` |
| Dino Dinovic | `fixer_dino` | `neutral` | No 6th Street-specific gig or lore link found `[inferred]` | `inferred` |
| Rogue Amendiares | `fixer_rogue` | `hostile` | She gives *Nasty Hangover* (recover a Kang Tao shard from a 6th Street warehouse) and *Family Heirloom* (retrieve a bootleg from Wyatt Alken) `[game-data]` `[wiki]` | `game-data+wiki` |
| Mr. Hands | `fixer_mr_hands` | `hostile` | *Roads to Redemption* is his Dogtown gig, with 6th Street as enemies `[game-data]` `[wiki]` | `game-data+wiki` |
| Afterlife | `afterlife` | `neutral` | Neutral merc marketplace; Combat Cab is popular with edgerunners, but no formal relation `[wiki]` `[inferred]` | `wiki+inferred` |
| Kendachi | `kendachi` | `patron` | Historical supplier of weapons `[wiki]`; 6th Street "secretly cooperated with Kendachi to design a new line of weapons" `[wiki]`; the "Arsenal" shard is at the Kendachi Almunecar factory (site 381) `[game-data]` `[wiki]` | `game-data+wiki` |
| NUSA | `nusa` | `ally` | The infobox lists the FIA as an affiliation `[wiki]`; many members are Unification War veterans `[wiki]`; Gunner armed and briefed Solomon Reed and V for the MaxTac convoy raid in *Black Steel In The Hour of Chaos* `[wiki]`; the 26-unit pre-ambush company is the operation's base `[game-data]` | `game-data+wiki` |
| NetWatch | `netwatch` | `neutral` | No attested interaction `[inferred]` | `inferred` |

### 3.3 Actors outside `data/factions.json`

These are real relationships but have no faction code, so they are prose only.

- **Combat Cab** — a combat-taxi service affiliated with 6th Street and
  popular with edgerunners. It is the gang's most legitimate-looking business
  and a mobility asset, not a faction. `[wiki]`
- **The FIA** — the federal agency behind Reed's MaxTac operation. It is not a
  `factions.json` code; the NUSA row covers the relationship. Gunner's support
  is a covert one-off, not a public alliance. `[wiki]`
- **The Peralez campaign** — 6th Street's propaganda server farm supports
  Jefferson Peralez and attacks Weldon Holt. This is a political investment in
  a mayoral campaign, not an attested contract. `[wiki]`
- **Ted Fox / N54** — the reporter in *Breaking News* who wants to expose the
  Kendachi-6th Street weapons link. A media threat, not a faction. `[wiki]`
- **Tina Agron** — a Biotechnica Flats worker who stole proteins for the gang;
  Gunner ordered her death after she asked for a better cut. An individual
  channel, not a faction. `[wiki]`
- **Karl Ginsky** — the Kang Tao employee whose shard 6th Street stole in
  *Nasty Hangover*. An individual victim, not a faction. `[wiki]`
- **Jimmy Kreutz** — the race driver killed by Hilary McKenna's crew. An
  individual, not a faction. `[wiki]`
- **Coach Fred** — the fight promoter in *Beat on the Brat*; a one-off client,
  not a faction. `[wiki]`
- **Kirk Sawyer** — the small-time fixer in the Streetkid prologue; not a
  `factions.json` code and not a 6th Street relation. `[wiki]`

### 3.4 Guarantor assessment

This is the design question: if a player founds a gang, which factions would
guarantee 6th Street's support, and which would 6th Street itself guarantee?

- **The only `patron` is Kendachi.** It supplies weapons and co-runs the secret
  "Arsenal" line. That is the gang's most valuable external relationship and
  its biggest ideological liability.
- **The only `ally` is NUSA, and it is a one-off.** Gunner supports Reed's
  MaxTac operation with equipment and intel. That is a covert operation, not a
  standing security guarantee.
- **The transactional guarantors are real but narrow:** the Aldecaldos
  (logistics and extraction), Biotechnica's black market (stolen proteins), the
  City Council/Peralez campaign (political cover), and Combat Cab (mobility).
- **No other gang is an ally.** The Valentinos are at war; the Tyger Claws and
  Scavengers are rivals; the rest are neutral placeholders.

**6th Street as a guarantor.** A player who takes over 6th Street inherits:

- a two-front war (Valentinos in Vista del Rey/the Glen, NCPD pressure
  everywhere),
- the Morton purge legacy (Flavio, the old guard's surviving sympathizers,
  Pablo Silva's scapegoating),
- the Kendachi dependency (a corporate patron with a secret to leak),
- a revenue base that is illegal, geographically concentrated and
  labor-intensive to protect.

What 6th Street can actually guarantee is **protection, military training,
vehicles and an ersatz-law umbrella** in Santo Domingo and the Glen. What it
cannot guarantee is peace with the Valentinos, NCPD neutrality, or freedom from
fixer contracts.

**Plausible guarantors for a player-founded gang** are therefore transactional:
Kendachi (arms), the Aldecaldos (logistics), Combat Cab (mobility), a
Peralez-style political patron (cover), or a corrupt NCPD officer (tolerance,
inferred from the gang's de facto law-enforcement role, not attested as a
specific channel). Not the Valentinos, not the NCPD as an institution, not
Arasaka.

**6th Street as an aggressor.** The gang is an expansionist paramilitary with a
standing war and a doctrine of "bringing justice" to its neighborhoods. For a
player founding a gang on a 6th Street-adjacent point, 6th Street is more
likely to be the **pre-emptive attacker** than the guarantor, especially in
Santo Domingo and the Glen. That is consistent with its `war`/`rival`/`hostile`
rows.

---

## 4. Pillar notes

Design claims from `docs/design/gameplay-systems.md`: 6th Street is a
**Paramilitary Organization** (archetype strength Military, weakness Economy);
faction strength **Culture**, weakness **Politics**.

| Pillar | Design claim | Lore verdict | Evidence |
| --- | --- | --- | --- |
| Military (archetype strength) | 6th Street is a military organization | **Strongly supported, but militia-grade.** Founders were Fourth Corporate War veterans; 2070s ranks are Unification War veterans, retired military and discharged corporate security; civilians get crash training. The gang uses military ranks, tactical gear, armories, convoys, snipers and heavy weapons. It hijacks Militech transports and fields a 26-unit ambush company. But it is not a professional army: it loses to NCPD raids and fixer-hired mercs, and its frontier cells are small. | Wiki *6th Street*, *Will Gunner*; `Character.q305_gunner`; `{q305_com_6th_street_pre_ambush}` 26; site 384 15; sniper records `arr_sixthstreet_sniper2_*` `[wiki]` `[game-data]` |
| Economy (archetype weakness) | 6th Street is economically weak | **Supported with a correction.** The gang is not poor: protection, arms, drugs, vehicles, smuggling, media, Combat Cab and betting produce real gross revenue. But it is structurally weak: the 2040s lore says it was "losing money really fast" and had to move into extortion and smuggling; it has no legitimate finance, depends on corporate suppliers (Militech, Kendachi) and nomad logistics, and must police the turf it taxes. Model it as **high illegal gross, low margin, high dependency**, not "no income." | Wiki *6th Street* history; revenue sites 379/382/389/368/381/125 `[wiki]` `[game-data]` |
| Culture (faction strength) | 6th Street binds through culture | **Strongly supported, but split.** Patriotic NUSA iconography, stars and stripes, "bring justice," neighborhood allegiance, military rituals, parties for Gunner, the Stadium Love contest, the "General" cult. The culture binds the heartland and the captains, but it fractures over the corporate question: the 2076 schism was a cultural civil war, and Gunner's secret Kendachi deal contradicts the official creed. | Wiki *6th Street* overview and Behind the Scenes; *Stadium Love*; *6th Street Members* `[wiki]` |
| Politics (faction weakness) | 6th Street cannot do politics | **Strongly supported.** A coup, a purge, a scapegoat, no allies, a two-front war, rogue cells outside the General's control, and fixers running contracts against the gang. The one political asset is the ersatz-law legitimacy and the Peralez propaganda channel, both fragile. The weakness is **personalized, violent politics**, not the absence of politics. | Coup and purge; Olga outside Gunner's control; Nolan's private vendetta; El Capitán/Rogue/Mr. Hands gigs `[wiki]` `[game-data]` |
| Overall fit | The pillars fit the faction | **Good.** Keep Military strong and Politics weak. Treat Economy as "illegal, dependency-heavy and fragile," and Culture as "high internal cohesion, split over corporations." The coup is the proof of the Politics weakness, not an exception. | Synthesis of the rows above `[inferred]` |

Design cautions, not redesigns:

- Do **not** model 6th Street as a poor gang. Model it as a gang with a real
  illegal economy and a structural margin problem.
- Do **not** model Politics as zero. The ersatz-law role and the Peralez
  channel are real political assets; losing them should hurt more than losing a
  generic business.
- The anti-corporate creed is a **legitimacy mechanic**, not just flavor. A
  player who exposes the Kendachi deal should be able to collapse Gunner's
  regime without a boss fight.
- The captain/company structure is a **parallel ladder**. A player can rise
  through a captain rather than through the General, and a popular captain is a
  credible coup leader.

---

## 5. Gaps and uncertainties

1. **No offline attitude matrix.** `refs/RED4ext.SDK/.../game/data/Attitude_Record.hpp`
   is opaque and `Affiliation.hpp` is identity only. Every stance in §3.2 is
   judged from quests, gigs, shards, wiki and spatial adjacency; none is read
   from a TweakDB relation table.
2. **Most named leaders are not in `data/sites/rosters.json`.** The precise
   named records are Lucius, Wyatt, Hilary, Darius (inferred), Olga (inferred),
   Sherman (inferred), Flavio (faction `null`) and Gunner (`q305`); Morton,
   Pablo, Nolan, Boz, Buck, Walker and Sam Carter have no 2077 actor record.
3. **Several records are inferred, not exact.** Darius
   (`ma_std_arr_03_outpost_miniboss`), Olga
   (`ma_std_rcr_08_outpost_miniboss`), Sherman
   (`mq008_6th_street_representative`) and Walker (`mq008_6th_street_male`)
   are one-record deductions and need an in-game check before seeding.
4. **Gunner has no site or marker.** The PL abandoned hotel/skybridge is
   anchored on the area `{q305_com_6th_street_pre_ambush}` at
   `(-2758.2, -2466.5, 17.3)`, not on a `sites.json` row. There is no
   `q305_prison_convoy` site row in the extract.
5. **The wiki's "Arroyo HQ" is a red link.** *Arroyo HQ*, *Old C-Team HQ* and
   *Pig Boy's Delight Irish Pub* have no page, marker, site or community. The
   verified substitute is the Megabuilding H6 hideout (site 384), as argued in
   [`../sixth-street.md`](../sixth-street.md) §5.
6. **Story actors will not spawn with the campaign disabled.** Gunner
   (`q305`), Sam Carter (`q000_street_kid`) and the PL ambush company are
   story-gated. The `world-activity` rows are the best reuse candidates, but
   gigs and scanner hustles may also be suppressed by the mod.
7. **Many leaders are "dependent."** Wyatt, Buck, Hilary, Olga, Darius, Lucius
   and Martha are marked dependent because their survival depends on V. A
   simulation must choose a branch or model the branches explicitly.
8. **Name collisions.** `Patricia Gerville` (6th Street) is not Maelstrom's
   Patricia Sirawian; the string `Patricia` also appears in a 6th Street
   warehouse record. `Sherman` is a Texas city page; `Walker` matches many
   unrelated records; `Boz` matches a Scavenger community entry
   (`{sts_ep1_03_boss_com}`), not a 6th Street spawn.
9. **Flavio's record is `faction_id: null`.** He is a quest ally, not a 6th
   Street unit. Do not count him as a garrison.
10. **The `mq008` communities are phases of one party.** `mq008_com_shooting`
    (14), `mq008_com_6th_street_party` (6), `mq008_com_representative` (1) and
    `mq008_com_background` (1) overlap; do not sum them.
11. **No per-clique membership counts.** The site and area counts are presence
    proxies, not rolls. The heartland and frontier totals also overlap with
    generic street spawns.
12. **The corporate-pragmatist bloc is inferred.** Its named leaders are dead
    (Morton, Pablo) or fugitive (Flavio). The bloc is a policy tendency visible
    in the 2076 schism and the Tina Agron channel, not an organized faction.
13. **The Kendachi "Arsenal" is a secret, and the factory is Kendachi's.** Site
    381 has zero 6th Street roster units; it is a partner facility, not gang
    territory. The relationship is `patron`, not ownership.
14. **The Peralez propaganda is attested; payment is not.** *Error 404* proves
    the server farm and the pro-Peralez line. It does not prove a contract,
    a payment or coordination with the campaign. The city_council stance is
    `trade` on the strength of the political investment, flagged `[inferred]`.
15. **NUSA/FIA is one covert operation.** Gunner's support for Reed is real,
    but it is a single PL main-job operation, not a standing alliance. The
    `ally` stance is the closest fit and is deliberately narrow.
16. **The 2045 lore is Cyberpunk RED, not 2077.** The Armory, Davis Squad, the
    3-I's, X's 2/3 vote and the monthly cyberware rule have no 2077 records.
    They are useful for a succession model, not for spawning.
17. **Neutral rows are placeholders.** Arasaka, Petrochem, Barghest, Wraiths,
    Animals, the Mox, Maelstrom, Voodoo Boys, Night Corp, NetWatch, Regina,
    Wakako, Dakota, Dino and Afterlife have no attested 6th Street interaction.
    Do not promote them without a source.
18. **`areas.jsonl.district_code` is unsafe.** The `sa_ep1_135` and `q305`
    rows are attributed by geocoded community names and coordinates, not by
    `district_code`; never aggregate by that field.
19. **`sub_territory_id` is a coarse bucket.** Site 384's `sub_territory_id`
    is 53 "Kendachi Foundry," but the hideout is the Megabuilding H6 floor on
    MLK Blvd. Attribute by coordinates.
20. **The wiki's ≈2,300 members is a world-book figure.** The extract has 183
    roster units at 29 sites. Neither number is a membership roll.
21. **Hilary McKenna's site and street do not match exactly.** Her record
    (`Character.ma_std_arr_09_hilary`) is at site 131 `ma_std_arr_09`, a
    five-unit Red Dirt Crossroads car hustle at `(-883.5, -1008.3)`, while the
    wiki places her autoshop on Mission Street. The record name is exact; the
    shop's map location is inferred from the site, not independently verified.
22. **Martha Frakes' *Heroes* appearance is a disguise.** She appears as
    "Martha Young" and is later comatose; do not treat her as an active member
    in 2077. The game files identify "Martha Young" as Gustavo's girlfriend.

### 5.1 Sources consulted

Local:

- `data/factions.json`, `data/districts.json`, `data/sub_territories.json`,
  `data/control_centers.json`, `data/spawn_points.json`.
- `data/sites/{sites,rosters,communities,guards,triggers,spots,patrols,doors,suitabilities}.json`.
- `dist/extract/areas.jsonl`, `dist/extract/markers.jsonl`,
  `dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_{0,1,2}.streamingsector.json`
  (community registry templates and `characterRecordId` values).
- `refs/RED4ext.SDK/.../game/data/Affiliation.hpp`,
  `refs/RED4ext.SDK/.../game/data/Attitude_Record.hpp`.

Wiki (MediaWiki API, infoboxes and quest bodies):

- Organization: [6th Street](https://cyberpunk.fandom.com/wiki/6th_Street),
  [6th Street Members](https://cyberpunk.fandom.com/wiki/6th_Street_Members),
  [Will Gunner](https://cyberpunk.fandom.com/wiki/Will_Gunner),
  [Rick Morton](https://cyberpunk.fandom.com/wiki/Rick_Morton),
  [Solomon Wright](https://cyberpunk.fandom.com/wiki/Solomon_Wright),
  [Arbiter](https://cyberpunk.fandom.com/wiki/Arbiter),
  [Pablo Silva](https://cyberpunk.fandom.com/wiki/Pablo_Silva),
  [Flavio dos Santos](https://cyberpunk.fandom.com/wiki/Flavio_dos_Santos),
  [Boz](https://cyberpunk.fandom.com/wiki/Boz),
  [Sam Carter](https://cyberpunk.fandom.com/wiki/Sam_Carter),
  [Martha Frakes](https://cyberpunk.fandom.com/wiki/Martha_Frakes),
  [Nolan Frakes](https://cyberpunk.fandom.com/wiki/Nolan_Frakes),
  [Lucius Thoran](https://cyberpunk.fandom.com/wiki/Lucius_Thoran),
  [Darius Miles](https://cyberpunk.fandom.com/wiki/Darius_Miles),
  [Olga Elisabeth Longmead](https://cyberpunk.fandom.com/wiki/Olga_Elisabeth_Longmead),
  [Wyatt Alken](https://cyberpunk.fandom.com/wiki/Wyatt_Alken),
  [Hilary McKenna](https://cyberpunk.fandom.com/wiki/Hilary_McKenna),
  [Buck Arnold](https://cyberpunk.fandom.com/wiki/Buck_Arnold),
  [Jake Estevez](https://cyberpunk.fandom.com/wiki/Jake_Estevez),
  [Matt Dodges](https://cyberpunk.fandom.com/wiki/Matt_Dodges),
  [Patricia Gerville](https://cyberpunk.fandom.com/wiki/Patricia_Gerville),
  [Kendachi](https://cyberpunk.fandom.com/wiki/Kendachi).
- Quests and gigs:
  [Stadium Love](https://cyberpunk.fandom.com/wiki/Stadium_Love),
  [Beat on the Brat: Arroyo](https://cyberpunk.fandom.com/wiki/Beat_on_the_Brat:_Arroyo),
  [Gig: Hacking the Hacker](https://cyberpunk.fandom.com/wiki/Gig:_Hacking_the_Hacker),
  [Gig: Serious Side Effects](https://cyberpunk.fandom.com/wiki/Gig:_Serious_Side_Effects),
  [Gig: Error 404](https://cyberpunk.fandom.com/wiki/Gig:_Error_404),
  [Gig: Breaking News](https://cyberpunk.fandom.com/wiki/Gig:_Breaking_News),
  [Gig: Nasty Hangover](https://cyberpunk.fandom.com/wiki/Gig:_Nasty_Hangover),
  [Gig: Family Heirloom](https://cyberpunk.fandom.com/wiki/Gig:_Family_Heirloom),
  [Gig: Life's Work](https://cyberpunk.fandom.com/wiki/Gig:_Life%27s_Work),
  [Gig: Going-away Party](https://cyberpunk.fandom.com/wiki/Gig:_Going-away_Party),
  [Gig: Bring Me the Head of Gustavo Orta](https://cyberpunk.fandom.com/wiki/Gig:_Bring_Me_the_Head_of_Gustavo_Orta),
  [Gig: Roads to Redemption](https://cyberpunk.fandom.com/wiki/Gig:_Roads_to_Redemption),
  [Suspected Organized Crime Activity (Arroyo)](https://cyberpunk.fandom.com/wiki/Suspected_Organized_Crime_Activity_(Arroyo)),
  [Suspected Organized Crime Activity: New Boss, New Rules](https://cyberpunk.fandom.com/wiki/Suspected_Organized_Crime_Activity:_New_Boss,_New_Rules),
  [Black Steel In The Hour of Chaos](https://cyberpunk.fandom.com/wiki/Black_Steel_In_The_Hour_of_Chaos),
  [The Streetkid](https://cyberpunk.fandom.com/wiki/The_Streetkid),
  [Archived Conversation: Will Gunner and Amos Licameli](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Will_Gunner_and_Amos_Licameli).
- Earlier repo research: [`../sixth-street.md`](../sixth-street.md),
  [`../METHOD.md`](../METHOD.md), [`./METHOD.md`](./METHOD.md),
  [`./maelstrom.md`](./maelstrom.md), [`./valentinos.md`](./valentinos.md),
  `docs/design/gameplay-systems.md`.

---

## 6. Machine-readable block

```json
{
  "faction_code": "sixth_street",
  "leaders": [
    {
      "name": "Will Gunner",
      "role": "General (2076-present; seized power in a coup)",
      "character_record_id": "Character.q305_gunner",
      "location_name": "Pre-ambush staging, abandoned hotel overlooking the skybridge, West Wind Estate, Pacifica",
      "open_world": false,
      "source": "raw always_loaded_1 communitySpawnEntry entryName gunner, characterRecordId Character.q305_gunner, appearance man_average__q305__6thstreet_officer, phase start, spot #q305_ws_pre_ambush_gunner_start; area {q305_com_6th_street_pre_ambush} at -2758.2,-2466.5,17.3; wiki Will Gunner",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Rick Morton",
      "role": "Former General (unknown-2076); killed in Gunner's coup for siding with corporations",
      "character_record_id": null,
      "location_name": null,
      "open_world": false,
      "source": "wiki Rick Morton; wiki 6th Street Members",
      "confidence": "wiki"
    },
    {
      "name": "Captain Sherman",
      "role": "Captain of a Rancho Coronado company; Walker's CO; hosts Gunner's ascension party (V-dependent)",
      "character_record_id": "Character.mq008_6th_street_representative",
      "location_name": "Stadium Love rooftop, Rancho Coronado",
      "open_world": true,
      "source": "raw mq008 community template uses generic Character.mq008_6th_street_representative and Character.mq008_6th_street_male records; markers mq008_01_sm_party_chats at 495.7,-2143.4,27.3 and mq008_02_sm_shooting_contest at 503.0,-2128.7,27.4; wiki Stadium Love; inferred",
      "confidence": "game-data+inferred+wiki"
    },
    {
      "name": "Lucius Thoran",
      "role": "Techie and H6 cell technical chief; stole a corporate weapon; El Capitan's target (V-dependent)",
      "character_record_id": "Character.sts_std_arr_11_lucius",
      "location_name": "6th Street hideout, Megabuilding H6 floor 19, Arroyo",
      "open_world": true,
      "source": "data/sites/rosters.json site 384 sts_std_arr_11 record Character.sts_std_arr_11_lucius; site anchor -199.039,-843.481,259.170; wiki Lucius Thoran; gig Hacking the Hacker",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Darius Miles",
      "role": "Drug-ring leader (beta acid); NCPD most-wanted (V-dependent)",
      "character_record_id": "Character.ma_std_arr_03_outpost_miniboss",
      "location_name": "Darius Miles' drug lab, Hargreaves St, Arroyo",
      "open_world": true,
      "source": "data/sites/rosters.json site 125 ma_std_arr_03 entry #enemy05 role boss; site anchor -614.238,-1038.144,7.390; NCPD dispatch names Darius Miles; wiki Darius Miles; inferred",
      "confidence": "game-data+inferred+wiki"
    },
    {
      "name": "Olga Elisabeth Longmead",
      "role": "Rogue cell leader; kidnapping and two murders; operates outside Gunner's control (V-dependent)",
      "character_record_id": "Character.ma_std_rcr_08_outpost_miniboss",
      "location_name": "Two-storey house on Carnitas St, Rancho Coronado",
      "open_world": true,
      "source": "data/sites/rosters.json site 153 ma_std_rcr_08 entry miniboss role boss; site anchor -156.981,-2169.689,5.782; NCPD dispatch New Boss, New Rules; wiki Olga Elisabeth Longmead; inferred",
      "confidence": "game-data+inferred+wiki"
    },
    {
      "name": "Nolan Frakes",
      "role": "Senior member; Valentinos-war hardliner; ordered the hit on Gustavo Orta",
      "character_record_id": null,
      "location_name": null,
      "open_world": false,
      "source": "wiki Nolan Frakes; gig Bring Me the Head of Gustavo Orta",
      "confidence": "wiki"
    },
    {
      "name": "Wyatt Alken",
      "role": "Car thief and fence; guards a Samurai bootleg at the Acorn Towers lot (V-dependent)",
      "character_record_id": "Character.sts_wbr_hil_06_wyatt_alken",
      "location_name": "Acorn Towers parking lot, Crockett St, Charter Hill",
      "open_world": true,
      "source": "data/sites/rosters.json site 416 sts_wbr_hil_06; site anchor 375.332,-400.129,2.646; wiki Wyatt Alken; gig Family Heirloom",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Flavio dos Santos",
      "role": "Ex-member and Morton loyalist; fugitive from Gunner's purge",
      "character_record_id": "Character.sts_std_rcr_03_flavio",
      "location_name": "Flavio's house, Mallagra St, Rancho Coronado",
      "open_world": true,
      "source": "data/sites/rosters.json site 388 sts_std_rcr_03 entry flavio, phase #rcr_03_ws_flavio_appear, faction_id null; site anchor 446.939,-1267.613,28.730; wiki Flavio dos Santos; gig Going-away Party",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Hilary McKenna",
      "role": "Auto-shop owner on Mission Street; Assault in Progress target (V-dependent)",
      "character_record_id": "Character.ma_std_arr_09_hilary",
      "location_name": "Mission Street autoshop, Arroyo",
      "open_world": true,
      "source": "data/sites/rosters.json site 131 ma_std_arr_09; site anchor -883.503,-1008.289,11.553; wiki Hilary McKenna",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Sam Carter",
      "role": "Member in the Streetkid prologue; tried to push the Valentinos out of Vista del Rey; executed by Padre",
      "character_record_id": null,
      "location_name": "Vista del Rey / the prologue ride through the Glen",
      "open_world": false,
      "source": "wiki Sam Carter; The Streetkid; 6th Street Members",
      "confidence": "wiki"
    },
    {
      "name": "Pablo Silva",
      "role": "Former high-ranking member; scapegoated for Morton's death and murdered",
      "character_record_id": null,
      "location_name": null,
      "open_world": false,
      "source": "wiki Pablo Silva; shard Sent to 47 users",
      "confidence": "wiki"
    }
  ],
  "internal_factions": [
    {
      "name": "Gunner's coup regime (anti-corporate patriots)",
      "leader": "Will Gunner",
      "goals": "Anti-corporate purity, purge Morton loyalists, territorial expansion, patriotic legitimacy",
      "members_hint": "q305_com_6th_street_pre_ambush 26; Gunner appearance man_average__q305__6thstreet_officer; the prison and Militech channels used by the purge",
      "source": "wiki 6th Street history and Will Gunner; q305 community",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Morton's purged old guard (corporate pragmatists)",
      "leader": "Rick Morton (dead); Pablo Silva (dead); Flavio dos Santos (fugitive)",
      "goals": "Restore the old arrangement, keep corporate deals, survive the purge",
      "members_hint": "No active community; Flavio at site 388 (faction_id null); Pablo dead; Tina Agron's protein channel cancelled",
      "source": "wiki Rick Morton, Pablo Silva, Flavio dos Santos, Will Gunner; archived conversations",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Field captains and the patriotic street culture",
      "leader": "Captain Sherman; Walker; Buck Arnold",
      "goals": "Prestige, fighting, turf, recruitment, Gunner's cult of personality",
      "members_hint": "mq008_com_shooting 14, mq008_com_6th_street_party 6, mq008_com_representative 1, mq008_com_background 1; captain records at sites 153 and 154",
      "source": "wiki Stadium Love, Beat on the Brat, 6th Street Members; game-data mq008 communities",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Technical-economic wing (techies, garages, labs)",
      "leader": "Lucius Thoran; site officers",
      "goals": "Arms jailbreaking, Kendachi Arsenal, vehicle work, drug production, fencing",
      "members_hint": "sites 384 15, 389 15, 125 13, 416 12, 382 10, 368 8, 379 6, 131 5",
      "source": "gigs Hacking the Hacker, Serious Side Effects, Error 404, Nasty Hangover, Family Heirloom, Life's Work; wiki",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Rogue frontier cells",
      "leader": "Olga Longmead; Darius Miles",
      "goals": "Personal profit, kidnapping and ransom, drug rings, autonomy outside Gunner's control",
      "members_hint": "site 153 13 (Olga), site 125 13 (Darius); separate communities with their own bosses",
      "source": "NCPD dispatches New Boss, New Rules and SOCA Arroyo; wiki Olga Elisabeth Longmead and Darius Miles",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Valentinos-war hardliners",
      "leader": "Nolan Frakes; Sam Carter (dead)",
      "goals": "Escalate the Vista del Rey war, avenge Martha, push the Valentinos out",
      "members_hint": "site 57 ma_hey_gle_11 4; site 65 ma_hey_rey_05 4; sa_ep1_135_com_combat 4 vs 4 vs 4",
      "source": "wiki Nolan Frakes, Sam Carter, Bring Me the Head of Gustavo Orta; politics/valentinos.md",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Outlying chapters (Glen, Charter Hill, Vista del Rey)",
      "leader": "Local officers (Wicked Tires, Acorn Towers)",
      "goals": "Hold revenue outposts in rival districts; survive without heartland support",
      "members_hint": "site 368 Glen 8; site 416 Charter Hill 12; site 65 Vista del Rey 4; site 47 Glen 6",
      "source": "wiki 6th Street (local HQs); game-data sites 368, 416, 65, 47",
      "confidence": "game-data+wiki"
    }
  ],
  "relations": [
    {
      "faction_code": "tyger_claws",
      "stance": "rival",
      "evidence": "Acorn Towers lot sits in Tyger Claws-flagged Charter Hill [game-data]; Kendal Park carries both a 6th Street community (2 entries) and a Tyger Claws community (4 entries) [game-data]; no lore feud attested [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "valentinos",
      "stance": "war",
      "evidence": "Turf war since at least 2071, escalated over Vista del Rey in 2074, intensifying in 2077 [wiki]; Sam Carter threatened them and was executed by Padre [wiki]; Nolan Frakes ordered the hit that wounded Martha [wiki]; game data ma_hey_gle_11, ma_hey_rey_05, sa_ep1_141_com_combat (4 vs 4), sa_ep1_135_com_combat (4 vs 4 vs 4) [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "arasaka",
      "stance": "neutral",
      "evidence": "No 6th Street-specific Arasaka operation found; the Streetkid prologue's Arasaka car theft is Kirk Sawyer's job, not the gang's [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "militech",
      "stance": "hostile",
      "evidence": "Historical arms supplier [wiki]; the H6 cell jumped a Militech transport and jailbreaks corporate weapons [wiki] [game-data]; Gunner ordered the deaths of 6th Streeters held in a Militech prison [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "kang_tao",
      "stance": "hostile",
      "evidence": "6th Street mugged Karl Ginsky for a top-secret Kang Tao shard; Kang Tao agents move to recover it and kill the witnesses [wiki] [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "biotechnica",
      "stance": "trade",
      "evidence": "Tina Agron stole proteins from Biotechnica Flats and sold them to 6th Street; Gunner tried to coerce a partnership, then ordered her death when she asked for Morton-era terms [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "petrochem",
      "stance": "neutral",
      "evidence": "No attested interaction; the Kendachi Almunecar factory sits in the Petrochem Freight Yard sub-territory, which is adjacency, not conflict [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "barghest",
      "stance": "neutral",
      "evidence": "No attested interaction; both appear as enemies in Roads to Redemption, but not against each other [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "aldecaldos",
      "stance": "trade",
      "evidence": "Extensive connections with nomad groups inside and outside Night City [wiki]; Boz is the nomad-courier lieutenant [wiki]; Going-away Party uses an Aldecaldo smuggler [wiki] [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "wraiths",
      "stance": "neutral",
      "evidence": "No attested interaction; the Wraiths are the Aldecaldos' enemy, not 6th Street's [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "animals",
      "stance": "neutral",
      "evidence": "Santo Domingo co-residents; no attested conflict or deal [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "the_mox",
      "stance": "neutral",
      "evidence": "No attested interaction; different districts [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "maelstrom",
      "stance": "neutral",
      "evidence": "No attested interaction; the Maelstrom politics doc records only gang-watch encounters in Rancho/Arroyo [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "voodoo_boys",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "ncpd",
      "stance": "hostile",
      "evidence": "NCPD runs SOCA/scanner hustles against Darius Miles and Olga Longmead [game-data] [wiki]; the gang's founding goal was to replace the corrupt NCPD [wiki]; but the NCPD tolerates the gang's ersatz law unless it causes trouble outside its turf [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "night_corp",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "city_council",
      "stance": "trade",
      "evidence": "6th Street runs a server farm pumping pro-Peralez / anti-Holt propaganda (Error 404) [game-data] [wiki]; a political investment, payment not attested [inferred]",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "faction_code": "scavengers",
      "stance": "rival",
      "evidence": "sa_ep1_135_com_combat is a four-way Glen street fight with 4 Scavengers, 4 6th Streeters, 4 Valentinos and 1 Arasaka [game-data]; both compete for Santo Domingo/Arroyo salvage [wiki] [inferred]",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "faction_code": "fixer_regina",
      "stance": "neutral",
      "evidence": "No 6th Street-specific gig found; her gigs are Watson [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_wakako",
      "stance": "neutral",
      "evidence": "No 6th Street-specific gig found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_padre",
      "stance": "hostile",
      "evidence": "Padre executed Sam Carter for threatening him [wiki]; he is the Valentinos' patron and gig-runner [wiki]; he also accepted Nolan Frakes' contract on Gustavo, so a transactional channel exists [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "fixer_el_capitan",
      "stance": "hostile",
      "evidence": "He gives Hacking the Hacker, Error 404, Breaking News, Serious Side Effects and Going-away Party, all against 6th Street [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_dakota",
      "stance": "neutral",
      "evidence": "No 6th Street-specific gig or lore link found; nomad logistics overlap only [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_dino",
      "stance": "neutral",
      "evidence": "No 6th Street-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_rogue",
      "stance": "hostile",
      "evidence": "She gives Nasty Hangover (recover a Kang Tao shard from a 6th Street warehouse) and Family Heirloom (retrieve a bootleg from Wyatt Alken) [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_mr_hands",
      "stance": "hostile",
      "evidence": "Roads to Redemption is his Dogtown gig, with 6th Street as enemies [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "afterlife",
      "stance": "neutral",
      "evidence": "Neutral merc marketplace; Combat Cab is popular with edgerunners, but no formal relation [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "kendachi",
      "stance": "patron",
      "evidence": "Historical supplier of weapons [wiki]; 6th Street secretly cooperated with Kendachi to design a new line of weapons [wiki]; the Arsenal shard is at the Kendachi Almunecar factory (site 381) [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "nusa",
      "stance": "ally",
      "evidence": "The infobox lists the FIA as an affiliation [wiki]; many members are Unification War veterans [wiki]; Gunner armed and briefed Solomon Reed and V for the MaxTac convoy raid in Black Steel In The Hour of Chaos [wiki]; the 26-unit pre-ambush company is the operation's base [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "netwatch",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    }
  ]
}
```
