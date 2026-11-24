#include <Windows.h>

#include <array>
#include <cmath>
#include <cstdio>
#include <deque>
#include <memory>
#include <mutex>
#include <shared_mutex>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include <RED4ext/CNamePool.hpp>
#include <RED4ext/RED4ext.hpp>
#include <RED4ext/ResourceDepot.hpp>
#include <RED4ext/ResourceLoader.hpp>
#include <RED4ext/TweakDB.hpp>
#include <RedLib.hpp>

#include "era.hpp"
#include "sim.hpp"
#include "store.hpp"

namespace {

constexpr double kCombatMissionRadiusXY = 160.0;
constexpr double kCombatMissionRadiusZ = 60.0;
constexpr size_t kMaxQueuedHudNotices = 16;

// Ascendancy clean-slate .gamedef redirect. On EP1 installs, native
// StartNewGame loads ep1\quest\ep1.gamedef (when !IsExpansionStandalone); on
// non-EP1 installs it loads base\quest\cyberpunk2077.gamedef. Redirecting both
// covers every install while keeping ep1_standalone.gamedef and vanilla New
// Game completely untouched.
constexpr const char* kVanillaBaseGamedefPath = "base\\quest\\cyberpunk2077.gamedef";
constexpr const char* kVanillaEp1GamedefPath = "ep1\\quest\\ep1.gamedef";
constexpr const char* kAscendancyGamedefPath = "mod\\neon_ascendancy\\ascendancy.gamedef";
constexpr const char* kAscendancyQuestPath = "mod\\neon_ascendancy\\ascendancy.quest";
constexpr const char* kAscendancyQuestPhasePath = "mod\\neon_ascendancy\\ascendancy.questphase";

// H10 apartment player spawn marker (worldStaticMarkerNode in
// always_loaded_1.streamingsector at (-1383.64, 1271.17, 123.06), literal tag
// "mq000_spwn_player" matching vanilla mq000.gamedef and
// data/clean-slate/clean_slate_spec.json). Native StartNewGame overrides
// gamedef.spawnPointTags with LifePath_Record.NewGameSpawnTag(), so
// NcArmAscendancyStart temporarily swaps the three unique
// LifePaths.*.newGameSpawnTag flats in-place and NcDisarmAscendancyStart
// restores their exact original CNames so vanilla New Game is untouched.
constexpr const char* kAscendancySpawnTag = "mq000_spwn_player";
constexpr std::array<const char*, 3> kLifePathSpawnTagFlats = {
    "LifePaths.Nomad.newGameSpawnTag",
    "LifePaths.Corporate.newGameSpawnTag",
    "LifePaths.StreetKid.newGameSpawnTag",
};

RED4ext::v1::PluginHandle g_plugin_handle = nullptr;
const RED4ext::v1::Sdk* g_sdk = nullptr;
HMODULE g_module_handle = nullptr;

struct CoreRuntime {
  std::mutex mu;
  std::string plugin_dir_utf8;
  neon::store::WorldDb world;
  neon::store::PlaythroughDb playthrough;
  std::unique_ptr<neon::sim::SimEngine> engine;
  neon::sim::SimState state;
  std::unordered_set<uint64_t> counted_kill_entities;
  std::deque<std::string> hud_notices;
  std::vector<neon::sim::SafeSanctuaryZone> safe_sanctuaries;
  std::unordered_map<uint64_t, int32_t> control_center_pins;
  std::array<RED4ext::CName, kLifePathSpawnTagFlats.size()> saved_lifepath_spawn_tags{};
  std::array<bool, kLifePathSpawnTagFlats.size()> saved_lifepath_spawn_tag_valid{};
  uint32_t playthrough_id_hi = 0;
  uint32_t playthrough_id_lo = 0;
  bool world_loaded = false;
  bool session_active = false;
  bool sanitizer_active = false;
  bool ascendancy_start_pending = false;
  bool lifepath_spawn_tags_overridden = false;
};

CoreRuntime g_rt;

void LogInfo(const char* msg) {
  if (g_sdk != nullptr && g_sdk->logger != nullptr && g_plugin_handle != nullptr) {
    g_sdk->logger->Info(g_plugin_handle, msg);
  }
}

void LogWarn(const char* msg) {
  if (g_sdk != nullptr && g_sdk->logger != nullptr && g_plugin_handle != nullptr) {
    g_sdk->logger->Warn(g_plugin_handle, msg);
  }
}

void LogError(const char* msg) {
  if (g_sdk != nullptr && g_sdk->logger != nullptr && g_plugin_handle != nullptr) {
    g_sdk->logger->Error(g_plugin_handle, msg);
  }
}

void PushHudNoticeLocked(std::string msg) {
  if (msg.empty()) {
    return;
  }
  if (g_rt.hud_notices.size() >= kMaxQueuedHudNotices) {
    g_rt.hud_notices.pop_front();
  }
  g_rt.hud_notices.push_back(std::move(msg));
}

std::string WideToUtf8(const std::wstring& ws) {
  if (ws.empty()) return {};
  const int needed = WideCharToMultiByte(
      CP_UTF8, 0, ws.data(), static_cast<int>(ws.size()), nullptr, 0, nullptr, nullptr);
  if (needed <= 0) return {};
  std::string out(static_cast<size_t>(needed), '\0');
  WideCharToMultiByte(
      CP_UTF8, 0, ws.data(), static_cast<int>(ws.size()), out.data(), needed, nullptr, nullptr);
  return out;
}

std::wstring Utf8ToWide(const std::string& s) {
  if (s.empty()) return {};
  const int needed = MultiByteToWideChar(
      CP_UTF8, 0, s.data(), static_cast<int>(s.size()), nullptr, 0);
  if (needed <= 0) return {};
  std::wstring out(static_cast<size_t>(needed), L'\0');
  MultiByteToWideChar(
      CP_UTF8, 0, s.data(), static_cast<int>(s.size()), out.data(), needed);
  return out;
}

std::string ResolvePluginDirUtf8() {
  wchar_t buf[MAX_PATH] = {};
  const DWORD len = GetModuleFileNameW(g_module_handle, buf, MAX_PATH);
  if (len == 0 || len >= MAX_PATH) {
    return ".";
  }
  std::wstring path(buf, len);
  const size_t slash = path.find_last_of(L"\\/");
  if (slash != std::wstring::npos) {
    path.resize(slash);
  }
  return WideToUtf8(path);
}

void EnsureDirExists(const std::string& dir_utf8) {
  const std::wstring wdir = Utf8ToWide(dir_utf8);
  if (!wdir.empty()) {
    CreateDirectoryW(wdir.c_str(), nullptr);
  }
}

std::string FormatPlaythroughDbPath(
    const std::string& plugin_dir, uint32_t id_hi, uint32_t id_lo) {
  const std::string dir = plugin_dir + "\\playthroughs";
  EnsureDirExists(dir);
  char name[64] = {};
  std::snprintf(name, sizeof(name), "\\pt_%08x%08x.db", id_hi, id_lo);
  return dir + name;
}

bool EnsureWorldLoadedLocked() {
  if (g_rt.world_loaded) {
    return true;
  }
  const std::string world_path = g_rt.plugin_dir_utf8 + "\\world.db";
  std::string err;
  if (!g_rt.world.Open(world_path, true, err)) {
    LogWarn(("world.db immutable open failed (" + err + "); retrying standard read-only").c_str());
    err.clear();
    if (!g_rt.world.Open(world_path, false, err)) {
      LogError(("Failed to open world.db at " + world_path + ": " + err).c_str());
      return false;
    }
  }
  g_rt.engine = std::make_unique<neon::sim::SimEngine>(g_rt.world.BuildTerritoryDefs());
  g_rt.world_loaded = true;
  LogInfo(("Loaded world.db hash=" + g_rt.world.ContentHash().substr(0, 12)).c_str());
  return true;
}

std::string ResolveFactionNameLocked(int32_t faction_id) {
  if (faction_id >= neon::sim::kPlayerFactionIdBase) {
    const auto* org = neon::sim::SimEngine::FindPlayerOrgConst(g_rt.state);
    if (org != nullptr && org->faction_id == faction_id) {
      return org->display_name;
    }
    return "Player Gang";
  }
  const auto* fac = g_rt.world.FindFaction(faction_id);
  return fac != nullptr ? fac->display_name : "Unclaimed";
}

uint32_t ResolveFactionColorLocked(int32_t faction_id) {
  if (faction_id >= neon::sim::kPlayerFactionIdBase) {
    return neon::sim::kPlayerOrgColorRgba;
  }
  const auto* fac = g_rt.world.FindFaction(faction_id);
  return fac != nullptr ? fac->color_rgba_packed : 0xAAAAAAFFU;
}

int32_t ResolveOwnerFactionIdLocked(int32_t sub_territory_id) {
  if (g_rt.session_active) {
    const auto* tr = neon::sim::SimEngine::FindTerritoryConst(g_rt.state, sub_territory_id);
    if (tr != nullptr) {
      return tr->owner_faction_id;
    }
  }
  const auto* st = g_rt.world.FindSubTerritory(sub_territory_id);
  return st != nullptr ? st->initial_owner_faction_id : 0;
}

// --- Native functions exposed to redscript 1.x via RedLib -------------------

Red::CString NcCoreVersion() {
  return Red::CString("0.0.0-dev");
}

void NcLogInfo(Red::CString msg) {
  LogInfo(msg.c_str());
}

void NcSetSanitizerActive(bool active) {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  g_rt.sanitizer_active = active;
}

bool NcIsSanitizerActive() {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  return g_rt.sanitizer_active;
}

void NcSetAscendancyStartPending(bool pending) {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  g_rt.ascendancy_start_pending = pending;
}

bool NcIsAscendancyStartPending() {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  return g_rt.ascendancy_start_pending;
}

// In-place flat swap for LifePaths.*.newGameSpawnTag. Safe because the three
// vanilla tag CNames (#q000_nomad_wp_garage_start,
// #q000_corpo_spwn_player_toilet_female, #q000_kid_spawn_start) are unique
// across the entire TweakDB, so their FlatValue slots in flatDataBuffer are
// never pooled with any other record. LifePath_Record::NewGameSpawnTag() reads
// *(CName*)(staticFlatDataBuffer + offset) directly via GetValueOffset_CName.
// NOTE: Never call TweakDB::GetFlatValue() while holding tdb->mutex00 because
// GetFlatValue() acquires a shared_lock on mutex00 itself.
int OverrideLifePathSpawnTagsLocked(const RED4ext::CName target_tag) {
  RED4ext::TweakDB* tdb = RED4ext::TweakDB::Get();
  if (tdb == nullptr) {
    LogWarn("NcArmAscendancyStart: TweakDB::Get() unavailable");
    return 0;
  }

  int swapped = 0;
  std::lock_guard<RED4ext::SharedSpinLock> tdb_guard(tdb->mutex00);
  const uintptr_t buf =
      tdb->flatDataBuffer != 0 ? tdb->flatDataBuffer : tdb->staticFlatDataBuffer;
  if (buf == 0) {
    LogWarn("NcArmAscendancyStart: TweakDB flatDataBuffer unavailable");
    return 0;
  }

  for (size_t i = 0; i < kLifePathSpawnTagFlats.size(); ++i) {
    const RED4ext::TweakDBID flat_id(kLifePathSpawnTagFlats[i]);
    const auto it = tdb->flats.Find(flat_id);
    if (it == tdb->flats.end()) {
      continue;
    }
    auto* fv = reinterpret_cast<RED4ext::TweakDB::FlatValue*>(buf + it->ToTDBOffset());
    if (fv == nullptr) {
      continue;
    }
    RED4ext::TweakDBID value_ref;
    if (!fv->GetValueOffset_CName(&value_ref) || !value_ref.HasTDBOffset()) {
      continue;
    }
    auto* cname_ptr = reinterpret_cast<RED4ext::CName*>(buf + value_ref.ToTDBOffset());
    if (!g_rt.saved_lifepath_spawn_tag_valid[i]) {
      g_rt.saved_lifepath_spawn_tags[i] = *cname_ptr;
      g_rt.saved_lifepath_spawn_tag_valid[i] = true;
    }
    *cname_ptr = target_tag;
    ++swapped;
  }

  if (swapped > 0) {
    g_rt.lifepath_spawn_tags_overridden = true;
  }
  return swapped;
}

int RestoreLifePathSpawnTagsLocked() {
  if (!g_rt.lifepath_spawn_tags_overridden) {
    return 0;
  }
  RED4ext::TweakDB* tdb = RED4ext::TweakDB::Get();
  if (tdb == nullptr) {
    return 0;
  }

  int restored = 0;
  std::lock_guard<RED4ext::SharedSpinLock> tdb_guard(tdb->mutex00);
  const uintptr_t buf =
      tdb->flatDataBuffer != 0 ? tdb->flatDataBuffer : tdb->staticFlatDataBuffer;
  if (buf == 0) {
    return 0;
  }

  for (size_t i = 0; i < kLifePathSpawnTagFlats.size(); ++i) {
    if (!g_rt.saved_lifepath_spawn_tag_valid[i]) {
      continue;
    }
    const RED4ext::TweakDBID flat_id(kLifePathSpawnTagFlats[i]);
    const auto it = tdb->flats.Find(flat_id);
    if (it == tdb->flats.end()) {
      continue;
    }
    auto* fv = reinterpret_cast<RED4ext::TweakDB::FlatValue*>(buf + it->ToTDBOffset());
    if (fv == nullptr) {
      continue;
    }
    RED4ext::TweakDBID value_ref;
    if (!fv->GetValueOffset_CName(&value_ref) || !value_ref.HasTDBOffset()) {
      continue;
    }
    auto* cname_ptr = reinterpret_cast<RED4ext::CName*>(buf + value_ref.ToTDBOffset());
    *cname_ptr = g_rt.saved_lifepath_spawn_tags[i];
    g_rt.saved_lifepath_spawn_tag_valid[i] = false;
    g_rt.saved_lifepath_spawn_tags[i] = RED4ext::CName{};
    ++restored;
  }

  g_rt.lifepath_spawn_tags_overridden = false;
  return restored;
}

// Redirect both base\quest\cyberpunk2077.gamedef (non-EP1) and
// ep1\quest\ep1.gamedef (EP1) -> mod\neon_ascendancy\ascendancy.gamedef in
// ResourceBank::resolvedPathMap, and temporarily redirect the three
// LifePaths.*.newGameSpawnTag flats to kAscendancySpawnTag so StartNewGame
// spawns directly into V's H10 apartment with full world streaming.
bool NcArmAscendancyStart() {
  RED4ext::ResourceLoader* loader = RED4ext::ResourceLoader::Get();
  if (loader == nullptr || loader->bank == nullptr) {
    LogWarn("NcArmAscendancyStart: ResourceLoader/ResourceBank unavailable");
    return false;
  }

  const RED4ext::ResourcePath base_src(kVanillaBaseGamedefPath);
  const RED4ext::ResourcePath ep1_src(kVanillaEp1GamedefPath);
  const RED4ext::ResourcePath dst(kAscendancyGamedefPath);

  bool depot_has_gamedef = false;
  bool depot_has_quest = false;
  bool depot_has_phase = false;
  if (RED4ext::ResourceDepot* depot = RED4ext::ResourceDepot::Get(); depot != nullptr) {
    depot_has_gamedef = depot->ResourceExists(dst);
    depot_has_quest = depot->ResourceExists(RED4ext::ResourcePath(kAscendancyQuestPath));
    depot_has_phase = depot->ResourceExists(RED4ext::ResourcePath(kAscendancyQuestPhasePath));
  }

  bool base_token_cached = false;
  bool ep1_token_cached = false;
  {
    std::shared_lock<RED4ext::SharedSpinLock> token_guard(loader->tokenLock);
    base_token_cached = loader->tokens.Contains(base_src);
    ep1_token_cached = loader->tokens.Contains(ep1_src);
  }

  uint32_t size_before = 0;
  uint32_t size_after = 0;
  bool base_existed = false;
  bool ep1_existed = false;
  {
    std::lock_guard<RED4ext::SharedSpinLock> map_guard(loader->bank->resolvedPathMapLock);
    auto& map = loader->bank->resolvedPathMap;
    size_before = map.size;
    base_existed = map.Get(base_src) != nullptr;
    ep1_existed = map.Get(ep1_src) != nullptr;
    map.InsertOrAssign(base_src, dst);
    map.InsertOrAssign(ep1_src, dst);
    size_after = map.size;
  }

  // Register CName before taking g_rt.mu / tdb->mutex00.
  const RED4ext::CName target_tag = RED4ext::CNamePool::Add(kAscendancySpawnTag);
  int swapped_tags = 0;
  {
    std::lock_guard<std::mutex> lock(g_rt.mu);
    swapped_tags = OverrideLifePathSpawnTagsLocked(target_tag);
  }

  char msg[448] = {};
  std::snprintf(
      msg, sizeof(msg),
      "NcArmAscendancyStart: {base,ep1}.gamedef -> %s; depotExists(gd=%d,q=%d,qp=%d); "
      "existed(base=%d,ep1=%d); tokens(base=%d,ep1=%d); map %u -> %u; "
      "lifepathSpawnTags=%d (%s)",
      kAscendancyGamedefPath,
      depot_has_gamedef ? 1 : 0, depot_has_quest ? 1 : 0, depot_has_phase ? 1 : 0,
      base_existed ? 1 : 0, ep1_existed ? 1 : 0,
      base_token_cached ? 1 : 0, ep1_token_cached ? 1 : 0,
      size_before, size_after, swapped_tags, kAscendancySpawnTag);
  LogInfo(msg);
  if (!depot_has_gamedef || !depot_has_quest || !depot_has_phase) {
    LogWarn("NcArmAscendancyStart: one or more mod\\neon_ascendancy\\* resources missing in ResourceDepot");
  }
  if (swapped_tags != static_cast<int>(kLifePathSpawnTagFlats.size())) {
    LogWarn("NcArmAscendancyStart: did not swap all 3 LifePaths.*.newGameSpawnTag flats");
  }
  return true;
}

// Remove Ascendancy gamedef mappings and restore LifePaths.*.newGameSpawnTag
// flats idempotently. Only removes resolvedPathMap entries that currently point
// to mod\neon_ascendancy\ascendancy.gamedef so vanilla cache entries are never
// disturbed when not armed.
bool NcDisarmAscendancyStart() {
  int restored_tags = 0;
  {
    std::lock_guard<std::mutex> lock(g_rt.mu);
    restored_tags = RestoreLifePathSpawnTagsLocked();
  }

  RED4ext::ResourceLoader* loader = RED4ext::ResourceLoader::Get();
  if (loader == nullptr || loader->bank == nullptr) {
    LogWarn("NcDisarmAscendancyStart: ResourceLoader/ResourceBank unavailable");
    return false;
  }

  const RED4ext::ResourcePath base_src(kVanillaBaseGamedefPath);
  const RED4ext::ResourcePath ep1_src(kVanillaEp1GamedefPath);
  const RED4ext::ResourcePath dst(kAscendancyGamedefPath);
  uint32_t size_before = 0;
  uint32_t size_after = 0;
  int removed = 0;
  {
    std::lock_guard<RED4ext::SharedSpinLock> map_guard(loader->bank->resolvedPathMapLock);
    auto& map = loader->bank->resolvedPathMap;
    size_before = map.size;
    if (const RED4ext::ResourcePath* cur = map.Get(base_src); cur != nullptr && *cur == dst) {
      if (map.Remove(base_src)) {
        ++removed;
      }
    }
    if (const RED4ext::ResourcePath* cur = map.Get(ep1_src); cur != nullptr && *cur == dst) {
      if (map.Remove(ep1_src)) {
        ++removed;
      }
    }
    size_after = map.size;
  }

  char msg[192] = {};
  std::snprintf(
      msg, sizeof(msg),
      "NcDisarmAscendancyStart: removed=%d; restoredTags=%d; resolvedPathMap size %u -> %u",
      removed, restored_tags, size_before, size_after);
  LogInfo(msg);
  return true;
}

bool NcIsSuppressedVanillaMappinVariant(int32_t mappin_variant_enum) {
  return neon::sim::IsSuppressedVanillaMappinVariant(mappin_variant_enum);
}

void NcClearControlCenterPins() {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  g_rt.control_center_pins.clear();
}

void NcBindControlCenterPin(uint64_t mappin_id, int32_t sub_territory_id) {
  if (mappin_id == 0U || sub_territory_id <= 0) {
    return;
  }
  std::lock_guard<std::mutex> lock(g_rt.mu);
  g_rt.control_center_pins[mappin_id] = sub_territory_id;
}

int32_t NcLookupControlCenterPin(uint64_t mappin_id) {
  if (mappin_id == 0U) {
    return 0;
  }
  std::lock_guard<std::mutex> lock(g_rt.mu);
  const auto it = g_rt.control_center_pins.find(mappin_id);
  return it != g_rt.control_center_pins.end() ? it->second : 0;
}

int32_t NcGetBoundControlCenterPinCount() {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  return static_cast<int32_t>(g_rt.control_center_pins.size());
}

int32_t NcGetSafeSanctuaryCount() {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  return static_cast<int32_t>(g_rt.safe_sanctuaries.size());
}

Red::CString NcPopHudNotice() {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (g_rt.hud_notices.empty()) {
    return Red::CString("");
  }
  std::string msg = std::move(g_rt.hud_notices.front());
  g_rt.hud_notices.pop_front();
  return Red::CString(msg.c_str());
}

uint32_t NcEvaluateSanitizer(uint32_t fact_bits, bool enabled) {
  const auto facts = neon::sim::UnpackEraFactsMask(fact_bits);
  const auto policy = neon::sim::ComputeSanitizerPolicy(facts, enabled);
  return neon::sim::PackSanitizerPolicyMask(policy);
}

Red::CString NcGetEraName(int32_t era_code) {
  const auto era = static_cast<neon::sim::WorldEra>(era_code);
  return Red::CString(neon::sim::WorldEraName(era));
}

void NcClearSafeSanctuaries() {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  g_rt.safe_sanctuaries.clear();
}

bool NcRegisterSafeSanctuaryPin(int32_t mappin_variant_enum, float x, float y, float z) {
  const auto kind = neon::sim::ClassifySafeSanctuaryVariant(mappin_variant_enum);
  if (kind == neon::sim::SafeSanctuaryKind::None) {
    return false;
  }
  std::lock_guard<std::mutex> lock(g_rt.mu);
  g_rt.safe_sanctuaries.push_back(neon::sim::SafeSanctuaryZone{
      kind,
      static_cast<double>(x),
      static_cast<double>(y),
      static_cast<double>(z),
  });
  return true;
}

bool NcIsAllowedSafeZone(float x, float y, float z) {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  return neon::sim::IsAllowedSafeZone(
      static_cast<double>(x),
      static_cast<double>(y),
      static_cast<double>(z),
      g_rt.safe_sanctuaries);
}

int32_t NcSessionBegin(
    int32_t schema_version,
    uint32_t id_hi,
    uint32_t id_lo,
    int32_t anchor_revision,
    int32_t game_seconds) {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!EnsureWorldLoadedLocked()) {
    return -1;
  }

