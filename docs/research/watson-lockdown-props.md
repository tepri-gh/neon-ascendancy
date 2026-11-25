# Research — Watson Lockdown Props in a Clean-Slate Start

**Target:** Cyberpunk 2077 2.5 + Phantom Liberty, redscript 1.0.2 (Codeware-free),
WolvenKit.CLI 10.0.0-beta.1 (Linux).
**Date:** 2026-11-25.
**Scope:** the physical prologue-lockdown traffic props (barricades, parked
"blockade" cars/trucks, barriers) that remain on the Watson exit bridges in an
Ascendancy run, and why `watson_prolog_lock = 0` / `watson_prolog_unlock = 1`
does not remove them.
**Non-goals:** implementation. This document writes no code and touches no
`tools/`, `data/`, or `src/` file.

**Evidence grades**

- **[V]**: verified in this session by extracting the local 2.5 archives with the
  pinned WolvenKit.CLI and reading the serialized resource.
- **[R]**: structurally certain from the extracted data, but the runtime
  behaviour still needs one in-game pass.
- **[H]**: hypothesis. Must be tested in-game before it becomes a design
  dependency.

Raw extracts were made into a session scratchpad and are gone; every number and
path below is reproducible with the commands in Appendix A.

---

## 0. Executive summary

1. **The props are not the `watson_prolog_lock` roadblock phases.** They are
   pre-placed barricade meshes baked into **`Exterior` streaming sectors** and
   gated by a named `worldStreamingSectorVariant`:
   **`q001_bridge_blockade`**. The block census has **31 occurrences of that
   variant, and all 31 are `enabledByDefault: 1`**, spread over 17 exterior
   sectors along the q001 bridge corridor. **[V]**

2. **Vanilla hides that variant exactly once:** in
   `q001_ride_to_mb.questphase`, node 230 emits a
   `questWorldDataManagerNodeDefinition -> questTogglePrefabVariant_NodeType`
   that sets `q001_bridge_blockade = 0` on `#wejt_03_devices`, behind the pause
   `q001_aft_blockade_scene >= 1`. A clean-slate run never executes q001, so the
   default-on barricades are frozen in place. **[V]**

3. **The Act-1 roadblock keepers are three separate phases**
   (`lch_`, `kab_`, `nid_prolog_roadblocks.questphase`). They do not depend on
   variants alone: they activate/deactivate **vehicle spawners** (bridge cars,
   roadblock cars), **guard communities**, **crowd null-areas**, and the
   `security_systems` variant. The LCH phase additionally shows/hides the
   `prolog_blockades` geometry variant. **[V]**

4. **The clean-slate archive copies `open_world_content` node 7 with its inline
   pause intact.** That pause is `watson_prolog_lock > 0`. In a boot where the
   fact is already `0`, the phase node never starts, so neither the activate
   branch nor the `watson_prolog_lock == 0` **cleanup branch** runs. The
   `clean_slate_spec.json` note "inert while unlocked" is therefore wrong for a
   cold boot: the cleanup that vanilla relies on is skipped. **[V]**

5. **There are two independent leftovers, and both must be handled:**
   `q001_bridge_blockade` static geometry (default-on, story-only toggle), and
   the roadblock spawners/communities (default state, cleaned up only by the
   skipped branch). The reported "truck" is most plausibly one of the
   `#lch_bridge_b_car_001..016` / `#kab_prolog_ow_roadblock_car_*` /
   `#nid_prolog_ow_roadblock_car_*` spawner vehicles, or the `road_block` mesh
   set. **[R]/[H]** — the spawner default state is the one runtime unknown.

6. **Minimal story-free change:** an always-on cleanup node group in
   `ascendancy.questphase`, emitted after the initial fact managers:
   - hide `q001_bridge_blockade` on `#wejt_03_devices` (verbatim vanilla q001
     node 230);
   - hide `security_systems` on the three devices prefabs and `prolog_blockades`
     on the LCH architecture prefab;
   - deactivate the 9 roadblock communities and 60 vehicle spawners.

7. **`add_variant_toggle_node` covers only the variant part.** The builder
   already has `add_community_spawn_node` for the 9 communities, but it has **no
   `questSpawner_NodeType` emitter**: `add_spawn_set_node` emits
   `questSpawnSet_NodeType`, which is a different node type and will not
   deactivate the bridge-car spawners. One new emitter (or a copied vanilla
   cleanup subgraph) is required. **[V]**

