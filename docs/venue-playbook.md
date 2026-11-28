# Venue Playbook

How to make a quest-only venue accessible and populated in the clean-slate
world, and the rules we learned the hard way. Read this before changing
`data/clean-slate/venue_phases.json`, `data/clean-slate/cast_and_hubs.json`,
or the venue code in `tools/build-clean-slate.py`.

Background research: [`research/world-access.md`](research/world-access.md)
(lock mechanisms, options). This playbook supersedes its §5 open probes where
they overlap.

## 1. What a venue needs

Every venue fix so far came down to four ingredients. Vanilla quest phases
already define all four; we copy them, never invent them.

| Ingredient | Vanilla source | Spec key |
| --- | --- | --- |
| Building sections (interiors, props) | a phase's `phasePrefabs` | `prefabs` |
| People: crowds, staff, guards | `questCommunityTemplate_NodeType` (spawner ref + entry + phase) | `communities` |
| Named NPCs (Woodman, Hansen, Dexter) | `questSpawnSet_NodeType` (reference + entry + phase), sometimes a community | `spawn_sets` |
| Door and device state | `questDeviceManager_NodeType` (controller class + action) | `doors` |
| Baked geometry states (shutters, barricades, dataterms) | `questTogglePrefabVariant_NodeType` | `variant_toggles` |

## 2. How the builder wires a venue

- **One quest phase per venue**: `mod\neon_ascendancy\venue_<code>.questphase`.
  All venue phases fan out from one gate pause (`gate` in the spec). A broken
  venue can then only empty itself.
- **Parallel branches, never serial chains.** Per venue:
  hub → branch fact →
  1. every community and spawn-set activation as its own leaf, at boot;
  2. variant toggles at boot, with no proximity wait;
  3. `_prewait` → proximity wait on a device → `_prox` → communities and spawn
     sets re-issued as leaves, plus the device actions as a leaf.
- **Debug breadcrumbs.** `debug_fact_prefix` makes the builder set
  `<prefix>_branch`, `_prewait`, `_prox`, `_reached` and `_done`. Add the
  prefix to `VenueProbe.reds`, and the probe logs them once a minute to
  `red4ext/logs/neonascendancy-*.log` as `VariantToggle[<prefix>]: ...`. That
  shows exactly where a branch stops.
- `--check` enforces the topology: one owner per prefab, leaves with exactly
  one incoming edge, and re-issue counts.

## 3. Rules, each learned from a real failure

**Phases and prefabs**

1. **A phase that fails to instantiate runs nothing, silently.** Symptom:
   `branch=0`. Usually one of rules 2–3.
2. **A prefab declared twice breaks the phase**, whether in one phase, across
   venue phases, or against a kept vanilla phase or `cast_and_hubs`. Each
   prefab gets one owner. If another phase already owns it, give the venue no
   `prefabs` and set `deferred_prefab_owner` to the owner.
   Declaring a prefab a *kept vanilla phase* already loads is redundant
   rather than fatal: hand-built Totentanz declares `#loc_pre_quest_totentanz`,
   which `wat_nid_phase` also loads, and it works. Omit such prefabs; activate
   only the people. Which vanilla loads are live in the clean slate is decided
   by `tools/mine-venues.py` gate analysis: traversal from a phase's inputs
   stops at pause nodes, and at a condition node's True branch, whose fact
   condition needs a fact the clean slate never sets: forbidden facts, and
   any fact nothing can set (not an initial fact, not set by game or mod
   scripts by name, not set by a reachable fact node in a kept phase). Erring
   towards "gated" is the safe direction: it costs at most a redundant
   activation, while wrongly "open" leaves a venue empty. Note that a phase node's `phaseInstancePrefabs`
   load when the node itself is reached. A `q000_done` pause *inside* the
   node gates only its contents: the border crossing's open-world section
   loads, while its guards inside wait on `q000_done`.

