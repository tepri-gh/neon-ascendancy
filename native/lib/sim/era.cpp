#include "era.hpp"

#include <cmath>

namespace neon::sim {

namespace {

// V's base-game apartments verified from always_loaded_*.streamingsector.json
// (Dogtown Kress Street Hideout and any DLC/modded apartments are additionally
// picked up dynamically from MappinSystem ApartmentVariant pins).
constexpr SafeSanctuaryZone kKnownPlayerApartments[] = {
    {SafeSanctuaryKind::PlayerApartment, -1381.758, 1271.708, 123.065}, // Megabuilding H10
    {SafeSanctuaryKind::PlayerApartment, -1505.056, 2231.156, 22.200},  // Northside Motel
    {SafeSanctuaryKind::PlayerApartment, -785.577, 977.945, 28.210},    // Japantown
    {SafeSanctuaryKind::PlayerApartment, -1520.291, -976.132, 86.803},  // The Glen
    {SafeSanctuaryKind::PlayerApartment, -1609.054, 356.505, 49.236},   // Corpo Plaza
};

} // namespace

EraFacts UnpackEraFactsMask(uint32_t b) {
  EraFacts f;
  f.ep1_standalone = (b & (1U << 0U)) != 0U ? 1 : 0;
  f.q000_done = (b & (1U << 1U)) != 0U ? 1 : 0;
  f.q001_active = (b & (1U << 2U)) != 0U ? 1 : 0;
  f.q001_done = (b & (1U << 3U)) != 0U ? 1 : 0;
  f.q005_active = (b & (1U << 4U)) != 0U ? 1 : 0;
  f.q005_done = (b & (1U << 5U)) != 0U ? 1 : 0;
  f.q101_done = (b & (1U << 6U)) != 0U ? 1 : 0;
  f.q101_enable_side_content = (b & (1U << 7U)) != 0U ? 1 : 0;
  f.q115_point_of_no_return = (b & (1U << 8U)) != 0U ? 1 : 0;
  f.q116_done = (b & (1U << 9U)) != 0U ? 1 : 0;
  f.q201_done = (b & (1U << 10U)) != 0U ? 1 : 0;
  f.q202_done = (b & (1U << 11U)) != 0U ? 1 : 0;
  f.q203_done = (b & (1U << 12U)) != 0U ? 1 : 0;
  f.q204_done = (b & (1U << 13U)) != 0U ? 1 : 0;
  f.watson_prolog_lock = (b & (1U << 14U)) != 0U ? 1 : 0;
  f.watson_prolog_unlock = (b & (1U << 15U)) != 0U ? 1 : 0;
  return f;
}

WorldEra ClassifyWorldEra(const EraFacts& f) {
  if (f.ep1_standalone > 0) {
    return WorldEra::PLStandalone;
  }
  if (f.q201_done > 0 || f.q202_done > 0 || f.q203_done > 0 || f.q204_done > 0) {
    return WorldEra::PostStory;
  }
  if (f.q115_point_of_no_return > 0 || f.q116_done > 0) {
    return WorldEra::Endgame;
  }
  if (f.q005_done > 0) {
    if (f.q101_done > 0 || f.q101_enable_side_content > 0 || f.watson_prolog_lock == 0) {
      return WorldEra::Act2;
    }
    return WorldEra::Interlude;
  }
  if (f.watson_prolog_unlock > 0) {
    return WorldEra::Interlude;
  }
  if (f.q001_done > 0) {
    return WorldEra::Act1PreHeist;
  }
  if (f.q005_active > 0 || f.q001_active > 0 || f.q000_done > 0) {
    return WorldEra::Prologue;
  }
  return WorldEra::Unknown;
}

SanitizerPolicy ComputeSanitizerPolicy(const EraFacts& f, bool enabled) {
  SanitizerPolicy policy;
  policy.era = ClassifyWorldEra(f);
  if (!enabled) {
    return policy;
  }

  // Monotonic city traversal unlock: lift Watson lock if still locked or unlock unset.
  policy.unlock_city = (f.watson_prolog_lock > 0 || f.watson_prolog_unlock == 0);

  // Enable open-world activities / side content when not already enabled.
  policy.unlock_act2_content =
      (policy.era == WorldEra::Prologue ||
       policy.era == WorldEra::Act1PreHeist ||
       policy.era == WorldEra::Interlude ||
       f.q101_enable_side_content == 0);

  policy.suppress_campaign = true;

  // Johnny / Relic status effects apply from post-Heist Interlude onward (and PL standalone).
  policy.suppress_johnny =
      (policy.era == WorldEra::Interlude ||
       policy.era == WorldEra::Act2 ||
       policy.era == WorldEra::Endgame ||
       policy.era == WorldEra::PostStory ||
       policy.era == WorldEra::PLStandalone);

  return policy;
}

uint32_t PackSanitizerPolicyMask(const SanitizerPolicy& p) {
  uint32_t mask = static_cast<uint32_t>(p.era) << 8U;
  if (p.unlock_city) mask |= 1U << 0U;
  if (p.unlock_act2_content) mask |= 1U << 1U;
  if (p.suppress_campaign) mask |= 1U << 2U;
  if (p.suppress_johnny) mask |= 1U << 3U;
  return mask;
}

const char* WorldEraName(WorldEra era) {
  switch (era) {
    case WorldEra::Unknown: return "Unknown";
    case WorldEra::Prologue: return "Prologue";
    case WorldEra::Act1PreHeist: return "Act 1 (Pre-Heist)";
    case WorldEra::Interlude: return "Interlude";
    case WorldEra::Act2: return "Act 2";
    case WorldEra::Endgame: return "Endgame";
    case WorldEra::PostStory: return "Post-Story";
    case WorldEra::PLStandalone: return "Phantom Liberty Standalone";
  }
  return "Unknown";
}

SafeSanctuaryKind ClassifySafeSanctuaryVariant(int32_t mappin_variant_enum) {
  // Exact values from Cyberpunk 2077 2.5 enum gamedataMappinVariant.
  switch (mappin_variant_enum) {
    case 10:  // ApartmentVariant
    case 125: // Zzz05_ApartmentToPurchaseVariant
      return SafeSanctuaryKind::PlayerApartment;

    case 96:  // ServicePointClothesVariant
    case 97:  // ServicePointCyberwareVariant
    case 100: // ServicePointGunsVariant
    case 101: // ServicePointJunkVariant
    case 102: // ServicePointMedsVariant
    case 103: // ServicePointMeleeTrainerVariant
    case 104: // ServicePointNetTrainerVariant
    case 106: // ServicePointRipperdocVariant
    case 107: // ServicePointTechVariant
    case 135: // Zzz14_ServicePointBlackMarketVariant
    case 143: // Zzz21_ServicePointGlamdocVariant
      return SafeSanctuaryKind::StoreOrRipperdoc;

    default:
      return SafeSanctuaryKind::None;
  }
}

bool IsInsideSafeSanctuaryZone(
    const SafeSanctuaryZone& zone,
    double player_x,
    double player_y,
    double player_z) {
  double radius_xy = 0.0;
  double half_z = 0.0;
  switch (zone.kind) {
    case SafeSanctuaryKind::PlayerApartment:
      radius_xy = kApartmentSanctuaryRadiusXY;
      half_z = kApartmentSanctuaryHalfHeightZ;
      break;
    case SafeSanctuaryKind::StoreOrRipperdoc:
      radius_xy = kStoreSanctuaryRadiusXY;
      half_z = kStoreSanctuaryHalfHeightZ;
      break;
    case SafeSanctuaryKind::None:
      return false;
  }
  const double dx = player_x - zone.x;
  const double dy = player_y - zone.y;
  const double dz = std::abs(player_z - zone.z);
  return (dx * dx + dy * dy) <= (radius_xy * radius_xy) && dz <= half_z;
}

bool IsInsideKnownPlayerApartment(
    double player_x,
    double player_y,
    double player_z) {
  for (const auto& apt : kKnownPlayerApartments) {
    if (IsInsideSafeSanctuaryZone(apt, player_x, player_y, player_z)) {
      return true;
    }
  }
  return false;
}

bool IsAllowedSafeZone(
    double player_x,
    double player_y,
    double player_z,
    const std::vector<SafeSanctuaryZone>& dynamic_zones) {
  if (IsInsideKnownPlayerApartment(player_x, player_y, player_z)) {
    return true;
  }
  for (const auto& zone : dynamic_zones) {
    if (IsInsideSafeSanctuaryZone(zone, player_x, player_y, player_z)) {
      return true;
    }
  }
  return false;
}

bool IsSuppressedVanillaMappinVariant(int32_t mappin_variant_enum) {
  // Exact values from Cyberpunk 2077 2.5 enum gamedataMappinVariant.
  // Preserves Fast Travel, Apartments, Drop Points, Vehicles, Ripperdocs, and Stores.
  switch (mappin_variant_enum) {
    case 13:  // BountyHuntVariant
    case 16:  // ClientInDistressVariant
    case 18:  // ConvoyVariant
    case 20:  // CourierVariant
    case 25:  // DefaultQuestVariant
    case 29:  // DynamicEventVariant
    case 49:  // ExclamationMarkVariant
    case 52:  // FixerVariant
    case 56:  // GangWatchVariant
    case 64:  // HiddenStashVariant
    case 66:  // HuntForPsychoVariant
    case 75:  // MinorActivityVariant
    case 85:  // OutpostVariant
    case 87:  // QuestGiverVariant
    case 88:  // QuestionMarkVariant
    case 92:  // RetrievingVariant
    case 93:  // SOSsignalVariant
    case 94:  // SabotageVariant
    case 109: // SmugglersDenVariant
    case 115: // TarotVariant
    case 117: // ThieveryVariant
    case 121: // Zzz01_CarForPurchaseVariant
    case 122: // Zzz02_MotorcycleForPurchaseVariant
    case 126: // Zzz06_NCPDGigVariant
    case 129: // Zzz09_CourierSandboxActivityVariant
    case 133: // Zzz12_WorldEncounterVariant
      return true;
    default:
      return false;
  }
}

} // namespace neon::sim
