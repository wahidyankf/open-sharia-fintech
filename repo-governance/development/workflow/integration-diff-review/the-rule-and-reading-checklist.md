---
title: "The Rule and Reading Checklist"
description: The integration checkpoint for reviewing an incoming diff and reconciling active work before the next action.
category: explanation
subcategory: development
tags:
  - git
  - workflow
  - safety
  - rebase
  - merge
  - review
created: 2026-08-06
when_to_use: Use immediately after a rebase, pull, merge, cherry-pick, or fast-forward, before resuming any in-flight task.
---

# The Rule and Reading Checklist

## The Rule

Immediately after any `git rebase`, `git pull`, `git merge`, `git cherry-pick`, or fast-forward that
introduces commits not previously present on the current branch, and before the next task action:

1. **Identify the incoming range.** Use `git log --oneline <old-ref>..<new-ref>` (for a rebase, the
   pre-rebase ref is available via `git reflog`) or `git log --oneline ORIG_HEAD..HEAD` immediately
   after the operation.
2. **Read the full diff, not just the commit list.** Use `git diff <old-ref>..<new-ref>` — or `git
show` per commit for a large range — and actually read it. A file list is not a substitute for
   reading the changed lines.
3. **Assess the complete active state.** Reconcile the diff against the current task, the whole
   plan, every active assumption, the actor-owned file-touch ledger, and all completed and remaining
   verification. Semantic effects matter even without path overlap.
4. **Preserve ledger ownership.** Incoming paths do not become actor-owned merely because they
   landed. Add a path to the ledger only when the actor subsequently mutates it for the current work.
5. **Adjust every affected item.** Update the task or plan, replace invalid assumptions, revise
   remaining verification, and rerun completed checks whose evidence depended on the old `HEAD`.
   Record that reconciliation before continuing.

An integration that introduces no commits absent from the pre-operation branch (for example, a pull
that reports "Already up to date") is a no-op for this convention. Commit authorship is irrelevant:
a commit is incoming when branch membership changed, including one the current actor authored in
another branch or session.

## Reading Checklist

When reading the incoming diff, look specifically for:

- Files you are currently editing or about to edit (rename, restructure, or semantic change nearby)
- Functions, types, or config keys your current task calls or reads
- Convention or governance files (`AGENTS.md`, `CLAUDE.md`, `repo-governance/**`) that redefine a rule
  your current task is following
- Dependency, lockfile, or toolchain version changes that could invalidate an assumption your task
  made about available tools or APIs
- Test files that now cover — or now conflict with — the behaviour your current task is changing
- Completed verification whose result depended on files, configuration, dependencies, or the old
  `HEAD` changed by the incoming range
