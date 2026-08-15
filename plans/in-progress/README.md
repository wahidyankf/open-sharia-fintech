# In-Progress Plans

Active project plans currently being worked on.

## Choose the right route 🧭

Use this index to understand delivery work that is underway. For the product story or a first local
run, start with the [repository README](../../README.md) and [documentation hub](../../docs/README.md)
instead. Each plan README explains its outcome and boundaries; its `delivery.md` is the detailed
execution checklist.

## Active Plans

- [ayokoding-learning-path-07-course-authoring-low-level-systems](./ayokoding-learning-path-07-course-authoring-low-level-systems/README.md)
  — Authors seven C/C++/Rust, Linux/Windows OS, and systems-programming course bodies.
- [beaver-chat](./beaver-chat/README.md) — Adds a durable, shared, full-authority browser chat
  for authenticated Codex and OpenCode CLI subprocesses, with streamed replies, direct CLI model
  selection, responsive Flutter UI, and explicitly sandbox-scoped trust.
- [optimize-governance-md](./optimize-governance-md/README.md) — Caps every governance Markdown
  file at 500 words, replaces the byte budget with a word budget, requires annotated `README.md`
  sibling indexes, and adds `when_to_use` frontmatter — across `ose-public` and `ose-private`.
  545 files over the ceiling; remediation is progressive disclosure, enforced by rhino-cli at
  pre-push and in the PR quality gate.
- [repository-onboarding-readme-refresh](./repository-onboarding-readme-refresh/README.md) — Refreshes
  living reader-facing READMEs, onboarding journeys, related docs, and GitHub About metadata across
  `ose-public`, `ose-primer`, and `ose-private`, with product-first paths, fresh-checkout proof, and
  strict secret-safety.

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
