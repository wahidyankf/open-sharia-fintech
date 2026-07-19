# 3 · Extending Neovim (By Example, Lua †)

**prd row**: Pass 0 · Editor Foundations · By Example · Lua † · Learn 103 / Drill 203 · Nvim-ready Yes ·
VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: turn vanilla Neovim ([topic 1](./01-just-enough-nvim.md)) into a real IDE-grade forge
using the Lua learned in [topic 2](./02-just-enough-lua.md) — plugin management, LSP, Treesitter,
autocommands/user commands, and a tiny self-authored plugin. This is the payoff topic of Pass 0; every
later topic assumes this forge exists (DD-17). Neovim and every plugin/LSP used are OSS (Tier-1, DD-21).

## Why this exists · the big idea

- **The problem before the solution**: vanilla Neovim edits text; real work also needs diagnostics,
  syntax-awareness, and a config you can reproduce on a new machine — this topic turns the editor into a
  versioned **forge** every later topic assumes (DD-17).
- **Keep-this-if-you-forget-everything**: your editor is code — the config is a Lua program in git, so your
  environment is reproducible and diffable, not a pile of clicked settings.
- **Big ideas touched**: `mechanism-vs-policy` — you now add the **policy** (plugins, LSP, keymaps) onto
  vanilla Neovim's **mechanism**; `abstraction-and-its-cost` — LSP and Treesitter are language-agnostic
  abstractions that buy uniform tooling across languages.

## Prerequisites

- **Prior topics**: [topic 1 Just Enough Nvim](./01-just-enough-nvim.md) (modal editing fluency) and
  [topic 2 Just Enough Lua](./02-just-enough-lua.md) (config is written in Lua).
- **Tools & environment**: a macOS/Linux terminal; the latest **Neovim** (`nvim --version`); **git** (to
  clone/manage the config and plugins); network access to fetch plugins; a working
  `~/.config/nvim` location. A language runtime for the LSP demo (Python 3.x) installed.
- **Assumed knowledge**: reading/writing basic Lua tables and functions (from topic 02); using the
  terminal and git.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28). **Two fast-moving items below —
> re-check immediately before authoring.**

- 2026-07-12 — verified: current stable Neovim **v0.12.4** (2026-07-05). The recommended LSP path is now
  **native `vim.lsp.config('name', {...})` + `vim.lsp.enable('name')`** (Neovim 0.11+); `nvim-lspconfig`'s
  role has shifted to supplying `lsp/*.lua` config files consumed via `vim.lsp.enable()` (requires
  0.11.3+). **Teach the native API as primary**, not the legacy `require('lspconfig').xyz.setup()`.
  (github.com neovim/nvim-lspconfig)
- 2026-07-12 — verified (CORRECTION, time-sensitive): Neovim 0.12 ships a **built-in native plugin
  manager `vim.pack`** (zero external dep; installs into the `packpath` **opt** side —
  `site/pack/core/opt` — and `:packadd`s each plugin programmatically, never using a `start/` dir) — name
  it as the raw-form-aligned
  default alongside lazy.nvim (still valid for richer lazy-loading). **`nvim-treesitter` was archived
  2026-04-03**: old `master` is frozen (0.11 compat only); a `main`-branch rewrite requires Nvim 0.12+ and
  its successor/maintenance status is fluid — **re-verify the correct plugin/version to pin at authoring**.
  (github.com nvim-treesitter discussions; echasnovski.com)
- 2026-07-12 — verified: `nvim_create_autocmd(event, opts)` + `nvim_create_user_command(name, command,
opts)` (and `vim.opt`/`vim.g`/`vim.keymap.set`) signatures are current. (neovim.io API docs)
- 2026-07-12 — verified: XDG layout — `$XDG_CONFIG_HOME/nvim/init.lua` (default `~/.config/nvim`), `lua/`
  on `runtimepath`; inspect via `stdpath('config')`. (neovim.io / archwiki)
- 2026-07-14 — re-confirmed at authoring time (Phase 3 V step, `web-researcher`): v0.12.4 (2026-07-05) is
  still current stable (github.com/neovim/neovim/releases); the native `vim.lsp.config()` +
  `vim.lsp.enable()` description and nvim-lspconfig's "0.11.3+" requirement re-confirmed verbatim against
  its README — no change. **Correction**: `nvim-treesitter/nvim-treesitter` is confirmed still archived
  (frozen 2026-04-03, zero commits since, per the GitHub API). Core Neovim's own `treesitter.txt` still
  names that archived repo as the reference installer and ships no built-in `:TSInstall`. A community fork,
  `neovim-treesitter/nvim-treesitter` (created 2026-04-06, 141 stars, last push 2026-06-22), is active and
  ships `:TSInstall`; ecosystem is fragmented with no consolidated winner (see
  github.com/neovim/neovim/discussions/38848) — ex-48 should cite this fork by name rather than an abstract
  "successor." **Correction**: `nvim_create_user_command`'s signature is upgraded from
  `[Needs Verification]` to `[Verified]`, fetched directly at the `v0.12.4` tag
  (`src/nvim/api/command.c`) — `bang` is not a distinctly-documented `opts` field like `nargs`/`range`/
  `count`/`complete`; it is one of the generic boolean `|command-attributes|` (alongside `bar`). The Lua
  callback table's full field set is `args`, `bang`, `count`, `fargs`, `line1`, `line2`, `mods`, `name`,
  `nargs`, `range`, `reg`, `smods` — richer than previously documented. **Correction**: Microsoft's LSP
  spec site now labels **3.18 "Current"** (3.17 demoted to "Previous"), though 3.18 itself still
  self-describes as "under development"; Neovim's own `lsp.txt` does not pin a spec version number — it
  links to whichever spec Microsoft currently marks "current," so citing "3.17" as Neovim's target is
  illustrative, not a settled fact confirmed by a Neovim primary source.
