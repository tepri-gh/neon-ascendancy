# Step 0.3 Research — Native RED4ext + RedLib + SQLite3 Architecture, MSVC Cross-Compilation, and Save-Branch-Safe Persistence

Status: research complete, design proposed, **not yet validated in-game**.
Scope: Phase 0 / Step 0.3 of [`docs/roadmap.md`](../roadmap.md). Design target is
Cyberpunk 2077 2.5 with the pinned stack in
[`tools/lib/versions.sh`](../../tools/lib/versions.sh) (RED4ext 1.31.1,
redscript 1.0.2, ArchiveXL 1.28.11, TweakXL 1.12.2; Codeware intentionally
absent).

Everything below was derived from the local trees in `refs/` and from commands
run on this Linux workstation. Where a claim is *not* verified, it is marked
**UNVERIFIED** with the probe that would settle it.

---

## 0. Executive summary

| Question | Answer |
| --- | --- |
| Can we cross-compile a RED4ext plugin from this Linux box? | **Yes, in principle.** `clang-cl` 23.1.5 + `lld-link` 23.1.5 + `llvm-lib` + `llvm-rc` + `llvm-mt` are installed and produce a valid `x86_64-pc-windows-msvc` PE DLL today. The **only** missing piece is the MSVC CRT/STL + Windows SDK headers and libs, which `xwin` supplies. `xwin` is **not installed** and there is no cache (`~/.xwin-cache`, no `splat` dir). |
| CRT model | **`/MT` (static)**, not `/MD`. Evidence in §2.5: the Proton/Wine builtin `msvcp140.dll` exports **zero** `__std_*` symbols, so `std::format` — which RedLib uses for `Red::Log::Debug(...)` — cannot resolve at load time with `/MD`. |
| Do we need a native save-time hook? | **No.** CP2077 exposes no script-level "save started/finished" callback that fires for autosaves and checkpoints. The design in §4 removes the dependency entirely by making the redscript anchor carry a *durable revision watermark* instead of incrementing a counter on save. |
| Save/load hooks that do exist | `ScriptableSystem.OnRestored(saveVersion, gameVersion)`, `OnAttach`, `OnDetach`, `WasRestored()`, `IsSavingLocked()`; menu-only `OnSavingComplete(success, locks)`; native `EGameStateType` transitions via `Sdk->gameStates->Add`. Details and caveats in §4.1. |
| SQLite cost | Measured here (WAL, `synchronous=NORMAL`, page cache warm): **4–9 µs** per single-row `UPDATE` in autocommit, **0.9 µs** amortized inside a 50-row transaction, **~4 µs** per R-Tree point query, **~3.4 µs** per primary-key lookup. Zero SQL on the frame path is easy to guarantee. |
| Disk budget | Static `world.db` ≈ 1–3 MB; per-playthrough DB ≈ 300 KB–8 MB with the retention policy in §4.5. |
| Biggest architectural risk | The redscript→native handoff is a *single* 32-bit integer; if the native writer thread and the game's serializer ever disagree, the save points at a revision that is not durable. §4.6 fixes this by write-ordering (commit to SQLite *before* publishing the revision). |

---

## 1. What was inspected and what was executed

### 1.1 Trees

| Tree | Revision | Used for |
| --- | --- | --- |
| `refs/RED4ext.SDK` | `a34f0ad` (2026-11-13, "Fixed ISerializable dtor and added ResourceBank") | plugin entry contract, ABI/EH macros, game-state callbacks, logger, generated 2.5 layouts |
| `refs/cp2077-red-lib` | `48cb21d` (2026-11-13, "Switch to IType") | RTTI registration macros, `std::format` dependency, persistence patterns |
| `refs/cyberpunk` | decompiled 2.5 scripts | `ScriptableSystem` lifecycle, save-lock/`OnSavingComplete` surfaces, `DelaySystem` interval pattern, `PlayerEnteredNewDistrictEvent` |

### 1.2 Commands that actually ran (all read-only, no installs)

- Tool inventory: `clang`, `clang-cl`, `lld-link`, `llvm-lib`, `llvm-rc`,
  `llvm-mt`, `cmake` (4.5.1), `ninja` (1.13.2), `sqlite3` (3.54.1),
  `python3` (sqlite 3.54.1), `wine`, `umu-run` present; **`xwin` absent**.
- `clang-cl --target=x86_64-pc-windows-msvc /c` + `lld-link /dll /noentry
  /machine:x64` → produced a valid PE32+ DLL with an exported `add` symbol
  (verified with `llvm-readobj`).
- `#pragma pack` / `__fastcall` / `static_assert(sizeof(...))` accepted by
  clang-cl under `--target=x86_64-pc-windows-msvc`.
- Full intended flag set compiled clean with `/W4 /WX` (see §2.6 for the two
  flags that must **not** be passed).
- Both proposed schemas (§5) executed against SQLite 3.54.1, including `STRICT`
  tables and three R-Tree virtual tables; `PRAGMA integrity_check` and
  `foreign_key_check` clean.
- Micro-benchmarks of SQLite WAL write/read latency (§3.5).

### 1.3 Not verified (explicit)

- **No cross-build was executed**, because no MSVC/Windows SDK headers exist on
  this machine and installing `xwin` is out of scope for this task.
- **No in-game run.** Save/load semantics below are derived from decompiled
  scripts and the SDK, not from observation. §6 lists the exact probes.
- The `libcmt.lib` / `libcpmt.lib` presence inside an `xwin` splat is
  **UNVERIFIED** here (`xwin` not installed). §2.3 has a one-line check.

---

## 2. Part A — Linux → Windows MSVC-ABI cross-compilation

### 2.1 What the SDK and RedLib actually require

- `refs/RED4ext.SDK/CMakeLists.txt:15-18` — hard floor of **C++20**
  (`FATAL_ERROR` below 20). No C++23 feature is required.
- `refs/RED4ext.SDK/include/RED4ext/Common.hpp:48-53` — the whole plugin ABI is
  `extern "C" __declspec(dllexport)` plus `__fastcall`; both are accepted by
  clang-cl for `x86_64-pc-windows-msvc` (verified). No MinGW/GNU ABI is viable:
  RED4ext loads the DLL and calls `Query`/`Supports`/`Main` with the MSVC
  calling convention and C++ layout rules.
- `refs/RED4ext.SDK/include/RED4ext/Common.hpp:27-35` — the only compiler
  conditional is `RED4EXT_ASSERT_OFFSET`, disabled under `__clang__`
  (documented TODO: `offsetof` in `static_assert`). **Sizes are still asserted**,
  see §2.7.
- `refs/RED4ext.SDK/include/RED4ext/Api/v1/Runtime.hpp:41,54` — this SDK has
  `RED4EXT_V1_RUNTIME_VERSION_2_50 = 3.0.88.46235` and maps
  `..._LATEST` to it. This is the *right* SDK for our target game build.
- `refs/cp2077-red-lib/include/RedLib.hpp:3-11` — RedLib needs `<atomic>`,
  `<concepts>`, `<format>`, `<source_location>`, `<string>`, `<vector>`, i.e. a
  full C++20 standard library. Under MSVC-ABI that means the **MSVC STL**, not
  libstdc++ (libstdc++ 16 is installed but is the wrong ABI and the wrong
  headers).
- `refs/cp2077-red-lib/include/Red/TypeInfo/Macros/Definition.hpp:11-17` —
  important clang-specific correctness fix already upstreamed: MSVC instantiates
  the `inline static` RTTI registrar eagerly, clang/GCC only when odr-used, so
  RedLib forces a `used` symbol. This means **RedLib's RTTI registration works
  under clang-cl**, which is the single most likely place a cross-compiled
  plugin would silently register nothing.

Version pinning caveat (actionable): the SDK's only tag is `1.0.0`
(2026-03-09, shipped alongside RED4ext 1.30.0). The 2.5 layout work
(`CBaseFunction +0x40`, `CStackFrame 0xA8`, `CRTTISystem` vtable, and the
`CBaseRTTIType` → `rtti::IType` rename) is listed under `[Unreleased]` in the
SDK changelog, i.e. it landed **after** that tag. Building against tag `1.0.0`
would compile but be layout-wrong at runtime, because size asserts only check
the SDK's own expectation. **Pin the exact commit
`a34f0ad0a9e4f37cbe1fe001e4ff68c2949d0665`** (and RedLib
`48cb21d4d22f63c8fcaa85aae6ac0fb1d9f24db6`) in `tools/lib/versions.sh` with a
commit-archive URL + SHA-256.

### 2.2 Installed toolchain on this machine

| Tool | Path | Version | Notes |
| --- | --- | --- | --- |
| `clang-cl` | `/usr/bin/clang-cl` | 23.1.5 | MSVC-ABI frontend, works |
| `clang++` | `/usr/bin/clang++` | 23.1.5 | host builds + Linux tests |
| `lld-link` | `/usr/bin/lld-link` | 23.1.5 | PE/COFF linker, works |
| `llvm-lib` | `/usr/bin/llvm-lib` | 23.1.5 | `.lib` archiver |
| `llvm-rc` | `/usr/bin/llvm-rc` | 23.1.5 | version resource |
| `llvm-mt` | `/usr/bin/llvm-mt` | 23.1.5 | manifests (CMake `CMAKE_MT`) |
| `cmake` / `ninja` | `/usr/bin` | 4.5.1 / 1.13.2 | fine for toolchain files |
| `xwin` | — | **missing** | must be provisioned |

