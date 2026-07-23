-- init.lua -- Extending Neovim capstone: complete config entry point (co-01)
-- Reproducible from an empty ~/.config/nvim: copy this whole after/ tree into
-- $XDG_CONFIG_HOME/nvim (default ~/.config/nvim) and restart Neovim.

vim.pack.add({ -- => vim.pack (co-08): Neovim's built-in, Git-backed plugin manager --
	--    zero external bootstrap script needed, unlike lazy.nvim (co-09)
	{
		src = "https://github.com/neovim/nvim-lspconfig",
		version = "v2.10.0", -- => pinned tag (not a moving branch) -- same revision every machine
	},
	{
		src = "https://github.com/neovim-treesitter/nvim-treesitter",
		-- => the ACTIVE community fork -- the original nvim-treesitter/
		--    nvim-treesitter has been archived and frozen since 2026-04-03
		version = "df7489eeea351bece7fd0f9c825be5cb6a1438f0",
		-- => pinned commit hash: the fork ships no version tags yet
	},
	{
		src = "https://github.com/neovim-treesitter/treesitter-parser-registry",
		-- => required companion repo the fork's own plugin/ file checks for
		version = "6eb15358bb9fc88f0d3401d8538d56652e9bdf3c",
	},
})

require("options") -- => lua/options.lua (co-02, co-03) -- editor-wide settings
require("keymaps") -- => lua/keymaps.lua (co-04) -- leader + core mappings
require("lsp") -- => lua/lsp.lua (co-05, co-12, co-14) -- diagnostics + LspAttach
require("treesitter") -- => lua/treesitter.lua (co-16, co-17) -- Python highlight/text-objects
require("plugins.greet").setup() -- => lua/plugins/greet.lua (co-06, co-18) -- self-authored plugin

vim.lsp.enable("pyright") -- => co-10, co-11: lsp/pyright.lua on the runtimepath supplies its config
