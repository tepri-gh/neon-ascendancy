# Living-World Encounter Sites: Anatomy, Runtime Mechanics, and Data Model

**Status:** research complete (2026-11-24). Produced by read-only inspection of the
installed Cyberpunk 2077 **2.5** build
(`/home/suvikyi/Games/Cyberpunk 2077`), pinned
`WolvenKit.CLI 10.0.0-beta.1`, `refs/cyberpunk/` (script decompile),
`refs/RED4ext.SDK/` (native layouts), and the existing
`tools/extract-world.py` output in `dist/extract/`. Trial extractions were made
into `/tmp/site_model_research` only and deleted afterwards. Nothing in the game
directory, `refs/`, `data/`, `tools/`, or `src/` was modified.

**Scope:** model NCPD scanner hustles (`ma_*`), fixer gigs (`sts_*`, including
`sts_ep1_*`), and enemy/interior side sites (`mq*`/`sq*`/`mws_*`) as first-class
**physical sites** that Neon Ascendancy owns, garrisons, fights over, converts,
and monetizes — while vanilla's own quest content stays switched off (Option A).

**Question this document must answer:** if
`open_world_minor_activities.questphase`, `street_stories.questphase`, and the
main/side quest phases never run, what is still there, what is not, and what is
the cheapest Codeware-free way to make those places *alive* again?

---

## 0. TL;DR

1. **A gig is four independent layers, and only one of them is quest-gated.**
   - **Geometry / interior / props** live in `Exterior`/`Interior`-category
     streaming sectors and interior prefab variants; the `Interior` variants we
     sampled are `enabledByDefault: 1`, so they stream and render with no quest
     at all.
   - **The gameplay layer** — `worldAISpotNode` workspots,
     `worldPatrolSplineNode` patrol routes, `worldGuardAreaNode` guard areas,
     `worldDeviceNode` security areas/cameras/turrets/doors, and the community
     spawner entities (`CommunityProxyPS`, referenced as
     `#<site>_com_<crew>`) — is compiled into a
     **`Quest`-category sector** (`quest_<hash>.streamingsector`) that is bound
     to a **quest prefab**.
   - **The quest prefab is declared by the site's phase**:
     `phasePrefabs[0].prefabNodeRef = "#sts_wat_kab_07_streetstory"`.
     A prefab is only instantiated by the phase that declares it, so omitting
     the phase leaves **no workspots, patrols, guard areas, spawners, or
     security devices** (§2.7 is the one spike that confirms this in-game). The
     building is there; the inhabitants are not.
   - **The quest graph** (`questSpawnManagerNodeDefinition`,
     `questDeviceManager_NodeType`, `questToggleDoor`, journal, mappins) decides
     which community phases are on and which doors are powered. It is the only
     layer we lose by omitting vanilla phases — and it is the layer we can
     re-author.

2. **The best verified mechanism is data, not code.** A Neon-authored
   `.questphase` that (a) lists the vanilla `prefabNodeRef` in `phasePrefabs`
   and (b) contains one `questSpawnManagerNodeDefinition` →
   `questCommunityTemplate_NodeType { action: Activate, spawnerReference:
   #<site>_com_<x>, communityEntryPhaseName: <phase> }` gives back
   **hand-authored, animated, patrolling, guard-area-aware NPCs standing on the
   exact vanilla workspots**. This is the vanilla mechanism, uses no Codeware,
   no native spawn call, and no world edit.

3. **Site communities are dormant by default — measured, not assumed.** In the
   ep1 community registry, **5,278** communities have every entry
   `entryActiveOnStart = 1` (ambient crowds, police, vendors) and **5,031** have
   every entry `entryActiveOnStart = 0`. Every sampled gig/hustle community is
   in the second group: `{kab_07_com_enemies}` has 15/15 entries inactive,
   `{ma_wat_kab_07_com_tyger_claw}` 6/6 inactive, `{ma_wat_kab_07_com_tyger_claw_junkie}`
   1/1 inactive. **Nothing spawns at a site unless something activates it.**

4. **No script-side "spawn a puppet" API exists.** `CommunitySystem` exposes only
   crowd-null areas and density (`orphans.swift:51491`); `DynamicSpawnSystem`
   exposes only counters (`core/systems/dynamicSpawnSystem.swift:4-6`). The only
   transform-explicit spawn function in the script surface is
   `PreventionSpawnSystem.RequestUnitSpawn(recordID, spawnTransform)`
   (`core/systems/preventionSpawnSystem.swift:8`), and it is the NCPD pipeline.
   Treat it as a Tier-C fallback, not the foundation.

5. **What we can *read* at runtime is excellent.** `ResolveNodeRef`
   (`orphans.swift:34317`) turns an extracted `NodeRef` into a `GlobalNodeRef`;
   `GetFixedEntityIdsFromSpawnerEntityID` (`orphans.swift:34038`) enumerates a
   community spawner's live puppets by entry name; and
   `EntitySpawnerEventsBroadcaster.RegisterSpawnerEventPSListener`
   (`orphans.swift:34042`) delivers `Spawn`/`Despawn`/`Death`
   (`orphans.swift:3537`) per community entry. **Garrison strength and kill
   tracking are event-driven, no polling, no per-frame cost.**

6. **Inventory:** 329 `ma_*` sites, ~110 `sts_*` gigs (100 base-game codes +
   10 Dogtown `sts_ep1_*`), 56 `mws_*` mini world stories → **~495 content
   sites, ~5 per sub-territory** across the current 96 sub-territories. 198
   `ma_*` and 95 `sts_*` sites ship their own `.community`; the compiled
   registry already inlines all of them, so no `.community` parsing is strictly
   required.

7. **`world.db` extends cleanly** with a `world_sites` spine plus normalized
   child tables (`site_spots`, `site_patrols`, `site_devices`, `site_doors`,
   `site_communities`, …). Every column proposed below is extractable today from
   data we already pull, plus one new `Quest`-sector stage. §4 has the DDL.

8. **One in-game spike closes the last gap** (§2.7): confirm that activating a
   vanilla `#prefab` from a Neon phase makes its `NodeRef`s resolve. Everything
   else in this report is verified offline.

---

## 1. Empirical anatomy of a site

### 1.1 The four layers

| Layer | Where it lives | Streams without a quest? | Example |
| --- | --- | --- | --- |
| **A. Architecture / interior shell** | `Exterior` grid sector (`exterior_<x>_<y>_<z>_<variant>.streamingsector`), nested prefab variants | **Yes** — variant `Interior` has `enabledByDefault: 1` | `exterior_-5_5_0_2.streamingsector` hosts `loc_sts_wat_kab_07_casino_bar_*` |
| **B. Default props / devices / doors** | Same Exterior sector + `_external/proxy/*.mesh`; default device variant | **Yes** | `#kab_07_gate_001`, `#kab_05_entrance_door_002` |
| **C. Gameplay layer** (spots, patrols, guard areas, spawners, security areas, loot prefabs) | `Quest`-category sector bound to `questPrefabNodeRef` | **No** — needs the quest prefab | `quest_36ce86f6ae0770ea.streamingsector` for `#sts_wat_kab_07_streetstory` |
| **D. Quest graph** (activation, doors, variants, journal, mappins) | `.questphase` resources | **No** — this is what Option A removes | `sts_wat_kab_07_combat.questphase` |

Verified with `blocks/all.streamingblock` (`23,718` descriptors): categories are
`Exterior 15,121`, `Navigation 3,811`, `Interior 2,425`, `Quest 2,358`,
`AlwaysLoaded 3`. Only `Quest` descriptors carry a non-zero
`questPrefabNodeRef`; only they contain the AI/workspot/patrol/guard node
families. Ep1 has its own block (`2186` descriptors in Dogtown: `Interior 969`,
`Exterior 835`, `Quest 381`, `AlwaysLoaded 1`).

### 1.2 The prefab gate — the single most important structural fact

Every sampled site phase declares exactly one prefab:

```json
"phasePrefabs": [ { "$type": "questQuestPrefabEntry",
  "prefabNodeRef": { "$type": "NodeRef", "$storage": "string",
                     "$value": "#sts_wat_kab_07_streetstory" } } ]
```

| Site | `phasePrefabs[0].prefabNodeRef` | Quest sector |
| --- | --- | --- |
| `ma_wat_nid_30` | `#loc_ma_wat_nid_30_openworld` | `quest_7e741456ad3217ad` |
| `ma_wat_kab_07` | `#ma_wat_kab_07` | `quest_b0269e4aed881cea` |
| `ma_std_arr_06` | `#ma_std_arr_06_openworld` | — |
| `ma_hey_gle_104` | `#loc_ma_hey_gle_104_openworld` | — |
| `ma_wat_lch_05` | `#loc_ma_wat_lch_05_openworld` | — |
| `sts_wat_kab_07` | `#sts_wat_kab_07_streetstory` | `quest_36ce86f6ae0770ea` |
| `sts_wat_kab_05` | `#sts_wat_kab_05_streetstory` | `quest_79a20bdef2dd4fe2` |
| `sts_wat_kab_04` | `#sts_wat_kab_04_streetstory` | — |
| `sts_wat_nid_01` | `#sts_wat_nid_01_streetstory` | — |
| `sts_hey_spr_01` | `#sts_hey_spr_01_streetstory` | — |
| `sts_ep1_06` (Zembinsky) | `…/loc_sts_ep1_06_prefab7J2LN5A/…#sts_ep1_06_streetstory` | `ep1/quest_02041ee18c2dd517` |

Two consequences:

- **Omitting the phase removes layer C.** The prefab is never instantiated, so
  the workspots/patrols/guard areas/spawners do not exist. Interior geometry and
  default props (layers A/B) still do.
- **The gate is a string we can name.** A Neon-authored phase can reference the
  same `NodeRef` and get the same prefab with the same nodes. This is the lever
  the whole design pivots on.

`open_world_minor_activities.questphase` and `street_stories.questphase` are
**pure dispatchers**: 34 and 11 `questPhaseNodeDefinition`s with
`phaseResource` paths plus journal/mappin pause conditions, `inplacePhases: 0`,
`phasePrefabs: 0`. Nothing is inlined; dropping them from the root `.quest`
removes the whole per-site phase tree cleanly.

### 1.3 Node census of sampled sites (hard evidence)

`sts_wat_kab_07` — interior casino/bar gig, file
`quest_36ce86f6ae0770ea.streamingsector`, `category: Quest`, **132 nodes / 132
instances, `persistentNodes: 132`** (every node persistent, i.e. not
individually streamed):

| Node type | Count | Notes |
| --- | --- | --- |
| `worldAISpotNode` | **79** | 79 distinct workspots, each with a `workspot` resource and `markings` |
| `worldTriggerAreaNode` | 30 | mission volumes (`tr_entrance_forced`, `tr_garage`, `tr_sniping_spot`) |
| `worldPatrolSplineNode` | **7** | 2–4 points each, points are `#workspot` refs |
| `worldGuardAreaNode` | **5** | each linked to `#kab_07_com_enemies`, `…_hard_mode`, `#kab_07_com_backup` |
| `worldSpeedSplineNode` | 4 | vehicle arrival/departure |
| `worldPopulationSpawnerNode` | 3 | `Character.ow_regina_driver`, fixer car, backup car |
| `worldSmartObjectNode` | 2 | cover objects |
| `worldCrowdNullAreaNode` | 1 | crowd suppression inside the venue |
| `worldAudioSignpostTriggerNode` | 1 | — |

