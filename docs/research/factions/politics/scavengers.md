# Scavengers — Leadership, Internal Politics and External Relations

Status: research run, 2026-11-25. One faction, one document.
Scope: Cyberpunk 2077 2.5 + Phantom Liberty, campaign disabled. Who a player can
join under, climb past, ally with or remove; the internal cells; and the external
relations matrix needed for wars, alliances and "guarantor" support when a player
founds a gang.
Method: this document follows [`METHOD.md`](./METHOD.md), including its §1.1–§1.3
corrections. The location catalog for the Scavengers is
[`../scavengers.md`](../scavengers.md); this document maps people and politics
onto those places and does not repeat the coordinates.

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page via the MediaWiki API (cited inline) | Secondary, high |
| `[lore]` | Book/comic/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My reasoning links a named person, place or stance to a record; reasoning stated | Weak, flagged |

**Presence class**, an extra convention for this document only. `ambient` =
persists in free roam without a quest; `world-activity` = gig, scanner hustle,
assault-in-progress or minor job, i.e. free-roam content but still
activity-gated; `story` = main/side job gated; `prologue` = lifepath intro (no
Scav uses this); `off-map` = named and alive in 2077 but never spawned;
`mentioned` = named only in shards, dialogue or a computer message;
`historical` = not present in 2077. The JSON `open_world` flag is `true` for
`ambient` + `world-activity`, `false` for `story` + `prologue` + `off-map` +
`mentioned` + `historical`.

The Scavengers are the hardest faction in this series for one reason: **there is
no faction-level leader to find**. The wiki's organization infobox leaves
`headquarters` and `leadership` blank; `data/faction_headquarters.json` has no
fid-7 row; and the faction text is explicit that they "tend to operate in small
groups, with no official hierarchy to unite them, nor do they have a designated
piece of turf". `[wiki]` `[game-data]` This document therefore models **cells**,
not a chain of command, and treats every named boss as a local power centre.

---

## 1. Leadership and ranks

### 1.1 The 2077 chain of command

The Scavengers are a **market, not an organization**. Cells coalesce around a
den, a buyer and a boss; the boss is whoever is "the most unscrupulous, savage,
and cunning" and can hold the crew together. `[wiki]`

| Name | 2077 role | Character record | Location / influence point | Presence | Source | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| **Tzar** | Dogtown oligarch; host of the Scav table at the Black Sapphire | `Character.q303_paradise_scav_tzar` | Black Sapphire, Dogtown | `story` | Raw `always_loaded_1` registry entry `13_tzar` (phase `spawn`, spot `#q303_ws_paradise_chat_13_scav_tzar`); guest community `{q303_com_paradise_quest_interactions}` | `[game-data]` |
| **Tzar's general** (unnamed) | Soviet-general actor seated with Tzar; the only visible Soviet command link | `Character.q303_paradise_scav_general` | Black Sapphire, Dogtown | `story` | Raw registry entry `13_tzar_general` (appearance `man_average__q303__soviet_general`, spot `#q303_ws_paradise_chat_13_scav_general`) | `[game-data]` `[inferred]` |
| **Boris Ribakov** | Boss of the Organitopia cell; ex-Spetsnaz, SovOil operative | `Character.sts_ep1_08_kgb_boss` (inferred) | Organitopia, Terra Cognita, Dogtown | `world-activity` | Site 360 `sts_ep1_08` (16 units); only boss record at `#sts_ep1_08_boss_ws_001`; *Gig: Spy in the Jungle*; wiki *Boris Ribakov* | `[game-data]` `[wiki]` `[inferred]` |
| **Nika Yankovich** | Leader of the Haven Clinic cell; Gaspar's twin | `Character.sts_ep1_01_nika` | Haven Clinic, Montaña de Oro Ave, Dogtown | `world-activity` | Site 355 `sts_ep1_01` (16 units); raw entry `nika`; *Gig: Dogtown Saints*; wiki *Nika Yankovich* | `[game-data]` `[wiki]` |
| **Slava Makarov** | Dealmaker of the Los Osos cell; buys combat chrome | none | Los Osos motel, West Wind Estate | `mentioned` | Shard *Archived Conversation: Jason Foreman and Slava Makarov* (`sts_ep1_03_shard_009`); *Gig: The Man Who Killed Jason Foreman* | `[wiki]` |
| **Yasha Ivanov** | Los Osos enforcer; the gig's mandatory boss | `Character.sts_ep1_03_miniboss_placeholder` (inferred) | Los Osos motel, West Wind Estate | `world-activity` | Site 356 `sts_ep1_03` (18 units); only `miniboss` slot; shard `sts_ep1_03_shard_022_boss`; gig text names Yasha | `[game-data]` `[wiki]` `[inferred]` |
| **Luka Morozov** | Los Osos coordinator; relays Damir Kovac's orders | none | Los Osos motel | `mentioned` | Shard *Archived Conversation: Yasha Ivanov and Luka Morozov* (`sts_ep1_03_shard_022_boss`) | `[wiki]` |
| **Anton Kolev** | Boss of the Pacific Boulevard / West Wind cell; Wraith partner | none found (generic `gang_leader`) | Pacific Blvd, West Wind Estate | `world-activity` | Site 114 `ma_pac_wwd_04` (4 units); NCPD dispatcher; wiki *Anton Kolev*; shard `ma_pac_wwd_04_onscreen_01` | `[wiki]` `[game-data]` `[inferred]` |
| **Stanislaus Zbyszko** | Captain of the Eden Beach cell; smuggling priors | `Character.ma_pac_cvi_12_outpost_miniboss` (inferred) | Eden Beach Mega Ride, Coastview | `world-activity` | Site 107 `ma_pac_cvi_12` (16 units); only `outpost_miniboss` slot; *SOCA: Wipe the Gonk, Take the Implants*; shard `ma_pac_cvi_12_onscreen_01` | `[game-data]` `[wiki]` `[inferred]` |
| **Yelena Sidorova** | Leader of the Ross Street cell; NCPD commissioner's contractor | `Character.ma_wat_nid_01_outpost_miniboss` (inferred) | Ross Street Parking Facility, Northside | `world-activity` | Site 215 `ma_wat_nid_01` (12 units); only `outpost_miniboss` slot; *SOCA: Vice Control*; computer `get to work` | `[game-data]` `[wiki]` `[inferred]` |
| **Barry Alken** | Leader of the Little China hit squad | `Character.ma_wat_lch_01_outpost_miniboss` (inferred) | Opposites Attract rooftop, Goldsmith & Cortes, Little China | `world-activity` | Site 192 `ma_wat_lch_01` (12 units); only `outpost_miniboss` slot; *SOCA: Opposites Attract*; wiki *Barry Alken* | `[game-data]` `[wiki]` `[inferred]` |
| **Roman** | Leader of the Arroyo cell; Aldecaldo cyberware buyer | `Character.mq002_scavenger_leader` (inferred) | MLK Boulevard & Valley, Arroyo | `world-activity` | Raw registry entry `leader` at `#mq002_ws_scav_lead_deal`; *Gun Music*; wiki *Roman (Cyberpunk 2077)* | `[game-data]` `[wiki]` `[inferred]` |
| **Scavenger Den boss** (unnamed) | Boss of the JapanTown prologue den | `Character.q001_scavenger_boss` | Scavenger Den, Crescent St., JapanTown | `story` | Raw registry entry `boss`; *The Rescue*; *Sweet Dreams* | `[game-data]` `[wiki]` |
| **Kajetan Zilevski** | Downtown hitman; Mordellini's contract killer | `Character.ma_cct_dtn_12_kajetan_zilevsk` | Corpo Plaza / Downtown | `world-activity` | Site 38 `ma_cct_dtn_12`; *Reported Crime: Turn Off the Tap*; shard `ma_cct_dtn_12_onscreen_01` | `[game-data]` `[wiki]` |
| **Damir Kovac** | Ripperdoc; the Terra Cognita network's medical authority | `Character.mq306_damir` | Digimmortal / Los Osos, Dogtown | `world-activity` | Wiki *Damir Kovac*; *No Easy Way Out*; Los Osos shards | `[game-data]` `[wiki]` |

Four facts do the political work here:

1. **No one commands the faction.** The wiki says "no official hierarchy"; the
   database entry says "not a centralized gang" in spirit if not in words, and
   the Dogtown entry only claims an "oligarchy", not a leader. `[wiki]`
2. **The biggest garrison has no name.** The Scraper holds 43 roster units, 20%
   of all 210 Scav units, and no named boss in any source. The only authority
   marker is the keycode-locked armory (2045). `[game-data]` `[wiki]`
3. **The richest cell is a social network, not a command.** Tzar's table at the
   Black Sapphire is where a Scav boss, an unnamed Soviet general and two hired
   Animal bodyguards sit together; the party also hosts the NCPD commissioner
   and a 6th Street officer. That is access, not rank. `[game-data]` `[wiki]`
4. **Every named boss is disposable.** Six of the seven 2077 cell bosses are
   gig or scanner targets; the game's default outcome is that V kills them and
   the cell evaporates. There is no succession office to inherit. `[wiki]`
   `[game-data]`

### 1.2 Succession history: no line, only cell deaths

There is no dated leadership line because there is no faction-wide leadership.
What the sources give is a set of cell tenures and a pattern of violent,
local replacement.

| Period | Centre of power | How the change happened |
| --- | --- | --- |
| pre-2077 | No central leadership; cells form around dens, chop shops and ripper clinics | The wiki describes small groups "led by the most unscrupulous, savage, and cunning individuals"; the business is inherited by whoever can hold the crew. `[wiki]` |
| 2077 (prologue) | **Scavenger Den, JapanTown** | V and Jackie kill the den boss and free Sandra Dorsett (*The Rescue*); Roman later recognises V as "the one who ruined their business in the Scavenger Den". `[wiki]` `[game-data]` |
| 2077 | **Eden Beach cell** | Zbyszko orders Goose killed for "startin' to get too fuckin' smart", then sells the haul to the Soviet Union and blames the Animals. V later kills Zbyszko (*SOCA: Wipe the Gonk*). `[wiki]` |
| 2077 | **Ross Street cell** | Yelena is hired by NCPD commissioner Jerry Fawlter to clear the homeless; V kills her cell (*SOCA: Vice Control*). `[wiki]` `[game-data]` |
| 2077 | **Little China cell** | Barry Alken's hit squad holds a rooftop; V kills them (*SOCA: Opposites Attract*). `[wiki]` `[game-data]` |
| 2077 | **West Wind cell** | Kolev runs the El Dorado pawn shop with Wraith partners; V kills him (*SOCA: West Wind Estate*). `[wiki]` `[game-data]` |
| 2077 | **Organitopia cell** | Boris Ribakov, a SovOil contract killer, hunts Katya Karelina; V kills him (*Spy in the Jungle*). `[wiki]` `[game-data]` |
| 2077 | **Haven Clinic cell** | Nika storms the clinic over her brother's death; V can kill or talk her down (*Dogtown Saints*). `[wiki]` `[game-data]` |
| 2077 | **Los Osos cell** | Slava Makarov's crew protects the fugitive Barghest soldier Leon Rinder for pay; Yasha guards him reluctantly, Luka relays Damir's orders; V kills Yasha and can kill Rinder (*The Man Who Killed Jason Foreman*). `[wiki]` `[game-data]` |
| 2077 | **Dogtown oligarchy / Black Sapphire** | Tzar survives the party; there is no recorded challenge or succession. `[game-data]` |

