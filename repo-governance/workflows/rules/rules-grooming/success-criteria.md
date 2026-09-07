---
title: "Success Criteria"
description: Gherkin scenarios for rules-grooming outcomes.
when_to_use: Use to validate or extend this workflow.
---

# Success Criteria

```gherkin
Feature: Repository rules grooming

  Scenario: A sweep nothing called for does not run
    Given no recurrence trigger condition is met by the census
    When the workflow is invoked
    Then the run records no-op with all three trigger values
    And no candidate discovery sweep runs

  Scenario: The first run is not blocked by having no baseline
    Given no prior grooming run is recorded
    When the census evaluates the recurrence trigger
    Then the elapsed-time condition is satisfied by definition
    And the run proceeds and its census becomes the baseline

  Scenario: A dry run skips the preservation baseline it cannot use
    Given the run is invoked with dry-run true
    When Step 2 is reached
    Then the obligation inventory is skipped and the skip recorded
    And no deterministic extract is labelled a preservation baseline

  Scenario: An unapproved obligation loss halts the run
    Given the post-run inventory is missing an obligation not on the approved retirement list
    When preservation verification runs
    Then the run halts
    And the propagation delivery that introduced the loss is identified
    And the revert is handed to propagation rather than written by this workflow

  Scenario: An obligation that survives but becomes unreachable is treated as lost
    Given a surviving obligation reachable from no surface that binds its audience
    When preservation verification runs
    Then the run halts with that obligation named

  Scenario: Grooming never writes a rule surface
    Given a manifest of approved candidates
    When the workflow hands them off
    Then every rule edit is written by rules-propagation
    And this workflow stages, commits, and pushes nothing

  Scenario: A partial run still records what it learned
    Given a run in which one subject group halted at propagation
    When the run ends
    Then the remaining approved groups still land
    And the log entry records the halt, every deferred item, and the metrics delta

  Scenario: A rejected candidate is not re-presented as new
    Given a candidate rejected at a previous run's checkpoint
    When the next sweep rediscovers it
    Then it is recorded as rejected-again with the prior reason attached
```

## Related

- [Success Criteria — Candidate Classes](./success-criteria-candidate-classes.md) — the per-class
  admission and refusal scenarios.
- [Termination Criteria](./termination-criteria.md) — the prose form.
