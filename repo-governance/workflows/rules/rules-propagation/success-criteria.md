---
description: Gherkin scenarios for rules-propagation outcomes.
when_to_use: Use to validate or extend this workflow.
---

# Success Criteria

```gherkin
Feature: Repository rules propagation

  Scenario: A semantically sufficient rule request is a no-op
    Given the effective rules already satisfy the requested meaning, strength, scope, boundaries, exceptions, and discoverability
    When semantic sufficiency is evaluated before placement
    Then the manifest records no-op with the canonical source and verification evidence
    And the rule produces no tracked diff

  Scenario: A material semantic gap continues to placement
    Given an existing rule resembles the request but has weaker scope or strength
    When semantic sufficiency is evaluated
    Then the request is not suppressed as a no-op
    And the workflow continues through placement and enforcement

  Scenario: A rule that must be read unprompted is admitted by evicting a weaker resident
    Given a normalized rule must be read before files are opened
    And the instruction surface is full
    When the workflow runs
    Then the rule is admitted by relocating a resident to its owning governance layer
    And both changes land together without changing a word-budget threshold

  Scenario: Word-budget remediation preserves material meaning
    Given a rule exceeds its destination word budget and names a specific audience and boundary
    When the workflow relocates detail through progressive disclosure
    Then obligation, audience, strength, scope, exceptions, pass conditions, and enforcement remain equivalent
    And no material qualifier is generalized or removed for brevity

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

  Scenario: Subject consolidation preserves rules
    Given a rule reaches Step 6
    When surfaces are reviewed
    Then each has a keep, amend, merge, delete, relocate, or supersede verdict
    And each names its canonical home
    And merge/delete preserves distinct obligations and necessary discovery paths
    And redundancy remains only with a keep rationale

  Scenario: A portable rule records what the sibling repository is owed
    Given a propagated rule that is portable governance guidance
    When the pull request is opened
    Then a sibling obligation naming the other repository is recorded
    And the obligation records the common objective slug and reusable worktree and branch identities
    And the current repository's actual identities match that record
    And the sibling repository is not modified by this run

  Scenario: A parity identity is unavailable before mutation
    Given a portable rule whose intended worktree basename or branch name is unavailable in one repository
    When the workflow performs its parity-identity preflight
    Then it proves an existing identity belongs to the same delivery or selects one common alternative
    And it does not silently diverge or commandeer a foreign identity
    And no sibling repository is modified by this run
```

## Related

[Termination Criteria](./termination-criteria.md) gives the prose form.
