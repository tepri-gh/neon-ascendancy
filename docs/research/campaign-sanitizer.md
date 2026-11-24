# Research 0.1 — Any-Entry-Point Campaign Disable & World-Era Sandbox Sanitizer

**Target:** Cyberpunk 2077 2.5, redscript 1.x, Codeware-free.
**Date:** 2026-11-23.
**Scope:** world-era detection; full-city unlock; Johnny suppression; vanilla quest/gig/call/dialogue suppression; CET verification playbook.

**Evidence grades used below**

- **[V]** verified in the local decompiled 2.5 scripts under `refs/cyberpunk` (file + line cited), or in official CDPR patch notes / official API docs.
- **[R]** verified in a published resource study of the 2.31 quest/phase/scene data (Ghostline, `axefrog/xf-studio`, `let_there_be_flight`). Strong structural evidence, not a runtime test on 2.5.
- **[C]** community report, mod description, or console-guide claim. Useful, but not proof.
- **[H]** hypothesis. Must be tested in-game before it becomes a design dependency.

The provided `refs/cyberpunk` checkout is the 2.5 script bundle but is **not complete** (1,788 `.swift` files). In particular it does not contain the 2.2+ Johnny passenger system. Claims that depend on missing files are marked **[H]** rather than presented as verified.

---

## 0. Executive summary

1. **Era detection is tractable with a small, monotonic fact set.** The reliable spine is:
   `q005_done`, `q101_done`, `watson_prolog_unlock`, `watson_prolog_lock`,
   `q101_enable_activities_flat`, `q101_enable_side_content`,
   `q115_point_of_no_return`, `ep1_standalone`, `ep1_installed`, `q301_00_done`.
   Use `> 0`, never `== 1`: several facts are incremented, and `q101_enable_side_content`
   can reach `2` in existing saves. **[R]** **[C]**

2. **Lifting the Watson lockdown needs at least two facts, not one.**
   `watson_prolog_lock = 0` removes the physical/NCART blockade, but the Act 2
   world-content switches are separate: `watson_prolog_unlock = 1`,
   `q101_enable_activities_flat = 1`, `q101_enable_side_content = 1`.
   Do **not** set `q101_done = 1` or `q005_done = 1` just to unlock the city;
   those are story-completion facts with other readers. **[R]**

3. **Vendors/ripperdocs are not story-gated in their UI or transaction code.**
   Their presence is controlled by spawn/`*_default_on` facts and by the vendor
   record. The safest design is to unlock movement, then probe/repair only
   missing vendor presence facts, not bulk-resurrect every vendor. **[V]**

4. **Johnny is several independent systems.**
   Verified and safe to suppress: possession fact (`isPlayerPossessedByJohnny`),
   relic-malfunction status effects (`JohnnySickness` tag), the Johnny tour HUD,
   and all scripted Johnny quest scenes (by suppressing quests).
   **Not verified:** a runtime switch for the 2.2/2.3 “Johnny passenger” feature.
   `johnny_on` / `johnny_off` / `johnny_default_on` are plausible candidates, but
   their semantics are not exposed in the provided scripts. This is the largest
   open question in this research. **[V]** **[H]**

5. **Journal state is a record, not the quest logic.**
   `JournalManager` can hide, untrack, and deactivate entries, but it does not
   stop an already-running quest phase or scene. Tier 1 can make vanilla content
   invisible and non-initiating; complete excision still needs Tier 2 quest-graph
   editing (already listed as deferred in `docs/roadmap.md`). **[V]** **[C]**

6. **The best suppression points are presentation and initiation gates:**
   - `PhoneSystem.OnTriggerCall` — block incoming fixer/quest calls.
   - `InteractionUIBase.OnDialogsData` — filter `QuestImportant` dialogue choices.
   - `WorldMappinsContainerController.CreateMappinUIProfile` and
     `MinimapContainerController.CreateMappinUIProfile` — deny quest/gig mappin
     variants while preserving fast travel, vendors, ripperdocs, stashes,
     apartments, and ambient dynamic events.
   - `JournalManager` callbacks — deactivate/untrack vanilla quests as they appear.
   - `WorldMapMenuGameController.UpdateTrackedQuest` and
     `QuestTrackerGameController.UpdateTrackerData` — defensive clearing.

7. **A safe sanitizer is a deferred, event-driven, idempotent system.**
   It must not mutate journal state inside a journal callback. It should enqueue
   one next-frame request, guard with `m_applying`, and re-scan only on load,
   era change, or journal event. No per-frame work.

---

## 1. World-era detection (`QuestsSystem` facts)

### 1.1 Fact primitives and their limits

`QuestsSystem` is a native system with only fact read/write and listener APIs:

```redscript
// refs/cyberpunk/orphans.swift:18132
public final importonly class QuestsSystem extends questIQuestsSystem {
  public final native func GetFact(factName: CName) -> Int32;
  public final native func GetFactStr(factName: String) -> Int32;
  public final native func SetFact(factName: CName, value: Int32) -> Void;
  public final native func SetFactStr(factName: String, value: Int32) -> Void;
  public final native func RegisterListener(factName: CName, listener: ref<IScriptable>, funcName: CName) -> Uint32;
  public final native func UnregisterListener(factName: CName, id: Uint32) -> Void;
}
```

Consequences:

- A fact that was never set reads `0`.
- Facts are signed 32-bit integers; some are “add 1” counters, so `== 1` is
  unsafe. Use `> 0`.
- Facts and journal state are **two separate records**. The quest graph writes
  both; changing one does not automatically change the other. **[R]**
- A fact name is not a specification. The tables below use both the name and the
  writer/reader evidence from the extracted quest resources.

### 1.2 The era-defining fact set

The following values are the useful discriminators. Sources: **[R]** 2.31
quest/phase/scene studies; **[V]** local 2.5 scripts where noted.

| Fact | Meaning | Writer / reader evidence | Expected values |
| --- | --- | --- | --- |
| `q000_done` | Life-path prologue finished | Set in `q000`; also set by `q303.quest` / `q306.quest` in PL. Read by `lizzies_default`, `q004_nightclub`, `q204_columbarium_holograms`. | `> 0` after the lifepath intro. Do **not** use alone: PL also writes it. |
| `q001_done` | The Rescue / The Ripperdoc finished | Set in `q001_cleanup`; also `q303.quest`. | `> 0` after the prologue. Some skip mods leave gaps. |
| `q001_active` | The Rescue active | Prologue phase. | `> 0` during the rescue. |
| `q003_done` | The Pickup finished | `q003` / `q003_end`. | `> 0` after The Pickup. |
| `q004_done` | The Information finished | `q004_nightclub` / `q004_after_bd`. | `> 0` after The Information. |
| `q005_start` | The Heist started | `q005_01_plan`. | `> 0` during The Heist. |
| `q005_active` | The Heist active | `q005`. | `> 0` during The Heist. |
| `q005_done` | The Heist finished | Set in `q005_09_no_tell_motel`. Read by `q204_columbarium_holograms`. | `> 0` after the Heist. **The strongest base-game “post-Heist” marker.** |
| `q101_active` | Playing for Time active | `q101_resurrection`. | `> 0` during early Act 2. |
| `q101_done` | Playing for Time / Love Like Fire finished | Set in `q101_cleanup` by “add 1”. | `> 0` after q101. |
| `watson_prolog_lock` | Watson lockdown is active | Set to `1` by `q001_ride_to_mb`; set to `0` by `q101.questphase`. Gates `open_world_content`’s `lch_prolog_roadblocks`; read by NCART/data-term scripts. | `1` in Act 1; `0` from q101 onward. |
| `watson_prolog_unlock` | Prologue is over / Act 2 marker | Set to `1` by `q101_j_01_concert.questphase` (Love Like Fire). Used by mods as “prologue finished”. | `0` before Love Like Fire; `1` after. |
| `q101_enable_activities_flat` | Act 2 open-world activities enabled | Set in scene `q101_07c_johnny_triggers.scene`; `q101_p2_v_room.questphase` waits for it. Used by Dark Future as “Act 2 start”. | `0` in Act 1; `> 0` in Act 2. |
| `q101_enable_side_content` | Act 2 side content enabled | Set in `q101_p2_meet_takemura.questphase`. Gates minor quests, some hustles, vehicle offers. | `0` in Act 1; `> 0` in Act 2 (can be `2`). |
| `q112_done` | Down on the Street chain finished | `q112_abduction`. | `> 0` late Act 1/2 branch. |
| `q115_point_of_no_return` | Point of no return passed | `q115_00_hanako`; also `q307` in PL. | `0` before Embers; `1` after. |
| `q115_done` | For Whom the Bell Tolls finished | `q115_02_ripperdoc` / `q115_afterlife`. | `> 0` on the Johnny route. |
| `q116_done` | Changes finished | `q116_mikoshi`. | `> 0` near the end. |
| `q201_done` … `q204_done` | Epilogues finished | Each epilogue phase. | One or more `> 0` after credits. |
| `ep1_installed` | Phantom Liberty installed | `ep1.quest`, `ep1_standalone.quest`. | `> 0` if DLC present. |
| `ep1_standalone` | Phantom Liberty standalone start | `ep1_standalone.quest`. Read by `act_1`, q301/q302/q304/q305 phases. | `> 0` only in a PL standalone game. |
| `ep1_active` | PL content active | `q110b`, `q301`–`q307`. | `> 0` once PL has started. |
| `ep1_side_content` | Dogtown side content open | `ep1_main_quests`, q302–q306. | `> 0` when Dogtown side content is open. |
| `q301_00_done` | Dog Eat Dog hook finished | `q301`, `q301_hook`. Read by q301 border phases. | `> 0` after the PL hook. |
| `q301_done` | PL quest 1 finished | `q301_shuttle`; also `q306.quest`. | `> 0` after Dog Eat Dog. |
| `q302_done` | Lucretia My Reflection finished | PL chain. | `> 0` after q302 (Dogtown opens further). |

**Hashes.** If an external save reader needs to inspect the same facts offline,
`axefrog/xf-studio/research/story-engine/main-story-facts.json` stores the
FNV-1a 32-bit hash of each fact name. Examples: `q005_done = f4b049dc`,
`q101_done = 37811c85`, `q115_point_of_no_return = 73189b35`,
`ep1_standalone = 8fec3b23`. **Do not hard-code these in redscript**; use the
name strings. They are useful only for external readers. **[R]**

### 1.3 Classifier

The classifier is a pure function over a fact snapshot. It never writes.

