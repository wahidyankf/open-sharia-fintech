-- Example 19: table array literal and the length operator
local t = { 10, 20, 30 } -- => a table literal with contiguous integer keys 1, 2, 3
print(t[1], t[3], #t) -- => t[1]/t[3] are 1-indexed elements; #t is the "sequence length"
-- => Output: 10    30    3
