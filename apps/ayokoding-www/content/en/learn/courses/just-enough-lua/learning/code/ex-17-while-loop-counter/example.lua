-- Example 17: while-loop counter
local n = 0 -- => n starts at 0
while n < 3 do -- => condition checked BEFORE each iteration
	n = n + 1 -- => body runs while the condition holds: n becomes 1, then 2, then 3
end -- => loop exits once n < 3 is false (n is 3)
print(n) -- => Output: 3