Also: no MinGW cross compiler, no `/opt/msvc`, no Windows SDK headers, no
`.xwin-cache`. `clang-cl ... #include <cstdint>` currently fails with
`'cstdint' file not found` — that is exactly the gap `xwin` closes.

### 2.3 Provisioning `xwin` (documented, not executed)

```bash
# one-time, needs network
cargo install xwin --locked
xwin splat --accept-license --arch x86_64 --output ~/.cache/neon-ascendancy/xwin \
  --crt-version <pin> --sdk-version <pin>
```

`splat` layout (from upstream README, confirmed shape):

```text
<xwin>/crt/include                 MSVC STL + CRT headers
<xwin>/crt/lib/x86_64              libcmt.lib, libcpmt.lib, libvcruntime.lib, ...
<xwin>/sdk/include/{ucrt,um,shared,winrt}
<xwin>/sdk/lib/{ucrt,um}/x86_64
```

Pin `--crt-version` / `--sdk-version` and record them in `tools/lib/versions.sh`
so the Windows build is reproducible the same way the redscript stack is.

Verify the static CRT exists **before** writing any code:

```bash
ls ~/.cache/neon-ascendancy/xwin/crt/lib/x86_64/libcmt.lib \
   ~/.cache/neon-ascendancy/xwin/crt/lib/x86_64/libcpmt.lib
```

If `libcpmt.lib` is absent from the splat, `/MT` with RedLib's `std::format`
cannot link, and the fallback is §2.5 option (B).

### 2.4 CMake toolchain file

Proposed at `native/cmake/x86_64-windows-msvc-clang.cmake`:

```cmake
# Cross-compile Cyberpunk 2077 native plugins from Linux with the MSVC ABI.
# Requires an xwin splat; pass -DXWIN_ROOT=... or set $XWIN_ROOT.
set(CMAKE_SYSTEM_NAME Windows)
set(CMAKE_SYSTEM_PROCESSOR x86_64)

set(CMAKE_C_COMPILER   clang-cl)
set(CMAKE_CXX_COMPILER clang-cl)
set(CMAKE_LINKER       lld-link)
set(CMAKE_AR           llvm-lib)
set(CMAKE_RC_COMPILER  llvm-rc)
set(CMAKE_MT           llvm-mt)

set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)

if(NOT XWIN_ROOT)
  if(DEFINED ENV{XWIN_ROOT})
    set(XWIN_ROOT "$ENV{XWIN_ROOT}")
  else()
    set(XWIN_ROOT "$ENV{HOME}/.cache/neon-ascendancy/xwin")
  endif()
endif()

foreach(_dir
    "${XWIN_ROOT}/crt/include"
    "${XWIN_ROOT}/sdk/include/ucrt"
    "${XWIN_ROOT}/sdk/include/um"
    "${XWIN_ROOT}/sdk/include/shared")
  if(NOT EXISTS "${_dir}")
    message(FATAL_ERROR "xwin splat incomplete, missing: ${_dir}")
  endif()
endforeach()

set(_incs
  "/imsvc${XWIN_ROOT}/crt/include"
  "/imsvc${XWIN_ROOT}/sdk/include/ucrt"
  "/imsvc${XWIN_ROOT}/sdk/include/um"
  "/imsvc${XWIN_ROOT}/sdk/include/shared")

set(CMAKE_C_FLAGS_INIT
  "${_incs} /DWIN32 /D_WINDOWS /D_CRT_SECURE_NO_WARNINGS /DUNICODE /D_UNICODE /utf-8")
set(CMAKE_CXX_FLAGS_INIT
  "${CMAKE_C_FLAGS_INIT} /std:c++20 /EHsc /permissive- /Zc:__cplusplus /GR-
   /D_HAS_EXCEPTIONS=1 /DNOMINMAX /DWIN32_LEAN_AND_MEAN")

set(CMAKE_SHARED_LINKER_FLAGS_INIT
  "/INCREMENTAL:NO /DEBUG:FULL /Brepro
   /LIBPATH:${XWIN_ROOT}/crt/lib/x86_64
   /LIBPATH:${XWIN_ROOT}/sdk/lib/um/x86_64
   /LIBPATH:${XWIN_ROOT}/sdk/lib/ucrt/x86_64")

# /MT: see 'CRT model' below.
set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded")

set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
```

Notes: `CMAKE_MSVC_RUNTIME_LIBRARY` requires `cmake_policy(SET CMP0091 NEW)` —
set the minimum CMake version to 3.25+ in `native/CMakeLists.txt` so the policy
is new by default. Do **not** also hardcode `/MT` in `CMAKE_CXX_FLAGS_INIT`:
the runtime-library property already emits `/MT` (or `/MTd` for a Debug
configuration), and a hardcoded `/MT` would silently override the debug CRT.
`CMAKE_MT` is only used for manifest embedding; `lld-link` can embed the
manifest itself if `llvm-mt` misbehaves.

### 2.5 CRT model: `/MT`, and why

Measured fact: the Proton 11 builtin
`files/lib/wine/x86_64-windows/msvcp140.dll` exports **1,489 named symbols and
0 symbols matching `__std_`** (no `__std_remove`, `__std_rename`, no `_Fs*`
family at all). MSVC's `<format>` and `<filesystem>` call into exactly those
`__std_*` runtime entry points in `msvcp140.dll`. RedLib instantiates the
`std::format` ones in
`Red::Log::Channel<N>(CName, std::format_string<N>, ...)`
(`refs/cp2077-red-lib/include/Red/Engine/LogChannel.hpp:33-42`).

Therefore:

- **Option A (recommended): `/MT`.** Static CRT + static MSVC STL inside
  `NeonAscendancy.dll`. `std::format` and `std::filesystem` become
  self-contained, no dependency on Wine's partial `msvcp140`. Cost: ~1.6–2.2 MB
  DLL instead of ~400 KB.
- **Option B: `/MD`.** Matches RED4ext's own import table
  (`MSVCP140.dll`, `VCRUNTIME140[_1].dll`, `api-ms-win-crt-*`), which *does*
  work today under this prefix — but only because RED4ext itself touches a small
  subset of the STL. It works for us only if we never instantiate `std::format`
  or `std::filesystem` and never touch another missing STL symbol. Brittle;
  rejected.

Whichever is chosen, the invariant that makes both safe is the same:
**never pass a `std::` object across the plugin/game boundary.** The boundary is
`CName`, `CString`, `Handle<T>`, `DynArray<T>` and plain integers, all of which
allocate through the game's `Memory::IAllocator`, not the CRT (see
`RED4ext/CString-inl.hpp`). Two CRTs in one process are then harmless.

Do **not** rely on `RED4ext.dll`'s CRT: the SDK is a static library
(`RED4ext.SDK` `RED4EXT_STATIC_LIB`, `CMakeLists.txt:111`) compiled into *our*
DLL. There is no CRT sharing with the loader at all.

### 2.6 Compile flags — validated set

This exact set compiled clean with `/W4 /WX` on clang-cl 23.1.5 targeting
`x86_64-pc-windows-msvc`:

```text
/std:c++20 /permissive- /Zc:__cplusplus /EHsc /GR- /GS- /O2 /Ob2 /utf-8
/W4 /WX /D_CRT_SECURE_NO_WARNINGS /DWIN32_LEAN_AND_MEAN /DNOMINMAX /MT
```

Two traps found by testing:

1. **`/Zc:preprocessor` must not be passed.** clang-cl reports
   `argument unused during compilation: '/Zc:preprocessor'`, which is fatal
   under `/WX`. clang always uses the conformant preprocessor.
2. **`/Fo` must use the colon form.** `/Fo out.obj` makes clang-cl treat
   `out.obj` as an unused *linker input* (`-Wunused-command-line-argument`,
   fatal under `/WX`). Use `/Fo:out.obj` (CMake emits the colon form already).

Additional hard rules:

- **No `/GL`** (MSVC LTCG objects are not readable by `lld-link`).
- **`/Z7`, never `/Zi`** — `/Zi` needs `mspdbsrv.exe`; `/Z7` puts CodeView in
  the object and `lld-link /DEBUG:FULL` still produces a usable `.pdb`.
- **`NOMINMAX` is mandatory** — `Windows.h`'s `min`/`max` macros break
  `std::min`/`std::max` in the sim core and in RedLib headers.
- `WIN32_LEAN_AND_MEAN` on every TU that includes `Windows.h` (the SDK sets it
  privately for itself; consumers must set it too).
- **Paths go through Win32, not `<filesystem>`** (`GetModuleFileNameW`,
  `CreateDirectoryW`, `MoveFileExW`) — with `/MD` this is mandatory (no
  `__std_*` exports), and with `/MT` it still avoids pulling in locale-heavy
  code paths that behave differently under Wine.
- Do not add `#pragma comment(lib, ...)`; all libs go through CMake.

### 2.7 The build itself is an ABI conformance test

`RED4EXT_ASSERT_SIZE` appears **9,457 times across 9,231 headers** in the pinned
SDK. Every game struct the plugin touches is size-checked at compile time. If
clang-cl ever produced different layout/padding rules than MSVC, the Windows
build fails loudly instead of corrupting memory at runtime.

The gap: `RED4EXT_ASSERT_OFFSET` is compiled out under `__clang__`
(`Common.hpp:27-35`). Field offsets are therefore **not** checked. Mitigation:
keep the plugin's surface area small (RTTI calls + a handful of game structs)
and, at integration time, dump a few `offsetof` values with the SDK's
`RED4ext/Dump` helpers in a Windows CI job (or a one-off MSVC container build)
and compare.

