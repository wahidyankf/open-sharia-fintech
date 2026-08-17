---
title: "Regression Test Mandate"
description: "Blocking rule requiring every bug fix to land with a reproducing test in the same commit/PR -- the bug-driven dual of Feature Change Completeness"
when_to_use: "Read this index to find the right Regression Test Mandate child document."
---

# Regression Test Mandate

- [Principles and Conventions Implemented/Respected](./01-principles-and-conventions-implemented-respected.md) — Principles and conventions this mandate implements. Use when tracing this mandate to the principles/conventions behind it.
- [The Rule](./02-the-rule.md) — The blocking rule: every fix needs a reproducing test in the same commit/PR, no exemptions. Use when you need the exact wording of the mandate.
- [Motivating Example](./03-motivating-example.md) — The bug batch that motivated this mandate. Use when you need the rationale behind this mandate.
- [Test Form by Defect Type](./04-test-form-by-defect-type.md) — Required test form per defect type: behavioral, visual, content, integration. Use when deciding what kind of test a defect type requires.
- [Never guard coverage with a hardcoded count](./05-never-guard-coverage-with-a-hardcoded-count.md) — Derive a coverage guard's expected set from the source of truth, never a magic count. Use when writing a test asserting "nothing escaped the check".
- [Relationship to Feature Change Completeness](./06-relationship-to-feature-change-completeness.md) — How this mandate and Feature Change Completeness divide obligations. Use when deciding which rule(s) a change needs.
- [Two Paths: With a Plan and Without a Plan](./07-two-paths-with-a-plan-and-without-a-plan.md) — How the mandate binds a direct fix versus a planned fix. Use when a bug fix has a plan doc and needs a tracked test step.
- [Enforcement](./08-enforcement.md) — Which agents enforce this mandate and at what severity. Use when you need to know which agent flags a missing test.
- [Completeness Checklist](./09-completeness-checklist.md) — Checklist before declaring a bug fix complete. Use as a final check before declaring a bug fix done.
- [Examples](./10-examples.md) — Worked PASS/FAIL examples for this mandate. Use when you need a concrete pass/fail example.
- [Related Documentation](./11-related-documentation.md) — Cross-references to related testing and sync conventions. Use when you need a related convention on testing or specs sync.
