---
description: "Examples of basic pure functions, pure data transformations, and the functional core/imperative shell split."
when_to_use: "Use when writing a function and want a worked example of keeping it pure versus isolating its side effects."
---

# Pure Function Patterns

## Basic Pure Functions

**All inputs as arguments, no side effects**:

```typescript
// PASS: Pure - deterministic, no side effects
function calculateZakat(wealth: number, nisab: number): number {
  if (wealth < nisab) {
    return 0;
  }
  return wealth * 0.025;
}

// FAIL: Impure - depends on global, has side effect
let totalZakat = 0;
function calculateZakat(wealth: number): number {
  const zakat = wealth * 0.025;
  totalZakat += zakat; // Side effect
  return zakat;
}
```

## Pure Data Transformations

**Transform data without mutations**:

```typescript
interface Transaction {
  readonly id: string;
  readonly amount: number;
  readonly timestamp: number;
}

// PASS: Pure transformation
function addTimestamp(transaction: Omit<Transaction, "timestamp">): Transaction {
  return {
    ...transaction,
    timestamp: Date.now(),
  };
}

// PASS: Pure filtering
function filterLargeTransactions(transactions: readonly Transaction[], threshold: number): readonly Transaction[] {
  return transactions.filter((tx) => tx.amount > threshold);
}

// PASS: Pure mapping
function convertToUSD(transactions: readonly Transaction[], exchangeRate: number): readonly Transaction[] {
  return transactions.map((tx) => ({
    ...tx,
    amount: tx.amount / exchangeRate,
  }));
}
```

## Functional Core, Imperative Shell

**Separate pure logic from side effects**:

```typescript
// FUNCTIONAL CORE: Pure business logic
interface Order {
  readonly items: readonly Item[];
  readonly discount: number;
}

function calculateSubtotal(items: readonly Item[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

function applyDiscount(subtotal: number, discount: number): number {
  return subtotal * (1 - discount);
}

function calculateTotal(order: Order): number {
  const subtotal = calculateSubtotal(order.items);
  return applyDiscount(subtotal, order.discount);
}

// IMPERATIVE SHELL: Side effects at boundaries
async function processOrder(order: Order): Promise<void> {
  // Pure calculation
  const total = calculateTotal(order);

  // Side effects at boundary
  await database.orders.insert({ ...order, total });
  await paymentGateway.charge(order.customerId, total);
  await emailService.sendConfirmation(order.customerEmail, total);
}
```
