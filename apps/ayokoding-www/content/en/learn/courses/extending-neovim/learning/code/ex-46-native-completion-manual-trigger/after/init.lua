vim.pack.add({ "https://github.com/neovim/nvim-lspconfig" })
vim.lsp.enable("lua_ls")
vim.keymap.set("i", "<C-space>", vim.lsp.completion.get)
