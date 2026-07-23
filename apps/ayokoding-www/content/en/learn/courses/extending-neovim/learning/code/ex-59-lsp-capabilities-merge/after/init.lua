vim.pack.add({ "https://github.com/neovim/nvim-lspconfig" })
local caps = vim.lsp.protocol.make_client_capabilities()
caps.textDocument.completion.completionItem.snippetSupport = true
vim.lsp.config("*", { capabilities = caps })
vim.lsp.enable({ "lua_ls", "pyright" })
