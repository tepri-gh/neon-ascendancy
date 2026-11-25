# Voodoo Boys — Leadership, Internal Politics and External Relations

Status: faction research run, 2026-11-25. One faction, one document.
Scope: Cyberpunk 2077 2.5 + Phantom Liberty, campaign disabled. This document
covers who a player can join under, climb past, ally with or remove; the internal
blocs; and the external relations matrix needed for wars, alliances and
"guarantor" support when a player founds a gang.

Method: follows [`METHOD.md`](./METHOD.md) (tags, local-data precedence, wiki
usage) and uses the Maelstrom pilot ([`maelstrom.md`](./maelstrom.md)) as the
worked example. The location catalog for the Voodoo Boys is
[`../voodoo-boys.md`](../voodoo-boys.md); this document does not re-derive
coordinates — it maps people and politics onto those places.

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/comic/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My reasoning links a named person, place or stance to a record; reasoning stated | Weak, flagged |

Extra convention for this document only: **presence class**.
`ambient` = persists in free roam without a quest; `world-activity` = gig,
scanner hustle or NCPD activity, i.e. free-roam content but still
activity-gated; `story` = gated by the base-game *M'ap Tann Pèlen* / *I Walk the
Line* / *Transmission* chain or the Phantom Liberty main job *The Damned*;
`historical` = not present in 2077. The JSON `open_world` flag is `true` for
`ambient` + `world-activity`, `false` for `story` + `historical`.

---

## 1. Leadership and ranks

### 1.1 The 2077 chain of command

The Voodoo Boys are not a corporate hierarchy. They are a **netrunner
collective** that also acts as the de facto government of Pacifica's Haitian
community. Lore gives a leader, a second-in-command, a netrunner core, a street
enforcement wing, and a separate Dogtown cell — not a formal rank ladder.

| Name | 2077 role | Character record | Location / influence point | Presence class | Source | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| **Maman Brigitte** (Brigitte, "Mama") | Leader of the Coastview Voodoo Boys; netrunner; the wiki database calls her the gang's *chéfine* | `Character.Voodoo_Queen` (holocall/world actor); `Character.q105_voodoo_queen` (braindance actor); `Character.Voodoo_Queen_dead` (dead-state variant) | Batty's Hotel, Pacifica Serenity Bible Church, Old Maglev Tunnel / Rezo Agwe | `story` | Raw `always_loaded_1` `SpawnSet_#voodoo_queen` and `SpawnSet_#maman_brigitte_holo`; raw `always_loaded_0` `{q105_com_voodoo_queen}`; wiki *Maman Brigitte* | `[game-data]` `[wiki]` |
| **Placide** | Second-in-command; enforcer, gatekeeper and deal-maker | `Character.Placide` (also `Character.Holocall_Placide`; `placideFakeDefault` is a fake, not a second Placide) | Batty's Hotel, Rolland's Butcher Shop, the netrunners' den, the chapel | `story` | Raw `always_loaded_1` `SpawnSet_#placide`; markers `q110_02_sm_placide_butcher`, `110_mp_placide_gate_hacking`; wiki *Placide* | `[game-data]` `[wiki]` |
| **Wilky "Slider" LaGuerre** | Leader of the Dogtown Voodoo Boys; netrunner; Brigitte's former right hand | No named 2077 record found | Slider's Hideout, Eventide Resort & Spa (Dogtown) | `story` | Wiki *Slider*; quest `q303_baron` (*The Damned*); Eventide computers | `[wiki]` |
| **Ayo Zarin** | Slider's right hand; Dogtown lieutenant (south wing) | `Character.we_ep1_05_mini_boss` (inferred; the only boss record in the `we_ep1_05` activity) | Luxor High Wellness Spa, south side (Dogtown) | `world-activity` | Site `we_ep1_05`; raw `Character.we_ep1_05_mini_boss`; wiki *Ayo Zarin* | `[game-data]` `[inferred]` `[wiki]` |
| **Milko Alexis** | Dogtown netrunner; blackmail boss (north wing) | `Character.sts_ep1_12_milko_alexis` | Luxor High Wellness Spa, north side (Dogtown) | `world-activity` | Raw `always_loaded_0` `{sts_ep1_12_main_com}`; site 362 roster; wiki *Milko Alexis* | `[game-data]` `[wiki]` |
| **Ti Neptune** | Netrunner; Brigitte's close aide, derogatorily called her "lapdog" | `Character.q110_tineptune` | Old Maglev Tunnel / Rezo Agwe | `story` | Raw `always_loaded_1` `SpawnSet_#q110_tineptune`; wiki *Ti Neptune* | `[game-data]` `[wiki]` |
| **The elders** (five) | Senior/elder netrunners in the data fortress; collective, not a named individual | `Character.q110_vdb_elder_1` … `_5` (plus `_dead` variants) | Old Maglev Tunnel / the "elders' lair" (Rezo Agwe) | `story` | Raw `always_loaded_1` `SpawnSet_#q110_com_vdb_elders`; prefab `{loc_q110_elders_lair}`; political role inferred | `[game-data]` `[inferred]` |
| **Philippe "Agwe" Oreste** | Founder (2062); former ship captain; led the Haitian refugees and organized the netrunner cadre | No 2077 record found | Pacifica (historical) | `historical` | Wiki *Philippe Oreste*; 2077 sourcebook | `[wiki]` `[lore]` |

The wiki marks Brigitte, Placide, Slider, Ayo Zarin, Milko, Ti Neptune and most
2077 named characters "dependent": their survival depends on V's choices in
*I Walk the Line*, *Transmission*, *The Damned* and *Gig: Treating Symptoms*.
That is not a source defect — it is the canonical picture of a leadership whose
top can be removed by an outsider, a NetWatch operation or an AI.

### 1.2 Succession history: schism, not coup

| Period | Leader | How the change happened |
| --- | --- | --- |
| 2062–? | **Philippe "Agwe" Oreste** | Founder; ex-ship captain who saved 150 refugees and organized the netrunner cadre in Pacifica. Status by 2077 unknown; no 2077 record. `[wiki]` |
| ?–2077 | **Maman Brigitte** | Leader in Coastview; netrunner; drives the Blackwall project. Dependent: can die in *Transmission*. `[wiki]` |
| ?–2077 | **Wilky "Slider" LaGuerre** | Brigitte's former right hand; split with her over the Blackwall and moved to Dogtown with his people. Killed in *The Damned*. `[wiki]` |
| 2077 | **Placide** | Second-in-command under Brigitte; runs the butcher-shop gate, the netrunners' den and the street wing. Dependent. `[wiki]` |
| 2077 | **Ayo Zarin** | Slider's right hand in Dogtown; runs the Luxor south wing. Dependent. `[wiki]` |
| 2077 | **Ti Neptune** | Netrunner; frozen with Brigitte by NetWatch black ICE; dependent. `[wiki]` |

The pattern is **ideological schism plus external decapitation**, not Maelstrom's
violent coup chain. The Brigitte–Slider split is the defining succession event:
Brigitte wanted to pierce the Blackwall; Slider considered it too dangerous and
took his followers to Dogtown. The base game can then remove Brigitte's cell
through NetWatch or Alt Cunningham, while the Dogtown cell survives as a rump
under Slider, Ayo Zarin and Milko. A simulation should model the two cells as
one faction with two power bases, not as a single decapitation target.

### 1.3 Rank structure, initiation and advancement

Lore does not name formal ranks beyond leader, second-in-command and netrunner.
What it does describe is a caste structure and a netrunner entry test:

1. **Leader / chéf(e).** Single leader per cell. Brigitte in Coastview; Slider in
   Dogtown. The wiki database calls Brigitte the gang's *chéfine*. `[wiki]`
2. **Second-in-command.** Placide under Brigitte; Ayo Zarin under Slider. They
   handle gatekeeping, deals and discipline. `[wiki]`
3. **Netrunner core.** Most Voodoo Boys are netrunners. Elite netrunners include
   the *Manbo* (a Vodou priestess archetype, Tier 3 elite netrunner enemy), the
   elders and Brigitte's personal team. `[wiki]` `[game-data]`
