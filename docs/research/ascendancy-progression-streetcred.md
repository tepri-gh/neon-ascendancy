# Level-1 Clean-Slate Baseline & Street Cred Rework

**Status:** Research + design spec (no source changes, no game launch)
**Date:** 2026-11-24
**Scope:** Cyberpunk 2077 2.5, redscript 1.x, Codeware-free, Neon Ascendancy
**Related:** [`campaign-sanitizer.md`](campaign-sanitizer.md), [`native-db-architecture.md`](native-db-architecture.md), [`option-a-clean-slate-start.md`](option-a-clean-slate-start.md), [`../architecture.md`](../architecture.md), [`../roadmap.md`](../roadmap.md)

---

## 0. Executive Summary

A fresh Level 1 character can be made **100% functional** without `q000`/`q001`/`q005`, but only if the bootstrap deliberately replicates the handful of **capability facts, cyberware, items, vehicle, and apartment state** that the vanilla prologue normally grants.

The most important findings:

1. **The scanner itself works at Level 1** because `player_base_stats.tweak` already sets `BaseStats.HasCybereye = 1`. However, **optical zoom** and the **NCPD bounty link** come only from Kiroshi optics (`CanUseZoom`, `HasLinkToBountySystem`), which Vik installs in `q001_04_ripperdoc.scene`.
2. **A fresh character has no cyberdeck, no quickhacks, no hand cyberware, no armor cyberware, no pistol, no outer clothing, no money, no vehicle, and no crafting recipes** unless `q000`/`q001` grant them. The best starter cyberdeck the prologue grants is **`Items.AdvancedMilitechParalineMKICommon`** (Memory 5, EMP Overload + Blind + Overheat), not `Items.CyberdeckSplinter` (a tutorial/quest deck that `q001_apartment` removes).
3. **Vehicle summoning is hard-blocked** until `unlock_car_hud_dpad = 1` (`VehicleSystem.IsSummoningVehiclesRestricted`), and **phone HUD quick-slot hints** require `q000_started = 1`. Both are prologue facts (`q000`/`q001`); a clean-slate start must set them or wrap the UI checks.
4. **The H10 apartment's ambient scenes require `apartment_on = 1`** (`mq000_vs_apartment_interactions`). Only the `q001` wake/ride phases set it. Without it the apartment can appear "off" (no ambient interactions, TV/radio/elevator scene logic).
5. **Crafting works, but the craft book is empty** without the prologue. Ammo recipes are only added on `OnRestored` retrofits; a new clean-slate character needs explicit `AddRecipe` calls.
6. **Enemies scale 1:1 to player level** in every open-world district (`Character.ScaleToPlayerLevel`, multiplier `1.0`). Level 1 is viable in City Center, Pacifica, the Badlands, and (with a Dogtown spot-check) Dogtown. There are no hard skull-locked zones for ordinary open-world spawns.
7. **Vanilla Street Cred is effectively a gig/NCPD-hustle farm track.** The 206 NCPD scanner-hustle activities award **147–1,949 SC each** (`minor_activities.tweak`); because each activity has an equal-value normal/pacifist pair, a single playthrough can earn up to roughly **~98,800 SC** from scanner hustles alone. That reaches about SC 38 under the proposed curve, and adding gigs, quests, vehicle purchases, and achievements easily exceeds SC 50. Random bounty kills also award SC whenever the player has Kiroshi's bounty link.
8. **Street Cred has exactly one authoritative sink:** `PlayerDevelopmentData.AddExperience(..., gamedataProficiencyType.StreetCred, ...)`. All vanilla SC awards funnel through `PlayerPuppet.OnExperienceGained` → `AddExperience`. That makes a **single `@wrapMethod` on `AddExperience`** sufficient to suppress vanilla SC, with one optional `BountyManager.SetBountyFromID` wrap to zero the scanner's displayed bounty SC.
9. **Proposed rework:** native C++ `CredPolicy` owns an **Ascendancy Cred Point (ACP)** curve (0 → 215,430 across SC 1–50) and a source/cap table tied to founding, captures, defenses, missions, lieutenants, territory, notoriety, district dominance, and heat. Redscript only applies the target SC level and proportional bar through `SetLevel`/`AddExperience`. Character Level XP is preserved; Ascendancy missions replace the missing quest XP with scaled Level XP.
10. **Open design decisions** remain around starting cash/vehicle, whether to keep the NCPD bounty link at all, Dogtown access, existing-save rebasing, and tutorial policy. The entry mechanism is resolved by the companion Option A research as a custom `.gamedef`/`.quest`/`.questphase` redirect; see §10.

---

## 1. Method, Scope, and Evidence

### 1.1 What was inspected

- Repository docs: `AGENTS.md`, `docs/architecture.md`, `docs/roadmap.md`, `docs/research/campaign-sanitizer.md`, `docs/research/native-db-architecture.md`, `docs/research/option-a-clean-slate-start.md`.
- Current redscript coordinator: `src/r6/scripts/NeonAscendancy/Gameplay/AscendancySystem.reds`.
- Decompiled game scripts: `refs/cyberpunk/cyberpunk/**`, `refs/cyberpunk/core/**` (`.swift` extension, REDscript content).
- Plain-text TweakDB: `<game>/tools/redmod/tweaks/base/**` and `ep1/**`.
- Quest-phase ground truth extracted from `<game>/archive/pc/content/basegame_4_gamedata.archive` with WolvenKit CLI 10.0.0-beta.1, converted to JSON with `WolvenKit.CLI cr2w -s`, and inspected for `questSetVar_NodeType`, `questAddRemoveItem_NodeTypeParams`, `questEquipItemParams`, `questEnablePlayerVehicle_NodeType`, `questDeviceManager_NodeType`, and reward nodes.

### 1.2 Evidence markers used below

- **[V]** verified in local scripts, TweakDB, or extracted quest-phase JSON.
- **[I]** needs an in-game check; the static evidence is suggestive but not conclusive.
- **[D]** design decision proposed by this document, not vanilla behavior.

### 1.3 Constraints

- No `.reds`/`.cpp`/`.hpp`/`tools/`/`data/` edits.
- No Cyberpunk 2077 launch.
- The repo holds sources, scripts, and docs only; extracted quest JSON lives outside the repo and is not committed.

---

## 2. What the Vanilla Prologue Actually Grants

The prologue is the `base\quest\main_quests\prologue\prologue.questphase` chain (q000–q005) referenced by the vanilla root graph. This document audits the `q000` lifepath chain, `q001` ("The Rescue" / "The Ripperdoc" / "The Ride"), and `q005` ("The Heist") phases because that is where the baseline grants live. See [`option-a-clean-slate-start.md`](option-a-clean-slate-start.md) for the full root-phase graph and the keep/exclude matrix.

### 2.1 `q000` — lifepath prologue

From `q000_vr_tutorial.questphase`, `q000_kid.questphase`, `q000_corpo.questphase`, `q000_nomad.questphase`, and the `q000_*` scenes:

| Grant | Exact ID / fact | Evidence |
|---|---|---|
| Starter cyberdeck (best variant) | `Items.AdvancedMilitechParalineMKICommon` (add + equip to `AttachmentSlots.Splinter`) | `q000_vr_tutorial.questphase` [V] |
| Tutorial/quest decks | `Items.CyberdeckSplinter`, `Items.MilitechParaline` (also added/equipped; Splinter later removed by `q001_apartment`) | `q000_vr_tutorial.questphase`, `q001_apartment.questphase` [V] |
| Starter pistol | `Items.Preset_V_Unity` (and `Items.Preset_V_Unity_Cutscene` for scenes) | `q000_vr_tutorial.questphase` [V] |
| Starter clothes | `Items.Q001_TShirt`, `Items.Q001_Pants`, `Items.Q001_Shoes`; lifepath `Items.Q000_*` sets are removed | `q000_vr_tutorial.questphase` [V] |
| Starting cash | Lifepath-specific scene adds/subtracts (Corpo +700 and a large Lizzies remove; Nomad +1,000 then −1,000; Street Kid no comparable add); net starting cash is small | `q000_corpo.questphase`, `q000_corpo_04_lizzies_club.scene`, `q000_nomad_05_border_crossing.scene` [V] |
| Full RPG progression flag | `full_rpg_progression_on = 1` | `q000_kid/corpo/nomad.questphase` [V] |
| 2.0 new-game marker | `q000_patch_2_0_new_game = 1` | `q000.questphase` [V] |
| Prologue started | `q000_started = 1` | `q000.questphase` [V] |
| Prologue done | `q000_done = 1` | `q000.questphase` [V] |
| HUD hint state | `dpad_hints_visibility_enabled` toggled 0/1 | `q000` phases [V] |
| Ammo counter | `q001_hide_ammo_counter` toggled 0/1 | `q000` phases [V] |
| Radio/TV | `radio_on`, `tv_on` toggled | `q000` phases [V] |
| NCPD dispatch | `prevention_dispatcher_disabled` toggled 0/1 (ends 0) | `q000` phases [V] |
| Combat tutorial guards | `disable_combat_events`, `block_combat_scripts_tutorials`, `gmpl_*` facts | `q000` phases [V] |
| Cyberdeck tutorial programs | The `AdvancedMilitechParalineMKICommon` record itself carries `EMP Overload`, `Blind`, and `Overheat` in its program slots | `cyberdeck_instances_advanced.tweak:1554-1605` [V] |

**Important:** `q000_vr_tutorial` does **not** grant Kiroshi, hand cyberware, or armor cyberware. Those come from Vik in `q001`.

### 2.2 `q001` — The Rescue / The Ripperdoc / The Ride

| Grant / fact | Exact ID / value | Evidence |
|---|---|---|
| Tutorial/quest cyberdeck | `Items.CyberdeckSplinter` (the real starter deck is `AdvancedMilitechParalineMKICommon` from `q000_vr_tutorial`) | `q001_mission0.questphase`, `q001.quest.json` [V] |
| Starter pistol again | `Items.Preset_V_Unity` | `q001_mission0.questphase` [V] |
| Starter clothes | `Items.Q001_TShirt/Pants/Shoes`; removes all `Q000_*` lifepath clothes | `q001_mission0.questphase` [V] |
| Kiroshi optics | `Items.KiroshiOptics` equipped | `q001_04_ripperdoc.scene` [V] |
| Hand cyberware | `Items.PowerGripRare` equipped | `q001_04_ripperdoc.scene` [V] |
| Ripperdoc completion | `q001_ripperdoc_done = 1` | `q001_ripperdoc.questphase` [V] |
| Codex | `glossary_ripperdocs = 1` | `q001_ripperdoc.questphase` [V] |
| Phone D-pad unlock | `unlock_phone_hud_dpad = 1` | `q001_00d_leaving.scene` [V] |
| Vehicle + car D-pad unlock | `questEnablePlayerVehicle` enables `Vehicle.v_standard2_archer_hella_player`; `questEnableVehicleSummon enable=1`; `unlock_car_hud_dpad = 1` | `q001_03a_meet_jackie_downstairs.scene` [V] |
| Apartment ambient on | `apartment_on = 1` | `q001_01_wakeup.scene`, `q001_ride_to_mb.questphase` [V] |
| Dressing enabled | `q001_enable_dressing = 1` | `q001_apartment.questphase` [V] |
| Player in room | `q001_in_v_room = 1` | `q001_apartment.questphase` [V] |
| Apartment weapons state | `q001_weapons_not_taken = 1` | `q001_apartment.questphase` [V] |
| Bed enabled | `q001_apartment_bed_disabled = 0` | `q001.questphase` [V] |
| Watson lockdown | `watson_prolog_lock = 1` | `q001_ride_to_mb.questphase` [V] |
| Tutorials off | `disable_tutorials = 1` | `q001_ride_to_mb.questphase` [V] |
| SC tutorial gate | `q001_show_sts_tut = 1` | `q001_path_to_diner.questphase` [V] |
| Fast-travel points | Registers all Watson data terms | `q001_fast_travel_unlock.questphase` [V] |
| Quest rewards | `QuestRewards.q001_mission0` (1,460 Level XP + 167 SC), `q001_dex` (1,516 + 167 SC), `q001_wakako_street_cred` (1,000 SC) | `main_quests.tweak:14-105` [V] |
| Weapons/clothes during The Ride | Adds Baseball Bat, Carnage, Copperhead, Guillotine, Knife, Machete, Q000 clothes | `q001_ride_to_mb.questphase` [V] |
| Apartment device control | Force-teleports elevator 1, disables elevator 2, force-seals lift doors, force-closes blinds | `q001_apartment.questphase` [V] |

