# Changelog

All notable changes to Neon Ascendancy are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
this project adheres to [docs/versioning.md](docs/versioning.md).

## [Unreleased]

### Added
- Dev tour checklist: every tour stop lists what to look at (base checks,
  unmapped groups, the venue's open research questions, extra checks from
  `data/venues/tour_checks.json`). The tour waits at each stop until the list
  is saved; "Neon: checklist here" opens it anywhere; the tour report flags
  PROBLEMS and UNCHECKED items.
- Research wave 15 (first part): La Catrina, the Sunshine Motel Militech
  outpost, 8ug8ear's building, the Union Railroad Station Wraith outpost,
  Gustavo's building, the Kendachi plant lot, the Lobos St tower, the
  monokatana workshop and the Acorn Towers lot. Then Tirempire Auto Shop,
  the Kabuki basement ripperdoc lab, the Mallagra St. house and the Kabuki
  docks container yard (re-anchored on an ungated lift). Last: the Rovinj
  St. glitter kitchen, the Highway 101 Wraith camp, Data Inc., the H11
  server room and the Valentinos auto shop.
- Research wave 14 (first part): Aaron's Northside flat, the Los Osos
  motel and the Benko St bus depot; six intact venues became tour checks.
  Second part: the Dewdrop Inn, the Longshore Stacks container yard, the
  Horrigan home and Capitán Caliente, and the Dogtown container-yard lanes.
- Research wave 13 (first part): Wired Head, the Eisenhower St. block, the
  Kabuki rooftop slums, Lina's home, a City Center back alley, the Japantown
  Apartments, the Cytech factory, the Tyger Claws casino, the Maelstrom
  warehouse and the Kenmore Diner. Second part: Cynosure Site D, the
  Montezuma's Throne boxing ring, Memorial Park NCART station, El Pinche
  Pollo, BuryGer and Farida's clinic.
- Research wave 12 (first part): 6th Street's floor 19 in Megabuilding H6,
  Jacked and Coke, Motel Kabuki, the Bennett alley, Tranquil Terrace, the
  Luxor High Wellness Spa, the Coastview relay tower, Poppy Farm and the
  Gutierrez penthouse. Second part: Cali Express, the Bullard & Sequoia
  construction site, the psychiatric center and the Old WNS station.
- Research wave 11 (first part): the Arasaka safe house (intact, empty),
  the Love Shack, Eva Cole's yacht party, the C-Team office, 7th Hell,
  Delamain HQ and the Brainporium. Second part: Yucca, the Chram Denya
  Jinja shrine, the High Peak VDB meeting ground, the landfill, a Rancho
  Coronado coffee cart, Jackie's garage, Laguna Bend's drowned town, the
  Revere Courier depot, the Wellsprings pump-station beach and the
  Longshore Stacks courtyard.
- Research wave 10 (second part): Haven Clinic in Dogtown (working free
  clinic), the Silver Pixel Cloud drive-in (shut, gates open), the No-Tell
  Motel, the Satwave power plant (security drones) and Jinguji (pre-attack
  staff and clients; the after-attack set deactivated as vanilla does), and
  Dodger's Barghest base in the old Coastview NCPD precinct.
- Research wave 10 (first part): the Dark Matter lounge (door and lift
  access, quiet between events) and the NCPD police lab in the Glen (its
  researcher on shift).
- Research wave 9: Corp-Bud Mine, the Arasaka Industrial Park lookout, the
  Embers garage, Chubby Buffalo’s BBQ, and Rancho Coronado’s Capitán Caliente.
- Research wave 8: Rolland’s Butcher Shop, Edgewood Farm’s entrance, Rocky
  Ridge, Empathy, Tripple Extreme Gym, and the Kabuki alley block.
- Research wave 7: Arasaka Estate, Ginger Panda and its netrunner den, the
  Peralezes' penthouse, PieZ, Organitopia, Night City Prison, Bree Whitney's
  apartment building, the Martin Street motel, the Highway 101 SovOil
  station, and Straight Shooters in Kabuki.
- Research wave 6: the Ebunike docks (Maelstrom crew), the prologue
  scavenger den, Ingalls Farm (switches only), the Wraiths' landfill
  outpost, Site 341 academy, the Black Box container yard and the crash-site
  route's residents and checkpoint (Dogtown), and the sealed Cynosure bunker.
- Research wave 5: the derelict West Wind Estate hotel, Gloria's house
  (Gloria and Mariah), the Militech Detention Center, the Dogtown checkpoint
  gate garrison, Cherry Blossom Market (Karim, the ramen cook, Ozob), The
  Moth (Alex and Margarita), Fingers' clinic frontage, the Rosebud club and
  the Electric Corporation Scav base. The q301 crash landing is excluded.
