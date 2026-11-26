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
  approve VENUE...   turn checked proposals into venue entries under
                     data/venues/approved/ (the builder loads them)
  tour-stops         regenerate tools/probes/tour_stops.json, the dev tour's
                     stops (every hand-built and approved venue)
  door-scope         regenerate src/.../World/DoorScope.reds, the quest-driven
                     doors the runtime door policy may act on

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
import math
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
BAD_PHASE_WORDS = re.compile(r"(hostile|combat|^scene|_scene|cin_|interrogat|after_|ambush|chase|dead|death|wounded|_cover|cover_)", re.I)


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


def kept_phase_set(venues_dir: Path) -> set[str]:
    """Kept vanilla phases plus every child phase they run (phase nodes'
    phaseResource), transitively."""
    spec = json.loads((CLEAN / "clean_slate_spec.json").read_text(encoding="utf-8"))
    children: dict[str, list[str]] = {}
    for line in (venues_dir / "phases.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        children[r["phase"]] = r.get("open_child_phases") or []
    todo = [d["depot_path"].replace("\\", "/") for d in spec["questphase"]["kept_depot_phases"]]
    todo += [p.replace("\\", "/") for p in spec["questphase"].get("inline_phase_depot_refs") or []]
    todo += ["ep1/quest/ep1.questphase"]  # auto-merged by the engine (ep1.gamedef)
    kept: set[str] = set()
    while todo:
        ph = todo.pop()
        if ph in kept:
            continue
        kept.add(ph)
        # The PL campaign stays dormant (q005_done / ep1_active never set).
        todo += [c for c in children.get(ph, []) if not c.startswith("ep1/quest/main_quests/")]
    return kept


def kept_vanilla_activations(venues_dir: Path) -> dict[tuple[str, str, str], str]:
    """(ref, entry, phase) spawn-set and community activations kept vanilla phases make."""
    kept = kept_phase_set(venues_dir)
    out: dict[tuple[str, str, str], str] = {}
    for line in (venues_dir / "phases.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if r["phase"] in kept:
            for it in (r.get("spawn_sets") or []) + (r.get("communities") or []):
                if it.get("action") == "Activate" and not it.get("gated"):
                    out[(it.get("ref"), it.get("entry"), it.get("phase"))] = r["phase"]
    return out


def kept_vanilla_prefabs(venues_dir: Path) -> dict[str, str]:
    kept = kept_phase_set(venues_dir)
    out: dict[str, str] = {}
    for line in (venues_dir / "phases.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if r["phase"] in kept:
            for p in r.get("prefabs") or []:
                out[p] = r["phase"]
            for p in r.get("instance_prefabs") or []:
                out.setdefault(p, "instance:" + r["phase"])
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
              acts: dict[tuple[str, str, str], str],
              kept_acts: dict[tuple[str, str, str], str] | None = None) -> tuple[list[str], list[str]]:
    kept_acts = kept_acts or {}
    errs: list[str] = []
    warns: list[str] = []

    def short_ok(ref: str, where: str) -> None:
        if ref and UNTAGGED_SHORT.match(ref):
            errs.append(f"{where}: untagged '#' ref {ref} needs its full $/ path (rule 3)")

    if prop.get("venue") != vn:
        errs.append(f"venue field {prop.get('venue')!r} != {vn}")

    if "tour_stop" in prop:
        stop = prop["tour_stop"]
        pos = stop.get("position") if isinstance(stop, dict) else None
        source = stop.get("source") if isinstance(stop, dict) else None
        if not isinstance(pos, list) or len(pos) != 3 or not all(
            type(axis) is int or (type(axis) is float and math.isfinite(axis)) for axis in pos
        ):
            errs.append("tour_stop.position must contain three finite coordinates")
        if not isinstance(source, str) or not source.strip():
            errs.append("tour_stop.source must identify the vanilla node and sector")

    for p in prop.get("prefabs") or []:
        ref = p.get("ref", "")
        short_ok(ref, "prefab")
        if not any(ref == q["path"] or q["path"].endswith("/" + ref) for q in v["prefabs"]):
            errs.append(f"prefab {ref}: not a quest prefab of this venue (use input.json 'prefabs')")
        for k, owner in kept.items():
            if ref == k or k.endswith("/" + ref) or ref.endswith("/" + k):
                # instance_prefabs only lists phase nodes the clean slate can
                # reach; gated ones (behind q000_done etc.) never instantiate.
                errs.append(f"prefab {ref}: kept vanilla phase {owner.removeprefix('instance:')} already "
                            f"instantiates it in the clean slate (rule 2)")
        if ref in layers:
            errs.append(f"prefab {ref}: already used by {layers[ref]} (rule 2)")

    opts = v.get("community_options") or []
    for c in prop.get("communities") or []:
        sp, en, ph = c.get("spawner", ""), c.get("entry_name", ""), c.get("phase_name", "")
        short_ok(sp, "community")
        if c.get("action", "Activate") == "Deactivate":
            # Removing an entry (a post-quest crowd, an alert squad) is what
            # rule 9 wants, so only the entry itself must exist.
            known = (en == "None" and ph == "None" and any(ref_matches(sp, e) for e in v["communities"])) or any(
                o["entry"] == en and o["phase"] == ph and ref_matches(sp, o) for o in opts)
            if not known:
                errs.append(f"community {sp} {en}/{ph}: Deactivate of an entry phase the catalogue does not know")
            continue
        if en == "None" and ph == "None":
            hits = [e for e in v["communities"] if e.get("whole_community") and ref_matches(sp, e)]
            if not hits:
                errs.append(f"community {sp} whole-community: vanilla never activates it whole")
            elif any(e.get("posture") in BAD_POSTURES for e in hits):
                errs.append(f"community {sp} whole-community: posture {hits[0].get('posture')}")
        else:
            hits = [o for o in opts if o["entry"] == en and o["phase"] == ph and ref_matches(sp, o)]
            vanilla_act = any("Activate" in (e.get("actions") or []) and not e.get("venue_inferred") and e.get("entry") == en and e.get("phase") == ph
                              and ref_matches(sp, e) for e in v["communities"])
            if not hits and vanilla_act:
                # The spawner's registry did not resolve (no options), but a
                # vanilla phase activates exactly this entry phase here.
                if not c.get("needs_tour_check"):
                    errs.append(f"community {sp} {en}/{ph}: vanilla activates it but the catalogue has no posture for "
                                f"it; set needs_tour_check")
                else:
                    warns.append(f"community {sp} {en}/{ph}: posture unknown (no catalogue options); vanilla "
                                 f"activates this entry phase here")
            elif not hits:
                errs.append(f"community {sp} {en}/{ph}: no such entry phase in the catalogue")
            else:
                pos = hits[0]["posture"]
                if pos in BAD_POSTURES or pos.startswith("mixed") and "relaxed" not in pos:
                    errs.append(f"community {sp} {en}/{ph}: posture {pos} (rule 9)")
                if pos == "unknown" and not c.get("needs_tour_check"):
                    warns.append(f"community {sp} {en}/{ph}: posture unknown; set needs_tour_check")
            if BAD_PHASE_WORDS.search(ph):
                warns.append(f"community {sp} {en}/{ph}: phase name looks like a quest scene (rule 10)")
        if (sp, en, ph) in kept_acts:
            warns.append(f"community {sp} {en}/{ph}: kept vanilla phase {kept_acts[(sp, en, ph)]} already activates it "
                         f"in the clean slate (re-activation is harmless but redundant)")
        elif en != "None" and (sp, "None", "None") in kept_acts:
            warns.append(f"community {sp} {en}/{ph}: kept vanilla phase {kept_acts[(sp, 'None', 'None')]} already "
                         f"activates the whole community; this entry only matters if {ph} is not its initial phase")
        owner = acts.get((sp, en, ph)) or acts.get((sp, "None", "None"))
        if owner:
            errs.append(f"community {sp} {en}/{ph}: already activated by {owner}")

    for s in prop.get("spawn_sets") or []:
        ref, en, ph = s.get("reference", ""), s.get("entry_name", ""), s.get("phase_name", "")
        short_ok(ref, "spawn set")
        same = [x for x in v["spawn_sets"] if ref_matches(ref, x) and x.get("entry") == en and x.get("phase") == ph]
        if not same:
            errs.append(f"spawn set {ref} {en}/{ph}: vanilla never uses this")
        elif not any(x.get("action") == "Activate" for x in same) and not s.get("needs_tour_check"):
            warns.append(f"spawn set {ref} {en}/{ph}: vanilla only deactivates it; set needs_tour_check")
        if ref in layers:
            errs.append(f"spawn set {ref}: already placed by {layers[ref]}")
        if (ref, en, ph) in kept_acts:
            errs.append(f"spawn set {ref} {en}/{ph}: kept vanilla phase {kept_acts[(ref, en, ph)]} already activates it")
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
    if prop.get("timeline_verdict") != "exclude" and is_empty(prop):
        warns.append("nothing to restore: approve will skip it (the builder rejects an empty venue); the lead agent "
                     "turns its open questions into data/venues/tour_checks.json entries")

    anc = (prop.get("proximity_anchor") or {}).get("ref", "")
    short_ok(anc, "anchor")
    if not anc:
        errs.append("proximity_anchor missing")
    elif "_ws_" in anc or anc.startswith("#ws_"):
        errs.append(f"proximity anchor {anc} looks like a workspot (rule 8)")
    elif not any(ref_matches(anc, x) for x in devs) and not any(anc == c["path"] for c in v.get("anchor_candidates") or []):
        warns.append(f"proximity anchor {anc}: not a device vanilla drives here; confirm it is a device")

    return errs, warns


def cmd_check(a: argparse.Namespace) -> int:
    cat = load_catalog(a.venues)
    layers = layer_refs()
    kept = kept_vanilla_prefabs(a.venues)
    acts = layer_activations()
    kept_acts = kept_vanilla_activations(a.venues)
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
        errs, warns = check_one(vn, prop, cat[vn], layers, kept, acts, kept_acts)
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


# ---------------------------------------------------------------- approve

APPROVED = ROOT / "data" / "venues" / "approved"


def to_venue_entry(vn: str, prop: dict, within: float) -> dict:
    """A checked proposal as a venue_phases.json venue entry (builder schema)."""
    code = vn[4:] if vn.startswith("loc_") else vn
    entry: dict[str, Any] = {
        "code": code,
        "display_name": prop.get("display_name") or vn,
        "why": prop.get("summary", ""),
        "source": {"proposal": f"research/{vn}/proposal.json", "confidence": prop.get("confidence"),
                   "open_questions": prop.get("open_questions") or []},
        "prefabs": [p["ref"] for p in prop.get("prefabs") or []],
        "communities": [{"spawner": c["spawner"], "entry_name": c["entry_name"], "phase_name": c["phase_name"],
                         "action": c.get("action", "Activate"), "why": c.get("why", ""),
                         **({"needs_tour_check": True} if c.get("needs_tour_check") else {})}
                        for c in prop.get("communities") or []],
        "spawn_sets": [{"action": s.get("action", "Activate"), "reference": s["reference"],
                        "entry_name": s["entry_name"], "phase_name": s["phase_name"], "why": s.get("why", ""),
                        **({"needs_tour_check": True} if s.get("needs_tour_check") else {})}
                       for s in prop.get("spawn_sets") or []],
        "variant_toggles": [{"prefab": t["prefab"], "states": t["states"], "why": t.get("why", "")}
                            for t in prop.get("variant_toggles") or []],
        "doors": [],
        "door_exclusions": prop.get("door_exclusions") or [],
    }
    if not entry["prefabs"]:
        entry["deferred_prefab_owner"] = "world streaming (the chosen people need no quest prefab)"
    if "tour_stop" in prop:
        entry["tour_stop"] = prop["tour_stop"]
    anchor = (prop.get("proximity_anchor") or {}).get("ref")
    if anchor:
        entry["proximity_wait"] = {"ref": anchor, "within": within,
                                   "why": (prop.get("proximity_anchor") or {}).get("why", "")}
    return entry


def hand_built_codes() -> set[str]:
    spec = json.loads((CLEAN / "venue_phases.json").read_text(encoding="utf-8"))
    return {v["code"] for v in spec["venues"]}


def strip_failing(vn: str, prop: dict, v: dict, layers: dict[str, str], kept: dict[str, str],
                  acts: dict[tuple[str, str, str], str],
                  kept_acts: dict[tuple[str, str, str], str]) -> tuple[dict, list[str]]:
    """Drop each item the checker rejects on its own (overlaps with hand-built
    venues or other layers, invented entries) and the door actions the runtime
    policy now owns. Keeps every addition that passes. For merging research
    into venues that already have a hand-built entry."""
    out = {**prop, "doors": []}
    dropped = [f"door action {d.get('ref')} {d.get('action')}" for d in prop.get("doors") or []]
    # Pilot agents wrote '*' for "the whole community". Use the real
    # whole-community form when vanilla activates it that way; otherwise
    # expand to each entry's relaxed phase (vanilla-activated phases first).
    comms = []
    for c in prop.get("communities") or []:
        if "*" not in (c.get("entry_name"), c.get("phase_name")):
            comms.append(c)
            continue
        sp = c.get("spawner", "")
        if any(e.get("whole_community") and ref_matches(sp, e) for e in v["communities"]):
            comms.append({**c, "entry_name": "None", "phase_name": "None"})
            continue
        best: dict[str, dict] = {}
        for o in v.get("community_options") or []:
            if not ref_matches(sp, o) or o["posture"] != "relaxed":
                continue
            cur = best.get(o["entry"])
            if cur is None or (o["activated"] and not cur["activated"]):
                best[o["entry"]] = o
        comms += [{**c, "entry_name": o["entry"], "phase_name": o["phase"],
                   "why": (c.get("why") or "") + " (expanded from '*' to a relaxed phase)"} for o in best.values()]
    prop = {**prop, "communities": comms}
    base = {"venue": vn, "proximity_anchor": prop.get("proximity_anchor")}
    for key in ("prefabs", "communities", "spawn_sets", "variant_toggles"):
        keep = []
        for it in prop.get(key) or []:
            errs, _w = check_one(vn, {**base, key: [it]}, v, layers, kept, acts, kept_acts)
            errs = [e for e in errs if not e.startswith(("proximity", "venue field"))]
            if errs:
                dropped.append(f"{key}: {errs[0]}")
            else:
                keep.append(it)
        out[key] = keep
    out.pop("doors")
    return out, dropped


def is_empty(prop: dict) -> bool:
    return not any(prop.get(k) for k in ("prefabs", "communities", "spawn_sets", "variant_toggles"))


def cmd_approve(a: argparse.Namespace) -> int:
    cat = load_catalog(a.venues)
    layers, kept, acts = layer_refs(), kept_vanilla_prefabs(a.venues), layer_activations()
    kept_acts = kept_vanilla_activations(a.venues)
    APPROVED.mkdir(parents=True, exist_ok=True)
    bad = 0
    for vn in a.names:
        prop = json.loads((a.venues / "research" / vn / "proposal.json").read_text(encoding="utf-8"))
        if prop.get("timeline_verdict") == "exclude":
            print(f"{vn}: timeline_verdict exclude; add it to data/venues/triage_overrides.json instead")
            bad += 1
            continue
        if is_empty(prop):
            print(f"{vn}: nothing to restore; not approved (add a data/venues/tour_checks.json entry for its open questions)")
            bad += 1
            continue
        dropped: list[str] = []
        if a.strip:
            prop, dropped = strip_failing(vn, prop, cat[vn], layers, kept, acts, kept_acts)
        errs, _w = check_one(vn, prop, cat[vn], layers, kept, acts, kept_acts)
        if errs:
            print(f"{vn}: not approved, {len(errs)} checker errors (run check)")
            for e in errs:
                print(f"  ERROR {e}")
            bad += 1
            continue
        entry = to_venue_entry(vn, prop, a.within)
        if entry["code"] in hand_built_codes():
            # Additions to a hand-built venue run as their own phase beside it.
            entry["code"] += "_additions"
        if dropped:
            entry["source"]["stripped"] = dropped
        out = APPROVED / f"{vn}.json"
        out.write_text(json.dumps(entry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{vn}: approved -> {out.relative_to(ROOT)}" + (f" ({len(dropped)} items stripped)" if dropped else ""))
    return 1 if bad else 0


# ---------------------------------------------------------------- door scope

SCOPE_OUT = ROOT / "src" / "r6" / "scripts" / "NeonAscendancy" / "World" / "DoorScope.reds"


def fnv1a64(path: str) -> int:
    h = 0xCBF29CE484222325
    for b in path.replace("#", "").encode():
        h ^= b
        h = (h * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return h


def cmd_door_scope(a: argparse.Namespace) -> int:
    """Doors the runtime door policy may act on: every DoorControllerPS a
    vanilla quest phase drives, resolved to a full path, outside excluded and
    deferred venues, minus door_exclusions from proposals. Quest-driven doors
    lead somewhere real; set-dressing doors often open onto nothing."""
    cat = load_catalog(a.venues)
    excluded: dict[str, str] = {}
    for ap in sorted(APPROVED.glob("*.json")):
        for d in json.loads(ap.read_text(encoding="utf-8")).get("door_exclusions") or []:
            excluded[d.get("ref", "")] = ap.stem
    for pp in sorted((a.venues / "research").glob("*/proposal.json")):
        try:
            prop = json.loads(pp.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        for d in prop.get("door_exclusions") or []:
            excluded[d.get("ref", "")] = pp.parent.name
    paths: set[str] = set()
    for v in cat.values():
        if v["tier"] in ("excluded", "deferred"):
            continue
        for d in v["devices"]:
            if d.get("controller") != "DoorControllerPS" or not d.get("path") or d.get("venue_inferred"):
                continue
            if d.get("ref") in excluded or d["path"] in excluded:
                continue
            paths.add(d["path"])
    hashes = sorted({fnv1a64(p) for p in paths})
    # Laid out exactly as tools/format-redscript.sh leaves it, so regenerating
    # never makes the format check fail.
    lines = [
        "module NeonAscendancy.World",
        "",
        "// GENERATED by tools/venue-proposals.py door-scope. Do not edit.",
        "// Doors the runtime door policy may act on (docs/venue-playbook.md rule 12):",
        f"// {len(hashes)} DoorControllerPS nodes that vanilla quest phases drive, as",
        "// FNV-1a 64 hashes of their full node paths, outside excluded/deferred",
        "// venues and minus proposal door_exclusions.",
        "public func NeonAscendancy_DoorScopeHashes() -> array<Uint64> {",
        "  return [",
    ]
    lines += [f"    {h}ul{',' if i + 1 < len(hashes) else ''}" for i, h in enumerate(hashes)]
    lines += ["  ];", "}", "", ""]
    SCOPE_OUT.parent.mkdir(parents=True, exist_ok=True)
    SCOPE_OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"door scope: {len(hashes)} doors ({len(excluded)} excluded refs) -> {SCOPE_OUT.relative_to(ROOT)}")
    return 0


# ---------------------------------------------------------------- tour stops

TOUR_OUT = ROOT / "tools" / "probes" / "tour_stops.json"
# Owner-facing checks that belong to no venue entry (an excluded venue's
# leftovers, a cross-venue system). Each names the stop it is shown at.
TOUR_CHECKS = ROOT / "data" / "venues" / "tour_checks.json"
# Asked at every stop, before the venue's own items.
BASE_CHECKS = [
    ("Normal business", "The place looks like an ordinary day: no quest dressing, blood, debris or crime scene."),
    ("People at their posts", "The people are there and doing their routine; nobody alert, hostile or in a combat stance."),
    ("You can get in", "Doors, gates and lifts you would expect to use work, or there is an in-world way through."),
]


def _check_item(text: str, source: str) -> dict[str, str]:
    """One checklist line: a short label for the list, the full text behind it."""
    first = re.split(r"(?<=[.?!])\s", text.strip(), maxsplit=1)[0]
    label = first if len(first) <= 150 else first[:147].rstrip() + "..."
    return {"label": label, "detail": text.strip(), "source": source}


def tour_checklist(e: dict) -> list[dict[str, str]]:
    """What the owner should look at at this venue on the tour."""
    items = [{"label": a, "detail": b, "source": "base"} for a, b in BASE_CHECKS]
    for t in e.get("tour_checks") or []:
        items.append(_check_item(t, "venue"))
    unsure: dict[str, list[str]] = {}
    for c in e.get("communities") or []:
        if c.get("needs_tour_check") and c.get("action", "Activate") == "Activate":
            entry = "the whole community" if c["entry_name"] == "None" else f"{c['entry_name']}/{c['phase_name']}"
            unsure.setdefault(c["spawner"], []).append(entry)
    for sp, entries in unsure.items():
        items.append({"label": f"Calm and on post: {sp} ({len(entries)} unmapped)",
                      "detail": "No spot map, so their posture is unknown; confirm they stand or work calmly, "
                                "not alert or in combat: " + ", ".join(entries) + ".",
                      "source": "community"})
    for q in (e.get("source") or {}).get("open_questions") or []:
        items.append(_check_item(q, "open question"))
    return items


def _median(vals: list[float]) -> float:
    v = sorted(vals)
    return v[len(v) // 2]


def cmd_tour_stops(a: argparse.Namespace) -> int:
    """Write the dev tour's stop list (tools/probes/tour_stops.json): every
    hand-built and approved venue with a position (median of its people's
    spots), a scan radius and the character records the tour should find."""
    cat = load_catalog(a.venues)
    spec = json.loads((CLEAN / "venue_phases.json").read_text(encoding="utf-8"))
    entries = [("hand-built", None, v) for v in spec["venues"]]
    entries += [("approved", p.stem, json.loads(p.read_text(encoding="utf-8")))
                for p in sorted(APPROVED.glob("*.json"))]
    stops = []
    for kind, best, e in entries:
        if best not in cat:
            # Hand-built entries have no catalogue key. Match their refs.
            refs = set(REF.findall(json.dumps(e)))
            best, score = None, 0
            for vn, v in cat.items():
                items = v["prefabs"] + v["communities"] + v["spawn_sets"] + v["devices"]
                n = sum(1 for it in items if it.get("ref") in refs or it.get("path") in refs)
                if n > score:
                    best, score = vn, n
        if not best:
            continue
        v = cat[best]
        want = {(c.get("spawner"), c.get("entry_name"), c.get("phase_name")) for c in e.get("communities") or []}
        pts, records = [], set()
        for o in v.get("community_options") or []:
            hit = any(ref_matches(sp, o) and (en in ("None", o["entry"])) and (ph in ("None", o["phase"]))
                      for sp, en, ph in want)
            if hit and o.get("spot_pos"):
                pts.append(o["spot_pos"])
            if hit and o.get("record") and o["role"] != "vehicle":
                records.add(o["record"])
        tour_stop = e.get("tour_stop")
        if tour_stop:
            pts = [tour_stop["position"]]
        if not pts:
            pts = [c["spot_pos"] for c in v["communities"] if c.get("spot_pos")]
        if not pts:
            # No mapped spots: the anchor device, else any device vanilla drives here.
            anc = (e.get("proximity_wait") or {}).get("ref")
            devs = [d for d in v["devices"] if d.get("pos")]
            pts = [d["pos"] for d in devs if ref_matches(anc, d)] or [d["pos"] for d in devs if not d.get("venue_inferred")]
        if not pts:
            print(f"  no position for {e['code']} ({best})")
            continue
        pos = [round(_median([p[i] for p in pts]), 2) for i in range(3)]
        spread = max(((p[0] - pos[0]) ** 2 + (p[1] - pos[1]) ** 2) ** 0.5 for p in pts)
        stops.append({"code": e["code"], "name": e.get("display_name") or e["code"], "kind": kind,
                      "venue": best, "pos": pos, "radius": round(min(max(spread + 15.0, 40.0), 120.0), 1),
                      "expected_records": sorted(records),
                      "spawn_sets": sorted({s["reference"] for s in e.get("spawn_sets") or []}),
                      "checklist": tour_checklist(e)})
    extra = json.loads(TOUR_CHECKS.read_text(encoding="utf-8"))["checks"] if TOUR_CHECKS.exists() else []
    by_code = {st["code"]: st for st in stops}
    for x in extra:
        st = by_code.get(x["stop"])
        if st is None:
            print(f"  tour check for unknown stop {x['stop']}: {x['text'][:60]}")
            continue
        st["checklist"].append(_check_item(x["text"], "extra"))
    stops.sort(key=lambda s: (s["pos"][0] // 1000, s["pos"][1] // 1000, s["code"]))
    TOUR_OUT.write_text(json.dumps({"generated_by": "tools/venue-proposals.py tour-stops", "stops": stops},
                                   indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    # The CET probe reads the same list as a Lua table (no JSON library needed).
    def lua(v: Any) -> str:
        if isinstance(v, str):
            return json.dumps(v, ensure_ascii=False)
        if isinstance(v, bool):
            return "true" if v else "false"
        if isinstance(v, (int, float)):
            return repr(v)
        if isinstance(v, list):
            return "{" + ", ".join(lua(x) for x in v) + "}"
        if isinstance(v, dict):
            return "{" + ", ".join(f"{k} = {lua(x)}" for k, x in v.items()) + "}"
        return "nil"
    TOUR_OUT.with_suffix(".lua").write_text(
        "-- GENERATED by tools/venue-proposals.py tour-stops. Do not edit.\nreturn {\n"
        + "".join(f"  {lua(st)},\n" for st in stops) + "}\n", encoding="utf-8")
    print(f"tour stops: {len(stops)} of {len(entries)} venues -> {TOUR_OUT.relative_to(ROOT)}")
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
    sub.add_parser("door-scope")
    sub.add_parser("tour-stops")
    p = sub.add_parser("approve"); p.add_argument("names", nargs="+")
    p.add_argument("--within", type=float, default=80.0, help="proximity wait radius in metres")
    p.add_argument("--strip", action="store_true",
                   help="drop individually failing items instead of refusing (merging into hand-built venues)")
    a = ap.parse_args()
    return {"prepare": cmd_prepare, "check": cmd_check, "wave": cmd_wave, "door-scope": cmd_door_scope, "approve": cmd_approve,
            "tour-stops": cmd_tour_stops}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
