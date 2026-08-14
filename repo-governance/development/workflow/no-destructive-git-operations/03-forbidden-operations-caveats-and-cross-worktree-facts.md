---
title: "Forbidden-Operations Caveats and Cross-Worktree Facts"
description: Two forbidden-operation behaviors that are easy to misread as safe, and the git mechanics that already enforce isolation across worktrees.
category: explanation
subcategory: development
tags:
  - git
  - workflow
  - safety
  - worktree
  - parallelism
created: 2026-07-20
when_to_use: Use when tempted to treat bare --force-with-lease or --prune=now as safe, or when reasoning about what git already isolates between worktrees.
---

# Forbidden-Operations Caveats and Cross-Worktree Facts

Two behaviors deserve their own statement because they are easy to misread as safe:

- **Bare `--force-with-lease` is not the safe form.** The lease is checked against whatever the local
  ref says, so a stale fetch can satisfy it. Per
  [git-push(1)](https://git-scm.com/docs/git-push), supplying the option without an expected value
  "interacts very badly with anything that implicitly runs `git fetch` … this is trivially defeated if
  some background process is updating refs in the background" — precisely the shared-machine case.
- **`--prune=now` is documented as corruption-risking under concurrency.** Per
  [git-gc(1)](https://git-scm.com/docs/git-gc), running gc concurrently with another process "may
  corrupt the repository if the other process later adds a reference to the deleted object."

## Cross-Worktree Facts

Git already enforces much of this. State the mechanics so agents cooperate with the tool rather than
fighting it.

- The **object database and `refs/*` are shared** across all worktrees; **`HEAD` and the index are
  per-worktree**. Concurrent checkouts of _different_ branches therefore do not collide by design —
  isolation is real, and does not need to be manufactured.
- Git **already refuses** to check out a branch that is active in another worktree. Note the exact
  mechanism: bare `-f` / `--force` does **not** bypass this guard, but a dedicated
  `--ignore-other-worktrees` flag exists that does. **Do not pass it.**
- Because the object store and refs are shared, `gc`, aggressive pruning, and forced worktree removal
  can affect state another worktree depends on **even though the working trees are isolated**.
