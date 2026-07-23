-- Example 21: table nested field access
local t = { a = { b = { c = 42 } } } -- => tables can nest arbitrarily deep: a table holding a table holding a table
print(t.a.b.c) -- => walks the chain: t.a is a table, t.a.b is a table, t.a.b.c is 42
-- => Output: 42
