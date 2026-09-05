---
title: "BDD with DDD Standards"
description: OSE Platform standards for integrating BDD scenarios with DDD bounded contexts and ubiquitous language
category: explanation
subcategory: development
tags:
  - bdd
  - ddd
  - bounded-contexts
  - ubiquitous-language
principles:
  - explicit-over-implicit
  - automation-over-manual
  - reproducibility
created: 2026-02-09
---

# BDD with DDD Standards

## Prerequisite Knowledge

**REQUIRED**: Complete [AyoKoding BDD By Example](../../../../../apps/ayokoding-www/content/en/learn/legacy/software-engineering/development/behavior-driven-development-bdd/by-example/) and [AyoKoding DDD By Example](../../../../../apps/ayokoding-www/content/en/learn/legacy/software-engineering/software-architecture/patterns-and-principles/) before using these standards.

## Purpose

OSE Platform standards for integrating BDD scenarios with DDD patterns.

These examples implement the
[canonical OSE BDD contract](../../../../../repo-governance/development/behaviour-driven-development.md).
Store each feature in its owner's recursively discovered `specs/**/behaviours/` corpus; do not
create a parallel root `features/` tree.

## REQUIRED: One Feature per Bounded Context Capability

**REQUIRED**: Feature files MUST align with bounded context boundaries.

```text
specs/apps/finance/zakat/behaviours/
  calculation/zakat-calculation.feature      # Capability: Calculate Zakat
  calculation/nisab-validation.feature       # Capability: Validate Nisab
  tracking/hawl-tracking.feature             # Capability: Track Hawl

specs/apps/finance/donation/behaviours/
  campaign/campaign-management.feature       # Capability: Manage Campaigns
  donation/donation-processing.feature       # Capability: Process Donations
```

## REQUIRED: Use Ubiquitous Language

**REQUIRED**: Scenarios MUST use terms from DDD glossary.

**Example: Zakat Context**

```gherkin
Feature: Zakat Calculation

  Scenario: Nisab threshold exceeded
    Given a Zakatable Asset of 100 grams of gold
    And the Nisab Threshold is 87.48 grams
    And the Hawl period has completed
    When Zakat Assessment is calculated
    Then Zakat Due should be 2.5 grams
```

**Terms from DDD Glossary:**

- `Zakatable Asset` (aggregate)
- `Nisab Threshold` (value object)
- `Hawl` (ubiquitous term for lunar year)
- `Zakat Assessment` (aggregate)
- `Zakat Due` (value object)

## REQUIRED: Domain Events in Then Steps

**REQUIRED**: When aggregates emit domain events, scenarios MUST verify them.

```gherkin
Scenario: Donation received and recorded
  Given a campaign "Build School" with goal $50,000
  When a donor contributes $1,000
  Then the campaign total should be $51,000
  And a "DonationReceived" event should be published
  And the event should contain donation ID and amount
```

## REQUIRED: Test Aggregate Invariants

**REQUIRED**: Scenarios MUST verify aggregate business rules.

```gherkin
Feature: Murabaha Contract Invariants

  Scenario: Contract enforces profit margin limit
    Given a Murabaha contract for $10,000 asset
    When profit margin is set to 11%
    Then the contract should be rejected
    And error message should be "Profit margin cannot exceed 10%"

  Scenario: Contract allows valid profit margin
    Given a Murabaha contract for $10,000 asset
    When profit margin is set to 8%
    Then the contract should be accepted
```

## Feature File per Bounded Context

**REQUIRED**: Features MUST NOT span bounded contexts.

**Good** (bounded context aligned):

```gherkin
# specs/apps/finance/donation/behaviours/campaign/campaign-management.feature
Feature: Campaign Management

  Scenario: Create campaign
    Given a campaign organizer has valid campaign details
    When the organizer creates the campaign
    Then the campaign should be available for donations
```

**Bad** (crossing bounded contexts):

```gherkin
# specs/apps/finance/donation/behaviours/mixed.feature (WRONG!)
Feature: Donation and Zakat Processing

  Scenario: Process donation (donation context)
    Given an active donation campaign
    When a donor submits a valid donation
    Then the donation should be recorded

  Scenario: Calculate Zakat (zakat context)
    Given wealth above the Nisab threshold
    When Zakat is calculated
    Then the Zakat amount should be returned
```

## OSE Platform Examples

### Zakat Context Scenarios

```gherkin
Feature: Zakat Obligation Assessment

  As a Zakat calculator
  I want to determine if Zakat is obligatory
  So that users know their religious obligations

  Scenario: Wealth above Nisab with complete Hawl
    Given a Muslim individual's wealth is 100 grams of gold
    And the Nisab threshold is 87.48 grams
    And one lunar year (Hawl) has passed since acquisition
    When Zakat obligation is assessed
    Then Zakat should be obligatory
    And the assessment status should be "OBLIGATORY"
```

### Contract Context Scenarios

```gherkin
Feature: Murabaha Contract Lifecycle

  As a contract manager
  I want contracts to follow proper state transitions
  So that all contracts maintain Shariah compliance

  Scenario: Contract transitions from DRAFT to PENDING_REVIEW
    Given a Murabaha contract in DRAFT status
    And all required fields are completed
    And profit margin is within 10% limit
    When the contract is submitted for review
    Then the contract status should be "PENDING_REVIEW"
    And a "ContractSubmitted" event should be published
```

### Campaign Context Scenarios

```gherkin
Feature: Campaign Goal Tracking

  As a campaign organizer
  I want to track progress toward goal
  So that donors see real-time impact

  Scenario: Donation moves campaign toward goal
    Given a campaign "Emergency Relief" with goal $100,000
    And the campaign has raised $60,000
    When a donor contributes $10,000
    Then the campaign total should be $70,000
    And the progress percentage should be 70%
    And a "DonationReceived" event should be published
```
