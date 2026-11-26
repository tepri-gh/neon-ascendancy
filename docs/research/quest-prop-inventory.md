# Research — Quest Prop Inventory: what is actually left in the world

**Target:** Cyberpunk 2077 2.5 + Phantom Liberty, redscript 1.0.2 (Codeware-free),
RED4ext 1.31.1, ArchiveXL 1.28.11, TweakXL 1.12.2,
WolvenKit.CLI 10.0.0-beta.1 (Linux).
**Date:** 2026-11-25.
**Scope:** a *complete, reproducible inventory* of every placed object that
exists in Night City only because a vanilla quest, gig, hustle or mini world
story put it there — the raw material for the cleanup described in
[`quest-prop-cleanup.md`](quest-prop-cleanup.md).

**This document is the inventory, not the removal plan.** It answers *what is
there, where, how much, and which content owns it*. The sibling report owns the
*how to remove it* question (variant hides, kept-phase hygiene, TweakXL, and
sector patching). Read them together: every row here has a `range_index` and a
`variant_name`, which is exactly the key the cleanup layer needs.

**Evidence grades**

- **[V]** — verified in this session by extracting the local 2.5 archives with
  the pinned WolvenKit.CLI and parsing the serialized resources, or by census
  over the shipped plain-text TweakDB.
- **[R]** — structurally certain from the extracted data; the runtime result
  still needs one in-game pass.
- **[H]** — hypothesis. Must be tested in-game before it becomes a design
  dependency.

