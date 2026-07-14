-- lua/options.lua -- editor-wide settings (co-02, co-03)
vim.g.mapleader = " " -- => must be set BEFORE any keymap that references <leader> (co-03)

vim.o.number = true -- => absolute number on the cursor's own line
vim.o.relativenumber = true -- => every other visible line shows distance-from-cursor
vim.o.expandtab = true -- => <Tab> inserts spaces, not a literal tab character
vim.o.shiftwidth = 2 -- => >>/<< and auto-indent step by 2 spaces
vim.o.tabstop = 2 -- => a literal tab character (if any survive) renders as 2 columns
vim.o.ignorecase = true -- => searches match regardless of case by default
vim.o.smartcase = true -- => ...unless the search pattern itself contains an uppercase letter
vim.o.termguicolors = true -- => true-color rendering instead of a 256-color-degraded palette
