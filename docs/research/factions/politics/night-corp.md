# Night Corp and the Government of Night City — Leadership, Blocs and Political Levers

Status: faction politics research run, 2026-11-25. One document, two bodies.
Scope: Cyberpunk 2077 2.5 + Phantom Liberty, campaign disabled, alternate
timeline per `docs/design/gameplay-systems.md` §7. These are the two **special
political factions with no territory** named in `gameplay-systems.md` §1: Night
Corp (`night_corp`, fid 40) and the Government of Night City / City Council
(`city_council`, fid 51). The document covers who leads each, the blocs inside
each, the external-relations matrix from Night Corp's side, and every attested
**lever** either body holds over territory and factions — raw material for the
title/claim system in `gameplay-systems.md` §4. No mechanics are designed here.

Method: follows [`METHOD.md`](./METHOD.md), including its §1.1–§1.3
corrections, and the data pitfalls in [`../METHOD.md`](../METHOD.md)
§1.1–§1.2. `AGENTS.md` was read first. Night Corp's location catalogue is
[`../night-corp.md`](../night-corp.md); this document does not repeat its
coordinates except where a person needs an anchor.

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Position, site, community, roster or raw-registry record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/artbook/tabletop/comic lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My reasoning links a named person, place or stance to a record; reasoning stated | Weak, flagged |

Presence classes (METHOD §2.5, §1.2 item 2): `ambient`, `world-activity`,
`story`, `prologue`, `off-map` (alive in lore, never spawned), `mentioned`
(named only in shards, dialogue or database entries), `historical`.
`open_world` is true only for `ambient`/`world-activity`.

**Up front, because it sets the shape of the whole doc:** both bodies are
almost entirely absent from the extract as *factions*. Night Corp has **0**
roster sites, **0** roster units, **0** community areas, **0** owned
sub-territories and no `gamedataAffiliation` value at all. The `city_council`
affiliation survives in exactly **three** community areas, and all three exist
to spawn **Lucius Rhyne and Weldon Holt** (plus generic cops and one assassin).
There is no sitting councillor NPC in the game outside a braindance. So this
document is, like the Arasaka one, mostly **wiki + registry + marker** work,
with the game data used to confirm which scenes are real and which markers are
centroid noise. `[game-data]`

---

## 1. Leadership and ranks

### 1.1 Two bodies, one city

| Body | What it is | Faction row | Extract footprint |
| --- | --- | --- | --- |
| **Night Corp** | Development firm and public-works corporation; the city's largest public-procurement contractor; NCART's parent; NCPD/MaxTac sponsor | `night_corp`, fid 40, `category: megacorp`, `affiliation_enum: null`, `income_multiplier 1.45`, `hostility_bias 0.25` | 0 sites, 0 units, 0 areas, 0 owned sub-territories. Only `q114` place assets (4 cars, 9 guard workspots, 1 AV spawn, 1 tunnel gate) — all Militech-garrisoned `[game-data]` |
| **Government of Night City** | Democratic mayoralty plus a 100-seat corporate-controlled City Council, headquartered at City Hall in the Glen | `city_council`, fid 51, `category: civic`, `income_multiplier 1.2`, `hostility_bias 0.2` | 3 community areas, 5 entries, 3 distinct people: Rhyne ×2, Holt ×2, Holt ×1. No sites, no CCs, no ownership `[game-data]` |

The relationship between them is the subject of the document. Short version:
**the council is the legal sovereign of the city; Night Corp is the contractor
that built it and still runs much of it; both fund the police, and neither can
field a garrison.** `[wiki]`

### 1.2 Night Corp: the chain of command

Night Corp is a family-founded but no longer family-run corporation. Richard
Night created the company that built the city; his widow ran it for decades;
by 2077 nobody the wiki will name is in charge.

| Name | 2077 role | Character record | Location / influence point | Presence class | Source | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| **Richard Night** | Founder of Night International (early 1990s) and of Coronado City; murdered 20 Sep 1998 at Parkview Tower | — (no `Character.*` record; only `mq061_06_Spawnpoint_Richard_Night_*` hologram spawnpoints) | Night Corp Tower (Downtown); Parkview Tower (death site); `mq061_06` holotour stop | `historical` | Wiki *Richard Night*, *Night Corp*; raw registry `mq061_06_Spawnpoint_Richard_Night_*` `[game-data]` | `[game-data]` `[wiki]` |
| **Miriam Night** | Richard's widow; founds Night's Foundation (1999), becomes Night Corp's CEO, later steps down | — | — | `historical` (status "Unknown" in 2077) | Wiki *Miriam Night*, *Night Corp* | `[wiki]` |
| **The Board / "the Company's Board"** | Collective sovereign of the 2077 corp; approves investment plans; unnamed members | — | Night Corp Tower, Downtown | `mentioned` | Shard *Night Corporation Construction Site: Access Strictly Prohibited* ("the Company's Board"); wiki *Night Corp* ("the corporation's rather mysterious structure") | `[wiki]` |
| **The 2077 executive tier** | "Much less competent leadership figures" who lost the race with Arasaka and Militech | — (no records) | Night Corp Tower, Downtown | `mentioned` | Wiki *Night Corp* database entry; `data/factions.json` `income_multiplier 1.45` | `[wiki]` |
| **Sandra Dorsett** | Night Corp netrunner; steals the Operation Carpe Noctem databank | `Character.mq024_sandra_combatable`; entries `sandra`, `sandra_holo`, `sandra_dorset__q000__sandra_dorset` | Sandra Dorsett's Apartment, Little China (Watson); Scav den (The Rescue) | `world-activity` | Raw `always_loaded_1` registry; minor job *Full Disclosure* (`baseid mq024_sandra`); wiki *Sandra Dorsett* | `[game-data]` `[wiki]` |
| **Sandra's unnamed supervisor** | The manager who turned on her over the AI project | — | Night Corp, unspecified | `mentioned` | Wiki *Sandra Dorsett* Humans-of-Night-City entry ("I even got my supervisor super competitive") | `[wiki]` |

Notes:

- **There is no CEO in 2077 and the wiki says so by omission.** The Night Corp
  infobox has `ceo =` empty and `members =` empty; the prose says Miriam "would
  eventually step down from the role of CEO during the following years" and
  that "the helm was taken over by much less competent figures." No successor is
  named anywhere on the wiki, in the game database entry, or in the shards. This
  is the single largest hole in either body's leadership. `[wiki]`
- **Richard Night's murderers are named but not charged.** The West Coast mob
  and the construction unions he cut out of the project are the wiki's
  attribution; "Night's killer was never apprehended." The same paragraph says
  the **newly appointed City Council** renamed Coronado City to Night City in
  his honour — the council and the corp are entangled from the first day.
  `[wiki]`
- **Night Corp's control is dynastic by intent, not by blood.** Miriam's
  "legacy and ideals were always upheld by her successors", and the database
  entry notes that "there are still those in the company's rather mysterious
  structure who have not lost faith in the vision of the city's founder." Those
  two sentences are the only evidence for an internal legitimacy bloc — see
  §2.1. `[wiki]`

### 1.3 The Government: mayor, council, parties

Night City is "a democratic mayoralty with a corporate-controlled city
council." Mayors are elected by simple majority through a Data Term using
IdentiCard registration software. The **council has 100 members, each usually
backed by one of the top ten largest corporations present in Night City.**
`[wiki]`

The mayor "oversees the treasurer's office, the deputies to the mayor and
directs the heads of the city's departments, such as the NCPD and the NCFD.
They have the power to appoint department heads and commissioners as well as
remove public officials from office." Part of the mayor's proposals need
council approval. `[wiki]`

| Name | 2077 role | Character record | Location / influence point | Presence class | Source | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| **Lucius Rhyne** | Mayor 2070–2077; councilman 2060–2070 (Devolutionist); Watson City Manager 2045; killed May 2077 | `Character.sq012_lucius_rhyne`; entry `q005_lucius_rhyne` | City Hall (Glen); Konpeki Plaza meeting room (ArasakaWaterfront); Red Queen's Race (CharterHill, death site); Columbarium niche | `story` | Raw registry (`{sq012_com_braindance}`, `{q005_com_flathead_room_b}`); markers `sq012_02a_sm_braindance`, `sq012_01a_sm_peralez_car`; wiki *Lucius Rhyne* | `[game-data]` `[wiki]` |
| **Weldon Holt** | Deputy Mayor 2070–2077; Acting Mayor 2077; election loser | `Character.sq012_weldon_holt` (entries `deputy_mayor`, `01_mayor_holt`); `Character.sq012_weldon_holt_clue` (entry `holt`) | City Hall conference room; Konpeki Plaza meeting; Black Sapphire gala (Dogtown); Red Queen's Race (arranged the cover-up) | `story` | Raw registry (3 communities); wiki *Weldon Holt*; area `{q303_com_paradise_quest_interactions}` `[game-data]` | `[game-data]` `[wiki]` |
| **Jefferson Peralez** | Councilman 2076–2077; DA before that; Mayor 2077– (still mayor in 2079) | `Character.Jefferson_Peralez`; entry `jefferson_holo` | Peralezes' Apartment, Charter Hill (Westbrook); City Hall; Reconciliation Park (Glen) | `story` | Raw registry; marker `sq012_08a_sm_peralez_apartment` (the apartment is `sq012`/`sq006` shared); `sq006_07a_sm_final_choice` (Reconciliation Park); wiki *Jefferson Peralez* | `[game-data]` `[wiki]` |
| **Elizabeth Peralez** | Lawyer; campaign principal; Federalist | `Character.Elizabeth_Peralez`; `Character.sq006_elizabeth_intercom` | Peralezes' Apartment; Yagami Market ramen shop (JapanTown) | `story` | Raw registry; wiki *Elizabeth Peralez* (no world-coordinate marker — `elizabeth_sm_peralez_default` reads `(8.590, 1.050, 0.760)`, a prefab-local position near the origin, and is rejected per METHOD §1.1 item 8) | `[game-data]` `[wiki]` |
| **Mbole Ebunike** | Mayor 2012–2023 (born Judson Freeman); stepped down | — | City Hall (old, City Center) | `historical` | Wiki *Mbole Ebunike* | `[wiki]` `[lore]` |
| **Garven Haakensen** | Deputy/Acting Mayor 2023; later City Manager of South Night City | — | City Hall; Haakensen Tower (SNC) | `historical` | Wiki *Garven Haakensen* | `[wiki]` `[lore]` |
| **Brad Noorwood** | Councilman; "a Militech fanboy in the Night City Council"; murdered by Militech-linked parties | — (no record) | City Hall; NCART Memorial Park Station (the gig) | `world-activity` | Gig *Serial Suicide* (`baseid sts_cct_cpz_01`); wiki *Government of Night City* | `[wiki]` `[game-data]` |
| **Eva Cole** | Councilwoman; anti-corruption; destroyed by a blackmail leak | — (no record) | Cannery Row marina, her yacht (Downtown, City Center) | `world-activity` | Gig *The Frolics of Councilwoman Cole* (`baseid sts_cct_dtn_05`); wiki *Eva Cole* | `[wiki]` `[game-data]` |
| **John McLean (McLane)** | Councilman; bought by Militech; assassinated by Benedict McAdams for Dakota Smith | — | — | `mentioned` | Shard *Archived Conversation: Dakota*; Gig *MIA* (`baseid sts_bls_ina_09`); wiki *John McLean* | `[wiki]` |
| **Jack Lars** | Councilman and NC Director of Urban Planning; close Militech ties | — | Wellsprings apartment (Heywood) | `off-map` | Wiki *Jack Lars*, citing the comic *Cyberpunk 2077: You Have My Word* | `[wiki]` `[lore]` |
| **Emilio Gutierrez** | Council candidate; sanitation budget; **cut content** | — | — | `mentioned` | Cut shard *Night City Council elections! Vote for Emilio Gutierrez!* (`baseid sts_wbr_hil_01_shard_001`) | `[wiki]` |
| **Georgina Zembinsky** | District Attorney, 2077 | — | Hall of Justice, the Glen | `mentioned` | Wiki *Government of Night City* | `[wiki]` |
| **Jerry Fawlter** | NCPD Commissioner from 2076; a dataterm sales executive; the mayor's appointee | — | NCPD HQ | `mentioned` | Wiki *Night City Police Department* | `[wiki]` |
| **The City Council (100 seats)** | Collective legislature; 99–1 on the *City of Opportunity* bill | — | City Hall, the Glen | `mentioned` | Wiki *Government of Night City*; wiki *Jefferson Peralez* | `[wiki]` |

