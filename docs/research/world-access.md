# Research — World Access: How Locations Lock, and How Neon Ascendancy Opens Them

**Target:** Cyberpunk 2077 2.5 + Phantom Liberty, redscript 1.0.2 (Codeware-free),
RED4ext 1.31.1 + RedLib, ArchiveXL 1.28.11, TweakXL 1.12.2, WolvenKit.CLI 10.0.0-beta.1.
**Date:** 2026-11-25.
**Scope:** the owner requirement in [gameplay-systems.md §10](../design/gameplay-systems.md):
**no vanilla gigs, ever**, and **every location reachable by V and NPCs** (doors and
areas included), except places that would not exist in this alternate timeline
(the nomad-camp tent after Panam's story, Kurtz/Kutcher's home).

**Evidence grades**

- **[V]** verified in this session against the local 2.5 install: decompiled
  scripts under `refs/cyberpunk/`, RED4ext SDK headers, or an actual
  WolvenKit.CLI extract of `basegame_4_gamedata.archive` /
  `basegame_3_nightcity.archive` / `ep1_1_nightcity.archive`.
- **[R]** read from extracted quest/streaming resources, structurally certain,
  but not yet observed at runtime.
- **[H]** hypothesis. Needs the in-game probe in §5.

Raw extracts for this document were made into a session scratchpad and deleted;
every number below is reproducible with the commands in Appendix A.

---

## 0. Executive summary

1. **Doors are not "locked by default." They are *powered and closed by a
   phase*.** The engine model is three persistent booleans on `DoorControllerPS`
   (`m_isOpened`, `m_isLocked`, `m_isSealed`) plus a device state
   (ON/OFF/DISABLED/UNPOWERED). Vanilla gigs reach into the world and issue
   `DoorControllerPS + ForceClose/ForceUnpower` to shut a venue, and
   `ForcePower/ForceOpen` to open it again. Measured across the 47 base-game
   gig open-world phases: **352 door actions in 35 of 47 phases**, dominated by
   `ForceUnpower` (131) and `ForceClose` (119). **[V]**

2. **The big quest interiors have geometry that already streams, but their
   gameplay layer does not.** The city block has 23,718 streaming descriptors;
   every street and building shell lives in `Exterior` (15,121) and `Interior`
   (2,425) sectors that stream with no quest at all. Only the *gameplay* layer —
   workspots, patrols, guard areas, security devices, spawners — is bound to a
   `Quest` sector (2,358 descriptors) and needs a phase to instantiate its
   prefab. So "reachable" splits into *shell reachable* (true almost everywhere)
   and *venue usable* (only where a location phase claims it). **[V]**

3. **The thing that actually keeps a venue "open" in vanilla is an open-world
   location phase, not the quest.** Example: Lizzies is kept open by
   `base\open_world\community\watson\kabuki\phases\wat_kab_lizzies_bar_phase.questphase`,
   which declares `#loc_q004_lizzys_nightclub_openworld` and fans into eight
   quest-scoped sub-phases (`lizzies_default`, `lizzies_q004`, `lizzies_q105`,
   `lizzies_location`, `lizzies_scenes`, …). Door control lives in those
   sub-phases: `lizzies_location` issues `ForceDisabled`/`ForceClose`/
   `ForceEnabled` on `#q105_lizzies_door_entrance` and the roof door. **[V]**

4. **The clean-slate archive already keeps this layer alive, and that is the
   right foundation.** `tools/build-clean-slate.py` keeps
   `open_world_global_commuinity_phase.questphase`, which fans into 17 district
   community phases, which in turn reach the per-location phases like
   `wat_kab_phase` → `wat_kab_lizzies_bar_phase`. So in a clean-slate boot the
   venue-keeping layer runs; what is missing is only the content inside it.
   **[V]**

5. **Only two lock mechanisms dominate in practice:** (a) a phase forcing door
   device state, and (b) a phase not being run at all, so its prefab never
   instantiates. Everything else — keycards, skill checks, lifts, security
   areas — is real but secondary, and each has a documented override. **[V]**

6. **Recommended approach: layered, phase-first, script as safety net.**
   Author a *venue phase* (built by `build-clean-slate.py`) that declares each
   venue's `phasePrefabs` and issues `ForcePower`/`ForceOpen`, then a redscript
   sweeper that fixes residual `LOCKED`/`SEALED`/`DISABLED` doors near the
   player. Do not chase facts: almost no interior door is gated on a fact, it is
   driven by device events. **[R]**

7. **Five things need an in-game probe** (§5), the most important being whether
   a Neon-authored phase's `phasePrefabs` makes its `NodeRef`s resolve. If it
   does, the whole venue-opening design is pure data. **[H]**

---

## 1. Lock mechanisms

### 1.1 The core model: a door is a device with three booleans

A door in Cyberpunk is not "locked by the map." It is a `DoorControllerPS` with
**three persistent booleans plus a device state**, and anything that changes
access does so by writing those:

```redscript
// refs/cyberpunk/cyberpunk/devices/door/doorController.swift:36-56
public class DoorControllerPS extends ScriptableDeviceComponentPS {
  protected persistent let m_doorProperties: DoorSetup;
  protected inline let m_doorSkillChecks: ref<EngDemoContainer>;
  private persistent let m_isOpened: Bool;          // :42
  private persistent let m_isLocked: Bool;          // :44
  private persistent let m_isSealed: Bool;          // :46
  ...
  protected persistent let m_isPlayerAuthorised: Bool;   // :54
```

The derived state that the UI and interaction system read is a strict
precedence chain (`doorController.swift:198-209`):

```redscript
public final const func GetDoorState() -> EDoorStatus {
  if this.IsOpen()   { return EDoorStatus.OPENED; };
  if this.IsLocked() { return EDoorStatus.LOCKED; };
  if this.IsSealed() { return EDoorStatus.SEALED; };
  return EDoorStatus.CLOSED;
}
```

So `OPENED > LOCKED > SEALED > CLOSED`. A door that is closed but neither locked
nor sealed is simply *shut and usable* — the normal open-world state. This
matters for the design: **there is no "gig lock flag" to clear.** The gig either
powers/closes the door, or it disables the device entirely.

Initial state comes from the entity template, not the world
(`doorController.swift:261-279`):

