-- Example 45: string.gsub -- substitution with a replacement count
local s, n = string.gsub("hello world", "o", "0")
-- => gsub returns TWO values: the new string, and the substitution count
-- => every "o" is replaced with "0": "hell0 w0rld"
-- => two substitutions were made, so n is 2
print(s, n) -- => Output: hell0 w0rld    2
