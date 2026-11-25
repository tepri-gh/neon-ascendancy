# Kang Tao — Leadership, Internal Politics and External Relations

Status: faction politics research run, 2026-11-25. One faction, one document.
Scope: Cyberpunk 2077 2.5 + Phantom Liberty, campaign disabled; the mod's
§7 alternate timeline applies. This document covers who a player can join
under, climb past, ally with or remove inside Kang Tao; the corporate blocs;
and the external-relations matrix needed for wars, alliances and "guarantor"
support when a player founds an organisation.

Method: this document follows the evidence rules in
[`METHOD.md`](./METHOD.md) including the §1.1–§1.3 corrections, and the data
pitfalls in [`../METHOD.md`](../METHOD.md) §1.1–§1.2. The location catalogue
for Kang Tao is [`../kang-tao.md`](../kang-tao.md); this document maps people
and politics onto those places and does not repeat every coordinate.
`AGENTS.md` was read first. No commits, no game launch; helper scripts ran
outside the repo under `python3 -I`.

**Up front, because it shapes every section: the political footprint is thin.**
Kang Tao has **no named 2077 CEO, no named North American Division director,
and no named leadership in Night City**. The wiki's `List of Kang Tao
employees` has three entries, one of them "TBA". The only named Kang Tao people
with game records are **Karl Ginsky**, a corporate employee, and **Azevedo**, a
security chief, both in the *Nasty Hangover* gig. The faction's Night City
presence is one HQ building, one overpass encounter, one warehouse kill team
and a Badlands quest corridor. This document reports that honestly rather than
inventing a boardroom.

## Evidence tags and presence classes

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Position, site, community, roster or raw-registry record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/comic/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My reasoning links a named person, place or stance to a record; reasoning stated | Weak, flagged |

Presence classes used in this document: `ambient` = persists in free roam
without a quest; `world-activity` = gig, scanner hustle or NCPD activity;
`story` = gated by a main or side quest; `prologue` = a lifepath prologue
(**Kang Tao has none**); `off-map` = alive/named in 2077 but never spawned;
`mentioned` = named only in shards or dialogue; `historical` = not present in
2077. The JSON `open_world` flag is `true` only for `ambient` and
`world-activity`.

**Alternate-timeline rule.** The mod's §7 removes the Konpeki heist, the Relic
plot and the Phantom Liberty events. That removes the **q104 Hellman
extraction** (*Ghost Town* → *Lightning Breaks* → *Life During Wartime*) from
the mod's canon, because the whole chain exists to fix the Relic. The places
and the structural relationships remain; the specific incident does not. The
*Nasty Hangover* gig and the Hanford Overpass world activity are not Relic-plot
content, so they remain. Where this changes a stance, it is flagged in §3.

---

## 1. Leadership and ranks

### 1.1 The 2077 chain of command

Kang Tao is a Chinese state-backed weapons manufacturer: 1,000,000 employees
and €$525 billion in 2077, restructured in 2050 by Colonel Shiming Xu, with its
global headquarters in Shenyang, China. Its business is firearms — above all
Smart-class weapons — plus a growing mercenary and security arm, and cyberware
through the QianT subsidiary. `[wiki]`

The top is unusually blank. The wiki gives a founder, a board member and one
"TBA" employee; it does not give a 2077 CEO.

| Name | 2077 role | Character record | Location / influence point | Presence class | Source | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| **Shiming Xu** | Founder and restructurer of the modern company; former Chinese army colonel; installed 2046, relaunch 2050 | — (mentioned only) | Shenyang, China; the 2046 predecessor firm | `off-map` | Wiki *Shiming Xu*; wiki *Kang Tao*; *The World of Cyberpunk 2077* | `[wiki]` |
| **Xiaohan Ling** | Board member (2077); the only named 2077 director | — (mentioned only) | Shenyang; stayed one week at Konpeki Plaza, Night City, in 2077 | `off-map` | Wiki *List of Kang Tao employees*; wiki *Xiaohan Ling*; *The World of Cyberpunk 2077* p.138 | `[wiki]` |
| **Yuan Huo** | Employee (2077); role "TBA" | — (mentioned only) | — | `off-map` | Wiki *List of Kang Tao employees*; wiki *Yuan Huo* | `[wiki]` |
| **Wong Nien-jen** | CEO (2020, Taiwan-era company) | — (mentioned only) | Taipei, Taiwan (2020 HQ) | `historical` | Wiki *Kang Tao* infobox | `[wiki]` `[lore]` |
| **Kang Tao Board of Directors** | Collective sovereign; Xiaohan Ling is the only named 2077 member | — (no individual records) | Shenyang, China | `off-map` | Wiki *Kang Tao*; wiki *List of Kang Tao employees* | `[wiki]` |
| **North American Division director** | Regional head of the North American Division; unnamed in every source | — (no record) | Kang Tao Building, Corporate Plaza, City Center | `off-map` | Wiki *Kang Tao Building* (`type = North American Division HQ / Regional HQ`); no employee record found | `[wiki]` `[inferred]` |
| **CEO (2077)** | Chief executive; **unnamed** | — (no record) | Shenyang, China | `off-map` | Wiki *Kang Tao* infobox (no 2077 CEO); employee list has no CEO | `[wiki]` `[inferred]` |

Notes:

- **The employee list is the whole named roster.** `List of Kang Tao
  employees` has three entries: Shiming Xu (founder), Yuan Huo (employee,
  TBA) and Xiaohan Ling (board member). The `<Faction> Members` page is empty;
  the main page's `{{Main|…}}` link is the employee list. `[wiki]`
- **Xu is the restructurer, not the 1990s founder.** The infobox gives
  `founder = Shiming Xu (2050)`, `established = 1990s`, and
  `ceo = Wong Nien-jen (2020)` / `Shiming Xu (2046)`. The body says the
  Chinese government appointed Xu in 2046 to manage an obsolete, collapsing
  defense corporation, and he renamed/relaunched it as Kang Tao in 2050. Treat
  the 2050 "founding" as the modern company's founding, not the original
  firm's. `[wiki]`
- **The Taiwanese-to-Chinese shift is the biggest leadership discontinuity.**
  Kang Tao was Taiwanese in 2020, independent of Japanese business interests,
  and headquartered in Taipei. It was restructured into a Chinese-based
  company in the 2040s, with government backing. By 2077 the state-champion
  identity is settled; the old Taiwanese management is not visible. `[wiki]`
- **Xiaohan Ling's Konpeki stay is a PR anecdote, not a power base.** She is a
  board member who praised the hotel to the media; there is no Night City
  office, staff or faction attached to her. `[wiki]`
- **The 2077 CEO is a genuine blank.** The wiki gives no name, no record and no
  succession. A simulation must either keep the seat abstract or invent a
  simulation agent. `[inferred]`

### 1.2 The Night City / North American Division branch

The Kang Tao Building in Corporate Plaza is the **North American Division HQ**
and regional HQ, not a sales kiosk. It is next to Petrochem Tower and reached
by a bridge from Memorial Park; it is the only wiki-documented Kang Tao address
in Night City. In game it is site 20 `ma_cct_cpz_16`
(`-1127.822, 546.952, 17.890`), inside the Kang Tao-owned sub-territory
`cpz_kang_tao_sector`. `[wiki]` `[game-data]`

The branch is thin in people and thick in guards:

| Layer | Who | Evidence |
| --- | --- | --- |
| Regional HQ | Unnamed North American Division director | Wiki *Kang Tao Building* (`type = North American Division HQ / Regional HQ`); no employee record |
| Corporate staff | **Karl Ginsky**, employee and shard carrier | `Character.sts_std_arr_06_karl_greenski`, roster site 382, faction 22; *Nasty Hangover* `[game-data]` `[wiki]` |
| Security detail | **Azevedo**, security chief | `Character.sts_std_arr_06_sec_chief`, roster site 382, faction 22; entry `azevedo` in the Kang Tao corporate community `[game-data]` `[inferred]` |
| Facility garrison | Generic rangers, soldiers and androids | Site 20: 5 units; site 60: 9; site 19: 3; site 382: 7 `[game-data]` |
| Covert channel | **QianT**, the cyberware subsidiary/shell | Wiki *QianT*: handled the Hellman extraction traffic; no address or named staff `[wiki]` |
| State link | The Chinese government / party directorate | Wiki *Kang Tao*: government backing, alleged connections, government-funded research `[wiki]` |

The branch has **no named director, no boardroom scene and no interior**. The
Kang Tao Building is `is_interior=0`, `has_doors=0`, with zero devices and zero
workslots; its gameplay record is a plaza volume with guard areas and enemy
workspots (location doc §3.1, §5). A politics layer cannot stage a board meeting
inside it. `[game-data]`

The branch's two documented initiatives are both expansionist:

1. **Pacifica server facility.** In 2077 Kang Tao expressed interest in buying
   property in Pacifica to build a new **server facility**. The City Council
   debated selling the lot for a single eurodollar in exchange for a Kang Tao
   pledge to help quell the district's crime. No deal was made. `[wiki]`
2. **Hellman recruitment.** Kang Tao negotiated with Arasaka's Relic director
   Anders Hellman before the Konpeki heist and routed the extraction traffic
   through QianT servers. In vanilla 2077 the extraction ends with a shoot-down
   over Jackson Plains; the mod's §7 removes that chain, but the recruitment
   attempt is pre-heist and remains evidence of the branch's talent-poaching
   role. `[wiki]`

The branch is the best model for a player joining Kang Tao as an employee, but
it is thinner than Arasaka's Corpo lifepath (which has a playable prologue) and
Militech's branch (which has Stout, Thorston and Roider). The closest templates
are **Ginsky** (a corporate employee with a shard) and **Azevedo** (a security
chief with a kill team). `[inferred]`

### 1.3 Succession history

| Period | Leader | How the change happened |
| --- | --- | --- |
| 1990s–2046 | Taiwanese independent management; **Wong Nien-jen** (CEO, 2020) | Kang Tao was a Taiwanese small-arms manufacturer, independent of Japanese business interests, popular with Asian gangers. The DataKrash-era CEO committed suicide (name and date not given). `[wiki]` |
| 2046 | **Colonel Shiming Xu** | The Chinese government appointed Xu, a former army colonel, to manage an obsolete, collapsing defense corporation kept alive by government subsidies. `[wiki]` |
| 2050 | **Shiming Xu** | Xu renamed/relaunched the company as Kang Tao and shipped the A-22B Chao "smart" pistol. Government connections and government-funded research facilities followed. `[wiki]` |
| 2050–2077 | **Unnamed management** | Smart-weapons expansion; top-tier manufacturer alongside Tsunami Arms and Arasaka; stock tripled since 2072; leading arms exporter in Asia. `[wiki]` |
| 2077 | **Unnamed CEO; board incl. Xiaohan Ling** | €$525bn, 1,000,000 employees, Shenyang HQ. A Hangzhou refinery explosion killed over 50,000; official accounts cleared the company. Kang Tao bid for a Pacifica server facility; no deal. Ranked 4th-best employer in Night City. `[wiki]` |

The pattern is **state-directed appointment, not dynastic succession**. The
founder of the modern company is a former colonel installed by the government;
the current CEO is unnamed; the board is the only continuous sovereign. That is
the opposite of Arasaka's family line and closer to Militech's institutional
succession — except that Kang Tao's institutional owner is the Chinese state,
not a national government that also buys 60% of its output. `[wiki]`
`[inferred]`

The historical fault line is the **Taiwanese-origin old guard vs the Chinese
state restructuring**. The 2020 company was Taiwanese and proud of staying
independent of Japanese interests; the 2040s restructuring made it a Chinese
state champion. By 2077 the old guard is not visible, but the shift explains
the company's secrecy, its government-protected reputation and its willingness
to use a shell company (QianT) for sensitive work. `[wiki]` `[inferred]`

### 1.4 Rank structure, entry and advancement

Kang Tao publishes almost nothing about its internal culture. The reconstruction
below uses the wiki's corporate facts, the in-game enemy records and the one
employee gig. It is a reconstruction, not a published org chart.

**Corporate ladder.**

1. **Board of Directors (Shenyang).** Collective sovereign; Xiaohan Ling is the
   only named 2077 member. The board manages the state relationship and the
   unnamed CEO. `[wiki]`
2. **CEO.** Unnamed in 2077; state-appointed or board-approved; the modern
   company's founder was a state appointee. `[wiki]`
3. **National / regional director.** The North American Division director runs
   the Corpo Plaza HQ. Unnamed. `[wiki]` `[inferred]`
4. **Area / local / district / site managers.** The departmental chain. No
   named examples in Night City. `[inferred]`
5. **Employees.** Karl Ginsky is the only named 2077 employee. The package:
   Trauma Team Gold, a 50-year loyalty pledge, and a 4th-place ranking in the
   *Big 5 Employers in Night City – 2077* shard. `[wiki]` `[game-data]`

**Security ladder** (reconstructed from roster records and the wiki's Kang Tao
enemy pages; `[game-data]` `[wiki]`):

1. **Security chief** — `Character.sts_std_arr_06_sec_chief` (Azevedo); commands
   a detail or site.
2. **Officer** — `Character.gle_kangtao_officer_grenadier3_mah_elite`; elite
   grenadier; leads the Hanford Overpass squad.
3. **Ranger** — `ranger1_ranged2_dian_ma`; the standard guard/patrol rank and
   the most common record in the rosters.
4. **Soldier** — `soldier2_shotgun2/3_zhuo_mah_rare/elite`; shotgun assault.
5. **Rapid** — wiki shotgunner; the "Elite Rapid" is the veteran variant.
6. **Heavy** — wiki grenadier; carries the A-22B Chao.
7. **Sniper** — wiki fast sniper; Ashura/Nekomata and Sandevistan.
8. **Support Unit** — wiki ranged support.
9. **Android / Robot** — `android_android2_dian_ma`, a Robot R Mk.2 variant.
   Machines are not a garrison and are reported separately (../METHOD.md
   §1.2.4).

**Entry and advancement.**

- **There is no Kang Tao prologue or lifepath.** The Corpo lifepath
  (`q000_corpo_*`) is Arasaka's. A player joining Kang Tao must be given a
  branch or a security billet by the mod, not by the game. `[game-data]`
- **The security arm is military-style.** The ranks are ranger/soldier/rapid/
  heavy/sniper/officer, and the modern company's founder was a colonel. Infer
  that military or mercenary experience is the route into the security arm;
  the corporate arm hires locally (Ginsky, Azevedo). `[inferred]`
- **The 50-year pledge is one-way.** The *Nasty Hangover* kill team arrives to
  recover a stolen shard and silence the employee who lost it. The company
  offers Trauma Team Gold and a top-5 employer ranking; it also sends a kill
  team after its own people. That is the strongest single fact about the
  employee contract. `[game-data]` `[wiki]`
- **The failure state is disposal, not demotion.** Ginsky is not demoted; he is
  a loose end. This mirrors Militech's disposal culture, not Arasaka's purges.
  `[inferred]`
- **No academy or promotion path is attested.** Unlike Arasaka Academy or
  Militech's officer corps, Kang Tao has no named training institution. The
  ladder is opaque by design. `[inferred]`

**Practical consequence for the mod:** a player joining Kang Tao should enter
as a **corporate employee** or a **security ranger**, not as a Corpo. The climb
is ranger → officer → security chief, or employee → manager → branch director.
The board/CEO tier is closed and unnamed. Promotion should be gated on
deniability and results, and the failure state should be a kill team, not a
performance review. `[inferred]`

### 1.5 Named members mapped to game data

`data/sites/rosters.json` contains **24 Kang Tao units across 4 sites and 10
distinct records**. Exactly **two are named people**: Karl Ginsky (employee)
and Azevedo (security chief). The rest are `ranger*`, `soldier*`, `officer*`
and `android*` variants. The named leadership lives in the wiki, not in the
rosters. `[game-data]`

| Name | Role / note | Character record | Community / marker | Location | Presence class | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| Shiming Xu | Founder/restructurer; ex-colonel | — | — | Shenyang | `off-map` | `[wiki]` |
| Xiaohan Ling | Board member | — | — | Shenyang; Konpeki Plaza (2077 stay) | `off-map` | `[wiki]` |
| Yuan Huo | Employee; role TBA | — | — | — | `off-map` | `[wiki]` |
| Wong Nien-jen | CEO (2020) | — | — | Taipei | `historical` | `[wiki]` `[lore]` |
| Karl Ginsky | Corporate employee; stolen-shard carrier | `Character.sts_std_arr_06_karl_greenski` | Entry `ginsky`, community `15970220439262687998`, spots `#arr_06_ws_ginsky*` | 6th Street warehouse, Arroyo (Hargreaves St.) | `world-activity` | `[game-data]` `[wiki]` `[inferred]` |
| Azevedo | Security chief; leads the recovery/kill team | `Character.sts_std_arr_06_sec_chief` | Entry `azevedo`, community `15970220439262687998`, spots `#arr_06_ws_azevedo*` | 6th Street warehouse, Arroyo | `world-activity` | `[game-data]` `[inferred]` |
| Kang Tao Board of Directors | Collective sovereign | — | — | Shenyang | `off-map` | `[wiki]` |
| North American Division director | Regional head; unnamed | — | — | Kang Tao Building, Corpo Plaza | `off-map` | `[wiki]` `[inferred]` |
| Hanford Overpass officer | Generic elite grenadier | `Character.gle_kangtao_officer_grenadier3_mah_elite` | Site 60, entry `ganger_002` | Hanford Overpass, Glen | `world-activity` | `[game-data]` |
| q104 pilot / paramedic | Generic Kang Tao escort | `Character.q104_av_pilot`, `Character.q104_kang_paramedic` | q104 communities | Jackson Plains / fuel station | `story` (removed by §7) | `[game-data]` |

