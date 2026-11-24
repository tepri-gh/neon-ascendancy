# Versioning Policy

This document defines how Neon Ascendancy versions releases, persisted save
state, and pinned Cyberpunk 2077 modding dependencies.

## 1. Mod Version (`VERSION` + Git Tags)

Neon Ascendancy follows [Semantic Versioning 2.0.0](https://semver.org/)
(`MAJOR.MINOR.PATCH[-prerelease]`).

- **Single source of truth:** [`VERSION`](../VERSION) at the repository root.
  When script sources expose a mod version constant, it must match `VERSION`.
- **Pre-release bootstrap:** `0.0.0-dev` until the first playable milestone
  (`0.1.0`) is tagged.
- **Pre-1.0 (`0.MINOR.PATCH`):**
  - Bump `MINOR` (`0.1.0 -> 0.2.0`) for new feature milestones or breaking
    save/state changes.
  - Bump `PATCH` (`0.1.0 -> 0.1.1`) for bug fixes and safe polish that do not
    break existing saves.
- **Post-1.0 (`MAJOR.MINOR.PATCH`):**
  - Bump `MAJOR` for save-breaking or major architecture-breaking changes.
  - Bump `MINOR` for backward-compatible feature additions.
  - Bump `PATCH` for backward-compatible bug fixes.
- **Pre-release suffixes:** `-dev` on unreleased branches when needed, or
  `-alpha.N` / `-beta.N` / `-rc.N` for test builds.
- **Git tags:** Tag releases on `main` with annotated tags named `vX.Y.Z`
  (for example `v0.1.0`).
- **Changelog:** Record user-visible changes, save-schema changes, and
  supported game/framework versions in [`CHANGELOG.md`](../CHANGELOG.md)
  (Keep a Changelog format). Move `[Unreleased]` entries under `[X.Y.Z] - YYYY-MM-DD`
  in the release commit.

## 2. Save Schema Version (`SCHEMA_VERSION`)

Persisted `ScriptableSystem` state changes independently of `PATCH` releases.
Track save compatibility separately using a monotonic integer:

- Define one root constant (e.g. `SCHEMA_VERSION: Int32`, starting at `1`) and
  store `persistent let m_schemaVersion: Int32` on the mod's root persisted
  `ScriptableSystem`.
- Increment `SCHEMA_VERSION` **only** when persisted field layouts, types, or
  meanings change. Do not bump it for pure behavior fixes that leave save data
  compatible.
- In `OnRestored(saveVersion: Int32, gameVersion: Int32)`:
  - If `m_schemaVersion == 0` (fresh save / first attach): initialize defaults
    and set `m_schemaVersion = SCHEMA_VERSION`.
  - If `m_schemaVersion < SCHEMA_VERSION`: run explicit, idempotent step-by-step
    migrations (`1 -> 2 -> ...`). During `0.x`, breaking migrations are allowed
    only when documented in `CHANGELOG.md` and handled cleanly (no silent half-migrated state).
  - If `m_schemaVersion > SCHEMA_VERSION` (downgrade): do not silently overwrite
    newer save data; refuse mutation or enter a safe read-only fallback.

## 3. Game & Framework Compatibility Pins

Cyberpunk 2077 patches frequently break native plugins and script layouts.

- **Single source of truth:** [`tools/lib/versions.sh`](../tools/lib/versions.sh)
  pins the target Cyberpunk 2077 version, framework versions, download URLs,
  and SHA-256 checksums. [`docs/modding.md`](modding.md) mirrors the
  human-readable summary table. Do not duplicate patch version numbers in
  `AGENTS.md` or skill files.
- **Upgrade discipline:**
  1. Bump pinned framework or game versions in their **own isolated commit**—never
     bundled silently into a feature commit.
  2. Update `tools/lib/versions.sh`, verify SHA-256 checksums, update the table
     in `docs/modding.md`, run `tools/verify.sh`, and confirm a clean in-game
     launch (`r6/logs/redscript_rCURRENT.log` + `red4ext/logs/`).
  3. Record the compatibility bump in `CHANGELOG.md`.
- **Codeware gate:** Do not add Codeware to `tools/lib/versions.sh` until an
  upstream release explicitly supports redscript 1.x and passes `tools/verify.sh`
  plus a clean game boot.
