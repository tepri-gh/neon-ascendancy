#pragma once

#include <cstdint>
#include <string>
#include <vector>

namespace neon::sim {

inline constexpr int32_t kPlayerFactionIdBase = 1000;
inline constexpr int32_t kDefaultCycleSeconds = 86400; // 1 in-game day
inline constexpr int32_t kMaxEventDepth = 64;
inline constexpr int32_t kDefaultCombatKillsRequired = 3;
inline constexpr uint32_t kPlayerOrgColorRgba = 0x00F0FFFFU; // Neon Cyan (#00F0FF, alpha 255)

enum class OrgKind : uint8_t {
  Gang = 0,
  Corporation = 1,
};

enum class MissionKind : uint8_t {
  Combat = 0,
  Economic = 1,
  Espionage = 2,
};

enum class MissionState : uint8_t {
  Offered = 0,
  Active = 1,
  Succeeded = 2,
  Failed = 3,
  Expired = 4,
};

enum class PauseMenuAction : int32_t {
  None = 0,
  ActivateAscendancy = 1,
  FoundGangHere = 2,
  LaunchRivalRaid = 3,
  ShowStatus = 4,
};

struct TerritoryDef {
  int32_t sub_territory_id = 0;
  int32_t district_id = 0;
  int32_t initial_owner_faction_id = 0;
  int32_t base_income_per_cycle = 0;
  int32_t defense_rating = 0;
};

struct TerritoryRuntime {
  int32_t sub_territory_id = 0;
  int32_t owner_faction_id = 0;
  int32_t holder_faction_id = 0;
  int32_t contested_by_faction_id = 0;
  float control_level = 1.0F;
  float heat = 0.0F;
  int32_t last_flip_revision = 0;
  int32_t last_flip_seconds = 0;
};

struct OrgRuntime {
  int32_t org_id = 0;
  OrgKind kind = OrgKind::Gang;
  std::string display_name;
  int32_t faction_id = 0;
  int64_t treasury_eddies = 0;
  float notoriety = 0.0F;
  float heat = 0.0F;
  int32_t upkeep_per_cycle = 0;
  int32_t founded_revision = 0;
  int32_t founded_seconds = 0;
};

struct MissionRuntime {
  int32_t mission_id = 0;
  MissionKind kind = MissionKind::Combat;
  MissionState state = MissionState::Offered;
  int32_t issuer_faction_id = 0;
  int32_t target_faction_id = 0;
  int32_t sub_territory_id = 0;
  int32_t control_center_id = 0;
  uint64_t seed = 0;
  float difficulty = 1.0F;
  int32_t reward_eddies = 0;
  int32_t created_seconds = 0;
  int32_t deadline_seconds = 0;
  int32_t resolved_seconds = 0;
  int32_t resolved_revision = 0;
  int32_t kills_required = kDefaultCombatKillsRequired;
  int32_t kills_done = 0;
};

struct SimClock {
  int32_t revision = 0;
  int32_t last_cycle_seconds = 0;
  int32_t cycle_index = 0;
  uint64_t rng_seed = 0;
  uint64_t rng_counter = 0;
};

enum class SimEventType : uint8_t {
  OrgFounded = 1,
  MissionOffered = 2,
  MissionCompleted = 3,
  MissionFailed = 4,
  TerritoryOwnerChanged = 5,
  HeatChanged = 6,
  IncomeSettled = 7,
  CycleElapsed = 8,
};

struct SimEvent {
  SimEventType type = SimEventType::CycleElapsed;
  int32_t game_seconds = 0;
  int32_t a = 0; // primary entity/territory/org/mission id
  int32_t b = 0; // secondary faction id or count
  int64_t amount = 0; // eddies or scaled delta
};

struct SimState {
  SimClock clock;
  std::vector<TerritoryRuntime> territories;
  std::vector<OrgRuntime> orgs;
  std::vector<MissionRuntime> missions;
};

struct CommandResult {
  bool ok = false;
  std::string error;
  int64_t payout_eddies = 0;
  std::vector<SimEvent> emitted;
};

// Pure deterministic causal simulation engine. Holds zero OS, SQLite, or game APIs.
class SimEngine {
 public:
  explicit SimEngine(std::vector<TerritoryDef> defs);

