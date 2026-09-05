---
title: "Anti-Pattern 5: Impure Functions with Hidden Dependencies"
description: "A function reads or depends on external mutable state, making its output non-deterministic."
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: "Use when a function's output depends on global state."
---

# Anti-Pattern 5: Impure Functions with Hidden Dependencies

**Problem**: Functions depending on external state.

**Bad Example:**

```typescript
// Impure function (hidden dependency)
let taxRate = 0.1;
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0) * (1 + taxRate);
}

// Change in global state affects function output
taxRate = 0.2;
calculateTotal(items); // Different result for same input!
```

**Solution:**

```typescript
// Pure function (explicit dependency)
function calculateTotal(items: Item[], taxRate: number): number {
  return items.reduce((sum, item) => sum + item.price, 0) * (1 + taxRate);
}

// Deterministic - same inputs always produce same output
calculateTotal(items, 0.1);
calculateTotal(items, 0.2);
```

**Rationale:**

- Deterministic behaviour
- Easier to test
- No hidden dependencies
- Supports memoization
