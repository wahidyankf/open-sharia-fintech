vim.lsp.config("lua_ls", { cmd = { "lua-language-server" }, filetypes = { "lua" }, root_markers = { ".git" } })
vim.lsp.enable("lua_ls")

-- BUG: bound at the TOP LEVEL, unconditionally -- this overrides built-in K (keywordprg lookup)
-- in EVERY buffer, including ones where lua_ls never attaches at all
vim.keymap.set("n", "K", vim.lsp.buf.hover, { desc = "LSP hover" })
