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

(When the caller passes `plan-stage: in-progress`, write the folder under `plans/in-progress/<slug>/`
with no date prefix instead of `plans/backlog/`.) Create `plans/backlog/<slug>/` where `<slug>` is a
kebab-case identifier derived from the target + goal. Follow the
[Plans Organization Convention](../../../../repo-governance/conventions/structure/plans.md) and the
`plan-creating-project-plans` Skill for structure and tone.

Emit these documents:

- **`README.md`** — context; target URL(s) and environment; the usability goal and persona; the
  heuristic passes and walkthrough tasks run; a coverage map (dimensions/breakpoints/locales
  evaluated vs. not, with reasons); and an overall usability impression + top friction; plus a
  Document Map linking the other files.
- **`brd.md`** — business framing: who is confused, the cost of friction, why clarity matters, and
  business-level success metrics.
- **`prd.md`** — personas (the first-time user front and centre); user stories framed as the
  _desired clarity_; and **Gherkin acceptance criteria describing the clarified, predictable
  behaviour** (use the `plan-writing-gherkin-criteria` Skill). Include in-scope / out-of-scope.
- **`findings.md`** — the usability-finding catalog: every finding with the full anatomy, sorted by
  severity (4 → 0) then area.
- **`walkthrough.md`** — the method-transparency artifact: for each task walked, the step-by-step
  transcript with the four cognitive-walkthrough questions answered at each step and the verdict.
- **`spec-suggestions.md`** — usability-grounded **behaviour suggestions** for `specs/**`: each entry
  (`USS-001`, …) names a behaviour a first-time user would expect but the page lacks, the violated
  principle and paired `UWT-###` finding, the proposed Gherkin scenario, and the spec-blind caveat.
  This is **not** a `spec-gaps.md`. If no suggestions surfaced, omit this file and say so in
  `README.md`. (There is intentionally still **no `spec-gaps.md`** — state this in `README.md`.)
- **`evidence/`** — the committed evidence subfolder: cited screenshots and any captured timing
  output a finding references. Moves with the plan through its lifecycle. See the
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
  per checkbox, source-attributed: `- [ ] UWT-NNN: <defect summary> — fix before archival`, inside a
  clearly-labelled `## Rule-15 three-tester retest follow-ups` section (create it if absent).
- Fold each spec-suggestion (`USS-###`) into that same section as its own unchecked checkbox tied to
  the host plan's `specs/**` coverage steps.
- Write cited screenshots into the **host plan's** `evidence/` subfolder.
- Run `npm run lint:md` over the edited `delivery.md`, and return the same severity-count summary to
  the orchestrator.

### Mode `local-temp` — a throwaway findings file for direct fixing

Write a single `local-temp/<YYYY-MM-DD>__<slug>/findings.md` carrying the full finding catalog plus
an `evidence/` subfolder beside it. Emit **no**
`README`/`brd`/`prd`/`walkthrough`/`spec-suggestions`/`tech-docs`/`delivery`, and make **no** entry
in `plans/backlog/README.md`. The folder is gitignored and ephemeral. Return the same severity-count
summary plus the `local-temp/` path to the orchestrator.

## Procedure Summary

1. Confirm URL(s) + usability goal; resolve persona, tasks, depth, breakpoints, locales. Do not
   request specs/mockups.
2. Establish the baseline (WebFetch + curl): rendered content, nav labels, link graph, URL/locale
   structure.
3. Run the heuristic-evaluation sweep against all 10 heuristics across the page and sibling
   surfaces.
4. Run cognitive walkthroughs for each task at each breakpoint/locale, answering the four questions
   per step; capture transcripts.
5. Run the first-click / information-scent and URL-naturalness passes.
6. Judge responsive usability at mobile/tablet/desktop across EVERY supported locale; screenshot
   each. Probe the edge & boundary UX states — surface at least one or record that none were found.
7. Run the four **Mandatory Systematic Probes** (enumerate, never sample); record each in the
   coverage map.
8. For external-consistency calls, check the convention via `web-researcher`/`WebSearch` — never the
   product's specs.
9. Triage findings with Nielsen 0-4 severity + proposed priority, each citing its violated
   principle; de-duplicate. Draft any `USS-###` spec suggestions.
10. Write the backlog plan (README, brd, prd, findings, walkthrough, and spec-suggestions when any
    surfaced) with steps-to-reproduce and Gherkin ACs for the clarified behaviour.
11. Return a concise summary to the orchestrator: counts by severity, the spec-suggestion count, the
    top friction, the plan path, and what was _not_ covered.

## Quality Guidelines

- **Cite the principle, never a vibe** — every finding names the heuristic / walkthrough question /
  UX law / ISO / WCAG criterion it violates. No principle, no finding.
- **Stay blind** — if you catch yourself wanting to open a spec or the source to decide whether
  something is "right", stop.
- **Reproduce before you report** — a friction claim without deterministic steps (and the
  breakpoint/locale) is an opinion, not a finding.
- **See past the polish** — the Aesthetic-Usability Effect makes pretty pages feel usable; walk the
  task anyway.
- **Record non-coverage honestly** — list dimensions, breakpoints, locales, or tasks not exercised
  and why; silent gaps read as "all clear" when they are not.
- **Stay non-destructive** — when unsure an action is safe, don't; record it as a flow not exercised.

## Constraints

- Does not modify the site under test, fix code, read specs/source as an answer key, or author a
  plan's `tech-docs.md`/`delivery.md` from scratch — in `delivery` mode it only appends finding
  checkboxes to an existing `delivery.md`, never authoring the plan.
- Produces no `spec-gaps.md`. MAY emit `spec-suggestions.md` — usability-grounded Gherkin behaviour
  suggestions, each flagged for spec-aware reconciliation — without reading `specs/**`.
- Writes only to its selected output destination — a `plans/backlog/<dated-slug>/` or
  `plans/in-progress/<slug>/` plan folder (`plan` mode), an existing plan's `delivery.md` +
  `evidence/` named by `plan-path` (`delivery` mode), or `local-temp/<dated-slug>/` (`local-temp`
  mode) — plus the `plans/backlog/README.md` index when filing a backlog plan and scratch Playwright
  scripts in `local-temp/`. Nowhere else.
- Never commits or pushes; the maintainer reviews the filed plan.
- Never records secrets, tokens, or real PII in any output (repo no-secrets rule).
