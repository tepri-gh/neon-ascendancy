# Arasaka — Leadership, Internal Politics and External Relations

Status: faction politics research run, 2026-11-25. One faction, one document.
Scope: Cyberpunk 2077 2.5 + Phantom Liberty, campaign disabled. This document
covers who a player can join under, climb past, ally with or remove inside
Arasaka; the corporate blocs; and the external-relations matrix needed for
wars, alliances and "guarantor" support when a player founds an organisation.

Method: this document follows the evidence rules in
[`METHOD.md`](./METHOD.md) and the data pitfalls in
[`../METHOD.md`](../METHOD.md) §1.1–§1.2. The location catalogue for Arasaka is
[`../arasaka.md`](../arasaka.md); this document does not repeat it — it maps
people and politics onto those places.

A corporation is not a gang. Three adjustments are used throughout and are
flagged again in §5:

- **Leadership is a hierarchy, not a leader list.** The Arasaka family, the
  board, the regional directors and the security chiefs are all "leadership";
  only some have character records.
- **The best wiki source is the employee list, not `<Faction> Members`.** The
  `List of Arasaka employees` page is the compact named-member table for a corp.
- **"Dependent" is the normal 2077 state.** The wiki marks most Arasaka leaders
  as dependent on V's choices. The branches are recorded, not silently chosen.

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Position, site, community, roster or raw-registry record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/comic/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My reasoning links a named person, place or stance to a record; reasoning stated | Weak, flagged |

Extra convention for this document only: **presence class**.
`ambient` = persists in free roam without a quest; `world-activity` = gig,
scanner hustle or NCPD activity; `story` = gated by a main or side quest;
`prologue` = the Corpo lifepath prologue, story-gated; `historical` = not
present in 2077. The JSON `open_world` flag is `true` only for `ambient` and
`world-activity`. Every named Arasaka leader below is `story`, `prologue` or
`historical`, so **no named leader is open-world**.

---

## 1. Leadership and ranks

### 1.1 The 2077 chain of command

Arasaka is a family-controlled public corporation: the Arasaka family holds
54% of the shares, the board holds 15%, and 31% trades publicly. The family
chairman is the real sovereign; the CEO is an operator. The 2077 top is
unusually unstable because Saburo is murdered in *The Heist* and three family
blocs claim the succession.

