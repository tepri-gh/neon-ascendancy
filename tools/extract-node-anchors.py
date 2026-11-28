#!/usr/bin/env python3
"""Node anchor candidates for the dynamic garrison, from local research extracts.

Anchors are candidates with a confidence label (vanilla, derived, generated),
not proven placements: the garrison spike and the sweep validate them in game
(docs/design/node-garrison-and-assault.md section 5). Sector AI spots come
from the mine-venues.py index and are typed by their workspot file
(spot_kind). Only guard and idle_stand spots become guard posts; sit and work
spots are boss-seat candidates.
"""
import argparse
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = Path.home() / '.cache/neon-ascendancy/extracts/venues'
OUTPUT = ROOT / 'data/territory/node_anchors.json'
ALIASES = {'loc_q303_paradise': 'loc_q304_combat_tower',
           'loc_sts_wat_kab_07': 'loc_sts_wat_kab_07_casino_bar'}
MINIMUM = {'small': 6, 'medium': 11, 'large': 21, 'very_large': 31}
MAXIMUM = {'small': 10, 'medium': 20, 'large': 30, 'very_large': 40}
POST_CAP_FACTOR = 3  # keep at most 3x the size's maximum headcount
# Workspot file words -> spot_kind, first match wins (order matters: a
# "sit_..._tablet" spot is a seat, a "stand_..._smoke" spot an idle post).
SPOT_KINDS = (
    ('civilian', ('dance', 'drink', 'eat', 'lying', 'sleep', 'beg', 'pray', 'crowd', 'shower', 'toilet', 'sex', 'stripper', 'kid', 'child')),
    ('sit', ('sit', 'bench', 'stool', 'couch', 'chair', 'sofa', 'squat')),
    ('guard', ('guard', 'patrol', 'lookout', 'aim', 'sentry', 'security', 'rifle', 'gun', 'bouncer', 'watch')),
    ('work', ('tablet', 'welder', 'weld', 'terminal', 'computer', 'inspect', 'repair', 'laptop', 'keyboard', 'desk', 'scan', 'mechanic', 'crate', 'box')),
    ('idle_stand', ('stand', 'lean', 'wall', 'smoke', 'cigarette', 'phone', 'arms_crossed', 'idle', 'wait')),
)

def read(path):
    return json.loads(path.read_text())

def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def point(pos, confidence, source):
    return {'pos': [round(float(x), 2) for x in pos], 'confidence': confidence, 'source': source}

def spot_kind(row):
    name = (Path(str(row.get('workspot') or '').replace('\\', '/')).stem or str(row.get('debug') or '')).lower()
    if not name:
        return 'unknown'
    for kind, words in SPOT_KINDS:
        if any(w in name for w in words):
            return kind
    return 'unknown'

def spread(points, start, cap):
    """Greedy farthest-point pick (floors count 3x), so the kept posts cover
    the venue's rooms and floors instead of one crowded corner."""
    if len(points) <= cap:
        return points
    def gap(a, b): return math.hypot(distance(a, b), 3 * (a[2] - b[2]))
    first = min(points, key=lambda p: gap(p['pos'], start))
    kept, rest = [first], [p for p in points if p is not first]
    best = {id(p): gap(p['pos'], first['pos']) for p in rest}
    while len(kept) < cap and rest:
        nxt = max(rest, key=lambda p: (best[id(p)], p['pos']))
        kept.append(nxt); rest.remove(nxt)
        for p in rest: best[id(p)] = min(best[id(p)], gap(p['pos'], nxt['pos']))
    return kept

