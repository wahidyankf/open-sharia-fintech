local function fib_gen()
	return coroutine.wrap(function()
		local a, b = 0, 1
		while true do
			coroutine.yield(a)
			a, b = b, a + b
		end
	end)
end

local gen = fib_gen()
print(gen(), gen(), gen(), gen(), gen(), gen())
