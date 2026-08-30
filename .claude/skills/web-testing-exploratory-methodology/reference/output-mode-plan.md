# Output Mode: `plan` (Explicit Only) — a New Plan Folder

Use only when the caller literally selects `output-mode: plan`; omission defaults to `local-tmp`.

(When the caller passes `plan-stage: in-progress`, write the folder under `plans/in-progress/<slug>/`
with no date prefix instead of `plans/backlog/`.) Create `plans/backlog/<slug>/` where `<slug>` is a
kebab-case identifier derived from the target and goal. Follow the
[Plans Organization Convention](../../../../repo-governance/conventions/structure/plans.md) and the
`plan-creating-project-plans` Skill for structure and tone.

Emit these documents (the format mirrors other plan docs, plus a dedicated findings catalog and a
spec-gap catalog):

- **`README.md`** — context; target URL(s) and environment; the testing goal; charters run; a
  coverage map (dimensions/areas tested vs. not tested, with reasons, plus the specs buckets:
  scenarios covered and passing, covered and diverging, and behaviours left uncovered); a risk
  summary; and a Document Map linking the other files.
- **`brd.md`** — business framing of the findings: who is affected, the cost of leaving the defects
  unfixed, why fixing matters, and business-level success metrics.
- **`prd.md`** — personas; user stories framed as the _desired_ behaviour; and **Gherkin acceptance
  criteria describing the corrected behaviour** (use the `plan-writing-gherkin-criteria` Skill).
  Include in-scope / out-of-scope.
- **`findings.md`** — the defect catalog: every finding with the full anatomy, sorted by severity
  then area.
- **`spec-gaps.md`** — the spec-coverage proposals: behaviours observed on the live target that
  existing `specs/**` Gherkin does not yet describe. Each entry carries an ID (`SG-001`, …), the
  observed behaviour, where it was observed, why it is spec-worthy, the proposed Gherkin scenario(s),
  and the target `specs/` feature file. These are proposals for maintainer confirmation, not
  assertions that a spec is wrong. If the run surfaced no gaps, omit this file and say so in the
  `README.md` coverage map.
- **`evidence/`** — the committed evidence subfolder: cited screenshots, Lighthouse JSON, and any
  long captured output a finding references. Moves with the plan through its lifecycle. See the
  [Evidence Capture Convention](../../../../repo-governance/development/quality/evidence-capture.md).
  Omit only when the run captured no file-based evidence.

Do **not** author `tech-docs.md` or `delivery.md` — those are produced when the plan is promoted via
`plan-maker`. State this explicitly in `README.md`.

After writing, add a one-line entry to `plans/backlog/README.md` if that index lists plans, and run
`npm run lint:md` over the new files.
