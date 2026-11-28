#pragma once

#include <cstdint>
#include <string>
#include <vector>

#include "sim.hpp"

namespace neon::sim {

// Node garrison domain types (docs/design/node-garrison-and-assault.md §1, §3, §4).
// Pure C++20: zero OS, SQLite, RED4ext, or anchor-file dependencies.

inline constexpr int32_t kMinFactionFieldedTier = 1;
inline constexpr int32_t kMaxFactionFieldedTier = 5;
inline constexpr int32_t kMinPowerLevel = 10;
inline constexpr int32_t kMaxPowerLevel = 65;

enum class NodeSize : uint8_t {
  Small = 0,
  Medium = 1,
  Large = 2,
  VeryLarge = 3,
};

enum class NodeType : uint8_t {
  Economy = 0,
  Espionage = 1,
  Tech = 2,
  Military = 3,
};

enum class GarrisonRole : uint8_t {
  GuardRanged = 0,
  GuardMelee = 1,
  Heavy = 2,
  Sniper = 3,
  Netrunner = 4,
  Elite = 5,
};

enum class BossArchetype : uint8_t {
  Enforcer = 0,
  Netrunner = 1,
  Vanguard = 2,
};

enum class UnitRarity : uint8_t {
  Normal = 0,
  Specialist = 1,
  Elite = 2,
  Boss = 3,
};

enum class GearBracket : uint8_t {
  Low = 0,   // Fielded tier 1-2
  Mid = 1,   // Fielded tier 3
  High = 2,  // Fielded tier 4-5
};

enum class AssignmentKind : uint8_t {
  BossSeat = 0,
  Post = 1,
  Patrol = 2,
};

struct BossTierSpec {
  UnitRarity primary_boss_rarity = UnitRarity::Elite;
  int32_t primary_boss_count = 1;
  int32_t min_sub_lt_count = 0;
  int32_t max_sub_lt_count = 0;
  int32_t boss_guard_elites = 0;  // Counted inside Specialists & Elites budget.
  int32_t zone_count = 1;
};

struct GarrisonBudget {
  NodeSize size = NodeSize::Small;
  NodeType type = NodeType::Economy;
  int32_t total_security = 0;
  int32_t netrunners = 0;
  int32_t heavies = 0;
  int32_t snipers = 0;
  int32_t elites = 0;        // Includes boss_guard_elites.
  int32_t guard_ranged = 0;
  int32_t guard_melee = 0;
  int32_t primary_bosses = 0;
  int32_t sub_lieutenants = 0;
  int32_t boss_guard_elites = 0;
  int32_t post_units = 0;    // Non-boss units on static posts.
  int32_t patrol_units = 0;  // Non-boss units on patrol loops.
  int32_t civilian_crowd_target = 0;
  int32_t netrunner_intel_bonus = 0;
  int32_t zone_count = 1;

  [[nodiscard]] int32_t SpecialistsAndElites() const { return heavies + snipers + elites; }
  [[nodiscard]] int32_t RankAndFileGuards() const { return guard_ranged + guard_melee; }
  [[nodiscard]] int32_t TotalBosses() const { return primary_bosses + sub_lieutenants; }
};

struct GarrisonUnitSpec {
  int32_t slot_index = 0;
  std::string record_id;
  GarrisonRole role = GarrisonRole::GuardRanged;
  UnitRarity rarity = UnitRarity::Normal;
  int32_t power_level = kMinPowerLevel;
  AssignmentKind assignment = AssignmentKind::Post;
  int32_t zone_index = 0;
  bool is_boss = false;
  bool is_sub_lt = false;
  bool is_boss_guard = false;
};

struct GarrisonSpec {
  int32_t faction_id = 0;
  int32_t fielded_tier = 1;
  NodeSize size = NodeSize::Small;
  NodeType type = NodeType::Economy;
  bool is_hq = false;
  uint64_t node_seed = 0;
  float strength_ratio = 1.0F;  // 0.0 = cleared, 1.0 = full garrison.
  OrgKind player_org_kind = OrgKind::Gang;
  // Optional canonical lore boss Character.* record (overrides generated template on primary boss).
  std::string lore_boss_record_id;
};

struct GarrisonRoster {
  std::string faction_template_key;
  GearBracket gear_bracket = GearBracket::Low;
  BossArchetype boss_archetype = BossArchetype::Vanguard;
  UnitRarity primary_boss_rarity = UnitRarity::Elite;
  int32_t influence = 1;
  GarrisonBudget budget;
  std::vector<GarrisonUnitSpec> units;
};

// Pure rules & lookup helpers.
[[nodiscard]] GearBracket ComputeGearBracket(int32_t fielded_tier);
[[nodiscard]] int32_t ComputeFactionTierBasePower(int32_t fielded_tier);
[[nodiscard]] int32_t ComputeRarityPowerOffset(UnitRarity rarity);
[[nodiscard]] int32_t ComputeSizePowerOffset(NodeSize size);
[[nodiscard]] int32_t ComputePowerLevel(int32_t fielded_tier, UnitRarity rarity, NodeSize size);

[[nodiscard]] BossTierSpec ResolveBossTier(NodeSize size);
[[nodiscard]] UnitRarity RoleDefaultRarity(GarrisonRole role);
[[nodiscard]] int32_t ComputeNodeInfluence(NodeSize size, bool is_hq);

// Maps any territorial faction_id (or Afterlife / player org) to its TweakXL PascalCase family key.
[[nodiscard]] std::string ResolveFactionTemplateKey(
    int32_t faction_id,
    OrgKind player_org_kind = OrgKind::Gang);

[[nodiscard]] const char* GarrisonRoleName(GarrisonRole role);
[[nodiscard]] const char* GearBracketName(GearBracket bracket);
[[nodiscard]] const char* BossArchetypeName(BossArchetype archetype);

[[nodiscard]] std::string FormatUnitRecordId(
    const std::string& faction_template_key,
    GarrisonRole role,
    GearBracket bracket);

[[nodiscard]] std::string FormatBossRecordId(
    const std::string& faction_template_key,
    BossArchetype archetype,
    UnitRarity boss_rarity);

// Deterministic headcount & role-mix solver obeying §1 size/type bounds.
[[nodiscard]] GarrisonBudget ComputeGarrisonBudget(
    NodeSize size,
    NodeType type,
    uint64_t node_seed,
    float strength_ratio = 1.0F);

// Deterministic full unit roster ready for anchor placement & spawning.
[[nodiscard]] GarrisonRoster BuildGarrisonRoster(const GarrisonSpec& spec);

}  // namespace neon::sim
