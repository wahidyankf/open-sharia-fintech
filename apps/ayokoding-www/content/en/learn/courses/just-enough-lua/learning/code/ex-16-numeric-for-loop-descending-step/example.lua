-- Example 16: numeric for-loop, descending with an explicit step
for i = 10, 1, -2 do -- => start=10, stop=1, step=-2 (step must be explicit to go backward)
	io.write(i, " ") -- => writes each value with a trailing space, no newline
end -- => loop runs for i = 10, 8, 6, 4, 2 (stops before going below 1)
print() -- => trailing newline for clean output
-- => Output: 10 8 6 4 2  (trailing space before the newline)
