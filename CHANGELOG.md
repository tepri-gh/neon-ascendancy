# Changelog

All notable changes to Neon Ascendancy are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
this project adheres to [docs/versioning.md](docs/versioning.md).

## [Unreleased]

### Added
- Dev boost: `NeonAscendancy_ApplyDevDebug` grants and equips Reinforced
  Tendons (`Items.AdvancedBoostedTendonsLegendary`, the double-jump leg
  cyberware) in the `LegsCW` slot via `EquipCyberwareByTDBID`, the same
  path a ripperdoc install uses. Idempotent (equipped leg slots are scanned by
  record id first) and logged as `doubleJump=` on the `DevDebug.Apply` line.
- Black Sapphire tower population (`data/clean-slate/tower_population.json` ->
  `bsc_tower_population.questphase`, always on): lobby, floor-67 and floor-99.
- Kurt Hansen (`Character.kurtz`) added to the cast layer as an ambient Barghest
  leader, spawned exactly as vanilla q303_06_paradise does (`#kurtz` /
  `kurtz` / `q303_restaurant_host`) on Black Sapphire floor 99.
- Probe: `Dataterm[...]` lines log each Dogtown fast-travel dataterm's resolve
  and PS `powered`/`disabled` state, and the Black Sapphire decoration node.
- `docs.clean-slate`: `venue_phases.json` now supports `allowed_device_controllers`
  (lift/window/platform/terminal/dataterm) so a route can drive non-door devices.

### Fixed
- Venue probe: duplicate `phasePrefabs` silently broke phase instantiation, which
  dropped every community activation and device action to zero. Prefabs are now
  deduplicated in `venue_probe.questphase`, and `--check` fails if a prefab is
  declared twice or is declared by both `venue_probe` and `cast_and_hubs`.
- Black Sapphire: the afterlife and sneak-in entries no longer re-declare
  `#q005_pr_afterlife` / `#q303_pr_combat_tower`, which `cast_and_hubs` owns.
- Dogtown dataterms: use the real device ref `#stadium_data_term_001`
  (`ep1_data_term_1.ent`) instead of the prefab segment name, and force
  enable/power it behind a proximity wait.
- Dev boost: attributes/perk logging no longer implies the level boost.

### Initial
- Initial repository structure, redscript 1.x CLI tooling (`tools/`), modding
  documentation (`docs/modding.md`), versioning policy (`docs/versioning.md`),
  and cross-agent redscript skill (`.agents/skills/redscript/SKILL.md`).
- Target stack pinned in `tools/lib/versions.sh`: Cyberpunk 2077 2.5,
  RED4ext 1.31.1, redscript 1.0.2, ArchiveXL 1.28.11, TweakXL 1.12.2
  (Codeware-free), plus dev/build pins for CET 1.38.1, WolvenKit.CLI
  10.0.0-beta.1, xwin 0.10.0, SQLite 3.54.1, RED4ext.SDK, and RedLib.
- Architecture, roadmap, glossary, and Phase 0 empirical research reports
  under `docs/`.
- Dev-only CET installer (`tools/install-dev-cet.sh`) and Phase 0 in-game
  probe pack (`tools/probes/neon_probe.lua`).
- Canonical SQLite schemas (`data/schema/world_v1.sql`,
  `data/schema/playthrough_v1.sql`), EP1-over-base world extractor
  (`tools/extract-world.py`), extracted Night City seed data (`data/*.json`),
  and deterministic `world.db` compiler (`tools/build-world-db.py`).
- Native C++20 simulation and SQLite storage core (`native/lib/sim`,
  `native/lib/store`), offline Linux unit tests (`native/tests`), cross-compiled
  Windows x64 `/MT` RED4ext + RedLib plugin (`native/plugin/Main.cpp`), and
  automated native verification (`tools/verify-native.sh`).
- Initial redscript 1.x core foundation (`Core/Version.reds`,
  `Core/NativeBridge.reds`, `Sandbox/WorldEra.reds`,
  `Persistence/AnchorSystem.reds`).