### 2.3 `q005` — The Heist

`q005` is not needed for baseline capability, but it contributes:

- More Level/SC rewards and gear.
- `q005_done` story marker, which some reward calculations read (`CalculateMinorActivityReward`, `CalculateStreetStoryReward`, equipment retrofixes). **Do not set `q005_done`** just to unlock content; it changes reward math and story state.
- Johnny/Relic state, which a clean-slate campaign must never enter.

### 2.4 What is safe to fake vs. what must not be touched

| Fact | Safe? | Why |
|---|---|---|
| `map_blocked = 0` | Yes | Pure UI/map gate. |
| `watson_prolog_lock = 0`, `watson_prolog_unlock = 1` | Yes | Traversal/sandbox switches; the sanitizer already does this. |
| `q101_enable_activities_flat = 1`, `q101_enable_side_content = 1` | Yes | Content-enable switches; sanitizer already does this. |
| `unlock_phone_hud_dpad`, `unlock_car_hud_dpad`, `initial_gadget_picked`, `dpad_hints_visibility_enabled` | Yes | HUD/controls only. |
| `q000_started = 1` | Yes with a caveat | Only read by phone HUD, autodrive, and quick-slot hint transitions in scripts. Native checks are not visible; verify in-game. |
| `full_rpg_progression_on = 1`, `q000_patch_2_0_new_game = 1` | Yes with a caveat | Set by every lifepath; likely enables full progression/2.0 new-game behavior. Native checks are not visible; verify in-game. |
| `apartment_on = 1`, `q001_in_v_room = 1`, `q001_enable_dressing = 1`, `q001_apartment_bed_disabled = 0` | Yes | Apartment/device state, not story completion. |
| `q001_ripperdoc_done = 1` + tutorial-passed facts | Yes | Skips Vik's tutorial; consistent with a pre-installed starter kit. Does not complete `q001`. |
| `q000_done`, `q001_done`, `q001_completed`, `q005_done`, `q101_done` | **No** | Story completion facts with quest-graph and reward-math readers. |
| `ep1_standalone`, `q302_done`, other PL story facts | **No** | PL/Dogtown story state; open design question. |

---

## 3. Level-1 Clean-Slate Capability Audit

### 3.1 Scanner / Kiroshi / cybereye

**Verified behavior:**

- `PlayerVisionModeController.VerifyActivation` blocks FocusMode/scanner when `!RPGManager.HasStatFlag(player, gamedataStatType.HasCybereye)` (`playerVisionModeController.swift:177`).
- `player_base_stats.tweak:504` sets `BaseStats.HasCybereye = 1` for the player record. So **the scanner works before Kiroshi**.
- `zoomTransitions.swift:236` and `:269` block zoom when `!HasStatFlag(gamedataStatType.CanUseZoom)`.
- `BaseOptics`/`KiroshiOptics` OnEquip grants:
  - `BaseStats.HasCybereye = 1`
  - `BaseStats.HasLinkToBountySystem = 1`
  - `BaseStats.CanUseZoom = 1`
  (`eyes_general.tweak:1-40`)

**Consequence:** A fresh Level 1 character can scan, but cannot optical-zoom or use the NCPD bounty link until Kiroshi is installed. In a clean-slate campaign, install **`Items.KiroshiOptics`** to restore zoom and the bounty-link scanner UI. If the rework zeroes bounty SC, the link still provides bounty money and scanner info.

**Recommendation:** Give and equip `Items.KiroshiOptics` in the baseline. The base tutorial record declares no humanity variant (the advanced Kiroshi variants use `Variants.Humanity1Cost`), and it is the canonical Vik item.

### 3.2 Cyberdeck / operating system / quickhacks

**Verified behavior:**

- `q000_vr_tutorial.questphase` adds and equips:
  - `Items.AdvancedMilitechParalineMKICommon` (real starter deck)
  - `Items.CyberdeckSplinter` (tutorial/quest deck)
  - `Items.MilitechParaline` (base deck)
- `q001_apartment.questphase` removes `Items.CyberdeckSplinter` after the rescue.
- `Items.AdvancedMilitechParalineMKICommon` (`cyberdeck_instances_advanced.tweak:1554-1605`) grants:
  - `BaseStats.Memory +5`
  - Program slots: `Items.EMPOverloadProgram`, `Items.BlindProgram`, `Items.OverheatProgram`
  - `Variants.Humanity14Cost` (inherited from `AdvancedBaseLowEnergyDeck`)
- `Items.MilitechParaline` is the lower-capacity base deck (Memory 4, no humanity variant in the record); it is a fallback if the player cannot afford 14 Humanity at very low level.
- `Items.CyberdeckSplinter` grants `HasCyberdeck` and `CanMalfunctionQuickHack` but has no Memory bonus and no installed quickhack programs (`base_splinters.tweak:61-90`).
- `q001_tbug_tutorial.questphase` grants `Items.PingProgram` separately.

**Consequence:** Without `q000`, a fresh character has no cyberdeck, no RAM bonus, and no quickhacks. The quickhack panel is empty/unavailable.

**OS-slot note:** the Operating System slot can hold a cyberdeck, a Sandevistan, or a Berserk. A Sandevistan/Berserk build is legitimate and has `HasCyberdeck = 0` by design. The capability-ensure check should grant a cyberdeck only when the OS slot is **empty**, not merely when `HasCyberdeck = 0`.

**Recommendation:** Give and equip `Items.AdvancedMilitechParalineMKICommon` when the OS slot is empty. If the player has a cyberdeck, optionally add `Items.PingProgram` to inventory so the player has a scouting hack; the deck has three slots filled, so Ping is a swap-in choice.

### 3.3 Hand cyberware / Smart Link / Power Grip

**Verified behavior:**

- `q001_04_ripperdoc.scene` equips `Items.PowerGripRare` (`HasPowerGrip = 1`).
- `player_base_stats.tweak:514` sets `HasSmartLink = 0` by default.
- Smart Link is not granted by `q001`; it is purchased from a ripperdoc.

**2.5 note:** the pre-2.0 "Ballistic Coprocessor" does not appear in the 2.5 plain-text cyberware records. The hand-slot baseline choices are **Power Grip** (power weapons) and **Smart Link** (smart weapons); arm replacements (Gorilla Arms, Mantis Blades, etc.) are a separate equipment area.

**Consequence:** A clean-slate player has no hand cyberware and cannot use smart-weapon linking. Power weapons do not require Power Grip to fire, but the item is part of the intended Vik baseline and improves the power-weapon handling loop.

**Recommendation:** Give and equip `Items.PowerGripRare`. The base tutorial record declares no humanity variant (advanced hand cyberware uses `Variants.Humanity2Cost`). If the player already owns a smart weapon, give `Items.AdvancedSmartLink_Tutorial_Common` instead, mirroring Vik's `GetAppropriateHandsTutorialCyberware` logic. At Level 1, Power Grip is the correct default.

### 3.4 Armor cyberware

**Verified behavior:**

- The `q001` ripperdoc flow can provide `Items.AdvancedBoringPlating_Q001` (17+ armor, 5 Humanity); the cyberware retrofix path also references `AdvancedBionicJointsCommon` and `AdvancedChargeSystemCommon` as free armor cyberware.
- The `q001_04_ripperdoc.scene` itself only equips Kiroshi, Power Grip, and the cutscene Unity; armor cyberware is a tutorial-stock/UI or retrofix behavior, not a quest-phase add.
- `AdvancedBoringPlating_Q001` inherits `AdvancedBoringPlatingCommon`, which grants 17 base armor + quality scaling (`integumentary_system_advanced.tweak:2448-2548`).

**Consequence:** A clean-slate Level 1 player has **no armor cyberware** and only the Q001 clothes (no armor stats). This is a significant survivability gap.

**Recommendation:** Give and equip `Items.AdvancedBoringPlating_Q001`. At Level 1, player Humanity is `21 + 3 × Level = 24`. The advanced starter cyberdeck costs 14, Boring Plating costs 5, and the tutorial Kiroshi/Power Grip records declare no humanity variants; even if those two are charged at their advanced counterparts' 1/2, the full kit totals 22, leaving 2. This is tight but matches the vanilla VR-tutorial loadout. If the player wants more cyberware at Level 1, swap to the base `Items.MilitechParaline` (no humanity variant) or delay Boring Plating.

### 3.5 Weapon, ammo, healing, grenades

**Verified behavior:**

- `q000_vr_tutorial.questphase` adds `Items.Preset_V_Unity`.
- `Items.Preset_V_Unity` is a normal Unity pistol preset, not the quest-only `Preset_V_Unity_Cutscene`.
- Ammo item: `Ammo.HandgunAmmo` (`ammo.tweak:65-82`).
- Healing: `Items.FirstAidWhiffV0` is granted by the VR tutorial and lifepath phases.
- Grenades: `Items.GrenadeFragRegular` is used by the VR tutorial.

**Recommendation:**

| Item | Quantity | Notes |
|---|---:|---|
| `Items.Preset_V_Unity` | 1 | Equip to the handgun slot. |
| `Ammo.HandgunAmmo` | 300 | Enough for several missions. |
| `Items.FirstAidWhiffV0` | 5 | Basic inhaler. |
| `Items.GrenadeFragRegular` | 2 | Basic frag. |
| `Items.Preset_Baseball_Bat_Default` | 1 | Optional melee fallback. |

### 3.6 Money

Vanilla starting money is small and lifepath-specific (typically a few hundred to ~1,000 eddies after the scene adjustments; the exact net varies by lifepath). A clean-slate org founder needs seed capital for ammo, healing, and a first contract.

**Recommendation [D]:** Grant **2,500 €$** once per new clean-slate character. This is enough for a few magazines, a Ripperdoc visit, and a first mission, but not enough to skip early progression. For an existing save, do not grant money.

### 3.7 Starter vehicle and summoning

**Verified behavior:**

- `VehicleSystem.IsSummoningVehiclesRestricted` returns true when `unlock_car_hud_dpad == 0` (`vehicleSystem.swift:82`).
- It also returns true when the player has no unlocked vehicles (`vehicleSystem.swift:97-99`).
- `q001_03a_meet_jackie_downstairs.scene` enables `Vehicle.v_standard2_archer_hella_player`, sets `questEnableVehicleSummon enable=1`, and sets `unlock_car_hud_dpad=1`.
- `questEnableVehicleSummon_NodeType` is a quest node, not a redscript-exposed function; the redscript-visible path is `VehicleSystem.EnablePlayerVehicle` + the `unlock_car_hud_dpad` fact.

**Consequence:** Without `q001`, the player cannot summon a vehicle even if one is enabled, because `unlock_car_hud_dpad` stays 0.

**Recommendation [D]:**

- Set `unlock_car_hud_dpad = 1`.
- Call `GameInstance.GetVehicleSystem(game).EnablePlayerVehicle("Vehicle.v_standard2_archer_hella_player", true)` once.
- Prefer the Archer Hella (`v_standard2_archer_hella_player`) because it is the canonical starter car and has a player variant. A neutral alternative is `Vehicle.v_standard2_thorton_galena_player` if the design wants to avoid Jackie's model.
- Verify garage state `SummonAvailable` in-game; if enabling alone does not refresh it, call the native refresh path or re-enter the garage.

### 3.8 Phone, HUD, quick slots

**Verified behavior:**

- `PhoneSystem` is a ScriptableSystem; it does not require a phone item (`phoneSystem.swift`).
- `newHudPhoneGameController.GameStarted()` returns `q000_started` (`newHudPhoneGameController.swift:83-89`).
- `TutorialActivated()` returns `dpad_hints_visibility_enabled` (`:91-97`).
- `quickSlotsTransitions` blocks the quick-slot hint when `q000_started && !dpad_hints_visibility_enabled` (`quickSlotsTransitions.swift:731`).
- `unlock_phone_hud_dpad` is set by `q001_00d_leaving.scene`.
- `initial_gadget_picked` is set in `player.swift:2541` when the first gadget is picked.

**Consequence:** Without `q000_started` and `unlock_phone_hud_dpad`, the phone's D-pad quick-slot UI can be hidden even though the phone opens. This is a subtle but real baseline gap. The phone itself opens; vanilla contacts (Jackie, Vik, etc.) are absent because they are added by journal/quest events, so Ascendancy must add its own contact later.

