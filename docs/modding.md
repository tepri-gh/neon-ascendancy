# Cyberpunk 2077 modding setup

Game reports `ProductVersion 2.5`; the script cache is the 2.5 bundle format.
Canonical pinned versions, URLs, and SHA-256 checksums live in
[`tools/lib/versions.sh`](../tools/lib/versions.sh).

## Constraints

- No Steam, no CDPR account, no game-side network use.
- Launch `Cyberpunk2077.exe` directly through `umu-run`; do not use `REDprelauncher.exe`.
- All frameworks below are local files. None require an account or an online check.

## Pinned stack

| Component | Version | Role | Installed at |
| --- | --- | --- | --- |
| RED4ext | 1.31.1 | Native plugin/loader | `bin/x64/winmm.dll`, `red4ext/` |
| redscript | 1.0.2 | Compiles/lints/formats `.reds` | `engine/tools/scc.exe`, `engine/config/base/scripts.ini` |
| ArchiveXL | 1.28.11 | Adds resources/archives | `red4ext/plugins/ArchiveXL/` |
| TweakXL | 1.12.2 | TweakDB edits | `red4ext/plugins/TweakXL/` |

CET, REDmod, and Codeware are not installed in the baseline stack.

### Codeware is intentionally absent

Current Codeware (`1.21.4` stable and `1.21.5-rc.2` prerelease) is not
compatible with redscript 1.x:

- One fatal game-start error: `OVERRIDE_RETURN_TYPE_MISMATCH` on `GetInnerNode` in the proxy mesh node.
- 22–25 strict-mode errors in its own scripts (visibility and duplicate native methods).

The game compiler tolerates the strict-mode errors, but not the fatal override.
Codeware has open upstream PRs for this:

- PR #68 `fix/redscript-1-proxy-inner-node` — renames the proxy method; requires a rebuilt native DLL.
- PR #69 `fix/redscript-1-strict-errors` — scripts-only visibility/duplicate fixes.

Neither is merged or released as of 2026-11-23. A Codeware-free stack compiles
cleanly: this mod plus ArchiveXL plus TweakXL, 0 errors under redscript 1.0.2.

Do not re-add Codeware until an upstream release supports redscript 1.x. In
particular, do not apply PR #68's script rename to the released DLL; the native
side must match.

## Linux / Wine notes

- RED4ext loads through a local `winmm.dll`, so Wine must prefer native DLLs:

  ```bash
  WINEDLLOVERRIDES=winmm,version=n,b
  ```

  The local desktop entry has the override; if launching another way, set it there too.
- On a Wine prefix, do not install the native VC++ redistributable unless RED4ext logs show a missing runtime; native MSVC DLLs are a known RED4ext failure.
- If the game fails to start after installing redscript, add `TZ=UTC` to the launch environment as a fallback.
- `-modded` is only needed for REDmod content; it is not needed for redscript/RED4ext/ArchiveXL/TweakXL.

## Optional native Linux `redscript-cli`

Upstream `jac3km4/redscript` releases publish Windows and macOS binaries only,
so `tools/lib/redscript.sh` defaults to downloading `redscript-cli.exe` and
running it under Wine. Because `crates/cli` is pure Rust, you can optionally
build a native Linux binary once to skip Wine overhead:

```bash
cargo install --git https://github.com/jac3km4/redscript --tag v1.0.2 \
  --root ~/.cache/neon-ascendancy/cargo-redscript redscript-cli
cp ~/.cache/neon-ascendancy/cargo-redscript/bin/redscript-cli \
  ~/.cache/neon-ascendancy/redscript-cli-1.0.2
```

`tools/lib/redscript.sh` auto-detects an executable
`~/.cache/neon-ascendancy/redscript-cli-<version>` (or a custom `REDSCRIPT_CLI`
override) and invokes it directly without Wine.

## Repository layout

```text
src/r6/scripts/NeonAscendancy/   redscript sources (.reds)
src/r6/tweaks/                   TweakXL YAML/TweakDB sources, when used
src/archive/pc/mod/              packaged .archive files, when used
tools/                           install, compile, lint, format, deploy, reference helpers
tools/lib/versions.sh            canonical pinned game/framework/CLI versions & checksums
.agents/skills/redscript/        cross-agent redscript 1.x skill (symlinked for .opencode/.claude)
refs/                            decompiled game scripts and SDK checkouts (gitignored)
dist/                            compile output (gitignored)
```

