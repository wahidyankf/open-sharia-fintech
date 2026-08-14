---
title: "Anti-Patterns — Self-Documenting Code and Deferred Documentation"
description: Why self-documenting-code claims and deferred documentation both fail.
category: explanation
subcategory: principles
tags:
  - principles
  - documentation
created: 2025-12-28
when_to_use: Use when reviewing a change that skips documentation.
---

# Anti-Patterns — Self-Documenting Code and Deferred Documentation

## "Self-Documenting Code" Excuse

FAIL: **Problem**: Claiming code doesn't need documentation because it's "readable".

```typescript
// CLAIMED TO BE "SELF-DOCUMENTING"
const result = items
  .filter((i) => i.type === "murabahah")
  .map((i) => i.cost * 1.15)
  .reduce((sum, val) => sum + val, 0);
```

**Why it's bad**: Code shows WHAT is calculated, not WHY or in what context. Future maintainers don't know:

- Why filter for 'murabahah' specifically?
- Why multiply by 1.15 (is this a fixed markup? Shariah-compliant rate?)?
- What does this result represent?
- When should this calculation be used?

PASS: **Solution**: Add documentation explaining context and rationale.

```typescript
/**
 * Calculates total expected profit for all Murabahah contracts.
 *
 * Murabahah contracts use a fixed 15% markup (1.15 multiplier) as per
 * our Shariah board's approved profit structure for short-term asset financing.
 *
 * @param items - Array of financial contracts
 * @returns Total profit in currency units
 */
function calculateTotalMurabahahProfit(items: Contract[]): number {
  return items
    .filter((i) => i.type === "murabahah")
    .map((i) => i.cost * 1.15)
    .reduce((sum, val) => sum + val, 0);
}
```

## "We'll Document It Later"

FAIL: **Problem**: Writing code without documentation, planning to add it "later".

**Why it's bad**:

- "Later" never comes (other priorities emerge)
- Context is forgotten (what was obvious during coding is forgotten days later)
- Technical debt accumulates (undocumented code breeds more undocumented code)
- Quality suffers (documentation is treated as optional, not essential)

PASS: **Solution**: Documentation First - write docs BEFORE or WITH code, not after.

**Workflow**:

1. Write explanation document (what problem, what approach, why)
2. Write API documentation (function signatures, parameters)
3. Write code implementing the documented API
4. Write how-to guide (how to use the feature)
5. Update README with overview
