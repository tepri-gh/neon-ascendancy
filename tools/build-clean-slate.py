#!/usr/bin/env python3
"""Build the Clean-Slate Night City world archive for Neon Ascendancy.

Reads the declarative specs `data/clean-slate/clean_slate_spec.json` and
`data/clean-slate/cast_and_hubs.json`, and produces
`dist/neon_ascendancy_world.archive` containing five CR2W resources:

  mod\\neon_ascendancy\\ascendancy.gamedef      (custom gsmGameDefinition)
  mod\\neon_ascendancy\\ascendancy.quest        (Start -> ascendancy.questphase)
  mod\\neon_ascendancy\\ascendancy.questphase   (clean-slate hub graph)
  mod\\neon_ascendancy\\cast_and_hubs.questphase (world cast, hubs & direct service vendors)
  mod\\neon_ascendancy\\spike_kab07.questphase  (dormant fact-gated living-world spike)

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
                    elif k == "HandleRefId" and isinstance(item, str):
                        if item not in remap:
                            raise ValueError(f"unmapped external HandleRefId {item} in renumbered subtree")
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

    def add_proximity_pause_node(
        self,
        node_ref: str,
        within: float,
    ) -> tuple[str, str]:
        """Add a questPauseConditionNodeDefinition that waits until the player is
        within `within` metres of `node_ref`.

        Schema matches vanilla ep1\\quest\\main_quests\\q304\\q304.questphase: a
        questDistanceCondition wrapping questDistanceComparison_ConditionType with
        distanceDefinition1 = questObjectDistance (refLocalPlayer=1, nodeRef2 =
        the authored node) and distanceDefinition2 = questValueDistance. This is
        the vanilla-native way to defer a phase's device actions until the venue
        streams in near the player, instead of firing them at bootstrap."""
        cut = self.new_socket("CutDestination", "CutDestination")
        inp = self.new_socket("In", "Input")
        out = self.new_socket("Out", "Output")
        player_ref = {
            "$type": "gameEntityReference",
            "dynamicEntityUniqueName": cname("None"),
            "names": [],
            "reference": {"$type": "NodeRef", "$storage": "uint64", "$value": "0"},
            "sceneActorContextName": cname("None"),
            "slotName": cname("None"),
            "type": "EntityRef",
        }
        self.nodes.append(
            {
                "HandleId": self.alloc(),
                "Data": {
                    "$type": "questPauseConditionNodeDefinition",
                    "id": self.node_id(),
                    "condition": {
                        "HandleId": self.alloc(),
                        "Data": {
                            "$type": "questDistanceCondition",
                            "type": {
                                "HandleId": self.alloc(),
                                "Data": {
                                    "$type": "questDistanceComparison_ConditionType",
                                    "comparisonType": "Less",
                                    "distanceDefinition1": {
                                        "HandleId": self.alloc(),
                                        "Data": {
                                            "$type": "questObjectDistance",
                                            "entityRef": {
                                                "HandleId": self.alloc(),
                                                "Data": {
                                                    "$type": "questUniversalRef",
                                                    "entityReference": player_ref,
                                                    "mainPlayerObject": 0,
                                                    "refLocalPlayer": 1,
                                                },
                                            },
                                            "nodeRef2": {
                                                "$type": "gameEntityReference",
                                                "dynamicEntityUniqueName": cname("None"),
                                                "names": [],
                                                "reference": noderef(node_ref),
                                                "sceneActorContextName": cname("None"),
                                                "slotName": cname("None"),
                                                "type": "EntityRef",
                                            },
                                        },
                                    },
                                    "distanceDefinition2": {
                                        "HandleId": self.alloc(),
                                        "Data": {
                                            "$type": "questValueDistance",
                                            "distanceValue": int(round(within)),
                                        },
                                    },
                                },
                            },
                        },
                    },
                    "_sockets": [cut, inp, out],
                },
            }
        )
        return inp, out

    def add_register_fast_travel_points_node(self, points: list[dict[str, Any]]) -> tuple[str, str]:
        """Add a questEventManagerNodeDefinition (RegisterFastTravelPointsRequest).

        Schema matches vanilla
        base\\open_world\\fast_travel\\open_world_fast_travel.questphase node 16
        field-for-field, except that the request carries every point in one list
        (vanilla registers one point per node)."""
        cut = self.new_socket("CutDestination", "CutDestination")
        inp = self.new_socket("In", "Input")
        out = self.new_socket("Out", "Output")
        fast_travel_nodes = [
            {
                "HandleId": self.alloc(),
                "Data": {
                    "$type": "gameFastTravelPointData",
                    "isEP1": p["is_ep1"],
                    "mappinID": {"$type": "gameNewMappinID", "value": "0"},
                    "markerRef": noderef(p["marker_ref"]),
                    "pointRecord": {"$type": "TweakDBID", "$storage": "string", "$value": p["point_record"]},
                    "requesterID": {"$type": "entEntityID", "hash": "0"},
                },
            }
            for p in points
        ]
        self.nodes.append(
            {
                "HandleId": self.alloc(),
                "Data": {
                    "$type": "questEventManagerNodeDefinition",
                    "componentName": cname("None"),
                    "event": {
                        "HandleId": self.alloc(),
                        "Data": {
                            "$type": "RegisterFastTravelPointsRequest",
                            "fastTravelNodes": fast_travel_nodes,
                            "register": 1,
                        },
                    },
                    "id": self.node_id(),
                    "isObjectPlayer": 0,
                    "isUiEvent": 0,
                    "managerName": "FastTravelSystem",
                    "objectRef": {
                        "$type": "gameEntityReference",
                        "dynamicEntityUniqueName": cname("None"),
                        "names": [],
                        "reference": {"$type": "NodeRef", "$storage": "uint64", "$value": "0"},
                        "sceneActorContextName": cname("None"),
                        "slotName": cname("None"),
                        "type": "EntityRef",
                    },
                    "PSClassName": cname("None"),
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

    def add_community_spawn_node(
        self,
        template: dict[str, Any],
        action: str,
        spawner_reference: str,
        entry_name: str,
        phase_name: str,
    ) -> tuple[str, str]:
        """Add a questSpawnManagerNodeDefinition (questCommunityTemplate_NodeType)."""
        raw = json.loads(json.dumps(template))
        raw.pop("sockets", None)
        data = self.renumber(raw)
        data["id"] = self.node_id()
        for act in data.get("actions", []):
            act_type = act["type"]["Data"]
            act_type["action"] = action
            act_type["spawnerReference"]["$value"] = spawner_reference
            act_type["communityEntryName"]["$value"] = entry_name
            act_type["communityEntryPhaseName"]["$value"] = phase_name
        cut = self.new_socket("CutDestination", "CutDestination")
        inp = self.new_socket("In", "Input")
        out = self.new_socket("Out", "Output")
        data["_sockets"] = [cut, inp, out]
        self.nodes.append({"HandleId": self.alloc(), "Data": data})
        return inp, out

    def add_spawn_set_node(
        self,
        action: str,
        reference: str,
        entry_name: str,
        phase_name: str,
    ) -> tuple[str, str]:
        """Add a questSpawnManagerNodeDefinition (questSpawnSet_NodeType).
        Schema matches vanilla wakako.questphase node 17 field-for-field."""
        cut = self.new_socket("CutDestination", "CutDestination")
        inp = self.new_socket("In", "Input")
        out = self.new_socket("Out", "Output")
        self.nodes.append(
            {
                "HandleId": self.alloc(),
                "Data": {
                    "$type": "questSpawnManagerNodeDefinition",
                    "actions": [
                        {
                            "$type": "questSpawnManagerNodeActionEntry",
                            "type": {
                                "HandleId": self.alloc(),
                                "Data": {
                                    "$type": "questSpawnSet_NodeType",
                                    "action": action,
                                    "entryName": cname(entry_name),
                                    "phaseName": cname(phase_name),
                                    "reference": noderef(reference),
                                },
                            },
                        }
                    ],
                    "id": self.node_id(),
                    "_sockets": [cut, inp, out],
                },
            }
        )
        return inp, out

    def add_spawner_node(self, action: str, refs: list[str]) -> tuple[str, str]:
        """Add a questSpawnManagerNodeDefinition (questSpawner_NodeType).

        Schema matches vanilla
        base\\open_world\\phases\\prolog_roadblocks\\lch_prolog_roadblocks.questphase
        field-for-field: one questSpawnManagerNodeActionEntry per ref, each a
        questSpawner_NodeType with `action` and `spawnerReference` (NOT the
        questSpawnSet_NodeType `reference`/`entryName`/`phaseName` shape). Used to
        Deactivate the prologue roadblock vehicle spawners."""
        cut = self.new_socket("CutDestination", "CutDestination")
        inp = self.new_socket("In", "Input")
        out = self.new_socket("Out", "Output")
        self.nodes.append(
            {
                "HandleId": self.alloc(),
                "Data": {
                    "$type": "questSpawnManagerNodeDefinition",
                    "actions": [
                        {
                            "$type": "questSpawnManagerNodeActionEntry",
                            "type": {
                                "HandleId": self.alloc(),
                                "Data": {
                                    "$type": "questSpawner_NodeType",
                                    "action": action,
                                    "spawnerReference": noderef(ref),
                                },
                            },
                        }
                        for ref in refs
                    ],
                    "id": self.node_id(),
                    "_sockets": [cut, inp, out],
                },
            }
        )
        return inp, out

    def add_device_manager_node(self, entries: list[dict[str, Any]]) -> tuple[str, str]:
        """Add a questInteractiveObjectManagerNodeDefinition (questDeviceManager_NodeType).

        Schema matches vanilla
        base\\open_world\\street_stories\\watson\\kabuki\\sts_wat_kab_07\\phase\\sts_wat_kab_07_openworld.questphase
        (node id 9) field-for-field. Each entry is:
          {"ref": "#node_ref", "controller": "DoorControllerPS", "action": "ForcePower"}
        The authored ref goes into `objectRef` (vanilla puts the full authored path
        or the short '#'-ref there; `entityRef.reference` stays "0")."""
        cut = self.new_socket("CutDestination", "CutDestination")
        inp = self.new_socket("In", "Input")
        out = self.new_socket("Out", "Output")
        params = [
            {
                "HandleId": self.alloc(),
                "Data": {
                    "$type": "questDeviceManager_NodeTypeParams",
                    "actionProperties": [],
                    "deviceAction": cname(e["action"]),
                    "deviceControllerClass": cname(e["controller"]),
                    "entityRef": {
                        "$type": "gameEntityReference",
                        "dynamicEntityUniqueName": cname("None"),
                        "names": [],
                        "reference": {"$type": "NodeRef", "$storage": "uint64", "$value": "0"},
                        "sceneActorContextName": cname("None"),
                        "slotName": cname("None"),
                        "type": "EntityRef",
                    },
                    "objectRef": noderef(e["ref"]),
                    "slotName": cname("None"),
                },
            }
            for e in entries
        ]
        self.nodes.append(
            {
                "HandleId": self.alloc(),
                "Data": {
                    "$type": "questInteractiveObjectManagerNodeDefinition",
                    "id": self.node_id(),
                    "_sockets": [cut, inp, out],
                    "type": {
                        "HandleId": self.alloc(),
                        "Data": {
                            "$type": "questDeviceManager_NodeType",
                            "params": params,
                        },
                    },
                },
            }
        )
        return inp, out

    def add_variant_toggle_node(self, prefab_ref: str, states: dict[str, int]) -> tuple[str, str]:
        """Add a questWorldDataManagerNodeDefinition (questTogglePrefabVariant_NodeType).

        Schema matches vanilla
        ep1\\quest\\main_quests\\q303\\phases\\q303_06b_paradise_technical.questphase
        field-for-field. `prefab_ref` is an authored '#name' prefab; `states` maps a
        variant name to 1 (show) or 0 (hide). This is how a venue phase swaps a
        closed prefab state (e.g. var_tower_gate_closed_default) for an open one
        (var_tower_gate_open_indestructible) - the only way to change baked
        geometry, which no door action can move."""
        cut = self.new_socket("CutDestination", "CutDestination")
        inp = self.new_socket("In", "Input")
        out = self.new_socket("Out", "Output")
        self.nodes.append(
            {
                "HandleId": self.alloc(),
                "Data": {
                    "$type": "questWorldDataManagerNodeDefinition",
                    "id": self.node_id(),
                    "_sockets": [cut, inp, out],
                    "type": {
                        "HandleId": self.alloc(),
                        "Data": {
                            "$type": "questTogglePrefabVariant_NodeType",
                            "params": [
                                {
                                    "$type": "questTogglePrefabVariant_NodeTypeParams",
                                    "prefabNodeRef": noderef(prefab_ref),
                                    "variantStates": [
                                        {"$type": "questVariantState", "name": cname(name), "show": show}
                                        for name, show in states.items()
                                    ],
                                }
                            ],
                        },
                    },
                },
            }
        )
        return inp, out

    def add_renumbered_inline_phase_node(
        self,
        vanilla_node: dict[str, Any],
        input_socket_name: str = "In1",
    ) -> str:
        """Clone a self-contained vanilla inline questPhaseNodeDefinition into this graph.
        Strips outer sockets so zero parent-graph connections leak, renumbers all internal
        handles, and attaches fresh CutDestination + input sockets."""
        raw = json.loads(json.dumps(vanilla_node))
        raw.pop("sockets", None)
        data = self.renumber(raw)
        data["id"] = self.node_id()
        cut = self.new_socket("CutDestination", "CutDestination")
        inp = self.new_socket(input_socket_name, "Input")
        data["_sockets"] = [cut, inp]
        self.nodes.append({"HandleId": self.alloc(), "Data": data})
        return inp

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


def build_questphase(
    templates: dict[str, dict[str, Any]],
    spec: dict[str, Any],
    cast_spec: dict[str, Any],
    venue_spec: dict[str, Any],
    barricade_spec: dict[str, Any],
    vendors_spec: dict[str, Any],
    tower_spec: dict[str, Any],
) -> dict[str, Any]:
    """Assemble the clean-slate hub questphase.

    Start -> hub -> initial + service-vendor fact managers (chained) -> fan-out to:
      cast_and_hubs phase + barricade cleanup phase + kept external phases
      + spike gate pause -> spike phase + venue gate pause -> venue probe phase
      + 5 copied inline phases.
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

    all_facts = list(qp["initial_facts"]) + list(cast_spec["service_vendors"]["vendor_facts"])
    seen_facts: set[str] = set()
    prev_out = hub_out
    for entry in all_facts:
        fname = entry["fact"]
        if fname in seen_facts:
            raise ValueError(f"duplicate initial/vendor fact {fname}")
        seen_facts.add(fname)
        f_in, f_out = g.add_fact_node(fname, entry["value"])
        g.connect(prev_out, f_in)
        prev_out = f_out

    # Fan-out directly from the final fact node (zero blocking teleport nodes).
    fan = prev_out

    # World Cast & Hubs layer (wired directly off fan-out after all facts are set)
    cast_phase_in = g.add_phase_node(cast_spec["phase_resource"])
    g.connect(fan, cast_phase_in)

    # Always-on Watson lockdown cleanup (NOT dev-gated): hide the q001 bridge
    # blockade variant, hide the prologue security/geometry variants, and
    # deactivate the roadblock communities + vehicle spawners, exactly as the
    # skipped watson_prolog_lock == 0 cleanup branches do.
    cleanup_phase_in = g.add_phase_node(barricade_spec["phase_resource"])
    g.connect(fan, cleanup_phase_in)

    # Dogtown vendor population: gate pause on the narrow per-vendor fact, then
    # the phase that re-activates the vendor spawn sets/communities without
    # ep1_vendors' ep1_side_content / q302_started gates.
    vgate = vendors_spec["gate"]
    vg_in, vg_out = g.add_pause_fact_node(vgate["fact"], vgate["comparison_type"], vgate["value"])
    g.connect(fan, vg_in)
    vendors_phase_in = g.add_phase_node(vendors_spec["phase_resource"])
    g.connect(vg_out, vendors_phase_in)

    # Black Sapphire tower population (always on): lobby, floor-67 and floor-99
    # communities with default/idle/guard entry phases only.
    tower_phase_in = g.add_phase_node(tower_spec["phase_resource"])
    g.connect(fan, tower_phase_in)

    # spike: gate pause -> spike phase node
    spike = qp["spike"]
    sp_in, sp_out = g.add_pause_fact_node(
        spike["gate"]["fact"], spike["gate"]["comparison_type"], spike["gate"]["value"]
    )
    g.connect(fan, sp_in)
    spike_phase_in = g.add_phase_node(spike["resource"])
    g.connect(sp_out, spike_phase_in)

    # venue probe: gate pause -> venue probe phase node. Gated on the runtime
    # dev fact so the probe stays dormant unless DevDebug sets it.
    venue_gate = venue_spec["gate"]
    vp_in, vp_out = g.add_pause_fact_node(
        venue_gate["fact"], venue_gate["comparison_type"], venue_gate["value"]
    )
    g.connect(fan, vp_in)
    venue_phase_in = g.add_phase_node(venue_spec["phase_resource"])
    g.connect(vp_out, venue_phase_in)

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


