---
description: The git commands for identifying and diffing an incoming range after each integration operation, and who is responsible for reviewing it.
when_to_use: Use when you need the exact command for the integration operation that just ran, or to confirm whose responsibility the review is.
---

# Commands and Agent Responsibilities

## Commands

```bash
# After a rebase — reflog gives you the pre-rebase tip
git reflog | head -5                      # find ORIG_HEAD or the pre-rebase SHA
git log --oneline ORIG_HEAD..HEAD         # commits that just landed on top of you
git diff ORIG_HEAD..HEAD                  # full diff of what changed

# After a pull or merge
git log --oneline HEAD@{1}..HEAD
git diff HEAD@{1}..HEAD

# After a fast-forward of local main to match origin
git log --oneline <old-local-sha>..HEAD
git diff <old-local-sha>..HEAD
```

## Agent Responsibilities

| Actor / Workflow        | Responsibility                                                                                                                     |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| All contributors        | Read the full incoming diff and reconcile task, plan, assumptions, ledger, and verification before the next action.                |
| plan-execution workflow | Treat integration as a checkpoint; revise affected remaining steps and rerun completed verification invalidated by the new `HEAD`. |
| Plan resume/takeover    | Apply this checkpoint after its freshness integration and before rebuilding or continuing execution state.                         |
