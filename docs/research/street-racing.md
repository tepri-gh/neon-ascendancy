# Vanilla street racing — how Cyberpunk 2077 does it

**Scope:** base game 2.5 + Phantom Liberty. Research for a Neon Ascendancy
street-racing system.
**Date:** 2026-11-26.
**Evidence tags:** **[V]** = verified from game data or decompiled scripts;
**[I]** = inferred (engine behaviour not in the script dump, or a reading of
several data points).

Raw evidence used:

- Converted quest phases:
  `/home/suvikyi/.cache/neon-ascendancy/extracts/questphases/raw/base/base/quest/`
  (paths below are the vanilla depot paths).
- Decompiled scripts: `refs/cyberpunk/`.
- Extracted checkpoint entity:
  `base/quest/side_quests/sq024/entities/sq024_checkpoint_marker.ent`
  (WolvenKit, from `basegame_3_nightcity.archive`).
- City race prefab sector:
  `quest_5aab979acf00452f.streamingsector` (Corpo Plaza / Wellsprings).
- Rewards: `$GAME/tools/redmod/tweaks/base/gameplay/static_data/database/quest_rewards/side_quests.tweak`.
- Venue catalogue and notes:
  `/home/suvikyi/.cache/neon-ascendancy/extracts/venues/`.

---

## Summary

- Vanilla has **one bespoke street-racing quest chain**, not a general race
  system: `sq024` (*The Beast in Me*, four legs) plus `mq056` (*The Distance*,
  the 2.1 repeatable wrapper that reuses the same four tracks). No other quest
  or activity starts a race. **[V]** (`questStartRace_NodeType` occurs only in
  those 9 phases.)
- A track is **fixed data in a quest prefab**: one `worldRaceSplineNode` (the AI
  racing line), 25–35 checkpoint **device entities** that each add 1 to a fact
  when the player drives through them, and separate trigger areas for start,
  finish, water and route recovery. **[V]**
- The start grid is a **community of five pre-placed cars with two occupants
  each**; the player's car is spawned at a fixed grid workspot. No opponent or
  grid slot is generated procedurally. **[V]**
- Opponents are driven by the native **`AIVehicleRacingCommand`** on the race
  spline with rubber-banding (20–150 m, no teleport catch-up). Passengers get
  scripted `ShootAt` commands; Claire shoots at rival drivers. **[V]**
- The race is **point-to-point, not lap-based**. There is no lap counter, no
  pit stop, and no standings table. **[V]**
- The live **position** HUD value and the countdown are engine-side: no script
  writes `UI_ActiveVehicleData.PositionInRace` or
  `sq024_city_race_countdown_end`. The **checkpoint** count is not engine-side:
  it is a world-device fact. **[V]/[I]**
- Placement is recorded only as **per-racer finish facts**; the phases contain
  no numeric place. Rewards are TweakDB records; only the Big Race wires a
  separate win reward. **[V]**
- Reusable: the AI vehicle commands, the checkpoint-device pattern, trigger
  areas, spline utility functions, and the vanilla HUD as a dumb display.
  Not reusable: runtime NPC-vehicle spawning, the engine's race-position logic,
  and any track that is not pre-placed in a prefab. **[V]/[I]**

---

## 1. How a race track is defined in data

### 1.1 Preset tracks, one per venue

Every leg uses a **preset track**: a single, non-looped spline with fixed start
and finish. There is no procedural route selection and no arbitrary start
point. The four tracks are:

| Leg | Vanilla quest | Track prefab (race prefab) | Checkpoints |
| --- | --- | --- | --- |
| City Center | `sq024_04_city_center_race` | `#sq024_pr_04_city_center_race` (+ `_04a` start, `_04b` end) | 31 |
| Santo Domingo | `sq024_02_pacifica_race` | `#sq024_pr_02_santo_domingo_race` (+ `_02a`, `_02b`) | 25 |
| Badlands | `sq024_03_badlands_race` | `#sq024_pr_03_badlands_race` (+ `_03a`, `_03b`) | 35 |
| Big Race (Westbrook/Watson) | `sq024_05_the_big_race` | `#sq024_pr_05_the_big_race` (+ `#mq056_pr_04_bigrace`) | 33 |

Checkpoint counts are the `maxCheckpoints` field of the
`VehicleRaceQuestEvent` in each phase. **[V]**

The `mq056` repeatable races reuse the same prefabs and add their own checkpoint
set (`#mq056_pr_*_checkpoints`), with the same counts. **[V]**
(`base/quest/minor_quests/mq056/phases/mq056_01_citycenter.questphase`, etc.)

