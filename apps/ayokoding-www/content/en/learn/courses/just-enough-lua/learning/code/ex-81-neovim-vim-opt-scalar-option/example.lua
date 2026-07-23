-- Example 81: vim.opt / vim.o -- setting and reading a scalar option
-- Run inside Neovim: :luafile example.lua
vim.opt.tabstop = 2 -- => vim.opt is the structured, Lua-friendly way to set any 'option
print(vim.o.tabstop) -- => vim.o is the plain scalar-value view of the same options
-- => Output: 2