8. **Traffic:** the traffic spline data (`all.traffic_persistent`, 31,718 lanes)
   contains no blocker records. `RoadBlock` is a device with an off-mesh/nav
   effect (`RoadBlockControllerPS.m_isBlocking`), and the bridge null-area
   trigger (`#q001_tr_bridge_null_area`) lives in the story-only
   `#q001_pr_police_blockade` prefab. If the static props are visible without
   the story trigger, AI traffic will drive through them. Removing the props
   removes the symptom; do not add a new traffic system. **[V]/[R]**

9. **The blocking runtime question:** do a quest-phase variant toggle and
   spawner deactivation issued from H10 at boot stick when the bridge sectors
   later stream? The spawner/community refs live in `always_loaded_1/2`
   sectors, so they should resolve; the exterior variant may need a proximity
   re-apply. This is the first in-game check (§7). **[H]**

---

## 1. What is physically on the bridge

### 1.1 The four layers

| Layer | Lives in | Controlled by | Removed by |
| --- | --- | --- | --- |
| **Baked barricade meshes** | `Exterior` streaming sectors, `worldStreamingSectorVariant` groups | Sector variant defaults (`enabledByDefault`) plus `questTogglePrefabVariant_NodeType` | A phase toggle (`show = 0`) |
| **Blockade cars/trucks** | Roadblock prefabs in `always_loaded_1/2` (`worldEntityNode`/spawner nodes) | `questSpawnManagerNodeDefinition -> questSpawner_NodeType` (Activate/Deactivate) | The phase cleanup branch |
| **Guards / crowd** | `worldCompiledCommunityAreaNode` + communities | `questCommunityTemplate_NodeType`, `questCrowdManagerNodeType_EnableNullArea` | The phase cleanup branch |
| **Security systems** | `*_prolog_roadblocks_devices_prefab*` | `questTogglePrefabVariant_NodeType` (`security_systems`) | The phase cleanup branch |

### 1.2 The `q001_bridge_blockade` variant is default-on

Census of `base\worlds\03_night_city\_compiled\default\blocks\all.streamingblock`
(23,718 descriptors): **[V]**

| Variant | Entries | `enabledByDefault = 1` | `enabledByDefault = 0` |
| --- | ---: | ---: | ---: |
| `q001_bridge_blockade` | 31 | **31** | 0 |
| `prolog_blockades` | 253 | 0 | 253 |
| `road_blockades_kab` | 31 | 0 | 31 |
| `road_blockades_lch` | 19 | 0 | 19 |
| `road_blockades_nid` | 41 | 0 | 41 |

The 31 `q001_bridge_blockade` entries are spread over 17 exterior sectors. The
bridge corridor sectors are `exterior_-13_15`, `-16_15`, `-16_16`, `-17_15`,
`-17_16`, `-18_15`, `-18_16` (all `on`), plus ten sectors further along the q001
route at grid cells `-2..-9 / 1..8`.

In `exterior_-18_15` the variant groups resolve to the actual props: **[V]**

- group 2 and 9 (`q001_bridge_blockade`, default 1) contain
  `decoset_blocade_long_holo_a_v1_*`, `decoset_blocade_single_red_a_*`,
  `blockade_h_prefab...`, and `road_block_prefab6NTLFYY/road_block_prefabWMFNVQQ`
  (`base\environment\decoration\public_utility\roadblock\blockade\blockade_h.mesh`);
- group 0 (`default`, default 1) adds a fence barricade, a street lamp, a
  `decoset_large_concrete_barricade_c_v1`, and a `blockade_h`;
- groups 3/7/10 (`prolog_blockades`) and 1/5/8 (`road_blockades_kab`) are the
  large concrete-barricade/fence/holo sets and are **off by default**.

The same pattern appears in `exterior_-16_15` (q001 groups carry
`wbr_bridge_barrels` meshes, 146 instances) and `exterior_-13_15` (four
default-on q001 groups on the Japantown side). **[V]**

**Consequence:** with no phase running, the default-on `q001_bridge_blockade`
groups render. `prolog_blockades` and `road_blockades_*` do not.

### 1.3 The roadblock prefabs and their exact contents

Each sub-district has one prefab root declared by its phase: **[V]**

