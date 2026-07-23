local M = {}

function M.new()
	return { items = {} }
end

function M.push(q, value)
	table.insert(q.items, value)
end

function M.pop(q)
	return table.remove(q.items)
end

return M