def build_cast_and_hubs(
    templates: dict[str, dict[str, Any]],
    cast_spec: dict[str, Any],
    ft_spec: dict[str, Any],
) -> dict[str, Any]:
    """Assemble mod\\neon_ascendancy\\cast_and_hubs.questphase.

    In1 -> hub -> fan-out to:
      - world_hubs community activations (questCommunityTemplate_NodeType)
      - overhaul_actors spawn sets (questSpawnSet_NodeType; 7 fixers + 10 iconic residents)
      - direct_vendor_phases cloned cleanly from default_dialogs.questphase (plus any spawn_set)
      - keep-alive pause condition (always-false fact, zero Output nodes -> phase never terminates)
      - dev fast-travel gate pause -> RegisterFastTravelPointsRequest (only when
        DevDebug.reds flips na_dev_unlock_all_ft; never set by the archive itself)
    RootChunk.phasePrefabs owns the 11 required workspot prefabs.
    """
    spawn_tpl = templates["spawn_manager_node"]
    default_dialogs = templates["default_dialogs_questphase"]

    g = QuestGraph(start_handle=1)
    start_out = g.add_input_node(cast_spec["entry_socket"])
    hub_in, hub_out = g.add_hub_node()
    g.connect(start_out, hub_in)

    # 1. Gated district hub crowds (questCommunityTemplate_NodeType)
    for hub in cast_spec["world_hubs"]:
        inp, _ = g.add_community_spawn_node(
            spawn_tpl,
            action="Activate",
            spawner_reference=hub["spawner_reference"],
            entry_name=hub["community_entry_name"],
            phase_name=hub["community_entry_phase_name"],
        )
        g.connect(hub_out, inp)

    # 2. Overhaul actors (7 fixers + 10 iconic hub/faction residents; questSpawnSet_NodeType)
    for actor in cast_spec["overhaul_actors"]:
        inp, _ = g.add_spawn_set_node(
            action="Activate",
            reference=actor["reference"],
            entry_name=actor["entry_name"],
            phase_name=actor["phase_name"],
        )
        g.connect(hub_out, inp)

    # 3. Direct service-vendor phases cloned from default_dialogs.questphase
    for vendor in cast_spec["service_vendors"]["direct_vendor_phases"]:
        if "spawn_set" in vendor:
            ss = vendor["spawn_set"]
            ss_in, _ = g.add_spawn_set_node(
                action="Activate",
                reference=ss["reference"],
                entry_name=ss["entry_name"],
                phase_name=ss["phase_name"],
            )
            g.connect(hub_out, ss_in)
        vanilla = find_node_by_id_path(default_dialogs, vendor["default_dialogs_id_path"])["Data"]
        p_in = g.add_renumbered_inline_phase_node(vanilla, input_socket_name="In1")
        g.connect(hub_out, p_in)

    # 4. Keep-alive pause (never fires; keeps phasePrefabs and questSpawnSet entries active forever)
    ka = cast_spec["keep_alive_pause"]
    ka_in, _ = g.add_pause_fact_node(ka["fact"], ka["comparison_type"], ka["value"])
    g.connect(hub_out, ka_in)

    # 5. Dev fast-travel registration, gated on the runtime dev-debug fact.
    # The archive never sets na_dev_unlock_all_ft itself; only DevDebug.reds does.
    ft_gate = ft_spec["gate"]
    ft_in, ft_out = g.add_pause_fact_node(
        ft_gate["fact"], ft_gate["comparison_type"], ft_gate["value"]
    )
    g.connect(hub_out, ft_in)
    reg_in, _ = g.add_register_fast_travel_points_node(ft_spec["points"])
    g.connect(ft_out, reg_in)

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
            "phasePrefabs": [
                {
                    "$type": "questQuestPrefabEntry",
                    "prefabNodeRef": noderef(entry["prefab"]),
                }
                for entry in cast_spec["phase_prefabs"]
            ],
        }
    )
    dups = find_duplicate_handles(doc)
    if dups:
        raise ValueError(f"duplicate HandleIds in cast_and_hubs.questphase: {dups[:5]}")
    cross = find_cross_graph_refs(doc)
    if cross:
        raise ValueError(f"cross-graph HandleRefIds in cast_and_hubs.questphase: {cross[:5]}")
    return doc


def build_spike(templates: dict[str, dict[str, Any]], spec: dict[str, Any]) -> dict[str, Any]:
    """Dormant fact-gated living-world spike resource (phasePrefabs + spawn manager)."""
    spike = spec["questphase"]["spike"]
    template = templates["spawn_manager_node"]

    g = QuestGraph(start_handle=1)

    start_out = g.add_input_node(spike["entry_socket"])
    inp, _ = g.add_community_spawn_node(
        template,
        action=spike["spawn_manager"]["action"],
        spawner_reference=spike["spawn_manager"]["spawner_reference"],
        entry_name=spike["spawn_manager"]["community_entry_name"],
        phase_name=spike["spawn_manager"]["community_entry_phase_name"],
    )
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