| Sub-district | Phase `phasePrefabs` root | Devices sub-prefab (variant host) |
| --- | --- | --- |
| LCH | `#lch_prolog_roadblocks_openworld` | `$/03_night_city/c_watson/little_china/little_china_openworld_prefab3SE7WFY/#lch_prolog_roadblocks/lch_prolog_roadblocks_env_prefab2GUBPEA/lch_prolog_roadblocks_devices_prefab2ULRIOY` |
| KAB | `#kab_prolog_roadblockades_openworld` (spelling is `...ades`, not `...s`) | `$/03_night_city/c_watson/kabuki/kabuki_openworld_prefab74SGL5A/kab_prolog_roadblocks_prefab3WPPOBQ/kab_prolog_roadblocks_devices_prefabJDN4YPY` |
| NID | `#nid_prolog_roadblocks_openworld` | `$/03_night_city/c_watson/northside/northside_openworld_prefabIDPOWEI/nid_prolog_roadblocks_prefabODFHNWI/nid_prolog_roadblocks_devices_prefabQUSH5AY` |

LCH also has an architecture prefab that hosts the `prolog_blockades` variant:
`.../lch_prolog_roadblocks_architecture_prefabXPXGK6Y`.

The node refs under these prefabs (in `always_loaded_1/2`) include: **[V]**

- `#lch_bridge_b_car_001 .. _016` — 16 bridge vehicles (the parked "traffic jam"
  / truck set);
- `#lch_prolog_ow_roadblock_car_00{1..8}_{A,C}`, `#lch_prolog_ow_roadblocks_com_{A,C}`,
  `#lch_prolog_ow_roadblock_{lower,upper}_b_com`, and the null areas
  `#lch_prolog_a_null`, `#lch_prolog_b_upper_null`, `#lch_prolog_b_lower_null`,
  `#lch_prolog_c_null`;
- `#kab_prolog_ow_roadblock_car_00{1,2}_A_l`,
  `#kab_prolog_ow_roadblock_car_00{1,3..8}_B`,
  `#kab_prolog_ow_roadblocks_com_{A_l,B}`, `#kab_prolog_{a,b}_null`;
- `#nid_prolog_ow_roadblock_car_00{1..7}_{B,C}`,
  `#nid_prolog_ow_roadblock_car_00{1..5}_A[_001]`,
  `#nid_prolog_ow_roadblocks_com_{A,B,C}`, `#nid_prolog_{a,b,c}_null`.

Whether these spawners are active before their phase runs is the runtime
unknown. They are in `always_loaded` sectors, so the node refs exist from boot;
the spawner's default activation state decides whether the cars are visible.
**[R]/[H]**

### 1.4 Metro station blockades (separate, already safe)

`open_world_content.questphase` node 35 toggles the variant
`prolog_blockade` (one station uses `prologue_blockade`) on five NCART station
decoration prefabs: `#metro_station_arasaka_waterfront_decoration`,
`#metro_station_little_china_hospital_decoration`,
`#metro_station_lch_north_decoration`, `#metro_station_wlc_south_decoration`,
`#metro_station_wlc_megabuilding_h7_decoration`. The clean-slate archive does
not keep node 35, and these variants are `enabledByDefault: 0`, so the station
blockades are already absent. **[V]**

### 1.5 The q001 bridge blockade (story-only)

`q001_ride_to_mb.questphase` declares `#q001_pr_police_blockade`, which contains
`#q001_ws_policecar_blockade`, `#q001_ws_policeman01_car_blockade`,
`#q001_ws_policeman02_car_blockade`, `#q001_ws_quadra_blockade`,
`#q001_ws_policemech_blockade`, `#q001_com_police_blockade`, and the triggers
`#q001_tr_police_blockade`, `#q001_tr_bridge_null_area`,
`#q001_tr_cna_crosswalk_to_mb1..4`, `#q001_tr_gate_for_closing_player`. **[V]**

This prefab is **not declared** in clean-slate, so its police car/officers and
its bridge null area should not exist. The visible barricades are the baked
`q001_bridge_blockade` group, not this prefab. **[R]**

---

## 2. What vanilla uses to remove them, and when

### 2.1 The phase graph that owns the Watson lockdown

`base\open_world\phases\open_world_content.questphase` node 7 is an inline
`questPhaseNodeDefinition`. Its inner graph begins with a
`questPauseConditionNodeDefinition` whose `questVarComparison_ConditionType` is
`watson_prolog_lock > 0` (inner node id 10) and then fans out to three
`questPhaseNodeDefinition`s referencing the LCH/KAB/NID roadblock phases. **[V]**

So in vanilla:

- `q001_ride_to_mb` sets `watson_prolog_lock = 1`;
- node 7's pause resolves, the three sub-phases start, and their activate
  branches spawn the cars/guards and show the security systems;
