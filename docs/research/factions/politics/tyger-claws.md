# Tyger Claws — Leadership, Internal Politics and External Relations

Status: research run, 2026-11-25. One faction, one document.
Scope: Cyberpunk 2077 2.5 + Phantom Liberty, campaign disabled. Second
document in the `politics/` research type, following the Maelstrom pilot
([`maelstrom.md`](./maelstrom.md)) and the method in
[`METHOD.md`](./METHOD.md).

The location catalog for this faction is
[`../tyger-claws.md`](../tyger-claws.md); this document does not repeat it. It
maps people and politics onto those places: Clouds, Jig-Jig Street, Ho-Oh,
Deravaja Dojo, the Chram Denya Jinja, Kabuki Market, the Charter Hill casino
and the Jig-Jig pachinko parlor.

Method note: the politics method's step 1 ("read the faction page's
*Notable Members → Leadership* section") does **not** yield a 2077 leader for
this faction. The leadership table names a 2042 oyabun and two "dependent"
secondary bosses. The real 2077 command tier had to be reconstructed from a
side job (*Pisces*), a cyberpsycho shard chain, and the raw community registry.
Those divergences are listed in §5.

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/comic/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My reasoning links a named person, record or stance to a place; reasoning stated | Weak, flagged |

Presence class, as in the pilot: `ambient` = persists in free roam;
`world-activity` = gig, scanner hustle or NCPD activity, i.e. free-roam
content but activity-gated; `story` = gated by a main/side job;
`historical` = not present in 2077.

---

## 1. Leadership and ranks

### 1.1 The 2077 chain of command: a boss tier, not a boss

The Tyger Claws in 2077 have **no named single leader**. The wiki's
`Leadership` block lists one main leader — Hayato Nakagawa, "Shinobu the
Second" — with a start date of 2042 and **no end date or 2077 successor**.
Below him it lists three secondary leaders, two of them explicitly
"dependent" on V's choices. `[wiki]` Everything else in the game names a tier
of co-equal **bosses**, each owning a revenue line, and each subordinate only
to the tier above them in general terms.

That is the single most important structural fact about this faction: it is a
**franchise of businesses under a council of bosses**, not a pyramid under one
oyabun. It is also what makes it simulation-ready — a player can take over one
revenue line without decapitating the gang.

| Name | 2077 role | Character record | Location / influence point | Presence class | Source | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| **Jun Azegami** | Tyger Claw boss; direct superior of Hiromi Sato; screens Clouds hires and doll-operation decisions | `Character.sq026_tc_leader_01` (`[inferred]`) | Hiromi's penthouse, Megabuilding H8 (`{sq026_com_hiromi}`, z 326.1) | `story` | Raw registry community `960242555655014674`, entry `tc_boss_01`, phase `start`, workspot `#sq026_ws_13_boss_01_start`; wiki *Jun Azegami*, *Pisces* | `[game-data]` `[wiki]` `[inferred]` |
| **Marcus Ichida** | Tyger Claw boss; co-superior of Hiromi Sato | `Character.sq026_tc_leader_02` (`[inferred]`) | Hiromi's penthouse, Megabuilding H8 | `story` | Same community, entry `tc_boss_02`, workspot `#sq026_ws_13_boss_02_start`; wiki *Marcus Ichida* | `[game-data]` `[wiki]` `[inferred]` |
| **Taki Kazo** | Underboss; tried to rule Japantown without Wakako Okada | no 2077 record | Shrine meetings (Chram Denya Jinja); killed "yesterday" before the Norio shard chain | `historical` | Wiki *Taki Kazo*, *Gig: A Shrine Defiled*; voice only in *Archived Conversation: Masaki Osawa and Taki Kazo* | `[wiki]` |
| **Sota Saito** | Former leader; the succession everyone in 2077 is reacting to | no 2077 record | — | `historical` | Wiki *Tyger Claws Members* ("Former leader, presumably killed by other Tyger Claws"); *Archived Conversation: Julia Lee and Norio Akuhara* | `[wiki]` |
| **Hayato Nakagawa** ("Shinobu the Second") | Oyabun from 2042; inherited the Nakagawa Foundation after the 2042 civil war | no 2077 record | Kabuki; Tyger Works Tower (2045) | `historical` | Wiki *Hayato Nakagawa*, *Tyger Claws* history | `[wiki]` `[lore]` |
| **Takeru Akagi** ("Burai") | Captain of the Kimen-Gumi, the gang's legal "police" arm; refused a push to usurp Hayato | no 2077 record | Kimen-Gumi HQ, Tyger Works Tower (2045) | `historical` | Wiki *Takeru Akagi*, *Kimen-Gumi* | `[wiki]` `[lore]` |
| **Hiromi Sato** | Manager of Clouds on the gang's behalf; the boss tier's local executive | `Character.sq026_hiromi` | Clouds, Megabuilding H8 floor 12; Hiromi's Apartment | `story` | Registry entry `hiromi`, initial phase `stand`; roster at `sq026_com_hiromi`; wiki *Hiromi Sato* | `[game-data]` `[wiki]` |
| **Maiko Maeda** | Clouds' unofficial manager; doll promoted to management; pitches herself as Hiromi's replacement | `Character.Maiko` | Clouds office; Judy's apartment (phases) | `story` | Registry entry `maiko`, initial phase `sq026_04_dh_office_desk`; wiki *Maiko Maeda* | `[game-data]` `[wiki]` |
| **Jotaro Shobo** ("the Devil of Kabuki") | High-ranking member; owner of Ho-Oh; XBD scroller with 17+ murders | `Character.sts_wat_kab_07_jotaro` | Ho-Oh, Kabuki (3rd-floor office/studio) | `story` | Registry communities `{kab_07_com_jotaro}` and `{kab_07_com_enemies}`, initial phase `0Computer`; roster at site 397; wiki *Jotaro Shobo* | `[game-data]` `[wiki]` |
| **Taki Kenmochi** | Member; runs an independent pachinko operation in a Cortes-Kennedy residential block | `Character.sts_wat_kab_107_taki_kenmochi` | Cortes-Kennedy Residential Block, Kabuki | `world-activity` | Roster at site 402 `sts_wat_kab_107`, phase `A`; wiki *Taki Kenmochi*, *Gig: Troublesome Neighbors* | `[game-data]` `[wiki]` |
| **Shinobu Imai** | Lieutenant in charge of "training" trafficking victims before sale; cages them | `Character.ma_wbr_jpn_20_outpost_miniboss` (`[inferred]`) | Willow Street market, Japantown | `world-activity` | Site 285 `ma_wbr_jpn_20` (13 TC units, one `*_outpost_miniboss`); wiki *Shinobu Imai*, *SOCA: Modern Labor Market* | `[game-data]` `[wiki]` `[inferred]` |
| **Mokomichi "Motor Boy" Yamada** | High-ranking; armed robbery and extortion racket against traffickers in Little China | `Character.ma_wat_lch_08_outpost_miniboss` (`[inferred]`) | Drake & Cartwright market, Little China | `world-activity` | Site 199 `ma_wat_lch_08` (13 TC units, one `*_outpost_miniboss`); wiki *Mokomichi Yamada*, *SOCA: Tygers by the Tail* | `[game-data]` `[wiki]` `[inferred]` |
| **Wakako Okada** | Westbrook's top fixer; a Tyger Claws member *by obligation*, not by choice; nine sons are high-ranking Claws | `Character.wakako_okada` | Pachinko Parlor, Jig-Jig Street (`-657.3, 826.7, 19.5`) | `ambient` | Registry community `10158080887420941720`, initial phase `default`, workspot `#ws_wakako_okada_default`; marker `wakako_sm_okada_default`; wiki *Wakako Okada*. **Not in `rosters.json`** | `[game-data]` `[wiki]` |

Two record-level cautions:

- **The boss mapping is an inference, but a tight one.** `Character.sq026_tc_leader_01`
  and `_02` are generic slot names with no personal name in the data. The wiki
  says exactly two Tyger Claw bosses attend the penthouse meeting in *Pisces*
  (Jun Azegami and Marcus Ichida), and the penthouse community contains exactly
  two `tc_boss_*` entries on two separate `#sq026_ws_13_boss_0N_start`
  workspots. Two bosses, two slots. Confirm in-game before seeding the names.
- **Norio Akuhara is not a Tyger Claw in the data.** The gang's most
  plot-relevant named killer is `Character.ma_cct_dtn_07_cyberpsycho` with
  `faction_id = null`, even though both the wiki and the shards make him a
  (former) member. Ex-members drop out of `rosters.json` entirely — the same
  happens to Hwangbo Dong-Gun, Julia Lee and Norio. Do not expect the roster to
  contain the gang's own casualties.

### 1.2 Succession history: business successions, punctuated by murders

The leadership line from the wiki's *Tyger Claws* history page and the
individual character pages:

| Period | Leader | How the change happened |
| --- | --- | --- |
| 2030s–2023 | **"Tyger's Claw" motorcycle club** | Founded as an **Arasaka-backed** motorcycle club; by 2020 a small combat gang claiming old Japantown. `[wiki]` `[lore]` |
| 2023 | — | Night City Holocaust. Arasaka is expelled from North America; the club is orphaned. `[wiki]` |
| 2023–2042 | **Shinobu Nakagawa** (NCCS chairman, not a gangster) | Reforms the remnants into a **guardian gang** under the Night City Co-Prosperity Sphere, with the **Kimen-Gumi** as its legal face. HQ moves to the Nakagawa Kabuki Theater. `[wiki]` |
| 2042 | **Hayato Nakagawa** ("Shinobu the Second") | Shinobu dies "under mysterious circumstances"; a **civil war over the inheritance** follows; Hayato wins with Ryoko Fujiwara's help. `[wiki]` `[lore]` |
| 2040s | Hayato, with **Burai** (Kimen-Gumi) | Old members, unhappy with no payday, **push Burai to take the gang**; he refuses and stays loyal. **Tyger Phoenix** loses a takeover bid and is demoted to running Ho-Oh. `[wiki]` `[lore]` |
| unknown–2077 | **Sota Saito** | Former leader; **"presumably killed by other Tyger Claws."** Every 2077 boss references his death as the start of the current instability. `[wiki]` |
| 2077 | **"the new boss"** (unnamed) | Norio Akuhara's shard: "Was in an op with the new boss today. His skills leave a lot to be desired compared to Sota's virtuosity." `[wiki]` |
| 2077 | **Jun Azegami, Marcus Ichida, Takehiro Chiba, Masaki Osawa** | Four named bosses, each with a revenue line or a crew. Taki Kazo is killed "yesterday" by Norio. `[wiki]` `[game-data]` |