  uint32_t req_hi = id_hi;
  uint32_t req_lo = id_lo;
  if (req_hi == 0 && req_lo == 0) {
    LARGE_INTEGER qpc{};
    QueryPerformanceCounter(&qpc);
    req_hi = static_cast<uint32_t>((static_cast<uint64_t>(qpc.QuadPart) >> 32U) ^ GetCurrentProcessId());
    req_lo = static_cast<uint32_t>(qpc.QuadPart ^ GetTickCount());
    if (req_hi == 0 && req_lo == 0) {
      req_lo = 1;
    }
  }

  const std::string db_path = FormatPlaythroughDbPath(g_rt.plugin_dir_utf8, req_hi, req_lo);
  const auto res = g_rt.playthrough.SessionBegin(
      db_path, g_rt.world, schema_version, req_hi, req_lo, anchor_revision, game_seconds, g_rt.state);
  if (res.status == neon::store::SessionStatus::Error) {
    LogError(("NcSessionBegin failed: " + res.warning_or_error).c_str());
    g_rt.session_active = false;
    return -1;
  }
  if (res.status == neon::store::SessionStatus::ReadOnlyFutureSchema) {
    LogError(("NcSessionBegin future schema: " + res.warning_or_error).c_str());
    g_rt.session_active = false;
    return -2;
  }
  if (!res.warning_or_error.empty()) {
    LogWarn(("NcSessionBegin warning: " + res.warning_or_error).c_str());
  }

