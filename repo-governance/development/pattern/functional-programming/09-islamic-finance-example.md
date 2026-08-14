---
title: "Islamic Finance Example"
description: "A worked Mudharabah profit-distribution example showing functional core/imperative shell applied to Shariah-compliant business logic."
category: explanation
subcategory: development
tags:
  - development
  - functional-programming
  - immutability
  - pure-functions
  - typescript
created: 2025-12-28
when_to_use: "Use when you need a complete worked example of applying functional core/imperative shell to financial business logic."
---

# Islamic Finance Example

**Mudharabah Profit Distribution**:

```typescript
// Types
interface Partner {
  readonly name: string;
  readonly ratio: number;
}

interface Investment {
  readonly principal: number;
  readonly returns: number;
}

interface Distribution {
  readonly partner: string;
  readonly share: number;
}

interface DistributionResult {
  readonly distributions: readonly Distribution[];
  readonly total: number;
  readonly verified: boolean;
}

// FUNCTIONAL CORE: Pure business logic

function validateRatios(partners: readonly Partner[]): boolean {
  const sum = partners.reduce((acc, p) => acc + p.ratio, 0);
  return Math.abs(sum - 1.0) < 0.0001; // Account for floating point
}

function distributeProfits(investment: Investment, partners: readonly Partner[]): readonly Distribution[] {
  return partners.map((partner) => ({
    partner: partner.name,
    share: investment.returns * partner.ratio,
  }));
}

function verifyDistribution(distributions: readonly Distribution[], expectedTotal: number): boolean {
  const actualTotal = distributions.reduce((sum, d) => sum + d.share, 0);
  return Math.abs(actualTotal - expectedTotal) < 0.01;
}

function calculateDistribution(investment: Investment, partners: readonly Partner[]): DistributionResult {
  if (!validateRatios(partners)) {
    throw new Error("Partner ratios must sum to 1.0");
  }

  const distributions = distributeProfits(investment, partners);
  const verified = verifyDistribution(distributions, investment.returns);

  return {
    distributions,
    total: investment.returns,
    verified,
  };
}

// IMPERATIVE SHELL: Side effects at boundaries

async function processMudharabahDistribution(investmentId: string, partners: readonly Partner[]): Promise<void> {
  // Load data (side effect)
  const investment = await database.investments.findById(investmentId);

  // Pure calculation
  const result = calculateDistribution(investment, partners);

  if (!result.verified) {
    throw new Error("Distribution verification failed");
  }

  // Save results (side effects)
  await database.distributions.insertMany(result.distributions);
  await auditLog.record({
    type: "mudharabah_distribution",
    investmentId,
    total: result.total,
    timestamp: Date.now(),
  });

  // Notify partners (side effect)
  for (const dist of result.distributions) {
    await notificationService.send(dist.partner, {
      message: `Your profit share: ${dist.share}`,
    });
  }
}
```

**Why functional approach matters**:

- **Testable**: Business logic tested without database/notification mocks
- **Auditable**: Pure functions make Shariah compliance verification straightforward
- **Composable**: Can combine distribution logic with other calculations
- **Predictable**: Same inputs always produce same outputs
