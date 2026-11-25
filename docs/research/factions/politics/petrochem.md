# Petrochem — Leadership, Internal Politics and External Relations

Status: faction politics research run, 2026-11-25. One faction, one document.
Scope: Cyberpunk 2077 2.5 + Phantom Liberty, campaign disabled. Who a player can
join under, climb past, ally with or remove inside Petrochem; the corporate
blocs; and the external-relations matrix needed for wars, alliances and
"guarantor" support when a player founds an organisation.

Method: this document follows the evidence rules in
[`METHOD.md`](./METHOD.md), including the §1.1–§1.3 corrections, and the data
pitfalls in [`../METHOD.md`](../METHOD.md) §1.1–§1.2. The location catalogue for
Petrochem is [`../petrochem.md`](../petrochem.md); this document maps people and
politics onto those places and does not repeat the coordinates. `AGENTS.md` was
read first. No commits, no game launch; helper scripts ran outside the repo
under `python3 -I`.

**Read this first, because it shapes every section:** Petrochem is the emptiest
faction in the extract. The 2.5 build contains **zero** Petrochem roster units,
**zero** community areas, **zero** spawn points, **zero** faction-owned sites,
and **no `gamedataAffiliation` value**. There is no Petrochem guard, drone,
office worker or executive anywhere in the game. No current Petrochem person
has a character record. Every name below is `[wiki]` or `[lore]`; every leader's
presence class is `off-map`, `mentioned` or `historical`. **No Petrochem leader
is open-world, and the mod must supply all of them.** The one named person with
a record is a former executive who is now a fixer.

Evidence tags used throughout:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Position, site, community, roster or raw-registry record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page, shard or in-game computer message (cited inline) | Secondary, high |
| `[lore]` | Book/comic/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | My reasoning links a named person, place or stance to a record; reasoning stated | Weak, flagged |

Extra convention for this document only: **presence class**.
`off-map` = alive and named in 2077 but never spawned (the CEO, the board);
`mentioned` = named only in a shard, computer message or broadcast; `story` =
gated by a main or side job; `historical` = no 2077 record. No Petrochem leader
is `ambient` or `world-activity`: **there is no Petrochem NPC to be ambient.**
The JSON `open_world` flag is `false` for every leader.

A corporation is not a gang, and Petrochem is not even a normal corporation in
the game. Three adjustments are used throughout and are flagged again in §5:

- **Leadership is an ownership chart, not a leader list.** The Parker family,
  the Trieste–Youngblood shareholding, the board and the CEO are all
  "leadership"; only the last two are jobs. The 2077 names are a CEO and a
  board, not a cast.
- **The best wiki source is the employee list, and it is four lines long.**
  `List of Petrochem employees` gives one 2077 CEO, one regional director, one
  regional manager and one former employee. There is no `<Faction> Members`
  table worth reading.
- **The decisive 2077 evidence is scattered outside the faction page.** A TV
  financial report, an Arasaka shard, a Badlands computer message, a netpage
  and one ex-executive's fixer page carry almost everything the game says
  about Petrochem politics.

---

## 1. Leadership and ranks

### 1.1 The 2077 chain of command

Petrochem is a public corporation (402 million shares in 2020) with a
family-founded ownership bloc, a board that actually governs, and a CEO who
serves at the board's pleasure. In 2077 it trades as **Petrochem BetterLife**
and is still the world's largest CHOOH2 producer, but it is coming off a bad
year: the 2076 droughts hit the harvest, Brazil and Colombia threatened to
seize crops, and the stock fell as much as 11%. `[wiki]`

| Name | 2077 role | Character record | Location / influence point | Presence class | Source | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| **Lars Muhammad** | CEO (2077); announced the purchase of one million acres in the USSR (Kazakh, Turkmen and Dagestani territories) after the 2076 drought | — (no record; no page) | World HQ, Dallas–Fort Worth / Petrochem Tower, Corpo Plaza | `off-map` | Wiki *List of Petrochem employees* (cited to the *Your Business is My Business* financial report); wiki *Petrochem* | `[wiki]` |
| **Habib al-Moskin** | Regional Executive Director, Petrochem Middle East | — (no record) | Middle East (off-map); named in a shard found on the 66th floor of Arasaka Tower | `mentioned` | Shard *Secure Your Soul: Short-term Priority* (`baseid q115_soul_shard`); wiki *List of Petrochem employees* | `[wiki]` |
| **Michaela LeDoux** | Regional Manager (region unstated); arranges hazardous-waste disposal at the Night City Municipal Landfill | — (no record) | Warbler Lake Hazardous Waste Facility, Badlands / Red Peaks | `mentioned` | Computer message *Waste Collection*, *Warbler Lake Hazardous Waste Facility/Computers*; wiki *List of Petrochem employees* | `[wiki]` |
| **The Board of Directors** | Collective sovereign; 402M shares in 2020 (Trieste largest, Parker second, Youngblood third); 2077 composition unknown | — (no individual records) | Tower One, Irving / Dallas–Fort Worth; regional boards | `off-map` | Wiki *Petrochem* (share structure, board); *Corporation Report 2020 Volume 3* | `[wiki]` `[lore]` |

Notes:

- **The CEO is a manager, not an owner.** The 2020 structure is explicit:
  Trenton Parker was CEO but had fewer votes than Ellen Trieste, and his
  decisions were "subject to her scrutiny, approval and modification." The
  2077 CEO is not described as a shareholder. Treat the board as the sovereign
  and the CEO as the operator until a source says otherwise. `[lore]`
- **The name is spelled two ways.** The employee list says **Lars Muhammad**;
  the TV transcript says **Lars Muhammed**. The employee list is the tidier
  spelling and is used here. Neither spelling has a character record. `[wiki]`
- **Habib al-Moskin is the best evidence of where Petrochem's money goes.**
  He is a paid VIP client of Arasaka's Secure Your Soul: full digitization and
  twelve backups. The shard adds a covert line: obtain an additional copy for
  Dr. Kuroda's team, and do not inform the client. A Petrochem regional
  director is therefore buying immortality from Arasaka while Arasaka copies
  his engram. `[wiki]`
- **Michaela LeDoux is the best evidence of how the regional layer works.**
  She arranges disposal of four cisterns of 10,000 gallons each of NUSHS09
  "human health hazard" reagents at a scrapyard at the municipal landfill, asks
  for a "promotional deal", and wants the paperwork straight "in the event of
  inspection" while thanking the operator for "flexibility concerning
  regulatory red tape." That is a regional manager with disposal authority
  cutting environmental corners, not a board policy. `[wiki]`
- **No Night City executive is named in 2077.** The Tower is the regional HQ,
  but the only 2077 local name is LeDoux, and her region is not stated. The
  last named head of the Night City office is **William Joseph Brentwood**
  (2020/RED). `[wiki]` `[lore]`

### 1.2 The Night City / regional branch

The Night City branch is a regional HQ with **no in-game staff**. What exists
is architecture and paperwork:

| Place | Political function | Evidence |
| --- | --- | --- |
| **Petrochem Tower**, Corpo Plaza | Regional HQ; the corporate face; next to the Kang Tao Building; reached by a bridge from Memorial Park | `[wiki]`; no marker, site or prefab |
| **North Sunrise Oil Fields**, Badlands | Faction HQ and production seat; joint-owned with SovOil and Night Corp | `[game-data]` `[wiki]`; see `../petrochem.md` |
| **Petrochem Nuclear Power Plant**, Arroyo | Industrial seat; fenced compound with a checkpoint; a live safety controversy | `[wiki]`; coordinate `TBD` |
| **Petrochem Fuel Station (Interstate 9)**, Badlands | Retail node; CHOOH2 plus a workshop; sits in Wraith turf | `[game-data]` `[wiki]` |
| **Warbler Lake Hazardous Waste Facility**, Badlands | Illegal disposal point used by a regional manager; not Petrochem-owned | `[wiki]` |

The 2020/RED branch was more substantial than the 2077 one: a 50-story office
on Plaza Drive with a heliport, a subterranean loading dock, a small museum and
gift shop, 24/7 patrols, a troop detachment on call, and computer security
"third only to that of Arasaka and Infocomp." In RED the offices moved to the
Watson Development, directly across the street from SovOil's offices, and the
employees of the two rivals shared a mirrored conapt complex. That is the
branch's real political texture: **Petrochem and SovOil are neighbours who
cannot avoid each other.** `[wiki]` `[lore]`

Two 2077 conflicts are worth recording:

- **The netpage gives a wrong street.** It puts Petrochem Tower on "Sequoia
  St.", but Sequoia Street is in eastern Rancho Coronado, while the Tower is in
  the Corporate Plaza roundabout. The wiki flags the contradiction. Do not use
  the netpage address as a coordinate. `[wiki]`
- **The Tower is generic scenery.** No marker, site, prefab or mappin carries
  its name; patch 2.1 hid an NCART station inside it, but that is a station
  entrance, not a tower anchor. A player cannot walk into a Petrochem office in
  2077. `[game-data]` `[wiki]`

### 1.3 Succession history

Petrochem's succession is **ownership-driven**, not a clean CEO line. The
founder's family kept the title; the largest shareholder kept the power; the
CEO seat changed hands when the ownership blocs let it.

