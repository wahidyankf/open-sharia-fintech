-- Example 44: string.gmatch -- iterate over every match
for word in string.gmatch("one two three", "%a+") do
	-- => gmatch returns an iterator over every non-overlapping match
	-- => %a+ matches one-or-more letters, so it yields each word in turn
	io.write(word, "|") -- => writes each word followed by a literal pipe, no newline
end
print() -- => trailing newline for clean output
-- => Output: one|two|three|