### 2.8 Post-link verification gates (`tools/verify-native.sh`, later)

Cheap, high-value checks that do not need the game:

```bash
# 1. It is a 64-bit Windows DLL.
llvm-readobj --file-headers NeonAscendancy.dll | grep -q 'IMAGE_FILE_MACHINE_AMD64'

# 2. It exports exactly the three RED4ext entry points.
llvm-readobj --coff-exports NeonAscendancy.dll   # expect Main, Query, Supports

# 3. No CRT dependency leaked (the /MT guarantee).
llvm-readobj --coff-imports NeonAscendancy.dll   # must NOT list msvcp140.dll,
                                                 # vcruntime140*.dll, api-ms-win-crt-*

# 4. Static libs, no rpath-ish surprises.
llvm-readobj --coff-load-config NeonAscendancy.dll
```

Gate 3 is the regression test for the whole `/MT` decision; if someone drops
back to `/MD`, it fails immediately.

### 2.9 Risk register

| Risk | Impact | Mitigation |
| --- | --- | --- |
| SDK commit drifts from loader 1.31.1 | silent layout corruption | pin commit SHA in `tools/lib/versions.sh`; bump only in its own commit per [`docs/versioning.md`](../versioning.md) |
| `libcpmt.lib` missing from splat | `/MT` unlinkable | check in the provisioning script; fallback = avoid `std::format`, use `Sdk->logger` only |
| `-Wunused-command-line-argument` under `/WX` | build fails on harmless flag | the validated flag list in §2.6 |
| Wine `msvcp140` gaps (no `__std_*`: `std::format`, `std::filesystem`) | load-time failure with `/MD` | `/MT` + import gate §2.8 + Win32 path API |
| Exceptions crossing the boundary | crash in game frames | every exported entry point is `noexcept`-guarded; `try/catch(...)` → log + `false` |
| Plugin loaded by `winmm.dll` override confusion | plugin never loads | plugin goes to `red4ext/plugins/NeonAscendancy/NeonAscendancy.dll`, never `bin/x64` |

### 2.10 Logging without extra plumbing

`Sdk->logger` is a function table
(`refs/RED4ext.SDK/include/RED4ext/Api/v1/Logger.hpp`) with `Trace/Debug/Info/
Warn/Error/Critical` plus `...F` varargs variants, in narrow and wide flavors.
RED4ext creates `<game>/red4ext/logs/<plugin name>.log` on first use.

This satisfies the "runtime logger" requirement in
[`docs/architecture.md`](../architecture.md) §2 with **zero** custom file I/O,
zero `<format>` dependency, and correct rotation/size handling from the user's
RED4ext config.

**UNVERIFIED:** the exact filename is derived from `PluginInfo::name`. If we
want `red4ext/logs/neon_ascendancy.log` exactly, set `name = L"neon_ascendancy"`
and confirm on first run; otherwise update the architecture doc to the observed
name.

---

## 3. Part B — Embedded SQLite3: build, PRAGMA policy, performance

### 3.1 Amalgamation and compile flags

Vendor `sqlite3.c` / `sqlite3.h` (public domain, no attribution obligation, no
link dependency). Two things matter, in this order:

1. **The runtime engine must be the engine the tests run.** Because the
   amalgamation is compiled into the plugin *and* into the host test binary, the
   cleanest guarantee is: pin one amalgamation, run `neon_tests` (which executes
   the real DDL and the real checkpoint codec) against it, and stop comparing to
   the distro `sqlite3` CLI entirely.
2. **Prefer an offline-vendorable version.** This machine already has
   amalgamations in `~/Projects/netto/third_party/sqlite3/src/sqlite3.c`
   (`3.53.4`, source id `2026-07-24 …`) and
   `~/Projects/netto/third_party/rust/libsqlite3-sys/sqlite3/sqlite3.c`
   (`3.50.2`). `3.53.4` has everything this design needs (`STRICT`, WAL,
   R-Tree), so it can be vendored and SHA-256-pinned without any network
   fetch. The distro CLI on this box is `3.54.1`, which is why the schema
   validation in §5 was run with it; if the vendored engine is `3.53.4`, re-run
   the same DDL through `neon_tests` so the pinned engine is the one that proves
   the schema.

```cmake
add_library(neon_sqlite STATIC third_party/sqlite/sqlite3.c)
set_source_files_properties(third_party/sqlite/sqlite3.c PROPERTIES LANGUAGE C)

target_compile_definitions(neon_sqlite PUBLIC
  SQLITE_ENABLE_RTREE=1              # required: spatial index
  SQLITE_THREADSAFE=2                # multi-thread mode (see 3.3)
  SQLITE_DEFAULT_MEMSTATUS=0         # no malloc accounting overhead
  SQLITE_OMIT_LOAD_EXTENSION=1       # no .load, no DLL attack surface
  SQLITE_OMIT_DEPRECATED=1
  SQLITE_DQS=0                       # no double-quoted string literals
  SQLITE_USE_URI=1                   # ?immutable=1 / ?mode=ro
  SQLITE_DEFAULT_WAL_SYNCHRONOUS=1   # NORMAL inside WAL
  SQLITE_DEFAULT_CACHE_SIZE=-8192   # 8 MiB page cache
  SQLITE_DEFAULT_PAGE_SIZE=4096)
```

Deliberately **not** enabled: `FTS5` (unused), `STAT4` (tables are tiny; planner
cost outweighs benefit), `COLUMN_METADATA` (unused), `SESSION`,
`ENABLE_JSON1` (built in since 3.38), and anything requiring the `sqlite3`
shell.

`SQLITE_THREADSAFE=2` (multi-thread) rather than `1` (serialized): in mode 2
SQLite omits the per-connection mutexes but keeps the global/static ones, which
is exactly right when every connection is owned by one thread. Mode `0`
(single-thread) also drops the static mutexes and is marginally faster, but it is
safe only as long as no two threads ever touch SQLite *at all* — too sharp an
edge for a plugin that also has to survive future refactors. Mode `1` would add
per-connection locking we never need.

### 3.2 PRAGMA policy per database

**`world.db` — shipped, read-only, never written at runtime**

```sql
-- open with: file:.../world.db?immutable=1  (URI, read-only)
PRAGMA query_only = 1;
PRAGMA cache_size = -16384;      -- 16 MiB, hot metadata
PRAGMA mmap_size  = 268435456;   -- 256 MiB virtual; resident set stays small
PRAGMA temp_store = MEMORY;
```

`immutable=1` opens the file read-only and disables all locking and change
detection (no `-shm`, no lock bytes, no change-counter checks). It is safe here
because `world.db` is a shipped asset that is only replaced between game runs,
and it ships without a `-wal`. Caveat: if a mod manager rewrites `world.db` while
the game is running, results are undefined — acceptable, and the same as any
shipped static asset.

**`playthroughs/<id>.db` — writable**

```sql
PRAGMA journal_mode       = WAL;   -- persistent, set once at creation
PRAGMA synchronous        = NORMAL;-- WAL+NORMAL: crash-safe, no fsync per commit
PRAGMA wal_autocheckpoint = 2048;  -- ~8 MiB of WAL before a passive checkpoint
PRAGMA journal_size_limit = 8388608;
PRAGMA mmap_size          = 67108864;
PRAGMA cache_size         = -8192;
PRAGMA foreign_keys       = ON;
PRAGMA temp_store         = MEMORY;
PRAGMA busy_timeout       = 2000;
```

`NORMAL` + WAL is the right trade for a game mod: a process crash loses at most
the last transaction, an OS/power loss cannot corrupt the database (only lose
recent commits). Full `FULL` durability would add an fsync per commit for a
save file the game itself writes asynchronously anyway.

### 3.3 Connection and thread model

```text
game thread ──────────────► in-memory SimState (no SQL)
     │  commands/events           ▲
     ▼                            │ snapshot publish (immutable view)
 "durable commit" enqueue ────────┘
     │
     ▼   SPSC queue (bounded, e.g. 4096 entries)
writer thread ──► play_conn (single writer) ──► WAL + checkpoints
     │
     └── publish durable revision (std::atomic<uint32_t>)

game thread ──► world_conn (read-only, immutable) for rare spatial lookups
```

Rules:

1. **One connection per thread, never shared.** Enables `THREADSAFE=2` with no
   contention.
2. **The game thread never blocks on SQLite.** Mutations go to a mutex-protected
   in-memory state and to the commit queue; the writer thread does all I/O.
3. **One writer, always.** SQLite allows exactly one writer; a second writer
   connection would only produce `SQLITE_BUSY`.
4. **Cross-database joins**: `ATTACH` is optional. `world_conn` answers the
   spatial lookup, then the id is used against the playthrough connection. Two
   lookups at ~3.5 µs each beat any attach bookkeeping.

### 3.4 Prepared statements

All statements are prepared once at open and stored in a fixed struct
(`constexpr` slot enum → `sqlite3_stmt*` array), then reused with
`sqlite3_bind_*` / `step` / `reset` / `clear_bindings`. No
`sqlite3_prepare_v2` and no `sqlite3_exec` on any runtime path. Roughly two
dozen statements cover the whole dynamic schema.

### 3.5 Measured cost (WAL + `synchronous=NORMAL`, page cache warm)

