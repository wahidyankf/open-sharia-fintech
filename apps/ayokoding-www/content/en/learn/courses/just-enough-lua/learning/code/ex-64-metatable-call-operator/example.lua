-- Example 64: metatable __call -- making a table callable
local mt = {} -- => a metatable holding one metamethod
mt.__call = function(self, ...)
	return "called"
end -- => self is the table itself, then the call's arguments
local t = setmetatable({}, mt) -- => t is an ordinary table wearing mt as its metatable
print(t(1, 2)) -- => t(1, 2) invokes __call(t, 1, 2) since t is not itself a function
-- => Output: called
