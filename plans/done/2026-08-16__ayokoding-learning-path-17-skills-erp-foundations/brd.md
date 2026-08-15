# Business Requirements Document — Skills Path: ERP Foundations (Stage A)

## Business Goal

Give `ayokoding.com` readers the first deployable slice of a domain-depth ERP learning surface —
enough, at this plan's own 15-course boundary, to read and reason about how a real ERP structures
documents, postings, and account determination — without the site ever teaching installation, vendor
selection, or system construction, and without exposing the platform to copyright or trademark risk
from the open-source projects and standards bodies the domain touches.

## Business Context

`ayokoding.com`'s `skills/` category currently ships zero ERP content. This plan is the first of a
two-plan split of the retired the superseded ERP-programme draft design: it authors Stage A (15
of 30 courses) and publishes both `skills/conventional-erp` and `skills/sharia-erp` at 15 ids each.
The successor plan,
[`ayokoding-learning-path-18-skills-erp-enterprise-depth`](../../backlog/ayokoding-learning-path-18-skills-erp-enterprise-depth/brd.md),
grows both manifests to their terminal 27/30-course state. Splitting the retired plan lets Stage A —
which needs nothing from any accounting plan — ship independently rather than wait on Stage B/C's
accounting gates.

## Business Impact

- **A real, live, deployable checkpoint** — not a placeholder. Both `skills/conventional-erp` and
  `skills/sharia-erp` go live at `ayokoding.com` with 15 real courses each, reaching the Dangerous 1
  boundary, the moment this plan's final phase merges and deploys.
- **Unblocks the successor plan's Stage B authoring immediately** — because this plan authors course
  17 (`erp-bom-and-routing-architecture`) despite its late content-stage position, three Stage B
  courses in the successor plan can start authoring the moment this plan merges, with no idle wait.
- **Zero accounting coupling** — this plan carries no historical source context edge to any accounting plan, so it
  proceeds fully concurrently with the accounting programme's own three-plan split
  (`ayokoding-learning-path-14/15/16-skills-accounting-*`).
- **Cross-domain reinforcement**: this plan's 15 courses declare prerequisite edges into 6
  software-engineering courses — `sql-essentials`, `networking-essentials`, `backend-essentials`, and
  `api-design` (already published), plus `domain-driven-design` and `event-driven-architecture` (not
  yet published; both are pending authoring targets of
  `ayokoding-learning-path-06-course-authoring-architecture-and-ai-harness`,
  which this plan therefore adds as a repository baseline context precondition — see
  [tech-docs.md §The prerequisite graph](./tech-docs.md#the-prerequisite-graph--this-plans-edges-only))
  — giving those courses a new downstream audience.

## Affected Roles

- **Content authors** (AI agents in the maker-checker-fixer pipeline) — author 15 course bodies and
  15 syllabus files against the already-settled 30-course catalog and prerequisite graph.
- **Site readers** pursuing early ERP domain literacy — see [prd.md](./prd.md#personas).
- **`ayokoding-learning-path-18-skills-erp-enterprise-depth`** — the direct successor; historical source context this
  plan for its own Phase 0 start precondition, and a **consumer** (never an editor) of this plan's
  syllabus corpus for the cross-plan prerequisite edges it must cite by id (course 13→6,7; 14→6;
  18→17; 21→12,17; 24→3; 26→3; 29→10,11).
- **`ayokoding-learning-path-03-navigation-ui`** — supplies every rendered component this plan's
  content appears on; this plan supplies content specifications only.
- **`vercel-function-cost-reduction`** — historical repository context for the rendering posture.
  This plan records current rendered-route behavior; it does not make that historical plan an
  additional start or delivery gate.

## Business-Scope Non-Goals

- **Any Stage B or Stage C course content.** Courses `#13-16, 18-21, 24-30` belong entirely to
  `ayokoding-learning-path-18-skills-erp-enterprise-depth`.
- **Any accounting content.** The full accounting corpus, its manifests, and its landings belong to
  the three accounting-split plans; this plan has no edge to any of them.
- **Any UI component, route, or design asset.** Both path landings are rendered by
  `ayokoding-learning-path-03-navigation-ui`; this plan supplies content specifications only.
- **Any structural `_index.md` under `paths/`** — owned by `ayokoding-learning-path-01-url-restructure`
  (A3).
- **Building, installing, configuring, or standing up an ERP system of any kind (A6).**
- **Evaluating, selecting, or endorsing any commercial or open-source ERP vendor (A7).**
- **Growing either manifest past 15 ids, or updating a landing's boundary past Dangerous 1.** That is
  the successor plan's entire job.
- **Reproducing any standard's text, proprietary schema, or copyleft reference-implementation code
  (A8).**

## Risks

| Risk                                                                                                                      | Likelihood | Impact | Mitigation                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------------- | ---------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| A course reproduces a copyrighted standard's text, a proprietary system's schema, or copyleft code                        | Medium     | High   | Eleven safe-authoring rules (A8); `apps-ayokoding-www-facts-checker` per-course review; Phase 4 grep-checkable acceptance clauses                  |
| A vendor name appears in a course title, path segment, or product name (trademark exposure)                               | Low        | Medium | Nominative-use rule; Phase 4 grep clause scanning every id for vendor-name substrings                                                              |
| The two new static landing pages reintroduce the dynamic-rendering regression `vercel-function-cost-reduction` just fixed | Low        | High   | a repository-baseline check plus a build-time prerender check at this plan's own Phase 0 and Phase 6 gates                                         |
| The successor plan cannot cite this plan's syllabus corpus correctly (custody drift)                                      | Low        | Medium | This plan's `syllabus/README.md` names itself `**Custodian**`; the successor plan echoes `custodied-by:` under its own `## Corpus Custody` heading |
| A syllabus's vague module title makes the corpus unverifiable                                                             | Low        | Low    | Module-title specificity rule enforced at authoring time; Phase 1.2a confirmation pass surfaces vagueness                                          |

## Success Criteria

- Both path landings live at `/en/learn/paths/skills/conventional-erp` and
  `/en/learn/paths/skills/sharia-erp`, each rendering exactly 15 courses and the Dangerous 1 boundary.
- Zero CRITICAL/HIGH findings from this plan's own Phase 5 three-tester manual retest.
- All Phase 4 licensing/trademark acceptance clauses pass.
- No accounting file, careers manifest, component, design asset, structural `_index.md`, or Stage B/C
  course body modified by this plan (ownership-invariant check, verified at every phase gate).
