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

Special factions:

- **Night Corp:** unscoped. Model the city's political leaders and Night
  Corp. Whether it becomes a full faction is undecided; treat it as one for
  research.
- **Scavs:** rebels/pirates, the unaligned faction (like rebels in Mount &
  Blade or pirates in Stellaris). Every neutral or abandoned point is held by
  the Scavs.
- **NCPD:** likely reframed in lore as weakened (the city is at war) so it
  becomes a real faction with limited holdings instead of being everywhere.

Political factions *within* gangs and corps (internal cliques, successions,
lieutenants) are to be represented. Design pending.

## 2. Territory: influence points and sub-districts

- **Influence point:** every place a faction holds counts toward territory:
  corners, small spawns, outposts, businesses, HQs. Each has an integer
  influence and a category such as HQ, Business, Stronghold, Outpost or
  Hangout (list not final).
- **Pillar resources:** only *meaningful* influence points produce pillar
  resources (cultural, economic, espionage, military, political): businesses,
  HQs, places with meaningful interiors, large community spawns, and
  meaningful lore locations (an open market, a prominent alley group). Minor
  points add influence only.
- **Connected capture:** important points cannot be taken directly. You must
  first secure the connected influence points around them, so an HQ cannot
  be walked into, turf and gang wars play out realistically, and control does
  not flip easily.
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