**Recommendation:** Set `q000_started = 1`, `unlock_phone_hud_dpad = 1`, `dpad_hints_visibility_enabled = 1`, and `initial_gadget_picked = 1`. Verify the phone HUD in-game; if setting `q000_started` causes native side effects, wrap the `GameStarted()` checks in the phone HUD, autodrive, and quick-slot classes instead.

### 3.9 Map, journal, fast travel

**Verified behavior:**

- `radialHubMenuGameController` disables the Map entry when `map_blocked` is set (`radialHubMenuGameController.swift:250`).
- `menuDataBuilder` computes map availability from `map_blocked` (`menuDataBuilder.swift:137`).
- Tarot is hidden until `q101_done` (`radialHubMenuGameController.swift:250`). The sanitizer explicitly says not to set `q101_done`; leave Tarot locked.
- `FastTravelSystem.IsFastTravelEnabledOnMap()` requires `m_isFastTravelEnabledOnMap` and no locks (`fastTravelSystem.swift:300-301`).
- `m_isFastTravelEnabledOnMap` is set when the fast-travel menu opens (`uiSystem.NotifyFastTravelSystem`, `fastTravelSystem.swift:586-590`).
- Data-term devices register their points on `ResolveGameplayState` (`dataTermDevice.swift:50-54`), independent of quests.
- `q001_fast_travel_unlock.questphase` pre-registers all Watson data terms; without it, points register when their devices stream in.

**Consequence:** The map works if `map_blocked=0`. Fast travel works with no locks, but only to data terms that have streamed in. The H10 ground-floor dataterm will register when the player exits the apartment; other districts unlock as visited. The Journal menu opens but is empty in a clean-slate save until Ascendancy adds its own entries.

**World-layer dependency:** fast travel, vendors, ripperdocs, Autofixer, NCPD PreventionSystem, crowds, and traffic live under `open_world_content.questphase` / `additional_game_elements`. The custom start must include those kept sub-phases (or their equivalents); the bootstrap facts alone do not start them. NCART/metro gates also read `q101_enable_side_content`, so include the metro phases if the campaign wants metro travel. The companion Option A research lists the exact keep-list (vendors, fast travel, Autofixer, metro, PreventionSystem, communities, traffic, and so on) in [`option-a-clean-slate-start.md`](option-a-clean-slate-start.md) §3.3–§3.4.

**Recommendation:**

- Set `map_blocked = 0`.
- Call `FastTravelSystem.RemoveAllFastTravelLocks(game)` on bootstrap (idempotent).
- Do not force-register all city points; let data terms self-register. If the design wants city-wide fast travel from frame 0, a curated `RegisterFastTravelPointsRequest` list is possible but requires valid `NodeRef`s for each dataterm and is best deferred.
- Leave Tarot locked; it is cosmetic and the sanitizer forbids faking `q101_done`.

### 3.10 Crafting

**Verified behavior:**

- `CraftingSystem` is attached and the craft book is initialized on player attach (`craftingSystem.swift:36-41`).
- `OnRestored` adds ammo recipes for existing saves (`craftingSystem.swift:60-66`, `:155-165`), but there is no equivalent new-game grant in the script.
- The only persistent recipe grants in script are the `OnRestored` ammo recipes and reward-based `AddRecipeRequest`s.
- `CraftBook.AddRecipe` is public (`craftingSystem.swift:2279`).

**Consequence:** A clean-slate character opens the crafting menu with no recipes (or, at best, only recipes delivered by a quest reward that no longer runs).

**Recommendation [D]:** On bootstrap, add:

- `Ammo.HandgunAmmo`
- `Ammo.ShotgunAmmo`
- `Ammo.RifleAmmo`
- `Ammo.SniperRifleAmmo`
- `Items.Craftable_Common_Unity`
- `Items.Craftable_Common_Knife`

Give `Items.CommonMaterial1` ×50 so the player can actually craft. Use `CraftingSystem.GetInstance(game).GetPlayerCraftBook().AddRecipe(...)` or the `AddRecipeRequest` queue.

### 3.11 Wardrobe, bed, shower, mirror, computer, radio/TV

| Device / system | Verified gate | Clean-slate action |
|---|---|---|
| Apartment door | No `q001` fact/device action found; it is a standard door with apartment clearance | Verify it opens from inside; no baseline fact needed. |
| Elevator 1 | `q001_apartment` force-teleports it to floor 0; no disable action | Use elevator 1 to leave; default state should work. |
| Elevator 2 | `q001_apartment` force-disables it; `mq000` ambient logic may also force it off | Do not force-enable; use elevator 1. |
| Stash | No `q001` gate; `mq000_stash` uses `mq007_skippy_stash`; `WardrobeInitFromStash` reads stash clothing | Verify stash UI; no baseline fact needed. |
| Wardrobe | No `q001` script gate; `WardrobeControllerPS.FirstInit` uses `WardrobeInitFromStash` | Set `q001_enable_dressing = 1`; leave `WardrobeInitFromStash` at 0 so the wardrobe imports stash clothing on first use. |
| Bed | `q001_apartment_bed_disabled` | Set `0` to keep the bed usable. Vanilla `q001_ride_to_mb` sets it to `1` during the ride; the clean-slate bootstrap deliberately overrides that. |
| Shower | No fact found in scripts | Verify in-game; likely no gate. |
| Mirror / appearance | No `q001` fact found in scripts | Verify in-game; the H10 mirror should open the in-game customization UI. |
| Computer / NETdir | `apartment_on` controls ambient scenes; `NETdir://ncity.pub` is a real desktop page in `browserController.swift:309`, and its pages come from `internet_content.questphase` | Set `apartment_on = 1` as a fallback; include `internet_content.questphase` in the custom start; verify the H10 computer has `m_internetMenu = true`. |
| Radio | `radio_on` | Set `1` for ambience; the player can toggle it. |
| TV | `tv_on` | Set `0`; the player can toggle it. |

### 3.12 H10 apartment ambient state

**Verified behavior:**

- `mq000_vs_apartment_interactions.questphase` waits for `apartment_on == 1` and `interior_manager_on == 0` before its ambient logic runs.
- `q001_01_wakeup.scene` sets `apartment_on` to 0 then 1.
- `q001_apartment.questphase` force-seals lift doors, force-disables elevator 2, and force-teleports elevator 1 to floor 0.
- Without `q001`, those force actions never run, so the apartment devices stay in their default state.

**Consequence:** `apartment_on = 0` can leave the apartment without its ambient interactions. `elevator_2` may still be force-off by the `mq000` ambient scene, but `elevator_1` is the normal apartment elevator and should work.

**Recommendation:** The clean-slate graph must include `persistent_content.questphase`, which pulls `mq000.questphase` (the H10 apartment interactions) and `dlc6_apart.questphase`. The companion Option A research uses the H10 spawn marker `#mq000_01_sm_apartment` — the same marker referenced by `mq000_vs_apartment_interactions` — for the initial teleport. `apartment_on` is expected to be managed by `mq000`; set it to `1` only as a fallback/self-heal if the first boot shows it at `0`. Set `interior_manager_on = 0` if it is not already. Do not force-enable elevator 2; use elevator 1. Verify the door, mirror, and shower in-game.

### 3.13 Enemy scaling and world level

**Verified behavior:**

- `base/gameplay/static_data/database/content_assignment/open_world.tweak` maps every district generic to `Character.ScaleToPlayerLevel`: Little China, Arasaka Waterfront, Northside, Downtown, Kabuki, Arroyo, Inland Avenue, Japan Town, Charter Hill, West Wind Estate, Coastview, North Oak, Wellsprings, Corporate Plaza, Vista del Rey, Glen, Rancho Coronado, and all four Badlands regions.
- `Character.ScaleToPlayerLevel` is a `CombinedStatModifier` that sets `PowerLevel = Player.PowerLevel × 1.0` (`characters/npcs/records/gameplay/gameplay.tweak:4-14`).
- `RPGManager.CalculatePowerDifferential` thresholds: `<= -6` IMPOSSIBLE, `-6..-3` HARD, `-3..2` NORMAL, `2..4` EASY, `>4` TRASH (`rpgManager.swift:1645-1659`).
- Therefore ordinary open-world enemies at Level 1 are Level 1 and display as NORMAL, not skull-locked.

**Caveats:**

- Named quest NPCs, bosses, and some scripted PL/Dogtown encounters can have fixed power levels. They are not present in a clean-slate save unless the mod spawns them.
- Dogtown: the PL expansion has its own content assignments and gate logic. No base `open_world.tweak` Dogtown generic was found. **[I]** Spot-check Barghest at Level 1; if some Dogtown areas are fixed-level, keep Ascendancy missions out of those cells until the player is ready.
- The mod's own lieutenants/bosses should use `Character.ScaleToPlayerLevel` plus a small `+1`/`+2` elite modifier, never a hard level. At Level 1, `+2` is still NORMAL/EASY and fair.

**Recommendation:** Mission tier should add enemy count, elite variants, and encounter complexity, **not** raw level. This keeps a high-SC/low-level player challenged but not stat-checked.

### 3.14 Movement, health, and base combat flags

The player record already grants the essential movement/combat flags without any quest:

- `CanCrouch = 1`
- `CanSprint = 1`
- `CanJump = 1`
- `HasDodge = 1`
- `HasCybereye = 1`
- `CanRemoveModsFromClothing = 1`

(`player_base_stats.tweak:504-560` [V])

Health, stamina, armor, and carrying capacity come from the player record, attributes, and level. Character creation sets attributes; Level 1 is the normal minimum. No prologue fact is required for movement, jumping, crouching, dodging, or basic combat. The only base-stat gaps are the item-granted flags covered above (`CanUseZoom`, `HasLinkToBountySystem`, `HasCyberdeck`, `HasPowerGrip`).

---

## 4. Recommended Level-1 Bootstrap

### 4.1 Design principle

Do not blindly grant a starter kit on every load. Use **capability ensure**:

- If the player already has a cyberdeck, do not replace it.
- If the player already has Kiroshi, do not duplicate it.
- If the player already has a vehicle, do not enable another.
- If the player already has a pistol, do not add a second.
- Grant money and clothes only once per clean-slate character.
- Set facts idempotently on every load; they are cheap and self-healing.

### 4.2 Bootstrap order

```text
0. Custom root phase (not the runtime system) starts the kept world layers:
   additional_game_elements -> persistent_content (mq000 H10),
   open_world_content (vendors, fast travel, Autofixer, PreventionSystem),
   internet_content (ncity.pub), holocall_initializers, default_dialogs.
   The runtime system below is a self-heal layer, not a replacement for this graph.
1. Verify game/player/system references.
2. Read persistent m_bootstrapVersion and m_isCleanSlate.
3. If clean-slate and not yet granted:
   a. Set facts (table 4.3).
   b. Ensure capabilities (table 4.4).
   c. Grant money (2,500 €$).
   d. Grant starter consumables/ammo.
   e. Add recipes and components.
   f. Enable starter vehicle.
4. If existing save:
   a. Set only missing traversal/HUD/apartment facts.
   b. Ensure essential capabilities (cyberdeck/Kiroshi/hand/armor/vehicle) only if absent.
   c. Do not grant money, clothes, or duplicate weapons.
5. Call FastTravelSystem.RemoveAllFastTravelLocks(game).
6. Sync Street Cred bridge (see §6).
7. Persist m_bootstrapVersion.
8. HUD notice: "Ascendancy baseline ready."
```

### 4.3 Facts to set