The pattern is **local and violent**. A cell changes hands when its boss dies;
the survivors either scatter, join the next den, or take the dead boss's buyer
channel. There is no coup, no council, no purge and no inheritance. That is why
the design's "at war with everyone" swarm is the Scavengers' **default** state,
not a failure state.

### 1.3 Rank structure, initiation and advancement

Lore names only **cell leader**, **crew** and **associates**. Everything else is
a combat tier or a job.

1. **Cell leader / boss.** One per den. Commands the crew, owns the buyer
   relationship, and usually holds the loot or the keycode. Examples: Tzar,
   Boris, Nika, Kolev, Zbyszko, Yelena, Barry, Roman, the unnamed Scraper and
   Den bosses. `[wiki]` `[game-data]`
2. **Crew.** The game's records use role tiers — `grunt1/2/3`, `elite2/3`,
   `strong3`, `fast3`, `butcher3`, `netrunner2`, `sniper`, `gunner` — plus
   gangster archetypes (`Crow`, `Hooligan`, `Rat`, `Hound`, `Spider`, `Cur`).
   These describe combat role, not authority. `[game-data]`
3. **Ripperdoc / med-tech.** A technical asset with real leverage. Damir Kovac
   is a member and the network's medical authority; Fingers and Charles Bucks
   are outside ripperdocs who buy or supply. `[wiki]`
4. **Associates and clients.** Fixers, smugglers, bodyguards, corrupt NCPD
   officers, corporate intermediaries and gangs that buy chrome. They are not
   members and cannot be ordered. `[wiki]` `[game-data]`

**Initiation and advancement.** There is no ceremony, no chrome requirement and
no oath:

- Entry is by usefulness: bring a victim, a haul, a vehicle or a buyer. The
  wiki's formula is "as long as there is money on the table, a Scav will take
  the job no questions asked". `[wiki]`
- Advancement is by **taking a den**, not by promotion. The boss is the person
  the crew will follow to the next score; when the boss dies, the crew follows
  whoever holds the loot. `[wiki]` `[inferred]`
- Exit is death or desertion. Paco Torres, a Barghest deserter, can join the
  Scavengers after *Balls to the Wall*; Zbyszko kills his own courier Goose for
  getting "too smart". `[wiki]`
- The body is the uniform: tracksuits, Soviet cyberware and criminal tattoos
  identify the trade; there is no faction-wide insignia beyond the look.
  `[wiki]`

The practical consequence: the Scavengers have a **den ladder**, not a career
ladder. A player rises by bringing value to a cell and then taking it, not by
earning favour in an office.

### 1.4 Named members mapped to game data

The table above covers the bosses. This one covers the named crew, the
shard-only figures and the associates who matter politically.

| Name | Role / note | Character record | Community / site | Location | Presence | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| **Tzar** | Dogtown oligarch; Black Sapphire host | `Character.q303_paradise_scav_tzar` | `13_tzar` guest entry | Black Sapphire | `story` | `[game-data]` |
| **Tzar's general** | Unnamed Soviet-general actor at Tzar's table | `Character.q303_paradise_scav_general` | `13_tzar_general` guest entry | Black Sapphire | `story` | `[game-data]` `[inferred]` |
| **Boris Ribakov** | Organitopia boss; SovOil contract killer | `Character.sts_ep1_08_kgb_boss` (inferred) | Site 360 `sts_ep1_08` | Organitopia | `world-activity` | `[game-data]` `[wiki]` `[inferred]` |
| **Nika Yankovich** | Haven Clinic leader; Gaspar's twin | `Character.sts_ep1_01_nika` | Site 355 `sts_ep1_01` | Haven Clinic | `world-activity` | `[game-data]` `[wiki]` |
| **Gaspar Yankovich** | Nika's brother; overdosed at Haven Clinic | none | — | Haven Clinic | `mentioned` | `[wiki]` |
| **Damir Kovac** | Ripperdoc; works for the scavs and sometimes the Animals | `Character.mq306_damir` | `mq306` quest community | Digimmortal / Los Osos | `world-activity` | `[game-data]` `[wiki]` |
| **Slava Makarov** | Los Osos dealmaker; buys Militech-grade chrome | none | `sts_ep1_03` shard | Los Osos | `mentioned` | `[wiki]` |
| **Yasha Ivanov** | Los Osos boss; guards Rinder for money | `Character.sts_ep1_03_miniboss_placeholder` (inferred) | Site 356 `sts_ep1_03` | Los Osos | `world-activity` | `[game-data]` `[wiki]` `[inferred]` |
| **Luka Morozov** | Los Osos coordinator; relays Damir's orders | none | shard | Los Osos | `mentioned` | `[wiki]` |
| **Samuil Egorov** | Los Osos member; runs a patient for Damir | none | shard `sts_ep1_03_shard_011_tranporting_rinder` | Los Osos | `mentioned` | `[wiki]` |
| **Darya Alexeeva** | Los Osos member; Zetatech gear user | none | same shard | Los Osos | `mentioned` | `[wiki]` |
| **Gennady Korolev** | Los Osos member; tests the amnesia drug batch | none | shard `sts_ep1_03_shard_018_drugs` | Los Osos | `mentioned` | `[wiki]` |
| **Kirill Osipov** | Los Osos member; drug test | none | same shard | Los Osos | `mentioned` | `[wiki]` |
| **Anton Kolev** | West Wind boss; Wraith collaborator | none found | Site 114 `ma_pac_wwd_04` | Pacific Blvd | `world-activity` | `[wiki]` `[game-data]` `[inferred]` |
| **Jonah Harper** | Kolev's partner; joint response to the Arasaka container | none | shard `ma_pac_wwd_04_onscreen_01` | West Wind | `mentioned` | `[wiki]` |
| **Stanislaus Zbyszko** | Eden Beach captain; exports to the Soviet Union | `Character.ma_pac_cvi_12_outpost_miniboss` (inferred) | Site 107 `ma_pac_cvi_12` | Eden Beach | `world-activity` | `[game-data]` `[wiki]` `[inferred]` |
| **Sedy "Goose"** | Scav courier killed on Zbyszko's orders | none | shard `ma_pac_cvi_12_onscreen_01` | Eden Beach | `mentioned` | `[wiki]` |
| **Yelena Sidorova** | Ross Street leader; NCPD contractor | `Character.ma_wat_nid_01_outpost_miniboss` (inferred) | Site 215 `ma_wat_nid_01` | Ross Street | `world-activity` | `[game-data]` `[wiki]` `[inferred]` |
| **Barry Alken** | Little China hit-squad leader | `Character.ma_wat_lch_01_outpost_miniboss` (inferred) | Site 192 `ma_wat_lch_01` | Little China | `world-activity` | `[game-data]` `[wiki]` `[inferred]` |
| **Roman** | Arroyo leader; Aldecaldo buyer | `Character.mq002_scavenger_leader` (inferred) | `mq002` | Arroyo | `world-activity` | `[game-data]` `[wiki]` `[inferred]` |
| **Scavenger Den boss** | Unnamed prologue boss | `Character.q001_scavenger_boss` | `q001` | Scavenger Den | `story` | `[game-data]` `[wiki]` |
| **Kajetan Zilevski** | Downtown hitman; Mordellini's client | `Character.ma_cct_dtn_12_kajetan_zilevsk` | Site 38 `ma_cct_dtn_12` | Corpo Plaza | `world-activity` | `[game-data]` `[wiki]` |
| **Misha Orlova** | Wild Blue crew; witness to Ellen Verde | `Character.ma_pac_cvi_09_scavenger_fast3_fmelee3_machete_wa_elite_Misha_Orlova` | Site 97 `ma_pac_cvi_09` | Wild Blue, Coastview | `world-activity` | `[game-data]` `[wiki]` |
| **Michal Glowinski** | Coastview netrunner | `Character.ma_pac_cvi_07_scavenger_grunt3_netrunner2_nova_ma_rare_Michal_Glowinski` | Site 95 `ma_pac_cvi_07` | Coastview | `world-activity` | `[game-data]` |
| **Alan Crank** | Northside docks crew; hunts a Tyger container | `Character.ma_wat_nid_12_shard_scav` (inferred) | Site 225 `ma_wat_nid_12` | Northside Docks | `world-activity` | `[game-data]` `[wiki]` `[inferred]` |
| **Stefan** | BD dealer who lures V to the den | `Character.mq036_stefan` | `mq036` | Cherry Blossom Market | `world-activity` | `[game-data]` `[wiki]` |

Data cautions:

- **The boss records are deductions, not names.** `ma_pac_cvi_12_outpost_miniboss`,
  `ma_wat_nid_01_outpost_miniboss` and `ma_wat_lch_01_outpost_miniboss` are the
  single miniboss slots at sites whose wiki pages name Zbyszko, Yelena and
  Barry; `sts_ep1_03_miniboss_placeholder` is the only boss slot at Los Osos,
  whose gig names Yasha. Tagged `[inferred]`; verify in game. `[game-data]`
  `[wiki]`
- **Boris's record is `kgb_boss`, not `ribakov`.** The gig's only boss record has
  appearance `man_average__sts_ep1_08__fiodor` and spawns holographic decoys;
  the wiki names the boss Boris Ribakov. The mapping is by elimination and
  appearance, tagged `[inferred]`. `[game-data]` `[wiki]`
- **Kolev has no named record.** Site 114 holds four generic melee scavs and the
  registry has a generic `gang_leader` entry; the identity comes from the NCPD
  dispatcher and the wiki. Do not seed a `kolev` record until one is found.
  `[game-data]` `[wiki]`
- **Slava, Luka, Samuil, Darya, Gennady and Kirill exist only in shards.** They
  are the best evidence that a cell has an internal division of labour, but
  they do not spawn. `[wiki]`
- **Tzar has no wiki page.** The name, faction and party placement are
  game-data only; the "oligarch" label is the wiki's descriptor for the Dogtown
  wing, not a title Tzar is given in game. `[game-data]` `[wiki]` `[inferred]`
- **Damir is a shared asset.** The Scavengers Members page lists him as a
  Scavenger ripperdoc; the Animals politics doc calls him "the Animals'
  ripperdoc". The wiki database entry resolves it: he works for the scavs in
  Terra Cognita and "sometimes takes jobs from Animals". He is a Scavenger
  affiliate, not an Animal officer. `[wiki]`

### 1.5 What the game actually spawns (campaign disabled)

**`story` — gated by the main/side job chain; do not expect them in free roam
with the campaign disabled.**
- **Tzar** and his general at the Black Sapphire (*You Know My Name*).
- **The Scavenger Den boss** in the prologue den (*The Rescue* / *Sweet
  Dreams*).

