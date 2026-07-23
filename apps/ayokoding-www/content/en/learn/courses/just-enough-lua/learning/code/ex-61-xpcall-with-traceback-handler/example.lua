-- Example 61: xpcall() with a traceback handler
local ok, tb = xpcall(function()
	error("oops") -- => raises an error inside the protected function
end, debug.traceback) -- => the SECOND argument is a handler, called WHILE the stack is still live
print(ok) -- => ok is false, same as pcall would report -- Output: false
print(string.find(tb, "stack traceback") ~= nil)
-- => debug.traceback() built a full call-stack string; it contains this phrase
-- => Output: true
