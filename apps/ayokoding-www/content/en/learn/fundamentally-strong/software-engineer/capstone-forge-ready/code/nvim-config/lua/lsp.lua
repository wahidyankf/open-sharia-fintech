-- lua/lsp.lua -- diagnostics rendering + LspAttach buffer-local keymap (co-05, co-12, co-14)
vim.diagnostic.config({
	virtual_text = true, -- => inline error/warning text right on the offending line
	signs = true, -- => gutter signs, independent of virtual_text
	underline = true, -- => underlines the exact span the diagnostic covers
	severity_sort = true, -- => an error visually outranks a warning on the same line
})

vim.api.nvim_create_autocmd("LspAttach", { -- => co-05: an autocommand reacting to a
	group = vim.api.nvim_create_augroup("CapstoneLspAttach", { clear = true }), --    live editor event
	callback = function(args)
		-- co-12: LspAttach is the idiomatic place for buffer-local LSP keymaps -- scoped so hover only
		-- exists in buffers where a server actually attached, never globally
		vim.keymap.set("n", "K", vim.lsp.buf.hover, { buffer = args.buf, desc = "LSP hover" })
		-- co-13: 'gra' (code action) and 'grr' (references) are already default-bound the instant any
		-- server attaches (Neovim 0.11+) -- no hand-binding needed here for either one
	end,
})
