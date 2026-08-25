---
title: "Purpose, Execution Mode, and When to Use"
description: What this workflow does, who orchestrates it, and when (not) to promote a two-pager into a backlog plan.
when_to_use: Use when deciding whether a two-pager is ready for the promotion procedure, and who runs it.
---

# Purpose, Execution Mode, and When to Use

**Purpose**: Turn one ripe two-pager in [`plans/ideas/`](../../../conventions/structure/plans/ideas-folder-overview-rationale-and-file-layout.md#ideas-folder-two-pagers)
into a full five-document backlog plan, operationalizing the four-step
[Promoting a Two-Pager to a Full Plan](../../../conventions/structure/plans/promoting-ideas-and-worked-examples.md#promoting-a-two-pager-to-a-full-plan)
procedure end to end. It gates the brief for completeness, runs the deep `web-researcher` prior-art
study that the capture phase deliberately deferred, hands the enriched brief to
[`plan-planning`](../plan-planning.md) with `target-stage=backlog`, and retires the two-pager so the
idea now lives as a plan.

> **The outcome is the plan, not the implementation.** This workflow never writes application or
> library code, never runs a delivery checklist, and never touches `plans/in-progress/`. It produces
> a proposal in `plans/backlog/`. The actual work happens later: the [Plan Execution
> workflow](../plan-execution.md)'s own Step 0 promotes the backlog plan to `plans/in-progress/`
> through the delivery-mode-aware
> [Starting Work procedure](../../../conventions/structure/plans/starting-and-completing-work.md#starting-work)
> as its mandatory precondition. A `*-to-pr` or direct-push-unavailable route merges a pure-move
> worktree PR first; only a permitted, selected direct-push mode pushes directly to `origin main`.
> No separate human promotion step is required.

This is a `planning`-type workflow: a single forward procedure whose terminal deliverable is a plan
document. It is **not** an iterative quality gate.

## Execution Mode

**Direct Orchestration** — the calling context (top-level assistant session) orchestrates the
phases, delegating the prior-art survey to `web-researcher` via the Agent tool, running the promotion
checkpoint inline (so the user's conversation is preserved), and invoking the
[plan-planning workflow](../plan-planning.md) for plan authoring. The deep design grill is left to
`plan-planning`'s own grill, seeded by this workflow's handoff, to avoid double-grilling the user.

## When to use

- A two-pager has matured — every section holds a real answer and the only open questions are ones
  that genuinely need a full plan's deeper design/research — and you want it scheduled as a plan.
- A Knowledge-Capture learning captured as a two-pager is now plan-ready.
- You want the deferred deep prior-art study run and folded into the plan as design input in one pass.

Do **not** use it to file a brand-new idea from a raw prompt (that is [`plan-planning`](../plan-planning.md)
directly), nor to execute a plan (that is [`plan-execution`](../plan-execution.md)).