**`world-activity` — free-roam content, activity-gated.**
- **Boris Ribakov** (*Spy in the Jungle*).
- **Nika Yankovich** (*Dogtown Saints*).
- **Yasha Ivanov** and the Los Osos crew (*The Man Who Killed Jason Foreman*).
- **Anton Kolev** (*SOCA: West Wind Estate*).
- **Stanislaus Zbyszko** (*SOCA: Wipe the Gonk, Take the Implants*).
- **Yelena Sidorova** (*SOCA: Vice Control*).
- **Barry Alken** (*SOCA: Opposites Attract*).
- **Roman** (*Gun Music*).
- **Kajetan Zilevski** (*Reported Crime: Turn Off the Tap*).
- **Misha Orlova** (Assault in Progress, Wild Blue).
- **Michal Glowinski** (scanner activity, Coastview).
- **Alan Crank** (*Reported Crime: Needle in a Haystack*).
- **Damir Kovac** (*No Easy Way Out*).

**`mentioned` — named only in shards, computers or dialogue.**
- **Slava Makarov, Luka Morozov, Samuil Egorov, Darya Alexeeva, Gennady
  Korolev, Kirill Osipov, Sedy "Goose", Gaspar Yankovich, Jonah Harper.**

**`ambient` — none.** No named Scavenger persists in free roam without an
activity. Generic scav crews do spawn across the map, but every named figure is
quest- or scanner-gated. The mod must spawn the cast itself. `[game-data]`

Caveat: "campaign disabled" may also suppress gigs and scanner hustles. The
`world-activity` rows are the best reuse candidates; the `story` and `mentioned`
rows are the ones to replace with simulation agents.

### 1.6 Player-path hooks

| Person | Join under | Climb past | Ally with | Remove |
| --- | --- | --- | --- | --- |
| **Tzar** | The Dogtown oligarchy: money, chrome, the Black Sapphire guest list | He is the social hub, not a commander; climbing past him means taking the party's business, not his rank | Animal bodyguards, the unnamed Soviet general, corrupt NCPD guests, Barghest tolerance | Killing him decapitates the oligarchy's social hub but not the cells; the party network scatters |
| **Boris Ribakov** | The Organitopia cell: mercenary work, SovOil contracts | He is the boss; a player under him climbs by taking the SovOil account | SovOil (external), the Organitopia garrison | Killing him frees Katya Karelina and ends the SovOil contract in Dogtown |
| **Nika Yankovich** | The Haven Clinic cell: family loyalty, ripper access | She leads through family, not rank; climbing past her means taking the clinic's client list | Damir Kovac, the clinic's ripperdoc network | Killing or talking her down ends the clinic occupation; Gaspar's death is the lever |
| **Yelena Sidorova** | The Ross Street cell: NCPD contract work, clearing the homeless | She is the boss and the commissioner's contact; a player climbs by becoming the new contact | Jerry Fawlter (NCPD commissioner), the Northside development project | Removing her cuts the corrupt NCPD channel and the cell's protection |
| **Anton Kolev** | The West Wind cell: chrome dealing, Wraith partnership | He is the boss; a player climbs by taking the Wraith and Aldecaldo buyer relationships | Wraiths, Jonah Harper, Aldecaldo buyers | Removing him breaks the Wraith link and the Arasaka-container operation |
| **Stanislaus Zbyszko** | The Eden Beach cell: smuggling, Soviet export | He is the captain; a player climbs by controlling the export channel | Soviet buyers (external), the Eden Beach crew | Removing him stops the Tyger frame-up and the Soviet implant pipeline |
| **Roman** | The Arroyo cell: Aldecaldo cyberware purchases | He is the leader; a player climbs by becoming the Aldecaldos' preferred buyer | Aldecaldos (Cassidy, Carol, Teddy), Arroyo industrial buyers | Removing him ends the Aldecaldo sales channel, not the faction |
| **The Scavenger Den boss** | The JapanTown den: the prologue cell | No ladder; the boss is the den | Wakako Okada's contract, the den's buyers | Killing him takes the den — the cleanest "take a Scav point" path in the design |
| **Damir Kovac** | The ripper network: medical work, implant sourcing | He is an asset, not a boss; a player climbs by becoming his protector or his supplier | Scav cells, Animals, Los Osos patients | Removing him hurts every cell that relies on his clinic, but decapitates none |
| **Any cell** | Bring a victim, a haul or a buyer | Take the den when the boss dies | The cell's existing buyer | Killing the boss leaves the cell to whoever holds the loot |

The design consequence: the Scavengers have **no single ladder and no faction
seat**, only a den ladder and a set of buyer relationships. Backing one cell
makes the others neutral at best; killing one boss takes one den and leaves the
rest untouched. This is the purest "rebel/pirate swarm" path in the game and
should not be flattened into a normal gang hierarchy.

---

## 2. Internal political factions

### 2.1 The blocs

"Members" counts are **presence proxies** from `dist/extract/areas.jsonl` and
site rosters, not membership rolls. Several communities are overlapping quest
phases of one site, so do not sum them.

| Bloc | Leader(s) | What it wants | Presence / members hint | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- |
| **Dogtown oligarchy** | Tzar; Boris, Nika and Damir as the other named Dogtown powers | Money, chrome, Soviet contacts, Barghest's tolerance; keep the Black Sapphire table | Dogtown: 34 areas / 240 entries; four named venues; Scraper 43 units, Organitopia 16, Digimmortal 37 entries, ESC Explorer 29 entries | Wiki "Scavs in Dogtown" database entry; Tzar registry; `q303` party | `[game-data]` `[wiki]` |
| **The Scraper mass (Longshore Stacks)** | No named boss; the armory keycode is the only authority marker | Hold the largest squat, sell the Zetatech prototype, keep the prison/lift/armory | Site 357, 43 units, 5 communities, 9 doors | *Gig: Prototype in the Scraper*; site 357 | `[game-data]` `[wiki]` |
| **Los Osos / West Wind network** | Slava Makarov (deals), Yasha Ivanov (muscle), Luka Morozov (coordination), Kolev (West Wind) | Buy Militech-grade chrome, protect paying clients, move the amnesia drug batch, keep the Wraith partnership | Los Osos 18 units; Kolev site 4 units; Wraiths present at Kolev's base | *The Man Who Killed Jason Foreman*; shards; *SOCA: West Wind Estate* | `[game-data]` `[wiki]` |
| **Eden Beach smuggling cell** | Stanislaus Zbyszko | Export implants to the Soviet Union; keep the Tyger Claws fooled; avoid NCPD | Site 107, 16 units, 5 guard volumes, 31 spots, 9 patrols | *SOCA: Wipe the Gonk*; shard `ma_pac_cvi_12_onscreen_01`; `today's hunt` | `[game-data]` `[wiki]` |
| **Night City street cells** | Yelena (Ross St), Barry (Little China), Roman (Arroyo), the Den boss (JapanTown), Kajetan (Downtown), Alan Crank (Northside) | Survive, sell to fixers and ripperdocs, take paid work | Ross St 12, Opposites 12, Scavenger Den 27 entries, Kajetan site 38, Roman `mq002` | *SOCA: Vice Control*, *Opposites Attract*, *Gun Music*, *The Rescue*, *Turn Off the Tap*, *Needle in a Haystack* | `[game-data]` `[wiki]` |
| **The ripperdoc network** | Damir Kovac; outside ripperdocs Fingers and Charles Bucks | Supply chrome, keep clients quiet, profit from both scavs and Animals | Damir at Digimmortal/Los Osos; Fingers in Japantown; Charles Bucks next to the Eisenhower den | Wiki *Damir Kovac*; *No Easy Way Out*; *Disasterpiece*; *Last Login* | `[wiki]` `[game-data]` |
| **The mercenary contract wing** | Yelena (NCPD), Kajetan (Mordellini), Tzar (Animal bodyguards), Kolev (Wraiths) | Sell violence "no questions asked"; keep the client | Yelena's NCPD contract; Kajetan's hit; Tzar's two Animal guards; Kolev's Wraith partners | *Vice Control*; *Turn Off the Tap*; `q303` registry; *SOCA: West Wind Estate* | `[game-data]` `[wiki]` |
| **The Soviet-linked current vs the NC rabble** | No leader; Tzar's general is the only visible symbol | Discipline, equipment, business vs survival, improvisation and predation | Dogtown's better gear; Zbyszko's Soviet export; Boris's SovOil background; the wiki's explicit disdain for "poorer NC kind" | Wiki *Scavs in Dogtown*; *Spy in the Jungle*; `ma_pac_cvi_12` shard | `[wiki]` `[game-data]` |
| **Smugglers vs harvesters** | No leader | Arms/contraband logistics vs organ and chrome harvesting | ESC Explorer (arms/smuggling), Eden Beach (smuggling), Scraper armory vs the ripper dens | Wiki *ESC Explorer*; *SOCA: Wipe the Gonk*; *Prototype in the Scraper* | `[wiki]` `[game-data]` |

### 2.2 No boss of bosses

This is the structural fact that separates the Scavengers from every other gang
in this series.

- There is no headquarters: the infobox leaves `headquarters` and
  `faction_locations` blank, and `data/faction_headquarters.json` has no fid-7
  row. `[wiki]` `[game-data]`
- There is no leader rank above cell boss: the wiki says "no official
  hierarchy", "small bands with little or no internal hierarchy", and only
  "groups tend to be led by the most unscrupulous, savage, and cunning
  individuals". `[wiki]`
- There is no shared community hash across the four Dogtown venues; the location
  doc checked and found none. The Dogtown "oligarchy" is a cluster, not a
  command post. `[game-data]`
- Tzar is the closest thing to a public face, and he is a **host**, not a
  commander: his table has two hired Animal bodyguards and an unnamed Soviet
  general, but no Scav staff officers. `[game-data]`

For the simulation this is an asset, not a gap. The design already has a state
for "a faction in internal war with no single leader". The Scavengers should
start in that state permanently: no claimant to a faction-wide seat, no rule
that says who commands when cells disagree, and no capital to capture. Any
attempt to give them a boss invents a rank the lore does not have.

### 2.3 Dogtown oligarchy vs Night City rabble

The cleanest policy axis inside the faction is **Dogtown business vs Night City
predation**. The wiki draws it explicitly:

- Dogtown scavs are "much better organized and equipped than their Night City
  brethren"; they have "cash, good equipment and a bit of disdain for their
  poorer NC kind". `[wiki]`
- "Only those without a knack for business end up in Night City"; the "scav
  oligarchy secures business in Hansen's backyard", and Hansen tolerates them
  because "it's all about the money". `[wiki]`
- Night City cells are the ones V meets in the prologue, Kabuki, Northside,
  Little China and Arroyo: smaller, poorer, more likely to be a scanner hustle.
  `[game-data]` `[wiki]`

This is not a civil war; it is a class split inside a market. A Dogtown boss
looks at an NC crew as cheap labor or a liability; an NC crew looks at Dogtown
as the place where the money and the Soviet chrome are. A simulation can model
it as a **prestige and price gradient**, not as two factions.

### 2.4 The ripperdoc network and medical authority

The Scavengers' product is chrome and organs, so the ripperdoc is the most
important non-boss role in the faction.

- **Damir Kovac** is the network's medical authority. He works for the scavs in
  Terra Cognita, sometimes takes Animal jobs, and gives orders that reach Los
  Osos through Luka Morozov. Yasha resents it — "he can stick his orders up his
  ass" — but takes the money. `[wiki]`
- **Fingers** is the Japantown ripperdoc who sold Evelyn Parker to the scavs;
  the Mox's politics doc records the sale and the scav XBD studio that follows.
  `[wiki]`