`ma_wat_nid_30` — NCPD hustle (drone scan + hidden stash), 16 nodes:
6 `worldAISpotNode` (drone scan workspots, markings `enemy02a`), 2
`worldPatrolSplineNode` (drone routes), 2 `worldGuardAreaNode`, 2
`worldTriggerAreaNode`, **3 `worldDeviceNode`** (two `security_area_1.ent`, one
`security_system.ent`), 1 audio signpost.

`ma_wat_kab_07` — NCPD hustle (rooftop Tyger Claws stash), 30 nodes:
14 `worldAISpotNode`, 4 `worldPatrolSplineNode`, 4 `worldGuardAreaNode`, 3
`worldDeviceNode`, 2 `worldTriggerAreaNode`, 1 crowd-null area, 1
interesting-conversations area.

`sts_ep1_06` (Zembinsky, Dogtown) — 23 nodes: 11 `worldAISpotNode`, 7
`worldSplineNode` (`mq304_spl_*`), 5 `worldTriggerAreaNode`. This prefab is
**shared with side quest `mq304`** — a physical building, not a single gig. The
schema therefore separates *site* from *content binding* (§4.1).

### 1.4 Workspots carry semantics, not just coordinates

`worldAISpotNode` is richer than a marker:

```json
{ "$type": "worldAISpotNode",
  "debugName": { "$value": "{kab_07_ws_bottom_guard_}001" },
  "markings": [ { "$value": "kab_07_mid_do_drugs" } ],
  "isWorkspotInfinite": 0, "isWorkspotStatic": 0,
  "spot": { "Data": { "$type": "AIActionSpot",
    "resource": { "DepotPath": { "$value":
      "base\\workspots\\generic\\generic__stand_ground__guard__01.workspot" } },
    "ActorBodytypeE3": "Undefined", "clippingSpaceRange": 120 } } }
```

Extractable role hints, all deterministic:

| Signal | Example | Gameplay use |
| --- | --- | --- |
| `markings[]` | `kab_07_mid_do_drugs`, `enemy02a`, `kab_07_glitch` | group/beat semantics; matches community phase markings |
| workspot resource path | `generic__stand_ground__guard__01.workspot`, `patrolling_stand.workspot` | classify guard vs. ambient vs. patrol |
| `debugName` token | `_guard_`, `_patrol_`, `_alerted_`, `_backup_`, `_jotaro_`, `_sniping_` | officer / patrol / reinforcement / sniper / boss slots |
| `isWorkspotInfinite` | 0/1 | whether the pose loops |
| `ActorBodytypeE3` | `Undefined`/`Female`/`Male` | body-type-correct spawn selection |

Patrol splines are literally ordered workspot lists, so patrol routes and their
stop animations come from one join:

```json
{ "$type": "worldPatrolSplineNode",
  "debugName": { "$value": "{kab_07_spl_casino_patrol_route_}001" },
  "patrolPointDefs": [ { "Data": { "$type": "worldPatrolSplinePointDefinition",
      "node": { "$value": "#kab_07_ws_bottom_tyger_patrol_003" },
      "pointType": "Workspot" } }, … ] }
```

Guard areas bind communities to space (and to difficulty variants):

```json
{ "$type": "worldGuardAreaNode",
  "debugName": { "$value": "{kab_07_guard_area_casino_floor}" },
  "communityEntries": [
    { "$type": "AIGuardAreaConnectedCommunity",
      "communityArea": { "names": ["Enemy3","Enemy_smoker","Enemy4"],
                         "reference": { "$value": "#kab_07_com_enemies" } },
      "isPrimary": 1 }, … ] }
```

That `names[]` array is a free **per-entry whitelist per area** — exactly what a
"guard this floor" order needs.

### 1.5 Communities: entries, phases, and initial state

`.community` (`communityCommunityTemplate`) → `entries[]`
(`communitySpawnEntry`):

```
entryName          CName            "Enemy11", "Jotaro", "handgunner2"
characterRecordId  TweakDBID        "Character.kab_07_enemy_1st_floor_handgun"
spawnInView        bool
phases[]           communitySpawnPhase
  phaseName        CName            "0combat", "alarm", "default", "community",
                                    "distractHologram", "watching_stripper"
  alwaysSpawned    enum             default__false_ | true_ | false_
  timePeriods[]    { hour: Day/Night, quantity, isSequence, markings[],
                     spotNodeRefs[]  → "#kab_07_ws_1stfloor_tyger_002" }
```

The **compiled registry** (`worldCommunityRegistryNode` in
`always_loaded_1`, 10,324 communities / 43,971 entries) inlines the same data
**plus** the field that decides default liveness:

```json
{ "$type": "worldCommunityRegistryItem",
  "communityId": { "entityId": { "hash": "…" } },
  "communityAreaType": "Regular" | "Streamable" | "Background",
  "entriesInitialState": [ { "$type": "worldCommunityEntryInitialState",
      "entryName": "Enemy11", "initialPhaseName": "0combat",
      "entryActiveOnStart": 0 } ],
  "template": { "Data": { "entries": [ … ] } } }
```

`worldCommunityEntryInitialState` is confirmed in
`refs/RED4ext.SDK/include/RED4ext/Scripting/Natives/Generated/world/CommunityEntryInitialState.hpp`.

**Measured distribution (ep1 registry):**

| Bucket | Communities |
| --- | --- |
| Every entry active on start (ambient) | **5,278** |
| No entry active on start (quest/site) | **5,031** |
| No entries | 15 |

**Sampled site communities:**

| Community | Entries | `entryActiveOnStart` | `initialPhaseName` |
| --- | --- | --- | --- |
| `{kab_07_com_enemies}` | 15 | **0 / 15** | `0combat` |
| `{ma_wat_kab_07_com_tyger_claw}` | 6 | **0 / 6** | `default` |
| `{ma_wat_kab_07_com_tyger_claw_junkie}` | 1 | **0 / 1** | `default` |
| `{kab_07_com_ground_floor_crowd}` | 7 | 0 / 7 | `community` |

So even communities whose phase is named `default` are **not** live on start.
This is why "the gig is empty but the door is unlocked" will be the normal state
after Option A, and why one spawn-manager activation per site is sufficient to
bring it back.

Contrast (ambient): an all-active community has entries like
`police1/default`, `actor_01/a`, `client_f/spawn` — crowd and patrol filler that
must keep working for Night City to feel populated. Our design must not touch
those.

### 1.6 Devices, doors, security, elevators

`worldDeviceNode` is a normal entity node plus a class hint and device links:

```json
{ "$type": "worldDeviceNode",
  "debugName": "{ma_wat_kab_07_dvc_security_area}",
  "entityTemplate": "base\\gameplay\\devices\\security_systems\\security_area\\security_area_1.ent",
  "deviceConnections": [ { "deviceClassName": "CommunityProxyPS",
                           "nodeRefs": [ "#ma_wat_kab_07_com_tyger_claw" ] } ] }
```

Key facts:

- **`CommunityProxyPS` is the device↔community bridge.**
  `cyberpunk/network/squadNode.swift:2` shows it registers a spawner-event
  listener and resolves members with
  `GetFixedEntityIdsFromSpawnerEntityID(spawnerID, entryNames, game, out ids)`
  (`squadNode.swift:181`). A security area with a `CommunityProxyPS` child can
  therefore *find and command* its garrison — no quest needed beyond the spawn
  activation.
- **Device class comes from `entityTemplate`, not `deviceClassName`** (which was
  `None` on every sampled security-area node). Classification rule:
  `…/security_systems/security_area_1.ent` → security area,
  `…/security_systems/security_system.ent` → security system,
  `…/doors/…` → door, turrets/cameras/terminals/lifts by their template family.
- **Doors are gated by power, not by a lock flag.** Vanilla gig phases do:
  `questDeviceManager_NodeType { deviceAction: "ForcePower",
  deviceControllerClass: "DoorControllerPS", objectRef:
  "#kab_05_entrance_door_002" }`; `sts_wat_kab_04_openworld` uses `ForceOpen`
  and `QuestRemoveQuickHacks` on the same class. `ForcePower` /
  `ForceUnpower` / `ForceON` / `ForceOFF` / `ForceEnabled` / `ForceDisabled`
  are public `ActionBool` classes in
  `cyberpunk/devices/core/baseDeviceActions.swift:2001-2040`.
- **Turrets and security systems are ordinary devices**:
  `SecurityTurretControllerPS` + `ForceON`/`ForceOFF`,
  `SecuritySystemControllerPS` + `ForceDisabled`, `LiftControllerPS` +
  `ForceGoToFloor`/`ForceTeleportToFloor` with a `floorNumber` action property.
- **`worldInteriorMapNode`** (`coords: uint64`, deferred buffer) marks an
  interior with a minimap; **`worldInteriorAreaNode`** (a
  `worldTriggerAreaNode` subclass) marks interior volume. Either is a clean
  `is_interior` signal.

Script-side door control needs no quest graph:

```swift
// NodeRef hash -> GlobalNodeRef -> EntityID (native builds the NodeRef from the
// extracted uint64; see §2.4)
let target: GlobalNodeRef = ResolveNodeRef(nodeRef, Cast<GlobalNodeRef>(GlobalNodeID.GetRoot()));
if GlobalNodeRef.IsDefined(target) {
  let device = GameInstance.FindEntityByID(game, Cast<EntityID>(target)) as Device;
  let ps = device.GetDevicePS();                       // deviceComponentBase.swift:2
  GameInstance.GetPersistencySystem(game)
    .QueuePSEvent(ps.GetID(), ps.GetClassName(), new QuestForcePower());
}
```

`Entity.QueueEventForNodeID(nodeID: GlobalNodeRef, evt)` (`core/entity/entity.swift:10`)
is an even shorter route when we already hold the `GlobalNodeRef`.

### 1.7 What "interior" means in practice

Interiors are **not** site-named sectors. They are grid cells
(`interior_<x>_<y>_<z>_<variant>.streamingsector`, 2,425 of them) plus nested
prefab variants carried by the nearest Exterior sector. Site folders
(`base/worlds/03_night_city/sectors/c_watson/kabuki/loc_sts_wat_kab_07_casino_bar/`)
hold lighting/envprobe/mesh assets, never sectors.

Consequence for extraction: `is_interior` cannot come from a path token. Use
`worldInteriorAreaNode` / `worldInteriorMapNode` present in the site's Quest
sector, or "site anchor Z is above/below the nearest street surface" as a
fallback. Sampled interiors: `sts_wat_kab_04` (penthouse), `sts_wat_kab_05`
(ripperdoc clinic), `sts_wat_kab_07` (casino/bar), `sts_ep1_06` (Zembinsky),
`ma_wat_nid_30` (warehouse/roof) — 4 of 5 have interior volumes.

---

## 2. The critical engine question

### 2.1 What survives Option A

