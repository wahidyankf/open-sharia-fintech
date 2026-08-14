---
title: "Stage 2: Make It Right"
description: The second workflow stage - refactor working code for readability, maintainability, and clean code principles.
category: explanation
subcategory: development
tags:
  - development
  - workflow
  - implementation
  - optimization
  - refactoring
  - surgical-changes
  - goal-driven
  - test-driven
created: 2025-12-15
when_to_use: Use once functionality from Stage 1 works and tests pass, before considering any optimization.
---

# Stage 2: Make It Right

**Goal**: Refactor code for readability, maintainability, and clean code principles.

**What to do**:

- Extract repeated code into functions (Rule of Three)
- Use meaningful variable and function names
- Apply clean code principles (small functions, single responsibility)
- Add proper error handling
- Improve type safety
- Write comprehensive tests
- Add documentation where needed

**What NOT to do**:

- FAIL: Don't optimize for performance yet
- FAIL: Don't add features not in requirements
- FAIL: Don't change functionality (keep tests green)

**Example**:

```typescript
// PASS: MAKE IT RIGHT - Clean, readable, maintainable
interface OrderItem {
  price: number;
  quantity: number;
}

function calculateOrderTotal(items: OrderItem[]): number {
  return items.reduce((total, item) => total + calculateItemTotal(item), 0);
}

function calculateItemTotal(item: OrderItem): number {
  return item.price * item.quantity;
}

// Tests remain green - functionality unchanged
```

**When you're done**: Code is clean, readable, well-tested, maintainable.
