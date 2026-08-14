---
title: "Where to Use LaTeX"
description: "Where LaTeX notation belongs: documentation files, README files, and plans, with a worked example for each."
when_to_use: Use when deciding whether a specific file (docs, README, or plan) should use LaTeX for a formula.
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

# Where to Use LaTeX

## Documentation Files in `docs/`

Use LaTeX for all mathematical notation in:

- **Tutorials** (`docs/tutorials/`) - Teaching mathematical concepts
- **How-To Guides** (`docs/how-to/`) - Calculation procedures
- **Reference** (`docs/reference/`) - Formula specifications
- **Explanation** (`docs/explanation/`) - Mathematical reasoning

**Example** (tutorial):

```markdown
## Calculating Net Present Value (NPV)

The NPV formula discounts future cash flows to present value:

$$
NPV = \sum_{t=0}^{n} \frac{CF_t}{(1 + r)^t}
$$

Where:

- $CF_t$ = cash flow at time $t$
- $r$ = discount rate
- $n$ = number of periods
```

## README Files

Use LaTeX in README files throughout the repository:

```markdown
## Performance Metrics

Our algorithm achieves $O(n \log n)$ time complexity and $O(n)$ space complexity.
```

## Plans Documentation

Use LaTeX in planning documents (`plans/`) when describing technical requirements:

```markdown
## Performance Requirements

The system must calculate portfolio returns using:

$$
R_p = \sum_{i=1}^{n} w_i \times R_i
$$

Where $w_i$ are portfolio weights and $R_i$ are asset returns.
```
