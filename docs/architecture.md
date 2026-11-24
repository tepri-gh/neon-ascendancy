# Neon Ascendancy Architecture

This document defines the system boundaries, data flow, persistence model, and
performance rules for Neon Ascendancy.

---

## 1. Guiding Constraints

1. **Causal simulation without coupling:** Dynamic Missions, Territory Control,
   Organization Management, and Stock Market all affect one another, but never
   through direct cross-pillar mutation. Every cross-pillar effect flows through
   typed `SimEvent`s on a bounded, deterministic event queue.
2. **Performance-first:** Cyberpunk 2077 is already heavy on CPU, GPU, and
   physics. Neon Ascendancy must add near-zero per-frame overhead:
   - **Never** run SQLite queries or full-world scans on per-frame ticks.
   - Cache hot state (active sub-territory, neighboring chunks, active mission
     targets) in memory; refresh only on discrete events (zone crossing, kill,
     ownership flip, `GameTime` cycle).
   - Batch database writes on save/checkpoint boundaries rather than every
     micro-mutation.
   - Pre-partitioned map overlays update only when territory ownership changes.
3. **Human-readable data in Git:** Static world definitions live as declarative
   seed files under `data/` and compile reproducibly into `world.db`. Never
   hand-edit binary `.db` files in Git.
4. **Codeware-free baseline (for now):** Redscript code targets the pinned
   redscript 1.x stack in `tools/lib/versions.sh` without Codeware until an
   upstream release supports 1.x. CET is approved for dev/schema prototyping and
   is acceptable if needed, while the native RED4ext plugin remains the primary
   performance and storage layer.

---

## 2. Layered System Diagram

```text
┌───────────────────────────────────────────────────────────────────────┐
│  Declarative World Seeds (data/*.json / *.sql, Git-tracked)           │
│     └── tools/build-db -> static world.db (read-only, shipped)        │
└───────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌───────────────────────────────────────────────────────────────────────┐
│  Thin Redscript 1.x Adapters (src/r6/scripts/NeonAscendancy/)         │
│  - Sandbox: World-Era Detector + Idempotent Campaign Sanitizer        │
│  - UI: ncity.pub browser menu, HUD alerts, World Map overlay/mappins  │
│  - World: Puppet OnDeath, District/Chunk crossings, TimeSystem ticks  │
│  - Save Anchor: tiny persistent ScriptableSystem (12-byte checkpoint) │
└───────────────────────────────────────────────────────────────────────┘
                   │ SimCommand                    ▲ View / World Diff
                   ▼                               │
┌───────────────────────────────────────────────────────────────────────┐
│  Native Core Plugin (RED4ext + RedLib + embedded SQLite3 w/ R-Tree)   │
│  - Pure Causal Simulation Engine (Missions, Territory, Org, Market)   │
│  - Static world.db + Per-Playthrough Save-Safe Dynamic SQLite DB      │
│  - Spatial & Chunk Indexes (territories, spawns, future road ledger)  │
│  - Runtime Logger (red4ext/logs/neon_ascendancy.log)                  │
│  - Offline Native Unit Test Suite (runs on Linux in milliseconds)     │
└───────────────────────────────────────────────────────────────────────┘
```

---

## 3. Core Subsystems

### 3.1 World-Era Detector & Sandbox Sanitizer (`Sandbox`)
Players must be able to launch Neon Ascendancy from **any save** (fresh Act 1,
Act 2+, Phantom Liberty skip-ahead, or third-party intro/Watson-skip mods).

- **Era detection:** Inspects canonical `QuestsSystem` facts (`watson_prolog_lock`,
  `q005_done`, `q101_done`, `ep1_standalone`, etc.) to classify the save's entry
  era.
- **Idempotent sanitization:** Applies era-appropriate unlocks and suppression
  layers safely even if re-run on every load:
  1. Ensure city traversal is unlocked (lift Watson lockdown if active) while
     leaving vendors, ripperdocs, stashes, and fast travel operational.
  2. Suppress and untrack vanilla `MainQuest`, `SideQuest`, `MinorQuest`, and
     `Contract` journal entries and prevent new ones from tracking.
  3. Block vanilla quest/fixer/Johnny/Songbird incoming calls at
     `PhoneSystem.OnTriggerCall`.
  4. Filter vanilla quest dialogue hubs in `dialogWidgetGameController` while
     preserving vendor, ripperdoc, and device interactions.
  5. Suppress Johnny appearances/Relic malfunctions in post-Heist saves.

### 3.2 Pure Causal Simulation Core (`Sim`)
Each gameplay pillar owns its own isolated module with two pure entry points:
`ApplyCommand(cmd, snapshot)` and `HandleEvent(evt, snapshot) -> [SimEvent]`.

