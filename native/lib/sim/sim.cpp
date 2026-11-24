#include "sim.hpp"

#include <algorithm>
#include <deque>
#include <utility>

namespace neon::sim {

SimEngine::SimEngine(std::vector<TerritoryDef> defs) : defs_(std::move(defs)) {
  std::sort(defs_.begin(), defs_.end(), [](const TerritoryDef& a, const TerritoryDef& b) {
    return a.sub_territory_id < b.sub_territory_id;
  });
}

SimState SimEngine::CreateInitialState(uint64_t rng_seed, int32_t start_seconds) const {
  SimState state;
  state.clock.revision = 0;
  state.clock.last_cycle_seconds = start_seconds;
  state.clock.cycle_index = 0;
  state.clock.rng_seed = rng_seed;
  state.clock.rng_counter = 0;
  state.territories.reserve(defs_.size());
  for (const auto& d : defs_) {
    TerritoryRuntime tr;
    tr.sub_territory_id = d.sub_territory_id;
    tr.owner_faction_id = d.initial_owner_faction_id;
    tr.control_level = 1.0F;
    state.territories.push_back(tr);
  }
  return state;
}

const TerritoryDef* SimEngine::FindDef(int32_t sub_territory_id) const {
  auto it = std::lower_bound(
      defs_.begin(), defs_.end(), sub_territory_id,
      [](const TerritoryDef& d, int32_t id) { return d.sub_territory_id < id; });
  if (it != defs_.end() && it->sub_territory_id == sub_territory_id) {
    return &(*it);
  }
  return nullptr;
}

TerritoryRuntime* SimEngine::FindTerritory(SimState& state, int32_t sub_territory_id) {
  for (auto& t : state.territories) {
    if (t.sub_territory_id == sub_territory_id) {
      return &t;
    }
  }
  return nullptr;
}

bool SimEngine::IsValidRaidCombatant(
    bool is_crowd,
    bool is_civilian,
    bool is_vendor,
    bool is_hostile,
    int32_t affiliation_enum) {
  if (is_crowd || is_civilian || is_vendor) {
    return false;
  }
  // Cyberpunk 2077 gamedataAffiliation non-combatant / sentinel values:
  // Civilian=7, Classified=8, REDACTED=19, Unaffiliated=30, Unknown=32, Count=44, Invalid=45.
  switch (affiliation_enum) {
    case 7:  // Civilian
    case 30: // Unaffiliated
    case 32: // Unknown
    case 44: // Count
    case 45: // Invalid
      return false;
    default:
      break;
  }
  // Require either a valid combatant faction affiliation or explicit hostile attitude.
  return affiliation_enum >= 0 || is_hostile;
}

const TerritoryRuntime* SimEngine::FindTerritoryConst(
    const SimState& state, int32_t sub_territory_id) {
  for (const auto& t : state.territories) {
    if (t.sub_territory_id == sub_territory_id) {
      return &t;
    }
  }
  return nullptr;
}

OrgRuntime* SimEngine::FindPlayerOrg(SimState& state) {
  if (state.orgs.empty()) {
    return nullptr;
  }
  return &state.orgs.front();
}

const OrgRuntime* SimEngine::FindPlayerOrgConst(const SimState& state) {
  if (state.orgs.empty()) {
    return nullptr;
  }
  return &state.orgs.front();
}

MissionRuntime* SimEngine::FindMission(SimState& state, int32_t mission_id) {
  for (auto& m : state.missions) {
    if (m.mission_id == mission_id) {
      return &m;
    }
  }
  return nullptr;
}

const MissionRuntime* SimEngine::FindActiveCombatMissionConst(const SimState& state) {
  for (auto it = state.missions.rbegin(); it != state.missions.rend(); ++it) {
    if (it->kind == MissionKind::Combat &&
        (it->state == MissionState::Active || it->state == MissionState::Offered)) {
      return &(*it);
    }
  }
  return nullptr;
}

int32_t SimEngine::CountOwnedTerritories(const SimState& state, int32_t faction_id) {
  int32_t count = 0;
  for (const auto& t : state.territories) {
    if (t.owner_faction_id == faction_id) {
      ++count;
    }
  }
  return count;
}

int64_t SimEngine::ComputeCycleIncome(const SimState& state, int32_t faction_id) const {
  int64_t total = 0;
  for (const auto& t : state.territories) {
    if (t.owner_faction_id != faction_id) {
      continue;
    }
    const auto* def = FindDef(t.sub_territory_id);
    if (def != nullptr) {
      total += static_cast<int64_t>(def->base_income_per_cycle);
    }
  }
  return total;
}

PauseMenuAction SimEngine::ResolvePauseMenuAction(
    const SimState& state, bool ascendancy_enabled) {
  if (!ascendancy_enabled) {
    return PauseMenuAction::ActivateAscendancy;
  }
  if (FindPlayerOrgConst(state) == nullptr) {
    return PauseMenuAction::FoundGangHere;
  }
  if (FindActiveCombatMissionConst(state) == nullptr) {
    return PauseMenuAction::LaunchRivalRaid;
  }
  return PauseMenuAction::ShowStatus;
}

std::string SimEngine::FormatPauseMenuLabel(
    const SimState& state, bool ascendancy_enabled) {
  switch (ResolvePauseMenuAction(state, ascendancy_enabled)) {
    case PauseMenuAction::ActivateAscendancy:
      return "NEON ASCENDANCY: START SANDBOX";
    case PauseMenuAction::FoundGangHere:
      return "NEON ASCENDANCY: FOUND GANG HERE";
    case PauseMenuAction::LaunchRivalRaid:
      return "NEON ASCENDANCY: LAUNCH RIVAL RAID";
    case PauseMenuAction::ShowStatus:
      return "NEON ASCENDANCY: GANG STATUS";
    case PauseMenuAction::None:
      break;
  }
  return "NEON ASCENDANCY";
}

std::string SimEngine::FormatTerritoryTooltipDesc(
    const std::string& district_name,
    const std::string& owner_name,
    int32_t base_income_per_cycle,
    bool is_player_owned,
    bool is_active_raid_target,
    int32_t raid_kills_done,
    int32_t raid_kills_required) {
  std::string out = "District: " + district_name +
                    "\nOwner: " + owner_name +
                    "\nDaily Income: " + std::to_string(base_income_per_cycle) + " eb";
  if (is_player_owned) {
    out += "\n[YOUR TURF]";
  } else if (is_active_raid_target) {
    out += "\n[ACTIVE RAID: " + std::to_string(raid_kills_done) + "/" +
           std::to_string(raid_kills_required) + " hostiles]";
  }
  return out;
}

std::string SimEngine::FormatStatusSummary(
    const SimState& state, const std::string& active_target_name) const {
  const auto* org = FindPlayerOrgConst(state);
  if (org == nullptr) {
    return "Neon Ascendancy active. No gang founded yet.";
  }
  const int32_t owned = CountOwnedTerritories(state, org->faction_id);
  const int64_t daily = ComputeCycleIncome(state, org->faction_id);
  std::string s = org->display_name + " | Turf: " + std::to_string(owned) +
                  " | Income: " + std::to_string(daily) + " eb/day";
  const auto* mission = FindActiveCombatMissionConst(state);
  if (mission != nullptr) {
    s += " | Raid: " + active_target_name + " (" + std::to_string(mission->kills_done) + "/" +
         std::to_string(mission->kills_required) + ")";
  }
  return s;
}

void SimEngine::ProcessEventQueue(
    SimState& state,
    std::vector<SimEvent> initial,
    CommandResult& out) const {
  std::deque<SimEvent> queue(initial.begin(), initial.end());
  int32_t processed = 0;

  while (!queue.empty() && processed < kMaxEventDepth) {
    const SimEvent evt = queue.front();
    queue.pop_front();
    ++processed;
    out.emitted.push_back(evt);

    switch (evt.type) {
      case SimEventType::MissionCompleted: {
        // Territory pillar reacts: v0.1.0 immediate flip to player org.
        auto* mission = FindMission(state, evt.a);
        auto* org = FindPlayerOrg(state);
        if (mission != nullptr && org != nullptr && mission->kind == MissionKind::Combat) {
          auto* terr = FindTerritory(state, mission->sub_territory_id);
          if (terr != nullptr && terr->owner_faction_id != org->faction_id) {
            const int32_t old_owner = terr->owner_faction_id;
            terr->owner_faction_id = org->faction_id;
            terr->contested_by_faction_id = 0;
            terr->control_level = 1.0F;
            terr->heat += 15.0F;
            terr->last_flip_revision = state.clock.revision;
            terr->last_flip_seconds = evt.game_seconds;
            queue.push_back(SimEvent{
                SimEventType::TerritoryOwnerChanged,
                evt.game_seconds,
                terr->sub_territory_id,
                org->faction_id,
                static_cast<int64_t>(old_owner),
            });
          }
          // Org pillar reacts: notoriety + mission reward payout.
          org->notoriety += 10.0F;
          org->heat += 5.0F;
          org->treasury_eddies += mission->reward_eddies;
          out.payout_eddies += mission->reward_eddies;
        }
        break;
      }

      case SimEventType::TerritoryOwnerChanged: {
        // Org pillar reacts: gaining turf increases notoriety and local heat.
        auto* org = FindPlayerOrg(state);
        if (org != nullptr && evt.b == org->faction_id) {
          org->notoriety += 5.0F;
          queue.push_back(SimEvent{
              SimEventType::HeatChanged,
              evt.game_seconds,
              evt.a,
              evt.b,
              15,
          });
        }
        break;
      }

      case SimEventType::CycleElapsed: {
        // Org pillar settles periodic income for each elapsed cycle.
        auto* org = FindPlayerOrg(state);
        if (org != nullptr) {
          const int64_t gross = ComputeCycleIncome(state, org->faction_id);
          const int64_t net =
              std::max<int64_t>(0, gross - static_cast<int64_t>(org->upkeep_per_cycle));
          if (net > 0) {
            org->treasury_eddies += net;
            out.payout_eddies += net;
            queue.push_back(SimEvent{
                SimEventType::IncomeSettled,
                evt.game_seconds,
                org->org_id,
                org->faction_id,
                net,
            });
          }
        }
        // Territory heat cools gently per cycle.
        for (auto& t : state.territories) {
          if (t.heat > 0.0F) {
            t.heat = std::max(0.0F, t.heat - 2.0F);
          }
        }
        break;
      }

      case SimEventType::OrgFounded:
      case SimEventType::MissionOffered:
      case SimEventType::MissionFailed:
      case SimEventType::HeatChanged:
      case SimEventType::IncomeSettled:
        break;
    }
  }
}

CommandResult SimEngine::FoundGang(
    SimState& state,
    const std::string& display_name,
    int32_t home_sub_territory_id,
    int32_t game_seconds) const {
  CommandResult res;
  if (display_name.empty()) {
    res.error = "gang display_name must not be empty";
    return res;
  }
  if (!state.orgs.empty()) {
    res.error = "player organization already exists";
    return res;
  }
  auto* home = FindTerritory(state, home_sub_territory_id);
  if (home == nullptr) {
    res.error = "unknown home_sub_territory_id";
    return res;
  }

  OrgRuntime org;
  org.org_id = 1;
  org.kind = OrgKind::Gang;
  org.display_name = display_name;
  org.faction_id = kPlayerFactionIdBase;
  org.founded_revision = state.clock.revision;
  org.founded_seconds = game_seconds;
  state.orgs.push_back(org);

  const int32_t old_owner = home->owner_faction_id;
  home->owner_faction_id = org.faction_id;
  home->control_level = 1.0F;
  home->last_flip_revision = state.clock.revision;
  home->last_flip_seconds = game_seconds;

  res.ok = true;
  ProcessEventQueue(
      state,
      {
          SimEvent{SimEventType::OrgFounded, game_seconds, org.org_id, org.faction_id, 0},
          SimEvent{SimEventType::TerritoryOwnerChanged, game_seconds, home_sub_territory_id,
                   org.faction_id, static_cast<int64_t>(old_owner)},
      },
      res);
  return res;
}

CommandResult SimEngine::OfferCombatMission(
    SimState& state,
    int32_t sub_territory_id,
    int32_t control_center_id,
    int32_t reward_eddies,
    int32_t game_seconds,
    int32_t kills_required) const {
  CommandResult res;
  auto* org = FindPlayerOrg(state);
  if (org == nullptr) {
    res.error = "no player organization founded";
    return res;
  }
  if (FindActiveCombatMissionConst(state) != nullptr) {
    res.error = "an active combat mission is already in progress";
    return res;
  }
  auto* terr = FindTerritory(state, sub_territory_id);
  if (terr == nullptr) {
    res.error = "unknown sub_territory_id";
    return res;
  }
  if (terr->owner_faction_id == org->faction_id) {
    res.error = "cannot generate rival mission on player-owned sub-territory";
    return res;
  }

  int32_t next_id = 1;
  for (const auto& m : state.missions) {
    next_id = std::max(next_id, m.mission_id + 1);
  }
  state.clock.rng_counter += 1;

  MissionRuntime m;
  m.mission_id = next_id;
  m.kind = MissionKind::Combat;
  m.state = MissionState::Active;
  m.issuer_faction_id = org->faction_id;
  m.target_faction_id = terr->owner_faction_id;
  m.sub_territory_id = sub_territory_id;
  m.control_center_id = control_center_id;
  m.seed = state.clock.rng_seed ^ (state.clock.rng_counter * 0x9E3779B97F4A7C15ULL);
  m.difficulty = 1.0F;
  m.reward_eddies = std::max(0, reward_eddies);
  m.created_seconds = game_seconds;
  m.kills_required = std::max(1, kills_required);
  m.kills_done = 0;
  state.missions.push_back(m);

  res.ok = true;
  ProcessEventQueue(
      state,
      {SimEvent{SimEventType::MissionOffered, game_seconds, m.mission_id, m.target_faction_id,
                m.sub_territory_id}},
      res);
  return res;
}

CommandResult SimEngine::RecordMissionKill(
    SimState& state,
    int32_t mission_id,
    int32_t game_seconds) const {
  CommandResult res;
  auto* m = FindMission(state, mission_id);
  if (m == nullptr) {
    res.error = "unknown mission_id";
    return res;
  }
  if (m->kind != MissionKind::Combat ||
      (m->state != MissionState::Active && m->state != MissionState::Offered)) {
    res.error = "mission is not an active combat mission";
    return res;
  }

  m->kills_done += 1;
  if (m->kills_done >= m->kills_required) {
    return CompleteMission(state, mission_id, game_seconds);
  }

  res.ok = true;
  return res;
}

CommandResult SimEngine::CompleteMission(
    SimState& state,
    int32_t mission_id,
    int32_t game_seconds) const {
  CommandResult res;
  auto* m = FindMission(state, mission_id);
  if (m == nullptr) {
    res.error = "unknown mission_id";
    return res;
  }
  if (m->state != MissionState::Active && m->state != MissionState::Offered) {
    res.error = "mission already resolved";
    return res;
  }
  m->state = MissionState::Succeeded;
  m->kills_done = std::max(m->kills_done, m->kills_required);
  m->resolved_seconds = game_seconds;
  m->resolved_revision = state.clock.revision;

  res.ok = true;
  ProcessEventQueue(
      state,
      {SimEvent{SimEventType::MissionCompleted, game_seconds, m->mission_id, m->target_faction_id,
                m->reward_eddies}},
      res);
  return res;
}

CommandResult SimEngine::AdvanceTime(
    SimState& state,
    int32_t current_game_seconds,
    int32_t cycle_seconds) const {
  CommandResult res;
  if (cycle_seconds <= 0) {
    res.error = "cycle_seconds must be positive";
    return res;
  }
  res.ok = true;
  if (current_game_seconds <= state.clock.last_cycle_seconds) {
    return res;
  }

  const int32_t delta = current_game_seconds - state.clock.last_cycle_seconds;
  const int32_t cycles = delta / cycle_seconds;
  if (cycles <= 0) {
    return res;
  }

  std::vector<SimEvent> ticks;
  ticks.reserve(static_cast<size_t>(std::min(cycles, 30)));
  // Cap catch-up per call at 30 cycles to keep event queue bounded on huge time jumps.
  const int32_t run_cycles = std::min(cycles, 30);
  for (int32_t i = 0; i < run_cycles; ++i) {
    state.clock.cycle_index += 1;
    state.clock.last_cycle_seconds += cycle_seconds;
    ticks.push_back(SimEvent{
        SimEventType::CycleElapsed,
        state.clock.last_cycle_seconds,
        state.clock.cycle_index,
        0,
        0,
    });
  }
  // If more than 30 cycles skipped at once, advance clock cleanly without dropping remainder.
  if (cycles > run_cycles) {
    state.clock.last_cycle_seconds += (cycles - run_cycles) * cycle_seconds;
    state.clock.cycle_index += (cycles - run_cycles);
  }

  ProcessEventQueue(state, std::move(ticks), res);
  return res;
}

} // namespace neon::sim