def find_node_by_id_path(resource: dict[str, Any], id_path: list[int]) -> dict[str, Any]:
    """Locate a nested node inside inline questPhaseNodeDefinition phaseGraphs by id path."""
    if not id_path:
        raise ValueError("empty id_path")
    nodes = resource["Data"]["RootChunk"]["graph"]["Data"]["nodes"]
    found: dict[str, Any] | None = None
    for depth, nid in enumerate(id_path):
        found = next((n for n in nodes if n["Data"].get("id") == nid), None)
        if found is None:
            raise KeyError(f"node id {nid} not found at depth {depth} of path {id_path}")
        if depth + 1 < len(id_path):
            pg = found["Data"].get("phaseGraph")
            if not isinstance(pg, dict) or "Data" not in pg:
                raise KeyError(f"node id {nid} at depth {depth} has no inline phaseGraph")
            nodes = pg["Data"]["nodes"]
    assert found is not None
    return found


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
        tpl["default_dialogs_questphase"],
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
    default_dialogs = load(tpl["default_dialogs_questphase"])
    spawn_resource = load(tpl["spawn_manager_node_template"])
    return {
        "gamedef": gamedef,
        "quest": quest,
        "open_world_content_questphase": owc,
        "default_dialogs_questphase": default_dialogs,
        "spawn_manager_node": find_first_node_of_type(spawn_resource, "questSpawnManagerNodeDefinition"),
    }


def load_cast_spec(spec: dict[str, Any]) -> dict[str, Any]:
    cast_path = ROOT / spec["questphase"]["cast_and_hubs"]["spec"]
    if not cast_path.is_file():
        raise FileNotFoundError(f"missing cast_and_hubs spec: {cast_path}")
    with cast_path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def load_barricade_spec(cast_spec: dict[str, Any]) -> dict[str, Any]:
    """Load + validate the always-on Watson lockdown cleanup spec.

    Enforces the doc's constraint that this group only ever hides story
    prologue variants, deactivates prologue roadblock communities, and
    deactivates prologue roadblock spawners - never anything story/journalled."""
    path = ROOT / cast_spec["barricade_cleanup_spec"]
    if not path.is_file():
        raise FileNotFoundError(f"missing barricade cleanup spec: {path}")
    with path.open("r", encoding="utf-8") as fh:
        spec = json.load(fh)

    if not spec.get("phase_resource"):
        raise ValueError(f"{path}: phase_resource is required")
    for t in spec.get("variant_toggles", []):
        if not t.get("prefab"):
            raise ValueError(f"{path}: variant toggle needs a prefab")
        if not isinstance(t.get("states"), dict) or not t["states"]:
            raise ValueError(f"{path}: variant toggle needs a non-empty states map")
        for name, show in t["states"].items():
            if show not in (0, 1):
                raise ValueError(f"{path}: variant {name} show must be 0 or 1")
    for c in spec.get("communities", []):
        if not c.get("spawner", "").startswith("#"):
            raise ValueError(f"{path}: bad community spawner {c}")
    for s in spec.get("spawners", []):
        if not s.get("ref", "").startswith("#"):
            raise ValueError(f"{path}: bad spawner ref {s}")
    for s in spec.get("probe_spawners", []):
        if not s.get("ref", "").startswith("#"):
            raise ValueError(f"{path}: bad probe spawner ref {s}")
    return spec


def build_barricade_cleanup(spec: dict[str, Any], templates: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Assemble mod\\neon_ascendancy\\barricade_cleanup.questphase.

    In1 -> hub -> variant toggles -> community deactivations -> spawner
    deactivations -> keep-alive pause. Mirrors the watson_prolog_lock == 0
    cleanup branches of the three prolog roadblock phases plus q001 node 230."""
    spawn_tpl = templates["spawn_manager_node"]

    g = QuestGraph(start_handle=1)
    start_out = g.add_input_node(spec["entry_socket"])
    hub_in, hub_out = g.add_hub_node()
    g.connect(start_out, hub_in)

    prev = hub_out
    for toggle in spec.get("variant_toggles", []):
        inp, out = g.add_variant_toggle_node(toggle["prefab"], toggle["states"])
        g.connect(prev, inp)
        prev = out
    for com in spec.get("communities", []):
        inp, out = g.add_community_spawn_node(
            spawn_tpl,
            action="Deactivate",
            spawner_reference=com["spawner"],
            entry_name="None",
            phase_name="None",
        )
        g.connect(prev, inp)
        prev = out
    if spec.get("spawners"):
        inp, out = g.add_spawner_node("Deactivate", [s["ref"] for s in spec["spawners"]])
        g.connect(prev, inp)
        prev = out

    ka = spec["keep_alive_pause"]
    ka_in, _ = g.add_pause_fact_node(ka["fact"], ka["comparison_type"], ka["value"])
    g.connect(hub_out, ka_in)

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
    dups = find_duplicate_handles(doc)
    if dups:
        raise ValueError(f"duplicate HandleIds in barricade_cleanup.questphase: {dups[:5]}")
    cross = find_cross_graph_refs(doc)
    if cross:
        raise ValueError(f"cross-graph HandleRefIds in barricade_cleanup.questphase: {cross[:5]}")
    return doc


def load_dogtown_vendors_spec(cast_spec: dict[str, Any]) -> dict[str, Any]:
    """Load + validate the always-on Dogtown vendor population spec."""
    path = ROOT / cast_spec["dogtown_vendors_spec"]
    if not path.is_file():
        raise FileNotFoundError(f"missing dogtown vendors spec: {path}")
    with path.open("r", encoding="utf-8") as fh:
        spec = json.load(fh)
    if not spec.get("phase_resource"):
        raise ValueError(f"{path}: phase_resource is required")
    for ss in spec.get("spawn_sets", []):
        if not ss.get("ref", "").startswith("#"):
            raise ValueError(f"{path}: bad spawn_set ref {ss}")
        if not ss.get("entry_name") or not ss.get("phase_name"):
            raise ValueError(f"{path}: spawn_set needs entry_name and phase_name: {ss}")
    for c in spec.get("communities", []):
        if not c.get("spawner", "").startswith("#"):
            raise ValueError(f"{path}: bad community spawner {c}")
    gate = spec.get("gate", {})
    if not gate.get("fact"):
        raise ValueError(f"{path}: gate.fact is required")
    return spec


def build_dogtown_vendors(spec: dict[str, Any], templates: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Assemble mod\\neon_ascendancy\\dogtown_vendors.questphase.

    In1 -> hub -> spawn-set activations -> community activations -> keep-alive
    pause. No journal/scene nodes; the story gate pauses are dropped."""
    spawn_tpl = templates["spawn_manager_node"]
    g = QuestGraph(start_handle=1)
    start_out = g.add_input_node(spec["entry_socket"])
    hub_in, hub_out = g.add_hub_node()
    g.connect(start_out, hub_in)

    prev = hub_out
    for ss in spec.get("spawn_sets", []):
        inp, out = g.add_spawn_set_node(
            action="Activate",
            reference=ss["ref"],
            entry_name=ss["entry_name"],
            phase_name=ss["phase_name"],
        )
        g.connect(prev, inp)
        prev = out
    for com in spec.get("communities", []):
        inp, out = g.add_community_spawn_node(
            spawn_tpl,
            action="Activate",
            spawner_reference=com["spawner"],
            entry_name=com.get("entry_name", "None"),
            phase_name=com.get("phase_name", "None"),
        )
        g.connect(prev, inp)
        prev = out

    ka = spec["keep_alive_pause"]
    ka_in, _ = g.add_pause_fact_node(ka["fact"], ka["comparison_type"], ka["value"])
    g.connect(hub_out, ka_in)

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
    dups = find_duplicate_handles(doc)
    if dups:
        raise ValueError(f"duplicate HandleIds in dogtown_vendors.questphase: {dups[:5]}")
    cross = find_cross_graph_refs(doc)
    if cross:
        raise ValueError(f"cross-graph HandleRefIds in dogtown_vendors.questphase: {cross[:5]}")
    return doc


def load_tower_population_spec(cast_spec: dict[str, Any]) -> dict[str, Any]:
    """Load + validate the always-on Black Sapphire tower population spec."""
    path = ROOT / cast_spec["tower_population_spec"]
    if not path.is_file():
        raise FileNotFoundError(f"missing tower population spec: {path}")
    with path.open("r", encoding="utf-8") as fh:
        spec = json.load(fh)
    if not spec.get("phase_resource"):
        raise ValueError(f"{path}: phase_resource is required")
    if not spec.get("communities"):
        raise ValueError(f"{path}: at least one community is required")
    for c in spec["communities"]:
        if not c.get("spawner", "").startswith("#"):
            raise ValueError(f"{path}: bad community spawner {c}")
        if c.get("action", "Activate") != "Activate":
            raise ValueError(f"{path}: tower population only Activates, got {c.get('action')}")
        if not c.get("floor"):
            raise ValueError(f"{path}: community needs a floor label for the probe report: {c}")
    return spec


def build_tower_population(spec: dict[str, Any], templates: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Assemble mod\\neon_ascendancy\\bsc_tower_population.questphase.

    In1 -> hub -> per-community Activate entries -> keep-alive pause. Only
    location/open-world communities with default/idle/guard entry phases, so
    nothing depends on a scene or dialogue."""
    spawn_tpl = templates["spawn_manager_node"]
    g = QuestGraph(start_handle=1)
    start_out = g.add_input_node(spec["entry_socket"])
    hub_in, hub_out = g.add_hub_node()
    g.connect(start_out, hub_in)

    for com in spec["communities"]:
        inp, _ = g.add_community_spawn_node(
            spawn_tpl,
            action="Activate",
            spawner_reference=com["spawner"],
            entry_name=com.get("entry_name", "None"),
            phase_name=com.get("phase_name", "None"),
        )
        g.connect(hub_out, inp)

    ka = spec["keep_alive_pause"]
    ka_in, _ = g.add_pause_fact_node(ka["fact"], ka["comparison_type"], ka["value"])
    g.connect(hub_out, ka_in)

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
    dups = find_duplicate_handles(doc)
    if dups:
        raise ValueError(f"duplicate HandleIds in bsc_tower_population.questphase: {dups[:5]}")
    cross = find_cross_graph_refs(doc)
    if cross:
        raise ValueError(f"cross-graph HandleRefIds in bsc_tower_population.questphase: {cross[:5]}")
    return doc


def load_venue_spec(cast_spec: dict[str, Any]) -> dict[str, Any]:
    """Load + validate the declarative venue-access probe spec.

    Asserts the owner decision that a venue phase carries prefabs, doors and
    communities ONLY: no journal/mappin/phone/street-story/gig phases, and no
    non-door device controllers. The refs themselves are authored from verified
    vanilla phase extractions (docs/research/world-access.md)."""
    venue_path = ROOT / cast_spec["venue_spec"]
    if not venue_path.is_file():
        raise FileNotFoundError(f"missing venue spec: {venue_path}")
    with venue_path.open("r", encoding="utf-8") as fh:
        venue_spec = json.load(fh)

    gate = venue_spec.get("gate", {})
    if gate.get("comparison_type") not in ("Greater", "GreaterOrEqual", "Equal", "Less", "LessOrEqual", "NotEqual"):
        raise ValueError(f"{venue_path}: bad gate comparison_type {gate.get('comparison_type')}")
    if not gate.get("fact"):
        raise ValueError(f"{venue_path}: gate.fact is required")

    venues = venue_spec.get("venues")
    if not isinstance(venues, list) or not venues:
        raise ValueError(f"{venue_path}: 'venues' must be a non-empty list")

    allowed_actions = {
        "ForcePower", "ForceUnpower", "ForceOpen", "ForceClose", "ForceCloseImmediate",
        "ForceLock", "ForceUnlock", "ForceSeal", "ForceUnseal", "ForceEnabled",
        "ForceDisabled", "ForceON", "ForceOFF", "AuthorizationDisable",
    }
    forbidden_prefixes = tuple(venue_spec["forbidden_device_controller_prefixes"])
    codes: set[str] = set()
    for v in venues:
        code = v.get("code")
        if not code:
            raise ValueError(f"{venue_path}: venue missing code")
        if code in codes:
            raise ValueError(f"{venue_path}: duplicate venue code {code}")
        codes.add(code)
        if not v.get("prefabs") and not v.get("doors"):
            raise ValueError(f"{venue_path}: venue {code} declares no prefabs and no doors")
        if not v.get("prefabs"):
            # Door-only entry: its prefabets are owned by another phase (cast_and_hubs).
            # Declaring the same prefab in two phases duplicates it, which can break
            # instantiation, so this is allowed and documented in the entry's `why`.
            if "deferred_prefab_owner" not in v:
                raise ValueError(
                    f"{venue_path}: venue {code} has no prefabs; set deferred_prefab_owner "
                    f"naming the phase that declares them")
        for p in v["prefabs"]:
            if not p.startswith("#"):
                raise ValueError(f"{venue_path}: venue {code} bad prefab ref {p}")
            if any(pat in p for pat in venue_spec["forbidden_phase_patterns"]):
                raise ValueError(f"{venue_path}: venue {code} prefab looks like a quest/gig phase: {p}")
        for d in v.get("doors", []):
            if not d.get("ref") or not d["ref"].startswith("#"):
                raise ValueError(f"{venue_path}: venue {code} bad door ref {d}")
            if d.get("action") not in allowed_actions:
                raise ValueError(f"{venue_path}: venue {code} bad door action {d.get('action')}")
            controller = d.get("controller", "DoorControllerPS")
            allowed_extra = set(venue_spec.get("allowed_device_controllers", []))
            if not controller.startswith("Door") and controller not in allowed_extra:
                raise ValueError(
                    f"{venue_path}: venue {code} door controller {controller} is not a door "
                    f"and is not in allowed_device_controllers")
            if any(controller.startswith(pfx) for pfx in forbidden_prefixes):
                raise ValueError(f"{venue_path}: venue {code} door controller {controller} is forbidden")
        for c in v.get("communities", []):
            if not c.get("spawner", "").startswith("#"):
                raise ValueError(f"{venue_path}: venue {code} bad community spawner {c}")
            if c.get("action") not in ("Activate", "Deactivate"):
                raise ValueError(f"{venue_path}: venue {code} bad community action {c.get('action')}")
        for t in v.get("variant_toggles", []):
            if not t.get("prefab", "").startswith("#"):
                raise ValueError(f"{venue_path}: venue {code} bad variant_toggles prefab {t}")
            if any(pat in t["prefab"] for pat in venue_spec["forbidden_phase_patterns"]):
                raise ValueError(f"{venue_path}: venue {code} variant_toggles prefab looks like a quest/gig phase: {t['prefab']}")
            states = t.get("states")
            if not isinstance(states, dict) or not states:
                raise ValueError(f"{venue_path}: venue {code} variant_toggles needs a non-empty states map")
            for name, show in states.items():
                if show not in (0, 1):
                    raise ValueError(f"{venue_path}: venue {code} variant {name} show must be 0 or 1")
        if "proximity_wait" in v:
            prox = v["proximity_wait"]
            if not prox.get("ref", "").startswith("#"):
                raise ValueError(f"{venue_path}: venue {code} proximity_wait.ref must be an authored '#name' ref")
            try:
                within = float(prox.get("within"))
            except (TypeError, ValueError):
                raise ValueError(f"{venue_path}: venue {code} proximity_wait.within must be a number")
            if not 1.0 <= within <= 500.0:
                raise ValueError(f"{venue_path}: venue {code} proximity_wait.within {within} out of range 1..500")
    return venue_spec


def build_venue_probe(venue_spec: dict[str, Any], templates: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Assemble mod\\neon_ascendancy\\venue_probe.questphase.

    In1 -> hub -> per-venue chain of:
      community activations (questCommunityTemplate_NodeType)
      -> device manager node (door ForcePower/ForceOpen/...)
    RootChunk.phasePrefabs owns every venue prefab. The whole phase is wired in
    ascendancy.questphase behind `gate.fact`, so it stays dormant unless DevDebug
    sets that fact (na_dev_venue_probe). A never-firing keep-alive pause keeps
    the phasePrefabs instantiated for the whole session once it starts."""
    spawn_tpl = templates["spawn_manager_node"]

    g = QuestGraph(start_handle=1)
    start_out = g.add_input_node(venue_spec["entry_socket"])
    hub_in, hub_out = g.add_hub_node()
    g.connect(start_out, hub_in)

    for venue in venue_spec["venues"]:
        prev = hub_out
        for com in venue.get("communities", []):
            inp, out = g.add_community_spawn_node(
                spawn_tpl,
                action=com["action"],
                spawner_reference=com["spawner"],
                entry_name=com.get("entry_name", "None"),
                phase_name=com.get("phase_name", "None"),
            )
            g.connect(prev, inp)
            prev = out
        # Defer the venue's device actions until the player is near the venue, so
        # they run against streamed entities. Firing them at bootstrap (while the
        # player is still in H10) hits no entity. `proximity` is an authored
        # workspot/door ref plus a radius; without it the actions run immediately.
        prox = venue.get("proximity_wait")
        if prox:
            inp, out = g.add_proximity_pause_node(prox["ref"], float(prox["within"]))
            g.connect(prev, inp)
            prev = out
        doors = venue.get("doors", [])
        if doors:
            entries = [
                {
                    "ref": d["ref"],
                    "controller": d.get("controller", "DoorControllerPS"),
                    "action": d["action"],
                }
                for d in doors
            ]
            inp, out = g.add_device_manager_node(entries)
            g.connect(prev, inp)
            prev = out
        for toggle in venue.get("variant_toggles", []):
            inp, out = g.add_variant_toggle_node(toggle["prefab"], toggle["states"])
            g.connect(prev, inp)
            prev = out

    # Keep-alive pause: always false; keeps phasePrefabs and community
    # activations alive for the whole session once the phase is entered.
    ka = venue_spec["keep_alive_pause"]
    ka_in, _ = g.add_pause_fact_node(ka["fact"], ka["comparison_type"], ka["value"])
    g.connect(hub_out, ka_in)

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
            # Deduplicate: two venue entries may legitimately need the same prefab
            # (e.g. the Black Sapphire entrance and the sneak-in route), and a
            # repeated questQuestPrefabEntry is not meaningful.
            "phasePrefabs": [
                {"$type": "questQuestPrefabEntry", "prefabNodeRef": noderef(p)}
                for p in dict.fromkeys(
                    p for venue in venue_spec["venues"] for p in venue["prefabs"]
                )
            ],
        }
    )
    dups = find_duplicate_handles(doc)
    if dups:
        raise ValueError(f"duplicate HandleIds in venue_probe.questphase: {dups[:5]}")
    cross = find_cross_graph_refs(doc)
    if cross:
        raise ValueError(f"cross-graph HandleRefIds in venue_probe.questphase: {cross[:5]}")
    return doc


