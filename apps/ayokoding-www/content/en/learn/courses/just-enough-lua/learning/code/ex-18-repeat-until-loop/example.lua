-- Example 18: repeat/until loop
local n = 0 -- => n starts at 0
repeat -- => the body always runs at least once
	n = n + 1 -- => n becomes 1, then 2, then 3
until n >= 3 -- => condition checked AFTER each iteration, unlike while
print(n) -- => Output: 3