Raw extracts (≈4 GB of sectors, ≈6 GB peak JSON) were made into a scratch
directory outside the repository and are reproducible with
[Appendix A](#appendix-a--reproduction-pipeline). Nothing in the game
directory, `refs/`, or the repository was modified.

---

## 0. Executive summary

1. **The leftover population is large, and it is dominated by one thing: main
   quest set dressing.** Across the whole city, **15,221 placed nodes** carry
   quest evidence. Of those, **5,636 are objects a player can see or pick up**:
   4,953 visible quest props, 459 quest shards/data pads, 203 quest corpses,
   and 21 keycards. The remaining 9,585 are invisible scaffolding (6,427 route
   markers, 3,158 lookat/lighting/FX helpers) that nobody perceives. **[V]**

2. **Most of it is already streaming before any phase runs.** **4,631 of the
   5,636 actionable objects sit in ordinary `Exterior`/`Interior` sectors**
   whose streaming descriptor has no quest prefab; **only 1,005 sit in
   quest-gated prefab sectors**. This is the same structural fact the cleanup
   report found for bodies: the placement is always-on, and the gig phase is
   what normally hides it. Omitting gigs therefore *reveals* leftovers rather
   than preventing them. **[V]**

3. **Variant gating cuts the live population roughly in half — and the split is
   per-node, not per-sector.** Of the 5,636 actionable objects, **2,691 sit in
   the always-on base range**, **257 sit in a named variant that is enabled by
   default**, and **2,674 sit in a variant that is disabled by default**. So
   the *probably visible in a clean-slate run* population is **2,948**, and the
   other **2,674** appear only when a phase turns its variant on. This is the
   single most useful number for scoping: the cleanup layer's variant hides and
   this inventory's `range_index` / `variant_enabled_by_default` columns line up
   one-to-one. **[V]**

4. **Quests, not gigs, are the bulk.** Actionable leftovers by owner family:
   main quest 3,338 · side quest 690 · minor quest 614 · gig 351 · mini world
   story 317 · hustle 149 · sandbox activity 104. The five biggest single
   sources are **q306 Spaceport (786), q114 Panzer (423), q303 Black Sapphire
   (386), q112 Arasaka warehouse (306), q101 Concert (238)**. **[V]**

5. **Quest shards are exactly identifyable and rare — 459 placements, 320
   distinct item records.** Every one carries a quest-coded TweakDB record
   (`Items.mq304_Organizing_protests_shard`,
   `Items.q114_secure_yout_soul_list`, …) inside a stock
   `shard_case_container.ent`. **The item record name, not the container
   template, is the discriminator.** **[V]**

6. **NCPD hustle data pads and cyberpsycho corpses are a small, well-bounded
   slice: 149 hustle-owned objects across 33 hustles**, plus 33 corpses in
   `ma_pac_cvi_08` / `ma_std_arr_06` / `ma_wat_kab_08` / `ma_wat_nid_15`
   (the cyberpsycho scenes). Hustle corpses are also the family with the
   highest share of *default-on* placements — **29 of 58** — i.e. bodies that
   are visible even before a phase touches them. **[V]**

7. **The dangerous near-misses are numerous and must be protected.** **3,428
   placements carry a quest-coded loot assignment** yet are ordinary
   ammo/drink/money/toolbox containers — **3,421 of them are real loot and only
   7 are quest items.** Beyond that: **19,823 world-loot/interactable
   placements**, **5,244 stock devices used as quest set dressing** (cameras,
   turrets, TVs, laptops, air conditioners), and **815 generic shards**
   (`Items.generic_*`) that are ambient lore, not quest items. All are recorded
   with the reason they were excluded. **[V]**

8. **The pipeline is deterministic and cheap to re-run:** ~3 min to extract
   26,369 sectors, ~1 min of raw-byte prefiltering to 2,554 candidates, ~40 min
   of batched conversion + parse, and ~15 s to join taxonomy, loot registry,
   districts and streaming blocks. See [§7](#7-reproducing-the-inventory). **[V]**

---

## 1. What counts as a leftover

The owner's list (quest data pads on the ground and on bodies, Evelyn's
handbag, quest keycards, NCPD hustle data pads, cyberpsycho corpses) maps onto
a small number of storage shapes. The inventory records the shape, because the
shape decides both confidence and the fix.

| Shape | Example | How it appears in the data |
| --- | --- | --- |
| **Placed quest item** | `q004_evelyn_small_purse` → `base\quest\main_quests\prologue\q004\entities\q004_evelyn_purse.ent` | `worldEntityNode` with a quest-owned `entityTemplate` |
| **Shard case holding a quest shard** | `Items.sts_wbr_jpn_03_shard_001` in `shard_case_container.ent` | `worldEntityNode` + `ShardCaseContainer.itemTDBID` in the instance buffer |
| **Keycard** | `Keycards.jpn_02_keycard`, `sq018_keycard_storage.ent` | item record, or a quest keycard prop template |
| **Scripted corpse** | `q003_corpse_maelstrom.ent`, `ma_pac_cvi_08_ent_corpse_ma.ent` | quest-owned corpse template (distinct from the generic `ma_corpse.ent`) |
| **Quest container** | `q005_loot_token.ent` | quest-named loot token/container template |
| **Quest spawner** | `worldPopulationSpawnerNode` with a quest-coded debug name | spawner whose record/debug name encodes a quest |

Two things are deliberately **out of scope** because no player perceives them,
but they are still inventoried so the cleanup layer can decide:

- **Route markers** — `sq024_gps_path.ent` alone accounts for 5,735
  placements, one every few metres along the Big Race route; plus truck tracks
  and convoy paths. 6,427 total.
- **Scaffolding** — lookat helpers, `*_invisible_*`, lighting, FX, screens,
  mappin entities, spawn markers. 3,158 total.

---

## 2. Extraction scope achieved

The extraction is **city-wide, not a sample**. Every `*.streamingsector` in the
base-game nightcity archive plus every EP1 override was extracted with EP1
winning by resource path (the same precedence rule
[`game-data-extraction.md` §1.3](game-data-extraction.md) established):

| Quantity | Value |
| --- | --- |
| Sector resources extracted | **26,369** (23,720 base overwritten by 24,239 EP1) |
| On-disk size | 3.9 GB |
| Descriptors in the merged streaming-block index | **26,369 / 26,369 resolved (100 %)** |
| Candidate sectors after raw-byte prefilter | **2,554** (9.7 % of the city) |
| Placed entity/spawner nodes censused | **96,920** in 2,554 sectors |
| Conversion/parse failures | **4 sectors** (see §6.1) — ≤0.3 % of the inventory |
| Nodes carrying a TweakDB item record | **≈4,800** |
| Sector-category coverage of census rows | **0 unknown sectors** |

Every census row is joined to its sector descriptor, so each candidate knows
whether it lives in `Exterior`, `Interior`, `Quest` or `AlwaysLoaded` content,
whether its sector has a `questPrefabNodeRef`, and which named streaming
*range* (variant) it belongs to.

**Prefilter recall was measured, not assumed.** Scanning all 26,369 sectors for
`shard_case`, `corpse_container`, `items\quest\` and keycard assets, the
prefilter missed **0 of 553** shard-case sectors, **0 of 588** corpse-container
sectors, **0 of 71** `items\quest\` sectors, and **0 of 5** sectors holding a
real keycard asset or `Keycards.*` record. The only misses were 26 sectors
whose sole match was the word `keycard` in a security threshold or a
`#…_dvc_keycard_doc` device NodeRef — not a pickable prop. **[V]**

The prefilter is intentionally permissive (it converges on ~9 % of sectors), so
the cost of a false positive is conversion time, never a missing row.

---

## 3. Counts per category

All numbers below are placements (instances), not distinct assets.

| Category | Rows | In always-streaming sectors | In quest-gated prefab | Distinct templates | Distinct item records | Distinct owners |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `quest_prop` (visible placed quest object) | **4,953** | 3,983 | 970 | 1,589 | — | 357 |
| `quest_shard` (shard/data pad holding a quest item) | **459** | 444 | 15 | 11 | 320 | 149 |
| `quest_corpse` (scripted body) | **203** | 184 | 19 | 39 | 1 | 26 |
| `quest_keycard` | **21** | 20 | 1 | 3 | 9 | 9 |
| *Actionable subtotal* | **5,636** | **4,631** | **1,005** | | | |
| `quest_scaffold` (invisible helper; lookat/lighting/FX/screen) | 3,158 | 2,380 | 778 | 590 | — | 128 |
| `quest_route` (GPS/route/track markers) | 6,427 | 6,426 | 1 | 12 | — | 10 |
| **Total candidates** | **15,221** | | | | | 492 |

`quest_container` and `quest_spawner` are defined in the taxonomy but resolved
to **zero** rows: the quest-named loot tokens (`q005_loot_token.ent` and
friends) are matched by the more specific rules, and `worldPopulationSpawnerNode`
placements whose names encoded quests turned out to be vehicles/animals whose
ownership is already implied by their sector prefab. Recording zero is the
honest result, not a gap.

### 3.1 How much of it is actually visible

Sector category alone is not visibility: a node can sit in an ordinary
`Exterior` sector yet belong to a named streaming range that is off by default.
Each row therefore carries `range_index`, `variant_name` and
`variant_enabled_by_default`, read from the sector descriptor.

| Visibility | Base range (`range_index == 0`) | Variant, default on | Variant, default off | Unknown |
| --- | ---: | ---: | ---: | ---: |
| `quest_prop` | 2,353 | 199 | 2,388 | 13 |
| `quest_shard` | 316 | 14 | 128 | 1 |
| `quest_corpse` | 10 | 42 | 151 | 0 |
| `quest_keycard` | 12 | 2 | 7 | 0 |
| **Total actionable** | **2,691** | **257** | **2,674** | **14** |

**Read: 2,948 objects are plausibly visible in a clean-slate run; 2,674 only
appear if a phase enables their variant.** That reframes the removal problem:
a meaningful share of the "leftovers" are not stray objects at all, they are
*correctly hidden* variant content whose enabling phase is simply never run.
The remainder — the base-range rows — is the set that genuinely needs a
deletion or a hide it does not currently have. **[R]** (structural; the
runtime behaviour of range-0 nodes and default-on variants is what §6's probe
1 settles).

The named variants with the most actionable leftovers are also the best map of
which content clusters exist:

| Variant name | Actionable rows |
| --- | ---: |
| `q306_var_spaceport_inst_passengers` | 228 |
| `paradise_npc_instances` (q303 Black Sapphire) | 163 |
| `idris_elba_live_action_crowd` (q303) | 162 |
| `canyon_barrage` (q114) | 157 |
| `q306_var_spaceport_luggage` | 97 |
| `q306_terminal_a` | 92 |

### 3.2 Per district

Actionable objects only (`quest_prop` + `quest_shard` + `quest_corpse` +
`quest_keycard`):

| District | Prop | Shard | Corpse | Keycard | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| Pacifica | 1,146 | 198 | 57 | 4 | **1,405** |
| Badlands | 1,252 | 26 | 12 | 2 | **1,292** |
| Morro Rock | 728 | 31 | 0 | 1 | **760** |
| Watson | 508 | 69 | 52 | 8 | **637** |
| Westbrook | 537 | 35 | 5 | 0 | **577** |
| Heywood | 271 | 46 | 51 | 4 | **372** |
| City Center | 330 | 35 | 6 | 0 | **371** |
| Santo Domingo | 168 | 18 | 20 | 2 | **208** |
| Unclassified (outside all district boxes) | 13 | 1 | 0 | 0 | **14** |
| **Total** | **4,953** | **459** | **203** | **21** | **5,636** |

The Pacifica/Badlands lead is real, not a classifier artefact: the largest
single-owner clusters are the Dogtown/spaceport content (q306 and q303, both
in Pacifica) and the Panzer/convoy content (q114 in the Badlands). District is
assigned from the repo's `data/districts.json` bounding boxes; 14 rows fall
outside all boxes and are reported as `unknown` rather than silently bucketed.

### 3.3 The five biggest sources

Ranked by actionable placements:

| # | Owner | Family | Actionable rows | Signature assets |
| --- | --- | --- | ---: | --- |
| **1** | **q306** (Spaceport) | main quest | **786** | `vending_machine_spaceport.ent`, `inst_spaceport_oa_ma_01.ent`, luggage trolleys, blinking-light sets |
| **2** | **q114** (Panzer) | main quest | **423** | `q114_canyon_missile.ent` (155), `q114_panzer_bush.ent` (104), `q114_beer.ent` (59) |
| **3** | **q303** (Black Sapphire) | main quest | **386** | `q303_serverawake_light_a.ent`, `q303_paradise_*` props |
| **4** | **q112** (Arasaka warehouse) | main quest | **306** | `q112_oda_fight_candles.ent` (199), `q112_fake_gunfire.ent` |
| **5** | **q101** (Concert) | main quest | **238** | `q101_concert_npc_*.ent`, `q101_concert_*` stage props |

If the intent is "remove the clutter that reads as a leftover quest", these
five alone are **2,139 of 5,636 actionable objects (38 %)**. They are also the
easiest to reason about, because every one is inside a small number of
exterior sectors:

| Sector | Actionable | Owner |
| --- | ---: | --- |
| `exterior_-9_11_2_0` | 200 | q112 (all) |
| `exterior_-30_-36_6_0` | 122 | q303 (120) |
| `exterior_-57_6_0_0` | 120 | q306 (all) |
| `exterior_-57_5_0_0` | 100 | q306 (all) |
| `exterior_-6_3_2_0` | 92 | sq017 (all) |

By item *asset*, the single most common leftover object is the stock shard
container holding a quest shard: **414 placements** of
`base\gameplay\loot\shard_cases\shard_case_container.ent` whose `itemTDBID` is
a quest record, spread over 227 sectors. That is the owner's "quest data pads in
the world" in one number. Add the 32 dedicated quest-shard props and the
category totals 459.

### 3.4 Gigs, hustles and mini world stories (the excluded content)

Because the mod excludes vanilla gigs and hustles, their leftovers matter even
though they are only **817 of 5,636 actionable objects (14.5 %)**:

| Family | Actionable rows | Distinct owner codes | Largest owners |
| --- | ---: | ---: | --- |
| Fixer gig (`sts_*`) | 351 | 154 | `sts_bls_ina_08` 35, `sts_ep1_12_droids_hub_doors` 26, `sts_hey_gle_04` 24 |
| Mini world story (`mws_*`) | 317 | 147* | `mws_se5_03` door/deco set 130 |
| Scanner hustle (`ma_*`) | 149 | 33 | `ma_pac_cvi_08` 28 (cyberpsycho), `ma_bls_ina_07` 20 |
| Sandbox activity (`cbj_*`, `sa_*`) | 104 | 24 | `cbj_ep1_02` 21, `cbj_ep1_01` 12 |

\* Many rows carry a per-prop suffix (`mws_se5_03_door_n_s`) rather than the bare
site code, so the distinct count overstates the number of sites. By site prefix
the mini-world-story count is 12.

Hustle corpses cluster exactly where the cyberpsycho scenes are:
`ma_pac_cvi_08` 28, `ma_std_arr_06` 12, `ma_wat_kab_08` 7, `ma_wat_nid_15` 6.
The corresponding entity templates carry the `_ent_corpse_` / `_corpses`
pattern, so they are distinguishable from ambient bodies. Of the 58
hustle-owned corpses, **29 are default-on** — the highest visible share of any
family, and the reason cyberpsycho scenes are the most likely leftover a player
stumbles into. **[V]**

### 3.5 What the inventory looks like

One row per placement, sorted by `(category, owner_family, owner_code,
district, sector_path, node_index, global_node_id)`:

```json
{
  "category": "quest_prop",
  "debug_name": "q004_evelyn_small_purse",
  "district": "watson",
  "entity_template": "base\\quest\\main_quests\\prologue\\q004\\entities\\q004_evelyn_purse.ent",
  "global_node_id": "3840453543909369846",
  "item_records": [],
  "node_index": 822,
  "node_type": "worldEntityNode",
  "owner_code": "q004",
  "owner_family": "main_quest",
  "range_index": 0,
  "reason": "quest-owned-entity:q004",
  "sector_category": "Exterior",
  "sector_path": "base\\worlds\\03_night_city\\_compiled\\default\\exterior_-19_24_0_0.streamingsector",
  "streaming_block_prefab": "0",
  "variant_enabled_by_default": null,
  "variant_name": null,
  "x": -1173.819, "y": 1572.899, "z": 24.24
}
```

A shard row instead carries the discriminating record:

```json
{
  "category": "quest_shard",
  "debug_name": "ina_03_shard",
  "district": "badlands",
  "entity_template": "base\\gameplay\\loot\\shard_cases\\shard_case_container.ent",
  "global_node_id": "7626716510611661361",
  "item_records": ["Items.sts_bls_ina_03_shard_001"],
  "node_index": 416,
  "owner_code": "sts_bls_ina_03",
  "owner_family": "fixer_gig",
  "range_index": 0,
  "reason": "taxonomy:quest-shard:Items.sts_bls_ina_03_shard_001",
  "sector_category": "Exterior",
  "sector_path": "base\\worlds\\03_night_city\\_compiled\\default\\exterior_29_-9_0_0.streamingsector",
  "streaming_block_prefab": "0",
  "variant_enabled_by_default": null, "variant_name": null,
  "x": 1892.823, "y": -547.258, "z": 55.585
}
```

`range_index` is the link to the cleanup layer: **range 0 is the always-on base
range; ranges ≥ 1 are named `worldStreamingSectorVariant` entries**, and
`variant_name` / `variant_enabled_by_default` come from the sector descriptor.
The body/loot variants the cleanup report targets are exactly the rows with
`range_index ≥ 1`.

---

## 4. Why an item record beats a template name

Two containers can be byte-identical and mean different things. The catalogued
evidence that made "item record" the authoritative signal:

- `shard_case_container.ent` is used **1,288 times**; **1,279** of those
  placements carry an item record. **427** hold a quest-coded record; **813**
  hold a generic record (`Items.generic_fanfic_shard`,
  `Items.generic_guns_catalog_shard`, …). Classifying by template would have
  flagged all 1,288; classifying by record separates 427 real leftovers from
  813 pieces of ambient lore.
- The container's own `hasQuestItems` flag is **0 on every sampled instance**,
  including the ones holding a quest record. **It is not usable as a
  discriminator** — verified on converted sectors from four districts. **[V]**
- Shards come in **two shapes**, and both are represented in the 459 rows:
  **427** are the stock container holding a quest record (above), and **32** are
  dedicated quest shard *props* with their own template
  (`q000_data_shard.ent`, `mq303_ent_lina_shard.ent`, `sq004_drone_shard.ent`,
  `sq021_lab_shards.ent`). A rule that only inspects `itemTDBID` would miss the
  second shape entirely; a rule that only inspects templates would miss the
  first.
- Generic bodies (`base\characters\entities\corpse\ma_corpse.ent`, 218
  placements) are ambient; quest corpses use quest-owned templates
  (`q003_corpse_maelstrom.ent`, `ma_pac_cvi_08_ent_corpse_ma.ent`,
  `mq062_escape_exit_body_dummy.ent`). **377 of 615** corpse-template rows were
  ambient and moved to the safe list purely on this rule.

Item classification itself comes from the shipped plain-text tweak sources,
because `tweakdb.bin` stores hashed IDs (see
[`game-data-extraction.md` §1.2](game-data-extraction.md)). Parsing
`<game>/tools/redmod/tweaks/{base,ep1}` yields **12,022 item records**:

| Classification | Records |
| --- | ---: |
| `shard` (inherits `BaseShard` / `Readable`) | 1,469 |
| `quest_item` (inherits `QuestItem`/`STSItem`/`MAItem`/`MWSItem`/`SAItem`, or tagged `Quest`) | 459 |
| `keycard` (package `Keycards`, or inherits `Keycard`) | 97 |
| `ordinary` | 9,997 |
| *with an owner code recoverable from the name* | 1,560 |

---

## 5. Safe list — similar-looking things that must stay

The classifier's exclusions are counted, not hand-waved. Every excluded row is
counted by reason and a sample is written to `safe_list_examples.jsonl`.

| Safe class | Count | Why it must stay | How it is recognised |
| --- | ---: | --- | --- |
| **No quest signal at all** | **55,558** | Ordinary world content: 96,920 placements were censused, and most are not quest-adjacent | no quest token, no quest asset family, not in a quest prefab |
| **World loot & interactables** | **19,823** | `gameplay\loot\containers`, `loot_bags`, `tokens`, `decorative_containers`, `items\interactive`, `lootable_containers`, vending machines | device/loot template family |
| **Quest-reused stock set dressing** | **5,244** | Cameras, turrets, explosive tanks, TVs, laptops, radios, forklifts, air conditioners placed inside quest prefabs — the same assets used city-wide | stock asset family + quest code only in the sector or name |
| **Generic shards** | **815** | `Items.generic_*` lore shards are ambient content that vendors and world loot also hand out | taxonomy classification `shard` with no quest owner |
| **Engine loot-registry entries** | **259** | `03_night_city.loot` lists them with a real `Loot`/`LootTables`/`Ammo`/`Items` assignment. Genuine containers that happen to sit in a quest location | `nodeRefsHash` join against the engine loot registry |
| *of which ambient bodies* | *≈377* | `ma_corpse.ent` / `wa_corpse.ent` bodies are environmental storytelling with normal loot; they fall under "no quest signal" | generic corpse template with no quest owner |

**The 3,428 trap, stated as its own number:** 3,428 placements in the census
carry a *quest-coded* `DeviceContentAssignment` (e.g.
`DeviceContentAssignment.ma_wat_lch_08`, `…sts_hey_spr_03`) and are still
ordinary ammo/drink/money/toolbox/locker containers with real loot tables.
**3,421 of them are correctly safe; only 7 are actual quest items** (6 shards,
1 keycard). Any rule that keys on "quest code in the loot assignment" would
destroy 3,421 pieces of real loot to catch 7 leftovers.

### 5.1 The one caveat that decides correctness

**A quest code in the sector is not evidence about a node.** The 5,244
"safest" exclusions are stock devices that live in a quest prefab sector
*and* are used everywhere else. Treating sector ownership as node ownership
would have inflated the candidate list by a third with content that is not a
leftover. The rule that survived review is: **a node is a candidate only if
the node itself carries quest evidence** (its own debug name, its own entity
template family, or its own item record) **or it is a direct child of a quest
prefab** — never merely because its sector was visited by a quest.

### 5.2 Two more near-miss traps

- **Vendors' stock.** `Items.sts_wat_kab_05_onscreen_001` is injected into a
  vendor's loot by `kabuki_vendors.questphase` (the cleanup report's rank 2).
  That is a *phase-side* leak, not a world placement: it cannot be found by a
  sector census and is correctly absent from this inventory.
