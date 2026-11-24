-- Neon Ascendancy dynamic per-playthrough database schema (v1).
-- Single source of truth shared by native/lib/store and offline native tests.
--
-- Static faction IDs from world.db occupy [1, 999]; runtime player organizations
-- allocate faction_id >= 1000. All *_seconds columns store absolute GameTime
-- seconds (never wall-clock or frame counts).

PRAGMA journal_mode = WAL;
PRAGMA synchronous  = NORMAL;
PRAGMA foreign_keys = ON;
PRAGMA user_version = 1;
PRAGMA application_id = 0x4E435750; -- 'NCWP'

CREATE TABLE meta (
  key   TEXT PRIMARY KEY,
  value TEXT NOT NULL
) STRICT, WITHOUT ROWID;

CREATE TABLE sim_clock (
  singleton          INTEGER PRIMARY KEY CHECK (singleton = 1),
  playthrough_id_hi  INTEGER NOT NULL,
  playthrough_id_lo  INTEGER NOT NULL,
  revision           INTEGER NOT NULL DEFAULT 0,   -- highest durable revision
  last_cycle_seconds INTEGER NOT NULL DEFAULT 0,   -- absolute GameTime seconds
  cycle_index        INTEGER NOT NULL DEFAULT 0,
  rng_seed           INTEGER NOT NULL,
  rng_counter        INTEGER NOT NULL DEFAULT 0,
  world_content_hash TEXT NOT NULL
) STRICT;

-- Durable checkpoint log: restore = newest 'full' <= R, then deltas in (C, R].
CREATE TABLE checkpoints (
  revision       INTEGER PRIMARY KEY,
  kind           TEXT NOT NULL CHECK (kind IN ('full','delta')),
  base_revision  INTEGER,
  format_version INTEGER NOT NULL,
  row_count      INTEGER NOT NULL,
  payload        BLOB NOT NULL,
  byte_size      INTEGER NOT NULL,
  created_utc    INTEGER NOT NULL,
  pinned         INTEGER NOT NULL DEFAULT 0 CHECK (pinned IN (0, 1))
) STRICT;

CREATE TABLE territory_state (
  sub_territory_id        INTEGER PRIMARY KEY,
  owner_faction_id        INTEGER NOT NULL,
  holder_faction_id       INTEGER,
  contested_by_faction_id INTEGER,
  control_level           REAL NOT NULL DEFAULT 1.0 CHECK (control_level BETWEEN 0.0 AND 1.0),
  heat                    REAL NOT NULL DEFAULT 0.0 CHECK (heat >= 0.0),
  last_flip_revision      INTEGER NOT NULL DEFAULT 0,
  last_flip_seconds       INTEGER NOT NULL DEFAULT 0
) STRICT;

CREATE TABLE org_state (
  org_id           INTEGER PRIMARY KEY,
  kind             TEXT NOT NULL CHECK (kind IN ('gang','corporation')),
  display_name     TEXT NOT NULL,
  faction_id       INTEGER NOT NULL UNIQUE,
  treasury_eddies  INTEGER NOT NULL DEFAULT 0 CHECK (treasury_eddies >= 0),
  notoriety        REAL NOT NULL DEFAULT 0.0,
  heat             REAL NOT NULL DEFAULT 0.0,
  upkeep_per_cycle INTEGER NOT NULL DEFAULT 0,
  founded_revision INTEGER NOT NULL DEFAULT 0,
  founded_seconds  INTEGER NOT NULL DEFAULT 0
) STRICT;

CREATE TABLE org_assets (
  asset_id          INTEGER PRIMARY KEY,
  org_id            INTEGER NOT NULL REFERENCES org_state(org_id) ON DELETE CASCADE,
  landmark_id       INTEGER,
  kind              TEXT NOT NULL,
  purchase_price    INTEGER NOT NULL DEFAULT 0,
  upkeep_per_cycle  INTEGER NOT NULL DEFAULT 0,
  acquired_revision INTEGER NOT NULL DEFAULT 0
) STRICT;
CREATE INDEX idx_org_assets_org ON org_assets(org_id);

CREATE TABLE missions (
  mission_id        INTEGER PRIMARY KEY,
  kind              TEXT NOT NULL CHECK (kind IN ('combat','economic','espionage')),
  state             TEXT NOT NULL CHECK (state IN
                      ('offered','active','succeeded','failed','expired')),
  issuer_faction_id INTEGER,
  target_faction_id INTEGER,
  sub_territory_id  INTEGER,
  control_center_id INTEGER,
  seed              INTEGER NOT NULL,
  difficulty        REAL NOT NULL DEFAULT 1.0,
  reward_eddies     INTEGER NOT NULL DEFAULT 0,
  created_seconds   INTEGER NOT NULL,
  deadline_seconds  INTEGER,
  resolved_seconds  INTEGER,
  resolved_revision INTEGER
) STRICT;
CREATE INDEX idx_missions_state     ON missions(state, kind);
CREATE INDEX idx_missions_territory ON missions(sub_territory_id, state);

CREATE TABLE event_log (
  revision     INTEGER NOT NULL,
  seq          INTEGER NOT NULL,
  event_type   TEXT NOT NULL,
  game_seconds INTEGER NOT NULL,
  payload      BLOB,
  PRIMARY KEY (revision, seq)
) STRICT, WITHOUT ROWID;
CREATE INDEX idx_event_log_type ON event_log(event_type, revision);

-- Deferred: Road-Chunk Vehicle Transit Ledger (created now, populated later).
CREATE TABLE transit_ledger (
  transit_id     INTEGER NOT NULL,
  seq            INTEGER NOT NULL,
  faction_id     INTEGER,
  vehicle_record TEXT,
  route_id       INTEGER,
  chunk_id       INTEGER NOT NULL,
  t_enter        INTEGER NOT NULL,
  t_exit         INTEGER NOT NULL,
  state          TEXT NOT NULL CHECK (state IN
                   ('scheduled','active','materialized','done','aborted')),
  PRIMARY KEY (transit_id, seq)
) STRICT, WITHOUT ROWID;
CREATE INDEX idx_transit_window ON transit_ledger(chunk_id, t_enter, t_exit);
