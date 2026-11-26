# Neon Ascendancy

Neon Ascendancy is a Cyberpunk 2077 mod where the player founds and grows a
corporation or gang. It adds organization management, territory control, a
stock market, and dynamically generated economic, espionage, and military
missions. The campaign is disabled; existing factions, spawns, and locations
are reused.

## Before you start

1. Read `AGENTS-LOCAL.md` (gitignored) if it exists.
2. Read any nested `AGENTS.md` in the directory you are editing.
3. Read `docs/modding.md` before changing `tools/` or `.reds` files.
4. For `.reds` work, read `.agents/skills/redscript/SKILL.md`.
5. Read `docs/versioning.md` before bumping versions, changing persisted save
   fields, or updating pinned frameworks.
6. Read `docs/venue-playbook.md` before venue, door, community or spawn work
   (`data/clean-slate/`, venue code in `tools/build-clean-slate.py`). Add new
   lessons there when a venue fix teaches one.
7. Before planning or implementing a feature, read the relevant design,
   roadmap, architecture, and glossary docs under `docs/` when they exist. If
   scope is missing or ambiguous, ask instead of inventing it.

## Repository map

- `src/r6/scripts/NeonAscendancy/` — redscript sources (`.reds`).
- `tools/` — install, verify, lint, format, deploy, and reference scripts.
- `tools/lib/versions.sh` — single source of truth for pinned game/framework/CLI versions and checksums.
- `.agents/skills/redscript/SKILL.md` — redscript 1.x coding, hook, and persistence rules.
- `docs/` — modding setup, versioning, design, roadmap, architecture, glossary.
- `VERSION` and `CHANGELOG.md` — mod release version and changelog.
- `refs/` — decompiled game/SDK references (gitignored).
- `dist/` — compile output (gitignored).

## Core engineering principles

Follow this loop on every task: **make it work -> make it right -> verify**.

- **Work in small, verifiable units.** Finish and verify one small change before
  starting the next.
- **Get the data shape right first.** Model domain types so illegal states are
  hard or impossible to represent. Validate external/game data at boundaries,
  trust it inside, and keep domain logic in pure functions separate from game
  hooks.
- **One decision in one place.** Do not duplicate constants, rules, or version
  pins across files.
- **Subtract before you add.** Remove dead or redundant complexity first.
  Prefer existing game systems and installed frameworks over new abstractions.
  Ship the smallest clean change that solves the problem.
- **Fix root causes, not symptoms.** Reproduce failures and fix the underlying
  cause. A guard that only hides a crash is not a fix. Never silence compiler
  errors or warnings.
- **Question broken assumptions.** If two fixes built on the same assumption
  fail, stop, write down that assumption in one sentence, and rethink before
  patching again.
- **Keep state safe and idempotent.** Setup, restore, and deploy operations
  should produce the same result if run twice or retried after failure. Avoid
  sharing mutable state across callbacks/threads without one clear owner.
- **No unapproved dependencies.** Do not add dependencies, frameworks,
  Codeware (until a released version supports redscript 1.x), or test
  infrastructure without asking.

## Testing

- Add unit tests only where they assert observable behavior of a real system
  through its public interface.
- Good candidates are pure domain logic: market calculations, territory state
  transitions, mission constraints, and save serialization.
- Do not test generated bindings, framework plumbing, module registration, or
  trivial delegation; compile/lint already covers those.
- Do not add removal or absence tests that assert a deleted feature, symbol,
  or code path stays gone. Those encode history, not behavior.
- Do not add broad test scaffolding, low-value smoke tests, or duplicate
  coverage to raise a metric. Test system boundaries and invariants, not every
  branch or trivial accessor.
- Redscript has no unit-test runner today. Until it does, use
  `tools/verify.sh` and targeted in-game checks. Add a real test harness only
  when there is behavior worth testing.
- Do not add mutation testing, coverage, CRAP/dryer/mutator, or bespoke
  quality checkers; that work is deferred.

## Verify

- `tools/verify.sh` must pass before claiming code work is done.
- For behavior changes, deploy with `tools/deploy.sh`. In-game verification
  checks `r6/logs/redscript_rCURRENT.log` (compile log), `red4ext/logs/`
  (loader log), and actual in-game behavior (or the configured runtime debug
  logger; see `docs/modding.md`).
- Report static checks separately from in-game verification.
- Do not launch the game unless asked.
- An LSP is optional. If configured, treat it as a hint layer; `tools/verify.sh`
  remains the source of truth.

## Versioning and git

- Follow `docs/versioning.md` for `VERSION`, `CHANGELOG.md`, save schema
  migrations, and pinned framework bumps.
- Commit often in small, ordered commits once `tools/verify.sh` passes.
- Each commit message must state **why**, **what changed**, and **how it was
  verified**.
- Push verified commits when a logical unit is complete. Never force-push
  `main`.
- Never commit game files, Wine prefixes, binaries, `refs/`, `dist/`, or
  `AGENTS-LOCAL.md`.

## Hard constraints

- Target Cyberpunk 2077 + redscript 1.x stack pinned in `tools/lib/versions.sh`
  (see `docs/modding.md`); Codeware-free until an upstream release supports
  redscript 1.x.
- The game runs offline: no Steam, CDPR account, or game network.
- This repo holds sources, scripts, and docs only.