- **Charles Bucks** runs the clinic directly above the Eisenhower Street chop
  den; the gig's back stairs lead from the scav basement into his clinic, and he
  pleads for his life when V emerges. `[wiki]` `[game-data]`
- **Anthony Anderson** is the Haven Clinic ripperdoc Nika threatens; he is a
  victim of the cell, not a member. `[wiki]`

The political consequence: **medical authority is separate from cell
authority**. Damir can direct a cell's patient work without being its boss;
killing a cell boss does not remove the ripperdoc, and killing the ripperdoc
hurts every cell that uses him.

### 2.5 The Soviet current

Three separate details point the same way, and none of them proves a formal
organization:

1. **Zbyszko's export.** "The whole haul's going to the Soviet Motherland"; the
   Eden Beach cell strips chrome for export. `[wiki]`
2. **Boris Ribakov.** A former Spetsnaz special-forces agent and SovOil
   operative, contracted by SovOil to assassinate Katya Karelina. `[wiki]`
3. **Tzar's table.** The Black Sapphire guest community places Tzar with a
   `soviet_general` appearance actor and two Animal bodyguards. `[game-data]`

The wiki's Dogtown database entry says the scavs there are "linked to Soviet
intelligence" and that "whoever is spreading these rumors runs the risk of
getting their picture stapled to the Memorial Tree in the Stacks". Treat this
as a **rumor with three corroborating details**, not as a chain of command. Do
not invent a Soviet faction or a Soviet rank; model it as an external buyer and
a prestige network.

### 2.6 The smuggling and export wing

The scav economy is not only organs. Two Dogtown/Coastview venues are explicitly
smuggling bases:

- **ESC Explorer** — "a base for their weapons smuggling operations"; 29
  entries across two communities. `[wiki]` `[game-data]`
- **Eden Beach Mega Ride** — Zbyszko is "a known captain amongst scavengers with
  multiple smuggling priors"; the cell strips chrome and ships it to the Soviet
  Union. `[wiki]` `[game-data]`
- **The Scraper armory** — keycode 2045, plus the Zetatech prototype; the
  largest garrison is also an arms cache. `[wiki]` `[game-data]`
- **Los Osos** — the amnesia drug batch "before it goes to NC" and the Militech
  chrome purchase show a contraband pipeline that is not just chrome. `[wiki]`

This wing is the faction's **growth** sector: it has buyers, routes and capital,
and it is the part most likely to collide with Barghest, the Tyger Claws and
Arasaka.

### 2.7 The mercenary contract wing

The wiki's business model is explicit: scavs are "frequently hired to perform
unpleasant or inconvenient tasks … heists, hit jobs, and abductions … no
questions asked". Four attested contracts show how far that reaches:

- **NCPD commissioner Jerry Fawlter → Yelena Sidorova**: clear the homeless out
  of the Ross Street Parking Facility; the commissioner promises that calls
  from the area "will be ignored". `[wiki]`
- **Bartolomeo Mordellini → Kajetan Zilevski**: kill Sandra Faucet over a debt;
  "body should be message enough". `[wiki]`
- **Tzar → Animal bodyguards**: two `Character.q303_paradise_animal_guard`
  flank him at the Black Sapphire. `[game-data]`
- **Kolev ↔ Wraiths**: shared base at the former El Dorado pawn shop and a
  joint security response to the Arasaka container. `[wiki]`

The contract wing is the faction's **political interface**: it is how scavs
touch the NCPD, the fixers, the corps and the other gangs without having a
diplomatic service.

### 2.8 What could drive internal conflict in a simulation

Evidence-based drivers, in rough order of plausibility:

1. **No boss of bosses.** Any cell can claim primacy; no rule says who wins.
   Taking a den is the only legitimate claim, and it is local.
2. **Dogtown vs Night City.** The explicit disdain for the "poorer NC kind"
   makes a rich Dogtown cell and a poor Kabuki cell natural rivals over buyers,
   chrome and prestige.
3. **Medical authority vs cell authority.** Damir gives orders that a cell boss
   resents; a boss who refuses them loses the ripper, and a boss who accepts
   them looks weak.
4. **Money vs loyalty.** Yasha guards Leon Rinder only because "he's paying for
   protection"; the same calculation can flip a crew.
5. **Disposal of liabilities.** Zbyszko kills Goose for getting "too smart";
   every ambitious member is a potential liability, and every boss knows it.
6. **The Barghest arrangement vs predation.** The Dogtown oligarchy lives on
   Hansen's tolerance, while other cells steal airdrops and ambush convoys. A
   cell that pushes too hard risks the whole Dogtown business.
7. **Buyer competition.** The same fixers, ripperdocs and gangs buy from several
   cells; a cell that loses a buyer blames the boss who lost it.
8. **Soviet-linked discipline vs street rabble.** The Dogtown wing's equipment
   and contacts versus the NC crews' improvisation is a status conflict, not an
   ideological one.
9. **Harvest vs smuggling.** The chrome dens and the arms/contraband crews want
   different buyers, different risks and different protection.
10. **Frame-ups and misinformation.** Zbyszko's cover story blames the Animals
    for Goose's death; a lie that works is a tool every cell can use.

---

## 3. External relations matrix

### 3.1 Stance vocabulary

One stance per row, chosen by the precedence in `METHOD.md` §3: explicit
violence first, then explicit transaction, then quest-giver role, then
adjacency, then a neutral placeholder.

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
and `Affiliation.hpp` is identity only (the Scavengers' `faction_id` is **7** and
their `affiliation_enum` is `Scavengers`; the enum value is not the join key).
Every stance below is judged from quests, shards, wiki and spatial adjacency,
which is why each row carries a tag and why the neutral rows are placeholders,
not claims of friendship.

**The design premise is not the lore.** `docs/design/gameplay-systems.md` makes
the Scavs the "rebel/pirate" swarm faction, "constantly at war with everyone",
holding every neutral or abandoned point. That is a system rule. The matrix
below records what the 2.5 + PL sources actually show: predation, paid
tolerance, a few real trades and a lot of uncontacted markets. Where the design
overrides lore, §5 says so.

### 3.2 The matrix

| Faction | Code | Stance | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| Tyger Claws | `tyger_claws` | `hostile` | Zbyszko's cell kills the courier Goose, who was carrying high-tech implants "from the Tygers", then orders the crew to blame the Animals; *Reported Crime: Lost and Found* is a scav-vs-Tyger alley scrap in Japantown; *Needle in a Haystack* is scavs hunting a container marked with Tyger graffiti; the Kabuki and Allen St. dens sit inside Tyger turf. The trafficking channel runs the other way: Jae-Hyun delivers kidnapped victims to the scavs and they end up with a Tyger like Jotaro Shobo. Hostile with a victim-trade channel | `game-data+wiki` |
| Valentinos | `valentinos` | `neutral` | No reliable incident. The Valentinos doc's `rival` row rests on `{sa_ep1_135_com_combat}`, a Phantom Liberty courier-loop combat pool (4 Scavs, 4 6th Street, 4 Valentinos, 1 Arasaka), which METHOD §1.3 item 3 says to exclude. Both work the chrome and sex economy in different districts; no attested deal or fight | `game-data+inferred` |
| Arasaka | `arasaka` | `rival` | Kolev's cell moves on a container from an Arasaka aircraft that landed on the West Wind beach, and his implant list includes an Arasaka Yonaguni Xc; the Scraper holds a stolen Zetatech prototype, not Arasaka property. No campaign, no deal — opportunistic predation on Arasaka salvage. The Arasaka doc records neutral | `wiki+game-data+inferred` |
| Militech | `militech` | `trade` | The Los Osos cell buys "militech 3rd gen" combat implants from Jason Foreman's supplier; Kolev's implant list includes Militech Kairos 6-M and Svalinn 9-F; the buyer is a black-market intermediary, not Militech procurement. Trade in stolen/off-book chrome, no corporate sanction. The Militech doc records neutral | `wiki+game-data` |
| Kang Tao | `kang_tao` | `neutral` | No attested interaction. Fenghuang `Hu shén-II` appears on Kolev's implant list, a black-market brand, not a relationship | `game-data+inferred` |
| Biotechnica | `biotechnica` | `neutral` | No attested interaction. Boris's pelmeni recipe uses a Biotechnica protein brick, a consumer purchase, not a political channel | `wiki+inferred` |
| Petrochem | `petrochem` | `neutral` | No attested interaction. The same recipe uses Petrochem synth-flour; the EBM Petrochem Stadium is a Dogtown landmark, not a scav patron | `wiki+inferred` |
| Barghest | `barghest` | `rival` | "In business with BARGHEST as frequently as they clash"; the Dogtown scav oligarchy "secures business in Hansen's backyard … It's all about the money"; scavs steal airdrops and ambush Paco Torres's convoy in *Balls to the Wall*, and Paco can later join them. Paid tolerance plus predation, not an alliance | `game-data+wiki` |
| 6th Street | `sixth_street` | `neutral` | No reliable incident. The 6th Street doc's `rival` row also rests on `{sa_ep1_135_com_combat}`, the PL courier-loop pool excluded by METHOD §1.3 item 3. The Gun Music site is in Arroyo but the counterparties are Aldecaldos, not 6th Street | `game-data+inferred` |
| Aldecaldos | `aldecaldos` | `trade` | *Gun Music*: Cassidy, Carol and Teddy deliver cyberware to Roman's crew in Arroyo; Roman complains the delivery is three days late and haggles the cut, and the deal nearly becomes a firefight. Kolev also sources a Kiroshi XtremSight 4553 for the Aldecaldo Jason Wildriver. The Aldecaldos doc records the same trade | `game-data+wiki` |
| Wraiths | `wraiths` | `trade` | Kolev "collaborates with the Wraiths" at the former El Dorado pawn shop on Pacific Boulevard; Wraiths members are present at his base, and Kolev and Jonah Harper "immediately agreed to send security personnel" to the Arasaka container. A cell-level operational partnership, not a faction treaty — the closest stance is trade | `wiki+game-data` |
| Animals | `animals` | `trade` | Two `Character.q303_paradise_animal_guard` flank Tzar at the Black Sapphire — a paid muscle contract; Damir Kovac works for the scavs and "sometimes takes jobs from Animals"; Zbyszko's frame-up blames the Animals for Goose's death, which is propaganda, not a war. The Animals doc records the same trade | `game-data+wiki` |
| The Mox | `the_mox` | `hostile` | Fingers sold Evelyn Parker to the scavs; they held her in the XBD studio at the abandoned power plant and tortured her; Judy and V raid it and kill the crew (*Disasterpiece*, *Double Life*). The Mox's protection mandate is anti-Scav. The Mox doc records hostile | `game-data+wiki` |
| Maelstrom | `maelstrom` | `rival` | Compete for the same chrome and salvage; *Reported Crime: Paranoia* places scavs and optional Maelstrom at the same Little China scene; Maelstrom's own doc records rival. No attested deal or full war | `game-data+wiki` |
| Voodoo Boys | `voodoo_boys` | `hostile` | Placide orders Fara Dupont to surround and kill scavs who raided a NetWatch stash; four VDB members (Fara Dupont, Diesuel, Josue, Lovelie) were killed by scavs; both operate in Pacifica, West Wind and Terra Cognita. The VDB doc records hostile | `game-data+wiki` |
| NCPD | `ncpd` | `hostile` | Standing target: NCPD APBs name Zbyszko, Kolev, Yelena and Barry; scanner hustles and reported crimes at Ross Street, Opposites Attract, Eden Beach, West Wind, Northside and Coastview. Yet commissioner Jerry Fawlter hires Yelena to clear the homeless and promises to ignore calls from the area — hostile with a corrupt channel | `game-data+wiki` |
| Night Corp | `night_corp` | `neutral` | No attested interaction; a corp, not a turf actor | `inferred` |
| City Council | `city_council` | `neutral` | No attested interaction. The Northside clearance is an NCPD commissioner's project, not a Council vote; no purchased channel found | `inferred` |
| Regina Jones | `fixer_regina` | `hostile` | Regina gives *Last Login* (Eisenhower St. den) and *Small Man, Big Evil* (Allen St. rooftop processing site); both send V to kill or displace scavs | `game-data+wiki` |
| Wakako Okada | `fixer_wakako` | `hostile` | Wakako gives *The Rescue*, the prologue raid on the Scavenger Den; she is also the fixer V asks about the XBD trade that leads to the power-plant scav studio in *Disasterpiece* | `game-data+wiki` |
| Sebastian Ibarra (Padre) | `fixer_padre` | `neutral` | No Scav-specific gig or lore link found | `inferred` |
| Muamar Reyes (El Capitán) | `fixer_el_capitan` | `neutral` | No Scav-specific gig or lore link found | `inferred` |
| Dakota Smith | `fixer_dakota` | `neutral` | No Scav-specific gig or lore link found | `inferred` |
| Dino Dinovic | `fixer_dino` | `neutral` | No Scav-specific gig or lore link found | `inferred` |
| Rogue Amendiares | `fixer_rogue` | `neutral` | No Scav-specific gig or lore link found | `inferred` |
| Mr. Hands | `fixer_mr_hands` | `hostile` | Mr. Hands gives four Dogtown gigs aimed at scav cells: *Prototype in the Scraper*, *The Man Who Killed Jason Foreman*, *Spy in the Jungle* and *Dogtown Saints* | `game-data+wiki` |
| Afterlife | `afterlife` | `neutral` | Neutral merc marketplace; no Scav doorman or contract attested | `inferred` |
| NetWatch | `netwatch` | `hostile` | Scavs raided a NetWatch stash in Pacifica; the VDB retaliation is recorded in the Voodoo Boys doc. No NetWatch counter-operation beyond that raid is attested | `wiki+inferred` |
| NUSA | `nusa` | `neutral` | No direct NUSA–Scav interaction. The Dogtown Soviet-intelligence rumor is not a NUSA relationship; the FIA's Dogtown file does not name the scavs | `inferred` |
| Zetatech | `zetatech` | `rival` | The Scraper garrison holds a stolen Zetatech prototype implant; Hasan Demir, a former Zetatech techie, had it in his eye; Los Osos patient files describe knockoff Zetatech implants; Darya Alexeeva uses Zetatech gear. Corporate IP theft, no contract | `game-data+wiki` |
| Trauma Team | `trauma_team` | `hostile` | Barry Alken's rooftop crew is looting a Trauma Team container while a Trauma Team AV flies away (*SOCA: Opposites Attract*); the E3 2018 trailer shows scavs fighting Trauma Team. Scavs are the reason Trauma Team exists in the fiction — they strip patients before pickup | `game-data+wiki+inferred` |

