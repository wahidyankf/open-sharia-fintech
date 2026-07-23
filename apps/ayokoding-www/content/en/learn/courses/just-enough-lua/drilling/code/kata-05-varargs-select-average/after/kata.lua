local function average(...)
	local n = select("#", ...)
	local sum = 0
	for i = 1, n do
		local v = select(i, ...)
		sum = sum + (v or 0)
	end
	return sum / n
end

print(average(4, 8, nil))