| Name | 2077 role | Character record | Location / influence point | Presence class | Source | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| **Saburo Arasaka** | Chairman (1960–2077); CEO (1960–late 1990s, again 2023–2077); engram in Mikoshi | `Character.Saburo` | Konpeki Plaza penthouse; Arasaka Tower (Saburo's office, Mikoshi) | `story` | Raw registry phases `q005_*`, `q101_*`; markers `q005_mrk_saburo_av_open_int`, `q113_06_sm_saburo_office`, `q113_07_sm_mikoshi`; wiki *Saburo Arasaka* | `[game-data]` `[wiki]` |
| **Yorinobu Arasaka** | CEO (2077, after murdering Saburo); Taka faction leader | `Character.Yorinobu` | Konpeki Plaza suite; Arasaka Tower CEO floor | `story` | Raw registry phases `q004_*`, `q005_*`, `q113_yorinobu_14_office*`; markers `mirror_sm_scene_konpeki_room`, `q113_12_sm_ceo_floor`, `q113_14_sm_yorinobu`; wiki *Yorinobu Arasaka* | `[game-data]` `[wiki]` |
| **Hanako Arasaka** | Kiji faction head; legitimist claimant; unofficial spokeswoman | `Character.Hanako` | Arasaka Estate (North Oak); Japantown parade; Arasaka Tower | `story` | Raw registry phases `q112_hanako_*`, `q113_hanako_*`, `q201_ws_hanako_*`; markers `q113_04_sm_hanako_estate`, `q112_08_sm_parade_speech`, `q115_00b_sm_hanako`; wiki *Hanako Arasaka* | `[game-data]` `[wiki]` |
| **Michiko Arasaka (Sanderson)** | Hato faction head; board member | `Character.Michiko` | Arasaka Tower (boardroom / jungle level) | `story` | Raw registry phases `q113_michiko_09_jungle*`, `#q113_michiko_10_jungle_combat`; marker `q113_10_sm_jungle_combat`; wiki *Michiko Arasaka (Kei's daughter)* | `[game-data]` `[wiki]` |
| **Kei Arasaka** | CEO (late 1990s–2023); deceased | — (no 2077 record) | — | `historical` | Wiki *Kei Arasaka*; Arasaka employee list | `[wiki]` `[lore]` |
| **Goro Takemura** | Saburo's personal bodyguard; ex-special forces | `Character.Takemura` | Konpeki Plaza; Japantown; Arasaka Industrial Park; Arasaka Estate; Arasaka Tower | `story` | Raw registry phases `q005_*`, `q101_*`, `q104_*`, `q112_*`; markers `q101_08_sm_takemura`, `q112_04_sm_takemura`; wiki *Goro Takemura* | `[game-data]` `[wiki]` |
| **Adam Smasher** | Yorinobu's bodyguard; Head of Security after Saburo's murder; enforcer | `Character.Smasher` (boss variants `Character.q113_boss_smasher`, `Character.main_boss_adam_smasher`) | Konpeki Plaza; Arasaka Tower (CEO floor, Mikoshi); Ebunike Docks (base, via Grayson) | `story` | Raw registry phases `q005_*`, `q101_*`, `q108_atlantis_bar`, `q112_safe_house_start`; markers `q113_13_sm_adam_smasher`, `smasher_marker`, `q005_14_sm_escape_smasher`; wiki *Adam Smasher* | `[game-data]` `[wiki]` |
| **Sandayu Oda** | Hanako's bodyguard; cyberninja | `Character.Cyberninja_Oda` | Japantown parade; Arasaka Tower | `story` | Raw registry phases `q112_cyberninja_08_bossfight`, `q112_cyberninja_oda_stealth`; marker `q112_00b_sm_secret_meeting_oda_car`; wiki *Sandayu Oda* | `[game-data]` `[wiki]` |
| **Anders Hellman** | Relic project director; defected to Kang Tao | `Character.Haru_Kasai` (development alias; wiki note) | Kang Tao AV crash (Jackson Plains); Sunset Motel; Arasaka Estate; Arasaka Orbital Station | `story` | Raw registry entries `haru`, `anders_hellman_holo`; phases `q004_*`, `q005_*`, `q101_*`, `q104_*`; markers `q104_07b_sm_haru_found`, `q104_spn_motel_haru_scene`, `q113_03a_sm_haru_kasai_drive`; wiki *Anders Hellman* | `[game-data]` `[wiki]` `[inferred]` |
| **Jeremiah Grayson** | Arasaka mercenary; Smasher's right-hand | `Character.Grayson` | Ebunike Docks | `story` | Raw registry phases `q005_default`, `q103_*`, `q203_*`, `sq031_*`; marker `sq031_04_sm_grayson`; wiki *Chippin' In* | `[game-data]` `[wiki]` |
| **The Board of Directors** | Collective sovereign: 19 Tokyo seats plus family shareholders | — (no individual records) | Arasaka Tower, Tokyo; boardroom in the Night City American Division HQ | `story` | Wiki *Arasaka* (board structure, 54/15/31 split); wiki *Totalimmortal* | `[wiki]` |

Notes:

- **The wiki lists three 2077 leaders because the outcome is dependent.**
  Saburo (1960–2077), Hanako (2077), Michiko (2077) and Yorinobu (2077) are all
  in the leadership infobox, but only one branch is true per playthrough. The
  base 2077 state after *The Heist* is Yorinobu as CEO; Hanako is the Kiji
  claimant; Michiko is a board member, not CEO. `[wiki]`
- **Hanako's title is deliberately ambiguous.** The Arasaka page calls her the
  Kiji figurehead and "the figurehead and CEO"; the employee list calls her an
  "unofficial spokeswoman" with no official position, given the task of keeping
  the family together. Treat her as the legitimist claimant and Kiji
  figurehead, not a settled CEO. `[wiki]`
- **Kei's dates conflict in the sources.** The Arasaka page says he became
  nominal CEO in 1997; the employee list says 1999. Both agree Saburo kept the
  real power and Kei died in 2023. `[wiki]`

### 1.2 The Night City / American Division branch

The Night City tower in Corpo Plaza is the **American Division HQ**, not a
regional sales office. It is where the 2077 succession is fought. The branch
has its own corporate ladder beneath the family:

| Name | Role in the Night City branch | Character record | Location | Presence class | Source | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| **Susan Abernathy** | Director of Special Operations, American HQ | `Character.q000_corpo_abernathy` | Arasaka Tower, Corpo Plaza | `prologue` | Raw registry entry `abernathy`, phase `conference`; wiki *Susan Abernathy* | `[game-data]` `[wiki]` |
| **Arthur Jenkins** | Senior member and head of Counterintelligence, Night City; V's boss | `Character.q000_corpo_jenkins` | Arasaka Tower (Jenkins' office, z≈142) | `prologue` | Raw registry entries `jenkins`, `jenkins_holo`, phases `conference`, `desk`; markers `q000_corpo_jenkins_office_chair`, `q000_sm_corpo_03_jenkins`; wiki *Arthur Jenkins* | `[game-data]` `[wiki]` |
| **Carter Smith** | Counterintelligence computer specialist; V's assistant | `Character.q000_corpo_assistant` (inferred; entry `assistant`) | Arasaka Tower | `prologue` | Raw registry entry `assistant`, phases `hall_waiting`, `hall_working`; wiki *Carter Smith* | `[game-data]` `[wiki]` `[inferred]` |
| **Frank Nostra** | Special Operations agent; V's co-worker | `Character.q000_corpo_friend` (inferred; entries `frank`, `corpo_friend`) | Arasaka Tower; Lizzie's Bar | `prologue` | Raw registry entries `frank`, `frank_holo`, `corpo_friend`, phases `elevator`, `final`, `lobby_left`, `lobby_right`, `bar`, `entrance`; wiki *Frank Nostra* | `[game-data]` `[wiki]` `[inferred]` |
| **V (Corporate lifepath)** | Counterintelligence operative under Jenkins | — (player character) | Arasaka Tower | `prologue` | Wiki *The Corpo-Rat*; employee list | `[wiki]` |
| **Yoru Tomobiki** | 2020 supervisor of Arasaka security contracts in Night City | — (no 2077 record) | Night City | `historical` | Wiki *List of Arasaka employees* | `[wiki]` `[lore]` |
| **Toshiro** | American Division CEO (2013); killed in the Alt Cunningham raid | — (no 2077 record) | Arasaka Tower, Night City | `historical` | Wiki *Saburo Arasaka*; employee list | `[wiki]` `[lore]` |
| **Iwasao Koremichi** | 2020s regional security director; held the Steel Dragons file | — (no 2077 record) | Night City | `historical` | Wiki *Yorinobu Arasaka*; employee list | `[wiki]` `[lore]` |

This branch is the **best model for a player joining Arasaka as an employee**.
The Corpo lifepath is not an abstraction: V is a counterintelligence operative
in this exact office, with a direct boss (Jenkins), a department director
(Abernathy), a rival department (Special Operations), a subordinate (Carter)
and a peer (Frank). The prologue then shows the promotion system failing: a
leak, a cover-up, a purge, and V's termination. `[wiki]` `[game-data]`

The formal regional hierarchy above the branch is from the 2020 corporate
sourcebook and still describes the org chart in 2077:

1. **CEO and Chairman** — the family sovereign.
2. **President and executive vice-presidents** — Tokyo.
3. **Board of directors** — 19 Tokyo seats plus the family; 54% family,
   15% board, 31% public.
4. **National Directors** — one per country/region.
5. **Regional Vice Presidents** — beneath them, a **Regional Security
   Director**, **Regional Sales Director** and **Regional Bank Director**.
6. **Area → Local → District → Site** — the departmental chain of command.
   `[wiki]`

### 1.3 Succession history

| Period | Leader | How the change happened |
| --- | --- | --- |
| 1915–1960 | **Sasai Arasaka** | Founder; built the family manufacturing firm and hid its capital abroad before the 1945 surrender. `[wiki]` |
| 1960–late 1990s | **Saburo Arasaka** | Took over on Sasai's death; added the Bank (1960s) and Security (1970) divisions; made Arasaka a global megacorp. `[wiki]` |
| late 1990s–2023 | **Kei Arasaka** | Saburo's eldest son and true believer; nominal CEO while Saburo kept the final say; died on 21 Aug 2023 after the Fourth Corporate War. `[wiki]` |
| 2023–2077 | **Saburo Arasaka** (nominal), **Hanako** as the face | Kei's death left Saburo in control again; from the 2040s the company split into Kiji (Hanako), Taka (Yorinobu) and Hato (Michiko). `[wiki]` |
| 2077 | **Yorinobu Arasaka** | Murdered Saburo at Konpeki Plaza; blamed Takemura; took the CEO seat and began sabotaging the company from within. `[wiki]` `[game-data]` |
| 2077 (dependent) | **Hanako / Saburo's engram** | If V takes Hanako's offer: Hanako confronts the board, Saburo's engram is revealed, Yorinobu is overwritten, and Saburo rules in his son's body. `[wiki]` |
| 2077 (dependent) | **Yorinobu** | If V sides with Panam, Rogue or goes alone: the Taka coup succeeds, Mikoshi is destroyed or damaged, Hanako dies or withdraws, and Yorinobu returns to Tokyo. `[wiki]` |
| 2079 (dependent) | **The board** | In the Phantom Liberty path, the board evicts Yorinobu as an inside saboteur; he flees with nomads. `[wiki]` |

The pattern is **dynastic and covert**, not meritocratic. The founder's son
inherits; the grandson is kept secret; the granddaughter is a board member;
the rebellious son murders the patriarch. External actors — Militech, the
NUSA, and V — decide the outcome. That is the core of Arasaka's "Politics"
weakness in §4. `[wiki]`

Historical secondary leaders worth knowing for a succession model:
**Toshiro** (American Division CEO, killed 2013), **Shintaro Takayama**
(director of security and Hanako's confidant), **Katsuo Iwashima** (compound
second-in-command), **Kiichi Nagawa** (Internal Affairs director), **Seiji
Okano** (corp with his own agenda), **Haruko Kanawa** (chief enforcer),
**Ubo Tanaka** (Hokkaido training-camp general), and **Yoru Tomobiki**
(Night City security-contracts supervisor). All are 2020/2013 lore with no
2077 record. `[wiki]` `[lore]`

### 1.4 Rank structure, entry and advancement

Arasaka publishes a conservative, rigid corporate culture: dark suits, silver
logo pins, Arasaka-made equipment, and a 20-year loyalty obligation for
company cyberware. The security arm is the visible one; the Bank and
Manufacturing arms are the other two pillars. `[wiki]`

**Corporate ladder.**

1. **Family / Chairman / CEO.** Closed to outsiders. The family holds 54% of
   the shares; the board holds 15%; the remaining 31% is public but watched,
   and noisy shareholders are "convinced" by black-ops teams. `[wiki]`
2. **President, executive VPs, board.** Tokyo. The board is 19 of Saburo's
   most trusted allies plus the family; it is a rubber stamp until a
   succession crisis makes it a prize. `[wiki]`
3. **National Director / Regional VP.** The top of a regional tower. Beneath
   the Regional VP sit the Regional Security, Sales and Bank Directors. `[wiki]`
4. **Area / Local / District / Site managers.** The departmental chain. `[wiki]`
5. **Executives and staff.** Conservative dress; Trauma Team card; loyalty
   tests. `[wiki]`

**Security ladder.**

1. **Guard.** The entry rank and the public face of the company; black
   uniform, rank on the left arm and right collar. `[wiki]`
2. **Soldier.** All soldiers are promoted from the guards; they wear name
   tapes and a chrysanthemum above the rank markings. `[wiki]`
3. **Bodyguard / special agent.** Distinguished ex-soldiers; bodyguards wear
   black or white suits; special agents can requisition untraceable equipment
   and run black operations. `[wiki]`
4. **Security director / head of security.** The top of the security arm;
   Adam Smasher holds the Night City role in 2077, reporting directly to
   Yorinobu. `[wiki]`

**Entry and advancement.**

- **Arasaka Academy** is the executive pipeline; Takemura graduated at the top
  of his class after being conscripted from the Chiba-11 slums. The Academy is
  the legitimate route for a clever outsider. `[wiki]`
- **Military conscription** is the other route: Arasaka transporters pick
  children from poor districts; the army provides food, shelter and training;
  the best are offered the Academy. `[wiki]`
- **Loyalty is the highest priority.** The corporate sourcebook is explicit:
  agents and executives who waver or fail are dismissed; those who betray the
  company are eliminated. The 2077 prologue shows the same logic: Abernathy
  purges the Counterintelligence Division to remove a liability. `[wiki]`
- **Advancement is a loyalty test, not just a performance review.** Jenkins is
  described as a "very capable psychopath"; Abernathy is "uncommonly cruel,
  even by corpo standards." Both are effective because they are ruthless, not
  because they are liked. `[wiki]`

**Practical consequence for the mod:** a player joining Arasaka should enter
as a guard, service employee or Academy trainee, then choose between the
security arm (guard → soldier → bodyguard/agent) and the corporate arm
(analyst → manager → regional director). The family/board tier is closed; the
player can become a regional director or a faction asset, but not CEO without
a coup or a family tie. That is the "join a corp and work up the ladder" path
in `docs/design/gameplay-systems.md` §3. `[inferred]`

### 1.5 Named members mapped to game data

Most named NPCs are **not in `data/sites/rosters.json`**. Arasaka's 68 roster
units are generic security records, KGB holograms and a scav-ambush enemy; no
named leader appears. The named leaders live in the raw sector community
registry and in the quest markers. Rows marked `[inferred]` are one-record
deductions; verify in-game before treating them as canonical.

| Name | Role / note | Character record | Community / marker | Location | Presence class | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| Saburo Arasaka | CEO/Chairman; engram | `Character.Saburo` | `saburo`; phases `q005_hotel_*`, `q101_*`, `#q201_ws_saburo_at_cp` | Konpeki; Tower; Mikoshi | `story` | `[game-data]` `[wiki]` |
| Yorinobu Arasaka | CEO after the murder; Taka | `Character.Yorinobu` | `yorinobu`; phases `q004_*`, `q005_*`, `q113_yorinobu_14_office*` | Konpeki; Tower CEO floor | `story` | `[game-data]` `[wiki]` |
| Hanako Arasaka | Kiji figurehead; claimant | `Character.Hanako` | `hanako`, `hanako_holo`; phases `q112_hanako_*`, `q113_hanako_*` | Estate; parade; Tower | `story` | `[game-data]` `[wiki]` |
| Michiko Arasaka | Hato head; board member | `Character.Michiko` | `michiko`; phases `q113_michiko_09_jungle*` | Tower jungle/boardroom | `story` | `[game-data]` `[wiki]` |
| Goro Takemura | Saburo's bodyguard | `Character.Takemura` | `takemura`, `Takemura`, `takemura_holo`; phases `q005_*`, `q101_*`, `q104_*`, `q112_*` | Konpeki; Japantown; Industrial Park; Estate; Tower | `story` | `[game-data]` `[wiki]` |
| Adam Smasher | Head of Security | `Character.Smasher`; variants `Character.q113_boss_smasher`, `Character.main_boss_adam_smasher` | `smasher`; phases `q005_*`, `q101_*`, `q108_atlantis_bar`, `q112_safe_house_start` | Konpeki; Tower; Mikoshi | `story` | `[game-data]` `[wiki]` |
| Sandayu Oda | Hanako's bodyguard | `Character.Cyberninja_Oda`; `Character.Cyberninja_Oda_Follower` | `oda`, `oda_follower`; phases `q112_cyberninja_08_bossfight`, `q112_cyberninja_oda_stealth` | Japantown; Tower | `story` | `[game-data]` `[wiki]` |
| Anders Hellman | Relic director; defector | `Character.Haru_Kasai` (inferred; dev alias) | `haru`, `anders_hellman_holo`; phases `q004_*`, `q005_*`, `q101_*`, `q104_*` | Kang Tao AV; Sunset Motel; Estate; Orbital Station | `story` | `[game-data]` `[wiki]` `[inferred]` |
| Jeremiah Grayson | Smasher's right-hand | `Character.Grayson` | `grayson`; phases `q005_default`, `q103_*`, `q203_*`, `sq031_*` | Ebunike Docks | `story` | `[game-data]` `[wiki]` |
| Susan Abernathy | Director of Special Operations | `Character.q000_corpo_abernathy` | `abernathy`; phase `conference` | Arasaka Tower | `prologue` | `[game-data]` `[wiki]` |
| Arthur Jenkins | Counterintelligence head | `Character.q000_corpo_jenkins` | `jenkins`, `jenkins_holo`; phases `conference`, `desk` | Arasaka Tower | `prologue` | `[game-data]` `[wiki]` |
| Carter Smith | V's assistant | `Character.q000_corpo_assistant` (inferred) | `assistant`; phases `hall_waiting`, `hall_working` | Arasaka Tower | `prologue` | `[game-data]` `[wiki]` `[inferred]` |
| Frank Nostra | Special Operations agent | `Character.q000_corpo_friend` (inferred) | `frank`, `frank_holo`, `corpo_friend` | Arasaka Tower; Lizzie's Bar | `prologue` | `[game-data]` `[wiki]` `[inferred]` |
| Kei Arasaka | CEO 1997/99–2023 | — | — | — | `historical` | `[wiki]` `[lore]` |
| Toshiro | American Division CEO 2013 | — | — | — | `historical` | `[wiki]` `[lore]` |
| Shintaro Takayama | Compound security director | — | — | — | `historical` | `[wiki]` `[lore]` |
| Katsuo Iwashima | Compound second-in-command | — | — | — | `historical` | `[wiki]` `[lore]` |

Two data cautions:

- **`Character.Haru_Kasai` is Hellman, not a separate person.** The wiki's
  Anders Hellman page says "during development, his name appeared as Haru
  Kasai." The raw registry uses `Character.Haru_Kasai` for the entries `haru`
  and `anders_hellman_holo`, with phases from the Konpeki heist and the Kang
  Tao extraction. Treat `Character.Haru_Kasai` as Hellman's record; do not
  seed a "Haru Kasai" NPC. `[game-data]` `[wiki]` `[inferred]`
- **`Character.mws_se5_03_enemy_smasher` is not Adam Smasher.** It is a
  Badlands scav-ambush mini-world-story enemy named "smasher". Likewise
  `Character.sts_ep1_08_kgb_boss_hologram*` is a KGB hologram set piece, not
  Arasaka leadership. `[game-data]`

### 1.6 What the game actually spawns (open world vs story-only)

This is the part other agents must not assume. A wiki infobox does not mean an
actor in free roam.

**`story` — gated by main/side quests; do not expect them with the campaign
disabled.**

- Saburo, Yorinobu, Hanako, Michiko, Takemura, Smasher, Oda, Hellman and
  Grayson. Their phases are `q004_*`, `q005_*`, `q101_*`, `q103_*`,
  `q104_*`, `q108_*`, `q112_*`, `q113_*`, `q115_*`, `q116_*`, `q203_*`,
  `sq031_*`, `#q201_*`. These are quest phases, not ambient schedules.
  `[game-data]`

**`prologue` — the Corpo lifepath; story-gated.**

- Abernathy, Jenkins, Carter Smith and Frank Nostra. Their phases are
  `q000_corpo_*`, which is the corporate prologue. They are the best
  **templates** for an employee-join path, but they do not spawn in free
  roam. `[game-data]`

**`ambient` — persists in free roam.**

- Generic Arasaka security guards and soldiers at the faction's sites. The
  roster has 8 sites / 68 units / 21 records, but the count is misleading:
  most units are the KGB holograms at `sts_ep1_08` or the scav-ambush enemy at
  `mws_se5_03`; the real facility garrisons are small (e.g. site 254
  `ma_wbr_hil_06` has 6 Arasaka units). There is **no named leader** among
  them. `[game-data]`

**Conclusion:** with the campaign disabled, the game provides generic guards,
not the Arasaka leadership. The mod must supply the leaders as simulation
agents. The `world-activity` rows in the Maelstrom pilot do not exist here:
Arasaka has no gig-scoped named leader. `[game-data]`

### 1.7 Player-path hooks

This is the design-facing summary of who a player can join under, climb past,
ally with or remove. It covers both the family tier and the Night City branch.

| Person | Join under | Climb past | Ally with | Remove |
| --- | --- | --- | --- | --- |
| **Saburo (engram)** | The old order; Kiji; the board's traditionalists | The engram is the throne; climbing past it means destroying Mikoshi or denying Hanako | Hanako, Takemura, Oda, the Kiji board | Destroy Mikoshi, side with Yorinobu, or let the Tower fall |
| **Yorinobu** | The Taka reform/sabotage wing; pro-Western modernisers | Smasher is the gatekeeper; the Taka officers are the ladder | Smasher, Taka loyalists, Hellman (R&D), nomads (later) | Expose him to the board, side with Hanako, or let the Aldecaldos/Rogue reach Mikoshi |
| **Hanako** | The Kiji legitimist wing; the board's continuity | Oda and Takemura are the gatekeepers; Hanako is the figurehead | Oda, Takemura, Hellman, Michiko (Hato), the board | Side with Yorinobu, destroy Mikoshi, or let her die in the Tower |
| **Michiko** | The Hato liberal-reform wing; board politics | Her board seat and Danger Gal are the ladder; she has the least muscle | Hanako, Danger Gal, media/politicians, the Hato board | Isolate her from the board; she dies in the coup unless V helps Hanako |
| **Susan Abernathy** | Special Operations; the corporate security state | Jenkins is the rival; her files are the lever | Her (dangerous), or use her files | Side with Jenkins, expose her, or let the purge run |
| **Arthur Jenkins** | Counterintelligence; the Corpo lifepath | Abernathy is the ceiling; the Frankfurt operation is the test | Jenkins (he saved V), Carter, Frank | Side with Abernathy, expose the Frankfurt op, or let the purge run |
| **Takemura** | The ex-bodyguard loyalist; Saburo's honour | His honour code is the ceiling; he will not betray Hanako | Takemura for Kiji; Oda as his pupil | Let him die in *Search and Destroy*, or side against Hanako |
| **Adam Smasher** | Not a joinable path; a power centre | — | Only as Yorinobu's enforcer; he has no political programme | Remove him to decapitate Taka security |
| **Anders Hellman** | Not a joinable path; an R&D power centre | — | Ally for Relic/Mikoshi expertise; he sells loyalty | Cut the Relic programme or let Kang Tao take him |

The design consequence: Arasaka has **two ladders, not one**. A player can
climb the family/board ladder (Saburo → Yorinobu → Hanako → Michiko) or the
corporate-department ladder (Abernathy/Jenkins → regional director → board).
The first is a dynastic contest; the second is a bureaucratic survival game.
Both matter for a player who joins as an employee. `[inferred]`

---

## 2. Internal political factions

### 2.1 The blocs

"Members" counts below are **presence proxies** from the raw registry and
`areas.jsonl`, not membership rolls. The Arasaka Tower communities are
overlapping quest phases of one site; do not sum them.

| Bloc | Leader(s) | What it wants | Presence / members hint | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- |
| **Kiji (雉, Green Pheasant)** | Hanako Arasaka; controlled by Saburo | Continue Saburo/Kei's order; conservative technocracy; stability; peace with the NUSA | Hanako; Takemura; Oda; Kiji-aligned board traditionalists; Arasaka Estate and Tower security | Wiki *Arasaka* (Kiji description); *Hanako Arasaka*; *Goro Takemura*; *Sandayu Oda* | `[wiki]` |
| **Taka (鷹, Hawk)** | Yorinobu Arasaka | Sabotage Arasaka from within; pro-Western reforms; direct, uncompromising action; military coup | Yorinobu; Adam Smasher; Taka loyalist soldiers in Night City, Kyoto, Dubai and Paris; militant board members | Wiki *Arasaka* (Taka description); *Yorinobu Arasaka*; *Adam Smasher* | `[wiki]` |
| **Hato (鳩, Dove)** | Michiko Arasaka (Sanderson) | Liberal reforms; deeper changes; US ties; the least powerful bloc | Michiko; Danger Gal; some politicians and media personalities; board liberals | Wiki *Arasaka* (Hato description); *Michiko Arasaka* | `[wiki]` |
| **The Board / old guard** | Collective (19 Tokyo seats + family) | Preserve the company and their seats; avoid open conflict; accept the strongest claimant | Tokyo board; branch directors from Paris, Shanghai and Kinshasa; family shareholders (54%) | Wiki *Arasaka* (board structure); *Totalimmortal* | `[wiki]` |
| **Saburo's engram / old order** | Saburo Arasaka (engram) | Restore Saburo's control; overwrite Yorinobu; revert the reforms; peace with Militech/NUSA | Saburo's engram in Mikoshi; Hanako; Kiji; Hellman's Relic team | Wiki *Saburo Arasaka*; *Hanako Arasaka*; *Totalimmortal* | `[wiki]` |
| **Smasher's security apparatus** | Adam Smasher | Carry out Yorinobu's dirty work; protect the CEO; no loose ends | Smasher; Grayson; Arasaka security teams; Ebunike base | Wiki *Adam Smasher*; *Chippin' In*; raw registry `Character.Smasher`, `Character.Grayson` | `[game-data]` `[wiki]` |
| **Hellman's R&D / defector wing** | Anders Hellman | Survive; monetise the Relic; sell loyalty to the highest bidder | Hellman; Relic team; Kang Tao contacts | Wiki *Anders Hellman*; raw registry `Character.Haru_Kasai` | `[game-data]` `[wiki]` |
| **Counterintelligence vs Special Operations** | Arthur Jenkins / Susan Abernathy | Promotion, jurisdiction and survival; each tries to purge the other | Jenkins' counterintel team (V, Carter Smith, Frank Nostra, Harry); Abernathy's Special Operations; Arasaka Tower offices | Wiki *Arthur Jenkins*; *Susan Abernathy*; *Carter Smith*; *Frank Nostra*; raw registry `q000_corpo_*` | `[game-data]` `[wiki]` |

### 2.2 The 2077 split: Yorinobu vs Hanako/Saburo

This is the central conflict, and it is both personal and ideological.

- **Yorinobu** is Saburo's youngest son and the original heir. He rejected his
  father's vision on the night he graduated, founded the Steel Dragons, and
  spent decades fighting Arasaka from outside. He concluded that the only way
  to destroy the company was from within. `[wiki]`
- **The Relic theft** is his opening move: he steals a Relic prototype from
  Saburo's Tokyo lab, ensures the engram on it is Johnny Silverhand, and
  retreats to Night City. Hellman warns him the chip is not ready and tells
  Saburo; Saburo sails to Night City on the *Kujira* with Hanako. `[wiki]`
- **The murder** at Konpeki Plaza is a family argument that turns violent.
  Yorinobu strangles Saburo, blames Takemura, and takes the CEO seat. `[wiki]`
  `[game-data]`
- **The coup** is Yorinobu's attempt to break the board and the other blocs:
  he calls an emergency supervisor-board meeting in Night City, brings in
  Tokyo executives and branch directors from Paris, Shanghai and Kinshasa,
  and orders Taka troops to destroy the other factions and remove the board.
  `[wiki]`
- **Hanako's counter-move** is legitimacy: she brings V as a witness, reveals
  Saburo's engram, and tells the board to follow her as if she were Saburo.
  The engram then overwrites Yorinobu. `[wiki]`

The policy difference is real, not just a family quarrel:

- **Yorinobu's line:** destroy Arasaka from within; sell assets; break the
  old order; pro-Western, innovative, militant.
- **Hanako's line:** preserve the old order; conservative technocracy;
  continuity; peace with the NUSA on Arasaka's terms.
- **Michiko's line:** liberal reform; US ties; the least powerful but the most
  legitimate-sounding alternative.
- **Saburo's line:** immortality through the Relic; restore the empire;
  no concessions.

That is a simulation-ready axis: **dynastic continuity vs internal sabotage vs
liberal reform**, with the board as the prize. `[inferred]`

### 2.3 Michiko and Hato: the liberal board bloc

Michiko is the wild card. She is Kei's daughter, Saburo's granddaughter, and
the head of the Hato faction. She was kept secret from Saburo because she was
half-American; she grew up in Night City, founded Danger Gal, and became a
board member. Hato is the liberal wing, the least powerful of the three, but
it has support among politicians and media personalities. `[wiki]`

Her 2077 position is cautious:

- She accepts Yorinobu as CEO after Saburo's death, like the rest of the board.
- She attends the board meeting in the Hanako path and is reluctant to believe
  V until Saburo's engram speaks.
- She survives the coup only if V helps Hanako; otherwise she is one of the
  board casualties. `[wiki]`

For a simulation, Michiko is the **reform/legitimacy candidate**: she can give
a player's faction a board seat, US contacts, and a respectable face, but she
has the least muscle and is the most likely to be outmanoeuvred by Smasher or
the Taka troops. `[inferred]`

### 2.4 The board and the Tokyo/Night City axis

The board is the legal sovereign, but it is not a deliberative body in 2077.
It is 19 of Saburo's most trusted allies plus the family; Saburo is chairman;
Hanako is a nominal shareholder. The board accepts Yorinobu after the murder
because no one is willing to stand against him; Saburo's engram later calls
them cowards for it. `[wiki]`

The Tokyo/Night City axis matters because the 2077 coup is fought in the
American Division HQ:

- **Tokyo** holds the board, the president, the executive VPs and the family
  compound. It is the source of legitimacy.
- **Night City** holds the American Division HQ, Yorinobu, Smasher, Hanako's
  estate, Michiko's board seat and the Mikoshi access point. It is the prize.
- **Branch directors** from Paris, Shanghai and Kinshasa are drawn into the
  Night City meeting, which is why the coup is global. `[wiki]`

For a simulation, control of the Night City tower plus the board's recognition
is the win condition for any Arasaka bloc. `[inferred]`

### 2.5 The departmental war: Counterintelligence vs Special Operations

The family blocs are the top-level politics; the branch has its own, and it is
the one a player employee actually experiences.

- **Arthur Jenkins** is the senior member and head of Night City's
  Counterintelligence Division. He is V's direct superior, saved V from a worse
  life, and is described as a "very capable psychopath." `[wiki]`
- **Susan Abernathy** is the Director of Special Operations for the American
  HQ. She got the promotion Jenkins wanted by smearing him and the entire
  Counterintelligence Division to the administrative board. She is "uncommonly
  cruel, even by corpo standards," and her name makes employees falter. `[wiki]`
- **The feud escalates** when Jenkins orders a cyberattack on the European
  Space Council to save Arasaka's Luna contracts. Abernathy criticises the
  mess; Jenkins orders V to eliminate her. Carter Smith warns Abernathy; the
  Counterintelligence Division is purged; V is terminated. `[wiki]`
- **Frank Nostra** is a Special Operations agent and V's co-worker; he is
  later purged by Abernathy's downsizing and turns his files into a dead
  man's trigger. `[wiki]`

This is a clean, simulation-ready **bureaucratic bloc**: two departments
fighting over promotions, jurisdiction and survival, with the player as a
pawn. It is not in the family-bloc table because it is a branch-level conflict,
but it matters more to an employee than Kiji/Taka/Hato. `[inferred]`

### 2.6 Smasher's security apparatus: a non-member power centre

Adam Smasher is not a faction leader and has no political programme. He is a
full-body-conversion mercenary who owes Arasaka his life and repays it by
killing the corporation's enemies. By 2077 he is Yorinobu's personal bodyguard
and the manager of Arasaka's dirtiest work; after Saburo's murder he is
promoted to **head of security**. `[wiki]`

His political weight is structural:

- He is the **gatekeeper** to Yorinobu; Oda cannot get past him to warn the CEO
  about parade security. `[wiki]`
- He commands the **security apparatus** and the strike teams; he personally
  rescues Hanako at the parade. `[wiki]`
- He is **personally loyal to Yorinobu**, not to the board or the family. His
  removal decapitates Taka security. `[wiki]`
- He is a **loose-end manager**: he knows where Johnny Silverhand is buried,
  keeps Silverhand's Porsche and Malorian, and uses Grayson as his right-hand.
  `[wiki]`

For a simulation, Smasher is a **military asset with veto power**, not a
voting bloc. He can be allied with only as Yorinobu's enforcer; removing him
is the cleanest way to weaken the Taka coup. `[inferred]`

### 2.7 Hellman's R&D / defector wing: a non-member power centre

Anders Hellman is the Relic project director, a leading bioengineer, and one
of Arasaka's scientific pillars. He is on first-name terms with Hanako and in
personal contact with Saburo. He is also the first person to warn Saburo that
Yorinobu stole the prototype. `[wiki]`

His loyalty is for sale:

- He begins negotiating with Kang Tao before the heist, and defects after
  Yorinobu becomes CEO. `[wiki]`
- Rogue tracks his AV; V and Panam bring it down over Jackson Plains; V
  interrogates him at the Sunset Motel. `[wiki]`
- In the Hanako path he is retrieved and works for Hanako, because he is
  "worth more alive than harmed or dead." `[wiki]`
- He runs the Relic/Mikoshi explanation and the Secure Your Soul contract at
  the Orbital Station. `[wiki]`

For a simulation, Hellman is a **portable R&D asset**: he can be bought,
stolen, or killed, and whichever bloc holds him holds the Relic expertise.
He is not a member of any family bloc. `[inferred]`

### 2.8 What could drive internal conflict in a simulation

Evidence-based drivers, in rough order of plausibility:

1. **Succession after Saburo's death.** Taka (Yorinobu) vs Kiji (Hanako) vs
   Hato (Michiko). Each has a different external policy and a different claim.
2. **Yorinobu's sabotage.** He is not trying to win the company; he is trying
   to destroy it. A player who wants Arasaka to survive must stop him, which
   means siding with Hanako or the board.
3. **The board's survival.** The board is the legal sovereign and the prize.
   Yorinobu's coup tries to kill it; Hanako's counter-coup tries to capture it.
4. **Control of Mikoshi and the Relic.** The engram is the throne, the
   immortality project and the R&D prize. Whoever holds Mikoshi holds the
   succession.
5. **Control of the Night City tower.** The American Division HQ is the
   physical seat of the coup and the link to the board.
6. **Security-apparatus loyalty.** Smasher vs Oda/Takemura is a personal and
   professional split; it decides who can reach the CEO.
7. **Departmental turf.** Counterintelligence vs Special Operations is a
   branch-level war over promotions and survival; it can purge a player's
   entire team.
8. **Defectors and poaching.** Hellman to Kang Tao; Yorinobu to the nomads;
   Michiko's US ties. Talent is mobile and loyal to the highest bidder.
9. **External pressure.** Militech, the NUSA, the Aldecaldos and V can all
   decide the succession by force. The historical pattern is that external
   violence often decides the outcome.

---

## 3. External relations matrix

### 3.1 Stance vocabulary

One stance per row. Use the first that fits; do not average two stances into a
non-answer. For this corp document, the stance is read **from Arasaka's side**:
`client` means Arasaka hires or uses the other faction; `patron` means Arasaka
protects or supplies it. This is stated because the generic vocabulary is
ambiguous for asymmetric corporate relationships (see §5).

| Stance | Meaning |
| --- | --- |
| `war` | Open, active armed conflict over turf or existence |
| `hostile` | Actively targets or raids the other side, but not a declared turf war |
| `rival` | Turf or economic competition, with skirmishes |
| `neutral` | No attested interaction; not an ally |
| `trade` | Transactional exchange, no loyalty |
| `ally` | Coordinated support or shared operations |
| `patron` | Protects or supplies the other faction |
| `client` | Hires or uses the other faction |

### 3.2 The matrix

Every row is a faction code from `data/factions.json`. Rows with no attested
interaction are marked `neutral` and `[inferred]`; they are placeholders, not
findings. Do not promote them without evidence.

There is **no usable offline attitude matrix**. `Affiliation.hpp` is an
identity enum, not a relation table; `Attitude_Record.hpp` is opaque. The
stances below are judged from quests, wiki and spatial adjacency, not from a
TweakDB relation row. That is why every row carries a tag and why the neutral
rows are not claims of friendship.

| Faction | Code | Stance | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| Tyger Claws | `tyger_claws` | `client` | Arasaka-backed motorcycle club; close ties to Arasaka upper management, which outsourced side-jobs and paid in cybertech and military-grade weapons; Arasaka sleeper agents joined the gang after 2023; still close in the 2070s `[wiki]` | `wiki` |
| Valentinos | `valentinos` | `trade` | Arasaka contracted Valentino José Luis to frame Militech for an attack on an Arasaka facility (Gig: *On a Tight Leash*); a one-off proxy hire, not a gang-level relationship `[wiki]` | `wiki` |
| Militech | `militech` | `rival` | Fourth Corporate War 2022–25; 2070 NUSA/Militech invasion of Night City forced back by Arasaka's supercarrier; 2077 mutual sabotage and rising tensions `[wiki]` | `wiki` |
| Kang Tao | `kang_tao` | `rival` | Kang Tao poached Arasaka technology and employees; Hellman defected to Kang Tao and was extracted by its AV; Kang Tao is Arasaka's top smart-weapons competitor `[wiki]` | `wiki` |
| Biotechnica | `biotechnica` | `neutral` | No attested interaction; a biotech supplier, not a Night City turf actor `[inferred]` | `inferred` |
| Petrochem | `petrochem` | `neutral` | No attested interaction; fuel/energy supplier only `[inferred]` | `inferred` |
| Barghest | `barghest` | `neutral` | No attested interaction; the Dogtown KGB hologram set piece is not an Arasaka relationship `[game-data]` `[inferred]` | `game-data+inferred` |
| 6th Street | `sixth_street` | `rival` | Anti-corporate paramilitary founded by Fourth Corporate War veterans; Arasaka Industrial Park sits in 6th Street's Arroyo turf; no explicit Arasaka gig found `[game-data]` `[wiki]` `[inferred]` | `game-data+wiki+inferred` |
| Aldecaldos | `aldecaldos` | `hostile` | The Star ending: Aldecaldos invade Arasaka Tower and destroy Mikoshi; dependent on V's choice `[wiki]` | `wiki` |
| Wraiths | `wraiths` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Animals | `animals` | `neutral` | No attested interaction; Animals hire out as bodyguards but no Arasaka contract found `[wiki]` `[inferred]` | `wiki+inferred` |
| The Mox | `the_mox` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Maelstrom | `maelstrom` | `hostile` | Maelstrom raids corporate transports and sells stolen tech; Arasaka merc Grayson guards the Ebunike in Maelstrom territory; 9 Maelstrom hold Memorial Ring West inside an Arasaka-owned sub-territory `[wiki]` `[game-data]` | `game-data+wiki` |
| Voodoo Boys | `voodoo_boys` | `neutral` | No attested interaction; VDBs hack corporate databanks but no Arasaka-specific operation found `[wiki]` `[inferred]` | `wiki+inferred` |
| NCPD | `ncpd` | `trade` | NCPD is beholden to Arasaka and Militech interests; Arasaka puts interests in the PD expecting return; official sponsor is Night Corp `[wiki]` | `wiki` |
| Night Corp | `night_corp` | `rival` | Night Corp lost the race for Night City influence to Arasaka and Militech; still runs public administration and funds NCPD `[wiki]` | `wiki` |
| City Council | `city_council` | `patron` | Councilman Lucius Rhyne invited Arasaka back to protect Night City from the NUSA in 2070; Arasaka arrived with a supercarrier and forced NUSA/Militech to retreat; Arasaka effectively controls the city `[wiki]` | `wiki` |
| Scavengers | `scavengers` | `neutral` | No attested interaction; Arasaka security would treat scavs as criminals, but no specific event `[inferred]` | `inferred` |
| Regina Jones | `fixer_regina` | `neutral` | No Arasaka-specific gig or lore link found `[inferred]` | `inferred` |
| Wakako Okada | `fixer_wakako` | `hostile` | Wakako lost a grandchild to Arasaka and has disdained the corporation since; she helps Takemura in q112 on V's behalf, not out of pro-Arasaka sympathy `[wiki]` `[game-data]` | `game-data+wiki` |
| Sebastian Ibarra (Padre) | `fixer_padre` | `hostile` | Padre gives the gig *On a Tight Leash*, which stops Arasaka's attempt to frame Militech via Valentino José Luis `[wiki]` | `wiki` |
| Muamar Reyes (El Capitán) | `fixer_el_capitan` | `hostile` | El Capitán gives the gig *Baby Let Me Take You*, robbing an Arasaka dockyard for medical supplies; he hates Arasaka for dumping toxic waste in Rancho Coronado `[wiki]` | `wiki` |
| Dakota Smith | `fixer_dakota` | `neutral` | No Arasaka-specific gig or lore link found `[inferred]` | `inferred` |
| Dino Dinovic | `fixer_dino` | `trade` | Dino profits from the corpo contracts generated by Hanako Arasaka's arrival in Downtown; transactional, not loyal `[wiki]` | `wiki` |
| Rogue Amendiares | `fixer_rogue` | `hostile` | Rogue raided Arasaka Tower in 2013 and 2023; *Chippin' In* targets Smasher/Grayson and the Ebunike; she works with V against Arasaka in the Sun ending `[wiki]` | `wiki` |
| Mr. Hands | `fixer_mr_hands` | `neutral` | No Arasaka-specific gig or lore link found `[inferred]` | `inferred` |
| Afterlife | `afterlife` | `neutral` | Neutral merc marketplace; Rogue's anti-Arasaka operations do not make the Afterlife an Arasaka enemy `[wiki]` `[inferred]` | `wiki+inferred` |
| NUSA | `nusa` | `hostile` | NUSA/Militech invaded Night City in 2070; Arasaka's supercarrier forced them to retreat; NUSA is Militech's parent and Arasaka's geopolitical rival `[wiki]` | `wiki` |
| Zetatech | `zetatech` | `trade` | Arasaka uses Zetatech Valgus helicopters and Atlus AVs; the Industrial Park retrofits Zetatech AVs; a supplier relationship `[wiki]` `[game-data]` | `game-data+wiki` |
| Trauma Team | `trauma_team` | `trade` | Trauma Team partners with Arasaka and gives Arasaka employees memberships; Arasaka is a client `[wiki]` | `wiki` |
| News 54 | `news54` | `rival` | Network News 54 lost reporters investigating Arasaka scandals; Arasaka avoids direct confrontation while feeding it bad press about rivals `[wiki]` | `wiki` |

Stance counts (31 rows): **hostile 7, rival 5, trade 5, neutral 12, client 1,
patron 1, ally 0.** Arasaka has no ally in the matrix. Its closest
relationship is the Tyger Claws proxy network (`client`), and the City Council
is the closest thing to a grateful dependent (`patron`). `[inferred]`

### 3.3 Actors outside `data/factions.json`

These are real relationships but have no faction code, so they are prose only.

- **FACS (Far Asian Co-prosperity Sphere)** — the Japanese corporate union
  formed to counter Arasaka's control of the Japanese government in the late
  1990s; it exposed Arasaka corruption and kept fighting it for decades. Treat
  as `hostile` in lore, but it is not a 2077 faction with a code. `[wiki]`
- **World News Service (WNS)** — Arasaka's long-standing media ally since the
  early 2000s; WNS is one of the few media organisations allowed to interview
  or report on Arasaka operations. `[wiki]`
- **Yakuza and Triads** — Arasaka has "strong ties" with underground
  organisations, including the Yakuza and Triads. They are proxies, not
  members. `[wiki]`
- **Amazonian Security** — a European rival; tensions rose in the late 2020s,
  and the two backed opposite candidates in Portugal in 2020. `[wiki]`
- **InfoComp** — a tiny database company that studied Arasaka's history and
  holdings; Arasaka pays it little attention. `[wiki]`
- **Danger Gal** — Michiko's private-investigation firm; a Hato asset and a
  source of US contacts, not an Arasaka division. `[wiki]`
- **Lazarus Group** — Militech's closest corporate ally; an indirect Arasaka
  rival through Militech. `[wiki]`
- **Arasaka Academy** — the executive pipeline inside the Tower; an
  institution, not a faction. `[wiki]`

### 3.4 Guarantor assessment

This is the design question: if a player founds an organisation, which
factions would guarantee Arasaka's support, and which would Arasaka itself
guarantee?

- **No faction is an ally.** The matrix has no `ally` row. The closest is the
  Tyger Claws proxy network (`client`), which is asymmetric: Arasaka uses the
  Claws, pays them in chrome and weapons, and plants sleeper agents among them.
  That is a patronage relationship, not a guarantee. `[wiki]`
- **Arasaka is a strong patron but a poor ally.** It protects the City Council
  and effectively controls Night City; it supplies the Tyger Claws; it buys
  from Zetatech and Trauma Team. But it discards proxies when they become a
  liability, and it eliminates employees who waver. A player who takes
  Arasaka's support inherits its enemies (Militech, the NUSA, 6th Street,
  Maelstrom) and its internal succession war. `[wiki]` `[inferred]`
