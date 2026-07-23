-- Example 30: table.insert -- insert at a specific position
local t = { 1, 2, 3 } -- => t is {1, 2, 3}
table.insert(t, 1, 0) -- => with 3 arguments, table.insert(t, pos, value) inserts at pos
-- => existing elements at pos 1+ shift right by one
print(t[1], t[2], t[3], t[4]) -- => Output: 0    1    2    3
