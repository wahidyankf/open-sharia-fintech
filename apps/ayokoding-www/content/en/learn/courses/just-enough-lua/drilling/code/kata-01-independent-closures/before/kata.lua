local function make_counter_pair()
	n = 0
	local function counter()
		n = n + 1
		return n
	end
	return counter, counter
end

local a, b = make_counter_pair()
print(a(), a(), b(), b())