4. **Enforcers and "shadows".** The gang enforces sovereignty with machetes and
   "has an aversion to firearms, preferring instead needles wielded by 'shadows,'
   skilled assassins with hologram skulls on their faces." `[wiki]`
5. **Community affiliates.** Grann Ertha (vendor and Voodoo Boys affiliate), the
   butcher-shop vendor, the chapel sermon leader and the congregation are not
   members but are part of the political base. `[wiki]` `[game-data]`
6. **Initiation.** The gang's real name is unknown and "only told to initiated
   members." `[wiki]` Recruitment is a netrunner test: Jean-ki-ri tells Shiva to
   hack an embassy server to "prove your worth to become a Voodoo Boy." `[wiki]`
7. **Advancement.** Netrunning skill, loyalty to the cell and service to the
   Haitian community. There is no evidence of a formal probationary rank or a
   promotion ceremony beyond the initiation test.

**Practical consequence for the mod:** "netrunner" is both the entry gate and
the promotion currency. A simulation can model advancement as a threshold on
`technology`/netrunning investment plus loyalty to the current cell, with
NetWatch attention as the failure state — the mirror image of Maelstrom's chrome
threshold and cyberpsychosis.

### 1.4 Named members mapped to game data

Most named Voodoo Boys are **not in `data/sites/rosters.json`**. The exceptions
are Milko Alexis and Alan Noël, who are roster entries at site 362 (`sts_ep1_12`,
33 units). Brigitte, Placide, Ti Neptune and the elders live in the raw sector
community templates. Rows marked `[inferred]` are one-record deductions; verify
in-game before treating them as canonical.

| Name | Role / note | Character record | Community / site | Location | Presence class | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| Maman Brigitte | Leader; netrunner | `Character.Voodoo_Queen`; `Character.q105_voodoo_queen` (BD actor) | `SpawnSet_#voodoo_queen`; `{q105_com_voodoo_queen}`; `SpawnSet_#maman_brigitte_holo` | Batty's Hotel; chapel; maglev | `story` | `[game-data]` `[wiki]` |
| Placide | Second-in-command | `Character.Placide` | `SpawnSet_#placide` | Butcher shop; Batty's Hotel; netrunners' den | `story` | `[game-data]` `[wiki]` |
| Wilky "Slider" LaGuerre | Dogtown leader | none found | `q303_com_voodoo_boys_*` (generic guards) | Eventide / Slider's Hideout | `story` | `[wiki]` |
| Ayo Zarin | Dogtown lieutenant | `Character.we_ep1_05_mini_boss` (inferred) | `{we_ep1_05_com}` | Luxor south wing | `world-activity` | `[game-data]` `[inferred]` `[wiki]` |
| Milko Alexis | Dogtown netrunner/blackmailer | `Character.sts_ep1_12_milko_alexis` | `{sts_ep1_12_main_com}` | Luxor north wing | `world-activity` | `[game-data]` `[wiki]` |
| Ti Neptune | Netrunner | `Character.q110_tineptune` | `SpawnSet_#q110_tineptune` | Maglev / Rezo Agwe | `story` | `[game-data]` `[wiki]` |
| The elders (5) | Senior netrunners | `Character.q110_vdb_elder_1..5` | `SpawnSet_#q110_com_vdb_elders` | Maglev / "elders' lair" | `story` | `[game-data]` `[inferred]` |
| Jean-ki-ri | Brigitte's netrunner team; recruiter | no distinct 2077 record found | — | shard `ma_wat_lch_10` (Little China) | `historical` | `[wiki]` |
| Leon | Brigitte's netrunner team | no distinct 2077 record found | — | — | `historical` | `[wiki]` |
| Philippe "Agwe" Oreste | Founder | no 2077 record | — | — | `historical` | `[wiki]` `[lore]` |
| Grann Ertha (Ertha Djasma) | Vendor; Voodoo Boys affiliate; calls Placide "my child" | `Character.q110_grann_ertha` | `SpawnSet_#q110_grann_ertha` | Pacifica (vendor) | `story` | `[game-data]` `[wiki]` |
| John Milard | Butcher-shop front vendor | `Character.q110_butcher_shop_vendor` (inferred) | — | Rolland's Butcher Shop | `story` | `[game-data]` `[inferred]` `[wiki]` |
| Chapel contact (Alexandre Batisma) | Contact at the altar | `Character.q110_contact` (inferred) | marker `q110_01_sm_chapel_contact` | Pacifica Serenity Bible Church | `story` | `[game-data]` `[inferred]` `[wiki]` |
| Sermon leader | Preacher at the chapel sermon | `Character.q110_sermon_leader` | `SpawnSet_#q110_com_sermon_contact` | Chapel | `story` | `[game-data]` |
| Fara Dupont | Member; killed by Scavengers | no distinct 2077 record found | — | West Wind Estate (body) | `historical` | `[wiki]` |
| Diesuel, Josue, Lovelie | Members; killed by Scavengers | no distinct 2077 records found | — | — | `historical` | `[wiki]` |
| Alan Noël | NetWatch mole inside Milko's cell | `Character.sts_ep1_12_alan_noel` | `{sts_ep1_12_main_com}` | Luxor north wing | `world-activity` | `[game-data]` `[wiki]` |

Data cautions:

- **Brigitte has three records, one person.** `Character.Voodoo_Queen` is the
  holocall/world actor; `Character.q105_voodoo_queen` is a braindance actor in
  Evelyn Parker's memory; `Character.Voodoo_Queen_dead` is a dead-state variant.
  None of the three is a separate leader.
- **`placideFakeDefault` is not Placide.** It is a scripted fake in the quest
  chain; `Character.Placide` is the real record. `Character.q110_placide_girlfriend`
  is a separate NPC, not Placide.
- **Slider has no record.** The Dogtown leader is represented by generic
  `q303_voodoo_boy_guard_*` entries and the wiki. Do not invent a record.
- **Ayo Zarin's record is inferred.** `Character.we_ep1_05_mini_boss` is the only
  boss record in the `we_ep1_05` activity and the wiki names her as the target.
  Verify in-game before seeding.
- **The elders are a collective.** No wiki page names them or describes a formal
  council; their political role comes from the community name
  (`q110_com_vdb_elders`) and the prefab (`{loc_q110_elders_lair}`), not from
  dialogue.

### 1.5 What the game actually spawns (open world vs story-only)

This is the part other agents must not assume. A wiki infobox does not mean an
actor in free roam.

**`ambient` — persists in free roam.**
- Generic Voodoo Boys street gangers in Coastview. Base-game notes say that if
  *Transmission* ends with violence against the gang, "their generic members who
  are normally found on the street will disappear and will no longer spawn
  outside of Dogtown." `[wiki]` With the campaign disabled, these ambient
  spawns persist. No named leader is among them.

**`world-activity` — gig, scanner hustle or NCPD activity; free-roam content but
activity-gated.**
- **Ayo Zarin** at the Luxor High Wellness Spa south side (*Increased Criminal
  Activity: Voodoo Boys*, `baseid=we_ep1_05`). `[wiki]` `[game-data]`
- **Milko Alexis** at the Luxor High Wellness Spa north side (*Gig: Treating
  Symptoms*, `baseid=sts_ep1_12`). `[wiki]` `[game-data]`
- **Alan Noël** at the same gig, but he is NetWatch, not a Voodoo Boy. `[wiki]`
  `[game-data]`

**`story` — gated by the base-game *M'ap Tann Pèlen* / *I Walk the Line* /
*Transmission* chain or the Phantom Liberty main job *The Damned*; do not expect
them in free roam with the campaign disabled.**
- Maman Brigitte, Placide, Ti Neptune, the five elders, Slider, Jean-ki-ri,
  Leon, Grann Ertha and the chapel/butcher-shop NPCs. Their communities are
  quest-phase states (`q110_*`, `q105_*`, `q303_*`, `sts_ep1_12_main_com`), and
  their markers are quest markers. `[game-data]`

**`historical` — not in 2077 at all.**
- Philippe "Agwe" Oreste, Diesuel, Fara Dupont, Josue, Lovelie, and the 2020
  Voodoo Boys. `[wiki]` `[lore]`

