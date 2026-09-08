---
description: "How to prefer const, use the spread operator for object updates, and use immutable array methods instead of mutation."
when_to_use: "Use when updating a primitive, object, or array value and need the immutable equivalent of a mutating operation."
---

# Immutability Patterns — Primitives, Objects, and Arrays

## Use const by Default

**Prefer const over let, never use var**:

```typescript
// PASS: Prefer const
const user = { name: "Ahmad", balance: 1000 };

// Use let only when reassignment necessary
let counter = 0;
counter += 1;

// FAIL: Never use var
var oldStyle = "bad"; // Don't do this
```

## Immutable Object Updates

**Use spread operator for shallow updates**:

```typescript
// PASS: Spread operator - creates new object
const user = { name: "Ahmad", email: "old@example.com", balance: 1000 };
const updatedUser = { ...user, email: "new@example.com" };

// PASS: Nested updates with multiple spreads
const account = {
  id: "ACC001",
  holder: { name: "Ahmad", email: "ahmad@example.com" },
  balance: 1000,
};

const updatedAccount = {
  ...account,
  holder: {
    ...account.holder,
    email: "ahmad.new@example.com",
  },
};

// FAIL: Mutation - avoid
user.email = "new@example.com"; // Mutates original
```

## Immutable Array Operations

**Use immutable array methods**:

```typescript
const numbers = [1, 2, 3, 4, 5];

// PASS: Immutable operations - return new arrays
const doubled = numbers.map((n) => n * 2);
const evens = numbers.filter((n) => n % 2 === 0);
const sum = numbers.reduce((acc, n) => acc + n, 0);
const first3 = numbers.slice(0, 3);
const withSix = [...numbers, 6];

// FAIL: Mutable operations - avoid
numbers.push(6); // Mutates
numbers.pop(); // Mutates
numbers.splice(0, 1); // Mutates
numbers.sort(); // Mutates
```
