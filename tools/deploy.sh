#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GAME_DIR="${GAME_DIR:-$HOME/Games/Cyberpunk 2077}"
MOD_NAME="NeonAscendancy"
SRC="$ROOT/src/r6/scripts/$MOD_NAME"
DEST="$GAME_DIR/r6/scripts/$MOD_NAME"

if pgrep -f '[C]yberpunk2077\.exe' >/dev/null 2>&1; then
  printf 'Close Cyberpunk 2077 before deploying.\n' >&2
  exit 1
fi

if [[ ! -d "$SRC" ]]; then
  printf 'No script sources at %s\n' "$SRC" >&2
  exit 1
fi

# Mod folder only: leave other installed mods untouched.
rm -rf "$DEST"
mkdir -p "$DEST"

count=0
while IFS= read -r -d '' file; do
  rel="${file#"$SRC"/}"
  mkdir -p "$DEST/$(dirname "$rel")"
  cp -a "$file" "$DEST/$rel"
  count=$((count + 1))
done < <(find "$SRC" -type f -name '*.reds' -print0)

printf 'Deployed %s (%d .reds files) to %s\n' "$MOD_NAME" "$count" "$DEST"
