# Structure and Requirements Validation (Scope 1-2)

## 1. Structure Validation

- Plan folder naming: `YYYY-MM-DD-project-identifier`.
- File structure: **Multi-file (default)** — five files `README.md`, `brd.md`, `prd.md`,
  `tech-docs.md`, `delivery.md`; flag missing files **HIGH**. **Single-file (exception)** — one
  `README.md` with eight mandatory sections (Context, Scope, Business Rationale, Product
  Requirements, Technical Approach, Delivery Checklist, Quality Gates, Verification); flag missing
  sections **HIGH**.
- Required sections per file: BRD (business goal, impact, affected roles, success metrics,
  non-goals, risks); PRD (product overview, personas, user stories, Gherkin acceptance criteria,
  product scope, product risks); tech-docs (architecture, decisions, file-impact, rollback);
  delivery (phased checkboxes with implementation-notes blocks).
- Folder sits under `plans/backlog/`, `plans/in-progress/`, or `plans/done/`.

## 2. Requirements Validation (BRD + PRD)

Per the
[Content-Placement Rules](../../../../repo-governance/conventions/structure/plans/content-placement-rules.md#content-placement-rules-brdmd-vs-prdmd),
business and product concerns live in separate files — misplacement is a structural violation, not
a stylistic issue.

**In `brd.md` (business perspective)**: business goal/rationale; business impact (pain points,
expected benefits); affected roles — **not** sponsor/stakeholder sign-off mapping (flag **HIGH** if
present); business-level success metrics grounded in observable facts, cited measurements (inline
excerpt, URL, access date), qualitative reasoning, or explicitly labeled Judgment calls — flag
**HIGH** a fabricated numeric target presented as already-measured with no baseline; business-scope
Non-Goals; business risks and mitigations.

**In `prd.md` (product perspective)**: product overview; personas (solo-maintainer hats and
consuming agents — not external stakeholder roles, flag **HIGH** if present); user stories in
`As a … I want … So that …` form; Gherkin acceptance criteria (Given/When/Then/And; flag if Gherkin
lives elsewhere); **step-keyword cardinality HARD rule** — every `Scenario` uses exactly one primary
`Given`, `When`, `Then`, extras chain with `And`/`But`, `Background` and `Scenario Outline`
`Examples` tables exempt; flag violations **HIGH**; applies to `plans/in-progress/` and
`plans/backlog/` (`plans/done/` exempt) — see
[Acceptance Criteria Convention §Step-Keyword Cardinality](../../../../repo-governance/development/infra/acceptance-criteria/gherkin-format-and-step-keyword-cardinality.md#step-keyword-cardinality-hard-rule);
product scope (in/out); product-level risks.

**Content-placement violations (flag HIGH)**: business framing (sign-off, sponsors, stakeholders,
KPIs) in `prd.md`; user stories or Gherkin in `brd.md`; personas in `brd.md`; affected roles in
`prd.md`.

**Internet-citation compliance**: a plan citing external data must inline the specific
excerpt/number/quote plus URL and access date — URL-only citations are a finding (links rot, future
readers must verify claims from the plan alone).
