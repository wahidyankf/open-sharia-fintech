---
title: "Iteration Example and Safety Features"
description: Shows a typical four-iteration execution flow, then lists the infinite-loop, convergence, and false-positive safety features.
when_to_use: Use when explaining how the check-fix loop converges, or when auditing what safeguards prevent runaway or thrashing iterations.
---

# Iteration Example and Safety Features

## Iteration Example

Typical execution flow:

```
Iteration 1:
  Check (full scan + comprehensive codebase inspection) → 12 findings → Fix → captures changed files

Iteration 2:
  Check (scoped to changed files, cached verification) → 3 findings → Fix → captures changed files

Iteration 3:
  Check (scoped) → 0 findings (consecutive_zero: 1)

Iteration 4 (confirmation):
  Re-check (scoped) → 0 findings (consecutive_zero: 2 — double-zero confirmed)

Result: SUCCESS (4 iterations)
```

## Safety Features

**Infinite Loop Prevention**:

- max-iterations defaults to 7 (override with higher value for more attempts)
- When provided, workflow terminates with `partial` if limit reached
- Tracks iteration count for monitoring
- Escalation warning at iteration 5 if not converging

**Convergence Safeguards**:

- Checker loads `.known-false-positives.md` skip list at start of each iteration
- Fixer persists new FALSE_POSITIVEs to skip list after each run
- Re-validation uses scoped scan (changed files only) to prevent scope expansion
- Comprehensive codebase inspection on iteration 1 with locked scope on iterations 2+
- Factual claims verified in iteration 1 are cached, not re-verified with WebSearch
- Escalation after repeated checker-fixer disagreements on the same finding

**False Positive Protection**:

- Fixer re-validates each finding before applying
- Skips FALSE_POSITIVE findings automatically
- Progressive writing ensures audit history survives

**Error Recovery**:

- Continues to verification even if some fixes fail
- Reports which fixes succeeded/failed
- Generates final report regardless of status
