---
title: "Code as Liability"
description: Every line of code is a maintenance liability, so a pull request that adds code states what it buys, what it costs to maintain, and which simpler alternative was rejected
category: explanation
subcategory: development
tags:
  - code-quality
  - maintenance
  - review
  - discipline
created: 2026-08-21
when_to_use: Use when adding code, reviewing a pull request that adds code, or deciding whether a problem should be solved by writing code at all.
---

# Code as Liability

Code is not an asset that accumulates value. Every line must be read, understood, kept working,
migrated, and eventually deleted by someone — often someone who did not write it. **Adding code
creates a permanent obligation; deleting it retires one.**

Changing existing code is unremarkable. _Adding_ to the total requires a reason good enough to
outlast the person who had it, written where the next reader will find it.

## Principles Implemented/Respected

- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: that
  principle governs the _shape_ of code; this practice governs whether it should exist at all.
- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: the
  cheapest fix for maintenance cost is the code never written, which requires deciding before typing.
- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: the
  trade is written down, so a future reader inherits the reasoning and not only the result.

## Conventions Implemented/Respected

- **[Test-Driven Development](../workflow/test-driven-development.md)**: tests and specs are exempt
  here precisely because that convention makes them mandatory; the two never compete.
- **[File-Touch Discipline](./file-touch-discipline.md)**: the structural sibling — that records
  what you changed, this records why the addition earned its place.
- **[File Naming Convention](../../conventions/structure/file-naming.md)** and
  **[Content Quality Principles](../../conventions/writing/quality.md)**: this document follows both.

## Contents

- [What Counts as Code](./code-as-liability/what-counts-as-code.md) — the surfaces this reaches, and the tests-and-specs exemption stated explicitly.
- [The Obligation](./code-as-liability/the-obligation.md) — the three things a pull request body must state, and what a good answer looks like.
- [Scrutiny and Enforcement](./code-as-liability/scrutiny-and-enforcement.md) — how the bar scales with blast radius, and the enforcement disposition.