- Research wave 4: the Digimmortal tech expo (scav-held), Marianne's garage
  (Aldecaldo mechanic), the Militech expo spider-tank arena (Barghest guards,
  the Chimera on standby), Fourth Wall Studios, the Hillpark basketball court
  (Voodoo Boys, outcasts) and the Rindo Hotel squat. The q104 crash site, the
  VR training sim and The Hammer are excluded. Venue entries may name
  untagged community spawners by full path (rule 3).
- Pilot research merged into hand-built venues as additions (owner: add
  generously, the tour subtracts): Clouds, the Afterlife (patrons, tube
  dancers, background crowd, Emmerick, Weyland, lights and music), Totentanz
  (pre-quest crowd, guards, music and interior switches), and the Arasaka
  Tower's working lobby and floor-33 office.
- Research wave 3: the Raffen Shiv camp, the Arasaka industrial park
  warehouse, the Elders' lair, the Chapel of the Black Madonna, the Sunset
  Motel roadhouse, and Heavy Hearts (a Dogtown gig site, restored as an
  ordinary club). Club Atlantis is excluded (closed in 2077).
- Research wave 2 venues (dev venue gate): Lizzie's (switches, crowd), the
  Dogtown stadium (Barghest posts, market crowd, normal look), El Coyote
  Cojo, Judy's apartment (neighbours; flat kept locked), Riot, the Hill Park
  spa Voodoo Boys den with Slider alive, Jig-Jig Street, Megabuilding H10, and
  the Red Peaks trailer park (Joss and her kids). Border crossing pass 2 adds
  the Militech post.
- First generated venues (research wave 1, `data/venues/approved/`), all
  behind the dev venue gate: Corp-Bud rail junction, Aldecaldos Mobile Camp,
  Grand Imperial Mall, maglev tunnel site, Voodoo Boys' netrunners' den,
  SoCal border crossing, Misty's/Viktor's clinic look, and the Japantown
  parade-area market. The Space Force One crash street and the new Nomad Camp
  are excluded from research (not in our timeline).
- Runtime door policy (`World/DoorPolicy.reds`, dev-gated by `na_door_policy`):
  every quest-driven door that streams in is enabled and powered, and is
  unlocked or unsealed only when it would otherwise be impassable (no
  authorization, no controlling terminal, no skill check, toggle or
  quickhack). Doors are never force-opened. Scope is generated from the venue
  catalogue (`World/DoorScope.reds`, 899 doors). Each decision is logged as
  `DoorPolicy:`.
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
- T-Bug (`Character.c_tbug`) added to the cast layer on the Afterlife back-room
  couch beside Dexter, activated exactly as vanilla q005_01_plan does
  (community template `#tbug` / `tbug` / `q005_tbug_afterlife`). The cast builder
  now supports `spawn_kind: "community"` as well as spawn sets.
- Probe: `Dataterm[...]` lines log each Dogtown fast-travel dataterm's resolve
  and PS `powered`/`disabled` state, and the Black Sapphire decoration node.
- Probe: `VariantToggle[...]` lines log the `na_dbg_vt_<venue>_branch` /
  `_prewait` / `_prox` / `_reached` / `_done` facts the builder emits around each
  venue branch and its `questTogglePrefabVariant` node, so a run shows exactly
  where a branch stalls.
- `docs.clean-slate`: `venue_phases.json` now supports `allowed_device_controllers`
  (lift/window/platform/terminal/dataterm) so a route can drive non-door devices.

### Changed
- Dogtown's vanilla open-world layer is live: the clean slate sets
  `ep1_side_content` (the only allowed `ep1_` fact). That opens the
  district ambient communities and combat groups, the quest communities
  (stadium, Heavy Hearts, Golden Pacific, Longshore market and others) and
  the checkpoint gate. Gigs, vendors, dynamic events and the Phantom Liberty
  campaign stay gated. The q302 protest at the gate is suppressed.
- Dogtown street dynamic events run: `ep1_dynamic_events` is wired directly
  (vanilla gates it on `ep1_active`, which also opens PL gigs). 38 of 43
  events run; 5 wait on story facts.
- Venue doors follow the owner's door policy: closed by default but usable
  (enabled/powered, unlocked only where there is no other way through), never
  force-opened; doors with an in-world opener (terminal, keycard, hacking,
  Technical/Body check) stay vanilla. The Black Sapphire main door is now closed
  by default; Woodman's front office door (server-room terminal) is untouched.
- Clouds staff phase: Woodman via his vanilla spawn set (friendly start), the
  Tyger Claws security from `#q105_com_dollhouse_combat` (non-hostile phases),
  and Woodman's private lift enabled with its authorization disabled. Venue
  entries can now declare `spawn_sets`.
- Dev look-at logger also reports `skillCheck`, `quickhack` and `authValid`.

### Fixed
- Wang's Clinic (Kabuki) is staffed: `kana_yakin_default_on` is set so the
  kept Kabuki vendor layer places Roger Wang (it was set only by a gig phase).
- Venue approve: a proposal's `proximity_anchor.within` now sets the wait
  radius (it was always the `--within` default of 80 m).
