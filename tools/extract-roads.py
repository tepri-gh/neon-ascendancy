#!/usr/bin/env python3
"""Extract deterministic drivable road graph seeds (data/roads/*.json) from CP2077 2.5 EP1 traffic data.

Sources (unbundled + converted via WolvenKit CLI from archive/pc/ep1 + content):
  base/worlds/03_night_city/sectors/_generated/traffic/
    - all.traffic_persistent.json   (33,953 worldTrafficLanePersistent records)
    - all.lane_polygons.json        (3D centerline outlines per lane index)
    - all.lane_connections.json     (inLanes / outlanes with exact exit/entry positions)

Filtering & topology rules (verified against RED4ext TrafficLanePersistentFlags):
  1. Select vehicle road lanes: (flags & 0x0010 [Road]) != 0 and subGraphId == 357
     (unified Night City + Badlands + Dogtown + Morro Rock vehicle network).
     Note: NoAIDriving (0x2000) lanes are retained because the Dogtown gate and
     compound driveways carry it; removing them severs Dogtown from Night City.
  2. Split every lane at exact thisLaneExitPosition / nextLaneEntryPosition points,
     simplify curved polylines with 3D Douglas-Peucker (eps = 1.5 m), and subdivide
     straight spans > 160 m so every edge stays bounded within 200 m road chunks.
  3. Weld contiguous lane endpoints within 0.25 m (preventing intra-lane collapse),
     add directed intersection connectors, same-direction neighborGroup lane-change
     edges, and 2-way dead-end turnaround edges.
  4. Prune the final directed node-edge graph to its largest strongly connected
     component (Tarjan SCC) so every node can reach every other node with zero
     dead-end traps.
  5. Partition nodes into deterministic 200 m x 200 m x 50 m road chunks mapped to
     data/districts.json and emit compact Git-tracked seeds under data/roads/.
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
ROADS_DIR = DATA_DIR / "roads"
DISTRICTS_PATH = DATA_DIR / "districts.json"
DEFAULT_CACHE_DIR = Path.home() / ".cache" / "neon-ascendancy" / "extracts" / "roads"
TRAFFIC_REL = Path("base/worlds/03_night_city/sectors/_generated/traffic")

# RED4ext world::TrafficLanePersistentFlags
FLAG_ROAD = 0x0010
FLAG_HIGHWAY = 0x4000
MAIN_VEHICLE_SUBGRAPH = 357

# Geometry / chunk constants
SPLIT_SNAP_M = 1.0
DP_EPSILON_M = 1.5
MAX_SEG_LEN_M = 160.0
WELD_DIST_M = 0.25
WELD_MAX_DRIFT_M = 0.50
CHUNK_XY_M = 200.0
CHUNK_Z_M = 50.0
TUNNEL_CELL_M = 10.0
TUNNEL_OVERHEAD_M = 6.0
TUNNEL_BELOW_Z_M = -1.0


def dist3(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)


def sample_point_at_s(
    outline: list[tuple[float, float, float]],
    accum: list[float],
    s: float,
) -> tuple[float, float, float]:
    """Interpolate a 3D point along a lane outline at arc length s."""
    if not outline:
        return (0.0, 0.0, 0.0)
    if s <= 0.0 or not accum:
        return outline[0]
    if s >= accum[-1]:
        return outline[-1]
    prev_s = 0.0
    for k, al in enumerate(accum):
        if s <= al and k + 1 < len(outline):
            seg = al - prev_s
            t = (s - prev_s) / seg if seg > 1e-6 else 0.0
            a = outline[k]
            b = outline[k + 1]
            return (
                a[0] + t * (b[0] - a[0]),
                a[1] + t * (b[1] - a[1]),
                a[2] + t * (b[2] - a[2]),
            )
        prev_s = al
    return outline[-1]


def extract_sub_polyline(
    outline: list[tuple[float, float, float]],
    accum: list[float],
    s0: float,
    s1: float,
) -> list[tuple[float, float, float]]:
    """Extract exact 3D polyline points between arc lengths s0 and s1 (s0 < s1)."""
    pts: list[tuple[float, float, float]] = [sample_point_at_s(outline, accum, s0)]
    for k, al in enumerate(accum):
        if s0 + 1e-3 < al < s1 - 1e-3 and k + 1 < len(outline):
            pts.append(outline[k + 1])
    pts.append(sample_point_at_s(outline, accum, s1))
    return pts


def dp_simplify_3d(
    pts: list[tuple[float, float, float]],
    eps: float,
) -> list[tuple[float, float, float]]:
    """3D Douglas-Peucker polyline simplification keeping endpoints."""
    if len(pts) <= 2:
        return pts
    keep = {0, len(pts) - 1}
    stack = [(0, len(pts) - 1)]
    eps2 = eps * eps
    while stack:
        a, b = stack.pop()
        if b <= a + 1:
            continue
        ax, ay, az = pts[a]
        bx, by, bz = pts[b]
        dx, dy, dz = bx - ax, by - ay, bz - az
        l2 = dx * dx + dy * dy + dz * dz
        max_d2 = -1.0
        max_k = -1
        for k in range(a + 1, b):
            px, py, pz = pts[k]
            if l2 < 1e-9:
                d2 = (px - ax) ** 2 + (py - ay) ** 2 + (pz - az) ** 2
            else:
                t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy + (pz - az) * dz) / l2))
                qx, qy, qz = ax + t * dx, ay + t * dy, az + t * dz
                d2 = (px - qx) ** 2 + (py - qy) ** 2 + (pz - qz) ** 2
            if d2 > max_d2:
                max_d2 = d2
                max_k = k
        if max_d2 > eps2:
            keep.add(max_k)
            stack.append((a, max_k))
            stack.append((max_k, b))
    return [pts[i] for i in sorted(keep)]


def subdivide_long_segments(
    pts: list[tuple[float, float, float]],
    max_len: float,
) -> list[tuple[float, float, float]]:
    """Subdivide any segment longer than max_len into equal spans."""
    out = [pts[0]]
    for i in range(len(pts) - 1):
        a = pts[i]
        b = pts[i + 1]
        d = dist3(a, b)
        if d > max_len:
            steps = int(math.ceil(d / max_len))
            for k in range(1, steps):
                t = k / steps
                out.append((
                    a[0] + t * (b[0] - a[0]),
                    a[1] + t * (b[1] - a[1]),
                    a[2] + t * (b[2] - a[2]),
                ))
        out.append(b)
    return out


def unit_xy(a: tuple[float, float, float], b: tuple[float, float, float]) -> tuple[float, float]:
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    if n < 1e-6:
        return (0.0, 0.0)
    return (dx / n, dy / n)


def tarjan_largest_scc(
    node_ids: list[int],
    adj: dict[int, list[int]],
) -> set[int]:
    """Iterative Tarjan strongly connected components; returns the largest SCC."""
    index = 0
    stack: list[int] = []
    on_stack: set[int] = set()
    indices: dict[int, int] = {}
    lowlink: dict[int, int] = {}
    best_scc: list[int] = []

    for start in node_ids:
        if start in indices:
            continue
        call_stack: list[tuple[int, int]] = [(start, 0)]
        indices[start] = lowlink[start] = index
        index += 1
        stack.append(start)
        on_stack.add(start)

        while call_stack:
            v, ei = call_stack[-1]
            nbrs = adj.get(v, ())
            if ei < len(nbrs):
                call_stack[-1] = (v, ei + 1)
                w = nbrs[ei]
                if w not in indices:
                    indices[w] = lowlink[w] = index
                    index += 1
                    stack.append(w)
                    on_stack.add(w)
                    call_stack.append((w, 0))
                elif w in on_stack:
                    if indices[w] < lowlink[v]:
                        lowlink[v] = indices[w]
            else:
                call_stack.pop()
                if call_stack:
                    parent = call_stack[-1][0]
                    if lowlink[v] < lowlink[parent]:
                        lowlink[parent] = lowlink[v]
                if lowlink[v] == indices[v]:
                    scc: list[int] = []
                    while True:
                        w = stack.pop()
                        on_stack.remove(w)
                        scc.append(w)
                        if w == v:
                            break
                    if len(scc) > len(best_scc):
                        best_scc = scc

    return set(best_scc)


def resolve_district_id(x: float, y: float, districts: list[dict[str, Any]]) -> int:
    """Map (x, y) to the most specific district whose bbox contains it."""
    non_badlands: list[tuple[float, int]] = []
    badlands_id: int | None = None
    for d in districts:
        did = d["district_id"]
        if d["kind"] == "badlands":
            badlands_id = did
        if d["bbox_min_x"] <= x <= d["bbox_max_x"] and d["bbox_min_y"] <= y <= d["bbox_max_y"]:
            if d["kind"] != "badlands":
                area = (d["bbox_max_x"] - d["bbox_min_x"]) * (d["bbox_max_y"] - d["bbox_min_y"])
                non_badlands.append((area, did))
    if non_badlands:
        non_badlands.sort()
        return non_badlands[0][1]
    if badlands_id is not None:
        return badlands_id
    # Fallback: nearest district bbox center.
    best_id = districts[0]["district_id"]
    best_d2 = float("inf")
    for d in districts:
        cx = 0.5 * (d["bbox_min_x"] + d["bbox_max_x"])
        cy = 0.5 * (d["bbox_min_y"] + d["bbox_max_y"])
        d2 = (x - cx) ** 2 + (y - cy) ** 2
        if d2 < best_d2:
            best_d2 = d2
            best_id = d["district_id"]
    return best_id


def maybe_extract_from_game(cache_dir: Path, game_dir: Path, wolvenkit_cli: Path) -> None:
    """Unbundle and CR2W-convert the traffic files if requested."""
    traffic_dir = cache_dir / TRAFFIC_REL
    needed = [
        traffic_dir / "all.traffic_persistent.json",
        traffic_dir / "all.lane_polygons.json",
        traffic_dir / "all.lane_connections.json",
    ]
    if all(p.is_file() for p in needed):
        return
    cache_dir.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env["DOTNET_ROLL_FORWARD"] = "Major"
    # Extract base content first, then EP1 overrides so Dogtown lanes win.
    for sub in ("archive/pc/content", "archive/pc/ep1"):
        src = game_dir / sub
        if not src.is_dir():
            continue
        cmd = [
            str(wolvenkit_cli),
            "unbundle",
            "-p",
            str(src),
            "-o",
            str(cache_dir),
            "-r",
            r"sectors\\_generated\\traffic\\all\.(traffic_persistent|lane_polygons|lane_connections)$",
        ]
        subprocess.run(cmd, env=env, check=True)
    for stem in ("all.traffic_persistent", "all.lane_polygons", "all.lane_connections"):
        raw = traffic_dir / stem
        if not raw.is_file():
            raise FileNotFoundError(f"Missing unbundled traffic file: {raw}")
        subprocess.run(
            [str(wolvenkit_cli), "cr2w", "-s", "-p", str(raw), "-o", str(traffic_dir)],
            env=env,
            check=True,
        )


def build_road_graph(cache_dir: Path) -> dict[str, Any]:
    traffic_dir = cache_dir / TRAFFIC_REL
    tp_path = traffic_dir / "all.traffic_persistent.json"
    lp_path = traffic_dir / "all.lane_polygons.json"
    lc_path = traffic_dir / "all.lane_connections.json"
    for p in (tp_path, lp_path, lc_path):
        if not p.is_file():
            raise FileNotFoundError(
                f"Missing extracted traffic JSON: {p}\n"
                f"Run with --extract or unbundle traffic files into {cache_dir}."
            )

    districts = json.loads(DISTRICTS_PATH.read_text(encoding="utf-8"))
    tp = json.loads(tp_path.read_text(encoding="utf-8"))
    lp = json.loads(lp_path.read_text(encoding="utf-8"))
    lc = json.loads(lc_path.read_text(encoding="utf-8"))

    lanes = tp["Data"]["RootChunk"]["data"]["lanes"]
    polys_raw = {item["index"]: item["value"] for item in lp["Data"]["RootChunk"]["data"]}
    conns_raw = {item["index"]: item["value"] for item in lc["Data"]["RootChunk"]["data"]}

    # 1. Select unified drivable vehicle road lanes (Road flag + main vehicle subGraph 357).
    selected: list[int] = []
    outlines: dict[int, list[tuple[float, float, float]]] = {}
    accums: dict[int, list[float]] = {}
    lengths: dict[int, float] = {}
    speeds_kph: dict[int, float] = {}

    for i, lane in enumerate(lanes):
        if (lane.get("flags", 0) & FLAG_ROAD) == 0:
            continue
        if lane.get("subGraphId") != MAIN_VEHICLE_SUBGRAPH:
            continue
        raw_ol = polys_raw.get(i, {}).get("outline", [])
        if len(raw_ol) < 2:
            continue
        ol = [(float(p["X"]), float(p["Y"]), float(p["Z"])) for p in raw_ol]
        al = [float(v) for v in lane.get("accumulatedLengths", [])]
        lane_len = float(lane.get("length", 0.0))
        if len(al) != len(ol) - 1 or lane_len <= 0.1:
            continue
        selected.append(i)
        outlines[i] = ol
        accums[i] = al
        lengths[i] = lane_len
        max_mps = float(lane.get("maxSpeed", 10) or 10)
        speeds_kph[i] = round(max(max_mps * 3.6, 15.0), 1)

    selected_set = set(selected)

    # Precompute 10 m XY maximum road height grid for tunnel/underpass detection.
    cell_max_z: dict[tuple[int, int], float] = {}
    for i in selected:
        for x, y, z in outlines[i]:
            key = (math.floor(x / TUNNEL_CELL_M), math.floor(y / TUNNEL_CELL_M))
            prev = cell_max_z.get(key)
            if prev is None or z > prev:
                cell_max_z[key] = z

    def is_tunnel_segment(a: tuple[float, float, float], b: tuple[float, float, float]) -> int:
        mx = 0.5 * (a[0] + b[0])
        my = 0.5 * (a[1] + b[1])
        mz = 0.5 * (a[2] + b[2])
        if mz < TUNNEL_BELOW_Z_M:
            return 1
        key = (math.floor(mx / TUNNEL_CELL_M), math.floor(my / TUNNEL_CELL_M))
        top_z = cell_max_z.get(key, mz)
        return 1 if (top_z - mz) >= TUNNEL_OVERHEAD_M else 0

    # 2. Collect exact split positions per lane from outlanes connections.
    split_sets: dict[int, list[float]] = {i: [0.0, lengths[i]] for i in selected}
    valid_outlanes: dict[int, list[tuple[int, float, float]]] = {i: [] for i in selected}
    for u in selected:
        lu = lengths[u]
        for c in conns_raw.get(u, {}).get("outlanes", []):
            v = int(c["laneIndex"])
            if v not in selected_set or v == u:
                continue
            lv = lengths[v]
            s_exit = max(0.0, min(lu, float(c.get("thisLaneExitPosition", lu))))
            s_entry = max(0.0, min(lv, float(c.get("nextLaneEntryPosition", 0.0))))
            if s_exit <= SPLIT_SNAP_M:
                s_exit = 0.0
            elif lu - s_exit <= SPLIT_SNAP_M:
                s_exit = lu
            if s_entry <= SPLIT_SNAP_M:
                s_entry = 0.0
            elif lv - s_entry <= SPLIT_SNAP_M:
                s_entry = lv
            split_sets[u].append(s_exit)
            split_sets[v].append(s_entry)
            valid_outlanes[u].append((v, s_exit, s_entry))

    # Merge nearby split positions per lane.
    lane_splits: dict[int, list[float]] = {}
    for u in selected:
        raw_s = sorted(split_sets[u])
        merged = [0.0]
        for s in raw_s[1:-1]:
            if s - merged[-1] >= SPLIT_SNAP_M and lengths[u] - s >= SPLIT_SNAP_M:
                merged.append(s)
        merged.append(lengths[u])
        lane_splits[u] = merged

    def nearest_split_idx(u: int, s: float) -> int:
        splits = lane_splits[u]
        best_k = 0
        best_d = abs(splits[0] - s)
        for k in range(1, len(splits)):
            d = abs(splits[k] - s)
            if d < best_d:
                best_d = d
                best_k = k
        return best_k

    # 3. Build raw nodes & along-lane edges.
    raw_pos: list[tuple[float, float, float]] = []
    raw_lane: list[int] = []
    lane_split_node: dict[tuple[int, int], int] = {}
    lane_chain_nodes: dict[int, list[int]] = {}
    raw_edges: list[tuple[int, int, float, float, int]] = []  # (u, v, length_m, speed_kph, is_tunnel)

    def add_raw_node(pos: tuple[float, float, float], lane_idx: int) -> int:
        nid = len(raw_pos)
        raw_pos.append(pos)
        raw_lane.append(lane_idx)
        return nid

    for u in selected:
        ol = outlines[u]
        al = accums[u]
        splits = lane_splits[u]
        sp_kph = speeds_kph[u]
        chain: list[int] = []

        start_pt = sample_point_at_s(ol, al, splits[0])
        prev_nid = add_raw_node(start_pt, u)
        lane_split_node[(u, 0)] = prev_nid
        chain.append(prev_nid)

        for k in range(len(splits) - 1):
            sub = extract_sub_polyline(ol, al, splits[k], splits[k + 1])
            simp = dp_simplify_3d(sub, DP_EPSILON_M)
            pts = subdivide_long_segments(simp, MAX_SEG_LEN_M)
            for idx_p in range(1, len(pts)):
                cur_nid = add_raw_node(pts[idx_p], u)
                seg_len = max(0.05, dist3(raw_pos[prev_nid], raw_pos[cur_nid]))
                tun = is_tunnel_segment(raw_pos[prev_nid], raw_pos[cur_nid])
                raw_edges.append((prev_nid, cur_nid, seg_len, sp_kph, tun))
                chain.append(cur_nid)
                prev_nid = cur_nid
            lane_split_node[(u, k + 1)] = prev_nid

        lane_chain_nodes[u] = chain

    # 4. Outlane connectors + endpoint welding (Union-Find).
    parent = list(range(len(raw_pos)))

    def uf_find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def uf_union(a: int, b: int) -> bool:
        ra, rb = uf_find(a), uf_find(b)
        if ra == rb:
            return True
        if dist3(raw_pos[ra], raw_pos[rb]) > WELD_MAX_DRIFT_M:
            return False
        if ra < rb:
            parent[rb] = ra
        else:
            parent[ra] = rb
        return True

    for u in selected:
        for v, s_exit, s_entry in valid_outlanes[u]:
            na = lane_split_node[(u, nearest_split_idx(u, s_exit))]
            nb = lane_split_node[(v, nearest_split_idx(v, s_entry))]
            d = dist3(raw_pos[na], raw_pos[nb])
            if d < WELD_DIST_M and uf_union(na, nb):
                continue
            conn_len = max(0.25, d)
            conn_sp = min(speeds_kph[u], speeds_kph[v])
            tun = is_tunnel_segment(raw_pos[na], raw_pos[nb])
            raw_edges.append((na, nb, conn_len, conn_sp, tun))

    # 5. Same-direction neighborGroup lane-change edges + 2-way dead-end turnarounds.
    ng_groups: dict[int, list[int]] = collections.defaultdict(list)
    for u in selected:
        ngi = int(lanes[u].get("neighborGroupIndex", 65535))
        if ngi != 65535:
            ng_groups[ngi].append(u)

    lane_dir: dict[int, tuple[float, float]] = {
        u: unit_xy(outlines[u][0], outlines[u][-1]) for u in selected
    }
    lane_change_count = 0
    uturn_count = 0

    for ngi in sorted(ng_groups):
        members = ng_groups[ngi]
        if len(members) < 2:
            continue
        for a in members:
            da = lane_dir[a]
            if da == (0.0, 0.0):
                continue
            nodes_a = lane_chain_nodes[a]
            # Pick up to 2 departure points on lane a (start + middle if multi-segment).
            dep_indices = [0]
            if len(nodes_a) >= 3:
                dep_indices.append(len(nodes_a) // 2)
            for b in members:
                if a == b:
                    continue
                db = lane_dir[b]
                if db == (0.0, 0.0):
                    continue
                dot = da[0] * db[0] + da[1] * db[1]
                nodes_b = lane_chain_nodes[b]
                if dot > 0.7:
                    # Same-direction parallel lane change.
                    for di in dep_indices:
                        na = nodes_a[di]
                        pa = raw_pos[na]
                        best_nb = -1
                        best_d = 35.0
                        for nb in nodes_b:
                            pb = raw_pos[nb]
                            dz = abs(pb[2] - pa[2])
                            if dz > 3.5:
                                continue
                            fwd = (pb[0] - pa[0]) * da[0] + (pb[1] - pa[1]) * da[1]
                            if fwd < 1.5:
                                continue
                            lat = abs((pb[0] - pa[0]) * (-da[1]) + (pb[1] - pa[1]) * da[0])
                            if lat > 12.0:
                                continue
                            d = dist3(pa, pb)
                            if 1.0 <= d < best_d:
                                best_d = d
                                best_nb = nb
                        if best_nb >= 0:
                            lc_sp = round(max(15.0, min(speeds_kph[a], speeds_kph[b]) * 0.75), 1)
                            tun = is_tunnel_segment(raw_pos[na], raw_pos[best_nb])
                            raw_edges.append((na, best_nb, best_d, lc_sp, tun))
                            lane_change_count += 1
                elif dot < -0.5 and not valid_outlanes[a]:
                    # 2-way dead-end turnaround at the end of a cul-de-sac / compound road.
                    na = nodes_a[-1]
                    nb = nodes_b[0]
                    d = dist3(raw_pos[na], raw_pos[nb])
                    if d <= 18.0:
                        tun = is_tunnel_segment(raw_pos[na], raw_pos[nb])
                        raw_edges.append((na, nb, max(2.0, d), 15.0, tun))
                        uturn_count += 1

    # 6. Collapse welded nodes and deduplicate edges keeping fastest travel time.
    best_edge: dict[tuple[int, int], tuple[float, float, int]] = {}
    for u, v, length_m, sp_kph, tun in raw_edges:
        ru = uf_find(u)
        rv = uf_find(v)
        if ru == rv:
            continue
        cost = length_m / max(sp_kph, 1.0)
        prev = best_edge.get((ru, rv))
        if prev is None or cost < (prev[0] / max(prev[1], 1.0)):
            best_edge[(ru, rv)] = (length_m, sp_kph, tun)

    adj: dict[int, list[int]] = collections.defaultdict(list)
    active_roots: set[int] = set()
    for (ru, rv) in sorted(best_edge):
        adj[ru].append(rv)
        active_roots.add(ru)
        active_roots.add(rv)

    # 7. Prune to the largest strongly connected component of the final node-edge graph.
    scc_roots = tarjan_largest_scc(sorted(active_roots), adj)
    if not scc_roots:
        raise RuntimeError("Largest road SCC is empty")

    # 8. Build deterministic 3D road chunks (200 m x 200 m x 50 m).
    chunk_nodes: dict[tuple[int, int, int], list[int]] = collections.defaultdict(list)
    chunk_lanes: dict[tuple[int, int, int], set[int]] = collections.defaultdict(set)
    for r in scc_roots:
        x, y, z = raw_pos[r]
        gk = (
            math.floor(x / CHUNK_XY_M),
            math.floor(y / CHUNK_XY_M),
            math.floor(z / CHUNK_Z_M),
        )
        chunk_nodes[gk].append(r)
        chunk_lanes[gk].add(raw_lane[r])

    chunk_keys = sorted(chunk_nodes)
    chunk_id_by_key: dict[tuple[int, int, int], int] = {}
    chunks_out: list[dict[str, Any]] = []
    district_counts: collections.Counter[int] = collections.Counter()

    for idx_c, gk in enumerate(chunk_keys, start=1):
        chunk_id_by_key[gk] = idx_c
        roots_in_chunk = chunk_nodes[gk]
        xs = [raw_pos[r][0] for r in roots_in_chunk]
        ys = [raw_pos[r][1] for r in roots_in_chunk]
        cx = sum(xs) / len(xs)
        cy = sum(ys) / len(ys)
        did = resolve_district_id(cx, cy, districts)
        district_counts[did] += 1
        chunks_out.append({
            "chunk_id": idx_c,
            "district_id": did,
            "grid_x": gk[0],
            "grid_y": gk[1],
            "grid_z": gk[2],
            "lane_count": len(chunk_lanes[gk]),
            "navmesh_ready": 1,
            "min_x": round(min(xs), 2),
            "max_x": round(max(xs), 2),
            "min_y": round(min(ys), 2),
            "max_y": round(max(ys), 2),
        })

    # 9. Assign deterministic node_ids and edge_ids.
    def node_sort_key(r: int) -> tuple[int, float, float, float, int]:
        x, y, z = raw_pos[r]
        gk = (
            math.floor(x / CHUNK_XY_M),
            math.floor(y / CHUNK_XY_M),
            math.floor(z / CHUNK_Z_M),
        )
        return (chunk_id_by_key[gk], round(x, 2), round(y, 2), round(z, 2), raw_lane[r])

    sorted_roots = sorted(scc_roots, key=node_sort_key)
    node_id_by_root: dict[int, int] = {}
    node_chunk_by_id: dict[int, int] = {}
    nodes_out: list[list[Any]] = []

    for nid, r in enumerate(sorted_roots, start=1):
        node_id_by_root[r] = nid
        x, y, z = raw_pos[r]
        gk = (
            math.floor(x / CHUNK_XY_M),
            math.floor(y / CHUNK_XY_M),
            math.floor(z / CHUNK_Z_M),
        )
        cid = chunk_id_by_key[gk]
        node_chunk_by_id[nid] = cid
        nodes_out.append([nid, cid, round(x, 2), round(y, 2), round(z, 2), raw_lane[r]])

    edges_tmp: list[tuple[int, int, int, float, float, int]] = []
    tunnel_edges = 0
    total_length_m = 0.0
    for (ru, rv), (length_m, sp_kph, tun) in best_edge.items():
        if ru not in node_id_by_root or rv not in node_id_by_root:
            continue
        nu = node_id_by_root[ru]
        nv = node_id_by_root[rv]
        cid = node_chunk_by_id[nu]
        len_r = round(max(0.05, length_m), 2)
        edges_tmp.append((nu, nv, cid, len_r, round(sp_kph, 1), tun))
        if tun:
            tunnel_edges += 1
        total_length_m += len_r

    edges_tmp.sort(key=lambda e: (e[0], e[1]))
    edges_out: list[list[Any]] = [
        [eid, nu, nv, cid, len_r, sp_kph, tun]
        for eid, (nu, nv, cid, len_r, sp_kph, tun) in enumerate(edges_tmp, start=1)
    ]

    xs_all = [n[2] for n in nodes_out]
    ys_all = [n[3] for n in nodes_out]
    zs_all = [n[4] for n in nodes_out]
    dist_name_by_id = {d["district_id"]: d["code"] for d in districts}

    meta = {
        "generator": "tools/extract-roads.py",
        "game_version": "2.5",
        "source_traffic_rel": str(TRAFFIC_REL),
        "chunk_xy_m": CHUNK_XY_M,
        "chunk_z_m": CHUNK_Z_M,
        "dp_epsilon_m": DP_EPSILON_M,
        "max_seg_len_m": MAX_SEG_LEN_M,
        "raw_total_lanes": len(lanes),
        "selected_vehicle_lanes": len(selected),
        "lane_change_edges_added": lane_change_count,
        "dead_end_uturn_edges_added": uturn_count,
        "strongly_connected": True,
        "chunk_count": len(chunks_out),
        "node_count": len(nodes_out),
        "edge_count": len(edges_out),
        "tunnel_edge_count": tunnel_edges,
        "total_directed_lane_km": round(total_length_m / 1000.0, 2),
        "bbox": {
            "min_x": min(xs_all),
            "max_x": max(xs_all),
            "min_y": min(ys_all),
            "max_y": max(ys_all),
            "min_z": min(zs_all),
            "max_z": max(zs_all),
        },
        "chunks_by_district": {
            dist_name_by_id[did]: cnt
            for did, cnt in sorted(district_counts.items())
        },
        "formats": {
            "nodes": ["node_id", "chunk_id", "x", "y", "z", "lane"],
            "edges": ["edge_id", "from_node_id", "to_node_id", "chunk_id", "length_m", "speed_kph", "is_tunnel"],
        },
    }

    return {
        "chunks": chunks_out,
        "nodes": nodes_out,
        "edges": edges_out,
        "meta": meta,
    }


def write_seeds(out_dir: Path, graph: dict[str, Any]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "meta.json").write_text(
        json.dumps(graph["meta"], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (out_dir / "chunks.json").write_text(
        json.dumps(graph["chunks"], separators=(",", ":"), sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (out_dir / "nodes.json").write_text(
        "[\n"
        + ",\n".join(json.dumps(row, separators=(",", ":")) for row in graph["nodes"])
        + "\n]\n",
        encoding="utf-8",
    )
    (out_dir / "edges.json").write_text(
        "[\n"
        + ",\n".join(json.dumps(row, separators=(",", ":")) for row in graph["edges"])
        + "\n]\n",
        encoding="utf-8",
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract Night City + Badlands + Dogtown road graph seeds.")
    ap.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE_DIR)
    ap.add_argument("--out-dir", type=Path, default=ROADS_DIR)
    ap.add_argument("--extract", action="store_true", help="Unbundle & convert traffic files via WolvenKit CLI first.")
    ap.add_argument(
        "--game-dir",
        type=Path,
        default=Path("/mnt/games/SteamLibrary/steamapps/common/Cyberpunk 2077"),
    )
    ap.add_argument(
        "--wolvenkit-cli",
        type=Path,
        default=Path.home() / ".cache/neon-ascendancy/wolvenkit-10.0.0-beta.1/WolvenKit.CLI",
    )
    args = ap.parse_args()

    if args.extract:
        maybe_extract_from_game(args.cache_dir, args.game_dir, args.wolvenkit_cli)

    graph = build_road_graph(args.cache_dir)
    write_seeds(args.out_dir, graph)

    sizes = {
        name: (args.out_dir / name).stat().st_size
        for name in ("meta.json", "chunks.json", "nodes.json", "edges.json")
    }
    summary = dict(graph["meta"])
    summary["seed_bytes"] = sizes
    summary["total_seed_mb"] = round(sum(sizes.values()) / (1024 * 1024), 2)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
