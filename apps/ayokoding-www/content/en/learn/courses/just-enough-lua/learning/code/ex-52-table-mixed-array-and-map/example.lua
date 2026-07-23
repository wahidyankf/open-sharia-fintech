-- Example 52: a table mixing array and map entries
local t = { 1, 2, 3, name = "mix" } -- => the array part {1, 2, 3} and hash part {name=...} coexist in ONE table
print(#t, t.name) -- => #t counts only the contiguous integer-keyed part: 3
-- => t.name reads the string-keyed part: "mix"
-- => Output: 3    mix
