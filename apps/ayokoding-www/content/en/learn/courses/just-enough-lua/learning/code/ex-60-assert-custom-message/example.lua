-- Example 60: assert() with a custom message
local ok, err = pcall(function()
	assert(false, "custom failure") -- => assert raises when its first argument is falsy, using message as the error
end) -- => closes the protected function
print(err) -- => like error() with a string message, assert's string message also gets
-- => a "file:line:" position prefix
-- => Output: example.lua:3: custom failure
