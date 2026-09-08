---
description: Four implementation-workflow anti-patterns - premature optimization, skipping "make it right," optimizing everything, and optimizing without measurement.
when_to_use: Use when reviewing a change to check it isn't optimizing prematurely, skipping cleanup, over-optimizing, or optimizing on a guess.
---

# Anti-Patterns

## Premature Optimization

FAIL: **Problem**: Optimizing before making it work or right.

```typescript
// FAIL: Stage 1: DON'T DO THIS - Premature optimization
function calculateOrderTotal(items: OrderItem[]): number {
  // Trying to optimize in Stage 1 (Make It Work)
  const cache = new WeakMap();
  const memoized = items.map((item) => {
    if (cache.has(item)) return cache.get(item);
    const result = item.price * item.quantity;
    cache.set(item, result);
    return result;
  });
  return memoized.reduce((a, b) => a + b, 0);
}
```

**Why it's bad**: Code is complex before it even works. Optimization might be in wrong place.

## Skipping "Make It Right"

FAIL: **Problem**: Optimizing messy code.

```typescript
// FAIL: Skipped Stage 2 - Went from "working" to "optimized" with ugly code
function calcOrdTot(itms) {
  let t = 0,
    i = 0,
    l = itms.length;
  for (; i < l; ++i) t += itms[i].p * itms[i].q;
  return t;
}
```

**Why it's bad**: Optimized but unmaintainable. Hard to modify or debug later.

## Optimizing Everything

FAIL: **Problem**: Optimizing code that doesn't need it.

```typescript
// FAIL: Optimizing a function that runs once per page load
function getAppTitle(): string {
  // Unnecessary memoization for function called once
  if (this.cachedTitle) return this.cachedTitle;
  this.cachedTitle = "Open Sharia Enterprise";
  return this.cachedTitle;
}
```

**Why it's bad**: Wasted effort. Adds complexity with no benefit.

## Optimization Without Measurement

FAIL: **Problem**: Guessing which parts are slow.

```typescript
// FAIL: "I think this is slow" - NO PROFILING DATA
// Developer spends 2 days optimizing this function
// Profiler shows it takes 0.1% of total execution time
```

**Why it's bad**: Optimizing the wrong thing. Real bottleneck remains unoptimized.
