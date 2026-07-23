-- FIX: vim.diagnostic.setloclist() is the dedicated function for this -- it targets the
-- current window's location list directly, with no manual toqflist()/setqflist() plumbing
vim.keymap.set("n", "<leader>xl", vim.diagnostic.setloclist, { desc = "Diagnostics to loclist" })
