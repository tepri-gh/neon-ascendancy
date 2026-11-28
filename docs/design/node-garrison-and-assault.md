# Node Garrison, De-Scaling, Assault AI & Convoy Design

Status: **agreed design spec** (owner, 2026-11-28). Settles open items S1–S8 and
S10 from [`node-staffing.md`](node-staffing.md) and defines how territory nodes
are populated, scaled, guarded, assaulted, and supplied.

Companion specs: [`venue-node-policy.md`](venue-node-policy.md),
[`territory-data-model.md`](territory-data-model.md),
[`economy-data-model.md`](economy-data-model.md),
[`gameplay-systems.md`](gameplay-systems.md),
[`../research/living-world-site-modeling.md`](../research/living-world-site-modeling.md).

---

## 1. Node sizes & garrison composition (S1, S2, S6)

Every node stays **one node per building/site** (one map pin, one controller,
one capture fight). Flagship multi-type headquarters use a fourth size tier,
**`very_large`**, which outputs across multiple pillars and zones its garrison
by floor/wing to stay within AI performance budgets.

### Headcount & role mix (civilian crowds are separate; boss included)

**Hard rule:** every node **always has at least 1 Netrunner**, regardless of
node type. Military nodes lean toward the top of each range (+25–30% within the
cap).

| Size | Total Security | Netrunners | Specialists & Elites (Heavies / Snipers / Elites) | Rank-and-File Guards | Boss | Posts vs Patrols |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| **`small`** | **6–10** | **1** | 0–2 | 4–6 | 1 Lt (`Elite` tier) | ~75% posts / ~25% patrol |
| **`medium`** | **11–20** | **1–2** | 2–5 | 7–12 | 1 Lt (`Boss` tier) | ~65% posts / ~35% patrol |
| **`large`** | **21–30** | **2–3** | 5–8 | 13–18 | 1 Lt (`Boss` tier + 2 Elite guards) | ~60% posts / ~40% patrol |
| **`very_large`** *(multi-type HQs)* | **31–40** *(zoned)* | **3–4** | 8–12 | 18–23 | 1 HQ Boss + 1–2 Sub-Lts | ~50% posts / ~50% patrol (per zone) |

- **Node-type role bias:**
  - `military`: top of headcount range; extra Heavies, Snipers, and Elites; denser patrol loops.
  - `espionage`: extra Netrunners (top of netrunner range) + stealth/fast-ranged guards; minimal heavies.
  - `tech`: tech-weapon specialists + netrunners; gig-staged robot mobs stay off at generic nodes (policy §5).
  - `economy`: bouncers/guards at chokepoints + Elites near VIP/boss office + civilian crowd scaled by size (`small` 4–8, `medium` 10–18, `large` 20–35).
- **Netrunners outside espionage (S6):** Every netrunner slot on a non-espionage
  node contributes a per-netrunner **Intel** bonus (e.g. `+1 Intel/turn` per
  netrunner), while `espionage` nodes still produce the bulk of Intel via their
  base node output + higher netrunner count.
- **Civilian crowds & club hours (S7):** Calm vanilla/quest party crowds may be
  reused at empty clubs (Empathy, Ho-Oh, 7th Hell) scaled to node size. Clubs
  stay open 24/7 until core simulation work is complete.

---

## 2. Node types, tags & Tyger Claws HQ (S3, S4, S5, S10)

Keep the **four node types** (`economy`, `espionage`, `tech`, `military`) and
universal Culture ordering (`economy > espionage > tech > military`):

- **Garages, auto shops & chop shops → `tech` (S5).** Balances distribution
  away from `economy` toward `tech` (and still feeds `vehicles_chop` materiel
  discounts).
- **Major drug labs → `tech` (S4)** (chemical/pharma synthesis; feeds `drugs`
  materiel discounts).
- **`is_logistics` tag (S3):** Applied to freight/container yards, docks,
  ports/marinas, courier depots, rail/bus yards, border crossings, and major
  supply warehouses (typically `economy`, or `military` for arms depots), **and
  to every Megacorp HQ** (`Arasaka Tower`, `Militech Offices`, `Kang Tao
  Building`, `Biotechnica Protein Flats`, `Petrochem North Sunrise Oil Fields`
  — corporate branches have industrial shipping yards, AV freight hangars, or
  underground loading docks so no megacorp starts with 0 logistics).
  - **Convoys** route from a faction's `is_logistics` nodes to its other nodes
    (driving "Intercept / Kill Convoy" dynamic missions).
  - **Zero-logistics penalty:** Any faction holding **0 logistics nodes**
    suffers a severe **Supply Chokepoint** penalty (materiel cost spike +
    reduced garrison reinforcement/recovery), **unless** it buys a recurring
    **Logistics Access Deal** from a **Friendly or Allied** faction that holds
    at least one logistics node.