- `q101.questphase` sets `watson_prolog_lock = 0`;
- each sub-phase has `watson_prolog_lock == 0` pause nodes that run the cleanup
  branches (deactivate spawners/communities, hide variants) and then terminate.

`q101.questphase` does not touch any blockade variant; it only writes the fact.
**[V]**

### 2.2 The exact cleanup work per phase

Extracted from `base\open_world\phases\prolog_roadblocks\*.questphase` in this
session. Every `Deactivate` below is a `questSpawnManagerNodeDefinition`
(`questSpawner_NodeType` or `questCommunityTemplate_NodeType`) on the
`watson_prolog_lock == 0` branch. **[V]**

**LCH (`lch_prolog_roadblocks.questphase`)** — 31 spawners (16 bridge cars +
15 roadblock cars), 4 communities:

```text
spawners:
#lch_bridge_b_car_001 .. #lch_bridge_b_car_016
#lch_prolog_ow_roadblock_car_00{1..8}_A
#lch_prolog_ow_roadblock_car_00{1..7}_C
communities:
#lch_prolog_ow_roadblocks_com_A
#lch_prolog_ow_roadblock_lower_b_com
#lch_prolog_ow_roadblock_upper_b_com
#lch_prolog_ow_roadblocks_com_C
variant toggles (show = 0):
.../lch_prolog_roadblocks_architecture_prefabXPXGK6Y  { prolog_blockades: 0 }
.../lch_prolog_roadblocks_devices_prefab2ULRIOY       { security_systems: 0 }
crowd null areas (enable = 0):
#lch_prolog_a_null, #lch_prolog_b_upper_null,
#lch_prolog_b_lower_null, #lch_prolog_c_null,
#lch_prolog_b_upper_null_001
```

**KAB (`kab_prolog_roadblocks.questphase`)** — 9 spawners, 2 communities:

```text
spawners:
#kab_prolog_ow_roadblock_car_001_A_l
#kab_prolog_ow_roadblock_car_002_A_l
#kab_prolog_ow_roadblock_car_00{1,3..8}_B
communities:
#kab_prolog_ow_roadblocks_com_A_l
#kab_prolog_ow_roadblocks_com_B
variant toggles (show = 0):
.../kab_prolog_roadblocks_devices_prefabJDN4YPY  { security_systems: 0 }
crowd null areas (enable = 0):
#kab_prolog_a_null, #kab_prolog_b_null
```

The KAB phase has **no** geometric `prolog_blockades` toggle. Its barricade
geometry relies on the prefab's baked default groups; the vehicles/guards carry
the lockdown. **[V]**

**NID (`nid_prolog_roadblocks.questphase`)** — 20 spawners, 3 communities:

```text
spawners:
#nid_prolog_ow_roadblock_car_00{1..7}_C
#nid_prolog_ow_roadblock_car_00{1..8}_B
#nid_prolog_ow_roadblock_car_001_A_001
#nid_prolog_ow_roadblock_car_00{2..5}_A
communities:
#nid_prolog_ow_roadblocks_com_A/B/C
variant toggles (show = 0):
.../nid_prolog_roadblocks_devices_prefabQUSH5AY  { security_systems: 0 }
crowd null areas (enable = 0):
#nid_prolog_a_null, #nid_prolog_b_null, #nid_prolog_c_null
```

### 2.3 The q001 bridge hide

`q001_ride_to_mb.questphase` node 229 shows and node 230 hides the bridge
blockade on `#wejt_03_devices`: **[V]**

```json
{
  "$type": "questWorldDataManagerNodeDefinition",
  "type": {
    "$type": "questTogglePrefabVariant_NodeType",
    "params": [{
      "$type": "questTogglePrefabVariant_NodeTypeParams",
      "prefabNodeRef": { "$value": "#wejt_03_devices" },
      "variantStates": [{
        "$type": "questVariantState",
        "name": { "$value": "q001_bridge_blockade" },
        "show": 0
      }]
    }]
  }
}
```

The phase's only story-fact gate is a `q001_aft_blockade_scene >= 1` pause
(node 227); the hide belongs to the post-blockade flow rather than to the
opening show. The full path of the target prefab is
`$/03_night_city/c_westbrook/japan_town/wejt_03/wejt_03_gameplay_prefabPBTDZFQ/#wejt_03_devices`.
**[V]**

No other quest phase toggles `q001_bridge_blockade`. A sweep of all 1,477
`base\open_world\*.questphase` resources found zero occurrences of
`q001_bridge_blockade`; the only `prolog_blockades` occurrence was in
`lch_prolog_roadblocks.questphase`. `q101.questphase` writes the fact only.
**[V]**

