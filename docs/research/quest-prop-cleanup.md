# Research — Quest / Gig / Hustle Prop Cleanup for an Ascendancy Run

**Target:** Cyberpunk 2077 2.5 + Phantom Liberty, redscript 1.0.2 (Codeware-free),
RED4ext 1.31.1, ArchiveXL 1.28.11, TweakXL 1.12.2, WolvenKit.CLI 10.0.0-beta.1 (Linux).
**Date:** 2026-11-25.
**Scope:** remove every quest / job / gig / hustle leftover *object* from the
world in an Ascendancy run — quest shards and data pads on the ground and on
bodies, Evelyn's handbag, quest keycards, NCPD hustle data pads, corpses left
behind by cyberpsycho and hustle scenes. Real loot and vendor stock stay.

**Non-goals:** implementation. This document writes no code and changes no
`tools/`, `data/`, `src/` file. Related reading:
[`world-access.md`](world-access.md) (phase-first venue access),
[`watson-lockdown-props.md`](watson-lockdown-props.md) (the same
"default-on `worldStreamingSectorVariant`" failure mode on the Watson bridges),
[`living-world-site-modeling.md`](living-world-site-modeling.md) (Quest-sector
prefabs), [`option-a-clean-slate-start.md`](option-a-clean-slate-start.md)
(what the clean-slate archive already keeps).

**Evidence grades**

- **[V]**: verified in this session by extracting the local 2.5 archives with
  the pinned WolvenKit.CLI and reading the serialized resource, or by census
  over the shipped plain-text TweakDB (`<game>/tools/redmod/tweaks/`).
- **[R]**: structurally certain from the extracted data; the runtime result
  still needs one in-game pass.
- **[H]**: hypothesis. Must be tested in-game before it becomes a design
  dependency.

Raw extracts were made into a session scratchpad and deleted. Every number and
path below is reproducible with Appendix A.

---

## 0. Executive summary

1. **The clutter is not one system. It is four, with one dominant cause.**

   | Rank | Source | Volume | Fixable by |
   | --- | --- | --- | --- |
   | **1** | **Default-on `bodies` / `body` / `final_loot` / `blood` sector variants** in `Exterior`/`Interior` streaming sectors, pointing at `ma_*` / `sts_*` / `mws_*` prefabs | **284 corpse-container nodes across 123 of 152 such sectors** (measured) | A phase `questTogglePrefabVariant_NodeType` hide (`show = 0`) |
   | **2** | **Missing-object leftovers carried by kept phases** — chiefly `kabuki_vendors.questphase`, which *injects* a gig shard into a vendor's loot (`Items.sts_wat_kab_05_onscreen_001`) | 1 confirmed, small | Drop the inject node, or TweakXL the item |
   | **3** | **Quest-sector prefabs that a kept phase declares** — e.g. `cast_and_hubs` declares `#q005_pr_afterlife`, whose sector ships `{q005_suit_cover_loot_new}` with template `q005_loot_token.ent` | small but visible | Do not declare the story sub-prefab; or hide its loot variant |
   | **4** | **Static quest items placed as plain world entity nodes** (`q005_police_holotape.ent`, `q003_credit_chip.ent`, `q003_gilchrist_corpse.ent`, plus `q001_police_holotape.ent` ×15) | ~25 nodes in the sampled 152 sectors | Node deletion (ArchiveXL `.xl`), last resort |

2. **Why the bodies are there at all — this is the root cause.** Vanilla does
   not ship hustles with corpses on. Each gig/hustle phase **explicitly hides**
   its spoiler variants while the gig is not in its "done" state, and **shows**
   them when the gig completes. Measured over all 455 base gig/hustle/mini-story
   phase resources plus 39 EP1 ones: **939 variant-state writes, 590 distinct
   `(prefab, variant)` pairs with a `show = 0`, 306 of them `body`/`loot`-named,
   and 230 that are hide-only (never re-shown).** Examples, verbatim from the
   resources:

   ```text
   ma_hey_gle_05_phase.questphase   -> <...>/ma_hey_gle_05_loot_prefab7UTUDCQ : final_loot = 0
   ma_hey_gle_05_phase.questphase   -> <...>/ma_hey_gle_05_loot_prefab7UTUDCQ : bodies     = 0
   ```

   The gig/hustle phases are omitted by `clean_slate_spec.json`
   (`omitted_depot_phases`: `street_stories`, `open_world_minor_activities`,
   `mini_world_stories`; plus `excluded_phase_patterns`), so **the hides never
   run** and the sector defaults (`enabledByDefault: 1`) win. This is the exact
   mechanism [`watson-lockdown-props.md`](watson-lockdown-props.md) found for
   the `q001_bridge_blockade` barricades; here it applies city-wide to bodies and
   loot. **[V]**

3. **The corpus of hide instructions is machine-extractable and small.** All of
   it comes from phase resources under
   `base\open_world\{minor_activities,street_stories,mini_world_stories}` and
   `ep1\openworld\{street_stories,mini_world_stories}`. 494 resources, 15 MB
   archived, ~140 MB as JSON, ~40 s to extract+convert on this machine.
   Deriving a `hide` list from that corpus is a generated artefact, not a hand
   list. **[V]**

