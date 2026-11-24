#pragma once

#include <cstdint>
#include <optional>
#include <string>
#include <unordered_map>
#include <vector>

#include "sim.hpp"

struct sqlite3;

namespace neon::store {

struct WorldFaction {
  int32_t faction_id = 0;
  std::string code;
  std::string display_name;
  std::string category;
  uint32_t color_rgba_packed = 0xCCCCCCFFU;
};

struct WorldDistrict {
  int32_t district_id = 0;
  std::string code;
  std::string display_name;
  std::string kind;
  double bbox_min_x = 0.0;
  double bbox_min_y = 0.0;
  double bbox_max_x = 0.0;
  double bbox_max_y = 0.0;
};

struct WorldControlCenter {
  int32_t control_center_id = 0;
  int32_t sub_territory_id = 0;
  std::string code;
  std::string display_name;
  double x = 0.0;
  double y = 0.0;
  double z = 0.0;
  double capture_radius_m = 40.0;
};

struct WorldSubTerritory {
  int32_t sub_territory_id = 0;
  int32_t district_id = 0;
  std::string code;
  std::string display_name;
  std::string gamedata_subdistrict;
  std::string owner_kind;
  int32_t initial_owner_faction_id = 0;
  int32_t base_income_per_cycle = 0;
  int32_t defense_rating = 0;
  double centroid_x = 0.0;
  double centroid_y = 0.0;
  double centroid_z = 0.0;
};

// Read-only static world.db loader with O(1) boot-loaded level-0 grid lookup.
class WorldDb {
 public:
  WorldDb() = default;
  ~WorldDb();

  WorldDb(const WorldDb&) = delete;
  WorldDb& operator=(const WorldDb&) = delete;

  bool Open(const std::string& path, bool immutable, std::string& err);
  void Close();

  [[nodiscard]] bool IsOpen() const { return db_ != nullptr; }
  [[nodiscard]] const std::string& ContentHash() const { return content_hash_; }
  [[nodiscard]] double CellSizeMeters() const { return cell_size_m_; }
  [[nodiscard]] const std::vector<WorldFaction>& Factions() const { return factions_; }
  [[nodiscard]] const std::vector<WorldDistrict>& Districts() const { return districts_; }
  [[nodiscard]] const std::vector<WorldSubTerritory>& SubTerritories() const { return sub_territories_; }
  [[nodiscard]] const std::vector<WorldControlCenter>& ControlCenters() const { return control_centers_; }
  [[nodiscard]] std::vector<sim::TerritoryDef> BuildTerritoryDefs() const;

  // O(1) RAM metadata lookups: zero SQL queries on hot path.
  [[nodiscard]] const WorldFaction* FindFaction(int32_t faction_id) const;
  [[nodiscard]] const WorldDistrict* FindDistrict(int32_t district_id) const;
  [[nodiscard]] const WorldSubTerritory* FindSubTerritory(int32_t sub_territory_id) const;
  [[nodiscard]] const WorldControlCenter* FindControlCenterBySubTerritory(int32_t sub_territory_id) const;

  // O(1) RAM spatial lookup: zero SQL queries on hot path.
  [[nodiscard]] int32_t LookupSubTerritoryAt(double x, double y) const;
  [[nodiscard]] int32_t FindNearestSubTerritory(double x, double y) const;
  [[nodiscard]] int32_t FindNearestRivalSubTerritory(
      double x,
      double y,
      int32_t exclude_faction_id,
      const std::vector<sim::TerritoryRuntime>& territories) const;

  // 2D R-Tree prefilter + 3D distance check in C++.
  [[nodiscard]] std::vector<int32_t> QuerySpawnPointsNear(
      double x, double y, double z, double radius_m) const;

  [[nodiscard]] static uint32_t ParseHexColorRgba(const std::string& hex);

 private:
  static uint64_t PackCellKey(int32_t cx, int32_t cy);

