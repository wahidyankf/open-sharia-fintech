-- Example 31: table.remove -- remove the last element
local t = { 1, 2, 3 } -- => t is {1, 2, 3}
local v = table.remove(t) -- => with 1 argument, table.remove removes and returns the LAST element
print(v, #t) -- => v is the removed value (3); #t shrinks from 3 to 2 -- Output: 3    2
