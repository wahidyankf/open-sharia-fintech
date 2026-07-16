# In-Progress Plans

Active project plans currently being worked on.

## Active Plans

- [fundamentally-strong-software-engineer](./fundamentally-strong-software-engineer/) — new breadth-first
  relearn-and-drill tutorial section on ayokoding-www (61 topics, Pass 0 forge prologue + five-pass
  spiral, learning + drilling tracks, Python-primary). Delivery Mode: `main-to-origin-main`.
- [web-ui-code-block-copy-button](./web-ui-code-block-copy-button/) — reusable `libs/web-ui` copy-to-clipboard
  primitive (`CopyButton` + `CodeBlock` + `useCopyToClipboard`) wired into the code-block rendering of
  ayokoding-www (bilingual en/id, live e2e) and ose-www (latent, unit-only), copying verbatim annotated
  source; deploys both apps to prod. Delivery Mode: `worktree-to-pr` (AI-automerge variant).

## Instructions

**Quick Idea Capture**: For 1-3 liner ideas not ready for formal planning, use `../ideas.md`.

**Naming**: Plans in `in-progress/` use NO date prefix — just the slug (e.g., `organiclever-web-responsive-breakpoints/`). Strip the date prefix when moving from `backlog/`.

When starting work on a plan:

1. Move and rename the plan folder: `git mv backlog/YYYY-MM-DD__[identifier]/ in-progress/[identifier]/` (strip the date prefix)
2. Update the plan's README.md status to "In Progress"
3. Add the plan to this list

When completing a plan:

1. Rename and move: `git mv in-progress/[identifier]/ done/YYYY-MM-DD__[identifier]/` using today's completion date
2. Update this list
