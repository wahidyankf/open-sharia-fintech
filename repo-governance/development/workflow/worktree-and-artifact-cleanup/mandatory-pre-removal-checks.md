---
title: "Mandatory Pre-Removal Checks"
description: Six checks required before any git worktree remove.
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

Reconcile its exact path with `git worktree list --porcelain`; the initial branch may differ from the
final checkout. Build the removal inventory from the append-only Delivery Branch Inventory plus:

```bash
git -C <worktree> branch --show-current
```

Classify every plan-created/current branch. Missing identity, path conflict, or an unrecorded current
branch blocks removal. The file-touch ledger is never cleanup evidence.

**2. Prove delivery for every inventoried branch, never by squash ancestry.**

```bash
gh pr view <recorded-pr> --json state,headRefName,headRefOid,mergedAt
git ls-remote --exit-code --heads origin "refs/heads/<branch>"
```

For each `*-to-pr` entry, GitHub must report `MERGED` with exact `headRefName`/`headRefOid` matching
the inventory branch/reviewed-head SHA; local branch must match. Never use squash ancestry. Classify:

- **Still exists**: fetch it; `origin/<branch>` and local branch equal recorded reviewed head.
- **GitHub auto-deleted it**: accept only with repository `delete_branch_on_merge: true` and a
  paginated timeline `HEAD_REF_DELETED_EVENT` for exact `headRefName` at/after `mergedAt`, plus the
  exact PR/local-head evidence above. Do not resurrect `origin/<branch>`.
- **Otherwise absent**: retain and escalate; disabled auto-delete, no matching event, changed PR
  head, or local mismatch is ambiguous.

Without auto-deletion, live-ref proof is required and canonical cleanup deletes it. Verified GitHub
deletion is remote cleanup: do not repeat it. Direct push needs its recorded commit on `origin/main`
and no open PR. These repos squash-merge: PR delivery is merged PR plus pinned reviewed head, not
`main` ancestry.

**Unenforced by decision.** A static gate cannot authenticate live repository settings or timelines.
Preserve those API results; an absent/incomplete record fails this check.

**3. Read the worktree's dirty diff before removing it.**

```bash
git -C <worktree> status --porcelain
```

A merged PR does not prove a clean tree: archival content may follow. Recover it or record why it is
discarded; never silently remove it.

**4. Check every inventoried branch for unpushed commits.**

```bash
git fetch origin
git log origin/<branch>..<branch> # PR-mode branch whose remote ref still exists
git merge-base --is-ancestor <branch> origin/main # direct-push branch
```

Output from the PR-mode check, remote-tip/reviewed-head mismatch, or failed direct-push reachability
blocks removal. For a verified auto-deleted PR branch, check 2 local-head equality is no-unpushed
proof; its remote is intentionally absent. Only direct pushes use `origin/main` ancestry.

**5. Always use non-force `git worktree remove`.**

Never `rm -rf`: it leaves orphaned administration. Non-force removal rejects a dirty tree, the
backstop when checks 1-4 were skipped or rushed; that is why force is forbidden.

**6. Never remove a worktree this plan did not create** without positive idleness evidence. On a
shared machine, path alone cannot distinguish another session's live work from stale state.
