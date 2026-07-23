local M = {}
function M.check()
	vim.health.start("myplugin")
	if vim.fn.executable("git") == 1 then
		vim.health.ok("git is executable")
	else
		vim.health.error("git not found on PATH")
	end
end
return M
