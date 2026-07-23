-- Example 35: table.sort -- custom comparator function
local t = { 3, 1, 2 } -- => t is {3, 1, 2}, unsorted
table.sort(t, function(a, b)
	return a > b
end)
-- => passing a function as the second argument overrides the default order
-- => `a > b` sorts descending instead of ascending
print(table.concat(t, ",")) -- => Output: 3,2,1
