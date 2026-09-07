---
description: The seven semantic checks the plan quality gate completes in one non-editing pass before freezing its ledger.
when_to_use: Use during step 2 of the plan quality gate, while auditing a formal plan without editing it.
---

# Audit Checklist

Complete all seven in one pass, without editing. Admit a finding only where it violates a rule or
makes scoped execution unsafe, ambiguous, or unprovable.

1. **Lifecycle.** One [plan stage](../../../conventions/structure/plans.md), the required documents
   for that stage, one technical shape (`tech-docs.md` or the mapped `tech-docs/`), and a truthful
   recorded status.
2. **Route.** Coherent purpose, decision, scope, non-goals, risks, and acceptance, with a
   [junior-readable route](../../../conventions/structure/plans/comprehensive-decision-records.md)
   from BRD and PRD through design to delivery.
3. **Artifacts.** Every file necessary, non-placeholder, and carrying a distinct reader job. No
   document exists only to satisfy a template.
4. **Synchronisation.** Architecture, Gherkin acceptance criteria, file impact, dependencies, and
   the applicable [BDD contract](../../../development/behaviour-driven-development.md) agree with
   one another and with the repository as it currently stands.
5. **Executability.** `[AI]`/`[HUMAN]` ownership on every step, acceptance traceability,
   RED/GREEN/REFACTOR shape on code steps, phase gates, evidence, cleanup, recovery, and rollback.
   A merge step keeps its human gate.
6. **Applicable contracts.** Delivery mode and worktree obligations, migration, UI, API, manual
   behavioural verification, test isolation, live-service, and
   [anti-hallucination](../../../development/quality/plan-anti-hallucination.md) rules that the
   plan's own scope makes applicable — and only those.
7. **Conflicts.** Nothing in the plan contradicts current specifications, governance, the
   implementation, or another active plan.

At the completion checkpoint, additionally confirm that every check the plan itself promised to
deliver now exists and passes, and that Knowledge Capture has run.

## Related Documents

- [Sufficiency and Ownership](./sufficiency-and-ownership.md) — what may not enter the ledger.
- [Deterministic Verification](./deterministic-verification.md) — what tooling proves instead.