Phantom Liberty adds no street-race phases: no `questStartRace_NodeType` or
`VehicleRaceQuestEvent` exists in the EP1 quest data. Its car content is vehicle
contracts (steal/deliver), not racing. No `sa_*` / `mws_*` phase starts a race
either — the only `questStartRace_NodeType` nodes in the whole extract are the
nine `sq024`/`mq056` files above. **[V]**

The city track is the only one converted in full in this session; its spline is
**5.75 km** long, non-looped, with a 100 m/s speed section and 7 m left/right
offsets (narrowing to 4.5 m at one point). The other three quest sectors
contain the same `#sq024_spl_*_spline` node names, which is consistent with the
same structure. **[V for the names, I for the full structure]**

### 1.2 Resource and node types

| Layer | Type | Role |
| --- | --- | --- |
| Race line | `worldRaceSplineNode` with `Spline` / `SplinePoint`, `worldRaceSplineNodeOffset`, `worldSpeedSplineNodeSpeedChangeSection` | AI racing line, width and speed sections |
| Traffic speed line | `worldSpeedSplineNode` (same points in the city prefab) | normal traffic speed profile |
| Checkpoint | `worldEntityNode` → `sq024_checkpoint_marker.ent` / `mq056_checkpoint_marker.ent`, containing `GenericDevice`, `GenericDeviceControllerPS`, `gameStaticTriggerAreaComponent`, `StreetSignWidgetComponent` + `RaceCheckpointSelector` | holographic gantry that adds a fact on player entry |
| Start / finish / recovery | `worldTriggerAreaNode` + `questTriggerNotifier_Quest` | phase `questTriggerCondition` volumes |
| Grid and crowd | community spawner (`CommunityProxyPS`) with entries `team_N_1`, `team_N_2`, `team_N_v` | pre-placed cars and people |
| Player grid slot | `worldAISpotNode` / workspot (city: `#sq024_ws_city_claire_truck`) | spawn/mount point for the player car |
| Route holo | prefab variant `gps_path` on `#loc_sq024_*_racetrack_gameplay` | the GPS route display |
| Race flow | `questVehicleNodeDefinition`, `questVehicleNodeCommandDefinition`, `questEventManagerNodeDefinition`, `questSpawnManagerNodeDefinition`, `questWorldDataManagerNodeDefinition`, `questFactsDBManagerNodeDefinition`, `questPauseConditionNodeDefinition`, `questRewardManagerNodeDefinition` | starting, driving, spawning, facts, gates, rewards |
| HUD | `hudCarRaceController` (ink) + `UI_ActiveVehicleData.PositionInRace` + `sq024_current_race_checkpoint_fact_add` | countdown, position, time, checkpoint count |

All rows are **[V]** from the converted city prefab and the city phase graph.

Important distinction: `questCheckpointNodeDefinition` in the quest graph is a
**save checkpoint** ("sq024_city_race_start/end"), not a race checkpoint. Race
checkpoints are world devices + fact gates. **[V]**

### 1.3 The checkpoint mechanism (the key finding)

The checkpoint marker is not a passive mesh and not a quest trigger. It is a
**GenericDevice with a static trigger volume**:

- `gameStaticTriggerAreaComponent` named `trigger`, 50 × 80 m footprint,
  30 m high. **[V]**
- On `ENTER`, with `isActivatorPlayer: 1`, it runs three operations:
  1. `FactsDeviceOperation` — `sq024_current_race_checkpoint_fact_add`,
     operation `Add`, value **1**, `executeOnce: 1`.
  2. `ToggleComponentsDeviceOperation` — disables `ui_back`, `ui_front` and
     `trigger` (the gantry disappears and cannot fire again).
  3. `PlaySoundDeviceOperation` — `sq024_race_countdown`.
  **[V]** (`sq024_checkpoint_marker.ent`, `GenericDeviceControllerPS.deviceOperationsSetup`)

The quest then gates on the fact. The city phase contains 30
`questShowWorldNode_NodeType` nodes that show checkpoints `001` … `030`, each
followed by a `questPauseConditionNodeDefinition` waiting for
`sq024_current_race_checkpoint_fact_add` to become greater than 0, 1, 2, …
29. **[V]** So checkpoint order is enforced by *only having the next gantry's
trigger active*.

The fact is seeded to **1** at race start (not 0), so the first gate is already
counted; the 30 driven gates `001` … `030` bring the total to 31, matching
`maxCheckpoints: 31`. The marker sequence runs `000` … `030`; `030` carries the
`RaceFinish` LCD face. The actual finish detection is a separate
`worldTriggerAreaNode`, not the marker device. **[V]**

