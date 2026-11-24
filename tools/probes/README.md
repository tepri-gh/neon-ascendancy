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