### 2.4 Why the clean-slate start leaves them in place

`data/clean-slate/clean_slate_spec.json:113` keeps `open_world_content` node 7
and notes "pause-gated on watson_prolog_lock > 0 (inert while unlocked)".
`build-clean-slate.py`'s `add_copied_phase_node` deep-copies node 7 with its
inner pause untouched. With the initial fact already `watson_prolog_lock = 0`
(`clean_slate_spec.json`; `SanitizerSystem.reds:287` and `:569`):

- node 7's `watson_prolog_lock > 0` pause never resolves, so the three
  sub-phases never start;
- their `watson_prolog_lock == 0` cleanup branches therefore never run;
- the baked `q001_bridge_blockade` groups stay at their default-on state;
- any spawner/community that defaults active stays active.

This is the root cause. It is not a fact-write problem. **[V]/[R]**

---

## 3. Recommended minimal, story-free change

### 3.1 One always-on cleanup group in `ascendancy.questphase`

The clean-slate hub fans out directly from the final fact node (`fan`) after all
initial facts are set (`build-clean-slate.py`, `build_questphase`). Add a chain
off that fan-out (before or after the kept phases; order is not important for
idempotent deactivations):

1. **Hide the story bridge blockade** — one
   `questWorldDataManagerNodeDefinition -> questTogglePrefabVariant_NodeType`:

   ```text
   prefabNodeRef: #wejt_03_devices
   variantStates: [ q001_bridge_blockade = 0 ]
   ```

   This is a verbatim copy of vanilla q001 node 230, minus its story pause.

2. **Hide the Act-1 security/geometry variants** — one toggle per prefab:

   ```text
   .../lch_prolog_roadblocks_architecture_prefabXPXGK6Y  { prolog_blockades: 0 }
   .../lch_prolog_roadblocks_devices_prefab2ULRIOY       { security_systems: 0 }
   .../kab_prolog_roadblocks_devices_prefabJDN4YPY       { security_systems: 0 }
   .../nid_prolog_roadblocks_devices_prefabQUSH5AY       { security_systems: 0 }
   ```

3. **Deactivate the 9 roadblock communities** —
   `questCommunityTemplate_NodeType`, `action: Deactivate`:
   the four LCH, two KAB, three NID refs listed in §2.2.

4. **Deactivate the 60 vehicle spawners** —
   `questSpawner_NodeType`, `action: Deactivate`, the exact refs listed in §2.2.
   These are the bridge cars / parked blockade vehicles. Deactivating an already
   inactive spawner is harmless, so including them is safe even if the probe
   shows they were never active.

5. **Optional:** `questCrowdManagerNodeType_EnableNullArea` with `enable = 0`
   for the 10 null areas. Their defaults are 0 and only the skipped activate
   branch sets them to 1, so this is normally a no-op; include it only if the
   probe shows a null area was enabled.

All five groups are idempotent. Running them twice, or on a save where a bridge
already streamed, produces no new state.

### 3.2 Why not simply un-gate node 7?

Every roadblock phase's activate branch is **not** gated by
`watson_prolog_lock`; only its cleanup branch is (`== 0`). The outer node 7
pause is the only `> 0` gate. Removing or bypassing that pause at boot with the
fact already `0` would run the activate and cleanup branches concurrently:
cars/guards could spawn and the prefabs could flash before the deactivations
land. Emitting the cleanup directly is deterministic; un-gating is not. **[R]**

An alternative, `watson_prolog_lock = 1` at boot then `= 0` after a delay, also
re-locks NCART/data terms and the map for the delay window. Do not do it.

### 3.3 If boot-time toggles do not stick

The spawner/community refs are in `always_loaded_1/2`, so their
`questSpawnManagerNodeDefinition` actions should resolve from H10 even though
the bridge sectors are far away. The exterior variant groups are streamed only
near the bridge. If §7.2 shows the static props reappear when the bridge
streams, reuse the venue-probe pattern: add a per-bridge proximity pause
(`add_proximity_pause_node`, already used by `venue_phases.json`) before the
`q001_bridge_blockade = 0` toggle. The bridge has story triggers
(`#q001_tr_bridge_null_area`, `#q001_tr_police_blockade`) that can serve as
proximity refs, but they belong to the undeclared story prefab; prefer a
barricade or road workspot ref that is present in the exterior sector.

Do **not** patch the streaming sector with a new archive override unless the
quest-phase route is proven impossible. An ArchiveXL sector override is the
last-resort lever, not the first.

