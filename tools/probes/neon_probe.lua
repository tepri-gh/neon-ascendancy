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

-- CET keeps one callback per event per mod: a second registerForEvent for the
-- same event replaces the first. The tour's onUpdate silently replaced
-- noclip's, and the checklist's onDraw replaced the note window. Register
-- each event once and fan out to every handler instead.
local handlers = {}
local function on(event, fn)
  if not handlers[event] then
    handlers[event] = {}
    local list = handlers[event]
    registerForEvent(event, function(...)
      for _, f in ipairs(list) do f(...) end
    end)
  end
  table.insert(handlers[event], fn)
end

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
  print("  p.look_at()          -- log the object under the crosshair (also hotkey 'Neon: log look-at')")
  print("  p.invisible()        -- toggle invisible to AI (also hotkey 'Neon: invisible to AI' and the Neon tour panel)")
  print("  p.noclip()           -- toggle noclip (also hotkey 'Neon: noclip toggle'; uses normal movement keys, Shift = fast)")
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
    return jm:GetQuests(ctx)
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
    return ms:GetMappins(gamemappinsMappinTargetType.Map)
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

-- Look-at logger (dev-only). Bind "Neon: log look-at" in CET Bindings, look at an
-- object and press the key. Logs to the CET console and NeonAscendancyProbe.log so
-- the agent can identify exactly what the owner sees. Baked static meshes are not
-- entities, so "nothing" means the target is world geometry, not a device or NPC.
local function safe(f, ...)
  local ok, v = pcall(f, ...)
  if ok then return v end
  return nil
end

