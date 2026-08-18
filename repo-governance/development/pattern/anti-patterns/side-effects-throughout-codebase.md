---
title: "Anti-Pattern 9: Side Effects Throughout Codebase"
description: "Side effects such as logging or notifications are mixed directly into business logic instead of isolated at the boundary."
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: "Use when reviewing a function that mixes I/O or side effects with its core calculation."
---

# Anti-Pattern 9: Side Effects Throughout Codebase

**Problem**: Side effects mixed with business logic.

**Bad Example:**

```typescript
// Side effects everywhere (DO NOT DO THIS)
function calculateDiscount(user: User): number {
  db.logAccess(user.id); // Side effect!
  const discount = user.loyaltyPoints / 100;
  emailService.send(user.email, "Discount calculated"); // Side effect!
  return discount;
}
```

**Solution:**

```typescript
// Pure core
function calculateDiscount(loyaltyPoints: number): number {
  return loyaltyPoints / 100;
}

// Imperative shell (side effects at boundary)
async function applyDiscountWithLogging(user: User): Promise<number> {
  await db.logAccess(user.id); // Side effect isolated
  const discount = calculateDiscount(user.loyaltyPoints); // Pure
  await emailService.send(user.email, "Discount calculated"); // Side effect isolated
  return discount;
}
```

**Rationale:**

- Easier to test pure logic
- Side effects isolated and controlled
- Clear separation of concerns
- Better code organization
