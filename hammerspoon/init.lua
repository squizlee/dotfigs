-- Managed by dotfigs: ~/.hammerspoon/init.lua -> hammerspoon/init.lua.
-- Hammerspoon needs Accessibility permission (System Settings > Privacy & Security).

-- Start Hammerspoon at login so the hotkeys below always work.
hs.autoLaunch(true)

-- Lets the `hs` CLI talk to this instance, e.g. `hs -c 'hs.reload()'`.
require("hs.ipc")

-- Leader: ctrl+; then a key. Times out, or escape cancels.
-- (cmd+` is Ghostty's own dropdown terminal; see ghostty/config.)
local LEADER_TIMEOUT = 1.5
local leader = hs.hotkey.modal.new({ "ctrl" }, ";")
local apps = {
  t = "Ghostty",
}

local hint, timer
function leader:entered()
  if timer then timer:stop() end
  local keys = {}
  for key, name in pairs(apps) do table.insert(keys, key .. " " .. name) end
  table.sort(keys)
  hint = hs.alert.show(table.concat(keys, "   "), LEADER_TIMEOUT)
  timer = hs.timer.doAfter(LEADER_TIMEOUT, function() leader:exit() end)
end

function leader:exited()
  if timer then timer:stop() end
  if hint then hs.alert.closeSpecific(hint) end
end

leader:bind({}, "escape", function() leader:exit() end)
for key, name in pairs(apps) do
  leader:bind({}, key, function()
    leader:exit()
    hs.application.launchOrFocus(name)
  end)
end
