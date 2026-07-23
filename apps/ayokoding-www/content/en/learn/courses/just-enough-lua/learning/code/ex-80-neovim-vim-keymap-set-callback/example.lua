-- Example 80: vim.keymap.set -- a Normal-mode mapping with a Lua callback
-- Run inside Neovim: :luafile example.lua, then press <leader>x to trigger it
vim.keymap.set("n", "<leader>x", function()
	print("mapped") -- => runs when <leader>x is pressed in Normal mode
end, { desc = "test" }) -- => desc documents the mapping for :Telescope keymaps / which-key style tools
-- => Output (after pressing <leader>x): mapped