4. **Recommended removal layers, in order:**

   - **L1 — generated variant-hide group in `ascendancy.questphase`.**
     `tools/build-clean-slate.py` already has `add_variant_toggle_node`
     (`:687`). Emit one `show = 0` per hide-only `(prefab, variant)` pair from
     the extracted corpus into a new always-on chain off the hub fan-out. This
     is the vanilla mechanism, idempotent, save-safe, and removes *bodies, loot
     bags, blood decals and container props* — rank 1 above.
   - **L2 — spec-side hygiene.** Remove the loot-inject node from
     `kabuki_vendors.questphase` (or narrow the kept-phase list), and stop
     declaring story sub-prefabs that ship quest loot (the `#q005_pr_afterlife`
     case). This is exactly the `forbidden_*` guard already present in
     `venue_phases.json`; extend it to the kept-phase/cast layer.
   - **L3 — TweakXL, only for item-record level leaks.** `Items.sts_*` /
     `Items.ma_*` quest records carry the `Quest` tag (356 occurrences across
     the shipped tweaks). Making the *specific* injected record non-spawning or
     removing its `lootDrop` reference is a two-record TweakXL patch. Do **not**
     bulk-edit `Quest`-tagged records: 95 of them live in
     `items/quest/quest_items.tweak` and include armour and weapons the design
     may still want. Blunt, globally-scoped edits are the reason
     `world-access.md` §4.3 rejects TweakXL for door templates.
   - **L4 — ArchiveXL `.xl` streaming-sector patch (`nodeDeletions`), last
     resort.** ArchiveXL 1.28.11 *does* support it — the DLL carries
     `sectors`, `expectedNodes`, `nodeDeletions`, `nodeMutations`,
     `actorDeletions`, `instanceDeletions`, `expectedActors`,
     `expectedInstances`, and the log strings `Patching sector "{}"` /
     `Sector definition for "{}" is missing expected nodes count`. But it is
     **index-based and therefore brittle** (see §3.4). Use it only for
     items that are plain `worldEntityNode`s in an always-on base range, where
     no variant toggle exists.
   - **L5 — runtime redscript despawn: not recommended.** There is no
     `GameObject.Despawn`. `PreventionSpawnSystem.RequestDespawn` exists
     (`refs/cyberpunk/core/systems/preventionSpawnSystem.swift:52`) but it is
     NCPD's own pipeline. A post-attach sweep over streaming sectors is the kind
     of per-frame nearest-entity work the sanitizer doc already forbids.

5. **No new native code is needed.** Every recommended layer is data
   (archive JSON emitted by the existing builder) plus one generated spec file.

6. **What could not be settled statically (§6):** whether a boot-time variant
   toggle issued from H10 sticks when the target `Exterior` sector streams much
   later, whether a hidden `bodies` variant also removes the lootable interaction
   (vs. leaving an empty container), and whether `cast_and_hubs`' declared
   prefabs pull more quest loot than the one found.

---

## 1. Classification: where each kind of object comes from

Five distinct storage shapes. Recognising the shape is what decides the fix.

### 1.1 Shape A — entity node inside a streaming sector, gated by a variant

This is the dominant shape for **corpses, loot bags and container props**.

A sector is a list of `nodes` plus a parallel `variantNodes` array. Each entry
of `variantNodes` is a *group* of `worldCompiledNodeInstanceSetupInfo` records
that reference `nodeIdx`; `variantIndices` / the descriptor's `variants[]`
array names each group and gives it an `enabledByDefault` flag. Group 0 is the
always-on base range.

Measured on `exterior_-20_42_0_0.streamingsector` **[V]**:

```jsonc
// descriptor (all.streamingblock)
"variants": [
  { "name": "body", "enabledByDefault": 1, "rangeIndex": 1,
    "nodeRef": ".../loc_ma_wat_nid_14_loot_prefabFEIIWDA" },
  { "name": "body", "enabledByDefault": 1, "rangeIndex": 2, "nodeRef": "...same..." }
]
// sector node 444
{ "$type": "worldEntityNode",
  "debugName": "EntityNode_002",
  "appearanceName": "ma_generic_homeless_03_corpse",
  "entityTemplate": { "DepotPath": "base\\gameplay\\loot\\containers\\bodies\\ma_corpse_container.ent" } }
```

**How to recognise it in data:**

| Signal | Value |
| --- | --- |
| Entity template | `base\gameplay\loot\containers\bodies\{ma,wa,mb,mba,wba,mf}_corpse_container.ent`, or `lying_body.ent` |
| Appearance name | `*_corpse` / `*_dead*` (`ma_generic_homeless_03_corpse`, `ma_sts_std_rcr_03_prostitute_02_corpse`, …) |
| Debug name | `{ma_<district>_<sub>_<nn>_loot}`, `{ma_..._body}`, `ma_corpse_container*`, `{worker_}0N` |
| Container chunk | `LootContainerObjectAnimatedByTransform` with `containerType = "Body"`, `contentAssignment = 0`, `hasQuestItems = 0` |
| Variant name | `bodies`, `body`, `Bodies`, `human_bodies`, `dead_bodies`, `corpses`, `final_loot`, `loot`, `blood` |
| Variant nodeRef | the quest prefab path (`/ma_*_loot_prefab*`, `/sts_*_...`, `/mws_*_...`) |

**Quantified** over the 152 sectors that have at least one *default-on*
body/loot variant pointing at a `ma_`/`sts_`/`mws_` prefab **[V]**:

- 284 corpse/body-container nodes in total; 123 of the 152 sectors have ≥1.
- By variant and default flag: `bodies=1` → 130, `final_loot=1` → 76,
  `body=1` → 36, `Bodies=1` → 5, `loot_hide=1` → 2, `after_shoot=1` → 1;
  and a tail at `enabledByDefault: 0` (`bodies` 12, `final_loot` 3, …) which
  is **already correct and must be left alone**.
