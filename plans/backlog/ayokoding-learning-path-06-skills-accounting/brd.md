# Business Requirements — Skills Path: Accounting

## Business Goal

Open a **second subject domain** on ayokoding.com. Today the entire 121-course library is software
engineering; this plan ships the first non-software-engineering path, `/en/learn/paths/skills/accounting`,
as a twenty-course **immediately-effective** arc for the reader who has to build or reason about
financial systems and has no accounting background.

The goal is not "teach accounting". Textbooks and certifications already do that, for accountants.
The goal is **accounting for people who build systems**: the reader leaves able to design a chart of
accounts as a schema, produce a balancing ledger, recognise the mistakes that still balance, and —
by the end — model murabaha, ijara, mudaraba and musharaka correctly rather than as loans with a
different label.

Two business consequences follow, and both are load-bearing:

1. **It unblocks ERP.** `ayokoding-learning-path-07-skills-erp` cannot deliver `record-to-report-systems`
   without a balanced ledger to post into. Accounting first is a dependency fact, not a preference.
2. **It is the platform's proof that the path machinery is subject-agnostic.** Everything built by
   plans 01–03 — the manifest schema, the variable-depth `pathId`, the renderer — was designed
   around one subject. This plan is the first evidence it generalises.

## Why accounting lands before ERP

The two skills subjects were split into two plans (A2 ruling, 2026-07-21). The ordering is forced by
the dependency direction, not chosen for convenience:

- **ERP depends on Accounting one-directionally. There is no cycle.** Nothing in the Accounting
  catalog needs any ERP course.
- The hard edge first bites at **ERP #7** (`record-to-report-systems`): subledger→GL posting is
  meaningless without a balanced ledger.
- ERP #1–4 and Accounting #1–3 are parallel-authorable; convergence is only required by ERP's stage 2. So plan 07 can start immediately and only stalls at its own #7 if this plan's Stage 1 has not
  landed.

Folding all 40 courses into one plan was rejected: it would have been the largest plan in the
programme, and it would have fused two corpora whose only coupling is a set of one-directional
prerequisite edges.

## Why twenty courses

**The count is curriculum judgment, not a sourced fact** [Judgment call]. It is labelled as such in
every document that states it, including the catalog table itself. What is defensible about it is
its **shape**, not its arithmetic:

- **Three courses to first payoff.** The single most expensive failure in a learning path is a reader
  who invests and gets nothing usable. Three courses buy a working, balancing ledger — a genuinely
  standalone-useful artefact.
- **Thirteen courses to conventional breadth.** The ramp slows deliberately after #3 because the
  domain's failures stop being loud. Compressing #4–#16 would produce readers who are confident and
  wrong, which is strictly worse than readers who are neither.