---

## 4. Does the existing builder cover it?

| Needed node | Builder status | Verdict |
| --- | --- | --- |
| `questWorldDataManagerNodeDefinition` -> `questTogglePrefabVariant_NodeType` (q001, LCH, KAB, NID variants) | `add_variant_toggle_node` (`tools/build-clean-slate.py`, around line 649) emits exactly this shape, one prefab + state map per call. | **Yes.** Emit five calls (or extend the method to accept a list). |
| `questSpawnManagerNodeDefinition` -> `questCommunityTemplate_NodeType` deactivate (9 communities) | `add_community_spawn_node` (around line 530) sets `action`, `spawnerReference`, `communityEntryName`, `communityEntryPhaseName`. | **Yes.** Pass `action="Deactivate"`. |
| `questSpawnManagerNodeDefinition` -> `questSpawner_NodeType` deactivate (60 vehicle spawners) | No emitter. `add_spawn_set_node` (around line 556) emits `questSpawnSet_NodeType`, a different node type (used for character spawn sets). | **No.** Add `add_spawner_node` or a `kind="spawner"` parameter. |
| `questCrowdManagerNodeDefinition` -> `questCrowdManagerNodeType_EnableNullArea` | No emitter. | Not needed by default (nulls are 0). |
| Declaring the three `#*_openworld` prefabs (`phasePrefabs`) | `build_venue_probe` and `build_cast_and_hubs` emit `phasePrefabs` from spec lists. | **Yes**, but the venue phase is gated on `na_dev_venue_probe`; an always-on boot group needs its own spec section or direct wiring off the hub fan-out. |

The venue `variant_toggles` path is **not** the right carrier as-is: the whole
`venue_probe.questphase` is wired behind `na_dev_venue_probe > 0` and kept
dormant. The cleanup must be on the always-on `ascendancy.questphase` path.

Line numbers are approximate because `tools/build-clean-slate.py` is being
edited concurrently; the method names are the stable reference.

---

## 5. Traffic and navigation side effects

### 5.1 Traffic lanes have no blockers

`base\worlds\03_night_city\sectors\_generated\traffic\all.traffic_persistent`
has 31,718 `worldTrafficLanePersistent` records. A string census of the
serialized resource found **zero** blocker / forbidden / blockade fields; a lane
is geometry, speed, crowd counts, and connections only. AI traffic follows
these splines. **[V]**

### 5.2 `RoadBlock` is a device, not a lane blocker

`base\gameplay\devices\traffic\road_blockade\road_block.ent` is a
`RoadBlock extends InteractiveDevice` with `RoadBlockControllerPS`
(`m_isBlocking`, `QuestForceRoadBlockadeActivate/Deactivate`,
`ToggleOffMeshConnection`). It blocks the **navigation/off-mesh path** and
toggles cover objects; it does not rewrite the traffic lane. **[V]**

These devices are part of the `road_blockades_kab/lch/nid` variants, which are
`enabledByDefault: 0` and only shown while the roadblock phase runs. In
clean-slate they are absent, which is why the static barricade meshes are not
recognised by the traffic system.

### 5.3 The story null area is not present

`#q001_tr_bridge_null_area` (inside `#q001_pr_police_blockade`) is the story-time
traffic null area. It is not declared in clean-slate. The only
`worldVehicleForbiddenAreaNotifier` found in the sampled bridge sectors is
`#dlc6_apart_wbr_jpn_tr_interior_02` (enableNullArea = 1) on an apartment
interior, not on the bridge. **[V]**

### 5.4 Practical consequence

- Removing the visible props removes the "traffic drives into barricades"
  symptom; no additional traffic lane or nav blocker needs to be authored.
- After the cleanup, verify that no orphan `RoadBlock` device remains in
  `IsBlocking = true` state. If one does, it belongs to a variant that should
  have been hidden; fixing the variant is the correct action, not adding a
  traffic block.
- Do not add a `worldVehicleForbiddenAreaNotifier` or a new traffic blocker as a
  first move. There is no evidence it is needed once the props are gone.

---

## 6. Risk register

