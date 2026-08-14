# Output Modes, Procedure Summary, Quality Guidelines, and Constraints

## Output Modes (Choose at Invocation)

The **`output-mode`** input selects where findings land. The evaluation methodology, finding anatomy,
and severity/priority scales are identical in every mode — only the **destination** changes.
`output-mode` defaults to `plan`, so prior invocations are unaffected.

| `output-mode`    | Destination                                                                                                         | Use when                                                                                                                                         |
| ---------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `plan` (default) | A new plan folder under `plans/backlog/` (or `plans/in-progress/` when the caller passes `plan-stage: in-progress`) | The findings need their own tracked, promotable plan a developer picks up later.                                                                 |
| `delivery`       | Appended as unchecked task-list checkboxes into an **existing** plan's `delivery.md` (requires a `plan-path`)       | The findings belong to a plan already in flight — the mechanism behind the rule-15 near-end three-tester retest, folded back into the host plan. |
| `local-temp`     | A single `findings.md` (+ an `evidence/` subfolder) under `local-temp/<slug>/`                                      | The caller will fix the findings immediately in the same session and wants no plan paperwork. Ephemeral and gitignored.                          |

If `output-mode` is omitted, default to `plan`. If `delivery` is selected without a `plan-path`, ask
for it before evaluating — never guess which plan to write into.

### Mode `plan` (default) — a new plan folder

(When the caller passes `plan-stage: in-progress`, write the folder under
`plans/in-progress/<slug>/` with no date prefix instead of `plans/backlog/`.) Create
`plans/backlog/<slug>/` where `<slug>` is a kebab-case identifier derived from the target + design goal
(e.g. `organiclever-pricing-design-findings`). Follow the
[Plans Organization Convention](../../../../repo-governance/conventions/structure/plans.md) and the
`plan-creating-project-plans` Skill for structure and tone.

Emit these documents (the format mirrors the two sibling testers, for triad symmetry):

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
- **`findings.md`** — the design-defect catalog: every finding with the full anatomy, sorted by
  severity then area. Carries the **steps to reproduce** and is the developer's primary worklist.
- **`spec-gaps.md`** — the design-spec proposals: on-design behaviours the live target exhibits (or
  should) that existing `specs/**` Gherkin does not yet describe — e.g. a responsive design rule or a
  token-state behaviour worth protecting. Each entry carries an ID (`SG-001`, …), the observed/desired
  design behaviour, where it applies, why it is spec-worthy, the proposed Gherkin scenario(s), and the
  target `specs/` feature file to extend or create. These are proposals for maintainer confirmation. If
  the run surfaced no gaps, omit this file and say so explicitly in the `README.md` coverage map.
- **`evidence/`** — the committed evidence subfolder: cited screenshots (one per finding per
  locale/breakpoint, named `phase-N-<description>-<locale>-<breakpoint>px.png`) and any captured
  computed-style/mockup-comparison output a finding references. The folder moves with the plan through
  its lifecycle (`backlog/` → `in-progress/` → `done/`). See the
  [Evidence Capture Convention](../../../../repo-governance/development/quality/evidence-capture.md).
  Omit the folder only when the run captured no file-based evidence.

Do **not** author `tech-docs.md` or `delivery.md` — those are produced when the plan is promoted to
`plans/in-progress/` via `plan-maker` (which grills the maintainer and adds the TDD-shaped delivery
checklist). State this explicitly in `README.md` so the promotion path is clear.

After writing, add a one-line entry to `plans/backlog/README.md` if that index lists plans, and run
`npm run lint:md` over the new files (or note it for the orchestrator) so they pass the markdown gates.

### Mode `delivery` — fold findings into an existing plan's `delivery.md`

Selected with `output-mode: delivery` and a `plan-path` (a plan folder already in
`plans/in-progress/` or `plans/backlog/`). This mode is the single mechanism behind the **rule-15
web-UI near-end three-tester retest** (see the
[User-Facing Delivery Hardening Convention](../../../../repo-governance/development/quality/user-facing-delivery-hardening.md)
and the
[Web UX Test-Fixing Planning workflow](../../../../repo-governance/workflows/web/web-ux-test-fixing-planning.md)).
Do not create a new plan folder and do not author `README`/`brd`/`prd`/`tech-docs`/`delivery` — the
host plan already has them. Instead:

- Append each finding to the host plan's `delivery.md` as a **new unchecked checkbox**, one finding per
  checkbox, source-attributed: `- [ ] DWT-NNN: <defect summary> — fix before archival`, inside a
  clearly-labelled `## Rule-15 three-tester retest follow-ups` section (create it if absent).
- Fold each spec-gap (`SG-###`) into that same section as its own unchecked checkbox tied to the host
  plan's `specs/**` coverage steps.
- Write cited screenshots into the **host plan's** `evidence/` subfolder (same
  `phase-N-<description>-<locale>-<breakpoint>px.png` naming), so the evidence travels with the plan it
  belongs to.
- Run `npm run lint:md` over the edited `delivery.md`, and return the same severity-count summary to
  the orchestrator.

### Mode `local-temp` — a throwaway findings file for direct fixing

Selected with `output-mode: local-temp`. Write a single
`local-temp/<YYYY-MM-DD>__<slug>/findings.md` carrying the full finding catalog (same anatomy,
severity/priority, steps-to-reproduce) plus an `evidence/` subfolder beside it for cited screenshots.
Emit **no** `README`/`brd`/`prd`/`spec-gaps`/`tech-docs`/`delivery`, and make **no** entry in
`plans/backlog/README.md`. The folder is gitignored and ephemeral — the calling session reads
`findings.md` and applies the fixes directly in the same run. Return the same severity-count summary
plus the `local-temp/` path to the orchestrator.

## Procedure Summary

1. Confirm URL(s) + design goal; resolve depth, breakpoints, locales, and the design ground truth
   (mockups, tokens, primitives, optional external source).
2. Establish the baseline (`WebFetch`): structure, routes, locale-prefix.
3. Render, measure computed styles, and screenshot each route across EVERY supported locale × EVERY
   breakpoint (375 / 768 / 1280, plus 320/1440 when `thorough`), saving cited screenshots to the plan's
   `evidence/` subfolder.
4. Compare every observation against the five ground-truth sources; for design practice, cite the
   principle (delegating to `web-researcher` when unsure). Deliberately probe spacing/density ("not
   cramped"), alignment, hierarchy, and cross-surface consistency — not just colour/mockup match.
5. Run the two **Mandatory Systematic Checks** (enumerate, never sample): the raw/unstyled
   native-element audit and the intra-form & cross-surface styling-consistency matrix; record each in
   the coverage map.
6. Detect design-spec gaps: catalog on-design behaviours worth protecting that `specs/**` does not
   cover, and draft proposed Gherkin for each.
7. Triage findings with severity + proposed priority, each citing its violated ground truth/principle;
   de-duplicate.
8. Write the backlog plan (README, brd, prd, findings, spec-gaps when any surfaced) with
   steps-to-reproduce and Gherkin ACs for the on-design result.
9. Return a concise summary to the orchestrator: counts by severity, the spec-gap count, the top
   design risks, the plan path, and what was _not_ covered.

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
  `evidence/` named by `plan-path` (`delivery` mode), or `local-temp/<dated-slug>/` (`local-temp`
  mode) — plus the `plans/backlog/README.md` index when filing a backlog plan and scratch Playwright
  scripts in `local-temp/`. Nowhere else.
- Never commits or pushes; the maintainer reviews the filed plan.
- Never records secrets, tokens, or real PII in any output (repo no-secrets rule).
