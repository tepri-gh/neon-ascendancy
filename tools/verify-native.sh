#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
XWIN_ROOT="${XWIN_ROOT:-$HOME/.cache/neon-ascendancy/xwin}"
LINUX_ONLY=0

while (($# > 0)); do
  case "$1" in
    --linux-only) LINUX_ONLY=1 ;;
    -h|--help)
      printf 'Usage: %s [--linux-only]\n' "$0"
      printf 'Verifies deterministic world.db build, Linux C++20 unit tests,\n'
      printf 'and (unless --linux-only) Windows x64 /MT RED4ext DLL cross-compile + PE gates.\n'
      exit 0
      ;;
    *)
      printf 'Unknown argument: %s\n' "$1" >&2
      exit 2
      ;;
  esac
  shift
done

printf '=== 1/3 Deterministic world.db build & check ===\n'
python3 "$ROOT/tools/build-world-db.py"
python3 "$ROOT/tools/build-world-db.py" --check

printf '=== 2/3 Native C++20 host build & unit tests ===\n'
cmake -S "$ROOT/native" -B "$ROOT/build/linux" -G Ninja \
  -DNEON_BUILD_PLUGIN=OFF \
  -DNEON_BUILD_TESTS=ON \
  -DCMAKE_BUILD_TYPE=Debug
cmake --build "$ROOT/build/linux"
ctest --test-dir "$ROOT/build/linux" --output-on-failure

if ((LINUX_ONLY)); then
  printf 'Native Linux verification passed (--linux-only)\n'
  exit 0
fi

printf '=== 3/3 Windows x64 /MT RED4ext plugin cross-compile & PE gates ===\n'
if [[ ! -d "$XWIN_ROOT/crt/include" ]]; then
  printf 'Missing xwin splat at %s (run tools/fetch-native-deps.sh --xwin)\n' "$XWIN_ROOT" >&2
  exit 1
fi

cmake -S "$ROOT/native" -B "$ROOT/build/win" -G Ninja \
  -DCMAKE_TOOLCHAIN_FILE="$ROOT/native/cmake/x86_64-windows-msvc-clang.cmake" \
  -DXWIN_ROOT="$XWIN_ROOT" \
  -DNEON_BUILD_PLUGIN=ON \
  -DNEON_BUILD_TESTS=OFF \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake --build "$ROOT/build/win"

DLL="$ROOT/build/win/NeonAscendancy.dll"
if [[ ! -f "$DLL" ]]; then
  printf 'Expected DLL not found: %s\n' "$DLL" >&2
  exit 1
fi

headers="$(llvm-readobj --file-headers "$DLL")"
if ! grep -q 'IMAGE_FILE_MACHINE_AMD64' <<<"$headers"; then
  printf 'PE check failed: DLL is not IMAGE_FILE_MACHINE_AMD64\n' >&2
  exit 1
fi

exports="$(llvm-readobj --coff-exports "$DLL")"
for sym in Main Query Supports; do
  if ! grep -Eq "Name:[[:space:]]+$sym$" <<<"$exports"; then
    printf 'PE export gate failed: missing exported symbol %s\n' "$sym" >&2
    exit 1
  fi
done

imports="$(llvm-readobj --coff-imports "$DLL")"
if grep -Eiq 'msvcp140|vcruntime140|ucrtbase' <<<"$imports"; then
  printf 'PE import gate failed: dynamic MSVC CRT import detected (must link /MT)\n' >&2
  grep -Ei 'Name:|msvcp140|vcruntime140|ucrtbase' <<<"$imports" >&2
  exit 1
fi

imported_dlls="$(grep -E '^[[:space:]]*Name:' <<<"$imports" | sed 's/^[[:space:]]*Name:[[:space:]]*//' | sort -u | paste -sd ', ' -)"
printf 'PE gates OK: %s (%s bytes), exports={Main,Query,Supports}, imports={%s}\n' \
  "$DLL" "$(stat -c '%s' "$DLL")" "$imported_dlls"
printf 'Native verification passed\n'
