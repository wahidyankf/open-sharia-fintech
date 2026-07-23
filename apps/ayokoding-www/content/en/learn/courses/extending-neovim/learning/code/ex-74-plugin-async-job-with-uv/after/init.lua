vim.api.nvim_create_user_command("RunFormat", function()
	local buf = vim.api.nvim_create_buf(false, true)
	local out = {}
	local stdout = vim.uv.new_pipe(false)
	vim.uv.spawn("echo", {
		args = { "formatted-output" },
		stdio = { nil, stdout, nil },
	}, function(code)
		vim.schedule(function()
			vim.api.nvim_buf_set_lines(buf, 0, -1, false, out)
			vim.g.run_format_done = true
			vim.g.run_format_code = code
		end)
	end)
	stdout:read_start(function(err, data)
		if data then
			table.insert(out, data)
		end
	end)
end, {})