- 2026-07-14 — new finding surfaced at authoring time (Phase 4 V step, `web-researcher`,
  `capstone-forge-ready`): re-running `:checkhealth` against the pinned `nvim-lspconfig` **v2.10.0** shows
  it now marks its own `:checkhealth lspconfig` integration **deprecated**, pointing users instead at
  `:checkhealth vim.lsp` (the plugin itself still functions; only its healthcheck hook is being retired).
  Independently reproduced against the pinned tag; no impact on the native `vim.lsp.config()` /
  `vim.lsp.enable()` guidance already recorded above.

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to a primary source fetched and read in the retroactive grounding sweep
> (2026-07-12, `web-researcher`). Sources: Neovim `runtime/doc/*.txt` + `runtime/lua/vim/*.lua` on
> `github.com/neovim/neovim` (authoritative `:help`), plugin project docs, LSP spec. Fast-moving —
> re-verify plugin/version pins at authoring.

- **Version + native LSP path (co-10/11/13)** — Neovim **v0.12.4** (2026-07-05,
  [Releases](https://github.com/neovim/neovim/releases)); `nvim-lspconfig`
  [README](https://github.com/neovim/nvim-lspconfig): "Use `vim.lsp.enable('…')` (not
  `require'lspconfig'.….setup{}`)", requires 0.11.3+, community-maintained. Default global LSP keymaps
  (`grn`/`gra`/`grr`/`gri`/`grt`/`gO`/`grx`/`K`) verbatim from
  [`lsp.txt`](https://raw.githubusercontent.com/neovim/neovim/master/runtime/doc/lsp.txt).
- **`vim.pack` (co-08, ex-28..31)** —
  [`runtime/lua/vim/pack.lua`](https://raw.githubusercontent.com/neovim/neovim/master/runtime/lua/vim/pack.lua):
  installs to `site/pack/core/opt` (opt side only, `:packadd`s programmatically — never a `start/` dir);
  JSON `packlockfile`; `add`/`get`/`update`/`del` confirmed. Accuracy-note phrasing corrected accordingly.
- **`nvim-treesitter` archival (co-16, ex-47/48)** — repo banner verbatim: "archived by the owner on
  Apr 3, 2026 … read-only"; `master` frozen (0.11 compat), `main` rewrite needs 0.12+. **Re-confirmed
  2026-07-14**: still archived (zero commits since), core Neovim's `treesitter.txt` still names it as the
  reference installer with no built-in `:TSInstall`; the active community fork
  [`neovim-treesitter/nvim-treesitter`](https://github.com/neovim-treesitter/nvim-treesitter) (created
  2026-04-06, 141 stars, last push 2026-06-22) ships `:TSInstall` and is what ex-48 should cite by name —
  ecosystem remains fragmented, no consolidated winner
  ([neovim/neovim#38848](https://github.com/neovim/neovim/discussions/38848)). Bundled parsers
  (C/Lua/Markdown/Vimscript/Vimdoc) + auto-`vim.treesitter.start()` per
  [`treesitter.txt`](https://raw.githubusercontent.com/neovim/neovim/master/runtime/doc/treesitter.txt) —
  supports ex-47's zero-plugin `.lua` highlight claim.
- **Autocommands, user commands, keymaps (co-04/05/06)** —
  [`api.txt`](https://raw.githubusercontent.com/neovim/neovim/master/runtime/doc/api.txt) +
  [`keymap.lua`](https://raw.githubusercontent.com/neovim/neovim/master/runtime/lua/vim/keymap.lua):
  `nvim_create_autocmd`/`nvim_create_augroup({clear})`, `keymap.set(modes,lhs,rhs,opts)`/`keymap.del`
  confirmed. `nvim_create_user_command` signature **[Verified] 2026-07-14** against
  [`src/nvim/api/command.c` at the `v0.12.4` tag](https://raw.githubusercontent.com/neovim/neovim/v0.12.4/src/nvim/api/command.c):
  `opts` fields are `nargs`/`range`/`count`/`complete`/`desc`/`force`/`preview`/`addr` plus boolean
  `|command-attributes|` such as `bang`/`bar` (`bang` is not a distinctly-documented `opts` key, unlike
  the syllabus's prior shorthand); the Lua callback table's full field set is `args`, `bang`, `count`,
  `fargs`, `line1`, `line2`, `mods`, `name`, `nargs`, `range`, `reg`, `smods`.
- **Options, diagnostics, Treesitter API, LSP surfaces** — `vim.o`/`vim.opt`/`vim.g`/`vim.bo`/`vim.wo`
  ([`lua.txt`](https://raw.githubusercontent.com/neovim/neovim/master/runtime/doc/lua.txt));
  `vim.diagnostic.config`/`setloclist` defaults
  ([`diagnostic.txt`](https://raw.githubusercontent.com/neovim/neovim/master/runtime/doc/diagnostic.txt));
  `vim.treesitter.start`/`query.parse`/`foldexpr`, default `an`/`in`/`]n`/`[n` selectors;
  `vim.lsp.buf.format({async})`, `get_clients`, `inlay_hint.enable` (`@since 12`), `completion.enable
({autotrigger})`, `vim.lsp.config('*', …)` wildcard — all confirmed.
- **Deprecations corrected** —
  [`deprecated.txt`](https://raw.githubusercontent.com/neovim/neovim/master/runtime/doc/deprecated.txt):
  `vim.lsp.stop_client()` → `Client:stop()` (ex-62 fixed); `vim.lsp.codelens.refresh()` →
  `vim.lsp.codelens.enable(true)` (ex-63 fixed).
- **`vim.uv`/fast-event, `vim.hl.on_yank` (ex-74/75/15)** — `vim.uv.spawn(program,opts,on_exit)`;
  `vim.api` calls illegal in `vim.uv` callbacks → `vim.schedule()` fix; `vim.hl.on_yank` is a `hl_op()`
  alias on 0.13+, `on_yank` on 0.12.x (secondary-corroborated, matches file's parenthetical).
- **Read more** — LSP spec version **re-checked 2026-07-14**: Microsoft's spec site now labels **3.18
  "Current"** (3.17 demoted to "Previous"), while 3.18 itself still self-describes as "under development";
  Neovim's own `lsp.txt` does not pin a spec version number — it links to whichever spec Microsoft
  currently marks "current." Citing "3.17" below is illustrative (matches the version community sources
  associate with Neovim 0.12's LSP client), not a settled fact confirmed by a Neovim primary source.
  `lazy.nvim` spec fields (`event`/`cmd`/`ft`/`keys`/`opts`/`config`) verbatim from
  [lazy.folke.io/spec](https://lazy.folke.io/spec); nvim-lspconfig attribution corrected from "core team"
  to community-maintained.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (subject topic). Each example below cites the co-NN it exercises. Web-verified against Neovim v0.12.4 (2026-07-05). -->

- **co-01 · init-lua-entrypoint** — `init.lua` under `stdpath('config')` (`~/.config/nvim/init.lua`) is the
  single Lua entry point Neovim sources at startup, with `lua/` beneath it available to `require()`.
- **co-02 · options-vim-o-vs-opt** — Editor options are set with `vim.o` (direct scalar access) for
  boolean/number/string values and `vim.opt` (Lua-table-like, supports `:append()`/`:remove()`) for
  list/map/set-like values, with `vim.bo`/`vim.wo` scoping to a specific buffer or window.
- **co-03 · global-and-scoped-variables** — `vim.g`, `vim.b`, `vim.w`, and `vim.t` are typed wrappers over
  Vim's global/buffer/window/tab variable scopes (including `vim.g.mapleader`), indexable per-object.
- **co-04 · keymap-set** — `vim.keymap.set(mode, lhs, rhs, opts)` is the standard Lua API for mappings,
  accepting a string or Lua function as `rhs` and an `opts` table (`desc`, `buffer`, `silent`, `expr`,
  `remap`); `vim.keymap.del` removes one.
- **co-05 · autocommands** — `vim.api.nvim_create_autocmd(event, opts)` paired with
  `vim.api.nvim_create_augroup(name, {clear=true})` replaces Vimscript `autocmd`/`augroup` for
  event-driven config, dispatching to a `command` string or Lua `callback`.
- **co-06 · user-commands** — `vim.api.nvim_create_user_command(name, command, opts)` defines custom Ex
  commands with `nargs`, `bang`, `range`, `count`, and `complete`, the callback receiving `fargs`, `args`,
  `bang`, `line1`/`line2`.
- **co-07 · lua-module-system** — Files under `lua/` on the runtimepath become `require()`-able modules
  (subdirectories map to dotted paths, `init.lua` collapses a folder), cached in `package.loaded` until
  explicitly cleared.
- **co-08 · plugin-management-vim-pack** — Neovim 0.12 ships a built-in, Git-backed plugin manager
  (`vim.pack.add/get/update/del`) that installs into `site/pack/core/opt` and tracks state in a JSON
  `packlockfile`.
- **co-09 · plugin-management-lazy-nvim** — `lazy.nvim` remains the dominant third-party plugin manager,
  driven by a declarative plugin-spec table with lazy-loading triggers (`event`, `cmd`, `ft`, `keys`) and
  an `opts`/`config` setup convention.
- **co-10 · native-lsp-config** — Neovim 0.11+ replaced `require('lspconfig').setup{}` with the native
  `vim.lsp.config(name, cfg)` / `vim.lsp.enable(name)` pair, where `vim.lsp.config('*', {...})` sets shared
  defaults inherited by every server.
- **co-11 · lsp-server-configs-and-lspconfig** — `nvim-lspconfig` is now a config-only registry (no longer
  the activation framework) that `vim.lsp.config` auto-discovers and merges with user-authored
  `lsp/<name>.lua` files on the runtimepath.
- **co-12 · lsp-attach-and-keymaps** — The `LspAttach` autocommand is the idiomatic place to set
  buffer-local LSP keymaps and inspect the attaching client, replacing the old `on_attach` callback.
- **co-13 · default-lsp-keymaps** — Neovim 0.11+ ships unconditional global LSP keymaps out of the box
  (`grn` rename, `gra` code action, `grr` references, `gri` implementation, `grt` type definition, `gO`
  document symbols, `K` hover), so hand-binding these is now redundant by default.
- **co-14 · diagnostics-config** — `vim.diagnostic.config(opts, namespace?)` controls how diagnostics
  render (`virtual_text`, `signs`, `underline`, `float`, `severity_sort`) globally or per-namespace.
- **co-15 · native-lsp-completion** — `vim.lsp.completion.enable(true, client_id, bufnr, opts)` wires LSP
  completion into Neovim's built-in insert-mode completion (with `autotrigger` and snippet expansion),
  removing the hard dependency on `nvim-cmp`.
- **co-16 · treesitter-highlighting** — Neovim 0.12+ bundles treesitter parsers and enables syntax
  highlighting by default via `vim.treesitter.start()`; the historic `nvim-treesitter` plugin was archived
  2026-04-03, shifting install/highlight setup toward core APIs and `:TSInstall` for non-bundled languages.
- **co-17 · treesitter-textobjects-and-queries** — The `vim.treesitter.query` API (`parse`, `get`, `set`,
  `iter_captures`) and built-in object-select operators (`an`/`in`, `]n`/`[n`) expose the syntax tree for
  textobjects, incremental selection, and expression-based folding (`vim.treesitter.foldexpr()`).
- **co-18 · writing-a-custom-plugin-module** — A user's own Lua functionality is packaged like any
  third-party plugin: a `require()`-able module exposing `M.setup(opts)`, optional `plugin/*.lua` autoload,
  and `lua/*/health.lua` for `:checkhealth` integration.

## Worked examples

Colocated under `extending-neovim/learning/code/`; each ends with a **complete runnable config listing**
(DD-20) and states the exact launch command + observable result (DD-30). Each cites the `co-NN` it
exercises. Contiguous `ex-01..ex-80`. Neovim and every plugin/LSP used are OSS (Tier-1, DD-21).

### Beginner

- **ex-01 · locate-init-lua** — confirm or create `~/.config/nvim/init.lua` as the config entry point —
  verify `:echo $MYVIMRC` reports that exact path after restart. (co-01)
- **ex-02 · set-boolean-option-vim-o** — add `vim.o.number = true` — verify `:set number?` reports
  `number` after restart. (co-02)
- **ex-03 · set-relativenumber** — add `vim.o.relativenumber = true` — verify line numbers render relative
  to the cursor line. (co-02)
- **ex-04 · set-tab-options** — set `vim.o.expandtab`, `vim.o.shiftwidth = 2`, `vim.o.tabstop = 2` — verify
  pressing `<Tab>` inserts two spaces, not a tab. (co-02)
- **ex-05 · append-list-option-vim-opt** — call `vim.opt.wildignore:append({ "*.pyc", "node_modules" })` —
  verify `:set wildignore?` shows both entries appended. (co-02)
- **ex-06 · ignorecase-smartcase** — set `vim.o.ignorecase` and `vim.o.smartcase` — verify `/Foo` matches
  case-sensitively while `/foo` matches both cases. (co-02)
- **ex-07 · set-mapleader** — set `vim.g.mapleader = " "` before any keymap — verify `:verbose map <space>`
  resolves later `<leader>`-prefixed mappings to space. (co-03)
- **ex-08 · basic-normal-keymap** — `vim.keymap.set('n', '<leader>w', ':w<CR>', { desc = 'Save file' })` —
  verify `<leader>w` saves and `:verbose map <leader>w` shows the `desc`. (co-04)
- **ex-09 · keymap-with-lua-function** — `vim.keymap.set('n', '<leader>q', function() vim.cmd('q') end,
{ silent = true })` — verify `<leader>q` closes the window silently. (co-04)
- **ex-10 · keymap-multiple-modes** — `vim.keymap.set({ 'n', 'v' }, '<leader>y', '"+y', ...)` — verify
  yanking in both normal and visual mode fills the system clipboard. (co-04)
- **ex-11 · buffer-local-keymap** — inside a `FileType` autocmd, `vim.keymap.set('n', 'q', '<cmd>close<CR>',
{ buffer = true })` — verify `q` closes only that filetype's buffers. (co-04, co-05)
- **ex-12 · remove-a-keymap** — call `vim.keymap.del('n', '<leader>w')` — verify `:verbose map <leader>w`
  reports no mapping. (co-04)
- **ex-13 · set-colorscheme** — call `vim.cmd.colorscheme('habamax')` — verify `:colorscheme` echoes
  `habamax` and the editor recolors. (co-02)
- **ex-14 · autocmd-command-string** — `nvim_create_autocmd('BufWritePre', { pattern = '*.lua', command =
[[%s/\s\+$//e]] })` — verify trailing whitespace is stripped when a `.lua` file saves. (co-05)
- **ex-15 · autocmd-yank-highlight** — `nvim_create_autocmd('TextYankPost', { callback = function()
vim.hl.on_yank() end })` — verify yanked text flashes briefly (0.13-dev flags `hl_op()` as successor;
  0.12.x still uses `on_yank`). (co-05)
- **ex-16 · augroup-scoped-autocmds** — `nvim_create_augroup('MyConfig', { clear = true })` + two autocmds
  with `group` — verify `:au MyConfig` lists exactly those two even after re-sourcing. (co-05)
- **ex-17 · filetype-local-option** — `FileType` autocmd for `markdown` setting `vim.opt_local.wrap = true`
  — verify `.md` files wrap while other filetypes do not. (co-05, co-02)
- **ex-18 · simple-user-command** — `nvim_create_user_command('Reload', function() vim.cmd('source
$MYVIMRC') end, {})` — verify `:Reload` re-sources `init.lua` without error. (co-06)
- **ex-19 · user-command-with-arg** — `nvim_create_user_command('Greet', function(o) print('Hello '..o.args)
end, { nargs = 1 })` — verify `:Greet World` prints `Hello World`. (co-06)
- **ex-20 · split-config-into-module** — move option lines into `lua/config/options.lua`, `require` it from
  `init.lua` — verify `:lua =package.loaded['config.options']` is non-nil and options apply. (co-07)
- **ex-21 · reload-a-module** — `:lua package.loaded['config.options']=nil; require('config.options')` after
  editing — verify the edited value takes effect without restart. (co-07)
- **ex-22 · run-checkhealth** — run `:checkhealth` — verify a per-component OK/ERROR/WARNING report
  including base provider checks. (co-01)
- **ex-23 · inspect-a-lua-value** — `:lua print(vim.inspect(vim.opt.shiftwidth:get()))` — verify the
  command line echoes the current `shiftwidth` as a Lua value. (co-02)
- **ex-24 · scoped-variable-independence** — set `vim.g.my_setting=1` and `vim.b.my_setting=2` in one buffer
  — verify `:lua print(vim.g.my_setting, vim.b.my_setting)` shows `1 2`, a second buffer shows `1 nil`.
  (co-03)
- **ex-25 · window-local-option** — set `vim.wo[winid].number = false` for one of two split windows — verify
  one window shows line numbers and the other does not. (co-02)
- **ex-26 · custom-statusline-format** — set `vim.o.statusline = '%f %m %=%l:%c'` — verify the statusline
  updates filename, modified flag, and line:column as the cursor moves. (co-02)
- **ex-27 · termguicolors** — set `vim.o.termguicolors = true` — verify true-color rendering instead of a
  256-color-degraded palette in a truecolor terminal. (co-02)
- **ex-28 · install-plugin-vim-pack-add** — `vim.pack.add({ 'https://github.com/sainnhe/gruvbox-material'
})` then `:colorscheme gruvbox-material` — verify the plugin clones under `site/pack/core/opt/` and
  applies. (co-08)

### Intermediate

- **ex-29 · pack-add-with-version-pin** — `vim.pack.add({ { src = '…/nvim-lspconfig', version = 'v2.0.0' }
})` — verify `vim.pack.get({'nvim-lspconfig'})` reports the `v2.0.0` rev. (co-08)
- **ex-30 · pack-update-plugins** — `:lua vim.pack.update()` — verify a confirmation buffer lists pending
  diffs and accepting updates the `packlockfile`. (co-08)
- **ex-31 · pack-remove-plugin** — `:lua vim.pack.del({'gruvbox-material'})` — verify the plugin directory is
  removed and drops from the lockfile. (co-08)
- **ex-32 · lazy-nvim-bootstrap** — add the `lazy.nvim` clone-if-missing block, then
  `require('lazy').setup('plugins')` — verify `:Lazy` opens the manager UI. (co-09)
- **ex-33 · lazy-plugin-spec-opts** — spec `{ 'nvim-lua/plenary.nvim', opts = {} }` — verify `:Lazy` shows
  it loaded and `require('plenary')` succeeds without manual `setup()`. (co-09)
- **ex-34 · lazy-loading-by-event** — spec with `event = 'InsertEnter'` — verify `:Lazy profile` shows the
  plugin loading only after entering insert mode. (co-09)
- **ex-35 · lazy-loading-by-command** — spec with `cmd = 'Telescope'` — verify the plugin stays unloaded
  until `:Telescope` is first invoked. (co-09)
- **ex-36 · enable-lsp-server** — `vim.lsp.enable('lua_ls')` (configs via nvim-lspconfig) — verify opening a
  `.lua` file attaches `lua_ls`, confirmed by `:lua =vim.lsp.get_clients()`. (co-10, co-11)
- **ex-37 · customize-lsp-config** — `vim.lsp.config('lua_ls', { settings = { Lua = { diagnostics = {
globals = {'vim'} } } } })` before enable — verify the "undefined global `vim`" diagnostic disappears.
  (co-10)
- **ex-38 · lsp-config-from-lsp-directory** — create `~/.config/nvim/lsp/pyright.lua` returning a config,
  then `vim.lsp.enable('pyright')` — verify auto-discovery via `:lua =vim.lsp.config.pyright`. (co-11)
- **ex-39 · lspattach-buffer-keymap** — `LspAttach` autocmd binding `K` to `vim.lsp.buf.hover` with
  `buffer = args.buf` — verify `K` shows hover only in LSP-attached buffers. (co-12)
- **ex-40 · verify-default-lsp-keymap** — with an LSP attached and no custom rename map, press `grn` — verify
  `vim.lsp.buf.rename()`'s prompt appears (0.11+ default). (co-13)
- **ex-41 · diagnostic-virtual-text-off** — `vim.diagnostic.config({ virtual_text = false, signs = true })`
  — verify inline error text disappears while gutter signs remain. (co-14)
- **ex-42 · diagnostic-float-on-cursorhold** — `CursorHold` autocmd calling `vim.diagnostic.open_float()` —
  verify holding on an error line pops a floating diagnostic. (co-14, co-05)
- **ex-43 · diagnostic-severity-sort** — `vim.diagnostic.config({ severity_sort = true })` — verify an error
  takes visual priority over a warning on the same line. (co-14)
- **ex-44 · lsp-format-on-save** — `BufWritePre` autocmd calling `vim.lsp.buf.format({ async = false })` —
  verify saving a misformatted file auto-reformats before the write. (co-12, co-05)
- **ex-45 · native-completion-enable** — inside `LspAttach`, `vim.lsp.completion.enable(true, client.id,
bufnr, { autotrigger = true })` — verify typing `.` opens native completion with no `nvim-cmp`. (co-15)
- **ex-46 · native-completion-manual-trigger** — `vim.keymap.set('i', '<C-space>', vim.lsp.completion.get)`
  — verify Ctrl-Space opens the completion menu. (co-15)
- **ex-47 · confirm-builtin-treesitter-highlight** — open a `.lua` file on 0.12+ with zero plugins — verify
  `:lua =vim.treesitter.highlighter.active[vim.api.nvim_get_current_buf()]` returns non-nil. (co-16)
- **ex-48 · treesitter-install-missing-parser** — install the active community fork
  [`neovim-treesitter/nvim-treesitter`](https://github.com/neovim-treesitter/nvim-treesitter) (the
  original `nvim-treesitter/nvim-treesitter` is archived and frozen since 2026-04-03), then `:TSInstall
<lang>` for a non-bundled language — verify the parser compiles and highlighting activates next open.
  (co-16)
- **ex-49 · treesitter-manual-start** — `vim.treesitter.start(0, 'python')` in a `FileType` autocmd — verify
  highlighting turns on for that buffer. (co-16)
- **ex-50 · treesitter-inspect-parser-lang** — `:lua print(vim.treesitter.get_parser():lang())` — verify the
  command line echoes the active parser language (e.g. `lua`). (co-16)
- **ex-51 · treesitter-node-at-cursor** — `:lua print(vim.treesitter.get_node():type())` — verify it prints
  the syntax node type under the cursor (e.g. `function_call`). (co-17)
- **ex-52 · user-command-with-complete** — `nvim_create_user_command('SetColor', …, { nargs = 1, complete =
'color' })` — verify `:SetColor <Tab>` tab-completes colorscheme names. (co-06)
- **ex-53 · user-command-with-range** — `nvim_create_user_command('Upper', …, { range = true })` uppercasing
  `line1..line2` — verify `:'<,'>Upper` uppercases only the selection. (co-06)
- **ex-54 · module-with-local-state** — `lua/config/scratch.lua` returning a table with an internal counter +
  `increment()` — verify two calls return `1` then `2`, proving module state persists. (co-07)
- **ex-55 · module-setup-merge-pattern** — `M.setup(opts)` running `vim.tbl_deep_extend('force', defaults,
opts or {})` — verify a merged table with untouched defaults + overridden key. (co-07, co-18)
- **ex-56 · opt-local-vs-global** — set `vim.opt_local.spell = true` in one buffer — verify `:set spell?` is
  on there and off in a fresh second buffer. (co-02)
- **ex-57 · keymap-expr-mapping** — `vim.keymap.set('i', '<Tab>', function() return vim.fn.pumvisible()==1
and '<C-n>' or '<Tab>' end, { expr = true })` — verify `<Tab>` cycles the popup or inserts a tab. (co-04)
- **ex-58 · augroup-clear-idempotence** — wrap two autocmds in `augroup(..., { clear = true })`, `:source
$MYVIMRC` thrice — verify `:au` still lists exactly the original entries, not triplicated. (co-05)

### Advanced

- **ex-59 · lsp-capabilities-merge** — `vim.lsp.config('*', { capabilities = tbl_deep_extend(…,
snippetSupport = true) })` — verify every server reports `snippetSupport = true` via
  `server_capabilities`. (co-10)
- **ex-60 · lsp-wildcard-shared-defaults** — `vim.lsp.config('*', { root_markers = {'.git'} })` without a
  per-server marker — verify `:LspInfo` still resolves the root at the nearest `.git`. (co-10)
- **ex-61 · lsp-multiple-clients-one-buffer** — enable two servers whose `filetypes` share one filetype —
  verify `vim.lsp.get_clients({ bufnr = 0 })` lists two distinct clients. (co-11)
- **ex-62 · lsp-stop-and-reattach** — `vim.lsp.get_client_by_id(id):stop()` (the 0.12 idiom;
  `vim.lsp.stop_client` is deprecated) then reopen the buffer — verify `:LspInfo` shows detach then
  reattach. (co-12)
- **ex-63 · lsp-codelens-enable-and-run** — `vim.lsp.codelens.enable(true, { bufnr = 0 })` (the 0.12 idiom
  that supersedes the old `BufEnter`/`CursorHold` → `codelens.refresh` autocmd) + default `grx` run —
  verify lenses render and `grx` executes one. (co-12, co-05)
- **ex-64 · lsp-workspace-symbol-search** — bind a key to `vim.lsp.buf.workspace_symbol()` — verify it opens
  a picker/quickfix of project-wide symbols matching the query. (co-12)
- **ex-65 · lsp-inlay-hints-toggle** — `vim.lsp.inlay_hint.enable(true, { bufnr = 0 })` — verify
  parameter/type inlay hints render inline. (co-12)
- **ex-66 · treesitter-iter-captures** — loop over `query.get('lua','highlights'):iter_captures(root, 0)` —
  verify the loop completes, confirming programmatic capture-stream access. (co-17)
- **ex-67 · treesitter-custom-query-override** — `vim.treesitter.query.set('lua', 'highlights', custom)` —
  verify highlighting changes to reflect the override after reopen. (co-17)
- **ex-68 · treesitter-select-parent-node** — cursor in a nested expression, visual mode, press `an` — verify
  the selection expands to exactly the enclosing syntax node. (co-17)
- **ex-69 · treesitter-sibling-navigation** — press `]n` inside a function body — verify the cursor jumps to
  the next sibling node (LSP-selection fallback if no parser). (co-17)
- **ex-70 · treesitter-fold-expr** — `foldmethod=expr`, `foldexpr='v:lua.vim.treesitter.foldexpr()'` — verify
  `zc` folds exactly a function body by syntax tree, not indentation. (co-17)
- **ex-71 · plugin-health-check** — `lua/myplugin/health.lua` exposing `M.check()` with
  `vim.health.ok/error` — verify `:checkhealth myplugin` runs and reports pass/fail. (co-18)
- **ex-72 · plugin-command-registered-in-setup** — register a user command inside `M.setup()`, not at file
  scope — verify `:MyPluginCmd` does not exist until `require('myplugin').setup()` runs. (co-18, co-06)
- **ex-73 · plugin-autoload-via-plugin-dir** — `plugin/myplugin.lua` guarded by a loaded flag calling
  `require('myplugin')` — verify commands are available at startup with no explicit `require` in `init.lua`.
  (co-18)
- **ex-74 · plugin-async-job-with-uv** — `vim.uv.spawn(...)` in a command running a formatter async — verify
  the editor stays responsive and output lands in a scratch buffer on exit. (co-18)
- **ex-75 · plugin-schedule-safety** — wrap `vim.notify` in `vim.schedule(...)` inside a fast-event callback
  — verify it succeeds wrapped and raises "must not be called in a fast event context" unwrapped. (co-18)
- **ex-76 · custom-statusline-lua-component** — embed `%{v:lua.MyStatusFn()}` reading
  `vim.lsp.get_clients()` — verify the statusline shows the attached server name once a client attaches.
  (co-18, co-02)
- **ex-77 · distribute-own-plugin-via-pack** — `vim.pack.add({ { src = '…/you/myplugin', version = 'main' }
})` at your own repo — verify the module becomes `require`-able and its `plugin/` file auto-runs. (co-18,
  co-08)
- **ex-78 · lsp-handler-override-to-quickfix** — override `textDocument/references` handler to
  `setqflist`+`copen` — verify `grr` opens results in the quickfix list, not the location list. (co-10,
  co-14)
- **ex-79 · diagnostic-setloclist** — bind a key to `vim.diagnostic.setloclist()` — verify it opens the
  location list populated with every buffer diagnostic. (co-14)
- **ex-80 · full-config-healthcheck** — after assembling LSP + treesitter + a plugin manager, run
  `:checkhealth all` — verify OK for providers, LSP, and the plugin manager with no unresolved ERROR.
  (co-18)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a complete, from-scratch Neovim configuration repository that turns vanilla Neovim into
  an IDE-grade editor for one language (Python, to dovetail with Pass 1), wiring a plugin manager, LSP,
  Treesitter, autocommands, and one self-authored plugin — reproducible from an empty `~/.config/nvim`.
- **Concepts exercised**: [ ] `init.lua` + `lua/` module tree [ ] plugin manager bootstrap [ ] LSP
  attach + diagnostics + code action [ ] Treesitter highlight/text-objects [ ] an autocommand [ ] a
  `nvim_create_user_command` [ ] a self-authored Lua plugin on `runtimepath`.
- **Ordered steps**:
  1. `extending-neovim/learning/capstone/code/nvim/init.lua` — bootstrap the pinned plugin manager;
     verify `nvim --headless "+qa"` exits 0 with the plugin manager installed.
  2. Add `lua/options.lua` + `lua/keymaps.lua`, `require`d from `init.lua`. Verify `:lua print(vim.o.…)`
     reflects the set options.
  3. Wire LSP + Treesitter for Python (pinned, CVE-clean versions). Verify opening a `.py` file shows
     diagnostics and `:Inspect`/`:checkhealth` reports the server attached and parser installed.
  4. `lua/plugins/greet.lua` — a self-authored module registering a `:Greet` user command + a
     `BufWritePost` autocommand. Verify `:Greet` runs and the autocommand fires on save.
  5. Document the full launch (`nvim -u NONE` baseline vs the capstone config) and pin every version.
- **Acceptance criteria**: from an empty config dir, following the listings yields a working IDE-grade
  Neovim: LSP diagnostics on a Python file, Treesitter highlighting, and the `:Greet` command all
  function; `nvim --headless "+checkhealth" "+qa"` reports no missing required dependency.
- **Done bar**: runnable end-to-end + web-verified.

## Capstone spec — inter-topic: `capstone-forge-ready` (Pass-0 boundary)

Anchored here (weight 135, section-root folder `capstone-forge-ready/` with colocated `code/`).
Integrates topics 01–03: vanilla editing fluency + Lua + a real extended config.

- **Goal**: stand up a complete, reproducible personal development **forge** from an empty machine
  profile — a versioned Neovim config repo the reader can `git clone` and use to edit, navigate, search,
  and run code with LSP + Treesitter — and prove editing fluency by driving a scripted refactor in it
  with no mouse/arrow keys.
- **Concepts exercised**: [ ] raw-form editing (01) [ ] Lua modules/closures/metatables (02) [ ] plugin
  manager + LSP + Treesitter + user command + autocommand (03) [ ] a reproducible config repo layout
  [ ] the `:terminal` build/run loop (DD-17).
- **Ordered steps**:
  1. `capstone-forge-ready/code/nvim-config/` — a self-contained config repo (init.lua + `lua/` tree +
     pinned plugin lockfile). Verify a clean `XDG_CONFIG_HOME=$(mktemp -d) nvim --headless
"+checkhealth" "+qa"` bootstraps and reports healthy.
  2. `capstone-forge-ready/code/sample-project/` — a small Python project. Open it in the forge; verify
     LSP diagnostics + Treesitter highlighting appear.
  3. Drive a scripted, mouse-free refactor across the sample project using motions + macros + quickfix
     (reusing the topic-01 workflow), recording the transcript. Verify the refactor lands identically
     from the transcript.
  4. Run the sample project's check from `:terminal` beside the source. Verify it passes.
- **Acceptance criteria**: a reader on a clean machine reproduces the forge from the repo, opens the
  sample project with working LSP+Treesitter, and replays the refactor transcript to the identical
  result — end to end, no hidden setup.
- **Done bar**: runnable end-to-end (clean-machine reproduction) + web-verified.

## Read more

**Papers & articles**

- **Neovim User Documentation (`:help lsp`, `:help treesitter`, `:help lua-guide`)** — Neovim core team. Authoritative reference for the built-in LSP client, Tree-sitter, and the Lua plugin API. <https://neovim.io/doc/user/>
- **Language Server Protocol Specification** — Microsoft (3.17; illustrative version — Neovim's own docs do not pin a spec number, and Microsoft's site now labels 3.18 "Current" while it remains "under development"). The formal protocol family Neovim's LSP client implements against. <https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/>
- **Tree-sitter Documentation** — Max Brunsfeld and maintainers. Official docs for the incremental-parsing library Neovim uses. <https://tree-sitter.github.io/tree-sitter/>
- **nvim-lspconfig** — community-maintained (hosted under the `neovim` GitHub org; its README states the configs are "best-effort and supported by the community"). Reference collection of default LSP client configs, now consumed via `vim.lsp.enable()`. <https://github.com/neovim/nvim-lspconfig>

---

← Previous: [2 · Just Enough Lua](./02-just-enough-lua.md) · Next: [4 · Just Enough Python](./04-just-enough-python.md) →
