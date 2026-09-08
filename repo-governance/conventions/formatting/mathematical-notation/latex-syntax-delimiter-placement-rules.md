---
description: "The critical delimiter placement rules: single `$` must stay inline, display equations and all `aligned` blocks must use `$$`, and why KaTeX requires `aligned` not `align`."
when_to_use: Use when a multi-line or display LaTeX equation is not rendering and you need to check delimiter placement.
---

# LaTeX Syntax: Delimiter Placement Rules

**Single `$` delimiters MUST be inline (on the same line as text):**

```markdown
PASS: Correct - Inline math:
The cost of equity $r_e$ is calculated using CAPM.

FAIL: Incorrect - Single $ on its own line:
$
r_e = r_f + \beta \times (r_m - r_f)
$
```

**Display-level equations MUST use `$$` delimiters:**

```markdown
PASS: Correct - Display math:

$$
r_e = r_f + \beta \times (r_m - r_f)
$$

FAIL: Incorrect - Single $ for display:
$
r_e = r_f + \beta \times (r_m - r_f)
$
```

**All `\begin{aligned}` blocks MUST use `$$` delimiters:**

```markdown
PASS: Correct - aligned with $$:

$$
\begin{aligned}
WACC &= \frac{E}{V} \times r_e + \frac{D}{V} \times r_d \times (1 - T_c) \\
     &= 0.645 \times 11.4\% + 0.355 \times 3.41\% \\
     &= 8.56\%
\end{aligned}
$$

FAIL: Incorrect - using align instead of aligned (KaTeX incompatible):

$$
\begin{align}
WACC &= \frac{E}{V} \times r_e + \frac{D}{V} \times r_d \times (1 - T_c)
\end{align}
$$

FAIL: Incorrect - aligned with single $:
$
\begin{aligned}
WACC &= \frac{E}{V} \times r_e + \frac{D}{V} \times r_d \times (1 - T_c)
\end{aligned}
$
```

**Why this matters:**

1. **KaTeX Compatibility**: This project uses KaTeX for math rendering. KaTeX does NOT support the `align` environment - it only supports `aligned`. Always use `\begin{aligned}...\end{aligned}` for multi-line equations.

2. **Delimiter Requirement**: Single `$` on its own line breaks rendering on GitHub - the LaTeX code displays as raw text instead of rendered math.

**Rule of thumb:**

- **Inline math** (within text): `$x + y$` on same line as text
- **Display math** (standalone): `$$...$$` on separate lines
- **Multi-line equations**: Always use `$$` with `\begin{aligned}` (NOT `\begin{align}`)