local function emit(line)
  print(line)
  -- Append to lookat.log in this mod's folder and close at once, so each line
  -- is on disk immediately (CET's own logs are buffered until exit).
  local f = io.open("lookat.log", "a")
  if f then
    f:write(os.date("%H:%M:%S "), line, "\n")
    f:close()
  end
end

function Probe.look_at()
  local player = Game.GetPlayer()
  if not player then return end
  local ppos = player:GetWorldPosition()
  local obj = Game.GetTargetingSystem():GetLookAtObject(player, false, false)
  if not obj then
    emit(string.format("LOOKAT nothing (static world geometry?) player=(%.3f,%.3f,%.3f)", ppos.x, ppos.y, ppos.z))
    return
  end
  local pos = obj:GetWorldPosition()
  local id = safe(function() return obj:GetEntityID().hash end)
  local cls = safe(function() return obj:GetClassName().value end) or "?"
  local app = safe(function() return obj:GetCurrentAppearanceName().value end) or "?"
  local line = string.format("LOOKAT class=%s id=%s app=%s pos=(%.3f,%.3f,%.3f) player=(%.3f,%.3f,%.3f) dist=%.2f",
    cls, tostring(id), app, pos.x, pos.y, pos.z, ppos.x, ppos.y, ppos.z, Vector4.Distance(pos, ppos))
  if obj:IsA("Device") then
    local ps = safe(function() return obj:GetDevicePS() end)
    if ps then
      local psCls = safe(function() return ps:GetClassName().value end) or "?"
      line = line .. string.format(" ps=%s powered=%s disabled=%s", psCls,
        tostring(safe(function() return ps:IsPowered() end)), tostring(safe(function() return ps:IsDisabled() end)))
      if ps:IsA("DoorControllerPS") then
        line = line .. string.format(" open=%s locked=%s sealed=%s",
          tostring(safe(function() return ps:IsOpen() end)), tostring(safe(function() return ps:IsLocked() end)),
          tostring(safe(function() return ps:IsSealed() end)))
      end
      -- In-world ways to open it (owner policy: such doors stay vanilla).
      -- Mirrors doorController.swift:84's "no way to open" test.
      line = line .. string.format(" skillCheck=%s quickhack=%s authValid=%s",
        tostring(safe(function() return ps:HasAnySkillCheckActive() end)),
        tostring(safe(function() return ps:CanCreateAnyQuickHackActions() end)),
        tostring(safe(function() return ps:IsAuthorizationValid() end)))
    end
  end
  if obj:IsA("ScriptedPuppet") then
    local rec = safe(function() return obj:GetRecordID() end)
    local aff = safe(function() return obj:GetRecord():Affiliation():Type().value end)
    line = line .. string.format(" record=%s affiliation=%s", rec and TDBID.ToStringDEBUG(rec) or "?", tostring(aff))
  end
  emit(line)
end

-- Noclip (dev-only). Toggle with "Neon: noclip toggle". While on, the normal
-- movement keys drive it: move forward/back/strafe follow the camera, Jump goes
-- up, Crouch goes down, Sprint (Shift) is fast. The player is held in place and
-- moved by teleporting each frame, so walls and gravity are ignored.
local fly = { on = false, pos = nil, mx = 0.0, my = 0.0, up = false, down = false, fast = false, speed = 8.0 }

function Probe.noclip(enable)
  local player = Game.GetPlayer()
  if not player then return end
  if enable == nil then enable = not fly.on end
  fly.on = enable
  fly.pos = enable and player:GetWorldPosition() or nil
  fly.mx, fly.my, fly.up, fly.down, fly.fast = 0.0, 0.0, false, false, false
  emit("NOCLIP " .. (enable and "on" or "off"))
end

registerHotkey("NeonNoclip", "Neon: noclip toggle", function() Probe.noclip() end)

-- Invisible to AI (dev-only, owner request 2026-11-26 for touring hostile
-- venues). PlayerPuppet.SetInvisible switches off the visibility component AI
-- perception uses; vanilla uses the same call for the spawn grace period and
-- optical camo. Camo ending, EnablePlayerVisibilityEvent and the grace period
-- can switch it back on, so it is re-applied every frame while enabled.
local ghost = { on = false }

function Probe.invisible(enable)
  local player = Game.GetPlayer()
  if not player then return end
  if enable == nil then enable = not ghost.on end
  ghost.on = enable
  player:SetInvisible(enable)
  emit("INVISIBLE " .. (enable and "on" or "off"))
end

registerHotkey("NeonInvisible", "Neon: invisible to AI", function() Probe.invisible() end)

on("onUpdate", function()
  if not ghost.on then return end
  local player = Game.GetPlayer()
  if player and not player:IsInvisible() then player:SetInvisible(true) end
end)

local function setup_noclip_input()
  Observe("PlayerPuppet", "OnAction", function(_, action)
    if not fly.on then return end
    local name = Game.NameToString(ListenerAction.GetName(action))
    local kind = ListenerAction.GetType(action).value
    local value = ListenerAction.GetValue(action)
    local pressed = kind == "BUTTON_PRESSED" or kind == "BUTTON_HOLD_PROGRESS"
    local released = kind == "BUTTON_RELEASED"
    if name == "MoveX" then fly.mx = value
    elseif name == "MoveY" then fly.my = value
    elseif name == "Jump" then
      if pressed then fly.up = true elseif released then fly.up = false end
    elseif name == "Crouch" or name == "ToggleCrouch" then
      if pressed then fly.down = true elseif released then fly.down = false end
    elseif name == "Sprint" or name == "ToggleSprint" then
      if pressed then fly.fast = true elseif released then fly.fast = false end
    end
  end)
end

on("onUpdate", function(dt)
  if not fly.on or not fly.pos then return end
  local player = Game.GetPlayer()
  if not player then fly.on = false; return end
  local f = Game.GetCameraSystem():GetActiveCameraForward()
  -- Horizontal right vector for strafing.
  local rl = math.sqrt(f.x * f.x + f.y * f.y)
  local rx, ry = 0.0, 0.0
  if rl > 0.0001 then rx, ry = f.y / rl, -f.x / rl end
  local step = fly.speed * (fly.fast and 4.0 or 1.0) * dt
  local dx = (f.x * fly.my + rx * fly.mx) * step
  local dy = (f.y * fly.my + ry * fly.mx) * step
  local dz = f.z * fly.my * step
  if fly.up then dz = dz + step end
  if fly.down then dz = dz - step end
  local p = fly.pos
  p = Vector4.new(p.x + dx, p.y + dy, p.z + dz, 1.0)
  fly.pos = p
  Game.GetTeleportationFacility():Teleport(player, p, player:GetWorldOrientation():ToEulerAngles())
end)

registerHotkey("NeonLookAt", "Neon: log look-at", function() Probe.look_at() end)
registerHotkey("NeonPlayerPos", "Neon: log player position", function()
  local player = Game.GetPlayer()
  if not player then return end
  local p = player:GetWorldPosition()
  emit(string.format("PLAYERPOS (%.3f,%.3f,%.3f)", p.x, p.y, p.z))
end)

-- ---------------------------------------------------------------- dev tour
-- Visits every venue in tour_stops.lua (generated by
-- `tools/venue-proposals.py tour-stops`). At each stop it teleports, waits for
-- streaming, then logs every NPC in the stop's radius to tour.log as one JSON
-- line: record, affiliation, high-level state, stance, workspot, attitude to
-- the player, dead. tools/venue-tour-report.py turns tour.log, notes.log and
-- the native DoorPolicy lines into a per-venue anomaly list. Hotkeys:
-- "Neon: tour start/resume", "Neon: tour skip stop", "Neon: tour stop".
-- A stop with a checklist waits after its scan until the checklist is saved
-- (or skipped); "Neon: checklist here" opens the nearest venue's list anytime.
-- Console: p.tour_start("code") starts at a named stop.

-- mode "tour" skips stops already toured (tour_stops.lua `done`) and waits
-- for checklists; mode "sweep" visits every stop unattended and also logs the
-- doors, lifts and lift terminals in range (see Probe.sweep_start).
local tour = { stops = nil, i = 0, state = "idle", t = 0.0, settle = 20.0, mode = "tour" }

local function json_str(s)
  s = tostring(s)
  s = s:gsub('\\', '\\\\'):gsub('"', '\\"'):gsub('\n', '\\n'):gsub('\r', '\\r'):gsub('\t', '\\t')
  return '"' .. s .. '"'
end

local function json_enc(v)
  local t = type(v)
  if t == "table" then
    if #v > 0 or next(v) == nil then
      local out = {}
      for _, x in ipairs(v) do out[#out + 1] = json_enc(x) end
      return "[" .. table.concat(out, ",") .. "]"
    end
    local out = {}
    for k, x in pairs(v) do out[#out + 1] = json_str(k) .. ":" .. json_enc(x) end
    return "{" .. table.concat(out, ",") .. "}"
  elseif t == "number" or t == "boolean" then
    return tostring(v)
  elseif v == nil then
    return "null"
  end
  return json_str(v)
end

local function append(file, line)
  local f = io.open(file, "a")
  if f then
    f:write(line, "\n")
    f:close()
  end
end

local function load_stops()
  if tour.stops then return tour.stops end
  -- CET resolves require() inside this mod's folder; dofile is the fallback.
  local ok, stops = pcall(require, "tour_stops")
  if not ok or type(stops) ~= "table" then ok, stops = pcall(dofile, "tour_stops.lua") end
  if not ok or type(stops) ~= "table" then
    emit("TOUR cannot load tour_stops.lua: " .. tostring(stops))
    return nil
  end
  tour.stops = stops
  return stops
end

local function nearest_stop(pos)
  local stops = load_stops()
  if not stops then return nil, nil end
  local best, bd = nil, nil
  for _, s in ipairs(stops) do
    local dx, dy, dz = pos.x - s.pos[1], pos.y - s.pos[2], pos.z - s.pos[3]
    local d = math.sqrt(dx * dx + dy * dy + dz * dz)
    if not bd or d < bd then best, bd = s, d end
  end
  return best, bd
end

local function scan_npcs(radius)
  local player = Game.GetPlayer()
  local out = {}
  local q = Game["TSQ_NPC;"]()
  q.maxDistance = radius
  q.testedSet = TargetingSet.Complete
  local ok, parts = Game.GetTargetingSystem():GetTargetParts(player, q)
  if not ok or not parts then return out end
  local seen = {}
  local ws = Game.GetWorkspotSystem()
  for _, part in ipairs(parts) do
    local npc = safe(function() return part:GetComponent(part):GetEntity() end)
    if npc and npc:IsA("NPCPuppet") then
      local id = tostring(safe(function() return npc:GetEntityID().hash end))
      if not seen[id] then
        seen[id] = true
        local pos = npc:GetWorldPosition()
        local rec = safe(function() return npc:GetRecordID() end)
        out[#out + 1] = {
          id = id,
          record = rec and TDBID.ToStringDEBUG(rec) or "?",
          affiliation = tostring(safe(function() return npc:GetRecord():Affiliation():Type().value end)),
          state = tostring(safe(function() return npc:GetHighLevelStateFromBlackboard().value end)),
          stance = tostring(safe(function() return npc:GetStanceStateFromBlackboard().value end)),
          workspot = safe(function() return ws:IsActorInWorkspot(npc) end) == true,
          attitude = tostring(safe(function() return npc:GetAttitudeTowards(player).value end)),
          dead = safe(function() return npc:IsDead() end) == true,
          pos = { pos.x, pos.y, pos.z },
        }
      end
    end
  end
  return out
end

-- Doors, lifts and lift terminals within the radius, with the raw state the
-- sweep report judges (tools/venue-tour-report.py): power, locks, seals, the
-- in-world ways in, lift door and side types. Read-only; nothing is changed.
local DEVICE_CLASSES = { "Door", "LiftDevice", "ElevatorFloorTerminal" }

local function scan_devices(radius)
  local player = Game.GetPlayer()
  local out = {}
  local q = Game["TSQ_ALL;"]()
  q.maxDistance = radius
  q.testedSet = TargetingSet.Complete
  local ok, parts = Game.GetTargetingSystem():GetTargetParts(player, q)
  if not ok or not parts then return out end
  local seen = {}
  for _, part in ipairs(parts) do
    local obj = safe(function() return part:GetComponent(part):GetEntity() end)
    local kind = nil
    if obj then
      for _, c in ipairs(DEVICE_CLASSES) do
        if obj:IsA(c) then kind = c end
      end
    end
    local id = kind and tostring(safe(function() return obj:GetEntityID().hash end))
    if kind and not seen[id] then
      seen[id] = true
      local pos = obj:GetWorldPosition()
      local ps = safe(function() return obj:GetDevicePS() end)
      local d = {
        id = id, kind = kind, pos = { pos.x, pos.y, pos.z },
        app = tostring(safe(function() return obj:GetCurrentAppearanceName().value end)),
      }
      if ps then
        d.powered = safe(function() return ps:IsPowered() end) == true
        d.disabled = safe(function() return ps:IsDisabled() end) == true
        if kind == "Door" then
          d.open = safe(function() return ps:IsOpen() end) == true
          d.locked = safe(function() return ps:IsLocked() end) == true
          d.sealed = safe(function() return ps:IsSealed() end) == true
          d.static = safe(function() return ps:IsStatic() end) == true
          d.auth_on = safe(function() return ps:IsAuthorizationModuleOn() end) == true
          d.auth_valid = safe(function() return ps:IsAuthorizationValid() end) == true
          d.skill = safe(function() return ps:HasAnySkillCheckActive() end) == true
          d.hack = safe(function() return ps:CanCreateAnyQuickHackActions() end) == true
          d.lift = safe(function() return ps:IsLiftDoor() end) == true
          d.shutter = safe(function() return ps:IsShutter() end) == true
          d.side1 = tostring(safe(function() return ps:GetDoorTypeSideOne().value end))
          d.side2 = tostring(safe(function() return ps:GetDoorTypeSideTwo().value end))
        end
      end
      out[#out + 1] = d
    end
  end
  return out
end

-- God mode for the unattended sweep (mines, turrets, hostile garrisons).
local function sweep_protect(enable)
  local player = Game.GetPlayer()
  if not player then return end
  local gms = Game.GetGodModeSystem()
  -- Invulnerable blocks damage; Immortal also keeps a fall or kill volume
  -- from killing (Invulnerable alone let V die in H10's atrium, 2026-11-27).
  for _, t in ipairs({ gameGodModeType.Invulnerable, gameGodModeType.Immortal }) do
    if enable then
      gms:AddGodMode(player:GetEntityID(), t, CName.new("NeonSweep"))
    else
      gms:RemoveGodMode(player:GetEntityID(), t, CName.new("NeonSweep"))
    end
  end
  Probe.invisible(enable)
end

local function tour_goto(i)
  local stops = load_stops()
  if not stops then return end
  if tour.mode == "tour" then
    while stops[i] and stops[i].done do i = i + 1 end
  end
  if tour.mode == "sweep" and stops[i] then
    -- Written before the teleport: if the game hangs loading this stop, the
    -- next resume sees a visit with no result and skips it.
    append("tour.log", json_enc({ event = "visit", time = os.date("%Y-%m-%d %H:%M:%S"), code = stops[i].code, mode = "sweep" }))
  end
  if i > #stops then
    -- God mode and invisibility stay on after a sweep: it ends wherever the
    -- last stop is (the owner died in the Badlands right after one). Starting
    -- the tour or "Stop sweep" turns them off.
    tour.state = "idle"
    emit("TOUR done (" .. #stops .. " stops)")
    append("tour.log", json_enc({ event = "done", time = os.date("%Y-%m-%d %H:%M:%S"), stops = #stops, mode = tour.mode }))
    return
  end
  local s = stops[i]
  tour.i, tour.state, tour.t, tour.retried = i, "settle", 0.0, false
  local player = Game.GetPlayer()
  if fly.on then fly.pos = Vector4.new(s.pos[1], s.pos[2], s.pos[3] + 1.5, 1.0) end
  Game.GetTeleportationFacility():Teleport(player, Vector4.new(s.pos[1], s.pos[2], s.pos[3] + 1.5, 1.0),
    player:GetWorldOrientation():ToEulerAngles())
  emit(string.format("TOUR %d/%d %s", i, #stops, s.code))
end

local function tour_scan()
  local s = tour.stops[tour.i]
  local npcs = scan_npcs(s.radius)
  local found = {}
  for _, n in ipairs(npcs) do found[n.record] = true end
  local missing = {}
  for _, r in ipairs(s.expected_records or {}) do
    if not found[r] then missing[#missing + 1] = r end
  end
  local p = Game.GetPlayer():GetWorldPosition()
  local devices = nil
  if tour.mode == "sweep" then devices = scan_devices(s.radius) end
  append("tour.log", json_enc({
    event = "stop", time = os.date("%Y-%m-%d %H:%M:%S"), code = s.code, venue = s.venue, kind = s.kind,
    mode = tour.mode, player = { p.x, p.y, p.z }, radius = s.radius, npcs = npcs, missing_records = missing,
    devices = devices,
  }))
  if tour.mode == "sweep" then
    emit(string.format("SWEEP %d/%d %s: %d npcs, %d devices", tour.i, #tour.stops, s.code, #npcs, #devices))
    tour_goto(tour.i + 1)
    return
  end
  emit(string.format("TOUR %s: %d npcs, %d expected records missing", s.code, #npcs, #missing))
  if s.checklist and #s.checklist > 0 then
    -- Wait here for the owner's checklist (drawn while the CET overlay is open).
    tour.state = "review"
    Probe.checklist_open(s, true)
    emit(string.format("TOUR %s: %d checks - open the CET overlay, then Next stop", s.code, #s.checklist))
  else
    tour_goto(tour.i + 1)
  end
end

-- ---------------------------------------------------------------- tour checklist
-- One window per venue: the generated checklist (tour_stops.lua `checklist`),
-- each item marked OK or Problem. Saving logs a "checklist" line to tour.log
-- for tools/venue-tour-report.py; unmarked items are reported as unchecked.

local review = nil       -- { stop, marks = {i -> "ok"|"problem"}, from_tour }
local last_review = nil  -- the checklist most recently closed without saving

function Probe.checklist_open(stop, from_tour)
  -- Reopening the stop you just closed keeps its marks.
  if last_review and last_review.stop.code == stop.code then
    review = last_review
    review.from_tour = review.from_tour or from_tour == true
  else
    review = { stop = stop, marks = {}, from_tour = from_tour == true }
  end
  last_review = nil
end

local function checklist_save()
  if not review then
    -- Window closed without saving: the skip hotkey still moves the tour on.
    if tour.state == "review" then tour_goto(tour.i + 1) end
    return
  end
  local s, results = review.stop, {}
  for i, c in ipairs(s.checklist or {}) do
    results[#results + 1] = { label = c.label, source = c.source, mark = review.marks[i] or "unchecked" }
  end
  local p = Game.GetPlayer():GetWorldPosition()
  append("tour.log", json_enc({
    event = "checklist", time = os.date("%Y-%m-%d %H:%M:%S"), code = s.code, venue = s.venue,
    player = { p.x, p.y, p.z }, items = results,
  }))
  emit("CHECKLIST saved for " .. s.code)
  local next_stop = review.from_tour and tour.state == "review"
  review = nil
  if next_stop then tour_goto(tour.i + 1) end
end
Probe.checklist_save = checklist_save

function Probe.tour_start(code)
  local stops = load_stops()
  if not stops then return end
  if tour.mode ~= "tour" then
    -- Coming from a sweep: start the tour from the top, not the sweep's index.
    tour.mode, tour.i = "tour", 0
    sweep_protect(false)
  end
  local start = (tour.state == "idle" and tour.i > 0 and tour.i < #stops) and tour.i or 1
  if code then
    for i, s in ipairs(stops) do if s.code == code then start = i end end
  end
  append("tour.log", json_enc({ event = "start", time = os.date("%Y-%m-%d %H:%M:%S"), from = stops[start].code }))
  tour_goto(start)
end

function Probe.tour_stop()
  if tour.mode == "sweep" then sweep_protect(false) end
  tour.state = "idle"
  emit("TOUR stopped at " .. tostring(tour.i))
end

-- Unattended sweep of every stop, toured or not: no checklists, god mode and
-- invisibility on, doors and lifts logged. A stopped sweep resumes where it
-- left off. About 25 s a stop.
-- Stops already swept in the latest unfinished sweep run, read back from
-- tour.log, so a sweep resumes after a game crash or hang (Spidertank arena
-- load hang, 2026-11-27). Empty when the latest run finished. Also returns
-- the stop the game was loading when it died (a `visit` with no `stop` or
-- `skip` after it), so the resume can skip it instead of hanging again.
local function swept_in_last_run()
  local done, pending = {}, nil
  local f = io.open("tour.log", "r")
  if not f then return done, nil end
  for line in f:lines() do
    if line:find('"mode":"sweep"', 1, true) then
      local ev = line:match('"event":"(%w+)"')
      local c = line:match('"code":"([^"]+)"')
      if (ev == "start" and not line:find('"resume":true', 1, true)) or ev == "done" then
        done, pending = {}, nil
      elseif ev == "visit" then
        pending = c
      elseif (ev == "stop" or ev == "skip") and c then
        done[c] = true
        if pending == c then pending = nil end
      elseif ev == "abort" and pending == c then
        -- The player died there (the game did not hang): retry it on resume.
        pending = nil
      end
    end
  end
  f:close()
  return done, pending
end

function Probe.sweep_start(code)
  local stops = load_stops()
  if not stops then return end
  local start = 1
  local done, hung = swept_in_last_run()
  if hung then
    append("tour.log", json_enc({ event = "skip", time = os.date("%Y-%m-%d %H:%M:%S"), code = hung,
      reason = "game hung loading it last run", mode = "sweep" }))
    emit("SWEEP skipping " .. hung .. ": the game hung loading it last run")
    done[hung] = true
  end
  while stops[start] and done[stops[start].code] do start = start + 1 end
  local resume = start > 1 and start <= #stops
  if not resume then start = 1 end
  if code then
    resume = false
    for i, s in ipairs(stops) do if s.code == code then start = i end end
  end
  tour.mode = "sweep"
  sweep_protect(true)
  append("tour.log", json_enc({ event = "start", time = os.date("%Y-%m-%d %H:%M:%S"), from = stops[start].code,
    mode = "sweep", resume = resume }))
  emit(string.format("SWEEP %s at %d/%d %s", resume and "resuming" or "starting", start, #stops, stops[start].code))
  tour_goto(start)
end

registerHotkey("NeonTourStart", "Neon: tour start/resume", function() Probe.tour_start() end)
registerHotkey("NeonTourSkip", "Neon: tour skip stop", function()
  if tour.state == "review" then
    checklist_save()
  elseif tour.state ~= "idle" then
    tour_goto(tour.i + 1)
  end
end)
registerHotkey("NeonChecklist", "Neon: checklist here", function()
  local s, d = nearest_stop(Game.GetPlayer():GetWorldPosition())
  if not s then return end
  Probe.checklist_open(s, false)
  emit(string.format("CHECKLIST %s (%.0f m away) - open the CET overlay", s.code, d))
end)
registerHotkey("NeonTourStop", "Neon: tour stop", function() Probe.tour_stop() end)
registerHotkey("NeonSweepStart", "Neon: sweep start/resume", function() Probe.sweep_start() end)

-- How far from a stop the player may be and still count as arrived.
local ARRIVE_M = 30.0

on("onUpdate", function(dt)
  if tour.state ~= "settle" then return end
  tour.t = tour.t + dt
  if tour.t >= tour.settle then
    local player = Game.GetPlayer()
    local s = tour.stops[tour.i]
    -- A dead player cannot teleport: the first sweep kept "visiting" 66 stops
    -- from the death screen at the Kabuki gun trainer (2026-11-27).
    if not player or safe(function() return player:IsDead() end) then
      emit(string.format("TOUR stopped at %d %s: the player is dead", tour.i, s.code))
      append("tour.log", json_enc({ event = "abort", time = os.date("%Y-%m-%d %H:%M:%S"), code = s.code,
        reason = "player dead", mode = tour.mode }))
      tour.state = "idle"
      return
    end
    local p = player:GetWorldPosition()
    local off = math.sqrt((p.x - s.pos[1]) ^ 2 + (p.y - s.pos[2]) ^ 2)
    if off > ARRIVE_M then
      if not tour.retried then
        tour.retried, tour.t = true, 0.0
        Game.GetTeleportationFacility():Teleport(player, Vector4.new(s.pos[1], s.pos[2], s.pos[3] + 1.5, 1.0),
          player:GetWorldOrientation():ToEulerAngles())
        emit(string.format("TOUR %s: %.0f m off after teleport, retrying", s.code, off))
        return
      end
      emit(string.format("TOUR %s: did not arrive (%.0f m off), skipped", s.code, off))
      append("tour.log", json_enc({ event = "skip", time = os.date("%Y-%m-%d %H:%M:%S"), code = s.code,
        reason = "not arrived", off = off, mode = tour.mode }))
      tour_goto(tour.i + 1)
      return
    end
    tour.state = "scan"
    local ok, err = pcall(tour_scan)
    if not ok then
      emit("TOUR scan failed: " .. tostring(err))
      tour_goto(tour.i + 1)
    end
  end
end)

-- ---------------------------------------------------------------- playtest notes
-- "Neon: playtest note" stamps the player's position and nearest venue; open
-- the CET overlay to type the note and press Save. Notes go to notes.log as
-- JSON lines for tools/venue-tour-report.py.

local note = { pending = nil, text = "", overlay = false }

local function note_new()
  local p = Game.GetPlayer():GetWorldPosition()
  local s, d = nearest_stop(p)
  note.pending = { pos = { p.x, p.y, p.z }, stop = s and s.code or nil, dist = d, time = os.date("%Y-%m-%d %H:%M:%S") }
  note.text = ""
  emit(string.format("NOTE stamped at (%.1f,%.1f,%.1f) near %s - open the CET overlay to write it",
    p.x, p.y, p.z, tostring(s and s.code)))
end
registerHotkey("NeonNote", "Neon: playtest note", note_new)

on("onOverlayOpen", function() note.overlay = true end)
on("onOverlayClose", function() note.overlay = false end)

on("onDraw", function()
  if not note.pending or not note.overlay then return end
  if ImGui.Begin("Neon playtest note") then
    ImGui.Text(string.format("Near %s (%.0f m)", tostring(note.pending.stop), note.pending.dist or -1))
    note.text = ImGui.InputTextMultiline("##note", note.text, 2000, 420, 120)
    if ImGui.Button("Save") then
      note.pending.text = note.text
      append("notes.log", json_enc(note.pending))
      emit("NOTE saved: " .. note.text)
      note.pending = nil
    end
    ImGui.SameLine()
    if ImGui.Button("Discard") then note.pending = nil end
  end
  ImGui.End()
end)

on("onDraw", function()
  if not review or not note.overlay then return end
  local s = review.stop
  ImGui.SetNextWindowSize(560, 520, ImGuiCond.FirstUseEver)
  if ImGui.Begin("Neon tour checklist") then
    ImGui.TextWrapped(string.format("%s  (%s)", s.name or s.code, s.code))
    local done = 0
    for i in pairs(review.marks) do done = done + 1 end
    ImGui.Text(string.format("%d of %d marked", done, #s.checklist))
    ImGui.Separator()
    for i, c in ipairs(s.checklist) do
      ImGui.PushID(i)
      local m = review.marks[i]
      if ImGui.RadioButton("OK", m == "ok") then review.marks[i] = "ok" end
      ImGui.SameLine()
      if ImGui.RadioButton("Problem", m == "problem") then review.marks[i] = "problem" end
      ImGui.SameLine()
      if ImGui.TreeNode(c.label) then
        ImGui.TextWrapped(c.detail)
        ImGui.TreePop()
      end
      ImGui.PopID()
    end
    ImGui.Separator()
    if ImGui.Button("Add note") then
      local p = Game.GetPlayer():GetWorldPosition()
      note.pending = { pos = { p.x, p.y, p.z }, stop = s.code, dist = 0, time = os.date("%Y-%m-%d %H:%M:%S") }
      note.text = ""
    end
    ImGui.SameLine()
    if ImGui.Button(review.from_tour and "Save + next stop" or "Save") then checklist_save() end
    ImGui.SameLine()
    if ImGui.Button("Close") then last_review = review; review = nil end
  end
  ImGui.End()
end)

-- Always-available panel (owner request 2026-11-26): closing the checklist
-- or a note must never strand you, and it must not depend on bound hotkeys.
on("onDraw", function()
  if not note.overlay then return end
  if ImGui.Begin("Neon tour") then
    local stops = load_stops()
    if tour.state ~= "idle" and stops and stops[tour.i] then
      ImGui.Text(string.format("%s: stop %d/%d %s (%s)", tour.mode == "sweep" and "Sweep" or "Tour",
        tour.i, #stops, stops[tour.i].code, tour.state))
      if tour.mode == "sweep" then
        if ImGui.Button("Stop sweep") then Probe.tour_stop() end
      end
    else
      ImGui.Text("Tour: idle")
      if tour.mode == "sweep" then
        if ImGui.Button("End sweep protection") then Probe.tour_stop() end
      end
      if ImGui.Button("Start tour") then Probe.tour_start() end
      ImGui.SameLine()
      if ImGui.Button("Sweep all stops") then Probe.sweep_start() end
    end
    local nc = ImGui.Checkbox("Noclip", fly.on)
    if nc ~= fly.on then Probe.noclip(nc) end
    ImGui.SameLine()
    local inv = ImGui.Checkbox("Invisible to AI", ghost.on)
    if inv ~= ghost.on then Probe.invisible(inv) end
    if ImGui.Button("Checklist here") then
      local p = Game.GetPlayer():GetWorldPosition()
      local st = nearest_stop(p)
      if st then Probe.checklist_open(st, tour.state == "review" and stops and stops[tour.i] == st) end
    end
    if last_review then
      ImGui.SameLine()
      if ImGui.Button("Reopen " .. last_review.stop.code) then
        review = last_review
        last_review = nil
      end
    end
    ImGui.SameLine()
    if ImGui.Button("New note") then note_new() end
    if tour.state == "review" and not review then
      if ImGui.Button("Next stop") then tour_goto(tour.i + 1) end
    end
  end
  ImGui.End()
end)

on("onInit", function()
  setup_noclip_input()
  print("[NeonAscendancyProbe] Ready. In console: p = GetMod(\"NeonAscendancyProbe\"); p.help()")
end)

return Probe