def load_ft_spec(cast_spec: dict[str, Any]) -> dict[str, Any]:
    ft_path = ROOT / cast_spec["dev_fast_travel_spec"]
    if not ft_path.is_file():
        raise FileNotFoundError(f"missing dev fast travel spec: {ft_path}")
    with ft_path.open("r", encoding="utf-8") as fh:
        ft_spec = json.load(fh)
    points = ft_spec.get("points")
    if not isinstance(points, list) or not points:
        raise ValueError(f"{ft_path}: 'points' must be a non-empty list")
    records = [p["point_record"] for p in points]
    if len(set(records)) != len(records):
        raise ValueError(f"{ft_path}: duplicate point_record entries")
    if records != sorted(records):
        raise ValueError(f"{ft_path}: points must be sorted by point_record")
    for p in points:
        if not p["point_record"].startswith("FastTravelPoints."):
            raise ValueError(f"{ft_path}: bad point_record {p['point_record']}")
        if not p["marker_ref"].startswith("#"):
            raise ValueError(f"{ft_path}: bad marker_ref {p['marker_ref']}")
        if p["is_ep1"] not in (0, 1):
            raise ValueError(f"{ft_path}: bad is_ep1 {p['is_ep1']}")
    gate = ft_spec.get("gate", {})
    if gate.get("comparison_type") not in ("Greater", "GreaterOrEqual", "Equal", "Less", "LessOrEqual", "NotEqual"):
        raise ValueError(f"{ft_path}: bad gate comparison_type {gate.get('comparison_type')}")
    return ft_spec


def write_resource_json(directory: Path, rel_path: str, doc: dict[str, Any]) -> None:
    target = directory / rel_path.replace("\\", "/")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(doc, indent=2), encoding="utf-8")


def build(
    args: argparse.Namespace,
    spec: dict[str, Any],
    cast_spec: dict[str, Any],
    ft_spec: dict[str, Any],
    venue_spec: dict[str, Any],
    barricade_spec: dict[str, Any],
    vendors_spec: dict[str, Any],
    tower_spec: dict[str, Any],
) -> Path:
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
            build_dir, "mod/neon_ascendancy/ascendancy.questphase.json", build_questphase(templates, spec, cast_spec, venue_spec, barricade_spec, vendors_spec, tower_spec)
        )
        write_resource_json(
            build_dir,
            "mod/neon_ascendancy/cast_and_hubs.questphase.json",
            build_cast_and_hubs(templates, cast_spec, ft_spec),
        )
        write_resource_json(build_dir, "mod/neon_ascendancy/spike_kab07.questphase.json", build_spike(templates, spec))
        write_resource_json(
            build_dir, "mod/neon_ascendancy/venue_probe.questphase.json", build_venue_probe(venue_spec, templates)
        )
        write_resource_json(
            build_dir, "mod/neon_ascendancy/barricade_cleanup.questphase.json", build_barricade_cleanup(barricade_spec, templates)
        )
        write_resource_json(
            build_dir, "mod/neon_ascendancy/dogtown_vendors.questphase.json", build_dogtown_vendors(vendors_spec, templates)
        )
        write_resource_json(
            build_dir, "mod/neon_ascendancy/bsc_tower_population.questphase.json", build_tower_population(tower_spec, templates)
        )

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


