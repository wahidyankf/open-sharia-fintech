-- Example 5: multiple assignment swap
local a, b = 1, 2 -- => a is 1, b is 2 (parallel assignment, not sequential)
a, b = b, a -- => the right side (2, 1) is fully evaluated before either assignment lands
-- => a becomes 2, b becomes 1 -- no temp variable needed
print(a, b) -- => Output: 2    1
