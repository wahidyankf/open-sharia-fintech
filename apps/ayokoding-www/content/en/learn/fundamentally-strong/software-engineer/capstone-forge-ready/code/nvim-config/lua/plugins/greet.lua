-- lua/plugins/greet.lua -- a self-authored plugin module, packaged the same way any third-party
-- plugin is (co-18): a require()-able module exposing M.setup(opts)
local M = {}

function M.setup()
	-- co-06: nvim_create_user_command -- a custom Ex command, tab-completable like any built-in one
	vim.api.nvim_create_user_command("Greet", function(cmd_opts)
		local who = cmd_opts.args ~= "" and cmd_opts.args or "World"
		print("Hello, " .. who .. "!")
	end, { nargs = "?", desc = "Greet someone (default: World)" })

	-- co-05: a second autocommand, this one owned by the plugin module itself, not the top-level config
	vim.api.nvim_create_autocmd("BufWritePost", {
		group = vim.api.nvim_create_augroup("GreetOnSave", { clear = true }),
		pattern = "*.py",
		callback = function(args)
			print("Greet: saved " .. vim.fn.fnamemodify(args.file, ":t"))
		end,
	})
end

return M