| Thing | Survives? | Why |
| --- | --- | --- |
| Building geometry, interior shell, navmesh | **Yes** | `Exterior`/`Interior` sectors, `Interior` variant `enabledByDefault: 1` |
| Default props, furniture, loot prefab *defaults* | **Yes** | baked into the same sectors |
| Doors, gates, cameras, turrets, terminals, lifts (as entities) | **Yes** | `worldDeviceNode` in the Exterior/Interior layer; PS defaults apply |
| Interior minimap | **Yes** | `worldInteriorMapNode` travels with the sector that hosts the interior |
| `worldAISpotNode` workspots | **No** | lives in the `Quest`-category prefab sector |
| `worldPatrolSplineNode` / `worldGuardAreaNode` | **No** | same |
| Community spawner (`CommunityProxyPS` device at `#<site>_com_<crew>`) | **No** | same |
| Security areas / cameras / turrets *placed in the Quest layer* | **No** | same |
| Community registry (all 10,324 templates) | **Yes** | `always_loaded_1`, always resident |
| Ambient crowds / vendors / police | **Yes** | `entryActiveOnStart = 1` communities, not site-bound |
| Site journals, mappins, fixer calls, rewards | **No** (by design) | journal/`.questphase` layer |

Two important corollaries:

1. **Doors are not "locked by default" in a special way.** The gig door is an
   ordinary `DoorControllerPS`; vanilla powers it from the phase. Without the
   phase it keeps whatever the entity default is — we did not measure per-door
   defaults offline, so the runtime must read the PS state and act. There is no
   "gig lock" flag to clear: we either power it (`QuestForcePower`), open it
   (`QuestForceOpen`), or leave it.
2. **Interior variants matter.** The `lockdown` device variant
   (`enabledByDefault: 0`) adds extra shutters/barricades during a gig. It will
   simply be absent — good for us: fewer artificial barriers to remove.

### 2.2 Mechanism comparison (all Codeware-free)

| # | Mechanism | Verified API evidence | Verdict |
| --- | --- | --- | --- |
| **A1** | Neon phase declares `phasePrefabs[].prefabNodeRef = "#<site>_streetstory"` | `sts_wat_kab_07.questphase`: `phasePrefabs[0]`, 10/10 sampled sites | **Primary.** Restores the whole gameplay layer |
| **A2** | Same phase adds `questSpawnManagerNodeDefinition` → `questCommunityTemplate_NodeType { action: Activate, spawnerReference, communityEntryName, communityEntryPhaseName }` | 185 definitions / 201 action entries across 28 sampled phases; actions `Activate`, `Deactivate`, `Reactivate` observed | **Primary.** Restores garrisons, per entry and per phase |
| **B** | Neon `.worldprefab` with a community spawner entity + Neon `.community`, placed via `phaseInstancePrefabs` | `questPhaseNodeDefinition.phaseInstancePrefabs` exists on every phase node; `worldPrefab` layout in `RED4ext.SDK/…/world/Prefab.hpp`; spawner behaviour in `cyberpunk/network/squadNode.swift` | **Best path to real faction swap.** Needs a prefab-authoring spike |
| **C1** | `PreventionSpawnSystem.RequestUnitSpawn(recordID, WorldTransform)` then `AIUseWorkspotCommand` / `AIPatrolCommand` / `AIMoveToCommand` | `preventionSpawnSystem.swift:8`; `AIComponent.SendCommand` `core/components/aiComponent.swift:11`; `AIPatrolCommand` `orphans.swift:48458`; `AIUseWorkspotCommand` `orphans.swift:48681`; `AIPatrolPathParameters.path: NodeRef` `orphans.swift:58286`; `AIMoveToCommand.movementTarget: AIPositionSpec` `orphans.swift:45302`; `AIPositionSpec.SetWorldPosition` `orphans.swift:34758` | **Fallback for dynamic waves / faction-swapped crews.** Spawn is real; side effects are inert (see below), but NCPD-pipeline behavior is unverified in-game |
| **C2** | Attitude/loyalty re-skin of an already-spawned vanilla garrison | `AttitudeAgent.SetAttitudeGroup`, `SetAttitudeTowards`, `SetAttitudeTowardsAgentGroup`, `SetAttitudeGroupUnsavable` — `orphans.swift:20443-20458` | **Good complement.** Makes a Tyger Claws crew fight for you without respawning |
| **D** | Native engine spawn via reverse-engineered `CommunitySystem` internals | No public layout; `RuntimeSystemWorldStreaming` is `unk` (`RED4ext.SDK/…/world/RuntimeSystemWorldStreaming.hpp`) | **Reject** for now |

#### Why `PreventionSpawnSystem` is *safer than it looks*

`RequestUnitSpawn` posts a ticket and the spawn system calls back into
`PreventionSystem`. The handler begins with a ticket lookup and **returns
immediately when the ticket is unknown**
(`core/systems/preventionSystem.swift:1615-1619`):

```swift
private final func OnPreventionUnitSpawnedRequest(request: ref<PreventionUnitSpawnedRequest>) -> Void {
  let ticketData: TicketData;
  if !this.m_agentRegistry.PopRequestTicket(request.requestResult.requestID, ticketData) {
    return;                     // ← no registration, no attitude change, no cleanup
  };
  …
}
```

So a third-party `RequestUnitSpawn` does **not** corrupt the NCPD agent registry.
What is unverified is whether the spawn system itself applies prevention-only
filters (wanted level, crowd-null areas, distance-to-player). That is a 15-minute
spike, not a design risk.

#### What is definitively *not* available

| Attempt | Result |
| --- | --- |
| `CommunitySystem.SpawnCommunity(...)` | Does not exist. Only `EnableDynamicCrowdNullArea`, `DisableCrowdNullArea`, `ChangeDensityModifier`, `ResetDensityModifier` (`orphans.swift:51491-51497`) |
| `DynamicSpawnSystem.RequestSpawn(...)` | Does not exist. Only `GetNumberOfSpawnedUnits`, `IsEntityRegistered`, `IsInUnmountingRange` (`core/systems/dynamicSpawnSystem.swift:4-6`) |
| `GameObject.Spawn(...)` / `GameInstance.SpawnPuppet(...)` | No such symbol anywhere in `refs/cyberpunk` |
| Starting a `.questphase` from script | `QuestsSystem` exposes facts + listeners only (`orphans.swift:18132-18151`) |

The last row is the one that shapes the architecture: **phases cannot be started
on demand from redscript.** They must already be running (or be started by the
journal/prefab state machine). Design accordingly (§2.6).

### 2.3 How to make a site "alive" — the concrete recipe

For each site we want live:

1. **Register the vanilla gameplay prefab** in our phase:
   `phasePrefabs[0].prefabNodeRef = "#<site>_streetstory"` (or the full
   `$/03_night_city/...` path from `questPrefabNodeRef`).
2. **Activate the garrison community**, one spawn-manager node per entry phase
   we want:
   ```
   questSpawnManagerNodeDefinition
     entries[0].type = questCommunityTemplate_NodeType
       action                    = Activate
       spawnerReference          = "#<site>_com_<crew>"
       communityEntryName        = "None"        // all entries
       communityEntryPhaseName   = "0combat"     // or "default"/"alarm"
   ```
3. **Power the entry devices** we want usable:
   `questDeviceManager_NodeType { DoorControllerPS, ForcePower, objectRef:
   "#<site>_entrance_door" }`.
4. **Optionally arm the security**: `SecurityTurretControllerPS` `ForceON`,
   `SecuritySystemControllerPS` `ForceEnabled`.
5. If the site should be *contested*, add `questCharacterKilled_ConditionType`
   on officer entries (vanilla pattern) to switch to the `alarm` phase and
   deactivate `0combat`; that is exactly what `sts_wat_kab_07_combat` does.

Nothing in that list is a Neon invention; it is the vanilla gig graph reduced to
its minimum. Reproducing it per site is a **build-tool job**, not hand-authoring:
one tiny `.questphase` per materialization slot, generated from `world.db`.

### 2.4 NodeRef handling from the native core

`NodeRef` is a 64-bit FNV-1a hash of the node path
(`refs/RED4ext.SDK/include/RED4ext/NodeRef.hpp`: `'#'` is stripped, `;` starts a
skip-to-`/` segment, `"$"` and `"~"` are the global/relative roots). Sectors
store that hash in `nodeData[].globalNodeId.hash`, so **the extracted numbers are
directly constructible**:

```cpp
RED4ext::NodeRef ref{hash_from_db};                                  // native
// or resolve an authored name:
RED4ext::NodeRef ref{"#kab_07_ws_bottom_guard_001"};
```

Script-side, a `NodeRef` cannot be built from a `uint64`, which is why the native
plugin must do this step and pass the resulting `GlobalNodeRef`/`EntityID` to
redscript. Verified script entry points:

| Function | Signature | File:line |
| --- | --- | --- |
| `ResolveNodeRef` | `(NodeRef, GlobalNodeRef) -> GlobalNodeRef` | `orphans.swift:34317` |
| `ResolveNodeRefWithEntityID` | `(NodeRef, EntityID) -> GlobalNodeRef` | `orphans.swift:28299` |
| `GlobalNodeRef.IsDefined` | `(GlobalNodeRef) -> Bool` | `orphans.swift:28303` |
| `GlobalNodeID.GetRoot` | `() -> GlobalNodeID` | `orphans.swift:33009` |
| `Cast<EntityID>` | from `GlobalNodeID`/`GlobalNodeRef` | `orphans.swift:33000` |
| `GameInstance.FindEntityByID` | `(GameInstance, EntityID) -> Entity` | used at `core/ai/actions/aiActionHelper.swift:350` |
| `Entity.QueueEventForNodeID` | `(GlobalNodeRef, ref<Event>) -> Bool` | `core/entity/entity.swift:10` |

### 2.5 Runtime read APIs that make the simulation cheap

| Need | API | Evidence |
| --- | --- | --- |
| Enumerate a spawner's live puppets (optionally filtered by entry names) | `GetFixedEntityIdsFromSpawnerEntityID(spawnerID, entryNames, game, out ids)` | `orphans.swift:34038`; used at `cyberpunk/network/squadNode.swift:181` |
| Subscribe to spawn/despawn/death per spawner+entry | `EntitySpawnerEventsBroadcaster.RegisterSpawnerEventPSListener(spawnerOrCommunityId, communityEntryName, psListenerPersistentId, psListenerClassName) -> Uint32` | `orphans.swift:34042`; types `Spawn=0, Despawn=1, Death=2` `orphans.swift:3537` |
| Get the device PS of a door/turret/terminal | `(device as Device).GetDevicePS()` → `ScriptableDeviceComponentPS` | `cyberpunk/devices/core/deviceComponentBase.swift:2` |
| Execute a device action | `PersistencySystem.QueuePSEvent(ps.GetID(), ps.GetClassName(), action)` | used at `core/components/lootContainers.swift:848` |
| Force a door/turret state | `new QuestForcePower()`, `QuestForceOpen()`, `QuestForceON()`, `QuestForceOFF()` | `cyberpunk/devices/core/baseDeviceActions.swift:2001-2040`; consumers `scriptableDeviceBasePS.swift:4521`, `doorController.swift:1076` |
| Order a puppet | `AIComponent.SendCommand(ref<AICommand>)` / static `AIComponent.SendCommand(puppet, cmd)` | `core/components/aiComponent.swift:11,74` |
| Patrol along a vanilla spline | `AIPatrolCommand{ pathParams: AIPatrolPathParameters{ path: NodeRef, isBackAndForth, isInfinite, movementType, patrolWithWeapon } }` | `orphans.swift:48458`, `orphans.swift:58286` |
| Sit/stand in a vanilla workspot | `AIUseWorkspotCommand{ workspotNode: NodeRef, jumpToEntry, entryId, moveToWorkspot }` | `orphans.swift:48681` |
| Walk to an extracted coordinate | `AIMoveToCommand{ movementTarget: AIPositionSpec }` + `AIPositionSpec.SetWorldPosition` | `orphans.swift:45302`, `orphans.swift:34758` |
| Change loyalty without respawning | `AttitudeAgent.SetAttitudeGroup/SetAttitudeTowards/SetAttitudeGroupUnsavable` | `orphans.swift:20443-20458` |
| Play a device animation with an NPC | `WorkspotGameSystem.PlayInDevice(device, actor, …)` | `orphans.swift:19161` |

