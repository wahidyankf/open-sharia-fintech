local function make_counter()
	local n = 0
	return function()
		n = n + 1
		return n
	end
end

local a = make_counter()
local b = make_counter()
print(a(), a(), b(), b())
