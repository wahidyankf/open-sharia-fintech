---
title: "Termination Criteria"
description: Pass/partial/fail conditions by mode level, including retained domain findings and separate lifecycle status.
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

**Retained deterministic findings**: layer-coherence and traceability findings count toward the
mode threshold. Vendor, word-budget, and other exact delegated lifecycle predicates are absent
from this domain count and use `lifecycle-status` instead.

**Note**: Below-threshold findings are reported in final audit but don't prevent success status. Success requires two consecutive zero-finding validations (consecutive pass requirement).