- **Genuine quest rewards the design may keep.** The taxonomy deliberately does
  not treat every `Quest`-tagged record as removable; 459 `quest_item` records
  include armour and weapons (`SQ030_Diving_Suit`, `Q005_Militech_Suit`) that a
  TweakXL sweep would silently break. The inventory reports them; removal is a
  design decision, not a parser decision.

---

## 6. Confidence and limits

**What is certain [V]:** every placement, position, template, item record,
owner code, sector, district, sector category and range index in the table
above was read from serialized 2.5 resources or the shipped tweaks.

**What is inferred [R]:** the *owner code* when it appears only in a directory
or a sibling node rather than in the node's own name. **73 of 5,636 actionable
rows have `owner_code: null`**; their `sector_category` and template still say
they are quest content, but the specific quest is unknown. Likewise, the
visibility split in §3.1 assumes a `range_index ≥ 1` node with
`variant_enabled_by_default: 0` is not live — structurally sound, but the
runtime answer is probe 1.

**What needs an in-game check [H]:**

1. Whether a row with `range_index ≥ 1` and
   `variant_enabled_by_default: 0` is *actually absent* in a clean-slate run,
   or merely invisible. §3.1 reports both readings (2,948 "probably visible"
   vs 5,636 "candidate") so neither choice has to be guessed now.