**Bottom line for the campaign-disabled world:** **no top-tier Voodoo Boys leader
is ambient.** The highest-ranking named Voodoo Boy that can exist with the
campaign disabled is **Ayo Zarin**, and only as an activity target; **Milko
Alexis** is the other named free-roam Voodoo Boy, also activity-gated. If the mod
disables gigs and activities along with the campaign, the faction has **no named
open-world leader at all** — only generic street gangers.

### 1.6 Player-path hooks

| Person | Join under | Climb past | Ally with | Remove |
| --- | --- | --- | --- | --- |
| **Maman Brigitte** | The Blackwall project, Net supremacy, the AI alliance | Placide is the gatekeeper; the elders legitimize; the netrunner core decides | Ti Neptune, the netrunner core, the chapel congregation | Killing her decapitates the Coastview cell; Alt or NetWatch may do it for the player |
| **Placide** | Turf protection, anti-outsider enforcement, the butcher-shop gate | He is second-in-command; climb past by proving netrunning skill or by going through Brigitte | The enforcers and "shadows"; Grann Ertha | Removing him decapitates the street wing and opens the butcher-shop route |
| **Slider** | Dogtown pragmatism, corporate heists, cyberspace assassination | Ayo Zarin is his right hand; Milko runs the blackmail racket | Ayo Zarin, Milko, Barghest (transactional) | He is already blind and doomed in *The Damned*; removing him leaves Ayo Zarin and Milko |
| **Ayo Zarin** | The Dogtown cell, the Luxor south wing | She is Slider's right hand; climb past her to reach Slider | Milko, Barghest | She is the top open-world leader; removing her collapses the south wing |
| **Milko Alexis** | The implant-blackmail racket | He is the local netrunner boss; climb past him to reach the wider network | Ayo Zarin; Alan Noël (unknowingly) | Mr. Hands' gig *Treating Symptoms* removes him and decapitates the blackmail operation |
| **The elders** | Ritual and senior-netrunner authority | They are a collective, not a ladder; the leader and the netrunner core outrank them politically | Brigitte, the netrunner core | Removing them cuts the data fortress's legitimacy, not its hardware |

The design consequence: the Voodoo Boys have **two legitimate ladders**, not
one. A player can rise through Brigitte's Coastview netrunner cell or through
Slider's Dogtown heist/blackmail cell, and each choice changes which locations,
crews and external relationships are friendly. Unlike Maelstrom, the split is
ideological rather than a personal coup, so both ladders can coexist.

---

## 2. Internal political factions

### 2.1 The blocs

"Members" counts below are **presence proxies** from `dist/extract/areas.jsonl`,
not membership rolls. The `q110`, `sts_ep1_12`, `we_ep1_05` and `q303`
communities are overlapping quest phases of one site or one cell, so do not sum
them.

| Bloc | Leader(s) | What it wants | Presence / members hint | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- |
| **Brigitte's Coastview inner circle (Blackwall idealists)** | Maman Brigitte; Placide as second | Pierce the Blackwall, contact Alt Cunningham and the rogue AIs, secure safe passage, keep the Relic project alive | `q110_com_netrunners_den_vdb_bg` 6; `q110_com_voodoo_boys_chapel` 5; `q110_lairs_escape_voodoo_boys` 7 + reinforcement 6; Ti Neptune, Jean-ki-ri, Leon, the elders | Wiki *Maman Brigitte*, *Transmission*, *I Walk the Line*; raw q110 communities | `[game-data]` `[wiki]` |
| **Placide's enforcers and "shadows"** | Placide | Protect Pacifica turf, keep outsiders out, enforce sovereignty with machetes and needle assassinations, handle the dirty work | `q110_voodoo_boy_soldier`, `_netrunner`, `_lookout`, `q110_esc_*`; the "shadows" have no dedicated records | Wiki *Placide*, *Voodoo Boys* (aversion to firearms, "shadows"); raw q110 soldier records | `[game-data]` `[wiki]` |
| **The elders / data-fortress keepers** | No single leader (collective) | Guard Rezo Agwe and the ice-bath netrunner ritual; provide religious and senior-netrunner authority | `Character.q110_vdb_elder_1..5` (live) and `_dead` variants; prefab `{loc_q110_elders_lair}`; phases `q110_01_vdb_elders_maglev`, `_alive`, `q110_02_vdb_elders_dead` | Raw `SpawnSet_#q110_com_vdb_elders`; raw `{loc_q110_elders_lair}`; no wiki description (role inferred) | `[game-data]` `[inferred]` |
| **Dogtown pragmatists (Slider's faction)** | Wilky "Slider" LaGuerre; Ayo Zarin as second; Milko Alexis as netrunner boss | Corporate heists and cyberspace assassinations, bootleg deck/hack production, blackmail, data protection for Hansen's guests; avoid the Blackwall grand project and NetWatch | `sts_ep1_12` 33 roster units; `we_ep1_05_com` 20 + `_2ndloop` 16 + `_reinf` 5; `q303_com_voodoo_boys_guards` 21 + `_reinforcements` 10 + `_rooftop_guards` 5 | Wiki *Voodoo Boys* (Dogtown database entry), *Slider*, *Ayo Zarin*, *Milko Alexis*, *The Damned*, *Gig: Treating Symptoms*; raw Dogtown communities | `[game-data]` `[wiki]` |
| **The Haitian community / congregation (non-member constituency)** | No single leader; Grann Ertha as a community elder/affiliate | Survival, autonomy, communal law, protection from NCPD and corporate eviction | Grann Ertha (`Character.q110_grann_ertha`), the butcher-shop vendor (`Character.q110_butcher_shop_vendor`), the sermon leader (`Character.q110_sermon_leader`), the Batty's Hotel market community | Wiki *Grann Ertha*, *Voodoo Boys*, *The Voodoo Boys: What We Know and What We Don't*; raw q110 communities | `[game-data]` `[wiki]` |
| **NetWatch mole (non-member power centre)** | Alan Noël | Dismantle the Dogtown implant-blackmail network from within and advance his NetWatch career | `Character.sts_ep1_12_alan_noel`; one undercover agent inside Milko's cell | Wiki *Alan Noël*, *Gig: Treating Symptoms*, *Voodoo Boys Operational Base Search Report* | `[game-data]` `[wiki]` |

### 2.2 The Brigitte–Slider schism

This is the faction's defining internal conflict, and it is cleanly documented:

- **Brigitte's line:** the Blackwall will eventually crumble; the Voodoo Boys
  should get close to the rogue AIs now so they are on the winning side when it
  happens. She probes the Blackwall, hires Evelyn Parker to steal the Relic, and
  ultimately uses V to contact Alt Cunningham. `[wiki]`
- **Slider's line:** the Blackwall project is too dangerous. He was Brigitte's
  right hand, but "ideological differences arose"; he preferred to stay away
  from NetWatch agents and focus on "corporate heists and assassinations via
  cyberspace." He fled Pacifica and took control of an illegal software
  operation in Dogtown. `[wiki]`
- **The Dogtown database entry** frames the split as "the boundary between
  idealists and pragmatists": Dogtown Voodoo Boys "take more risks and rarely
  look back, explore the dark corners of the net more often and end up earning
  more, too." They do business in the Stadium, lend their services, run shady
  biz and protect Hansen's guests' data. `[wiki]`
- **Slider's own business ethics** are visible in his computer messages: he
  refuses a corporate assassination if the target corporation is Arasaka or
  Militech, and he treats a NetWatch "remove my data" offer as an obvious trap.
  `[wiki]`

The split is therefore **policy, not personality**: Blackwall transcendence vs
lucrative, low-profile netcrime. That is a real, simulation-ready axis:
**ideological transcendence vs pragmatic netcrime**.

### 2.3 The netrunner core vs the street wing

The Voodoo Boys are usually described as a gang of netrunners, but the game
shows a division of labour:

- **Netrunner core.** Most members are netrunners. The elite include the
  *Manbo* (Vodou priestess archetype, Tier 3 elite netrunner), the elders, and
  Brigitte's personal team (Jean-ki-ri, Leon, Ti Neptune). Their work is data
  theft, intrusion, black ICE, and Blackwall probing. `[wiki]` `[game-data]`
- **Street wing.** Placide's enforcers, the "shadows" (hologram-skulled needle
  assassins), and the machete-armed turf enforcers. They handle sovereignty,
  intimidation, protection and the butcher-shop gate. The gang "has an aversion
  to firearms," which is a real tactical and cultural marker. `[wiki]`
