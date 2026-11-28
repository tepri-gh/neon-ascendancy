#!/usr/bin/env python3
"""Compile deterministic static world.db from Git-tracked data/*.json seeds.

Applies data/schema/world_v1.sql then data/schema/world_v2.sql (living-site
model), loads the v1 seeds plus data/sites/*.json, and validates:

  - Stable unique primary IDs and unique codes
  - Finite coordinates inside each district bounding box
  - Referential integrity (PRAGMA foreign_key_check)
  - Full level-0 territory_cells grid coverage per district (O(1) RAM lookup)
  - Pre-partitioned territory_cell_polygons outer rings for map visualization
  - R-Tree spatial prefilter population (sub_territory, landmark, spawn_point,
    site, site_spot)
  - Site rollups agree with their child tables (no boolean soup)
  - Site FK targets resolved (district, sub-territory, control center, faction)
  - PRAGMA integrity_check == 'ok'
  - Deterministic SHA-256 content_hash stored in meta
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sqlite3
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
SCHEMA_V1_PATH = DATA_DIR / "schema" / "world_v1.sql"
SCHEMA_V2_PATH = DATA_DIR / "schema" / "world_v2.sql"
SITES_DIR = DATA_DIR / "sites"
ROADS_DIR = DATA_DIR / "roads"
DEFAULT_OUT = ROOT / "dist" / "world.db"

CELL_SIZE_M = 100.0  # 100 m level-0 ownership grid cells (~80x100 across NC)
SCHEMA_VERSION = "2"

ROAD_SEED_FILES = (
    "chunks.json",
    "nodes.json",
    "edges.json",
    "meta.json",
)

SITE_SEED_FILES = (
    "sites.json",
    "bindings.json",
    "suitabilities.json",
    "communities.json",
    "rosters.json",
    "phases.json",
    "slots.json",
    "spots.json",
    "patrols.json",
    "patrol_points.json",
    "guards.json",
    "guard_communities.json",
    "devices.json",
    "doors.json",
    "triggers.json",
    "variants.json",
    "links.json",
    "meta.json",
)

WORLD_SEED_FILES = (
    "factions.json",
    "districts.json",
    "sub_territories.json",
    "control_centers.json",
    "faction_headquarters.json",
    "landmarks.json",
    "spawn_points.json",
)


def load_json(name: str) -> Any:
    path = DATA_DIR / name
    if not path.is_file():
        raise FileNotFoundError(f"Missing seed file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_site_seed(name: str) -> Any:
    path = SITES_DIR / name
    if not path.is_file():
        raise FileNotFoundError(
            f"Missing site seed file: {path}\nRun tools/extract-sites.py first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def load_road_seed(name: str) -> Any:
    path = ROADS_DIR / name
    if not path.is_file():
        raise FileNotFoundError(
            f"Missing road seed file: {path}\nRun tools/extract-roads.py first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def json_text(value: Any) -> str | None:
    """Lists/dicts become compact sorted JSON text; scalars become TEXT."""
    if value is None:
        return None
    if isinstance(value, (list, dict)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)


def compute_seed_hash(
    files: list[str],
    site_files: list[str],
    road_files: list[str],
) -> str:
    h = hashlib.sha256()
    h.update(SCHEMA_V1_PATH.read_bytes())
    h.update(b"\0")
    h.update(SCHEMA_V2_PATH.read_bytes())
    h.update(b"\0")
    for name in sorted(files):
        h.update(name.encode("utf-8"))
        h.update(b"\0")
        h.update((DATA_DIR / name).read_bytes())
        h.update(b"\0")
    for name in sorted(site_files):
        h.update(b"data/sites/")
        h.update(name.encode("utf-8"))
        h.update(b"\0")
        h.update((SITES_DIR / name).read_bytes())
        h.update(b"\0")
    for name in sorted(road_files):
        h.update(b"data/roads/")
        h.update(name.encode("utf-8"))
        h.update(b"\0")
        h.update((ROADS_DIR / name).read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def build_grid_and_polygons(
    districts: list[dict[str, Any]],
    sub_territories: list[dict[str, Any]],
    control_centers: list[dict[str, Any]],
) -> tuple[list[tuple[int, int, int, int]], dict[int, tuple[float, float, float, float]], list[tuple[int, int, str, int, float, float]]]:
    """Generate level-0 territory_cells (nearest control center per district) and convex hull polygons."""
    cc_by_st = {cc["sub_territory_id"]: cc for cc in control_centers}
    sts_by_dist: dict[int, list[dict[str, Any]]] = {}
    for st in sub_territories:
        sts_by_dist.setdefault(st["district_id"], []).append(st)

    # Value is (dist_sq, sub_territory_id, is_badlands).
    # Non-badlands districts win over the map-spanning badlands bbox; among overlapping
    # non-badlands district bboxes, the geometrically nearest control center wins.
    best_cells: dict[tuple[int, int], tuple[float, int, bool]] = {}
    st_points: dict[int, list[tuple[float, float]]] = {st["sub_territory_id"]: [] for st in sub_territories}

    for d in districts:
        did = d["district_id"]
        dsts = sts_by_dist.get(did, [])
        if not dsts:
            continue
        is_badlands = d["kind"] == "badlands"
        anchors = []
        for st in dsts:
            cc = cc_by_st[st["sub_territory_id"]]
            anchors.append((st["sub_territory_id"], cc["x"], cc["y"]))

        min_cx = math.floor(d["bbox_min_x"] / CELL_SIZE_M)
        max_cx = math.floor(d["bbox_max_x"] / CELL_SIZE_M)
        min_cy = math.floor(d["bbox_min_y"] / CELL_SIZE_M)
        max_cy = math.floor(d["bbox_max_y"] / CELL_SIZE_M)

        for cx in range(min_cx, max_cx + 1):
            wx = (cx + 0.5) * CELL_SIZE_M
            for cy in range(min_cy, max_cy + 1):
                wy = (cy + 0.5) * CELL_SIZE_M
                prev = best_cells.get((cx, cy))
                if prev is not None and not prev[2] and is_badlands:
                    continue
                best_st = -1
                best_d2 = float("inf")
                for stid, ax, ay in anchors:
                    d2 = (wx - ax) ** 2 + (wy - ay) ** 2
                    if d2 < best_d2 or (d2 == best_d2 and stid < best_st):
                        best_d2 = d2
                        best_st = stid
                if (
                    prev is None
                    or (prev[2] and not is_badlands)
                    or best_d2 < prev[0]
                    or (best_d2 == prev[0] and best_st < prev[1])
                ):
                    best_cells[(cx, cy)] = (best_d2, best_st, is_badlands)

    cells: dict[tuple[int, int], int] = {k: v[1] for k, v in best_cells.items()}

    for (cx, cy), stid in cells.items():
        wx = (cx + 0.5) * CELL_SIZE_M
        wy = (cy + 0.5) * CELL_SIZE_M
        st_points[stid].append((wx, wy))

    # Ensure every sub-territory has at least its own control center cell.
    for st in sub_territories:
        stid = st["sub_territory_id"]
        cc = cc_by_st[stid]
        if not st_points[stid]:
            cx = math.floor(cc["x"] / CELL_SIZE_M)
            cy = math.floor(cc["y"] / CELL_SIZE_M)
            cells[(cx, cy)] = stid
            st_points[stid].append((cc["x"], cc["y"]))

    # Compute bboxes and Andrew's monotone chain convex hull for each sub-territory polygon.
    bboxes: dict[int, tuple[float, float, float, float]] = {}
    poly_rows: list[tuple[int, int, str, int, float, float]] = []

    def cross(o: tuple[float, float], a: tuple[float, float], b: tuple[float, float]) -> float:
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    for st in sub_territories:
        stid = st["sub_territory_id"]
        pts = sorted(set(st_points[stid]))
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        half = CELL_SIZE_M * 0.5
        bboxes[stid] = (min(xs) - half, max(xs) + half, min(ys) - half, max(ys) + half)

        if len(pts) < 3:
            min_x, max_x, min_y, max_y = bboxes[stid]
            hull = [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)]
        else:
            lower: list[tuple[float, float]] = []
            for p in pts:
                while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
                    lower.pop()
                lower.append(p)
            upper: list[tuple[float, float]] = []
            for p in reversed(pts):
                while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
                    upper.pop()
                upper.append(p)
            hull = lower[:-1] + upper[:-1]

        for pi, (hx, hy) in enumerate(hull):
            poly_rows.append((stid, 0, "outer", pi, round(hx, 2), round(hy, 2)))

    cell_rows = [(0, cx, cy, stid) for (cx, cy), stid in sorted(cells.items())]
    return cell_rows, bboxes, poly_rows


def insert_site_tables(con: sqlite3.Connection, seeds: dict[str, Any]) -> dict[str, int]:
    """Insert the v2 living-site tables from data/sites/*.json."""
    sites = seeds["sites.json"]
    bindings = seeds["bindings.json"]
    suitabilities = seeds["suitabilities.json"]
    communities = seeds["communities.json"]
    rosters = seeds["rosters.json"]
    phases = seeds["phases.json"]
    slots = seeds["slots.json"]
    spots = seeds["spots.json"]
    patrols = seeds["patrols.json"]
    patrol_points = seeds["patrol_points.json"]
    guards = seeds["guards.json"]
    guard_communities = seeds["guard_communities.json"]
    devices = seeds["devices.json"]
    doors = seeds["doors.json"]
    triggers = seeds["triggers.json"]
    variants = seeds["variants.json"]
    links = seeds["links.json"]

    if not sites:
        raise RuntimeError("data/sites/sites.json is empty; run tools/extract-sites.py")

    con.executemany(
        """INSERT INTO world_sites(
             site_id, code, display_name, site_kind, source_family,
             district_id, sub_territory_id, control_center_id,
             anchor_x, anchor_y, anchor_z,
             bbox_min_x, bbox_min_y, bbox_min_z, bbox_max_x, bbox_max_y, bbox_max_z,
             radius_m, is_interior, interior_map_coords, floor_count,
             default_faction_id, initial_owner_faction_id, faction_source,
             tier, difficulty, loot_tier,
             has_patrols, has_workspots, has_guard_areas, has_security_devices,
             has_doors, has_community, spot_count, patrol_count, device_count, community_count,
             quest_prefab_ref, quest_sector_path, sector_category, streaming_block,
             extraction_confidence, source_archive, source_path
           ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        [
            (
                row["site_id"], row["code"], row.get("display_name"), row["site_kind"],
                row["source_family"], row["district_id"], row.get("sub_territory_id"),
                row.get("control_center_id"),
                row["anchor_x"], row["anchor_y"], row["anchor_z"],
                row.get("bbox_min_x"), row.get("bbox_min_y"), row.get("bbox_min_z"),
                row.get("bbox_max_x"), row.get("bbox_max_y"), row.get("bbox_max_z"),
                row["radius_m"], row["is_interior"], row.get("interior_map_coords"),
                row.get("floor_count"), row.get("default_faction_id"),
                row.get("initial_owner_faction_id"), row["faction_source"],
                row["tier"], row["difficulty"], row["loot_tier"],
                row["has_patrols"], row["has_workspots"], row["has_guard_areas"],
                row["has_security_devices"], row["has_doors"], row["has_community"],
                row["spot_count"], row["patrol_count"], row["device_count"], row["community_count"],
                row.get("quest_prefab_ref"), row.get("quest_sector_path"),
                row.get("sector_category"), row.get("streaming_block"),
                row["extraction_confidence"], row["source_archive"], row["source_path"],
            )
            for row in sorted(sites, key=lambda r: r["site_id"])
        ],
    )
    con.executemany(
        "INSERT INTO site_rtree(id, min_x, max_x, min_y, max_y) VALUES(?,?,?,?,?)",
        [
            (row["site_id"], row["anchor_x"], row["anchor_x"], row["anchor_y"], row["anchor_y"])
            for row in sorted(sites, key=lambda r: r["site_id"])
        ],
    )
    con.executemany(
        """INSERT INTO site_bindings(
             site_id, content_kind, content_code, quest_phase_path,
             quest_resource_path, is_primary
           ) VALUES(?,?,?,?,?,?)""",
        [
            (
                row["site_id"], row["content_kind"], row["content_code"],
                row.get("quest_phase_path"), row.get("quest_resource_path"),
                row["is_primary"],
            )
            for row in bindings
        ],
    )
    con.executemany(
        "INSERT INTO site_suitabilities(site_id, suitability, score) VALUES(?,?,?)",
        [(row["site_id"], row["suitability"], row["score"]) for row in suitabilities],
    )
    con.executemany(
        """INSERT INTO site_communities(
             site_community_id, site_id, community_hash, spawner_ref, spawner_global_id,
             area_node_type, community_path, is_primary, entry_count, active_on_start,
             x, y, z
           ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        [
            (
                row["site_community_id"], row["site_id"], row["community_hash"],
                row["spawner_ref"], row.get("spawner_global_id"),
                row.get("area_node_type"), row.get("community_path"),
                row["is_primary"], row["entry_count"], row["active_on_start"],
                row["x"], row["y"], row["z"],
            )
            for row in communities
        ],
    )
    con.executemany(
        """INSERT INTO site_community_entries(
             entry_id, site_community_id, entry_name, character_record_id, faction_id,
             role_hint, initial_phase_name, entry_active_on_start, spawn_in_view
           ) VALUES(?,?,?,?,?,?,?,?,?)""",
        [
            (
                row["entry_id"], row["site_community_id"], row["entry_name"],
                row.get("character_record_id"), row.get("faction_id"),
                row.get("role_hint"), row.get("initial_phase_name"),
                row["entry_active_on_start"], row["spawn_in_view"],
            )
            for row in rosters
        ],
    )
    con.executemany(
        """INSERT INTO site_community_phases(
             phase_id, entry_id, phase_name, always_spawned, hour, quantity, is_sequence
           ) VALUES(?,?,?,?,?,?,?)""",
        [
            (
                row["phase_id"], row["entry_id"], row["phase_name"],
                row["always_spawned"], row["hour"], row["quantity"], row["is_sequence"],
            )
            for row in phases
        ],
    )
    con.executemany(
        """INSERT INTO site_spots(
             spot_id, site_id, node_ref, global_node_id, debug_name, workspot_resource,
             spot_role, markings, is_workspot_infinite, is_workspot_static,
             actor_bodytype, floor_index, x, y, z, yaw, source_sector
           ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        [
            (
                row["spot_id"], row["site_id"], row["node_ref"], row.get("global_node_id"),
                row.get("debug_name"), row.get("workspot_resource"), row.get("spot_role"),
                json_text(row.get("markings")), row["is_workspot_infinite"],
                row["is_workspot_static"], row.get("actor_bodytype"), row.get("floor_index"),
                row["x"], row["y"], row["z"], row.get("yaw"), row["source_sector"],
            )
            for row in spots
        ],
    )
    con.executemany(
        "INSERT INTO site_spot_rtree(id, min_x, max_x, min_y, max_y) VALUES(?,?,?,?,?)",
        [
            (row["spot_id"], row["x"], row["x"], row["y"], row["y"])
            for row in spots
        ],
    )
    con.executemany(
        """INSERT INTO site_community_slots(
             phase_id, slot_index, spot_ref, spot_id, markings
           ) VALUES(?,?,?,?,?)""",
        [
            (
                row["phase_id"], row["slot_index"], row["spot_ref"],
                row.get("spot_id"), json_text(row.get("markings")),
            )
            for row in slots
        ],
    )
    con.executemany(
        """INSERT INTO site_patrols(
             patrol_id, site_id, node_ref, global_node_id, debug_name, point_count,
             floor_index, x, y, z, source_sector
           ) VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
        [
            (
                row["patrol_id"], row["site_id"], row["node_ref"], row.get("global_node_id"),
                row.get("debug_name"), row["point_count"], row.get("floor_index"),
                row["x"], row["y"], row["z"], row["source_sector"],
            )
            for row in patrols
        ],
    )
    con.executemany(
        """INSERT INTO site_patrol_points(
             patrol_id, point_index, spot_ref, spot_id, point_type, x, y, z
           ) VALUES(?,?,?,?,?,?,?,?)""",
        [
            (
                row["patrol_id"], row["point_index"], row["spot_ref"], row.get("spot_id"),
                row["point_type"], row.get("x"), row.get("y"), row.get("z"),
            )
            for row in patrol_points
        ],
    )
    con.executemany(
        """INSERT INTO site_guard_areas(
             guard_area_id, site_id, node_ref, global_node_id, debug_name,
             pursuit_range_m, floor_index, x, y, z, source_sector
           ) VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
        [
            (
                row["guard_area_id"], row["site_id"], row["node_ref"],
                row.get("global_node_id"), row.get("debug_name"), row.get("pursuit_range_m"),
                row.get("floor_index"), row["x"], row["y"], row["z"], row["source_sector"],
            )
            for row in guards
        ],
    )
    con.executemany(
        """INSERT INTO site_guard_area_communities(
             guard_area_id, community_ref, is_primary, entry_names
           ) VALUES(?,?,?,?)""",
        [
            (
                row["guard_area_id"], row["community_ref"], row["is_primary"],
                json_text(row.get("entry_names")),
            )
            for row in guard_communities
        ],
    )
    con.executemany(
        """INSERT INTO site_devices(
             device_id, site_id, node_ref, global_node_id, debug_name, device_kind,
             controller_class, entity_template, connected_community_ref,
             is_quest_gated, floor_index, x, y, z, source_sector
           ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        [
            (
                row["device_id"], row["site_id"], row["node_ref"], row.get("global_node_id"),
                row.get("debug_name"), row["device_kind"], row.get("controller_class"),
                row.get("entity_template"), row.get("connected_community_ref"),
                row["is_quest_gated"], row.get("floor_index"),
                row["x"], row["y"], row["z"], row["source_sector"],
            )
            for row in devices
        ],
    )
    con.executemany(
        """INSERT INTO site_doors(
             door_id, site_id, device_id, node_ref, global_node_id, debug_name,
             door_role, controller_class, default_state, requires_power,
             unlock_action, vanilla_lock_action
           ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
        [
            (
                row["door_id"], row["site_id"], row.get("device_id"), row["node_ref"],
                row.get("global_node_id"), row.get("debug_name"), row["door_role"],
                row["controller_class"], row.get("default_state"), row["requires_power"],
                row["unlock_action"], row.get("vanilla_lock_action"),
            )
            for row in doors
        ],
    )
    con.executemany(
        """INSERT INTO site_triggers(
             trigger_id, site_id, node_ref, global_node_id, debug_name,
             trigger_role, volume_json, x, y, z
           ) VALUES(?,?,?,?,?,?,?,?,?,?)""",
        [
            (
                row["trigger_id"], row["site_id"], row["node_ref"], row.get("global_node_id"),
                row.get("debug_name"), row.get("trigger_role"), row.get("volume_json"),
                row["x"], row["y"], row["z"],
            )
            for row in triggers
        ],
    )
    con.executemany(
        """INSERT INTO site_variants(
             site_variant_id, site_id, sector_path, variant_name, variant_id,
             enabled_by_default, node_ref
           ) VALUES(?,?,?,?,?,?,?)""",
        [
            (
                row["site_variant_id"], row["site_id"], row["sector_path"],
                row["variant_name"], row["variant_id"], row["enabled_by_default"],
                row.get("node_ref"),
            )
            for row in variants
        ],
    )
    con.executemany(
        """INSERT INTO site_links(
             from_site_id, to_site_id, link_kind, weight, distance_m
           ) VALUES(?,?,?,?,?)""",
        [
            (
                row["from_site_id"], row["to_site_id"], row["link_kind"],
                row["weight"], row.get("distance_m"),
            )
            for row in links
        ],
    )
    return {
        "world_sites": len(sites),
        "site_bindings": len(bindings),
        "site_suitabilities": len(suitabilities),
        "site_communities": len(communities),
        "site_community_entries": len(rosters),
        "site_community_phases": len(phases),
        "site_community_slots": len(slots),
        "site_spots": len(spots),
        "site_patrols": len(patrols),
        "site_patrol_points": len(patrol_points),
        "site_guard_areas": len(guards),
        "site_guard_area_communities": len(guard_communities),
        "site_devices": len(devices),
        "site_doors": len(doors),
        "site_triggers": len(triggers),
        "site_variants": len(variants),
        "site_links": len(links),
    }


def validate_site_tables(con: sqlite3.Connection) -> None:
    """Assert site rollups and invariants before publishing."""
    mismatched = con.execute(
        """SELECT s.code, s.spot_count, COUNT(sp.spot_id)
             FROM world_sites s
             LEFT JOIN site_spots sp ON sp.site_id = s.site_id
            GROUP BY s.site_id
           HAVING s.spot_count <> COUNT(sp.spot_id)
            LIMIT 5"""
    ).fetchall()
    if mismatched:
        raise RuntimeError(f"site spot_count rollup mismatch: {mismatched}")

    mismatched = con.execute(
        """SELECT s.code, s.patrol_count, COUNT(p.patrol_id)
             FROM world_sites s
             LEFT JOIN site_patrols p ON p.site_id = s.site_id
            GROUP BY s.site_id
           HAVING s.patrol_count <> COUNT(p.patrol_id)
            LIMIT 5"""
    ).fetchall()
    if mismatched:
        raise RuntimeError(f"site patrol_count rollup mismatch: {mismatched}")

    mismatched = con.execute(
        """SELECT s.code, s.device_count, COUNT(d.device_id)
             FROM world_sites s
             LEFT JOIN site_devices d ON d.site_id = s.site_id
            GROUP BY s.site_id
           HAVING s.device_count <> COUNT(d.device_id)
            LIMIT 5"""
    ).fetchall()
    if mismatched:
        raise RuntimeError(f"site device_count rollup mismatch: {mismatched}")

    mismatched = con.execute(
        """SELECT s.code, s.community_count, COUNT(c.site_community_id)
             FROM world_sites s
             LEFT JOIN site_communities c ON c.site_id = s.site_id
            GROUP BY s.site_id
           HAVING s.community_count <> COUNT(c.site_community_id)
            LIMIT 5"""
    ).fetchall()
    if mismatched:
        raise RuntimeError(f"site community_count rollup mismatch: {mismatched}")

    unplaced = con.execute(
        """SELECT COUNT(*) FROM world_sites
            WHERE district_id IS NULL OR sub_territory_id IS NULL
               OR control_center_id IS NULL"""
    ).fetchone()[0]
    if unplaced:
        raise RuntimeError(f"{unplaced} world_sites rows lack a territory anchor")

    orphan_slots = con.execute(
        """SELECT COUNT(*) FROM site_community_slots sl
             LEFT JOIN site_spots sp ON sp.spot_id = sl.spot_id
            WHERE sl.spot_id IS NOT NULL AND sp.spot_id IS NULL"""
    ).fetchone()[0]
    if orphan_slots:
        raise RuntimeError(f"{orphan_slots} site_community_slots reference missing spots")

    bad_links = con.execute(
        """SELECT COUNT(*) FROM site_links l
             LEFT JOIN world_sites a ON a.site_id = l.from_site_id
             LEFT JOIN world_sites b ON b.site_id = l.to_site_id
            WHERE a.site_id IS NULL OR b.site_id IS NULL"""
    ).fetchone()[0]
    if bad_links:
        raise RuntimeError(f"{bad_links} site_links reference missing sites")

    views = con.execute("SELECT COUNT(*) FROM v_site_garrison").fetchone()[0]
    if views == 0:
        raise RuntimeError("v_site_garrison returned no rows")


def insert_road_tables(con: sqlite3.Connection, road_seeds: dict[str, Any]) -> dict[str, int]:
    """Insert road_chunks, road_chunk_rtree, road_nodes, and road_edges from data/roads/*.json."""
    chunks = road_seeds["chunks.json"]
    nodes = road_seeds["nodes.json"]
    edges = road_seeds["edges.json"]

    if not chunks or not nodes or not edges:
        raise RuntimeError("data/roads/*.json is empty; run tools/extract-roads.py")

    sorted_chunks = sorted(chunks, key=lambda r: r["chunk_id"])
    con.executemany(
        """INSERT INTO road_chunks(
             chunk_id, district_id, grid_x, grid_y, grid_z, lane_count, navmesh_ready
           ) VALUES(?,?,?,?,?,?,?)""",
        [
            (
                c["chunk_id"], c["district_id"], c["grid_x"], c["grid_y"], c["grid_z"],
                c["lane_count"], c["navmesh_ready"],
            )
            for c in sorted_chunks
        ],
    )
    con.executemany(
        "INSERT INTO road_chunk_rtree(id, min_x, max_x, min_y, max_y) VALUES(?,?,?,?,?)",
        [
            (c["chunk_id"], c["min_x"], c["max_x"], c["min_y"], c["max_y"])
            for c in sorted_chunks
        ],
    )
    con.executemany(
        "INSERT INTO road_nodes(node_id, chunk_id, x, y, z, lane) VALUES(?,?,?,?,?,?)",
        sorted(nodes, key=lambda r: r[0]),
    )
    con.executemany(
        """INSERT INTO road_edges(
             edge_id, from_node_id, to_node_id, chunk_id, length_m, speed_kph, is_tunnel
           ) VALUES(?,?,?,?,?,?,?)""",
        sorted(edges, key=lambda r: r[0]),
    )
    return {
        "road_chunks": len(chunks),
        "road_nodes": len(nodes),
        "road_edges": len(edges),
    }


def validate_road_tables(con: sqlite3.Connection) -> None:
    """Assert road graph structural and spatial invariants."""
    chunk_count = con.execute("SELECT COUNT(*) FROM road_chunks").fetchone()[0]
    rtree_count = con.execute("SELECT COUNT(*) FROM road_chunk_rtree").fetchone()[0]
    node_count = con.execute("SELECT COUNT(*) FROM road_nodes").fetchone()[0]
    edge_count = con.execute("SELECT COUNT(*) FROM road_edges").fetchone()[0]
    if chunk_count == 0 or node_count == 0 or edge_count == 0:
        raise RuntimeError(
            f"Road graph tables are empty (chunks={chunk_count}, nodes={node_count}, edges={edge_count})"
        )
    if chunk_count != rtree_count:
        raise RuntimeError(f"road_chunk_rtree count {rtree_count} != road_chunks count {chunk_count}")
    self_loops = con.execute(
        "SELECT COUNT(*) FROM road_edges WHERE from_node_id = to_node_id"
    ).fetchone()[0]
    if self_loops:
        raise RuntimeError(f"{self_loops} self-loop road_edges found")
    bad_speed = con.execute(
        "SELECT COUNT(*) FROM road_edges WHERE speed_kph IS NULL OR speed_kph <= 0.0"
    ).fetchone()[0]
    if bad_speed:
        raise RuntimeError(f"{bad_speed} road_edges have invalid speed_kph")


def build_db(out_path: Path) -> dict[str, Any]:
    seeds = {name: load_json(name) for name in WORLD_SEED_FILES}
    site_seeds = {name: load_site_seed(name) for name in SITE_SEED_FILES}
    road_seeds = {name: load_road_seed(name) for name in ROAD_SEED_FILES}

    factions = seeds["factions.json"]
    districts = seeds["districts.json"]
    sub_territories = seeds["sub_territories.json"]
    control_centers = seeds["control_centers.json"]
    headquarters = seeds["faction_headquarters.json"]
    landmarks = seeds["landmarks.json"]
    spawn_points = seeds["spawn_points.json"]

    content_hash = compute_seed_hash(
        list(WORLD_SEED_FILES),
        list(SITE_SEED_FILES),
        list(ROAD_SEED_FILES),
    )

    # Coordinate and structural validation before writing.
    dist_map = {d["district_id"]: d for d in districts}
    for st in sub_territories:
        d = dist_map[st["district_id"]]
        for v in (st["centroid_x"], st["centroid_y"], st["centroid_z"]):
            if not math.isfinite(v):
                raise ValueError(f"Non-finite centroid in {st['code']}")
        if not (d["bbox_min_x"] <= st["centroid_x"] <= d["bbox_max_x"] and d["bbox_min_y"] <= st["centroid_y"] <= d["bbox_max_y"]):
            raise ValueError(f"Sub-territory {st['code']} centroid outside district {d['code']} bbox")

    faction_ids = {f["faction_id"] for f in factions}
    district_ids = {d["district_id"] for d in districts}
    st_ids = {st["sub_territory_id"] for st in sub_territories}
    cc_ids = {cc["control_center_id"] for cc in control_centers}
    for site in site_seeds["sites.json"]:
        if not all(math.isfinite(site[k]) for k in ("anchor_x", "anchor_y", "anchor_z")):
            raise ValueError(f"Non-finite site anchor: {site['code']}")
        if site["district_id"] not in district_ids:
            raise ValueError(f"Site {site['code']} references unknown district")
        if site["sub_territory_id"] not in st_ids:
            raise ValueError(f"Site {site['code']} references unknown sub-territory")
        if site["control_center_id"] not in cc_ids:
            raise ValueError(f"Site {site['code']} references unknown control center")
        for key in ("default_faction_id", "initial_owner_faction_id"):
            value = site.get(key)
            if value is not None and value not in faction_ids:
                raise ValueError(f"Site {site['code']} references unknown faction {value}")

    cell_rows, st_bboxes, poly_rows = build_grid_and_polygons(districts, sub_territories, control_centers)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = out_path.with_suffix(".db.tmp")
    if tmp_path.exists():
        tmp_path.unlink()

    con = sqlite3.connect(str(tmp_path))
    try:
        con.execute("PRAGMA foreign_keys = ON")
        con.executescript(SCHEMA_V1_PATH.read_text(encoding="utf-8"))
        con.executescript(SCHEMA_V2_PATH.read_text(encoding="utf-8"))
        with con:
            con.executemany(
                "INSERT INTO meta(key, value) VALUES(?, ?)",
                [
                    ("schema_version", SCHEMA_VERSION),
                    ("content_hash", content_hash),
                    ("game_version", "2.5"),
                    ("cell_size_m", str(CELL_SIZE_M)),
                    ("generator", "tools/build-world-db.py"),
                    ("site_seed_generator", site_seeds["meta.json"].get("generator", "tools/extract-sites.py")),
                    ("road_seed_generator", road_seeds["meta.json"].get("generator", "tools/extract-roads.py")),
                    ("road_chunk_xy_m", str(road_seeds["meta.json"].get("chunk_xy_m", 200.0))),
                    ("road_chunk_z_m", str(road_seeds["meta.json"].get("chunk_z_m", 50.0))),
                ],
            )
            con.executemany(
                """INSERT INTO districts(
                     district_id, code, display_name, kind, gamedata_district,
                     crime_multiplier, bbox_min_x, bbox_min_y, bbox_max_x, bbox_max_y
                   ) VALUES(?,?,?,?,?,?,?,?,?,?)""",
                [
                    (
                        d["district_id"], d["code"], d["display_name"], d["kind"],
                        d["gamedata_district"], d["crime_multiplier"],
                        d["bbox_min_x"], d["bbox_min_y"], d["bbox_max_x"], d["bbox_max_y"],
                    )
                    for d in sorted(districts, key=lambda r: r["district_id"])
                ],
            )
            con.executemany(
                """INSERT INTO factions(
                     faction_id, code, display_name, category, affiliation_enum, ticker,
                     parent_faction_id, color_rgba, income_multiplier, hostility_bias, is_playable
                   ) VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                [
                    (
                        f["faction_id"], f["code"], f["display_name"], f["category"],
                        f.get("affiliation_enum"), f.get("ticker"),
                        f.get("parent_faction_id"), f["color_rgba"],
                        f.get("income_multiplier", 1.0), f.get("hostility_bias", 0.0),
                        f.get("is_playable", 0),
                    )
                    for f in sorted(factions, key=lambda r: r["faction_id"])
                ],
            )
            con.executemany(
                """INSERT INTO sub_territories(
                     sub_territory_id, district_id, code, display_name, gamedata_subdistrict,
                     owner_kind, initial_owner_faction_id, claim_strength,
                     base_income_per_cycle, defense_rating, area_m2,
                     centroid_x, centroid_y, centroid_z
                   ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                [
                    (
                        st["sub_territory_id"], st["district_id"], st["code"], st["display_name"],
                        st.get("gamedata_subdistrict"), st["owner_kind"],
                        st.get("initial_owner_faction_id"), st.get("claim_strength", 1.0),
                        st["base_income_per_cycle"], st["defense_rating"],
                        round((st_bboxes[st["sub_territory_id"]][1] - st_bboxes[st["sub_territory_id"]][0])
                              * (st_bboxes[st["sub_territory_id"]][3] - st_bboxes[st["sub_territory_id"]][2]), 1),
                        st["centroid_x"], st["centroid_y"], st["centroid_z"],
                    )
                    for st in sorted(sub_territories, key=lambda r: r["sub_territory_id"])
                ],
            )
            con.executemany(
                """INSERT INTO landmarks(
                     landmark_id, code, display_name, kind, sub_territory_id,
                     gamedata_district, x, y, z, purchasable, base_price
                   ) VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                [
                    (
                        lm["landmark_id"], lm["code"], lm["display_name"], lm["kind"],
                        lm.get("sub_territory_id"), lm.get("gamedata_district"),
                        lm["x"], lm["y"], lm["z"], lm.get("purchasable", 0), lm.get("base_price"),
                    )
                    for lm in sorted(landmarks, key=lambda r: r["landmark_id"])
                ],
            )
            con.executemany(
                """INSERT INTO control_centers(
                     control_center_id, sub_territory_id, code, display_name, landmark_id,
                     x, y, z, capture_radius_m, is_capital, is_active
                   ) VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                [
                    (
                        cc["control_center_id"], cc["sub_territory_id"], cc["code"],
                        cc["display_name"], cc.get("landmark_id"),
                        cc["x"], cc["y"], cc["z"], cc.get("capture_radius_m", 40.0),
                        cc.get("is_capital", 0), cc["is_active"],
                    )
                    for cc in sorted(control_centers, key=lambda r: r["control_center_id"])
                ],
            )
            con.executemany(
                """INSERT INTO faction_headquarters(
                     faction_id, code, display_name, gamedata_subdistrict, x, y, z
                   ) VALUES(?,?,?,?,?,?,?)""",
                [
                    (
                        hq["faction_id"], hq["code"], hq["display_name"],
                        hq.get("gamedata_subdistrict"), hq["x"], hq["y"], hq["z"],
                    )
                    for hq in headquarters
                ],
            )
            con.executemany(
                """INSERT INTO spawn_points(
                     spawn_point_id, control_center_id, sub_territory_id, faction_id,
                     encounter_type, community_hash, community_template,
                     x, y, z, yaw, spawn_weight, min_era, max_era
                   ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                [
                    (
                        sp["spawn_point_id"], sp["control_center_id"], sp["sub_territory_id"],
                        sp["faction_id"], sp["encounter_type"], sp.get("community_hash"),
                        sp.get("community_template"), sp["x"], sp["y"], sp["z"],
                        sp.get("yaw"), sp.get("spawn_weight", 100),
                        sp.get("min_era", "any"), sp.get("max_era", "any"),
                    )
                    for sp in sorted(spawn_points, key=lambda r: r["spawn_point_id"])
                ],
            )
            con.executemany(
                "INSERT INTO territory_cells(level, cell_x, cell_y, sub_territory_id) VALUES(?,?,?,?)",
                cell_rows,
            )
            con.executemany(
                "INSERT INTO territory_cell_polygons(sub_territory_id, ring_index, ring_kind, point_index, x, y) VALUES(?,?,?,?,?,?)",
                poly_rows,
            )
            # Populate v1 R-Tree spatial prefilters.
            con.executemany(
                "INSERT INTO sub_territory_rtree(id, min_x, max_x, min_y, max_y) VALUES(?,?,?,?,?)",
                [(stid, *bbox) for stid, bbox in sorted(st_bboxes.items())],
            )
            con.executemany(
                "INSERT INTO landmark_rtree(id, min_x, max_x, min_y, max_y) VALUES(?,?,?,?,?)",
                [(lm["landmark_id"], lm["x"], lm["x"], lm["y"], lm["y"]) for lm in sorted(landmarks, key=lambda r: r["landmark_id"])],
            )
            con.executemany(
                "INSERT INTO spawn_point_rtree(id, min_x, max_x, min_y, max_y) VALUES(?,?,?,?,?)",
                [(sp["spawn_point_id"], sp["x"], sp["x"], sp["y"], sp["y"]) for sp in sorted(spawn_points, key=lambda r: r["spawn_point_id"])],
            )
            site_stats = insert_site_tables(con, site_seeds)
            road_stats = insert_road_tables(con, road_seeds)

        ic = con.execute("PRAGMA integrity_check").fetchall()
        if ic != [("ok",)]:
            raise RuntimeError(f"integrity_check failed: {ic}")
        fk = con.execute("PRAGMA foreign_key_check").fetchall()
        if fk:
            raise RuntimeError(f"foreign_key_check failed: {fk[:5]}")
        validate_site_tables(con)
        validate_road_tables(con)
        user_version = con.execute("PRAGMA user_version").fetchone()[0]
        if user_version != 2:
            raise RuntimeError(f"user_version is {user_version}, expected 2")
        con.execute("ANALYZE")
    finally:
        con.close()

    tmp_path.replace(out_path)
    stats = {
        "out": str(out_path),
        "bytes": out_path.stat().st_size,
        "content_hash": content_hash,
        "schema_version": SCHEMA_VERSION,
        "factions": len(factions),
        "districts": len(districts),
        "sub_territories": len(sub_territories),
        "control_centers": len(control_centers),
        "active_control_centers": sum(cc["is_active"] for cc in control_centers),
        "faction_headquarters": len(headquarters),
        "landmarks": len(landmarks),
        "spawn_points": len(spawn_points),
        "territory_cells": len(cell_rows),
        "polygon_vertices": len(poly_rows),
    }
    stats.update(site_stats)
    stats.update(road_stats)
    return stats


def main() -> int:
    ap = argparse.ArgumentParser(description="Compile data/*.json into dist/world.db.")
    ap.add_argument("-o", "--output", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--check", action="store_true", help="Verify deterministic rebuild matches existing output.")
    args = ap.parse_args()

    if args.check:
        probe = args.output.with_suffix(".check.db")
        try:
            a = build_db(probe)
            b = build_db(args.output)
            ha = hashlib.sha256(probe.read_bytes()).hexdigest()
            hb = hashlib.sha256(args.output.read_bytes()).hexdigest()
            if ha != hb:
                raise RuntimeError(f"Non-deterministic world.db build: {ha} != {hb}")
            print(
                f"world.db deterministic OK (sha256={hb[:16]}..., {b['bytes']} B, "
                f"schema v{b['schema_version']}, {b['world_sites']} sites, "
                f"{b['site_spots']} spots, {b['road_nodes']} road_nodes, {b['road_edges']} road_edges)"
            )
        finally:
            if probe.exists():
                probe.unlink()
        return 0

    stats = build_db(args.output)
    print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
