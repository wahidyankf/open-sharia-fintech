---
title: "Principles and Conventions Implemented/Respected"
description: "Principles and conventions this mandate implements."
category: explanation
subcategory: development
tags:
  - regression
  - testing
  - bug-fix
  - quality
  - gherkin
  - specs
created: 2026-06-22
when_to_use: "Use when tracing this mandate to the principles/conventions behind it."
---

# Principles and Conventions Implemented/Respected

## Principles Implemented/Respected

- **[Root Cause Orientation](../../../principles/general/root-cause-orientation.md)**: A bug that
  recurs is a bug whose fix was never pinned. The root cause of recurring bugs is not developer
  carelessness -- it is a workflow that accepts fixes without requiring proof that the defect
  cannot re-enter the codebase silently. This mandate addresses that root cause: every fix must
  leave behind a sentinel.

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**:
  "I fixed it" is an implicit claim. A test that fails on the unfixed code and passes on the
  fixed code is an explicit, machine-verifiable claim. The mandate converts the implicit
  assertion into an auditable artifact.

- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**:
  Human re-verification of previously fixed bugs does not scale. A regression test suite that
  exercises every pinned fix verifies the entire fix history on every CI run -- automatically,
  without human attention.

- **[Reproducibility First](../../../principles/software-engineering/reproducibility.md)**: A
  reproducing test makes the bug deterministically observable. Before the fix, the test fails
  repeatably. After the fix, it passes repeatably. This determinism is what makes the fix
  auditable and the regression detectable.

## Conventions Implemented/Respected

- **[Feature Change Completeness Convention](.././feature-change-completeness.md)**: That convention
  requires all related specs, contracts, tests, and documentation to accompany a _feature change_.
  This mandate is its bug-driven dual: a _fix_ is not complete without a _reproducing test_. The
  two rules together cover the full space -- no behaviour change (new, modified, or restored) lands
  without companion artifacts. See [Relationship to Feature Change Completeness](./relationship-to-feature-change-completeness.md).

- **[Behaviour-Driven Development](../../behaviour-driven-development.md)**: The reproducing test must
  slot into the appropriate level -- unit for logic defects, integration for persistence/boundary
  defects, E2E for full-stack or user-facing defects -- following the isolation rules of that level.

- **[Code Quality Convention](.././code.md)**: Fast gates run Unit plus every applicable static
  coverage validator through `test:quick`; scheduled CI runs the full Integration and E2E suites.
  The pinning test must pass its applicable runtime and coverage gates before the fix lands.
