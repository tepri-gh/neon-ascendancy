-- Neon Ascendancy static world database, v2: living-site model.
--
-- Additive migration: apply AFTER world_v1.sql. No v1 table, column, index, or
-- row is altered or dropped. Bumps PRAGMA user_version to 2.
--
-- Semantics
--   * A "site" is one *physical place* (one quest prefab). A single place can
--     host several vanilla content graphs (ma/sts/mws/mq/sq); those live in
--     site_bindings, while conquest/garrison/conversion attach to world_sites.
--   * NodeRefs are stored verbatim as authored ('#kab_07_com_enemies',
--     '$/03_night_city/.../#prefab'), plus global_node_id: the compiled
--     uint64 NodeRef hash as TEXT (SQLite has no u64).
--   * Coordinates are CP2077 world-space metres (X/Y/Z, Z up). Yaw radians,
--     counter-clockwise from +X.
--   * Site-level has_*/count columns are denormalised rollups; the build
--     asserts they agree with the child tables before publishing.
--
-- Sources: docs/research/living-world-site-modeling.md §4.2.

PRAGMA user_version = 2;

-- ---------------------------------------------------------------------------
-- 1. Physical sites
-- ---------------------------------------------------------------------------

CREATE TABLE world_sites (
  site_id              INTEGER PRIMARY KEY,
  code                 TEXT    NOT NULL UNIQUE,      -- 'sts_wat_kab_07'
  display_name         TEXT,                          -- NULL until a journal join lands
  site_kind            TEXT    NOT NULL CHECK (site_kind IN (
                         'scanner_hustle','fixer_gig','mini_world_story',
                         'side_quest','combat_event','dynamic_event',
                         'corp_facility','gang_compound','interior_hideout',
                         'service','manual')),
  source_family        TEXT    NOT NULL CHECK (source_family IN (
                         'ma','sts','sts_ep1','mws','mq','sq','ce','de','manual')),
  district_id          INTEGER NOT NULL REFERENCES districts(district_id),
  sub_territory_id     INTEGER REFERENCES sub_territories(sub_territory_id),
  control_center_id    INTEGER REFERENCES control_centers(control_center_id),

  anchor_x             REAL    NOT NULL,
  anchor_y             REAL    NOT NULL,
  anchor_z             REAL    NOT NULL,
  bbox_min_x           REAL,
  bbox_min_y           REAL,
  bbox_min_z           REAL,
  bbox_max_x           REAL,
  bbox_max_y           REAL,
  bbox_max_z           REAL,
  radius_m             REAL    NOT NULL DEFAULT 40.0 CHECK (radius_m > 0.0),

  is_interior          INTEGER NOT NULL DEFAULT 0 CHECK (is_interior IN (0,1)),
  interior_map_coords  TEXT,                          -- worldInteriorMapNode.coords
  floor_count          INTEGER CHECK (floor_count IS NULL OR floor_count >= 1),

  default_faction_id       INTEGER REFERENCES factions(faction_id),
  initial_owner_faction_id INTEGER REFERENCES factions(faction_id),
  faction_source       TEXT    NOT NULL DEFAULT 'none'
                         CHECK (faction_source IN ('tweak','spatial','manual','none')),

  tier                 INTEGER NOT NULL DEFAULT 1 CHECK (tier BETWEEN 1 AND 5),
  difficulty           INTEGER NOT NULL DEFAULT 1 CHECK (difficulty BETWEEN 1 AND 5),
  loot_tier            INTEGER NOT NULL DEFAULT 1 CHECK (loot_tier BETWEEN 1 AND 5),

  -- Denormalised rollups, asserted against the child tables at build time.
  has_patrols          INTEGER NOT NULL DEFAULT 0 CHECK (has_patrols IN (0,1)),
  has_workspots        INTEGER NOT NULL DEFAULT 0 CHECK (has_workspots IN (0,1)),
  has_guard_areas      INTEGER NOT NULL DEFAULT 0 CHECK (has_guard_areas IN (0,1)),
  has_security_devices INTEGER NOT NULL DEFAULT 0 CHECK (has_security_devices IN (0,1)),
  has_doors            INTEGER NOT NULL DEFAULT 0 CHECK (has_doors IN (0,1)),
  has_community        INTEGER NOT NULL DEFAULT 0 CHECK (has_community IN (0,1)),
  spot_count           INTEGER NOT NULL DEFAULT 0 CHECK (spot_count   >= 0),
  patrol_count         INTEGER NOT NULL DEFAULT 0 CHECK (patrol_count >= 0),
  device_count         INTEGER NOT NULL DEFAULT 0 CHECK (device_count >= 0),
  community_count      INTEGER NOT NULL DEFAULT 0 CHECK (community_count >= 0),

  -- Runtime materialisation handles (native plugin / generated phases).
  quest_prefab_ref     TEXT,                          -- '#sts_wat_kab_07_streetstory'
  quest_sector_path    TEXT,                          -- 'base\worlds\...\quest_<hash>.streamingsector'
  sector_category      TEXT CHECK (sector_category IN ('Quest','Interior','Exterior')),
  streaming_block      TEXT,                          -- 'base\worlds\...\blocks\all.streamingblock'

  -- Provenance / trust.
  extraction_confidence TEXT NOT NULL DEFAULT 'exact'
                         CHECK (extraction_confidence IN ('exact','derived','heuristic','unresolved')),
  source_archive       TEXT NOT NULL,
  source_path          TEXT NOT NULL,
  UNIQUE (source_path)
) STRICT;

