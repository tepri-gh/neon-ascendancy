#include "garrison.hpp"

#include <algorithm>
#include <cmath>

namespace neon::sim {

namespace {

// Deterministic SplitMix64 PRNG (zero global state, identical across Linux & MSVC).
struct SplitMix64 {
  uint64_t state;

  explicit SplitMix64(uint64_t seed) : state(seed ^ 0x9E3779B97F4A7C15ULL) {}

  uint64_t Next() {
    uint64_t z = (state += 0x9E3779B97F4A7C15ULL);
    z = (z ^ (z >> 30U)) * 0xBF58476D1CE4E5B9ULL;
    z = (z ^ (z >> 27U)) * 0x94D049BB133111EBULL;
    return z ^ (z >> 31U);
  }

  int32_t NextRange(int32_t lo, int32_t hi) {
    if (hi <= lo) {
      return lo;
    }
    const uint64_t span = static_cast<uint64_t>(hi - lo) + 1ULL;
    return lo + static_cast<int32_t>(Next() % span);
  }
};

struct SizeBounds {
  int32_t min_total;
  int32_t max_total;
  int32_t min_net;
  int32_t max_net;
  int32_t min_spec;
  int32_t max_spec;
  int32_t min_guards;
  int32_t max_guards;
  double base_patrol_ratio;
  int32_t econ_civ_min;
  int32_t econ_civ_max;
};

SizeBounds BoundsForSize(NodeSize size) {
  // Exact §1 table from docs/design/node-garrison-and-assault.md.
  switch (size) {
    case NodeSize::Small:
      return SizeBounds{6, 10, 1, 1, 0, 2, 4, 6, 0.25, 4, 8};
    case NodeSize::Medium:
      return SizeBounds{11, 20, 1, 2, 2, 5, 7, 12, 0.35, 10, 18};
    case NodeSize::Large:
      return SizeBounds{21, 30, 2, 3, 5, 8, 13, 18, 0.40, 20, 35};
    case NodeSize::VeryLarge:
      return SizeBounds{31, 40, 3, 4, 8, 12, 18, 23, 0.50, 30, 40};
  }
  return SizeBounds{6, 10, 1, 1, 0, 2, 4, 6, 0.25, 4, 8};
}

BossArchetype PickBossArchetype(NodeType type, SplitMix64& rng) {
  // Type-aligned default with deterministic variety.
  const int32_t roll = rng.NextRange(0, 99);
  switch (type) {
    case NodeType::Espionage:
      return roll < 65 ? BossArchetype::Netrunner : BossArchetype::Vanguard;
    case NodeType::Military:
      return roll < 55 ? BossArchetype::Enforcer : BossArchetype::Vanguard;
    case NodeType::Tech:
      if (roll < 45) return BossArchetype::Netrunner;
      return roll < 75 ? BossArchetype::Enforcer : BossArchetype::Vanguard;
    case NodeType::Economy:
      if (roll < 50) return BossArchetype::Vanguard;
      return roll < 80 ? BossArchetype::Enforcer : BossArchetype::Netrunner;
  }
  return BossArchetype::Vanguard;
}

}  // namespace

GearBracket ComputeGearBracket(int32_t fielded_tier) {
  const int32_t tier = std::clamp(fielded_tier, kMinFactionFieldedTier, kMaxFactionFieldedTier);
  if (tier <= 2) {
    return GearBracket::Low;
  }
  if (tier == 3) {
    return GearBracket::Mid;
  }
  return GearBracket::High;
}

int32_t ComputeFactionTierBasePower(int32_t fielded_tier) {
  const int32_t tier = std::clamp(fielded_tier, kMinFactionFieldedTier, kMaxFactionFieldedTier);
  switch (tier) {
    case 1: return 14;
    case 2: return 22;
    case 3: return 32;
    case 4: return 44;
    case 5: return 54;
    default: return 14;
  }
}

int32_t ComputeRarityPowerOffset(UnitRarity rarity) {
  switch (rarity) {
    case UnitRarity::Normal: return 0;
    case UnitRarity::Specialist: return 3;
    case UnitRarity::Elite: return 6;
    case UnitRarity::Boss: return 10;
  }
  return 0;
}

int32_t ComputeSizePowerOffset(NodeSize size) {
  switch (size) {
    case NodeSize::Small: return 0;
    case NodeSize::Medium: return 2;
    case NodeSize::Large: return 5;
    case NodeSize::VeryLarge: return 8;
  }
  return 0;
}

int32_t ComputePowerLevel(int32_t fielded_tier, UnitRarity rarity, NodeSize size) {
  const int32_t raw = ComputeFactionTierBasePower(fielded_tier) +
                      ComputeRarityPowerOffset(rarity) +
                      ComputeSizePowerOffset(size);
  return std::clamp(raw, kMinPowerLevel, kMaxPowerLevel);
}

BossTierSpec ResolveBossTier(NodeSize size) {
  switch (size) {
    case NodeSize::Small:
      return BossTierSpec{UnitRarity::Elite, 1, 0, 0, 0, 1};
    case NodeSize::Medium:
      return BossTierSpec{UnitRarity::Boss, 1, 0, 0, 0, 1};
    case NodeSize::Large:
      return BossTierSpec{UnitRarity::Boss, 1, 0, 0, 2, 1};
    case NodeSize::VeryLarge:
      return BossTierSpec{UnitRarity::Boss, 1, 1, 2, 2, 3};
  }
  return BossTierSpec{UnitRarity::Elite, 1, 0, 0, 0, 1};
}

UnitRarity RoleDefaultRarity(GarrisonRole role) {
  switch (role) {
    case GarrisonRole::GuardRanged:
    case GarrisonRole::GuardMelee:
      return UnitRarity::Normal;
    case GarrisonRole::Heavy:
    case GarrisonRole::Sniper:
    case GarrisonRole::Netrunner:
      return UnitRarity::Specialist;
    case GarrisonRole::Elite:
      return UnitRarity::Elite;
  }
  return UnitRarity::Normal;
}

int32_t ComputeNodeInfluence(NodeSize size, bool is_hq) {
  if (is_hq || size == NodeSize::VeryLarge) {
    return 5;
  }
  switch (size) {
    case NodeSize::Small: return 1;
    case NodeSize::Medium: return 2;
    case NodeSize::Large: return 3;
    case NodeSize::VeryLarge: return 5;
  }
  return 1;
}

std::string ResolveFactionTemplateKey(int32_t faction_id, OrgKind player_org_kind) {
  if (faction_id >= kPlayerFactionIdBase) {
    return player_org_kind == OrgKind::Corporation ? "Afterlife" : "Afterlife";
  }
  switch (faction_id) {
    case 1:  return "Maelstrom";
    case 2:  return "TygerClaws";
    case 3:  return "Valentinos";
    case 4:  return "SixthStreet";
    case 5:  return "VoodooBoys";
    case 6:  return "Animals";
    case 7:  return "Scavengers";
    case 8:  return "Wraiths";
    case 9:  return "Aldecaldos";
    case 10: return "Barghest";
    case 11: return "TheMox";
    case 20: return "Arasaka";
    case 21: return "Militech";
    case 22: return "KangTao";
    case 23: return "Biotechnica";
    case 43: return "Petrochem";
    case 50: return "NCPD";
    case 53: return "Afterlife";
    default: return "Scavengers";
  }
}

const char* GarrisonRoleName(GarrisonRole role) {
  switch (role) {
    case GarrisonRole::GuardRanged: return "GuardRanged";
    case GarrisonRole::GuardMelee:  return "GuardMelee";
    case GarrisonRole::Heavy:       return "Heavy";
    case GarrisonRole::Sniper:      return "Sniper";
    case GarrisonRole::Netrunner:   return "Netrunner";
    case GarrisonRole::Elite:       return "Elite";
  }
  return "GuardRanged";
}

const char* GearBracketName(GearBracket bracket) {
  switch (bracket) {
    case GearBracket::Low:  return "Low";
    case GearBracket::Mid:  return "Mid";
    case GearBracket::High: return "High";
  }
  return "Low";
}

const char* BossArchetypeName(BossArchetype archetype) {
  switch (archetype) {
    case BossArchetype::Enforcer:  return "Enforcer";
    case BossArchetype::Netrunner: return "Netrunner";
    case BossArchetype::Vanguard:  return "Vanguard";
  }
  return "Vanguard";
}

std::string FormatUnitRecordId(
    const std::string& faction_template_key,
    GarrisonRole role,
    GearBracket bracket) {
  return "Character.NA_" + faction_template_key + "_" +
         GarrisonRoleName(role) + "_" + GearBracketName(bracket);
}

std::string FormatBossRecordId(
    const std::string& faction_template_key,
    BossArchetype archetype,
    UnitRarity boss_rarity) {
  const char* tier_suffix = (boss_rarity == UnitRarity::Boss) ? "Boss" : "Elite";
  return "Character.NA_Boss_" + faction_template_key + "_" +
         BossArchetypeName(archetype) + "_" + tier_suffix;
}

GarrisonBudget ComputeGarrisonBudget(
    NodeSize size,
    NodeType type,
    uint64_t node_seed,
    float strength_ratio) {
  GarrisonBudget b;
  b.size = size;
  b.type = type;

  const BossTierSpec boss_spec = ResolveBossTier(size);
  b.zone_count = boss_spec.zone_count;

  const SizeBounds sb = BoundsForSize(size);
  SplitMix64 rng(node_seed ^
                 (static_cast<uint64_t>(size) << 40U) ^
                 (static_cast<uint64_t>(type) << 32U));

  if (type == NodeType::Economy) {
    b.civilian_crowd_target = rng.NextRange(sb.econ_civ_min, sb.econ_civ_max);
  }

  const float clamped_strength = std::clamp(strength_ratio, 0.0F, 1.0F);
  if (clamped_strength <= 0.0F) {
    return b;
  }

  // 1. Pick full-strength target headcount inside [min_total, max_total] with node-type bias.
  const int32_t span = sb.max_total - sb.min_total;
  int32_t total_lo = sb.min_total;
  int32_t total_hi = sb.max_total;
  switch (type) {
    case NodeType::Military:
      // Top of range (+25-30% within cap).
      total_lo = sb.min_total + (span * 3) / 4;
      total_hi = sb.max_total;
      break;
    case NodeType::Tech:
      total_lo = sb.min_total + span / 4;
      total_hi = sb.max_total - span / 5;
      break;
    case NodeType::Espionage:
      total_lo = sb.min_total + span / 6;
      total_hi = sb.max_total - span / 3;
      break;
    case NodeType::Economy:
      total_lo = sb.min_total;
      total_hi = sb.max_total - span / 3;
      break;
  }
  total_lo = std::clamp(total_lo, sb.min_total, sb.max_total);
  total_hi = std::clamp(total_hi, total_lo, sb.max_total);
  int32_t total = rng.NextRange(total_lo, total_hi);

  // 2. Bosses & sub-lieutenants.
  b.primary_bosses = boss_spec.primary_boss_count;
  if (boss_spec.max_sub_lt_count > boss_spec.min_sub_lt_count) {
    b.sub_lieutenants = (type == NodeType::Military)
                            ? boss_spec.max_sub_lt_count
                            : rng.NextRange(boss_spec.min_sub_lt_count, boss_spec.max_sub_lt_count);
  } else {
    b.sub_lieutenants = boss_spec.min_sub_lt_count;
  }
  int32_t total_bosses = b.primary_bosses + b.sub_lieutenants;

  // 3. Netrunners (hard rule: always >= 1 on any occupied node).
  int32_t netrunners = sb.min_net;
  if (sb.max_net > sb.min_net) {
    if (type == NodeType::Espionage) {
      netrunners = sb.max_net;
    } else if (type == NodeType::Tech) {
      netrunners = (rng.NextRange(0, 99) < 75) ? sb.max_net : sb.min_net;
    } else {
      netrunners = rng.NextRange(sb.min_net, sb.max_net);
    }
  }

  // Ensure remaining slots fit [min_spec + min_guards, max_spec + max_guards].
  const int32_t min_non_boss_non_net = sb.min_spec + sb.min_guards;
  const int32_t max_non_boss_non_net = sb.max_spec + sb.max_guards;
  int32_t rem = total - total_bosses - netrunners;
  if (rem < min_non_boss_non_net) {
    // Trim sub-Lts or netrunners within allowed bounds before raising total.
    while (rem < min_non_boss_non_net && b.sub_lieutenants > boss_spec.min_sub_lt_count) {
      --b.sub_lieutenants;
      --total_bosses;
      ++rem;
    }
    while (rem < min_non_boss_non_net && netrunners > sb.min_net) {
      --netrunners;
      ++rem;
    }
    if (rem < min_non_boss_non_net) {
      total += (min_non_boss_non_net - rem);
      rem = min_non_boss_non_net;
    }
  } else if (rem > max_non_boss_non_net) {
    while (rem > max_non_boss_non_net && netrunners < sb.max_net) {
      ++netrunners;
      --rem;
    }
    if (rem > max_non_boss_non_net) {
      total -= (rem - max_non_boss_non_net);
      rem = max_non_boss_non_net;
    }
  }

  // 4. Specialists & Elites vs Rank-and-File Guards (strictly inside §1 table bounds).
  const int32_t spec_lo = std::max(sb.min_spec, rem - sb.max_guards);
  const int32_t spec_hi = std::min(sb.max_spec, rem - sb.min_guards);
  int32_t spec_total = spec_lo;
  if (spec_hi > spec_lo) {
    switch (type) {
      case NodeType::Military:
        spec_total = rng.NextRange(std::max(spec_lo, spec_hi - 1), spec_hi);
        break;
      case NodeType::Espionage:
        spec_total = rng.NextRange(spec_lo, std::min(spec_hi, spec_lo + (spec_hi - spec_lo) / 2));
        break;
      case NodeType::Tech:
        spec_total = rng.NextRange(spec_lo + (spec_hi - spec_lo) / 2, spec_hi);
        break;
      case NodeType::Economy:
        spec_total = rng.NextRange(spec_lo, spec_hi);
        break;
    }
  }
  int32_t guards_total = rem - spec_total;

  // Apply weakened garrison scaling if strength_ratio < 1.0 (preserving boss + >= 1 netrunner).
  if (clamped_strength < 0.999F) {
    const int32_t target_total = std::max(
        2, static_cast<int32_t>(std::lround(static_cast<double>(total) * clamped_strength)));
    int32_t drop = total - target_total;
    if (drop > 0) {
      const int32_t drop_g = std::min(guards_total, (drop * 2 + 2) / 3);
      guards_total -= drop_g;
      drop -= drop_g;

      const int32_t drop_s = std::min(spec_total, drop);
      spec_total -= drop_s;
      drop -= drop_s;

      const int32_t drop_sub = std::min(b.sub_lieutenants, drop);
      b.sub_lieutenants -= drop_sub;
      total_bosses -= drop_sub;
      drop -= drop_sub;

      const int32_t drop_net = std::min(std::max(0, netrunners - 1), drop);
      netrunners -= drop_net;
      drop -= drop_net;

      if (drop > 0 && guards_total > 0) {
        const int32_t extra_g = std::min(guards_total, drop);
        guards_total -= extra_g;
        drop -= extra_g;
      }
      total = total_bosses + netrunners + spec_total + guards_total;
    }
  }

  // 5. Split Specialists & Elites into (Elites [incl. boss guards], Heavies, Snipers).
  b.boss_guard_elites = std::min(boss_spec.boss_guard_elites, spec_total);
  b.elites = b.boss_guard_elites;
  int32_t spec_rem = spec_total - b.elites;

  // Economy nodes place an Elite near the VIP/boss office when budget allows.
  if (type == NodeType::Economy && b.elites == 0 && spec_rem > 0) {
    ++b.elites;
    --spec_rem;
  }

  while (spec_rem > 0) {
    const int32_t roll = rng.NextRange(0, 99);
    switch (type) {
      case NodeType::Military:
        if (roll < 40) {
          ++b.heavies;
        } else if (roll < 72) {
          ++b.snipers;
        } else {
          ++b.elites;
        }
        break;
      case NodeType::Espionage:
        // Minimal heavies on espionage nodes.
        if (roll < 55) {
          ++b.snipers;
        } else {
          ++b.elites;
        }
        break;
      case NodeType::Tech:
        if (roll < 45) {
          ++b.snipers;
        } else if (roll < 75) {
          ++b.elites;
        } else {
          ++b.heavies;
        }
        break;
      case NodeType::Economy:
        if (roll < 45) {
          ++b.elites;
        } else if (roll < 80) {
          ++b.heavies;
        } else {
          ++b.snipers;
        }
        break;
    }
    --spec_rem;
  }

  // 6. Split rank-and-file guards into ranged vs melee (economy clubs lean more melee/bouncers).
  double melee_share = 0.25;
  if (type == NodeType::Economy) {
    melee_share = 0.35;
  } else if (type == NodeType::Military || type == NodeType::Espionage) {
    melee_share = 0.20;
  }
  b.guard_melee = static_cast<int32_t>(std::lround(static_cast<double>(guards_total) * melee_share));
  b.guard_melee = std::clamp(b.guard_melee, 0, guards_total);
  b.guard_ranged = guards_total - b.guard_melee;

  // 7. Split non-boss units into Posts vs Patrols.
  b.netrunners = netrunners;
  b.total_security = total_bosses + b.netrunners + b.SpecialistsAndElites() + b.RankAndFileGuards();
  b.netrunner_intel_bonus = b.netrunners;

  const int32_t non_boss = b.total_security - total_bosses;
  double patrol_ratio = sb.base_patrol_ratio;
  if (type == NodeType::Military) {
    patrol_ratio = std::min(0.60, patrol_ratio + 0.08);
  }
  const int32_t min_posts = b.boss_guard_elites;
  const int32_t max_patrols = std::max(0, non_boss - min_posts);
  b.patrol_units = std::clamp(
      static_cast<int32_t>(std::lround(static_cast<double>(non_boss) * patrol_ratio)),
      0,
      max_patrols);
  b.post_units = non_boss - b.patrol_units;
  return b;
}

GarrisonRoster BuildGarrisonRoster(const GarrisonSpec& spec) {
  GarrisonRoster out;
  out.faction_template_key = ResolveFactionTemplateKey(spec.faction_id, spec.player_org_kind);
  out.gear_bracket = ComputeGearBracket(spec.fielded_tier);
  out.influence = ComputeNodeInfluence(spec.size, spec.is_hq);

  const BossTierSpec boss_tier = ResolveBossTier(spec.size);
  out.primary_boss_rarity = boss_tier.primary_boss_rarity;

  SplitMix64 rng(spec.node_seed ^ 0xD6E8FEB86659FD93ULL);
  out.boss_archetype = PickBossArchetype(spec.type, rng);
  out.budget = ComputeGarrisonBudget(spec.size, spec.type, spec.node_seed, spec.strength_ratio);

  const auto& b = out.budget;
  if (b.total_security <= 0) {
    return out;
  }

  out.units.reserve(static_cast<size_t>(b.total_security));
  int32_t next_slot = 0;

  // 1. Primary boss (HQ Leader / Lieutenant Boss).
  if (b.primary_bosses > 0) {
    GarrisonUnitSpec boss;
    boss.slot_index = next_slot++;
    boss.record_id = !spec.lore_boss_record_id.empty()
                         ? spec.lore_boss_record_id
                         : FormatBossRecordId(
                               out.faction_template_key,
                               out.boss_archetype,
                               out.primary_boss_rarity);
    boss.role = (out.boss_archetype == BossArchetype::Netrunner)
                    ? GarrisonRole::Netrunner
                    : (out.boss_archetype == BossArchetype::Enforcer
                           ? GarrisonRole::Heavy
                           : GarrisonRole::Elite);
    boss.rarity = out.primary_boss_rarity;
    boss.power_level = ComputePowerLevel(spec.fielded_tier, boss.rarity, spec.size);
    boss.assignment = AssignmentKind::BossSeat;
    boss.zone_index = 0;
    boss.is_boss = true;
    out.units.push_back(std::move(boss));
  }

  // 2. Sub-lieutenants (very_large multi-zone HQs).
  for (int32_t i = 0; i < b.sub_lieutenants; ++i) {
    const BossArchetype sub_arch = static_cast<BossArchetype>((static_cast<int32_t>(out.boss_archetype) + i + 1) % 3);
    GarrisonUnitSpec sub;
    sub.slot_index = next_slot++;
    sub.record_id = FormatBossRecordId(out.faction_template_key, sub_arch, UnitRarity::Elite);
    sub.role = GarrisonRole::Elite;
    sub.rarity = UnitRarity::Elite;
    sub.power_level = ComputePowerLevel(spec.fielded_tier, UnitRarity::Elite, spec.size);
    sub.assignment = AssignmentKind::BossSeat;
    sub.zone_index = (i + 1) % std::max(1, b.zone_count);
    sub.is_boss = true;
    sub.is_sub_lt = true;
    out.units.push_back(std::move(sub));
  }

  // 3. Emit non-boss units: boss-guard Elites first (pinned to boss zone Post), then rest.
  int32_t posts_left = b.post_units;
  int32_t patrols_left = b.patrol_units;
  int32_t zone_cursor = 0;

  auto next_zone = [&]() -> int32_t {
    const int32_t z = zone_cursor % std::max(1, b.zone_count);
    ++zone_cursor;
    return z;
  };

  auto push_unit = [&](GarrisonRole role, bool boss_guard, bool prefer_post) {
    GarrisonUnitSpec u;
    u.slot_index = next_slot++;
    u.record_id = FormatUnitRecordId(out.faction_template_key, role, out.gear_bracket);
    u.role = role;
    u.rarity = RoleDefaultRarity(role);
    u.power_level = ComputePowerLevel(spec.fielded_tier, u.rarity, spec.size);
    u.is_boss_guard = boss_guard;
    u.zone_index = boss_guard ? 0 : next_zone();

    if (boss_guard || (prefer_post && posts_left > 0) || patrols_left <= 0) {
      u.assignment = AssignmentKind::Post;
      if (posts_left > 0) {
        --posts_left;
      }
    } else {
      u.assignment = AssignmentKind::Patrol;
      --patrols_left;
    }
    out.units.push_back(std::move(u));
  };

  for (int32_t i = 0; i < b.boss_guard_elites; ++i) {
    push_unit(GarrisonRole::Elite, true, true);
  }
  for (int32_t i = 0; i < b.netrunners; ++i) {
    // Netrunners prefer overwatch/security-room posts.
    push_unit(GarrisonRole::Netrunner, false, true);
  }
  for (int32_t i = 0; i < b.snipers; ++i) {
    push_unit(GarrisonRole::Sniper, false, true);
  }
  for (int32_t i = b.boss_guard_elites; i < b.elites; ++i) {
    push_unit(GarrisonRole::Elite, false, (i % 2) == 0);
  }
  for (int32_t i = 0; i < b.heavies; ++i) {
    push_unit(GarrisonRole::Heavy, false, (i % 2) == 0);
  }
  for (int32_t i = 0; i < b.guard_ranged; ++i) {
    // Interleave posts and patrols evenly across rank-and-file guards.
    const bool prefer_post = (posts_left >= patrols_left);
    push_unit(GarrisonRole::GuardRanged, false, prefer_post);
  }
  for (int32_t i = 0; i < b.guard_melee; ++i) {
    const bool prefer_post = (posts_left >= patrols_left);
    push_unit(GarrisonRole::GuardMelee, false, prefer_post);
  }

  return out;
}

}  // namespace neon::sim