```text
Era Detect(f):
  if f.ep1_standalone > 0:
      return PLStandalone

  if f.q201_done > 0 or f.q202_done > 0 or f.q203_done > 0 or f.q204_done > 0:
      return PostStory

  if f.q115_point_of_no_return > 0 or f.q116_done > 0:
      return Endgame

  if f.q005_done > 0:
      if f.q101_done > 0
         or f.q101_enable_side_content > 0
         or f.watson_prolog_lock == 0:
          return Act2
      return Interlude          // post-Heist, before Playing for Time

  if f.watson_prolog_unlock > 0:
      return Interlude          // save during Love Like Fire

  if f.q001_done > 0:
      return Act1PreHeist

  if f.q005_active > 0 or f.q001_active > 0 or f.q000_done > 0:
      return Prologue

  return Unknown
```

Then compute a **consistency mask** separately:

```text
flags.HasHeistDone      = q005_done > 0
flags.HasAct2Flags      = q101_enable_activities_flat > 0 or q101_enable_side_content > 0
flags.HasCityUnlock     = watson_prolog_lock == 0 and watson_prolog_unlock > 0
flags.HasPL             = ep1_installed > 0
flags.IsPLStandalone    = ep1_standalone > 0
flags.IntroSkipped      = q001_done > 0 and q000_done == 0
flags.HeistSkipped      = q005_done == 0 and (q101_done > 0 or q101_enable_side_content > 0)
flags.LockAlreadyLifted = watson_prolog_lock == 0 and q005_done == 0
```

`IntroSkipped`, `HeistSkipped`, and `LockAlreadyLifted` are **not errors**.
They are the expected signatures of intro-skip, Watson-skip, save-editor, and
NG+ mods. The sanitizer should classify them as “modified” and apply only
monotonic unlocks. It must **never** “repair” the story by setting
`q005_done = 1`, `q101_done = 1`, or `q000_done = 1`; those facts have other
readers and can change epilogue holograms, quest gates, and side content. **[R]**

### 1.4 Common intro / Watson-skip signatures

| Mod family | Likely signature | Sanitizer response |
| --- | --- | --- |
| Resource-edit intro skip (“Fresh Start”, “New Lifepath Intro”) | `q001_done > 0`, `q000_done == 0`, possibly `q005_done > 0`; quest resources edited, facts may be sparse | Treat as `Act1PreHeist` or `Interlude` by furthest milestone; do not require `q000_done`. |
| Fact-based Watson skip | `watson_prolog_lock == 0`, `watson_prolog_unlock > 0`, often `q101_enable_side_content > 0`, `q005_done == 0` | `LockAlreadyLifted`; set only missing Act 2 switches; do not set story-done facts. |
| Save editor / NG+ | `q101_done > 0` without `q005_done`, or `q115_point_of_no_return` already `0` after endgame | Classify by highest completed milestone; never lower an existing flag. |
| PL standalone | `ep1_standalone > 0` | Check first; base-game facts may be zero or synthetic. |
| Hand-edited/unknown | contradictory pairs (`q101_done > 0` and `q005_done == 0`) | `Unknown/Modified`; require explicit user confirmation before destructive suppression. |

### 1.5 Era policy

| Era | City unlock | Campaign suppression | Johnny suppression |
| --- | --- | --- | --- |
| `Prologue` | No — wait for `q001_done > 0` and no active scene | No | No |
| `Act1PreHeist` | Yes, explicit opt-in only | Yes, player-facing; warn that the campaign will stall | No (Johnny not present yet) |
| `Interlude` | Yes | Yes; defer if a Heist/Love Like Fire scene is active | Partial |
| `Act2` | Already open; repair missing flags only | Yes | Yes |
| `Endgame` | Already open | Yes; do not rewind `q115_point_of_no_return` | Yes |
| `PostStory` | Already open | Yes | Yes |
| `PLStandalone` | Night City + Dogtown open; repair missing Night City flags | Yes, including q301–q307 | Yes if Johnny is present |
| `Unknown/Modified` | Observe only until confirmed | Observe only | Observe only |

The “explicit opt-in” is important. Applying the sanitizer in Act 1 is
irreversible for that save branch unless the player reloads a backup. The entry
menu should state that and offer a checkpoint save first.

---

## 2. Full city unlock and working shops

### 2.1 What `watson_prolog_lock` actually gates

Verified:

- `dataTermGameController` refuses to resolve the NCART hologram when
  `watson_prolog_lock >= 1`.
  (`refs/cyberpunk/cyberpunk/devices/UI/dataTerm/dataTermGameController.swift:38`)
- `ncartTimetableGameController` hides the timetable UI when the fact is `> 0`.
  (`.../ncrtTimeTable/ncartTimetableGameController.swift:151-152`)
- `open_world_content` starts the `lch_prolog_roadblocks` phase while the fact is
  `> 0`; the phase hides the blockade once the fact is `0`. The same study states
  `q001_ride_to_mb` sets it to `1` and `q101` sets it to `0`. **[R]**
- `FastTravelSystem` does **not** read `watson_prolog_lock`. Its gates are the
  `m_fastTravelLocks` array, the `BlockFastTravel` status-effect tag, and
  `m_isFastTravelEnabledOnMap`.
  (`refs/cyberpunk/core/systems/fastTravelSystem.swift:300-407, 547-670`)

So the lockdown is primarily:

1. physical roadblocks and NCART gate state,
2. map/NCART presentation,
3. Act 2 content switches that are normally set by q101.

It is **not** a vendor/ripperdoc transaction gate.

### 2.2 Minimal and recommended unlock sets

**Minimal physical unlock (Act 1):**

```text
watson_prolog_lock   = 0
watson_prolog_unlock = 1
```

**Recommended full-city unlock (Act 1 sandbox):**

```text
watson_prolog_lock            = 0
watson_prolog_unlock          = 1
q101_enable_activities_flat   = 1
q101_enable_side_content      = 1
```

**Do not set:**

| Fact | Why not |
| --- | --- |
| `q101_done = 1` | It means Playing for Time finished. It has quest-graph readers and can skip/alter content. Use the enable flags instead. |
| `q005_done = 1` | It means the Heist finished; read by epilogue holograms and other phases. |
| `q001_done = 1` / `q000_done = 1` | Story completion, not an unlock. Breaks intro-skip detection and may trigger readers. |
| `q115_point_of_no_return = 0` | Never rewind a point-of-no-return save. |
| `q301_* = 1` in a non-PL save | Could start PL content without the DLC/graph. |

`q101_enable_activities_flat` and `q101_enable_side_content` are the correct
“Act 2 is open” switches. They are read by world-content phases, minor quests,
vehicle offers, and mods. Setting them early may cause gigs/fixers to start;
that is exactly what the suppression layers are for. **[R]**

**Interlude caveat:** if `q101_active > 0` (Playing for Time is running), setting
`q101_enable_side_content` can let q101’s own phases advance. In that era, either
suppress the journal first or apply the unlock only after the player has accepted
that the campaign is abandoned. On a pre-Heist Act 1 save, q101 is not active,
so this caveat does not apply.

`q001_show_sts_tut` opens street stories and `ow_psychos_intro_done` opens
cyberpsycho pins. The sanitizer suppresses those activities, so it does **not**
need to set them. If the design later wants an opt-in “vanilla gigs on” mode,
set them only in that mode.

### 2.3 Fast travel

Verified from `FastTravelSystem`:

- `IsFastTravelEnabled()` is false if `m_fastTravelLocks` is non-empty.
- `IsFastTravelEnabledOnMap()` additionally requires
  `m_isFastTravelEnabledOnMap`.
- `RemoveAllFastTravelLocks(game)` queues `RemoveAllFastTravelLocksRequest`.
- `FastTravelMenuToggledEvent { isEnabled = true }` sets map availability and
  bumps `tutorial_fast_travel`.
- `RegisterFastTravelPoint` refuses to register a point while the player has a
  `BlockFastTravel` status effect.

Recommended idempotent sequence on load:

```redscript
// pseudo-redscript
let ft = GameInstance.GetScriptableSystemsContainer(game).Get(n"FastTravelSystem") as FastTravelSystem;
let removeLocks = new RemoveAllFastTravelLocksRequest();
ft.QueueRequest(removeLocks);
let enableMap = new FastTravelMenuToggledEvent();
enableMap.isEnabled = true;
ft.QueueRequest(enableMap);
```

This clears vehicle/combat/quest locks and turns on map fast travel. It does
**not** create fast-travel points that were never registered. The open-world
fast-travel phase normally registers all points at world init; whether all
non-Watson points exist in an Act 1 save is an in-game question. **[H]**

If points are missing, the heavier fallback is to iterate the
`FastTravelPoint` TweakDB records and queue `RegisterFastTravelPointRequest`
with `FastTravelPointData`. That is not designed here because it requires
building `FastTravelPointData` for ~159 points and risks duplicating points.
The CET playbook in §6 includes a probe to decide whether this is necessary.

### 2.4 Vendors and ripperdocs

Verified in the 2.5 scripts:

- Vendor and ripperdoc screens obtain stock from `VendorDataManager` / vendor
  records. There is no `watson_prolog_lock` check in the transaction path.
- In the inspected vendor/ripperdoc code, `q001_ripperdoc_done` gates only
  Viktor’s first-time tutorial path (`vendorHubMenuGameController.swift:198`,
  `ripperdoc.swift:476`). It may have other readers outside this subset.
- `mq048_active` / `ep1_ripperdoc_tutorial_seen` control the cyberware tutorial,
  not whether the shop works (`ripperdoc.swift:478-480`).
- `*_default_on` facts control whether a vendor/NPC spawn set is active. They
  are not transaction gates.

Therefore:

- If the vendor NPC is present and interactable, the shop works in Act 1.
- If the vendor is missing, the fix is the vendor’s `*_default_on` fact (or the
  community/spawn set), not `watson_prolog_lock`.
- The `*_default_on` facts are also used by quest phases to temporarily replace
  or close a vendor. Bulk-setting all of them can resurrect a vendor that a
  quest intentionally closed (for example, a ripperdoc after a violent outcome).
  Use a **probe-then-repair** strategy, not a blanket overwrite.

Relevant ripperdoc/medic facts for a probe (from the 2.1 fact dump; verify on
2.5):

