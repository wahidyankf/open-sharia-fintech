-- Example 4: local vs global shadowing
x = 10 -- => no `local` keyword, so x is a GLOBAL variable
do -- => opens a new block
	local x = 20 -- => declares a NEW local x, shadowing the global inside this block
	print(x) -- => reads the local x -- Output line 1: 20
end -- => the local x goes out of scope here
print(x) -- => reads the global x again, unaffected -- Output line 2: 10