Notes:

- **Rhyne is the only person in either body with a `city_council` faction-area
  record on three separate scenes.** `{sq012_com_braindance}` (2
  `city_council` entries), `{q005_com_flathead_room_b}` (2) and
  `{q303_com_paradise_quest_interactions}` (1, `01_mayor_holt`). That is the
  entire detectable footprint of the government as a *faction*. `[game-data]`
- **Brad Noorwood has no wiki page.** `action=parse&page=Brad Noorwood` returns
  no `parse` key; he exists only as a name in the gig journal entry and in
  Zoli Barnes' unfinished article. Do not seed him beyond the gig. `[wiki]`
- **John McLean's name is spelled both ways.** The page is *John McLean*; the
  body text says "John McLane"; the *MIA* journal entry says "Councilman
  McClean". One person. `[wiki]`
- **`Jerry Fawlter` is a government leader only in the appointment sense.** He
  is the mayor's creature and the reason the NCPD is a private-profit
  department; the NCPD doc owns his file. He is listed here because the
  appointment itself is the government's most consequential lever (§4). `[wiki]`

### 1.4 Succession history

| Period | Office | How the change happened |
| --- | --- | --- |
| 1994–1998 | City under Richard Night's company; **no elected mayor attested** | Night International builds and effectively runs Coronado City; the mob controls construction. `[wiki]` |
| 1998 | Council renames the city | Richard Night murdered; "the newly appointed City Council officially renamed Coronado City as Night City." `[wiki]` |
| 2012–2023 | **Mbole Ebunike** (mayor) | Elected after the Mob War as a corporate puppet; re-elected 2016, turned hostile to his backers, renamed himself; "suffered a nervous breakdown" in July 2023 and stepped down under Arasaka pressure. `[wiki]` |
| 2023 | **Garven Haakensen** (acting) | Took over as acting mayor; "much more compliant and obedient than Ebunike" and therefore acceptable to Arasaka; **fled the city** after the AHQ Disaster. `[wiki]` |
| 2023–2070 | **No mayor.** Council rule | "The office of mayor had been left vacant for years, and the city was instead ruled by the City Council", a junta of survivors, edgerunners, nomad factions and corporations — Zetatech, Biotechnica, Petrochem "and secretly Arasaka". Council-appointed **City Managers** ran each district. Faction friction "sometimes settled with violence on the streets." `[wiki]` |
| 2070 | **Lucius Rhyne** (mayor) | Rhyne leads the city's defence in the Unification War, brings Arasaka back with a supercarrier, wins the first mayoral election since 2023; his first act is to give Arasaka a **seat on the City Council**. `[wiki]` |
| 2077 (May) | **Weldon Holt** (acting) | Rhyne killed by a virus-spiked braindance at the Red Queen's Race; Holt covers it up and runs in his place. `[wiki]` |
| 2077 (election) | **Jefferson Peralez** (mayor) | Wins with 70.7% if V conceals the conspiracy, 49.3% if V tells him the truth. Still mayor in 2079. `[wiki]` |

The pattern is the opposite of Arasaka's. Arasaka's succession is dynastic and
covert; Night City's is **electoral, externally decided and frequently
vacant**. Three of the seven periods above have no functioning mayor at all, and
both 2077 transitions are decided by a murder and a brainwashing programme
rather than by voters. `[inferred]`

### 1.5 Rank structure, entry and advancement

**Night Corp.** No public ladder is attested. What the sources give:

1. **The Board / the "mysterious structure."** Unnamed, approves investment
   plans, "biometric access separating teams by floor to prevent
   cross-contamination of data." `[wiki]`
2. **Executives and administrators** — "thousands of engineers, analysts and
   administrators" in the Tower; employees know "only as much as they needed to
   do their jobs and little more." `[wiki]`
3. **Specialists** — netrunners (Dorsett), public-works engineers, the covert AI
   programme's staff. `[wiki]`
4. **NCART** — the subsidiary, run as a utility. `[wiki]`
5. **Contractors** — Lazarus (2045 tower security, solar-farm patrols) and
   Militech SiteSecure (maglev site). Night Corp fields no security of its own.
   `[wiki]` `[game-data]`

The recruitment pipeline is soft power, not a ladder: **Night Foundation
scholarships** (Peralez and Elizabeth both took them), orphanage donations,
charity for poor children, and the corp's ranking as the **5th-best employer in
Night City** after cutting the mandatory week to 80 hours. That is how the corp
recruits loyalty it cannot buy with a career path. `[wiki]`

**Government.** The ladder is statutory and is documented:

1. **Mayor** — appoints and removes department heads and commissioners; directs
   NCPD and NCFD; proposes budgets and bills. `[wiki]`
2. **Deputy Mayor** — inherits as acting mayor; Holt's route. `[wiki]`
3. **City Council (100 seats)** — legislates; each seat usually corporation-
   backed; can be bought, blackmailed or assassinated (§4). `[wiki]`
4. **City Managers** (2040s) — elected by the council, one per district; in
   charge of "zoning designations for corporations and neighborhoods, road
   infrastructure taxes, freelance private investigators and police licensing,
   and city contracts for construction and justice services." Their 2077 status
   is unverified (§7.4). `[wiki]`
5. **Department heads and commissioners** — NCPD, NCFD, Port Authority,
   Municipal Works, Business Licencing, DMV, Water, Environmental Task Force,
   Health, Landlord's Authority, Records Office, Recreation, Tourism. `[wiki]`
6. **District Attorney** — Zembinsky in 2077, Peralez before her. `[wiki]`

Entry is electoral or appointed; advancement is a matter of corporate backing.
Peralez's own biography is the model: poor kid → Night Corp scholarship →
Asukaga-Berkeley law → DA → council → mayor. `[wiki]`

### 1.6 What the game actually spawns

**`story`** — gated by quests; not present in free roam with the campaign
disabled: Rhyne, Holt, Jefferson Peralez, Elizabeth Peralez. Their phases are
`q005_*`, `sq012_*`, `sq006_*`, `q303_*`. `[game-data]`

**`world-activity`** — gig/scanner scoped, still not ambient: Noorwood (gig
*Serial Suicide*), Cole (gig *The Frolics of Councilwoman Cole*), Sandra Dorsett
(minor job *Full Disclosure*). **None of these three has a character record**;
they exist as names attached to a site, and the site's garrison is a third
party (Militech at Memorial Park Station, Animals at the marina/RQR). `[game-data]`

**`ambient`** — nothing. There is no councillor, mayor, city manager or Night
Corp employee who walks the street in free roam. The closest thing is
`static_city_hall_crowd_*`, `dynamic_city_hall_corp_*` and `city_hall_vendor_*`
crowd entries in the raw registry — set dressing at City Hall, no faction id.
`[game-data]`

**Conclusion:** with the campaign disabled the game supplies **no political
leadership at all**. Both bodies must be spawned by the mod, exactly as the
Arasaka doc concluded for that faction. `[game-data]` `[inferred]`

### 1.7 Player-path hooks