| District | Ripperdoc / medic presence facts |
| --- | --- |
| Badlands | `bls_ina_se1_ripperdoc_01_default_on`, `bls_ina_se1_medicstore_01_default_on` |
| City Center | `cct_dtn_ripdoc_01_default_on`, `cct_dtn_medic_01_default_on`, `cct_cpz_medic_01_default_on` |
| Heywood | `hey_spr_ripperdoc_01_default_on`, `hey_spr_medicstore_01_default_on` |
| Pacifica | `pac_wwd_ripdoc_01_default_on`, `pac_cvi_medicstore_01_default_on` |
| Santo Domingo | `std_arr_ripperdoc_01_default_on`, `std_rcr_ripperdoc_01_default_on`, `std_arr_medicstore_01_default_on`, `std_rcr_medicstore_01_default_on` |
| Watson | `wat_kab_ripperdoc_01/02/03_default_on`, `wat_nid_ripperdoc_01_default_on`, `wat_lch_medicstore_01_default_on`, `wat_nid_medicstore_01/02_default_on` |
| Westbrook | `wbr_jpn_ripdoc_01/02_default_on`, `wbr_hil_ripdoc_01_default_on`, `wbr_jpn_medic_01_default_on`, `wbr_nok_medic_01_default_on` |

Other vendor classes follow the same pattern: `*_gunsmith_*_default_on`,
`*_clothingshop_*_default_on`, `*_foodshop_*_default_on`,
`*_junkshop_*_default_on`, `*_melee_*_default_on`, `*_netrunner_*_default_on`,
`*_techstore_*_default_on`. They should be treated the same way: probe first.

Stashes use the device/apartment system (`Zzz07_PlayerStashVariant`), not a
story fact. If the apartment/stash device exists, it works.

### 2.5 Apartments

Verified facts in the 2.1 dump / 2.31 resource studies:

- H10: `apartment_on` (plus `apartment_tv` for the TV).
- Purchasable apartments:
  - `dlc6_apart_cct_dtn_purchased` (Corpo Plaza)
  - `dlc6_apart_hey_gle_purchased` (The Glen)
  - `dlc6_apart_wat_nid_purchased` (Northside)
  - `dlc6_apart_wbr_jpn_purchased` (Japantown)
- Their purchase terminals/phase also use
  `dlc6_apart_*_purchase_possibility` and `dlc6_apart_*_purchase_setup`.
- The four apartment fast-travel points are
  `FastTravelPoints.dlc6_apart_*_dataterm`.

Setting only `*_purchased` is the smallest possible unlock. Whether it also
registers the apartment dataterm, stash, wardrobe, and bed is **[H]**: the
apartment phase may need to run. Test sequence:

1. Set `dlc6_apart_wbr_jpn_purchased = 1` on a copy.
2. Open the map; check for the Japantown apartment dataterm.
3. Enter the apartment; check stash/wardrobe/bed.
4. If missing, also set `*_purchase_possibility = 1` and retest.
5. Do not set all four at once until one works; isolate.

### 2.6 Post-Act 1 saves

A post-Heist save should already have:

```text
watson_prolog_lock   = 0
watson_prolog_unlock = 1
q101_enable_activities_flat > 0
q101_enable_side_content > 0
```

The sanitizer must be **monotonic**: it only raises unlock flags from `0` to `1`
and lowers `watson_prolog_lock` from `1` to `0`. It never lowers a completed
story fact and never re-locks the city. If a post-Heist save is missing an Act 2
switch because of a skip mod, set only that missing switch.

### 2.7 Acceptance matrix

| # | Save | Action | Expected |
| --- | --- | --- | --- |
| 1 | Act 1, after The Ride | Read facts | `lock=1`, `unlock=0`, `q005_done=0`, `q101_done=0` |
| 2 | Act 1 | Set only `lock=0`, `unlock=1` | Watson roadblock/NCART open; fast travel map state unchanged; non-Watson vendor still reachable only by walking |
| 3 | Act 1 | Add `q101_enable_activities_flat=1`, `q101_enable_side_content=1` | Map/fast travel behavior matches Act 2; if gigs appear, suppression must hide them |
| 4 | Act 1 | Walk to a non-Watson ripperdoc | Shop opens; no tutorial unless `q001_ripperdoc_done=0` |
| 5 | Act 1 | Walk to a non-Watson vendor | Shop opens; stock follows vendor record |
| 6 | Post-Heist | Apply sanitizer | City remains open; no re-lock |
| 7 | PL standalone | Apply sanitizer | Night City and Dogtown remain open; PL quests hidden |
| 8 | Intro-skip save | Apply sanitizer | Classified as modified; only missing unlocks set; no story “repair” |

---

## 3. Disabling Johnny Silverhand

### 3.1 Verified systems

**Possession fact.**

```redscript
// refs/cyberpunk/core/systems/playerSystem.swift:28-34
public final const func GetPossessedByJohnnyFactName() -> String {
  return "isPlayerPossessedByJohnny";
}

protected final cb func OnGameRestored() -> Bool {
  if Cast<Bool>(GameInstance.GetQuestsSystem(this.GetGameInstance()).GetFactStr(this.GetPossessedByJohnnyFactName())) {
    this.OnLocalPlayerPossesionChanged(gamedataPlayerPossesion.Johnny);
  } else {
    this.OnLocalPlayerPossesionChanged(gamedataPlayerPossesion.Default);
  };
}
```

Setting `isPlayerPossessedByJohnny = 0` on load clears the possession UI theme.
It does not by itself stop a Johnny replacer puppet; that is controlled by the
quest/scene that mounted it.

**Johnny replacer.**

`PlayerPuppet.IsJohnnyReplacer()` returns true when the controlled puppet record
is `Character.johnny_replacer`
(`refs/cyberpunk/cyberpunk/player/player.swift:633-634`). The replacer path also
applies `GameplayRestriction.BlockAllHubMenu`, `BlockFastTravel`, and invulnerability
during the sequence (`player.swift:983-1003`). Do not try to remove those
restrictions while a replacer scene is active; wait for the scene to end.

**Johnny tour HUD.**

`hudJohnnyController` shows the “Johnny tour” overlay when:

```redscript
// refs/cyberpunk/cyberpunk/UI/hud/custom/hud_johnny.swift
q108_active == 1
q101_active == 1
q101_johnny_tour_cancelled == 1
```

If the campaign is suppressed but those facts remain, the HUD can still appear.
The clean fix is a HUD wrapper that hides the root widget when the sanitizer is
active, not setting `q101_active = 0` / `q108_active = 0` (those are quest facts
with other readers).

**Relic malfunction status effects.**

`PlayerPuppet.IsJohnnySicknessBreathingEffectActive` checks four effects:

```redscript
// refs/cyberpunk/cyberpunk/player/player.swift:4879-4886
BaseStatusEffect.JohnnySicknessLow
BaseStatusEffect.JohnnySicknessMedium
BaseStatusEffect.JohnnySicknessHeavy
BaseStatusEffect.JohnnySicknessMediumQuest
```

All four are tagged `JohnnySickness`. `StatusEffectHelper` provides the removal
primitive:

```redscript
// refs/cyberpunk/core/systems/statusEffectSystem.swift
StatusEffectHelper.RemoveStatusEffectsWithTag(target, n"JohnnySickness");
```

This removes current effects. It does not prevent a quest phase from applying a
new one. Use a short post-load cleanup window and/or a status-effect listener to
keep them off. Do **not** remove all status effects; that would remove Relic
perks, cyberware effects, and quest restrictions.

**Johnny perk tree.**

`q005_johnny_chip_acquired` gates the Johnny/Relic perk category
(`NewPerksCategoriesGameController.swift:443`, `perksMain.swift:130`). Do not set
it unless the design explicitly wants the Relic tree. Suppressing Johnny does not
require touching it.

**“Was ever Johnny”.**

`GameplaySettingsSystem.WasEverJohnny` is persistent (`core/ui/userSettingsData.swift:19-76`).
It only restores the Johnny HUD setting; it is not a spawn switch. Leave it.

### 3.2 The 2.2 / 2.3 passenger feature

Official CDPR statements:

- Update 2.2: “after finishing the first act, Johnny can now sometimes appear in
  the passenger seat,” except during combat, missions where Johnny plays a role,
  or when another passenger occupies the seat.
- Update 2.3: the player can ask Johnny to leave; he disappears “for a couple
  days.” **[C, official patch notes]**

Community mods confirm the behavior and show two implementation approaches:

- `Remove Passenger Johnny` is an **archive-only** mod that removes the system
  and has reports of crashes when exiting multi-seat vehicles and during quests
  that expect a Johnny passenger. **[C]**
- `The Passenger - Feature Settings` is a runtime mod with a configurable spawn
  chance, dialogue categories, and a “gone for 1–4 days” selector. Its changelog
  refers to “cooldown facts”, confirming the feature has facts, but the names
  are not public. **[C]**

The provided `refs/cyberpunk` 2.5 scripts contain **no** `PassengerSystem`,
`JohnnyPassenger`, or equivalent. A global search for `passenger` finds only
vehicle/mounting code, and a search for `johnny` finds HUD, possession, and quest
facts, not the 2.2 passenger system. Therefore:

- There is **no verified runtime switch** in the provided references.
- A Tier 1 “set a fact and Johnny never rides again” solution is a hypothesis.
- A hard despawn on vehicle mount is possible but risky; the archive mod’s crash
  reports are a warning, not proof that a script despawn is safe.

**Candidate facts to test (all [H]).** These names come from the 2.1 fact dump
(`pharingWell/factlog`) and are not proven to exist or mean the same thing in
2.5; the 2.5 fact dump was not available. Confirm each with `GetFactStr` before
using it.

| Fact | Why it is a candidate | What to measure |
| --- | --- | --- |
| `johnny_off` | Name suggests a global “Johnny off” state. | Read before/after telling Johnny to leave; set `1`; enter a car. |
| `johnny_on` | Inverse of `johnny_off`; may be the spawn enable. | Should be `0` when Johnny is off. |
| `johnny_default_on` | Written by `mq033_tarot.questphase`; likely the apartment/default spawn switch. | Read in apartment with/without Johnny; set `0`. |
| `johnny_mirror` | Apartment mirror Johnny. | Read before/after mirror scene. |
| `johnny_lookat_randomiser_01` | Presentation/randomiser, not spawn. | Low priority. |
| `isPlayerPossessedByJohnny` | Possession, not passenger. | Set `0` for UI; should not affect passenger. |

**If the facts fail:** do not ship a blind despawn. Either:

