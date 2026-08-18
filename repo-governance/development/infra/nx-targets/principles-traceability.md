---
title: "Principles Traceability"
description: Maps each major Nx target design decision to the software-engineering principle it implements.
category: explanation
subcategory: development
tags:
  - nx
  - targets
  - project-json
  - build
  - scripts
created: 2026-02-23
when_to_use: Use when writing a rationale section that needs to cite which principle a target-design decision satisfies.
---

# Principles Traceability

| Decision                                                                                                                                                                                    | Principle                                                                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Consistent target names across all projects                                                                                                                                                 | [Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md) |
| `typecheck`, `lint`, `test:quick` (which includes `test:unit`, `test:coverage`, `test:specs`) enforced identically at pre-push and the PR gate; `test:integration` and `test:e2e` CRON-only | [Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md) |
| Mandatory-six echo-placeholder rule ensures every project participates in workspace-wide `nx affected -t <target>` with no special-casing                                                   | [Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md) |
| Minimum required targets per project type; echo placeholders preferred over target omission                                                                                                 | [Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)      |
| `outputs` required for cacheable targets                                                                                                                                                    | [Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md) |
| Four-dimension tag scheme with controlled vocabulary declared in every `project.json`                                                                                                       | [Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md) |
