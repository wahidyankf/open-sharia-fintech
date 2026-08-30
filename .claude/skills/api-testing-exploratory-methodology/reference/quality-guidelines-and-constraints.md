# Quality Guidelines and Constraints

- **Reproduce before you report** — a finding without a deterministic (or honestly-labelled
  intermittent) `curl`/GraphQL repro is a rumor, not a defect.
- **Assert shape and value, not presence** — "a field exists" is not "the right field with the right
  type and value"; "a 200 came back" is not "the documented representation came back".
- **Cite the ground truth** — every "expected" must point to a contract clause, a `.feature` scenario,
  an RFC, or an independent computation, not the agent's assumption.
- **Record non-coverage honestly** — list operations, methods, auth contexts, or dimensions not
  exercised and why; silent gaps read as "all clear" when they are not.
- **Spec gaps are proposals, not verdicts** — `spec-gaps.md` proposes coverage for behaviours you
  observed and believe are intended; a live behaviour that _contradicts_ the contract or an existing
  scenario is a defect for `findings.md`, not a gap.
- **Stay non-destructive** — when in doubt about whether a request is safe or authorized, don't send
  it; record the operation as not exercised. Redact every credential in every capture.

## Constraints

- Does not modify the API's persistent state beyond benign, explicitly-authorized writes; does not fix
  code, and does not author a plan's `tech-docs.md`/`delivery.md` from scratch — in `delivery` mode it
  only appends finding checkboxes to an existing `delivery.md`, never authoring the plan.
- Never drives a browser and never audits rendered UI, HTML/CSS, responsive layout, or visual design —
  that is the web tester triad's surface.
- Writes only to its resolved output destination: `local-tmp/<dated-slug>/` by default; an existing
  plan's `delivery.md` + `evidence/` in `delivery` mode; or a `plans/backlog/<slug>/` or
  `plans/in-progress/<slug>/` folder in explicitly authorized `plan` mode. Only plan mode may update
  `plans/backlog/README.md`; scratch request scripts remain in `local-tmp/`. Nowhere else.
- Never commits or pushes; the maintainer reviews the filed plan.
- Never records secrets, tokens, `Authorization` values, or real PII in any output (repo no-secrets
  rule) — redact them in every captured request/response.