- **`is_meeting_spot` tag:** Applied to upscale/private VIP venues (Peralez
  Apartment, Slayton's Apartment, Gutierrezes' Penthouse, Tucker Albach's Condo,
  Embers, Konpeki Plaza, and Hiromi Sato's Megabuilding H8 Penthouse
  `#sq026_pr_hiromi` once split out as a `small` node). These remain normal
  ownable `economy` nodes **and** serve as target pools for dynamic
  **assassination, espionage/wiretap, and political meeting** missions.
- **Tyger Claws HQ (S10):** **Ho-Oh** (`loc_sts_wat_kab_07`, 3 floors + garage,
  street-accessible) is the Tyger Claws HQ. **Clouds** (`loc_q105_dollhouse`)
  becomes a regular `medium` `economy` business node under Woodman; Hiromi's H8
  Penthouse (`#sq026_pr_hiromi`) is scoped as a separate `small` `meeting_spot`
  node rather than an HQ.

---

## 3. World de-scaling & high-level challenge

Vanilla 2.5 scales almost every open-world enemy via
`powerLevelMod = "Character.ScaleToPlayerLevel"` feeding `BaseStats.PowerLevel`
(which drives Health, DPS, and Resistances via curves in `primary_stats.tweak`).

### Fixed simulation-driven `PowerLevel`
All Neon Ascendancy garrison records **omit `ScaleToPlayerLevel`** and receive
an explicit `BaseStats.PowerLevel` (via TweakXL / `StatsSystem` on spawn):

```text
PowerLevel = FactionTierBase + RarityOffset + SizeOffset   (clamped to [10, 65])
```

- **Faction Fielded Tier base (1–5):**
  - Tier 1 (Scavs / weak gangs): `14`
  - Tier 2: `22`
  - Tier 3 (mid syndicates/gangs): `32`
  - Tier 4 (strong gangs / Barghest): `44`
  - Tier 5 (Arasaka / Militech / Kang Tao / late-game researched factions): `54`
- **Rarity offset:** Normal `+0`, Specialist (Netrunner/Heavy/Sniper) `+3`,
  Elite `+6`, Boss `+10`.
- **Size offset:** `small +0`, `medium +2`, `large +5`, `very_large +8`.

### Keeping nodes challenging at both low and high player level
- **Low-level V (Lv 1–15):** Cannot solo `medium+` or corp nodes; must rely on
  **allied faction assault squads** to take territory.
- **High-level V (Lv 50–60):** Weak Scav dens stay appropriately weaker, while
  serious nodes stay dangerous through four non-sponge mechanics:
  1. **Guaranteed Netrunner(s) on every node** applying overlapping upload/trace
     pressure (Cyberware Malfunction, Weapon Glitch, Overheat) + security cams.
  2. **Tier 4–5 Elite & Boss kits:** Sandevistan/Kerenzikov Elites matching V's
     speed, `WillCounterHack`, and quickhack/takedown-resistant Bosses.
  3. **Connected-Node QRF Reinforcements:** Attacking a node whose controller
     still holds adjacent nodes (`node_links`) starts a short alarm timer
     (45–60s unless the node's netrunner/officer is neutralized) that calls a
     4–8 unit QRF squad from a neighbouring friendly node — making cutting the
     guard ring feel tangible in combat.
  4. **Faction Tech Progression:** Surviving factions research up the shared
     tech tree over the campaign, raising their Fielded Tier and gear quality.

---

## 4. NPCs: appearances, weapons, affiliation, elites & bosses

Vanilla `.community` files hardcode one faction's `characterRecordId` and cannot
swap factions when territory flips. Every node therefore splits cleanly into:
1. **Static Clean-Slate Layer:** geometry, doors/lifts, lighting, music/DJs,
   and **civilian/vendor crowds** (vanilla communities).
2. **Dynamic Garrison Layer (sim-owned):** controller-driven security,
   specialists, elites, and boss spawned from **TweakXL** faction templates.

### TweakXL Faction Template Matrix
- **Appearances & variety:** Inherit each faction's vanilla `$base`
  `entityTemplatePath` (`ma`/`wa`/`mb` bodies) and `visualTags` (`Lvl1`/`Lvl2`/`Lvl3`,
  faction sub-styles) so spawned squads randomize outfits naturally.
  - Thin vanilla rosters (**Kang Tao**, **The Mox**, **Aldecaldos**) add TweakXL
    role clones inheriting their own faction base `.ent`.
  - Record-less factions (**Biotechnica**, **Petrochem**) clone corp/Militech
    `.ent` bases and override `affiliation`, `baseAttitudeGroup`, `visualTags`,
    and `displayName` so **the scanner accurately reads Petrochem / Biotechnica**.
- **Weapons & Gear Brackets:** Each faction exposes ~6 roles (`Guard_Ranged`,
  `Guard_Melee`, `Heavy`, `Sniper`, `Netrunner`, `Elite`) across 3 gear brackets
  mapped to the faction's **Fielded Materiel Tier** (Low = T1–2, Mid = T3,
  High = T4–5), keeping faction weapon flavor (Tyger Claws smart guns/katanas,
  Maelstrom tech/LMGs, Militech/6th Street power rifles, VDB netrunners, etc.).