CREATE INDEX idx_world_sites_kind        ON world_sites(site_kind);
CREATE INDEX idx_world_sites_family      ON world_sites(source_family);
CREATE INDEX idx_world_sites_territory   ON world_sites(sub_territory_id);
CREATE INDEX idx_world_sites_district    ON world_sites(district_id);
CREATE INDEX idx_world_sites_center      ON world_sites(control_center_id);
CREATE INDEX idx_world_sites_faction     ON world_sites(default_faction_id);
CREATE INDEX idx_world_sites_prefab      ON world_sites(quest_prefab_ref);

CREATE VIRTUAL TABLE site_rtree USING rtree(id, min_x, max_x, min_y, max_y);

-- Which vanilla content used this physical site (one site, many bindings).
CREATE TABLE site_bindings (
  site_id             INTEGER NOT NULL REFERENCES world_sites(site_id) ON DELETE CASCADE,
  content_kind        TEXT    NOT NULL CHECK (content_kind IN
                        ('ma','sts','sts_ep1','mws','mq','sq','ce','de')),
  content_code        TEXT    NOT NULL,               -- 'sts_wat_kab_07' / 'mq304'
  quest_phase_path    TEXT,                           -- '...\sts_wat_kab_07_combat.questphase'
  quest_resource_path TEXT,                           -- '...\sts_wat_kab_07_quest.quest'
  is_primary          INTEGER NOT NULL DEFAULT 0 CHECK (is_primary IN (0,1)),
  PRIMARY KEY (site_id, content_kind, content_code)
) STRICT, WITHOUT ROWID;

CREATE INDEX idx_site_bindings_code ON site_bindings(content_code);

-- Intent vocabulary: what this place can become / be used for.
CREATE TABLE site_suitabilities (
  site_id     INTEGER NOT NULL REFERENCES world_sites(site_id) ON DELETE CASCADE,
  suitability TEXT    NOT NULL CHECK (suitability IN (
                'raid_target','stealth_entry','sniper_nest','vehicle_bay',
                'rooftop_access','sewer_access','elevator','hostage_site',
                'officer_site','arms_cache','data_vault','terminal_cluster',
                'turret_cluster','camera_net','safehouse','chop_shop',
                'netrunner_den','clinic','club','warehouse','branch_office',
                'market_stall','lab')),
  score       INTEGER NOT NULL DEFAULT 50 CHECK (score BETWEEN 0 AND 100),
  PRIMARY KEY (site_id, suitability)
) STRICT, WITHOUT ROWID;

