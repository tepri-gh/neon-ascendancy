#!/usr/bin/env bash
set -euo pipefail

TOOLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# `compile` runs the same full analysis pass as `lint` before writing the
# output bundle, so we skip running `lint-redscript.sh` twice here.
"$TOOLS_DIR/format-redscript.sh" --check
"$TOOLS_DIR/check-redscript.sh"

printf 'All checks passed\n'
