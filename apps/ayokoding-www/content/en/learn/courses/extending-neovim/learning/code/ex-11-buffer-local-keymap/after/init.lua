vim.api.nvim_create_autocmd("FileType", {
	pattern = "help",
	callback = function(args)
		vim.keymap.set("n", "q", "<cmd>close<CR>", { buffer = args.buf, desc = "Close help window" })
	end,
})