- Templates: `ma_corpse_container.ent` 176, `wa_corpse_container.ent` 89,
  `mb_corpse_container.ent` 12, `mba_corpse_container.ent` 6,
  `wba_corpse_container.ent` 1.

Note the `*_corpse_container.ent` templates are **generic** — they have 181
(`ma`), 124 (`wa`) appearance entries and carry no loot table of their own.
The loot is either the fixed `contentAssignment` on the instance or a
`lootDrop` on the NPC record that produced the body. **Do not delete the
`.ent`**: it is used by non-quest corpses too. Hide the *variant* instead.

### 1.2 Shape B — entity node in an always-on base range

Same node shape, no variant gate. These are hand-placed story props. In the
152-sector sample **[V]**:

```text
87  sq024_gps_path.ent            (sq024 map pickups)
18  ma_pac_cvi_08_ent_corpse_ma.ent
15  q001_police_holotape.ent
 6  ma_pac_cvi_08_ent_corpse_mb.ent
 4  ma_pac_cvi_08_ent_corpse_wa.ent
 4  ma_wat_nid_22_corpses.ent
 2  ma_wat_kab_02_body.ent
 2  q110_choice_point.ent
 1  q003_credit_chip.ent
 1  q003_gilchrist_corpse.ent
 1  q000_nomad_radio_tower_circut.ent
```

`q001_police_holotape.ent` is a direct, visible quest leftover: the q001 bridge
police blockades are gone (per `watson-lockdown-props.md`), but 15 holotapes
remain. These have **no variant to toggle**; removal needs `nodeDeletions`
(§3.4) or a prefab/phase-ownership change.

### 1.3 Shape C — quest item defined in TweakDB, dropped by loot or a record

**Quest shards, keycards and story items.** Four separate signals, all in the
shipped plain-text TweakDB (`<game>/tools/redmod/tweaks/`) **[V]**:

| Signal | Where | Count |
| --- | --- | --- |
| Base record `QuestItem` (empty class extending `Item`) | `items/quest/quest_items.tweak:6` | the base for 170 records |
| `BaseShard` (extends `Readable`, adds tags `Shard`, `SkipActivityLog`, `HideInBackpackUI`, `HideAtVendor`) | `items/misc/readables.tweak:24` | 30+ records across 4 files |
| Keycards: `itemType = "ItemType.Gen_Keycard"` | `items/quest/keycards.tweak` | 79 records |
| Explicit `CName[] tags = ["Quest"]` | 37 files | **356 occurrences** |

Distribution of the `Quest` tag by file **[V]**:

```text
items/quest/quest_items.tweak           95
items/quest/minor_activity_items.tweak   56
items/quest/sts_items.tweak              45
items/clothing/quest_clothing.tweak      22
items/quest/keycards.tweak               20
items/base_values.tweak                   3
items/quest/samples.tweak                 2
items/consumables/drugs.tweak             2
weapons/.../preset_malorian_overture      2
weapons/.../preset_base_nova / unity / silverhand  1 each
```

The owner's named examples map exactly onto this space:

```text
q105_evelyns_handbag : QuestItem        (quest_items.tweak:499)  "Evelyn's Handbag"
q105_evelyns_cigarette_case : QuestItem (quest_items.tweak:483)
q005_keycard        : Keycard           (keycards.tweak)  tags ["Quest"]
q005_saburo_data_carrier : QuestItem    (quest_items.tweak:363)
```

**Caveat that decides the fix:** `q105_evelyns_handbag` carries **no `tags`
array at all** (`quest_items.tweak:499-508`). Tag-based filtering is therefore
*not* complete. The reliable classifier is **the record's owning directory**
(`items/quest/**`), the base class (`QuestItem` / `BaseShard` / `Keycard`),
*plus* the `Quest` tag, unioned — not the tag alone.

### 1.4 Shape D — loot-table or container content

A corpse's *contents* come from three different places, and this matters:

1. **`LootTable` records** — `items/.../loot/*.tweak`. 1,158 entries reference
   `Items.sts_*` / `Items.ma_*` / `Items.mws_*` across
   `item_pass_loot_tables.tweak`, `minor_activity_loot.tweak`,
   `sts_loot.tweak`, `mws_loot_gang_retaliation.tweak`,
   `sts_loot_gang_retaliation.tweak`. These are the `ItemPass_Shard*` and
   `ma_*_loot_table` families. **[V]**
2. **`lootDrop` on the NPC record** — e.g.
   `characters/npcs/records/quest/minor_activities/ma_hey_gle.tweak:10`
   (`ma_hey_gle_02_outpost_miniboss` → `ma_hey_gle_02_Yukimura_Recipe_loot_table`). **[V]**
3. **`questInjectLoot_NodeType` in a phase** — a phase *adds* an item to an
   existing container. **[V]**

Case (3) is the one that leaks into kept content, see §1.5.

### 1.5 Shape E — spawned or injected by a phase (including kept phases)

Gig/hustle phases do not place most quest items as world nodes; they **spawn or
inject** them. Two mechanisms measured **[V]**:

- **`questInjectLoot_NodeType`** — the only gig-item inject that survives in the
  current kept set is in `kabuki_vendors.questphase`:
  `Items.sts_wat_kab_05_onscreen_001` (`operationType: Inject`, `quantity: 1`),
  a shard from `sts_wat_kab_05`. This is the concrete "quest data pad in a shop"
  leak. 3 inject entries total in the kept set, 2 distinct items.
