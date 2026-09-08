---
description: Covers Phase C steps 1-3 — adopting an existing worktree/branch rather than reprovisioning, applying the freshness gate, and rebuilding the file-touch ledger.
when_to_use: Use when adopting a repo's already-in-flight worktree or branch instead of reprovisioning over it, or when reconciling it against origin/main.
---

# Phase C — Take Over the Live Work: Adopt, Freshness Gate, Ledger Rebuild (Sequential per Bucket-3 Repo)

For each repo classified Bucket 3:

1. **Adopt, never reprovision.** If a worktree already exists at `worktrees/<plan-identifier>/`,
   enter it directly — this satisfies `plan-execution.md` Step 0's "if it exists, make it the
   execution root" branch; do not run `git worktree add` again over it. If only a branch or PR exists
   with no local worktree, provision the worktree **from that existing branch**
   (`git worktree add worktrees/<plan-identifier> <branch>`) — never from `origin/main`, which would
   silently discard the branch's real content by starting a sibling history instead of continuing it.
2. **Apply the freshness gate exactly as `plan-execution.md` Step 0.5 states it**: `git fetch origin`;
   if the adopted worktree has uncommitted changes, do NOT auto-stash or discard — surface the dirty
   state and STOP for the user's explicit direction (commit, stash, or hold as-is), per [No
   Destructive Git Operations](../../../development/workflow/no-destructive-git-operations.md). If the
   branch carries commits not yet on `origin/main`, `git rebase origin/main`; on conflict, abort and
   surface the conflicting files rather than auto-resolving — identical to `plan-execution.md`'s own
   rule.
3. **Rebuild the file-touch ledger from the adopted branch**, per `plan-execution.md`'s own [Resume
   Reconciliation item 7](../plan-execution.md#resume-reconciliation-disk-is-truth): reconstruct it
   from the branch's `git log` commit list, each ticked checkbox's implementation-notes `Files
Changed` block, and (if recoverable) a prior session's transcript. Until the ledger is rebuilt,
   every modified or untracked path in the adopted worktree is treated as foreign, per [File-Touch
   Discipline](../../../development/practice/file-touch-discipline.md).

**Continued in** [Phase C — Recording an Existing PR and Reconciling delivery.md](./phase-c-pr-record-and-reconcile-delivery.md) for steps 4-5.
