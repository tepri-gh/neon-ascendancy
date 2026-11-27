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
  PROBLEMS     checklist items the owner marked Problem
  UNCHECKED    checklist items left unmarked when the checklist was saved
  STUCK        (sweep) doors or lifts the policy or an override covers that
               still stop the player: disabled, unpowered, sealed, locked
               with no way in, or one-sided
  BLOCKED-UNSCOPED  (sweep) the same for doors outside the policy's scope
  DUPLICATE    (sweep) two devices of one kind within 0.75 m (a doubled
               prefab or variant)

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
ROOT = Path(__file__).resolve().parents[1]
NATIVE_LOGS = GAME / "red4ext" / "logs"
DEFAULT_OUT = Path.home() / ".cache" / "neon-ascendancy" / "extracts" / "venues" / "tour-report.md"
BAD_STATES = {"Alerted", "Combat", "Stealth", "Fear"}
DOOR_RE = re.compile(r"\[(?P<t>[\d-]+ [\d:.]+)\].*DoorPolicy: id=(?P<id>\d+) pos=\((?P<x>[-\d.]+),(?P<y>[-\d.]+),"
                     r"(?P<z>[-\d.]+)\) recheck=(?P<re>\w+) .*impassable=(?P<imp>\w+) otherWayIn=(?P<other>\w+) "
                     r".*?decision=(?P<dec>.*)$")
OVERRIDES = ROOT / "data" / "venues" / "door_overrides.json"
USABLE_SIDES = {"INTERACTIVE", "AUTOMATIC", "PHYSICAL"}
# Two devices of one kind closer than this are a doubled prefab or variant.
DUPLICATE_M = 0.75


def door_problems(d: dict) -> list[str]:
    """Why a swept door would stop the player, from its raw state (empty when
    it opens, or has an in-world way through)."""
    out = []
    if d.get("disabled"):
        out.append("disabled")
    if not d.get("powered"):
        out.append("unpowered")
    if d.get("sealed"):
        out.append("sealed")
    # A lift door stays locked on every floor the car is not at; that is normal.
    if d.get("locked") and not d.get("lift") and not (d.get("auth_valid") or d.get("skill") or d.get("hack")):
        out.append("locked, no way in")
    sides = {d.get("side1"), d.get("side2")}
    if not d.get("shutter") and len(sides & USABLE_SIDES) == 1 and len(sides) == 2:
        out.append(f"one-sided ({d.get('side1')}/{d.get('side2')})")
    return out


def device_id(d: dict) -> str:
    return str(d.get("id", "")).removesuffix("ULL")


def duplicates(devices: list[dict]) -> list[tuple[dict, dict]]:
    pairs = []
    for i, a in enumerate(devices):
        for b in devices[i + 1:]:
            if a["kind"] == b["kind"] and dist(a["pos"], b["pos"]) < DUPLICATE_M:
                pairs.append((a, b))
    return pairs


def dist(a, b) -> float:
    return sum((a[i] - b[i]) ** 2 for i in range(3)) ** 0.5


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




