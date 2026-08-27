---
title: "Forbidden Actions and Examples"
description: Actions that violate the integration diff review convention, and worked pass/fail examples of reviewing after a rebase, pull, or fast-forward.
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
when_to_use: Use when checking whether a resumed task actually reviewed its incoming diff, or when writing a worked example of doing so.
---

# Forbidden Actions and Examples

## Forbidden Actions

- Continuing an in-flight task immediately after a rebase/pull/merge without reading the incoming diff.
- Treating "no conflict markers" as proof the integration is safe to ignore.
- Reading only the commit subject lines (`git log --oneline`) and skipping the actual diff content.
- Assuming a fast-forward is inherently safe because it involved no merge commit.
- Adding every incoming path to the actor-owned file-touch ledger without subsequently mutating it.
- Trusting verification completed against the old `HEAD` after its inputs changed.

## Examples

### PASS: Reviewing impact before resuming

```
Agent: Rebased onto origin/main — 4 commits landed.

Reading diff:
  git diff ORIG_HEAD..HEAD

Found: repo-governance/development/quality/code.md now requires an additional
pre-commit check that my current task's new script doesn't yet satisfy.

Adjusting: updating the plan step and script, leaving untouched incoming paths
off my ledger, and rerunning the invalidated governance check before continuing.
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

### FAIL: Pulling then pushing without impact reconciliation

```text
Agent: Pulled with rebase and the history is linear.

Pushing now.
```

The linear history proves topology only. It does not prove that the incoming diff preserved the
task's assumptions or the validity of checks run against the previous `HEAD`.