  g_rt.playthrough_id_hi = res.playthrough_id_hi;
  g_rt.playthrough_id_lo = res.playthrough_id_lo;
  g_rt.counted_kill_entities.clear();
  g_rt.hud_notices.clear();
  g_rt.session_active = true;

  char msg[160] = {};
  std::snprintf(
      msg, sizeof(msg),
      "NcSessionBegin succeeded: pt=%08x%08x status=%u anchor_rev=%d -> rev=%d",
      res.playthrough_id_hi, res.playthrough_id_lo,
      static_cast<unsigned>(res.status), anchor_revision, res.durable_revision);
  LogInfo(msg);
  return res.durable_revision;
}

uint32_t NcSessionGetPlaythroughIdHi() {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  return g_rt.playthrough_id_hi;
}

uint32_t NcSessionGetPlaythroughIdLo() {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  return g_rt.playthrough_id_lo;
}

int32_t NcSessionCurrentRevision() {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  return g_rt.session_active ? g_rt.playthrough.DurableRevision() : 0;
}

bool NcSessionEnd() {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  g_rt.session_active = false;
  g_rt.sanitizer_active = false;
  g_rt.counted_kill_entities.clear();
  g_rt.hud_notices.clear();
  g_rt.safe_sanctuaries.clear();
  g_rt.control_center_pins.clear();
  return g_rt.playthrough.Close(true);
}

