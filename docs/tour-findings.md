# Tour findings backlog

Problems the owner finds on the venue tour, waiting for a batched fix pass
(subagents). Fixed items move to the changelog. The raw sources are the
probe's `notes.log`, `lookat.log` and `tour.log` (checklist marks) in the CET
mod folder; `tools/venue-tour-report.py` summarises them.

Toured stops are listed in `data/venues/tour_done.json` and left out of the
tour. Owner calls from the tour are in `docs/design/owner-decisions.md`
section 12.

## Leg 1 (2026-11-26): 28 stops, Yucca to the Stadium

Each batch owns its files, so agents can work in parallel in one checkout.
Door ids come from `lookat.log`.

| Batch | Venue | Finding |
| --- | --- | --- |
| A doors | `mq303_shanks_store` | Front door sealed (`15265392420759227790`). |
| A doors | `q303_nighthawks_bar` | Both doors to the boiler-room hideout will not open (`13400032501529177363`, `830512930825541107`). |
| A doors | `sts_cct_dtn_04` | Ground-floor lift works, but its gate does not open (`5474562508547213513`, unpowered). |
| A doors | `sts_hey_spr_06` | The street door opens from inside but not from the street (`7285717058466177479`). |
| A doors | `mq306_tech_expo` | A door near (-2400, -3095, 144) and the front gate stay sealed; the door was never in scope. |
| A doors | `q000_border_crossing` | The checkpoint office double door: which side does it open onto (marked a problem)? |
| A doors | `q104_gas_station` | Garage doors and shutters start down and must be forced; they should work as normal garage doors. |
| B checkpoint | `q303_combat_zone_gate` | The Dogtown pedestrian scanners finish their animation but never unlock the door, either way; the western gate does the same. |
| C1 Pacifica | `q110_pacifica_mall` | Many NPCs missing; the boxing robot fights nothing; the hall, gym, robot and garage groups marked as problems. |
| C1 Pacifica | `q305_netwatch_ambush` | One NPC sits on air near (-2772, -2460, 17); the interior near (-2779, -2498, 18) has no lighting; check which building is the Pistis Sophia. |
| C2 people | `sts_hey_spr_06` | Not normal business: no arguing customer, staffing marked as a problem; the netrunner den at (-2250, -400, 1). |
| C2 people | `q000_border_crossing` | Civilians stand on the far side (away from the city) looking at nothing; guards are fine. |
| C2 people | `megabuilding_a` | `#mq011_com_contestants` and `#q001_com_residents_gate` marked as problems; loading `#q001_pr_megabuilding` brings the fistfight tutorial sub-prefab. |
| D1 leftovers | `sts_ep1_botanic_gardens` | The wall authorization console shows a yellow quest icon; using it gets V stuck. |
| D1 leftovers | `q111_pumpstation` | A cyberpsycho site with a body and clues everywhere. |
| D1 leftovers | `q302_goodnight_charlies` | A mine at the entrance (-1673, -2426, 40) kills V and leaves broken HUD elements. |
| D2 services | `pr_stadium` | Vendors still do not work at all. |
| D2 services | `mq305_wanted` | The lift is doubled (a second lift door inside the first); the street door will not open; the wiki places it in Wellsprings. |
| E scene | `q302_squat` | The squat's lights are off; Jacob and James's flat is very dark. |
| E scene | `sts_cct_dtn_05_luxury_yacht` | No yacht exists; the boarding, security room and aft door checks all failed. |

The fix reports go in `~/.cache/neon-ascendancy/extracts/venues/research/fixes/`.

### Leg 1 status (fix pass done, awaiting the second tour)

Fixed in data or code, all of them awaiting the second tour: batches A,
C1, C2, D1, D2 and E, and the west half of B. Agent reports (with the
second-tour checks) are A-doors, B-checkpoint, C1-pacifica, C2-people,
D1-leftovers, D2-services and E-scene in the fixes folder.

Still open:

- **Dogtown main checkpoint** (-1797, -2250): the pedestrian door belongs to
  the combat tower's sectors (`#q303_dvc_combat_tower_main_door`), not
  `q303_combat_zone_gate`; it needs its own fix in that venue.
