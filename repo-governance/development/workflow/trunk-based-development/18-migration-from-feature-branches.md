---
title: "Migration from Feature Branches"
description: Mindset shifts, transition steps, and common concerns addressed when moving a team from GitFlow/GitHub Flow to TBD.
category: explanation
subcategory: development
tags:
  - trunk-based-development
  - git
  - workflow
  - development
  - continuous-integration
created: 2025-11-26
when_to_use: Use when transitioning a team that is used to a feature-branch workflow to TBD.
---

# Migration from Feature Branches

If you're used to feature-branch workflows (GitFlow, GitHub Flow), here's how to transition:

## Mindset Shifts

| Feature Branch Mindset              | TBD Mindset                                             |
| ----------------------------------- | ------------------------------------------------------- |
| "I'll merge when feature is done"   | "I'll commit daily, hide with feature flag until done"  |
| "My branch is my workspace"         | "`main` is everyone's workspace"                        |
| "Integration happens at merge time" | "Integration happens continuously"                      |
| "Branches isolate risk"             | "Feature flags and tests manage risk"                   |
| "Review before merge"               | "Review can happen post-commit (or via short-lived PR)" |

## Transition Steps

1. **Start small**: Pick a simple task and take it through one short-lived branch and PR end to end
2. **Use feature flags**: Hide incomplete work, so no branch stays open to hide it
3. **Integrate frequently**: Land work multiple times per day; measure branch _lifespan_, not count
4. **Keep CI green**: Fix failures immediately
5. **Review old habits**: Notice when a branch starts outliving its plan

## Common Concerns Addressed

**"What if I break `main`?"**

- PASS: Tests and CI catch most issues before push
- PASS: Rapid revert if something slips through
- PASS: Feature flags hide incomplete features

**"What if I need to work on multiple things?"**

- PASS: Finish one thing before starting another
- PASS: Use feature flags to work incrementally
- PASS: Commit small pieces, don't wait for "done"

**"What about code review?"**

- PASS: Review can happen post-commit (async)
- PASS: Or use very short-lived PR branches (< 1 day)
- PASS: Pair/mob programming provides real-time review

**"What if I'm not confident in my code?"**

- PASS: Write tests first (TDD)
- PASS: Use feature flags to isolate risk
- PASS: Commit small changes, easier to verify
