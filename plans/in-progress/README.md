# In-Progress Plans

Active project plans currently being worked on.

## Active Plans

- [sdlc-gate-registry-enforcement](./sdlc-gate-registry-enforcement/README.md) — Makes the already-ratified
  Gate Composition Rule (`(pre-commit ∪ pre-push) == PR gate`) mechanically enforced via a `gates:`
  registry in `repo-config.yml` plus `rhino-cli gate list/run/validate`, and retires `main-ci.yml`
  after folding its unique checks into the PR gate. Closes seven drift findings from the 2026-08-02
  four-repo audit; spans `ose-public`, `ose-primer`, `ose-private`, and `beaver-nest`.
- [pr-review-cycle-scout-and-typesafety](./pr-review-cycle-scout-and-typesafety/README.md) — Adds a
  `pr-review-scout-maker` pipeline stage 0 (risk-tier classification + specialist selection + context
  assembly, moved off `pr-review-synthesis-maker`), a ninth `pr-review-types-maker` discipline for
  cross-language type-soundness (TypeScript/Rust/F#/C#), and a `Cycle: N of {total}` field on every
  Consolidated Review Header. `ose-public`-only, `worktree-to-pr` delivery, dogfoods the new pipeline
  against its own PR.

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