3. **`#` short refs only resolve for authored (tagged) node names.** Untagged
   nodes (`..._prefabXXXXXXX`) need the full `$/03_night_city/...` path. Take
   it from the streaming block (`all.streamingblock`, a descriptor's
   `questPrefabNodeRef` or a variant's `nodeRef`). The builder rejects untagged
   `#` refs.
4. **A serial chain stalls if any spawn or device node never completes.** Use
   parallel leaves (§2).

**Timing and streaming**

5. **Variant toggles work at boot, without proximity** (the Watson barricades
   proved it).
6. **Communities need activating twice: at boot, and again after
   proximity.** On a fresh start, a one-shot boot activation misses venues
   that haven't streamed in yet.
7. **Device actions need the entity streamed in**, so they run after the
   proximity wait.
8. **Proximity anchors must be device entities** (a door, an alarm, a
   dataterm), not workspots. A workspot anchor never fired at Clouds.

**People**

9. **Pick community phases by their workspot, not by their name.** A phase is
   a set of spots, and each spot plays a workspot animation.
   - `start`, `bar`, `end` and similar phases usually use `routine\...`
     workspots (sit, lean, use a tablet).
   - `hostile`, `after_*` and lockdown phases use
     `generic__stand_ground_gun__nervous__*` or `patrolling\..._agitated_shuffle`.
     NPCs on those look alert, crouched or "sheltering", even when not hostile.

   At Clouds, `after_woodman` looked harmless by name but is the
   post-interrogation lockdown. See §4.2 for how to check.
9a. **Entry `None` with phase `None` and `Activate` switches on a whole
    community**, every entry in its initial phase (`entriesInitialState`).
    It is not a reset. The Totentanz DJ and crowd run this way
    (`#com_totentanz`). The catalogue marks these `whole_community: true` and
    lists each entry's initial phase, so check their postures there.
10. **Drop combat, hostile, scene, cutscene and interrogation phases** unless
    one is chosen on purpose and its workspot is checked. Example: Woodman's
    `q105_interrogation_friendly_start` spawn set is idle behind his desk.
11. **Named NPCs often come from spawn sets, not communities.** Woodman is
    `#woodman`, Hansen is `#kurtz` / `q303_restaurant_host`. Copy vanilla's
    exact reference, entry and phase. The cast layer (`cast_and_hubs.json`)
    holds city-wide named NPCs; venue phases hold venue staff.

11a. **Population priority (owner rule).** When an area has to cap how many
    groups are active (spawn budget, performance, overlapping venues),
    keep combat groups first: netrunners above all, then other fighting
    groups (guards, security, gangers, soldiers, police), then civilians
    (staff, patrons, crowds). Combat groups still use relaxed, non-hostile
    phases. The catalogue tags each entry with `role` (`netrunner`,
    `combat`, `civilian`, `vehicle`) from its character record name.

**Doors and devices**

12. **Door policy** (the owner's, recorded as `door_policy` in the spec):
    - Doors are closed by default but usable: enable and power them, and
      unlock only where there is otherwise no way through.
    - Never `ForceOpen`.
    - Doors with an in-world way through stay exactly vanilla: a terminal, a
      keycard somewhere in the world, a quickhack, or a Technical or Body
      check. That covers locks only: nothing in the world opens a seal, so
      a sealed, impassable door is always unsealed (Wilson's range in H10
      stayed shut behind its auth module, tour 2026-11-26).
    - When the "other way in" is not obtainable in our timeline (no keycard,
      a prologue-only authorization), list the door's logged entity id in
      `data/venues/door_overrides.json`. `door-scope` generates it into
      `DoorScope.reds`, and the policy disables authorization, unlocks and
      unseals it, in or out of scope. Still never force-opens.

    The engine's own "no way to open" test is `doorController.swift:84`:
    `IsLocked() && !IsAuthorizationValid() && !canPlayerToggleLockState() &&
    !HasAnySkillCheckActive() && !CanCreateAnyQuickHackActions()`. The
    look-at logger prints those inputs. The only exception so far is the
    Black Sapphire sneak-in route.

    **The runtime door policy applies this automatically**
    (`World/DoorPolicy.reds`, gated by fact `na_door_policy`, which dev
    debug sets). On every door that streams in, it acts only on
    quest-driven doors in scope (`World/DoorScope.reds`, generated by
    `tools/venue-proposals.py door-scope`). It enables and powers the door,
    re-checks a second later (skill checks and quickhacks only register on a
    live device), then unlocks or unseals only if `DoorControllerPS.IsStatic()`
    says the door is impassable and there is no authorization module and no
    controlling terminal. Every decision is logged as `DoorPolicy: ...` in
    `red4ext/logs/neonascendancy-*.log`. Venue specs and research proposals
    therefore do not list door actions any more; they list
    `door_exclusions` (rooms that must stay shut) and `door_notes`.

    A sweep flag is a lead, not proof that a door is inaccessible. The sweep
    does not inspect terminal parents, and a one-sided door may deliberately
    have an in-world remote opener. On the 2026-11-27 sweep the Yucca gate
    `10942343670595111412` had a terminal parent; H10 door
    `12144628006029586807` and shutter `750585353481470118` reported
    `IsStatic=false`, which also accounts for a player-toggleable lock. The
    latter shutter's repeated appearances in the report are the same entity,
    not separate doors. Confirm the terminal's actual controls and reachability
    before treating a terminal parent as a working way in: a parent alone does
    not establish either. Inspect the one-sided H10 secret-room door
    `6373481765164401677`, nightclub door `14118118983733731532`, and Dogtown
    door `10846427555440147780` from both sides before overriding them.
    The same sweep's proximity pairs also need inspection: the Arasaka hotel
    pair `6790515536193496286` / `6191024671720459010` have different
    appearances and elevations; the metal-club pair `11883500528457144420` /
    `16335784949598343898` comprise a regular door and a lift door; and the
    Glen terminals `3984133746229174344` / `3984134845740802555` are 0.48 m
    apart vertically. Proximity alone does not establish duplicate geometry or
    identify which device, if any, should be removed.
13. **Lifts work everywhere** (owner decision 58, 2026-11-27): no area is
    out of reach unless it has strict lore implications we cannot remove
    (the Space Force One crash site, the Cynosure bunker). At runtime every
    lift car and floor terminal is enabled, powered, switched ON (a car
    only moves when ON, and `ForceEnabled` leaves a disabled car OFF) and
    has its authorization turned off, and every lift door is enabled and
    powered
    (`DeviceOverrides.reds`, `DoorPolicy.reds`). Never write a lift, floor
    terminal or lift door as "kept vanilla" in a venue entry. Floor access
    comes from the floor terminals (`liftController.swift`,
    `GetFloorAuthorizationFromSlaves`), so a keycard-only floor opens too.
    The exceptions are lift groups of excluded and deferred venues, plus
    `data/venues/lift_exclusions.json` for any other lore-sealed lift;
    `door-scope` grows each to its whole group (car, terminals, lift doors)
    from the world device registry. A single floor stays vanilla when
    vanilla never makes it usable (owner, 2026-11-27: if no vanilla state
    or quest, base game or Phantom Liberty, ever enables a lift entry, it
    leads somewhere never designed to be entered): a `floors` entry in the same file, grown only to that
    floor's lift doors. The policy never shows a hidden floor or activates
    an inactive one, so those stay as vanilla leaves them.
14. **Baked shutters are mesh (`worldCookedStaticMeshNode`), not devices.**
    Only a variant toggle opens them (Black Sapphire tower gate).
15. **Never touch journal, map pin, phone or holocall controllers.** The
    spec's `forbidden_*` lists enforce this, and `allowed_device_controllers`
    lists the non-door devices we may drive.

**Phantom Liberty (Dogtown)**

16a. **Check which quest roots the save actually runs.** Clean Slate redirects
    `ep1.gamedef` to its own game definition. Recent Clean Slate saves had
    `ep1_side_content = 1` and recorded `ascendancy.quest` as a quest root,
    with no `ep1.quest` root. The miner's assumption that the EP1 root is
    always available needs runtime confirmation for any venue that relies on it.
    Dogtown's street dynamic events are explicitly wired as a kept phase.
    The 2026-11-26 playtest confirmed populated streets and dynamic events,
    with no PL story, gigs, fixer calls or protest at the gate.

16b. **The Dogtown checkpoint needs its open-world phase and clearance fact.**
    Vanilla sets `ep1_side_content = 1` in `q302_04_squot.scene`.
    The fact releases node 8 of `combat_zone_gate.questphase`, which starts
    the two vehicle loops and the pedestrian loops. Clean Slate attaches that
    phase to `ascendancy.quest` with ArchiveXL, which also starts the
    attachment once on restore for older saves. The Clean Slate bootstrap
    supplies the clearance fact on older saves with Phantom Liberty installed.
    The vanilla phase owns the four vehicle barriers and the combat variant.
    The 2026-11-26 playtest confirmed vehicle scans in both directions.
    ArchiveXL's runtime log confirmed the phase attached, and the playtest
    autosave recorded one vehicle crossing into Dogtown.
    To verify in game, drive a civilian car through the western checkpoint in
    both directions and check that the scans play and the barriers cycle.
    The game increments `by_car_dogtown_crossed` and `by_car_night_city_crossed`
    on the respective crossings.

**Content that lives elsewhere**

16. The Dogtown vendors are in `ep1_vendors.questphase`, gated by facts; see
    the spec's `notes` entry `dogtown_vendors`.

## 4. Finding the data

Extracting game data uses the pinned WolvenKit CLI
(`~/.cache/neon-ascendancy/wolvenkit-10.0.0-beta.1/WolvenKit.CLI`, run with
`DOTNET_ROLL_FORWARD=Major`). Never commit extracted files. Local extract
locations are listed in `AGENTS-LOCAL.md`.

### 4.1 Quest phases

Extract the `.questphase` files from the base and EP1 archives, then
`convert serialize` them to JSON. For a venue:
- collect the prefabs it instantiates. A phase declares them in two places:
  its own `phasePrefabs`, and `phaseInstancePrefabs` on each
  `questPhaseNodeDefinition` in a parent graph (instantiated while that node
  runs). Open-world sections such as `#loc_q000_border_crossing_openworld`
  load the second way, often behind `q000_done`, which the clean slate never
  sets. The catalogue marks each prefab's `kinds` (`phase`, `instance`);
- collect every `questCommunityTemplate_NodeType`
  (`spawnerReference`, `communityEntryName`, `communityEntryPhaseName`,
  `action`);
- collect every spawn set, device action (`deviceControllerClass`,
  `deviceAction`, `objectRef`) and variant toggle;
- note which phase owns each item. That phase's name says what it's for
  (setup, mood, combat, leave).

### 4.2 Community definitions and their workspots

1. **Entries and records.** Community templates live in
   `always_loaded_1.streamingsector` as `worldCommunityRegistryItem` (entries,
   `characterRecordId`, phases, `entriesInitialState`). Find the right one by
   searching for an entry name.
2. **Spots.** The matching `worldCompiledCommunityAreaNode` (same sector,
   same `communityId` hash) maps each entry and phase to `spotNodeIds`
   (`worldGlobalNodeID` hashes).
3. **Workspots.** Convert the venue's sectors and match the
   `nodeData[*].globalNodeId.hash` values. `nodes[nodeIdx]` is a
   `worldAISpotNode` whose `spot` names the `.workspot` file. That path
   decides rule 9.

Sector buffers are compressed, so byte-grepping `.streamingsector` files for
hashes or names finds nothing. Convert them first.

If a scan over the extracted sectors hangs at 100% CPU (mostly kernel time),
suspect one damaged copy, not the tool. On 2026-11-25 one file's reads ended
at 36 KB of its 194 KB, and every reader (grep, ripgrep, Python) spun on it
forever. Find such files with a per-file timeout:
`find . -name '*.streamingsector' -print0 | xargs -0 -P8 -n1 sh -c 'n=$(timeout 5 cat "$1" | wc -c); [ "$n" = "$(stat -c %s "$1")" ] || echo "$1"' _`.
Move the bad file aside and re-extract it from the game archive.

### 4.3 Which sectors belong to a venue

`all.streamingblock` (base and EP1) lists every sector with its category,
`questPrefabNodeRef` and variants. Filter by the venue's prefab path.

### 4.4 Mapping an in-game object to a ref

The look-at logger prints an entity's 64-bit id. Static entity ids are the
FNV-1a 64 hash of the node's full ref path with the `#` characters removed
(`NcHashNodeRefPath` in `native/plugin/Main.cpp`). Hash the `nodeRefs` of the venue's sectors and match the id. The
Afterlife back-room door was found this way.

### 4.5 In-game evidence

- `lookat.log` (in the CET probe folder): class, id, appearance, position,
  PS state, door open/locked/sealed, `skillCheck`, `quickhack`, `authValid`,
  and NPC record and affiliation.
- `red4ext/logs/neonascendancy-*.log`: `VariantToggle[...]` breadcrumbs,
  `VenueProbe[...]` and `Dataterm[...]` lines.

## 5. Checklist for a new venue

1. Find the vanilla phases that own the venue (§4.1). List prefabs,
   communities, spawn sets, devices and toggles.
2. Check prefab ownership against kept vanilla phases, `cast_and_hubs` and
   other venues (rule 2).
3. Resolve every ref; use full `$/` paths for untagged nodes (rule 3).
4. Choose community phases by workspot (rules 9–10).
5. Classify each door against the door policy (rules 12–13).
6. Pick a device as the proximity anchor (rule 8).
7. Set `debug_fact_prefix` and add it to `VenueProbe.reds`.
8. Build, run `--check` and `tools/verify.sh`, deploy, then read the
   breadcrumbs and the look-at log in game.

## 6. Venue catalogue and walkthroughs

Two local tools feed venue research. Their output is never committed;
`AGENTS-LOCAL.md` records where it lives.

- **`tools/fetch-wiki-walkthroughs.py`** downloads the Cyberpunk wiki's quest
  and location pages (main jobs, side jobs, gigs, minor jobs, minor
  activities, district locations, stores, vendors, apartments) as raw
  wikitext, plus `index.json`. GameFAQs guides are from 2021 and refuse
  automated downloads, so the wiki is the walkthrough source. Quest pages
  carry `baseid` (e.g. `q105_02_jigjig`), which joins them to quest phases.
- **`tools/mine-venues.py`** builds `catalog.json` from the extracted quest
  phases, the community registry, the streaming blocks and (after the
  `sectors` stage) every converted sector. One record per venue (top-level
  location prefab, sibling sub-prefabs merged):
  - owning quests and phases, and matching wiki pages;
  - prefabs, community activations (with character record, spot count,
    workspots and posture), spawn sets, device actions and variant toggles,
    each with the phases that own it;
  - `community_options`: every phase each used community entry defines, with
    its posture and workspots and whether vanilla activates it. Pick ambient
    phases here (rule 9). The relaxed choice is often a phase no quest
    activates, such as Clouds' `guard_vipentrance_01/start`;
  - `posture: unknown` means no spot map was found. About 1,700
    communities, mostly Phantom Liberty, have no community area node in any
    converted sector (where their spots live is still open), and some
    vanilla quests activate phases that do not exist. Check those on the dev
    tour;
  - `venue_inferred: true` on items whose ref is not yet resolved to a path
    and was attached to the venues its phase touches. Treat those as
    unverified until the `sectors` stage has run;
  - `anchor_candidates`: up to five named devices within 150 m of the venue's
    spots, nearest first, as full paths, for venues vanilla drives no
    device at. The builder accepts `$/` anchors;
  - `tier`: `individual` (one research agent each: an authored location used
    by a main job, side job, minor job or gig, with people, devices or
    sections to restore) or `batch` (open-world areas, hustles, apartments,
    small sites; several per agent). Owner decisions in
    `data/venues/triage_overrides.json` replace the tier with `excluded`
    (no research) or `deferred` (a later dedicated pass).

  Stages: `phases`, `communities`, `sectors` (slow: converts every sector
  holding spots, devices or community areas; resumable), `catalog`.

  Four sectors refuse WolvenKit 10.0.0-beta.1 conversion. Three hold device
  data cooked with older class names (`APChallangeContainer`,
  `DemolitionContainer`) where the current game classes declare
  `HackingContainer` and `EngDemoContainer`. The game tolerates the
  mismatch; WolvenKit's strict RTTI check refuses the file. The fourth (EP1
  `exterior_-40_-38_0_0`) fails inside WolvenKit's own JSON step. None of
  the four holds community areas; they cost a few devices and spots.

- **Empty venues get no entry.** A venue that is intact and empty in
  vanilla, or already filled by kept phases, has nothing to restore. The
  builder rejects an entry that declares nothing, so `approve` skips it and
  `check` warns. Put its open questions into `data/venues/tour_checks.json`
  on the nearest stop instead (lesson from Dry Creek, wave 11).
- **Legacy community actions.** Vanilla writes some community actions as
  `questLegacy_NodeType` (same fields as `questCommunityTemplate_NodeType`).
  The miner reads both; any new tool that scans community actions must too
  (lesson from 7th Hell, wave 11).

- **Tag aliases in sector refs.** A sector `nodeRefs` entry can read
  `<path>;#tag`. The node's id is FNV-1a 64 of `<path>` alone, `#` removed
  (checked against `globalNodeId`, 324 of 324 refs in one sector), and
  `#tag` is its name. The miner used to index only paths ending in `#tag`,
  so 150 quest-driven doors (Jacked and Coke's front door, the q112 safe
  house entrances, the H6 lift) never reached the door scope (wave 12).

- **Name collisions drag in other venues' cast.** q003 tags generic TV
  prefabs `#tv_1_q003`, so any venue with the same TV prefab inherits All
  Foods' spawn sets (DumDum, Jackie, Royce) as `venue_inferred`. Treat those
  as noise: check every `venue_inferred` spawn set's own quest before
  keeping it (waves 11-13: Cytech, the Kenmore Diner, Dry Creek).

- **An anchor inside an off-by-default variant never resolves.** If a
  venue's only device sits in a quest variant that stays off (the Kabuki
  container yard's GPS trackers in `during_sts`, the Kenmore Diner's camera
  in its DLC range), the proximity wait never fires and only the boot
  activation runs. Anchor on the nearest ungated device instead, even a
  building away, and widen `proximity_anchor.within` to cover the venue
  (`approve` honours it). If none exists, add a fresh-start tour check
  (wave 15).

