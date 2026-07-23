local mod1 = require("config.scratch")
print("first require:", mod1.value)

-- simulate a live edit to the module's own file, on disk, while Neovim is still running
local target = vim.fn.stdpath("config") .. "/lua/config/scratch.lua"
vim.fn.writefile({ "return { value = 2 }" }, target)

-- FIX: clear the cache entry first, so the next require() genuinely re-reads and re-runs
-- the file from disk instead of returning the stale cached table
package.loaded["config.scratch"] = nil
local mod2 = require("config.scratch")
print("second require (cache cleared first):", mod2.value)
