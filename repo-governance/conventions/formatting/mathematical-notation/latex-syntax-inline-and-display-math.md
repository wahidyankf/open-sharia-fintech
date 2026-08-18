---
title: "LaTeX Syntax: Inline and Display Math"
description: The `$...$` inline math syntax and `$$...$$` display math syntax, with when to use each.
when_to_use: Use when writing a LaTeX expression and deciding between inline and display math syntax.
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

# LaTeX Syntax: Inline and Display Math

## LaTeX Syntax

### Inline Math

Use single dollar signs `$...$` for inline mathematical expressions within text:

```markdown
The cost of equity $r_e$ is calculated using the formula $r_e = r_f + \beta \times (r_m - r_f)$.
```

**Renders as:**

The cost of equity $r_e$ is calculated using the formula $r_e = r_f + \beta \times (r_m - r_f)$.

**When to use inline math:**

- Variables within sentences ($x$, $r_f$, $\beta$)
- Simple expressions embedded in text ($a + b$, $n^2$)
- Mathematical terms in running text

### Display Math

Use double dollar signs `$$...$$` for standalone equations on their own line:

```markdown
The Weighted Average Cost of Capital (WACC) formula:

$$
WACC = \frac{E}{V} \times r_e + \frac{D}{V} \times r_d \times (1 - T_c)
$$
```

**Renders as:**

The Weighted Average Cost of Capital (WACC) formula:

$$
WACC = \frac{E}{V} \times r_e + \frac{D}{V} \times r_d \times (1 - T_c)
$$

**When to use display math:**

- Important formulas that deserve emphasis
- Complex multi-line expressions
- Equations that should stand out visually
- Formulas that need to be referenced or cited
