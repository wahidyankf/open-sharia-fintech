---
title: "Gherkin-Tagged Delivery Steps"
description: Why one RED-GREEN-REFACTOR cycle binds exactly one Gherkin scenario, the required tag-line format, the two exceptions, and PASS/FAIL examples.
category: explanation
subcategory: development
tags:
  - development
  - workflow
  - tdd
  - testing
  - red-green-refactor
created: 2026-05-02
when_to_use: Use when writing a RED step for a plan touching apps/ or libs/ with companion Gherkin specs.
---

# Gherkin-Tagged Delivery Steps

A behavior-implementing delivery cycle targets **exactly one Gherkin scenario**. Split work so
that each `RED → GREEN → REFACTOR` cycle implements a single scenario — never bundle multiple
scenarios into one RED (or one GREEN, or one REFACTOR). Long, granular checklists are expected and
preferred over a few broad steps.

Each such cycle's RED step MUST carry, in two parts:

1. A **tag line** naming the one scenario: `**Gherkin (binds) →** "<Scenario title>"`.
2. That scenario's **complete `Given/When/Then`** inline as a fenced ` ```gherkin ` block
   immediately under the step — copied **verbatim** from the companion `.feature` file (itself
   mirrored verbatim from `prd.md §Acceptance Criteria`). The `.feature` is the source of truth if
   they ever diverge.

The matching GREEN step implements only the slice that makes that one scenario pass; the REFACTOR
step tidies that slice. Because each scenario gets its own cycle, its full `Given/When/Then` appears
exactly once — in that cycle's RED step.

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

**PASS example** — one RED step bound to exactly one scenario:

````markdown
- [ ] [AI] **RED**: Write failing test for discount calculation in
      `apps/organiclever-app-web/src/features/pricing/core/discount.test.ts`
      — command: `nx run organiclever-app-web:test:unit`
      — acceptance: test fails with `TypeError: calculateDiscount is not a function`

  **Gherkin (binds) →** "10% discount reduces price"

  ```gherkin
  Scenario: 10% discount reduces price
    Given a product priced at 100
    When a 10% discount is applied
    Then the final price should be 90
  ```
````

**FAIL examples** (each a HIGH finding):

- A behavior RED step whose `**Gherkin (binds) →**` tag lists **more than one** scenario — split it
  into one cycle per scenario.
- A behavior RED step missing its tag line, or whose inline `Given/When/Then` block is absent or not
  verbatim-equal to the companion `.feature`.

`plan-checker` flags both as **HIGH** findings.

For more on Gherkin format and the step-keyword cardinality rule, see the
[Acceptance Criteria Convention](../../infra/acceptance-criteria.md).
For the two-path completeness rule that governs when this requirement applies, see
[Feature Change Completeness](../../quality/feature-change-completeness.md).
