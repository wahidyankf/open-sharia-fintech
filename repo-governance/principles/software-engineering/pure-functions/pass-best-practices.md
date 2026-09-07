---
description: Summarizes six concrete best practices for writing pure functions, from explicit dependencies to mock-free testing.
when_to_use: Use as a quick checklist when writing or reviewing TypeScript code for purity compliance.
---

# PASS: Best Practices

## 1. Make Dependencies Explicit

**Pass everything as arguments**:

```typescript
// PASS: All dependencies explicit
function calculateMurabahaTotal(cost: number, markupRate: number, taxRate: number): number {
  const markup = cost * markupRate;
  const subtotal = cost + markup;
  const tax = subtotal * taxRate;
  return subtotal + tax;
}
```

## 2. Return New Values, Don't Modify

**Create new data instead of mutating**:

```typescript
// PASS: Returns new array
function addItem(items: readonly Item[], newItem: Item): readonly Item[] {
  return [...items, newItem];
}

// FAIL: Mutates input
function addItem(items: Item[], newItem: Item): Item[] {
  items.push(newItem); // MUTATION
  return items;
}
```

## 3. Use Pure Functions for Business Logic

**All business rules should be pure**:

```typescript
// PASS: Pure business logic
function isEligibleForZakat(wealth: number, nisab: number): boolean {
  return wealth >= nisab;
}

function calculateProfit(revenue: number, expenses: number): number {
  return revenue - expenses;
}

function isHalalInvestment(asset: Asset): boolean {
  return !asset.categories.some((c) => HARAM_CATEGORIES.includes(c));
}
```

## 4. Isolate Side Effects at Boundaries

**Functional Core, Imperative Shell**:

```typescript
// CORE: Pure logic
function validateOrder(order: Order): ValidationResult {
  // Pure validation
}

function calculateOrderTotal(order: Order): number {
  // Pure calculation
}

// SHELL: Side effects at edges
async function processOrder(order: Order): Promise<void> {
  const validation = validateOrder(order); // Pure
  if (!validation.valid) throw new Error(validation.errors);

  const total = calculateOrderTotal(order); // Pure

  await database.orders.insert(order); // SIDE EFFECT
  await paymentGateway.charge(total); // SIDE EFFECT
  await emailService.sendConfirmation(order); // SIDE EFFECT
}
```

## 5. Test Pure Functions Without Mocks

**Simple, direct tests**:

```typescript
describe("calculateZakat", () => {
  it("calculates 2.5% for wealth above nisab", () => {
    expect(calculateZakat(10000, 5000)).toBe(250);
  });

  it("returns 0 for wealth below nisab", () => {
    expect(calculateZakat(3000, 5000)).toBe(0);
  });

  // No mocking, no setup, just inputs and outputs
});
```

## 6. Use Higher-Order Functions

**Compose pure functions**:

```typescript
// PASS: Pure higher-order functions
const pipe =
  (...fns) =>
  (x) =>
    fns.reduce((v, f) => f(v), x);

const processData = pipe(
  validateInput, // Pure
  transformData, // Pure
  calculateResults, // Pure
  formatOutput, // Pure
);

const result = processData(input);
```