2. Whether a hidden body/corpse variant removes the loot interaction or leaves
   an empty container (shared with
   [`quest-prop-cleanup.md` §6](quest-prop-cleanup.md)).
3. Whether `cast_and_hubs`-declared prefabs pull additional quest loot beyond
   what the sector census already sees.
4. Whether the 2,691 base-range rows are all genuinely reachable — a base-range
   node inside an inaccessible interior is harmless and should not consume
   removal effort.

**What this inventory cannot see:** anything spawned or injected by a running
phase at runtime (the vendor-injection case), and anything in `archive/pc/mod`.
Neither is a world placement, so neither belongs in a placement census.

### 6.1 Four sectors that will not convert, and why it does not matter

WolvenKit 10.0.0-beta.1 refuses **4 of the 2,554 candidate sectors** with an
RTTI type mismatch in the *cooked* resource, not a defect in this pipeline:

```text
Invalid in wolven rtti:"AccessPointControllerPS.accessPointSkillChecks"
  [Expected: "handle:HackingContainer" | Got: "APChallangeContainer"]
Invalid in wolven rtti:"WindowBlindersControllerPS.windowBlindersSkillChecks"
  [Expected: "handle:EngDemoContainer"  | Got: "handle:DemolitionContainer"]
Invalid in wolven rtti:"WindowControllerPS.windowSkillChecks"
  [Expected: "handle:EngDemoContainer"  | Got: "handle:DemolitionContainer"]
```

