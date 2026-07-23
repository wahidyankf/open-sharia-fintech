-- Example 25: the `or` default-parameter idiom
local function greet(name) -- => Lua has no native default-parameter syntax
	name = name or "world" -- => if name is nil (omitted), fall back to "world"
	return "Hello " .. name -- => builds the greeting string
end -- => closes the function body
print(greet()) -- => called with zero arguments, so the parameter name is nil
-- => Output: Hello world
