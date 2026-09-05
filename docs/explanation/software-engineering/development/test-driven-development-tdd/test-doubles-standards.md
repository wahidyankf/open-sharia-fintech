---
title: "TDD Test Doubles Standards"
description: OSE Platform standards for mocks, stubs, spies, and fakes
category: explanation
subcategory: development
tags:
  - tdd
  - testing
  - test-doubles
  - mocking
principles:
  - explicit-over-implicit
  - simplicity-over-complexity
  - automation-over-manual
  - reproducibility
created: 2026-02-09
---

# TDD Test Doubles Standards

## Prerequisite Knowledge

**REQUIRED**: Complete [AyoKoding TDD By Example](../../../../../apps/ayokoding-www/content/en/learn/legacy/software-engineering/development/test-driven-development-tdd/by-example/) before using these standards.

## Purpose

OSE Platform standards for using test doubles (mocks, stubs, fakes).

## REQUIRED: Prefer In-Memory Implementations

**REQUIRED**: Use in-memory implementations over mocks when possible.

**Good** (in-memory implementation):

```rust
use std::collections::HashMap;

struct InMemoryDonationRepository {
    donations: HashMap<DonationId, Donation>,
}

impl InMemoryDonationRepository {
    fn new() -> Self {
        Self { donations: HashMap::new() }
    }
}

impl DonationRepository for InMemoryDonationRepository {
    fn save(&mut self, donation: Donation) {
        self.donations.insert(donation.id.clone(), donation);
    }

    fn find_by_id(&self, id: &DonationId) -> Option<&Donation> {
        self.donations.get(id)
    }
}

#[test]
fn should_save_and_retrieve_donation() {
    // No mocking framework needed
    let mut repository = InMemoryDonationRepository::new();
    let donation = build_donation();

    repository.save(donation.clone());
    let retrieved = repository.find_by_id(&donation.id);

    assert!(retrieved.is_some());
}
```

**Avoid** (excessive mocking):

```rust
// DON'T wire up a full mock for simple state-holding behaviour —
// the in-memory struct above is simpler and more realistic.
// mockall::mock! can replace a trait, but that's overkill here:
mock! {
    DonationRepository {}
    impl DonationRepositoryTrait for DonationRepository {
        fn save(&mut self, donation: Donation);
        fn find_by_id(&self, id: &DonationId) -> Option<&Donation>;
    }
}
// Test becomes brittle and coupled to implementation details
```

## When to Use Test Doubles

### Use Stubs for External Dependencies

**REQUIRED**: Stub external services (payment gateways, notification services).

```typescript
class StubPaymentGateway implements PaymentGateway {
  async process(payment: Payment): Promise<PaymentResult> {
    // Deterministic response for testing
    return PaymentResult.success(payment.id);
  }
}

describe("DonationService", () => {
  it("should process donation payment", async () => {
    const gateway = new StubPaymentGateway();
    const service = new DonationService(gateway);

    const result = await service.processDonation(Money.usd(100));

    expect(result.isSuccess()).toBe(true);
  });
});
```

### Use Spies for Verification

**OPTIONAL**: Use spies when verifying behaviour matters.

```rust
use mockall::predicate::*;
use mockall::mock;

mock! {
    pub EventPublisher {}
    impl EventPublisherTrait for EventPublisher {
        fn publish(&self, event: ZakatCalculated);
    }
}

#[test]
fn should_publish_event_after_calculation() {
    let mut publisher = MockEventPublisher::new();
    // Expect publish to be called exactly once
    publisher
        .expect_publish()
        .times(1)
        .returning(|_| ());

    let service = ZakatService::new(publisher);
    service.calculate_zakat(Money::usd(100_000));
}
```

## PROHIBITED: Over-Mocking

**PROHIBITED**: Mocking domain objects (aggregates, value objects).

**Bad** (mocking domain):

```rust
// DON'T mock domain value objects — use the real structs.
// Mocking a Money struct is always the wrong approach:
mock! {
    pub Money {}
    impl MoneyOps for Money {
        fn multiply(&self, rate: f64) -> Money;
    }
}
// Test becomes meaningless — testing the mock, not real logic
```

**Good** (use real domain objects):

```rust
#[test]
fn should_calculate_zakat() {
    // Use real value objects
    let wealth = Money::usd(100_000);
    let zakat = ZakatCalculator::calculate(wealth);

    assert_eq!(zakat, Money::usd(2_500));
}
```

## OSE Platform Examples

### Testing with In-Memory Repository

```typescript
class InMemoryCampaignRepository implements CampaignRepository {
  private campaigns: Map<string, Campaign> = new Map();

  async save(campaign: Campaign): Promise<void> {
    this.campaigns.set(campaign.id.value, campaign);
  }

  async findActive(): Promise<Campaign[]> {
    return Array.from(this.campaigns.values()).filter((c) => c.status === "ACTIVE");
  }
}

describe("CampaignService", () => {
  let repository: CampaignRepository;

  beforeEach(() => {
    repository = new InMemoryCampaignRepository();
  });

  it("should list active campaigns", async () => {
    // Arrange
    const campaign1 = Campaign.create(Money.usd(10000));
    campaign1.activate();
    await repository.save(campaign1);

    const campaign2 = Campaign.create(Money.usd(5000));
    // campaign2 stays DRAFT
    await repository.save(campaign2);

    // Act
    const activeCampaigns = await repository.findActive();

    // Assert
    expect(activeCampaigns).toHaveLength(1);
  });
});
```