- `v0.1.0` playable slice (thick C++20 core + thin redscript 1.x wires):
  - Pure C++20 world-era classifier and sanitizer policy engine (`native/lib/sim/era.*`),
    `WorldDb` faction/district/color metadata & nearest-rival lookup, combat
    mission kill progression (`RecordMissionKill`), and backwards-compatible
    v2 snapshot serialization.
  - Pre-game-safe `AnchorSystem` (opens session only on `PlayerPuppet` attach
    or save restore, avoiding main-menu dummy DB files).
  - Opt-in `SanitizerSystem` (monotonic city/FT unlock, Act 2 content flags,
    vanilla quest suppression, unsolicited call/dialog/mappin filters).
  - TweakXL mappin definitions (`src/r6/tweaks/NeonAscendancy/Mappins.yaml`),
    41 faction-tinted World Map control-center pins with custom tooltips,
    and active combat raid waypoints (`Map/TerritoryMapSystem.reds`).
  - Contextual Codeware-free Pause Menu entry (`UI/PauseMenuEntry.reds`) and
    gameplay/income coordinator (`Gameplay/AscendancySystem.reds`) wiring
    gang founding, NPC takedown raid tracking, immediate territory flip,
    and periodic `GameTime` eddie payouts.
- Test-scope territory: one active control center per modeled faction
  (`ACTIVE_TEST_CONTROL_CENTERS` in `tools/generate-world-seeds.py`); the
  rest ship dormant (`control_centers.is_active = 0`) and stay out of the sim,
  map and spatial lookups. Existing playthroughs reconcile on load.
- Faction headquarters map markers (`faction_headquarters` world table,
  faction-tinted fixer-icon pins with tooltips; not capturable yet), seeded
  from the lore research in `docs/research/factions/`.
- Dev-only venue-access probe (the first in-game test that a Neon-authored
  phase can open quest-only interiors):
  - `data/clean-slate/venue_phases.json` declarative spec; the builder emits
    `mod\neon_ascendancy\venue_probe.questphase` and wires it off
    `ascendancy.questphase` behind the dev fact `na_dev_venue_probe > 0`. The
    builder asserts venue phases carry prefabs, doors and communities only
    (never journal/mappin/phone/street-story/gig phases) and `--check`
    round-trip-verifies the new `questInteractiveObjectManagerNodeDefinition`
    (`questDeviceManager_NodeType`) door nodes.
  - Nine venues: Ho-Oh/Kabuki (section 5.1 case, `#sts_wat_kab_07_streetstory`,
    `#kab_07_com_enemies` `0combat`, entrance gate power/open) plus Konpeki
    Plaza, Clouds, All Foods, Totentanz, Batty's Hotel, Embers, Black Sapphire
    and Arasaka Tower, each with refs verified from vanilla phase and streaming
    sector extractions.
  - Native helpers `NcResolveNodeRefByHash(Uint64) -> GlobalNodeRef` and
    `NcHashNodeRefPath(String) -> Uint64` (RED4ext `NodeRef::Hash`, FNV-1a 64
    with `#` stripped), because redscript 1.x cannot construct or hash a NodeRef.
  - Dev-only `NeonAscendancy.Debug.VenueProbe` reports, once after bootstrap and
    once after a delay, whether each venue's workspot resolves, the probed door
    `DoorControllerPS` state (`IsOpen/IsLocked/IsSealed/IsDisabled/IsPowered`),
    and the community spawner's spawned-entity count.
  - Prefab-variant support: the builder now emits
    `questWorldDataManagerNodeDefinition` / `questTogglePrefabVariant_NodeType`
    (schema from vanilla `q303_06b_paradise_technical`), the only way to open
    baked geometry such as the Black Sapphire tower-gate shutters. Black
    Sapphire swaps to `var_tower_gate_open_indestructible` on
    `#loc_q304_pr_combat_tower_decoration`; `--check` round-trip-verifies the
    toggle.
  - Konpeki now activates `#q005_com_hotel_guests`/`#q005_com_hotel_staff`
    (`None`/`default`); Clouds activates Hiromi (`manager`/`start`) and the
    Tyger Claws shop staff (`shop_tc_01/02`, `shop_owner`/`start`) plus
    `employees_fem/male`; Totentanz probes a real workspot under
    `#loc_pre_quest_totentanz`.
  - The probe re-runs every 60 s while `na_dev_venue_probe` is set, and the
    door census logs within 150 m with the player position (the debug name/path
    APIs return `None` for authored doors) and de-duplicates repeat attaches.
- Venue-door reliability fixes from the first in-game run:
  - Every venue door now issues ForceEnabled -> ForcePower -> ForceUnlock ->
    ForceOpen (vanilla `q303_07b_lobby_combat` uses ForceUnlock -> ForceOpen on
    `#q303_dvc_combat_tower_main_door`; the leading actions are added so a
    disabled/unpowered device still opens).
  - The Black Sapphire entry now declares `#loc_q304_pr_combat_tower_decoration`
    and `#loc_q303_combat_tower_devices_bottom_lobby` (a phasePrefab variant
    only applies to a prefab the phase declares) and opens the tech-warehouse
    shutter (`#q303_dvc_tech_warehouse_gate`), the Barghest-logo roller door at
    the tower entrance.
  - Totentanz now declares `#loc_sq011_totentanz_openworld` so the
    `#com_totentanz` crowd spawner resolves.
  - Dev-only on-site door repair: when the player is within 60 m, the probe
    re-issues the vanilla sequence against the live PS, because the phase's own
    device actions fire at bootstrap while the player is still in H10.
