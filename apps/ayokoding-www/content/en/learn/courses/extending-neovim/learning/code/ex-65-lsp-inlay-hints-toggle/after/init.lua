vim.pack.add({ "https://github.com/neovim/nvim-lspconfig" })
vim.api.nvim_create_autocmd("LspAttach", {
	callback = function(args)
		vim.lsp.inlay_hint.enable(true, { bufnr = args.buf })
	end,
})
vim.lsp.enable("lua_ls")
