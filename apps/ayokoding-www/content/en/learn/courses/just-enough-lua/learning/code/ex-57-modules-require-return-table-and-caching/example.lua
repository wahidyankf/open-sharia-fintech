-- Example 57: modules -- require() returns and caches the module's table
local m1 = require("mymodule") -- => runs mymodule.lua and caches its RETURN VALUE in package.loaded
local m2 = require("mymodule") -- => does NOT re-run the file; returns the SAME cached table
print(m1.greet(), m1 == m2) -- => m1.greet() calls the function stored in the module's table: "hi"
-- => m1 == m2 is true because both are the identical cached table
-- => Output: hi    true