CREATE INDEX idx_site_suitabilities_kind ON site_suitabilities(suitability, score DESC);

-- ---------------------------------------------------------------------------
-- 2. Communities and their roster
-- ---------------------------------------------------------------------------

CREATE TABLE site_communities (
  site_community_id INTEGER PRIMARY KEY,
  site_id           INTEGER NOT NULL REFERENCES world_sites(site_id) ON DELETE CASCADE,
  community_hash    TEXT    NOT NULL,                 -- registry communityId hash
  spawner_ref       TEXT    NOT NULL,                 -- '#kab_07_com_enemies'
  spawner_global_id TEXT,
  area_node_type    TEXT CHECK (area_node_type IN ('Regular','Streamable','Background')),
  community_path    TEXT,                             -- '...\sts_wat_kab_07_com_enemies.community'
  is_primary        INTEGER NOT NULL DEFAULT 0 CHECK (is_primary IN (0,1)),
  entry_count       INTEGER NOT NULL DEFAULT 0 CHECK (entry_count >= 0),
  active_on_start   INTEGER NOT NULL DEFAULT 0 CHECK (active_on_start >= 0),
  x REAL NOT NULL, y REAL NOT NULL, z REAL NOT NULL,
  UNIQUE (site_id, community_hash)
) STRICT;

CREATE INDEX idx_site_communities_hash    ON site_communities(community_hash);
CREATE INDEX idx_site_communities_spawner ON site_communities(spawner_ref);

CREATE TABLE site_community_entries (
  entry_id              INTEGER PRIMARY KEY,
  site_community_id     INTEGER NOT NULL REFERENCES site_communities(site_community_id) ON DELETE CASCADE,
  entry_name            TEXT    NOT NULL,             -- 'Enemy11', 'Jotaro'
  character_record_id   TEXT,                         -- 'Character.kab_07_enemy_1st_floor_handgun'
  faction_id            INTEGER REFERENCES factions(faction_id),
  role_hint             TEXT CHECK (role_hint IN (
                          'grunt','officer','boss','sniper','melee','ranged',
                          'netrunner','medic','driver','civilian','unknown')),
  initial_phase_name    TEXT,
  entry_active_on_start INTEGER NOT NULL DEFAULT 0 CHECK (entry_active_on_start IN (0,1)),
  spawn_in_view         INTEGER NOT NULL DEFAULT 1 CHECK (spawn_in_view IN (0,1)),
  UNIQUE (site_community_id, entry_name)
) STRICT;

CREATE INDEX idx_site_entries_faction ON site_community_entries(faction_id);
CREATE INDEX idx_site_entries_role    ON site_community_entries(role_hint);

CREATE TABLE site_community_phases (
  phase_id       INTEGER PRIMARY KEY,
  entry_id       INTEGER NOT NULL REFERENCES site_community_entries(entry_id) ON DELETE CASCADE,
  phase_name     TEXT    NOT NULL,                    -- '0combat','alarm','default'
  always_spawned TEXT    NOT NULL DEFAULT 'default__false_'
                   CHECK (always_spawned IN ('default__false_','true_','false_')),
  hour           TEXT    NOT NULL DEFAULT 'Any'
                   CHECK (hour IN ('Day','Night','Morning','Evening','Any')),
  quantity       INTEGER NOT NULL DEFAULT 1 CHECK (quantity >= 0),
  is_sequence    INTEGER NOT NULL DEFAULT 0 CHECK (is_sequence IN (0,1)),
  UNIQUE (entry_id, phase_name, hour, quantity)
) STRICT;

CREATE INDEX idx_site_phases_name ON site_community_phases(phase_name);