### 2.6 The phase-lifetime problem and its solution

`QuestsSystem` cannot start a phase (`orphans.swift:18132-18151`), so a
"materialize this site now" design must not assume runtime phase starts. Three
workable shapes, in order of preference:

**S1 — Journal-driven activation (preferred if the spike confirms it).**
Ship one journal quest entry per site whose `questPhase` points at the site's
generated phase. When the native core decides a site becomes *manned*, redscript
sets the journal entry Active via `JournalManager`; the phase starts, registers
its prefab, activates the community. On *dormant*, set the entry Inactive and the
phase unloads the prefab. This gives a true runtime on/off switch with bounded
cost. **Spike required:** confirm a mod-authored journal quest entry can start a
mod-authored `.questphase`.

**S2 — Always-running district phase with fact-gated nodes (no journal API).**
One long-lived phase per district (8 phases) that registers the district's site
prefabs in `phasePrefabs` and gates every spawn-manager node behind
`questFactsDBCondition` on `na_site_<code>_on`. Cost: all district prefabs are
resident while the district phase runs. Acceptable if we scope it to the sites
we actually garrison (say 6–12 per district), and it needs no journal write.
This is the **safe default** if S1 fails.

**S3 — No prefab at all.** Garrisons are spawned via Tier C
(`RequestUnitSpawn`) and moved with `AIMoveToCommand` / position-based loops;
workspots are skipped. Loses the hand-authored animations, but works anywhere,
including faction-swapped crews and player-built outposts.

Recommendation: build **S2 first** (lowest risk, no new API), and keep the phase
generator parameterised so switching to S1 is a build-flag change, not a rewrite.

### 2.7 The one in-game spike that closes the loop

Ship a throwaway `.questphase` (`na_probe.questphase`) with:

1. `phasePrefabs = [ "#sts_wat_kab_07_streetstory" ]`
2. one `questSpawnManagerNodeDefinition` activating `#kab_07_com_enemies` with
   `communityEntryPhaseName = "0combat"`
3. one `questDeviceManager_NodeType` powering `#kab_07_entrance_door_002`
   (whichever door resolves in that prefab)

Then from the native plugin log:

- `ResolveNodeRef("#kab_07_ws_bottom_guard_001")` → defined? (layer C present)
- `GetFixedEntityIdsFromSpawnerEntityID(<kab_07_com_enemies>, [], gi, ids)` →
  non-empty? (activation worked)
- `ResolveNodeRef("#kab_07_entrance_door_002")` → defined and PS class =
  `DoorControllerPS`?

Pass condition: all three true, and 15 hostiles stand on the casino workspots.
If only the first fails, S2's `phasePrefabs` approach is wrong and we fall back
to S3. This is one deploy + one load, and it decides the whole pillar's runtime
shape.

---

## 3. Inventory and extraction feasibility

### 3.1 Site counts (measured from the archive indexes)

Index sources: `archive -l` on `basegame_4_gamedata` (57,033 entries),
`basegame_3_nightcity` (103,917), `ep1_2_gamedata` (30,891),
`ep1_1_nightcity` (43,411). Site codes are matched as
`ma_<d>_<sub>_<nnn>` / `sts_(ep1_)?<d>_<sub>_<nnn>` / `mws_<name>`.

| Family | Unique sites | Own `.questphase` | Own `.community` | Notes |
| --- | --- | --- | --- | --- |
| `ma_*` scanner hustles | **329** | 310 | 198 | no Dogtown `ma_*` exists |
| `sts_*` fixer gigs | **~110** | 87 | 95 | 100 base-game codes + 10 `sts_ep1_*` (Dogtown); a few extra tokens are journal-only variants |
| `mws_*` mini world stories | **56** | — | 35 | district dirs `mws_<d>_<nn>` + named ones |
| **Total content sites** | **~495** | — | — | physical prefabs overlap (e.g. `mq304` shares `sts_ep1_06`) |

`ma_*` by sub-district token (canonical site codes only):

| Token | Sites | Token | Sites | Token | Sites |
| --- | --- | --- | --- | --- | --- |
| `wat_nid` | 34 | `std_rcr` | 27 | `pac_cvi` | 21 |
| `wbr_jpn` | 31 | `cct_dtn` | 25 | `hey_spr` | 21 |
| `wat_kab` | 25 | `wat_lch` | 23 | `hey_gle` | 24 |
| `cct_cpz` | 14 | `hey_rey` | 15 | `pac_wwd` | 12 |
| `wbr_hil` | 14 | `bls_ina` | 8 | `wbr_nok` | 5 |
| `bls_se5` | 2 | `off_work` | 4 | `wat_ich` | 1 |

Top-level district roll-up (our `districts.code`): Watson 83, Heywood 60,
Santo Domingo 50, Westbrook 50, City Center 39, Pacifica 33, Badlands 10,
`off_work` 4, **Dogtown 0**.

`sts_*` roll-up: Watson 34, Santo Domingo 16, Heywood 14, **Dogtown (`ep1`) 13**,
Badlands 12, Westbrook 11, City Center 7, Pacifica 2 (+ a few journal-only
tokens).

**Density:** the repo currently seeds **96 sub-territories** across **9
districts** (`data/sub_territories.json`, incl. `morro_rock` / Orbital Air NCX).
That gives **~3.4 `ma_*` sites**, **~1.2 gigs**, and **~0.6 `mws_*`** per
sub-territory — **~5.2 physical sites per sub-territory**, i.e. every
sub-territory can have a control center plus 3–6 satellite sites without
inventing geometry.

### 3.2 What `tools/extract-world.py` already gives us

Already emitted and directly reusable:

| Output | Fields that matter for sites |
| --- | --- |
| `dist/extract/areas.jsonl` | `community_hash`, `debug_name` (`{kab_07_com_enemies}`), `entry_count`, `dominant_faction`, `faction_counts`, `x/y/z`, `district_code`, `source_file` |
| `dist/extract/registry` (in memory today) | `communityId.hash`, `template.entries[].characterRecordId/entryName/phases[].timePeriods[].spotNodeRefs/markings/hour/quantity` |
| `dist/extract/pois.jsonl` | `journal_path_hash`, `x/y/z` |
| `data/spawn_points.json` | 1,329 faction-resolved community anchors |

Measured coverage of the site-community join in the current extract:

- **328** area rows whose `debug_name` starts with `ma_`/`sts_`/`mws_`
  (206 `ma_`, 82 `sts_`, 35 `mws_` distinct names);
- **216 further rows** with the generic `<sub>_<nn>_…` prefix
  (`kab_07_…`, `arr_06_…`, 71 distinct prefixes).

So **~540 site communities are already anchored and faction-resolved today**,
with no new archive reads. That is enough to ship `world_sites` v0.

### 3.3 What must be added

| Gap | Fix | Cost |
| --- | --- | --- |
| `entriesInitialState` (the liveness bit) is not read | Parse `worldCommunityRegistryItem.entriesInitialState[]` in `parse_always_loaded` | trivial, same file |
| `spotNodeRefs` / phase names are not persisted | Emit them from the registry `template` | trivial |
| Quest-sector discovery | Read `blocks/all.streamingblock` (+ `ep1/blocks/all.streamingblock`), index descriptors by `questPrefabNodeRef` and `streamingBox` | ~2 × 37 MB JSON, one pass |
| Per-site node census | Extract + convert each site's `Quest` sector, collect `worldAISpotNode`/`worldPatrolSplineNode`/`worldGuardAreaNode`/`worldDeviceNode`/`worldInteriorAreaNode`/`worldInteriorMapNode` | ~470 sectors × ~1 s ≈ 8–10 min; peak disk ~1 GB with batching |
| Site → district / sub-territory | Spatial join on anchor (existing `classify_district_xy` + nearest control center) | already exists |
| Site display names | `journalPathHash` join is still unresolved (known risk 10); ship `code` + `debug_name`, add `journal_path_hash` for later | optional |
| Device class | Map `entityTemplate` path family + `deviceConnections[].deviceClassName` | trivial |

**Do not extract `.community` files.** The registry inlines the same templates;
the only thing `.community` paths add is the site token, which `debug_name` and
`questPrefabNodeRef` already give. Skipping them saves 5,462 conversions.

### 3.4 Determinism and invariants for the data stage

- Sort all rows by `(site_code, node_ref)`; round coordinates to 3 decimals.
- Assert `sum(len(entriesInitialState))` over site communities reconciles with
  the registry (43,971 ep1).
- Assert every `site_communities.spawner_ref` resolves to either a sector
  `nodeRefs` entry or a `debug_name` in `always_loaded_*`; otherwise mark the
  row `confidence = 'unresolved'` instead of failing the build.
- Assert `ma_*` count ≥ 300, `sts_*` ≥ 100, `mws_*` ≥ 50 (base-only extraction
  would fail these).
- Never emit `dist/` paths into `data/`.

---

## 4. Data model: `data/schema/world_v2.sql`

### 4.1 Design decisions

1. **Site ≠ content.** One physical prefab can host several quests
   (`sts_ep1_06` hosts `mq304`). `world_sites` is the physical place;
   `site_bindings` lists every vanilla content graph that used it. Conquest,
   garrison, and conversion attach to the *site*, not to a gig.
2. **Every NodeRef is stored as text** exactly as authored
   (`#kab_07_com_enemies`, `$/03_night_city/...`), plus `global_node_id` (the
   compiled `uint64`) when a sector instance exists. Text is the authoring key;
   the hash is the runtime key.
3. **No boolean soup.** Per-node facts live on the child row; site-level
   `has_*` columns are derived aggregates kept for cheap filtering, and the
   build asserts they match the child counts.
4. **Suitability is a normalized vocabulary**, not a bitmask, so queries read
   like intent (`WHERE suitability = 'chop_shop'`) and illegal values fail the
   `CHECK`.
5. **Hashes are text.** `community_hash` stays `TEXT` like
   `spawn_points.community_hash`; SQLite has no `u64`.
