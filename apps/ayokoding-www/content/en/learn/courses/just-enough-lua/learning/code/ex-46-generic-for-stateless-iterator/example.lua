-- Example 46: generic for-loop with a custom stateless iterator
local function range(n) -- => returns an (iterator-function, state, control-variable) triplet
	local function iter(_, i) -- => the iterator itself: takes (state, control), returns the next value
		i = i + 1 -- => advances the control variable by one
		if i <= n then
			return i
		end -- => returns nil (implicitly) once past n, ending the loop
	end -- => closes iter
	return iter, nil, 0 -- => no shared state needed; control starts at 0
end -- => closes range
for i in range(3) do -- => `for` calls iter(state, control) repeatedly until it returns nil
	print(i) -- => no closure involved -- range()'s state lives in the returned triplet
end -- => closes the for-loop
-- => Output line 1: 1
-- => Output line 2: 2
-- => Output line 3: 3
