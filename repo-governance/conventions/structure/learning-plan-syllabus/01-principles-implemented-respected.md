---
title: "Learning-Plan Syllabus: Principles Implemented/Respected"
description: The four core principles this convention implements — documentation-first deliverables, explicit triggers and ownership, a copy-paste template over a new directory, and a re-derivable measured tiering method.
when_to_use: Read this to understand why the syllabus convention is shaped the way it is before applying its rules to a specific plan.
category: explanation
subcategory: conventions
tags:
  - plans
  - syllabus
  - learning-bearing
  - custody
  - governance
created: 2026-07-22
---

# Learning-Plan Syllabus: Principles Implemented/Respected

Part of the [Learning-Plan `syllabus/` Folder Convention](../learning-plan-syllabus.md).

This convention implements the following core principles:

- **[Documentation First](../../../principles/content/documentation-first.md)**: `syllabus/README.md`,
  `syllabus/courses/README.md`, and `syllabus/paths/README.md` are REQUIRED deliverables for a new
  corpus, not an afterthought — documenting a learning corpus is a first-class delivery output,
  mirroring how the UI-design-funnel record is a required part of a UI-bearing plan's `prd.md`.
- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: the
  learning-bearing trigger is defined by delivery effect and illustrated with worked positive and
  negative examples, so whether a given plan is in scope is decidable without a judgment call. The
  `## Corpus Disposition` declaration and the `**Custodian**` line make ownership and lifecycle
  explicit in the plan's own files rather than left to institutional memory.
- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: the
  course template ships as a single copy-paste fenced block inside this convention, following the
  repo's established pattern (the two-pager template in `plans.md`, the UI funnel's copy-paste
  example in `diagrams.md`), rather than inventing a new `templates/` directory.
- **[Reproducibility First](../../../principles/software-engineering/reproducibility.md)**: the section
  tiers below are derived from a stated, re-runnable measurement over the existing corpus, not
  designed from intuition — a later author with a larger corpus can re-derive the tiers using the
  same method and get a defensible answer, not inherit a frozen list.