- **The elders** sit between the two: senior netrunners with ritual authority,
  physically jacked into ice baths in the maglev lair. `[game-data]`
  `[inferred]`

This is not a hostile split. Placide is loyal to Brigitte, and the street wing
exists to protect the netrunner core. But it is a real **resource and status
divide**: the netrunner core gets the prestige and the Blackwall project; the
street wing gets the dangerous, low-status work. A simulation can make that
divide political when casualties rise or when the netrunner core's grand project
stops paying.

### 2.4 The Dogtown cell

The Phantom Liberty cell is a separate power base, not a branch office:

- **Slider** leads it from his hideout in the Eventide Resort & Spa. He is
  blind, chair-bound and jacked into a machine; he still runs heists and
  assassinations through cyberspace. `[wiki]`
- **Ayo Zarin** runs the Luxor High Wellness Spa south side; she is Slider's
  right hand and a heavily chromed tomahawk fighter. `[wiki]` `[game-data]`
- **Milko Alexis** runs the north side and the implant-blackmail racket: he
  threatens to fatally damage victims' implants and synthetic organs unless they
  pay or cooperate. He spends more time in the Net than in realspace. `[wiki]`
  `[game-data]`
- **The cell's economy** is more pragmatic and more exposed than Coastview's:
  corporate heists, cyberspace assassination, bootleg decks and hacks, data
  protection for Hansen's guests, and blackmail. `[wiki]`
- **The Barghest relationship** is symbiotic but shaky: the Voodoo Boys operate
  in Dogtown "in business with BARGHEST as frequently as they clash with them,"
  and Hansen keeps it "a little rumble here and there and not a full-blown
  earthquake." `[wiki]`
- **NetWatch has already penetrated the cell**: Alan Noël spent months
  undercover inside Milko's operation. `[wiki]` `[game-data]`

The cell can survive the destruction of Brigitte's Coastview circle. That is the
key political fact for the simulation: the faction has **two decapitation
points**, and killing one does not kill the other.

### 2.5 The community as a political base

The Voodoo Boys are not just a gang; they are the self-appointed government of
Pacifica's Haitian community:

- They "establish the common law and likewise enforce it, ensuring the relative
  well-being of their fellow residents." Their loyalty to "their own" is as
  strong as their contempt for "the city." `[wiki]`
- They are the district's de facto authority: "Neither the NCPD nor the
  corporations have any power in this area … the Voodoo Boys or one of the
  locals must give an okay" to enter. `[wiki]`
- The community is a constituency, not a faction: Grann Ertha is a vendor and
  affiliate who calls Placide "[her] child"; the butcher shop is a front; the
  chapel is the public face; Batty's Hotel's market floor is the communal
  economy. `[wiki]` `[game-data]`
- The gang's religion is "a deadly serious matter": Vodou-derived ritual, the
  chapel, the sermon, the elders, the *Manbo* priestess archetype, and the
  promise of the Net as eternal life. `[wiki]`

For the simulation, the community is a **legitimacy resource**: it gives the
gang intelligence, recruits, safe houses and political cover, but it also
creates obligations. A leader who exploits the community (Milko's blackmail,
Slider's heists) gains money and loses legitimacy; a leader who protects it
(Brigitte's public works, Placide's turf enforcement) gains loyalty and loses
flexibility.

### 2.6 Historical precedents

- **The 2020 Voodoo Boys are a different gang.** They were drug-dealing
  terrorists in the University District, with ritual-magic trappings and no
  connection to the 2077 netrunner collective beyond the name. The 2077 gang
  "do not call themselves by that name"; it was applied by outsiders. `[wiki]`
  Do not import 2020 characters. `Baron D` is the 2045 leader of the old gang,
  not the 2077 Voodoo Boys. `[wiki]`
- **The 2062 Haitian refugees** built Pacifica, were abandoned when the
  Unification War scared off investors, and stayed. The collective that emerged
  became the district's self-appointed leadership. `[wiki]`
- **Philippe "Agwe" Oreste** organized the netrunner cadre and led the refugees;
  his status by 2077 is unknown. He is the founding legitimacy figure, not a
  2077 actor. `[wiki]`
- **The Brigitte–Slider split** is the only attested 2077 succession event. It
  is ideological, not violent. `[wiki]`

### 2.7 What could drive internal conflict in a simulation

Evidence-based drivers, in rough order of plausibility:

1. **Succession after Brigitte or Placide is removed.** The Coastview cell has
   no obvious successor besides Placide; if both fall, the netrunner core and
   the elders must choose, and the Dogtown cell may claim the whole faction.
2. **Ideology vs pragmatism.** The Blackwall project vs Slider's heist economy.
   A player who brings in lucrative corporate work strengthens the Dogtown line;
   a player who pursues the Blackwall strengthens Brigitte's line.
3. **Coastview vs Dogtown resource split.** Dogtown earns more but depends on
   Hansen's tolerance; Coastview has legitimacy but less cash. A leader who
   taxes one cell to fund the other creates a grievance.
4. **NetWatch infiltration.** Alan Noël is the proof that the Dogtown cell can
   be penetrated. A player who exposes or recruits a mole can decapitate a cell
   without a fight.
5. **Treatment of the community.** Protection vs exploitation. Milko's
   blackmail and Slider's heists are lucrative but corrosive; Brigitte's
   communal authority depends on being seen to protect.
6. **Control of Rezo Agwe and the elders.** The data fortress is the faction's
   crown jewel. Whoever controls the elders and the ice baths controls the
   netrunner core's legitimacy.
7. **External pressure.** NetWatch, Barghest, the Animals and the Scavengers can
   unite the cells or expose a leader's failure. The historical pattern is that
   external violence decides the succession.

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

There is **no usable offline attitude matrix**. `refs/RED4ext.SDK/.../game/data/Affiliation.hpp`
is an identity enum (VoodooBoys = 34, NetWatch = 16, Barghest = 4), not a
relation table; `Attitude_Record.hpp` is opaque. The stances below are therefore
judged from quests, wiki and spatial adjacency, not from a TweakDB relation row.
That is why every row carries a tag and why the neutral rows are not claims of
friendship.

| Faction | Code | Stance | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| Tyger Claws | `tyger_claws` | `neutral` | No attested conflict. Voodoo Boys bootleg hacks are sold "under the counter in Kabuki" (Tyger Claws turf) and a Voodoo Boys recruitment shard sits in Little China (`ma_wat_lch_10`), but these are commercial adjacency, not a feud `[wiki]` `[game-data]` | `[game-data]` `[inferred]` |
| Valentinos | `valentinos` | `neutral` | No attested interaction; different district (Heywood) `[inferred]` | `[inferred]` |
| Arasaka | `arasaka` | `hostile` | Voodoo Boys hired Evelyn Parker to steal the Relic prototype from Yorinobu Arasaka `[wiki]`; corporate databank theft is their primary income `[wiki]`; Slider refuses jobs against Arasaka as too dangerous `[wiki]` | `[wiki]` |
| Militech | `militech` | `rival` | Militech combat robots found at the Luxor spa; the NetWatch search report flags possible corporate espionage or sabotage `[game-data]` `[wiki]`; corporate data theft targets Militech among others `[wiki]`; Slider refuses Militech jobs `[wiki]`. No direct firefight attested | `[game-data]` `[wiki]` |
| Kang Tao | `kang_tao` | `neutral` | No specific operation attested; only generic corporate data theft `[inferred]` | `[inferred]` |
| Biotechnica | `biotechnica` | `neutral` | No specific operation attested `[inferred]` | `[inferred]` |
| Petrochem | `petrochem` | `neutral` | No specific operation attested `[inferred]` | `[inferred]` |
| Barghest | `barghest` | `trade` | Dogtown Voodoo Boys protect Hansen's guests' data and cover their tracks; "in business with BARGHEST as frequently as they clash with them"; symbiotic but shaky, kept to "a little rumble here and there" `[wiki]` | `[wiki]` |
| 6th Street | `sixth_street` | `neutral` | No attested interaction `[inferred]` | `[inferred]` |
| Aldecaldos | `aldecaldos` | `neutral` | No attested interaction `[inferred]` | `[inferred]` |
| Wraiths | `wraiths` | `neutral` | No attested interaction `[inferred]` | `[inferred]` |
| Animals | `animals` | `hostile` | NetWatch hired the Animals to guard the Grand Imperial Mall; Voodoo Boys fight them in *I Walk the Line* `[wiki]` `[game-data]`; the wiki records a Voodoo Boys–Animals rivalry `[wiki]` | `[game-data]` `[wiki]` |
| The Mox | `the_mox` | `neutral` | No institutional link. The Voodoo Boys' betrayal of Evelyn Parker (a Clouds doll and Judy Alvarez's friend) is a personal grievance, not a Voodoo Boys–Mox relation `[wiki]` `[inferred]` | `[wiki]` `[inferred]` |
| Maelstrom | `maelstrom` | `neutral` | No attested interaction; different district and different obsession (chrome vs the Net) `[inferred]` | `[inferred]` |
| NCPD | `ncpd` | `hostile` | Voodoo Boys are the de facto law in Pacifica and hold it against NCPD/corporate eviction; NCPD has no power there `[wiki]`; Voodoo Boys records appear in NCPD crime-scene/patrol areas (`cs_police_execution_com`, `cs_highway_patrol_com`) `[game-data]` | `[game-data]` `[wiki]` |
| Night Corp | `night_corp` | `neutral` | No attested interaction; a corporation, not a Pacifica turf actor `[inferred]` | `[inferred]` |
| City Council | `city_council` | `neutral` | No attested interaction; the Voodoo Boys are outside city political authority `[inferred]` | `[inferred]` |
| Scavengers | `scavengers` | `hostile` | Placide orders Fara Dupont to surround and kill Scavengers who raided a NetWatch stash `[wiki]`; four Voodoo Boys members (Fara Dupont, Diesuel, Josue, Lovelie) were killed by Scavengers `[wiki]`; both operate in Pacifica/West Wind/Terra Cognita `[game-data]` | `[game-data]` `[wiki]` |
| Regina Jones | `fixer_regina` | `neutral` | No Voodoo Boys-specific gig or lore link found `[inferred]` | `[inferred]` |
| Wakako Okada | `fixer_wakako` | `neutral` | No Voodoo Boys-specific gig or lore link found `[inferred]` | `[inferred]` |
| Sebastian Ibarra (Padre) | `fixer_padre` | `neutral` | No Voodoo Boys-specific gig or lore link found `[inferred]` | `[inferred]` |
| Muamar Reyes (El Capitán) | `fixer_el_capitan` | `neutral` | No Voodoo Boys-specific gig or lore link found `[inferred]` | `[inferred]` |
| Dakota Smith | `fixer_dakota` | `neutral` | No Voodoo Boys-specific gig or lore link found `[inferred]` | `[inferred]` |
| Dino Dinovic | `fixer_dino` | `neutral` | No Voodoo Boys-specific gig or lore link found `[inferred]` | `[inferred]` |
| Rogue Amendiares | `fixer_rogue` | `neutral` | No Voodoo Boys-specific gig; Afterlife is neutral ground `[inferred]` | `[inferred]` |
| Mr. Hands | `fixer_mr_hands` | `trade` | Pacifica fixer who brokers V's access to the Voodoo Boys and volunteers V for Placide's Grand Imperial Mall job `[wiki]`; later hires V to neutralize Milko (*Gig: Treating Symptoms*) and moves against Ayo Zarin's cell in Phantom Liberty `[wiki]`; a transactional broker, not a loyal ally | `[wiki]` |
| Afterlife | `afterlife` | `neutral` | Neutral merc marketplace; no Voodoo Boys-specific link `[inferred]` | `[inferred]` |
| NetWatch | `netwatch` | `war` | NetWatch maintains the Blackwall and hunts rogue netrunners/AI contact `[wiki]`; Bryce Mosley maps and shuts down Rezo Agwe and freezes Brigitte and Ti `[wiki]`; Alan Noël infiltrates the Dogtown cell `[wiki]`; Placide's virus targets NetWatch agents `[wiki]`; NetWatch agents are present across the city (`cvi/kab/cpz_netwatch_agent_*`) `[game-data]` | `[game-data]` `[wiki]` |

