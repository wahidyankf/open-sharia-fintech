---
title: "Best Practices"
description: Six best practices for the implementation workflow, from starting simple through re-measuring after optimization.
category: explanation
subcategory: development
tags:
  - development
  - workflow
  - implementation
  - optimization
  - refactoring
  - surgical-changes
  - goal-driven
  - test-driven
created: 2025-12-15
when_to_use: Use as a checklist when implementing, refactoring, or optimizing any change.
---

# Best Practices

## 1. Always Start Simple

**First implementation should be the simplest**:

```typescript
// PASS: Stage 1: Simple and obvious
function isValidEmail(email: string): boolean {
  return email.includes("@") && email.includes(".");
}

// Later Stage 2: Make it right (proper validation)
function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// Only if Stage 3 needed: Optimize (cache regex, use faster library)
```

## 2. Write Tests Before Refactoring

**Ensure tests pass before "Make It Right"**:

```typescript
// PASS: Tests lock in behavior before refactoring
describe("calculateOrderTotal", () => {
  it("calculates total for multiple items", () => {
    const items = [
      { price: 10, quantity: 2 },
      { price: 5, quantity: 3 },
    ];
    expect(calculateOrderTotal(items)).toBe(35);
  });
});

// Now safe to refactor - tests will catch breakage
```

## 3. Profile Before Optimizing

**Always measure, never guess**:

```bash
# PASS: Profile first
npm run profile

# Output shows:
# calculateOrderTotal: 850ms (85% of total time) ← THIS is the bottleneck
# formatCurrency: 50ms (5% of total time)
# Other functions: 100ms (10% of total time)

# Optimize calculateOrderTotal, not formatCurrency
```

## 4. Document Optimization Decisions

**Explain WHY optimization was needed**:

```typescript
/**
 * Optimized version of calculateOrderTotal
 *
 * Profiling data (2025-12-15):
 * - Baseline: 850ms for 10,000 items (85% of checkout time)
 * - Bottleneck: Repeated item.price * item.quantity calculations
 * - Solution: Memoize item totals
 * - Result: 45ms for 10,000 items (95% improvement)
 */
function calculateOrderTotalOptimized(items: OrderItem[]): number {
  // ... optimized implementation
}
```

## 5. Keep Optimization Localized

**Optimize the bottleneck, keep rest of code clean**:

```typescript
// PASS: Most code remains clean and readable
function processOrder(order: Order) {
  validateOrder(order); // Clean code
  applyDiscounts(order); // Clean code
  const total = calculateOrderTotalOptimized(order.items); // ONLY this optimized
  chargeCustomer(order.customer, total); // Clean code
}
```

## 6. Re-measure After Optimization

**Verify optimization actually helped**:

```typescript
// PASS: Before optimization
console.time("calculateOrderTotal");
const total = calculateOrderTotal(items);
console.timeEnd("calculateOrderTotal");
// calculateOrderTotal: 850ms

// After optimization
console.time("calculateOrderTotal");
const total = calculateOrderTotalOptimized(items);
console.timeEnd("calculateOrderTotal");
// calculateOrderTotal: 45ms ← Verified 95% improvement
```
