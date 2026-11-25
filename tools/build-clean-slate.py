#!/usr/bin/env python3
"""Build the Clean-Slate Night City world archive for Neon Ascendancy.

Reads the declarative spec `data/clean-slate/clean_slate_spec.json` and produces
`dist/neon_ascendancy_world.archive` containing exactly four CR2W resources:

  mod\\neon_ascendancy\\ascendancy.gamedef    (custom gsmGameDefinition)
  mod\\neon_ascendancy\\ascendancy.quest      (Start -> ascendancy.questphase)
  mod\\neon_ascendancy\\ascendancy.questphase (clean-slate hub graph)
  mod\\neon_ascendancy\\spike_kab07.questphase (dormant fact-gated living-world spike)

Pipeline (all through the pinned WolvenKit.CLI 10.0.0-beta.1, DOTNET_ROLL_FORWARD=Major):
  1. Extract vanilla templates from basegame_4_gamedata.archive into a temp dir:
     cyberpunk2077.gamedef/.quest, open_world_content.questphase, q001.quest
     (teleport node template) and sts_wat_kab_07_combat.questphase (spawn manager template).
  2. Build the four CR2W JSONs from the templates + spec, using the exact WolvenKit
     CR2W JSON schema conventions (HandleIds unique and referenced only after they
     are defined; connection definitions stored in the source socket's connections
     list with the destination socket definition embedded inline).
  3. `convert deserialize` -> CR2W files, copy ONLY the CR2W files (never .json
     sidecars) into a pack dir and `pack` -> dist/neon_ascendancy_world.archive.

With --check the script re-extracts the packed archive, re-serializes it to JSON,
and asserts: the four resources exist, the graphs connect from Start, every kept
phase + initial fact is present, zero excluded campaign/gig/hustle/Johnny phases
are present, and zero .json files leaked into the archive.

Environment:
  WK_CLI    WolvenKit.CLI executable (default ~/.cache/neon-ascendancy/wolvenkit-10.0.0-beta.1/WolvenKit.CLI)
  GAME_DIR  Cyberpunk 2077 install root (default ~/Games/Cyberpunk 2077)

Reproducibility: the generated JSON sources are byte-deterministic for a pinned
spec + game version. The CR2W/archive bytes depend on WolvenKit internals; content
is verified by the round-trip --check, which is the source of truth.
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
from typing import Any, Callable

ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = ROOT / "data" / "clean-slate" / "clean_slate_spec.json"
DEFAULT_WK = Path(
    os.environ.get(
        "WK_CLI",
        Path.home() / ".cache" / "neon-ascendancy" / "wolvenkit-10.0.0-beta.1" / "WolvenKit.CLI",
    )
)
DEFAULT_GAME_DIR = Path(os.environ.get("GAME_DIR", Path.home() / "Games" / "Cyberpunk 2077"))

FIXED_HEADER: dict[str, Any] = {
    "WolvenKitVersion": "10.0.0-beta.1",
    "WKitJsonVersion": "0.0.9",
    "GameVersion": 2500,
    "ExportedDateTime": "2026-01-01T00:00:00.0000000Z",
    "DataType": "CR2W",
    "ArchiveFileName": "",
}


# --------------------------------------------------------------------------
# WolvenKit CLI helpers
# --------------------------------------------------------------------------

def run_wk(wk: Path, args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    """Run WolvenKit.CLI; fail loudly on non-zero exit or logged errors.

    The CLI returns rc 0 even when a conversion fails and only logs an
    `[ 0: Error ]` line, so the output is scanned for errors as well."""
    env = {**os.environ, "DOTNET_ROLL_FORWARD": "Major"}
    proc = subprocess.run(
        [str(wk), *args], env=env, capture_output=True, text=True, cwd=str(cwd) if cwd else None
    )
    logged_error = "Error" in proc.stdout or "Error" in proc.stderr
    if proc.returncode != 0 or logged_error:
        raise RuntimeError(
            f"WolvenKit.CLI failed (rc={proc.returncode}): {' '.join(args)}\n"
            f"stdout:\n{proc.stdout[-2000:]}\nstderr:\n{proc.stderr[-2000:]}"
        )
    return proc


# --------------------------------------------------------------------------
# CR2W JSON primitives (schema shapes verified against vanilla 2.5 resources)
# --------------------------------------------------------------------------

def cname(value: str) -> dict[str, Any]:
    return {"$type": "CName", "$storage": "string", "$value": value}


def noderef(value: str) -> dict[str, Any]:
    return {"$type": "NodeRef", "$storage": "string", "$value": value}


def rpath(depot: str) -> dict[str, Any]:
    return {
        "DepotPath": {"$type": "ResourcePath", "$storage": "string", "$value": depot},
        "Flags": "Soft",
    }


def collect_handle_ids(value: Any) -> set[int]:
    """All numeric HandleIds present anywhere in a JSON subtree."""
    out: set[int] = set()
    if isinstance(value, dict):
        if "HandleId" in value and str(value.get("HandleId", "")).isdigit():
            out.add(int(value["HandleId"]))
        for v in value.values():
            out |= collect_handle_ids(v)
    elif isinstance(value, list):
        for v in value:
            out |= collect_handle_ids(v)
    return out


def wrap_resource(root_chunk: dict[str, Any], data_version: int = 195) -> dict[str, Any]:
    return {
        "Header": dict(FIXED_HEADER),
        "Data": {
            "Version": data_version,
            "BuildVersion": 0,
            "RootChunk": root_chunk,
            "EmbeddedFiles": [],
        },
    }


class QuestGraph:
    """Builds a quest graph node list using the vanilla CR2W JSON conventions.

    Invariants (mirror the vanilla serializer so WolvenKit deserializes cleanly):
      - HandleIds are unique, sequential strings, and a HandleRefId always points
        at a HandleId that appeared EARLIER in the serialized document.
      - A connection definition lives in the SOURCE socket's `connections` list,
        with `source` as a HandleRefId and `destination` as the full inline socket
        definition (carrying the back-ref in its own `connections` list).
      - The destination node's socket slot holds a bare HandleRefId.
    """

    def __init__(self, start_handle: int):
        self._next_handle = start_handle
        self._next_id = 1000
        self.nodes: list[dict[str, Any]] = []
        self._socket_meta: dict[str, tuple[str, str]] = {}  # handle -> (name, type)
        self._socket_conns: dict[str, list[dict[str, Any]]] = {}  # handle -> conn list
        self._targeted: set[str] = set()

    def alloc(self) -> str:
        h = str(self._next_handle)
        self._next_handle += 1
        return h

    def node_id(self) -> int:
        nid = self._next_id
        self._next_id += 1
        return nid

    def register_socket(self, handle: str, name: str, stype: str) -> None:
        """Register an externally-owned socket (e.g. inside a copied node) so connect() can target it."""
        self._socket_meta[handle] = (name, stype)
        self._socket_conns.setdefault(handle, [])

    def renumber(self, value: Any) -> Any:
        """Deep-copy a template subtree and reassign every HandleId to a fresh
        allocator handle (HandleRefIds pointing inside the subtree are remapped).
        Template-internal handles must not collide with handles of copied vanilla
        nodes, which keep their original ids."""
        remap: dict[str, str] = {}

        def pass1(v: Any) -> None:
            if isinstance(v, dict):
                if "HandleId" in v and isinstance(v.get("HandleId"), str):
                    remap[v["HandleId"]] = self.alloc()
                for item in v.values():
                    pass1(item)
            elif isinstance(v, list):
                for item in v:
                    pass1(item)

        def pass2(v: Any) -> Any:
            if isinstance(v, dict):
                out = {}
                for k, item in v.items():
                    if k == "HandleId" and isinstance(item, str) and item in remap:
                        out[k] = remap[item]
                    elif k == "HandleRefId" and isinstance(item, str) and item in remap:
                        out[k] = remap[item]
                    else:
                        out[k] = pass2(item)
                return out
            if isinstance(v, list):
                return [pass2(item) for item in v]
            return v

        pass1(value)
        return pass2(value)

    def new_socket(self, name: str, stype: str) -> str:
        h = self.alloc()
        self._socket_meta[h] = (name, stype)
        self._socket_conns[h] = []
        return h

    def connect(self, src: str, dst: str) -> None:
        """src -> dst. Requires both sockets to exist (dst may belong to a copied node)."""
        if dst not in self._socket_meta:
            raise KeyError(f"unknown destination socket handle {dst}")
        ch = self.alloc()
        self._socket_conns[src].append(
            {
                "HandleId": ch,
                "Data": {
                    "$type": "graphGraphConnectionDefinition",
                    "destination": {
                        "HandleId": dst,
                        "Data": {
                            "$type": "questSocketDefinition",
                            "connections": [{"HandleRefId": ch}],
                            "name": cname(self._socket_meta[dst][0]),
                            "type": self._socket_meta[dst][1],
                        },
                    },
                    "source": {"HandleRefId": src},
                },
            }
        )
        self._targeted.add(dst)

    def _slots(self, handles: list[str]) -> list[dict[str, Any]]:
        out = []
        for h in handles:
            if h in self._targeted:
                out.append({"HandleRefId": h})
            else:
                out.append(
                    {
                        "HandleId": h,
                        "Data": {
                            "$type": "questSocketDefinition",
                            "connections": self._socket_conns[h],
                            "name": cname(self._socket_meta[h][0]),
                            "type": self._socket_meta[h][1],
                        },
                    }
                )
        return out

    def add_input_node(self, socket_name: str) -> str:
        cut = self.new_socket("CutDestination", "CutDestination")
        out = self.new_socket("Out", "Output")
        self.nodes.append(
            {
                "HandleId": self.alloc(),
                "Data": {
                    "$type": "questInputNodeDefinition",
                    "id": self.node_id(),
                    "socketName": cname(socket_name),
                    "_sockets": [cut, out],
                },
            }
        )
        return out

    def add_hub_node(self) -> tuple[str, str]:
        cut = self.new_socket("CutDestination", "CutDestination")
        inp = self.new_socket("In1", "Input")
        out = self.new_socket("Out1", "Output")
        self.nodes.append(
            {
                "HandleId": self.alloc(),
                "Data": {
                    "$type": "questLogicalHubNodeDefinition",
                    "id": self.node_id(),
                    "inputSocketCount": 1,
                    "outputSocketCount": 1,
                    "_sockets": [cut, inp, out],
                },
            }
        )
        return inp, out

    def add_fact_node(self, fact: str, value: int) -> tuple[str, str]:
        cut = self.new_socket("CutDestination", "CutDestination")
        inp = self.new_socket("In", "Input")
        out = self.new_socket("Out", "Output")
        type_handle = self.alloc()
        self.nodes.append(
            {
                "HandleId": self.alloc(),
                "Data": {
                    "$type": "questFactsDBManagerNodeDefinition",
                    "id": self.node_id(),
                    "_sockets": [cut, inp, out],
                    "type": {
                        "HandleId": type_handle,
                        "Data": {
                            "$type": "questSetVar_NodeType",
                            "factName": fact,
                            "setExactValue": 1,
                            "value": value,
                        },
                    },
                },
            }
        )
        return inp, out

    def add_phase_node(self, depot: str) -> str:
        cut = self.new_socket("CutDestination", "CutDestination")
        inp = self.new_socket("In1", "Input")
        self.nodes.append(
            {
                "HandleId": self.alloc(),
                "Data": {
                    "$type": "questPhaseNodeDefinition",
                    "id": self.node_id(),
                    "phaseGraph": None,
                    "phaseInstancePrefabs": [],
                    "phaseResource": rpath(depot),
                    "saveLock": 0,
                    "_sockets": [cut, inp],
                    "unfreezingTriggerNodeRef": {"$type": "NodeRef", "$storage": "uint64", "$value": "0"},
                },
            }
        )
        return inp

    def add_pause_fact_node(self, fact: str, comparison: str, value: int) -> tuple[str, str]:
        cut = self.new_socket("CutDestination", "CutDestination")
        inp = self.new_socket("In", "Input")
        out = self.new_socket("Out", "Output")
        self.nodes.append(
            {
                "HandleId": self.alloc(),
                "Data": {
                    "$type": "questPauseConditionNodeDefinition",
                    "id": self.node_id(),
                    "condition": {
                        "HandleId": self.alloc(),
                        "Data": {
                            "$type": "questFactsDBCondition",
                            "type": {
                                "HandleId": self.alloc(),
                                "Data": {
                                    "$type": "questVarComparison_ConditionType",
                                    "comparisonType": comparison,
                                    "factName": fact,
                                    "value": value,
                                },
                            },
                        },
                    },
                    "_sockets": [cut, inp, out],
                },
            }
        )
        return inp, out

    def add_copied_phase_node(self, vanilla_node: dict[str, Any]) -> str:
        """Deep-copy an inline phase node (e.g. open_world_content nodes [7]/[8]/[139]/[142]/[156]).
        Returns the handle of its 'In1' input socket (the only external wiring point)."""
        data = json.loads(json.dumps(vanilla_node))
        in_handle = None
        for slot in data.get("sockets", []):
            if "HandleRefId" in slot:
                ref = slot["HandleRefId"]
                # register the socket name/type so connect() can embed it inline
                self._socket_meta[ref] = ("In1", "Input")
                self._socket_conns[ref] = []
                in_handle = ref
        if in_handle is None:
            raise ValueError(f"copied phase node id {vanilla_node.get('id')} has no HandleRefId input socket")
        # keep the vanilla socket list untouched (only the In HandleRefId is rewired
        # implicitly by connect() embedding the socket definition inline)
        self.nodes.append({"HandleId": self.alloc(), "Data": data})
        return in_handle

    def finalize(self) -> list[dict[str, Any]]:
        """Materialize node socket slots (full defs / HandleRefIds per target state)."""
        out = []
        for node in self.nodes:
            data = node["Data"]
            if "_sockets" in data:
                data["sockets"] = [
                    (
                        {"HandleRefId": h}
                        if h in self._targeted
                        else {
                            "HandleId": h,
                            "Data": {
                                "$type": "questSocketDefinition",
                                "connections": self._socket_conns[h],
                                "name": cname(self._socket_meta[h][0]),
                                "type": self._socket_meta[h][1],
                            },
                        }
                    )
                    for h in data.pop("_sockets")
                ]
            out.append(node)
        return out


# --------------------------------------------------------------------------
# Resource builders
# --------------------------------------------------------------------------

def build_gamedef(template: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    doc = json.loads(json.dumps(template))
    doc["Header"] = dict(FIXED_HEADER)
    rc = doc["Data"]["RootChunk"]
    spec_gd = spec["gamedef"]
    rc["mainQuests"][0]["Data"]["questFile"]["DepotPath"]["$value"] = spec_gd["main_quest"]
    rc["spawnPointTags"]["tags"] = [cname(t) for t in spec_gd["spawn_point_tags"]]
    rc["streamingWorld"]["DepotPath"]["$value"] = spec_gd["streaming_world"]
    rc["world"]["DepotPath"]["$value"] = spec_gd["world"]
    rc["worldName"] = spec_gd["world_name"]
    return doc


def build_quest(template: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    doc = json.loads(json.dumps(template))
    doc["Header"] = dict(FIXED_HEADER)
    rc = doc["Data"]["RootChunk"]
    for node in rc["graph"]["Data"]["nodes"]:
        if node["Data"].get("$type") == "questPhaseNodeDefinition":
            node["Data"]["phaseResource"]["DepotPath"]["$value"] = spec["quest"]["questphase"]
    return doc


def build_questphase(templates: dict[str, dict[str, Any]], spec: dict[str, Any]) -> dict[str, Any]:
    """Assemble the clean-slate hub questphase.

    Start -> hub -> initial fact managers (chained) -> fan-out to:
      kept external phases + spike gate pause -> spike phase + 5 copied inline phases.
    """
    qp = spec["questphase"]
    owc = templates["open_world_content_questphase"]

    # --- start our allocator above every handle id in the copied vanilla nodes;
    # template-derived nodes are renumbered through the allocator themselves.
    max_handle = 0
    for owc_node_id in [p["owc_node_id"] for p in qp["kept_inline_phases"]]:
        node = find_node_by_id(owc, owc_node_id)
        max_handle = max(max_handle, max(collect_handle_ids(node) | {0}))

    g = QuestGraph(start_handle=max_handle + 1)

    start_out = g.add_input_node(qp["entry_socket"])
    hub_in, hub_out = g.add_hub_node()
    g.connect(start_out, hub_in)

    prev_out = hub_out
    for entry in qp["initial_facts"]:
        f_in, f_out = g.add_fact_node(entry["fact"], entry["value"])
        g.connect(prev_out, f_in)
        prev_out = f_out

    # Fan-out directly from the final fact node (zero blocking teleport nodes).
    fan = prev_out

    # spike: gate pause -> spike phase node
    spike = qp["spike"]
    sp_in, sp_out = g.add_pause_fact_node(
        spike["gate"]["fact"], spike["gate"]["comparison_type"], spike["gate"]["value"]
    )
    g.connect(fan, sp_in)
    spike_phase_in = g.add_phase_node(spike["resource"])
    g.connect(sp_out, spike_phase_in)

    # kept external phases
    for entry in qp["kept_depot_phases"]:
        p_in = g.add_phase_node(entry["depot_path"])
        g.connect(fan, p_in)

    # copied inline phases from open_world_content (strictly untouched internals,
    # zero cross-graph handle references)
    for entry in qp["kept_inline_phases"]:
        vanilla = find_node_by_id(owc, entry["owc_node_id"])["Data"]
        in_handle = g.add_copied_phase_node(vanilla)
        g.connect(fan, in_handle)

    nodes = g.finalize()
    validate_refs(nodes)

    doc = wrap_resource(
        {
            "$type": "questQuestPhaseResource",
            "cookingPlatform": "PLATFORM_PC",
            "graph": {
                "HandleId": g.alloc(),
                "Data": {"$type": "questGraphDefinition", "nodes": nodes},
            },
            "inplacePhases": [],
            "phasePrefabs": [],
        }
    )
    cross = find_cross_graph_refs(doc)
    if cross:
        raise ValueError(f"cross-graph HandleRefIds detected: {cross[:5]}")
    return doc


def build_spike(templates: dict[str, dict[str, Any]], spec: dict[str, Any]) -> dict[str, Any]:
    """Dormant fact-gated living-world spike resource (phasePrefabs + spawn manager)."""
    spike = spec["questphase"]["spike"]
    template = templates["spawn_manager_node"]

    g = QuestGraph(start_handle=1)

    start_out = g.add_input_node(spike["entry_socket"])

    data = g.renumber(template)  # deep copy with fresh internal handles
    data.pop("sockets", None)  # sockets are rebuilt below with graph-local handles
    data["id"] = g.node_id()
    for action in data.get("actions", []):
        act_type = action["type"]["Data"]
        act_type["action"] = spike["spawn_manager"]["action"]
        act_type["communityEntryName"]["$value"] = spike["spawn_manager"]["community_entry_name"]
        act_type["communityEntryPhaseName"]["$value"] = spike["spawn_manager"]["community_entry_phase_name"]
        act_type["spawnerReference"]["$value"] = spike["spawn_manager"]["spawner_reference"]
    cut = g.new_socket("CutDestination", "CutDestination")
    inp = g.new_socket("In", "Input")
    out = g.new_socket("Out", "Output")
    data["_sockets"] = [cut, inp, out]
    g.nodes.append({"HandleId": g.alloc(), "Data": data})
    g.connect(start_out, inp)

    nodes = g.finalize()
    validate_refs(nodes)

    return wrap_resource(
        {
            "$type": "questQuestPhaseResource",
            "cookingPlatform": "PLATFORM_PC",
            "graph": {
                "HandleId": g.alloc(),
                "Data": {"$type": "questGraphDefinition", "nodes": nodes},
            },
            "inplacePhases": [],
            "phasePrefabs": [
                {
                    "$type": "questQuestPrefabEntry",
                    "prefabNodeRef": noderef(ref),
                }
                for ref in spike["phase_prefabs"]
            ],
        }
    )


# --------------------------------------------------------------------------
# Template helpers
# --------------------------------------------------------------------------

def find_node_by_id(resource: dict[str, Any], node_id: int) -> dict[str, Any]:
    for node in resource["Data"]["RootChunk"]["graph"]["Data"]["nodes"]:
        if node["Data"].get("id") == node_id:
            return node
    raise KeyError(f"node id {node_id} not found in template")


def find_first_node_of_type(resource: dict[str, Any], node_type: str) -> dict[str, Any]:
    def walk(value: Any) -> dict[str, Any] | None:
        if isinstance(value, dict):
            if value.get("$type") == node_type:
                return value
            for v in value.values():
                found = walk(v)
                if found is not None:
                    return found
        elif isinstance(value, list):
            for v in value:
                found = walk(v)
                if found is not None:
                    return found
        return None

    found = walk(resource)
    if found is None:
        raise KeyError(f"no {node_type} found in template")
    return found


def find_cross_graph_refs(doc: dict[str, Any]) -> list[tuple[str, str, str]]:
    """Return any HandleRefIds whose target HandleId belongs to a different questGraphDefinition."""
    owner: dict[str, str] = {}

    def map_graphs(value: Any, gid: str = "root") -> None:
        if isinstance(value, dict):
            if value.get("$type") == "questGraphDefinition":
                gid = f"graph@{id(value)}"
            if "HandleId" in value and isinstance(value.get("HandleId"), str):
                owner[value["HandleId"]] = gid
            for v in value.values():
                map_graphs(v, gid)
        elif isinstance(value, list):
            for v in value:
                map_graphs(v, gid)

    map_graphs(doc)
    bad: list[tuple[str, str, str]] = []

    def check_refs(value: Any, gid: str = "root") -> None:
        if isinstance(value, dict):
            if value.get("$type") == "questGraphDefinition":
                gid = f"graph@{id(value)}"
            if "HandleRefId" in value and isinstance(value.get("HandleRefId"), str):
                ref = value["HandleRefId"]
                ref_gid = owner.get(ref)
                if ref_gid is not None and ref_gid != gid:
                    bad.append((ref, ref_gid, gid))
            for v in value.values():
                check_refs(v, gid)
        elif isinstance(value, list):
            for v in value:
                check_refs(v, gid)

    check_refs(doc)
    return bad


def find_duplicate_handles(doc: dict[str, Any]) -> list[str]:
    seen: set[str] = set()
    dups: list[str] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            if "HandleId" in value and isinstance(value.get("HandleId"), str):
                h = value["HandleId"]
                if h in seen:
                    dups.append(h)
                else:
                    seen.add(h)
            for v in value.values():
                walk(v)
        elif isinstance(value, list):
            for v in value:
                walk(v)

    walk(doc)
    return dups


def validate_refs(nodes: list[dict[str, Any]]) -> None:
    """Ensure every HandleRefId points at a HandleId defined earlier in document order.

    This mirrors the constraint the WolvenKit JSON deserializer enforces; failing here
    means `convert deserialize` would fail with a confusing JsonException."""
    defined: set[str] = set()

    def walk(value: Any, order: list[str]):
        if isinstance(value, dict):
            if "HandleId" in value and isinstance(value.get("HandleId"), str):
                defined.add(value["HandleId"])
            if "HandleRefId" in value:
                ref = value["HandleRefId"]
                if ref not in defined:
                    raise ValueError(f"forward reference to undefined HandleId {ref}")
            for v in value.values():
                walk(v, order)
        elif isinstance(value, list):
            for v in value:
                walk(v, order)

    walk(nodes, [])


# --------------------------------------------------------------------------
# Build pipeline
# --------------------------------------------------------------------------

def extract_templates(wk: Path, game_dir: Path, spec: dict[str, Any], tmp: Path) -> dict[str, dict[str, Any]]:
    tpl = spec["templates"]
    archive = game_dir / tpl["archive"]
    if not archive.is_file():
        raise FileNotFoundError(f"missing game archive: {archive}")
    raw = tmp / "templates"
    raw.mkdir(parents=True, exist_ok=True)
    print(f"Extracting templates from {archive.name} ...", flush=True)

    # Build one anchored regex from the plain depot paths (escape \ and . for regex).
    depot_paths = [
        tpl["gamedef"],
        tpl["quest"],
        tpl["open_world_content_questphase"],
        tpl["spawn_manager_node_template"],
    ]
    escaped = [p.replace("\\", "\\\\").replace(".", "\\.") for p in depot_paths]
    regex = "^(" + "|".join(escaped) + ")$"
    run_wk(wk, ["extract", str(archive), "-o", str(raw), "-r", regex])
    run_wk(wk, ["convert", "serialize", str(raw)])

    def load(depot: str) -> dict[str, Any]:
        path = raw / depot.replace("\\", "/")
        json_path = Path(str(path) + ".json")
        if not json_path.is_file():
            raise FileNotFoundError(f"expected extracted template missing: {json_path}")
        with json_path.open("r", encoding="utf-8") as fh:
            return json.load(fh)

    gamedef = load(tpl["gamedef"])
    quest = load(tpl["quest"])
    owc = load(tpl["open_world_content_questphase"])
    spawn_resource = load(tpl["spawn_manager_node_template"])
    return {
        "gamedef": gamedef,
        "quest": quest,
        "open_world_content_questphase": owc,
        "spawn_manager_node": find_first_node_of_type(spawn_resource, "questSpawnManagerNodeDefinition"),
    }


def write_resource_json(directory: Path, rel_path: str, doc: dict[str, Any]) -> None:
    target = directory / rel_path.replace("\\", "/")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(doc, indent=2), encoding="utf-8")


def build(args: argparse.Namespace, spec: dict[str, Any]) -> Path:
    wk = Path(args.wk_cli)
    if not wk.is_file():
        raise FileNotFoundError(f"WolvenKit.CLI not found at {wk}")
    game_dir = Path(args.game_dir)

    dist_dir = ROOT / "dist"
    dist_dir.mkdir(parents=True, exist_ok=True)
    archive_out = ROOT / spec["output_archive"]

    with tempfile.TemporaryDirectory(prefix="na-clean-slate-") as tmp_s:
        tmp = Path(tmp_s)
        templates = extract_templates(wk, game_dir, spec, tmp)

        build_dir = tmp / "build"
        write_resource_json(build_dir, "mod/neon_ascendancy/ascendancy.gamedef.json", build_gamedef(templates["gamedef"], spec))
        write_resource_json(build_dir, "mod/neon_ascendancy/ascendancy.quest.json", build_quest(templates["quest"], spec))
        write_resource_json(
            build_dir, "mod/neon_ascendancy/ascendancy.questphase.json", build_questphase(templates, spec)
        )
        write_resource_json(build_dir, "mod/neon_ascendancy/spike_kab07.questphase.json", build_spike(templates, spec))

        print("Deserializing CR2W JSONs ...", flush=True)
        run_wk(wk, ["convert", "deserialize", str(build_dir)])

        # Pack CR2W files only (never the .json sidecars).
        pack_dir = tmp / "neon_ascendancy_world"
        for cr2w in sorted((build_dir / "mod" / "neon_ascendancy").iterdir()):
            if cr2w.suffix == ".json":
                continue
            dest = pack_dir / "mod" / "neon_ascendancy" / cr2w.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(cr2w, dest)
        print("Packing archive ...", flush=True)
        run_wk(wk, ["pack", str(pack_dir), "-o", str(dist_dir)])

    if not archive_out.is_file():
        raise RuntimeError(f"expected output archive missing: {archive_out}")
    return archive_out


# --------------------------------------------------------------------------
# Check pipeline
# --------------------------------------------------------------------------

class CheckFailure(Exception):
    pass


def check(args: argparse.Namespace, spec: dict[str, Any]) -> None:
    wk = Path(args.wk_cli)
    if not wk.is_file():
        raise FileNotFoundError(f"WolvenKit.CLI not found at {wk}")
    archive = ROOT / spec["output_archive"]
    if not archive.is_file():
        raise FileNotFoundError(f"archive not built yet: {archive} (run without --check first)")

    failures: list[str] = []

    def ok(cond: bool, message: str) -> None:
        if not cond:
            failures.append(message)

    with tempfile.TemporaryDirectory(prefix="na-clean-slate-check-") as tmp_s:
        tmp = Path(tmp_s)
        print(f"Extracting {archive.name} ...", flush=True)
        run_wk(wk, ["extract", str(archive), "-o", str(tmp)])
        extracted = sorted(p.relative_to(tmp).as_posix().replace("/", "\\") for p in tmp.rglob("*") if p.is_file())

        ok(extracted == sorted(spec["archive_resources"]),
           f"archive contents mismatch: {extracted}")
        ok(not any(p.lower().endswith(".json") for p in extracted),
           f"archive contains stray .json files: {[p for p in extracted if p.lower().endswith('.json')]}")

        run_wk(wk, ["convert", "serialize", str(tmp)])
        resources: dict[str, dict[str, Any]] = {}
        for rel in spec["archive_resources"]:
            jpath = tmp / (rel.replace("\\", "/") + ".json")
            ok(jpath.is_file(), f"missing serialized resource: {rel}")
            if jpath.is_file():
                with jpath.open("r", encoding="utf-8") as fh:
                    resources[rel] = json.load(fh)

        if not failures and len(resources) == len(spec["archive_resources"]):
            _check_gamedef(resources, spec, ok)
            _check_quest(resources, spec, ok)
            _check_questphase(resources, spec, ok)
            _check_spike(resources, spec, ok)

    if failures:
        print("\n--check FAILED:")
        for f in failures:
            print(f"  - {f}")
        raise SystemExit(1)
    print("\n--check PASSED: all resources valid, every kept phase & fact present, "
          "zero excluded content, zero stray .json files.")


def _gamedef_path() -> str:
    return "mod\\neon_ascendancy\\ascendancy.gamedef"


def _check_gamedef(resources: dict[str, dict[str, Any]], spec: dict[str, Any], ok: Callable[[bool, str], None]) -> None:
    doc = resources[_gamedef_path()]
    rc = doc["Data"]["RootChunk"]
    ok(rc.get("$type") == "gsmGameDefinition", "gamedef root type is not gsmGameDefinition")
    gd = spec["gamedef"]
    quest_files = [m["Data"]["questFile"]["DepotPath"]["$value"] for m in rc.get("mainQuests", [])]
    ok(quest_files == [gd["main_quest"]], f"gamedef mainQuests mismatch: {quest_files}")
    tags = [t["$value"] for t in rc.get("spawnPointTags", {}).get("tags", [])]
    ok(tags == gd["spawn_point_tags"], f"gamedef spawnPointTags mismatch: {tags}")
    ok(rc["world"]["DepotPath"]["$value"] == gd["world"], "gamedef world path mismatch")
    ok(rc["streamingWorld"]["DepotPath"]["$value"] == gd["streaming_world"], "gamedef streamingWorld path mismatch")
    ok(rc["worldName"] == gd["world_name"], "gamedef worldName mismatch")


def _check_quest(resources: dict[str, dict[str, Any]], spec: dict[str, Any], ok: Callable[[bool, str], None]) -> None:
    doc = resources["mod\\neon_ascendancy\\ascendancy.quest"]
    rc = doc["Data"]["RootChunk"]
    ok(rc.get("$type") == "questQuestResource", "quest root type is not questQuestResource")
    nodes = rc["graph"]["Data"]["nodes"]
    starts = [n for n in nodes if n["Data"].get("$type") == "questStartNodeDefinition"]
    ok(len(starts) == 1, f"quest has {len(starts)} start nodes")
    phases = [n for n in nodes if n["Data"].get("$type") == "questPhaseNodeDefinition"]
    ok(len(phases) == 1, f"quest has {len(phases)} phase nodes")
    if starts and phases:
        phase_paths = [n["Data"].get("phaseResource", {}).get("DepotPath", {}).get("$value") for n in phases]
        ok(phase_paths == [spec["quest"]["questphase"]], f"quest phaseResource mismatch: {phase_paths}")
        reachable = reachable_nodes(rc["graph"]["Data"]["nodes"], starts[0])
        ok(id_of(phases[0]) in reachable, "quest graph does not connect Start to the phase node")


def id_of(node: dict[str, Any]) -> int:
    return node["Data"].get("id")


def reachable_nodes(nodes: list[dict[str, Any]], start: dict[str, Any]) -> set[int]:
    """BFS over a graph's nodes following graphGraphConnectionDefinitions."""
    owner: dict[str, tuple[int, str]] = {}
    for node in nodes:
        d = node["Data"]
        for slot in d.get("sockets", []):
            h = slot.get("HandleId") or slot.get("HandleRefId")
            if h is not None:
                owner[str(h)] = (d.get("id"), d.get("$type"))

    def walk_conns(value: Any, edges: list[tuple[int, int]]) -> None:
        if isinstance(value, dict):
            if value.get("$type") == "graphGraphConnectionDefinition":
                src = value.get("source", {})
                dst = value.get("destination", {})
                s = str(src.get("HandleId") or src.get("HandleRefId"))
                t = str(dst.get("HandleId") or dst.get("HandleRefId"))
                if s in owner and t in owner:
                    edges.append((owner[s][0], owner[t][0]))
            for v in value.values():
                walk_conns(v, edges)
        elif isinstance(value, list):
            for v in value:
                walk_conns(v, edges)

    edges: list[tuple[int, int]] = []
    walk_conns(nodes, edges)
    adj: dict[int, set[int]] = {}
    for s, t in edges:
        adj.setdefault(s, set()).add(t)
        adj.setdefault(t, set())
    seen = {start["Data"]["id"]}
    frontier = [start["Data"]["id"]]
    while frontier:
        cur = frontier.pop()
        for nxt in adj.get(cur, ()):
            if nxt not in seen:
                seen.add(nxt)
                frontier.append(nxt)
    return seen