| Operation | Measured | Notes |
| --- | --- | --- |
| Single-row `UPDATE`, autocommit | **4–9 µs** | one transaction per statement; spread is machine/load noise |
| Single-row `UPDATE`, 50 per transaction | **0.9 µs** amortized | batching pays ~5–10× |
| R-Tree point query on a 20–50k-row index | **~4 µs** | bbox filter + `LIMIT 1` |
| Primary-key lookup, warm cache | **~3.4 µs** | |
| `PRAGMA wal_checkpoint(TRUNCATE)` after ~280 KB of WAL | **0.03 ms** | cheap enough to call on session end |

Consequences for the design:

- A "zone crossing" event that does one R-Tree query plus two PK lookups costs
  on the order of **10 µs** — measured, not estimated.
- A checkpoint flush of a few hundred rows in one transaction is
  **sub-millisecond**.
- The entire zero-hitch rule therefore reduces to a *discipline* problem, not a
  performance problem: **no SQL on the per-frame path**, which the architecture
  already mandates.

Caveats, stated plainly: these are page-cache-warm numbers on a quiet machine.
A first run with a cold cache and a contended disk on the same filesystem was
slow enough to be abandoned after minutes — a real and important signal. Cold
storage can cost orders of magnitude more per commit, which is exactly why
commits are batched, serialized on a writer thread, and never awaited by the
frame. Under Wine/Proton the same calls also add syscall translation overhead
(typically 1.5–3×). Treat these as a warm-path budget, not a promise.

### 3.6 Memory and CPU budgets

| Bucket | Budget | Basis |
| --- | --- | --- |
| `world.db` page cache + mmap *resident* | ≤ 16 MB | 16 MiB cache, mmap is virtual |
| Playthrough DB page cache | 8 MB | `cache_size=-8192` |
| In-memory sim state (territories, missions, org, market) | ≤ 2 MB | ~64 territories × 64 B, ≤ 256 missions × 160 B, plus indexes |
| Commit queue + journal staging | 1 MB | bounded SPSC ring |
| SQLite code + amalgamation | ~1.1 MB text | static |
| **Total plugin RSS target** | **< 32 MB** | well under a mid-range GPU texture |

CPU: target **< 1 ms per simulation cycle** and cycles are event/time driven
(one per in-game hour or day, not per frame). The only recurring cost is a
1–2 s `DelaySystem` callback that publishes the durable revision into the
redscript anchor (one integer write) and drains any pending commit batch.

---

## 4. Part C — Save-branch-safe persistence

### 4.1 What the game actually gives us (findings)

| Surface | Where | Fires on | Usable? |
| --- | --- | --- | --- |
| `ScriptableSystem.OnRestored(saveVersion, gameVersion)` | `refs/cyberpunk/core/systems/scriptableSystem.swift:14` | after a save is loaded, for every scriptable system | **Yes — primary load signal.** Gives both the mod's own save version and the game version. |
| `ScriptableSystem.WasRestored()` | same file, line 8 | query at any time | Yes — distinguishes fresh attach from load. |
| `OnAttach()` / `OnDetach()` | same file, lines 12–13 | new game / system attach; session teardown | Yes for lifecycle, **not** for save timing. |
| `IsSavingLocked()` | same file, line 16; `SaveLocksManager` in `core/systems/saveLocksManager.swift` | when the game/UI asks whether saving is allowed | No — it is a *permission* query, not a save event. |
| `OnSavingComplete(success, locks)` | `pauseMenu.swift:267`, `saveGameMenu.swift:292`, `inGameMenuGameController.swift:618` | manual save / quicksave from menus only | No — Ink controllers only; **autosaves and quest checkpoints never reach it**. |
| `gameAutoSaveSystem.RequestCheckpoint()` | `orphans.swift:36896-36902` | we can *request* a checkpoint | Not a notification; must not be abused to probe saves. |
| Native `EGameStateType {BaseInitialization, Initialization, Running, Shutdown}` | `refs/RED4ext.SDK/include/RED4ext/GameStates.hpp:8-14`, added via `Sdk->gameStates->Add` | boot / session / exit | Yes for one-time init and shutdown flush; **not per save**. |
| Native function hooks | `Sdk->hooking->Attach` + `RED4ext::RelocFunc` (`Relocation.hpp`) | anything | Technically possible, but the address library (`bin/x64/cyberpunk2077_addresses.json`, 1,118,540 entries) is **hash-keyed**: only 84 entries still carry a symbol name, **none** save-related, and the SDK ships no `Addresses.hpp`. Not viable without a maintained hash list per game build. |

**Conclusion: there is no reliable, script-visible "save is happening" event in
CP2077 2.5.** Incrementing a generation counter "on save" (as originally sketched
in [`docs/architecture.md`](../architecture.md) §3.3) cannot be implemented
faithfully. The design below removes the requirement instead of faking it.

### 4.2 Core idea: the anchor is a *durable revision watermark*, not a save counter

The only thing a save file can carry is whatever the persisted fields contain
**at the instant the serializer runs**. We cannot run code at that instant, but
we do not need to: we make the field always point at a state that is *already
durable*, and we keep enough history to reconstruct exactly that state.

Definitions (per playthrough):

- **revision** — a monotonically increasing `uint32` counting *durable commits*.
  A commit is one atomic batch of state mutations (a territory flip, a mission
  acceptance, an income settlement, a cycle rollover). Cosmetic or re-derivable
  changes are not commits.
- **watermark** — the highest revision whose state is fully written to SQLite.
- **anchor** — the persisted redscript triple. `m_saveGeneration` holds the
  watermark.

Invariant (**write ordering**): the anchor is only ever advanced to `R` *after*
the SQLite transaction for `R` has returned `SQLITE_DONE`/`COMMIT` successfully.
Since the serializer can only capture values that were actually written, every
revision found in a save file is durable by construction.

That single invariant is what makes quicksave/reload/branching exact.

### 4.3 The anchor

`NcPersistenceSystem extends ScriptableSystem` (redscript, root system):

```swift
public class NcPersistenceSystem extends ScriptableSystem {
  private persistent let m_schemaVersion: Int32;      // SCHEMA_VERSION
  private persistent let m_playthroughIdHi: Uint32;   // 64-bit id, hi half
  private persistent let m_playthroughIdLo: Uint32;   // 64-bit id, lo half
  private persistent let m_saveGeneration: Int32;     // durable revision watermark

  // Base-class names from core/systems/scriptableSystem.swift; vanilla
  // systems re-declare them the same way.
  private func OnAttach() -> Void;                     // new game / first attach
  private func OnRestored(saveVersion: Int32, gameVersion: Int32) -> Void;
  private func OnDetach() -> Void;
}
```

Encoding notes:

- The `Uint64` playthrough id is split into two `Uint32` halves **on purpose**.
  Vanilla `persistent` fields in the decompiled 2.5 scripts use `Int32`,
  `Uint32`, `Bool`, `Float`, `CName`, `TweakDBID`, `EntityID` and arrays/refs of
  persistent structs — **no 64-bit primitive appears among 781 `persistent let`
  declarations**. Two `Uint32`s are provably safe; a single `Uint64` is
  **UNVERIFIED** (probe P4 in §6).
- `Int32` for the revision is comfortable: at one commit per in-game hour, 2³¹
  revisions is ~245k in-game years.
- Total anchor size: **20 bytes** (5 × 4). [`docs/architecture.md`](../architecture.md)
  says "12-byte checkpoint"; that number should be updated to 20 (or 16 if the
  playthrough id ever shrinks to one `Uint32`).

### 4.4 Protocol

**First attach of a brand-new playthrough**

```text
NcPersistenceSystem.OnAttach()
  → native SessionBegin(gi, schemaVersion=0, idHi=0, idLo=0, revision=0)
  → native generates playthroughId (CSPRNG), creates playthroughs/<id>.db,
    applies schema, seeds territory_state from world.db initial ownership,
    writes sim_clock row, writes a FULL checkpoint at revision 0
  → returns (status=Created, idHi, idLo, revision=0)
  → redscript stores m_playthroughIdHi/Lo, m_saveGeneration=0, m_schemaVersion=SCHEMA_VERSION
```

**Load of an existing save**

```text
NcPersistenceSystem.OnRestored(saveVersion, gameVersion)
  → if m_saveGeneration == 0 and m_playthroughId == 0: treat as first attach
  → if m_schemaVersion >  SCHEMA_VERSION: enter read-only fallback (no writes)
  → if m_schemaVersion <  SCHEMA_VERSION: run table migrations, then continue
  → native SessionBegin(gi, m_schemaVersion, idHi, idLo, m_saveGeneration)
      open DB, verify sim_clock.playthrough_id
      locate: newest FULL checkpoint with revision <= R
      replay DELTA checkpoints with revision in (C, R], in revision order
      (if R == 0: nothing to restore; adopt DB max revision, see §4.7)
      next = max(max_revision_in_db, R) + 1
      write a FULL checkpoint at `next` that holds the restored (state at R)
      mark revision R as pinned (it identifies this save file; never prune it)
  → returns (status=Restored, currentRevision=next)
  → redscript sets m_saveGeneration = next
```

The `next` full checkpoint is what keeps the invariant uniform: **the anchor
always names an existing checkpoint**. It costs one ~30 KB snapshot per load and
means a save taken immediately after loading (without playing) is still exact.

**During play**

```text
a commit happens (redscript command or sim event)
  → native applies it to in-memory state, enqueues it
  → writer thread: BEGIN IMMEDIATE; apply rows; append DELTA checkpoint(revision);
                   COMMIT; durableWatermark.store(revision)
anchored tick (DelaySystem IntervalCaller, 1–2 s)
  → this.m_saveGeneration = NcSessionCurrentRevision()   // one int write
```

