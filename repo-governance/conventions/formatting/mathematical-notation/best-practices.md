---
description: "Best practices for LaTeX notation: defining variables, consistent notation, formatting complex formulas, semantic tables, and balancing precision with clarity."
when_to_use: Use when writing a non-trivial formula and want guidance on notation style, variable definitions, or formula complexity.
---

# Best Practices

## Define Variables

Always define variables after displaying a formula:

```markdown
$$
r_e = r_f + \beta \times (r_m - r_f)
$$

Where:

- $r_e$ = cost of equity
- $r_f$ = risk-free rate
- $\beta$ = beta coefficient
```

**Why**: Readers may not know standard notation. Explicit definitions ensure clarity.

## Use Consistent Notation

Choose notation conventions and stick to them:

- **Time periods**: Use $t$ consistently (not mixing $t$, $n$, $i$)
- **Returns**: Use $r$ for rates, $R$ for returns
- **Weights**: Use $w$ for portfolio weights
- **Volatility**: Use $\sigma$ for standard deviation

**Why**: Consistency reduces cognitive load and prevents confusion.

## Format Complex Formulas

Break multi-line formulas for readability:

```markdown
$$
\begin{aligned}
NPV &= \sum_{t=0}^{n} \frac{CF_t}{(1 + r)^t} \\
    &= -I_0 + \frac{CF_1}{1+r} + \frac{CF_2}{(1+r)^2} + \cdots + \frac{CF_n}{(1+r)^n}
\end{aligned}
$$
```

**Why**: Multi-line alignment improves readability for complex derivations.

## Use Semantic HTML When Needed

For very complex layouts, consider tables alongside LaTeX:

```markdown
| Variable | Symbol | Unit    |
| -------- | ------ | ------- |
| Equity   | $E$    | USD     |
| Debt     | $D$    | USD     |
| WACC     | $WACC$ | Percent |
```

## Balance Precision and Clarity

Don't over-complicate notation:

```markdown
PASS: Good:
$$r_e = r_f + \beta \times MRP$$

FAIL: Too complex:
$$r_{e,adjusted,t} = r_{f,t} + \beta_{asset,market,t} \times (r_{m,expected,t} - r_{f,t})$$
```

**Why**: Simpler notation is easier to understand. Add subscripts only when necessary to distinguish different variables.
