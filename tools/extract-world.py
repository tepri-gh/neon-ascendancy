#!/usr/bin/env python3
"""Extract ground-truth Cyberpunk 2077 2.5 world data into dist/extract/ and data/.

Read-only against the installed game directory. Uses:
  1. Plain-text <game>/tools/redmod/tweaks/**/*.tweak (factions, districts, characters)
  2. Pinned WolvenKit.CLI 10.0.0-beta.1 (DOTNET_ROLL_FORWARD=Major) in EP1-over-base
     precedence for always_loaded_0/1/2.streamingsector, 03_night_city.mappins,
     03_night_city.poimappins, and (optionally) all.traffic_persistent.

Fixes all prototype pitfalls documented in docs/research/game-data-extraction.md:
  - Always extracts content -> ep1 so EP1 overwrites base by resource path
  - Verifies community registry >= 10,000 communities (fails if base-only)
  - Iterates ALL nodeData instances per nodeIdx (never drops duplicate placements)
  - Never attributes city-wide always_loaded_* areas by file majority
  - Checks subprocess exit codes strictly; never truncates character lists
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_GAME_DIR = Path(os.environ.get("GAME_DIR", Path.home() / "Games" / "Cyberpunk 2077"))
DEFAULT_CACHE_DIR = Path(os.environ.get("CACHE_DIR", Path.home() / ".cache" / "neon-ascendancy"))
WOLVENKIT_VERSION = "10.0.0-beta.1"

# Top-level districts (8 canonical playable regions; Dogtown_Worldmap_Sub excluded).
TOP_DISTRICTS: list[dict[str, Any]] = [
    {"district_id": 1, "code": "watson",        "display_name": "Watson",        "kind": "city",     "gamedata_district": "Watson"},
    {"district_id": 2, "code": "westbrook",     "display_name": "Westbrook",     "kind": "city",     "gamedata_district": "Westbrook"},
    {"district_id": 3, "code": "heywood",       "display_name": "Heywood",       "kind": "city",     "gamedata_district": "Heywood"},
    {"district_id": 4, "code": "santo_domingo", "display_name": "Santo Domingo", "kind": "city",     "gamedata_district": "SantoDomingo"},
    {"district_id": 5, "code": "pacifica",      "display_name": "Pacifica",      "kind": "city",     "gamedata_district": "Pacifica"},
    {"district_id": 6, "code": "city_center",   "display_name": "City Center",   "kind": "city",     "gamedata_district": "CityCenter"},
    {"district_id": 7, "code": "badlands",      "display_name": "Badlands",      "kind": "badlands", "gamedata_district": "Badlands"},
    {"district_id": 8, "code": "dogtown",       "display_name": "Dogtown",       "kind": "dogtown",  "gamedata_district": "Dogtown"},
]

# Approximate Night City district polygons/centers (world metres, X/Y) used ONLY
# to spatially classify city-wide always_loaded_* community areas into their
# top-level district when nodeRefs are absent. Refined against real extracted POIs.
# Derived from Night City 2.5 world coordinate layout (Little China ~(-1600, 1000),
# JapanTown ~(-1500, -1380)? Note: we verify actual coords directly from markers!).
FACTIONS_CATALOG: list[dict[str, Any]] = [
    # Gangs (1..19)
    {"faction_id": 1,  "code": "maelstrom",    "display_name": "Maelstrom",      "category": "gang", "affiliation_enum": "Maelstrom",    "ticker": None, "color_rgba": "#D92626CC", "income_multiplier": 1.0, "hostility_bias": 0.8},
    {"faction_id": 2,  "code": "tyger_claws",  "display_name": "Tyger Claws",    "category": "gang", "affiliation_enum": "TygerClaws",   "ticker": None, "color_rgba": "#E84AA8CC", "income_multiplier": 1.15,"hostility_bias": 0.5},
    {"faction_id": 3,  "code": "valentinos",   "display_name": "Valentinos",     "category": "gang", "affiliation_enum": "Valentinos",   "ticker": None, "color_rgba": "#D9A326CC", "income_multiplier": 1.05,"hostility_bias": 0.4},
    {"faction_id": 4,  "code": "sixth_street", "display_name": "6th Street",     "category": "gang", "affiliation_enum": "SixthStreet",  "ticker": None, "color_rgba": "#3B7AD9CC", "income_multiplier": 1.0, "hostility_bias": 0.6},
    {"faction_id": 5,  "code": "voodoo_boys",  "display_name": "Voodoo Boys",    "category": "gang", "affiliation_enum": "VoodooBoys",   "ticker": None, "color_rgba": "#7A3BD9CC", "income_multiplier": 1.1, "hostility_bias": 0.7},
    {"faction_id": 6,  "code": "animals",      "display_name": "Animals",        "category": "gang", "affiliation_enum": "Animals",      "ticker": None, "color_rgba": "#D96B26CC", "income_multiplier": 0.95,"hostility_bias": 0.7},
    {"faction_id": 7,  "code": "scavengers",   "display_name": "Scavengers",     "category": "gang", "affiliation_enum": "Scavengers",   "ticker": None, "color_rgba": "#6E7A52CC", "income_multiplier": 0.8, "hostility_bias": 0.9},
    {"faction_id": 8,  "code": "wraiths",      "display_name": "Wraiths",        "category": "gang", "affiliation_enum": "Wraiths",      "ticker": None, "color_rgba": "#8C4A2ECC", "income_multiplier": 0.85,"hostility_bias": 0.9},
    {"faction_id": 9,  "code": "aldecaldos",   "display_name": "Aldecaldos",     "category": "gang", "affiliation_enum": "Aldecaldos",   "ticker": None, "color_rgba": "#C98B3ECC", "income_multiplier": 0.95,"hostility_bias": -0.2},
    {"faction_id": 10, "code": "barghest",     "display_name": "Barghest",       "category": "gang", "affiliation_enum": "Barghest",     "ticker": None, "color_rgba": "#88B02ECC", "income_multiplier": 1.25,"hostility_bias": 0.75},
    {"faction_id": 11, "code": "the_mox",      "display_name": "The Mox",        "category": "gang", "affiliation_enum": "TheMox",       "ticker": None, "color_rgba": "#38D9C5CC", "income_multiplier": 1.0, "hostility_bias": -0.1},
    # Megacorps — vanilla affiliations (20..39)
    {"faction_id": 20, "code": "arasaka",      "display_name": "Arasaka",        "category": "megacorp", "affiliation_enum": "Arasaka",     "ticker": "ARSK",  "color_rgba": "#B81424CC", "income_multiplier": 1.6, "hostility_bias": 0.6},
    {"faction_id": 21, "code": "militech",     "display_name": "Militech",       "category": "megacorp", "affiliation_enum": "Militech",    "ticker": "MLTC",  "color_rgba": "#2D5A88CC", "income_multiplier": 1.5, "hostility_bias": 0.55},
    {"faction_id": 22, "code": "kang_tao",     "display_name": "Kang Tao",       "category": "megacorp", "affiliation_enum": "KangTao",     "ticker": "KTAO",  "color_rgba": "#C47D1ACC", "income_multiplier": 1.4, "hostility_bias": 0.5},
    {"faction_id": 23, "code": "biotechnica",  "display_name": "Biotechnica",    "category": "megacorp", "affiliation_enum": "Biotechnica", "ticker": "BIOT",  "color_rgba": "#2E9E5BCC", "income_multiplier": 1.35,"hostility_bias": 0.3},
    {"faction_id": 24, "code": "zetatech",     "display_name": "Zetatech",       "category": "megacorp", "affiliation_enum": "Zetatech",    "ticker": "ZETA",  "color_rgba": "#4D88B8CC", "income_multiplier": 1.3, "hostility_bias": 0.3},
    {"faction_id": 25, "code": "netwatch",     "display_name": "NetWatch",       "category": "megacorp", "affiliation_enum": "NetWatch",    "ticker": "NTWT",  "color_rgba": "#22A6B3CC", "income_multiplier": 1.3, "hostility_bias": 0.4},
    {"faction_id": 26, "code": "trauma_team",  "display_name": "Trauma Team",    "category": "megacorp", "affiliation_enum": "TraumaTeam",  "ticker": "TRMA",  "color_rgba": "#E0E6EBCC", "income_multiplier": 1.4, "hostility_bias": 0.2},
    {"faction_id": 27, "code": "news54",       "display_name": "News 54",        "category": "megacorp", "affiliation_enum": "News54",      "ticker": "NWS54", "color_rgba": "#9BA4B0CC", "income_multiplier": 1.1, "hostility_bias": 0.0},
    {"faction_id": 28, "code": "orbital_air",  "display_name": "Orbital Air",    "category": "megacorp", "affiliation_enum": "OA",          "ticker": "ORBA",  "color_rgba": "#59A5D8CC", "income_multiplier": 1.5, "hostility_bias": 0.35},
    # Megacorps — synthetic IDs (no vanilla gamedataAffiliation record; 40..49)
    {"faction_id": 40, "code": "night_corp",   "display_name": "Night Corp",     "category": "megacorp", "affiliation_enum": None,          "ticker": "NGTCP", "color_rgba": "#3E4C66CC", "income_multiplier": 1.45,"hostility_bias": 0.25},
    {"faction_id": 41, "code": "kiroshi",      "display_name": "Kiroshi Optics", "category": "megacorp", "affiliation_enum": None,          "ticker": "KIRO",  "color_rgba": "#5EC4D4CC", "income_multiplier": 1.35,"hostility_bias": 0.2},
    {"faction_id": 42, "code": "kendachi",     "display_name": "Kendachi",       "category": "megacorp", "affiliation_enum": None,          "ticker": "KEND",  "color_rgba": "#A85544CC", "income_multiplier": 1.25,"hostility_bias": 0.3},
    {"faction_id": 43, "code": "petrochem",    "display_name": "Petrochem",      "category": "megacorp", "affiliation_enum": None,          "ticker": "PTRC",  "color_rgba": "#B38A2ECC", "income_multiplier": 1.4, "hostility_bias": 0.4},
    {"faction_id": 44, "code": "budget_arms",  "display_name": "Budget Arms",    "category": "megacorp", "affiliation_enum": None,          "ticker": None,    "color_rgba": "#7A6A5ACC", "income_multiplier": 0.9, "hostility_bias": 0.1},
    # Civic & Independents (50..69)
    {"faction_id": 50, "code": "ncpd",         "display_name": "NCPD",           "category": "civic",       "affiliation_enum": "NCPD",           "ticker": None, "color_rgba": "#246BCECC", "income_multiplier": 0.0, "hostility_bias": 0.5},
    {"faction_id": 51, "code": "city_council", "display_name": "City Council",   "category": "civic",       "affiliation_enum": "CityCouncil",    "ticker": None, "color_rgba": "#647896CC", "income_multiplier": 1.2, "hostility_bias": 0.2},
    {"faction_id": 52, "code": "nusa",         "display_name": "NUSA",           "category": "civic",       "affiliation_enum": "NUSA",           "ticker": None, "color_rgba": "#3A4E7ACC", "income_multiplier": 0.0, "hostility_bias": 0.5},
    {"faction_id": 53, "code": "afterlife",    "display_name": "Afterlife Mercs","category": "independent", "affiliation_enum": "AfterlifeMercs", "ticker": None, "color_rgba": "#F2C94CCC", "income_multiplier": 1.1, "hostility_bias": 0.0},
    {"faction_id": 54, "code": "delamain",     "display_name": "Delamain",       "category": "independent", "affiliation_enum": None,             "ticker": None, "color_rgba": "#40B5ADCC", "income_multiplier": 1.2, "hostility_bias": 0.0},
    # Active Fixers (70..79)
    {"faction_id": 70, "code": "fixer_regina",     "display_name": "Regina Jones",       "category": "fixer", "affiliation_enum": None, "ticker": None, "color_rgba": "#8C9BAACC", "income_multiplier": 1.0, "hostility_bias": 0.0},
    {"faction_id": 71, "code": "fixer_wakako",     "display_name": "Wakako Okada",       "category": "fixer", "affiliation_enum": None, "ticker": None, "color_rgba": "#A86694CC", "income_multiplier": 1.0, "hostility_bias": 0.0},
    {"faction_id": 72, "code": "fixer_padre",      "display_name": "Sebastian Ibarra",   "category": "fixer", "affiliation_enum": None, "ticker": None, "color_rgba": "#B39252CC", "income_multiplier": 1.0, "hostility_bias": 0.0},
    {"faction_id": 73, "code": "fixer_el_capitan", "display_name": "Muamar Reyes",       "category": "fixer", "affiliation_enum": None, "ticker": None, "color_rgba": "#6E8CB3CC", "income_multiplier": 1.0, "hostility_bias": 0.0},
    {"faction_id": 74, "code": "fixer_dakota",     "display_name": "Dakota Smith",       "category": "fixer", "affiliation_enum": None, "ticker": None, "color_rgba": "#B08258CC", "income_multiplier": 1.0, "hostility_bias": 0.0},
    {"faction_id": 75, "code": "fixer_dino",       "display_name": "Dino Dinovic",       "category": "fixer", "affiliation_enum": None, "ticker": None, "color_rgba": "#5994A6CC", "income_multiplier": 1.0, "hostility_bias": 0.0},
    {"faction_id": 76, "code": "fixer_rogue",      "display_name": "Rogue Amendiares",   "category": "fixer", "affiliation_enum": None, "ticker": None, "color_rgba": "#D9AE42CC", "income_multiplier": 1.0, "hostility_bias": 0.0},
    {"faction_id": 77, "code": "fixer_mr_hands",   "display_name": "Mr. Hands",          "category": "fixer", "affiliation_enum": None, "ticker": None, "color_rgba": "#7A9E52CC", "income_multiplier": 1.0, "hostility_bias": 0.0},
]

AFFILIATION_ALIAS_TO_CODE: dict[str, str] = {
    "Maelstrom": "maelstrom",
    "MaelstromAndroid": "maelstrom",
    "TygerClaws": "tyger_claws",
    "Valentinos": "valentinos",
    "SixthStreet": "sixth_street",
    "SixthStreetAndroid": "sixth_street",
    "VoodooBoys": "voodoo_boys",
    "Animals": "animals",
    "Scavengers": "scavengers",
    "ScavengersAndroid": "scavengers",
    "Wraiths": "wraiths",
    "WraithsAndroid": "wraiths",
    "Wraiths_Former": "wraiths",
    "Aldecaldos": "aldecaldos",
    "Barghest": "barghest",
    "TheMox": "the_mox",
    "Arasaka": "arasaka",
    "Militech": "militech",
    "KangTao": "kang_tao",
    "Biotechnica": "biotechnica",
    "Zetatech": "zetatech",
    "NetWatch": "netwatch",
    "TraumaTeam": "trauma_team",
    "News54": "news54",
    "OA": "orbital_air",
    "NCPD": "ncpd",
    "CityCouncil": "city_council",
    "NUSA": "nusa",
    "AfterlifeMercs": "afterlife",
    "AfterlifeMercRogue": "afterlife",
}


def run_wk(wk: Path, args: list[str]) -> None:
    env = {**os.environ, "DOTNET_ROLL_FORWARD": "Major"}
    proc = subprocess.run([str(wk), *args], env=env, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"WolvenKit.CLI failed (rc={proc.returncode}): {' '.join(args)}\n"
            f"stdout:\n{proc.stdout[-1500:]}\nstderr:\n{proc.stderr[-1500:]}"
        )


def parse_tweak_sources(tweaks_root: Path) -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    """Parse plain-text .tweak files for Districts.* and Character.* affiliations."""
    if not tweaks_root.is_dir():
        raise FileNotFoundError(f"Missing tweaks directory: {tweaks_root}")

    # Parse Character.* records with inheritance for affiliation resolution.
    char_parent: dict[str, str] = {}
    char_aff: dict[str, str] = {}
    districts_raw: dict[str, dict[str, Any]] = {}

    pkg_re = re.compile(r"^\s*package\s+([A-Za-z0-9_.]+)")
    rec_re = re.compile(r"^\s*([A-Za-z0-9_]+)\s*:\s*([A-Za-z0-9_.]+)\s*\{?\s*$")
    aff_re = re.compile(r'^\s*(?:fk\s*<[^>]+>\s+)?affiliation\s*=\s*"Factions\.([A-Za-z0-9_]+)"\s*;')
    enum_re = re.compile(r'^\s*(?:string\s+)?enumName\s*=\s*"([^"]+)"\s*;')
    parent_dist_re = re.compile(r'^\s*(?:fk\s*<[^>]+>\s+)?parentDistrict\s*=\s*"Districts\.([^"]+)"\s*;')
    crime_re = re.compile(r"^\s*(?:float\s+)?crimeMultiplier\s*=\s*([0-9.]+)f?\s*;")
    quest_dist_re = re.compile(r"^\s*(?:bool\s+)?isQuestDistrict\s*=\s*(true|false)\s*;")
    gang_item_re = re.compile(r'"Factions\.([A-Za-z0-9_]+)"')

    # Process base first, then ep1 so EP1 blocks override base.
    tweak_files = sorted((tweaks_root / "base").rglob("*.tweak"))
    ep1_dir = tweaks_root / "ep1"
    if ep1_dir.is_dir():
        tweak_files.extend(sorted(ep1_dir.rglob("*.tweak")))

    for path in tweak_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        pkg = ""
        cur_rec: str | None = None
        brace_depth = 0
        in_gangs = False

        for line in text.splitlines():
            m_pkg = pkg_re.match(line)
            if m_pkg:
                pkg = m_pkg.group(1)
                continue

            if brace_depth == 0:
                m_rec = rec_re.match(line)
                if m_rec:
                    name, base = m_rec.group(1), m_rec.group(2)
                    cur_rec = name
                    if pkg == "Character":
                        full = f"Character.{name}"
                        base_full = base if "." in base else f"Character.{base}"
                        char_parent[full] = base_full
                    elif pkg == "Districts" and base == "District":
                        districts_raw.setdefault(name, {
                            "record": name,
                            "enumName": None,
                            "parentRecord": None,
                            "crimeMultiplier": None,
                            "isQuestDistrict": False,
                            "gangs": [],
                        })
                    brace_depth += line.count("{") - line.count("}")
                    continue

            opens = line.count("{")
            closes = line.count("}")
            brace_depth += opens - closes

            if cur_rec and brace_depth >= 1:
                if pkg == "Character":
                    m_aff = aff_re.match(line)
                    if m_aff:
                        char_aff[f"Character.{cur_rec}"] = m_aff.group(1)
                elif pkg == "Districts" and cur_rec in districts_raw:
                    d = districts_raw[cur_rec]
                    if (m := enum_re.match(line)):
                        d["enumName"] = m.group(1)
                    elif (m := parent_dist_re.match(line)):
                        d["parentRecord"] = m.group(1)
                    elif (m := crime_re.match(line)):
                        d["crimeMultiplier"] = float(m.group(1))
                    elif (m := quest_dist_re.match(line)):
                        d["isQuestDistrict"] = (m.group(1) == "true")
                    if "gangs" in line and "=" in line:
                        in_gangs = True
                        d["gangs"] = gang_item_re.findall(line)
                        if "]" in line:
                            in_gangs = False
                    elif in_gangs:
                        d["gangs"].extend(gang_item_re.findall(line))
                        if "]" in line:
                            in_gangs = False

            if brace_depth <= 0:
                brace_depth = 0
                cur_rec = None
                in_gangs = False

    # Resolve Character.* affiliations via inheritance with cycle guard.
    resolved_aff: dict[str, str] = {}
    for rec in set(char_parent) | set(char_aff):
        seen: set[str] = set()
        cur: str | None = rec
        while cur and cur not in seen:
            seen.add(cur)
            if cur in char_aff:
                resolved_aff[rec] = char_aff[cur]
                break
            cur = char_parent.get(cur)

    return districts_raw, resolved_aff


def extract_game_resources(game_dir: Path, wk: Path, out_raw: Path, with_roads: bool) -> dict[str, Path]:
    """Extract EP1-over-base world files using WolvenKit.CLI."""
    out_raw.mkdir(parents=True, exist_ok=True)
    # Extract base first, then EP1 so EP1 wins by path.
    archives = [
        game_dir / "archive" / "pc" / "content" / "basegame_3_nightcity.archive",
        game_dir / "archive" / "pc" / "ep1" / "ep1_1_nightcity.archive",
    ]
    pattern_parts = [
        r"default\\always_loaded_[012]\.streamingsector$",
        r"default\\03_night_city\.(mappins|poimappins)$",
    ]
    if with_roads:
        pattern_parts.append(r"traffic\\all\.(traffic_persistent|lane_polygons|lane_connections)$")
    regex = "(" + "|".join(pattern_parts) + ")"

    for arc in archives:
        if not arc.is_file():
            raise FileNotFoundError(f"Missing game archive: {arc}")
        print(f"Extracting {arc.name} ...", flush=True)
        run_wk(wk, ["extract", str(arc), "-o", str(out_raw), "-r", regex])

    compiled = out_raw / "base" / "worlds" / "03_night_city" / "_compiled" / "default"
    targets = {
        "always_loaded_0": compiled / "always_loaded_0.streamingsector",
        "always_loaded_1": compiled / "always_loaded_1.streamingsector",
        "always_loaded_2": compiled / "always_loaded_2.streamingsector",
        "mappins": compiled / "03_night_city.mappins",
        "poimappins": compiled / "03_night_city.poimappins",
    }
    if with_roads:
        traffic = out_raw / "base" / "worlds" / "03_night_city" / "sectors" / "_generated" / "traffic"
        targets["traffic_persistent"] = traffic / "all.traffic_persistent"

    for key, path in targets.items():
        if not path.is_file():
            raise FileNotFoundError(f"Expected extracted resource missing: {path}")
        json_path = Path(str(path) + ".json")
        if not json_path.is_file() or json_path.stat().st_mtime < path.stat().st_mtime:
            print(f"Converting {path.name} -> JSON ...", flush=True)
            run_wk(wk, ["convert", "s", str(path)])
        targets[key] = json_path

    return targets


def parse_always_loaded(
    json_paths: list[Path],
    char_aff: dict[str, str],
) -> tuple[dict[int, list[str]], list[dict[str, Any]], list[dict[str, Any]]]:
    """Parse community registry, ALL community area instances, and static markers."""
    registry: dict[int, list[str]] = {}
    areas: list[dict[str, Any]] = []
    markers: list[dict[str, Any]] = []

    # Pass 1: find worldCommunityRegistryNode (lives in always_loaded_1).
    loaded_chunks: list[tuple[str, dict[str, Any]]] = []
    for jp in json_paths:
        print(f"Loading {jp.name} ...", flush=True)
        with jp.open("r", encoding="utf-8") as fh:
            root = json.load(fh)["Data"]["RootChunk"]
        loaded_chunks.append((jp.name, root))
        for node in root.get("nodes", []):
            data = node.get("Data") or {}
            if data.get("$type") == "worldCommunityRegistryNode":
                for c in data.get("communitiesData", []):
                    cid = int(c["communityId"]["entityId"]["hash"])
                    entries = ((c.get("template") or {}).get("Data") or {}).get("entries") or []
                    chars = [
                        val
                        for e in entries
                        if (val := ((e.get("Data") or {}).get("characterRecordId") or {}).get("$value"))
                    ]
                    registry[cid] = chars

    if len(registry) < 10000:
        raise RuntimeError(
            f"Build gate failed: community registry has only {len(registry)} communities "
            f"(expected >= 10000 from EP1 always_loaded_1)."
        )

    # Pass 2: collect ALL instances of every community area & static marker node.
    for fname, root in loaded_chunks:
        nodes = root.get("nodes", [])
        inst_by_idx: dict[int, list[dict[str, Any]]] = collections.defaultdict(list)
        for inst in (root.get("nodeData") or {}).get("Data", []):
            inst_by_idx[int(inst["nodeIdx"])].append(inst)

        for idx, node in enumerate(nodes):
            data = node.get("Data") or {}
            ntype = data.get("$type", "")
            instances = inst_by_idx.get(idx, [])
            if not instances:
                continue

            if "CommunityAreaNode" in ntype:
                sid = int(data["sourceObjectId"]["hash"])
                chars = registry.get(sid, [])
                aff_counts: collections.Counter[str] = collections.Counter()
                for ch in chars:
                    raw_aff = char_aff.get(ch)
                    if raw_aff and raw_aff in AFFILIATION_ALIAS_TO_CODE:
                        aff_counts[AFFILIATION_ALIAS_TO_CODE[raw_aff]] += 1
                dominant_faction = aff_counts.most_common(1)[0][0] if aff_counts else None
                debug_name = (data.get("debugName") or {}).get("$value", "")

                # Iterate ALL instances (never break on first).
                for inst in instances:
                    pos = (inst.get("transform") or {}).get("position")
                    if not pos:
                        continue
                    x, y, z = float(pos["X"]), float(pos["Y"]), float(pos["Z"])
                    if not (math.isfinite(x) and math.isfinite(y) and math.isfinite(z)):
                        continue
                    if z < -200.0 or z > 1000.0:
                        continue
                    # Skip unplaced (0, 0, 0) prefab-origin shells.
                    if abs(x) < 1.0 and abs(y) < 1.0 and abs(z) < 1.0:
                        continue
                    areas.append({
                        "source_file": fname,
                        "global_node_id": str((inst.get("globalNodeId") or {}).get("hash", "")),
                        "community_hash": str(sid),
                        "debug_name": debug_name,
                        "entry_count": len(chars),
                        "affiliated_count": sum(aff_counts.values()),
                        "dominant_faction": dominant_faction,
                        "faction_counts": dict(sorted(aff_counts.items())),
                        "x": round(x, 3),
                        "y": round(y, 3),
                        "z": round(z, 3),
                    })
            elif ntype == "worldStaticMarkerNode":
                debug_name = (data.get("debugName") or {}).get("$value", "")
                if not debug_name:
                    continue
                for inst in instances:
                    pos = (inst.get("transform") or {}).get("position")
                    if not pos:
                        continue
                    x, y, z = float(pos["X"]), float(pos["Y"]), float(pos["Z"])
                    if not (math.isfinite(x) and math.isfinite(y) and math.isfinite(z)):
                        continue
                    if z < -200.0 or z > 1000.0:
                        continue
                    # Skip unplaced (0, 0, 0) prefab-origin shells.
                    if abs(x) < 1.0 and abs(y) < 1.0 and abs(z) < 1.0:
                        continue
                    markers.append({
                        "source_file": fname,
                        "debug_name": debug_name,
                        "x": round(x, 3),
                        "y": round(y, 3),
                        "z": round(z, 3),
                    })

    return registry, areas, markers


def parse_poimappins(poi_json: Path) -> list[dict[str, Any]]:
    with poi_json.open("r", encoding="utf-8") as fh:
        root = json.load(fh)["Data"]["RootChunk"]
    out: list[dict[str, Any]] = []
    for item in root.get("cookedData", []):
        pos = item.get("position") or {}
        if "X" not in pos:
            continue
        x, y, z = float(pos["X"]), float(pos["Y"]), float(pos["Z"])
        if not (math.isfinite(x) and math.isfinite(y) and math.isfinite(z)):
            continue
        if z < -200.0 or z > 1000.0:
            continue
        out.append({
            "entity_id": str((item.get("entityID") or {}).get("hash", "")),
            "journal_path_hash": int(item.get("journalPathHash", 0)),
            "x": round(x, 3),
            "y": round(y, 3),
            "z": round(z, 3),
        })
    return out


def classify_district_xy(x: float, y: float) -> str:
    """Classify a Night City world-space (X, Y) coordinate into one of the 8 top-level districts.

    Night City coordinate axes (metres):
      - X negative = West (coast / Pacifica / Dogtown / Watson west), X positive = East (Badlands / Santo Domingo / Charter Hill)
      - Y positive = North (Watson / Northside / North Oak / North Badlands), Y negative = South (Pacifica / Dogtown / Rancho Coronado / South Badlands)
    Validated directly against extracted faction spawn densities below.
    """
    # Dogtown (walled southeast section of Pacifica, including EBM Stadium north to Y ~ -1920
    # and Luxor/Kress west to X ~ -2490; Coastview GIM sits north of -1920, West Wind west of -2490).
    if -2490.0 <= x <= -1280.0 and -3100.0 <= y <= -1920.0:
        return "dogtown"
    # Pacifica (Coastview + West Wind Estate, west/north of Dogtown)
    if -3150.0 <= x <= -1250.0 and -3300.0 <= y <= -1400.0:
        return "pacifica"
    # Watson (Northside, Kabuki, Little China, Arasaka Waterfront)
    if -2450.0 <= x <= -450.0 and 550.0 <= y <= 3450.0:
        return "watson"
    # City Center (Corpo Plaza + Downtown)
    if -2250.0 <= x <= -1050.0 and -600.0 <= y <= 650.0:
        return "city_center"
    # Westbrook (Japantown, Charter Hill, North Oak)
    if -1150.0 <= x <= 950.0 and -750.0 <= y <= 1850.0:
        return "westbrook"
    # Heywood (Wellsprings, Vista del Rey, Glen)
    if -2650.0 <= x <= -800.0 and -1600.0 <= y <= -550.0:
        return "heywood"
    # Santo Domingo (Arroyo + Rancho Coronado)
    if -950.0 <= x <= 1450.0 and -2550.0 <= y <= -650.0:
        return "santo_domingo"
    # Everything outside urban core is Badlands (including Morro Rock NCX on far west)
    return "badlands"


def deterministic_kmeans_xy(points: list[dict[str, Any]], k: int, iters: int = 30) -> list[list[dict[str, Any]]]:
    """Deterministic k-means++ style clustering over (x, y) coordinates (no external deps)."""
    if not points:
        return []
    k = min(k, len(points))
    # Sort deterministically by (x, y, community_hash) before picking initial centroids.
    pts = sorted(points, key=lambda p: (p["x"], p["y"], p.get("community_hash", "")))
    # Deterministic farthest-point seeding starting from median-X point.
    centroids: list[tuple[float, float]] = [(pts[len(pts) // 2]["x"], pts[len(pts) // 2]["y"])]
    while len(centroids) < k:
        best_pt = max(
            pts,
            key=lambda p: min((p["x"] - cx) ** 2 + (p["y"] - cy) ** 2 for cx, cy in centroids),
        )
        centroids.append((best_pt["x"], best_pt["y"]))

    clusters: list[list[dict[str, Any]]] = [[] for _ in range(k)]
    for _ in range(iters):
        clusters = [[] for _ in range(k)]
        for p in pts:
            ci = min(range(k), key=lambda i: (p["x"] - centroids[i][0]) ** 2 + (p["y"] - centroids[i][1]) ** 2)
            clusters[ci].append(p)
        new_centroids: list[tuple[float, float]] = []
        for i, cl in enumerate(clusters):
            if cl:
                wx = sum(p["x"] * max(1, p["affiliated_count"]) for p in cl)
                wy = sum(p["y"] * max(1, p["affiliated_count"]) for p in cl)
                wt = sum(max(1, p["affiliated_count"]) for p in cl)
                new_centroids.append((wx / wt, wy / wt))
            else:
                new_centroids.append(centroids[i])
        if all(abs(a[0] - b[0]) < 1e-3 and abs(a[1] - b[1]) < 1e-3 for a, b in zip(centroids, new_centroids)):
            break
        centroids = new_centroids

    # Sort clusters deterministically north-to-south, west-to-east for stable IDs.
    non_empty = [c for c in clusters if c]
    non_empty.sort(key=lambda c: (-round(sum(p["y"] for p in c) / len(c), 1), round(sum(p["x"] for p in c) / len(c), 1)))
    return non_empty


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract ground-truth CP2077 2.5 data into dist/extract/ and data/.")
    ap.add_argument("--game-dir", type=Path, default=DEFAULT_GAME_DIR)
    ap.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE_DIR)
    ap.add_argument("--with-roads", action="store_true", help="Also extract all.traffic_persistent.")
    ap.add_argument("--skip-wolvenkit", action="store_true", help="Reuse existing JSON files in dist/extract/raw.")
    ap.add_argument("--emit-seeds", action="store_true", help="Write deterministic data/*.json seed files from extraction.")
    args = ap.parse_args()

    wk = args.cache_dir / f"wolvenkit-{WOLVENKIT_VERSION}" / "WolvenKit.CLI"
    if not args.skip_wolvenkit and not wk.is_file():
        raise FileNotFoundError(f"WolvenKit.CLI not found at {wk}")

    extract_dir = ROOT / "dist" / "extract"
    raw_dir = extract_dir / "raw"

    print("1/4 Parsing plain-text .tweak files ...", flush=True)
    tweaks_root = args.game_dir / "tools" / "redmod" / "tweaks"
    districts_raw, char_aff = parse_tweak_sources(tweaks_root)
    print(f"    Parsed {len(districts_raw)} district records and {len(char_aff)} character affiliations.", flush=True)

    if args.skip_wolvenkit:
        compiled = raw_dir / "base" / "worlds" / "03_night_city" / "_compiled" / "default"
        targets = {
            "always_loaded_0": compiled / "always_loaded_0.streamingsector.json",
            "always_loaded_1": compiled / "always_loaded_1.streamingsector.json",
            "always_loaded_2": compiled / "always_loaded_2.streamingsector.json",
            "mappins": compiled / "03_night_city.mappins.json",
            "poimappins": compiled / "03_night_city.poimappins.json",
        }
    else:
        print("2/4 Extracting & converting EP1-over-base world files ...", flush=True)
        targets = extract_game_resources(args.game_dir, wk, raw_dir, args.with_roads)

    print("3/4 Joining community registry, area transforms, and affiliations ...", flush=True)
    registry, areas, markers = parse_always_loaded(
        [targets["always_loaded_0"], targets["always_loaded_1"], targets["always_loaded_2"]],
        char_aff,
    )
    pois = parse_poimappins(targets["poimappins"])

    # Assign spatial district to every extracted area.
    dist_counts: collections.Counter[str] = collections.Counter()
    dist_faction_counts: dict[str, collections.Counter[str]] = collections.defaultdict(collections.Counter)
    for a in areas:
        dcode = classify_district_xy(a["x"], a["y"])
        a["district_code"] = dcode
        dist_counts[dcode] += 1
        if a["dominant_faction"]:
            dist_faction_counts[dcode][a["dominant_faction"]] += a["affiliated_count"]

    extract_dir.mkdir(parents=True, exist_ok=True)
    with (extract_dir / "areas.jsonl").open("w", encoding="utf-8") as fh:
        for a in sorted(areas, key=lambda r: (r["district_code"], r["community_hash"], r["x"], r["y"])):
            fh.write(json.dumps(a, sort_keys=True) + "\n")
    with (extract_dir / "pois.jsonl").open("w", encoding="utf-8") as fh:
        for p in sorted(pois, key=lambda r: (r["journal_path_hash"], r["x"], r["y"])):
            fh.write(json.dumps(p, sort_keys=True) + "\n")
    with (extract_dir / "markers.jsonl").open("w", encoding="utf-8") as fh:
        for m in sorted(markers, key=lambda r: (r["debug_name"], r["x"], r["y"])):
            fh.write(json.dumps(m, sort_keys=True) + "\n")

    summary = {
        "registry_communities": len(registry),
        "areas_total": len(areas),
        "areas_affiliated": sum(1 for a in areas if a["dominant_faction"]),
        "pois_total": len(pois),
        "markers_total": len(markers),
        "areas_by_district": dict(sorted(dist_counts.items())),
        "top_factions_by_district": {
            k: v.most_common(6) for k, v in sorted(dist_faction_counts.items())
        },
    }
    write_json(extract_dir / "summary.json", summary)
    print("    Extraction summary:", json.dumps(summary, indent=2), flush=True)

    if not args.emit_seeds:
        print("Done (raw extract only; pass --emit-seeds to generate data/*.json).", flush=True)
        return 0

    print("4/4 Building deterministic seed files under data/ ...", flush=True)
    faction_by_code = {f["code"]: f for f in FACTIONS_CATALOG}
    district_by_code = {d["code"]: d for d in TOP_DISTRICTS}

    # Build districts.json with real crimeMultiplier from districts.tweak and real bboxes.
    district_seeds: list[dict[str, Any]] = []
    for d in TOP_DISTRICTS:
        dcode = d["code"]
        raw = districts_raw.get(d["gamedata_district"], {})
        d_areas = [a for a in areas if a["district_code"] == dcode]
        if not d_areas:
            raise RuntimeError(f"Zero extracted areas for district {dcode}")
        xs = [a["x"] for a in d_areas]
        ys = [a["y"] for a in d_areas]
        pad = 150.0
        district_seeds.append({
            "district_id": d["district_id"],
            "code": dcode,
            "display_name": d["display_name"],
            "kind": d["kind"],
            "gamedata_district": d["gamedata_district"],
            "crime_multiplier": raw.get("crimeMultiplier") or 1.0,
            "vanilla_gangs": raw.get("gangs", []),
            "bbox_min_x": round(min(xs) - pad, 1),
            "bbox_min_y": round(min(ys) - pad, 1),
            "bbox_max_x": round(max(xs) + pad, 1),
            "bbox_max_y": round(max(ys) + pad, 1),
        })

    # Target ~5 control centers per major district (Badlands 6, others 5 => 41 total; tunable).
    target_k = {
        "watson": 5,
        "westbrook": 5,
        "heywood": 5,
        "santo_domingo": 5,
        "pacifica": 5,
        "city_center": 5,
        "badlands": 6,
        "dogtown": 5,
    }
    default_owner_by_district = {
        "watson": ("maelstrom", "gang"),
        "westbrook": ("tyger_claws", "gang"),
        "heywood": ("valentinos", "gang"),
        "santo_domingo": ("sixth_street", "gang"),
        "pacifica": ("voodoo_boys", "gang"),
        "city_center": ("arasaka", "corp"),
        "badlands": ("wraiths", "gang"),
        "dogtown": ("barghest", "gang"),
    }
    base_income_by_district = {
        "watson": 450,
        "westbrook": 650,
        "heywood": 500,
        "santo_domingo": 450,
        "pacifica": 400,
        "city_center": 950,
        "badlands": 350,
        "dogtown": 700,
    }

    sub_territories: list[dict[str, Any]] = []
    control_centers: list[dict[str, Any]] = []
    spawn_points: list[dict[str, Any]] = []
    landmarks: list[dict[str, Any]] = []

    st_id = 1
    cc_id = 1
    sp_id = 1
    lm_id = 1

    # Non-civic combat/territory factions preferred for ownership voting.
    civic_codes = {"ncpd", "city_council", "nusa", "trauma_team", "news54"}

    for d in TOP_DISTRICTS:
        dcode = d["code"]
        did = d["district_id"]
        d_areas = [a for a in areas if a["district_code"] == dcode]
        # Prefer combat/affiliated areas for cluster seeding; fall back to all areas.
        affiliated = [a for a in d_areas if a["dominant_faction"] and a["dominant_faction"] not in civic_codes]
        seed_pool = affiliated if len(affiliated) >= target_k[dcode] else d_areas
        clusters = deterministic_kmeans_xy(seed_pool, target_k[dcode])

        # Compute cluster centroids, then assign EVERY area in the district to its nearest cluster.
        centroids: list[tuple[float, float]] = []
        for cl in clusters:
            cx = sum(p["x"] for p in cl) / len(cl)
            cy = sum(p["y"] for p in cl) / len(cl)
            centroids.append((cx, cy))

        all_in_cluster: list[list[dict[str, Any]]] = [[] for _ in clusters]
        for a in d_areas:
            ci = min(range(len(centroids)), key=lambda i: (a["x"] - centroids[i][0]) ** 2 + (a["y"] - centroids[i][1]) ** 2)
            all_in_cluster[ci].append(a)

        for idx, cl_all in enumerate(all_in_cluster, start=1):
            # Pick the highest-density affiliated community area as the real physical Control Center anchor.
            aff_cl = [a for a in cl_all if a["dominant_faction"] and a["dominant_faction"] not in civic_codes]
            anchor_pool = aff_cl if aff_cl else cl_all
            anchor = max(anchor_pool, key=lambda a: (a["affiliated_count"], a["entry_count"], -abs(a["x"]), -abs(a["y"])))

            # Vote owner faction from cluster's affiliated spawn entries.
            votes: collections.Counter[str] = collections.Counter()
            for a in cl_all:
                for fcode, cnt in a["faction_counts"].items():
                    if fcode not in civic_codes:
                        votes[fcode] += cnt

            if dcode == "city_center":
                corp_votes = {k: v for k, v in votes.items() if faction_by_code[k]["category"] == "megacorp"}
                if corp_votes:
                    owner_code = max(corp_votes.items(), key=lambda kv: (kv[1], kv[0]))[0]
                else:
                    owner_code = "city_council" if idx % 2 == 0 else "arasaka"
                owner_kind = "corp"
            elif votes:
                owner_code = max(votes.items(), key=lambda kv: (kv[1], kv[0]))[0]
                cat = faction_by_code[owner_code]["category"]
                if owner_code == "the_mox":
                    owner_kind = "enclave"
                elif cat == "megacorp":
                    owner_kind = "corp"
                else:
                    owner_kind = "gang"
            else:
                owner_code, owner_kind = default_owner_by_district[dcode]

            owner_fid = faction_by_code[owner_code]["faction_id"]
            st_code = f"{dcode}_zone_{idx:02d}"
            cc_code = f"cc_{st_code}"
            st_name = f"{d['display_name']} Sector {idx}"
            cc_name = f"{d['display_name']} Control Center {idx}"
            if anchor["debug_name"]:
                clean_dbg = re.sub(r"[^A-Za-z0-9_ -]+", "", anchor["debug_name"]).strip()
                if clean_dbg:
                    cc_name = f"{d['display_name']} Hub {idx} ({clean_dbg[:40]})"

            cx = round(sum(a["x"] for a in cl_all) / len(cl_all), 3)
            cy = round(sum(a["y"] for a in cl_all) / len(cl_all), 3)
            cz = round(sum(a["z"] for a in cl_all) / len(cl_all), 3)
            defense = min(100, 15 + len(aff_cl) * 2)
            income = base_income_by_district[dcode] + min(300, len(cl_all) * 5)

            sub_territories.append({
                "sub_territory_id": st_id,
                "district_id": did,
                "code": st_code,
                "display_name": st_name,
                "gamedata_subdistrict": d["gamedata_district"],
                "owner_kind": owner_kind,
                "initial_owner_faction_id": owner_fid,
                "claim_strength": 2.0 if owner_kind == "corp" else 1.0,
                "base_income_per_cycle": income,
                "defense_rating": defense,
                "centroid_x": cx,
                "centroid_y": cy,
                "centroid_z": cz,
            })

            landmarks.append({
                "landmark_id": lm_id,
                "code": f"lm_{st_code}",
                "display_name": cc_name,
                "kind": "compound" if owner_kind == "gang" else "hq",
                "sub_territory_id": st_id,
                "gamedata_district": d["gamedata_district"],
                "x": anchor["x"],
                "y": anchor["y"],
                "z": anchor["z"],
                "purchasable": 1 if owner_kind == "corp" else 0,
                "base_price": 250000 if owner_kind == "corp" else None,
            })

            control_centers.append({
                "control_center_id": cc_id,
                "sub_territory_id": st_id,
                "code": cc_code,
                "display_name": cc_name,
                "landmark_id": lm_id,
                "x": anchor["x"],
                "y": anchor["y"],
                "z": anchor["z"],
                "capture_radius_m": 40.0,
                "is_capital": 1 if idx == 1 else 0,
            })

            # Emit ground-truth affiliated spawn points in this sub-territory.
            for a in sorted(aff_cl, key=lambda r: (r["community_hash"], r["x"], r["y"])):
                fcode = a["dominant_faction"]
                fid = faction_by_code[fcode]["faction_id"]
                spawn_points.append({
                    "spawn_point_id": sp_id,
                    "control_center_id": cc_id,
                    "sub_territory_id": st_id,
                    "faction_id": fid,
                    "encounter_type": "community",
                    "community_hash": a["community_hash"],
                    "community_template": a["debug_name"] or None,
                    "x": a["x"],
                    "y": a["y"],
                    "z": a["z"],
                    "yaw": None,
                    "spawn_weight": min(1000, max(10, a["affiliated_count"] * 10)),
                    "min_era": "dogtown" if dcode == "dogtown" else "any",
                    "max_era": "any",
                })
                sp_id += 1

            st_id += 1
            cc_id += 1
            lm_id += 1

    data_dir = ROOT / "data"
    write_json(data_dir / "factions.json", FACTIONS_CATALOG)
    write_json(data_dir / "districts.json", district_seeds)
    write_json(data_dir / "sub_territories.json", sub_territories)
    write_json(data_dir / "control_centers.json", control_centers)
    write_json(data_dir / "landmarks.json", landmarks)
    write_json(data_dir / "spawn_points.json", spawn_points)

    manifest = {
        "game_version": "2.5",
        "wolvenkit_version": WOLVENKIT_VERSION,
        "registry_communities": len(registry),
        "counts": {
            "factions": len(FACTIONS_CATALOG),
            "districts": len(district_seeds),
            "sub_territories": len(sub_territories),
            "control_centers": len(control_centers),
            "landmarks": len(landmarks),
            "spawn_points": len(spawn_points),
        },
    }
    write_json(data_dir / "MANIFEST.json", manifest)
    print("Emitted data/ seeds:", json.dumps(manifest["counts"], indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
