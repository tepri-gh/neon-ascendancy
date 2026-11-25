# Aldecaldos — Leadership, Internal Politics and External Relations

Status: research run, 2026-11-25. One faction, one document.
Scope: Cyberpunk 2077 2.5 + Phantom Liberty, campaign disabled. Who a player can
join under, climb past, ally with or remove inside the Aldecaldos; the internal
blocs; and the external-relations matrix needed for wars, alliances and
"guarantor" support when a player founds a gang.

Method: this document follows [`METHOD.md`](./METHOD.md) and the evidence rules
of [`../METHOD.md`](../METHOD.md) §1.1–§1.2. The location catalog for the
Aldecaldos is [`../aldecaldos.md`](../aldecaldos.md); this document maps people
and politics onto those places and does not repeat the coordinates.

Two structural facts drive everything below and are easy to get wrong:

1. **The 2077 faction is one pack, not the nation.** The Aldecaldos are a
   Seven-Nations member with tens of thousands of members; the Badlands group is
   Saul Bright's **Bright Family**, "a pack, maybe a couple of packs, in a
   temporary encampment" (J Gray, clarifying the 2045 enclave versus 2077). The
   `aldecaldos` faction id 9 models the pack. `[wiki]`
2. **The pack has no ranks, only relationships.** Lore gives a family leader, a
   co-leader, "veterans", members, and an adoption ritual — no grade ladder.
   Every named NPC is story-gated. `[wiki]` `[game-data]`

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/comic/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My reasoning links a named person, place or stance to a record; reasoning stated | Weak, flagged |

**Presence class**, an extra convention for this document only. `ambient` =
persists in free roam without a quest; `world-activity` = gig, scanner hustle or
minor job, i.e. free-roam content but still activity-gated; `story` = gated by
the Panam main/side job chain; `historical` = named and alive in 2077 but never
spawned, or not present at all. The JSON `open_world` flag is `true` for
`ambient` + `world-activity`, `false` for `story` + `historical`.

---

## 1. Leadership and ranks

### 1.1 The 2077 chain of command

The chain is **two people plus a veterans' bench**. Saul holds the seat; Panam
takes half of it after *Queen of the Highway* and all of it if Saul dies in the
*Star* ending. Carol Emeka is interim leader only while Saul is missing.

| Name | 2077 role | Character record | Location / influence point | Presence class | Source | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| **Saul Bright** | Family leader (Act 2); co-leader after *Queen of the Highway*; dies in the *Star* ending | `Character.Saul` | Old camp command trailer `(3430.5, -357.1, 134.0)`; new camp sitrep table `(1815.9, 2269.7, 180.9)` | `story` | Raw `always_loaded_1` registry entry `saul`, initial phase `default`, phases `default_newcamp`, `holocall`, `q114_*`; markers `{saul_sm_default}`, `q114_02_sm_saul_sitrep`, `q114_04b_sm__saul`; wiki *Saul Bright* | `[game-data]` `[wiki]` |
| **Panam Palmer** | Ex-member turned mercenary; rejoins; co-leader (branch); full leader after Saul's death (branch) | `Character.Panam` | Old camp `(3413.4, -361.6, 133.6)`; new camp `default_newcamp`; Afterlife during *Ghost Town* | `story` | Raw registry entry `panam`, phases `default`, `default_newcamp`, `default_hug`, `holocall`, `q103_afterlife_argument`, `q005_default`; markers `{panam_sm_default}`, `{panam_sm_hug_default}`; wiki *Panam Palmer* | `[game-data]` `[wiki]` |
| **Carol Emeka** | Interim leader while Saul is abducted; netrunner/techie; veteran | `Character.Carol` | Old camp `(3441.1, -333.8, 134.7)`; Corp-Bud Railroad Station `(2990.4, -1833.3, 101.9)` | `story` | Raw registry entry `carol`, phases `default`, `default_newcamp`, `mq002_deal`, `q114_driller_ctrls`; marker `{carol_sm_default}`; wiki *Carol Emeka* ("a distressed Carol acted in his place") | `[game-data]` `[wiki]` |
| **Mitch Anderson** | Veteran lieutenant; panzerboy, mechanic; Panam's closest ally | `Character.Mitch` | Old camp `(3426.2, -326.9, 134.6)`; new camp; Maglev assault (Basilisk solo pilot) | `story` | Raw registry entry `Mitch`, phases `default`, `mitch_default_active`, `default_newcamp`, `mq001_camp_funeral`; markers `{mitch_sm_default}`, `{fb_sm_mitch}`; wiki *Mitch Anderson* | `[game-data]` `[wiki]` |
| **Cassidy Righter** | Clan elder; best shot in camp; veteran; Panam's protector since childhood | `Character.Cassidy` | Old camp `(3442.5, -356.3, 133.9)`; Railroad Station `(2989.0, -1809.2, 101.5)` | `story` | Raw registry entry `cassidy`, phases `default`, `default_newcamp`, `mq002_deal`, `q114_dampening_*`; markers `cassidy_sm_default`, `sq027_04_sm_preparations_cassidy_teddy`; wiki *Cassidy Righter* | `[game-data]` `[wiki]` |
| **Bob Sagan** | Techie; veteran; dies at the Maglev site in the *Star* ending | `Character.Bob` | Old camp `(3395.8, -337.5, 134.5)`; new camp | `story` | Raw registry entry `Bob`, phases `default`, `default_newcamp`, `q114_bob_arasaka`, `q114_bob_attack`; marker `{bob_sm_default}`; wiki *Bob Sagan* | `[game-data]` `[wiki]` |
| **Theodore "Teddy" Simos** | Member; veteran; dies at the Maglev site in the *Star* ending | `Character.Teddy` | Old camp `(3410.6, -332.7, 134.5)`; new camp | `story` | Raw registry entry `Teddy`, phases `#sq027_teddy_post_final_scene`, `default`, `default_newcamp`, `q114_construction`; marker `{teddy_sm_default}`; wiki *Teddy Simos* | `[game-data]` `[wiki]` |
| **Driss "Scorpion" Meriana** | Veteran panzerboy; demoted dissident (2070); killed by Kang Tao (2077) | `Character.Scorpion` | Old camp funeral zone `(3328.1, -453.1, 124.2)`; Kang Tao crash site | `story` | Raw registry entry `scorpion`, initial phase `mq001_camp`, phases `q103_ws_scorpion_goodbye`, `q104_scorpion_dead`; wiki *Driss Meriana* | `[game-data]` `[wiki]` |
| Dakota Smith | Fixer; clan elder ("static"); the pack's economic interface — not in the command chain | `Character.dakota_smith` | DaKota autoshop `(2421.8, -772.4, 66.7)`; new-camp trailer `(1810.6, 2238.7, 180.2)` | `world-activity` | Raw registry entry `dakota`, phases `default`, `ina_06_ws_dakota_working`, `ina_07_dakota_waiting`, `q114_dakota_initiation_01`; markers `ina_07_mp_workshop`, `q114_03c_sm_dakota_trailer`; wiki *Dakota Smith*. The isolated `dakota_sm_smith_defaut` marker is a decoy, see [`../aldecaldos.md`](../aldecaldos.md) §8 item 2 | `[game-data]` `[wiki]` |

Two facts do the political work:

1. **The seat is shared, not contested.** Saul does not lose power to Panam; he
   *promotes* her after she defies him and the clan survives. "Saul tells Panam
   that she's been making the right decisions for the Aldecaldos family, and
   asks her that she leads them alongside him." `[wiki]` There is no coup, no
   purge, no exile — the opposite of Maelstrom's pattern.
2. **Legitimacy is earned by risking yourself for the family.** Saul's stated
   error is mistaking "her willingness to risk everything for the family with
   recklessness." `[wiki]` Advancement in this faction is *demonstrated
   sacrifice*, not seniority.

### 1.2 Succession history: dynastic at the nation, personal at the pack

| Period | Leader / centre of power | How the change happened |
| --- | --- | --- |
| 1992–2015 | **Juan Aldecaldo** | Founder. Built the nation out of an LA neighbourhood watch after his son's murder; appointed his successor on his deathbed in Mexico. `[wiki]` |
| 2015–2045+ | **Nomad Santiago** | Chosen by Juan, not elected. Mercenary and Rogue Amendiares' partner; led the return to the US; forged the Seven Nations at Omaha in 2017; sent the Lobos to the 2023 Arasaka Towers assault. Still leader in 2045. `[wiki]` |
| unknown | **Tommy Blaine** | Leader of the **Blaine Family**, one of several Aldecaldo families. A family leader, not a nation leader — the structure is federal. `[wiki]` |
| unknown–2077 | **Saul Bright** | Took the Bright Family when it "was in a fragile state"; broke from the smuggling tradition toward corporate contracts. `[wiki]` |
| 2077 | **Saul + Panam** (branch) | Saul makes Panam co-leader after the Raffen attack on the camp, admitting he was wrong. `[wiki]` |
| 2077 | **Panam alone** (*Star* branch) | Saul is killed by Adam Smasher inside Arasaka Tower; "Panam assumed full leadership of the Aldecaldos, leading her clan south across the border." `[wiki]` |

The pattern: **succession is appointed, not seized.** Juan named Santiago;
Santiago's authority was reputational and confirmed by the nation's acclamation;
Saul promoted his own critic. The only removal in the record is external
violence (Smasher), and even then the successor was already co-leader. A
simulation that kills the leader should produce a **named successor**, not a
power vacuum — unless the successor is also removed.

Historical secondary figures worth knowing for a succession model: **Father
Jonah Dominguez** (co-founder, 1992–2002, died of a heart attack), **Tommy
Blaine** (Blaine Family), and the **Lobos** — the nation's elite commando arm,
which has commanders and negotiators (Izzy Lobo) but no 2077 presence. `[wiki]`
`[lore]`

