# In-Progress Plans

Active project plans currently being worked on.

## Active Plans

- [ayokoding-learning-path-04-course-authoring](./ayokoding-learning-path-04-course-authoring/README.md)
  — Wave 2. Authors the `careers/` course bodies band by band, each from its `syllabus/` spec.
- [vercel-function-cost-reduction](./vercel-function-cost-reduction/README.md) — Cuts gross metered
  Vercel usage from ~$57/mo to under $20/mo so the Pro plan's included credit absorbs it and the
  invoice stays at the $20 subscription. Fixes the root cause: `ayokoding-www` prerenders zero of
  its ~2,068 content pages.

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