- **A kept vanilla phase can undo a venue's variant toggles.** Boot order
  between phases is not defined. `cct_dtn_phase` hides the North Oak
  yacht's whole party layout at boot, and the venue showed it at boot too,
  so there was sometimes no yacht at all. The builder now re-issues every
  venue's toggles after its proximity wait, so ours land last. When
  proposing a toggle, check the catalogue `toggles` owners for a kept phase
  that sets the opposite value (leg 1 tour).

- **An empty authorization module is not a way in.** The policy counted
  any authorization module as "another way in" and kept the lock, but many
  quest doors ship a module with no keycard or password (Shank's, the
  Nighthawks safehouse). It now asks `IsAuthorizationValid()` (leg 1 tour).

- **Lift doors only get enable and power.** Their lift and floor
  terminals open them; unlocking one can leave it open on a floor the car
  has left. An owner override still unlocks one (the Wellsprings lobby).
  Every lift door outside a lore-sealed group is in the policy's scope,
  catalogued or not (rule 13).
  A lift that looks doubled is usually two door entities in one shaft, one
  of them still quest-locked, not a second prefab.

- **One-sided doors.** A door typed interactive on one side and remote or
  none on the other opens only from inside (the Berkeley Ave junk shop).
  For an owner override the policy gives both sides the usable type; never
  for shutters or lift doors.

