-- FIX: read the bundled query's own source text first (co-17's query.get_files), then
-- APPEND the custom pattern to it before calling query.set() -- this keeps every original
-- capture and adds one more, instead of throwing the rest away
local files = vim.treesitter.query.get_files("lua", "highlights")
local original = table.concat(vim.fn.readfile(files[1]), "\n")
vim.treesitter.query.set("lua", "highlights", original .. "\n(identifier) @custom_ident")
