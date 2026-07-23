-- Example 39: string.sub -- negative index, called with colon syntax
print(("hello"):sub(-3)) -- => colon-call sugar for string.sub("hello", -3); -3 counts from the end
-- => Output: llo