The marker's LCD face is selected by `RaceCheckpointSelector`:
`LCDScreens.RaceCheckpointLeft` / `RaceCheckpointRight` for normal gates and
`LCDScreens.RaceFinish` for the finish. There is no logic in the selector; it is
only the screen texture. **[V]**

### 1.4 What is *not* used

- No per-checkpoint **mappins**. The route is a prefab holo path (`gps_path`
  variant), not map markers. **[V]**
- No **trigger areas** for normal checkpoints. Only start, finish, water,
  sharp-turn and backwards-warning volumes exist in the phase. **[V]**
- No **laps**. The spline has `looped: 0`, and there is no lap counter or lap
  fact anywhere in the phases or HUD. **[V]**
- The Big Race has four `questMappinManagerNodeDefinition` nodes, but they are
  objective/POI markers, not checkpoint logic. **[V]**

---

## 2. Grid, opponents, driving, rubber-banding, crashes, finish

### 2.1 Fixed start and finish

Start and finish are fixed per track. The grid is the community's pre-placed
layout inside the race prefab; the phase only *activates* the community
(`questCommunityTemplate_NodeType { action: Activate, communityEntryName: None,
communityEntryPhaseName: default }`). **[V]** No start, finish, grid slot or
checkpoint position is randomized. Race-wise, the player's only choices are
the car and, in the Big Race, whether to follow Sampson. **[V]**

City evidence:

- Community `#sq024_com_city_race` (and the `mq056` twin
  `#mq056_com_city_race`) has five teams:
  `team_1_1`/`team_1_2`/`team_1_v` … `team_5_1`/`team_5_2`/`team_5_v`.
- Character records are faction racers (Tyger Claws, Mox, 6th Street,
  Valentino, corporate) and the vehicles are quest cars (Caliburn, Shion,
  Emperor, etc.). **[V]**
- The phase assigns `team_N_1` to `seat_front_left` and `team_N_2` to
  `seat_front_right`, `isInstant: 1` for the initial line-up. **[V]**
- Claire is assigned to the player's car `seat_front_right`. **[V]**
- The player's own car is spawned by
  `questSpawnPlayerVehicle_NodeType { vehicle: "Currently Active Car",
  positionRef: #sq024_ws_city_claire_truck }`; Claire's truck is the same slot
  when the player chooses her car. **[V]**
- The phase contains no grid coordinates. The five car transforms live in the
  community spawner inside the race prefab; the phase turns the community on
  and assigns seats. **[V]**

Start trigger: `#sq024_tr_begin_city_center_race_small`. Finish trigger:
`#sq024_tr_city_race_finish`. Water and sharp-turn recovery triggers:
`#sq024_tr_city_race_in_water_000/001`, `#sq024_tr_city_race_sharp_turn_000/001`,
`#sq024_tr_city_backwards_checkpoint`. **[V]**

### 2.2 How opponents are driven

Each opponent car gets a `questVehicleNodeCommandDefinition` whose
`questVehicleCommandParams.type` is **`Racing`**, carrying a
`questvehicleRacingParams` block. **[V]**

City race values (all five cars identical):

| Field | Value |
| --- | --- |
| `splineRef` | `#sq024_spl_city_race_spline` |
| `rubberBanding` | 1 |
| `rubberBandingParam.targetRef` | local player |
| `minDistance` / `maxDistance` | 20 / 150 m |
| `stayInFront` | 1 |
| `teleportToCatchUp` | 0 |
| `stopAndWait` | 0 |
| `preciseLevel` | 1 (2 on Badlands and Big Race) |
| `closest` | 1 (start from nearest point) |
| `pushOtherVehiclesAside` | 0 |
| `reverseSpline` / `backwards` | 0 |

**[V]** (`sq024_04_city_center_race.questphase`, 19 racing commands across the
phase; values above are the five real racer commands.)

The command maps to the native **`AIVehicleRacingCommand`**
(`refs/cyberpunk/orphans.swift:48604`) and is applied by
`AIDriveRacingCommandHandler` (`refs/cyberpunk/cyberpunk/ai/commands/aiDriveCommandHandler.swift:557`).
The script-side handler copies `splineRef`, rubber-band target, min/max
distance, `stayInFront`, `teleportToCatchUp` into the AI command. **[V]**

`preciseLevel` is not exposed in the redscript command class; it is a quest
parameter only. Its exact effect is engine-side. **[I]**

The `stayInFront` semantics are engine-side; the value says the AI should
prefer to stay ahead of the rubber-band target (the player), within the min/max
window. Do not copy this as "the AI always wins": the player can still pass, and
the AI has no teleport catch-up. **[I]**