The pattern is different from Maelstrom's. Maelstrom's successions are violent
and *external* (nuclear war, MAX-TAC, cyberpsychosis). The Tyger Claws'
successions are **murder inside the family** — inheritance war, a "presumably
killed by other Tyger Claws" former leader, a boss "zeroed" by his own
cyberpsychotic subordinate — followed by a **business reorganisation** in
which the surviving bosses simply absorb the dead man's revenue line. Loss of a
leader does not fracture the gang; it re-prices it.

That is directly usable: killing a boss should transfer a business, not start a
war. Killing a boss *and* failing to control the business should start one.

### 1.3 Rank structure, initiation and advancement

**The named tiers.** Lore names only boss, lieutenant, manager and member. The
game, however, ships a full enemy archetype ladder that reads as a rank
structure and maps cleanly onto threat tier and rarity — this is the most
concrete rank system of any faction researched so far:

| Archetype | Tier | Rarity | Combat role | Read as |
| --- | ---: | --- | --- | --- |
| **Thug** | 1 | Normal | Melee (bat, tire iron, pipe, razor) | Prospect / street muscle |
| **Racketeer** | 1 | Normal | Ranged, handguns and SMGs/ARs | Made member; runs a racket |
| **Hunter** | 2 | Weak | Melee | Junior enforcer |
| **Blitzer** | 2 | Normal | Shotgunner | Assault specialist |
| **Tyger / Tygress** | 2 | Weak | Ranged, biker or gangster build | Named-rank soldier |
| **Adept** | 2 | Rare | Fast melee | Martial-arts initiate |
| **Fang** | 2 | Rare | Heavy melee | Heavy |
| **Claw** | 2 | Rare | Heavy melee with Gorilla Arms | Senior heavy |
| **Jonin** | 2 | Rare | Netrunner | Crew netrunner |
| **Dragon** | 3 | Rare | Fast ranged | Elite shooter |
| **Kunoichi** | 3 | Elite | Fast melee (katana) | Elite assassin |
| **Ozeki** | 3 | Elite | Heavy melee (kanabo) | Elite champion |

`[wiki]` (each archetype page) `[game-data]` (every one of these appears as a
`character_record_id` in `data/sites/rosters.json` for faction 2).

Caution: the names are sumo and ninja flavour, not a chain of command. *Ozeki*
is a sumo rank, *Jonin* and *Kunoichi* are ninja terms, *Claw/Fang/Tyger* are
house branding. Do not read them as a strict ladder; read **tier (1–3) and
rarity (Weak/Normal/Rare/Elite)** as the ladder and the names as costume.

**Initiation.** Unusually for this report, there is **no described initiation
rite** — unlike Maelstrom's surgical transformation. What the sources describe
is a *dress code and a debt*:

- Luminous, microchipped tattoos of Japanese demons (ECM in disguise),
  Realskinn, katanas and tantos, and fast street bikes are the identifying
  marks. `[wiki]`
- `[Irezumi](/wiki/Irezumi)` implies many members were previously yakuza; the
  wiki states this outright about Wakako Okada. `[wiki]`
- Entry is by *connection*, not ceremony: Wakako was made a member "whether she
  liked it or not" because Hayato owed her murdered husband. `[wiki]`
  Taki Kenmochi recruits Kenji Sakura into a *scheme*, not a ritual. `[wiki]`

**Advancement is commercial.** The database entry and the boss pages agree:
Jotaro rose because "his orders are authoritatively inflexible" and he was
"never late with his cut"; the bosses "repay [that] with protection and turning
a blind eye." Hiromi Sato's failure was explicitly **managerial** — Jun: "You
know what always annoyed me about Hiromi? He had no vision." `[wiki]`
Jun's price for accepting Maiko was that she prove herself "by Tyger principles
of strength and ruthlessness and having an approved face." `[wiki]`

Practical consequence for the mod: **promotion is a function of revenue
delivered plus a public demonstration of force.** A simulation should advance
members on business income and *visible* violence, and should model
"no vision" (indecision, refusing to act without orders) as the failure state —
not disloyalty. Disloyalty is a different, faster death.

### 1.4 Named members mapped to game data

Most named Tyger Claws are **not** in `data/sites/rosters.json` and several are
not in the game at all. This table separates the three cases. Records marked
`[inferred]` are one-record deductions from the site's `baseid` and its single
boss/miniboss slot.

| Name | Role / note | Character record | Community / site | Location | Presence class | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| Jun Azegami | Boss | `Character.sq026_tc_leader_01` (`[inferred]`) | `{sq026_com_hiromi}` | Hiromi's penthouse, MB H8 | `story` | `[game-data]` `[inferred]` |
| Marcus Ichida | Boss | `Character.sq026_tc_leader_02` (`[inferred]`) | `{sq026_com_hiromi}` | Hiromi's penthouse, MB H8 | `story` | `[game-data]` `[inferred]` |
| Hiromi Sato | Clouds manager | `Character.sq026_hiromi` | `{sq026_com_hiromi}` | Clouds / Hiromi's Apartment | `story` | `[game-data]` `[wiki]` |
| Maiko Maeda | Clouds unofficial manager | `Character.Maiko` | Community `8891863926077971537` (no area row) | Clouds office → Judy's kitchen → penthouse | `story` | `[game-data]` `[wiki]` |
| Oswald "Woodman" Forrest | Clouds caretaker; **not a member** — a client/asset with gang ties | `Character.Woodman`, `Character.sq026_woodman` | Community `17681605929484532661` (no area row) | Clouds | `story` | `[game-data]` `[wiki]` |
| Jotaro Shobo | High-ranking; Ho-Oh owner | `Character.sts_wat_kab_07_jotaro` | `{kab_07_com_jotaro}`, `{kab_07_com_enemies}` | Ho-Oh 3rd floor | `story` | `[game-data]` `[wiki]` |
| Taki Kenmochi | Pachinko operator | `Character.sts_wat_kab_107_taki_kenmochi` | `{kab_107_combat_com}` | Cortes-Kennedy block | `world-activity` | `[game-data]` `[wiki]` |
| Kenji Sakura | Taki's reluctant partner | `Character.sts_wat_kab_107_kenji_sakura` | `{kab_107_combat_com}` | Cortes-Kennedy block | `world-activity` | `[game-data]` `[wiki]` |
| Wakako Okada | Fixer / member by obligation | `Character.wakako_okada` | Community `10158080887420941720` (no area row) | Pachinko Parlor, Jig-Jig | `ambient` | `[game-data]` `[wiki]` |
| Shinobu Imai | Lieutenant, trafficking | `Character.ma_wbr_jpn_20_outpost_miniboss` (`[inferred]`) | `{ma_wbr_jpn_20_com}` | Willow St. market | `world-activity` | `[game-data]` `[inferred]` |
| Mokomichi Yamada | High-ranking racketeer | `Character.ma_wat_lch_08_outpost_miniboss` (`[inferred]`) | `{ma_wat_ich_08_com}` | Drake & Cartwright | `world-activity` | `[game-data]` `[inferred]` |
| Joe Kaneshiro | Glitter-lab operator | `Character.lch_06_tyger_joe_kaneshiro` | `{lch_06_com_combat}` | Rovinj St. lab, Little China | `world-activity` | `[game-data]` `[wiki]` |
| Yusaku Ogata | Glitter-lab operator | `Character.lch_06_tyger_yusaku_ogata` | `{lch_06_com_combat}` | Rovinj St. lab | `world-activity` | `[game-data]` `[wiki]` |
| Emon Fujikura | Shrine guard (named) | `Character.jpn_03_tyger_guard_emon_fujikura` | `{jpn_03_com_enemies}` | Chram Denya Jinja | `world-activity` | `[game-data]` |
| "Owner" (Deravaja) | Unnamed dojo owner; *Bloodsport* target's keeper | `Character.sts_wat_lch_03_owner` | `{lch_03_com_enemies}` | Deravaja Dojo | `world-activity` | `[game-data]` |
| Timothee LeBeau | Deravaja instructor | no 2077 record found | — | Deravaja Dojo | `historical` | `[wiki]` |
| Hiroto Saiki | Jotaro's subordinate; hunts the informant Evan Flakes | no named record found | Kabuki Market / Pinewood St. | `world-activity` | `[wiki]` |
| Takeshi Kazou | Jotaro's subordinate; hunts the deserter Keiko | no named record found | Ganymede St. overpass, Kabuki | `world-activity` | `[wiki]` |
| Samantha Samu ("Isamu") | Solo; executes underage dealers on gang turf | no named record found | Basketball court opposite Lizzie's | `world-activity` | `[wiki]` |
| Aoki Sonoda | Racketeer; Eisenhower St. assault | no named record found | `ma_wat_nid_09` | `world-activity` | `[wiki]` |
| Frank | Member; *Crash Test* | `Character.ma_wbr_nok_01_frank` | `{ma_wbr_nok_01_com}` | North Oak | `world-activity` | `[game-data]` `[wiki]` |
| Norio Akuhara ("Akki") | **Ex-member**, cyberpsycho; kills Claws in blackouts | `Character.ma_cct_dtn_07_cyberpsycho` (**faction null**) | `{ma_cct_dtn_07}` | Corpo Plaza | `world-activity` | `[game-data]` `[wiki]` |
| Julia Lee | Member; Norio's girlfriend, "killed by other Tyger Claws" | no 2077 record | — | `historical` | `[wiki]` |
| Sota Saito; Taki Kazo; Takehiro Chiba; Masaki Osawa | Former leader; murdered underboss; two bosses | no 2077 records | — | `historical` | `[wiki]` |
| Hwangbo Dong-Gun | Ex-member on the run for theft | no 2077 record | — | `historical` | `[wiki]` |
| Hayato Nakagawa; Takeru Akagi; Ryoko Fujiwara | 2042–2045 leadership | no 2077 records | Tyger Works Tower (2045) | `historical` | `[wiki]` `[lore]` |

Two data cautions:

- **`taki` and `kenji` are both real and both generic.** `Character.sts_wat_kab_107_taki_kenmochi`
  and `..._kenji_sakura` are exact and correct. Do not substring-match
  `taki`, which also hits `Character.sts_wat_kab_107_taki_kenmochi`'s
  sibling entry names and, on the wiki side, `Takeshi Kazou` and `Taki Kazo`
  — three different people.
