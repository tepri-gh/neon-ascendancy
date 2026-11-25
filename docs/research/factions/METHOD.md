# Faction Control-Point Research — Method

Status: playbook, 2026-11-25. Derived from the Tyger Claws pilot
(`docs/research/factions/tyger-claws.md`) and a tested Arasaka corp trial.
This file is self-contained: an agent that receives **only** this file and a
faction name should be able to produce the faction doc and its JSON block.

Read `AGENTS.md` first. Do not commit. Do not launch the game. Do helper
scripting outside the repo with `python3 -I`.

---

## 1. Goal and scope

We are replacing a generic ~5-control-centres-per-sub-district grid with
**lore-relevant control points**: places a faction actually owns, runs, or
garrisons — especially interiors and businesses. These points feed a later
business/economy simulation.

Each faction doc must deliver:

1. One **HQ** recommendation (a map-marker anchor).
2. A ranked **location catalog** with verified coordinates.
3. An **economic structure**: which revenue streams the faction runs, mapped to
   specific places, using the shared vocabulary in §7.
4. **Per-sub-district counts** (`named` vs `filler`) for yield balancing.
5. A **machine-readable JSON block** (§10) that a seed script can parse.

Scope is Night City + Badlands + Dogtown in Cyberpunk 2077 **2.5 with Phantom
Liberty**. Reuse existing factions, spawns, and locations; invent nothing.

---

## 2. Data sources, ranked

Everything here is local and offline. Paths are relative to the repo root.

| Rank | Source | What it is good for |
| ---: | --- | --- |
| 1 | `data/sites/rosters.json` | **Best presence signal.** Which site the faction's units actually stand in, and how many. Join on `faction_id`. |
| 2 | `data/sites/sites.json` | Site anchors, `default_faction_id`, `is_interior`, `site_kind`, `district_id`, `sub_territory_id`, `quest_prefab_ref`. |
| 3 | `data/sites/{guards,triggers,spots,patrols,slots,doors,devices}.json` | **Interior identification.** Node names like `#kab_07_guard_area_casino_floor` tell you what a building is. |
| 4 | `dist/extract/markers.jsonl` | **Named-place coordinates.** One row per marker: `debug_name`, `x`, `y`, `z`. This is the only reliable offline source of named-point coordinates. |
| 5 | `data/sub_territories.json` + `data/landmarks.json` + `data/control_centers.json` + `data/faction_headquarters.json` | **Seed shortcut.** These already carry lore-ish names and per-sub-territory ownership. Check them before researching from scratch. |
| 6 | `dist/extract/areas.jsonl` | Faction **presence density** by community area (`faction_counts`, `dominant_faction`). Better than sites for Dogtown/Barghest. |
| 7 | `data/sites/communities.json` | Community paths and spawner refs per site, with coordinates. |
| 8 | `data/sites/suitabilities.json` | Business affordances: `club`, `market_stall`, `chop_shop`, `clinic`, `vehicle_bay`, `lab`, `warehouse`, `branch_office`, … |
| 9 | `data/factions.json` | `faction_id`, `code`, `affiliation_enum`, `category`, `display_name`. |
| 10 | `data/districts.json` | `gamedata_district`, bbox, `vanilla_gangs`. |
| 11 | Cyberpunk Wiki MediaWiki API | Lore, ownership, business type. Infobox only (§4). |
| 12 | `refs/cyberpunk/` `gamedataDistrict` / `gamedataSubDistrict` enums | Free primary-source existence check for a place enum. |
| — | `dist/extract/pois.jsonl` | **Ignore.** Only `journal_path_hash`; names cannot be resolved offline. |

### 2.1 Fields to use

- `rosters.json`: `site_id`, `faction_id`, `character_record_id`, `entry_name`, `community_hash`.
- `sites.json`: `site_id`, `code`, `anchor_x/y/z`, `default_faction_id`, `initial_owner_faction_id`, `is_interior`, `site_kind`, `district_id`, `sub_territory_id`, `quest_prefab_ref`, `source_path`.
- `areas.jsonl`: `debug_name`, `faction_counts`, `dominant_faction`, `x`, `y`, `z`, `community_hash`, `entry_count`.
- `markers.jsonl`: `debug_name`, `x`, `y`, `z`.
- `sub_territories.json`: `code`, `display_name`, `gamedata_subdistrict`, `initial_owner_faction_id`, `centroid_x/y/z`.
- `control_centers.json`: `code`, `display_name`, `x`, `y`, `z`, `sub_territory_id`, `is_active`.
- `landmarks.json`: `code`, `display_name`, `gamedata_district`, `kind` (`hq`/`compound`), `x`, `y`, `z`.
- `guards/triggers/spots/patrols/doors`: `site_id`, `node_ref`, `debug_name`, `x`, `y`, `z`.
- `suitabilities.json`: `site_id`, `suitability`, `score`.
- `factions.json`: `faction_id` (**numeric** — use this for joins), `code`, `affiliation_enum`.