- Venue checker: refs named only in free-text notes no longer count as
  placed by another layer (Farida was blocked by a Dogtown vendors note).
- Cali Express (the Glen) trades: its vendor and customers were gated on
  `q004_done`; the narrow `hey_gle_foodshop_01_default_on` vendor fact is set
  instead.
- Venue checker: an entry phase vanilla itself activates at the venue is
  accepted (with a required tour check) when the catalogue could not resolve
  the spawner's postures, e.g. Max Jones at the Old WNS station.
- Venue miner: sector refs written as `<path>;#tag` now resolve, so 150
  more quest-driven doors (e.g. Jacked and Coke's front door, the q112 safe
  house entrances) are in the runtime door policy's scope (875 -> 1020).
- Venue miner: community actions written as the older `questLegacy_NodeType`
  (99 vanilla phases) were ignored, so 394 activations were invisible to the
  checker, e.g. the downtown phase that already fills 7th Hell. The checker
  now also warns when vanilla activates the whole community an entry
  belongs to.
- Venue checker: a community `Deactivate` is no longer judged as an
  activation. Removing an alert or post-quest entry used to fail the posture
  rule; now only the entry's existence is checked.
- Start Dogtown's vanilla vehicle checkpoint from the Clean Slate quest on
  new games and save restore. The open-world phase runs the scans and barriers
  in both directions without the Phantom Liberty campaign.
- Clouds Tyger Claws no longer look alert. The two VIP-entrance guards used
  vanilla's `after_woodman` phase, whose workspots are the post-interrogation
  lockdown (nervous stance, agitated shuffle). They now use `start` (leaning,
  waiting), and the ground-floor lift guard is added on its `start` tablet
  spot. Woodman's lift drops the no-op `AuthorizationDisable`: floor access
  comes from its floor terminals, and the lift offers the authorization
  quickhack, so door policy keeps it vanilla.
- Venue access: inside each venue phase, community activations, variant toggles,
  the proximity chain and door actions now each leave the venue's branch on their
  own edge (spawn and device nodes are leaves), so one node that never completes
  blocks nothing else; variant toggles fire at boot without a proximity wait.
  Dogtown dataterms: the variant is addressed by its full `$/…` path (untagged
  prefab nodes do not resolve as `#` short refs) and the prefab is no longer
  declared; the builder now rejects `#…_prefabXXXXXXX` short refs. Clouds: the
  proximity anchor is the VIP door device, and the manager/Tyger Claws staff run
  in their own `venue_q105_dollhouse_staff` phase with the Woodman office prefab.
- Venue access: each venue now has its own quest phase
  (`mod\neon_ascendancy\venue_<code>.questphase`), all fanned out from the one
  `na_dev_venue_probe` gate. In owner runs the single shared `venue_probe` phase
  never entered its hub at all (`branch=0` for every venue), so one failing venue
  disabled every other one. A prefab may now be owned by one venue phase only
  (`--check` enforces it); the sneak-in route no longer re-declares
  `#q303_pr_paradise_technical`.
- Venue probe: community activations now also run *after* each venue's proximity
  wait, not only at the hub fan-out. On a fresh start the venue prefab has not
  streamed when the phase boots, so the boot-time `Activate` hit nothing: the
  18:20 log showed Clouds at `communitySpawned=0` for the whole session with the
  owner standing inside. On a loaded save the prefab is already streamed, which
  is why 18:33 read 34. The boot pass is kept (a load may never revisit the
  venue) and the re-issue is idempotent, so a fresh start now behaves like a
  load. `--check` asserts both passes bracket the wait and each venue leaves the
  hub on its own edge.
- Venue probe: a `questDeviceManagerNodeDefinition` whose objectRef does not
  resolve to a live entity does not complete, so everything chained behind it
  never ran. That is why the variant toggles reported `reached=0` even while
  communities spawned. Variant toggles now run *before* the device actions, and
  each venue branch emits `na_dbg_vt_<venue>_branch` / `_prewait` / `_prox` /
  `_reached` / `_done` facts the probe logs, so the stall point is visible.
- Venue probe: the Afterlife door waited on `#q005_ws_dex_afterlife_01`, which
  lives inside the `#q005_cin_01_plan` cinematics sub-prefab and is not
  instantiated unless that scene streams, so the pause never resolved. The
  anchor is now `#q005_dvc_afterlife_briefing_room_door` itself (an ungated
  `worldEntityNode` at the door).
- Venue probe: the Dogtown dataterm proximity anchor was `#stadium_data_term_001`
  itself, which sits *inside* variant group 1798 (the hidden
  `combat_zone_data_terminals_active` group). The distance pause could therefore
  never resolve, so neither the toggle nor the device actions ever ran. The
  anchor is now `#decoset_streetsign_gwashington_001_prefabJBZIHZI`, an ungated
  decoration 3.6 m from the terminal; the builder now rejects an anchor that is
  a variant state or is marked variant-gated.
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