**Why the tick is not a correctness hole:** a save taken between two ticks
captures the *last published* watermark, and the state at that watermark is
durable and exactly reconstructible. The only thing not captured is work
committed after the last publish — bounded by the tick interval. To remove even
that, commit-critical mutations publish synchronously: the native call that
performs a territory flip returns the new watermark, and the redscript assigns
it in the same call. Then a save can never be more than one *non-critical*
commit stale, and critical state (ownership, org, missions) is always exact.

**Shutdown**

```text
NcPersistenceSystem.OnDetach() / EGameStateType::Shutdown
  → native SessionEnd(): drain queue, wal_checkpoint(TRUNCATE), close
```

### 4.5 Restore algorithm, retention, and "no bloat"

`checkpoints` stores one record per commit: `kind = 'delta'` for ordinary
commits, `kind = 'full'` every `CHECKPOINT_INTERVAL` (default **64**) revisions
and at every fork. Restore = newest full ≤ R, then deltas in `(C, R]`.

Retention (per playthrough, enforced by the writer thread after each full
checkpoint):

1. Always keep the newest full checkpoint.
2. Always keep the newest pinned revision (learned on load) and every checkpoint
   needed to reach it.
3. Delete deltas older than `RETENTION_BYTES` (default **8 MB**) except those
   required by (2), and keep at most `MAX_FULL` (default **4**) full snapshots.
4. `VACUUM` only on an explicit maintenance path (loading screen), never during
   play — it rewrites the file and takes milliseconds-to-seconds.

Sizing: a full snapshot of the whole dynamic state is ~20–40 KB; a delta is
~200–600 B. A 10-hour session with ~2,000 commits is ~0.5–1 MB plus 4 snapshots
≈ 1.2 MB. The 8 MB cap is only reached by extreme save-scumming, and then the
oldest history is trimmed (with a `WARN`) rather than the file growing without
bound.

Worst-case degradation, documented explicitly: loading a very old manual save
whose deltas were pruned restores the nearest surviving full checkpoint ≤ R —
i.e. **at most 64 commits stale** — logs a `WARN`, and reports the condition to
redscript so the UI can say "state restored from a nearby checkpoint".

### 4.6 Consistency argument

1. *A save never references non-durable state.* Anchor advances only after
   `COMMIT` (§4.2).
2. *A reload restores exactly that revision.* Full ≤ R + deltas `(C, R]` is a
   deterministic replay of the same mutations; state tables are only an
   optimization for the live session, never the restore source.
3. *Continuing after a reload cannot collide with abandoned history.* The next
   revision is `max(max_revision_in_db, R) + 1`, so a fork's new commits are
   strictly newer than every existing record, and the fork immediately writes a
   **full** checkpoint (its ancestry diverges, so a delta chain would be wrong).
4. *Quicksave → keep playing → reload* restores R, leaves R+1…R+n intact (they
   belong to the abandoned branch and are pruned by retention, not by
   correctness).
5. *Two manual saves from one session* are two revisions R₁ < R₂, both
   reconstructible; loading R₁ and playing on creates revisions above R₂.
6. *Interrupted writes* cannot be half-applied: a commit is one SQLite
   transaction, and a checkpoint record is written inside it.

The one remaining assumption: **SQLite's `COMMIT` returning means the WAL record
is in the OS page cache** (`synchronous=NORMAL`). A power loss can lose the last
commit; that simultaneously loses the save-file change too, so the two stay
consistent. `synchronous=FULL` would be needed only if saves could survive a
power loss that the WAL did not.

### 4.7 Failure modes and recovery

| Situation | Detection | Behaviour |
| --- | --- | --- |
| DB file missing, save says R > 0 (save copied from another machine) | open fails / no rows | rebuild from `world.db` defaults, fork at `R + 1`, `ERROR` log, set a flag so the UI can warn "external state not found" |
| DB exists, `sim_clock.playthrough_id` ≠ anchor id | mismatch | treat as foreign DB: do **not** write; open read-only; rebuild a fresh DB keyed to the anchor id |
| `R` newer than DB max (DB partially lost / restored from backup) | `R > max_revision` | restore the newest available checkpoint, then fork at `max(max_in_db, R) + 1` so revision numbering stays monotonic, `WARN` |
| `R == 0` but DB has revisions (anchor never written: save taken in the first seconds of a session, or save predates the mod) | `R == 0 && max_revision > 0` | if the playthrough id matches, adopt DB max revision; else start fresh at 0 |
| `m_schemaVersion > SCHEMA_VERSION` (save from a newer mod build) | compare in `OnRestored` | read-only fallback, no mutation, `ERROR` — matches [`docs/versioning.md`](../versioning.md) §2 |
| `world.db` content changed between mod versions | `world_content_hash` mismatch | integrity pass: verify every referenced `sub_territory_id` still exists, remap by `code` where possible, log removed ids |
| Crash mid-session | WAL replay on next open | last committed revision survives; uncommitted work is dropped |

### 4.8 Why not store state in persistent redscript fields?

Worth stating because it is the obvious alternative: a few hundred territory
rows plus missions plus market state serialized as persistent redscript structs
would (a) bloat every save by tens to hundreds of KB, (b) require the entire
simulation to be expressed in redscript (no offline unit tests, no SQL),
(c) hit `persistent` limitations (no `String`/`Variant`/`ResRef`, nested fields
must each be marked `persistent`), and (d) make queries O(n). The anchor +
SQLite split is strictly better *provided* the anchor invariant holds.

### 4.9 Where the dynamic DB lives

```text
<game>/red4ext/plugins/NeonAscendancy/
├── NeonAscendancy.dll
├── world.db                      # shipped read-only, rebuilt by tools/build-db
└── playthroughs/
    ├── index.json                # housekeeping: id, created, last opened, bytes
    └── pt_<16 hex digits>.db     # one file per playthrough (+ -wal, -shm)
```

One file per playthrough keeps deletion/space accounting trivial and means a
corrupted file loses one campaign, not all of them. Bounded retention per file
(§4.5) means an index.json + pruning pass is enough; no global database.

---

## 5. Part D — Initial schema blueprint

Both DDL files below were **executed** against SQLite 3.54.1 (the installed CLI)
and passed `PRAGMA integrity_check` + `foreign_key_check`; sample rows and the
checkpoint lookup query were exercised. Before trusting a pinned amalgamation
(3.53.4 or newer), re-run these exact bytes through `neon_tests` linked against
that amalgamation — the tests are the authority, not the CLI. They are intended
to become the literal contents of `data/schema/world_v1.sql` and
`data/schema/playthrough_v1.sql`, with `build-db` embedding the same bytes into
both the runtime and the tests.

Conventions:

- World coordinates are Cyberpunk engine units (**centimetres**), matching
  `Vector4` values in game data.
- `STRICT` tables everywhere (SQLite ≥ 3.37) — illegal values become errors at
  the boundary instead of silently stored text.
- Every static id is **explicit and permanent**; ids are never reused across mod
  versions so playthrough state can survive a `world.db` rebuild.
- Dynamic tables reference static ids as **soft references** (cross-database
  FKs are impossible); they are validated at load, not enforced by SQLite.

### 5.1 `world.db` (static, read-only)

