# Animals — Leadership, Internal Politics and External Relations

Status: research run, 2026-11-25. One faction, one document.
Scope: Cyberpunk 2077 2.5 + Phantom Liberty, campaign disabled. Who a player can
join under, climb past, ally with or remove; the internal blocs; and the external
relations matrix needed for wars, alliances and "guarantor" support when a player
founds a gang.

Method: this document follows [`METHOD.md`](./METHOD.md), including its §1.1 and
§1.2 corrections. The location catalog for the Animals is
[`../animals.md`](../animals.md); this document maps people and politics onto
those places and does not repeat the coordinates.

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
activity-gated; `story` = main/side job gated; `prologue` = lifepath intro (no
Animal uses this); `off-map` = named and alive in 2077 but never spawned;
`mentioned` = named only in shards, dialogue or a poster; `historical` = not
present in 2077. The JSON `open_world` flag is `true` for `ambient` +
`world-activity`, `false` for `story` + `prologue` + `off-map` + `mentioned` +
`historical`.

The Animals needed one extra distinction that the other gang docs did not: they
**have no faction-level leader at all**. The wiki names pack leaders and
secondary leaders, never a boss. This document treats "pack leader" as the
highest attested rank and does not invent a chief executive.

---

## 1. Leadership and ranks

### 1.1 The 2077 chain of command

The Animals are a **confederation of packs**, not an organization. The
organisation infobox reads `headquarters = N/A` and the database entry is
explicit: "The Animals aren't a centralized gang – they're divided into smaller
groups led by independent 'alphas' males or females." `[wiki]` The wiki's
structural section repeats it: "Instead of a single leader, the Animals are
divided between a number of packs, each with a single alpha acting as the Pack
Leader." `[wiki]`

| Name | 2077 role | Character record | Location / influence point | Presence class | Source | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| **Matilda "Sasquatch" K. Rose** | Pack leader (Grand Imperial Mall pack); alpha since 2075. **Not** a faction-wide boss | `Character.q110_animals_boss` | Grand Imperial Mall, Coastview | `story` | Raw `always_loaded_1` registry entry `animals_boss` (phases `arena`, `hall_chat`, spot `#q110_ws_boss_on_arena`); markers `q110_08c_sm_bossfight`, `q110_08d_sm_animals_stand_down`, `sasquatch_perf_spn`; wiki *Matilda K. Rose*; *I Walk the Line* | `[game-data]` `[wiki]` |
| **Denzel "The Brain" Cryer** | Pack leader; Juice-trafficking chief | `Character.ma_hey_spr_11_outpost_miniboss` (appearance `denzel_cryer_default`) | Skyline South Juice den, Wellsprings | `world-activity` | Raw registry entry `enemy_005` (phase `A`, spot `#ma_hey_spr_11_ws_enemy_005`); site 90 `ma_hey_spr_11` (10 units); *SOCA: Living the Big Life*; wiki *Denzel Cryer* | `[game-data]` `[wiki]` |
| **Angelica "Angie" Whelan** | Pack leader (Dogtown); fight arranger and fixer | `Character.mq306_angie` | Dogtown — Montezuma's Throne ring and Damir's clinic | `world-activity` | Raw registry entry `angie` (phases `03_ripper_in`/`03_ripper_out`, spot `#mq306_angie_clinic_in`); areas `{mq306_com_animals_end}` 3; *No Easy Way Out*; wiki *Angelica Whelan* | `[game-data]` `[wiki]` |
| **Valdemar "The Bully"** | Pack leader (book only) | none | Night City, off-map | `off-map` | *The World of Cyberpunk 2077* p. 162; wiki *Animals* Leadership; wiki *Valdemar* | `[wiki]` `[lore]` |
| **Logan Garcia** | Secondary leader; owner of the Tripple Extreme Gym fight club | `Character.wwd_05_target` (inferred) | Tripple Extreme Gym, Arroyo | `world-activity` | Site 378 `sts_pac_wwd_05` (9 units); the site's only `target` slot (`#wwd_05_ws_target`); *Gig: For My Son*; wiki *Logan Garcia*; wiki *Tripple Extreme Gym* | `[inferred]` `[wiki]` |
| **Jesse Sabara** | Secondary leader; Denzel Cryer's second in command | none found | Skyline South Juice den, Wellsprings | `world-activity` | Wiki *Animals Members*; wiki *Jesse Sabara*; *SOCA: Living the Big Life*; no distinct record at site 90 | `[wiki]` `[inferred]` |
| **Martha "Abomination" Ling** | Listed as a secondary leader on the Animals page; her own page says Tyger Claws | none | Night City — poster only | `mentioned` | Wiki *Animals* Leadership; wiki *Martha Ling*; *World of Cyberpunk* p. 162; in-game *Abomination vs Guerriera* poster | `[wiki]` `[lore]` |
| **Rhino** | Fight-circuit champion; trains at the Tripple Gym, fights at the GIM finale | `Character.mq025_rhino` | Tripple Extreme Gym; Grand Imperial Mall ring | `world-activity` | Raw registry entry `rhino` (phases `mq025_rhino_01_pre_fight`, `_02_fight`, `_03_post_fight`, `mq025_rhino_finale_*`); *Beat on the Brat: Rancho Coronado*; wiki *Rhino* | `[game-data]` `[wiki]` |
| **Razor Hugh** | Heavyweight champion; final *Beat on the Brat* opponent | `Character.mq025_razor` | Grand Imperial Mall ring, Coastview | `world-activity` | Raw registry entry `razor` (phases `mq025_razor_01_pre_fight`, `_02_fight`); marker `mq025_mp_08_ring`; wiki *Razor Hugh* | `[game-data]` `[wiki]` |
| **Emmerick Bronson** | Afterlife doorman; Animal member | `Character.Emmerick` | Afterlife, Little China | `ambient` | Raw registry entry `emmerick` (quest phases `q005_emmerick_bouncer`, `q103_afterlife_entrance`); markers `q005_emmerick_bouncer`, `q203_emmerick_front_door`; wiki *Emmerick Bronson*; wiki *Afterlife* | `[game-data]` `[wiki]` |
| **Seamus Sawicki** | Bouncer; led the Militech-intern killing | `Character.ma_std_arr_10_seamus` | Corpo Plaza alley, Bruce Skiv & Union St. | `world-activity` | Raw registry record (single placement); shard baseid `ma_cct_cpz_17_onscreen_01`; shard *Seamus Sawicki and Fred Risch*; site `ma_cct_cpz_17`; wiki *Seamus Sawicki* | `[game-data]` `[wiki]` |
| **Fred Risch** | Bouncer-crew boss; authorises the Militech-intern killing | none | Corpo Plaza (shard only) | `mentioned` | Shard *Seamus Sawicki and Fred Risch* (`ma_cct_cpz_17_onscreen_01`); no record or wiki page | `[wiki]` |

Three facts do the political work here:

1. **Sasquatch is the most visible alpha, not the boss.** She is the only Animal
   with a main-quest role and the only one the wiki dates (alpha since 2075),
   but her authority is her pack's. `[wiki]` `[game-data]` The seed's
   `hq_animals` = Grand Imperial Mall is her *hired* base, not a capital.
   `[game-data]`
2. **The named alphas are not all muscle.** Sasquatch is the bruiser; Denzel is
   "The Brain", a drug lord; Angelica "earned the respect of her people through
   sheer charisma" and runs fight-fixing. `[wiki]` The ideology says brawn; the
   successful leaders are organizers.
3. **The organization has no succession office.** Pack leadership changes by
   challenge and trial by combat "fought until one side completely submitted",
   not by appointment. `[wiki]` There is no faction-level seat to inherit.

### 1.2 Succession history: athletic, local, and mostly unrecorded

There is no dated leadership line because there is no faction-wide leadership.
What the sources give is a set of pack tenures and a few internal killings.

| Period | Centre of power | How the change happened |
| --- | --- | --- |
| 2070s | No central leadership; packs without permanent turf | The gang is described as "an aggressive street-fighting gang without permanent turf" that valued brawn above all. `[wiki]` |
| by 2075 | **Sasquatch's pack** | Sasquatch "has been the alpha animal of her pack since 2075" (*Dossier: Sasquatch*). `[wiki]` How she took it is not recorded. |
| unknown | **Valdemar's pack**, **Denzel Cryer's pack**, **Angelica Whelan's pack** | Pack leaders per the wiki, with no dates and no recorded challenges. Valdemar is book-only. `[wiki]` `[lore]` |
| unknown–2077 | **Logan Garcia's gym**, **Jesse Sabara as Denzel's second**, **Abomination as a secondary leader** | Secondary leaders; Logan owns the Tripple Gym, Jesse is Denzel's lieutenant, Abomination is a book/poster figure. `[wiki]` |
| 2077 | Sasquatch's pack at the Grand Imperial Mall | A **contract**, not a conquest: NetWatch hired the pack to guard its operation against the Voodoo Boys. `[wiki]` |
| 2077 | Larissa "Guerriera" Almeida | The NCART pack's to-do list orders her death: "Guerriera's no more use to us, time to put that bitch out to pasture … concrete boots are in fashion this season." `[wiki]` |
| 2077 | Aaron Waines | A fighter the pack controlled with an implant; he leaves and asks V to have it removed. `[wiki]` |

The pattern is **local and athletic**. A pack changes hands when someone wins a
fight; a liability is removed when the pack decides she is "no more use". There
is no coup, no council, no purge. That is why the design's "internal war with no
single leader" state is the Animals' **default**, not their failure state.

