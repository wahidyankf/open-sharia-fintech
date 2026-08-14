---
title: "Anti-Pattern 6: Monolithic Functions"
description: "A single large function performs many unrelated responsibilities instead of composing small functions."
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: "Use when reviewing a function that mixes validation, transformation, filtering, and aggregation together."
---

# Anti-Pattern 6: Monolithic Functions

**Problem**: Large functions doing too many things.

**Bad Example:**

```typescript
// Monolithic function (DO NOT DO THIS)
function processUserData(users: User[]): ProcessedData {
  // 200 lines of complex logic
  // Validation, transformation, filtering, sorting, aggregation...
  // All mixed together
}
```

**Solution:**

```typescript
// Composed from small functions
const validateUser = (user: User) => user.email && user.name;
const isActive = (user: User) => user.status === "active";
const toDTO = (user: User) => ({ id: user.id, name: user.name });

function processUserData(users: User[]): ProcessedData {
  return users.filter(validateUser).filter(isActive).map(toDTO);
}
```

**Rationale:**

- Small, testable units
- Reusable building blocks
- Clear intent and naming
- Easier to maintain