Data cautions:

- **Ginsky vs Greenski.** The wiki spells the employee "Karl Ginsky"; the
  record is `Character.sts_std_arr_06_karl_greenski`; the registry entry is
  `ginsky`. Same person, three spellings. Do not seed a second "Greenski".
  `[game-data]` `[wiki]`
- **Azevedo is an entry name, not a wiki person.** The record is a generic
  `sec_chief` slot. The name may be a local hire; do not seed him as a top
  leader. `[game-data]` `[inferred]`
- **The Hanford Overpass officer is generic.** The wiki's "Assault in Progress
  on Skyline South" is the encounter; there is no named leader record.
  `[game-data]` `[wiki]`
- **No named Kang Tao leader is in `data/sites/rosters.json`.** The two named
  records are the employee and the security chief. The off-map people are
  wiki-only. `[game-data]`
- **The Downtown glamdoc androids are not a Kang Tao holding.**
  `Character.kangtao_android_android2_dian_ma_dtn_glamdoc` are the two security
  androids at Serena Zhao's glamdoc clinic; the clinic is a 2.5 vendor, not a
  Kang Tao business. `[game-data]` `[wiki]`
- **The Phantom Liberty courier-loop records are fake co-presence.**
  `sa_ep1_*_courier_loop_enemies_kangtao_*` put Kang Tao in a shared enemy pool
  with six other factions. Exclude them from relations evidence
  (../METHOD.md §1.3.3). `[game-data]`

