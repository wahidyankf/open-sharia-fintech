-- Example 63: metatable __eq -- overriding the equality operator
local mt = {} -- => a shared metatable for both objects below
mt.__eq = function(a, b)
	return a.id == b.id
end -- => __eq only fires when BOTH operands share this metatable
local a = setmetatable({ id = 1 }, mt) -- => a and b are two DISTINCT table objects
local b = setmetatable({ id = 1 }, mt) -- => same id, but a different table identity from a
print(a == b) -- => without __eq, a == b would be false (different table identities)
-- => with __eq, equality is redefined by id instead -- Output: true