- **`questSpawnToken_NodeSubType` / `ReserveItemToThisDropPoint`** — used by
  gigs to place a token at a specific container. `sts_wat_kab_05_openworld`
  references `#kab_05_shard` and `Items.kab_05_shard` this way.

Also relevant: `cast_and_hubs.json:phase_prefabs` declares
`#q005_pr_afterlife` "so the cast layer can seat Dexter DeShawn". That
declared story prefab's sector
(`quest_201b9d28a00e19e8`, 94 nodes) contains **[V]**:

```text
node 28  worldEntityNode  {q005_suit_cover_loot_new}
         template base\quest\main_quests\prologue\q005\entities\q005_loot_token.ent
```

So the declared-prefab path *does* drag in quest loot, exactly as the
`venue_phases.json` `forbidden_*` guards were designed to prevent — but the
cast layer has no such guard today.

**Items the mod must keep:** `base_junk_item`, `Items.Junk*`, all
`GenericOuterChestClothing` / weapon presets without the `Quest` tag, vendor
stock records, `Price.Junk` items. The `Quest`-tagged clothing (22 records in
`quest_clothing.tweak`) and the iconic weapon presets in
`quest_items.tweak` are a design decision, not automatically "clutter" — flag
them for the owner rather than deleting them silently.

---

## 2. Removal options in this stack: cost, risk, verdict

### 2.1 ArchiveXL streaming-sector mutations — supported in the pinned version

ArchiveXL 1.28.11's DLL exposes the full sector-patch schema **[V]** (strings
extracted from `red4ext/plugins/ArchiveXL/ArchiveXL.dll`):

```text
streaming / blocks / sectors / path / expectedNodes
nodeDeletions / nodeMutations
actorDeletions / instanceDeletions / actorMutations / instanceMutations
expectedActors / expectedInstances
[{}] Patching sector "{}"...
[{}] Sector "{}" doesn't exist.
Sector definition for "{}" is missing expected nodes count.
Sector definition for "{}" has invalid expected nodes count.
[{}] {}: The target node #{} has type {}, but the mod expects {}.
[{}] {}: The target node #{} has {} actor(s), but the mod expects {}.
[{}] {}: The target node #{} has {} instance(s), but the mod expects {}.
[{}] World streaming is initializing...
[{}] Merging streaming block "{}"...
```

The upstream wiki confirms the YAML shape and the 2.5 caveats **[C]**:

```yaml
streaming:
  sectors:
    - path: base\worlds\03_night_city\_compiled\default\exterior_-6_-4_0_0.streamingsector
      expectedNodes: 1953
      nodeDeletions:
        - index: 41
          type: worldStaticDecalNode
          debugName: decals_084
        - index: 112
          type: worldCollisionNode
          actorDeletions: [3, 4, 7]
          expectedActors: 12
```

Two hard constraints from the same source:

1. **2.5 renumbered and merged almost every sector** into
   `worldCookedStaticMeshNode` / `worldCookedStaticDecalNode` /
   `worldCookedCollisionNode`. Indices from a pre-2.5 file no longer point at
   the same object. Our indices must be generated **for 2.5**.
2. **Removing actors from 2.5 collision nodes needs ArchiveXL newer than
   1.28.1** — 1.28.11 satisfies this.

**Cost/risk:** medium effort, *high brittleness*. Every entry is
`(sector, index, expected type)`. Any game patch or another mod touching the
same sector invalidates it. ArchiveXL *silently ignores* misspelled keys and a
deletion whose actor/instance list it cannot read **removes the whole node** —
a documented footgun. And `expectedNodes` mismatch makes ArchiveXL **skip the
sector entirely**, which is a silent no-op. **[C]**

**Verdict:** technically available, correctly used only for Shape B/E items that
have no variant gate. Not the primary lever.

### 2.2 Not loading a phase or prefab

Already the mod's main mechanism, and it is what *causes* rank-1 clutter as a
side effect: omitting a gig phase skips both its spawns **and its hides**.

- Omit a phase → its `questSpawnManagerNodeDefinition` spawns never happen
  (good), but its `questTogglePrefabVariant_NodeType` hides also never happen
  (bad, and that is the bodies).
- Declare a prefab (`phasePrefabs`) → every node in its Quest sector
  instantiates, including story loot (the `#q005_pr_afterlife` case).

**Cost:** zero. **Risk:** the failure is *silent* and *directional* — you either
get story loot (declared) or you get un-hidden defaults (omitted). This is the
single most important insight of this research: **omission is not neutral.**

### 2.3 Prefab-variant toggles in our archive — the recommended primary lever

`tools/build-clean-slate.py:687` `add_variant_toggle_node(prefab_ref, states)`
emits exactly the node vanilla uses:

```jsonc
{ "$type": "questWorldDataManagerNodeDefinition",
  "type": { "$type": "questTogglePrefabVariant_NodeType",
    "params": [ { "$type": "questTogglePrefabVariant_NodeTypeParams",
      "prefabNodeRef": { "$type": "NodeRef", "$value": "$/03_night_city/..." },
      "variantStates": [ { "$type": "questVariantState",
        "name": "bodies", "show": 0 } ] } ] } }
```

It is already used by `barricade_cleanup.json` and `venue_phases.json`. **The
builder needs no new emitter** for the dominant case.