Taken together, the values describe the intent: keep the pack within
20–150 m of the player, never let it teleport, never let it stop and wait, and
raise `preciseLevel` on the fast Badlands/Big Race tracks. The actual speed
modulation is native and not in the script dump. **[V values, I behaviour]**

Claire/traffic use `Move_On_Spline` (`questvehicleOnSplineParams`) on the
non-suffixed spline (`#sq024_spl_city_race`) rather than `Racing`. Those
commands use 20–70 m rubber-banding and `stayInFront: 0`; some of them set
`teleportToCatchUp: 1` so the pace car can snap back to the player. **[V]**

### 2.3 Gunners and drive-by combat

The race is a two-person format (driver + gunner). The city phase contains 73
`questCombatNodeDefinition` nodes:

- Claire (`#claire`) gets 13 `questCombatNodeParams_ShootAt` commands against
  rival drivers (`team_N_1`).
- Each rival passenger (`team_N_2`) gets 12 `ShootAt` commands against other
  passengers/drivers.
- The targets are entity references inside `#sq024_com_city_race`; the command
  params are `AIInjectCombatThreatCommandParams`. **[V]**

So combat is scripted aggro, not a separate vehicle-combat AI. It creates the
crashes and chaos; it is not required to finish. **[I]**

### 2.4 Crashes and damage

- The player and the player's mounted vehicle are set **Immortal** during the
  race; Claire is Invulnerable. **[V]** (`questCharacterManagerParameters_SetMortality`
  in `sq024_04_city_center_race`, phase 152.)
- Rival vehicles are set **Mortal** at the start. **[V]**
- Each rival has a `questCharacterHealth_ConditionType { comparisonType: Equal,
  percent: 0 }` pause condition in the finish phase. A destroyed rival cannot
  cross the finish, so the health-0 branch is its retirement path. **[V for the
  condition; I for the exact branch outcome]** (There is no repair or respawn
  for rivals.)
- The player's vehicle is repaired by `questRepair_NodeType` only in the
  route-recovery branch. **[V]**
- The Big Race's Sampson crash is a **scripted set piece**, not physics: a
  damage trigger (`#sq024_tr_big_sampson_damaged_area`), an AI trigger
  (`#sq024_tr_sampson_race_ai`), crash FX facts (`sq024_sampson_crashed`,
  `sq024_sampson_crash_fx_stop`) and dedicated splines. **[V]**

### 2.5 Leaving the route

The engine writes a fact `RacePlayerDistanceFromSpline`; the phase reads it
(no script sets it except a reset to 0 at the start). **[V]/[I]**

City recovery logic:

1. If the player is inside either water trigger **or**
   `RacePlayerDistanceFromSpline > 50`, show the warning
   `questWarningMessage_NodeType` "RETURN TO THE RACE". **[V]**
2. If the player is outside both water areas **and** the distance is `< 40`,
   hide the warning, wait 2 s (anti-flicker). **[V]**
3. Run the recovery sub-phase: fade, `questRepair_NodeType` on
   `#mounted_vehicle`, then `questGoBackToRace_NodeType`. **[V]**

`questGoBackToRace_NodeType` is a quest node with no parameters; the engine
puts the vehicle back on the race spline near its progress. **[I]** The
`RacePlayerDistanceFromSpline` fact is written by the engine, not by the
redscript in `refs/cyberpunk`. **[V absence]**

### 2.6 Finish

- Player: `#sq024_tr_city_race_finish`, `isPlayerActivator: 1`, `IsInside`.
  On entry the phase sets `sq024_v_finished_cc_race = 1`. **[V]**
- Each rival: the same trigger with the rival vehicle as activator. On entry
  the phase **adds 1** to its own finish fact
  (`sq024_city_rcr_finish_1` … `_5`) and to
  `sq024_city_race_enemy_finish`. **[V]**
- After finishing, each rival is switched from `Racing` to `Move_On_Spline` on
  its own short end spline (`#sq024_spl_city_end_racer_000` … `_004`,
  `stopAtPathEnd: 1`) so it decelerates and parks instead of piling up at the
  line. **[V]**
- The player's car is likewise put on `#sq024_spl_city_end_player` with
  `Move_On_Spline` to stop at the finish. **[V]**
- End sequence: `VehicleRaceQuestEvent { mode: RaceEnd, maxPosition: 6,
  maxCheckpoints: 31 }` to `#mounted_vehicle`; `questStopRace_NodeType`;
  `disable_combat_events = 1`; remove/add restrictions; crowd and audio
  cleanup. **[V]**