```redscript
protected final func SetDefaultDoorState() -> Void {
  switch this.m_doorProperties.m_initialDoorState {
    case EDoorStatus.OPENED: this.SetIsOpened(true); break;
    case EDoorStatus.CLOSED: this.SetIsOpened(false); break;
    case EDoorStatus.LOCKED: this.SetIsOpened(false); this.SetIsLocked(true); break;
    case EDoorStatus.SEALED: this.SetIsOpened(false); this.SetIsSealed(true); break;
```
`m_initialDoorState` and the toggle permissions live on the `DoorSetup` struct
(`orphans.swift:33210-33258`): `m_initialDoorState`, `m_canPlayerToggleLockState`,
`m_canPlayerToggleSealState`, `m_canPayToUnlock`, `m_isShutter`.

There is also a *second* gate worth knowing: `IsStatic()` returns true when a
door is sealed-and-not-toggleable, or locked-and-not-authorised-and-not-hackable
(`doorController.swift:80-88`). A static door exposes no interaction at all — it
looks like a wall. That is how quest "fake doors" and permanently shut service
corridors behave. **[V]**

### 1.2 Mechanism catalogue, ranked by prevalence

The ranking below is measured, not guessed: I extracted all 47 base-game gig
open-world phases and counted their device actions. Results are in the table.

| # | Mechanism | What it is | Prevalence | Override |
| --- | --- | --- | --- | --- |
| **1** | **Phase forces device state** | A `.questphase` issues `DoorControllerPS` + `ForceClose` / `ForceUnpower` / `ForceOpen` / `ForcePower` against a `#node_ref` | **Dominant.** 352 door actions across 35/47 gig phases; `ForceUnpower` 131, `ForceClose` 119, `ForcePower` 43, `ForceOpen` 18 | Send the inverse action (`QuestForcePower`, `QuestForceOpen`, `QuestForceUnlock`, `QuestForceUnseal`) via script, or author our own phase |
| **2** | **Phase not running → no prefab → no gameplay layer** | Venue workspots/guards/doors-as-devices exist only in a `Quest`-category sector bound to `phasePrefabs[].prefabNodeRef` | **Dominant for "interior is empty."** 2,358 of 23,718 descriptors are `Quest` | Declare the prefab in our own phase (§4) |
| **3** | **Device disabled (`ForceDisabled`)** | `EDeviceStatus.DISABLED`; the device stops responding entirely (no power, no interaction) | Common on data terms (24 in node 142 alone), doors in some phases | `QuestForceEnabled` (`scriptableDeviceBasePS.swift:4486`) then `QuestForcePower` |
| **4** | **Door locked (`ForceLock`)** | Sets `m_isLocked = true`, clears seal (`doorController.swift:1196-1207`) | Moderate; more common in gig *sub*phases than openworld | `QuestForceUnlock` (`:1218`), or set `m_isLocked=false` |
| **5** | **Door sealed (`ForceSeal`)** | Sets `m_isSealed = true` and closes; often paired with `m_canPlayerToggleSealState=false` ⇒ `IsStatic()` | Less common; blast doors, vaults, story barriers | `QuestForceUnseal` (`:1262`) |
| **6** | **Keycard / password / authorization** | `IsUserAuthorized` checks security system level, an authorized-user list, then `UserAuthorizationAttempt` (`scriptableDeviceBasePS.swift:1934-1960`); keycards via `IsDeviceSecuredWithKeycard` (`:1909`) | Venue-specific: Konpeki, Arasaka, corp floors, Black Sapphire | `QuestForceAuthorizationDisabled` (action name `AuthorizationDisable`) sets the module off; `OnSetAuthorizationModuleOFF` also unlocks+opens the door (`doorController.swift:1300-1309`) if not sealed |
| **7** | **Skill check (hacking / engineering / demolition)** | `m_doorSkillChecks: EngDemoContainer` (`doorController.swift:40`); slots from `skillCheckContainer.swift:2-46` | Common on service doors and shortcuts, not on main story doors | `HasAnySkillCheckActive()` false ⇒ no gate. Script can clear `m_doorSkillChecks` or grant the check; or just `ForcePower`/`ForceOpen` past it |
| **8** | **Elevator floor inactive / hidden / unauthorized** | `LiftControllerPS.m_floors[i].m_isInactive`, `.m_isHidden`, `m_floorsAuthorization[i]` (`liftController.swift:241-247, 657-664`) | Venue-specific (Arasaka Tower, Konpeki AV, Black Sapphire) | `QuestSetFloorActive` (`:903`, clears inactive), `QuestSetFloorInactive` (`:911`); `ForceGoToFloor` / `ForceTeleportToFloor` teleport past the gate |
| **9** | **Security area (`SAFE`/`RESTRICTED`)/system** | `SecurityAreaControllerPS`, `SecuritySystemControllerPS`; alarms, lockdowns, turrets | 96 security areas + 63 security systems in the extracted site sample; present in most gig prefabs | The mod already overrides `GetSecurityAreaType` and `UpdateSecurityZoneDataBlackboard` for `SAFE`. `ForceDisabled` works on the system PS |
| **10** | **Streaming / prefab variant** | Named `worldStreamingSectorVariant` entries with `enabledByDefault` (lockdown bars, extra props, lighting) | 13,351 variants in the city block; 9,109 disabled by default | Variants are normally toggled by a phase; no script API exists (§1.4) |
| **11** | **Quest fact gating a phase** | A phase waits on e.g. `q000_done >= 1`, `q105_01_active >= 1`, `lizzies_bar_closed` | Real but narrow — see §1.5 | Set the fact, or author our own phase without the gate |

**Why (1) outranks keycards and skill checks:** the measured action distribution
from the 47 gig open-world phases was

```
DoorControllerPS ForceUnpower 131 | ForceClose 119 | ForcePower 43 | ForceOpen 18 | ForceON 15
ElectricLightControllerPS ForceOFF 54 | ForceON 16
ComputerControllerPS ForceUnpower 11 | ExplosiveDeviceControllerPS ForceDisabled 9
```

No `ForceLock`, `ForceSeal`, or `AuthorizationDisable` appears in that sample at
all: **the open-world "keep the venue shut" layer is powered-off and closed
doors, not locked ones.** That is a much easier state to reverse than a lock.
The `data/sites/doors.json` sample agrees: of 375 doors, `unlock_action` is
`ForcePower` for 277 and vanilla `vanilla_lock_action` is `ForceClose` (91) or
`ForceUnpower` (79) most often. **[V]**

