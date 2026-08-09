---
title: "Regression Test Mandate"
description: Blocking rule requiring every bug fix to land with a reproducing test in the same commit/PR -- the bug-driven dual of Feature Change Completeness
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
---

# Regression Test Mandate

A bug fix is **not complete** until it lands with a test that would have failed before the fix
and passes after it. No exceptions. A fixed bug that lacks a pinning test is only temporarily
absent -- it will recur.

## Principles Implemented/Respected

- **[Root Cause Orientation](../../principles/general/root-cause-orientation.md)**: A bug that
  recurs is a bug whose fix was never pinned. The root cause of recurring bugs is not developer
  carelessness -- it is a workflow that accepts fixes without requiring proof that the defect
  cannot re-enter the codebase silently. This mandate addresses that root cause: every fix must
  leave behind a sentinel.

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**:
  "I fixed it" is an implicit claim. A test that fails on the unfixed code and passes on the
  fixed code is an explicit, machine-verifiable claim. The mandate converts the implicit
  assertion into an auditable artifact.

- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)**:
  Human re-verification of previously fixed bugs does not scale. A regression test suite that
  exercises every pinned fix verifies the entire fix history on every CI run -- automatically,
  without human attention.

- **[Reproducibility First](../../principles/software-engineering/reproducibility.md)**: A
  reproducing test makes the bug deterministically observable. Before the fix, the test fails
  repeatably. After the fix, it passes repeatably. This determinism is what makes the fix
  auditable and the regression detectable.

## Conventions Implemented/Respected

