-- Example 24: basic function definition and call
local function add(a, b) -- => `local function` names the function for recursion/reuse
	return a + b -- => returns the sum of its two parameters
end -- => closes the function body
print(add(2, 3)) -- => calls add with a=2, b=3
-- => Output: 5
