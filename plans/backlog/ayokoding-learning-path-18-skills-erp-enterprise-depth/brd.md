# Business Requirements Document — Skills Path: ERP Enterprise Depth (Stage B + Stage C)

## Business Goal

Complete the domain-depth ERP learning surface `ayokoding-learning-path-17-skills-erp-foundations`
began: grow both `skills/conventional-erp` and `skills/sharia-erp` from their 15-course Stage A state
to their terminal 27/30-course state, giving a reader the full subledger-to-GL architecture, the hard
inventory/planning/quality parts, enterprise-scale concerns (multi-entity, payroll, security,
analytics), and — for `sharia-erp` only — jurisdiction-plural Sharia-compliant design, without ever
teaching installation, vendor selection, or system construction.

## Business Context

This is the second of a two-plan split of the retired the superseded ERP-programme draft design.
`ayokoding-learning-path-17-skills-erp-foundations` (Stage A, no accounting precondition) already
ships independently; this plan carries the two remaining authoring stages that genuinely wait on the
accounting programme, which was itself split into three new plans
(`ayokoding-learning-path-14/15/16-skills-accounting-*`) by a sibling agent.

## Business Impact

- **Completes both ERP products end to end.** `conventional-erp` reaches its terminal 27 ids and
  `sharia-erp` its terminal 30, matching the full domain-depth promise the retired source plan made.
- **The accounting-gate re-pointing removes a stale dependency.** The retired source plan's
  `ACCT_GATE_B`/`ACCT_GATE_C` checks named the single, now-superseded
  the superseded accounting-programme draft; this plan re-points them to the correct two of the
  three new accounting-split plans (15 for `ACCT_GATE_B`, 16 for `ACCT_GATE_C`), each transitively
  covering its own predecessor, so no redundant historical source context edge is declared.
- **Cross-domain reinforcement**: this plan's 15 courses declare 7 direct edges into the
  accounting-split corpus and 7 edges into the existing software-engineering library
  (`security-essentials`, `data-engineering`, `analytics-and-experimentation`,
  `advanced-sql-and-query-performance`), plus 7 cross-plan edges by specific id into plan 17's Stage A
  corpus.
- **Shared-corpus efficiency preserved**: the 27 shared course bodies (15 from plan 17, 12 from this
  plan) serve both products; `A11`'s reference-by-id-never-duplicate architecture holds across the
  two-plan split exactly as it held within the retired single plan.

## Affected Roles

- **Content authors** (AI agents in the maker-checker-fixer pipeline) — author 15 course bodies and
  15 syllabus files against the already-settled 30-course catalog.
- **Site readers** pursuing full ERP domain literacy — see [prd.md](./prd.md#personas).
- **`ayokoding-learning-path-17-skills-erp-foundations`** — the predecessor plan; this plan is a
  **read-only consumer** of its syllabus corpus (never an editor) and inherits explicit edit rights
  over the eight files plan 17 authored fresh (both manifests, both unit tests, both landings, the
  Gherkin feature file, and its step-definition file) to grow them further.
- **`ayokoding-learning-path-15-skills-accounting-enterprise-reporting`** and
  **`ayokoding-learning-path-16-skills-accounting-sharia-extension`** — the two accounting-split plans
  this plan's Stage B and Stage C respectively historical source context gate on.
- **`ayokoding-learning-path-03-navigation-ui`** — supplies every rendered component this plan's
  content appears on; this plan supplies content specifications only.

## Business-Scope Non-Goals

- **Any Stage A course content or Stage A syllabus file.** Those 15 courses and syllabi belong entirely
  to `ayokoding-learning-path-17-skills-erp-foundations`, which this plan only reads by relative link.
- **Any accounting content.** The full accounting corpus, its manifests, and its landings belong to
  the three accounting-split plans; this plan only consumes them via the two staged historical source context gates.
- **Any UI component, route, or design asset.**
- **Any structural `_index.md` under `paths/`.**
- **Building, installing, configuring, or standing up an ERP system of any kind (A6).**
- **Evaluating, selecting, or endorsing any commercial or open-source ERP vendor (A7).**
- **An Indonesian mirror of either path, or a second skills arc.**
- **Reproducing any standard's text, proprietary schema, or copyleft reference-implementation code
  (A8)** — including, for Stage C specifically, any AAOIFI FAS clause text or PSAK ratification date
  beyond the verified series number.

## Risks

| Risk                                                                                                                     | Likelihood | Impact | Mitigation                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------------ | ---------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| The accounting-split plans (14/15/16) rename or restructure one of the seven `ACCT_GATE_*` ids before this plan executes | Medium     | Medium | Mechanical `test -d` gates fail safely (wait, not silent wrong-authoring); coordination risk flagged explicitly in tech-docs.md, re-verified before Phase 2/3      |
| A course reproduces a copyrighted standard's text, a proprietary system's schema, or copyleft code                       | Medium     | High   | Eleven safe-authoring rules (A8), Sharia-specific AAOIFI addendum; `apps-ayokoding-www-facts-checker` per-course review; Phase 5 grep-checkable acceptance clauses |
| A jurisdictional claim in the Sharia-exclusive courses (28-30) is stated as settled fact while still `[Unverified]`      | Medium     | Medium | A4 verification-status carry-forward; explicit Phase 3.0 re-verification step gates Stage C authoring                                                              |
| This plan edits plan 17's manifests/landings incorrectly, corrupting the already-published 15-id state                   | Low        | High   | Deferral-check assertions (both directions) at every growth step, re-run against plan 17's exact pre-growth commit                                                 |
| A vendor name appears in a course title, path segment, or product name (trademark exposure)                              | Low        | Medium | Nominative-use rule; Phase 5 grep clause scanning every id for vendor-name substrings                                                                              |

## Success Criteria

- `conventional-erp` renders 27 courses and ends at Dangerous 3; `sharia-erp` renders 30 courses and
  ends at Dangerous 4 — both live at `ayokoding.com`.
- Zero CRITICAL/HIGH findings from this plan's own final three-tester manual retest.
- All Phase 5 licensing/trademark acceptance clauses pass, including the Stage C AAOIFI addendum.
- `<CONVMAN>` is verified **unchanged** at 27 ids once Stage C grows only `<SHARMAN>` to 30
  (deferral-check both directions).
- No accounting file, careers manifest, component, design asset, structural `_index.md`, or plan-17
  Stage-A course body modified by this plan (ownership-invariant check, verified at every phase gate).
