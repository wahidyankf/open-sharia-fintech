---
title: "Termination Criteria"
description: Defines the success, partial, and failure termination conditions for the Primer quality gate across all four strictness modes.
when_to_use: Use when determining whether a quality-gate run has reached a terminal excellent, needs-improvement, or failing state.
---

# Termination Criteria

**Success** (`excellent`):

- **lax**: Zero CRITICAL findings on 2 consecutive checks, 75-85 examples (HIGH/MEDIUM/LOW may
  exist)
- **normal**: Zero CRITICAL/HIGH findings on 2 consecutive checks, 75-85 examples (MEDIUM/LOW may
  exist)
- **strict**: Zero CRITICAL/HIGH/MEDIUM findings on 2 consecutive checks, 75-85 examples (LOW may
  exist)
- **ocd**: Zero findings at all levels on 2 consecutive checks, 75-85 examples

**Partial** (`needs-improvement`):

- Threshold-level findings remain after max-iterations OR example count below 75

**Failure** (`failing`):

- Major structural issues require maker rework, auto-fixing not applicable

**Note**: Below-threshold findings are reported in final audit but don't prevent success status.
