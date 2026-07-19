# 1 · Just Enough Nvim (Primer, Neovim §)

**prd row**: Pass 0 · Editor Foundations · Primer · Neovim § · Learn 101 / Drill 201 · Nvim-ready Yes ·
VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: **vanilla latest Neovim with zero plugins/extensions** — editing fluency built entirely
on what ships in the box. Plugin management, LSP, DAP, Treesitter, and completion are deliberately **out
of scope here** and belong to [`03-extending-neovim`](./03-extending-neovim.md). Neovim is Apache-2.0
(Tier-1, DD-21); this primer precedes [`02-just-enough-lua`](./02-just-enough-lua.md), so configuration
is shown as `:set`/ex-commands, **not** Lua code.

## Why this exists · the big idea

- **The problem before the solution**: every later topic drives build/run/test/git from the terminal
  (DD-17); without a modal editor under your fingers you fight your tools instead of the problem.
- **Keep-this-if-you-forget-everything**: modal editing separates _moving and selecting_ from _inserting_,
  so plain keystrokes become a composable editing language (operator + motion + text object).
- **Big ideas touched**: `mechanism-vs-policy` — vanilla Neovim is pure **mechanism**; the **policy** (your
  config, plugins, LSP) is deliberately deferred to [`02`](./02-just-enough-lua.md) and
  [`03`](./03-extending-neovim.md).

## Prerequisites

**This is the entry point — it assumes no prior programming.**

- **Prior topics**: none.
- **Tools & environment**: a computer with a **macOS/Linux-compatible terminal** and the latest **Neovim**
  installed (`nvim --version`); nothing else. (Windows readers use WSL2 or Git Bash — DD-25.)
- **Assumed knowledge**: how to open a terminal and run a command; the willingness to learn modal editing.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28). Re-confirm version pins at authoring
> time (fast-moving).

- 2026-07-12 — verified: current stable Neovim is **v0.12.4** (2026-07-05). Vanilla `nvim` ships
  `:checkhealth`, built-in `:terminal`, and `:help` with zero plugins (all core). (neovim.io / github.com)
- 2026-07-12 — verified: Neovim license is **Apache-2.0** with Vim-license-derived portions dual-licensed;
  Tier-1 free-to-teach (DD-21). (github.com neovim/LICENSE.txt)
- 2026-07-12 — verified (stable, not literally re-quoted): default keymaps `<C-v>` blockwise, `<C-w>`
  window prefix, `gt` tab-next are unchanged Vim-heritage defaults; spot-check `:help` at authoring.

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to a primary source fetched and read in the retroactive grounding sweep
> (2026-07-12, `web-researcher`). Neovim's `:help` doc source (`runtime/doc/*.txt` on
> `github.com/neovim/neovim`) is the authoritative primary source — identical content to `:help`.

