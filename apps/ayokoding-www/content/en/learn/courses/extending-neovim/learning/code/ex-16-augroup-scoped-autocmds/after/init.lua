local group = vim.api.nvim_create_augroup("MyConfig", { clear = true })
vim.api.nvim_create_autocmd("BufWritePre", {
	group = group,
	pattern = "*",
	command = 'echo "saving"',
})
vim.api.nvim_create_autocmd("BufReadPost", {
	group = group,
	pattern = "*",
	command = 'echo "reading"',
})
