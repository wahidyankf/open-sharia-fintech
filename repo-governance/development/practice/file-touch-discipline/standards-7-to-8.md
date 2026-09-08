---
description: The ledger is scoped to one (repository, worktree) pair, and foreign files not on the ledger get no action at all
when_to_use: Use when working across multiple repositories or worktrees, or when you encounter a file that is not on your ledger.
---

# Standards 7-8: Scope and Foreign Files

## Standard 7 — The Ledger Is Scoped to a (Repository, Worktree) Pair

A ledger is valid for exactly one working tree in one repository. The same relative path in a
different worktree is a **different file** with a different authorship history.

Work spanning several repositories or worktrees keeps **one ledger per tree**, never a merged list.
Delegated agents each keep their own and return it as part of their result; the orchestrator merges
the returned ledgers explicitly and never assumes a subagent touched only what it was asked to touch.

## Standard 8 — Foreign Files Are Left Exactly As Found

A file that is not on your ledger gets **no action at all**: not staged, not reverted, not stashed,
not cleaned, not deleted, not reformatted, not "fixed while I was in there", not `git add`-ed
because it looked related.

This holds even when the file appears stray, broken, or obviously wrong. A file that looks abandoned
is frequently a colleague's work in progress, and a formatter run across a tree you do not own
produces a diff that is genuinely painful to disentangle.

If a foreign file is genuinely blocking your work, **say so and stop** — report the path, say why it
blocks you, and let the user decide. That is a two-line report against an unrecoverable loss.