// --- World & Map O(1) RAM Queries -------------------------------------------

int32_t NcGetControlCenterCount() {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!EnsureWorldLoadedLocked()) {
    return 0;
  }
  return static_cast<int32_t>(g_rt.world.ControlCenters().size());
}

int32_t NcGetControlCenterSubTerritoryId(int32_t index) {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!EnsureWorldLoadedLocked() || index < 0 ||
      static_cast<size_t>(index) >= g_rt.world.ControlCenters().size()) {
    return 0;
  }
  return g_rt.world.ControlCenters()[static_cast<size_t>(index)].sub_territory_id;
}

int32_t NcGetControlCenterId(int32_t index) {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!EnsureWorldLoadedLocked() || index < 0 ||
      static_cast<size_t>(index) >= g_rt.world.ControlCenters().size()) {
    return 0;
  }
  return g_rt.world.ControlCenters()[static_cast<size_t>(index)].control_center_id;
}

float NcGetControlCenterX(int32_t index) {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!EnsureWorldLoadedLocked() || index < 0 ||
      static_cast<size_t>(index) >= g_rt.world.ControlCenters().size()) {
    return 0.0F;
  }
  return static_cast<float>(g_rt.world.ControlCenters()[static_cast<size_t>(index)].x);
}

float NcGetControlCenterY(int32_t index) {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!EnsureWorldLoadedLocked() || index < 0 ||
      static_cast<size_t>(index) >= g_rt.world.ControlCenters().size()) {
    return 0.0F;
  }
  return static_cast<float>(g_rt.world.ControlCenters()[static_cast<size_t>(index)].y);
}