### 2.2 Fields to ignore or distrust

- `areas.jsonl.district_code` — **wrong for `always_loaded_*` quest communities.**
  They inherit the file's path token. Example: `q105_com_dollhouse` is labelled
  `watson` but sits in JapanTown. Never aggregate presence by this field; use the
  attribution function in §3.
- `sites.json.initial_owner_faction_id` — **not a per-site faction.** It follows
  the seeded sub-territory owner. In the pilot, 102 sites "belonged" to Tyger
  Claws by this field but only 43 had Tyger units. Use `default_faction_id` plus
  the roster join.
- `is_interior` — sparse (17 of 424 sites). Its absence proves nothing; its
  presence is reliable.
- `pois.jsonl` — unusable offline.
- Anything in `refs/` that is a rendered/compiled view — treat as a hint, not a
  source.

### 2.3 Known pitfalls (all observed)

1. **Quest variants duplicate sites.** Ho-Oh is site 397 *and* 401. Dedupe by
   sub-district plus distance under 25 m (§3.4).
2. **`mws_*` mini-world-story sites are often crime scenes or ambushes, not
   businesses.** `mws_hey_07` is 24 Tyger units at a Trauma Team AV ambush.
   Presence is not ownership.
3. **Reused prefabs carry the wrong district codes.** `rey_09` sites sit in
   JapanTown at `(-537, 1292)` despite Heywood codes. Attribute by position.
4. **Marker names are wrapped in braces and sometimes `#`.** `{q105_mp_dollhouse_entrance}`,
   `{#q105_sm_03_dollhouse_mood}`. Normalize with `.strip('{}#')` before lookup.
5. **`areas.jsonl` is the better signal for Dogtown/Barghest.** Dogtown has
   almost no sector-level community areas; its 2,186 ep1 sectors contain zero
   `worldCompiledCommunityAreaNode`. Barghest has 187 areas but only 4 roster
   sites. Use areas for presence, sites for interiors.
6. **Corp security records are not always corp-prefixed.** Biotechnica's
   Dogtown security is `Character.sts_dtn_04_security`; Arasaka also has
   `Character.CorpoManArasaka`. Search by the corp token *and* by site.
7. **The extract has no vendor inventory.** "What it sells" is always `[wiki]`
   or `[inferred]`.
8. **Rendered wiki pages are mostly navigation.** Navboxes list every location
   in a district and say nothing about ownership. Use infoboxes only.
9. **Expect seed-vs-lore conflicts.** Kabuki Market's control centre is owned by
   The Mox in the seed but is Tyger Claws turf in lore. Report it; don't paper
   over it.
10. **Some factions have almost no footprint.** The Mox: 1 roster site / 3 units.
    Petrochem: 0 roster sites, 0 areas, 1 owned sub-territory. Say so plainly
    instead of inventing points.

---

## 3. Procedure

Set two variables once. `FID` is **numeric**; `CODE` is the seed code.

```python
import json
F = {f['code']: f for f in json.load(open('data/factions.json'))}
CODE = 'tyger_claws'
FID  = F[CODE]['faction_id']          # e.g. 2
AFF  = F[CODE]['affiliation_enum']    # e.g. 'TygerClaws'
print(FID, AFF, F[CODE]['category'])
```

### 3.0 Seed shortcut (do this first, it is cheap)

The seed files already encode lore-ish names and ownership. Check them before
doing any archaeology:

```python
import json
subs = json.load(open('data/sub_territories.json'))
lms  = {l['landmark_id']: l for l in json.load(open('data/landmarks.json'))}
owned = [s for s in subs if s['initial_owner_faction_id'] == FID]
print(len(owned), 'owned sub-territories')
for s in owned:
    l = lms.get(s['sub_territory_id']) or {}
    print(' ', s['code'], '|', s['gamedata_subdistrict'], '|', s['display_name'],
          '|', l.get('display_name'), '|', l.get('x'), l.get('y'), l.get('z'))
```

