-- Example 11: logical `or` as a default-value idiom
local x = nil -- => x is nil (Lua has no separate "undefined")
print(x or "default") -- => `or` returns its first truthy operand
-- => x is falsy (nil), so the expression evaluates to "default"
-- => Output: default
