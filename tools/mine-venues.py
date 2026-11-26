#!/usr/bin/env python3
"""Mine vanilla game data into a per-venue catalogue for venue work.

See docs/venue-playbook.md (section 6). Every stage reads local
extracts, writes to OUT (default ~/.cache/neon-ascendancy/extracts/venues),
and is idempotent: re-running a stage rewrites its output, and the slow
`sectors` stage resumes from finished batches.

Stages:
  sectors      Convert every streaming sector that contains AI spots or
               devices, and record spot nodes (global id -> workspot,
               position) and node refs (path, FNV-1a hash). Slow; parallel.
  communities  Read the community registry from the always-loaded sectors:
               community id -> entries, character records, phases, and the
               spot ids of every entry phase.
  phases       Read every converted .questphase and record the venue-relevant
               items it touches: prefabs, community and spawn-set
               activations, device actions, variant toggles.
  catalog      Join the stages into catalog.json: venues (grouped by
               location prefab), their items, each community phase's
               workspots and posture, owning quests, and the wiki pages that
               match those quests.
  all          phases, communities, sectors, catalog.

Inputs (override with flags):
  --sectors    raw streaming sectors, base and EP1 (EP1 winning by path)
  --phases     converted .questphase JSON tree
  --wiki       tools/fetch-wiki-walkthroughs.py output
  --blocks     converted all.streamingblock JSONs (base and EP1)
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterator

HOME = Path.home()
CACHE = HOME / ".cache" / "neon-ascendancy"
DEFAULT_WK = CACHE / "wolvenkit-10.0.0-beta.1" / "WolvenKit.CLI"
DEFAULT_OUT = CACHE / "extracts" / "venues"
DEFAULT_SECTORS = HOME / "na-prop-scratch" / "sectors"
DEFAULT_PHASES = CACHE / "extracts" / "questphases" / "raw"
DEFAULT_WIKI = HOME / "Work" / "Cyberpunk" / "Walkthroughs" / "cyberpunk-fandom"

# CNames that appear uncompressed in a sector's name table when it holds the
# node types we care about. Sector buffers are compressed, so this is the only
# byte-level prefilter that works.
SECTOR_MARKERS = (b"worldAISpotNode", b"worldDeviceNode", b"DoorControllerPS", b"worldCompiledCommunityAreaNode")

BATCH = 150


# ---------------------------------------------------------------- helpers

def fnv1a64(path: str) -> int:
    """Engine NodeRef / static EntityID hash: FNV-1a 64 over the path, '#' skipped."""
    h = 0xCBF29CE484222325
    for b in path.replace("#", "").encode():
        h ^= b
        h = (h * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return h


def val(x: Any) -> Any:
    if isinstance(x, dict):
        if "$value" in x:
            return x["$value"]
        if "hash" in x:
            return x["hash"]
        if "Data" in x and isinstance(x["Data"], dict):
            return x["Data"]
    return x


def walk(o: Any) -> Iterator[dict]:
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)


def run_wk(wk: Path, args: list[str]) -> None:
    env = {**os.environ, "DOTNET_ROLL_FORWARD": "Major"}
    subprocess.run([str(wk), *args], check=True, env=env, stdin=subprocess.DEVNULL,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def write_jsonl(path: Path, rows: list[dict]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    tmp.replace(path)


def read_jsonl(path: Path) -> Iterator[dict]:
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


WORKSPOT_RE = re.compile(r"[A-Za-z0-9_\\/.-]+\.workspot")


def posture(workspot: str | None) -> str:
    """Classify a workspot path. 'relaxed' is safe ambient; 'alert' reads as combat-ready."""
    if not workspot:
        return "unknown"
    w = workspot.lower()
    if any(k in w for k in ("agitated", "nervous", "alert", "combat", "cover", "aim", "hostile", "cower", "panic", "fear")):
        return "alert"
    if any(k in w for k in ("dead", "corpse", "unconscious", "lying_dead", "body_")):
        return "dead"
    if "\\cutscene" in w or "\\scene" in w or "\\quest\\" in w:
        return "scene"
    return "relaxed"


_COMBAT_TOKENS = re.compile(
    r"(^|[._])(ranged\d*|melee\d*|[fh]melee\d*|grunt\d*|guard|guards|security|soldier|officer|sniper|shotgun\d*|"
    r"shotgunner|rifle|handgun|hmg|elite|enemy|enemies|gangster\d*|ganger|ncpd|police|maxtac|max_tac|bodyguard|"
    r"combat|merc|heavy|boss|katana|mantis|kanabo|lmg|smg|bouncer|enforcer|thug|cop|cops|militia)([._]|\d|$)")


def role_of(record: str | None) -> str:
    """Population role from a character record name: 'netrunner', 'combat'
    (any fighting group: guards, security, gangers, soldiers, police),
    'vehicle', or 'civilian'. Name-based; owner rule (playbook rule 17)
    ranks netrunner > combat > civilian when an area's groups are capped."""
    if not record:
        return "unknown"
    r = record.lower()
    if "netrunner" in r:
        return "netrunner"
    if r.startswith(("vehicle.", "character.vehicle")) or "_vehicle_" in r:
        return "vehicle"
    if _COMBAT_TOKENS.search(r):
        return "combat"
    return "civilian"


