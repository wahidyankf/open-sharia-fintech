vim.lsp.config("lua_ls", { cmd = { "lua-language-server" }, filetypes = { "lua" }, root_markers = { ".git" } })
vim.lsp.enable("lua_ls")

-- FIX: bind inside LspAttach with buffer = args.buf -- K only exists in buffers where a
-- server actually attached, exactly like every other filetype/buffer-local keymap in this topic
vim.api.nvim_create_autocmd("LspAttach", {
	callback = function(args)
		vim.keymap.set("n", "K", vim.lsp.buf.hover, { buffer = args.buf, desc = "LSP hover" })
	end,
})
