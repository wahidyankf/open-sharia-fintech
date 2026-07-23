local function setup()
	-- BUG: no augroup at all -- nothing clears prior entries before this one registers
	vim.api.nvim_create_autocmd("BufWritePre", { pattern = "*", command = 'echo "saving"' })
end

setup()
