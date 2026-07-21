# Business Requirements — Skills Path: Enterprise Resource Planning

## Business Goal

Turn a subject the repo teaches **nothing** about today into a usable product: a single
`skills/enterprise-resource-planning` path that takes a software engineer from zero ERP knowledge to
integrating, extending, and eventually building ERP systems — including a Sharia-compliant one.

The path is the **immediately-effective** arc, always (R8): get up and running and become dangerous as
fast as possible, then go deeper and deeper on solid ground. It ships **usable before it ships
complete**, at the research's first "dangerous by here" boundary, and deepens from there.

This is one of two products in the new `skills/` category. Its sibling,
`ayokoding-learning-path-06-skills-accounting`, ships the accounting half. Together they are the
first non-software-engineering subject domain the library has ever carried.

## Why ERP is worth a path at all

ERP is where most enterprise software engineers actually meet the business, and it is the largest
blind spot in the existing 121-course catalog [Repo-grounded — zero ERP material anywhere in the
repo]. The catalog teaches how to build systems; it teaches nothing about the system that already
runs the company the reader is building for.

The concrete pain that creates:

- **An engineer integrating against an ERP with no ERP model does damage that looks like success.**
  The API returns 200, the screen renders, and the ledger is wrong — orphaned purchase orders,
  double-counted inventory, GL entries that never reconcile. ERP shares accounting's characteristic
  **silent failure** class, which is precisely why it needs teaching rather than improvising.
- **"ERP" is treated as a vendor question rather than a data-model question.** Readers pick a platform
  before they can describe master versus transactional data, then discover the mismatch after the
  migration.
- **Sharia-compliant ERP has no coherent engineering account anywhere.** The repo's own vision is
  Shariah-compliant enterprise systems, and there is currently no course that explains how to design
  one — or, critically, that there is **no single Sharia accounting standard** to hardcode against.

## Why one manifest, not a curriculum fork

The manifest model the careers category proved out applies unchanged here [Judgment call]:

- **A path is a lightweight ordered list of course ids** — cheap to author, cheap to reorder, and
  impossible to fork a body through.
- **Cross-domain reuse is free.** The eight existing software-engineering courses the ERP corpus
  depends on are **linked, never re-walked**; a fix to `api-design` benefits the ERP path
  automatically.
- **The accounting coupling stays a set of edges, not a merge.** Because ERP references accounting
  courses by stable id, the two corpora can be authored by two plans, on two schedules, without
  either copying the other's material.
- **Growth is additive.** The manifest is published at 10 course ids and grown to 15, 18, and 20 as
  waves land. No body is ever touched twice.

## Why this is a separate plan from accounting

One plan carrying all 40 skills courses was considered and rejected (A2). It would have been the
largest plan in the programme and would have fused two corpora whose only coupling is a set of
one-directional prerequisite edges.

The split is cheap precisely because the coupling is acyclic:

- **Nothing in accounting needs ERP**, so plan 06 never waits on this plan.
- **Ten of the twenty ERP courses need nothing from accounting**, so this plan does not wait on plan
  06 either — for half its corpus.
- The remaining coupling is four named wave gates, each a one-line `test -d` check against a specific
  accounting course bundle.

The alternative — declaring this plan simply "blocked by 06" — would idle ten authorable courses for
the whole duration of a twenty-course sibling plan, in a repo whose entire delivery model exists to
maximise parallelism. That cost is real and avoidable.

## Business Impact

**Pain points addressed**

- The library has no enterprise-systems literacy at all, so a reader working in an ERP-shaped company
  gets no help from it.
- Engineers integrating with ERPs learn by breaking production data, because the failure mode is
  silent and the feedback loop is a quarter-end close.
- The repo's Sharia-compliant-enterprise vision has no engineering curriculum behind it on the
  systems side.
- The `skills/` URL category exists structurally but would render empty without a populated path
  (amendment A3 makes that empty state real and user-visible between plan 01 and this plan).

**Expected benefits** (qualitative reasoning; no fabricated metrics)

- **A reader becomes genuinely useful after four courses**, not after twenty — the immediately-effective
  promise made concrete and checkable at a named boundary.
