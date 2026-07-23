vim.pack.add({ "https://github.com/neovim/nvim-lspconfig" })
vim.keymap.set("n", "<leader>ws", vim.lsp.buf.workspace_symbol, { desc = "Workspace symbols" })
vim.lsp.enable("lua_ls")
