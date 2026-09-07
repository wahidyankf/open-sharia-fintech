---
description: "Separates runtime code coverage from static scenario and adapter coverage"
when_to_use: "Use when assigning coverage work to a test or coverage target."
---

# Runtime and Static Coverage Responsibilities

`test:unit`, `test:integration`, and `test:e2e` execute tests. When a runtime layer measures code
coverage, its native instrumentation and threshold belong to that same runtime target.

`test:coverage:*` has a different meaning: it statically validates whether tests cover the
canonical scenario/adapter contract. It must not start a test runner, invoke another runtime target,
or require a prior runtime report. `test:coverage` only aggregates these static validators, and
every applicable validator is mandatory in `test:quick`.

Never satisfy either responsibility with a no-op, hardcoded count, stale report, or exclusion that
leaves behaviour without an owning proof.

A Unit numeric exclusion must enumerate a whole boundary file or a narrow boundary function and
name the Integration or E2E runtime proof that exercises it. Broad path globs, mixed core-logic
exclusions, and unproved boundary code are coverage gaming.
