---
title: "The Rule and Reading Checklist"
description: The five-step rule for reviewing an incoming diff before resuming in-flight work, and what to look for while reading it.
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
introduces commits you did not author in this session, and before resuming or continuing any
in-flight task:

1. **Identify the incoming range.** Use `git log --oneline <old-ref>..<new-ref>` (for a rebase, the
   pre-rebase ref is available via `git reflog`) or `git log --oneline ORIG_HEAD..HEAD` immediately
   after the operation.
2. **Read the full diff, not just the commit list.** Use `git diff <old-ref>..<new-ref>` — or `git
show` per commit for a large range — and actually read it. A file list is not a substitute for
   reading the changed lines.
3. **Cross-reference against your current work.** Check every file you have uncommitted changes in,
   every file your current plan step names, and every function/type/config your next action depends
   on, against the files touched by the incoming diff.
4. **Judge impact, not just overlap.** A rename, a signature change, a config default flip, a removed
   file, or a changed convention can invalidate your plan even when git reports zero line-level
   conflict with your own uncommitted edits.
5. **Adjust before continuing.** If the incoming diff changes an assumption your current work depends
   on, update the plan step, re-run affected tests, or re-read the changed file before proceeding —
   do not continue the original approach unmodified out of inertia.

A rebase/pull/merge that introduces zero foreign commits (e.g., `git pull` that reports "Already up to
date") is a no-op for this convention — there is nothing to review.

## Reading Checklist

When reading the incoming diff, look specifically for:

- Files you are currently editing or about to edit (rename, restructure, or semantic change nearby)
- Functions, types, or config keys your current task calls or reads
- Convention or governance files (`AGENTS.md`, `CLAUDE.md`, `repo-governance/**`) that redefine a rule
  your current task is following
- Dependency, lockfile, or toolchain version changes that could invalidate an assumption your task
  made about available tools or APIs
- Test files that now cover — or now conflict with — the behavior your current task is changing
