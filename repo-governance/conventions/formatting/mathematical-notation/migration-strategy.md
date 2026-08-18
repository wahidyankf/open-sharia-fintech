---
title: "Migration Strategy"
description: Rules for new documentation, updating existing documentation opportunistically, and a worked example converting plain-text math to LaTeX.
when_to_use: Use when editing a document that has plain-text math and deciding whether and how to convert it to LaTeX.
category: explanation
subcategory: conventions
tags:
  - latex
  - mathematics
  - formulas
  - notation
  - conventions
created: 2025-12-02
---

# Migration Strategy

## New Documentation

All new documentation MUST use LaTeX for mathematical notation:

- Write formulas in LaTeX from the start
- Define variables clearly
- Test rendering on GitHub

## Existing Documentation

Update existing docs **when modified** (not retroactively):

- If editing a document with plain text math, convert to LaTeX
- Don't create standalone PRs just to convert notation
- Gradual migration as documents are naturally updated

**Why**: Avoid unnecessary churn. Convert to LaTeX when there's a natural reason to edit the file.

## Converting Plain Text to LaTeX

**Before** (plain text):

```markdown
The WACC formula is: WACC = (E/V) _ r_e + (D/V) _ r_d \* (1 - T_c)
```

**After** (LaTeX):

```markdown
The WACC formula is:

$$
WACC = \frac{E}{V} \times r_e + \frac{D}{V} \times r_d \times (1 - T_c)
$$

Where:

- $E$ = market value of equity
- $D$ = market value of debt
- $V$ = total market value ($V = E + D$)
- $r_e$ = cost of equity
- $r_d$ = cost of debt
- $T_c$ = corporate tax rate
```

**Process**:

1. Identify mathematical expressions in plain text
2. Convert to inline `$...$` or display `$$...$$`
3. Add variable definitions
4. Test rendering
5. Commit with descriptive message: `docs: convert math notation to LaTeX`
