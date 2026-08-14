---
title: "Proactive Preexisting Error Resolution — Scope Judgment"
description: How to size a discovered preexisting-error fix as small (fix inline), medium (its own commit in the current session), or large (a plan)
category: explanation
subcategory: development
tags:
  - root-cause
  - quality
  - preexisting-errors
  - proactive
  - bug-fixing
  - ai-agents
created: 2026-03-28
when_to_use: Use when deciding how big a change to make in response to a discovered preexisting error.
---

# Scope Judgment

## Small Fixes (fix inline)

These require no separate commit and no deliberation:

- Broken links in documentation
- Incorrect or outdated configuration values
- Dead imports or unused variables created by a previous refactor
- Typos in error messages or comments
- Minor validation gaps (empty string edge cases, null checks)

Fix these as part of your current work. They take seconds to minutes.

## Medium Fixes (fix in a separate commit)

These warrant their own commit but belong in the current session:

- Broken tests (failing or flaking)
- Incorrect implementations that produce wrong results on valid inputs
- Incorrect contracts between modules
- Environment configuration that fails on standard inputs

Fix these within the current session. Write a commit message that references the preexisting bug, for example: `fix(user-service): validate empty strings in user input (preexisting bug)`.

## Large Fixes (create a plan and execute it)

These require more than a single commit:

- Architectural problems where the wrong abstraction is used throughout a module
- Systemic configuration issues affecting multiple services
- Test suites with fundamental structural problems (testing implementation instead of behavior)

Create a plan in `plans/in-progress/` and begin executing it. The presence of a plan does not defer the work — it organizes it. Execution starts immediately.