# ---------------------------------------------------------------- sectors

def _sector_batch(args: tuple[Path, Path, list[str], int]) -> int:
    wk, out_dir, rels, idx = args
    done = out_dir / f"batch_{idx:04d}.jsonl"
    if done.exists():
        return 0
    rows: list[dict] = []
    with tempfile.TemporaryDirectory(prefix="na-mine-") as td:
        tdp = Path(td)
        for i, (rel, src) in enumerate(rels):
            shutil.copy(src, tdp / f"{i:04d}.streamingsector")
        try:
            run_wk(wk, ["convert", "serialize", str(tdp)])
        except subprocess.CalledProcessError:
            pass  # a few sectors refuse conversion; the missing JSONs are recorded below
        for i, (rel, _src) in enumerate(rels):
            jp = tdp / f"{i:04d}.streamingsector.json"
            if not jp.exists():
                rows.append({"kind": "unconverted", "sector": rel})
                continue
            try:
                root = json.loads(jp.read_text(encoding="utf-8"))["Data"]["RootChunk"]
            except (json.JSONDecodeError, KeyError):
                rows.append({"kind": "unconverted", "sector": rel})
                continue
            for r in root.get("nodeRefs") or []:
                p = val(r)
                if isinstance(p, str) and p:
                    rows.append({"kind": "ref", "sector": rel, "path": p, "hash": str(fnv1a64(p))})
            nodes = root.get("nodes") or []
            for inst in (root.get("nodeData") or {}).get("Data") or []:
                node = val(nodes[int(inst["nodeIdx"])]) if nodes else None
                if not isinstance(node, dict):
                    continue
                t = node.get("$type", "")
                pos = (inst.get("transform") or {}).get("position") or {}
                xyz = [round(float(pos.get(k, 0)), 2) for k in ("X", "Y", "Z")]
                gid = str(val(inst.get("globalNodeId")))
                if t == "worldAISpotNode":
                    spot = val(node.get("spot")) or {}
                    m = WORKSPOT_RE.findall(json.dumps(spot).replace("\\\\", "\\"))
                    rows.append({"kind": "spot", "sector": rel, "gid": gid, "pos": xyz,
                                 "debug": val(node.get("debugName")), "spot_type": spot.get("$type"),
                                 "workspot": m[0] if m else None})
                elif t.startswith("worldCompiledCommunityAreaNode"):
                    area = val(node.get("area")) or {}
                    m: dict[str, list[str]] = {}
                    for e in area.get("entriesData") or []:
                        for ph in e.get("phasesData") or []:
                            m[f"{val(e['entryName'])}/{val(ph['entryPhaseName'])}"] = [
                                str(val(s)) for tp in ph.get("timePeriodsData") or [] for s in tp.get("spotNodeIds") or []]
                    rows.append({"kind": "area", "sector": rel, "cid": str(val(node.get("sourceObjectId"))), "spots": m})
                elif "Device" in t or "Door" in t:
                    rows.append({"kind": "device", "sector": rel, "gid": gid, "pos": xyz, "type": t,
                                 "debug": val(node.get("debugName"))})
    write_jsonl(done, rows)
    return len(rels)


