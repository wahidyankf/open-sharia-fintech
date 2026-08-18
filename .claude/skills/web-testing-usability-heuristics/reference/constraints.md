# Constraints

- Does not modify the site under test, fix code, read specs/source as an answer key, or author a
  plan's `tech-docs.md`/`delivery.md` from scratch — in `delivery` mode it only appends finding
  checkboxes to an existing `delivery.md`, never authoring the plan.
- Produces no `spec-gaps.md`. MAY emit `spec-suggestions.md` — usability-grounded Gherkin behaviour
  suggestions, each flagged for spec-aware reconciliation — without reading `specs/**`.
- Writes only to its selected output destination — a `plans/backlog/<dated-slug>/` or
  `plans/in-progress/<slug>/` plan folder (`plan` mode), an existing plan's `delivery.md` +
  `evidence/` named by `plan-path` (`delivery` mode), or `local-tmp/<dated-slug>/` (`local-tmp`
  mode) — plus the `plans/backlog/README.md` index when filing a backlog plan and scratch Playwright
  scripts in `local-tmp/`. Nowhere else.
- Never commits or pushes; the maintainer reviews the filed plan.
- Never records secrets, tokens, or real PII in any output (repo no-secrets rule).
