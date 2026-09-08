---
description: Rebase-and-push as the last resort for a genuinely wedged worktree-to-pr run once contention has been ruled out.
when_to_use: Use when a worktree-to-pr run is stuck with contention already ruled out and cancel/rerun does not clear it.
---

# Retriggering a Stuck Run With No Contention (PR Branches)

If [runner contention across the OSE repos](./runner-contention-across-the-ose-repos.md#runner-contention-across-the-ose-repos-read-first) has
been ruled out (nothing else queued or running) and a `worktree-to-pr` run is still stuck — queued
indefinitely, or wedged in a way `gh run cancel`/`gh run rerun` does not clear — rebase the PR branch
onto latest `origin/main` and push. The new commit SHA registers as a fresh trigger, which often
clears whatever the platform wedged on:

```bash
git fetch origin main
git rebase origin/main
git push --force-with-lease
```

Use `--force-with-lease`, never `--force`, per the
[No Destructive Git Operations Convention](../no-destructive-git-operations.md). This applies to
`worktree-to-pr` branches only — a direct push to `main` has no PR branch to rebase; if that is stuck
with contention ruled out, use `gh run rerun` (above) or wait longer.

The rebase lands foreign `origin/main` commits on the branch — apply the
[Integration Diff Review Convention](../integration-diff-review.md) before continuing. Retriggering
CI is not a reason to skip diff review of what just landed.
