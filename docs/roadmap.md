# Neon Ascendancy Roadmap

This roadmap tracks Neon Ascendancy from foundational engine/data proofs through
the full causal sandbox simulation. Gameplay systems are deliberately sequenced
*after* Phase 0 so territory, mission, and economic designs rest on verified
Cyberpunk 2077 2.5 data and engine capabilities.

---

## Phase 0 — Foundations, World Data & Visual Proof (`0.0.x`, Current)

The five steps below establish the ground truth and infrastructure needed before
locking down detailed territory-hold and mission-generation mechanics.

### Step 0.1 — Any-Entry-Point Campaign Disable & World Probe
- Support starting Neon Ascendancy from **any save state**: fresh Act 1
  (pre-Heist), post-Heist / Act 2+, Phantom Liberty skip-ahead, or saves started
  with existing intro/Watson-skip mods.
- Empirically verify in-game (using dev CET) on Cyberpunk 2077 2.5:
  - Lifting Watson lockdown in Act 1 (`watson_prolog_lock = 0`,
    `watson_prolog_unlock = 1`) and confirming all non-Watson shops, ripperdocs,
    and fast-travel points function.
  - Suppressing Johnny (passenger/Relic/voiceover in post-Act 1 saves), all
    vanilla main quests, side quests, gigs, fixer calls, and NPC quest dialogue
    choices without breaking shops or ambient city life.
- Deliver the design for the era-detecting, idempotent **Sandbox Sanitizer**.

### Step 0.2 — Parallel World, Faction & Spawn Mapping (Research)
- Use parallel research agents to catalog every active power in Night City,
  Badlands, and Dogtown:
  - **Gangs** (Maelstrom, Tyger Claws, Valentinos, 6th Street, Voodoo Boys,
    Animals, Scavengers, Wraiths, Aldecaldos, Barghest, The Mox).
  - **Megacorps** (Arasaka, Militech, Kang Tao, Biotechnica, Zetatech, NetWatch,
    Trauma Team, Night Corp / News54 / Orbital Air / Kiroshi as applicable).
  - **Fixers** (Regina, Wakako, Padre, Muamar, Dakota, Dino, Rogue, Mr. Hands).
  - **Civic & Independents** (NCPD, Afterlife Mercs, Delamain, etc.).
- Map each faction's controlled areas, key buildings/HQ landmarks, and **exact
  ground-truth spawn locations** extracted from Cyberpunk 2077 2.5 game data
  (`refs/cyberpunk`, TweakDB, community/sector data).
- Target granularity: **~5 control centers per major district** (tunable after
  research completes).

### Step 0.3 — Database & Native Core Architecture
- Prove the storage and simulation backend:
  - Primary target: thin **RED4ext + RedLib native C++ plugin** embedding
    **SQLite3** (amalgamation + R-Tree spatial index) for high performance,
    indexed queries, runtime logging, and offline unit testing.
  - Prove Linux-to-Windows MSVC-ABI cross-compilation (`clang-cl` + `lld-link` +
    `xwin`).
  - Design save-branch-safe persistence (`(playthroughId, saveGeneration)`
    checkpointing) so external SQLite never drifts on reload/quicksave.
  - CET's bundled `lsqlite3` is allowed for rapid schema prototyping before the
    native plugin is ready.
- Ensure schema foresight for the deferred **Road-Chunk Vehicle Transit Ledger**
  (see Deferred Systems below).

### Step 0.4 — Build the World Database & Assignments
- Represent all factions, sub-territories, control centers, spawn points, and
  initial ownership in human-readable, Git-diffable seed files under `data/`.
- Build a deterministic `tools/` generator with schema and coordinate validation
  that compiles `data/` into the read-only static `world.db`.

### Step 0.5 — In-Game Map Territory Visualization
- Design and prove **pre-partitioned sub-territory overlays** on Night City's
  in-game World Map:
  - Transparent faction-colored fills with crisp borders meeting neighboring
    sub-territories (Stellaris-inspired readability).
  - Distinct **control-center dots** marking each sub-territory's NPC spawn hub.
  - Performance-safe rendering that updates only on ownership changes and avoids
    per-frame CPU/GPU stalls.

