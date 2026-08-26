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

Removing a shared worktree leaves one branch per delivery unit. Run this after removing the worktree.

**Delete only inventory branches after rechecking delivery proof and no-unpushed state.** A `*-to-pr`
branch needs its recorded PR `MERGED`, with both that PR's reviewed head and current
`origin/<branch>` tip equal to the inventory's recorded reviewed-head SHA. A missing remote ref or
any mismatch means retain the branch/worktree evidence and escalate. Direct push needs its recorded
commit on `origin/main` and no open PR. Do not treat the provisioned initial branch as the only branch.

**Local deletion uses `git branch -d`** — never `git branch -D`. For a squash-merged PR branch, make
the merged PR the delivery proof, then fetch without pruning and verify the local and
`origin/<branch>` tips are identical. Set that matching remote ref as the branch upstream if needed,
then use the ordinary non-force delete:

```bash
git fetch origin
test "$(git rev-parse origin/<branch>)" = "<recorded-reviewed-head-SHA>"
test "$(git rev-parse <branch>)" = "$(git rev-parse origin/<branch>)"
git branch --set-upstream-to=origin/<branch> <branch>
git branch -d <branch>
git push origin --delete <branch>
```

Equal tips prove no local commit followed review; `git branch -d` keeps Git's merged-check against
that upstream. `git log origin/main..<branch>` is non-empty after squash merge and proves nothing.
Without the matching remote-tracking ref, retain and escalate; never bypass the non-force guard.

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
