---
title: "Surgical Changes — Application Examples"
description: Worked bug-fix and validation examples contrasting scope-creep changes with surgical ones.
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
when_to_use: Use as a worked reference when deciding whether a specific edit is surgical or has drifted into scope creep.
---

# Surgical Changes — Application Examples

## Example 1: Bug Fix in Payment Module

**FAIL - Scope creep**:

```typescript
function processPayment(amount: number, userId: string) {
-  const fee = calculateFee(amount)  // Fixed typo in function name
+  const fee = calculateFee(amount)
-  const total = amount + fee         // Reformatted this line
+  const total = amount + fee
-  // TODO: Add validation             // Removed unrelated TODO
-  const user = getUser(userId)        // Refactored to use new helper
+  const user = await getUserById(userId)
  return chargeCard(user, total)
}

// Added new helper function (scope creep)
+async function getUserById(id: string) {
+  return await db.users.findOne({ id })
+}
```

**PASS - Surgical change**:

```typescript
function processPayment(amount: number, userId: string) {
-  const fee = calculateFee(amount)  // Fixed the actual bug only
+  const fee = calculateFee(amount)
  const total = amount + fee
  // TODO: Add validation             // Left unrelated TODO
  const user = getUser(userId)        // Left existing code alone
  return chargeCard(user, total)
}
```

## Example 2: Adding Validation

**FAIL - While I'm here syndrome**:

```typescript
function createUser(email: string, name: string) {
+  // Added validation (requested)
+  if (!email || !email.includes('@')) {
+    throw new Error('Invalid email')
+  }
-  // Create user                      // "Improved" comment
+  // Creates a new user in the database
-  const user = { email, name }        // "Improved" structure
+  const user = {
+    email: email.toLowerCase(),       // Added normalization (not asked)
+    name: name.trim(),                // Added trimming (not asked)
+    createdAt: new Date(),            // Added timestamp (not asked)
+  }
-  return db.save(user)                // Refactored to async/await
+  return await db.users.insert(user)
}
```

**PASS - Only what was asked**:

```typescript
function createUser(email: string, name: string) {
+  // Added validation (requested)
+  if (!email || !email.includes('@')) {
+    throw new Error('Invalid email')
+  }
  // Create user                       // Left existing comment
  const user = { email, name }         // Left existing structure
  return db.save(user)                 // Left existing implementation
}
```
