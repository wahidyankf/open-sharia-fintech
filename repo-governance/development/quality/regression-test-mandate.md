---
description: Blocking rule requiring every bug fix to land with a reproducing test in the same commit/PR -- the bug-driven dual of Feature Change Completeness
when_to_use: "Use when landing a bug fix and deciding what reproducing test it must include."
---

# Regression Test Mandate

A bug fix is **not complete** until it lands with a test that would have failed before the fix and passes after it. No exceptions. A fixed bug that lacks a pinning test is only temporarily absent -- it will recur.

## Documents

- [Principles and Conventions Implemented/Respected](./regression-test-mandate/principles-and-conventions-implemented-respected.md) — Principles and conventions this mandate implements. Use when tracing this mandate to the principles/conventions behind it.
- [The Rule](./regression-test-mandate/the-rule.md) — The blocking rule: every fix needs a reproducing test in the same commit/PR, no exemptions. Use when you need the exact wording of the mandate.
- [Motivating Example](./regression-test-mandate/motivating-example.md) — The bug batch that motivated this mandate. Use when you need the rationale behind this mandate.
- [Test Form by Defect Type](./regression-test-mandate/test-form-by-defect-type.md) — Required test form per defect type: behavioural, visual, content, integration. Use when deciding what kind of test a defect type requires.
- [Never guard coverage with a hardcoded count](./regression-test-mandate/never-guard-coverage-with-a-hardcoded-count.md) — Derive a coverage guard's expected set from the source of truth, never a magic count. Use when writing a test asserting "nothing escaped the check".
- [Relationship to Feature Change Completeness](./regression-test-mandate/relationship-to-feature-change-completeness.md) — How this mandate and Feature Change Completeness divide obligations. Use when deciding which rule(s) a change needs.
- [Two Paths: With a Plan and Without a Plan](./regression-test-mandate/two-paths-with-a-plan-and-without-a-plan.md) — How the mandate binds a direct fix versus a planned fix. Use when a bug fix has a plan doc and needs a tracked test step.
- [Enforcement](./regression-test-mandate/enforcement.md) — Which agents enforce this mandate and at what severity. Use when you need to know which agent flags a missing test.
- [Completeness Checklist](./regression-test-mandate/completeness-checklist.md) — Checklist before declaring a bug fix complete. Use as a final check before declaring a bug fix done.
- [Examples](./regression-test-mandate/examples.md) — Worked PASS/FAIL examples for this mandate. Use when you need a concrete pass/fail example.
- [Related Documentation](./regression-test-mandate/related-documentation.md) — Cross-references to related testing and sync conventions. Use when you need a related convention on testing or specs sync.