- There is no lap and no time-based tie-break. Finish order is simply the order
  in which vehicles enter the finish trigger. **[V]**

### 2.7 Abort / police

`sq024_race_prevention_interrupt.questphase` watches `wanted_level > 0`. If the
player gets a wanted level during a race, it force-brakes the player vehicle,
disables door interactions, ejects player and Claire, fails the race
(`sq024_prevention_fail`) and sets `sq024_claire_pissed`. **[V]** The `mq056`
repeatable races have the same `prevention_fail` phase. **[V]**

---

## 3. Start/end flow, UI, rewards and placements

### 3.1 Start sequence

1. Approach venue, call Claire, sit on the bench, take the shard, get in the
   car. Journal objectives drive this; no race system is running yet. **[V]**
2. `questCharacterMount_ConditionType { childIsPlayer: 1, OnMount }` detects
   the player in the car; set `sq024_city_race_inside_car = 1`; wait 2 s;
   objective "Wait for the race to start". **[V]**
3. Force brake on (`questToggleForceBrake_NodeType`), add
   `GameplayRestriction.VehicleBlockExit`, `BlockAllHubMenu`,
   `VehicleBlockRadioInput`. **[V]**
4. Pre-race setup phase: show the `checkpoints` prefab variant, show the
   `gps_path` holo route, make player/vehicle immortal, make rivals mortal,
   reset the checkpoint factor, add `VehicleBlockExit`, set tier. **[V]**
5. `questStartRace_NodeType` (no parameters). This is the hand-off to the
   engine race manager. **[V]**
6. Engine countdown, then the race. No script sends `CountdownStart`; the fact
   `sq024_city_race_countdown_end` has no script setter, only a `> 0` gate.
   Therefore the countdown/`CountdownStart`/`RaceStart` events are engine-side
   (or an engine-driven scene), not quest-graph logic. **[I]**

The Big Race is the exception: it explicitly sends
`VehicleRaceQuestEvent { mode: PreRaceSetup, maxPosition: 6,
maxCheckpoints: 33 }` before the start, probably because its intro scene needs
the HUD set up earlier. **[V for the event, I for the reason]**

### 3.2 HUD

`hudCarRaceController` (`refs/cyberpunk/cyberpunk/UI/vehicles/car_race_hud.swift`)
is a normal ink HUD controller with four fields:

- countdown animation (`Countdown`)
- race position (`m_RacePosition`, "N/M")
- race time (`m_RaceTime`)
- checkpoint count (`m_RaceCheckpoint`, "N/M")

It is driven by `VehicleRaceQuestEvent` modes
`PreRaceSetup → CountdownStart → RaceStart → RaceEnd → Disable` and by
`ForwardVehicleRaceUIEvent`. **[V]**

Mechanics:

- `PreRaceSetup` pushes `UIGameContext.VehicleRace`, sets `maxPosition` and
  `maxCheckpoints`, hides the HUD.
- `CountdownStart` plays the countdown animation and shows position/counters.
- `RaceStart` records the sim-time origin for the clock.
- `RaceEnd` stops the clock.
- `Disable` pops the game context and unregisters the fact listener. **[V]**
  (`vehicleComponentPS.swift:1769-1783`, `vehicleComponent.swift:4991-5027`)

The HUD registers a QuestSystem listener on the **hardcoded** fact
`sq024_current_race_checkpoint_fact_add` and reads
`UI_ActiveVehicleData.PositionInRace` from the mounted vehicle blackboard. It
also writes `sq024_current_race_player_position` each time the position
changes. **[V]** (`car_race_hud.swift:71-130`)

There is **no lap field**, no rival names, no gaps, no speed, and no minimap
route. The HUD is a small sprint display, not a racing telemetry system. **[V]**

### 3.3 Where position comes from

No script in `refs/cyberpunk` writes `PositionInRace`; the only access is the
HUD read. The vanilla quest never sets it either. Therefore the engine race
manager populates it. Its inputs are not in the script dump; the most likely
model is race-spline progress for the player and the AI (the AI racing commands
run on the same spline), but that is **[I]**, not verified.

The quest-side "place" phases are **orphans**:

- `sq024_race_counter.questphase` and `sq024_race_counter_city.questphase`
  compute `sq024_player_race_place_counter` / `sq024_current_place_count` by
  comparing the player's distance to a checkpoint against each rival's
  distance to the same checkpoint (`questDistanceVsDistanceComparison_ConditionType`).
- No other phase references either file, and no phase reads the place facts.
  They are leftover prototypes, superseded by the engine HUD. **[V]**

