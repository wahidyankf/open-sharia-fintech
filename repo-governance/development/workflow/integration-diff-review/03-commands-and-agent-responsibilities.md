---
title: "Commands and Agent Responsibilities"
description: The git commands for identifying and diffing an incoming range after each integration operation, and who is responsible for reviewing it.
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
when_to_use: Use when you need the exact command for the integration operation that just ran, or to confirm whose responsibility the review is.
---

# Commands and Agent Responsibilities

## Commands

```bash
# After a rebase — reflog gives you the pre-rebase tip
git reflog | head -5                      # find ORIG_HEAD or the pre-rebase SHA
git log --oneline ORIG_HEAD..HEAD         # commits that just landed on top of you
git diff ORIG_HEAD..HEAD                  # full diff of what changed

# After a pull or merge
git log --oneline HEAD@{1}..HEAD
git diff HEAD@{1}..HEAD

# After a fast-forward of local main to match origin
git log --oneline <old-local-sha>..HEAD
git diff <old-local-sha>..HEAD
```

## Agent Responsibilities

| Agent / Workflow        | Responsibility                                                                                                                    |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| All AI agents           | Read the full incoming diff and reassess in-flight work impact after every rebase, pull, merge, or cherry-pick before continuing. |
| plan-execution workflow | Treat an integration event mid-phase as a checkpoint: pause, review, adjust the remaining delivery steps if needed, then resume.  |
| Developer (human)       | Same expectation — this convention is not agent-specific.                                                                         |
