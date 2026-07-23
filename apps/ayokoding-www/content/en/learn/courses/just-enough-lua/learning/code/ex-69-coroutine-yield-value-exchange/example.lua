-- Example 69: coroutines -- exchanging values through yield/resume
local co = coroutine.create(function(x) -- => x is the first resume's extra argument
	local y = coroutine.yield(x * 2) -- => yield's argument becomes resume's extra return value
	return y + 100 -- => resume's extra argument becomes yield's return value
end) -- => closes the coroutine body
local ok1, val1 = coroutine.resume(co, 5) -- => x is 5; yields x*2 = 10 back to the caller
print(ok1, val1) -- => Output: true    10
local ok2, val2 = coroutine.resume(co, 7) -- => 7 becomes y inside the coroutine; returns y+100 = 107
print(ok2, val2) -- => Output: true    107
