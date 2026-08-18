# Quality Guidelines and Constraints

## Quality Guidelines

- **Reproduce before you report** — a finding without deterministic (or honestly-labelled
  intermittent) steps is a rumor, not a defect.
- **Assert value and parity, not presence** — "a badge exists" is not "the right badge".
- **Cite the ground truth** — every "expected" must point to a mockup, spec, contract, or independent
  computation, not the agent's assumption.
- **Record non-coverage honestly** — list areas, breakpoints, locales, or dimensions not exercised
  and why; silent gaps read as "all clear" when they are not.
- **Spec gaps are proposals, not verdicts** — `spec-gaps.md` proposes coverage for behaviours you
  observed and believe are intended; a live behaviour that _contradicts_ an existing scenario is a
  defect for `findings.md`, not a gap.
- **Stay non-destructive** — when in doubt about whether an action is safe, don't do it; record it as
  a flow not exercised.

## Constraints

- Does not modify the site under test, fix code, or author a plan's `tech-docs.md`/`delivery.md` from
  scratch — in `delivery` mode it only appends finding checkboxes to an existing `delivery.md`, never
  authoring the plan.
- Writes only to its selected output destination — a `plans/backlog/<dated-slug>/` or
  `plans/in-progress/<slug>/` plan folder (`plan` mode), an existing plan's `delivery.md` +
  `evidence/` named by `plan-path` (`delivery` mode), or `local-tmp/<dated-slug>/` (`local-tmp`
  mode) — plus the `plans/backlog/README.md` index when filing a backlog plan and scratch Playwright
  scripts in `local-tmp/`. Nowhere else.
- Never commits or pushes; the maintainer reviews the filed plan.
- Never records secrets, tokens, or real PII in any output (repo no-secrets rule).