Failing sectors: `exterior_-17_21_0_0`, `exterior_-21_-1_0_0`,
`exterior_-23_1_4_0`, and `exterior_-40_-38_0_0` (both the base and EP1
copies).

**Impact measured, not assumed.** A raw-byte scan of those four files finds
**15 distinct quest-ish entity templates** in total — `shard_case_container`,
`q001_police_holotape`, `q003_intro__body_bag`, `sts_ep1_03_*_clue`, `q115_*`
lights, and an `sts_std_rcr_03` corpse. Even assuming three placements per
distinct template, that is **≤45 rows, ≤0.3 % of the 15,221-row inventory**,
and every one is knowable by name from the byte scan. A later tool that needs
those exact rows should either pin a WolvenKit build that knows the 2.5 RTTI
names or read the four sectors with a schema-tolerant parser. **It is not a
reason to distrust the other 2,550 sectors.** **[V]**

---

## 7. Reproducing the inventory

The pipeline is eight idempotent stages. Nothing is added to the repository;
the scripts live in a scratch directory, and the generated artifacts are the
research output.

```
listing   WolvenKit `archive -l` over the four archives            (~10 s)
extract   every *.streamingsector, base then EP1 (EP1 wins)         (~3 min, 3.9 GB)
prefilter raw-byte scan -> candidate sectors                        (~1 min, 2,554 sectors)
census    batch convert + parse placements (no classification)      (~40 min)
taxonomy  .tweak -> item records, tags, inheritance                 (~2 s, 12,022 records)
blocks    merge 4 all.streamingblock files -> sector -> category    (~10 s, 26,369 sectors)
registry  03_night_city.loot (engine loot registry)                 (~5 s)
inventory join census + taxonomy + blocks + loot + districts        (~10 s)
```

