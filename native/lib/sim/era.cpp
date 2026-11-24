#include "era.hpp"

namespace neon::sim {

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

} // namespace neon::sim