6. **Extraction confidence is explicit** (`exact` / `derived` / `heuristic`) so
   the runtime can refuse to build a mission on a guessed anchor.

### 4.2 DDL (additive migration; keep `world_v1.sql` unchanged)

```sql
-- Neon Ascendancy static world database, v2: living-site model.
-- Apply AFTER world_v1.sql. Bumps PRAGMA user_version to 2.
--
-- Coordinates: CP2077 world-space metres (X/Y/Z, Z up). Yaw radians, CCW from +X.
-- NodeRefs are stored verbatim; global_node_id is the compiled uint64 as TEXT.

PRAGMA user_version = 2;

-- ---------------------------------------------------------------------------
-- 1. Physical sites
-- ---------------------------------------------------------------------------

CREATE TABLE world_sites (
  site_id              INTEGER PRIMARY KEY,
  code                 TEXT    NOT NULL UNIQUE,      -- 'sts_wat_kab_07'
  display_name         TEXT,                          -- nullable until journal join lands
  site_kind            TEXT    NOT NULL CHECK (site_kind IN (
                         'scanner_hustle','fixer_gig','mini_world_story',
                         'side_quest','combat_event','dynamic_event',
                         'corp_facility','gang_compound','interior_hideout',
                         'service','manual')),
  source_family        TEXT    NOT NULL CHECK (source_family IN (
                         'ma','sts','sts_ep1','mws','mq','sq','ce','de','manual')),
  district_id          INTEGER NOT NULL REFERENCES districts(district_id),
  sub_territory_id     INTEGER REFERENCES sub_territories(sub_territory_id),
  control_center_id    INTEGER REFERENCES control_centers(control_center_id),

  anchor_x             REAL    NOT NULL,
  anchor_y             REAL    NOT NULL,
  anchor_z             REAL    NOT NULL,
  bbox_min_x           REAL, bbox_min_y REAL, bbox_min_z REAL,
  bbox_max_x           REAL, bbox_max_y REAL, bbox_max_z REAL,
  radius_m             REAL    NOT NULL DEFAULT 40.0 CHECK (radius_m > 0.0),

  is_interior          INTEGER NOT NULL DEFAULT 0 CHECK (is_interior IN (0,1)),
  interior_map_coords  TEXT,                          -- worldInteriorMapNode.coords
  floor_count          INTEGER CHECK (floor_count IS NULL OR floor_count >= 1),

  default_faction_id       INTEGER REFERENCES factions(faction_id),
  initial_owner_faction_id INTEGER REFERENCES factions(faction_id),
  faction_source       TEXT    NOT NULL DEFAULT 'none'
                         CHECK (faction_source IN ('tweak','spatial','manual','none')),

  tier                 INTEGER NOT NULL DEFAULT 1 CHECK (tier BETWEEN 1 AND 5),
  difficulty           INTEGER NOT NULL DEFAULT 1 CHECK (difficulty BETWEEN 1 AND 5),
  loot_tier            INTEGER NOT NULL DEFAULT 1 CHECK (loot_tier BETWEEN 1 AND 5),

  -- Denormalised rollups, asserted against child tables at build time.
  has_patrols          INTEGER NOT NULL DEFAULT 0 CHECK (has_patrols IN (0,1)),
  has_workspots        INTEGER NOT NULL DEFAULT 0 CHECK (has_workspots IN (0,1)),
  has_guard_areas      INTEGER NOT NULL DEFAULT 0 CHECK (has_guard_areas IN (0,1)),
  has_security_devices INTEGER NOT NULL DEFAULT 0 CHECK (has_security_devices IN (0,1)),
  has_doors            INTEGER NOT NULL DEFAULT 0 CHECK (has_doors IN (0,1)),
  has_community        INTEGER NOT NULL DEFAULT 0 CHECK (has_community IN (0,1)),
  spot_count           INTEGER NOT NULL DEFAULT 0 CHECK (spot_count   >= 0),
  patrol_count         INTEGER NOT NULL DEFAULT 0 CHECK (patrol_count >= 0),
  device_count         INTEGER NOT NULL DEFAULT 0 CHECK (device_count >= 0),
  community_count      INTEGER NOT NULL DEFAULT 0 CHECK (community_count >= 0),

  -- Runtime materialisation handle (native plugin).
  quest_prefab_ref     TEXT,                          -- '#sts_wat_kab_07_streetstory'
  quest_sector_path    TEXT,                          -- 'base\worlds\...\quest_<hash>.streamingsector'
  sector_category      TEXT CHECK (sector_category IN ('Quest','Interior','Exterior')),
  streaming_block      TEXT,                          -- 'base\worlds\...\blocks\all.streamingblock'

  -- Provenance / trust.
  extraction_confidence TEXT NOT NULL DEFAULT 'exact'
                         CHECK (extraction_confidence IN ('exact','derived','heuristic','unresolved')),
  source_archive       TEXT NOT NULL,
  source_path          TEXT NOT NULL,
  UNIQUE (source_path)
) STRICT;

CREATE INDEX idx_world_sites_kind      ON world_sites(site_kind);
CREATE INDEX idx_world_sites_territory ON world_sites(sub_territory_id);
CREATE INDEX idx_world_sites_district  ON world_sites(district_id);
CREATE INDEX idx_world_sites_faction   ON world_sites(default_faction_id);

CREATE VIRTUAL TABLE site_rtree USING rtree(id, min_x, max_x, min_y, max_y);

-- Which vanilla content used this physical site (one site, many bindings).
CREATE TABLE site_bindings (
  site_id            INTEGER NOT NULL REFERENCES world_sites(site_id) ON DELETE CASCADE,
  content_kind       TEXT    NOT NULL CHECK (content_kind IN
                        ('ma','sts','sts_ep1','mws','mq','sq','ce','de')),
  content_code       TEXT    NOT NULL,                -- 'sts_wat_kab_07' / 'mq304'
  quest_phase_path   TEXT,                            -- '...\sts_wat_kab_07_combat.questphase'
  quest_resource_path TEXT,                           -- '...\sts_wat_kab_07_quest.quest'
  is_primary         INTEGER NOT NULL DEFAULT 0 CHECK (is_primary IN (0,1)),
  PRIMARY KEY (site_id, content_kind, content_code)
) STRICT, WITHOUT ROWID;

CREATE INDEX idx_site_bindings_code ON site_bindings(content_code);

-- Intent vocabulary: what this place can become / be used for.
CREATE TABLE site_suitabilities (
  site_id     INTEGER NOT NULL REFERENCES world_sites(site_id) ON DELETE CASCADE,
  suitability TEXT    NOT NULL CHECK (suitability IN (
                'raid_target','stealth_entry','sniper_nest','vehicle_bay',
                'rooftop_access','sewer_access','elevator','hostage_site',
                'officer_site','arms_cache','data_vault','terminal_cluster',
                'turret_cluster','camera_net','safehouse','chop_shop',
                'netrunner_den','clinic','club','warehouse','branch_office',
                'market_stall','lab')),
  score       INTEGER NOT NULL DEFAULT 50 CHECK (score BETWEEN 0 AND 100),
  PRIMARY KEY (site_id, suitability)
) STRICT, WITHOUT ROWID;

-- ---------------------------------------------------------------------------
-- 2. Communities and their roster
-- ---------------------------------------------------------------------------

CREATE TABLE site_communities (
  site_community_id   INTEGER PRIMARY KEY,
  site_id             INTEGER NOT NULL REFERENCES world_sites(site_id) ON DELETE CASCADE,
  community_hash      TEXT    NOT NULL,               -- registry communityId
  spawner_ref         TEXT    NOT NULL,               -- '#kab_07_com_enemies'
  spawner_global_id   TEXT,
  area_node_type      TEXT CHECK (area_node_type IN ('Regular','Streamable','Background')),
  community_path      TEXT,                           -- '...\sts_wat_kab_07_com_enemies.community'
  is_primary          INTEGER NOT NULL DEFAULT 0 CHECK (is_primary IN (0,1)),
  entry_count         INTEGER NOT NULL DEFAULT 0 CHECK (entry_count >= 0),
  active_on_start     INTEGER NOT NULL DEFAULT 0 CHECK (active_on_start BETWEEN 0 AND entry_count),
  x REAL NOT NULL, y REAL NOT NULL, z REAL NOT NULL,
  UNIQUE (site_id, community_hash)
) STRICT;

CREATE INDEX idx_site_communities_hash    ON site_communities(community_hash);
CREATE INDEX idx_site_communities_spawner ON site_communities(spawner_ref);

CREATE TABLE site_community_entries (
  entry_id            INTEGER PRIMARY KEY,
  site_community_id   INTEGER NOT NULL REFERENCES site_communities(site_community_id) ON DELETE CASCADE,
  entry_name          TEXT    NOT NULL,               -- 'Enemy11', 'Jotaro'
  character_record_id TEXT,                           -- 'Character.kab_07_enemy_1st_floor_handgun'
  faction_id          INTEGER REFERENCES factions(faction_id),
  role_hint           TEXT CHECK (role_hint IN (
                        'grunt','officer','boss','sniper','melee','ranged',
                        'netrunner','medic','driver','civilian','unknown')),
  initial_phase_name  TEXT,
  entry_active_on_start INTEGER NOT NULL DEFAULT 0 CHECK (entry_active_on_start IN (0,1)),
  spawn_in_view       INTEGER NOT NULL DEFAULT 1 CHECK (spawn_in_view IN (0,1)),
  UNIQUE (site_community_id, entry_name)
) STRICT;

CREATE INDEX idx_site_entries_faction ON site_community_entries(faction_id);

CREATE TABLE site_community_phases (
  phase_id        INTEGER PRIMARY KEY,
  entry_id        INTEGER NOT NULL REFERENCES site_community_entries(entry_id) ON DELETE CASCADE,
  phase_name      TEXT    NOT NULL,                   -- '0combat','alarm','default'
  always_spawned TEXT    NOT NULL DEFAULT 'default__false_'
                    CHECK (always_spawned IN ('default__false_','true_','false_')),
  hour            TEXT CHECK (hour IN ('Day','Night','Morning','Evening','Any')),
  quantity        INTEGER NOT NULL DEFAULT 1 CHECK (quantity >= 0),
  is_sequence     INTEGER NOT NULL DEFAULT 0 CHECK (is_sequence IN (0,1)),
  UNIQUE (entry_id, phase_name, hour, quantity)
) STRICT;

CREATE INDEX idx_site_phases_name ON site_community_phases(phase_name);

-- One row per (phase, workspot). This is the join that makes AIUseWorkspot
-- possible straight from the DB.
CREATE TABLE site_community_slots (
  phase_id     INTEGER NOT NULL REFERENCES site_community_phases(phase_id) ON DELETE CASCADE,
  slot_index   INTEGER NOT NULL,
  spot_ref     TEXT    NOT NULL,                      -- '#kab_07_ws_1stfloor_tyger_002'
  spot_id      INTEGER REFERENCES site_spots(spot_id),
  markings     TEXT,                                  -- JSON array of CName strings
  PRIMARY KEY (phase_id, slot_index)
) STRICT, WITHOUT ROWID;

-- ---------------------------------------------------------------------------
-- 3. Workspots, patrols, guard areas
-- ---------------------------------------------------------------------------

CREATE TABLE site_spots (
  spot_id         INTEGER PRIMARY KEY,
  site_id         INTEGER NOT NULL REFERENCES world_sites(site_id) ON DELETE CASCADE,
  node_ref        TEXT    NOT NULL,
  global_node_id  TEXT,
  debug_name      TEXT,
  workspot_resource TEXT,                             -- 'base\workspots\...\guard__01.workspot'
  spot_role       TEXT CHECK (spot_role IN
                    ('guard','patrol','idle','sit','sleep','work','eat','drink',
                     'dance','drug','inspect','search','cover','sniper','driver',
                     'crowd','unknown')),
  markings        TEXT,                               -- JSON array
  is_workspot_infinite INTEGER NOT NULL DEFAULT 0 CHECK (is_workspot_infinite IN (0,1)),
  is_workspot_static   INTEGER NOT NULL DEFAULT 0 CHECK (is_workspot_static IN (0,1)),
  actor_bodytype  TEXT,
  floor_index     INTEGER,
  x REAL NOT NULL, y REAL NOT NULL, z REAL NOT NULL, yaw REAL,
  source_sector   TEXT NOT NULL,
  UNIQUE (site_id, node_ref)
) STRICT;

CREATE INDEX idx_site_spots_role ON site_spots(spot_role);
CREATE INDEX idx_site_spots_gnid ON site_spots(global_node_id);
CREATE VIRTUAL TABLE site_spot_rtree USING rtree(id, min_x, max_x, min_y, max_y);

CREATE TABLE site_patrols (
  patrol_id       INTEGER PRIMARY KEY,
  site_id         INTEGER NOT NULL REFERENCES world_sites(site_id) ON DELETE CASCADE,
  node_ref        TEXT    NOT NULL,
  global_node_id  TEXT,
  debug_name      TEXT,
  point_count     INTEGER NOT NULL DEFAULT 0 CHECK (point_count >= 0),
  floor_index     INTEGER,
  x REAL NOT NULL, y REAL NOT NULL, z REAL NOT NULL,
  source_sector   TEXT NOT NULL,
  UNIQUE (site_id, node_ref)
) STRICT;

CREATE TABLE site_patrol_points (
  patrol_id   INTEGER NOT NULL REFERENCES site_patrols(patrol_id) ON DELETE CASCADE,
  point_index INTEGER NOT NULL,
  spot_ref    TEXT    NOT NULL,                       -- NodeRef of the workspot point
  spot_id     INTEGER REFERENCES site_spots(spot_id),
  point_type  TEXT    NOT NULL DEFAULT 'Workspot'
                CHECK (point_type IN ('Workspot','Point','Entity')),
  x REAL, y REAL, z REAL,
  PRIMARY KEY (patrol_id, point_index)
) STRICT, WITHOUT ROWID;

CREATE TABLE site_guard_areas (
  guard_area_id INTEGER PRIMARY KEY,
  site_id       INTEGER NOT NULL REFERENCES world_sites(site_id) ON DELETE CASCADE,
  node_ref      TEXT    NOT NULL,
  global_node_id TEXT,
  debug_name    TEXT,
  pursuit_range_m REAL,
  floor_index   INTEGER,
  x REAL NOT NULL, y REAL NOT NULL, z REAL NOT NULL,
  source_sector TEXT NOT NULL,
  UNIQUE (site_id, node_ref)
) STRICT;

CREATE TABLE site_guard_area_communities (
  guard_area_id INTEGER NOT NULL REFERENCES site_guard_areas(guard_area_id) ON DELETE CASCADE,
  community_ref TEXT    NOT NULL,                     -- '#kab_07_com_enemies'
  is_primary    INTEGER NOT NULL DEFAULT 1 CHECK (is_primary IN (0,1)),
  entry_names   TEXT,                                 -- JSON array of CName
  PRIMARY KEY (guard_area_id, community_ref)
) STRICT, WITHOUT ROWID;

-- ---------------------------------------------------------------------------
-- 4. Devices, doors, triggers, prefab variants
-- ---------------------------------------------------------------------------

CREATE TABLE site_devices (
  device_id      INTEGER PRIMARY KEY,
  site_id        INTEGER NOT NULL REFERENCES world_sites(site_id) ON DELETE CASCADE,
  node_ref       TEXT    NOT NULL,
  global_node_id TEXT,
  debug_name     TEXT,
  device_kind    TEXT    NOT NULL CHECK (device_kind IN (
                   'security_area','security_system','camera','turret',
                   'terminal','computer','door','gate','lift','vending',
                   'speaker','tv','other')),
  controller_class TEXT,                              -- 'SecurityAreaControllerPS', 'DoorControllerPS'
  entity_template  TEXT,
  connected_community_ref TEXT,                       -- from deviceConnections[CommunityProxyPS]
  is_quest_gated   INTEGER NOT NULL DEFAULT 0 CHECK (is_quest_gated IN (0,1)),
  floor_index      INTEGER,
  x REAL NOT NULL, y REAL NOT NULL, z REAL NOT NULL,
  source_sector    TEXT NOT NULL,
  UNIQUE (site_id, node_ref)
) STRICT;

CREATE INDEX idx_site_devices_kind ON site_devices(device_kind);

CREATE TABLE site_doors (
  door_id      INTEGER PRIMARY KEY,
  site_id      INTEGER NOT NULL REFERENCES world_sites(site_id) ON DELETE CASCADE,
  device_id    INTEGER REFERENCES site_devices(device_id) ON DELETE SET NULL,
  node_ref     TEXT    NOT NULL,
  global_node_id TEXT,
  debug_name   TEXT,
  door_role    TEXT    NOT NULL CHECK (door_role IN
                 ('entrance','exit','interior','elevator','garage','roof','service')),
  controller_class TEXT NOT NULL DEFAULT 'DoorControllerPS',
  default_state TEXT CHECK (default_state IN ('OPENED','CLOSED','LOCKED','SEALED')),
  requires_power INTEGER NOT NULL DEFAULT 1 CHECK (requires_power IN (0,1)),
  unlock_action  TEXT NOT NULL DEFAULT 'ForcePower'
                   CHECK (unlock_action IN ('ForcePower','ForceOpen','ForceUnlock','None')),
  vanilla_lock_action TEXT,                           -- observed questDeviceManager action
  UNIQUE (site_id, node_ref)
) STRICT;

CREATE TABLE site_triggers (
  trigger_id   INTEGER PRIMARY KEY,
  site_id      INTEGER NOT NULL REFERENCES world_sites(site_id) ON DELETE CASCADE,
  node_ref     TEXT    NOT NULL,
  debug_name   TEXT,
  trigger_role TEXT CHECK (trigger_role IN
                  ('entry','mission_volume','ambush','extraction','elevator',
                   'elevator_close','despawn','patrol_gate','unknown')),
  volume_json  TEXT,
  x REAL NOT NULL, y REAL NOT NULL, z REAL NOT NULL,
  UNIQUE (site_id, node_ref)
) STRICT;

-- Prefab variants observed in the streaming block (lockdown, loot, interior…).
CREATE TABLE site_variants (
  site_variant_id INTEGER PRIMARY KEY,
  site_id          INTEGER NOT NULL REFERENCES world_sites(site_id) ON DELETE CASCADE,
  sector_path      TEXT NOT NULL,
  variant_name     TEXT NOT NULL,                     -- 'Interior','lockdown','final_loot'
  variant_id       TEXT,
  enabled_by_default INTEGER NOT NULL DEFAULT 0 CHECK (enabled_by_default IN (0,1)),
  node_ref         TEXT,
  UNIQUE (site_id, sector_path, variant_name, variant_id)
) STRICT;

-- Supply / reinforcement / sightline graph between sites.
CREATE TABLE site_links (
  from_site_id INTEGER NOT NULL REFERENCES world_sites(site_id) ON DELETE CASCADE,
  to_site_id   INTEGER NOT NULL REFERENCES world_sites(site_id) ON DELETE CASCADE,
  link_kind    TEXT NOT NULL CHECK (link_kind IN
                 ('reinforcement','supply','escape_route','sightline','patrol_route')),
  weight       INTEGER NOT NULL DEFAULT 100 CHECK (weight BETWEEN 0 AND 1000),
  distance_m   REAL CHECK (distance_m IS NULL OR distance_m >= 0.0),
  PRIMARY KEY (from_site_id, to_site_id, link_kind),
  CHECK (from_site_id <> to_site_id)
) STRICT, WITHOUT ROWID;

-- ---------------------------------------------------------------------------
-- 5. Convenience views (read-only; no hidden writes)
-- ---------------------------------------------------------------------------

CREATE VIEW v_site_garrison AS
SELECT s.site_id, s.code, s.site_kind, s.sub_territory_id, s.default_faction_id,
       COUNT(DISTINCT c.site_community_id) AS communities,
       COUNT(DISTINCT e.entry_id)          AS roster,
       COUNT(DISTINCT e.entry_id) FILTER (WHERE e.role_hint IN ('officer','boss')) AS officers,
       COUNT(DISTINCT p.patrol_id)         AS patrols,
       COUNT(DISTINCT sp.spot_id)          AS spots,
       COUNT(DISTINCT d.device_id)         AS devices
FROM world_sites s
LEFT JOIN site_communities c        ON c.site_id = s.site_id
LEFT JOIN site_community_entries e  ON e.site_community_id = c.site_community_id
LEFT JOIN site_patrols p            ON p.site_id = s.site_id
LEFT JOIN site_spots sp             ON sp.site_id = s.site_id
LEFT JOIN site_devices d            ON d.site_id = s.site_id
GROUP BY s.site_id;

CREATE VIEW v_site_conversion_candidates AS
SELECT s.site_id, s.code, s.is_interior, su.suitability, su.score,
       s.tier, s.difficulty, s.default_faction_id
FROM world_sites s
JOIN site_suitabilities su ON su.site_id = s.site_id
WHERE su.suitability IN ('safehouse','chop_shop','netrunner_den','clinic',
                         'club','warehouse','branch_office')
ORDER BY su.score DESC, s.site_id;
```