1. accept the passenger and mute his dialogue (not a full disable), or
2. move the passenger removal to Tier 2 archive/quest-graph editing, or
3. implement a narrowly scoped post-mount despawn with explicit crash testing
   on multi-seat vehicles, quests with a scripted passenger, and vehicle exit.

### 3.3 Johnny quest scenes and voiceovers

Most Johnny scenes are quest scenes. Suppressing the quests hides their journal
entries and blocks their dialogue choices, but **does not stop an already-running
scene**. The sanitizer should:

- defer destructive suppression while
  `SceneSystem.GetScriptInterface().IsEntityInScene(playerID)` or
  `IsRewindableSectionActive()` is true;
- hide the Johnny tour HUD with a wrapper;
- leave the quest facts alone;
- accept that a scene already in progress may finish.

Ambient Johnny comments in the apartment and passenger seat are separate from
quests. The apartment spawn is likely `johnny_default_on`; the passenger system
is the unresolved part above.

### 3.4 Recommended Johnny policy

| Layer | Action | Confidence |
| --- | --- | --- |
| Possession | Set `isPlayerPossessedByJohnny = 0` on load | [V] |
| Relic malfunction | Remove `JohnnySickness` effects; repeat for a short window | [V] |
| Tour HUD | Wrap `hudJohnnyController.OnPlayerAttach` / hide root when sanitizer active | [V] |
| Quest scenes/VO | Suppress quests + dialogue; defer during active scene | [V]/[R] |
| Apartment ambient | Set `johnny_default_on = 0`, `johnny_off = 1`; test | [H] |
| Passenger | Set `johnny_off = 1`, `johnny_on = 0`, `johnny_default_on = 0`; test; fall back to Tier 2 | [H] |
| Hard despawn | Not recommended until proven safe | [H] |

---

## 4. Suppressing vanilla quests, gigs, calls, and NPC quest dialogue

### 4.1 The hard limit: journal ≠ quest logic

`JournalManager` exposes quest records, states, tracking, and callbacks:

```redscript
// refs/cyberpunk/core/systems/journalManager.swift:2-94
public final native const func GetQuests(context: JournalRequestContext, out entries: [wref<JournalEntry>]) -> Void;
public final native const func GetMetaQuests(context: JournalRequestContext, out entries: [wref<JournalEntry>]) -> Void;
public final native const func GetEntry(hash: Uint32) -> wref<JournalEntry>;
public final native const func GetEntryState(entry: wref<JournalEntry>) -> gameJournalEntryState;
public final native func ChangeEntryStateByHash(hash: Uint32, state: gameJournalEntryState, notifyOption: JournalNotifyOption) -> Void;
public final native func GetTrackedEntry() -> wref<JournalEntry>;
public final native func UntrackEntry() -> Void;
public final native func RegisterScriptCallback(obj: ref<IScriptable>, functionName: CName, type: gameJournalListenerType) -> Void;
public final native func UnregisterScriptCallback(obj: ref<IScriptable>, functionName: CName) -> Void;
```

`gameJournalEntryState`: `Inactive = 1`, `Active = 2`, `Succeeded = 3`,
`Failed = 4`. `JournalNotifyOption`: `DoNotNotify = 1`, `Notify = 2`.
(`refs/cyberpunk/orphans.swift:8796-8826`)

`JournalQuest.GetType()` returns `MainQuest`, `SideQuest`, `MinorQuest`,
`StreetStory`, `CyberPsycho`, `Contract`, `VehicleQuest`, `ApartmentQuest`,
`CourierQuest`, `CourierSideQuest`
(`refs/cyberpunk/orphans.swift:7295-7306`, `22294-22303`).

What this can do:

- hide entries from the journal and quest tracker,
- untrack a quest,
- make a quest entry `Inactive`,
- react to new quests and re-hide them.

What it cannot do:

- stop a running `.questphase`,
- cancel a scene,
- prevent a trigger area from starting a phase,
- prevent a script from spawning an NPC,
- undo a quest’s world changes.

Community testing is explicit: changing a journal entry’s state “does not skip
or complete anything”; it hides the entry and can stall logic. **[C]**
That is acceptable for a sandbox that wants content to stop being offered, but
it must be described as **player-facing suppression**, not a true campaign
deletion. Tier 2 quest-graph excision remains the only complete kill.

### 4.2 Journal sanitizer

**Enumerate.**

```redscript
let context: JournalRequestContext;
context.stateFilter.active = true;
context.stateFilter.inactive = false;
context.stateFilter.succeeded = false;
context.stateFilter.failed = false;

let quests: array<wref<JournalEntry>>;
journal.GetQuests(context, quests);
journal.GetMetaQuests(context, quests); // merge, or run separately
```

**Classify.**

```redscript
let quest = entry as JournalQuest;
if IsDefined(quest) {
  let id = quest.GetId(); // e.g. "quests/main_quest/..." or "ep1/quests/..."
  if StrBeginsWith(id, "quests/") || StrBeginsWith(id, "ep1/quests/") {
    // vanilla, not Neon Ascendancy
  }
}
```

Do not rely on `GetType()` alone: a mod could create a `MainQuest` through the
scripted-quest template. Use the path prefix plus an explicit
`NeonAscendancy`/`na_` allow-list.

**Deactivate.**

```redscript
journal.ChangeEntryStateByHash(
  Cast<Uint32>(journal.GetEntryHash(entry)),
  gameJournalEntryState.Inactive,
  JournalNotifyOption.DoNotNotify
);
```

`ChangeEntryStateByHash` takes `Uint32`; `GetEntryHash` returns `Int32` in the
native signature. Cast explicitly.

**Deactivate children.** Parent quest state does not always hide objectives.
For each suppressed quest, get children with a filter that includes
`active/inactive/succeeded/failed`, and deactivate `JournalQuestObjective`
entries. Do this once at load, not on every tick.

**Do not touch** `JournalContact`, `JournalPhoneConversation`,
`JournalOnscreen`, `JournalCodexEntry`, `JournalPointOfInterest`,
`JournalTarot`, or `JournalInternetPage` by default. They are not quests and
are needed for vendors, messages, shards, and the codex.

**React to new quests.** Register a `gameJournalListenerType.State` callback:

```redscript
protected cb func OnJournalState(
  hash: Uint32,
  className: CName,
  notifyOption: JournalNotifyOption,
  changeType: JournalChangeType
) -> Bool
```

If `className == n"gameJournalQuest"` and the entry is vanilla and
`GetEntryState(entry) == Active`, enqueue a `SuppressEntryRequest` for the next
frame. **Never** call `ChangeEntryStateByHash` synchronously inside the callback:
it can re-enter the listener and mutate the journal while the game is iterating.

**React to tracking.** Register a `gameJournalListenerType.Tracked` callback.
If the tracked entry’s top-level quest is vanilla, call `UntrackEntry()`.
`JournalManager.TrackEntry` is native; do not wrap it (the project rule forbids
wrapping native functions). The callback + `UntrackEntry` is the compliant path.

**Ledger.** Keep an in-memory `array<Uint32>` of suppressed hashes. Rebuild it on
load; do not persist it. Persisting a large hash array adds save schema surface
for no benefit.

### 4.3 Tracking and world map

Verified hooks:

- `WorldMapMenuGameController.UpdateTrackedQuest()` is a private scripted method
  that reads `GetTrackedEntry()` and fills the map’s quest container
  (`refs/cyberpunk/cyberpunk/UI/fullscreen/map/worldMap.swift:442-472`).
- `QuestTrackerGameController.UpdateTrackerData()` is a private scripted method
  that fills the HUD tracker (`.../UI/quests/quest_tracker.swift:193-...`).
- `WorldMapMenuGameController.OnTrackedEntryChanges(...)` is registered for
  `gameJournalListenerType.Tracked` (`worldMap.swift:240`).

Defensive wrappers:

```redscript
@wrapMethod(WorldMapMenuGameController)
private final func UpdateTrackedQuest() -> Void {
  let journal = GameInstance.GetJournalManager(this.GetPlayerControlledObject().GetGame());
  let tracked = journal.GetTrackedEntry();
  if IsDefined(tracked) && Sandbox.IsVanillaQuestEntry(tracked) {
    journal.UntrackEntry();
  };
  wrappedMethod();
}
```

```redscript
@wrapMethod(QuestTrackerGameController)
private final func UpdateTrackerData() -> Void {
  let journal = GameInstance.GetJournalManager(this.GetPlayerControlledObject().GetGame());
  let tracked = journal.GetTrackedEntry();
  if IsDefined(tracked) && Sandbox.IsVanillaQuestEntry(tracked) {
    journal.UntrackEntry();
  };
  wrappedMethod();
}
```

If private field access is a problem, use the journal manager from the player’s
game instance as above. The wrapper is a fail-safe; the primary mechanism is the
tracked callback + `UntrackEntry`.

### 4.4 Mappin policy — the key to preserving shops and city life

The world map and minimap are populated from `MappinSystem`. Quest/gig pins are
separate from journal quests; deactivating a `JournalQuest` does not necessarily
remove a POI pin. The clean presentation gate is
`CreateMappinUIProfile`:

```redscript
// refs/cyberpunk/cyberpunk/UI/mappins/mappinsContainers.swift:45
public func CreateMappinUIProfile(
  mappin: wref<IMappin>,
  mappinVariant: gamedataMappinVariant,
  customData: ref<MappinControllerCustomData>
) -> MappinUIProfile
```

The same method exists on `MinimapContainerController` (`minimap.swift:362`).
Wrap both:

```redscript
@wrapMethod(WorldMappinsContainerController)
public func CreateMappinUIProfile(
  mappin: wref<IMappin>,
  mappinVariant: gamedataMappinVariant,
  customData: ref<MappinControllerCustomData>
) -> MappinUIProfile {
  if Sandbox.IsDeniedMappin(mappin, mappinVariant) {
    return MappinUIProfile.None();
  };
  return wrappedMethod(mappin, mappinVariant, customData);
}
```

```redscript
@wrapMethod(MinimapContainerController)
public func CreateMappinUIProfile(
  mappin: wref<IMappin>,
  mappinVariant: gamedataMappinVariant,
  customData: ref<MappinControllerCustomData>
) -> MappinUIProfile {
  if Sandbox.IsDeniedMappin(mappin, mappinVariant) {
    return MappinUIProfile.None();
  };
  return wrappedMethod(mappin, mappinVariant, customData);
}
```

`MappinUIProfile.None()` is a real static constructor
(`refs/cyberpunk/cyberpunk/UI/mappins/mappinUIProfile.swift:28-32`); it returns
an empty profile, which is how the game already hides stub/prevention mappins.

