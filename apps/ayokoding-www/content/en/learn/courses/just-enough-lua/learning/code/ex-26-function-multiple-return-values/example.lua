-- Example 26: functions returning multiple values
local function minmax(a, b) -- => a function that returns TWO values, not a table or list
	if a < b then -- => compares the two parameters
		return a, b -- => returns a as the min, b as the max
	else -- => taken when a is not less than b
		return b, a -- => returns b as the min, a as the max
	end -- => closes the if/else
end -- => closes the function
local lo, hi = minmax(5, 2) -- => both return values are captured in one multiple-assignment
print(lo, hi) -- => Output: 2    5
