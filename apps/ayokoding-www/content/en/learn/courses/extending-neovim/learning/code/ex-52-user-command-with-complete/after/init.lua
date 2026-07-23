vim.api.nvim_create_user_command("SetColor", function(o)
	vim.cmd.colorscheme(o.args)
end, { nargs = 1, complete = "color" })
