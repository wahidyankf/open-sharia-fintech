vim.pack.add({ "https://github.com/neovim/nvim-lspconfig" })
vim.api.nvim_create_autocmd("BufWritePre", {
	callback = function()
		if #vim.lsp.get_clients({ bufnr = 0 }) > 0 then
			vim.lsp.buf.format({ async = false })
		end
	end,
})
vim.lsp.enable("lua_ls")
