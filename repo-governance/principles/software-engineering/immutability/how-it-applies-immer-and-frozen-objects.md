---
description: Shows immutable object updates plus Immer and Object.freeze techniques for complex or runtime-enforced immutability.
when_to_use: Use when updating deeply nested objects immutably or when runtime enforcement of immutability is required.
---

# How It Applies — Immer and Frozen Objects

Continues [How It Applies](./how-it-applies.md).

## Using Immer for Complex Updates

**Context**: Deep nested structures are cumbersome with spread operators.

PASS: **Immutable with Immer (Preferred for complex structures)**:

```typescript
import { produce } from "immer";

const state = {
  users: [
    { id: 1, profile: { name: "Ahmad", settings: { theme: "dark" } } },
    { id: 2, profile: { name: "Fatima", settings: { theme: "light" } } },
  ],
};

// Immer allows "mutation" syntax but produces immutable result
const newState = produce(state, (draft) => {
  draft.users[0].profile.settings.theme = "light";
});

// Original unchanged
console.log(state.users[0].profile.settings.theme); // "dark"
console.log(newState.users[0].profile.settings.theme); // "light"
```

**Why this works**: Immer uses structural sharing. Looks like mutation but produces immutable result efficiently.

## Frozen Objects for True Immutability

**Context**: Preventing accidental mutations at runtime.

PASS: **Deeply Frozen (Maximum Safety)**:

```typescript
const transaction = Object.freeze({
  id: "TX001",
  amount: 1000,
  items: Object.freeze([Object.freeze({ name: "Item 1", price: 500 }), Object.freeze({ name: "Item 2", price: 500 })]),
});

// All mutation attempts fail in strict mode
transaction.amount = 2000; // Error in strict mode
transaction.items.push({ name: "Item 3", price: 100 }); // Error
transaction.items[0].price = 600; // Error
```

**Why this works**: `Object.freeze()` makes objects truly immutable at runtime. TypeScript enforces at compile time.
