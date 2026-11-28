#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <filesystem>
#include <iostream>
#include <string>
#include <unordered_set>
#include <vector>

#include "era.hpp"
#include "sim.hpp"
#include "store.hpp"

namespace {

int g_failures = 0;

#define NC_CHECK(expr)                                                               \
  do {                                                                               \
    if (!(expr)) {                                                                   \
      std::cerr << "[FAIL] " << __FILE__ << ":" << __LINE__ << ": " #expr << "\n";  \
      ++g_failures;                                                                  \
      return;                                                                        \
    }                                                                                \
  } while (0)

const neon::sim::TerritoryRuntime* FindTerr(const neon::sim::SimState& st, int32_t id) {
  for (const auto& t : st.territories) {
    if (t.sub_territory_id == id) return &t;
  }
  return nullptr;
}

void TestEraAndSanitizerPolicy() {
  // Disabled sanitizer never emits unlock or suppression flags.
  {
    neon::sim::EraFacts f;
    f.q001_done = 1;
    f.watson_prolog_lock = 1;
    const auto p = neon::sim::ComputeSanitizerPolicy(f, false);
    NC_CHECK(p.era == neon::sim::WorldEra::Act1PreHeist);
    NC_CHECK(!p.unlock_city && !p.unlock_act2_content && !p.suppress_campaign && !p.suppress_johnny);
  }

  // Enabled in Act 1 pre-Heist unlocks city & Act 2 content, suppresses campaign, skips Johnny.
  {
    neon::sim::EraFacts f;
    f.q001_done = 1;
    f.watson_prolog_lock = 1;
    const auto p = neon::sim::ComputeSanitizerPolicy(f, true);
    NC_CHECK(p.era == neon::sim::WorldEra::Act1PreHeist);
    NC_CHECK(p.unlock_city);
    NC_CHECK(p.unlock_act2_content);
    NC_CHECK(p.suppress_campaign);
    NC_CHECK(!p.suppress_johnny);
    const uint32_t mask = neon::sim::PackSanitizerPolicyMask(p);
    NC_CHECK((mask & 1U) != 0U);
    NC_CHECK((mask & 2U) != 0U);
    NC_CHECK((mask & 4U) != 0U);
    NC_CHECK((mask & 8U) == 0U);
    NC_CHECK(((mask >> 8U) & 0xFFU) == static_cast<uint32_t>(neon::sim::WorldEra::Act1PreHeist));
  }

  // PLStandalone via packed bitmask.
  {
    const uint32_t bits = (1U << 0U) | (1U << 7U) | (1U << 15U); // ep1_standalone + side_content + unlock
    const auto f = neon::sim::UnpackEraFactsMask(bits);
    const auto p = neon::sim::ComputeSanitizerPolicy(f, true);
    NC_CHECK(p.era == neon::sim::WorldEra::PLStandalone);
    NC_CHECK(!p.unlock_city); // already unlocked
    NC_CHECK(!p.unlock_act2_content); // side content already active
    NC_CHECK(p.suppress_campaign);
    NC_CHECK(p.suppress_johnny);
  }

  // Clean-slate boot (Watson open + side content with zero story progress) is
  // its own era: campaign suppressed, Johnny suppression off, no unlock flags.
  {
    neon::sim::EraFacts f;
    f.watson_prolog_unlock = 1;
    f.q101_enable_side_content = 1;
    const auto p = neon::sim::ComputeSanitizerPolicy(f, true);
    NC_CHECK(p.era == neon::sim::WorldEra::CleanSlate);
    NC_CHECK(!p.unlock_city);
    NC_CHECK(!p.unlock_act2_content);
    NC_CHECK(p.suppress_campaign);
    NC_CHECK(!p.suppress_johnny);
    const uint32_t mask = neon::sim::PackSanitizerPolicyMask(p);
    NC_CHECK(((mask >> 8U) & 0xFFU) == static_cast<uint32_t>(neon::sim::WorldEra::CleanSlate));
    NC_CHECK(!strcmp(neon::sim::WorldEraName(neon::sim::WorldEra::CleanSlate), "Clean Slate"));
  }

  // CleanSlate via packed bitmask (bits 7 + 15 only).
  {
    const uint32_t bits = (1U << 7U) | (1U << 15U); // side_content + unlock, no story bits
    const auto f = neon::sim::UnpackEraFactsMask(bits);
    NC_CHECK(neon::sim::ClassifyWorldEra(f) == neon::sim::WorldEra::CleanSlate);
  }

  // A sanitized vanilla save (q001_done) with the same unlock facts is NOT
  // CleanSlate: story progress exists, so Interlude classification is kept.
  {
    neon::sim::EraFacts f;
    f.q001_done = 1;
    f.watson_prolog_unlock = 1;
    f.q101_enable_side_content = 1;
    const auto p = neon::sim::ComputeSanitizerPolicy(f, true);
    NC_CHECK(p.era == neon::sim::WorldEra::Interlude);
    NC_CHECK(p.suppress_johnny);
  }

  // Raid combatant filter must reject civilians, crowds, vendors, and Unaffiliated/Unknown.
  NC_CHECK(!neon::sim::SimEngine::IsValidRaidCombatant(true, false, false, true, 34));
  NC_CHECK(!neon::sim::SimEngine::IsValidRaidCombatant(false, true, false, true, 34));
  NC_CHECK(!neon::sim::SimEngine::IsValidRaidCombatant(false, false, true, true, 34));
  NC_CHECK(!neon::sim::SimEngine::IsValidRaidCombatant(false, false, false, true, 7));  // Civilian
  NC_CHECK(!neon::sim::SimEngine::IsValidRaidCombatant(false, false, false, true, 30)); // Unaffiliated
  NC_CHECK(!neon::sim::SimEngine::IsValidRaidCombatant(false, false, false, true, 32)); // Unknown
  NC_CHECK(neon::sim::SimEngine::IsValidRaidCombatant(false, false, false, true, 34));  // VoodooBoys
  NC_CHECK(neon::sim::SimEngine::IsValidRaidCombatant(false, false, false, false, 4));  // Barghest

  // Values > 1 (e.g. q101_enable_side_content = 2) classify identically to > 0.
  {
    neon::sim::EraFacts f;
    f.q005_done = 1;
    f.q101_enable_side_content = 2;
    f.watson_prolog_unlock = 1;
    const auto p = neon::sim::ComputeSanitizerPolicy(f, true);
    NC_CHECK(p.era == neon::sim::WorldEra::Act2);
    NC_CHECK(p.suppress_johnny);
  }

  // Safe-zone allowlist: only V's apartments, stores, and ripperdocs remain safe zones.
  {
    using neon::sim::ClassifySafeSanctuaryVariant;
    using neon::sim::IsAllowedSafeZone;
    using neon::sim::SafeSanctuaryKind;
    using neon::sim::SafeSanctuaryZone;

    // Variant classification
    NC_CHECK(ClassifySafeSanctuaryVariant(10) == SafeSanctuaryKind::PlayerApartment);   // Apartment
    NC_CHECK(ClassifySafeSanctuaryVariant(125) == SafeSanctuaryKind::PlayerApartment);  // ApartmentToPurchase
    NC_CHECK(ClassifySafeSanctuaryVariant(106) == SafeSanctuaryKind::StoreOrRipperdoc); // Ripperdoc
    NC_CHECK(ClassifySafeSanctuaryVariant(100) == SafeSanctuaryKind::StoreOrRipperdoc); // Guns
    NC_CHECK(ClassifySafeSanctuaryVariant(96) == SafeSanctuaryKind::StoreOrRipperdoc);  // Clothes
    NC_CHECK(ClassifySafeSanctuaryVariant(102) == SafeSanctuaryKind::StoreOrRipperdoc); // Meds
    NC_CHECK(ClassifySafeSanctuaryVariant(103) == SafeSanctuaryKind::StoreOrRipperdoc); // Melee
    NC_CHECK(ClassifySafeSanctuaryVariant(104) == SafeSanctuaryKind::StoreOrRipperdoc); // Netrunner
    NC_CHECK(ClassifySafeSanctuaryVariant(101) == SafeSanctuaryKind::StoreOrRipperdoc); // Junk
    NC_CHECK(ClassifySafeSanctuaryVariant(135) == SafeSanctuaryKind::StoreOrRipperdoc); // BlackMarket
    NC_CHECK(ClassifySafeSanctuaryVariant(143) == SafeSanctuaryKind::StoreOrRipperdoc); // Glamdoc
    NC_CHECK(ClassifySafeSanctuaryVariant(95) == SafeSanctuaryKind::None);              // Bar (not store)
    NC_CHECK(ClassifySafeSanctuaryVariant(98) == SafeSanctuaryKind::None);              // DropPoint
    NC_CHECK(ClassifySafeSanctuaryVariant(99) == SafeSanctuaryKind::None);              // Food stall
    NC_CHECK(ClassifySafeSanctuaryVariant(25) == SafeSanctuaryKind::None);              // DefaultQuest

    std::vector<SafeSanctuaryZone> dynamic_zones = {
        {SafeSanctuaryKind::PlayerApartment, -2100.0, -2550.0, 45.0},   // Dynamic Dogtown apartment pin
        {SafeSanctuaryKind::StoreOrRipperdoc, -1549.0, 1188.0, 18.0},   // Viktor's clinic ripperdoc
        {SafeSanctuaryKind::StoreOrRipperdoc, -1700.0, -1835.0, 60.0},  // Nearby Coastview melee shop (~50m away)
    };

    // Static fallback apartments (even with empty dynamic list).
    const std::vector<SafeSanctuaryZone> empty_zones;
    NC_CHECK(IsAllowedSafeZone(-1381.758, 1271.708, 123.065, empty_zones)); // H10
    NC_CHECK(IsAllowedSafeZone(-1505.056, 2231.156, 22.200, empty_zones));  // Northside
    NC_CHECK(IsAllowedSafeZone(-785.577, 977.945, 28.210, empty_zones));    // Japantown
    NC_CHECK(IsAllowedSafeZone(-1520.291, -976.132, 86.803, empty_zones));  // The Glen
    NC_CHECK(IsAllowedSafeZone(-1609.054, 356.505, 49.236, empty_zones));   // Corpo Plaza
    // Wrong floor below H10 apartment must NOT be safe.
    NC_CHECK(!IsAllowedSafeZone(-1381.758, 1271.708, 100.0, empty_zones));

    // Dynamic apartment & store/ripperdoc pins.
    NC_CHECK(IsAllowedSafeZone(-2110.0, -2540.0, 46.0, dynamic_zones));     // Inside Dogtown apartment
    NC_CHECK(IsAllowedSafeZone(-1545.0, 1192.0, 19.5, dynamic_zones));      // Inside Viktor's clinic
    NC_CHECK(!IsAllowedSafeZone(-1545.0, 1192.0, 30.0, dynamic_zones));     // Floor above clinic (|dz|=12 > 6)
    NC_CHECK(!IsAllowedSafeZone(-1520.0, 1188.0, 18.0, dynamic_zones));     // 29m outside clinic

    // Coastview plaza safe area from playtest must NOT be a safe zone even with a shop 50m away.
    NC_CHECK(!IsAllowedSafeZone(-1750.597, -1835.524, 60.889, dynamic_zones));

    // Vanilla mappin suppression allow/deny policy.
    NC_CHECK(neon::sim::IsSuppressedVanillaMappinVariant(25));   // DefaultQuest
    NC_CHECK(neon::sim::IsSuppressedVanillaMappinVariant(49));   // ExclamationMark
    NC_CHECK(neon::sim::IsSuppressedVanillaMappinVariant(52));   // Fixer
    NC_CHECK(neon::sim::IsSuppressedVanillaMappinVariant(87));   // QuestGiver
    NC_CHECK(neon::sim::IsSuppressedVanillaMappinVariant(126));  // NCPDGig
    NC_CHECK(neon::sim::IsSuppressedVanillaMappinVariant(133));  // WorldEncounter
    NC_CHECK(!neon::sim::IsSuppressedVanillaMappinVariant(10));  // Apartment (kept)
    NC_CHECK(!neon::sim::IsSuppressedVanillaMappinVariant(51));  // FastTravel (kept)
    NC_CHECK(!neon::sim::IsSuppressedVanillaMappinVariant(98));  // DropPoint (kept)
    NC_CHECK(!neon::sim::IsSuppressedVanillaMappinVariant(106)); // Ripperdoc (kept)
    NC_CHECK(!neon::sim::IsSuppressedVanillaMappinVariant(100)); // Gun store (kept)
  }
}

void TestWorldDbAndSpatialLookups(const std::string& world_db_path) {
  neon::store::WorldDb world;
  std::string err;
  NC_CHECK(world.Open(world_db_path, true, err));
  NC_CHECK(!world.ContentHash().empty());
  NC_CHECK(world.Factions().size() >= 30);
  NC_CHECK(world.Districts().size() == 9);
  NC_CHECK(world.SubTerritories().size() == 96);
  // Only active control centers load; only their sub-territories enter the sim.
  NC_CHECK(!world.ControlCenters().empty());
  NC_CHECK(world.ControlCenters().size() <= world.SubTerritories().size());
  NC_CHECK(world.BuildTerritoryDefs().size() == world.ControlCenters().size());
  const auto* morro = world.FindDistrict(9);
  NC_CHECK(morro != nullptr && morro->code == "morro_rock");

  // Dormant sub-territories are invisible to the runtime spatial grid.
  for (const auto& st : world.SubTerritories()) {
    if (world.FindControlCenterBySubTerritory(st.sub_territory_id) == nullptr) {
      NC_CHECK(world.LookupSubTerritoryAt(st.centroid_x, st.centroid_y) != st.sub_territory_id);
    }
  }

  // Headquarters: at most one per faction, each tied to a known faction.
  {
    std::unordered_set<int32_t> hq_factions;
    for (const auto& hq : world.FactionHeadquarters()) {
      NC_CHECK(world.FindFaction(hq.faction_id) != nullptr);
      NC_CHECK(hq_factions.insert(hq.faction_id).second);
    }
  }

  // Color parsing & metadata lookup.
  NC_CHECK(neon::store::WorldDb::ParseHexColorRgba("#D92626CC") == 0xD92626CCU);
  NC_CHECK(neon::store::WorldDb::ParseHexColorRgba("#00F0FF") == 0x00F0FFFFU);
  const auto* maelstrom = world.FindFaction(1);
  NC_CHECK(maelstrom != nullptr && maelstrom->code == "maelstrom");
  NC_CHECK(maelstrom->color_rgba_packed != 0U);

  // Every control center resolves via O(1) RAM cell grid and metadata maps.
  for (const auto& cc : world.ControlCenters()) {
    const int32_t resolved = world.LookupSubTerritoryAt(cc.x, cc.y);
    NC_CHECK(resolved == cc.sub_territory_id);
    const auto* st = world.FindSubTerritory(cc.sub_territory_id);
    NC_CHECK(st != nullptr);
    NC_CHECK(world.FindDistrict(st->district_id) != nullptr);
    NC_CHECK(world.FindControlCenterBySubTerritory(cc.sub_territory_id) != nullptr);
  }

  // Verified live PLStandalone Coastview position (-1750.6, -1835.5) resolves cleanly.
  const int32_t coastview_st = world.FindNearestSubTerritory(-1750.597, -1835.524);
  NC_CHECK(coastview_st > 0);
  const auto* coastview_def = world.FindSubTerritory(coastview_st);
  NC_CHECK(coastview_def != nullptr);

  // R-Tree spatial prefilter + 3D check finds real spawns near most active control centers.
  size_t centers_with_spawns = 0;
  for (const auto& cc : world.ControlCenters()) {
    const auto nearby = world.QuerySpawnPointsNear(cc.x, cc.y, cc.z, 250.0);
    if (!nearby.empty()) {
      ++centers_with_spawns;
    }
  }
  NC_CHECK(centers_with_spawns * 2 >= world.ControlCenters().size());

  // Road graph boot-load, chunk R-Tree prefilter, snapping, and cross-district A* routing.
  NC_CHECK(world.RoadChunks().size() >= 1000);
  NC_CHECK(world.RoadNodes().size() >= 25000);
  NC_CHECK(world.RoadEdgeCount() >= 40000);

  // Every faction HQ snaps cleanly onto the strongly connected road graph.
  for (const auto& hq : world.FactionHeadquarters()) {
    const int32_t nid = world.FindNearestRoadNode(hq.x, hq.y, hq.z, 500.0);
    NC_CHECK(nid > 0);
    const auto* rn = world.FindRoadNode(nid);
    NC_CHECK(rn != nullptr);
    NC_CHECK(world.FindRoadChunk(rn->chunk_id) != nullptr);
  }

  // SQLite road_chunk_rtree query returns chunks near Corpo Plaza.
  NC_CHECK(!world.QueryRoadChunksNear(-1609.0, 356.0, 400.0).empty());

  // Cross-district bidirectional A* routes: Watson <-> Santo Domingo, Heywood <-> Dogtown,
  // and City Center <-> Badlands must all resolve with realistic driving distances.
  {
    const auto watson_to_sd = world.FindRoadPathBetween(
        -1381.8, 1271.7, 25.0,    // Watson (H10 area)
        -150.0, -1950.0, 10.0);   // Santo Domingo (Rancho Coronado)
    NC_CHECK(watson_to_sd.found);
    NC_CHECK(watson_to_sd.waypoints.size() >= 10);
    NC_CHECK(watson_to_sd.total_length_m > 3000.0 && watson_to_sd.total_length_m < 12000.0);
    NC_CHECK(watson_to_sd.estimated_seconds > 150.0);

    const auto sd_to_watson = world.FindRoadPathBetween(
        -150.0, -1950.0, 10.0,
        -1381.8, 1271.7, 25.0);
    NC_CHECK(sd_to_watson.found);
    NC_CHECK(sd_to_watson.total_length_m > 3000.0);

    // Heywood <-> Dogtown interior (verifies Dogtown checkpoint connectivity!)
    const auto heywood_to_dt = world.FindRoadPathBetween(
        -1520.0, -976.0, 25.0,    // Heywood (The Glen)
        -2134.3, -2692.7, 78.6);  // Dogtown (Luxor Heights)
    NC_CHECK(heywood_to_dt.found);
    NC_CHECK(heywood_to_dt.total_length_m > 1500.0 && heywood_to_dt.total_length_m < 10000.0);

    const auto dt_to_heywood = world.FindRoadPathBetween(
        -2134.3, -2692.7, 78.6,
        -1520.0, -976.0, 25.0);
    NC_CHECK(dt_to_heywood.found);
    NC_CHECK(dt_to_heywood.total_length_m > 1500.0);

    // City Center <-> Badlands
    const auto cc_to_badlands = world.FindRoadPathBetween(
        -1609.0, 356.5, 25.0,     // City Center
        3003.6, -2394.3, 118.5);  // Badlands (Wraith Compound area)
    NC_CHECK(cc_to_badlands.found);
    NC_CHECK(cc_to_badlands.total_length_m > 5000.0);
  }
}

void TestCausalSimAndSaveBranching(const std::string& world_db_path) {
  neon::store::WorldDb world;
  std::string err;
  NC_CHECK(world.Open(world_db_path, true, err));
  neon::sim::SimEngine engine(world.BuildTerritoryDefs());

  const auto tmp_db = (std::filesystem::temp_directory_path() / "neon_test_pt.db").string();
  std::filesystem::remove(tmp_db);
  std::filesystem::remove(tmp_db + "-wal");
  std::filesystem::remove(tmp_db + "-shm");

  const int32_t home_st = world.ControlCenters()[0].sub_territory_id;
  const int32_t rival_st = world.ControlCenters()[1].sub_territory_id;
  const int32_t rival_cc = world.ControlCenters()[1].control_center_id;
  const int32_t rival_orig_owner = world.FindSubTerritory(rival_st)->initial_owner_faction_id;

  // 1. Fresh playthrough creation -> revision 0.
  neon::sim::SimState state;
  neon::store::PlaythroughDb pt;
  auto begin = pt.SessionBegin(tmp_db, world, 0, 0x11223344U, 0x55667788U, 0, 1000, state);
  NC_CHECK(begin.status == neon::store::SessionStatus::Created);
  NC_CHECK(begin.durable_revision == 0);
  NC_CHECK(state.territories.size() == world.ControlCenters().size());
  NC_CHECK(neon::sim::SimEngine::ResolvePauseMenuAction(state, false) ==
           neon::sim::PauseMenuAction::ActivateAscendancy);
  NC_CHECK(neon::sim::SimEngine::ResolvePauseMenuAction(state, true) ==
           neon::sim::PauseMenuAction::FoundGangHere);

  // 2. Found gang at home sub-territory -> commit rev 1.
  auto r_found = engine.FoundGang(state, "Neon Vipers", home_st, 1100);
  NC_CHECK(r_found.ok);
  const int32_t rev_after_found = pt.CommitState(state, r_found.emitted, false, err);
  NC_CHECK(rev_after_found == 1);
  const int64_t income_one = engine.ComputeCycleIncome(state, neon::sim::kPlayerFactionIdBase);
  NC_CHECK(income_one > 0);
  NC_CHECK(neon::sim::SimEngine::ResolvePauseMenuAction(state, true) ==
           neon::sim::PauseMenuAction::LaunchRivalRaid);

  // Nearest rival from home control center must not return home_st.
  const auto* home_cc = world.FindControlCenterBySubTerritory(home_st);
  NC_CHECK(home_cc != nullptr);
  const int32_t nearest_rival = world.FindNearestRivalSubTerritory(
      home_cc->x, home_cc->y, neon::sim::kPlayerFactionIdBase, state.territories);
  NC_CHECK(nearest_rival > 0 && nearest_rival != home_st);

  // 3. Offer combat mission (3 kills required) against rival sub-territory -> commit rev 2.
  auto r_offer = engine.OfferCombatMission(state, rival_st, rival_cc, 2500, 1200, 3);
  NC_CHECK(r_offer.ok);
  NC_CHECK(state.missions.size() == 1);
  NC_CHECK(neon::sim::SimEngine::ResolvePauseMenuAction(state, true) ==
           neon::sim::PauseMenuAction::ShowStatus);
  const int32_t mission_id = state.missions[0].mission_id;
  const int32_t rev_after_offer = pt.CommitState(state, r_offer.emitted, false, err);
  NC_CHECK(rev_after_offer == 2);

  // 4. Record kills 1 and 2 (must not flip yet); verify kill progress round-trips across snapshot!
  auto r_k1 = engine.RecordMissionKill(state, mission_id, 1300);
  NC_CHECK(r_k1.ok && r_k1.payout_eddies == 0);
  auto r_k2 = engine.RecordMissionKill(state, mission_id, 1400);
  NC_CHECK(r_k2.ok && r_k2.payout_eddies == 0);
  NC_CHECK(FindTerr(state, rival_st)->owner_faction_id == rival_orig_owner);
  {
    const auto snap = neon::store::PlaythroughDb::EncodeFullSnapshot(state);
    neon::sim::SimState decoded;
    NC_CHECK(neon::store::PlaythroughDb::DecodeFullSnapshot(snap, decoded));
    NC_CHECK(decoded.missions.size() == 1);
    NC_CHECK(decoded.missions[0].kills_done == 2 && decoded.missions[0].kills_required == 3);
  }

  // 5. Final kill (3/3) -> automatic completion, immediate flip, reward -> commit rev 3.
  auto r_k3 = engine.RecordMissionKill(state, mission_id, 1500);
  NC_CHECK(r_k3.ok);
  NC_CHECK(r_k3.payout_eddies == 2500);
  NC_CHECK(FindTerr(state, rival_st)->owner_faction_id == neon::sim::kPlayerFactionIdBase);
  NC_CHECK(neon::sim::SimEngine::FindActiveCombatMissionConst(state) == nullptr);
  const int64_t income_two = engine.ComputeCycleIncome(state, neon::sim::kPlayerFactionIdBase);
  NC_CHECK(income_two > income_one);
  const int32_t rev_after_flip = pt.CommitState(state, r_k3.emitted, false, err);
  NC_CHECK(rev_after_flip == 3);

  // 6. Advance 2 in-game days -> settles 2 cycles of income -> commit rev 4.
  auto r_time = engine.AdvanceTime(state, 1000 + 2 * neon::sim::kDefaultCycleSeconds);
  NC_CHECK(r_time.ok);
  NC_CHECK(r_time.payout_eddies == 2 * income_two);
  const int32_t rev_after_time = pt.CommitState(state, r_time.emitted, false, err);
  NC_CHECK(rev_after_time == 4);
  NC_CHECK(pt.Close(true));

  // 7. Save-branching / reload test: reload older save at rev 1 (before mission/flip).
  neon::sim::SimState restored_r1;
  auto r_load1 = pt.SessionBegin(
      tmp_db, world, neon::store::PlaythroughDb::kSchemaVersion,
      0x11223344U, 0x55667788U, rev_after_found, 1100, restored_r1);
  NC_CHECK(r_load1.status == neon::store::SessionStatus::Restored);
  NC_CHECK(r_load1.durable_revision == 5); // forked at max(4, 1) + 1
  NC_CHECK(restored_r1.orgs.size() == 1);
  NC_CHECK(restored_r1.orgs[0].display_name == "Neon Vipers");
  NC_CHECK(restored_r1.missions.empty());
  NC_CHECK(FindTerr(restored_r1, rival_st)->owner_faction_id == rival_orig_owner);

  // Advance on the forked branch -> rev 6 (must not clobber old rev 3).
  auto r_fork_time = engine.AdvanceTime(restored_r1, 1000 + neon::sim::kDefaultCycleSeconds);
  NC_CHECK(r_fork_time.ok);
  NC_CHECK(r_fork_time.payout_eddies == income_one);
  NC_CHECK(pt.CommitState(restored_r1, r_fork_time.emitted, false, err) == 6);
  NC_CHECK(pt.Close(true));

  // Reload the other manual save at rev 3 (post-flip branch) -> still intact!
  neon::sim::SimState restored_r3;
  auto r_load3 = pt.SessionBegin(
      tmp_db, world, neon::store::PlaythroughDb::kSchemaVersion,
      0x11223344U, 0x55667788U, rev_after_flip, 1500, restored_r3);
  NC_CHECK(r_load3.status == neon::store::SessionStatus::Restored);
  NC_CHECK(r_load3.durable_revision == 7);
  NC_CHECK(FindTerr(restored_r3, rival_st)->owner_faction_id == neon::sim::kPlayerFactionIdBase);
  NC_CHECK(restored_r3.orgs[0].treasury_eddies == 2500);
  NC_CHECK(pt.Close(true));

  // Reload an older manual save at rev 0 (pre-gang founding) -> must restore rev 0, NOT max_rev!
  neon::sim::SimState restored_r0;
  auto r_load0 = pt.SessionBegin(
      tmp_db, world, neon::store::PlaythroughDb::kSchemaVersion,
      0x11223344U, 0x55667788U, 0, 1000, restored_r0);
  NC_CHECK(r_load0.status == neon::store::SessionStatus::Restored);
  NC_CHECK(r_load0.durable_revision == 8);
  NC_CHECK(restored_r0.orgs.empty());
  NC_CHECK(restored_r0.missions.empty());
  NC_CHECK(FindTerr(restored_r0, rival_st)->owner_faction_id == rival_orig_owner);

  // 8. Prune checkpoints aggressively: pinned revisions (1, 3) must remain restorable.
  NC_CHECK(pt.PruneCheckpoints(1024, err));
  NC_CHECK(pt.Close(true));
  neon::sim::SimState restored_pinned;
  auto r_pin = pt.SessionBegin(
      tmp_db, world, neon::store::PlaythroughDb::kSchemaVersion,
      0x11223344U, 0x55667788U, rev_after_found, 1100, restored_pinned);
  NC_CHECK(r_pin.status == neon::store::SessionStatus::Restored);
  NC_CHECK(FindTerr(restored_pinned, rival_st)->owner_faction_id == rival_orig_owner);
  NC_CHECK(pt.Close(true));

  // 9. Future schema guard: downgrade refuses mutation cleanly.
  neon::sim::SimState future_state;
  auto r_future = pt.SessionBegin(tmp_db, world, 99, 0x11223344U, 0x55667788U, 1, 1100, future_state);
  NC_CHECK(r_future.status == neon::store::SessionStatus::ReadOnlyFutureSchema);
  NC_CHECK(pt.IsReadOnlyFallback());

  // 10. Snapshot codec rejects corrupted CRC32.
  auto blob = neon::store::PlaythroughDb::EncodeFullSnapshot(restored_r3);
  NC_CHECK(!blob.empty());
  blob[blob.size() / 2] ^= 0xFFU;
  neon::sim::SimState bad;
  NC_CHECK(!neon::store::PlaythroughDb::DecodeFullSnapshot(blob, bad));

  // 11. Formatting helpers produce non-empty UI text.
  const std::string tip = neon::sim::SimEngine::FormatTerritoryTooltipDesc(
      "Pacifica", "Barghest", 450, false, true, 2, 3);
  NC_CHECK(tip.find("ACTIVE RAID: 2/3") != std::string::npos);
  const std::string status = engine.FormatStatusSummary(restored_r3, "");
  NC_CHECK(status.find("Neon Vipers") != std::string::npos);

  std::filesystem::remove(tmp_db);
  std::filesystem::remove(tmp_db + "-wal");
  std::filesystem::remove(tmp_db + "-shm");
}

} // namespace

int main(int argc, char** argv) {
  if (argc < 2) {
    std::cerr << "Usage: neon_tests <path/to/world.db>\n";
    return 2;
  }
  const std::string world_db_path = argv[1];
  TestEraAndSanitizerPolicy();
  TestWorldDbAndSpatialLookups(world_db_path);
  TestCausalSimAndSaveBranching(world_db_path);

  if (g_failures == 0) {
    std::cout << "All native tests passed.\n";
    return 0;
  }
  std::cerr << g_failures << " test check(s) failed.\n";
  return 1;
}