| Fact | Value | Why |
|---|---:|---|
| `map_blocked` | 0 | Map menu. |
| `watson_prolog_lock` | 0 | Lift Watson lockdown. |
| `watson_prolog_unlock` | 1 | Mark prologue traversal open. |
| `q101_enable_activities_flat` | 1 | Enable Act 2 open-world activities. |
| `q101_enable_side_content` | 1 | Enable side content switches. |
| `q000_started` | 1 | Phone HUD / autodrive / quick-slot hints. |
| `q000_patch_2_0_new_game` | 1 | 2.0 new-game marker. |
| `full_rpg_progression_on` | 1 | Full RPG progression flag. |
| `unlock_phone_hud_dpad` | 1 | Phone D-pad. |
| `unlock_car_hud_dpad` | 1 | Vehicle summoning. |
| `initial_gadget_picked` | 1 | Suppress gadget tutorial. |
| `dpad_hints_visibility_enabled` | 1 | HUD hints. |
| `disable_tutorials` | 1 | Suppress tutorial spam. |
| `levelup_tutorial` | 1 | Suppress level-up tutorial. |
| `fast_travel_tutorial` | 1 | Suppress fast-travel tutorial. |
| `fast_travel_tutorial_seen` | 1 | Same. |
| `street_cred_tutorial` | 1 | Suppress SC tutorial. |
| `q001_ripperdoc_done` | 1 | Skip Vik tutorial. |
| `ripperdoc_tutorial_seen` | 1 | Skip ripperdoc tutorial. |
| `tutorial_ripperdoc_slots` | 2 | Mark slots tutorial done. |
| `tutorial_ripperdoc_eyes_passed` | 1 | Prevent tutorial Kiroshi. |
| `tutorial_ripperdoc_hands_passed` | 1 | Prevent tutorial hand cyberware. |
| `tutorial_ripperdoc_armor_passed` | 1 | Prevent tutorial armor cyberware. |
| `q001_hide_ammo_counter` | 0 | Show ammo counter. |
| `apartment_on` | 1 (fallback) | H10 ambient logic; `mq000` normally manages it. Set only if boot shows 0. |
| `interior_manager_on` | 0 (fallback) | H10 interior manager. |
| `q001_in_v_room` | 1 | Apartment/fast-travel tutorial context. |
| `q001_enable_dressing` | 1 | Wardrobe interaction. |
| `q001_weapons_not_taken` | 1 | Leave apartment weapon state consistent. |
| `q001_apartment_bed_disabled` | 0 | Bed enabled. |
| `radio_on` | 1 | Apartment radio ambience. |
| `tv_on` | 0 | TV off by default. |

**Optional flavor:** `glossary_fixers`, `glossary_mercenaries`, `glossary_ripperdocs`, and `glossary_scavengers` can be set to 1 to populate the codex entries the prologue normally adds.

**Do not set `q001_show_sts_tut`:** leave it at default 0. The companion Option A research treats it as an activity pin; `disable_tutorials=1` and `street_cred_tutorial=1` are enough to suppress the SC tutorial.

**Do not set:** `q000_done`, `q001_done`, `q001_completed`, `q001_active`, `q005_done`, `q101_done`, `sts_loop_start`, any `q115_*` / `ep1_*` story fact, or any other story-completion fact.

> **Side-content note:** `q101_enable_activities_flat` and `q101_enable_side_content` are set for vendor/vehicle/metro/world-system compatibility (one vehicle offer directly reads `q101_enable_side_content`). The companion Option A graph excludes `street_stories.questphase` and `open_world_minor_activities.questphase` entirely, so no vanilla gigs or NCPD hustles start; the sanitizer's journal/mappin/phone suppression remains defense-in-depth for existing saves.

**Clean-slate-only:** `q001_weapons_not_taken`, `q001_apartment_bed_disabled`, `q000_patch_2_0_new_game`, and `full_rpg_progression_on` are forced only for a new clean-slate character. Existing saves already have the latter two from `q000`; re-setting them could trigger native retrofix/progression behavior. On an existing save, leave them as-is unless they are missing and the apartment is visibly broken.

### 4.4 Capability ensure

This is the concrete implementation of the "minimal starter kit" recommendation in [`option-a-clean-slate-start.md`](option-a-clean-slate-start.md) §3.6.

Check `StatsSystem` flags before granting:

| Capability | Check | Grant / action |
|---|---|---|
| Cyberdeck | OS slot empty (not merely `HasCyberdeck <= 0`; a Sandevistan/Berserk is a valid OS) | Give + equip `Items.AdvancedMilitechParalineMKICommon` if `HumanityAvailable` can absorb 14; otherwise use `Items.MilitechParaline`. |
| Quickhacks | Deck has slots; optional Ping | Give `Items.PingProgram` to inventory. |
| Cybereye/zoom/bounty | `CanUseZoom <= 0` or `HasLinkToBountySystem <= 0` | Give + equip `Items.KiroshiOptics`. |
| Hand cyberware | `HasPowerGrip <= 0` and `HasSmartLink <= 0` | Give + equip `Items.PowerGripRare`. |
| Armor cyberware | No integumentary item equipped | Give + equip `Items.AdvancedBoringPlating_Q001`. |
| Pistol | No handgun in inventory | Give `Items.Preset_V_Unity`. |
| Ammo | `Ammo.HandgunAmmo < 100` | Give 300. |
| Outer clothing | No chest clothing equipped | Give + equip `Q001_TShirt`, `Q001_Pants`, `Q001_Shoes`. |
| Healing | `FirstAidWhiffV0 < 3` | Give 5. |
| Grenades | `GrenadeFragRegular < 2` | Give 2. |
| Money | Clean-slate only, once | Give 2,500 €$ via `MarketSystem.Money()`. |
| Vehicle | `GetPlayerUnlockedVehicles` empty | `EnablePlayerVehicle("Vehicle.v_standard2_archer_hella_player", true)`. |
| Recipes | `KnowsRecipe` false | Add ammo/Unity/Knife recipes; give 50 `Items.CommonMaterial1`. |

**Exact API shapes (redscript 1.x):**

```redscript
let ts = GameInstance.GetTransactionSystem(game);
ts.GiveItem(player, ItemID.FromTDBID(t"Items.AdvancedMilitechParalineMKICommon"), 1);
ts.GiveItem(player, MarketSystem.Money(), 2500);

let equipment = EquipmentSystem.GetData(player);
if !equipment.IsEquipped(ItemID.FromTDBID(t"Items.AdvancedMilitechParalineMKICommon")) {
  equipment.EquipItem(ItemID.FromTDBID(t"Items.AdvancedMilitechParalineMKICommon"));
}

let craftBook = GameInstance.GetScriptableSystemsContainer(game)
  .Get(n"CraftingSystem") as CraftingSystem;
craftBook.GetPlayerCraftBook().AddRecipe(t"Ammo.HandgunAmmo");
craftBook.GetPlayerCraftBook().AddRecipe(t"Items.Craftable_Common_Unity");

GameInstance.GetVehicleSystem(game)
  .EnablePlayerVehicle("Vehicle.v_standard2_archer_hella_player", true);
```

> Exact signatures must be checked against the redscript 1.x compile in `tools/verify.sh`; the decompiled 0.5-era files use slightly different syntax in places.

### 4.5 Persistence and idempotency

- Persist `m_bootstrapVersion: Int32`, `m_baselineGranted: Bool`, `m_isCleanSlate: Bool`.
- On `OnRestored`, re-run fact setting and capability checks, but not money/clothes grants.
- On `OnPlayerAttached`, run once per session.
- Use `TransactionSystem.HasItem` and `EquipmentSystemPlayerData.IsEquipped` to avoid duplicates.
- If the player loads an existing save with better gear, leave it untouched.
- If the player uninstalls the mod, the grants remain in the save; that is acceptable.

### 4.6 Entry mechanism (resolved by companion research)

The clean-slate entry is researched separately in [`option-a-clean-slate-start.md`](option-a-clean-slate-start.md). Its recommended path is a **custom `.gamedef` + `.quest` + `.questphase`** that reuses the vanilla character-creation chain, redirects the root quest graph only for the Ascendancy entry, and starts the kept city-life layer while excluding the campaign, gigs, NCPD hustles, and Johnny. Vanilla New Game remains untouched.

This document's baseline list applies regardless of the exact arm/disarm mechanism:

- The custom root phase should set the safe facts and grant the starter kit directly where possible (quest `questAddRemoveItem`/`questEquipItem` nodes or the runtime system).
- The runtime `NeonAscendancy_BaselineSystem` is a **self-heal layer**: it repairs missing facts/capabilities on load and covers existing saves, but it cannot prevent `q000` from starting in a normal New Game.
- A save template remains a valid fallback if the native resource redirect proves unreliable, but it is a binary asset and conflicts with the repo's sources-only rule unless generated locally by the installer.

**Recommendation:** Follow the companion Option A entry design; keep this document's capability list as the acceptance criteria for the first boot. The companion root phase's four traversal facts (`watson_prolog_lock=0`, `watson_prolog_unlock=1`, `q101_enable_activities_flat=1`, `q101_enable_side_content=1`) are the minimum; the additional HUD/apartment/ripperdoc facts in §4.3 are baseline/UX and can be set by the same root phase or by the runtime self-heal.

---

## 5. Street Cred Engine Audit

### 5.1 Data model and flow

**Street Cred is a proficiency, not a separate system:**

- `gamedataProficiencyType.StreetCred` is one of the 20 proficiency types.
- `PlayerDevelopmentData.OnNewGame` initializes all proficiencies at `m_startingLevel = 1`, `m_startingExperience = 0` (`playerDevelopmentSystem.swift:48-55`, `:263-275`, `:542-550`).
- `StreetCred` max level is **50** (`proficiencies/base_values.tweak:18-28`).
- `PlayerDevelopmentData.AddExperience` is the single level-up/XP sink (`playerDevelopmentSystem.swift:552-607`).
- `SetProficiencyStat` writes `gamedataStatType.StreetCred` to the player (`:481-486`).
- `PlayerPuppet.OnExperienceGained` queues an `AddExperience` request for every `ExperiencePointsEvent` (`player.swift:2028-2032`).
- `ModifyProficiencyLevel` handles level-up notifications, stat updates, passive bonuses, achievements, and tutorial facts (`playerDevelopmentSystem.swift:355-417`).

**Important:** `RPGManager.AwardExperienceFromDamage` awards **skill proficiencies** (Strength/Reflexes/Cool/Intelligence/Technical), not Street Cred (`rpgManager.swift:1774-1924`). Random combat damage does **not** directly award SC.

### 5.2 Every vanilla SC award source

| Source | Exact mechanism | Approx amount | Evidence |
|---|---|---|---|
| Bounty completion | `BountyManager.CompleteBounty` queues `ExperiencePointsEvent(StreetCred)` if `HasLinkToBountySystem` | `m_streetCredAmount` from `power_level_to_bounty_cred_mult` | `bountyManager.swift:166-219` |
| Quest reward | `RPGManager.GiveReward` queues SC XP for `Proficiencies.StreetCred` reward entries | Reward-defined | `rpgManager.swift:2130-2270` |
| `q001_mission0` | `QuestRewards.q001_mission0` | 167 | `main_quests.tweak:45-75` |
| `q001_dex` | `QuestRewards.q001_dex` | 167 | `main_quests.tweak:14-43` |
| `q001_wakako_street_cred` | `QuestRewards.q001_wakako_street_cred` | 1,000 | `main_quests.tweak:88-105` |
| Vehicle metaquest | `Tier1..6VehicleReward` | 100 / 200 / 300 / 500 / 3,000 / 5,000 | `vehicle_metaquest.tweak` |
| Cyberpsycho (CCL) | `CCL_Encounter_*` | 100 each | `ccl_rewards.tweak` |
| Achievement | `i_am_maxtac_achievement` | 1,200 | `achievements.tweak:51` |
| NCPD scanner hustles | `ma_*_completion` reward records | **147–1,949 each; 206 activities; ~98,800 per playthrough** (412 records counting both normal/pacifist variants; ~197,700 if both are summed) | `minor_activities.tweak` |
| Bounty rewards | `BountyReward.Generic` / specific bounties | Curve/named | `bounty_rewards.tweak` |
| Street stories / gigs | `street_stories.tweak` | Reward-defined | `street_stories.tweak` |
| Side quests | `side_quests.tweak` | Reward-defined | `side_quests.tweak` |
| Main quests | `main_quests.tweak` | Reward-defined | `main_quests.tweak` |

**NCPD hustle farming math [V]:**

- 412 `ma_*_completion` and `ma_*_completion_pacifist` records contain `Proficiencies.StreetCred` (206 unique activities, each with a normal and a pacifist completion reward; the two variants have equal values).
- Values range from **147** (Little China filler) to **1,949** (`ma_bls_ina_se1_07_completion`).
- Up to one reward per activity: **~98,841 SC** from scanner hustles alone, before gigs, quests, bounties, vehicles, and achievements.
- That alone reaches about **SC 38** on the proposed ACP curve (SC 38 = 98,730 ACP). It is enough to skip most org progression in practice, and a normal gig/quest playthrough pushes it past SC 50.

**Bounty farming:** Any gang NPC with a wanted bounty record awards SC on kill when the player has Kiroshi's `HasLinkToBountySystem`. This includes random street gang members, not just NCPD scanner targets.