### 3.3 Actors outside `data/factions.json`

Real relationships with no faction code, so prose only:

- **SovOil** — Boris Ribakov is a former Spetsnaz agent and SovOil operative,
  contracted by SovOil to assassinate Katya Karelina. `[wiki]` No `sovoil` code
  in `data/factions.json`; do not invent one.
- **The Soviet Union / Soviet intelligence** — Zbyszko exports implants to the
  "Soviet Motherland"; the Dogtown database entry says the local scavs are
  rumored to be linked to Soviet intelligence; Tzar's table includes a
  `soviet_general` actor. Treat as an external buyer and a rumor, not a state
  actor with a faction row. `[wiki]` `[game-data]`
- **Jerry Fawlter** — NCPD commissioner; hires Yelena to clear the homeless and
  suppresses police response. The single most important corrupt channel in the
  faction's politics. `[wiki]`
- **Bartolomeo Mordellini** — illicit entertainer and BD producer; hires
  Kajetan Zilevski to kill Sandra Faucet over a debt. A client of scav violence,
  not a member. `[wiki]`
- **Fingers** — Japantown ripperdoc who sold Evelyn Parker to the scavs; the
  supply link between the sex trade and the XBD studio. `[wiki]`
- **Charles Bucks** — ripperdoc whose clinic sits above the Eisenhower Street
  chop den; he pleads with V, offers a discount, and may flee. A compromised
  neighbor, not a member. `[wiki]`
- **Anthony Anderson / Odell Blanco** — Haven Clinic ripperdoc and the
  go-between who calls Mr. Hands; Nika's cell occupies the clinic, they do not
  own it. `[wiki]`
- **Jae-Hyun Lee** — kidnapper who delivers victims to the scavs; his victims
  end up as property of a Tyger like Jotaro Shobo. A supplier of people, not a
  Scav. `[wiki]`
- **Jotaro Shobo** — Tyger Claws boss and XBD producer; the buyer at the end of
  Jae-Hyun's trafficking chain. The scav–Tyger relationship is hostile on turf
  and commercial at the victim-trade layer. `[wiki]`
- **Jason Foreman** — intermediary between a top-tier Militech chrome supplier
  and the Los Osos scavs; killed before the gig starts. His shard is the
  faction's clearest Militech trade evidence. `[wiki]`
- **Leon Rinder** — Barghest soldier and deserter hiding at Los Osos; the scavs
  protect him for money, and Yasha resents the babysitting. A client, not a
  member. `[wiki]`
- **Paco Torres / Babs Okoye** — Barghest recruits; Paco can desert and join the
  Scavengers after *Balls to the Wall*. A recruitment path from Barghest into
  the swarm. `[wiki]`
- **Hasan Demir** — former Zetatech techie with the stolen prototype in his eye;
  the Scraper's prisoner, not a Scav. `[wiki]`
- **Katya Karelina / Mark Bana / the BIA** — the SovOil–BIA spy plot behind
  *Spy in the Jungle*; Boris's contract target and the agents who hire V. `[wiki]`
- **Stefan** — BD dealer who lures V into the Sweet Dreams trap; a Scav
  accomplice (record `Character.mq036_stefan`), not a boss. `[game-data]`
- **Sandra Dorsett, Evelyn Parker, Alois Daquin, Ellen Verde** — victims whose
  abductions define the faction's public face. They are the demand signal, not
  political actors. `[wiki]`
- **The unnamed Soviet general** — a `Character.q303_paradise_scav_general`
  actor seated with Tzar at the Black Sapphire; the only visible Soviet command
  symbol. Do not name him. `[game-data]`

### 3.4 Guarantor assessment

The design question: if a player founds a gang, which factions would guarantee
the Scavengers' support, and which would the Scavengers guarantee?

- **No `ally`, no `patron` and no `client` row.** Nothing in the lore protects,
  funds or formally hires the faction as a whole. The closest rows are `trade`
  (Barghest's paid tolerance is recorded as `rival`, Aldecaldos, Wraiths,
  Animals) and they are all cell-level.
- **The Scavengers are a hired auxiliary, not a loyal one.** A player can buy
  scav muscle, buy their chrome, or buy their silence, exactly as Fawlter,
  Mordellini, Tzar, Kolev and the Aldecaldos do. The guarantee lasts as long as
  the payment; Yasha's "I'm a slut for those sweet, sweet eddies" is the whole
  doctrine. `[wiki]`
- **They are a poor political guarantor.** The matrix has no ally and no
  patron. Their political capital is four things: chrome, den space, a Soviet
  export channel and a willingness to do dirty work. Three are private and one
  is a rumor.
- **They are a likely aggressor.** The design's "at war with everyone" is
  directionally right: scavs raid NetWatch stashes, Arasaka containers, Tyger
  shipments and Barghest convoys. A player who takes a Scav point should expect
  retaliation, not negotiation.
- **Plausible guarantors for a player-founded gang** are transactional: hire
  scav muscle, buy chrome through them, share an enemy (Barghest, Tyger Claws,
  NCPD), or use their Soviet export channel. Not loyalty, not territory, not
  diplomacy.
- **The Scavengers as a guarantor for a player**: a player who wins one cell
  gets that cell's den, buyer and crew; the other cells remain neutral or
  hostile. The faction cannot guarantee anything it does not centrally
  control — and it centrally controls nothing.

---

## 4. Pillar notes

The design does not assign the Scavengers an archetype or a strength/weakness
pair in `docs/design/gameplay-systems.md` §1; it makes them a special
"rebel/pirate" swarm faction. The closest fit would be a **Syndicate** economy
with a **Tribe** culture, but forcing either label loses the point. Assess the
six pillars directly.

| Pillar | Design claim | Lore verdict | Evidence |
| --- | --- | --- | --- |
| Politics | No claim; the Scavs are outside the political archetype table | **None.** No seat, no legitimacy, no alliance, no diplomatic channel. Their only politics is buying tolerance and selling violence. | Wiki infobox blanks; no HQ row; Tzar's party is access, not office `[wiki]` `[game-data]` |
| Espionage | No claim | **Mixed.** They have netrunners (`Spider` archetype, Michal Glowinski, Yelena), a Soviet-intelligence rumor and a working export channel. They also broadcast a 24-recipient shard about a murder and leave patient files on the floor. Good local intelligence, terrible opsec. | *SOCA: Wipe the Gonk* shard; `Character.q105_bds_*_netrunner*`; Yelena's computer `[game-data]` `[wiki]` |
| Economy | No claim; the design gives them every neutral point | **Strong in one niche, weak in diversification.** They hold a near-monopoly on low-end chrome and organs and are the main suppliers to other gangs, small-time criminals and shady ripperdocs. They are price-takers, not manufacturers; `income_multiplier` is 0.8 in `factions.json`. | Wiki *Sources of Income*; `data/factions.json` `[wiki]` `[game-data]` |
| Military | No claim; "rebels/pirates" | **Weak operationally, dangerous locally.** Numbers, ambush, turrets, mines and netrunners; the Scraper holds 43 units. But one merc beats every named boss, and they have no armour, air or force projection. | Site 357; all seven boss fights `[game-data]` `[wiki]` |
| Culture | No claim | **Weak/none at faction level.** No shared creed beyond predation and a Soviet/European aesthetic; cells distrust each other, and Dogtown despises Night City. The culture is the tracksuit and the tattoo, not an institution. | Wiki *Philosophy and Structure*, *Scavs in Dogtown* `[wiki]` |
| Technology | No claim | **Medium.** They use cyberoptics, pain editors, health monitors, Kerenzikov and K.E.R.S.; they have netrunners and a Zetatech prototype. But the tech is bought, stolen or scavenged, and they have no R&D. | Wiki *Philosophy and Structure*; *Prototype in the Scraper* `[wiki]` |

Design cautions, not redesigns:

- **Do not give the Scavengers a faction-wide leader.** Cell bosses are the top
  rank. The design's "internal war with no single leader" is their normal state,
  not a failure state.
