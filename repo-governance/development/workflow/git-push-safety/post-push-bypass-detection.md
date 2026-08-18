---
title: "Post-Push Bypass Detection"
description: The post-hoc obligation to read push output for ruleset-bypass language and treat a bypassed required check as a discovered violation.
category: explanation
subcategory: development
tags:
  - git
  - workflow
  - safety
  - automation
  - human-approval
created: 2026-03-30
when_to_use: Use immediately after any git push completes, to check whether branch protection was bypassed.
---

# Post-Push Bypass Detection

A ruleset bypass cannot be pre-approved the way `--force` can: whether a given push will trigger one
depends on server-side branch-protection rules and the pusher's bypass privileges, neither of which
the agent can see in advance. The obligation is therefore post-hoc, not preventive.

After every push, the agent MUST read the push output. If it contains bypass language — for example
`Bypassed rule violations`, `bypassed branch protection`, or an equivalent GitHub ruleset-bypass
notice — the push is not routine, even though no destructive flag was used:

1. Stop treating the push as autonomous-and-done. Do not proceed to the next step as if the pushed
   state passed its required checks.
2. Report to the user, verbatim from the output, which required check or rule was bypassed.
3. Record a written reason in the plan (or the session, if no plan exists) for why the underlying
   check did not run or was not satisfied — the same standard [No Destructive Git
   Operations](../no-destructive-git-operations/no-corner-cutting-and-preferring-additive-operations.md#no-corner-cutting--root-cause-orientation-is-binding)
   already requires for skipping a declared quality gate (see its "skipping a declared quality gate"
   item). A bypassed required status check is exactly that case, discovered after the fact instead of
   before it.
4. Never treat "the push succeeded" as evidence the bypassed check would have passed.