> **Design Gate:** Once Phase 0 is complete, finalize detailed designs for the
> **Territory Hold / Contest** system and **Dynamic Mission Generator** before
> moving into full Phase 2 implementation.

---

## Phase 1 — First Playable Slice (`v0.1.0`)

Smallest end-to-end playable loop proving every architectural layer together:

1. **Codeware-Free Start Entry:** Start Neon Ascendancy from an in-game menu
   (diegetic `NETdir://ncity.pub` browser page, with optional pause-menu entry),
   activating the Sandbox Sanitizer for the current save's era.
2. **Found a Named Gang:** Player founds a named gang (corporation deferred
   until capital/asset ownership is implemented) and takes over an initial
   sub-territory control center inside a district.
3. **Periodic Territory Income:** Owned sub-territories pay periodic eddies on
   deterministic in-game `GameTime` cycles with HUD notifications.
4. **Rival Sub-Territory & Combat Clear Mission:** At least one rival faction
   sub-territory exists nearby with a dynamically generated combat clear-out
   mission.
5. **Immediate Ownership Flip & Causal Loop:** Clearing the rival NPCs flips
   the sub-territory immediately to the player's gang (hold mechanics come in
   Phase 2), updating the map visualization, recalculating periodic income via
   the causal event bus, and persisting cleanly across save/reload
   (`SCHEMA_VERSION = 1`).

---

## Phase 2+ — Causal Simulation Pillars (Priority Order)

All four pillars participate in one causal simulation through decoupled domain
events (`SimEvent`) so every player or faction action ripples across Night City.

### `v0.2.0` — Dynamic Missions & Territory Control
- Full **Territory Hold / Contest** mechanics (designed after Phase 0).
- Sub-territories populated across Night City districts (~5 control centers per
  major district, tuned from Step 0.2 data).
- Mission generator driven by borders, faction hostility, and local heat
  (raids, counter-raids/defense, disruption, supply hits).

### `v0.3.0` — Organization Management
- Founding a **Corporation** (requires capital and purchasing a physical
  asset/property) alongside the **Gang** path.
- Treasury, payroll/upkeep, lieutenants/roles, facility upgrades, notoriety,
  and NCPD/faction heat management.

### `v0.4.0` — Stock Market
- Corporate and faction-linked market tickers driven causally by territory
  ownership shifts, mission outcomes, district heat, and org activity.
- Player equity trading, shorting, and **Economic / Espionage** missions that
  deliberately move valuations.

---

## Deferred / Later Systems

Tracked explicitly here so Phase 0 database and architecture choices stay
compatible without premature implementation:

- **Fixer Freelance Contract System:** Gangs and megacorporations route
  freelance contract missions to V through the canonical Night City fixers
  (Regina Jones, Wakako Okada, Sebastian "Padre" Ibarra, Dakota Smith, Dino
  Dinovic, Muamar "El Capitán" Reyes, Rogue Amendiares, and Mr. Hands). The
  clean-slate world cast layer (`data/clean-slate/cast_and_hubs.json`) keeps
  every fixer physically present in their canonical HQ with zero vanilla gig
  phases or intro holocalls so Neon Ascendancy can hook custom freelance
  contract interactions directly onto them.
- **Iconic Weapons Rework Sweep:** Dedicated later pass to sweep vanilla iconic
  weapons (including vendor-stocked iconics such as Wilson's Dying Night) and
  integrate them into a Neon Ascendancy acquisition/reward system.
- **Road-Chunk Vehicle Transit Ledger:** Simulate offscreen convoys, patrols,
  and deliveries traveling from point A to point B along Night City's road
  network. Store chunk traversal intervals in SQLite indexed by road chunk;
  when the player enters a road chunk during a vehicle's active time window,
  materialize the vehicle/escort in-world and hand off cleanly on exit.
- **Tier 2 Engine-Level Campaign Excision:** Optional WolvenKit + ArchiveXL
  custom New Game `.questphase` if Tier 1 runtime sanitization leaves any
  stubborn vanilla world triggers.
- **Codeware 1.x Integration:** Adopt once an upstream release supports
  redscript 1.x (unlocking richer custom Ink dashboards, native text input, and
  `DynamicEntitySystem` if needed).
