# In-Progress Plans

Active project plans currently being worked on.

## Choose the right route 🧭

Use this index to understand delivery work that is underway. For the product story or a first local
run, start with the [repository README](../../README.md) and [documentation hub](../../docs/README.md)
instead. Each plan README explains its outcome and boundaries; its `delivery.md` is the detailed
execution checklist.

## Active Plans

- [rewrite-rhino-cli-to-fsharp](./rewrite-rhino-cli-to-fsharp/README.md) — replace the Rust
  `rhino-cli` with a behavior-equivalent F# implementation across all 13 namespaces and 525
  Gherkin scenarios, namespace by namespace behind a dispatch shim, then retire the Rust crate and
  tear down the Rust CI surface. Lands in both `ose-public` and `ose-private`; the plan docs are
  single-sourced here, so the two repos can never drift. Thirteen phases, six waves, roughly 71
  implementation PRs at one feature file per PR. Started 2026-08-25.

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