| Person / body | Join under | Climb past | Ally with | Remove |
| --- | --- | --- | --- | --- |
| **Night Corp (Board)** | A specialist or administrator role in a public-works or R&D wing; the corp hires quietly and promotes on results | The Board is the ceiling and has no faces; climbing means becoming the face the Board lacks | NCART, the NCPD funding relationship, city procurement officers | Expose Carpe Noctem (Dorsett's route), or take the procurement contracts (§4) |
| **The Night Corp "faithful"** | The founder's-vision wing; employees who want the corp back in power | The incumbent 2077 management is the obstacle, and they are weak | Residents who "wish for the day Night Corp returns to a position of true power"; the Council | Buy out or disgrace the incumbent tier; win a council seat for the corp |
| **Jefferson Peralez** | The Federalist anti-corporate campaign; union and worker networks | Holt's machine, then the SSI/"Voices" handlers who own his behaviour | 6th Street (bribery/intimidation), unions, River Ward, the media | Kill or expose him — but his handlers replace him rather than stop |
| **Elizabeth Peralez** | The campaign's operational core; the lawyer who runs it | She is a principal, not a subordinate; she has no ladder above her | Peralez, Judy Álvarez, V | Isolate her from Jefferson; she withdraws rather than fight (§2.9) |
| **Weldon Holt** | The Devolutionist, Arasaka-friendly machine; the NCPD and the corps | Arasaka is the ceiling; Max Jones says he is "in Arasaka's pocket" | Arasaka, the Animals (as hired wreckers), 6th Street contacts | Expose the Red Queen's Race cover-up (*I Fought the Law*) |
| **Eva Cole** | The reform bloc; the only councillor who "doesn't treat money with the respect and adoration it deserves" | The council's corporate majority is the ceiling | Peralez (before his election), the press | Blackmail (her own gig) or a leaked recording ends her |
| **The City Council as a body** | Buy or win a seat; 100 seats means the player can be one voice | The council is bought wholesale; one seat is worth little until a bloc forms | Whoever funds the campaign | Dissolve or capture the council by capturing the corps that back it |

The design consequence: **the two bodies offer two different climb paths.** A
player who joins Night Corp climbs a *corporate* ladder with no visible top
(the Board has no faces) and finds that the corp's real power is its contracts,
not its org chart. A player who joins the government climbs an *electoral*
ladder whose rungs are purchasable — and finds that the mayor's office is
occupied by someone else's candidate. Both are "join and work up" in the sense
of `gameplay-systems.md` §3, but neither produces a leader the player can
simply defeat in a room. `[inferred]`

---

## 2. Internal political factions

### 2.1 Night Corp: four wings, no parties

Night Corp has no attested political factions in the gang sense — no Royce-vs-
Brick. What it has is a **generational legitimacy split** and a **covert
operating wing**, both visible in the wiki's own language.

| Bloc | Leader(s) | What it wants | Presence / members hint | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- |
| **The founder's-vision wing ("the faithful")** | None named; "those in the company's rather mysterious structure who have not lost faith in the vision of the city's founder" | Restore Night Corp to "a position of true power"; keep Richard Night's civic mission; public works over profit | Unquantified; the corp's own netpage sells exactly this ("What IS Night Corporation? Richard Night's legacy. The foundation stone of Night City. Its silent, watchful guardian.") | Wiki *Night Corp* database entry and netpage | `[wiki]` |
| **The incumbent executive tier** | Unnamed "much less competent figures" | Manage the shrinking capital; keep the public-administration influence; avoid fights with Arasaka and Militech | The Board and the Tower staff; "biometric access separating teams by floor" | Wiki *Night Corp*; wiki *Night Corp Headquarters* database entry | `[wiki]` |
| **NCART (the subsidiary)** | None named | Run the metro; deliver the maglev revival (first links 2078, Chicago 2080); keep the City Pass revenue | 5 lines, 19 stations; the single operational asset the corp owns outright | Wiki *Night Corp*; wiki *NCART*; location doc §3 item 2 | `[wiki]` `[game-data]` |
| **The covert conditioning wing (Carpe Noctem / Condin)** | Sandra Dorsett's unnamed supervisor; SSI "Management"; "Chief of Security Wallace" (SSI) | Condition employees, then officials, into compliant behaviour; mold the ideal mayoral candidate | Carpe Noctem databank; SSI's ORANGE/BLUE/BLACK teams; the "Sector Zero" room and the roof transmitter | Wiki *Night Corp* (AI conditioning); wiki *Secure Services Inc.* (Condin); wiki *Dream On* | `[wiki]` `[game-data]` `[inferred]` |

Notes:

- **The last row is the whole plot and it is officially a rumour.** The corp's
  own database entry frames it as conspiracy: "rumors also tell of their
  underwater works in Del Coronado Bay, **secretive engagement in mayoral
  elections**, and their shares in the orbital station projects." The
  *Dream On* page states that "it is implied by Sandra Dorsett's quest that
  Night Corp is the entity behind SSI and the neuroplasticity experiments" and
  that this "is backed up by references in the 2077 world book." Treat the
  identity as `[inferred]` with wiki support, not as a proven fact — but treat
  the *capability* (an AI that conditions people, and a mayoral candidate under
  conditioning) as attested. `[wiki]` `[inferred]`
- **The two wings are not at war; they are unaware of each other.** Nothing in
  the sources has the founder's-vision wing opposing the conditioning wing. The
  likely friction is that the conditioning wing is what *prevents* the corp
  from returning to open power: it works through proxies and secrecy, which is
  the opposite of the faithful's civic-legitimacy route. That is a
  simulation-ready tension, and it is `[inferred]`. `[inferred]`
- **The corporate-security gap is structural, not a faction.** Night Corp buys
  its guards (Lazarus, Militech SiteSecure) and therefore has no internal
  security constituency — the opposite of Arasaka, where Smasher's apparatus is
  a power centre. `[wiki]` `[game-data]`

### 2.2 The Government: five blocs and one shadow

| Bloc | Leader(s) | What it wants | Presence / members hint | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- |
| **Devolutionist Party** | Lucius Rhyne (until 2077), then Weldon Holt | Night City's autonomy inside a devolved NUSA; corporate freedom; Arasaka as guarantor | Mayor's office; the council seats Rhyne and Holt held | Wiki *Lucius Rhyne* (Devolutionist affiliation); wiki *Devolutionist Party*; wiki *Weldon Holt* | `[wiki]` |
| **Federalist Party** | Jefferson Peralez; Elizabeth Peralez | Federal alignment; anti-corporate populism; the "City of Opportunity" reversal | Council seat; the campaign; the Peralez apartment as campaign HQ | Wiki *Jefferson Peralez*; wiki *Federalist Party*; wiki *Elizabeth Peralez* | `[wiki]` |
| **The corp-bought council bloc** | None; individual patrons | Pass pro-corporate measures; keep the tax exemptions; protect patrons from NCPD jurisdiction | 99 of 100 seats on the *City of Opportunity* vote; Noorwood (Militech), McLean (Militech), the unnamed councillor pressured by Arasaka reps over a Japantown building, Lars (Militech, comic) | Wiki *Jefferson Peralez* (99–1 vote); gigs *Serial Suicide*, *MIA*, *Frolics of Councilwoman Cole*; wiki *Government of Night City* (Arasaka pressure anecdote) | `[game-data]` `[wiki]` |
| **The reform bloc** | Eva Cole; Peralez before his election | Crack down on corporate corruption; refuse bribes; investigate | Cole alone after Peralez leaves the council; Peralez's lone dissenting vote | Wiki *Eva Cole*; wiki *Jefferson Peralez* | `[wiki]` |
| **The City Manager layer (historical)** | 2045 district managers (Rhyne in Watson, Freeman in the Glen, Haakensen in SNC, …) | District control of zoning, licensing and contracts; personal enrichment | 22 named 2040s managers; Haakensen's tenure is the fully documented case | Wiki *Government of Night City* (2045 manager list); wiki *Garven Haakensen* | `[wiki]` `[lore]` |
| **The Peralez conspiracy (SSI / "Condin" / Mr. Blue Eyes)** | Mr. Blue Eyes (unidentified proxy); SSI Chief of Security Wallace; "management" | Install a conditioned mayor; keep the operation invisible; delete its own data | SSI ORANGE/BLUE/BLACK teams, Sector Zero, the roof transmitter, the mobile data centre van, the Maelstrom escort | Wiki *Dream On*; wiki *Secure Services Inc.*; wiki *Mr. Blue Eyes*; shard *PROJECT CONDIN SUSPENDED* | `[game-data]` `[wiki]` |

Notes:

- **The parties are national, not municipal.** Devolutionist vs Federalist is
  the NUSA/Free State cleavage from the Unification War, imported into a city
  election. That is why Rhyne's sponsor (Arasaka) and Holt's sponsor (Arasaka)
  and Peralez's backers (unions, 6th Street) line up the way they do: the
  election is a proxy for the NUSA question. `[wiki]` `[inferred]`
- **The 99–1 vote is the cleanest single number in this document.** The *City
  of Opportunity* bill exempted **32 of the largest corporations** from taxes
  "via a loophole"; it passed **99–1**, Peralez the lone holdout. That is the
  council's baseline behaviour, not an aberration. `[wiki]`
- **The council is bought with three different currencies.** Militech buys
  councillors (Noorwood, McLean, Lars). Arasaka applies direct pressure on a
  single real-estate vote. Corporate donors buy blackmail on the honest ones
  (Cole's orgy footage). None of the three is influence-peddling in the
  abstract: each is a specific transaction attached to a specific measure.
  `[wiki]`
- **The conspiracy is a bloc, not a faction.** SSI was a real licensed
  contractor with a real client list; ORANGE (visible detail), BLUE and BLACK
  (covert) were compartmented inside it; "management" sat above Wallace. The
  wiki has SSI at 2062 founding, 2077 small-company tier, clients all over the
  city. The operation's codename is **CONDIN**, Jefferson is "target ALPHA", the
  hidden room is "Sector Zero". All of that is game-attested via *Dream On*.
  `[wiki]` `[game-data]`
- **Mr. Blue Eyes is a non-member power centre, not a member.** He cannot be
  interacted with or harmed; he watches the Reconciliation Park meeting from a
  balcony; he telephones V with a warning that "nothing will change." Treat him
  as `client`/asset-tier influence in the design's terms, not as a council
  actor. `[wiki]` `[game-data]`

### 2.3 What could drive internal conflict in a simulation

Evidence-based, in rough order of plausibility:

1. **The corp's legitimacy problem.** The faithful want open civic power; the
   incumbents work through secrecy and proxies. Every success of the covert
   wing makes the faithful's route harder. `[inferred]`
2. **Carpe Noctem exposure.** Sandra Dorsett holds a databank proving the corp
   conditioned its own employees and "other figures Night Corp deemed useful."
   One leak and the corp's public-administration role is gone. `[wiki]`
3. **The Board's invisibility.** No named board member means no legitimate
   authority to negotiate with. Any player-facing deal with Night Corp has to
   invent a signatory, or route through NCART or a department. `[inferred]`
4. **The 2077 mayoral transition.** Rhyne dead, Holt acting, Peralez winning.
   Three claims to one office in one year, and the previous transition (2023)
   ended with no mayor for 47 years. `[wiki]`
5. **The conditioning of the winner.** If Peralez is mayor and conditioned, the
   government's policy is being written by an unidentified third party. That is
   the largest single instability in the city's politics. `[wiki]`
6. **The corp bloc's discipline.** 99–1 is not a coalition; it is a purchased
   majority. It holds only while the corps keep paying, and the Pacifica/Kang
   Tao lot shows the price falling to one eurodollar. `[wiki]`
7. **The reform bloc's fragility.** Cole is destroyed by one recording; Peralez
   leaves the council to become mayor and the seat of opposition empties.
   `[wiki]`
8. **The City Manager question.** If the 2040s manager offices still exist in
   some form, they are the layer that actually signs zoning and licensing — a
   parallel authority under the council, with its own corruption history.
   `[wiki]` `[inferred]`
9. **Police funding.** Night Corp's coffers are shrinking; the NCPD is
   privatised and unprofitable; the mayor's office is openly considering
   replacing the police with corporate security firms. Whoever pays the police
   owns the streets. `[wiki]`
10. **The NUSA question.** The Devolutionist/Federalist split is the same fight
    as 2069–70, unresolved by the Arvin Accord. `[wiki]`

---

## 3. External relations matrix

### 3.1 Stance vocabulary and direction

One stance per row, read **from Night Corp's side**, per METHOD §3 and §1.2
item 8. Direction is stated explicitly in every evidence string, because a corp
that hires a gang and a corp that is hired by the city are both "transactions":

- **`patron`** — Night Corp funds, supplies or protects the other side.
- **`client`** — Night Corp depends on or works for the other side.
- **`trade`** — transactional exchange, no loyalty, no protection.

The Government's stances differ from Night Corp's in several rows and are
described in §3.3 rather than forced into the same table, because the two
bodies are not one actor.

There is **no offline attitude matrix.** `Affiliation.hpp` is an identity enum;
`Attitude_Record.hpp` is opaque. Every stance below is judged from quests, the
wiki and spatial adjacency, and tagged accordingly.

### 3.2 The matrix

| Faction | Code | Stance | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| Tyger Claws | `tyger_claws` | `neutral` | No attested interaction. The only contact is spatial and seeded: `cc_dtn_corporation_st` (143 m from Night Corp Tower) is seeded to faction id **2 = Tyger Claws**, and `ma_cct_dtn_07` (92 m from the tower) is a Tyger Claws site, so the corp's own street is seeded to the Claws. That is a seed conflict, not a relationship `[game-data]` `[inferred]` | `game-data+inferred` |
| Valentinos | `valentinos` | `neutral` | No attested interaction. Adjacent only through the seed: the Glen blocks around City Hall (`gle_reconciliation_park`, `gle_ventura_skyline`) are seeded to faction id **3 = Valentinos**, so the seat of government sits in Valentinos-seeded turf in the seed. No lore contact `[game-data]` `[inferred]` | `game-data+inferred` |
| Arasaka | `arasaka` | `rival` | Night Corp "lost the race against major corporations such as Arasaka and Militech, both of whom came to wield the most power in Night City". Arasaka was given a **council seat** by Rhyne in 2070, and Arasaka reps pressure a councillor over a Japantown building purchase. Arasaka Tower is 374 m from Night Corp Tower `[wiki]` `[game-data]` | `game-data+wiki` |
| Militech | `militech` | `trade` | Night Corp **hires** Militech: "Militech SiteSecure" guards the maglev construction site, and the six-droid garrison at `{q114_com_construction_nc_security}` is Militech. Militech also took over security at NCART Memorial Park Station after Zoli Barnes' death. A commercial security contract inside a rivalry `[game-data]` `[wiki]` | `game-data+wiki` |
| Kang Tao | `kang_tao` | `neutral` | No attested interaction with Night Corp. Kang Tao's city-facing play is the Pacifica server lot, negotiated with the **council**, not the corp `[wiki]` `[inferred]` | `wiki+inferred` |
| Biotechnica | `biotechnica` | `neutral` | No attested interaction. Biotechnica sat on the 2045 council junta alongside Night Corp's city, not with the corp `[wiki]` `[inferred]` | `wiki+inferred` |
| Petrochem | `petrochem` | `trade` | The **Northern Oil Fields** are "a joint project of Petrochem and Night Corp", and Night Corp **brokered the Petrochem–SovOil peace** over those fields after the Fourth Corporate War. A commercial joint venture between rivals `[wiki]` `[game-data]` | `game-data+wiki` |
| Barghest | `barghest` | `neutral` | No attested interaction. Dogtown is outside city administration and outside Night Corp's contracts; the wall that created Dogtown was a **council** decision `[wiki]` `[inferred]` | `wiki+inferred` |
| 6th Street | `sixth_street` | `neutral` | No attested interaction with Night Corp. 6th Street's city-politics role is election dirty work for Peralez and Holt, i.e. Government-facing `[wiki]` `[inferred]` | `wiki+inferred` |
| Aldecaldos | `aldecaldos` | `trade` | Night Corp "were a major reason as to why the nomads traveled to Night City to help", offering "generous pay and free cyberware and biomonitor upgrades to anyone willing to help clean up the crater" — and the cleanup crews were "especially … the Aldecaldos nation". A paid, one-off labour contract `[wiki]` | `wiki` |
| Wraiths | `wraiths` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Animals | `animals` | `neutral` | No attested interaction with Night Corp. Animals' documented city-politics role is Holt hiring them to wreck the Red Queen's Race — Government-facing. Animals do hire out as bodyguards, but no Night Corp contract is attested `[wiki]` `[inferred]` | `wiki+inferred` |
| The Mox | `the_mox` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Maelstrom | `maelstrom` | `trade` | A deniable one-off hire: SSI's BLACK team drove its data-centre van into a **Maelstrom compound near All Foods**, and a Maelstrom goon named Dante led the ambush that covered their tracks ("Need your boys' help like last time"). SSI→Night Corp is `[inferred]`, so this row is two links deep `[wiki]` `[inferred]` | `wiki+inferred` |
| Voodoo Boys | `voodoo_boys` | `rival` | A property dispute, not a war: the **Old Maglev Tunnel** is Night Corp's *de jure* and the Voodoo Boys hold it as a data fortress (*de facto*). `gamedataDistrict.Coastview_VDBMaglev = 40` names the place for its occupier. No violent event is attested between the corp and the gang `[game-data]` `[wiki]` | `game-data+wiki` |
| NCPD | `ncpd` | `patron` | Night Corp **funds** the police: "the NCPD is also partly financed by Night Corp's shrinking coffers"; "the police force's official sponsor is Night Corp"; MaxTac's funding likewise. Also the design's own fallback: with no Night Corp affiliation in the game, Night Corp places are assigned to NCPD. Direction: Night Corp pays, NCPD receives `[wiki]` `[game-data]` | `wiki+game-data` |
| Scavengers | `scavengers` | `hostile` | Scavengers kidnapped Night Corp netrunner Sandra Dorsett and her Carpe Noctem databank, and Night Corp's covert operations run through scav dens (the databank recovery happens in a Scav-infested building). The corp's data is a standing target for the scav trade `[game-data]` `[wiki]` | `game-data+wiki` |
| City Council | `city_council` | `patron` | Night Corp has "a significant say in matters pertaining to the public administration", funds the scholarships that produced the mayor, and in 2078 obtained a **council-approved investment plan** for its Complex while seizing market stalls under threat of prosecution. Direction: Night Corp funds and cultivates councillors; the council returns approvals `[wiki]` | `wiki` |
| Afterlife | `afterlife` | `neutral` | No attested interaction; a merc marketplace, not a political actor `[inferred]` | `inferred` |
| Regina Jones | `fixer_regina` | `neutral` | No Night Corp-specific gig. Regina's city-politics gig (*Freedom of the Press*) protects a muckraker who says Holt is in Arasaka's pocket — Government-facing `[wiki]` `[inferred]` | `wiki+inferred` |
| Wakako Okada | `fixer_wakako` | `neutral` | Indirect only: Wakako brokers the return of Night Corp's stolen Carpe Noctem databank to Sandra Dorsett, who intends to "use the databank to fight against Night Corp". The channel works *against* the corp; no direct corporate relationship is attested `[wiki]` | `wiki+inferred` |
| Sebastian Ibarra (Padre) | `fixer_padre` | `neutral` | No Night Corp-specific gig or lore link found `[inferred]` | `inferred` |
| Muamar Reyes (El Capitán) | `fixer_el_capitan` | `neutral` | No Night Corp-specific gig or lore link found `[inferred]` | `inferred` |
| Dakota Smith | `fixer_dakota` | `neutral` | No Night Corp contact. Dakota commissions the assassination of a Militech-bought **councillor** — Government-facing `[wiki]` `[inferred]` | `wiki+inferred` |
| Dino Dinovic | `fixer_dino` | `neutral` | Dino runs both council gigs (*Serial Suicide*, *Frolics of Councilwoman Cole*) and profits from corpo contracts in Downtown — Government-facing, and transactional even then `[wiki]` `[inferred]` | `wiki+inferred` |
| Rogue Amendiares | `fixer_rogue` | `neutral` | No Night Corp-specific gig or lore link found `[inferred]` | `inferred` |
| Mr. Hands | `fixer_mr_hands` | `neutral` | No Night Corp-specific gig or lore link found `[inferred]` | `inferred` |
| Orbital Air | `orbital_air` | `rival` | Night Corp "cut all ties with Orbital Air, starting a sort of cold war between them" after OA abandoned the mass driver and built the NCX Spaceport instead; residents speculate Night Corp will push OA out of the city `[wiki]` | `wiki` |
| NUSA | `nusa` | `neutral` | No attested corporate interaction. The NUSA is the *government's* adversary (2070 invasion, Arvin Accord), and Night Corp's business is the free city's infrastructure — but no source has the corp taking a side `[wiki]` `[inferred]` | `wiki+inferred` |

Stance counts (29 rows): **neutral 19, trade 4, rival 3, patron 2, hostile 1,
ally 0, client 0, war 0.**

The three that matter most:

1. **`ncpd` — `patron`.** Night Corp pays the police and MaxTac. This is the
   single lever that makes the corp politically real despite owning no ground.
2. **`city_council` — `patron`.** The corp's contracts, its investment plans
   and its scholarship pipeline all run through the council. This is corporate
   capture by transaction, not by seat.
3. **`arasaka` — `rival`.** The corp lost the city to Arasaka and Militech. It
   is the reason Night Corp is "declining but structurally embedded" rather than
   dominant.

The matrix is overwhelmingly `neutral` because the faction has **no
footprint**. That is an honest result, not a gap in the research: 19 of 29 rows
are placeholders. Do not promote any of them without evidence. `[inferred]`

### 3.3 Where the Government's stances differ

The council and mayor's office are not the corp's stances and must not be read
off §3.2. Their distinct positions, attested:

| Toward | Government stance | Evidence |
| --- | --- | --- |
| **Arasaka** | `patron` (the corp protects the city) | Rhyne invited Arasaka back in 2070; Arasaka's supercarrier ended the war; Rhyne's first act as mayor was to give Arasaka a **council seat**; Arasaka reps lobby councillors directly over Japantown property `[wiki]` |
| **Militech** | `trade` (purchased influence, no loyalty) | Three Militech-bought councillors (Noorwood, McLean, Lars); Militech scapegoated McLean's assassin to bury the corruption and put a bounty on him. The NUSA's defeat in 2070 was a Militech defeat `[wiki]` `[game-data]` |
| **NUSA** | `hostile` | The 2069–70 Unification War; the NUSA army assaulted the city's outskirts; the Arvin Accord left the borders ambiguous rather than settled `[wiki]` |
| **6th Street** | `trade`, with coercion | Peralez "was embraced by the city's worker unions, some of which had close associations with 6th Street", and "there were cases of 6th Street using bribes and intimidation tactics to force citizens to vote for him"; Holt used a 6th Street contact (Julia Bonet) against Peralez's union ally `[wiki]` |
| **Animals** | `client` (hired muscle) | Holt hired the Animals to wreck the Red Queen's Race and then failed to pay them `[wiki]` |
| **Barghest** | `neutral` / de facto non-relation | The council **walled off** Serenisands to create Dogtown; the NCPD is forbidden inside; MaxTac is the one NCPD unit allowed in; Barghest is the local law. The council has no authority there and Holt attends Hansen's Black Sapphire gala as a guest `[wiki]` `[game-data]` |
| **Voodoo Boys** | `neutral` / de facto non-relation | The NCPD withdrew from Pacifica in 2072 under VDB-led riots; the VDB are "the de-facto authority in the western area of the district" `[wiki]` |
| **Kang Tao** | `trade` (a live negotiation) | The council debated selling Kang Tao a Pacifica lot "for a single eurodollar in exchange for a pledge to help quell the district's rampant crime" `[wiki]` |
| **Night Corp** | `client` (the city depends on the contractor) | Night Corp is the largest public-procurement contractor; NCART is its subsidiary; it funds the NCPD the city directs `[wiki]` |
| **Scavengers** | `hostile` (criminal, not political) | Scavs prey on Pacifica and the Badlands; the NCPD treats them as a crime category, not a faction `[wiki]` `[inferred]` |
| **Media (News 54, WNS, NC Inquirer, Max Jones)** | `trade` / `hostile` (varies by outlet) | Max Jones reports Holt is in Arasaka's pocket and gets a hit put on him (Regina's gig); N54/WNS/NC Inquirer all cover the election result `[wiki]` |

### 3.4 Actors outside `data/factions.json`

Real, attested, and no faction code — prose only:

- **The NUSA federal government** — the external sovereign Night City left.
  Beyond the `nusa` row: the war, the treaty and the ambiguity are the city's
  founding political fact. `[wiki]`
- **The Free States of North America** — the Devolutionist bloc; Night City's
  independence is a Free State outcome. `[wiki]`
- **Secure Services Inc. (SSI)** — the Condin front; a licensed contractor, not
  a faction. `[wiki]`
- **Mr. Blue Eyes** — unidentified proxy; watches the Peralez meeting, handles
  Songbird's moon flight in the PL timeline (non-canon here), hires V in *Path
  of Glory*. Treat as a `client`-tier asset with unknown backing. `[wiki]`
- **PacCon Electric** — manages Night Corp's Jackson Plains solar farm and the
  city-owned wind farms; a joint-venture partner. `[wiki]`
- **Lazarus** — Night Corp's 2045 security provider at the tower and the solar
  farm. `[wiki]`
- **SovOil** — the third owner of the Northern Oil Fields; Night Corp brokered
  its peace with Petrochem. `[wiki]`
- **The Night City Co-Prosperity Sphere (NCCS)** — defunct 2020s Japanese
  corporate bloc (Kendachi, Kiroshi, Nakagawa Foundation, Segotari); a 2045
  council constituency, not a 2077 actor. `[wiki]`
- **The Dorado Clan** — ran NCTC/NCART from 2039; a reclaimer group, not a
  faction. `[wiki]`
- **Halsey, Ferris & Skiv (HFS)** — the construction firm that built the Black
  Sapphire and, in its earlier form as Halsey, Ferris and Night, employed
  Richard Night. A contractor with a century-long grudge. `[wiki]`
- **The unions and worker networks** — Rancho Coronado Workers United and its
  president Ivan Vassiliev; Peralez's organised base. `[wiki]`

### 3.5 Guarantor assessment

If a player founds an organisation in Night City, which of these two bodies
would guarantee anything?

- **The Government cannot guarantee ground.** It has no garrison, no territory
  and no police it controls outright (the NCPD is privatised, underfunded and
  partly owned by Night Corp, Arasaka and Militech). What it can grant is
  **title** — and that is precisely the design's `title holder` slot in
  `gameplay-systems.md` §4. A council resolution, a zoning change or a
  procurement award is a legal claim with no enforcement behind it. `[inferred]`
- **Night Corp cannot guarantee ground either**, and for a sharper reason: it
  owns infrastructure, not blocks. Its guarantees would be **service
  guarantees** — transit, power, water, net — which are chokepoints rather than
  territories. `[inferred]`
- **Both are better patrons than allies.** Night Corp funds the police and the
  council approves the budget; a player who takes either as a guarantor inherits
  the other's enemies (Arasaka, Militech, Orbital Air for the corp; the
  Devolutionists' or Federalists' opposite number for the government) and,
  worse, inherits an institution with no way to defend the player's claim.
  `[inferred]`