- **Border crossing car queue**: the passengers were removed because their
  cars never spawn. Restoring the queue needs `questSpawner` Activate in
  the builder (C2 report has the list).
- **Spot maps**: the miner loses the spot map of 1,880 communities whose area
  node is in another `always_loaded` sector; the cause of most "(N
  unmapped)" labels. Fix the miner and re-mine (C2 report).
- **Container-zone vendors**: same scene gap as the stadium, and their
  `cz_con_*_default_on` facts are not set (D2 report).
- **Other cyberpsycho sites**: eight hustle set pieces leave bodies and
  mines on by default (D1 report); fix each where a venue sits on one.
- **Stadium crowd**: 31 expected records missing (gangs, Kurtz's people,
  stall staff); check on the second tour.

## Sweep (2026-11-27): 153 stops, unattended

The first full sweep flagged 193 devices. Five agents triaged them
(reports and proposals in the fixes folder's `sweep/`): 23 door overrides
and 13 lift/terminal power overrides went in; the rest are vanilla-locked,
dressing or close terminal pairs. Owner calls are items 177 to 182.

Still open:

- **Miner stale prefab names**: `mine-venues.py` writes some device rows
  under a prefab no sector holds (the shrine's `prefab2FYTMBQ`), so their
  scope hashes are phantoms. Fix the miner and re-mine (S2 report).
- **Roadhouse garage door** (`#q000_dvc_garage_door`): its controller comes
  from an entity template, so the sweep never logged it; check by look-at.
- **Dogtown main checkpoint**: running the `q303_paradise` venue phase is
  the fix (it already unlocks the door), not an override (S3 report).
- **Sweep radius**: Wired Head's stop also sweeps the Scavenger Den's
  garage gate; cap overlapping radii.

## Tours from 2026-11-27

Three short tours replace the long checklist tour (playbook section 7):
the node tour (81 simulation nodes not yet toured), the hub tour (8 stops)
and the access tour (47 stops, 71 checks: every door override and the lift,
floor and route checks in `data/venues/access_checks.json`). Civilian
venues get no tour. 18 nodes have no tour position yet, so they are in no
tour until one is found.

## Strip-list pass (2026-11-27)

Nine agents matched 166 venues to their classification strip lists and
resolutions (reports in the extract cache's `research/strip/`). 37 approved
entries and 2 hand-built venues (Batty's rooftop, Black Sapphire) changed; most items were already absent.
Owner calls are items 183 to 193. Left for later:

- **World-placed mines and traps** (Wraiths and Scavenger sites): not in any
  venue toggle; they need a runtime look.
- **Konpeki Plaza**: the lockdown dressing is not identified (item 166 keeps
  it a separate job).
- **Stacks container yard** (`q301_crashsite_way_up`): a kept vanilla phase
  may bring back the removed Scavenger crew.
- **Node garrisons and generated lieutenants**: wait for the simulation.
- **Marked Ragnar** (`sts_hey_spr_01`, near -2076, -958): two agents could
  not find what gives it the investigation marker. On the next visit, log a
  look-at on it ("Neon: log look-at"); the id and state settle the fix.
- **Stripped Shion** (`sts_hey_spr_03`, node 1034 of exterior_-39_-15_0_0):
  its variant group does not match the streaming block; check whether it
  shows in game. The stripped Colby there is deleted (world_deletions.json).

## Second tour (re-test)

- H10 lobby residents staring through the open gate (`fa60430`).
- Wilson's shooting range sealed behind an auth module: the seal rule (`fa60430`).
- Yucca garage duplicate gate and sealed roller door (`36b1ebe`).
- Yucca radio tower fence gate and SoCal border office doors: door overrides
  (`36b1ebe`).
- Tech Expo gate doors and Damir's clinic on the map.
- Probe: noclip, notes and checklist reopening (`f3d0008`, `7a7c8be`); the
  invisible-to-AI toggle (`b3b55f0`).
- Everything the leg 1 fix pass changes.
- Everything the sweep fix pass changes: each override's "Second tour" line
  is in the sweep reports. Lifts: ride H10's apartment lift, the den lift,
  the Haven clinic lift and the braindance studio lifts. The Badlands
  sts_bls_ina_03 service lift (no lift device in the data) and the
  Arasaka tower lift to floor 33.