- **Four courses of Sharia depth.** This is the differentiating half of the corpus and the reason the
  path exists on this platform at all. It cannot be one course: it needs the standards landscape
  (#17), the contract modelling (#18), a conventional ledger to contrast against (#19), and the
  Sharia ledger itself (#20).

A shorter corpus would either drop the Sharia stage or compress the silent-failure stage. Neither is
acceptable. A longer one would dilute the immediately-effective promise.

## Business Impact

**Pain points addressed**

- **The platform teaches one subject.** A reader who needs a domain other than software engineering
  has nothing here. The path machinery exists but has never served a second subject.
- **The existing accounting material is the wrong artefact for the wrong reader.** `business/accounting.md`
  is a 34 KB single page for small-business owners. It has no syllabus spec, is not a course bundle,
  never touches schema or data modelling, and plan 01 is relocating it to `legacy/` precisely because
  it does not fit the new IA.
- **ERP is blocked with no path forward.** Plan 07 has a hard prerequisite that nothing in the repo
  can satisfy.
- **Sharia-compliant financial systems have no learning surface anywhere on the platform**, despite
  being the parent project's entire reason for existing. A builder asked to model a murabaha today
  has no place to learn why it is not a loan.

**Expected benefits** (qualitative reasoning; no fabricated metrics)

- **A second subject domain**, proving the shared library plus manifest model generalises beyond
  software engineering at the marginal cost of one manifest and one corpus.
- **ERP unblocked in three courses rather than twenty** — the stage-signal contract means plan 07
  gets its hard prerequisite at this plan's first authoring gate, not at its archival.
- **A defensible position on Sharia accounting.** Presenting three coexisting jurisdictional models —
  rather than one — is the difference between a resource practitioners can use across Bahrain,
  Indonesia and Malaysia, and one that is confidently wrong in two of the three.
- **A reusable ramp pattern.** The "dangerous by here" boundary is a skills-path concept with no
  careers-path equivalent. Establishing it here makes it available to every future skills subject.

## Affected Roles

Solo-maintainer repo — no sign-off ceremony. The maintainer wears:

- **Content strategist** — owns the ramp, its three boundaries, and what is deliberately omitted.
- **Domain researcher** — owns the verification debt: resolving OI-1 and OI-2 against primary
  sources before any standard number or doctrinal claim is written as fact.
- **Content author** — authors 20 syllabus specs and 20 course bodies via the ayokoding maker agents.
- **Frontend engineer** — authors one YAML manifest the `course-paths` feature loads and validates at
  build time.
- **Content reviewer** — validates the bodies and the landing via the ayokoding checkers.

Consuming agents: `apps-ayokoding-www-by-example-maker` and `apps-ayokoding-www-annotated-concept-maker`
(the two formats this corpus uses), their matching checkers and fixers,
`apps-ayokoding-www-general-maker` (landing prose), `apps-ayokoding-www-facts-checker`,
`apps-ayokoding-www-link-checker`, `web-researcher` (the verification debt and every external claim),
`apps-ayokoding-www-deployer`, and the three live-site testers `web-exploratory-tester`,
`web-usability-tester`, `web-design-tester` for the Rule-15 retest [Repo-grounded — each verified
present under `.claude/agents/`].

## Business-Level Success Metrics

Every metric is an **observable check**, not a projected number. Each is falsifiable in both
directions — the "before" value is stated so a vacuous pass is impossible.

- **One skills manifest published, at full composition** (observable): `manifests/skills/accounting.yaml`
  exists and its `courseOrder` holds exactly 20 IDs. Before Phase 2 the file does not exist at all;
  after Phase 2 it holds 3; after Phase 3, 16.
- **Twenty course bundles resolve** (observable): each of the 20 course IDs resolves to a directory
  under `content/en/learn/courses/`. Before Phase 2 all 20 are missing. **Asserted by ID, never by a
  global directory count** — plan 04 is authoring concurrently, so the total is a moving target (see
  [tech-docs DD-618](./tech-docs.md#design-decisions)).
- **The first 2-segment `pathId` resolves end-to-end** (observable): `/en/learn/paths/skills/accounting`
  renders its ordered course list, and `?path=skills/accounting` propagates through prev/next and the
  breadcrumb. Before this plan, the 2-segment shape exists only as a unit-test fixture in plan 02.
- **The ramp is visible to a reader** (observable): the landing states all three "dangerous by here"
  boundaries and what a reader can and cannot do at each, in prose a reader meets before the course
  list.
- **No prerequisite is walked that should be linked** (observable): `courseOrder` contains neither
  `sql-essentials` nor `backend-essentials`, while course #2's and #19's `_index.md` frontmatter
  declares them. Both halves are checked — the absence alone would also pass if the edge were simply
  forgotten.
- **The silent-failure requirement is met** (observable): every course from #4 onward carries an
  explicit "what still balances while being wrong" section in its `overview.md`. Before authoring,
  zero do.
- **Zero laundered verification claims** (observable): no `[Needs Verification]` item remains open at
  the Phase 4 gate, and no standard number or doctrinal claim appears in a syllabus spec or body
  without either a primary-source citation or an explicit marker.
- **Three jurisdictional models, not one** (observable): courses #17, #18 and #20 each name AAOIFI,
  PSAK Syariah **and** MFRS-plus-BNM, and none of them describes AAOIFI as "the" standard.
- **Three stage signals emitted** (observable): each of the three signals is recorded with all five
  fields and a real merged commit SHA, so plan 07 can consume them without asking.
- **No regressions** (observable): `ayokoding-www:build`, the affected test tiers,
  `specs:behavior:coverage`, heading-hierarchy, markdownlint, and link validation all pass.

## Business-Scope Non-Goals

- **Any ERP content.** The full ERP corpus, its manifest, and its landing belong to
  `ayokoding-learning-path-07-skills-erp`. This plan authors none of it and does not write into its
  manifest.
- **Any structural `_index.md` under `paths/`.** `paths/_index.md`, `paths/careers/_index.md`, the
  three arc indexes, and **`paths/skills/_index.md`** are all plan 01's (A3). This plan creates only
  its own path-landing bundle. The empty state those indexes render between plan 01 and this plan is
  plan 03's to design.
- **Re-authoring or editing any existing library course.** `sql-essentials` and `backend-essentials`
  are linked. Not forked, not re-walked, not extended with an accounting section.
- **Accountancy certification coverage.** This is not a CPA/ACCA/CA syllabus and does not claim
  equivalence with one. It is deliberately a systems-builder's slice.
- **Tax jurisdiction depth.** Course #14 covers payroll-and-tax _accounting essentials_ — the ledger
  mechanics — not any country's tax code.
- **Corporate finance.** Valuation and capital structure stay out; `business/corporate-finance.md`
  is adjacent prior art, not a source, and no course cites it.
- **An Indonesian mirror of the path.** `id/belajar/` holds zero courses and zero paths, so a
  manifest over it would compose nothing. This is a content-availability fact, not a code limitation
  — the navigation mechanism is locale-neutral.
- **A second skills arc.** Every skills path is `immediately-effective` (R8). Adding a
  `skills/<arc>/<subject>` grammar later must stay purely additive, which is why the manifest records
  `arc` even though the URL omits it — but no second arc is authored here.

## Business Risks and Mitigations

| Risk                                                                                                                                          | Mitigation                                                                                                                                                                                                                                                                   |
| --------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **A course teaches a plausible, silently wrong model** — the domain's characteristic failure, reproduced by the material meant to prevent it. | Every course from #4 onward carries a mandatory "what still balances while being wrong" section, checked by a grep-verifiable acceptance clause at its authoring step; the ramp deliberately slows after #3 rather than accelerating.                                        |
| **AAOIFI is presented as "the" Sharia accounting standard.**                                                                                  | Three jurisdictional models are a stated content invariant, asserted per course at #17, #18 and #20, and re-asserted at the Phase 5 gate. Malaysia's absence from AAOIFI's mandatory-adoption list is stated explicitly rather than left to inference.                       |
| **An `[Unverified]` research claim is restated as fact in a syllabus spec or body.**                                                          | Phase 4 is a dedicated verification-debt phase gating the entire Sharia stage; every external claim carries a confidence marker; `apps-ayokoding-www-facts-checker` runs on every body; the Phase 4 gate asserts zero open `[Needs Verification]` items in this plan folder. |
| **Indonesian PSAK standard numbers are published wrong** (the "PSAK 59 / SIFAS 101-109" vs "PSAK 101-110" conflict).                          | OI-1 names IAI's published list as the primary source and blocks course #17's authoring until resolved. If it cannot be resolved, the course scopes around the numbering rather than guessing — the escape is written into the resolution step.                              |
| **The manifest ships truncated at 3 courses and is never grown**, passing integrity forever.                                                  | Every publication and growth step carries a falsifiable before/after deferred-ID check; the terminal gate asserts all 20 IDs present; the three stage signals make truncation visible to plan 07 as well.                                                                    |
| **Scope creep into ERP.** The two domains share vocabulary, so an accounting course drifts into ERP module design.                            | Each affected body states its scope boundary explicitly against the ERP course that owns the adjacent material; the boundary statement is a grep-checkable acceptance clause, not a review opinion.                                                                          |
| **The linked prerequisites get walked**, quietly turning a 20-course accounting path into a software-engineering path.                        | The manifest is asserted to contain neither `sql-essentials` nor `backend-essentials`, **and** the corresponding `_index.md` frontmatter is asserted to declare them — so neither "walked" nor "forgotten" passes.                                                           |
| **Plan 02's doc-level prerequisite-omission rule reads as forbidding this plan's manifest.**                                                  | Recorded as OI-4 and routed to plan 02's owner in Phase 0 rather than silently diverged from or unilaterally edited. The implemented `checkPrerequisiteConsistency` already permits it; only the prose rule needs a carve-out sentence.                                      |
| **This plan is scheduled behind plan 04 unnecessarily**, delaying ERP by the whole 90-body authoring run.                                     | The no-edge finding is verified, not assumed: both linked prerequisites are among plan 01's 37 re-homed bundles, checked as a Phase 0 start precondition.                                                                                                                    |
| **The two skills plans collide** on a shared manifest directory or the skills structural index.                                               | Ownership is scoped to exactly one file per plan (`manifests/skills/accounting.yaml` here), and neither skills plan creates any `_index.md` — A3 assigns every structural index to plan 01. The Phase 6 ownership check asserts this plan's directory footprint exactly.     |
| **The landing reads as a table of contents** rather than an immediately-effective promise.                                                    | The landing content contract requires the arc statement and the three ramp boundaries **before** the course list, with the course list rendered from the manifest rather than hand-listed; verified by the Rule-15 usability tester against the live page.                   |
