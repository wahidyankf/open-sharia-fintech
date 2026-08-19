---
title: "Whole-Tree Staging Is Forbidden"
description: Why staging the entire working tree is forbidden on a shared machine, every forbidden spelling of it, and the explicit-paths procedure to use instead.
category: explanation
subcategory: development
tags:
  - git
  - workflow
  - safety
  - worktree
  - parallelism
created: 2026-07-20
when_to_use: Use before running git add or git commit -a, to confirm you are staging only paths you can account for.
---

# Whole-Tree Staging Is Forbidden

Stage **explicit paths only**. On a shared machine another actor's uncommitted work, scratch files,
and half-finished edits sit in the same tree. A whole-tree stage sweeps them into _your_ commit —
both a correctness bug (your commit now contains changes you did not author and cannot defend in
review) and a disclosure risk (it is how an unrelated credential-adjacent or scratch file gets
committed by accident, into a history that is permanent).

The rule is therefore stated as a **shape**, not as one flag spelling. Blocking `-A` alone would just
redirect the habit to the next spelling. All of the following are forbidden without explicit
per-instance approval:

- `git add -A` and its long form `git add --all`
- `git add .` — and any bare-directory add that pulls in paths you did not author
- `git add -u` / `--update` across the whole tree
- `git commit -a` / `--all`, which stages every tracked modification implicitly
- any wrapper, alias, or agent shortcut whose net effect is "stage everything"

**Required instead:**

1. Run `git status --porcelain` **first** and read every line.
2. Stage only the paths you can account for: `git add <path> [<path>...]`. Anything you cannot
   account for belongs to another actor and stays unstaged.

   **"Account for" is not a judgement call** — it means the path appears on the touched-file ledger
   the [File-Touch Discipline](../../practice/file-touch-discipline.md) requires you to keep. Without
   that ledger this step degrades into guessing from the diff, which is the failure it exists to
   prevent. Note that a `.claude/` edit legitimately brings generated `.opencode/`, `.codex/`, and
   `.agents/` mirrors into the same commit; those are yours, and they belong on the ledger too.

3. In a sibling repo or another worktree, use the `-C <worktree>` form —
   `git -C <worktree> add <path>` — so the operation cannot leak into the wrong tree.

The cost is a few named paths. The failure it prevents is committing someone else's work, or a
secret, into a history that cannot be rewritten without coordinating with everyone who has pulled it.