- **The category's second product at marginal cost**: one manifest, one landing, one corpus, over the
  same rendering and schema layers four careers paths already use.
- **A jurisdiction-aware account of Sharia-compliant ERP design** — the first anywhere in the repo,
  and correct by construction about the three coexisting standards models rather than presenting one
  as canonical.
- **A checkable smoothness guarantee**: prerequisite-consistency turns "does this ramp read smoothly?"
  from judgment into a machine-verified invariant re-run at every gate.

## Affected Roles

Solo-maintainer repo — no sign-off ceremony. The maintainer wears:

- **Content strategist** — owns the ramp, the curation, and the runway justification.
- **Domain researcher** — closes the A4 verification gaps before any `[Unverified]` claim is written
  as fact.
- **Content author** (via the ayokoding maker agents) — writes the 20 bodies and the landing.
- **Frontend engineer** — authors the single YAML manifest the `course-paths` feature loads and
  validates at build time.
- **Content reviewer** (via the ayokoding checker agents) — validates bodies, facts, and links.

Consuming agents: `apps-ayokoding-www-by-example-maker` and
`apps-ayokoding-www-annotated-concept-maker` (course bodies), `apps-ayokoding-www-general-maker`
(landing + manifest), `web-researcher` (the A4 re-verification pass),
`apps-ayokoding-www-facts-checker`, `apps-ayokoding-www-link-checker`,
`apps-ayokoding-www-deployer`, and the three live-site testers `web-exploratory-tester`,
`web-usability-tester`, `web-design-tester` for the Rule-15 retest [Repo-grounded — each verified
present under `.claude/agents/`].

## Business-Level Success Metrics

Every metric below is an **observable check**, not a projected number.

- **The path is live and standalone-useful before the sibling corpus finishes** (observable): the
  manifest is published with 10 course ids and the landing renders while
  `ayokoding-learning-path-06-skills-accounting` is still in flight. Falsifiable both ways — before
  Phase 2 no manifest file exists at all.
- **Ten courses provably need nothing from accounting** (observable): every Wave-A course's declared
  prerequisites resolve entirely within the ERP corpus plus the existing software-engineering library;
  no Wave-A body names an accounting course id.
- **The hard edge is honoured, not assumed away** (observable): `record-to-report-systems` is not
  authored until `financial-statements-and-close-cycle` resolves as a course bundle on `origin/main`.
- **Each ramp boundary is a real gate** (observable): boundary 1 closes with 10 ids in `courseOrder`,
  boundary 2 with 15, and boundary 3 with 20 — each asserted with a count that returns a different
  value before and after.
- **No manifest ships permanently truncated** (observable): every deferred course id carries a
  falsifiable before/after check written at publication time; the terminal gate asserts all 20.
- **Zero body duplication** (observable): the 8 existing software-engineering prerequisites and the 8
  accounting prerequisites are **linked** from the landing, never copied into `courseOrder`; the
  no-forked-body check reports zero duplicated bodies.
- **Scope boundaries are stated, not hoped for** (observable): the three boundary-risk bodies each name
  their neighbouring existing course explicitly in their own `overview.md`.
- **No `[Unverified]` claim is restated as fact** (observable): every fast-moving claim — ERP
  integration surfaces, analyst positioning, platform version pins — sits in a dated accuracy-note
  sidebar or carries its marker; the facts checker reports zero CRITICAL/HIGH findings.
- **Sharia design is jurisdiction-plural** (observable): the `sharia-compliant-erp-design` body names
  all three models (AAOIFI, PSAK Syariah, MFRS + BNM SGP 2019) and presents none as "the" standard.
- **No regressions** (observable): `npx nx run ayokoding-www:build`, the affected test tiers,
  `specs:behavior:coverage`, heading-hierarchy, markdownlint, and link validation all pass.

## Business-Scope Non-Goals

- **Authoring any accounting course, spec, manifest, or landing.** Owned end-to-end by
  `ayokoding-learning-path-06-skills-accounting`. This plan reads accounting course ids to declare
  prerequisites and never writes one.