-- One row per (phase, workspot). This join makes AIUseWorkspot possible
-- straight from the database.
CREATE TABLE site_community_slots (
  phase_id   INTEGER NOT NULL REFERENCES site_community_phases(phase_id) ON DELETE CASCADE,
  slot_index INTEGER NOT NULL,
  spot_ref   TEXT    NOT NULL,                       -- '#kab_07_ws_1stfloor_tyger_002'
  spot_id    INTEGER REFERENCES site_spots(spot_id) ON DELETE SET NULL,
  markings   TEXT,                                   -- JSON array of CName strings
  PRIMARY KEY (phase_id, slot_index)
) STRICT, WITHOUT ROWID;

-- ---------------------------------------------------------------------------
-- 3. Workspots, patrols, guard areas
-- ---------------------------------------------------------------------------

CREATE TABLE site_spots (
  spot_id           INTEGER PRIMARY KEY,
  site_id           INTEGER NOT NULL REFERENCES world_sites(site_id) ON DELETE CASCADE,
  node_ref          TEXT    NOT NULL,
  global_node_id    TEXT,
  debug_name        TEXT,
  workspot_resource TEXT,                            -- 'base\workspots\...\guard__01.workspot'
  spot_role         TEXT CHECK (spot_role IN
                      ('guard','patrol','idle','sit','sleep','work','eat','drink',
                       'dance','drug','inspect','search','cover','sniper','driver',
                       'crowd','unknown')),
  markings          TEXT,                            -- JSON array
  is_workspot_infinite INTEGER NOT NULL DEFAULT 0 CHECK (is_workspot_infinite IN (0,1)),
  is_workspot_static   INTEGER NOT NULL DEFAULT 0 CHECK (is_workspot_static IN (0,1)),
  actor_bodytype    TEXT,
  floor_index       INTEGER,
  x REAL NOT NULL, y REAL NOT NULL, z REAL NOT NULL, yaw REAL,
  source_sector     TEXT NOT NULL,
  UNIQUE (site_id, node_ref)
) STRICT;

CREATE INDEX idx_site_spots_role ON site_spots(spot_role);
CREATE INDEX idx_site_spots_gnid ON site_spots(global_node_id);
CREATE VIRTUAL TABLE site_spot_rtree USING rtree(id, min_x, max_x, min_y, max_y);

CREATE TABLE site_patrols (
  patrol_id      INTEGER PRIMARY KEY,
  site_id        INTEGER NOT NULL REFERENCES world_sites(site_id) ON DELETE CASCADE,
  node_ref       TEXT    NOT NULL,
  global_node_id TEXT,
  debug_name     TEXT,
  point_count    INTEGER NOT NULL DEFAULT 0 CHECK (point_count >= 0),
  floor_index    INTEGER,
  x REAL NOT NULL, y REAL NOT NULL, z REAL NOT NULL,
  source_sector  TEXT NOT NULL,
  UNIQUE (site_id, node_ref)
) STRICT;

CREATE INDEX idx_site_patrols_site ON site_patrols(site_id);

CREATE TABLE site_patrol_points (
  patrol_id   INTEGER NOT NULL REFERENCES site_patrols(patrol_id) ON DELETE CASCADE,
  point_index INTEGER NOT NULL,
  spot_ref    TEXT    NOT NULL,                      -- NodeRef of the workspot point
  spot_id     INTEGER REFERENCES site_spots(spot_id) ON DELETE SET NULL,
  point_type  TEXT    NOT NULL DEFAULT 'Workspot'
                CHECK (point_type IN ('Workspot','Point','Entity')),
  x REAL, y REAL, z REAL,
  PRIMARY KEY (patrol_id, point_index)
) STRICT, WITHOUT ROWID;

