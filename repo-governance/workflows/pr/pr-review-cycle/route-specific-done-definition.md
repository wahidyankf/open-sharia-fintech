---
description: "Defines completion of an explicitly requested iterative review cycle."
when_to_use: "Use when deciding whether pr-review-cycle returns done or blocked."
---

# Cycle-Local Done Definition

Return `done` only when all of these cycle-local conditions hold:

1. Two adjacent authenticated `ose-pr-review-pass:v1` records are clean on the same live head.
2. The two credits use different probe classes and pass the durable positive-credit read-back.
3. Exact-head/base aggregate PR CI is green for each credited pass.
4. No unresolved MEDIUM, HIGH, or CRITICAL finding remains in this cycle's authenticated history.
5. Every fixer disposition is authenticated and every claimed fix is pushed in the PR diff.

Return `blocked` on unrecoverable record conflict or when the configured ceiling arrives without
all five conditions. This result says only whether the optional cycle met its own exit. It does not
declare the PR mergeable, and absence of a cycle result is valid for ordinary delivery.