| Risk | Why it matters | Mitigation |
| --- | --- | --- |
| Boot-time variant toggle is a no-op because the sector is not streamed | Player boots in H10; the bridge exterior is far away | Check §7.2; if needed, add a proximity pause per bridge |
| Variant state resets on sector unload / save load | Vanilla's q001 hide persists, but our one-shot may not | Check §7.3; re-apply on load or near the bridge |
| Deactivating spawners at boot hits nothing | Spawner refs are in `always_loaded`, but the underlying vehicle entities may be in a streamed sector | Probe spawner entity counts before/after; if empty at boot, defer to proximity |
| Declaring the `#*_openworld` prefabs re-activates the very props we hide | The prefab's `default` groups are default-on | Prefer not to declare them unless a toggle needs the prefab; verify in-game |
| The q001 variant is used elsewhere | It is story-only, but the name appears in 17 sectors | It is only toggled by q001; hiding it globally at boot is consistent with post-q001 vanilla |
| Hiding `security_systems` turns off something the player needs | It only disables roadblock turrets/security devices | Review: those are prologue checkpoints, not services |

---

## 7. In-game verification checklist

Use a save copy and the dev CET install. Do not ship these probes.

1. **Baseline at H10.** Boot Start Ascendancy, stand in H10, and log:
   `Game.GetQuestsSystem():GetFactStr("watson_prolog_lock")`,
   `q001_aft_blockade_scene`, and the spawner entity counts for
   `#lch_bridge_b_car_001`, `#kab_prolog_ow_roadblock_car_001_B`,
   `#nid_prolog_ow_roadblock_car_001_A_001`
   (`GetFixedEntityIdsFromSpawnerEntityID`). This settles whether the cars are
   default-active before any phase runs. **[H]**

2. **Variant timing.** Apply only the `#wejt_03_devices`
   `{q001_bridge_blockade: 0}` toggle at boot. Drive to the Watson/Westbrook
   bridge and check the barricade meshes. If they are absent while the sector
   is far away but reappear as it streams, the toggle needs a proximity re-run
   or a sector-level override. **[H]**

3. **Persistence.** With the cleanup applied, save, reload, fast-travel away,
   and drive back. Confirm the barricades and cars stay gone. **[H]**

4. **Spawner cleanup.** After the community/spawner deactivations, re-read the
   spawner counts from step 1; they should be zero. Check the LCH bridge for the
   parked car/truck set (`#lch_bridge_b_car_001..016`). **[H]**

5. **Traffic.** Watch the bridge lanes for 2-3 minutes day and night. Cars
   should not clip anything. If they do, identify whether a `RoadBlock` device
   is still `IsBlocking()` and which variant owns it. Do not add a new traffic
   blocker. **[H]**

6. **Metro stations.** Confirm the five NCART station decorations show no
   `prolog_blockade` props. Node 35 is not kept, so this should already pass.
   **[R]/[H]**

7. **Regression.** Check that the three `security_systems` toggles did not turn
   off any player-service device, and that the deactivations did not touch a
   non-prologue community with the same prefix. All refs in §2.2 are
   phase-local and prefixed `*_prolog_*` / `lch_bridge_b_*`. **[R]**

---

## 8. Source ledger

### Local scripts and docs

- `data/clean-slate/clean_slate_spec.json:113` — node 7 is kept with the note
  "pause-gated on watson_prolog_lock > 0 (inert while unlocked)".
- `src/r6/scripts/NeonAscendancy/Sandbox/SanitizerSystem.reds:287, :569-573` —
  the only `watson_prolog_lock` writes; no prop handling.
- `tools/build-clean-slate.py` — `add_community_spawn_node` (~530),
  `add_spawn_set_node` (~556), `add_variant_toggle_node` (~649),
  `add_copied_phase_node` (~511), `add_proximity_pause_node` (venue probe),
  `build_questphase` fan-out.
- `data/clean-slate/venue_phases.json:719, :837` — working examples of
  `variant_toggles` (Black Sapphire tower gate, Dogtown dataterms).
- [world-access.md §1.4](world-access.md) — sector variants are not
  script-addressable; a phase that owns the prefab is the supported lever.

### Game resources (2.5, verified in this session)

- `base\open_world\phases\open_world_content.questphase` — node 7 (roadblocks),
  node 35 (metro station blockades).
- `base\open_world\phases\prolog_roadblocks\{lch,kab,nid}_prolog_roadblocks.questphase`
  — prefab roots, spawner/community/crowd cleanup, variant toggles.
- `base\quest\main_quests\prologue\q001\phases\q001_ride_to_mb.questphase`
  — nodes 229/230 (`#wejt_03_devices`, `q001_bridge_blockade`).
- `base\quest\main_quests\part1\q101\q101.questphase` — writes
  `watson_prolog_lock = 0`.
- `base\worlds\03_night_city\_compiled\default\blocks\all.streamingblock` —
  variant census (23,718 descriptors).