- **Affiliation & Attitude:** Every garrison unit starts **neutral to V** on
  spawn (`AttitudeAgent.SetAttitudeTowards(player, Neutral)`) unless V's
  affiliation/standing is Hostile, V is in an active raid against the node, or
  V provokes them.
- **Elites:** `NPCRarity.Elite` + `Lvl3` visual tags + Tier-3 archetypes
  (`FastMeleeT3`, `HeavyRangedT3`, `NetrunnerT3`, `FastSniperT3`); 2 Elites
  guard the boss's room/approach on `large` and `very_large` nodes.
- **Lore & Generated Bosses:**
  - **Lore bosses** (e.g. Sasquatch, Kurt Hansen, Placide, Brigitte, Dodger,
    Woodman) use their canonical `Character.*` record (with a TweakXL combat
    wrapper if vanilla is non-combat).
  - **Generated lieutenant bosses:** 3–4 TweakXL boss archetype templates per
    faction (`Character.NA_Boss_<Faction>_<Archetype>`), using `NPCRarity.Elite`
    on `small` nodes and `NPCRarity.Boss` (`bossHealthBarThresholds`,
    `TargetTracking.BossPreset`, faction signature gear) on `medium+` nodes.
  - **Dynamic names without TweakDB bloat:** The native sim generates and
    persists `(leader_id, name, title, archetype_template)` in the playthrough
    DB. On spawn, redscript registers `entityID -> leader_id` and a thin
    scanner/nameplate hook displays the generated name & rank. On death, the
    sim deducts the replacement cost and generates a successor.

---

## 5. Spatial anchors, patrols & generic allied assault AI (S8)

### Per-node spatial anchors in `world.db`
Extracted from each node's vanilla Quest streaming sector (supplemented where
absent):
- `boss_seat` (1 primary office/VIP workspot)
- `guard_posts[]` (`worldAISpotNode` at entrances, stairs, chokepoints, VIP doors)
- `patrol_splines[]` (`worldPatrolSplineNode` workspot chains, or 2–4 waypoint
  coordinate loops where vanilla lacks splines — fixing elevator-stuck guards)
- `staging_point` (safe street approach 35–60 m outside)
- `breach_points[]` (1–2 main entrances/gates)
- `interior_waypoints[]` (1–3 ordered room/floor anchors leading to `boss_seat`)
- `lift_links[]` (optional `(lift_entity_id, ground_floor_idx, target_floor_idx, cab_capacity=4..5)` for elevator-accessed nodes)

