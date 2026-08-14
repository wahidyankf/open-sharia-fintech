---
title: "LaTeX Reference"
description: A quick-reference table of essential LaTeX commands, the aligned multi-line environment, text-in-formulas syntax, and common finance symbols.
when_to_use: Use as a lookup table for a specific LaTeX command, symbol, or the aligned multi-line syntax.
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

# LaTeX Reference

## Essential Commands

| Command           | Usage              | Renders           |
| ----------------- | ------------------ | ----------------- |
| `\frac{a}{b}`     | Fraction           | $\frac{a}{b}$     |
| `x^2`             | Superscript        | $x^2$             |
| `x_i`             | Subscript          | $x_i$             |
| `\sqrt{x}`        | Square root        | $\sqrt{x}$        |
| `\sum_{i=1}^{n}`  | Summation          | $\sum_{i=1}^{n}$  |
| `\prod_{i=1}^{n}` | Product            | $\prod_{i=1}^{n}$ |
| `\times`          | Multiplication     | $\times$          |
| `\cdot`           | Dot multiplication | $\cdot$           |
| `\leq`, `\geq`    | Less/greater equal | $\leq$, $\geq$    |
| `\neq`            | Not equal          | $\neq$            |
| `\approx`         | Approximately      | $\approx$         |
| `\pm`             | Plus-minus         | $\pm$             |
| `\infty`          | Infinity           | $\infty$          |
| `\alpha`, `\beta` | Greek letters      | $\alpha$, $\beta$ |

## Alignment (Multi-line)

Use `aligned` environment for multi-line equations (KaTeX compatible):

```markdown
$$
\begin{aligned}
WACC &= \frac{E}{V} \times r_e + \frac{D}{V} \times r_d \times (1 - T_c) \\
     &= \text{Equity weight} \times \text{Cost of equity} \\
     &\quad + \text{Debt weight} \times \text{After-tax cost of debt}
\end{aligned}
$$
```

**Note**: Use `aligned` (not `align`) for KaTeX compatibility. The `aligned` environment does not auto-number equations.

## Text in Formulas

Use `\text{...}` for descriptive text within formulas:

```markdown
$$
\text{Profit} = \text{Revenue} - \text{Costs}
$$
```

## Common Finance Symbols

| Symbol    | LaTeX Command | Usage                     |
| --------- | ------------- | ------------------------- |
| $\alpha$  | `\alpha`      | Alpha, excess return      |
| $\beta$   | `\beta`       | Beta, systematic risk     |
| $\Delta$  | `\Delta`      | Change, difference        |
| $\sigma$  | `\sigma`      | Standard deviation        |
| $\mu$     | `\mu`         | Mean, expected value      |
| $\pi$     | `\pi`         | Profit, pi constant       |
| $\rho$    | `\rho`        | Correlation               |
| $\lambda$ | `\lambda`     | Lambda, adjustment factor |
