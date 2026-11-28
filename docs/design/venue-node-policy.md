# Venue & Node Classification Policy

Status: agreed direction (owner, 2026-11-27). Single source of truth for
automated venue classification, node typing/sizing, boss placement, cast
pruning, and resolving `docs/design/owner-decisions.md`.

Companion specs: [`gameplay-systems.md`](gameplay-systems.md),
[`territory-data-model.md`](territory-data-model.md),
[`politics-data-model.md`](politics-data-model.md),
[`economy-data-model.md`](economy-data-model.md).

---

## 1. Classification buckets

Every mapped venue (and shortlisted hustle site) falls into exactly one bucket:

| Bucket | Meaning | Population rule |
| --- | --- | --- |
| `node` | Participates in territory control, capture, pillar output, and faction occupation. | Staff/crowd (if public-facing) + **5+ neutral-until-provoked security garrison** + **1 lieutenant boss**. |
| `civilian_venue` | Already mapped, but does not fit the node system. Kept as living world scenery or vendor space. | **Civilian population only** (ambient patrons, residents, vendors). Strip gang/security garrisons, bosses, and hostile restricted-area crews. |
| `neutral_hub` | Protected non-capturable hub required by a gameplay system: **Fixer HQs**, **Companion homes**, or **Neutral service orgs** (Delamain HQ). | System-owned (fixers static in `cast_and_hubs`; companions despawn from home while rolling with V). Never flips. |
| `excluded` | Unremovable campaign/gig lore implications (Space Force One crash, Cynosure bunker, Spidertank arena, submerged Laguna Bend) or empty street-corner / road-staging wrappers with nothing to restore. | Excluded / sealed as vanilla leaves it. |

---

## 2. Strict criteria for a `node`

A venue is a `node` if and only if **all four** conditions hold:

1. **Meaningful pillar role:** It plausibly operates as an asset in one of the
   four node types:
   - **`economy`** — markets, **open-air commercial/economy hubs** (e.g.
     Jig-Jig Street, Cherry Blossom Market), businesses, nightclubs/bars (big
     clubs fold into `economy`), hotels/motels, casinos, chop shops, automotive
     repair/gas stations with garages, logistics hubs (container yards, freight
     depots, docks, warehouses), ownable upscale real-estate / apartment
     buildings (e.g. Peralez apartment building, Lobos St. tower, Gutierrezes'
     penthouse — upscale civic/residential towers with no gang owner default to
     **NCPD** rather than Scavs; someone owns the building and the node boss
     sits in the penthouse/apartment).
   - **`espionage`** — netrunner dens, server rooms, relay towers, BD/media
     studios used for intel/blackmail, wiretap/intel offices.
   - **`tech`** — ripperdoc clinics/labs (large enough to guard), pharma/chem
     labs, R&D outposts, cyberware/arms workshops, power/utility/forensic
     facilities.
   - **`military`** — gang strongholds, fortified compounds, corp security
     bases, detention centers/prisons, precincts, checkpoints, arms staging
     depots, large occupied gang hideouts with no more specific purpose.
2. **5+ security garrison test:** The physical space must plausibly support
   everyday staff, a **security team of 5 or more**, and a **lieutenant boss**
   without looking absurd. Small one-off shops, street corners, single-room
   flats, coffee carts, and tiny alleys fail this test → `civilian_venue` or
   `excluded`.
3. **Lore-clean:** Story-only wreckage, corpses, hostages, ambush waves, mines,
   and quest props can be removed or toggled off so the location reads as a
   normal, ownable 2077 asset.
4. **Not a protected neutral hub:** Fixers (Afterlife, Wakako's, Padre's,
   Regina's, Dakota's, Dino's, El Capitán's, Heavy Hearts), companion homes,
   and Delamain HQ are `neutral_hub`, never nodes.

### Universal cultural output & node size

- **No separate `culture` node type.** Big clubs, bars, shrines, and social
  venues with 5+ security fold into `economy` (or `military` if primarily a
  stronghold).
- **Every node produces Culture**, ordered by node type:
  `economy > espionage > tech > military`.
