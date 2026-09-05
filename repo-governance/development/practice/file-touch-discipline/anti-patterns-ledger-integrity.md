---
title: "File-Touch Discipline — Anti-Patterns: Ledger Integrity"
description: Four anti-patterns that corrupt ledger integrity - post-compaction blanket staging, reconstructing authorship from the diff, tidying the tree, and trusting a clean-looking worktree
category: explanation
subcategory: development
tags:
  - git
  - safety
  - concurrency
  - ai-agents
  - compaction
  - discipline
created: 2026-08-01
when_to_use: Use when reviewing your own staging behaviour for signs of these four failure patterns, or when explaining why a specific staging shortcut is unsafe.
---

# Anti-Patterns: Ledger Integrity

## Post-Compaction Blanket Staging

**Problem**: After a compaction, the agent runs `git status`, sees a set of modified files, concludes
"this is my work from before the summary", and stages all of it.

**Why it fails**: The compaction dropped the inventory but not the confidence. The tree contains
other actors' changes and the agent has no way to tell — the inference feels sound and is unfalsifiable
from inside the tree.

**Fix**: Standard 4 keeps the inventory alive through the compaction. If it was already lost,
Standard 5 governs: degraded mode, default deny.

---

## Reconstructing Authorship From the Diff

**Problem**: The agent reads `git diff` and decides which hunks look like its own work based on style,
subject matter, or plausibility.

**Why it fails**: Two agents working from the same conventions in the same repository produce changes
that look identical in style and subject. Plausibility is not authorship, and the method fails most
often precisely where the repository is most active.

**Fix**: Standard 3 — the ledger comes from what you did, never from what the tree shows.

---

## Tidying the Tree

**Problem**: The agent encounters an untracked scratch file, a stray edit, or a half-finished change
and cleans it up in passing as a courtesy.

**Why it fails**: Uncommitted work has no recovery path. The courtesy is unrecoverable when wrong,
and the actor who lost the work usually discovers it much later, with no way to trace what happened.

**Fix**: Standard 8 — no action on foreign paths. Report and stop if genuinely blocked.

---

## Trusting a Clean-Looking Worktree

**Problem**: The PR merged, so the agent assumes the worktree is spent and removes it.

**Why it fails**: A merged PR says nothing about uncommitted files still sitting in that worktree —
evidence, notes, or a colleague's follow-up work that was never part of the PR.

**Fix**: Read the dirty state before removal, reconcile it against the ledger (Standard 6), and
recover anything foreign before the worktree is destroyed.
