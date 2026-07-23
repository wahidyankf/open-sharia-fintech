-- Example 51: a function returning a function -- adder
local function adder(n) -- => adder takes n and returns a NEW function specialized to that n
	return function(x) -- => this closure captures n as an upvalue
		return x + n -- => adds the captured n to whatever x is passed later
	end -- => closes the inner closure
end -- => closes adder
local add5 = adder(5) -- => add5 is a closure that always adds 5
print(add5(10)) -- => 10 + 5
-- => Output: 15
