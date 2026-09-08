---
description: "Functions should depend only on their inputs, not on external mutable state."
when_to_use: "Use when writing or reviewing a function to check whether it depends on hidden external state."
---

# Practice 6: Write Pure Functions

**Principle**: Functions should depend only on inputs, not external state.

**Good Example:**

```typescript
// Pure function
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

**Bad Example:**

```typescript
// Impure function (depends on external state)
let discount = 0.1;
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0) * (1 - discount);
}
```

**Rationale:**

- Deterministic output for same input
- Easier to test
- No hidden dependencies
- Supports memoization
