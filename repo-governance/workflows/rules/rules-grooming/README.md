---
title: "rules-grooming Workflow"
description: "Sweeps the repo-rules corpus for volume that carries no obligation — fragmentation overhead, cross-surface duplication, dead rules — and hands every reduction to rules-propagation."
when_to_use: "Read this index to find the right rules-grooming Workflow child document."
---

# rules-grooming Workflow

- [Purpose and When to Use](./purpose-and-when-to-use.md) — What this workflow reduces in the rule corpus, the gap it fills between propagation and the quality gate, and the three falsifiable recurrence-trigger conditions. Use when deciding whether the corpus is due a sweep.
- [Scope Boundary and the Non-Writing Invariant](./scope-boundary-and-non-writing-invariant.md) — The three admitted candidate classes and their semantic risk, the reductions permanently refused, and why every edit goes to rules-propagation. Use when checking whether a proposed reduction is in scope.
- [Steps 0-2 — Authorization, Census, and Inventory](./steps-0-2-authorization-census-and-inventory.md) — Freezing the run's inputs, measuring the corpus against the recurrence trigger, and capturing the pre-run obligation snapshot. Use when starting a sweep and establishing its preservation baseline.
- [Steps 3-4 — Candidate Discovery and Ranking](./steps-3-4-candidate-discovery-and-ranking.md) — The three class-scoped discovery sweeps with their admission rules, and the yield-over-risk ordering that groups candidates by subject. Use when running discovery or ordering its results.
- [Steps 5-6 — Checkpoint and Hand-Off](./steps-5-6-checkpoint-and-handoff.md) — The per-class approval gate, why retirements are approved one at a time, and the subject-batched hand-off to propagation. Use when approving a manifest or handing items off.
- [Steps 7-8 — Preservation Verification and Recurrence](./steps-7-8-preservation-verification-and-recurrence.md) — The post-run obligation diff that proves nothing was lost, the revert path when it fails, and the log entry that arms the next trigger. Use when verifying or recording a completed sweep.
- [Success Criteria](./success-criteria.md) — Gherkin scenarios covering the run lifecycle: no-op, the first-run bootstrap, obligation loss, dry-run behaviour, and the non-writing invariant. Use when validating or extending this workflow.
- [Success Criteria — Candidate Classes](./success-criteria-candidate-classes.md) — Gherkin scenarios for what each candidate class admits, what it refuses, and the reductions no class may ever produce. Use when validating or extending an admission rule.
- [Termination Criteria](./termination-criteria.md) — The four terminal states — no-op, groomed, halted, partial — and what produces each. Use when deciding whether a run is finished and what to report.
- [Related Workflows and Documentation](./related-workflows-and-documentation.md) — What this workflow composes, what it deliberately never calls, and the conventions its reductions are measured against. Use when navigating to a composed workflow or governing convention.