**Deny list** (quest/gig/activity presentation):

| Variant | Why deny |
| --- | --- |
| `DefaultQuestVariant` | Generic quest objective. |
| `QuestGiverVariant` | Mission-giver marker. |
| `ExclamationMarkVariant` / `QuestionMarkVariant` | Quest/activity markers. |
| `MinorActivityVariant` | NCPD hustles and minor activities. |
| `Zzz06_NCPDGigVariant` | NCPD gig pins. |
| `HuntForPsychoVariant` | Cyberpsycho sightings. |
| `ClientInDistressVariant` | Rescue/activity pins. |
| `BountyHuntVariant` | Bounty hunts. |
| `OutpostVariant` | Assault-in-progress/outpost pins. |
| `RetrievingVariant` | Retrieval activities. |
| `SabotageVariant` | Sabotage activities. |
| `ThieveryVariant` | Thievery activities. |
| `SOSsignalVariant` | SOS activities. |
| `Zzz09_CourierSandboxActivityVariant` | Courier sandbox. |
| `Zzz18_RacingVariant` | Races. |

Also deny any `mappin.IsQuestMappin()` regardless of variant; that is the
strongest signal for quest-owned pins.

**Keep list** (city life and services):

| Variant | Why keep |
| --- | --- |
| `FastTravelVariant`, `Zzz17_NCARTVariant` | Fast travel/NCART. |
| `ServicePoint*` (`Food`, `Guns`, `Clothes`, `Junk`, `Meds`, `MeleeTrainer`, `NetTrainer`, `Tech`, `Ripperdoc`, `Bar`, `DropPoint`, `Prostitute`, `BlackMarket`, `Glamdoc`) | Vendors, ripperdocs, drop points. |
| `ApartmentVariant`, `Zzz05_ApartmentToPurchaseVariant` | Housing. |
| `Zzz07_PlayerStashVariant`, `Zzz08_WardrobeVariant` | Stash/wardrobe. |
| `Zzz01_CarForPurchaseVariant`, `Zzz02_MotorcycleForPurchaseVariant` | Vehicle vendors. |
| `FixerVariant` | Fixer location; keep the person, suppress the work. |
| `GangWatchVariant` | Ambient gang activity. |
| `DynamicEventVariant`, `Zzz12_WorldEncounterVariant` | Ambient world events. |
| `HiddenStashVariant` | Stashes. |
| `TarotVariant` | Collectible; optional. |

**Data layer cleanup.** For mappins already registered, iterate:
`MappinSystem.GetMappins(gamemappinsMappinTargetType.Map, mappins)` and
`GetMappins(Minimap, ...)`, then `SetMappinActive(id, false)` for denied
variants. If the mappin is a `QuestMappin`, compare
`GetJournalPathHash()` against the suppressed journal hash set; that avoids
hiding a non-quest mappin that happens to share a variant.

`SetMappinActive` is a native method; do not wrap it. Use it from the sanitizer
on load and when a denied mappin appears. The UI profile wrapper is the
fail-safe if a quest phase re-activates the mappin.

**Neon Ascendancy’s own mappins must not be caught by this filter.** Use a
non-quest mappin type/variant (for example `Mappins.DefaultStaticMappin` with
`DefaultVariant`, or a dedicated custom variant), or add an explicit
`NeonAscendancy` allow-list checked before the deny list. Do not create our
mission pins as `QuestMappin` unless the filter is taught to distinguish them.

### 4.5 Phone calls

`PhoneSystem.OnTriggerCall` is the single quest-call entry point:

```redscript
// refs/cyberpunk/cyberpunk/systems/phoneSystem.swift:83
private final func OnTriggerCall(request: ref<questTriggerCallRequest>) -> Void
```

`questTriggerCallRequest` carries `caller`, `addressee`, `callPhase`,
`callMode`, `isPlayerTriggered`, `isRejectable`, `showAvatar`, `visuals`
(`refs/cyberpunk/orphans.swift:41474-41491`). `questPhoneCallPhase`:
`IncomingCall = 1`, `StartCall = 2`, `EndCall = 3`
(`orphans.swift:11039-11044`).

Wrapper policy:

```redscript
@wrapMethod(PhoneSystem)
private final func OnTriggerCall(request: ref<questTriggerCallRequest>) -> Void {
  if Sandbox.ShouldBlockCall(request) {
    return; // swallow the call; do not play audio or set phone facts
  };
  wrappedMethod(request);
}
```

```text
ShouldBlockCall:
  if request.callPhase == EndCall: return false
  if request.isPlayerTriggered: return false
  if caller == "player" / "Player": return false
  if caller or addressee is a Neon Ascendancy contact: return false
  if callPhase == IncomingCall or StartCall: return true
  return false
```

Notes:

- Always pass `EndCall`; swallowing it can leave the phone UI stuck in a call.
- Always pass player-triggered calls; the player may call a vendor/fixer, and
  that is not quest initiation.
- Allow the mod’s own contacts by name prefix.
- Some quest calls are `StartCall` with `isPlayerTriggered = false`; block them
  too. The quest is suppressed anyway.
- This blocks the **call**, not the quest phase. Gigs can still start from a
  trigger area; combine with mappin/pin suppression.
- Fixer text messages are not phone calls. If the design wants a completely
  silent fixer, add an optional SMS layer; do not block all phone messages
  (vendors and story contacts use them).

### 4.6 NPC quest dialogue

The actual dialogue data flow is:

```text
UIInteractions.DialogChoiceHubs (Variant)
  -> InteractionUIBase.OnDialogsData(Variant)      // refs/.../interactionUIBase.swift:62-70
  -> UpdateDialogsData(script_ref<DialogChoiceHubs>)
  -> dialogWidgetGameController stores m_data      // refs/.../dialogUI.swift:57-59
  -> DialogHubLogicController.SetData(...)
```

`dialogWidgetGameController.UpdateDialogsData` is the subclass override, but the
reliable hook is the base `InteractionUIBase.OnDialogsData(Variant)`: that is
where the game converts the Variant and calls the virtual update. A community
note that `dialogWidgetGameController.UpdateDialogsData` “compiles, never fires”
is a warning against relying only on the subclass method. **[C]**

Recommended wrapper:

```redscript
@wrapMethod(InteractionUIBase)
protected cb func OnDialogsData(value: Variant) -> Bool {
  let data: DialogChoiceHubs = FromVariant<DialogChoiceHubs>(value);
  if Sandbox.IsActive(this.GetPlayerControlledObject().GetGame()) {
    data = Sandbox.FilterDialogHubs(data);
  };
  return wrappedMethod(ToVariant(data));
}
```

**Compile-check note.** `FromVariant<DialogChoiceHubs>` is used by the vanilla
base class, so it is valid. `ToVariant(DialogChoiceHubs)` is the natural inverse
but is not exercised in the provided scripts; if 1.x rejects it, use the
`dialogWidgetGameController.UpdateDialogsData(script_ref<DialogChoiceHubs>)`
override and mutate `Deref(data).choiceHubs` directly instead. Do not ship
without a compile and an in-game vendor/ripperdoc dialogue test.

Filtering:

```text
For each hub in data.choiceHubs:
  kept = []
  for each choice in hub.choices:
    if ChoiceTypeWrapper.IsType(choice.type, gameinteractionsChoiceType.QuestImportant):
      drop
    else:
      keep
  if kept is empty:
    drop hub
  else:
    hub.choices = kept
    keep hub
```

`gameinteractionsChoiceType.QuestImportant = 0`
(`refs/cyberpunk/orphans.swift:688-702`). `ChoiceTypeWrapper.IsType` is the
public predicate (`orphans.swift:23867-23873`).

Why filter choices instead of hubs:

- A vendor/ripperdoc hub can contain a mix of service choices and quest choices.
  Dropping the whole hub would break “Show me your wares.”
- A mission-giver hub is usually all `QuestImportant`; it disappears.
- A hub with only a non-quest “Leave” remains, which is harmless: the player can
  talk but cannot start the quest.

**Service fallback.** If testing shows that vendor/ripperdoc service choices are
also marked `QuestImportant`, add a service allow-list:

```text
Keep if:
  hub.title matches a known vendor/ripperdoc name, OR
  any choice.localizedName contains "wares", "cyberware", "buy", "sell",
  "install", "upgrade", "trade", "shop"
```

This is data-driven and must be verified in-game. Do not ship a blind “drop all
dialog hubs” filter; it will break ripperdocs.

**Our own dialogue.** If Neon Ascendancy later uses scene dialogue, tag its hubs
with a `NeonAscendancy` prefix/title and exempt them. Otherwise the filter will
remove our own quest choices.

### 4.7 What is preserved

| System | Mechanism | Why it survives |
| --- | --- | --- |
| Vendors | `VendorDataManager`, `*_default_on`, service mappins | No journal/quest filter touches them. |
| Ripperdocs | Vendor/ripperdoc UI + service dialog choices | Service fallback keeps non-quest choices. |
| Stashes | Device/apartment system, `Zzz07_PlayerStashVariant` | Kept mappin variant; no quest state. |
| Fast travel | `FastTravelSystem`, `FastTravelVariant`, `Zzz17_NCARTVariant` | Kept mappin variants; no quest filter. |
| Apartments | `ApartmentVariant`, `Zzz05_ApartmentToPurchaseVariant` | Kept; purchase/stash devices remain. |
| Ambient spawns | Communities/`*_default_on` | Sanitizer only repairs vendor presence on demand. |
| Fixers | `FixerVariant` kept | The person stays; gig calls/pins are blocked. |
| Drop points | `ServicePointDropPointVariant` | Kept. |
| Vehicle vendors | `Zzz01`/`Zzz02` | Kept. |

### 4.8 Idempotency and concurrency

- Run `Apply()` on load, era change, and sanitizer toggle. Do not run per frame.
- Guard with `m_applying: Bool`. If a request arrives while applying, set
  `m_applyAgain = true` and return.
- Never mutate the journal inside `OnJournalState`. Enqueue
  `SuppressEntryRequest` and apply it with
  `DelayScriptableSystemRequestNextFrame`.
- Re-check `IsDefined(player)` in every delayed callback.
- Register listeners once per attach. `OnRestored` can fire after `OnAttach`;
  use a field `m_listenersRegistered` and unregister in `OnDetach`.
- All writes are monotonic: `SetFact` only if the current value differs; journal
  only if `Active`; mappin only if `Active`.
