---
title: "Verification Before Done"
description: "Defines the verification requirements before marking a task done, for different task types, and how to compare diffs and behavior."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - workflow
  - orchestration
created: 2025-11-23
when_to_use: Use before reporting any task complete, to confirm what still needs verifying.
---

# Verification Before Done

Never declare a task complete without proving it works.

## Verification Requirements

Before marking any task complete:

1. **Run the relevant tests** - If code changed, tests must pass
2. **Check logs for errors** - Silent failures are still failures
3. **Demonstrate the behavior** - Show that the output matches the requirement, not just that the code was written
4. **Apply the senior engineer test** - Ask "would a senior engineer approve this?" If not, keep working

## Verification for Different Task Types

| Task Type            | Verification Method                                         |
| -------------------- | ----------------------------------------------------------- |
| Code change          | Run `nx run [project]:test:quick`, check no regressions     |
| Documentation update | Verify links work, content renders correctly                |
| Bug fix              | Show the failing test now passes; existing tests still pass |
| Refactor             | All tests pass before and after; behavior unchanged         |
| New feature          | Tests cover the new behavior; edge cases handled            |

## Diffs and Behavior Comparison

When a change might have unintended side effects, compare behavior before and after. This is especially relevant for:

- Changes to shared utilities used by many consumers
- Changes to configuration that affects build or test behavior
- Refactors touching core logic