### 4.3 Seed files

| Seed | Contents | Approx rows |
| --- | --- | --- |
| `data/sites/sites.json` | one row per physical site | ~470 |
| `data/sites/bindings.json` | site ↔ `ma`/`sts`/`mws`/`mq`/`sq` | ~520 |
| `data/sites/communities.json` | spawner refs + hashes + anchors | ~540 |
| `data/sites/rosters.json` | entries (name, record, faction, initial state) | ~4–6 k |
| `data/sites/phases.json` | phase rows + slot refs | ~3–5 k |
| `data/sites/spots.json` | workspots (NodeRef, role, workspot, xyz) | ~8–12 k |
| `data/sites/patrols.json` | splines + points | ~400 / ~1.2 k |
| `data/sites/guards.json` | guard areas + linked communities | ~300 |
| `data/sites/devices.json` | devices + doors | ~1–2 k |
| `data/sites/variants.json` | prefab variants | ~1 k |
| `data/sites/links.json` | derived adjacency | ~1 k |

Total committed JSON ≈ 5–8 MB. `world.db` grows by roughly 6–10 MB. That is
acceptable for a read-only, `immutable=1` database; keep it out of the native
hot path except for boot-time index building.

### 4.4 Compatibility with v1

- No v1 column changes, no v1 table drops. `build-world-db.py` runs
  `world_v1.sql` then `world_v2.sql`, then inserts. `meta.schema_version = 2`.