- Re-running the same apply produces no additional changes.

### 4.9 What Tier 1 cannot do

- Stop an active quest phase. If the player is mid-Heist, mid-gig, or in a quest
  scene when the sanitizer activates, the scene may finish.
- Prevent a quest trigger area from starting a phase if the phase is not gated
  by the pin journal entry.
- Remove quest NPCs/vehicles that a phase already spawned.
- Undo world changes a quest already made.
- Guarantee that no quest scene ever starts again. Most quests wait on player
  interaction, calls, or journal state; starving those inputs stalls them, but
  it is best-effort.

Tier 2 (WolvenKit + ArchiveXL custom New Game quest phase, already deferred in
`docs/roadmap.md`) is the complete solution: remove the vanilla main/side/gig
phases from the quest graph, or replace the root quest resource with a sandbox
root. Do not pretend Tier 1 is equivalent.

---

## 5. Sandbox Sanitizer architecture

### 5.1 Modules

```text
module NeonAscendancy.Sandbox

  SandboxEra              enum (pure)
  SandboxConsistency      struct/bit flags (pure)
  SandboxFactSnapshot     struct (pure data)
  SandboxEraDetector      class/static pure functions
  SandboxPolicy           struct (pure: what to unlock/suppress)
  SandboxSanitizerSystem  extends ScriptableSystem (adapter/state)
  SandboxJournalAdapter   class (journal/mappin calls)
  SandboxHooks            redscript wrappers
```

Keep the era detector and policy pure. The `ScriptableSystem` is a thin adapter
that reads facts, calls the pure functions, and applies the resulting policy.

### 5.2 Persistent state

Follow `docs/versioning.md`. Keep the save footprint tiny.

```redscript
public class SandboxSanitizerSystem extends ScriptableSystem {
  @default(SandboxSanitizerSystem, 1)
  private persistent let m_schemaVersion: Int32;

  private persistent let m_enabled: Bool;
  private persistent let m_era: Int32;              // SandboxEra as Int32
  private persistent let m_lastAppliedEra: Int32;
  private persistent let m_cityUnlockApplied: Bool;
  private persistent let m_campaignSuppressed: Bool;
  private persistent let m_johnnySuppressed: Bool;
  private persistent let m_housingUnlockApplied: Bool;

  // In-memory only; rebuilt on load.
  private let m_suppressedHashes: array<Uint32>;
  private let m_listenersRegistered: Bool;
  private let m_applying: Bool;
  private let m_applyAgain: Bool;
  private let m_playerAttachedCallbackID: Uint32;
}
```

Do **not** persist `String`, `Variant`, `ResRef`, or arrays of those. A hash
array is in-memory; the journal can be re-scanned.

`m_enabled` defaults to `false` in a new save. The player enables the sandbox
from the entry menu. On load, if enabled, apply. If the player loads without the
mod installed, persisted data is stripped; a reinstall starts from defaults and
re-applies. Document that.

### 5.3 Lifecycle

```text
OnAttach:
  register player-attached callback
  register journal listeners only when enabled (or register always and no-op)
  if WasRestored(): ScheduleApply(1.0)

OnPlayerAttach(request):
  ScheduleApply(1.0)

OnRestored(saveVersion, gameVersion):
  if m_schemaVersion < CURRENT: Migrate()
  ScheduleApply(0.5)

OnDetach:
  unregister player callback
  unregister journal callbacks
  cancel pending apply

ScheduleApply(delay):
  DelayScriptableSystemRequestNextFrame(n"NeonAscendancy.Sandbox.SandboxSanitizerSystem",
    new SandboxApplyRequest())

OnApplyRequest:
  if m_applying: m_applyAgain = true; return
  m_applying = true
  Apply()
  m_applying = false
  if m_applyAgain: m_applyAgain = false; ScheduleApply(0.0)
```

`DelayScriptableSystemRequestNextFrame` is available on `DelaySystem`
(`refs/cyberpunk/orphans.swift:12148-12156`). Use next-frame, not `0.0`
`DelayEvent`, to avoid running inside the current journal callback.

### 5.4 Apply pipeline

```text
Apply():
  if !IsDefined(player): return
  if !CanApplyDestructive(): ScheduleApply(2.0); return

  let snapshot = ReadFacts()
  let verdict = SandboxEraDetector.Classify(snapshot)
  let policy = SandboxPolicy.For(verdict, m_enabled, userOptions)

  if policy.UnlockCity:
      EnsureCityUnlocked(verdict)

  if policy.SuppressCampaign:
      SuppressJournal()
      SuppressTracking()
      SuppressMappins()

  if policy.SuppressJohnny:
      SuppressJohnny()

  if policy.EnsureWorldPresence:
      ProbeAndRepairVendorPresence()
      ProbeAndRepairHousing()

  m_era = verdict.Era
  m_lastAppliedEra = verdict.Era
  ShowHudNotice(verdict)
```

`CanApplyDestructive`:

```redscript
private final func CanApplyDestructive() -> Bool {
  let player = GameInstance.GetPlayerSystem(this.GetGameInstance()).GetLocalPlayerMainGameObject();
  if !IsDefined(player) { return false; };
  let scene = GameInstance.GetSceneSystem(this.GetGameInstance()).GetScriptInterface();
  if scene.IsEntityInScene(player.GetEntityID()) { return false; };
  if scene.IsRewindableSectionActive() { return false; };
  return true;
}
```

This is the single most important safety gate. Deactivating a journal entry or
removing a status effect during a scene can soft-lock the scene.

### 5.5 Hooks (redscript 1.x, Codeware-free)

| Hook | Type | Purpose |
| --- | --- | --- |
| `PhoneSystem.OnTriggerCall` | `@wrapMethod`, private scripted | Drop incoming quest/fixer calls. |
| `InteractionUIBase.OnDialogsData` | `@wrapMethod`, protected cb | Filter `QuestImportant` choices. |
| `WorldMappinsContainerController.CreateMappinUIProfile` | `@wrapMethod`, public scripted | Deny quest/gig mappins on world map. |
| `MinimapContainerController.CreateMappinUIProfile` | `@wrapMethod`, public scripted | Deny quest/gig mappins on minimap. |
| `WorldMapMenuGameController.UpdateTrackedQuest` | `@wrapMethod`, private scripted | Clear tracked vanilla quest. |
| `QuestTrackerGameController.UpdateTrackerData` | `@wrapMethod`, private scripted | Clear tracked vanilla quest on HUD. |
| `hudJohnnyController.OnPlayerAttach` | `@wrapMethod`, protected cb | Hide Johnny tour HUD. |
| `PlayerSystem` callbacks | `@addMethod` / system | Detect load/attach. |

Do **not** wrap native functions (`JournalManager.TrackEntry`,
`MappinSystem.SetMappinActive`, `QuestsSystem.SetFact`, etc.). The project skill
forbids it. Call them from the system instead.

### 5.6 Performance

- Journal scan: only on load, era change, or sanitizer toggle. About 80 active
  quests; negligible.
- Mappin scan: only when the map opens or after a journal change. About 400
  mappins; one pass, not per frame.
- Fact reads: ~15 per apply; negligible.
- Hook wrappers: O(1) per call; the dialog wrapper scans only the hubs currently
  being shown (usually 1–3).
- No SQLite, no world scans, no per-frame `GetFact` loops.

### 5.7 Failure modes and mitigations

| Failure | Mitigation |
| --- | --- |
| Applied mid-scene → soft-lock | Defer while `IsEntityInScene` / rewindable section active. |
| Journal callback re-entrancy | Never mutate inside callback; next-frame request + `m_applying`. |
| Hides vendors/ripperdocs | Deny only quest/gig mappin variants; service fallback in dialog filter. |
| Hides our own missions | Path/prefix allow-list; keep our mappin variants out of the deny list. |
| Johnny passenger remains | Tier 2 or verified fact; do not blind-despawn. |
| Quest phase continues | Accept Tier 1 limitation; document; plan Tier 2. |
| Save without mod strips state | Re-apply on reinstall; document. |
| Re-locks a post-Heist save | Monotonic writes only; never set `watson_prolog_lock = 1`. |

---

## 6. CET in-game verification playbook (10 minutes)

**Warning:** These snippets mutate a save. Use a **copy** of a save, not the
only copy. CET is a dev tool here, not a mod dependency. Do not run these on a
save you cannot lose. Close the game after the test and restore the backup.

### 6.1 Prep

1. Install CET as a dev-only tool (not shipped).
2. Load the test save.
3. Open the CET console.
4. Run the fact snapshot; copy the output.

### 6.2 Snippet A — fact snapshot

```lua
local names = {
  "watson_prolog_lock", "watson_prolog_unlock",
  "q000_done", "q001_done", "q001_active",
  "q003_done", "q004_done",
  "q005_start", "q005_active", "q005_done",
  "q101_active", "q101_done",
  "q101_enable_activities_flat", "q101_enable_side_content",
  "q112_done", "q115_point_of_no_return", "q115_done", "q116_done",
  "q201_done", "q202_done", "q203_done", "q204_done",
  "ep1_installed", "ep1_standalone", "ep1_active", "ep1_side_content",
  "q301_00_done", "q301_active", "q301_done", "q302_done",
  "johnny_on", "johnny_off", "johnny_default_on",
  "isPlayerPossessedByJohnny"
}

local qs = Game.GetQuestsSystem()
for _, n in ipairs(names) do
  print(string.format("%-34s %d", n, qs:GetFactStr(n)))
end
```

### 6.3 Snippet B — classify the save

```lua
local qs = Game.GetQuestsSystem()
local function f(n) return qs:GetFactStr(n) end

local era
if f("ep1_standalone") > 0 then
  era = "PLStandalone"
elseif f("q201_done") > 0 or f("q202_done") > 0 or
       f("q203_done") > 0 or f("q204_done") > 0 then
  era = "PostStory"
elseif f("q115_point_of_no_return") > 0 or f("q116_done") > 0 then
  era = "Endgame"
elseif f("q005_done") > 0 then
  if f("q101_done") > 0 or f("q101_enable_side_content") > 0 or
     f("watson_prolog_lock") == 0 then
    era = "Act2"
  else
    era = "Interlude"
  end
elseif f("watson_prolog_unlock") > 0 then
  era = "Interlude"
elseif f("q001_done") > 0 then
  era = "Act1PreHeist"
elseif f("q005_active") > 0 or f("q001_active") > 0 or f("q000_done") > 0 then
  era = "Prologue"
else
  era = "Unknown"
end

print("ERA=" .. era)
print("IntroSkipped=" .. tostring(f("q001_done") > 0 and f("q000_done") == 0))
print("HeistSkipped=" .. tostring(f("q005_done") == 0 and
  (f("q101_done") > 0 or f("q101_enable_side_content") > 0)))
print("LockAlreadyLifted=" .. tostring(f("watson_prolog_lock") == 0 and
  f("q005_done") == 0))
```

