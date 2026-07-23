-- BUG: intends to send diagnostics to the WINDOW-scoped location list, but calls
-- vim.fn.setqflist(), which always targets the single GLOBAL quickfix list instead
vim.keymap.set("n", "<leader>xl", function()
	local diags = vim.diagnostic.get(0)
	local items = vim.diagnostic.toqflist(diags)
	vim.fn.setqflist({}, " ", { title = "Diagnostics", items = items })
	vim.cmd("copen")
end, { desc = "Diagnostics to loclist" })
