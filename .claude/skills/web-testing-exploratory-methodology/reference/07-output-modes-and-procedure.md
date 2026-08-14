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
for it before testing — never guess which plan to write into.

### Mode `plan` (default) — a new plan folder

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

### Mode `delivery` — fold findings into an existing plan's `delivery.md`

Selected with `output-mode: delivery` and a `plan-path`. This mode is the single mechanism behind the
**rule-15 web-UI near-end three-tester retest** (see the
[User-Facing Delivery Hardening Convention](../../../../repo-governance/development/quality/user-facing-delivery-hardening.md)
and the
[Web UX Test-Fixing Planning workflow](../../../../repo-governance/workflows/web/web-ux-test-fixing-planning.md)).
Do not create a new plan folder and do not author `README`/`brd`/`prd`/`tech-docs`/`delivery`.
Instead:

- Append each finding to the host plan's `delivery.md` as a **new unchecked checkbox**, one finding
  per checkbox, source-attributed: `- [ ] EWT-NNN: <defect summary> — fix before archival`, inside a
  clearly-labelled `## Rule-15 three-tester retest follow-ups` section (create it if absent).
- Fold each spec-gap (`SG-###`) into that same section as its own unchecked checkbox tied to the
  host plan's `specs/**` coverage steps.
- Write cited screenshots into the **host plan's** `evidence/` subfolder.
- Run `npm run lint:md` over the edited `delivery.md`, and return the same severity-count summary to
  the orchestrator.

### Mode `local-temp` — a throwaway findings file for direct fixing

Write a single `local-temp/<YYYY-MM-DD>__<slug>/findings.md` carrying the full finding catalog plus
an `evidence/` subfolder beside it. Emit **no**
`README`/`brd`/`prd`/`spec-gaps`/`tech-docs`/`delivery`, and make **no** entry in
`plans/backlog/README.md`. The folder is gitignored and ephemeral. Return the same severity-count
summary plus the `local-temp/` path to the orchestrator.

## Procedure Summary

1. Confirm URL(s) and goal; resolve depth, breakpoints, locales, ground truth.
2. Frame charters from the goal.
3. Establish the baseline (WebFetch and curl): structure, links, headers, redirects.
4. Run interactive/visual/responsive/perf passes across EVERY supported locale × EVERY breakpoint,
   saving cited screenshots to the plan's `evidence/` subfolder; deliberately exercise edge cases and
   boundary conditions, not only the happy path.
5. Run the three **Mandatory Systematic Sweeps** (enumerate, never sample); record each matrix in
   the coverage map, then run the self-completeness check.
6. Compare every observation against ground truth — including each mapped `specs/**` scenario;
   recompute values; confirm reproducibility.
7. Detect spec gaps: catalog correct behaviours the live target exhibits but `specs/**` does not
   cover — giving edge-case behaviours special attention — and draft proposed Gherkin for each.
8. Triage findings with severity and proposed priority; de-duplicate.
9. Write the backlog plan (README, brd, prd, findings, spec-gaps) with steps-to-reproduce, Gherkin
   ACs, and spec-gap proposals.
10. Return a concise summary to the orchestrator: counts by severity, the spec-gap count, the top
    risks, the plan path, and what was _not_ covered.

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
  `evidence/` named by `plan-path` (`delivery` mode), or `local-temp/<dated-slug>/` (`local-temp`
  mode) — plus the `plans/backlog/README.md` index when filing a backlog plan and scratch Playwright
  scripts in `local-temp/`. Nowhere else.
- Never commits or pushes; the maintainer reviews the filed plan.
- Never records secrets, tokens, or real PII in any output (repo no-secrets rule).
