---
name: rules-grooming
title: "rules-grooming"
description: "Sweeps the repo-rules corpus for volume that carries no obligation — fragmentation overhead, cross-surface duplication, dead rules — and hands every reduction to rules-propagation."
when_to_use: "Use when the rule corpus is due a recurring volume sweep, never as remediation for one file failing its word budget."
goal: >
  Reduce the size of the repository's rule corpus without reducing its normative content, by
  identifying representation that carries no obligation and routing each reduction through the sole
  writer of rule edits
termination: >
  Every manifest item is landed, rejected, or deferred with a recorded reason, the post-run
  obligation inventory differs from the pre-run inventory only by the approved retirements, and the
  run and its metrics delta are recorded; halts on any unapproved obligation loss
inputs:
  - name: scope
    type: string
    description: >
      Path prefixes to sweep, comma-separated. Defaults to the full repo-rules corpus as the
      Membership Test defines it. Narrowing is permitted; the census still reports corpus-wide
      metrics so a partial sweep cannot misreport overall progress.
    required: false
    default: "repo-rules corpus"
  - name: classes
    type: enum
    values: [fragmentation, duplication, retirement]
    description: >
      Which candidate classes this run considers. Multi-valued. Omitting a class suppresses its
      discovery sweep entirely rather than discovering and skipping it.
    required: false
    default: "fragmentation,duplication"
  - name: max-concurrency
    type: number
    description: "Background agents run concurrently — the N in the N+1 model. Never self-promoted beyond the declared value."
    required: false
    default: 3
  - name: dry-run
    type: boolean
    description: "Emit the census, manifest, and obligation inventory; hand nothing to propagation."
    required: false
    default: false
outputs:
  - name: grooming-manifest
    type: file
    pattern: local-tmp/rules-grooming/rules-grooming__*__manifest.md
    description: "Ranked candidates with class, measured yield, semantic risk, and per-item disposition"
  - name: obligation-inventory
    type: file-list
    pattern: local-tmp/rules-grooming/rules-grooming__*__obligations-{pre,post}.md
    description: "The distinct-obligation snapshots whose diff is the run's preservation proof"
  - name: final-status
    type: enum
    values: [no-op, groomed, halted, partial]
---

# Repository Rules Grooming Workflow

The rule corpus grows by accretion. Word budgets push content into ever-smaller shards, each
carrying frontmatter, a parent `Contents` line, a README index entry, and cross-links; the same
obligation gets restated on a second surface; a rule outlives its subject. None of that is
obligation — it is **representation**, and it is what this workflow removes.

**Reduction target.** Volume that carries no obligation. Three candidate classes only:
fragmentation overhead, cross-surface duplication, and dead rules. Nothing else is admitted.

**Non-writing invariant.** [rules-propagation](./rules-propagation.md) is the sole writer of every
rule edit. This workflow discovers, measures, ranks, and hands off; it never edits a rule surface.
That keeps the pair acyclic and leaves conflict scanning, placement, and enforcement disposition
with the workflow that already owns them.

**This is not prose compression.** Rewriting wording to save words is
[forbidden anti-fix 2](../../conventions/structure/governance-word-budget-remediation.md) and
violates propagation's semantic-preservation hard gate. Grooming never paraphrases a rule, never
generalizes a qualifier, and never trims a safety guardrail. A file over its word budget is
remediated by progressive disclosure, not by scheduling a grooming run.

Agents composed: `rules-checker` for discovery. There is no grooming writer.

## Contents

- [Purpose and When to Use](./rules-grooming/purpose-and-when-to-use.md) — what it reduces; the recurrence trigger.
- [Scope Boundary and the Non-Writing Invariant](./rules-grooming/scope-boundary-and-non-writing-invariant.md) — the three classes; why it never writes.
- [Steps 0-2](./rules-grooming/steps-0-2-authorization-census-and-inventory.md) — authorization, corpus census, obligation inventory.
- [Steps 3-4](./rules-grooming/steps-3-4-candidate-discovery-and-ranking.md) — the three discovery sweeps; yield over risk.
- [Steps 5-6](./rules-grooming/steps-5-6-checkpoint-and-handoff.md) — human checkpoint; propagation hand-off.
- [Steps 7-8](./rules-grooming/steps-7-8-preservation-verification-and-recurrence.md) — the preservation diff; the re-run condition.
- [Success Criteria](./rules-grooming/success-criteria.md) — Gherkin, run lifecycle.
- [Success Criteria — Candidate Classes](./rules-grooming/success-criteria-candidate-classes.md) — Gherkin, per class.
- [Termination Criteria](./rules-grooming/termination-criteria.md) — no-op, groomed, halted, partial.
- [Related Workflows and Documentation](./rules-grooming/related-workflows-and-documentation.md) — what runs before and after it.