- **Vendors need their scenes.** A stall's trade interaction runs through
  its vendor scene; the spawn set alone gives a vendor you cannot trade
  with. `dogtown_vendors.json` `scenes` starts each stadium stall's scene.

- **Dead quest marks.** Some devices bake `markAsQuest` and a forced
  personal link for a gig step we never run (yellow icon, V freezes on
  jack-in). List them in `data/venues/device_quest_marks.json`;
  `DeviceOverrides.reds` clears both when the device attaches.

- **Hustle set pieces leak into neighbouring venues.** NCPD hustle
  dressing (bodies, clue props, armed mines) is often on by default, with
  only an unkept cleanup phase hiding it. Toggle the hustle's own loot and
  devices variants to vanilla's post-hustle values (the pump station).

- **Tour stop radius.** A `tour_stop` pins the scan to 40 m unless it
  sets `radius`; a spread-out venue needs a larger one (Pacifica mall).

- **Lifts are not doors** (sweep 2026-11-27). The door policy only touched
  `Door` entities, so lift cars (`LiftDevice`) and floor terminals
  (`ElevatorFloorTerminal`) a skipped phase would enable or power stayed
  dead, and their doors with them: H10's apartment lift, the netrunners'
  den, the Haven clinic, the braindance studio. Rule 13 now covers every
  lift; `LiftPolicy:` lines in the native log show what it changed.
