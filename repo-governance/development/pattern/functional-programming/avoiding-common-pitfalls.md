---
description: "Common functional-programming mistakes - mutating function arguments, class-based mutable state, and mixing validation with I/O."
when_to_use: "Use when reviewing code for accidental mutation, mutable class state, or side effects mixed into pure logic."
---

# Avoiding Common Pitfalls

## Don't Mutate Function Arguments

FAIL: **Bad**:

```typescript
function addTransaction(transactions: Transaction[], newTx: Transaction) {
  transactions.push(newTx); // Mutates input
  return transactions;
}
```

PASS: **Good**:

```typescript
function addTransaction(transactions: readonly Transaction[], newTx: Transaction): readonly Transaction[] {
  return [...transactions, newTx];
}
```

## Avoid Class-Based OOP with Mutable State

FAIL: **Bad**:

```typescript
class ShoppingCart {
  private items: Item[] = [];

  addItem(item: Item): void {
    this.items.push(item); // Mutable state
  }

  removeItem(id: string): void {
    this.items = this.items.filter((i) => i.id !== id); // Mutates
  }
}
```

PASS: **Good**:

```typescript
interface ShoppingCart {
  readonly items: readonly Item[];
}

function addItem(cart: ShoppingCart, item: Item): ShoppingCart {
  return { items: [...cart.items, item] };
}

function removeItem(cart: ShoppingCart, id: string): ShoppingCart {
  return { items: cart.items.filter((i) => i.id !== id) };
}
```

## Keep Functions Pure, Move Side Effects to Edges

FAIL: **Bad**:

```typescript
function saveUser(user: User): void {
  // Validation mixed with I/O
  if (!user.email.includes("@")) {
    throw new Error("Invalid email");
  }
  database.users.insert(user); // Side effect
}
```

PASS: **Good**:

```typescript
// Pure validation
function isValidEmail(email: string): boolean {
  return email.includes("@") && email.includes(".");
}

function validateUser(user: User): ValidationResult {
  const errors: string[] = [];
  if (!isValidEmail(user.email)) {
    errors.push("Invalid email");
  }
  return { valid: errors.length === 0, errors };
}

// Imperative shell
async function saveUser(user: User): Promise<void> {
  const validation = validateUser(user); // Pure
  if (!validation.valid) {
    throw new Error(validation.errors.join(", "));
  }
  await database.users.insert(user); // Side effect at boundary
}
```
