vim.pack.add({ "https://github.com/neovim/nvim-lspconfig" })
vim.lsp.config("extra_lua_checker", {
	cmd = { "lua-language-server" },
	filetypes = { "lua" },
})
vim.lsp.enable({ "lua_ls", "extra_lua_checker" })