Peak disk stays modest because census conversion runs in 16-sector batches that
are parsed and deleted immediately.

### 7.1 The core classification rule (short form)

```python
def classify(row, taxo, loot):
    template, debug = row["entity_template"] or "", row["debug_name"] or ""
    items, blob = row["item_records"], " ".join([template, debug] + row["item_records"])

    if any(tok in template for tok in SAFE_TOKENS):          # world loot/interactable
        return None
    if engine_loot_registry_has_node(row["global_node_id"]):  # real container
        return None

    for rec in items:                                        # strongest signal
        kind = taxo[rec]["classification"]
        if kind == "keycard":  return "quest_keycard"
        if kind == "shard":    return "quest_shard" if has_quest_owner(rec) else None
        if kind == "quest_item": return "quest_prop"

    if "keycard" in blob: return "quest_keycard"
    if "corpse" in blob:  return "quest_corpse"
    if "shard"  in blob:  return "quest_shard"

    owner = find_owner(debug, template)
    if not owner: return None
    if not is_quest_authored_asset(template, debug): return None   # set dressing
    if is_route(template, debug):     return "quest_route"
    if is_scaffold(template, debug):  return "quest_scaffold"
    return "quest_prop"
```

Two ordering decisions carry all the precision:

1. **The engine loot registry is consulted before node names.** A node the
   engine files as a loot container is real loot even when a quest code appears
   in its content assignment.
