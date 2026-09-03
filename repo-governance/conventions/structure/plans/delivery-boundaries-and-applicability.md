---
title: "Delivery Boundaries Declaration and Applicability"
description: Shows the required Delivery Boundaries table format mapping phases to mode-specific delivery opportunities, and states applicability.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when writing a plan's Delivery Boundaries table or checking whether a grandfathered in-progress plan must retrofit gates.
---

# Delivery Boundaries Declaration and Applicability

## Delivery Boundaries

**Required declaration format**: every plan carries a `### Delivery Boundaries` subsection inside its
`## Parallelization Model` section, mapping every phase to its delivery unit:

```markdown
### Delivery Boundaries

| Phase(s) | Natural cohesive seam  | Worktree        | Branch       | Delivery opportunity | Exact resulting `main` / rollback / feature-flag evidence                        |
| -------- | ---------------------- | --------------- | ------------ | -------------------- | -------------------------------------------------------------------------------- |
| 0        | — (setup and baseline) | —               | —            | none                 | No resulting state change; flag not applicable                                   |
| 1-3      | Schema and loader      | `worktrees/foo` | `foo-schema` | PR at Phase 3        | Compatible schema and loader complete; both paths pass; flag not applicable      |
| 4-5      | Navigation UI          | `worktrees/foo` | `foo-nav`    | PR at Phase 5        | Production-disabled `nav-v2`; both paths pass; rollout/rollback/removal recorded |
```

Every change-producing phase must appear in exactly one row. A phase absent from the table is a
defect: its work has no declared route to `main`.

Each row must name one natural cohesive seam, state how its exact resulting `main` state is safe to
deploy to production immediately, and identify its rollback evidence. Keep all build, verification,
operational, rollback, and internal-consistency artifacts with the unit. Incomplete behavior
requires a temporary production-disabled feature flag, enabled and disabled path tests, and
rollout/rollback/removal.
LOC and file counts never create, erase, or force a row.

**Enforcement**: `plan-maker` emits the table and places mode-specific integration steps only in
boundary phases. Under `*-to-pr`, these are PR/push/CI/merge steps; under a direct mode, they are
direct checkpoints. An explicitly requested semantic review is a PR step and belongs at a boundary.
`plan-checker` flags as **HIGH** any such step inside a non-boundary
phase; a change-producing phase absent from the table; or a final
change-producing phase that is not a boundary. It flags as **MEDIUM** a missing
`### Delivery Boundaries` table on a non-trivial plan, and a plan declaring a single end-of-plan
boundary while its `## Parallelization Model` declares independent parallel nodes. `plan-fixer` adds
the table and relocates misplaced integration steps to the boundary phase. `plan-execution-checker`
flags a PR opened for a non-boundary phase under `*-to-pr`, a unit whose PR never merged, or a
direct-mode unit whose checkpoint never reached `origin/main`.
They also reject a count-derived boundary, a unit missing required consistency artifacts, or a
resulting `main` state that is not immediately production-deployable.

## Applicability (Execution Markers + Phase Gates)

Both HARD RULES above — Executor Tagging and Phases as Natural Pauses With Clear Gates — apply to **net-new plans at authoring time**: a plan created after this convention landed MUST comply from creation, and `plan-checker` flags missing markers or gates as HIGH on those plans.

**In-progress plans authored before this convention are grandfathered and retrofitted lazily**: a plan already under `plans/in-progress/` when the convention landed is not retroactively invalid. Each phase gains its `[AI]`/`[HUMAN]` markers and its `### Phase N Gate` + **Pause Safety** note the next time that phase is touched during execution (the executor adds them as it works the phase). Do NOT bulk-fabricate gate checks for unstarted phases of a pre-existing plan — fabricated, ungroundable acceptance checks violate the anti-hallucination rule. `plan-checker` does not raise HIGH findings against grandfathered in-progress plans solely for missing markers/gates; it flags them only on the phases being newly added or edited. New plans get no such grace.
