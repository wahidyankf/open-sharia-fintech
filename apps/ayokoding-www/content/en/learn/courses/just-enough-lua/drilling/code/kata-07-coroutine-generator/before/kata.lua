local function fib_gen()
	return coroutine.wrap(function()
		local a, b = 0, 1
		coroutine.yield(a)
	end)
end

local gen = fib_gen()
print(gen())
print(gen())
print(gen())
