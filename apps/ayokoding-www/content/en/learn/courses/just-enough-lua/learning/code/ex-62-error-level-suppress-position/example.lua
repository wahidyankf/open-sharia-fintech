-- Example 62: error() with level 0 -- suppressing the position prefix
local ok, err = pcall(function()
	error("raw", 0) -- => the second argument to error() is a LEVEL; 0 means "add no position info"
end) -- => closes the protected function
print(err) -- => with level 0, err is exactly "raw" -- no "file:line:" prefix at all
-- => Output: raw
