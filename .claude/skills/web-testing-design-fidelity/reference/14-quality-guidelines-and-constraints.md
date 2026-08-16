# Quality Guidelines and Constraints

## Quality Guidelines

- **Cite the ground truth, never a vibe** — every finding names the mockup, token, primitive, external
  source, or design principle it breaks. No ground truth, no finding.
- **Assert the rendered value, not presence** — "a button exists" is not "the on-token button"; quote
  the computed colour/spacing, compared to the designed value.
- **Stay on the runtime side** — judge the **rendered** page; do not audit component source (that is
  `swe-ui-checker`). Report the runtime symptom; note a source locus only as a hypothesis.
- **Reproduce before you report** — a design claim without deterministic steps (and the
  breakpoint/locale) is an opinion, not a finding.
- **Record non-coverage honestly** — list dimensions, breakpoints, locales, or sources not exercised
  and why; silent gaps read as "all on-design" when they are not.
- **Stay non-destructive** — when unsure an action is safe, don't; record it as a flow not exercised.

## Constraints

- Does not modify the site under test, fix code, audit component source the way `swe-ui-checker` does,
  or author a plan's `tech-docs.md`/`delivery.md` from scratch — in `delivery` mode it only appends
  finding checkboxes to an existing `delivery.md`, never authoring the plan.
- Writes only to its selected output destination — a `plans/backlog/<dated-slug>/` or
  `plans/in-progress/<slug>/` plan folder (`plan` mode), an existing plan's `delivery.md` +
  `evidence/` named by `plan-path` (`delivery` mode), or `local-tmp/<dated-slug>/` (`local-tmp`
  mode) — plus the `plans/backlog/README.md` index when filing a backlog plan and scratch Playwright
  scripts in `local-tmp/`. Nowhere else.
- Never commits or pushes; the maintainer reviews the filed plan.
- Never records secrets, tokens, or real PII in any output (repo no-secrets rule).
