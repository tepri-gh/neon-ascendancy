---
name: redscript
description: Write, review, compile, lint, format, deploy, and debug Cyberpunk 2077 redscript 1.x mods in this repo. Use for .reds files, @wrapMethod/@replaceMethod hooks, ScriptableSystem persistence, script compilation, or redscript errors.
---

# Redscript 1.x

Read `AGENTS-LOCAL.md` (if present) and `docs/modding.md` before changing code.
Work CLI-first: the commands below work under every agent harness. Pinned game,
framework, and CLI versions live in `tools/lib/versions.sh` (do not duplicate
them elsewhere).

## Toolchain

- Sources: `src/r6/scripts/NeonAscendancy/` (`.reds`).
- Format: `tools/format-redscript.sh` (check-only: `tools/format-redscript.sh --check`).
- Fast lint: `tools/lint-redscript.sh` (runs analysis with `-W unused_locals`, writes no bundle).
- Compile: `tools/check-redscript.sh` (writes `dist/final_patched.redscripts`; never touches `r6/cache/final.redscripts`).
- Verify all: `tools/verify.sh` (format check + compile).
- Deploy: `tools/deploy.sh` (copies only `.reds` files to `<game>/r6/scripts/NeonAscendancy/`).
- Vanilla scripts: `refs/cyberpunk` (files use `.swift` extension but contain REDscript). Fetch with `tools/fetch-refs.sh`.

`tools/lib/redscript.sh` checks both the CLI exit code and the
`Compilation successful` marker. An LSP is optional; `tools/verify.sh` is the
source of truth.

## Workflow

1. Find the original class, method, field, or event in `refs/cyberpunk`; read
   the method body and nearby helpers. Those files use 0.5-era decompiled
   syntax, so use them for APIs and behavior, not as a 1.x style guide.
2. Check installed dependency scripts under `<game>/red4ext/plugins/*/Scripts`
   and any installed mods in `<game>/r6/scripts` for existing hooks or name
   collisions.
3. Implement a narrow change in `src/r6/scripts/NeonAscendancy/` using 1.x
   style. Keep pure domain logic separate from thin game-hook adapters.
4. Run `tools/format-redscript.sh`, then `tools/verify.sh`. Fix all errors and
   warnings in this mod's files (warnings in third-party dependency scripts can
   be ignored unless caused by our hooks).
5. Deploy with `tools/deploy.sh`. Never launch the game unless asked; always
   report static verification separately from in-game verification.

## Hook rules

- Prefer `@wrapMethod` over `@replaceMethod`; wrappers compose with other mods.
- Every `@wrapMethod` must call `wrappedMethod(...)` with the exact original
  arguments unless replacing behavior is intentional—state that explicitly when
  it is.
- Never `@wrapMethod` or `@replaceMethod` `native` **functions**. Scripted
  (non-native) methods on `native` classes (such as `PlayerPuppet`,
  `ScriptableSystem`, or `inkGameController` subclasses) **can** be hooked, and
  `@addMethod`/`@addField` work on them (unless `importonly` blocks added
  fields).
- Match the original signature exactly: name, parameters, return type,
  static/instance shape, and visibility (overrides cannot narrow visibility).
- Prefix `@addMethod` and `@addField` names with `NeonAscendancy_` and check
  for collisions.
- Store the player as `wref<PlayerPuppet>`, never strong `ref<PlayerPuppet>`,
  in mod classes or added fields.
- Validate references with `IsDefined(...)`. Delayed callbacks, queued system
  requests, and async events must re-check `IsDefined(...)` when they run.
- Do not overwrite `<game>/r6/cache/final.redscripts`; it is the compile
  baseline.

## Language notes for 1.x

- Use `module NeonAscendancy.<Area>` namespaces. Cross-module classes, structs,
  and enums must be declared `public`.
- Primitive and core types are case-sensitive: `Bool`, `Int32`, `Int64`,
  `Float`, `String`, `CName`, `TweakDBID`, `ResRef`, `array<T>`, `ref<T>`,
  `wref<T>`, `script_ref<T>`.
- For class types, 1.x supplies strong `ref<T>` implicitly: prefer `GameObject`
  over `ref<GameObject>` unless explicit `ref<T>` aids clarity. Keep `wref<T>`
  and `script_ref<T>` explicit.
- Construct **structs without `new`**: `Point(1.0, 2.0)`. Construct classes
  with `new MyClass()`, or annotate a class with `@deriveNew()` to generate a
  static `MyClass.New(...)` factory (in field declaration order; does **not**
  enable `new MyClass(args)`).
- Default visibility: **class** fields/methods default to `private`; **struct**
  fields default to `public`.
- 1.x supports generics, lambdas/closures, pattern matching (`switch` /
  `if let` / `while let`), stronger local inference, `continue`, and `const`
  locals. Every `case let` branch must end explicitly with `break` or `return`
  (no fallthrough). Use 1.x features when they simplify code, not for novelty.
- `@intrinsic` is reserved for the boot library; never use it in mod code.
- Literals: `n"Name"` for `CName`, `t"Record.ID"` for `TweakDBID`, `r"path"`
  for `ResRef`, `s"val=\(x)"` for interpolated `String`.
- Recursive source discovery in 1.x respects `.gitignore`.

## Persistence (`ScriptableSystem`) and concurrency

- `ScriptableSystem` fields marked `persistent` are stored **per save file**.
- `persistent` does **not** support `String`, `Variant`, `ResRef`, or arrays of
  those types. Use `CName`, `TweakDBID`, enums, primitives, or structs instead.
- Persisting a custom class does **not** automatically persist its sub-fields:
  every saved field inside nested classes must also be marked `persistent`.
- If a player loads and saves without the mod installed, all persisted
  `ScriptableSystem` data for the mod is permanently stripped from that save.
- Persisted root systems must track `persistent let m_schemaVersion: Int32` and
  handle upgrades cleanly in `OnRestored` (see `docs/versioning.md`).
- Multiple engine threads can execute redscript concurrently. Avoid
  unsynchronized writes to shared mutable state across hooks and delayed
  callbacks; funnel state mutations through `ScriptableSystemRequest` where
  appropriate.

## Logging and runtime observability

- `<game>/r6/logs/redscript_rCURRENT.log` is the **startup compiler log from
  `scc.exe` only**. It does **not** receive runtime script logs.
- `<game>/red4ext/logs/` records RED4ext loader and native plugin startup/errors.
- In release builds of Cyberpunk 2077, native `FTLog(...)` / `LogChannel(...)`
  calls are **silent no-ops** unless a runtime logger hooks them (for example
  CET's console/`scripting.log`, Codeware's `ModLog`, or RedFileSystem).
- Do not reference Codeware's `ModLog` while Codeware is absent. Check
  `docs/modding.md` and `AGENTS-LOCAL.md` for whether a dev runtime logger
  (such as CET) is installed before relying on `FTLog(...)` for verification.

## Installed framework boundaries

- ArchiveXL scripts: `<game>/red4ext/plugins/ArchiveXL/Scripts`
- TweakXL scripts: `<game>/red4ext/plugins/TweakXL/Scripts`
- Codeware is intentionally absent until a released version supports redscript
  1.x (see `docs/modding.md`). Do not reference Codeware APIs (`ModLog`,
  `ScriptableService`, `DynamicEntitySystem`, `inkCustomController`, etc.).
- Do not introduce ArchiveXL or TweakXL dependencies into `.reds` code unless
  the feature genuinely needs them.
