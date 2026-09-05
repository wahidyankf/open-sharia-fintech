---
title: "Examples"
description: One PASS and three FAIL examples of agent behaviour around force-push and --no-verify approval.
category: explanation
subcategory: development
tags:
  - git
  - workflow
  - safety
  - automation
  - human-approval
created: 2026-03-30
when_to_use: Use when checking whether a specific agent transcript around a force-push or --no-verify complies with this convention.
---

# Examples

## PASS: Correct agent behaviour

```
Agent: I need your explicit approval before running:

  git push --force-with-lease origin feature/auth

Reason: the local branch was rebased onto main to resolve a conflict.
Remote tip: abc1234. Local tip after rebase: def5678.
The rebase replaces 3 commits with 3 rewritten equivalents.

Do you want to proceed?

User: yes

Agent: Running git push --force-with-lease origin feature/auth...
```

## FAIL: Incorrect agent behaviour — executing without approval

```
Agent: Rebasing is complete. Pushing with --force-with-lease.
[runs git push --force-with-lease without asking]
```

## FAIL: Incorrect agent behaviour — reusing prior approval

```
User: [earlier] Yes, go ahead with the force-push.
Agent: [30 minutes later, different situation] Reusing your earlier approval
       to run git push --force again.
```

## FAIL: Incorrect agent behaviour — treating --no-verify as routine

```
Agent: The pre-push hook is taking too long. Running with --no-verify
       to skip it and save time.
[runs git push --no-verify without asking]
```
