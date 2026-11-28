# Gameplay Systems (design draft)

Status: owner's design draft, 2026-11-25. Early and incomplete; fleshed out
iteratively. Agents: treat this file as design intent. Do not implement a
system here until it is specified further; ask when scope is unclear.

Systems: **Politics, Espionage, Economy, Military, Culture, Technology,
Missions, Companions.**

Missions are generated from the simulation: they derive from what each
faction's AI wants to do. They come after the faction, territory and pillar
systems they depend on.

## 1. Faction archetypes and pillars

Each faction belongs to an archetype. The archetype and the faction each
have a strength and a weakness pillar.

| Archetype | Strength | Weakness | Factions |
| --- | --- | --- | --- |
| Syndicate | Economy | Military | Tyger Claws, Valentinos |
| Corporation | Technology | Culture | Arasaka, Militech, Kang Tao, Biotechnica, Petrochem |
| Paramilitary Organization | Military | Economy | Barghest, 6th Street, NCPD/MaxTac (tentative) |
| Tribe | Culture | Espionage | Aldecaldos, Wraiths, Animals |
| Ideological Collective | Culture | Economy | The Mox, Maelstrom, Voodoo Boys |

| Faction | Archetype | Strength | Weakness |
| --- | --- | --- | --- |
| Tyger Claws | Syndicate | Technology | Culture |
| Valentinos | Syndicate | Culture | Politics |
| Arasaka | Corporation | Espionage | Politics |
| Militech | Corporation | Military | Espionage |
| Kang Tao | Corporation | Espionage | Economy |
| Biotechnica | Corporation | Economy | Military |
| Petrochem | Corporation | Economy | Espionage |
| Barghest | Paramilitary | Politics | Espionage |
| 6th Street | Paramilitary | Culture | Politics |
| NCPD/MaxTac | Paramilitary | Technology | Politics |
| Aldecaldos | Tribe | Economy | Technology |
| Wraiths | Tribe | Military | Politics |
| Animals | Tribe | Military | Technology |
| The Mox | Ideological Collective | Politics | Military |
| Maelstrom | Ideological Collective | Technology | Politics |
| Voodoo Boys | Ideological Collective | Espionage | Politics |

Scope: territory is modeled only under the factions above plus the Scavs.
Places owned by anything else (Trauma Team, Afterlife, Orbital Air,
Zetatech, NetWatch, the fixers, …) are dropped as nodes.

Special factions:

- **Night Corp and the Government of Night City:** special political
  factions with no territory. The city's mayoral politics runs on a **three-way
  political structure** (owner, 2026-11-27):
  1. **Current Mayor** (Lucius Rhyne / Weldon Holt): **pro-corp** (NCPD counts
     as corp) / **anti-gang**.
  2. **Jefferson Peralez:** **anti-corp (federalist)** / **anti-gang**.
  3. **Third Candidate:** **pro-gang** / **anti-corp**.
  Any city politician can be targeted by assassination contracts (available to
  V and to AI factions hiring off-screen freelancers of varying quality).
  Political assassinations are hard and rare, with a discovery chance that
  applies a political-influence-gain penalty to the sponsor. On death, a
  politician gets an immediate dynamically generated replacement; if the
  **Mayor** dies, the Mayor's simulation effects are nulled until a special
  **election 1 week (7 turns) later**. The game has no Night Corp affiliation,
  so places tied to Night Corp go to NCPD.
- **Scavs:** rebels/pirates, the unaligned swarm faction (like rebels in
  Mount & Blade or pirates in Stellaris), constantly at war with everyone.
  Every neutral or abandoned node is held by the Scavs. Scav nodes are
  valued by their real worth like any other node; Scavs can hold large
  places and even HQs.
- **NCPD:** likely reframed in lore as weakened (the city is at war) so it
  becomes a real faction with limited holdings instead of being everywhere.

Political factions *within* gangs and corps (internal cliques, successions,
lieutenants) are to be represented. Design pending.

## 2. Territory: nodes and sub-districts

