---
title: "Iteration Example"
description: A worked four-iteration trace from cold preflight through double-zero AI-only confirmation.
when_to_use: Use when you want a concrete trace of how the preflight cache and check-fix cycles play out together.
---

# Iteration Example

Typical execution flow:

```
Step 0.5: Preflight (cold) → 4 governance categories scanned (layer-coherence, traceability-audit, vendor-audit, governance-word-budget); any deterministic findings emitted to generated-reports/ (visibility only)

Iteration 1:
  Step 0.5: Preflight (cached, RHINO_AUDIT_NOW=...) → same deterministic findings (SHA-256 hash match, skip re-eval)
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

Result: PASS (double-zero AI-only; any deterministic findings fixed at source or documented in skip-list)
```
