# Territory Data Model — Territory Nodes (spec draft)

Status: draft for review, 2026-11-25. Implements the territory parts of
[`gameplay-systems.md`](gameplay-systems.md). Built from the per-faction
research in [`docs/research/factions/`](../research/factions/). Nothing here
is implemented yet. It replaces the generic 96-sub-territory grid
(`sub_territories`, `control_centers`, `landmarks`, `faction_headquarters`
and the `is_active` test flag).

Principles: static facts live in `world.db`; mutable state lives in the
playthrough DB; rules are pure functions in `native/lib/sim`; one decision
lives in one place.

## 1. Concepts

| Term | Meaning |
| --- | --- |
| **Node** | A meaningful, capturable place a faction holds (see [`venue-node-policy.md`](venue-node-policy.md) and [`node-garrison-and-assault.md`](node-garrison-and-assault.md)). The unit of capture. Exactly one controller. |
| **Size** | `small` (6–10 security, influence 1), `medium` (11–20, influence 2), `large` (21–30, influence 3), `very_large` (31–40 multi-type flagship HQs, influence 5). Any node with `is_hq = 1` carries influence 5. |
| **Type** | The node's primary pillar focus: `economy` (markets, open-air hubs, businesses, clubs, hotels, logistics, ownable executive buildings), `espionage` (netrunner dens, server rooms, relay/intel hubs), `tech` (garages, chop shops, drug labs, workshops, clinics, power/utility facilities), `military` (strongholds, garrisons, precincts, checkpoints, depots). Every node also outputs Influence (Politics) and **Culture** (`economy > espionage > tech > military`), and always has ≥ 1 Netrunner. |
| **Boss** | Every non-HQ node has 1 lieutenant boss; each faction's active **Leader** (or Council chair) sits at its HQ (lore character at largest/most meaningful node, otherwise dynamically generated). Killable and replaceable at a cost to the owning faction. |
| **Controller** | The faction physically holding a node. Drives influence, spawns and pillar output. |
| **Title holder** | Optional. The faction with the legal/political claim. Holding without title runs at reduced efficiency. Mechanics come with the Politics pillar. |
| **Bloc** | An internal political faction (vassal) inside a faction, with a leader. A node may be assigned to one of its controller's blocs. |
| **Sub-district** | Vanilla `gamedataDistrict` sub-district. Its holder is derived from influence (§4). |
| **Presence** | Evidence of a faction's activity (patrols, dynamic events, quest communities) that is not a node. Used for ambient spawns and heat, never for influence. |

Territorial factions: Tyger Claws, Valentinos, Arasaka, Militech, Kang Tao,
Biotechnica, Petrochem, Barghest, 6th Street, NCPD, Aldecaldos, Wraiths,
Animals, The Mox, Maelstrom, Voodoo Boys, Scavs. Night Corp and the
Government of Night City are political-only (no nodes). Places of any other
faction are dropped.

**Fixers are not nodes** (owner 2026-11-26). Fixer locations (the Afterlife,
Wakako's parlour, Mr. Hands' club and the like) hold their own ground, and
fixers are neutral in the lore. They stay as venues, but no faction captures
or controls them. Candidate nodes are listed with reasoning in
[`territory-node-candidates.md`](territory-node-candidates.md).

## 2. Static tables (`world.db`, schema v3)

### `factions` (extended)

Political columns (`kind`, archetype, pillars, government,
`spawn_template_faction_id`, `attitude_group`) are defined in
[`politics-data-model.md`](politics-data-model.md) §2. Only factions with
`kind = territorial` own nodes. `attitude_group` is the CName
for runtime re-tagging via `AttitudeAgent.SetAttitudeGroup`
(`refs/cyberpunk/orphans.swift:20451`).

### `sub_districts`

`sub_district_id`, `gamedata_district` (enum name), `district_id`,
`display_name`, `min_hold_influence`. Node membership comes from
attribution (§5), not from geometry. Map polygons are a later visual concern.

### `territory_nodes`

