# Neon Ascendancy

Neon Ascendancy is a Cyberpunk 2077 sandbox overhaul mod where the player founds
and grows a corporation or gang—adding organization management, territory
control, a stock market, and dynamically generated economic, espionage, and
military missions.

> **Status:** Early bootstrap (`0.0.0-dev`). Toolchain, docs, and versioning
> policy are in place; gameplay systems are not yet implemented.

## Quick start

```bash
tools/install-frameworks.sh   # install pinned RED4ext/redscript/ArchiveXL/TweakXL (game closed)
tools/fetch-refs.sh           # clone local decompiled game scripts & SDK refs into refs/
tools/verify.sh               # format check + compile against the game's 2.5 script cache
tools/deploy.sh               # deploy src/r6/scripts/NeonAscendancy/*.reds into the game
```

## Documentation

- [`docs/modding.md`](docs/modding.md) — toolchain, Wine/Linux notes, logging, and stack constraints.
- [`docs/versioning.md`](docs/versioning.md) — SemVer, save schema versioning, and framework pinning policy.
- [`AGENTS.md`](AGENTS.md) — engineering principles, testing policy, and contributor/agent rules.
- [`.agents/skills/redscript/SKILL.md`](.agents/skills/redscript/SKILL.md) — redscript 1.x language, hook, and persistence guide.
