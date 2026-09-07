---
description: What a passing repository rule asserts, and the machine-decidable checks the rules quality gate must never reproduce.
when_to_use: Use when deciding whether a rule gap is admissible to the ledger, or whether a check belongs to deterministic tooling.
---

# Sufficiency and Ownership

A passing rule is good enough for its stated need, scope, and known risk — not perfect, exhaustive,
or future-proof. Never raise a finding for wording preference, a speculative case, optional
explanation, or automation without demonstrated need. Apply the
[Minimal Sufficiency Test](../../../principles/general/simplicity-over-complexity/minimal-sufficiency-test.md).

This gate owns semantic rule quality only. Deterministic tooling owns every machine-decidable
check; never reproduce, sample, or second-guess it. The word ceiling is the standing example: leave
`governance-word-budget` skipped locally, record it under the run's `delegated-gate-ids`, and let a
budget verdict come only from the gate that measures. For a deterministic check proposed but not yet
built, `PROPOSAL` verifies only that its ownership, executable delivery, and proof obligation are
explicit. `EFFECTIVE` requires the canonical target to exist and pass. Never simulate a future tool.