CREATE TABLE site_guard_areas (
  guard_area_id   INTEGER PRIMARY KEY,
  site_id         INTEGER NOT NULL REFERENCES world_sites(site_id) ON DELETE CASCADE,
  node_ref        TEXT    NOT NULL,
  global_node_id  TEXT,
  debug_name      TEXT,
  pursuit_range_m REAL CHECK (pursuit_range_m IS NULL OR pursuit_range_m >= 0.0),
  floor_index     INTEGER,
  x REAL NOT NULL, y REAL NOT NULL, z REAL NOT NULL,
  source_sector   TEXT NOT NULL,
  UNIQUE (site_id, node_ref)
) STRICT;

CREATE INDEX idx_site_guard_areas_site ON site_guard_areas(site_id);

CREATE TABLE site_guard_area_communities (
  guard_area_id INTEGER NOT NULL REFERENCES site_guard_areas(guard_area_id) ON DELETE CASCADE,
  community_ref TEXT    NOT NULL,                    -- '#kab_07_com_enemies'
  is_primary    INTEGER NOT NULL DEFAULT 1 CHECK (is_primary IN (0,1)),
  entry_names   TEXT,                                -- JSON array of CName
  PRIMARY KEY (guard_area_id, community_ref)
) STRICT, WITHOUT ROWID;

-- ---------------------------------------------------------------------------
-- 4. Devices, doors, triggers, prefab variants
-- ---------------------------------------------------------------------------

CREATE TABLE site_devices (
  device_id         INTEGER PRIMARY KEY,
  site_id           INTEGER NOT NULL REFERENCES world_sites(site_id) ON DELETE CASCADE,
  node_ref          TEXT    NOT NULL,
  global_node_id    TEXT,
  debug_name        TEXT,
  device_kind       TEXT    NOT NULL CHECK (device_kind IN (
                      'security_area','security_system','camera','turret',
                      'terminal','computer','door','gate','lift','vending',
                      'speaker','tv','other')),
  controller_class  TEXT,                            -- 'SecurityAreaControllerPS', 'DoorControllerPS'
  entity_template   TEXT,
  connected_community_ref TEXT,                      -- from deviceConnections[CommunityProxyPS]
  is_quest_gated    INTEGER NOT NULL DEFAULT 0 CHECK (is_quest_gated IN (0,1)),
  floor_index       INTEGER,
  x REAL NOT NULL, y REAL NOT NULL, z REAL NOT NULL,
  source_sector     TEXT NOT NULL,
  UNIQUE (site_id, node_ref)
) STRICT;

CREATE INDEX idx_site_devices_kind ON site_devices(device_kind);
CREATE INDEX idx_site_devices_site ON site_devices(site_id);

CREATE TABLE site_doors (
  door_id             INTEGER PRIMARY KEY,
  site_id             INTEGER NOT NULL REFERENCES world_sites(site_id) ON DELETE CASCADE,
  device_id           INTEGER REFERENCES site_devices(device_id) ON DELETE SET NULL,
  node_ref            TEXT    NOT NULL,
  global_node_id      TEXT,
  debug_name          TEXT,
  door_role           TEXT    NOT NULL CHECK (door_role IN
                        ('entrance','exit','interior','elevator','garage','roof','service')),
  controller_class    TEXT    NOT NULL DEFAULT 'DoorControllerPS',
  default_state       TEXT    CHECK (default_state IN ('OPENED','CLOSED','LOCKED','SEALED')),
  requires_power      INTEGER NOT NULL DEFAULT 1 CHECK (requires_power IN (0,1)),
  unlock_action       TEXT    NOT NULL DEFAULT 'ForcePower'
                        CHECK (unlock_action IN ('ForcePower','ForceOpen','ForceUnlock','None')),
  vanilla_lock_action TEXT,                          -- observed questDeviceManager action
  UNIQUE (site_id, node_ref)
) STRICT;

CREATE INDEX idx_site_doors_site ON site_doors(site_id);

