#!/usr/bin/env bash
# Single source of truth for pinned Cyberpunk 2077 framework and CLI versions.
# Source this after `set -euo pipefail` from scripts under tools/.

# shellcheck disable=SC2034
NEON_GAME_VERSION="2.5"

# Pinned framework releases (Codeware is omitted until a release supports redscript 1.x).
# Format: name|version|url|sha256
# shellcheck disable=SC2034
NEON_RED4EXT_VERSION="1.31.1"
NEON_REDSCRIPT_VERSION="1.0.2"
NEON_ARCHIVEXL_VERSION="1.28.11"
NEON_TWEAKXL_VERSION="1.12.2"

# shellcheck disable=SC2034
NEON_FRAMEWORKS=(
  "RED4ext|${NEON_RED4EXT_VERSION}|https://github.com/WopsS/RED4ext/releases/download/v${NEON_RED4EXT_VERSION}/red4ext-${NEON_RED4EXT_VERSION}.zip|ce10bda503fd48c8674ef3e517d635636a262c089055f189caabeb300eef7932"
  "redscript|${NEON_REDSCRIPT_VERSION}|https://github.com/jac3km4/redscript/releases/download/v${NEON_REDSCRIPT_VERSION}/redscript-v${NEON_REDSCRIPT_VERSION}-windows.zip|c29604bb56bb7ee6799dc66b749b4f52d3688fa99574c41c1a0ab8ee955743c0"
  "ArchiveXL|${NEON_ARCHIVEXL_VERSION}|https://github.com/psiberx/cp2077-archive-xl/releases/download/v${NEON_ARCHIVEXL_VERSION}/ArchiveXL-${NEON_ARCHIVEXL_VERSION}.zip|cfb45741aa76bcb010f433fadb541a1c627f732c00fe5ebf72aafcb3785acaa8"
  "TweakXL|${NEON_TWEAKXL_VERSION}|https://github.com/psiberx/cp2077-tweak-xl/releases/download/v${NEON_TWEAKXL_VERSION}/TweakXL-${NEON_TWEAKXL_VERSION}.zip|b416a3d063823b347e933c30f7acafb1539813e9a36cce89d282f3b649705128"
)

# Standalone Windows CLI used by tools/ (or overridden by a native Linux build).
# shellcheck disable=SC2034
NEON_REDSCRIPT_CLI_URL="https://github.com/jac3km4/redscript/releases/download/v${NEON_REDSCRIPT_VERSION}/redscript-cli.exe"
# shellcheck disable=SC2034
NEON_REDSCRIPT_CLI_SHA="43e05ea38e46ba4f79c19f6262f1a5a9d6f356865980ac9a1d665670ba6af63b"
