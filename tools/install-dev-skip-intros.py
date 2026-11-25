#!/usr/bin/env python3
"""Build and install a dev-only archive that skips Cyberpunk 2077's startup
splash logos, seizure warning, and intro video for fast iteration.

Targets `base\\gameplay\\gui\\fullscreen\\splash_screen_loading\\splash_screen_loading_animations.inkanim`
from `basegame_1_engine.archive`, collapsing every splash/intro sequence
(`logo_train`, `logo_train_long`, `loc_message`, `game_intro`, `after_skip_pressed`)
to 0.01 s with audio events muted, and packs the single override into:

  <GAME_DIR>/archive/pc/mod/dev_skip_intros.archive

Pair with `-skipStartScreen` on the game command line to go straight to the
Main Menu. Pass `--uninstall` to remove the dev archive cleanly.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DEFAULT_WK = Path(
    os.environ.get(
        "WK_CLI",
        Path.home() / ".cache" / "neon-ascendancy" / "wolvenkit-10.0.0-beta.1" / "WolvenKit.CLI",
    )
)
DEFAULT_GAME_DIR = Path(os.environ.get("GAME_DIR", Path.home() / "Games" / "Cyberpunk 2077"))
ANIM_REL = "base/gameplay/gui/fullscreen/splash_screen_loading/splash_screen_loading_animations.inkanim"
ARCHIVE_NAME = "dev_skip_intros.archive"


def run_wk(wk: Path, args: list[str]) -> subprocess.CompletedProcess:
    env = {**os.environ, "DOTNET_ROLL_FORWARD": "Major"}
    proc = subprocess.run([str(wk), *args], env=env, capture_output=True, text=True)
    if proc.returncode != 0 or "Error" in proc.stdout or "Error" in proc.stderr:
        raise RuntimeError(
            f"WolvenKit.CLI failed (rc={proc.returncode}): {' '.join(args)}\n"
            f"stdout:\n{proc.stdout[-1500:]}\nstderr:\n{proc.stderr[-1500:]}"
        )
    return proc


def shorten_sequences(doc: dict) -> list[str]:
    names: list[str] = []
    for seq in doc["Data"]["RootChunk"].get("sequences", []):
        sd = seq["Data"]
        names.append(sd["name"]["$value"])
        for df in sd.get("definitions", []):
            dd = df["Data"]
            dd["events"] = []
            for interp in dd.get("interpolators", []):
                id_ = interp["Data"]
                if "duration" in id_:
                    id_["duration"] = 0.01
                if "startDelay" in id_:
                    id_["startDelay"] = 0
                if "synchronizeToAudio" in id_:
                    id_["synchronizeToAudio"] = 0
                if isinstance(id_.get("audioEvent"), dict) and "$value" in id_["audioEvent"]:
                    id_["audioEvent"]["$value"] = "None"
    return names


def main() -> int:
    ap = argparse.ArgumentParser(description="Install/uninstall dev-only skip-intro-splashes archive.")
    ap.add_argument("--wk-cli", type=Path, default=DEFAULT_WK)
    ap.add_argument("--game-dir", type=Path, default=DEFAULT_GAME_DIR)
    ap.add_argument("--uninstall", action="store_true")
    args = ap.parse_args()

    mod_dir = args.game_dir / "archive" / "pc" / "mod"
    out_archive = mod_dir / ARCHIVE_NAME

    if args.uninstall:
        if out_archive.exists():
            out_archive.unlink()
            print(f"Removed {out_archive}")
        else:
            print(f"Already absent: {out_archive}")
        return 0

    if not args.wk_cli.is_file():
        raise FileNotFoundError(f"WolvenKit.CLI not found at {args.wk_cli}")
    engine_arch = args.game_dir / "archive" / "pc" / "content" / "basegame_1_engine.archive"
    if not engine_arch.is_file():
        raise FileNotFoundError(f"Missing base archive: {engine_arch}")

    with tempfile.TemporaryDirectory(prefix="na-skip-intros-") as tmp_s:
        tmp = Path(tmp_s)
        ext = tmp / "ext"
        ext.mkdir()
        run_wk(args.wk_cli, ["extract", str(engine_arch), "-o", str(ext), "-r", r"splash_screen_loading_animations\.inkanim$"])
        anim_path = ext / ANIM_REL
        if not anim_path.is_file():
            raise FileNotFoundError(f"Expected extracted animation missing: {anim_path}")
        run_wk(args.wk_cli, ["convert", "serialize", str(anim_path)])

        json_path = Path(str(anim_path) + ".json")
        doc = json.loads(json_path.read_text(encoding="utf-8"))
        names = shorten_sequences(doc)
        if not names:
            raise RuntimeError("No animation sequences found in splash_screen_loading_animations.inkanim")
        json_path.write_text(json.dumps(doc, indent=2), encoding="utf-8")

        run_wk(args.wk_cli, ["convert", "deserialize", str(json_path)])

        pack_root = tmp / "dev_skip_intros"
        dest_anim = pack_root / ANIM_REL
        dest_anim.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(anim_path, dest_anim)

        out_dir = tmp / "out"
        out_dir.mkdir()
        run_wk(args.wk_cli, ["pack", str(pack_root), "-o", str(out_dir)])
        packed = out_dir / ARCHIVE_NAME
        if not packed.is_file():
            raise RuntimeError(f"Expected packed archive missing: {packed}")

        # Round-trip verify packed archive
        chk = tmp / "chk"
        chk.mkdir()
        run_wk(args.wk_cli, ["extract", str(packed), "-o", str(chk)])
        chk_anim = chk / ANIM_REL
        if not chk_anim.is_file():
            raise RuntimeError("Round-trip verify failed: animation missing from packed archive")
        run_wk(args.wk_cli, ["convert", "serialize", str(chk_anim)])
        chk_doc = json.loads(Path(str(chk_anim) + ".json").read_text(encoding="utf-8"))
        for seq in chk_doc["Data"]["RootChunk"].get("sequences", []):
            for df in seq["Data"].get("definitions", []):
                assert not df["Data"].get("events"), "unexpected sound event survived"
                for interp in df["Data"].get("interpolators", []):
                    dur = interp["Data"].get("duration", 0)
                    assert dur <= 0.02, f"duration not shortened: {dur}"

        mod_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(packed, out_archive)

    print(f"Installed {out_archive} ({out_archive.stat().st_size} bytes); shortened sequences: {names}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