def _collect_phase_refs(rc: dict[str, Any]) -> list[str]:
    refs: list[str] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            if value.get("$type") == "questPhaseNodeDefinition":
                pr = value.get("phaseResource") or {}
                depot = pr.get("DepotPath", {}).get("$value")
                if depot and depot != "0":
                    refs.append(depot)
            for v in value.values():
                walk(v)
        elif isinstance(value, list):
            for v in value:
                walk(v)

    walk(rc)
    return refs


def _collect_setvar_facts(rc: dict[str, Any]) -> list[tuple[str, int]]:
    facts: list[tuple[str, int]] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            if value.get("$type") == "questSetVar_NodeType":
                facts.append((value.get("factName"), value.get("value")))
            for v in value.values():
                walk(v)
        elif isinstance(value, list):
            for v in value:
                walk(v)

    walk(rc)
    return facts


def _collect_nodes_of_type(rc: dict[str, Any], node_type: str) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            if value.get("$type") == node_type:
                found.append(value)
            for v in value.values():
                walk(v)
        elif isinstance(value, list):
            for v in value:
                walk(v)

    walk(rc)
    return found


def _socket_handle(slot: Any) -> str | None:
    if isinstance(slot, dict):
        h = slot.get("HandleId") or slot.get("HandleRefId")
        return str(h) if h is not None else None
    return None


