local M = {}

-- FIX: registration lives INSIDE M.setup() -- it only runs once a caller explicitly opts in
function M.setup(opts)
	vim.api.nvim_create_user_command("MyPluginCmd", function()
		print("ran")
	end, {})
end

return M
