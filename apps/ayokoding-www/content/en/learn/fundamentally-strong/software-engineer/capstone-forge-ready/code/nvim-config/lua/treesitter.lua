-- lua/treesitter.lua -- Treesitter highlighting + text-objects for Python (co-16, co-17)
require("nvim-treesitter").setup() -- => the active fork's own setup call, installed by init.lua's vim.pack.add

vim.api.nvim_create_autocmd("FileType", { -- => co-05: reacts to the FileType event
	pattern = "python",
	callback = function()
		vim.treesitter.start(0, "python")
		-- => co-16: Python is NOT one of Neovim's six bundled parsers (c, lua, markdown, markdown_inline,
		--    vim, vimdoc), so no ftplugin/python.lua calls this automatically -- this autocmd is what a
		--    config author adds once the parser itself is installed (:TSInstall python, run once manually)
	end,
})
-- co-17: once the parser is running, the built-in an/in ("a node"/"in node") object-select operators
-- and ]n/[n sibling navigation work immediately -- no further config needed for text-objects
