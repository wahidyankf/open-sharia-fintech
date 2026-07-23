-- Example 54: metatable __index as a table -- inheritance-style fallback
local defaults = { inherited_field = "from-defaults" } -- => a plain table of fallback values
local t = {} -- => t starts empty; it has no inherited_field of its own
setmetatable(t, { __index = defaults }) -- => __index as a TABLE redirects failed lookups to that table
print(t.inherited_field) -- => t.inherited_field isn't in t, so the lookup falls through to defaults
-- => Output: from-defaults