- `base\worlds\03_night_city\_compiled\default\exterior_-13_15_0_0`,
  `-16_15_0_0`, `-17_15_0_0`, `-18_15_0_0` `.streamingsector` — variant groups,
  barricade meshes, `road_block.ent` entity nodes.
- `base\worlds\03_night_city\_compiled\default\always_loaded_1/2.streamingsector`
  — prefab node refs for the bridge cars, guards, null areas, q001 police
  blockade.
- `base\worlds\03_night_city\sectors\_generated\traffic\all.traffic_persistent`
  — 31,718 lanes; no blocker records.
- `base\gameplay\devices\traffic\road_blockade\road_block.ent` and
  `road_block_area.ent` — `RoadBlock` / `RoadBlockControllerPS`,
  `RoadBlockTrap`.
- `refs/cyberpunk/cyberpunk/devices/roadBlock/roadBlockController.swift:9-31,
  145-153` — `m_isBlocking`, quest activate/deactivate.
- `refs/cyberpunk/cyberpunk/devices/roadBlock/roadBlock.swift:221-231` —
  `ToggleOffMeshConnection` is the nav/AI effect.

---

## Appendix A — reproduction

Pinned tool and archives:

```bash
WK="$HOME/.cache/neon-ascendancy/wolvenkit-10.0.0-beta.1/WolvenKit.CLI"
GAME="$HOME/Games/Cyberpunk 2077"
export DOTNET_ROLL_FORWARD=Major
WORK="$COMMANDCODE_SCRATCHPAD/watson-props"
```

1. Roadblock and q001 phases:

```bash
"$WK" extract "$GAME/archive/pc/content/basegame_4_gamedata.archive" -o "$WORK/ph" \
  -r '^base\\open_world\\phases\\prolog_roadblocks\\.*\.questphase$|^base\\open_world\\phases\\open_world_content\\.questphase$|^base\\quest\\main_quests\\prologue\\q001\\.*\.questphase$|^base\\quest\\main_quests\\part1\\q101\\q101\.questphase$'
"$WK" convert serialize "$WORK/ph"
```

2. Streaming block and variant census:

```bash
"$WK" extract "$GAME/archive/pc/content/basegame_3_nightcity.archive" -o "$WORK/blk" -w "*all.streamingblock"
"$WK" convert serialize "$WORK/blk"
```

Parse `all.streamingblock.json` -> `Data.RootChunk.descriptors`; count
`descriptors[].variants[]` by `name.$value` and `enabledByDefault`.

3. Bridge sectors and traffic:

```bash
"$WK" extract "$GAME/archive/pc/content/basegame_3_nightcity.archive" -o "$WORK/sec" \
  -r 'exterior_(-13_15|-16_15|-17_15|-18_15)_0_0\.streamingsector$'
"$WK" extract "$GAME/archive/pc/content/basegame_3_nightcity.archive" -o "$WORK/trf" \
  -r 'traffic\\all\.traffic_persistent$'
"$WK" convert serialize "$WORK/sec" "$WORK/trf"
```

`variantIndices` / `variantNodes` in the sector align with the descriptor's
`variants` array by index; `variantNodes[i]` lists the
`worldCompiledNodeInstanceSetupInfo.nodeIdx` entries that variant `i` turns on
or off.

4. All-open-world sweep (used to prove no other phase toggles the variant):

```bash
"$WK" extract "$GAME/archive/pc/content/basegame_4_gamedata.archive" -o "$WORK/ow" \
  -r '^base\\open_world\\.*\.questphase$'
"$WK" convert serialize "$WORK/ow"
grep -rl 'q001_bridge_blockade' "$WORK/ow" --include='*.json'
grep -rl 'prolog_blockades'     "$WORK/ow" --include='*.json'
```

---

## 9. Bottom line

- The bridges are not held by `watson_prolog_lock`; they are held by an
  default-on `q001_bridge_blockade` sector variant plus a set of roadblock
  spawners/communities whose cleanup branch the clean-slate boot never reaches.
- Hide the q001 variant (exactly as q001_ride_to_mb node 230 does) and emit the
  three phases' `lock == 0` cleanup: 9 community deactivations, 60 spawner
  deactivations, 4 variant toggles.
- `add_variant_toggle_node` handles the variants and
  `add_community_spawn_node` handles the communities; the 60
  `questSpawner_NodeType` deactivations need one new builder emitter.
- The only blocking unknown is whether a boot-time variant toggle survives the
  bridge sector streaming in. Check that first; use a proximity re-apply only if
  it does not.
