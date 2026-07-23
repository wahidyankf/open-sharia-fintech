vim.api.nvim_create_autocmd("CursorHold", {
	callback = function()
		vim.diagnostic.open_float()
	end,
})