### 6.4 Snippet C — minimal city unlock

Run on an Act 1 save copy, **not** on a post-Heist save.

```lua
local qs = Game.GetQuestsSystem()
local function set(n, v)
  if qs:GetFactStr(n) ~= v then
    qs:SetFactStr(n, v)
    print("SET " .. n .. " = " .. v)
  end
end

set("watson_prolog_lock", 0)
set("watson_prolog_unlock", 1)

-- Remove vehicle/combat/quest fast-travel locks and enable map fast travel.
local ft = Game.GetScriptableSystemsContainer():Get("FastTravelSystem")
if ft then
  ft:QueueRequest(RemoveAllFastTravelLocksRequest.new())
  local evt = FastTravelMenuToggledEvent.new()
  evt.isEnabled = true
  ft:QueueRequest(evt)
  print("FastTravel locks cleared")
else
  print("FastTravelSystem not found")
end
```

Then walk/drive to the Watson border; check:

- roadblock gone?
- NCART gate open?
- map still locked?
- non-Watson fast-travel points listed?

### 6.5 Snippet D — Act 2 content switches

Run only after C, on a copy. This is what may start gigs/fixers.

```lua
local qs = Game.GetQuestsSystem()
for _, n in ipairs({
  "q101_enable_activities_flat",
  "q101_enable_side_content"
}) do
  if qs:GetFactStr(n) == 0 then
    qs:SetFactStr(n, 1)
    print("SET " .. n .. " = 1")
  end
end
```

Retest:

- fast-travel points outside Watson?
- vendor/ripperdoc outside Watson?
- apartments?
- gig pins/calls? (These should be suppressed by the mod; in this raw test they
  may appear. That is expected.)

### 6.6 Snippet E — journal audit and destructive suppression

**Audit first** (safe, read-only):

```lua
local jm = Game.GetJournalManager()
local filter = JournalRequestStateFilter.new()
filter.active = true
filter.inactive = false
filter.succeeded = false
filter.failed = false

local ctx = JournalRequestContext.new()
ctx.stateFilter = filter

local quests = {}
jm:GetQuests(ctx, quests)
-- If your CET build returns the array instead of filling the out table:
-- quests = jm:GetQuests(ctx)
print("active quests: " .. tostring(#quests))
for _, q in ipairs(quests) do
  print(string.format("%s | %s | state=%s",
    tostring(jm:GetEntryHash(q)), q:GetId(),
    tostring(jm:GetEntryState(q))))
end

local tracked = jm:GetTrackedEntry()
print("tracked: " .. (tracked and tracked:GetId() or "nil"))
```

**Destructive suppression** (copy only):

```lua
local jm = Game.GetJournalManager()
local filter = JournalRequestStateFilter.new()
filter.active = true
filter.inactive = false
filter.succeeded = false
filter.failed = false

local ctx = JournalRequestContext.new()
ctx.stateFilter = filter

local quests = {}
jm:GetQuests(ctx, quests)

for _, q in ipairs(quests) do
  local id = q:GetId()
  if string.sub(id, 1, 6) == "quests" or
     string.sub(id, 1, 9) == "ep1/quest" then
    jm:ChangeEntryStateByHash(jm:GetEntryHash(q), 1, 1) -- Inactive, DoNotNotify
    print("SUPPRESS " .. id)
  end
end

if jm:GetTrackedEntry() ~= nil then
  jm:UntrackEntry()
  print("UNTRACKED")
end
```

Immediately check:

- journal empty of vanilla quests?
- tracker clear?
- map pins gone? (If not, the mappin layer is missing; see F.)
- phone calls still arriving? (See G.)
- vendors/ripperdocs still work? (See §2.4.)

### 6.7 Snippet F — mappin audit

```lua
local ms = Game.GetMappinSystem()
local mappins = {}
ms:GetMappins(gamemappinsMappinTargetType.Map, mappins)

print("map mappins: " .. tostring(#mappins))
for _, m in ipairs(mappins) do
  print(string.format("%s | variant=%s | quest=%s | %s",
    tostring(m:GetNewMappinID()),
    tostring(m:GetVariant()),
    tostring(m:IsQuestMappin()),
    m:GetDisplayName()))
end
```

Optional deny test for a few known quest variants (values from the enum):

```lua
local ms = Game.GetMappinSystem()
local mappins = {}
ms:GetMappins(gamemappinsMappinTargetType.Map, mappins)

local deny = {
  [25] = true,  -- DefaultQuestVariant
  [49] = true,  -- ExclamationMarkVariant
  [87] = true,  -- QuestGiverVariant
  [75] = true,  -- MinorActivityVariant
  [126] = true, -- Zzz06_NCPDGigVariant
  [66] = true,  -- HuntForPsychoVariant
}

for _, m in ipairs(mappins) do
  if deny[m:GetVariant().value] then
    ms:SetMappinActive(m:GetNewMappinID(), false)
  end
end
```

Do **not** deny `FastTravelVariant (51)`, service-point variants (95–107),
`ApartmentVariant (10)`, `Zzz05_ApartmentToPurchaseVariant (125)`,
`Zzz07_PlayerStashVariant (127)`, `Zzz08_WardrobeVariant (128)`, or
`Zzz01`/`Zzz02` vehicle purchase variants.

### 6.8 Snippet G — phone call audit

```lua
Observe("PhoneSystem", "OnTriggerCall", function(self, request)
  print(string.format("CALL caller=%s addressee=%s phase=%s player=%s",
    tostring(request.caller),
    tostring(request.addressee),
    tostring(request.callPhase),
    tostring(request.isPlayerTriggered)))
end)
```

Then wait for a fixer call. If the log shows `IncomingCall`, the wrapper policy
in §4.5 will drop it. Check that player-initiated calls still work.

### 6.9 Snippet H — Johnny audit

```lua
local qs = Game.GetQuestsSystem()
for _, n in ipairs({ "johnny_on", "johnny_off", "johnny_default_on",
                     "johnny_mirror", "isPlayerPossessedByJohnny" }) do
  print(n .. " = " .. tostring(qs:GetFactStr(n)))
end

-- Clear current relic-malfunction effects.
StatusEffectHelper.RemoveStatusEffectsWithTag(Game.GetPlayer(), "JohnnySickness")
print("Removed JohnnySickness effects")

-- Optional candidate test; observe before/after.
qs:SetFactStr("johnny_off", 1)
qs:SetFactStr("johnny_on", 0)
qs:SetFactStr("johnny_default_on", 0)
qs:SetFactStr("isPlayerPossessedByJohnny", 0)
print("Johnny candidate facts set")
```

Then:

1. Enter a car, alone.
2. Wait 60–120 seconds.
3. Look at the passenger seat.
4. Report whether Johnny appears.
5. Re-read the facts; record which changed.

If Johnny still appears, run the passenger audit while in the car:

```lua
local player = Game.GetPlayer()
local pid = player:GetEntityID()
local mf = Game.GetMountingFacility()

local single = mf:GetMountingInfoSingleWithIds(pid)
if single and single.parentId then
  print("vehicle=" .. tostring(single.parentId))
  local infos = mf:GetMountingInfoMultipleWithIds(single.parentId)
  for _, info in ipairs(infos) do
    local e = Game.FindEntityByID(info.childId)
    print(string.format("slot=%s child=%s entity=%s",
      tostring(info.slotId),
      tostring(info.childId),
      e and tostring(e:GetRecordID()) or "nil"))
  end
else
  print("Player is not mounted")
end
```

This tells you whether Johnny is a real mounted entity. If he is not in the
mounting list, he may be a visual proxy; facts are the only safe route, or Tier 2.

### 6.10 Snippet I — dialogue hub audit

The dialog data is a `Variant` on the `UIInteractions` blackboard. Dump it while
a conversation is open:

```lua
local bb = Game.GetBlackboardSystem():Get(GetAllBlackboardDefs().UIInteractions)
local v = bb:GetVariant(GetAllBlackboardDefs().UIInteractions.DialogChoiceHubs)
print(v)
```

`print(v)` dumps the struct. If your CET build can convert it, this prints a
compact summary:

```lua
local bb = Game.GetBlackboardSystem():Get(GetAllBlackboardDefs().UIInteractions)
local v = bb:GetVariant(GetAllBlackboardDefs().UIInteractions.DialogChoiceHubs)
local d = FromVariant(v)
if d then
  for i, hub in ipairs(d.choiceHubs) do
    print(string.format("HUB %d title=%s choices=%d", i, hub.title, #hub.choices))
    for j, c in ipairs(hub.choices) do
      print(string.format("  [%d] %s type=%s", j, c.localizedName, tostring(c.type)))
    end
  end
else
  print("FromVariant refused the struct; screenshot the print(v) output")
end
```

Use this to answer the critical question: **are vendor/ripperdoc service choices
marked `QuestImportant`?** If yes, the filter needs the service allow-list.

### 6.11 10-minute test matrix

| Minute | Save | Action | Expected | If not |
| --- | --- | --- | --- | --- |
| 0–1 | Act 1 copy | Snippet A + B | `Act1PreHeist`, `lock=1`, `unlock=0`, `q005_done=0` | Record every value; a nonzero `q005_done` means the save is not Act 1. |
| 1–2 | Act 1 copy | Snippet C | Roadblock/NCART open; no re-lock | Check `lock` value; if still 1, another writer re-set it. |
| 2–3 | Act 1 copy | Snippet D | Map/fast travel behaves like Act 2 | If not, fast-travel points are not registered; see §2.3. |
| 3–4 | Act 1 copy | Walk to non-Watson ripperdoc/vendor | Shop works | If missing, probe its `*_default_on`; do not set all. |
| 4–5 | Post-Heist copy | Snippet B + C (no-op expected) | `Act2`, no re-lock | If `lock` becomes 1, the sanitizer is not monotonic. |
| 5–6 | Act 1 copy | Snippet E audit | Active quests listed | If `GetQuests` returns nothing, the out-array binding differs; use the wiki listener pattern. |
| 6–7 | Act 1 copy | Snippet E suppress | Journal/tracker empty; vendors still work | If vendors break, the dialog/mappin filter is too broad. |
| 7–8 | Any | Snippet F | Quest/gig mappins visible; services/fast travel visible | If a service pin disappears, adjust the deny list. |
| 8–9 | Act 1 copy | Snippet G + wait | No incoming fixer call | If a call arrives, the wrapper is not installed; check `PhoneSystem` hook. |
| 9–10 | Post-Heist copy | Snippet H + car | Johnny absent, or facts identified | If he appears, the passenger system is not fact-gated; Tier 2. |

