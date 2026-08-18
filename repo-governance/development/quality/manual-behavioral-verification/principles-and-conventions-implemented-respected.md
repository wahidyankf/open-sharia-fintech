---
title: "Principles and Conventions Implemented/Respected"
description: "Principles/conventions this convention implements."
category: explanation
subcategory: development
tags:
  - verification
  - testing
  - playwright
  - api
  - quality
  - manual-testing
created: 2026-04-04
when_to_use: "Use when tracing this convention's rationale."
---

# Principles and Conventions Implemented/Respected

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md)**: Manual verification forces the implementer to observe the actual behavior of the system, not just trust that tests passed. This deliberate observation step catches integration issues, visual regressions, and behavioral mismatches that automated tests may not cover.

- **[Root Cause Orientation](../../../principles/general/root-cause-orientation.md)**: Bugs that reach production often stem from skipping manual verification. The root cause is not inadequate tests -- it is the absence of a human or agent observing the actual behavior before declaring the work complete. This convention addresses that root cause directly.

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: The verification step is an explicit, required action in the implementation workflow. It is not assumed to have happened because tests passed. The evidence of verification (screenshots, console output, API responses) makes the check visible and auditable.

## Conventions Implemented/Respected

This practice implements/respects the following conventions:

- **[Three-Level Testing Standard](.././three-level-testing-standard.md)**: Manual verification supplements the three automated testing levels (unit, integration, E2E). It does not replace any of them. All three levels plus manual verification form the complete quality assurance picture.

- **[Code Quality Convention](.././code.md)**: Automated quality gates (typecheck, lint, test:quick) catch code-level issues. Manual verification catches behavioral issues that survive those gates. Together they form a complete quality boundary.

- **[Evidence Capture Convention](.././evidence-capture.md)**: Manual verification must leave a committed record — screenshots in the plan's `evidence/` subfolder, curl outputs inline in `delivery.md`. "Verified manually" without a record is incomplete.