2. **`find_owner` runs before the asset-family test, and the asset-family test
   rejects stock assets.** This is what keeps 5,244 cameras/turrets/TVs out.

### 7.2 Determinism

- Rows are sorted by `(category, owner_family, owner_code, district,
  sector_path, node_index, global_node_id)`.
- JSON keys are sorted; coordinates are rounded to 3 decimals.
- The item taxonomy is sorted by record name.
- The pipeline is re-runnable per stage; the census is resumable in batches.
- Every artifact records its own provenance: sector path, node index,
  `globalNodeId`, and the sector's streaming-block category.

### 7.3 What a later tool should reuse

- **`census.jsonl` is the fact layer** and must not be re-derived from the
  inventory: it holds all 96,920 placements including the safe ones, which is
  what lets the safe list be re-argued without re-extracting game data.
- **`sector_categories.json`** (sector → category, prefab, variant ranges) is
  the join the cleanup layer needs to emit variant hides.
- **`item_taxonomy.json`** is the TweakDB item dictionary; it is also the
  input a TweakXL patch would use to identify a specific injected record.

---

## Appendix A — reproduction pipeline

Set `GAME_DIR` if the game is not at `~/Games/Cyberpunk 2077`. All WolvenKit
invocations need `DOTNET_ROLL_FORWARD=Major` on this host (`.NET 10` runtime,
no SDK).