What this gives you: the sub-district and a display name for every seeded
holding. `sub_territories.display_name` is already updated to lore names in
places (`kab_allen_street` is **Ho-Oh**), and `landmarks.json` carries one named
anchor per sub-territory. Do not assume these names are correct — verify them
against §3.3/§3.4 — but they point you at the right 5–15 candidate places fast.

**Caveat:** `landmarks.json` and `control_centers.json` currently share
coordinates with `sub_territories.centroid_*`. A "nearest control centre" will
therefore be **0 m** from the landmark you just looked up. That is expected, not
a bug; it means the grid has already been partly retargeted.

### 3.1 Presence: which sites does the faction actually occupy

```python
import json, collections
sites = {s['site_id']: s for s in json.load(open('data/sites/sites.json'))}
roster = json.load(open('data/sites/rosters.json'))

units = collections.Counter()
chars = collections.defaultdict(collections.Counter)
for r in roster:
    if r.get('faction_id') == FID:
        units[r['site_id']] += 1
        chars[r['site_id']][r['character_record_id']] += 1

rows = []
for s in sites.values():
    n = units.get(s['site_id'], 0)
    if s['default_faction_id'] == FID or n > 0:
        rows.append((s['code'], s['site_id'], n, s['is_interior'],
                     round(s['anchor_x'], 1), round(s['anchor_y'], 1), round(s['anchor_z'], 1)))
print(len(rows), 'candidate sites')
for r in sorted(rows, key=lambda r: -r[2]):
    print(r)
```

`units` counts roster entries, which is a proxy for garrison size. A site with
`default_faction_id == FID` but zero units is faction-owned but empty; keep it
but flag it.

### 3.2 Presence by community area (use for Dogtown and density)

```python
import json, collections
rows = [json.loads(l) for l in open('dist/extract/areas.jsonl')]
mine = [r for r in rows if CODE in (r.get('faction_counts') or {})]
print(len(mine), 'areas;', sum(r['dominant_faction'] == CODE for r in mine), 'dominant')
for r in sorted(mine, key=lambda r: -r['faction_counts'][CODE])[:20]:
    print(r['faction_counts'][CODE], r['debug_name'], r['district_code'],
          round(r['x']), round(r['y']), round(r['z']))
```

### 3.3 Sub-district attribution (do not use `district_code`)

Attribute by (a) the geocode token in the record name, then (b) the nearest
geocoded site within 400 m, then (c) the nearest sub-territory centroid. This
reproduces the pilot's per-sub-district table exactly.

```python
import json, re, math, collections
SD = {'nid':'Northside','kab':'Kabuki','lch':'LittleChina','jpn':'JapanTown','hil':'CharterHill',
      'nok':'NorthOaks','gle':'Glen','rey':'VistaDelRey','spr':'Wellsprings','arr':'Arroyo',
      'rcr':'RanchoCoronado','cvi':'Coastview','wwd':'WestWindEstate','cpz':'CorpoPlaza','dtn':'Downtown'}
_SITE = re.compile(r'(?:ma|sts|mws|ce|de|sa|sq|cs|q\d+)_(?:wat|wbr|hey|std|pac|cct|bls)_([a-z]{3})')
_TOKEN = re.compile(r'(?:^|[\[{#_])(nid|kab|lch|jpn|hil|nok|gle|rey|spr|arr|rcr|cvi|wwd|cpz|dtn)_\d')

def token_sd(name):
    n = name or ''
    m = _SITE.search(n)
    if m and m.group(1) in SD:
        return SD[m.group(1)]
    m = _TOKEN.search(n)
    return SD.get(m.group(1)) if m else None

ref = [(s['anchor_x'], s['anchor_y'], token_sd(s['code']))
       for s in json.load(open('data/sites/sites.json'))]
ref = [r for r in ref if r[2]]
subs = json.load(open('data/sub_territories.json'))

def attribute(name, x, y, limit=400.0):
    sd = token_sd(name)
    if sd:
        return sd, 'token'
    b = min(ref, key=lambda z: (z[0]-x)**2 + (z[1]-y)**2)
    if math.dist((b[0], b[1]), (x, y)) <= limit:
        return b[2], 'nearest-site'
    b = min(subs, key=lambda z: (z['centroid_x']-x)**2 + (z['centroid_y']-y)**2)
    return b['gamedata_subdistrict'], 'nearest-subterritory'

rows = [json.loads(l) for l in open('dist/extract/areas.jsonl')]
mine = [r for r in rows if CODE in (r.get('faction_counts') or {})]
c, src = collections.Counter(), collections.Counter()
for r in mine:
    sd, how = attribute(r['debug_name'], r['x'], r['y'])
    c[sd] += 1
    src[how] += 1
print(sorted(c.items(), key=lambda x: -x[1]))
print(src)
```

