vim.pack.add({ "https://github.com/neovim/nvim-lspconfig" })
vim.lsp.handlers["textDocument/references"] = function(err, result, ctx, config)
	if not result or vim.tbl_isempty(result) then
		return
	end
	local client = vim.lsp.get_client_by_id(ctx.client_id)
	local items = vim.lsp.util.locations_to_items(result, client.offset_encoding)
	vim.fn.setqflist({}, " ", { title = "References", items = items })
	vim.cmd("copen")
end
vim.lsp.enable("lua_ls")
