# Research 0.4 — Option A: True Clean-Slate Night City Start

**Target:** Cyberpunk 2077 2.5, redscript 1.0.2 (Codeware-free), RED4ext 1.31.1 +
RedLib C++20 native core, ArchiveXL 1.28.11, TweakXL 1.12.2,
WolvenKit.CLI 10.0.0-beta.1 (Linux).
**Date:** 2026-11-24.
**Scope:** a separate **"Start Ascendancy"** main-menu entry that boots a custom
`.gamedef` + `.quest` + `.questphase` clean-slate Night City while vanilla
**New Game** (base + Phantom Liberty skip-ahead) stays 100% untouched.

**Evidence grades used below**

- **[V]** verified directly in this research session against the local 2.5
  install (decompiled `refs/cyberpunk` scripts, RED4ext.SDK headers,
  `cyberpunk2077_addresses.json`, extracted game archives, or a successful
  WolvenKit.CLI round-trip on Linux).
- **[R]** strong structural evidence from the 2.5 game resources, not yet
  confirmed at runtime (behavior is data-driven; the data was read, the
  runtime result still needs one in-game pass).
- **[C]** community knowledge from the redmodding wiki / published mod
  documentation.
- **[H]** hypothesis. Needs the in-game spike in §6 before it becomes a design
  dependency.

---

## 0. Executive summary

1. **Main menu entry is fully tractable Codeware-free.** The main-menu action
   list is a native `inkListController` (`itemLibraryID = "PauseButtonItem"`)
   inside `singleplayer_menu.inkwidget`; the scripted
   `SingleplayerMenuGameController.ShowActionsList()` is the verified hook
   point. Spawn a `PauseButtonItem` copy with `SpawnFromLocal`, dispatch a
   custom menu event, and add a scenario handler that routes into the existing
   **vanilla** `MenuScenario_Difficulty → LifePath → BodyType →
   CharacterCustomization → Stats → Summary` chain. **[V]**

2. **Lifepath screen is KEPT as an origin pick, not skipped.** The lifepath
   choice writes `CharacterCustomizationState.SetLifePath(t"LifePaths.*")`
   (native) and nothing else; the vanilla intro selection happens in the
   **root quest phase graph** (which we replace), not in the UI. Keeping the
   screen costs nothing and preserves `CharacterCustomizationState` invariants
   (the state is initialized on this very screen, line 28 of
   `characterCreationGenderBackstoryMenu.swift`). **[V]**

3. **Launch mechanism — recommended:** native **arm/disarm resource redirect**
   in our RED4ext plugin + pass-through to the vanilla `StartNewGame` flow:
   - redscript wraps `characterCreationSummaryMenu.OnOutroComplete` (scripted,
     hookable) and, only when the Ascendancy flag is set, calls
     `NeonAscendancy.Core.ArmAscendancy()` **immediately before** the vanilla
     `wrappedMethod()` (which calls native `StartNewGame(ccState)`).
   - The C++ arm step inserts
     `"base\quest\cyberpunk2077.gamedef" → "mod\neon_ascendancy\ascendancy.gamedef"`
     into `RED4ext::ResourceBank::resolvedPathMap` (SDK-exposed field with its
     own lock — the same path→path resolution table ArchiveXL's `.xl`
     `resource: link:` mechanism populates [C]).
   - Everything downstream (CharacterCustomizationState application, world
     boot, spawn resolution, quest-graph start) runs **unchanged vanilla
     engine code** on our custom resources. Vanilla New Game never arms the
     redirect, so it is preserved bit-for-bit.
   - Disarm on `MenuScenario_SingleplayerMenu.OnEnterScenario` and on plugin
     shutdown.
   - **Fallback (zero-native-risk):** static ArchiveXL `.xl` redirect of
     `ep1\quest\ep1_standalone.gamedef` → our gamedef + hide/replace the
     vanilla "skip to Phantom Liberty" tile. Base New Game stays untouched;
     the vanilla PL-skip entry is sacrificed (flagged as a user-visible
     trade-off, see §5). **[V for the pieces, H for the runtime insertion]**

4. **The clean-slate phase graph is fully mapped.** The vanilla root chain is:
   `cyberpunk2077.gamedef (mainQuests=[cyberpunk2077.quest], spawnPointTags=[#q000_spwn_start], world=base\worlds\03_night_city\03_night_city.world)`
   → `.quest` (Start → phase node `cyberpunk2077.questphase`) → root phase
   graph: Start → [`cp77_new_game > 0`] → hubs → `prologue.questphase` (q000–q005),
   plus inline node **[82]** which activates `additional_game_elements`,
   `bugfixing`, `sidequests`, `minorquests`. Node **[57]** is an unconnected
   EP1 chicken-test easter egg, not the CC finalize. The entire city-life
   layer hangs off `additional_game_elements.questphase` →
   `open_world_content.questphase` (29 phases) + `default_dialogs` +
   `holocall_initializers` + `persistent_content` (→ `mq000` = **H10 apartment**
   → `dlc6_apart` = purchasable apartments) + `internet_content` (ncity.pub,
   needed by our own UI). **[V]**

