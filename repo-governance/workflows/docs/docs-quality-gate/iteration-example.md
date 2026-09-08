---
description: "A worked trace showing a partial result from unfixable broken links, followed by success after manual link fixes."
when_to_use: "Use when you need to see a realistic multi-iteration run, including the broken-links partial-result case."
---

# Iteration Example

Typical execution flow:

```
Iteration 1:
  Parallel Check (3 validators) → 18 total findings
    - Factual: 8 CRITICAL/HIGH findings
    - Tutorial: 6 CRITICAL/HIGH findings
    - Links: 4 broken links
  Sequential Fix → Factual → Tutorial
  Re-check → 4 findings remain (links unfixable)

Iteration 2:
  Parallel Check → 4 findings (all link-related)
  Sequential Fix → Factual (0 new) → Tutorial (0 new)
  Re-check → 4 findings remain

Result: PARTIAL (broken links require manual intervention)

After manual link fixes:

Iteration 3:
  Parallel Check → 0 findings

Result: SUCCESS (3 iterations)
```
