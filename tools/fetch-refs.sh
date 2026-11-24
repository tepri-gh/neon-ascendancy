#!/usr/bin/env bash
set -euo pipefail

# Clone gitignored reference repositories into refs/:
#   cyberpunk       - Decompiled vanilla Cyberpunk 2077 scripts (.swift files containing REDscript)
#   RED4ext.SDK     - Native engine/RTTI type reference (and future native plugin option)
#   cp2077-red-lib  - Native RED4ext C++ wrapper reference (not required for .reds builds)

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REFS="$ROOT/refs"

mkdir -p "$REFS"

clone() {
  local name="$1" url="$2"
  if [[ -d "$REFS/$name/.git" ]]; then
    printf '%s already present, skipping (remove %s to refresh)\n' "$name" "$REFS/$name"
    return
  fi
  printf 'Cloning %s\n' "$name"
  git clone --depth 1 "$url" "$REFS/$name"
}

clone cyberpunk https://codeberg.org/adamsmasher/cyberpunk.git
clone RED4ext.SDK https://github.com/wopss/RED4ext.SDK.git
clone cp2077-red-lib https://github.com/psiberx/cp2077-red-lib.git

printf '\nReference checkouts:\n'
printf '  game scripts: %s (files use .swift extension but are REDscript)\n' "$REFS/cyberpunk"
printf '  RED4ext SDK:  %s (native RTTI/type reference)\n' "$REFS/RED4ext.SDK"
printf '  RedLib:       %s (native plugin reference)\n' "$REFS/cp2077-red-lib"
