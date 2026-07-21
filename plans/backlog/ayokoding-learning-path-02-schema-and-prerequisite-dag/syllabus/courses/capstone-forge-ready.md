# Capstone: Forge-Ready (Prologue milestone, multi)

**Course ID**: `capstone-forge-ready` · **Kind**: Prologue milestone · **Language**: multi.

**Short summary**: Reproducible personal dev forge (nvim + lua + extend)

**Integrates**: `just-enough-nvim`, `just-enough-lua`, `extending-neovim` — the same three editor-tooling
courses each path places in its Prologue / Stage 1.

## Why this exists · the big idea

- **The problem before the solution**: every later course assumes a real, reproducible editing forge
  exists. This capstone stands one up from an empty machine so nothing downstream has to re-explain
  setup.
- **Keep-this-if-you-forget-everything**: your editor is code — a versioned Lua config you can
  `git clone` onto a clean machine and be productive in minutes.
- **Big ideas touched**: reproducibility (pinned config + lockfile), raw-form-first tooling (edit /
  navigate / build / run / debug in Neovim + terminal, no mouse).

## Prerequisites

- **Prior courses**: [`just-enough-nvim`](./just-enough-nvim.md), [`just-enough-lua`](./just-enough-lua.md),
  [`extending-neovim`](./extending-neovim.md).
- **Tools & environment**: a macOS/Linux terminal; **Neovim** with a plugin manager, LSP, and
  Treesitter (all OSS, Tier-1); `git`.
- **Assumed knowledge**: vanilla Neovim editing fluency, basic Lua, and a working extended config from
  the three prerequisite courses.

## Capstone spec — inter-course (Prologue milestone)

Integrates the editor-tooling trio (`just-enough-nvim`, `just-enough-lua`, `extending-neovim`): vanilla
editing fluency + Lua + a real extended config.

- **Goal**: stand up a complete, reproducible personal development **forge** from an empty machine
  profile — a versioned Neovim config repo the reader can `git clone` and use to edit, navigate, search,
  and run code with LSP + Treesitter — and prove editing fluency by driving a scripted refactor in it
  with no mouse/arrow keys.
- **Concepts exercised**: [ ] raw-form editing (`just-enough-nvim`) [ ] Lua modules/closures/metatables
  (`just-enough-lua`) [ ] plugin manager + LSP + Treesitter + user command + autocommand
  (`extending-neovim`) [ ] a reproducible config repo layout [ ] the `:terminal` build/run loop.
- **Ordered steps**:
  1. `capstone-forge-ready/code/nvim-config/` — a self-contained config repo (init.lua + `lua/` tree +
     pinned plugin lockfile). Verify a clean `XDG_CONFIG_HOME=$(mktemp -d) nvim --headless "+checkhealth"
"+qa"` bootstraps and reports healthy.
  2. `capstone-forge-ready/code/sample-project/` — a small Python project. Open it in the forge; verify
     LSP diagnostics + Treesitter highlighting appear.
  3. Drive a scripted, mouse-free refactor across the sample project using motions + macros + quickfix
     (reusing the raw-form editing workflow), recording the transcript. Verify the refactor lands
     identically from the transcript.
  4. Run the sample project's check from `:terminal` beside the source. Verify it passes.
- **Acceptance criteria**: a reader on a clean machine reproduces the forge from the repo, opens the
  sample project with working LSP+Treesitter, and replays the refactor transcript to the identical
  result — end to end, no hidden setup.
- **Done bar**: runnable end-to-end (clean-machine reproduction) + web-verified.

## In which paths

- `interview-ready/software-engineer` — Prologue · Editor foundations (skippable for the experienced).
- `immediately-effective/software-engineer` — Stage 1 · Editor & tooling (get set up fast).
- `fundamentally-strong/software-engineer` — Prologue · Editor & reproducible forge (skippable).

> _Content originated in the now-closed FS-SE plan (the `capstone-forge-ready` inter-topic capstone,
> anchored in topic 3); it now lives here in full — this course block is self-contained. The legacy
> embedded spec (formerly in `extending-neovim.md`, `_index.md` weight **135**) has been removed as a
> stale duplicate (reconciled 2026-07-19) — this file is the sole canonical spec._

---

← Back to the [course library catalog](./README.md)
