#!/usr/bin/env bash
# Copy the dev-only CET probe (tools/probes/) into the game's CET mods folder:
# neon_probe.lua -> init.lua, plus the generated tour and access stop lists. Idempotent; does
# not touch CET itself (tools/install-dev-cet.sh installs CET). Dev-only, never
# part of the shipping mod.
set -euo pipefail
TOOLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GAME_DIR="${GAME_DIR:-$HOME/Games/Cyberpunk 2077}"
DEST="$GAME_DIR/bin/x64/plugins/cyber_engine_tweaks/mods/NeonAscendancyProbe"
if [[ ! -d "$GAME_DIR/bin/x64/plugins/cyber_engine_tweaks" ]]; then
  echo "CET is not installed in $GAME_DIR; run tools/install-dev-cet.sh first." >&2
  exit 1
fi
mkdir -p "$DEST"
cp -a "$TOOLS_DIR/probes/neon_probe.lua" "$DEST/init.lua"
cp -a "$TOOLS_DIR/probes/tour_stops.lua" "$DEST/tour_stops.lua"
cp -a "$TOOLS_DIR/probes/access_stops.lua" "$DEST/access_stops.lua"
echo "Deployed NeonAscendancyProbe (init.lua, tour_stops.lua, access_stops.lua) to $DEST"
