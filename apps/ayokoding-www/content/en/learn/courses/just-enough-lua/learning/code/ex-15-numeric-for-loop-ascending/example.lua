-- Example 15: numeric for-loop, ascending
for i = 1, 5 do -- => start=1, stop=5, implicit step=1
	io.write(i, " ") -- => io.write adds no newline or separator, unlike print
end -- => loop runs for i = 1, 2, 3, 4, 5 inclusive of both ends
print() -- => flushes a trailing newline so shell output looks clean
-- => Output: 1 2 3 4 5  (trailing space before the newline)
