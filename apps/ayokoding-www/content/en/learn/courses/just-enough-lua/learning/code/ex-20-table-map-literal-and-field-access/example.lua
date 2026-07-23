-- Example 20: table map literal and field access
local t = { name = "Ada", age = 36 } -- => a table literal with string keys, like a record
print(t.name, t["age"]) -- => t.name is sugar for t["name"]: "Ada"
-- => t["age"] is the explicit bracket form: 36
-- => Output: Ada    36