- `spawn_points` stays as the faction-density table; `world_sites` is the
  *place* table. A site may reference the same `community_hash` that already
  appears in `spawn_points` — that is a deliberate, documented duplication of
  identity, not of meaning.
- `landmarks` and `control_centers` are unchanged; sites link to them, never
  replace them. `world_sites.control_center_id` is the capture anchor.

---

## 5. Living-territory gameplay architecture

### 5.1 Territory Control: garrisons, not flags

**Model.** A sub-territory's effective strength is no longer a single number:

```
claim_effective = claim_strength
                * (0.5 + 0.5 * manned_site_ratio)
                * (1 + 0.15 * sum(site.fortification))
                * control_center_factor        // 1.0 held, 0.6 contested, 0.3 lost
```

- `manned_site_ratio = manned_sites / total_sites` in the sub-territory.
- A site is **manned** when (a) the player is within `MATERIALIZE_RADIUS`
  (suggest 250 m) or (b) the simulation marks it garrisoned and the player is in
  the district. Only manned sites cost runtime.
- `fortification` is a player-buildable upgrade (0–3), stored in the dynamic DB.

**Site state machine** (dynamic DB, not `world.db`):

```
dormant ──garrison──▶ manned ──alert──▶ alerted ──combat──▶ contested
   ▲                    │                                        │
   │                    └──────────cleared──────▶ cleared ◀──────┘
   │                                                │
   └──────── abandoned ◀── convert ◀── occupied ◀───┘
```

- `dormant → manned`: activate the spawn-manager phase (S2 fact flip), power
  entry doors, arm security.
- `manned → alerted`: kill an officer or trip a camera; switch community phase
  `0combat → alarm`, enable `_hard_mode` / `_backup` communities.
- `contested → cleared`: all roster entries dead (`Death` events from the
  spawner broadcaster, or `GetFixedEntityIdsFromSpawnerEntityID` = empty).
- `cleared → occupied`: player claims. Attitude re-skin
  (`AttitudeAgent.SetAttitudeGroupUnsavable`) makes the surviving crew loyal, or
  the site becomes a Neon garrison spawn (Tier B/C).
- `occupied → converted`: Organization pillar purchase.