**Counts:** `war` 1, `hostile` 4, `rival` 1, `trade` 2, `neutral` 20. No `ally`,
`patron` or `client` row among the coded factions. The Voodoo Boys' only
patron-like relationship is with the un-coded Haitian community (§3.3).

### 3.3 Actors outside `data/factions.json`

These are real relationships but have no faction code, so they are prose only.

- **The Haitian community / diaspora** — the Voodoo Boys' core constituency and
  the source of their legitimacy. They are the community's self-appointed
  government and protectors, not its hired muscle. A `patron` relationship in
  the vocabulary's sense, but there is no faction code and no membership roll.
  `[wiki]`
- **The "shadows"** — the gang's needle-armed, hologram-skulled assassins. An
  internal specialist cadre, not a faction. `[wiki]`
- **Evelyn Parker** — a Clouds doll hired by the Voodoo Boys to locate the
  Relic, then remotely hacked by Brigitte to keep her quiet. A one-off
  **client/asset**, then a victim; not a faction. `[wiki]`
- **Bryce Mosley** — the NetWatch agent who maps Rezo Agwe. An individual; the
  NetWatch row covers the institution. `[wiki]`
- **Alan Noël** — the NetWatch mole inside Milko's cell. An individual power
  centre; the NetWatch row covers the institution. `[wiki]`
- **Kyle Araujo** — the independent implant supplier who "has a deal with the
  Voodoo Boys and supplies them with implants used for research purposes." A
  supplier/client, not a faction. `[wiki]`
- **Philippe "Agwe" Oreste** — the founder. Historical legitimacy figure, not a
  2077 faction. `[wiki]`
- **The 2020 Voodoo Boys / Baron D** — a different gang with the same name. Do
  not import them into the 2077 matrix. `[wiki]`

### 3.4 Guarantor assessment

This is the design question: if a player founds a gang, which factions would
guarantee the Voodoo Boys' support, and which would the Voodoo Boys guarantee?

- **No full-faction ally.** The matrix has no `ally`, `patron` or `client` row
  for a coded faction. The only `trade` rows are Barghest (a territorial host
  whose tolerance is conditional) and Mr. Hands (a broker with his own agenda).
- **The Voodoo Boys are a poor guarantor.** A player who takes over the faction
  inherits a war with NetWatch, a rivalry with the Animals, a hostile
  relationship with the Scavengers, and a Dogtown cell that exists at Hansen's
  pleasure. Their political capital is the Net, the community's legitimacy and
  the data fortress — all intangible and all vulnerable to a single NetWatch
  operation.
- **Plausible guarantors for a player-founded gang** are therefore transactional:
  Barghest (Dogtown only, and only while the player is useful), Mr. Hands (a
  broker who can open doors), a corrupt or compromised NetWatch agent (Alan
  Noël-type), or the Haitian community (legitimacy and intelligence, not
  muscle). None is an ideological ally.
- **The Voodoo Boys as an aggressor.** They are more likely to be the **target**
  of NetWatch, Barghest or the Animals than a guarantor. They do not fight open
  turf wars; they fight through the Net, blackmail and proxy operations. A
  player who founds a gang on a Voodoo Boys-held point should expect a
  cyber-espionage response, not a street war.

---

## 4. Pillar notes

Design claims from `docs/design/gameplay-systems.md`: the Voodoo Boys are an
**Ideological Collective** (archetype strength Culture, weakness Economy);
faction strength **Espionage**, weakness **Politics**.

