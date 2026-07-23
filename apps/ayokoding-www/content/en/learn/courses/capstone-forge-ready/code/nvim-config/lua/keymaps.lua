-- lua/keymaps.lua -- core key mappings (co-04)
-- vim.g.mapleader is already set by lua/options.lua, required one line before this module in init.lua
vim.keymap.set("n", "<leader>w", ":w<CR>", { desc = "Save file" })
vim.keymap.set("n", "<leader>q", ":q<CR>", { desc = "Quit window" })
vim.keymap.set({ "n", "v" }, "<leader>y", '"+y', { desc = "Yank to system clipboard" })
