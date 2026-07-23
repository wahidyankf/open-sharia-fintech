-- Example 79: vim.tbl_map -- transforming every element of a table
-- Run inside Neovim: :luafile example.lua
print(vim.inspect(vim.tbl_map(function(x)
	return x * 2
end, { 1, 2, 3 })))
-- => tbl_map applies the function to each value, returning a NEW table
-- => Output: { 2, 4, 6 }
