local M = {}
local count = 0
function M.increment()
	count = count + 1
	return count
end
return M
