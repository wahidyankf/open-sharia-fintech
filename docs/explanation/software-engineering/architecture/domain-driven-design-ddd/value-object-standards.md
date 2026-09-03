---
title: "DDD Value Object Standards"
description: OSE Platform standards for immutable value objects in Islamic finance domains
category: explanation
subcategory: architecture
tags:
  - ddd
  - value-objects
  - immutability
principles:
  - immutability
  - explicit-over-implicit
  - simplicity-over-complexity
created: 2026-02-09
---

# DDD Value Object Standards

## Prerequisite Knowledge

**REQUIRED**: Complete [AyoKoding DDD Value Objects](../../../../../apps/ayokoding-www/content/en/learn/legacy/software-engineering/software-architecture/patterns-and-principles/) before using these standards.

## Purpose

OSE Platform value object standards for domain primitives.

## REQUIRED: Use Immutable Value Objects

**REQUIRED**: All domain primitives MUST be implemented as immutable value objects.

**Implementation**:

- **Rust**: Use struct with `PartialEq`/`Eq` derive
- **TypeScript**: Use `readonly` properties
- **F#**: Use discriminated union or record with private setters

## OSE Platform Value Objects

### Money

**REQUIRED for all financial amounts**:

#### `Rust`

```rust
use rust_decimal::Decimal;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Money {
    amount: Decimal,
    currency: String,
}

impl Money {
    pub fn new(amount: Decimal, currency: String) -> Result<Self, &'static str> {
        if amount < Decimal::ZERO {
            return Err("Amount cannot be negative");
        }
        Ok(Self { amount, currency })
    }

    pub fn add(&self, other: &Money) -> Result<Money, &'static str> {
        self.assert_same_currency(other)?;
        Money::new(self.amount + other.amount, self.currency.clone())
    }

    pub fn multiply(&self, factor: Decimal) -> Result<Money, &'static str> {
        Money::new(self.amount * factor, self.currency.clone())
    }
}
```

#### `C#`

```csharp
namespace Ose.Zakat.Domain;

public sealed record Money(decimal Amount, string Currency)
{
    public Money
    {
        if (Amount < 0)
            throw new ArgumentException("Amount cannot be negative", nameof(Amount));
    }

    public Money Add(Money other)
    {
        AssertSameCurrency(other);
        return this with { Amount = Amount + other.Amount };
    }

    public Money Multiply(decimal factor) => this with { Amount = Amount * factor };
}
```

### FiscalDate

**REQUIRED for Zakat calculations (Islamic calendar)**:

#### `Rust`

```rust
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FiscalDate {
    pub hijri_year: u32,
    pub hijri_month: u8,
    pub hijri_day: u8,
}

impl FiscalDate {
    pub fn new(hijri_year: u32, hijri_month: u8, hijri_day: u8) -> Result<Self, &'static str> {
        // Validation, conversion methods
        Ok(Self { hijri_year, hijri_month, hijri_day })
    }
}
```

#### `C#`

```csharp
namespace Ose.Zakat.Domain;

public sealed record FiscalDate(int HijriYear, int HijriMonth, int HijriDay)
{
    // Validation, conversion methods
}
```

### NisabThreshold

**REQUIRED for Zakat obligation checks**:

#### `Rust`

```rust
use rust_decimal::Decimal;
use rust_decimal_macros::dec;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NisabThreshold {
    gold_equivalent: Money,
}

impl NisabThreshold {
    const GOLD_GRAMS: Decimal = dec!(87.48);

    pub fn new(gold_equivalent: Money) -> Self {
        Self { gold_equivalent }
    }

    pub fn exceeds(&self, wealth: &Money) -> bool {
        wealth.is_greater_than(&self.gold_equivalent)
    }
}
```

#### `C#`

```csharp
namespace Ose.Zakat.Domain;

public sealed record NisabThreshold(Money GoldEquivalent)
{
    private static readonly decimal GoldGrams = 87.48m;

    public bool Exceeds(Money wealth) => wealth.IsGreaterThan(GoldEquivalent);
}
```

## Validation

**REQUIRED**: All value objects MUST validate invariants in constructor.

**PROHIBITED**: Setters (value objects are immutable).
