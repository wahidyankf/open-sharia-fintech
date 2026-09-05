---
title: "The Red-Green-Refactor Cycle"
description: The three-step Red/Green/Refactor loop every code change follows under TDD.
category: explanation
subcategory: development
tags:
  - development
  - workflow
  - tdd
  - testing
  - red-green-refactor
created: 2026-05-02
when_to_use: Use as the canonical definition of the Red-Green-Refactor loop before implementing any code change.
---

# The Red-Green-Refactor Cycle

Every code change follows this loop:

1. **Red** — Write a failing test that captures the desired behaviour. Run it and confirm it fails
   for the right reason (not due to a syntax error, missing import, or wrong test setup). A test
   that fails for the wrong reason is not a useful test.
2. **Green** — Write the minimum production code that makes the failing test pass without a
   hardcoded outcome, literal-success sentinel, or production bypass. Do not add behaviour beyond
   what the scenario requires.
3. **Refactor** — With all tests green, improve the implementation: remove duplication, improve
   names, extract functions, apply clean-code principles. Tests must remain green after every
   refactor step. If they go red during refactoring, that is a bug introduced by the refactor, not
   a deliberate failure.

Repeat the cycle for the next behaviour and applicable adapter.
