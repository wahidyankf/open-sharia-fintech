# Output Mode: `plan` (Explicit Only) — a New Plan Folder

Use only when the caller literally selects `output-mode: plan`; omission defaults to `local-tmp`.

(When the caller passes `plan-stage: in-progress`, write the folder under
`plans/in-progress/<slug>/` with no date prefix instead of `plans/backlog/`.) Create
`plans/backlog/<slug>/` where `<slug>` is a kebab-case identifier derived from the target + design goal
(e.g. `organiclever-pricing-design-findings`). Follow the
[Plans Organization Convention](../../../../repo-governance/conventions/structure/plans.md) and the
`plan-creating-project-plans` Skill for structure and tone.

Run the full pre-write grill from `plan-creating-project-plans`, then emit the mature core with a
mapped `tech-docs/` form:

- **`README.md`** — context; target URL(s) and environment; the design goal; the design sources used;
  a coverage map (dimensions / breakpoints / locales evaluated vs. not, with reasons); an overall
  design-fidelity impression + top risks; and a Document Map linking the other files.
- **`brd.md`** — business framing of the findings: who is affected (brand, design language), the cost
  of leaving the drift unfixed, why fixing matters, and business-level success metrics (e.g. "all
  Blocker/Critical design findings resolved and re-verified at every breakpoint/locale").
- **`prd.md`** — personas; user stories framed as the _designed_ behaviour ("As a user, the pricing
  page renders in the brand palette and matches the mockup at every breakpoint"); and **Gherkin
  acceptance criteria describing the on-design result** (use the `plan-writing-gherkin-criteria`
  Skill). Include in-scope / out-of-scope.
- **`tech-docs/README.md`** — maps the technical companions and explains the selected remediation
  architecture and constraints.
- **`tech-docs/findings.md`** — the design-defect catalog: every finding with the full anatomy, sorted by
  severity then area. Carries the **steps to reproduce** and is the developer's primary worklist.
- **`tech-docs/spec-gaps.md`** — the design-spec proposals: on-design behaviours the live target exhibits (or
  should) that existing `specs/**` Gherkin does not yet describe — e.g. a responsive design rule or a
  token-state behaviour worth protecting. Each entry carries an ID (`SG-001`, …), the observed/desired
  design behaviour, where it applies, why it is spec-worthy, the proposed Gherkin scenario(s), and the
  target `specs/` feature file to extend or create. These are proposals for maintainer confirmation. If
  the run surfaced no gaps, omit this file and say so explicitly in the `README.md` coverage map.
- **`delivery.md`** — cohesive outcomes tied to PRD criteria, with Input/Outcome/Proof, granular
  action checkboxes, separate detailed RED/GREEN/REFACTOR cycles, phase gates, natural seams, and
  archival gates.
- **`learnings.md`** — the required transient Knowledge Capture log scaffold.
- **`evidence/`** — the committed evidence subfolder: cited screenshots (one per finding per
  locale/breakpoint, named `phase-N-<description>-<locale>-<breakpoint>px.png`) and any captured
  computed-style/mockup-comparison output a finding references. The folder moves with the plan through
  its lifecycle (`backlog/` → `in-progress/` → `done/`). See the
  [Evidence Capture Convention](../../../../repo-governance/development/quality/evidence-capture.md).
  Omit the folder only when the run captured no file-based evidence.

After writing, add a one-line entry to `plans/backlog/README.md` if that index lists plans, and run
the plan quality gate, including `rtk npm run lint:md`, over the new files.
