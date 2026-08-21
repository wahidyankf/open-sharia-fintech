---
title: "Success Criteria"
description: Gherkin scenarios covering placement, admission, eviction, precedence, enforcement disposition, and the sibling obligation.
when_to_use: Use when validating that a propagation run behaved correctly, or when extending the workflow.
---

# Success Criteria

```gherkin
Feature: Repository rules propagation

  Scenario: A rule that must be read unprompted is admitted by evicting a weaker resident
    Given a normalized rule whose audience is everyone before any file is opened
    And the canonical instruction surface has no budget headroom
    When the workflow runs
    Then the rule is written to the canonical instruction surface
    And one resident entry is relocated into the governance layer owning its subject
    And the eviction and the admission land in the same pull request
    And no word-budget threshold is changed

  Scenario: A rule reachable by activity is placed in a governance layer
    Given a normalized rule whose audience reaches it through the activity it governs
    When the workflow runs
    Then the rule is written into the layer recorded at classification
    And the instruction surface is unchanged

  Scenario: A vendor-neutral rule never lands in a binding shim
    Given a normalized rule that can be stated without naming a harness
    When the workflow places it on the instruction surface
    Then it is written to the canonical instruction file
    And it is not written to any binding shim

  Scenario: A higher-layer contradiction halts the run
    Given a normalized rule that contradicts a principle
    When the conflict scan runs
    Then the run halts for that rule
    And the principle is not edited
    And the conflict is reported to the human with both statements named

  Scenario: A same-layer contradiction supersedes the existing rule
    Given a normalized rule that contradicts a rule in the same layer
    When the workflow runs
    Then the existing statement is retired
    And the supersession is recorded with its replacement's location

  Scenario: No rule ships without an enforcement disposition
    Given a batch of normalized rules
    When the workflow reaches delivery
    Then every rule carries exactly one of covered, gated, or unenforced-by-decision
    And every unenforced rule carries a recorded reason

  Scenario: A portable rule records what the sibling repository is owed
    Given a propagated rule that is portable governance guidance
    When the pull request is opened
    Then a sibling obligation naming the other repository is recorded
    And the sibling repository is not modified by this run
```

## Related Documents

- [Termination Criteria](./termination-criteria.md) — the prose form of these scenarios.
