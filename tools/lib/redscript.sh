#!/usr/bin/env bash
# Shared helpers for the redscript CLI wrappers.
# Source this after `set -euo pipefail` from a script under tools/.

NEON_LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NEON_ROOT="$(cd "$NEON_LIB_DIR/../.." && pwd)"
# shellcheck source=versions.sh
source "$NEON_LIB_DIR/versions.sh"

NEON_GAME_DIR="${GAME_DIR:-$HOME/Games/Cyberpunk 2077}"
NEON_CACHE_DIR="${CACHE_DIR:-$HOME/.cache/neon-ascendancy}"
NEON_WARN_ARGS=(-W unused_locals)

NEON_CLI=""
NEON_CLI_USE_WINE=0

neon_fail() {
  printf '%s\n' "$*" >&2
  exit 1
}

neon_check_game() {
  [[ -f "$NEON_GAME_DIR/r6/cache/final.redscripts" ]] || \
    neon_fail "Game script cache not found under $NEON_GAME_DIR (set GAME_DIR)."
}

neon_ensure_cli_download() {
  local path="$1" url="$2" sha="$3" name
  name="$(basename "$path")"
  command -v curl >/dev/null || neon_fail 'curl is required.'
  command -v sha256sum >/dev/null || neon_fail 'sha256sum is required.'
  mkdir -p "$(dirname "$path")"

  if [[ ! -f "$path" ]]; then
    printf 'Downloading %s\n' "$name"
    curl -fL --retry 3 -o "$path.part" "$url"
    mv "$path.part" "$path"
  fi

  printf '%s  %s\n' "$sha" "$path" | sha256sum -c - >/dev/null || \
    neon_fail "Checksum mismatch for $path; delete it and retry."
}

neon_ensure_wine() {
  if [[ -z "${NEON_WINE:-}" ]]; then
    NEON_WINE="${WINE:-$(command -v wine || true)}"
  fi
  [[ -n "$NEON_WINE" ]] || neon_fail 'wine is required to run Windows redscript-cli.exe (or build a native binary; see docs/modding.md).'

  export WINEPREFIX="${REDSCRIPT_WINEPREFIX:-$NEON_CACHE_DIR/wineprefix}"
  export WINEDEBUG="${WINEDEBUG:--all}"
  mkdir -p "$WINEPREFIX"
}

# Resolve redscript-cli:
#   1. Explicit REDSCRIPT_CLI override (native binary or .exe)
#   2. Cached native Linux binary ($CACHE_DIR/redscript-cli-<version>)
#   3. Downloaded Windows binary ($CACHE_DIR/redscript-cli-<version>.exe) via Wine
neon_ensure_redscript_cli() {
  local native_default="$NEON_CACHE_DIR/redscript-cli-${NEON_REDSCRIPT_VERSION}"
  local win_default="$NEON_CACHE_DIR/redscript-cli-${NEON_REDSCRIPT_VERSION}.exe"

  if [[ -n "${REDSCRIPT_CLI:-}" ]]; then
    NEON_CLI="$REDSCRIPT_CLI"
    if [[ "$NEON_CLI" == *.exe ]]; then
      [[ -f "$NEON_CLI" ]] || neon_fail "REDSCRIPT_CLI not found: $NEON_CLI"
      NEON_CLI_USE_WINE=1
      neon_ensure_wine
    else
      [[ -x "$NEON_CLI" ]] || neon_fail "REDSCRIPT_CLI is not executable: $NEON_CLI"
      NEON_CLI_USE_WINE=0
    fi
    return
  fi

  if [[ -x "$native_default" ]]; then
    NEON_CLI="$native_default"
    NEON_CLI_USE_WINE=0
    return
  fi

  NEON_CLI="$win_default"
  neon_ensure_cli_download "$NEON_CLI" "$NEON_REDSCRIPT_CLI_URL" "$NEON_REDSCRIPT_CLI_SHA"
  NEON_CLI_USE_WINE=1
  neon_ensure_wine
}

neon_source_args() {
  local src="$NEON_ROOT/src/r6/scripts"
  [[ -d "$src" ]] || neon_fail "Missing source directory: $src"

  NEON_SOURCE_ARGS=(-s "$src")
  local dep
  for dep in \
    "$NEON_GAME_DIR/red4ext/plugins/ArchiveXL/Scripts" \
    "$NEON_GAME_DIR/red4ext/plugins/TweakXL/Scripts"; do
    [[ -d "$dep" ]] && NEON_SOURCE_ARGS+=(-s "$dep")
  done
}

# Run a CLI command, show its output, and fail if the exit code is nonzero or
# the expected success marker is missing.
neon_run_cli() {
  local marker="$1"
  shift
  local log status
  log="$(mktemp "${TMPDIR:-/tmp}/neon-redscript.XXXXXX")"

  local cmd=("$NEON_CLI" "$@")
  if (( NEON_CLI_USE_WINE )); then
    cmd=("$NEON_WINE" "$NEON_CLI" "$@")
  fi

  set +e
  "${cmd[@]}" 2>&1 | tee "$log"
  status=${PIPESTATUS[0]}
  set -e

  if (( status != 0 )) || { [[ -n "$marker" ]] && ! grep -qF -- "$marker" "$log"; }; then
    rm -f "$log"
    neon_fail "redscript command failed: $*"
  fi

  rm -f "$log"
}