- **Model cells as blocs, not departments.** A cell owns its den, its buyer and
  its crew. Losing a boss decapitates that cell; it does not change the faction.
- **The den is the succession mechanic.** A player rises by taking a den, not by
  earning favour. That is a distinct advancement path from the other gangs.
- **Do not model them as poor.** The Dogtown oligarchy has cash, equipment and
  a Soviet export channel; the NC crews are poor, not the faction.
- **Do not model them as a standing army.** With the campaign disabled, every
  named Scav is quest- or activity-gated. The mod must spawn the cast.
- **Do not give them `protection` or `drugs` revenue without evidence.** The
  wiki's business model is chrome, mercenary work, XBD and smuggling. The Los
  Osos amnesia batch is contraband moving through a cell, not a drug lab.
- **Do not make them uniformly anti-corp.** Kolev's implant list is a
  corp-agnostic shopping list; the scavs buy, steal and resell Arasaka, Militech,
  Dynalar, Biodyne, Kiroshi and Fenghuang chrome.

---

## 5. Gaps and uncertainties

1. **There is no faction-wide leader, and none should be invented.** The wiki
   leaves `leadership` and `headquarters` blank; the text says "no official
   hierarchy". Tzar is the most visible Scav, but he is a host, not a boss. Any
   model with a single Scav leader contradicts the sources.
2. **Tzar has no wiki page.** The name, faction, record and party placement are
   game-data only. The "oligarch" label is the wiki's description of the
   Dogtown wing, not a title Tzar is given. `[game-data]` `[wiki]` `[inferred]`
3. **Tzar's general is unnamed.** The record is
   `Character.q303_paradise_scav_general` with appearance
   `man_average__q303__soviet_general`. Do not name him or promote him to a
   faction rank; he is a single scripted actor. `[game-data]`
4. **Boris's record is a deduction.** The site's only boss record is
   `Character.sts_ep1_08_kgb_boss`, appearance `fiodor`, with holographic decoys;
   the gig names Boris Ribakov. The mapping is by elimination and appearance,
   tagged `[inferred]`. Verify in game. `[game-data]` `[wiki]`
5. **Yasha's record is a deduction.** `Character.sts_ep1_03_miniboss_placeholder`
   is the only boss slot at Los Osos; the gig text names Yasha as the large
   scavenger. Tagged `[inferred]`. `[game-data]` `[wiki]`
6. **Kolev has no named record.** Site 114 holds four generic melee scavs and a
   generic `gang_leader` entry. The identity comes from the NCPD dispatcher and
   the wiki. Do not seed a `kolev` record until one is found. `[game-data]`
   `[wiki]`
7. **The Valentinos and 6th Street docs overstate their rows.** Both use
   `{sa_ep1_135_com_combat}` as relation evidence, but it is a Phantom Liberty
   courier-loop combat pool (4 Scavs, 4 6th Street, 4 Valentinos, 1 Arasaka)
   that METHOD §1.3 item 3 says to exclude. This doc records both as `neutral`.
   A reviewer may prefer to keep `rival` for symmetry; the lore does not support
   it. `[game-data]`
8. **The Tyger Claws doc says `rival`; this doc says `hostile`.** The decisive
   difference is Zbyszko's murder of Goose and the deliberate frame-up of the
   Animals, plus the Jae-Hyun/Jotaro victim-trade channel. `rival` understates
   the killing; `hostile` is the better fit. Flagged for cross-doc reconciliation.
   `[wiki]` `[game-data]`
9. **The Arasaka and Militech docs say `neutral`; this doc says `rival` and
   `trade`.** Arasaka: Kolev's cell salvages a container from an Arasaka
   aircraft. Militech: Los Osos buys 3rd-gen Militech chrome from an
   intermediary. Both are black-market/opportunistic, not corporate policy; the
   asymmetry is intentional and flagged. `[wiki]` `[game-data]`
10. **Damir Kovac is a shared asset, not a member of two factions.** The
    Scavengers Members page lists him; the Animals doc calls him "the Animals'
    ripperdoc". The wiki database entry resolves it: he works for the scavs in
    Terra Cognita and "sometimes takes jobs from Animals". `[wiki]`
11. **The Scavenger Den has no site and no dedicated marker.** Its evidence is
    the `{mq036_com_scavengers}` area plus the *Rescue* markers; the address
    ("apartments 1235 and 1237, Crescent Street") is wiki identity evidence, not
    a coordinate. This doc uses the location doc's anchor and does not repeat it.
    `[wiki]` `[game-data]`
12. **The Scraper has no named leader.** 43 units, the faction's largest
    garrison, and no boss record. The only authority marker is the keycode-locked
    armory (2045). Do not invent a boss to fill the seat. `[game-data]` `[wiki]`
13. **The Dogtown "oligarchy" is not one place.** The four venues (Scraper,
    Digimmortal, Organitopia, ESC Explorer) share no community hash. The location
    doc checked; this doc models a cluster, not a headquarters. `[game-data]`
14. **The Soviet intelligence link is a rumor with three details.** Zbyszko's
    export, Boris's SovOil background and Tzar's `soviet_general` actor are
    suggestive, not proof of a command structure. Do not invent a Soviet faction
    row; `sovoil` has no code in `data/factions.json`. `[wiki]` `[game-data]`
15. **The Los Osos amnesia drug batch contradicts the location doc's "no drugs"
    finding.** The shard says "that amnesia shit … before it goes to NC"; the
    location doc says the only drug reference near a scav site is a Tyger stash.
    This is contraband moving through a cell, not evidence of a scav drug lab.
    Do not add a `drugs` revenue stream to the location catalog without a check.
    `[wiki]`
16. **The "at war with everyone" premise is a design rule, not a lore fact.**
    Lore shows paid tolerance (Barghest), a real cyberware trade (Aldecaldos), a
    cell-level Wraith partnership, Animal bodyguards and a corrupt NCPD channel.
    The design overrides these in play; the research matrix records them so the
    override is a choice, not an accident. `[wiki]` `[game-data]`
    `docs/design/gameplay-systems.md`
17. **No member counts per cell.** Roster units and area entries are presence
    proxies; several `q###_*` communities are phases of one site. Do not sum
    them. `[game-data]`
18. **Almost every named Scav is quest- or activity-gated.** With the campaign
    disabled, the mod must spawn Tzar, Boris, Nika, Kolev, Zbyszko, Yelena,
    Barry, Roman, Yasha, Kajetan and Damir itself. `[game-data]`
19. **The fixers are mostly clients of V against the scavs, not clients of the
    scavs.** Mr. Hands, Regina and Wakako sell contracts to remove scav cells;
    they are not buyers of chrome. Do not model them as scav customers. `[wiki]`
20. **`factions.json` has `hostility_bias` 0.9 and `income_multiplier` 0.8 for
    the Scavengers.** These are seed knobs, not political evidence. They are
    consistent with the design's "at war with everyone" and poor-economy read,
    but they should not be cited as lore. `[game-data]`

### 5.1 Sources consulted

- Local: `data/factions.json`, `data/sites/rosters.json`,
  `data/sites/sites.json`, `data/sites/communities.json`,
  `data/sites/{guards,triggers,spots,patrols,doors,devices}.json`,
  `data/sites/suitabilities.json`, `data/sub_territories.json`,
  `data/control_centers.json`, `data/faction_headquarters.json`,
  `data/districts.json`, `dist/extract/areas.jsonl`,
  `dist/extract/markers.jsonl`,
  `dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_1.streamingsector.json`
  (community registry: `characterRecordId`, `entryName`, `phaseName`,
  `spotNodeRefs`, appearances).