5. **Exact keep/exclude phase matrix is below (§3.3).** Excluded:
   `street_stories`, `open_world_minor_activities` (NCPD hustles),
   `thepassenger` (Johnny), the main-quest chain (`prologue`, `act_1`,
   `epilogue`, `final_boards`), `sidequests`, `minorquests`. Kept: vendors,
   ripperdocs, fast travel, NCART/metro, NCPD PreventionSystem,
   crowds/communities, traffic, Autofixer, H10 + purchasable apartments,
   fixers, radio, chats, city scenes, dynamic events, combat events, Delamain,
   glamdocs, internet, holocall initializers, default dialogs. **[V]**

6. **WolvenKit.CLI on Linux reproducibly compiles our custom
   `.gamedef` + `.quest` + `.questphase` into a valid `.archive`:**
   `convert serialize → edit JSON → convert deserialize → pack → extract →
   serialize` round-trip verified end-to-end in this session, content-exact.
   One caveat: `pack` logs "Oodle couldn't be loaded. Using Kraken.dll instead
   could cause errors" — the produced archive is still valid (buffers written
   uncompressed); validate in-game, and pack CR2W files only (never `.json`).
   **[V]**

7. **Critical risks** (§5): (a) the runtime `resolvedPathMap` insertion timing
   vs. the engine's gamedef resource cache, (b) whether a fresh boot without
   any story fact leaves some vendor/quest-gated city pieces inert (e.g. one
   `q000_done`-gated vendor), (c) the 2.2/2.3 passenger-Johnny system if the
   phase is merely omitted vs. gated, (d) starting inventory/money/car are not
   granted by any phase in clean-slate (design decision needed).

---

## 1. Evidence inventory (what was inspected where)

| Surface | Location | What was verified |
| --- | --- | --- |
| Pregame UI scripts | `refs/cyberpunk/cyberpunk/UI/fullscreen/pregame/` (2.5 bundle) | Scenario chain, `StartNewGame(ccState)` call site, `StartGameDefinition(cat, def, gender)`, lifepath/difficulty handlers, `PauseButtonItem`, list controller wiring |
| `inkISystemRequestsHandler` | `refs/cyberpunk/orphans.swift:45790-45839` | Native script surface: `GetGameDefCategories/GetGameDefinitions/GetWorlds/GetGenders/StartGameDefinition/StartWorld/StartNewGame` |
| `gameGameSessionDesc` | `refs/RED4ext.SDK/include/RED4ext/Scripting/Natives/gameGameSessionDesc.hpp` | Full struct layout incl. `mainQuests`, `questsFromMainGameDefinitions`, `characterCustomizationState`, `playerSpawnParams` |
| `gamePlayerSpawnParams` | SDK `Generated/game/PlayerSpawnParams.hpp` | `spawnTags` TagList + `useSpecifiedStartPoint` |
| `gsmGameDefinition` | SDK `Generated/gsm/GameDefinition.hpp` | `.gamedef` layout: `mainQuests`, `world`, `streamingWorld`, `worldName`, `spawnPointTags` |
| gsm state machine | SDK `Generated/gsm/*.hpp` | Opaque structs only; no method tables in SDK |
| AddressLib map | `<game>/bin/x64/cyberpunk2077_addresses.json` (1,118,540 symbols) | **0 hits** for `StartNewGame`, gsm states, `GameSessionDesc` — no linkable-symbol hook exists; internal functions must be pattern-scanned or reached through RTTI/vtables |
| RED4ext hooking API | SDK `Api/v1/Hooking.hpp`, `Detail/AddressHashes.hpp` | `hooking->Attach/Detach` by raw address; `UniversalRelocFunc` limited to ~267 RED4ext-internal hashes |
| Resource system | SDK `ResourceLoader.hpp`, `ResourceDepot.hpp` | `ResourceBank.resolvedPathMap` (+ dedicated `resolvedPathMapLock`), `resourceSwapList`, `ResourceDepot` archive scopes incl. `Mod = 6` |
| Vanilla gamedef/quest JSON | extracted `base\quest\cyberpunk2077.{gamedef,quest,questphase}`, `base\open_world\{open_world_test.*, phases\open_world_content.questphase}`, `base\quest\{default_dialogs,persistent_content,additional_game_elements,holocall_initializers}.questphase`, `mq000.*`, `dlc6_apart.questphase`, `ep1\quest\ep1.{gamedef,quest,questphase}`, `ep1_standalone.gamedef`, `ep1_open_world.*` | Exact resource wiring below; deserialized with WolvenKit.CLI from `basegame_4_gamedata.archive` + `ep1_2_gamedata.archive` |
| Main menu widget | `base\gameplay\gui\fullscreen\main_menu\singleplayer_menu.inkwidget` (basegame_1_engine) | `mainListVert` = `inkListController`, `itemLibraryID=PauseButtonItem`, `OnItemActivated/OnItemSelected` |
| `pregame_menu.inkmenu` / `menu.inkmenu` | basegame_1_engine | scenario ↔ inkwidget mapping (60 entries) |
| ArchiveXL bundle | `<game>/red4ext/plugins/ArchiveXL/Bundle/*.xl` | `QuestBaseScope.xl` (`cyberpunk2077.quest` scope = base + ep1_standalone quests); `resource: link:` = path→path symlinks |
| redmodding wiki | ArchiveXL resource-linking page, quest pages | `.xl` `link:` semantics confirmed; **no documented way** for the game to "discover" or "select" a custom `.gamedef` for New Game (native/internal behavior) [C] |

---

