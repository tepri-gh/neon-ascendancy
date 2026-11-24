#!/usr/bin/env bash
set -euo pipefail

TOOLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/redscript.sh
source "$TOOLS_DIR/lib/redscript.sh"

neon_check_game
neon_ensure_redscript_cli
neon_source_args

mkdir -p "$NEON_ROOT/dist"
rm -f "$NEON_ROOT/dist/final_patched.redscripts"

neon_run_cli "Compilation successful" compile \
  "${NEON_WARN_ARGS[@]}" \
  "${NEON_SOURCE_ARGS[@]}" \
  -b "$NEON_GAME_DIR/r6/cache/final.redscripts" \
  -o "$NEON_ROOT/dist/final_patched.redscripts"

printf 'Compiled OK: %s\n' "$NEON_ROOT/dist/final_patched.redscripts"
