#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   tools/format-redscript.sh [--check] [path...]
#
# Default path: src/r6/scripts
# Default action: rewrite files in place. Use --check for CI/pre-commit.

TOOLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/redscript.sh
source "$TOOLS_DIR/lib/redscript.sh"

check=0
if [[ ${1:-} == "--check" ]]; then
  check=1
  shift
fi

neon_ensure_redscript_cli

paths=("$@")
if [[ ${#paths[@]} -eq 0 ]]; then
  paths=("$NEON_ROOT/src/r6/scripts")
fi

for path in "${paths[@]}"; do
  if (( check )); then
    neon_run_cli "" format -s "$path" -c
  else
    neon_run_cli "" format -s "$path" --save
  fi
done

if (( check )); then
  printf 'Format check OK\n'
else
  printf 'Formatted %s\n' "${paths[*]}"
fi
