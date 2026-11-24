#pragma once

#include <cstdint>
#include <vector>

namespace neon::sim {

enum class SafeSanctuaryKind : uint8_t {
  None = 0,
  PlayerApartment = 1,
  StoreOrRipperdoc = 2,
};

struct SafeSanctuaryZone {
  SafeSanctuaryKind kind = SafeSanctuaryKind::None;
  double x = 0.0;
  double y = 0.0;
  double z = 0.0;
};

inline constexpr double kApartmentSanctuaryRadiusXY = 28.0;
inline constexpr double kApartmentSanctuaryHalfHeightZ = 10.0;
inline constexpr double kStoreSanctuaryRadiusXY = 14.0;
inline constexpr double kStoreSanctuaryHalfHeightZ = 4.5;

enum class WorldEra : uint8_t {
  Unknown = 0,
  Prologue = 1,
  Act1PreHeist = 2,
  Interlude = 3,
  Act2 = 4,
  Endgame = 5,
  PostStory = 6,
  PLStandalone = 7,
};

struct EraFacts {
  int32_t ep1_standalone = 0;
  int32_t q000_done = 0;
  int32_t q001_active = 0;
  int32_t q001_done = 0;
  int32_t q005_active = 0;
  int32_t q005_done = 0;
  int32_t q101_done = 0;
  int32_t q101_enable_side_content = 0;
  int32_t q115_point_of_no_return = 0;
  int32_t q116_done = 0;
  int32_t q201_done = 0;
  int32_t q202_done = 0;
  int32_t q203_done = 0;
  int32_t q204_done = 0;
  int32_t watson_prolog_lock = 0;
  int32_t watson_prolog_unlock = 0;
};

struct SanitizerPolicy {
  WorldEra era = WorldEra::Unknown;
  bool unlock_city = false;
  bool unlock_act2_content = false;
  bool suppress_campaign = false;
  bool suppress_johnny = false;
};

// Unpack a 16-bit fact presence bitmask (bit i = 1 iff canonical fact i > 0)
// into EraFacts so redscript can pass all 16 facts in a single Uint32 scalar.
[[nodiscard]] EraFacts UnpackEraFactsMask(uint32_t fact_bits);

// Pure world-era classifier over the canonical fact spine (always > 0, never == 1).
[[nodiscard]] WorldEra ClassifyWorldEra(const EraFacts& f);

// Pure sanitizer policy calculator; returns all-false action flags when disabled.
[[nodiscard]] SanitizerPolicy ComputeSanitizerPolicy(const EraFacts& f, bool enabled);

// Compact bitmask for crossing the RED4ext/redscript boundary in a single scalar:
//   bit 0 (1): unlock_city
//   bit 1 (2): unlock_act2_content
//   bit 2 (4): suppress_campaign
//   bit 3 (8): suppress_johnny
//   bits 8..15: WorldEra enum value
[[nodiscard]] uint32_t PackSanitizerPolicyMask(const SanitizerPolicy& p);

[[nodiscard]] const char* WorldEraName(WorldEra era);

// Classify a Cyberpunk 2077 gamedataMappinVariant enum integer into a safe-zone
// sanctuary category (V's apartments, stores, and ripperdocs only).
[[nodiscard]] SafeSanctuaryKind ClassifySafeSanctuaryVariant(int32_t mappin_variant_enum);

// Returns true if (player_x, player_y, player_z) lies inside a single sanctuary cylinder.
[[nodiscard]] bool IsInsideSafeSanctuaryZone(
    const SafeSanctuaryZone& zone,
    double player_x,
    double player_y,
    double player_z);

// Static fallback table covering V's owned apartments so safe zones remain valid even
// before live MappinSystem pins sync on frame 0.
[[nodiscard]] bool IsInsideKnownPlayerApartment(
    double player_x,
    double player_y,
    double player_z);

// Master safe-zone allowlist check: returns true only inside V's apartments,
// stores, or ripperdocs (static apartment fallback + live MappinSystem sanctuaries).
[[nodiscard]] bool IsAllowedSafeZone(
    double player_x,
    double player_y,
    double player_z,
    const std::vector<SafeSanctuaryZone>& dynamic_zones);

// Returns true for vanilla campaign/gig/NCPD/fixer/encounter/tarot/car-purchase
// mappin variants that Sandbox Mode hides from the World Map, Minimap, and 3D HUD.
[[nodiscard]] bool IsSuppressedVanillaMappinVariant(int32_t mappin_variant_enum);

} // namespace neon::sim
