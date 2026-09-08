---
description: Work location and integration target are independent axes; running from a worktree resolves to worktree-to-pr unless explicitly overridden.
when_to_use: Use when an agent or session is running inside a git worktree and must decide which delivery mode applies.
---

# Standard 6: Worktree Execution Does Not Determine the Mode by Itself

Running from inside a git worktree does not, by itself, select a push target. Work location (worktree
vs. primary checkout) and integration target (PR vs. direct push) are independent axes — the active
mode is whichever the three-tier precedence resolves to.

This standard covers all worktree execution patterns:

- An AI agent using `isolation: "worktree"` in the Agent tool.
- An agent or developer session started inside a path created by `git worktree add`.
- Any working directory under `worktrees/` or any other `git worktree add` target.

Running from a worktree resolves to `worktree-to-pr` (the default) unless an invocation argument or the
plan's `## Delivery Mode` field explicitly selects `worktree-to-origin-main`. Running from the primary
checkout (no worktree) resolves to `main-to-origin-main` or `main-to-pr` under the same precedence —
never inferred from the mere absence of a worktree.