float NcGetControlCenterZ(int32_t index) {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!EnsureWorldLoadedLocked() || index < 0 ||
      static_cast<size_t>(index) >= g_rt.world.ControlCenters().size()) {
    return 0.0F;
  }
  return static_cast<float>(g_rt.world.ControlCenters()[static_cast<size_t>(index)].z);
}

int32_t NcGetSubTerritoryOwner(int32_t sub_territory_id) {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!EnsureWorldLoadedLocked()) {
    return 0;
  }
  return ResolveOwnerFactionIdLocked(sub_territory_id);
}

uint32_t NcGetFactionColorRgba(int32_t faction_id) {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!EnsureWorldLoadedLocked()) {
    return 0xAAAAAAFFU;
  }
  return ResolveFactionColorLocked(faction_id);
}

Red::CString NcGetControlCenterTooltipTitle(int32_t sub_territory_id) {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!EnsureWorldLoadedLocked()) {
    return Red::CString("Control Center");
  }
  const auto* st = g_rt.world.FindSubTerritory(sub_territory_id);
  return Red::CString(st != nullptr ? st->display_name.c_str() : "Control Center");
}

std::string FormatSubdistrictDisplay(const std::string& district_name, const std::string& gamedata_sub) {
  if (gamedata_sub.empty()) return district_name;
  if (gamedata_sub == "LittleChina") return district_name + " - Little China";
  if (gamedata_sub == "Kabuki") return district_name + " - Kabuki";
  if (gamedata_sub == "Northside") return district_name + " - Northside";
  if (gamedata_sub == "ArasakaWaterfront") return district_name + " - Arasaka Waterfront";
  if (gamedata_sub == "JapanTown") return district_name + " - Japantown";
  if (gamedata_sub == "CharterHill") return district_name + " - Charter Hill";
  if (gamedata_sub == "NorthOaks") return district_name + " - North Oak";
  if (gamedata_sub == "VistaDelRey") return district_name + " - Vista Del Rey";
  if (gamedata_sub == "Glen") return district_name + " - The Glen";
  if (gamedata_sub == "Wellsprings") return district_name + " - Wellsprings";
  if (gamedata_sub == "Arroyo") return district_name + " - Arroyo";
  if (gamedata_sub == "RanchoCoronado") return district_name + " - Rancho Coronado";
  if (gamedata_sub == "Coastview") return district_name + " - Coastview";
  if (gamedata_sub == "WestWindEstate") return district_name + " - West Wind Estate";
  if (gamedata_sub == "Downtown") return district_name + " - Downtown";
  if (gamedata_sub == "CorpoPlaza") return district_name + " - Corpo Plaza";
  return district_name;
}

Red::CString NcGetControlCenterTooltipDesc(int32_t sub_territory_id) {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!EnsureWorldLoadedLocked()) {
    return Red::CString("");
  }
  const auto* st = g_rt.world.FindSubTerritory(sub_territory_id);
  if (st == nullptr) {
    return Red::CString("");
  }
  const auto* dist = g_rt.world.FindDistrict(st->district_id);
  const std::string base_dist = dist != nullptr ? dist->display_name : "Night City";
  const std::string dist_name = FormatSubdistrictDisplay(base_dist, st->gamedata_subdistrict);
  const int32_t owner_id = ResolveOwnerFactionIdLocked(sub_territory_id);
  const std::string owner_name = ResolveFactionNameLocked(owner_id);
  const auto* org = g_rt.session_active
                        ? neon::sim::SimEngine::FindPlayerOrgConst(g_rt.state)
                        : nullptr;
  const bool is_player = (org != nullptr && owner_id == org->faction_id);
  const auto* active = g_rt.session_active
                           ? neon::sim::SimEngine::FindActiveCombatMissionConst(g_rt.state)
                           : nullptr;
  const bool is_raid = (active != nullptr && active->sub_territory_id == sub_territory_id);
  const std::string desc = neon::sim::SimEngine::FormatTerritoryTooltipDesc(
      dist_name,
      owner_name,
      st->base_income_per_cycle,
      is_player,
      is_raid,
      is_raid ? active->kills_done : 0,
      is_raid ? active->kills_required : 0);
  return Red::CString(desc.c_str());
}

int32_t NcLookupSubTerritoryAt(float x, float y) {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!EnsureWorldLoadedLocked()) {
    return 0;
  }
  return g_rt.world.LookupSubTerritoryAt(static_cast<double>(x), static_cast<double>(y));
}

int32_t NcFindBestSubTerritoryAt(float x, float y) {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!EnsureWorldLoadedLocked()) {
    return 0;
  }
  const int32_t exact = g_rt.world.LookupSubTerritoryAt(static_cast<double>(x), static_cast<double>(y));
  if (exact > 0) {
    return exact;
  }
  return g_rt.world.FindNearestSubTerritory(static_cast<double>(x), static_cast<double>(y));
}

// --- Org, Economy & Combat Mission Commands / Queries -----------------------

bool NcHasPlayerOrg() {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  return g_rt.session_active && neon::sim::SimEngine::FindPlayerOrgConst(g_rt.state) != nullptr;
}

Red::CString NcGetPlayerOrgName() {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!g_rt.session_active) {
    return Red::CString("");
  }
  const auto* org = neon::sim::SimEngine::FindPlayerOrgConst(g_rt.state);
  return Red::CString(org != nullptr ? org->display_name.c_str() : "");
}

int32_t NcGetPlayerOwnedCount() {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!g_rt.session_active) {
    return 0;
  }
  const auto* org = neon::sim::SimEngine::FindPlayerOrgConst(g_rt.state);
  if (org == nullptr) {
    return 0;
  }
  return neon::sim::SimEngine::CountOwnedTerritories(g_rt.state, org->faction_id);
}

int64_t NcGetPlayerCycleIncome() {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!g_rt.session_active || g_rt.engine == nullptr) {
    return 0;
  }
  const auto* org = neon::sim::SimEngine::FindPlayerOrgConst(g_rt.state);
  if (org == nullptr) {
    return 0;
  }
  return g_rt.engine->ComputeCycleIncome(g_rt.state, org->faction_id);
}

int64_t NcGetPlayerTreasury() {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!g_rt.session_active) {
    return 0;
  }
  const auto* org = neon::sim::SimEngine::FindPlayerOrgConst(g_rt.state);
  return org != nullptr ? org->treasury_eddies : 0;
}

int32_t NcFoundGang(Red::CString display_name, int32_t home_sub_territory_id, int32_t game_seconds) {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!g_rt.session_active || g_rt.engine == nullptr) {
    return -1;
  }
  const std::string name(display_name.c_str());
  auto res = g_rt.engine->FoundGang(g_rt.state, name, home_sub_territory_id, game_seconds);
  if (!res.ok) {
    LogWarn(("NcFoundGang rejected: " + res.error).c_str());
    return -1;
  }
  std::string err;
  const int32_t rev = g_rt.playthrough.CommitState(g_rt.state, res.emitted, true, err);
  if (rev <= 0) {
    LogError(("NcFoundGang commit failed: " + err).c_str());
    return -1;
  }
  const auto* st = g_rt.world.FindSubTerritory(home_sub_territory_id);
  const std::string st_name = st != nullptr ? st->display_name : "Control Center";
  const int64_t daily = g_rt.engine->ComputeCycleIncome(g_rt.state, neon::sim::kPlayerFactionIdBase);
  PushHudNoticeLocked(
      "GANG FOUNDED: " + name + " | Claimed " + st_name +
      " (" + std::to_string(daily) + " eb/day)");
  return rev;
}

