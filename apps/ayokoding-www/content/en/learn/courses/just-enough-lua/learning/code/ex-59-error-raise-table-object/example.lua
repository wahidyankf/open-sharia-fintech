-- Example 59: error() can raise ANY value, not just a string
local ok, err = pcall(function() -- => runs the inner function in protected mode
	error({ code = 42 }) -- => error()'s argument can be any Lua value -- here, a table
end) -- => closes the protected function
print(err.code) -- => err IS the table passed to error(), untouched
-- => (no "file:line:" prefix is added for non-string error objects)
-- => Output: 42