- **Node:** every meaningful place a faction holds counts toward territory (see
  [`venue-node-policy.md`](venue-node-policy.md) and
  [`node-garrison-and-assault.md`](node-garrison-and-assault.md)). Each node has
  exactly one controller (no co-owners), a **type** in
  `{economy, espionage, tech, military}` (big clubs, hotels, and open-air
  economy hubs fold into `economy`; garages and drug labs are `tech`), and a
  **size** in `{small, medium, large, very_large}` (with optional `is_hq`,
  `is_multi_type`, `is_logistics`, and `is_meeting_spot` flags). Security scales
  by size (`small` 6–10, `medium` 11–20, `large` 21–30, `very_large` 31–40,
  always including ≥ 1 Netrunner and 1 Boss). Small one-off shops, street
  corners, and venues that cannot hold a garrison are dropped from nodes (if
  mapped, kept as civilian-only venues). Dynamic events, patrols and convoys
  are presence only, not nodes.
- **Pillar resources & universal culture:** Every node produces its primary
  pillar output plus Influence (Politics: `small = 1`, `medium = 2`,
  `large = 3`, `very_large` or `is_hq = 5`) and **Culture**, scaled by node
  `size`. Cultural output is ordered by node type:
  **`economy > espionage > tech > military`**. Sub-district scarcity scaling
  (boosting yield when a sub-district has fewer nodes) is **deferred** until
  simulation testing shows whether it is needed.
- **Bosses & replacement:** Every non-HQ node is staffed by a **lieutenant
  boss**, and each territorial faction's active **Leader** (or Council chair)
  sits physically at its **HQ** (lore character at their largest/most
  meaningful node; no duplicate placements; dynamically generated otherwise).
  Any lieutenant, faction leader, or city politician can be killed and
  dynamically replaced; losing a lieutenant imposes a replacement cost on the
  owning gang/corp.
- **Connected capture:** important nodes cannot be taken directly. You must
  first secure the connected nodes around them, so an HQ cannot
  be walked into, turf and gang wars play out realistically, and control does
  not flip easily. Rule (agreed): nodes form an adjacency graph;
  a node is attackable only from an adjacent node you own; `small` and `medium`
  nodes are attackable directly; a `large` node is attackable only once its
  controller holds at most half of its adjacent nodes (its "guard ring"); an
  `is_hq` or `very_large` node needs all controller-held adjacent nodes taken
  first.
- **Sub-district holding:** a faction holds a sub-district when it owns
  ≥ 50% of the sub-district's total influence. Otherwise the sub-district is
  contested (anarchy). A tie is contested. Neutral/abandoned nodes count
  toward the total (they are Scav-held). A minimum total influence is
  required before a sub-district can be held. Holding a sub-district grants
  benefits (to be designed); sub-districts are not necessarily the whole
  territory system.

## 3. Player paths (later)

- Join a corp or gang and work up the ladder to leader.
- Stay independent: freelancer/fixer-style contract work driven by the
  simulation.
- Found a gang (deliberately hard; a level-1 nobody cannot):
  - take a Scav-held location given enough personal influence (Scavs
    retaliate, and other gangs may pre-emptively war a low-respect upstart);
  - or take a gang-owned location, which starts a war and needs money,
    recruits and some insurance (e.g. guarantor factions, or contracts that
    keep a territory uncontested).

## 4. Titles, claims and coring (agreed direction)

- Every node has one **controller** (who physically holds it:
  influence, spawns, pillar output) and an optional **title holder** (who
  has the legal/political claim). Title is a data field now; its mechanics
  come with the Politics pillar.
- Factions spend political influence to claim ground and gain title
  ("coring", a casus belli system).
- Factions can still fight border wars and hold nodes without title, at
  reduced efficiency/strength. That lets them damage rivals or avoid being
  steamrolled by a faction that starts to snowball.
- Corps should find it hard to gain territory but be strong at defending
  what they claim.

## 5. Leadership and internal politics (direction; design pending)

- Every faction and corp has a **Leader** and **sub-leaders**, plus internal
  blocs where lore has them (e.g. Royce vs Brick in Maelstrom; Valentinos,
  Tyger Claws and corps such as Arasaka have similar structures).
- A faction can be in **internal war** with no single leader. This must hurt
  the faction, and eventually one bloc wins and takes leadership.
- **Blocs are vassals.** A losing bloc is not absorbed or purged. Blocs keep
  influence over the faction even without territory and can start an
  internal turf war. Leaders must dole out nodes to blocs to keep
  them happy. Some political structures (archetypes) manage blocs better
  than others.
- **Rising in a faction:** a nobody starts as a grunt; nobody cares whom
  they back, but backing a leader can earn favour. Missions for a leader earn
  favour, which unlocks higher-tier (harder, more important) missions. At the
  top the player becomes a sub-leader with their own bloc, granted one
  node from the most powerful bloc. If that would drop that bloc
  below leadership control, the node comes from the second most powerful
  bloc instead; when tied blocs matter, pick between them with an even
  random roll.
