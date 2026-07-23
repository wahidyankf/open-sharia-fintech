-- Example 78: vim.tbl_deep_extend -- recursively merging config tables
-- Run inside Neovim: :luafile example.lua  (vim.* only exists inside Neovim's Lua runtime)
print(vim.inspect(vim.tbl_deep_extend("force", { a = 1, b = { c = 2 } }, { b = { c = 3 } })))
-- => "force" behavior merges recursively: b.c is overridden to 3, a=1 survives
-- => Output: { a = 1, b = { c = 3 } }  (vim.inspect pretty-prints across lines)
