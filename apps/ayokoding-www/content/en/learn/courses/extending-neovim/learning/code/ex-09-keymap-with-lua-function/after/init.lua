vim.g.mapleader = " "
vim.keymap.set("n", "<leader>q", function()
	vim.cmd("q")
end, { silent = true })