If a row resolves via `nearest-subterritory`, flag it `[inferred]` in the doc.
Only one Tyger row needed that, and it was a Badlands point 3.2 km from any
geocoded site.

### 3.4 Dedupe site variants

```python
import math
def dedupe(rows, dist=25.0):
    kept = []
    for r in sorted(rows, key=lambda r: (-r[2], r[1])):   # (site_id, x, y)
        if all(math.dist((r[1], r[2]), (k[1], k[2])) >= dist for k in kept):
            kept.append(r)
    return kept
```

The pilot's 43 candidate sites did not collapse; the rule exists for the
next faction where it will (Ho-Oh 397/401 are the canonical example).

### 3.5 Identify interiors from site node names

This is how you turn `sts_wat_kab_07` into "Ho-Oh".

```python
import json
sid = 397
for fn in ('guards', 'triggers', 'spots', 'patrols', 'doors'):
    data = json.load(open(f'data/sites/{fn}.json'))
    names = sorted({r.get('node_ref') or r.get('debug_name') for r in data if r.get('site_id') == sid})
    if names:
        print(fn, names[:15])
```

Read the names like a caption: `casino_floor`, `inside_dojo`,
`barman_*`, `fighter_*`, `near_shrine` identify the business. Cross-check the
roster character records for a manager/boss (`Character.sts_wat_kab_07_jotaro`)
— that is the strongest single clue that a site is a named place.

### 3.6 Find named-place coordinates in markers

```python
import json
idx = {}
for line in open('dist/extract/markers.jsonl'):
    r = json.loads(line)
    idx.setdefault(r['debug_name'].strip('{}#'), []).append(r)

terms = ['dollhouse', 'jigjig', 'wakako', 'pachinko', 'fingers', 'clouds']
for name, rows in idx.items():
    if any(t in name.lower() for t in terms):
        print(name, rows[0]['x'], rows[0]['y'], rows[0]['z'])
```

Replace `terms` with your faction's place keywords (business names, fixer names,
district-specific landmarks). Normalize brace/`#` wrappers as shown. Prefer an
`*_entrance`, `*_mappin`, or `*_sm_<place>` marker over a `*_spwn_player_*`
marker (the latter is a player teleport, sometimes in a lobby or a different
floor). Record the exact marker `debug_name` as the coordinate source.

### 3.7 Nearest existing control centre

Use **all** control centres, active or not (`is_active` is a test flag, not a
spatial filter).

```python
import json, math
cc = json.load(open('data/control_centers.json'))
def nearest_cc(x, y):
    b = min(cc, key=lambda c: (c['x']-x)**2 + (c['y']-y)**2)
    return b['code'], round(math.dist((b['x'], b['y']), (x, y)), 1)
```

To get the CC's current owner, join `control_center.sub_territory_id` to
`sub_territories.sub_territory_id` and read `initial_owner_faction_id`. Note in
the doc when the owner conflicts with lore.

### 3.8 Rank, choose HQ and test point, count

- **HQ**: permanent-feeling seat with rooms to assign, canonically owned, and
  ideally in the faction's canon HQ district. Prefer an interior. State the
  trade-off.
- **Test control point**: an enclosed interior with clean ownership
  (`default_faction_id == FID`), rich guard/patrol/door records, and **not the
  HQ**, so the first in-game test exercises capture on a non-seat. Prefer one
  that is close to an existing CC so no new map plumbing is needed.
- **Ranked list**: relevance 1–5. Relevance reflects lore + revenue + record
  richness, not raw unit count.
- **Counts**: `named` and `filler` per sub-district (§8).

---

## 4. Wiki usage rules

Use the MediaWiki API, not the rendered page. It returns wikitext with the
infobox and no navigation furniture.

```
https://cyberpunk.fandom.com/api.php?action=parse&page=<Page>&prop=wikitext&format=json&formatversion=2
```

```python
import json, urllib.request, urllib.parse
def wikitext(page):
    q = urllib.parse.urlencode({'action': 'parse', 'page': page, 'prop': 'wikitext',
                                'format': 'json', 'formatversion': 2})
    req = urllib.request.Request('https://cyberpunk.fandom.com/api.php?' + q,
                                 headers={'User-Agent': 'NeonAscendancy-research/1.0'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)['parse']['wikitext']
```

Rules:

