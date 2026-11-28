local visible, floor, call, seen, lines = false, 0, 0, 0, {}
local function system()
  local ok, value = pcall(function() return Game.GetScriptableSystemsContainer():Get('NeonAscendancy.Dev.NeonAscendancy_GarrisonSpike') end)
  if ok then return value end
end
local function log(line)
  lines[#lines + 1] = line
  if #lines > 10 then table.remove(lines, 1) end
  local file = io.open('spike.log', 'a')
  if file then file:write(line, '\n'); file:close() end
end
local function invoke(name, ...)
  local s = system()
  if not s then log('GarrisonSpike: Q1 UNKNOWN system unavailable'); return end
  local args = {...}
  local ok, err = pcall(function() s[name](s, unpack(args)) end)
  if not ok then log('GarrisonSpike: Q1 UNKNOWN panel error ' .. tostring(err)) end
end
local function capture()
  local player = Game.GetPlayer()
  if not player then return end
  local q = Game['TSQ_ALL;']()
  q.maxDistance = 30
  q.testedSet = TargetingSet.Complete
  local ok, parts = Game.GetTargetingSystem():GetTargetParts(player, q)
  local closest, distance
  if ok and parts then
    local p = player:GetWorldPosition()
    for _, part in ipairs(parts) do
      local success, obj = pcall(function() return part:GetComponent(part):GetEntity() end)
      if success and obj and obj:IsA('LiftDevice') then
        local v = obj:GetWorldPosition()
        local d = (v.x-p.x)^2 + (v.y-p.y)^2 + (v.z-p.z)^2
        if not distance or d < distance then closest, distance = obj, d end
      end
    end
  end
  if closest then
    local success, active = pcall(function() return closest:GetDevicePS():GetActiveFloor() end)
    if success then call, floor = active, active + 1 end
    invoke('CaptureLift', closest)
  else log('GarrisonSpike: Q4 UNKNOWN no lift found in targeting query') end
end
registerForEvent('onOverlayOpen', function() visible = true end)
registerForEvent('onOverlayClose', function() visible = false end)
registerForEvent('onUpdate', function()
  local s = system()
  if not s then return end
  local ok, count = pcall(function() return s:LogCount() end)
  if not ok then return end
  if count < seen then seen = 0 end
  for i = seen, count - 1 do
    local success, line = pcall(function() return s:LogAt(i) end)
    if success and line ~= '' then log(line) end
  end
  seen = count
end)
registerForEvent('onDraw', function()
  if not visible then return end
  ImGui.Begin('Neon Ascendancy Garrison Spike')
  if ImGui.Button('Q1 Spawn') then invoke('Q1') end
  if ImGui.Button('Q2 PowerLevel') then invoke('Q2') end
  if ImGui.Button('Q3 AI') then invoke('Q3') end
  if ImGui.Button('Q4 Lift capture') then capture() end
  call = ImGui.InputInt('Call cab to floor (where you stand)', call)
  floor = ImGui.InputInt('Ride to floor', floor)
  if ImGui.Button('Lift board & ride') then invoke('LiftRide', call, floor) end
  if ImGui.Button('Q5 Name') then invoke('Q5') end
  if ImGui.Button('Cleanup') then invoke('Cleanup') end
  for _, line in ipairs(lines) do ImGui.TextWrapped(line) end
  ImGui.End()
end)