**Satellite outposts.** Because a sub-territory has ~5 sites, control becomes
spatial: hold the control center *and* the majority of satellite sites to flip
ownership. Sites project `site_links` reinforcement edges, so an unmanned
neighbour can send a squad if the sim says it is manned (abstracted, then
materialized at the site's `reinforcement` spots when the player is close).

**Player-built outposts.** A cleared site with `safehouse`/`warehouse`
suitability can be converted into a Neon outpost: the sim stores it, and the
runtime adds a Neon garrison (Tier B prefab or Tier C spawns) at the site's
`site_spots` of role `guard`/`patrol`. This is how the map fills with *your*
people without touching vanilla geometry.

### 5.2 Dynamic Missions: archetypes bound to site features

Mission generation becomes a constraint satisfaction over `world.db` instead of
random points:

| Archetype | Site requirements | Uses | Win / fail |
| --- | --- | --- | --- |
| **Assault / Raid** | exterior, `has_patrols`, `raid_target`, tier ≥ 2 | patrol routes, guard areas, reinforcement links | Clear roster, hold 60 s |
| **Data heist** | `is_interior`, `data_vault` or `terminal_cluster`, `stealth_entry` | terminal `site_devices`, interior triggers, cameras | Download at terminal, exfiltrate unseen |
| **Sabotage** | `turret_cluster` / `camera_net` | turret + camera `site_devices` | Disable N devices, leave |
| **Assassination** | `officer_site`, roster contains `officer`/`boss` | entry-level `role_hint`, guard area `names[]` | Kill VIP only |
| **Rescue / hostage** | `hostage_site` (entry name `victim`/`hostage`) | interior doors, lifts | Extract VIP alive |
| **Ambush defense** | player-owned site, `reinforcement` links | `site_links`, spawn waves | Survive N waves |
| **Territory sweep** | all sites in a sub-territory | aggregate | Clear ≥ 80 % of sites |
| **Interdiction** | deferred road chunks | `road_chunks` | Stop convoy |

Each generated mission stores concrete `NodeRef`s (target spot, terminal, door,
extraction trigger) so the runtime never has to search. Mission failure does not
reset the site; it raises local heat and triggers `alerted`.

**Stealth is spatial, not flag-based.** `site_triggers` with
`trigger_role = 'entry'`/`'mission_volume'` plus camera coverage from
`site_devices` give a detection graph. A data heist can be scored on
"cameras disabled / cameras seen", which is real gameplay rather than a dice
roll.

### 5.3 Organization Management: sites as assets

Conversion catalogue (each requires suitability + tier + cash + staff):

| Conversion | Requires | Income | Effects |
| --- | --- | --- | --- |
| **Safehouse** | interior, `safehouse` | 0 | respawn point, stash, +garrison cap |
| **Chop shop** | `vehicle_bay`, `warehouse` | medium | converts stolen vehicles, +heat |
| **Netrunner den** | `data_vault`, `netrunner_den` | medium | enables espionage missions, +intel |
| **Clinic** | `clinic` | low | heals, reduces crew attrition |
| **Club** | `club` | high | income + intel, +heat, crowd |
| **Warehouse** | `warehouse` | medium | supply capacity for raids |
| **Branch office** | `branch_office` (corp sites only) | high | stock influence, legal cover |

Each conversion is a `site_asset` row in the dynamic DB:
`(site_id, asset_kind, level, staff, upkeep, income, heat, opened_at_game_time)`.
Upkeep is charged per cycle; unpaid upkeep drops the asset to `derelict` and the
site reverts to `cleared`, not to the enemy — a deliberate, non-punitive loop.

**Why this matters:** it gives the player a reason to *keep* a site instead of
farming it, and it turns `world.db`'s `suitability` column into the strategic
map: "this Watson interior has a data vault and a service elevator — that's my
next den."

### 5.4 Stock Market: facilities as fundamentals

Two channels, both cheap:

1. **Asset value → price drift.** Each corp-owned site carries
   `facility_value` (derived from `tier`, `site_kind`, device count). A corp's
   fundamental = `Σ facility_value` over sites it owns. Quarterly (sim cycle)
   drift = `k * (fundamental_delta / fundamental)`. Losing three facilities in
   Watson visibly moves the ticker without a special-case event.
2. **Targeted shocks.** Capturing, sabotaging, or data-heisting a corp site
   emits `MarketShock { ticker, magnitude, half_life }`:
   - sabotage turret cluster → small, short shock;
   - data heist at a `data_vault` → medium shock + temporary `INSIDER` edge;
   - capture a `branch_office` → large, long shock;
   - assassination of a corp officer on-site → medium shock + heat.

This keeps the existing `SimEvent` contract: the Market pillar never reads
`world.db` at runtime; it reads the cached `corp_fundamentals` snapshot the
Territory pillar updates on ownership change.

### 5.5 Performance and materialisation budget

Hard rules, consistent with `docs/architecture.md` §1.2:

- **Never query `world.db` per frame.** Site lookups happen on discrete events:
  district/chunk crossing, mission start, ownership flip, `GameTime` cycle.
- **Materialisation budget:** at most `N = 3` sites have an active phase
  (S2/S1) at once, chosen by `distance² / (mission_relevance + 1)`. Everything
  else is abstract garrison state in the dynamic DB.
- **Event-driven roster tracking:** one
  `RegisterSpawnerEventPSListener` per materialized site community; the callback
  updates a small in-memory counter and writes back on death/despawn. No polling.
- **Boot cost:** build the site R-Tree and per-district site lists once; the
  native core keeps a flat array of ~500 `SiteRuntime` structs (< 100 KB).
- **Save safety:** site state lives in the dynamic DB behind the existing
  revision watermark; no new save hook.
- **Phase churn:** prefer S2 (always-running district phase, fact-gated) over
  starting/stopping phases, because phase start is not script-accessible and
  churn is the riskiest part of the whole design.

---

## 6. Risks and mitigations

| # | Risk | Evidence | Mitigation |
| --- | --- | --- | --- |
| 1 | **Quest sector may not stream without its prefab being instantiated** | Every site phase declares `phasePrefabs[0]`; `Quest` descriptors have `rldGridCell: 0` and an infinite `streamingBox` | S2 registers the prefab explicitly; the §2.7 spike verifies `ResolveNodeRef` before any content work |
| 2 | Phase cannot be started from script | `QuestsSystem` = facts + listeners only (`orphans.swift:18132`) | S2 (always-running, fact-gated) as default; S1 (journal) only after a spike |
| 3 | Prefab registration cost (all district prefabs resident) | 2,358 `Quest` sectors city-wide | Register only sites we garrison (6–12/district); keep the rest abstract |
| 4 | Faction swap cannot change baked `characterRecordId`s | `.community` rosters are TweakDBIDs | Tier B (Neon prefab + Neon `.community`) for true swap; Tier C2 attitude re-skin for immediate "they work for you" |
| 5 | `PreventionSpawnSystem` may apply NCPD filters | ticket-not-found path is inert (`preventionSystem.swift:1615`) | Spike; keep Tier C off the critical path so failure degrades to "no dynamic waves" |
| 6 | `worldDeviceNode.deviceClassName` is often `None` | sampled security areas | Classify by `entityTemplate` path family + `deviceConnections[].deviceClassName` |
| 7 | Door default state varies per entity | `DoorControllerPS.SetDefaultDoorState` (`doorController.swift:261`) | Never assume locked/unlocked: read PS, then `ForcePower`/`ForceOpen` as needed |
| 8 | Site ↔ community hash has no name-based join | FNV of `#kab_07_com_enemies` is not the community hash | Join positionally via area node ↔ `sourceObjectId` ↔ `debug_name` (already working: 328 + 216 rows) |
| 9 | Overlapping sites (one prefab, several quests) | `sts_ep1_06` hosts `mq304` | `site_bindings`; one physical site, many content rows |
| 10 | Localised titles unavailable offline | `journalPathHash` unresolved (known risk 10) | `display_name` nullable; ship `code` + `debug_name`; add hash column for later |
| 11 | Disk/time for 470 quest-sector conversions | ~45 MB JSON per sector | Batch 12–16, parse, delete; ~10 min; `dist/` only |
| 12 | Extractor over-counts (`sts_wat_kab_07_client_signal` subpaths) | naive regex gave 657 "sts sites" | Canonical regex `sts_(ep1_)?<d>_<sub>_<nnn>` → ~110; assert bounds in the data stage |

---

## 7. Open questions for the user

1. **Materialisation philosophy.** Do you want sites to be **always physically
   populated** (S1: journal-activated phases, bounded but stateful) or
   **populated only near the player** (S2: district phase + facts, simpler and
   cheaper)? This is the one decision that shapes the runtime, the DB's dynamic
   side, and how "alive" the city feels when you are not there.
2. **Faction swap fidelity.** Is it acceptable that a conquered site's crew
   keeps its vanilla archetype but changes loyalty/attitude (Tier C2, ships
   fast), or do you require true visual/archetype replacement (Tier B: authored
   Neon prefab + community, more build tooling and a prefab spike)?
3. **Scope of "site".** Do we model all ~500 content sites, or only the ~330
   `ma_*` + ~110 `sts_*` (skipping `mws_*` flavour vignettes and `mq*`/`sq*`
   compounds that share prefabs)?
4. **Dogtown.** There are **zero** `ma_*` sites in Dogtown; it has 13
   `sts_ep1_*` gigs and several `mws_cz_*`. Should Dogtown be conquest-enabled
   from day one, or treated as a neutral enclave with only gigs/espionage?
5. **Player-built garrisons.** Should a converted site spawn *your* NPCs
   (needs Tier B/C) or remain an abstract asset with a UI presence only
   (no spawn, cheapest)? This changes the Organization pillar's feel a lot.
6. **Interiors and the law.** Do you want gig interiors to stay enterable at all
   times (immersion, but players can loot empty rooms) or to be sealed until a
   Neon mission targets them (tighter pacing, requires door/PS control on every
   site)?
7. **`spawn_points` overlap.** Should seized sites also rewrite their
   `spawn_points` rows at runtime so the old faction stops respawning nearby, or
   is community-phase control sufficient?
8. **Display names.** Are generated names (`"Kabuki Safehouse 07"`) acceptable
   for v0, or should the data stage invest in the `journalPathHash` join now?

---

## Appendix A — commands used

```bash
GAME='/home/suvikyi/Games/Cyberpunk 2077'
WK=/home/suvikyi/.cache/neon-ascendancy/wolvenkit-10.0.0-beta.1/WolvenKit.CLI
export DOTNET_ROLL_FORWARD=Major

# indexes (seconds)
$WK archive -l "$GAME/archive/pc/content/basegame_4_gamedata.archive"   > base4.txt
$WK archive -l "$GAME/archive/pc/content/basegame_3_nightcity.archive"  > base3.txt
$WK archive -l "$GAME/archive/pc/ep1/ep1_2_gamedata.archive"            > ep1_2.txt

# site phases + communities (base), ep1 gigs
$WK extract "$GAME/archive/pc/content/basegame_4_gamedata.archive" -o raw \
  -r '(ma_wat_nid_30|ma_wat_lch_05|ma_hey_gle_104|ma_std_arr_06|sts_wat_kab_05|sts_wat_kab_07|sts_wat_kab_04|sts_wat_nid_01|sts_hey_spr_01|mws_arr_04|mws_wbr_04)\.*\.(questphase|community)$'
$WK convert s raw/base

# streaming block: sector <-> prefab <-> bbox
$WK extract "$GAME/archive/pc/content/basegame_3_nightcity.archive" -o raw -w "*all.streamingblock"
$WK convert s raw/base/worlds/03_night_city/_compiled/default/blocks/all.streamingblock
$WK extract "$GAME/archive/pc/ep1/ep1_1_nightcity.archive" -o raw -w "*ep1*all.streamingblock"
$WK convert s raw/base/worlds/03_night_city/_compiled/default/ep1/blocks/all.streamingblock

# site Quest sectors
$WK extract "$GAME/archive/pc/content/basegame_3_nightcity.archive" -o raw \
  -r 'quest_(36ce86f6ae0770ea|7e741456ad3217ad|b0269e4aed881cea)\.streamingsector$'
$WK convert s raw/base/worlds/03_night_city/_compiled/default/quest_36ce86f6ae0770ea.streamingsector

# registry liveness bits (existing extract, no new archive read)
python3 - <<'PY'
import json
p='dist/extract/raw/base/worlds/03_night_city/_compiled/default/always_loaded_1.streamingsector.json'
rc=json.load(open(p))['Data']['RootChunk']
for n in rc['nodes']:
    d=n.get('Data') or {}
    if d.get('$type')=='worldCommunityRegistryNode':
        items=d['communitiesData']; break
print(len(items), sum(len(i.get('entriesInitialState') or []) for i in items))
PY
```

## Appendix B — sampled site dossiers

| Site | Family | Nodes of interest | Community model |
| --- | --- | --- | --- |
| `sts_wat_kab_07` "casino bar" | interior gig | 79 spots, 7 patrol splines, 5 guard areas, 3 population spawners, 1 crowd-null, 1 audio signpost | 15-entry `#kab_07_com_enemies` (phases `0combat`/`alarm`/`distractHologram`), `_hard_mode`, `_backup`, crowds |
| `sts_wat_kab_05` "client signal" | interior gig (clinic) | doors `#kab_05_entrance_door_002`, `_solo`, `_ripper`; `mq024` shares the prefab | `sts_wat_kab_05_enemies`, `_enemies_1st_floor`, `_enemies_2nd_floor` |
| `sts_wat_kab_04` "psycho penthouse" | interior gig | `LiftControllerPS` floors, `DoorControllerPS` `ForcePower`, reinforcement car | `sts_wat_kab_04_penthouse`, `_backup`, `_guests_com`, `_receptionist` |
| `sts_ep1_06` "Zembinsky" (Dogtown) | interior gig, shared with `mq304` | 11 spots, 7 `mq304_spl_*` splines, 5 triggers, no devices | `sts_ep1_06_enemies_ground_floor`, `_ic_night_ff`, `_crowd` |
| `ma_wat_nid_30` "hidden stash" | exterior hustle (roof/warehouse) | 6 drone workspots, 2 drone patrol splines, 2 guard areas, security area + security system | prefab-scoped `$/…/#loc_ma_wat_nid_30_openworld/ma_hidden_stash_com` |
| `ma_wat_kab_07` "rooftop stash" | exterior hustle | 14 spots, 4 patrol splines, 4 guard areas, security area ×2 + security system | `#ma_wat_kab_07_com_tyger_claw` (6 entries), `_junkie` |

## Appendix C — API index (verified in `refs/`)

| Symbol | Signature | File:line |
| --- | --- | --- |
| `CommunitySystem` | 4 crowd/density natives only | `orphans.swift:51491` |
| `DynamicSpawnSystem` | 3 query natives only | `core/systems/dynamicSpawnSystem.swift:4` |
| `PreventionSpawnSystem.RequestUnitSpawn` | `(TweakDBID, WorldTransform) -> Uint32` | `core/systems/preventionSpawnSystem.swift:8` |
| `PreventionSystem.OnPreventionUnitSpawnedRequest` | ticket-or-return | `core/systems/preventionSystem.swift:1615` |
| `GetFixedEntityIdsFromSpawnerEntityID` | `(EntityID, [CName], GameInstance, out [EntityID])` | `orphans.swift:34038` |
| `EntitySpawnerEventsBroadcaster.RegisterSpawnerEventPSListener` | `(EntityID, CName, PersistentID, CName) -> Uint32` | `orphans.swift:34042` |
| `gameEntitySpawnerEventType` | `Spawn/Despawn/Death` | `orphans.swift:3537` |
| `CommunityProxyPS` | spawner listener + `ExtractEntityIDs` | `cyberpunk/network/squadNode.swift:2,181` |
| `SecurityAreaControllerPS.ExtractSquadProxies` | child `CommunityProxyPS` lookup | `cyberpunk/devices/masters/systems/securitySystem/securityAreaController.swift:673` |
| `NPCReference` | `{communitySpawner: NodeRef, entryName: CName}` | `securitySystemMisc.swift:376` |
| `ResolveNodeRef` | `(NodeRef, GlobalNodeRef) -> GlobalNodeRef` | `orphans.swift:34317` |
| `ResolveNodeRefWithEntityID` | `(NodeRef, EntityID) -> GlobalNodeRef` | `orphans.swift:28299` |
| `GlobalNodeRef.IsDefined` / `GlobalNodeID.GetRoot` | — | `orphans.swift:28303`, `orphans.swift:33009` |
| `Entity.QueueEventForNodeID` | `(GlobalNodeRef, ref<Event>) -> Bool` | `core/entity/entity.swift:10` |
| `Device.GetDevicePS` | `-> ref<ScriptableDeviceComponentPS>` | `cyberpunk/devices/core/deviceComponentBase.swift:2` |
| `QuestForcePower` / `QuestForceOpen` / `QuestForceON` / `QuestForceOFF` | `ActionBool` subclasses | `cyberpunk/devices/core/baseDeviceActions.swift:2001-2040` |
| `DoorControllerPS` | `m_isOpened/m_isLocked/m_isSealed`, `SetDefaultDoorState` | `cyberpunk/devices/door/doorController.swift:36,261` |
| `AIComponent.SendCommand` | `(ref<AICommand>) -> Bool` | `core/components/aiComponent.swift:11` |
| `AIPatrolCommand` | `pathParams: ref<AIPatrolPathParameters>` | `orphans.swift:48458` |
| `AIPatrolPathParameters` | `path: NodeRef`, `isBackAndForth`, `isInfinite`, `movementType` | `orphans.swift:58286` |
| `AIUseWorkspotCommand` | `workspotNode: NodeRef`, `entryId`, `jumpToEntry` | `orphans.swift:48681` |
| `AIMoveToCommand` | `movementTarget: AIPositionSpec` | `orphans.swift:45302` |
| `AIPositionSpec.SetWorldPosition` | `(script_ref<AIPositionSpec>, WorldPosition)` | `orphans.swift:34758` |
| `AttitudeAgent` | `SetAttitudeGroup`, `SetAttitudeTowards`, `SetAttitudeGroupUnsavable` | `orphans.swift:20443-20458` |
| `WorkspotGameSystem.PlayInDevice` | `(device, actor, …)` | `orphans.swift:19161` |
| `QuestsSystem` | facts + listeners only | `orphans.swift:18132` |
| `worldCommunityEntryInitialState` | `{entryName, initialPhaseName, entryActiveOnStart}` | `RED4ext.SDK/…/world/CommunityEntryInitialState.hpp` |
| `world::AISpotNode` | `spot`, `markings`, `crowdWhitelist/Blacklist`, `isWorkspotInfinite` | `RED4ext.SDK/…/world/AISpotNode.hpp` |
| `world::PatrolSplineNode` | `patrolPoints[]`, `patrolPointDefs[]` | `RED4ext.SDK/…/world/PatrolSplineNode.hpp` |
| `world::GuardAreaNode` | `communityEntries[]`, `combatCommunityEntries[]`, `pursuitArea/Range` | `RED4ext.SDK/…/world/GuardAreaNode.hpp` |
| `world::DeviceNode` | `deviceClassName`, `deviceConnections[]` | `RED4ext.SDK/…/world/DeviceNode.hpp` |
| `world::StreamingSectorDescriptor` | `streamingBox`, `questPrefabNodeRef`, `variants`, `category` | `RED4ext.SDK/…/world/StreamingSectorDescriptor.hpp` |
| `world::StreamingSectorCategory` | `Exterior/Interior/Quest/Navigation/AlwaysLoaded` | `RED4ext.SDK/…/world/StreamingSectorCategory.hpp` |
