local group = vim.api.nvim_create_augroup("Idempotent", { clear = true })
vim.api.nvim_create_autocmd("BufWritePre", { group = group, pattern = "*", command = 'echo "pre-write"' })
vim.api.nvim_create_autocmd("BufWritePost", { group = group, pattern = "*", command = 'echo "post-write"' })
