---
title: "How It Applies — Functional Core and Hidden Dependencies"
description: Shows the Functional Core, Imperative Shell pattern and how to avoid hidden global-config dependencies.
category: explanation
subcategory: principles
tags:
  - principles
  - functional-programming
  - pure-functions
  - testability
  - determinism
created: 2025-12-28
when_to_use: Use when separating pure logic from I/O or removing a hidden dependency on global state.
---

# How It Applies — Functional Core and Hidden Dependencies

Continues [How It Applies](./how-it-applies.md).

## Functional Core, Imperative Shell

**Context**: Saving Murabaha contract to database.

PASS: **Pure core + Impure shell (Preferred architecture)**:

```typescript
// FUNCTIONAL CORE: Pure business logic
interface MurabahaContract {
  readonly cost: number;
  readonly markupRate: number;
  readonly markup: number;
  readonly total: number;
}

function createMurabahaContract(cost: number, markupRate: number): MurabahaContract {
  const markup = cost * markupRate;
  return {
    cost,
    markupRate,
    markup,
    total: cost + markup,
  };
}

function validateMurabahaContract(contract: MurabahaContract): boolean {
  // Pure validation logic
  return (
    contract.cost > 0 &&
    contract.markupRate > 0 &&
    contract.markupRate < 1 && // Max 100% markup
    contract.markup === contract.cost * contract.markupRate &&
    contract.total === contract.cost + contract.markup
  );
}

// IMPERATIVE SHELL: Side effects at boundaries
async function saveMurabahaContract(cost: number, markupRate: number): Promise<void> {
  // Create contract (pure)
  const contract = createMurabahaContract(cost, markupRate);

  // Validate contract (pure)
  if (!validateMurabahaContract(contract)) {
    throw new Error("Invalid Murabaha contract");
  }

  // Side effect: Save to database (at boundary)
  await database.contracts.insert(contract);
}
```

**Why this works**:

- Core business logic is pure (testable, verifiable)
- Side effects isolated at system boundaries
- Easy to test business rules without database
- Clear separation of concerns

## Avoiding Hidden Dependencies

**Context**: Formatting currency for display.

PASS: **Pure (Preferred)**:

```typescript
// Pure function - all dependencies explicit
function formatCurrency(amount: number, currency: string, locale: string): string {
  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency,
  }).format(amount);
}

// All inputs explicit, deterministic
formatCurrency(1000, "SAR", "ar-SA"); // "١٬٠٠٠٫٠٠ ر.س.‏"
formatCurrency(1000, "USD", "en-US"); // "$1,000.00"
```

**Why this works**: All dependencies passed as arguments. Same inputs = same output.

FAIL: **Impure (Avoid)**:

```typescript
// Impure - depends on global configuration
const appConfig = {
  currency: "SAR",
  locale: "ar-SA",
};

function formatCurrency(amount: number): string {
  // Hidden dependency on appConfig
  return new Intl.NumberFormat(appConfig.locale, {
    style: "currency",
    currency: appConfig.currency,
  }).format(amount);
}

// Behavior changes if appConfig changes
// Hard to test different locales
// Not deterministic
```

**Why this fails**: Hidden dependency on global config. Different results if config changes. Hard to test.
