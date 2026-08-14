---
title: "PASS: Best Practices"
description: Summarizes six concrete best practices for writing immutable code, from const-by-default to typed readonly enforcement.
category: explanation
subcategory: principles
tags:
  - principles
  - functional-programming
  - immutability
  - data-structures
  - concurrency
created: 2025-12-28
when_to_use: Use as a quick checklist when writing or reviewing TypeScript code for immutability compliance.
---

# PASS: Best Practices

## 1. Use const by Default

**Always start with const**:

```typescript
PASS: const user = { name: "Ahmad" };
let user = { name: "Ahmad" }; // Only if you MUST reassign
FAIL: var user = { name: "Ahmad" }; // Never use var
```

## 2. Use Immutable Array Methods

**Prefer map/filter/reduce over loops**:

```typescript
// PASS: Immutable transformations
const doubled = numbers.map((n) => n * 2);
const evens = numbers.filter((n) => n % 2 === 0);
const sum = numbers.reduce((acc, n) => acc + n, 0);

// FAIL: Avoid mutation in loops
const doubled = [];
for (let i = 0; i < numbers.length; i++) {
  doubled.push(numbers[i] * 2); // Creates and mutates array
}
```

## 3. Use Spread Operator for Shallow Copies

**Copy objects and arrays**:

```typescript
// PASS: Objects
const updated = { ...original, field: newValue };

// PASS: Arrays
const newArray = [...oldArray, newItem];
const merged = [...array1, ...array2];
```

## 4. Use Immer for Deep Nested Updates

**Complex state updates**:

```typescript
import { produce } from "immer";

// PASS: Complex update with Immer
const newState = produce(state, (draft) => {
  draft.users[userId].profile.settings.theme = "dark";
  draft.users[userId].lastUpdated = Date.now();
});
```

## 5. Make Immutability Explicit with Types

**Use readonly modifiers**:

```typescript
interface Transaction {
  readonly id: string;
  readonly amount: number;
  readonly timestamp: number;
}

type ReadonlyArray<T> = readonly T[];

// Compile-time enforcement of immutability
```

## 6. Return New Values from Functions

**Never mutate, always return**:

```typescript
// PASS: Pure function returning new value
function calculateZakat(wealth: number): number {
  return wealth * 0.025;
}

// PASS: Returns new object
function applyDiscount(order: Order, discount: number): Order {
  return {
    ...order,
    total: order.total * (1 - discount),
  };
}
```