```sql
PRAGMA application_id = 0x4E435744; -- 'NCWD'
PRAGMA user_version = 1;

CREATE TABLE meta (
  key   TEXT PRIMARY KEY,
  value TEXT NOT NULL
) STRICT, WITHOUT ROWID;
-- rows: schema_version, content_hash, game_version, generated_at, generator

CREATE TABLE districts (
  district_id       INTEGER PRIMARY KEY,
  code              TEXT NOT NULL UNIQUE,          -- 'watson', 'westbrook', ...
  display_name      TEXT NOT NULL,
  kind              TEXT NOT NULL CHECK (kind IN ('city','badlands','dogtown')),
  gamedata_district TEXT,                          -- vanilla gamedataDistrict enum name
  bbox_min_x REAL NOT NULL, bbox_min_y REAL NOT NULL,
  bbox_max_x REAL NOT NULL, bbox_max_y REAL NOT NULL,
  CHECK (bbox_min_x < bbox_max_x AND bbox_min_y < bbox_max_y)
) STRICT;

CREATE TABLE factions (
  faction_id        INTEGER PRIMARY KEY,
  code              TEXT NOT NULL UNIQUE,          -- 'maelstrom', 'arasaka', ...
  display_name      TEXT NOT NULL,
  category          TEXT NOT NULL CHECK (category IN
                      ('gang','megacorp','fixer','civic','independent','player')),
  parent_faction_id INTEGER REFERENCES factions(faction_id),
  color_rgba        TEXT NOT NULL CHECK (length(color_rgba) = 9 AND substr(color_rgba,1,1) = '#'),
  income_multiplier REAL NOT NULL DEFAULT 1.0 CHECK (income_multiplier >= 0.0),
  hostility_bias    REAL NOT NULL DEFAULT 0.0,
  is_playable       INTEGER NOT NULL DEFAULT 0 CHECK (is_playable IN (0,1))
) STRICT;
CREATE INDEX idx_factions_category ON factions(category);

CREATE TABLE landmarks (
  landmark_id      INTEGER PRIMARY KEY,
  code             TEXT NOT NULL UNIQUE,
  display_name     TEXT NOT NULL,
  kind             TEXT NOT NULL CHECK (kind IN
                     ('hq','compound','warehouse','clinic','shop','venue','asset')),
  sub_territory_id INTEGER,                        -- soft ref, validated by build-db
  x REAL NOT NULL, y REAL NOT NULL, z REAL NOT NULL,
  purchasable      INTEGER NOT NULL DEFAULT 0 CHECK (purchasable IN (0,1)),
  base_price       INTEGER CHECK (base_price IS NULL OR base_price >= 0)
) STRICT;

CREATE TABLE sub_territories (
  sub_territory_id INTEGER PRIMARY KEY,
  district_id      INTEGER NOT NULL REFERENCES districts(district_id),
  code             TEXT NOT NULL UNIQUE,
  display_name     TEXT NOT NULL,
  initial_owner_faction_id INTEGER REFERENCES factions(faction_id),
  base_income_per_cycle INTEGER NOT NULL DEFAULT 0 CHECK (base_income_per_cycle >= 0),
  defense_rating   INTEGER NOT NULL DEFAULT 0 CHECK (defense_rating >= 0),
  area_m2          REAL,
  centroid_x REAL NOT NULL, centroid_y REAL NOT NULL, centroid_z REAL NOT NULL,
  UNIQUE (district_id, code)
) STRICT;
CREATE INDEX idx_sub_territories_district ON sub_territories(district_id);

CREATE TABLE control_centers (
  control_center_id INTEGER PRIMARY KEY,
  sub_territory_id  INTEGER NOT NULL REFERENCES sub_territories(sub_territory_id) ON DELETE CASCADE,
  code              TEXT NOT NULL UNIQUE,
  display_name      TEXT NOT NULL,
  landmark_id       INTEGER REFERENCES landmarks(landmark_id),
  x REAL NOT NULL, y REAL NOT NULL, z REAL NOT NULL,
  capture_radius_m  REAL NOT NULL DEFAULT 25.0 CHECK (capture_radius_m > 0),
  is_capital        INTEGER NOT NULL DEFAULT 0 CHECK (is_capital IN (0,1))
) STRICT;
CREATE INDEX idx_control_centers_territory ON control_centers(sub_territory_id);

CREATE TABLE spawn_points (
  spawn_point_id    INTEGER PRIMARY KEY,
  control_center_id INTEGER NOT NULL REFERENCES control_centers(control_center_id) ON DELETE CASCADE,
  sub_territory_id  INTEGER NOT NULL REFERENCES sub_territories(sub_territory_id),
  faction_id        INTEGER NOT NULL REFERENCES factions(faction_id),
  encounter_type    TEXT NOT NULL CHECK (encounter_type IN
                      ('guard','patrol','ambush','camp','vehicle','sniper','civilian')),
  community_template TEXT,                          -- e.g. '#gang__maelstrom_ow'
  x REAL NOT NULL, y REAL NOT NULL, z REAL NOT NULL,
  yaw REAL,
  spawn_weight      INTEGER NOT NULL DEFAULT 100 CHECK (spawn_weight >= 0),
  min_era           TEXT NOT NULL DEFAULT 'any' CHECK (min_era IN ('any','act1','act2','postgame','dogtown')),
  max_era           TEXT NOT NULL DEFAULT 'any' CHECK (max_era IN ('any','act1','act2','postgame','dogtown'))
) STRICT;
CREATE INDEX idx_spawn_points_center  ON spawn_points(control_center_id);
CREATE INDEX idx_spawn_points_faction ON spawn_points(faction_id);

-- Ownership grid, loaded entirely into RAM at boot: O(1) point -> territory.
CREATE TABLE territory_cells (
  level            INTEGER NOT NULL CHECK (level BETWEEN 0 AND 3),
  cell_x           INTEGER NOT NULL,
  cell_y           INTEGER NOT NULL,
  sub_territory_id INTEGER NOT NULL REFERENCES sub_territories(sub_territory_id) ON DELETE CASCADE,
  PRIMARY KEY (level, cell_x, cell_y)
) STRICT, WITHOUT ROWID;

-- Map overlay geometry (rendering/authoring only, never queried at runtime).
CREATE TABLE territory_cell_polygons (
  sub_territory_id INTEGER NOT NULL REFERENCES sub_territories(sub_territory_id) ON DELETE CASCADE,
  ring_index       INTEGER NOT NULL,
  ring_kind        TEXT NOT NULL CHECK (ring_kind IN ('outer','hole')),
  point_index      INTEGER NOT NULL,
  x REAL NOT NULL, y REAL NOT NULL,
  PRIMARY KEY (sub_territory_id, ring_index, point_index)
) STRICT, WITHOUT ROWID;

-- Spatial indexes (bbox prefilter only, exact tests live in C++).
CREATE VIRTUAL TABLE sub_territory_rtree USING rtree(id, min_x, max_x, min_y, max_y);
CREATE VIRTUAL TABLE landmark_rtree      USING rtree(id, min_x, max_x, min_y, max_y);
CREATE VIRTUAL TABLE spawn_point_rtree   USING rtree(id, min_x, max_x, min_y, max_y);

-- Deferred: Road-Chunk Vehicle Transit Ledger spatial scaffolding.
CREATE TABLE road_chunks (
  chunk_id    INTEGER PRIMARY KEY,
  district_id INTEGER REFERENCES districts(district_id),
  grid_x INTEGER NOT NULL, grid_y INTEGER NOT NULL, grid_z INTEGER NOT NULL,
  lane_count INTEGER NOT NULL DEFAULT 0,
  navmesh_ready INTEGER NOT NULL DEFAULT 0 CHECK (navmesh_ready IN (0,1)),
  UNIQUE (grid_x, grid_y, grid_z)
) STRICT;
CREATE VIRTUAL TABLE road_chunk_rtree USING rtree(id, min_x, max_x, min_y, max_y);

CREATE TABLE road_nodes (
  node_id  INTEGER PRIMARY KEY,
  chunk_id INTEGER NOT NULL REFERENCES road_chunks(chunk_id),
  x REAL NOT NULL, y REAL NOT NULL, z REAL NOT NULL,
  lane     INTEGER NOT NULL DEFAULT 0
) STRICT;
CREATE INDEX idx_road_nodes_chunk ON road_nodes(chunk_id);

CREATE TABLE road_edges (
  edge_id      INTEGER PRIMARY KEY,
  from_node_id INTEGER NOT NULL REFERENCES road_nodes(node_id),
  to_node_id   INTEGER NOT NULL REFERENCES road_nodes(node_id),
  chunk_id     INTEGER NOT NULL REFERENCES road_chunks(chunk_id),
  length_m     REAL NOT NULL CHECK (length_m > 0),
  speed_kph    REAL,
  is_tunnel    INTEGER NOT NULL DEFAULT 0 CHECK (is_tunnel IN (0,1))
) STRICT;
CREATE INDEX idx_road_edges_chunk ON road_edges(chunk_id);
CREATE INDEX idx_road_edges_from  ON road_edges(from_node_id);
```

Design notes:

- **R-Tree is 2D; Night City is very vertical.** All R-Trees are a bbox
  *prefilter*; the exact test (including `z` and stacked interiors) runs in C++
  against the bbox + `control_center.z`. Do not pretend the R-Tree is a
  point-in-solid oracle.
- **`territory_cells` is the hot path**, not the R-Tree: a single integer grid
  lookup at boot-loaded level 0 gives O(1) "which sub-territory am I in?" with
  no geometry at runtime and no SQL at all once loaded.