Historical names worth knowing for a succession model: **Valdemar "the Bully"**
(book pack leader), **Martha "Abomination" Ling** (book/poster secondary leader,
sourced as a Tyger Claws member on her own page), and **Kyle J.** (comic member,
deceased 2077). `[wiki]` `[lore]`

### 1.3 Rank structure, initiation and advancement

Lore names only **pack leader (alpha)**, **secondary leader**, and **member**.
Everything else is a combat tier.

1. **Pack leader / alpha.** One per pack, "the biggest and strongest member, the
   alpha male or female." Commands the pack; disputes are settled by trial by
   combat until submission. `[wiki]`
2. **Secondary leader.** A lieutenant/second: Logan Garcia at the gym, Jesse
   Sabara under Denzel, Abomination in the book list. `[wiki]`
3. **Members.** Grunts, bouncers, elites and fighters. The game's records use
   combat tiers — `grunt1/2`, `bouncer1/2`, `elite2/3`, `_officer`,
   `_miniboss` — which describe role, not authority. `[game-data]`
4. **Associates and non-members.** Ripperdocs (Damir Kovac), venue owners (Jack
   Mausser, Adam Ibrahimovic), a coerced netrunner (Rebeca Price), a client
   (Bryce Mosley), and fixers who broker their fights (Coach Fred, El Capitan).
   `[wiki]` `[game-data]`

**Initiation and advancement.** There is no ceremony and no chrome requirement
(contrast Maelstrom). Entry is by proving strength in a fight:

- Rhino's own account: she fought an Animal bouncer to protect her netrunner
  partner, won, and "if you win the fight, you get to start punching for the
  Animals." `[wiki]`
- The body is the uniform: Juice, ultra-testosterone, equine growth hormone,
  artisanal implants, tattoos and hooligan hoods; pack colors and emblems are
  worn openly. `[wiki]`
- Disputes and advancement run through **trial by combat**, not a promotion
  board. `[wiki]`
- Exit is possible but dangerous: Aaron Waines leaves the gang and needs the
  implant removed before he can fight freely; the pack's response to a liability
  (Guerriera) is a kill order. `[wiki]`

The practical consequence: the Animals have a **duel ladder**, not a career
ladder. A player rises by beating an alpha, not by earning favour in an office.

### 1.4 Named members mapped to game data

Unlike Maelstrom, several named Animals **are** in
`data/sites/rosters.json` or in the always-loaded community registry. The
join is exact record names; `Character.Emmerick` and `Character.mq306_angie` are
single unique records.

| Name | Role / note | Character record | Community / site | Location | Presence class | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| Matilda "Sasquatch" K. Rose | Pack leader, GIM | `Character.q110_animals_boss` | `animals_boss` community, phases `arena`/`hall_chat` | Grand Imperial Mall | `story` | `[game-data]` `[wiki]` |
| Denzel "The Brain" Cryer | Pack leader, Juice | `Character.ma_hey_spr_11_outpost_miniboss` | `{ma_hey_spr_11_com}` (10); site 90 | Skyline South Juice den | `world-activity` | `[game-data]` `[wiki]` |
| Jesse Sabara | Denzel's second | none | `{ma_hey_spr_11_com}` (10); site 90 | Skyline South Juice den | `world-activity` | `[wiki]` `[inferred]` |
| Angelica "Angie" Whelan | Pack leader, Dogtown | `Character.mq306_angie` | `{mq306_com_animals_end}` (3); `mq306_com_animals` | Dogtown ring / Damir's clinic | `world-activity` | `[game-data]` `[wiki]` |
| Logan Garcia | Gym owner, secondary leader | `Character.wwd_05_target` (inferred) | `{wwd_05_com_enemies}` (9); site 378 | Tripple Extreme Gym | `world-activity` | `[inferred]` `[wiki]` |
| Rhino | Fight champion | `Character.mq025_rhino` | `mq025` fight communities | Tripple Gym; GIM ring | `world-activity` | `[game-data]` `[wiki]` |
| Razor Hugh | Heavyweight champion | `Character.mq025_razor` | `mq025` finale community | GIM ring | `world-activity` | `[game-data]` `[wiki]` |
| Emmerick Bronson | Afterlife doorman | `Character.Emmerick` | Afterlife entrance phases | Afterlife | `ambient` | `[game-data]` `[wiki]` |
| Seamus Sawicki | Bouncer, Militech-intern killing | `Character.ma_std_arr_10_seamus` | one placement at `ma_std_arr_10`; shard at `ma_cct_cpz_17` | Corpo Plaza alley | `world-activity` | `[game-data]` `[wiki]` |
| Fred Risch | Bouncer-crew boss | none | shard only | Corpo Plaza | `mentioned` | `[wiki]` |
| Aaron Waines | Former member; fixed fighter | `Character.mq306_aaron` | `{mq306_com_aaron}` variants | Dogtown | `world-activity` | `[game-data]` `[wiki]` |
| Damir Kovac | Ripperdoc; implants the control chip | `Character.mq306_damir` | `{mq306_com_damir}` community | Dogtown clinic | `world-activity` | `[game-data]` `[wiki]` |
| Larissa "Guerriera" Almeida | Fighter; ordered killed by her own pack | none | shard + poster | GIM pier / Coastview | `mentioned` | `[wiki]` |
| Keenan | Named Animal, West Wind gang-watch scene | `Character.ma_pac_wwd_01_animal_keenan` | `{ma_pac_wwd_01_com}` (4) | West Wind Estate | `world-activity` | `[game-data]` |
| Sheila | Named Animal, West Wind gang-watch scene | `Character.ma_pac_wwd_01_animal_sheila` | `{ma_pac_wwd_01_com}` (4) | West Wind Estate | `world-activity` | `[game-data]` |
| Paul Roberts | Named Animal grunt | `Character.ma_pac_cvi_05_animals_grunt1_ranged1_pulsar_mb_Paul_Roberts` | `{ma_pac_cvi_05_com}` (7) | Coastview | `world-activity` | `[game-data]` |
| Adam Giles | Named Animal grunt | `Character.ma_wbr_jpn_19_adam_giles` | `{ma_wbr_jpn_19_com}` (5) | JapanTown | `world-activity` | `[game-data]` |
| Rudi | Juice cook ("blind_rudi"), lab unlocated | none | computer message only | — | `mentioned` | `[wiki]` |
| Hyacinth | Juice logistics (NCART computer message) | none | computer message only | Unfinished NCART Station | `mentioned` | `[wiki]` |
| Kade; waxxy | Named in NCART computer messages | none | computer message only | Unfinished NCART Station | `mentioned` | `[wiki]` |
| Valdemar "The Bully" | Book pack leader | none | — | — | `off-map` | `[wiki]` `[lore]` |
| Martha "Abomination" Ling | Book/poster secondary leader (Tyger per own page) | none | — | — | `mentioned` | `[wiki]` `[lore]` |
| Kyle J. | Comic member, deceased 2077 | none | — | — | `historical` | `[wiki]` `[lore]` |

Data cautions:

- **`Character.wwd_05_target` is Logan Garcia by elimination.** Site 378 has one
  `target` slot (`#wwd_05_ws_target`) and one gig target, Logan. There is no
  named record; the mapping is `[inferred]`. Verify in-game.
- **Jesse Sabara has no distinct record.** Denzel occupies the site's only
  `*_outpost_miniboss` slot; Jesse is one of the generic `spr_animals_*`
  entries. Do not assign him a record without a check.
- **Seamus's record and shard disagree on place.** The record
  `Character.ma_std_arr_10_seamus` is placed once in a 6th Street community at
  Arroyo `ma_std_arr_10`; his shard's `baseid` is `ma_cct_cpz_17_onscreen_01`
  (Corpo Plaza). The shard is the better location evidence; the record is a
  reuse/mismatch, flagged in §5.
- **Emmerick's phases are all quest phases.** He is at the Afterlife door in
  free roam per the wiki, but the registry only has `q005_emmerick_bouncer` and
  `q103_afterlife_entrance` phases. Ambient is a behaviour judgement, not a
  record fact.

### 1.5 What the game actually spawns (campaign disabled)

This is the part other systems must not assume.

**`ambient` — persists in free roam.**
- **Emmerick Bronson** at the Afterlife door. The wiki says he refuses entry
  before *The Heist* and comments when V returns, which is free-roam behaviour.
  His record's phases are quest phases, so this needs an in-game check. `[wiki]`
  `[game-data]`

**`world-activity` — free-roam content, activity-gated.**
- **Denzel Cryer, Jesse Sabara** (*SOCA: Living the Big Life*, `baseid =
  ma_hey_spr_11`). `[game-data]` `[wiki]`
- **Angelica Whelan** (*No Easy Way Out*, `baseid = mq306`). `[game-data]` `[wiki]`
- **Logan Garcia** (*Gig: For My Son*, `baseid = sts_pac_wwd_05`). `[inferred]`
  `[wiki]`
- **Rhino** (*Beat on the Brat: Rancho Coronado* / finale). `[game-data]` `[wiki]`
- **Razor Hugh** (*Beat on the Brat* finale at the GIM ring). `[game-data]` `[wiki]`
- **Seamus Sawicki** (Assault in Progress, Corpo Plaza). `[game-data]` `[wiki]`
- **Keenan, Sheila, Paul Roberts, Adam Giles** (named scanner-hustle bosses and
  grunts). `[game-data]`

**`story` — gated by the main job chain; do not expect them in free roam with
the campaign disabled.**
- **Sasquatch** and the GIM pack (*I Walk the Line*). Her community's phases are
  `arena` and `hall_chat`, and the markers are quest markers. `[game-data]` `[wiki]`

**`off-map` — alive in lore, never spawned.**
- **Valdemar "the Bully"** (book only). `[wiki]` `[lore]`

