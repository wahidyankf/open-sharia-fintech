# In-Progress Plans

Active project plans currently being worked on.

## Active Plans

- [fundamentally-strong-software-engineer](./fundamentally-strong-software-engineer/) — new breadth-first
  relearn-and-drill tutorial section on ayokoding-www (61 topics, Pass 0 forge prologue + five-pass
  spiral, learning + drilling tracks, Python-primary). Delivery Mode: `main-to-origin-main`.
- [rhino-cli-git-root-test-fixture-race](./rhino-cli-git-root-test-fixture-race/README.md) —
  a rhino-cli git-root test fixture races under parallel `nx affected`, corrupting the real
  repository's git state (stray commits, stray linked worktrees, mis-attributed authorship).
  Delivery Mode: `worktree-to-pr`.
- [e2e-coverage-rule-feature-skip-fixme-gap](./e2e-coverage-rule-feature-skip-fixme-gap/README.md) —
  the e2e-coverage gap detector's `@skip`/`@fixme` special-tag detection is scoped to
  `Scenario Outline` level only; `Rule:`/`Feature:`-level tags produce the same undetected shape one
  AST level up. Delivery Mode: `worktree-to-pr`.
- [rust-cargo-target-dir-sharing](./rust-cargo-target-dir-sharing/README.md) —
  Rust `target/` directories are duplicated per git worktree (~32 GB observed); share build output
  across worktrees by folding a per-crate `target/` symlink + worktree-aware cache GC into
  `rhino-cli doctor` (local-dev-only, CI-guarded), byte-identical across all three repos.
  Delivery Mode: `worktree-to-pr`.

## Instructions

**Quick Idea Capture**: For 1-3 liner ideas not ready for formal planning, use `../ideas.md`.

**Naming**: Plans in `in-progress/` use NO date prefix — just the slug (e.g., `organiclever-web-responsive-breakpoints/`). Strip the date prefix when moving from `backlog/`.

When starting work on a plan:

1. Move and rename the plan folder: `git mv backlog/YYYY-MM-DD__[identifier]/ in-progress/[identifier]/` (strip the date prefix)
2. Update the plan's README.md status to "In Progress"
3. Add the plan to this list

When completing a plan:

1. Rename and move: `git mv in-progress/[identifier]/ done/YYYY-MM-DD__[identifier]/` using today's completion date
2. Update this list
