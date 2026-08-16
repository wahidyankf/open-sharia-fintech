# Output Modes `delivery`, `local-tmp`, and Procedure Summary

## Mode `delivery` — fold findings into an existing plan's `delivery.md`

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

### Mode `local-tmp` — a throwaway findings file for direct fixing

Selected with `output-mode: local-tmp`. Write a single `local-tmp/<YYYY-MM-DD>__<slug>/findings.md`
carrying the full finding catalog (same anatomy, severity/priority, steps-to-reproduce) plus an
`evidence/` subfolder beside it for cited captures. Emit **no**
`README`/`brd`/`prd`/`spec-gaps`/`tech-docs`/`delivery`, and make **no** entry in
`plans/backlog/README.md`. The folder is gitignored and ephemeral — the calling session reads
`findings.md` and applies the fixes directly in the same run. Return the same severity-count summary
plus the `local-tmp/` path to the orchestrator.

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
