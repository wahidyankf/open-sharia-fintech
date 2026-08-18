---
title: "Anti-Patterns"
description: Catalogs common purity anti-patterns — side-effecting functions, hidden randomness, reading current time, and global state dependencies — with fixes.
category: explanation
subcategory: principles
tags:
  - principles
  - functional-programming
  - pure-functions
  - testability
  - determinism
created: 2025-12-28
when_to_use: Use when reviewing code for hidden non-determinism or side effects and refactoring toward pure functions.
---

# Anti-Patterns

## Functions with Side Effects

FAIL: **Problem**: Function modifies external state.

```typescript
// FAIL: Impure - modifies database
function addTransaction(transaction) {
  database.transactions.insert(transaction); // SIDE EFFECT
  return transaction.id;
}

// Hard to test - requires database
// Not deterministic - DB state affects result
// Concurrency issues
```

PASS: **Solution**: Separate pure logic from I/O.

```typescript
// PASS: Pure - prepares data
function prepareTransaction(from: string, to: string, amount: number): Transaction {
  return {
    id: generateId(),
    from,
    to,
    amount,
    timestamp: Date.now(),
  };
}

// PASS: Impure shell - handles I/O
async function saveTransaction(transaction: Transaction): Promise<void> {
  await database.transactions.insert(transaction);
}

// Clear separation: logic (pure) vs I/O (impure)
```

## Hidden Randomness

FAIL: **Problem**: Function uses random values internally.

```typescript
// FAIL: Non-deterministic
function generateContractId(): string {
  return `CONTRACT-${Math.random()}`; // RANDOM
}

// Different result every call
generateContractId(); // "CONTRACT-0.123"
generateContractId(); // "CONTRACT-0.456"
```

PASS: **Solution**: Pass randomness as input.

```typescript
// PASS: Deterministic - randomness passed in
function generateContractId(random: number): string {
  return `CONTRACT-${random}`;
}

// Caller controls randomness
generateContractId(Math.random()); // Randomness at boundary
generateContractId(0.5); // Deterministic for testing
```

## Reading Current Time

FAIL: **Problem**: Function reads current time internally.

```typescript
// FAIL: Non-deterministic
function isContractExpired(expiryDate: Date): boolean {
  const now = new Date(); // READS CURRENT TIME
  return now > expiryDate;
}

// Different result at different times
```

PASS: **Solution**: Pass current time as input.

```typescript
// PASS: Deterministic
function isContractExpired(expiryDate: Date, now: Date): boolean {
  return now > expiryDate;
}

// Caller controls "now"
isContractExpired(expiryDate, new Date()); // Real time
isContractExpired(expiryDate, new Date("2025-12-28")); // Fixed time for testing
```

## Global State Dependencies

FAIL: **Problem**: Function depends on global variable.

```typescript
// FAIL: Depends on global
let exchangeRate = 3.75; // SAR to USD

function convertToUSD(sar: number): number {
  return sar / exchangeRate; // HIDDEN DEPENDENCY
}

// Result changes if exchangeRate changes
// Hard to test with different rates
```

PASS: **Solution**: Pass dependencies explicitly.

```typescript
// PASS: Explicit dependency
function convertToUSD(sar: number, exchangeRate: number): number {
  return sar / exchangeRate;
}

// All inputs explicit
convertToUSD(1000, 3.75); // 266.67
convertToUSD(1000, 4.0); // 250 (different rate)
```