- Venue phase proximity waits (vanilla-native, replaces the bootstrap problem):
  - The builder emits `questPauseConditionNodeDefinition` ->
    `questDistanceCondition` (`questDistanceComparison_ConditionType`, player
    within N metres of an authored node), schema from vanilla `q304.questphase`.
    Every venue declares a `proximity_wait`, so its device actions run only once
    the player is near and the venue has streamed. `--check` round-trips the
    waits.
- Clouds (item 7): the manager/Tyger entries were already correct but never
  streamed; `#q105_ws_03a_manager_start` is not in `#q105_pr_dollhouse`, so the
  manager seat comes from the `#q105_pr_03c_dollhouse_woodman` sub-prefab.
  Added the office doors (`#q105_dvc_dollhouse_door_woodman`,
  `..._woodman_glass`) and the VIP lounge door
  (`#q105_dvc_dollhouse_door_vip`) with `AuthorizationDisable` first.
- Authorization doors (item 8): `AuthorizationDisable`
  (`QuestForceAuthorizationDisabled`) is now an allowed venue-door action and
  leads the Clouds VIP sequence; the probe logs `authModuleOn=<0|1|-1>` so a
  test proves the module state. The dev keycard grant was dropped by owner
  request.
- Dogtown dataterms (item 4): they live in
  `combat_zone_data_terminals_prefabLN6J6KI`, streamed only via the
  `combat_zone_data_terminals_active` variant (default off). New
  `dogtown_dataterms` venue declares that prefab and swaps the variant.
- Totentanz DJ/music (item 6): the DJ and club audio come from
  `dancefloors.questphase`'s `#dancefloor_totentanz` sub-phase
  (`dancefloor_totentanz.scene`), gated on fact `totentanz_dancefloor_on >= 1`;
  it is already wired, so only that fact is needed (set by DevDebug, not the
  archive). The DJ is not a `#com_totentanz` entry.
- Dexter DeShawn (item 9): added to the cast layer as an ambient fixer at the
  Afterlife booth via `questSpawnSet` `#dex` / `dex` /
  `q005_afterlife_default` (exactly as vanilla `q005_01_plan`), with
  `#q005_pr_afterlife` declared for his seat workspot
  `#q005_ws_dex_afterlife_01`.
- Dogtown vendor findings and the Afterlife back-room door (auth ref
  unresolved) are recorded in `venue_phases.json` notes rather than guessed.
- Watson lockdown cleanup (`data/clean-slate/barricade_cleanup.json` ->
  `barricade_cleanup.questphase`, always on, not dev-gated): reproduces the
  `watson_prolog_lock == 0` cleanup branches a clean-slate boot never reaches.
  Hides `q001_bridge_blockade` on `#wejt_03_devices` (verbatim q001 node 230),
  `prolog_blockades` on the LCH architecture prefab, and `security_systems` on
  the three devices prefabs; deactivates the 9 roadblock communities and the 60
  roadblock vehicle spawners via a new `questSpawner_NodeType` emitter
  (`QuestGraph.add_spawner_node`, `spawnerReference` shape from
  `lch_prolog_roadblocks.questphase`). `--check` round-trips the whole group and
  asserts 60 spawners / 9 communities / 5 toggles. The probe logs
  `BridgeState:` (fact + three spawner counts) so a test proves it.
- Dogtown vendors (`data/clean-slate/dogtown_vendors.json` ->
  `dogtown_vendors.questphase`, gated on a per-vendor fact): re-emits only the
  Activate spawn-set + community entries of `stadium_vendors` and the
  container-zone vendors, bypassing `ep1_vendors`' `ep1_side_content` /
  `q302_started` gates and dropping its 43 journal/scene nodes. The 10 narrow
  `cz_stadium_*_default_on` facts are added to `initial_facts`; they are read
  only by `q304_stadium_vendors_controller` / `stadium_vendors`.
- Afterlife briefing-room door: ref resolved by FNV-1a hashing
  `exterior_-23_15_0_0` -> `#q005_dvc_afterlife_briefing_room_door`; added with
  enable/power/unlock/open behind a proximity wait at `#q005_ws_dex_afterlife_01`.
- Roadblock research notes: the Dogtown main checkpoint pedestrian door
  refs were not extractable offline (prefab-template placeholders), so they are
  recorded rather than guessed.
