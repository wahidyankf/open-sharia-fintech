-- Example 53: metatable __index as a function -- default values
local t = {} -- => t starts as an empty table
setmetatable(t, {
	__index = function()
		return "N/A"
	end,
})
-- => __index as a FUNCTION is called on any failed lookup: (table, key)
print(t.missing) -- => t.missing isn't in t, so __index fires and returns "N/A"
-- => Output: N/A
