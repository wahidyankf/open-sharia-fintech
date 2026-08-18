---
title: "Phases as Natural Pauses With Clear Gates (HARD RULE)"
description: Requires every delivery phase to end in a coherent state with a Phase N Gate and a Pause Safety note.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when writing a delivery.md phase's closing gate and Pause Safety note.
---

# Phases as Natural Pauses With Clear Gates (HARD RULE)

Every phase in a delivery checklist MUST be designed as a **natural pause point** that ends with a **clear gate**. A reader — human or AI — must be able to stop after any phase and find the repository in a coherent, non-broken state.

**Natural pause point**: at every phase boundary the working tree is internally consistent — code compiles, tests pass, nothing is half-applied, no build is knowingly broken. No phase ends mid-refactor or carries a known-red state into the next phase.

**Clear gate**: every phase ends with a `### Phase N Gate` subsection — a must-pass verification checklist whose items state the exact commands and the observable acceptance criterion. Phase N+1 MUST NOT begin while any check in phase N's gate is failing. Gate items carry executor tags like any other checkbox (usually `[AI]` verification commands; a gate MAY be a `[HUMAN]` approval, which makes the boundary a hand-off point — see [Executor Tagging](./executor-tagging-tags-and-bias.md#executor-tagging--ai-vs-human-hard-rule) above).

**Pause Safety note**: immediately after each `### Phase N Gate`, add a short **Pause Safety** blockquote stating (a) the safe-to-stop state reached after the phase and (b) the single command to resume or re-verify. This makes the natural-pause property explicit and auditable.

**Template**:

```markdown
## Phase N: <name>

- [ ] [AI] <work item> — acceptance: <observable outcome>
- [ ] [AI] <work item> — acceptance: <observable outcome>

### Phase N Gate

> All checks below must pass before starting Phase N+1. If any check fails, fix it in Phase N
> before proceeding.

- [ ] [AI] `<verification command>` — <acceptance>
- [ ] [AI] `<verification command>` — <acceptance>

> **Pause Safety**: <what coherent state exists after this phase; what has and has not changed>.
> Safe to stop. To resume: `<single command to re-verify>`.
```

Order phases so each builds on a green predecessor. Phase 0 (Environment Setup and Baseline) already follows this shape — its gate is the recorded clean baseline, and that gate is the whole of it: Phase 0 opens no PR, per [Phase 0 Opens No PR](./phase-0-opens-no-pr.md#phase-0-opens-no-pr--the-earliest-pr-is-phase-1-hard-rule). A gate marks the end of a **phase**; it does not by itself mark a PR. Only the phases named as delivery boundaries carry integration steps, per [PRs Open at Delivery Boundaries](./prs-open-at-delivery-boundaries-rules.md#prs-open-at-delivery-boundaries-not-every-phase-hard-rule).

**Enforcement**: `plan-checker` flags any phase lacking a `### Phase N Gate` as **HIGH**, and flags a gate lacking concrete verification commands or criteria, or a missing Pause Safety note, as **MEDIUM**. `plan-execution-checker` verifies each phase gate was satisfied before the next phase's work began (via git history). `plan-fixer` adds missing gates and Pause Safety notes.