- **The realistic guarantor pattern is a slice, not the whole.** A single
  councillor's vote, one NCART line, one procurement contract, one district
  manager's signature. That is what both bodies actually have to give, and it
  is consistent with a fleet of `trade` and `patron` rows rather than a single
  `ally`. `[inferred]`
- **No `ally` rows exist in either direction.** Not for Night Corp, and not for
  the government toward anyone. That is a real finding, not a placeholder: a
  city government whose every relationship is a purchase or a bribe has no
  friends. `[inferred]`

---

## 4. Levers: what these two bodies can actually do to territory and factions

This is the raw material for the title/claim system in
`gameplay-systems.md` §4. Facts only; the mechanics are not designed here.
Every row is attested; the "instance" column names the concrete case the game
or the wiki actually shows.

| # | Lever | Who holds it | Attested instance | Evidence |
| ---: | --- | --- | --- | --- |
| 1 | **Police budget and funding** | Mayor + council (budget); Night Corp (sponsorship) | Night Corp partly finances the NCPD and MaxTac "though every passing day their coffers kept shrinking"; the NCPD's "official sponsor is Night Corp"; the force's capitalization dropped 17% in early 2077 and the Mayor's Office began considering corporate security firms instead | `[wiki]` |
| 2 | **Appointment and removal of department heads and commissioners** | Mayor | Rhyne's cost-cutting plan led to the NCPD being "transferred to private ownership" and a dataterm sales executive, Jerry Fawlter, being installed as commissioner in 2076; he fired half the officers and cut patrols | `[wiki]` |
| 3 | **Legislation, including tax exemptions** | Council (100 seats) | The *City of Opportunity* bill exempted 32 of the largest corporations from taxes; it passed **99–1**, Peralez dissenting | `[wiki]` |
| 4 | **Granting police powers** | Council, on NCPD petition | NCPD officers may detain without charges for up to a year; a limb shot counts as a warning shot; fleeing vehicles may be fired on; collateral civilian deaths are "unofficially permissible" against a cyberpsycho | `[wiki]` |
| 5 | **Statutory programmes with tenders** | Council | The **Avian Extermination Act** (4 May 2063): exterminate all avian life within 18 miles of city limits, with "the call and selection of tenders for the contract" | `[wiki]` |
| 6 | **Public procurement contracts** | Council awards; Night Corp is the largest recipient | Night Corp is "the largest contractor of public procurements within Night City's boundaries", building roads, bridges, tunnels, metro lines, power plants, net transmitters, waterworks and sewerage | `[wiki]` |
| 7 | **Zoning designations** | City Managers (2040s); mayor + council by 2077 | City Managers were "in charge of … zoning designations for corporations and neighborhoods" and of "city contracts for construction and justice services" | `[wiki]` |
| 8 | **Land transfer and the corporate buy-up** | Council approval; mayor's signature | Rhyne and Holt met Arasaka reps at Konpeki Plaza "to discuss Arasaka's plans to buy up low-income housing in Watson for corporate re-development"; Rhyne was reluctant because Watson was his constituency | `[wiki]` `[game-data]` |
| 9 | **Single-building sale pressure** | Individual councillors | An unnamed councilman "in the cafe in front of Arasaka Tower … being pressured by an Arasaka representative to throw his support behind a measure that would allow Arasaka to buy a building in Japantown" | `[wiki]` |
| 10 | **Land sale for a token price** | Council | The council debated selling Kang Tao a Pacifica lot "for a single eurodollar in exchange for a pledge to help quell the district's rampant crime" | `[wiki]` |
| 11 | **Property seizure under an approved investment plan** | Council approval; Night Corp as acquirer | Night Corp's Complex construction site: "With the investment plan approved by the Night City Council", former market vendors are barred, pickets banned, and trespassers "subject to criminal prosecution"; acquired 12/16/2078 | `[wiki]` |
| 12 | **Redrawing administrative boundaries** | Mayor | Rhyne re-designated Pacifica an "independent district", removing it from the city's administrative boundaries so its crime statistics did not count; Holt and Rhyne took credit for a 3% crime-rate "drop" | `[wiki]` |
| 13 | **Decommissioning a police precinct** | Deputy Commissioner + mayor | On 17 Oct 2072 the Coastview precinct was "officially disbanded by Deputy Commissioner Claudia Feldman — with the full support of Mayor Lucius Rhyne", and the district was recognised as a **combat zone** "as it was easier to contain it than solving the problem" | `[wiki]` |
| 14 | **Walling off a district** | Council decision | The council "decided to wall-off Serenisands, giving the excuse of a gas leak"; Militech built the wall; the area became **Dogtown**, where "the NCPD is forbidden to enter" and only MaxTac may operate | `[wiki]` |
| 15 | **Treaty ambiguity over borders** | Mayor (Arvin Accord, 2070) | The Accord "did not end the war, but simply moved it elsewhere without designating clear winners or losers"; its "ambiguity of borders" makes Pacifica "a perfect location for everyone working in the shadows" | `[wiki]` |
| 16 | **Shutting off utilities and services** | City | "The city shut down all services in Pacifica", leaving the VDB and Barghest to find their own water, power and CitiNet; the Night City government also "fumigates the sewers regularly" | `[wiki]` |
| 17 | **Owning the utilities themselves** | Night Corp | NCART (metro, bought 2068); the maglev revival; power plants, net transmitters, waterworks and sewerage built and maintained under contract; the Jackson Plains solar farm; a share of the Northern Oil Fields | `[wiki]` |
| 18 | **Transit as a chokepoint** | Night Corp via NCART | NCART runs the metro and streetcars citywide; the Memorial Park Station is its "central hub"; the maglev is planned to reach Corporate Plaza in 2078 and Chicago by 2080 | `[wiki]` `[game-data]` |
| 19 | **Business licensing, vehicle registration, tenancy** | City departments | Department of Business Licencing; DMV; **Night City Landlord's Authority (NCLA)**; Records Office; Health Department; Environmental Task Force | `[wiki]` |
| 20 | **Port and harbour jurisdiction** | Port Authority / Harbor Police | The Harbormaster's Office handles shipping movements and facility assignment; the Harbor Police hold "jurisdiction over the whole surrounding sea and waterfronts" and are separate from the NCPD | `[wiki]` `[lore]` |
| 21 | **Criminal justice and detention** | DA, Hall of Justice, MaxTac | DA Georgina Zembinsky in 2077 (Peralez before her); cyberpsychos are transported to Los Padres Penitentiary; "any internal investigations are sure to be dropped" for MaxTac | `[wiki]` |
| 22 | **Election machinery** | City | Votes cast "via a Data Term using IdentiCard registration software", winner by simple majority; the council's 100 seats are "elected along pseudo-democratic lines by the then largest corporations headquartered in the city" | `[wiki]` |
| 23 | **Blackmail and kompromat** | Corporate donors against councillors | Eva Cole destroyed by leaked orgy footage after refusing to vote with lobbyists; Noorwood's murder suppressed because he was a Militech asset; McLean bought by Militech and killed for it | `[wiki]` |
| 24 | **Cover-up and control of police records** | Mayor's office via NCPD officers | Holt ordered Detective Harold Han to move Rhyne's body and report a heart attack; Han confirmed the false finding; the lethal braindance "went unnoticed" | `[wiki]` |
| 25 | **Patronage and the talent pipeline** | Night Corp | Night Foundation scholarships (Peralez and Elizabeth both, €$2.7m each); orphanage donations; charity for poor children; the 5th-best-employer ranking | `[wiki]` |
| 26 | **Behavioural conditioning** | Night Corp's covert wing | Carpe Noctem conditioned employees with an AI "designed to control not just their workers, but other figures Night Corp deemed useful"; Condin conditioned the mayoral candidate and his wife, causing memory loss | `[wiki]` |
| 27 | **Legal cover for private security** | Council / NCPD approval | Night Corp hires Lazarus and Militech SiteSecure; the police "hire mercenaries on the sly" outside corporate jurisdiction; the mayor's office considers replacing the NCPD with corporate security firms | `[wiki]` |