int32_t NcOfferCombatMission(
    int32_t sub_territory_id, int32_t control_center_id, int32_t reward_eddies, int32_t game_seconds) {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!g_rt.session_active || g_rt.engine == nullptr) {
    return -1;
  }
  auto res = g_rt.engine->OfferCombatMission(
      g_rt.state, sub_territory_id, control_center_id, reward_eddies, game_seconds);
  if (!res.ok) {
    LogWarn(("NcOfferCombatMission rejected: " + res.error).c_str());
    return -1;
  }
  std::string err;
  if (g_rt.playthrough.CommitState(g_rt.state, res.emitted, false, err) <= 0) {
    LogError(("NcOfferCombatMission commit failed: " + err).c_str());
    return -1;
  }
  g_rt.counted_kill_entities.clear();
  return g_rt.state.missions.empty() ? -1 : g_rt.state.missions.back().mission_id;
}

int32_t NcOfferNearestRivalMission(float x, float y, int32_t game_seconds) {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!g_rt.session_active || g_rt.engine == nullptr) {
    return -1;
  }
  const auto* org = neon::sim::SimEngine::FindPlayerOrgConst(g_rt.state);
  if (org == nullptr) {
    return -1;
  }
  if (const auto* existing = neon::sim::SimEngine::FindActiveCombatMissionConst(g_rt.state);
      existing != nullptr) {
    return existing->mission_id;
  }

  const int32_t rival_st = g_rt.world.FindNearestRivalSubTerritory(
      static_cast<double>(x), static_cast<double>(y), org->faction_id, g_rt.state.territories);
  if (rival_st <= 0) {
    PushHudNoticeLocked("No rival territories remaining in Night City.");
    return -1;
  }
  const auto* st = g_rt.world.FindSubTerritory(rival_st);
  const auto* cc = g_rt.world.FindControlCenterBySubTerritory(rival_st);
  if (st == nullptr || cc == nullptr) {
    return -1;
  }

  const int32_t reward = 1500 + std::max(0, st->defense_rating) * 250;
  auto res = g_rt.engine->OfferCombatMission(
      g_rt.state, rival_st, cc->control_center_id, reward, game_seconds,
      neon::sim::kDefaultCombatKillsRequired);
  if (!res.ok) {
    LogWarn(("NcOfferNearestRivalMission rejected: " + res.error).c_str());
    return -1;
  }
  std::string err;
  if (g_rt.playthrough.CommitState(g_rt.state, res.emitted, false, err) <= 0) {
    LogError(("NcOfferNearestRivalMission commit failed: " + err).c_str());
    return -1;
  }
  g_rt.counted_kill_entities.clear();

  const auto* m = neon::sim::SimEngine::FindActiveCombatMissionConst(g_rt.state);
  const std::string rival_name = m != nullptr ? ResolveFactionNameLocked(m->target_faction_id) : "Rival";
  PushHudNoticeLocked(
      "RIVAL RAID: Clear " + st->display_name + " (" + rival_name + ") — " +
      std::to_string(neon::sim::kDefaultCombatKillsRequired) + " hostiles | +" +
      std::to_string(reward) + " eb");
  return m != nullptr ? m->mission_id : -1;
}

int64_t NcCompleteMission(int32_t mission_id, int32_t game_seconds) {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!g_rt.session_active || g_rt.engine == nullptr) {
    return -1;
  }
  auto res = g_rt.engine->CompleteMission(g_rt.state, mission_id, game_seconds);
  if (!res.ok) {
    LogWarn(("NcCompleteMission rejected: " + res.error).c_str());
    return -1;
  }
  std::string err;
  if (g_rt.playthrough.CommitState(g_rt.state, res.emitted, false, err) <= 0) {
    LogError(("NcCompleteMission commit failed: " + err).c_str());
    return -1;
  }
  g_rt.counted_kill_entities.clear();
  return res.payout_eddies;
}

int64_t NcOnNpcIncapacitated(
    uint64_t entity_hash,
    int32_t affiliation_enum,
    bool is_crowd,
    bool is_civilian,
    bool is_vendor,
    bool is_hostile,
    float x,
    float y,
    float z,
    int32_t game_seconds) {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!g_rt.session_active || g_rt.engine == nullptr || entity_hash == 0U) {
    return 0;
  }
  if (!neon::sim::SimEngine::IsValidRaidCombatant(
          is_crowd, is_civilian, is_vendor, is_hostile, affiliation_enum)) {
    return 0;
  }
  const auto* active = neon::sim::SimEngine::FindActiveCombatMissionConst(g_rt.state);
  if (active == nullptr) {
    return 0;
  }
  if (g_rt.counted_kill_entities.contains(entity_hash)) {
    return 0;
  }
  const auto* cc = g_rt.world.FindControlCenterBySubTerritory(active->sub_territory_id);
  if (cc == nullptr) {
    return 0;
  }

  const double dx = static_cast<double>(x) - cc->x;
  const double dy = static_cast<double>(y) - cc->y;
  const double dz = std::abs(static_cast<double>(z) - cc->z);
  if ((dx * dx + dy * dy) > (kCombatMissionRadiusXY * kCombatMissionRadiusXY) ||
      dz > kCombatMissionRadiusZ) {
    return 0;
  }

  const int32_t mission_id = active->mission_id;
  const int32_t target_st = active->sub_territory_id;
  g_rt.counted_kill_entities.insert(entity_hash);

  auto res = g_rt.engine->RecordMissionKill(g_rt.state, mission_id, game_seconds);
  if (!res.ok) {
    return 0;
  }

  std::string err;
  if (g_rt.playthrough.CommitState(g_rt.state, res.emitted, false, err) <= 0) {
    LogError(("NcOnNpcIncapacitated commit failed: " + err).c_str());
    return -1;
  }

  const auto* st = g_rt.world.FindSubTerritory(target_st);
  const std::string st_name = st != nullptr ? st->display_name : "Control Center";

  if (res.payout_eddies > 0) {
    g_rt.counted_kill_entities.clear();
    const auto* org = neon::sim::SimEngine::FindPlayerOrgConst(g_rt.state);
    const int64_t daily = org != nullptr
                              ? g_rt.engine->ComputeCycleIncome(g_rt.state, org->faction_id)
                              : 0;
    PushHudNoticeLocked(
        "TERRITORY CAPTURED: " + st_name + " | +" + std::to_string(res.payout_eddies) +
        " eb | Income: " + std::to_string(daily) + " eb/day");
    return res.payout_eddies;
  }

  const auto* updated = neon::sim::SimEngine::FindActiveCombatMissionConst(g_rt.state);
  if (updated != nullptr) {
    PushHudNoticeLocked(
        "Raid Progress (" + st_name + "): " + std::to_string(updated->kills_done) + "/" +
        std::to_string(updated->kills_required) + " hostiles");
  }
  return 0;
}

