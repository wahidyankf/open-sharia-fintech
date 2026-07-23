-- Example 77: packing varargs directly into a table constructor
local function collect(...)
	return { ... } -- => {...} packs every argument into a fresh array-part table
end -- => closes the function
local t = collect(1, 2, 3) -- => t is {1, 2, 3}
print(#t, t[1], t[3]) -- => #t is 3 (three contiguous entries); t[1] and t[3] are the ends
-- => Output: 3    1    3
