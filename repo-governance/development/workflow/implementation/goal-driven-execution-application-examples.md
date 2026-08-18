---
title: "Goal-Driven Execution — Application Examples"
description: Two worked examples of goal-driven execution end to end - a new API endpoint and a bug fix.
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
when_to_use: Use as a worked reference when applying goal-driven execution to a new endpoint or a bug fix task.
---

# Goal-Driven Execution — Application Examples

## Example 1: API Endpoint Addition

**Goal**: Add `/users/{id}` endpoint

**Success Criteria**:

- Returns 200 with user JSON for valid ID
- Returns 404 for non-existent ID
- Returns 400 for invalid ID format

**Execution**:

```bash
# Step 1: Write tests
$ cat > test/api/users.test.ts

# Step 2: Run tests (expect failures)
$ npm test
FAIL: 3 tests (endpoint not implemented)

# Step 3: Implement endpoint
$ # ... code changes ...

# Step 4: Run tests again
$ npm test
FAIL: 1 test (404 case not handling correctly)

# Step 5: Fix and verify
$ # ... fix 404 handling ...
$ npm test
PASS: All tests passed ✓

# Step 6: Manual verification
$ curl http://localhost:3000/users/123
{"id": 123, "name": "John"} ✓
```

## Example 2: Bug Fix

**Goal**: Fix "cart total incorrect when discount applied"

**Success Criteria**:

- Test reproduces the bug (fails initially)
- Fix makes test pass
- All existing tests still pass

**Execution**:

```bash
# Step 1: Write test that reproduces bug
describe('Cart total with discount', () => {
  it('applies 10% discount correctly', () => {
    const cart = { items: [{ price: 100 }], discount: 0.1 }
    expect(calculateTotal(cart)).toBe(90) // Currently fails: returns 100
  })
})

# Step 2: Verify test fails (confirms bug exists)
$ npm test
FAIL: expected 90, got 100 ✓ (bug confirmed)

# Step 3: Fix the bug
function calculateTotal(cart) {
  const subtotal = cart.items.reduce((sum, item) => sum + item.price, 0)
-  return subtotal
+  return subtotal * (1 - cart.discount)
}

# Step 4: Verify test passes
$ npm test
PASS: applies 10% discount correctly ✓

# Step 5: Verify no regressions
$ npm test
PASS: All 47 tests passed ✓
```