When V enters streaming range, the controller's garrison spawns via
`PreventionSpawnSystem.RequestUnitSpawn(recordID, transform)` (verified not to
pollute NCPD's ticket registry in `living-world-site-modeling.md` §2.2) and
receives `AIUseWorkspotCommand` (static posts) or `AIPatrolCommand` /
`AIMoveToCommand` (patrols).

### Generic 4-Phase Assault Controller (zero per-venue scripts)
Ticked every 2–3 seconds (never per-frame) in C++ + thin redscript adapter:
1. **Rally & Advance:** Spawn allied squad at `staging_point` (drawn from
   attacking bloc's Manpower). Set mutual Hostile attitudes between attackers
   and defenders via `AttitudeAgent.SetAttitudeTowardsAgentGroup`. Advance via
   `AIMoveToCommand` toward `breach_points`.
2. **Native Combat Handover:** Once attackers come within ~25–30 m of a
   defender (or shots are fired), register mutual persistent threats via
   `TargetTrackingExtension.AddThreat(entity, true, pos, 1.0, 0.0, true)`.
   Cyberpunk's native combat AI (`Gang.Map`, cover, flanking, grenades,
   netrunning) handles the firefight automatically.
3. **Anti-Stall Leapfrog:** When an attacker has no threat within ~20 m, advance
   its `AIMoveToCommand` target to the next `interior_waypoint` / nearest living
   defender and refresh `AddThreat` so squads clear room-by-room.
4. **Capture & Handover:** When defenders and boss are neutralized, flip
   ownership in SQLite, transition surviving attackers onto `guard_posts` /
   `patrol_splines`, and seat the new lieutenant at `boss_seat`.

### Real AI Elevator Mechanism (zero teleporting)
Verified in `refs/cyberpunk/cyberpunk/devices/elevator/lift.swift`: `LiftDevice`
uses a physical `MovingPlatform` (`m_movingPlatform`) that carries puppets
inside the cab, an `OffMeshConnectionComponent` (`EvaluateOffMeshLinks()`) that
bridges cab-to-lobby navmesh when doors open, and `QuestForceGoToFloor` (which
moves the lift without applying `TemporarilyBlockMovement` to V):
1. **Call:** Squad waits outside the lift doors; if `!ps.IsMoving()`,
   `ps.GetActiveFloor() != floorA`, and `!ps.IsPlayerInsideLift()`, send
   `QuestForceGoToFloor(floorA)`.
2. **Board:** When doors open at `floorA`, issue `AIMoveToCommand` for a batch
   of 4–5 NPCs to offset cab points around `lift.GetWorldPosition()` (with a
   6–8s boarding timeout so one snagged unit never deadlocks the wave).
3. **Ride:** Send `QuestForceGoToFloor(floorB)` — doors close, safeguard
   colliders engage, and `MovingPlatform` carries the batch (and V if V rides
   with them) physically to `floorB`.
4. **Breach & Cycle:** On arrival, push the batch into `floorB_breach_point` +
   `AddThreat(nearestDefender)` and cycle the car back for Wave 2 if more
   attackers wait downstairs.

### Rank-Gated Squad Commands (`Follow / Push / Hold`)
- **Low Rank / Grunt (or joining another lieutenant's mission solo):** V does
  **not** command the squad. The mission's NPC Captain/Lieutenant drives the
  assault state machine; V fights alongside them to build favor and rank.
- **Lieutenant / Captain (or Leader of V's own gang/corp):** V unlocks her own
  persistent personal squad (drawn from her bloc's Manpower) and leads missions
  she captains, enabling the **Follow / Push / Hold** toggle:
  - **Follow:** `AIFollowTargetCommand(player)`
  - **Push:** `AIMoveToCommand` + `AddThreat` along assault waypoints
  - **Hold:** `AIHoldPositionCommand` at current cover

---

## 6. Convoy AI & road graph

`data/schema/world_v1.sql` already defines `road_chunks`, `road_chunk_rtree`,
and `road_edges` (backed by `all.traffic_persistent` — 33,953 traffic lanes,
extracted via `tools/extract-world.py --with-roads`). Once populated, the road
graph powers two convoy systems:

1. **Supply Convoys (`is_logistics` → faction nodes):**
   - Scheduled in the Road-Chunk Vehicle Transit Ledger; materialized along the
     road graph when V approaches an active chunk (driving **"Intercept / Kill
     Faction Convoy"** missions).
   - Lead vehicle runs `AIVehicleDriveToPointAutonomousCommand` along road-graph
     waypoints; escort vehicle(s) trail the lead via `AIVehicleChaseCommand`
     (`distanceMin` / `distanceMax`) or staggered waypoints.
2. **Assault Squad Convoys (riding with the squad):**
   - V rides with her squad (+ 1 companion slot, deferred to companion system)
     to the target node's `staging_point`, with an optional second escort car
     following behind.
   - **Passenger-seat rule for multi-car convoys:** When a second AI vehicle
     follows the lead car, **V rides as a passenger** while an NPC driver runs
     `AIVehicleDriveToPointAutonomousCommand` along the road graph. This
     prevents erratic player driving from breaking the trailing car's AI and
     lets V fight from the passenger window if ambushed en route.

---

## 7. Required in-game verification spike (before full build)

Before implementing the full garrison and assault systems, run one small dev
probe spike (one deploy + one load) to empirically confirm:
1. `PreventionSpawnSystem.RequestUnitSpawn(recordID, transform)` spawns a
   TweakXL faction unit cleanly without wanted-level or crowd-null suppression.
2. `StatsSystem` `PowerLevel` override de-scales the spawned puppet to the
   requested level cleanly.
3. `AIUseWorkspotCommand`, `AIPatrolCommand`, and `AIMoveToCommand` +
   `TargetTrackingExtension.AddThreat` drive posts, patrols, and NPC-vs-NPC
   combat reliably.
4. `LiftDevice` boarding across `OffMeshConnectionComponent` + riding
   `MovingPlatform` via `QuestForceGoToFloor` carries 4–5 NPCs cleanly between
   floors.
5. Redscript scanner/nameplate hook displays a native-supplied generated boss
   name.
