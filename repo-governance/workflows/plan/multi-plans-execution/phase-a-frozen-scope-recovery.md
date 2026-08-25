---
title: "Phase A — Frozen Scope Recovery"
description: "Persists a multi-plan run's enumerated scope and promotion states so resume cannot silently redefine the run."
when_to_use: "Use after resolving multi-plan scope and before promoting any backlog member, or when resuming that run."
---

# Phase A — Frozen Scope Recovery

Before the first promotion mutation, create one durable, caller-visible run record in the
repository issue tracker. Local task lists, reports, conversation state, and lifecycle-folder
enumeration are insufficient because they can disappear or change during promotion.

The record has a stable run identifier and stores:

- the original explicit list or selector and exclusions;
- the complete enumerated plan-identifier set in caller-confirmed order;
- the `origin/main` commit used for enumeration;
- each member's observed lifecycle path and promotion state; and
- links to its promotion branch and pull request when they exist.

Write the full set with every member initially classified before promoting the first member. After
each remote transition, apply the canonical
[Promotion Recovery](../../../conventions/structure/plans/starting-work-promotion-recovery.md)
classifier, then update that member's state in the same record. Do not infer completion from a
missing backlog path.

On resume, the caller supplies or confirms the run identifier. Reload the stored set and states,
reconcile them against `origin`, and continue incomplete promotions. Never re-expand
`all-backlog`, `all-in-progress`, or `all` for that run: newly added plans are outside its frozen
scope, and already-promoted members remain inside it. A missing, malformed, duplicated, or
conflicting record stops the run for explicit reconciliation before scheduling or mutation.

The issue is execution state, not a plan-document delivery unit. Keep secrets out of it, retain it
as the durable recovery and audit record, and link it from every promotion pull request created by
the run.
