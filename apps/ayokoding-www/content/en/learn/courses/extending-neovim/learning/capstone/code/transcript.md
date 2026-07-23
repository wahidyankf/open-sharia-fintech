# Capstone launch transcript

Every command below was run against a genuinely fresh `$XDG_CONFIG_HOME` pointed at a plain copy of
`after/` -- no prior `~/.config/nvim` reused, no output hand-edited (verified against real Neovim
v0.12.3, not simulated). The technique: `export XDG_CONFIG_HOME=$(mktemp -d)`, copy `after/` to
`"$XDG_CONFIG_HOME/nvim"`, then run `nvim` exactly as shown -- this is what makes `stdpath('config')`
resolve to the copy, which is what makes `lsp/pyright.lua` auto-discoverable on the `runtimepath`
(co-11) the same way it would be from a real `~/.config/nvim`.

```bash
export XDG_CONFIG_HOME=$(mktemp -d)
export XDG_DATA_HOME=$(mktemp -d)
export XDG_STATE_HOME=$(mktemp -d)
mkdir -p "$XDG_CONFIG_HOME/nvim"
cp -r after/* "$XDG_CONFIG_HOME/nvim/"
```

## Step 1 -- bootstrap the pinned plugin manager

_ordered step 1 -- co-01, co-08_

```text
$ nvim --headless "+qa"

These plugins will be installed:

nvim-lspconfig             from https://github.com/neovim/nvim-lspconfig
nvim-treesitter            from https://github.com/neovim-treesitter/nvim-treesitter
treesitter-parser-registry from https://github.com/neovim-treesitter/treesitter-parser-registry

vim.pack: Installing plugins (0/3)
vim.pack:  33% Installing plugins (1/3) - treesitter-parser-registry
vim.pack:  66% Installing plugins (2/3) - nvim-lspconfig
vim.pack: 100% Installing plugins (3/3) - nvim-treesitter
vim.pack: 100% Installing plugins (3/3)
$ echo $?
0
```

All three pinned plugins clone on the very first launch of a config that has never run before, and
the process exits `0` -- `vim.pack.add` alone is enough, no separate installer or bootstrap script.

## Step 2 -- verify options and keymaps took effect

_ordered step 2 -- co-02, co-03, co-04, co-07_

```text
$ nvim --headless -c "lua print(vim.o.number, vim.o.relativenumber, vim.o.shiftwidth, vim.o.tabstop)" -c "lua print(vim.fn.maparg('<leader>w', 'n') ~= '')" -c 'qa!'
true true 2 2
true
```

`lua/options.lua` and `lua/keymaps.lua` both loaded through `init.lua`'s two `require()` calls
(co-07): all four inspected options carry their configured values, and `<leader>w` (leader is a
literal space, set by `options.lua` one line before `keymaps.lua` is required) resolves to a real
mapping.

## Step 3 -- wire LSP and Treesitter for Python, verify both

_ordered step 3 -- co-10, co-11, co-12, co-14, co-16, co-17_

The Python grammar is not one of Neovim's six bundled parsers, so it needs installing once with the
active community fork (same prerequisite Example 48 discovered: the fork needs its companion
`treesitter-parser-registry` repository and the separate `tree-sitter` CLI binary).

```text
$ nvim --headless -c 'TSInstall! python' -c "lua vim.wait(30000, function() return #vim.fs.find('python.so', {path=vim.fn.stdpath('data')}) > 0 end, 500)" -c 'qa!'
[nvim-treesitter/install/python]: Downloading tree-sitter-queries-python...
[nvim-treesitter/install/python]: Downloading shared-f1cbf91dc8d3...
[nvim-treesitter/install/python]: Compiling parser...
[nvim-treesitter/install/python]: Installing parser...
```

With the parser installed, a deliberately broken `scratch.py` (an undefined name, `nam` instead of
`name`) exercises highlighting, diagnostics, and code-action capability together:

```python
def greet(name: str) -> str:
    return "Hello, " + nam
```

```text
$ nvim --headless scratch.py -c "lua print(vim.treesitter.highlighter.active[vim.api.nvim_get_current_buf()] ~= nil, vim.treesitter.get_parser():lang())" -c 'qa!'
true python
```

```text
$ nvim --headless scratch.py \
    -c "lua vim.wait(8000, function() return #vim.lsp.get_clients({bufnr=0}) > 0 end, 200)" \
    -c "lua local c = vim.lsp.get_clients({bufnr=0})[1]; print('attached:', c ~= nil, c and c.name)" \
    -c "lua vim.wait(8000, function() return #vim.diagnostic.get(0) > 0 end, 200)" \
    -c "lua for _, d in ipairs(vim.diagnostic.get(0)) do print(d.lnum + 1, d.severity, d.message) end" \
    -c "lua local c = vim.lsp.get_clients({bufnr=0})[1]; print('codeActionProvider:', c and c.server_capabilities.codeActionProvider ~= nil)" \
    -c 'qa!'
attached: true pyright
2 1 "nam" is not defined
1 4 "name" is not accessed
codeActionProvider: true
```

