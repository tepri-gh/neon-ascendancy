#!/usr/bin/env python3
"""Extract deterministic living-world *site* seeds into data/sites/*.json.

Builds directly on the existing `tools/extract-world.py` output
(`dist/extract/areas.jsonl`, `markers.jsonl`, and the compiled community
registry in `dist/extract/raw/.../always_loaded_1.streamingsector.json`) plus
targeted, read-only WolvenKit.CLI reads of the installed game:

  1. Site `.questphase` resources under
     `base\\open_world\\{minor_activities,street_stories,mini_world_stories}`
     and `ep1\\openworld\\{street_stories,mini_world_stories}`:
     `phasePrefabs[0].prefabNodeRef`, community activations
     (`questCommunityTemplate_NodeType`) and door/device actions
     (`questDeviceManager_NodeType`).
  2. `blocks/all.streamingblock` (base + EP1): prefab NodeRef -> quest sector
     path, category and prefab variants.
  3. Every matched Quest-category `.streamingsector`: `worldAISpotNode`,
     `worldPatrolSplineNode`, `worldGuardAreaNode`, `worldDeviceNode`,
     `worldTriggerAreaNode`, `worldInteriorMapNode` / `worldInteriorAreaNode`.

Nothing is written outside `data/sites/` and `dist/sites/`; phase and sector
conversion batches are parsed and deleted immediately so peak disk stays small.

Determinism: records are sorted by stable natural keys, floats are rounded,
JSON keys are sorted, and every emitted file is byte-identical across runs.
Inventory bounds are asserted; failures abort instead of shipping a guess.

NodeRef identity: a sector's `nodeRefs[]` strings are the authoring keys. Their
compiled 64-bit hash is FNV-1a over the path with '#' removed, which is exactly
what `nodeData[].globalNodeId.hash` stores, so both keys are reproduced here
instead of being re-derived at runtime.
"""

from __future__ import annotations

import argparse
import collections
import importlib.util
import json
import math
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUT_DIR = DATA_DIR / "sites"
WORK_DIR = ROOT / "dist" / "sites"
CACHE_DIR = WORK_DIR / "cache"
TMP_DIR = WORK_DIR / "tmp"
EXTRACT_DIR = ROOT / "dist" / "extract"

GAME_VERSION = "2.5"

DEFAULT_GAME_DIR = Path(os.environ.get("GAME_DIR", Path.home() / "Games" / "Cyberpunk 2077"))
DEFAULT_CACHE_ROOT = Path(os.environ.get("CACHE_DIR", Path.home() / ".cache" / "neon-ascendancy"))

ARCHIVES = {
    "base_world": Path("archive/pc/content/basegame_3_nightcity.archive"),
    "base_data": Path("archive/pc/content/basegame_4_gamedata.archive"),
    "ep1_world": Path("archive/pc/ep1/ep1_1_nightcity.archive"),
    "ep1_data": Path("archive/pc/ep1/ep1_2_gamedata.archive"),
}

BASE_BLOCK = r"base\worlds\03_night_city\_compiled\default\blocks\all.streamingblock"
EP1_BLOCK = r"base\worlds\03_night_city\_compiled\default\ep1\blocks\all.streamingblock"

# Canonical sub-district geocodes. A site code is only canonical when its
# (district, subdistrict) token pair is listed here; this is what keeps
# sub-phases and cut variant directories from inflating site counts.
GEO_TOKENS: dict[str, frozenset[str]] = {
    "wat": frozenset({"nid", "kab", "lch", "ich"}),
    "wbr": frozenset({"jpn", "hil", "nok"}),
    "hey": frozenset({"gle", "rey", "spr"}),
    "std": frozenset({"arr", "rcr"}),
    "pac": frozenset({"cvi", "wwd"}),
    "cct": frozenset({"cpz", "dtn"}),
    "bls": frozenset({"ina", "se5"}),
    "off": frozenset({"work"}),
}

MA_RE = re.compile(r"^ma_([a-z]{3})_([a-z]{3})_(\d{1,3})$")
STS_RE = re.compile(r"^sts_([a-z]{3})_([a-z]{3})_(\d{1,3})$")
STS_EP1_RE = re.compile(r"^sts_ep1_(\d{2})(?:_[a-z0-9]+)*$")
MWS_RE = re.compile(r"^mws_[a-z0-9]+(?:_[a-z0-9]+)*$")

SITE_ROOT_MARKERS = ("minor_activities", "street_stories", "mini_world_stories")

SITE_KIND_BY_FAMILY = {
    "ma": "scanner_hustle",
    "sts": "fixer_gig",
    "sts_ep1": "fixer_gig",
    "mws": "mini_world_story",
}

SUITABILITIES = (
    "raid_target", "stealth_entry", "sniper_nest", "vehicle_bay",
    "rooftop_access", "sewer_access", "elevator", "hostage_site",
    "officer_site", "arms_cache", "data_vault", "terminal_cluster",
    "turret_cluster", "camera_net", "safehouse", "chop_shop",
    "netrunner_den", "clinic", "club", "warehouse", "branch_office",
    "market_stall", "lab",
)

DEVICE_CONTROLLER_CLASS = {
    "security_area": "SecurityAreaControllerPS",
    "security_system": "SecuritySystemControllerPS",
    "camera": "CameraControllerPS",
    "turret": "SecurityTurretControllerPS",
    "terminal": "TerminalControllerPS",
    "computer": "ComputerControllerPS",
    "door": "DoorControllerPS",
    "gate": "DoorControllerPS",
    "lift": "LiftControllerPS",
    "vending": "VendingMachineControllerPS",
    "speaker": "SpeakerControllerPS",
    "tv": "TVControllerPS",
    "other": "DeviceControllerPS",
}

# Longest-first so `security_area` wins over `security_system`, etc.
DEVICE_TEMPLATE_RULES: tuple[tuple[str, str], ...] = (
    ("security_area", "security_area"),
    ("security_system", "security_system"),
    ("security_camera", "camera"),
    ("security_cameras", "camera"),
    ("surveillance_camera", "camera"),
    ("camera", "camera"),
    ("security_turret", "turret"),
    ("turret", "turret"),
    ("terminal", "terminal"),
    ("computer", "computer"),
    ("personal_link", "computer"),
    ("door", "door"),
    ("gate", "gate"),
    ("elevator", "lift"),
    ("lift", "lift"),
    ("vending", "vending"),
    ("speaker", "speaker"),
    ("television", "tv"),
    ("tv", "tv"),
)

DOOR_ROLE_RULES: tuple[tuple[str, str], ...] = (
    ("garage", "garage"),
    ("roof", "roof"),
    ("service", "service"),
    ("elevator", "elevator"),
    ("lift", "elevator"),
    ("entrance", "entrance"),
    ("entry", "entrance"),
    ("exit", "exit"),
    ("back", "interior"),
)

SPOT_ROLE_RULES: tuple[tuple[str, str], ...] = (
    ("guard", "guard"),
    ("sniper", "sniper"),
    ("patrol", "patrol"),
    ("sleep", "sleep"),
    ("bed", "sleep"),
    ("sit", "sit"),
    ("chair", "sit"),
    ("bench", "sit"),
    ("couch", "sit"),
    ("drug", "drug"),
    ("smoke", "drug"),
    ("kneel", "drug"),
    ("dance", "dance"),
    ("drink", "drink"),
    ("bottle", "drink"),
    ("bar_", "drink"),
    ("eat", "eat"),
    ("food", "eat"),
    ("inspect", "inspect"),
    ("search", "search"),
    ("loot", "inspect"),
    ("cover", "cover"),
    ("drive", "driver"),
    ("vehicle", "driver"),
    ("typing", "work"),
    ("terminal", "work"),
    ("work", "work"),
    ("desk", "work"),
    ("shelf", "work"),
    ("crowd", "crowd"),
    ("idle", "idle"),
    ("stand", "idle"),
)

OFFICER_TOKENS = ("officer", "boss", "leader", "jotaro", "miniboss", "chief", "lieutenant", "captain", "sergeant")
VIP_TOKENS = ("target", "vip", "celebrity", "politician", "exec")
SNIPER_TOKENS = ("sniper", "sniping", "marksman")
NETRUNNER_TOKENS = ("netrunner", "hacker", "techie")
MEDIC_TOKENS = ("medic", "ripper", "doctor", "trauma")
CIVILIAN_TOKENS = ("civilian", "citizen", "victim", "hostage", "client", "vendor", "barman", "stripper", "guest", "gamer", "waitress", "clerk")
DRIVER_TOKENS = ("driver", "wheelman")
MELEE_TOKENS = ("melee", "blade", "katana", "mantis", "sledge", "knife", "strongarms", "fists", "hmelee")
RANGED_TOKENS = ("ranged", "handgun", "rifle", "shotgun", "saratoga", "shingen", "lexington", "hmg", "lmg", "smg", "gunner", "sniper_rifle")
GRUNT_TOKENS = (
    "enemy", "gang", "guard", "tyger", "maelstrom", "valentino", "scav",
    "animal", "wraith", "barghest", "voodoo", "sixth", "soldier", "merc",
)

CLINIC_TOKENS = ("clinic", "ripper", "medical", "medic", "hospital")
CLUB_TOKENS = ("club", "casino", "bar", "strip", "dance", "nightclub", "lounge")
WAREHOUSE_TOKENS = ("warehouse", "depot", "storage", "factory", "cargo", "garage", "hangar")
OFFICE_TOKENS = ("office", "corpo", "corp_", "tower", "hq", "headquarter", "branch")
MARKET_TOKENS = ("market", "shop", "store", "vendor", "stall", "kiosk")
LAB_TOKENS = ("lab", "research", "clinic", "ripper")

# Gig/prefab names that denote a roofed, enterable venue. Used only as a
# fallback for sites whose Quest sector carries no explicit interior volume
# node; exterior families (ma_*) never use it.
INTERIOR_VENUE_TOKENS = (
    "casino", "bar", "club", "clinic", "ripperdoc", "penthouse", "apartment",
    "hotel", "office", "lab", "warehouse", "shop", "store", "restaurant",
    "tower", "mall", "market", "stadium", "arena", "bunker", "vault",
    "factory", "depot", "garage", "hideout", "safehouse",
)

AREA_MIN_Z = -200.0
AREA_MAX_Z = 1000.0

