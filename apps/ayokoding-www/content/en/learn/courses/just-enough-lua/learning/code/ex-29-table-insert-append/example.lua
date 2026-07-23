-- Example 29: table.insert -- append to the end
local t = { 1, 2 } -- => t is {1, 2}
table.insert(t, 3) -- => with 2 arguments, table.insert appends to the end (position #t + 1)
print(t[3]) -- => Output: 3
