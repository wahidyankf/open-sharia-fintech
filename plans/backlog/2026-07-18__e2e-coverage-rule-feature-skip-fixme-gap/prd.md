# Product Requirements: E2E Coverage Rule/Feature Skip/Fixme Gap

## Product Overview

Extend the e2e-coverage gap detector's special-tag handling so a `Rule:`- or `Feature:`-level
`@skip`/`@fixme` tag is detected the same way an `Outline:`-level one already is, and refresh the
design-decision documentation for the shipped detector so it matches the current implementation.

## Personas

- **Gherkin author** tagging a `Rule:` or `Feature:` block `@skip`/`@fixme`.
- **rhino-cli maintainer** reading design-decision docs to understand the shipped detector's actual
  behavior.

## User Stories

- As a Gherkin author, I want a `Rule:`-level `@skip`/`@fixme` tag to be correctly detected as unbound
  by the e2e-coverage gate, so the gate's guarantee holds regardless of which Gherkin construct I use.
- As a maintainer, I want the design-decision documentation to reflect every shipped detection
  mechanism, so I don't have to reverse-engineer the code to know what's covered.

## Acceptance Criteria (Gherkin)

```gherkin
Feature: Rule/Feature-level skip/fixme detection

  Scenario: AC-1 - Rule-level @skip tag is detected as unbound
    Given a .feature file with a "Rule:" block tagged "@skip"
    And the Rule contains at least one Scenario
    And the file also has other, non-skipped content so it still generates
    When "specs e2e-coverage validate" runs
    Then every scenario nested under the skipped Rule is reported as unbound

  Scenario: AC-2 - Feature-level @fixme tag is detected as unbound
    Given a .feature file whose top-level "Feature:" is tagged "@fixme"
    When "specs e2e-coverage validate" runs
    Then every scenario in the file is reported as unbound

  Scenario: AC-3 - .only is still excluded (no false positive)
    Given a .feature file with a "Rule:" block tagged "@only"
    When "specs e2e-coverage validate" runs
    Then no scenario under that Rule is reported as unbound

  Scenario: AC-4 - existing Outline-level detection is unaffected
    Given the existing Outline-level @skip/@fixme regression fixture
    When "specs e2e-coverage validate" runs
    Then it still correctly reports the Outline's scenarios as unbound
```

## Product Scope

**In scope**: `apps/rhino-cli/src/application/e2e_coverage/parser.rs` and its design-decision
documentation.

**Out of scope**: any other e2e-coverage detection gap not identified in PR #66 cycle-7's review.

## Product-Level Risks

- Broadening detection to the Rule/Feature level could newly flag existing PASS-ing projects if any
  already (unknowingly) use Rule/Feature-level skip tags — mitigated by the full 11-project
  `specs:e2e:coverage` run in delivery.md's quality gates, and by baselining any real pre-existing gap
  the stricter check surfaces (same pattern as the zero-row-Outline generalization in the originating
  plan).