  sqlite3* db_ = nullptr;
  std::string content_hash_;
  double cell_size_m_ = 100.0;
  std::vector<WorldFaction> factions_;
  std::vector<WorldDistrict> districts_;
  std::vector<WorldSubTerritory> sub_territories_;
  std::vector<WorldControlCenter> control_centers_;
  std::unordered_map<int32_t, size_t> faction_index_;
  std::unordered_map<int32_t, size_t> district_index_;
  std::unordered_map<int32_t, size_t> sub_territory_index_;
  std::unordered_map<int32_t, size_t> cc_by_st_index_;
  std::unordered_map<uint64_t, int32_t> cell_grid_;
};

enum class SessionStatus : uint8_t {
  Error = 0,
  Created = 1,
  Restored = 2,
  ReadOnlyFutureSchema = 3,
};

struct SessionBeginResult {
  SessionStatus status = SessionStatus::Error;
  uint32_t playthrough_id_hi = 0;
  uint32_t playthrough_id_lo = 0;
  int32_t durable_revision = 0;
  std::string warning_or_error;
};

// Durable per-playthrough dynamic SQLite store implementing the revision-watermark
// checkpoint/restore/fork protocol from docs/research/native-db-architecture.md.
class PlaythroughDb {
 public:
  static constexpr int32_t kSchemaVersion = 1;
  static constexpr int32_t kCheckpointInterval = 64;
  static constexpr uint16_t kPayloadFormatVersion = 2;

  PlaythroughDb() = default;
  ~PlaythroughDb();

  PlaythroughDb(const PlaythroughDb&) = delete;
  PlaythroughDb& operator=(const PlaythroughDb&) = delete;

  // Open or create playthrough DB, restore exact state at anchor_revision (if > 0),
  // and fork at max(db_max, anchor_revision) + 1 with a full checkpoint.
  SessionBeginResult SessionBegin(
      const std::string& db_path,
      const WorldDb& world,
      int32_t anchor_schema_version,
      uint32_t id_hi,
      uint32_t id_lo,
      int32_t anchor_revision,
      int32_t start_game_seconds,
      sim::SimState& out_state);

  // Atomically persist live state + checkpoint at next revision.
  // Returns the new durable revision (> 0) AFTER SQLite COMMIT returns, or 0 on error.
  int32_t CommitState(
      const sim::SimState& state,
      const std::vector<sim::SimEvent>& events,
      bool force_full_checkpoint,
      std::string& err);

  // Prune unpinned checkpoints if total stored payload exceeds max_bytes.
  bool PruneCheckpoints(int64_t max_bytes, std::string& err);

  bool Close(bool truncate_wal = true);

  [[nodiscard]] bool IsOpen() const { return db_ != nullptr; }
  [[nodiscard]] int32_t DurableRevision() const { return durable_revision_; }
  [[nodiscard]] bool IsReadOnlyFallback() const { return read_only_fallback_; }

  // Exposed for deterministic codec tests.
  static std::vector<uint8_t> EncodeFullSnapshot(const sim::SimState& state);
  static bool DecodeFullSnapshot(const std::vector<uint8_t>& blob, sim::SimState& out_state);

 private:
  bool ApplyLiveTables(const sim::SimState& state, std::string& err);
  bool WriteCheckpointRow(
      int32_t revision,
      const char* kind,
      std::optional<int32_t> base_revision,
      const std::vector<uint8_t>& payload,
      int32_t row_count,
      bool pinned,
      std::string& err);
  bool RestoreAtRevision(int32_t target_rev, sim::SimState& out_state, std::string& err);
  int32_t MaxCheckpointRevision() const;

  sqlite3* db_ = nullptr;
  uint32_t id_hi_ = 0;
  uint32_t id_lo_ = 0;
  int32_t durable_revision_ = 0;
  int32_t last_full_revision_ = 0;
  bool read_only_fallback_ = false;
};

} // namespace neon::store
