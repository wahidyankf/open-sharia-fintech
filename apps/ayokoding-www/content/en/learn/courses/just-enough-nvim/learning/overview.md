---
title: "Overview"
date: 2026-07-13T00:00:00+07:00
draft: false
weight: 1
---

## Prerequisites

**This is the entry point -- it assumes no prior programming.**

- **Prior topics**: none, this is the entry point of the journey.
- **Tools & environment**: a computer with a macOS/Linux-compatible terminal and the latest
  **Neovim** installed (verify with `nvim --version`); nothing else. Current stable Neovim is
  **v0.12.4** (released 2026-07-05); re-run `nvim --version` at install time since Neovim ships
  fast-moving releases. Windows readers use WSL2 or Git Bash. Neovim is licensed **Apache-2.0**
  (with Vim-license-derived portions dual-licensed), a Tier-1 free-to-teach license.
- **Assumed knowledge**: how to open a terminal and run a command, and the willingness to learn
  modal editing.

## Why this exists -- the big idea

Every later topic in this journey drives build/run/test/git from the terminal, and without a
modal editor under your fingers you end up fighting your tools instead of the problem you are
actually trying to solve. The one idea worth keeping if you forget everything else: modal editing
separates _moving and selecting_ from _inserting_, so plain keystrokes become a composable editing
language built from an operator, a motion, and (optionally) a text object -- not a list of shortcuts
to memorize one by one.

**Cross-cutting big idea**: `mechanism-vs-policy` -- vanilla Neovim, as taught in this primer, is
pure **mechanism**. The **policy** layer (your own configuration, plugins, and language-server
tooling) is deliberately deferred to the next two topics in this journey, _Just Enough Lua_ and
_Extending Neovim_. This primer covers **vanilla latest Neovim with zero plugins or extensions**;
every keystroke below ships in the box.

## Install and open your first file

Install Neovim for your platform (macOS: `brew install neovim`; Debian/Ubuntu:
`sudo apt install neovim`; or download a release archive from
[github.com/neovim/neovim/releases](https://github.com/neovim/neovim/releases)), then confirm the
version:

```text
$ nvim --version
NVIM v0.12.4
```

Open any file directly from the shell -- this is the single command every example in this primer
starts from:

```text
nvim notes.txt
```

Neovim starts in **Normal mode** displaying the file's contents. From here, every worked example
below is a self-contained before/after file pair plus an exact, heavily annotated keystroke
transcript -- follow along by creating the "Before" file shown in each example, typing the listed
keystrokes exactly, and comparing your result against the "After" file.

## How this primer is organized

- **Beginner** (Examples 1-30) -- opening/quitting/saving, entering Insert mode, single-cell and
  word motions, the first operator+motion commands, yank/paste, undo/redo, basic search.
- **Intermediate** (Examples 31-62) -- `:substitute`, counts, Replace mode, all three Visual mode
  variants, the full text-object family, dot-repeat, named/numbered registers, marks and the
  jumplist, buffers/windows/tabs.
- **Advanced** (Examples 63-91) -- case operators, number increment/decrement, confirmed and
  ranged substitution, capture groups, macros, the undo tree, the global command, folding, the
  quickfix list, netrw, the black hole register, `:saveas`, and Terminal mode.

Every example cites the concept (`co-NN`) it exercises, and every keystroke shown traces to
Neovim's own `:help` documentation (`runtime/doc/*.txt`), web-verified 2026-07-12.

## Scope: just enough, not comprehensive

This is a **Primer**, not a comprehensive Neovim reference: it covers exactly the editing surface
the rest of this journey depends on, and deliberately excludes plugin management, LSP, debugging,
Treesitter, and completion -- all of which belong to _Extending Neovim_, two topics ahead. If a
Neovim feature is not exercised by a later topic in this journey, it is out of scope here on
purpose, not by oversight.

---

← Previous: [Overview (section)](../../overview.md) · Next: [Beginner Examples](./beginner.md) →
