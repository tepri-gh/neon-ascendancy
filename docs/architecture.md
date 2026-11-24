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
4. **Thick C++20 core + paper-thin redscript adapters:** Keep **90%+ of the
   mod in C++20 (`native/`)**—all simulation, economy, mission generation, kill
   tracking, territory ownership, world-era classification, sanitizer policy
   decisions, tooltip/HUD text formatting, contextual menu state machines, and
   SQLite storage. This maximizes agent code quality, native runtime
   performance, and millisecond offline unit testing (`ctest`) without booting
   Cyberpunk 2077. Keep redscript (`src/r6/scripts/`) strictly as dumb,
   thin plumbing (`@wrapMethod` hooks on scripted gameplay/UI methods, the
   20-byte `ScriptableSystem` `.sav` watermark, and compile-time-checked calls
   to `MappinSystem`, `TransactionSystem`, `JournalManager`, and `inkWidget`
   APIs).
5. **Codeware-free baseline (for now):** Redscript code targets the pinned
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
│  - Save Anchor: tiny persistent ScriptableSystem (20-byte watermark) │
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

- **Era detection:** Inspects canonical `QuestsSystem` facts (`ep1_standalone`,
  `q005_done`, `q101_done`, `watson_prolog_lock`, `watson_prolog_unlock`,
  `q101_enable_activities_flat`, `q101_enable_side_content`,
  `q115_point_of_no_return`, `q301_00_done`) using `> 0` checks (never `== 1`).
  Never mutate story-completion facts (`q005_done`, `q101_done`) just to lift
  world gates.
- **Idempotent sanitization:** Applies era-appropriate unlocks and suppression
  layers safely even if re-run on every load (see
  [`docs/research/campaign-sanitizer.md`](research/campaign-sanitizer.md)):
  1. Ensure city traversal is unlocked (`watson_prolog_lock = 0`,
     `watson_prolog_unlock = 1`, `q101_enable_activities_flat = 1`,
     `q101_enable_side_content = 1`) while leaving vendors, ripperdocs,
     stashes, and fast travel operational.
  2. Suppress and untrack vanilla `MainQuest`, `SideQuest`, `MinorQuest`, and
     `Contract` journal entries via journal callbacks + `UntrackEntry`, and
     filter quest/gig pins in `CreateMappinUIProfile`.
  3. Drop incoming non-player quest/fixer/Songbird calls at
     `PhoneSystem.OnTriggerCall` while always passing `EndCall`.
  4. Filter `QuestImportant` dialogue choices in `InteractionUIBase.OnDialogsData`
     while preserving vendor, ripperdoc, and device service interactions.
  5. Remove `JohnnySickness` status effects in post-Heist saves (2.2/2.3
     passenger Johnny control pending in-game CET probe).

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

1. **Static `world.db` (read-only/`immutable=1`, built from `data/`):**
   - Extracted from plain-text `<game>/tools/redmod/tweaks/**/*.tweak` +
     EP1-over-base `always_loaded_0/1/2` and streaming sectors via pinned
     `WolvenKit.CLI 10.0.0-beta.1` (see
     [`docs/research/game-data-extraction.md`](research/game-data-extraction.md)).
   - `factions` (gangs, megacorps—including synthetic IDs for Night Corp,
     Kiroshi, Kendachi, Petrochem, and Budget Arms which lack vanilla
     `gamedataAffiliation` entries—fixers, civic/independents, colors)
   - `districts` (linked by `ParentDistrict()`, excluding `Dogtown_Worldmap_Sub`)
     and `sub_territories` (~5 control centers per major district, `owner_kind`
     in `{gang, corp, enclave, unclaimed}`, anchor `(x, y, z)`, boot-loaded
     grid/cell index + 2D R-Tree prefilter, base economy values)
   - `spawn_points` (exact game coordinates, faction affiliation, encounter type,
     linked `sub_territory_id`)
   - `landmarks` (key buildings, fixer hubs, purchasable corp assets)
   - *(Schema-ready, populated later)* `road_chunks` and `road_edges` from
     `all.traffic_persistent` (33,953 lanes) for the vehicle transit ledger
2. **Dynamic playthrough DB (mutable, per playthrough, WAL + `synchronous=NORMAL`):**
   - **Save-branching safety without a save hook:** Cyberpunk 2077 has no
     universal script-level save event (autosaves bypass `OnSavingComplete`).
     Instead, a tiny 20-byte `persistent` redscript `ScriptableSystem` stores
     `(m_schemaVersion, m_playthroughId, m_saveGeneration)` where
     `m_saveGeneration` acts as a **durable revision watermark**—advanced
     *only after* the native SQLite `COMMIT` returns.
   - Any save (manual, quick, or autosave) therefore captures a guaranteed-durable
     revision `R`. On load (`OnRestored`), the native core restores the newest
     checkpoint `<= R` plus deltas up to `R` and forks at `max(db, R) + 1` with
     a full snapshot—keeping reloads and branching saves exact with zero native
     save hooks (see [`docs/research/native-db-architecture.md`](research/native-db-architecture.md)).
   - Follow [`docs/versioning.md`](versioning.md) for all schema bumps.

### 3.4 Native Build & Cross-Compilation Constraint
- RED4ext / REDengine 4 uses the **MSVC x64 C++ ABI** (`x86_64-pc-windows-msvc`).
- Cross-compiling from Linux uses `clang-cl` + `lld-link` + `xwin` (MSVC
  CRT/SDK), **not** MinGW/GNU ABI, and **must link `/MT` (static CRT), not
  `/MD`**: Proton 11's builtin `msvcp140.dll` exports zero `__std_*` symbols,
  so `/MD` fails at plugin load on RedLib's `std::format` calls. Use Win32 path
  APIs instead of `<filesystem>`.
- Pin exact `RED4ext.SDK` and `cp2077-red-lib` commits compatible with 2.5
  rather than outdated tags.
- Pure C++ simulation and SQLite logic compiles natively on Linux (`clang++` /
  `g++`) for fast offline unit tests without launching Cyberpunk 2077.

### 3.5 World Map Territory Visualization
- Sub-territories are **pre-partitioned** around ~5 control centers per major
  district (derived from Step 0.2 spawn/building research).
- `WorldMapMenuGameController` renders a 3D hologram into a dynamic texture
  (`world_map_texture.dtex`), and `WorldMapDistrictLogicController` only drives
  labels/icons (see
  [`docs/research/world-map-visualization.md`](research/world-map-visualization.md)).
- Phased rendering path (Codeware-free):
  - **`v0.1.0`:** Vanilla map-only `MappinSystem` control-center dots tinted by
    owning faction in `BaseWorldMapMappinController.UpdateIcon` with custom
    tooltips.
  - **`v0.2.0`:** Pre-partitioned transparent fill + border polygons rendered as
    an `inkShape` layer inside `EntityPreview`, projected from world coordinates
    via a **4-anchor-mappin homography** (handles pan, zoom, tilt, and mod yaw
    rotation with O(1) recolor and zero idle per-frame cost—gated on 3 quick
    in-game spikes).

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
