#include <Windows.h>

#include <cstdio>
#include <memory>
#include <mutex>
#include <string>
#include <vector>

#include <RED4ext/RED4ext.hpp>
#include <RedLib.hpp>

#include "sim.hpp"
#include "store.hpp"

namespace {

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
  uint32_t playthrough_id_hi = 0;
  uint32_t playthrough_id_lo = 0;
  bool world_loaded = false;
  bool session_active = false;
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

// --- Native functions exposed to redscript 1.x via RedLib -------------------

Red::CString NcCoreVersion() {
  return Red::CString("0.0.0-dev");
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
    // Let PlaythroughDb generate ID on a temporary unique path? Generate here first
    // so filename matches the stored playthrough_id deterministically.
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
  g_rt.session_active = true;
  LogInfo("NcSessionBegin succeeded");
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
  return g_rt.playthrough.Close(true);
}

int32_t NcLookupSubTerritoryAt(float x, float y) {
  std::lock_guard<std::mutex> lock(g_rt.mu);
  if (!EnsureWorldLoadedLocked()) {
    return 0;
  }
  return g_rt.world.LookupSubTerritoryAt(static_cast<double>(x), static_cast<double>(y));
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
  return g_rt.state.missions.empty() ? -1 : g_rt.state.missions.back().mission_id;
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
  return res.payout_eddies;
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
  return res.payout_eddies;
}

} // namespace

RTTI_DEFINE_GLOBALS({
  RTTI_FUNCTION(NcCoreVersion);
  RTTI_FUNCTION(NcSessionBegin);
  RTTI_FUNCTION(NcSessionGetPlaythroughIdHi);
  RTTI_FUNCTION(NcSessionGetPlaythroughIdLo);
  RTTI_FUNCTION(NcSessionCurrentRevision);
  RTTI_FUNCTION(NcSessionEnd);
  RTTI_FUNCTION(NcLookupSubTerritoryAt);
  RTTI_FUNCTION(NcFoundGang);
  RTTI_FUNCTION(NcOfferCombatMission);
  RTTI_FUNCTION(NcCompleteMission);
  RTTI_FUNCTION(NcAdvanceTime);
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
      std::lock_guard<std::mutex> lock(g_rt.mu);
      g_rt.session_active = false;
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
