---
description: The nine decisions the rules quality gate makes about an affected rule, without editing it.
when_to_use: Use at step 2 of the rules quality gate, while auditing a proposed or effective rule state.
---

# Semantic Audit

Inspect only the affected rule, its points of use, relevant higher authority, and directly
overlapping guidance. Decide whether:

1. the need, intended outcome, and rationale are concrete enough to evaluate;
2. `must`, `should`, or `may` expresses the intended normative strength;
3. scope, trigger, action or prohibition, boundaries, and necessary exceptions are explicit;
4. the [canonical governance level](../../../repository-governance-architecture.md) is correct and
   no lower rule conflicts with higher authority;
5. one canonical source owns the meaning while concise point-of-use links keep it discoverable
   without duplication;
6. each enforcement claim names a truthful class and route, carrying required evidence wherever
   automation cannot decide the outcome;
7. the instruction survives compaction and handoff at every applicable entry point;
8. a reasonable reader can act without inventing policy, while the rule stays minimally
   sufficient; and
9. a move or deletion preserves unique intent and updates every affected consumer.

A finding is admissible only where one of these fails in a way that makes the requested outcome
unsafe, contradictory, undiscoverable, or materially ambiguous. Wording preference, speculative
cases, optional explanation, and unrequested automation are never findings.

Never audit unrelated governance, and never rerun a check owned by deterministic tooling.

## Related Documents

- [Rules Quality Gate](../rules-quality-gate.md) — the procedure this serves.
- [Rules Propagation](../rules-propagation.md) — the sole writer that resolves these findings.
