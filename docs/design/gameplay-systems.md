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
Zetatech, NetWatch, the fixers, …) are dropped as influence points.

Special factions:

- **Night Corp and the Government of Night City:** special political
  factions with no territory. They influence the political simulation (how
  is not yet designed). The game has no Night Corp affiliation, so places
  tied to Night Corp go to NCPD.
- **Scavs:** rebels/pirates, the unaligned swarm faction (like rebels in
  Mount & Blade or pirates in Stellaris), constantly at war with everyone.
  Every neutral or abandoned point is held by the Scavs. Scav points are
  valued by their real worth like any other point; Scavs can hold large
  places and even HQs.
- **NCPD:** likely reframed in lore as weakened (the city is at war) so it
  becomes a real faction with limited holdings instead of being everywhere.

Political factions *within* gangs and corps (internal cliques, successions,
lieutenants) are to be represented. Design pending.

## 2. Territory: influence points and sub-districts

- **Influence point:** every place a faction holds counts toward territory:
  corners, small spawns, outposts, businesses, HQs. Each has exactly one
  owner (no co-owners) and an integer influence by category: Hangout 1,
  Outpost 2, Landmark 3, Stronghold 3–4, Business 3–4, HQ 5. Dynamic events,
  patrols and convoys are presence only, not points.
- **Pillar resources:** only *meaningful* influence points produce pillar
  resources (cultural, economic, espionage, military, political): businesses,
  HQs, places with meaningful interiors, large community spawns, and
  meaningful lore locations (an open market, a prominent alley group). Minor
  points add influence only.
- **Connected capture:** important points cannot be taken directly. You must
  first secure the connected influence points around them, so an HQ cannot
  be walked into, turf and gang wars play out realistically, and control does
  not flip easily. Rule (agreed): influence points form an adjacency graph;
  a point is attackable only from an adjacent point you own; a Business,
  Stronghold or HQ is attackable only once its owner holds at most half of
  its connected points (its "guard ring"); an HQ needs its whole ring taken.
- **Sub-district holding:** a faction holds a sub-district when it owns
  ≥ 50% of the sub-district's total influence. Otherwise the sub-district is
  contested (anarchy). A tie is contested. Neutral/abandoned points count
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

- Every influence point has one **controller** (who physically holds it:
  influence, spawns, pillar output) and an optional **title holder** (who
  has the legal/political claim). Title is a data field now; its mechanics
  come with the Politics pillar.
- Factions spend political influence to claim ground and gain title
  ("coring", a casus belli system).
- Factions can still fight border wars and hold points without title, at
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
  internal turf war. Leaders must dole out influence points to blocs to keep
  them happy. Some political structures (archetypes) manage blocs better
  than others.
- **Rising in a faction:** a nobody starts as a grunt; nobody cares whom
  they back, but backing a leader can earn favour. Missions for a leader earn
  favour, which unlocks higher-tier (harder, more important) missions. At the
  top the player becomes a sub-leader with their own bloc, granted one
  control point from the most powerful bloc. If that would drop that bloc
  below leadership control, the point comes from the second most powerful
  bloc instead; when tied blocs matter, pick between them with an even
  random roll.
- **Alternate timeline:** Yorinobu Arasaka is alive. Arasaka's ship and
  Yorinobu's daughter are in the city.
- **Deferred:** spawning faction leaders. With the campaign disabled, most
  named leaders are story-only, so the mod must spawn them itself.

## 6. Relations

- Four levels: **Allied, Friendly, Neutral, Hostile.**
- **No Allied at game start:** at most Friendly. Alliances are earned in play.
- **Anti-snowball coalitions:** factions near one that grows too fast drift
  toward Hostile with it.
- **Alliances carry obligations** (allies get pulled into each other's
  wars). What an alliance concretely provides waits until the economy and
  other pillar systems are designed.

## 7. Architecture

The mod owns its world model in `world.db` rather than steering vanilla
through flags and triggers. That stays the long-term architecture.
