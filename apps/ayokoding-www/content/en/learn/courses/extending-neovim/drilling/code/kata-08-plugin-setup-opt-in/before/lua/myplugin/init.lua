local M = {}

-- BUG: registers the command at FILE (module) SCOPE -- it runs the instant this module is
-- require()-d, not inside M.setup() where a caller has actually opted in
vim.api.nvim_create_user_command("MyPluginCmd", function()
	print("ran")
end, {})

function M.setup(opts) end

return M
