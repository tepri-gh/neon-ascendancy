#!/usr/bin/env python3
"""Prepare, check and list venue research proposals.

Venue research agents (docs/venue-playbook.md section 6) each write a
proposal.json for one catalogue venue. This tool keeps that loop honest:

  prepare VENUE...   write research/<venue>/input.json (the venue's catalogue
                     record, its vanilla phase JSONs and wiki pages)
  check [VENUE...]   validate proposals against the catalogue and the mod's
                     own layers; exit 1 on any error. With no venues, checks
                     every proposal under research/.
  wave N             print the next N untried individual-tier venues, skipping
                     ones with a research folder or a hand-built venue entry

Everything a proposal names must exist in vanilla data for that venue. The
checker also rejects choices that break the playbook's rules: alert, dead or
scene phases, untagged '#' refs, prefabs that are not quest prefabs of the
venue, prefabs and people another layer already owns, and workspot anchors.

Research data lives outside the repo (default
~/.cache/neon-ascendancy/extracts/venues); AGENTS-LOCAL.md records where.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
HOME = Path.home()
DEFAULT_VENUES = HOME / ".cache" / "neon-ascendancy" / "extracts" / "venues"
DEFAULT_PHASES = HOME / ".cache" / "neon-ascendancy" / "extracts" / "questphases" / "raw"
DEFAULT_WIKI = HOME / "Work" / "Cyberpunk" / "Walkthroughs" / "cyberpunk-fandom"
CLEAN = ROOT / "data" / "clean-slate"

UNTAGGED_SHORT = re.compile(r"^#.*_prefab[A-Z0-9]{7}$")
REF = re.compile(r"(?:#|\$/)[A-Za-z0-9_{}#/$.-]+")
BAD_POSTURES = {"alert", "dead", "scene"}
BAD_PHASE_WORDS = re.compile(r"(hostile|combat|^scene|_scene|cin_|interrogat|after_|ambush|chase|dead|death|wounded)", re.I)


def load_catalog(venues_dir: Path) -> dict[str, dict]:
    return {v["venue"]: v for v in json.loads((venues_dir / "catalog.json").read_text(encoding="utf-8"))}


def hand_built_venues(catalog: dict[str, dict]) -> set[str]:
    """Catalogue venues that share a prefab, device or community ref with a
    hand-built venue_phases.json entry."""
    refs = set(REF.findall((CLEAN / "venue_phases.json").read_text(encoding="utf-8")))
    out = set()
    for vn, v in catalog.items():
        items = v["prefabs"] + v["communities"]  # shared devices alone (e.g. a dataterm) do not make a venue hand-built
        if any(it.get("ref") in refs or it.get("path") in refs for it in items):
            out.add(vn)
    return out


def layer_refs() -> dict[str, str]:
    """Every ref another mod layer already uses -> the file that uses it."""
    out: dict[str, str] = {}
    files = [CLEAN / "cast_and_hubs.json", CLEAN / "venue_phases.json"]
    cast = json.loads((CLEAN / "cast_and_hubs.json").read_text(encoding="utf-8"))
    for key in ("tower_population_spec", "dogtown_vendors_spec"):
        p = cast.get(key)
        if isinstance(p, str):
            files.append(ROOT / p)
    for f in files:
        for r in REF.findall(f.read_text(encoding="utf-8")):
            out.setdefault(r, f.name)
    return out


def layer_activations() -> dict[tuple[str, str, str], str]:
    """(spawner, entry, phase) activations other mod layers already make."""
    out: dict[tuple[str, str, str], str] = {}
    cast = json.loads((CLEAN / "cast_and_hubs.json").read_text(encoding="utf-8"))
    for h in cast.get("world_hubs") or []:
        out[(h["spawner_reference"], h["community_entry_name"], h["community_entry_phase_name"])] = "cast_and_hubs.json"
    spec = json.loads((CLEAN / "venue_phases.json").read_text(encoding="utf-8"))
    for v in spec["venues"]:
        for c in v.get("communities") or []:
            out[(c["spawner"], c["entry_name"], c["phase_name"])] = "venue_phases.json:" + v["code"]
    return out


def kept_vanilla_prefabs(venues_dir: Path) -> dict[str, str]:
    spec = json.loads((CLEAN / "clean_slate_spec.json").read_text(encoding="utf-8"))
    kept = {d["depot_path"].replace("\\", "/") for d in spec["questphase"]["kept_depot_phases"]}
    out: dict[str, str] = {}
    for line in (venues_dir / "phases.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if r["phase"] in kept:
            for p in r.get("prefabs") or []:
                out[p] = r["phase"]
    return out


def ref_matches(ref: str, item: dict) -> bool:
    if not ref:
        return False
    full = item.get("path") or ""
    short = item.get("ref") or ""
    return ref == short or ref == full or (ref.startswith("#") and full.endswith("/" + ref))


# ---------------------------------------------------------------- prepare

def cmd_prepare(a: argparse.Namespace) -> int:
    cat = load_catalog(a.venues)
    for vn in a.names:
        if vn not in cat:
            print(f"unknown venue {vn}", file=sys.stderr)
            return 1
        v = cat[vn]
        d = a.venues / "research" / vn
        d.mkdir(parents=True, exist_ok=True)
        phases = []
        for ph in v["phases"]:
            p = a.phases / ph.split("/")[0] / (ph + ".json")
            phases.append({"phase": ph, "json": str(p), "exists": p.exists()})
        wiki = [{"title": w["title"], "path": str(a.wiki / w["file"])} for w in v["wiki"]]
        (d / "input.json").write_text(json.dumps({**v, "phase_files": phases, "wiki_files": wiki},
                                                 indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{vn}: {len(phases)} phase files, {len(wiki)} wiki pages")
    return 0


# ---------------------------------------------------------------- check

def check_one(vn: str, prop: dict, v: dict, layers: dict[str, str], kept: dict[str, str],
              acts: dict[tuple[str, str, str], str]) -> tuple[list[str], list[str]]:
    errs: list[str] = []
    warns: list[str] = []

    def short_ok(ref: str, where: str) -> None:
        if ref and UNTAGGED_SHORT.match(ref):
            errs.append(f"{where}: untagged '#' ref {ref} needs its full $/ path (rule 3)")

    if prop.get("venue") != vn:
        errs.append(f"venue field {prop.get('venue')!r} != {vn}")

    for p in prop.get("prefabs") or []:
        ref = p.get("ref", "")
        short_ok(ref, "prefab")
        if not any(ref == q["path"] or q["path"].endswith("/" + ref) for q in v["prefabs"]):
            errs.append(f"prefab {ref}: not a quest prefab of this venue (use input.json 'prefabs')")
        for k, owner in kept.items():
            if ref == k or k.endswith("/" + ref) or ref.endswith("/" + k):
                errs.append(f"prefab {ref}: already declared by kept vanilla phase {owner} (rule 2)")
        if ref in layers:
            errs.append(f"prefab {ref}: already used by {layers[ref]} (rule 2)")

    opts = v.get("community_options") or []
    for c in prop.get("communities") or []:
        sp, en, ph = c.get("spawner", ""), c.get("entry_name", ""), c.get("phase_name", "")
        short_ok(sp, "community")
        if en == "None" and ph == "None":
            hits = [e for e in v["communities"] if e.get("whole_community") and ref_matches(sp, e)]
            if not hits:
                errs.append(f"community {sp} whole-community: vanilla never activates it whole")
            elif any(e.get("posture") in BAD_POSTURES for e in hits):
                errs.append(f"community {sp} whole-community: posture {hits[0].get('posture')}")
        else:
            hits = [o for o in opts if o["entry"] == en and o["phase"] == ph and ref_matches(sp, o)]
            if not hits:
                errs.append(f"community {sp} {en}/{ph}: no such entry phase in the catalogue")
            else:
                pos = hits[0]["posture"]
                if pos in BAD_POSTURES or pos.startswith("mixed") and "relaxed" not in pos:
                    errs.append(f"community {sp} {en}/{ph}: posture {pos} (rule 9)")
                if pos == "unknown" and not c.get("needs_tour_check"):
                    warns.append(f"community {sp} {en}/{ph}: posture unknown; set needs_tour_check")
            if BAD_PHASE_WORDS.search(ph):
                warns.append(f"community {sp} {en}/{ph}: phase name looks like a quest scene (rule 10)")
        owner = acts.get((sp, en, ph)) or acts.get((sp, "None", "None"))
        if owner:
            errs.append(f"community {sp} {en}/{ph}: already activated by {owner}")

    for s in prop.get("spawn_sets") or []:
        ref, en, ph = s.get("reference", ""), s.get("entry_name", ""), s.get("phase_name", "")
        short_ok(ref, "spawn set")
        if not any(ref_matches(ref, x) and x.get("entry") == en and x.get("phase") == ph for x in v["spawn_sets"]):
            errs.append(f"spawn set {ref} {en}/{ph}: vanilla never activates this")
        if ref in layers:
            errs.append(f"spawn set {ref}: already placed by {layers[ref]}")
        if BAD_PHASE_WORDS.search(ph) and "friendly" not in ph:
            warns.append(f"spawn set {ref} {en}/{ph}: phase name looks like a quest scene")

    for t in prop.get("variant_toggles") or []:
        ref = t.get("prefab", "")
        short_ok(ref, "toggle")
        seen = [x for x in v["toggles"] if ref_matches(ref, x)]
        if not seen:
            errs.append(f"toggle {ref}: vanilla never toggles this prefab")
            continue
        names = {n for x in seen for n in (x.get("states") or {})}
        for n in t.get("states") or {}:
            if n not in names:
                errs.append(f"toggle {ref}: unknown variant {n} (known: {sorted(names)})")

    devs = v.get("devices") or []
    for d in prop.get("door_exclusions") or []:
        if not any(ref_matches(d.get("ref", ""), x) for x in devs):
            warns.append(f"door exclusion {d.get('ref')}: not a device vanilla drives at this venue")
    if prop.get("doors"):
        errs.append("doors: door actions are decided by the runtime door policy; use door_exclusions/door_notes")

    anc = (prop.get("proximity_anchor") or {}).get("ref", "")
    short_ok(anc, "anchor")
    if not anc:
        errs.append("proximity_anchor missing")
    elif "_ws_" in anc or anc.startswith("#ws_"):
        errs.append(f"proximity anchor {anc} looks like a workspot (rule 8)")
    elif not any(ref_matches(anc, x) for x in devs):
        warns.append(f"proximity anchor {anc}: not a device vanilla drives here; confirm it is a device")

    return errs, warns


def cmd_check(a: argparse.Namespace) -> int:
    cat = load_catalog(a.venues)
    layers = layer_refs()
    kept = kept_vanilla_prefabs(a.venues)
    acts = layer_activations()
    names = a.names or sorted(p.parent.name for p in (a.venues / "research").glob("*/proposal.json"))
    bad = 0
    for vn in names:
        pp = a.venues / "research" / vn / "proposal.json"
        if not pp.exists():
            print(f"{vn}: MISSING proposal.json")
            bad += 1
            continue
        try:
            prop = json.loads(pp.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"{vn}: INVALID JSON {exc}")
            bad += 1
            continue
        errs, warns = check_one(vn, prop, cat[vn], layers, kept, acts)
        status = "FAIL" if errs else "ok"
        print(f"{vn}: {status} ({len(errs)} errors, {len(warns)} warnings)")
        for e in errs:
            print(f"  ERROR {e}")
        for w in warns:
            print(f"  warn  {w}")
        bad += bool(errs)
    return 1 if bad else 0


# ---------------------------------------------------------------- wave

def cmd_wave(a: argparse.Namespace) -> int:
    cat = load_catalog(a.venues)
    done = {p.name for p in (a.venues / "research").iterdir() if p.is_dir()}
    hand = hand_built_venues(cat)
    pool = [v for v in cat.values() if v["tier"] == "individual" and v["venue"] not in done | hand]
    pool.sort(key=lambda v: (not v["wiki"], -(v["counts"]["communities"] + v["counts"]["spawn_sets"]), v["venue"]))
    for v in pool[: a.n]:
        print(v["venue"])
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--venues", type=Path, default=DEFAULT_VENUES)
    ap.add_argument("--phases", type=Path, default=DEFAULT_PHASES)
    ap.add_argument("--wiki", type=Path, default=DEFAULT_WIKI)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepare"); p.add_argument("names", nargs="+")
    p = sub.add_parser("check"); p.add_argument("names", nargs="*")
    p = sub.add_parser("wave"); p.add_argument("n", type=int)
    a = ap.parse_args()
    return {"prepare": cmd_prepare, "check": cmd_check, "wave": cmd_wave}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
