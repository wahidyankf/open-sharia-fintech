vim.pack.add({ "https://github.com/neovim/nvim-lspconfig" })
vim.lsp.config("*", { root_markers = { ".git" } })
vim.lsp.enable("lua_ls")