| Pillar | Design claim | Lore verdict | Evidence |
| --- | --- | --- | --- |
| Espionage (strength) | The Voodoo Boys are the city's premier netrunner gang | **Strongly supported.** Their primary income is corporate databank and account hacking; they hire out as mercenary netrunners; they run black ICE, implant blackmail and a data fortress; they probe the Blackwall. NetWatch exists partly to stop them. | Wiki *Voodoo Boys* sources of income; *NetWatch*; *Placide*; *Milko Alexis*; *Transmission*; `cvi/kab/cpz_netwatch_agent_*` `[wiki]` `[game-data]` |
| Politics (weakness) | The Voodoo Boys cannot do politics | **Supported, with an important qualification.** They have no city politics, no allies and a NetWatch war, and their leadership is split between Coastview and Dogtown. But they *do* have internal governance: they establish and enforce common law in Pacifica and act as the community's government. The weakness is **external** politics, not the absence of politics. | Wiki *The Voodoo Boys: What We Know and What We Don't*; *Voodoo Boys* database entry; *Barghest* (symbiosis); *Mr. Hands* `[wiki]` |
| Culture (archetype strength) | An Ideological Collective binds through culture | **Strongly supported and outward-facing within the community.** Vodou-derived ritual, the chapel, the sermon, the elders, the *Manbo* priestess archetype, the secret name, the initiation test, and the Net-as-afterlife belief bind the Haitian diaspora and legitimize the gang's rule. It repels outsiders and sustains the community. | Wiki *Voodoo Boys* (philosophy/structure), *Net Shamans*, *The Voodoo Boys: What We Know*; `Character.q110_sermon_leader`, `Character.q110_vdb_elder_*` `[wiki]` `[game-data]` |
| Economy (archetype weakness) | The Voodoo Boys are economically weak | **Complicates the design.** Their income is high-value but illegal and intangible: corporate data theft, mercenary netrunning, implant blackmail, bootleg hardware, and Dogtown data protection. They have no legitimate front, no finance/real-estate, and no territorial business base. Model them as **high-value illegal income, low legitimacy and low resilience**, not "low output." | Wiki *Voodoo Boys* sources of income; *Milko Alexis*; *Eventide Resort & Spa/Computers*; location doc `../voodoo-boys.md` §4 `[wiki]` `[game-data]` |
| Overall fit | The pillars fit the faction's identity | **Good for identity, imperfect for balance sheet.** Keep Espionage strong and Politics weak. Treat Culture as high internal cohesion and communal legitimacy, and Economy as "illegal-only, intangible and fragile." | Synthesis of the rows above `[inferred]` |

Design cautions, not redesigns:

- Do **not** model the Voodoo Boys as poor. Model them as a faction whose income
  is illegal, intangible and geographically split between Coastview and Dogtown.
- Do **not** model Politics as zero. The faction has a real internal government
  (common law, elders, community authority); what it lacks is city-level
  political leverage and allies.
- The Net is the battlefield. A Voodoo Boys war should be fought through
  espionage, blackmail and data denial, not street turf.
- The Brigitte–Slider split is a **policy** split, not a personal feud. A
  simulation should let the player choose a side and change the faction's
  external posture.

---

## 5. Gaps and uncertainties

1. **No offline attitude matrix.** `refs/RED4ext.SDK/.../game/data/Attitude_Record.hpp`
   is opaque, and `Affiliation.hpp` only gives identity (VoodooBoys = 34,
   NetWatch = 16, Barghest = 4). Every stance in §3.2 is judged from quests,
   wiki and spatial adjacency; none is read from a TweakDB relation table. A
   TweakDB dump would settle the neutral rows.
2. **Named leaders are mostly not in `data/sites/rosters.json`.** Milko Alexis
   and Alan Noël are roster entries at site 362; Brigitte, Placide, Ti Neptune
   and the elders exist only in the raw sector community registry. This is the
   same "rosters miss quest communities" problem as the location METHOD, but
   worse for named characters.
3. **Multiple records per named NPC.** Brigitte has `Character.Voodoo_Queen`
   (holocall/world), `Character.q105_voodoo_queen` (braindance actor) and
   `Character.Voodoo_Queen_dead` (dead-state variant). Placide has
   `Character.Placide`, `Character.Holocall_Placide` and `placideFakeDefault`
   (a fake). A naive name search produces false leaders. This is a **METHOD
   gap**: the politics METHOD does not warn about `_dead`, `*_holo`/`Holocall_*`,
   `*Fake*`, or BD-actor records.
4. **The elders' political role is inferred.** The community name
   `q110_com_vdb_elders` and the prefab `{loc_q110_elders_lair}` prove five VDB
   elders exist in the maglev lair, but no wiki page names them or describes a
   formal council. Treat their authority as `[inferred]`.
5. **Slider has no character record.** The Dogtown leader is represented by
   generic `q303_voodoo_boy_guard_*` entries and the wiki. His position in the
   JSON rests on `[wiki]` only.
6. **Ayo Zarin's record is inferred.** `Character.we_ep1_05_mini_boss` is the
   only boss record in the `we_ep1_05` activity and the wiki names her as the
   target. Verify in-game before seeding.
7. **The Dogtown cell's communities overlap.** `sts_ep1_12_*` (six communities),
   `we_ep1_05_*` (three) and `q303_com_voodoo_boys_*` (three) are overlapping
   quest phases of one cell or one site. Do not sum them. The counts in §2.1 are
   presence proxies, not rolls.
8. **The "shadows" have no dedicated records.** The needle-armed, hologram-skulled
   assassins are wiki-only. Do not invent a site or a character record.
9. **The Voodoo Boys' coded relations are sparse.** Most rows are
   `neutral`/`[inferred]`. The biggest gap is the absence of a stance for
   **patron/protector of a non-faction community**: the Haitian community is
   central to the faction but has no `factions.json` code. This is a **METHOD
   gap**, not a data gap.
10. **NetWatch is not in the politics METHOD's required-rows list.** It is the
    defining adversary for the Voodoo Boys (and arguably for Maelstrom), and it
    has a `factions.json` code (`netwatch`, fid 25). The list should include it
    for any Net-adjacent faction. I added the row.
11. **`open_world` is activity-gated for the only named free-roam leaders.**
    Ayo Zarin and Milko Alexis exist only as an Increased Criminal Activity
    target and a gig target. If the mod disables gigs/activities, the faction
    has no named open-world leader at all. This is a **faction-level** finding
    that the per-NPC `open_world` flag does not express.
12. **Phantom Liberty changes the political map.** The Dogtown Voodoo Boys are
    tenants of Barghest, not sovereigns; the base-game claim that the Voodoo
    Boys rule Pacifica does not extend to Dogtown. The politics METHOD's
    single-faction template does not force this split; this document does.
13. **The location doc's Eventide coordinate is inferred.** The Dogtown HQ anchor
    is weaker than the Luxor (`sts_ep1_12`, proven by quest id). This affects
    where a player can meet Slider, not who he is. See `../voodoo-boys.md` §8.
14. **The wiki marks most leaders "dependent."** Brigitte, Placide, Slider, Ayo
    Zarin, Milko and Ti Neptune can all be removed or killed by V. A simulation
    must choose a branch or model the branches explicitly.
15. **The 2020 Voodoo Boys are a different gang.** They are drug-dealing
    terrorists with ritual trappings, not the 2077 netrunner collective. Baron D
    is their 2045 leader. Do not import them into the 2077 matrix.
16. **`data/factions.json` has no `hostility_bias` relation.** Voodoo Boys'
    `hostility_bias` is 0.7 and `income_multiplier` is 1.1, but these are seed
    tuning values, not pairwise stances. Do not read them as relations.
17. **The community's internal politics are not modeled.** Grann Ertha, the
    butcher-shop vendor, the sermon leader and the congregation are presence
    proxies, not a roll. A simulation that wants community legitimacy needs a
    separate constituency model.
18. **The `q110_contact` and `q110_butcher_shop_vendor` name mappings are
    inferred.** The wiki's quest objectives name "Alexandre Batisma" and "John
    Milard" but those pages are red links/missing; the records are the best
    available match. Flagged `[inferred]`.

### 5.1 Sources consulted

- Local: `data/factions.json`, `data/sites/{sites,rosters,guards,triggers,spots,patrols,doors,communities}.json`,
  `data/faction_headquarters.json`, `data/sub_territories.json`,
  `data/control_centers.json`, `data/landmarks.json`,
  `dist/extract/areas.jsonl`, `dist/extract/markers.jsonl`,
  `dist/extract/raw/**/always_loaded_{0,1,2}.streamingsector.json` (community
  registry templates, `characterRecordId` values and prefab node names),
  `refs/RED4ext.SDK/.../game/data/Affiliation.hpp`,
  `refs/RED4ext.SDK/.../game/data/Attitude_Record.hpp`.