- **Cost:** low. One generated spec file + one fan-out chain.
- **Risk:** low. Idempotent; `show = 0` on an already-hidden variant is a no-op.
- **Limit:** only covers variants that exist as named groups. It cannot remove
  always-on base-range nodes (Shape B).

### 2.4 TweakXL edits

TweakXL 1.12.2 can rewrite or delete records. Applicable narrowly:

- Null the `lootDrop` on a specific NPC record that drops a gig shard.
- Remove/replace the injected `Items.sts_wat_kab_05_onscreen_001` reference.
- Mark a specific record non-spawning.

**Cost:** low per record. **Risk:** *global* — 356 `Quest`-tagged records span
items, clothing and weapons, and 95 of them are in `quest_items.tweak`
including iconic gear. A rule like "delete everything tagged `Quest`" would
delete wanted items. Use explicit record names only, never a rule.

### 2.5 Runtime redscript hooks that despawn on attach

There is **no general despawn API**. `Entity` (`refs/cyberpunk/core/entity/entity.swift:2-63`)
exposes `QueueEvent`, `GetEntityID`, transforms — no delete. The nearest things
are `PreventionSpawnSystem.RequestDespawn(EntityID)`
(`refs/cyberpunk/core/systems/preventionSpawnSystem.swift:52`, NCPD-only) and
`ReactionSystem.MarkDespawnCandidate` (`reactionComponent.swift:2596`, AI-only).

A redscript sweep would have to find entities by proximity every stream-in,
which is per-frame-adjacent work, cannot reach inside a Quest sector that was
never instantiated, and duplicates what a variant hide does for free.

**Verdict:** not recommended. The sanitizer doc already forbids per-frame world
scans.

### 2.6 Native RED4ext helpers

`world::IQuestPrefabStateListener` exists in the SDK but is an empty base struct
(confirmed in [`world-access.md`](world-access.md) §4.1 O5). Nothing here is
cheaper than a data fix.

### 2.7 Recommended layered plan

| Layer | Mechanism | Covers | Effort | Risk |
| --- | --- | --- | --- | --- |
| **L1** | Generated `add_variant_toggle_node(show=0)` group in `ascendancy.questphase`, emitted from the extracted phase corpus | Rank 1: bodies, loot bags, blood, container props (284 nodes in the measured set) | Low (spec + builder wiring) | Low |
| **L2** | Kept-phase hygiene: drop the `kabuki_vendors` loot inject; stop declaring story sub-prefabs that ship quest loot; extend the `forbidden_*` guard from `venue_phases.json` to `cast_and_hubs` | Rank 2 and 3 | Low | Low |
| **L3** | Explicit-record TweakXL only (named items, named `lootDrop`s) | Residual item-record leaks | Low | Medium (global scope if done as a rule) |
| **L4** | ArchiveXL `.xl` `nodeDeletions` on 2.5-generated indices, one entry per offending `worldEntityNode` | Rank 4: hand-placed story entities (`q001_police_holotape.ent`, `q003_gilchrist_corpse.ent`, …) | Medium | High (index brittleness) |

Everything in L1/L2 is **data driven and generated by a tool from the
extract**, as requested — not hand lists.

---

## 3. Safety: what must not be removed, and how to keep it reviewable

### 3.1 Never touch

| Must keep | Why | Guard |
| --- | --- | --- |
| `wa_*`, `mb_*`, `mba_*`, `wba_*`, `mf_*` corpse containers used by ambient/gang content | They are the *same templates* as quest corpses; only the instance and variant differ | Act on `(prefab, variant)` pairs, never on the `.ent` |
| Any variant already `enabledByDefault: 0` | It is already correct; a redundant `show = 0` is harmless but masks a bug if the pairing is wrong | Assert `default == 1` before emitting a hide |
| Vendor stock / `*_vendors.questphase` loot except the one known inject | Shops are the mod's economy | Allow-list of kept injects |
| `FastTravel*`, service-point, apartment, stash/wardrobe prefabs | City services | Reuse `venue_phases.json` `forbidden_device_controller_prefixes` idea |
| Non-quest junk loot (`base_junk_item`, `Items.Junk*`, `Price.Junk` records) | Real loot | Do not filter by template; filter by owning prefab |
| Playable/iconic items and `quest_clothing.tweak` gear | Design may want them | Owner decision; list explicitly, do not batch-delete |

### 3.2 The one dangerous assumption to encode

**`enabledByDefault == 1` does not mean "story leftover".** Measured: 379
`Exterior` variant entries with a body/loot name are default-on **without** a
quest token in their nodeRef, and 330 are default-on **with** one. Only the
second group is quest-owned. The reference (`ma_` / `sts_` / `mws_` /
`/mq` / `/sq`) is the discriminator, not the name. Sampling proved this
matters: `bodies` and `blood` names appear under ordinary city decoration
prefabs too.

### 3.3 Determinism and reviewability

The corpus is finite and small (494 phase resources). The generated spec
should be:

- sorted by `(prefab, variant)` for byte-stable output;
- annotated with the source phase path and the `show` value seen, so a reviewer
  can trace every line back to a vanilla resource;
- split into `hide_only` (230 pairs, always `show = 0`) and
  `state_dependent` (360 pairs, both `show = 0` and `show = 1`) — **emit only
  `hide_only`** in L1. A state-dependent variant is a gig *effect* (e.g. a
  scripted reveal); hiding it unconditionally could contradict a later state the
  design wants, and `show = 0` on a variant the game later shows is at best
  wasted work, at worst a visible flicker;
