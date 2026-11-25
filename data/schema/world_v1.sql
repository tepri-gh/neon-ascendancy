-- Neon Ascendancy static world database schema (v1).
-- Single source of truth shared by tools/build-world-db.py, native/lib/store,
-- and offline native tests.
--
-- Coordinates are Cyberpunk 2077 world-space metres (Vector4 X/Y/Z, Z up).
-- Static IDs are permanent and never reused across mod versions.

PRAGMA application_id = 0x4E435744; -- 'NCWD'
PRAGMA user_version = 1;
PRAGMA foreign_keys = ON;

CREATE TABLE meta (
  key   TEXT PRIMARY KEY,
  value TEXT NOT NULL
) STRICT, WITHOUT ROWID;

CREATE TABLE districts (
  district_id       INTEGER PRIMARY KEY,
  code              TEXT NOT NULL UNIQUE,
  display_name      TEXT NOT NULL,
  kind              TEXT NOT NULL CHECK (kind IN ('city','badlands','dogtown')),
  gamedata_district TEXT NOT NULL UNIQUE,
  crime_multiplier  REAL NOT NULL DEFAULT 1.0 CHECK (crime_multiplier >= 0.0),
  bbox_min_x        REAL NOT NULL,
  bbox_min_y        REAL NOT NULL,
  bbox_max_x        REAL NOT NULL,
  bbox_max_y        REAL NOT NULL,
  CHECK (bbox_min_x < bbox_max_x AND bbox_min_y < bbox_max_y)
) STRICT;

CREATE TABLE factions (
  faction_id        INTEGER PRIMARY KEY,
  code              TEXT NOT NULL UNIQUE,
  display_name      TEXT NOT NULL,
  category          TEXT NOT NULL CHECK (category IN
                      ('gang','megacorp','fixer','civic','independent','player')),
  affiliation_enum  TEXT,                           -- NULL for synthetic factions (e.g. Night Corp)
  ticker            TEXT UNIQUE,                    -- NULL for non-market factions
  parent_faction_id INTEGER REFERENCES factions(faction_id),
  color_rgba        TEXT NOT NULL CHECK (length(color_rgba) = 9 AND substr(color_rgba, 1, 1) = '#'),
  income_multiplier REAL NOT NULL DEFAULT 1.0 CHECK (income_multiplier >= 0.0),
  hostility_bias    REAL NOT NULL DEFAULT 0.0,
  is_playable       INTEGER NOT NULL DEFAULT 0 CHECK (is_playable IN (0, 1))
) STRICT;
CREATE INDEX idx_factions_category ON factions(category);

CREATE TABLE sub_territories (
  sub_territory_id         INTEGER PRIMARY KEY,
  district_id              INTEGER NOT NULL REFERENCES districts(district_id),
  code                     TEXT NOT NULL UNIQUE,
  display_name             TEXT NOT NULL,
  gamedata_subdistrict     TEXT,                    -- vanilla sub-district enum name
  owner_kind               TEXT NOT NULL CHECK (owner_kind IN ('gang','corp','enclave','unclaimed')),
  initial_owner_faction_id INTEGER REFERENCES factions(faction_id),
  claim_strength           REAL NOT NULL DEFAULT 1.0 CHECK (claim_strength >= 0.0),
  base_income_per_cycle    INTEGER NOT NULL DEFAULT 0 CHECK (base_income_per_cycle >= 0),
  defense_rating           INTEGER NOT NULL DEFAULT 0 CHECK (defense_rating >= 0),
  area_m2                  REAL,
  centroid_x               REAL NOT NULL,
  centroid_y               REAL NOT NULL,
  centroid_z               REAL NOT NULL,
  UNIQUE (district_id, code)
) STRICT;
CREATE INDEX idx_sub_territories_district ON sub_territories(district_id);

CREATE TABLE landmarks (
  landmark_id      INTEGER PRIMARY KEY,
  code             TEXT NOT NULL UNIQUE,
  display_name     TEXT NOT NULL,
  kind             TEXT NOT NULL CHECK (kind IN
                     ('hq','compound','warehouse','clinic','shop','venue','asset','fixer','fast_travel')),
  sub_territory_id INTEGER REFERENCES sub_territories(sub_territory_id),
  gamedata_district TEXT,
  x                REAL NOT NULL,
  y                REAL NOT NULL,
  z                REAL NOT NULL,
  purchasable      INTEGER NOT NULL DEFAULT 0 CHECK (purchasable IN (0, 1)),
  base_price       INTEGER CHECK (base_price IS NULL OR base_price >= 0)
) STRICT;
CREATE INDEX idx_landmarks_territory ON landmarks(sub_territory_id);

CREATE TABLE control_centers (
  control_center_id INTEGER PRIMARY KEY,
  sub_territory_id  INTEGER NOT NULL REFERENCES sub_territories(sub_territory_id) ON DELETE CASCADE,
  code              TEXT NOT NULL UNIQUE,
  display_name      TEXT NOT NULL,
  landmark_id       INTEGER REFERENCES landmarks(landmark_id),
  x                 REAL NOT NULL,
  y                 REAL NOT NULL,
  z                 REAL NOT NULL,
  capture_radius_m  REAL NOT NULL DEFAULT 35.0 CHECK (capture_radius_m > 0.0),
  is_capital        INTEGER NOT NULL DEFAULT 0 CHECK (is_capital IN (0, 1)),
  -- 0 = dormant: kept for site/spawn links but not loaded into the sim or map.
  is_active         INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1))
) STRICT;
CREATE INDEX idx_control_centers_territory ON control_centers(sub_territory_id);

