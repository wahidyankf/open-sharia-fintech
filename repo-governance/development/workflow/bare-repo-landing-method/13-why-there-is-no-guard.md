---
title: "Why There Is No Guard"
description: Why no automated hook can enforce the terminal reconcile step, and what primitive a future guard would have to use.
category: explanation
subcategory: development
tags:
  - git
  - workflow
  - worktree
  - bare-repo
  - safety
created: 2026-07-21
when_to_use: Use before proposing an automated guard for the terminal reconcile step, to understand why none exists today.
---

# Why There Is No Guard

No automated guard enforces the terminal reconcile step, and this section states why, so a future
reader does not propose one without first reading this.

Git ships **no `post-push` client hook**. The full enumerated hook list in `githooks(5)` has no entry
by that name. The nearest primitive, `pre-push`, fires **before** the transfer completes and therefore
cannot observe the state a push leaves behind. Background maintenance does not fill the gap either:
`git maintenance`'s `prefetch` task writes to a separate `refs/prefetch/*` namespace and never updates
`refs/remotes/origin/*`, so no maintenance task would trigger a guard even if one existed to trigger.

The consequence is direct: any future lag guard is necessarily a **wrapper script, never a hook** —
there is no git-native extension point this defect can attach to. If such a guard is ever built, it
has a documented starting primitive: `git status --porcelain=v2 --branch` emits a `# branch.ab` line
showing ahead/behind counts, but it does not run in a bare repository. A portable detector would
instead use `git rev-list --left-right --count origin/main...main`, the same command this document
uses throughout to show the defect and its resolution.