CREATE TABLE site_triggers (
  trigger_id   INTEGER PRIMARY KEY,
  site_id      INTEGER NOT NULL REFERENCES world_sites(site_id) ON DELETE CASCADE,
  node_ref     TEXT    NOT NULL,
  global_node_id TEXT,
  debug_name   TEXT,
  trigger_role TEXT CHECK (trigger_role IN
                  ('entry','mission_volume','ambush','extraction','elevator',
                   'elevator_close','despawn','patrol_gate','unknown')),
  volume_json  TEXT,
  x REAL NOT NULL, y REAL NOT NULL, z REAL NOT NULL,
  UNIQUE (site_id, node_ref)
) STRICT;

CREATE INDEX idx_site_triggers_site ON site_triggers(site_id);

-- Prefab variants observed in the streaming block (lockdown, interior, loot…).
CREATE TABLE site_variants (
  site_variant_id    INTEGER PRIMARY KEY,
  site_id            INTEGER NOT NULL REFERENCES world_sites(site_id) ON DELETE CASCADE,
  sector_path        TEXT NOT NULL,
  variant_name       TEXT NOT NULL,                  -- 'Interior','lockdown','final_loot'
  variant_id         TEXT NOT NULL DEFAULT '',       -- decimal uint32 as TEXT
  enabled_by_default INTEGER NOT NULL DEFAULT 0 CHECK (enabled_by_default IN (0,1)),
  node_ref           TEXT,
  UNIQUE (site_id, sector_path, variant_name, variant_id)
) STRICT;

CREATE INDEX idx_site_variants_site ON site_variants(site_id);

-- Supply / reinforcement / sightline graph between sites.
CREATE TABLE site_links (
  from_site_id INTEGER NOT NULL REFERENCES world_sites(site_id) ON DELETE CASCADE,
  to_site_id   INTEGER NOT NULL REFERENCES world_sites(site_id) ON DELETE CASCADE,
  link_kind    TEXT NOT NULL CHECK (link_kind IN
                 ('reinforcement','supply','escape_route','sightline','patrol_route')),
  weight       INTEGER NOT NULL DEFAULT 100 CHECK (weight BETWEEN 0 AND 1000),
  distance_m   REAL CHECK (distance_m IS NULL OR distance_m >= 0.0),
  PRIMARY KEY (from_site_id, to_site_id, link_kind),
  CHECK (from_site_id <> to_site_id)
) STRICT, WITHOUT ROWID;

-- ---------------------------------------------------------------------------
-- 5. Convenience views (read-only; no hidden writes)
-- ---------------------------------------------------------------------------

CREATE VIEW v_site_garrison AS
SELECT s.site_id, s.code, s.site_kind, s.sub_territory_id, s.default_faction_id,
       COUNT(DISTINCT c.site_community_id) AS communities,
       COUNT(DISTINCT e.entry_id)          AS roster,
       COUNT(DISTINCT e.entry_id) FILTER (WHERE e.role_hint IN ('officer','boss')) AS officers,
       COUNT(DISTINCT p.patrol_id)         AS patrols,
       COUNT(DISTINCT sp.spot_id)          AS spots,
       COUNT(DISTINCT d.device_id)         AS devices
FROM world_sites s
LEFT JOIN site_communities c        ON c.site_id = s.site_id
LEFT JOIN site_community_entries e  ON e.site_community_id = c.site_community_id
LEFT JOIN site_patrols p            ON p.site_id = s.site_id
LEFT JOIN site_spots sp             ON sp.site_id = s.site_id
LEFT JOIN site_devices d            ON d.site_id = s.site_id
GROUP BY s.site_id;

CREATE VIEW v_site_conversion_candidates AS
SELECT s.site_id, s.code, s.is_interior, su.suitability, su.score,
       s.tier, s.difficulty, s.default_faction_id
FROM world_sites s
JOIN site_suitabilities su ON su.site_id = s.site_id
WHERE su.suitability IN ('safehouse','chop_shop','netrunner_den','clinic',
                         'club','warehouse','branch_office')
ORDER BY su.score DESC, s.site_id;
