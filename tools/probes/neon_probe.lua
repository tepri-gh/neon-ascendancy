-- Neon Ascendancy Phase 0 Dev-Only CET Probe Helper
-- Installed to bin/x64/plugins/cyber_engine_tweaks/mods/NeonAscendancyProbe/init.lua
-- by tools/install-dev-cet.sh.
--
-- Usage in CET console:
--   p = GetMod("NeonAscendancyProbe")
--   p.help()
--
-- ALWAYS run destructive probes (unlock, suppress_quests) on a COPY of your save.

local Probe = {}

local ERA_FACTS = {
  "watson_prolog_lock", "watson_prolog_unlock",
  "q000_done", "q001_done", "q001_active",
  "q003_done", "q004_done",
  "q005_start", "q005_active", "q005_done",
  "q101_active", "q101_done",
  "q101_enable_activities_flat", "q101_enable_side_content",
  "q112_done", "q115_point_of_no_return", "q115_done", "q116_done",
  "q201_done", "q202_done", "q203_done", "q204_done",
  "ep1_installed", "ep1_standalone", "ep1_active", "ep1_side_content",
  "q301_00_done", "q301_active", "q301_done", "q302_done",
  "johnny_on", "johnny_off", "johnny_default_on", "johnny_mirror",
  "isPlayerPossessedByJohnny",
}

function Probe.help()
  print("=== NeonAscendancyProbe (Phase 0 dev probes) ===")
  print("  p.snapshot()         -- Step 0.1: print canonical era & Johnny facts (read-only)")
  print("  p.classify()         -- Step 0.1: classify current save era (read-only)")
  print("  p.unlock_minimal()   -- Step 0.1: lift Watson lockdown + clear FT locks (COPY SAVE)")
  print("  p.unlock_act2()      -- Step 0.1: enable q101_enable_activities_flat/side_content (COPY SAVE)")
  print("  p.audit_quests()     -- Step 0.1: list active quests & tracked entry (read-only)")
  print("  p.suppress_quests()  -- Step 0.1: mark vanilla quests Inactive & untrack (COPY SAVE)")
  print("  p.audit_mappins()    -- Step 0.1: summarize map mappins by variant (read-only)")
  print("  p.audit_johnny()     -- Step 0.1: print Johnny facts & vehicle passengers (read-only)")
  print("  p.test_johnny_off()  -- Step 0.1: test candidate Johnny off facts + remove JohnnySickness (COPY SAVE)")
  print("  p.audit_dialog()     -- Step 0.1: dump active dialog choices & QuestImportant flags (open dialog first)")
  print("  p.watch_calls()      -- Step 0.1: log PhoneSystem.OnTriggerCall events")
  print("  p.player_pos()       -- Step 0.2: print player world X/Y/Z & current district")
  print("  p.dump_tweak_check() -- Step 0.2/0.4: count Character & District records in runtime TweakDB")
end

function Probe.snapshot()
  local qs = Game.GetQuestsSystem()
  print("=== Era & Johnny Fact Snapshot ===")
  for _, name in ipairs(ERA_FACTS) do
    print(string.format("  %-34s = %d", name, qs:GetFactStr(name)))
  end
end

function Probe.classify()
  local qs = Game.GetQuestsSystem()
  local function f(n) return qs:GetFactStr(n) end

  local era
  if f("ep1_standalone") > 0 then
    era = "PLStandalone"
  elseif f("q201_done") > 0 or f("q202_done") > 0 or f("q203_done") > 0 or f("q204_done") > 0 then
    era = "PostStory"
  elseif f("q115_point_of_no_return") > 0 or f("q116_done") > 0 then
    era = "Endgame"
  elseif f("q005_done") > 0 then
    if f("q101_done") > 0 or f("q101_enable_side_content") > 0 or f("watson_prolog_lock") == 0 then
      era = "Act2"
    else
      era = "Interlude"
    end
  elseif f("watson_prolog_unlock") > 0 then
    era = "Interlude"
  elseif f("q001_done") > 0 then
    era = "Act1PreHeist"
  elseif f("q005_active") > 0 or f("q001_active") > 0 or f("q000_done") > 0 then
    era = "Prologue"
  else
    era = "Unknown"
  end

  print("ERA=" .. era)
  print("IntroSkipped=" .. tostring(f("q001_done") > 0 and f("q000_done") == 0))
  print("HeistSkipped=" .. tostring(f("q005_done") == 0 and (f("q101_done") > 0 or f("q101_enable_side_content") > 0)))
  print("LockAlreadyLifted=" .. tostring(f("watson_prolog_lock") == 0 and f("q005_done") == 0))
  return era