def check(
    args: argparse.Namespace,
    spec: dict[str, Any],
    cast_spec: dict[str, Any],
    ft_spec: dict[str, Any],
    venue_spec: dict[str, Any],
    barricade_spec: dict[str, Any],
    vendors_spec: dict[str, Any],
    tower_spec: dict[str, Any],
) -> None:
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
            _check_questphase(resources, spec, cast_spec, venue_spec, barricade_spec, vendors_spec, tower_spec, ok)
            _check_cast_and_hubs(resources, spec, cast_spec, ft_spec, ok)
            _check_spike(resources, spec, ok)
            _check_venue_probe(resources, spec, venue_spec, ok)
            _check_barricade_cleanup(resources, barricade_spec, ok)
            _check_dogtown_vendors(resources, vendors_spec, ok)
            _check_tower_population(resources, tower_spec, ok)

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


def _check_questphase(
    resources: dict[str, dict[str, Any]],
    spec: dict[str, Any],
    cast_spec: dict[str, Any],
    venue_spec: dict[str, Any],
    barricade_spec: dict[str, Any],
    vendors_spec: dict[str, Any],
    tower_spec: dict[str, Any],
    ok: Callable[[bool, str], None],
) -> None:
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
        all_expected_facts = list(qp["initial_facts"]) + list(cast_spec["service_vendors"]["vendor_facts"])
        facts = by_type("questFactsDBManagerNodeDefinition")
        ok(len(facts) == len(all_expected_facts),
           f"expected {len(all_expected_facts)} fact nodes, found {len(facts)}")
        expected_reachable += facts
        teles = by_type("questTeleportPuppetNodeDefinition")
        ok(len(teles) == 0, f"expected 0 blocking teleport nodes in questphase, found {len(teles)}")
        phases = by_type("questPhaseNodeDefinition")
        top_phase_nodes = [p for p in phases if p["Data"].get("phaseResource", {}).get("DepotPath", {}).get("$value") and p["Data"]["phaseResource"]["DepotPath"]["$value"] != "0"]
        ok(len(top_phase_nodes) == len(qp["kept_depot_phases"]) + 6,
           f"expected {len(qp['kept_depot_phases']) + 6} external phase nodes ({len(qp['kept_depot_phases'])} kept + cast_and_hubs + barricade_cleanup + dogtown_vendors + bsc_tower_population + spike + venue_probe), found {len(top_phase_nodes)}")
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

        # facts exactly match the spec + cast vendor_facts, none forbidden
        actual_facts = _collect_setvar_facts(rc)
        expected_facts = [(f["fact"], f["value"]) for f in all_expected_facts]
        ok(sorted(actual_facts) == sorted(expected_facts),
           f"setvar facts mismatch:\n  actual:   {sorted(actual_facts)}\n  expected: {sorted(expected_facts)}")
        forbidden = set(qp["forbidden_facts"]) | set(cast_spec["forbidden_default_on_facts"])
        prefixes = tuple(qp["forbidden_fact_prefixes"])
        bad = [f for f, _ in actual_facts if f in forbidden or f.startswith(prefixes)]
        ok(not bad, f"forbidden story/default_on facts set: {bad}")

        # phase refs: kept + cast_and_hubs + spike present, excluded absent
        refs = _collect_phase_refs(rc)
        expected_refs = (
            {e["depot_path"] for e in qp["kept_depot_phases"]}
            | set(qp["inline_phase_depot_refs"])
            | {cast_spec["phase_resource"], qp["spike"]["resource"], venue_spec["phase_resource"], barricade_spec["phase_resource"], vendors_spec["phase_resource"], tower_spec["phase_resource"]}
        )
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


def _check_fast_travel_registration(
    rc: dict[str, Any],
    nodes: list[dict[str, Any]],
    ft_spec: dict[str, Any],
    ok: Callable[[bool, str], None],
) -> None:
    """Round-trip verify the dev-gated fast-travel registration chain.

    Expected: In1 (reachable) -> gate pause (fact) -> questEventManagerNodeDefinition
    (managerName=FastTravelSystem, RegisterFastTravelPointsRequest, register=1)
    carrying exactly the (pointRecord, markerRef, isEP1) triples from the spec."""
    gate = ft_spec["gate"]

    inputs = [n for n in nodes if n["Data"].get("$type") == "questInputNodeDefinition"]
    reachable = reachable_nodes(nodes, inputs[0]) if inputs else set()

    gate_pauses = []
    for p in nodes:
        d = p["Data"]
        if d.get("$type") != "questPauseConditionNodeDefinition":
            continue
        typ = d.get("condition", {}).get("Data", {}).get("type", {}).get("Data", {})
        if (typ.get("factName") == gate["fact"]
                and typ.get("comparisonType") == gate["comparison_type"]
                and typ.get("value") == gate["value"]):
            gate_pauses.append(p)
    ok(len(gate_pauses) == 1,
       f"expected 1 fast-travel gate pause ({gate['fact']} {gate['comparison_type']} {gate['value']}), "
       f"found {len(gate_pauses)}")

    events = [
        n for n in nodes
        if n["Data"].get("$type") == "questEventManagerNodeDefinition"
        and n["Data"].get("event", {}).get("Data", {}).get("$type") == "RegisterFastTravelPointsRequest"
    ]
    ok(len(events) == 1, f"expected 1 RegisterFastTravelPointsRequest event node, found {len(events)}")
    if not gate_pauses or not events:
        return

    gate_node = gate_pauses[0]
    event_node = events[0]
    gate_id = id_of(gate_node)
    event_id = id_of(event_node)
    ok(gate_id in reachable, "fast-travel gate pause is not reachable from the phase input")
    ok(event_id in reachable, "fast-travel registration node is not reachable from the phase input")
    ok((gate_id, event_id) in _graph_edges(nodes),
       "fast-travel gate pause is not connected to the registration node")

    gate_in = _socket_handle(gate_node["Data"]["sockets"][1])
    gate_out = _socket_handle(gate_node["Data"]["sockets"][2])
    ok(_count_connections(rc, gate_in) == (1, 0), "fast-travel gate In must have exactly 1 incoming connection")
    ok(_count_connections(rc, gate_out) == (0, 1), "fast-travel gate Out must have exactly 1 outgoing connection")

    data = event_node["Data"]
    event = data.get("event", {}).get("Data", {})
    ok(data.get("managerName") == "FastTravelSystem", "fast-travel event managerName != FastTravelSystem")
    ok(event.get("$type") == "RegisterFastTravelPointsRequest", "fast-travel event type mismatch")
    ok(event.get("register") == 1, "fast-travel event register != 1")
    ok(data.get("componentName", {}).get("$value") == "None", "fast-travel event componentName != None")
    ok(data.get("PSClassName", {}).get("$value") == "None", "fast-travel event PSClassName != None")
    ok(data.get("isObjectPlayer") == 0 and data.get("isUiEvent") == 0,
       "fast-travel event isObjectPlayer/isUiEvent must be 0")
    ok((data.get("objectRef") or {}).get("type") == "EntityRef", "fast-travel event objectRef.type != EntityRef")

    actual = {
        (ft["Data"]["pointRecord"]["$value"], ft["Data"]["markerRef"]["$value"], ft["Data"]["isEP1"])
        for ft in event.get("fastTravelNodes", [])
    }
    entries = event.get("fastTravelNodes", [])
    expected = {(p["point_record"], p["marker_ref"], p["is_ep1"]) for p in ft_spec["points"]}
    ok(len(entries) == len(ft_spec["points"]),
       f"fast-travel registration has {len(entries)} entries, expected {len(ft_spec['points'])}")
    ok(len(actual) == len(entries), "fast-travel registration contains duplicate (pointRecord, markerRef, isEP1) entries")
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    ok(not missing, f"fast-travel registration missing points: {missing[:5]}")
    ok(not extra, f"fast-travel registration has unexpected points: {extra[:5]}")


