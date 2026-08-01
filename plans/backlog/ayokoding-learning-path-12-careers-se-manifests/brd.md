# Business Requirements — Learning Path Manifests (software-engineer-role)

## Business Goal

Turn the shared **software-engineering** course library into **three usable `careers/` products** by
authoring, publishing, growing, and verifying the three ordered `software-engineer`-role path
manifests. (The fourth `careers/` product, `careers/immediately-effective/ai-engineer`, is the sibling
plan `ayokoding-learning-path-13-careers-ai-manifest`'s own deliverable — out of this plan's scope,
coupled to it only as described in [README §The plan-12 / plan-13 coupling](./README.md#the-plan-12--plan-13-coupling-non-circular-by-construction).)
The library is the investment; the manifests are what convert that single investment into
audience-fit reading arcs:

- a **`careers/interview-ready/software-engineer`** path — the **interview/job-prep-first** arc for an
  experienced engineer re-entering the market: interview prep FIRST → production-effective → deeper;
- a **`careers/immediately-effective/software-engineer`** path — the **immediately-effective**
  principle: set up the editor, learn one language end-to-end, **build a real app first**, then
  deepen;
- a **`careers/fundamentally-strong/software-engineer`** path — the **university-style,
  fundamentals-first** arc: CS foundations / theory first → deeper.

All three converge on the **same** software-engineering endpoint — only the **entry point**, the
**journey ordering**, and the **teaching emphasis** differ.

**This plan ships no course body and no rendering component.** It ships the composition layer: three
YAML manifests, three thin landing anchors, this plan's slice of the paths-hub card population, the
smoothness audits, and every growth of these three manifests as backfill content lands.

## Why this plan is its own deliverable, split out from a four-manifest predecessor

The plan this split replaces authored all four `careers/` manifests in one folder. Splitting it into
two plans rather than keeping one, or splitting it 2+2, is a structural call, not a stylistic one — see
[README §Why 3 + 1, not 2 + 2](./README.md#why-3--1-not-2--2) for the full reasoning. The short version:
three cross-manifest checks (no-forked-body, Band-9 growth, the ownership-boundary sweep) bind
specifically across the three software-engineer-role manifests and never touch the AI-engineer
manifest, so those three manifests are a coherent, separable unit of work; the AI-engineer manifest has
its own independent nine-course growth track and no dependency on this plan's three checks.

## Why manifests instead of curricula

The naive alternative — author three separate curricula — would triplicate the course corpus,
triple the maintenance surface, and let three trees drift out of sync [Judgment call]. The manifest
model avoids that entirely:

- **A path is a lightweight ordered list of course IDs** — cheap to author, cheap to change, and
  impossible to fork a body through.
- **A fix propagates for free.** Because every manifest references courses by stable ID, correcting a
  typo, updating a version, or improving an example in one canonical body benefits every referencing
  path at once.
- **The prerequisite DAG keeps every path honest.** Each manifest is a different valid entry point and
  topological ordering into one dependency graph, machine-checked at every phase gate.
- **Growth is additive.** As the seven course-authoring successor plans land their bands, each affected
  manifest grows in place; the arcs deepen without any body being touched twice.

## Business Impact

**Pain points addressed**

- The library exists but is unreadable as a journey: without a manifest, a reader lands on a flat
  catalog with no ordering, no entry point, and no signal about what to read first.
- An experienced re-entrant, a productive-fast builder, and a theory-first learner are all forced
  through the same order today, and none is optimally served.
- Without this plan, the upstream investment in URL restructure, schema, navigation UI, and authored
  course bodies has no user-visible product surface for three of the four `careers/` audiences.
- Without a single owner for these three manifests' mutation, backfill growth from seven separate
  course-authoring successor plans would either be skipped (leaving permanently truncated paths that
  look correct because integrity passes) or duplicated across plans that then drift.

**Expected benefits** (qualitative reasoning; no fabricated metrics)

- **Three audience-fit products from one content investment**, with no duplication and one maintenance
  surface.
- **A checkable smoothness guarantee**: prerequisite-consistency turns "does this order read smoothly?"
  from an ad-hoc judgment into a machine-verified invariant, re-run at every gate.
- **No silent truncation**: the growth phase closes every gap each smoke-test-scoped or Band-9-deferred
  manifest deliberately left open, and the terminal gates assert the full arcs.
- **A clean seam with the sibling AI-manifest plan**: because the three software-engineer manifests and
  the one AI-engineer manifest are separately owned, a defect or delay in one plan's growth cannot
  silently corrupt the other's manifest.

## Affected Roles

Solo-maintainer repo — no sign-off ceremony. The maintainer wears:

- **Content strategist** — owns each path's arc, its curation (what is omitted), and its framing.
- **Frontend engineer** — authors the YAML data files the `course-paths` feature loads and validates at
  build time.
- **Content author** (via `apps-ayokoding-www-general-maker`) — writes the three thin landing anchors
  and this plan's slice of the hub card copy.
- **Content reviewer** (via `apps-ayokoding-www-link-checker` and the facts checker) — validates the
  landings and their outbound canonical-page links.

Consuming agents: `apps-ayokoding-www-general-maker` (manifest + landing authoring), `web-researcher`
(smoothness-audit facts), `apps-ayokoding-www-link-checker`, `apps-ayokoding-www-deployer`, and the
three live-site testers `web-exploratory-tester`, `web-usability-tester`, `web-design-tester` for the
Rule-15 retest [Repo-grounded — each verified present under `.claude/agents/`].

## Business-Level Success Metrics

Every metric below is an **observable check**, not a projected number.

- **Three manifests published, zero body duplication** (observable): all three `courseOrder` lists
  reference courses **by ID**; the no-forked-body check reports zero duplicated bodies across all
  three. Falsifiable both ways: before Phase 1 no manifest file exists at all.
- **Prerequisite DAG consistency holds at every gate** (observable): `checkManifestIntegrity` +
  `checkPrerequisiteConsistency` exit 0 across every published manifest at every phase gate.
- **interview-ready MVP proves the architecture first, and unblocks the sibling plan** (observable):
  the interview-first path's landing, manifest, and path-aware nav are live in production, and its
  merge is the recorded precondition the sibling AI-manifest plan starts against.
- **immediately-effective is build-app-first** (observable): its manifest places editor/tooling → one
  language end-to-end → build a real app ahead of CS-fundamentals/DS&A/algorithms/systems depth.
- **fundamentally-strong is theory-first** (observable): its manifest places CS
  foundations/architecture/paradigms/DS&A ahead of build-at-scale courses.
- **No manifest ships permanently truncated** (observable): after the growth phase, `interview-ready`
  and `fundamentally-strong` carry all five Band-9 interview-technique courses as their trailing
  optional tail; `immediately-effective/software-engineer` deliberately never receives them (two-of-three,
  DD-41).
- **This plan's own catalog contribution resolves** (observable): every non-AI course body this plan's
  three manifests reference resolves under `apps/ayokoding-www/content/en/learn/courses/`.
- **The four-manifest, 127-course catalog resolves at this plan's final phase** (observable, needs the
  sibling plan fully merged): all four `careers/` manifests validate against the complete 127-course
  catalog, and the "a shared course names every path" affordance lists all four.
- **Progression smoothness verified per path** (observable): each manifest passes its own smoothness
  audit before archival.
- **No regressions** (observable): `npx nx run ayokoding-www:build`, the affected test tiers,
  `specs:behavior:coverage`, heading-hierarchy, markdownlint, and link validation all pass.

## Business-Scope Non-Goals

- **The `careers/immediately-effective/ai-engineer` manifest, its landing, and its hub card.** Owned
  entirely by `ayokoding-learning-path-13-careers-ai-manifest`.
- **Authoring or editing any course body.** Owned by the seven course-authoring successor plans. This
  plan reads bodies (to verify a `courseOrder` ID resolves) and never writes one.
- **Building or changing any rendering component.** `path-landing.tsx`, `path-card.tsx`,
  `path-rail.tsx`, `manifest-repository.ts`, and the `?path=` route wiring are owned by
  `ayokoding-learning-path-03-navigation-ui`.
- **Defining the `PathManifest` schema or the integrity gates.** Owned by
  `ayokoding-learning-path-02-schema-and-prerequisite-dag`.
- **Any URL, redirect, or IA change.** Owned by `ayokoding-learning-path-01-url-restructure`.
- **The `apps/ayokoding-www` root-layout/middleware rendering-mode work.** Owned by
  `vercel-function-cost-reduction`, treated here as a hard, already-merged precondition.
- **The `skills/` category's four manifests.** Owned end-to-end by the accounting/ERP split plans —
  disjoint category subtree, no shared file (see [README](./README.md#disjoint-subtree-confirmation)).
- **Adding an Indonesian mirror of the path content** — deferred; `id/belajar/` has zero courses and
  zero paths.
- **Path-level progress persistence, accounts, or bookmarking.**
- **Enumerating speculative course variants** — authored on demand only, by the course-authoring
  successor plans.
- **A fifth `careers/` path, or renumbering the four-path `careers/` composition.** Locked.

## Business Risks and Mitigations

| Risk                                                                                                  | Mitigation                                                                                                                                                                                                                                                                  |
| ----------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A manifest references a missing or renamed course ID.                                                 | `checkManifestIntegrity` verifies every `courseOrder` ID resolves to a bundle under `<COURSES>`; runs as a unit test and at every phase gate.                                                                                                                               |
| A manifest orders a course before its declared prerequisite, breaking the DAG.                        | `checkPrerequisiteConsistency` verifies every manifest is a valid topological entry; a violation fails the phase gate.                                                                                                                                                      |
| A manifest ships **narrowed** and is never grown.                                                     | Every smoke-test-scoped manifest carries a falsifiable before/after check. Phase 4 is a dedicated growth phase; the terminal gate asserts the full arcs.                                                                                                                    |
| Band-9 growth lands in the wrong manifest(s) — e.g., silently includes `immediately-effective`.       | The Phase 4.2 acceptance clause asserts the five-ID check returns **5** for `interview-ready` and `fundamentally-strong` **and returns 0** for `immediately-effective/software-engineer`, in the same step — a wrong-manifold append fails immediately in either direction. |
| Duplication creeps in — a path forks a body for its framing.                                          | Framing is limited to an optional intro/outro callout (DL-5); the no-forked-body check runs at every manifest gate.                                                                                                                                                         |
| A course-authoring successor plan edits a manifest, or this plan edits a body — the boundary erodes.  | The ownership invariant is stated in both this plan's and every course-authoring successor plan's own docs; this plan's Phase 5 gate greps its own manifest paths' git history scope.                                                                                       |
| The plan-12 / plan-13 coupling is misread as circular.                                                | The coupling is documented explicitly, with a sequence diagram, in both plans' READMEs, and the two edges are stated as distinct nodes (Phase 1 vs. the final phase) rather than a single bidirectional edge.                                                               |
| The four-manifest check runs before the sibling plan has actually merged, producing a false pass.     | Phase 8's start condition is a literal `gh pr list --search "ayokoding-learning-path-13-careers-ai-manifest" --state merged` check, falsifiable both ways, not an assumption from reading the delivery checklist alone.                                                     |
| The seven course-authoring successor plans' growth signals arrive out of the order this plan expects. | Phase 4's sub-phases are each gated on their own named source plan's merge, not on calendar order; a signal that arrives early is processed early, and the final arc-confirmation step re-verifies the complete composition regardless of arrival order.                    |
| Cross-plan `syllabus/` links break when the schema plan has already archived.                         | This plan's own pre-archival link-validation gate is scoped to its own folder and re-run at Phase 8.                                                                                                                                                                        |
