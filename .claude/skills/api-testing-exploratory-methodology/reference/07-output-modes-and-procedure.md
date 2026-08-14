# Output Modes, Procedure Summary, Quality Guidelines, and Constraints

## Output Modes (Choose at Invocation)

The **`output-mode`** input selects where findings land. The evaluation methodology, finding anatomy,
and severity/priority scales above are identical in every mode — only the **destination** changes.
`output-mode` defaults to `plan`.

| `output-mode`    | Destination                                                                                                         | Use when                                                                                                                                |
| ---------------- | ------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `plan` (default) | A new plan folder under `plans/backlog/` (or `plans/in-progress/` when the caller passes `plan-stage: in-progress`) | The findings need their own tracked, promotable plan a developer picks up later.                                                        |
| `delivery`       | Appended as unchecked task-list checkboxes into an **existing** plan's `delivery.md` (requires a `plan-path`)       | The findings belong to a plan already in flight — the API-side analogue of the rule-15 near-end retest, folded back into the host plan. |
| `local-temp`     | A single `findings.md` (+ an `evidence/` subfolder) under `local-temp/<slug>/`                                      | The caller will fix the findings immediately in the same session and wants no plan paperwork. Ephemeral and gitignored.                 |

If `output-mode` is omitted, default to `plan`. If `delivery` is selected without a `plan-path`, ask
for it before testing — never guess which plan to write into.

### Mode `plan` (default) — a new plan folder

This is the default when `output-mode` is omitted. (When the caller passes `plan-stage: in-progress`,
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

### Mode `delivery` — fold findings into an existing plan's `delivery.md`

Selected with `output-mode: delivery` and a `plan-path` (a plan folder already in
`plans/in-progress/` or `plans/backlog/`). This is the API-side analogue of the
[User-Facing Delivery Hardening](../../../../repo-governance/development/quality/user-facing-delivery-hardening.md)
near-end retest, folded back into the host plan. Do not create a new plan folder and do not author
`README`/`brd`/`prd`/`tech-docs`/`delivery` — the host plan already has them. Instead:

- Append each finding to the host plan's `delivery.md` as a **new unchecked checkbox**, one finding per
  checkbox, source-attributed: `- [ ] AET-NNN: <defect summary> — fix before archival`, inside a
  clearly-labelled `## API exploratory-test retest follow-ups` section (create it if absent).
- Fold each spec-gap (`SG-###`) into that same section as its own unchecked checkbox tied to the host
  plan's `specs/**` coverage steps.
- Write cited captures into the **host plan's** `evidence/` subfolder (same naming), so the evidence
  travels with the plan it belongs to.
- Run `npm run lint:md` over the edited `delivery.md`, and return the same severity-count summary to
  the orchestrator.

### Mode `local-temp` — a throwaway findings file for direct fixing

Selected with `output-mode: local-temp`. Write a single `local-temp/<YYYY-MM-DD>__<slug>/findings.md`
carrying the full finding catalog (same anatomy, severity/priority, steps-to-reproduce) plus an
`evidence/` subfolder beside it for cited captures. Emit **no**
`README`/`brd`/`prd`/`spec-gaps`/`tech-docs`/`delivery`, and make **no** entry in
`plans/backlog/README.md`. The folder is gitignored and ephemeral — the calling session reads
`findings.md` and applies the fixes directly in the same run. Return the same severity-count summary
plus the `local-temp/` path to the orchestrator.

## Procedure Summary

1. Confirm target(s) + goal; resolve protocol (auto-detect if unset), depth, contract pointer, and
   synthetic auth context.
2. Frame charters from the goal.
3. Establish the baseline (curl + contract discovery / GraphQL introspection): operations, status,
   headers, error envelopes.
4. Run edge / negative / auth-context probes across operations — deliberately exercise boundary and
   malformed payloads (the Data dimension + Antisocial tour), not only the happy path — surfacing at
   least one edge observation or recording that none were found; save cited captures to the plan's
   `evidence/` subfolder with secrets redacted.
5. Run the three **Mandatory Systematic Sweeps** (enumerate, never sample): the operation × property
   matrix, the cross-cutting convention round-trip, and the declared-invariant conformance pass;
   record each matrix in the coverage map, then run the self-completeness check.
6. Compare every observation against ground truth — the contract (OpenAPI/SDL) AND each mapped
   `specs/**` scenario; recompute derived values; confirm reproducibility.
7. Detect spec gaps: catalog correct behaviours the live API exhibits but the contract/`specs/**` does
   not cover — giving edge-case behaviours special attention — and draft proposed Gherkin for each.
8. Triage findings with severity + proposed priority; de-duplicate.
9. Write the backlog plan (README, brd, prd, findings, spec-gaps) with steps-to-reproduce (exact
   `curl`/GraphQL), Gherkin ACs, and spec-gap proposals.
10. Return a concise summary to the orchestrator: counts by severity, the spec-gap count, the top
    risks, the plan path, and what was _not_ covered.

## Quality Guidelines

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
- Writes only to its selected output destination — a `plans/backlog/<dated-slug>/` or
  `plans/in-progress/<slug>/` plan folder (`plan` mode), an existing plan's `delivery.md` +
  `evidence/` named by `plan-path` (`delivery` mode), or `local-temp/<dated-slug>/` (`local-temp`
  mode) — plus the `plans/backlog/README.md` index when filing a backlog plan and scratch request
  scripts in `local-temp/`. Nowhere else.
- Never commits or pushes; the maintainer reviews the filed plan.
- Never records secrets, tokens, `Authorization` values, or real PII in any output (repo no-secrets
  rule) — redact them in every captured request/response.
