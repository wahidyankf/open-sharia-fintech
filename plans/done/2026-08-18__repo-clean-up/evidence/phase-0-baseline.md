# Phase 0 Baseline — Repository Clean-Up

Captured on branch `worktree/repo-clean-up` at `c53ce0d6b`, before any
deletion. Recorded so no post-deletion failure can be misattributed to this plan.

## Toolchain

`npm run doctor -- --fix` → exit 0. 15/16 tools OK, 1 warning, 0 missing. Target-share fix created
8 shared `target/` symlinks across the two live worktrees.

## Project baselines

| Command                                    | Exit |
| ------------------------------------------ | ---- |
| `npm exec nx run ayokoding-www:test:quick` | 0    |
| `npm exec nx run ose-www:test:quick`       | 0    |
| `npm exec nx run rust-commons:test:quick`  | 0    |

All three pass before any change. `rust-commons` is included because this plan deletes it; its
green baseline establishes that the deletion removes working code rather than hiding a failure.

## Shell hazard encountered

The first two attempts recorded all three as failing with `Cannot find project 'ayokoding-wwwest'`.
That is not a project failure — zsh applies its `:t` (tail) history modifier to a bare `$p:test`,
even inside double quotes, rewriting the target name. `${p}:test:quick` with explicit braces is
required. The exit codes above were taken after that correction.