- **Bloc stakes and muscle (agreed):** blocs have their own lieutenants and
  muscle (manpower; name TBD). A bloc loses satisfaction mainly when its own
  nodes are lost or threatened, its lieutenants die, or it loses muscle,
  especially defending another bloc's territory. Front-line blocs turn
  dovish while safe blocs stay hawkish.
- **Demand and severity (agreed):** every bloc has a demand (what it needs
  to stay content) and a severity (how hard it escalates when unmet).
  Policies can modify both. MaxTac is an NCPD bloc that can hold territory,
  with low demand and very high severity.
- **War support (agreed):** shown as one number, the influence-weighted
  satisfaction of the blocs. Below a threshold the leader must sue for peace
  or face a revolt; the winner's support caps its terms.
- **War settlement (agreed):** war goals are claims made before declaring;
  at peace the winner gains title to the war goals it holds; other captured
  nodes revert unless the winner's support lets it keep them as untitled
  occupations (reduced strength, upkeep, bloc drain); peace starts an
  automatic non-aggression pact; no coring during war.
- **Policies and government (agreed):** factions have policy slots with
  exclusive options and trade-offs. Government is one slot: the leadership
  model (autocracy, council, packs, collective) defaults from the archetype
  and can change in play, e.g. the Tyger Claws becoming a dictatorship.
  Changing it needs blocs with ≥ 50% of the faction's influence. Each pillar
  will have several policy slots (design for three or more). Policies
  modify other systems and bloc demand/severity.
- **Faction kinds (agreed):** one factions table with a kind (territorial,
  political, external).
- **Deferred:** spawning faction leaders, garrisons for HQs and major
  nodes (several flagship venues are empty with the campaign disabled),
  using the faction's own records or its spawn template. Corps with no named
  2077 head (Kang Tao, Biotechnica, Petrochem) get original Night City
  directors; Kang Tao's answers to the Chinese state.

## 6. Relations

- Four levels: **Allied, Friendly, Neutral, Hostile.**
- **No Allied at game start:** at most Friendly. Alliances are earned in play.
- **Anti-snowball coalitions:** factions near one that grows too fast drift
  toward Hostile with it.
- **Alliances carry obligations** (allies get pulled into each other's
  wars). What an alliance concretely provides waits until the economy and
  other pillar systems are designed.
- **Rivalry** is a flag on a pair, not a level: rivals start Neutral (or
  Hostile where attested) but coalition drift and casus belli between them
  are cheaper. A pair can be Hostile *and* rivals (Animals–Maelstrom).
- **Non-aggression pacts** are a state between factions (like being at
  war): they block war declarations for a duration and can be broken at a
  political cost. Tyger Claws–Mox start Hostile under a pact (the 2067 deal).
- **Trade with anyone:** hostile factions, Scavs included, can still trade.
  Hostility penalises trade. Trade will run through a generic deal system
  designed with the economy; no per-relation "kind" (supplier/buyer/…)
  labels.
- **War resolution:** both sides accumulate war pressure (exhaustion);
  losing raises it faster and eventually forces a settlement in which the
  winner takes the loser's legitimate claims. Design pending: the owner
  wants something better than a copy of Paradox's war score.
- **Starting matrix rules:** an attested stance beats a "no evidence"
  neutral placeholder; stances that exist only on story branches the
  timeline removes start Neutral and stay documented as history; Scavs are
  Hostile with everyone.
- **Personal standing:** the player has a personal relation with each
  faction, built by doing work for it. It gates access (see §10).

## 7. Alternate timeline (canon for this mod)

- The Konpeki heist and the Relic plot never happen, and neither do Phantom
  Liberty's Songbird/Space Force One events.
- Yorinobu Arasaka is alive. Arasaka's ship and Yorinobu's daughter are in
  the city.
- Kurt Hansen is alive and leads Barghest.
- Dexter DeShawn is alive (no heist) and still works as a fixer, based in
  the Afterlife back room.
- T-Bug is alive (no heist) and spends time with Dexter in the Afterlife
  back room.
- Songbird should still exist somewhere in the world (players want her);
  placement to be decided.
- **NUSA:** an external military/political special faction that influences
  the city in a special way (design pending; the owner will work out how it
  enters the game).

## 8. Companions and relationships (future)

- A companion/relationship system where characters such as Jackie Welles
  can roll with V.