## 2. Main Menu "Start Ascendancy" entry (vanilla New Game preserved)

### 2.1 The verified vanilla New Game flow (2.5, EP1 installed)

```text
Main menu item "New Game"
  → MenuScenario_SingleplayerMenu.OnNewGame()
      if EP1 installed: SwitchToScenario(MenuScenario_ExpansionNewGame)   // base vs "skip to PL" pick
      else:             SwitchToScenario(MenuScenario_Difficulty)
  → MenuScenario_Difficulty ("singleplayer_menu_difficulty")
      difficultySelection.SetDifficulty(...)   // StatsDataSystem, applies immediately
      OnAccept → MenuScenario_LifePathSelection
  → MenuScenario_LifePathSelection ("character_customization_background" + "life_path_selection")
      characterCreationGenderBackstoryMenu.OnReleaseXxx:
        m_characterCustomizationState.SetLifePath(t"LifePaths.Nomad"|"StreetKid"|"Corporate")  // native
        SpawnEvent("OnAccept") → MenuScenario_BodyTypeSelection
  → MenuScenario_BodyTypeSelection ("gender_selection") → MenuScenario_CharacterCustomization
  → MenuScenario_CharacterCustomization ("player_puppet" + "character_customization")
      appearance / voice / body  → MenuScenario_StatsAdjustment
  → MenuScenario_StatsAdjustment ("statistics_adjustment")  → MenuScenario_Summary
  → MenuScenario_Summary ("character_customization_summary")
      characterCreationSummaryMenu.OnOutroComplete:
        system.FinalizeState()
        GetSystemRequestsHandler().StartNewGame(this.m_characterCustomizationState)   // NATIVE
```

Key facts **[V]**:

- `StartNewGame(state: ref<IScriptable>)` is `public final native` on
  `inkISystemRequestsHandler` (`orphans.swift:45825`) — cannot be wrapped from
  redscript, but **its call site** (`characterCreationSummaryMenu.OnOutroComplete`,
  line 168-178) is scripted and wrappable.
- The base-vs-PL gamedef choice travels **inside the CC state** via
  `SetIsExpansionStandalone(bool)` (`expansionNewGame.swift:97,108`); the
  native `StartNewGame` reads it. There is no third selector.
- `InitializeState()` is called on the **lifepath screen**
  (`characterCreationGenderBackstoryMenu.swift:28`) — so a flow that enters
  `MenuScenario_Difficulty` directly (like vanilla without EP1) initializes
  the CC system correctly.
- `m_characterCustomizationState` is `protected` on
  `BaseCharacterCreationController`; our wrapper runs inside
  `characterCreationSummaryMenu` (a subclass), so the exact same access the
  vanilla method uses is legal in the wrapper.

### 2.2 Button injection (Codeware-free, composable)

The main-menu action list is `Root/mainListVert`, an
`inkVerticalPanelWidget` whose `inkListController` spawns
`PauseButtonItem` library items. The scripted
`SingleplayerMenuGameController.ShowActionsList()` (`singleplayerMenu.swift:1000`)
is the safe post-list-decoration hook.

```redscript
@wrapMethod(SingleplayerMenuGameController)
protected func ShowActionsList() -> Void {
  wrappedMethod();                                  // vanilla items first
  // spawn an extra button copy into the menu list
  let widget: ref<inkWidget> = this.SpawnFromLocal(
    inkCompoundRef.Get(this.m_menuList), n"PauseButtonItem");
  // set the label text (exact text widget name inside the PauseButtonItem
  // library item is TBD at implementation time; one WK click on the item)
  // register activation:
  widget.RegisterToCallback(n"OnRelease", this, n"OnAscendancyButtonRelease");
}

protected cb func OnAscendancyButtonRelease(evt: ref<inkPointerEvent>) -> Bool {
  if evt.IsAction(n"click") || evt.IsAction(n"tap") {
    this.SpawnMenuInstanceEvent(n"OnStartAscendancy");
  };
}
```

Scenario handler (added to the existing scenario class):

```redscript
@addMethod(MenuScenario_SingleplayerMenu)
protected cb func OnStartAscendancy() -> Bool {
  NeonAscendancy.Ascendancy.SetPending(true);   // in-memory flag, NOT persisted
  this.CloseSubMenu();
  this.SwitchToScenario(n"MenuScenario_Difficulty");  // skip base/PL pick
}
```

Notes **[V]**:

- `SpawnFromLocal` from the widget's own library (`n"PauseButtonItem"`) is the
  same mechanism vanilla uses everywhere (`browserModsMenu.swift` etc.) — no
  new inkwidget resource needed, no conflicts with other mods.
- `SpawnMenuInstanceEvent` reaches the active scenario's `cb func` handlers,
  which is how all vanilla submenu buttons talk to their scenario; `@addMethod`
  `cb func` handlers on scenarios are picked up (established redscript
  pattern).
- The vanilla "New Game" item keeps its exact flow (incl. the EP1 picker) —
  zero changes to vanilla UI behavior.
- `MenuScenario_SingleplayerMenu.OnEnterScenario` (scripted) additionally gets
  a wrapper that (a) clears the Ascendancy pending flag and (b) calls
  `NeonAscendancy.Core.DisarmAscendancy()` — the redirect can then never leak
  into a vanilla New Game or a save load.

### 2.3 Lifepath screen: keep as origin pick

