-- Example 22: ipairs() iteration over the array part
for i, v in ipairs({ "x", "y", "z" }) do
	-- => ipairs walks contiguous integer keys 1..n in guaranteed ascending order
	print(i, v) -- => i is the index, v is the value at that index
end
-- => Output line 1: 1    x
-- => Output line 2: 2    y
-- => Output line 3: 3    z
