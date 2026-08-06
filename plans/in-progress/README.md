# In-Progress Plans

Active project plans currently being worked on.

## Choose the right route 🧭

Use this index to understand delivery work that is underway. For the product story or a first local
run, start with the [repository README](../../README.md) and [documentation hub](../../docs/README.md)
instead. Each plan README explains its outcome and boundaries; its `delivery.md` is the detailed
execution checklist.

## Active Plans

- [repository-onboarding-readme-refresh](./repository-onboarding-readme-refresh/README.md) — Refreshes
  living reader-facing READMEs, onboarding journeys, related docs, and GitHub About metadata across
  `ose-public`, `ose-primer`, and `ose-private`, with product-first paths, fresh-checkout proof, and
  strict secret-safety.
- [sdlc-gate-registry-enforcement](./sdlc-gate-registry-enforcement/README.md) — Makes the already-ratified
  Gate Composition Rule (`(pre-commit ∪ pre-push) == PR gate`) mechanically enforced via a `gates:`
  registry in `repo-config.yml` plus `rhino-cli gate list/run/validate`, and retires `main-ci.yml`
  after folding its unique checks into the PR gate. Closes seven drift findings from the 2026-08-02
  four-repo audit; spans `ose-public`, `ose-primer`, `ose-private`, and `beaver-nest`.

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