- **Creating any structural `_index.md`** under `paths/` — owned by
  `ayokoding-learning-path-01-url-restructure` (A3). This plan populates its own card only.
- **Creating any design asset.** Mockups, HTML sources, and PNG renders are owned by
  `ayokoding-learning-path-03-navigation-ui`. This plan states what the landing must convey and ships
  no `assets/` folder.
- **Building or changing any rendering component, route, or schema.** Owned by plans 02 and 03.
- **Re-authoring or restructuring any of the 14 existing library courses** the corpus depends on.
  Link, do not walk.
- **Vendor certification content.** The corpus teaches ERP as an engineering domain, never as
  preparation for a specific vendor's certification exam.
- **A second skills arc.** Skills paths are always `immediately-effective` (R8); adding a
  `skills/<arc>/<subject>` grammar later stays purely additive and is not attempted here.
- **An Indonesian mirror** — deferred; `id/belajar/` holds zero courses and zero paths, so a manifest
  over it would compose nothing.
- **Folding the ERP corpus into the 127-course careers catalog figure.** 127 remains the
  careers/software-engineering total (R5); ERP's 20 are additional.

## Business Risks and Mitigations

| Risk                                                                                                          | Mitigation                                                                                                                                                                                                                               |
| ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The plan is treated as wholly blocked by plan 06, idling ten authorable courses.                              | The dependency is encoded **per wave**, not per plan: Wave A declares zero accounting preconditions, and the delivery checklist's Phase-2 gate contains no accounting check at all. A reviewer can see the absence directly.             |
| The hard edge at ERP #7 is assumed away and `record-to-report-systems` is authored against a guess at the GL. | Wave B cannot start until `test -d <COURSES>financial-statements-and-close-cycle` exits 0. The check is falsifiable both ways — it exits non-zero today.                                                                                 |
| An `[Unverified]` research claim is quietly promoted to fact in a course body.                                | Phase 1 is a dedicated verification pass that carries every marker into the spec files with a named resolution step; fast-moving claims go into dated accuracy-note sidebars, and `apps-ayokoding-www-facts-checker` runs on every body. |
| A course presents AAOIFI as "the" Sharia accounting standard.                                                 | DD-12 makes jurisdictional pluggability the engineering lesson of `sharia-compliant-erp-design`; the body must name all three models, and the acceptance clause greps for all three.                                                     |
| A new ERP course re-teaches an existing library course, splitting the canonical explanation across two homes. | Three boundary risks are named up front with a stated boundary each, and each affected body's `overview.md` must name its neighbour — a grep-checkable acceptance criterion, not a review-time opinion.                                  |
| The manifest ships truncated at 10 ids and is never grown.                                                    | Every deferred id carries a falsifiable before/after check written at publication time; Phases 3-5 are dedicated growth phases; the archival gate asserts all 20 ids.                                                                    |
| Both skills plans edit the same skills category landing and collide.                                          | Each plan populates only **its own** card and asserts its own card's presence with a literal-string check rather than a total count, so a sibling card landing first or later never fails this plan's gate.                              |
| The longer runway to first payoff reads as padding and the landing loses readers before #4.                   | The runway justification is a **stated landing content requirement** handed to plan 03, not left to prose luck — and the ramp boundaries are surfaced on the landing so the reader knows exactly how far in usefulness starts.           |
| A capstone body's sample code depends on a live third-party ERP and breaks CI.                                | DD-14 forbids a live-network dependency in any code sample: the #4 and #10 capstones use a containerised or fixtured ERP, so the third-party API stays subject matter rather than a build dependency.                                    |
| Plan 03's landing design assumes the two skills landings are interchangeable.                                 | The tech-docs landing-content requirements state explicitly what differs between ERP and accounting — the three-course runway versus accounting's two — so plan 03 designs for the difference rather than discovering it.                |
| Cross-plan references break when a sibling plan archives ahead of this one.                                   | Sibling plans are referenced by **name in code spans, not links**, until both coexist; the archival phase re-runs a scoped link validation over this plan's own folder.                                                                  |