### 1.3 Rank structure, adoption and advancement

Lore names **family leader**, **co-leader**, **veteran**, **member**, and an
informal stage before membership. Below that it is function, not grade.

1. **Family leader (the seat).** One person. Runs the camp, negotiates the
   contracts, and controls assignments. `[wiki]`
2. **Co-leader.** A second seat created in 2077 for Panam; it is real power
   (she plans and leads operations) but stays subordinate while Saul lives.
   `[wiki]`
3. **Veterans.** The Unification War cohort — Mitch, Scorpion, Carol, Cassidy,
   Bob, Teddy. They are the clan's military and technical bench and they act as
   a **caucus**: Panam recruits "like-minded clan members" from their number,
   and Saul must answer them. `[wiki]` `[game-data]`
4. **Members.** Everyone else: gunslingers (Taco, Jeff), technicians, families
   (the Scooters), racers. `[wiki]`
5. **Informal members and adoptees.** V is "an informal member already" before
   the formal welcome. `[wiki]`
6. **Non-member dependents.** Dakota (member, but static and outside the
   chain), and the camp's non-Aldecaldo neighbours such as Joss Kutcher, whose
   *husband* was the member. `[wiki]`

**The family council is the only named deliberative body.** Saul tells Panam
they will hold a "family council" to decide her future in the clan — a hearing,
not a vote, convened by the leader. `[wiki]` It is the single strongest hook for
modelling internal politics: a leader can be *tried* by the family.

**Adoption is the membership mechanic, and it is a ritual plus a declaration.**
*We Gotta Live Together* has V "get in the tub" and Saul welcomes V as a full
member before the clan. `[wiki]` `[game-data]` marker `q114_04_sm_initiation`
`(1829.0, 2284.6, 179.9)`. Two independent gates matter:

- **Entry by invitation.** Anna Hamill can be talked into joining (*Woman of La
  Mancha*, Nomad lifepath only); Bruce Welby joins after *Goodbye, Night City*
  and is present at the initiation and party (`#q114_ws_welby_initiation_01`,
  `#q114_ws_welby_party_01`). `[wiki]` `[game-data]`
- **Exit by judgment.** Scorpion's punishment for lobbying to join Snake Nation
  was **demotion and a year without assignments** — not expulsion. Expulsion is
  reserved for the crimes that create Raffen Shiv (murder, rape, trafficking,
  betrayal). `[wiki]`

Practical consequence for the mod: membership is a **two-stage** state
(informal → full), advancement is **service + the leader's declaration**, and
the failure mode is not a ladder but a **family council**.

### 1.4 Named members mapped to game data

None of the leadership is in `data/sites/rosters.json`. The faction's 5 roster
sites / 8 units are all generic quest NPCs (`Character.aldecaldos_grunt2_melee2__ma`,
`Character.sts_bls_ina_08_nomad_01`, `Character.ina_09_nomad`,
`Character.sts_std_rcr_03_nomad`, and the `ma_bls_ina_07` cyberpsycho). Every
named Aldecaldo lives in the raw sector community registry. `[game-data]`

| Name | Role / note | Character record | Community / site | Location | Presence class | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| Saul Bright | Leader | `Character.Saul` | 1-entry community, hash `6366518277857704447` | Old camp; new camp | `story` | `[game-data]` `[wiki]` |
| Panam Palmer | Co-leader / leader | `Character.Panam` | hash `11284313788165891607` | Old camp; new camp; Afterlife | `story` | `[game-data]` `[wiki]` |
| Carol Emeka | Interim leader, netrunner | `Character.Carol` | hash `10087771383514019631` | Old camp | `story` | `[game-data]` `[wiki]` |
| Cassidy Righter | Elder, marksman | `Character.Cassidy` | hash `2403952533023319600` | Old camp | `story` | `[game-data]` `[wiki]` |
| Mitch Anderson | Veteran lieutenant | `Character.Mitch` | hash `12239698428191821195` | Old camp; new camp | `story` | `[game-data]` `[wiki]` |
| Bob Sagan | Techie | `Character.Bob` | hash `18190633559077816429` | Old camp; new camp | `story` | `[game-data]` `[wiki]` |
| Teddy Simos | Member, veteran | `Character.Teddy` | hash `5483915938093667172` | Old camp; new camp | `story` | `[game-data]` `[wiki]` |
| Driss "Scorpion" Meriana | Veteran, demoted dissident | `Character.Scorpion` | hash `6765127873941692499` | Old camp funeral; crash site | `story` | `[game-data]` `[wiki]` |
| Dakota Smith | Fixer, elder | `Character.dakota_smith` | hash `8145842032574589124` | DaKota; new camp | `world-activity` | `[game-data]` `[wiki]` |
| Ellie | Young member near the bar | `Character.q103_nomad_ellie` (entry `nomad_05`) | `{q103_com_dlg_nomads}` (7) | Old camp bar | `story` | `[game-data]` `[wiki]` |
| Taco; Jeff | Twin gunslingers; guards at the Scav deal | no named record found; generic `{mq002_com_nomads}` (2) | `{mq002_com_nomads}` | Arroyo industrial lot; then camp | `story` | `[inferred]` `[wiki]` |
| Jake Scooter | Injured member; *Fortunate Son* | `Character.mq021_nomad_scooter` (entries `hurt_nomad`, `scooter`) | `{mq021_com_nomads}` (2) | New camp; Little China hospital | `story` | `[game-data]` `[wiki]` |
| Emily Scooter | Jake's partner; unnamed in crowd | no distinct record found | — | New camp | `story` | `[wiki]` |
| Trevor Brass | Member killed by Wraiths; *Trevor's Last Ride* | no named record; body prop at `sts_bls_ina_08` | site 346 | Wraith outpost, Biotechnica Flats | `world-activity` | `[inferred]` `[wiki]` |
| Euralio Alma | Member tortured by Wraiths; cyberpsycho | `Character.ma_bls_ina_se1_07_cyberpsycho_1` | site 7 `ma_bls_ina_07` | Wind Farms; buried at camp | `world-activity` | `[game-data]` `[wiki]` |
| Josie Alcazar | Member killed by Tyger Claws; *The Highwayman* | body prop `mq029_01b_sm_josie_body` `(-1382.4, -645.0, 7.7)` | — | the Glen alley | `story` | `[game-data]` `[wiki]` |
| Jason Wildriver | Member who sold out a merc to Militech; *MIA* | `Character.ina_09_jason_2` | `{ina_09_com_jason}` (2) | Clements St. | `world-activity` | `[game-data]` `[wiki]` |
| Benedict McAdams | Merc rescued by the clan's gig; joins the camp party | `Character.ina_09_benedict` (`#q114_ws_benedict_party_01`) | `{ina_09_*}` | New camp | `world-activity` | `[game-data]` `[wiki]` |
| Bruce Welby | Ex-smuggler adopted after *Goodbye, Night City* | `Character.sts_bls_ina_05_bruce` | `{ina_05_*}` | Militech Detention Center → new camp | `world-activity` | `[game-data]` `[wiki]` |
| Anna Hamill | Ex-NCPD officer who can join (Nomad lifepath only) | no Aldecaldo record; the gig is `sts_wat_kab_08` (site 398) | site 398 | Kabuki Market → new camp | `world-activity` | `[inferred]` `[wiki]` |
| Cyndi Lathan | 17-year-old runaway listed for sale; not rescued on screen | none | — | Night City | `historical` | `[wiki]` |
| Jakub Antonowicz; Margot Wojciechowicz | Racers (*The Beast in Me*) | `Character.sq024_badlands_race_nomad_racer` ×2 | `{sq024_com_badlands_race}` | Badlands circuit | `world-activity` | `[game-data]` `[wiki]` |
| Juan Aldecaldo | Founder (1992–2015) | none | — | — | `historical` | `[wiki]` `[lore]` |
| Nomad Santiago | Nation leader (2015–2045+) | none (2077 flashback only) | — | — | `historical` | `[wiki]` |
| Tommy Blaine | Blaine Family leader | none | — | — | `historical` | `[wiki]` `[lore]` |
| Father Jonah Dominguez | Co-founder (1992–2002) | none | — | — | `historical` | `[wiki]` `[lore]` |

Two data cautions:

- **`bob` and `teddy` are exact entry names, not substrings.** The registry uses
  `Bob` / `Teddy` with capitalised entry names while their records are
  `Character.Bob` / `Character.Teddy`. A lowercase substring scan of the whole
  sector returns thousands of unrelated rows; use the entry name plus the
  exact record.
- **`emily` in the registry is not Emily Scooter.** The only `emily` entry
  outside the camp is `Character.cpz_security_blackmasked_sniper3_grad_ma_elite`
  at `#mq062_Escape_Exit_AISpot_NCPD_04` — a Phantom Liberty NCPD sniper.
  Emily Scooter has no distinct record; she appears as unnamed camp crowd.

### 1.5 What the game actually spawns (open world vs story-only)

**`ambient` — persists in free roam.**
- **None of the leadership.** No named Aldecaldo leader is ambient. `[game-data]`
- The only quasi-ambient Aldecaldo body is the **19-nomad caravan camp** at
  `{post_ma_bls_ina_se1_22_com}` `(4831.9, -1378.2, 136.7)`: 23 entries in
  `default`, day and night variants, a working fire, a guitar, patrolling and
  wandering spots, three nomad cars and a broken-down one. It is real
  open-world set dressing and the single best in-game Aldecaldo test target.
  But its name is `post_`-prefixed to the Cyberpsycho Sighting site
  `ma_bls_ina_se1_22` (*Second Chances*), so treat it as a static caravan
  tableau, not a seat. `[game-data]` `[inferred]`

