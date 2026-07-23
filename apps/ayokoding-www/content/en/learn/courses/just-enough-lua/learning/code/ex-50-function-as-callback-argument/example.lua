-- Example 50: passing a function as a callback argument
local function apply(f, x) -- => f is an ordinary parameter that happens to hold a function value
	return f(x) -- => calls whatever function was passed, with x as its argument
end
print(apply(function(x)
	return x * x
end, 5))
-- => an anonymous function is passed directly as the first argument
-- => apply calls it with x=5, squaring: 25
-- => Output: 25
