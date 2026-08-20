# Output Modes: `delivery` and `local-tmp`, and Procedure Summary

## Mode `delivery` — fold findings into an existing plan's `delivery.md`

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

## Mode `local-tmp` — a throwaway findings file for direct fixing

Write a single `local-tmp/<YYYY-MM-DD>__<slug>/findings.md` carrying the full finding catalog plus
an `evidence/` subfolder beside it. Emit **no**
`README`/`brd`/`prd`/`spec-gaps`/`tech-docs`/`delivery`, and make **no** entry in
`plans/backlog/README.md`. The folder is gitignored and ephemeral. Return the same severity-count
summary plus the `local-tmp/` path to the orchestrator.

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
