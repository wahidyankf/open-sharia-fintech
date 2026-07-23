-- init.lua -- Pass-0 capstone forge: complete config entry point
-- Reproducible from an empty ~/.config/nvim: copy this whole nvim-config/ tree into
-- $XDG_CONFIG_HOME/nvim (default ~/.config/nvim) and restart Neovim.
-- Reuses the same pinned plugins, require order, and vim.lsp.enable call as
-- topic-03 (Extending Neovim)'s capstone config; comments rewritten for this page.

vim.pack.add({ -- vim.pack: Neovim's built-in, Git-backed plugin manager
	{
		src = "https://github.com/neovim/nvim-lspconfig",
		version = "v2.10.0", -- pinned tag
	},
	{
		src = "https://github.com/neovim-treesitter/nvim-treesitter",
		version = "df7489eeea351bece7fd0f9c825be5cb6a1438f0", -- pinned commit (active fork ships no tags)
	},
	{
		src = "https://github.com/neovim-treesitter/treesitter-parser-registry",
		version = "6eb15358bb9fc88f0d3401d8538d56652e9bdf3c", -- required companion repo
	},
})

require("options")
require("keymaps")
require("lsp")
require("treesitter")
require("plugins.greet").setup()

vim.lsp.enable("pyright")