Reading the table: **the Government's levers are all legal-form levers** —
budget, appointment, statute, zoning, boundary, licence, title, treaty. It has
almost no physical lever. **Night Corp's levers are all service and
infrastructure levers** — transit, power, water, net, plus money for the police
and a covert conditioning capability. Neither body can take a block; both can
decide who is *allowed* to hold one. That division maps cleanly onto the
design's controller / title-holder split and is the strongest structural finding
in this document. `[inferred]`

---

## 5. Pillar notes

`gameplay-systems.md` does not give either body an archetype row — they are
"special political factions with no territory". The NCPD/MaxTac row (tentative
Paramilitary, strength Technology, weakness Politics) is the nearest design
anchor. These notes test the claims that *can* be tested and flag the ones that
cannot.

| Claim | Lore verdict | Evidence |
| --- | --- | --- |
| Night Corp is a **Corporation** (`category: megacorp`) | **True by category, misleading by behaviour.** It has no product line, no security force, no technology it sells, and no market presence. Its business is contracts and infrastructure. Modelled as a Corporation it will read as an unusually weak Arasaka. | `[wiki]` `[game-data]` |
| Night Corp's strength is **Politics**, not Technology | **Supported.** The corp's whole 2077 position is "a significant say in public administration", council-approved investment plans, and a Mayor it educated. Its Technology is real (maglev, AI) but it is not a technology *seller*. | `[wiki]` |
| Night Corp's weakness is **Military** | **Strongly supported.** It fields no garrison at all; every site it owns is guarded by a contractor (Lazarus, Militech SiteSecure); its "security" at the maglev site is six Militech drones and two Militech snipers, while its own employees are two generic workers. | `[wiki]` `[game-data]` |
| Night Corp's culture is weak / it is **secretive** | **Supported, and it is the corp's defining trait.** "Nobody really knows how much the corporation is worth, what its main source of revenue is, nor how many people it employs"; employees "knew only as much as they needed"; biometric floor separation. A faction that cannot be known cannot build soft power. | `[wiki]` |
| The Government is a **Politics** faction | **Overwhelmingly supported.** Every lever in §4 except #16 and #21 is a political or legal instrument. | `[wiki]` |
| The Government's weakness is **Military** | **Supported.** No forces of its own; the NCPD is privatised, underfunded and partly foreign-owned; Pacifica and Dogtown are lost; the Badlands are unpatrolled. | `[wiki]` |
| The Government's weakness is also **Economy** | **Supported, separately.** It taxes (badly — see the 99–1 exemption), spends contracted, and by 2077 is considering selling a district lot for €$1. Its own police was declared "not profitable enough" and privatised. | `[wiki]` |
| `income_multiplier 1.45` on a zero-footprint faction | **Unsupported by any extract data.** It is the highest multiplier in the megacorp group and Night Corp owns nothing to multiply. Held over from the location doc §8 item 14; repeated here because it affects both bodies' design weight. | `[game-data]` |
| `hostility_bias 0.25` and `0.2` | **Consistent with the lore.** Night Corp "avoid[ed] power struggles with other major corporations"; the council is a purchased majority that prefers not to fight. The two lowest biases in the civic/megacorp set are the two bodies that never field force. | `[game-data]` `[wiki]` |

Design cautions, not redesigns:

- **Do not model the Government as an owner.** It is a *title issuer*. Give it
  claims and it becomes the design's `title holder` for half the map; give it
  territory and the simulation contradicts Pacifica, Dogtown and the Badlands
  all at once. `[inferred]`
- **Do not model Night Corp as a landlord.** Its holdings are the tower (no
  interior), one metro station and three Badlands infrastructure sites. Its
  power is the contract, not the address. `[inferred]`
- **Both bodies need a face the game does not have.** The Board is unnamed and
  the council is 99 faceless votes. A political simulation that starts with
  these two factions starts with two institutions and roughly five usable
  people: Rhyne, Holt, Jefferson, Elizabeth, Cole. `[inferred]`

---

## 6. Gaps and uncertainties

1. **No named Night Corp CEO, ever, after Miriam.** The infobox `ceo` field is
   empty, the prose names no successor, and no shard, database entry or netpage
   supplies one. This is the largest hole in either body. A simulation needs a
   signatory the sources do not provide. `[wiki]`
2. **Night Corp has no affiliation value in the game at all.**
   `data/factions.json` gives `affiliation_enum: null`, and the full
   `gamedataAffiliation` enum has no Night Corp entry. It is not merely "no
   ganger roster"; the game cannot tag an NPC as Night Corp. Combined with
   `gameplay-systems.md` §1 ("places tied to Night Corp go to NCPD"), this means
   Night Corp can only exist in the mod as a **non-physical** faction. `[game-data]`
3. **The `city_council` faction footprint is three people.** All three
   `city_council` areas are Rhyne/Holt scenes: `{sq012_com_braindance}`
   (City Hall conference room), `{q005_com_flathead_room_b}` (Konpeki meeting
   room) and `{q303_com_paradise_quest_interactions}` (Black Sapphire, Dogtown).
   No councillor, city manager or department head exists as a spawned actor.
   `[game-data]`
4. **The City Manager offices' 2077 status is unverified.** The 2045 layer is
   fully documented (22 named managers, their powers, their corruption). Whether
   the office still exists in 2077 is not stated anywhere I found. It matters
   because zoning and licensing — two of the strongest levers in §4 — were
   manager functions, and the 2077 text attributes them to nobody in
   particular. `[wiki]`
5. **The `city_council` community counts are not a presence measure.** Two of
   the three areas are *scenes* (a braindance and a single meeting room), and
   the third is a party guest list. Do not read 5 entries as five councillors.
   `[game-data]`