- `road_*` tables exist now so the deferred ledger (roadmap "Deferred
  Systems") never needs a `SCHEMA_VERSION` bump just to add spatial scaffolding.
  They ship empty.

### 5.2 `playthrough.db` (dynamic, per playthrough)

```sql
PRAGMA journal_mode = WAL;
PRAGMA synchronous  = NORMAL;
PRAGMA foreign_keys = ON;
PRAGMA user_version = 1;
PRAGMA application_id = 0x4E435750; -- 'NCWP'

CREATE TABLE meta (
  key   TEXT PRIMARY KEY,
  value TEXT NOT NULL
) STRICT, WITHOUT ROWID;
-- rows: schema_version, world_content_hash, created_at, last_opened_at,
--       engine_version, mod_version

CREATE TABLE sim_clock (
  singleton            INTEGER PRIMARY KEY CHECK (singleton = 1),
  playthrough_id_hi    INTEGER NOT NULL,
  playthrough_id_lo    INTEGER NOT NULL,
  revision             INTEGER NOT NULL DEFAULT 0,   -- highest durable revision
  last_cycle_seconds   INTEGER NOT NULL DEFAULT 0,   -- absolute GameTime seconds
  cycle_index          INTEGER NOT NULL DEFAULT 0,
  rng_seed             INTEGER NOT NULL,
  rng_counter          INTEGER NOT NULL DEFAULT 0,
  world_content_hash   TEXT NOT NULL                 -- must match world.db meta
) STRICT;

-- One record per durable commit. Restore = newest 'full' <= R, then 'delta' up to R.
CREATE TABLE checkpoints (
  revision       INTEGER PRIMARY KEY,
  kind           TEXT NOT NULL CHECK (kind IN ('full','delta')),
  base_revision  INTEGER,                -- deltas: the full checkpoint they apply to
  format_version INTEGER NOT NULL,
  row_count      INTEGER NOT NULL,
  payload        BLOB NOT NULL,          -- typed binary rows, see 5.3
  byte_size      INTEGER NOT NULL,
  created_utc    INTEGER NOT NULL,
  pinned         INTEGER NOT NULL DEFAULT 0 CHECK (pinned IN (0,1))
) STRICT;

CREATE TABLE territory_state (
  sub_territory_id        INTEGER PRIMARY KEY,      -- soft ref into world.db
  owner_faction_id        INTEGER NOT NULL,
  holder_faction_id       INTEGER,
  contested_by_faction_id INTEGER,
  control_level           REAL NOT NULL DEFAULT 1.0 CHECK (control_level BETWEEN 0.0 AND 1.0),
  heat                    REAL NOT NULL DEFAULT 0.0 CHECK (heat >= 0.0),
  last_flip_revision      INTEGER NOT NULL DEFAULT 0,
  last_flip_seconds       INTEGER NOT NULL DEFAULT 0
) STRICT;

CREATE TABLE org_state (
  org_id           INTEGER PRIMARY KEY,
  kind             TEXT NOT NULL CHECK (kind IN ('gang','corporation')),
  display_name     TEXT NOT NULL,
  faction_id       INTEGER,
  treasury_eddies  INTEGER NOT NULL DEFAULT 0 CHECK (treasury_eddies >= 0),
  notoriety        REAL NOT NULL DEFAULT 0.0,
  heat             REAL NOT NULL DEFAULT 0.0,
  upkeep_per_cycle INTEGER NOT NULL DEFAULT 0,
  founded_revision INTEGER NOT NULL DEFAULT 0,
  founded_seconds  INTEGER NOT NULL DEFAULT 0
) STRICT;

CREATE TABLE org_assets (
  asset_id          INTEGER PRIMARY KEY,
  org_id            INTEGER NOT NULL REFERENCES org_state(org_id) ON DELETE CASCADE,
  landmark_id       INTEGER,
  kind              TEXT NOT NULL,
  purchase_price    INTEGER NOT NULL DEFAULT 0,
  upkeep_per_cycle  INTEGER NOT NULL DEFAULT 0,
  acquired_revision INTEGER NOT NULL DEFAULT 0
) STRICT;
CREATE INDEX idx_org_assets_org ON org_assets(org_id);

CREATE TABLE missions (
  mission_id        INTEGER PRIMARY KEY,
  kind              TEXT NOT NULL CHECK (kind IN ('combat','economic','espionage')),
  state             TEXT NOT NULL CHECK (state IN
                      ('offered','active','succeeded','failed','expired')),
  issuer_faction_id INTEGER,
  target_faction_id INTEGER,
  sub_territory_id  INTEGER,
  control_center_id INTEGER,
  seed              INTEGER NOT NULL,               -- deterministic generation seed
  difficulty        REAL NOT NULL DEFAULT 1.0,
  reward_eddies     INTEGER NOT NULL DEFAULT 0,
  created_seconds   INTEGER NOT NULL,
  deadline_seconds  INTEGER,
  resolved_seconds  INTEGER,
  resolved_revision INTEGER
) STRICT;
CREATE INDEX idx_missions_state     ON missions(state, kind);
CREATE INDEX idx_missions_territory ON missions(sub_territory_id, state);

CREATE TABLE event_log (
  revision     INTEGER NOT NULL,
  seq          INTEGER NOT NULL,
  event_type   TEXT NOT NULL,
  game_seconds INTEGER NOT NULL,
  payload      BLOB,
  PRIMARY KEY (revision, seq)
) STRICT, WITHOUT ROWID;
CREATE INDEX idx_event_log_type ON event_log(event_type, revision);

-- Deferred: Road-Chunk Vehicle Transit Ledger (created now, unused until later).
CREATE TABLE transit_ledger (
  transit_id     INTEGER NOT NULL,
  seq            INTEGER NOT NULL,
  faction_id     INTEGER,
  vehicle_record TEXT,
  route_id       INTEGER,
  chunk_id       INTEGER NOT NULL,
  t_enter        INTEGER NOT NULL,                  -- absolute GameTime seconds
  t_exit         INTEGER NOT NULL,
  state          TEXT NOT NULL CHECK (state IN
                   ('scheduled','active','materialized','done','aborted')),
  PRIMARY KEY (transit_id, seq)
) STRICT, WITHOUT ROWID;
CREATE INDEX idx_transit_window ON transit_ledger(chunk_id, t_enter, t_exit);
```

Design notes:

- **Faction id space is partitioned.** Static factions come from `world.db`
  (`faction_id < 1000`). Runtime-created organizations (the player's gang or
  corporation) allocate ids from `1000` upward and are mirrored in
  `org_state.faction_id`, so `territory_state.owner_faction_id` has one uniform
  meaning: "an id that resolves either in `world.db: factions` or in
  `org_state`". Resolve order: static first, then `org_state`.
- **Absolute time only.** Every `*_seconds` column is absolute in-game seconds
  (`days*86400 + hours*3600 + minutes*60 + seconds`), never a wall-clock
  timestamp or a frame count. This is what makes sleep/time-skip and reload
  deterministic, per [`docs/architecture.md`](../architecture.md) §3.2.
- **`revision` lives in `sim_clock`, not in the anchor alone.** The anchor is the
  authority on load; `sim_clock.revision` is the authority on disk. A mismatch is
  a recoverable condition (§4.7), never a silent overwrite.

### 5.3 Checkpoint payload format

Binary, little-endian, versioned — not SQL text (no parse cost, no injection
surface, smaller):

```text
payload := header record* footer
header  := u16 magic(0x4E43 'NC') | u16 format_version | u32 record_count
record  := u16 row_type | u16 byte_len | byte[byte_len]
footer  := u32 crc32(payload bytes before footer)
```

Row types are small fixed structs (`territory_state`, `org_state`,
`mission`, `sim_clock`, …), encoded field by field with a hand-written codec so
layout never depends on compiler packing. A `neon-db dump` host tool renders
payloads as SQL for debugging; nothing at runtime parses text.

### 5.4 `world.db` build (Step 0.4 interface)

`tools/build-db` (a host binary, `native/tools/neon-wdb`) reads `data/` seeds,
validates, and writes `world.db` deterministically:

1. Stable ids must be present and unique; `code` values unique.
2. Referential integrity for every soft reference (`landmarks.sub_territory_id`,
   `territory_state` compatibility).
3. Coordinate sanity (inside the district bbox, finite, plausible `z`).
4. `territory_cells` coverage: every land cell at level 0 maps to exactly one
   sub-territory (no holes, no double assignment) — catches partition mistakes
   before they reach the map overlay.
5. R-Tree rows regenerated from the owning tables (never hand-written).
6. Writes `meta.content_hash` = SHA-256 over canonicalized seed input; the
   runtime compares it against `sim_clock.world_content_hash`.

The same binary runs on Linux, so the entire world pipeline is testable without
the game.

---

## 6. Part E — Offline Linux testing and the CMake target split

### 6.1 Layout

```text
native/
├── CMakeLists.txt
├── cmake/x86_64-windows-msvc-clang.cmake
├── third_party/
│   ├── sqlite/{sqlite3.c,sqlite3.h}     # pinned amalgamation
│   ├── RED4ext.SDK/                     # pinned commit, fetched (gitignored)
│   └── RedLib/                          # pinned commit, fetched (gitignored)
├── lib/
│   ├── sim/            # pure C++20: no Windows.h, no RedLib, no SQLite
│   ├── store/          # SQLite wrapper, schema, checkpoint codec
│   └── schema/         # generated header embedding the two .sql files
├── tools/
│   ├── neon-wdb/       # seed -> world.db
│   └── neon-db/        # inspect / dump / vacuum
├── plugin/             # RED4ext + RedLib, Windows only
└── tests/              # host-only harness
```

### 6.2 Two configurations, one source tree

```bash
# Linux: fast offline tests, world-db build, no plugin
cmake -S native -B build/linux -G Ninja -DNEON_BUILD_PLUGIN=OFF -DCMAKE_BUILD_TYPE=Debug
cmake --build build/linux
ctest --test-dir build/linux --output-on-failure

# Windows: cross-compiled plugin (needs the xwin splat)
cmake -S native -B build/win -G Ninja \
  -DCMAKE_TOOLCHAIN_FILE=native/cmake/x86_64-windows-msvc-clang.cmake \
  -DNEON_BUILD_PLUGIN=ON -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake --build build/win
```

```cmake
# native/CMakeLists.txt (shape)
cmake_minimum_required(VERSION 3.25)
project(neon_ascendancy_native LANGUAGES C CXX)

option(NEON_BUILD_PLUGIN "Build the Windows RED4ext plugin" OFF)
option(NEON_BUILD_TOOLS  "Build host tools" ON)

add_subdirectory(third_party/sqlite)   # neon_sqlite (PUBLIC defines)
add_subdirectory(lib/schema)           # neon_schema (embedded .sql, INTERFACE)
add_subdirectory(lib/sim)              # neon_sim   (portable, warning-clean)
add_subdirectory(lib/store)            # neon_store (links neon_sqlite)

if(NEON_BUILD_TOOLS)
  add_subdirectory(tools/neon-wdb)
  add_subdirectory(tools/neon-db)
endif()

if(NEON_BUILD_PLUGIN)
  enable_language(RC)
  add_subdirectory(plugin)             # NeonAscendancy.dll
endif()

if(NEON_BUILD_TOOLS)
  enable_testing()
  add_subdirectory(tests)              # neon_tests, host-only
endif()
```

Hard rules that keep this split honest:

- `lib/sim` includes **no** `<Windows.h>`, no `RED4ext/*`, no `sqlite3.h`. It
  compiles with `-Wall -Wextra -Werror` on both toolchains, which is what makes
  the Linux tests meaningful for the Windows build.
- `lib/store` hides `sqlite3*` behind a small RAII interface (`Db`, `Stmt`,
  `Txn`) so the sim never sees SQL types.
- `plugin/` is the only place that includes `<RedLib.hpp>`; it is a thin
  adapter: RTTI registration, command marshalling, session lifecycle, logging.
- The schema lives in `.sql` files, embedded via a generated raw-string header
  shared by runtime, `neon-wdb`, and tests. One source of truth.

### 6.3 What the Linux tests should actually assert

Per [`AGENTS.md`](../../AGENTS.md) ("assert observable behavior of a real
system through its public interface"), the valuable cases are:

1. **Schema applies** to a fresh DB and `PRAGMA integrity_check` is clean.
2. **Revision restore is exact**: commit N states, restore at revision
   K < N, assert every observable field equals the state at K.
3. **Fork after reload**: restore at K, commit more, assert new revisions are
   `> max` and that restoring the old branch at K still yields K's state.
4. **Retention never breaks a pinned revision**: force pruning, then restore
   every pinned revision successfully.
5. **WAL crash recovery**: write without checkpoint, close without clean
   shutdown (simulated by discarding the connection), reopen, assert the last
   committed revision survives and the DB is not corrupt.
6. **Territory cell lookup**: a hand-built grid, assert no holes/overlaps and
   correct id per cell.
7. **`world.db` ↔ `playthrough.db` id compatibility**: build a seed world,
   load it, assert `content_hash` gate and soft-reference validation.

A minimal `NC_CHECK(expr)` macro + a `main()` that runs registered test
functions is enough; no test framework dependency is warranted (and adding one
needs approval per `AGENTS.md`).

### 6.4 CI-shaped script (future `tools/verify-native.sh`)

```bash
# 1. host build + tests
cmake -S native -B build/linux -G Ninja -DNEON_BUILD_PLUGIN=OFF
cmake --build build/linux
ctest --test-dir build/linux --output-on-failure
# 2. schema regeneration is deterministic
tools/build-db --check           # byte-identical world.db from seeds
# 3. cross build (only if the xwin splat exists)
if [ -d "${XWIN_ROOT:-$HOME/.cache/neon-ascendancy/xwin}" ]; then
  cmake -S native -B build/win -G Ninja \
    -DCMAKE_TOOLCHAIN_FILE=native/cmake/x86_64-windows-msvc-clang.cmake \
    -DNEON_BUILD_PLUGIN=ON
  cmake --build build/win
  llvm-readobj --coff-imports build/win/NeonAscendancy.dll | grep -q msvcp140 && exit 1
fi
```

Static checks and in-game verification stay separate, per `AGENTS.md`.

---

## 7. Part F — Open questions and the probe list

These are the things that can only be settled in-game (or with the xwin
toolchain present). Each has a concrete, cheap probe.

| # | Question | Probe | Fallback if the answer is bad |
| --- | --- | --- | --- |
| P1 | Does `OnRestored` run with a valid `GetGameInstance()`? | log `GameInstance.IsValid` + `GetGameTime()` inside `OnRestored` | defer the native handshake to the first `DelayCallback` tick after restore |
| P2 | Is the anchor value at save time exactly the last published value? | write a known counter, save, reload, compare | publish synchronously on every commit (already the rule for critical commits) |
| P3 | Does `OnAttach` fire before or after `OnRestored` on a new game? | log both, plus `WasRestored()` | branch on `m_playthroughId == 0` instead of call order |
| P4 | Is a `Uint64` persistent field supported? | add a probe field, save/reload | already designed for two `Uint32`s |
| P5 | Does the plugin load with `/MT` (no CRT imports)? | `llvm-readobj --coff-imports` + boot | fall back to `/MD` and avoid `std::format` |
| P6 | Exact `red4ext/logs/*.log` filename from `PluginInfo::name` | boot once, `ls red4ext/logs/` | update the architecture doc to the observed name |
| P7 | Does a 1 s `IntervalCaller` cost anything measurable? | compare frame times with/without | 2–5 s interval, or drive from `TimeSystem` deltas only |
| P8 | Is `OnDetach` called on exit-to-main-menu (not only on quit)? | log, then load another save | treat `SessionBegin` as authoritative (it already closes any prior session) |
| P9 | Does `world.db` with `?immutable=1` open cleanly under Wine? | one log line with `PRAGMA query_only` | drop `immutable=1`, keep read-only + `query_only` |

---

## 8. Recommendations (ordered, minimal)

1. **Pin the SDK/RedLib commits, not tags**, in `tools/lib/versions.sh`
   (`a34f0ad…`, `48cb21d…`) and fetch them into `native/third_party/` via a
   script; keep `refs/` as read-only reference.
2. **Adopt `/MT` + the validated flag list** (§2.5–2.6) and make
   "no `msvcp140` import" a build gate.
3. **Provision `xwin` as a documented one-time step**, version-pinned, before
   writing plugin code — the toolchain otherwise cannot be exercised at all.
4. **Implement the revision-watermark persistence (§4) instead of a
   save-generation counter.** It is the only variant that stays correct without
   a save hook, and it changes nothing about the user-visible model: generation
   still identifies the exact state, it is just durable-first.
5. **Keep SQLite off every frame path**: in-memory state + commit queue +
   single writer thread; the 9 µs / 0.9 µs / 3.9 µs measurements say the
   remaining work is discipline, not optimization.
6. **Ship the schema as `.sql` files consumed by runtime, build tool and tests**
   (§5, §6.2) so `SCHEMA_VERSION` has exactly one definition site.
7. **Do not build native hooks in Phase 0.** No save-critical behaviour needs
   them, and the address library is hash-keyed without usable symbol names
   (§4.1). Revisit only for Step 0.5 rendering or the transit ledger.
8. **Update two docs** once the design is accepted:
   [`docs/architecture.md`](../architecture.md) §3.3 (anchor is 20 bytes and is
   a durable watermark, not a save counter) and §3.4 (add the `/MT` decision and
   the "no CRT object across the boundary" rule).

---

## 9. Evidence index

| Claim | Evidence |
| --- | --- |
| C++20 floor | `refs/RED4ext.SDK/CMakeLists.txt:15-18` |
| Plugin ABI = `__declspec(dllexport)` + `__fastcall` | `refs/RED4ext.SDK/include/RED4ext/Common.hpp:48-53` |
| Offset asserts disabled under clang | `refs/RED4ext.SDK/include/RED4ext/Common.hpp:27-35` |
| 9,457 size asserts across 9,231 headers | `grep -rc RED4EXT_ASSERT_SIZE refs/RED4ext.SDK/include` |
| SDK targets game 2.5 (3.0.88.46235) | `refs/RED4ext.SDK/include/RED4ext/Api/v1/Runtime.hpp:41,54` |
| Static-lib SDK mode | `refs/RED4ext.SDK/CMakeLists.txt:111` (`RED4EXT_STATIC_LIB`) |
| Game-state callback types | `refs/RED4ext.SDK/include/RED4ext/GameStates.hpp:8-14` |
| Per-plugin logger API | `refs/RED4ext.SDK/include/RED4ext/Api/v1/Logger.hpp`; docs `docs.red4ext.com/mod-developers/logging` |
| RedLib requires `<format>` | `refs/cp2077-red-lib/include/RedLib.hpp:7`; `.../Engine/LogChannel.hpp:33-42` |
| clang registrar workaround | `refs/cp2077-red-lib/include/Red/TypeInfo/Macros/Definition.hpp:11-17` |
| Wine `msvcp140` has 0 `__std_*` exports | `llvm-readobj --coff-exports` on Proton 11 `x86_64-windows/msvcp140.dll` (1,489 named exports, no `_Fs*`, no `__std_remove`) |
| `ScriptableSystem` lifecycle | `refs/cyberpunk/core/systems/scriptableSystem.swift:1-17` |
| `OnSavingComplete` is menu-only | `refs/cyberpunk/cyberpunk/UI/fullscreen/ingame/pauseMenu.swift:267`, `.../pregame/saveGameMenu.swift:292`, `.../ingame/inGameMenuGameController.swift:618` |
| Save-lock manager | `refs/cyberpunk/core/systems/saveLocksManager.swift` |
| Interval tick pattern | `refs/cyberpunk/core/systems/preventionSystemAIHelperClasses.swift:687-724` |
| District-crossing event | `refs/cyberpunk/cyberpunk/player/player.swift:6140` (`OnDistrictChanged`) |
| Address library is hash-keyed, 1,118,540 entries, 84 named | `bin/x64/cyberpunk2077_addresses.json` (installed game) |
| `RelocFunc` uses fixed offsets | `refs/RED4ext.SDK/include/RED4ext/Relocation.hpp` |
| RED4ext 1.31.1 requires game ≥ 2.5 | upstream release notes, `v1.31.0` changelog |
| clang-cl/lld-link produce a valid PE DLL | local build test (`/dll /noentry /machine:x64`, exported `add`) |
| Validated flag set | local `/W4 /WX` compile, clang-cl 23.1.5 |
| Schemas valid on 3.54.1 | local `sqlite3 <schema` + `integrity_check` + `foreign_key_check` |
| Offline amalgamation available | `~/Projects/netto/third_party/sqlite3/src/sqlite3.c` (3.53.4, source id `2026-07-24`) |
| SQLite latencies | local micro-benchmark, WAL + `synchronous=NORMAL`, page cache warm (see §3.5 caveats) |
