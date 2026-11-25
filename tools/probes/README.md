# Phase 0 Dev-Only In-Game Probes

`neon_probe.lua` is a small, **dev-only** Cyber Engine Tweaks (CET) helper for
running the Step 0.1 campaign-sanitizer and Step 0.2/0.5 empirical checks
documented in [`docs/research/campaign-sanitizer.md`](../../docs/research/campaign-sanitizer.md).

It is **not** part of the shipping mod.

## Setup

```bash
tools/install-dev-cet.sh
```

This installs pinned CET (`tools/lib/versions.sh`) and copies `neon_probe.lua`
to `<game>/bin/x64/plugins/cyber_engine_tweaks/mods/NeonAscendancyProbe/init.lua`.

## Usage in-game (always test on a save copy)

Open the CET overlay console and run:

```lua
p = GetMod("NeonAscendancyProbe")
p.help()
```

Follow the 10-minute verification matrix in
[`docs/research/campaign-sanitizer.md`](../../docs/research/campaign-sanitizer.md) (§6.11):
`p.snapshot()`, `p.classify()`, `p.unlock_minimal()`, `p.unlock_act2()`,
`p.audit_quests()`, `p.suppress_quests()`, `p.audit_mappins()`,
`p.audit_johnny()`, `p.test_johnny_off()`, `p.audit_dialog()`, `p.watch_calls()`.

## Look-at logger (on-site identification)

Bind **Neon: log look-at** (and optionally **Neon: log player position**) in the
CET overlay → Bindings. Look at a door, device, NPC or object and press the key.
The line (`LOOKAT class=… id=… app=… pos=… player=… ps=… open=/locked=/…`, plus
`record=`/`affiliation=` for NPCs) goes to the CET console and
`…/mods/NeonAscendancyProbe/lookat.log` (flushed per line). `LOOKAT nothing` means the
target is static world geometry (a baked mesh), not an entity. After editing this
file, reinstall with `tools/install-dev-cet.sh` or copy it to the mod's
`init.lua`, then use CET's "Reload All Mods".

## Noclip

Bind **Neon: noclip toggle** in CET Bindings. While noclip is on, your normal
movement keys drive it: forward/back/strafe follow the camera, Jump goes up,
Crouch goes down, hold Sprint (Shift) for fast. Collision and gravity are
ignored (the player is teleported each frame). Toggle off to land.
