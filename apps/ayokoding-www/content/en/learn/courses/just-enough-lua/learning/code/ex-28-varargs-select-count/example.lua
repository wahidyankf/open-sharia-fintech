-- Example 28: varargs -- counting with select('#', ...)
local function count(...)
	return select("#", ...) -- => select('#', ...) returns the ARGUMENT COUNT, including nils
end -- => closes the function
print(count(1, nil, 3)) -- => three arguments passed, one of them nil
-- => Output: 3