| Period | Top power centre | How the change happened |
| --- | --- | --- |
| 1990s–2003 | **Louis Parker** | Founder of Parker Petrochemicals. He set up the Biotechnica CHOOH2 licence in the mid-1990s with **Ellen Trieste**'s capital; in 1999 she made a sizable investment in the struggling company and became a prime shareholder. Died 2003. `[wiki]` `[lore]` |
| 2003–? | **Trenton Parker** (CEO) with **Ellen Trieste** (chairman, largest shareholder) | Trenton inherited the CEO seat, but Trieste had more votes and could veto or modify his decisions. She later persuaded the board to remove the family name from the company. `[lore]` |
| 2006–2010 | The same two, at war | The Second Corporate War against SovOil (2008–10) split them: Trieste supported it, Trenton opposed it. After the defeat, Trenton nearly seized control; Trieste rallied her supporters and headed off a coup "at the last instant." `[wiki]` `[lore]` |
| 2020 | The same two, near open war | Tensions were "becoming critical"; each side prepared for a war that "could tear the company apart from the inside out"; intrigue and betrayal were rampant. `[lore]` |
| 2040–2045 | **Angus Youngblood** rises | Continental Agricorp spun itself off as Continental Brands (see §2.4). Ellen Trieste died in 2045. Youngblood, her husband and third-largest board power, combined their stock and became **Chief Officer**. `[wiki]` `[lore]` |
| ?–2077 | **Lars Muhammad** (CEO) | No transition date, no predecessor named, no heir named. Muhammad is CEO by 2077 and stakes his tenure on the USSR land purchase. `[wiki]` |

The pattern is **dynastic at the top and managerial below it**. The Parker
family supplied the founder and the first inherited CEO; the Trieste and
Youngblood fortunes supplied the votes; the professional managers supplied the
work. The 2077 CEO is the first top figure with no attested ownership tie, and
the board he answers to has no named members. That is a succession vacuum, not
a settled line. `[inferred]`

### 1.4 Corporate structure, entry and advancement

**Corporate structure (2020 sourcebook, still the claimed org chart).**

1. **The board and major shareholders.** The real sovereign. In 2020: Ellen
   Trieste (most votes, chairman), Trenton Parker (second), Angus Youngblood
   (third). The board could remove a CEO; the CEO could not remove the board.
   `[lore]`
2. **CEO and Chief Officer.** Trenton Parker was CEO under Trieste; Angus
   Youngblood became Chief Officer in 2045. Lars Muhammad is CEO in 2077.
   `[wiki]` `[lore]`
3. **Functional chiefs.** A CFO (Rita Redhawk, five years in post as of 2020),
   a military commander (Col. Marshall Rock Shepard), and regional directors
   and managers. `[lore]`
4. **Divisions.** PAIC's divisions include Petrochem Inc., Petrochem Petroleum
   Technologies, Petrochem CHOOH2, Petrochem Advanced Fuel Technologies, the
   Petrochem Credit Union, Petrochem Chemical Industries and the Petrochem
   Armed Forces. Subdivisions include the Submerged Drilling Project, Shipping,
   Petroleum Refining, Farms, Advanced Fuel Refining, Special Projects,
   Advanced Materials, Alternate Fuels, Weapons, and Lobbying and Marketing.
   `[lore]`
5. **Subsidiaries.** Xoma Pharmaceuticals (drugs), Continental Farms Agricorp
   (food; later Continental Brands), CHOOH4U (fuel retail), Hundred Under
   Haven (convenience stores), SeaRig, International Hydro-Technologies,
   PetroTech Auto Parts, Loomis Advanced Electronic Research, Nanosystems,
   Coastal Carting (garbage), Cactus Water (bottled water), Fire Brand
   (clothing), and a long tail of food and consumer brands. `[lore]`
6. **Security.** Corporate troops, a large standing armed force (50,000 in
   2020), the merchant marine (10,000), and the **Water Leopards**, a Jamaican
   black-ops unit. Xoma's Night City HQ alone kept twenty-two troops on duty,
   with more on call. `[lore]`

**Headcount (2020/2045).** The infobox gives 451,800 employees in 2020 and
338,000 in 2045. The 2020 breakdown is 50,000 armed forces, 10,000 merchant
marine, 40,000 in CHOOH2/oil refining and drilling, 40,000 on farms, 20,000 in
Agri-corp facilities, and 80,000 executives, researchers and staff. `[wiki]`
`[lore]`

**The employee ladder.**

1. **Ownership tier.** Closed to outsiders. Board seats follow shares, not
   merit. A player cannot buy in at a salary; a takeover needs capital or a
   patron. `[inferred]`
2. **Executive tier.** CEO, Chief Officer, CFO, regional directors, refinery
   directors, office heads. Appointed by the board; survival depends on
   ownership backing. `[lore]`
3. **Technical and research tier.** Chemists, engineers, biologists and
   agronomists; Xoma is the prestige subsidiary and recruits "the best and the
   brightest." This is the most plausible entry route for a skilled outsider.
   `[lore]`
4. **Regional and field tier.** Regional managers (LeDoux), farm command
   centres, remote outposts, refinery staff, logistics and retail. Broad,
   poorly supervised, and where the corners get cut. `[wiki]` `[lore]`
   `[inferred]`
5. **Security tier.** Guards, corporate troops, merchant marine, and the
   Water Leopards. Promotion is command-based; loyalty is personal (Weyland to
   Youngblood) as much as corporate. `[lore]`

**Entry and advancement.** There is no Petrochem prologue. The only corpo
lifepath in the game is Arasaka's `q000_corpo_*`, so it is the template, not
the faction. The 2020 material gives the realistic routes: technical/research
recruitment, a regional office job, farm/refinery work, or the armed forces.
Advancement in the middle is meritocratic and political at once — Gilbert
Braham is "out to nail down the score that will assure his rise" — while
advancement at the top is ownership-gated. `[wiki]` `[lore]` `[inferred]`

### 1.5 Named members mapped to game data

No named Petrochem person is in `data/sites/rosters.json`; the roster is empty
for faction 43. The only named person with a character record is **Wade
Bleecker**, and his record is the fixer **Mr. Hands**, not a Petrochem NPC.
No row here is an identity deduction; every record and message is named
explicitly.

| Name | Role / note | Character record | Community / marker | Location | Presence class | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| Lars Muhammad | CEO (2077) | — | — (TV report and employee list only) | Dallas–Fort Worth / Petrochem Tower | `off-map` | `[wiki]` |
| Habib al-Moskin | Regional Executive Director, Middle East | — | Shard `q115_soul_shard` | Arasaka Tower, 66th floor (shard) | `mentioned` | `[wiki]` |
| Michaela LeDoux | Regional Manager; waste disposal | — | Computer message *Waste Collection* | Warbler Lake / Municipal Landfill | `mentioned` | `[wiki]` |
| Wade Bleecker / Mr. Hands | Former high-ranking corporate (2072–74); survived an internal purge and a bounty; now Pacifica's fixer | `Character.mr_hands`; `Character.mr_hands_limited` | Entries `mr_hands`, `mr_hands_holo`, `mr_hands_limited`, `mr_hands_combat_zone` | Pacifica / Dogtown | `story` (PL main jobs) / `world-activity` (gigs) | `[game-data]` `[wiki]` |
| Andrew "Boa Boa" Weyland | Water Leopards commander; dead before 2077 | — | Columbarium niche; Jackie Welles mentions him | Columbarium, Night City | `mentioned` | `[wiki]` `[lore]` |
| Trenton Parker | CEO (2003–?); Parker camp | — | — | Dallas–Fort Worth | `historical` | `[wiki]` `[lore]` |
| Ellen Trieste | Chairman, largest shareholder; died 2045 | — | — | Crystal Tower orbital / Dallas | `historical` | `[wiki]` `[lore]` |
| Angus Youngblood | Board power; Chief Officer 2045 | — | — | Dallas | `historical` | `[wiki]` `[lore]` |
| Malcolm Youngblood | Board member; Angus's candidate for CEO | — | — | Dallas | `historical` | `[wiki]` `[lore]` |
| Marshall Rock Shepard | Colonel; commander of Petrochem's armed forces | — | — | Dallas | `historical` | `[wiki]` `[lore]` |
| Rita Redhawk | CFO (2020) | — | — | Dallas | `historical` | `[wiki]` `[lore]` |
| William Joseph Brentwood | Head of the Night City office (2020/RED) | — | — | Night City | `historical` | `[wiki]` `[lore]` |
| Louis Parker | Founder and first CEO; died 2003 | — | — | Dallas | `historical` | `[wiki]` `[lore]` |

Two data cautions:

- **"Lars" is a colliding token.** The raw registry contains
  `q003_deal_lars_end_peaceful` (The Pickup, Militech/Maelstrom), not Lars
  Muhammad. Do not join the CEO to that phase. There is no record for the CEO.
  `[game-data]`
- **Mr. Hands is not a Petrochem actor in 2077.** He is a fixer with his own
  Pacifica agenda; his Petrochem history is the reason for the `hostile` row in
  §3.2, not a reason to seed him as an employee. `[wiki]`