def _count_connections(rc: dict[str, Any], socket_handle: str | None) -> tuple[int, int]:
    """(incoming, outgoing) connection counts for a socket handle across the whole resource."""
    n_in = 0
    n_out = 0

    def walk(value: Any) -> None:
        nonlocal n_in, n_out
        if isinstance(value, dict):
            if value.get("$type") == "graphGraphConnectionDefinition":
                src = value.get("source", {})
                dst = value.get("destination", {})
                s = str(src.get("HandleId") or src.get("HandleRefId")) if isinstance(src, dict) else ""
                t = str(dst.get("HandleId") or dst.get("HandleRefId")) if isinstance(dst, dict) else ""
                if socket_handle and t == socket_handle:
                    n_in += 1
                if socket_handle and s == socket_handle:
                    n_out += 1
            for v in value.values():
                walk(v)
        elif isinstance(value, list):
            for v in value:
                walk(v)

    walk(rc)
    return n_in, n_out


def _check_questphase(resources: dict[str, dict[str, Any]], spec: dict[str, Any], ok: Callable[[bool, str], None]) -> None:
    doc = resources["mod\\neon_ascendancy\\ascendancy.questphase"]
    rc = doc["Data"]["RootChunk"]
    qp = spec["questphase"]
    ok(rc.get("$type") == "questQuestPhaseResource", "questphase root type is not questQuestPhaseResource")

    nodes = rc["graph"]["Data"]["nodes"]
    inputs = [n for n in nodes if n["Data"].get("$type") == "questInputNodeDefinition"]
    ok(len(inputs) == 1, f"questphase has {len(inputs)} input nodes")
    if inputs:
        ok(inputs[0]["Data"]["socketName"]["$value"] == qp["entry_socket"],
           f"questphase input socketName != {qp['entry_socket']}")
        reachable = reachable_nodes(nodes, inputs[0])

        def by_type(t: str) -> list[dict[str, Any]]:
            return [n for n in nodes if n["Data"].get("$type") == t]

        expected_reachable = []
        hubs = by_type("questLogicalHubNodeDefinition")
        ok(len(hubs) == 1, f"expected 1 hub node, found {len(hubs)}")
        expected_reachable += hubs
        facts = by_type("questFactsDBManagerNodeDefinition")
        ok(len(facts) == len(qp["initial_facts"]),
           f"expected {len(qp['initial_facts'])} fact nodes, found {len(facts)}")
        expected_reachable += facts
        teles = by_type("questTeleportPuppetNodeDefinition")
        ok(len(teles) == 0, f"expected 0 blocking teleport nodes in questphase, found {len(teles)}")
        phases = by_type("questPhaseNodeDefinition")
        top_phase_nodes = [p for p in phases if p["Data"].get("phaseResource", {}).get("DepotPath", {}).get("$value") and p["Data"]["phaseResource"]["DepotPath"]["$value"] != "0"]
        ok(len(top_phase_nodes) == len(qp["kept_depot_phases"]) + 1,
           f"expected {len(qp['kept_depot_phases']) + 1} external phase nodes ({len(qp['kept_depot_phases'])} kept + spike), found {len(top_phase_nodes)}")
        expected_reachable += phases
        pause = by_type("questPauseConditionNodeDefinition")
        expected_reachable += pause
        unreachable = [n for n in expected_reachable if id_of(n) not in reachable]
        ok(not unreachable, f"nodes unreachable from Start: {[id_of(n) for n in unreachable]}")

        # strict graph integrity: zero duplicate HandleIds and zero cross-graph HandleRefIds
        dups = find_duplicate_handles(doc)
        ok(not dups, f"duplicate HandleIds in ascendancy.questphase: {dups[:10]}")
        cross = find_cross_graph_refs(doc)
        ok(not cross, f"cross-graph HandleRefIds in ascendancy.questphase: {cross[:10]}")

        # facts exactly match the spec, none forbidden
        actual_facts = _collect_setvar_facts(rc)
        expected_facts = [(f["fact"], f["value"]) for f in qp["initial_facts"]]
        ok(sorted(actual_facts) == sorted(expected_facts),
           f"setvar facts mismatch:\n  actual:   {sorted(actual_facts)}\n  expected: {sorted(expected_facts)}")
        forbidden = set(qp["forbidden_facts"])
        prefixes = tuple(qp["forbidden_fact_prefixes"])
        bad = [f for f, _ in actual_facts if f in forbidden or f.startswith(prefixes)]
        ok(not bad, f"forbidden story facts set: {bad}")

        # phase refs: kept present, excluded absent
        refs = _collect_phase_refs(rc)
        expected_refs = {e["depot_path"] for e in qp["kept_depot_phases"]} | set(qp["inline_phase_depot_refs"]) | {qp["spike"]["resource"]}
        missing = sorted(expected_refs - set(refs))
        ok(not missing, f"missing kept phase refs: {missing}")
        excluded = sorted({r for r in refs if any(p in r for p in qp["excluded_phase_patterns"])})
        ok(not excluded, f"excluded phase refs present: {excluded}")

        # spike gate wired: fan-out source (final fact node) -> gate pause -> spike phase node
        spike = qp["spike"]
        spike_ref = spike["resource"]
        spike_phase = [p for p in phases if p["Data"].get("phaseResource", {}).get("DepotPath", {}).get("$value") == spike_ref]
        ok(len(spike_phase) == 1, f"expected 1 spike phase node, found {len(spike_phase)}")
        gate_pauses = []
        for p in pause:
            cond = p["Data"].get("condition", {}).get("Data", {})
            typ = cond.get("type", {})
            if isinstance(typ, dict):
                typ = typ.get("Data", {})
            if (typ.get("factName") == spike["gate"]["fact"] and typ.get("comparisonType") == spike["gate"]["comparison_type"]
                    and typ.get("value") == spike["gate"]["value"]):
                gate_pauses.append(p)
        ok(len(gate_pauses) == 1, f"expected 1 spike gate pause condition, found {len(gate_pauses)}")
        if gate_pauses and spike_phase and facts:
            gate_id = id_of(gate_pauses[0])
            spike_id = id_of(spike_phase[0])
            fan_id = id_of(facts[-1])
            edges = _graph_edges(nodes)
            ok((fan_id, gate_id) in edges, "final fact node is not connected to the spike gate pause")
            ok((gate_id, spike_id) in edges, "spike gate pause is not connected to the spike phase node")
            gate = gate_pauses[0]["Data"]
            gate_in = _socket_handle(gate["sockets"][1])
            gate_out = _socket_handle(gate["sockets"][2])
            ok(_count_connections(rc, gate_in) == (1, 0), "spike gate In must have exactly 1 incoming connection")
            ok(_count_connections(rc, gate_out) == (0, 1), "spike gate Out must have exactly 1 outgoing connection")

        # NCPD PreventionSystem inline copy ([8]): 36 trigger areas + 36 event managers
        event_managers = _collect_nodes_of_type(rc, "questEventManagerNodeDefinition")
        prevention = [m for m in event_managers if m.get("managerName") == "PreventionSystem"]
        ok(len(prevention) == 36, f"expected 36 PreventionSystem event managers, found {len(prevention)}")
        ok(len(_collect_nodes_of_type(rc, "questTriggerCondition")) == 36,
           "expected 36 PreventionSystem trigger conditions")

        # [142] kept cleanly unmodified (no cross-graph wire into its nested phaseGraph)
        lock_zero_pauses = []
        for p in _collect_nodes_of_type(rc, "questPauseConditionNodeDefinition"):
            cond = p.get("condition", {}).get("Data", {})
            typ = cond.get("type", {})
            if isinstance(typ, dict):
                typ = typ.get("Data", {})
            if isinstance(typ, dict) and typ.get("factName") == "watson_prolog_lock" and typ.get("comparisonType") == "Equal" and typ.get("value") == 0:
                lock_zero_pauses.append(p)
        ok(len(lock_zero_pauses) == 1, f"expected 1 watson_prolog_lock == 0 pause gate, found {len(lock_zero_pauses)}")
        if lock_zero_pauses:
            pz = lock_zero_pauses[0]
            in_h = _socket_handle(pz["sockets"][1])
            n_in, _ = _count_connections(rc, in_h)
            ok(n_in == 1, f"watson_prolog_lock == 0 pause gate has {n_in} incoming connections (expected 1: vanilla AND chain)")


