local mod1 = require("config.scratch")
print("first require:", mod1.value)

-- simulate a live edit to the module's own file, on disk, while Neovim is still running
local target = vim.fn.stdpath("config") .. "/lua/config/scratch.lua"
vim.fn.writefile({ "return { value = 2 }" }, target)

-- BUG: require() alone never re-reads an already-loaded module -- package.loaded still
-- holds the cached table from the FIRST call, so this returns the exact same object
local mod2 = require("config.scratch")
print("second require (no cache clear):", mod2.value)
