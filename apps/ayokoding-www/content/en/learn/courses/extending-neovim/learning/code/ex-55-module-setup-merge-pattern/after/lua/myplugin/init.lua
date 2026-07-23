local M = {}
local defaults = { greeting = "Hello", width = 80 }
M.options = {}
function M.setup(opts)
	M.options = vim.tbl_deep_extend("force", defaults, opts or {})
end
return M