- **Windows are doors, scope is not.** `Window` extends `Door`, so the
  policy and owner overrides reach a `WindowControllerPS`; but `door-scope`
  keeps only `DoorControllerPS` rows, so a window a street story powered
  needs an override (the Little China dojo's roof windows).
- **Most blocked devices are fine.** Of the 193 the first full sweep
  flagged, about 30 needed a fix: the rest were vanilla-locked rooms,
  display doors and shutters, or close pairs of floor terminals. Triage
  each against its sector node and the phase that drives it before
  opening anything.
- **The catalogue's tiers are as old as the last mining run.**
  `load_catalog` applies `triage_overrides.json` on top, so a venue the
  owner excluded since then drops out of the door scope and keeps its lifts
  vanilla without a re-mine (the crash site, the bunker, the Spidertank
  hall had stayed in scope).
- **Catalogue paths can carry a `;#tag` suffix.** The entity id hashes the
  path without it; `door-scope` strips it (it hid the braindance studio's
  two doors). The miner can also record a stale prefab name (the shrine's
  `prefab2FYTMBQ` rows, real `prefab62JAV6Q`), which makes a phantom id:
  check the id against the sweep or look-at log before trusting the scope.

## 7. Dev tour and playtest notes

Dev-only tooling in the CET probe (`tools/probes/neon_probe.lua`). Deploy with
`tools/deploy-probe.sh` after `tools/install-dev-cet.sh` has installed CET.

- **Stops** come from `tools/venue-proposals.py tour-stops`. It writes
  `tools/probes/tour_stops.json` and `.lua` with every hand-built and approved
  venue with a known position, plus the scan radius and expected characters.
  Approved entries use the catalogue key from their filename because short
  refs can recur at unrelated venues. The generator uses the people's spots
  or the anchor device. To use a safer arrival point or fill a missing
  position, set `tour_stop.position` and record its vanilla node and sector in
  `tour_stop.source`. Approval copies this field from the proposal into the
  venue entry. Regenerate after every approval wave.
- **Tour** (hotkeys "Neon: tour start/resume", "Neon: tour skip stop",
  "Neon: tour stop"; console `p.tour_start("code")`). It teleports to each
  stop, waits 20 s for streaming, then writes one JSON line per stop to
  `tour.log`: every NPC in the radius with record, affiliation, high-level
  state, stance, workspot, attitude and dead flag, plus the expected records
  it did not find. Run it in a dev session (dev debug arms the venue gate and
  the door policy).
- **Checklist** (owner request, 2026-11-26). Each stop carries a
  `checklist`: three base checks (normal business, people at their posts,
  you can get in), the entry's `tour_checks` lines, one "calm and on post"
  item per spawner with `needs_tour_check` entries, and every
  `source.open_questions` line (first sentence as the label, full text
  behind it). `data/venues/tour_checks.json` adds checks that belong to no
  venue entry (an excluded venue's leftovers) to a named stop. On the tour,
  a stop with a checklist waits after its scan. Open the CET overlay, mark
  each item OK or Problem, then "Save + next stop" (or the skip hotkey).
  "Neon: checklist here" opens the nearest venue's list without the tour.
  Saved lists go to `tour.log` as `checklist` lines. When a research agent's
  open question is really a thing to look at, put it in the proposal; a
  check the owner should repeat at a hand-built venue goes in its
  `tour_checks`.
- **Sweep first, tour second** (owner, 2026-11-26: 28 hand-toured stops
  took hours, mostly on doors and lifts). "Neon: sweep start/resume" or the
  panel's "Sweep all stops" visits every stop unattended, including toured
  ones, with god mode and invisibility on, and no checklists. On top of the
  NPC scan it logs every door, lift and lift terminal in the radius with
  its raw state (power, lock, seal, valid authorization, skill check,
  quickhack, lift door, side types). The report then flags `STUCK` (doors
  the policy or an override covers that still stop the player),
  `BLOCKED-UNSCOPED` and `DUPLICATE` (two devices of one kind within
  0.75 m), and ends with one table of devices to fix. Fix those in a batch,
  then hand-tour only the flagged stops and the things a script cannot
  judge (lore, lighting, a pose, whether it reads as normal business).
  Toured stops are listed in `data/venues/tour_done.json`; the tour skips
  them and the sweep does not. Venues without a known position (28) are
  not swept; give them a `tour_stop`.
- **CET events in the probe:** CET keeps one callback per event per mod, so
  a second `registerForEvent` for the same event silently replaces the
  first (the tour's `onUpdate` broke noclip). Register handlers through the
  probe's `on(event, fn)`, which fans one CET registration out to all of
  them.
- **Notes** ("Neon: playtest note"). The hotkey stamps the position and the
  nearest stop; open the CET overlay, type the note and press Save. Notes go
  to `notes.log`.
- **Report**: `tools/venue-tour-report.py` combines `tour.log`, `notes.log`
  and the native log's `DoorPolicy:` lines (which carry door positions) into
  `~/.cache/neon-ascendancy/extracts/venues/tour-report.md`. One section per
  stop; flags EMPTY, ALERT, HOSTILE, NO-WORKSPOT, DEAD, MISSING, DOORS, NOTES,
  PROBLEMS and UNCHECKED (checklist items marked Problem or left unmarked).
  Fix what it flags, record the lesson here, and subtract what the owner
  marks as wrong.
