-- Example 71: coroutine.status -- the suspended/running/dead lifecycle
local co -- => forward-declare co so the closure below captures the LOCAL, not a global
co = coroutine.create(function()
	print(coroutine.status(co)) -- => queried from INSIDE the coroutine while it is executing
end) -- => closes the coroutine body
print(coroutine.status(co)) -- => a freshly created coroutine starts "suspended" -- Output line 1: suspended
coroutine.resume(co) -- => runs the body; the print inside reports "running" -- Output line 2: running
print(coroutine.status(co)) -- => the function has returned, so the coroutine is now "dead"
-- => Output line 3: dead
