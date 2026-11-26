#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GAME_DIR="${GAME_DIR:-$HOME/Games/Cyberpunk 2077}"
MOD_NAME="NeonAscendancy"
SRC="$ROOT/src/r6/scripts/$MOD_NAME"
DEST="$GAME_DIR/r6/scripts/$MOD_NAME"
TWEAKS_SRC="$ROOT/src/r6/tweaks/$MOD_NAME"
TWEAKS_DEST="$GAME_DIR/r6/tweaks/$MOD_NAME"
NATIVE_DLL="$ROOT/build/win/$MOD_NAME.dll"
NATIVE_PDB="$ROOT/build/win/$MOD_NAME.pdb"
WORLD_DB="$ROOT/dist/world.db"
WORLD_ARCHIVE="$ROOT/dist/neon_ascendancy_world.archive"
WORLD_ARCHIVE_CONFIG="$ROOT/src/archive/pc/mod/neon_ascendancy_world.archive.xl"
NATIVE_DEST="$GAME_DIR/red4ext/plugins/$MOD_NAME"
ARCHIVE_DEST="$GAME_DIR/archive/pc/mod/neon_ascendancy_world.archive"
SCRIPTS_ONLY=0

while (($# > 0)); do
  case "$1" in
    --scripts-only) SCRIPTS_ONLY=1 ;;
    -h|--help)
      printf 'Usage: %s [--scripts-only]\n' "$0"
      printf 'Deploys .reds scripts to <game>/r6/scripts/%s and (when built, unless\n' "$MOD_NAME"
      printf -- '--scripts-only) deploys %s.dll + world.db to <game>/red4ext/plugins/%s\n' "$MOD_NAME" "$MOD_NAME"
      printf 'while preserving existing playthroughs/ databases.\n'
      exit 0
      ;;
    *)
      printf 'Unknown argument: %s\n' "$1" >&2
      exit 2
      ;;
  esac
  shift
done

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

if [[ -d "$TWEAKS_SRC" ]]; then
  rm -rf "$TWEAKS_DEST"
  mkdir -p "$TWEAKS_DEST"
  tweak_count=0
  while IFS= read -r -d '' file; do
    rel="${file#"$TWEAKS_SRC"/}"
    mkdir -p "$TWEAKS_DEST/$(dirname "$rel")"
    cp -a "$file" "$TWEAKS_DEST/$rel"
    tweak_count=$((tweak_count + 1))
  done < <(find "$TWEAKS_SRC" -type f \( -name '*.yaml' -o -name '*.yml' -o -name '*.tweak' \) -print0)
  printf 'Deployed %s (%d tweak files) to %s\n' "$MOD_NAME" "$tweak_count" "$TWEAKS_DEST"
fi

if ((SCRIPTS_ONLY == 0)) && [[ -f "$NATIVE_DLL" ]]; then
  if [[ ! -f "$WORLD_DB" ]]; then
    printf 'Found %s but missing %s — run python3 tools/build-world-db.py first.\n' "$NATIVE_DLL" "$WORLD_DB" >&2
    exit 1
  fi
  # Preserve existing playthroughs/ directory under NATIVE_DEST!
  mkdir -p "$NATIVE_DEST"
  cp -f "$NATIVE_DLL" "$NATIVE_DEST/$MOD_NAME.dll"
  cp -f "$WORLD_DB" "$NATIVE_DEST/world.db"
  if [[ -f "$NATIVE_PDB" ]]; then
    cp -f "$NATIVE_PDB" "$NATIVE_DEST/$MOD_NAME.pdb"
  fi
  printf 'Deployed native plugin + world.db to %s (playthroughs/ preserved)\n' "$NATIVE_DEST"
fi

if ((SCRIPTS_ONLY == 0)) && [[ -f "$WORLD_ARCHIVE" ]]; then
  mkdir -p "$(dirname "$ARCHIVE_DEST")"
  cp -f "$WORLD_ARCHIVE" "$ARCHIVE_DEST"
  cp -f "$WORLD_ARCHIVE_CONFIG" "$ARCHIVE_DEST.xl"
  printf 'Deployed clean-slate world archive to %s\n' "$ARCHIVE_DEST"
fi