def build():
    items = [x for x in read(ROOT / 'data/venues/classification.json')['items'] if x['bucket'] == 'node']
    stops = read(ROOT / 'tools/probes/tour_stops.json')['stops']
    catalogue = {x['venue']: x for x in read(CACHE / 'catalog.json')}
    hustles = {x['venue']: x for x in read(ROOT / 'data/venues/hustle_sites.json')['sites']}
    research_hustles = {x['venue']: x for x in read(CACHE / 'research/hustles/badlands_se1.json')['sites']}
    roads = read(ROOT / 'data/roads/nodes.json')
    registry = read(Path.home() / 'na-prop-scratch/world_res/base/worlds/03_night_city/_compiled/default/03_night_city.devices.json')
    devices = registry['Data']['RootChunk']['data']['Data']['unk1']
    device_by_id = {str(d.get('hash')): d for d in devices}
    doors = []
    for d in devices:
        if 'door' not in str(d.get('className', {})).lower():
            continue
        p = d.get('nodePosition', {})
        if all(k in p for k in ('X', 'Y', 'Z')):
            doors.append(([p[k] for k in ('X', 'Y', 'Z')], str(d.get('hash', ''))))
    spots = []
    for file in sorted((CACHE / 'sectors').glob('batch_*.jsonl')):
        with file.open() as f:
            for line in f:
                row = json.loads(line)
                if row.get('kind') == 'spot' and row.get('pos'):
                    spots.append(row)
    lifts = read(CACHE / 'research/lifts/lift_audit_live.json')['lifts']
    excluded = read(ROOT / 'data/venues/lift_exclusions.json')
    bad_lifts = {str(x['id']) for x in excluded['lifts']}
    bad_floors = {str(x['id']) for x in excluded['floors']}
    output = []
    for item in sorted(items, key=lambda x: x['id']):
        ident = item['id']; venue = ALIASES.get(ident, ident)
        cat = catalogue.get(venue, {})
        mine = [x for x in stops if x.get('classification_id') == ident or x.get('venue') == ident]
        if not mine and venue != ident:
            mine = [x for x in stops if x.get('venue') == venue]
        stop = mine[0] if mine else None
        # A venue with stops on several floors (Arasaka Tower: lobby, 142,
        # 388) is the union of its stop areas.
        zones = [(x['pos'], float(x['radius'])) for x in mine]
        if stop:
            center, radius = stop['pos'], float(stop['radius'])
        elif ident.startswith('hustle_'):
            h = hustles['loc_ma_' + ident[len('hustle_'):]]
            center = h.get('position')
            if not center:
                m = re.search(r'"position"\s*:\s*(\[[^\]]+\])', h.get('place', ''))
                center = json.loads(m.group(1)) if m else research_hustles.get(h['venue'], {}).get('place', {}).get('position')
            if not center:
                raise ValueError('Missing hustle position: ' + ident)
            radius = 40.0
        else:
            coords = [x['spot_pos'] for x in cat.get('communities', []) if x.get('spot_pos')]
            coords += [x['pos'] for x in cat.get('devices', []) if x.get('pos')]
            if not coords:
                raise ValueError('Missing area: ' + ident)
            center = [sum(p[i] for p in coords) / len(coords) for i in range(3)]; radius = 40.0
        zones = zones or [(center, radius)]
        def inside(p): return any(distance(p, c) <= r and abs(p[2] - c[2]) <= 35 for c, r in zones)
        communities = [x for x in cat.get('communities', []) if x.get('spot_pos') and inside(x['spot_pos'])]
        local_spots = [x for x in spots if inside(x['pos'])]
        posts = []
        for c in communities:
            name = ' '.join(str(c.get(k, '')) for k in ('entry', 'record', 'role')).lower()
            if 'guard' in name or 'security' in name:
                posts.append(point(c['spot_pos'], 'vanilla', 'community:' + str(c.get('ref')) + '/' + str(c.get('entry'))))
        for p in posts: p['spot_kind'] = 'guard'
        seats = []
        for s in local_spots:
            kind = spot_kind(s)
            pt = point(s['pos'], 'vanilla', 'sector:' + s['sector'] + '#' + s['gid'])
            pt['spot_kind'] = kind
            if kind in ('guard', 'idle_stand'):
                posts.append(pt)
            elif kind in ('sit', 'work'):
                seats.append(pt)
        unique = {}
        for p in posts: unique.setdefault(tuple(p['pos']), p)
        posts = list(unique.values())
        if not posts:
            for i in range(6):
                angle = 2 * math.pi * i / 6
                posts.append(point([center[0] + radius*.5*math.cos(angle), center[1] + radius*.5*math.sin(angle), center[2]], 'generated', 'ring'))
        ds = [(p, 'registry:' + id) for p, id in doors if inside(p)]
        ds += [(d['pos'], 'catalogue:' + str(d.get('ref'))) for d in cat.get('devices', []) if d.get('pos') and 'door' in str(d.get('controller', '')).lower() and inside(d['pos'])]
        ds.sort(key=lambda x: (-distance(x[0], center), x[1]))
        breaches = [point(p, 'derived', s) for p, s in ds[:2]]
        if not breaches:
            breaches = [point([center[0]+radius, center[1], center[2]], 'generated', 'area boundary')]
        breach = breaches[0]['pos']
        posts = spread(posts, breach, POST_CAP_FACTOR * MAXIMUM[item['size']])
        boss_candidates = [c for c in communities if any(w in (' '.join(str(c.get(k, '')) for k in ('entry','record')).lower()) for w in ('boss','lieutenant','miniboss'))]
        if boss_candidates:
            c = boss_candidates[0]; boss = point(c['spot_pos'], 'vanilla', 'community:' + str(c.get('ref')) + '/' + str(c.get('entry')))
        elif seats:
            s = max(seats, key=lambda x: (x['spot_kind'] == 'work', distance(x['pos'], breach), x['pos']))
            boss = point(s['pos'], 'derived', 'deepest ' + s['spot_kind'] + ' spot ' + s['source'])
        else:
            boss = point(max(posts, key=lambda x: distance(x['pos'], breach))['pos'], 'generated', 'farthest post')
        candidates = [r for r in roads if 35 <= distance(r[2:5], breach) <= 60 and distance(r[2:5], center) > radius]
        if candidates:
            road = min(candidates, key=lambda r: (abs(distance(r[2:5], breach)-45), r[0])); staging = point(road[2:5], 'derived', 'road:' + str(road[0]))
        else:
            dx, dy = breach[0]-center[0], breach[1]-center[1]; length = math.hypot(dx,dy) or 1
            staging = point([breach[0]+45*dx/length, breach[1]+45*dy/length, breach[2]], 'generated', 'breach direction')
        same = [p for p in posts if abs(p['pos'][2]-posts[0]['pos'][2]) <= 3]
        patrols = [{'points': [p['pos'] for p in same[:4]], 'confidence': 'generated', 'source': 'guard posts'}] if len(same) >= 2 else []
        waypoints = [point(p['pos'], 'generated', 'guard post') for p in sorted(posts, key=lambda p: distance(p['pos'], breach)+distance(p['pos'], boss['pos']))[:3]]
        links = []
        for lift in lifts:
            car_id = str(lift['id'])
            if car_id in bad_lifts or any(str(f['terminal']) in bad_lifts for f in lift.get('floors', [])):
                continue
            floors, positions = [], []
            for floor in lift.get('floors', []):
                terminal_id = str(floor['terminal'])
                pos = device_by_id.get(terminal_id, {}).get('nodePosition', {})
                if terminal_id in bad_floors or not all(k in pos for k in ('X', 'Y', 'Z')):
                    continue
                positions.append([pos[k] for k in ('X', 'Y', 'Z')])
                floors.append({'index': floor['index'], 'z': round(float(pos['Z']), 2)})
            if lift.get('pos'):
                positions.append(lift['pos'])
            if len(floors) < 2 or not any(distance(p, center) <= radius for p in positions):
                continue
            floors.sort(key=lambda f: f['index'])
            ground = min(floors, key=lambda f: (abs(f['z'] - breach[2]), f['index']))
            target = min(floors, key=lambda f: (abs(f['z'] - boss['pos'][2]), f['index']))
            links.append({'id': car_id, 'floors': floors, 'ground_floor_idx': ground['index'],
                          'target_floor_idx': target['index'], 'cab_capacity': 4,
                          'confidence': 'derived', 'source': 'lift audit and device registry'})
        links.sort(key=lambda link: link['id'])
        slots = len(posts) + len(patrols)
        deficit = max(0, MINIMUM[item['size']] - slots)
        output.append({'id': ident, 'catalogue_venue': venue, 'area': {'pos': [round(x,2) for x in center], 'radius': radius}, 'guard_posts': posts, 'boss_seat': boss, 'patrol_splines': patrols, 'breach_points': breaches, 'staging': staging, 'interior_waypoints': waypoints, 'lift_links': links, 'capacity': {'slots': slots, 'minimum': MINIMUM[item['size']], 'capacity_ok': deficit == 0, 'deficit': deficit}})
    return {'generated_by': 'tools/extract-node-anchors.py', 'nodes': output}

def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--check', action='store_true'); args = parser.parse_args()
    data = build()
    compact = lambda value: json.dumps(value, separators=(',', ':'), ensure_ascii=False)
    result = ('{"generated_by":' + compact(data['generated_by']) + ',\n"nodes":[\n'
              + ',\n'.join(compact(node) for node in data['nodes']) + '\n]}\n')
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text() != result:
            raise SystemExit('node anchors are out of date')
        print('node anchors are up to date')
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True); OUTPUT.write_text(result); print('wrote', OUTPUT)

if __name__ == '__main__': main()
