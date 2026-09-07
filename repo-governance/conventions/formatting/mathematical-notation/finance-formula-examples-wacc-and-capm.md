---
description: Worked LaTeX examples for the Weighted Average Cost of Capital and Capital Asset Pricing Model formulas, source and rendered.
when_to_use: Use when writing a WACC or CAPM formula in documentation and want a ready LaTeX template with variable definitions.
---

# Finance Formula Examples: WACC and CAPM

## Finance Formula Examples

### Weighted Average Cost of Capital (WACC)

```markdown
## WACC Formula

$$
WACC = \frac{E}{V} \times r_e + \frac{D}{V} \times r_d \times (1 - T_c)
$$

Where:

- $E$ = market value of equity
- $D$ = market value of debt
- $V$ = total market value of capital ($V = E + D$)
- $r_e$ = cost of equity
- $r_d$ = cost of debt
- $T_c$ = corporate tax rate
```

**Renders as:**

## WACC Formula

$$
WACC = \frac{E}{V} \times r_e + \frac{D}{V} \times r_d \times (1 - T_c)
$$

Where:

- $E$ = market value of equity
- $D$ = market value of debt
- $V$ = total market value of capital ($V = E + D$)
- $r_e$ = cost of equity
- $r_d$ = cost of debt
- $T_c$ = corporate tax rate

### Capital Asset Pricing Model (CAPM)

```markdown
## CAPM Formula

The cost of equity is calculated using CAPM:

$$
r_e = r_f + \beta \times (r_m - r_f)
$$

Where:

- $r_e$ = expected return on equity (cost of equity)
- $r_f$ = risk-free rate
- $\beta$ = beta coefficient (systematic risk)
- $r_m$ = expected market return
- $(r_m - r_f)$ = market risk premium
```

**Renders as:**

## CAPM Formula

The cost of equity is calculated using CAPM:

$$
r_e = r_f + \beta \times (r_m - r_f)
$$

Where:

- $r_e$ = expected return on equity (cost of equity)
- $r_f$ = risk-free rate
- $\beta$ = beta coefficient (systematic risk)
- $r_m$ = expected market return
- $(r_m - r_f)$ = market risk premium

### Net Present Value (NPV)

```markdown
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
```

**Renders as:**