- Johnny Silverhand later: e.g. a message that V was knocked out by Scavs
  and woke up with the chip in her head, but she is not dying. The hard part
  is making sure Johnny never references V dying.

## 8b. Resources (agreed direction)

| Pillar | Resource | Notes |
| --- | --- | --- |
| Politics | **Influence** | Every node grants Influence each turn; blocs add a base from their history and leader. Spent on claims, coring and policies. |
| Economy | **Eddies** | The base currency: military upkeep, keeping nodes loyal, hiring netrunners and contractors (freelancers/fixers, tied to missions), buying chips and cyberware. |
| Espionage | **Intel** | |
| Technology | **Research** (UI: **R&D**) | Drives a shared tech tree that decides what each faction can produce (e.g. Arasaka makes tier-5 weapons; gangs research higher tiers over time). |
| Military | **Muscle** (`manpower`) | Per bloc, regenerating from the military nodes each bloc controls; the faction's army is the sum, and the leader can draft from a bloc at a satisfaction cost. Plus **materiel** (weapons, vehicles, equipment, cyberware, drugs): stockpiled **per faction**, bought with eddies, capacity tied to technology. |
| Culture | none (projected force) | Culture nodes push **cultural pressure** into neighbouring nodes. A node's loyalty drifts toward the strongest pressure unless its controller garrisons it, spends eddies or adopts policies. Culture also feeds recruitment (manpower regeneration) and bloc contentment. |

- **Nodes and titles are tradeable** through the deal system (see
  [`economy-data-model.md`](economy-data-model.md)).
- **Upkeep deficits** drain both bloc satisfaction and node loyalty, more
  steeply the worse the deficit.
- **Coring does not mean loyalty.** A titled node still has to be
  garrisoned and kept content through policies or eddies, or it drifts
  toward another faction.
- One **turn** is 24 in-game hours.
- **No production system.** Industry is not a pillar and there is no
  materiel manufacturing simulation. Nodes with production revenue
  (`manufacturing`, `vehicles_chop`, `cyberware`, `drugs`, `arms`) only
  give a minor discount on the eddie cost of the matching materiel. Corps'
  global industry is off-map; their Night City branches run on their own
  budgets.
- **Shared tech tree** reused by every faction, with archetype and faction
  starting unlocks (e.g. Arasaka tier-5 weapons, Kang Tao smart weapons,
  Biotechnica bio/drugs, Maelstrom chrome). Technology strength speeds
  research. The tree decides the highest tier a faction can field; trade
  and alliances can raise what it can buy.

## 9. Factions outside the territory game

- **Kang Tao** is a full territorial faction.
- **External powers** (the Chinese state, NUSA, NetWatch, SovOil) shape
  relations without holding territory. NetWatch and NUSA exist in-game, so
  they can field assault squads via spawn templates like the corps. Whether
  they live in the factions table (with a kind/flag) or a separate table is
  under discussion.
- Places owned by unmodeled factions (Trauma Team, Afterlife, Orbital Air,
  Zetatech, NetWatch) are not nodes, but their locations are
  stored for later use as externals or factions. Fixers' locations are not
  needed. Alternate-history idea: Trauma Team folded into NCPD.
- **Scanner labels** must show the faction an NPC belongs to (e.g. a
  Petrochem guard spawned from a Militech template reads Petrochem).

## 10. Access and gigs

- **No vanilla gigs, ever.** The player gets access to faction content
  through the mod's own gates (missions for a faction, personal standing).
- **Every location accessible** to V and NPCs (doors, areas), except places
  that would not exist in this timeline (e.g. the nomad-camp tent after
  Panam's story). Owner 2026-11-26: Joss Kutcher's trailer park and Kurt
  Hansen's places stay; both people exist in the timeline even though their
  quests never run.
- **Door policy:** doors are closed by default but usable (enabled and
  powered; unlocked only when there is otherwise no way through). Doors with
  an in-world way to open them (a terminal, a keycard placed in the world,
  hacking, a Technical or Body check) stay exactly as vanilla. Quest
  infiltration routes we preserve for missions (e.g. the Black Sapphire
  sneak-in) are opened end to end.

## 11. Architecture

The mod owns its world model in `world.db` rather than steering vanilla
through flags and triggers. That stays the long-term architecture.

Ascendancy runs are fully decoupled from the story campaign: a run always
starts fresh via *Start Ascendancy*. Existing story saves are not loaded,
converted or repaired, so no system needs a "fix up an old save" path.
