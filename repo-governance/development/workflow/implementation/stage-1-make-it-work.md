---
description: The first workflow stage - get functionality working with the simplest possible solution.
when_to_use: Use when starting a new feature or bug fix and deciding how much design work is appropriate before anything runs.
---

# Stage 1: Make It Work

**Goal**: Get functionality working with the simplest possible solution.

**What to do**:

- Write the most straightforward code that solves the problem
- Don't worry about performance, elegance, or abstractions yet
- Focus on passing tests and meeting requirements
- Hard-code values if it helps you move faster
- Copy-paste code if it gets you to working faster

**What NOT to do**:

- FAIL: Don't create abstractions or design patterns yet
- FAIL: Don't optimize for performance
- FAIL: Don't worry about code duplication
- FAIL: Don't refactor while implementing

**Example**:

```typescript
// PASS: MAKE IT WORK - Simple, straightforward implementation
function calculateOrderTotal(items: any[]) {
  let total = 0;
  for (let i = 0; i < items.length; i++) {
    total = total + items[i].price * items[i].quantity;
  }
  return total;
}

// FAIL: DON'T DO THIS YET - Premature abstraction
class OrderCalculator {
  private strategy: PricingStrategy;
  constructor(strategy: PricingStrategy) {
    this.strategy = strategy;
  }
  calculate(items: OrderItem[]): Money {
    return this.strategy.computeTotal(items);
  }
}
```

**When you're done**: Functionality works, tests pass, requirements met.
