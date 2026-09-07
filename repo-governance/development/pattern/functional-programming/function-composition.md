---
description: "The pipe pattern, compose pattern, and higher-order functions for building complex behaviour from simple functions."
when_to_use: "Use when you need to combine several small functions into a single pipeline or transformation."
---

# Function Composition

## Pipe Pattern

**Compose functions left-to-right**:

```typescript
const pipe =
  <T>(...fns: Array<(arg: T) => T>) =>
  (value: T): T =>
    fns.reduce((acc, fn) => fn(acc), value);

// Pure functions
const trim = (s: string) => s.trim();
const lowercase = (s: string) => s.toLowerCase();
const removeSpaces = (s: string) => s.replace(/\s+/g, "");

// Compose into pipeline
const normalize = pipe(trim, lowercase, removeSpaces);

normalize("  Hello World  "); // "helloworld"
```

## Compose Pattern

**Compose functions right-to-left**:

```typescript
const compose =
  <T>(...fns: Array<(arg: T) => T>) =>
  (value: T): T =>
    fns.reduceRight((acc, fn) => fn(acc), value);

// Same functions as pipe example
const normalize = compose(removeSpaces, lowercase, trim);

normalize("  Hello World  "); // "helloworld"
// Executes: removeSpaces(lowercase(trim(input)))
```

## Higher-Order Functions

**Functions that return functions**:

```typescript
// Higher-order function
function multiplyBy(factor: number): (n: number) => number {
  return (n: number) => n * factor;
}

const double = multiplyBy(2);
const triple = multiplyBy(3);

double(5); // 10
triple(5); // 15

// Practical example: Discount calculator
function createDiscountCalculator(rate: number): (price: number) => number {
  return (price: number) => price * (1 - rate);
}

const apply10Percent = createDiscountCalculator(0.1);
const apply25Percent = createDiscountCalculator(0.25);

apply10Percent(100); // 90
apply25Percent(100); // 75
```
