vim.g.mapleader = " " -- must run BEFORE any keymap that references <leader>
vim.keymap.set("n", "<leader>w", ":w<CR>", { desc = "Save file" })
