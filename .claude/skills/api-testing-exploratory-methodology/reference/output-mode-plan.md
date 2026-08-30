# Output Mode `plan`

## Mode `plan` (explicit only) — a new plan folder

Use only when the caller literally selects `output-mode: plan`. When omitted, use `local-tmp`.
(When the caller passes `plan-stage: in-progress`,
write the folder under `plans/in-progress/<slug>/` with no date prefix instead of `plans/backlog/`.)

Create `plans/backlog/<slug>/` where `<slug>` is a kebab-case identifier derived from the target +
goal (e.g. `organiclever-be-activities-api-findings`). Follow the
[Plans Organization Convention](../../../../repo-governance/conventions/structure/plans.md) and the
`plan-creating-project-plans` Skill for structure and tone.

Emit these documents:

- **`README.md`** — context; target base URL(s) and environment; protocol; the testing goal; charters
  run; a coverage map (dimensions/operations tested vs. not tested, with reasons, plus the three
  mandatory-sweep matrices and the contract/specs buckets: covered + passing, covered + diverging,
  uncovered); a risk summary (overall impression + top risks); and a Document Map linking the other
  files.
- **`brd.md`** — business framing of the findings: who is affected (API consumers, downstream apps),
  the cost of leaving the defects unfixed, why fixing matters, and business-level success metrics
  (e.g. "all Blocker/Critical findings resolved and re-verified against the contract").
- **`prd.md`** — personas (API consumers); user stories framed as the _desired_ behaviour ("As a
  client, when I POST an invalid body, I receive a 400 with the documented error envelope"); and
  **Gherkin acceptance criteria describing the corrected behaviour** (use the
  `plan-writing-gherkin-criteria` Skill). These ACs become the dev's definition-of-done and the first
  failing tests. Include in-scope / out-of-scope.
- **`findings.md`** — the defect catalog: every finding with the full anatomy, sorted by severity then
  operation. This carries the **steps to reproduce** (exact `curl`/GraphQL) and is the developer's
  primary worklist.
- **`spec-gaps.md`** — the spec-coverage proposals: behaviours observed on the live API that the
  contract or existing `specs/**` Gherkin does not yet describe. Each entry carries an ID (`SG-001`,
  …), the observed behaviour, the operation where it was observed, why it is spec-worthy, the proposed
  Gherkin scenario(s), and the target `specs/` feature file to extend or create. Proposals for
  maintainer confirmation, not assertions that a spec is wrong. If the run surfaced no gaps, omit this
  file and say so explicitly in the `README.md` coverage map.
- **`evidence/`** — the committed evidence subfolder: cited request/response captures (one per
  finding, named `phase-N-<operation>-<condition>.http`/`.json`, secrets redacted) and any long
  captured output a finding references. The folder moves with the plan through its lifecycle
  (`backlog/` → `in-progress/` → `done/`). See the
  [Evidence Capture Convention](../../../../repo-governance/development/quality/evidence-capture.md).
  Omit the folder only when the run captured no file-based evidence.

Do **not** author `tech-docs.md` or `delivery.md` — those are produced when the plan is promoted to
`plans/in-progress/` via `plan-maker`. State this explicitly in `README.md` so the promotion path is
clear.

After writing, add a one-line entry to `plans/backlog/README.md` if that index lists plans, and run
`npm run lint:md` over the new files (or note it for the orchestrator) so they pass the markdown gates.
