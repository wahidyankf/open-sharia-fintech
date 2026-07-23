-- Example 68: coroutine.create and coroutine.resume
local co = coroutine.create(function() -- => wraps a function as a suspendable coroutine
	print("a") -- => runs during the FIRST resume
	coroutine.yield() -- => pauses execution here, handing control back to the caller
	print("b") -- => runs during the SECOND resume, continuing right after yield
end) -- => closes the coroutine body
coroutine.resume(co) -- => starts the coroutine; prints "a" then pauses -- Output line 1: a
coroutine.resume(co) -- => resumes right where it paused; prints "b" then finishes
-- => Output line 2: b