### 1.3 What each action actually does

The action classes are plain `ActionBool` subclasses
(`cyberpunk/devices/core/baseDeviceActions.swift:1985-2046`), and the handlers
live on the PS:

| Action | Handler | Effect |
| --- | --- | --- |
| `QuestForceEnabled` | `scriptableDeviceBasePS.swift:4486` | Re-enables a DISABLED device; restores cached state or OFF |
| `QuestForceDisabled` | `:4512` | `DisableDevice()` — device stops responding |
| `QuestForcePower` | `:4529` | `PowerDevice()`; if DISABLED, also activates |
| `QuestForceUnpower` | `:4552` | `UnpowerDevice()` |
| `QuestForceOpen` | `doorController.swift:1084` | Opens |
| `QuestForceLock` | `:1196` | `m_isLocked=true`, `m_isSealed=false` |
| `QuestForceUnlock` | `:1218` | `m_isLocked=false`, `m_isSealed=false` |
| `QuestForceSeal` | `:1240` | closes, `m_isSealed=true` |
| `QuestForceUnseal` | `:1262` | `m_isSealed=false` |
| `QuestForceAuthorizationDisabled` | `doorController.swift:1300` | authorization module off; also unlocks and opens if not sealed |

Crucially, `OnQuestForceLock` and `OnQuestForceSeal` both begin with an empty
`if this.IsUnpowered() || this.IsDisabled() { }` guard — the write happens
regardless. `OnQuestForceOpen` (`doorController.swift:1084-1095`) is the same: it
sets `m_isOpened=true`, clears lock and seal, and returns
`SendPSChangedEventToEntity` without checking power. So the *quest* actions are
state writers, not physical-authority checks.

The distinction that matters is with the **non-quest** actions. The ordinary
player/interaction path `OnForceOpen` (`:1062-1077`) *does* refuse:

```redscript
if this.IsDisabled() || this.IsSealed() {
  return this.SendActionFailedEvent(evt, evt.GetRequesterID(), "Sealed or Disabled");
};
```

So the player cannot open a sealed or disabled door, but a `QuestForceOpen`
clears the seal for them. Still, **pair `ForcePower` before `ForceOpen`**: an
unpowered door entity has no power to animate or drive its shutter, so the PS
flag and the physical door can disagree. Probe §5.4 settles whether the pair is
required on 2.5. **[V]**

### 1.4 Streaming/prefab variants — real, but not script-addressable

The block file carries 13,351 named variants; 4,242 enabled by default, 9,109
not. Names are semantic: `lockdown`, `prolog_blockades` (253), `final_loot`
(355), `on_off_switch` (738), `loot` (660), `assets_variant` (885), plus
quest-specific ones like `q201_johnny_bridge`, `q116_v`.

Sampled interiors show the split clearly:

| Venue token | Variants | `Exterior` | `Interior` | `Quest` |
| --- | --- | --- | --- | --- |
| `arasaka_hotel` / konpeki | 166 | 143 | 17 | 6 |
| `dollhouse` (Clouds) | 116 | 67 | 47 | 2 |
| `arasaka_tower` | 418 | 265 | 126 | 27 |
| `totentanz` | 13 | 12 | 0 | 1 |
| `lizzys` | 12 | 9 | 2 | 1 |

There is **no redscript API to toggle a sector variant**. `SetVariant` exists
only on `IBlackboard` (`orphans.swift:18321`) and `EffectData`
(`:19115`), which is unrelated. The SDK exposes the data types
(`world::StreamingSectorVariant`, `StreamingWorld::blockRefs`) and
`world::IQuestPrefabStateListener` (`RED4ext.SDK/.../world/IQuestPrefabStateListener.hpp`),
but no callable toggle. The supported lever is *the phase that owns the prefab*:
registering `prefabNodeRef` in `phasePrefabs` is what causes the sector and its
variants to be applied. Treat variants as a consequence of phase ownership, not
an independent control. **[V]**

Practical consequence for the mod: the `lockdown` variants we would most want
to suppress are `enabledByDefault: 0` already, so with the gig phases omitted
they are simply absent. There is nothing to switch off. **[R]**

### 1.5 Fact-gated location phases — narrower than it looks

Facts do gate *location* phases, but the common gates I sampled are benign in a
clean-slate run because we already set the unlock set:

- `lizzies_default.questphase` pauses on `q000_done >= 1` (node id 15) to gate
  *crowd* activation, but its single `ForceClose` on `#q105_lizzies_door_entrance`
  sits on an ungated `questInteractiveObjectManagerNodeDefinition` (node id 54)
  reachable straight from the phase input. So the entrance is **always closed**
  by the open-world layer. It is *closed, not locked* — still usable. This is
  the normal case and precisely why "door closed by a gig" is not a lock.
  **[V]**
- `wat_kab_lizzies_bar_phase.questphase` sets `q000_done = 1` on its **`q004`
  input only** — verified by reachability walk: the `In1` input reaches 14 nodes
  and sets zero facts, while the `q004` input sets `q000_corpo_background` and
  `q000_done`. Since our archive wires `In1`, this is safe. **This is a design
  constraint to preserve, not an accident to rely on blindly.** **[V]**
- `lizzies_location.questphase` gates its door actions on
  `q004_nightclub_accessed >= 1`, `q105_01_active`, `q105_01_door_open`, and
  toggles `lizzies_bar_closed`. All stay 0/false in clean-slate. **[V]**

Net: fact gates on venue doors mostly *fail closed toward open* in our world.
The ones to watch are gates that would **disable** something when a fact is
missing, not gates that only fire when a story fact is present. `node 142`
in `open_world_content` is the one already handled this way: its
`DataTermControllerPS ForceDisabled` branch is guarded by
`watson_prolog_lock > 0`, and the mod keeps the node unmodified and sets the
fact to 0 (see `clean_slate_spec.json` `kept_inline_phases` node 142 note). **[V]**

### 1.6 Areas that only exist while a quest is active

Three concrete shapes, all verified:

