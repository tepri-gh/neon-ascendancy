# Tour findings backlog

Problems the owner finds on the venue tour, waiting for a batched fix pass
(subagents). Fixed items move to the changelog. The raw sources are the
probe's `notes.log` and `tour.log` (checklist marks) in the CET mod folder;
`tools/venue-tour-report.py` summarises them.

## Open

| Venue | Finding | Lead |
| --- | --- | --- |
| `mq306_tech_expo` | One door at about (-2400, -3095, 144) will not open. The policy never logged it, so it is outside the door scope. | Owner: "Neon: log look-at" on it for the entity id, then add it to `data/venues/door_overrides.json`. |
| `mq306_tech_expo` | Damir's clinic is not on the map; the gate-terminal question is still open. | Check after the seal fix (the gate doors were sealed). |
| `sts_ep1_botanic_gardens` | The wall authorization console shows a yellow quest icon; using it gets V stuck because the gig's trigger never fires. | Leftover gig interaction: find its mappin or journal and disable the device or its quest interaction. |
| `q000_border_crossing` | Civilians stand on the far side (away from the city) looking at nothing; guards are fine. | Probably the prologue queue posts: pick their calm phase or drop those entries. |
| `megabuilding_a` | `#mq011_com_contestants` (2 unmapped) marked as a problem. | Check posture and spots; drop or re-phase. |
| `megabuilding_a` | Loading `#q001_pr_megabuilding` also loads the fistfight tutorial sub-prefab. | Find a variant that hides it, or stop declaring the prefab. |

## Fixed, awaiting re-test

- H10 lobby residents staring through the open gate (`fa60430`).
- Wilson's shooting range sealed behind an auth module: seal rule (`fa60430`).
- Yucca garage duplicate gate and sealed roller door (`36b1ebe`).
- Yucca radio tower fence gate and SoCal border office doors: door overrides
  (`36b1ebe`).
- Tech Expo gate doors: sealed, covered by the seal rule (`fa60430`).
- Probe: noclip, notes and checklist reopening (`f3d0008`, `7a7c8be`);
  invisible-to-AI toggle (`b3b55f0`).