-- At most one headquarters per faction. Map marker only for now; not capturable.
CREATE TABLE faction_headquarters (
  faction_id           INTEGER PRIMARY KEY REFERENCES factions(faction_id),
  code                 TEXT NOT NULL UNIQUE,
  display_name         TEXT NOT NULL,
  gamedata_subdistrict TEXT,
  x                    REAL NOT NULL,
  y                    REAL NOT NULL,
  z                    REAL NOT NULL
) STRICT;

CREATE TABLE spawn_points (
  spawn_point_id     INTEGER PRIMARY KEY,
  control_center_id  INTEGER NOT NULL REFERENCES control_centers(control_center_id) ON DELETE CASCADE,
  sub_territory_id   INTEGER NOT NULL REFERENCES sub_territories(sub_territory_id),
  faction_id         INTEGER NOT NULL REFERENCES factions(faction_id),
  encounter_type     TEXT NOT NULL CHECK (encounter_type IN
                       ('guard','patrol','ambush','camp','vehicle','sniper','civilian','community')),
  community_hash     TEXT,
  community_template TEXT,
  x                  REAL NOT NULL,
  y                  REAL NOT NULL,
  z                  REAL NOT NULL,
  yaw                REAL,
  spawn_weight       INTEGER NOT NULL DEFAULT 100 CHECK (spawn_weight >= 0),
  min_era            TEXT NOT NULL DEFAULT 'any' CHECK (min_era IN ('any','act1','act2','postgame','dogtown')),
  max_era            TEXT NOT NULL DEFAULT 'any' CHECK (max_era IN ('any','act1','act2','postgame','dogtown'))
) STRICT;
CREATE INDEX idx_spawn_points_center  ON spawn_points(control_center_id);
CREATE INDEX idx_spawn_points_faction ON spawn_points(faction_id);

-- Boot-loaded ownership grid: O(1) point -> sub_territory_id lookup in RAM.
CREATE TABLE territory_cells (
  level            INTEGER NOT NULL CHECK (level BETWEEN 0 AND 3),
  cell_x           INTEGER NOT NULL,
  cell_y           INTEGER NOT NULL,
  sub_territory_id INTEGER NOT NULL REFERENCES sub_territories(sub_territory_id) ON DELETE CASCADE,
  PRIMARY KEY (level, cell_x, cell_y)
) STRICT, WITHOUT ROWID;

-- Pre-partitioned map overlay geometry (for Step 0.5 / v0.2.0 inkShape overlay).
CREATE TABLE territory_cell_polygons (
  sub_territory_id INTEGER NOT NULL REFERENCES sub_territories(sub_territory_id) ON DELETE CASCADE,
  ring_index       INTEGER NOT NULL,
  ring_kind        TEXT NOT NULL CHECK (ring_kind IN ('outer','hole')),
  point_index      INTEGER NOT NULL,
  x                REAL NOT NULL,
  y                REAL NOT NULL,
  PRIMARY KEY (sub_territory_id, ring_index, point_index)
) STRICT, WITHOUT ROWID;

-- 2D bounding-box spatial prefilters (exact Z / 3D checks live in C++).
CREATE VIRTUAL TABLE sub_territory_rtree USING rtree(id, min_x, max_x, min_y, max_y);
CREATE VIRTUAL TABLE landmark_rtree      USING rtree(id, min_x, max_x, min_y, max_y);
CREATE VIRTUAL TABLE spawn_point_rtree   USING rtree(id, min_x, max_x, min_y, max_y);

-- Deferred: Road-Chunk Vehicle Transit Ledger spatial scaffolding (ships empty).
CREATE TABLE road_chunks (
  chunk_id      INTEGER PRIMARY KEY,
  district_id   INTEGER REFERENCES districts(district_id),
  grid_x        INTEGER NOT NULL,
  grid_y        INTEGER NOT NULL,
  grid_z        INTEGER NOT NULL,
  lane_count    INTEGER NOT NULL DEFAULT 0,
  navmesh_ready INTEGER NOT NULL DEFAULT 0 CHECK (navmesh_ready IN (0, 1)),
  UNIQUE (grid_x, grid_y, grid_z)
) STRICT;
CREATE VIRTUAL TABLE road_chunk_rtree USING rtree(id, min_x, max_x, min_y, max_y);

CREATE TABLE road_nodes (
  node_id  INTEGER PRIMARY KEY,
  chunk_id INTEGER NOT NULL REFERENCES road_chunks(chunk_id),
  x        REAL NOT NULL,
  y        REAL NOT NULL,
  z        REAL NOT NULL,
  lane     INTEGER NOT NULL DEFAULT 0
) STRICT;
CREATE INDEX idx_road_nodes_chunk ON road_nodes(chunk_id);

CREATE TABLE road_edges (
  edge_id      INTEGER PRIMARY KEY,
  from_node_id INTEGER NOT NULL REFERENCES road_nodes(node_id),
  to_node_id   INTEGER NOT NULL REFERENCES road_nodes(node_id),
  chunk_id     INTEGER NOT NULL REFERENCES road_chunks(chunk_id),
  length_m     REAL NOT NULL CHECK (length_m > 0.0),
  speed_kph    REAL,
  is_tunnel    INTEGER NOT NULL DEFAULT 0 CHECK (is_tunnel IN (0, 1))
) STRICT;
CREATE INDEX idx_road_edges_chunk ON road_edges(chunk_id);
CREATE INDEX idx_road_edges_from  ON road_edges(from_node_id);
