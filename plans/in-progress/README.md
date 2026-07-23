# In-Progress Plans

Active project plans currently being worked on.

## Active Plans

- [worktree-to-pr-hardening](./worktree-to-pr-hardening/README.md)
  — Hardens the `worktree-to-pr` delivery workflow by decomposing the monolithic `pr-review-maker`
  into eight specialist reviewer agents plus a mandatory `pr-review-synthesis-maker` coordinator, with
  a reviewer-discipline convention, workflow revision (retiring the monolith at cutover), quality-gate
  enhancements, and a post-cutover monitoring + rollback trigger. Scoped as a **three-repo parity
  deliverable** (`ose-public` source of truth → `ose-primer` + `ose-infra` downstream, each propagated
  via its own `worktree-to-pr` cycle). Decisions D1–D15 resolved; passed the strict plan-quality-gate.

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
