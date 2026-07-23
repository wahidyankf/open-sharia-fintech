vim.api.nvim_create_user_command("Greet", function(o)
	print("Hello " .. o.args)
end, { nargs = 1 })
