vim.api.nvim_create_autocmd("BufWritePre", {
	pattern = "*.lua",
	command = [[%s/\s\+$//e]],
})