- checked by `build-clean-slate.py --check`, which already re-extracts the
  packed archive and compares resources. Add an assertion that every emitted
  hide targets a prefab that exists in the 2.5 block and that its
  `enabledByDefault` is 1.

### 3.4 Why L4 stays last

`nodeDeletions` needs `expectedNodes` for the sector, which changes with every
patch. The wiki documents an updater tool and eight failure statuses
(`exact`, `match`, `moved`, `by name`, `already target`, `other mod`,
`not found`, `source mismatch`) — i.e. the ecosystem already treats this as a
maintenance burden. In a mod that is rebuilt from `data/` on every release, a
hand-maintained index list is the wrong shape. If L4 is needed, generate it
from a fresh 2.5 extract each build and assert `expectedNodes`.

---

## 4. Tooling

### 4.1 What exists today

| Tool | What it yields | Gap for this task |
| --- | --- | --- |
| `tools/extract-world.py` | `dist/extract/raw/**/always_loaded_{0,1,2}.streamingsector(.json)`, mappins, POIs, markers | **Only the always_loaded sectors.** Confirmed: `dist/extract/raw` holds 10 files, 700 MB, and the three always_loaded sectors contain only `worldStaticMarkerNode` and `worldCompiledCommunityAreaNode` (5,731 / 6,216 / 3,561 nodes). **Zero** corpse, loot or quest-entity nodes. Clutter lives in ordinary `exterior_*` / `interior_*` sectors. |
| `tools/extract-sites.py` | `data/sites/*.json` (424 sites, 375 doors, 562 communities, 3,777 phase records) | Enumerates **Quest-category** sectors only, and only the ones bound to `ma_/sts_/mws_` phases. It does **not** read `Exterior`/`Interior` sectors, which is where the bodies are. |
| WolvenKit.CLI (`~/.cache/neon-ascendancy/wolvenkit-10.0.0-beta.1/`) | `extract`, `convert serialize/deserialize`, `pack` | Works. Measured throughput below. |

So the current extract is **the wrong three files**. This is the tooling gap.

### 4.2 Extraction needed to enumerate candidates city-wide

Two datasets, both cheap.

**(a) The phase corpus — the source of truth for what to hide.**

```bash
# 455 base resources + 39 EP1 resources
WK extract <game>/archive/pc/content/basegame_4_gamedata.archive -o phases/base \
  -r '^base\\open_world\\(minor_activities|street_stories|mini_world_stories)\\.*_(phase|openworld)\.questphase$'
WK extract <game>/archive/pc/ep1/ep1_2_gamedata.archive -o phases/ep1 \
  -r '^ep1\\openworld\\.*_(phase|openworld)\.questphase$'
WK convert serialize phases
```

Measured on this machine: **3.2 s** extract base (15 MB), **8 s** serialize
(140 MB JSON); EP1 39 resources in ~3 s. Total under **20 s**.

Then walk every `questTogglePrefabVariant_NodeType` and keep
`show == 0` with a quest-token prefab. Measured yield:

```text
939 variant-state writes total
590 distinct (prefab, variant) pairs with a show=0
306 of them body/loot-named
230 hide-only (never shown again)  <- the L1 emit set
360 state-dependent              <- skip; gig effects
  8 pairs from the EP1 corpus (bodies, corpses, final_loot, homeless_body,
                                loot_room, clues_blood)
```

**(b) The streaming block — to validate every prefab and get defaults.**

```bash
WK extract <game>/archive/pc/content/basegame_3_nightcity.archive -o blk -w "*all.streamingblock"
WK extract <game>/archive/pc/ep1/ep1_1_nightcity.archive -o blk2 -w "*streamingblock"
WK convert serialize blk blk2
```

One file, 23,718 descriptors, 37 MB JSON. Gives, per variant entry: `name`,
`enabledByDefault`, `nodeRef`, and the owning sector `DepotPath` +
`streamingBox`. Validated in this session: **258 of 334** body/loot pairs match
a real variant `nodeRef` in the base block (the rest are EP1 or carried by
phases that no longer exist). **[V]**

**(c) Optional — sector node census, to catch Shape B.**

Only needed for the always-on base-range nodes (the `q001_police_holotape` /
`q003_gilchrist_corpse` class). Narrow the extraction to the sectors that the
hide list does not already cover:

```bash
# 152 sectors with a default-on body/loot variant -> 1.4 GB JSON, 33 s
WK extract basegame_3_nightcity.archive -o allsec -r "$(cat /tmp/all.rx)"
WK convert serialize allsec
```

Measured: **152/152 extracted in 3.3 s**, converted in **27 s**, 1.4 GB on disk.
A full city sweep (all 17,546 Exterior+Interior descriptors) would be roughly
**115× that ≈ 160 GB of JSON** — not viable, and unnecessary: rank-1 clutter is
entirely inside the 152 sectors the block census already names.

**Do not** attempt a full `_compiled/default` sweep. Use the block to select
sectors, then extract only those.

### 4.3 Effort estimate

| Work | Shape | Effort |
| --- | --- | --- |
| Phase-corpus extraction + hide-list generator | New `tools/extract-quest-props.py` (or a mode on `extract-sites.py`), emitting `data/clean-slate/quest_prop_hides.json` | Small — the walk is ~40 lines over already-proven WolvenKit calls |
| Builder wiring | New always-on chain off the hub fan-out calling the existing `add_variant_toggle_node` | Small — mirrors `build_barricade_cleanup` |
| Block validation | Assert prefab exists + `enabledByDefault == 1` in `--check` | Small |
| Shape B node deletion (if wanted) | 2.5-generated `.xl` `nodeDeletions` | Medium, ongoing maintenance |
| TweakXL record patches | 1–3 named records | Small |