- **Plausible guarantors for a player-founded organisation** are therefore
  transactional and branch-level, not corporate-level: a corrupt Arasaka
  regional director (Jenkins/Abernathy type), a Tyger Claws proxy arrangement,
  a Hato/Danger Gal channel, or a City Council patron who owes Arasaka. None
  is a formal alliance. `[inferred]`
- **Arasaka as an aggressor.** For a player founding an organisation on an
  Arasaka-held point, Arasaka is more likely to be the **pre-emptive patron or
  attacker** than the guarantor: it buys proxies, plants sleeper agents, and
  sends Smasher's security apparatus after loose ends. That is consistent with
  its `client`/`patron` rows and its `hostile` rows toward Maelstrom and the
  Aldecaldos. `[inferred]`

---

## 4. Pillar notes

Design claims from `docs/design/gameplay-systems.md`: Arasaka is a
**Corporation** (archetype strength Technology, weakness Culture); faction
strength **Espionage**, weakness **Politics**.

| Pillar | Design claim | Lore verdict | Evidence |
| --- | --- | --- | --- |
| Technology (archetype strength) | Corporations are technology-led | **Strongly supported.** Arasaka's edge is the Relic, Mikoshi, Soulkiller, cyberware, security systems, orbital R&D and the Arasaka Academy. It is one of the world's largest cyberware and weapons manufacturers. | Relic project; Mikoshi; Soulkiller; cyberware manufacturing; security equipment; Orbital Station; Academy `[wiki]` |
| Culture (archetype weakness) | Corporations are culturally weak | **Supported, with a twist.** Arasaka has a strong *internal* culture — samurai ethos, loyalty, family, the Academy, the company uniform — but it is coercive and inward-facing. It produces fear, not affection, and it produces defectors (Yorinobu, Hellman, Michiko's Hato). Its culture does not export; it repels outsiders. | Corporate dress and loyalty rules; "highest priority is loyalty"; Yorinobu's rebellion; Hellman's defection; Hato's liberal wing `[wiki]` |
| Espionage (faction strength) | Arasaka is an espionage power | **Strongly supported.** The 2020 sourcebook gives Arasaka 5,000 undercover agents, assassins and spies; black operations, blackmail, bribery and Soulkiller are core tools; Arasaka plants sleeper agents in the Tyger Claws; Smasher is the loose-end manager; the Counterintelligence Division is a playable department. | Black Resources; 5,000 agents; Soulkiller; Tyger Claws sleeper agents; Smasher; Jenkins/Abernathy `[wiki]` `[game-data]` |
| Politics (faction weakness) | Arasaka is politically weak | **Supported, but specific.** Arasaka is excellent at *covert* political influence — bribery, blackmail, city control, a supercarrier that decides a war — but brittle at *legitimate* succession and coalition-building. The 2077 crisis is a dynastic coup, not a failure of political skill. Model it as **high covert influence, low legitimate legitimacy**, not "bad at politics." | Board rubber-stamp; 54/15/31 ownership; Yorinobu's coup; Kiji/Taka/Hato; City Council patronage; NUSA standoff `[wiki]` |
| Overall fit | The pillars fit the corp's identity | **Good for identity, imperfect for balance.** Keep Technology and Espionage strong; keep Culture weak as *external soft power*; model Politics as *internal legitimacy* rather than absence of influence. | Synthesis of the rows above `[inferred]` |

Design cautions, not redesigns:

- **Do not model Arasaka as politically incompetent.** It runs a city, bribes
  a council, and forces the NUSA to retreat. Its weakness is that its
  legitimacy depends on a 158-year-old patriarch and a family that is trying
  to kill each other.
- **Do not model Culture as zero.** The samurai/loyalty culture is real and
  binds the security arm; it simply does not win friends outside the company.
- **The Relic/Mikoshi is the technology and politics hinge.** Whoever controls
  it controls the succession and the R&D pipeline. It should be a high-value
  capture/espionage target, not a generic lab.
- **The departmental war is the employee-level politics.** Kiji/Taka/Hato is
  the family game; Counterintelligence vs Special Operations is the game a
  player joining as an employee actually plays.

---

## 5. Gaps and uncertainties

1. **No offline attitude matrix.** `Affiliation.hpp` is an identity enum, not
   a relation table; `Attitude_Record.hpp` is opaque. Every stance in §3.2 is
   judged from quests, wiki and spatial adjacency; none is read from a TweakDB
   relation row. A TweakDB dump would settle the neutral rows.
2. **The named leadership is not in `data/sites/rosters.json`.** Arasaka's 68
   roster units are generic security records, KGB holograms and a scav-ambush
   enemy. Saburo, Yorinobu, Hanako, Michiko, Takemura, Smasher, Oda, Hellman
   and Grayson exist only in the raw sector community registry and quest
   markers. This is the same "rosters miss quest communities" problem as
   METHOD §1.2 item 6, but worse for corps.
3. **Hellman's record is a development alias.** `Character.Haru_Kasai` is the
   only record tied to the entries `haru` and `anders_hellman_holo`; the wiki
   says his name appeared as Haru Kasai during development. There is no
   `Character.Hellman`. This is an `[inferred]` identity, not an exact one.
4. **Carter Smith and Frank Nostra are inferred.** `Character.q000_corpo_assistant`
   (`assistant`) and `Character.q000_corpo_friend` (`frank`, `corpo_friend`)
   are one-record deductions from the prologue entries and the wiki. Verify
   in-game before seeding them as named NPCs.
5. **The board has no individual records.** The 19 Tokyo seats, the family
   shareholders and the branch directors are a collective. The JSON `leaders`
   entry for the board uses `character_record_id: null`; a simulation that
   needs individual board members must invent or research them separately.
6. **The 2077 leadership is dependent on V.** Yorinobu, Hanako, Saburo's
   engram, Michiko, Takemura, Oda, Smasher, Hellman and Grayson all have
   branches. The document records the branches; a simulation must choose one
   or model them explicitly. The base state after *The Heist* is Yorinobu as
   CEO, Hanako as Kiji claimant, Michiko as board member.
7. **"Open world with the campaign disabled" is a heuristic.** The mod may
   disable gigs and the prologue along with the campaign. The `story` and
   `prologue` rows are definitely not ambient; the generic security rows need
   an in-game spawn check.
8. **The 68 roster units are not a garrison.** Most are the KGB holograms at
   `sts_ep1_08` (27) and the scav-ambush enemy at `mws_se5_03` (15); the real
   facility garrisons are small. Do not use the roster count as a loyalty or
   manpower measure.
9. **The Arasaka Tower communities are overlapping quest phases.** Do not sum
   `q113_*`, `q115_*` and `q116_*` communities; they are phases of one site.
10. **The wiki's "Hanako as CEO" and "Hanako as spokeswoman" conflict.** The
    Arasaka page calls her the Kiji figurehead and CEO; the employee list calls
    her an unofficial spokeswoman with no official position. Treat her as the
    legitimist claimant and Kiji figurehead, not a settled CEO.
11. **Kei's CEO dates conflict.** The Arasaka page says 1997; the employee list
    says 1999. Both agree Saburo kept the real power and Kei died in 2023.
12. **The 2020 corporate hierarchy is being used for 2077.** The
    National Director / Regional VP / Regional Security-Sales-Bank Director
    ladder and the 19-seat board are 2020 sourcebook lore. The 2077 game
    shows the family and the Night City branch, not the full ladder. Treat the
    ladder as the org chart the corp *claims*, not a fully modelled 2077
    structure.
13. **The City Council relation is inferred from a 2070 event.** Lucius Rhyne
    invited Arasaka back to protect Night City from the NUSA; by 2077 the
    council is also tied to Night Corp and the mayor's office. The `patron`
    stance is a reading of that history, not a current contract.
14. **The Tyger Claws relation is asymmetric.** The wiki says "close ties" and
    "proxy gang"; it does not say the Claws are a formal ally. The `client`
    stance means Arasaka hires/uses them, not that they are loyal.
15. **The Militech stance is a cold war, not an open war.** The Fourth
    Corporate War (2022–25) and the 2070 NUSA standoff are historical; 2077 is
    mutual sabotage and rising tension. `rival` is the current stance; `war`
    would overstate it.
16. **6th Street's stance is inferred.** No explicit Arasaka gig or lore event
    was found; the `rival` stance comes from the gang's anti-corporate
    ideology and the Arasaka Industrial Park sitting in its Arroyo turf.
17. **Wakako's stance is hostile despite helping Takemura.** She lost a
    grandchild to Arasaka and disdains the corporation; her help in q112 is a
    favour to V/Takemura, not a pro-Arasaka alignment.
18. **The fixers are not a bloc.** Dino is `trade`, Wakako/Padre/El Capitán/
    Rogue are `hostile`, and the rest are `neutral`. Do not average them into
    "the fixers."
19. **No faction is an `ally`.** The matrix has zero ally rows. The closest is
    the Tyger Claws proxy network; the City Council is a patron relationship.
    A simulation that needs an Arasaka ally must create one or model a
    branch-level patron.
20. **The `patron`/`client` vocabulary is ambiguous for corps.** A corp buys
    from a supplier (is the corp the client or the patron?), sells security to
    a city (is the city the client?), and uses a gang as a proxy (is the gang
    the client?). This document states its reading in §3.1; the METHOD should
    define direction explicitly or add `supplier`/`contractor`.

### 5.1 Sources consulted

Local:

- `dist/extract/markers.jsonl` — leader locations and quest markers (Konpeki,
  Tower, Estate, parade, Industrial Park, Ebunike, Hellman, Oda, Smasher,
  Jenkins' office).
- `dist/extract/areas.jsonl` — Arasaka presence density and community names.
- `dist/extract/raw/**/always_loaded_{0,1,2}.streamingsector.json` — community
  registry templates and `characterRecordId` values for `Character.Saburo`,
  `Character.Yorinobu`, `Character.Hanako`, `Character.Takemura`,
  `Character.Smasher`, `Character.Cyberninja_Oda`, `Character.Michiko`,
  `Character.Haru_Kasai`, `Character.Grayson`, `Character.q000_corpo_*`.
- `data/sites/rosters.json` — 68 Arasaka units, 21 distinct records; no named
  leader.
- `data/factions.json` — faction codes used in the matrix.
- `docs/design/gameplay-systems.md` — archetype and pillar claims.
- `docs/research/factions/arasaka.md` — location catalogue and coordinates.
- `docs/research/factions/METHOD.md` §1.1–§1.2 — data pitfalls.
- `docs/research/factions/politics/METHOD.md` — politics method.
- `docs/research/factions/politics/maelstrom.md` — worked example.

Wiki:

- [Arasaka](https://cyberpunk.fandom.com/wiki/Arasaka)
- [List of Arasaka employees](https://cyberpunk.fandom.com/wiki/List_of_Arasaka_employees)
- [Saburo Arasaka](https://cyberpunk.fandom.com/wiki/Saburo_Arasaka)
- [Yorinobu Arasaka](https://cyberpunk.fandom.com/wiki/Yorinobu_Arasaka)
- [Hanako Arasaka](https://cyberpunk.fandom.com/wiki/Hanako_Arasaka)
- [Kei Arasaka](https://cyberpunk.fandom.com/wiki/Kei_Arasaka)
- [Michiko Arasaka (Kei's daughter)](https://cyberpunk.fandom.com/wiki/Michiko_Arasaka_(Kei%27s_daughter))
- [Goro Takemura](https://cyberpunk.fandom.com/wiki/Goro_Takemura)
- [Adam Smasher](https://cyberpunk.fandom.com/wiki/Adam_Smasher)
- [Sandayu Oda](https://cyberpunk.fandom.com/wiki/Sandayu_Oda)
- [Anders Hellman](https://cyberpunk.fandom.com/wiki/Anders_Hellman)
- [Susan Abernathy](https://cyberpunk.fandom.com/wiki/Susan_Abernathy)
- [Arthur Jenkins](https://cyberpunk.fandom.com/wiki/Arthur_Jenkins)
- [Carter Smith](https://cyberpunk.fandom.com/wiki/Carter_Smith)
- [Frank Nostra](https://cyberpunk.fandom.com/wiki/Frank_Nostra)
- [Arasaka Tower](https://cyberpunk.fandom.com/wiki/Arasaka_Tower)
- [Konpeki Plaza](https://cyberpunk.fandom.com/wiki/Konpeki_Plaza)
- [Arasaka Waterfront](https://cyberpunk.fandom.com/wiki/Arasaka_Waterfront)
- [Arasaka Estate](https://cyberpunk.fandom.com/wiki/Arasaka_Estate)
- [Arasaka Industrial Park](https://cyberpunk.fandom.com/wiki/Arasaka_Industrial_Park)
- [Mikoshi](https://cyberpunk.fandom.com/wiki/Mikoshi)
- [Relic](https://cyberpunk.fandom.com/wiki/Relic)
- [Militech](https://cyberpunk.fandom.com/wiki/Militech)
- [Kang Tao](https://cyberpunk.fandom.com/wiki/Kang_Tao)
- [Night Corp](https://cyberpunk.fandom.com/wiki/Night_Corp)
- [NUSA](https://cyberpunk.fandom.com/wiki/NUSA)
- [NCPD](https://cyberpunk.fandom.com/wiki/NCPD)
- [Tyger Claws](https://cyberpunk.fandom.com/wiki/Tyger_Claws)
- [6th Street](https://cyberpunk.fandom.com/wiki/6th_Street)
- [Valentinos](https://cyberpunk.fandom.com/wiki/Valentinos)
- [Wakako Okada](https://cyberpunk.fandom.com/wiki/Wakako_Okada)
- [Rogue Amendiares](https://cyberpunk.fandom.com/wiki/Rogue_Amendiares)
- [Dino Dinovic](https://cyberpunk.fandom.com/wiki/Dino_Dinovic)
- [Muamar Reyes](https://cyberpunk.fandom.com/wiki/Muamar_Reyes)
- [Zetatech](https://cyberpunk.fandom.com/wiki/Zetatech)
- [Trauma Team](https://cyberpunk.fandom.com/wiki/Trauma_Team)
- [The Corpo-Rat](https://cyberpunk.fandom.com/wiki/The_Corpo-Rat)
- [Totalimmortal](https://cyberpunk.fandom.com/wiki/Totalimmortal)
- [Nocturne Op55N1](https://cyberpunk.fandom.com/wiki/Nocturne_Op55N1)

---

## 6. Machine-readable block

```json
{
  "faction_code": "arasaka",
  "leaders": [
    {
      "name": "Saburo Arasaka",
      "role": "Chairman (1960-2077); CEO (1960-late 1990s, again 2023-2077); engram in Mikoshi",
      "character_record_id": "Character.Saburo",
      "location_name": "Konpeki Plaza / Arasaka Tower (Saburo's office, Mikoshi)",
      "open_world": false,
      "source": "raw always_loaded_1 community registry (Character.Saburo; phases q005_hotel_*, q101_*, #q201_ws_saburo_at_cp); markers q005_mrk_saburo_av_open_int, q113_06_sm_saburo_office, q113_07_sm_mikoshi; wiki Saburo Arasaka",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Yorinobu Arasaka",
      "role": "CEO (2077, after Saburo's murder); Taka faction leader",
      "character_record_id": "Character.Yorinobu",
      "location_name": "Konpeki Plaza suite / Arasaka Tower CEO floor",
      "open_world": false,
      "source": "raw always_loaded_1 community registry (Character.Yorinobu; phases q004_*, q005_*, q113_yorinobu_14_office*); markers mirror_sm_scene_konpeki_room, q113_12_sm_ceo_floor, q113_14_sm_yorinobu; wiki Yorinobu Arasaka",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Hanako Arasaka",
      "role": "Kiji faction head; legitimist claimant; unofficial spokeswoman",
      "character_record_id": "Character.Hanako",
      "location_name": "Arasaka Estate (North Oak) / Japantown parade / Arasaka Tower",
      "open_world": false,
      "source": "raw always_loaded_1 community registry (Character.Hanako; phases q112_hanako_*, q113_hanako_*, #q201_ws_hanako_*); markers q113_04_sm_hanako_estate, q112_08_sm_parade_speech, q115_00b_sm_hanako; wiki Hanako Arasaka",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Michiko Arasaka (Sanderson)",
      "role": "Hato faction head; board member",
      "character_record_id": "Character.Michiko",
      "location_name": "Arasaka Tower (boardroom / jungle level)",
      "open_world": false,
      "source": "raw always_loaded_1 community registry (Character.Michiko; phases q113_michiko_09_jungle*, #q113_michiko_10_jungle_combat); marker q113_10_sm_jungle_combat; wiki Michiko Arasaka (Kei's daughter)",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Kei Arasaka",
      "role": "CEO (late 1990s-2023); deceased",
      "character_record_id": null,
      "location_name": null,
      "open_world": false,
      "source": "wiki Kei Arasaka; wiki List of Arasaka employees",
      "confidence": "wiki+lore"
    },
    {
      "name": "Goro Takemura",
      "role": "Saburo's personal bodyguard; ex-special forces",
      "character_record_id": "Character.Takemura",
      "location_name": "Konpeki Plaza / Japantown / Arasaka Industrial Park / Arasaka Estate / Arasaka Tower",
      "open_world": false,
      "source": "raw always_loaded_1 community registry (Character.Takemura; phases q005_*, q101_*, q104_*, q112_*); markers q101_08_sm_takemura, q112_04_sm_takemura; wiki Goro Takemura",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Adam Smasher",
      "role": "Yorinobu's bodyguard; Head of Security after Saburo's murder; enforcer",
      "character_record_id": "Character.Smasher",
      "location_name": "Konpeki Plaza / Arasaka Tower / Ebunike Docks (base, via Grayson)",
      "open_world": false,
      "source": "raw always_loaded_1 community registry (Character.Smasher; boss variants Character.q113_boss_smasher, Character.main_boss_adam_smasher; phases q005_*, q101_*, q108_atlantis_bar, q112_safe_house_start); markers q113_13_sm_adam_smasher, smasher_marker, q005_14_sm_escape_smasher; wiki Adam Smasher",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Sandayu Oda",
      "role": "Hanako's bodyguard; cyberninja",
      "character_record_id": "Character.Cyberninja_Oda",
      "location_name": "Japantown parade / Arasaka Tower",
      "open_world": false,
      "source": "raw always_loaded_1 community registry (Character.Cyberninja_Oda; phases q112_cyberninja_08_bossfight, q112_cyberninja_oda_stealth); marker q112_00b_sm_secret_meeting_oda_car; wiki Sandayu Oda",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Anders Hellman",
      "role": "Relic project director; defected to Kang Tao",
      "character_record_id": "Character.Haru_Kasai",
      "location_name": "Kang Tao AV crash (Jackson Plains) / Sunset Motel / Arasaka Estate / Arasaka Orbital Station",
      "open_world": false,
      "source": "raw always_loaded_1 community registry (Character.Haru_Kasai; entries haru, anders_hellman_holo; phases q004_*, q005_*, q101_*, q104_*); markers q104_07b_sm_haru_found, q104_spn_motel_haru_scene, q113_03a_sm_haru_kasai_drive; wiki Anders Hellman (development name Haru Kasai)",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "name": "Jeremiah Grayson",
      "role": "Arasaka mercenary; Smasher's right-hand",
      "character_record_id": "Character.Grayson",
      "location_name": "Ebunike Docks",
      "open_world": false,
      "source": "raw always_loaded_1 community registry (Character.Grayson; phases q005_default, q103_*, q203_*, sq031_*); marker sq031_04_sm_grayson; wiki Chippin' In",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Susan Abernathy",
      "role": "Director of Special Operations, American HQ",
      "character_record_id": "Character.q000_corpo_abernathy",
      "location_name": "Arasaka Tower, Corpo Plaza",
      "open_world": false,
      "source": "raw always_loaded_1 community registry (Character.q000_corpo_abernathy; entry abernathy, phase conference); wiki Susan Abernathy",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Arthur Jenkins",
      "role": "Senior member and head of Counterintelligence, Night City",
      "character_record_id": "Character.q000_corpo_jenkins",
      "location_name": "Arasaka Tower (Jenkins' office, z~142)",
      "open_world": false,
      "source": "raw always_loaded_1 community registry (Character.q000_corpo_jenkins; entries jenkins, jenkins_holo; phases conference, desk); markers q000_corpo_jenkins_office_chair, q000_sm_corpo_03_jenkins; wiki Arthur Jenkins",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Arasaka Board of Directors",
      "role": "Collective sovereign: 19 Tokyo seats plus family shareholders",
      "character_record_id": null,
      "location_name": "Arasaka Tower, Tokyo / Night City boardroom",
      "open_world": false,
      "source": "wiki Arasaka (board structure: 54% family, 15% board, 31% public); wiki Totalimmortal",
      "confidence": "wiki"
    }
  ],
  "internal_factions": [
    {
      "name": "Kiji (Green Pheasant)",
      "leader": "Hanako Arasaka",
      "goals": "Continue Saburo/Kei's order; conservative technocracy; stability; peace with the NUSA on Arasaka's terms",
      "members_hint": "Hanako; Takemura; Oda; Kiji-aligned board traditionalists; Arasaka Estate and Tower security",
      "source": "wiki Arasaka (Kiji description); wiki Hanako Arasaka; wiki Goro Takemura; wiki Sandayu Oda",
      "confidence": "wiki"
    },
    {
      "name": "Taka (Hawk)",
      "leader": "Yorinobu Arasaka",
      "goals": "Sabotage Arasaka from within; pro-Western reforms; direct, uncompromising action; military coup",
      "members_hint": "Yorinobu; Adam Smasher; Taka loyalist soldiers in Night City, Kyoto, Dubai and Paris; militant board members",
      "source": "wiki Arasaka (Taka description); wiki Yorinobu Arasaka; wiki Adam Smasher",
      "confidence": "wiki"
    },
    {
      "name": "Hato (Dove)",
      "leader": "Michiko Arasaka (Sanderson)",
      "goals": "Liberal reforms; deeper changes; US ties; the least powerful bloc",
      "members_hint": "Michiko; Danger Gal; some politicians and media personalities; board liberals",
      "source": "wiki Arasaka (Hato description); wiki Michiko Arasaka (Kei's daughter)",
      "confidence": "wiki"
    },
    {
      "name": "The Board / old guard",
      "leader": null,
      "goals": "Preserve the company and their seats; avoid open conflict; accept the strongest claimant",
      "members_hint": "19 Tokyo board seats; family shareholders (54%); branch directors from Paris, Shanghai and Kinshasa",
      "source": "wiki Arasaka (board structure); wiki Totalimmortal",
      "confidence": "wiki"
    },
    {
      "name": "Saburo's engram / old order",
      "leader": "Saburo Arasaka (engram)",
      "goals": "Restore Saburo's control; overwrite Yorinobu; revert the reforms; peace with Militech and the NUSA",
      "members_hint": "Saburo's engram in Mikoshi; Hanako; Kiji; Hellman's Relic team",
      "source": "wiki Saburo Arasaka; wiki Hanako Arasaka; wiki Totalimmortal",
      "confidence": "wiki"
    },
    {
      "name": "Smasher's security apparatus",
      "leader": "Adam Smasher",
      "goals": "Carry out Yorinobu's dirty work; protect the CEO; no loose ends",
      "members_hint": "Smasher; Grayson; Arasaka security teams; Ebunike base",
      "source": "wiki Adam Smasher; wiki Chippin' In; raw registry Character.Smasher and Character.Grayson",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Hellman's R&D / defector wing",
      "leader": "Anders Hellman",
      "goals": "Survive; monetise the Relic; sell loyalty to the highest bidder",
      "members_hint": "Hellman; Relic team; Kang Tao contacts",
      "source": "wiki Anders Hellman; raw registry Character.Haru_Kasai",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Counterintelligence vs Special Operations",
      "leader": "Arthur Jenkins / Susan Abernathy",
      "goals": "Promotion, jurisdiction and survival; each tries to purge the other",
      "members_hint": "Jenkins' counterintel team (V, Carter Smith, Frank Nostra, Harry); Abernathy's Special Operations; Arasaka Tower offices",
      "source": "wiki Arthur Jenkins; wiki Susan Abernathy; wiki Carter Smith; wiki Frank Nostra; raw registry q000_corpo_*",
      "confidence": "game-data+wiki"
    }
  ],
  "relations": [
    {
      "faction_code": "tyger_claws",
      "stance": "client",
      "evidence": "Arasaka-backed motorcycle club; close ties to Arasaka upper management, which outsourced side-jobs and paid in cybertech and military-grade weapons; Arasaka sleeper agents joined the gang after 2023; still close in the 2070s [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "valentinos",
      "stance": "trade",
      "evidence": "Arasaka contracted Valentino Jose Luis to frame Militech for an attack on an Arasaka facility (Gig: On a Tight Leash); a one-off proxy hire, not a gang-level relationship [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "militech",
      "stance": "rival",
      "evidence": "Fourth Corporate War 2022-25; 2070 NUSA/Militech invasion of Night City forced back by Arasaka's supercarrier; 2077 mutual sabotage and rising tensions [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "kang_tao",
      "stance": "rival",
      "evidence": "Kang Tao poached Arasaka technology and employees; Hellman defected to Kang Tao and was extracted by its AV; Kang Tao is Arasaka's top smart-weapons competitor [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "biotechnica",
      "stance": "neutral",
      "evidence": "No attested interaction; a biotech supplier, not a Night City turf actor [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "petrochem",
      "stance": "neutral",
      "evidence": "No attested interaction; fuel/energy supplier only [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "barghest",
      "stance": "neutral",
      "evidence": "No attested interaction; the Dogtown KGB hologram set piece is not an Arasaka relationship [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "sixth_street",
      "stance": "rival",
      "evidence": "Anti-corporate paramilitary founded by Fourth Corporate War veterans; Arasaka Industrial Park sits in 6th Street's Arroyo turf; no explicit Arasaka gig found [game-data] [wiki] [inferred]",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "faction_code": "aldecaldos",
      "stance": "hostile",
      "evidence": "The Star ending: Aldecaldos invade Arasaka Tower and destroy Mikoshi; dependent on V's choice [wiki]",
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
      "stance": "neutral",
      "evidence": "No attested interaction; Animals hire out as bodyguards but no Arasaka contract found [wiki] [inferred]",
      "confidence": "wiki+inferred"
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
      "evidence": "Maelstrom raids corporate transports and sells stolen tech; Arasaka merc Grayson guards the Ebunike in Maelstrom territory; 9 Maelstrom hold Memorial Ring West inside an Arasaka-owned sub-territory [wiki] [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "voodoo_boys",
      "stance": "neutral",
      "evidence": "No attested interaction; VDBs hack corporate databanks but no Arasaka-specific operation found [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "ncpd",
      "stance": "trade",
      "evidence": "NCPD is beholden to Arasaka and Militech interests; Arasaka puts interests in the PD expecting return; official sponsor is Night Corp [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "night_corp",
      "stance": "rival",
      "evidence": "Night Corp lost the race for Night City influence to Arasaka and Militech; still runs public administration and funds NCPD [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "city_council",
      "stance": "patron",
      "evidence": "Councilman Lucius Rhyne invited Arasaka back to protect Night City from the NUSA in 2070; Arasaka arrived with a supercarrier and forced NUSA/Militech to retreat; Arasaka effectively controls the city [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "scavengers",
      "stance": "neutral",
      "evidence": "No attested interaction; Arasaka security would treat scavs as criminals, but no specific event [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_regina",
      "stance": "neutral",
      "evidence": "No Arasaka-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_wakako",
      "stance": "hostile",
      "evidence": "Wakako lost a grandchild to Arasaka and has disdained the corporation since; she helps Takemura in q112 on V's behalf, not out of pro-Arasaka sympathy [wiki] [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_padre",
      "stance": "hostile",
      "evidence": "Padre gives the gig On a Tight Leash, which stops Arasaka's attempt to frame Militech via Valentino Jose Luis [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "fixer_el_capitan",
      "stance": "hostile",
      "evidence": "El Capitan gives the gig Baby Let Me Take You, robbing an Arasaka dockyard for medical supplies; he hates Arasaka for dumping toxic waste in Rancho Coronado [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "fixer_dakota",
      "stance": "neutral",
      "evidence": "No Arasaka-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_dino",
      "stance": "trade",
      "evidence": "Dino profits from the corpo contracts generated by Hanako Arasaka's arrival in Downtown; transactional, not loyal [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "fixer_rogue",
      "stance": "hostile",
      "evidence": "Rogue raided Arasaka Tower in 2013 and 2023; Chippin' In targets Smasher/Grayson and the Ebunike; she works with V against Arasaka in the Sun ending [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "fixer_mr_hands",
      "stance": "neutral",
      "evidence": "No Arasaka-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "afterlife",
      "stance": "neutral",
      "evidence": "Neutral merc marketplace; Rogue's anti-Arasaka operations do not make the Afterlife an Arasaka enemy [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "nusa",
      "stance": "hostile",
      "evidence": "NUSA/Militech invaded Night City in 2070; Arasaka's supercarrier forced them to retreat; NUSA is Militech's parent and Arasaka's geopolitical rival [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "zetatech",
      "stance": "trade",
      "evidence": "Arasaka uses Zetatech Valgus helicopters and Atlus AVs; the Industrial Park retrofits Zetatech AVs; a supplier relationship [wiki] [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "trauma_team",
      "stance": "trade",
      "evidence": "Trauma Team partners with Arasaka and gives Arasaka employees memberships; Arasaka is a client [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "news54",
      "stance": "rival",
      "evidence": "Network News 54 lost reporters investigating Arasaka scandals; Arasaka avoids direct confrontation while feeding it bad press about rivals [wiki]",
      "confidence": "wiki"
    }
  ]
}
```