Decision: **keep** `MenuScenario_LifePathSelection` unchanged. Evidence:

- The only script-side effect is `SetLifePath(t"LifePaths.*")` on the CC state
  + telemetry (`characterCreationGenderBackstoryMenu.swift:62-90`). **[V]**
- The lifepath→intro mapping lives in the quest graph (the vanilla root phase
  routes lifepath into q000 intro scenes). Our root graph simply never reads
  it, so it becomes flavor data for Neon Ascendancy's own origin system
  (Nomad/Streetkid/Corpo starting bonuses). **[R]**
- Skipping the screen would leave `GetLifePath()` unset, which the summary
  menu displays and the engine may index on (spawn selection), for zero
  benefit. No evidence the screen breaks anything in a custom gamedef boot.

Difficulty screen is likewise kept (it writes `StatsDataSystem.SetDifficulty`
immediately and the CC summary reads it back).

---

## 3. Launching the custom `.gamedef` + `.quest` (vanilla New Game untouched)

### 3.1 What is known natively

- `game::GameSessionDesc` (SDK, size 0x1D0, **[V]**): `mainQuests`
  (`DynArray<MainQuestData>`: `questPath` + `questPathValid` +
  `additionalContentId`), `playerSpawnParams` (`gamePlayerSpawnParams` with
  `spawnTags`), `characterCustomizationState`
  (`Handle<game::ui::CharacterCustomizationState>`), and
  `questsFromMainGameDefinitions` — "Filled with quests from
  `ep1\quest\ep1.gamedef` and `ep1\quest\ep1_standalone.gamedef` on game load"
  (SDK comment, **[V]**). The engine therefore merges the ep1 gamedef quests
  into **every** session at game boot regardless of the chosen base gamedef —
  which is exactly what makes Dogtown systems available in a vanilla base New
  Game, and what we get for free in ours.
- `gsm::GameDefinition` (`.gamedef`, size 0x90): `mainQuests`, `world`,
  `streamingWorld`, `worldName`, `spawnPointTags` — all present in the
  deserialized vanilla files. **[V]**
- The AddressLib linker map has **no symbols** for `StartNewGame`, any
  `gsm::MenuState_*`, or `GameSessionDesc` consumers — there is no
  hash-resolvable hook into the native new-game code path. **[V]**
- RED4ext `hooking->Attach` takes raw addresses; `UniversalRelocFunc` only
  resolves RED4ext's ~267 internal hashes. Any direct native hook on the boot
  path needs a runtime pattern scan (2.5-pinned, checksum-pinned — feasible
  but needs the in-game spike). **[V]**
- `inkISystemRequestsHandler.StartGameDefinition(categoryId, gamedefId,
  genderId)` exists but takes **no** character customization state; the debug
  `new_game_menu` (reachable via `MenuScenario_NewGame`) boots a raw session
  with default appearance. It cannot preserve character creation. **[V]**
- Nothing in the wiki documents `.gamedef` discovery or selection; the base/PL
  choice is internal to the native `StartNewGame` implementation. **[C]**

### 3.2 Candidate mechanisms, ranked

| # | Mechanism | CC preserved | Vanilla NG untouched | Native risk | Verdict |
| --- | --- | --- | --- | --- | --- |
| 1 | **Arm/disarm `ResourceBank.resolvedPathMap` redirect of `base\quest\cyberpunk2077.gamedef` → our gamedef**, armed by our native `NeonAscendancy.Core.ArmAscendancy()` immediately before the vanilla scripted `StartNewGame` call site, disarmed on main-menu re-entry | Yes (vanilla boot on our resource) | Yes (redirect armed only for our flow) | Low-medium (map insertion timing + cache; SDK-exposed fields) | **RECOMMENDED** |
| 2 | Static ArchiveXL `.xl` redirect of `ep1\quest\ep1_standalone.gamedef` → our gamedef; replace the vanilla PL-skip tile with "Start Ascendancy" (both set `IsExpansionStandalone(true)`; ours re-labels + adds a fact) | Yes | Base NG yes; **PL skip-ahead sacrificed** | None (pure `.xl`) | FALLBACK (fastest to ship; visible vanilla change) |
| 3 | Native hook (pattern scan) on the internal gamedef-load/desc-build function; rewrite `mainQuests` when a flag is set | Yes | Yes | High (no symbols; scan + ABI guessing) | Last resort |
| 4 | `StartGameDefinition` debug path | **No** | Yes | None | Rejected (no CC) |
| 5 | Redscript-only "set PL flag" | Yes | No (steals PL path anyway) | None | Same as #2 minus relabel |

**Mechanism 1 detail (recommended):**