No new dependencies, no native code, no new framework.

---

## 5. Risks

1. **Boot-time toggle vs late streaming [H].** The hides are issued from H10 at
   boot; the target `Exterior` sector may not have streamed yet. This is the
   same blocking question `watson-lockdown-props.md` §7.1 raises for the bridge
   variants. If the toggle does not stick, the fallback already exists in the
   builder: `add_proximity_pause_node` (used by `venue_phases.json`), gating each
   hide behind a proximity pause on a nearby workspot/trigger ref. Budget for it.
2. **Hidden variant vs. lootable interaction [H].** Does `bodies = 0` remove the
   corpse entity, or leave an empty container? The measurement shows the corpse
   node lives *inside* the variant group (`grp=[0]` / `grp=[5]`), so hiding the
   group should remove the node. Needs one in-game confirmation, because a
   non-removed-but-invisible lootable would be worse than the status quo.
3. **`state_dependent` variants.** 360 pairs are both hidden and shown. Emitting
   only the 230 hide-only pairs is deliberately conservative; if the owner later
   sees remains after a specific gig, the fix is to add that gig's pair
   explicitly, not to flip the whole set.
4. **`cast_and_hubs` story prefabs.** Declaring `#q005_pr_afterlife` brought in
   `q005_loot_token.ent`. Other declared prefabs
   (`#pr_misty_default`, `#pr_judy_default`, `#pr_panam_default`,
   `#pr_sobchak_default`, `#pr_mama_welles_default`, `#pr_totentanz_bouncer_default`,
   …) were **not** audited node-by-node in this session. Add a `forbidden_*`
   assertion to the cast layer and audit each declared sector once.
5. **Vendor inject.** `kabuki_vendors.questphase` is in `kept_depot_phases` by
   explicit decision (its `why` mentions wiring it directly). Editing the phase
   means shipping a patched copy; the cheaper path is to drop that one item
   record via TweakXL or to stop the inject at the record level.
6. **ArchiveXL `nodeDeletions` fragility** if L4 is used: `expectedNodes`
   mismatch silently skips the sector, and an unreadable actor list removes the
   whole node. Assert, and log.
7. **Save safety.** L1/L2 are pure phase data; device/entity state is
   engine-owned and nothing new is persisted. L3 changes TweakDB globally. L4
   changes world content for everyone. Only L1/L2 are comfortably idempotent.

---

## 6. What needs an in-game check

| # | Check | Pass condition |
| --- | --- | --- |
| 1 | **Toggle persistence** — boot Ascendancy, then drive to `ma_hey_gle_05` (Glen, `-1730,-222`) and `ma_pac_cvi_09` (Coastview) | No corpse containers, no loot bags, no blood decals. If they appear, add `add_proximity_pause_node` and retest |
| 2 | **Interaction gone, not just invisible** — stand where a corpse was and scan/loot | No loot prompt. An invisible lootable is a fail |
| 3 | **Non-quest corpses intact** — kill a random gang member in the same district | Body and loot work; the hide did not touch ambient content |
| 4 | **Vendor stock clean** — open the Kabuki vendor that injects `sts_wat_kab_05_onscreen_001` | No quest shard in stock |
| 5 | **Afterlife** — enter Afterlife, look at Dexter's booth | No `q005_suit_cover_loot` token; Dexter seated |
| 6 | **q001 holotapes** — walk the old q001 bridge corridor | Either absent (L4 applied) or explicitly accepted |
| 7 | **Save/reload** — save in a cleaned area, reload, re-enter | No resurrection of the hidden variants |
| 8 | **No false positives** — sample a `bodies = 0` pair that L1 skips (a `state_dependent` one) | Behaviour unchanged from today, proving the hide-only filter is doing what it claims |

---

## 7. Bottom line

- **Sources ranked by clutter volume:** (1) default-on `bodies`/`body`/`final_loot`
  sector variants over `ma_`/`sts_`/`mws_` prefabs — 284 corpse nodes in 123 of
  152 sectors, and the gig/hustle phases that would have hidden them are
  deliberately omitted; (2) one vendor loot-inject of a gig shard;
  (3) story sub-prefabs declared by the cast layer (`#q005_pr_afterlife`) that
  ship quest loot; (4) hand-placed story entities in always-on base ranges
  (`q001_police_holotape.ent`, `q003_gilchrist_corpse.ent`).
- **Recommended layers:** L1 generated `questTogglePrefabVariant = 0` group in
  `ascendancy.questphase` (uses the existing `add_variant_toggle_node`), L2
  kept-phase and cast hygiene, L3 named-record TweakXL, L4 ArchiveXL
  `nodeDeletions` only as a last resort. No native code, no redscript despawn.
- **Tooling:** extract the 494 gig/hustle phase resources and the two
  `all.streamingblock` files (~20 s, ~180 MB), generate a sorted hide-only spec
  (230 pairs), and validate each prefab against the block. The existing
  `dist/extract/raw` always_loaded sectors contain no clutter and are the wrong
  base for this task.
- **Risks:** boot-vs-stream toggle timing (mitigation already in the builder),
  hide-vs-lootable semantics, the `state_dependent` 360 pairs, unaudited cast
  prefabs, and ArchiveXL index fragility.
