---
title: "TypeScript-Specific Patterns"
description: "TypeScript-specific functional patterns - readonly types, branded types, and discriminated unions for state modeling."
category: explanation
subcategory: development
tags:
  - development
  - functional-programming
  - immutability
  - pure-functions
  - typescript
created: 2025-12-28
when_to_use: "Use when you need a TypeScript-specific technique for enforcing immutability or modeling state explicitly."
---

# TypeScript-Specific Patterns

## Readonly Types

**Use TypeScript's readonly modifiers**:

```typescript
// Readonly object properties
interface User {
  readonly id: string;
  readonly name: string;
  readonly email: string;
}

// Readonly arrays
type ReadonlyNumbers = readonly number[];

// Deep readonly with utility type
type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};

interface Config {
  database: {
    host: string;
    port: number;
  };
}

type FrozenConfig = DeepReadonly<Config>;
```

## Branded Types for Type Safety

**Create distinct types even with same underlying type**:

```typescript
// Branded types
type SAR = number & { readonly __brand: "SAR" };
type USD = number & { readonly __brand: "USD" };

function toSAR(amount: number): SAR {
  return amount as SAR;
}

function toUSD(amount: number): USD {
  return amount as USD;
}

function convertSARtoUSD(sar: SAR, rate: number): USD {
  return toUSD(sar / rate);
}

// PASS: Type-safe
const sar = toSAR(1000);
const usd = convertSARtoUSD(sar, 3.75);

// FAIL: Compile error - can't pass USD where SAR expected
// convertSARtoUSD(usd, 3.75);
```

## Discriminated Unions for State Modeling

**Model states explicitly**:

```typescript
type PaymentState =
  | { type: "pending"; orderId: string }
  | { type: "processing"; orderId: string; transactionId: string }
  | { type: "completed"; orderId: string; transactionId: string; receiptId: string }
  | { type: "failed"; orderId: string; error: string };

function getPaymentStatus(state: PaymentState): string {
  switch (state.type) {
    case "pending":
      return "Payment is pending";
    case "processing":
      return `Processing transaction ${state.transactionId}`;
    case "completed":
      return `Payment completed. Receipt: ${state.receiptId}`;
    case "failed":
      return `Payment failed: ${state.error}`;
  }
}
```