- RED4ext's `ResourceBank` exposes `resolvedPathMap: HashMap<ResourcePath,
  ResourcePath>` with a dedicated `resolvedPathMapLock`
  (`RED4ext/ResourceLoader.hpp:181,190`). This is the same path→path
  resolution table that ArchiveXL's `.xl` `resource: link:` feature populates
  ("when the game tries to read X, ArchiveXL points it at Y" — wiki, [C]).
- Our plugin adds two native globals via the existing `RTTI_DEFINE_GLOBALS`
  infra (`native/plugin/Main.cpp:861+`):
  - `NeonAscendancy.Core.ArmAscendancy()` — lock `resolvedPathMapLock`, insert
    `ResourcePath("base\\quest\\cyberpunk2077.gamedef") →
    ResourcePath("mod\\neon_ascendancy\\ascendancy.gamedef")`; set a bool.
  - `NeonAscendancy.Core.DisarmAscendancy()` — remove the entry (idempotent).
- redscript wrapper (exact call-site control):

```redscript
@wrapMethod(characterCreationSummaryMenu)
protected cb func OnOutroComplete(anim: ref<inkAnimProxy>) -> Bool {
  if NeonAscendancy.Ascendancy.IsPending() {
    NeonAscendancy.Core.ArmAscendancy();   // redirect armed for THIS boot only
    NeonAscendancy.Ascendancy.ClearPending();
  };
  wrappedMethod(anim);                     // vanilla FinalizeState + StartNewGame run untouched
}
```

- Disarm points: `MenuScenario_SingleplayerMenu.OnEnterScenario` wrapper +
  plugin shutdown hook. Save loads do not re-read the base gamedef (the
  session desc persists in the save), and the ep1 gamedef merge happens at
  process boot before any arm is possible, so no save-load path can observe
  the redirect. **[R for the load semantics, H for the insertion API]**

**Mechanism 2 detail (fallback):**

```yaml
# ArchiveXL link semantics (wiki-verified): the KEY is the real file served;
# the VALUES are the paths that redirect to it. Reading ep1_standalone.gamedef
# therefore serves our file:
resource:
  link:
    mod\neon_ascendancy\ascendancy.gamedef:
      - ep1\quest\ep1_standalone.gamedef
```

plus a redscript wrapper that hides the vanilla standalone tile on
`expansion_new_game_menu` and adds our own tile that sets
`SetIsExpansionStandalone(true)` + `na_ascendancy_origin` fact. Base New Game
is byte-identical; only the vanilla PL-skip entry changes behavior. Acceptable
only if the team accepts that trade-off (see §5.2).

**Rejected:** `StartGameDefinition` (no CC); direct gsm state-machine
injection (no reachable API, no symbols); `@replaceMethod` on any native
function (project rule).

### 3.3 The resources we ship

All three resources are proven buildable on Linux (§4).

**`mod\neon_ascendancy\ascendancy.gamedef`** (exact JSON skeleton, modeled on
the vanilla file — field-for-field verified **[V]**):

```json
{
  "$type": "gsmGameDefinition",
  "mainQuests": [
    {
      "Data": {
        "$type": "gsmMainQuest",
        "additionalContent": 0,
        "additionalContentName": { "$type": "CName", "$value": "None" },
        "questFile": {
          "DepotPath": { "$type": "ResourcePath", "$value": "mod\\neon_ascendancy\\ascendancy.quest" },
          "Flags": "Soft"
        }
      }
    }
  ],
  "spawnPointTags": { "$type": "redTagList", "tags": [ { "$type": "CName", "$value": "#q000_spwn_start" } ] },
  "streamingWorld": { "DepotPath": { "$value": "base\\worlds\\03_night_city\\_compiled\\default\\03_night_city.streamingworld" }, "Flags": "Soft" },
  "world": { "DepotPath": { "$value": "base\\worlds\\03_night_city\\03_night_city.world" }, "Flags": "Soft" },
  "worldName": "03_night_city"
}
```

- `#q000_spwn_start` is the engine-validated vanilla New Game spawn tag; it
  resolves to a real world spawn point (vanilla uses it every NG). **[V]**
- The JSON above is the semantic shape; in practice **derive the file by
  editing a serialized vanilla `cyberpunk2077.gamedef.json`** (keeps WK's
  handle graph intact — the verified §4 workflow), not by typing the skeleton
  from scratch.
- **Do not** list `ep1\quest\ep1.quest` here: the engine already merges
  `ep1.gamedef`'s mainQuests into every session desc at game boot (SDK comment
  on `questsFromMainGameDefinitions`). Double-listing risks double phase
  activation. Verify Dogtown liveness in the spike; if it turns out dead,
  add the explicit mainQuest entry then (see §5.3). **[R]**

**`mod\neon_ascendancy\ascendancy.quest`** — the same trivial 2-node shape as
vanilla (`questStartNodeDefinition` → `questPhaseNodeDefinition` with
`phaseResource = mod\neon_ascendancy\ascendancy.questphase`); build it from
the deserialized `cyberpunk2077.quest` template. **[V]**

**`mod\neon_ascendancy\ascendancy.questphase`** — a hand-built hub (input
`Start` → fact managers → teleport → phase nodes). Node types used are all
verified vanilla types: `questFactsDBManagerNodeDefinition` with
`questSetVar_NodeType` (exact-value sets), `questTeleportPuppetNodeDefinition`
with `questTeleportPuppetParamsV1.destinationRef` (NodeRef,
`useFastTravelMechanism` present), `questPhaseNodeDefinition` +
`questLogicalAndNodeDefinition`. **[V]**

### 3.4 The exact phase list

**Our hub includes (keep-list — exact depot paths):**