def _check_cast_and_hubs(
    resources: dict[str, dict[str, Any]],
    spec: dict[str, Any],
    cast_spec: dict[str, Any],
    ft_spec: dict[str, Any],
    ok: Callable[[bool, str], None],
) -> None:
    doc = resources[cast_spec["phase_resource"]]
    rc = doc["Data"]["RootChunk"]
    ok(rc.get("$type") == "questQuestPhaseResource", "cast_and_hubs root type is not questQuestPhaseResource")

    # Required workspot phasePrefabs
    actual_prefabs = [e["prefabNodeRef"]["$value"] for e in rc.get("phasePrefabs", [])]
    expected_prefabs = [e["prefab"] for e in cast_spec["phase_prefabs"]]
    ok(actual_prefabs == expected_prefabs,
       f"cast_and_hubs phasePrefabs mismatch:\n  actual:   {actual_prefabs}\n  expected: {expected_prefabs}")

    # Strict handle integrity
    dups = find_duplicate_handles(doc)
    ok(not dups, f"duplicate HandleIds in cast_and_hubs.questphase: {dups[:10]}")
    cross = find_cross_graph_refs(doc)
    ok(not cross, f"cross-graph HandleRefIds in cast_and_hubs.questphase: {cross[:10]}")

    nodes = rc["graph"]["Data"]["nodes"]
    inputs = [n for n in nodes if n["Data"].get("$type") == "questInputNodeDefinition"]
    ok(len(inputs) == 1, f"cast_and_hubs has {len(inputs)} input nodes")
    top_outputs = [n for n in nodes if n["Data"].get("$type") == "questOutputNodeDefinition"]
    ok(len(top_outputs) == 0,
       f"cast_and_hubs has {len(top_outputs)} top-level Output nodes (phase must stay alive forever)")

    if inputs:
        ok(inputs[0]["Data"]["socketName"]["$value"] == cast_spec["entry_socket"],
           f"cast_and_hubs input socketName != {cast_spec['entry_socket']}")
        reachable = reachable_nodes(nodes, inputs[0])
        unreachable = [id_of(n) for n in nodes if id_of(n) not in reachable]
        ok(not unreachable, f"cast_and_hubs nodes unreachable from {cast_spec['entry_socket']}: {unreachable}")

    # Verify all top-level community and spawn-set activations
    actual_communities: set[tuple[str, str, str, str]] = set()
    actual_spawn_sets: set[tuple[str, str, str, str]] = set()
    for n in nodes:
        d = n["Data"]
        if d.get("$type") != "questSpawnManagerNodeDefinition":
            continue
        for act in d.get("actions", []):
            at = act.get("type", {}).get("Data", {})
            t = at.get("$type")
            if t == "questCommunityTemplate_NodeType":
                actual_communities.add((
                    at.get("action"),
                    at.get("spawnerReference", {}).get("$value"),
                    at.get("communityEntryName", {}).get("$value"),
                    at.get("communityEntryPhaseName", {}).get("$value"),
                ))
            elif t == "questSpawnSet_NodeType":
                actual_spawn_sets.add((
                    at.get("action"),
                    at.get("reference", {}).get("$value"),
                    at.get("entryName", {}).get("$value"),
                    at.get("phaseName", {}).get("$value"),
                ))

    expected_communities = {
        ("Activate", h["spawner_reference"], h["community_entry_name"], h["community_entry_phase_name"])
        for h in cast_spec["world_hubs"]
    }
    ok(expected_communities <= actual_communities,
       f"cast_and_hubs missing world_hubs activations: {sorted(expected_communities - actual_communities)}")

    expected_spawn_sets = {
        ("Activate", a["reference"], a["entry_name"], a["phase_name"])
        for a in cast_spec["overhaul_actors"]
    }
    for v in cast_spec["service_vendors"]["direct_vendor_phases"]:
        if "spawn_set" in v:
            ss = v["spawn_set"]
            expected_spawn_sets.add(("Activate", ss["reference"], ss["entry_name"], ss["phase_name"]))
    ok(expected_spawn_sets <= actual_spawn_sets,
       f"cast_and_hubs missing spawn_set activations: {sorted(expected_spawn_sets - actual_spawn_sets)}")

    # Verify direct vendor inline phases (expected scenes & phaseInstancePrefabs)
    inline_phases = [n["Data"] for n in nodes if n["Data"].get("$type") == "questPhaseNodeDefinition"]
    ok(len(inline_phases) == len(cast_spec["service_vendors"]["direct_vendor_phases"]),
       f"cast_and_hubs expected {len(cast_spec['service_vendors']['direct_vendor_phases'])} direct vendor phases, found {len(inline_phases)}")
    all_scenes = {
        s.get("sceneFile", {}).get("DepotPath", {}).get("$value")
        for s in _collect_nodes_of_type(rc, "questSceneNodeDefinition")
    }
    all_inst_prefabs = {
        e["prefabNodeRef"]["$value"]
        for p in _collect_nodes_of_type(rc, "questPhaseNodeDefinition")
        for e in p.get("phaseInstancePrefabs", [])
    }
    for v in cast_spec["service_vendors"]["direct_vendor_phases"]:
        ok(v["expected_scene"] in all_scenes,
           f"cast_and_hubs missing direct vendor scene: {v['expected_scene']}")
        for pf in v.get("expected_prefabs", []):
            ok(pf in all_inst_prefabs,
               f"cast_and_hubs missing direct vendor phaseInstancePrefab: {pf}")

    # Verify keep-alive pause condition
    ka = cast_spec["keep_alive_pause"]
    top_pauses = [n["Data"] for n in nodes if n["Data"].get("$type") == "questPauseConditionNodeDefinition"]
    ka_found = False
    for p in top_pauses:
        typ = p.get("condition", {}).get("Data", {}).get("type", {}).get("Data", {})
        if (typ.get("factName") == ka["fact"]
                and typ.get("comparisonType") == ka["comparison_type"]
                and typ.get("value") == ka["value"]):
            ka_found = True
    ok(ka_found, f"cast_and_hubs missing keep-alive pause {ka['fact']} {ka['comparison_type']} {ka['value']}")

    # Verify the dev fast-travel gate -> RegisterFastTravelPointsRequest chain
    ft_gate = ft_spec["gate"]
    _check_fast_travel_registration(rc, nodes, ft_spec, ok)

    # The dev unlock fact must stay runtime-only: no archive resource may set it.
    for rel in ("mod\\neon_ascendancy\\ascendancy.questphase", cast_spec["phase_resource"]):
        setvars = [f for f, _ in _collect_setvar_facts(resources[rel]["Data"]["RootChunk"])]
        ok(ft_gate["fact"] not in setvars,
           f"{rel} sets {ft_gate['fact']} via questSetVar_NodeType; it must stay DevDebug-only")
    spec_facts = {f["fact"] for f in spec["questphase"]["initial_facts"]}
    spec_facts |= {f["fact"] for f in cast_spec["service_vendors"]["vendor_facts"]}
    ok(ft_gate["fact"] not in spec_facts,
       f"{ft_gate['fact']} must not be declared in initial_facts/vendor_facts")

    # Verify zero forbidden facts and zero excluded phases inside cast_and_hubs
    qp = spec["questphase"]
    actual_facts = _collect_setvar_facts(rc)
    forbidden = set(qp["forbidden_facts"]) | set(cast_spec["forbidden_default_on_facts"])
    prefixes = tuple(qp["forbidden_fact_prefixes"])
    bad_facts = [f for f, _ in actual_facts if f in forbidden or f.startswith(prefixes)]
    ok(not bad_facts, f"forbidden facts set inside cast_and_hubs.questphase: {bad_facts}")

    refs = _collect_phase_refs(rc)
    excluded = sorted({r for r in refs if any(p in r for p in qp["excluded_phase_patterns"])})
    ok(not excluded, f"excluded phase refs inside cast_and_hubs.questphase: {excluded}")


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


def _check_barricade_cleanup(
    resources: dict[str, dict[str, Any]],
    barricade_spec: dict[str, Any],
    ok: Callable[[bool, str], None],
) -> None:
    """Round-trip verify barricade_cleanup.questphase.

    Expected: exactly the spec's variant toggles (prefab + show map), community
    Deactivations, and one questSpawner_NodeType Deactivate node carrying every
    spec spawner ref; plus the keep-alive pause. Nothing story/journalled."""
    doc = resources[barricade_spec["phase_resource"]]
    rc = doc["Data"]["RootChunk"]
    ok(rc.get("$type") == "questQuestPhaseResource", "barricade_cleanup root type is not questQuestPhaseResource")
    ok(rc.get("phasePrefabs", []) == [], "barricade_cleanup must not declare phasePrefabs (declaring them can re-show the props)")

    dups = find_duplicate_handles(doc)
    ok(not dups, f"duplicate HandleIds in barricade_cleanup.questphase: {dups[:10]}")
    cross = find_cross_graph_refs(doc)
    ok(not cross, f"cross-graph HandleRefIds in barricade_cleanup.questphase: {cross[:10]}")

    nodes = rc["graph"]["Data"]["nodes"]
    inputs = [n for n in nodes if n["Data"].get("$type") == "questInputNodeDefinition"]
    ok(len(inputs) == 1, f"barricade_cleanup has {len(inputs)} input nodes")
    if inputs:
        ok(inputs[0]["Data"]["socketName"]["$value"] == barricade_spec["entry_socket"],
           f"barricade_cleanup input socketName != {barricade_spec['entry_socket']}")
        reachable = reachable_nodes(nodes, inputs[0])
        unreachable = [id_of(n) for n in nodes if id_of(n) not in reachable]
        ok(not unreachable, f"barricade_cleanup nodes unreachable from input: {unreachable}")

    # Variant toggles: exact list, in order.
    expected_toggles = [(t["prefab"], dict(t["states"])) for t in barricade_spec["variant_toggles"]]
    actual_toggles = []
    for n in nodes:
        d = n["Data"]
        if d.get("$type") != "questWorldDataManagerNodeDefinition":
            continue
        typ = d.get("type", {}).get("Data", {})
        ok(typ.get("$type") == "questTogglePrefabVariant_NodeType",
           "barricade variant toggle type is not questTogglePrefabVariant_NodeType")
        for p in typ.get("params", []):
            states = {s["name"]["$value"]: s["show"] for s in p.get("variantStates", [])}
            actual_toggles.append((p.get("prefabNodeRef", {}).get("$value"), states))
    ok(actual_toggles == expected_toggles,
       f"barricade variant toggles mismatch:\n  actual:   {actual_toggles}\n  expected: {expected_toggles}")

    # Communities: exact set of Deactivations.
    actual_comms = set()
    for n in nodes:
        d = n["Data"]
        if d.get("$type") != "questSpawnManagerNodeDefinition":
            continue
        for act in d.get("actions", []):
            at = act.get("type", {}).get("Data", {})
            if at.get("$type") == "questCommunityTemplate_NodeType":
                ok(at.get("action") == "Deactivate", f"barricade community action is {at.get('action')}, not Deactivate")
                actual_comms.add(at.get("spawnerReference", {}).get("$value"))
    expected_comms = {c["spawner"] for c in barricade_spec["communities"]}
    ok(actual_comms == expected_comms,
       f"barricade communities mismatch:\n  actual:   {sorted(actual_comms)}\n  expected: {sorted(expected_comms)}")

    # Spawners: exact set of Deactivations via questSpawner_NodeType.
    actual_spawners = set()
    for n in nodes:
        d = n["Data"]
        if d.get("$type") != "questSpawnManagerNodeDefinition":
            continue
        for act in d.get("actions", []):
            at = act.get("type", {}).get("Data", {})
            if at.get("$type") == "questSpawner_NodeType":
                ok(at.get("action") == "Deactivate", f"barricade spawner action is {at.get('action')}, not Deactivate")
                actual_spawners.add(at.get("spawnerReference", {}).get("$value"))
    expected_spawners = {s["ref"] for s in barricade_spec["spawners"]}
    ok(len(expected_spawners) == 60, f"expected 60 spawner refs in spec, found {len(expected_spawners)}")
    ok(actual_spawners == expected_spawners,
       f"barricade spawners mismatch: missing {sorted(expected_spawners - actual_spawners)[:5]} extra {sorted(actual_spawners - expected_spawners)[:5]}")

    # Keep-alive pause present.
    ka = barricade_spec["keep_alive_pause"]
    ka_found = False
    for n in nodes:
        d = n["Data"]
        if d.get("$type") != "questPauseConditionNodeDefinition":
            continue
        typ = d.get("condition", {}).get("Data", {}).get("type", {}).get("Data", {})
        if (typ.get("factName") == ka["fact"] and typ.get("comparisonType") == ka["comparison_type"]
                and typ.get("value") == ka["value"]):
            ka_found = True
    ok(ka_found, f"barricade_cleanup missing keep-alive pause {ka['fact']}")

    # The cleanup resource must not carry journal/mappin/phone/quest refs.
    prefixes = ("journal", "mappin", "phone", "holocall", "quests\\main", "quests\\side", "street_stories")
    refs = _collect_phase_refs(rc)
    bad = sorted({r for r in refs if any(p in r.lower() for p in prefixes)})
    ok(not bad, f"barricade_cleanup carries story/journalled phase refs: {bad}")

    # ascendancy.questphase must wire the cleanup phase node off the fan-out.
    qp_doc = resources["mod\\neon_ascendancy\\ascendancy.questphase"]
    qp_nodes = qp_doc["Data"]["RootChunk"]["graph"]["Data"]["nodes"]
    cleanup_phases = [
        p for p in qp_nodes
        if p["Data"].get("$type") == "questPhaseNodeDefinition"
        and p["Data"].get("phaseResource", {}).get("DepotPath", {}).get("$value") == barricade_spec["phase_resource"]
    ]
    ok(len(cleanup_phases) == 1, f"expected 1 barricade cleanup phase node in ascendancy.questphase, found {len(cleanup_phases)}")