- **Version + license** — current stable **Neovim v0.12.4** (2026-07-05), per
  [neovim/neovim Releases](https://github.com/neovim/neovim/releases); license **Apache-2.0** with
  Vim-license-derived portions dual-licensed, verbatim from
  [LICENSE.txt](https://raw.githubusercontent.com/neovim/neovim/master/LICENSE.txt). Fast-moving —
  re-confirm at authoring.
- **Modes (co-01/02)** — [`runtime/doc/intro.txt`](https://raw.githubusercontent.com/neovim/neovim/master/runtime/doc/intro.txt):
  seven basic + variant modes; co-02 names a curated subset (Normal/Insert/Visual/Command-line/Replace +
  Operator-pending), Terminal correctly deferred to co-20. `<C-\><C-n>` universal escape-to-Normal confirmed.
- **Motions + text objects (co-03/06)** — [`motion.txt`](https://raw.githubusercontent.com/neovim/neovim/master/runtime/doc/motion.txt):
  `w`/`b` exclusive, `e` inclusive, `$` inclusive, `gg`/`G` linewise; `iw`/`aw`/`i(`/`i"`/`ip`/`it`/`at`
  all built-in (tag objects need no plugin) — matches co-03's inclusive/exclusive/linewise classification.
- **Marks + jumplist (co-08)** — [`motion.txt`](https://raw.githubusercontent.com/neovim/neovim/master/runtime/doc/motion.txt):
  documented jump-motions list is `'` `` ` `` `G` `/` `?` `n` `N` `%` `(` `)` `[[` `]]` `{` `}` `:s` `:tag`
  `L` `M` `H` — **excludes `gg`** (only `G` registers a jump). ex-52 corrected accordingly.
- **Registers, case, increment, undo tree, macros (co-04/05/07/09/13/14)** —
  [`change.txt`](https://raw.githubusercontent.com/neovim/neovim/master/runtime/doc/change.txt),
  [`undo.txt`](https://raw.githubusercontent.com/neovim/neovim/master/runtime/doc/undo.txt),
  [`repeat.txt`](https://raw.githubusercontent.com/neovim/neovim/master/runtime/doc/repeat.txt): register 0 =
  most-recent yank, 1-9 = shifting delete history; `g<C-a>` sequential visual-block increment verbatim; undo
  is a genuine branching tree (`g-`/`g+`/`:undolist`/`:earlier`); dot-repeat + `q`/`@`/`@@`/`5@a` confirmed.
- **Substitution + ranges + global (co-10/11/12)** —
  [`change.txt`](https://raw.githubusercontent.com/neovim/neovim/master/runtime/doc/change.txt): the doc's own
  capture-group example is `:%s/\(foo\)bar/\1baz/` — verbatim match to ex-73. `:g`/`:g!`/`:v` all confirmed.
- **Tab pages (co-15)** — [`tabpage.txt`](https://raw.githubusercontent.com/neovim/neovim/master/runtime/doc/tabpage.txt):
  tab pages are **numbered** left-to-right from 1 (`tabpagenr()`); no built-in naming mechanism (native
  `:tabname` is [unimplemented issue #19272](https://github.com/neovim/neovim/issues/19272)). co-15 corrected
  from "named" to "numbered".
- **Folding, quickfix, netrw, terminal, visual (co-16/17/18/19/20)** —
  [`fold.txt`](https://raw.githubusercontent.com/neovim/neovim/master/runtime/doc/fold.txt),
  [`quickfix.txt`](https://raw.githubusercontent.com/neovim/neovim/master/runtime/doc/quickfix.txt),
  [`terminal.txt`](https://raw.githubusercontent.com/neovim/neovim/master/runtime/doc/terminal.txt),
  [`visual.txt`](https://raw.githubusercontent.com/neovim/neovim/master/runtime/doc/visual.txt): six
  foldmethods, `:copen`/`:cnext`/`:cdo`, location-list-as-window-scoped-quickfix, `:terminal` first-class
  Terminal mode all confirmed. Netrw still bundled + auto-loaded by default
  (`runtime/plugin/netrwPlugin.vim` runs `packadd netrw` at startup); freshness risk flagged
  ([opt-in proposal #32280](https://github.com/neovim/neovim/issues/32280) has **not** landed as of v0.12.4).
- **Books (Read more)** — "Practical Vim," Drew Neil, 2nd ed. 2015, Pragmatic Bookshelf; "Learning the vi
  and Vim Editors," Robbins/Hannah/Lamb, 8th ed., O'Reilly — both confirmed against publisher pages.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 8 (Primer §). Each example below cites the co-NN it exercises. -->

- **co-01 · modal-editing** — Every keystroke's meaning depends on the current mode; Normal mode is the
  default "home" state you return to via `<Esc>`, not a special editing state.
- **co-02 · mode-taxonomy** — Neovim exposes Normal, Insert, Visual, Command-line, and Replace modes plus
  the internal Operator-pending mode, each with distinct entry/exit keys and keystroke semantics.
- **co-03 · motions** — Cursor-movement commands (character, word, line, paragraph, search, find-char) are
  first-class objects usable alone or as an operator's argument, and are classified
  inclusive/exclusive/linewise.
- **co-04 · operator-motion-grammar** — Commands compose as `{operator}{count}{motion|text-object}` (e.g.
  `d3w`, `yi(`), so a small operator vocabulary combines with an open-ended motion vocabulary.
- **co-05 · counts** — A numeric prefix multiplies the following motion or operator+motion (`3dw` deletes
  three words; `5j` moves down five lines).
- **co-06 · text-objects** — `iw`/`aw`/`i(`/`a(`/`i"`/`a"`/`it`/`at`/`ip`/`ap` select semantically
  meaningful regions (word, block, quote, tag, paragraph) independent of exact cursor position, usable
  after an operator or in Visual mode.
- **co-07 · registers** — Named (`a`-`z`/`A`-`Z`), numbered (`0`-`9`), and special registers (unnamed `"`,
  black hole `_`, yank `0`, clipboard `+`) are named storage slots holding yanked or deleted text.
- **co-08 · marks-and-jumplist** — `m{letter}` bookmarks a buffer position for later recall via `'`/`` ` ``,
  while the separate jumplist automatically records "jump" motions so `<C-o>`/`<C-i>` navigate history like
  browser back/forward.
- **co-09 · the-dot-repeat** — The `.` command repeats the last change (an insertion or an operator+motion)
  verbatim at the new cursor position, making single-location edits composable across a file.
- **co-10 · search-and-substitution** — `/`, `?`, `n`, `N`, `*`, `#` locate text interactively, while the
  separate `:substitute` (`:s`) Ex command performs pattern-based find/replace with flags controlling scope
  and confirmation.
- **co-11 · ex-command-ranges** — Command-line-mode (`:`) commands accept an optional leading range (`.`,
  `$`, `%`, `'<,'>`, `/pat/,/pat2/`, line numbers) that scopes the command to specific lines before it runs.
- **co-12 · the-global-command** — `:g/pattern/command` is the "search then act" primitive: it executes any
  Ex command once per matching line across a given range (default: whole buffer).
- **co-13 · undo-tree** — `u` and `<C-r>` form a linear undo/redo stack, but every change actually branches a
  full undo tree; `g-`/`g+`, `:undolist`, and `:earlier`/`:later` expose and traverse branches unreachable
  by plain undo/redo.
- **co-14 · macros** — `q{register}` records a keystroke sequence into a register as replayable text;
  `@{register}` executes it, `@@` repeats the last-played macro, and a count (`5@a`) replays it n times.
- **co-15 · buffers-windows-tabs** — Three nested concepts: a buffer is in-memory file text, a window is a
  viewport onto exactly one buffer, and a tab page is a numbered collection of windows (identified by number
  via `tabpagenr()`, not by name) — each with independent navigation and lifecycle commands.
- **co-16 · folding** — A foldmethod (manual, indent, marker, syntax, expr, diff) determines how ranges of
  lines collapse into single foldable summary lines; `zo`/`zc`/`za`/`zR`/`zM` operate on fold state.
- **co-17 · quickfix-list** — A single global list of file/line locations (populated by `:make`, `:grep`, or
  `:vimgrep`) is navigable with `:cnext`/`:cprevious`/`:copen`; the location list is the same mechanism
  scoped per-window.
- **co-18 · netrw-file-explorer** — Neovim ships a built-in file browser (netrw), reachable via `:Explore`
  or by opening a directory path, supporting navigation, file creation, deletion, and renaming without
  leaving the editor.
- **co-19 · visual-mode-variants** — `v` (characterwise), `V` (linewise), and `<C-v>` (blockwise) extend a
  highlighted region from an anchor point that subsequent operators act upon; `gv` reselects the last region
  and `o` swaps the active end.
- **co-20 · terminal-mode-and-jobs** — `:terminal` opens a real shell inside a buffer with its own Terminal
  mode; `<C-\><C-n>` escapes to Normal mode to scroll/yank its output, and the buffer persists like any other.
  Terminal is a first-class mode (not a plugin), load-bearing for a terminal-first build/run/test loop.

## Worked examples

All in vanilla Neovim, no plugins → colocated under `just-enough-nvim/learning/code/`. Each example is a
before/after file pair plus the exact keystroke transcript (DD-30 follow-along). Each cites the `co-NN` it
exercises. Contiguous `ex-01..ex-91`.

### Beginner

- **ex-01 · launch-nvim-on-file** — open a file from the shell with `nvim notes.txt` — verify Neovim starts
  in Normal mode displaying `notes.txt`'s contents. (co-01)
- **ex-02 · quit-unmodified-buffer** — quit an unmodified buffer with `:q` — verify Neovim exits to the
  shell with no save prompt. (co-11)
- **ex-03 · quit-discard-changes** — edit a line, then run `:q!` — verify Neovim exits and the on-disk file
  is unchanged. (co-11)
- **ex-04 · reload-discard-with-e-bang** — edit a line, then run `:e!` — verify the buffer reloads from disk
  and the in-memory edit disappears without leaving Neovim. (co-11)
- **ex-05 · save-file** — save a modified buffer with `:w` — verify the file's contents on disk match the
  buffer. (co-11)
- **ex-06 · save-and-quit** — save and exit in one step with `:wq` — verify the file is written and the
  process ends. (co-11)
- **ex-07 · save-and-quit-shortcut** — press `ZZ` on a modified buffer — verify it writes (only if modified)
  and quits, equivalent to `:x`. (co-11)
- **ex-08 · enter-insert-before-cursor** — press `i` and type text — verify characters are inserted
  immediately before the original cursor column. (co-02)
- **ex-09 · enter-insert-after-cursor** — press `a` and type text — verify characters are inserted
  immediately after the original cursor column. (co-02)
- **ex-10 · append-end-of-line** — press `A` and type text — verify the cursor jumps to end-of-line before
  text is appended. (co-02)
- **ex-11 · insert-start-of-line** — press `I` and type text — verify insertion begins at the line's first
  non-blank character. (co-02)
- **ex-12 · open-line-below** — press `o` and type text — verify a new line opens below the current line in
  Insert mode. (co-02)
- **ex-13 · open-line-above** — press `O` and type text — verify a new line opens above the current line in
  Insert mode. (co-02)
- **ex-14 · escape-to-normal** — from Insert mode press `<Esc>` — verify mode returns to Normal and the
  cursor moves one column left. (co-01)
- **ex-15 · move-with-hjkl** — move right/down/up/left with `l`/`j`/`k`/`h` — verify cursor position changes
  by exactly one cell per keystroke. (co-03)
- **ex-16 · move-by-word** — press `w` and `b` repeatedly across a line — verify the cursor lands on the
  first character of the next/previous word each time. (co-03)
- **ex-17 · move-to-word-end** — press `e` on a word — verify the cursor lands on the last character of the
  current or next word. (co-03)
- **ex-18 · move-line-boundaries** — press `0`, then `^`, then `$` — verify the cursor moves to column 1, the
  first non-blank character, and end of line in turn. (co-03)
- **ex-19 · move-file-boundaries** — press `gg` then `G` — verify the cursor jumps to line 1, then to the
  last line of the file. (co-03)
- **ex-20 · move-by-paragraph** — press `}` then `{` across blank-line-separated paragraphs — verify the
  cursor jumps to the next and previous blank-line boundary. (co-03)
- **ex-21 · delete-char** — press `x` on a character — verify that character is removed and the line shifts
  left. (co-04)
- **ex-22 · delete-word** — press `dw` on a word — verify the word plus trailing whitespace up to the next
  word start is deleted. (co-04)
- **ex-23 · delete-line** — press `dd` — verify the entire current line is removed and the following line
  shifts up. (co-04)
- **ex-24 · delete-to-eol** — press `D` (equivalent to `d$`) — verify text from the cursor to end of line is
  deleted. (co-04)
- **ex-25 · change-word** — press `cw`, type replacement text — verify the word is deleted and Insert mode
  opens at that position. (co-04)
- **ex-26 · yank-and-paste-line** — press `yy` then `p` — verify a duplicate of the line appears directly
  below the original. (co-07)
- **ex-27 · undo-last-change** — press `u` after any edit — verify the buffer reverts to its pre-edit state.
  (co-13)
- **ex-28 · redo-change** — press `<C-r>` immediately after `u` — verify the undone change is reapplied.
  (co-13)
- **ex-29 · basic-search-forward** — type `/needle<CR>` — verify the cursor jumps to the next match of
  "needle" after the cursor. (co-10)
- **ex-30 · repeat-search** — press `n` then `N` after a search — verify the cursor advances to the next
  match, then back to the previous match. (co-10)

### Intermediate

- **ex-31 · basic-substitute-line** — run `:s/old/new/` on the current line — verify only the first
  occurrence on that line is replaced. (co-10)
- **ex-32 · substitute-whole-file** — run `:%s/old/new/g` — verify every occurrence of "old" in the file
  becomes "new". (co-10, co-11)
- **ex-33 · count-prefixed-motion** — press `3w` — verify the cursor advances exactly three words forward.
  (co-05)
- **ex-34 · count-prefixed-delete** — press `3dd` — verify exactly three lines starting at the cursor are
  deleted. (co-05)
- **ex-35 · replace-single-char** — press `r` then a character over an existing one — verify only that one
  character changes, remaining in Normal mode. (co-02)
- **ex-36 · replace-mode-typing** — press `R` and type several characters — verify each typed character
  overwrites existing text rather than inserting. (co-02)
- **ex-37 · visual-char-select-delete** — press `v`, extend the selection, then `d` — verify exactly the
  highlighted characters are removed. (co-19)
- **ex-38 · visual-line-select-indent** — press `V`, extend across lines, then `>` — verify all selected
  lines shift right by one shiftwidth. (co-19)
- **ex-39 · visual-block-insert** — press `<C-v>`, select a column across lines, then `I`, type text,
  `<Esc>` — verify the text is inserted at that column on every selected line. (co-19)
- **ex-40 · text-object-inner-word** — press `diw` inside a word — verify only that word is deleted,
  surrounding whitespace intact. (co-06)
- **ex-41 · text-object-a-word** — press `daw` — verify the word plus one adjacent whitespace run is deleted.
  (co-06)
- **ex-42 · text-object-inner-paren** — press `ci(` inside parentheses — verify only the content between `(`
  and `)` is deleted and Insert mode opens there. (co-06)
- **ex-43 · text-object-inner-quote** — press `di"` inside a quoted string — verify only the text between the
  quote marks is deleted. (co-06)
- **ex-44 · text-object-inner-tag** — press `cit` inside an HTML/XML tag pair — verify only the tag's inner
  content is replaced. (co-06)
- **ex-45 · text-object-a-paragraph** — press `dap` inside a paragraph — verify the whole paragraph plus its
  trailing blank line is deleted. (co-06)
- **ex-46 · dot-repeat-edit** — perform `cwFOO<Esc>`, move to another word, press `.` — verify the same
  change reapplies at the new location. (co-09)
- **ex-47 · named-register-yank-paste** — yank a line with `"ayy`, move elsewhere, paste with `"ap` — verify
  the yanked line appears there, independent of the unnamed register. (co-07)
- **ex-48 · named-register-append** — yank more text into the same register with `"Ayy` (uppercase) — verify
  the new text is appended to, not overwriting, register `a`. (co-07)
- **ex-49 · numbered-register-recall** — delete several separate lines, then paste with `"2p` — verify the
  second-most-recent deletion is inserted, not the most recent. (co-07)
- **ex-50 · set-mark-and-jump** — set a mark with `ma`, move away, jump back with `'a` — verify the cursor
  returns to mark `a`'s line. (co-08)
- **ex-51 · exact-mark-jump** — set a mark with `mb`, move away, jump back with `` `b `` — verify the cursor
  returns to the exact column, unlike `'b`. (co-08)
- **ex-52 · jumplist-navigation** — perform several jump motions (`G`, `/search`, `%`), then press `<C-o>`
  repeatedly — verify the cursor steps backward through prior jump locations, `<C-i>` steps forward again.
  (co-08)
- **ex-53 · open-second-file-buffer** — run `:e other.txt` — verify a new buffer for `other.txt` loads and
  becomes the active window content. (co-15)
- **ex-54 · list-and-switch-buffers** — run `:ls` to list open buffers, then `:b 2` — verify buffer number 2
  becomes active. (co-15)
- **ex-55 · cycle-buffers** — press `:bnext` then `:bprevious` — verify the active buffer advances to the
  next one in the list, then returns. (co-15)
- **ex-56 · horizontal-split-navigate** — run `:split`, then `<C-w>j` / `<C-w>k` — verify a second horizontal
  viewport opens and focus toggles between top and bottom windows. (co-15)
- **ex-57 · vertical-split-navigate** — run `:vsplit`, then `<C-w>l` / `<C-w>h` — verify a second vertical
  viewport opens and focus toggles between left and right windows. (co-15)
- **ex-58 · open-new-tab** — run `:tabnew`, then `gt` and `gT` — verify a new tab page opens and navigation
  cycles forward/backward through tabs. (co-15)
- **ex-59 · write-all-buffers** — with multiple modified buffers open, run `:wa` — verify every modified
  buffer is written to disk in one command. (co-15)
- **ex-60 · join-lines** — press `J` on a line — verify the next line is appended to the current one,
  separated by a single space. (co-04)
- **ex-61 · join-lines-no-space** — press `gJ` on a line — verify the next line is appended directly with no
  inserted space. (co-04)
- **ex-62 · decrease-indent** — press `<<` on an indented line — verify the line shifts left by one
  shiftwidth. (co-04)

### Advanced

- **ex-63 · indent-shift-multiple-lines** — visually select several lines with `V`, then press `3>` — verify
  all selected lines shift right by three shiftwidths in one operation. (co-05, co-19)
- **ex-64 · case-toggle-tilde** — press `~` on a character — verify its case flips and the cursor advances.
  (co-04)
- **ex-65 · case-lower-motion** — press `guiw` on a word — verify the entire word becomes lowercase.
  (co-04, co-06)
- **ex-66 · case-upper-motion** — press `gUiw` on a word — verify the entire word becomes uppercase.
  (co-04, co-06)
- **ex-67 · increment-number** — place the cursor on/before a digit and press `<C-a>` — verify the number
  under/after the cursor increases by 1. (co-04)
- **ex-68 · decrement-number** — press `<C-x>` on a number — verify the number decreases by 1. (co-04)
- **ex-69 · sequential-increment-visual-block** — block-select (`<C-v>`) a column of identical numbers across
  lines, press `g<C-a>` — verify each line's number increases sequentially (1, 2, 3, …) rather than all
  becoming the same value. (co-19)
- **ex-70 · substitute-with-confirm-flag** — run `:%s/old/new/gc` — verify Neovim prompts y/n/a/q before each
  replacement rather than substituting silently. (co-10)
- **ex-71 · substitute-with-line-range** — run `:10,20s/old/new/g` — verify only lines 10-20 are affected,
  leaving matches elsewhere untouched. (co-11)
- **ex-72 · substitute-visual-range** — visually select lines, press `:` to populate `'<,'>`, append
  `s/old/new/g`, `<CR>` — verify only the selected lines are substituted. (co-11, co-19)
- **ex-73 · substitute-with-capture-group** — run `:%s/\(foo\)bar/\1baz/` — verify the captured group is
  reused in the replacement, producing "foobaz" from "foobar". (co-10)
- **ex-74 · record-and-play-macro** — record with `qa`, perform an edit sequence, stop with `q`, replay with
  `@a` — verify the same edit sequence reapplies exactly once. (co-14)
- **ex-75 · repeat-macro-with-count** — run `5@a` to replay a recorded macro five times — verify the edit
  sequence applies to five successive targets. (co-14)
- **ex-76 · repeat-last-macro** — after running `@a` once, press `@@` — verify the most recently executed
  macro replays again without specifying the register. (co-14)
- **ex-77 · undo-tree-time-travel** — undo several changes, make a new edit (creating a branch), then press
  `g-` and `g+` — verify these reach the abandoned branch's text state, which plain `u`/`<C-r>` cannot.
  (co-13)
- **ex-78 · inspect-undo-tree** — run `:undolist` after several edits and undos — verify it lists change
  numbers, line-count deltas, and timestamps for each branch. (co-13)
- **ex-79 · global-delete-matching-lines** — run `:g/TODO/d` — verify every line containing "TODO" anywhere
  in the file is deleted in one pass. (co-12)
- **ex-80 · global-inverse-keep-matching** — run `:g!/KEEP/d` (or `:v/KEEP/d`) — verify every line NOT
  containing "KEEP" is deleted, leaving only matching lines. (co-12)
- **ex-81 · global-normal-command** — run `:g/^-/normal A;` — verify a semicolon is appended to the end of
  every line that starts with a hyphen. (co-12)
- **ex-82 · create-and-toggle-fold** — select several lines and press `zf`, then `za` — verify the lines
  collapse into a single foldable summary line, then toggle open/closed. (co-16)
- **ex-83 · close-open-all-folds** — with multiple folds defined, press `zM` then `zR` — verify all folds
  close to top level, then all reopen. (co-16)
- **ex-84 · populate-quickfix-vimgrep** — run `:vimgrep /TODO/ **/*.txt` — verify the quickfix list populates
  with every match across the glob. (co-17)
- **ex-85 · navigate-quickfix-list** — run `:copen`, then `:cnext` and `:cprevious` — verify the quickfix
  window shows the match list and the cursor jumps to each match's file/line in turn. (co-17)
- **ex-86 · netrw-open-explorer** — run `:Explore` in a buffer — verify a directory listing of the current
  file's folder opens as a netrw buffer. (co-18)
- **ex-87 · netrw-create-file** — inside netrw, press `%` and type a filename — verify a new empty file is
  created and opened for editing. (co-18)
- **ex-88 · netrw-delete-file** — inside netrw, place the cursor on a file and press `D` — verify the file is
  removed from disk after confirmation and disappears from the listing. (co-18)
- **ex-89 · black-hole-register-delete** — delete a word (into the unnamed register), then delete a line with
  `"_dd` — verify the black-hole deletion does not overwrite the unnamed register, so the original word is
  still available for `p`. (co-07)
- **ex-90 · saveas-new-filename** — run `:saveas copy.txt` — verify a new file `copy.txt` is written and the
  buffer's associated filename switches to `copy.txt`. (co-11, co-15)
- **ex-91 · terminal-run-and-escape** — run `:terminal ls`, then press `<C-\><C-n>` to leave Terminal mode —
  verify the command output appears in the buffer and Normal-mode motions (`gg`/`G`) then navigate it. (co-20)

## Capstone spec — intra-topic (primer → light consolidation)

- **Goal**: perform one non-trivial refactor of a small multi-file text project **entirely in vanilla
  Neovim** — no plugins, no mouse, no arrow keys — driving find/replace, macros, and the quickfix list,
  and capture the full keystroke transcript so the session is reproducible.
- **Concepts exercised**: [ ] modal editing [ ] operator+motion grammar [ ] text objects [ ] `:%s///`
  with capture groups [ ] a recorded macro replayed with a count [ ] `:vimgrep`→quickfix→`:cnext`
  multi-file edit [ ] registers [ ] `:terminal` build/run loop.
- **Ordered steps**:
  1. `just-enough-nvim/learning/capstone/code/before/` — seed 3 small text/source files with a repeated
     symbol to rename and a list to transform. Verify `ls` shows the seed files.
  2. Open in Neovim; rename the symbol across all files via `:vimgrep /oldName/ **/*` → `:copen` →
     `:cdo s/oldName/newName/g | update`. Verify `:cnext` walks every hit and `git diff`/`diff -r` shows
     the rename applied everywhere.
  3. Record a macro `qa … q` that reformats one list line; replay with a count `10@a`. Verify all lines
     reformatted identically.
  4. Run the project's check from `:terminal` (e.g. `python3 -m py_compile *.py` or a `grep` assertion)
     beside the source. Verify the terminal reports success.
  5. Save the keystroke transcript to `just-enough-nvim/learning/capstone/code/transcript.md`.
- **Acceptance criteria**: the `after/` tree differs from `before/` exactly by the intended refactor; the
  transcript reproduces it from scratch; no plugin, mouse, or arrow key was used.
- **Done bar**: runnable end-to-end (a reader following the transcript reaches the identical `after/`
  tree) + web-verified.

## Read more

**Books**

- **Practical Vim: Edit Text at the Speed of Thought** — Drew Neil (2nd ed., 2015). The classic guide to Vim's composable command grammar, still the most recommended path to editing fluency.
- **Learning the vi and Vim Editors** — Arnold Robbins, Elbert Hannah, Linda Lamb (8th ed., O'Reilly). The long-running comprehensive vi/Vim reference, basics to power-user scripting.

**Papers & articles**

- **Neovim User Documentation (`:help`)** — Neovim core team. Authoritative version-matched reference for Neovim's modal model, commands, options. <https://neovim.io/doc/user/>
- **Vim/Neovim built-in tutorial (`vimtutor` / `:Tutor`)** — Bram Moolenaar; Neovim team. Original hands-on modal-editing intro shipped with the editor.

---

← Previous: [README (syllabus index)](./README.md) · Next: [2 · Just Enough Lua](./02-just-enough-lua.md) →