### 1.6 What the game actually spawns (campaign disabled)

A wiki infobox does not mean an actor in free roam. This is what exists:

**`ambient` — persists in free roam, no quest required.**

- Generic Kang Tao guards at the Kang Tao Building (site 20, 5 units), the
  Hanford Overpass (site 60, 9 units) and the Corpo Plaza hustle (site 19,
  3 units). No named leader. `[game-data]`

**`world-activity` — free-roam content, activity-gated.**

- **Karl Ginsky** and **Azevedo**, plus three rangers and two reinforcements,
  in *Gig: Nasty Hangover* (site 382 `sts_std_arr_06`). `[game-data]` `[wiki]`
- The **Hanford Overpass Assault in Progress**: 9 roster units, including an
  elite grenadier officer and three androids. `[game-data]` `[wiki]`
- The **Corpo Plaza scanner hustle** (site 19): 3 units on Militech's HQ
  concourse sub-territory. `[game-data]`

**`story` — gated by a main or side job.**

- The **q104 Hellman extraction**: a generic Kang Tao pilot, paramedic, rangers
  and shotgun troops across the fuel station, crash site and airstrip. In
  vanilla 2077 this is a main-job chain; **the mod's §7 removes it**. `[game-data]`
  `[wiki]`

**`off-map` — alive/named in 2077, never spawned.**

- Shiming Xu, Xiaohan Ling, Yuan Huo, the board, the unnamed North American
  Division director. `[wiki]`

**`historical` — not in 2077.**

- Wong Nien-jen and the 2020 Taiwanese management. `[wiki]` `[lore]`

**The finding.** **No named Kang Tao top leader is open-world.** The highest-
ranking named Kang Tao person a player can meet without a story quest is a
**security chief** (Azevedo) or a **corporate employee** (Ginsky), both in a
fixer gig. Everything above them is `off-map`. The mod must spawn the
leadership, not expect the game to provide it. `[game-data]` `[inferred]`

Caveat: "campaign disabled" may also suppress gigs and world activities. The
`world-activity` rows are the best reuse candidates, but they need an in-game
spawn check. The `story` row is the one to remove with the Relic plot; the
`off-map` people are the ones to replace with simulation agents. `[inferred]`

### 1.7 Player-path hooks

| Person / body | Join under | Climb past | Ally with | Remove |
| --- | --- | --- | --- | --- |
| **North American Division (unnamed director)** | The commercial branch: sales, contracts, Pacifica, talent recruitment | The director is the ceiling; Shenyang is above; the board is the sovereign | QianT, the security wing, the city council channel | Remove the director to decapitate the branch; keep the building for the seat |
| **The security arm (Azevedo)** | The ranger/officer ladder; bodyguard and kill-team work | The security chief is the local ceiling; the branch director is above | The kill team, QianT, the state | Remove Azevedo to break the recovery apparatus |
| **Karl Ginsky** | The employee path: a suit with a shard, disposable | There is no ladder from his seat; he is a cautionary tale | Ally with him for the shard or sell him out | The corp will remove him; the player can beat them to it |
| **QianT** | The deniable path: covert ops, extraction, cyberware | QianT has no named staff; the ladder is invisible | The shell company, the state, the branch | Expose or seize QianT to cut the covert channel |
| **The board / Chinese state** | The state-champion line: defense supply, secrecy, government R&D | The board is the sovereign; the CEO is unnamed | The state, the board, the arms/R&D establishment | Remove the state relationship and the company loses its shield |