- **`Character.Tsutomu` and `Character.Ogawa` are not Tyger Claws.**
  `Character.Tsutomu` belongs to a `q112` Arasaka AV-garage community;
  `Character.Ogawa` to `q000`/`q101` Arasaka party scenes. They appear in the
  same registry because it is a single global registry. Nothing in
  `rosters.json` gives either faction 2.

### 1.5 What the game actually spawns (open world vs story-only)

This is the part other agents must not assume, and for this faction the
presence picture is **much thinner than the location catalog implies**.

`data/sites/rosters.json` gives Tyger Claws **306 units across 43 sites**. But
`initial_phase_name` splits them hard: **241 units are live at start, 65 are
quest-gated**, and the 43 sites are overwhelmingly *activity* sites:

| Site kind | Count | Meaning |
| --- | ---: | --- |
| `scanner_hustle` | 29 | NCPD activities — the player is hired to attack them |
| `fixer_gig` | 13 | Fixer gigs — same |
| `mini_world_story` | 1 | `mws_hey_07`, a Trauma Team ambush scene |

Only **10 places** are named lore holdings (see `../tyger-claws.md` §7). So
"43 sites" is a measure of *crime scenes*, not holdings. Do not read it as
strength.

**`ambient` — persists in free roam.**
- **Kabuki Market** (`{kab_08_com_tyger_claws}`, hash `526896125729211230`,
  `-1231, 1960, 4`): 9 Tyger Claws on phase `default`, including
  `Character.sts_wat_kab_08_tyger_claws_officer`. This is the one Tyger
  community whose units are unconditionally live. `[game-data]`
- **District-event street groups** (`de_*_com`, 8 communities, 2–5 Units each,
  all on phase `A`): Japantown `de_wbr_jpn_01/02/03/05`, Little China
  `de_wat_lch_04/05/09/11`. These are the roving groups that trigger street
  events, so they read as ambient but are event-gated in practice. Worth
  reusing as ambient Tyger presence because they are the only Tyger crowds in
  the city *outside* a business or a crime scene. `[game-data]`
- **Wakako Okada** at her pachinko parlor, phase `default`. Caveat: she has no
  roster row and no community area, so this rests on the always-on `default`
  phase plus the marker `wakako_sm_okada_default`, not on a verified spawn.
  `[game-data]`

**`world-activity` — gig, scanner hustle or NCPD activity; free-roam content but
activity-gated.**
- **Tyger Claws Casino**, Charter Hill (`{hil_07_com_enemies}`, 14–15 units all
  on phase `A`). `[game-data]`
- **Glitter lab**, Little China (`{lch_06_com_combat}`, 9–11 units,
  `Default`). `[game-data]`
- **Ho-Oh** ground/casino floors: 4 of 22 units are live (`start`/`default`);
  the other 18 are on `0combat`/`0smoke`/`0attack`/`0Computer` and belong to
  *Monster Hunt*. `[game-data]`
- The ~26 scanner-hustle sites with units on `A`/`start` (Willow St., Drake &
  Cartwright, North Oak, Corpo Plaza, the Salinas St. Animals assault…).
- Taki Kenmochi's pachinko block, phase `A`. `[game-data]`

