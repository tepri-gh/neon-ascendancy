# Valentinos — Leadership, Internal Politics and External Relations

Status: research run, 2026-11-25. One faction, one document.
Scope: Cyberpunk 2077 2.5 + Phantom Liberty, campaign disabled. Who a player can
join under, climb past, ally with or remove; the internal blocs; and the external
relations matrix needed for wars, alliances and "guarantor" support when a player
founds a gang.

Method: this document follows
[`METHOD.md`](./METHOD.md) and the evidence rules of
[`../METHOD.md`](../METHOD.md). The location catalog for the Valentinos is
[`../valentinos.md`](../valentinos.md); this document maps people and politics
onto those places and does not repeat the coordinates.

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/comic/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My reasoning links a named person, place or stance to a record; reasoning stated | Weak, flagged |

**Presence class**, an extra convention for this document only. `ambient` =
persists in free roam without a quest; `world-activity` = gig, scanner hustle,
assault-in-progress or minor job, i.e. free-roam content but still
activity-gated; `story` = main/side job gated; `off-map` = named and alive in
2077 but never spawned (prison, out of town, elsewhere); `historical` = not
present in 2077. The JSON `open_world` flag is `true` for `ambient` +
`world-activity`, `false` for `story` + `off-map` + `historical`.

The Valentinos needed a fifth class: their top leader is not in a cell you can
walk to. He is in a prison that does not exist as a playable space.

---

## 1. Leadership and ranks

### 1.1 The 2077 chain of command

The Valentinos are a **federated barrio gang**: a titular boss, a family seat,
and a set of place-crews that run their own turf. For 2077 the sources give a
boss who is not present, an interim leader, one secondary leader who dies off
camera, and three high-ranking crew chiefs who actually hold the map.

| Name | 2077 role | Character record | Location / influence point | Presence class | Source | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| **Campo Orta** | Boss (in prison, four years left) | none | Prison, off-map | `off-map` | Wiki *Valentinos* Leadership; wiki *Campo Orta*; *Heroes* dialogue | `[wiki]` |
| **Gustavo Orta** | Interim leader on the street; Campo's relative | `Character.sts_hey_rey_01_gustavo`; also `Character.sq018_rey_01_gustavo` | Gustavo Orta's Apartment, Vista del Rey | `world-activity` | Raw `always_loaded_1` registry entry `gustavo` (phases `A_spawn`/`B`/`C`); site 369 `sts_hey_rey_01`; wiki *Nolan Frakes* ("the Valentinos' interim leader"); wiki *Gustavo Orta* | `[game-data]` `[wiki]` |
| **El Sombrerón** | Secondary leader (dies in 2077, comic) | none | Badlands, off-map | `historical` | Wiki *Valentinos* Leadership; wiki *El Sombrerón*; *Cyberpunk 2077: You Have My Word* | `[wiki]` `[lore]` |
| **Zoe Alonzo** | High-ranking member; Glen network chief | `Character.ma_hey_gle_02_outpost_miniboss` (inferred) | Valentino Alley, the Glen | `world-activity` | Site 42 `ma_hey_gle_02` (11 units, `default` phase); *Suspected Organized Crime Activity: Chapel*; shard *Got a problem*; wiki *Zoe Alonzo* | `[inferred]` `[wiki]` |
| **Rogelio Cruz** | High-ranking member; Zoe's field commander | `Character.ma_hey_gle_02_valentinos_grunt2_ranged2_ajax_ma_Rogelio_Cruz` | Valentino Alley, the Glen | `world-activity` | Raw registry entry `ganger_04` (phase `default`, spot `#ma_hey_gle_02_ws_ganger_04_a`); roster site 42; wiki *Rogelio Cruz* | `[game-data]` `[wiki]` |
| **Miguel "Gizmo" Rodriguez** | High-ranking member; Mercado Sonora smuggling chief | `Character.ma_hey_rey_06_outpost_miniboss` (inferred) | Mercado Sonora, Vista del Rey | `world-activity` | Site 66 `ma_hey_rey_06` (12 units); *Suspected Organized Crime Activity (Vista del Rey)*; wiki *Miguel Rodriguez* | `[inferred]` `[wiki]` |
| **Dario Sanchez** | High-ranking member (imprisoned, then killed by his lieutenant) | none | Downtown, off-map | `historical` | Wiki *Valentinos Members*; shards *Dario Sanchez and Claudio Moreno*, *Claudio Moreno and Aaron McCarlson* | `[wiki]` |
| **Claudio Moreno** | Crew chief, Downtown; Dario's lieutenant | `Character.ma_cct_dtn_02_claudio_moreno` | Corporation St, Downtown | `world-activity` | Raw registry entry `enemy01` (phases `start`); site 24 `ma_cct_dtn_02` (5 units); wiki *Claudio Moreno* | `[game-data]` `[wiki]` |

Two facts do the political work here:

1. **The seat is vacant, not contested.** Campo is the boss and is simply
   absent, serving a sentence with four years left in 2077. `[wiki]` No coup,
   no exile, no death: the gang is running on an interim arrangement.
2. **The interim leader is the boss's relative.** Gustavo is Campo's kinsman
   and "the Valentinos' interim leader" per the 6th Street side's own page, and
   the Members page calls him a "high-ranking member" who climbed through
   "ruthlessness and familial ties." `[wiki]` Legitimacy is dynastic, not
   electoral.

### 1.2 Succession history: a cartel that became a family firm

There is **no recorded violent succession at the top**. The recorded changes are
external and institutional: a cartel invested in a politician, the gang was born
out of that, and a boss went to prison. That is the opposite of Maelstrom's
coup-and-purge pattern, and it matters for the simulation.

| Period | Leader / centre of power | How the change happened |
| --- | --- | --- |
| 2030s–2040s | **El Norte Cartel**, boss Rubén Meza | Predecessor organisation. Enforcers El Sombrerón and La Llorona ("El Norte's Butchers") terrorised the city. `[wiki]` |
| 2044 | **Theresa Valentino**, Santo Domingo city manager | El Norte financed her campaign and beat the Aldecaldo-backed candidate; the cartel's members became known as "Valentino's Fists." `[wiki]` |
| late 2040s–2060s | The Valentinos as a small Latino cartel | La Llorona faked her death (2047) and left; El Sombrerón stayed and rose. A bloodbath at **Moto Cielo** killed many Valentinos; the priest Sebastian Ibarra survived it and left to become the fixer **Padre**. `[wiki]` |
| 2060s–2077 | **Campo Orta**, boss | Led the gang through its growth into one of Night City's largest gangs (~6,000 members). Convicted and imprisoned; four years left by 2077. `[wiki]` |
| 2077 | **Gustavo Orta**, interim leader | Runs the street while Campo is inside. El Sombrerón is listed as a secondary leader until his death in the Badlands. `[wiki]` |

The pattern: **succession is dynastic and absent-by-default.** The gang has never
had to answer "who replaces the boss?" in 2077, because the boss is still alive
and still formally in charge. A simulation that removes Campo or Gustavo forces
the gang to invent an answer it has no precedent for — which is exactly the
design opportunity.

