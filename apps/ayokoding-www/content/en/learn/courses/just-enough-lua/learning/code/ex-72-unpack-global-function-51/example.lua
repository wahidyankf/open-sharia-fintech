-- Example 72: the Lua 5.1 global unpack() -- Neovim's embedded dialect
-- NOTE: run this one with `luajit example.lua`, not `lua example.lua` --
-- LuaJIT targets Lua 5.1 semantics, where unpack() is a GLOBAL function.
-- Standalone Lua 5.5 removed the global; only table.unpack() exists there (5.2+).
print(unpack({ 1, 2, 3 })) -- => unpack() expands a table's array part back into separate values
-- => Output (under luajit): 1    2    3
