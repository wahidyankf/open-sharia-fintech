vim.o.wrap = false -- baseline: wrap off everywhere by default
vim.api.nvim_create_autocmd("FileType", {
	pattern = "markdown",
	callback = function()
		vim.opt_local.wrap = true
	end,
})
