-- Example 34: table.sort -- default ascending order
local t = { 3, 1, 2 } -- => t is {3, 1, 2}, unsorted
table.sort(t) -- => sorts IN PLACE using the default `<` comparison
print(table.concat(t, ",")) -- => Output: 1,2,3