- Wiki: [Voodoo Boys](https://cyberpunk.fandom.com/wiki/Voodoo_Boys),
  [Voodoo Boys Members](https://cyberpunk.fandom.com/wiki/Voodoo_Boys_Members),
  [Maman Brigitte](https://cyberpunk.fandom.com/wiki/Maman_Brigitte),
  [Placide](https://cyberpunk.fandom.com/wiki/Placide),
  [Slider](https://cyberpunk.fandom.com/wiki/Slider),
  [Ayo Zarin](https://cyberpunk.fandom.com/wiki/Ayo_Zarin),
  [Milko Alexis](https://cyberpunk.fandom.com/wiki/Milko_Alexis),
  [Ti Neptune](https://cyberpunk.fandom.com/wiki/Ti_Neptune),
  [Philippe Oreste](https://cyberpunk.fandom.com/wiki/Philippe_Oreste),
  [Grann Ertha](https://cyberpunk.fandom.com/wiki/Ertha_Ojasma),
  [Alan Noël](https://cyberpunk.fandom.com/wiki/Alan_No%C3%ABl),
  [Bryce Mosley](https://cyberpunk.fandom.com/wiki/Bryce_Mosley),
  [NetWatch](https://cyberpunk.fandom.com/wiki/NetWatch),
  [Animals](https://cyberpunk.fandom.com/wiki/Animals),
  [Barghest](https://cyberpunk.fandom.com/wiki/Barghest),
  [Mr. Hands](https://cyberpunk.fandom.com/wiki/Mr._Hands),
  [M'ap Tann Pèlen](https://cyberpunk.fandom.com/wiki/M%27ap_Tann_P%C3%A8len),
  [I Walk the Line](https://cyberpunk.fandom.com/wiki/I_Walk_the_Line),
  [Transmission](https://cyberpunk.fandom.com/wiki/Transmission),
  [The Damned](https://cyberpunk.fandom.com/wiki/The_Damned),
  [Gig: Treating Symptoms](https://cyberpunk.fandom.com/wiki/Gig:_Treating_Symptoms),
  [Increased Criminal Activity: Voodoo Boys](https://cyberpunk.fandom.com/wiki/Increased_Criminal_Activity:_Voodoo_Boys),
  [Net Shamans](https://cyberpunk.fandom.com/wiki/Net_Shamans),
  [Voodoo Boys Manbo](https://cyberpunk.fandom.com/wiki/Voodoo_Boys_Manbo),
  [The Voodoo Boys: What We Know and What We Don't](https://cyberpunk.fandom.com/wiki/The_Voodoo_Boys:_What_We_Know_and_What_We_Don%27t),
  [Archived Conversation: Fara Dupont and Placide](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Fara_Dupont_and_Placide),
  [Archived Conversation: Jean-ki-ri and Shiva](https://cyberpunk.fandom.com/wiki/Archived_Conversation:_Jean-ki-ri_and_Shiva),
  [Voodoo Boys Operational Base Search Report](https://cyberpunk.fandom.com/wiki/Voodoo_Boys_Operational_Base_Search_Report),
  [Eventide Resort & Spa/Computers](https://cyberpunk.fandom.com/wiki/Eventide_Resort_%26_Spa/Computers),
  [Batty's Hotel](https://cyberpunk.fandom.com/wiki/Batty%27s_Hotel),
  [Eventide Resort & Spa](https://cyberpunk.fandom.com/wiki/Eventide_Resort_%26_Spa),
  [Pacifica Serenity Bible Church](https://cyberpunk.fandom.com/wiki/Pacifica_Serenity_Bible_Church),
  [Old Maglev Tunnel](https://cyberpunk.fandom.com/wiki/Old_Maglev_Tunnel),
  [Voodoo Boys (2020)](https://cyberpunk.fandom.com/wiki/Voodoo_Boys_(2020)).
- Earlier repo research: `docs/research/factions/voodoo-boys.md`,
  `docs/research/factions/METHOD.md`, `docs/research/factions/politics/METHOD.md`,
  `docs/research/factions/politics/maelstrom.md`,
  `docs/design/gameplay-systems.md`.

---

## 6. Machine-readable block

```json
{
  "faction_code": "voodoo_boys",
  "leaders": [
    {
      "name": "Maman Brigitte (Brigitte)",
      "role": "Leader of the Coastview Voodoo Boys; netrunner; chefine",
      "character_record_id": "Character.Voodoo_Queen",
      "location_name": "Batty's Hotel / Pacifica Serenity Bible Church / Old Maglev Tunnel (Rezo Agwe)",
      "open_world": false,
      "source": "raw always_loaded_1 SpawnSet_#voodoo_queen (Character.Voodoo_Queen), SpawnSet_#maman_brigitte_holo (Character.Voodoo_Queen); raw always_loaded_0 {q105_com_voodoo_queen} (Character.q105_voodoo_queen, BD actor); wiki Maman Brigitte",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Placide",
      "role": "Second-in-command; enforcer and gatekeeper",
      "character_record_id": "Character.Placide",
      "location_name": "Batty's Hotel / Rolland's Butcher Shop / netrunners' den / chapel",
      "open_world": false,
      "source": "raw always_loaded_1 SpawnSet_#placide (Character.Placide; Character.Holocall_Placide; placideFakeDefault is a fake); markers q110_02_sm_placide_butcher and 110_mp_placide_gate_hacking; wiki Placide",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Wilky \"Slider\" LaGuerre",
      "role": "Leader of the Dogtown Voodoo Boys; netrunner; Brigitte's former right hand",
      "character_record_id": null,
      "location_name": "Slider's Hideout, Eventide Resort & Spa (Dogtown)",
      "open_world": false,
      "source": "wiki Slider; quest q303_baron (The Damned); Eventide Resort & Spa/Computers; no named character record found in raw always_loaded_*",
      "confidence": "wiki"
    },
    {
      "name": "Ayo Zarin",
      "role": "Slider's right hand; Dogtown lieutenant (south wing)",
      "character_record_id": "Character.we_ep1_05_mini_boss",
      "location_name": "Luxor High Wellness Spa (south side), Dogtown",
      "open_world": true,
      "source": "site we_ep1_05 (Increased Criminal Activity: Voodoo Boys) boss entry; raw always_loaded_1 Character.we_ep1_05_mini_boss; wiki Ayo Zarin; record mapping inferred",
      "confidence": "game-data+inferred+wiki"
    },
    {
      "name": "Milko Alexis",
      "role": "Dogtown netrunner; blackmail boss (north wing)",
      "character_record_id": "Character.sts_ep1_12_milko_alexis",
      "location_name": "Luxor High Wellness Spa (north side), Dogtown",
      "open_world": true,
      "source": "raw always_loaded_0 {sts_ep1_12_main_com} entry milko_alexis (Character.sts_ep1_12_milko_alexis); site 362 roster; wiki Milko Alexis",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Ti Neptune",
      "role": "Netrunner; Brigitte's close aide",
      "character_record_id": "Character.q110_tineptune",
      "location_name": "Old Maglev Tunnel (Rezo Agwe), Coastview",
      "open_world": false,
      "source": "raw always_loaded_1 SpawnSet_#q110_tineptune (Character.q110_tineptune); wiki Ti Neptune",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The elders (five Voodoo Boys elders)",
      "role": "Senior/elder netrunners in the data fortress; collective",
      "character_record_id": null,
      "location_name": "Old Maglev Tunnel / elders' lair (Rezo Agwe), Coastview",
      "open_world": false,
      "source": "raw always_loaded_1 SpawnSet_#q110_com_vdb_elders (Character.q110_vdb_elder_1..5 and _dead variants); prefab {loc_q110_elders_lair}; political role inferred",
      "confidence": "game-data+inferred"
    }
  ],
  "internal_factions": [
    {
      "name": "Brigitte's Coastview inner circle (Blackwall idealists)",
      "leader": "Maman Brigitte",
      "goals": "Pierce the Blackwall, contact Alt Cunningham and the rogue AIs, secure safe passage for the gang, and keep the Relic project alive",
      "members_hint": "Placide, Ti Neptune, Jean-ki-ri, Leon, the five elders, the chapel congregation; q110_com_netrunners_den_vdb_bg 6, q110_com_voodoo_boys_chapel 5, q110_lairs_escape_voodoo_boys 7 + reinforcement 6 (overlapping quest phases)",
      "source": "wiki Voodoo Boys, Maman Brigitte, Placide, Ti Neptune, Transmission, I Walk the Line; raw q110 communities",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Placide's enforcers and shadows",
      "leader": "Placide",
      "goals": "Protect Pacifica turf, keep outsiders out, enforce sovereignty with machetes and needle assassinations, and handle the dirty work Brigitte will not",
      "members_hint": "q110_voodoo_boy_soldier, q110_voodoo_boy_netrunner, q110_voodoo_boy_lookout, q110_esc_* records; the shadows (hologram-skulled needle assassins) have no dedicated records",
      "source": "wiki Voodoo Boys (aversion to firearms, shadows), Placide; raw q110 soldier/esc records",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The elders / data-fortress keepers",
      "leader": null,
      "goals": "Guard Rezo Agwe and the ice-bath netrunner ritual; provide religious and senior-netrunner authority",
      "members_hint": "Character.q110_vdb_elder_1..5 (live) and _dead variants; prefab {loc_q110_elders_lair}; phases q110_01_vdb_elders_maglev, _alive, q110_02_vdb_elders_dead",
      "source": "raw always_loaded_1 SpawnSet_#q110_com_vdb_elders; raw prefab {loc_q110_elders_lair}; no wiki page describes a formal council (role inferred)",
      "confidence": "game-data+inferred"
    },
    {
      "name": "Dogtown pragmatists (Slider's faction)",
      "leader": "Wilky \"Slider\" LaGuerre",
      "goals": "Corporate heists and cyberspace assassinations, bootleg deck/hack production, blackmail, and data protection for Hansen's guests; avoid the Blackwall grand project and NetWatch",
      "members_hint": "Ayo Zarin, Milko Alexis; sts_ep1_12 33 roster units; we_ep1_05_com 20 + _2ndloop 16 + _reinf 5; q303_com_voodoo_boys_guards 21 + _reinforcements 10 + _rooftop_guards 5 (overlapping phases)",
      "source": "wiki Voodoo Boys (Dogtown database entry), Slider, Ayo Zarin, Milko Alexis, The Damned, Gig: Treating Symptoms; raw sts_ep1_12/we_ep1_05/q303 communities",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The Haitian community / congregation (non-member constituency)",
      "leader": null,
      "goals": "Survival, autonomy, communal law, and protection from NCPD and corporate eviction",
      "members_hint": "Grann Ertha (Character.q110_grann_ertha), the butcher-shop vendor (Character.q110_butcher_shop_vendor), the chapel sermon leader (Character.q110_sermon_leader), the Batty's Hotel market community; not gang members",
      "source": "wiki Grann Ertha, Voodoo Boys, The Voodoo Boys: What We Know and What We Don't; raw q110 communities",
      "confidence": "game-data+wiki"
    },
    {
      "name": "NetWatch mole (non-member power centre)",
      "leader": "Alan Noel",
      "goals": "Dismantle the Dogtown Voodoo Boys' implant-blackmail network from within and advance his NetWatch career",
      "members_hint": "Character.sts_ep1_12_alan_noel; one undercover agent inside Milko's cell",
      "source": "wiki Alan Noel, Gig: Treating Symptoms, Voodoo Boys Operational Base Search Report",
      "confidence": "game-data+wiki"
    }
  ],
  "relations": [
    {
      "faction_code": "tyger_claws",
      "stance": "neutral",
      "evidence": "No attested conflict; VDB bootleg hacks are sold under the counter in Kabuki and a VDB recruitment shard sits in Little China (ma_wat_lch_10), but these are commercial adjacency, not a feud [game-data] [wiki] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "valentinos",
      "stance": "neutral",
      "evidence": "No attested interaction; different district (Heywood) [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "arasaka",
      "stance": "hostile",
      "evidence": "VDB hired Evelyn Parker to steal the Relic prototype from Yorinobu Arasaka; corporate databank theft is their primary income; Slider refuses jobs against Arasaka as too dangerous [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "militech",
      "stance": "rival",
      "evidence": "Militech combat robots found at the Luxor spa; NetWatch search report flags possible corporate espionage or sabotage [game-data] [wiki]; corporate data theft targets Militech among others; Slider refuses Militech jobs. No direct firefight attested [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "kang_tao",
      "stance": "neutral",
      "evidence": "No specific operation attested; only generic corporate data theft [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "biotechnica",
      "stance": "neutral",
      "evidence": "No specific operation attested [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "petrochem",
      "stance": "neutral",
      "evidence": "No specific operation attested [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "barghest",
      "stance": "trade",
      "evidence": "Dogtown VDB protect Hansen's guests' data and cover their tracks; in business with BARGHEST as frequently as they clash; symbiotic but shaky, kept to a little rumble here and there [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "sixth_street",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "aldecaldos",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "wraiths",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "animals",
      "stance": "hostile",
      "evidence": "NetWatch hired the Animals to guard the Grand Imperial Mall; VDB fight them in I Walk the Line; wiki records a VDB-Animals rivalry [wiki] [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "the_mox",
      "stance": "neutral",
      "evidence": "No institutional link; the VDB betrayal of Evelyn Parker (a Clouds doll and Judy Alvarez's friend) is a personal grievance, not a VDB-Mox relation [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "maelstrom",
      "stance": "neutral",
      "evidence": "No attested interaction; different district and different obsession (chrome vs the Net) [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "ncpd",
      "stance": "hostile",
      "evidence": "VDB are the de facto law in Pacifica and hold it against NCPD/corporate eviction; NCPD has no power there [wiki]; VDB records appear in NCPD crime-scene/patrol areas (cs_police_execution_com, cs_highway_patrol_com) [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "night_corp",
      "stance": "neutral",
      "evidence": "No attested interaction; a corporation, not a Pacifica turf actor [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "city_council",
      "stance": "neutral",
      "evidence": "No attested interaction; the VDB are outside city political authority [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "scavengers",
      "stance": "hostile",
      "evidence": "Placide orders Fara Dupont to surround and kill Scavengers who raided a NetWatch stash; four VDB members (Fara Dupont, Diesuel, Josue, Lovelie) were killed by Scavengers; both operate in Pacifica/West Wind/Terra Cognita [wiki] [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "fixer_regina",
      "stance": "neutral",
      "evidence": "No VDB-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_wakako",
      "stance": "neutral",
      "evidence": "No VDB-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_padre",
      "stance": "neutral",
      "evidence": "No VDB-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_el_capitan",
      "stance": "neutral",
      "evidence": "No VDB-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_dakota",
      "stance": "neutral",
      "evidence": "No VDB-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_dino",
      "stance": "neutral",
      "evidence": "No VDB-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_rogue",
      "stance": "neutral",
      "evidence": "No VDB-specific gig; Afterlife is neutral ground [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_mr_hands",
      "stance": "trade",
      "evidence": "Pacifica fixer who brokers V's access to the VDB and volunteers V for Placide's Grand Imperial Mall job; later hires V to neutralize Milko (Gig: Treating Symptoms) and moves against Ayo Zarin's cell in Phantom Liberty; a transactional broker, not a loyal ally [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "afterlife",
      "stance": "neutral",
      "evidence": "Neutral merc marketplace; no VDB-specific link [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "netwatch",
      "stance": "war",
      "evidence": "NetWatch maintains the Blackwall and hunts rogue netrunners/AI contact; Bryce Mosley maps and shuts down Rezo Agwe and freezes Brigitte and Ti; Alan Noel infiltrates the Dogtown cell; Placide's virus targets NetWatch agents; NetWatch agents are present across the city (cvi/kab/cpz_netwatch_agent_*) [wiki] [game-data]",
      "confidence": "game-data+wiki"
    }
  ]
}
```
