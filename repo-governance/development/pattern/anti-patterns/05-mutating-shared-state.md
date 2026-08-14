---
title: "Anti-Pattern 4: Mutating Shared State"
description: "Code mutates data structures in place instead of creating new ones."
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: "Use when reviewing code that mutates function arguments or shared objects."
---

# Anti-Pattern 4: Mutating Shared State

**Problem**: Mutating data structures instead of creating new ones.

**Bad Example:**

```typescript
// Mutation (problematic)
function processItems(items: Item[]): void {
  items.forEach((item) => {
    item.processed = true; // Mutates original!
  });
}

const original = [{ id: 1, processed: false }];
processItems(original);
// original is now mutated - unexpected side effects!
```

**Solution:**

```typescript
// Immutable approach
function processItems(items: Item[]): Item[] {
  return items.map((item) => ({
    ...item,
    processed: true,
  }));
}

const original = [{ id: 1, processed: false }];
const processed = processItems(original);
// original unchanged, new array returned
```

**Rationale:**

- Prevents unexpected side effects
- Easier to reason about code
- Supports functional composition
- Better testability