- **Infobox only.** For a location, read `owner=`, `type=`, `district=`,
  `sub_district=`, `location=`. For an organization, read `headquarters=`,
  `type=`, `faction locations=`.
- **Never take a coordinate from the wiki.** Coordinates come from §3.6 or are
  `TBD`.
- Ignore navboxes and "Appearances" sections for ownership; they list every
  location in a district.
- If the infobox and our seed disagree, report the conflict in
  *Gaps & uncertainties*.

---

## 5. Corp factions (no ganger rosters)

This covers **Arasaka, Militech, Kang Tao, Biotechnica, Petrochem** (and the
other megacorps in `data/factions.json`: Zetatech, Netwatch, Trauma Team,
News 54, Orbital Air, Night Corp, Kiroshi, Kendachi, Budget Arms). They have no
ganger rosters, but they are still fully represented in the extract.

### 5.1 Find the corp id and code

```python
import json
F = {f['code']: f for f in json.load(open('data/factions.json'))}
for code in ['arasaka','militech','kang_tao','biotechnica','petrochem']:
    f = F[code]
    print(code, f['faction_id'], f['affiliation_enum'], f['category'])
```

Arasaka 20, Militech 21, Kang Tao 22, Biotechnica 23, Petrochem 43.

### 5.2 Corp presence: three independent signals

```python
import json, collections
fid = F['arasaka']['faction_id']
units = collections.Counter()
chars = collections.Counter()
for r in json.load(open('data/sites/rosters.json')):
    if r.get('faction_id') == fid:
        units[r['site_id']] += 1
        chars[r['character_record_id']] += 1
print('roster sites:', len(units), 'units:', sum(units.values()))
print('security records:'); [print(' ', c, n) for c, n in chars.most_common()]
```

1. **Rosters** (`faction_id == fid`): corp security units standing in a site.
2. **`areas.jsonl`** (`CODE in faction_counts`): community-area density. This is
   the best signal in Dogtown and the Badlands.
3. **Seed ownership** (`sub_territories.initial_owner_faction_id == fid`):
   already-named facilities.

Corp security character records follow
`Character.{geocode}_{corp}_{guard|ranger|security|agent|ninja|sniper}_{archetype}_{weapon}_{ma|wa}[_elite]`,
e.g. `Character.cpz_arasaka_guard2_ranged1_kenshin_ma`,
`Character.wwd_arasaka_security1_ranged1_kenshin_ma`,
`Character.hil_arasaka_ninja_fmelee3_katana_wa_elite`. But some are generic
(`Character.sts_dtn_04_security`, `Character.CorpoManArasaka`), so also inspect
the records at the corp's sites.

Facility kinds to look for: towers/HQ, labs, manufacturing plants, industrial
parks, cargo piers, warehouses, estates, outposts, oil fields/refineries,
checkpoints, spaceports.

### 5.3 Tested Arasaka trial (what actually worked)

| Signal | Result |
| --- | --- |
| `sub_territories` owned | 12: Konpeki Plaza Approach, Arasaka North Cargo Pier, Waterfront Freight Terminal, Waterfront South Quay (ArasakaWaterfront); Charter Hill Substation, Charter Hill Terraces (CharterHill); Arasaka Estate Gate, North Oak Columbarium, North Oak Villa Ridge (NorthOaks); Arasaka Industrial Park (Arroyo); Arasaka Tower Plaza, Memorial Ring West (CorpoPlaza) |
| Roster sites | 8 sites / 68 units |
| Character records | 21, including `cpz_arasaka_guard*`, `nid_arasaka_ranger*`, `hil_arasaka_ninja*`, `wwd_arasaka_security1*`, `CorpoManArasaka`, `CorpoWomanArasaka` |
| `areas.jsonl` | 146 areas, 126 Arasaka-dominant (City Center 55, Watson 34) |
| Named facilities from markers | Arasaka Tower lobby `{q115_12b_sm_tower_lobby}` `(-1443.5, 158.5, 15.4)`; rooftop `q101_mk_arasaka_rooftop` `(-1428.3, 188.4, 616.7)`; underground manufacturing `q114_11_sm_arasaka_manufacturing_infiltration` `(-1481.7, 81.3, -23.8)`; Arasaka Memorial `mq061_03_sm_arasaka_memorial_scene` `(-1317.8, -84.3, 0.0)`; Konpeki room `mirror_sm_scene_konpeki_room` `(-2205.1, 1774.9, 163.0)`; Hanako estate `q113_04_sm_hanako_estate` `(287.8, 1017.9, 230.3)` |
| Landmark names | "Arasaka Tower Plaza", "Arasaka Industrial Park", "Arasaka North Cargo Pier", "Arasaka Estate Gate" |

