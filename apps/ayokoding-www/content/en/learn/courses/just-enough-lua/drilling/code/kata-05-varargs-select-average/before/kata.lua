local function average(...)
	local args = { ... }
	local sum = 0
	for i = 1, #args do
		sum = sum + (args[i] or 0)
	end
	return sum / #args
end

print(average(4, 8, nil))
