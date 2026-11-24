#!/usr/bin/env bash
set -euo pipefail

# Provision gitignored native build dependencies under native/third_party/ and
# (with --xwin) the MSVC CRT/Windows SDK splat under ~/.cache/neon-ascendancy/xwin.
# All versions and checksums are pinned in tools/lib/versions.sh.

TOOLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$TOOLS_DIR/.." && pwd)"
# shellcheck source=lib/versions.sh
source "$TOOLS_DIR/lib/versions.sh"

CACHE="${CACHE_DIR:-$HOME/.cache/neon-ascendancy}"
DL="$CACHE/downloads"
TP="$ROOT/native/third_party"
WITH_XWIN=0

for arg in "$@"; do
  case "$arg" in
    --xwin) WITH_XWIN=1 ;;
    *) printf 'Usage: %s [--xwin]\n' "$0" >&2; exit 1 ;;
  esac
done

command -v curl >/dev/null || { printf 'curl is required\n' >&2; exit 1; }
command -v unzip >/dev/null || { printf 'unzip is required\n' >&2; exit 1; }
command -v sha256sum >/dev/null || { printf 'sha256sum is required\n' >&2; exit 1; }
command -v git >/dev/null || { printf 'git is required\n' >&2; exit 1; }

mkdir -p "$DL" "$TP"

# 1. SQLite amalgamation
SQLITE_ZIP="$DL/sqlite-amalgamation-${NEON_SQLITE_VERSION}.zip"
if [[ ! -f "$SQLITE_ZIP" ]]; then
  if [[ -f "$DL/sqlite-amalgamation-3540100.zip" ]]; then
    cp "$DL/sqlite-amalgamation-3540100.zip" "$SQLITE_ZIP"
  else
    printf 'Downloading SQLite %s amalgamation\n' "$NEON_SQLITE_VERSION"
    curl -fsSL --retry 3 -o "$SQLITE_ZIP.part" "$NEON_SQLITE_URL"
    mv "$SQLITE_ZIP.part" "$SQLITE_ZIP"
  fi
fi
printf '%s  %s\n' "$NEON_SQLITE_SHA" "$SQLITE_ZIP" | sha256sum -c - >/dev/null

if [[ ! -f "$TP/sqlite/sqlite3.c" || ! -f "$TP/sqlite/sqlite3.h" ]]; then
  rm -rf "$TP/sqlite" "$TP/sqlite.tmp"
  mkdir -p "$TP/sqlite" "$TP/sqlite.tmp"
  unzip -oq "$SQLITE_ZIP" -d "$TP/sqlite.tmp"
  cp "$TP/sqlite.tmp"/*/sqlite3.c "$TP/sqlite.tmp"/*/sqlite3.h "$TP/sqlite/"
  rm -rf "$TP/sqlite.tmp"
  printf 'Prepared SQLite %s in native/third_party/sqlite/\n' "$NEON_SQLITE_VERSION"
fi

# 2. Pinned RED4ext.SDK & cp2077-red-lib commits (reuse refs/ if matching commit exists)
fetch_repo_commit() {
  local name="$1" url="$2" commit="$3" ref_dir="$4"
  local dest="$TP/$name"

  if [[ -d "$dest/.git" ]] && [[ "$(git -C "$dest" rev-parse HEAD 2>/dev/null || true)" == "$commit" ]]; then
    printf '%s already at %s\n' "$name" "${commit:0:10}"
    return
  fi

  rm -rf "$dest"
  if [[ -d "$ref_dir/.git" ]] && [[ "$(git -C "$ref_dir" rev-parse HEAD 2>/dev/null || true)" == "$commit" ]]; then
    printf 'Cloning %s (%s) from local refs/\n' "$name" "${commit:0:10}"
    git clone --quiet "$ref_dir" "$dest"
    git -C "$dest" checkout --quiet "$commit"
    return
  fi

  printf 'Fetching %s at %s\n' "$name" "${commit:0:10}"
  git init --quiet "$dest"
  git -C "$dest" remote add origin "$url"
  git -C "$dest" fetch --depth 1 origin "$commit"
  git -C "$dest" checkout --quiet FETCH_HEAD
}

fetch_repo_commit "RED4ext.SDK" "https://github.com/wopss/RED4ext.SDK.git" "$NEON_RED4EXT_SDK_COMMIT" "$ROOT/refs/RED4ext.SDK"
fetch_repo_commit "RedLib" "https://github.com/psiberx/cp2077-red-lib.git" "$NEON_REDLIB_COMMIT" "$ROOT/refs/cp2077-red-lib"

# 3. Optional xwin MSVC CRT + Windows SDK splat (for Linux -> Windows cross-compile)
if (( WITH_XWIN )); then
  XWIN_TGZ="$DL/xwin-${NEON_XWIN_VERSION}-x86_64-unknown-linux-musl.tar.gz"
  if [[ ! -f "$XWIN_TGZ" ]]; then
    printf 'Downloading xwin %s\n' "$NEON_XWIN_VERSION"
    curl -fsSL --retry 3 -o "$XWIN_TGZ.part" "$NEON_XWIN_URL"
    mv "$XWIN_TGZ.part" "$XWIN_TGZ"
  fi
  printf '%s  %s\n' "$NEON_XWIN_SHA" "$XWIN_TGZ" | sha256sum -c - >/dev/null

  if [[ ! -x "$CACHE/bin/xwin" ]]; then
    mkdir -p "$CACHE/bin"
    tar -xzf "$XWIN_TGZ" --strip-components=1 -C "$CACHE/bin" "xwin-${NEON_XWIN_VERSION}-x86_64-unknown-linux-musl/xwin"
    chmod +x "$CACHE/bin/xwin"
  fi

  XWIN_OUT="${XWIN_ROOT:-$CACHE/xwin}"
  if [[ ! -f "$XWIN_OUT/crt/lib/x86_64/libcmt.lib" || ! -f "$XWIN_OUT/crt/lib/x86_64/libcpmt.lib" ]]; then
    printf 'Running xwin splat into %s\n' "$XWIN_OUT"
    "$CACHE/bin/xwin" --accept-license --arch x86_64 --cache-dir "$CACHE/xwin-cache" splat --output "$XWIN_OUT"
  fi
  printf 'xwin splat ready at %s\n' "$XWIN_OUT"
fi

printf 'Native dependencies ready.\n'
