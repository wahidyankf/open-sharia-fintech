-- Example 55: metatable __tostring -- customizing print()
local p = { x = 1, y = 2 } -- => a plain table with x and y fields
setmetatable(p, { -- => attaches a metatable with one metamethod
	__tostring = function(p)
		return "Point(" .. p.x .. "," .. p.y .. ")"
	end,
}) -- => __tostring is called whenever the value is coerced to a string
print(p) -- => print() calls tostring() on each argument internally
-- => Output: Point(1,2)
