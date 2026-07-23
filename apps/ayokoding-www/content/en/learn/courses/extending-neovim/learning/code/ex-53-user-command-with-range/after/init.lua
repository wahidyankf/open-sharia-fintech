vim.api.nvim_create_user_command("Upper", function(o)
	vim.cmd(string.format("%d,%dnormal! guu", o.line1, o.line2))
	vim.cmd(string.format("%d,%dnormal! VU", o.line1, o.line2))
end, { range = true })
