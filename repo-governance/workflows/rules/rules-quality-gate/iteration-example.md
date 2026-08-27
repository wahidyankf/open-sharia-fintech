---
title: "Iteration Example"
description: A worked trace combining retained domain checks with separate lifecycle evidence.
when_to_use: Use when you want a concrete trace of how the preflight cache and check-fix cycles play out together.
---

# Iteration Example

Typical execution flow:

```
Step 0: Vendor and word-budget predicates delegated → lifecycle evidence recorded
Step 0.5: Layer-coherence and traceability retained → domain findings recorded

Iteration 1:
  Step 0.5: Retained preflight → domain findings included in threshold count
  Step 1: AI checks → 5 AI-only findings
  Steps 2-5: Fixer addresses 3 findings

Iteration 2:
  Step 0.5: Preflight (cached) → same deterministic findings
  Step 1: AI checks → 2 AI-only findings remaining
  Steps 2-5: Fixer addresses 2 findings

Iteration 3:
  Step 0.5: Preflight (cached) → same deterministic findings
  Step 1: AI checks → 0 AI-only findings (consecutive_zero=1)

Iteration 4:
  Step 0.5: Preflight (cached) → same deterministic findings
  Step 1: AI checks → 0 AI-only findings (consecutive_zero=2)

Result: final-status PASS after double-zero domain checks; lifecycle-status reported separately
```
