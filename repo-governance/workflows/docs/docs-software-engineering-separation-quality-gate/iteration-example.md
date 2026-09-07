---
description: "A worked three-iteration trace showing findings dropping from 8 to 3 to 0, with the double-zero confirmation."
when_to_use: "Use when you need to see how consecutive_zero_count evolves across a realistic multi-iteration run."
---

# Iteration Example

Typical execution flow:

```
Iteration 1:
  Check → 8 findings (missing prerequisites, duplicated content) → Fix → Re-check → 3 findings

Iteration 2:
  Check (reuse) → 3 findings (style guide lacks OSE Platform context) → Fix → Re-check → 0 findings (consecutive_zero: 1)

Iteration 3 (confirmation):
  Re-check → 0 findings (consecutive_zero: 2 — double-zero confirmed)

Result: SUCCESS (3 iterations)
```
