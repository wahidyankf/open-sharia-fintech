-- Example 7: math library floor and huge
print(math.floor(3.7), math.huge > 1e300)
-- => math.floor(3.7) rounds down to 3; math.huge > 1e300 is true (infinity)
-- => Output: 3    true