- **In-game checks:** the eight-item table in §6; #1 and #2 are the blocking
  ones.

---

## Appendix A — reproduction commands

```bash
WK="$HOME/.cache/neon-ascendancy/wolvenkit-10.0.0-beta.1/WolvenKit.CLI"
GAME="$HOME/Games/Cyberpunk 2077"
S=/tmp/quest-prop-cleanup        # any scratch dir
export DOTNET_ROLL_FORWARD=Major

# 1. Streaming block (variant names, defaults, prefab refs) — 23,718 descriptors
"$WK" extract "$GAME/archive/pc/content/basegame_3_nightcity.archive" -o "$S/blk" -w "*all.streamingblock"
"$WK" extract "$GAME/archive/pc/ep1/ep1_1_nightcity.archive"        -o "$S/blk2" -w "*streamingblock"
"$WK" convert serialize "$S/blk" "$S/blk2"

# 2. The gig/hustle/mini-story phase corpus (the hides)
"$WK" extract "$GAME/archive/pc/content/basegame_4_gamedata.archive" -o "$S/phases/base" \
  -r '^base\\open_world\\(minor_activities|street_stories|mini_world_stories)\\.*_(phase|openworld)\.questphase$'
"$WK" extract "$GAME/archive/pc/ep1/ep1_2_gamedata.archive" -o "$S/phases/ep1" \
  -r '^ep1\\openworld\\.*_(phase|openworld)\.questphase$'
"$WK" convert serialize "$S/phases"

# 3. Optional: the 152 sectors with a default-on body/loot quest variant
#    (build the alternation from the block first)
"$WK" extract "$GAME/archive/pc/content/basegame_3_nightcity.archive" -o "$S/allsec" -r "$(cat /tmp/all.rx)"
"$WK" convert serialize "$S/allsec"

# 4. Kept-phase audit (what the archive actually runs)
"$WK" extract "$GAME/archive/pc/content/basegame_4_gamedata.archive" -o "$S/kept" -r "$(cat /tmp/kept.rx)"
"$WK" convert serialize "$S/kept"

# 5. Item records / loot tables (plain text, no WolvenKit needed)
TW="$GAME/tools/redmod/tweaks"
grep -rc '"Quest"'        "$TW/base/gameplay/static_data/database/items"      # 356 total
grep -rc 'BaseShard'      "$TW/base/gameplay/static_data/database/items"
grep -rc 'Gen_Keycard'    "$TW/base/gameplay/static_data/database/items/quest/keycards.tweak"
grep -rn  'itemID = "Items\.\(sts_\|ma_\|mws_\)' "$TW/base/gameplay/static_data/database/loot"   # 1,158
```

Census snippets (numbers quoted above):

- Variant census: for each descriptor in `all.streamingblock`, read
  `category`, `variants[].{name, enabledByDefault, nodeRef}`, and
  `data.DepotPath`. Count `(category, name)` pairs.
- Hide census: walk each phase JSON for
  `questTogglePrefabVariant_NodeType.params[].{prefabNodeRef, variantStates[]}`.
  Classify a pair `hide_only` when every observation is `show: 0`.
- Node census: for a sector, map `variantNodes[gi][].nodeIdx` to node indices,
  then read `nodes[i].Data.{ $type, debugName, appearanceName, entityTemplate.DepotPath }`.

Key citations:

- `data/clean-slate/clean_slate_spec.json:137-179` — `omitted_depot_phases`,
  `excluded_phase_patterns` (why the hides never run).
- `data/clean-slate/clean_slate_spec.json:64-111` — `kept_depot_phases`
  (the vendor phases, including `kabuki_vendors.questphase`).
- `data/clean-slate/cast_and_hubs.json` `phase_prefabs` — the declared story
  prefabs, including `#q005_pr_afterlife`.
- `data/clean-slate/venue_phases.json` `forbidden_phase_patterns`,
  `forbidden_device_controller_prefixes` — the guard to extend to the cast
  layer.
- `tools/build-clean-slate.py:687` `add_variant_toggle_node`;
  `:530` `add_community_spawn_node`; `:371` `add_proximity_pause_node`;
  `:1281-1320` `build_barricade_cleanup` (the shape to mirror).
- `refs/cyberpunk/core/entity/entity.swift:2-63` — no despawn surface.
- `refs/cyberpunk/core/systems/preventionSpawnSystem.swift:52` —
  `RequestDespawn`, NCPD-only.
- `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/items/quest/quest_items.tweak:499`
  — `q105_evelyns_handbag` (no `tags` array).
- `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/items/misc/readables.tweak:24`
  — `BaseShard`.
- `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/items/quest/keycards.tweak`
  — `ItemType.Gen_Keycard`.
- `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/loot/item_pass_loot_tables.tweak`
  — `ItemPass_Shard*`, 1,158 gig-item loot entries.

External:

- [ArchiveXL — removing objects (`.xl` `nodeDeletions` / `nodeMutations`)](https://wiki.redmodding.org/cyberpunk-2077-modding/modding-guides/world-editing/removing-objects)
- [ArchiveXL — updating `.xl` files for a new game version (2.5 renumbering)](https://wiki.redmodding.org/cyberpunk-2077-modding/modding-guides/world-editing/removing-objects/updating-.xl-files-for-a-new-game-version)
- [ArchiveXL wiki (loader config, resource merging)](https://github.com/psiberx/cp2077-archive-xl/wiki)
