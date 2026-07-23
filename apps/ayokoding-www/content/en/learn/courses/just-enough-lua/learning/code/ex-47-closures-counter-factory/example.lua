-- Example 47: closures -- a counter factory
local function makeCounter() -- => a function that BUILDS and returns another function
	local n = 0 -- => n is local to makeCounter's call, not global
	return function() -- => this inner function is a CLOSURE: it captures n as an upvalue
		n = n + 1 -- => mutates the captured n on every call
		return n -- => returns the new count
	end -- => closes the inner closure
end -- => closes makeCounter
local c = makeCounter() -- => c is the closure; n keeps living on as its private state
print(c(), c(), c()) -- => each call mutates the SAME captured n, surviving between calls
-- => Output: 1    2    3