**Entry-graph note:** the companion Option A graph excludes `street_stories.questphase` (gigs) and `open_world_minor_activities.questphase` (NCPD hustles) entirely, so those sources never start in a clean-slate save. The `AddExperience` gate is still required as defense-in-depth for existing saves, achievements, vehicle purchases, and any quest reward that slips through.

### 5.3 Every vanilla SC consumer / gate

| Consumer / gate | Effect | Evidence |
|---|---|---|
| `StreetCred` stat | Written by `SetProficiencyStat`, read by UI and price curves | `playerDevelopmentSystem.swift:481-486` |
| Vendor buy discount | `Price.BuyPrice_StreetCred_Discount` adds `-0.01 × BaseStats.VendorBuyPriceDiscount` to the buy-price multiplier (≈1% reduction per point of the discount stat); the stat is driven by the `street_cred_to_vendor_discount` curve | `price_modifiers.tweak:1340-1350`, `player_proficiency_passives.tweak:255-265` |
| Autofixer vehicle offers | `unlockType = Vehicle.StreetCred`; UI text "unlocked by Street Cred" | `vehicleoffers.tweak:39,66`, `vehicleDetailsLogicController.swift:97-107` |
| Vehicle tiers | `VehicleTier1..7` requirements 6 / 12 / 19 / 26 / 34 / 42 / 50 | `street_cred_tiers.tweak:144-176` |
| Vendor stock templates | `MidStreetCredItem` >= 18, `HighStreetCredItem` >= 36; `StreetCredAvailability` records for districts/cyberdecks/hacks. No base vendor record in the inspected plain-text tweaks references these records by name; treat as native/legacy until verified. | `vendors/base_values.tweak:278-650` |
| Cyberdeck program stock | `SuicideLvl3Program` / `SuicideLvl4Program` vendor items require SC 40 (explicit `StatPrereq`) | `vendors/base_values.tweak:307-340` |
| Item requirement UI | Items can require a `StreetCred` stat; UI switches to a `StreetCred` requirement state when unmet | `inventoryItemDisplayController.swift:1190-1200` |
| Legendary treasure drops | `Prereqs.LegenaryTreasureDrop` requires SC 40 | `simple_prereqs.tweak:135-142` |
| Vendor hub UI | SC level and progress bar | `vendorHubMenuGameController.swift:347-403` |
| Radial hub UI | SC level and points | `radialHubMenuGameController.swift:138-141, 200-219` |
| Stats screen | SC progress and reward list | `statsMain.swift`, `statsStreetCredReward.swift` |
| Progression notifications | SC XP/level notifications | `progression_notification.swift:114-115` |
| Achievement | `YouKnowWhoIAm` at SC 50 | `playerDevelopmentSystem.swift:426-432` |
| Tutorial | `street_cred_tutorial` gated by `q001_show_sts_tut` | `playerDevelopmentSystem.swift:590-592` |
| Scanner bounty UI | Shows bounty SC reward and whether the player has the link | `NPCPuppet.swift:3530-3582` |
| Black market | No base SC-gated black-market vendor found | [V] absence |

**Important nuance:** Base-game ripperdoc cyberware stock is gated by **player level** (`LootPrereqs.PlayerLevel_Tier_*`), not Street Cred. SC affects cyberware **price**, not availability. The `StreetCredAvailability` records exist, but no base vendor record in the plain-text tweaks references them by name; treat them as native/legacy and verify in-game. This means a Street Cred rework should not promise "SC unlocks vanilla ripperdoc cyberware" unless it adds its own black-market gate.

### 5.4 Where to intercept

**Single authoritative gate:** `PlayerDevelopmentData.AddExperience`.

Why:

- All event-based SC awards go through `PlayerPuppet.OnExperienceGained` → `AddExperience`.
- `BountyManager`, `RPGManager.GiveReward`, and `AwardXP` all queue `ExperiencePointsEvent` to the player.
- `AwardExperienceFromDamage` does not touch SC.
- There is no other SC sink in the decompiled scripts.

**Recommended hooks:**

1. **`@wrapMethod(PlayerDevelopmentData) public final const func AddExperience(...)`**
   - If `type == StreetCred` and Ascendancy is active and `!m_allowCredXp` and `!isDebug`, return without calling `wrappedMethod` (allow debug commands to bypass).
   - This drops quest, gig, NCPD, vehicle, achievement, CCL, and random bounty SC in one place.
   - The Ascendancy bridge sets `m_allowCredXp = true` around its own `SetLevel`/`AddExperience` calls.

2. **`@wrapMethod(BountyManager) public final static func SetBountyFromID(...)`** (optional but recommended)
   - After `wrappedMethod`, if Ascendancy is active, set `bounty.m_streetCredAmount = 0` and re-apply it with `NPCPuppet.SetBountyObject(target, bounty)`.
   - This keeps the scanner UI honest: the player sees the money reward and 0 SC, not a SC reward that is silently dropped.
   - Do **not** wrap `CompleteBounty` per kill; `SetBountyFromID` is called once per bounty generation and is the cheaper, cleaner point.

3. **Optional `@wrapMethod(RPGManager) public final static func GiveReward(...)`**
   - If an NCPD job completion UI shows a false SC reward in an existing save, strip `Proficiencies.StreetCred` entries from the reward's `expArr` before queueing. Not needed for clean-slate because there are no NCPD jobs.

**Do not** wrap `AwardExperienceFromDamage`; it awards skill XP, not SC. Suppressing it would break combat skill progression.

> **Compile caveat:** the decompiled signatures are `public final const func AddExperience(...)` and `public final static func SetBountyFromID(...)`. The redscript 1.x wrappers must match the visibility, `const`, and `static` shape exactly. Compile-check both with `tools/verify.sh` before relying on them.

### 5.5 What vanilla SC suppression should *not* break

- **Vendor discount:** SC level still rises through Ascendancy awards, so the vanilla discount curve still applies.
- **Autofixer:** SC still unlocks vehicle tiers at 6/12/19/26/34/42/50.
- **Bounty money:** `BountyManager.CompleteBounty` still awards eddies and Level XP; only SC is zeroed.
- **NCPD heat:** `PreventionSystem` is independent of SC.
- **Achievement:** `YouKnowWhoIAm` still triggers at SC 50.
- **UI:** the SC bar/level still updates because the bridge uses `SetLevel`/`AddExperience`.

---

## 6. Ascendancy Street Cred Rework

### 6.1 Goals

1. Street Cred should represent **the player organization's public reputation**, not a tally of freelance gigs.
2. Random sidewalk kills and NCPD hustles must not bypass org progression.
3. SC should still integrate with vanilla vendors, ripperdocs (price), Autofixer, and UI.
4. SC should gate **org capabilities** (territory, crew, mission tier, corp founding, stock access, black market).
5. Character Level XP and skill proficiencies must remain a separate, healthy track.

### 6.2 Ascendancy Cred Points (ACP) curve

Use an **ACP** counter in the native sim. The vanilla `player_primary_level_to_xp` curve is baked into `tweakdb.bin` and is not present in the plain-text tweaks; bypass it entirely for leveling and use the vanilla curve only for the visual bar fraction.

**Curve formula for SC level `L` (cumulative ACP):**

```text
n = L - 1
ACP(L) = round_to_10( 1.5·n³ + 15·n² + 60·n )
```

Total to SC 50: **215,430 ACP**.

| SC | ACP total | ACP to next | Proposed unlock |
|---:|---:|---:|---|
| 1 | 0 | 80 | Found gang; 1 territory; T1 missions |
| 2 | 80 | 110 | Crew 1; basic black market |
| 3 | 190 | 170 | Max 2 territories |
| 4 | 360 | 220 | — |
| 5 | 580 | 280 | T1 contracts; crew 2; first lieutenant |
| 6 | 860 | 360 | Autofixer Tier 1 (vanilla) |
| 7 | 1,220 | 450 | — |
| 8 | 1,670 | 540 | Max 3 territories; T2 missions |
| 9 | 2,210 | 640 | — |
| 10 | 2,850 | 750 | Vanilla vendor discount (curve-driven; verify %) |
| 11 | 3,600 | 870 | — |
| 12 | 4,470 | 1,000 | Autofixer Tier 2 (vanilla); max 4 territories |
| 13 | 5,470 | 1,140 | — |
| 14 | 6,610 | 1,290 | — |
| 15 | 7,900 | 1,440 | Max 5 territories; T3 missions; corp shell |
| 16 | 9,340 | 1,600 | — |
| 17 | 10,940 | 1,780 | — |
| 18 | 12,720 | 1,970 | Lieutenant 2; crew 4; black-market cyberware |
| 19 | 14,690 | 2,150 | Autofixer Tier 3 (vanilla) |
| 20 | 16,840 | 2,360 | Found Corporation; stock trading |
| 21 | 19,200 | 2,570 | — |
| 22 | 21,770 | 2,780 | — |
| 23 | 24,550 | 3,020 | — |
| 24 | 27,570 | 3,250 | — |
| 25 | 30,820 | 3,490 | Max 7 territories; T4 missions; shorting |
| 26 | 34,310 | 3,750 | Autofixer Tier 4 (vanilla) |
| 27 | 38,060 | 4,020 | — |
| 28 | 42,080 | 4,290 | — |
| 29 | 46,370 | 4,570 | — |
| 30 | 50,940 | 4,860 | Max 9 territories; T4 contracts; elite lieutenants |
| 31 | 55,800 | 5,160 | — |
| 32 | 60,960 | 5,470 | — |
| 33 | 66,430 | 5,790 | — |
| 34 | 72,220 | 6,120 | Autofixer Tier 5 (vanilla) |
| 35 | 78,340 | 6,450 | Max 11 territories; T5 missions; hostile takeovers |
| 36 | 84,790 | 6,790 | — |
| 37 | 91,580 | 7,150 | — |
| 38 | 98,730 | 7,520 | — |
| 39 | 106,250 | 7,880 | — |
| 40 | 114,130 | 8,270 | Max 13 territories; T5 contracts; district perks |
| 41 | 122,400 | 8,660 | — |
| 42 | 131,060 | 9,050 | Autofixer Tier 6 (vanilla) |
| 43 | 140,110 | 9,470 | — |
| 44 | 149,580 | 9,880 | — |
| 45 | 159,460 | 10,300 | Max 15 territories; T6 missions; city-wide notoriety |
| 46 | 169,760 | 10,740 | — |
| 47 | 180,500 | 11,190 | — |
| 48 | 191,690 | 11,640 | — |
| 49 | 203,330 | 12,100 | — |
| 50 | 215,430 | — | Max 18–20 territories; T6 contracts; capstone; Autofixer Tier 7 |

**Pacing target:** SC 6 in ~1–2 hours, SC 12 in ~3–5 hours, SC 20 in ~6–8 hours, SC 30 in ~15–20 hours, SC 40 in ~28–35 hours, SC 50 in ~45–55 hours of org play.

### 6.3 ACP award sources

| Source | ACP | Cap / cooldown | Notes |
|---|---:|---|---|
| Found gang | 500 | One-time | The founding milestone. |
| Found corporation | 5,000 | One-time | Requires SC 20 + 250k €$ + a physical asset. |
| Capture control center T1 | 1,000 | First capture | T1 site. |
| Capture control center T2 | 1,200 | First capture | T2 site. |
| Capture control center T3 | 1,400 | First capture | T3 site. |
| Capture control center T4 | 1,600 | First capture | T4 site. |
| Capture control center T5 | 1,800 | First capture | T5 site. |
| Recapture same site | 25% | Within 7 in-game days | Prevents ping-pong farming. |
| Defend control center T1–T5 | 500–900 | 1/site/day | 400 + 100×tier. |
| Military mission T1–T6 | 400 × tierMult | Diminishing returns | tierMult: 1, 1.5, 2.2, 3.2, 4.5, 6.0. |
| Espionage mission T1–T6 | 500 × tierMult | Diminishing returns | Same multipliers. |
| Economic mission T1–T6 | 300 × tierMult | Diminishing returns | Same multipliers. |
| Sabotage mission T1–T6 | 450 × tierMult | Diminishing returns | Same multipliers. |
| Assassination mission T1–T6 | 600 × tierMult | Diminishing returns | Same multipliers. |
| Rival lieutenant | 1,500 | Mission-tagged only | One-time per target. |
| Rival boss | 5,000 | Mission-tagged only | One-time per target. |
| Territory passive | 10/territory/day | Max 150/day | Only held, uncontested territory. |
| Org notoriety level | 500/level | One-time per level | Native org stat. |
| District dominance 50% | 2,000 | One-time per district | >50% of control centers. |
| District dominance 100% | 5,000 | One-time per district | Full district control. |
| Survive 4–5 star heat | 300 | Max 1/day | Must decay naturally; no hospital/ripperdoc clear. |
| Stock milestone | 1,000 | One-time per milestone | First 100k portfolio, first hostile takeover, etc. |
| NCPD hustle | 0 | Always suppressed | Vanilla source removed. |
| Random street kill | 0 | Always suppressed | Vanilla bounty SC removed. |
| Quest/gig/vehicle/achievement | 0 | Always suppressed | Vanilla sources removed. |