| Column | Notes |
| --- | --- |
| `node_id`, `code`, `display_name` | `code` is stable across builds. |
| `size` | `small`, `medium`, `large`, `very_large`; drives `influence` and garrison sizing. |
| `node_type` | Pillar focus: `economy`, `espionage`, `tech`, `military`. |
| `is_hq`, `is_multi_type`, `is_logistics`, `is_meeting_spot` | Capability/role booleans (see [`node-garrison-and-assault.md`](node-garrison-and-assault.md)). |
| `influence` | Derived from size/HQ: `small = 1`, `medium = 2`, `large = 3`, `very_large` or `is_hq = 5`. |
| `sub_district_id` | Required. |
| `x, y, z` | From a cited extract record only (site anchor, guard area, community, marker). Never a centroid. |
| `interior` | Bool, proven from node names. |
| `initial_controller_faction_id` | Required. Neutral/abandoned → Scavs. |
| `initial_title_faction_id` | Nullable. |
| `initial_bloc_id` | Nullable; must belong to the controller. |
| `site_id` | Nullable link to `sites` for capture content (guards, patrols, doors, communities). |
| `pillar_economy … pillar_politics` | Six small ints; all 0 unless meaningful. |
| `is_named` | Lore place (yield balancing) vs filler. |
| `source`, `confidence` | Provenance (record + research doc) and tag. |

Child tables: `node_revenue (node_id, stream_code)` using the
shared vocabulary in `docs/research/factions/METHOD.md` §7, and
`node_communities (node_id, community_hash)` for capture spawns.

### `node_links` (adjacency)

`node_a < node_b`, `distance_m`, `crosses_sub_district` (bool). Built by
the generator (§5), undirected.

### Blocs, leaders, relations, policies

Defined in [`politics-data-model.md`](politics-data-model.md). A node's
`initial_bloc_id` references `blocs`.

## 3. Playthrough state (mutable)

- Per node: `controller_faction_id`, `title_faction_id`, `bloc_id`,
  `strength` (garrison/defence, 0–100).
- Faction, bloc, relation, war, pact and claim state: see
  [`politics-data-model.md`](politics-data-model.md) §3.
- Not stored, derived: sub-district holders, faction influence totals,
  attackable sets. Cache them only if profiling demands it.

This is a breaking playthrough-schema change. Per `docs/versioning.md`,
existing test saves reset their territory; document it in `CHANGELOG.md`.

## 4. Rules (pure functions, `native/lib/sim`)

1. **Sub-district holder:** sum `influence` per controller over the
   sub-district's nodes. The holder is the faction with ≥ 50% of the total,
   provided the total ≥ `min_hold_influence`. A tie, or no faction reaching
   50%, means contested. Scav-held nodes count toward the total.
2. **Attackable:** a node is attackable by faction F only if F controls an
   adjacent node (`node_links`).
3. **Guard ring:** `small` and `medium` nodes are attackable directly from any
   adjacent owned node. A `large` node is attackable only once its controller
   holds ≤ 50% of its adjacent nodes. An `is_hq` or `very_large` node needs all
   controller-held adjacent nodes taken first.
4. **Title efficiency:** a node whose controller lacks title produces
   pillar output and strength at a reduced multiplier (value TBD).
5. **Leadership, blocs, wars, peace, policies, relations and the sub-leader
   grant:** see [`politics-data-model.md`](politics-data-model.md) §4.

## 5. Generator (`tools/build-territory-map.py`)

A deterministic build step, like `build-world-db.py`, that writes `data/`
seeds. Inputs:

- the extract: `dist/extract/*.jsonl`, `data/sites/*.json`;
- the research JSON blocks in `docs/research/factions/*.md` and
  `docs/research/factions/politics/*.md` (evidence);
- `data/territory/overrides.json` (owner decisions, e.g. Old Maglev Tunnel →
  Voodoo Boys, Northern Oil Fields → Petrochem, Night Corp places → NCPD,
  dropped factions, relation conflicts).

Steps:

1. **Candidates:** every site, every research control point, every named
   marker or community the research cites.
2. **Classify** each community area into node evidence vs presence
   (`ma_`/`sts_`/site communities → nodes; `cs_`/`de_`/patrols → presence;
   `q###` quest communities → identity only).
3. **Cluster** same-faction evidence within ~75–100 m into one node.
4. **Attribute faction** with the METHOD §1.2 item 1 precedence and its
   pitfalls (roster dedupe by community hash, machines are not a garrison,
   look-alike traps). Assign Scavs where no territorial faction is present.
   Drop non-territorial owners.