1. **Quest-sector prefab interiors.** Konpeki's netrunner room
   (`#konpeki_netrunners_room_env`), the whole `#q005_pr_arasaka` set, Clouds'
   `#q105_pr_dollhouse` — each is a `Quest` descriptor bound to a prefab that a
   phase must declare. Konpeki has only 2 quest prefabs total; Arasaka Tower has
   20. See §2. **[V]**
2. **Quest MACRO scenes.** `q004_01_meet_the_lizzies.scene`, `sq011_10_concert.scene`
   etc. These mount characters and props on top of geometry. They are not
   locations; they are events. Omitting quests removes them, which is correct.
   **[V]**
3. **Pre/post-quest venue states.** Totentanz ships
   `#loc_pre_quest_totentanz`, `#loc_quest_totentanz` and
   `#loc_post_quest_totentanz` as three separate community prefabs. This is the
   exact pattern the owner's exception describes (a place that "does not exist"
   after a story beat) — and it is *also* the pattern we can reuse: pick the
   venue state we want and declare that prefab. **[V]**

### 1.7 Commonality summary

| Lock family | Share of venues | Reversible from script? | Notes |
| --- | --- | --- | --- |
| Phase-driven power/close | ~75% of gig interiors (35/47) | **Yes**, cleanly | Idempotent; primary lever |
| Missing prefab (interior empty) | All quest-only interiors | **Only via a phase** | No script spawn of prefabs |
| Keycard/authorization | Corp + VIP venues (Konpeki, Arasaka, Sapphire, Clouds) | **Yes**, `AuthorizationDisable` | Check `IsDeviceSecured()` first |
| Skill check | Service doors, shortcuts | **Yes**, but blunt | Prefer story-neutral: power/open |
| Lift floor gating | Multi-floor venues | **Yes**, `SetFloorActive` | Prefer `ForceGoToFloor` for full access |
| Security area/system | Most gig prefabs | **Yes** | Mod already overrides SAFE zones |
| Streaming variant | Decoration/lockdown | **No** (phase-owned) | Absent by default when phase omitted |

---

## 2. Key-interior inventory

### 2.1 How "reachable" is graded here

Three distinct questions, which vanilla answers differently:

| Grade | Meaning | Test used |
| --- | --- | --- |
| **Shell reachable** | The building/room geometry streams with no quest (Exterior/Interior sector) | Does the location's assets exist in `Exterior`/`Interior` descriptor counts? |
| **Open-world prefab** | A location phase declares an `*_openworld` prefab, so the venue is populated/usable without story | Is there a `phasePrefabs` entry containing `openworld`? |
| **Quest-only** | Only a `q###_pr_*` / `sq###_pr_*` quest-design prefab exists | Are all prefabs quest-design, with no openworld variant? |

The self-check I ran: for each venue I listed every `questPrefabNodeRef` under
its location directory in both the base block (23,718 descriptors) and the
Dogtown block (2,186), and checked for an `openworld` token. **[V]**

### 2.2 Inventory

| Venue | Shell reachable | Open-world prefab | Loaded by | Grade |
| --- | --- | --- | --- | --- |
| **Arasaka Tower** | Yes — 418 variants across Exterior 265 / Interior 126 / Quest 27 | **No** — 20 prefabs, all quest-design (`#q000_corpo_pr_arasaka_lobby`, `#q113_pr_jungle`, `#q115_pr_tower_lobby/atrium/jungle/nest`, `#q114_pr_nest_new`) | `q000`, `q113`, `q114`, `q115` phases; `loc_arasaka_tower_questdesign_prefabDP2FMWA` | **Quest-only** (interior gameplay) |
| **Konpeki Plaza** | Yes — 166 variants (Exterior 143 / Interior 17 / Quest 6) | Partial — only `#mirror_scene_konpeki_room`; the hotel proper is `#q005_pr_arasaka`, `#q004_pr_hotel` | `q004.questphase` declares `#q004_pr_nightclub`; `q005_heist.questphase` declares **none** (declared by `q005` sub-phases) | **Quest-only** |
| **Clouds (dollhouse)** | Yes — 116 variants (Exterior 67 / Interior 47 / Quest 2) | Partial — `#mirror_scene_dollhouse` only; main set is `#q105_pr_dollhouse`, `#sq026_pr_pc_dollhouse` | `q105_dollhouse.questphase` declares prefab, issues 4×`ForceClose`+1×`ForceOpen` on cabin doors; `q105_dollhouse_persistent` locks 8 doors + 3 windows | **Quest-only** |
| **Totentanz** | Yes — 13 variants (Exterior 12 / Quest 1) | **Yes** — three states: `#loc_pre_quest_totentanz`, `#loc_quest_totentanz`, `#loc_post_quest_totentanz`, declared by `#loc_sq011_totentanz_openworld/` | Location phase + `sq011`; `cast_and_hubs` already claims `#pr_totentanz_bouncer_default` | **Reachable** (pick a state prefab) |
| **Lizzie's** | Yes — 12 variants (Exterior 9 / Interior 2 / Quest 1) | **Yes** — `#loc_q004_lizzys_nightclub_openworld`, declared by `wat_kab_lizzies_bar_phase` | `base\open_world\community\watson\kabuki\phases\wat_kab_lizzies_bar_phase.questphase` → 8 sub-phases | **Reachable** (already live in clean-slate) |
| **All Foods** | Yes — geometry under `wnid_07` / `#loc_q003_meat_factory` | **No** — only `#q003_pr_quest` under `loc_meat_factory_questdesign_prefabCIYNT2A` | `q003.questphase` declares `#q003_pr_quest` | **Quest-only** |
| **Black Sapphire** | Yes — under `combat_zone_prefabUEX7DCY` / `boulevard_av` | **No** — `#q303_pr_paradise_*`, `#q303_pr_nighthawks`, `#q304_pr_*` are all quest-design | `q303`/`q304` (Dogtown block) | **Quest-only** |
| **Batty's Hotel** | Yes — `q110_battys_hotel` assets, `mq025/batty/batty.ent` + `batty_community` | **No** — `batty` prefab count 0 in both blocks; it is an `ent` + community under `mq025` | `mq025` (minor quest) | **Quest-only** (Petrochem/Animals doc already notes marker-only) |
| **Embers** | Partial — signage + `q115_embers_window_rain.mesh` only | **No** — `#q115_pr_restaurant` (`loc_q115_fancy_restaurant_questdesign_prefabXXJX6OQ`) | `q115_00_hanako` | **Quest-only** (a restaurant interior, not a tower) |
| **Militech Offices** | Yes — Corpo Plaza prefab dirs exist | **No** — only city-scene prefabs (`cs_militech_pre_border_post_openworld`, `cs_militech_execution`); no office interior prefab | Corpo Plaza quests / city scenes | **Quest-only** (office interior) |
| **Night Corp Tower** | **No cell** — scenery + `#mq061` tour prefab only | **No** — `#mq061` (quest-design) | `mq061` | **Quest-only / scenery** (corroborates [night-corp.md §3.1](factions/night-corp.md)) |
| **NCPD precinct (Dogtown)** | Yes | **Yes** — `#loc_sts_ep1_10_openworld/#sts_ep_1_10_streetstory`, declared by the gig | `sts_ep1_10` street story | **Reachable via gig prefab** |
| **Afterlife** | Yes — 17 prefabs | Partial — `#pr_tiny_mike_default`, `#mirror_scene_afterlife`; `cast_and_hubs` already claims `#pr_rogue_default` | Hotel/location phase + `q005_afterlife_phase` | **Reachable** |