**Worked examples:**

- At SC 15 (7,900 ACP), a T1 capture (1,000) + T1 economic mission (300) + 2 territories of passive (20) = **1,320 ACP**, about 92% of the gap to SC 16 (1,440).
- At SC 25 (30,820 ACP), a T3 capture (1,400) + T3 economic mission (300 × 2.2 = 660) + 4 territories of passive (40) = **2,100 ACP**, about 60% of the gap to SC 26 (3,490).

**Diminishing returns:** Repeating the same mission type in the same district within 24 in-game hours: 100% → 75% → 50% → 25% → 0%. This encourages rotating mission types and districts.

**District multiplier (optional):** City Center 1.10, Pacifica 1.15, Dogtown 1.20, Badlands 0.90, other districts 1.00. This makes high-risk districts more rewarding without hard level gates.

### 6.4 Ascendancy unlocks driven by SC

SC is an **eligibility gate**, not the only requirement. Territory, crew, corp, and stock actions also require capital, upkeep, and milestones. This prevents a max-SC save from instantly owning the city.

| SC | Org capability | Additional requirement |
|---:|---|---|
| 1 | Found a gang; claim 1 territory; T1 missions | None |
| 2 | Crew slot 1; basic black market | Founding |
| 3 | Max 2 territories | — |
| 5 | T1 contracts; crew 2; first lieutenant | Lieutenant recruit cost |
| 6 | Autofixer Tier 1 (vanilla) | Money |
| 8 | Max 3 territories; T2 missions | — |
| 10 | Vanilla vendor discount (curve-driven; verify %) | Automatic |
| 12 | Autofixer Tier 2 (vanilla); max 4 territories | Money |
| 15 | Max 5 territories; T3 missions; corp shell (read-only market) | — |
| 18 | Lieutenant 2; crew 4; black-market cyberware | Black-market contact |
| 19 | Autofixer Tier 3 (vanilla) | Money |
| 20 | **Found Corporation**; stock trading | 250k €$ + physical asset |
| 25 | Max 7 territories; T4 missions; shorting; corp assets | — |
| 26 | Autofixer Tier 4 (vanilla) | Money |
| 30 | Max 9 territories; T4 contracts; elite lieutenants | — |
| 34 | Autofixer Tier 5 (vanilla) | Money |
| 35 | Max 11 territories; T5 missions; hostile takeovers | — |
| 40 | Max 13 territories; T5 contracts; district perks | — |
| 42 | Autofixer Tier 6 (vanilla) | Money |
| 45 | Max 15 territories; T6 missions; city-wide notoriety | — |
| 50 | Max 18–20 territories; T6 contracts; capstone; Autofixer Tier 7 | — |

**Crew cap:** `min(1 + floor(SC / 4), 12)`. SC 1 → 1, SC 5 → 2, SC 12 → 4, SC 20 → 6, SC 30 → 8, SC 40 → 11, SC 50 → 12.

**Lieutenant cap:** 1 at SC 5, 2 at SC 18, 3 at SC 30, 4 at SC 45.

**Mission tiers:** T1 SC 1, T2 SC 8, T3 SC 15, T4 SC 25, T5 SC 35, T6 SC 45.

**Black market tiers:** SC 5 junk/tech, SC 18 cyberware, SC 30 military hardware, SC 40 corpo-grade.

**Stock access:** SC 20 trading, SC 25 shorting, SC 35 hostile takeover, SC 45 IPO/own ticker.

### 6.5 Native + redscript architecture

```text
┌─────────────────────────────────────────────────────────────────────┐
│ Native C++20 (native/lib/sim/cred/)                                 │
│  - CredState: xp, level, lastDailyTick, source caps, history        │
│  - CredPolicy: pure functions, unit-tested on Linux                 │
│    • LevelForXp(xp) -> level                                        │
│    • XpForLevel(level) -> xp                                        │
│    • Award(source, tier, district, context) -> CredAward            │
│    • UnlocksForLevel(level) -> bitset                               │
│  - Emits CredAwarded { xpDelta, newXp, newLevel, unlockBits }       │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Redscript 1.x (thin)                                                │
│  - NeonAscendancy_StreetCredSystem (ScriptableSystem)               │
│      OnRestored -> sync target level                                │
│      AwardCred(...) -> NcAwardCred(...) -> queue level-up apply     │
│      ApplyPendingLevelUps() -> one level per delay tick             │
│  - @wrapMethod(PlayerDevelopmentData) AddExperience                 │
│      drop StreetCred unless m_allowCredXp                           │
│  - @wrapMethod(BountyManager) SetBountyFromID                       │
│      zero m_streetCredAmount while Ascendancy active                │
│  - UI: HUD notice + optional reputation panel                       │
└─────────────────────────────────────────────────────────────────────┘
```

**Why `SetLevel` instead of feeding the vanilla curve:**

- The vanilla SC curve is baked and opaque. Using `SetLevel(SC, targetLevel)` lets the native ACP table be the source of truth.
- The visual bar can still be proportional: compute `fraction = (ACP - ACP(level)) / (ACP(level+1) - ACP(level))`, read `remaining = data.GetRemainingExpForLevelUp(SC)`, and compute `desiredExp = round(remaining × fraction)`. Read `currentExp = data.GetCurrentLevelProficiencyExp(SC)`; if `desiredExp > currentExp`, add `desiredExp - currentExp` XP. If `desiredExp <= currentExp`, do nothing (the bar is already at or ahead and will correct on the next level-up). This uses the vanilla curve only for the bar, never for leveling.
- Apply at most one level per delayed tick to avoid a burst of 19 level-up notifications when a large award lands. Delayed callbacks must re-check `IsDefined` on the system, player, and data object before applying (per the redscript 1.x hook rules).

**Integration with the existing coordinator:** `NeonAscendancy_AscendancySystem` already runs a 10-second `DelayCallback` tick and drains HUD notices. Reuse that tick for passive ACP accrual and pending level-up application; do not add a second per-frame ticker.

**Persistence:**

- Native `CredState` lives in the per-playthrough SQLite save branch, with schema versioning per `docs/versioning.md`.
- Redscript persists `m_schemaVersion`, `m_lastAppliedLevel`, `m_lastAppliedExp`, `m_bootstrapVersion`.
- `m_allowCredXp` is transient; never persist it.

**Existing saves:**

- On first activation, `baseline = max(native level, current SC level)`.
- If native ACP is behind `baseline`, set native ACP to `ACP(baseline)`.
- Never lower the player's SC. A SC 50 save starts at SC 50, but org milestones/capital still gate the unlocks.
- If the player has SC 0 (corrupt/edited save), clamp to 1.

### 6.6 Anti-farm rules

1. **No SC from NCPD hustles, gigs, quests, vehicles, achievements, or CCL.** The `AddExperience` gate drops them.
2. **No SC from random kills.** `BountyManager.SetBountyFromID` zeroes bounty SC; only mission-tagged lieutenants/bosses award through the Ascendancy API.
3. **Recapture cooldown.** Same site recaptured within 7 in-game days awards 25%.
4. **Mission diminishing returns.** Same type + district within 24h: 100/75/50/25/0%.
5. **Passive cap.** 150 ACP/day from territory.
6. **Heat cap.** 300 ACP/day; only natural decay from 4–5 stars.
7. **One-time milestones.** Founding, corp, district dominance, stock milestones, notoriety levels cannot be re-farmed.
8. **No money→SC loop.** Vehicle purchases and stock profits award 0 SC; stock milestones are one-time.

### 6.7 UI / UX

- Vanilla SC bar/level still updates.
- HUD notice on ACP award: `+250 Street Cred (Capture: Kabuki)`.
- HUD notice on unlock: `Street Cred 12: Autofixer Tier 2 unlocked`.
- Optional `ncity.pub` reputation page: current SC, ACP, next unlock, owned territories, crew, active caps.
- Vendor hub still shows SC and discount.
- Autofixer still shows SC-locked cars.
- Do not show vanilla gig/NCPD SC rewards; the scanner bounty UI should show 0 SC.

---

## 7. Character Level XP and Skill Proficiencies

### 7.1 Vanilla Level XP sources

| Source | Mechanism | Evidence |
|---|---|---|
| Enemy neutralization | `RPGActionRewards.NeutralizeTrash/Weak/Normal/Rare/Elite/Boss` → `Proficiencies.Level` XP | `bountyManager.swift:193-218`, `rpg_action_rewards.tweak:71-180` |
| Quest rewards | `RPGManager.GiveReward` Level XP entries | `rpgManager.swift:2130-2270` |
| NCPD jobs | `ma_*` rewards Level XP | `minor_activities.tweak` |
| Vehicle metaquest | Level XP + SC | `vehicle_metaquest.tweak` |
| Achievements/CCL | Level XP | `achievements.tweak`, `ccl_rewards.tweak` |
| Combat skill XP | `RPGManager.AwardExperienceFromDamage` → Strength/Reflexes/Cool/Intelligence/Technical | `rpgManager.swift:1774-1924` |

**Does random combat award Level XP?** Yes, through `BountyManager.CompleteBounty` → `RPGManager.GiveReward(target, RPGActionRewards.Neutralize*)` when `target.AwardsExperience()` is true. The reward is small: base 3–25 XP plus 1% of target health. At Level 1, that is roughly 4–10 XP per kill. Without quest XP, early levels are slow.

### 7.2 The clean-slate Level XP gap

Vanilla `q001_mission0` alone awards **1,460 Level XP**, and `q001_dex` awards **1,516 Level XP**. Those are the early-game levels. A clean-slate player who only kills random enemies will need dozens of kills for Level 2 and hundreds for the first few levels.

**Recommendation:** Replace the missing quest XP with **Ascendancy mission Level XP**, not a blanket combat multiplier.

| Source | Level XP |
|---|---:|
| Found gang | 1,500 |
| Capture T1–T5 | 800 + 200×tier |
| Defend T1–T5 | 500 + 100×tier |
| Military/Espionage/Economic mission T1–T6 | 500 × tierMult (1, 2, 3.5, 5.5, 8, 12) |
| Rival lieutenant | 1,500 |
| Rival boss | 5,000 |
| District dominance 50% / 100% | 2,000 / 5,000 |

This mirrors the vanilla quest curve: the first founding + capture gives ~2,500 XP, enough for the first few levels; mid-game missions give 1,000–2,750 XP; late-game missions give 4,000–6,000 XP, with boss kills adding a 5,000 XP spike.

**Pacing caveat:** the exact Level 1→60 total is baked into the vanilla `player_level_up_curve` and is not visible in the plain-text tweaks. The table is a starting point. Target: a player who completes ~150 Ascendancy missions and fights through them should reach roughly **Level 50–60 by SC 45–50**. Tune the mission XP constants in native policy after a playtest; do not hard-code them in redscript.

**Optional:** Add a 100–300 XP completion bonus to the mission's primary skill (e.g., Cool for espionage, Intelligence for netrunning, Technical for economic) so non-combat missions do not starve skill progression. This is a nice-to-have, not a requirement.

**Do not** apply a global combat XP multiplier by default. It inflates the whole game and makes Level 60 trivial. If early-game testing shows the first mission is too far away, add a **1.15× Level XP multiplier for Level 1–10 only**, then remove it.

### 7.3 Skill proficiencies in 2.5 (important correction)

The prompt mentions "Headhunter, Netrunner, Shinobi, Solo, Engineer." Those are **pre-2.0 skill trees** and no longer exist in Cyberpunk 2077 2.0/2.5. The 2.5 model is:

- Five attributes: **Body, Reflexes, Technical Ability, Intelligence, Cool**.
- Five combat proficiencies: **StrengthSkill, ReflexesSkill, TechnicalAbilitySkill, IntelligenceSkill, CoolSkill**.
- Each proficiency has a 1–60 record max but its effective max is capped by the tied attribute; it grants passive bonuses at milestones.
- Perk points come from **Character Level** (and Espionage in PL), not from the five skill proficiencies. `GetDevPointsForLevel` returns points only for `Level` and `Espionage` (`playerDevelopmentSystem.swift:788-815`).
- Street Cred is a separate 1–50 proficiency.

