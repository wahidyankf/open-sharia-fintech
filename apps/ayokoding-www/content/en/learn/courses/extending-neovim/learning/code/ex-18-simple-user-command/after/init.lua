vim.api.nvim_create_user_command("Reload", function()
	vim.cmd("source $MYVIMRC")
end, {})