**`world-activity` — gig or scanner content; free-roam but activity-gated.**
- **Dakota Smith** at the autoshop. Fixers are the one NPC class the campaign
  sanitizer deliberately preserves (mappin `FixerVariant` kept, "the person
  stays; gig calls/pins are blocked"). She is the only leadership figure likely
  to survive a campaign-disabled world. `[game-data]` `[wiki]`
  `docs/research/campaign-sanitizer.md`
- The five gig/scanner scenes: *Flight of the Cheetah* (site 409, Northside),
  *Trevor's Last Ride* (346), *MIA* (347), *The Wasteland* cyberpsycho (7),
  *Going-away Party* (388). `[game-data]`

**`story` — gated by the Panam chain; do not expect them in free roam.**
- Saul, Panam, Carol, Cassidy, Mitch, Bob, Teddy, Scorpion, Ellie, Jake, the
  Taco/Jeff pair, Josie, and every camp community. Their initial phases are
  quest states (`default`, `mq001_camp`, `#q103_06b_panam_open_trunk`,
  `#sq027_teddy_post_final_scene`) and `entryActiveOnStart` is **0** for every
  one of them. `[game-data]`

Caveat: "campaign disabled" may also suppress the gigs. The `world-activity`
rows are the best reuse candidates but still need an in-game spawn check; the
`story` rows are the ones to replace with simulation agents.

### 1.6 Player-path hooks

| Person | Join under | Climb past | Ally with | Remove |
| --- | --- | --- | --- | --- |
| **Saul** | Corporate contract work, self-sufficiency, keeping the family fed — the "responsible adult" path | The veterans are his legitimacy; Panam is his declared successor, so climbing past him means beating her claim too | Dakota (money), Carol (competence), the camp's non-combatants | Killing Saul on the *Star* path hands the clan to Panam; killing him any other way leaves no canonical successor |
| **Panam** | Bold operations, no corporate dependence, strength through reputation | She is already co-leader; climbing past her means the family council or her death | Mitch, Cassidy, Bob, Teddy, Carol — the whole Basilisk crew | Removing Panam decapitates the expansion wing and leaves Saul's contract line dominant |
| **Carol** | Technical work, netrunning, the Scav arms channel | She is a peer, not a rung; she takes the seat only in a crisis | The veterans; Dakota (she assists Dakota's Net access in the *Star* branch) | Removing Carol costs the clan its only netrunner and its ICE checks |
| **Cassidy** | The clan's conscience: honesty, self-respect, "money can't buy" | Not a ladder; his endorsement is what makes a leader legitimate | Everyone; he is Panam's protector and the camp's moral referee | Removing Cassidy removes the arbitration that keeps the family from splitting |
| **Dakota** | Not a joinable path; she is the **fixer interface** | — | Ally for income, contracts and Badlands intelligence | Removing Dakota cuts the clan's contract pipeline and its only static asset |
| **Mitch** | Soldiering, panzers, loyalty | Veteran peer; the natural regent if both seats empty | Panam unconditionally; the Basilisk crew | Removing Mitch removes the clan's heavy-vehicle capability and its steadiest officer |

The design consequence: the Aldecaldos have **one legitimate ladder with two
claimants**, not a set of rival ladders. A player can back Saul's contract line
or Panam's independence line, and the losing side is *reintegrated*, not exiled
— which makes this faction the natural "reform from inside" path.

---

## 2. Internal political factions

### 2.1 The blocs

"Members" below are **presence proxies** from `dist/extract/areas.jsonl` and the
raw registry, not rolls. The camp communities are overlapping quest phases of
one place, so do not sum them.

| Bloc | Leader(s) | What it wants | Presence / members hint | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- |
| **Saul's contract line (pragmatists)** | Saul Bright | A steady corporate contract, self-sufficiency through paid work, avoid anything that risks the family's income | Saul; Carol as interim; the camp's non-combatants. `{sq004_com_nomads}` 20, `{q103_com_dlg_nomads}` 6 | The Biotechnica negotiation (paid in reverse-transpiration xerophytes); "desperate move to save the clan"; "we should be able to finish the job by the agreed upon date" | `[game-data]` `[wiki]` |
| **Panam's independence bloc (the Basilisk crew)** | Panam Palmer | No corporate dependence; strength through force and reputation; later, the border and a fresh start | Mitch, Cassidy, Bob, Teddy, Carol, Scorpion (posthumously). `{sq027_com_nomad_defense}` 9, `{sq027_com_guards}` 3, `{q114_com_nomad_party_mood_scenes}` 25 | *With a Little Help from My Friends*: Panam "gathers some like-minded fellow Aldecaldos"; Carol calls the plan "damn short, sweet, and pertinent"; the convoy heist | `[game-data]` `[wiki]` |
| **The Snake Nation current ("the third option")** | Scorpion (2070, demoted); unnamed members in 2077 | Join Snake Nation rather than serve corporations — "if we join Snake, we'll still be nomads" | No dedicated community; the idea circulates among the veterans | Saul Bright's computer, message *Third option*; Scorpion demoted and given no assignments for a year; the idea "brought up again by other clan members in 2077" | `[wiki]` |
| **The veterans' brotherhood** | No single leader; Mitch and Cassidy are the senior voices | The family as a soldiers' mutual-aid society; contempt for the corporate world that used them | The Unification War cohort: Mitch, Scorpion, Carol, Cassidy, Bob, Teddy — six of the camp's named members | Every one is a Unification War veteran; Mitch and Scorpion were panzerboys drugged to keep their synapses live; Carol: "the army was just another corporation" | `[wiki]` |
| **Dakota's static wing (broker/asset)** | Dakota Smith | Keep the Badlands ecosystem running, earn from those who come and go, oppose detachment from nomad life | DaKota autoshop; her gig chain (`sts_bls_ina_02/03/04/05/06/09/11`), `Every Grain of Sand` | "Statics are necessary — they take care of those who come and go. She does not deny earning from this duty"; the ecosystem speech | `[game-data]` `[wiki]` |

### 2.2 Saul vs Panam: the 2077 split

This is the faction's cleanest internal conflict and it maps onto a policy
difference, not a personality clash.

- **Saul's line:** the Brights left the smuggling tradition because it could no
  longer feed them. He negotiates crop-protection work for **Biotechnica**, asks
  to be paid in reverse-transpiration xerophytes (equipment to farm the
  Badlands), and accepts "increasingly unfavorable conditions" for a steady
  income. `[wiki]`
- **Panam's line:** any corporate partnership "would make them dependent on a
  ruthless corporation." She left the clan over it, worked as a mercenary under
  Rogue, and came back only when Saul was taken. `[wiki]`
- **The veterans split, and that is the point.** Mitch tells Saul the Biotechnica
  deal "would further cause the Nomad family to fall apart" and backs Panam;
  Carol hacks the Militech comms to prove the heist is not a setup; Cassidy
  would have preferred Saul's blessing but joins anyway. Only the contract
  itself keeps Saul's side together. `[wiki]`
- **Saul wins the argument but loses the policy.** He is proved right about the
  risk (Militech does trace the theft) and wrong about Panam; he promotes her,
  then terminates Biotechnica: "a conflict of interest as well as ensuring a
  clean conscience for the entire family." `[wiki]`

That is a simulation-ready axis: **dependent steady income vs. independent
risky income**. It is the mirror image of Maelstrom's *ideological violence vs.
transactional crime*, and it is the axis the design's "Economy strength /
Technology weakness" reading needs.

### 2.3 The veterans' caucus

The Unification War cohort is not an organised faction, but it behaves like a
caucus with three properties:

1. **It is the only body that can overrule the leader in practice.** Saul
   forbids the Basilisk operation and is simply ignored by five veterans plus
   Panam. `[wiki]`
2. **It supplies every specialist function.** Mitch (panzers, mechanics),
   Scorpion (vehicles, scouting), Carol (netrunning, ICE, heavy panzers),
   Cassidy (marksmanship, arbitration), Bob and Teddy (tech, logistics).
   `[wiki]` `[game-data]`
3. **It carries the clan's damage.** Panzerboy drug cocktails caused severe
   PTSD; Scorpion "had not been able to sleep soundly since." `[wiki]` A
   simulation can model the veterans as high-skill, high-fatigue members.

### 2.4 The "third option" and Snake Nation

Snake Nation is the largest Seven-Nations member and a loose confederation that
"claim[s] to represent the views of all independent nomad groups." `[wiki]`
Joining it is the clan's standing alternative to corporate work, and it has a
martyr: **Scorpion** proposed it in 2070, was demoted and given no assignments
for a year, and the idea resurfaced in 2077 "due to the family's dire
situation." `[wiki]`

This is the faction's only **external-alignment** cleavage. It also explains the
*Star* ending's logistics: Saul and Panam "tapped into their Snake Nation
sources" for the Maglev tunnel plans — the very faction Scorpion was punished
for advocating supplies the clan's escape. `[wiki]`

### 2.5 Dakota and the static question

Dakota is a member and an elder, and she is also the clan's sharpest internal
critic on one axis: **detachment**. The gig messages show her "boldly oppos[ing]
detachment from the nomad life, even if it means confronting an enemy," and she
calls herself a "static" in a tone "not one to assign as a compliment," while
insisting statics are necessary. `[wiki]`

She is a **non-chain power centre**: she has money, contracts, the only
permanent building, and the Badlands' information network, but no vote and no
followers. Model her as a `client`/asset with leverage, not a bloc leader.

### 2.6 What could drive internal conflict in a simulation

Evidence-based drivers, in rough order of plausibility:

1. **Corporate dependence vs. independence.** The core 2077 axis. A player who
   brings corporate contracts strengthens Saul's line; a player who brings
   raids and spoils strengthens Panam's.
2. **Succession when both seats are empty.** Saul dies in the *Star* branch and
   Panam inherits, but if Panam is also removed there is **no canonical
   successor**. The veterans (Mitch first) are the only credible regents, and
   the family council is the only process.
3. **The Snake Nation question.** A leader who signs with Snake Nation gains
   numbers and loses autonomy; a leader who refuses keeps the pack's freedom and
   its fragility. Scorpion's punishment is the precedent for how the seat
   treats dissent.
4. **Distribution of the take.** The Basilisk, the Militech loot and the Arasaka
   plunder are all contested. Cassidy's trick — dumping the stolen trucks at
   the Wraith camp to shift blame — shows that *how* spoils are handled is a
   political act, not just a logistics one.
5. **Treatment of newcomers.** Adoption is the growth engine (V, Anna Hamill,
   Bruce Welby, Benedict McAdams) and the security risk (Jason Wildriver sold a
   merc to Militech; Cyndi Lathan ran away and was trafficked). A leader who
   admits too many outsiders weakens the family's identity; one who admits too
   few cannot replace the veterans.
6. **Raffen attrition.** Trevor Brass, Euralio Alma and Saul's kidnapping are
   the same pressure: the Wraiths pick off small patrols. A leader who cannot
   protect the edges loses legitimacy faster than one who loses a contract.
7. **The static-versus-road argument.** Dakota's position — that the clan's
   future is to serve those who move — is a genuine alternative to both Saul's
   contracts and Panam's raids, and it is the only bloc with an independent
   economic base.

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
| `client` | Depends on or works for the other (buyer, supplier, proxy) |

There is **no usable offline attitude matrix**. `Attitude_Record.hpp` is opaque
and `Affiliation.hpp` is identity only. Every stance below is judged from
quests, wiki and spatial adjacency, which is why each row carries a tag and why
the neutral rows are placeholders, not claims of friendship.

### 3.2 The matrix

| Faction | Code | Stance | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| Wraiths | `wraiths` | `war` | The defining enemy: "a long history of frequent conflict and warring with the other nomad group, the Aldecaldos" `[wiki]`; Saul kidnapped by Wraiths and held drugged in the cement factory `[wiki]`; the Wraiths attack the camp (`{sq027_com_nomad_defense}` 9, `{sq027_com_guards}` 3) `[game-data]`; Trevor Brass shot, Euralio Alma tortured, Jake Scooter wounded `[wiki]`; Wraiths hold Union Railroad Station and the Corp-Bud Cement Factory `[wiki]` `[game-data]` | `game-data+wiki` |
| Militech | `militech` | `hostile` | The Basilisk is stolen from a Militech convoy; Saul fears Militech tracing it and moving a strike team `[wiki]`; *Radar Love* steals the P9D/2.161 mobile radar, an **anti-nomad** surveillance system the clan wants to reverse-engineer `[game-data]` `[wiki]`; the Militech Detention Center holds border crossers (Bruce Welby) `[wiki]` `[game-data]`; Militech defends the Maglev site and the Arasaka approach in the *Star* branch `[wiki]`; 4 co-presence areas, all race crowds or the border wall `[game-data]` | `game-data+wiki` |
| Arasaka | `arasaka` | `neutral` | Canon history only: in the *Star* branch the clan assaults Arasaka Tower, Saul/Bob/Teddy die, and Mikoshi is reached — but that branch requires the Konpeki heist and the Relic plot, which this mod's timeline removes. No live Act-2 hostility; Arasaka secretly financed the Free States the veterans fought for in 2069–70, which is a grievance, not a current fight `[wiki]` `[design]` | `wiki+design` |
| Kang Tao | `kang_tao` | `neutral` | Canon history only: in *Lightning Breaks* / *Life During Wartime* Panam and V EMP the Kang Tao transport carrying Anders Hellman, the clan's salvage party is wiped out and Scorpion is killed. That job exists to seize Hellman's Relic knowledge, so this mod's removal of the Relic plot removes it. No independent Kang Tao–Aldecaldo incident is attested, and Kang Tao itself blamed the Raffen Shiv `[wiki]` `[game-data]` `[design]` | `game-data+wiki+design` |
| Biotechnica | `biotechnica` | `client` | Saul contracts the clan for crop protection and a lost-cargo recovery, paid in reverse-transpiration xerophytes rather than eddies; terms squeezed to −25% and reclassified "B41" with no insurance; Saul terminates all dealings after *Queen of the Highway* ("a conflict of interest … a clean conscience for the entire family") `[wiki]` `[game-data]`; no Biotechnica area at any Aldecaldo site `[game-data]` | `game-data+wiki` |
| Petrochem | `petrochem` | `rival` | Panam's recollection of Saul's "more adventurous days": he hijacked a Petrochem tanker, opened the valves and set the desert ablaze for the kids — a historical theft, not a 2077 operation `[wiki]`; the Petrochem Fuel Station (I-9) control centre is 1,087 m from the old camp and adjoins the DaKota autoshop's sub-territory `[game-data]` `[inferred]` | `wiki+inferred` |
| Barghest | `barghest` | `neutral` | No attested interaction. The only co-presence is `{ce_easy_com}_145` in Dogtown, a dynamic-event crowd of 5 Aldecaldos with no Barghest entry in the same area; the Barghest doc records the same neutrality `[game-data]` `[inferred]` | `game-data+inferred` |
| 6th Street | `sixth_street` | `trade` | Boz, a 6th Street lieutenant, hired Panam and Nash to move merchandise; Panam still calls him "a good guy" `[wiki]`; *Going-away Party* hires V to hand Flavio dos Santos to an Aldecaldo smuggler — the clan is 6th Street's extraction service `[wiki]` `[game-data]`; the 6th Street doc records `trade` in the other direction `[wiki]` | `game-data+wiki` |
| Animals | `animals` | `neutral` | No attested interaction; no shared community area `[game-data]` `[inferred]` | `inferred` |
| The Mox | `the_mox` | `neutral` | Only `{interesting_conversation_com_area}_344` (1 Aldecaldo, 1 Mox) and the city-race crowds `[game-data]`; Panam's Afterlife years are not a Mox tie `[inferred]` | `game-data+inferred` |
| Maelstrom | `maelstrom` | `neutral` | No attested interaction; co-presence is the border-crossing crowd (`q305`, `q301`) and the Maelstrom-turf garage where Josie Alcazar stashed a stolen bike — adjacency, not a relationship `[game-data]` `[inferred]`; the Maelstrom doc records the same neutrality | `game-data+inferred` |
| Voodoo Boys | `voodoo_boys` | `neutral` | No attested interaction. Zion Wylde, the Badlands cyberpsycho V hunts, was left psychotic by a VDB job, but he is not an Aldecaldo `[wiki]` `[inferred]` | `wiki+inferred` |
| Tyger Claws | `tyger_claws` | `rival` | Aldecaldo member **Josie Alcazar** stole a bike from a Tyger Claws boss and was killed by Tyger Claws; her body was found in the Glen wearing Aldecaldo clothes (*The Highwayman*) `[wiki]` `[game-data]` `mq029_01b_sm_josie_body`; otherwise only the city-race crowds (`mq056`/`sq024`, 2 Aldecaldos each) `[game-data]`. The Tyger Claws doc records `neutral` — a cross-doc asymmetry, see §5 | `game-data+wiki` |
| Valentinos | `valentinos` | `rival` | The Valentinos sold the nomads a stolen Militech SUV, took the eddies, beat them and refused delivery; the nomads' rep Dakota called Padre to recover it (*The Lord Giveth and Taketh Away*) `[wiki]` `[game-data]`; the Valentinos doc records `rival` — reciprocal | `game-data+wiki` |
| NCPD | `ncpd` | `hostile` | *Fortunate Son*: NCPD ambushes the implant pickup and tries to kill V, "as they believed Dakota was helping out Raffen Shiv and couldn't tell the difference between them and nomads" `[wiki]`; "cops don't like nomads" is standing nomad lore `[wiki]` `[lore]`; NCPD scanner hustles blanket the Badlands (Wraiths, not Aldecaldos) `[game-data]`; no corrupt NCPD channel is attested for this faction | `game-data+wiki` |
| Night Corp | `night_corp` | `neutral` | The *Star* escape route crosses Night Corp infrastructure (the Solar Arrays in Jackson Plains, the Coronado Dam overlook) but the clan uses the ground, it does not deal with the corp `[wiki]` `[inferred]` | `wiki+inferred` |
| City Council | `city_council` | `neutral` | Historical: in 2044 the Aldecaldos backed a Santo Domingo city-manager candidate who lost to the El Norte–funded **Theresa Valentino** `[wiki]` `[lore]`; no 2077 political channel is attested (Night City has no Aldecaldo ward) `[inferred]` | `wiki+inferred` |
| Scavengers | `scavengers` | `trade` | *Gun Music*: Carol, Cassidy and Teddy sell cyberware to a Scavenger crew in Arroyo because the clan "must really be desperate"; the deal nearly turns into a firefight and only closes on an intimidation check `[wiki]` `[game-data]`; no shared community area `[game-data]` | `game-data+wiki` |
| Regina Jones | `fixer_regina` | `trade` | Regina brokers two jobs the clan is inside: *Flight of the Cheetah* delivers Hwangbo to an Aldecaldo smuggling crew in Northside (`sts_wat_nid_03`, 3 Aldecaldos) `[game-data]` `[wiki]`; *Cyberpsycho Sighting: The Wasteland* targets the Aldecaldo Euralio Alma `[wiki]`; *Woman of La Mancha* can hand Anna Hamill to the clan (Nomad lifepath) `[wiki]` | `game-data+wiki` |
| Wakako Okada | `fixer_wakako` | `neutral` | No Aldecaldo-specific gig or lore link found `[inferred]` | `inferred` |
| Sebastian Ibarra (Padre) | `fixer_padre` | `trade` | Dakota called Padre when the Valentinos robbed the nomads; Padre ran the recovery of the stolen Militech SUV as a fixer-to-fixer favour (*The Lord Giveth and Taketh Away*) `[wiki]` `[game-data]`; a mediated debt, not a partnership | `game-data+wiki` |
| Muamar Reyes (El Capitán) | `fixer_el_capitan` | `trade` | *Going-away Party*: El Capitán pays V to deliver Flavio to an Aldecaldo smuggler — he buys the clan's extraction service `[wiki]` `[game-data]` | `game-data+wiki` |
| Dakota Smith | `fixer_dakota` | `ally` | Dakota **is an Aldecaldo** — a member, an elder and the clan's fixer; "eldest daughter of the Pomo tribe, eldest fixer in the Badlands" `[wiki]`; she runs the clan's whole gig chain (`sts_bls_ina_02/03/04/05/06/09/11`) and supplies the *Star* Net access `[game-data]` `[wiki]`. The row exists because fixers are a required row; it is degenerate — see §5 | `game-data+wiki` |
| Dino Dinovic | `fixer_dino` | `neutral` | No Aldecaldo-specific gig or lore link found `[inferred]` | `inferred` |
| Rogue Amendiares | `fixer_rogue` | `trade` | Panam worked Panam's gigs for Rogue after leaving the clan and was paired with Nash (a Wraith, which Panam did not know) `[wiki]`; "how things are going with Rogue… mostly stay out of each other's hair" `[wiki]`; Rogue's *Ghost Town* job is the clan's entry into the Hellman chain `[game-data]` | `game-data+wiki` |
| Mr. Hands | `fixer_mr_hands` | `neutral` | No Aldecaldo-specific gig or lore link found; his work is Dogtown `[inferred]` | `inferred` |
| Afterlife | `afterlife` | `trade` | Panam was an **Afterlife mercenary** — her record carries `q005_default` / `q103_afterlife_argument` workspots in the bar, and she appears there in canon quests including *Ghost Town* `[game-data]` `[wiki]`; she hoped to "start fresh in Night City, with Rogue, and with new friends" `[wiki]` | `game-data+wiki` |
| NUSA | `nusa` | `hostile` | The clan's core business is crossing the NUSA/SoCal border: smuggling exists because of the wall, Border Patrol "will want to stop any trespassers who try to jump the Border Crossing", and Militech — NUSA's nationalised force — holds the detention centre and defends the border `[wiki]` `[game-data]` `[wiki]`. The *Star* ending's escape run is the canon set piece built on this, but the border conflict stands on its own and survives the mod's timeline change | `game-data+wiki` |
| Netwatch | `netwatch` | `neutral` | No attested interaction; the clan has one netrunner (Carol) and no Net-facing operations `[inferred]` | `inferred` |

Stance counts (29 rows): **hostile 3, war 1, rival 3, trade 7, neutral 13,
client 1, ally 1, patron 0.** The single `ally` row is degenerate (Dakota is a
member). The single `client` row is the Biotechnica contract, which the clan
itself terminates. Arasaka and Kang Tao dropped from `hostile` to `neutral`
because each row's only evidence is a branch this mod's timeline removes (the
*Star* Tower assault and the Hellman extraction). So the honest reading is:
**no external ally, one live employer, one war, and three hostile great
powers.** `[inferred]`

### 3.3 Actors outside `data/factions.json`

Real relationships with no faction code, so prose only:

- **Snake Nation** — the Seven Nations member the clan may join; Scorpion's
  cause, and the source of the *Star* branch's tunnel intelligence. A political
  option, not a faction in `data/factions.json`. `[wiki]`
- **The Seven Nations** — the treaty body of nomad nations (Aldecaldos, Snake,
  Blood, Folk, Jodes, Thelas, MetaCorp). Membership is the clan's diplomatic
  identity; the 2041 near-war with the **Jodes** outside Night City is the one
  recorded inter-nation confrontation. `[wiki]` `[lore]`
- **Raffen Shiv** — the outcast category, not a faction; the Wraiths are its
  Night City expression. Exile is the clan's ultimate sanction. `[wiki]`
- **The Bakkers** — V's birth clan in the Nomad prologue; "recently merged into"
  Snake Nation. Not the Aldecaldos; do not seed their garage as an Aldecaldo
  site. `[wiki]`
- **The Blaine Family** — another Aldecaldo family (leader Tommy Blaine), with no
  2077 presence. Evidence that the "faction" is federal. `[wiki]`
- **The Lobos** — the nation's elite commando arm (2023 Arasaka Towers, 2045
  Night Market security). No 2077 records. `[wiki]` `[lore]`
- **Sightseers; Aldecaldo Peacekeepers** — 2045 Aldecaldo packs/organisations
  (East Cargo Village; Santo Domingo HQ) with no 2077 presence. `[wiki]` `[lore]`
- **StormTech** — the corporation that partnered with the Aldecaldos on the
  post-Holocaust Night City rebuild in the 2040s. Historical partner, no 2077
  link. `[wiki]` `[lore]`
- **Jeffrey Simmons / Rahima Acreman** — the Biotechnica counterparties (senior
  PM; contract termination). Individual channels, not a faction. `[wiki]`
- **Noah** — Sunset Motel owner and bartender; Panam's lodging in Wraith
  country. A neutral civilian, not a contact. `[wiki]`
- **Joss Kutcher** — River Ward's sister; her *husband* was an Aldecaldo. She is
  not a member and must not be recruited as one. `[wiki]`
- **Boz** — 6th Street lieutenant and Panam's former client; the personal link
  behind the `trade` row. `[wiki]`

### 3.4 Guarantor assessment

The design question: if a player founds a gang, which factions would guarantee
the Aldecaldos' support, and which would the Aldecaldos guarantee?

- **No external ally exists.** The matrix has one `ally` row and it is a member.
  There is no faction that would fight for the clan. `[inferred]`
- **The clan's political capital is four things**: the family's reputation for
  finishing a job ("the Aldecaldos never leave a job unfinished"), Dakota's
  fixer network, the smuggling corridor, and the veterans' military skill. Three
  are reputational and one is a person. All are fragile. `[wiki]`
- **The Aldecaldos are a good guarantor and a poor client.** They genuinely
  honour contracts (Saul cuts his own rate rather than break one) and they can
  put an armoured convoy or a stolen panzer on a road. What they cannot do is
  absorb a loss: one wiped salvage party costs them Scorpion. `[wiki]`
  `[inferred]`
- **Plausible guarantors for a player-founded gang** are transactional, not
  ideological: Dakota (money, contracts, intelligence — if the player is not her
  enemy), 6th Street (extraction and courier work), El Capitán (a delivery
  contract), Padre (mediation, as he mediated the SUV debt), and Panam
  personally if the player earned it — she promises the clan's help "at any
  cost" to V. None is a bloc. `[game-data]` `[wiki]` `[inferred]`
- **The Aldecaldos as an aggressor.** For a player founding a gang on a
  Wraith-held or Militech-adjacent Badlands point, the clan is a plausible
  **pre-emptive attacker**: it wars the Wraiths as a matter of course, raids
  Militech convoys for hardware, and its veterans are the best light armour on
  the map. It is *not* an expansionist — it does not take urban turf. That is
  consistent with its `war`/`hostile` rows and its zero city sub-districts.
  `[inferred]`

---

## 4. Pillar notes

Design claims from `docs/design/gameplay-systems.md`: the Aldecaldos are a
**Tribe** (archetype strength **Culture**, weakness **Espionage**); faction
strength **Economy**, weakness **Technology**.

| Pillar | Design claim | Lore verdict | Evidence |
| --- | --- | --- | --- |
| Culture (archetype strength) | Tribes bind through culture | **Strongly supported, and it is the faction's real power.** The nomad code (six founding rules, three surviving rules), "protect your family and clan — in that order", the adoption ritual, the camp funeral, the saying "she who lives in the hearts of her loved ones can never truly die", and the veterans' shared war. It converts outsiders into family (V, Welby, Hamill) and it survives losing everything material. | Nomad code shard; *We Gotta Live Together* initiation; `mq001_com_funeral_nomads` (13); Trevor's Last Ride saying; adoption of V/Welby/Hamill `[wiki]` `[game-data]` |
| Espionage (archetype weakness) | Tribes are bad at intelligence | **Strongly supported — this is the clan's most consistent failure.** They do not know the Kang Tao AV is armed and lose a salvage party; they cannot break Militech's dynamic encryption ("we won't squeeze out more than this"); they do not know Nash is Raffen Shiv; Saul is taken on a small patrol because nobody saw the Wraiths massing; Carol is their only netrunner, and she is a technician first. Their intelligence is *borrowed* (Dakota, Snake Nation, Rogue). | *Lightning Breaks*; Saul's computer *Militech won't give up*; *Ghost Town*; *Riders on the Storm*; `q114_after_alt` / Dakota's Net access `[wiki]` `[game-data]` |
| Economy (faction strength) | The faction is economically strong | **Supported, but as *diversified fragility*.** Legal-plus-illegal breadth is real: salvage and reconstruction of dead cities, seasonal farm labour, bootlegging, long-haul smuggling to Chicago and Phoenix, passenger transport, mercenary work, and Dakota's fixer brokerage and autoshop. But there is no fixed asset except the autoshop, one contract can dominate the camp's income, and one bad convoy costs a specialist. Model it as **high output, no reserves**, not as wealth. | Aldecaldos overview and *Behind the Scenes*; the Biotechnica negotiation; `../aldecaldos.md` §4 `[wiki]` `[game-data]` |
| Technology (faction weakness) | The faction is weak at technology | **Supported — they are adapters, not innovators.** The Basilisk is stolen and assembled; the P9D radar is stolen to be reverse-engineered; the camp has a ripperdoc and gunsmith but no lab; Cassidy uses no cyberware at all. Their tech edge is *maintenance* (Mitch, Bob, Carol keep 40-year-old panzers alive) rather than invention. | Basilisk assembly; *Radar Love*; Cassidy "did not use any cyberware"; camp vendors `[wiki]` `[game-data]` |
| Overall fit | The pillars fit the faction's identity | **Good, with one correction.** Culture and Economy are right. Technology as *weakness* should mean "cannot innovate or secure its own systems", not "poorly equipped" — a nomad convoy is heavily armed. Espionage as the archetype weakness is the best-supported claim in the whole set. | Synthesis of the rows above `[inferred]` |

Design cautions, not redesigns:

- **Do not model the Aldecaldos as poor.** Model them as rich in capability and
  poor in reserves: they can field a panzer and cannot replace Scorpion.
- **Do not model Culture as soft.** The nomad code is enforceable — exile is
  real, and exile creates the Wraiths. Culture is this faction's *military*
  logistics.
- **Espionage weakness should bite in the simulation.** Give the clan delayed or
  wrong intelligence: it should learn about a threat one step late, which is
  exactly what happens to Saul, to the Kang Tao salvage party, and to Panam with
  Nash.

---

## 5. Gaps and uncertainties

1. **No offline attitude matrix.** `Attitude_Record.hpp` is opaque and
   `Affiliation.hpp` is identity only, so every stance in §3.2 is judged from
   quests, wiki and adjacency. The neutral rows are placeholders, not findings.
2. **The 2077 leadership is not in `data/sites/rosters.json`.** The faction's 5
   roster sites / 8 units are all generic quest NPCs; Saul, Panam, Carol,
   Cassidy, Mitch, Bob, Teddy, Scorpion and Dakota exist only in the raw sector
   community registry. A roster-only pipeline finds nobody.
3. **Every leader is V-dependent.** Saul dies in the *Star* branch; Panam's
   co-leadership requires *Queen of the Highway*; Carol's interim leadership
   exists only during *Riders on the Storm*. A simulation must choose a branch
   or model all three.
4. **Dakota's `open_world: true` is an inference, not a spawn test.** It rests on
   the campaign sanitizer preserving `FixerVariant` pins and on her
   `default` / `ina_06` / `ina_07` phases. Verify in-game that she stands at the
   autoshop with the campaign disabled.
5. **Cross-doc asymmetry: Tyger Claws.** This document records `rival` (the Josie
   Alcazar killing); the Tyger Claws politics doc records `neutral` toward the
   Aldecaldos. One side is wrong, or the METHOD needs an explicit rule for
   recording an *unreciprocated* incident. I record the incident and flag it
   rather than match the neighbour.
6. **Arasaka hostility is branch-only, and the branch is removed.** There is no
   live Act-2 Aldecaldo–Arasaka conflict; the old row reflected the *Star*
   ending, which needs the Konpeki heist and the Relic plot. This mod's timeline
   removes them, so the row now reads `neutral`.
7. **Kang Tao hostility is branch-only too, and covert when it exists.** The
   old row rested on the Hellman extraction; with the Relic plot removed the
   incident never happens. Even in canon Kang Tao believed the Raffen Shiv did
   it. The row now reads `neutral`, and a simulation should not surface an open
   war that no one involved admits to.
8. **The 2077 "faction" is a pack.** The Aldecaldos nation has tens of thousands
   of members and several families; faction id 9 is the Bright Family plus
   Dakota. Nation-level politics (Seven Nations, the Jodes near-war, Snake
   Nation accession) have no 2077 records and are prose only.
9. **The ambient caravan camp is real but unnamed.** `{post_ma_bls_ina_se1_22_com}`
   `(4831.9, -1378.2, 136.7)` holds 23 entries with day/night variants, no
   marker, no `sites.json` row, a Militech CC 1,270.8 m away, and a `post_`
   prefix tying it to the *Second Chances* cyberpsycho site. It is the only
   ambient Aldecaldo crowd and a good in-game test, but it is not a seat and
   must not be seeded as one.
10. **No membership counts.** `areas.jsonl` entry counts are presence proxies and
    the camp communities are overlapping quest phases. `{sq004_com_nomads}` (20)
    and `{q114_com_nomad_party_mood_scenes}` (25) are two scenes of the same
    camp at different story times, not 45 people.
11. **`entryActiveOnStart` is 0 for every named NPC.** Presence class is derived
    from phase names and wiki behaviour, not from that field.
12. **Two inferred character records.** Taco and Jeff have no named records (the
    generic `{mq002_com_nomads}` pair is the best candidate); Trevor Brass and
    Anna Hamill have none at all. Emily Scooter has no distinct record and is
    not the `emily` sniper entry.
13. **The family council is mentioned once and never shown.** Saul's "family
    council" is the only deliberative body in the record; its membership,
    procedure and authority are unstated. Any council mechanic is invention.
14. **Adoption is attested but not formalised.** V is welcomed by declaration and
    ritual; Welby and Hamill join through gigs. There is no name for the
    probationary stage beyond "informal member."
15. **Joss Kutcher is not a member.** Her husband was the Aldecaldo; she is River
    Ward's sister and a Red Peaks civilian. Do not treat her as clan.
16. **The Nomad prologue is the Bakkers.** `q000_*` nomads (border patrol
    guards, civilians, the Yucca garage) are V's Bakker clan, now merged into
    Snake Nation — not the Aldecaldos. `[game-data]` `[wiki]`
17. **Saul's Afterlife phase is the Sun-ending path.** `q115_ws_saul_afterlife`
    belongs to *For Whom the Bell Tolls*; it is not a standing 2077 presence and
    must not be read as one.
18. **No camp garrison records.** `sq027_com_nomad_defense` (9) plus
    `{sq027_com_guards}` (3) is the only defended-camp community; the rest are
    mood scenes and story crowds. There is no patrol or guard record for the
    camp in `data/sites/`.
19. **Phantom Liberty adds no Aldecaldo leadership content.** The only PL-era
    presence is civilian crowds (`q301_com_border_community`,
    `{ce_easy_com}_145` in Dogtown) and Carol's optional netrunner favour in
    *Black Steel in the Hour of Chaos*, which requires the Panam side jobs. `[wiki]`
    `[game-data]`
20. **"Static" is undefined in data.** Dakota's own self-description is the only
    definition; there is no faction attribute for it. If the mod models
    settled-versus-mobile members, that is new vocabulary.

### 5.1 Sources consulted

- Local: `data/factions.json`, `data/sites/rosters.json`,
  `data/sites/sites.json`, `data/sub_territories.json`,
  `data/control_centers.json`, `data/faction_headquarters.json`,
  `data/districts.json`, `dist/extract/areas.jsonl`,
  `dist/extract/markers.jsonl`,
  `dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_{0,1,2}.streamingsector.json`
  (`worldCommunityRegistryNode` templates, `communitiesData`, phases, workspots,
  and the `#post_ma_ina_se1_22` prefab paths),
  `docs/research/campaign-sanitizer.md`, `docs/research/factions/aldecaldos.md`,
  `docs/research/factions/METHOD.md`, `docs/design/gameplay-systems.md`.
- Wiki: [Aldecaldos](https://cyberpunk.fandom.com/wiki/Aldecaldos),
  [Aldecaldos Members](https://cyberpunk.fandom.com/wiki/Aldecaldos_Members),
  [Bright Family](https://cyberpunk.fandom.com/wiki/Bright_Family),
  [Aldecaldo Camp (2077)](https://cyberpunk.fandom.com/wiki/Aldecaldo_Camp_(2077)),
  [Saul Bright](https://cyberpunk.fandom.com/wiki/Saul_Bright),
  [Saul Bright/Computers](https://cyberpunk.fandom.com/wiki/Saul_Bright/Computers),
  [Panam Palmer](https://cyberpunk.fandom.com/wiki/Panam_Palmer),
  [Panam Palmer/Computers](https://cyberpunk.fandom.com/wiki/Panam_Palmer/Computers),
  [Mitch Anderson](https://cyberpunk.fandom.com/wiki/Mitch_Anderson),
  [Carol Emeka](https://cyberpunk.fandom.com/wiki/Carol_Emeka),
  [Cassidy Righter](https://cyberpunk.fandom.com/wiki/Cassidy_Righter),
  [Bob Sagan](https://cyberpunk.fandom.com/wiki/Bob_Sagan),
  [Teddy Simos](https://cyberpunk.fandom.com/wiki/Teddy_Simos),
  [Driss Meriana](https://cyberpunk.fandom.com/wiki/Driss_Meriana),
  [Dakota Smith](https://cyberpunk.fandom.com/wiki/Dakota_Smith),
  [Nomad Santiago](https://cyberpunk.fandom.com/wiki/Nomad_Santiago),
  [Snake Nation](https://cyberpunk.fandom.com/wiki/Snake_Nation),
  [Seven Nations](https://cyberpunk.fandom.com/wiki/Seven_Nations),
  [Nomad](https://cyberpunk.fandom.com/wiki/Nomad),
  [Raffen Shiv](https://cyberpunk.fandom.com/wiki/Raffen_Shiv),
  [Wraiths](https://cyberpunk.fandom.com/wiki/Wraiths),
  [Unification War](https://cyberpunk.fandom.com/wiki/Unification_War),
  [Rogue Amendiares](https://cyberpunk.fandom.com/wiki/Rogue_Amendiares),
  [Boz](https://cyberpunk.fandom.com/wiki/Boz),
  [Nash](https://cyberpunk.fandom.com/wiki/Nash),
  quests: [Ghost Town](https://cyberpunk.fandom.com/wiki/Ghost_Town),
  [Lightning Breaks](https://cyberpunk.fandom.com/wiki/Lightning_Breaks),
  [Life During Wartime](https://cyberpunk.fandom.com/wiki/Life_During_Wartime),
  [Riders on the Storm](https://cyberpunk.fandom.com/wiki/Riders_on_the_Storm),
  [With a Little Help from My Friends](https://cyberpunk.fandom.com/wiki/With_a_Little_Help_from_My_Friends),
  [Queen of the Highway](https://cyberpunk.fandom.com/wiki/Queen_of_the_Highway),
  [Gun Music](https://cyberpunk.fandom.com/wiki/Gun_Music),
  [Fortunate Son](https://cyberpunk.fandom.com/wiki/Fortunate_Son),
  [We Gotta Live Together](https://cyberpunk.fandom.com/wiki/We_Gotta_Live_Together),
  [Forward to Death](https://cyberpunk.fandom.com/wiki/Forward_to_Death),
  [Belly of the Beast](https://cyberpunk.fandom.com/wiki/Belly_of_the_Beast),
  [All Along the Watchtower](https://cyberpunk.fandom.com/wiki/All_Along_the_Watchtower),
  [Every Grain of Sand](https://cyberpunk.fandom.com/wiki/Every_Grain_of_Sand),
  [The Highwayman](https://cyberpunk.fandom.com/wiki/The_Highwayman),
  gigs: [No Fixers](https://cyberpunk.fandom.com/wiki/Gig:_No_Fixers),
  [MIA](https://cyberpunk.fandom.com/wiki/Gig:_MIA),
  [Trevor's Last Ride](https://cyberpunk.fandom.com/wiki/Gig:_Trevor%27s_Last_Ride),
  [Radar Love](https://cyberpunk.fandom.com/wiki/Gig:_Radar_Love),
  [Flying Drugs](https://cyberpunk.fandom.com/wiki/Gig:_Flying_Drugs),
  [Goodbye, Night City](https://cyberpunk.fandom.com/wiki/Gig:_Goodbye,_Night_City),
  [Woman of La Mancha](https://cyberpunk.fandom.com/wiki/Gig:_Woman_of_La_Mancha),
  [The Lord Giveth and Taketh Away](https://cyberpunk.fandom.com/wiki/Gig:_The_Lord_Giveth_and_Taketh_Away),
  [Going-away Party](https://cyberpunk.fandom.com/wiki/Gig:_Going-away_Party),
  [Flight of the Cheetah](https://cyberpunk.fandom.com/wiki/Gig:_Flight_of_the_Cheetah),
  [Black Steel in the Hour of Chaos](https://cyberpunk.fandom.com/wiki/Black_Steel_in_the_Hour_of_Chaos),
  [Cyberpsycho Sighting: The Wasteland](https://cyberpunk.fandom.com/wiki/Cyberpsycho_Sighting:_The_Wasteland),
  [Cyberpsycho Sighting: Second Chances](https://cyberpunk.fandom.com/wiki/Cyberpsycho_Sighting:_Second_Chances),
  shards: [Excerpts from "A History of the Nomads" by B.B. Pires](https://cyberpunk.fandom.com/wiki/Excerpts_from_%22A_History_of_the_Nomads%22_by_B.B._Pires),
  [Nomads for the Thick-Skinned](https://cyberpunk.fandom.com/wiki/Nomads_for_the_Thick-Skinned).
- Earlier repo research: `docs/research/factions/politics/METHOD.md`,
  `docs/research/factions/politics/maelstrom.md` (worked example),
  `docs/research/factions/aldecaldos.md`.

---

## 6. Machine-readable block

```json
{
  "faction_code": "aldecaldos",
  "leaders": [
    {
      "name": "Saul Bright",
      "role": "Bright Family leader (Act 2); co-leader after Queen of the Highway; canon kills him in the Star ending, which the mod's timeline removes",
      "character_record_id": "Character.Saul",
      "location_name": "Aldecaldo Mobile Camp (old camp) / Nomad Camp",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_1 community registry entry saul, initial phase default, phases default_newcamp/holocall/q114_*; markers {saul_sm_default}, q114_02_sm_saul_sitrep; wiki Saul Bright",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Panam Palmer",
      "role": "Ex-member turned mercenary; co-leader (branch); full leader after Saul's death (Star branch)",
      "character_record_id": "Character.Panam",
      "location_name": "Aldecaldo Mobile Camp / Nomad Camp / Afterlife",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_1 registry entry panam, phases default/default_newcamp/default_hug/holocall/q103_afterlife_argument/q005_default; markers {panam_sm_default}, {panam_sm_hug_default}; wiki Panam Palmer",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Carol Emeka",
      "role": "Interim leader while Saul is abducted; netrunner and technician; Unification War veteran",
      "character_record_id": "Character.Carol",
      "location_name": "Aldecaldo Mobile Camp",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_1 registry entry carol, phases default/default_newcamp/mq002_deal/q114_driller_ctrls; marker {carol_sm_default}; wiki Carol Emeka",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Cassidy Righter",
      "role": "Clan elder and best shot in camp; veteran; Panam's protector and the camp's moral referee",
      "character_record_id": "Character.Cassidy",
      "location_name": "Aldecaldo Mobile Camp / Corp-Bud Railroad Station",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_1 registry entry cassidy, phases default/default_newcamp/mq002_deal/q114_dampening_*; markers cassidy_sm_default, sq027_04_sm_preparations_cassidy_teddy; wiki Cassidy Righter",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Mitch Anderson",
      "role": "Veteran lieutenant; panzerboy and mechanic; Panam's closest ally and the natural regent",
      "character_record_id": "Character.Mitch",
      "location_name": "Aldecaldo Mobile Camp / Nomad Camp / Maglev assault (Basilisk pilot)",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_1 registry entry Mitch, phases default/mitch_default_active/default_newcamp/mq001_camp_funeral; markers {mitch_sm_default}, {fb_sm_mitch}; wiki Mitch Anderson",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Bob Sagan",
      "role": "Techie and veteran; canon dies at the Maglev site in the Star ending, which the mod's timeline removes",
      "character_record_id": "Character.Bob",
      "location_name": "Aldecaldo Mobile Camp / Nomad Camp",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_1 registry entry Bob, phases default/default_newcamp/q114_bob_arasaka/q114_bob_attack; marker {bob_sm_default}; wiki Bob Sagan",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Theodore \"Teddy\" Simos",
      "role": "Member and veteran; canon dies at the Maglev site in the Star ending, which the mod's timeline removes",
      "character_record_id": "Character.Teddy",
      "location_name": "Aldecaldo Mobile Camp / Nomad Camp",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_1 registry entry Teddy, phases #sq027_teddy_post_final_scene/default/default_newcamp/q114_construction; marker {teddy_sm_default}; wiki Teddy Simos",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Driss \"Scorpion\" Meriana",
      "role": "Veteran panzerboy; demoted dissident after proposing Snake Nation (2070); killed by Kang Tao (2077)",
      "character_record_id": "Character.Scorpion",
      "location_name": "Aldecaldo camp funeral zone / Kang Tao crash site",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_1 registry entry scorpion, initial phase mq001_camp, phases q103_ws_scorpion_goodbye/q104_scorpion_dead; wiki Driss Meriana; Saul Bright/Computers Third option",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Dakota Smith",
      "role": "Fixer and clan elder (static); the pack's economic interface, outside the command chain",
      "character_record_id": "Character.dakota_smith",
      "location_name": "DaKota autoshop / Nomad Camp trailer",
      "presence_class": "world-activity",
      "open_world": true,
      "source": "raw always_loaded_1 registry entry dakota, phases default/ina_06_ws_dakota_working/ina_07_dakota_waiting/q114_dakota_initiation_01; markers ina_07_mp_workshop, q114_03c_sm_dakota_trailer; wiki Dakota Smith; campaign-sanitizer keeps FixerVariant",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "name": "Juan Aldecaldo",
      "role": "Nation founder and first leader (1992-2015)",
      "character_record_id": null,
      "location_name": null,
      "presence_class": "historical",
      "open_world": false,
      "source": "wiki Aldecaldos (Main Leaders); wiki Aldecaldos Members",
      "confidence": "wiki"
    },
    {
      "name": "Nomad Santiago",
      "role": "Nation leader (2015-2045+); appointed by Juan; forged the Seven Nations in 2017",
      "character_record_id": null,
      "location_name": null,
      "presence_class": "historical",
      "open_world": false,
      "source": "wiki Nomad Santiago; wiki Aldecaldos (Main Leaders)",
      "confidence": "wiki"
    }
  ],
  "internal_factions": [
    {
      "name": "Saul's contract line (pragmatists)",
      "leader": "Saul Bright",
      "goals": "A steady corporate contract for the family, self-sufficiency through paid work, avoid anything that risks the clan's income",
      "members_hint": "Saul; Carol as interim; the camp's non-combatants; {sq004_com_nomads} 20, {q103_com_dlg_nomads} 6",
      "source": "Biotechnica negotiation paid in reverse-transpiration xerophytes; Saul Bright/Computers New contract and We are done here; Riders on the Storm",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Panam's independence bloc (the Basilisk crew)",
      "leader": "Panam Palmer",
      "goals": "No corporate dependence; strength through force and reputation; later the border and a fresh start",
      "members_hint": "Mitch, Cassidy, Bob, Teddy, Carol, Scorpion (posthumously); {sq027_com_nomad_defense} 9, {sq027_com_guards} 3, {q114_com_nomad_party_mood_scenes} 25",
      "source": "With a Little Help from My Friends (like-minded clan members); Queen of the Highway; the Militech convoy heist",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The Snake Nation current (the third option)",
      "leader": null,
      "goals": "Join Snake Nation rather than serve corporations; stay nomads instead of becoming corporate labour",
      "members_hint": "No dedicated community; circulates among the veterans; Scorpion was the original advocate",
      "source": "Saul Bright/Computers message Third option; Scorpion demoted and given no assignments for a year; the idea revived in 2077 per With a Little Help from My Friends",
      "confidence": "wiki"
    },
    {
      "name": "The veterans' brotherhood",
      "leader": "Mitch Anderson (senior voice, with Cassidy Righter)",
      "goals": "The family as a soldiers' mutual-aid society; contempt for the corporate world that used them",
      "members_hint": "The Unification War cohort: Mitch, Scorpion, Carol, Cassidy, Bob, Teddy - six of the camp's named members",
      "source": "Unification War service; panzerboy drug cocktails and PTSD; Carol's database entry on the army as another corporation",
      "confidence": "wiki"
    },
    {
      "name": "Dakota's static wing (broker and asset)",
      "leader": "Dakota Smith",
      "goals": "Keep the Badlands ecosystem running, earn from those who come and go, oppose detachment from nomad life",
      "members_hint": "DaKota autoshop; her gig chain sts_bls_ina_02/03/04/05/06/09/11; Every Grain of Sand",
      "source": "wiki Dakota Smith (statics take care of those who come and go; the ecosystem speech); gig messages",
      "confidence": "game-data+wiki"
    }
  ],
  "relations": [
    {
      "faction_code": "wraiths",
      "stance": "war",
      "evidence": "Long history of frequent conflict and warring [wiki]; Saul kidnapped and held drugged in the cement factory [wiki]; Wraiths attack the camp, {sq027_com_nomad_defense} 9 + {sq027_com_guards} 3 [game-data]; Trevor Brass shot, Euralio Alma tortured, Jake Scooter wounded [wiki]; Wraiths hold the Corp-Bud Cement Factory and Union Railroad Station [wiki] [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "militech",
      "stance": "hostile",
      "evidence": "Basilisk stolen from a Militech convoy and Saul fears the trace [wiki]; Radar Love steals the P9D/2.161 anti-nomad mobile radar for reverse engineering [game-data] [wiki]; Militech Detention Center holds border crossers (Bruce Welby) [wiki]. In canon Militech also defends the Maglev site and Arasaka approach in the Star branch, but the hostility stands on the base-game incidents above",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "arasaka",
      "stance": "neutral",
      "evidence": "Canon history only: in the Star branch the clan assaults Arasaka Tower, Saul/Bob/Teddy die, and Mikoshi is reached - but that branch requires the Konpeki heist and the Relic plot, which this mod's timeline removes. No live Act-2 hostility; Arasaka secretly financed the Free States the veterans fought for in 2069-70, which is a grievance, not a current fight [wiki] [design]",
      "confidence": "wiki+design"
    },
    {
      "faction_code": "kang_tao",
      "stance": "neutral",
      "evidence": "Canon history only: in Lightning Breaks / Life During Wartime Panam and V EMP the Kang Tao transport carrying Anders Hellman, the clan's salvage party is wiped out and Scorpion is killed. That job exists to seize Hellman's Relic knowledge, so this mod's removal of the Relic plot removes it. No independent Kang Tao-Aldecaldo incident is attested, and Kang Tao itself blamed the Raffen Shiv [wiki] [game-data] [design]",
      "confidence": "game-data+wiki+design"
    },
    {
      "faction_code": "biotechnica",
      "stance": "client",
      "evidence": "Saul contracts crop protection and lost-cargo recovery, paid in reverse-transpiration xerophytes; terms cut 25 percent and reclassified B41 with no insurance; Saul terminates all dealings after Queen of the Highway [wiki] [game-data]; no Biotechnica area at any Aldecaldo site [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "petrochem",
      "stance": "rival",
      "evidence": "Panam recalls Saul hijacking a Petrochem tanker and setting the desert ablaze in his adventurous years, a historical theft not a 2077 operation [wiki]; the Petrochem Fuel Station (I-9) CC is 1087 m from the old camp and adjoins the DaKota autoshop sub-territory [game-data] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "barghest",
      "stance": "neutral",
      "evidence": "No attested interaction; the only co-presence is the Dogtown dynamic-event crowd {ce_easy_com}_145, and the Barghest doc records the same neutrality [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "sixth_street",
      "stance": "trade",
      "evidence": "Boz, a 6th Street lieutenant, hired Panam and Nash to move merchandise and Panam still calls him a good guy [wiki]; Going-away Party hands Flavio dos Santos to an Aldecaldo smuggler [wiki] [game-data]; the 6th Street doc records trade reciprocally [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "animals",
      "stance": "neutral",
      "evidence": "No attested interaction and no shared community area [game-data] [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "the_mox",
      "stance": "neutral",
      "evidence": "Only {interesting_conversation_com_area}_344 (1 Aldecaldo, 1 Mox) and the city-race crowds [game-data]; no economic or violent link [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "maelstrom",
      "stance": "neutral",
      "evidence": "No attested interaction; co-presence is the border-crossing crowds q305/q301 and the Maelstrom-turf garage where Josie stashed a stolen bike, which is adjacency [game-data] [inferred]; the Maelstrom doc agrees",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "voodoo_boys",
      "stance": "neutral",
      "evidence": "No attested interaction; Zion Wylde was left psychotic by a VDB job but is not an Aldecaldo [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "tyger_claws",
      "stance": "rival",
      "evidence": "Aldecaldo member Josie Alcazar stole a Tyger Claws boss bike and was killed by Tyger Claws, body found in the Glen wearing Aldecaldo clothes (The Highwayman) [wiki] [game-data]; otherwise only city-race crowds [game-data]; the Tyger Claws doc records neutral, an unresolved asymmetry",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "valentinos",
      "stance": "rival",
      "evidence": "Valentinos sold the nomads a stolen Militech SUV, took the eddies, beat them and refused delivery; Dakota called Padre to recover it (The Lord Giveth and Taketh Away) [wiki] [game-data]; the Valentinos doc records rival reciprocally",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "ncpd",
      "stance": "hostile",
      "evidence": "Fortunate Son: NCPD ambushes the implant pickup and tries to kill V, believing Dakota helped Raffen Shiv and unable to tell them from nomads [wiki]; cops do not like nomads in standing nomad lore [wiki] [lore]; NCPD scanner hustles blanket the Badlands [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "night_corp",
      "stance": "neutral",
      "evidence": "The Star escape crosses Night Corp infrastructure (Solar Arrays, Coronado Dam) but the clan uses the ground without dealing with the corp [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "city_council",
      "stance": "neutral",
      "evidence": "Historical: in 2044 the Aldecaldos backed a Santo Domingo city-manager candidate who lost to the El Norte-funded Theresa Valentino [wiki] [lore]; no 2077 political channel is attested [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "scavengers",
      "stance": "trade",
      "evidence": "Gun Music: Carol, Cassidy and Teddy sell cyberware to a Scavenger crew in Arroyo because the clan is desperate; the deal nearly becomes a firefight and closes only on an intimidation check [wiki] [game-data]; no shared community area [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_regina",
      "stance": "trade",
      "evidence": "Regina brokers Flight of the Cheetah, which delivers Hwangbo to an Aldecaldo smuggling crew at sts_wat_nid_03 (3 Aldecaldos) [game-data] [wiki]; Cyberpsycho Sighting: The Wasteland targets the Aldecaldo Euralio Alma [wiki]; Woman of La Mancha can hand Anna Hamill to the clan [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_wakako",
      "stance": "neutral",
      "evidence": "No Aldecaldo-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_padre",
      "stance": "trade",
      "evidence": "Dakota called Padre when the Valentinos robbed the nomads and he ran the recovery of the stolen Militech SUV as a fixer-to-fixer favour (The Lord Giveth and Taketh Away) [wiki] [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_el_capitan",
      "stance": "trade",
      "evidence": "Going-away Party: El Capitan pays V to deliver Flavio dos Santos to an Aldecaldo smuggler, buying the clan's extraction service [wiki] [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_dakota",
      "stance": "ally",
      "evidence": "Dakota Smith is an Aldecaldo member, elder and the clan's fixer (eldest daughter of the Pomo tribe, eldest fixer in the Badlands) [wiki]; she runs the clan's gig chain and supplies the Star-branch Net access [game-data] [wiki]; degenerate row, she is inside the faction",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "faction_code": "fixer_dino",
      "stance": "neutral",
      "evidence": "No Aldecaldo-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_rogue",
      "stance": "trade",
      "evidence": "Panam worked Rogue's gigs after leaving the clan and was paired with Nash, a Wraith she did not know [wiki]; Rogue's Ghost Town job opens the Hellman chain [game-data]; Panam says they mostly stay out of each other's hair [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_mr_hands",
      "stance": "neutral",
      "evidence": "No Aldecaldo-specific gig or lore link found; his work is Dogtown [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "afterlife",
      "stance": "trade",
      "evidence": "Panam was an Afterlife mercenary, with q005_default and q103_afterlife_argument workspots in the bar and appearances during The Heist and Ghost Town [game-data] [wiki]; she hoped to start fresh in Night City with Rogue [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "nusa",
      "stance": "hostile",
      "evidence": "The clan's business is crossing the NUSA-SoCal border; smuggling exists because of the wall, Border Patrol will want to stop any trespassers who try to jump the Border Crossing, and Militech, NUSA's nationalised force, holds the detention centre and defends the border [game-data] [wiki]. The Star ending's escape run is the canon set piece built on this, but the border conflict stands on its own and survives the mod's timeline change",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "netwatch",
      "stance": "neutral",
      "evidence": "No attested interaction; the clan has one netrunner (Carol) and no Net-facing operations [inferred]",
      "confidence": "inferred"
    }
  ]
}
```
