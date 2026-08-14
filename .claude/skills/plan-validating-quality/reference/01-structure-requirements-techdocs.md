# Validation Scope 1-3: Structure, Requirements, Technical Documentation

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
[Content-Placement Rules](../../../../repo-governance/conventions/structure/plans/14-content-placement-rules.md#content-placement-rules-brdmd-vs-prdmd),
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
[Acceptance Criteria Convention §Step-Keyword Cardinality](../../../../repo-governance/development/infra/acceptance-criteria/02-gherkin-format-and-step-keyword-cardinality.md#step-keyword-cardinality-hard-rule);
product scope (in/out); product-level risks.

**Content-placement violations (flag HIGH)**: business framing (sign-off, sponsors, stakeholders,
KPIs) in `prd.md`; user stories or Gherkin in `brd.md`; personas in `brd.md`; affected roles in
`prd.md`.

**Internet-citation compliance**: a plan citing external data must inline the specific
excerpt/number/quote plus URL and access date — URL-only citations are a finding (links rot, future
readers must verify claims from the plan alone).

## 3. Technical Documentation Validation

Architecture documented; design decisions justified; implementation approach clear; dependencies
listed; testing strategy defined.

**File-impact tree (HARD RULE)**: `tech-docs.md` has a `## File-Impact Analysis` whose primary view
is a root-relative fenced `text` tree; each planned path or bounded pattern carries `[E]`, `[N]`,
`[D]`, or `[G]` — the tree, not prose bullets, is the scan-first scope. Flag a missing tree, missing
action markers, an unbounded/vague target, or prose as the primary view as **HIGH**. An optional
`### More Detail` section must immediately follow the tree and only explain mechanics/ordering/
discovery/archival follow-up — it cannot replace the tree or contain delivery checkboxes. See
[Plans Organization Convention §File-Impact Analysis Format](../../../../repo-governance/conventions/structure/plans/12-file-impact-analysis-format.md#file-impact-analysis-format-hard-rule).

### Diagram Format Check

Audit all plan files (`README.md`, `brd.md`, `prd.md`, `tech-docs.md`, `delivery.md`):

- **MEDIUM**: ASCII art depicting component interactions, data flows, sequences, state machines, or
  decision branches — a Mermaid diagram would fit better. Simple directory-tree listings are exempt.
- **MEDIUM (under-diagrammed plan)**: a non-trivial plan covers a diagram-warranting concern
  (component interactions, agent/system sequence, state transitions, decision branches,
  upstream/downstream dependency position, phase/delivery flow) with no diagram for it. Trivial
  plans (single-file config bumps, renames, doc fixes, no-behavior-change dependency bumps) are
  exempt. Each undiagrammed concern is a separate finding.
- Reference: [Plans Organization Convention §Diagrams in Plans](../../../../repo-governance/conventions/structure/plans.md) and
  [Diagrams Convention](../../../../repo-governance/conventions/formatting/diagrams.md).
