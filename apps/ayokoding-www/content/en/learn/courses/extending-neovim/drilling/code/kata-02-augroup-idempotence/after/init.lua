local function setup()
	-- FIX: an augroup with { clear = true } wipes this group's prior entries before re-adding them
	local group = vim.api.nvim_create_augroup("MyConfig", { clear = true })
	vim.api.nvim_create_autocmd("BufWritePre", { group = group, pattern = "*", command = 'echo "saving"' })
end

setup()
