---
title: "TDD with DDD Standards"
description: OSE Platform standards for testing aggregates, value objects, entities, and domain events
category: explanation
subcategory: development
tags:
  - tdd
  - ddd
  - domain-testing
principles:
  - explicit-over-implicit
  - automation-over-manual
  - reproducibility
  - pure-functions
created: 2026-02-09
---

# TDD with DDD Standards

## Prerequisite Knowledge

**REQUIRED**: Complete [AyoKoding TDD By Example](../../../../../apps/ayokoding-www/content/en/learn/legacy/software-engineering/development/test-driven-development-tdd/by-example/) and [AyoKoding DDD By Example](../../../../../apps/ayokoding-www/content/en/learn/legacy/software-engineering/software-architecture/patterns-and-principles/) before using these standards.

## Purpose

OSE Platform standards for testing DDD tactical patterns.

## REQUIRED: Test Aggregate Invariants

**REQUIRED**: All aggregate invariants MUST be tested.

```rust
#[test]
fn should_enforce_markup_limit() {
    // Arrange & Act & Assert
    let result = Contract::create(
        Money::usd(10_000),
        Money::usd(1_100), // 11% markup — exceeds 10% limit
    );

    assert!(matches!(result, Err(ContractError::InvalidMarkup(_))));
    assert_eq!(
        result.unwrap_err().to_string(),
        "Markup cannot exceed 10% of asset price"
    );
}

#[test]
fn should_allow_valid_markup() {
    // Arrange & Act
    let contract = Contract::create(
        Money::usd(10_000),
        Money::usd(1_000), // 10% markup — valid
    )
    .expect("should create contract with valid markup");

    // Assert
    assert_eq!(contract.markup(), Money::usd(1_000));
}
```

## REQUIRED: Test Value Object Immutability

**REQUIRED**: All value objects MUST test immutability.

```typescript
describe("Money Value Object", () => {
  it("should not mutate original on add operation", () => {
    // Arrange
    const original = Money.usd(100);
    const originalAmount = original.amount;

    // Act
    const sum = original.add(Money.usd(50));

    // Assert
    expect(original.amount).toBe(originalAmount); // Unchanged
    expect(sum.amount).toBe(150); // New instance
  });
});
```

## REQUIRED: Test Value Object Equality

**REQUIRED**: Value objects MUST test equality by value.

```rust
#[test]
fn should_be_equal_when_values_match() {
    // Arrange
    let money1 = Money::usd(100);
    let money2 = Money::usd(100);

    // Assert — value equality via PartialEq derive
    assert_eq!(money1, money2);
    // Rust value types are copied/cloned, not reference-compared,
    // so structural equality is the natural semantic here.
}
```

## REQUIRED: Test Domain Event Emission

**REQUIRED**: Aggregates MUST test domain event emission.

```typescript
describe("ZakatAssessment - Domain Events", () => {
  it("should emit ZakatCalculated event on calculation", () => {
    // Arrange
    const assessment = ZakatAssessment.create(
      UserId.generate(),
      Money.usd(100000),
      NisabThreshold.goldEquivalent(Money.fromGold(87.48)),
    );

    // Act
    assessment.calculate();

    // Assert
    const events = assessment.getDomainEvents();
    expect(events).toHaveLength(1);
    expect(events[0]).toBeInstanceOf(ZakatCalculated);
  });

  it("should include correct data in event", () => {
    // Arrange
    const userId = UserId.generate();
    const assessment = ZakatAssessment.create(
      userId,
      Money.usd(100000),
      NisabThreshold.goldEquivalent(Money.fromGold(87.48)),
    );

    // Act
    assessment.calculate();

    // Assert
    const event = assessment.getDomainEvents()[0] as ZakatCalculated;
    expect(event.userId.equals(userId)).toBe(true);
    expect(event.zakatAmount.equals(Money.usd(2500))).toBe(true);
  });
});
```

## REQUIRED: Test Entity Identity

**REQUIRED**: Entities MUST test identity-based equality.

```rust
#[test]
fn should_be_equal_by_identity() {
    // Arrange — same ID, different amounts
    let id = DonationId::generate();
    let donation1 = Donation::new(id.clone(), Money::usd(100));
    let donation2 = Donation::new(id.clone(), Money::usd(200));

    // Assert — entities compare by ID only
    assert_eq!(donation1.id(), donation2.id()); // Same ID
    assert_ne!(donation1.amount(), donation2.amount()); // Different amounts
}
```

## OSE Platform Examples

### Testing Zakat Aggregate

```rust
#[cfg(test)]
mod zakat_assessment_tests {
    use super::*;

    #[test]
    fn should_calculate_zakat_when_above_nisab() {
        // Arrange
        let mut assessment = ZakatAssessment::create(
            UserId::generate(),
            Money::usd(100_000),
            NisabThreshold::gold_equivalent(Money::from_gold(87.48)),
        );

        // Act
        assessment.calculate().expect("calculation should succeed");

        // Assert
        assert_eq!(assessment.zakat_due(), Money::usd(2_500)); // 2.5% of wealth
        assert_eq!(assessment.status(), AssessmentStatus::Calculated);
    }

    #[test]
    fn should_reject_calculation_below_nisab() {
        // Arrange
        let mut assessment = ZakatAssessment::create(
            UserId::generate(),
            Money::usd(1_000), // Below Nisab
            NisabThreshold::gold_equivalent(Money::from_gold(87.48)),
        );

        // Act & Assert
        let result = assessment.calculate();
        assert!(matches!(result, Err(ZakatError::BelowNisab)));
    }
}
```

### Testing FiscalDate Value Object

```typescript
describe("FiscalDate Value Object", () => {
  it("should validate Hijri month range", () => {
    // Act & Assert
    expect(() => FiscalDate.of(1445, 13, 1)).toThrow("Month must be between 1 and 12");
  });

  it("should compare dates correctly", () => {
    // Arrange
    const earlier = FiscalDate.of(1445, 1, 1);
    const later = FiscalDate.of(1445, 6, 1);

    // Assert
    expect(later.isAfter(earlier)).toBe(true);
  });

  it("should have value equality", () => {
    // Arrange
    const date1 = FiscalDate.of(1445, 1, 1);
    const date2 = FiscalDate.of(1445, 1, 1);

    // Assert
    expect(date1.equals(date2)).toBe(true);
    expect(date1).not.toBe(date2); // Different instances
  });
});
```