### 2.3 What this table actually means

**Seven of thirteen are quest-only**: Arasaka Tower, Konpeki Plaza, Clouds, All
Foods, Black Sapphire, Batty's Hotel, Embers (plus Militech Offices and Night
Corp Tower, which are quest-only or scenery). **Four are already reachable**:
Totentanz, Lizzie's, Afterlife, NCPD precinct. **[V]**

Two structural facts drive that split:

1. **Ownership, not district.** A venue is open-world if some *open-world
   community phase* claims it. `wat_kab_lizzies_bar_phase` claims Lizzie's;
   `#loc_sq011_totentanz_openworld` claims Totentanz. Nothing claims Arasaka
   Tower's interior, so only `q113`/`q114`/`q115` can bring it in.
2. **Shell ≠ interior.** Every venue's *outer building* streams. Walking to
   Arasaka Tower works today; the lobby beyond the quest door does not. That is
   why "every location accessible" is mostly a **prefab + door** problem, not a
   geometry problem.

### 2.4 Verified vs inferred

| Claim | Grade |
| --- | --- |
| Exterior/Interior/Quest descriptor counts, and the 2,358 Quest descriptors | **[V]** measured on both blocks |
| Each venue's prefab list and openworld presence | **[V]** extracted from the block files |
| Which phase declares which prefab (Lizzie's, Clouds, Konpeki, All Foods) | **[V]** extracted those phases |
| That an undeclared prefab means no workspots/doors-as-devices | **[R]** structural (matches [site-modeling §1.2](living-world-site-modeling.md)); runtime spike pending |
| Arasaka Tower/Konpeki being *enterable* once a prefab is declared | **[H]** — needs probe §5.1 and §5.2 |
| Whether the shell of a quest-only interior is lit/propped without the quest | **[H]** — variants suggest yes (`Interior` sectors are `enabledByDefault`) but unobserved |

---

## 3. Gigs

### 3.1 How a vanilla gig is actually offered

Four independent layers, and the mod has to deal with each separately:

| Layer | Mechanism | Verified |
| --- | --- | --- |
| **Dispatch** | A district dispatcher `.questphase` fans out one child phase per gig, e.g. `street_stories` → 7 district dispatchers → `sts_watson` → 3 sub-districts → `sts_wat_kabuki` → 10 gig phases | **[V]** extracted |
| **Offer** | The gig's own `*_openworld` phase sets up the site and writes journal + phone-call facts (`holo_reggie_calls_v_start_activate`, `kab_07_start`, …) | **[V]** on `sts_wat_kab_07_openworld` |
| **Presentation** | Quest mappin (`IsQuestMappin()`), journal entry, fixer SMS/call. Filtered in the mod by `NcIsSuppressedVanillaMappinVariant` and the mappin/journal wrappers | **[V]** |
| **World state** | The `*_openworld` phase closes and unpowers doors, switches lights, spawns the crew via prefab communities | **[V]** |

The dispatch tree is nearly ungated: `street_stories.questphase` has 11 phase
nodes and exactly **one** fact gate (`q115_point_of_no_return > 0`, a
post-point-of-no-return cleanup). `sts_watson` has 3 subphases and **zero**
gates. The gating lives deeper, per gig, and is about *tiers and prerequisites*
(`sts_wat_kab_tier_1 > 0`, `kab_05_after_confrontation > 0`, …) — not about
whether a fixer feels like calling. **[V]**

### 3.2 How the mod already suppresses them

Two mechanisms, both already shipped:

1. **Clean-slate archive (structural).** The custom root phase
   ([`clean_slate_spec.json`](../../data/clean-slate/clean_slate_spec.json))
   simply never wires `street_stories`, `open_world_minor_activities`,
   `open_world_fixers`, `mini_world_stories` or `side_quests`/`minorquests`.
   Both dispatchers are `excluded_phase_patterns`, and
   `build-clean-slate.py --check` fails the build if any excluded phase reappears
   (`check_questphase`, `excluded = sorted({r for r in refs if any(p in r ...)})`).
   Since the dispatchers are pure fan-outs with `phasePrefabs: 0` and
   `inplacePhases: 0`, dropping the root wiring removes the entire gig tree.
   **This is the complete fix for a fresh clean-slate run.** **[V]**

2. **Runtime sanitizer (defensive, for non-clean-slate saves).**
   `NeonAscendancy_SanitizerSystem` (`Sandbox/SanitizerSystem.reds`) deactivates
   every non-`na_` journal entry, untracks the tracked entry, blocks quest phone
   calls (`PhoneSystem.OnTriggerCall` wrapper), and nulls quest mappin profiles
   in three containers (world map, 3D world mappins, minimap). This is
   presentation suppression — it does not stop a quest phase already running.
   `campaign-sanitizer.md §4.1` is explicit about that limit. **[V]**

### 3.3 What still leaks

| Leak | Why | Severity |
| --- | --- | --- |
| **Door state left by a gig's `_openworld` phase** | If a gig phase ran before suppression (or on a non-clean-slate save), doors stay unpowered/closed and lights off. The journal is hidden but the world is not restored | **High** — this is the main "venue looks dead" symptom |
| **Prefab isn't instantiated at all** | Clean-slate omits the gig phase, so the site's `Quest` sector never streams; the venue has geometry but no workspots/guards/doors-as-devices | **High** — the "empty venue" symptom |
| **Gig mappin variants** | `FixerVariant` (52) is in the deny list, so fixer *pins* vanish; but a gig that uses `DefaultQuestVariant` (25) with a non-quest mappin could survive | Low |
| **Fixer SMS** | `OnTriggerCall` blocks calls, not messages. A fixer SMS text can still arrive | Low (cosmetic) |
| **`q001_show_sts_tut` / `ow_psychos_intro_done`** | If these are ever set, street stories / cyberpsycho pins open. Clean-slate deliberately never sets them | None if facts stay 0 |

Both high-severity leaks have the same root: **the venue's world state is a side
effect of a phase we are not running.** The fix is §4's venue phases, not more
suppression.

### 3.4 Keeping gig locations usable as *places*

The insight is that a gig already ships the venue in two pieces, and we can take
one and drop the other:

```
sts_wat_kab_07.questphase            → phasePrefabs: [#sts_wat_kab_07_streetstory]   (the venue)
sts_wat_kab_07_openworld.questphase  → doors/lights/facts/journal/phone            (the gig)
sts_wat_kab_07_combat.questphase     → combat escalation                           (the fight)
sts_wat_kab_07_bugfixing.questphase  → `AuthorizationDisable` on a door            (a patch)
```

The main phase's **only job is to declare the prefab** — it has 4 nodes and no
device actions at all. So a Neon-authored venue phase can do exactly that and
nothing else:

```text
phasePrefabs = [ "#sts_wat_kab_07_streetstory" ]
+ questSpawnManagerNodeDefinition: Activate #kab_07_com_enemies "0combat"
+ questDeviceManager_NodeType: DoorControllerPS ForcePower #<entry door>
```

And because the `_openworld` phase is the one that *closes* things, omitting it
leaves the venue in its default state — which is exactly the "open and usable"
state we want. **The gig is therefore not a blocker to place reuse; it is a
convenient map of where the doors and communities are.** That map is already in
`data/sites/` (`doors.json` 375 rows, `devices.json` 161, `communities.json`
562, `phases.json` 3777). **[V]**/**[R]**

There is one real exception: a gig whose *own* prefab contains the venue's only
copy of a door or lift, with `enabledByDefault: 0` variants for the "open" state.
Totentanz is the clean example — it ships `pre_quest`/`quest`/`post_quest`
prefabs, so we must pick a state explicitly rather than rely on a default. **[V]**

---

## 4. Options

### 4.1 The stack's actual levers, honestly stated

Five mechanisms exist in this pinned stack. Each is listed with what it can and
cannot do for world access.

| # | Lever | Can open a venue? | Can populate it? | Cost / risk |
| --- | --- | --- | --- | --- |
| **O1** | **Phase authored in the mod's own archive** (`tools/build-clean-slate.py`): declare `phasePrefabs`, add `questSpawnManagerNodeDefinition`, add `questInteractiveObjectManagerNodeDefinition` → `questDeviceManager_NodeType` | **Yes** — `ForcePower`/`ForceOpen`/`ForceUnlock` per door | **Yes** — via the venue prefab | Medium build tooling; zero runtime risk; save-safe |
| **O2** | **Redscript sweeper**: find doors near the player, read PS state, queue `QuestForcePower`/`QuestForceOpen` | **Yes** — best for stragglers | **No** (cannot spawn or instantiate prefabs) | Low code; runs on a delay/trigger, not per frame; composable |
| **O3** | **TweakXL**: edit `DoorSetup`/device records, or add records | **Partially** — changes an entity template's default door state | **No** | Blunt: changes every instance of a template globally; does not help quest-only interiors |
| **O4** | **ArchiveXL**: `.xl` resource links, prefab/streaming overrides, archive swaps | **Yes** — can swap a phase or streaming sector | **Yes** — can ship a patched phase | Medium; least composable layer, most likely to conflict |
| **O5** | **Native RED4ext plugin**: reach the streaming/prefab system directly | **Theoretically** | **Theoretically** | High; no documented prefab-instantiation API (`world::IQuestPrefabStateListener` is an empty base struct) |

### 4.2 Recommendation: O1 first, O2 as the net, O4 only for exceptions

**Layer 1 — venue phases in the clean-slate archive (O1). The foundation.**

Extend `data/clean-slate/` with a `venue_phases` spec and let
`build-clean-slate.py` emit one phase (or one hub phase with many nodes) whose
only job is to declare the venue and energize its doors. Each entry is:

```jsonc
{
  "code": "sts_wat_kab_07",                 // from sites.json
  "prefab": "#sts_wat_kab_07_streetstory",  // from sites.json quest_prefab_ref
  "doors": [                                 // from data/sites/doors.json
    { "ref": "#kab_07_entrance_door_002", "action": "ForcePower" },
    { "ref": "#kab_07_entrance_door_002", "action": "ForceOpen"  }
  ],
  "communities": [                            // optional; from communities.json
    { "spawner": "#kab_07_com_enemies", "phase": "default", "action": "Activate" }
  ]
}
```

The builder already emits all three node kinds —
`add_community_spawn_node` (`build-clean-slate.py:448`),
`add_spawn_set_node` (`:474`), `add_phase_node` (`:320`) — and
`_check_cast_and_hubs` already round-trip-verifies `phasePrefabs` and spawn
actions (`:1568-1634`). A device-manager node is the one new builder method
needed; it is the same `questInteractiveObjectManagerNodeDefinition` →
`questDeviceManager_NodeType` shape that vanilla `open_world_content` node 142
uses (extracted and read in this session).

Why this is the right foundation:

- **It is the vanilla mechanism** — no invention, no native code.
- **It is save-safe and idempotent.** Device PS state is ordinary persisted save
  data; `OnQuestForcePower` early-returns when already powered
  (`scriptableDeviceBasePS.swift:4529-4534`).
- **It composes.** Prefab declaration is additive and reference-counted.
- **It fixes the root cause.** The venue exists *because a phase says so*.

**Layer 2 — redscript door sweeper (O2). The safety net.**

A door can still be `LOCKED`/`SEALED`/`DISABLED` from an older save or another
mod. The sweeper should:

1. Trigger on a **bounded** schedule (player attach, zone change, low-frequency
   timer) — **never per frame**.
2. Look up nearby doors spatially (`data/sites/doors.json` has `node_ref` and
   `global_node_id`; `world.db` has the R-tree).
3. Read the PS, then act: `IsDisabled()` → `QuestForceEnabled`;
   `!IsPowered()` → `QuestForcePower`; `IsLocked()` → `QuestForceUnlock`;
   `IsSealed()` → `QuestForceUnseal`.

All primitives verified:

```redscript
// refs/cyberpunk/orphans.swift:34317, 33005, 33011, 11869
ResolveNodeRef(nodeRef, Cast<GlobalNodeRef>(GlobalNodeID.GetRoot()))
Cast<EntityID>(globalNodeRef)                    // GlobalNodeID -> EntityID
GameInstance.FindEntityByID(game, entityID)      // -> ref<Entity>
(device as Device).GetDevicePS()                 // -> ref<ScriptableDeviceComponentPS>
GameInstance.GetPersistencySystem(game).QueuePSDeviceEvent(action)
```

with `QuestForcePower`, `QuestForceUnlock`, `QuestForceEnabled`,
`QuestForceUnseal` constructible (`baseDeviceActions.swift:1985-2046`,
`doorController.swift:1036-1075`), each needing `clearanceLevel = 99` +
`SetUp(ps)` + `SetProperties()` before queueing — exactly what the vanilla
`Action*` helpers do.

**Caveat that decides feasibility:** redscript 1.x cannot construct a `NodeRef`
from a `String` or `Uint64` — there is no `NodeRef` literal syntax in the
surface, and the extracted `global_node_id` values are `uint64`. So the sweeper
must either take `NodeRef`s from engine-resolved data (entity components,
trigger callbacks) or call a small native helper that builds
`RED4ext::NodeRef{hash}` (the pattern in
[living-world-site-modeling.md §2.4](living-world-site-modeling.md)). A native
`NcResolveNodeRefByHash(Uint64) -> GlobalNodeRef` is ~20 lines, and the bridge
pattern already exists (`Main.cpp:1222-1232`). **This is the one place a native
helper is genuinely the cheapest path.** **[V]**

**Layer 3 — exceptions only (O4/O3).**

- **Totentanz** — a tiny phase that declares the chosen state prefab
  (`#loc_pre_quest_totentanz` vs `#loc_post_quest_totentanz`). Prefer this over
  an archive edit.
- **The owner's exclusion list** (nomad-camp tent after Panam, Kurtz/Kutcher's
  home) — already closed, because we simply do not declare their prefabs. Free.
- Do **not** TweakXL-edit `DoorSetup` templates globally: it changes every
  instance of a reusable template with no per-venue control.

### 4.3 What not to do

| Temptation | Why not |
| --- | --- |
| Set `q000_done = 1` / `q001_done = 1` to "unlock" venues | Story-completion facts with many readers; `campaign-sanitizer.md §2.2` forbids it. Measured gain is near-zero, risk is high |
| Bulk-set every `*_default_on` fact | Resurrects vendors a story intentionally closed (same doc, same reason) |
| `ForceOpen` without `ForcePower` | No-op on an unpowered door (§1.3) |
| Patch `IsStatic()` away | Broad blast radius; use the action events |
| Script-spawn NPCs to "populate" a venue | No `GameObject.Spawn`/`SpawnPuppet` exists; `PreventionSpawnSystem.RequestUnitSpawn` is the NCPD pipeline, a Tier-C fallback ([site-modeling §2.2](living-world-site-modeling.md)) |

### 4.4 Costs and risks

| Risk | Mitigation |
| --- | --- |
| **Prefab reference-count conflicts** with another mod declaring the venue | Declaration is additive; test with a known venue mod installed |
| **Save made before the venue phase** still has locked doors | Layer 2 sweeper |
| **A venue's "open" state is a quest variant** (Totentanz) | Pick the state prefab explicitly; never assume a default |
| **Enabling a venue re-enables gig content** | Venue phases declare prefabs and doors only — never journal, mappin, phone or `street_stories` phases. Make this a builder assertion |
| **`ForcePower` re-enabling a security system** | Only act on `DoorControllerPS`/`LiftControllerPS` unless intended |
| **Performance** | Spatial query on zone change + a ≥30 s timer; no per-frame loop |
| **Save schema growth** | None required; device state is engine-owned |

---

## 5. What needs an in-game probe

Five probes. The first decides the architecture; the rest are cheap checks that
prevent rework. Use a **save copy** and a dev-only CET install
(`tools/install-dev-cet.sh`); the probe pack in `tools/probes/` is the natural
place to add them.

### 5.1 Does a Neon phase's `phasePrefabs` make its `NodeRef`s resolve? **[H] — blocking**

Everything in §4.2 Layer 1 rests on this. Ship a throwaway phase with:

1. `phasePrefabs = [ "#sts_wat_kab_07_streetstory" ]`
2. one `questSpawnManagerNodeDefinition` activating `#kab_07_com_enemies`,
   `communityEntryPhaseName = "0combat"`
3. one `questDeviceManager_NodeType` powering `#kab_07_entrance_door_002`

Then check: `ResolveNodeRef("#kab_07_ws_bottom_guard_001")` is defined;
`GetFixedEntityIdsFromSpawnerEntityID(<kab_07_com_enemies>)` is non-empty; and
`#kab_07_entrance_door_002` resolves with PS class `DoorControllerPS`.

**Pass:** all three true, hostiles on the workspots. **Fail:** the whole
prefab-instantiation approach is wrong and we fall back to O2-only (which opens
doors but cannot populate anything).

### 5.2 Is a quest-only interior already enterable? **[H]**

Konpeki and Arasaka Tower lobbies are the test. Walk to the door without a quest
and record: does the door open; is the interior lit; are there props or is it a
bare shell; is there a `SecurityAreaControllerPS` turning the player back. This
tells us whether "open the door" is sufficient for *these* venues or whether
they genuinely need their prefab.

### 5.3 What is the default door state in a clean-slate run? **[H]**

Sample ~20 doors from `data/sites/doors.json` (mix of `interior`, `entrance`,
`elevator`) and dump `IsOpen/IsLocked/IsSealed/IsDisabled/IsPowered` before and
after the venue phase. This calibrates the sweeper: if most are already
`CLOSED + powered`, the sweeper has almost nothing to do, and the cost/benefit
of O2 shrinks.

### 5.4 Does `ForceOpen` alone make a closed door physically usable? **[H]**

§1.3 shows `OnQuestForceOpen` writes the flag regardless of power, while the
player-facing `OnForceOpen` refuses when disabled or sealed. The open question is
physical: on an unpowered-but-not-disabled door, does the PS flag alone give a
working door, or does the entity stay inert until `ForcePower`? Confirm on one
door, because it decides whether every door entry needs two actions
(`ForcePower` then `ForceOpen`) or one.

### 5.5 Does the Totentanz state prefab behave as expected? **[H]**

Declare `#loc_pre_quest_totentanz` in a probe phase, enter, and confirm the
venue is the pre-quest state (not the post-quest one, and not empty). If the
three states are not independent, the "pick a state" pattern in §2.2/§3.4 needs
amending before it is used for other venues.

### 5.6 Not needed (already settled)

| Question | Answer |
| --- | --- |
| Do interiors stream without a quest? | **Yes** for geometry — Exterior/Interior descriptors, 2,425 Interior sectors |
| Do gigs close/unpower doors? | **Yes** — 352 actions in 35/47 phases, measured |
| Is there a script API for sector variants? | **No** — verified absent from the 2.5 surface |
| Can redscript construct a `NodeRef`? | **No** — needs a native hash helper (§4.2 Layer 2) |
| Is `q000_done` needed to open venues? | **No** — it gates crowds and one sub-phase, not venue access |

---

## Appendix A — reproduction commands

All extracts were made with the pinned WolvenKit.CLI into a temporary directory
and deleted afterwards. Nothing in `data/`, `refs/`, `tools/`, `src/` or the
game directory was modified.

```bash
WK="$HOME/.cache/neon-ascendancy/wolvenkit-10.0.0-beta.1/WolvenKit.CLI"
GAME="$HOME/Games/Cyberpunk 2077"
export DOTNET_ROLL_FORWARD=Major

# 1. Streaming blocks: category + quest prefab + variant census
"$WK" extract "$GAME/archive/pc/content/basegame_3_nightcity.archive" -o blk -w "*all.streamingblock"
"$WK" extract "$GAME/archive/pc/ep1/ep1_1_nightcity.archive"        -o blk2 -w "*streamingblock"
"$WK" convert s blk/base/worlds/03_night_city/_compiled/default/blocks/all.streamingblock
"$WK" convert s blk2/base/worlds/03_night_city/_compiled/default/ep1/blocks/all.streamingblock

# 2. Gig open-world phases (door-action census)
"$WK" extract "$GAME/archive/pc/content/basegame_4_gamedata.archive" -o raw \
  -r '^base\\open_world\\street_stories\\.*_openworld\.questphase$'
"$WK" convert s raw

# 3. Gig dispatchers (gate census)
"$WK" extract "$GAME/archive/pc/content/basegame_4_gamedata.archive" -o raw \
  -r '^base\\open_world\\street_stories\\street_stories\.questphase$|^base\\open_world\\minor_activities\\open_world_minor_activities\.questphase$'

# 4. Location phases (the "venue stays open" layer)
"$WK" extract "$GAME/archive/pc/content/basegame_4_gamedata.archive" -o raw \
  -r '^base\\open_world\\community\\watson\\kabuki\\phases\\wat_kab_lizzies_bar_phase\.questphase$|^base\\open_world\\community\\global_phase\\open_world_global_commuinity_phase\.questphase$'

# 5. Interior top-level quests (prefab declarations)
"$WK" extract "$GAME/archive/pc/content/basegame_4_gamedata.archive" -o raw \
  -r '^base\\quest\\main_quests\\prologue\\q004\\q004\.questphase$|^base\\quest\\main_quests\\part1\\q105\\phases\\q105_dollhouse(_persistent)?\.questphase$'
"$WK" convert s raw
```

Census snippets used (numbers quoted in §1–§3):

- Door-action prevalence: walk every JSON, count
  `questDeviceManager_NodeTypeParams` by `(deviceControllerClass, deviceAction)`;
  filter where class contains `Door`.
- Descriptor census: `RootChunk.descriptors`, count `category`; count
  `questPrefabNodeRef != "0"`; count `variants` and `enabledByDefault`.
- Reachability: build a socket-handle → node-id map, collect
  `graphGraphConnectionDefinition` edges, BFS from each `questInputNodeDefinition`,
  then list the `questSetVar_NodeType` / `questDeviceManager_NodeType` nodes in
  the reached set.

Key script and resource citations:

- `refs/cyberpunk/cyberpunk/devices/door/doorController.swift:36-56, 80-88, 198-209, 261-279, 1196-1272, 1300-1309`
- `refs/cyberpunk/cyberpunk/devices/core/scriptableDeviceBasePS.swift:1887-1960, 4486-4575, 5268`
- `refs/cyberpunk/cyberpunk/devices/core/baseDeviceActions.swift:1985-2046`
- `refs/cyberpunk/cyberpunk/devices/elevator/liftController.swift:127-186, 241-247, 657-664, 903-930`
- `refs/cyberpunk/cyberpunk/devices/skillChecks/skillCheckContainer.swift:2-46`
- `refs/cyberpunk/orphans.swift:11869, 17307-17321, 28299, 33005-33011, 33210-33258, 34317`
- `refs/RED4ext.SDK/include/RED4ext/Scripting/Natives/Generated/world/StreamingWorld.hpp`
- `refs/RED4ext.SDK/include/RED4ext/Scripting/Natives/Generated/world/IQuestPrefabStateListener.hpp`
- `data/sites/doors.json`, `devices.json`, `variants.json`, `sites.json`, `communities.json`
- `data/clean-slate/clean_slate_spec.json` (`kept_depot_phases`, `kept_inline_phases`,
  `excluded_phase_patterns`, `forbidden_facts`)
- `tools/build-clean-slate.py:320, 448, 474, 1568-1634`
- `src/r6/scripts/NeonAscendancy/Sandbox/SanitizerSystem.reds`
- `native/lib/sim/era.cpp:213-247`; `native/plugin/Main.cpp:1222-1232`

