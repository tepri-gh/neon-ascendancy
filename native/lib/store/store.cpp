#include "store.hpp"

#include <sqlite3.h>

#include <algorithm>
#include <cmath>
#include <cstring>
#include <ctime>
#include <random>

#include "embedded_schemas.hpp"

namespace neon::store {

namespace {

constexpr uint16_t kPayloadMagic = 0x4E43; // 'NC'

uint32_t ComputeCrc32(const uint8_t* data, size_t len) {
  uint32_t crc = 0xFFFFFFFFU;
  for (size_t i = 0; i < len; ++i) {
    crc ^= static_cast<uint32_t>(data[i]);
    for (int bit = 0; bit < 8; ++bit) {
      const uint32_t mask = -(crc & 1U);
      crc = (crc >> 1U) ^ (0xEDB88320U & mask);
    }
  }
  return ~crc;
}

class BinaryWriter {
 public:
  void PutU8(uint8_t v) { buf_.push_back(v); }
  void PutU16(uint16_t v) {
    buf_.push_back(static_cast<uint8_t>(v & 0xFFU));
    buf_.push_back(static_cast<uint8_t>((v >> 8U) & 0xFFU));
  }
  void PutU32(uint32_t v) {
    for (int i = 0; i < 4; ++i) {
      buf_.push_back(static_cast<uint8_t>((v >> (i * 8)) & 0xFFU));
    }
  }
  void PutU64(uint64_t v) {
    for (int i = 0; i < 8; ++i) {
      buf_.push_back(static_cast<uint8_t>((v >> (i * 8)) & 0xFFU));
    }
  }
  void PutI32(int32_t v) { PutU32(static_cast<uint32_t>(v)); }
  void PutI64(int64_t v) { PutU64(static_cast<uint64_t>(v)); }
  void PutF32(float v) {
    uint32_t bits = 0;
    std::memcpy(&bits, &v, sizeof(bits));
    PutU32(bits);
  }
  void PutString(const std::string& s) {
    PutU16(static_cast<uint16_t>(std::min<size_t>(s.size(), 65535)));
    buf_.insert(buf_.end(), s.begin(), s.begin() + std::min<size_t>(s.size(), 65535));
  }
  void AppendFooterCrc() {
    const uint32_t crc = ComputeCrc32(buf_.data(), buf_.size());
    PutU32(crc);
  }
  std::vector<uint8_t> Take() { return std::move(buf_); }

 private:
  std::vector<uint8_t> buf_;
};

class BinaryReader {
 public:
  BinaryReader(const uint8_t* data, size_t len) : data_(data), len_(len) {}

  bool GetU8(uint8_t& out) {
    if (pos_ + 1 > len_) return false;
    out = data_[pos_++];
    return true;
  }
  bool GetU16(uint16_t& out) {
    if (pos_ + 2 > len_) return false;
    out = static_cast<uint16_t>(data_[pos_]) | (static_cast<uint16_t>(data_[pos_ + 1]) << 8U);
    pos_ += 2;
    return true;
  }
  bool GetU32(uint32_t& out) {
    if (pos_ + 4 > len_) return false;
    out = 0;
    for (int i = 0; i < 4; ++i) {
      out |= static_cast<uint32_t>(data_[pos_ + i]) << (i * 8);
    }
    pos_ += 4;
    return true;
  }
  bool GetU64(uint64_t& out) {
    if (pos_ + 8 > len_) return false;
    out = 0;
    for (int i = 0; i < 8; ++i) {
      out |= static_cast<uint64_t>(data_[pos_ + i]) << (i * 8);
    }
    pos_ += 8;
    return true;
  }
  bool GetI32(int32_t& out) {
    uint32_t u = 0;
    if (!GetU32(u)) return false;
    out = static_cast<int32_t>(u);
    return true;
  }
  bool GetI64(int64_t& out) {
    uint64_t u = 0;
    if (!GetU64(u)) return false;
    out = static_cast<int64_t>(u);
    return true;
  }
  bool GetF32(float& out) {
    uint32_t bits = 0;
    if (!GetU32(bits)) return false;
    std::memcpy(&out, &bits, sizeof(out));
    return true;
  }
  bool GetString(std::string& out) {
    uint16_t n = 0;
    if (!GetU16(n) || pos_ + n > len_) return false;
    out.assign(reinterpret_cast<const char*>(data_ + pos_), n);
    pos_ += n;
    return true;
  }

