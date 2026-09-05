---
title: "Practice 7: Compose Small Functions"
description: "Build complex behaviour from small, composable, reusable functions rather than one large function."
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: "Use when a function is growing large and could be decomposed into smaller composable functions."
---

# Practice 7: Compose Small Functions

**Principle**: Build complex behaviour from small, composable functions.

**Good Example:**

```typescript
const isActive = (user: User) => user.status === "active";
const hasEmail = (user: User) => !!user.email;
const canReceiveEmail = (user: User) => isActive(user) && hasEmail(user);

const emailableUsers = users.filter(canReceiveEmail);
```

**Bad Example:**

```typescript
// Monolithic function
const emailableUsers = users.filter((user) => {
  // 50 lines of complex logic...
});
```

**Rationale:**

- Reusable building blocks
- Easier to test individual functions
- Clear intent and naming
- Supports functional pipelines
