# In-Progress Plans

Active project plans currently being worked on.

## Active Plans

- [ayokoding-learning-path-04-course-authoring](./ayokoding-learning-path-04-course-authoring/README.md)
  — Wave 2. Trimmed 2026-08-01 to its 21 already-merged/in-flight course bodies (6 net-new AI
  courses + Band 1 Data-depth + Band 2 Web/backend/platform); the remaining 69 courses of its
  original 90-course scope are split across 7 new backlog plans
  (`ayokoding-learning-path-05` through `-11`).
- [vercel-function-cost-reduction](./vercel-function-cost-reduction/README.md) — Cuts gross metered
  Vercel usage from ~$57/mo to under $20/mo so the Pro plan's included credit absorbs it and the
  invoice stays at the $20 subscription. Fixes the root cause: `ayokoding-www` prerenders zero of
  its ~2,068 content pages.
- [plan-decision-integrity-hardening](./plan-decision-integrity-hardening/README.md) — Four
  authoring-time rules plus a mechanical `plan-checker` Step 5o that stop a plan from shipping
  pre-loaded with its own successor, propagated to `ose-primer` and `ose-private` and applied
  retroactively to every open plan in all three repos. Derived from the three-plan AI Model
  Benchmark chain.

Ready-to-execute plans wait in [`../backlog/`](../backlog/README.md); promote one here when
work begins.

## Instructions

**Idea Capture**: For ideas not ready for formal planning, write a two-pager in `../ideas/`.

**Naming**: Plans in `in-progress/` use NO date prefix — just the slug (e.g., `organiclever-web-responsive-breakpoints/`). `backlog/` also uses no date prefix, so moving from `backlog/` is a pure move.

When starting work on a plan:

1. Move the plan folder: `git mv backlog/[identifier]/ in-progress/[identifier]/` (no rename — neither stage carries a date prefix)
2. Update the plan's README.md status to "In Progress"
3. Add the plan to this list

When completing a plan:

1. Rename and move: `git mv in-progress/[identifier]/ done/YYYY-MM-DD__[identifier]/` using today's completion date
2. Update this list
