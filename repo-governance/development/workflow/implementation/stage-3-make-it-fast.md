---
title: "Stage 3: Make It Fast (If Needed)"
description: The third workflow stage - optimize performance only if measurements show it is necessary.
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
when_to_use: Use only after profiling data shows a measured bottleneck in code that already works and is clean.
---

# Stage 3: Make It Fast (If Needed)

**Goal**: Optimize performance ONLY if measurements show it's necessary.

**Critical requirement**: **MEASURE FIRST**. Never optimize without profiling.

**What to do**:

1. **Profile the code** - Use profiling tools to find actual bottlenecks
2. **Measure baseline** - Record current performance metrics
3. **Identify bottleneck** - Find the slowest part (often 10% of code = 90% of time)
4. **Optimize bottleneck** - Apply targeted optimizations
5. **Measure improvement** - Verify optimization actually helped
6. **Keep tests green** - Ensure functionality didn't break

**What NOT to do**:

- FAIL: Don't optimize without profiling data
- FAIL: Don't optimize everything - only bottlenecks
- FAIL: Don't sacrifice readability unless necessary
- FAIL: Don't guess which parts are slow

**Example**:

```typescript
// Stage 2: Clean code
function calculateOrderTotal(items: OrderItem[]): number {
  return items.reduce((total, item) => total + calculateItemTotal(item), 0);
}

// Stage 3: Optimize ONLY if profiling shows this is a bottleneck
// AND measurements show significant performance impact
function calculateOrderTotalOptimized(items: OrderItem[]): number {
  // Optimized version with memoization, caching, or algorithmic improvement
  // ONLY if measurements prove it's needed
  const cached = orderCache.get(items);
  if (cached) return cached;

  const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  orderCache.set(items, total);
  return total;
}

// Document WHY optimization was needed:
// Profiling showed 80% of checkout time spent in calculateOrderTotal
// Baseline: 1000ms for 10,000 items
// After optimization: 50ms for 10,000 items (20x improvement)
```

**When you're done**: Performance meets requirements, code still clean, optimizations justified by data.
