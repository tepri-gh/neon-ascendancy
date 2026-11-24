#include <cstdio>
#include <cstdlib>
#include <filesystem>
#include <iostream>
#include <string>
#include <vector>

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

void TestWorldDbAndSpatialLookups(const std::string& world_db_path) {
  neon::store::WorldDb world;
  std::string err;
  NC_CHECK(world.Open(world_db_path, true, err));
  NC_CHECK(!world.ContentHash().empty());
  NC_CHECK(world.SubTerritories().size() >= 40);
  NC_CHECK(world.ControlCenters().size() == world.SubTerritories().size());

  // Every control center must resolve to a valid sub-territory via O(1) RAM cell grid.
  for (const auto& cc : world.ControlCenters()) {
    const int32_t resolved = world.LookupSubTerritoryAt(cc.x, cc.y);
    NC_CHECK(resolved > 0);
  }

  // R-Tree spatial prefilter + 3D check finds real spawns near at least one control center.
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

  // 2. Found gang at home sub-territory -> commit rev 1.
  auto r_found = engine.FoundGang(state, "Neon Vipers", home_st, 1100);
  NC_CHECK(r_found.ok);
  const int32_t rev_after_found = pt.CommitState(state, r_found.emitted, false, err);
  NC_CHECK(rev_after_found == 1);
  const int64_t income_one = engine.ComputeCycleIncome(state, neon::sim::kPlayerFactionIdBase);
  NC_CHECK(income_one > 0);

  // 3. Offer combat mission against rival sub-territory -> commit rev 2.
  auto r_offer = engine.OfferCombatMission(state, rival_st, rival_cc, 2500, 1200);
  NC_CHECK(r_offer.ok);
  NC_CHECK(state.missions.size() == 1);
  const int32_t mission_id = state.missions[0].mission_id;
  const int32_t rev_after_offer = pt.CommitState(state, r_offer.emitted, false, err);
  NC_CHECK(rev_after_offer == 2);

  // 4. Complete mission -> immediate flip + reward -> commit rev 3.
  auto r_done = engine.CompleteMission(state, mission_id, 1500);
  NC_CHECK(r_done.ok);
  NC_CHECK(r_done.payout_eddies == 2500);
  NC_CHECK(FindTerr(state, rival_st)->owner_faction_id == neon::sim::kPlayerFactionIdBase);
  const int64_t income_two = engine.ComputeCycleIncome(state, neon::sim::kPlayerFactionIdBase);
  NC_CHECK(income_two > income_one);
  const int32_t rev_after_flip = pt.CommitState(state, r_done.emitted, false, err);
  NC_CHECK(rev_after_flip == 3);

  // 5. Advance 2 in-game days -> settles 2 cycles of income -> commit rev 4.
  auto r_time = engine.AdvanceTime(state, 1000 + 2 * neon::sim::kDefaultCycleSeconds);
  NC_CHECK(r_time.ok);
  NC_CHECK(r_time.payout_eddies == 2 * income_two);
  const int32_t rev_after_time = pt.CommitState(state, r_time.emitted, false, err);
  NC_CHECK(rev_after_time == 4);
  NC_CHECK(pt.Close(true));

  // 6. Save-branching / reload test: reload older save at rev 1 (before mission/flip).
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

  // 7. Prune checkpoints aggressively: pinned revisions (1, 3) must remain restorable.
  NC_CHECK(pt.PruneCheckpoints(1024, err));
  NC_CHECK(pt.Close(true));
  neon::sim::SimState restored_pinned;
  auto r_pin = pt.SessionBegin(
      tmp_db, world, neon::store::PlaythroughDb::kSchemaVersion,
      0x11223344U, 0x55667788U, rev_after_found, 1100, restored_pinned);
  NC_CHECK(r_pin.status == neon::store::SessionStatus::Restored);
  NC_CHECK(FindTerr(restored_pinned, rival_st)->owner_faction_id == rival_orig_owner);
  NC_CHECK(pt.Close(true));

  // 8. Future schema guard: downgrade refuses mutation cleanly.
  neon::sim::SimState future_state;
  auto r_future = pt.SessionBegin(tmp_db, world, 99, 0x11223344U, 0x55667788U, 1, 1100, future_state);
  NC_CHECK(r_future.status == neon::store::SessionStatus::ReadOnlyFutureSchema);
  NC_CHECK(pt.IsReadOnlyFallback());

  // 9. Snapshot codec rejects corrupted CRC32.
  auto blob = neon::store::PlaythroughDb::EncodeFullSnapshot(restored_r3);
  NC_CHECK(!blob.empty());
  blob[blob.size() / 2] ^= 0xFFU;
  neon::sim::SimState bad;
  NC_CHECK(!neon::store::PlaythroughDb::DecodeFullSnapshot(blob, bad));

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
  TestWorldDbAndSpatialLookups(world_db_path);
  TestCausalSimAndSaveBranching(world_db_path);

  if (g_failures == 0) {
    std::cout << "All native tests passed.\n";
    return 0;
  }
  std::cerr << g_failures << " test check(s) failed.\n";
  return 1;
}