### 1.6 What the game actually spawns (campaign disabled)

**Nothing Petrochem.** The extract has 0 roster sites, 0 units, 0 community
areas, 0 spawn points, 0 faction-owned sites and no `gamedataAffiliation` value
for Petrochem. The only Petrochem strings in the raw sectors belong to the
Kang Tao quest community `{q104_com_petrochem_operators}`. `[game-data]`

What does exist is **environmental evidence**, not actors:

- the **Petrochem/Netpage** (the "Petrochem BetterLife" sales pitch);
- the **Your Business is My Business** financial report (Lars Muhammad, the
  2076 drought, the USSR land purchase);
- the **Secure Your Soul** shard (Habib al-Moskin, Arasaka's covert copy);
- the **Warbler Lake** computer message (Michaela LeDoux);
- the **Petrochem Tower** and **nuclear plant** exteriors;
- the **I-9 fuel station** and the **oil fields**;
- the **EBM Petrochem Stadium** name (Barghest-held, not Petrochem).

With the campaign disabled, even some of that is gated: the Secure Your Soul
shard is on the 66th floor of Arasaka Tower in *Knockin' on Heaven's Door*, and
Mr. Hands is Phantom Liberty story/gig content. The netpage, the TV report and
the locations persist. **No Petrochem leader will appear unless the mod spawns
one.** `[game-data]` `[wiki]`

Three look-alikes to exclude:

- **Jago Szabó** is Barghest's chief accountant and a Dogtown leadership
  candidate. He embezzled Petrochem funds in 2066, but he is not Petrochem.
  `[wiki]`
- **Sophia Dupont** is a weapon vendor at the EBM Petrochem Stadium. The
  stadium name is a sponsorship; she has no Petrochem affiliation. `[wiki]`
- **The q104 "petrochem operators"** are Kang Tao at the AV crash site. The
  label is a staging name. `[game-data]`

### 1.7 Player-path hooks

| Person / bloc | Join under | Climb past | Ally with | Remove |
| --- | --- | --- | --- | --- |
| **Lars Muhammad** | His expansion bet (an inferred wing, not an attested bloc); the USSR land purchase | The board/ownership ceiling; no heir is named | Biotechnica, Night Corp, Arasaka trade channels | A board vote, an expose of the bet's cost, or a hostile takeover |
| **The board / old ownership** | The Parker–Trieste–Youngblood tradition; shareholder politics | The CEO is the gatekeeper; the board is the prize | Major shareholders, Night Corp as broker | Buy shares, blackmail a director, or run a proxy fight |
| **A regional manager (LeDoux type)** | The regional office; waste, logistics and procurement | The regional director; then the CEO | Local dump owners, corrupt officials, fixers | Expose the dumping or the paperwork; replace with a loyalist |
| **The military wing (Shepard type)** | Corporate security or the armed forces | The security chief; the Water Leopards | Angus-type patrons, arms suppliers | Replace the commander; cut the black-ops budget; set the Leopards against the regulars |
| **Mr. Hands (outside)** | Not a Petrochem path; a fixer with a grudge | — | As an external broker and a source of inside files | He is already hostile; use him as a wedge |

The design consequence: Petrochem offers **two ladders**, and neither reaches
the throne. The corporate ladder runs regional office → regional director →
functional chief → CEO, but the board can fire the CEO. The security ladder
runs guard → troop commander → Water Leopards/black ops, but the army is a
political asset, not a career. A player can become a regional director, a
refinery director, a security commander or a bloc's fixer. Becoming CEO needs a
board coup; becoming an owner needs capital. That is the "join a corp and work
up the ladder" path in `docs/design/gameplay-systems.md` §3, with the top
deliberately closed. `[inferred]`

---

## 2. Internal political factions

### 2.1 The blocs

**There is no attested 2077 bloc.** The faction's last named board blocs are
from 2020, and the last internal rupture is the 2040–45 subsidiary secession.
The only 2070s internal-politics datum is an unnamed purge. The table below is
therefore explicitly historical, not a current roster; a seeder should not
treat these as living organisations without a design decision.

| Bloc | Leader(s) | What it wants | Presence / members hint | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- |
| **Parker camp** (historical, 2003–2020) | Trenton Parker | Keep the CEO seat and the Parker family tradition; block Trieste's consolidation | Trenton; board directors still loyal to the family | *Corporation Report 2020 Volume 3*; wiki *Trenton Parker* | `[lore]` |
| **Trieste–Youngblood camp** (historical) | Ellen Trieste; Angus Youngblood | Remove Parker; install Malcolm Youngblood as CEO; concentrate ownership under Trieste/Youngblood | Trieste (votes, board chair); Angus (strategy, third power); Malcolm (CEO candidate); board supporters | *Corporation Report 2020 Volume 3*; wiki *Ellen Trieste*, *Angus Youngblood* | `[lore]` |
| **Armed forces / Water Leopards** (historical) | Col. Marshall Rock Shepard; Andrew Weyland | Command of all Petrochem forces; Shepard stays impartial, Weyland wants the top job and is loyal to Angus | Regular corporate troops; the Water Leopards black-ops unit | *Corporation Report 2020 Volume 3*; *2020 Solo of Fortune 2*; wiki *Marshall Rock Shepard*, *Andrew Weyland* | `[lore]` |
| **Continental Agricorp secession** (historical, 2040–45) | Olivia Forsythe; Lewis McAllister | Spin Continental Agricorp out of Petrochem; buy half the CHOOH-4U stations; become an independent food/fuel rival | Continental Agricorp staff; the Oasis store chain | *Cyberpunk RED*; wiki *Continental Brands*, *Olivia Forsythe* | `[lore]` |
| **2070s upper-management purge** (unnamed) | Unknown | Protect the company after a management shake-up by sacrificing an executive — "blood at the altar of corporate efficiency" | Unnamed; Wade Bleecker was the intended victim | Wiki *Wade Bleecker* / Mr. Hands database entry | `[wiki]` |

### 2.2 The last attested bloc war: Parker vs Trieste–Youngblood

This is the best-documented internal conflict in Petrochem's history, and it is
the template the simulation should use.

- **The dependency is personal and financial.** Louis Parker had set up the
  Biotechnica CHOOH2 licence in the mid-1990s; Ellen Trieste provided much of
  the capital for it and made a sizable investment in the struggling company in
  1999. She became the largest shareholder; the Parkers kept the CEO title but
  not the votes. Trieste later persuaded the board to remove the family name
  from the company around the time she gave Trenton the CEO seat. `[lore]`
- **The war split the company.** Trieste backed the Second Corporate War
  against SovOil; Trenton opposed it. After the 2010 defeat, Trenton nearly
  seized control, but Trieste "rallied her supporters and headed off a coup at
  the last instant." Neither could unseat the other; neither dared direct
  action. `[wiki]` `[lore]`
- **By 2020 it was critical.** Each side was preparing for a war that could
  "tear the company apart from the inside out"; intrigue and betrayal were
  rampant. `[lore]`
- **Angus Youngblood was the third vector.** He was "firmly in Trieste's camp"
  and always voted with her, but he was out for himself: he combined his stock
  with hers, planned to have Parker declared incompetent if she became
  irrational, and lobbied to install his brother Malcolm as CEO. He viewed the
  marriage as a joke and was waiting for her to die. `[lore]`
- **The outcome was a takeover, not a reconciliation.** Trieste died in 2045;
  Youngblood became Chief Officer; no Parker is named after 2020. `[wiki]`
  `[lore]`

The simulation-ready axis is **ownership vs management**: a CEO with a title
but not the votes, a board that can remove him, and a major shareholder who
wants a different CEO. It needs no invented ideology.

### 2.3 The military wing: Shepard vs Weyland

Petrochem's army is large enough to be a political actor in its own right, and
it had two poles in 2020:

- **Col. Marshall Rock Shepard** commands the armed forces. He was hired from
  outside in 2011 after the SovOil defeat, is popular with his troops, and is
  uncomfortable with executives and boardrooms. He is trying to remain
  impartial, but knows his command is a desirable asset and expects to be
  dragged into the board conflict. `[lore]`
- **Andrew "Boa Boa" Weyland** leads the **Water Leopards**, a Jamaican
  mercenary black-ops unit that joined Petrochem through Angus Youngblood.
  Weyland is completely loyal to Angus, aspires to command all of Petrochem's
  forces, and has been promised the job when Youngblood seizes power. The
  Leopards have an acrimonious relationship with the regular soldiers, and
  Weyland and Shepard dislike and distrust each other while working together as
  the job requires. `[lore]`

This is a **private army inside the army**: a patron's loyalist unit, a
professional commander, and a promised promotion that would overturn the chain
of command. Weyland died before 2077 (his Columbarium niche and Jackie Welles's
mention are the 2077 traces), but the structural tension — regulars vs black
ops, professional command vs patron loyalty — is the best model for a Petrochem
internal war. `[wiki]` `[lore]` `[inferred]`

### 2.4 The subsidiary revolt: Continental Agricorp → Continental Brands

This is the one internal rupture that became an external rival, and it is the
cleanest template for a player-founded splinter.

- Continental Agricorp was Petrochem's agricultural marketing subsidiary — the
  one-step-removed brand that sold food without the Petrochem name. `[lore]`
- In summer 2040, **Olivia Forsythe** (New Beverages Marketing Director) and
  **Lewis McAllister** (New Foods Marketing Director) began a campaign to make
  it independent. While Petrochem's leadership was distracted by the Fourth
  Corporate War's aftermath, the subsidiary forced a spin-off, bought half of
  Petrochem's CHOOH-4U stations, and rebranded them as **Oasis**. Continental
  Brands was born. `[lore]`
- By 2045, Angus Youngblood had a personal rivalry with Forsythe over
  "stealing billions of dollars of intellectual and physical property from
  Petrochem under his watch." He also supposedly conceived the **Hundred Under
  Haven** convenience chain to anger her. `[lore]`

The lesson for the simulation: **Petrochem's subsidiaries are not loyal.** A
charismatic subsidiary executive plus a distracted parent equals a spin-off,
and the parent's response is commercial and legal before it is military.
`[inferred]`

### 2.5 The 2070s purge: Bleecker

The only attested 2070s internal politics is an assassination.

Wade Bleecker was a well-known, high-ranking Petrochem corporate, employed
there from 2072 to 2074. After "a sudden shake-up in upper management," someone
decided "blood needed spilling at the altar of corporate efficiency," and
Bleecker was chosen as the sacrifice. He survived the initial assassination
attempt, but when an official bounty was put on his head he changed his face
and name and disappeared. He is now **Mr. Hands**, Pacifica's fixer. `[wiki]`

What this establishes, and what it does not:

- **Establishes:** a 2070s management purge willing to kill a senior executive;
  a purge, not a resignation; a bounty that outlived the initial attempt.
  `[wiki]`
- **Does not establish:** the faction's name, leader, size or goal; whether it
  still exists in 2077; whether Bleecker was guilty of anything. The "corporate
  efficiency" phrase is the only stated motive. `[inferred]`

For the simulation, Bleecker is a **named grudge with inside knowledge** and a
ready-made hostile fixer. He is not a bloc.

### 2.6 2077: none attested

Say it plainly: **no 2077 Petrochem bloc has a name, leader, goal or member
list.** The faction page is silent; the employee list is four names; the
in-game evidence is a TV report, a shard and a computer message. The historical
blocs in §2.1 are the last attested structure, and the 2070s purge is the only
recent event.

What a designer can reasonably infer — and must label `[inferred]` — is a
**drought-and-expansion fault line**. The 2076 harvest failure and the
one-million-acre USSR purchase are a capital-intensive bet by a non-owner CEO.
A board worried about the share price, a finance wing worried about the
purchase, and a regional wing worried about harvests would all have reasons to
oppose or support him. No source names them. Do not seed them as fact.
`[inferred]`

### 2.7 What could drive internal conflict in a simulation

1. **Ownership vs management.** The 2020 Parker–Trieste war is the template: a
   CEO with the title, a shareholder with the votes, and a board that decides.
2. **The 2076 drought and the USSR land bet.** A bet-the-company purchase that
   could revive the stock or bankrupt the balance sheet; the finance and
   regional wings have opposite interests. `[inferred]`
3. **Subsidiary autonomy.** Continental Agricorp's 2040 spin-off is the
   precedent; Xoma, Coastal Carting or the retail chains could follow.
4. **Regular military vs black ops.** Shepard vs Weyland: professional command
   against a patron's private army, with a promised promotion at stake.
5. **Executive purge and security.** The 2070s shake-up shows a faction willing
   to kill a senior executive; a player can be the next sacrifice or the one
   ordering it.
6. **Succession.** No heir, no named board, no transition date from Youngblood
   to Muhammad. A CEO under harvest pressure with an unnamed board is a vacuum.
7. **External shareholders and predators.** Biotechnica's licence leverage,
   SovOil's predation, Night Corp's brokerage, Continental Brands' poaching.
   These are external, but they decide internal winners. `[inferred]`

---

## 3. External relations matrix

### 3.1 Stance vocabulary and direction

One stance per row. The stance is read **from Petrochem's side**. Because the
generic vocabulary is ambiguous for a supplier/licensor corp, this document
uses these readings:

| Stance | Meaning here |
| --- | --- |
| `war` | Open armed conflict over existence or assets |
| `hostile` | Actively targets or hunts the other side, but not a declared war |
| `rival` | Economic or turf competition, with skirmishes or predation |
| `neutral` | No attested interaction; not an ally |
| `trade` | Transactional sale, purchase or joint venture, no loyalty |
| `ally` | Coordinated support or shared operations (none at game start) |
| `patron` | Petrochem protects, funds or supplies the other side |
| `client` | Petrochem depends on or works for the other side (the licence case) |

The key direction call: **Biotechnica is `client`, not `trade`.** Petrochem
sells fuel to Arasaka and Militech (a sale, so `trade`), but it produces CHOOH2
under Biotechnica's patents and could be destroyed by Biotechnica's viruses.
That is dependence, so `client`. The 2020 sourcebook calls Biotechnica
Petrochem's "strongest ally"; the design forbids an `ally` at game start, and
the relationship is asymmetrically dependent, so `client` is the honest
mechanical reading. `[wiki]` `[lore]`

### 3.2 The matrix

Every row is a faction code from `data/factions.json`, plus `nusa` (a
political actor that matters here). Rows with no attested interaction are
`neutral` and `[inferred]`; they are placeholders, not findings.

| Faction | Code | Stance | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| Tyger Claws | `tyger_claws` | `neutral` | No attested interaction; no shared district, gig or shard `[inferred]` | `inferred` |
| Valentinos | `valentinos` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Arasaka | `arasaka` | `trade` | 2020: "cordial footing" and bulk CHOOH2 discounts for Arasaka, Militech, EBM and IEC; Petrochem researches fusion with Arasaka Heavy Industries; 2077: Habib al-Moskin buys Arasaka's Secure Your Soul (12 backups) while Arasaka covertly copies his engram `[wiki]` | `wiki` |
| Militech | `militech` | `trade` | Petrochem sells Militech rocket propellants, advanced materials and CHOOH2 at bulk discount; the two compete in chemical weapons, which "has not stopped" Militech buying `[wiki]` | `wiki` |
| Kang Tao | `kang_tao` | `neutral` | Petrochem Tower is next to the Kang Tao Building; adjacency only, no deal or incident `[wiki]` `[inferred]` | `wiki+inferred` |
| Biotechnica | `biotechnica` | `client` | CHOOH2 patent licence and *T. vulgaris megasuavis* grain; Petrochem is the largest licensee; Xoma runs a genetic-drug venture with Biotechnica; "strongest ally", but Biotechnica's viruses can destroy the wheat, so the licence is leverage `[wiki]` `[lore]` | `wiki+lore` |
| Barghest | `barghest` | `neutral` | The EBM Petrochem Stadium bears the name from 2060s sponsorship but is Barghest-held; Jago Szabó embezzled Petrochem funds in 2066 before helping found Barghest in 2072; no current relation `[wiki]` | `wiki` |
| 6th Street | `sixth_street` | `neutral` | The Arroyo nuclear plant sits in 6th Street turf; the 6th Street politics doc records neutral, and the Kendachi factory case is adjacency, not conflict `[game-data]` `[wiki]` `[inferred]` | `game-data+wiki+inferred` |
| Aldecaldos | `aldecaldos` | `neutral` | Parker-era oil fields were home to nomad tribes; nomads are fuel customers; no attested 2077 deal or feud `[lore]` `[inferred]` | `lore+inferred` |
| Wraiths | `wraiths` | `rival` | RED-era I-9 tanker runs needed armed escort against Raffen Shiv (the Wraiths' predecessor culture); in 2077 the Wraiths hold the Sunset Motel turf 74 m from the Petrochem station and prey on Badlands convoys; no direct station raid attested `[wiki]` `[game-data]` `[inferred]` | `wiki+game-data+inferred` |
| Animals | `animals` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| The Mox | `the_mox` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Maelstrom | `maelstrom` | `neutral` | No attested interaction; Maelstrom's politics doc records neutral `[inferred]` | `inferred` |
| Voodoo Boys | `voodoo_boys` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| NCPD | `ncpd` | `neutral` | No attested tie; the only 2077 illegality is a regional manager's waste dumping, and no NCPD action is attested `[wiki]` `[inferred]` | `wiki+inferred` |
| Night Corp | `night_corp` | `trade` | Joint owner of the Northern Oil Fields; brokered the Petrochem–SovOil peace after the Fourth Corporate War; also runs city administration, NCART and a solar farm `[wiki]` | `wiki` |
| Scavengers | `scavengers` | `neutral` | No attested interaction; the seed's "Northside Oil Wharf" refinery name is a scav stash, a naming trap, not a relation `[game-data]` `[inferred]` | `game-data+inferred` |
| City Council | `city_council` | `neutral` | The city owns the wind farms and Coronado Dam and regulates the Arroyo nuclear plant; a TV crew presses the plant manager on poisoning; no attested contract or corruption `[wiki]` `[inferred]` | `wiki+inferred` |
| Afterlife | `afterlife` | `neutral` | No attested interaction; merc market only `[inferred]` | `inferred` |
| Regina Jones | `fixer_regina` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Wakako Okada | `fixer_wakako` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Sebastian Ibarra (Padre) | `fixer_padre` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Muamar Reyes (El Capitán) | `fixer_el_capitan` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Dakota Smith | `fixer_dakota` | `neutral` | Her *Sparring Partner* gig uses the Warbler Lake dump where Petrochem dumps waste, but the arrangement is with the dump owner; no Dakota–Petrochem deal `[wiki]` `[inferred]` | `wiki+inferred` |
| Dino Dinovic | `fixer_dino` | `neutral` | No attested interaction `[inferred]` | `inferred` |
| Rogue Amendiares | `fixer_rogue` | `neutral` | No attested interaction; no anti-Petrochem operation `[inferred]` | `inferred` |
| Mr. Hands | `fixer_mr_hands` | `hostile` | Wade Bleecker was a high-ranking Petrochem corporate (2072–74); after an upper-management shake-up he was chosen as a sacrifice, survived an assassination attempt and a bounty, and changed his face and name; he is now Pacifica's fixer `[wiki]` | `wiki` |
| NUSA | `nusa` | `trade` | Netpage: "We supply power to the NUSA and the Free States"; bulk CHOOH2, natural gas and oil customer; a major market and a state regulator, with the 2076 harvest crisis showing how exposed the corp is to state action `[wiki]` | `wiki` |

Stance counts (28 rows): **hostile 1, rival 1, trade 4, client 1, neutral 21,
ally 0, war 0, patron 0.** Petrochem has no ally in the matrix. Its defining
relation, SovOil, has no faction code and is therefore prose only (§3.3), which
is the single biggest matrix hole for this faction.

### 3.3 Actors outside `data/factions.json`

These are real relationships with no faction code. They carry more political
weight than half the matrix.

**SovOil — the arch-rival.** `[wiki]` `[lore]`

- **Second Corporate War (April 2008 – August 2010).** Petrochem and SovOil
  fought over the South China Sea. Petrochem lost: it withdrew from the region,
  SovOil became the sole drilling power there, and Petrochem's stock fell to
  52 EB (from a pre-war 99). Both sides destroyed about 75% of each other's oil
  facilities. Petrochem briefly gained the upper hand by seizing the Spratly
  Islands and assassinating SovOil's founder-CEO Anatoly Novikovo with planes
  loaned by Malaysia. The war's casus belli — the explosion of Petrochem's
  *Sabina Bravo* platform — turned out to be an accident SovOil did not cause.
- **The Prudhoe Pride lease (2021).** Petrochem had leased part of the
  Northern Oil Fields to Prudhoe Pride Oil to fund the war. SovOil bought
  Prudhoe Pride and invoked an obscure clause to claim full ownership of the
  leased properties. Petrochem tried to terminate; the dispute nearly restarted
  the war before the Fourth Corporate War intervened.
- **The uneasy peace.** After the Fourth Corporate War, **Night Corp** brokered
  a peace over the Northern Oil Fields, which the two now own jointly with
  Night Corp. The fields are running dry, so the conflict is now pride as much
  as profit. RED-era rig crews squabbled over property and occasionally a
  worker was murdered; the two companies' Night City employees shared a mirrored
  conapt complex because their own housing had been destroyed.
- **2077.** Both still drain the same fields. The wiki calls SovOil Petrochem's
  "most obvious enemy" and says the two have a decades-long history of
  animosity. This is the faction's defining rivalry, and it is invisible to the
  machine-readable matrix because SovOil is not in `data/factions.json`.

**Other energy and fuel competitors.** `[wiki]` `[lore]`

- **IEC (International Electric Corporation).** A 2020 "cordial footing" and
  bulk CHOOH2 customer, but IEC researches fusion as an alternative to
  CHOOH2-burning plants — a direct threat to Petrochem's long-term fuel
  demand. Not in `factions.json`.
- **EBM.** A 2020 cordial customer with a bulk discount; the EBM Petrochem
  Stadium name is a 2060s sponsorship, not a current holding. Not in
  `factions.json`.
- **Continental Brands.** The former Continental Agricorp subsidiary, spun off
  in 2040–45, now a food and fuel-retail rival (Oasis stores, half the old
  CHOOH-4U network). Olivia Forsythe is its CEO and Angus Youngblood's personal
  rival. Not in `factions.json`.
- **Corp-Bud, independent Badlands stations, and the city utilities.** The
  other fuel retailers and the city-owned wind farms and Coronado Dam compete
  at the edges. The Petrochem station on Interstate 9 is the only 2077 station
  with a Petrochem owner in its infobox; Rocky Ridge, Laguna Bend, Medeski and
  the SovOil Highway 101 station are not Petrochem.

**Subsidiaries and internal actors.** `[lore]`

- **Xoma Pharmaceuticals.** The drug subsidiary, founded in Night City; its
  2020 HQ was a four-story, fenced building in South Night City with 300 staff
  and 22 troops on duty. It runs a genetic-drug venture with Biotechnica. This
  is the best "Petrochem interior" in the lore and has no 2077 game record.
- **Coastal Carting.** The garbage-collection subsidiary; in 2045 it shared the
  Night City Municipal Landfill contract with SovOil's SMKP Hauling. That is
  the institutional ancestor of LeDoux's 2077 waste-disposal arrangement at
  Warbler Lake. `[inferred]`
- **Hundred Under Haven.** The convenience-store chain, supposedly conceived by
  Angus Youngblood to annoy Olivia Forsythe; its I-9 store is the retail face of
  the fuel station in the RED-era layout.
- **Water Leopards.** The black-ops unit, not a faction code. Weyland's loyalty
  was personal to Angus Youngblood, not corporate.
- **Arcadiex and New East Asia Agricultural.** With Petrochem, they formed a
  consortium that owned most of North Dakota's land and ran a corporate
  legislature. This is Petrochem's clearest example of state capture, and it
  has no 2077 code or presence.
- **Prudhoe Pride Oil.** Defunct after SovOil's 2021 acquisition; the lease
  dispute is history, not a current row.

**Night City civic and media.** `[wiki]`

- **The city government** owns the wind farms and Coronado Dam, regulates the
  Arroyo nuclear plant, and is a lobbying target by inference. The TV
  interview outside the plant — a reporter asking the manager whether the plant
  is poisoning the neighbourhood — is the only 2077 civic-pressure scene.
- **WNS / *Your Business is My Business*.** The business show is pro-Arasaka
  and treats Petrochem as a stock tip. It is a media channel, not an ally.
- **The NCPD** has no attested Petrochem tie. The illegal dumping is a
  regulatory failure, not a proven police arrangement.

### 3.4 Guarantor assessment

This is the design question: if a player founds an organisation, which
factions would guarantee Petrochem's support, and which would Petrochem itself
guarantee?

- **No faction is an ally.** The matrix has no `ally` row. Petrochem's `trade`
  rows are sales and joint ventures; its one `client` row is a licence
  dependence. Nothing in the lore says Petrochem will fight for another
  faction. `[inferred]`
- **Petrochem is a supplier, not a patron.** It can provide fuel, feedstock,
  materials, logistics and a security contract. Its army exists to protect
  wells, farms, refineries and offices, not to wage proxy wars. A player who
  wants Petrochem's backing should expect a commercial contract with an
  option to buy the player out, not a guarantee. `[inferred]`
- **Plausible guarantors for a player-founded organisation** are transactional
  and local: a corrupt regional manager (LeDoux type) who needs a deniable
  crew; a Biotechnica licence channel; Night Corp as a broker; an Arasaka
  trade contact (with the engram-copy risk); a Militech fuel contract; or
  Mr. Hands, who knows the inside and hates it. None is a corporate alliance.
  `[inferred]`
- **Petrochem as an aggressor.** If a player founds on Petrochem ground — the
  oil fields, the I-9 station, the nuclear plant — Petrochem is more likely to
  use legal title, security troops and a buyout than to declare war. The I-9
  station sits in Wraith turf, so the first fight may be with the Wraiths, not
  Petrochem. `[game-data]` `[inferred]`
- **SovOil and Night Corp are the outside guarantors to watch.** SovOil would
  back a wedge against Petrochem; Night Corp would rather broker a settlement
  than pick a side. Both are outside `factions.json`, which is exactly why the
  matrix cannot express this faction's real politics. `[inferred]`

---

## 4. Pillar notes

Design claims from `docs/design/gameplay-systems.md`: Petrochem is a
**Corporation** (archetype strength Technology, weakness Culture); faction
strength **Economy**, weakness **Espionage**.

| Pillar | Design claim | Lore verdict | Evidence |
| --- | --- | --- | --- |
| Technology (archetype strength) | Corporations are technology-led | **Strongly supported, but industrial.** Petrochem's edge is process chemistry, CHOOH2 refining, agri-genetics under licence, advanced materials, nanotech, Xoma pharma and fusion research — thousands of patents a month. It is not a consumer-cyberware company. | CHOOH2 process; *T. megasuavis*; advanced materials; Nanosystems; Xoma; fusion research `[wiki]` `[lore]` |
| Culture (archetype weakness) | Corporations are culturally weak | **Supported.** Petrochem buys goodwill — "BetterLife" greenwash, food charity, stadium and museum sponsorship — but it does not earn affection. The 2077 evidence is a poisoning controversy and an illegal dumping arrangement. Internally there is a real Old West/oil nostalgia and an ownership tradition, but it does not export. | Netpage; database entry; stadium; museum; nuclear-plant interview; LeDoux message `[wiki]` `[lore]` |
| Economy (faction strength) | Petrochem is an economic power | **Strongly supported.** World's largest CHOOH2 producer (60% of world supplies), top-eight megacorp in 2020, €$381B in assets, 402M shares, millions of acres, 400,000+ employees, 50,000 armed forces. The weakness is harvest dependence: the 2076 drought cut the stock 11%. | Wiki *Petrochem*; *Your Business is My Business*; *Corporation Report 2020 Volume 3* `[wiki]` `[lore]` |
| Espionage (faction weakness) | Petrochem is weak at espionage | **Supported with a twist: strong at the fence, porous at the periphery.** The core has "the best industry counterintel specialists", high alert, corporate troops and black resources (Water Leopards, viral agents). But subsidiaries secede, an employee embezzles, a senior executive is nearly assassinated after a management purge, Arasaka covertly copies a regional director's engram, and a regional manager illegally dumps waste. Model it as porous edges, not absent capability. | Database entry; Continental Brands; Jago; Bleecker; Secure Your Soul shard; LeDoux `[wiki]` `[lore]` `[inferred]` |
| Overall fit | The pillars fit the corp's identity | **Good.** Keep Economy and Technology strong; keep Culture weak as external soft power; model Espionage as a perimeter problem. Do not turn Petrochem into a pushover: it has a small-country army and a biological black-resource arsenal. | Synthesis of the rows above `[inferred]` |

Design cautions, not redesigns:

- **The CHOOH2 licence is the economic and political hinge.** Whoever holds
  Biotechnica's favour holds Petrochem's margin. A licence-renewal crisis is a
  better Petrochem story than a turf war.
- **The 2076 drought is the best current-events hook.** It justifies fuel
  scarcity, convoy missions, harvest seizures, land grabs and a CEO under
  pressure. It also gives the Wraiths and SovOil a reason to move.
- **The army is a political actor.** 50,000 troops and a black-ops unit are not
  scenery; they are the reason a board member wants the security chief's
  loyalty.
- **Do not model Culture as zero.** The internal ownership/family/oil culture
  is real and binds the executive layer; it simply does not win outsiders.

---

## 5. Gaps and uncertainties

1. **Petrochem has no NPCs and no character records.** 0 rosters, 0 areas, 0
   spawns, 0 sites, no `gamedataAffiliation` value. Every leader is wiki/lore
   only. The mod must spawn all of them; there is no in-game actor to reuse.
   `[game-data]`
2. **The CEO's name is spelled two ways.** *Lars Muhammad* (employee list) vs
   *Lars Muhammed* (TV transcript). Neither has a page or a record. Pick one
   spelling and keep it consistent in the seed.
3. **No Night City executive is named in 2077.** Habib al-Moskin is Middle East;
   LeDoux's region is unstated; the Tower has no staff. The last named Night
   City head is Brentwood (2020/RED).
4. **The 2045–2077 succession is blank.** Angus Youngblood is Chief Officer in
   2045; Lars Muhammad is CEO in 2077. No predecessor, date, heir or board
   vote is recorded.
5. **The 2077 board has no members.** The 2020 share structure (Trieste,
   Parker, Youngblood) is the only ownership data. Do not invent 2077 directors.
6. **No 2077 internal bloc is attested.** The Parker, Trieste–Youngblood,
   military and Continental blocs are 2020/RED history. The only 2070s datum
   is the unnamed purge that targeted Bleecker. §2.1 is labelled historical
   for that reason.
7. **Bleecker's purge has no date, faction, leader or charge.** His employment
   dates (2072–74) come from the employee list, whose citation is indirect; the
   assassination and bounty come from his database entry. Treat the dates as
   approximate.
8. **SovOil has no faction code.** The faction's defining rivalry cannot be a
   machine-readable relation row. The same is true of IEC, EBM, Continental
   Brands, Xoma and Arcadiex. This is the biggest METHOD gap for this doc.
9. **The `patron`/`client` vocabulary is still ambiguous for a licensee.** The
   method defines `client` as "depends on or works for", which fits Biotechnica,
   but a licence is not a hired-crew relationship. This doc states its reading
   in §3.1; the METHOD should add `supplier`/`licensee` or a direction field.
10. **`mentioned` is defined as shards or dialogue.** This faction's best
    evidence is a TV report, a netpage and a computer message. The class worked,
    but the definition should include in-game broadcasts, netpages and
    documents.
11. **The seed has two Petrochem sub-territories, not one.** The location doc
    says one; the current data has `bls_rocky_ridge` ("Petrochem Fuel Station
    (I-9)", active CC, correct anchor) and `arr_petrochem_yard` ("Petrochem
    Freight Yard", inactive CC, still on Arasaka's Industrial Park). The
    faction HQ file points at the oil fields. This doc does not change the
    seed; the location doc's count is stale.
12. **The Petrochem Freight Yard is still a fiction.** It is 5.2 m from an
    Arasaka Industrial Park warehouse marker and every site in its sub-territory
    is Arasaka-owned. Do not treat it as a Petrochem political asset.
13. **The Secure Your Soul shard is one line of evidence, not a policy.** It
    proves that one Petrochem regional director bought Arasaka's service and
    that Arasaka covertly copied him. It does not prove a corporate
    Petrochem–Arasaka intelligence relationship. `[wiki]`
14. **LeDoux's dumping is one computer message.** It proves a regional
    manager's corruption and a disposal channel, not a board-level
    environmental policy. The facility is owned by an unnamed junk vendor, not
    Petrochem. `[wiki]`
15. **The EBM Petrochem Stadium is a naming trap.** It is Barghest-held in
    2077; Petrochem was a 2060s sponsor/participant. It is not a Petrochem
    holding and should not count as one. `[wiki]` `[game-data]`
16. **Jago's embezzlement is a 2066 crime, not a current alliance.** He is
    Barghest's chief accountant and a Dogtown leadership candidate. The
    Barghest politics doc already records the pair as neutral.
17. **The Arasaka politics doc records Petrochem as `neutral`.** This doc
    records `trade`, based on the 2020 "cordial footing", the bulk CHOOH2
    discount, the fusion collaboration and the 2077 Secure Your Soul purchase.
    The Arasaka row is a placeholder that under-reads the 2020 source; flag the
    divergence rather than silently averaging it.
18. **The 2020 org chart is 57 years old.** The divisions, headcount, share
    structure and 50,000-strong army are 2020/RED. The 2077 game shows a
    tower, a plant, a station and a name. Treat the org chart as the structure
    the corp claims, not a fully modelled 2077 reality.
19. **There is no offline attitude matrix.** `Affiliation.hpp` is an identity
    enum and `Attitude_Record.hpp` is opaque. Every stance in §3.2 is judged
    from lore, quests and spatial adjacency, not from a TweakDB relation row.
20. **There is no player-join path in the game.** The only corpo prologue is
    Arasaka's `q000_corpo_*`. A Petrochem employee path must be built from the
    2020 ladder and the location doc's places.
21. **The 2077 TV report names the wrong feedstock.** It calls soybean and corn
    CHOOH2's "primary components"; the 2020 sourcebook and the netpage name the
    genetically modified wheat *T. vulgaris megasuavis*. The TV line is a
    simplified news report, not the full feedstock model. Do not build a
    soybean/corn supply chain from it.
22. **The 2020 headcount breakdown does not sum.** The listed categories add to
    240,000 of the stated 400,000+ employees; the source omits categories. Use
    the total as scale, not the breakdown as a complete payroll.

### 5.1 Sources consulted

Local:

- `data/factions.json` — faction 43 (`petrochem`, `affiliation_enum: null`,
  megacorp).
- `data/sub_territories.json`, `data/control_centers.json`,
  `data/landmarks.json`, `data/faction_headquarters.json` — the two owned
  sub-territories, both CCs, the two landmarks and the oil-fields HQ.
- `data/sites/rosters.json`, `data/sites/sites.json`, `data/spawn_points.json`
  — zero rows for faction 43.
- `dist/extract/areas.jsonl` — zero areas containing `petrochem`; the Kang Tao
  `{q104_com_petrochem_operators}` row.
- `dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_0.streamingsector.json`
  — the only `petrochem` string is the q104 Kang Tao community.
- `dist/extract/raw/.../always_loaded_1.streamingsector.json` — Mr. Hands
  records `Character.mr_hands`, `Character.mr_hands_limited`; entries
  `mr_hands`, `mr_hands_holo`, `mr_hands_limited`, `mr_hands_combat_zone`.
- `docs/design/gameplay-systems.md` — archetype and pillar claims; §7 alternate
  timeline.
- `docs/research/factions/METHOD.md` §1.1–§1.2 — data pitfalls.
- `docs/research/factions/politics/METHOD.md` — politics method.
- `docs/research/factions/petrochem.md` — locations, coordinates and the
  zero-footprint finding.
- `docs/research/factions/politics/arasaka.md`,
  `docs/research/factions/politics/militech.md` — corp worked examples.
- `docs/research/factions/night-corp.md`,
  `docs/research/factions/biotechnica.md`,
  `docs/research/factions/politics/barghest.md`,
  `docs/research/factions/politics/sixth-street.md`,
  `docs/research/factions/politics/kang-tao.md` — the other side of the
  relations.

Wiki (MediaWiki API, wikitext only, 2026-11-25):

- [Petrochem](https://cyberpunk.fandom.com/wiki/Petrochem) ·
  [Petrochem/Netpage](https://cyberpunk.fandom.com/wiki/Petrochem/Netpage) ·
  [List of Petrochem employees](https://cyberpunk.fandom.com/wiki/List_of_Petrochem_employees) ·
  [Lars Muhammad](https://cyberpunk.fandom.com/wiki/Lars_Muhammad) (no page)
- [Wade Bleecker](https://cyberpunk.fandom.com/wiki/Wade_Bleecker) ·
  [Your Business is My Business](https://cyberpunk.fandom.com/wiki/Your_Business_is_My_Business) ·
  [Secure Your Soul: Short-term Priority](https://cyberpunk.fandom.com/wiki/Secure_Your_Soul:_Short-term_Priority) ·
  [Warbler Lake Hazardous Waste Facility](https://cyberpunk.fandom.com/wiki/Warbler_Lake_Hazardous_Waste_Facility)
- [Petrochem Tower](https://cyberpunk.fandom.com/wiki/Petrochem_Tower) ·
  [Petrochem Nuclear Power Plant](https://cyberpunk.fandom.com/wiki/Petrochem_Nuclear_Power_Plant) ·
  [Petrochem Fuel Station (Interstate 9)](https://cyberpunk.fandom.com/wiki/Petrochem_Fuel_Station_(Interstate_9)) ·
  [Northern Oil Fields](https://cyberpunk.fandom.com/wiki/Northern_Oil_Fields) ·
  [EBM Petrochem Stadium](https://cyberpunk.fandom.com/wiki/EBM_Petrochem_Stadium)
- [Second Corporate War](https://cyberpunk.fandom.com/wiki/Second_Corporate_War) ·
  [SovOil](https://cyberpunk.fandom.com/wiki/SovOil) ·
  [Prudhoe Pride Oil](https://cyberpunk.fandom.com/wiki/Prudhoe_Pride_Oil) ·
  [Biotechnica](https://cyberpunk.fandom.com/wiki/Biotechnica) ·
  [Night Corp](https://cyberpunk.fandom.com/wiki/Night_Corp)
- [Louis Parker](https://cyberpunk.fandom.com/wiki/Louis_Parker) ·
  [Trenton Parker](https://cyberpunk.fandom.com/wiki/Trenton_Parker) ·
  [Ellen Trieste](https://cyberpunk.fandom.com/wiki/Ellen_Trieste) ·
  [Angus Youngblood](https://cyberpunk.fandom.com/wiki/Angus_Youngblood) ·
  [Marshall Rock Shepard](https://cyberpunk.fandom.com/wiki/Marshall_Rock_Shepard) ·
  [Andrew Weyland](https://cyberpunk.fandom.com/wiki/Andrew_Weyland) ·
  [Gilbert Braham](https://cyberpunk.fandom.com/wiki/Gilbert_Braham)
- [Continental Brands](https://cyberpunk.fandom.com/wiki/Continental_Brands) ·
  [Olivia Forsythe](https://cyberpunk.fandom.com/wiki/Olivia_Forsythe) ·
  [Xoma Pharmaceuticals Headquarters](https://cyberpunk.fandom.com/wiki/Xoma_Pharmaceuticals_Headquarters) ·
  [Coastal Carting](https://cyberpunk.fandom.com/wiki/Coastal_Carting) ·
  [Hundred Under Haven](https://cyberpunk.fandom.com/wiki/Hundred_Under_Haven) ·
  [Cactus Water](https://cyberpunk.fandom.com/wiki/Cactus_Water) ·
  [Fire Brand](https://cyberpunk.fandom.com/wiki/Fire_Brand)
- [Petrochem Offices (2020)](https://cyberpunk.fandom.com/wiki/Petrochem_Offices_(2020)) ·
  [Petrochem Offices (RED)](https://cyberpunk.fandom.com/wiki/Petrochem_Offices_(RED)) ·
  [Petrochem & SovOil Joint Temporary Housing Solution](https://cyberpunk.fandom.com/wiki/Petrochem_%26_SovOil_Joint_Temporary_Housing_Solution) ·
  [Petrochem Fine Arts Museum](https://cyberpunk.fandom.com/wiki/Petrochem_Fine_Arts_Museum) ·
  [Petrochem Refinery Terminal](https://cyberpunk.fandom.com/wiki/Petrochem_Refinery_Terminal) ·
  [Dynergy Power Plant](https://cyberpunk.fandom.com/wiki/Dynergy_Power_Plant)
- [Jago Szabó](https://cyberpunk.fandom.com/wiki/Jago_Szab%C3%B3) ·
  [Arcadiex](https://cyberpunk.fandom.com/wiki/Arcadiex) ·
  [Sophia Dupont](https://cyberpunk.fandom.com/wiki/Sophia_Dupont)

---

## 6. Machine-readable block

```json
{
  "faction_code": "petrochem",
  "leaders": [
    {
      "name": "Lars Muhammad",
      "role": "CEO (2077); announced the purchase of one million acres in the USSR after the 2076 drought",
      "character_record_id": null,
      "location_name": "World HQ, Dallas-Fort Worth / Petrochem Tower, Corpo Plaza",
      "presence_class": "off-map",
      "open_world": false,
      "source": "wiki List of Petrochem employees (cited to the Your Business is My Business financial report); wiki Petrochem; no character record",
      "confidence": "wiki"
    },
    {
      "name": "Habib al-Moskin",
      "role": "Regional Executive Director, Petrochem Middle East; paid Secure Your Soul VIP client",
      "character_record_id": null,
      "location_name": "Petrochem Middle East (off-map); shard found on the 66th floor of Arasaka Tower",
      "presence_class": "mentioned",
      "open_world": false,
      "source": "shard Secure Your Soul: Short-term Priority (baseid q115_soul_shard); wiki List of Petrochem employees",
      "confidence": "wiki"
    },
    {
      "name": "Michaela LeDoux",
      "role": "Regional Manager; arranged hazardous-waste disposal at the Night City Municipal Landfill",
      "character_record_id": null,
      "location_name": "Warbler Lake Hazardous Waste Facility, Badlands / Red Peaks",
      "presence_class": "mentioned",
      "open_world": false,
      "source": "computer message Waste Collection, Warbler Lake Hazardous Waste Facility/Computers; wiki List of Petrochem employees",
      "confidence": "wiki"
    },
    {
      "name": "Petrochem Board of Directors",
      "role": "Collective sovereign; 402M shares in 2020; 2077 composition unknown",
      "character_record_id": null,
      "location_name": "Tower One, Irving / Dallas-Fort Worth; regional boards",
      "presence_class": "off-map",
      "open_world": false,
      "source": "wiki Petrochem (share structure, board); Corporation Report 2020 Volume 3",
      "confidence": "wiki+lore"
    },
    {
      "name": "Louis Parker",
      "role": "Founder and first CEO; died 2003",
      "character_record_id": null,
      "location_name": "Dallas-Fort Worth",
      "presence_class": "historical",
      "open_world": false,
      "source": "wiki Louis Parker; wiki List of Petrochem employees; Corporation Report 2020 Volume 3",
      "confidence": "wiki+lore"
    },
    {
      "name": "Trenton Parker",
      "role": "CEO (2003-?); Parker camp leader; second-largest shareholder",
      "character_record_id": null,
      "location_name": "Dallas-Fort Worth",
      "presence_class": "historical",
      "open_world": false,
      "source": "wiki Trenton Parker; Corporation Report 2020 Volume 3",
      "confidence": "wiki+lore"
    },
    {
      "name": "Ellen Trieste",
      "role": "Chairman of the board and largest shareholder; died 2045",
      "character_record_id": null,
      "location_name": "Crystal Tower orbital / Dallas-Fort Worth",
      "presence_class": "historical",
      "open_world": false,
      "source": "wiki Ellen Trieste; Corporation Report 2020 Volume 3",
      "confidence": "wiki+lore"
    },
    {
      "name": "Angus Youngblood",
      "role": "Board power; Chief Officer by 2045; Trieste's husband and heir",
      "character_record_id": null,
      "location_name": "Dallas-Fort Worth",
      "presence_class": "historical",
      "open_world": false,
      "source": "wiki Angus Youngblood; wiki Ellen Trieste; Corporation Report 2020 Volume 3; Cyberpunk RED",
      "confidence": "wiki+lore"
    },
    {
      "name": "Malcolm Youngblood",
      "role": "Board member; Angus's candidate for CEO",
      "character_record_id": null,
      "location_name": "Dallas-Fort Worth",
      "presence_class": "historical",
      "open_world": false,
      "source": "wiki Angus Youngblood; wiki List of Petrochem employees; Corporation Report 2020 Volume 3",
      "confidence": "wiki+lore"
    },
    {
      "name": "Marshall Rock Shepard",
      "role": "Colonel; commander of Petrochem's armed forces",
      "character_record_id": null,
      "location_name": "Dallas-Fort Worth",
      "presence_class": "historical",
      "open_world": false,
      "source": "wiki Marshall Rock Shepard; Corporation Report 2020 Volume 3",
      "confidence": "wiki+lore"
    },
    {
      "name": "Rita Redhawk",
      "role": "Chief Financial Officer (2020)",
      "character_record_id": null,
      "location_name": "Dallas-Fort Worth",
      "presence_class": "historical",
      "open_world": false,
      "source": "wiki List of Petrochem employees; Corporation Report 2020 Volume 3",
      "confidence": "wiki+lore"
    },
    {
      "name": "William Joseph Brentwood",
      "role": "Head of the Night City office (2020/RED); last named Night City executive",
      "character_record_id": null,
      "location_name": "Petrochem Offices, Night City",
      "presence_class": "historical",
      "open_world": false,
      "source": "wiki List of Petrochem employees; wiki Petrochem Offices (2020); wiki Petrochem Offices (RED)",
      "confidence": "wiki+lore"
    },
    {
      "name": "Andrew Weyland",
      "role": "Water Leopards commander; loyal to Angus Youngblood; dead before 2077",
      "character_record_id": null,
      "location_name": "Columbarium, Night City (niche); Dallas-Fort Worth (historic)",
      "presence_class": "mentioned",
      "open_world": false,
      "source": "wiki Andrew Weyland; wiki List of Petrochem employees; 2020 Solo of Fortune 2; Jackie Welles mention in The Heist",
      "confidence": "wiki+lore"
    }
  ],
  "internal_factions": [
    {
      "name": "Parker camp (historical, 2003-2020s)",
      "leader": "Trenton Parker",
      "goals": "Keep the CEO seat and the Parker family tradition; block Trieste's consolidation",
      "members_hint": "Trenton Parker; board directors still loyal to the Parker family",
      "source": "Corporation Report 2020 Volume 3; wiki Trenton Parker",
      "confidence": "lore"
    },
    {
      "name": "Trieste-Youngblood camp (historical, 2003-2045)",
      "leader": "Ellen Trieste / Angus Youngblood",
      "goals": "Push Parker out; install Malcolm Youngblood as CEO; concentrate ownership under Trieste and Youngblood",
      "members_hint": "Ellen Trieste; Angus Youngblood; Malcolm Youngblood; board supporters",
      "source": "Corporation Report 2020 Volume 3; wiki Ellen Trieste; wiki Angus Youngblood",
      "confidence": "lore"
    },
    {
      "name": "Armed forces / Water Leopards (historical, 2020)",
      "leader": "Marshall Rock Shepard / Andrew Weyland",
      "goals": "Command of all Petrochem forces; Shepard stays impartial, Weyland wants the top job and is loyal to Angus",
      "members_hint": "Regular corporate troops; the Water Leopards black-ops unit",
      "source": "Corporation Report 2020 Volume 3; 2020 Solo of Fortune 2; wiki Marshall Rock Shepard; wiki Andrew Weyland",
      "confidence": "lore"
    },
    {
      "name": "Continental Agricorp secession (historical, 2040-2045)",
      "leader": "Olivia Forsythe",
      "goals": "Spin Continental Agricorp out of Petrochem; buy half the CHOOH-4U stations; become an independent food and fuel rival",
      "members_hint": "Olivia Forsythe; Lewis McAllister; Continental Agricorp staff; Oasis stores",
      "source": "Cyberpunk RED; wiki Continental Brands; wiki Olivia Forsythe",
      "confidence": "lore"
    },
    {
      "name": "2070s upper-management purge (unnamed)",
      "leader": null,
      "goals": "Protect the company after a management shake-up by sacrificing an executive - blood at the altar of corporate efficiency",
      "members_hint": "Unnamed; Wade Bleecker was the intended victim",
      "source": "wiki Wade Bleecker / Mr. Hands database entry",
      "confidence": "wiki"
    }
  ],
  "relations": [
    {
      "faction_code": "tyger_claws",
      "stance": "neutral",
      "evidence": "No attested interaction; no shared district, gig or shard [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "valentinos",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "arasaka",
      "stance": "trade",
      "evidence": "2020 cordial footing and bulk CHOOH2 discounts for Arasaka, Militech, EBM and IEC; Petrochem researches fusion with Arasaka Heavy Industries; 2077 Habib al-Moskin buys Arasaka Secure Your Soul (12 backups) while Arasaka covertly copies his engram [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "militech",
      "stance": "trade",
      "evidence": "Petrochem sells Militech rocket propellants, advanced materials and CHOOH2 at bulk discount; the two compete in chemical weapons, which has not stopped Militech buying [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "kang_tao",
      "stance": "neutral",
      "evidence": "Petrochem Tower is next to the Kang Tao Building; adjacency only, no deal or incident [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "biotechnica",
      "stance": "client",
      "evidence": "CHOOH2 patent licence and T. vulgaris megasuavis grain; Petrochem is the largest licensee; Xoma runs a genetic-drug venture with Biotechnica; strongest ally, but Biotechnica's viruses can destroy the wheat, so the licence is leverage [wiki] [lore]",
      "confidence": "wiki+lore"
    },
    {
      "faction_code": "barghest",
      "stance": "neutral",
      "evidence": "The EBM Petrochem Stadium bears the name from 2060s sponsorship but is Barghest-held; Jago Szabo embezzled Petrochem funds in 2066 before helping found Barghest in 2072; no current relation [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "sixth_street",
      "stance": "neutral",
      "evidence": "The Arroyo nuclear plant sits in 6th Street turf; the 6th Street politics doc records neutral, and the Kendachi factory case is adjacency, not conflict [game-data] [wiki] [inferred]",
      "confidence": "game-data+wiki+inferred"
    },
    {
      "faction_code": "aldecaldos",
      "stance": "neutral",
      "evidence": "Parker-era oil fields were home to nomad tribes; nomads are fuel customers; no attested 2077 deal or feud [lore] [inferred]",
      "confidence": "lore+inferred"
    },
    {
      "faction_code": "wraiths",
      "stance": "rival",
      "evidence": "RED-era I-9 tanker runs needed armed escort against Raffen Shiv (the Wraiths' predecessor culture); in 2077 the Wraiths hold the Sunset Motel turf 74 m from the Petrochem station and prey on Badlands convoys; no direct station raid attested [wiki] [game-data] [inferred]",
      "confidence": "wiki+game-data+inferred"
    },
    {
      "faction_code": "animals",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
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
      "evidence": "No attested interaction; Maelstrom's politics doc records neutral [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "voodoo_boys",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "ncpd",
      "stance": "neutral",
      "evidence": "No attested tie; the only 2077 illegality is a regional manager's waste dumping, and no NCPD action is attested [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "night_corp",
      "stance": "trade",
      "evidence": "Joint owner of the Northern Oil Fields; brokered the Petrochem-SovOil peace after the Fourth Corporate War; also runs city administration, NCART and a solar farm [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "scavengers",
      "stance": "neutral",
      "evidence": "No attested interaction; the seed's Northside Oil Wharf refinery name is a scav stash, a naming trap, not a relation [game-data] [inferred]",
      "confidence": "game-data+inferred"
    },
    {
      "faction_code": "city_council",
      "stance": "neutral",
      "evidence": "The city owns the wind farms and Coronado Dam and regulates the Arroyo nuclear plant; a TV crew presses the plant manager on poisoning; no attested contract or corruption [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "afterlife",
      "stance": "neutral",
      "evidence": "No attested interaction; merc market only [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_regina",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_wakako",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_padre",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_el_capitan",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_dakota",
      "stance": "neutral",
      "evidence": "Her Sparring Partner gig uses the Warbler Lake dump where Petrochem dumps waste, but the arrangement is with the dump owner; no Dakota-Petrochem deal [wiki] [inferred]",
      "confidence": "wiki+inferred"
    },
    {
      "faction_code": "fixer_dino",
      "stance": "neutral",
      "evidence": "No attested interaction [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_rogue",
      "stance": "neutral",
      "evidence": "No attested interaction; no anti-Petrochem operation [inferred]",
      "confidence": "inferred"
    },
    {
      "faction_code": "fixer_mr_hands",
      "stance": "hostile",
      "evidence": "Wade Bleecker was a high-ranking Petrochem corporate (2072-74); after an upper-management shake-up he was chosen as a sacrifice, survived an assassination attempt and a bounty, and changed his face and name; he is now Pacifica's fixer [wiki]",
      "confidence": "wiki"
    },
    {
      "faction_code": "nusa",
      "stance": "trade",
      "evidence": "Netpage: We supply power to the NUSA and the Free States; bulk CHOOH2, natural gas and oil customer; a major market and state regulator, with the 2076 harvest crisis showing how exposed the corp is to state action [wiki]",
      "confidence": "wiki"
    }
  ]
}
```