For a new system this is good news: you can compute your own position with
`AIScriptUtils.CalculateDistanceToEndFrom` on the race spline
(`refs/cyberpunk/orphans.swift:23242-23252`) and write it to the blackboard if
you reuse the vanilla HUD.

### 3.4 Rewards and placements

Reward records are plain TweakDB:

| Record | Content |
| --- | --- |
| `sq024_finish_city_race` | 486 XP, 728 Street Cred |
| `sq024_finish_santo_domingo_race` | 486 XP, 728 SC |
| `sq024_finish_badlands_race` | 486 XP, 728 SC |
| `sq024_finish_big_race` | 728 XP, 1092 SC |
| `sq024_win_city_race` | 3,860 eddies |
| `sq024_win_badlands_race` | 3,860 eddies |
| `sq024_win_santo_domingo_race` | 3,860 eddies |
| `sq024_win_big_race` | 5,790 eddies |

**[V]** (`side_quests.tweak:865-1070`)

What is actually wired in the phase graphs:

- Every qualifier phase grants its `*_finish_*` record at the end. **[V]**
- The Big Race grants **both** `sq024_win_big_race` and
  `sq024_finish_big_race`. **[V]**
- No qualifier phase references its `sq024_win_*` record. The three 3,860
  eddie records exist but are **not wired** in any phase. **[V]**
- `sq024.questphase` also grants `sq024_finish_big_race` in its cleanup. **[V]**

Placement itself: the phase records per-racer finish facts, but no numeric
place and no "qualification" fact. The "top three in two races" rule from the
wiki is not implemented as a fact in the phase data we have. It may be handled
by dialogue/scene branching, or it may be narrative only. **[V absence]/[I]**

The `mq056` repeatable wrapper (*The Distance*) adds an entry fee and a payout
through its bench/POI interaction and its own reward node; the phase we read
only grants `sq024_finish_city_race`. The 2,000 €$ entry and 10,000 €$ payout
(wiki amounts) are not represented as quest facts in the phase we read.
**[V for the phase, I for the interaction]**

---

## 4. What can and cannot be reused

### 4.1 Reusable

| Piece | How |
| --- | --- |
| `AIVehicleRacingCommand` | Native class; construct in redscript and queue an `AICommandEvent`, or author a `questVehicleNodeCommandDefinition` with `type: Racing`. **[V]** |
| `AIVehicleOnSplineCommand`, `AIVehicleToNodeCommand`, `AIVehicleDriveToPointAutonomousCommand`, `AIVehicleFollowCommand`, `AIVehicleChaseCommand` | Public native command classes with public fields (`orphans.swift:48514-48620`, `32443`). **[V]** |
| Checkpoint device pattern | Clone/author an entity with a `GenericDeviceControllerPS`, a `gameStaticTriggerAreaComponent` and a `FactsDeviceOperation` to increment a fact. **[V]** |
| Trigger areas + quest phases | Start/finish/recovery volumes and phase gates are normal world/quest data. **[V]** |
| Spline math | `AIScriptUtils.GetClosestPointOnSpline`, `GetStartPointOfSpline`, `GetEndPointOfSpline`, `CalculateDistanceToEndFrom` (`orphans.swift:23242-23252`). **[V]** |
| HUD as a dumb display | Send `VehicleRaceQuestEvent` to the mounted vehicle, set the checkpoint fact, write `PositionInRace`. No engine race needed. **[V]** (the event path is normal event dispatch; queueing from redscript is **[I]** but the classes are public.) |
| Race assets (gantries, LCD screens, markers) | `sq024_checkpoint_marker.ent` and the four track prefabs are normal vanilla assets. **[V]** |

### 4.2 Not reusable / hard limits

| Limit | Why |
| --- | --- |
| Runtime NPC-vehicle spawning | No script API. `CommunitySystem` exposes only density/crowd null areas; `DynamicSpawnSystem` only counters; the only transform spawn is `PreventionSpawnSystem.RequestUnitSpawn` (NCPD pipeline). A race grid must be a pre-placed community spawner activated by a phase. **[V]** (`docs/research/living-world-site-modeling.md` §0.4) |
| Engine race-position and countdown | No script writes `PositionInRace` or `sq024_city_race_countdown_end`; the engine race manager is a black box. **[V]/[I]** |
| `questStartRace` / `questStopRace` / `questGoBackToRace` from redscript | They are quest-node types only; not exposed as redscript classes. You can use them only by authoring a `.questphase`. **[V]** |
| Laps, standings, gaps, names, speed | The HUD has no fields for them; the race data has no lap model. **[V]** |
| Arbitrary/generated tracks | A race needs a prefab with a `worldRaceSplineNode` and checkpoint entities. Mods can declare an existing vanilla prefab in `phasePrefabs`; authoring a new spline prefab needs an ArchiveXL world edit (medium risk). **[V]/[I]** |
| More than ~6 racers / 31 checkpoints *in the vanilla HUD* | Values are fields, so you can pass other numbers, but the layout and animation were authored for 6/31. **[I]** |
| The `sq024` fact names | The checkpoint entity and HUD hardcode `sq024_current_race_checkpoint_fact_add`. Reusing vanilla markers means using that fact; running two races at once collides. **[V]** |