def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--since", default="", help="ignore entries before this time")
    a = ap.parse_args()

    stops = [r for r in read_jsonl(PROBE / "tour.log") if r.get("event") == "stop" and r.get("time", "") >= a.since]
    notes = [r for r in read_jsonl(PROBE / "notes.log") if r.get("time", "") >= a.since]
    doors = door_decisions(a.since)
    in_policy = {d["id"] for d in doors}
    overridden = ({str(d["id"]) for d in json.loads(OVERRIDES.read_text(encoding="utf-8"))["doors"]}
                  if OVERRIDES.exists() else set())
    fix_rows: list[str] = []
    latest: dict[str, dict] = {}
    for s in stops:
        latest[s["code"]] = s  # the last visit of each stop wins

    checks: dict[str, dict] = {}
    for r in read_jsonl(PROBE / "tour.log"):
        if r.get("event") == "checklist" and r.get("time", "") >= a.since:
            checks[r["code"]] = r  # the last saved checklist of each venue wins
    for code, c in checks.items():
        # A checklist saved while walking, without a tour scan of that stop.
        latest.setdefault(code, {"code": code, "venue": c.get("venue"), "kind": "walk", "player": c["player"],
                                 "radius": 60, "npcs": None})

    notes_by: dict[str, list[dict]] = defaultdict(list)
    for n in notes:
        notes_by[n.get("stop") or "?"].append(n)

    lines = ["# Venue tour report", "",
             f"{len(latest)} stops toured, {len(notes)} notes, {len(doors)} door decisions logged.", ""]
    summary = []
    for code, s in sorted(latest.items()):
        scanned = s.get("npcs") is not None
        npcs = s.get("npcs") or []
        alive = [n for n in npcs if not n.get("dead")]
        flags = []
        items = (checks.get(code) or {}).get("items") or []
        problems = [i for i in items if i.get("mark") == "problem"]
        unchecked = [i for i in items if i.get("mark") == "unchecked"]
        if problems:
            flags.append(f"PROBLEMS {len(problems)}")
        if unchecked:
            flags.append(f"UNCHECKED {len(unchecked)}")
        bad = [n for n in alive if n.get("state") in BAD_STATES]
        hostile = [n for n in alive if "Hostile" in str(n.get("attitude"))]
        no_ws = [n for n in alive if not n.get("workspot")]
        dead = [n for n in npcs if n.get("dead")]
        if scanned and not npcs:
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
        devices = s.get("devices")
        stuck_dev: list[tuple[dict, list[str]]] = []
        dups: list[tuple[dict, dict]] = []
        if devices is not None:
            for dv in devices:
                if dv["kind"] == "Door":
                    why = door_problems(dv)
                    if why:
                        stuck_dev.append((dv, why))
                elif dv.get("disabled") or not dv.get("powered"):
                    stuck_dev.append((dv, ["disabled" if dv.get("disabled") else "unpowered"]))
            dups = duplicates(devices)
            scoped = [x for x in stuck_dev if device_id(x[0]) in in_policy | overridden]
            if scoped:
                flags.append(f"STUCK {len(scoped)}")
            if len(stuck_dev) > len(scoped):
                flags.append(f"BLOCKED-UNSCOPED {len(stuck_dev) - len(scoped)}")
            if dups:
                flags.append(f"DUPLICATE {len(dups)}")
            for dv, why in stuck_dev:
                scope = "override" if device_id(dv) in overridden else ("policy" if device_id(dv) in in_policy else "unscoped")
                fix_rows.append(f"| {code} | {dv['kind']} | {device_id(dv)} | {dv.get('app')} | "
                                f"({dv['pos'][0]:.1f}, {dv['pos'][1]:.1f}, {dv['pos'][2]:.1f}) | {scope} | {', '.join(why)} |")
            for x, y in dups:
                fix_rows.append(f"| {code} | {x['kind']} x2 | {device_id(x)} + {device_id(y)} | {x.get('app')} | "
                                f"({x['pos'][0]:.1f}, {x['pos'][1]:.1f}, {x['pos'][2]:.1f}) | - | duplicate |")
        if notes_by.get(code):
            flags.append(f"NOTES {len(notes_by[code])}")
        summary.append((code, flags))

        lines += [f"## {code} ({s.get('kind')}, {s.get('venue')})", "",
                  f"Flags: {', '.join(flags) or 'none'}", "",
                  (f"- NPCs: {len(npcs)} ({len(alive)} alive). States: " if scanned else "- NPCs: not scanned (checklist saved while walking)")
                  + ", ".join(f"{k} {v}" for k, v in Counter(n.get('state') for n in alive).most_common())]
        if bad:
            lines.append("- Alert/combat NPCs: " + ", ".join(sorted({f"{n['record']} ({n['state']})" for n in bad}))[:600])
        if hostile:
            lines.append("- Hostile NPCs: " + ", ".join(sorted({n["record"] for n in hostile}))[:600])
        if s.get("missing_records"):
            lines.append("- Missing records: " + ", ".join(s["missing_records"])[:600])
        if devices is not None:
            lines.append(f"- Swept devices: {len(devices)} ("
                         + ", ".join(f"{k} {v}" for k, v in Counter(dv["kind"] for dv in devices).most_common())
                         + f"); blocked {len(stuck_dev)}, duplicates {len(dups)}")
        if near_doors:
            lines.append("- Door decisions: " + ", ".join(f"{k} {v}" for k, v in
                                                     Counter(d["decision"] for d in near_doors).most_common()))
        if items:
            lines.append(f"- Checklist: {len(items) - len(problems) - len(unchecked)} OK, {len(problems)} problem, "
                         f"{len(unchecked)} unchecked")
            lines += [f"  - PROBLEM: {i['label']}" for i in problems]
            lines += [f"  - unchecked: {i['label']}" for i in unchecked]
        for n in notes_by.get(code, []):
            lines.append(f"- Note ({n.get('time')}): {n.get('text')}")
        lines.append("")

    flagged = [(c, f) for c, f in summary if f]
    lines[4:4] = ["## Summary", ""] + [f"- **{c}**: {', '.join(f)}" for c, f in flagged] + [""]
    if fix_rows:
        lines += ["## Sweep: devices that stop the player", "",
                  "scope: `policy` = the door policy acts on it, `override` = owner override, "
                  "`unscoped` = neither (often set dressing that opens onto nothing; check the venue's own doors).", "",
                  "| Stop | Kind | Id | Appearance | Position | Scope | Why |", "| --- | --- | --- | --- | --- | --- | --- |"]
        lines += fix_rows + [""]
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
