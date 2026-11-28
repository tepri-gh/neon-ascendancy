#!/usr/bin/env python3
"""Check CET tour JSONL against venue policy. Outputs only violations."""
import argparse
import importlib.util
import json
import math
import shlex
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path.home() / '.cache/neon-ascendancy/extracts/venues'
PROBE = Path.home() / 'Games/Cyberpunk 2077/bin/x64/plugins/cyber_engine_tweaks/mods/NeonAscendancyProbe'

def load(path):
    return json.loads(path.read_text())

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--log', type=Path, default=PROBE / 'tour.log')
    ap.add_argument('--out-dir', type=Path, default=CACHE)
    ap.add_argument('--catalog', type=Path, default=CACHE / 'catalog.json')
    ap.add_argument('--since', default='')
    a = ap.parse_args()
    rules = load(ROOT / 'data/venues/sweep_rules.json')
    stops = {s['code']: s for s in load(ROOT / 'tools/probes/tour_stops.json')['stops']}
    classes = {x['id']: x for x in load(ROOT / 'data/venues/classification.json')['items']}
    catalog = {x['venue']: x for x in load(a.catalog)}
    exclusions = load(ROOT / 'data/venues/lift_exclusions.json')
    excluded_ids = {str(x['id']) for k in ('lifts', 'floors') for x in exclusions.get(k, [])}
    spec = importlib.util.spec_from_file_location('tour_report', ROOT / 'tools/venue-tour-report.py')
    report = importlib.util.module_from_spec(spec); spec.loader.exec_module(report)
    decisions = report.door_decisions(a.since)
    rows = []
    for line_no, line in enumerate(a.log.read_text(encoding='utf-8', errors='replace').splitlines(), 1):
        try: row = json.loads(line)
        except json.JSONDecodeError: continue
        if row.get('time', '') >= a.since: rows.append((line_no, row))
    latest, pending, failures = {}, {}, []
    for line_no, row in rows:
        code, event = row.get('code'), row.get('event')
        if event == 'visit' and row.get('mode') == 'sweep':
            if code in pending: failures.append(('hang', code, pending[code]))
            pending[code] = {'line': line_no, 'time': row.get('time')}
        elif event == 'stop' and code:
            latest[code] = row
            if row.get('mode') == 'sweep': pending.pop(code, None)
        elif event in ('skip', 'not_arrived') and row.get('reason', 'not arrived') == 'not arrived':
            failures.append(('arrival', code, {'line': line_no, **row}))
            if row.get('mode') == 'sweep': pending.pop(code, None)
        elif event == 'abort' and row.get('mode') == 'sweep': pending.pop(code, None)
    failures.extend(('hang', code, evidence) for code, evidence in pending.items())
    violations = []
    def add(kind, code, evidence, route):
        s = stops.get(code, {}); venue = s.get('venue') or latest.get(code, {}).get('venue')
        violations.append({'class':kind, 'stop':code, 'venue':venue, 'evidence':evidence, 'route':route})
    for kind, code, evidence in failures: add(kind, code, evidence, 'owner look in play')
    for code, s in latest.items():
        stop = stops.get(code, {}); venue = s.get('venue') or stop.get('venue'); cls = classes.get(stop.get('classification_id', venue), {}); bucket = cls.get('bucket', stop.get('bucket'))
        cat = catalog.get(venue, {}); options = cat.get('community_options', [])
        def community(record):
            return [{'path':o.get('path'), 'entry':o.get('entry'), 'phase':o.get('phase')} for o in options if o.get('record') == record]
        def venue_route(record): return {'tool':'venue data', 'community':community(record)}
        player, target = s.get('player'), stop.get('pos')
        if player and target:
            horizontal = math.hypot(player[0]-target[0], player[1]-target[1]); dz = player[2]-target[2]
            floor = [x['pos'][2] for x in (s.get('npcs') or []) + (s.get('devices') or []) if x.get('pos')]
            fell = bool(floor) and dz < -rules['arrival']['fell_below_target_m'] and player[2] < min(floor)-rules['arrival']['fell_below_floor_m']
            if fell or horizontal > rules['arrival']['far_horizontal_m']:
                add('arrival', code, {'player':player,'target':target,'dx_horizontal':horizontal,'dz':dz,'fell':fell}, 'owner look in play'); continue
        npcs = s.get('npcs') or []
        for n in npcs:
            record = n.get('record', '')
            if n.get('dead'): add('dead_npc', code, n, 'owner look in play')
            elif bucket != 'excluded' and (n.get('state') in rules['alert_states'] or 'Hostile' in str(n.get('attitude'))): add('hostile_alert', code, n, venue_route(record))
            low = record.lower()
            allowed = any(x['stop'] == code and x['record'].lower() == low for x in rules['robot_allowlist'])
            if bucket == 'node' and not allowed and any(x in low for x in rules['robot_record_patterns']) and not any(x in low for x in rules['robot_exclude_patterns']): add('robot', code, n, 'owner look in play')
        for obj in s.get('quest_objects') or []:
            ident = str(obj.get('id','')).removesuffix('ULL')
            cmd = shlex.join(['tools/world-deletions.py','add',ident,'--venue',str(venue),'--why',f'Quest object or corpse at {code}'])
            add('quest_object' if obj.get('quest') else 'corpse', code, obj, cmd)
        # Expected records include time-of-day and dynamic entries, so one absent
        # record is noise; flag the stop when most of them are missing.
        missing = s.get('missing_records') or []
        expected = len((stops.get(code) or {}).get('expected_records') or []) or len(missing)
        mr = rules['missing_records']
        if len(missing) >= mr['min_count'] and len(missing) >= mr['min_share'] * expected:
            add('missing_records', code, {'missing': len(missing), 'expected': expected, 'records': missing},
                [venue_route(r) for r in missing])
        civilian_records = {o.get('record') for o in options if o.get('role') == 'civilian'}
        if bucket in ('node','civilian_venue') and civilian_records and not any(not n.get('dead') and (n.get('record') in civilian_records or n.get('affiliation') in rules['civilian_affiliations']) for n in npcs): add('empty_public', code, {'expected_civilian_records':sorted(x for x in civilian_records if x)}, 'owner look in play')
        for d in s.get('devices') or []:
            ident = str(d.get('id','')).removesuffix('ULL'); kind = d.get('kind')
            if kind in ('LiftDevice','ElevatorFloorTerminal') and ident not in excluded_ids and d.get('on') is False: add('lift', code, d, 'lift check')
            if kind in ('ElectricLight','GameplayLight','AlarmLight','DestructibleMasterLight','Fuse','FuseBox') and (d.get('powered') is False or d.get('on') is False): add('power', code, d, 'owner look in play')
        if player:
            for d in decisions:
                if report.dist(d['pos'], player) <= s.get('radius',60) and d['recheck'] and d['impassable'] and not d['other'] and 'unlock' not in d['decision'] and 'unseal' not in d['decision']:
                    add('door', code, d, {'tool':'door_overrides.json','candidate':{'id':d['id'],'pos':d['pos'],'why':d['decision']}})
        if rules['garrison']['enabled'] and bucket == 'node' and cls.get('size') in rules['garrison']['sizes']:
            roles = Counter(o.get('role') for n in npcs for o in options if o.get('record') == n.get('record') and o.get('role') in ('combat','netrunner'))
            limits = rules['garrison']['sizes'][cls['size']]; total = roles['combat'] + roles['netrunner']
            if not limits['total'][0] <= total <= limits['total'][1] or not limits['netrunner'][0] <= roles['netrunner'] <= limits['netrunner'][1]: add('garrison',code,{'roles':dict(roles),'limits':limits},'owner look in play')
    a.out_dir.mkdir(parents=True, exist_ok=True)
    (a.out_dir/'sweep-violations.json').write_text(json.dumps(violations, indent=2)+'\n')
    lines = ['# Sweep violations','',f'{len(violations)} violations.','']
    for v in violations:
        lines += [f"## {v['class']} — {v['stop']} ({v['venue']})", '', f"- Evidence: `{json.dumps(v['evidence'], ensure_ascii=False)}`", f"- Route: `{json.dumps(v['route'], ensure_ascii=False)}`", '']
    (a.out_dir/'sweep-violations.md').write_text('\n'.join(lines))
    print(f'{len(violations)} violations: '+', '.join(f'{k} {v}' for k,v in sorted(Counter(x['class'] for x in violations).items())))
    print(f"Wrote {a.out_dir/'sweep-violations.md'} and {a.out_dir/'sweep-violations.json'}")

if __name__ == '__main__': main()