Note on `refs/` (cloned by `tools/fetch-refs.sh`):

- `refs/cyberpunk` — decompiled vanilla 2.5 scripts (`.swift` files containing REDscript); primary API reference.
- `refs/RED4ext.SDK` and `refs/cp2077-red-lib` — native RTTI/engine struct references (and reference for a native RED4ext C++ plugin if the simulation core ever warrants one). Not required to build `.reds` files.

## Workflow

```bash
tools/install-frameworks.sh         # reinstall pinned framework versions (game closed)
tools/fetch-refs.sh                 # one-time: clone decompiled scripts and SDK references
tools/format-redscript.sh           # rewrite src/ with the formatter
tools/format-redscript.sh --check   # fail if formatting is stale
tools/lint-redscript.sh             # fast standalone analysis (-W unused_locals), no output bundle
tools/check-redscript.sh            # compile src/ (-W unused_locals) against the game's 2.5 cache
tools/verify.sh                     # format check + compile (compile already runs full lint analysis)
tools/deploy.sh                     # copy .reds files into <game>/r6/scripts/NeonAscendancy
```

`check-redscript.sh` writes `dist/final_patched.redscripts`. Never overwrite the
game's `r6/cache/final.redscripts`.

The CLI wrappers check for the `Compilation successful` marker in addition to
the process exit code.

## Logs and runtime observability

First launch after installing the stack creates the log folders (`r6/logs/` and
`red4ext/logs/`). Verify a clean baseline launch before debugging mod code:

- **`r6/logs/redscript_rCURRENT.log`** — **compile-time only** (`scc.exe` startup
  compilation output). Does **not** contain runtime `FTLog` lines.
- **`red4ext/logs/`** — RED4ext loader and native plugin startup/error logs.
- **Runtime script logs (`FTLog` / `LogChannel`):** In release builds of
  Cyberpunk 2077, native `FTLog(...)` calls are silent no-ops unless hooked by
  a runtime logger. With the minimal baseline stack (no CET, no Codeware, no
  RedFileSystem), runtime verification relies on observable in-game effects.
  Installing **CET** as a dev-only tool (without adding CET as a mod
  dependency) is the standard way to capture `FTLog`, inspect `ScriptableSystem`
  state interactively, and run in-game checks.

## Mod install locations

| Content | Destination |
| --- | --- |
| `.reds` scripts | `r6/scripts/<mod>/` |
| RED4ext plugins | `red4ext/plugins/<plugin>/` |
| TweakXL files | `r6/tweaks/<mod>/` |
| `.archive` mods | `archive/pc/mod/` |
| CET Lua (if CET is installed) | `bin/x64/plugins/cyber_engine_tweaks/mods/` |

## Agent skills and references

- Project skill: [`.agents/skills/redscript/SKILL.md`](../.agents/skills/redscript/SKILL.md) (symlinked at `.opencode/skills/redscript` and `.claude/skills/redscript`).
- [alphanin9/CP2077AgentSkills](https://github.com/alphanin9/CP2077AgentSkills) (MIT) — general native/redscript agent skills (not vendored; reference only).
- [djkovrik/CP77Mods skills](https://github.com/djkovrik/CP77Mods/tree/master/.agents/skills) — detailed `redscript` skill (all-rights-reserved; link only, do not copy).
- [Scripting Cyberpunk wiki](https://wiki.redmodding.org/scripting-cyberpunk/) and [decompiled game scripts](https://codeberg.org/adamsmasher/cyberpunk) — language/API references.
- LSP (`jac3km4/redscript-ide`) is optional and not configured by default; CLI checks remain the shared source of truth.

## Source links

- RED4ext: https://github.com/WopsS/RED4ext/releases
- redscript: https://github.com/jac3km4/redscript/releases
- ArchiveXL: https://github.com/psiberx/cp2077-archive-xl/releases
- TweakXL: https://github.com/psiberx/cp2077-tweak-xl/releases
- Codeware 1.x PRs: https://github.com/psiberx/cp2077-codeware/pull/68, https://github.com/psiberx/cp2077-codeware/pull/69
- Linux modding notes: https://wiki.redmodding.org/cyberpunk-2077-modding/for-mod-users/users-modding-cyberpunk-2077/modding-on-linux
