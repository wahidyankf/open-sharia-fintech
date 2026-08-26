---
title: "Branch Cleanup"
description: Safely delete plan-created branches after their PR is confirmed merged.
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

**Delete only inventory branches after rechecking delivery and no-unpushed proof.** For `*-to-pr`,
the recorded PR must be `MERGED`; its exact branch and head must equal the inventory's reviewed-head
SHA; and its live `origin/<branch>` must equal that SHA, unless GitHub proves automatic deletion with
`HEAD_REF_DELETED_EVENT` and enabled `delete_branch_on_merge`. Any other absent ref is unsafe. Direct
push needs its recorded commit on `origin/main` and no open PR. Include every plan-created/current
branch, not only the initial branch.

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

Equal tips prove no local commit followed review; `git branch -d` retains Git's merged check.
`git log origin/main..<branch>` proves nothing after a squash merge.

For a GitHub-auto-deleted branch, preserve the required GitHub proof and local-head equality; do not
recreate or delete a remote ref. Attempt only `git branch -d <branch>`. If it declines because squash
merge leaves no upstream, retain and escalate that branch-cleanup exception; worktree removal remains
valid. Never substitute `-D`, a fabricated tracking ref, or a direct ref delete.

**Use `git push origin --delete <branch>`** only for a plan-pushed, still-live branch after its PR is
`MERGED`. Verified GitHub auto-deletion needs no second command. **Never delete `main` or an
environment branch.** Environment branches are repo-specific: `ose-public` has `prod-*`/`stag-*`;
`ose-private` currently has none. Confirm each repo with `git branch -a`.

**Jurisdiction.** `git push origin --delete` deletes a remote ref; it is not history-rewriting
force-push. It is governed by this convention's merged-check requirement, not the per-instance gate
for `--force`, `--force-with-lease`, or hook bypass. Other local/remote force-push rules defer here.

**Run `git worktree prune`** after removals; it touches only removed entries.

**Never `gc` or object-store `prune`** during cleanup: shared-machine history maintenance risks
corruption while another process writes.
