---
description: "Prefer immutable operations such as spread and array methods over direct mutation."
when_to_use: "Use when writing code that updates objects or arrays and needs to avoid mutating the original."
---

# Practice 5: Use Immutable Data Structures

**Principle**: Prefer immutable operations over mutation.

**Good Example:**

```typescript
// Immutable array operations
const newItems = [...items, newItem]; // Spread operator
const filtered = items.filter((x) => x.active); // Returns new array
const mapped = items.map((x) => ({ ...x, processed: true })); // New objects
```

**Bad Example:**

```typescript
// Mutation (avoid when possible)
items.push(newItem); // Mutates original
items[0].processed = true; // Direct mutation
```

**Rationale:**

- Easier to reason about code
- Prevents unexpected side effects
- Supports functional composition
- Improves testability