**`story` — gated by a job; do not expect them in free roam.**
- **Jun Azegami and Marcus Ichida** exist *only* in `{sq026_com_hiromi}`
  (Hiromi's penthouse, `-701.252, 835.81, 326.112`, 7 TC of 10 entries) — the
  *Pisces* meeting. `[game-data]`
- Hiromi Sato and Maiko Maeda — their communities have no area row and no site;
  they exist only as quest workspot placements. `[game-data]`
- **Jotaro Shobo** — `0Computer`, Ho-Oh 3rd floor, *Monster Hunt*. `[game-data]`
- **Deravaja Dojo**: all 11 units on `0spawn` (*Bloodsport*). `[game-data]`
- **Chram Denya Jinja**: all 17 units on `0Guard`/`0Guarding`/`0Spawn`/`0Talk`
  (*A Shrine Defiled*). `[game-data]`
- Monokatana Workshop (`sts_wbr_jpn_02`, 9 units on `0spawn`, *We Have Your
  Wife*), the Redwood St. garage (`sts_wbr_jpn_01`, 4 on `0spawn`, *Olive
  Branch*). `[game-data]`
- Woodman — two records, `q105_interrogation_*` and
  `sq026_05a_dollhouse_ambush_start`. `[game-data]`

**`historical` — not in 2077 at all.**
Sota Saito, Taki Kazo, Takehiro Chiba, Masaki Osawa, Timothee LeBeau, Hiroto
Saiki, Takeshi Kazou, Samantha Samu, Aoki Sonoda, Julia Lee, Hwangbo Dong-Gun,
Hayato Nakagawa, Takeru Akagi, Ryoko Fujiwara. `[wiki]` `[lore]`

**Bottom line for the campaign-disabled question:** *no Tyger Claws leader
exists in the open world.* The bosses are two quest-gated generic slots in a
penthouse. The only always-on leadership-adjacent NPC is Wakako Okada — and she
is a fixer, not a boss. If the mod wants a Tyger Claws command tier in free
roam, it must supply it from simulation agents, not from the game.

Caveat: "campaign disabled" may also suppress gigs and scanner hustles. The
`world-activity` rows are the best reuse candidates but still need an in-game
spawn check. The `story` rows are the ones to replace.

### 1.6 Player-path hooks

| Person | Join under | Climb past | Ally with | Remove |
| --- | --- | --- | --- | --- |
| **Jun Azegami** | Business competence and "vision"; he despises indecision | He has no superior above the boss tier, so climbing past him means becoming a boss | Marcus Ichida (they move as a pair); Maiko, if she is useful | Killing him removes the Clouds *supervisor*, not the Clouds *manager* — the business keeps running |
| **Marcus Ichida** | Same as Jun; the two act together | Same — he is a peer, not a rung | Jun; Maiko; any appointed "face" | Killing him is symmetrical to Jun; killing *both* leaves the penthouse without a decision-maker |
| **Hiromi Sato** | Managing a revenue line competently | He is the door to the boss tier; climbing past him means replacing him, and the bosses will help you do it | Jun/Marcus (his own superiors, dangerously); *not* Maiko | Maiko's route: expose his negligence and get the bosses to kill him (canonical) |
| **Maiko Maeda** | She wants a boss's protection and a revenue line | She is the swing: manager without a gang rank | Jun/Marcus, if you can be her "approved face" | Removing her restores the previous manager; the bosses respond by retaliation, not reform |
| **Wakako Okada** | Not a ladder — she is the **gate** to Japantown | — | The single best guarantor for any player operating in Westbrook | Removing her decapitates the fixer economy and embarrasses nine high-ranking sons |
| **Jotaro Shobo** | He is a *revenue line*, not a career path | — | Ally for XBD, trafficking and protection income | Removing him is the canonical Mox favour (and the safest way to earn Mox goodwill) |
| **Taki Kenmochi** | Freelance entrepreneurship inside the gang | — | Ally for an unaffiliated gambling operation | Removing her is a Regina favour and costs the gang almost nothing |
| **Shinobu Imai / Mokomichi Yamada** | Criminal enterprise | — | — | Both are NCPD bounties; removing them is public-order work, not internal politics |

Design consequence: this faction has **four separate ladders** that do not meet
until the boss tier — the **dollhouse line** (Clouds), the **casino line**
(Ho-Oh, Charter Hill casino, pachinko), the **vice line** (Jig-Jig, trafficking)
and the **fixer line** (Wakako). A player can rise inside one line and never
touch the others, which is exactly the franchise structure the lore describes.

---

## 2. Internal political factions

### 2.1 The blocs

"Members" counts are **presence proxies** from `dist/extract/areas.jsonl` and
`data/sites/rosters.json`, not membership rolls. The two Clouds communities
(`{q105_com_dollhouse}` and `{sq026_com_hiromi}`) are the same building at
different floors; do not sum them.

| Bloc | Leader(s) | What it wants | Presence / members hint | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- |
| **The boss council** | Jun Azegami, Marcus Ichida, Takehiro Chiba, Masaki Osawa | Business over war; revenue lines protected; faces approved; problems handled internally | No community of its own. Physically instantiated only at `{sq026_com_hiromi}` (7 TC / 10 entries, penthouse z 326) | Wiki *Tyger Claws* ("top brass believed business preferable to war"); *Pisces*; *Archived Conversation: Osawa and Chiba* | `[game-data]` `[wiki]` |
| **The Clouds / dollhouse management wing** | Hiromi Sato; then Maiko Maeda | Own the dollhouse revenue and the manager's cut; autonomy from the bosses | `{q105_com_dollhouse}` (40 entries, TC-dominant); `{sq026_com_hiromi}` (7 TC) | Wiki *Hiromi Sato*, *Maiko Maeda*, *Pisces* | `[game-data]` `[wiki]` |
| **Wakako Okada's network (non-leader power centre)** | Wakako Okada; nine unnamed high-ranking sons | Keep Japantown's contract economy flowing; keep her sons off other fixers' target lists; never be anyone's subordinate | No community area and no roster row. Pachinko Parlor marker `q112_mp_wakakos_pachinko_parlor`; `wakako_sm_okada_default`; driver `Character.ow_wakako_driver` at `sts_hey_rey_09` | Wiki *Wakako Okada*; *Gig: A Shrine Defiled* (Taki Kazo's whole rebellion is against her) | `[game-data]` `[wiki]` |
| **The high-earner violence wing** | Jotaro Shobo; Shinobu Imai; Mokomichi Yamada | Money through XBD, trafficking and extortion; protection from the bosses in exchange for the cut | Ho-Oh `{kab_07_com_enemies}` 15 TC; Willow St. `{ma_wbr_jpn_20_com}` 13 TC; Drake & Cartwright `{ma_wat_ich_08_com}` 13 TC | Wiki *Jotaro Shobo* database entry ("the bosses repay him with protection and a blind eye") | `[game-data]` `[wiki]` |
| **Sota Saito's old guard / demoralised veterans** | None; Norio Akuhara, Julia Lee, Taki Kazo, Masaki Osawa and Takehiro Chiba orbit it | Their own survival; some want out of "this failing gang"; all blame the post-Sota leadership | `{ma_cct_dtn_07}` (6 TC + 1 faction-less psycho); otherwise shards only | *Archived Conversation: Julia Lee and Norio Akuhara* ("our new life away from this failing gang"); *Osawa and Chiba*; *Osawa and Kazo* | `[game-data]` `[wiki]` |
| **Tyger Phoenix (historical)** | unnamed (2040s) | Rule the gang | Ran Ho-Oh; lost a takeover bid in the succession wars | Wiki *Ho-Oh* history | `[wiki]` `[lore]` |

### 2.2 Why there is no single 2077 leader — the structural argument

The conventional reading is "the wiki is just incomplete." The evidence says
otherwise: **the gang is designed as a franchise, and the franchise structure is
the politics.**

1. Each boss owns a revenue line, not a district. Jun and Marcus supervise
   Clouds; Jotaro owns Ho-Oh; Taki Kazo wanted Japantown "without Wakako's
   influence"; Taki Kenmochi starts her *own* pachinko operation without asking.
   `[wiki]`
2. The bosses judge each other on delivery, not hierarchy. Jun's complaint about
   Hiromi is that he "had no vision" and "refus[ed] to proceed without being told
   how to." That is a critique of a *manager*, not a subordinate. `[wiki]`
3. The gang closes ranks against outsiders and resumes internal wars afterwards:
   "if a dangerous outsider stepped into Claws territory, they would instead find
   the gang as a unified front. Once the interlopers had been dealt with, the
   internal wars could resume." `[wiki]`
4. Succession is absorbed by the business, not by the structure: Sota dies, a
   "new boss" appears, Taki Kazo is killed, and the boss tier is *still* four
   named bosses with no oyabun. `[wiki]`

So the correct simulation model is **not** "who is the boss" but "which revenue
lines are held, by whom, and at what cut." A player replaces a *line holder*.

### 2.3 The Wakako problem: the gang's most important non-member

Wakako Okada is the best-documented political fact about this faction and the
one the design most needs.

- She is a Tyger Claws member **by obligation**: Hayato Nakagawa made her one
  after her husband Hiroto was killed in the 2042 inheritance war, "whether she
  liked it or not." `[wiki]`
- She has **nine sons, all high-ranking Claws**, and she keeps them "strictly in
  line to ensure that they were never the target of a gig picked up by another
  fixer." `[wiki]` That is a mother using the fixer economy as a shield for her
  family inside the gang.
- She is the **top fixer of Westbrook** and runs gigs *against* individual
  Claws: *A Shrine Defiled* (bug Taki Kazo's shrine meetings), *Tyger and
  Vulture* (rob the gang's own Charter Hill casino), *We Have Your Wife*,
  *Getting Warmer…*, *Greed Never Pays*, *Olive Branch*. `[wiki]`
- Taki Kazo's entire arc is a boss who "believed he could rule Japantown without
  the influence of Wakako Okada" — and Wakako bugged his shrine to prove him
  wrong. `[wiki]`
- She is coldly pragmatic about dead members: only "the stupid and greedy would
  fall to such an ignominious fate." `[wiki]`
- She has personal reason to hate Arasaka — she lost a grandchild to them — even
  though the gang is Arasaka's client. `[wiki]` That is a live internal fault
  line.

She is therefore a **guarantor, a gatekeeper and a potential defector** in one person.
For the mod: Wakako is the strongest single argument that the Tyger Claws'
"Politics" should not be modelled as weak (the design gives them Culture as the
weakness, which is more defensible). Their politics is *commercial*, and she is
its centre.

### 2.4 The high-earner protection racket

Jotaro Shobo's database entry is an explicit description of a political bargain
inside the gang:

> "he rules his lackeys with an iron fist and is never late with his cut for the
> bosses, who repay him with protection and turning a blind eye to his various
> 'hobbies.'" `[wiki]`

That is a **bloc in one sentence**: the bosses tolerate atrocity because it
pays. It also explains the gang's central strategic vulnerability — Jotaro's
XBD business is what brings the Mox down on Ho-Oh (*Monster Hunt*), and the
same tolerance applies to Imai's trafficking cages and Yamada's extortion
racket, both of which are NCPD bounties.

For simulation: a player who *pays well* can commit almost any atrocity and stay
protected; a player who *embarrasses the gang publicly* is removed regardless of
income. Jun's price for Maiko was not morality, it was "strength and
ruthlessness and an approved face." `[wiki]`

### 2.5 The Sota succession hangover

Every 2077 internal conversation is about the same dead man. Masaki Osawa:
"Someone zeroed Taki Kazo yesterday. First that accident with Julia, now this."
Takehiro Chiba: "It all started after our boss Sota was killed. Think they're
picking us off one by one?" `[wiki]`

The bloc is real but it is **negative**: it is not an organisation, it is a
shared suspicion that the leadership is being picked off and that the gang is
"failing." Norio, its most dangerous member, defects into cyberpsychosis and
starts killing Claws to "test" them. `[wiki]` `[game-data]`

This is the cleanest internal-conflict engine in the faction: a demoralised old
guard, a boss tier that will not explain itself, and a killer who believes the
gang has lost the ability to sense danger.

### 2.6 Historical precedents for internal conflict

- **The 2042 inheritance civil war.** Shinobu Nakagawa dies; Hayato and his
  rivals fight "a great deal of bloodshed" for the Foundation. Hayato wins, and
  the losers' friends are targeted — Wakako's husband is killed for being
  Hayato's friend. `[wiki]`
- **Tyger Phoenix's failed takeover (2040s).** A faction that bid for the gang
  during the succession wars, lost, and was demoted to running Ho-Oh. It kept
  the club for a generation. `[wiki]` `[lore]` This is the single best evidence
  that a losing internal faction **survives as a business**, which the mod
  should model.
- **Burai's refused coup.** Old members, angry that the Nakagawa Foundation
  takeover produced no payday, "pushed for him to take control of the gang.
  However, he remained loyal." `[wiki]` `[lore]` A coup that did not happen for
  personal-loyalty reasons, not structural ones.
- **The Kimen-Gumi decay.** The gang's legal "police" arm was its public face and
  its respectability. As NCCS sponsors drifted to their own security, the Claws
  became dependent on "the security contracts acquired by the Kimen-Gumi and
  what they gained from their more illicit activities." `[wiki]` By 2077 the
  Kimen-Gumi does not appear in the game data at all. Legitimacy was tried and
  lost.
- **Sota's death and the Norio purge.** A leader dies, a subordinate goes
  psychotic, and the gang's own people become the target list. `[wiki]`

### 2.7 What could drive internal conflict in a simulation

Evidence-based drivers, in rough order of plausibility:

1. **Revenue-line inheritance.** Kill a boss and the line is up for grabs. This
   is the faction's native conflict and needs no invention.
2. **Wakako vs. boss autonomy.** A boss who wants Japantown without her (Taki
   Kazo's mistake) triggers her network — nine sons inside the gang plus every
   fixer contract in Westbrook. Model her as a bloc that can *withdraw* from a
   boss rather than fight him.
3. **Public embarrassment vs. private income.** Jotaro/Imai/Yamada generate
   money and NCPD heat simultaneously. A boss who protects them loses standing;
   a boss who cuts them loses income. This is the gang's central trade.
4. **The "approved face" test.** Jun's acceptance criterion is strength,
   ruthlessness and a presentable proxy. A player who cannot produce a face is
   rejected no matter how strong — a real, quotable gate.
5. **Old guard demoralisation.** A boss tier that absorbs murders without
   explaining them breeds the Sota/Norio pattern: veterans who conclude the gang
   is failing and either leave or turn on it.
6. **The Mox.** External, but it is the pressure that forces internal decisions
   about the vice economy — Ho-Oh and Clouds are both Mox targets.
7. **Arasaka dependency.** The gang's cyberware and weapons come from Arasaka
   side jobs. A boss who loses that channel loses the gang's material edge, and
   Wakako's private hatred of Arasaka makes the channel politically contested.

---

## 3. External relations matrix

### 3.1 Stance vocabulary

Unchanged from the pilot. One stance per row; nuance goes in the evidence
string.

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

There is no usable offline attitude matrix (see the pilot's §3.2; the same
`Affiliation.hpp`/`Attitude_Record.hpp` limitation applies). Every stance is
judged from quests, wiki and — carefully — spatial data. **A new trap for this
faction: Phantom Liberty's `sa_ep1_*_courier_loop_enemies_*` communities pool
every gang into one spawn table.** They manufacture fake co-presence between the
Tyger Claws and Valentinos, Arasaka, Militech, Kang Tao, Barghest, Voodoo Boys
and Animals in Dogtown and the city centre. None of that is evidence of a
relationship, and I have excluded it from every row below.

| Faction | Code | Stance | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| The Mox | `the_mox` | `war` | Founded **because** Tyger Claws raped and murdered a Mox's predecessor's worker and then killed Lizzie Borden; riots targeted Tyger businesses; a live firefight mini-world story (`mws_wbr_05`, Hudson & Lilac) pairs them; Mox weapons are "pilfered from their fallen opponents in the ongoing conflict"; Mox netrunners hunted Jotaro and hired Regina for *Monster Hunt*; the Mox "still harbor a special hatred for the Tyger Claws" `[wiki]` `[game-data]` | `game-data+wiki` |
| Wakako Okada | `fixer_wakako` | `ally` | A Tyger Claws **member by obligation**; nine sons are high-ranking Claws; runs the Westbrook fixer economy the gang depends on; bugged Taki Kazo's shrine for the gang's benefit — *but* also contracts hits on individual Claws (A Shrine Defiled, Tyger and Vulture, We Have Your Wife, Getting Warmer…, Greed Never Pays). Structural ally, selective betrayer `[game-data]` `[wiki]` | `game-data+wiki` |
| Arasaka | `arasaka` | `patron` | The gang began as an **Arasaka-backed motorcycle club**; Arasaka upper management "outsourced them side-jobs, paying them with cybertechnology and military-grade automatic weapons"; Arasaka sleeper agents joined the gang after 2023; the corp "has strong ties with underground organizations such as the various Yakuza clans, Triads, and even the Tyger Claws" `[wiki]`. No 2077 Arasaka units stand in any Tyger site `[game-data]` | `wiki` |
| Regina Jones | `fixer_regina` | `hostile` | The single largest source of anti-Tyger work: *Monster Hunt*, *Troublesome Neighbors*, *Bloodsport*, *The Heisenberg Principle*, *Playing for Keeps*, *Many Ways to Skin a Cat*, *Catch a Tyger's Toe*, *Flight of the Cheetah*, *Woman of La Mancha*, and the Norio cyberpsycho sighting `[wiki]` `[game-data]` | `game-data+wiki` |
| NCPD | `ncpd` | `hostile` | Two Suspected Organized Crime Activities (*Tygers by the Tail*, *Modern Labor Market*), three Reported Crimes (*Protect and Serve*, *One Thing Led to Another*, *Crash Test*) and multiple Assaults in Progress are all NCPD-issued against Tyger crews `[wiki]` `[game-data]`. **But** a corrupt officer, Anna Hamill, passed a Kabuki Market informant's name to Jotaro Shobo, and the 2045 Kimen-Gumi "collaborat[ed] with the NCPD on occasions" `[wiki]` — hostile with a bought channel | `game-data+wiki` |
| Trauma Team | `trauma_team` | `hostile` | Mini-world story *Trauma Team vs. Tyger Claws* at Megabuilding H3: Tygers ambush a Trauma Team AV to take a corpo's data; site `mws_hey_07` holds 24 Tyger Claws, 6 dead Tygers and 1 Trauma Team pilot `[wiki]` `[game-data]` | `game-data+wiki` |
| 6th Street | `sixth_street` | `rival` | Norio's shard: an op that "took a couple cuts to finish off some of the **6th Streeters**"; the 6th Street doc lists Tyger Claws as a rival over Charter Hill; a shared Kendal Park community `{ma_std_rcr_05_tyger_com}` (note: the community's units are Valentinos, so the *name* is the only Tyger evidence there) `[wiki]` `[game-data]` | `game-data+wiki` |
| Scavengers | `scavengers` | `rival` | Mini-world story *Tyger Claws vs. Scavengers* (`mws_wbr_03`, Monroe & Sagan, NE of Cherry Blossom Market); *Reported Crime: Lost and Found* is a scav-vs-Tyger scrap in a Japantown alley; both work the Jig-Jig chrome trade `[wiki]` `[game-data]` | `game-data+wiki` |
| Valentinos | `valentinos` | `rival` | Mini-world story *Tyger Claws vs. Valentinos* (`mws_hey_06`, the Glen); a motorcycle chase between Tygers and Valentinos at Berkeley & Market in Wellsprings; the Valentinos doc records a Valentino street scene in south JapanTown `[wiki]` `[game-data]` | `game-data+wiki` |
| Maelstrom | `maelstrom` | `rival` | The 2045 Maelstrom push into Old Japantown "caus[ed] them to clash with the local Claws"; adjacent Northside/Kabuki turf `[wiki]` `[game-data]` | `game-data+wiki` |
| Animals | `animals` | `rival` | Jig-Jig Street lists Animals among its four gangs; an Animals assault-in-progress on Salinas St. (`ma_wbr_jpn_19`) sits inside JapanTown with a single Tyger Claw present; the Animals doc lists Tyger Claws as a rival over JapanTown/Kabuki turf `[wiki]` `[game-data]` | `game-data+wiki` |
| Militech | `militech` | `neutral` | **No attested conflict in lore.** The only co-location is Badlands scanner site `ma_bls_ina_04`: 5 Tyger Claws and 6 Militech units (drone, sniper, HMG gunner) in one hustle with a Wraith "victim" — both are targets of the same NCPD event, not of each other `[game-data]`. Militech's Watson "prologue roadblocks" are prologue staging, not a Tyger feud `[wiki]`. A tempting but unsupported `rival` | `game-data+inferred` |
| Biotechnica | `biotechnica` | `neutral` | *Olive Branch* delivers a kidnapped **Biotechnica employee** (Alex Pushkin) to the Tyger Claws as a peace offering from a blacklisted solo. Biotechnica is the victim's employer, not a party to the deal `[wiki]` `[game-data]` | `wiki+inferred` |
| Kang Tao | `kang_tao` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Petrochem | `petrochem` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Barghest | `barghest` | `neutral` | No attested interaction; the Phantom Liberty courier-loop spawn pool that couples them is excluded as evidence `[inferred]` | `inferred` |
| Aldecaldos | `aldecaldos` | `neutral` | No attested interaction. Only `mq056`/`sq024` city-race contrived crowds `[inferred]` | `inferred` |
| Wraiths | `wraiths` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Voodoo Boys | `voodoo_boys` | `neutral` | No attested interaction; Dogtown co-presence comes only from the excluded Phantom Liberty spawn pool `[inferred]` | `inferred` |
| Night Corp | `night_corp` | `neutral` | No attested interaction. The Night Corp doc notes `cc_dtn_corporation_st` is Tyger-seeded, with site `ma_cct_dtn_07` 92 m away — a seed accident, not a relationship `[game-data]` `[inferred]` | `game-data+inferred` |
| City Council | `city_council` | `neutral` | No attested interaction; political, not territorial `[inferred]` | `inferred` |
| Sebastian Ibarra (Padre) | `fixer_padre` | `neutral` | No Tyger-specific gig or lore link found `[inferred]` | `inferred` |
| Muamar Reyes (El Capitán) | `fixer_el_capitan` | `neutral` | No Tyger-specific gig or lore link found `[inferred]` | `inferred` |
| Dakota Smith | `fixer_dakota` | `neutral` | No Tyger-specific gig or lore link found (her *Sparring Partner* has no Tyger involvement) `[inferred]` | `inferred` |
| Dino Dinovic | `fixer_dino` | `neutral` | No Tyger-specific gig or lore link found `[inferred]` | `inferred` |
| Rogue Amendiares | `fixer_rogue` | `neutral` | Her *Family Heirloom* and *The Union Strikes Back* target 6th Street and veteran guards, not Tygers; the Afterlife is neutral ground `[wiki]` `[inferred]` | `wiki+inferred` |
| Mr. Hands | `fixer_mr_hands` | `neutral` | No Tyger-specific gig found; *Two Wrongs* and *Spy in the Jungle* target Animals and Scavengers `[wiki]` `[inferred]` | `wiki+inferred` |
| Afterlife | `afterlife` | `neutral` | Neutral merc marketplace. Three Tyger Claw crowd units appear in `{q005_com_afterlife_community}` — background dressing, not a relationship `[game-data]` `[inferred]` | `game-data+inferred` |

### 3.3 Actors outside `data/factions.json`

- **Wakako Okada's nine sons.** Real, named only as "nine unnamed sons," all
  high-ranking Claws. They are a bloc inside the gang, not a faction. `[wiki]`
- **Kanzaki Family** — the last true yakuza clan in Night City and the gang's
  rival in the 2040s, "at odds with the Tyger Claws." No 2077 presence. `[wiki]`
  `[lore]` Note the counter-intuitive direction: the *yakuza* are the Tyger
  Claws' enemy, not their parent.
- **Night City Co-Prosperity Sphere (NCCS)** — the Japanese-corp conglomerate
  that reformed the gang in 2023 and financed it through the Nakagawa
  Foundation. Defunct by 2077; its members (Kendachi, Kiroshi, Segotari) drifted
  to their own security. `[wiki]` `[lore]`
- **Nakagawa Foundation / Fujiwara Family** — the gang's 2040s paymaster, run by
  Ryoko Fujiwara. No 2077 role. `[wiki]` `[lore]`
- **Continental Brands** — built an Oasis in Kabuki in the 2040s and
  "harrass[ed] and attack[ed] local vendors," raising tensions with the gang.
  No 2077 presence. `[wiki]` `[lore]`
- **Kimen-Gumi** — the gang's own legal/security arm (2045), the "police" the
  gang pretended to be. Gone by 2077. `[wiki]` `[lore]`
- **Tyger Phoenix** — an internal faction, not a separate actor; see §2.6.
- **Sergei Karasinsky** — the solo who kidnaps a Biotechnica employee to buy
  himself a pardon from the Claws (*Olive Branch*). A one-off client, not a
  faction. `[wiki]`
- **Anna Hamill** — the corrupt NCPD officer who sold a Kabuki Market informant
  to Jotaro Shobo. An individual channel. `[wiki]`
- **Keisuke Kagawa, Roh Chi-Won, Vortex, Macidew Coolidge** — individual
  counterparties in single gigs; listed here only so they are not mistaken for
  factions.

### 3.4 Guarantor assessment

- **One ally, one patron, one war.** The only `ally` is Wakako Okada — and she
  is a faction *code*, not a gang. The only `patron` is Arasaka — and Arasaka's
  support is a procurement channel with a political price. The only `war` is the
  Mox, and it is a war of existence, not of turf.
- **The Tyger Claws are a strong guarantor for a player, conditionally.** They
  control the largest business portfolio in the city, the largest membership
  (≈5,500), legal fronts, and the Westbrook fixer economy. If a player can get
  onto a boss's payroll, the guarantee is real: money, laundering, premises and
  muscle. The condition is Jun's test — strength, ruthlessness and an approved
  **face**. A player with no public representative gets nothing.
- **They are a poor ally against other gangs.** No `ally` row exists with any
  gang. Their wars are the Mox (existential, unwinnable by force without
  destroying the vice economy), Maelstrom (adjacent, chronic), and four running
  skirmishes (Valentinos, 6th Street, Scavengers, Animals). A player who founds
  a gang next to them inherits all of that.
- **Arasaka is the guarantor behind the guarantor.** The gang's cyberware edge
  comes from Arasaka side jobs. Cut that channel and the Technology pillar
  collapses — which is why this row matters more to the mod than the stance
  count suggests. Wakako's private anti-Arasaka grievance is the lever.
- **Wakako is the best guarantor in the game for a Westbrook start**, better
  than the gang itself. She supplies contracts, protection and premises without
  requiring a public face. She is also the most likely to sell the player out
  the moment the player becomes a liability — canonically, she is untroubled
  when Claws die.

---

## 4. Pillar notes

Design claims from `docs/design/gameplay-systems.md`: Tyger Claws are a
**Syndicate** (archetype strength Economy, weakness Military); faction strength
**Technology**, weakness **Culture**.

| Pillar | Design claim | Lore verdict | Evidence |
| --- | --- | --- | --- |
| Economy (archetype strength) | Syndicates are economically strong | **Strongly supported.** Largest gang in the city (≈5,500), "owned more businesses in Night City than any other gang," most revenue registered as legal fronts for laundering. Six revenue lines run simultaneously: sex work, gambling, nightlife, braindance/XBD, drugs (glitter), protection, plus contract violence. `factions.json` already gives them `income_multiplier 1.15`, the highest of the gangs. | Wiki *Tyger Claws* sources of income; `../tyger-claws.md` §4; `data/factions.json` `[wiki]` `[game-data]` |
| Military (archetype weakness) | Syndicates cannot fight | **Supported.** The rank-and-file are tier-1 and tier-2 thugs; the elite (Ozeki, Kunoichi) are rare; the bosses prefer business to war; the gang loses bosses to single mercenaries and reacts with retaliation against civilians, not force projection. Their "military" answer to the Mox is killing dolls. | Archetype tiers and rarity `[wiki]` `[game-data]`; *Pisces* retaliation note; "top brass believed business was preferable to war" `[wiki]` |
| Technology (faction strength) | Tyger Claws are a technology faction | **Partial — the design overstates it.** The chrome is real and good: reflex boosters, augmented limbs, pain editors, ECM tattoos, Realskinn, Kerenzikov/Sandevistan on every boss, and dedicated netrunner ranks (Jonin, gangster3_netrunner). But it is **bought, not made** — Arasaka pays them in cybertechnology and military-grade automatics, and the gang's actual combat edge is martial arts, speed and bikes. Compare Arasaka (R&D) and Maelstrom (chrome culture). Suggest reading Technology here as **procurement and chrome adoption**, and noting it collapses if the Arasaka channel is cut. | Wiki *Tyger Claws* + *Arasaka* ties; boss cyberware from character pages; archetype records `[wiki]` `[game-data]` |
| Culture (faction weakness) | Tyger Claws cannot do culture | **Supported, but precisely.** Culture is not absent — it is **unconvertible**. They have a shrine they defile for meetings, a dojo that teaches their fighting style, luminous irezumi, bikes, and a Kabuki-theatre lineage. What fails is cultural *legitimacy*: the Kimen-Gumi's guardian-gang model decayed as sponsors left, and rank-and-file sadism "undermine[s] the gang's ideologies," so the community they claim to protect produced the Mox against them. Model it as "high internal identity, negative external legitimacy." | Wiki *Tyger Claws* philosophy, *Kimen-Gumi*, *The Mox*; *Deravaja Dojo*, *Chram Denya Jinja* pages `[wiki]` `[lore]` |
| Politics (not a design weakness here) | — | **Design gives Valentinos Politics as their weakness and Tyger Claws Culture.** That holds up: the Claws' politics is commercial and effective (Wakako, the boss council, the protection bargain). Do not import the Maelstrom "politics is broken" reading. | Boss council; Wakako; Jotaro's bargain `[game-data]` `[wiki]` |
| Overall fit | Syndicate / Economy-Military / Technology-Culture | **Good, with one correction.** Keep Economy strong and Military weak. Re-read Technology as a purchased edge with a single-supplier dependency, not an indigenous strength. Treat Culture as unconvertible rather than absent. | Synthesis above `[inferred]` |

Design cautions, not redesigns:

- **Do not model them as a weak gang.** They are the largest, richest and
  best-connected criminal organisation in Night City. The weakness is depth of
  force and legitimacy, not capability.
- **Model the Arasaka channel as a technology dependency.** Losing it should
  visibly degrade the Technology pillar. That is a legitimate, lore-grounded
  economic lever and the only one the sources support.
- **Model the Mox war as existential for the economy, not the gang.** The Claws
  cannot win it by force without destroying the vice businesses that fund them.
  That is a designed dilemma, not a bug.
- **Do not give them a single leader.** The franchise structure is the point;
  collapsing it into one boss discards the faction's best mechanic.

---

## 5. Gaps and uncertainties

1. **No 2077 oyabun exists in the sources.** The wiki's Leadership block ends
   the main-leader line at 2042 with "unknown," and the 2077 tier is four
   bosses. This is either a genuine franchise structure (my reading) or a wiki
   gap. A designer who needs one leader must invent a name; the method should
   not be read as requiring one.
2. **The Jun Azegami / Marcus Ichida record mapping is an inference.** Two
   generic slots (`sq026_tc_leader_01/02`) matched to two named bosses on two
   workspots. Strong, but not a labelled record. Verify in-game.
3. **`rosters.json` loses the top of the hierarchy entirely.** The boss tier is
   stored as `tc_leader_*`, the Clouds manager as `sq026_hiromi`, and the
   dojo owner as `sts_wat_lch_03_owner`. **The method's "exact record names only,
   never substring matching" rule actively prevents finding these**, because the
   record name carries the slot, not the person. The wiki→quest→community→slot
   join needs to be added to the method.
4. **Several named NPC communities have no `areas.jsonl` row at all.** Wakako,
   Maiko, Woodman and Hiromi's story communities return no `debug_name` and no
   position from the area join; only the penthouse (`{sq026_com_hiromi}`) does.
   Their only anchors are workspot refs (`#ws_wakako_okada_default`) and
   markers. The method's join (§2 item 6) does not cover this case.
5. **Presence class by phase prefix misclassifies this faction.** The pilot's
   rule is "`story`: `q###_*`/`sq###_*` phases." Tyger Claws' story sites use
   **numeric-prefixed** phases (`0spawn`, `0Guard`, `0combat`, `0Computer`), and
   their open-world sites use `A`/`Default`/`start`. A literal `q###` rule
   would call Deravaja, the shrine and Jotaro's office *ambient*. The rule needs
   to be "0-prefixed or quest-named phase ⇒ gated," with the caveat that even
   that is a heuristic (§2 item 5 already warns it is).
6. **"43 roster sites" is misleading for this faction.** Only 10 places are
   named holdings; 29 of the 43 sites are NCPD scanner hustles and 13 are fixer
   gigs. Most "Tyger sites" are crime scenes the player is hired to attack. The
   method's appendix table should pair roster-site counts with a site-kind
   breakdown, or the next agent will overstate the footprint. The 8 `de_*`
   district-event communities are the only ambient Tyger crowds and they appear
   in neither `sites.json` nor `rosters.json` (only in `areas.jsonl` and the raw
   registry), so a site-based method misses them entirely.
7. **Phantom Liberty's `sa_ep1_*_courier_loop_enemies_*` communities manufacture
   fake relations.** They pool Tyger Claws with Valentinos, Arasaka, Militech,
   Kang Tao, Barghest, Voodoo Boys and Animals into single spawn tables. Six of
   the seven Valentino "shared areas," all Arasaka/Militech/Kang Tao/Barghest/
   Voodoo Boys co-presence, and the Dogtown hits come from these. This is the
   biggest new data trap for the politics type and it is not in the method.
8. **Ex-members vanish from the roster.** Norio Akuhara — arguably the most
   important living Tyger Claw in the base game — is
   `Character.ma_cct_dtn_07_cyberpsycho` with `faction_id = null`. Julia Lee and
   Hwangbo Dong-Gun have no record at all. A roster-first method silently loses
   the gang's own casualties and defectors.
9. **`Category:Cyberpunk 2077 Enemies - Tyger Claws` is the richest member
   list and the method discourages it.** 32 pages, including members with no
   individual page (`Aoki Sonoda`, `Frank`, `Samantha Samu`, `Takeshi Kazou`,
   `Yuri Shaku`, `Katsumi Sasaki`-class entries). The method says category pages
   "may be empty; don't rely on them." For this faction the *enemy* category is
   better than the Members page, which lists 24 names and omits several of
   these.
10. **The required-faction list omits an attested enemy.** Trauma Team is a
    live Tyger opponent (mini-world story `mws_hey_07`: 24 Tyger Claws, 6 dead
    Tygers, 1 Trauma Team pilot, an AV they were ambushing) but the method's
    row list does not name it. I added `trauma_team` as a 28th row. The method
    should say "plus any faction with an attested relation," not just the fixed
    list.
11. **Wakako is a faction code and a gang member simultaneously.** `fixer_wakako`
    (fid 71) is structurally `ally` to `tyger_claws` (fid 2), but she runs gigs
    against individual Claws. The vocabulary has no "internal patron/asset"
    stance. Flagged; `ally` is the least-wrong fit.
12. **There is no `Character.JunAzegami`, `Character.TakehiroChiba`,
    `Character.MasakiOsawa`, `Character.SotaSaito` or `Character.TakiKazo`.**
    Four of the eight named 2077 bosses exist only as wiki prose and shards.
    Do not chase them in the registry.
13. **`Character.Tsutomu` and `Character.Ogawa` are not Tyger Claws.** Same
    global registry, different quests (Arasaka `q112` AV garage and `q000`/`q101`
    party scenes). No faction-2 roster row anywhere.
14. **Patricia-style name collisions are not the risk here; rank collisions
    are.** `Taki Kazo`, `Takeshi Kazou` and `Taki Kenmochi` are three people;
    `Kenji Sakura` and `Samantha Samu ("Isamu")` are one each. Search exact
    names, never `taki_`.
15. **Clouds is quest-locked to the point of invisibility.** All 40 entries in
    `{q105_com_dollhouse}` and the penthouse's 7 Tyger units are story content.
    With the campaign disabled, the gang's flagship venue may have **no** gang
    presence at all in free roam. This is the strongest single case for
    simulation agents replacing the game's cast.
16. **Wakako has no roster row and no site.** Her presence class rests on the
    always-on `default` phase and the `wakako_sm_okada_default` marker. It is
    almost certainly correct (she is a working fixer in 2077), but it is
    inference-backed, not roster-backed.
17. **`mws_*` and `sa_ep1_*` sites are not holdings.** `mws_hey_07` looks like
    "24 Tyger units in the Glen" but is a Trauma Team ambush crime scene with six
    dead Tygers. It is the site's `default_faction_id = 2` that makes it look
    owned. Presence is not ownership.
18. **The 2077 "new boss" has no name.** Norio's shard refers to him only as
    "the new boss," and no other source names him. He may be Jun or Marcus, or a
    fifth person. Unresolvable from the wiki; flagged.
19. **No attitude matrix, again.** Same limitation as the pilot: every stance in
    §3.2 is judged from quests, wiki and carefully filtered spatial data. The
    neutral rows are placeholders, not findings.
20. **The 2042 civil war has no roster of losers.** Tyger Phoenix is the only
    named losing faction; the rest are inferred from "a great deal of
    bloodshed." Do not invent factions for the 2040s.

### 5.1 Sources consulted

- Local: `data/factions.json`, `data/districts.json`, `data/sub_territories.json`,
  `data/control_centers.json`,
  `data/sites/{sites,rosters,phases,guards,spots,triggers,patrols,doors,suitabilities}.json`,
  `dist/extract/areas.jsonl` (including the `de_*` district-event communities,
  which have no `sites.json` or `rosters.json` row), `dist/extract/markers.jsonl`,
  `dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_{0,1,2}.streamingsector.json`
  (community registry templates, `entriesInitialState`, `communitySpawnPhase`
  names and `spotNodeRefs`).
- Wiki: [Tyger Claws](https://cyberpunk.fandom.com/wiki/Tyger_Claws),
  [Tyger Claws Members](https://cyberpunk.fandom.com/wiki/Tyger_Claws_Members),
  [Jun Azegami](https://cyberpunk.fandom.com/wiki/Jun_Azegami),
  [Marcus Ichida](https://cyberpunk.fandom.com/wiki/Marcus_Ichida),
  [Taki Kazo](https://cyberpunk.fandom.com/wiki/Taki_Kazo),
  [Hiromi Sato](https://cyberpunk.fandom.com/wiki/Hiromi_Sato),
  [Maiko Maeda](https://cyberpunk.fandom.com/wiki/Maiko_Maeda),
  [Jotaro Shobo](https://cyberpunk.fandom.com/wiki/Jotaro_Shobo),
  [Taki Kenmochi](https://cyberpunk.fandom.com/wiki/Taki_Kenmochi),
  [Shinobu Imai](https://cyberpunk.fandom.com/wiki/Shinobu_Imai),
  [Mokomichi Yamada](https://cyberpunk.fandom.com/wiki/Mokomichi_Yamada),
  [Norio Akuhara](https://cyberpunk.fandom.com/wiki/Norio_Akuhara),
  [Wakako Okada](https://cyberpunk.fandom.com/wiki/Wakako_Okada),
  [Woodman](https://cyberpunk.fandom.com/wiki/Woodman),
  [Hayato Nakagawa](https://cyberpunk.fandom.com/wiki/Hayato_Nakagawa),
  [Takeru Akagi](https://cyberpunk.fandom.com/wiki/Takeru_Akagi),
  [Ryoko Fujiwara](https://cyberpunk.fandom.com/wiki/Ryoko_Fujiwara),
  [Kimen-Gumi](https://cyberpunk.fandom.com/wiki/Kimen-Gumi),
  [Kanzaki Family](https://cyberpunk.fandom.com/wiki/Kanzaki_Family),
  [Nakagawa Foundation](https://cyberpunk.fandom.com/wiki/Nakagawa_Foundation),
  [Night City Co-Prosperity Sphere](https://cyberpunk.fandom.com/wiki/Night_City_Co-Prosperity_Sphere),
  [Pisces](https://cyberpunk.fandom.com/wiki/Pisces),
  [The Mox](https://cyberpunk.fandom.com/wiki/The_Mox),
  [Ho-Oh](https://cyberpunk.fandom.com/wiki/Ho-Oh),
  [Clouds](https://cyberpunk.fandom.com/wiki/Clouds),
  [Gig: Monster Hunt](https://cyberpunk.fandom.com/wiki/Gig:_Monster_Hunt),
  [Gig: Bloodsport](https://cyberpunk.fandom.com/wiki/Gig:_Bloodsport),
  [Gig: The Heisenberg Principle](https://cyberpunk.fandom.com/wiki/Gig:_The_Heisenberg_Principle),
  [Gig: Troublesome Neighbors](https://cyberpunk.fandom.com/wiki/Gig:_Troublesome_Neighbors),
  [Gig: A Shrine Defiled](https://cyberpunk.fandom.com/wiki/Gig:_A_Shrine_Defiled),
  [Gig: Tyger and Vulture](https://cyberpunk.fandom.com/wiki/Gig:_Tyger_and_Vulture),
  [Gig: Olive Branch](https://cyberpunk.fandom.com/wiki/Gig:_Olive_Branch),
  [Suspected Organized Crime Activity: Tygers by the Tail](https://cyberpunk.fandom.com/wiki/Suspected_Organized_Crime_Activity:_Tygers_by_the_Tail),
  [Suspected Organized Crime Activity: Modern Labor Market](https://cyberpunk.fandom.com/wiki/Suspected_Organized_Crime_Activity:_Modern_Labor_Market),
  [Cyberpsycho Sighting: Phantom of Night City](https://cyberpunk.fandom.com/wiki/Cyberpsycho_Sighting:_Phantom_of_Night_City),
  [Reported Crime: Lost and Found](https://cyberpunk.fandom.com/wiki/Reported_Crime:_Lost_and_Found),
  [Reported Crime: Crash Test](https://cyberpunk.fandom.com/wiki/Reported_Crime:_Crash_Test),
  [Cyberpunk 2077 Mini-World Stories](https://cyberpunk.fandom.com/wiki/Cyberpunk_2077_Mini-World_Stories),
  [Archived Conversation: Julia Lee and Norio Akuhara](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Julia_Lee_and_Norio_Akuhara),
  [Archived Conversation: Masaki Osawa and Takehiro Chiba](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Masaki_Osawa_and_Takehiro_Chiba),
  [Archived Conversation: Masaki Osawa and Taki Kazo](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Masaki_Osawa_and_Taki_Kazo),
  [Archived Conversation: Taki Kenmochi and Kenji Sakura](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Taki_Kenmochi_and_Kenji_Sakura),
  [Arasaka](https://cyberpunk.fandom.com/wiki/Arasaka),
  and the twelve Tyger Claws enemy archetype pages.
- Earlier repo research: `docs/research/factions/tyger-claws.md`,
  `docs/research/factions/METHOD.md`, `docs/research/factions/politics/METHOD.md`,
  `docs/research/factions/{valentinos,sixth-street,the-mox,animals,scavengers,maelstrom,night-corp,militech}.md`,
  `docs/design/gameplay-systems.md`.

---

## 6. Machine-readable block

```json
{
  "faction_code": "tyger_claws",
  "leaders": [
    {
      "name": "Jun Azegami",
      "role": "Tyger Claw boss; superior of Hiromi Sato",
      "character_record_id": "Character.sq026_tc_leader_01",
      "location_name": "Hiromi's penthouse, Megabuilding H8",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_1 community 960242555655014674, entry tc_boss_01, phase start, workspot #sq026_ws_13_boss_01_start; area {sq026_com_hiromi} at -701.252,835.81,326.112; record name is a generic slot, personal-name mapping inferred; wiki Jun Azegami and Pisces",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "name": "Marcus Ichida",
      "role": "Tyger Claw boss; co-superior of Hiromi Sato",
      "character_record_id": "Character.sq026_tc_leader_02",
      "location_name": "Hiromi's penthouse, Megabuilding H8",
      "presence_class": "story",
      "open_world": false,
      "source": "same community, entry tc_boss_02, phase start, workspot #sq026_ws_13_boss_02_start; personal-name mapping inferred; wiki Marcus Ichida",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "name": "Taki Kazo",
      "role": "Underboss; tried to rule Japantown without Wakako Okada (deceased 2077)",
      "character_record_id": null,
      "location_name": "Chram Denya Jinja shrine",
      "presence_class": "historical",
      "open_world": false,
      "source": "wiki Taki Kazo and Gig: A Shrine Defiled; mentioned in Archived Conversation: Masaki Osawa and Taki Kazo; no 2077 character record",
      "confidence": "wiki"
    },
    {
      "name": "Sota Saito",
      "role": "Former leader; his death starts the 2077 succession crisis",
      "character_record_id": null,
      "location_name": null,
      "presence_class": "historical",
      "open_world": false,
      "source": "wiki Tyger Claws Members (former leader, presumably killed by other Tyger Claws); Archived Conversation: Julia Lee and Norio Akuhara",
      "confidence": "wiki"
    },
    {
      "name": "Hayato Nakagawa (Shinobu the Second)",
      "role": "Oyabun from 2042; won the 2042 inheritance civil war",
      "character_record_id": null,
      "location_name": "Kabuki / Tyger Works Tower",
      "presence_class": "historical",
      "open_world": false,
      "source": "wiki Hayato Nakagawa, Tyger Claws history, Nakagawa Foundation; Cyberpunk RED lore",
      "confidence": "wiki+lore"
    },
    {
      "name": "Takeru Akagi (Burai)",
      "role": "Captain of the Kimen-Gumi; refused a coup against Hayato",
      "character_record_id": null,
      "location_name": "Kimen-Gumi HQ, Tyger Works Tower",
      "presence_class": "historical",
      "open_world": false,
      "source": "wiki Takeru Akagi and Kimen-Gumi; Cyberpunk RED lore",
      "confidence": "wiki+lore"
    },
    {
      "name": "Hiromi Sato",
      "role": "Manager of Clouds on the gang's behalf",
      "character_record_id": "Character.sq026_hiromi",
      "location_name": "Clouds, Megabuilding H8 floor 12 / Hiromi's Apartment",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_1 entry hiromi, initial phase stand; roster at community 960242555655014674; wiki Hiromi Sato",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Maiko Maeda",
      "role": "Clouds unofficial manager; pitches herself as Hiromi's replacement",
      "character_record_id": "Character.Maiko",
      "location_name": "Clouds office / Judy's apartment",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_1 community 8891863926077971537, entry maiko, initial phase sq026_04_dh_office_desk; no areas.jsonl row; wiki Maiko Maeda",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Jotaro Shobo",
      "role": "High-ranking member; owner of Ho-Oh; XBD scroller",
      "character_record_id": "Character.sts_wat_kab_07_jotaro",
      "location_name": "Ho-Oh, Kabuki (3rd floor)",
      "presence_class": "story",
      "open_world": false,
      "source": "raw communities {kab_07_com_jotaro} and {kab_07_com_enemies}, initial phase 0Computer; roster at site 397 sts_wat_kab_07; wiki Jotaro Shobo",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Taki Kenmochi",
      "role": "Member; runs an independent pachinko operation",
      "character_record_id": "Character.sts_wat_kab_107_taki_kenmochi",
      "location_name": "Cortes-Kennedy Residential Block, Kabuki",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "roster at site 402 sts_wat_kab_107, phase A; community {kab_107_combat_com}; wiki Taki Kenmochi and Gig: Troublesome Neighbors",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Shinobu Imai",
      "role": "Lieutenant in charge of trafficking victims",
      "character_record_id": "Character.ma_wbr_jpn_20_outpost_miniboss",
      "location_name": "Willow Street market, Japantown",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "site 285 ma_wbr_jpn_20, 13 Tyger units with a single *outpost_miniboss* slot (mapping inferred); wiki Shinobu Imai and SOCA: Modern Labor Market",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "name": "Mokomichi Yamada",
      "role": "High-ranking racketeer in Little China",
      "character_record_id": "Character.ma_wat_lch_08_outpost_miniboss",
      "location_name": "Drake & Cartwright market, Little China",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "site 199 ma_wat_lch_08, 13 Tyger units with a single *outpost_miniboss* slot (mapping inferred); wiki Mokomichi Yamada and SOCA: Tygers by the Tail",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "name": "Wakako Okada",
      "role": "Westbrook fixer; Tyger Claws member by obligation; nine sons are high-ranking Claws",
      "character_record_id": "Character.wakako_okada",
      "location_name": "Pachinko Parlor, Jig-Jig Street, Japantown",
      "presence_class": "ambient",
      "open_world": true,
      "source": "raw always_loaded_1 community 10158080887420941720, entry wakako, initial phase default, workspot #ws_wakako_okada_default; marker wakako_sm_okada_default at -671.492,822.324,19.598; not in rosters.json; wiki Wakako Okada",
      "confidence": "game-data+wiki"
    }
  ],
  "internal_factions": [
    {
      "name": "The boss council",
      "leader": "Jun Azegami",
      "goals": "Business over war; protect and grow revenue lines; approve faces; handle disputes internally",
      "members_hint": "Jun Azegami, Marcus Ichida, Takehiro Chiba, Masaki Osawa; only physical instantiation is the Pisces penthouse community {sq026_com_hiromi} with 7 Tyger units of 10 entries",
      "source": "wiki Tyger Claws philosophy; wiki Pisces; Archived Conversation: Masaki Osawa and Takehiro Chiba; raw community 960242555655014674",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The Clouds / dollhouse management wing",
      "leader": "Hiromi Sato",
      "goals": "Own the dollhouse revenue and the manager's cut; autonomy from the boss tier",
      "members_hint": "q105_com_dollhouse 40 entries, TC-dominant; {sq026_com_hiromi} 7 TC units at z 326; Maiko Maeda as successor candidate",
      "source": "wiki Hiromi Sato, Maiko Maeda, Pisces; raw communities {q105_com_dollhouse} and {sq026_com_hiromi}",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Wakako Okada's network",
      "leader": "Wakako Okada",
      "goals": "Keep the Westbrook contract economy flowing; shield her nine sons from fixer contracts; remain nobody's subordinate",
      "members_hint": "Nine unnamed high-ranking sons; driver Character.ow_wakako_driver at sts_hey_rey_09; no community area and no roster row of her own",
      "source": "wiki Wakako Okada; wiki Gig: A Shrine Defiled; roster entry ow_wakako_driver",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The high-earner violence wing",
      "leader": "Jotaro Shobo",
      "goals": "Money through XBD, trafficking and extortion; buy protection from the boss tier with a reliable cut",
      "members_hint": "Ho-Oh {kab_07_com_enemies} 15 TC; Willow St. {ma_wbr_jpn_20_com} 13 TC (Shinobu Imai); Drake & Cartwright {ma_wat_ich_08_com} 13 TC (Mokomichi Yamada)",
      "source": "wiki Jotaro Shobo database entry; wiki Shinobu Imai and Mokomichi Yamada; raw community areas",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Sota Saito's old guard",
      "leader": null,
      "goals": "Survival; some want out of 'this failing gang'; all blame the post-Sota leadership",
      "members_hint": "{ma_cct_dtn_07} 6 TC units plus 1 faction-less cyberpsycho (Norio); otherwise shards only",
      "source": "Archived Conversation: Julia Lee and Norio Akuhara; Archived Conversation: Masaki Osawa and Takehiro Chiba; Archived Conversation: Masaki Osawa and Taki Kazo; wiki Norio Akuhara",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Tyger Phoenix (historical)",
      "leader": null,
      "goals": "Rule the gang; ran Ho-Oh after losing the succession-wars takeover bid",
      "members_hint": "No 2077 records; Ho-Oh's 2040s management",
      "source": "wiki Ho-Oh history; Cyberpunk RED lore",
      "confidence": "wiki+lore"
    }
  ],
  "relations": [
    {
      "faction_code": "the_mox",
      "stance": "war",
      "evidence": "Mox founded after Tyger Claws raped and murdered one of Lizzie Borden's workers and then killed Lizzie; riots targeted Tyger businesses; live firefight mini-world story mws_wbr_05 at Hudson & Lilac; Mox weapons pilfered from fallen Tygers in the ongoing conflict; Mox netrunners hunted Jotaro and hired Regina for Monster Hunt; Mox still harbor a special hatred for the Tyger Claws",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_wakako",
      "stance": "ally",
      "evidence": "Tyger Claws member by obligation since 2042; nine sons are high-ranking Claws; runs the Westbrook fixer economy the gang depends on; bugged Taki Kazo's shrine for the gang; but also contracts hits on individual Claws in A Shrine Defiled, Tyger and Vulture, We Have Your Wife, Getting Warmer, Greed Never Pays and Olive Branch",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "arasaka",
      "stance": "patron",
      "evidence": "Gang began as an Arasaka-backed motorcycle club; Arasaka upper management outsourced them side jobs paying in cybertechnology and military-grade automatics; Arasaka sleeper agents joined the gang after 2023; Arasaka has strong ties with the Tyger Claws. No 2077 Arasaka units stand in any Tyger site in the extract",
      "confidence": "wiki"
    },
    {
      "faction_code": "fixer_regina",
      "stance": "hostile",
      "evidence": "Largest source of anti-Tyger work: Monster Hunt, Troublesome Neighbors, Bloodsport, The Heisenberg Principle, Playing for Keeps, Many Ways to Skin a Cat, Catch a Tyger's Toe, Flight of the Cheetah, Woman of La Mancha, and the Norio cyberpsycho sighting",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "ncpd",
      "stance": "hostile",
      "evidence": "Two Suspected Organized Crime Activities (Tygers by the Tail, Modern Labor Market), three Reported Crimes (Protect and Serve, One Thing Led to Another, Crash Test) and multiple Assaults in Progress are NCPD-issued against Tyger crews. However officer Anna Hamill sold a Kabuki Market informant to Jotaro, and the 2045 Kimen-Gumi collaborated with the NCPD: hostile with a bought channel",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "trauma_team",
      "stance": "hostile",
      "evidence": "Mini-world story Trauma Team vs. Tyger Claws at Megabuilding H3: Tygers ambush a Trauma Team AV for a corpo's data; site mws_hey_07 holds 24 Tyger Claws, 6 dead Tygers and 1 Trauma Team pilot",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "sixth_street",
      "stance": "rival",
      "evidence": "Norio's shard describes an op that took a couple cuts to finish off some 6th Streeters; 6th Street doc records Charter Hill contest; shared Kendal Park community {ma_std_rcr_05_tyger_com} although its units are Valentinos",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "scavengers",
      "stance": "rival",
      "evidence": "Mini-world story Tyger Claws vs. Scavengers at Monroe & Sagan near Cherry Blossom Market; Reported Crime: Lost and Found is a scav-vs-Tyger scrap in a Japantown alley; both work the Jig-Jig chrome trade",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "valentinos",
      "stance": "rival",
      "evidence": "Mini-world story Tyger Claws vs. Valentinos in the Glen (mws_hey_06); motorcycle chase between Tygers and Valentinos at Berkeley & Market in Wellsprings; Valentinos doc records a Valentino street scene in south JapanTown",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "maelstrom",
      "stance": "rival",
      "evidence": "2045 Maelstrom expansion into Old Japantown clashed with the local Claws; adjacent Northside and Kabuki turf; coupled in generic Phantom Liberty combat spawns in Kabuki and Northside",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "animals",
      "stance": "rival",
      "evidence": "Jig-Jig Street lists Animals among its four gangs; an Animals assault-in-progress on Salinas St. (ma_wbr_jpn_19) sits inside JapanTown with one Tyger Claw present; Animals doc lists Tyger Claws as a JapanTown/Kabuki rival",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "militech",
      "stance": "neutral",
      "evidence": "No attested conflict in lore. Only co-location is Badlands scanner site ma_bls_ina_04 with 5 Tyger Claws and 6 Militech units plus a Wraith victim, all targets of one NCPD event rather than of each other. Militech Watson prologue roadblocks are staging, not a feud",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "biotechnica",
      "stance": "neutral",
      "evidence": "Gig: Olive Branch delivers a kidnapped Biotechnica employee (Alex Pushkin) to the Tyger Claws as a peace offering from a blacklisted solo; Biotechnica is the victim's employer, not a party to the deal",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "kang_tao",
      "stance": "neutral",
      "evidence": "No attested interaction; only Phantom Liberty shared combat spawns [inferred]",
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
      "evidence": "No attested interaction; the Phantom Liberty courier-loop spawn pool that couples them is excluded as evidence [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "aldecaldos",
      "stance": "neutral",
      "evidence": "No attested interaction; only mq056/sq024 city-race contrived crowds [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "wraiths",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "voodoo_boys",
      "stance": "neutral",
      "evidence": "No attested interaction; Dogtown shared spawns only [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "night_corp",
      "stance": "neutral",
      "evidence": "No attested interaction; cc_dtn_corporation_st is Tyger-seeded with site ma_cct_dtn_07 92 m away, a seed accident [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "city_council",
      "stance": "neutral",
      "evidence": "No attested interaction; political, not territorial [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_padre",
      "stance": "neutral",
      "evidence": "No Tyger-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_el_capitan",
      "stance": "neutral",
      "evidence": "No Tyger-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_dakota",
      "stance": "neutral",
      "evidence": "No Tyger-specific gig or lore link found; her Sparring Partner has no Tyger involvement [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_dino",
      "stance": "neutral",
      "evidence": "No Tyger-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_rogue",
      "stance": "neutral",
      "evidence": "Family Heirloom and The Union Strikes Back target 6th Street and veteran guards; the Afterlife is neutral ground [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "fixer_mr_hands",
      "stance": "neutral",
      "evidence": "No Tyger-specific gig found; Two Wrongs and Spy in the Jungle target Animals and Scavengers [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "afterlife",
      "stance": "neutral",
      "evidence": "Neutral merc marketplace; three Tyger Claw crowd units in {q005_com_afterlife_community} are background dressing [inferred]",
      "confidence": "game-data+inferred"
    }
  ]
}
```
