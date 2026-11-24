#!/usr/bin/env bash
set -euo pipefail

TOOLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/redscript.sh
source "$TOOLS_DIR/lib/redscript.sh"

neon_check_game
neon_ensure_redscript_cli
neon_source_args

neon_run_cli "Compilation successful" lint \
  "${NEON_WARN_ARGS[@]}" \
  "${NEON_SOURCE_ARGS[@]}" \
  -b "$NEON_GAME_DIR/r6/cache/final.redscripts"

printf 'Lint OK\n'
