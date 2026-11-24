#include <cstdio>
#include <cstdlib>
#include <filesystem>
#include <iostream>
#include <string>
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
  NC_CHECK(world.Districts().size() == 8);
  NC_CHECK(world.SubTerritories().size() >= 40);
  NC_CHECK(world.ControlCenters().size() == world.SubTerritories().size());

  // Color parsing & metadata lookup.
  NC_CHECK(neon::store::WorldDb::ParseHexColorRgba("#D92626CC") == 0xD92626CCU);
  NC_CHECK(neon::store::WorldDb::ParseHexColorRgba("#00F0FF") == 0x00F0FFFFU);
  const auto* maelstrom = world.FindFaction(1);
  NC_CHECK(maelstrom != nullptr && maelstrom->code == "maelstrom");
  NC_CHECK(maelstrom->color_rgba_packed != 0U);

  // Every control center resolves via O(1) RAM cell grid and metadata maps.
  for (const auto& cc : world.ControlCenters()) {
    const int32_t resolved = world.LookupSubTerritoryAt(cc.x, cc.y);
    NC_CHECK(resolved > 0);
    const auto* st = world.FindSubTerritory(cc.sub_territory_id);
    NC_CHECK(st != nullptr);
    NC_CHECK(world.FindDistrict(st->district_id) != nullptr);
    NC_CHECK(world.FindControlCenterBySubTerritory(cc.sub_territory_id) != nullptr);
  }

  // Verified live PLStandalone Coastview position (-1750.6, -1835.5) resolves cleanly.
  const int32_t coastview_st = world.LookupSubTerritoryAt(-1750.597, -1835.524);
  NC_CHECK(coastview_st > 0);
  const auto* coastview_def = world.FindSubTerritory(coastview_st);
  NC_CHECK(coastview_def != nullptr);

  // R-Tree spatial prefilter + 3D check finds real spawns near at least 20 control centers.
  size_t centers_with_spawns = 0;
  for (const auto& cc : world.ControlCenters()) {
    const auto nearby = world.QuerySpawnPointsNear(cc.x, cc.y, cc.z, 250.0);
    if (!nearby.empty()) {
      ++centers_with_spawns;
    }
  }
  NC_CHECK(centers_with_spawns >= 20);
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

  const int32_t home_st = world.SubTerritories()[0].sub_territory_id;
  const int32_t rival_st = world.SubTerritories()[1].sub_territory_id;
  const int32_t rival_cc = world.ControlCenters()[1].control_center_id;
  const int32_t rival_orig_owner = world.SubTerritories()[1].initial_owner_faction_id;

  // 1. Fresh playthrough creation -> revision 0.
  neon::sim::SimState state;
  neon::store::PlaythroughDb pt;
  auto begin = pt.SessionBegin(tmp_db, world, 0, 0x11223344U, 0x55667788U, 0, 1000, state);
  NC_CHECK(begin.status == neon::store::SessionStatus::Created);
  NC_CHECK(begin.durable_revision == 0);
  NC_CHECK(state.territories.size() == world.SubTerritories().size());
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