**Recommendation:** Leave the five combat proficiencies on vanilla damage-based XP. They level naturally from mission combat. Do not merge them into Street Cred; they represent personal combat mastery, while SC represents org reputation.

### 7.4 Level/SC interplay

- **SC is independent of Character Level.** A high-SC/low-level player can access high-tier contracts, but enemies scale to player level and mission tier adds elites, not raw level. A high-level/low-SC player cannot found a corp or access T4+ missions until they earn SC.
- **Vendor/ripperdoc stock still gates by player level.** A high-SC/low-level player cannot buy high-level cyberware. This is intentional; SC is reputation, not power level.
- **At Level 60**, Ascendancy mission Level XP is wasted. Options: disable it, or convert 10% to ACP with a 500/day cap. Recommend disabling to keep SC finite; org notoriety continues.

---

## 8. Verification Plan

Static verification is complete for the file-level claims. The following require in-game checks (do not launch the game as part of this research task; this is the handoff checklist).

### 8.1 Clean-slate baseline

1. New clean-slate character: Level 1, SC 1, H10 apartment.
2. Scanner: hold scan, confirm Kiroshi visuals; zoom with the optics key.
3. Quickhack panel: confirm EMP Overload / Blind / Overheat, Memory 5.
4. Inventory: Kiroshi, Power Grip, Boring Plating, Militech Paraline MK I equipped; Unity + 300 HandgunAmmo; Q001 clothes; 5 inhalers; 2 frags.
5. H10: door opens from inside; elevator 1 works; stash, wardrobe, bed, shower, mirror, computer NETdir all usable; bed sleep works.
6. HUD: phone D-pad quick slots visible; vehicle summon works; map opens; fast travel from the H10 dataterm works; ammo counter visible.
7. Crafting: ammo/Unity/Knife recipes visible; craft ammo with 50 CommonMaterial1.
8. Vik: no tutorial; normal stock; no duplicate Kiroshi/PowerGrip/Boring Plating.
9. Vendors: SC discount applies as SC rises; no false SC from gigs/NCPD.
10. Autofixer: SC 6 car offer unlocks; below SC 6 it is locked.
11. NCPD: kill a wanted gang member; money awarded, SC unchanged; scanner shows 0 SC.
12. Ascendancy: found gang; capture a T1 site; SC jumps to the expected ACP level; Level XP increases; no tutorial spam.
13. Save/reload: SC/ACP persist; no duplicate money/items/vehicle; facts self-heal.
14. Existing save: SC preserved; missing cyberdeck/Kiroshi/vehicle repaired; no money/clothes duplicate.

### 8.2 Enemy scaling

1. Level 1 in City Center, Pacifica, Badlands, and Dogtown: check enemy nameplates/threat indicators.
2. Confirm ordinary spawns are NORMAL, not skull-locked.
3. Confirm named/scripted NPCs are absent or scaled by the mod's spawner.
4. If Dogtown has fixed-level cells, exclude them from early Ascendancy missions.

### 8.3 Street Cred math

1. Award a known ACP amount; confirm SC level and bar fraction.
2. Jump multiple levels in one award; confirm level-up notifications are queued, not lost.
3. Confirm `YouKnowWhoIAm` triggers at SC 50.
4. Confirm vendor discount at SC 10/20/30/40/50.
5. Confirm Autofixer tiers at 6/12/19/26/34/42/50.

---

## 9. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| `q000_started = 1` has native side effects not visible in scripts | Verify in-game; if broken, wrap the `GameStarted()` checks in the phone HUD, autodrive, and quick-slot classes instead of setting the fact. |
| `full_rpg_progression_on = 1` / `q000_patch_2_0_new_game = 1` are native-read | Set only on clean-slate new games; verify XP/perks; if broken, remove and test. |
| Level/perk progression unexpectedly capped despite `full_rpg_progression_on = 1` | First verify XP events and perk points in-game. If a native gate reads `q000_done`, do **not** fake the story fact; wrap the progression gate or use a custom new-game questphase instead. |
| H10 door/mirror/shower have hidden quest conditions | Verify each device in-game; add a targeted `DeviceManager` force-enable only if a specific device fails. |
| Fast travel only has H10 until other districts are visited | Accept as diegetic; or curate a `RegisterFastTravelPointsRequest` list later. |
| `SetLevel` burst-spams level-up notifications | Queue one level per 0.25–0.5s delayed tick; summarize in HUD. |
| Existing save with SC 50 skips SC progression | Unlocks still require capital/assets/milestones; consider a one-time "reputation audit" UI. |
| Other mods award SC | The AddExperience gate suppresses them; document compatibility. |
| Other mods hook the same methods | Use `@wrapMethod`, call `wrappedMethod` exactly, and avoid replacing. |
| Dogtown fixed-level cells | Spot-check; exclude from early missions or scale via the mod's spawner. |

---

## 10. Open Design Questions

### 10.1 Recommended defaults (for a first implementation)

| Decision | Recommended default | Why |
|---|---|---|
| Entry mechanism | Custom `.gamedef`/`.quest`/`.questphase` redirect (see `option-a-clean-slate-start.md`) | Actually avoids `q000`/`q001`; runtime bootstrap cannot prevent them from starting. |
| Starting cash | 2,500 €$ | Enough for ammo/healing/first contract; not enough to skip progression. |
| Starting vehicle | Archer Hella | Canonical starter car; already has a player variant. |
| Kiroshi / bounty link | Keep Kiroshi; zero bounty SC | Restores zoom and scanner info; bounty money remains a side income. |
| Dogtown | Open from frame 0 if the custom graph's gate is open; otherwise a short Ascendancy unlock | The companion graph keeps Dogtown city-life; do not fake `q302_done`. |
| SC cap | 50 + org notoriety | Uses vanilla cap; post-50 progression stays org-based. |
| Existing saves | Preserve SC; repair missing capabilities | Avoids punishing players; org milestones still gate. |
| Tutorials | Disable vanilla tutorials | A standalone campaign should not replay the prologue tutorials. |
| Level XP | Mission XP only | Replaces missing quest XP without inflating combat. |
| Territory cap | SC eligibility + capital/upkeep | Prevents a max-SC save from instantly owning the city. |

### 10.2 Questions for the user