 private:
  const uint8_t* data_;
  size_t len_;
  size_t pos_ = 0;
};

struct StmtGuard {
  sqlite3_stmt* stmt = nullptr;
  ~StmtGuard() {
    if (stmt != nullptr) {
      sqlite3_finalize(stmt);
    }
  }
};

std::string ColText(sqlite3_stmt* stmt, int col) {
  const unsigned char* p = sqlite3_column_text(stmt, col);
  return p != nullptr ? std::string(reinterpret_cast<const char*>(p)) : std::string();
}

const char* OrgKindStr(sim::OrgKind k) {
  return k == sim::OrgKind::Corporation ? "corporation" : "gang";
}

const char* MissionKindStr(sim::MissionKind k) {
  switch (k) {
    case sim::MissionKind::Combat: return "combat";
    case sim::MissionKind::Economic: return "economic";
    case sim::MissionKind::Espionage: return "espionage";
  }
  return "combat";
}

const char* MissionStateStr(sim::MissionState s) {
  switch (s) {
    case sim::MissionState::Offered: return "offered";
    case sim::MissionState::Active: return "active";
    case sim::MissionState::Succeeded: return "succeeded";
    case sim::MissionState::Failed: return "failed";
    case sim::MissionState::Expired: return "expired";
  }
  return "offered";
}

const char* EventTypeStr(sim::SimEventType t) {
  switch (t) {
    case sim::SimEventType::OrgFounded: return "OrgFounded";
    case sim::SimEventType::MissionOffered: return "MissionOffered";
    case sim::SimEventType::MissionCompleted: return "MissionCompleted";
    case sim::SimEventType::MissionFailed: return "MissionFailed";
    case sim::SimEventType::TerritoryOwnerChanged: return "TerritoryOwnerChanged";
    case sim::SimEventType::HeatChanged: return "HeatChanged";
    case sim::SimEventType::IncomeSettled: return "IncomeSettled";
    case sim::SimEventType::CycleElapsed: return "CycleElapsed";
  }
  return "Unknown";
}

bool ExecSql(sqlite3* db, const char* sql, std::string& err) {
  char* msg = nullptr;
  const int rc = sqlite3_exec(db, sql, nullptr, nullptr, &msg);
  if (rc != SQLITE_OK) {
    err = msg != nullptr ? msg : sqlite3_errmsg(db);
    if (msg != nullptr) {
      sqlite3_free(msg);
    }
    return false;
  }
  return true;
}

} // namespace

// --- WorldDb ----------------------------------------------------------------

WorldDb::~WorldDb() { Close(); }

void WorldDb::Close() {
  if (db_ != nullptr) {
    sqlite3_close(db_);
    db_ = nullptr;
  }
  content_hash_.clear();
  sub_territories_.clear();
  control_centers_.clear();
  cell_grid_.clear();
}

uint64_t WorldDb::PackCellKey(int32_t cx, int32_t cy) {
  return (static_cast<uint64_t>(static_cast<uint32_t>(cx)) << 32U) |
         static_cast<uint64_t>(static_cast<uint32_t>(cy));
}

bool WorldDb::Open(const std::string& path, bool immutable, std::string& err) {
  Close();
  std::string uri = "file:" + path;
  if (immutable) {
    uri += "?immutable=1";
  }
  const int flags = SQLITE_OPEN_READONLY | SQLITE_OPEN_URI;
  if (sqlite3_open_v2(uri.c_str(), &db_, flags, nullptr) != SQLITE_OK) {
    err = db_ != nullptr ? sqlite3_errmsg(db_) : "failed to allocate sqlite3 handle";
    Close();
    return false;
  }
  if (!ExecSql(db_, "PRAGMA query_only = ON;", err)) {
    Close();
    return false;
  }

  // Load meta
  {
    StmtGuard g;
    if (sqlite3_prepare_v2(db_, "SELECT key, value FROM meta", -1, &g.stmt, nullptr) != SQLITE_OK) {
      err = sqlite3_errmsg(db_);
      Close();
      return false;
    }
    while (sqlite3_step(g.stmt) == SQLITE_ROW) {
      const std::string k = ColText(g.stmt, 0);
      const std::string v = ColText(g.stmt, 1);
      if (k == "content_hash") {
        content_hash_ = v;
      } else if (k == "cell_size_m") {
        cell_size_m_ = std::stod(v);
      }
    }
  }

  // Load sub_territories
  {
    StmtGuard g;
    const char* sql =
        "SELECT sub_territory_id, district_id, code, display_name, owner_kind, "
        "COALESCE(initial_owner_faction_id, 0), base_income_per_cycle, defense_rating, "
        "centroid_x, centroid_y, centroid_z "
        "FROM sub_territories ORDER BY sub_territory_id";
    if (sqlite3_prepare_v2(db_, sql, -1, &g.stmt, nullptr) != SQLITE_OK) {
      err = sqlite3_errmsg(db_);
      Close();
      return false;
    }
    while (sqlite3_step(g.stmt) == SQLITE_ROW) {
      WorldSubTerritory st;
      st.sub_territory_id = sqlite3_column_int(g.stmt, 0);
      st.district_id = sqlite3_column_int(g.stmt, 1);
      st.code = ColText(g.stmt, 2);
      st.display_name = ColText(g.stmt, 3);
      st.owner_kind = ColText(g.stmt, 4);
      st.initial_owner_faction_id = sqlite3_column_int(g.stmt, 5);
      st.base_income_per_cycle = sqlite3_column_int(g.stmt, 6);
      st.defense_rating = sqlite3_column_int(g.stmt, 7);
      st.centroid_x = sqlite3_column_double(g.stmt, 8);
      st.centroid_y = sqlite3_column_double(g.stmt, 9);
      st.centroid_z = sqlite3_column_double(g.stmt, 10);
      sub_territories_.push_back(std::move(st));
    }
  }

  // Load control_centers
  {
    StmtGuard g;
    const char* sql =
        "SELECT control_center_id, sub_territory_id, code, display_name, x, y, z, capture_radius_m "
        "FROM control_centers ORDER BY control_center_id";
    if (sqlite3_prepare_v2(db_, sql, -1, &g.stmt, nullptr) != SQLITE_OK) {
      err = sqlite3_errmsg(db_);
      Close();
      return false;
    }
    while (sqlite3_step(g.stmt) == SQLITE_ROW) {
      WorldControlCenter cc;
      cc.control_center_id = sqlite3_column_int(g.stmt, 0);
      cc.sub_territory_id = sqlite3_column_int(g.stmt, 1);
      cc.code = ColText(g.stmt, 2);
      cc.display_name = ColText(g.stmt, 3);
      cc.x = sqlite3_column_double(g.stmt, 4);
      cc.y = sqlite3_column_double(g.stmt, 5);
      cc.z = sqlite3_column_double(g.stmt, 6);
      cc.capture_radius_m = sqlite3_column_double(g.stmt, 7);
      control_centers_.push_back(std::move(cc));
    }
  }

  // Boot-load level-0 ownership grid into RAM for O(1) lookup.
  {
    StmtGuard g;
    if (sqlite3_prepare_v2(
            db_, "SELECT cell_x, cell_y, sub_territory_id FROM territory_cells WHERE level = 0",
            -1, &g.stmt, nullptr) != SQLITE_OK) {
      err = sqlite3_errmsg(db_);
      Close();
      return false;
    }
    while (sqlite3_step(g.stmt) == SQLITE_ROW) {
      const int32_t cx = sqlite3_column_int(g.stmt, 0);
      const int32_t cy = sqlite3_column_int(g.stmt, 1);
      const int32_t stid = sqlite3_column_int(g.stmt, 2);
      cell_grid_[PackCellKey(cx, cy)] = stid;
    }
  }

  return !sub_territories_.empty();
}

std::vector<sim::TerritoryDef> WorldDb::BuildTerritoryDefs() const {
  std::vector<sim::TerritoryDef> out;
  out.reserve(sub_territories_.size());
  for (const auto& st : sub_territories_) {
    out.push_back(sim::TerritoryDef{
        st.sub_territory_id,
        st.district_id,
        st.initial_owner_faction_id,
        st.base_income_per_cycle,
        st.defense_rating,
    });
  }
  return out;
}

int32_t WorldDb::LookupSubTerritoryAt(double x, double y) const {
  if (cell_size_m_ <= 0.0) {
    return 0;
  }
  const int32_t cx = static_cast<int32_t>(std::floor(x / cell_size_m_));
  const int32_t cy = static_cast<int32_t>(std::floor(y / cell_size_m_));
  const auto it = cell_grid_.find(PackCellKey(cx, cy));
  return it != cell_grid_.end() ? it->second : 0;
}

std::vector<int32_t> WorldDb::QuerySpawnPointsNear(
    double x, double y, double z, double radius_m) const {
  std::vector<int32_t> out;
  if (db_ == nullptr || radius_m <= 0.0) {
    return out;
  }
  StmtGuard g;
  const char* sql =
      "SELECT sp.spawn_point_id, sp.x, sp.y, sp.z "
      "FROM spawn_point_rtree rt "
      "JOIN spawn_points sp ON sp.spawn_point_id = rt.id "
      "WHERE rt.min_x <= ?1 AND rt.max_x >= ?2 AND rt.min_y <= ?3 AND rt.max_y >= ?4";
  if (sqlite3_prepare_v2(db_, sql, -1, &g.stmt, nullptr) != SQLITE_OK) {
    return out;
  }
  sqlite3_bind_double(g.stmt, 1, x + radius_m);
  sqlite3_bind_double(g.stmt, 2, x - radius_m);
  sqlite3_bind_double(g.stmt, 3, y + radius_m);
  sqlite3_bind_double(g.stmt, 4, y - radius_m);
  const double r2 = radius_m * radius_m;
  while (sqlite3_step(g.stmt) == SQLITE_ROW) {
    const double dx = sqlite3_column_double(g.stmt, 1) - x;
    const double dy = sqlite3_column_double(g.stmt, 2) - y;
    const double dz = sqlite3_column_double(g.stmt, 3) - z;
    if ((dx * dx + dy * dy + dz * dz) <= r2) {
      out.push_back(sqlite3_column_int(g.stmt, 0));
    }
  }
  return out;
}

// --- PlaythroughDb ----------------------------------------------------------

PlaythroughDb::~PlaythroughDb() { Close(true); }

bool PlaythroughDb::Close(bool truncate_wal) {
  if (db_ == nullptr) {
    return true;
  }
  if (truncate_wal && !read_only_fallback_) {
    sqlite3_wal_checkpoint_v2(db_, nullptr, SQLITE_CHECKPOINT_TRUNCATE, nullptr, nullptr);
  }
  const int rc = sqlite3_close(db_);
  db_ = nullptr;
  return rc == SQLITE_OK;
}

std::vector<uint8_t> PlaythroughDb::EncodeFullSnapshot(const sim::SimState& state) {
  BinaryWriter w;
  w.PutU16(kPayloadMagic);
  w.PutU16(kPayloadFormatVersion);
  const uint32_t total_rows = static_cast<uint32_t>(
      1 + state.territories.size() + state.orgs.size() + state.missions.size());
  w.PutU32(total_rows);

  // Clock
  w.PutI32(state.clock.revision);
  w.PutI32(state.clock.last_cycle_seconds);
  w.PutI32(state.clock.cycle_index);
  w.PutU64(state.clock.rng_seed);
  w.PutU64(state.clock.rng_counter);

  // Territories
  w.PutU32(static_cast<uint32_t>(state.territories.size()));
  for (const auto& t : state.territories) {
    w.PutI32(t.sub_territory_id);
    w.PutI32(t.owner_faction_id);
    w.PutI32(t.holder_faction_id);
    w.PutI32(t.contested_by_faction_id);
    w.PutF32(t.control_level);
    w.PutF32(t.heat);
    w.PutI32(t.last_flip_revision);
    w.PutI32(t.last_flip_seconds);
  }

  // Orgs
  w.PutU32(static_cast<uint32_t>(state.orgs.size()));
  for (const auto& o : state.orgs) {
    w.PutI32(o.org_id);
    w.PutU8(static_cast<uint8_t>(o.kind));
    w.PutString(o.display_name);
    w.PutI32(o.faction_id);
    w.PutI64(o.treasury_eddies);
    w.PutF32(o.notoriety);
    w.PutF32(o.heat);
    w.PutI32(o.upkeep_per_cycle);
    w.PutI32(o.founded_revision);
    w.PutI32(o.founded_seconds);
  }

  // Missions
  w.PutU32(static_cast<uint32_t>(state.missions.size()));
  for (const auto& m : state.missions) {
    w.PutI32(m.mission_id);
    w.PutU8(static_cast<uint8_t>(m.kind));
    w.PutU8(static_cast<uint8_t>(m.state));
    w.PutI32(m.issuer_faction_id);
    w.PutI32(m.target_faction_id);
    w.PutI32(m.sub_territory_id);
    w.PutI32(m.control_center_id);
    w.PutU64(m.seed);
    w.PutF32(m.difficulty);
    w.PutI32(m.reward_eddies);
    w.PutI32(m.created_seconds);
    w.PutI32(m.deadline_seconds);
    w.PutI32(m.resolved_seconds);
    w.PutI32(m.resolved_revision);
  }

  w.AppendFooterCrc();
  return w.Take();
}

bool PlaythroughDb::DecodeFullSnapshot(const std::vector<uint8_t>& blob, sim::SimState& out_state) {
  if (blob.size() < 12) {
    return false;
  }
  const size_t body_len = blob.size() - 4;
  uint32_t expected_crc = 0;
  {
    BinaryReader crc_reader(blob.data() + body_len, 4);
    if (!crc_reader.GetU32(expected_crc)) {
      return false;
    }
  }
  if (ComputeCrc32(blob.data(), body_len) != expected_crc) {
    return false;
  }

  BinaryReader r(blob.data(), body_len);
  uint16_t magic = 0;
  uint16_t ver = 0;
  uint32_t total_rows = 0;
  if (!r.GetU16(magic) || !r.GetU16(ver) || !r.GetU32(total_rows)) {
    return false;
  }
  if (magic != kPayloadMagic || ver != kPayloadFormatVersion) {
    return false;
  }

  sim::SimState st;
  if (!r.GetI32(st.clock.revision) || !r.GetI32(st.clock.last_cycle_seconds) ||
      !r.GetI32(st.clock.cycle_index) || !r.GetU64(st.clock.rng_seed) ||
      !r.GetU64(st.clock.rng_counter)) {
    return false;
  }

  uint32_t n_terr = 0;
  if (!r.GetU32(n_terr)) return false;
  st.territories.resize(n_terr);
  for (uint32_t i = 0; i < n_terr; ++i) {
    auto& t = st.territories[i];
    if (!r.GetI32(t.sub_territory_id) || !r.GetI32(t.owner_faction_id) ||
        !r.GetI32(t.holder_faction_id) || !r.GetI32(t.contested_by_faction_id) ||
        !r.GetF32(t.control_level) || !r.GetF32(t.heat) ||
        !r.GetI32(t.last_flip_revision) || !r.GetI32(t.last_flip_seconds)) {
      return false;
    }
  }

  uint32_t n_orgs = 0;
  if (!r.GetU32(n_orgs)) return false;
  st.orgs.resize(n_orgs);
  for (uint32_t i = 0; i < n_orgs; ++i) {
    auto& o = st.orgs[i];
    uint8_t kind = 0;
    if (!r.GetI32(o.org_id) || !r.GetU8(kind) || !r.GetString(o.display_name) ||
        !r.GetI32(o.faction_id) || !r.GetI64(o.treasury_eddies) || !r.GetF32(o.notoriety) ||
        !r.GetF32(o.heat) || !r.GetI32(o.upkeep_per_cycle) ||
        !r.GetI32(o.founded_revision) || !r.GetI32(o.founded_seconds)) {
      return false;
    }
    o.kind = static_cast<sim::OrgKind>(kind);
  }

  uint32_t n_missions = 0;
  if (!r.GetU32(n_missions)) return false;
  st.missions.resize(n_missions);
  for (uint32_t i = 0; i < n_missions; ++i) {
    auto& m = st.missions[i];
    uint8_t kind = 0;
    uint8_t mstate = 0;
    if (!r.GetI32(m.mission_id) || !r.GetU8(kind) || !r.GetU8(mstate) ||
        !r.GetI32(m.issuer_faction_id) || !r.GetI32(m.target_faction_id) ||
        !r.GetI32(m.sub_territory_id) || !r.GetI32(m.control_center_id) ||
        !r.GetU64(m.seed) || !r.GetF32(m.difficulty) || !r.GetI32(m.reward_eddies) ||
        !r.GetI32(m.created_seconds) || !r.GetI32(m.deadline_seconds) ||
        !r.GetI32(m.resolved_seconds) || !r.GetI32(m.resolved_revision)) {
      return false;
    }
    m.kind = static_cast<sim::MissionKind>(kind);
    m.state = static_cast<sim::MissionState>(mstate);
  }

  out_state = std::move(st);
  return true;
}

int32_t PlaythroughDb::MaxCheckpointRevision() const {
  if (db_ == nullptr) return -1;
  StmtGuard g;
  if (sqlite3_prepare_v2(db_, "SELECT COALESCE(MAX(revision), -1) FROM checkpoints", -1, &g.stmt, nullptr) != SQLITE_OK) {
    return -1;
  }
  return sqlite3_step(g.stmt) == SQLITE_ROW ? sqlite3_column_int(g.stmt, 0) : -1;
}

bool PlaythroughDb::ApplyLiveTables(const sim::SimState& state, std::string& err) {
  if (!ExecSql(db_, "DELETE FROM territory_state; DELETE FROM org_state; DELETE FROM missions;", err)) {
    return false;
  }
  {
    StmtGuard g;
    const char* sql =
        "UPDATE sim_clock SET revision = ?1, last_cycle_seconds = ?2, cycle_index = ?3, "
        "rng_seed = ?4, rng_counter = ?5 WHERE singleton = 1";
    if (sqlite3_prepare_v2(db_, sql, -1, &g.stmt, nullptr) != SQLITE_OK) {
      err = sqlite3_errmsg(db_);
      return false;
    }
    sqlite3_bind_int(g.stmt, 1, state.clock.revision);
    sqlite3_bind_int(g.stmt, 2, state.clock.last_cycle_seconds);
    sqlite3_bind_int(g.stmt, 3, state.clock.cycle_index);
    sqlite3_bind_int64(g.stmt, 4, static_cast<sqlite3_int64>(state.clock.rng_seed));
    sqlite3_bind_int64(g.stmt, 5, static_cast<sqlite3_int64>(state.clock.rng_counter));
    if (sqlite3_step(g.stmt) != SQLITE_DONE) {
      err = sqlite3_errmsg(db_);
      return false;
    }
  }
  {
    StmtGuard g;
    const char* sql =
        "INSERT INTO territory_state(sub_territory_id, owner_faction_id, holder_faction_id, "
        "contested_by_faction_id, control_level, heat, last_flip_revision, last_flip_seconds) "
        "VALUES(?1,?2,?3,?4,?5,?6,?7,?8)";
    if (sqlite3_prepare_v2(db_, sql, -1, &g.stmt, nullptr) != SQLITE_OK) {
      err = sqlite3_errmsg(db_);
      return false;
    }
    for (const auto& t : state.territories) {
      sqlite3_reset(g.stmt);
      sqlite3_bind_int(g.stmt, 1, t.sub_territory_id);
      sqlite3_bind_int(g.stmt, 2, t.owner_faction_id);
      if (t.holder_faction_id != 0) sqlite3_bind_int(g.stmt, 3, t.holder_faction_id);
      else sqlite3_bind_null(g.stmt, 3);
      if (t.contested_by_faction_id != 0) sqlite3_bind_int(g.stmt, 4, t.contested_by_faction_id);
      else sqlite3_bind_null(g.stmt, 4);
      sqlite3_bind_double(g.stmt, 5, t.control_level);
      sqlite3_bind_double(g.stmt, 6, t.heat);
      sqlite3_bind_int(g.stmt, 7, t.last_flip_revision);
      sqlite3_bind_int(g.stmt, 8, t.last_flip_seconds);
      if (sqlite3_step(g.stmt) != SQLITE_DONE) {
        err = sqlite3_errmsg(db_);
        return false;
      }
    }
  }
  {
    StmtGuard g;
    const char* sql =
        "INSERT INTO org_state(org_id, kind, display_name, faction_id, treasury_eddies, "
        "notoriety, heat, upkeep_per_cycle, founded_revision, founded_seconds) "
        "VALUES(?1,?2,?3,?4,?5,?6,?7,?8,?9,?10)";
    if (sqlite3_prepare_v2(db_, sql, -1, &g.stmt, nullptr) != SQLITE_OK) {
      err = sqlite3_errmsg(db_);
      return false;
    }
    for (const auto& o : state.orgs) {
      sqlite3_reset(g.stmt);
      sqlite3_bind_int(g.stmt, 1, o.org_id);
      sqlite3_bind_text(g.stmt, 2, OrgKindStr(o.kind), -1, SQLITE_STATIC);
      sqlite3_bind_text(g.stmt, 3, o.display_name.c_str(), -1, SQLITE_TRANSIENT);
      sqlite3_bind_int(g.stmt, 4, o.faction_id);
      sqlite3_bind_int64(g.stmt, 5, o.treasury_eddies);
      sqlite3_bind_double(g.stmt, 6, o.notoriety);
      sqlite3_bind_double(g.stmt, 7, o.heat);
      sqlite3_bind_int(g.stmt, 8, o.upkeep_per_cycle);
      sqlite3_bind_int(g.stmt, 9, o.founded_revision);
      sqlite3_bind_int(g.stmt, 10, o.founded_seconds);
      if (sqlite3_step(g.stmt) != SQLITE_DONE) {
        err = sqlite3_errmsg(db_);
        return false;
      }
    }
  }
  {
    StmtGuard g;
    const char* sql =
        "INSERT INTO missions(mission_id, kind, state, issuer_faction_id, target_faction_id, "
        "sub_territory_id, control_center_id, seed, difficulty, reward_eddies, "
        "created_seconds, deadline_seconds, resolved_seconds, resolved_revision) "
        "VALUES(?1,?2,?3,?4,?5,?6,?7,?8,?9,?10,?11,?12,?13,?14)";
    if (sqlite3_prepare_v2(db_, sql, -1, &g.stmt, nullptr) != SQLITE_OK) {
      err = sqlite3_errmsg(db_);
      return false;
    }
    for (const auto& m : state.missions) {
      sqlite3_reset(g.stmt);
      sqlite3_bind_int(g.stmt, 1, m.mission_id);
      sqlite3_bind_text(g.stmt, 2, MissionKindStr(m.kind), -1, SQLITE_STATIC);
      sqlite3_bind_text(g.stmt, 3, MissionStateStr(m.state), -1, SQLITE_STATIC);
      sqlite3_bind_int(g.stmt, 4, m.issuer_faction_id);
      sqlite3_bind_int(g.stmt, 5, m.target_faction_id);
      sqlite3_bind_int(g.stmt, 6, m.sub_territory_id);
      sqlite3_bind_int(g.stmt, 7, m.control_center_id);
      sqlite3_bind_int64(g.stmt, 8, static_cast<sqlite3_int64>(m.seed));
      sqlite3_bind_double(g.stmt, 9, m.difficulty);
      sqlite3_bind_int(g.stmt, 10, m.reward_eddies);
      sqlite3_bind_int(g.stmt, 11, m.created_seconds);
      if (m.deadline_seconds != 0) sqlite3_bind_int(g.stmt, 12, m.deadline_seconds);
      else sqlite3_bind_null(g.stmt, 12);
      if (m.resolved_seconds != 0) sqlite3_bind_int(g.stmt, 13, m.resolved_seconds);
      else sqlite3_bind_null(g.stmt, 13);
      if (m.resolved_revision != 0) sqlite3_bind_int(g.stmt, 14, m.resolved_revision);
      else sqlite3_bind_null(g.stmt, 14);
      if (sqlite3_step(g.stmt) != SQLITE_DONE) {
        err = sqlite3_errmsg(db_);
        return false;
      }
    }
  }
  return true;
}

bool PlaythroughDb::WriteCheckpointRow(
    int32_t revision,
    const char* kind,
    std::optional<int32_t> base_revision,
    const std::vector<uint8_t>& payload,
    int32_t row_count,
    bool pinned,
    std::string& err) {
  StmtGuard g;
  const char* sql =
      "INSERT INTO checkpoints(revision, kind, base_revision, format_version, row_count, "
      "payload, byte_size, created_utc, pinned) VALUES(?1,?2,?3,?4,?5,?6,?7,?8,?9)";
  if (sqlite3_prepare_v2(db_, sql, -1, &g.stmt, nullptr) != SQLITE_OK) {
    err = sqlite3_errmsg(db_);
    return false;
  }
  sqlite3_bind_int(g.stmt, 1, revision);
  sqlite3_bind_text(g.stmt, 2, kind, -1, SQLITE_STATIC);
  if (base_revision.has_value()) sqlite3_bind_int(g.stmt, 3, *base_revision);
  else sqlite3_bind_null(g.stmt, 3);
  sqlite3_bind_int(g.stmt, 4, kPayloadFormatVersion);
  sqlite3_bind_int(g.stmt, 5, row_count);
  sqlite3_bind_blob(g.stmt, 6, payload.data(), static_cast<int>(payload.size()), SQLITE_TRANSIENT);
  sqlite3_bind_int(g.stmt, 7, static_cast<int>(payload.size()));
  sqlite3_bind_int64(g.stmt, 8, static_cast<sqlite3_int64>(std::time(nullptr)));
  sqlite3_bind_int(g.stmt, 9, pinned ? 1 : 0);
  if (sqlite3_step(g.stmt) != SQLITE_DONE) {
    err = sqlite3_errmsg(db_);
    return false;
  }
  return true;
}

bool PlaythroughDb::RestoreAtRevision(int32_t target_rev, sim::SimState& out_state, std::string& err) {
  // Find exact checkpoint at target_rev (or newest <= target_rev if pruned).
  StmtGuard g;
  const char* sql =
      "SELECT revision, payload FROM checkpoints "
      "WHERE revision <= ?1 ORDER BY revision DESC LIMIT 1";
  if (sqlite3_prepare_v2(db_, sql, -1, &g.stmt, nullptr) != SQLITE_OK) {
    err = sqlite3_errmsg(db_);
    return false;
  }
  sqlite3_bind_int(g.stmt, 1, target_rev);
  if (sqlite3_step(g.stmt) != SQLITE_ROW) {
    err = "no checkpoint found at or before target revision";
    return false;
  }
  const auto* ptr = static_cast<const uint8_t*>(sqlite3_column_blob(g.stmt, 1));
  const int n = sqlite3_column_bytes(g.stmt, 1);
  if (ptr == nullptr || n <= 0) {
    err = "empty checkpoint blob";
    return false;
  }
  std::vector<uint8_t> blob(ptr, ptr + n);
  if (!DecodeFullSnapshot(blob, out_state)) {
    err = "checkpoint payload failed CRC32 or format decode";
    return false;
  }
  return true;
}

SessionBeginResult PlaythroughDb::SessionBegin(
    const std::string& db_path,
    const WorldDb& world,
    int32_t anchor_schema_version,
    uint32_t id_hi,
    uint32_t id_lo,
    int32_t anchor_revision,
    int32_t start_game_seconds,
    sim::SimState& out_state) {
  Close(true);
  SessionBeginResult res;
  read_only_fallback_ = false;

  if (anchor_schema_version > kSchemaVersion) {
    res.status = SessionStatus::ReadOnlyFutureSchema;
    res.warning_or_error = "save schema version is newer than this mod build; read-only fallback";
    read_only_fallback_ = true;
    return res;
  }

  if (sqlite3_open_v2(
          db_path.c_str(), &db_,
          SQLITE_OPEN_READWRITE | SQLITE_OPEN_CREATE, nullptr) != SQLITE_OK) {
    res.warning_or_error = db_ != nullptr ? sqlite3_errmsg(db_) : "sqlite3_open_v2 failed";
    Close(false);
    return res;
  }
  sqlite3_busy_timeout(db_, 2000);

  std::string err;
  // Check whether schema already exists.
  bool has_clock = false;
  {
    StmtGuard g;
    if (sqlite3_prepare_v2(
            db_, "SELECT 1 FROM sqlite_master WHERE type='table' AND name='sim_clock'",
            -1, &g.stmt, nullptr) == SQLITE_OK) {
      has_clock = (sqlite3_step(g.stmt) == SQLITE_ROW);
    }
  }

  if (!has_clock) {
    if (!ExecSql(db_, schema::kPlaythroughV1Sql, err)) {
      res.warning_or_error = err;
      Close(false);
      return res;
    }

    if (id_hi == 0 && id_lo == 0) {
      std::random_device rd;
      id_hi = rd();
      id_lo = rd();
      if (id_hi == 0 && id_lo == 0) {
        id_lo = 1;
      }
    }
    id_hi_ = id_hi;
    id_lo_ = id_lo;

    sim::SimEngine engine(world.BuildTerritoryDefs());
    const uint64_t seed = (static_cast<uint64_t>(id_hi_) << 32U) | static_cast<uint64_t>(id_lo_);
    out_state = engine.CreateInitialState(seed, start_game_seconds);
    const int32_t init_rev = (anchor_revision > 0) ? (anchor_revision + 1) : 0;
    out_state.clock.revision = init_rev;

    if (!ExecSql(db_, "BEGIN IMMEDIATE;", err)) {
      res.warning_or_error = err;
      Close(false);
      return res;
    }
    {
      StmtGuard g;
      const char* sql =
          "INSERT INTO sim_clock(singleton, playthrough_id_hi, playthrough_id_lo, revision, "
          "last_cycle_seconds, cycle_index, rng_seed, rng_counter, world_content_hash) "
          "VALUES(1, ?1, ?2, ?3, ?4, 0, ?5, 0, ?6)";
      if (sqlite3_prepare_v2(db_, sql, -1, &g.stmt, nullptr) != SQLITE_OK) {
        ExecSql(db_, "ROLLBACK;", err);
        res.warning_or_error = sqlite3_errmsg(db_);
        Close(false);
        return res;
      }
      sqlite3_bind_int64(g.stmt, 1, static_cast<sqlite3_int64>(id_hi_));
      sqlite3_bind_int64(g.stmt, 2, static_cast<sqlite3_int64>(id_lo_));
      sqlite3_bind_int(g.stmt, 3, init_rev);
      sqlite3_bind_int(g.stmt, 4, start_game_seconds);
      sqlite3_bind_int64(g.stmt, 5, static_cast<sqlite3_int64>(seed));
      sqlite3_bind_text(g.stmt, 6, world.ContentHash().c_str(), -1, SQLITE_TRANSIENT);
      if (sqlite3_step(g.stmt) != SQLITE_DONE) {
        ExecSql(db_, "ROLLBACK;", err);
        res.warning_or_error = sqlite3_errmsg(db_);
        Close(false);
        return res;
      }
    }
    const auto payload = EncodeFullSnapshot(out_state);
    const int32_t row_count = static_cast<int32_t>(out_state.territories.size());
    if (!ApplyLiveTables(out_state, err) ||
        !WriteCheckpointRow(init_rev, "full", std::nullopt, payload, row_count, true, err) ||
        !ExecSql(db_, "COMMIT;", err)) {
      std::string rb_err;
      ExecSql(db_, "ROLLBACK;", rb_err);
      res.warning_or_error = err;
      Close(false);
      return res;
    }

    durable_revision_ = init_rev;
    last_full_revision_ = init_rev;
    res.status = SessionStatus::Created;
    res.playthrough_id_hi = id_hi_;
    res.playthrough_id_lo = id_lo_;
    res.durable_revision = durable_revision_;
    if (anchor_revision > 0) {
      res.warning_or_error = "external DB missing for save; rebuilt from world defaults";
    }
    return res;
  }

  // Existing DB: verify playthrough ID, restore at anchor_revision, pin R, and fork at max+1.
  if (!ExecSql(db_, "PRAGMA foreign_keys = ON;", err)) {
    res.warning_or_error = err;
    Close(false);
    return res;
  }
  uint32_t db_hi = 0;
  uint32_t db_lo = 0;
  {
    StmtGuard g;
    if (sqlite3_prepare_v2(
            db_, "SELECT playthrough_id_hi, playthrough_id_lo FROM sim_clock WHERE singleton = 1",
            -1, &g.stmt, nullptr) != SQLITE_OK ||
        sqlite3_step(g.stmt) != SQLITE_ROW) {
      res.warning_or_error = "corrupt sim_clock table";
      Close(false);
      return res;
    }
    db_hi = static_cast<uint32_t>(sqlite3_column_int64(g.stmt, 0));
    db_lo = static_cast<uint32_t>(sqlite3_column_int64(g.stmt, 1));
  }
  if ((id_hi != 0 || id_lo != 0) && (db_hi != id_hi || db_lo != id_lo)) {
    res.warning_or_error = "playthrough_id mismatch between save anchor and DB";
    Close(false);
    return res;
  }
  id_hi_ = db_hi;
  id_lo_ = db_lo;

  const int32_t max_rev = MaxCheckpointRevision();
  const int32_t restore_target = (anchor_revision == 0 && max_rev > 0) ? max_rev : anchor_revision;
  if (!RestoreAtRevision(restore_target, out_state, err)) {
    res.warning_or_error = err;
    Close(false);
    return res;
  }

  const int32_t fork_rev = std::max(max_rev, restore_target) + 1;
  out_state.clock.revision = fork_rev;
  const auto fork_payload = EncodeFullSnapshot(out_state);
  const int32_t row_count = static_cast<int32_t>(
      out_state.territories.size() + out_state.orgs.size() + out_state.missions.size());

  if (!ExecSql(db_, "BEGIN IMMEDIATE;", err)) {
    res.warning_or_error = err;
    Close(false);
    return res;
  }
  // Pin restored revision R so retention never drops a known save anchor.
  {
    StmtGuard g;
    if (sqlite3_prepare_v2(db_, "UPDATE checkpoints SET pinned = 1 WHERE revision = ?1", -1, &g.stmt, nullptr) == SQLITE_OK) {
      sqlite3_bind_int(g.stmt, 1, restore_target);
      sqlite3_step(g.stmt);
    }
  }
  if (!ApplyLiveTables(out_state, err) ||
      !WriteCheckpointRow(fork_rev, "full", std::nullopt, fork_payload, row_count, false, err) ||
      !ExecSql(db_, "COMMIT;", err)) {
    std::string rb_err;
    ExecSql(db_, "ROLLBACK;", rb_err);
    res.warning_or_error = err;
    Close(false);
    return res;
  }

  durable_revision_ = fork_rev;
  last_full_revision_ = fork_rev;
  res.status = SessionStatus::Restored;
  res.playthrough_id_hi = id_hi_;
  res.playthrough_id_lo = id_lo_;
  res.durable_revision = durable_revision_;
  return res;
}

int32_t PlaythroughDb::CommitState(
    const sim::SimState& state,
    const std::vector<sim::SimEvent>& events,
    bool force_full_checkpoint,
    std::string& err) {
  if (db_ == nullptr || read_only_fallback_) {
    err = "playthrough DB is not writable";
    return 0;
  }

  const int32_t next_rev = std::max(durable_revision_, MaxCheckpointRevision()) + 1;
  sim::SimState committed = state;
  committed.clock.revision = next_rev;

  const bool is_full = force_full_checkpoint || ((next_rev - last_full_revision_) >= kCheckpointInterval);
  const auto payload = EncodeFullSnapshot(committed);
  const int32_t row_count = static_cast<int32_t>(
      committed.territories.size() + committed.orgs.size() + committed.missions.size());

  if (!ExecSql(db_, "BEGIN IMMEDIATE;", err)) {
    return 0;
  }
  if (!ApplyLiveTables(committed, err) ||
      !WriteCheckpointRow(
          next_rev,
          is_full ? "full" : "delta",
          is_full ? std::nullopt : std::optional<int32_t>(last_full_revision_),
          payload,
          row_count,
          false,
          err)) {
    std::string rb_err;
    ExecSql(db_, "ROLLBACK;", rb_err);
    return 0;
  }

  // Append domain events to event_log inside the same atomic transaction.
  if (!events.empty()) {
    StmtGuard g;
    const char* sql =
        "INSERT INTO event_log(revision, seq, event_type, game_seconds, payload) "
        "VALUES(?1, ?2, ?3, ?4, NULL)";
    if (sqlite3_prepare_v2(db_, sql, -1, &g.stmt, nullptr) != SQLITE_OK) {
      err = sqlite3_errmsg(db_);
      std::string rb_err;
      ExecSql(db_, "ROLLBACK;", rb_err);
      return 0;
    }
    int32_t seq = 0;
    for (const auto& e : events) {
      sqlite3_reset(g.stmt);
      sqlite3_bind_int(g.stmt, 1, next_rev);
      sqlite3_bind_int(g.stmt, 2, seq++);
      sqlite3_bind_text(g.stmt, 3, EventTypeStr(e.type), -1, SQLITE_STATIC);
      sqlite3_bind_int(g.stmt, 4, e.game_seconds);
      if (sqlite3_step(g.stmt) != SQLITE_DONE) {
        err = sqlite3_errmsg(db_);
        std::string rb_err;
        ExecSql(db_, "ROLLBACK;", rb_err);
        return 0;
      }
    }
  }

  if (!ExecSql(db_, "COMMIT;", err)) {
    std::string rb_err;
    ExecSql(db_, "ROLLBACK;", rb_err);
    return 0;
  }

  // Advance durable watermark ONLY after COMMIT returns.
  durable_revision_ = next_rev;
  if (is_full) {
    last_full_revision_ = next_rev;
  }
  return durable_revision_;
}

bool PlaythroughDb::PruneCheckpoints(int64_t max_bytes, std::string& err) {
  if (db_ == nullptr || read_only_fallback_) {
    return false;
  }
  int64_t total_bytes = 0;
  {
    StmtGuard g;
    if (sqlite3_prepare_v2(db_, "SELECT COALESCE(SUM(byte_size), 0) FROM checkpoints", -1, &g.stmt, nullptr) != SQLITE_OK) {
      err = sqlite3_errmsg(db_);
      return false;
    }
    if (sqlite3_step(g.stmt) == SQLITE_ROW) {
      total_bytes = sqlite3_column_int64(g.stmt, 0);
    }
  }
  if (total_bytes <= max_bytes) {
    return true;
  }

  // Delete oldest unpinned checkpoints strictly older than durable_revision_ & last_full_revision_.
  if (!ExecSql(db_, "BEGIN IMMEDIATE;", err)) {
    return false;
  }
  std::vector<std::pair<int32_t, int64_t>> candidates;
  {
    StmtGuard g;
    const char* sql =
        "SELECT revision, byte_size FROM checkpoints "
        "WHERE pinned = 0 AND revision < ?1 AND revision < ?2 "
        "ORDER BY revision ASC";
    if (sqlite3_prepare_v2(db_, sql, -1, &g.stmt, nullptr) != SQLITE_OK) {
      err = sqlite3_errmsg(db_);
      std::string rb;
      ExecSql(db_, "ROLLBACK;", rb);
      return false;
    }
    sqlite3_bind_int(g.stmt, 1, durable_revision_);
    sqlite3_bind_int(g.stmt, 2, last_full_revision_);
    while (sqlite3_step(g.stmt) == SQLITE_ROW) {
      candidates.emplace_back(sqlite3_column_int(g.stmt, 0), sqlite3_column_int64(g.stmt, 1));
    }
  }

  {
    StmtGuard g;
    if (sqlite3_prepare_v2(db_, "DELETE FROM checkpoints WHERE revision = ?1", -1, &g.stmt, nullptr) != SQLITE_OK) {
      err = sqlite3_errmsg(db_);
      std::string rb;
      ExecSql(db_, "ROLLBACK;", rb);
      return false;
    }
    for (const auto& [rev, sz] : candidates) {
      if (total_bytes <= max_bytes) break;
      sqlite3_reset(g.stmt);
      sqlite3_bind_int(g.stmt, 1, rev);
      if (sqlite3_step(g.stmt) != SQLITE_DONE) {
        err = sqlite3_errmsg(db_);
        std::string rb;
        ExecSql(db_, "ROLLBACK;", rb);
        return false;
      }
      total_bytes -= sz;
    }
  }
  return ExecSql(db_, "COMMIT;", err);
}

} // namespace neon::store
