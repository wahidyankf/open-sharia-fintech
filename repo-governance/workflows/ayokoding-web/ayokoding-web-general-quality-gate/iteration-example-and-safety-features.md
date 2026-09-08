---
description: Walks through a typical two-iteration execution flow, then documents loop-prevention, convergence, false-positive, and error-recovery safety mechanisms.
when_to_use: Use as a worked reference for a typical run, or when you need to understand how the workflow protects against runaway iteration.
---

# Iteration Example and Safety Features

## Iteration Example

Typical execution flow:

```
Iteration 1:
  Parallel Check (3 validators) → 20 total findings
    - Content: 10 findings
    - Facts: 8 findings
    - Links: 2 findings
  Sequential Fix → Content → Facts
  Re-check → 5 findings remain

Iteration 2:
  Parallel Check → 5 findings
  Sequential Fix → Content → Facts
  Re-check → 0 findings

Finalization:
  Final Validation → Zero issues

Result: SUCCESS (2 iterations)
```

## Safety Features

**Infinite Loop Prevention**:

- max-iterations defaults to 7 (override with higher value for more attempts)
- When provided, workflow terminates with `partial` if limit reached
- Tracks iteration count and finding trends
- Use max-iterations when fix convergence is uncertain

**Convergence Safeguards**:

- Checker loads `.known-false-positives.md` skip list at start of each iteration
- Fixer persists new FALSE_POSITIVEs to skip list after each run
- Re-validation uses scoped scan (changed files only) to prevent scope expansion
- Factual claims verified in iteration 1 are cached, not re-verified with WebSearch
- Escalation after repeated checker-fixer disagreements on the same finding

**False Positive Protection**:

- All fixers re-validate findings before applying
- Skips FALSE_POSITIVE findings automatically
- Progressive writing ensures audit history survives

**Error Recovery**:

- Continues to next fixer even if one fails
- Continues to finalization even if fixes partially fail
- Reports which fixes succeeded/failed
- Generates final reports regardless of status

**Comprehensive Coverage**:

- Three validation dimensions (content, facts, links)
- Parallel validation for efficiency
- Sequential fixing for dependency management
- Post-fix regeneration for consistency
