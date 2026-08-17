---
title: "Branch Cleanup"
description: How to safely delete local and remote branches a plan created, after their PR is confirmed merged.
category: explanation
subcategory: development
tags:
  - git
  - workflow
  - worktree
  - cleanup
  - parallelism
created: 2026-07-20
when_to_use: Use when deleting local or remote branches after removing a repo's worktree.
---

# Branch Cleanup

Removing a worktree leaves its branches behind. Under the 1-PR ↔ 1-branch mapping, a multi-phase plan
accumulates one branch per **delivery unit** in a repo, even though it shares a single worktree across
all of them — so a plan that cleans its (one) worktree but not refs still leaves stale local and
remote branches on every repo it touched. Run this after removing a repo's worktree.

**Delete only branches this plan created**, and only after the branch's PR is confirmed MERGED by the
same `gh pr list --head <branch> --state all --json number,state,mergedAt` test used in check 1.
Ancestry tests are useless here for the same squash-merge reason.

**Local deletion uses `git branch -d`** — never `git branch -D`. The merged-check that `-d` retains is
the point: it refuses on an unmerged branch, which is the intended backstop. If `-d` refuses on a
branch whose PR reports MERGED, that is the **squash-merge shape, not lost work** — confirm the
content landed with `git log origin/main..<branch>`, then delete with an explicit stated reason. Do
not reflexively reach for `-D`; force-deletion is on the forbidden-operations list precisely because
it silences the signal you would want in the case where the content genuinely had not landed.

**Remote deletion uses `git push origin --delete <branch>`**, only after the PR is MERGED, and only
for branches this plan pushed. **Never delete `main`, and never delete an environment branch.** Which
branches those are is **repo-specific**: `ose-public` defines `prod-*` and `stag-*`; `ose-private`
currently defines none, so the rule is vacuously satisfied there. Confirm each repo's own
set with `git branch -a` rather than assuming this pattern is universal — a plan that hardcodes one
repo's environment-branch shape will eventually run against a repo that does not match it.

**Jurisdiction note.** `git push origin --delete` is remote-ref deletion, not history-rewriting
force-push. It sits deliberately **outside** the per-instance-approval gate that covers
`--force` / `--force-with-lease` / hook bypass, and is instead safety-gated by **this convention's
own** merged-check requirement above. This convention is the single authority for remote branch
deletion; the local-side forbidden-operations table and the remote-side force-push convention both
defer here.

**Run `git worktree prune`** after removals so administrative worktree metadata does not accumulate.
It touches only already-removed entries and is safe alongside other sessions.

**Never `gc` or `prune` the object store** as part of cleanup. History maintenance is a serialization
point on a shared machine, and carries a documented corruption risk when another process is writing
concurrently. It stays out of the cleanup gate entirely.
