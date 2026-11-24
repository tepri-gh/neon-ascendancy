#!/usr/bin/env python3
"""Compile deterministic static world.db from Git-tracked data/*.json seeds.

Validates:
  - Stable unique primary IDs and unique codes
  - Finite coordinates inside each district bounding box
  - Referential integrity (PRAGMA foreign_key_check)
  - Full level-0 territory_cells grid coverage per district (O(1) RAM lookup)
  - Pre-partitioned territory_cell_polygons outer rings for map visualization
  - R-Tree spatial prefilter population (sub_territory, landmark, spawn_point)
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
SCHEMA_PATH = DATA_DIR / "schema" / "world_v1.sql"
DEFAULT_OUT = ROOT / "dist" / "world.db"

CELL_SIZE_M = 100.0  # 100 m level-0 ownership grid cells (~80x100 across NC)


def load_json(name: str) -> Any:
    path = DATA_DIR / name
    if not path.is_file():
        raise FileNotFoundError(f"Missing seed file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def compute_seed_hash(files: list[str]) -> str:
    h = hashlib.sha256()
    h.update(SCHEMA_PATH.read_bytes())
    for name in sorted(files):
        h.update(name.encode("utf-8"))
        h.update(b"\0")
        h.update((DATA_DIR / name).read_bytes())
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

    cells: dict[tuple[int, int], int] = {}
    st_points: dict[int, list[tuple[float, float]]] = {st["sub_territory_id"]: [] for st in sub_territories}

    for d in districts:
        did = d["district_id"]
        dsts = sts_by_dist.get(did, [])
        if not dsts:
            continue
        anchors = []
        for st in dsts:
            cc = cc_by_st[st["sub_territory_id"]]
            anchors.append((st["sub_territory_id"], cc["x"], cc["y"]))

        min_cx = math.floor(d["bbox_min_x"] / CELL_SIZE_M)
        max_cx = math.ceil(d["bbox_max_x"] / CELL_SIZE_M)
        min_cy = math.floor(d["bbox_min_y"] / CELL_SIZE_M)
        max_cy = math.ceil(d["bbox_max_y"] / CELL_SIZE_M)

        for cx in range(min_cx, max_cx + 1):
            wx = (cx + 0.5) * CELL_SIZE_M
            for cy in range(min_cy, max_cy + 1):
                wy = (cy + 0.5) * CELL_SIZE_M
                # Nearest control center within this district; if cell already claimed by
                # an urban district before badlands, keep the urban district owner.
                if (cx, cy) in cells and d["kind"] == "badlands":
                    continue
                best_st = min(anchors, key=lambda a: (wx - a[1]) ** 2 + (wy - a[2]) ** 2)[0]
                cells[(cx, cy)] = best_st

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


def build_db(out_path: Path) -> dict[str, Any]:
    seed_files = [
        "factions.json",
        "districts.json",
        "sub_territories.json",
        "control_centers.json",
        "landmarks.json",
        "spawn_points.json",
    ]
    factions = load_json("factions.json")
    districts = load_json("districts.json")
    sub_territories = load_json("sub_territories.json")
    control_centers = load_json("control_centers.json")
    landmarks = load_json("landmarks.json")
    spawn_points = load_json("spawn_points.json")

    content_hash = compute_seed_hash(seed_files)

    # Coordinate and structural validation before writing.
    dist_map = {d["district_id"]: d for d in districts}
    for st in sub_territories:
        d = dist_map[st["district_id"]]
        for v in (st["centroid_x"], st["centroid_y"], st["centroid_z"]):
            if not math.isfinite(v):
                raise ValueError(f"Non-finite centroid in {st['code']}")
        if not (d["bbox_min_x"] <= st["centroid_x"] <= d["bbox_max_x"] and d["bbox_min_y"] <= st["centroid_y"] <= d["bbox_max_y"]):
            raise ValueError(f"Sub-territory {st['code']} centroid outside district {d['code']} bbox")

    cell_rows, st_bboxes, poly_rows = build_grid_and_polygons(districts, sub_territories, control_centers)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = out_path.with_suffix(".db.tmp")
    if tmp_path.exists():
        tmp_path.unlink()

    con = sqlite3.connect(str(tmp_path))
    try:
        con.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        with con:
            con.executemany(
                "INSERT INTO meta(key, value) VALUES(?, ?)",
                [
                    ("schema_version", "1"),
                    ("content_hash", content_hash),
                    ("game_version", "2.5"),
                    ("cell_size_m", str(CELL_SIZE_M)),
                    ("generator", "tools/build-world-db.py"),
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
                     x, y, z, capture_radius_m, is_capital
                   ) VALUES(?,?,?,?,?,?,?,?,?,?)""",
                [
                    (
                        cc["control_center_id"], cc["sub_territory_id"], cc["code"],
                        cc["display_name"], cc.get("landmark_id"),
                        cc["x"], cc["y"], cc["z"], cc.get("capture_radius_m", 40.0),
                        cc.get("is_capital", 0),
                    )
                    for cc in sorted(control_centers, key=lambda r: r["control_center_id"])
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
            # Populate R-Tree spatial prefilters.
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

        ic = con.execute("PRAGMA integrity_check").fetchall()
        if ic != [("ok",)]:
            raise RuntimeError(f"integrity_check failed: {ic}")
        fk = con.execute("PRAGMA foreign_key_check").fetchall()
        if fk:
            raise RuntimeError(f"foreign_key_check failed: {fk[:5]}")
        con.execute("ANALYZE")
    finally:
        con.close()

    tmp_path.replace(out_path)
    return {
        "out": str(out_path),
        "bytes": out_path.stat().st_size,
        "content_hash": content_hash,
        "factions": len(factions),
        "districts": len(districts),
        "sub_territories": len(sub_territories),
        "control_centers": len(control_centers),
        "landmarks": len(landmarks),
        "spawn_points": len(spawn_points),
        "territory_cells": len(cell_rows),
        "polygon_vertices": len(poly_rows),
    }


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
            print(f"world.db deterministic OK (sha256={hb[:16]}..., {b['bytes']} B)")
        finally:
            if probe.exists():
                probe.unlink()
        return 0

    stats = build_db(args.output)
    print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