- Wiki: [Scavengers](https://cyberpunk.fandom.com/wiki/Scavengers),
  [Scavengers Members](https://cyberpunk.fandom.com/wiki/Scavengers_Members),
  [Boris Ribakov](https://cyberpunk.fandom.com/wiki/Boris_Ribakov),
  [Nika Yankovich](https://cyberpunk.fandom.com/wiki/Nika_Yankovich),
  [Anton Kolev](https://cyberpunk.fandom.com/wiki/Anton_Kolev),
  [Stanislaus Zbyszko](https://cyberpunk.fandom.com/wiki/Stanislaus_Zbyszko),
  [Yelena Sidorova](https://cyberpunk.fandom.com/wiki/Yelena_Sidorova),
  [Barry Alken](https://cyberpunk.fandom.com/wiki/Barry_Alken),
  [Roman (Cyberpunk 2077)](https://cyberpunk.fandom.com/wiki/Roman_(Cyberpunk_2077)),
  [Kajetan Zilevski](https://cyberpunk.fandom.com/wiki/Kajetan_Zilevski),
  [Misha Orlova](https://cyberpunk.fandom.com/wiki/Misha_Orlova),
  [Damir Kovac](https://cyberpunk.fandom.com/wiki/Damir_Kovac),
  [Jerry Fawlter](https://cyberpunk.fandom.com/wiki/Jerry_Fawlter),
  [Bartolomeo Mordellini](https://cyberpunk.fandom.com/wiki/Bartolomeo_Mordellini),
  [Leon Rinder](https://cyberpunk.fandom.com/wiki/Leon_Rinder).
- Gigs, side jobs and NCPD activities:
  [The Rescue](https://cyberpunk.fandom.com/wiki/The_Rescue),
  [Sweet Dreams](https://cyberpunk.fandom.com/wiki/Sweet_Dreams),
  [Disasterpiece](https://cyberpunk.fandom.com/wiki/Disasterpiece),
  [Gun Music](https://cyberpunk.fandom.com/wiki/Gun_Music),
  [Balls to the Wall](https://cyberpunk.fandom.com/wiki/Balls_to_the_Wall),
  [No Easy Way Out](https://cyberpunk.fandom.com/wiki/No_Easy_Way_Out),
  [Gig: Prototype in the Scraper](https://cyberpunk.fandom.com/wiki/Gig:_Prototype_in_the_Scraper),
  [Gig: The Man Who Killed Jason Foreman](https://cyberpunk.fandom.com/wiki/Gig:_The_Man_Who_Killed_Jason_Foreman),
  [Gig: Spy in the Jungle](https://cyberpunk.fandom.com/wiki/Gig:_Spy_in_the_Jungle),
  [Gig: Dogtown Saints](https://cyberpunk.fandom.com/wiki/Gig:_Dogtown_Saints),
  [Gig: Last Login](https://cyberpunk.fandom.com/wiki/Gig:_Last_Login),
  [Gig: Small Man, Big Evil](https://cyberpunk.fandom.com/wiki/Gig:_Small_Man,_Big_Evil),
  [SOCA: Wipe the Gonk, Take the Implants](https://cyberpunk.fandom.com/wiki/Suspected_Organized_Crime_Activity:_Wipe_the_Gonk,_Take_the_Implants),
  [SOCA: Vice Control](https://cyberpunk.fandom.com/wiki/Suspected_Organized_Crime_Activity:_Vice_Control),
  [SOCA: Opposites Attract](https://cyberpunk.fandom.com/wiki/Suspected_Organized_Crime_Activity:_Opposites_Attract),
  [SOCA (West Wind Estate)](https://cyberpunk.fandom.com/wiki/Suspected_Organized_Crime_Activity_(West_Wind_Estate)),
  [Reported Crime: Needle in a Haystack](https://cyberpunk.fandom.com/wiki/Reported_Crime:_Needle_in_a_Haystack),
  [Reported Crime: Paranoia](https://cyberpunk.fandom.com/wiki/Reported_Crime:_Paranoia),
  [Reported Crime: Lost and Found](https://cyberpunk.fandom.com/wiki/Reported_Crime:_Lost_and_Found),
  [Reported Crime: Turn Off the Tap](https://cyberpunk.fandom.com/wiki/Reported_Crime:_Turn_Off_the_Tap).
- Shards and computers:
  [Archived Conversation: Jason Foreman and Slava Makarov](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Jason_Foreman_and_Slava_Makarov),
  [Archived Conversation: Yasha Ivanov and Luka Morozov](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Yasha_Ivanov_and_Luka_Morozov),
  [Archived Conversation: Stanislaus Zbyszko to 24 recipients](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Stanislaus_Zbyszko_to_24_recipients),
  [Archived Conversation: Jonah Harper and Anton Kolev](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Jonah_Harper_and_Anton_Kolev),
  [Archived Conversation: Kajetan Zilevski and Bartolomeo Mordellini](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Kajetan_Zilevski_and_Bartolomeo_Mordellini),
  [Archived Conversation: Samuil Egorov and Darya Alexeeva](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Samuil_Egorov_and_Darya_Alexeeva),
  [Archived Conversation: Gennady Korolev and Kirill Osipov](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Gennady_Korolev_and_Kirill_Osipov),
  [today's hunt](https://cyberpunk.fandom.com/wiki/Today%27s_hunt),
  [Note for ripperdoc](https://cyberpunk.fandom.com/wiki/Note_for_ripperdoc),
  [Implant list](https://cyberpunk.fandom.com/wiki/Implant_list),
  [Kiroshi XtremSight 4553](https://cyberpunk.fandom.com/wiki/Kiroshi_XtremSight_4553_(Computer_message)),
  [Yelena Sidorova/Computers](https://cyberpunk.fandom.com/wiki/Yelena_Sidorova/Computers),
  [boris's recipe](https://cyberpunk.fandom.com/wiki/Boris%27s_recipe).
- Earlier repo research: `docs/research/factions/scavengers.md`,
  `docs/research/factions/METHOD.md`, `docs/design/gameplay-systems.md`,
  `docs/research/factions/politics/animals.md`,
  `docs/research/factions/politics/barghest.md`,
  `docs/research/factions/politics/voodoo-boys.md`,
  `docs/research/factions/politics/the-mox.md`,
  `docs/research/factions/politics/tyger-claws.md`,
  `docs/research/factions/politics/valentinos.md`,
  `docs/research/factions/politics/sixth-street.md`,
  `docs/research/factions/politics/maelstrom.md`,
  `docs/research/factions/politics/aldecaldos.md`,
  `docs/research/factions/politics/militech.md`,
  `docs/research/factions/politics/arasaka.md`.

---

## 6. Machine-readable block

```json
{
  "faction_code": "scavengers",
  "leaders": [
    {
      "name": "Tzar",
      "role": "Dogtown oligarch; host of the Scav table at the Black Sapphire; not a faction-wide boss",
      "character_record_id": "Character.q303_paradise_scav_tzar",
      "location_name": "Black Sapphire, Dogtown",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_1 registry entry 13_tzar (phase spawn, spot #q303_ws_paradise_chat_13_scav_tzar); q303 guest community; wiki Scavs in Dogtown database entry",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Tzar's general (unnamed)",
      "role": "Unnamed Soviet-general actor seated with Tzar; the only visible Soviet command link",
      "character_record_id": "Character.q303_paradise_scav_general",
      "location_name": "Black Sapphire, Dogtown",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_1 registry entry 13_tzar_general (appearance man_average__q303__soviet_general, spot #q303_ws_paradise_chat_13_scav_general)",
      "confidence": "game-data+inferred"
    },
    {
      "name": "Boris Ribakov",
      "role": "Boss of the Organitopia cell; ex-Spetsnaz, SovOil operative",
      "character_record_id": "Character.sts_ep1_08_kgb_boss",
      "location_name": "Organitopia, Terra Cognita, Dogtown",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "site 360 sts_ep1_08 (16 units); only boss record at #sts_ep1_08_boss_ws_001; Gig Spy in the Jungle; wiki Boris Ribakov",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "name": "Nika Yankovich",
      "role": "Leader of the Haven Clinic cell; Gaspar's twin",
      "character_record_id": "Character.sts_ep1_01_nika",
      "location_name": "Haven Clinic, Montana de Oro Ave, Dogtown",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "site 355 sts_ep1_01 (16 units); raw entry nika; Gig Dogtown Saints; wiki Nika Yankovich",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Slava Makarov",
      "role": "Dealmaker of the Los Osos cell; buys combat chrome",
      "character_record_id": null,
      "location_name": "Los Osos motel, West Wind Estate",
      "presence_class": "mentioned",
      "open_world": false,
      "source": "shard Archived Conversation Jason Foreman and Slava Makarov (sts_ep1_03_shard_009); Gig The Man Who Killed Jason Foreman",
      "confidence": "wiki"
    },
    {
      "name": "Yasha Ivanov",
      "role": "Los Osos enforcer; the gig's mandatory boss",
      "character_record_id": "Character.sts_ep1_03_miniboss_placeholder",
      "location_name": "Los Osos motel, West Wind Estate",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "site 356 sts_ep1_03 (18 units); only miniboss slot; shard sts_ep1_03_shard_022_boss; gig text names Yasha",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "name": "Luka Morozov",
      "role": "Los Osos coordinator; relays Damir Kovac's orders",
      "character_record_id": null,
      "location_name": "Los Osos motel, West Wind Estate",
      "presence_class": "mentioned",
      "open_world": false,
      "source": "shard Archived Conversation Yasha Ivanov and Luka Morozov (sts_ep1_03_shard_022_boss)",
      "confidence": "wiki"
    },
    {
      "name": "Anton Kolev",
      "role": "Boss of the Pacific Boulevard and West Wind cell; Wraith partner",
      "character_record_id": null,
      "location_name": "Pacific Blvd, West Wind Estate",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "site 114 ma_pac_wwd_04 (4 units); NCPD dispatcher; wiki Anton Kolev; shard ma_pac_wwd_04_onscreen_01; no named record found",
      "confidence": "wiki+game-data+inferred"
    },
    {
      "name": "Stanislaus Zbyszko",
      "role": "Captain of the Eden Beach cell; smuggling priors",
      "character_record_id": "Character.ma_pac_cvi_12_outpost_miniboss",
      "location_name": "Eden Beach Mega Ride, Coastview",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "site 107 ma_pac_cvi_12 (16 units); only outpost_miniboss slot; SOCA Wipe the Gonk Take the Implants; shard ma_pac_cvi_12_onscreen_01",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "name": "Yelena Sidorova",
      "role": "Leader of the Ross Street cell; NCPD commissioner's contractor",
      "character_record_id": "Character.ma_wat_nid_01_outpost_miniboss",
      "location_name": "Ross Street Parking Facility, Northside",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "site 215 ma_wat_nid_01 (12 units); only outpost_miniboss slot; SOCA Vice Control; computer get to work",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "name": "Barry Alken",
      "role": "Leader of the Little China hit squad",
      "character_record_id": "Character.ma_wat_lch_01_outpost_miniboss",
      "location_name": "Opposites Attract rooftop, Goldsmith and Cortes, Little China",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "site 192 ma_wat_lch_01 (12 units); only outpost_miniboss slot; SOCA Opposites Attract; wiki Barry Alken",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "name": "Roman",
      "role": "Leader of the Arroyo cell; Aldecaldo cyberware buyer",
      "character_record_id": "Character.mq002_scavenger_leader",
      "location_name": "MLK Boulevard and Valley, Arroyo",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "raw registry entry leader at #mq002_ws_scav_lead_deal; Gun Music; wiki Roman (Cyberpunk 2077)",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "name": "Scavenger Den boss (unnamed)",
      "role": "Boss of the JapanTown prologue den",
      "character_record_id": "Character.q001_scavenger_boss",
      "location_name": "Scavenger Den, Crescent St., JapanTown",
      "presence_class": "story",
      "open_world": false,
      "source": "raw registry entry boss; The Rescue; Sweet Dreams",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Kajetan Zilevski",
      "role": "Downtown hitman; Mordellini's contract killer",
      "character_record_id": "Character.ma_cct_dtn_12_kajetan_zilevsk",
      "location_name": "Corpo Plaza and Downtown",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "site 38 ma_cct_dtn_12; Reported Crime Turn Off the Tap; shard ma_cct_dtn_12_onscreen_01",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Damir Kovac",
      "role": "Ripperdoc; the Terra Cognita network's medical authority",
      "character_record_id": "Character.mq306_damir",
      "location_name": "Digimmortal and Los Osos, Dogtown",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "wiki Damir Kovac; No Easy Way Out; Los Osos shards",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Misha Orlova",
      "role": "Wild Blue crew member; witness to Ellen Verde",
      "character_record_id": "Character.ma_pac_cvi_09_scavenger_fast3_fmelee3_machete_wa_elite_Misha_Orlova",
      "location_name": "Wild Blue, Coastview",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "site 97 ma_pac_cvi_09; Assault in Progress; wiki Misha Orlova",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Michal Glowinski",
      "role": "Coastview netrunner",
      "character_record_id": "Character.ma_pac_cvi_07_scavenger_grunt3_netrunner2_nova_ma_rare_Michal_Glowinski",
      "location_name": "Coastview",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "site 95 ma_pac_cvi_07; scanner activity",
      "confidence": "game-data"
    },
    {
      "name": "Alan Crank",
      "role": "Northside docks crew; hunts a Tyger container",
      "character_record_id": "Character.ma_wat_nid_12_shard_scav",
      "location_name": "Northside Docks",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "site 225 ma_wat_nid_12; Reported Crime Needle in a Haystack; wiki Alan Crank",
      "confidence": "game-data+wiki+inferred"
    }
  ],
  "internal_factions": [
    {
      "name": "Dogtown oligarchy (Black Sapphire)",
      "leader": "Tzar",
      "goals": "Money, chrome, Soviet contacts and Barghest's tolerance; keep the Black Sapphire table and the Dogtown business",
      "members_hint": "34 Dogtown areas / 240 entries; Scraper 43 units, Organitopia 16, Digimmortal 37 entries, ESC Explorer 29 entries; Tzar, Boris, Nika, Damir",
      "source": "wiki Scavs in Dogtown; q303 Tzar registry; docs/research/factions/scavengers.md",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The Scraper mass (Longshore Stacks)",
      "leader": null,
      "goals": "Hold the largest squat, sell the Zetatech prototype, keep the armory, prison and lift",
      "members_hint": "site 357 sts_ep1_04; 43 units; 5 communities; 9 doors; armory keycode 2045",
      "source": "Gig Prototype in the Scraper; site 357",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Organitopia cell",
      "leader": "Boris Ribakov",
      "goals": "Serve the SovOil contract, hunt Katya Karelina, hold the museum",
      "members_hint": "site 360 sts_ep1_08; 16 units; sts_ep1_08_front_building_com 4, sts_ep1_08_enemies_com 12",
      "source": "Gig Spy in the Jungle; wiki Boris Ribakov",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Haven Clinic cell",
      "leader": "Nika Yankovich",
      "goals": "Recover Gaspar's body, pressure the ripperdoc, hold the clinic",
      "members_hint": "site 355 sts_ep1_01; 16 units; nika plus generic crew",
      "source": "Gig Dogtown Saints; wiki Nika Yankovich",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Los Osos and West Wind network",
      "leader": "Slava Makarov",
      "goals": "Buy Militech-grade chrome, protect paying clients, move the amnesia drug batch, keep the Wraith partnership",
      "members_hint": "Los Osos 18 units; Kolev site 4 units; Wraiths present at Kolev's base; Slava, Yasha, Luka, Samuil, Darya, Gennady, Kirill",
      "source": "Gig The Man Who Killed Jason Foreman; shards; SOCA West Wind Estate",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Eden Beach smuggling cell",
      "leader": "Stanislaus Zbyszko",
      "goals": "Export implants to the Soviet Union, keep the Tyger Claws fooled, avoid NCPD",
      "members_hint": "site 107 ma_pac_cvi_12; 16 units; 5 guard volumes, 31 spots, 9 patrols",
      "source": "SOCA Wipe the Gonk Take the Implants; shard ma_pac_cvi_12_onscreen_01; today's hunt",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Night City street cells",
      "leader": "Yelena Sidorova (Ross Street); Barry Alken (Little China); Roman (Arroyo); unnamed Den boss (JapanTown); Kajetan Zilevski (Downtown); Alan Crank (Northside)",
      "goals": "Survive, sell to fixers and ripperdocs, take paid work",
      "members_hint": "Ross St 12, Opposites 12, Scavenger Den 27 entries, Kajetan site 38, Roman mq002",
      "source": "SOCA Vice Control, SOCA Opposites Attract, Gun Music, The Rescue, Turn Off the Tap, Needle in a Haystack",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Ripperdoc network",
      "leader": "Damir Kovac",
      "goals": "Supply chrome, keep clients quiet, profit from both scavs and Animals",
      "members_hint": "Damir at Digimmortal and Los Osos; Fingers in Japantown; Charles Bucks above the Eisenhower den",
      "source": "wiki Damir Kovac; No Easy Way Out; Disasterpiece; Last Login",
      "confidence": "wiki+game-data"
    },
    {
      "name": "Mercenary contract wing",
      "leader": "Yelena Sidorova; Kajetan Zilevski; Tzar; Anton Kolev",
      "goals": "Sell violence no questions asked; keep the client",
      "members_hint": "Yelena's NCPD contract; Kajetan's hit for Mordellini; Tzar's two Animal guards; Kolev's Wraith partners",
      "source": "Vice Control; Turn Off the Tap; q303 registry; SOCA West Wind Estate",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Soviet-linked current vs Night City rabble",
      "leader": null,
      "goals": "Discipline, equipment and business vs survival, improvisation and predation",
      "members_hint": "Dogtown's better gear; Zbyszko's Soviet export; Boris's SovOil background; the wiki's disdain for the poorer NC kind",
      "source": "wiki Scavs in Dogtown; Spy in the Jungle; ma_pac_cvi_12 shard",
      "confidence": "wiki+game-data"
    }
  ],
  "relations": [
    {
      "faction_code": "tyger_claws",
      "stance": "hostile",
      "evidence": "Zbyszko's cell kills the courier Goose, who was carrying high-tech implants from the Tygers, then orders the crew to blame the Animals; Reported Crime Lost and Found is a scav-vs-Tyger alley scrap in Japantown; Needle in a Haystack is scavs hunting a container marked with Tyger graffiti; the Kabuki and Allen St dens sit inside Tyger turf. The trafficking channel runs the other way: Jae-Hyun delivers kidnapped victims to the scavs and they end up with a Tyger like Jotaro Shobo. Hostile with a victim-trade channel [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "valentinos",
      "stance": "neutral",
      "evidence": "No reliable incident. The Valentinos doc's rival row rests on sa_ep1_135_com_combat, a Phantom Liberty courier-loop combat pool (4 Scavs, 4 6th Street, 4 Valentinos, 1 Arasaka), which METHOD 1.3 item 3 says to exclude. Both work the chrome and sex economy in different districts; no attested deal or fight [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "arasaka",
      "stance": "rival",
      "evidence": "Kolev's cell moves on a container from an Arasaka aircraft that landed on the West Wind beach, and his implant list includes an Arasaka Yonaguni Xc; the Scraper holds a stolen Zetatech prototype, not Arasaka property. No campaign, no deal - opportunistic predation on Arasaka salvage. The Arasaka doc records neutral [wiki] [game-data] [inferred]",
      "confidence": "wiki+game-data+inferred"
    },
    {
      "faction_code": "militech",
      "stance": "trade",
      "evidence": "The Los Osos cell buys militech 3rd gen combat implants from Jason Foreman's supplier; Kolev's implant list includes Militech Kairos 6-M and Svalinn 9-F; the buyer is a black-market intermediary, not Militech procurement. Trade in stolen or off-book chrome, no corporate sanction. The Militech doc records neutral [wiki] [game-data]",
      "confidence": "wiki+game-data"
    },
    {
      "faction_code": "kang_tao",
      "stance": "neutral",
      "evidence": "No attested interaction. Fenghuang Hu shen-II appears on Kolev's implant list, a black-market brand, not a relationship [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "biotechnica",
      "stance": "neutral",
      "evidence": "No attested interaction. Boris's pelmeni recipe uses a Biotechnica protein brick, a consumer purchase, not a political channel [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "petrochem",
      "stance": "neutral",
      "evidence": "No attested interaction. The same recipe uses Petrochem synth-flour; the EBM Petrochem Stadium is a Dogtown landmark, not a scav patron [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "barghest",
      "stance": "rival",
      "evidence": "In business with BARGHEST as frequently as they clash; the Dogtown scav oligarchy secures business in Hansen's backyard and It's all about the money; scavs steal airdrops and ambush Paco Torres's convoy in Balls to the Wall, and Paco can later join them. Paid tolerance plus predation, not an alliance [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "sixth_street",
      "stance": "neutral",
      "evidence": "No reliable incident. The 6th Street doc's rival row also rests on sa_ep1_135_com_combat, the PL courier-loop pool excluded by METHOD 1.3 item 3. The Gun Music site is in Arroyo but the counterparties are Aldecaldos, not 6th Street [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "aldecaldos",
      "stance": "trade",
      "evidence": "Gun Music: Cassidy, Carol and Teddy deliver cyberware to Roman's crew in Arroyo; Roman complains the delivery is three days late and haggles the cut, and the deal nearly becomes a firefight. Kolev also sources a Kiroshi XtremSight 4553 for the Aldecaldo Jason Wildriver. The Aldecaldos doc records the same trade [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "wraiths",
      "stance": "trade",
      "evidence": "Kolev collaborates with the Wraiths at the former El Dorado pawn shop on Pacific Boulevard; Wraiths members are present at his base, and Kolev and Jonah Harper immediately agreed to send security personnel to the Arasaka container. A cell-level operational partnership, not a faction treaty - the closest stance is trade [wiki] [game-data]",
      "confidence": "wiki+game-data"
    },
    {
      "faction_code": "animals",
      "stance": "trade",
      "evidence": "Two Character.q303_paradise_animal_guard flank Tzar at the Black Sapphire - a paid muscle contract; Damir Kovac works for the scavs and sometimes takes jobs from Animals; Zbyszko's frame-up blames the Animals for Goose's death, which is propaganda, not a war. The Animals doc records the same trade [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "the_mox",
      "stance": "hostile",
      "evidence": "Fingers sold Evelyn Parker to the scavs; they held her in the XBD studio at the abandoned power plant and tortured her; Judy and V raid it and kill the crew (Disasterpiece, Double Life). The Mox's protection mandate is anti-Scav. The Mox doc records hostile [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "maelstrom",
      "stance": "rival",
      "evidence": "Compete for the same chrome and salvage; Reported Crime Paranoia places scavs and optional Maelstrom at the same Little China scene; Maelstrom's own doc records rival. No attested deal or full war [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "voodoo_boys",
      "stance": "hostile",
      "evidence": "Placide orders Fara Dupont to surround and kill scavs who raided a NetWatch stash; four VDB members (Fara Dupont, Diesuel, Josue, Lovelie) were killed by scavs; both operate in Pacifica, West Wind and Terra Cognita. The VDB doc records hostile [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "ncpd",
      "stance": "hostile",
      "evidence": "Standing target: NCPD APBs name Zbyszko, Kolev, Yelena and Barry; scanner hustles and reported crimes at Ross Street, Opposites Attract, Eden Beach, West Wind, Northside and Coastview. Yet commissioner Jerry Fawlter hires Yelena to clear the homeless and promises to ignore calls from the area - hostile with a corrupt channel [game-data] [wiki]",
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
      "evidence": "No attested interaction. The Northside clearance is an NCPD commissioner's project, not a Council vote; no purchased channel found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_regina",
      "stance": "hostile",
      "evidence": "Regina gives Last Login (Eisenhower St den) and Small Man Big Evil (Allen St rooftop processing site); both send V to kill or displace scavs [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_wakako",
      "stance": "hostile",
      "evidence": "Wakako gives The Rescue, the prologue raid on the Scavenger Den; she is also the fixer V asks about the XBD trade that leads to the power-plant scav studio in Disasterpiece [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_padre",
      "stance": "neutral",
      "evidence": "No Scav-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_el_capitan",
      "stance": "neutral",
      "evidence": "No Scav-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_dakota",
      "stance": "neutral",
      "evidence": "No Scav-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_dino",
      "stance": "neutral",
      "evidence": "No Scav-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_rogue",
      "stance": "neutral",
      "evidence": "No Scav-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_mr_hands",
      "stance": "hostile",
      "evidence": "Mr. Hands gives four Dogtown gigs aimed at scav cells: Prototype in the Scraper, The Man Who Killed Jason Foreman, Spy in the Jungle and Dogtown Saints [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "afterlife",
      "stance": "neutral",
      "evidence": "Neutral merc marketplace; no Scav doorman or contract attested [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "netwatch",
      "stance": "hostile",
      "evidence": "Scavs raided a NetWatch stash in Pacifica; the VDB retaliation is recorded in the Voodoo Boys doc. No NetWatch counter-operation beyond that raid is attested [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "nusa",
      "stance": "neutral",
      "evidence": "No direct NUSA-Scav interaction. The Dogtown Soviet-intelligence rumor is not a NUSA relationship; the FIA's Dogtown file does not name the scavs [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "zetatech",
      "stance": "rival",
      "evidence": "The Scraper garrison holds a stolen Zetatech prototype implant; Hasan Demir, a former Zetatech techie, had it in his eye; Los Osos patient files describe knockoff Zetatech implants; Darya Alexeeva uses Zetatech gear. Corporate IP theft, no contract [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "trauma_team",
      "stance": "hostile",
      "evidence": "Barry Alken's rooftop crew is looting a Trauma Team container while a Trauma Team AV flies away (SOCA Opposites Attract); the E3 2018 trailer shows scavs fighting Trauma Team. Scavs are the reason Trauma Team exists in the fiction - they strip patients before pickup [game-data] [wiki] [inferred]",
      "confidence": "game-data+wiki+inferred"
    }
  ]
}
```
