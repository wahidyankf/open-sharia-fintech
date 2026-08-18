---
title: "Mandatory Pre-Removal Checks"
description: The five checks required before any git worktree remove, each grounded in an observed incident.
category: explanation
subcategory: development
tags:
  - git
  - workflow
  - worktree
  - cleanup
  - parallelism
created: 2026-07-20
when_to_use: Use immediately before running git worktree remove, to confirm merge state, dirty diff, unpushed commits, and idleness.
---

# Mandatory Pre-Removal Checks

Run all five before any `git worktree remove`. Each is grounded in an observed incident, not a
hypothetical.

**1. Test merge state with `gh pr list`, never with ancestry.**

```bash
gh pr list --head <branch> --state all --json number,state,mergedAt
```

PRs in these repos are **squash**-merged, which replays the branch as one new commit. The branch's own
commits therefore never become ancestors of `main`, and `git merge-base --is-ancestor` reports
NOT-MERGED for **every** merged branch. Observed live: four worktree branches all reported NOT-MERGED
by ancestry while `gh` showed their PRs merged. Ancestry is not a conservative approximation here — it
is wrong in the direction that blocks correct cleanup, and it would be wrong in the dangerous
direction if anyone inverted it.

**2. Read the worktree's dirty diff before removing it.**

```bash
git -C <worktree> status --porcelain
```

A merged PR proves the _branch_ landed, not that the _working tree_ is empty. Archival record-keeping
in particular is written last — after the merge — and is easily left uncommitted. Observed live: a
worktree held its plan's two terminal archival checkboxes, ticked with real commit SHAs and a merge
timestamp, that existed **nowhere else**; every merge-state signal said "safe to delete". Recover such
content first, or discard it explicitly with a stated reason. Never discard it silently.

**3. Check for unpushed commits — work that exists nowhere but this machine.**

```bash
git -C <worktree> log origin/<branch>..<branch>
```

Any output is a commit that has never left this disk. Unlike checks 1 and 2, there is no remote copy
to fall back on: if the worktree goes, so does the commit.

**4. Always use non-force `git worktree remove`.**

Never `rm -rf` a worktree — that leaves orphaned administrative state behind. The non-force command
refuses on a dirty worktree, which is the backstop for when checks 1-3 were skipped or rushed.
Preserving that backstop is the entire reason force is forbidden here.

**5. Never remove a worktree this plan did not create** without positive evidence it is idle. On a
shared machine, another session's live work is indistinguishable from stale state by path alone.
Observed live: of 11 worktrees across three repos, one held five dirty files belonging to active work
and was correctly left in place.
