-- Example 48: closures -- independent instances
local function makeCounter() -- => builds a fresh closure with its own private n each call
	local n = 0 -- => n is local to THIS call of makeCounter
	return function() -- => the returned closure captures this call's n
		n = n + 1 -- => mutates the captured n
		return n -- => returns the new count
	end -- => closes the inner closure
end -- => closes makeCounter
local c1 = makeCounter() -- => c1 gets its OWN private n, separate from any other counter
local c2 = makeCounter() -- => c2 gets a SECOND, independent n
print(c1(), c1(), c2()) -- => c1 is called twice (n: 1, then 2); c2 is called once (n: 1)
-- => Output: 1    2    1
