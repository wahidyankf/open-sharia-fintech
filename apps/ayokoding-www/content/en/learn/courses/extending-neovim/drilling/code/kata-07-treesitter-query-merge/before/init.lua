-- BUG: intends to ADD one custom highlight capture on top of Lua's bundled highlights, but
-- query.set() REPLACES the compiled query outright rather than merging into it -- every
-- other capture (keywords, strings, comments, numbers, ...) silently disappears
vim.treesitter.query.set("lua", "highlights", "(identifier) @custom_ident")
