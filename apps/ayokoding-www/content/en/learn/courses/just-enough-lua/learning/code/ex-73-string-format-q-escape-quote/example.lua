-- Example 73: string.format %q -- a Lua-reader-safe escaped literal
print(string.format("%q", 'He said "hi"'))
-- => %q escapes quotes/backslashes so the Lua reader could reload it verbatim
-- => Output: "He said \"hi\""
