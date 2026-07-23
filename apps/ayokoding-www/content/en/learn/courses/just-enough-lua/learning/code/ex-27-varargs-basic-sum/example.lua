-- Example 27: varargs -- a basic sum function
local function sum(...) -- => `...` declares a variable number of arguments
	local s = 0 -- => accumulator starts at 0
	for _, v in ipairs({ ... }) do -- => {...} packs the varargs into a table, then ipairs walks it
		s = s + v -- => accumulates each value into s
	end -- => closes the for-loop
	return s -- => returns the final total
end -- => closes the function
print(sum(1, 2, 3)) -- => called with three arguments: 1, 2, 3
-- => Output: 6
