vim.pack.add({ "https://github.com/neovim/nvim-lspconfig" })
function MyStatusFn()
	local clients = vim.lsp.get_clients({ bufnr = 0 })
	if #clients == 0 then
		return ""
	end
	return clients[1].name
end
vim.o.statusline = "%f %{v:lua.MyStatusFn()}"
vim.lsp.enable("lua_ls")
