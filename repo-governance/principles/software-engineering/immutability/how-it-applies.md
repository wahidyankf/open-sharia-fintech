---
title: "How It Applies"
description: Shows immutable versus mutable patterns for variables and array operations in TypeScript.
category: explanation
subcategory: principles
tags:
  - principles
  - functional-programming
  - immutability
  - data-structures
  - concurrency
created: 2025-12-28
when_to_use: Use when implementing immutable variable declarations or array updates and needing a concrete before/after example.
---

# How It Applies

## Immutable Variables (const)

**Context**: Variable declarations in TypeScript/JavaScript.

PASS: **Immutable (Preferred)**:

```typescript
const user = { name: "Ahmad", balance: 1000 };
// user = { ... }  // FAIL: Error: Cannot reassign const

// Create new object instead of modifying
const updatedUser = { ...user, balance: 1200 };
// Original user unchanged: { name: "Ahmad", balance: 1000 }
// New value: { name: "Ahmad", balance: 1200 }
```

**Why this works**: `const` prevents reassignment. Spread operator creates new object. Original data preserved.

FAIL: **Mutable (Avoid)**:

```typescript
let user = { name: "Ahmad", balance: 1000 };
user.balance = 1200; // Mutates original object
// Original value lost, can't trace history
```

**Why this fails**: Mutable state. Previous balance lost. No audit trail of changes.

## Immutable Array Operations

**Context**: Working with arrays.

PASS: **Immutable (Preferred)**:

```typescript
const transactions = [
  { id: 1, amount: 100 },
  { id: 2, amount: 200 },
];

// Add item: Create new array
const withNewTransaction = [...transactions, { id: 3, amount: 300 }];

// Remove item: Create new array
const withoutFirst = transactions.slice(1);

// Update item: Create new array
const updated = transactions.map((tx) => (tx.id === 2 ? { ...tx, amount: 250 } : tx));

// Original unchanged
console.log(transactions); // Still [{id:1, amount:100}, {id:2, amount:200}]
```

**Why this works**: Each operation creates new array. Original preserved. Clear data lineage.

FAIL: **Mutable (Avoid)**:

```typescript
const transactions = [
  { id: 1, amount: 100 },
  { id: 2, amount: 200 },
];

transactions.push({ id: 3, amount: 300 }); // Mutates array
transactions.shift(); // Mutates array
transactions[0].amount = 250; // Mutates object in array

// Original data lost, no history
```

**Why this fails**: Array and objects mutated. History lost. Concurrent access unsafe.

## Immutable Object Updates

**Context**: Updating nested objects.

PASS: **Immutable (Preferred)**:

```typescript
interface Account {
  id: string;
  holder: { name: string; email: string };
  balance: number;
}

const account: Account = {
  id: "ACC001",
  holder: { name: "Ahmad", email: "ahmad@example.com" },
  balance: 1000,
};

// Update nested property immutably
const updatedAccount = {
  ...account,
  holder: {
    ...account.holder,
    email: "ahmad.new@example.com",
  },
};

// Original unchanged
console.log(account.holder.email); // "ahmad@example.com"
console.log(updatedAccount.holder.email); // "ahmad.new@example.com"
```

**Why this works**: Nested spread creates new objects at each level. Original preserved.

FAIL: **Mutable (Avoid)**:

```typescript
const account = {
  id: "ACC001",
  holder: { name: "Ahmad", email: "ahmad@example.com" },
  balance: 1000,
};

account.holder.email = "ahmad.new@example.com"; // Mutates nested object
// Original email lost, no audit trail
```

**Why this fails**: Mutation makes it impossible to trace what the email was before change.