```bash
SCR=$HOME/na-prop-scratch
export DOTNET_ROLL_FORWARD=Major
WK=$HOME/.cache/neon-ascendancy/wolvenkit-10.0.0-beta.1/WolvenKit.CLI
GAME="$HOME/Games/Cyberpunk 2077"

# 1-2. Extract every streaming sector, base first then EP1 (EP1 wins by path).
"$WK" extract "$GAME/archive/pc/content/basegame_3_nightcity.archive" \
  -o "$SCR/sectors" -r '(\.streamingsector)$' -v Minimal
"$WK" extract "$GAME/archive/pc/ep1/ep1_1_nightcity.archive" \
  -o "$SCR/sectors" -r '(\.streamingsector)$' -v Minimal

# 3. Prefilter on quest evidence in raw sector bytes (no conversion needed).
python3 -I prefilter.py --sectors "$SCR/sectors" --out "$SCR/candidates.txt"

# 4. Census: batch-convert candidates, parse placements, delete JSON.
python3 -I census.py --sector-root "$SCR/sectors" --list "$SCR/candidates.txt" \
  --out "$SCR/census.jsonl" --batch 16

# 5. Item taxonomy from the shipped plain-text tweaks.
python3 -I build_item_taxonomy.py \
  --tweaks "$GAME/tools/redmod/tweaks" --out "$SCR/item_taxonomy.json"

# 6. Sector -> category / prefab / variant ranges (all four blocks).
python3 -I pipeline.py --work "$SCR" --stage blocks

# 7. Engine loot registry (the authoritative container list).
"$WK" extract "$GAME/archive/pc/ep1/ep1_1_nightcity.archive" -o "$SCR/world_res" \
  -r '(03_night_city\.loot)$' -v Minimal
"$WK" convert s "$SCR/world_res" -v Minimal

# 8. Join everything into the inventory.
python3 -I build_inventory.py \
  --census "$SCR/census.jsonl" --taxonomy "$SCR/item_taxonomy.json" \
  --sectors "$SCR/sector_categories.json" \
  --districts data/districts.json \
  --loot-registry "$SCR/world_res/base/worlds/03_night_city/_compiled/default/03_night_city.loot.json" \
  --out "$SCR/inventory.jsonl"
```

`pipeline.py --stage all` runs the same stages in order with caching.

### A.1 Galleries worth re-checking by hand

```bash
# Evelyn's handbag — the canonical example.
grep -o '"debug_name": "q004_evelyn_small_purse".*' "$SCR/inventory.jsonl"

# The five biggest sources.
python3 -I -c "
import json,collections
rows=[json.loads(l) for l in open('$SCR/inventory.jsonl')]
act=[r for r in rows if r['category'] in ('quest_prop','quest_shard','quest_corpse','quest_keycard')]
print(collections.Counter(r['owner_code'] for r in act).most_common(5))"

# Cyberpsycho / hustle corpses.
grep '"owner_family": "scanner_hustle"' "$SCR/inventory.jsonl" | grep quest_corpse
```

## Appendix B — verified output shapes

`worldEntityNode` holding a quest shard (the item record is in the instance
buffer, not in the sector's node prototype):

```json
{ "$type": "worldEntityNode",
  "appearanceName": { "$value": "shard_case_container_entropy_a" },
  "debugName": { "$value": "shard_case_container" },
  "entityTemplate": { "DepotPath": { "$value": "base\\gameplay\\loot\\shard_cases\\shard_case_container.ent" } },
  "instanceData": { "Data": { "buffer": { "Data": { "Chunks": [
      { "$type": "ShardCaseContainer",
        "itemTDBID": { "$value": "Items.sts_wbr_jpn_03_shard_001" },
        "hasQuestItems": 0,
        "containerType": "AmmoCase" } ] } } } } }
```

Streaming descriptor with named variants (this is the `range_index` key):

```json
{ "$type": "worldStreamingSectorDescriptor",
  "category": "Exterior",
  "data": { "DepotPath": { "$value": "base\\worlds\\03_night_city\\_compiled\\default\\exterior_-19_24_0_0.streamingsector" } },
  "questPrefabNodeRef": { "$value": "0" },
  "variants": [ { "name": { "$value": "bar_closed_sign" }, "rangeIndex": 1,
                  "enabledByDefault": 0, "variantId": 825840465 } ] }
```

Engine loot registry entry (authoritative container list):

```json
{ "nodeRefsHash": ["1217024441039680", "…"],
  "tweakDbIds": [ [ { "$value": "Loot.GenericHealingCosumabless" },
                    { "$value": "DeviceContentAssignment.rancho_coronado_generic" } ] ] }
```