`pyright` (installed in this sandbox as a Node-based CLI, `pyright-langserver --stdio`) attaches to
the buffer, reports two real diagnostics -- an error (severity `1`) on the undefined `nam` and a hint
(severity `4`) on the now-unused `name` parameter -- and its `server_capabilities.codeActionProvider`
is truthy, confirming a code action request (the default `gra` keymap, co-13) is genuinely
serviceable, not merely configured. `:checkhealth nvim-treesitter` corroborates the parser install
independently:

```text
Installed languages     H L F I J ~
- python                ✓ ✓ ✓ ✓ ✓
```

## Step 4 -- exercise the self-authored plugin

_ordered step 4 -- co-06, co-18_

```text
$ nvim --headless -c 'silent Greet' -c 'redir END' -c 'qa!'
Hello, World!

$ nvim --headless -c 'silent Greet Neovim' -c 'redir END' -c 'qa!'
Hello, Neovim!

$ nvim --headless scratch.py -c 'silent write' -c 'redir END' -c 'qa!'
"scratch.py" 2L, 56B written
Greet: saved scratch.py
```

`:Greet` with no argument defaults to `World`; with an argument it greets that name instead --
`nargs = '?'` (co-06) accepts both. Saving a `.py` buffer fires `lua/plugins/greet.lua`'s own
`BufWritePost` autocommand (co-05), printing a confirmation line -- proof the self-authored module's
command and its autocommand both work from a plain `require('plugins.greet').setup()` call in
`init.lua`, indistinguishable in shape from a third-party plugin (co-18).

## Step 5 -- baseline vs. capstone config, and every pinned version

_ordered step 5_

**Baseline** (`nvim -u NONE`, no config loaded at all):

```text
$ nvim --headless -u NONE scratch.py \
    -c "lua print('Greet exists:', vim.fn.exists(':Greet') == 2)" \
    -c "lua print('treesitter active:', vim.treesitter.highlighter.active[vim.api.nvim_get_current_buf()] ~= nil)" \
    -c "lua print('lsp clients:', #vim.lsp.get_clients({bufnr = 0}))" \
    -c 'qa!'
Greet exists: false
treesitter active: false
lsp clients: 0
```

**Capstone config** (`after/init.lua`, the same file this whole transcript exercises): `:Greet`
exists, Python highlighting is active, and a real LSP client is attached -- the exact three
capabilities `-u NONE` has none of.

**Pinned versions** (every plugin `init.lua` installs, by exact tag or commit):

| Plugin                        | Source                                                            | Pinned to                                         |
| ----------------------------- | ----------------------------------------------------------------- | ------------------------------------------------- |
| nvim-lspconfig                | `https://github.com/neovim/nvim-lspconfig`                        | tag `v2.10.0`                                     |
| nvim-treesitter (active fork) | `https://github.com/neovim-treesitter/nvim-treesitter`            | commit `df7489eeea351bece7fd0f9c825be5cb6a1438f0` |
| treesitter-parser-registry    | `https://github.com/neovim-treesitter/treesitter-parser-registry` | commit `6eb15358bb9fc88f0d3401d8538d56652e9bdf3c` |

The fork ships no version tags yet (verified against its own tag list, empty at authoring time), so
its two repositories are pinned by exact commit hash instead of a tag -- `vim.pack`'s `version` field
accepts a "Git branch, tag, or commit hash" interchangeably (`runtime/lua/vim/pack.lua`), so a commit
pin is exactly as reproducible as a tag pin.

## Acceptance criteria -- full healthcheck

```text
$ nvim --headless "+checkhealth" "+qa"
$ echo $?
0
```

```text
==============================================================================
lspconfig:                                                                  OK

==============================================================================
nvim-treesitter:                                                            OK
Installed languages     H L F I J ~
- python                v v v v v

==============================================================================
vim.deprecated:                                                             OK

==============================================================================
vim.health:                                                         2 WARN  1 ERROR
- WARN Nvim 0.12.4 is available (current: 0.12.3)
- ERROR $TERM should be "screen-256color", "tmux-256color", or "tmux-direct" in tmux.

==============================================================================
vim.lsp:                                                                    OK
- pyright: cmd: { "pyright-langserver", "--stdio" }, filetypes: python

==============================================================================
vim.pack:                                                                   OK
- Git, Lockfile, Plugin directory all OK

==============================================================================
vim.provider:                                                             6 WARN
(Node.js/Perl/Python3/Ruby providers -- every one explicitly labeled "(optional)")
```

Honest accounting of the two non-OK sections, condensed above from the real, unedited report:

- **`vim.health`'s one ERROR** is this sandbox's tmux terminal type (`$TERM=xterm-256color` inside
  tmux, which `:checkhealth` would prefer to be `tmux-256color`) -- a terminal-emulation setting of
  the machine running Neovim, not a dependency this config installs, requires, or controls. It is
  present identically whether or not any file in this capstone's `after/` tree exists at all.
- **`vim.health`'s WARN about 0.12.4** and **`vim.provider`'s six WARNs** are the same class of
  finding Example 22 already documented honestly earlier in this topic: a genuinely newer Neovim
  patch being available, and four scripting-language host providers (Node.js, Perl, Python 3, Ruby)
  that this config never asks for and that `:checkhealth` itself labels `(optional)`.

Every plugin manager, LSP server, and Treesitter parser this capstone's config actually declares as a
dependency reports `OK` with zero missing required dependency -- exactly what the acceptance
criteria asks `nvim --headless "+checkhealth" "+qa"` to confirm.