One vanilla quirk to avoid copying: the race start resets a **typo** fact
`sq024_current_race_chekpoint_fact_add` (missing "c") in one phase, while the
device and HUD use the correctly spelled one. Two facts, one of them dead.
**[V]**

---

## 5. Ambient street racing on the mod's road graph

Short answer: **not as a real off-screen simulation, and not with the vanilla
race command.** It is possible to fake a small AI race near the player with
waypoint commands, but spawning and streaming are the blockers.

### 5.1 The road graph is not a spline graph

`all.traffic_persistent` is 33,953 `worldTrafficLanePersistent` records with
outlines, lengths, widths, speeds, `inLanes`/`outLanes`, `playerGPSInfo` and
`crowdCreationInfo` (`docs/research/game-data-extraction.md` §1.7). It is a
complete drivable graph, but the lanes are **data**, not world nodes. There is
no `NodeRef` for a lane. **[V]**

Consequences:

- `AIVehicleRacingCommand` and `AIVehicleOnSplineCommand` cannot consume a lane
  outline; they require a `NodeRef` to a `worldRaceSplineNode` /
  `worldSpeedSplineNode`. **[V]**
- `AIVehicleToNodeCommand` also requires a `NodeRef`. **[V]**
- `AIVehicleDriveToPointAutonomousCommand` takes a `Vector3` target
  (`orphans.swift:32443`). It is the natural command for the lane graph because
  it needs no `NodeRef`; it is the command behind the game's autonomous driving,
  so it is the right bet for lane routing, but its internal pathing is
  engine-side. **[V for the signature, I for the routing behaviour]**
- With `DriveToPointAutonomous` you must sequence waypoints yourself and
  implement speed/rubber-banding in script; there is no built-in racing line or
  catch-up. **[I]**

### 5.2 Spawning is the hard blocker

- There is **no script-side "spawn an NPC vehicle and driver" API**. The
  community system exposes only crowd-null areas and density. **[V]**
- The ways to get an NPC vehicle are:
  1. a pre-placed community spawner activated by a phase (the vanilla race
     method), or
  2. the NCPD pipeline — `PreventionSpawnSystem.RequestUnitSpawn(recordID,
     transform)` for units and `RequestChaseVehicle(vehicleRecordID,
     passengerRecordIDs, strategy)` for cars — which is police-specific and not
     a general race spawner. **[V]**
- Traffic vehicles are engine-owned. `TrafficSystem` exposes only
  `IsPathIntersectingWithTraffic` and `FindEntitiesNearPlane`; there is no
  public API to assign a lane, spawn a traffic car, or command a traffic car.
  **[V]** (`orphans.swift:51978`)
- Community entries only exist inside the player's streaming bubble; a race
  that runs while the player is elsewhere is not simulated. **[I]** (streaming
  behaviour documented in `world-access.md` / `living-world-site-modeling.md`.)
- A pre-placed spawner is tied to one area. An "ambient race anywhere on the
  graph" would need either a spawner that follows the player (not possible
  without a world edit) or a network of fixed spawners. **[I]**

### 5.3 What ambient racing could look like

Feasible, but staged rather than simulated:

- Put a small race-start spawner at a fixed spot on a suitable road loop.
- When the player is near, activate the community, give the cars
  `DriveToPointAutonomous` waypoints around a short loop, and despawn after
  N laps or when the player leaves.
- No player involvement: skip the vanilla HUD (`VehicleRaceQuestEvent` needs a
  mounted player), skip `questStartRace`, and just let the AI drive. The player
  sees a race, not a race they can join.
- Do not expect the race to continue off-screen, produce results, or survive a
  save/load in a consistent state. Persist an abstract result (who won, when)
  rather than live racer positions.

Verdict: a road-graph ambient race is a **near-player visual event**, not a
world simulation. If Neon Ascendancy needs races that exist without the player,
model them abstractly (timer + result + occasional staged visual) rather than
simulating 34k lanes.

---

## Design implications

