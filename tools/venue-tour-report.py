#!/usr/bin/env python3
"""Turn a dev tour into a per-venue anomaly report.

Reads the CET probe's tour.log and notes.log (JSON lines, written by
tools/probes/neon_probe.lua) and the native log's DoorPolicy lines, and
writes a Markdown report: one section per stop with flags, the NPC posture
summary, door decisions inside the stop's radius, and the playtest notes
taken near it. See docs/venue-playbook.md section 7.

Flags:
  EMPTY        no NPC within the radius
  ALERT        NPCs in Alerted/Combat/Stealth/Fear high-level states
  HOSTILE      NPCs hostile to the player
  NO-WORKSPOT  more than half the living NPCs are not in a workspot
  DEAD         dead NPCs (bodies that should not be there)
  MISSING      expected character records that were not found
  DOORS        doors the policy still found impassable after its recheck

Usage:
  tools/venue-tour-report.py [--out FILE] [--since "YYYY-MM-DD HH:MM:SS"]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

GAME = Path.home() / "Games" / "Cyberpunk 2077"
PROBE = GAME / "bin" / "x64" / "plugins" / "cyber_engine_tweaks" / "mods" / "NeonAscendancyProbe"
NATIVE_LOGS = GAME / "red4ext" / "logs"
DEFAULT_OUT = Path.home() / ".cache" / "neon-ascendancy" / "extracts" / "venues" / "tour-report.md"
BAD_STATES = {"Alerted", "Combat", "Stealth", "Fear"}
DOOR_RE = re.compile(r"\[(?P<t>[\d-]+ [\d:.]+)\].*DoorPolicy: id=(?P<id>\d+) pos=\((?P<x>[-\d.]+),(?P<y>[-\d.]+),"
                     r"(?P<z>[-\d.]+)\) recheck=(?P<re>\w+) .*impassable=(?P<imp>\w+) otherWayIn=(?P<other>\w+) "
                     r"decision=(?P<dec>.*)$")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return rows


def door_decisions(since: str) -> list[dict]:
    out = []
    for log in sorted(NATIVE_LOGS.glob("neonascendancy-*.log")):
        for line in log.read_text(encoding="utf-8", errors="replace").splitlines():
            m = DOOR_RE.search(line)
            if m and m["t"] >= since:
                out.append({"id": m["id"], "pos": (float(m["x"]), float(m["y"]), float(m["z"])),
                            "recheck": m["re"] == "true", "impassable": m["imp"] == "true",
                            "other": m["other"] == "true", "decision": m["dec"].strip()})
    return out


def dist(a, b) -> float:
    return sum((a[i] - b[i]) ** 2 for i in range(3)) ** 0.5


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--since", default="", help="ignore entries before this time")
    a = ap.parse_args()

    stops = [r for r in read_jsonl(PROBE / "tour.log") if r.get("event") == "stop" and r.get("time", "") >= a.since]
    notes = [r for r in read_jsonl(PROBE / "notes.log") if r.get("time", "") >= a.since]
    doors = door_decisions(a.since)
    latest: dict[str, dict] = {}
    for s in stops:
        latest[s["code"]] = s  # the last visit of each stop wins

    notes_by: dict[str, list[dict]] = defaultdict(list)
    for n in notes:
        notes_by[n.get("stop") or "?"].append(n)

    lines = ["# Venue tour report", "",
             f"{len(latest)} stops toured, {len(notes)} notes, {len(doors)} door decisions logged.", ""]
    summary = []
    for code, s in sorted(latest.items()):
        npcs = s.get("npcs") or []
        alive = [n for n in npcs if not n.get("dead")]
        flags = []
        bad = [n for n in alive if n.get("state") in BAD_STATES]
        hostile = [n for n in alive if "Hostile" in str(n.get("attitude"))]
        no_ws = [n for n in alive if not n.get("workspot")]
        dead = [n for n in npcs if n.get("dead")]
        if not npcs:
            flags.append("EMPTY")
        if bad:
            flags.append(f"ALERT {len(bad)}")
        if hostile:
            flags.append(f"HOSTILE {len(hostile)}")
        if alive and len(no_ws) > len(alive) / 2:
            flags.append(f"NO-WORKSPOT {len(no_ws)}/{len(alive)}")
        if dead:
            flags.append(f"DEAD {len(dead)}")
        if s.get("missing_records"):
            flags.append(f"MISSING {len(s['missing_records'])}")
        near_doors = [d for d in doors if dist(d["pos"], s["player"]) <= s.get("radius", 60)]
        stuck = [d for d in near_doors if d["recheck"] and d["impassable"] and not d["other"]
                 and "unlock" not in d["decision"] and "unseal" not in d["decision"]]
        if stuck:
            flags.append(f"DOORS {len(stuck)}")
        if notes_by.get(code):
            flags.append(f"NOTES {len(notes_by[code])}")
        summary.append((code, flags))

        lines += [f"## {code} ({s.get('kind')}, {s.get('venue')})", "",
                  f"Flags: {', '.join(flags) or 'none'}", "",
                  f"- NPCs: {len(npcs)} ({len(alive)} alive). States: "
                  + ", ".join(f"{k} {v}" for k, v in Counter(n.get('state') for n in alive).most_common())]
        if bad:
            lines.append("- Alert/combat NPCs: " + ", ".join(sorted({f"{n['record']} ({n['state']})" for n in bad}))[:600])
        if hostile:
            lines.append("- Hostile NPCs: " + ", ".join(sorted({n["record"] for n in hostile}))[:600])
        if s.get("missing_records"):
            lines.append("- Missing records: " + ", ".join(s["missing_records"])[:600])
        if near_doors:
            lines.append("- Door decisions: " + ", ".join(f"{k} {v}" for k, v in
                                                     Counter(d["decision"] for d in near_doors).most_common()))
        for n in notes_by.get(code, []):
            lines.append(f"- Note ({n.get('time')}): {n.get('text')}")
        lines.append("")

    flagged = [(c, f) for c, f in summary if f]
    lines[4:4] = ["## Summary", ""] + [f"- **{c}**: {', '.join(f)}" for c, f in flagged] + [""]
    stray = notes_by.get("?", [])
    if stray:
        lines += ["## Notes away from any stop", ""] + [f"- ({n.get('time')}) at {n.get('pos')}: {n.get('text')}"
                                                       for n in stray]
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(latest)} stops, {len(flagged)} flagged -> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
