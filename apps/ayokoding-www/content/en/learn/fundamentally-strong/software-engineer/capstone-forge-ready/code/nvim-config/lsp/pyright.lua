-- lsp/pyright.lua -- auto-discovered by vim.lsp.enable('pyright') purely from its runtimepath location
-- (co-11) -- no vim.lsp.config() call needed anywhere else in this config
return {
	cmd = { "pyright-langserver", "--stdio" },
	filetypes = { "python" },
	root_markers = { "pyproject.toml", "setup.py", ".git" },
}
