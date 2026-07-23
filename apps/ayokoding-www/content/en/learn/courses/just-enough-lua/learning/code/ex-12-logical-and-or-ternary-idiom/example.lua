-- Example 12: `and`/`or` as a ternary-operator idiom
local ok = true -- => ok is true
print(ok and "yes" or "no") -- => `and` short-circuits: if ok is truthy, evaluate the right side ("yes")
-- => the whole `A and B or C` then evaluates to B when A is truthy
-- => Output: yes
