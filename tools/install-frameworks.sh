#!/usr/bin/env bash
set -euo pipefail

# Install the pinned Cyberpunk 2077 redscript stack into the game directory.
# Works on a plain Wine/Proton install; no Steam, launcher, or account needed.
#
# Override GAME_DIR or CACHE_DIR if your paths differ.

TOOLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/versions.sh
source "$TOOLS_DIR/lib/versions.sh"

GAME_DIR="${GAME_DIR:-$HOME/Games/Cyberpunk 2077}"
CACHE_DIR="${CACHE_DIR:-$HOME/.cache/neon-ascendancy/frameworks}"

if [[ ! -f "$GAME_DIR/bin/x64/Cyberpunk2077.exe" ]]; then
  printf 'Game not found at %s\n' "$GAME_DIR" >&2
  printf 'Set GAME_DIR to the directory containing bin/x64/Cyberpunk2077.exe.\n' >&2
  exit 1
fi

if pgrep -f '[C]yberpunk2077\.exe' >/dev/null 2>&1; then
  printf 'Close Cyberpunk 2077 before installing frameworks.\n' >&2
  exit 1
fi

command -v curl >/dev/null || { printf 'curl is required\n' >&2; exit 1; }
command -v unzip >/dev/null || { printf 'unzip is required\n' >&2; exit 1; }
command -v sha256sum >/dev/null || { printf 'sha256sum is required\n' >&2; exit 1; }

mkdir -p "$CACHE_DIR"

for entry in "${NEON_FRAMEWORKS[@]}"; do
  IFS='|' read -r name version url sha <<<"$entry"
  zip="$CACHE_DIR/$name-$version.zip"

  if [[ ! -f "$zip" ]]; then
    printf 'Downloading %s %s\n' "$name" "$version"
    curl -fL --retry 3 --retry-delay 2 -o "$zip.part" "$url"
    mv "$zip.part" "$zip"
  fi

  printf '%s  %s\n' "$sha" "$zip" | sha256sum -c - >/dev/null
  printf 'Installing %s %s\n' "$name" "$version"
  unzip -oq "$zip" -d "$GAME_DIR"
done

# Standard mod destinations.
mkdir -p \
  "$GAME_DIR/archive/pc/mod" \
  "$GAME_DIR/r6/scripts" \
  "$GAME_DIR/r6/tweaks"

printf '\nInstalled (target Cyberpunk 2077 %s):\n' "$NEON_GAME_VERSION"
for entry in "${NEON_FRAMEWORKS[@]}"; do
  IFS='|' read -r name version _ _ <<<"$entry"
  printf '  %s %s\n' "$name" "$version"
done
printf '\nLaunch with WINEDLLOVERRIDES=winmm,version=n,b so RED4ext loads.\n'