Historical secondary figures worth knowing: **La Llorona** (El Sombrerón's
younger sister, ex-El Norte enforcer, faked her death in 2047, married the
Militech corporate Aarno, lives in the Badlands as "Teresa") and **Theresa
Valentino** (the 2040s Santo Domingo city manager whose campaign El Norte
financed; the cartel's members became known as "Valentino's Fists").
`[wiki]` `[lore]`

### 1.3 Rank structure, initiation and advancement

Lore names only four roles: **boss**, **secondary leader**, **high-ranking
member**, and **member**. `[wiki]` Everything below that is either a place-crew
or a combat tier.

1. **Boss (jefe).** One leader, currently Campo Orta, in prison. `[wiki]`
2. **Interim / secondary leaders.** Gustavo (interim, Campo's relative) and
   El Sombrerón (secondary, dead in 2077). They are not a council; they are
   two claims on the same seat. `[wiki]`
3. **High-ranking members.** Zoe Alonzo, Rogelio Cruz, Miguel Rodriguez, Dario
   Sanchez (deceased), Gustavo before he became interim. In practice these are
   **place-crew chiefs**: Zoe and Rogelio own the Glen, Miguel owns Mercado
   Sonora, Claudio inherited the Downtown crew. `[wiki]` `[game-data]`
4. **Members.** Tied to a site: José Luis (Rogelio's crew), César Diego Ruiz
   (the Glen's boxing champion), Alma Maria (arms courier), Ernesto Muñoz
   (bouncer at El Pinche Pollo), Lena Dominguez (Dicky Twister), Pablo (auto
   shop), Xavi Velez and Danilo Ruiz (named outpost bosses). `[wiki]`
   `[game-data]`
5. **Associates and non-members.** Padre (ex-member, fixer), Karubo Bairei
   (bar owner, friendly, refuses war work), Saulo Capon (Ladrillo's
   lieutenant). `[wiki]`

**Initiation and advancement.** The gang is culturally exclusive but ethnically
open: "you don't have to be Mexican to join… all have adopted the gang's culture
and assimilated." `[wiki]` There is no described ceremony and no chrome
requirement (contrast Maelstrom). What the sources do describe is a **social
contract**:

- The barrio's loyalty is the gang's shield: it made "NCPD and corporate
  infiltrations into the gang almost impossible." `[wiki]`
- In return the gang "protected the whole neighborhood." `[wiki]`
- **Betrayal is the cardinal sin**, "usually punished with a particularly
  gruesome death." `[wiki]`
- **Death in a gang fight makes a martyr**: murals, songs, and the dead treated
  as saints. `[wiki]`

Advancement is therefore reputational plus familial, and it is **place-based**:
you hold a racket, then a site, then a crew. Gustavo rose on ruthlessness and
blood; Zoe runs a network on fear and cover-ups; Miguel runs a market on volume.

**Combat tiers, not ranks.** The game's Valentino enemy list is a Spanish tier
ladder — `Thug`/`Gangoon` (tier 1), `Sanguinario`/`Seasoned Thug`/`Guerrero`/
`Macho`/`Matón` (tier 2), `Francotirador`/`Sicario`/`Toro` (tier 3 elite) — and
the records add `_officer` and `_miniboss` suffixes. `[wiki]` `[game-data]`
These describe combat role, not authority. Do not read "Sicario" as a rank.

### 1.4 Named members mapped to game data

Unlike Maelstrom, **a substantial part of the named cast is in
`data/sites/rosters.json`**. The roster join works by taking the capitalised
personal-name suffix of a `character_record_id` (`..._Rogelio_Cruz`,
`..._jose`, `..._gustavo`). Exact names only; `jose` is a substring trap for
`josephine`-style records and `karubo` is unique.

| Name | Role / note | Character record | Community / site | Location | Presence class | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| Campo Orta | Boss (incarcerated) | none | — | Prison, off-map | `off-map` | `[wiki]` |
| Gustavo Orta | Interim leader | `Character.sts_hey_rey_01_gustavo` | `{rey_01_apartment_com}` (6), `{rey_01_gustavo_com}` (1); site 369 | Gustavo Orta's Apartment | `world-activity` | `[game-data]` `[wiki]` |
| El Sombrerón | Secondary leader (d. 2077) | none | — | Badlands (comic) | `historical` | `[wiki]` `[lore]` |
| Zoe Alonzo | Glen network chief | `Character.ma_hey_gle_02_outpost_miniboss` (inferred) | `{ma_hey_gle_02_com}` (11); site 42 | Valentino Alley | `world-activity` | `[inferred]` `[wiki]` |
| Rogelio Cruz | Zoe's field commander | `Character.ma_hey_gle_02_valentinos_grunt2_ranged2_ajax_ma_Rogelio_Cruz` | same | Valentino Alley | `world-activity` | `[game-data]` `[wiki]` |
| Miguel "Gizmo" Rodriguez | Mercado Sonora chief | `Character.ma_hey_rey_06_outpost_miniboss` (inferred) | `{ma_hey_rey_06_enemies}` (12); site 66 | Mercado Sonora | `world-activity` | `[inferred]` `[wiki]` |
| Dario Sanchez | High-ranking (imprisoned, killed) | none | — | Downtown (shard) | `historical` | `[wiki]` |
| Claudio Moreno | Downtown crew chief | `Character.ma_cct_dtn_02_claudio_moreno` | `{ma_cct_dtn_02_com}` (5); site 24 | Corporation St, Downtown | `world-activity` | `[game-data]` `[wiki]` |
| José Luis | Rogelio's subordinate; Arasaka instrument | `Character.sts_hey_spr_01_jose` | `{spr_01_jose_com}` (1); site 374 | Bus Depot | `world-activity` | `[game-data]` `[wiki]` |
| César Diego Ruiz | Glen boxing champion | `Character.mq025_cesar` | `{mq025_com_cesar}` (4) | the Glen | `world-activity` | `[game-data]` `[wiki]` |
| Alma Maria | Arms courier for Kendachi | `Character.ma_std_arr_02_alma` | site 124 `ma_std_arr_02` | Arroyo container terminal | `world-activity` | `[game-data]` `[wiki]` |
| Xavi Velez | Named outpost boss | `Character.ma_hey_gle_03_valentinos_grunt1_ranged1_nova_ma_Xavi_Velez` | `{ma_hey_gle_03_com}` (6); site 43 | Glen outpost | `world-activity` | `[game-data]` |
| Danilo Ruiz | Named outpost boss | `Character.ma_hey_gle_05_valentinos_grunt2_ranged2_overture_ma_Danilo_Ruiz` | `{ma_hey_gle_05_com}` (6); site 44 | Glen canal/sewer level | `world-activity` | `[game-data]` |
| Lena Dominguez | Named Valentina at the club | `Character.sts_hey_rey_02_valentinos_grunt1_ranged1_nue_wa_Lena_dominguez` | `{rey_02_com_enemies}` (12); site 370 | Dicky Twister | `world-activity` | `[game-data]` |
| Pablo | Named Valentino at the garage | `Character.spr_03_valentinos_man_Pablo` | `{spr_03_com}` (11); site 375 | Valentinos Auto Shop | `world-activity` | `[game-data]` |
| Ernesto Muñoz | Bouncer; Jackie's friend | `Character.gle_04_bouncer` (inferred) | `{gle_04_com}` (12); site 366 | El Pinche Pollo | `world-activity` | `[inferred]` `[wiki]` |
| Señor Ladrillo | Member; owner of Dicky Twister | none | site 370 | Dicky Twister | `off-map` | `[wiki]` |
| Saulo Capon | Ladrillo's lieutenant | none | — | Dicky Twister | `off-map` | `[wiki]` |
| Karubo Bairei | Non-member; owner of Jacked and Coke | `Character.sts_hey_rey_08_karubo` | `{rey_08_karubo_com}` (1); site 372 | Jacked and Coke | `world-activity` | `[game-data]` `[wiki]` |
| Sebastian "Padre" Ibarra | Ex-member; fixer and broker | `Character.Padre` | `#ws_padre_default` | Padre's Glen corner | `ambient` | `[game-data]` `[wiki]` |
| Jackie Welles | Ex-member; Campo's favourite, Gustavo's childhood friend | `Character.Jackie` | El Coyote Cojo crowd | El Coyote Cojo | `story` | `[game-data]` `[wiki]` |
| La Llorona | Ex-El Norte; El Sombrerón's sister | none | — | Badlands | `historical` | `[wiki]` `[lore]` |
| Raúl Welles | Member; Jackie's father | none | — | — | `historical` | `[wiki]` |
| Juan Esteban Abasto | Campo's messenger at Jackie's ofrenda | none | — | El Coyote Cojo | `off-map` | `[wiki]` |

Data cautions:

- **`Character.Padre` is a fixer, not a gang officer.** His wiki infobox reads
  `affiliation = Valentinos (formerly)`, and his database entry says he "doesn't
  support any particular group or gang." `[wiki]` He still runs the gang's gigs
  and takes contracts *against* its members.
- **`Karubo Bairei`'s infobox says `affiliation = Valentinos`**, but Padre's gig
  text says the gang is "friendly with him" and Karubo owns the bar; Gustavo
  tried to hire him and was refused. `[wiki]` Treat him as an asset, not a
  member.
- **Lena Dominguez, Pablo, Xavi Velez and Danilo Ruiz have no wiki pages.** The
  names come from the records; spelling is the record's.
- **Zoe and Miguel are one-record deductions.** They have no named record, so I
  map them to the site's single `*_outpost_miniboss`. At Valentino Alley both
  Zoe and Rogelio are present, but Rogelio has a named record, so the miniboss
  must be Zoe by elimination. Verify in-game.

### 1.5 What the game actually spawns (campaign disabled)

A named NPC in a wiki infobox does not mean an actor in free roam. This is the
part other systems must not assume.

**`ambient` — persists in free roam.**
- **Padre**, at his Glen corner. His registry entry has a `default` phase and a
  `default_glen` variant, with the workspot `#ws_padre_default`, and his only
  quest phase is the Streetkid prologue (`q000_01_street`). That is an ambient
  spawn, not a quest one. `[game-data]` Caveat: a fixer who persists is not the
  same as a fixer whose gigs are available; if the mod disables gigs, Padre is
  present but mute.

**`world-activity` — free-roam content, activity-gated.**
- **Gustavo Orta** (gig *Bring Me the Head of Gustavo Orta*, `baseid =
  sts_hey_rey_01`). Also a `story` cameo at Jackie's ofrenda in *Heroes*
  (`Character.sq018_rey_01_gustavo`, phases `funeral`/`ofrenda`/`outisde`). `[game-data]` `[wiki]`
- **Zoe Alonzo, Rogelio Cruz** (scanner hustle *Suspected Organized Crime
  Activity: Chapel*, `baseid = ma_hey_gle_02`). `[game-data]` `[wiki]`
- **Miguel Rodriguez** (scanner hustle *Suspected Organized Crime Activity
  (Vista del Rey)*, `baseid = ma_hey_rey_06`). `[game-data]` `[wiki]`
- **José Luis** (gig *On a Tight Leash*, `baseid = sts_hey_spr_01`). `[game-data]` `[wiki]`
- **Claudio Moreno** (Assault in Progress, Corporation St, Downtown). `[game-data]` `[wiki]`
- **Alma Maria** (Assault in Progress, Arroyo container terminal). `[game-data]` `[wiki]`
- **Xavi Velez, Danilo Ruiz** (named bosses of scanner-hustle outposts
  `ma_hey_gle_03` and `ma_hey_gle_05`). `[game-data]`
- **César Diego Ruiz** (*Beat on the Brat: The Glen*, `mq025_05_glen`). Minor
  job; `mq` prefix but free-roam availability. `[game-data]` `[wiki]`
- **Ernesto Muñoz** (El Pinche Pollo bouncer, *Fifth Column*). `[inferred]`
- **Karubo Bairei** (gig *Old Friends*, `baseid = sts_hey_rey_08`). Non-member. `[game-data]` `[wiki]`

**`story` — gated by the main/side job chain.**
- **Jackie Welles** (deceased; appears in *Heroes* and the prologue). `[wiki]`

**`off-map` — alive in 2077, never spawned.**
- **Campo Orta** (prison), **Señor Ladrillo** (out of town during his gig; his
  office is guarded by Saulo Capon, who also has no record), **Juan Esteban
  Abasto** (one-scene messenger). `[wiki]`

**`historical` — not in 2077.**
- **El Sombrerón** (dies in the 2077 comic), **La Llorona** (left in 2047),
  **Dario Sanchez** (killed before the downtown assault), **Raúl Welles**. `[wiki]` `[lore]`

Caveat: "campaign disabled" may also suppress gigs and scanner hustles. The
`world-activity` rows are the best reuse candidates; the `off-map` and
`story` rows are the ones to replace with simulation agents, not expect the game
to provide.

### 1.6 Player-path hooks

| Person | Join under | Climb past | Ally with | Remove |
| --- | --- | --- | --- | --- |
| **Gustavo Orta** | The Orta household: the family seat, the apartment detail, the 6th Street vendetta | He is interim, so climbing past him means the seat itself; the crews already ignore him | The apartment detail; César (a local celebrity); anyone who wants the war kept private | Killing or exiling Gustavo leaves Campo's claim open and forces a succession the gang has no rule for |
| **Zoe Alonzo** | The Glen rackets: extortion, kidnapping, robbery | Rogelio is her field commander and the practical gatekeeper | Rogelio and José Luis; the Glen's silence economy | Removing Zoe decapitates the Glen network and exposes the cop-killing cover-up |
| **Miguel Rodriguez** | The market: smuggling, trafficking, stalls, protection | He is a crew chief, not a ladder; climbing past him means taking the market | The market vendors; the netrunner unlocked after his hustle | Removing Miguel opens Mercado Sonora, the faction's busiest revenue point |
| **Claudio Moreno** | The Downtown crew: a detached racket with an NCPD contact | He already betrayed one boss; a player under him is one more loose end | Detective McCarlson (a channel, not a friend) | Removing Claudio severs the only proven NCPD corruption link |
| **Padre** | Not a membership path; he is the broker you impress | — | Padre is the natural **ally** for any player who respects the code: he supplies contracts, mediation and information | Removing Padre removes the faction's diplomatic layer and its 6th Street back-channel |
| **Ladrillo / Karubo** | Not joinable; they are **power centres** | — | Ladrillo: frontage, money, blackmail. Karubo: a neutral venue and a refusal to escalate | Taking Ladrillo's archive is a political weapon; killing Karubo closes a neutral bar |

The design consequence: the Valentinos have **no single ladder either**, but
unlike Maelstrom the split is not ideological — it is geographic. Back the Orta
seat, the Glen network, or the market, and each choice changes which places and
crews are friendly.

---

## 2. Internal political factions

### 2.1 The blocs

"Members" counts are **presence proxies** from `dist/extract/areas.jsonl` and
site rosters, not membership rolls. Several communities are overlapping quest
phases of one site, so do not sum them.

| Bloc | Leader(s) | What it wants | Presence / members hint | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- |
| **The Orta seat (Vista del Rey)** | Gustavo Orta; Campo Orta as the absent authority | Hold the family's claim, avenge Martha, keep a private war with 6th Street from dragging the crews in | `{rey_01_apartment_com}` 6, `{rey_01_reinforcement_com}` 2, `{rey_01_groud_floor_com}` 3; site 369: 12 units incl. 2 officers | Site 369 roster; shard *Gustavo and Karubo* ("can't drag my people into this"); wiki *Nolan Frakes*, *Gustavo Orta* | `[game-data]` `[wiki]` |
| **Zoe Alonzo's Glen network** | Zoe Alonzo; Rogelio Cruz as field commander | Run extortion, kidnapping and robbery; erase footage and witnesses; protect the crew from NCPD | `{ma_hey_gle_02_com}` 11, including a sniper and machete elites; site 42: 11 units | Shard *Got a problem* ("our turf… make sure all the security footage disappears"); *SOCA: Chapel* | `[game-data]` `[wiki]` |
| **Mercado Sonora smuggling wing** | Miguel "Gizmo" Rodriguez | Volume smuggling and trafficking through the barrio's market; control stalls and protection | `{ma_hey_rey_06_enemies}` 12; site 66: 12 units | NCPD dispatcher ("smuggling and trafficking operations"); wiki *Miguel Rodriguez* | `[game-data]` `[wiki]` |
| **The frontage bloc** | Señor Ladrillo (Dicky Twister); La Catrina's unnamed manager; El Pinche Pollo's crew | Keep the fronts legal-looking, keep NCPD out, preserve the blackmail archive, avoid open war | Dicky Twister 14, La Catrina 8, El Pinche Pollo 12 | *Sr. Ladrillo's Private Collection* (recordings of "politicians, suits, crime bosses, celebrities… maybe even the cops"); *Jeopardy* ("that's where they get rid of their bodies") | `[game-data]` `[wiki]` |
| **The Downtown crew** | Claudio Moreno | Hold a detached City Center racket; manage the NCPD relationship; succeed Dario | Site 24: 5 units; `{ma_cct_dtn_02_com}` 5 | Shards *Dario Sanchez and Claudio Moreno*, *Claudio Moreno and Aaron McCarlson* | `[game-data]` `[wiki]` |
| **The barrio and the community shield** | none | Protect residents, keep the gang's social immunity, remember the fallen as saints | The neighbourhood; ~6,000 members; murals and shrines | Wiki *Valentinos* philosophy and structure | `[wiki]` |
| **Padre's brokerage (non-member power centre)** | Sebastian Ibarra | Keep the balance of power in Heywood; enforce the code; broker between gangs, fixers and the nomads | Padre's Glen corner; a netrunner; NCPD informants ("my little rats") | Wiki *Sebastian Ibarra*; *Fifth Column*, *Jeopardy*, *The Lord Giveth…* | `[game-data]` `[wiki]` |
| **Karubo's bar (non-member asset)** | Karubo Bairei | Autonomy, quiet, no war work | Site 372: 13 units; the gang treats it as a hangout | *Old Friends*; shard *Gustavo and Karubo* (refuses a hit on 6th Street) | `[game-data]` `[wiki]` |
| **El Norte ancestry and the martyr cult** | none (El Sombrerón as a dead figurehead) | Legitimacy from El Norte and Theresa Valentino; saints, murals and songs for the fallen | Historical; no 2077 actors | Wiki *El Norte Cartel*, *Valentinos* history, *La Llorona* | `[wiki]` `[lore]` |

### 2.2 The vacant seat

This is the structural difference from every other gang document in this series.
Maelstrom's politics is a **coup**; the Valentinos' politics is a **vacancy**.

- Campo is the boss and is alive; he sent a messenger (Juan Esteban Abasto) to
  Jackie's ofrenda and was "extremely distraught" at the death. `[wiki]`
- Gustavo runs the street as interim, but the crews below him are not his. Zoe
  writes "on our turf" and gives orders in the Glen; Miguel runs the market;
  Claudio runs Downtown. `[wiki]` `[game-data]`
- Gustavo's own instinct is to keep his war private: "can't drag my people into
  this," he tells Karubo, when he tries to hire an outside killer to hit 6th
  Street. Karubo refuses and names the risk: "looking to start a private war
  with 6th street?" `[wiki]`

That is a simulation-ready axis: **dynastic authority vs. place autonomy**. The
seat commands loyalty in the abstract and very little in practice.

### 2.3 The Glen network and the cover-up culture

Zoe Alonzo's shard is the clearest internal-command document the gang has:

> "Rogelio, got a problem. One of your crew killed a cop on our turf. José Luis.
> NCPD got pissed, gonna raid us for sure. Make sure all the security footage
> disappears, make sure any witnesses know what happens to snitches. And tell
> Jose he's a fucking gonk and if he pulls a dumbass stunt like that again, I'll
> deal with him myself." — Zoe Alonzo `[wiki]`

Three things follow:

1. **The chain is Zoe → Rogelio → José**, independent of Gustavo.
2. **The gang's first response to a crisis is erasure**, not escalation. That is
   a coherent strategy for a gang whose immunity depends on the neighbourhood
   staying silent — and it is also what turns a single shooting into an NCPD
   crackdown.
3. **Zoe is willing to threaten a member to protect the network.** José is
   warned and then used; the NCPD crackdown that follows lands on Zoe and
   Rogelio, not on him. `[wiki]`

### 2.4 The frontage bloc and Ladrillo's archive

The gang's legal fronts are its political infrastructure, and the best evidence
is Dicky Twister:

- Ladrillo kept a computer "full of data thanks to spying tech in his VIP
  rooms… politicians, suits, crime bosses, celebrities (maybe even the cops
  themselves)." `[wiki]`
- Padre's own reasoning for stealing it is not morality, it is stability: "If
  the boys in blue get their hands on these recordings, Ladrillo's… house of
  cards collapses, leaving the whole district in chaos. And chaos isn't in our
  best interest at the moment." `[wiki]`

That archive is the faction's **mutual-assurance weapon**. It is also why the
frontage bloc is a bloc: it wants quiet, records kept, and the 6th Street war
contained. Whoever holds the archive can blackmail the city; whoever loses it
loses the district's arrangements.

### 2.5 Padre: the non-member centre of gravity

Padre is the most important political actor in the faction and he is not in it:

- He is an **ex-Valentino**, a former priest, and a survivor of the Moto Cielo
  bloodbath. `[wiki]`
- The database entry: he "started out by lining up jobs exclusively for his
  people from Heywood and the Valentinos — later he even shook hands with the
  likes of 6th Street… He doesn't support any particular group or gang — his
  interests lie in maintaining the delicate balance of power." `[wiki]`
- He runs the gang's entire gig economy: *Fifth Column*, *Jeopardy*, *On a Tight
  Leash*, *Bring Me the Head of Gustavo Orta*, *Old Friends*, *Sr. Ladrillo's
  Private Collection*, *The Lord Giveth and Taketh Away*. `[wiki]`
- He also **sanctions** the gang. He takes 6th Street's money to have Gustavo
  killed, and he contracts V to remove José Luis. `[wiki]`

Model him as `patron`: protection plus enforcement. He is not a member, not a
leader, and not neutral in the sense of uninvolved.

### 2.6 Karubo: the asset with a veto

Karubo Bairei is a retired solo who owns Jacked and Coke, "a hideout for the
Valentinos." The gang is "friendly with him," which is why Padre asks V not to
make a scene. `[wiki]`

The shard *Gustavo and Karubo* is a small masterpiece of internal politics:
Gustavo tries to hire him to hit 6th Street, offers double pay, and is refused —
"looking to start a private war with 6th street? you asked the wrong man."
`[wiki]` Karubo is therefore an asset with a **veto**: he can host the gang, and
he can refuse its most dangerous work.

### 2.7 The El Norte inheritance and the martyr cult

The gang's legitimacy is ancestral in two directions:

- **El Norte Cartel** is named as the Valentinos' predecessor, and El Norte
  financed Theresa Valentino's 2044 campaign for Santo Domingo city manager.
  Its members became "Valentino's Fists." `[wiki]`
- **Martyrdom** is the other half: Valentinos who die fighting other gangs,
  police or corporate enforcers "were often remembered as saints and martyrs,"
  commemorated in songs and giant murals. `[wiki]`

For the simulation this is a **legitimacy resource**, not a bloc: a leader who
avenges the dead gains standing; a leader who lets a death go unanswered loses
it. It also explains why Gustavo's private war is politically attractive even
when it is strategically stupid.

### 2.8 What could drive internal conflict in a simulation

Evidence-based drivers, in rough order of plausibility:

1. **The vacant seat.** Campo is absent, Gustavo is interim, and there is no
   succession rule. Removing either forces the gang to invent one.
2. **War vs. quiet.** Gustavo wants a private war with 6th Street; the frontage
   bloc and Padre want it contained, because the fronts are the revenue and the
   NCPD exposure. This is the main policy axis.
3. **Dynastic authority vs. place autonomy.** Zoe, Miguel and Claudio run their
   own turf. The seat commands loyalty in principle only.
4. **Cover-up culture.** Erasing witnesses protects a crew and invites a
   crackdown. A player can exploit it or expose it.
5. **Succession by betrayal.** Claudio proved a lieutenant can sell a boss to
   the NCPD, frame him as a snitch, and take the crew. Every leaderless crew is
   a target for the same move.
6. **Frontage leverage.** Ladrillo's recordings are a weapon that can be held,
   sold, stolen or lost to a raid.
7. **Cross-gang personal ties.** Gustavo and Martha Frakes; Xavi Velez and Nolan
   Frakes. Love and friendship cross the war line and create leaks, peace
   attempts, and accusations of the cardinal sin.
8. **The community shield.** Violence against the barrio erodes the loyalty that
   makes the gang immune to infiltration. An aggressive leader wins battles and
   loses the shield.

---

## 3. External relations matrix

### 3.1 Stance vocabulary

One stance per row, chosen by the precedence in `METHOD.md` §3: explicit violence
first, then explicit transaction, then quest-giver role, then adjacency, then a
neutral placeholder.

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
and `Affiliation.hpp` is identity only. Every stance below is judged from quests,
wiki and spatial adjacency, which is why each row carries a tag and why the
neutral rows are placeholders, not claims of friendship.

### 3.2 The matrix

| Faction | Code | Stance | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| Tyger Claws | `tyger_claws` | `neutral` | No attested conflict. Only overlaps are one Tyger NPC mixed into the Dicky Twister enemy group (`{rey_02_com_enemies}`: 1 Tyger, 12 Valentinos), shared street-race crowds (`sq024_com_*_race`), and a reused JapanTown prefab (`ma_hey_rey_01`). The location doc's "rival" is adjacency, not evidence `[game-data]` `[inferred]` | `game-data+inferred` |
| Arasaka | `arasaka` | `client` | Arasaka contracted José Luis's crew to attack an Arasaka facility dressed as Militech — a false flag to start a corporate war; the Bus Depot held Militech uniforms, ammo and vehicles for it; an unnamed Arasaka agent dealt with José directly `[game-data]` `[wiki]` | `game-data+wiki` |
| Militech | `militech` | `hostile` | The false-flag operation targets Militech; the gang fences stolen Militech vehicles (the SUV sold to the nomads) and stores Militech gear. One-way hostility, entangled with a Militech-covered corruption channel (Alvarado) `[game-data]` `[wiki]` | `game-data+wiki` |
| Kang Tao | `kang_tao` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Biotechnica | `biotechnica` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Petrochem | `petrochem` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Barghest | `barghest` | `neutral` | No attested interaction. Phantom Liberty only adds Valentino **crowd** records in the Dogtown stadium (`ep1_stadium_valentinos_non_reaction_*`), which is set dressing `[game-data]` `[inferred]` | `game-data+inferred` |
| 6th Street | `sixth_street` | `war` | Turf war since at least 2071 (a Westbrook firefight), escalated in 2074 over Vista del Rey, "intensifying" in 2077; 6th Street ambushed Gustavo and shot Martha; Nolan Frakes put a contract on Gustavo. Game data: `ma_hey_gle_11`, `ma_std_rcr_05`, and `sa_ep1_141` 4v4 street fights in the Glen `[game-data]` `[wiki]` | `game-data+wiki` |
| Aldecaldos | `aldecaldos` | `rival` | Sold a stolen Militech SUV to nomads, took the eddies, beat them and refused delivery; the nomads' rep Dakota called Padre to recover it. A commercial dispute with violence, mediated but unresolved `[wiki]` | `wiki` |
| Wraiths | `wraiths` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Animals | `animals` | `neutral` | No community area contains both factions. The only artifact is a single Valentino customer at Animals-owned Data Inc. (`sts_hey_spr_06`); Animals businesses sit inside Valentino-flagged Wellsprings sub-territories — adjacency, not conflict `[game-data]` `[inferred]` | `game-data+inferred` |
| The Mox | `the_mox` | `neutral` | Valentinos are customers at Lizzie's Bar (`lizzies_customer_*_valentinos`; `{wat_kab_com_lizzies_default}`: 16 Mox, 5 Valentinos). No conflict attested `[game-data]` `[inferred]` | `game-data+inferred` |
| Maelstrom | `maelstrom` | `hostile` | A 2070s gang-war firefight with Maelstrom nearly killed Jackie Welles — he left the gang because of it; Maelstrom kidnapped Lely Hein to force-recruit him, the implant went wrong, and Valentino netrunner Tamara Cosby went cyberpsycho searching for him `[wiki]` | `wiki` |
| Voodoo Boys | `voodoo_boys` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| NCPD | `ncpd` | `hostile` | Standing target: SOCA at Valentino Alley and Mercado Sonora, Assault in Progress in Downtown and Arroyo, and Zoe Alonzo's NCPD record. But a corrupt channel exists: Detective Aaron McCarlson conspired with Claudio Moreno to frame and murder Dario Sanchez, and Padre has informants in NCPD command `[game-data]` `[wiki]` | `game-data+wiki` |
| Night Corp | `night_corp` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| City Council | `city_council` | `trade` | Advisor Javier Alvarado (office of interim mayor Weldon Holt) embezzles public money into the gang, is a regular at El Pinche Pollo, and has Militech allies covering it; *Fifth Column* recovers the evidence. A purchased channel, no loyalty `[game-data]` `[wiki]` | `game-data+wiki` |
| Scavengers | `scavengers` | `neutral` | No reliable incident. The only game-data support was `{sa_ep1_135_com_combat}`, a Phantom Liberty courier-loop pool that METHOD §1.3 item 3 excludes. Both work Vista del Rey's chrome and organ trade and Jackie Welles, an ex-Valentino, despised scavs, but that is overlap and one man's antipathy, not a gang-level fight `[game-data]` `[wiki]` `[inferred]` | `wiki+inferred` |
| Regina Jones | `fixer_regina` | `neutral` | No Valentino-specific gig or lore link found; her gigs are Watson `[inferred]` | `inferred` |
| Wakako Okada | `fixer_wakako` | `neutral` | No Valentino-specific gig or lore link found `[inferred]` | `inferred` |
| Sebastian Ibarra (Padre) | `fixer_padre` | `patron` | Ex-Valentino priest; runs the gang's gigs, brokers with 6th Street and Dakota, and stole Ladrillo's blackmail to keep NCPD from toppling the district — while also taking contracts on Valentinos who break the code (Gustavo, José Luis). Protection plus enforcement `[game-data]` `[wiki]` | `game-data+wiki` |
| Muamar Reyes (El Capitan) | `fixer_el_capitan` | `neutral` | No Valentino-specific gig or lore link found `[inferred]` | `inferred` |
| Dakota Smith | `fixer_dakota` | `neutral` | Dakota called Padre to recover the nomads' SUV from the Valentinos; a mediated dispute, not a relationship `[wiki]` | `wiki` |
| Dino Dinovic | `fixer_dino` | `neutral` | No attested interaction. Padre's gigs spill into City Center and the gang holds a Downtown sub-territory, which is adjacency only `[inferred]` | `inferred` |
| Rogue Amendiares | `fixer_rogue` | `neutral` | No Valentino-specific gig or lore link found `[inferred]` | `inferred` |
| Mr. Hands | `fixer_mr_hands` | `neutral` | No Valentino-specific gig or lore link found `[inferred]` | `inferred` |
| Afterlife | `afterlife` | `neutral` | `{afterlife_com}` crowd includes 3 Valentino-tagged NPCs; neutral merc ground `[game-data]` `[inferred]` | `game-data+inferred` |
| Kendachi | `kendachi` | `trade` | Alma Maria dealt arms with Kendachi director candidate Matheus Stove and moved his warehouse stock; an Assault in Progress in Arroyo `[wiki]` | `wiki` |

### 3.3 Actors outside `data/factions.json`

Real relationships with no faction code, so prose only:

- **El Norte Cartel** — the predecessor organisation, boss Rubén Meza, HQ
  Salón de Valentino. No 2077 presence. `[wiki]` `[lore]`
- **Theresa Valentino** — 2040s Santo Domingo city manager, financed by El
  Norte; the cartel's members became "Valentino's Fists". Attested ancestry,
  unproven namesake. `[wiki]` `[lore]`
- **Nolan Frakes** (6th Street) — ordered the hit on Gustavo; his daughter was
  the unintended casualty; then hired Padre to finish Gustavo. `[wiki]`
- **Martha Frakes** — 6th Street daughter, Gustavo's girlfriend, comatose. The
  human cost of the war and the reason Gustavo is compromised. `[wiki]`
- **Aaron McCarlson** — NCPD detective and Claudio Moreno's accomplice. `[wiki]`
- **Javier Alvarado** — advisor to interim mayor **Weldon Holt**; the gang's City
  Hall channel. `[wiki]`
- **Kirk Sawyer** — fixer killed by Thomas Hays's Valentino crew at Tirempire
  Auto Shop, Arroyo. A fixer, but not one of the eight in `data/factions.json`. `[wiki]`
- **Saulo Capon** — Ladrillo's lieutenant, guarding his office. `[wiki]`
- **Juan Esteban Abasto** — Campo's messenger at Jackie's ofrenda. `[wiki]`
- **Matheus Stove** — Kendachi director candidate who bought the gang's silence. `[wiki]`
- **Karubo Bairei** — retired solo, bar owner, gang-friendly. Not a faction. `[wiki]`
- **Aarno** — La Llorona's Militech corporate husband. A historical family tie,
  not a channel. `[wiki]` `[lore]`

### 3.4 Guarantor assessment

The design question: if a player founds a gang, which factions would guarantee
the Valentinos' support, and which would the Valentinos guarantee?

- **No `ally` row.** The matrix's only `patron` is Padre, an individual fixer with
  a balance-of-power doctrine, not a bloc. There is no faction that would fight
  for the Valentinos.
- **The gang's political capital is four things**: the barrio's community shield,
  Ladrillo's blackmail archive, the Alvarado/Holt channel, and the Orta name.
  Three of the four are individuals, and all four are fragile.
- **The Valentinos are a poor guarantor.** A player who takes over inherits a war
  with 6th Street, NCPD hostility, a live Arasaka false-flag entanglement, and a
  vacant seat that invites a coup.
- **Plausible guarantors for a player-founded gang** are transactional: Padre
  (mediation, contracts, information), a corrupt NCPD detective (McCarlson-type),
  Kendachi (an arms buyer), and the Aldecaldos (if the SUV debt is settled). Not
  6th Street, not Maelstrom, and not the NCPD as an institution.
- **The Valentinos as a guarantor** for a player: a player who befriends one
  place-crew (Zoe's Glen network or Miguel's market) gets local muscle and a
  market to sell through; the gang as a whole can guarantee nothing while the
  seat is vacant. That asymmetry is the faction's defining political weakness.

---

## 4. Pillar notes

Design claims from `docs/design/gameplay-systems.md`: the Valentinos are a
**Syndicate** (archetype strength **Economy**, weakness **Military**); faction
strength **Culture**, weakness **Politics**.

| Pillar | Design claim | Lore verdict | Evidence |
| --- | --- | --- | --- |
| Culture (faction strength) | Chicano culture is the gang's binding force | **Strongly supported.** Santa Muerte and Jesús Malverde, Day of the Dead, Quinceañeras, Semana Santa, Guadalupe; murals and narcocorridos for the dead; a "protect the barrio" code; ethnic openness with cultural assimilation. Culture is also the gang's **export**: corpos, athletes and BD stars imitate Valentino style and buy from their chop shops. | Wiki *Valentinos* overview, philosophy and Behind the Scenes; La Catrina's saint imagery `[wiki]` |
| Politics (faction weakness) | The gang cannot do politics | **Supported, with one complication.** No headquarters, a boss in prison, place-crews that act independently, a policy split over the 6th Street war, and succession by family or betrayal. The complication: there *is* a real political channel — Javier Alvarado, Padre's brokerage, and the Dicky Twister archive. The weakness is **no unified political voice**, not zero politics. | Blank `headquarters`; Campo in prison; Zoe's "our turf"; Claudio/Dario; Alvarado; Ladrillo's recordings `[wiki]` `[game-data]` |
| Economy (archetype strength) | The gang is economically strong | **Supported.** Legal fronts (funeral home, club, market, restaurant, auto shop, bus depot) plus gun smuggling, chop shops, drugs, prostitution, robbery, protection and sports betting. It is a diversified cash economy with laundering built in. The weakness is structural: everything sits in three barrios, the fronts are gig targets, and there is no finance or real-estate scale. Model it as **high, raidable income**, not invulnerable income. | Wiki "Source of Income"; the location doc's revenue map `[wiki]` `[game-data]` |
| Military (archetype weakness) | The gang cannot project force | **Supported.** No armour, air or heavy weapons; street crews with machetes, Overtures and shotguns, plus a few tier-3 elites (`Sicario`, `Toro`, `Francotirador`). Its largest concentration is 20 units at a bus depot used as a staging site. It loses to corpos and to NCPD raids and cannot hold ground against 6th Street's escalation. | Enemy tier list; site 374 (20 units); the 6th Street war `[wiki]` `[game-data]` |
| Overall fit | The pillars fit the faction's identity | **Good for identity, precise for balance.** Keep Culture strong and Politics weak. Treat Economy as "rich but raidable" and Military as "street-capable, no projection." | Synthesis `[inferred]` |

Design cautions, not redesigns:

- Do **not** model Politics as zero. The gang has a purchased City Hall channel,
  a broker with a doctrine, and a blackmail archive. Losing them should hurt.
- Do **not** model the gang as poor. It is one of the two richest gangs in the
  game by revenue type; its problem is legitimacy and force, not turnover.
- The **vacant seat** is the faction's signature political mechanic. Any
  succession system should treat "boss alive but absent" as a distinct state
  from "boss dead."

---

## 5. Gaps and uncertainties

1. **Campo Orta has no actor, record or marker.** His prison is off-map. His
   leadership is known only from wiki text, the *Heroes* dialogue ("four more
   years"), and the Members page. Any seat mechanic must be invented, not
   located.
2. **El Sombrerón's 2077 death is comic-only.** *You Have My Word* kills him in
   the Badlands; the game has no record. The Valentinos page still lists him as
   a secondary leader "unknown–2077." Treat his death as canon-adjacent, not
   game-verifiable.
3. **"Sets" is not attested in any 2077 source I could read.** The wiki's gang
   pages use boss/lieutenant/member, and the Valentinos page adds no cell
   vocabulary. The 2077 structure is **place-crews**. Do not import the tabletop
   term silently.
4. **Zoe Alonzo's and Miguel Rodriguez's records are one-record deductions**
   (`*_outpost_miniboss`). Verify in-game before seeding them as exact actors.
5. **At Valentino Alley two high-rankers share one site** and only Rogelio has a
   named record; the miniboss must be Zoe by elimination. That is an inference,
   not a direct match.
6. **Ernesto Muñoz is mapped by elimination** to `Character.gle_04_bouncer`, the
   only bouncer slot at El Pinche Pollo.
7. **Padre is a member in one source and an independent in another.** The
   infobox says "Valentinos (formerly)"; the database entry says he supports no
   group. He still enforces the code with contracts. Treated as `patron`.
8. **Ladrillo's affiliation is inconsistent inside the wiki.** One page says
   "owner of Dicky Twister," the location page says "Valentinos member," and he
   has no record (he is "out of town" during the gig). His lieutenant Saulo
   Capon also has no record.
9. **Karubo's infobox says `affiliation = Valentinos`**, but the gig text and the
   shard describe a friendly outsider who refuses war work. Treated as a
   non-member asset, flagged.
10. **There is no canonical headquarters.** The infobox `headquarters` field is
    blank; the location doc's La Catrina choice is a reasoned substitute. Politics
    therefore has no seat to anchor a "capital" on.
11. **The seeded map does not match the political map.** Gustavo's flat sits in
    a Militech-owned Corpo Plaza sub-territory (location doc), while the
    Downtown crew operates in a Valentino-owned Downtown South Quay sub-territory.
    Neither reflects the faction's real centre of gravity.
12. **`areas.jsonl` co-occurrence is weak relation evidence.** `{04_NPC_Gang_Community_Area}`
    and `mq061_*` are respawn pools, `{wat_kab_com_lizzies_default}` is a customer
    crowd, and `{q305_com_border_crossing_}002` is a scripted crowd. I used
    co-occurrence only to corroborate wiki-attested rows.
13. **The best game-data evidence of the 6th Street war is base-game street
    activity.** `ma_hey_gle_11` and `ma_std_rcr_05` are 4v4 shootouts. The
    Phantom Liberty `{sa_ep1_135_com_combat}` and `{sa_ep1_141_com_combat}`
    pools are courier-loop spawn tables and are not relation evidence
    (METHOD §1.3 item 3). None of these is a territory claim.
14. **Phantom Liberty stadium records are set dressing.** `ep1_stadium_valentinos_non_reaction_*`
    are crowd variants by time of day in the Dogtown stadium. They do not
    indicate a Valentino operation in Dogtown.
15. **Four named members have no wiki page** (Lena Dominguez, Pablo, Xavi Velez,
    Danilo Ruiz). Their names and roles are read from records only; Xavi also
    appears in a 6th Street shard, so his faction is inferred from his record and
    site.
16. **`ma_std_arr_02` (Alma Maria) is not a Valentino holding.** It has no
    default faction, a 6th Street initial owner, and one Valentino working party.
    Do not count it as territory.
17. **NCPD corruption is attested at detective level only** (McCarlson) and
    through Padre's informants. Do not model an institutional NCPD channel.
18. **The Arasaka relationship is one covert contract**, not a standing client
    relationship. The shard implies Gustavo knew José was in trouble; the wiki
    does not say the gang's leadership authorised the false flag.
19. **The name lineage is partly unresolved.** The 2077 gang descends from El
    Norte Cartel (attested), but the link to the 2020s "Valentino's" posergang is
    explicitly unrevealed by the developers. Do not assert it.
20. **No member counts per clique.** Community entries are presence proxies, and
    several are overlapping quest phases of one site. Do not sum them.

### 5.1 Sources consulted

- Local: `data/sites/rosters.json`, `data/sites/sites.json`,
  `data/sites/{communities,guards,triggers,spots,patrols,doors}.json`,
  `data/factions.json`, `data/sub_territories.json`, `data/control_centers.json`,
  `data/districts.json`, `dist/extract/areas.jsonl`, `dist/extract/markers.jsonl`,
  `dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_1.streamingsector.json`
  (community registry: `characterRecordId`, `entryName`, `phaseName`,
  `spotNodeRefs`).
- Wiki: [Valentinos](https://cyberpunk.fandom.com/wiki/Valentinos),
  [Valentinos Members](https://cyberpunk.fandom.com/wiki/Valentinos_Members),
  [Campo Orta](https://cyberpunk.fandom.com/wiki/Campo_Orta),
  [Gustavo Orta](https://cyberpunk.fandom.com/wiki/Gustavo_Orta),
  [El Sombrerón](https://cyberpunk.fandom.com/wiki/El_Sombrer%C3%B3n),
  [La Llorona](https://cyberpunk.fandom.com/wiki/La_Llorona),
  [El Norte Cartel](https://cyberpunk.fandom.com/wiki/El_Norte_Cartel),
  [Zoe Alonzo](https://cyberpunk.fandom.com/wiki/Zoe_Alonzo),
  [Rogelio Cruz](https://cyberpunk.fandom.com/wiki/Rogelio_Cruz),
  [Miguel Rodriguez](https://cyberpunk.fandom.com/wiki/Miguel_Rodriguez),
  [José Luis](https://cyberpunk.fandom.com/wiki/Jos%C3%A9_Luis),
  [Claudio Moreno](https://cyberpunk.fandom.com/wiki/Claudio_Moreno),
  [César Diego Ruiz](https://cyberpunk.fandom.com/wiki/C%C3%A9sar_Diego_Ruiz),
  [Alma Maria](https://cyberpunk.fandom.com/wiki/Alma_Maria),
  [Ernesto Muñoz](https://cyberpunk.fandom.com/wiki/Ernesto_Mu%C3%B1oz),
  [Señor Ladrillo](https://cyberpunk.fandom.com/wiki/Se%C3%B1or_Ladrillo),
  [Karubo Bairei](https://cyberpunk.fandom.com/wiki/Karubo_Bairei),
  [Sebastian Ibarra](https://cyberpunk.fandom.com/wiki/Sebastian_Ibarra),
  [Jackie Welles](https://cyberpunk.fandom.com/wiki/Jackie_Welles),
  [Nolan Frakes](https://cyberpunk.fandom.com/wiki/Nolan_Frakes),
  [Martha Frakes](https://cyberpunk.fandom.com/wiki/Martha_Frakes),
  [Javier Alvarado](https://cyberpunk.fandom.com/wiki/Javier_Alvarado),
  [Weldon Holt](https://cyberpunk.fandom.com/wiki/Weldon_Holt),
  [Lely Hein](https://cyberpunk.fandom.com/wiki/Lely_Hein),
  [Tamara Cosby](https://cyberpunk.fandom.com/wiki/Tamara_Cosby),
  [Thomas Hays](https://cyberpunk.fandom.com/wiki/Thomas_Hays),
  [Dicky Twister](https://cyberpunk.fandom.com/wiki/Dicky_Twister),
  [La Catrina](https://cyberpunk.fandom.com/wiki/La_Catrina),
  [El Coyote Cojo](https://cyberpunk.fandom.com/wiki/El_Coyote_Cojo),
  [Moto Cielo](https://cyberpunk.fandom.com/wiki/Moto_Cielo).
- Quest and shard pages: [Heroes](https://cyberpunk.fandom.com/wiki/Heroes),
  [Gig: Bring Me the Head of Gustavo Orta](https://cyberpunk.fandom.com/wiki/Gig:_Bring_Me_the_Head_of_Gustavo_Orta),
  [Gig: On a Tight Leash](https://cyberpunk.fandom.com/wiki/Gig:_On_a_Tight_Leash),
  [Gig: Fifth Column](https://cyberpunk.fandom.com/wiki/Gig:_Fifth_Column),
  [Gig: Old Friends](https://cyberpunk.fandom.com/wiki/Gig:_Old_Friends),
  [Gig: Jeopardy](https://cyberpunk.fandom.com/wiki/Gig:_Jeopardy),
  [Gig: The Lord Giveth and Taketh Away](https://cyberpunk.fandom.com/wiki/Gig:_The_Lord_Giveth_and_Taketh_Away),
  [Gig: Sr. Ladrillo's Private Collection](https://cyberpunk.fandom.com/wiki/Gig:_Sr._Ladrillo%27s_Private_Collection),
  [Suspected Organized Crime Activity: Chapel](https://cyberpunk.fandom.com/wiki/Suspected_Organized_Crime_Activity:_Chapel),
  [Suspected Organized Crime Activity (Vista del Rey)](https://cyberpunk.fandom.com/wiki/Suspected_Organized_Crime_Activity_(Vista_del_Rey)),
  [Beat on the Brat: The Glen](https://cyberpunk.fandom.com/wiki/Beat_on_the_Brat:_The_Glen),
  [Got a problem](https://cyberpunk.fandom.com/wiki/Got_a_problem),
  [Archived Conversation: Jose and Gustavo](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Jose_and_Gustavo),
  [Archived Conversation: Gustavo and Karubo](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Gustavo_and_Karubo),
  [Archived Conversation: Nolan and Xavi](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Nolan_and_Xavi),
  [Archived Conversation: Dario Sanchez and Claudio Moreno](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Dario_Sanchez_and_Claudio_Moreno),
  [Archived Conversation: Claudio Moreno and Aaron McCarlson](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Claudio_Moreno_and_Aaron_McCarlson).
- Enemy pages for the combat tiers: *Valentinos Thug*, *Gangoon*,
  *Sanguinario*, *Seasoned Thug*, *Guerrero*, *Macho*, *Matón*, *Sicario*,
  *Toro*, *Francotirador*.
- Earlier repo research: `docs/research/factions/valentinos.md`,
  `docs/research/factions/METHOD.md`, `docs/research/factions/politics/maelstrom.md`,
  `docs/design/gameplay-systems.md`, `docs/research/factions/sixth-street.md`,
  `docs/research/factions/animals.md`.

---

## 6. Machine-readable block

```json
{
  "faction_code": "valentinos",
  "leaders": [
    {
      "name": "Campo Orta",
      "role": "Boss (incarcerated; four years left in 2077)",
      "character_record_id": null,
      "location_name": "Prison (off-map)",
      "presence_class": "off-map",
      "open_world": false,
      "source": "wiki Valentinos Leadership; wiki Campo Orta; Heroes dialogue",
      "confidence": "wiki"
    },
    {
      "name": "Gustavo Orta",
      "role": "Interim leader on the street; Orta family seat",
      "character_record_id": "Character.sts_hey_rey_01_gustavo",
      "location_name": "Gustavo Orta's Apartment, Vista del Rey",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "raw always_loaded_1 registry entry gustavo (phases A_spawn/B/C); Character.sq018_rey_01_gustavo; site 369 sts_hey_rey_01; wiki Nolan Frakes (interim leader); wiki Gustavo Orta",
      "confidence": "game-data+wiki"
    },
    {
      "name": "El Sombrerón",
      "role": "Secondary leader (dies in 2077, comic)",
      "character_record_id": null,
      "location_name": "Badlands (off-map)",
      "presence_class": "historical",
      "open_world": false,
      "source": "wiki Valentinos Leadership; wiki El Sombrerón; Cyberpunk 2077: You Have My Word",
      "confidence": "wiki+lore"
    },
    {
      "name": "Zoe Alonzo",
      "role": "High-ranking member; Glen network chief",
      "character_record_id": "Character.ma_hey_gle_02_outpost_miniboss",
      "location_name": "Valentino Alley, the Glen",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "site 42 ma_hey_gle_02 (11 units, default phase); SOCA Chapel; shard Got a problem; wiki Zoe Alonzo",
      "confidence": "inferred+wiki"
    },
    {
      "name": "Rogelio Cruz",
      "role": "High-ranking member; Zoe's field commander",
      "character_record_id": "Character.ma_hey_gle_02_valentinos_grunt2_ranged2_ajax_ma_Rogelio_Cruz",
      "location_name": "Valentino Alley, the Glen",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "raw always_loaded_1 registry entry ganger_04 (phase default, spot #ma_hey_gle_02_ws_ganger_04_a); roster site 42; wiki Rogelio Cruz",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Miguel \"Gizmo\" Rodriguez",
      "role": "High-ranking member; Mercado Sonora smuggling chief",
      "character_record_id": "Character.ma_hey_rey_06_outpost_miniboss",
      "location_name": "Mercado Sonora, Vista del Rey",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "site 66 ma_hey_rey_06 (12 units); SOCA Vista del Rey; wiki Miguel Rodriguez",
      "confidence": "inferred+wiki"
    },
    {
      "name": "Dario Sanchez",
      "role": "High-ranking member (imprisoned, then killed by his lieutenant)",
      "character_record_id": null,
      "location_name": "Downtown (shard only)",
      "presence_class": "historical",
      "open_world": false,
      "source": "wiki Valentinos Members; shards Dario Sanchez/Claudio Moreno and Claudio Moreno/Aaron McCarlson",
      "confidence": "wiki"
    },
    {
      "name": "Claudio Moreno",
      "role": "Downtown crew chief; Dario's lieutenant",
      "character_record_id": "Character.ma_cct_dtn_02_claudio_moreno",
      "location_name": "Corporation St, Downtown",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "raw always_loaded_1 registry entry enemy01 (phases start); site 24 ma_cct_dtn_02 (5 units); wiki Claudio Moreno",
      "confidence": "game-data+wiki"
    }
  ],
  "internal_factions": [
    {
      "name": "The Orta seat (Vista del Rey)",
      "leader": "Gustavo Orta",
      "goals": "Hold the Orta family's claim while Campo is in prison; avenge Martha; keep a private war with 6th Street from dragging the crews in",
      "members_hint": "rey_01_apartment_com 6, rey_01_reinforcement_com 2, rey_01_groud_floor_com 3; site 369 12 units incl. 2 officers",
      "source": "roster site 369; shard Gustavo and Karubo; wiki Nolan Frakes and Gustavo Orta",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Zoe Alonzo's Glen network",
      "leader": "Zoe Alonzo",
      "goals": "Run extortion, kidnapping and robbery in the Glen; erase evidence and silence witnesses; protect the crew from NCPD",
      "members_hint": "ma_hey_gle_02_com 11 (sniper, machete elites); Rogelio Cruz; José Luis",
      "source": "site 42; shard Got a problem; SOCA Chapel; wiki Zoe Alonzo and Rogelio Cruz",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Mercado Sonora smuggling wing",
      "leader": "Miguel \"Gizmo\" Rodriguez",
      "goals": "Volume smuggling and trafficking through the barrio market; control stalls and protection",
      "members_hint": "ma_hey_rey_06_enemies 12; site 66",
      "source": "site 66; NCPD dispatcher; wiki Miguel Rodriguez",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The frontage bloc",
      "leader": "Señor Ladrillo",
      "goals": "Keep the legal fronts legal-looking, keep NCPD out, preserve the blackmail archive, avoid open war",
      "members_hint": "Dicky Twister 14, La Catrina 8, El Pinche Pollo 12",
      "source": "Gig: Sr. Ladrillo's Private Collection; Gig: Jeopardy; wiki Dicky Twister and La Catrina",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The Downtown crew",
      "leader": "Claudio Moreno",
      "goals": "Hold a detached City Center racket; manage the NCPD relationship; succeed Dario",
      "members_hint": "site 24 ma_cct_dtn_02 5 units; ma_cct_dtn_02_com 5",
      "source": "site 24; shards Dario Sanchez/Claudio Moreno and Claudio Moreno/Aaron McCarlson",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The barrio and the community shield",
      "leader": null,
      "goals": "Protect residents, keep the gang's social immunity, remember the fallen as saints",
      "members_hint": "the neighbourhood; about 6000 members; murals and shrines",
      "source": "wiki Valentinos philosophy and structure",
      "confidence": "wiki"
    },
    {
      "name": "Padre's brokerage (non-member power centre)",
      "leader": "Sebastian \"Padre\" Ibarra",
      "goals": "Keep the balance of power in Heywood; enforce the code; broker between gangs, fixers and nomads",
      "members_hint": "Padre's Glen corner; a netrunner; NCPD informants",
      "source": "wiki Sebastian Ibarra; gigs Fifth Column, Jeopardy, The Lord Giveth and Taketh Away",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Karubo's bar (non-member asset)",
      "leader": "Karubo Bairei",
      "goals": "Autonomy and quiet; refuse war work",
      "members_hint": "site 372 13 units; rey_08_karubo_com 1",
      "source": "Gig: Old Friends; shard Gustavo and Karubo",
      "confidence": "game-data+wiki"
    },
    {
      "name": "El Norte ancestry and the martyr cult",
      "leader": null,
      "goals": "Legitimacy from El Norte and Theresa Valentino; saints, murals and songs for the fallen",
      "members_hint": "historical; no 2077 actors",
      "source": "wiki El Norte Cartel; wiki Valentinos history; wiki La Llorona and El Sombrerón",
      "confidence": "wiki+lore"
    }
  ],
  "relations": [
    {
      "faction_code": "tyger_claws",
      "stance": "neutral",
      "evidence": "No attested conflict; only overlaps are one Tyger NPC in the Dicky Twister enemy group (rey_02_com_enemies: 1 Tyger, 12 Valentinos), shared street-race crowds, and a reused JapanTown prefab (ma_hey_rey_01) [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "arasaka",
      "stance": "client",
      "evidence": "Arasaka contracted José Luis's crew to attack an Arasaka facility dressed as Militech (false flag); the Bus Depot held Militech uniforms, ammo and vehicles for it; an unnamed Arasaka agent dealt with José directly [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "militech",
      "stance": "hostile",
      "evidence": "The false-flag operation targets Militech; the gang fences stolen Militech vehicles and stores Militech gear; one-way hostility entangled with a Militech-covered corruption channel (Alvarado) [game-data] [wiki]",
      "confidence": "game-data+wiki"
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
      "evidence": "No attested interaction; Phantom Liberty only adds Valentino stadium crowd records in Dogtown (set dressing) [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "sixth_street",
      "stance": "war",
      "evidence": "Turf war since at least 2071 (Westbrook firefight), escalated in 2074 over Vista del Rey and intensifying in 2077; 6th Street ambushed Gustavo and shot Martha; Nolan Frakes put a contract on Gustavo; game data: ma_hey_gle_11, ma_std_rcr_05, sa_ep1_141 4v4 Glen fights [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "aldecaldos",
      "stance": "rival",
      "evidence": "Sold a stolen Militech SUV to nomads, took the eddies, beat them and refused delivery; Dakota called Padre to recover it [wiki]",
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
      "evidence": "No community area contains both factions; the only artifact is one Valentino customer at Animals-owned Data Inc. (sts_hey_spr_06); Animals businesses sit inside Valentino-flagged Wellsprings sub-territories - adjacency, not conflict [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "the_mox",
      "stance": "neutral",
      "evidence": "Valentinos are customers at Lizzie's Bar (lizzies_customer_*_valentinos; wat_kab_com_lizzies_default: 16 Mox, 5 Valentinos); no conflict attested [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "maelstrom",
      "stance": "hostile",
      "evidence": "A 2070s gang-war firefight with Maelstrom nearly killed Jackie Welles and he left the gang because of it; Maelstrom kidnapped Lely Hein to force-recruit him, the implant went wrong, and Valentino netrunner Tamara Cosby went cyberpsycho searching for him [wiki]",
      "confidence": "wiki"
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
      "evidence": "Standing target: SOCA at Valentino Alley and Mercado Sonora, Assault in Progress in Downtown and Arroyo; but a corrupt channel exists - Detective Aaron McCarlson conspired with Claudio Moreno to frame and murder Dario Sanchez, and Padre has informants in NCPD command [game-data] [wiki]",
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
      "evidence": "Advisor Javier Alvarado (office of interim mayor Weldon Holt) embezzles public money into the gang, is a regular at El Pinche Pollo, and has Militech allies covering it; Fifth Column recovers the evidence - a purchased channel, no loyalty [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "scavengers",
      "stance": "neutral",
      "evidence": "No reliable incident. The only game-data support was sa_ep1_135_com_combat, a Phantom Liberty courier-loop pool that METHOD 1.3 item 3 excludes. Both work Vista del Rey's chrome and organ trade and Jackie Welles, an ex-Valentino, despised scavs, but that is overlap and one man's antipathy, not a gang-level fight [game-data] [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "fixer_regina",
      "stance": "neutral",
      "evidence": "No Valentino-specific gig or lore link found; her gigs are Watson [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_wakako",
      "stance": "neutral",
      "evidence": "No Valentino-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_padre",
      "stance": "patron",
      "evidence": "Ex-Valentino priest; runs the gang's gigs, brokers with 6th Street and Dakota, and stole Ladrillo's blackmail to keep NCPD from toppling the district - while also taking contracts on Valentinos who break the code (Gustavo, José Luis); protection plus enforcement [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_el_capitan",
      "stance": "neutral",
      "evidence": "No Valentino-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_dakota",
      "stance": "neutral",
      "evidence": "Dakota called Padre to recover the nomads' SUV from the Valentinos; a mediated dispute, not a relationship [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "fixer_dino",
      "stance": "neutral",
      "evidence": "No attested interaction; Padre's gigs spill into City Center and the gang holds a Downtown sub-territory, which is adjacency only [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_rogue",
      "stance": "neutral",
      "evidence": "No Valentino-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_mr_hands",
      "stance": "neutral",
      "evidence": "No Valentino-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "afterlife",
      "stance": "neutral",
      "evidence": "afterlife_com crowd includes 3 Valentino-tagged NPCs; neutral merc ground [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "kendachi",
      "stance": "trade",
      "evidence": "Alma Maria dealt arms with Kendachi director candidate Matheus Stove and moved his warehouse stock; an Assault in Progress in Arroyo [wiki]",
      "confidence": "wiki"
    }
  ]
}
```
