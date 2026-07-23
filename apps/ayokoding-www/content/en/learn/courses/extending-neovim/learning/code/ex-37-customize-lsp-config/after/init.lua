vim.pack.add({ "https://github.com/neovim/nvim-lspconfig" })
vim.lsp.config("lua_ls", {
	settings = { Lua = { diagnostics = { globals = { "MY_CUSTOM_GLOBAL" } } } },
})
vim.lsp.enable("lua_ls")