end

function Probe.unlock_minimal()
  local qs = Game.GetQuestsSystem()
  local function set(n, v)
    if qs:GetFactStr(n) ~= v then
      qs:SetFactStr(n, v)
      print("SET " .. n .. " = " .. tostring(v))
    end
  end

  set("watson_prolog_lock", 0)
  set("watson_prolog_unlock", 1)

  local ft = Game.GetScriptableSystemsContainer():Get("FastTravelSystem")
  if ft then
    ft:QueueRequest(RemoveAllFastTravelLocksRequest.new())
    local evt = FastTravelMenuToggledEvent.new()
    evt.isEnabled = true
    ft:QueueRequest(evt)
    print("FastTravel locks cleared & map FT enabled")
  else
    print("WARN: FastTravelSystem not found")
  end
end

function Probe.unlock_act2()
  local qs = Game.GetQuestsSystem()
  for _, n in ipairs({ "q101_enable_activities_flat", "q101_enable_side_content" }) do
    if qs:GetFactStr(n) == 0 then
      qs:SetFactStr(n, 1)
      print("SET " .. n .. " = 1")
    else
      print("KEEP " .. n .. " = " .. tostring(qs:GetFactStr(n)))
    end
  end
end

local function get_active_quests()
  local jm = Game.GetJournalManager()
  local filter = JournalRequestStateFilter.new()
  filter.active = true
  filter.inactive = false
  filter.succeeded = false
  filter.failed = false

  local ctx = JournalRequestContext.new()
  ctx.stateFilter = filter

  local ok, res = pcall(function()
    local out = {}
    local ret = jm:GetQuests(ctx, out)
    if type(ret) == "table" and #ret > 0 then
      return ret
    end
    return out
  end)
  if ok and type(res) == "table" then
    return jm, res
  end
  return jm, {}
end

