#!/usr/bin/env bash
set -euo pipefail

# Install the pinned DEV-ONLY Cyber Engine Tweaks (CET) release into the game directory.
# CET is NOT part of the baseline mod dependency stack; it is used during development
# for runtime FTLog capture, interactive console probes (tools/probes/neon_probe.lua),
# and rapid schema checks.
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
  printf 'Close Cyberpunk 2077 before installing CET.\n' >&2
  exit 1
fi

command -v curl >/dev/null || { printf 'curl is required\n' >&2; exit 1; }
command -v unzip >/dev/null || { printf 'unzip is required\n' >&2; exit 1; }
command -v sha256sum >/dev/null || { printf 'sha256sum is required\n' >&2; exit 1; }

mkdir -p "$CACHE_DIR"
zip="$CACHE_DIR/CET-${NEON_CET_VERSION}.zip"

if [[ ! -f "$zip" ]]; then
  printf 'Downloading dev-only CET %s\n' "$NEON_CET_VERSION"
  curl -fL --retry 3 --retry-delay 2 -o "$zip.part" "$NEON_CET_URL"
  mv "$zip.part" "$zip"
fi

printf '%s  %s\n' "$NEON_CET_SHA" "$zip" | sha256sum -c - >/dev/null
printf 'Installing dev-only CET %s into %s\n' "$NEON_CET_VERSION" "$GAME_DIR"
unzip -oq "$zip" -d "$GAME_DIR"

GAME_DIR="$GAME_DIR" "$TOOLS_DIR/deploy-probe.sh"

printf '\nInstalled dev-only CET %s and NeonAscendancyProbe helper.\n' "$NEON_CET_VERSION"
printf 'Remember: WINEDLLOVERRIDES=winmm,version=n,b loads both RED4ext (winmm) and CET (version).\n'
printf 'In CET console, run: p = GetMod("NeonAscendancyProbe"); p.help()\n'