5. **Scale, type and influence:** research and overrides first, then rules:
   `hq` from research; `business`/`landmark` from named research nodes;
   `stronghold` for large garrisons or camps; `outpost` for guard areas or
   patrols; otherwise `hangout`. Thresholds are tunable constants in one
   place.
6. **Sub-district:** attribution precedence. Dogtown and Badlands need a
   decision (§6).
7. **Adjacency:** connect neighbours within a district (Gabriel graph or
   k-nearest, max edge ~300–400 m in the city, longer in the Badlands), plus
   cross-sub-district edges.
8. **Validate:**
   - every coordinate traces to a record;
   - no centroid snaps;
   - every node has a sub-district;
   - each district graph is connected;
   - exactly one HQ per territorial faction except Scavs;
   - no `allied` relations;
   - relation conflicts resolved.
9. **Review artifact:** a rendered map of nodes, owners and holders, so the
   owner can check it before anything ships.

## 6. Open questions

1. ~~Dogtown and the Badlands~~ **Decided: split them.** Use the vanilla
   `gamedataDistrict` records as sub-districts: Badlands → Biotechnica Flats,
   Dry Creek, Jackson Plains, Laguna Bend, Las Palapas, North Sunrise Oil
   Field, Rattlesnake Creek, Red Peaks, Rocky Ridge, Santa Clara, Sierra
   Sonora, SoCal Border Crossing, Vasquez Pass, Yucca (`Badlands_Spaceport`,
   `_YuccaGarage` and `_YuccaRadioTower` are locations, not sub-districts);
   Dogtown → Akebono, Brooklyn, Capitan Caliente, Cynosure, Expo
   (`Dogtown_Hideout` and `Dogtown_Worldmap_Sub` excluded). Open sub-task:
   assigning nodes to them needs the district trigger areas from the
   extract, or the runtime `PreventionSystem.GetCurrentDistrict()` probe.
2. **Vanilla gang lists per sub-district** (`District_Record.Gangs()`): read
   them with a one-time dev CET probe to sanity-check computed starting
   holders?
3. **Clustering radius** and scale thresholds: tune against the review
   map.
4. **Pillar output formula** per scale, type and revenue stream (needs the
   economy design).
5. **Untitled efficiency** multiplier and **bloc satisfaction** model (need
   the politics design).
6. **Patron/client direction** is kept as flavour (`kind`) only. Enough?

## Node anchors (candidates for the dynamic garrison)

`data/territory/node_anchors.json` holds, for each of the 123 nodes, the
anchors `docs/design/node-garrison-and-assault.md` section 5 asks for. It is
built by `tools/extract-node-anchors.py` (`--check` for drift) from local
research extracts: the venue catalogue, the mine-venues sector AI-spot index,
the device registry, the lift audit and `data/roads/nodes.json`.

Anchors are **candidates**, not proven placements. Each one carries a
`confidence` (`vanilla` as found, `derived` computed from vanilla data,
`generated` placed by rule) and a `source`. The garrison spike and the sweep
validate them in game. The fields per node:
- `id`, `catalogue_venue`: the classification id and the catalogue venue
  key (two aliases: Black Sapphire, Ho-Oh).
- `area`: the first tour stop's centre and radius. Spots count as inside
  when they are within any of the venue's stops (Arasaka Tower spans three),
  horizontally, and within 35 m vertically.
- `guard_posts[]`: vanilla guard community spots, plus sector AI spots
  whose workspot file reads as `guard` or `idle_stand` (`spot_kind`). Sit,
  work, civilian and unknown spots are not posts. They are capped at 3× the
  size's maximum headcount, picked for spread across rooms and floors.
- `boss_seat`: a vanilla boss, lieutenant or miniboss spot; otherwise the
  work or sit spot deepest from the main breach point (`derived`).
- `patrol_splines[]`: generated loops through posts on one floor. No
  vanilla spline points are in the index yet.
- `breach_points[]`: the 1–2 doors farthest from the area centre.
- `staging`: a road-graph node 35–60 m from the breach point, outside the
  area.
- `interior_waypoints[]`: up to three posts nearest the line from the
  breach point to the boss seat.
- `lift_links[]`: usable lift cars in the area (lift exclusions applied),
  with their floors, the floors nearest the breach and the boss seat, and
  a cab capacity of 4.
- `capacity`: posts plus patrols against the size's minimum headcount. The
  10 nodes short of it are listed in the file and need generated posts or a
  larger area.