**`mentioned` — named only in shards, dialogue or a poster.**
- **Fred Risch** (the bouncer-crew boss in Seamus's shard), **Larissa
  "Guerriera" Almeida** (poster and shard), **Rudi**, **Hyacinth**, **Kade**,
  **waxxy** (computer messages), **Martha "Abomination" Ling** (poster). `[wiki]`

**`historical` — not in 2077.**
- **Kyle J.** (comic, deceased). `[wiki]` `[lore]`

Caveat: "campaign disabled" may also suppress gigs and scanner hustles. The
Animals are the worst case in the game for this: almost every named Animal is
quest- or activity-gated. The `world-activity` rows are the best reuse
candidates; the `story`, `off-map` and `mentioned` rows are the ones to replace
with simulation agents.

### 1.6 Player-path hooks

| Person | Join under | Climb past | Ally with | Remove |
| --- | --- | --- | --- | --- |
| **Sasquatch** | The GIM contract pack: corporate security work, the NetWatch client, the mall | She is the alpha; climbing past her means beating her in a fight or breaking the contract | Bryce Mosley (the client), the mall garrison, a NetWatch channel | Killing her ends the contract pack and the GIM tenure; the survivors hold a grudge and the Scavs move in |
| **Denzel Cryer** | The Juice business: manufacture, trafficking, pharmacy raids | He is a pack leader; a player under him climbs by controlling supply, then the pack | Jesse Sabara, Rudi (the cook), Juice customers | Removing Denzel and Jesse decapitates the Juice distribution node; the NCPD hustle is exactly that |
| **Logan Garcia** | The fight club: gate fees, the melee vendor, fight promotion | He owns the gym; climbing past him means taking the venue | Rhino, the vendor, the fight crowd | Killing Logan leaves the gym ownerless; Rhino and the circuit continue without a promoter |
| **Angelica Whelan** | The Dogtown fight-fixing ring: arrange bouts, control fighters | She is a pack leader and the broker; a player under her is one more asset | Damir Kovac (the ripperdoc), the Dogtown venues, the spectators | Removing her frees Aaron Waines and ends the fight-fixing operation |
| **Rhino** | The fight circuit; a pure duel path | She is a champion, not a leader; beating her earns respect, not command | The athlete wing, the Tripple Gym crowd | Removing Rhino removes the faction's most honest fighter, not a political actor |
| **The door economy (no leader)** | A bouncer/bodyguard contract at a club or corp | No ladder: each door has a site boss; taking one door does not take the network | Venue owners and corporate clients | Removing one site boss closes one door; the rest of the network is unaffected |
| **The NCART cell ("S")** | The contraband/expansion crew: lidocaine, transport hijacking, turf grabs | The author is unidentified; a player can take the cell by taking its den | The Juice cook, the NCART crew | Removing the cell ends the expansion agenda and the contraband staging, not the faction |

The design consequence: the Animals have **no single ladder and no faction
seat**, only a duel ladder and a set of contracts. Backing one pack makes the
others neutral at best; beating one alpha makes that pack yours and leaves the
rest untouched. This is the purest "Tribe" path in the game and it should not be
flattened into a normal gang hierarchy.

---

## 2. Internal political factions

### 2.1 The blocs

"Members" counts are **presence proxies** from `dist/extract/areas.jsonl` and
site rosters, not membership rolls. Several communities are overlapping quest
phases of one site, so do not sum them.

| Bloc | Leader(s) | What it wants | Presence / members hint | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- |
| **Sasquatch's NetWatch contract pack (GIM)** | Matilda "Sasquatch" K. Rose | Hold the mall, protect NetWatch agent Bryce Mosley, keep the Voodoo Boys out, earn the security contract | 55 Animals across six `q110_com_mall_*` communities; site 61; 8 spawn points | *I Walk the Line*; `q110` markers; wiki *Animals* History and *Grand Imperial Mall* | `[game-data]` `[wiki]` |
| **Denzel Cryer's Juice cartel (Wellsprings)** | Denzel "The Brain" Cryer; Jesse Sabara as second | Manufacture and distribute Juice; raid drug stores, chemical transports and pharma for inputs | Site 90, 10 units; `{ma_hey_spr_11_com}` 10; Jesse, Rudi (cook) | *SOCA: Living the Big Life*; NCART *DELIVERY!!!*; wiki *Denzel Cryer*, *Jesse Sabara*, *Juice* | `[game-data]` `[wiki]` |
| **Logan Garcia's fight club (Tripple Gym)** | Logan Garcia | Run the paint-vat fight ring, gate fees, the melee vendor and fight tourism; keep the gym's reputation | Site 378, 9 units; `{wwd_05_com_enemies}` 9; Rhino trains here | *Gig: For My Son*; *Beat on the Brat: Rancho Coronado*; wiki *Tripple Extreme Gym* | `[game-data]` `[wiki]` |
| **Angelica Whelan's Dogtown fight-fixing ring** | Angelica "Angie" Whelan | Arrange and fix fights, control boxers with implants, wheel in cash | `{mq306_com_animals_end}` 3 (Angie + two); ripperdoc Damir Kovac; Aaron Waines as the fixed fighter | *No Easy Way Out*; *Damir Kovac/Computers*; areas `mq306`; wiki *Angelica Whelan* | `[game-data]` `[wiki]` |
| **The NCART expansion cell** | "S" (unidentified) | Seize the stadium parking lot, monitor Monica Steiner's nomad outreach, collect on the Valentino generator deal, dispose of Guerriera | Site 377, 13 units; `{cvi_02_combat_com}` 13 | NCART computers *Upcoming work*, *DELIVERY!!!*, *brandon frost*; *Gig: Two Wrongs Makes Us Right* | `[game-data]` `[wiki]` |
| **The door economy (bouncer/bodyguard contracts)** | No single leader; Fred Risch leads one crew | Sell muscle to clubs, corporates and venues; keep the contracts | 7th Hell 9 (gig variant), Empathy 11 (gig variant), Data Inc. 4, Afterlife 1 (Emmerick), Corpo Plaza 4 | *A Lack of Empathy*, *An Inconvenient Killer*, *Hot Merchandise*; wiki *Animals* database entry | `[game-data]` `[wiki]` |
| **The fight circuit / athlete wing** | Rhino (de facto) | Championships, prize money, sponsorship, street cred | Rhino, Razor Hugh, Larissa Almeida (dead), Abomination (book/poster); GIM ring, Tripple Gym | *Beat on the Brat*; wiki *Rhino*, *Razor Hugh*; posters; Larissa shard | `[game-data]` `[wiki]` `[lore]` |
| **The purist hormone current vs chrome pragmatists** | No leader | Peak human body through Juice and surgery vs accept corporate prototype chrome and hired netrunning | Diffuse: Juice users vs Razor's prototype implants vs the Data Inc. netrunning den | Wiki *Animals* overview; wiki *Razor Hugh*; Data Inc. computers | `[wiki]` `[lore]` |
| **Valdemar's pack / historical alphas** | Valdemar "The Bully" | Unknown; book only | No 2077 record | *World of Cyberpunk* p. 162; wiki *Animals* Leadership | `[wiki]` `[lore]` |

### 2.2 No alpha of alphas

This is the structural fact that separates the Animals from every other gang in
this series.

- There is no headquarters: the infobox reads `headquarters = N/A`. `[wiki]`
- There is no leader rank above alpha: the wiki lists four pack leaders and
  three secondary leaders, and says each pack has "a single alpha". `[wiki]`
- The database entry calls them "not a centralized gang". `[wiki]`
- The seed's `hq_animals` is the Grand Imperial Mall, which is Sasquatch's
  **hired** base; the wiki says the Animals held it "formerly" and the Scavengers
  stripped it after they left. `[game-data]` `[wiki]`

For the simulation this is an asset, not a gap. The design already has a state
for "a faction in internal war with no single leader". The Animals should start
in a softened version of that state: multiple legitimate alphas, no claimant to
a faction-wide seat, and no rule that says who commands when packs disagree.
Any attempt to give them a boss invents a rank the lore does not have.

### 2.3 The contract pack vs the street packs

The cleanest policy axis inside the faction is **contract discipline vs
predation**.

- The GIM pack takes corporate money and hides a client's presence. That is
  disciplined, quiet, professional work: guard a mall, keep the Voodoo Boys out,
  do not start a war you were not hired for. `[wiki]`
- The door economy sells the same discipline to clubs and stores: 7th Hell,
  Empathy, Data Inc., the Afterlife. `[wiki]` `[game-data]`
- The street packs do the opposite: they raid transports and pharmacies, sell
  stolen Militech guns, hijack cargo, and run the Juice trade. `[wiki]`
  `[game-data]`

Both are the same business — muscle — but one is **sold** and one is **taken**.
A leader who takes too many corporate contracts loses the raider identity and
the Juice inputs; a leader who raids too openly loses the clients. This is the
Animals' version of Royce vs Brick, except it is not one coup: it repeats in
every pack.

### 2.4 The Juice cartel and the supply chain

Juice is the faction's signature product and its recruitment engine. It is also
a dependency:

- Denzel Cryer "leads a subgroup of the so-called Animals gang, known to traffic
  in the illegal supplement commonly called 'juice'." `[wiki]`
- The NCART pack receives "a big delivery of lido … from those chromed
  cocksuckers" (Maelstrom) and cooks it. `[wiki]`
- The `Two Wrongs` gig says the same lidocaine was "stolen already once before
  from Maelstrom"; Maelstrom uses it for initiation rites, the Animals for
  Juice. `[wiki]`
- Side effects are severe and documented in-game (*Juice – Top 8 Dangers*):
  gynecomastia, balding, acne, kidney and liver failure, asymmetric muscle
  growth. `[wiki]`
- The cook is a named but unlocated "Rudi"; the lab is not a seeded site.
  `[wiki]`

Politically, Juice is a **loyalty technology**: it makes bodies, and bodies are
the gang's product. The pack that controls supply controls recruitment. The
supply crosses enemy lines (Maelstrom), which is why the Maelstrom relationship
is hostile *and* commercial at the same time.

### 2.5 The fight economy and the control chip

The fight economy is the faction's public face and its sharpest internal fault
line. Four positions sit inside it:

1. **The promoter.** Logan Garcia owns the Tripple Gym, charges €$3,800 at the
   gate, runs the paint-vat pit and a melee vendor. `[wiki]`
2. **The fixer.** Angelica Whelan "arrang[es] and fix[es] fights and wheel[s] in
   cash"; she had her ripperdoc implant a remote failsafe in Aaron Waines so she
   could drop him in predetermined rounds. `[wiki]`
3. **The purist fighter.** Rhino fights "for fun and to make a name", boasts she
   has never lost, and is the only *Beat on the Brat* opponent who fights V for
   free. `[wiki]`
4. **The sellout.** Razor Hugh has "elite corpo sponsors and prototype
   implants", calls himself a corporate test bed, and is the faction's
   three-time heavyweight champion. `[wiki]`

That is a real internal conflict: **sport vs fix, purism vs sponsorship,
prestige vs cash**. Angelica's chip is the extreme case; Razor's prototype chrome
is the respectable one; Rhino's free fight is the ideological one. A simulation
can treat these as three positions inside the athlete wing, not as one bloc.

### 2.6 The NCART expansion cell and internal discipline

The Unfinished NCART Station is the only place where an Animal pack writes down
a political agenda. Its computer holds three documents:

- **"Upcoming work"** (signed "S"): seize and secure the stadium parking lot;
  check whether Monica Steiner is really looking to nomads for help; fix the
  generators bought from the Valentinos ("incompatible transistors?"); and kill
  Guerriera "outside our zone". `[wiki]`
- **"DELIVERY!!!"**: a lidocaine delivery from Maelstrom, "cook today", "let the
  boss know everything's a go". `[wiki]`
- **"brandon frost"**: a revenge order against the Maelstrom member who buried
  Animals alive in concrete and sold the XBD; "I WANT HIM ALIVE". `[wiki]`

Two things follow:

1. **A pack can act as a political actor.** The NCART cell is expansionist,
   tracks a client's revenge contract, manages a supplier dispute, and orders an
   internal execution — all without a faction-level leader.
2. **Internal discipline is lethal and administrative.** Guerriera won a fight,
   the Valentinos turned hostile towards her ("after you won that fight, Tinos
   aren't big fans of you"), she became a liability, and her own pack ordered her
   killed. That is the faction's justice: not a trial, a to-do list.

The author "S" is not identified. Do not assume Sasquatch; the NCART cell is a
different pack and the initial is the only evidence.

### 2.7 The door economy and non-member power centres

The Animals' most valuable political asset is other people's property:

- **Venue owners** — Jack Mausser (7th Hell), Adam Ibrahimovic (Empathy), Rebeca
  Price (Data Inc.) hire Animal muscle. Mausser bought the club and "hired the
  Animals for protection"; Ibrahimovic "hired Animals as bouncers" after seizing
  Empathy; Rebeca staffs Data Inc. with Animals posing as businessmen. `[wiki]`
- **A ripperdoc** — Damir Kovac is "their ripperdoc", the man who implants the
  control chip. He is an asset with technical leverage, not a member. `[wiki]`
- **A coerced netrunner** — Rebeca Price runs the Data Inc. netrunning den "under
  duress rather than her own initiative." The gang's only netrunning capability
  is borrowed and unwilling. `[wiki]`
- **A corporate client** — Bryce Mosley (NetWatch) is the GIM pack's principal.
  He is not a member and cannot be ordered; he is the reason the pack is in
  Pacifica. `[wiki]`
- **A fight broker** — Coach Fred feeds the Dogtown boxing scene and gives the
  *No Easy Way Out* job. `[wiki]`

These are the faction's **non-member power centres**: they can host the gang,
pay it, refuse it, or defect. Removing one hurts a revenue line; removing a pack
leader hurts a pack. The two are not the same.

### 2.8 What could drive internal conflict in a simulation

Evidence-based drivers, in rough order of plausibility:

1. **No alpha of alphas.** Any pack can claim primacy; no rule says who wins.
   Beating an alpha is the only legitimate claim, and it is local.
2. **Contract vs predation.** Corporate security work and street raiding pull in
   opposite directions. A pack that takes NetWatch money cannot also run a
   Militech theft ring without exposure.
3. **Fight-fixing vs the fighter's code.** Angelica's control chip, Logan's
   brutal promotions and Rhino's free fights are incompatible models of the same
   sport.
4. **Purism vs sponsorship.** Razor's prototype chrome and corporate sponsors
   contradict the anti-cyberware ethos; the Data Inc. netrunning den contradicts
   the anti-tech ethos. Purists can call either a betrayal.
5. **Juice supply.** A pack that loses its lidocaine source loses recruitment;
   a pack that controls the cook controls the bodies. The Maelstrom channel is
   both necessary and hostile.
6. **Disposal of liabilities.** Guerriera's kill order and Aaron's implant show
   the faction's answer to a fighter who becomes inconvenient. Every ambitious
   member is a potential liability.
7. **Expansion into others' turf.** The NCART list names the stadium parking lot
   (Dogtown/Barghest), the Valentino shop (the Glen), and the nomad question.
   Each is a way to start a war the faction cannot centrally authorise.
8. **No intelligence arm.** The gang cannot see NCPD APBs, NetWatch operations or
   fixer contracts coming; the only netrunner is coerced. A pack that is surprised
   blames the alpha who missed it.
9. **The star athlete.** Razor is a corporate asset and a gang member; his
   sponsorships buy the gang prestige and expose it to corpo control. A leader
   who leans on him looks strong; a leader who loses him looks weak.
10. **The community of the body.** Juice users are loyal and unstable; the
    side-effects are visible and disabling. A pack that pushes Juice too hard
    loses members to the drug as surely as to a rival.

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
and `Affiliation.hpp` is identity only (Animals = 2 in that enum; the
`data/factions.json` id is 6). Every stance below is judged from quests, wiki and
spatial adjacency, which is why each row carries a tag and why the neutral rows
are placeholders, not claims of friendship.

### 3.2 The matrix

| Faction | Code | Stance | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| Tyger Claws | `tyger_claws` | `neutral` | No attested conflict. Jig-Jig Street lists Animals among its gangs and an Assault in Progress on Salinas St (site 284, 5 Animals) sits in Tyger JapanTown; the location doc's "rival" is adjacency, not evidence. No Animals–Tyger community co-occurrence beyond the generic `sa_ep1_113` brawl `[game-data]` `[wiki]` `[inferred]` | `game-data+inferred` |
| Valentinos | `valentinos` | `trade` | The NCART to-do list: "generators from the tinos still don't work (incompatible transistors?) Head to their shop in the Glen and sort it" — a purchased-goods dispute. Larissa Almeida's shard: after she won a fight, "Tinos aren't big fans of you". No violence attested; the Valentinos doc calls the pair neutral `[wiki]` `[game-data]` | `wiki` |
| Arasaka | `arasaka` | `neutral` | No attested interaction; the Arasaka politics doc also records neutral. Animals sell bodyguards but no Arasaka contract is attested `[wiki]` `[inferred]` | `wiki+inferred` |
| Militech | `militech` | `hostile` | A recorded kill order on Militech interns (Seamus Sawicki shard); Data Inc. sells hacked, previously stolen Militech guns to international clients (Data Inc. "WATCH OUT" list); the Data Inc. office says it "intercepted the militech arms shipments … at the chop shop"; Rogue's gig frames Militech as about to send troops into the city `[game-data]` `[wiki]` | `game-data+wiki` |
| Kang Tao | `kang_tao` | `neutral` | No attested interaction; Sasquatch carries a Kang Tao A-22B Chao, an equipment choice, not a relationship `[wiki]` `[inferred]` | `wiki+inferred` |
| Biotechnica | `biotechnica` | `neutral` | No attested interaction; the Animals brew their own hormones (Juice, ultra-testosterone, equine growth hormone) rather than buy Biotechnica product `[wiki]` `[inferred]` | `wiki+inferred` |
| Petrochem | `petrochem` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Barghest | `barghest` | `neutral` | Angelica Whelan's Dogtown fight night places 3 Animals at `{mq306_com_animals_end}` with 2 Barghest in the spectator crowd `{mq306_com_spectators}`; tolerated co-presence in Barghest turf, no deal or conflict attested. The Barghest doc also records neutral `[game-data]` `[inferred]` | `game-data+inferred` |
| 6th Street | `sixth_street` | `neutral` | Co-residents in Santo Domingo: the Tripple Gym sits in 6th Street turf and the 6th Street doc records neutral. No attested conflict or deal `[game-data]` `[inferred]` | `game-data+inferred` |
| Aldecaldos | `aldecaldos` | `neutral` | No attested interaction. The NCART to-do list notes Monica Steiner is "looking to nomads for help" over her son's death — a threat the Animals are tracking, not a nomad relationship `[wiki]` `[inferred]` | `wiki+inferred` |
| Wraiths | `wraiths` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| The Mox | `the_mox` | `neutral` | No attested interaction; both work the club economy but no shared venue, deal or conflict is attested `[inferred]` | `inferred` |
| Maelstrom | `maelstrom` | `hostile` | Brandon Frost buried several Animals alive in concrete and sold the XBD; the NCART pack's computer orders "I WANT HIM ALIVE". The same pack buys/receives stolen lidocaine "from those chromed cocksuckers" for Juice — hostility with a supply channel `[game-data]` `[wiki]` | `game-data+wiki` |
| Voodoo Boys | `voodoo_boys` | `hostile` | NetWatch hired Sasquatch's pack to guard agent Bryce Mosley at the GIM and hide him from the VDB; the VDB send V to wipe the pack in *I Walk the Line*; the GIM is in VDB-controlled west Pacifica. The VDB doc records the same hostile stance `[game-data]` `[wiki]` | `game-data+wiki` |
| NCPD | `ncpd` | `hostile` | Standing target: the NCPD APB names Denzel Cryer and his Juice ring (*SOCA: Living the Big Life*); Assault in Progress and scanner-hustle sites at Corpo Plaza, JapanTown, Little China and Coastview; gang-watch activities across the map `[game-data]` `[wiki]` | `game-data+wiki` |
| Night Corp | `night_corp` | `neutral` | No attested interaction; a corp, not a turf actor `[inferred]` | `inferred` |
| City Council | `city_council` | `neutral` | No attested interaction; no purchased channel found `[inferred]` | `inferred` |
| Scavengers | `scavengers` | `trade` | Animal bodyguards (`Character.q303_paradise_animal_guard` ×2) flank the Scav boss Tzar at the Black Sapphire party — a transactional muscle contract. Scavs later moved into the GIM after the Animals left, which is succession, not a feud. No attested Animals–Scav fight `[game-data]` `[wiki]` | `game-data+wiki` |
| Regina Jones | `fixer_regina` | `neutral` | No Animals-specific gig or lore link found; her gigs are Watson `[inferred]` | `inferred` |
| Wakako Okada | `fixer_wakako` | `neutral` | No Animals-specific gig or lore link found `[inferred]` | `inferred` |
| Sebastian Ibarra (Padre) | `fixer_padre` | `neutral` | No Animals-specific gig or lore link found `[inferred]` | `inferred` |
| Muamar Reyes (El Capitán) | `fixer_el_capitan` | `hostile` | El Capitán takes Monica Steiner's contract and sends V to neutralise Logan Garcia at the Tripple Gym (*Gig: For My Son*); the NCART to-do list tracks her outreach to the nomads `[game-data]` `[wiki]` | `game-data+wiki` |
| Dakota Smith | `fixer_dakota` | `neutral` | No Animals-specific gig or lore link found `[inferred]` | `inferred` |
| Dino Dinovic | `fixer_dino` | `hostile` | Dino gives *An Inconvenient Killer* (neutralise Jack Mausser inside Animal-guarded 7th Hell) and *A Lack of Empathy* (upload a virus to Animal-guarded Empathy's subnet) `[game-data]` `[wiki]` | `game-data+wiki` |
| Rogue Amendiares | `fixer_rogue` | `hostile` | Rogue gives *Hot Merchandise*: neutralise Rebeca Price inside the Animal-staffed Data Inc. store, to stop stolen Militech guns drawing a corporate crackdown `[game-data]` `[wiki]` | `game-data+wiki` |
| Mr. Hands | `fixer_mr_hands` | `hostile` | Mr. Hands gives *Two Wrongs Makes Us Right*: steal the Animals' lidocaine van from the NCART den and resell it to ripperdocs `[game-data]` `[wiki]` | `game-data+wiki` |
| Afterlife | `afterlife` | `client` | Emmerick Bronson, an Animal, is the Afterlife's doorman (`Character.Emmerick`; markers `q005_emmerick_bouncer`, `q203_emmerick_front_door`); the bar hires the gang's muscle `[game-data]` `[wiki]` | `game-data+wiki` |
| NetWatch | `netwatch` | `client` | NetWatch hired Sasquatch's pack as private security for agent Bryce Mosley at the GIM, using the Animals as its proxy against the Voodoo Boys. The contract is with the pack, not the faction `[game-data]` `[wiki]` | `game-data+wiki` |
| NUSA | `nusa` | `neutral` | No direct NUSA–Animals interaction; the client is NetWatch, an international agency, not the NUSA state `[inferred]` | `inferred` |

### 3.3 Actors outside `data/factions.json`

Real relationships with no faction code, so prose only:

- **Bryce Mosley** — NetWatch agent and the GIM pack's principal; Sasquatch's
  pack guards him. `[wiki]`
- **Fred Risch** — the bouncer-crew boss who authorises the Militech-intern
  killing in Seamus's shard. No record, no page. `[wiki]`
- **Damir Kovac** — the Animals' ripperdoc; implants Angelica's control chip in
  Aaron Waines. An asset with technical leverage. `[wiki]`
- **Aaron Waines** — former Animal, fixed fighter, and the reason the control
  chip is known. `[wiki]`
- **Larissa "Guerriera" Almeida** — Animal fighter ordered killed by her own
  pack, after a win that made the Valentinos hostile. `[wiki]`
- **Tzar** — Scav boss who hires Animal bodyguards at the Black Sapphire. `[wiki]`
  `[game-data]`
- **Brandon Frost** — Maelstrom member who buried Animals alive; the NCART pack
  wants him alive. `[wiki]`
- **Jack Mausser** — ex-merc owner of 7th Hell who hires the Animals for
  protection. `[wiki]`
- **Adam Ibrahimovic / Larry Fanghorn** — Empathy's co-owners; Adam seized the
  club and hired the Animals as bouncers. `[wiki]`
- **Rebeca Price** — coerced netrunner at Data Inc.; not a member. `[wiki]`
- **Coach Fred** — boxing coach and the *No Easy Way Out* quest giver. `[wiki]`
- **Monica Steiner / Lenny Steiner** — the mother and son behind *For My Son*;
  the NCART pack tracks Monica's nomad outreach. `[wiki]`
- **Rudi, Hyacinth, Kade, waxxy, "S"** — named only in Animal computer messages;
  the Juice cook, the logger, the NCART pack. `[wiki]`
- **Razor's unnamed manager and corporate sponsors** — the money behind the
  champion; a corporate channel, not a faction. `[wiki]`
- **Kyle J. and Oriona** — comic characters; Kyle is an Animal, Oriona is not.
  No 2077 presence. `[wiki]` `[lore]`

### 3.4 Guarantor assessment

The design question: if a player founds a gang, which factions would guarantee
the Animals' support, and which would the Animals guarantee?

- **No `ally` and no `patron` row.** Nothing in the lore protects or funds the
  Animals. Their two `client` rows (NetWatch, Afterlife) are *they* working for
  someone else, not someone working for them.
- **The Animals are a hired guarantor, not a loyal one.** A player-founded gang
  can buy Animal muscle as security, exactly as NetWatch, Afterlife, Mausser and
  Ibrahimovic do. The guarantee lasts as long as the contract and no longer.
  Their own alphas kill their own fighters; their word is only as good as the
  next fight.
- **They are a poor political guarantor.** The matrix has no ally, no patron and
  no diplomatic channel. Their political capital is four things: muscle, the fight
  circuit, the Juice supply, and pack turf. Three are private and one is
  contested.
- **They are a likely aggressor.** The NCART list names a stadium parking lot, a
  Valentino shop and a nomad question; the street packs raid transports and
  pharmacies. A player who takes a Coastview or Wellsprings point should expect
  the Animals to pre-empt rather than negotiate.
- **Plausible guarantors for a player-founded gang** are transactional: hire
  Animal muscle (a security contract), share an enemy (VDB, Militech, Maelstrom,
  NCPD), or supply Juice inputs. Not loyalty, not territory, not diplomacy.
- **The Animals as a guarantor for a player**: a player who wins one pack gets
  that pack's muscle and venue; the other packs remain neutral or hostile. The
  faction cannot guarantee anything it does not centrally control — and it
  centrally controls nothing.

---

## 4. Pillar notes

Design claims from `docs/design/gameplay-systems.md`: the Animals are a **Tribe**
(archetype strength **Culture**, weakness **Espionage**); faction strength
**Military**, weakness **Technology**.

| Pillar | Design claim | Lore verdict | Evidence |
| --- | --- | --- | --- |
| Culture (archetype strength) | A Tribe binds through culture | **Strongly supported, but pack-local.** Pack colors and emblems, "intensely proud of their group identity", the body as uniform, alpha rule, trial by combat, Juice as a shared ritual. The culture binds a pack and repels outsiders; there is no faction-wide identity beyond "brawn". | Wiki *Animals* overview, philosophy and Behind the Scenes; database entry; trial by combat `[wiki]` |
| Espionage (archetype weakness) | The gang cannot do intelligence | **Strongly supported.** No netrunners of its own; the only netrunning den is staffed by a coerced outsider (Rebeca Price) and is penetrated by Rogue's gig. The NCART cell learns of Monica Steiner second-hand; NCPD APBs name their leaders; no counter-intelligence, no blackmail, no information business. | Data Inc. computers; *Hot Merchandise*; NCART *Upcoming work*; NCPD dispatcher `[game-data]` `[wiki]` |
| Military (faction strength) | The gang is militarily strong | **Supported tactically, not operationally.** Elite heavy-melee brawlers, bouncers and cage champions; heavy weapons (Carnage, Burya, Sasquatch's hammer); they hold a mall against a VDB-commissioned infiltration and sell corporate security. But no armour, air, drones or force projection, and one merc can beat the GIM pack. | Enemy records; *I Walk the Line*; wiki *Animals* sources of income `[game-data]` `[wiki]` |
| Technology (faction weakness) | The gang is technologically weak | **Strongly supported.** They "eschew traditional cyberware" for home-brewed hormones and artisanal implants; only pain editors, subdermal armour, injectors and reinforced joints. The exceptions — Razor's prototype chrome, the Data Inc. netrunning den, Sasquatch's Kang Tao rifle — are bought or borrowed, not owned. | Wiki *Animals* overview; wiki *Razor Hugh*; Data Inc. computers `[wiki]` `[game-data]` |
| Overall fit | The pillars fit the faction's identity | **Excellent; the Animals are the purest Tribe in the game.** Keep Culture strong, Espionage weak, Military tactically strong, Technology weak. Model the pack, not the faction. | Synthesis `[inferred]` |

Design cautions, not redesigns:

- **Do not give the Animals a faction-wide leader.** Pack leaders are the top
  rank. The design's "internal war with no single leader" is their normal state,
  not a failure state.
- **Model packs as blocs, not departments.** A pack owns its turf, its contract
  and its fighters. Losing a pack leader decapitates that pack; it does not
  change the faction.
- **The duel is the succession mechanic.** A player rises by beating an alpha,
  not by earning favour. That is a distinct advancement path from the other
  gangs and should be preserved.
- **Do not model them as poor.** They have security contracts, fight revenue,
  Juice, arms and smuggling. Their weakness is legitimacy and intelligence, not
  turnover.
- **Do not model them as a standing army.** With the campaign disabled, almost
  every named Animal is quest- or activity-gated. The mod must spawn them.
- **Juice is a recruitment and dependency mechanic**, not just a `drugs` revenue
  code: it makes bodies, and bodies are the product.

---

## 5. Gaps and uncertainties

1. **There is no faction-wide leader, and none should be invented.** The wiki
   lists pack leaders and secondary leaders only; the database entry says "not a
   centralized gang". Sasquatch is the most visible alpha, not the boss. Any
   model with a single Animal leader contradicts the sources.
2. **Martha "Abomination" Ling is a source conflict.** The Animals page lists
   her as a secondary leader; her own page says she is a Tyger Claws member, and
   the citation is the same *World of Cyberpunk* page. She appears only on a
   poster. Treated as `mentioned` and flagged, not as an Animal officer.
3. **Valdemar "the Bully" is book-only.** *World of Cyberpunk* p. 162 is the only
   source; there is no record, marker or wiki page beyond the stub. `off-map`.
4. **Jesse Sabara has no distinct record.** Denzel occupies the site's only
   `*_outpost_miniboss` slot; Jesse is one of the generic `spr_animals_*`
   entries. Do not assign him a record without an in-game check.
5. **Logan Garcia's record is a one-record deduction.** `Character.wwd_05_target`
   is the only `target` slot at `sts_pac_wwd_05`; the gig target is Logan. Tagged
   `[inferred]`.
6. **Seamus Sawicki's record and shard disagree on place.** The record
   `Character.ma_std_arr_10_seamus` is placed once in a 6th Street community at
   Arroyo `ma_std_arr_10`; the shard's `baseid` is `ma_cct_cpz_17_onscreen_01`
   (Corpo Plaza). The shard is the better location evidence; the record is a
   reuse/mismatch. Verify in-game.
7. **Emmerick's ambient status is a behaviour judgement.** His registry phases
   are all quest phases (`q005_emmerick_bouncer`, `q103_afterlife_entrance`), but
   the wiki attests he refuses entry before *The Heist* and comments on V's
   return. Re-check with the campaign disabled.
8. **7th Hell and Empathy are empty outside their gigs.** The wiki says 7th Hell
   has no Animals before or after *An Inconvenient Killer*, and Empathy is
   disabled outside quests. Their 9 and 11 roster units are **gig variants**, not
   persistent garrisons. Do not treat the door economy as a standing force.
9. **The Grand Imperial Mall is a hired base, not a capital.** The wiki says the
   Animals held it "formerly" and the Scavengers stripped it after they left;
   `headquarters = N/A`. The seed's `hq_animals` is the GIM, which is Sasquatch's
   contract, not a seat.
10. **Angelica Whelan's Dogtown cell is thin in local data.** The PL quest
    sector is not in `dist/extract/raw`; the evidence is `{mq306_com_animals_end}`
    3 Animals at the ring, 2 Barghest spectators, her record in
    `always_loaded_1`, and the quest page. Treat the 3 as the quest's "Angie + two
    Animals", not a pack roster.
11. **No member counts per pack.** Community entries are presence proxies, and
    the `q110` mall communities are overlapping phases of one site. Do not sum
    them.
12. **The NCART "S" is unidentified.** The author of *Upcoming work* signs only
    "S". Do not assume Sasquatch; the cell is a different pack.
13. **The Valentinos row is asymmetric with the Valentinos doc.** That doc calls
    the pair neutral; the Animals-side shard shows a generator purchase/dispute
    and a fight grudge. This doc uses `trade` and cites the shard. A reviewer may
    prefer `neutral` for symmetry.
14. **The 6th Street, Arasaka and Barghest docs all call the Animals neutral,
    and this doc agrees.** The location doc's "rival" rows for Tyger Claws, 6th
    Street, Valentinos and Barghest are adjacency, not evidence. Do not promote
    them without a source.
15. **The Scavengers row is `trade`, not `rival`.** The strongest evidence is a
    bodyguard contract for the Scav boss Tzar (`Character.q303_paradise_animal_guard`
    ×2); the GIM takeover is succession, not conflict. The design's "Scavs are at
    war with everyone" is a system rule and may override this row in play.
16. **The Maelstrom relationship is hostile *and* commercial.** The Brandon Frost
    atrocity and the revenge order sit beside a stolen-lidocaine supply channel.
    One stance (`hostile`), nuance in the evidence. Do not model a clean war.
17. **`areas.jsonl` co-occurrence is weak relation evidence.**
    `{sa_ep1_113_com_combat}` is a multi-faction brawl pool (Animals 5, VDB 11,
    Scav 6, Barghest 3, Tyger 3, Arasaka 1); `{mq025_com_finale}` and
    `{mq303_com_fans}` are crowds. I used co-occurrence only to corroborate
    wiki-attested rows.
18. **No offline attitude matrix.** `Attitude_Record.hpp` is opaque and
    `Affiliation.hpp` is identity only (Animals = 2 in the enum; the
    `factions.json` id is 6). Every stance is judged.
19. **Phantom Liberty supplies the only Dogtown pack leader and the fight-fixing
    plot.** Without PL, the Animals have no Dogtown politics beyond the GIM and
    a generic Dogtown area.
20. **The campaign-disabled caveat is worse here than for any other gang.**
    Almost every named Animal is quest- or activity-gated; the mod must spawn
    the cast itself.
21. **Razor Hugh contradicts the purist identity.** He has corporate sponsors and
    prototype chrome; the faction is not uniformly anti-cyberware. Model the
    purist/chrome split, not a single doctrine.
22. **"Juice" has no located lab.** The cook "Rudi" and the lab are named only in
    a computer message; the seeded Juice site is a distribution den, not a
    factory. Do not give the product a manufacturing control point yet.
23. **The Abomination/Guerriera poster is a cross-gang bout, not diplomacy.** The
    sources disagree on Abomination's faction; the poster is not a treaty.
24. **The Animals' international gun clients have no faction codes.** The Data
    Inc. "WATCH OUT" list names buyers in Pakistan, France, Scotland, Argentina,
    Turkey, Brazil and South Africa. Prose only; do not invent faction rows.
25. **`initial_owner_faction_id` is a sub-territory artefact.** It is not used for
    any political claim here; the ownership evidence is `default_faction_id`,
    rosters and the wiki.

### 5.1 Sources consulted

- Local: `data/sites/rosters.json`, `data/sites/sites.json`,
  `data/sites/{communities,guards,triggers,spots,patrols,doors,suitabilities}.json`,
  `data/factions.json`, `data/sub_territories.json`,
  `data/control_centers.json`, `data/faction_headquarters.json`,
  `data/districts.json`, `dist/extract/areas.jsonl`,
  `dist/extract/markers.jsonl`,
  `dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_{0,1,2}.streamingsector.json`
  (community registry: `characterRecordId`, `entryName`, `phaseName`,
  `spotNodeRefs`).
- Wiki: [Animals](https://cyberpunk.fandom.com/wiki/Animals),
  [Animals Members](https://cyberpunk.fandom.com/wiki/Animals_Members),
  [Matilda K. Rose](https://cyberpunk.fandom.com/wiki/Matilda_K._Rose),
  [Valdemar](https://cyberpunk.fandom.com/wiki/Valdemar),
  [Denzel Cryer](https://cyberpunk.fandom.com/wiki/Denzel_Cryer),
  [Jesse Sabara](https://cyberpunk.fandom.com/wiki/Jesse_Sabara),
  [Angelica Whelan](https://cyberpunk.fandom.com/wiki/Angelica_Whelan),
  [Martha Ling](https://cyberpunk.fandom.com/wiki/Martha_Ling),
  [Logan Garcia](https://cyberpunk.fandom.com/wiki/Logan_Garcia),
  [Rhino](https://cyberpunk.fandom.com/wiki/Rhino),
  [Razor Hugh](https://cyberpunk.fandom.com/wiki/Razor_Hugh),
  [Emmerick Bronson](https://cyberpunk.fandom.com/wiki/Emmerick_Bronson),
  [Seamus Sawicki](https://cyberpunk.fandom.com/wiki/Seamus_Sawicki),
  [Larissa Almeida](https://cyberpunk.fandom.com/wiki/Larissa_Almeida),
  [Aaron Waines](https://cyberpunk.fandom.com/wiki/Aaron_Waines),
  [Kyle J.](https://cyberpunk.fandom.com/wiki/Kyle_J.),
  [Grand Imperial Mall](https://cyberpunk.fandom.com/wiki/Grand_Imperial_Mall),
  [Tripple Extreme Gym](https://cyberpunk.fandom.com/wiki/Tripple_Extreme_Gym),
  [Unfinished NCART Station](https://cyberpunk.fandom.com/wiki/Unfinished_NCART_Station),
  [7th Hell](https://cyberpunk.fandom.com/wiki/7th_Hell),
  [Empathy](https://cyberpunk.fandom.com/wiki/Empathy_(club)),
  [Data Inc. (Wellsprings)](https://cyberpunk.fandom.com/wiki/Data_Inc._(Wellsprings)),
  [Afterlife](https://cyberpunk.fandom.com/wiki/Afterlife),
  [NetWatch](https://cyberpunk.fandom.com/wiki/NetWatch),
  [Black Sapphire](https://cyberpunk.fandom.com/wiki/Black_Sapphire),
  [Jack Mausser](https://cyberpunk.fandom.com/wiki/Jack_Mausser),
  [Juice](https://cyberpunk.fandom.com/wiki/Juice).
- Quest and shard pages:
  [I Walk the Line](https://cyberpunk.fandom.com/wiki/I_Walk_the_Line),
  [No Easy Way Out](https://cyberpunk.fandom.com/wiki/No_Easy_Way_Out),
  [Gig: For My Son](https://cyberpunk.fandom.com/wiki/Gig:_For_My_Son),
  [Gig: Two Wrongs Makes Us Right](https://cyberpunk.fandom.com/wiki/Gig:_Two_Wrongs_Makes_Us_Right),
  [Gig: An Inconvenient Killer](https://cyberpunk.fandom.com/wiki/Gig:_An_Inconvenient_Killer),
  [Gig: A Lack of Empathy](https://cyberpunk.fandom.com/wiki/Gig:_A_Lack_of_Empathy),
  [Gig: Hot Merchandise](https://cyberpunk.fandom.com/wiki/Gig:_Hot_Merchandise),
  [SOCA: Living the Big Life](https://cyberpunk.fandom.com/wiki/Suspected_Organized_Crime_Activity:_Living_the_Big_Life),
  [Beat on the Brat](https://cyberpunk.fandom.com/wiki/Beat_on_the_Brat),
  [Beat on the Brat: Rancho Coronado](https://cyberpunk.fandom.com/wiki/Beat_on_the_Brat:_Rancho_Coronado),
  [Archived Conversation: Seamus Sawicki and Fred Risch](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Seamus_Sawicki_and_Fred_Risch),
  [Archived Conversation: Larissa Almeida and Joe Peck](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Larissa_Almeida_and_Joe_Peck),
  [Unfinished NCART Station/Computers](https://cyberpunk.fandom.com/wiki/Unfinished_NCART_Station/Computers),
  [Data Inc. (Wellsprings)/Computers](https://cyberpunk.fandom.com/wiki/Data_Inc._(Wellsprings)/Computers),
  [Damir Kovac/Computers](https://cyberpunk.fandom.com/wiki/Damir_Kovac/Computers).
- Earlier repo research: `docs/research/factions/animals.md`,
  `docs/research/factions/METHOD.md`, `docs/design/gameplay-systems.md`,
  `docs/research/factions/politics/maelstrom.md`,
  `docs/research/factions/politics/valentinos.md`,
  `docs/research/factions/politics/voodoo-boys.md`,
  `docs/research/factions/politics/sixth-street.md`,
  `docs/research/factions/politics/arasaka.md`,
  `docs/research/factions/politics/barghest.md`.

---

## 6. Machine-readable block

```json
{
  "faction_code": "animals",
  "leaders": [
    {
      "name": "Matilda \"Sasquatch\" K. Rose",
      "role": "Pack leader (Grand Imperial Mall pack); alpha since 2075; not a faction-wide boss",
      "character_record_id": "Character.q110_animals_boss",
      "location_name": "Grand Imperial Mall, Coastview",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_1 registry entry animals_boss (phases arena, hall_chat, spot #q110_ws_boss_on_arena); markers q110_08c_sm_bossfight, q110_08d_sm_animals_stand_down, sasquatch_perf_spn; wiki Matilda K. Rose; I Walk the Line",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Denzel \"The Brain\" Cryer",
      "role": "Pack leader; Juice trafficking chief",
      "character_record_id": "Character.ma_hey_spr_11_outpost_miniboss",
      "location_name": "Skyline South Juice den, Wellsprings",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "raw always_loaded_1 entry enemy_005 (appearance denzel_cryer_default, phase A, spot #ma_hey_spr_11_ws_enemy_005); site 90 ma_hey_spr_11; SOCA Living the Big Life; wiki Denzel Cryer",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Angelica \"Angie\" Whelan",
      "role": "Pack leader (Dogtown); fight arranger and fixer",
      "character_record_id": "Character.mq306_angie",
      "location_name": "Dogtown (Montezuma's Throne ring / Damir's clinic)",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "raw always_loaded_1 entry angie (phases 03_ripper_in/03_ripper_out, spot #mq306_angie_clinic_in); area {mq306_com_animals_end} 3; No Easy Way Out; wiki Angelica Whelan",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Valdemar \"The Bully\"",
      "role": "Pack leader (book only)",
      "character_record_id": null,
      "location_name": "Night City (off-map)",
      "presence_class": "off-map",
      "open_world": false,
      "source": "The World of Cyberpunk 2077 p.162; wiki Animals Leadership; wiki Valdemar",
      "confidence": "wiki+lore"
    },
    {
      "name": "Logan Garcia",
      "role": "Secondary leader; owner of the Tripple Extreme Gym fight club",
      "character_record_id": "Character.wwd_05_target",
      "location_name": "Tripple Extreme Gym, Arroyo",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "site 378 sts_pac_wwd_05 (9 units); only target slot #wwd_05_ws_target; Gig: For My Son; wiki Logan Garcia; wiki Tripple Extreme Gym",
      "confidence": "inferred+wiki"
    },
    {
      "name": "Jesse Sabara",
      "role": "Secondary leader; Denzel Cryer's second in command",
      "character_record_id": null,
      "location_name": "Skyline South Juice den, Wellsprings",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "wiki Animals Members; wiki Jesse Sabara; SOCA Living the Big Life; no distinct record at site 90",
      "confidence": "wiki+inferred"
    },
    {
      "name": "Martha \"Abomination\" Ling",
      "role": "Listed as a secondary leader on the Animals page; her own page says Tyger Claws",
      "character_record_id": null,
      "location_name": "Night City (poster only)",
      "presence_class": "mentioned",
      "open_world": false,
      "source": "wiki Animals Leadership; wiki Martha Ling; World of Cyberpunk p.162; in-game Abomination vs Guerriera poster",
      "confidence": "wiki+lore"
    },
    {
      "name": "Rhino",
      "role": "Fight-circuit champion; Tripple Gym trainee, GIM finale spectator",
      "character_record_id": "Character.mq025_rhino",
      "location_name": "Tripple Extreme Gym; Grand Imperial Mall ring",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "raw always_loaded_1 entry rhino (phases mq025_rhino_01_pre_fight, _02_fight, _03_post_fight, finale); Beat on the Brat: Rancho Coronado; wiki Rhino",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Razor Hugh",
      "role": "Heavyweight champion; final Beat on the Brat opponent",
      "character_record_id": "Character.mq025_razor",
      "location_name": "Grand Imperial Mall ring, Coastview",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "raw always_loaded_1 entry razor (phases mq025_razor_01_pre_fight, _02_fight); marker mq025_mp_08_ring; Beat on the Brat; wiki Razor Hugh",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Emmerick Bronson",
      "role": "Afterlife doorman; Animal member",
      "character_record_id": "Character.Emmerick",
      "location_name": "Afterlife, Little China",
      "presence_class": "ambient",
      "open_world": true,
      "source": "raw always_loaded_1 entry emmerick (quest phases q005_emmerick_bouncer, q103_afterlife_entrance); markers q005_emmerick_bouncer, q203_emmerick_front_door; wiki Emmerick Bronson; wiki Afterlife",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Seamus Sawicki",
      "role": "Bouncer; led the Militech-intern killing",
      "character_record_id": "Character.ma_std_arr_10_seamus",
      "location_name": "Corpo Plaza alley, Bruce Skiv & Union St.",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "raw always_loaded_1 record (single placement at ma_std_arr_10); shard baseid ma_cct_cpz_17_onscreen_01; shard Seamus Sawicki and Fred Risch; site ma_cct_cpz_17; wiki Seamus Sawicki",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Fred Risch",
      "role": "Bouncer-crew boss; authorises the Militech-intern killing",
      "character_record_id": null,
      "location_name": "Corpo Plaza (shard only)",
      "presence_class": "mentioned",
      "open_world": false,
      "source": "shard Seamus Sawicki and Fred Risch (ma_cct_cpz_17_onscreen_01); no record or wiki page",
      "confidence": "wiki"
    }
  ],
  "internal_factions": [
    {
      "name": "Sasquatch's NetWatch contract pack (GIM)",
      "leader": "Matilda \"Sasquatch\" K. Rose",
      "goals": "Hold the Grand Imperial Mall, protect NetWatch agent Bryce Mosley, keep the Voodoo Boys out, earn the security contract",
      "members_hint": "55 Animals across six q110_com_mall_* communities; sub-territory 61 cvi_grand_imperial_mall; 8 spawn points",
      "source": "I Walk the Line; q110 markers; wiki Animals History; wiki Grand Imperial Mall",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Denzel Cryer's Juice cartel (Wellsprings)",
      "leader": "Denzel \"The Brain\" Cryer",
      "goals": "Manufacture and distribute Juice; raid drug stores, chemical transports and pharma for inputs",
      "members_hint": "site 90 ma_hey_spr_11 10 units; ma_hey_spr_11_com 10; Jesse Sabara as second; Rudi as cook",
      "source": "SOCA Living the Big Life; NCART DELIVERY!!!; wiki Denzel Cryer, Jesse Sabara, Juice",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Logan Garcia's fight club (Tripple Gym)",
      "leader": "Logan Garcia",
      "goals": "Run the paint-vat fight ring, gate fees, the melee vendor and fight tourism; keep the gym's reputation",
      "members_hint": "site 378 sts_pac_wwd_05 9 units; wwd_05_com_enemies 9; Rhino trains here",
      "source": "Gig: For My Son; Beat on the Brat: Rancho Coronado; wiki Tripple Extreme Gym",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Angelica Whelan's Dogtown fight-fixing ring",
      "leader": "Angelica \"Angie\" Whelan",
      "goals": "Arrange and fix fights, control boxers with implants, wheel in cash",
      "members_hint": "mq306_com_animals_end 3 (Angie plus two); Damir Kovac as ripperdoc; Aaron Waines as fixed fighter",
      "source": "No Easy Way Out; Damir Kovac/Computers; areas mq306; wiki Angelica Whelan",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The NCART expansion cell",
      "leader": null,
      "goals": "Seize the stadium parking lot, monitor Monica Steiner's nomad outreach, collect on the Valentino generator deal, dispose of Guerriera",
      "members_hint": "site 377 sts_pac_cvi_02 13 units; cvi_02_combat_com 13; author signs only S",
      "source": "NCART computers Upcoming work, DELIVERY!!!, brandon frost; Gig: Two Wrongs Makes Us Right",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The door economy (bouncer/bodyguard contracts)",
      "leader": "Fred Risch (one crew; no faction-wide leader)",
      "goals": "Sell muscle to clubs, corporates and venues; keep the contracts",
      "members_hint": "7th Hell 9 (gig variant), Empathy 11 (gig variant), Data Inc. 4, Afterlife 1 (Emmerick), Corpo Plaza 4",
      "source": "A Lack of Empathy; An Inconvenient Killer; Hot Merchandise; wiki Animals database entry",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The fight circuit / athlete wing",
      "leader": "Rhino",
      "goals": "Championships, prize money, sponsorship, street cred",
      "members_hint": "Rhino, Razor Hugh, Larissa Almeida (dead), Abomination (book/poster); GIM ring and Tripple Gym",
      "source": "Beat on the Brat; wiki Rhino and Razor Hugh; posters; Larissa Almeida shard",
      "confidence": "game-data+wiki+lore"
    },
    {
      "name": "The purist hormone current vs chrome pragmatists",
      "leader": null,
      "goals": "Peak human body through Juice and surgery vs accept corporate prototype chrome and hired netrunning",
      "members_hint": "diffuse: Juice users vs Razor's prototype implants vs the Data Inc. netrunning den",
      "source": "wiki Animals overview; wiki Razor Hugh; Data Inc. computers",
      "confidence": "wiki+lore"
    },
    {
      "name": "Valdemar's pack / historical alphas",
      "leader": "Valdemar \"The Bully\"",
      "goals": "Unknown; book only",
      "members_hint": "no 2077 record",
      "source": "The World of Cyberpunk 2077 p.162; wiki Animals Leadership",
      "confidence": "wiki+lore"
    }
  ],
  "relations": [
    {
      "faction_code": "tyger_claws",
      "stance": "neutral",
      "evidence": "No attested conflict. Jig-Jig Street lists Animals among its gangs and an Assault in Progress on Salinas St (site 284, 5 Animals) sits in Tyger JapanTown; the location doc's rival is adjacency, not evidence. No Animals-Tyger co-occurrence beyond the generic sa_ep1_113 brawl [game-data] [wiki] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "valentinos",
      "stance": "trade",
      "evidence": "NCART to-do list: generators from the tinos still don't work (incompatible transistors?) head to their shop in the Glen and sort it - a purchased-goods dispute. Larissa Almeida's shard: after she beat a Valentino, Tinos aren't big fans of you. No violence attested; the Valentinos doc calls the pair neutral [wiki] [game-data]",
      "confidence": "wiki"
    },
    {
      "faction_code": "arasaka",
      "stance": "neutral",
      "evidence": "No attested interaction; the Arasaka politics doc also records neutral. Animals sell bodyguards but no Arasaka contract is attested [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "militech",
      "stance": "hostile",
      "evidence": "Recorded kill order on Militech interns (Seamus Sawicki shard); Data Inc. sells hacked, previously stolen Militech guns to international clients (Data Inc. WATCH OUT list); the Data Inc. office says it intercepted militech arms shipments at the chop shop; Rogue's gig frames Militech as about to send troops into the city [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "kang_tao",
      "stance": "neutral",
      "evidence": "No attested interaction; Sasquatch carries a Kang Tao A-22B Chao, an equipment choice, not a relationship [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "biotechnica",
      "stance": "neutral",
      "evidence": "No attested interaction; the Animals brew their own hormones (Juice, ultra-testosterone, equine growth hormone) rather than buy Biotechnica product [wiki] [inferred]",
      "confidence": "wiki+inferred"
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
      "evidence": "Angelica Whelan's Dogtown fight night places 3 Animals at mq306_com_animals_end with 2 Barghest in the spectator crowd mq306_com_spectators; tolerated co-presence in Barghest turf, no deal or conflict attested. The Barghest doc also records neutral [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "sixth_street",
      "stance": "neutral",
      "evidence": "Co-residents in Santo Domingo: the Tripple Gym sits in 6th Street turf and the 6th Street doc records neutral. No attested conflict or deal [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "aldecaldos",
      "stance": "neutral",
      "evidence": "No attested interaction. The NCART to-do list notes Monica Steiner is looking to nomads for help over her son's death - a threat the Animals are tracking, not a nomad relationship [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "wraiths",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "the_mox",
      "stance": "neutral",
      "evidence": "No attested interaction; both work the club economy but no shared venue, deal or conflict is attested [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "maelstrom",
      "stance": "hostile",
      "evidence": "Brandon Frost buried several Animals alive in concrete and sold the XBD; the NCART pack's computer orders I WANT HIM ALIVE. The same pack buys/receives stolen lidocaine from those chromed cocksuckers for Juice - hostility with a supply channel [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "voodoo_boys",
      "stance": "hostile",
      "evidence": "NetWatch hired Sasquatch's pack to guard agent Bryce Mosley at the GIM and hide him from the VDB; the VDB send V to wipe the pack in I Walk the Line; the GIM is in VDB-controlled west Pacifica. The VDB doc records the same hostile stance [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "ncpd",
      "stance": "hostile",
      "evidence": "Standing target: the NCPD APB names Denzel Cryer and his Juice ring (SOCA Living the Big Life); Assault in Progress sites at Corpo Plaza, JapanTown, Little China and Coastview; scanner hustles and gang-watch activities across the map [game-data] [wiki]",
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
      "evidence": "No attested interaction; no purchased channel found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "scavengers",
      "stance": "trade",
      "evidence": "Animal bodyguards (Character.q303_paradise_animal_guard x2) flank the Scav boss Tzar at the Black Sapphire party - a transactional muscle contract. Scavs later moved into the GIM after the Animals left, which is succession, not a feud. No attested Animals-Scav fight [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_regina",
      "stance": "neutral",
      "evidence": "No Animals-specific gig or lore link found; her gigs are Watson [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_wakako",
      "stance": "neutral",
      "evidence": "No Animals-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_padre",
      "stance": "neutral",
      "evidence": "No Animals-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_el_capitan",
      "stance": "hostile",
      "evidence": "El Capitan takes Monica Steiner's contract and sends V to neutralise Logan Garcia at the Tripple Gym (Gig: For My Son); the NCART to-do list tracks her outreach to the nomads [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_dakota",
      "stance": "neutral",
      "evidence": "No Animals-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_dino",
      "stance": "hostile",
      "evidence": "Dino gives An Inconvenient Killer (neutralise Jack Mausser inside Animal-guarded 7th Hell) and A Lack of Empathy (upload a virus to Animal-guarded Empathy's subnet) [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_rogue",
      "stance": "hostile",
      "evidence": "Rogue gives Hot Merchandise: neutralise Rebeca Price inside the Animal-staffed Data Inc. store, to stop stolen Militech guns drawing a corporate crackdown [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_mr_hands",
      "stance": "hostile",
      "evidence": "Mr. Hands gives Two Wrongs Makes Us Right: steal the Animals' lidocaine van from the NCART den and resell it to ripperdocs [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "afterlife",
      "stance": "client",
      "evidence": "Emmerick Bronson, an Animal, is the Afterlife's doorman (Character.Emmerick; markers q005_emmerick_bouncer, q203_emmerick_front_door); the bar hires the gang's muscle [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "netwatch",
      "stance": "client",
      "evidence": "NetWatch hired Sasquatch's pack as private security for agent Bryce Mosley at the GIM, using the Animals as its proxy against the Voodoo Boys. The contract is with the pack, not the faction [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "nusa",
      "stance": "neutral",
      "evidence": "No direct NUSA-Animals interaction; the client is NetWatch, an international agency, not the NUSA state [inferred]",
      "confidence": "inferred"
    }
  ]
}
```
