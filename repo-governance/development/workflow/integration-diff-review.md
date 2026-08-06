---
title: "Integration Diff Review Convention"
description: Before continuing in-flight work after a rebase, pull, merge, or other operation that brings foreign commits into the current branch, read the full incoming diff, assess its impact on the work already underway, and adjust that work accordingly
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
---

# Integration Diff Review Convention

Any operation that brings commits from another branch or remote into the branch you are currently
working on — `git rebase`, `git pull`, `git merge`, `git cherry-pick`, or a fast-forward of local
`main` after a sibling worktree pushed ahead of it — changes the ground you are standing on. A clean
merge with zero textual conflicts is not evidence that the incoming changes are safe to ignore: files
you are mid-edit on may have been renamed, functions you are calling may have changed signature,
assumptions your current plan step depends on may no longer hold. Before continuing the interrupted
work, you MUST read the incoming diff in full and think hard about what changed and what it means for
what you were doing — not just check that git reports no conflict markers.

## Principles Implemented/Respected

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: Resuming
  work on autopilot immediately after an integration operation is the opposite of understanding before
  acting. This convention inserts a mandatory understanding step between "the integration succeeded"
  and "continue the task."

- **[Root Cause Orientation](../../principles/general/root-cause-orientation.md)**: Bugs introduced by
  an unreviewed rebase/pull surface later as confusing test failures or silent semantic breakage, far
  from their true cause. Reviewing the diff at the moment of integration catches the cause immediately,
  not downstream.

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: "The
  merge was clean" is an implicit, git-mechanical signal. This convention requires an explicit,
  read-the-diff judgment call about semantic impact, which git's conflict detection cannot make.

## Conventions Implemented/Respected

- **[No Destructive Git Operations Convention](./no-destructive-git-operations.md)**: That convention
  governs which local operations are safe to run. This convention governs what to do with the
  operation's _result_ once it has run — the two are companions, not overlapping.

- **[Bare-Repo Base-Worktree Landing Method](./bare-repo-landing-method.md)**: Fast-forwarding local
  `main` after a sibling worktree has pushed ahead is itself an integration event in scope of this
  convention — the incoming commits must be read, not just fast-forwarded past.

- **[Agent Workflow Orchestration](../agents/agent-workflow-orchestration.md)**: The same-machine
  assumption means other agents' pushes can land on the branch you are rebasing onto or pulling from
  at any time. This convention is the required response the moment that happens.

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

## Forbidden Actions

- Continuing an in-flight task immediately after a rebase/pull/merge without reading the incoming diff.
- Treating "no conflict markers" as proof the integration is safe to ignore.
- Reading only the commit subject lines (`git log --oneline`) and skipping the actual diff content.
- Assuming a fast-forward is inherently safe because it involved no merge commit.

## Examples

### PASS: Reviewing impact before resuming

```
Agent: Rebased onto origin/main — 4 commits landed.

Reading diff:
  git diff ORIG_HEAD..HEAD

Found: repo-governance/development/quality/code.md now requires an additional
pre-commit check that my current task's new script doesn't yet satisfy.

Adjusting: updating the script before continuing the original task, rather
than pushing straight to a failing hook.
```

### FAIL: Resuming on autopilot after a clean rebase

```
Agent: Rebased onto origin/main — no conflicts.

Continuing with the original plan.
```

No diff was read. A clean rebase says nothing about whether the incoming commits changed something
the current task depends on.

### PASS: Fast-forwarding local main after a sibling worktree push

```
Agent: Sibling worktree pushed 2 commits to origin/main. Fast-forwarding local main.

Reading diff before resuming:
  git diff <old-local-sha>..HEAD

Found: one of the 2 commits renamed a lib import path my current task's new
file already uses.

Adjusting: updating the import in my new file before committing.
```

## Related Documentation

- [No Destructive Git Operations Convention](./no-destructive-git-operations.md) — the companion
  convention for which local git operations are safe to run at all.
- [Agent Workflow Orchestration](../agents/agent-workflow-orchestration.md) — the same-machine
  assumption that makes concurrent, unreviewed integration events likely.
- [CI Post-Push Verification Convention](./ci-post-push-verification.md) — the parallel post-push
  discipline: verify after you push out, review after you pull in.
