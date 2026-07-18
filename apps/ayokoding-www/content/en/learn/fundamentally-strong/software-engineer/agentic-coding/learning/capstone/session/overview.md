---
title: "Capstone: The Session"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 10
---

_Capstone step 2 of 3 -- exercises co-04 (context management), co-12 (small reversible steps),
co-13/co-14 (verification discipline, test-driven agent workflows), co-15/co-16 (diff review,
hallucination awareness)._

## Context loaded for this session

Only two files were in scope for the whole session: the prompt (`prompt.md`, already reviewed) and
the tripwire test (`test_parse_duration.py`, already reviewed and confirmed red). No other file in
the repository was loaded -- there was nothing else this feature's logic depended on (co-04: the
smallest context that can do the job, not the largest available).

## The three small, independently revertible steps

1. **[Step 1: first attempt, rejected](./step-1-first-attempt-rejected.md)** -- the agent's first
   generation is plausible, confident, and silently wrong. Caught by the tripwire test, not by
   reading the code.
2. **[Step 2: fix, green](./step-2-fix-and-green.md)** -- the one-line fix, reviewed, all seven
   acceptance-criteria tests pass.
3. **[Step 3: refactor, reviewed](./step-3-refactor-reviewed.md)** -- a small, behavior-preserving
   refactor (extract one helper function), reviewed again, tests still green.

Each step above is its own independently revertible commit-sized change (co-12): reverting step 3
alone leaves a working, green step-2 state; reverting steps 2 and 3 leaves the red step-1 state,
never a half-applied mix.

**Verify**: every diff below was run against the real test suite before being accepted (co-13), and
step 1's bad generation was caught and rejected with a specific, written reason (co-15, co-16) before
any later step built on top of it.

---

← Previous: [Prompt](../prompt.md) &middot; Next: [Trust/Verify Log](../trust-verify-log.md) →
