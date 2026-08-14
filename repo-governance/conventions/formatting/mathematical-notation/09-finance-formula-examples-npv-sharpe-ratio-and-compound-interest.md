---
title: "Finance Formula Examples: NPV, Sharpe Ratio, and Compound Interest"
description: Worked LaTeX examples for Net Present Value, Sharpe Ratio, and Compound Interest formulas, source and rendered.
when_to_use: Use when writing an NPV, Sharpe Ratio, or compound interest formula in documentation and want a ready LaTeX template.
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

# Finance Formula Examples: NPV, Sharpe Ratio, and Compound Interest

## NPV Formula

$$
NPV = \sum_{t=0}^{n} \frac{CF_t}{(1 + r)^t}
$$

Or expanded:

$$
NPV = \frac{CF_0}{(1 + r)^0} + \frac{CF_1}{(1 + r)^1} + \frac{CF_2}{(1 + r)^2} + \cdots + \frac{CF_n}{(1 + r)^n}
$$

Where:

- $CF_t$ = cash flow at time $t$
- $r$ = discount rate (typically WACC)
- $n$ = project lifetime in periods
- $t$ = time period ($t = 0$ is present)

### Sharpe Ratio

```markdown
## Sharpe Ratio Formula

Measures risk-adjusted return:

$$
Sharpe = \frac{r_p - r_f}{\sigma_p}
$$

Where:

- $r_p$ = portfolio return
- $r_f$ = risk-free rate
- $\sigma_p$ = standard deviation of portfolio returns
```

**Renders as:**

## Sharpe Ratio Formula

Measures risk-adjusted return:

$$
Sharpe = \frac{r_p - r_f}{\sigma_p}
$$

Where:

- $r_p$ = portfolio return
- $r_f$ = risk-free rate
- $\sigma_p$ = standard deviation of portfolio returns

### Compound Interest

```markdown
## Compound Interest Formula

Future value with compound interest:

$$
FV = PV \times (1 + r)^n
$$

With continuous compounding:

$$
FV = PV \times e^{rt}
$$

Where:

- $FV$ = future value
- $PV$ = present value
- $r$ = interest rate per period
- $n$ = number of periods
- $t$ = time
- $e$ = Euler's number ($\approx 2.71828$)
```

**Renders as:**

## Compound Interest Formula

Future value with compound interest:

$$
FV = PV \times (1 + r)^n
$$

With continuous compounding:

$$
FV = PV \times e^{rt}
$$

Where:

- $FV$ = future value
- $PV$ = present value
- $r$ = interest rate per period
- $n$ = number of periods
- $t$ = time
- $e$ = Euler's number ($\approx 2.71828$)