  [[nodiscard]] SimState CreateInitialState(uint64_t rng_seed, int32_t start_seconds) const;

  // Player founds a named gang and claims an initial home sub-territory.
  CommandResult FoundGang(
      SimState& state,
      const std::string& display_name,
      int32_t home_sub_territory_id,
      int32_t game_seconds) const;

  // Generate/offer a combat clear-out mission against a rival sub-territory.
  CommandResult OfferCombatMission(
      SimState& state,
      int32_t sub_territory_id,
      int32_t control_center_id,
      int32_t reward_eddies,
      int32_t game_seconds,
      int32_t kills_required = kDefaultCombatKillsRequired) const;

  // Record a hostile takedown for an active combat mission; automatically completes
  // and flips the territory immediately once kills_done >= kills_required.
  CommandResult RecordMissionKill(
      SimState& state,
      int32_t mission_id,
      int32_t game_seconds) const;

  // Complete a mission; in v0.1.0, completing a combat mission flips the
  // target sub-territory immediately to the player's org via the causal event bus.
  CommandResult CompleteMission(
      SimState& state,
      int32_t mission_id,
      int32_t game_seconds) const;

  // Advance deterministic GameTime cycles and settle periodic territory income.
  CommandResult AdvanceTime(
      SimState& state,
      int32_t current_game_seconds,
      int32_t cycle_seconds = kDefaultCycleSeconds) const;

  [[nodiscard]] int64_t ComputeCycleIncome(const SimState& state, int32_t faction_id) const;

  // Pure raid combatant filter: rejects crowds, civilians, vendors, and non-combatant
  // affiliations so innocent bystanders never count toward territory capture.
  [[nodiscard]] static bool IsValidRaidCombatant(
      bool is_crowd,
      bool is_civilian,
      bool is_vendor,
      bool is_hostile,
      int32_t affiliation_enum);

  // Pure read-only queries and presentation helpers (keep UI logic in C++).
  [[nodiscard]] static const TerritoryRuntime* FindTerritoryConst(
      const SimState& state, int32_t sub_territory_id);
  [[nodiscard]] static const OrgRuntime* FindPlayerOrgConst(const SimState& state);
  [[nodiscard]] static const MissionRuntime* FindActiveCombatMissionConst(const SimState& state);
  [[nodiscard]] static int32_t CountOwnedTerritories(const SimState& state, int32_t faction_id);

  [[nodiscard]] static PauseMenuAction ResolvePauseMenuAction(
      const SimState& state, bool ascendancy_enabled);
  [[nodiscard]] static std::string FormatPauseMenuLabel(
      const SimState& state, bool ascendancy_enabled);
  [[nodiscard]] static std::string FormatTerritoryTooltipDesc(
      const std::string& district_name,
      const std::string& owner_name,
      int32_t base_income_per_cycle,
      bool is_player_owned,
      bool is_active_raid_target,
      int32_t raid_kills_done,
      int32_t raid_kills_required);
  [[nodiscard]] std::string FormatStatusSummary(
      const SimState& state, const std::string& active_target_name) const;

 private:
  const TerritoryDef* FindDef(int32_t sub_territory_id) const;
  static TerritoryRuntime* FindTerritory(SimState& state, int32_t sub_territory_id);
  static OrgRuntime* FindPlayerOrg(SimState& state);
  static MissionRuntime* FindMission(SimState& state, int32_t mission_id);

  void ProcessEventQueue(
      SimState& state,
      std::vector<SimEvent> initial,
      CommandResult& out) const;

  std::vector<TerritoryDef> defs_;
};

} // namespace neon::sim
