-- Example 56: metatable __add -- operator overloading
local Vector = {} -- => the class table doubles as the metatable
Vector.__index = Vector -- => failed instance lookups fall back to Vector itself
function Vector.new(x, y)
	return setmetatable({ x = x, y = y }, Vector)
end -- => constructor
Vector.__add = function(a, b) -- => __add is called whenever two Vector values meet the `+` operator
	return Vector.new(a.x + b.x, a.y + b.y) -- => builds a new Vector from the componentwise sum
end -- => closes __add
local v1 = Vector.new(1, 2) -- => first operand
local v2 = Vector.new(3, 4) -- => second operand
print((v1 + v2).x) -- => v1 + v2 invokes __add, producing Vector(4, 6); .x reads the field
-- => Output: 4
