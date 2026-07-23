vim.pack.add({
	"https://github.com/neovim-treesitter/nvim-treesitter",
	"https://github.com/neovim-treesitter/treesitter-parser-registry",
})
require("nvim-treesitter").setup()
vim.api.nvim_create_autocmd("FileType", {
	pattern = "python",
	callback = function()
		vim.treesitter.start(0, "python")
	end,
})
