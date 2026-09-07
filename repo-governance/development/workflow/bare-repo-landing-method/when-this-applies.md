---
description: The two conditions that trigger the bare-repo landing method, and the checked-out-branch trap to avoid.
when_to_use: Use when deciding whether a landing needs this method — a bare target repository, or a landing performed from a side worktree.
---

# When This Applies

Use this method whenever either condition holds:

- The target repository has **no primary checkout** — a bare repository (`core.bare=true`). Bareness
  is a per-invocation property of a specific clone, not fixed to a repository's name; verify with
  `git worktree list` rather than assuming which repos are bare from this document. Every mutation
  there must flow through a linked worktree, because there is no other tree to work in.
- A landing is performed **from a side worktree rather than from the branch's own checkout**, even in
  a non-bare repository such as `ose-public`. The side worktree's push reaches the remote branch, but
  nothing about that push touches the local `main` sitting in the repository's own primary checkout —
  the same lag this method exists to close.

**If you found this document while reconciling a repository that has a work tree, the [Terminal
Reconcile](./terminal-reconcile.md#terminal-reconcile) table's second row — `git fetch` then `git merge --ff-only
origin/main` — is the command for you, not the bare-repo refspec form.** Running
`git fetch origin main:main` against a **checked-out** branch fast-forwards the ref without touching
the index or working tree, leaving them pinned to the old commit while `HEAD` points at the new one;
git then reports the entire skipped delta as a pending mass revert. This happened for real — see the
[Terminal Reconcile](./terminal-reconcile.md#terminal-reconcile) table's "Why this form" column, and
the incident this caused is separately tracked.