def _check_dogtown_vendors(
    resources: dict[str, dict[str, Any]],
    vendors_spec: dict[str, Any],
    ok: Callable[[bool, str], None],
) -> None:
    """Round-trip verify dogtown_vendors.questphase.

    Expected: exactly the spec's questSpawnSet Activate triples and community
    Activate triples, no journal/scene nodes, and the phase wired in
    ascendancy.questphase behind its gate pause."""
    doc = resources[vendors_spec["phase_resource"]]
    rc = doc["Data"]["RootChunk"]
    ok(rc.get("$type") == "questQuestPhaseResource", "dogtown_vendors root type is not questQuestPhaseResource")
    dups = find_duplicate_handles(doc)
    ok(not dups, f"duplicate HandleIds in dogtown_vendors.questphase: {dups[:10]}")
    cross = find_cross_graph_refs(doc)
    ok(not cross, f"cross-graph HandleRefIds in dogtown_vendors.questphase: {cross[:10]}")

    nodes = rc["graph"]["Data"]["nodes"]
    inputs = [n for n in nodes if n["Data"].get("$type") == "questInputNodeDefinition"]
    ok(len(inputs) == 1, f"dogtown_vendors has {len(inputs)} input nodes")
    if inputs:
        ok(inputs[0]["Data"]["socketName"]["$value"] == vendors_spec["entry_socket"],
           f"dogtown_vendors input socketName != {vendors_spec['entry_socket']}")
        reachable = reachable_nodes(nodes, inputs[0])
        unreachable = [id_of(n) for n in nodes if id_of(n) not in reachable]
        ok(not unreachable, f"dogtown_vendors nodes unreachable from input: {unreachable}")

    actual_sets = set()
    actual_comms = set()
    for n in nodes:
        d = n["Data"]
        if d.get("$type") != "questSpawnManagerNodeDefinition":
            continue
        for act in d.get("actions", []):
            at = act.get("type", {}).get("Data", {})
            if at.get("$type") == "questSpawnSet_NodeType":
                ok(at.get("action") == "Activate", f"vendor spawn_set action is {at.get('action')}")
                actual_sets.add((at.get("reference", {}).get("$value"),
                                 at.get("entryName", {}).get("$value"),
                                 at.get("phaseName", {}).get("$value")))
            elif at.get("$type") == "questCommunityTemplate_NodeType":
                ok(at.get("action") == "Activate", f"vendor community action is {at.get('action')}")
                actual_comms.add((at.get("spawnerReference", {}).get("$value"),
                                  at.get("communityEntryName", {}).get("$value"),
                                  at.get("communityEntryPhaseName", {}).get("$value")))
    expected_sets = {(s["ref"], s["entry_name"], s["phase_name"]) for s in vendors_spec["spawn_sets"]}
    expected_comms = {(c["spawner"], c.get("entry_name", "None"), c.get("phase_name", "None"))
                      for c in vendors_spec["communities"]}
    ok(actual_sets == expected_sets,
       f"vendor spawn_sets mismatch: missing {sorted(expected_sets - actual_sets)[:5]} extra {sorted(actual_sets - expected_sets)[:5]}")
    ok(actual_comms == expected_comms,
       f"vendor communities mismatch:\n  actual:   {sorted(actual_comms)}\n  expected: {sorted(expected_comms)}")

    # No story content copied in.
    story = [n for n in nodes if n["Data"].get("$type") in
             ("questJournalNodeDefinition", "questSceneNodeDefinition", "questMappinManagerNodeDefinition")]
    ok(not story, f"dogtown_vendors must not copy journal/scene/mappin nodes, found {len(story)}")

    # Keep-alive pause lives inside the vendor phase; the gate pause lives in
    # ascendancy.questphase.
    gate = vendors_spec["gate"]
    ka = vendors_spec["keep_alive_pause"]
    ka_found = False
    for n in nodes:
        d = n["Data"]
        if d.get("$type") == "questPauseConditionNodeDefinition":
            typ = d.get("condition", {}).get("Data", {}).get("type", {}).get("Data", {})
            if typ.get("factName") == ka["fact"] and typ.get("comparisonType") == ka["comparison_type"]:
                ka_found = True
    ok(ka_found, "dogtown_vendors missing its keep-alive pause")
    qp_doc = resources["mod\\neon_ascendancy\\ascendancy.questphase"]
    qp_nodes = qp_doc["Data"]["RootChunk"]["graph"]["Data"]["nodes"]
    phase_nodes = [
        p for p in qp_nodes
        if p["Data"].get("$type") == "questPhaseNodeDefinition"
        and p["Data"].get("phaseResource", {}).get("DepotPath", {}).get("$value") == vendors_spec["phase_resource"]
    ]
    ok(len(phase_nodes) == 1, f"expected 1 dogtown_vendors phase node in ascendancy.questphase, found {len(phase_nodes)}")
    qp_gate = [
        p for p in qp_nodes
        if p["Data"].get("$type") == "questPauseConditionNodeDefinition"
        and p["Data"].get("condition", {}).get("Data", {}).get("type", {}).get("Data", {}).get("factName") == gate["fact"]
    ]
    ok(len(qp_gate) == 1, f"expected 1 vendor gate pause in ascendancy.questphase, found {len(qp_gate)}")


def _check_tower_population(
    resources: dict[str, dict[str, Any]],
    tower_spec: dict[str, Any],
    ok: Callable[[bool, str], None],
) -> None:
    """Round-trip verify bsc_tower_population.questphase.

    Expected: exactly the spec's community Activate triples, one per entry, with
    no journal/scene/mappin nodes; wired in ascendancy.questphase."""
    doc = resources[tower_spec["phase_resource"]]
    rc = doc["Data"]["RootChunk"]
    ok(rc.get("$type") == "questQuestPhaseResource", "bsc_tower_population root type is not questQuestPhaseResource")
    dups = find_duplicate_handles(doc)
    ok(not dups, f"duplicate HandleIds in bsc_tower_population.questphase: {dups[:10]}")
    cross = find_cross_graph_refs(doc)
    ok(not cross, f"cross-graph HandleRefIds in bsc_tower_population.questphase: {cross[:10]}")

    nodes = rc["graph"]["Data"]["nodes"]
    inputs = [n for n in nodes if n["Data"].get("$type") == "questInputNodeDefinition"]
    ok(len(inputs) == 1, f"bsc_tower_population has {len(inputs)} input nodes")
    if inputs:
        reachable = reachable_nodes(nodes, inputs[0])
        unreachable = [id_of(n) for n in nodes if id_of(n) not in reachable]
        ok(not unreachable, f"bsc_tower_population nodes unreachable from input: {unreachable}")

    actual = []
    for n in nodes:
        d = n["Data"]
        if d.get("$type") != "questSpawnManagerNodeDefinition":
            continue
        for act in d.get("actions", []):
            at = act.get("type", {}).get("Data", {})
            if at.get("$type") != "questCommunityTemplate_NodeType":
                continue
            ok(at.get("action") == "Activate", f"tower community action is {at.get('action')}, not Activate")
            actual.append((at.get("spawnerReference", {}).get("$value"),
                           at.get("communityEntryName", {}).get("$value"),
                           at.get("communityEntryPhaseName", {}).get("$value")))
    expected = [(c["spawner"], c.get("entry_name", "None"), c.get("phase_name", "None"))
                for c in tower_spec["communities"]]
    ok(sorted(actual) == sorted(expected),
       f"tower communities mismatch: missing {sorted(set(expected) - set(actual))[:5]} extra {sorted(set(actual) - set(expected))[:5]}")
    ok(len(actual) == len(expected), f"tower community count {len(actual)} != spec {len(expected)}")

    story = [n for n in nodes if n["Data"].get("$type") in
             ("questJournalNodeDefinition", "questSceneNodeDefinition", "questMappinManagerNodeDefinition")]
    ok(not story, f"bsc_tower_population must not copy journal/scene/mappin nodes, found {len(story)}")

    qp_doc = resources["mod\\neon_ascendancy\\ascendancy.questphase"]
    qp_nodes = qp_doc["Data"]["RootChunk"]["graph"]["Data"]["nodes"]
    phase_nodes = [
        p for p in qp_nodes
        if p["Data"].get("$type") == "questPhaseNodeDefinition"
        and p["Data"].get("phaseResource", {}).get("DepotPath", {}).get("$value") == tower_spec["phase_resource"]
    ]
    ok(len(phase_nodes) == 1, f"expected 1 bsc_tower_population phase node, found {len(phase_nodes)}")


