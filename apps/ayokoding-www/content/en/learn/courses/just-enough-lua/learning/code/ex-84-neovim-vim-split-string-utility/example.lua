-- Example 84: vim.split -- splitting a string on a separator
-- Run inside Neovim: :luafile example.lua
print(vim.inspect(vim.split("a,b,,c", ",")))
-- => trimempty defaults to FALSE, so the empty field between "b" and "c" stays
-- => Output: { "a", "b", "", "c" }