| # | Phase | Why |
| --- | --- | --- |
| 1 | `base\open_world\community\global_phase\open_world_global_commuinity_phase.questphase` | Crowds/communities (traffic is engine-driven by world sectors) |
| 2 | `base\open_world\vendors\open_world_vendors.questphase` | Vendors + ripperdocs (gates read `q101_enable_side_content`, which we set) |
| 3 | `base\open_world\phases\prolog_roadblocks\lch_prolog_roadblocks.questphase` (+ `kab_`, `nid_`) | Roadblock unlock mechanics; inert while `watson_prolog_lock = 0` |
| 4 | *(inline)* NCPD PreventionSystem init | 36× `questEventManagerNodeDefinition` (`managerName = "PreventionSystem"`) — copied inline from `open_world_content` node [8] |
| 5 | `base\open_world\vendors\vehicles_metaquest\phases\vehicles_metaquest.questphase` + `vehicles_metaquest_new.questphase` | Vehicle purchases / Autofixer offers |
| 6 | `base\open_world\fixers\open_world_fixers.questphase` | Fixer presence (no gigs — those live in street_stories) |
| 7 | `base\open_world\combat_events\open_world_combat_events.questphase` + `ce_living_city_pass.questphase` | Ambient gang combat / living city pass |
| 8 | `base\open_world\fast_travel\open_world_fast_travel.questphase` | Fast travel points |
| 9 | `base\open_world\phases\radio\open_world_radio.questphase` | Radio |
| 10 | `base\open_world\dynamic_events\open_world_dynamic_events.questphase` | World encounters |
| 11 | `base\open_world\city_scenes\open_world_city_scenes.questphase` | City scenes |
| 12 | `base\open_world\phases\chats\open_world_chats.questphase` | NPC chats |
| 13 | `base\open_world\phases\city_entities\city_entities.questphase` | City entities |
| 14 | `base\open_world\mini_world_stories\ow_mini_world_stories.questphase` | Ambient mini stories |
| 15 | `base\open_world\phases\autofixer_spots\autofixer_spots_poi.questphase` | Autofixer spots |
| 16 | `base\open_world\metro\night_city_metro_nge.questphase` + `ue_metro_main.questphase` (+ inline metro communities from `open_world_content` node [139]) | NCART metro (gates read `q101_enable_side_content` — we set it) |
| 17 | *(inline from node [142])* district interactive-object managers | Doors / interactive world |
| 18 | `base\open_world\scenes\ue_cats\wst_ue_cats.questphase` | Cats (2.2) |
| 19 | `base\open_world\delamain_taxi\phases\delamain_taxi.questphase` | Delamain taxi |
| 20 | `base\open_world\autodrive\autodrive.questphase` | Autodrive |
| 21 | `base\open_world\vendors\glamdocs.questphase` | Glamdocs (2.3) |
| 22 | `base\gameplay\gui\world\internet\internet_content.questphase` | ncity.pub pages (**our own mod's UI depends on this**) |
| 23 | `base\quest\default_dialogs.questphase` | Ambient NPC dialogue (pulls prostitutes scenes, mq033 tarot) |
| 24 | `base\quest\holocalls\holocall_initializers.questphase` | Phone/holocall system init |
| 25 | `base\quest\character_entries.questphase`, `base\quest\cyberpunk2077_metajournal.questphase`, `base\quest\glossary_entries.questphase`, `base\quest\hiding_av_loops.questphase`, `base\quest\loading_screens.questphase`, `base\quest\locations_entries.questphase` | Codex/meta journal/glossary/loading screens |
| 26 | `base\quest\persistent_content.questphase` | **Pulls `mq000.questphase` (H10 apartment: `apartment_on`, bed/stash/wardrobe/mirror/computer interactions) + `dlc6_apart.questphase` (all 4 purchasable apartments) + `tutorials.questphase` + air traffic/dancefloors/mirrors.** Quest-scoped sub-phases inside are pause-gated on story facts that stay 0. |

**Excluded (clean-slate removals):**

| Resource | Why excluded |
| --- | --- |
| `base\quest\main_quests\prologue\prologue.questphase` (q000–q005), `base\quest\main_quests\part1\act_1.questphase` (q101–q116), `base\quest\main_quests\epilogue\epilogue.questphase`, `final_boards.questphase` | The campaign. Root phase chain `[93] → prologue "Q000 Main"` is never wired in our graph |
| `base\quest\side_quests\sidequests.questphase`, `base\quest\minor_quests\minorquests.questphase` | Side/minor quest hubs (mq000 reached via persistent_content instead) |
| `base\open_world\street_stories\street_stories.questphase` | Zero fixer gigs |
| `base\open_world\minor_activities\open_world_minor_activities.questphase` | Zero NCPD scanner hustles |
| `base\open_world\passenger\phases\thepassenger.questphase` | Zero Johnny (omitted entirely, per requirement) |
| `base\quest\bugfixing.questphase`, `base\quest\additional_content` bugfix phases | Bugfix graph (quest-scoped) |
| `ep1\quest\main_quests\ep1_main_quests.questphase` | PL campaign. **Not** wired; ep1.quest auto-merge keeps Dogtown city-life (vendors/communities/gate) but the PL quest chain stays dormant because `q005_done` / `ep1_active` / `q301_*` all stay 0 |

### 3.5 Initial facts set by our root phase (exact, monotonic)

```text
watson_prolog_lock          = 0
watson_prolog_unlock        = 1
q101_enable_activities_flat = 1
q101_enable_side_content    = 1
```

These are the *recommended full-city unlock set* already vetted in
[`campaign-sanitizer.md`](campaign-sanitizer.md#22-minimal-and-recommended-unlock-sets).
They unlock NCART/data terms, roadblocks, and the Act-2 world-content switches
(needed by vendors/metro/vehicles gates) without setting any story-completion
fact. **Never set** `q000_done`, `q001_done`, `q005_done`, `q101_done`,
`q115_*`, `ep1_*`. Do not set `sts_loop_start` (keeps gig loops off) and do
not set `q001_show_sts_tut` / `ow_psychos_intro_done` (activity pins).

### 3.6 Spawn: Level 1 in V's H10 apartment

- gamedef `spawnPointTags = [#q000_spwn_start]` → engine-validated initial
  spawn (runs during load, invisible).
- Our root phase's Start chain teleports the player to the H10 apartment with
  `questTeleportPuppetNodeDefinition` using `destinationRef =
  #mq000_01_sm_apartment` — the apartment marker NodeRef used by
  `mq000_vs_apartment_interactions.questphase` (verified in the deserialized
  resource). World NodeRefs resolve globally, so the reference is valid from
  our own quest phase. **[R]**
- Fresh session = level 1, no story flags, no journal entries — nothing to
  clean. The `apartment_on` fact is managed by mq000 (present via
  persistent_content); verify it is `1` after boot in the spike (§6).
- **Open design decision:** starting outfit, starting weapon, starting eddies,
  and the starter car are normally granted by q000/q001/vehicles phases that
  we removed. Options: (a) accept an empty start, (b) add
  `questAddRemoveItem_NodeType` managers to our root phase (exact pattern
  verified in `open_world_test.quest` node [25]) + a vehicle grant, (c) set
  vehicle fact `carbought`-equivalent if a vanilla "starter car" fact exists.
  Recommend (b) with a minimal starter kit.

---

## 4. WolvenKit.CLI 10.0.0-beta.1 build feasibility on Linux — VERIFIED

Reproducible pipeline, exercised end-to-end in this session **[V]**:

```bash
WK=/home/suvikyi/.cache/neon-ascendancy/wolvenkit-10.0.0-beta.1/WolvenKit.CLI
export DOTNET_ROLL_FORWARD=Major

# 1. Extract template resources from the 2.5 archives (regex filters work):
$WK extract -o out -r '^base\\quest\\cyberpunk2077\.gamedef$' \
  '<game>/archive/pc/content/basegame_4_gamedata.archive'

# 2. CR2W -> JSON:
$WK convert serialize out

# 3. Edit the JSON (paths, tags, graph) ...

# 4. JSON -> CR2W (all three types verified: gsmGameDefinition,
#    questQuestResource, questQuestPhaseResource):
$WK convert deserialize <dir-with-jsons>

# 5. Pack ONLY the CR2W files (never the .json sidecars):
$WK pack -o out2 <dir-with-cr2w-files>

# 6. Integrity round-trip (content-exact in testing):
$WK extract -o rt out2/*.archive && $WK convert serialize rt
```

Round-trip results: `ascendancy.gamedef` (type `gsmGameDefinition`, questFile
`mod\neon_ascendancy\ascendancy.quest`, spawn tags, world refs all preserved),
`ascendancy.quest` (`questQuestResource`), `ascendancy.questphase`
(`questQuestPhaseResource`). Caveats:

- `pack` logs: `"Oodle couldn't be loaded. Using Kraken.dll instead could
  cause errors."` The archive was still produced and re-extracted cleanly
  (buffers stored uncompressed). Validate the packed archive in-game once;
  if the game rejects it, ship the three CR2W files unpacked under a REDmod
  `mods/` folder or use a Windows-hosted WK pack for Kraken compression.
- The game resource depot loads mod archives from `archive/pc/mod/`
  (`ArchiveScope::Mod = 6`, [V]); arbitrary top-level folder paths inside mod
  archives are legal (`archive_xl\`, `dlc\` precedents). Our
  `mod\neon_ascendancy\` prefix avoids all vanilla collisions.
- A version-control workflow matches the repo rules: keep **JSON sources** in
  `data/` (human-readable), build the CR2W/archive with a
  `tools/build-clean-slate.sh` step, ship the archive to
  `<game>/archive/pc/mod/` via `tools/deploy.sh`.

---

## 5. Risks, unknowns, and open questions

### 5.1 Runtime insertion of the redirect (mechanism 1) — [H]

The exact semantics of writing `ResourceBank.resolvedPathMap` from a third
plugin are not documented: whether resolution happens before or after the
resource cache, and whether the engine caches the base gamedef token from a
prior vanilla NG in the same process. Mitigations (in order):

1. Spike first: arm → vanilla NG → check which quest graph boots.
2. If caching interferes, also use the SDK-exposed `resourceSwapList` (the
   mechanism ArchiveXL uses to swap *already-loaded* resources) or evict the
   cached token before arming.
3. If direct map surgery proves unstable, drop to mechanism 2 (static `.xl`
   redirect; zero runtime risk) — the only cost is the vanilla PL-skip entry.

### 5.2 Vanilla PL-skip trade-off (only if mechanism 2 is used)

Mechanism 2 replaces the vanilla "skip to Phantom Liberty" new game with
Ascendancy. Base New Game stays untouched, and PL-skip is arguably redundant
in a mod whose premise is "campaign disabled" — but it IS a vanilla behavior
change. Needs explicit user sign-off before shipping; keep it as fallback
only.

### 5.3 Dogtown liveness in the clean-slate boot

The engine merges `ep1.gamedef` quests at game boot (SDK comment [V]), which
should bring Dogtown's open-world wiring (`ep1.questphase` →
`ep1_open_world.questphase` → vendors/communities/combat-zone gate). The PL
campaign chain inside is fact-gated and should stay dormant. Verify in the
spike: `ep1_installed > 0`, Dogtown vendors/communities alive, combat-zone
gate present, and **no** q301 hook/call on border approach. If Dogtown is
dead, add `ep1\quest\ep1.quest` as a second `mainQuests` entry in our gamedef
and re-test (watch for double-activation).

### 5.4 Quest-gated city pieces with clean facts

A few kept phases read story facts that we deliberately leave at 0:
- `open_world_vendors` reads `q000_done` once — possibly one vendor stays
  hidden. Probe: which vendor, and whether its `*_default_on` fact fixes it.
- `persistent_content`'s quest-scoped sub-phases are pause-gated; verify none
  activates in a clean save.
- `ue_metro_main` gates on `q101_enable_side_content` — satisfied by our
  unlock set.

### 5.5 Johnny passenger (2.2/2.3)

Omitting `thepassenger.questphase` removes the phase wiring, but the 2.2/2.3
passenger system's *facts* (names unknown; see
`campaign-sanitizer.md` §3.2) may still exist in a fresh session. With zero
Johnny-related story facts and the phase gone, no spawn is expected; confirm
with the passenger probe from the sanitizer playbook.

### 5.6 Starting inventory / money / car

No vanilla phase grants them in our graph. Design decision required
(§3.6). The mechanic (item manager nodes / vehicle manager nodes) is verified;
the content (which items) is a design choice.

### 5.7 Menu button label text widget

The exact text-widget path inside the `PauseButtonItem` library item needs one
WK inspection to name in `inkTextRef.SetText`; trivial, no risk.

### 5.8 Non-EP1 installs

If EP1 is not present, drop the ep1 expectations (§5.3) and note that the
auto-merge no-ops. Our base keep-list already contains no ep1 paths.

---

## 6. Implementation plan and in-game verification playbook

### 6.1 Build order

1. `data/clean-slate/ascendancy.gamedef.json`, `ascendancy.quest.json`,
   `ascendancy.questphase.json` sources + `tools/build-clean-slate.sh`
   (WK round-trip, §4) → `archive/pc/mod/neon_ascendancy.archive`.
2. Native: `ArmAscendancy` / `DisarmAscendancy` globals in
   `native/plugin/Main.cpp` (+ unit tests for the mapping logic).
3. Redscript: button spawn wrapper, scenario handler, `OnOutroComplete`
   wrapper, disarm-on-main-menu wrapper (`src/r6/scripts/NeonAscendancy/UI/`).
4. `tools/verify.sh` + `tools/verify-native.sh`, then deploy.

### 6.2 CET spike checklist (dev-only CET 1.38.1 is installed)

1. Main menu shows the extra button; vanilla New Game still boots the vanilla
   intro (unchanged behavior).
2. Start Ascendancy → full CC chain → boots `03_night_city`.
3. Facts after boot: `watson_prolog_lock=0`, `watson_prolog_unlock=1`,
   `q101_enable_activities_flat=1`, `q101_enable_side_content=1`,
   `apartment_on=1`, `ep1_installed` (if EP1), and `q000_done=q001_done=
   q005_done=q101_done=sts_loop_start=0`.
4. Journal: empty. Phone: silent. Mappins: vendors/ripperdocs/fast
   travel/NCART present; no quest/gig/NCPD-hustle pins.
5. Player is in H10 (level 1), bed/stash/wardrobe/mirror/computer usable;
   map shows the 4 purchasable apartments as purchasable.
6. Watson roadblocks absent; NCART data term resolves; metro rides work.
7. Vendors/ripperdocs transact; NCPD wanted system works (shoot a cop);
   crowds/traffic/gangs present day & night.
8. Autofixer sites + vehicle purchase flow open.
9. Dogtown (EP1): border gate state, vendors/communities inside, and **no**
   PL quest triggers when approaching the gate.
10. No Johnny anywhere (apartment mirror, passenger seat, tour HUD).
11. Vanilla NG after an Ascendancy NG in the same process still boots the
    vanilla intro (redirect disarmed — proves the arm/disarm scoping).
12. Save + reload the clean-slate run: world state persists, no vanilla quest
    resurrection, no redirect artifacts.

### 6.3 Acceptance matrix

| # | Check | Pass condition |
| --- | --- | --- |
| 1 | Vanilla NG (base) | 100% unchanged intro/flow |
| 2 | Vanilla NG (PL skip) | unchanged (mechanism 1) or documented replacement (mechanism 2) |
| 3 | Ascendancy NG | H10 spawn, level 1, open city + Dogtown, zero quests/gigs/hustles/Johnny/Watson-lock |
| 4 | Services | vendors, ripperdocs, fast travel, NCART, Autofixer, apartments, stash/wardrobe, internet pages |
| 5 | Ambience | crowds, traffic, gangs, NCPD prevention, dynamic events |
| 6 | Persistence | save/load stable; no vanilla content creeps in |
| 7 | Build | `tools/verify.sh` + WK round-trip clean on Linux |
