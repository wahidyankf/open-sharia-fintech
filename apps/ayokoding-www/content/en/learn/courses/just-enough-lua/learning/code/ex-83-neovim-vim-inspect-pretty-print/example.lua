-- Example 83: vim.inspect -- human-readable table dumps for debugging
-- Run inside Neovim: :luafile example.lua
print(vim.inspect({ 1, 2, { x = 3 } }))
-- => vim.inspect formats any Lua value as readable, re-parseable Lua syntax
-- => Output (nested table expands across lines): { 1, 2, { x = 3 } }