| Pillar | Owns | Emits | Reacts To |
| --- | --- | --- | --- |
| **Missions** | Mission lifecycle, target generation, completion/failure | `MissionOffered`, `MissionCompleted`, `MissionFailed` | `TerritoryOwnerChanged`, `HeatChanged`, `CycleElapsed` |
| **Territory** | Sub-territory ownership, control centers, hold/contest state, local heat | `TerritoryOwnerChanged`, `TerritoryContested`, `HeatChanged` | `MissionCompleted`, `MissionFailed`, `CycleElapsed` |
| **Organization** | Player Gang/Corp identity, assets, treasury, upkeep, notoriety | `OrgFounded`, `IncomeSettled`, `OrgNotorietyChanged` | `TerritoryOwnerChanged`, `MissionCompleted`, `CycleElapsed` |
| **Stock Market** | Faction/corp tickers, price momentum, player positions | `MarketPriceMoved`, `MarketShock` | `TerritoryOwnerChanged`, `MissionCompleted`, `HeatChanged`, `OrgNotorietyChanged` |

- **Deterministic time:** Simulation cycles advance strictly from in-game
  `GameTime` deltas (`currentGameTime - lastSimGameTime >= CYCLE_SECONDS`),
  making sleep/time-skip and save/reload completely deterministic.
- **Bounded propagation:** `SimEngine` processes the `SimEvent` queue with a
  strict max-depth/cycle cap to prevent runaway feedback loops.

### 3.3 Database & Save-Branch-Safe Persistence (`SQLite3`)
Two logical databases keep static mod content separate from player state:

1. **Static `world.db` (read-only, built from `data/`):**
   - `factions` (gangs, megacorps, fixers, civic/independents, colors, affiliations)
   - `districts` and `sub_territories` (~5 control centers per major district,
     anchor `(x, y, z)`, polygon/cell IDs, base economy values)
   - `spawn_points` (exact game coordinates, faction affiliation, encounter type,
     linked `sub_territory_id`)
   - `landmarks` (key buildings, HQs, purchasable corp assets)
   - *(Later)* `road_chunks` and `road_edges` (spatial R-Tree indexed for the
     vehicle transit ledger)
2. **Dynamic playthrough DB (mutable, per playthrough):**
   - **Save-branching safety:** A tiny `persistent` redscript `ScriptableSystem`
     stores only `(m_schemaVersion: Int32, m_playthroughId: Uint64, m_saveGeneration: Int32)`.
   - On save, the native core records an immutable checkpoint keyed by
     `(playthroughId, saveGeneration)` and increments the generation for future
     saves. On load (`OnRestored`), the native core restores the exact
     checkpoint matching the loaded save's `(playthroughId, saveGeneration)`—so
     quicksave/reload and branching manual saves never drift out of sync.
   - Follow [`docs/versioning.md`](versioning.md) for all schema bumps.

### 3.4 Native Build & Cross-Compilation Constraint
- RED4ext / REDengine 4 uses the **MSVC x64 C++ ABI** (`x86_64-pc-windows-msvc`).
- Cross-compiling the native plugin from Linux must use `clang-cl` + `lld-link`
  + `xwin` (MSVC CRT/SDK), **not** MinGW/GNU ABI.
- Pure C++ simulation and SQLite logic compiles natively on Linux (`clang++` /
  `g++`) for fast offline unit tests without launching Cyberpunk 2077.

### 3.5 World Map Territory Visualization
- Sub-territories are **pre-partitioned** around ~5 control centers per major
  district (derived from Step 0.2 spawn/building research).
- Visual targets:
  - Transparent faction-colored fill + border for each pre-partitioned
    sub-territory cell, meeting neighboring borders cleanly.
  - Control-center dot marking each sub-territory's faction spawn hub.
- Exact rendering mechanism on CP2077's 3D World Map (`WorldMapMenuGameController`,
  `.inkwidget` / `inkShape` / ArchiveXL overlay vs dynamic texture/plane) is
  selected in Step 0.5 based on measured pan/zoom alignment and frame cost.

---

## 4. Deferred Architectural Hook: Road-Chunk Vehicle Transit Ledger

Not implemented in Phase 0 or `v0.1.0`, but accounted for in the SQLite schema:

- Night City's drivable road network is partitioned into spatial **road chunks**
  indexed via SQLite R-Tree / chunk IDs.
- Offscreen convoys, patrols, and supply deliveries are simulated cheaply as
  scheduled chunk traversals in a `transit_ledger` table:
  `(transit_id, faction_id, vehicle_record, route_id, chunk_id, t_enter, t_exit, state)`.
- In-game, redscript notifies the native core **only when the player crosses
  into a new road chunk** (not per frame). One indexed query fetches any
  vehicles scheduled in the player's current/adjacent chunks at current
  `GameTime` and materializes them at their interpolated road transform; when
  they leave player range, remaining route progress writes back to the ledger.
