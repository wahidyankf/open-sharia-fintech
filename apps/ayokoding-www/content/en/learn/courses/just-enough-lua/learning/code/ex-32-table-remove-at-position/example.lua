-- Example 32: table.remove -- remove at a specific position
local t = { 1, 2, 3 } -- => t is {1, 2, 3}
table.remove(t, 1) -- => removes the element at position 1; later elements shift left
print(t[1], t[2]) -- => what was t[2]/t[3] are now t[1]/t[2] -- Output: 2    3