6. **The seed puts the seat of government in gang turf.** City Hall's block
   (`gle_reconciliation_park`, sub-territory 43) is seeded to faction id **3 =
   Valentinos**; the Downtown block under Night Corp Tower
   (`dtn_corporation_st`) is seeded to faction id **2 = Tyger Claws**. Both are
   seed artefacts with no lore basis. Note also that
   [`../night-corp.md`](../night-corp.md) §5 describes
   `cc_dtn_corporation_st` as "seeded to Valentinos (`initial_owner_faction_id
   = 2`)"; id 2 is Tyger Claws, so that row's label is wrong although its id is
   right. `[game-data]`
7. **The City Hall anchor is a drone-tour community, not a building row.** The
   conference room's placement prefab
   (`#c_heywood/glen/loc_sq012_city_hall_conference_room_prefab…`) is solid
   evidence of identity and sub-district, but the only *position* records are a
   community area at `(-1781.910, -1010.925, 94.730)` (the conference room, 95 m
   up) and `{mq061_city_hall_drone_com}` at `(-1775.100, -933.140, 13.860)`
   (street level, 1 entry, no faction). The marker
   `mq061_04_sm_city_hall_scene` is **centroid-snapped** to
   `(-1317.810, -84.292, 0.000)` and is not evidence (METHOD §1.1 item 6). There
   is no `sites.json` row for City Hall. `[game-data]`
8. **Rhyne's and Holt's records are scene records, not world NPCs.** All six
   registry entries (`rhyne`, `holt`, `q005_lucius_rhyne`, `deputy_mayor`,
   `01_mayor_holt`, `holt` → `Character.sq012_weldon_holt_clue`) are quest
   phases. `Character.sq012_weldon_holt_clue` is a *clue* variant, not a second
   person. Do not spawn either as ambient. `[game-data]`
9. **The base 2077 state is ambiguous in this mod.** The wiki's 2077 is an
   election year: Rhyne dies in May, Holt is acting, Peralez wins. Rhyne's death
   and Peralez's election do *not* depend on the heist or on Phantom Liberty, so
   they survive `gameplay-systems.md` §7 — but the owner has not said whether the
   mod freezes politics before the election or accepts the result. **Do not pick
   silently.** Both states are recorded in §1.4. `[inferred]`
10. **Two levers in §4 are Phantom Liberty / 2079 material.** The Night Corp
    Complex seizure (#11) is dated 12/16/2078 and appears in *Things Done
    Changed*, which is downstream of the Space Force One chain the alternate
    timeline deletes. Treat #11 as evidence that the *lever* exists (council
    approves investment plans; a corp can then seize property with legal
    backing), not as a 2077 event. `[wiki]`
11. **The Konpeki meeting is a heist-day scene.** `{q005_com_flathead_room_b}`
    exists to put V's Flathead drone in the room. The *meeting* (mayor, deputy
    mayor, Arasaka reps, Watson low-income housing) is attested lore, but its
    only game record is gated by `q005` — the quest the alternate timeline
    removes. Lever #8 survives on the wiki; the *coordinate* is
    timeline-dependent. `[game-data]` `[wiki]`
12. **SSI→Night Corp is inferred, not proven.** *Dream On* never names Night
    Corp. The wiki says the link "is implied by Sandra Dorsett's quest" and
    "backed up by references in the 2077 world book." Any stance that depends on
    it (`maelstrom` `trade`, the conditioning wing in §2.1) is two inferences
    deep. `[wiki]` `[inferred]`
