---
description: What a plan-quality-gate PASS asserts, and the machine-decidable checks the gate must never reproduce.
when_to_use: Use when deciding whether a plan gap is admissible to the ledger, or whether a check belongs to deterministic tooling.
---

# Sufficiency and Ownership

`PASS` means good enough for the authorized scope, known risks, and applicable rules — not perfect,
exhaustive, or future-proof. Do not block on stylistic preference, speculative hardening, optional
detail, or an improvement that can wait without making execution unsafe or ambiguous. Apply the
[Minimal Sufficiency Test](../../../principles/general/simplicity-over-complexity/minimal-sufficiency-test.md).

This gate evaluates meaning, consistency, safety, executability, and proof. Deterministic tooling
owns every machine-decidable check — links, README indexes, word budgets, Mermaid, harness parity,
naming, frontmatter. Never manually reproduce, sample, or second-guess them. For a check the plan
itself delivers, verify only that `delivery.md` carries an executable implementation and proof
task; never simulate a future tool. At the completion checkpoint that target must exist and pass.
