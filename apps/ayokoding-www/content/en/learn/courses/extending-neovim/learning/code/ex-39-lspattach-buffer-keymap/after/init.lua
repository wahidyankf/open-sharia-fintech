vim.pack.add({ "https://github.com/neovim/nvim-lspconfig" })
vim.api.nvim_create_autocmd("LspAttach", {
	callback = function(args)
		vim.keymap.set("n", "K", vim.lsp.buf.hover, { buffer = args.buf, desc = "LSP hover" })
	end,
})
vim.lsp.enable("lua_ls")
