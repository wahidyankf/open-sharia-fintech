---
title: "Iteration Example"
description: "A full worked trace of a four-iteration run, showing findings counts and consecutive-zero tracking across iterations."
when_to_use: "Use when you need to see how consecutive_zero_count evolves across a realistic multi-iteration run."
---

# Iteration Example

```
Iteration 1:
  Maker: PDF → Markdown (847 pages, 23 tables, 45 figures, 12 Mermaid diagrams)
  Checker: 15 findings
    - CRITICAL: 3 missing sections (pages 234-241)
    - HIGH: 5 invalid Mermaid blocks
    - HIGH: 4 missing figure placeholders
    - MEDIUM: 3 heading hierarchy drifts
  Fixer: Applied 12 HIGH_CONFIDENCE fixes; skipped 3 MEDIUM_CONFIDENCE

Iteration 2:
  Re-validate (scoped to changed sections): 2 findings
    - HIGH: 1 Mermaid block still invalid after first fix attempt
    - MEDIUM: 1 heading drift in re-inserted section
  Fixer: Applied 1 fix; 1 MEDIUM skipped
  consecutive_zero_count: 0 (findings > 0 — reset)

Iteration 3:
  Re-validate (scoped): 0 findings
  consecutive_zero_count: 1 (first zero)

Iteration 4 (confirmation):
  Re-validate (scoped): 0 findings
  consecutive_zero_count: 2 ← double-zero confirmed

Result: PASS (4 iterations)
```
