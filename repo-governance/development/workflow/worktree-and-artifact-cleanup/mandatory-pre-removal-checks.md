---
title: "Mandatory Pre-Removal Checks"
description: The six checks required before any git worktree remove, each grounded in an observed incident.
category: explanation
subcategory: development
tags:
  - git
  - workflow
  - worktree
  - cleanup
  - parallelism
created: 2026-07-20
when_to_use: Use immediately before running git worktree remove, to confirm identity, branch delivery, dirty diff, unpushed commits, and idleness.
---

# Mandatory Pre-Removal Checks

Run all six before any `git worktree remove`.

**1. Resolve the recorded worktree and every branch it used.**

Reconcile the identity's exact path with `git worktree list --porcelain`; its initial branch need not
equal the final checkout. Build the removal inventory from the append-only Delivery Branch Inventory
plus:

```bash
git -C <worktree> branch --show-current
```

Every plan-created/current branch needs a classification. A missing identity, path conflict, or
unrecorded current branch blocks removal. The file-touch ledger is never cleanup evidence.

**2. Prove delivery for every inventoried branch, never by squash ancestry.**

```bash
gh pr view <recorded-pr> --json state,headRefOid
```

For each `*-to-pr` entry, its recorded PR must report `MERGED`, and the inventory's reviewed-head SHA
must equal the current remote branch tip:

```bash
git fetch origin
test "$(git rev-parse origin/<branch>)" = "<recorded-reviewed-head-SHA>"
```

A missing remote ref, mismatch, or changed review head blocks removal and branch deletion: retain and
escalate. A direct-push entry needs its recorded commit reachable from `origin/main` and no open PR.
These repos **squash**-merge, so PR-mode delivery is the merged PR plus pinned reviewed head, never
branch ancestry on `main`.

**3. Read the worktree's dirty diff before removing it.**

```bash
git -C <worktree> status --porcelain
```

A merged PR does not prove the working tree is empty: archival content can be written after merge.
Recover it, or explicitly record why it is discarded; never silently remove it.

**4. Check every inventoried branch for unpushed commits — work that exists nowhere but this machine.**

```bash
git fetch origin
git log origin/<branch>..<branch> # PR-mode branch
git merge-base --is-ancestor <branch> origin/main # direct-push branch
```

Any output from the PR-mode check, a remote-tip/reviewed-head mismatch, or failed direct-push
reachability blocks removal. This protects against a local commit added after delivery. Do not use
`origin/main` ancestry for squash-merged PR branches; only direct pushes use it.

**5. Always use non-force `git worktree remove`.**

Never `rm -rf` a worktree — that leaves orphaned administrative state behind. The non-force command
refuses on a dirty worktree, which is the backstop for when checks 1-4 were skipped or rushed.
Preserving that backstop is the entire reason force is forbidden here.

**6. Never remove a worktree this plan did not create** without positive evidence it is idle. On a
shared machine, another session's live work is indistinguishable from stale state by path alone.
Observed live: of 11 worktrees across three repos, one held five dirty files belonging to active work
and was correctly left in place.
