-- Example 49: function recursion -- factorial
local function fact(n) -- => `local function` (not `local fact = function`) lets fact call ITSELF
	if n == 0 then -- => base case check
		return 1 -- => base case: 0! is 1
	else -- => recursive case
		return n * fact(n - 1) -- => n! is n times (n-1)!
	end -- => closes the if/else
end -- => closes the function
print(fact(5)) -- => 5 * 4 * 3 * 2 * 1 = 120
-- => Output: 120