**Verdict:** the method works for corps without any special extract. Roster +
areas + seed ownership + markers is enough to find towers, labs, plants and
outposts. The wiki supplies the `owner=`/`type=` infobox and the business
description. Two cautions:

- **Not every corp has a footprint.** Biotechnica has 2 roster sites / 25 units
  and 5 areas; Petrochem has **zero** rosters, **zero** areas and one named
  landmark (`Petrochem Freight Yard`). For Petrochem, document the lore business
  (oil/fuel) and leave coordinates `TBD`, or use the owned sub-territory anchor.
- **A roster site is not necessarily the corp's.** `sts_ep1_08` (Dogtown) has 27
  Arasaka units but is a KGB hologram set piece; `mws_se5_03` is a scav/ambush
  mini-world-story. Verify the site identity via §3.5 before calling it a
  facility.

### 5.4 Corp economic structure

Corps rarely earn from a single storefront. Model them with the vocabulary:

| Corp | Typical streams |
| --- | --- |
| Arasaka | `security_services`, `manufacturing`, `rnd`, `arms`, `cyberware`, `real_estate` |
| Militech | `arms`, `security_services`, `manufacturing`, `rnd` |
| Kang Tao | `arms`, `manufacturing`, `rnd` |
| Biotechnica | `agriculture`, `rnd`, `manufacturing` |
| Petrochem | `energy`, `manufacturing`, `smuggling` |

Treat these as hypotheses to confirm with the wiki infobox, not facts.

---

## 6. Confidence tags and the coordinate rule

Every factual claim gets exactly one tag:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[game-data]` | Position, site, community, roster, or spawn record read from `dist/extract/` or `data/` (2.5 build) | Primary, exact |
| `[wiki]` | Cyberpunk Wiki page (cited inline) | Secondary, high |
| `[lore]` | Book/artbook/tabletop lore with no verified in-game artifact | Tertiary |
| `[inferred]` | Reasoning links a named place to a game record; reasoning stated | Weak, flagged |

**Coordinate rule:** site anchor, then marker, else `TBD`. **Never take a
coordinate from the wiki.** Every `(x, y, z)` in the doc and in the JSON block
must be traceable to a local record; name that record in the `source` field.
Round to 3 decimals for seeds. If a point is `TBD`, use `null` — never `0`.

---

## 7. Shared revenue-stream vocabulary

All faction docs use these exact short codes. One line each; do not invent
synonyms. A place can have several.

| Code | Definition |
| --- | --- |
| `sex_work` | Prostitution, dollhouses, joytoy trade, trafficking |
| `gambling` | Casinos, pachinko, bookmaking, fight betting |
| `drugs` | Narcotics manufacture, wholesale, or retail |
| `arms` | Weapons sales, gun running, ammunition |
| `cyberware` | Chrome sales, ripperdoc trade, scavenged implants |
| `braindance` | BD production or sale, including illegal XBD |
| `protection` | Extortion, "security" fees on local businesses |
| `vehicles_chop` | Chop shops, stolen-vehicle fencing, vehicle bays |
| `smuggling` | Contraband logistics, border and dock running |
| `fixer_brokerage` | Fixer commissions, contract brokering |
| `security_services` | Licensed corporate or military security contracts |
| `manufacturing` | Factories, assembly, industrial production |
| `rnd` | Research, labs, prototypes, testing |
| `energy` | Power, fuel, oil, utilities |
| `real_estate` | Property, rent, development |
| `retail` | Shops, markets, storefronts |
| `food_drink` | Bars, restaurants, food stalls, nightlife |
| `media` | News, propaganda, entertainment broadcasting |
| `agriculture` | Farming, protein/soil production, agri-labs |

---

## 8. Two-tier count rule

Count two different things and never mix them:

- **`named`** — distinct lore-relevant places the faction owns, runs, protects
  or habitually occupies. One entry per named place, not per quest variant. This
  is the number used for **yield balancing** (named places carry the high yield).
- **`filler`** — deduped faction-occupied sites that are **not** a named catalog
  point. These are honest but generic: "occupied block", not "lore business".
  Filler points should not receive iconic-business yield multipliers.

Rules:

- Dedupe site variants within 25 m and by sub-district.
- A named place does not have to be one of our sites (Clouds, Jig-Jig Street,
  Wakako's parlor are marker-only). It still counts as `named`.
- A site that is a named catalog point is excluded from `filler` even if its
  geocode attributes it to a different sub-district. In the pilot, the shrine
  site attributes to JapanTown but is catalogued as a NorthOak named place.
- Report the total: `named` + `filler` should reconcile with the deduped site
  count plus marker-only named places.

Tyger Claws reconciliation: 10 named + 38 filler = 48; 43 deduped occupied
sites − 5 site-backed named points = 38 filler; 10 named = 4 marker-only + 5
site-backed + 1 named place that is neither (Kabuki Market's site is NCPD-owned).

---

## 9. Document template

Every `docs/research/factions/<faction-code>.md` must have these sections, in
this order. `<faction-code>` is the `code` from `data/factions.json`
(`tyger_claws`, `sixth_street`, `the_mox`, `kang_tao`, …).

1. **Summary** — who they are, canon base, economic model, where the weight sits.
2. **Territory** — districts, evidence table (lore / vanilla panel / game-data
   counts), sub-district presence table, attribution caveat.
3. **Location catalog** — the master table: name, type, district/sub-district,
   interior?, business?, coordinates, coordinate source, linked
   communities/sites, confidence. Then a short "how the name→coordinate links
   were proven" subsection and a **generic occupied-site** table (suitability
   tags) as the filler pool.
4. **Economic structure** — revenue streams → catalog locations, using §7 codes;
   then suppliers/customers/rivals.
5. **Headquarters recommendation** — primary HQ with coordinates, numbered
   rationale, trade-off; 2 alternates; overruled suggestions.
6. **Priority list of control points** — ranked table with relevance,
   coordinates, nearest existing CC + distance, and why. Must include one
   **test control point** that is not the HQ, with a justification.
7. **Per-sub-district counts** — `named` and `filler` per sub-district, with the
   sites behind the filler count.
8. **Gaps & uncertainties** — numbered, honest; conflicts with seed data and
   inferred links called out.
9. **Sources** — local files and wiki pages, grouped.
10. **Machine-readable block** — the fenced `json` block from §10, last in the
    file. No prose after it.

Use the confidence tags in every table. Keep the doc in the same voice as the
pilot: direct, evidence-first, no filler prose.

---

## 10. Machine-readable block

The last thing in every faction doc is a fenced ` ```json ` block. It is parsed
to seed the game, so it must be strict JSON.

