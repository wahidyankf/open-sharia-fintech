---
description: "Child documents of the rules-quality-gate governance gate"
when_to_use: "Read this index to find the right rules-quality-gate child document."
---

# Rules Quality Gate

- [Authorization and Sanctioned Callers](./authorization-and-callers.md) — Who may start this gate, why rules-grooming is its one sanctioned workflow caller, why propagation is not, and how a grooming invocation's audit scope is bounded. Use when deciding whether a trigger may start the gate.
- [Sufficiency and Ownership](./sufficiency-and-ownership.md) — What a passing rule asserts and does not assert, how `PROPOSAL` and `EFFECTIVE` differ on a not-yet-built deterministic check, and the machine-decidable checks this gate must never reproduce. Use when deciding whether a rule gap is admissible to the ledger.
- [Semantic Audit](./semantic-audit.md) — The nine decisions the gate makes about an affected rule: concreteness, normative strength, explicit scope, correct governance level, single canonical source, truthful enforcement, compaction survival, actionability, and move-or-deletion integrity. Use at step 2 of the procedure.
- [Execution and Delegation](./execution-and-delegation.md) — How the read-only `rules-checker` sweep is delegated for context isolation, why `rules-fixer` was retired in favour of propagation as sole writer, and where repository-wide consistency sweeps now live. Use when starting a run and deciding what the subagent does.
