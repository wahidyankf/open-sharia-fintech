---
title: "DDD Domain Event Standards"
description: OSE Platform standards for domain event design, naming, and publishing
category: explanation
subcategory: architecture
tags:
  - ddd
  - domain-events
  - event-driven
principles:
  - immutability
  - explicit-over-implicit
  - simplicity-over-complexity
created: 2026-02-09
---

# DDD Domain Event Standards

## Prerequisite Knowledge

**REQUIRED**: Complete [AyoKoding DDD Domain Events](../../../../../apps/ayokoding-www/content/en/learn/legacy/software-engineering/software-architecture/patterns-and-principles/) before using these standards.

## Purpose

OSE Platform domain event standards for event-driven architecture.

## REQUIRED: Capture Business Occurrences

**REQUIRED**: All significant business occurrences MUST emit domain events.

## Event Naming

**Format**: `[Entity][PastTenseVerb]`

**Examples**:

- `ZakatCalculated`
- `DonationReceived`
- `CampaignFunded`
- `BeneficiaryVerified`
- `ContractApproved`

**PROHIBITED**: Present tense ("ZakatCalculating"), future tense ("ZakatWillCalculate").

## Event Structure

**REQUIRED**: All events MUST be immutable.

### `Rust`

```rust
use chrono::{DateTime, Utc};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ZakatCalculated {
    pub assessment_id: AssessmentId,
    pub user_id: UserId,
    pub zakat_amount: Money,
    pub occurred_at: DateTime<Utc>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ZakatDomainEvent {
    ZakatCalculated(ZakatCalculated),
    MurabahaContractSigned { contract_id: ContractId, occurred_at: DateTime<Utc> },
    ZakatPaid { assessment_id: AssessmentId, amount: Money, occurred_at: DateTime<Utc> },
}
// No setters — enum variants and struct fields are immutable by default
```

### `C#`

```csharp
namespace Ose.Zakat.Domain.Events;

public sealed record ZakatCalculated(
    AssessmentId AssessmentId,
    UserId UserId,
    Money ZakatAmount,
    DateTimeOffset OccurredAt) : DomainEvent;
// No setters - immutable record
```

## OSE Platform Domain Events

| Event                   | When                           | Contains                |
| ----------------------- | ------------------------------ | ----------------------- |
| `ZakatCalculated`       | Zakat amount determined        | AssessmentId, Amount    |
| `DonationReceived`      | Donation payment confirmed     | DonationId, Amount      |
| `CampaignFunded`        | Campaign reaches goal          | CampaignId, TotalRaised |
| `BeneficiaryVerified`   | Eligibility confirmed          | BeneficiaryId, Status   |
| `ContractApproved`      | Shariah board approves         | ContractId, ApprovalId  |
| `DistributionCompleted` | Funds disbursed to beneficiary | DistributionId, Amount  |

## Publishing

**REQUIRED**: Publish events AFTER aggregate persistence succeeds.

**PROHIBITED**: Publishing events before transaction commits.