1. **Entry mechanism:** the companion Option A research recommends a custom `.gamedef`/`.quest`/`.questphase` redirect. Confirm the native arm/disarm spike and the H10 spawn marker (`#mq000_01_sm_apartment`) before treating it as final. The baseline list is independent of the arm mechanism.
2. **Starting cash:** 2,500 €$ (recommended), 1,000 (vanilla-like), or 5,000 (faster org ramp)?
3. **Starting vehicle:** Archer Hella (canonical, recommended), Thorton Galena (neutral), or no vehicle (buy one)?
4. **Kiroshi/bounty link:** keep the NCPD bounty link for money-only bounties, or remove it entirely and rely on Ascendancy missions for income? Recommended: keep Kiroshi for zoom and scanner quality of life, zero bounty SC.
5. **Dogtown:** open it from frame 0 (recommended if the custom graph's gate is open), or keep it behind a short Ascendancy milestone? PL story gates are complex; a narrative unlock is cleaner than faking `q302_done`.
6. **Street Cred cap:** stay at vanilla 50, or add an Ascendancy prestige track beyond 50? Recommended: SC 50 cap + org notoriety for post-50.
7. **Existing saves:** preserve SC (recommended) or rebase to a lower "fresh org" value? Preserving avoids punishing players; org milestones still gate.
8. **Tutorials:** disable all (recommended for a standalone campaign) or keep a custom onboarding? If custom, do not set `disable_tutorials=1` and gate the vanilla tutorials individually.
9. **Level XP:** mission XP only (recommended), or add a small 1.15× combat XP multiplier for Level 1–10?
10. **Territory cap:** is SC the primary cap, or should capital/upkeep also cap territory? Recommended: SC eligibility + capital/upkeep.
11. **Vanilla gigs/NCPD:** permanently suppressed (per scope), or later reskinned as Ascendancy contracts? The current scope says suppressed.
12. **SC unlock scope:** should Autofixer/vanilla vendor gates remain untouched (recommended), or should the mod add SC prerequisites to high-tier cyberware? Vanilla ripperdoc stock is player-level gated; a separate black market is cleaner.

---

## Appendix A — Extracted Quest-Phase Facts (Selected)

These are the facts that matter for baseline. Values are from `q000`/`q001`/`q005`/`mq000` quest-phase and scene JSON exported with WolvenKit.

> **Read this as "what vanilla sets", not "what to set".** Appendix A includes story facts such as `q000_done`, `q001_active`, and `q001_started` so the audit is complete. The recommended bootstrap in §4.3 deliberately omits the story-completion facts and sets only the safe subset.

### A.1 `q000` progression/HUD facts

```text
q000_started = 1
q000_done = 1
q000_patch_2_0_new_game = 1
full_rpg_progression_on = 1
dpad_hints_visibility_enabled = 0/1
q001_hide_ammo_counter = 0/1
radio_on = 0/1
tv_on = 0/1
prevention_dispatcher_disabled = 0/1
disable_combat_events = 0/1
block_combat_scripts_tutorials = 0/1
```

### A.2 `q001` baseline facts

```text
q001_active = 1
q001_started = 1
q001_ripperdoc_done = 1
q001_in_v_room = 1
q001_enable_dressing = 1
q001_weapons_not_taken = 1
q001_apartment_bed_disabled = 0
q001_show_sts_tut = 1
q001_can_call_dex = 1
q001_checked_stash = 1
q001_left_v_apartment = 1
q001_tbug_netrunner_tut = 1
q001_used_mb_elevator = 1
apartment_on = 1
unlock_phone_hud_dpad = 1
unlock_car_hud_dpad = 1
watson_prolog_lock = 1
disable_tutorials = 1
glossary_ripperdocs = 1
glossary_fixers = 1
glossary_mercenaries = 1
```

### A.3 `q001` item grants/equips

```text
AddItem Items.CyberdeckSplinter 1
AddItem Items.Preset_V_Unity 1
AddItem Items.Preset_V_Unity_Cutscene 1
AddItem Items.Q001_Pants 1
AddItem Items.Q001_Shoes 1
AddItem Items.Q001_TShirt 1
RemoveByItemID Items.Q000_* (all lifepath clothes)
Equip Items.CyberdeckSplinter AttachmentSlots.Splinter
Equip Items.Q001_Pants
Equip Items.Q001_Shoes
Equip Items.Q001_TShirt
```

### A.4 `q000_vr_tutorial` item grants/equips

```text
AddItem Items.AdvancedMilitechParalineMKICommon 1
AddItem Items.CyberdeckSplinter 1
AddItem Items.MilitechParaline 1
AddItem Items.Preset_V_Unity 1
AddItem Items.Preset_V_Unity_Cutscene 1
AddItem Items.Q001_Pants 1
AddItem Items.Q001_Shoes 1
AddItem Items.Q001_TShirt 1
Equip Items.AdvancedMilitechParalineMKICommon AttachmentSlots.Splinter
Equip Items.CyberdeckSplinter AttachmentSlots.Splinter
Equip Items.MilitechParaline AttachmentSlots.Splinter
Equip Items.Q001_Pants
Equip Items.Q001_Shoes
Equip Items.Q001_TShirt
```

### A.5 `q001_04_ripperdoc` item equips

```text
Equip Items.KiroshiOptics
Equip Items.PowerGripRare
Equip Items.Preset_V_Unity_Cutscene
```

### A.6 `q001_03a_meet_jackie_downstairs` vehicle facts

```text
questEnablePlayerVehicle vehicle=Vehicle.v_standard2_archer_hella_player enable=1
questEnableVehicleSummon enable=1
unlock_car_hud_dpad = 1
```

### A.7 `q001_00d_leaving` phone fact

```text
unlock_phone_hud_dpad = 1
```

### A.8 `q001_01_wakeup` apartment fact

```text
apartment_on = 0
apartment_on = 1
```

### A.9 `mq000_vs_apartment_interactions` ambient condition

```text
apartment_on == 1
interior_manager_on == 0
q305_johnny_scene_active == 0
```

The phase force-offs `#megabuilding_elevator_2`, `#q001_v_radio`, `#q001_v_room_tv`, and `#q001_v_room_tv_02` as part of its ambient logic. Elevator 1 is not force-disabled.

---

## Appendix B — Exact IDs and Facts for Implementation

### B.1 Items

| Purpose | TDBID |
|---|---|
| Starter cyberdeck | `Items.AdvancedMilitechParalineMKICommon` |
| Tutorial/quest deck (not the canonical starter) | `Items.CyberdeckSplinter` |
| Kiroshi optics | `Items.KiroshiOptics` |
| Hand cyberware | `Items.PowerGripRare` |
| Smart Link alternative | `Items.AdvancedSmartLink_Tutorial_Common` |
| Armor cyberware | `Items.AdvancedBoringPlating_Q001` |
| Pistol | `Items.Preset_V_Unity` |
| Pistol ammo | `Ammo.HandgunAmmo` |
| Basic healing | `Items.FirstAidWhiffV0` |
| Frag grenade | `Items.GrenadeFragRegular` |
| Melee fallback | `Items.Preset_Baseball_Bat_Default` |
| Ping quickhack | `Items.PingProgram` |
| Starter shirt | `Items.Q001_TShirt` |
| Starter pants | `Items.Q001_Pants` |
| Starter shoes | `Items.Q001_Shoes` |
| Crafting material | `Items.CommonMaterial1` |
| Craftable Unity recipe | `Items.Craftable_Common_Unity` |
| Craftable knife recipe | `Items.Craftable_Common_Knife` |
| Starter vehicle | `Vehicle.v_standard2_archer_hella_player` |
| Neutral vehicle alternative | `Vehicle.v_standard2_thorton_galena_player` |
| Money item | `MarketSystem.Money()` |

### B.2 Facts

```text
map_blocked = 0
watson_prolog_lock = 0
watson_prolog_unlock = 1
q101_enable_activities_flat = 1
q101_enable_side_content = 1
q000_started = 1
q000_patch_2_0_new_game = 1          # clean-slate only
full_rpg_progression_on = 1          # clean-slate only
unlock_phone_hud_dpad = 1
unlock_car_hud_dpad = 1
initial_gadget_picked = 1
dpad_hints_visibility_enabled = 1
disable_tutorials = 1
levelup_tutorial = 1
fast_travel_tutorial = 1
fast_travel_tutorial_seen = 1
street_cred_tutorial = 1
q001_ripperdoc_done = 1
ripperdoc_tutorial_seen = 1
tutorial_ripperdoc_slots = 2
tutorial_ripperdoc_eyes_passed = 1
tutorial_ripperdoc_hands_passed = 1
tutorial_ripperdoc_armor_passed = 1
q001_hide_ammo_counter = 0
apartment_on = 1                     # fallback only; mq000 normally manages it
interior_manager_on = 0              # fallback only
q001_in_v_room = 1
q001_enable_dressing = 1
q001_weapons_not_taken = 1           # clean-slate only
q001_apartment_bed_disabled = 0      # clean-slate only
radio_on = 1
tv_on = 0
```

**Never set:**

```text
q000_done
q001_done
q001_completed
q001_active
q005_done
q101_done
sts_loop_start
ep1_standalone
q302_done
q115_point_of_no_return
# and any other q115_* / ep1_* story fact
```

### B.3 APIs used by the bootstrap

| Action | API |
|---|---|
| Give item | `TransactionSystem.GiveItem(player, itemID, quantity)` |
| Has item | `TransactionSystem.HasItem(player, itemID)` |
| Equip | `EquipmentSystem.GetData(player).EquipItem(itemID)` |
| Is equipped | `EquipmentSystem.GetData(player).IsEquipped(itemID)` |
| Give money | `TransactionSystem.GiveItem(player, MarketSystem.Money(), amount)` |
| Set fact | `GameInstance.GetQuestsSystem(game).SetFact(n"fact", value)` |
| Get fact | `GameInstance.GetQuestsSystem(game).GetFact(n"fact")` |
| Add recipe | `CraftingSystem.GetInstance(game).GetPlayerCraftBook().AddRecipe(t"Recipe.ID")` |
| Enable vehicle | `GameInstance.GetVehicleSystem(game).EnablePlayerVehicle("Vehicle.ID", true)` |
| Unlocked vehicles | `GameInstance.GetVehicleSystem(game).GetPlayerUnlockedVehicles(out vehicles)` |
| Remove fast-travel locks | `FastTravelSystem.RemoveAllFastTravelLocks(game)` |
| Set SC level | `PlayerDevelopmentData.SetLevel(gamedataProficiencyType.StreetCred, level, telemetryLevelGainReason.Gameplay)` |
| Add SC XP | `PlayerDevelopmentData.AddExperience(amount, gamedataProficiencyType.StreetCred, telemetryLevelGainReason.Gameplay)` |
| Remaining SC XP | `PlayerDevelopmentData.GetRemainingExpForLevelUp(gamedataProficiencyType.StreetCred)` |
| Current SC XP | `PlayerDevelopmentData.GetCurrentLevelProficiencyExp(gamedataProficiencyType.StreetCred)` |
| Current SC level | `PlayerDevelopmentData.GetProficiencyLevel(gamedataProficiencyType.StreetCred)` |

---

## Appendix C — Source Index

### C.1 Repository references

| Topic | Path |
|---|---|
| Scanner gate | `refs/cyberpunk/cyberpunk/player/playerVisionModeController.swift:173-187` |
| Zoom gate | `refs/cyberpunk/cyberpunk/player/psm/zoomTransitions.swift:230-275` |
| Kiroshi stats | `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/items/cyberware/eyes/eyes_general.tweak:1-40` |
| Player base stats | `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/characters/player/player_base_stats.tweak:504-520, 1825-1860` |
| Cyberdeck stats | `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/items/cyberware/system_replacement/cyberdeck_instances_advanced.tweak:1554-1605` |
| Splinter deck | `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/items/splinters/base_splinters.tweak:61-90` |
| Power Grip | `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/items/cyberware/hands/hands_general.tweak:1-60` |
| Boring Plating | `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/items/cyberware/integumentary_system/integumentary_system_advanced.tweak:2448-2548` |
| Unity preset | `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/items/weapons/ranged/handguns/unity/preset_base_unity.tweak:429` |
| Ammo | `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/items/ammo/ammo.tweak:65-82` |
| Vehicle summoning gate | `refs/cyberpunk/core/systems/vehicleSystem.swift:65-108` |
| Fast travel | `refs/cyberpunk/core/systems/fastTravelSystem.swift:300-301, 547-590, 642` |
| Map gate | `refs/cyberpunk/cyberpunk/UI/fullscreen/ingame/menuDataBuilder.swift:132-140` |
| Hub map/Tarot | `refs/cyberpunk/cyberpunk/UI/fullscreen/hub/radialHubMenuGameController.swift:250-251` |
| Phone HUD | `refs/cyberpunk/cyberpunk/UI/hud/phone/newHudPhoneGameController.swift:83-97, 1505-1515` |
| Quick-slot hint gate | `refs/cyberpunk/cyberpunk/player/psm/quickSlotsTransitions.swift:731` |
| Ammo counter | `refs/cyberpunk/cyberpunk/UI/weapons/weaponRoster.swift:467, 631` |
| SC sink | `refs/cyberpunk/cyberpunk/systems/playerDevelopmentSystem.swift:552-607` |
| SC stat write | `refs/cyberpunk/cyberpunk/systems/playerDevelopmentSystem.swift:481-486` |
| SC tutorial | `refs/cyberpunk/cyberpunk/systems/playerDevelopmentSystem.swift:590-592` |
| SC achievement | `refs/cyberpunk/cyberpunk/systems/playerDevelopmentSystem.swift:426-432` |
| Bounty SC | `refs/cyberpunk/cyberpunk/managers/bountyManager.swift:66-219` |
| Bounty link gate | `refs/cyberpunk/cyberpunk/managers/bountyManager.swift:179` |
| Reward SC | `refs/cyberpunk/cyberpunk/managers/rpgManager.swift:2130-2270` |
| Damage skill XP | `refs/cyberpunk/cyberpunk/managers/rpgManager.swift:1774-1924` |
| XP event funnel | `refs/cyberpunk/cyberpunk/player/player.swift:2028-2032` |
| Power differential | `refs/cyberpunk/cyberpunk/managers/rpgManager.swift:1645-1659` |
| Open-world scaling | `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/content_assignment/open_world.tweak` |
| Scale modifier | `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/characters/npcs/records/gameplay/gameplay.tweak:4-14` |
| SC max | `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/proficiencies/base_values.tweak:18-28` |
| Vendor SC templates | `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/vendors/base_values.tweak:278-650` |
| SC program stock | `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/vendors/base_values.tweak:307-340` |
| SC loot prereq | `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/prereqs/simple_prereqs.tweak:135-142` |
| SC discount | `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/items/prices/price_modifiers.tweak:1340-1350` |
| SC passive group | `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/characters/player/player_proficiency_passives.tweak:255-265` |
| Vehicle offers | `<game>/tools/redmod/tweaks/ep1/gameplay/static_data/database/vehicles/vehicleoffers.tweak:39,66` |
| Vehicle SC tiers | `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/content_assignment/street_cred_tiers.tweak:144-176` |
| SC item requirement UI | `refs/cyberpunk/cyberpunk/UI/inventory/inventoryItemDisplayController.swift:1190-1200` |

### C.2 Extracted quest phases

| Phase | What it establishes |
|---|---|
| `base/quest/main_quests/prologue/q000/phases/q000_vr_tutorial.questphase` | Starter cyberdeck, Unity, Q001 clothes |
| `base/quest/main_quests/prologue/q000/q000.questphase` | `q000_done`, `q000_patch_2_0_new_game`, VR tutorial flags |
| `base/quest/main_quests/prologue/q000/phases/q000_kid.questphase` | `full_rpg_progression_on` |
| `base/quest/main_quests/prologue/q000/phases/q000_corpo.questphase` | `full_rpg_progression_on`, money |
| `base/quest/main_quests/prologue/q000/phases/q000_nomad.questphase` | `full_rpg_progression_on`, money |
| `base/quest/main_quests/prologue/q001/phases/q001_mission0.questphase` | Splinter, Unity, Q001 clothes, removes Q000 clothes |
| `base/quest/main_quests/prologue/q001/phases/q001_04_ripperdoc.scene` | Kiroshi, PowerGrip |
| `base/quest/main_quests/prologue/q001/phases/q001_ripperdoc.questphase` | `q001_ripperdoc_done`, glossary |
| `base/quest/main_quests/prologue/q001/phases/q001_03a_meet_jackie_downstairs.scene` | Archer Hella, `unlock_car_hud_dpad` |
| `base/quest/main_quests/prologue/q001/phases/q001_00d_leaving.scene` | `unlock_phone_hud_dpad` |
| `base/quest/main_quests/prologue/q001/phases/q001_01_wakeup.scene` | `apartment_on` |
| `base/quest/main_quests/prologue/q001/phases/q001_apartment.questphase` | dressing/room/weapons, removes Splinter, device control |
| `base/quest/main_quests/prologue/q001/q001.questphase` | `q001_apartment_bed_disabled` |
| `base/quest/main_quests/prologue/q001/phases/q001_fast_travel_unlock.questphase` | Watson dataterm registration |
| `base/quest/minor_quests/mq000/phases/mq000_vs_apartment_interactions.questphase` | `apartment_on`/`interior_manager_on` ambient condition |

---

## Appendix D — Glossary

| Term | Meaning |
|---|---|
| **ACP** | Ascendancy Cred Points; the native XP currency behind the reworked Street Cred. |
| **Capability ensure** | An idempotent bootstrap that grants only missing essential systems, not a blind starter kit. |
| **Clean-slate** | A new Level 1 campaign with no `q000`/`q001`/`q005`, no main quests, no gigs, no NCPD scanner hustles. |
| **SC** | Street Cred, the vanilla 1–50 proficiency. |
| **SC tier** | The vanilla `VehicleTier1..7` vehicle thresholds (6/12/19/26/34/42/50); vendor stock availability uses separate `*CredAvailability` records. |
| **Story fact** | A `QuestsSystem` fact that records quest completion or story state; never fake these to unlock content. |
| **Traversal fact** | A fact that gates movement/content (e.g., `watson_prolog_lock`); safe to set to the era-appropriate value. |
| **HUD fact** | A fact that gates UI hints (e.g., `unlock_car_hud_dpad`); safe to set. |
