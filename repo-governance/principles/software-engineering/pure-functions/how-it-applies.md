---
description: Shows pure versus impure patterns for calculating Zakat and distributing Musharakah profit shares in TypeScript.
when_to_use: Use when implementing a business-logic calculation and needing a concrete pure-versus-impure example.
---

# How It Applies

## Pure Business Logic

**Context**: Calculating Zakat (Islamic wealth tax - 2.5% on qualifying wealth).

PASS: **Pure (Preferred)**:

```typescript
// Pure function - deterministic, no side effects
function calculateZakat(wealth: number, nisab: number): number {
  if (wealth < nisab) {
    return 0;
  }
  return wealth * 0.025; // 2.5% Zakat rate
}

// Easy to test
expect(calculateZakat(10000, 5000)).toBe(250);
expect(calculateZakat(3000, 5000)).toBe(0);
expect(calculateZakat(10000, 5000)).toBe(250); // Same result every time
```

**Why this works**: No external dependencies. Same inputs always produce same output. Trivial to test and verify.

FAIL: **Impure (Avoid)**:

```typescript
// Impure - depends on external state
let currentNisab = 5000;
let zakatPaid = 0;

function calculateZakat(wealth: number): number {
  // Depends on external variable
  if (wealth < currentNisab) {
    return 0;
  }

  const zakat = wealth * 0.025;
  zakatPaid += zakat; // SIDE EFFECT: Modifies external state
  return zakat;
}

// Hard to test - depends on global state
// Different results if currentNisab changes
// Side effect makes it unpredictable
```

**Why this fails**: Depends on and modifies global state. Not deterministic. Hard to test. Concurrent calls would corrupt `zakatPaid`.

## Pure Data Transformation

**Context**: Applying profit-sharing ratio to investment returns (Musharakah).

PASS: **Pure (Preferred)**:

```typescript
interface Investment {
  readonly principal: number;
  readonly returns: number;
}

interface Partner {
  readonly name: string;
  readonly ratio: number;
}

// Pure function - deterministic
function distributeProfits(
  investment: Investment,
  partners: readonly Partner[],
): readonly { name: string; share: number }[] {
  return partners.map((partner) => ({
    name: partner.name,
    share: investment.returns * partner.ratio,
  }));
}

const investment = { principal: 100000, returns: 10000 };
const partners = [
  { name: "Ahmad", ratio: 0.6 },
  { name: "Fatima", ratio: 0.4 },
];

const distribution = distributeProfits(investment, partners);
// [{ name: "Ahmad", share: 6000 }, { name: "Fatima", share: 4000 }]
```

**Why this works**: Pure calculation. No side effects. Easy to verify Shariah compliance (60/40 split).

FAIL: **Impure (Avoid)**:

```typescript
const partnerBalances = { Ahmad: 0, Fatima: 0 };

function distributeProfits(investment, partners) {
  partners.forEach((partner) => {
    // SIDE EFFECT: Modifies external object
    partnerBalances[partner.name] += investment.returns * partner.ratio;
  });
}

// Side effects make it hard to test
// Can't verify calculation without checking external state
// Concurrent calls would corrupt balances
```

**Why this fails**: Modifies global state. Not testable in isolation. Concurrent execution unsafe.