def _check_venue_probe(
    resources: dict[str, dict[str, Any]],
    spec: dict[str, Any],
    venue_spec: dict[str, Any],
    ok: Callable[[bool, str], None],
) -> None:
    """Round-trip verify venue_probe.questphase and its gate in ascendancy.questphase.

    Expected:
      - phasePrefabs == every venue prefab, in spec order;
      - one questInteractiveObjectManagerNodeDefinition per venue that has doors,
        with exactly the spec's (ref, controller, action) triples in order;
      - community activations match the spec exactly;
      - no journal/mappin/phone/street-story/gig phases and no non-door devices;
      - one keep-alive pause;
      - ascendancy.questphase wires the venue gate pause -> venue probe phase."""
    doc = resources[venue_spec["phase_resource"]]
    rc = doc["Data"]["RootChunk"]
    ok(rc.get("$type") == "questQuestPhaseResource", "venue_probe root type is not questQuestPhaseResource")

    expected_prefabs = list(dict.fromkeys(p for venue in venue_spec["venues"] for p in venue["prefabs"]))
    actual_prefabs = [e["prefabNodeRef"]["$value"] for e in rc.get("phasePrefabs", [])]
    ok(actual_prefabs == expected_prefabs,
       f"venue_probe phasePrefabs mismatch:\n  actual:   {actual_prefabs}\n  expected: {expected_prefabs}")

    dups = find_duplicate_handles(doc)
    ok(not dups, f"duplicate HandleIds in venue_probe.questphase: {dups[:10]}")
    cross = find_cross_graph_refs(doc)
    ok(not cross, f"cross-graph HandleRefIds in venue_probe.questphase: {cross[:10]}")

    nodes = rc["graph"]["Data"]["nodes"]
    inputs = [n for n in nodes if n["Data"].get("$type") == "questInputNodeDefinition"]
    ok(len(inputs) == 1, f"venue_probe has {len(inputs)} input nodes")
    if inputs:
        ok(inputs[0]["Data"]["socketName"]["$value"] == venue_spec["entry_socket"],
           f"venue_probe input socketName != {venue_spec['entry_socket']}")
        reachable = reachable_nodes(nodes, inputs[0])
        unreachable = [id_of(n) for n in nodes if id_of(n) not in reachable]
        ok(not unreachable, f"venue_probe nodes unreachable from input: {unreachable}")

    # Device manager: one node per venue that declares doors; params exactly match.
    expected_device_groups = [
        [(d["ref"], d.get("controller", "DoorControllerPS"), d["action"]) for d in v.get("doors", [])]
        for v in venue_spec["venues"] if v.get("doors")
    ]
    device_nodes = [
        n["Data"] for n in nodes
        if n["Data"].get("$type") == "questInteractiveObjectManagerNodeDefinition"
    ]
    ok(len(device_nodes) == len(expected_device_groups),
       f"expected {len(expected_device_groups)} device manager nodes, found {len(device_nodes)}")
    actual_groups = []
    for d_node in device_nodes:
        typ = d_node.get("type", {}).get("Data", {})
        ok(typ.get("$type") == "questDeviceManager_NodeType",
           "device manager node type is not questDeviceManager_NodeType")
        group = []
        for p in typ.get("params", []):
            pd = p["Data"]
            ok(pd.get("$type") == "questDeviceManager_NodeTypeParams",
               "device manager param type mismatch")
            ok((pd.get("entityRef", {}).get("reference", {}).get("$value")) == "0",
               "device manager entityRef.reference must be 0 (objectRef carries the node ref)")
            group.append((
                pd.get("objectRef", {}).get("$value"),
                pd.get("deviceControllerClass", {}).get("$value"),
                pd.get("deviceAction", {}).get("$value"),
            ))
        actual_groups.append(group)
    ok(actual_groups == expected_device_groups,
       f"venue_probe device groups mismatch:\n  actual:   {actual_groups}\n  expected: {expected_device_groups}")

    # Variant toggles: one questWorldDataManagerNodeDefinition per variant_toggles
    # entry, each carrying exactly the spec's prefab + show map.
    expected_toggles = [
        (t["prefab"], dict(t["states"]))
        for v in venue_spec["venues"] for t in v.get("variant_toggles", [])
    ]
    toggle_nodes = [
        n["Data"] for n in nodes
        if n["Data"].get("$type") == "questWorldDataManagerNodeDefinition"
    ]
    ok(len(toggle_nodes) == len(expected_toggles),
       f"expected {len(expected_toggles)} variant toggle nodes, found {len(toggle_nodes)}")
    actual_toggles = []
    for t_node in toggle_nodes:
        typ = t_node.get("type", {}).get("Data", {})
        ok(typ.get("$type") == "questTogglePrefabVariant_NodeType",
           "variant toggle node type is not questTogglePrefabVariant_NodeType")
        for p in typ.get("params", []):
            ok(p.get("$type") == "questTogglePrefabVariant_NodeTypeParams",
               "variant toggle param type mismatch")
            states = {s["name"]["$value"]: s["show"] for s in p.get("variantStates", [])}
            actual_toggles.append((p.get("prefabNodeRef", {}).get("$value"), states))
    ok(actual_toggles == expected_toggles,
       f"venue_probe variant toggles mismatch:\n  actual:   {actual_toggles}\n  expected: {expected_toggles}")

    # Proximity waits: one questPauseConditionNodeDefinition with a
    # questDistanceCondition per venue proximity_wait, waiting for the player to
    # come within the spec radius of the spec node.
    expected_prox = [
        (v["proximity_wait"]["ref"], float(v["proximity_wait"]["within"]))
        for v in venue_spec["venues"] if "proximity_wait" in v
    ]
    actual_prox = []
    for n in nodes:
        d = n["Data"]
        if d.get("$type") != "questPauseConditionNodeDefinition":
            continue
        cond = d.get("condition", {}).get("Data", {})
        if cond.get("$type") != "questDistanceCondition":
            continue
        typ = cond.get("type", {}).get("Data", {})
        ok(typ.get("$type") == "questDistanceComparison_ConditionType",
           "proximity condition type is not questDistanceComparison_ConditionType")
        ok(typ.get("comparisonType") == "Less",
           "proximity condition comparisonType must be Less (player within radius)")
        d1 = typ.get("distanceDefinition1", {}).get("Data", {})
        d2 = typ.get("distanceDefinition2", {}).get("Data", {})
        ok(d1.get("$type") == "questObjectDistance", "proximity distanceDefinition1 must be questObjectDistance")
        ok(d1.get("entityRef", {}).get("Data", {}).get("refLocalPlayer") == 1,
           "proximity entityRef must reference the local player")
        ok(d2.get("$type") == "questValueDistance", "proximity distanceDefinition2 must be questValueDistance")
        actual_prox.append((
            d1.get("nodeRef2", {}).get("reference", {}).get("$value"),
            float(d2.get("distanceValue")),
        ))
    ok(actual_prox == expected_prox,
       f"venue_probe proximity waits mismatch:\n  actual:   {actual_prox}\n  expected: {expected_prox}")

    # Communities: exact multiset match.
    actual_comms = set()
    for n in nodes:
        d = n["Data"]
        if d.get("$type") != "questSpawnManagerNodeDefinition":
            continue
        for act in d.get("actions", []):
            at = act.get("type", {}).get("Data", {})
            if at.get("$type") == "questCommunityTemplate_NodeType":
                actual_comms.add((
                    at.get("action"),
                    at.get("spawnerReference", {}).get("$value"),
                    at.get("communityEntryName", {}).get("$value"),
                    at.get("communityEntryPhaseName", {}).get("$value"),
                ))
    expected_comms = {
        (c["action"], c["spawner"], c.get("entry_name", "None"), c.get("phase_name", "None"))
        for v in venue_spec["venues"] for c in v.get("communities", [])
    }
    ok(actual_comms == expected_comms,
       f"venue_probe communities mismatch:\n  actual:   {sorted(actual_comms)}\n  expected: {sorted(expected_comms)}")

    # Owner constraint: prefabs/doors/communities ONLY, never quest content.
    all_refs = _collect_phase_refs(rc)
    bad_refs = sorted({r for r in all_refs if any(p in r for p in venue_spec["forbidden_phase_patterns"])})
    ok(not bad_refs, f"venue_probe declares forbidden phase refs: {bad_refs}")

    # A prefab declared twice can break phase instantiation, which silently
    # disables every community and device action in the phase.
    ven_prefabs = [e["prefabNodeRef"]["$value"] for e in rc.get("phasePrefabs", [])]
    dup_prefabs = sorted({p for p in ven_prefabs if ven_prefabs.count(p) > 1})
    ok(not dup_prefabs, f"venue_probe declares duplicate phasePrefabs (breaks instantiation): {dup_prefabs}")
    cast_doc = resources.get("mod\\neon_ascendancy\\cast_and_hubs.questphase")
    if cast_doc:
        cast_prefabs = {e["prefabNodeRef"]["$value"]
                        for e in cast_doc["Data"]["RootChunk"].get("phasePrefabs", []) or []}
        shared = sorted(set(ven_prefabs) & cast_prefabs)
        ok(not shared,
           f"venue_probe and cast_and_hubs both declare these prefabs (prefab must be owned by one phase): {shared}")
    for d_node in device_nodes:
        for p in d_node.get("type", {}).get("Data", {}).get("params", []):
            controller = p["Data"].get("deviceControllerClass", {}).get("$value", "")
            # Doors are always allowed; the spec may additionally opt in specific
            # non-door controllers (lift/window/platform/terminal) a route needs.
            ok(controller.startswith("Door") or controller in set(venue_spec.get("allowed_device_controllers", [])),
               f"venue_probe device controller {controller} is not a door and not in allowed_device_controllers (owner decision)")

    # Keep-alive pause present.
    ka = venue_spec["keep_alive_pause"]
    ka_found = False
    for p in nodes:
        d = p["Data"]
        if d.get("$type") != "questPauseConditionNodeDefinition":
            continue
        typ = d.get("condition", {}).get("Data", {}).get("type", {}).get("Data", {})
        if (typ.get("factName") == ka["fact"]
                and typ.get("comparisonType") == ka["comparison_type"]
                and typ.get("value") == ka["value"]):
            ka_found = True
    ok(ka_found, f"venue_probe missing keep-alive pause {ka['fact']} {ka['comparison_type']} {ka['value']}")

    # The dev probe redscript hardcodes these refs (it cannot read JSON at
    # runtime). Fail the build if they drift from the spec so the in-game log
    # always reports on the refs the venue phase actually addresses.
    probe_src = ROOT / "src" / "r6" / "scripts" / "NeonAscendancy" / "Debug" / "VenueProbe.reds"
    if probe_src.is_file():
        source = probe_src.read_text(encoding="utf-8")
        for v in venue_spec["venues"]:
            pr = v.get("probe_refs", {})
            for key in ("workspot", "door", "community"):
                val = pr.get(key, "")
                ok(not val or val in source,
                   f"VenueProbe.reds is missing probe_refs.{key} for venue {v['code']}: {val}")

    # ascendancy.questphase: gate pause -> venue probe phase node, gated on the fact.
    qp_doc = resources["mod\\neon_ascendancy\\ascendancy.questphase"]
    qp_nodes = qp_doc["Data"]["RootChunk"]["graph"]["Data"]["nodes"]
    gate = venue_spec["gate"]
    gate_pauses = []
    for p in qp_nodes:
        d = p["Data"]
        if d.get("$type") != "questPauseConditionNodeDefinition":
            continue
        typ = d.get("condition", {}).get("Data", {}).get("type", {}).get("Data", {})
        if (typ.get("factName") == gate["fact"]
                and typ.get("comparisonType") == gate["comparison_type"]
                and typ.get("value") == gate["value"]):
            gate_pauses.append(p)
    ok(len(gate_pauses) == 1,
       f"expected 1 venue gate pause ({gate['fact']} {gate['comparison_type']} {gate['value']}), "
       f"found {len(gate_pauses)}")
    venue_phases = [
        p for p in qp_nodes
        if p["Data"].get("$type") == "questPhaseNodeDefinition"
        and p["Data"].get("phaseResource", {}).get("DepotPath", {}).get("$value") == venue_spec["phase_resource"]
    ]
    ok(len(venue_phases) == 1, f"expected 1 venue probe phase node, found {len(venue_phases)}")
    if gate_pauses and venue_phases:
        edges = _graph_edges(qp_nodes)
        gate_id = id_of(gate_pauses[0])
        venue_id = id_of(venue_phases[0])
        ok((gate_id, venue_id) in edges, "venue gate pause is not connected to the venue probe phase node")
        gate_in = _socket_handle(gate_pauses[0]["Data"]["sockets"][1])
        gate_out = _socket_handle(gate_pauses[0]["Data"]["sockets"][2])
        ok(_count_connections(qp_doc["Data"]["RootChunk"], gate_in) == (1, 0),
           "venue gate In must have exactly 1 incoming connection")
        ok(_count_connections(qp_doc["Data"]["RootChunk"], gate_out) == (0, 1),
           "venue gate Out must have exactly 1 outgoing connection")

    # The dev probe fact must stay runtime-only: no archive resource may set it.
    for rel in ("mod\\neon_ascendancy\\ascendancy.questphase", venue_spec["phase_resource"]):
        setvars = [f for f, _ in _collect_setvar_facts(resources[rel]["Data"]["RootChunk"])]
        ok(gate["fact"] not in setvars,
           f"{rel} sets {gate['fact']} via questSetVar_NodeType; it must stay DevDebug-only")
    spec_facts = {f["fact"] for f in spec["questphase"]["initial_facts"]}
    ok(gate["fact"] not in spec_facts, f"{gate['fact']} must not be declared in initial_facts")


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
    cast_spec = load_cast_spec(spec)
    ft_spec = load_ft_spec(cast_spec)
    venue_spec = load_venue_spec(cast_spec)
    barricade_spec = load_barricade_spec(cast_spec)
    vendors_spec = load_dogtown_vendors_spec(cast_spec)
    tower_spec = load_tower_population_spec(cast_spec)

    if args.check:
        check(args, spec, cast_spec, ft_spec, venue_spec, barricade_spec, vendors_spec, tower_spec)
    else:
        archive = build(args, spec, cast_spec, ft_spec, venue_spec, barricade_spec, vendors_spec, tower_spec)
        print(f"\nBuilt {archive} ({archive.stat().st_size} bytes).")
        print("Run `python3 tools/build-clean-slate.py --check` to verify the round-trip.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
