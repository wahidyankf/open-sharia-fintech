---
title: "Termination Criteria"
description: Pass/partial/fail conditions by mode level, and how deterministic preflight findings relate to the two-consecutive-zero requirement.
when_to_use: Use when checking whether a completed run's status is correctly determined.
---

# Termination Criteria

**Success** (`pass`):

- **lax**: Zero CRITICAL findings on 2 consecutive checks (HIGH/MEDIUM/LOW may exist)
- **normal**: Zero CRITICAL/HIGH findings on 2 consecutive checks (MEDIUM/LOW may exist)
- **strict**: Zero CRITICAL/HIGH/MEDIUM findings on 2 consecutive checks (LOW may exist)
- **ocd**: Zero findings at all levels on 2 consecutive checks

**Partial** (`partial`):

- Threshold-level findings remain after max-iterations safety limit

**Failure** (`fail`):

- Technical errors during check or fix

**Note on deterministic findings**: Deterministic findings from preflight are reported in the audit's `## Deterministic Findings (rhino-cli preflight)` section but do NOT count toward any mode threshold per Step 2's visibility-only rule. Two consecutive zero-finding validations refers to AI-only findings only.

**Note**: Below-threshold findings are reported in final audit but don't prevent success status. Success requires two consecutive zero-finding validations (consecutive pass requirement).
