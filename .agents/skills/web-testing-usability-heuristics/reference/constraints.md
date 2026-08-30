# Constraints

- Does not modify the site under test, fix code, read specs/source as an answer key, or author a
  plan's `tech-docs.md`/`delivery.md` from scratch — in `delivery` mode it only appends finding
  checkboxes to an existing `delivery.md`, never authoring the plan.
- Produces no `spec-gaps.md`. MAY emit `spec-suggestions.md` — usability-grounded Gherkin behaviour
  suggestions, each flagged for spec-aware reconciliation — without reading `specs/**`.
- Writes only to its resolved output destination: `local-tmp/<dated-slug>/` by default; an existing
  plan's `delivery.md` + `evidence/` in `delivery` mode; or a `plans/backlog/<slug>/` or
  `plans/in-progress/<slug>/` folder in explicitly authorized `plan` mode. Only plan mode may update
  `plans/backlog/README.md`; scratch Playwright scripts remain in `local-tmp/`. Nowhere else.
- Never commits or pushes; the maintainer reviews the filed plan.
- Never records secrets, tokens, or real PII in any output (repo no-secrets rule).
