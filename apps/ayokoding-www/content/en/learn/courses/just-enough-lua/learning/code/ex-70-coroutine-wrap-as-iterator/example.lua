-- Example 70: coroutine.wrap -- using a coroutine as a for-loop iterator
local gen = coroutine.wrap(function() -- => wrap returns a plain FUNCTION, not a coroutine handle
	for i = 1, 3 do -- => walks 1, 2, 3
		coroutine.yield(i) -- => each call to gen() resumes up to the next yield
	end -- => closes the for-loop
end) -- => closes the wrapped function
for v in gen do
	io.write(v, " ")
end -- => a generic for-loop calls gen() repeatedly until it returns nothing
print() -- => trailing newline for clean output
-- => Output: 1 2 3  (trailing space before the newline)