- **Node size:** every node gets a `size` in `{small, medium, large}`:
  - `large` — flagship HQs, major complexes, megaclubs, malls, hotels,
    industrial parks, stadiums (e.g. Totentanz, Clouds, Arasaka Tower,
    Black Sapphire, Konpeki Plaza, Grand Imperial Mall, All Foods, EBM
    Stadium).
  - `medium` — full standalone businesses, warehouses, container yards,
    garages/chop shops, mid-sized clubs, clinics, apartments/towers,
    compounds (e.g. Ho-Oh, 7th Hell, Empathy, Biotechnica Hotel, Revere
    Courier, Peralez apartment building, El Pinche Pollo, Deravaja Dojo).
  - `small` — compact outposts, small chop-shop gas stations, relay stations,
    smaller fortified dens or single-floor gang hideouts that still support 5+
    guards + a lieutenant boss.
- Output scales directly from `size` (`small / medium / large`). Per-subdistrict
  scarcity multipliers are **deferred** until simulation testing shows whether
  they are needed.

---

## 3. Boss placement & conflict resolution

- Every node is staffed by **1 lieutenant boss** (plus security and staff).
- A **lore character** (canonical gang/corp leader, sub-leader, or lieutenant)
  may sit as the node's initial boss **only if** they are not placed at another
  node.
- **Conflict rule:** If a lore character could sit at two nodes, they sit at
  the **larger, more meaningful node** (e.g. Sasquatch at Grand Imperial Mall
  rather than Tripple Xtreme; Brigitte at Elders' Lair rather than the Chapel;
  Kurt Hansen at Black Sapphire). The secondary node gets a **scoped /
  dynamically generated boss**.
- **Death & capture replacement:** Any faction leader, lieutenant boss, or
  politician can be killed or displaced when a node flips and is replaced by
  the simulation's dynamic character generator. Losing a lieutenant imposes a
  replacement cost on the owning gang/corp (eddies + political influence /
  bloc satisfaction hit).

---

## 4. Cast policy (who stays in static clean-slate spawns)

Only four groups are statically cared about at game start:
1. **Companions** — owned by the companion layer; sit at their home hubs and
   despawn from home while accompanying V.
2. **Fixers** — static in `cast_and_hubs.json` at their neutral fixer HQs.
3. **Faction cast** — canonical leaders, sub-leaders, and node lieutenants
   belonging to one of the 17 territorial factions (and their guards/staff).
4. **Prominent city politicians (3-way mayoral structure)** —
   - Incumbent Mayor (**pro-corp [NCPD counts as corp] / anti-gang**),
   - Jefferson Peralez (**anti-corp federalist / anti-gang**),
   - Third candidate (**pro-gang / anti-corp**).
   Handled by the political simulation (assassination contracts by V or AI
   freelancers, discovery penalty, immediate replacement, and for the Mayor:
   nulled sim effects + special election 1 week / 7 turns later).

**Side-job & gig characters:** Removed from static venue placements unless they
genuinely belong to one of the four groups above (e.g. a canonical faction
lieutenant running a faction node). One-off gig targets, victims, hostages, and
side-job civilians are dropped; dynamic character generation supplies
replacement bosses, politicians, and future mission targets. Neutral contracts
on non-nodes are **deferred** until the core simulation is working.

---

## 5. Automated resolution defaults (for `owner-decisions.md`)

When classifying venues and settling pending `owner-decisions.md` items:
- **Lighting:** Always on (owner #40).
- **Access (doors & lifts):** Usable everywhere except lore-excluded venues and
  vanilla-unusable lift floors (owner #24, #25, #58, playbook rule 13).
- **Attitude:** All node garrisons spawn **neutral until provoked**; hostility
  is determined by V's affiliation and faction standing (owner #27–30, #78).
- **Quest dressing:** Corpses, hostages, mines, blood decals, ambush/reinforcement
  waves, and gig escape cars stay **OFF**. Everyday ambient vehicles, vendors,
  and calm staff stay **ON**.
- **Ambiguity discipline:** Classifying agents must reason through **both** the
  case FOR a venue being a node and the case AGAINST it before deciding.
  `undecided` is reserved for genuinely balanced edge cases and must stay small
  (<10% of venues; if it grows larger, tighten the rules above and re-run).
