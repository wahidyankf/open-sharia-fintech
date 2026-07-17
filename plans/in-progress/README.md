# In-Progress Plans

Active project plans currently being worked on.

## Active Plans

- [fundamentally-strong-software-engineer](./fundamentally-strong-software-engineer/) — new breadth-first
  relearn-and-drill tutorial section on ayokoding-www (61 topics, Pass 0 forge prologue + five-pass
  spiral, learning + drilling tracks, Python-primary). Delivery Mode: `main-to-origin-main`.
- [rhino-cli-source-drift-reconciliation](./rhino-cli-source-drift-reconciliation/) — reconcile the
  pre-existing rhino-cli `src/` drift across ose-public / ose-primer / ose-infra to a single canonical
  union so the tri-repo byte-identity boundary holds. **Predecessor** of the two rhino-cli plans below.
- [rhino-speccoverage-multiline-scenario-scan](./rhino-speccoverage-multiline-scenario-scan/) — make
  rhino's `speccoverage` scenario-title extractor multi-line-aware so a prettier-wrapped `Scenario(...)`
  call no longer reports a spurious coverage gap. Runs after the drift reconciliation.
- [e2e-scenario-coverage-gap-detector](./e2e-scenario-coverage-gap-detector/) — detect Gherkin scenarios
  that silently lose E2E coverage under `playwright-bdd`'s `missingSteps: skip-scenario` config. Runs
  after the drift reconciliation.

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