def stage_sectors(a: argparse.Namespace) -> None:
    out_dir = a.out / "sectors"
    out_dir.mkdir(parents=True, exist_ok=True)
    # One single-pattern grep per marker scans 19 GB in seconds; a multi-pattern
    # grep or a Python byte search over binary data takes many minutes.
    hits: set[str] = set()
    for m in SECTOR_MARKERS:
        res = subprocess.run(["grep", "-rlaF", "--include=*.streamingsector", m.decode(), str(a.sectors)],
                             capture_output=True, text=True, env={**os.environ, "LC_ALL": "C"})
        if res.returncode > 1:
            raise RuntimeError(res.stderr)
        hits |= set(res.stdout.splitlines())
    cands: list[tuple[str, str]] = []
    for line in sorted(hits):
        p = Path(line)
        if p.name.startswith("always_loaded"):
            continue  # registry sectors; read by the communities stage
        cands.append((str(p.relative_to(a.sectors)), str(p)))
    if a.limit:
        cands = [c for c in cands if any(k in c[0] for k in a.limit)]
    print(f"sectors: {len(cands)} candidates", flush=True)
    jobs = [(a.wk, out_dir, cands[i:i + BATCH], i // BATCH) for i in range(0, len(cands), BATCH)]
    total = 0
    with cf.ProcessPoolExecutor(max_workers=a.jobs) as ex:
        for n in ex.map(_sector_batch, jobs):
            total += n
            print(f"sectors: converted {total} this run", flush=True)
    print(f"sectors: done ({len(jobs)} batches)")


# ---------------------------------------------------------------- communities

def stage_communities(a: argparse.Namespace) -> None:
    al = sorted(a.sectors.rglob("always_loaded_*.streamingsector"))
    rows: dict[str, dict] = {}
    refs: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="na-mine-al-") as td:
        tdp = Path(td)
        for i, p in enumerate(al):
            shutil.copy(p, tdp / f"{i:02d}_{p.name}")
        run_wk(a.wk, ["convert", "serialize", str(tdp)])
        for jp in sorted(tdp.glob("*.json")):
            root = json.loads(jp.read_text(encoding="utf-8"))["Data"]["RootChunk"]
            for r in root.get("nodeRefs") or []:
                p = val(r)
                if isinstance(p, str) and p:
                    refs[str(fnv1a64(p))] = p
            spots: dict[str, dict[str, list[str]]] = {}
            for o in walk(root):
                t = o.get("$type")
                if t == "worldCompiledCommunityAreaNode":
                    cid = str(val(o.get("sourceObjectId")))  # = the registry item's communityId
                    area = val(o.get("area")) or {}
                    for e in area.get("entriesData") or []:
                        en = val(e["entryName"])
                        for ph in e.get("phasesData") or []:
                            ids = [str(val(s)) for tp in ph.get("timePeriodsData") or [] for s in tp.get("spotNodeIds") or []]
                            spots.setdefault(cid, {}).setdefault(f"{en}/{val(ph['entryPhaseName'])}", []).extend(ids)
                elif t == "worldCommunityRegistryItem":
                    cid = str(val(val(o["communityId"]).get("entityId")))
                    tmpl = val(o.get("template")) or {}
                    init = {val(e["entryName"]): {"phase": val(e["initialPhaseName"]), "active": e.get("entryActiveOnStart")}
                            for e in o.get("entriesInitialState") or []}
                    entries = []
                    for e in tmpl.get("entries") or []:
                        e = val(e)
                        entries.append({
                            "name": val(e["entryName"]),
                            "record": val(e.get("characterRecordId")),
                            "phases": [val(val(p)["phaseName"]) for p in e.get("phases") or []],
                            "initial": init.get(val(e["entryName"])),
                        })
                    rows[cid] = {"id": cid, "area_type": o.get("communityAreaType"),
                                 "spawn_set": val(tmpl.get("spawnSetReference")), "entries": entries}
            for cid, m in spots.items():
                rows.setdefault(cid, {"id": cid, "entries": []}).setdefault("spots", {}).update(m)
    for cid, r in rows.items():
        r["path"] = refs.get(cid)
    (a.out).mkdir(parents=True, exist_ok=True)
    (a.out / "communities.json").write_text(json.dumps(rows, indent=0, ensure_ascii=False) + "\n", encoding="utf-8")
    named = sum(1 for r in rows.values() if r.get("path"))
    print(f"communities: {len(rows)} ({named} with a path)")


# ---------------------------------------------------------------- phases

def _is_node(o: dict) -> bool:
    t = o.get("$type", "")
    return t.startswith("quest") and t.endswith("NodeDefinition") and "sockets" in o and "id" in o


# Facts exempt from forbidden_fact_prefixes (clean_slate_spec allowed_prefixed_facts).
ALLOWED_PREFIXED: set[str] = set()


def _blocks(node: dict, forbidden: set[str], prefixes: tuple[str, ...], settable: set[str] | None = None) -> bool:
    """True when the node's fact condition can never pass in the clean slate.

    A required fact (> 0, >= 1, == 1+) that is forbidden, or (when `settable`
    is given) that nothing in the clean slate can set, keeps its default 0.
    Conditions with an OR are treated as passable."""
    cond = node.get("condition")
    if not cond:
        return False
    s = json.dumps(cond)
    if '"Or"' in s or '"OR"' in s:
        return False
    for o in walk(cond):
        if o.get("$type") != "questVarComparison_ConditionType":
            continue
        name = str(val(o.get("factName")))
        never = (name in forbidden or (name.startswith(prefixes) and name not in ALLOWED_PREFIXED)
                 or (settable is not None and name not in settable))
        if not never:
            continue
        cmp_, value = o.get("comparisonType"), o.get("value", 0)
        if (cmp_ == "Greater" and value >= 0) or (cmp_ in ("GreaterOrEqual", "Equal") and value >= 1):
            return True
    return False


def _reachable_nodes(d: dict, forbidden: set[str], prefixes: tuple[str, ...],
                     settable: set[str] | None = None) -> tuple[dict[int, dict], set[int], dict[int, int | None]]:
    """Map every graph node to whether the clean slate can reach it.

    Nodes connect through shared socket handles (WolvenKit HandleId /
    HandleRefId). Traversal starts at input nodes and stops at pause nodes,
    and at a condition node's True output, whose fact condition can never
    pass. A nested phase graph's inputs count only if its phase node does."""
    handles: dict[str, dict] = {}
    for o in walk(d):
        if "HandleId" in o and isinstance(o.get("Data"), dict):
            handles[o["HandleId"]] = o["Data"]
    nodes: dict[int, dict] = {}
    container: dict[int, int | None] = {}

    def collect(o: Any, cont: int | None) -> None:
        if isinstance(o, dict):
            if _is_node(o):
                nodes[id(o)] = o
                container[id(o)] = cont
                for k, v in o.items():
                    collect(v, id(o) if k in ("phaseGraph", "graph") else cont)
                return
            for v in o.values():
                collect(v, cont)
        elif isinstance(o, list):
            for v in o:
                collect(v, cont)

    collect(d, None)

    def hid(x: dict) -> str | None:
        return x.get("HandleId") or x.get("HandleRefId")

    sock_owner: dict[str, int] = {}
    for nid, n in nodes.items():
        for sk in n.get("sockets") or []:
            h = hid(sk)
            if h:
                sock_owner[h] = nid
    edges: dict[int, list[tuple[str, int]]] = defaultdict(list)
    for nid, n in nodes.items():
        for sk in n.get("sockets") or []:
            sd = handles.get(hid(sk) or "", {})
            if sd.get("type") != "Output":
                continue
            out_name = str(val(sd.get("name")))
            for c in sd.get("connections") or []:
                cd = handles.get(hid(c) or "", c.get("Data") if isinstance(c.get("Data"), dict) else {})
                dst = cd.get("destination") or {}
                owner = sock_owner.get(hid(dst) or "")
                if owner is not None:
                    edges[nid].append((out_name, owner))
    reach: set[int] = set()
    changed = True
    while changed:
        changed = False
        todo = [nid for nid, n in nodes.items() if n["$type"] == "questInputNodeDefinition"
                and nid not in reach and (container[nid] is None or container[nid] in reach)]
        while todo:
            nid = todo.pop()
            if nid in reach:
                continue
            reach.add(nid)
            changed = True
            n = nodes[nid]
            blocked = _blocks(n, forbidden, prefixes, settable)
            if blocked and n["$type"] == "questPauseConditionNodeDefinition":
                continue
            for out_name, dst in edges.get(nid, []):
                if blocked and out_name == "True":
                    continue
                if dst not in reach:
                    todo.append(dst)
    return nodes, reach, container


def _phase_items(path: Path, rel: str, forbidden: set[str], prefixes: tuple[str, ...],
                 settable: set[str] | None = None) -> dict:
    d = json.loads(path.read_text(encoding="utf-8"))
    nodes, reach, _cont = _reachable_nodes(d, forbidden, prefixes, settable)
    items: dict[str, list] = defaultdict(list)

    def visit(o: Any, node: int | None) -> None:
        if isinstance(o, dict):
            if _is_node(o):
                node = id(o)
            gated = node is not None and node not in reach
            t = o.get("$type")
            # questLegacy_NodeType is the older community action (same fields);
            # 99 vanilla phases still use it, e.g. cct_dtn_phase for 7th Hell.
            if t == "questCommunityTemplate_NodeType" or (t == "questLegacy_NodeType" and "spawnerReference" in o):
                items["communities"].append({"ref": val(o.get("spawnerReference")), "entry": val(o.get("communityEntryName")),
                                             "phase": val(o.get("communityEntryPhaseName")), "action": o.get("action"),
                                             "gated": gated})
            elif t == "questSpawnSet_NodeType":
                s = json.dumps(o)
                items["spawn_sets"].append({"ref": val(o.get("reference")), "entry": val(o.get("entryName")),
                                            "phase": val(o.get("phaseName")), "action": o.get("action"), "gated": gated,
                                            "raw_refs": sorted(set(re.findall(r'"\$value": "(#[^"]+)"', s)))})
            elif t == "questDeviceManager_NodeTypeParams":
                items["devices"].append({"ref": val(o.get("objectRef")), "controller": val(o.get("deviceControllerClass")),
                                         "action": val(o.get("deviceAction")), "gated": gated,
                                         "props": {val(p["name"]): val(p.get("value")) for p in o.get("actionProperties") or []}})
            elif t == "questPhaseNodeDefinition":
                # A phase node instantiates these prefabs while it runs, in addition
                # to the child phase's own phasePrefabs.
                res = val(val(o.get("phaseResource") or {}).get("DepotPath") or {}) if isinstance(o.get("phaseResource"), dict) else None
                if isinstance(res, str) and res.endswith(".questphase"):
                    items["child_phases"].append(res.replace("\\", "/"))
                    if not gated:
                        items["open_child_phases"].append(res.replace("\\", "/"))
                for e in o.get("phaseInstancePrefabs") or []:
                    e = val(e)
                    ref = val(e.get("prefabNodeRef")) if isinstance(e, dict) else None
                    if ref:
                        items["gated_instance_prefabs" if gated else "instance_prefabs"].append(ref)
            elif t == "questSetVar_NodeType" and not gated:
                items["sets_facts"].append(str(val(o.get("factName"))))
            elif t == "questTogglePrefabVariant_NodeType":
                for p in o.get("params") or []:
                    p = val(p)
                    items["toggles"].append({"ref": val(p.get("prefabNodeRef")), "gated": gated,
                                             "states": {val(s["name"]): s.get("show") for s in p.get("variantStates") or []}})
            for v in o.values():
                visit(v, node)
        elif isinstance(o, list):
            for v in o:
                visit(v, node)

    visit(d, None)
    for pp in val(val(d["Data"]["RootChunk"]).get("phasePrefabs")) or []:
        items["prefabs"].append(val(pp.get("prefabNodeRef")) if isinstance(pp, dict) else val(pp))
    return {"phase": rel, **{k: v for k, v in items.items()}}


def clean_slate_forbidden() -> tuple[set[str], tuple[str, ...]]:
    """Facts the clean slate never sets: a condition requiring one never passes."""
    root = Path(__file__).resolve().parent.parent / "data" / "clean-slate"
    spec = json.loads((root / "clean_slate_spec.json").read_text(encoding="utf-8"))["questphase"]
    cast = json.loads((root / "cast_and_hubs.json").read_text(encoding="utf-8"))
    facts = set(spec.get("forbidden_facts") or []) | set(cast.get("forbidden_default_on_facts") or [])
    ALLOWED_PREFIXED.clear()
    ALLOWED_PREFIXED.update(spec.get("allowed_prefixed_facts") or [])
    return facts, tuple(spec.get("forbidden_fact_prefixes") or [])


# The engine merges ep1.gamedef's quests at boot (docs/research/option-a-clean-
# slate-start.md 5.3), so Phantom Liberty's tree runs alongside ours, gated
# by facts.
EP1_AUTO_MERGED_ROOTS = ["ep1/quest/ep1.questphase"]
# The PL campaign under it stays dormant: its start needs q005_done and
# ep1_active (both forbidden) plus player-driven triggers, which a static
# fact analysis cannot see. Never treat it as running.
EP1_DORMANT_PREFIXES = ("ep1/quest/main_quests/",)


def _kept_closure(rows: list[dict]) -> set[str]:
    root = Path(__file__).resolve().parent.parent / "data" / "clean-slate"
    spec = json.loads((root / "clean_slate_spec.json").read_text(encoding="utf-8"))["questphase"]
    children = {r["phase"]: r.get("open_child_phases") or [] for r in rows}
    todo = [d["depot_path"].replace("\\", "/") for d in spec["kept_depot_phases"]]
    todo += [p.replace("\\", "/") for p in spec.get("inline_phase_depot_refs") or []]
    todo += EP1_AUTO_MERGED_ROOTS
    kept: set[str] = set()
    while todo:
        ph = todo.pop()
        if ph not in kept:
            kept.add(ph)
            todo += [c for c in children.get(ph, []) if not c.startswith(EP1_DORMANT_PREFIXES)]
    return kept


def _settable_facts(rows: list[dict]) -> set[str]:
    """Facts something in the clean slate can set: our initial facts, facts
    the game's and this mod's scripts set by name, and facts reachable fact
    nodes in kept phases set."""
    root = Path(__file__).resolve().parent.parent
    spec = json.loads((root / "data" / "clean-slate" / "clean_slate_spec.json").read_text(encoding="utf-8"))["questphase"]
    facts = {f["fact"] for f in spec.get("initial_facts") or []}
    pat = re.compile(r'SetFact(?:Value)?\(n"([A-Za-z0-9_]+)"')
    for d in (root / "refs" / "cyberpunk", root / "src"):
        for f in list(d.rglob("*.swift")) + list(d.rglob("*.reds")):
            facts |= set(pat.findall(f.read_text(encoding="utf-8", errors="ignore")))
    kept = _kept_closure(rows)
    for r in rows:
        if r["phase"] in kept:
            facts |= set(r.get("sets_facts") or [])
    return facts


def stage_phases(a: argparse.Namespace) -> None:
    """Two passes: the first finds which facts the clean slate can set; the
    second gates every item on conditions that need any other fact."""
    forbidden, prefixes = clean_slate_forbidden()
    files = sorted(a.phases.rglob("*.questphase.json"))
    settable: set[str] | None = None
    for _pass in range(2):
        rows = []
        for p in files:
            rel = "/".join(p.relative_to(a.phases).parts[1:])[: -len(".json")]
            try:
                rows.append(_phase_items(p, rel, forbidden, prefixes, settable))
            except (json.JSONDecodeError, KeyError) as exc:
                rows.append({"phase": rel, "error": str(exc)})
        settable = _settable_facts(rows) - forbidden
    a.out.mkdir(parents=True, exist_ok=True)
    write_jsonl(a.out / "phases.jsonl", rows)
    n = sum(1 for r in rows if any(r.get(k) for k in ("communities", "spawn_sets", "devices", "toggles", "prefabs")))
    print(f"phases: {len(rows)} read, {n} touch venues, {len(settable)} settable facts")


# ---------------------------------------------------------------- catalog

QUEST_ID = re.compile(r"\b((?:q|sq|mq|ep1_|sts_|ma_|mws_|sa_|bd_)[a-z0-9]*?\d+[a-z]?)(?=_|$)")


_SUBPREFAB = re.compile(r"_(env(_[a-z0-9]+)?|fx|gameplay|questdesign|leveldesign|lighting|audio|decoration|devices|interior|openworld)$")


def _venue_name(seg: str) -> str:
    name = re.sub(r"_prefab[A-Z0-9]{7}$", "", seg.lstrip("#").replace("{", "").replace("}", ""))
    while True:
        stripped = _SUBPREFAB.sub("", name)
        if stripped == name or len(stripped) < 4:
            return name
        name = stripped


def venue_of(path: str | None) -> str | None:
    """Top-level location prefab of a full node path: the first 'loc_*' segment, else the
    deepest '_prefabXXXXXXX' segment under the sub-district."""
    if not path or not path.startswith("$/"):
        return None
    segs = path[2:].split("/")
    for s in segs:
        if s.lstrip("#{").startswith("loc_"):
            return _venue_name(s)
    for s in segs[3:]:
        if re.search(r"_prefab[A-Z0-9]{7}$", s):
            return _venue_name(s)
    return None


def quest_family(q: str) -> str:
    for prefix, fam in (("sts_", "gig"), ("ma_", "hustle"), ("mq", "minor"), ("sq", "side"), ("q", "main"),
                        ("ep1_", "ep1"), ("mws_", "world_story"), ("sa_", "activity"), ("bd_", "braindance")):
        if q.startswith(prefix):
            return fam
    return "other"


def tier_of(v: dict) -> str:
    """Research triage. 'individual': an authored location used by a main job,
    side job, minor job or gig, with real people, devices or sections to
    restore; one research agent each. 'batch': everything else that touches the
    world (open-world areas, hustles, apartments, small sites), several per
    agent. 'skip': nothing to restore."""
    c = v["counts"]
    people = c["communities"] + c["spawn_sets"]
    name = v["venue"]
    quest_fams = {quest_family(q) for q in v["quests"]} & {"main", "side", "minor", "gig", "ep1"}
    small_kind = name.startswith(("loc_ma_", "loc_dlc6_apart")) or "fixer_" in name
    if name.startswith("loc_") and quest_fams and not small_kind and (people >= 5 or c["devices"] >= 10 or c["prefabs"] >= 2):
        return "individual"
    if people or c["devices"] or c["toggles"] or c["prefabs"]:
        return "batch"
    return "skip"


def stage_catalog(a: argparse.Namespace) -> None:
    comms: dict[str, dict] = json.loads((a.out / "communities.json").read_text(encoding="utf-8"))
    spots: dict[str, dict] = {}
    devices_pos: list[tuple[str, list[float], str]] = []  # (gid, pos, debug)
    hash_path: dict[str, str] = {}
    ref_paths: dict[str, list[str]] = defaultdict(list)  # short '#name' -> full paths
    unconverted: list[str] = []
    for bp in sorted((a.out / "sectors").glob("batch_*.jsonl")):
        for r in read_jsonl(bp):
            k = r["kind"]
            if k == "spot":
                spots[r["gid"]] = r
            elif k == "device":
                devices_pos.append((r["gid"], r["pos"], r.get("debug") or ""))
            elif k == "ref":
                hash_path[r["hash"]] = r["path"]
                last = r["path"].rsplit("/", 1)[-1]
                if last.startswith("#"):
                    ref_paths[last].append(r["path"])
            elif k == "area":
                c = comms.setdefault(r["cid"], {"id": r["cid"], "entries": []})
                for key, ids in r["spots"].items():
                    c.setdefault("spots", {}).setdefault(key, ids)
            elif k == "unconverted":
                unconverted.append(r["sector"])
    for c in comms.values():
        p = c.get("path")
        if p:
            last = p.rsplit("/", 1)[-1]
            if last.startswith("#") and p not in ref_paths[last]:
                ref_paths[last].append(p)

    # Streaming blocks name every quest prefab and variant node by full path;
    # each '#'-tagged prefix of those paths is itself an addressable node.
    for bf in sorted(a.blocks.rglob("all.streamingblock.json")):
        for o in walk(json.loads(bf.read_text(encoding="utf-8"))):
            for key in ("questPrefabNodeRef", "nodeRef"):
                p = val(o.get(key)) if key in o else None
                if isinstance(p, str) and p.startswith("$/"):
                    segs = p.split("/")
                    for i in range(2, len(segs) + 1):
                        if segs[i - 1].startswith("#"):
                            pre = "/".join(segs[:i])
                            lst = ref_paths[segs[i - 1]]
                            if pre not in lst:
                                lst.append(pre)

    by_path = {c["path"]: c for c in comms.values() if c.get("path")}
    dev_pos = {gid: pos for gid, pos, _d in devices_pos}

    def resolve(ref: str | None) -> list[str]:
        if not ref:
            return []
        if ref.startswith("$/"):
            return [ref]
        return sorted(set(ref_paths.get(ref, [])))

    wiki: dict[str, list[dict]] = defaultdict(list)
    ix = a.wiki / "index.json"
    if ix.exists():
        for page in json.loads(ix.read_text(encoding="utf-8")):
            text = (a.wiki / page["file"]).read_text(encoding="utf-8")
            m = re.search(r"\|\s*baseid\s*=\s*([^\n|}]+)", text)
            if m:
                for qid in re.split(r"[\s,<>/]+|br", m.group(1)):
                    qm = QUEST_ID.match(qid.strip().lower())
                    if qm:
                        wiki[qm.group(1)].append({"title": page["title"], "file": page["file"], "kinds": page["kinds"]})

    overrides = {o["venue"]: o for o in json.loads(a.overrides.read_text(encoding="utf-8"))["venues"]}
    venues: dict[str, dict] = {}

    def venue(name: str) -> dict:
        return venues.setdefault(name, {"venue": name, "quests": set(), "phases": set(), "prefabs": {},
                                        "communities": {}, "spawn_sets": {}, "devices": {}, "toggles": {}})

    def add(v: dict, kind: str, it: Any, ref: str | None, full: str | None, ph: str, inferred: bool) -> None:
        if kind in ("prefabs", "instance_prefabs", "gated_instance_prefabs"):
            e = v["prefabs"].setdefault(full or ref, {"owners": set(), "kinds": set()})
            e["owners"].add(ph)
            e["kinds"].add("phase" if kind == "prefabs" else "instance")
            return
        if kind == "communities":
            key = f"{full or ref}|{it['entry']}|{it['phase']}"
            e = v["communities"].setdefault(key, {"ref": ref, "path": full, "entry": it["entry"],
                                                  "phase": it["phase"], "actions": set(), "owners": set()})
            e["actions"].add(it["action"])
            e["owners"].add(ph)
            if inferred:
                e["venue_inferred"] = True
            c = by_path.get(full) if full else None
            if c and "record" not in e and it["entry"] == "None":
                # Whole-community activation: every entry starts in its initial phase.
                e["whole_community"] = True
                ents = [(x, (x.get("initial") or {}).get("phase")) for x in c["entries"]]
                ws = [spots[i]["workspot"] for x, ph0 in ents
                      for i in (c.get("spots") or {}).get(f"{x['name']}/{ph0}", []) if i in spots]
                e["entries"] = [{"entry": x["name"], "initial_phase": ph0, "record": x["record"],
                                 "role": role_of(x["record"])} for x, ph0 in ents]
                e["workspots"] = sorted({w for w in ws if w})
                roles = {role_of(x["record"]) for x, _ in ents}
                e["role"] = next((r for r in ("netrunner", "combat", "civilian", "vehicle") if r in roles), "unknown")
                pos = sorted({posture(w) for w in ws}) or ["unknown"]
                e["posture"] = "alert" if "alert" in pos else pos[0] if len(pos) == 1 else "mixed:" + "+".join(pos)
                e["record"] = None
            elif c and "record" not in e:
                ent = next((x for x in c["entries"] if x["name"] == it["entry"]), None)
                e["record"] = ent and ent["record"]
                e["role"] = role_of(e["record"])
                ids = (c.get("spots") or {}).get(f"{it['entry']}/{it['phase']}", [])
                ws = [spots[i]["workspot"] for i in ids if i in spots]
                e["workspots"] = sorted({w for w in ws if w})
                e["spots"] = len(ids)
                e["spots_resolved"] = sum(1 for i in ids if i in spots)
                pos = sorted({posture(w) for w in ws}) or ["unknown"]
                e["posture"] = "alert" if "alert" in pos else pos[0] if len(pos) == 1 else "mixed:" + "+".join(pos)
                if ids and ids[0] in spots:
                    e["spot_pos"] = spots[ids[0]]["pos"]
            return
        key = json.dumps({k: it.get(k) for k in it if k != "raw_refs"}, sort_keys=True)
        e = v[kind].setdefault((full or "") + "|" + key, {**{k: it[k] for k in it if k != "raw_refs"},
                                                          "path": full, "owners": set()})
        e["owners"].add(ph)
        if inferred:
            e["venue_inferred"] = True

    unresolved: dict[str, int] = defaultdict(int)
    inferred_n: dict[str, int] = defaultdict(int)
    for row in read_jsonl(a.out / "phases.jsonl"):
        ph = row["phase"]
        stem = Path(ph).name.replace(".questphase", "")
        qm = QUEST_ID.match(stem)
        quest = qm.group(1) if qm else stem
        resolved: list[tuple[str, Any, str | None, str, str]] = []
        pending: list[tuple[str, Any, str | None]] = []
        for kind in ("prefabs", "instance_prefabs", "gated_instance_prefabs", "communities", "spawn_sets", "devices", "toggles"):
            for it in row.get(kind) or []:
                if kind == "communities" and it.get("action") == "Deactivate":
                    continue  # switches people off; not a spawn
                if kind == "communities" and it.get("phase") == "None" and it.get("entry") != "None":
                    continue  # entry reset without a phase; not a spawn
                ref = it if kind in ("prefabs", "instance_prefabs", "gated_instance_prefabs") else it.get("ref")
                hits = [(full, venue_of(full)) for full in resolve(ref)]
                hits = [(f, vn) for f, vn in hits if vn]
                if hits:
                    resolved += [(kind, it, ref, f, vn) for f, vn in hits]
                else:
                    pending.append((kind, it, ref))
        row_venues = sorted({vn for *_x, vn in resolved})
        for kind, it, ref, full, vn in resolved:
            v = venue(vn)
            v["quests"].add(quest)
            v["phases"].add(ph)
            add(v, kind, it, ref, full, ph, False)
        # Unresolved refs (no converted sector names them yet) belong to the
        # venues their own phase touches; flagged so a reader knows.
        for kind, it, ref in pending:
            if not row_venues:
                unresolved[kind] += 1
                continue
            inferred_n[kind] += 1
            for vn in row_venues:
                add(venue(vn), kind, it, ref, None, ph, True)

    # Communities that live under a venue's prefab, activated by vanilla or not.
    registry_by_venue: dict[str, set[str]] = defaultdict(set)
    for c in comms.values():
        vn0 = venue_of(c.get("path"))
        if vn0:
            registry_by_venue[vn0].add(c["path"])

    def plain(o: Any) -> Any:
        if isinstance(o, set):
            return sorted(o)
        if isinstance(o, dict):
            return {k: plain(v) for k, v in o.items()}
        if isinstance(o, list):
            return [plain(v) for v in o]
        return o

    out = []
    for vn in sorted(venues):
        v = venues[vn]
        rec = {
            "venue": vn,
            "quests": sorted(v["quests"]),
            "phases": sorted(v["phases"]),
            "prefabs": [{"path": p, "owners": sorted(o["owners"]), "kinds": sorted(o["kinds"])}
                        for p, o in sorted(v["prefabs"].items())],
            "communities": [plain(e) for _k, e in sorted(v["communities"].items())],
            "spawn_sets": [plain(e) for _k, e in sorted(v["spawn_sets"].items())],
            "devices": [plain(e) for _k, e in sorted(v["devices"].items())],
            "toggles": [plain(e) for _k, e in sorted(v["toggles"].items())],
            "wiki": sorted({json.dumps(w, sort_keys=True) for q in v["quests"] for w in wiki.get(q, [])}),
        }
        rec["wiki"] = [json.loads(w) for w in rec["wiki"]]
        # Every phase each used community entry defines, activated by vanilla
        # or not: an unused relaxed phase is often the right ambient choice.
        used = {(e["path"], e["entry"], e["phase"]) for e in rec["communities"]}
        opts = []
        owned = registry_by_venue.get(vn, set())
        for cpath in sorted({e["path"] for e in rec["communities"] if e.get("path")} | owned):
            c = by_path.get(cpath)
            if not c:
                continue
            for ent in c["entries"]:
                for phname in ent["phases"]:
                    ids = (c.get("spots") or {}).get(f"{ent['name']}/{phname}", [])
                    ws = sorted({spots[i]["workspot"] for i in ids if i in spots and spots[i]["workspot"]})
                    pos = sorted({posture(w) for w in ws}) or ["unknown"]
                    first = next((spots[i]["pos"] for i in ids if i in spots), None)
                    opts.append({"path": cpath, "entry": ent["name"], "phase": phname, "record": ent["record"],
                                 "role": role_of(ent["record"]), "spot_pos": first,
                                 "initial": ent.get("initial"), "activated": (cpath, ent["name"], phname) in used,
                                 "posture": "alert" if "alert" in pos else pos[0] if len(pos) == 1 else "mixed:" + "+".join(pos),
                                 "workspots": ws})
        rec["community_options"] = opts
        for d in rec["devices"]:
            if d.get("path"):
                d["pos"] = dev_pos.get(str(fnv1a64(d["path"])))
        # Anchor candidates: named devices nearest the venue's own spots, for
        # venues vanilla drives no device at (rule 8 needs a device anchor).
        pts = [e["spot_pos"] for e in rec["communities"] if e.get("spot_pos")]
        if pts:
            cands = []
            for gid, pos, dbg in devices_pos:
                path = hash_path.get(gid)
                if not path:
                    continue
                d = min(((pos[0] - p[0]) ** 2 + (pos[1] - p[1]) ** 2 + (pos[2] - p[2]) ** 2) ** 0.5 for p in pts)
                if d <= 150.0:
                    cands.append({"path": path, "dist": round(d, 1), "debug": dbg})
            rec["anchor_candidates"] = sorted(cands, key=lambda c: c["dist"])[:5]
        rec["counts"] = {k: len(rec[k]) for k in ("prefabs", "communities", "spawn_sets", "devices", "toggles", "quests")}
        rec["quest_families"] = sorted({quest_family(q) for q in rec["quests"]})
        rec["tier"] = tier_of(rec)
        if vn in overrides:
            rec["tier"] = overrides[vn]["decision"]
            rec["tier_why"] = overrides[vn]["why"]
        out.append(rec)
    (a.out / "catalog.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    missing = sorted(set(overrides) - {r["venue"] for r in out})
    if missing:
        raise SystemExit(f"triage overrides name unknown venues: {missing}")
    tiers = {t: sum(1 for r in out if r["tier"] == t) for t in ("individual", "batch", "excluded", "deferred")}
    print(f"catalog: {len(out)} venues {tiers}; unresolved refs by kind {dict(unresolved)}; "
          f"inferred by phase {dict(inferred_n)}; {len(spots)} spots indexed; {len(unconverted)} sectors unconverted")


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["sectors", "communities", "phases", "catalog", "all"])
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--sectors", type=Path, default=DEFAULT_SECTORS)
    ap.add_argument("--phases", type=Path, default=DEFAULT_PHASES)
    ap.add_argument("--wiki", type=Path, default=DEFAULT_WIKI)
    ap.add_argument("--overrides", type=Path, default=Path(__file__).resolve().parent.parent / "data" / "venues" / "triage_overrides.json")
    ap.add_argument("--blocks", type=Path, default=HOME / "na-prop-scratch" / "blocks")
    ap.add_argument("--wk", type=Path, default=Path(os.environ.get("WK_CLI", DEFAULT_WK)))
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--limit", nargs="*", help="sectors stage: only sector paths containing one of these strings (testing)")
    a = ap.parse_args()
    stages = {"sectors": stage_sectors, "communities": stage_communities, "phases": stage_phases,
              "catalog": stage_catalog}
    for s in (["phases", "communities", "sectors", "catalog"] if a.stage == "all" else [a.stage]):
        stages[s](a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