int64_t NcAdvanceTime(int32_t current_game_seconds) {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!g_rt.session_active || g_rt.engine == nullptr) {
    return 0;
  }
  auto res = g_rt.engine->AdvanceTime(g_rt.state, current_game_seconds);
  if (!res.ok || res.emitted.empty()) {
    return 0;
  }
  std::string err;
  if (g_rt.playthrough.CommitState(g_rt.state, res.emitted, false, err) <= 0) {
    LogError(("NcAdvanceTime commit failed: " + err).c_str());
    return -1;
  }
  if (res.payout_eddies > 0) {
    const auto* org = neon::sim::SimEngine::FindPlayerOrgConst(g_rt.state);
    const int32_t owned = org != nullptr
                              ? neon::sim::SimEngine::CountOwnedTerritories(g_rt.state, org->faction_id)
                              : 0;
    PushHudNoticeLocked(
        "TERRITORY INCOME: +" + std::to_string(res.payout_eddies) +
        " eb (" + std::to_string(owned) + " zones)");
  }
  return res.payout_eddies;
}

int32_t NcGetActiveMissionId() {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!g_rt.session_active) return 0;
  const auto* m = neon::sim::SimEngine::FindActiveCombatMissionConst(g_rt.state);
  return m != nullptr ? m->mission_id : 0;
}

int32_t NcGetActiveMissionSubTerritoryId() {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!g_rt.session_active) return 0;
  const auto* m = neon::sim::SimEngine::FindActiveCombatMissionConst(g_rt.state);
  return m != nullptr ? m->sub_territory_id : 0;
}

float NcGetActiveMissionTargetX() {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!g_rt.session_active) return 0.0F;
  const auto* m = neon::sim::SimEngine::FindActiveCombatMissionConst(g_rt.state);
  const auto* cc = m != nullptr ? g_rt.world.FindControlCenterBySubTerritory(m->sub_territory_id) : nullptr;
  return cc != nullptr ? static_cast<float>(cc->x) : 0.0F;
}

float NcGetActiveMissionTargetY() {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!g_rt.session_active) return 0.0F;
  const auto* m = neon::sim::SimEngine::FindActiveCombatMissionConst(g_rt.state);
  const auto* cc = m != nullptr ? g_rt.world.FindControlCenterBySubTerritory(m->sub_territory_id) : nullptr;
  return cc != nullptr ? static_cast<float>(cc->y) : 0.0F;
}

float NcGetActiveMissionTargetZ() {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!g_rt.session_active) return 0.0F;
  const auto* m = neon::sim::SimEngine::FindActiveCombatMissionConst(g_rt.state);
  const auto* cc = m != nullptr ? g_rt.world.FindControlCenterBySubTerritory(m->sub_territory_id) : nullptr;
  return cc != nullptr ? static_cast<float>(cc->z) : 0.0F;
}

int32_t NcGetPauseMenuActionCode(bool ascendancy_enabled) {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  return static_cast<int32_t>(
      neon::sim::SimEngine::ResolvePauseMenuAction(g_rt.state, ascendancy_enabled));
}

Red::CString NcGetPauseMenuLabel(bool ascendancy_enabled) {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  const std::string label =
      neon::sim::SimEngine::FormatPauseMenuLabel(g_rt.state, ascendancy_enabled);
  return Red::CString(label.c_str());
}

Red::CString NcFormatStatusSummary() {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!g_rt.session_active || g_rt.engine == nullptr) {
    return Red::CString("Neon Ascendancy session not initialized.");
  }
  std::string target_name;
  if (const auto* m = neon::sim::SimEngine::FindActiveCombatMissionConst(g_rt.state);
      m != nullptr) {
    if (const auto* st = g_rt.world.FindSubTerritory(m->sub_territory_id); st != nullptr) {
      target_name = st->display_name;
    }
  }
  const std::string summary = g_rt.engine->FormatStatusSummary(g_rt.state, target_name);
  return Red::CString(summary.c_str());
}

} // namespace

