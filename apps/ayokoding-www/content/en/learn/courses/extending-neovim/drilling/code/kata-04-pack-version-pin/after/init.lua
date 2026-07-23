-- FIX: a table spec's version field pins the plugin to an exact tag -- vim.pack.get()
-- resolves and reports back the exact commit that tag points to
vim.pack.add({ { src = "https://github.com/sainnhe/gruvbox-material", version = "v1.0.0" } })
