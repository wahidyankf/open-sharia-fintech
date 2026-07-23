local M = {}
function M.setup(opts)
	vim.api.nvim_create_user_command("MyPluginCmd", function()
		print("ran")
	end, {})
end
return M
