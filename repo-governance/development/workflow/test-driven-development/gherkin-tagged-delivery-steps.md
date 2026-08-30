---
title: "Gherkin-Tagged Delivery Steps"
description: How detailed outcome sections reference canonical Gherkin without duplicating full scenarios in delivery.md.
category: explanation
subcategory: development
tags:
  - development
  - workflow
  - tdd
  - testing
  - red-green-refactor
created: 2026-05-02
when_to_use: Use when writing detailed code delivery steps for a plan with companion Gherkin specs.
---

# Gherkin-Tagged Delivery Steps

A behavior-implementing outcome section names every acceptance criterion it binds by stable ID or
exact scenario title and links the canonical `prd.md` or `specs/**` source. `delivery.md` never
copies the full `Given/When/Then`; duplicated scenarios drift.

A section may bind multiple scenarios when their actions are inseparable and one observable outcome
and proof boundary accepts or rejects them together. Otherwise split them into separate outcome
sections. Pure-core tests may use `Gherkin (underpins)` and aggregate BDD binders may name all
consumed scenarios; both still reference, rather than copy, the canonical scenarios.

**Two exceptions** keep a multi-scenario tag (a `;`-separated title list) and are **not** split
one-cycle-per-scenario:

- **Pure-core (`underpins`) steps** — data/calculation unit tests that supply the math or data many
  scenarios rely on without binding any single scenario's steps. Tag them
  `**Gherkin (underpins) →** "<title>"; …` listing the scenarios they support.
- **Aggregate BDD binders** — a feature-consuming unit test or `playwright-bdd` step-definition file
  that consumes the **whole** `.feature` for `specs:coverage` / E2E. Tag with the scenarios it binds;
  it is one step, not one-per-scenario.

**Scope**: applies to plans touching `apps/` or `libs/` that carry companion `specs/`
Gherkin (ties to the
[Specs & Gherkin two-path completeness rule](../../quality/feature-change-completeness.md)).
Exempt: pure refactors, docs/governance-only plans, and non-code delivery steps.

**PASS example**:

```markdown
### AC-PRICING-04 — A percentage discount produces the contracted final price

- **Input:** [AC-PRICING-04 "10% discount reduces price"](../prd.md#acceptance-criteria).
- **Outcome:** the final price matches the canonical scenario.
- [ ] [AI] **RED:** [exact calculation test/path/command/expected failure].
- [ ] [AI] **GREEN:** [exact implementation symbol/path/command/expected pass].
- [ ] [AI] **REFACTOR:** [exact pricing-helper cleanup/regression command/invariant].
- **Proof:** recorded RED failure and `rtk nx run organiclever-app-web:test:unit` passes.
```

**FAIL examples** (each a HIGH finding):

- A behavior outcome section with no canonical scenario reference.
- Full Gherkin copied into `delivery.md`.
- Multiple independently verifiable behaviors hidden in one section.

`plan-checker` flags both as **HIGH** findings.

For more on Gherkin format and the step-keyword cardinality rule, see the
[Acceptance Criteria Convention](../../infra/acceptance-criteria.md).
For the two-path completeness rule that governs when this requirement applies, see
[Feature Change Completeness](../../quality/feature-change-completeness.md).