1. **Author races as phase + prefab content, not pure redscript.** Grid,
   splines, checkpoint devices and finish triggers are world entities. A
   redscript-only race has no spawn and no track.
2. **Reuse the four vanilla track prefabs before building new geometry.** They
   are public roads with a race spline, 25–35 checkpoint gantries, start/finish
   triggers and end-parking splines. A Neon phase can declare the prefab and
   use the same `NodeRef`s. Do not reuse Claire, the teams or the story.
   The one unproven step is whether a mod-authored `phasePrefabs` entry makes
   the prefab's `NodeRef`s resolve; `docs/research/world-access.md` §4.1 marks
   the same operation as the outstanding in-game spike. **[I]**
3. **Model the track as: spline + ordered checkpoint devices + start/finish
   triggers.** Do not use mappins for checkpoints and do not use a single
   trigger volume for the whole route.
4. **Use `AIVehicleRacingCommand` for opponents, not traffic AI.** It is the
   only command with a racing line, `preciseLevel` and rubber-banding. Keep the
   vanilla 20–150 m window and no teleport catch-up as the baseline.
5. **Keep the grid small and pre-placed.** Five rivals + player is the vanilla
   shape (6 positions). Each rival is one car with two occupants; only the
   driver is commanded, the passenger gets scripted `ShootAt` orders.
6. **Make the player vehicle immortal and rivals mortal.** Crashes should
   retire a rival, not end the race. Use scripted crash set pieces (Sampson
   style) for story beats, not physics.
7. **Recover the player by distance-to-spline, not by a reset button.** Warn at
   >50 m, repair, and put the car back on the spline (or re-issue `Racing` with
   `closest: 1`). The vanilla `questGoBackToRace_NodeType` is quest-only; in
   redscript use the spline utilities and a teleport/re-command.
8. **Record finish order yourself.** One trigger or one checkpoint per racer,
   append to an ordered array. Do not rely on the engine's `PositionInRace` for
   results; it is a display value with an undocumented algorithm.
9. **Compute live position from spline progress.** `AIScriptUtils.
   CalculateDistanceToEndFrom` gives a single scalar per vehicle on the same
   spline, which is enough for position and gaps. Write it to
   `UI_ActiveVehicleData.PositionInRace` if you reuse the vanilla HUD.
10. **Treat the vanilla HUD as a reusable shell with limits.** It can show
    countdown, position "N/M", time and checkpoint "N/M" for a mounted player.
    It cannot show laps, names, gaps or speed. For a richer race, author a Neon
    HUD and keep the vanilla one only as a fallback.
11. **Do not copy the hardcoded `sq024` fact names into a multi-race system.**
    If two races can overlap, clone the checkpoint entity with a Neon fact name
    (ArchiveXL) or gate races so only one is active. The vanilla marker and HUD
    both hardcode `sq024_current_race_checkpoint_fact_add`.
12. **No runtime NPC-vehicle spawn.** Every opponent must come from a community
    spawner in a prefab, activated by a phase. This is also the save-safe
    approach; a script-spawned convoy has no persistence.
13. **No laps unless you add them.** Vanilla splines are one-way and
    non-looped. A Neon race can loop by re-issuing commands, but the checkpoint
    fact and HUD counter are monotonic; implement lap state in your own system.
14. **Do not build ambient races on the traffic graph as a simulation.** The
    lanes have no `NodeRef`s, the racing command needs a spline, and there is no
    spawn API. Use a pre-placed near-player spawner with
    `DriveToPointAutonomous` waypoints, or simulate results abstractly.
15. **Keep qualification/reward rules in one place.** Vanilla records finish
    order but has no place fact and only wires the Big Race win reward. A Neon
    system should compute place explicitly and map place → payout in one
    table, rather than repeating the vanilla "finish reward + separate win
    record" split.

---

## Appendix — the four vanilla venues

| Venue | Location | Notes |
| --- | --- | --- |
| `loc_sq024_citycenter_racetrack` | Vista del Rey → Corpo Plaza → Wellsprings docks | city streets; finish at the docks |
| `loc_sq024_badlands_racetrack` | Brookland St, Laguna Bend dam | highway turnout; sandstorm/dust variant |
| `loc_sq024_santo_domingo_racetrack` | Brandon & Wollesen, Arroyo | industrial streets |
| `loc_sq024_watson_racetrack` | Pardey St, Charter Hill → Watson | Big Race; Sampson set piece |

All four are ordinary public road outside the race. The race prefabs are
quest-scoped, so a clean-slate boot does not load their splines, gantries or
grid communities until a phase declares the prefab. **[V]**