WOLVENKIT_VERSION = "10.0.0-beta.1"


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def load_extract_world() -> Any:
    """Reuse extract-world.py's tweak parser and faction catalog (single source)."""
    path = ROOT / "tools" / "extract-world.py"
    spec = importlib.util.spec_from_file_location("neon_extract_world", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def r3(value: float | None) -> float | None:
    if value is None:
        return None
    if not math.isfinite(value):
        raise ValueError(f"Non-finite coordinate: {value}")
    return round(float(value), 3)


def clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def win_path(path: Path | str) -> str:
    """Resource paths are authored with backslashes; normalise host separators."""
    return str(path).replace("/", "\\")


def fs_path(root: Path, win_rel: str) -> Path:
    """Turn an authored backslash resource path into a host filesystem path."""
    return root.joinpath(*[part for part in win_rel.split("\\") if part])


def fnv1a64(text: str) -> int:
    """RED4ext NodeRef hash: FNV-1a 64-bit over the path with '#' removed."""
    h = 0xCBF29CE484222325
    for byte in text.replace("#", "").encode("utf-8"):
        h ^= byte
        h = (h * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return h


def node_leaf(ref: str) -> str:
    """Last authored name of a NodeRef path ('.../#kab_07_com_enemies' -> '#kab_07_com_enemies')."""
    leaf = ref.replace("\\", "/").split("/")[-1]
    if leaf.startswith("~/"):
        leaf = leaf.rsplit("/", 1)[-1]
    return leaf if leaf.startswith("#") else f"#{leaf}"


def node_name(ref: str) -> str:
    return node_leaf(ref).lstrip("#")


def json_value(handle: Any) -> Any:
    """Unwrap {'$value': ...} handles."""
    if isinstance(handle, dict) and "$value" in handle:
        return handle["$value"]
    return handle


def cname_handle(handle: Any) -> str | None:
    value = json_value(handle)
    if value is None:
        return None
    text = str(value)
    return text or None


def normalize_hour(raw: Any) -> str:
    """Map vanilla time-of-day enums and clock tokens onto the schema vocabulary."""
    text = str(raw or "").strip()
    if text in ("Day", "Night", "Morning", "Evening", "Any"):
        return text
    match = re.search(r"(?:^|_)(\d{1,2})_00", text)
    if match:
        hour = int(match.group(1))
        if 0 <= hour < 6:
            return "Night"
        if hour < 12:
            return "Morning"
        if hour < 18:
            return "Day"
        return "Evening"
    return "Any"


def quat_yaw(orientation: dict[str, Any] | None) -> float | None:
    if not orientation:
        return None
    i = float(orientation.get("i", 0.0))
    j = float(orientation.get("j", 0.0))
    k = float(orientation.get("k", 0.0))
    r = float(orientation.get("r", 1.0))
    yaw = math.atan2(2.0 * (r * k + i * j), 1.0 - 2.0 * (j * j + k * k))
    return round(yaw, 4)


def write_rows(name: str, rows: Iterable[dict[str, Any]]) -> int:
    """One readable JSON object per line inside a JSON array (deterministic)."""
    materialised = [json.dumps(row, sort_keys=True, ensure_ascii=False) for row in rows]
    body = ",\n".join(materialised)
    text = "[\n" + body + "\n]\n" if materialised else "[]\n"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / name).write_text(text, encoding="utf-8")
    return len(materialised)


def write_object(name: str, obj: dict[str, Any]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / name).write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def chunked(items: list[Any], size: int) -> Iterable[list[Any]]:
    for start in range(0, len(items), size):
        yield items[start:start + size]


# ---------------------------------------------------------------------------
# WolvenKit
# ---------------------------------------------------------------------------


class WolvenKit:
    def __init__(self, game_dir: Path, cache_root: Path) -> None:
        self.game_dir = game_dir
        self.binary = cache_root / f"wolvenkit-{WOLVENKIT_VERSION}" / "WolvenKit.CLI"
        if not self.binary.is_file():
            raise FileNotFoundError(f"WolvenKit.CLI not found at {self.binary}")

    def run(self, args: list[str]) -> None:
        env = {**os.environ, "DOTNET_ROLL_FORWARD": "Major"}
        proc = subprocess.run(
            [str(self.binary), *args], env=env, capture_output=True, text=True
        )
        if proc.returncode != 0:
            raise RuntimeError(
                f"WolvenKit.CLI failed (rc={proc.returncode}): {' '.join(args)}\n"
                f"stdout:\n{proc.stdout[-2000:]}\nstderr:\n{proc.stderr[-2000:]}"
            )

    def archive(self, key: str) -> Path:
        path = self.game_dir / ARCHIVES[key]
        if not path.is_file():
            raise FileNotFoundError(f"Missing game archive: {path}")
        return path

    def listing(self, key: str) -> list[str]:
        archive = self.archive(key)
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache = CACHE_DIR / f"listing_{key}.txt"
        if not cache.is_file() or cache.stat().st_mtime < archive.stat().st_mtime:
            env = {**os.environ, "DOTNET_ROLL_FORWARD": "Major"}
            proc = subprocess.run(
                [str(self.binary), "archive", "-l", str(archive)],
                env=env, capture_output=True, text=True,
            )
            if proc.returncode != 0:
                raise RuntimeError(f"WolvenKit archive -l failed for {archive}: {proc.stderr[-1000:]}")
            lines = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
            cache.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return [ln for ln in cache.read_text(encoding="utf-8").splitlines() if ln.strip()]

    def extract(
        self, key: str, out_dir: Path, pattern: str | None = None, regex: str | None = None
    ) -> None:
        out_dir.mkdir(parents=True, exist_ok=True)
        args = ["extract", str(self.archive(key)), "-o", str(out_dir), "-v", "Minimal"]
        if pattern:
            args += ["-w", pattern]
        if regex:
            args += ["-r", regex]
        self.run(args)

    def convert(self, path: Path) -> None:
        self.run(["convert", "s", str(path), "-v", "Minimal"])


# ---------------------------------------------------------------------------
# Site inventory
# ---------------------------------------------------------------------------


def canonical_site_code(segment: str) -> str | None:
    """Map a directory name to a canonical site code, or None."""
    name = segment[4:] if segment.startswith("loc_") else segment
    match = MA_RE.match(name)
    if match and match.group(2) in GEO_TOKENS.get(match.group(1), frozenset()):
        return name
    match = STS_RE.match(name)
    if match and match.group(2) in GEO_TOKENS.get(match.group(1), frozenset()):
        return name
    match = STS_EP1_RE.match(name)
    if match:
        return f"sts_ep1_{match.group(1)}"
    if MWS_RE.match(name):
        return name
    return None


def site_code_from_path(path: str) -> str | None:
    """Find the canonical site directory that owns a game resource path."""
    parts = win_path(path).split("\\")
    if len(parts) < 5:
        return None
    if parts[0] == "base" and parts[1] == "open_world" and parts[2] in SITE_ROOT_MARKERS:
        for index in range(3, len(parts) - 1):
            code = canonical_site_code(parts[index])
            if code:
                return code
        return None
    if parts[0] == "ep1" and parts[1] == "openworld":
        for index in range(2, len(parts) - 1):
            code = canonical_site_code(parts[index])
            if code:
                return code
    return None


def site_dir_prefix(path: str) -> str | None:
    """Resource path up to and including the site directory."""
    parts = win_path(path).split("\\")
    for index in range(2, len(parts) - 1):
        if canonical_site_code(parts[index]):
            return "\\".join(parts[: index + 1])
    return None


def family_of(code: str) -> str:
    if code.startswith("ma_"):
        return "ma"
    if code.startswith("sts_ep1_"):
        return "sts_ep1"
    if code.startswith("sts_"):
        return "sts"
    return "mws"


def gather_inventory(listings: dict[str, list[str]]) -> dict[str, dict[str, Any]]:
    """Unique canonical site codes with their resource paths."""
    inventory: dict[str, dict[str, Any]] = {}
    for key, lines in listings.items():
        for line in lines:
            code = site_code_from_path(line)
            if not code:
                continue
            entry = inventory.setdefault(code, {"code": code, "paths": set(), "archives": set()})
            entry["paths"].add(line)
            entry["archives"].add(key)
    for entry in inventory.values():
        prefixes = sorted(
            prefix for prefix in (site_dir_prefix(line) for line in entry["paths"]) if prefix
        )
        entry["prefix"] = prefixes[0] if prefixes else None
    return inventory


def index_resources(listings: dict[str, list[str]]) -> dict[str, Any]:
    """Resource indexes used for bindings and community paths."""
    quests: dict[str, str] = {}
    communities: dict[str, str] = {}
    community_suffix: dict[str, str] = {}
    all_paths = sorted({ln for lines in listings.values() for ln in lines})
    for line in all_paths:
        lower = line.lower()
        stem = line.rsplit("\\", 1)[-1].rsplit(".", 1)[0]
        if lower.endswith(".quest"):
            quests.setdefault(stem, line)
        elif lower.endswith(".community"):
            communities.setdefault(stem, line)
            # Community resources are prefixed with their owning site
            # (`sts_wat_kab_07_com_enemies.community`) while spawners are
            # authored as `#kab_07_com_enemies`; index every token suffix.
            parts = stem.split("_")
            for index in range(len(parts)):
                community_suffix.setdefault("_".join(parts[index:]), line)
    return {"quests": quests, "communities": communities, "community_suffix": community_suffix}


# ---------------------------------------------------------------------------
# Phase parsing
# ---------------------------------------------------------------------------


def iter_nodes(value: Any, wanted: set[str], out: list[dict[str, Any]]) -> None:
    """Collect every dict whose $type is in `wanted` (iterative, no recursion limit)."""
    stack = [value]
    while stack:
        item = stack.pop()
        if isinstance(item, dict):
            if item.get("$type") in wanted:
                out.append(item)
            stack.extend(item.values())
        elif isinstance(item, list):
            stack.extend(item)


def parse_phase(path: Path) -> dict[str, Any]:
    root = json.loads(path.read_text(encoding="utf-8"))["Data"]["RootChunk"]
    prefabs = []
    for entry in root.get("phasePrefabs") or []:
        ref = json_value(entry.get("prefabNodeRef"))
        if ref:
            prefabs.append(str(ref))
    nodes: list[dict[str, Any]] = []
    iter_nodes(root, {"questCommunityTemplate_NodeType", "questDeviceManager_NodeType"}, nodes)
    activations: list[dict[str, Any]] = []
    device_actions: list[dict[str, Any]] = []
    for node in nodes:
        if node["$type"] == "questCommunityTemplate_NodeType":
            ref = json_value(node.get("spawnerReference"))
            if not ref:
                continue
            activations.append({
                "action": str(json_value(node.get("action")) or ""),
                "spawner_ref": node_leaf(str(ref)),
                "entry_name": cname_handle(node.get("communityEntryName")) or "None",
                "entry_phase": cname_handle(node.get("communityEntryPhaseName")) or "None",
            })
        else:
            for param in node.get("params") or []:
                data = param.get("Data") or {}
                action = cname_handle(data.get("deviceAction"))
                if not action:
                    continue
                target = json_value(data.get("objectRef"))
                if not target or str(target) == "0":
                    target = json_value((data.get("entityRef") or {}).get("reference"))
                if not target or str(target) == "0":
                    continue
                device_actions.append({
                    "action": action,
                    "controller_class": cname_handle(data.get("deviceControllerClass")) or "",
                    "node_ref": node_leaf(str(target)),
                })
    return {"prefabs": prefabs, "activations": activations, "device_actions": device_actions}


def collect_phases(wk: WolvenKit, inventory: dict[str, dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Extract + convert every site phase, returning reduced per-code records."""
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    phases_root = TMP_DIR / "phases"
    try:
        wk.extract(
            "base_data",
            phases_root,
            regex=r"^base.open_world.(minor_activities|street_stories|mini_world_stories).*questphase$",
        )
        wk.extract(
            "ep1_data",
            phases_root,
            regex=r"^ep1.openworld.(street_stories|mini_world_stories).*questphase$",
        )
        wk.convert(phases_root)

        by_code: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
        for json_path in sorted(phases_root.rglob("*.questphase.json")):
            rel = win_path(json_path.relative_to(phases_root))[: -len(".json")]
            code = site_code_from_path(rel)
            if not code or code not in inventory:
                continue
            record = parse_phase(json_path)
            record["resource"] = rel
            by_code[code].append(record)
        return by_code
    finally:
        if phases_root.exists():
            shutil.rmtree(phases_root, ignore_errors=True)


# ---------------------------------------------------------------------------
# Streaming blocks
# ---------------------------------------------------------------------------


class BlockIndex:
    def __init__(self) -> None:
        self.by_leaf: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)

    def add_block(self, block_path: str, doc: dict[str, Any]) -> None:
        for descriptor in doc["Data"]["RootChunk"].get("descriptors") or []:
            prefab = json_value(descriptor.get("questPrefabNodeRef"))
            sector_path = json_value(((descriptor.get("data") or {}).get("DepotPath") or {}))
            category = str(descriptor.get("category") or "")
            # Unbound descriptors carry a uint64-zero NodeRef; they are not prefabs.
            if not prefab or not sector_path or str(prefab) in ("0", "None"):
                continue
            if category not in ("Quest", "Interior", "Exterior"):
                continue
            self.by_leaf[node_name(str(prefab))].append({
                "block": block_path,
                "sector_path": win_path(str(sector_path)),
                "category": category,
                "prefab_ref": str(prefab),
                "variants": descriptor.get("variants") or [],
            })

    def lookup_leaf(self, leaf: str) -> list[dict[str, Any]]:
        return self.by_leaf.get(leaf.lstrip("#"), [])

    def lookup_code(self, code: str) -> list[dict[str, Any]]:
        # `loc_ma_<code>_openworld` style prefabs embed the code after a '_'.
        pattern = re.compile(r"(?<![a-z0-9])" + re.escape(code) + r"(?![0-9])")
        found: list[dict[str, Any]] = []
        for leaf, descriptors in sorted(self.by_leaf.items()):
            if pattern.search(leaf):
                found.extend(descriptors)
        return found


def load_blocks(wk: WolvenKit) -> BlockIndex:
    blocks_root = CACHE_DIR / "blocks"
    blocks_root.mkdir(parents=True, exist_ok=True)
    if not fs_path(blocks_root, BASE_BLOCK).is_file():
        wk.extract("base_world", blocks_root, pattern="*all.streamingblock")
    if not fs_path(blocks_root, EP1_BLOCK).is_file():
        wk.extract("ep1_world", blocks_root, pattern="*ep1*all.streamingblock")
    for path in sorted(blocks_root.rglob("*.streamingblock")):
        json_path = path.with_suffix(path.suffix + ".json")
        if not json_path.is_file() or json_path.stat().st_mtime < path.stat().st_mtime:
            wk.convert(path)

    index = BlockIndex()
    for block_path in (BASE_BLOCK, EP1_BLOCK):
        json_path = fs_path(blocks_root, block_path + ".json")
        if not json_path.is_file():
            raise FileNotFoundError(f"Missing streaming block JSON: {json_path}")
        index.add_block(block_path, json.loads(json_path.read_text(encoding="utf-8")))
    return index


# ---------------------------------------------------------------------------
# Sector parsing
# ---------------------------------------------------------------------------


def classify_device(entity_template: str | None) -> str:
    text = (entity_template or "").lower().replace("\\", "/")
    for token, kind in DEVICE_TEMPLATE_RULES:
        if token in text:
            return kind
    return "other"


def classify_door_role(debug_name: str, node_ref: str) -> str:
    text = f"{debug_name} {node_ref}".lower()
    for token, role in DOOR_ROLE_RULES:
        if token in text:
            return role
    return "interior"


def classify_spot_role(workspot: str | None, debug_name: str, markings: list[str]) -> str:
    """Classify a workspot from its own file name (not the generic 'workspots' root)."""
    base = ""
    if workspot:
        base = workspot.replace("\\", "/").rsplit("/", 1)[-1].rsplit(".", 1)[0]
    text = " ".join(part for part in (base, debug_name, " ".join(markings)) if part).lower()
    for token, role in SPOT_ROLE_RULES:
        if token in text:
            return role
    return "unknown"


def classify_trigger_role(debug_name: str) -> str:
    text = debug_name.lower()
    if "elevator" in text and "close" in text:
        return "elevator_close"
    if "elevator" in text or "_lift" in text:
        return "elevator"
    if "despawn" in text:
        return "despawn"
    if "ambush" in text:
        return "ambush"
    if "extract" in text or "exfil" in text:
        return "extraction"
    if "entrance" in text or "entry" in text or text.endswith("_ent"):
        return "entry"
    if "patrol" in text:
        return "patrol_gate"
    if "tr_" in text or "trigger" in text or "volume" in text:
        return "mission_volume"
    return "unknown"


def classify_binding_tokens(values: Iterable[str]) -> list[tuple[str, str]]:
    """Content codes evidenced by a sector's NodeRefs and node debug names (mq304, sq011)."""
    found: set[tuple[str, str]] = set()
    for value in values:
        for token in re.findall(r"(?<![a-z0-9])(mq\d{2,3}|sq\d{2,3})(?![0-9])", value.lower()):
            found.add(("mq" if token.startswith("mq") else "sq", token))
    return sorted(found)


def parse_sector(json_path: Path, descriptor: dict[str, Any]) -> dict[str, Any]:
    root = json.loads(json_path.read_text(encoding="utf-8"))["Data"]["RootChunk"]
    nodes = root.get("nodes") or []
    node_data = ((root.get("nodeData") or {}).get("Data")) or []
    node_refs = root.get("nodeRefs") or []

    ref_by_hash: dict[int, str] = {}
    for handle in node_refs:
        ref = json_value(handle)
        if ref:
            ref_by_hash[fnv1a64(str(ref))] = str(ref)

    # Authored prefab path (everything before the first '#segment'), used for
    # venue keywords and provenance. Not a runtime key.
    prefab_path = None
    for ref in sorted(ref_by_hash.values()):
        cut = ref.find("/#")
        if cut > 0:
            prefab_path = ref[:cut]
            break

    instances: dict[int, list[dict[str, Any]]] = collections.defaultdict(list)
    for instance in node_data:
        try:
            instances[int(instance.get("nodeIdx", -1))].append(instance)
        except (TypeError, ValueError):
            continue

    positions: list[tuple[float, float, float]] = []
    for group in instances.values():
        for instance in group:
            pos = ((instance.get("transform") or {}).get("position") or {})
            if "X" not in pos:
                continue
            triple = (float(pos["X"]), float(pos["Y"]), float(pos["Z"]))
            if not all(math.isfinite(v) for v in triple):
                continue
            if triple[2] < AREA_MIN_Z or triple[2] > AREA_MAX_Z:
                continue
            positions.append(triple)

    spots: list[dict[str, Any]] = []
    patrols: list[dict[str, Any]] = []
    guards: list[dict[str, Any]] = []
    devices: list[dict[str, Any]] = []
    triggers: list[dict[str, Any]] = []
    interior = False
    interior_map_coords: str | None = None
    sector_path = descriptor["sector_path"]
    is_quest_sector = descriptor["category"] == "Quest"

    for index, node in enumerate(nodes):
        data = node.get("Data") or {}
        node_type = data.get("$type") or ""
        if not node_type:
            continue
        debug_name = cname_handle(data.get("debugName")) or ""
        for instance in instances.get(index, []):
            transform = instance.get("transform") or {}
            pos = transform.get("position") or {}
            if "X" not in pos:
                continue
            x, y, z = float(pos["X"]), float(pos["Y"]), float(pos["Z"])
            if not all(math.isfinite(v) for v in (x, y, z)):
                continue
            global_hash = int((instance.get("globalNodeId") or {}).get("hash") or 0)
            ref = ref_by_hash.get(global_hash)
            node_ref = node_leaf(ref) if ref else (f"#{debug_name.strip('{}')}" if debug_name else None)
            if not node_ref:
                continue
            global_node_id = str(global_hash) if global_hash else None

            if node_type == "worldAISpotNode":
                spot_data = (data.get("spot") or {}).get("Data") or {}
                resource = json_value((spot_data.get("resource") or {}).get("DepotPath"))
                markings = [cname_handle(m) or "" for m in (data.get("markings") or [])]
                markings = [m for m in markings if m]
                spots.append({
                    "node_ref": node_ref,
                    "global_node_id": global_node_id,
                    "debug_name": debug_name or None,
                    "workspot_resource": str(resource) if resource else None,
                    "spot_role": classify_spot_role(str(resource) if resource else None, debug_name, markings),
                    "markings": markings,
                    "is_workspot_infinite": int(data.get("isWorkspotInfinite") or 0),
                    "is_workspot_static": int(data.get("isWorkspotStatic") or 0),
                    "actor_bodytype": cname_handle(spot_data.get("ActorBodytypeE3")) or None,
                    "x": x, "y": y, "z": z,
                    "yaw": quat_yaw(transform.get("orientation")),
                    "source_sector": sector_path,
                })
            elif node_type == "worldPatrolSplineNode":
                points = []
                for point in data.get("patrolPointDefs") or []:
                    point_data = point.get("Data") or {}
                    ref_value = json_value(point_data.get("node"))
                    if not ref_value:
                        continue
                    points.append({
                        "spot_ref": node_leaf(str(ref_value)),
                        "point_type": str(point_data.get("pointType") or "Workspot"),
                    })
                patrols.append({
                    "node_ref": node_ref,
                    "global_node_id": global_node_id,
                    "debug_name": debug_name or None,
                    "points": points,
                    "x": x, "y": y, "z": z,
                    "source_sector": sector_path,
                })
            elif node_type == "worldGuardAreaNode":
                communities = []
                for entry in data.get("communityEntries") or []:
                    area = entry.get("communityArea") or {}
                    ref_value = json_value(area.get("reference"))
                    if not ref_value or str(ref_value) == "0":
                        continue
                    names = [cname_handle(n) or "" for n in (area.get("names") or [])]
                    communities.append({
                        "community_ref": node_leaf(str(ref_value)),
                        "is_primary": int(entry.get("isPrimary") or 0),
                        "entry_names": [n for n in names if n],
                    })
                pursuit = data.get("pursuitRange")
                guards.append({
                    "node_ref": node_ref,
                    "global_node_id": global_node_id,
                    "debug_name": debug_name or None,
                    "pursuit_range_m": float(pursuit) if isinstance(pursuit, (int, float)) else None,
                    "communities": communities,
                    "x": x, "y": y, "z": z,
                    "source_sector": sector_path,
                })
            elif node_type == "worldDeviceNode":
                template = json_value((data.get("entityTemplate") or {}).get("DepotPath"))
                template_text = str(template) if template else None
                kind = classify_device(template_text)
                connected = None
                for connection in data.get("deviceConnections") or []:
                    class_name = cname_handle(connection.get("deviceClassName")) or ""
                    if class_name != "CommunityProxyPS":
                        continue
                    for ref_handle in connection.get("nodeRefs") or []:
                        ref_value = json_value(ref_handle)
                        if ref_value:
                            connected = node_leaf(str(ref_value))
                            break
                    if connected:
                        break
                devices.append({
                    "node_ref": node_ref,
                    "global_node_id": global_node_id,
                    "debug_name": debug_name or None,
                    "device_kind": kind,
                    "controller_class": DEVICE_CONTROLLER_CLASS.get(kind, "DeviceControllerPS"),
                    "entity_template": template_text,
                    "connected_community_ref": connected,
                    "is_quest_gated": 1 if is_quest_sector else 0,
                    "x": x, "y": y, "z": z,
                    "source_sector": sector_path,
                })
            elif node_type in ("worldTriggerAreaNode", "worldInteriorAreaNode"):
                if node_type == "worldInteriorAreaNode":
                    interior = True
                outline = (data.get("outline") or {}).get("Data") or {}
                points = []
                for point in (outline.get("points") or [])[:32]:
                    points.append([
                        r3(float(point.get("X", 0.0))),
                        r3(float(point.get("Y", 0.0))),
                        r3(float(point.get("Z", 0.0))),
                    ])
                volume = None
                if points:
                    volume = json.dumps(
                        {"height": r3(float(outline.get("height") or 0.0)), "points": points},
                        sort_keys=True, separators=(",", ":"),
                    )
                triggers.append({
                    "node_ref": node_ref,
                    "global_node_id": global_node_id,
                    "debug_name": debug_name or None,
                    "trigger_role": classify_trigger_role(debug_name),
                    "volume_json": volume,
                    "x": x, "y": y, "z": z,
                })
            elif node_type == "worldInteriorMapNode":
                interior = True
                coords = data.get("coords")
                if isinstance(coords, (int, str)):
                    interior_map_coords = str(coords)

    return {
        "sector_path": sector_path,
        "category": descriptor["category"],
        "prefab_ref": descriptor["prefab_ref"],
        "prefab_path": prefab_path,
        "positions": positions,
        "spots": spots,
        "patrols": patrols,
        "guards": guards,
        "devices": devices,
        "triggers": triggers,
        "is_interior": interior,
        "interior_map_coords": interior_map_coords,
        "binding_tokens": classify_binding_tokens(
            list(ref_by_hash.values())
            + [str(node.get("debugName", "")) for node in nodes]
        ),
    }


def collect_sectors(
    wk: WolvenKit, plan: dict[str, dict[str, Any]], batch_size: int
) -> dict[str, dict[str, Any]]:
    """Extract, convert and reduce sectors in throwaway batches."""
    results: dict[str, dict[str, Any]] = {}
    batches = list(chunked(sorted(plan), batch_size))
    for index, batch in enumerate(batches, start=1):
        batch_dir = TMP_DIR / f"sectors_{index:03d}"
        try:
            for archive_key, group in (
                ("base_world", [p for p in batch if "\\ep1\\" not in p]),
                ("ep1_world", [p for p in batch if "\\ep1\\" in p]),
            ):
                if not group:
                    continue
                hashes = []
                for path in group:
                    match = re.search(r"quest_([0-9a-f]+)\.streamingsector$", path)
                    if not match:
                        raise ValueError(f"Unrecognised sector path: {path}")
                    hashes.append(match.group(1))
                wk.extract(
                    archive_key, batch_dir,
                    regex="quest_(" + "|".join(hashes) + r")\.streamingsector$",
                )
            wk.convert(batch_dir)
            for json_path in sorted(batch_dir.rglob("*.streamingsector.json")):
                rel = win_path(json_path.relative_to(batch_dir))[: -len(".json")]
                descriptor = plan.get(rel)
                if descriptor is None:
                    continue
                results[rel] = parse_sector(json_path, descriptor)
            print(f"    sector batch {index}/{len(batches)}: {len(batch)} sectors", flush=True)
        finally:
            if batch_dir.exists():
                shutil.rmtree(batch_dir, ignore_errors=True)
    return results


# ---------------------------------------------------------------------------
# World seeds: territory assignment, links
# ---------------------------------------------------------------------------


class WorldSeeds:
    def __init__(self) -> None:
        self.districts = json.loads((DATA_DIR / "districts.json").read_text(encoding="utf-8"))
        self.sub_territories = json.loads((DATA_DIR / "sub_territories.json").read_text(encoding="utf-8"))
        self.control_centers = json.loads((DATA_DIR / "control_centers.json").read_text(encoding="utf-8"))
        self.st_by_id = {st["sub_territory_id"]: st for st in self.sub_territories}
        self.cc_by_st = {cc["sub_territory_id"]: cc for cc in self.control_centers}
        self.sts_by_district: dict[int, list[dict[str, Any]]] = collections.defaultdict(list)
        for st in self.sub_territories:
            self.sts_by_district[st["district_id"]].append(st)
        self.faction_id_by_code = {
            f["code"]: f["faction_id"]
            for f in json.loads((DATA_DIR / "factions.json").read_text(encoding="utf-8"))
        }

    def assign(self, x: float, y: float) -> tuple[int, int, int, bool]:
        """Return (district_id, sub_territory_id, control_center_id, exact).

        Mirrors build-world-db.py's Voronoi: inside a district bbox, the nearest
        control center of that district wins; non-badlands beats badlands when
        boxes overlap, then distance, then district id.
        """
        candidates: list[tuple[int, float, int, int]] = []
        for district in self.districts:
            if not (
                district["bbox_min_x"] <= x <= district["bbox_max_x"]
                and district["bbox_min_y"] <= y <= district["bbox_max_y"]
            ):
                continue
            best: tuple[float, int] | None = None
            for st in self.sts_by_district.get(district["district_id"], []):
                cc = self.cc_by_st[st["sub_territory_id"]]
                key = ((x - cc["x"]) ** 2 + (y - cc["y"]) ** 2, st["sub_territory_id"])
                if best is None or key < best:
                    best = key
            if best is None:
                continue
            candidates.append((
                1 if district["kind"] == "badlands" else 0,
                best[0], district["district_id"], best[1],
            ))
        if candidates:
            _, _, district_id, sub_territory_id = min(candidates)
            return (
                district_id,
                sub_territory_id,
                self.cc_by_st[sub_territory_id]["control_center_id"],
                True,
            )

        nearest = min(
            (
                (x - self.cc_by_st[st["sub_territory_id"]]["x"]) ** 2
                + (y - self.cc_by_st[st["sub_territory_id"]]["y"]) ** 2,
                st["sub_territory_id"],
            )
            for st in self.sub_territories
        )
        sub_territory_id = nearest[1]
        return (
            self.st_by_id[sub_territory_id]["district_id"],
            sub_territory_id,
            self.cc_by_st[sub_territory_id]["control_center_id"],
            False,
        )

    def owner_faction(self, sub_territory_id: int) -> int | None:
        return self.st_by_id[sub_territory_id].get("initial_owner_faction_id")

    def nearest_site_links(self, sites: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Two nearest neighbours inside the same sub-territory become reinforcement links."""
        by_st: dict[int, list[dict[str, Any]]] = collections.defaultdict(list)
        for site in sites:
            if site.get("sub_territory_id") is not None:
                by_st[site["sub_territory_id"]].append(site)
        rows: list[dict[str, Any]] = []
        for stid in sorted(by_st):
            group = sorted(by_st[stid], key=lambda s: s["site_id"])
            for site in group:
                neighbours = []
                for other in group:
                    if other["site_id"] == site["site_id"]:
                        continue
                    distance = math.hypot(
                        other["anchor_x"] - site["anchor_x"], other["anchor_y"] - site["anchor_y"]
                    )
                    neighbours.append((round(distance, 2), other["site_id"]))
                for distance, other_id in sorted(neighbours)[:2]:
                    rows.append({
                        "from_site_id": site["site_id"],
                        "to_site_id": other_id,
                        "link_kind": "reinforcement",
                        "weight": clamp(int(1000 - distance), 50, 1000),
                        "distance_m": distance,
                    })
        return rows


# ---------------------------------------------------------------------------
# Community registry
# ---------------------------------------------------------------------------


def load_registry() -> dict[int, dict[str, Any]]:
    path = EXTRACT_DIR / "raw" / "base" / "worlds" / "03_night_city" / "_compiled" / "default" / "always_loaded_1.streamingsector.json"
    if not path.is_file():
        raise FileNotFoundError(
            f"Missing compiled community registry: {path}\nRun tools/extract-world.py first."
        )
    root = json.loads(path.read_text(encoding="utf-8"))["Data"]["RootChunk"]
    registry: dict[int, dict[str, Any]] = {}
    for node in root.get("nodes", []):
        data = node.get("Data") or {}
        if data.get("$type") != "worldCommunityRegistryNode":
            continue
        for item in data.get("communitiesData") or []:
            community_hash = int((item.get("communityId") or {}).get("entityId", {}).get("hash") or 0)
            if not community_hash:
                continue
            initial = {}
            for entry in item.get("entriesInitialState") or []:
                name = cname_handle(entry.get("entryName"))
                if name:
                    initial[name] = {
                        "active": int(entry.get("entryActiveOnStart") or 0),
                        "phase": cname_handle(entry.get("initialPhaseName")),
                    }
            entries = []
            for entry in (((item.get("template") or {}).get("Data") or {}).get("entries") or []):
                entry_data = entry.get("Data") or {}
                name = cname_handle(entry_data.get("entryName"))
                if not name:
                    continue
                phases = []
                for phase in entry_data.get("phases") or []:
                    phase_data = phase.get("Data") or {}
                    periods = []
                    for period in phase_data.get("timePeriods") or []:
                        periods.append({
                            "hour": normalize_hour(period.get("hour")),
                            "quantity": int(period.get("quantity") or 0),
                            "is_sequence": int(period.get("isSequence") or 0),
                            "markings": [cname_handle(m) or "" for m in (period.get("markings") or [])],
                            "spots": [
                                node_leaf(str(value))
                                for value in (json_value(r) for r in (period.get("spotNodeRefs") or []))
                                if value
                            ],
                        })
                    phases.append({
                        "name": cname_handle(phase_data.get("phaseName")) or "default",
                        "always_spawned": str(phase_data.get("alwaysSpawned") or "default__false_"),
                        "periods": periods,
                    })
                entries.append({
                    "name": name,
                    "record": cname_handle(entry_data.get("characterRecordId")),
                    "spawn_in_view": 1 if "true" in str(entry_data.get("spawnInView", "")).lower() else 0,
                    "phases": phases,
                })
            registry[community_hash] = {
                "area_type": str(item.get("communityAreaType") or "") or None,
                "initial": initial,
                "entries": entries,
            }
        break
    if len(registry) < 10000:
        raise RuntimeError(
            f"Community registry has only {len(registry)} communities (expected >= 10000)."
        )
    return registry


def load_jsonl_by_name(filename: str) -> dict[str, list[dict[str, Any]]]:
    path = EXTRACT_DIR / filename
    if not path.is_file():
        raise FileNotFoundError(f"Missing {path}\nRun tools/extract-world.py first.")
    by_name: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            name = (row.get("debug_name") or "").strip("{}")
            if name:
                by_name[name].append(row)
    return by_name


# ---------------------------------------------------------------------------
# Classification helpers
# ---------------------------------------------------------------------------


def role_hint(entry_name: str, record: str | None) -> str:
    text = f"{entry_name} {record or ''}".lower()
    if any(token in text for token in OFFICER_TOKENS):
        return "boss" if any(t in text for t in ("boss", "jotaro")) else "officer"
    if any(token in text for token in VIP_TOKENS):
        return "boss"
    if any(token in text for token in SNIPER_TOKENS):
        return "sniper"
    if any(token in text for token in NETRUNNER_TOKENS):
        return "netrunner"
    if any(token in text for token in MEDIC_TOKENS):
        return "medic"
    if any(token in text for token in DRIVER_TOKENS):
        return "driver"
    if any(token in text for token in CIVILIAN_TOKENS):
        return "civilian"
    if any(token in text for token in MELEE_TOKENS):
        return "melee"
    if any(token in text for token in RANGED_TOKENS):
        return "ranged"
    if any(token in text for token in GRUNT_TOKENS):
        return "grunt"
    return "unknown"


def contains_any(text: str, tokens: Iterable[str]) -> bool:
    return any(token in text for token in tokens)


def build_suitabilities(site: dict[str, Any], ctx: dict[str, Any]) -> list[dict[str, Any]]:
    """Deterministic intent scores derived from extracted facts only."""
    scores: dict[str, int] = {}
    text = " ".join(ctx["keywords"]).lower()
    spots = ctx["role_counts"]
    devices = ctx["device_counts"]
    doors = ctx["door_count"]
    door_roles = ctx.get("door_roles", collections.Counter())
    patrols = ctx["patrol_count"]
    officers = ctx["officer_count"]
    terminals = devices.get("terminal", 0) + devices.get("computer", 0)
    cameras = devices.get("camera", 0)
    turrets = devices.get("turret", 0)
    lifts = devices.get("lift", 0) + door_roles.get("elevator", 0)
    security = devices.get("security_area", 0) + devices.get("security_system", 0)
    interior = bool(site["is_interior"])

    if patrols or ctx["spot_count"] >= 2:
        scores["raid_target"] = clamp(45 + 6 * min(patrols, 4) + 3 * min(ctx["spot_count"], 10), 0, 95)
    if interior or security:
        scores["stealth_entry"] = clamp(50 + 5 * min(doors, 5) + (10 if security else 0), 0, 95)
    if spots.get("sniper", 0):
        scores["sniper_nest"] = clamp(
            55 + 8 * min(spots["sniper"], 3) + (10 if site["anchor_z"] > 15 else 0), 0, 95
        )
    if officers:
        scores["officer_site"] = clamp(50 + 10 * min(officers, 4), 0, 95)
    if terminals:
        scores["terminal_cluster"] = clamp(45 + 12 * min(terminals, 4), 0, 95)
    if interior and terminals >= 1:
        scores["data_vault"] = clamp(50 + 10 * min(terminals, 4), 0, 95)
    if cameras >= 1 or security >= 1:
        scores["camera_net"] = clamp(45 + 8 * min(cameras + security, 5), 0, 95)
    if turrets:
        scores["turret_cluster"] = clamp(55 + 10 * min(turrets, 4), 0, 95)
    if spots.get("inspect", 0) or contains_any(text, ("stash", "cache", "loot", "weapon", "arms")):
        scores["arms_cache"] = clamp(50 + 6 * min(spots.get("inspect", 0) + 1, 5), 0, 90)
    if door_roles.get("garage", 0) or contains_any(text, ("garage", "vehicle", "_car", "car_", "_bay", "parking")):
        scores["vehicle_bay"] = 65
    if not interior and site["anchor_z"] >= 8.0:
        scores["rooftop_access"] = clamp(int(50 + min(30.0, site["anchor_z"])), 0, 95)
    if site["anchor_z"] <= -6.0:
        scores["sewer_access"] = clamp(int(55 + min(25.0, -site["anchor_z"])), 0, 95)
    if lifts:
        scores["elevator"] = 70
    if spots.get("crowd", 0) or contains_any(text, ("hostage", "victim", "vip", "kidnap")):
        scores["hostage_site"] = 60 if interior else 50
    if contains_any(text, CLINIC_TOKENS):
        scores["clinic"] = 70 if interior else 60
    if contains_any(text, CLUB_TOKENS):
        scores["club"] = 70 if interior else 55
    if contains_any(text, WAREHOUSE_TOKENS):
        scores["warehouse"] = 65
    if contains_any(text, OFFICE_TOKENS) or (interior and site["site_kind"] == "fixer_gig" and ctx["device_count"] >= 1):
        scores["branch_office"] = 60 if interior else 45
    if contains_any(text, MARKET_TOKENS):
        scores["market_stall"] = 60
    if contains_any(text, LAB_TOKENS):
        scores["lab"] = 60
    if interior and site["site_kind"] in ("fixer_gig", "mini_world_story"):
        scores["safehouse"] = clamp(45 + 6 * min(doors, 5) + (10 if lifts else 0), 0, 90)
    if interior and (lifts or contains_any(text, ("garage", "vehicle", "warehouse", "depot"))):
        scores["chop_shop"] = 55
    if interior and (devices.get("computer", 0) or terminals >= 1):
        scores["netrunner_den"] = 60

    return [
        {"site_id": site["site_id"], "suitability": name, "score": int(score)}
        for name, score in sorted(scores.items())
        if name in SUITABILITIES and 0 <= score <= 100
    ]


# ---------------------------------------------------------------------------
# Main build
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract living-world site seeds into data/sites/*.json.")
    parser.add_argument("--game-dir", type=Path, default=DEFAULT_GAME_DIR)
    parser.add_argument("--cache-root", type=Path, default=DEFAULT_CACHE_ROOT)
    parser.add_argument("--limit", type=int, default=0, help="Debug: only process the first N sites.")
    parser.add_argument("--batch-size", type=int, default=48, help="Sectors per conversion batch.")
    parser.add_argument(
        "--reuse-sectors", action="store_true",
        help="Cache reduced sectors in dist/sites/cache/sectors.json between runs.",
    )
    args = parser.parse_args()

    global WOLVENKIT_VERSION
    extract_world = load_extract_world()
    WOLVENKIT_VERSION = extract_world.WOLVENKIT_VERSION

    wk = WolvenKit(args.game_dir, args.cache_root)
    if TMP_DIR.exists():
        shutil.rmtree(TMP_DIR, ignore_errors=True)
    TMP_DIR.parent.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    print("1/7 Indexing archives ...", flush=True)
    listings = {key: wk.listing(key) for key in ARCHIVES}
    inventory = gather_inventory(listings)
    resources = index_resources(listings)
    families = collections.Counter(family_of(code) for code in inventory)
    sts_total = families["sts"] + families["sts_ep1"]
    print(f"    canonical sites: ma={families['ma']} sts={sts_total} mws={families['mws']}", flush=True)

    if not (300 <= families["ma"] <= 360):
        raise RuntimeError(f"ma_* site count {families['ma']} outside expected 300..360")
    if not (95 <= sts_total <= 125):
        raise RuntimeError(f"sts_* site count {sts_total} outside expected 95..125")
    if not (40 <= families["mws"] <= 75):
        raise RuntimeError(f"mws_* site count {families['mws']} outside expected 40..75")

    print("2/7 Parsing site phases ...", flush=True)
    phases = collect_phases(wk, inventory)
    print(f"    {sum(len(v) for v in phases.values())} phases across {len(phases)} sites", flush=True)

    print("3/7 Indexing streaming blocks ...", flush=True)
    blocks = load_blocks(wk)
    print(f"    {len(blocks.by_leaf)} prefab NodeRefs", flush=True)

    # --- Resolve every site to prefabs, sectors and phase evidence ---------
    site_records: list[dict[str, Any]] = []
    sector_plan: dict[str, dict[str, Any]] = {}
    for code in sorted(inventory):
        entry = inventory[code]
        phase_records = phases.get(code, [])
        prefabs: set[str] = set()
        activations: list[dict[str, Any]] = []
        device_actions: list[dict[str, Any]] = []
        for record in phase_records:
            prefabs.update(record["prefabs"])
            activations.extend(record["activations"])
            device_actions.extend(record["device_actions"])

        descriptors: dict[str, dict[str, Any]] = {}
        for prefab in sorted(prefabs):
            for descriptor in blocks.lookup_leaf(node_name(prefab)):
                descriptors[descriptor["sector_path"]] = descriptor
        if not descriptors:
            for descriptor in blocks.lookup_code(code):
                descriptors[descriptor["sector_path"]] = descriptor

        quest_descriptors = [d for d in descriptors.values() if d["category"] == "Quest"]
        preferred = sorted(
            quest_descriptors or list(descriptors.values()),
            key=lambda d: (
                0 if node_name(d["prefab_ref"]) == code else 1,
                0 if code in node_name(d["prefab_ref"]) else 1,
                d["sector_path"],
            ),
        )
        primary = preferred[0] if preferred else None
        for path, descriptor in sorted(descriptors.items()):
            sector_plan.setdefault(path, descriptor)

        primary_phase = None
        for record in sorted(phase_records, key=lambda r: r["resource"]):
            stem = record["resource"].rsplit("\\", 1)[-1]
            if stem in (code, f"{code}_phase"):
                primary_phase = record["resource"]
                break
        if primary_phase is None and phase_records:
            primary_phase = sorted(r["resource"] for r in phase_records)[0]

        community_refs: set[str] = set()
        for record in phase_records:
            for activation in record["activations"]:
                community_refs.add(activation["spawner_ref"])

        site_records.append({
            "code": code,
            "family": family_of(code),
            "prefix": entry["prefix"],
            "archives": sorted(entry["archives"]),
            "primary": primary,
            "descriptors": sorted(descriptors.values(), key=lambda d: d["sector_path"]),
            "phase_path": primary_phase,
            "activations": activations,
            "device_actions": device_actions,
            "community_refs": community_refs,
        })

    if args.limit:
        site_records = site_records[: args.limit]
        keep = {r["code"] for r in site_records}
        sector_plan = {
            path: descriptor
            for path, descriptor in sector_plan.items()
            if any(descriptor in r["descriptors"] for r in site_records)
        }
        print(f"    limit mode: {len(keep)} codes", flush=True)

    print(f"4/7 Extracting {len(sector_plan)} quest sectors ...", flush=True)
    sector_cache = CACHE_DIR / "sectors.json"
    sectors: dict[str, dict[str, Any]] = {}
    if args.reuse_sectors and sector_cache.is_file():
        cached = json.loads(sector_cache.read_text(encoding="utf-8"))
        if set(cached) == set(sector_plan):
            sectors = cached
            print(f"    reused {len(sectors)} cached sectors", flush=True)
    if not sectors:
        sectors = collect_sectors(wk, sector_plan, args.batch_size)
        if args.reuse_sectors:
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            sector_cache.write_text(json.dumps(sectors, sort_keys=True), encoding="utf-8")
    print(f"    parsed {len(sectors)} sectors", flush=True)

    # --- Join communities, roster, anchors ---------------------------------
    print("5/7 Joining communities, roster and anchors ...", flush=True)
    registry = load_registry()
    areas_by_name = load_jsonl_by_name("areas.jsonl")
    markers_by_name = load_jsonl_by_name("markers.jsonl")
    seeds = WorldSeeds()
    _, char_aff = extract_world.parse_tweak_sources(args.game_dir / "tools" / "redmod" / "tweaks")
    alias = extract_world.AFFILIATION_ALIAS_TO_CODE

    community_rows: list[dict[str, Any]] = []
    roster_rows: list[dict[str, Any]] = []
    phase_rows: list[dict[str, Any]] = []
    slot_rows: list[dict[str, Any]] = []
    dropped: list[str] = []
    placed: list[dict[str, Any]] = []

    for record in site_records:
        code = record["code"]
        site_sectors = [sectors[d["sector_path"]] for d in record["descriptors"] if d["sector_path"] in sectors]
        spots: dict[str, dict[str, Any]] = {}
        patrols: dict[str, dict[str, Any]] = {}
        guards: dict[str, dict[str, Any]] = {}
        devices: dict[str, dict[str, Any]] = {}
        triggers: dict[str, dict[str, Any]] = {}
        positions: list[tuple[float, float, float]] = []
        interior = False
        interior_map_coords = None
        binding_tokens: set[tuple[str, str]] = set()
        prefab_paths: list[str] = []
        for sector in site_sectors:
            for spot in sector["spots"]:
                spots.setdefault(spot["node_ref"], spot)
            for patrol in sector["patrols"]:
                patrols.setdefault(patrol["node_ref"], patrol)
            for guard in sector["guards"]:
                guards.setdefault(guard["node_ref"], guard)
                for community in guard["communities"]:
                    record["community_refs"].add(community["community_ref"])
            for device in sector["devices"]:
                devices.setdefault(device["node_ref"], device)
            for trigger in sector["triggers"]:
                triggers.setdefault(trigger["node_ref"], trigger)
            positions.extend(sector["positions"])
            interior = interior or sector["is_interior"]
            interior_map_coords = interior_map_coords or sector["interior_map_coords"]
            binding_tokens.update((kind, token) for kind, token in sector["binding_tokens"])
            if sector.get("prefab_path"):
                prefab_paths.append(sector["prefab_path"])

        anchor: tuple[float, float, float] | None = None
        confidence = "unresolved"
        if positions:
            xs = [p[0] for p in positions]
            ys = [p[1] for p in positions]
            zs = sorted(p[2] for p in positions)
            anchor = (sum(xs) / len(xs), sum(ys) / len(ys), zs[len(zs) // 2])
            confidence = "exact"
        else:
            area_rows: list[dict[str, Any]] = []
            for name in sorted(areas_by_name):
                if name == code or name.startswith(code + "_"):
                    area_rows.extend(areas_by_name[name])
            if area_rows:
                anchor = (
                    sum(a["x"] for a in area_rows) / len(area_rows),
                    sum(a["y"] for a in area_rows) / len(area_rows),
                    sorted(a["z"] for a in area_rows)[len(area_rows) // 2],
                )
                confidence = "derived"
            else:
                marker_rows = [m for name, rows in markers_by_name.items() if code in name for m in rows]
                if marker_rows:
                    anchor = (
                        sum(m["x"] for m in marker_rows) / len(marker_rows),
                        sum(m["y"] for m in marker_rows) / len(marker_rows),
                        sorted(m["z"] for m in marker_rows)[len(marker_rows) // 2],
                    )
                    confidence = "derived"
        if anchor is None:
            dropped.append(code)
            continue

        x, y, z = (r3(v) for v in anchor)
        district_id, sub_territory_id, control_center_id, exact_district = seeds.assign(x, y)
        if not exact_district and confidence == "exact":
            confidence = "derived"
        if positions:
            bbox = (
                r3(min(p[0] for p in positions)), r3(min(p[1] for p in positions)), r3(min(p[2] for p in positions)),
                r3(max(p[0] for p in positions)), r3(max(p[1] for p in positions)), r3(max(p[2] for p in positions)),
            )
            radius = max(10.0, min(250.0, max(math.hypot(px - x, py - y) for px, py, _ in positions)))
        else:
            bbox = (None, None, None, None, None, None)
            radius = 40.0

        primary = record["primary"]
        interior = bool(interior)
        if not interior and record["family"] in ("sts", "sts_ep1", "mws"):
            prefab_text = " ".join(sorted(prefab_paths)).lower()
            interior = any(token in prefab_text for token in INTERIOR_VENUE_TOKENS)
        record.update({
            "site_id": None,
            "anchor": (x, y, z),
            "district_id": district_id,
            "sub_territory_id": sub_territory_id,
            "control_center_id": control_center_id,
            "bbox": bbox,
            "radius_m": round(radius, 3),
            "is_interior": 1 if interior else 0,
            "interior_map_coords": interior_map_coords,
            "confidence": confidence,
            "primary": primary,
            "prefab_path": sorted(prefab_paths)[0] if prefab_paths else None,
            "spots": spots,
            "patrols": patrols,
            "guards": guards,
            "devices": devices,
            "triggers": triggers,
            "binding_tokens": binding_tokens,
            "source_path": record["phase_path"] or (primary["sector_path"] if primary else code),
        })
        placed.append(record)

    site_records = placed
    site_records.sort(key=lambda r: r["code"])
    for index, record in enumerate(site_records, start=1):
        record["site_id"] = index

    for record in site_records:
        site_id = record["site_id"]
        refs = sorted(record["community_refs"])
        resolved: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
        seen_hashes: set[int] = set()
        for ref in refs:
            name = node_name(ref)
            rows = areas_by_name.get(name)
            if not rows:
                continue
            row = sorted(rows, key=lambda a: (a["community_hash"], a["x"], a["y"]))[0]
            community_hash = int(row["community_hash"])
            if community_hash in seen_hashes:
                continue
            registry_entry = registry.get(community_hash)
            if not registry_entry:
                continue
            seen_hashes.add(community_hash)
            resolved.append((name, row, registry_entry))
        resolved.sort(key=lambda item: (-len(item[2]["entries"]), item[0]))

        faction_votes: collections.Counter[int] = collections.Counter()
        for order, (name, row, registry_entry) in enumerate(resolved):
            community_hash = int(row["community_hash"])
            active = sum(1 for e in registry_entry["initial"].values() if e["active"])
            # The registry may repeat an entry name inside one community; the
            # runtime addresses entries by name, so keep the first and drop the
            # ambiguous duplicates.
            entries: list[dict[str, Any]] = []
            seen_entry_names: set[str] = set()
            for entry in sorted(
                registry_entry["entries"], key=lambda e: (e["name"], e["record"] or "")
            ):
                if entry["name"] in seen_entry_names:
                    continue
                seen_entry_names.add(entry["name"])
                entries.append(entry)
            community_rows.append({
                "site_id": site_id,
                "community_hash": str(community_hash),
                "spawner_ref": f"#{name}",
                "spawner_global_id": (
                    str(row["global_node_id"])
                    if row.get("global_node_id") and str(row["global_node_id"]) != "0"
                    else None
                ),
                "area_node_type": registry_entry["area_type"],
                "community_path": (
                    resources["communities"].get(name)
                    or resources["community_suffix"].get(name)
                ),
                "is_primary": 1 if order == 0 else 0,
                "entry_count": len(entries),
                "active_on_start": min(active, len(entries)),
                "x": r3(row["x"]),
                "y": r3(row["y"]),
                "z": r3(row["z"]),
            })
            for entry in entries:
                initial = registry_entry["initial"].get(entry["name"], {})
                record_id = entry["record"]
                affiliation = alias.get(char_aff.get(record_id, ""), None) if record_id else None
                faction_id = seeds.faction_id_by_code.get(affiliation) if affiliation else None
                if faction_id is not None:
                    faction_votes[faction_id] += 1
                roster_rows.append({
                    "site_id": site_id,
                    "community_hash": str(community_hash),
                    "entry_name": entry["name"],
                    "character_record_id": record_id,
                    "faction_id": faction_id,
                    "role_hint": role_hint(entry["name"], record_id),
                    "initial_phase_name": initial.get("phase"),
                    "entry_active_on_start": int(initial.get("active") or 0),
                    "spawn_in_view": int(entry.get("spawn_in_view", 1)),
                })
                seen_phase_keys: set[tuple[str, str, int]] = set()
                for phase in sorted(entry["phases"], key=lambda p: p["name"]):
                    seen_periods: set[tuple[str, int]] = set()
                    for period in phase["periods"]:
                        key = (period["hour"], period["quantity"])
                        if key in seen_periods:
                            continue
                        seen_periods.add(key)
                        phase_key = (phase["name"], period["hour"], period["quantity"])
                        if phase_key in seen_phase_keys:
                            continue
                        seen_phase_keys.add(phase_key)
                        phase_rows.append({
                            "site_id": site_id,
                            "community_hash": str(community_hash),
                            "entry_name": entry["name"],
                            "phase_name": phase["name"],
                            "always_spawned": phase["always_spawned"],
                            "hour": period["hour"],
                            "quantity": period["quantity"],
                            "is_sequence": period["is_sequence"],
                        })
                        for slot_index, spot_ref in enumerate(period["spots"]):
                            slot_rows.append({
                                "site_id": site_id,
                                "community_hash": str(community_hash),
                                "entry_name": entry["name"],
                                "phase_name": phase["name"],
                                "hour": period["hour"],
                                "quantity": period["quantity"],
                                "slot_index": slot_index,
                                "spot_ref": spot_ref,
                                "markings": period["markings"],
                            })

        record["community_count"] = len(resolved)
        if faction_votes:
            record["default_faction_id"] = sorted(faction_votes.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
            record["faction_source"] = "tweak"
        else:
            dominant: collections.Counter[str] = collections.Counter()
            for _, row, _ in resolved:
                if row.get("dominant_faction"):
                    dominant[row["dominant_faction"]] += int(row.get("affiliated_count") or 1)
            if dominant:
                faction_code = sorted(dominant.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
                record["default_faction_id"] = seeds.faction_id_by_code.get(faction_code)
                record["faction_source"] = "spatial" if record["default_faction_id"] is not None else "none"
            else:
                record["default_faction_id"] = None
                record["faction_source"] = "none"
        record["initial_owner_faction_id"] = seeds.owner_faction(record["sub_territory_id"])

    print(
        f"    {len(site_records)} sites placed ({len(dropped)} without anchors dropped), "
        f"{len(community_rows)} communities, {len(roster_rows)} roster entries",
        flush=True,
    )

    # --- Emit rows ---------------------------------------------------------
    print("6/7 Scoring sites and writing seeds ...", flush=True)
    spots_out: list[dict[str, Any]] = []
    spot_id_by_key: dict[tuple[int, str], int] = {}
    spot_xyz: dict[int, tuple[Any, Any, Any]] = {}
    spot_id = 1
    for record in site_records:
        site_id = record["site_id"]
        base_z = record["bbox"][2]
        for node_ref in sorted(record["spots"]):
            spot = record["spots"][node_ref]
            floor_index = None
            if record["is_interior"] and base_z is not None:
                floor_index = int(round((spot["z"] - base_z) / 3.6))
            row = {
                "spot_id": spot_id,
                "site_id": site_id,
                "node_ref": spot["node_ref"],
                "global_node_id": spot["global_node_id"],
                "debug_name": spot["debug_name"],
                "workspot_resource": spot["workspot_resource"],
                "spot_role": spot["spot_role"],
                "markings": spot["markings"],
                "is_workspot_infinite": spot["is_workspot_infinite"],
                "is_workspot_static": spot["is_workspot_static"],
                "actor_bodytype": spot["actor_bodytype"],
                "floor_index": floor_index,
                "x": r3(spot["x"]), "y": r3(spot["y"]), "z": r3(spot["z"]),
                "yaw": spot["yaw"],
                "source_sector": spot["source_sector"],
            }
            spots_out.append(row)
            spot_id_by_key[(site_id, spot["node_ref"])] = spot_id
            spot_xyz[spot_id] = (row["x"], row["y"], row["z"])
            spot_id += 1

    patrols_out: list[dict[str, Any]] = []
    patrol_points_out: list[dict[str, Any]] = []
    patrol_id = 1
    for record in site_records:
        site_id = record["site_id"]
        base_z = record["bbox"][2]
        for node_ref in sorted(record["patrols"]):
            patrol = record["patrols"][node_ref]
            floor_index = None
            if record["is_interior"] and base_z is not None:
                floor_index = int(round((patrol["z"] - base_z) / 3.6))
            patrols_out.append({
                "patrol_id": patrol_id,
                "site_id": site_id,
                "node_ref": patrol["node_ref"],
                "global_node_id": patrol["global_node_id"],
                "debug_name": patrol["debug_name"],
                "point_count": len(patrol["points"]),
                "floor_index": floor_index,
                "x": r3(patrol["x"]), "y": r3(patrol["y"]), "z": r3(patrol["z"]),
                "source_sector": patrol["source_sector"],
            })
            for point_index, point in enumerate(patrol["points"]):
                spot_id_value = spot_id_by_key.get((site_id, point["spot_ref"]))
                px, py, pz = spot_xyz.get(spot_id_value, (None, None, None)) if spot_id_value else (None, None, None)
                patrol_points_out.append({
                    "patrol_id": patrol_id,
                    "point_index": point_index,
                    "spot_ref": point["spot_ref"],
                    "spot_id": spot_id_value,
                    "point_type": point["point_type"],
                    "x": px, "y": py, "z": pz,
                })
            patrol_id += 1

    guards_out: list[dict[str, Any]] = []
    guard_community_out: list[dict[str, Any]] = []
    guard_id = 1
    for record in site_records:
        site_id = record["site_id"]
        base_z = record["bbox"][2]
        for node_ref in sorted(record["guards"]):
            guard = record["guards"][node_ref]
            floor_index = None
            if record["is_interior"] and base_z is not None:
                floor_index = int(round((guard["z"] - base_z) / 3.6))
            guards_out.append({
                "guard_area_id": guard_id,
                "site_id": site_id,
                "node_ref": guard["node_ref"],
                "global_node_id": guard["global_node_id"],
                "debug_name": guard["debug_name"],
                "pursuit_range_m": r3(guard["pursuit_range_m"]),
                "floor_index": floor_index,
                "x": r3(guard["x"]), "y": r3(guard["y"]), "z": r3(guard["z"]),
                "source_sector": guard["source_sector"],
            })
            for community in sorted(guard["communities"], key=lambda c: c["community_ref"]):
                guard_community_out.append({
                    "guard_area_id": guard_id,
                    "community_ref": community["community_ref"],
                    "is_primary": community["is_primary"],
                    "entry_names": community["entry_names"],
                })
            guard_id += 1

    devices_out: list[dict[str, Any]] = []
    doors_out: list[dict[str, Any]] = []
    device_id = 1
    door_id = 1
    for record in site_records:
        site_id = record["site_id"]
        base_z = record["bbox"][2]
        site_door_actions: dict[str, dict[str, str]] = {}
        for action in record["device_actions"]:
            site_door_actions.setdefault(
                action["node_ref"],
                {"action": action["action"], "controller_class": action["controller_class"]},
            )
        door_refs: set[str] = set()
        for node_ref in sorted(record["devices"]):
            device = record["devices"][node_ref]
            floor_index = None
            if record["is_interior"] and base_z is not None:
                floor_index = int(round((device["z"] - base_z) / 3.6))
            devices_out.append({
                "device_id": device_id,
                "site_id": site_id,
                "node_ref": device["node_ref"],
                "global_node_id": device["global_node_id"],
                "debug_name": device["debug_name"],
                "device_kind": device["device_kind"],
                "controller_class": device["controller_class"],
                "entity_template": device["entity_template"],
                "connected_community_ref": device["connected_community_ref"],
                "is_quest_gated": device["is_quest_gated"],
                "floor_index": floor_index,
                "x": r3(device["x"]), "y": r3(device["y"]), "z": r3(device["z"]),
                "source_sector": device["source_sector"],
            })
            if device["device_kind"] in ("door", "gate", "lift"):
                door_refs.add(device["node_ref"])
                vanilla = site_door_actions.get(device["node_ref"], {})
                if device["device_kind"] == "lift":
                    role, unlock, requires_power = "elevator", "None", 0
                else:
                    role = classify_door_role(device["debug_name"] or "", device["node_ref"])
                    unlock = {"ForceOpen": "ForceOpen", "ForceUnlock": "ForceUnlock"}.get(
                        vanilla.get("action") or "", "ForcePower"
                    )
                    requires_power = 1
                doors_out.append({
                    "door_id": door_id,
                    "site_id": site_id,
                    "device_id": device_id,
                    "node_ref": device["node_ref"],
                    "global_node_id": device["global_node_id"],
                    "debug_name": device["debug_name"],
                    "door_role": role,
                    "controller_class": device["controller_class"],
                    "default_state": None,
                    "requires_power": requires_power,
                    "unlock_action": unlock,
                    "vanilla_lock_action": vanilla.get("action"),
                })
                door_id += 1
            device_id += 1

        # Doors the vanilla phases power but that live in Exterior/Interior
        # sectors (layer B) rather than this Quest sector (layer C).
        for node_ref, vanilla in sorted(site_door_actions.items()):
            if node_ref in door_refs:
                continue
            if not any(token in (vanilla.get("controller_class") or "") for token in ("DoorControllerPS", "LiftControllerPS")):
                continue
            name = node_ref.lstrip("#")
            if not any(
                token in name.lower()
                for token in ("door", "gate", "entrance", "exit", "garage", "elevator", "lift", "shutter")
            ):
                continue
            is_lift = "Lift" in (vanilla.get("controller_class") or "")
            unlock = "None" if is_lift else {
                "ForceOpen": "ForceOpen", "ForceUnlock": "ForceUnlock"
            }.get(vanilla.get("action") or "", "ForcePower")
            doors_out.append({
                "door_id": door_id,
                "site_id": site_id,
                "device_id": None,
                "node_ref": node_ref,
                "global_node_id": None,
                "debug_name": name or None,
                "door_role": "elevator" if is_lift else classify_door_role(name, node_ref),
                "controller_class": vanilla.get("controller_class") or "DoorControllerPS",
                "default_state": None,
                "requires_power": 0 if is_lift else 1,
                "unlock_action": unlock,
                "vanilla_lock_action": vanilla.get("action"),
            })
            door_id += 1

    triggers_out: list[dict[str, Any]] = []
    trigger_id = 1
    for record in site_records:
        site_id = record["site_id"]
        for node_ref in sorted(record["triggers"]):
            trigger = record["triggers"][node_ref]
            triggers_out.append({
                "trigger_id": trigger_id,
                "site_id": site_id,
                "node_ref": trigger["node_ref"],
                "global_node_id": trigger["global_node_id"],
                "debug_name": trigger["debug_name"],
                "trigger_role": trigger["trigger_role"],
                "volume_json": trigger["volume_json"],
                "x": r3(trigger["x"]), "y": r3(trigger["y"]), "z": r3(trigger["z"]),
            })
            trigger_id += 1

    variants_out: list[dict[str, Any]] = []
    variant_id = 1
    for record in site_records:
        seen: set[tuple[str, str, str]] = set()
        for descriptor in record["descriptors"]:
            for variant in descriptor.get("variants") or []:
                name = cname_handle(variant.get("name")) or "default"
                raw_id = variant.get("variantId")
                variant_key = str(int(raw_id)) if isinstance(raw_id, (int, float)) else str(raw_id or "")
                key = (descriptor["sector_path"], name, variant_key)
                if key in seen:
                    continue
                seen.add(key)
                ref = json_value(variant.get("nodeRef"))
                variants_out.append({
                    "site_variant_id": variant_id,
                    "site_id": record["site_id"],
                    "sector_path": descriptor["sector_path"],
                    "variant_name": name,
                    "variant_id": variant_key,
                    "enabled_by_default": int(variant.get("enabledByDefault") or 0),
                    "node_ref": node_leaf(str(ref)) if ref else None,
                })
                variant_id += 1

    quests_by_prefix: dict[str, list[str]] = collections.defaultdict(list)
    for path in resources["quests"].values():
        prefix = site_dir_prefix(path)
        if prefix:
            quests_by_prefix[prefix].append(path)
    bindings_out: list[dict[str, Any]] = []
    for record in site_records:
        quest_resource = resources["quests"].get(record["code"])
        if quest_resource is None and record["prefix"]:
            candidates = sorted(quests_by_prefix.get(record["prefix"], []))
            if candidates:
                quest_resource = candidates[0]
        bindings_out.append({
            "site_id": record["site_id"],
            "content_kind": record["family"],
            "content_code": record["code"],
            "quest_phase_path": record["phase_path"],
            "quest_resource_path": quest_resource,
            "is_primary": 1,
        })
        for kind, token in sorted(record["binding_tokens"]):
            bindings_out.append({
                "site_id": record["site_id"],
                "content_kind": kind,
                "content_code": token,
                "quest_phase_path": None,
                "quest_resource_path": None,
                "is_primary": 0,
            })
    bindings_out.sort(key=lambda b: (b["site_id"], -b["is_primary"], b["content_kind"], b["content_code"]))

    # --- Stable child IDs from natural keys --------------------------------
    community_rows.sort(key=lambda r: (r["site_id"], -r["is_primary"], r["community_hash"]))
    community_id_by_key: dict[tuple[int, str], int] = {}
    for index, row in enumerate(community_rows, start=1):
        row["site_community_id"] = index
        community_id_by_key[(row["site_id"], row["community_hash"])] = index

    roster_rows.sort(key=lambda r: (community_id_by_key[(r["site_id"], r["community_hash"])], r["entry_name"]))
    entry_id_by_key: dict[tuple[int, str], int] = {}
    for index, row in enumerate(roster_rows, start=1):
        row["site_community_id"] = community_id_by_key[(row["site_id"], row["community_hash"])]
        row["entry_id"] = index
        entry_id_by_key[(row["site_community_id"], row["entry_name"])] = index

    phase_rows.sort(key=lambda r: (
        entry_id_by_key[(community_id_by_key[(r["site_id"], r["community_hash"])], r["entry_name"])],
        r["phase_name"], r["hour"], r["quantity"],
    ))
    phase_id_by_key: dict[tuple[int, str, str, int], int] = {}
    phases_out: list[dict[str, Any]] = []
    for index, row in enumerate(phase_rows, start=1):
        community_id_value = community_id_by_key[(row["site_id"], row["community_hash"])]
        entry_id_value = entry_id_by_key[(community_id_value, row["entry_name"])]
        row["phase_id"] = index
        row["entry_id"] = entry_id_value
        phase_id_by_key[(entry_id_value, row["phase_name"], row["hour"], row["quantity"])] = index
        phases_out.append({
            "phase_id": index,
            "entry_id": entry_id_value,
            "phase_name": row["phase_name"],
            "always_spawned": row["always_spawned"],
            "hour": row["hour"],
            "quantity": row["quantity"],
            "is_sequence": row["is_sequence"],
        })

    slots_out: list[dict[str, Any]] = []
    for row in slot_rows:
        community_id_value = community_id_by_key[(row["site_id"], row["community_hash"])]
        entry_id_value = entry_id_by_key[(community_id_value, row["entry_name"])]
        phase_key = (entry_id_value, row["phase_name"], row["hour"], row["quantity"])
        phase_id_value = phase_id_by_key.get(phase_key)
        if phase_id_value is None:
            continue
        slots_out.append({
            "phase_id": phase_id_value,
            "slot_index": row["slot_index"],
            "spot_ref": row["spot_ref"],
            "spot_id": spot_id_by_key.get((row["site_id"], row["spot_ref"])),
            "markings": row["markings"],
        })
    slots_out.sort(key=lambda r: (r["phase_id"], r["slot_index"]))

    # --- Site rollups ------------------------------------------------------
    role_counts_by_site: dict[int, collections.Counter[str]] = collections.defaultdict(collections.Counter)
    for spot in spots_out:
        role_counts_by_site[spot["site_id"]][spot["spot_role"] or "unknown"] += 1
    device_counts_by_site: dict[int, collections.Counter[str]] = collections.defaultdict(collections.Counter)
    for device in devices_out:
        device_counts_by_site[device["site_id"]][device["device_kind"]] += 1
    patrols_by_site = collections.Counter(p["site_id"] for p in patrols_out)
    guards_by_site = collections.Counter(g["site_id"] for g in guards_out)
    doors_by_site = collections.Counter(d["site_id"] for d in doors_out)
    door_roles_by_site: dict[int, collections.Counter[str]] = collections.defaultdict(collections.Counter)
    for door in doors_out:
        door_roles_by_site[door["site_id"]][door["door_role"]] += 1
    spots_by_site = collections.Counter(s["site_id"] for s in spots_out)
    roster_by_site: collections.Counter[int] = collections.Counter()
    officers_by_site: collections.Counter[int] = collections.Counter()
    community_site = {c["site_community_id"]: c["site_id"] for c in community_rows}
    for row in roster_rows:
        sid = community_site[row["site_community_id"]]
        roster_by_site[sid] += 1
        if row["role_hint"] in ("officer", "boss"):
            officers_by_site[sid] += 1

    keywords_by_site: dict[int, list[str]] = collections.defaultdict(list)
    for record in site_records:
        keywords_by_site[record["site_id"]].extend(
            [record["code"], record["prefix"] or "", record.get("prefab_path") or ""]
        )
    for spot in spots_out:
        keywords_by_site[spot["site_id"]].extend([spot["workspot_resource"] or "", spot["debug_name"] or ""])
    for device in devices_out:
        keywords_by_site[device["site_id"]].extend([device["debug_name"] or "", device["entity_template"] or ""])
    for guard in guards_out:
        keywords_by_site[guard["site_id"]].append(guard["debug_name"] or "")

    sites_out: list[dict[str, Any]] = []
    suitabilities_out: list[dict[str, Any]] = []
    for record in site_records:
        site_id = record["site_id"]
        spot_count = spots_by_site[site_id]
        patrol_count = patrols_by_site[site_id]
        guard_count = guards_by_site[site_id]
        door_count = doors_by_site[site_id]
        device_counts = device_counts_by_site[site_id]
        device_count = sum(device_counts.values())
        roster_count = roster_by_site[site_id]
        primary = record["primary"]
        x, y, z = record["anchor"]
        difficulty = clamp(
            1 + int(round(roster_count / 8.0)) + (1 if record["is_interior"] else 0)
            + (1 if device_count >= 6 else 0),
            1, 5,
        )
        tier = clamp(
            1 + (1 if spot_count >= 12 else 0) + (1 if guard_count >= 2 else 0)
            + (1 if roster_count >= 10 else 0) + (1 if record["family"] in ("sts", "sts_ep1") else 0),
            1, 5,
        )
        loot_tier = clamp(difficulty + (1 if device_counts.get("terminal", 0) else 0), 1, 5)
        floor_count = None
        if record["is_interior"] and record["bbox"][2] is not None:
            floor_count = clamp(int(round((record["bbox"][5] - record["bbox"][2]) / 3.6)) + 1, 1, 20)
        site = {
            "site_id": site_id,
            "code": record["code"],
            "display_name": None,
            "site_kind": SITE_KIND_BY_FAMILY[record["family"]],
            "source_family": record["family"],
            "district_id": record["district_id"],
            "sub_territory_id": record["sub_territory_id"],
            "control_center_id": record["control_center_id"],
            "anchor_x": x, "anchor_y": y, "anchor_z": z,
            "bbox_min_x": record["bbox"][0], "bbox_min_y": record["bbox"][1], "bbox_min_z": record["bbox"][2],
            "bbox_max_x": record["bbox"][3], "bbox_max_y": record["bbox"][4], "bbox_max_z": record["bbox"][5],
            "radius_m": record["radius_m"],
            "is_interior": record["is_interior"],
            "interior_map_coords": record["interior_map_coords"],
            "floor_count": floor_count,
            "default_faction_id": record.get("default_faction_id"),
            "initial_owner_faction_id": record.get("initial_owner_faction_id"),
            "faction_source": record.get("faction_source", "none"),
            "tier": tier,
            "difficulty": difficulty,
            "loot_tier": loot_tier,
            "has_patrols": 1 if patrol_count else 0,
            "has_workspots": 1 if spot_count else 0,
            "has_guard_areas": 1 if guard_count else 0,
            "has_security_devices": 1 if any(
                key in device_counts
                for key in ("security_area", "security_system", "camera", "turret", "terminal", "computer")
            ) else 0,
            "has_doors": 1 if door_count else 0,
            "has_community": 1 if record["community_count"] else 0,
            "spot_count": spot_count,
            "patrol_count": patrol_count,
            "device_count": device_count,
            "community_count": record["community_count"],
            "quest_prefab_ref": node_leaf(primary["prefab_ref"]) if primary else None,
            "quest_sector_path": primary["sector_path"] if primary else None,
            "sector_category": primary["category"] if primary else None,
            "streaming_block": primary["block"] if primary else None,
            "extraction_confidence": record["confidence"],
            "source_archive": record["archives"][0] if record["archives"] else "manual",
            "source_path": record["source_path"],
        }
        sites_out.append(site)
        suitabilities_out.extend(build_suitabilities(site, {
            "keywords": keywords_by_site[site_id],
            "role_counts": role_counts_by_site[site_id],
            "device_counts": device_counts,
            "device_count": device_count,
            "door_count": door_count,
            "door_roles": door_roles_by_site[site_id],
            "patrol_count": patrol_count,
            "officer_count": officers_by_site[site_id],
            "spot_count": spot_count,
        }))

    links_out = sorted(
        seeds.nearest_site_links(sites_out),
        key=lambda r: (r["from_site_id"], r["to_site_id"], r["link_kind"]),
    )

    # --- Integrity cross-checks -------------------------------------------
    for site in sites_out:
        site_id = site["site_id"]
        assert site["spot_count"] == sum(1 for s in spots_out if s["site_id"] == site_id), site["code"]
        assert site["patrol_count"] == sum(1 for p in patrols_out if p["site_id"] == site_id), site["code"]
        assert site["device_count"] == sum(1 for d in devices_out if d["site_id"] == site_id), site["code"]
        assert site["community_count"] == sum(1 for c in community_rows if c["site_id"] == site_id), site["code"]
        assert site["has_workspots"] == (1 if site["spot_count"] else 0)
        assert site["has_patrols"] == (1 if site["patrol_count"] else 0)
        assert site["has_doors"] == (1 if any(d["site_id"] == site_id for d in doors_out) else 0)
        assert site["has_community"] == (1 if site["community_count"] else 0)
    for community in community_rows:
        assert community["active_on_start"] <= community["entry_count"], community["spawner_ref"]
    assert {row["entry_id"] for row in roster_rows} == set(range(1, len(roster_rows) + 1))
    assert {row["phase_id"] for row in phases_out} == set(range(1, len(phases_out) + 1))
    assert all(row["phase_id"] <= len(phases_out) for row in slots_out)

    counts = {
        "sites": write_rows("sites.json", sites_out),
        "bindings": write_rows("bindings.json", bindings_out),
        "suitabilities": write_rows("suitabilities.json", sorted(
            suitabilities_out, key=lambda r: (r["site_id"], r["suitability"])
        )),
        "communities": write_rows("communities.json", community_rows),
        "rosters": write_rows("rosters.json", roster_rows),
        "phases": write_rows("phases.json", phases_out),
        "slots": write_rows("slots.json", slots_out),
        "spots": write_rows("spots.json", spots_out),
        "patrols": write_rows("patrols.json", patrols_out),
        "patrol_points": write_rows("patrol_points.json", patrol_points_out),
        "guards": write_rows("guards.json", guards_out),
        "guard_communities": write_rows("guard_communities.json", guard_community_out),
        "devices": write_rows("devices.json", devices_out),
        "doors": write_rows("doors.json", doors_out),
        "triggers": write_rows("triggers.json", triggers_out),
        "variants": write_rows("variants.json", variants_out),
        "links": write_rows("links.json", links_out),
    }

    by_family = collections.Counter(site["source_family"] for site in sites_out)
    by_district = collections.Counter(site["district_id"] for site in sites_out)
    by_sub_territory = collections.Counter(site["sub_territory_id"] for site in sites_out)
    meta = {
        "schema_version": 2,
        "generator": "tools/extract-sites.py",
        "game_version": GAME_VERSION,
        "wolvenkit_version": WOLVENKIT_VERSION,
        "counts": counts,
        "sites_by_family": dict(sorted(by_family.items())),
        "sites_by_district": {str(k): v for k, v in sorted(by_district.items())},
        "sites_per_sub_territory": {
            "min": min(by_sub_territory.values()),
            "max": max(by_sub_territory.values()),
            "mean": round(len(sites_out) / max(1, len(by_sub_territory)), 2),
        },
        "interior_sites": sum(site["is_interior"] for site in sites_out),
        "extraction_confidence": dict(sorted(
            collections.Counter(site["extraction_confidence"] for site in sites_out).items()
        )),
        "inventory": {
            "canonical_codes": {
                "ma": families["ma"],
                "sts": sts_total,
                "mws": families["mws"],
            },
            "sites_with_phase": len(phases),
            "sites_with_sector": sum(1 for site in sites_out if site["quest_sector_path"]),
            "dropped_without_anchor": dropped,
        },
        "notes": [
            "Sites are physical prefabs; site_bindings lists every content graph that used one.",
            "extraction_confidence='exact' means the anchor came from the site's own Quest-sector nodes.",
            "Non-canonical badlands sub-variant directories (ma_bls_ina_se{1,5}_*) are outside the canonical geocode table and therefore excluded.",
        ],
    }
    write_object("meta.json", meta)

    print("7/7 Done.", flush=True)
    print(json.dumps(meta, indent=2), flush=True)

    shutil.rmtree(TMP_DIR, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