function Probe.audit_quests()
  local jm, quests = get_active_quests()
  print("Active quests: " .. tostring(#quests))
  for _, q in ipairs(quests) do
    print(string.format("  hash=%-10s id=%-45s state=%s",
      tostring(jm:GetEntryHash(q)), q:GetId(), tostring(jm:GetEntryState(q))))
  end
  local tracked = jm:GetTrackedEntry()
  print("Tracked: " .. (tracked and tracked:GetId() or "nil"))
end

function Probe.suppress_quests()
  local jm, quests = get_active_quests()
  local count = 0
  for _, q in ipairs(quests) do
    local id = q:GetId()
    if string.sub(id, 1, 6) == "quests" or string.sub(id, 1, 9) == "ep1/quest" then
      jm:ChangeEntryStateByHash(jm:GetEntryHash(q), 1, 1) -- Inactive, DoNotNotify
      count = count + 1
    end
  end
  if jm:GetTrackedEntry() ~= nil then
    jm:UntrackEntry()
  end
  print("Suppressed " .. tostring(count) .. " vanilla quests and cleared tracked entry.")
end

function Probe.audit_mappins()
  local ms = Game.GetMappinSystem()
  local ok, mappins = pcall(function()
    local out = {}
    local ret = ms:GetMappins(gamemappinsMappinTargetType.Map, out)
    if type(ret) == "table" and #ret > 0 then return ret end
    return out
  end)
  if not ok or type(mappins) ~= "table" then
    print("WARN: GetMappins failed")
    return
  end
  local counts = {}
  for _, m in ipairs(mappins) do
    local v = tostring(m:GetVariant())
    counts[v] = (counts[v] or 0) + 1
  end
  print("Total map mappins: " .. tostring(#mappins))
  for k, v in pairs(counts) do
    print(string.format("  %-40s %d", k, v))
  end
end

function Probe.audit_johnny()
  local qs = Game.GetQuestsSystem()
  for _, n in ipairs({ "johnny_on", "johnny_off", "johnny_default_on", "johnny_mirror", "isPlayerPossessedByJohnny" }) do
    print(string.format("  %-28s = %d", n, qs:GetFactStr(n)))
  end

  local player = Game.GetPlayer()
  if not player then return end
  local mf = Game.GetMountingFacility()
  local single = mf:GetMountingInfoSingleWithIds(player:GetEntityID())
  if single and single.parentId and EntityID.IsDefined(single.parentId) then
    print("Mounted in vehicle=" .. tostring(single.parentId))
    local infos = mf:GetMountingInfoMultipleWithIds(single.parentId)
    for _, info in ipairs(infos) do
      local e = Game.FindEntityByID(info.childId)
      print(string.format("  slot=%s child=%s record=%s",
        tostring(info.slotId), tostring(info.childId),
        e and tostring(e:GetRecordID()) or "nil"))
    end
  else
    print("Player not mounted in a vehicle.")
  end
end

function Probe.test_johnny_off()
  local qs = Game.GetQuestsSystem()
  local player = Game.GetPlayer()
  if player then
    StatusEffectHelper.RemoveStatusEffectsWithTag(player, "JohnnySickness")
    print("Removed JohnnySickness status effects")
  end
  qs:SetFactStr("johnny_off", 1)
  qs:SetFactStr("johnny_on", 0)
  qs:SetFactStr("johnny_default_on", 0)
  qs:SetFactStr("isPlayerPossessedByJohnny", 0)
  print("Set candidate Johnny off facts. Enter a vehicle alone and wait 60-120s to test passenger.")
end

function Probe.audit_dialog()
  local bb = Game.GetBlackboardSystem():Get(GetAllBlackboardDefs().UIInteractions)
  local v = bb:GetVariant(GetAllBlackboardDefs().UIInteractions.DialogChoiceHubs)
  local d = FromVariant(v)
  if not d then
    print("FromVariant returned nil; raw variant:")
    print(v)
    return
  end
  for i, hub in ipairs(d.choiceHubs) do
    print(string.format("HUB %d title=%s choices=%d", i, tostring(hub.title), #hub.choices))
    for j, c in ipairs(hub.choices) do
      print(string.format("  [%d] %s | type=%s", j, tostring(c.localizedName), tostring(c.type)))
    end
  end
end

local watching_calls = false
function Probe.watch_calls()
  if watching_calls then
    print("Already watching PhoneSystem.OnTriggerCall")
    return
  end
  watching_calls = true
  Observe("PhoneSystem", "OnTriggerCall", function(_, request)
    print(string.format("CALL caller=%s addressee=%s phase=%s player=%s",
      tostring(request.caller), tostring(request.addressee),
      tostring(request.callPhase), tostring(request.isPlayerTriggered)))
  end)
  print("Watching PhoneSystem.OnTriggerCall")
end

function Probe.player_pos()
  local player = Game.GetPlayer()
  if not player then return end
  local pos = player:GetWorldPosition()
  local ps = Game.GetScriptableSystemsContainer():Get("PreventionSystem")
  local dist = ps and ps:GetCurrentDistrict()
  local dname = (dist and dist:GetDistrictRecord()) and tostring(dist:GetDistrictRecord():EnumName()) or "unknown"
  print(string.format("POS X=%.3f Y=%.3f Z=%.3f | district=%s", pos.x, pos.y, pos.z, dname))
end

function Probe.dump_tweak_check()
  local chars = TweakDB:GetRecords("gamedataCharacter_Record")
  local dists = TweakDB:GetRecords("gamedataDistrict_Record")
  print(string.format("Runtime TweakDB: %d Character records, %d District records", #chars, #dists))
end

registerForEvent("onInit", function()
  print("[NeonAscendancyProbe] Ready. In console: p = GetMod(\"NeonAscendancyProbe\"); p.help()")
end)

return Probe
