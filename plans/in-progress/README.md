# In-Progress Plans

Active project plans currently being worked on.

## Choose the right route 🧭

Use this index to understand delivery work that is underway. For the product story or a first local
run, start with the [repository README](../../README.md) and [documentation hub](../../docs/README.md)
instead. Each plan README explains its outcome and boundaries; its `delivery.md` is the detailed
execution checklist.

## Active Plans

- [beaver-chat](./beaver-chat/README.md) — Adds a durable, shared, full-authority browser chat
  for authenticated Codex and OpenCode CLI subprocesses, with streamed replies, direct CLI model
  selection, responsive Flutter UI, and explicitly sandbox-scoped trust.
- [repository-onboarding-readme-refresh](./repository-onboarding-readme-refresh/README.md) — Refreshes
  living reader-facing READMEs, onboarding journeys, related docs, and GitHub About metadata across
  `ose-public` and `ose-private`, with product-first paths, fresh-checkout proof, and
  strict secret-safety (`ose-primer` units descoped 2026-08-16).
- [update-harness-support](./update-harness-support/README.md) — Reduces supported coding-agent
  harnesses from eleven to three (Claude Code, OpenCode, OpenAI Codex CLI), raises Codex to
  generated parity, adopts `.agents/skills/` as a cross-vendor surface, generates the
  platform-bindings catalog from `repo-config.yml`, and gives every binding file a declared
  ownership class enforced by the `harness-ownership` and `harness-catalog` gates. Automated
  external-drift detection (a freshness gate) was considered and deliberately not shipped;
  re-verification against upstream stays manual and on-demand.

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
