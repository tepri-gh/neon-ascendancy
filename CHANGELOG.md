# Changelog

All notable changes to Neon Ascendancy are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
this project adheres to [docs/versioning.md](docs/versioning.md).

## [Unreleased]

### Added
- Initial repository structure, redscript 1.x CLI tooling (`tools/`), modding
  documentation (`docs/modding.md`), versioning policy (`docs/versioning.md`),
  and cross-agent redscript skill (`.agents/skills/redscript/SKILL.md`).
- Target stack pinned in `tools/lib/versions.sh`: Cyberpunk 2077 2.5,
  RED4ext 1.31.1, redscript 1.0.2, ArchiveXL 1.28.11, TweakXL 1.12.2
  (Codeware-free), plus dev/build pins for CET 1.38.1, WolvenKit.CLI
  10.0.0-beta.1, xwin 0.10.0, SQLite 3.54.1, RED4ext.SDK, and RedLib.
- Architecture, roadmap, glossary, and Phase 0 empirical research reports
  under `docs/`.
- Dev-only CET installer (`tools/install-dev-cet.sh`) and Phase 0 in-game
  probe pack (`tools/probes/neon_probe.lua`).
- Canonical SQLite schemas (`data/schema/world_v1.sql`,
  `data/schema/playthrough_v1.sql`), EP1-over-base world extractor
  (`tools/extract-world.py`), extracted Night City seed data (`data/*.json`),
  and deterministic `world.db` compiler (`tools/build-world-db.py`).
- Native C++20 simulation and SQLite storage core (`native/lib/sim`,
  `native/lib/store`), offline Linux unit tests (`native/tests`), cross-compiled
  Windows x64 `/MT` RED4ext + RedLib plugin (`native/plugin/Main.cpp`), and
  automated native verification (`tools/verify-native.sh`).
- Initial redscript 1.x core foundation (`Core/Version.reds`,
  `Core/NativeBridge.reds`, `Sandbox/WorldEra.reds`,
  `Persistence/AnchorSystem.reds`).
