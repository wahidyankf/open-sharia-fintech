if vim.g.loaded_myplugin then
	return
end
vim.g.loaded_myplugin = true
require("myplugin").setup()