RTTI_DEFINE_GLOBALS({
  RTTI_FUNCTION(NcCoreVersion, "NeonAscendancy.Core.NcCoreVersion");
  RTTI_FUNCTION(NcLogInfo, "NeonAscendancy.Core.NcLogInfo");
  RTTI_FUNCTION(NcSetSanitizerActive, "NeonAscendancy.Core.NcSetSanitizerActive");
  RTTI_FUNCTION(NcIsSanitizerActive, "NeonAscendancy.Core.NcIsSanitizerActive");
  RTTI_FUNCTION(NcSetAscendancyStartPending, "NeonAscendancy.Core.NcSetAscendancyStartPending");
  RTTI_FUNCTION(NcIsAscendancyStartPending, "NeonAscendancy.Core.NcIsAscendancyStartPending");
  RTTI_FUNCTION(NcArmAscendancyStart, "NeonAscendancy.Core.NcArmAscendancyStart");
  RTTI_FUNCTION(NcDisarmAscendancyStart, "NeonAscendancy.Core.NcDisarmAscendancyStart");
  RTTI_FUNCTION(NcIsSuppressedVanillaMappinVariant, "NeonAscendancy.Core.NcIsSuppressedVanillaMappinVariant");
  RTTI_FUNCTION(NcClearControlCenterPins, "NeonAscendancy.Core.NcClearControlCenterPins");
  RTTI_FUNCTION(NcBindControlCenterPin, "NeonAscendancy.Core.NcBindControlCenterPin");
  RTTI_FUNCTION(NcLookupControlCenterPin, "NeonAscendancy.Core.NcLookupControlCenterPin");
  RTTI_FUNCTION(NcGetBoundControlCenterPinCount, "NeonAscendancy.Core.NcGetBoundControlCenterPinCount");
  RTTI_FUNCTION(NcGetSafeSanctuaryCount, "NeonAscendancy.Core.NcGetSafeSanctuaryCount");
  RTTI_FUNCTION(NcPopHudNotice, "NeonAscendancy.Core.NcPopHudNotice");
  RTTI_FUNCTION(NcEvaluateSanitizer, "NeonAscendancy.Core.NcEvaluateSanitizer");
  RTTI_FUNCTION(NcGetEraName, "NeonAscendancy.Core.NcGetEraName");
  RTTI_FUNCTION(NcClearSafeSanctuaries, "NeonAscendancy.Core.NcClearSafeSanctuaries");
  RTTI_FUNCTION(NcRegisterSafeSanctuaryPin, "NeonAscendancy.Core.NcRegisterSafeSanctuaryPin");
  RTTI_FUNCTION(NcIsAllowedSafeZone, "NeonAscendancy.Core.NcIsAllowedSafeZone");
  RTTI_FUNCTION(NcSessionBegin, "NeonAscendancy.Core.NcSessionBegin");
  RTTI_FUNCTION(NcSessionGetPlaythroughIdHi, "NeonAscendancy.Core.NcSessionGetPlaythroughIdHi");
  RTTI_FUNCTION(NcSessionGetPlaythroughIdLo, "NeonAscendancy.Core.NcSessionGetPlaythroughIdLo");
  RTTI_FUNCTION(NcSessionCurrentRevision, "NeonAscendancy.Core.NcSessionCurrentRevision");
  RTTI_FUNCTION(NcSessionEnd, "NeonAscendancy.Core.NcSessionEnd");
  RTTI_FUNCTION(NcGetControlCenterCount, "NeonAscendancy.Core.NcGetControlCenterCount");
  RTTI_FUNCTION(NcGetControlCenterSubTerritoryId, "NeonAscendancy.Core.NcGetControlCenterSubTerritoryId");
  RTTI_FUNCTION(NcGetControlCenterId, "NeonAscendancy.Core.NcGetControlCenterId");
  RTTI_FUNCTION(NcGetControlCenterX, "NeonAscendancy.Core.NcGetControlCenterX");
  RTTI_FUNCTION(NcGetControlCenterY, "NeonAscendancy.Core.NcGetControlCenterY");
  RTTI_FUNCTION(NcGetControlCenterZ, "NeonAscendancy.Core.NcGetControlCenterZ");
  RTTI_FUNCTION(NcGetSubTerritoryOwner, "NeonAscendancy.Core.NcGetSubTerritoryOwner");
  RTTI_FUNCTION(NcGetFactionColorRgba, "NeonAscendancy.Core.NcGetFactionColorRgba");
  RTTI_FUNCTION(NcGetControlCenterTooltipTitle, "NeonAscendancy.Core.NcGetControlCenterTooltipTitle");
  RTTI_FUNCTION(NcGetControlCenterTooltipDesc, "NeonAscendancy.Core.NcGetControlCenterTooltipDesc");
  RTTI_FUNCTION(NcLookupSubTerritoryAt, "NeonAscendancy.Core.NcLookupSubTerritoryAt");
  RTTI_FUNCTION(NcFindBestSubTerritoryAt, "NeonAscendancy.Core.NcFindBestSubTerritoryAt");
  RTTI_FUNCTION(NcHasPlayerOrg, "NeonAscendancy.Core.NcHasPlayerOrg");
  RTTI_FUNCTION(NcGetPlayerOrgName, "NeonAscendancy.Core.NcGetPlayerOrgName");
  RTTI_FUNCTION(NcGetPlayerOwnedCount, "NeonAscendancy.Core.NcGetPlayerOwnedCount");
  RTTI_FUNCTION(NcGetPlayerCycleIncome, "NeonAscendancy.Core.NcGetPlayerCycleIncome");
  RTTI_FUNCTION(NcGetPlayerTreasury, "NeonAscendancy.Core.NcGetPlayerTreasury");
  RTTI_FUNCTION(NcFoundGang, "NeonAscendancy.Core.NcFoundGang");
  RTTI_FUNCTION(NcOfferCombatMission, "NeonAscendancy.Core.NcOfferCombatMission");
  RTTI_FUNCTION(NcOfferNearestRivalMission, "NeonAscendancy.Core.NcOfferNearestRivalMission");
  RTTI_FUNCTION(NcCompleteMission, "NeonAscendancy.Core.NcCompleteMission");
  RTTI_FUNCTION(NcOnNpcIncapacitated, "NeonAscendancy.Core.NcOnNpcIncapacitated");
  RTTI_FUNCTION(NcAdvanceTime, "NeonAscendancy.Core.NcAdvanceTime");
  RTTI_FUNCTION(NcGetActiveMissionId, "NeonAscendancy.Core.NcGetActiveMissionId");
  RTTI_FUNCTION(NcGetActiveMissionSubTerritoryId, "NeonAscendancy.Core.NcGetActiveMissionSubTerritoryId");
  RTTI_FUNCTION(NcGetActiveMissionTargetX, "NeonAscendancy.Core.NcGetActiveMissionTargetX");
  RTTI_FUNCTION(NcGetActiveMissionTargetY, "NeonAscendancy.Core.NcGetActiveMissionTargetY");
  RTTI_FUNCTION(NcGetActiveMissionTargetZ, "NeonAscendancy.Core.NcGetActiveMissionTargetZ");
  RTTI_FUNCTION(NcGetPauseMenuActionCode, "NeonAscendancy.Core.NcGetPauseMenuActionCode");
  RTTI_FUNCTION(NcGetPauseMenuLabel, "NeonAscendancy.Core.NcGetPauseMenuLabel");
  RTTI_FUNCTION(NcFormatStatusSummary, "NeonAscendancy.Core.NcFormatStatusSummary");
  LogInfo("Registered 56 NeonAscendancy.Core native RTTI globals");
});

BOOL WINAPI DllMain(HINSTANCE hinst, DWORD reason, LPVOID) {
  if (reason == DLL_PROCESS_ATTACH) {
    g_module_handle = hinst;
    DisableThreadLibraryCalls(hinst);
  }
  return TRUE;
}

RED4EXT_C_EXPORT bool RED4EXT_CALL Main(
    RED4ext::v1::PluginHandle aHandle,
    RED4ext::v1::EMainReason aReason,
    const RED4ext::v1::Sdk* aSdk) {
  switch (aReason) {
    case RED4ext::v1::EMainReason::Load: {
      g_plugin_handle = aHandle;
      g_sdk = aSdk;
      g_rt.plugin_dir_utf8 = ResolvePluginDirUtf8();
      Red::TypeInfoRegistrar::RegisterDiscovered();
      LogInfo("NeonAscendancy native core loaded");
      break;
    }
    case RED4ext::v1::EMainReason::Unload: {
      NcDisarmAscendancyStart();
      std::lock_guard<std::mutex> lock(g_rt.mu);
      g_rt.session_active = false;
      g_rt.counted_kill_entities.clear();
      g_rt.hud_notices.clear();
      g_rt.playthrough.Close(true);
      g_rt.world.Close();
      LogInfo("NeonAscendancy native core unloaded");
      break;
    }
  }
  return true;
}

RED4EXT_C_EXPORT void RED4EXT_CALL Query(RED4ext::v1::PluginInfo* aInfo) {
  aInfo->name = L"NeonAscendancy";
  aInfo->author = L"Neon Ascendancy";
  aInfo->version = RED4EXT_V1_SEMVER(0, 0, 0);
  aInfo->runtime = RED4EXT_V1_RUNTIME_VERSION_LATEST;
  aInfo->sdk = RED4EXT_V1_SDK_VERSION_CURRENT;
}

RED4EXT_C_EXPORT uint32_t RED4EXT_CALL Supports() {
  return RED4EXT_API_VERSION_1;
}
