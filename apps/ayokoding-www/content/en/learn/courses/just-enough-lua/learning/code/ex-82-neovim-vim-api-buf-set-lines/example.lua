-- Example 82: vim.api.nvim_buf_set_lines / get_lines -- editing a buffer from Lua
-- Run inside Neovim: :luafile example.lua
vim.api.nvim_buf_set_lines(0, 0, -1, false, { "hello", "world" })
-- => buffer 0 is "the current buffer"; 0, -1 means "the whole buffer"
-- => start/end lines are 0-BASED and end-EXCLUSIVE, unlike Lua's own tables
print(table.concat(vim.api.nvim_buf_get_lines(0, 0, -1, false), "|"))
-- => reads the whole buffer back as a list of lines, joined with "|"
-- => Output: hello|world
