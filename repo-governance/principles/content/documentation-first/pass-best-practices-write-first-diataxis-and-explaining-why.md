---
title: "PASS: Best Practices — Write First, Diátaxis, and Explaining WHY"
description: Write docs first, use Diátaxis, explain WHY, and give examples.
category: explanation
subcategory: principles
tags:
  - principles
  - documentation
created: 2025-12-28
when_to_use: Use as a checklist when starting new documentation.
---

# PASS: Best Practices — Write First, Diátaxis, and Explaining WHY

## 1. Write Documentation BEFORE or WITH Code

**Documentation First approach**:

1. Start with explanation document (context, problem, approach)
2. Write API documentation (signatures, parameters, examples)
3. Implement code matching the documented API
4. Write how-to guide teaching usage
5. Update README with overview

**Why this works**: Documentation drives design. Explaining the API before writing it reveals design flaws early.

## 2. Use the Diátaxis Framework

Organize documentation into four categories:

- **Tutorials**: Learning-oriented (teach newcomers step-by-step)
- **How-To Guides**: Problem-oriented (solve specific problems)
- **Reference**: Information-oriented (technical specifications, API details)
- **Explanation**: Understanding-oriented (concepts, architecture, decisions)

See [Diátaxis Framework](../../../conventions/structure/diataxis-framework.md) for complete details.

**Why this works**: Different audiences need different documentation types. Organizing by purpose makes information findable.

## 3. Document the WHY, Not Just the WHAT

**Code shows WHAT**. Comments and documentation explain **WHY**.

```typescript
// FAIL: BAD COMMENT - Repeats what code already shows
// Loop through items and add them
for (const item of items) {
  total += item.value;
}

// PASS: GOOD COMMENT - Explains WHY
// Murabahah contracts require total cost calculation before applying
// markup. This ensures profit is calculated on actual asset cost, not
// estimated values (Shariah compliance requirement).
for (const item of items) {
  total += item.value;
}
```

## 4. Provide Examples

Every piece of documentation should include examples:

- **API docs**: Show function calls with realistic parameters and expected outputs
- **How-to guides**: Include complete, working examples users can copy
- **Explanations**: Use concrete scenarios to illustrate abstract concepts

**Why this works**: Examples make abstract concepts concrete. Users learn faster from examples than from descriptions.
