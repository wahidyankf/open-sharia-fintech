---
title: "Feature Change Completeness Convention"
description: Practice requiring all related specs, contracts, tests, and documentation to be updated as part of any feature change -- binding both the direct-code path and the plan path
category: explanation
subcategory: development
tags:
  - feature-completeness
  - specs
  - contracts
  - testing
  - documentation
  - quality
created: 2026-04-04
when_to_use: "Use when landing a feature change and deciding which companion artifacts it must also update."
---

# Feature Change Completeness Convention

This convention requires every feature change to land with all its related specs, contracts, tests, and documentation updated in the same commit or PR -- whether the change is made directly or through a plan.

## Documents

- [Principles and Conventions Implemented/Respected](./feature-change-completeness/principles-and-conventions-implemented-respected.md) — Principles and conventions this convention implements. Use when tracing this convention to the principles/conventions behind it.
- [The Rule](./feature-change-completeness/the-rule.md) — The rule: every feature change lands with all related specs, contracts, tests, and docs updated. Use when you need the exact wording of the feature-change-completeness rule.
- [Two Paths: With a Plan and Without a Plan](./feature-change-completeness/two-paths-with-a-plan-and-without-a-plan.md) — How this rule binds a direct code change versus a change made through a plan document. Use when a feature change has a plan doc and you need to know how completeness is tracked.
- [What Must Be Updated](./feature-change-completeness/what-must-be-updated.md) — The full list of artifact types (specs, contracts, tests, docs) a feature change must keep in sync. Use when unsure which companion artifact a feature change must also update.
- [The Completeness Checklist](./feature-change-completeness/the-completeness-checklist.md) — The checklist to verify before declaring a feature change complete. Use as a final check before declaring a feature change done.
- [What This Applies To](./feature-change-completeness/what-this-applies-to.md) — The kinds of changes this convention covers and does not cover. Use when deciding whether a specific change falls under this convention.
- [Examples](./feature-change-completeness/examples.md) — Worked examples of feature changes and their required companion artifacts. Use when you need a concrete example of what a feature change must update.
- [Scope](./feature-change-completeness/scope.md) — The boundary of this convention, including the plans/ exception and its Two Paths cross-reference. Use when checking whether this convention's scope covers a specific directory or artifact.
- [Tools and Automation](./feature-change-completeness/tools-and-automation.md) — The agents and checks that enforce feature-change completeness. Use when locating the automated check for a feature-completeness violation.
- [Related Documentation](./feature-change-completeness/related-documentation.md) — Cross-references to related testing, specs-sync, and regression conventions. Use when you need a related convention on testing, specs sync, or regressions.
