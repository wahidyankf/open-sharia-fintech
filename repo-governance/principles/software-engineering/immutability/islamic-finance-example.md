---
description: Walks through a Murabaha profit-distribution contract implemented with mutable versus immutable state to show the audit-trail difference.
when_to_use: Use when implementing or reviewing Islamic finance calculation logic that must produce an auditable, Shariah-compliant history of state changes.
---

# Islamic Finance Example

**Scenario**: Calculating Murabaha (cost-plus financing) profit distribution.

FAIL: **Mutable approach** (avoid):

```typescript
let contract = {
  cost: 100000,
  markup: 0,
  total: 100000,
  payments: [],
};

function applyMarkup(rate) {
  contract.markup = contract.cost * rate; // MUTATES
  contract.total = contract.cost + contract.markup; // MUTATES
}

function addPayment(amount) {
  contract.payments.push({ amount, date: Date.now() }); // MUTATES
}

applyMarkup(0.1);
addPayment(11000);
// Original contract state lost, can't audit calculation
```

PASS: **Immutable approach** (preferred):

```typescript
interface MurabahaContract {
  readonly cost: number;
  readonly markup: number;
  readonly total: number;
  readonly payments: readonly Payment[];
}

function applyMarkup(contract: MurabahaContract, rate: number): MurabahaContract {
  const markup = contract.cost * rate;
  return {
    ...contract,
    markup,
    total: contract.cost + markup,
  };
}

function addPayment(contract: MurabahaContract, payment: Payment): MurabahaContract {
  return {
    ...contract,
    payments: [...contract.payments, payment],
  };
}

// Clear audit trail
let contract: MurabahaContract = {
  cost: 100000,
  markup: 0,
  total: 100000,
  payments: [],
};
const withMarkup = applyMarkup(contract, 0.1);
const withPayment = addPayment(withMarkup, { amount: 11000, date: Date.now() });

// Each step preserved for Shariah audit
console.log("Original:", contract); // { cost: 100000, markup: 0, ... }
console.log("With markup:", withMarkup); // { cost: 100000, markup: 10000, ... }
console.log("With payment:", withPayment); // Full history
```

**Why immutability matters for Shariah compliance**:

- **Audit trail**: Each calculation step preserved for verification
- **Transparency**: Can verify markup calculation didn't violate riba (usury) rules
- **Reproducibility**: Same inputs always produce same outputs
- **Trust**: Islamic scholars can audit the entire calculation chain
