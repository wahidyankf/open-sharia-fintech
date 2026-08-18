---
title: "One Landing Path Per Unit Of Work"
description: The rule that a unit of work must land through exactly one path, and the duplicate-commit failure that results from mixing paths.
category: explanation
subcategory: development
tags:
  - git
  - workflow
  - worktree
  - bare-repo
  - safety
created: 2026-07-21
when_to_use: Use when a unit of work might be landed through more than one path, to confirm only one is actually used.
---

# One Landing Path Per Unit Of Work

Choose exactly one landing path for a given unit of work: through the worktree described above — step
6's direct push, or its branch-and-pull-request variant — **or** through an already-reconciled local
`main`. **Never both.** Applying the same delta through both paths produces a duplicate, stale-base
commit — the second landing carries a parent that the first landing's push has already superseded, and
the two histories then diverge instead of one simply following the other.

The duplicate-commit failure is the sharper-edged sibling of the silent-lag defect the worked example
above shows: that example left local `main` two commits behind with no divergence, because nothing
was re-landed against the stale base. Re-landing against a stale base is what turns a merely-behind
`main` into a **diverged** one, which the topology-keyed reconcile above cannot repair with a
fast-forward — recovery then requires the kind of manual, per-instance judgment this method exists to
make unnecessary.
