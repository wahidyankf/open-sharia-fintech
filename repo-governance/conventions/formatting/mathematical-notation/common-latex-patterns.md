---
title: "Common LaTeX Patterns"
description: Reference patterns for subscripts/superscripts, Greek letters, fractions, summations/products, square roots, and mathematical operators.
when_to_use: Use when you need the LaTeX command for a subscript, Greek letter, fraction, summation, square root, or operator.
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

# Common LaTeX Patterns

## Subscripts and Superscripts

Use `_` for subscripts and `^` for superscripts:

```markdown
- Single character: $r_f$, $x^2$
- Multiple characters (use braces): $r_{free}$, $x^{2n}$
- Combined: $x_i^2$, $r_{i,t}^{adjusted}$
```

**Renders as:**

- Single character: $r_f$, $x^2$
- Multiple characters (use braces): $r_{free}$, $x^{2n}$
- Combined: $x_i^2$, $r_{i,t}^{adjusted}$

## Greek Letters

Precede with backslash:

```markdown
Common in finance:

- $\alpha$ (alpha) - excess return
- $\beta$ (beta) - systematic risk
- $\gamma$ (gamma) - risk aversion
- $\delta$ (delta) - change/derivative
- $\sigma$ (sigma) - standard deviation
- $\mu$ (mu) - mean/expected value
- $\pi$ (pi) - profit
- $\rho$ (rho) - correlation coefficient
```

**Renders as:**

Common in finance:

- $\alpha$ (alpha) - excess return
- $\beta$ (beta) - systematic risk
- $\gamma$ (gamma) - risk aversion
- $\delta$ (delta) - change/derivative
- $\sigma$ (sigma) - standard deviation
- $\mu$ (mu) - mean/expected value
- $\pi$ (pi) - profit
- $\rho$ (rho) - correlation coefficient

## Fractions

Use `\frac{numerator}{denominator}`:

```markdown
Simple fraction: $\frac{E}{V}$

Complex fraction: $\frac{E}{E + D}$

Nested: $\frac{1}{1 + \frac{r}{n}}$
```

**Renders as:**

Simple fraction: $\frac{E}{V}$

Complex fraction: $\frac{E}{E + D}$

Nested: $\frac{1}{1 + \frac{r}{n}}$

## Summations and Products

Use `\sum` and `\prod`:

```markdown
Sum: $\sum_{i=1}^{n} x_i$

Weighted sum: $\sum_{i=1}^{n} w_i \times r_i$

Product: $\prod_{i=1}^{n} (1 + r_i)$
```

**Renders as:**

Sum: $\sum_{i=1}^{n} x_i$

Weighted sum: $\sum_{i=1}^{n} w_i \times r_i$

Product: $\prod_{i=1}^{n} (1 + r_i)$

## Square Roots

Use `\sqrt`:

```markdown
Square root: $\sqrt{x}$

Nth root: $\sqrt[n]{x}$

Complex: $\sqrt{(x_1 - \mu)^2 + (x_2 - \mu)^2}$
```

**Renders as:**

Square root: $\sqrt{x}$

Nth root: $\sqrt[n]{x}$

Complex: $\sqrt{(x_1 - \mu)^2 + (x_2 - \mu)^2}$

## Mathematical Operators

Common operators:

```markdown
- Multiplication: $a \times b$ or $a \cdot b$
- Division: $a \div b$ or $\frac{a}{b}$
- Plus/minus: $\pm$
- Not equal: $\neq$
- Less/greater: $\leq$, $\geq$
- Approximately: $\approx$
- Infinity: $\infty$
```

**Renders as:**

- Multiplication: $a \times b$ or $a \cdot b$
- Division: $a \div b$ or $\frac{a}{b}$
- Plus/minus: $\pm$
- Not equal: $\neq$
- Less/greater: $\leq$, $\geq$
- Approximately: $\approx$
- Infinity: $\infty$