### 10.1 Shape

```json
{
  "faction_code": "tyger_claws",
  "hq": {"name": "…", "district": "Westbrook", "sub_district": "JapanTown",
         "x": -662.718, "y": 806.865, "z": 129.893,
         "source": "dist/extract/markers.jsonl q105_mp_dollhouse_entrance",
         "confidence": "game-data+wiki"},
  "alternate_hqs": [ /* same shape */ ],
  "test_control_point": { /* same shape */ },
  "control_points": [
    {"rank": 1, "name": "…", "type": "dollhouse", "relevance": 5,
     "district": "Westbrook", "sub_district": "JapanTown",
     "x": -662.718, "y": 806.865, "z": 129.893,
     "source": "…", "confidence": "game-data+wiki",
     "interior": true,
     "revenue_streams": ["sex_work", "braindance", "food_drink"],
     "nearest_cc_code": "cc_jpn_crescent_alley", "nearest_cc_m": 103.7}
  ],
  "subdistrict_counts": {
    "JapanTown": {"named": 4, "filler": 13}
  }
}
```

Field rules:

- `faction_code` — `code` from `data/factions.json`.
- `district` — `gamedataDistrict` spelling from `data/districts.json`
  (`Watson`, `Westbrook`, `Heywood`, `SantoDomingo`, `Pacifica`, `CityCenter`,
  `Badlands`, `Dogtown`).
- `sub_district` — **`gamedata_subdistrict` spelling** from
  `data/sub_territories.json` (`JapanTown`, `Kabuki`, `LittleChina`,
  `CharterHill`, `NorthOaks`, `Northside`, `Glen`, `VistaDelRey`, `Downtown`,
  `CorpoPlaza`, `Wellsprings`, `Arroyo`, `RanchoCoronado`, `Coastview`,
  `WestWindEstate`, `ArasakaWaterfront`, `Badlands`, `Dogtown`, `MorroRock`).
- `x/y/z` — verified numbers or `null`. Never `0` as a placeholder.
- `confidence` — one or more §6 tags joined with `+`, strongest first.
- `interior` — boolean. `true` if the game has a distinct interior cell, even if
  `is_interior` is unset (the flag is sparse). Say how you know in the doc.
