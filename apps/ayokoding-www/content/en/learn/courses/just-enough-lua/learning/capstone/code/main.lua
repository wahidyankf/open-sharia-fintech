-- main.lua -- capstone: tables, closures, a required module, a metatable, and pcall error handling together
local store = require("store") -- => runs store.lua once, caches its return value: {new = <function>}

local s = store.new() -- => a fresh closure-backed store instance; its internal data starts empty

-- Set and get several keys ---------------------------------------------------
s.set("username", "alice") -- => writes directly into this instance's own data
print(s.get("username")) -- => Output: alice

print(s.get("theme")) -- => "theme" was never set on this instance -- __index falls through
-- => Output: default
s.set("theme", "dark") -- => an explicit set always overrides whatever default __index would supply
print(s.get("theme")) -- => Output: dark

-- An array-shaped value, walked with ipairs ----------------------------------
s.set("tags", { "work", "urgent" })
for i, tag in ipairs(s.get("tags")) do
	print(i, tag) -- => Output: 1  work   then   2  urgent
end

-- Every key actually set on this instance, walked with pairs (then sorted) ---
for _, key in ipairs(s.keys()) do
	print(key) -- => Output: tags, theme, username -- one per line, alphabetical
end

-- A deliberately failing lookup, caught cleanly with pcall -------------------
local ok, result = pcall(function()
	return s.get_required("api_key")
end)
if not ok then
	print(nil, result) -- => pcall caught the error -- print nil (no value) beside the err message
	-- => Output: nil  missing required key: api_key
else
	print(result)
end
