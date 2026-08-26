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

Run all six before any `git worktree remove`. Each is grounded in an observed incident, not a
hypothetical.

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
gh pr list --head <branch> --state all --json number,state,mergedAt
```

For each `*-to-pr` entry, its recorded PR must report `MERGED`. For a direct-push entry, fetch first,
verify its recorded delivery commit is reachable from `origin/main`, and confirm no PR for that branch
remains open. PRs in these repos are **squash**-merged, so a branch's commits do not become ancestors
of `main`; GitHub's merged-PR result is the delivery proof for PR-mode branches.

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

Any output from the PR-mode check, or a failed direct-push reachability check, blocks removal. Unlike
the delivery check, this protects against a local commit added after the recorded delivery. Do not use
`origin/main` ancestry for a squash-merged PR branch; it is valid only for the direct-push entry whose
recorded commit was pushed there directly.

**5. Always use non-force `git worktree remove`.**

Never `rm -rf` a worktree — that leaves orphaned administrative state behind. The non-force command
refuses on a dirty worktree, which is the backstop for when checks 1-4 were skipped or rushed.
Preserving that backstop is the entire reason force is forbidden here.

**6. Never remove a worktree this plan did not create** without positive evidence it is idle. On a
shared machine, another session's live work is indistinguishable from stale state by path alone.
Observed live: of 11 worktrees across three repos, one held five dirty files belonging to active work
and was correctly left in place.
