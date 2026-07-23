-- Example 58: error() with a message, caught by pcall()
local ok, err = pcall(function() -- => pcall calls its function argument in PROTECTED mode
	error("boom") -- => error() raises a Lua error carrying the value "boom"
end) -- => closes the protected function
print(ok, err) -- => ok is false since the protected call raised an error
-- => err is "boom" prefixed with "file:line:" by default (level 1)
-- => Output: false    example.lua:3: boom