13. **`voodoo_boys` disagrees with the Voodoo Boys doc.** That doc calls the
    Night Corp relation `neutral` ("no attested interaction; a corporation, not
    a Pacifica turf actor"). This doc says `rival`, because the location doc
    establishes that the VDB hold Night Corp's *de jure* Old Maglev Tunnel. I
    think `rival` is right and the VDB doc missed the location doc's finding;
    flagging rather than silently diverging. `[game-data]` `[wiki]`
14. **Night Corp's per-faction stances are 19/29 neutral.** With no roster
    presence there is simply no co-presence evidence. Do not treat this matrix
    as a political map of the corp; it is a list of the four transactions the
    corp is attested to have made (Militech, Petrochem, Aldecaldos, Maelstrom)
    plus two patrons and three rivals. `[inferred]`
15. **No `ally` row in either body's direction.** For the government this is a
    substantive finding — a body whose every relationship is purchased has no
    friends. For Night Corp it is partly a data limit. Do not read the absence
    as neutrality-with-goodwill. `[inferred]`
16. **Jerry Fawlter is double-counted by design.** He is the mayor's appointee
    (Government lever #2) and the NCPD's commissioner (the NCPD doc's leader).
    Listed in both; only one should carry his spawning. `[wiki]`
17. **`Emilio Gutierrez` is cut content.** The election shard is tagged
    `{{CutContent}}` and the quest it points at (*Until Death Do Us Part*) is a
    different gig. Do not treat him as a 2077 candidate. `[wiki]`
18. **The `mq061_06` Richard Night records are spawnpoints, not a character.**
    Eleven `mq061_06_Spawnpoint_Richard_Night_*` markers plus
    `mq061_06_Marker_Mappin_*` exist at `(110–141, -1170…-1191, 13–32)`; there is
    no `Character.Richard_Night` record anywhere in the extract. It is a
    hologram staging area. `[game-data]`
19. **`SSI` is a first-class affiliation in the engine, and it is NOT used.**
    `refs/cyberpunk/orphans.swift` `gamedataAffiliation` has `SSI = 21`,
    between `RecordingAgency = 20` and `Scavengers = 22`; the enum declares
    46 names (indexes 0–45, with `Count = 44` a sentinel and `Invalid = 45`).
    No roster entry, community entry or `Character.*` record uses it, and no
    `ssi`-prefixed character record exists. So the engine can tag SSI personnel
    but the shipped content does not — the Condin actors are spawned as generic
    security. This is the one place where the game's own enum is *stronger*
    evidence for a political bloc than its content is. `[game-data]`
20. **`night_corp` has no enum value at all, which is a different failure from
    SSI.** `SSI = 21` exists and is unused; Night Corp has no value in the
    enum. That asymmetry means "the game has no Night Corp
    affiliation" (§1, and `gameplay-systems.md` §1) is exact, not shorthand, and
    it is why the design routes Night Corp places to `ncpd`. `[game-data]`

### Sources consulted

Local:

- `data/factions.json` — `night_corp` (fid 40, `affiliation_enum: null`,
  `income_multiplier 1.45`, `hostility_bias 0.25`) and `city_council` (fid 51,
  `income_multiplier 1.2`, `hostility_bias 0.2`).
- `dist/extract/areas.jsonl` — the three `city_council` areas
  (`{sq012_com_braindance}`, `{q005_com_flathead_room_b}`,
  `{q303_com_paradise_quest_interactions}`) and zero `night_corp` areas.
- `dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_{0,1,2}.streamingsector.json`
  — the community registry entries and `characterRecordId` values for
  `Character.sq012_lucius_rhyne`, `Character.sq012_weldon_holt`,
  `Character.sq012_weldon_holt_clue`, `Character.Jefferson_Peralez`,
  `Character.Elizabeth_Peralez`, `Character.mq024_sandra_combatable`; the
  `loc_sq012_city_hall_conference_room` placement prefab; the
  `static_city_hall_crowd_*` / `nightcorp` decoy checks.
- `dist/extract/markers.jsonl` — `sq012_02a_sm_braindance`,
  `sq012_08a_sm_peralez_apartment`, `sq012_mappin_peralez_apartment_outer_door`,
  `sq012_mappin_enter_RQR`, `sq012_06b_sm_rqr_investigation`,
  `sq012_06a_sm_rqr_ext`, `sq006_07a_sm_final_choice`,
  `sq006_04a_sm_secret_lab`, `sq006_04a_sm_secret_lab_van`,
  `elizabeth_sm_peralez_default` (rejected: prefab-local `(8.590, 1.050,
  0.760)`),
  `mq061_06_Spawnpoint_Richard_Night_*`, the centroid-snapped
  `mq061_04_sm_city_hall_scene`.
- `data/sites/sites.json`, `data/sites/rosters.json` — 0 Night Corp sites and 0
  roster units; 0 named mayor/councillor records.
- `data/sub_territories.json`, `data/control_centers.json` — CC owners and
  distances; the seeded owners of `gle_reconciliation_park` (id 3) and
  `dtn_corporation_st` (id 2).
- `docs/design/gameplay-systems.md` §1 (special factions), §4 (titles/claims),
  §7 (alternate timeline).
- `docs/research/factions/night-corp.md` — the location catalogue, §5 trade-offs
  and §8 gaps.
- `docs/research/factions/politics/METHOD.md`; `../METHOD.md` §1.1–§1.2.

Wiki (MediaWiki API, wikitext only):

- [Government of Night City](https://cyberpunk.fandom.com/wiki/Government_of_Night_City) ·
  [Night City Hall](https://cyberpunk.fandom.com/wiki/Night_City_Hall) ·
  [Night City Hall (City Center)](https://cyberpunk.fandom.com/wiki/Night_City_Hall_(City_Center))
- [Lucius Rhyne](https://cyberpunk.fandom.com/wiki/Lucius_Rhyne) ·
  [Weldon Holt](https://cyberpunk.fandom.com/wiki/Weldon_Holt) ·
  [Mbole Ebunike](https://cyberpunk.fandom.com/wiki/Mbole_Ebunike) ·
  [Garven Haakensen](https://cyberpunk.fandom.com/wiki/Garven_Haakensen)
- [Jefferson Peralez](https://cyberpunk.fandom.com/wiki/Jefferson_Peralez) ·
  [Elizabeth Peralez](https://cyberpunk.fandom.com/wiki/Elizabeth_Peralez) ·
  [Eva Cole](https://cyberpunk.fandom.com/wiki/Eva_Cole) ·
  [John McLean](https://cyberpunk.fandom.com/wiki/John_McLean) ·
  [Jack Lars](https://cyberpunk.fandom.com/wiki/Jack_Lars)
- [Devolutionist Party](https://cyberpunk.fandom.com/wiki/Devolutionist_Party) ·
  [Federalist Party](https://cyberpunk.fandom.com/wiki/Federalist_Party)
- [Dream On](https://cyberpunk.fandom.com/wiki/Dream_On) ·
  [I Fought the Law](https://cyberpunk.fandom.com/wiki/I_Fought_the_Law) ·
  [Secure Services Inc.](https://cyberpunk.fandom.com/wiki/Secure_Services_Inc.) ·
  [Mr. Blue Eyes](https://cyberpunk.fandom.com/wiki/Mr._Blue_Eyes) ·
  [PROJECT CONDIN SUSPENDED](https://cyberpunk.fandom.com/wiki/PROJECT_CONDIN_SUSPENDED)
- [Gig: Serial Suicide](https://cyberpunk.fandom.com/wiki/Gig:_Serial_Suicide) ·
  [Gig: The Frolics of Councilwoman Cole](https://cyberpunk.fandom.com/wiki/Gig:_The_Frolics_of_Councilwoman_Cole) ·
  [Gig: MIA](https://cyberpunk.fandom.com/wiki/Gig:_MIA) ·
  [Gig: Freedom of the Press](https://cyberpunk.fandom.com/wiki/Gig:_Freedom_of_the_Press) ·
  [Gig: Until Death Do Us Part](https://cyberpunk.fandom.com/wiki/Gig:_Until_Death_Do_Us_Part)
- [Night Corp](https://cyberpunk.fandom.com/wiki/Night_Corp) ·
  [Night Corp Headquarters](https://cyberpunk.fandom.com/wiki/Night_Corp_Headquarters) ·
  [Night Corp/Netpage](https://cyberpunk.fandom.com/wiki/Night_Corp/Netpage) ·
  [Richard Night](https://cyberpunk.fandom.com/wiki/Richard_Night) ·
  [Miriam Night](https://cyberpunk.fandom.com/wiki/Miriam_Night) ·
  [Sandra Dorsett](https://cyberpunk.fandom.com/wiki/Sandra_Dorsett) ·
  [Full Disclosure](https://cyberpunk.fandom.com/wiki/Full_Disclosure) ·
  [Big 5 Employers in Night City – 2077](https://cyberpunk.fandom.com/wiki/Big_5_Employers_in_Night_City_%E2%80%93_2077)
- [Night City Police Department](https://cyberpunk.fandom.com/wiki/Night_City_Police_Department) ·
  [MaxTac](https://cyberpunk.fandom.com/wiki/MaxTac) ·
  [Night City Port Authority](https://cyberpunk.fandom.com/wiki/Night_City_Port_Authority) ·
  [Night City Transit Corporation](https://cyberpunk.fandom.com/wiki/Night_City_Transit_Corporation)
- [Pacifica (2077)](https://cyberpunk.fandom.com/wiki/Pacifica_(2077)) ·
  [Dogtown](https://cyberpunk.fandom.com/wiki/Dogtown) ·
  [Arvin Accord Redefined?](https://cyberpunk.fandom.com/wiki/Arvin_Accord_Redefined%3F) ·
  [Avian Extermination Act](https://cyberpunk.fandom.com/wiki/Avian_Extermination_Act) ·
  [Birth of a Free City](https://cyberpunk.fandom.com/wiki/Birth_of_a_Free_City) ·
  [Night City – A New Era](https://cyberpunk.fandom.com/wiki/Night_City_%E2%80%93_A_New_Era)
- [Konpeki Plaza](https://cyberpunk.fandom.com/wiki/Konpeki_Plaza) ·
  [Black Sapphire](https://cyberpunk.fandom.com/wiki/Black_Sapphire) ·
  [You Know My Name](https://cyberpunk.fandom.com/wiki/You_Know_My_Name) ·
  [Things Done Changed](https://cyberpunk.fandom.com/wiki/Things_Done_Changed) ·
  [Night Corporation Construction Site: Access Strictly Prohibited](https://cyberpunk.fandom.com/wiki/Night_Corporation_Construction_Site:_Access_Strictly_Prohibited)
- [Night City Co-Prosperity Sphere](https://cyberpunk.fandom.com/wiki/Night_City_Co-Prosperity_Sphere) ·
  [Orbital Air](https://cyberpunk.fandom.com/wiki/Orbital_Air) ·
  [Petrochem](https://cyberpunk.fandom.com/wiki/Petrochem) ·
  [Aldecaldos](https://cyberpunk.fandom.com/wiki/Aldecaldos) ·
  [Voodoo Boys](https://cyberpunk.fandom.com/wiki/Voodoo_Boys)

Earlier repo research:

- [`./arasaka.md`](./arasaka.md) — corp politics format and the `patron`/`client`
  direction problem (§5 item 20).
- [`./militech.md`](./militech.md) — `night_corp trade` and `city_council trade`
  rows, symmetric with §3.2.
- [`./voodoo-boys.md`](./voodoo-boys.md) — `night_corp neutral`, diverging; see
  §6 item 13.
- [`./barghest.md`](./barghest.md) — Dogtown as a territory-holding faction.
- [`../night-corp.md`](../night-corp.md) — the location catalogue.

---

## 7. Machine-readable block

Strict JSON (contract in [`METHOD.md`](./METHOD.md) §6). `faction_code` is
`night_corp`; the Government's leaders are in the same `leaders` array with
`role` naming the body. `character_record_id` is `null` where no record exists;
`presence_class` and `open_world` follow §1; `relations` are read from Night
Corp's side, with the Government's differing stances in §3.3.

```json
{
  "faction_code": "night_corp",
  "leaders": [
    {
      "name": "Richard Night",
      "role": "Night Corp - founder of Night International (early 1990s) and of Coronado City; murdered 20 Sep 1998 at Parkview Tower",
      "character_record_id": null,
      "location_name": "Night Corp Tower, Downtown / Parkview Tower (death site) / mq061_06 holotour stop",
      "presence_class": "historical",
      "open_world": false,
      "source": "wiki Richard Night; wiki Night Corp; raw always_loaded_1 registry mq061_06_Spawnpoint_Richard_Night_* (hologram staging only, no Character record)",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Miriam Night",
      "role": "Night Corp - Richard's widow; founder of Night's Foundation (1999); CEO of Night Corp; stepped down before 2077; status Unknown",
      "character_record_id": null,
      "location_name": null,
      "presence_class": "historical",
      "open_world": false,
      "source": "wiki Miriam Night; wiki Night Corp",
      "confidence": "wiki"
    },
    {
      "name": "The Night Corp Board",
      "role": "Night Corp - collective sovereign; unnamed seats; approves investment plans; no individual is ever named",
      "character_record_id": null,
      "location_name": "Night Corp Tower, Downtown",
      "presence_class": "mentioned",
      "open_world": false,
      "source": "shard Night Corporation Construction Site: Access Strictly Prohibited (the Company's Board); wiki Night Corp (the corporation's rather mysterious structure); wiki Night Corp Headquarters database entry (biometric access separating teams by floor)",
      "confidence": "wiki"
    },
    {
      "name": "Sandra Dorsett",
      "role": "Night Corp - corporate netrunner; stole the Operation Carpe Noctem databank; the only named living Night Corp employee",
      "character_record_id": "Character.mq024_sandra_combatable",
      "location_name": "Sandra Dorsett's Apartment, Little China (Watson)",
      "presence_class": "world-activity",
      "open_world": false,
      "source": "raw always_loaded_1 registry (entry names sandra, sandra_holo, sandra_dorset__q000__sandra_dorset); minor job Full Disclosure (baseid mq024_sandra); wiki Sandra Dorsett",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Lucius Rhyne",
      "role": "Government - Mayor of Night City 2070-2077; councilman 2060-2070 (Devolutionist); Watson City Manager 2045; killed May 2077 at the Red Queen's Race",
      "character_record_id": "Character.sq012_lucius_rhyne",
      "location_name": "City Hall (Glen) / Konpeki Plaza meeting room (ArasakaWaterfront) / Red Queen's Race (CharterHill)",
      "presence_class": "story",
      "open_world": false,
      "source": "raw always_loaded_0 and _2 registry (entries q005_lucius_rhyne, rhyne); areas {sq012_com_braindance} (-1781.910,-1010.925,94.730) and {q005_com_flathead_room_b} (-2183.046,1795.546,162.993); wiki Lucius Rhyne",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Weldon Holt",
      "role": "Government - Deputy Mayor 2070-2077; Acting Mayor 2077; Devolutionist; in Arasaka's pocket per Max Jones; covered up Rhyne's death",
      "character_record_id": "Character.sq012_weldon_holt",
      "location_name": "City Hall conference room / Konpeki Plaza meeting room / Black Sapphire gala (Dogtown)",
      "presence_class": "story",
      "open_world": false,
      "source": "raw registry (entries deputy_mayor, 01_mayor_holt; clue variant Character.sq012_weldon_holt_clue, entry holt); areas {sq012_com_braindance}, {q005_com_flathead_room_b}, {q303_com_paradise_quest_interactions} (-1922.437,-2314.250,439.766); wiki Weldon Holt",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Jefferson Peralez",
      "role": "Government - Councilman 2076-2077; DA before that; Federalist; Mayor of Night City 2077- (still mayor in 2079); under Condin conditioning",
      "character_record_id": "Character.Jefferson_Peralez",
      "location_name": "Peralezes' Apartment, Charter Hill (Westbrook) / City Hall (Glen) / Reconciliation Park (Glen)",
      "presence_class": "story",
      "open_world": false,
      "source": "raw registry (entry jefferson_holo -> Character.Jefferson_Peralez); markers sq012_08a_sm_peralez_apartment (-78.170,-117.440,111.159), sq006_07a_sm_final_choice (-1694.890,-190.238,13.494); wiki Jefferson Peralez",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Elizabeth Peralez",
      "role": "Government - lawyer and campaign principal; Federalist; the operation behind Jefferson's candidacy",
      "character_record_id": "Character.Elizabeth_Peralez",
      "location_name": "Peralezes' Apartment, Charter Hill (Westbrook) / Yagami Market ramen shop (JapanTown)",
      "presence_class": "story",
      "open_world": false,
      "source": "raw registry (Character.Elizabeth_Peralez, Character.sq006_elizabeth_intercom); wiki Elizabeth Peralez. No world coordinate: elizabeth_sm_peralez_default is prefab-local (8.590,1.050,0.760)",
      "confidence": "game-data+wiki"
    },
    {
      "name": "Mbole Ebunike",
      "role": "Government - Mayor of Night City 2012-2023 (born Judson Freeman); corporate puppet who turned hostile; stepped down under Arasaka pressure",
      "character_record_id": null,
      "location_name": "Night City Hall (City Center, 2020 building)",
      "presence_class": "historical",
      "open_world": false,
      "source": "wiki Mbole Ebunike; wiki Night City Hall (City Center)",
      "confidence": "wiki+lore"
    },
    {
      "name": "Garven Haakensen",
      "role": "Government - Deputy/Acting Mayor 2023; fled after the AHQ Disaster; later City Manager of South Night City and the council's deal-maker",
      "character_record_id": null,
      "location_name": "Haakensen Tower (South Night City) / City Hall",
      "presence_class": "historical",
      "open_world": false,
      "source": "wiki Garven Haakensen",
      "confidence": "wiki+lore"
    },
    {
      "name": "Brad Noorwood",
      "role": "Government - City Council member; a Militech fanboy; murdered over an unpublished article",
      "character_record_id": null,
      "location_name": "NCART Memorial Park Station (CorpoPlaza) - the gig site",
      "presence_class": "world-activity",
      "open_world": false,
      "source": "gig Serial Suicide (baseid sts_cct_cpz_01) journal entry, quest giver Dino Dinovic; wiki Government of Night City; wiki page does not exist",
      "confidence": "wiki+game-data"
    },
    {
      "name": "Eva Cole",
      "role": "Government - City Council member; anti-corruption; career destroyed by leaked blackmail footage",
      "character_record_id": null,
      "location_name": "Cannery Row marina, her yacht (Downtown, CityCenter)",
      "presence_class": "world-activity",
      "open_world": false,
      "source": "gig The Frolics of Councilwoman Cole (baseid sts_cct_dtn_05); radio news line quoted on wiki Eva Cole",
      "confidence": "wiki+game-data"
    },
    {
      "name": "John McLean",
      "role": "Government - City Council member; bought by Militech; assassinated by Benedict McAdams on Dakota Smith's contract",
      "character_record_id": null,
      "location_name": null,
      "presence_class": "mentioned",
      "open_world": false,
      "source": "shard Archived Conversation: Dakota; gig MIA (baseid sts_bls_ina_09); wiki John McLean (body text spells McLane; the gig spells McClean)",
      "confidence": "wiki"
    },
    {
      "name": "Jack Lars",
      "role": "Government - City Council member and Night City Director of Urban Planning; close Militech ties (comic only)",
      "character_record_id": null,
      "location_name": "Wellsprings apartment (Heywood)",
      "presence_class": "off-map",
      "open_world": false,
      "source": "wiki Jack Lars, citing Cyberpunk 2077: You Have My Word",
      "confidence": "wiki+lore"
    },
    {
      "name": "Emilio Gutierrez",
      "role": "Government - City Council candidate; sanitation budget record; cut content",
      "character_record_id": null,
      "location_name": null,
      "presence_class": "mentioned",
      "open_world": false,
      "source": "cut shard Night City Council elections! Vote for Emilio Gutierrez! (baseid sts_wbr_hil_01_shard_001, tagged CutContent)",
      "confidence": "wiki"
    },
    {
      "name": "Georgina Zembinsky",
      "role": "Government - District Attorney of Night City, 2077",
      "character_record_id": null,
      "location_name": "Hall of Justice, the Glen",
      "presence_class": "mentioned",
      "open_world": false,
      "source": "wiki Government of Night City",
      "confidence": "wiki"
    },
    {
      "name": "Jerry Fawlter",
      "role": "Government - NCPD Commissioner from 2076, appointed by the Mayor's Office; former dataterm sales executive; fired half the force",
      "character_record_id": null,
      "location_name": "NCPD Headquarters",
      "presence_class": "mentioned",
      "open_world": false,
      "source": "wiki Night City Police Department (Leadership); wiki NCPD - Anatomy of a Disaster",
      "confidence": "wiki"
    },
    {
      "name": "The City Council (100 seats)",
      "role": "Government - collective legislature; 100 members, each usually backed by one of the top ten corporations in the city; voted 99-1 for the City of Opportunity tax exemption",
      "character_record_id": null,
      "location_name": "City Hall, the Glen (Heywood)",
      "presence_class": "mentioned",
      "open_world": false,
      "source": "wiki Government of Night City (structure, 100 seats); wiki Jefferson Peralez (99-1 vote, 32 corporations exempted)",
      "confidence": "wiki"
    }
  ],
  "internal_factions": [
    {
      "name": "The founder's-vision wing (the faithful)",
      "leader": null,
      "goals": "Restore Night Corp to a position of true power; keep Richard Night's civic mission; public works and public administration over profit",
      "members_hint": "Unquantified. The corp's own netpage sells this line; the database entry notes those in the mysterious structure who have not lost faith in the founder's vision, and residents who wish the corp would return to power",
      "source": "wiki Night Corp database entry; wiki Night Corp/Netpage",
      "confidence": "wiki"
    },
    {
      "name": "The incumbent executive tier",
      "leader": null,
      "goals": "Manage shrinking capital; preserve the public-administration say; avoid power struggles with Arasaka and Militech",
      "members_hint": "The Board and Tower staff; biometric floor separation; employees know only what their job requires",
      "source": "wiki Night Corp (much less competent figures); wiki Night Corp Headquarters database entry",
      "confidence": "wiki"
    },
    {
      "name": "NCART (subsidiary)",
      "leader": null,
      "goals": "Run the metro and streetcars; deliver the maglev revival (first links 2078, Chicago 2080); keep City Pass revenue",
      "members_hint": "5 lines, 19 stations; bought out 2068 after poison-gas attacks bankrupted the transit corporation; the corp's only wholly owned operational asset",
      "source": "wiki Night Corp; wiki Night City Area Rapid Transit; docs/research/factions/night-corp.md section 3 item 2",
      "confidence": "wiki+game-data"
    },
    {
      "name": "The covert conditioning wing (Carpe Noctem / Condin)",
      "leader": "Sandra Dorsett's unnamed supervisor; SSI Chief of Security Wallace (operations)",
      "goals": "Condition employees, then officials, into compliant behaviour; mold the ideal mayoral candidate; keep the operation invisible and delete its own data",
      "members_hint": "Carpe Noctem databank and AI; SSI ORANGE/BLUE/BLACK teams; Sector Zero; the roof transmitter; the mobile data-centre van; the Maelstrom escort",
      "source": "wiki Night Corp (AI conditioning); wiki Secure Services Inc. (Condin, target ALPHA); wiki Dream On; shard PROJECT CONDIN SUSPENDED",
      "confidence": "wiki+game-data+inferred"
    },
    {
      "name": "Devolutionist Party (city branch)",
      "leader": "Lucius Rhyne (to 2077), then Weldon Holt",
      "goals": "Night City autonomy inside a devolved NUSA; corporate freedom; Arasaka as the city's guarantor",
      "members_hint": "The Mayor's Office; Rhyne's and Holt's council seats; the 2070 war cabinet",
      "source": "wiki Lucius Rhyne (Devolutionist affiliation); wiki Devolutionist Party; wiki Weldon Holt",
      "confidence": "wiki"
    },
    {
      "name": "Federalist Party (city branch)",
      "leader": "Jefferson Peralez",
      "goals": "Federal alignment; anti-corporate populism; reverse the tax exemptions; shift protection from corporate security to public police",
      "members_hint": "Peralez's council seat and mayoral campaign; Elizabeth Peralez; union networks; 6th Street-linked supporters",
      "source": "wiki Jefferson Peralez; wiki Federalist Party; wiki Elizabeth Peralez",
      "confidence": "wiki"
    },
    {
      "name": "The corp-bought council bloc",
      "leader": null,
      "goals": "Pass pro-corporate measures; protect tax exemptions; keep corporate crimes out of police jurisdiction; protect patrons",
      "members_hint": "99 of 100 seats on the City of Opportunity vote; Brad Noorwood and John McLean (Militech); Jack Lars (Militech, comic); an unnamed councillor pressured by Arasaka over a Japantown building",
      "source": "wiki Jefferson Peralez (99-1); gigs Serial Suicide, MIA, Frolics of Councilwoman Cole; wiki Government of Night City (Arasaka pressure); wiki Jack Lars",
      "confidence": "game-data+wiki"
    },
    {
      "name": "The reform bloc",
      "leader": "Eva Cole",
      "goals": "Crack down on corporate corruption; refuse bribes; investigate; hold the police accountable",
      "members_hint": "Cole alone after Peralez leaves the council for the mayoralty; Peralez's lone dissenting vote is the bloc's high-water mark",
      "source": "wiki Eva Cole; wiki Jefferson Peralez",
      "confidence": "wiki"
    },
    {
      "name": "The City Manager layer (2040s)",
      "leader": null,
      "goals": "District control of zoning, licensing, police licensing and construction contracts; personal enrichment",
      "members_hint": "22 named 2040s district managers including Rhyne (Watson), Freeman (the Glen), Haakensen (South Night City); Haakensen's tenure is the fully documented case. 2077 status unverified",
      "source": "wiki Government of Night City (2045 City Managers list); wiki Garven Haakensen",
      "confidence": "wiki+lore"
    },
    {
      "name": "The Peralez conspiracy (SSI / Condin / Mr. Blue Eyes)",
      "leader": "Mr. Blue Eyes (unidentified proxy); SSI Chief of Security Wallace",
      "goals": "Install a conditioned mayor; keep the operation invisible; delete its own data; deter investigators",
      "members_hint": "SSI ORANGE/BLUE/BLACK teams; Security Officer West; agents BLUE-66M/87G/89H/03A; the mobile data centre; a Maelstrom escort led by Dante",
      "source": "wiki Dream On; wiki Secure Services Inc.; wiki Mr. Blue Eyes; shard PROJECT CONDIN SUSPENDED",
      "confidence": "game-data+wiki"
    }
  ],
  "relations": [
    {
      "faction_code": "tyger_claws",
      "stance": "neutral",
      "evidence": "No attested interaction. Spatial and seeded only: cc_dtn_corporation_st (143 m from Night Corp Tower) is seeded to faction id 2 = Tyger Claws, and ma_cct_dtn_07 (92 m) is a Tyger Claws site, so the corp's own street is seeded to the Claws. A seed conflict, not a relationship [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "valentinos",
      "stance": "neutral",
      "evidence": "No attested interaction. Adjacent only through the seed: the Glen blocks around City Hall (gle_reconciliation_park, gle_ventura_skyline) are seeded to faction id 3 = Valentinos, so the seat of government sits in Valentinos-seeded turf [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "arasaka",
      "stance": "rival",
      "evidence": "Night Corp lost the race for Night City influence to Arasaka and Militech, both of which came to wield the most power in the city; Arasaka was given a council seat by Rhyne in 2070 and Arasaka reps pressure councillors directly. Arasaka Tower is 374 m from Night Corp Tower [wiki] [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "militech",
      "stance": "trade",
      "evidence": "Night Corp hires Militech: Militech SiteSecure guards the maglev construction site and the six-droid garrison at {q114_com_construction_nc_security} is Militech; Militech also took over security at NCART Memorial Park Station after Zoli Barnes' death. Direction: Night Corp is the buyer. Commercial contract inside a rivalry [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "kang_tao",
      "stance": "neutral",
      "evidence": "No attested interaction with Night Corp. Kang Tao's city-facing play is the Pacifica server lot, negotiated with the council, not the corp [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "biotechnica",
      "stance": "neutral",
      "evidence": "No attested interaction. Biotechnica sat on the 2045 council junta alongside Night Corp's city, not with the corp [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "petrochem",
      "stance": "trade",
      "evidence": "The Northern Oil Fields are a joint project of Petrochem and Night Corp, and Night Corp brokered the Petrochem-SovOil peace over those fields after the Fourth Corporate War. A commercial joint venture between otherwise separate houses [wiki] [game-data]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "barghest",
      "stance": "neutral",
      "evidence": "No attested interaction. Dogtown is outside city administration and outside Night Corp's contracts; the wall that created Dogtown was a council decision [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "sixth_street",
      "stance": "neutral",
      "evidence": "No attested interaction with Night Corp. 6th Street's city-politics role is election dirty work for Peralez and Holt, i.e. government-facing [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "aldecaldos",
      "stance": "trade",
      "evidence": "Night Corp was a major reason the nomads came to Night City to help, offering generous pay and free cyberware and biomonitor upgrades to anyone willing to clean the radioactive crater; the cleanup crews were especially Aldecaldos. A paid one-off labour contract [wiki]",
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
      "evidence": "No attested interaction with Night Corp. Animals' documented city-politics role is Holt hiring them to wreck the Red Queen's Race, i.e. government-facing; they hire out as bodyguards but no Night Corp contract is attested [wiki] [inferred]",
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
      "stance": "trade",
      "evidence": "A deniable one-off hire: SSI's BLACK team drove its data-centre van into a Maelstrom compound near All Foods, and a Maelstrom goon named Dante led the ambush that covered their tracks (email title: Need your boys' help like last time). SSI -> Night Corp is [inferred], so this is two links deep [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "voodoo_boys",
      "stance": "rival",
      "evidence": "A property dispute, not a war: the Old Maglev Tunnel is Night Corp's de jure and the Voodoo Boys hold it as a data fortress de facto; gamedataDistrict.Coastview_VDBMaglev = 40 names the place for its occupier. No violent event is attested between corp and gang [game-data] [wiki]. Note: the Voodoo Boys doc records this as neutral",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "ncpd",
      "stance": "patron",
      "evidence": "Night Corp funds the police: the NCPD is partly financed by Night Corp's shrinking coffers and both NCPD and MaxTac are named as its beneficiaries; the NCPD database entry says the force's official sponsor is Night Corp. Direction: Night Corp pays, NCPD receives. Also the design's fallback assigns Night Corp places to NCPD [wiki] [game-data]",
      "confidence": "wiki+game-data"
    },
    {
      "faction_code": "scavengers",
      "stance": "hostile",
      "evidence": "Scavengers kidnapped Night Corp netrunner Sandra Dorsett and her Carpe Noctem databank, and Night Corp's covert data recovery runs through a Scav-infested building. The corp's data is a standing target of the scav trade [game-data] [wiki]",
      "confidence": "game-data+wiki"
    },
    {
      "faction_code": "city_council",
      "stance": "patron",
      "evidence": "Night Corp has a significant say in public administration, funds the scholarships that produced the mayor, and in 2078 obtained a council-approved investment plan for its Complex while seizing market stalls under threat of prosecution. Direction: Night Corp funds and cultivates councillors; the council returns approvals [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "afterlife",
      "stance": "neutral",
      "evidence": "No attested interaction; a merc marketplace, not a political actor [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_regina",
      "stance": "neutral",
      "evidence": "No Night Corp-specific gig. Regina's city-politics gig Freedom of the Press protects a muckraker who says Holt is in Arasaka's pocket, i.e. government-facing [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "fixer_wakako",
      "stance": "neutral",
      "evidence": "Indirect only: Wakako brokers the return of Night Corp's stolen Carpe Noctem databank to Sandra Dorsett, who intends to use it to fight against Night Corp. The channel works against the corp; no direct corporate relationship is attested [wiki]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "fixer_padre",
      "stance": "neutral",
      "evidence": "No Night Corp-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_el_capitan",
      "stance": "neutral",
      "evidence": "No Night Corp-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_dakota",
      "stance": "neutral",
      "evidence": "No Night Corp contact. Dakota commissions the assassination of a Militech-bought councillor, i.e. government-facing [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "fixer_dino",
      "stance": "neutral",
      "evidence": "Dino runs both council gigs (Serial Suicide, The Frolics of Councilwoman Cole) and profits from corpo contracts in Downtown, i.e. government-facing and transactional even then [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "fixer_rogue",
      "stance": "neutral",
      "evidence": "No Night Corp-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_mr_hands",
      "stance": "neutral",
      "evidence": "No Night Corp-specific gig or lore link found [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "orbital_air",
      "stance": "rival",
      "evidence": "Night Corp cut all ties with Orbital Air, starting a sort of cold war, after OA abandoned the mass driver and built the NCX Spaceport instead; residents speculate Night Corp will try to push OA out of the city. An attested corporate feud, not a turf war [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "nusa",
      "stance": "neutral",
      "evidence": "No attested corporate interaction. The NUSA is the government's adversary (2070 invasion, Arvin Accord) and Night Corp's business is the free city's infrastructure, but no source has the corp taking a side [wiki] [inferred]",
      "confidence": "wiki+inferred"
    }
  ]
}
```