- `revenue_streams` — only §7 codes.
- `nearest_cc_code` / `nearest_cc_m` — from §3.7, all CCs regardless of
  `is_active`.
- `subdistrict_counts` — only sub-districts with a nonzero count, or the full
  set the doc discusses. `named` + `filler` must equal the doc's totals.

### 10.2 Validate before you finish

Run this against your own doc. It checks JSON syntax, required keys, tag and
vocabulary membership, coordinate sanity, and sub-district spelling.

```python
import json, re, sys

path = 'docs/research/factions/<faction-code>.md'   # substitute your file
text = open(path).read()
raw = text.rsplit('```json', 1)[1].split('```', 1)[0]
d = json.loads(raw)                                  # strict parse

VOCAB = {'sex_work','gambling','drugs','arms','cyberware','braindance','protection',
         'vehicles_chop','smuggling','fixer_brokerage','security_services','manufacturing',
         'rnd','energy','real_estate','retail','food_drink','media','agriculture'}
TAGS = {'game-data','wiki','lore','inferred'}
SUBS = {s['gamedata_subdistrict'] for s in json.load(open('data/sub_territories.json'))}
DISTRICTS = {d2['gamedata_district'] for d2 in json.load(open('data/districts.json'))}

assert {'faction_code','hq','alternate_hqs','test_control_point',
        'control_points','subdistrict_counts'} <= set(d)
point_keys = {'name','district','sub_district','x','y','z','source','confidence'}
assert point_keys <= set(d['hq'])
assert point_keys <= set(d['test_control_point'])
for p in [d['hq'], d['test_control_point']] + d['alternate_hqs']:
    if p['sub_district'] is not None: assert p['sub_district'] in SUBS, p['sub_district']
    if p['district'] is not None: assert p['district'] in DISTRICTS, p['district']
    assert set(p['confidence'].split('+')) <= TAGS, p['confidence']
    for k in ('x','y','z'):
        assert p[k] is None or abs(p[k]) < 20000, (p['name'], k, p[k])
ranks = [p['rank'] for p in d['control_points']]
assert ranks == list(range(1, len(ranks)+1)), ranks
for p in d['control_points']:
    assert p['sub_district'] in SUBS, p['sub_district']
    assert p['district'] in DISTRICTS, p['district']
    assert set(p['confidence'].split('+')) <= TAGS, p['confidence']
    assert set(p['revenue_streams']) <= VOCAB, p['revenue_streams']
    assert 1 <= p['relevance'] <= 5, p['relevance']
    assert isinstance(p['interior'], bool)
    for k in ('x','y','z'):
        assert p[k] is None or abs(p[k]) < 20000, (p['name'], k, p[k])
for sd, v in d['subdistrict_counts'].items():
    assert sd in SUBS, sd
    assert v['named'] >= 0 and v['filler'] >= 0
print('OK', d['faction_code'], len(d['control_points']), 'control points')
```

The snippet above was run against the pilot doc after it was converted.

---

## Appendix — measured faction footprints (set expectations)

From the 2.5 extract, for the 16 factions in scope. `areas` = community areas
containing the faction; `rosters` = sites with at least one of its units.

| Faction | fid | roster sites | units | owned sub-territories | areas |
| --- | ---: | ---: | ---: | ---: | ---: |
| Maelstrom | 1 | 22 | 134 | 7 | 73 |
| Tyger Claws | 2 | 43 | 306 | 17 | 135 |
| Valentinos | 3 | 24 | 177 | 13 | 87 |
| 6th Street | 4 | 29 | 183 | 9 | 96 |
| Voodoo Boys | 5 | 3 | 38 | 4 | 40 |
| Animals | 6 | 14 | 97 | 4 | 45 |
| Scavengers | 7 | 24 | 210 | 5 | 104 |
| Wraiths | 8 | 12 | 85 | 3 | 55 |
| Aldecaldos | 9 | 5 | 8 | 1 | 61 |
| Barghest | 10 | 4 | 87 | 4 | 187 |
| The Mox | 11 | 1 | 3 | 1 | 20 |
| Arasaka | 20 | 8 | 68 | 12 | 146 |
| Militech | 21 | 25 | 159 | 10 | 136 |
| Kang Tao | 22 | 4 | 24 | 2 | 17 |
| Biotechnica | 23 | 2 | 25 | 2 | 5 |
| Petrochem | 43 | 0 | 0 | 1 | 0 |

Use this to calibrate ambition, not to write the doc. A faction with one roster
site still gets a full doc: named places can be marker-only, and the honest
answer may be "little verified footprint; seed the landmark only".
