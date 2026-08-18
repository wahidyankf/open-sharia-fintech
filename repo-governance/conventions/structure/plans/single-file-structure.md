---
title: "Single-File Structure"
description: Specifies the mandatory section order for a single-file README.md plan and when this exception structure is permitted.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when authoring a plan that meets all single-file exception criteria.
---

# Single-File Structure

```
2025-12-01__feature-name/
└── README.md                # All-in-one plan document
```

**README.md sections** (mandatory, in order):

1. **Context** — project description, background, non-technical framing
2. **Scope** — in-scope + out-of-scope; affected subrepos / apps named explicitly
3. **Business rationale (condensed BRD)** — why this matters, business goals, affected roles, success metrics (gut-based reasoning OK; judgment calls labeled; fabricated KPIs forbidden; internet citations inline with excerpt + URL + access date)
4. **Product requirements (condensed PRD)** — user stories (`As a … I want … So that …`), Gherkin acceptance criteria, product scope
5. **Technical approach** — architecture, design decisions, implementation approach
6. **Worktree** — declared worktree path (`worktrees/<plan-identifier>/`) and provisioning command (see [Worktree Specification](./worktree-specification.md#worktree-specification))
7. **Delivery checklist** — phased `- [ ]` items with one concrete action per checkbox; opens with the `[AI]`/`[HUMAN]` executor legend; every phase ends with a `### Phase N Gate` and a Pause Safety note (see Executor Tagging and Phases as Natural Pauses With Clear Gates above)
8. **Quality gates** — local gates + CI gates that must pass
9. **Verification** — how to confirm the plan is done

If the author cannot comfortably fit both the condensed BRD and condensed PRD sections into the README without crowding out the technical sections, promote the plan to the five-document multi-file layout before execution begins.
