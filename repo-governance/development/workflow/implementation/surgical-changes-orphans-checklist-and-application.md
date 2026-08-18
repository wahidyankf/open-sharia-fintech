---
title: "Surgical Changes — Orphans, Checklist, and Application"
description: What to remove when your own changes create orphaned code, the pre-commit checklist, and how surgical changes relate to core principles and AI agents.
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
when_to_use: Use when deciding whether to remove code your change made unused, or before committing a surgical change.
---

# Surgical Changes — Orphans, Checklist, and Application

## When YOUR Changes Create Orphans

**Do remove**:

- Imports that YOUR changes made unused
- Variables that YOUR changes made unused
- Functions that YOUR changes made unused

**Don't remove**:

- Pre-existing dead code
- Imports used elsewhere (verify with Grep)
- Code that might be used by other modules

### Example: Import Cleanup

**PASS - Clean up your own mess**:

```typescript
-import { oldFormatter, calculateTotal } from './utils'  // Removed oldFormatter (you stopped using it)
+import { calculateTotal } from './utils'

function processOrder(items: Item[]) {
-  const formatted = oldFormatter(items)  // You removed this line
-  return calculateTotal(formatted)
+  return calculateTotal(items)          // You changed to this
}

// Note: calculateTotal is still used, so import stays
```

**FAIL - Removing unrelated dead code**:

```typescript
-import { oldFormatter, calculateTotal, unusedHelper } from './utils'
+import { calculateTotal } from './utils'

// Removed unusedHelper from import even though YOUR changes didn't affect it
// Don't do this - mention it instead
```

## Surgical Changes Checklist

Before committing:

- [ ] Every changed line traces to the user's request
- [ ] No "improvements" to adjacent code
- [ ] No refactoring of unrelated code
- [ ] Existing style matched consistently
- [ ] Only orphans created BY YOUR changes were removed
- [ ] Pre-existing errors were fixed at root cause (see [Proactive Preexisting Error Resolution](../../practice/proactive-preexisting-error-resolution.md)), or if scope is too large, a follow-up plan was created in `plans/in-progress/` and execution has begun

## Relationship to Principles

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: Minimal changes reduce complexity
- **[Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md)**: Explicit scope boundaries prevent scope creep
- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Clear traceability from request to change

## For AI Agents

Agents must practice surgical precision by:

1. **Scoping changes** to exactly what was requested
2. **Avoiding refactoring** unrelated code
3. **Matching existing patterns** rather than imposing preferences
4. **Fixing preexisting errors at root cause** — not ignoring them, not patching around them, not mentioning without action. See [Proactive Preexisting Error Resolution](../../practice/proactive-preexisting-error-resolution.md) for scope judgment and full requirements.
5. **Cleaning up only** what their changes made unused

This practice is especially important in large codebases where unintended changes can introduce bugs or merge conflicts.
