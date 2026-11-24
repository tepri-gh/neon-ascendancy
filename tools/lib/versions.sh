#!/usr/bin/env bash
# Single source of truth for pinned Cyberpunk 2077 framework, dev-tool, and
# native build versions + SHA-256 checksums.
# Source this after `set -euo pipefail` from scripts under tools/.

# shellcheck disable=SC2034
NEON_GAME_VERSION="2.5"

# Pinned runtime framework releases (Codeware omitted until a release supports redscript 1.x).
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

# Standalone redscript CLI (Windows .exe default; optional native Linux binary auto-detected).
# shellcheck disable=SC2034
NEON_REDSCRIPT_CLI_URL="https://github.com/jac3km4/redscript/releases/download/v${NEON_REDSCRIPT_VERSION}/redscript-cli.exe"
# shellcheck disable=SC2034
NEON_REDSCRIPT_CLI_SHA="43e05ea38e46ba4f79c19f6262f1a5a9d6f356865980ac9a1d665670ba6af63b"

# Dev-only Cyber Engine Tweaks (installed explicitly via tools/install-dev-cet.sh).
# shellcheck disable=SC2034
NEON_CET_VERSION="1.38.1"
# shellcheck disable=SC2034
NEON_CET_URL="https://github.com/maximegmd/CyberEngineTweaks/releases/download/v${NEON_CET_VERSION}/cet_1_38_1.zip"
# shellcheck disable=SC2034
NEON_CET_SHA="2e52be4ed431fad787e64ecbf75db346b4224577d2b89894912bc3f159020e73"

# Offline world extraction binary (native Linux ELF; requires .NET + DOTNET_ROLL_FORWARD=Major).
# shellcheck disable=SC2034
NEON_WOLVENKIT_VERSION="10.0.0-beta.1"
# shellcheck disable=SC2034
NEON_WOLVENKIT_URL="https://github.com/WolvenKit/WolvenKit/releases/download/${NEON_WOLVENKIT_VERSION}/WolvenKit.ConsoleLinux-${NEON_WOLVENKIT_VERSION}.zip"
# shellcheck disable=SC2034
NEON_WOLVENKIT_SHA="561ff1387cb09e529c40a115cb55e12be0215653415dd2c6131c9c3f320f07d4"

# Native plugin toolchain & embedded SQLite3 amalgamation.
# shellcheck disable=SC2034
NEON_XWIN_VERSION="0.10.0"
# shellcheck disable=SC2034
NEON_XWIN_URL="https://github.com/Jake-Shadle/xwin/releases/download/${NEON_XWIN_VERSION}/xwin-${NEON_XWIN_VERSION}-x86_64-unknown-linux-musl.tar.gz"
# shellcheck disable=SC2034
NEON_XWIN_SHA="d870eb4b2f390878af6da1ccd3cf321d22fcb72720984853b4be732ae597fc88"

# shellcheck disable=SC2034
NEON_SQLITE_VERSION="3.54.1"
# shellcheck disable=SC2034
NEON_SQLITE_URL="https://www.sqlite.org/2026/sqlite-amalgamation-3540100.zip"
# shellcheck disable=SC2034
NEON_SQLITE_SHA="0a9c8e34352dad46006aa82836d5383bff9dc6bc9ce5a60553c05aa30e6ad1f9"

# Pinned native SDK commits compatible with Cyberpunk 2077 2.5 (do not use 1.0.0 tag).
# shellcheck disable=SC2034
NEON_RED4EXT_SDK_COMMIT="a34f0ad0a9e4f37cbe1fe001e4ff68c2949d0665"
# shellcheck disable=SC2034
NEON_REDLIB_COMMIT="48cb21d4d22f63c8fcaa85aae6ac0fb1d9f24db6"