- **[Feature Change Completeness Convention](./feature-change-completeness.md)**: That convention
  requires all related specs, contracts, tests, and documentation to accompany a _feature change_.
  This mandate is its bug-driven dual: a _fix_ is not complete without a _reproducing test_. The
  two rules together cover the full space -- no behavior change (new, modified, or restored) lands
  without companion artifacts. See [Relationship to Feature Change Completeness](#relationship-to-feature-change-completeness).

- **[Three-Level Testing Standard](./three-level-testing-standard.md)**: The reproducing test must
  slot into the appropriate level -- unit for logic defects, integration for persistence/boundary
  defects, E2E for full-stack or user-facing defects -- following the isolation rules of that level.

- **[Code Quality Convention](./code.md)**: Automated quality gates (typecheck, lint, test:quick,
  specs:coverage) run the full regression suite on every push. The pinning test must pass those
  gates in CI before the fix lands.

## The Rule

**Every fix for a discovered bug or regression MUST land with a test that reproduces the defect
in the SAME commit or PR as the fix.**

The reproducing test must:

1. **Fail** on the code as it existed before the fix (or be clearly written to target the
   defect condition -- for new code paths, document the scenario explicitly in the test description).
2. **Pass** on the fixed code.
3. **Continue to pass** on every future build without manual attention.

This rule is **BLOCKING**. There are **no exemptions** -- not for trivial fixes, not for cosmetic
defects, not for "obvious" one-liners, not for hotfixes. The form of the test adapts to the
defect type (see [Test Form by Defect Type](#test-form-by-defect-type)), but the obligation to
write one does not.

## Motivating Example

The cost-of-living calculator work is the concrete case that motivated this mandate. Every bug
found during that work -- the savings tab ignoring the geographic filter, inputs not persisted
in the URL, a redundant UI panel, a hidden toggle that controlled visible output, a jargon label,
and a USD-only currency input -- was converted into a Gherkin scenario so it could not return.
Before that conversion, each bug was "fixed" but free to recur because no automated check
asserted the corrected behavior.

This mandate generalizes that practice into a standing rule: every bug found anywhere becomes
a pinned scenario that cannot be silently broken again.

## Test Form by Defect Type

The obligation is uniform; the form adapts:

| Defect type                         | Required test form                                                                                                                                                                                                  |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Behavioral / functional**         | A Gherkin scenario in `specs/**` (preferred) expressing the correct behavior -- plus the unit, integration, or E2E test that consumes it per the [Three-Level Testing Standard](./three-level-testing-standard.md). |
| **Visual / design / UI regression** | A DOM assertion, a computed-style assertion, a Playwright snapshot assertion, or a Gherkin scenario capturing the on-design expectation -- whichever level can assert the specific visual property that was wrong.  |
| **Content / copy / i18n**           | A test asserting the corrected string, translation key, or rendered text -- at the unit level if the string is in logic, at E2E level if it is rendered.                                                            |
| **Integration / API regression**    | An integration or E2E test asserting the correct response shape, status code, or state transition.                                                                                                                  |

The common thread: the test must make the specific defect _impossible to silently reintroduce_.
A test that passes even on the broken version does not satisfy this mandate.

### Never guard coverage with a hardcoded count

When a test asserts "nothing escaped the check", express that as an equality against a **derived
set**, never as a count of members. A magic number fails in exactly the wrong direction on both
sides: it fails **open** in the case that matters (add a command to a target the guard never reads
and the count can still be made to match) and **closed** in the case that does not (any legitimate
restructure trips it).

A real instance: an isolation guard asserted
`assert_eq!(commands.len(), 9, "seven serialized unit commands plus integration and coverage")`. A
later change legitimately collapsed six `cargo test --test X` invocations into one; the guard went
red at 4, reporting a defect where there was only a restructure. The property the guard actually
cared about — every inspected command starts with `env -u GIT_DIR -u GIT_WORK_TREE -u
GIT_COMMON_DIR` — was already asserted on the line above. The count was a proxy for _coverage_: that
the inspected set is the whole set.

The fix is to derive that set from the same source of truth the production code reads — here, an
equality against every `cargo test` / `cargo llvm-cov` string found by scanning all of
`project.json`. It cannot go stale on restructuring, and unlike the count it genuinely fails when a
new direct Cargo command is added to a target the guard does not inspect.

**Whenever a test asserts "how many", ask what set it is really asserting membership of, and derive
that set.**

## Relationship to Feature Change Completeness

[Feature Change Completeness](./feature-change-completeness.md) asks: _does this feature change
land with all its companion artifacts?_ This mandate asks: _does this bug fix land with a
reproducing test?_

They are complementary, not overlapping:

| Work type                     | Governing rule              | Artifact required                                   |
| ----------------------------- | --------------------------- | --------------------------------------------------- |
| New or modified feature       | Feature Change Completeness | Gherkin specs + contracts + tests + documentation   |
| Bug fix (spec was correct)    | **This mandate**            | Reproducing test only (spec was already right)      |
| Bug fix (spec was also wrong) | Both rules                  | Updated spec + reproducing test + related artifacts |

The table in Feature Change Completeness that reads _"Bug fix that matches existing spec → Tests
only (add regression test)"_ is the same obligation stated at a higher level of abstraction.
This document makes that obligation explicit, names it, and declares it BLOCKING.

## Two Paths: With a Plan and Without a Plan

Like Feature Change Completeness, this mandate binds both paths a fix can take:

1. **Direct fix (no plan doc)**: The reproducing test MUST be added in the same commit or PR
   as the fix. The `swe-code-checker` agent flags a code fix that lacks a companion reproducing
   test. This is the same enforcement path used for missing Gherkin specs under Feature Change
   Completeness.

2. **Planned fix (plan doc)**: Any bug-fix plan MUST include an explicit delivery-checklist step
   that adds the reproducing test. The step must name the test file and describe the scenario it
   pins. `plan-maker` emits this step; `plan-checker` flags its absence. The test is then written
   -- and verified -- when the plan executes.

## Enforcement

This mandate is enforced by the same infrastructure that enforces the specs+Gherkin two-path rule:

- **`swe-code-checker`**: Flags a code fix (a diff that removes a defect condition) that lands
  without a companion test asserting the corrected behavior. Finding severity: **HIGH**.
- **`plan-maker`**: Emits a regression-test delivery step in every bug-fix plan. The step names
  the test file path, the scenario description, and the `Given/When/Then` trigger that would have
  reproduced the bug.
- **`plan-checker`**: Flags a bug-fix plan that lacks a regression-test delivery step. Finding
  severity: **HIGH**.

Neither the agent definitions nor their prompts are edited here -- this document records that
those agents are the enforcers and what they must flag.

## Completeness Checklist

Before declaring a bug fix complete, verify:

- [ ] A test exists that targets the specific defect condition (not a general "happy path" test
      that happened to pass even when broken).
- [ ] The test is committed in the same PR or commit as the fix (not in a follow-up).
- [ ] The test slots into the correct level per the [Three-Level Testing Standard](./three-level-testing-standard.md).
- [ ] For behavioral/functional defects: a Gherkin scenario in `specs/**` captures the correct
      expectation and the test that consumes it is updated.
- [ ] `test:quick` passes (including `specs:coverage`) after the fix + test are in place.

## Examples

### PASS: Behavioral bug with Gherkin scenario

A developer discovers that the savings tab ignores the geographic filter and shows global
averages instead of city-specific figures.

They fix the filtering logic AND add:

1. A Gherkin scenario in `specs/apps/organiclever/behavior/.../calculator.feature`:

   ```gherkin
   Scenario: Savings tab respects the selected city filter
     Given I have selected "Kuala Lumpur" as my city
     When I navigate to the Savings tab
     Then all figures reflect Kuala Lumpur cost data
     And no global-average figures are shown
   ```

2. A unit test that calls the filter function with a city and asserts the output
   excludes global-average data.

The fix and the scenario land in the same commit. The mandate is satisfied.

### PASS: Visual regression with DOM assertion

A developer discovers that the currency input accepts non-numeric characters in production.
They fix the input validation AND add an E2E test:

```typescript
test("currency input rejects non-numeric characters", async ({ page }) => {
  await page.fill('[data-testid="currency-input"]', "abc");
  await expect(page.locator('[data-testid="currency-input"]')).toHaveValue("");
});
```

Fix + test land in the same commit. The mandate is satisfied.

### FAIL: Fix without a reproducing test

A developer discovers the hidden toggle controls visible output but has no visible affordance.
They add a label to make it discoverable but do not add a test asserting the label exists and
the toggle is accessible. The fix is incomplete -- the label can be removed in a future cleanup
without any automated gate objecting.

### FAIL: Fix in one commit, test in a later PR

A developer fixes a jargon label in commit A and says "I'll add the test in a follow-up PR."
The mandate requires both in the same commit or PR. The fix is incomplete until the test lands.

## Related Documentation

- [Feature Change Completeness Convention](./feature-change-completeness.md) -- The feature-change
  dual of this mandate; together they cover all behavior-altering work
- [Three-Level Testing Standard](./three-level-testing-standard.md) -- Which test level applies
  to which defect type
- [Code Quality Convention](./code.md) -- Automated quality gates that run the regression suite
- [Test-Driven Development Convention](../workflow/test-driven-development.md) -- Red→Green→Refactor
  cycle; a reproducing test is the natural RED step for a bug fix
- [Specs-Application Sync Convention](./specs-application-sync.md) -- Bidirectional sync between
  specs/ and application code; behavioral regression tests belong in specs/
- [Live-Tester Systematic Coverage](./live-tester-systematic-coverage.md) -- How the three live-site
  testers find defects that become inputs to this mandate