---

## 7. Open questions requiring in-game verification

1. **Johnny passenger switch.** Do `johnny_off = 1`, `johnny_on = 0`,
   `johnny_default_on = 0` stop the 2.2/2.3 passenger? If not, is there a hidden
   cooldown/spawn fact? This is the largest unknown.
2. **Fast-travel registration.** After `watson_prolog_lock = 0` in Act 1, are all
   non-Watson fast-travel points already registered, or does the open-world
   fast-travel phase need `q101_enable_activities_flat`? If they are missing,
   what request registers them?
3. **Vendor presence.** Are non-Watson vendor NPCs already spawned in Act 1, or
   do their `*_default_on` facts need to be set? Which vendors are intentionally
   closed by story outcomes and must not be reopened?
4. **Ripperdoc service dialogue.** Are “Show me your wares” / “Install cyberware”
   choices marked `QuestImportant`? If so, the dialog filter must use a service
   allow-list.
5. **Apartment unlock.** Does setting `dlc6_apart_*_purchased` alone register the
   apartment fast-travel point, stash, wardrobe, and bed, or must the apartment
   phase run? Does `*_purchase_possibility` need to be set?
6. **Journal state vs. quest phase.** Does `ChangeEntryStateByHash(Inactive)`
   on an active main quest stop its phase, or only hide it? What side effects
   occur on the next scene/trigger?
7. **Gig pin gate.** Does deactivating a gig POI pin prevent its district phase
   from starting, or can the trigger area start it anyway?
8. **EP1/meta quests.** Does `GetQuests` include all `ep1/quests` and
   `quests/meta` entries, or is `GetMetaQuests` required separately for a clean
   sweep?
9. **`q101_enable_activities_flat` early.** In an Act 1 save, does setting this
   fact advance `q101_p2_v_room` or trigger any scene if `q101_active` is 0?
10. **Johnny relic effects.** Does removing `JohnnySickness` once prevent
    reapplication, or does a quest/ambient system reapply it later? Is a status
    effect listener needed?
11. **`q001_ripperdoc_done`.** Is it safe to set in an Act 1 sandbox to skip
    Viktor’s tutorial, or does it change later Vik dialogue/scenes?
12. **Menu mid-untrack.** If the map is open when a vanilla quest is untracked,
    does `WorldMapMenuGameController` refresh cleanly, or does it need an explicit
    `UpdateTrackedQuest()` call?

---

## 8. Source ledger

### Local references (2.5 decompiled scripts)

- `refs/cyberpunk/orphans.swift:18132` — `QuestsSystem` fact API.
- `refs/cyberpunk/orphans.swift:688-702` — `gameinteractionsChoiceType`.
- `refs/cyberpunk/orphans.swift:8796-8826` — journal state/notify enums.
- `refs/cyberpunk/orphans.swift:7295-7306` — `gameJournalQuestType`.
- `refs/cyberpunk/orphans.swift:11039-11062` — phone call enums.
- `refs/cyberpunk/orphans.swift:41474-41491` — `questTriggerCallRequest`.
- `refs/cyberpunk/orphans.swift:11713-11785` — `GameInstance.GetMappinSystem/GetPlayerSystem/GetQuestsSystem/GetStatusEffectSystem/GetJournalManager`.
- `refs/cyberpunk/orphans.swift:12140-12156` — `DelaySystem` delay/callback APIs.
- `refs/cyberpunk/orphans.swift:22259-22353` — journal entry/quest types.
- `refs/cyberpunk/orphans.swift:23867-23873` — `ChoiceTypeWrapper`.
- `refs/cyberpunk/orphans.swift:41950-41955` — `DialogChoiceHubs` (see `ListChoiceHubData` at 56147).
- `refs/cyberpunk/orphans.swift:56134-56162` — `ListChoiceData` / `ListChoiceHubData`.
- `refs/cyberpunk/core/systems/journalManager.swift:2-94` — `JournalManager` API.
- `refs/cyberpunk/core/systems/phoneSystem.swift:83-105` — `OnTriggerCall`.
- `refs/cyberpunk/core/systems/playerSystem.swift:28-80` — Johnny possession fact.
- `refs/cyberpunk/core/systems/statusEffectSystem.swift:1-140` — `StatusEffectHelper`, tag removal.
- `refs/cyberpunk/core/systems/fastTravelSystem.swift:139-407, 547-670` — fast-travel locks, map state, requests.
- `refs/cyberpunk/core/systems/scriptableSystem.swift:1-15` — `OnAttach`/`OnDetach`/`OnRestored`.
- `refs/cyberpunk/core/gameplay/prereqs/ui/DialogueChoiceHubPrereq.swift` — dialog hub prereq.
- `refs/cyberpunk/cyberpunk/UI/interactions/interactionUIBase.swift:32-107` — dialog/HUD listener flow.
- `refs/cyberpunk/cyberpunk/UI/interactions/dialogUI.swift:57-59, 326` — `UpdateDialogsData`, `QuestImportant`.
- `refs/cyberpunk/cyberpunk/UI/fullscreen/map/worldMap.swift:240, 442-472` — tracked quest/map.
- `refs/cyberpunk/cyberpunk/UI/mappins/mappinsContainers.swift:43-110` — `WorldMappinsContainerController.CreateMappinUIProfile`.
- `refs/cyberpunk/cyberpunk/UI/mappins/mappinUIProfile.swift:28-32` — `MappinUIProfile.None()`.
- `refs/cyberpunk/cyberpunk/UI/widgets/minimap/minimap.swift:362` — `MinimapContainerController.CreateMappinUIProfile`.
- `refs/cyberpunk/cyberpunk/UI/quests/quest_tracker.swift:193` — `UpdateTrackerData`.
- `refs/cyberpunk/cyberpunk/UI/hud/custom/hud_johnny.swift` — Johnny tour HUD.
- `refs/cyberpunk/cyberpunk/player/player.swift:633-634, 983-1003, 4879-4906` — Johnny replacer, restrictions, relic effects.
- `refs/cyberpunk/cyberpunk/devices/UI/dataTerm/dataTermGameController.swift:38, 59` — NCART lockdown.
- `refs/cyberpunk/cyberpunk/devices/UI/ncartTimeTable/ncartTimetableGameController.swift:151-152` — NCART timetable lockdown.
- `refs/cyberpunk/cyberpunk/UI/fullscreen/vendor/vendorHubMenuGameController.swift:198, 423` — vendor/ripperdoc tutorial facts.
- `refs/cyberpunk/cyberpunk/UI/fullscreen/ripperdoc/ripperdoc.swift:476-480` — ripperdoc tutorial facts.

### Resource studies (2.31, not runtime)

- `axefrog/xf-studio/knowledge/main-story-state.md` — fact spine, writers/readers, point of no return, PL switches, character facts, hashes.
- `axefrog/xf-studio/knowledge/open-world-activities.md` — fixer tiers, gig phases, pin/call/text fallback, content locks.
- `axefrog/xf-studio/knowledge/quests-and-story.md` — facts as script interface, journal, ArchiveXL scope.
- `axefrog/xf-studio/knowledge/input-and-choices.md` — `DialogChoiceHubs`, `ListChoiceHubData`, choice flow.
- `axefrog/xf-studio/knowledge/npc-direction.md` — runtime dialogue hub construction, `OnDialogsData`.
- `axefrog/xf-studio/knowledge/places.md` — fast travel, apartments, service points, mappin variants.
- `hlky/Ghostline` q101 deep dive — `watson_prolog_unlock` set by `q101_j_01_concert`, `q101_enable_side_content` / `q101_enable_activities_flat` producers.
- `jackhumbert/let_there_be_flight/docs/design/world-boundaries.md` — `watson_prolog_lock` gates `lch_prolog_roadblocks`; `q001_ride_to_mb` sets 1, `q101` sets 0.
- `pharingWell/factlog/facts.txt` — 2.1 fact-name dump used for candidate names and vendor `*_default_on` lists.
- `nobody71004/RedSync/release/PL-QUEST-WHITELIST.md` — PL fact prefixes and quest paths.
- `main-story-facts.json` — exact FNV hashes for external save readers.

### Official / community

- CDPR Update 2.2 notes: Johnny passenger added after Act 1; not during combat/missions/other passenger.
- CDPR Update 2.3 notes: ask Johnny to leave; he disappears for a couple of days.
- CDPR Modding Docs: quest facts and files; journal state does not complete quests.
- RedModding quest ID reference: main/side/minor/gig/contract journal paths.
- Nexus “Remove Passenger Johnny” and “The Passenger - Feature Settings” descriptions: archive removal, crash reports, cooldown facts, 1–4 day selector.
- `djkovrik/CP77Mods` `Wannabe Edgerunner` `IsPrologueFinished` — `watson_prolog_unlock == 1` as prologue-finished test.
- `GreenManNK/Cyberpunk-2077-mod` NGPlus bugfix — `q101_enable_side_content` can become `2`.
- `IIHyperiionII/Cyberpunk2077` `AutoTrackQuestOnDoneFix` — example of wrapping journal tracking (note: it wraps native `TrackEntry`; this project should not).

---

## 9. Bottom line

- **Build the era detector first.** It is a pure function over ~20 facts and can
  be exhaustively tested without the game.
- **Unlock the city with `lock=0`, `unlock=1`, `activities_flat=1`,
  `side_content=1`.** Do not fake story completion.
- **Suppress at the edges:** calls, dialogue choices, mappins, tracking, journal
  state, Johnny HUD/effects. Keep service mappins and service dialogue.
- **Accept the Tier 1 limit:** journal state hides content but does not stop a
  running quest phase. Plan Tier 2 for a true campaign excision.
- **Verify Johnny passenger in-game before designing around it.** The provided
  scripts do not contain the 2.2/2.3 passenger system, and the public evidence
  points to a system that is not a single documented fact.
- **Use the CET playbook on save copies.** The fastest path to certainty is the
  fact snapshot + minimal unlock + mappin/dialog audit, not more static reading.
