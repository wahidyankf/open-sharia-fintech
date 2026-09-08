---
description: Walks through a Mudharabah profit-distribution calculation implemented with impure versus pure functions to show the verifiability difference.
when_to_use: Use when implementing Islamic finance profit-sharing logic that must be independently verifiable.
---

# Islamic Finance Example

**Scenario**: Calculating profit distribution in Mudharabah (profit-sharing partnership).

FAIL: **Impure approach** (avoid):

```typescript
let totalProfits = 0;
const partnerAccounts = { investor: 0, manager: 0 };

function distributeMudharabahProfits(profit, investorRatio) {
  // SIDE EFFECTS: modifies globals
  totalProfits += profit;
  partnerAccounts.investor += profit * investorRatio;
  partnerAccounts.manager += profit * (1 - investorRatio);

  // Depends on global state
  console.log("Total profits so far:", totalProfits);
}

distributeMudharabahProfits(10000, 0.7);
// Hard to test, non-deterministic, concurrent-unsafe
```

PASS: **Pure approach** (preferred):

```typescript
interface MudharabahDistribution {
  readonly investor: number;
  readonly manager: number;
  readonly total: number;
}

// Pure function - deterministic, no side effects
function distributeMudharabahProfits(profit: number, investorRatio: number): MudharabahDistribution {
  const investorShare = profit * investorRatio;
  const managerShare = profit * (1 - investorRatio);

  return {
    investor: investorShare,
    manager: managerShare,
    total: profit,
  };
}

// Easy to test
expect(distributeMudharabahProfits(10000, 0.7)).toEqual({
  investor: 7000,
  manager: 3000,
  total: 10000,
});

// Compose with other pure functions
function recordDistribution(distribution: MudharabahDistribution, timestamp: number): DistributionRecord {
  return {
    ...distribution,
    timestamp,
    verified: true,
  };
}

// IMPERATIVE SHELL: Side effects at boundary
async function saveMudharabahDistribution(profit: number, investorRatio: number): Promise<void> {
  const distribution = distributeMudharabahProfits(profit, investorRatio); // Pure
  const record = recordDistribution(distribution, Date.now()); // Pure
  await database.distributions.insert(record); // SIDE EFFECT
}
```

**Why pure functions matter for Shariah compliance**:

- **Verifiable**: Islamic scholars can verify profit-sharing calculations through simple tests
- **Transparent**: No hidden state or side effects that could violate Mudharabah contract terms
- **Auditable**: Each calculation step is deterministic and traceable
- **Trustworthy**: Investors and managers can independently verify their share calculations
