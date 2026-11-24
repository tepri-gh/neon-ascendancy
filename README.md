# Neon Ascendancy

Neon Ascendancy is a Cyberpunk 2077 sandbox overhaul mod where the player founds
and grows a corporation or gang—adding organization management, territory
control, a stock market, and dynamically generated economic, espionage, and
military missions.

> **Status:** `v0.1.0` playable slice in development (`0.0.0-dev`). Native C++20
> SQLite core (`NeonAscendancy.dll`), `world.db` extraction pipeline, Campaign
> Sanitizer, World Map control-center pins, Pause Menu entry, and combat raid
> territory-flip loop are implemented and verified offline; in-game gameplay
> testing is in progress.

## Quick start

```bash
tools/install-frameworks.sh   # install pinned RED4ext/redscript/ArchiveXL/TweakXL (game closed)
tools/fetch-refs.sh           # clone local decompiled game scripts & SDK refs into refs/
tools/fetch-native-deps.sh --xwin # fetch pinned SQLite3, RED4ext.SDK, RedLib, xwin splat
tools/verify.sh               # redscript 1.x format check + compile against 2.5 cache
tools/verify-native.sh        # world.db --check + Linux ctest + Windows /MT DLL PE gates
tools/deploy.sh               # deploy .reds, tweaks, NeonAscendancy.dll, and world.db
```

## Documentation

- [`docs/roadmap.md`](docs/roadmap.md) — Phase 0 foundations, `v0.1.0` vertical slice, causal pillars, and deferred systems.
- [`docs/architecture.md`](docs/architecture.md) — system layers, causal event bus, native SQLite core, and performance rules.
- [`docs/glossary.md`](docs/glossary.md) — canonical domain terminology.
- [`docs/research/README.md`](docs/research/README.md) — Phase 0 engine, world-data, DB, and map-overlay research reports.
- [`docs/modding.md`](docs/modding.md) — toolchain, Wine/Linux notes, logging, and stack constraints.
- [`docs/versioning.md`](docs/versioning.md) — SemVer, save schema versioning, and framework pinning policy.
- [`AGENTS.md`](AGENTS.md) — engineering principles, testing policy, and contributor/agent rules.
- [`.agents/skills/redscript/SKILL.md`](.agents/skills/redscript/SKILL.md) — redscript 1.x language, hook, and persistence guide.
