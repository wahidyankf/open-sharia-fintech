-- Example 75: a memoized closure -- fibonacci with a cache upvalue
local function makeFib()
	local cache = {} -- => cache is an upvalue shared by every recursive call below
	local fib -- => forward-declare fib so the closure can call itself by that name
	fib = function(n) -- => the memoized recursive worker
		if n < 2 then
			return n
		end -- => base cases: fib(0) is 0, fib(1) is 1
		if cache[n] then
			return cache[n]
		end -- => already computed -- skip the recursive work entirely
		local result = fib(n - 1) + fib(n - 2) -- => the two recursive calls this cache exists to avoid repeating
		cache[n] = result -- => store this result in the shared cache before returning
		return result -- => hand the value back to the caller
	end -- => closes fib
	return fib -- => exposes only the memoized function
end -- => closes makeFib
local fib = makeFib() -- => fib is now a closure sharing one private cache
print(fib(30)) -- => without memoization this branches exponentially; with it, it's instant
-- => Output: 832040