def _graph_edges(nodes: list[dict[str, Any]]) -> set[tuple[int, int]]:
    owner: dict[str, int] = {}
    for node in nodes:
        d = node["Data"]
        for slot in d.get("sockets", []):
            h = slot.get("HandleId") or slot.get("HandleRefId")
            if h is not None:
                owner[str(h)] = d.get("id")

    edges: set[tuple[int, int]] = set()

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            if value.get("$type") == "graphGraphConnectionDefinition":
                src = value.get("source", {})
                dst = value.get("destination", {})
                s = str(src.get("HandleId") or src.get("HandleRefId"))
                t = str(dst.get("HandleId") or dst.get("HandleRefId"))
                if s in owner and t in owner:
                    edges.add((owner[s], owner[t]))
            for v in value.values():
                walk(v)
        elif isinstance(value, list):
            for v in value:
                walk(v)

    walk(nodes)
    return edges


def _check_spike(resources: dict[str, dict[str, Any]], spec: dict[str, Any], ok: Callable[[bool, str], None]) -> None:
    doc = resources["mod\\neon_ascendancy\\spike_kab07.questphase"]
    rc = doc["Data"]["RootChunk"]
    spike = spec["questphase"]["spike"]
    ok(rc.get("$type") == "questQuestPhaseResource", "spike root type is not questQuestPhaseResource")

    prefab_refs = [e["prefabNodeRef"]["$value"] for e in rc.get("phasePrefabs", [])]
    ok(prefab_refs == spike["phase_prefabs"],
       f"spike phasePrefabs mismatch: {prefab_refs}")

    nodes = rc["graph"]["Data"]["nodes"]
    inputs = [n for n in nodes if n["Data"].get("$type") == "questInputNodeDefinition"]
    ok(len(inputs) == 1, f"spike has {len(inputs)} input nodes")
    if inputs:
        ok(inputs[0]["Data"]["socketName"]["$value"] == spike["entry_socket"],
           f"spike input socketName != {spike['entry_socket']}")
    spawns = [n for n in nodes if n["Data"].get("$type") == "questSpawnManagerNodeDefinition"]
    ok(len(spawns) == 1, f"spike has {len(spawns)} spawn manager nodes")
    if spawns:
        reachable = reachable_nodes(nodes, inputs[0]) if inputs else set()
        ok(id_of(spawns[0]) in reachable, "spike input does not connect to the spawn manager")
        actions = spawns[0]["Data"].get("actions", [])
        ok(len(actions) == 1, f"spike spawn manager has {len(actions)} actions")
        if actions:
            a = actions[0]["type"]["Data"]
            ok(a.get("$type") == "questCommunityTemplate_NodeType", "spike action type mismatch")
            ok(a.get("action") == spike["spawn_manager"]["action"], "spike action mismatch")
            ok(a.get("spawnerReference", {}).get("$value") == spike["spawn_manager"]["spawner_reference"],
               "spike spawnerReference mismatch")
            ok(a.get("communityEntryPhaseName", {}).get("$value") == spike["spawn_manager"]["community_entry_phase_name"],
               "spike communityEntryPhaseName mismatch")


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="Build/verify the Clean-Slate Night City world archive.")
    ap.add_argument("--check", action="store_true", help="Verify the packed archive instead of building.")
    ap.add_argument("--wk-cli", type=Path, default=DEFAULT_WK, help=f"WolvenKit.CLI path (default {DEFAULT_WK})")
    ap.add_argument("--game-dir", type=Path, default=DEFAULT_GAME_DIR,
                    help=f"Cyberpunk 2077 root (default {DEFAULT_GAME_DIR})")
    ap.add_argument("--spec", type=Path, default=SPEC_PATH, help=f"spec JSON (default {SPEC_PATH})")
    args = ap.parse_args()

    if not args.spec.is_file():
        raise FileNotFoundError(f"missing spec: {args.spec}")
    with args.spec.open("r", encoding="utf-8") as fh:
        spec = json.load(fh)

    if args.check:
        check(args, spec)
    else:
        archive = build(args, spec)
        print(f"\nBuilt {archive} ({archive.stat().st_size} bytes).")
        print("Run `python3 tools/build-clean-slate.py --check` to verify the round-trip.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
