-- Example 76: rawget/rawequal -- bypassing metamethods
local mt = { -- => a metatable with two metamethods
	__index = function()
		return "default"
	end,
	__eq = function()
		return true
	end,
} -- => closes the metatable literal
local a = setmetatable({}, mt) -- => a is an empty table wearing mt
local b = setmetatable({}, mt) -- => b is a SEPARATE empty table, also wearing mt
print(a.missing, rawget(a, "missing")) -- => a.missing triggers __index: "default"
-- => rawget(a, "missing") skips __index entirely: nil (truly absent)
-- => Output: default    nil
print(a == b, rawequal(a, b)) -- => a == b triggers __eq: true
-- => rawequal(a, b) skips __eq entirely: false (different identities)
-- => Output: true    false