The design consequence: Kang Tao has **no joinable named leader**. A player
joins a *branch* or a *security detail*, not a person. The two exits are the
**quiet exit** (Ginsky: a defector with a shard) and the **loud exit** (Azevedo:
a security chief with a private detail and the corp's own hardware). The mod
must create the branch director and CEO as simulation agents. `[inferred]`

---

## 2. Internal political factions

### 2.1 The blocs

**Kang Tao has no attested named internal factions.** Unlike Arasaka's
Kiji/Taka/Hato or Maelstrom's Royce/Brick, the wiki gives no named cliques and
no internal-war narrative. The blocs below are **structural**, derived from the
org chart and the documented operations. They are simulation scaffolding, not
canon; rows that are not directly attested are tagged `[inferred]`.

| Bloc | Leader(s) | What it wants | Presence / members hint | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- |
| **The Chinese state directorate / Shenyang line** | Unnamed state-appointed management; the board | State priorities: defense supply, strategic technology, secrecy, government-funded R&D, protect the company's government relations | Shenyang HQ; Xiaohan Ling; QianT; government-funded research | Wiki *Kang Tao* (government backing, alleged connections, government-funded research facilities); wiki *Shiming Xu* | `[wiki]` |
| **The North American expansion wing** | Unnamed North American Division director; local staff | Grow Night City market share; win security contracts; buy a Pacifica server facility; recruit foreign talent (Hellman) | Kang Tao Building; Ginsky; QianT; Pacifica bid; Hellman recruitment | Wiki *Kang Tao Building*; wiki *Kang Tao* (Pacifica); wiki *Pacifica (2077)* (server facility); wiki *QianT* | `[wiki]` `[game-data]` `[inferred]` |
| **The smart-weapons R&D / arms establishment** | Unnamed; Xiaohan Ling on the board | Protect the smart-weapon moat; steal competitor research; keep the A-22B/G-58/L-69 line dominant | Shenyang R&D and factories (off-map); no Night City lab | Wiki *Kang Tao* (products, smart-weapon specialization, research theft); wiki *QianT* | `[wiki]` |
| **The security and mercenary services wing** | Unnamed; Azevedo is a field-level security chief | Sell security, bodyguard and escort contracts; run extraditions and kill teams; expand beyond hardware | Rangers, soldiers, rapids, heavies, snipers, androids; Hanford Overpass; Nasty Hangover; q104 escort | Wiki *Kang Tao* (mercenary and security markets); roster records; wiki unit pages | `[game-data]` `[wiki]` |
| **QianT deniable-operations wing** | Unnamed | Handle sensitive operations Kang Tao cannot be publicly associated with; carry extraction traffic; sell high-end cyberware | QianT subsidiary; Hellman extraction servers; no address or named staff | Wiki *QianT*; wiki *Kang Tao* (affiliations) | `[wiki]` |
| **The board / Shenyang old guard** | Kang Tao Board of Directors (Xiaohan Ling the only named member) | Preserve the company and the state relationship; avoid scandal; manage the unnamed CEO succession | Shenyang board; Xiaohan Ling; no other named 2077 directors | Wiki *List of Kang Tao employees*; wiki *Kang Tao* | `[wiki]` |

### 2.2 The state-market fault line

The central internal contradiction is that **Kang Tao is a state-backed
champion with a commercial expansion arm.** Both halves are documented:

- The Chinese government appointed Xu, funded the research facilities, and its
  relations "kept it out of trouble in the past." The state is the shield.
  `[wiki]`
- The company is a top-tier arms exporter with 1,000,000 employees and
  €$525 billion; it wants market share, not just state contracts. `[wiki]`
- The **Pacifica server-facility bid** is a commercial real-estate and data
  play that requires the Night City Council and a crime-clearance pledge; a
  state directorate would not negotiate that. `[wiki]`
- The **Hellman recruitment** is a talent poach run through QianT, not a state
  program. `[wiki]`

Two readings coexist and imply opposite strategies:

1. **State-first.** Serve the Chinese state, protect the defense base, keep the
   research secret, avoid foreign entanglements that expose the company.
2. **Market-first.** Expand into Night City, buy Pacifica, sell security
   contracts, poach foreign talent, and use QianT to keep the brand clean.

For a simulation, score every Kang Tao internal conflict as **"serve the
state" vs "grow the market."** The Taiwanese-origin vs Chinese-state shift is
the historical version of the same fault line; by 2077 it is mostly absorbed,
but it explains why the leadership is opaque and why the company prefers a
shell company to a public subsidiary. `[inferred]`

### 2.3 HQ vs branch

- **Shenyang** holds the board, the CEO, R&D, the factories and the state
  relationship. It is the source of legitimacy.
- **The North American Division** holds the only Night City building, the
  Pacifica bid, the Hellman recruitment and the kill teams. It is the growth
  engine.
- The branch has no named director and no interior, so its autonomy is
  undocumented. The Hellman extraction ran through QianT servers, which
  suggests the branch can run sensitive operations without the public brand.
  `[wiki]`
- For a simulation, control of the Kang Tao Building plus Shenyang recognition
  is the win condition for a branch bloc. `[inferred]`

### 2.4 Arms vs services

- The company's identity is smart weapons; its growth line is mercenary and
  security services. The wiki says it is "becoming important players in the
  mercenary and security markets" in 2077. `[wiki]`
- The arms line sells to national and paramilitary buyers and to the street
  market; it is a product business with patents, research theft and export
  controls.
- The services line sells guards, bodyguards, escorts and kill teams; it is a
  people business with contracts, deniability and casualties. Azevedo's detail
  is the field-level example. `[game-data]`
- The two blocs compete for budget and board attention. A player who wants to
  run Kang Tao can choose the arms/R&D ladder or the security/services ladder.
  `[inferred]`

### 2.5 Secrecy vs growth (QianT)

- The slogan **"This is Kang Tao. This is intelligence."** and the QianT shell
  company show that deniability is a core operating principle. `[wiki]`
- The company steals competitor research, runs extraditions and kills employees
  who leak; it also wants to be a top-4 employer with Trauma Team Gold. `[wiki]`
  `[game-data]`
- The contradiction is manageable only while the covert wing stays invisible.
  A scandal — the Hangzhou refinery explosion that killed 50,000, or the
  *Nasty Hangover* kill team — exposes the gap. `[wiki]` `[game-data]`
- **QianT is the institutional answer:** a separate legal entity for sensitive
  operations, with its own servers and no public address. It is a bloc without
  a face. `[wiki]`

### 2.6 What could drive internal conflict in a simulation

1. **State vs market.** Shenyang's state priorities vs the North American
   Division's expansion. `[inferred]`
2. **HQ vs branch.** The Pacifica bid, the Hellman recruitment and the local
   kill teams are branch initiatives that can outrun Shenyang. `[inferred]`
3. **Arms vs services.** Product business vs contract business; different
   margins, risks and customers. `[inferred]`
4. **Secrecy vs growth.** QianT, research theft and the Hangzhou scandal vs the
   top-4-employer public brand. `[wiki]` `[inferred]`
5. **Board succession.** The 2077 CEO is unnamed; the founder is a state
   appointee; there is no visible heir. `[wiki]` `[inferred]`
6. **Employee loyalty vs disposal.** The 50-year pledge and Trauma Team Gold vs
   the kill team sent after Ginsky. `[game-data]` `[wiki]`
7. **External pressure.** Arasaka and Militech competition, 6th Street
   predation, and the City Council's Pacifica conditionality. `[wiki]`
   `[game-data]`

---

## 3. External relations matrix

### 3.1 Stance vocabulary and direction

One stance per row, read **from Kang Tao's side**, following the precedence in
`METHOD.md` §3: explicit violence first, then explicit transaction, then
quest-giver role, then adjacency, then a neutral placeholder.

| Stance | Meaning (from Kang Tao's side) |
| --- | --- |
| `war` | Open, active armed conflict over turf or existence |
| `hostile` | Actively targets or raids the other side, but not a declared turf war |
| `rival` | Turf or economic competition, with skirmishes |
| `neutral` | No attested interaction; not an ally |
| `trade` | Transactional exchange, no loyalty |
| `ally` | Coordinated support or shared operations |
| `patron` | Kang Tao protects or funds the other |
| `client` | Kang Tao depends on or works for the other |

Three direction notes:

- **The Chinese state is the real patron and has no faction code.** It funds,
  appoints and protects Kang Tao; it is not in `data/factions.json`, so it is
  prose only.
- **`trade` is used for suppliers.** Zetatech supplies airframes and Trauma
  Team supplies medical coverage; Kang Tao is the customer, but the vocabulary
  has no `supplier` field, so `trade` is the closest fit. This is a METHOD gap
  (§5).
- **The alternate timeline changes two rows.** The q104 Hellman extraction is
  removed by §7, so the **Aldecaldos** and **Rogue** rows are `neutral` for the
  mod rather than `hostile`. The evidence strings record the vanilla state and
  the reason for the change. `[inferred]`

### 3.2 The matrix

There is **no usable offline attitude matrix**. `Attitude_Record.hpp` is opaque
and `Affiliation.hpp` is identity only. Every stance below is judged from
quests, wiki and spatial adjacency, which is why each row carries a tag and why
the neutral rows are placeholders, not claims of friendship.

| Faction | Code | Stance | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| Tyger Claws | `tyger_claws` | `neutral` | No attested interaction. Kang Tao pistols are street-popular in Asia, but no Night City supply relationship to the Claws is attested; the Tyger Claws doc also reads neutral `[wiki]` `[inferred]` | `wiki+inferred` |
| Valentinos | `valentinos` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Arasaka | `arasaka` | `rival` | Smart-weapons competitors; Kang Tao "made various efforts to steal from competitors"; Kang Tao negotiated with Arasaka Relic director Anders Hellman before the heist; both towers are in Corpo Plaza. The q104 extraction is removed by §7, but the rivalry is structural `[game-data]` `[wiki]` | `game-data+wiki` |
| Militech | `militech` | `rival` | Arms-manufacturing competitors; neighbouring Corpo Plaza towers; a Kang Tao detail stands on Militech's HQ-concourse sub-territory (`ma_cct_cpz_15`, 269 m from Militech's CC); the Militech doc also reads rival `[game-data]` `[wiki]` `[inferred]` | `game-data+wiki+inferred` |
| Biotechnica | `biotechnica` | `neutral` | No attested interaction; both have Corpo Plaza buildings, but no contract or incident `[inferred]` | `inferred` |
| Petrochem | `petrochem` | `neutral` | The Kang Tao Building is next to Petrochem Tower; adjacency only, no attested interaction `[wiki]` `[inferred]` | `wiki+inferred` |
| Barghest | `barghest` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| 6th Street | `sixth_street` | `hostile` | *Nasty Hangover*: 6th Street mugged Kang Tao employee Karl Ginsky and stole a top-secret Kang Tao shard; a Kang Tao kill team arrives to recover it and silence the witnesses; the Hanford Overpass encounter is Kang Tao versus 6th Street `[game-data]` `[wiki]` | `game-data+wiki` |
| Aldecaldos | `aldecaldos` | `neutral` | The only attested interaction is the q104 AV ambush (Panam and V shoot down a Kang Tao AV), which the mod's §7 removes with the Relic plot. No other Aldecaldo-Kang Tao interaction is attested `[game-data]` `[wiki]` `[inferred]` | `game-data+wiki+inferred` |
| Wraiths | `wraiths` | `neutral` | The old Jackson Plains airstrip is Wraith territory and Kang Tao agents are tracked through it in q104 (removed); no attested combat `[game-data]` `[inferred]` | `game-data+inferred` |
| Animals | `animals` | `neutral` | Sasquatch carries a Kang Tao A-22B Chao; an equipment choice, not a relationship; the Animals doc also reads neutral `[wiki]` `[inferred]` | `wiki+inferred` |
| The Mox | `the_mox` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Maelstrom | `maelstrom` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Voodoo Boys | `voodoo_boys` | `neutral` | No specific operation attested; only generic corporate data theft `[inferred]` | `inferred` |
| NCPD | `ncpd` | `neutral` | No attested interaction. Corporate Plaza is jointly patrolled by NCPD and private corporate security, but no Kang Tao-specific arrangement is attested `[wiki]` `[inferred]` | `wiki+inferred` |
| Night Corp | `night_corp` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| City Council | `city_council` | `neutral` | 2077 Pacifica bid: Kang Tao wanted property for a new server facility; the council debated selling the lot for €$1 in exchange for a crime-clearance pledge; no deal was made. A failed negotiation, not a transaction `[wiki]` | `wiki` |
| Scavengers | `scavengers` | `neutral` | No attested interaction; Kang Tao security would treat scavs as criminals, but no specific event `[inferred]` | `inferred` |
| Regina Jones | `fixer_regina` | `neutral` | No Kang Tao-specific gig or lore link found `[inferred]` | `inferred` |
| Wakako Okada | `fixer_wakako` | `neutral` | No attested Kang Tao gig. Her netrunner Chang-Hoon Nam has a "kang tao container" computer thread, but the contract is not confirmed as hers `[game-data]` `[inferred]` | `game-data+inferred` |
| Sebastian Ibarra (Padre) | `fixer_padre` | `neutral` | No Kang Tao-specific gig or lore link found `[inferred]` | `inferred` |
| Muamar Reyes (El Capitán) | `fixer_el_capitan` | `neutral` | No Kang Tao-specific gig or lore link found `[inferred]` | `inferred` |
| Dakota Smith | `fixer_dakota` | `neutral` | No Kang Tao-specific gig or lore link found `[inferred]` | `inferred` |
| Dino Dinovic | `fixer_dino` | `neutral` | No Kang Tao-specific gig or lore link found `[inferred]` | `inferred` |
| Rogue Amendiares | `fixer_rogue` | `neutral` | In the mod's timeline her only Kang Tao link is *Nasty Hangover*, where she takes a job from Kang Tao employee Karl Ginsky to recover his stolen shard from 6th Street; she is not acting against Kang Tao. In vanilla 2077 she also sells the QianT extraction data (*Ghost Town*), but the Relic plot is removed `[game-data]` `[wiki]` `[inferred]` | `game-data+wiki+inferred` |
| Mr. Hands | `fixer_mr_hands` | `neutral` | No Kang Tao-specific gig or lore link found `[inferred]` | `inferred` |
| Afterlife | `afterlife` | `neutral` | Neutral merc marketplace; no Kang Tao-specific arrangement is attested `[inferred]` | `inferred` |
| NUSA | `nusa` | `neutral` | No attested interaction. The Chinese state is Kang Tao's patron, but no 2077 NUSA-Kang Tao incident is attested; the row is a geopolitical placeholder `[inferred]` | `inferred` |
| NetWatch | `netwatch` | `neutral` | No attested interaction. Kang Tao's QianT servers and data theft could intersect NetWatch, but nothing specific is attested `[inferred]` | `inferred` |
| Zetatech | `zetatech` | `trade` | Kang Tao's AV is a Zetatech Surveyor; Zetatech is the airframe supplier (Kang Tao leases, does not build). The q104 extraction is removed, but the airframe dependency remains `[wiki]` `[inferred]` | `wiki+inferred` |
| Trauma Team | `trauma_team` | `trade` | Kang Tao provides Trauma Team Gold to employees; Trauma Team rescued Karl Ginsky in *Nasty Hangover*; Kang Tao is the customer `[wiki]` `[game-data]` | `wiki+game-data` |

Stance counts (**31 rows**): **hostile 1, rival 2, trade 2, neutral 26,
patron 0, client 0, ally 0, war 0.**

The three that matter most for the mod:

- **`arasaka` — `rival`.** The defining relationship: smart-weapons competition,
  research theft, and the Hellman poach. This is the axis every other Kang Tao
  stance is read against. `[wiki]`
- **`militech` — `rival`.** The other arms giant, a neighbour in Corpo Plaza,
  and the owner of the concourse where Kang Tao keeps a detail. `[game-data]`
  `[wiki]`
- **`sixth_street` — `hostile`.** The only attested street-level hostility:
  6th Street steals a Kang Tao shard and Kang Tao sends a kill team. This is
  the best template for a player-founded gang that crosses Kang Tao. `[game-data]`
  `[wiki]`

### 3.3 Actors outside `data/factions.json`

Real relationships with no faction code, so prose only:

- **The Chinese government / party directorate** — the real patron. It appointed
  Xu, funded the research facilities, and its relations "kept Kang Tao out of
  trouble." There is no named ministry, party body or official, so it cannot be
  seeded as a faction. `[wiki]`
- **QianT** — the cyberware subsidiary and shell company. It handled the
  Hellman extraction traffic and sells high-end cyberware; it has no address or
  named staff. `[wiki]`
- **Tsunami Arms** — named as a peer in the top tier of weapons manufacturers
  alongside Kang Tao and Arasaka. No Night City presence. `[wiki]`
- **SovOil** — owns the Highway 101 fuel station Kang Tao uses as a fallback in
  q104. Not a Kang Tao asset; the location doc is explicit. `[wiki]`
- **The Hangzhou refinery victims** — the 2077 explosion killed over 50,000;
  official accounts cleared the company. A scandal and a legitimacy liability,
  not an actor. `[wiki]`
- **The Night City Council** — already a row; the Pacifica negotiation is the
  only attested channel. `[wiki]`
- **Serena Zhao / Glamdoc** — a Downtown clinic that uses two Kang Tao androids
  as security. A vendor, not a Kang Tao business. `[game-data]` `[wiki]`
- **Chang-Hoon Nam / Spectral Kid** — Wakako's netrunner and a reckless teenager
  with a "kang tao container" thread. Not a confirmed Kang Tao relationship.
  `[game-data]`
- **The "top brass"** — the unnamed Kang Tao leadership referenced in the
  *Nasty Hangover* journal; the kill team's principal. No record. `[wiki]`

### 3.4 Guarantor assessment

The design question: if a player founds an organisation, which factions would
guarantee Kang Tao's support, and which would Kang Tao guarantee?

- **No faction is an ally.** The matrix has no `ally` row and no `patron` or
  `client` row. The closest relationships are transactional: Zetatech
  (airframes), Trauma Team (employee coverage) and the Chinese state (patron,
  no faction code). `[inferred]`
- **Kang Tao is a poor ally and a dangerous patron.** It kills its own
  employees to contain leaks, runs extraditions through a shell company, steals
  competitor research, and is protected by a state that can absorb the
  reputational cost. A player who takes Kang Tao's support inherits Arasaka,
  Militech, 6th Street and the Chinese state's enemies. `[inferred]`
- **Plausible guarantors are branch-level and individual**, not corporate:
  - a **QianT contract** for deniable cyberware or data work;
  - a **security-services contract** (a Militech SiteSecure analogue) for a
    player-owned site;
  - a **North American Division director** who owes the player a favour;
  - the **Chinese state** through a QianT or trade channel.
  All four are transactional. None is a formal alliance. `[inferred]`
- **Kang Tao as an aggressor is the more likely configuration.** For a player
  founding an organisation on a Kang Tao-held point, Kang Tao is the
  **pre-emptive attacker or the client**: it sends kill teams (Nasty Hangover),
  runs covert extractions (q104 in vanilla), and buys proxies. Its `hostile`
  row is 6th Street, not a broad war; its `rival` rows are the arms giants.
  `[inferred]`
- **The state is the structural exception.** If a player organisation can obtain
  Chinese state sanction, Kang Tao's patron cannot move against it openly — the
  same logic as Militech and the NUSA, but with a foreign state and no faction
  code. `[inferred]`

---

## 4. Pillar notes

Design claims from `docs/design/gameplay-systems.md`: Kang Tao is a
**Corporation** (archetype strength **Technology**, weakness **Culture**);
faction strength **Espionage**, weakness **Economy**.

| Pillar | Design claim | Lore verdict | Evidence |
| --- | --- | --- | --- |
| Technology (archetype strength) | Corporations are technology-led | **Strongly supported.** Kang Tao's edge is Smart-class weaponry — gyrojet technology, caseless guided ammunition, the A-22B Chao pistol, G-58 Dian SMG, L-69 Zhuo shotgun — plus cyberware through QianT (a high-end cyberware subsidiary) and Kang Tao-branded cyberware (NeoFiber, Blood Pump, Optical Camo, RAM Recoup, Scar Coalescer, Nano-plating, plus cosmetic styles for Mantis Blades, Gorilla Arms and the Projectile Launch System) and androids. But the R&D and factories are in China, not Night City. | Wiki *Kang Tao* (products, smart-weapon specialization); wiki *QianT*; wiki *Kang Tao Mantis Blades / Gorilla Arms / Projectile Launch System* (styles); roster androids `[wiki]` `[game-data]` |
| Culture (archetype weakness) | Corporations are culturally weak | **Supported, with a twist.** Kang Tao has a real employee offer — Trauma Team Gold, a 50-year loyalty pledge, 4th-best employer — but it is coercive and transactional: kill teams, a 50,000-dead refinery negligence record, and a Taiwanese-origin/Chinese-state identity shift. The culture does not export; it buys compliance. | Wiki *Kang Tao* (Hangzhou, employer ranking); shard *Big 5 Employers*; *Nasty Hangover* kill team `[wiki]` `[game-data]` |
| Espionage (faction strength) | Kang Tao is an espionage power | **Strongly supported.** The slogan "This is Kang Tao. This is intelligence."; QianT as a shell company; "various efforts to steal from competitors"; the Hellman recruitment and QianT-routed extraction; the stolen datashard; the kill team. This is the faction's clearest strength. | Wiki *Kang Tao* (slogan, research theft); wiki *QianT*; *Nasty Hangover*; q104 `[wiki]` `[game-data]` |
| Economy (faction weakness) | Kang Tao is economically weak | **Supported, but read it as no local economic depth, not a weak balance sheet.** Kang Tao is a €$525bn, 1,000,000-employee giant — but in Night City it has one HQ building and no factory, lab, warehouse or storefront. Manufacturing and R&D are off-map; the local economy is arms sales, security contracts, cyberware licensing and intelligence. The HQ produces no manufacturing yield (location doc §4.1, §8.3). | Wiki *Kang Tao* (€$525bn, 1M employees, Shenyang); location doc §4.1; roster sites `[wiki]` `[game-data]` |
| Overall fit | The pillars fit the corp's identity | **Good.** An intelligence-and-technology arms dealer with a thin local economy is the cleanest possible "Corporation / Espionage / Economy" fit. Keep Technology and Espionage strong; keep Culture weak as external soft power; keep Economy weak as local footprint. | Synthesis `[inferred]` |

Design cautions, not redesigns:

- **Do not model Kang Tao as economically weak in absolute terms.** It is a
  €$525 billion company. Its weakness is that its Night City footprint is one
  sales/administration building and no production.
- **Do not model Culture as zero.** The 50-year pledge and Trauma Team Gold are
  real incentives, and the top-5 employer ranking is real. But the culture is
  coercive and inward-facing; it produces compliance, not loyalty.
- **Do not model Espionage as generic spying.** It is corporate intelligence,
  research theft, shell companies, extraditions and kill teams. The slogan is
  the faction's thesis.
- **The state relationship is the hidden sovereign.** Any politics layer must
  decide whether the Chinese state is an external patron or an internal bloc.
  The source material supports both readings; the document treats it as a
  patron with no faction code.

---

## 5. Gaps and uncertainties

1. **No named 2077 CEO.** The wiki gives a founder, a board member and one
   "TBA" employee; the CEO seat is blank. A simulation must invent or abstract
   it. `[wiki]`
2. **No named North American Division director or branch staff.** The Kang Tao
   Building has no interior, no named occupants and no boardroom. The branch is
   a plaza volume, not a playable office. `[wiki]` `[game-data]`
3. **Ginsky vs Greenski.** The wiki spells "Karl Ginsky", the record is
   `karl_greenski`, the entry is `ginsky`. Same person; three spellings. Do not
   seed a second NPC. `[game-data]` `[wiki]`
4. **Azevedo is an entry name, not a wiki person.** The record is a generic
   `sec_chief` slot; the name may be a local hire. Treat him as a mid-level
   security chief, not a top leader. `[game-data]` `[inferred]`
5. **The q104 Hellman extraction is removed by the mod's §7.** The places and
   the Arasaka rivalry remain; the AV ambush and the Aldecaldo/Rogue hostility
   do not. The Aldecaldos and Rogue rows are `neutral` for the mod, with the
   vanilla state recorded in the evidence. `[inferred]`
6. **The 50-year loyalty pledge is from a satirical shard.** *Big 5 Employers in
   Night City – 2077* is an in-world listicle, not a corporate sourcebook. It is
   the only employee-contract evidence; treat the number as colour, not law.
   `[wiki]`
7. **No prologue or lifepath.** The employee ladder is reconstructed from enemy
   types and one gig. There is no academy, no promotion path and no named
   training institution. `[inferred]`
8. **The Hanford Overpass name is invented.** The location doc (§8.1) shows the
   seed name has no wiki, marker or prefab identity; the encounter is the
   Skyline South Assault in Progress in the Glen. Do not treat the name as
   canon. `[game-data]` `[inferred]`
9. **The Chinese state relationship is "alleged" and "government backing."** No
   ministry, party body or official is named. The state is a patron, not a
   faction with a code. `[wiki]`
10. **QianT has no address and no named staff.** It is a shell company, not a
    place. Do not seed a QianT facility. `[wiki]`
11. **No Kang Tao retail/storefront.** The "gangs it arms" premise is not
    supported: no Night City gang is an attested Kang Tao client. Kang Tao
    pistols are street-popular in Asia, but they reach Night City through other
    vendors; the only named gang user is Sasquatch (Animals) with an A-22B
    Chao, an equipment choice. `[wiki]` `[inferred]`
12. **The Kang Tao Building has no interior.** The HQ control point is an
    outdoor plaza volume (location doc §5). Politics cannot rely on a boardroom
    scene. `[game-data]`
13. **The Downtown glamdoc androids are not a Kang Tao holding.** They are
    clinic security at Serena Zhao's glamdoc; the site is a 2.5 vendor, not a
    Kang Tao business. `[game-data]` `[wiki]`
14. **The Phantom Liberty courier-loop records are fake co-presence.**
    `sa_ep1_*_courier_loop_enemies_kangtao_*` put Kang Tao in a shared enemy
    pool with six other factions; exclude them (../METHOD.md §1.3.3).
    `[game-data]`
15. **Pacifica is a failed negotiation, not a holding.** Kang Tao wanted a
    server facility; the council debated a €$1 sale conditional on crime
    clearance; no deal. The extract has zero Kang Tao Pacifica/Dogtown rows.
    Do not seed Pacifica. `[wiki]` `[game-data]`
16. **The board/CEO succession is unknown.** The founder is a state appointee,
    the current CEO is unnamed, and the only named director is a board member.
    A simulation must choose a succession model. `[wiki]` `[inferred]`
17. **Wong Nien-jen has no page.** The 2020 CEO exists only in the *Kang Tao*
    infobox. Treat him as historical colour, not a modelled actor. `[wiki]`
    `[lore]`
18. **The "founder" field conflates the restructurer with the original firm.**
    The infobox says `founder = Shiming Xu (2050)` and `established = 1990s`;
    the body says Xu was appointed in 2046 to manage a predecessor company and
    relaunched it in 2050. Use "founder of the modern company", not "1990s
    founder". `[wiki]`
19. **The "mercenary and security markets" line is wiki prose, not a contract.**
    The security arm is attested by in-game guards and kill teams, but no named
    client, price or contract is given. `[wiki]` `[game-data]`
20. **The Rogue row is neutral in the mod, hostile in vanilla.** The difference
    is the Relic plot: *Ghost Town* (QianT data sale) is removed, *Nasty
    Hangover* remains and is not anti-Kang Tao at the faction level.
    `[game-data]` `[inferred]`
21. **The Aldecaldos row is neutral in the mod, hostile in vanilla.** Same
    reason: the q104 AV ambush is part of the Relic plot and is removed.
    `[game-data]` `[wiki]` `[inferred]`
22. **The Tyger Claws, Valentinos and Animals rows are placeholders.** No
    attested Night City gang client exists; the street market is generic. Do not
    promote these rows to `trade` without a record. `[inferred]`
23. **The `nusa` row is a geopolitical placeholder.** The Chinese state is
    Kang Tao's patron, but no 2077 NUSA-Kang Tao incident is attested. The row
    exists because the METHOD requires it, not because there is evidence.
    `[inferred]`
24. **The `netwatch` row is a placeholder.** QianT's servers and Kang Tao's
    data theft could intersect NetWatch, but nothing specific is attested.
    `[inferred]`
25. **Several rows are omitted for lack of evidence.** Kendachi, Budget Arms,
    Kiroshi, Orbital Air, News 54 and Delamain have no attested Kang Tao
    interaction and are not in the matrix, rather than being added as neutral
    padding. `[inferred]`

### 5.1 Sources consulted

Local:

- `data/sites/rosters.json` — 24 Kang Tao units, 4 sites, 10 distinct records;
  the named `karl_greenski` and `sec_chief` entries.
- `data/sites/sites.json` — sites 19, 20, 60, 382 and their
  `default_faction_id`, `initial_owner_faction_id`, `sub_territory_id`,
  `is_interior`, `source_path`.
- `data/sites/{guards,triggers,spots}.json` — the `#arr_06_guard_area_kang_tao`,
  `#arr_06_tr_kang_tao_mp`, `#arr_06_tr_kang_tao_rainforcement_spawn` and
  `#arr_06_ws_azevedo*` records.
- `data/sub_territories.json` — `gle_hanford_overpass` (42) and
  `cpz_kang_tao_sector` (78), both owned by faction 22.
- `data/control_centers.json` — `cc_gle_hanford_overpass` (active) and
  `cc_cpz_kang_tao_sector`.
- `dist/extract/areas.jsonl` — 17 Kang Tao areas, 16 dominant.
- `dist/extract/markers.jsonl` — the q104 fuel station, crash site, airstrip,
  power plant and Kang Tao Building anchors.
- `dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_1.streamingsector.json`
  — the `worldCommunityRegistryNode`: 13 Kang Tao communities, the `azevedo`
  and `ginsky` entries, the generic ranger/soldier/officer/android records, the
  q104 pilot/paramedic records, and the `sa_ep1_courier_loop_enemies_kangtao_*`
  and `dtn_glamdoc` records.
- `data/factions.json` — faction code `kang_tao`, id 22, category megacorp.
- `docs/design/gameplay-systems.md` — archetype and pillar claims; §7 alternate
  timeline.
- `docs/research/factions/kang-tao.md` — location catalogue, HQ, sub-districts.
- `docs/research/factions/METHOD.md` §1.1–§1.2 — data pitfalls.
- `docs/research/factions/politics/METHOD.md` — politics method.
- Other faction docs read for cross-incidents: `politics/arasaka.md`,
  `politics/militech.md`, `politics/sixth-street.md`,
  `politics/tyger-claws.md`, `politics/valentinos.md`,
  `politics/maelstrom.md`, `politics/barghest.md`,
  `politics/voodoo-boys.md`, `politics/animals.md`.

Wiki (MediaWiki API, `action=parse&prop=wikitext`, 2026-11-25):

- [Kang Tao](https://cyberpunk.fandom.com/wiki/Kang_Tao) ·
  [Kang Tao Building](https://cyberpunk.fandom.com/wiki/Kang_Tao_Building) ·
  [List of Kang Tao employees](https://cyberpunk.fandom.com/wiki/List_of_Kang_Tao_employees)
- [Shiming Xu](https://cyberpunk.fandom.com/wiki/Shiming_Xu) ·
  [Xiaohan Ling](https://cyberpunk.fandom.com/wiki/Xiaohan_Ling) ·
  [Yuan Huo](https://cyberpunk.fandom.com/wiki/Yuan_Huo) ·
  [QianT](https://cyberpunk.fandom.com/wiki/QianT)
- [Gig: Nasty Hangover](https://cyberpunk.fandom.com/wiki/Gig:_Nasty_Hangover) ·
  [Life During Wartime](https://cyberpunk.fandom.com/wiki/Life_During_Wartime) ·
  [Lightning Breaks](https://cyberpunk.fandom.com/wiki/Lightning_Breaks) ·
  [Ghost Town](https://cyberpunk.fandom.com/wiki/Ghost_Town)
- [Corporate Plaza (2077)](https://cyberpunk.fandom.com/wiki/Corporate_Plaza_(2077)) ·
  [Pacifica (2077)](https://cyberpunk.fandom.com/wiki/Pacifica_(2077)) ·
  [Satwave Power Plant](https://cyberpunk.fandom.com/wiki/Satwave_Power_Plant) ·
  [SovOil Fuel Station (Highway 101)](https://cyberpunk.fandom.com/wiki/SovOil_Fuel_Station_(Highway_101)) ·
  [Jackson Plains Regional Airport](https://cyberpunk.fandom.com/wiki/Jackson_Plains_Regional_Airport)
- [Soldier (Kang Tao)](https://cyberpunk.fandom.com/wiki/Soldier_(Kang_Tao)) ·
  [Heavy (Kang Tao)](https://cyberpunk.fandom.com/wiki/Heavy_(Kang_Tao)) ·
  [Rapid (Kang Tao)](https://cyberpunk.fandom.com/wiki/Rapid_(Kang_Tao)) ·
  [Sniper (Kang Tao)](https://cyberpunk.fandom.com/wiki/Sniper_(Kang_Tao)) ·
  [Robot (Kang Tao)](https://cyberpunk.fandom.com/wiki/Robot_(Kang_Tao)) ·
  [Support Unit (Kang Tao)](https://cyberpunk.fandom.com/wiki/Support_Unit_(Kang_Tao)) ·
  [Elite Rapid (Kang Tao)](https://cyberpunk.fandom.com/wiki/Elite_Rapid_(Kang_Tao))
- [Big 5 Employers in Night City – 2077](https://cyberpunk.fandom.com/wiki/Big_5_Employers_in_Night_City_%E2%80%93_2077) ·
  [Chang-Hoon Nam](https://cyberpunk.fandom.com/wiki/Chang-Hoon_Nam) ·
  [Glamdoc / Vendors](https://cyberpunk.fandom.com/wiki/Vendors)

---

## 6. Machine-readable block

```json
{
  "faction_code": "kang_tao",
  "leaders": [
    {
      "name": "Shiming Xu",
      "role": "Founder and restructurer of the modern company; former Chinese army colonel; installed 2046, relaunch 2050",
      "character_record_id": null,
      "location_name": "Shenyang, China",
      "presence_class": "off-map",
      "open_world": false,
      "source": "wiki Shiming Xu; wiki Kang Tao; The World of Cyberpunk 2077",
      "confidence": "wiki"
    },
    {
      "name": "Xiaohan Ling",
      "role": "Board member (2077); the only named 2077 director",
      "character_record_id": null,
      "location_name": "Shenyang, China / Konpeki Plaza, Night City (2077 stay)",
      "presence_class": "off-map",
      "open_world": false,
      "source": "wiki List of Kang Tao employees; wiki Xiaohan Ling; The World of Cyberpunk 2077 p.138",
      "confidence": "wiki"
    },
    {
      "name": "Yuan Huo",
      "role": "Employee (2077); role TBA",
      "character_record_id": null,
      "location_name": null,
      "presence_class": "off-map",
      "open_world": false,
      "source": "wiki List of Kang Tao employees; wiki Yuan Huo",
      "confidence": "wiki"
    },
    {
      "name": "Wong Nien-jen",
      "role": "CEO (2020, Taiwan-era company)",
      "character_record_id": null,
      "location_name": "Taipei, Taiwan (2020 HQ)",
      "presence_class": "historical",
      "open_world": false,
      "source": "wiki Kang Tao infobox",
      "confidence": "wiki+lore"
    },
    {
      "name": "Kang Tao Board of Directors",
      "role": "Collective sovereign; Xiaohan Ling is the only named 2077 member",
      "character_record_id": null,
      "location_name": "Shenyang, China",
      "presence_class": "off-map",
      "open_world": false,
      "source": "wiki Kang Tao; wiki List of Kang Tao employees",
      "confidence": "wiki"
    },
    {
      "name": "North American Division director",
      "role": "Regional head of the North American Division; unnamed in every source",
      "character_record_id": null,
      "location_name": "Kang Tao Building, Corporate Plaza, City Center",
      "presence_class": "off-map",
      "open_world": false,
      "source": "wiki Kang Tao Building (type = North American Division HQ / Regional HQ); no employee record found",
      "confidence": "wiki+inferred"
    },
    {
      "name": "Karl Ginsky",
      "role": "Corporate employee; carrier of the stolen Kang Tao datashard",
      "character_record_id": "Character.sts_std_arr_06_karl_greenski",
      "location_name": "6th Street warehouse, Arroyo (Hargreaves St.)",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "roster site 382 sts_std_arr_06 (faction_id 22, entry ginsky); raw always_loaded_1 community 15970220439262687998; wiki Gig: Nasty Hangover (spelling Ginsky vs record karl_greenski)",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "name": "Azevedo",
      "role": "Kang Tao security chief; leads the Nasty Hangover recovery/kill team",
      "character_record_id": "Character.sts_std_arr_06_sec_chief",
      "location_name": "6th Street warehouse, Arroyo",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "roster site 382 sts_std_arr_06 (faction_id 22); raw always_loaded_1 community 15970220439262687998 entry azevedo; spots #arr_06_ws_azevedo*; no wiki page",
      "confidence": "game-data+inferred"
    }
  ],
  "internal_factions": [
    {
      "name": "The Chinese state directorate / Shenyang line",
      "leader": null,
      "goals": "State priorities: defense supply, strategic technology, secrecy, government-funded R&D, protect the company's government relations",
      "members_hint": "Shenyang HQ; Xiaohan Ling; QianT; government-funded research facilities",
      "source": "wiki Kang Tao (government backing, alleged connections, government-funded research facilities); wiki Shiming Xu",
      "confidence": "wiki"
    },
    {
      "name": "The North American expansion wing",
      "leader": "Unnamed North American Division director",
      "goals": "Grow Night City market share; win security contracts; buy a Pacifica server facility; recruit foreign talent (Hellman)",
      "members_hint": "Kang Tao Building; Karl Ginsky; QianT; Pacifica bid; Hellman recruitment",
      "source": "wiki Kang Tao Building; wiki Kang Tao (Pacifica); wiki Pacifica (2077) (server facility); wiki QianT",
      "confidence": "wiki+game-data+inferred"
    },
    {
      "name": "The smart-weapons R&D / arms establishment",
      "leader": null,
      "goals": "Protect the smart-weapon moat; steal competitor research; keep the A-22B/G-58/L-69 line dominant",
      "members_hint": "Shenyang R&D and factories (off-map); Xiaohan Ling on the board; no Night City lab",
      "source": "wiki Kang Tao (products, smart-weapon specialization, research theft); wiki QianT",
      "confidence": "wiki"
    },
    {
      "name": "The security and mercenary services wing",
      "leader": "Unnamed; Azevedo is a field-level security chief",
      "goals": "Sell security, bodyguard and escort contracts; run extraditions and kill teams; expand beyond hardware",
      "members_hint": "Rangers, soldiers, rapids, heavies, snipers, androids; Hanford Overpass; Nasty Hangover; q104 escort",
      "source": "wiki Kang Tao (mercenary and security markets); roster records; wiki unit pages",
      "confidence": "game-data+wiki"
    },
    {
      "name": "QianT deniable-operations wing",
      "leader": null,
      "goals": "Handle sensitive operations Kang Tao cannot be publicly associated with; carry extraction traffic; sell high-end cyberware",
      "members_hint": "QianT subsidiary; Hellman extraction servers; no address or named staff",
      "source": "wiki QianT; wiki Kang Tao (affiliations)",
      "confidence": "wiki"
    },
    {
      "name": "The board / Shenyang old guard",
      "leader": "Kang Tao Board of Directors (Xiaohan Ling the only named member)",
      "goals": "Preserve the company and the state relationship; avoid scandal; manage the unnamed CEO succession",
      "members_hint": "Shenyang board; Xiaohan Ling; no other named 2077 directors",
      "source": "wiki List of Kang Tao employees; wiki Kang Tao",
      "confidence": "wiki"
    }
  ],
  "relations": [
    {
      "faction_code": "tyger_claws",
      "stance": "neutral",
      "evidence": "No attested interaction. Kang Tao pistols are street-popular in Asia, but no Night City supply relationship to the Claws is attested; the Tyger Claws doc also reads neutral [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "valentinos",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "arasaka",
      "stance": "rival",
      "evidence": "Smart-weapons competitors; Kang Tao made various efforts to steal from competitors; Kang Tao negotiated with Arasaka Relic director Anders Hellman before the heist; both towers are in Corpo Plaza. The q104 extraction is removed by the mod's alternate timeline, but the rivalry is structural [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "militech",
      "stance": "rival",
      "evidence": "Arms-manufacturing competitors; neighbouring Corpo Plaza towers; a Kang Tao detail stands on Militech's HQ-concourse sub-territory (ma_cct_cpz_15, 269 m from Militech's CC); the Militech doc also reads rival [game-data] [wiki] [inferred]",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "faction_code": "biotechnica",
      "stance": "neutral",
      "evidence": "No attested interaction; both have Corpo Plaza buildings, but no contract or incident [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "petrochem",
      "stance": "neutral",
      "evidence": "The Kang Tao Building is next to Petrochem Tower; adjacency only, no attested interaction [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "barghest",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "sixth_street",
      "stance": "hostile",
      "evidence": "Nasty Hangover: 6th Street mugged Kang Tao employee Karl Ginsky and stole a top-secret Kang Tao shard; a Kang Tao kill team arrives to recover it and silence the witnesses; the Hanford Overpass encounter is Kang Tao versus 6th Street [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "aldecaldos",
      "stance": "neutral",
      "evidence": "The only attested interaction is the q104 AV ambush (Panam and V shoot down a Kang Tao AV), which the mod's alternate timeline removes with the Relic plot. No other Aldecaldo-Kang Tao interaction is attested [game-data] [wiki] [inferred]",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "faction_code": "wraiths",
      "stance": "neutral",
      "evidence": "The old Jackson Plains airstrip is Wraith territory and Kang Tao agents are tracked through it in q104 (removed); no attested combat [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "animals",
      "stance": "neutral",
      "evidence": "Sasquatch carries a Kang Tao A-22B Chao; an equipment choice, not a relationship; the Animals doc also reads neutral [wiki] [inferred]",
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
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "voodoo_boys",
      "stance": "neutral",
      "evidence": "No specific operation attested; only generic corporate data theft [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "ncpd",
      "stance": "neutral",
      "evidence": "No attested interaction. Corporate Plaza is jointly patrolled by NCPD and private corporate security, but no Kang Tao-specific arrangement is attested [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "night_corp",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "city_council",
      "stance": "neutral",
      "evidence": "2077 Pacifica bid: Kang Tao wanted property for a new server facility; the council debated selling the lot for one eurodollar in exchange for a crime-clearance pledge; no deal was made. A failed negotiation, not a transaction [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "scavengers",
      "stance": "neutral",
      "evidence": "No attested interaction; Kang Tao security would treat scavs as criminals, but no specific event [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_regina",
      "stance": "neutral",
      "evidence": "No Kang Tao-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_wakako",
      "stance": "neutral",
      "evidence": "No attested Kang Tao gig. Her netrunner Chang-Hoon Nam has a kang tao container computer thread, but the contract is not confirmed as hers [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "fixer_padre",
      "stance": "neutral",
      "evidence": "No Kang Tao-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_el_capitan",
      "stance": "neutral",
      "evidence": "No Kang Tao-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_dakota",
      "stance": "neutral",
      "evidence": "No Kang Tao-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_dino",
      "stance": "neutral",
      "evidence": "No Kang Tao-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_rogue",
      "stance": "neutral",
      "evidence": "In the mod's timeline her only Kang Tao link is Nasty Hangover, where she takes a job from Kang Tao employee Karl Ginsky to recover his stolen shard from 6th Street; she is not acting against Kang Tao. In vanilla 2077 she also sells the QianT extraction data (Ghost Town), but the Relic plot is removed [game-data] [wiki] [inferred]",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "faction_code": "fixer_mr_hands",
      "stance": "neutral",
      "evidence": "No Kang Tao-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "afterlife",
      "stance": "neutral",
      "evidence": "Neutral merc marketplace; no Kang Tao-specific arrangement is attested [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "nusa",
      "stance": "neutral",
      "evidence": "No attested interaction. The Chinese state is Kang Tao's patron, but no 2077 NUSA-Kang Tao incident is attested; the row is a geopolitical placeholder [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "netwatch",
      "stance": "neutral",
      "evidence": "No attested interaction. Kang Tao's QianT servers and data theft could intersect NetWatch, but nothing specific is attested [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "zetatech",
      "stance": "trade",
      "evidence": "Kang Tao's AV is a Zetatech Surveyor; Zetatech is the airframe supplier (Kang Tao leases, does not build). The q104 extraction is removed, but the airframe dependency remains [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "trauma_team",
      "stance": "trade",
      "evidence": "Kang Tao provides Trauma Team Gold to employees; Trauma Team rescued Karl Ginsky in Nasty Hangover; Kang Tao is the customer [wiki] [game-data]",
      "confidence": "wiki+game-data"
    }
  ]
}
```
