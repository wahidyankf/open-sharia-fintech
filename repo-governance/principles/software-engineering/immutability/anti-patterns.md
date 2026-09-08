---
description: Catalogs common mutability anti-patterns — mutating function arguments, shared mutable state, and hidden mutations in methods — with fixes.
when_to_use: Use when reviewing code for accidental mutation bugs or refactoring a mutable design toward immutability.
---

# Anti-Patterns

## Mutating Function Arguments

FAIL: **Problem**: Function modifies input data.

```typescript
// FAIL: Mutates input array
function addTransaction(transactions, newTx) {
  transactions.push(newTx); // MUTATES INPUT
  return transactions;
}

const myTransactions = [{ id: 1, amount: 100 }];
addTransaction(myTransactions, { id: 2, amount: 200 });
// myTransactions is now modified - side effect!
```

**Why it's bad**: Caller's data changed unexpectedly. Breaks assumptions. Hard to debug.

PASS: **Solution**:

```typescript
function addTransaction(transactions, newTx) {
  return [...transactions, newTx]; // Returns new array
}

const myTransactions = [{ id: 1, amount: 100 }];
const updated = addTransaction(myTransactions, { id: 2, amount: 200 });
// myTransactions unchanged, updated is new array
```

## Shared Mutable State

FAIL: **Problem**: Multiple parts of code share and mutate same object.

```typescript
// FAIL: Shared mutable state
const appState = { currentUser: null, balance: 0 };

function login(user) {
  appState.currentUser = user; // MUTATES SHARED STATE
}

function updateBalance(amount) {
  appState.balance += amount; // MUTATES SHARED STATE
}

// Different parts of app mutate appState - hard to track changes
```

**Why it's bad**: Changes happen anywhere in codebase. Difficult to trace bugs. Race conditions in concurrent code.

PASS: **Solution**:

```typescript
interface AppState {
  currentUser: User | null;
  balance: number;
}

function login(state: AppState, user: User): AppState {
  return { ...state, currentUser: user };
}

function updateBalance(state: AppState, amount: number): AppState {
  return { ...state, balance: state.balance + amount };
}

// Each function returns new state, original unchanged
```

## Hidden Mutations in Methods

FAIL: **Problem**: Class methods mutate internal state.

```typescript
// FAIL: Mutable class
class ShoppingCart {
  private items = [];

  addItem(item) {
    this.items.push(item); // MUTATES INTERNAL STATE
  }

  removeItem(itemId) {
    this.items = this.items.filter((i) => i.id !== itemId); // MUTATES
  }
}

const cart = new ShoppingCart();
cart.addItem({ id: 1, name: "Book" });
// cart state changed - no history, can't undo
```

**Why it's bad**: State changes invisible to caller. Can't track history. Concurrent access unsafe.

PASS: **Solution** (Functional approach):

```typescript
interface ShoppingCart {
  items: readonly Item[];
}

function addItem(cart: ShoppingCart, item: Item): ShoppingCart {
  return { items: [...cart.items, item] };
}

function removeItem(cart: ShoppingCart, itemId: string): ShoppingCart {
  return { items: cart.items.filter((i) => i.id !== itemId) };
}

let cart: ShoppingCart = { items: [] };
cart = addItem(cart, { id: 1, name: "Book" });
// Each operation creates new cart, history preserved
```
