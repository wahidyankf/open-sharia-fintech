# Business Requirements — Learning Path Manifests

## Business Goal

Turn the shared course library into **four usable products** by authoring, publishing, growing, and
verifying the four ordered path manifests that compose it. The library is the investment; the
manifests are what convert that single investment into four audience-fit reading arcs, each with a
coherent, prerequisite-aware, path-aware journey:

- an **`interview-ready/software-engineer`** path — the **interview/job-prep-first** arc for an
  experienced engineer re-entering the market: interview prep FIRST → production-effective → deeper;
- an **`immediately-effective/software-engineer`** path — the **immediately-effective** principle:
  set up the editor, learn one language end-to-end, **build a real app first**, then deepen;
- a **`fundamentally-strong/software-engineer`** path — the **university-style, fundamentals-first**
  arc: CS foundations / theory first → deeper; and
- an **`immediately-effective/software-engineer-to-ai-engineer`** path — an already-working software
  engineer transitioning to AI engineering: assumes SWE competence (prerequisite SWE-fundamentals
  courses are **linked, not included**) and teaches **building** AI systems, fast because it assumes
  competence, not because it skips depth.

The three `software-engineer` paths converge on the **same** software-engineering endpoint — only the
**entry point**, the **journey ordering**, and the **teaching emphasis** differ. The fourth path
converges on a **distinct** AI-engineering endpoint: the library serves **more than one endpoint**,
one per role it serves. Convergence is a per-role property, not a library-wide axiom (see
[tech-docs.md DD-22](./tech-docs.md#design-decisions)).

**This plan ships no course body and no rendering component.** It ships the composition layer: four
YAML manifests, four thin landing anchors, the paths-hub card population, the smoothness audits, and
every manifest growth as backfill content lands.

## Why the manifest layer is its own deliverable

The five-way split of `shared-course-library-and-learning-paths` could have folded manifest authoring
into either the navigation plan (which renders manifests) or the course-authoring plan (which
supplies the bodies a manifest orders). Neither works, and the reason is structural rather than
stylistic:

- **Folding into the navigation plan is impossible.** A manifest whose `courseOrder` names a course
  with no resolving bundle fails `checkManifestIntegrity` outright. The navigation plan merges before
  90 of the 127 bodies exist, so any manifest it published would have to be narrowed to whatever
  happened to exist — and a narrowed manifest that passes integrity looks correct forever. The
  dangerous failure here is silent truncation, not a loud error.
- **Folding into the course-authoring plan produces an unschedulable cycle.** The course-authoring
  plan is Wave 2; this plan is Wave 3. Its backfill phase grew manifests this plan authors, while this
  plan's AI-path phase publishes a manifest over courses that plan authors. Flipping the wave order
  reverses the cycle rather than removing it. **No wave ordering satisfies both directions.**
- **Only an ownership invariant breaks it.** One plan owns every manifest file and every manifest
  mutation; the other owns bodies only and signals band completion. That is this plan.

The consequence is a clean, auditable boundary: any step in any plan that writes a `.yaml` under
`apps/ayokoding-www/src/features/course-paths/manifests/` is either in this plan or is a boundary
violation. There is no ambiguous middle.

## Why four manifests instead of four curricula

The naive alternative — author four separate curricula — would quadruplicate the course corpus,
quadruple the maintenance surface, and let four trees drift out of sync [Judgment call]. The
manifest model avoids that entirely:

- **A path is a lightweight ordered list of course IDs** — cheap to author, cheap to change, and
  impossible to fork a body through. A fifth path costs one more manifest, not one more curriculum.
- **A fix propagates for free.** Because every manifest references courses by stable ID, correcting a
  typo, updating a version, or improving an example in one canonical body benefits every referencing
  path at once.
- **The prerequisite DAG keeps every path honest.** Each manifest is simply a different valid entry
  point and topological ordering into one dependency graph, machine-checked at every phase gate.
- **Growth is additive.** As backfill bands land, each affected manifest grows in place; the arcs
  deepen without any body being touched twice.

## Business Impact

**Pain points addressed**

- The library exists but is unreadable as a journey: without a manifest, a reader lands on a flat
  catalog of 127 courses with no ordering, no entry point, and no signal about what to read first.
- An experienced re-entrant, a productive-fast builder, a theory-first learner, and a
  SWE-to-AI-engineer transitioner are all forced through the same order today, and none is optimally
  served.
- Without the composition layer, the whole upstream investment — the URL restructure, the schema, the
  navigation UI, the 127 authored bodies — has no user-visible product surface. All four upstream
  plans are enabling work whose payoff lands here.
- Without a single owner for manifest mutation, backfill growth would either be skipped (leaving four
  permanently truncated paths that look correct because integrity passes) or duplicated across two
  plans that then drift.

**Expected benefits** (qualitative reasoning; no fabricated metrics)

- **Four audience-fit products from one content investment**, with no duplication and one maintenance
  surface.
- **A reusable composition capability**: a future track (a security track, a data track) costs one
  more manifest plus its landing anchor — proven out by the fourth, AI-engineering track added at
  exactly that marginal cost.
- **A checkable smoothness guarantee**: prerequisite-consistency turns "does this order read
  smoothly?" from an ad-hoc judgment into a machine-verified invariant, re-run at every gate.
- **No silent truncation**: the growth phase closes the gap each smoke-test-scoped manifest
  deliberately left open, and the terminal gate asserts the full arcs against the full 127-course
  catalog.

## Affected Roles

Solo-maintainer repo — no sign-off ceremony. The maintainer wears:

- **Content strategist** — owns each path's arc, its curation (what is omitted), and its framing.
- **Frontend engineer** — authors the YAML data files that the `course-paths` feature loads and
  validates at build time.
- **Content author** (via the `apps-ayokoding-www-general-maker` agent) — writes the four thin landing
  anchors and the paths-hub card copy.
- **Content reviewer** (via `apps-ayokoding-www-link-checker` and the facts checker) — validates the
  landings and their outbound canonical-page links.

Consuming agents: `apps-ayokoding-www-general-maker` (manifest + landing authoring),
`web-researcher` (smoothness-audit facts), `apps-ayokoding-www-link-checker`,
`apps-ayokoding-www-deployer`, and the three live-site testers `web-exploratory-tester`,
`web-usability-tester`, `web-design-tester` for the Rule-15 retest [Repo-grounded — each verified
present under `.claude/agents/`].

## Business-Level Success Metrics

Every metric below is an **observable check**, not a projected number.

- **Four manifests published, zero body duplication** (observable): all four `courseOrder` lists
  reference courses **by ID**; the no-forked-body check reports zero duplicated bodies across the
  three software-engineer-role manifests. Falsifiable in both directions — before Phase 1 no manifest
  file exists at all.
- **Prerequisite DAG consistency holds at every gate** (observable): `checkManifestIntegrity` +
  `checkPrerequisiteConsistency` exit 0 across every published manifest at every phase gate, so a
  regression cannot survive a single phase boundary.
- **interview-ready MVP proves the architecture first** (observable): the interview-first path's
  landing, manifest, and path-aware nav are live in production before the AI path and the other two
  manifests are composed.
- **The AI path is assumes-competence-first** (observable): its manifest **links** rather than
  includes SWE-fundamentals prerequisites, and **walks** the nine-course AI/harness cluster (DD-33);
  authoring it has priority #1 over the immediately-effective and fundamentally-strong manifests.
- **immediately-effective is build-app-first** (observable): its manifest places editor/tooling → one
  language end-to-end → build a real app ahead of CS-fundamentals/DS&A/algorithms/systems depth.
- **fundamentally-strong is theory-first** (observable): its manifest places CS
  foundations/architecture/paradigms/DS&A ahead of build-at-scale courses.
- **No manifest ships permanently truncated** (observable): after the growth phase, the interview-ready
  and fundamentally-strong manifests both carry all five Band-9 interview-technique courses, the
  immediately-effective manifest carries none of them by design, and the AI path has grown from its
  six-course smoke-test spine to its full 15-course composition.
- **The full catalog resolves** (observable): 127 course bundles resolve under
  `apps/ayokoding-www/content/en/learn/courses/` and all four manifests validate against them.
- **Progression smoothness verified per path** (observable): each manifest passes its own smoothness
  audit — prereq-chaining, monotonic-ish difficulty, skip/fast-path affordances, and (for
  interview-ready) the refresh register — before archival.
- **No regressions** (observable): `npx nx run ayokoding-www:build`, the affected test tiers,
  `specs:behavior:coverage`, heading-hierarchy, markdownlint, and link validation all pass.

## Business-Scope Non-Goals

- **Authoring or editing any course body.** Every body — the 37 re-homed bundles, the 61 transferred
  topics, the 10 remaining new courses, the 8 remaining capstones, the 5 Band-9 interview bodies, and
  the 6 net-new AI courses — is owned by `ayokoding-learning-path-04-course-authoring`. This plan
  reads bodies (to verify a `courseOrder` ID resolves) and never writes one.
- **Building or changing any rendering component.** `path-landing.tsx`, `path-card.tsx`,
  `path-rail.tsx`, `path-banner.tsx`, `path-course-links.tsx`, `prerequisite-list.tsx`,
  `manifest-repository.ts`, and the `?path=` route wiring are owned by
  `ayokoding-learning-path-03-navigation-ui`. This plan consumes them.
- **Defining the `PathManifest` schema or the integrity gates.** Owned by
  `ayokoding-learning-path-02-schema-and-prerequisite-dag`. This plan runs the gates; it does not
  author them.
- **Any URL, redirect, or IA change.** Owned by `ayokoding-learning-path-01-url-restructure`.
- **Adding an Indonesian mirror of the path content** — deferred. `id/belajar/` has zero courses and
  zero paths, so a path manifest over it would compose nothing. The nav mechanism itself is
  locale-neutral; this is a content-availability fact, not a code limitation.
- **Path-level progress persistence, accounts, or bookmarking** — the path context stays URL/client
  state for this plan.
- **Enumerating speculative course variants** — variants are authored on demand only, and by the
  course-authoring plan when they are.
- **A fifth path.** The four-path composition is locked (DL-1 / DL-15); a fifth would be its own plan.

## Business Risks and Mitigations

| Risk                                                                                                         | Mitigation                                                                                                                                                                                                                                                                                      |
| ------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A manifest references a missing or renamed course ID.                                                        | `checkManifestIntegrity` verifies every `courseOrder` ID resolves to a bundle under `<COURSES>`; it runs as a unit test and as a check on every phase gate. Course IDs are stable slugs, never renumbered.                                                                                      |
| A manifest orders a course before its declared prerequisite, breaking the DAG.                               | `checkPrerequisiteConsistency` verifies every manifest is a valid topological entry into the prerequisite DAG; a violation fails the phase gate, not a later review.                                                                                                                            |
| A manifest ships **narrowed** to whatever content happened to exist and is never grown.                      | Every smoke-test-scoped manifest carries a falsifiable before/after check written at publication time — the deferred IDs must be absent now and present after growth. Phase 5 is a dedicated growth phase and the terminal gate asserts the full arcs, so silent truncation cannot pass.        |
| Duplication creeps in — a path forks a body for its framing.                                                 | Framing is limited to an optional intro/outro callout applied by the path layer (DD-7 / DL-5); a distinct-pedagogy need is met by a separate course variant in the course-authoring plan, never a body copy. Enforced by the no-forked-body check at every manifest gate.                       |
| The course-authoring plan edits a manifest, or this plan edits a body — the boundary erodes.                 | The manifest ownership invariant is stated in both plans' READMEs and tech-docs, and this plan's Phase 6 gate greps the manifest directory's git history scope. Any `.yaml` mutation outside this plan is a boundary violation by definition, not a judgment call.                              |
| The per-role convergence amendment reads as a contradiction of the original "one converging endpoint" claim. | The amendment is documented explicitly in one place (DD-22) and cross-referenced from every prose and diagram site that made the original claim, rather than silently overwritten — a reader following any link lands on the current model.                                                     |
| The DD-7 invariant and its DD-28 amendment land in **different plans**, so a reader inherits a stale claim.  | This plan's DD-7 carries the full amendment sentence verbatim plus a working cross-plan link to `ayokoding-learning-path-04-course-authoring`'s DD-28; that plan's DD-28 carries the reciprocal link back and restates DD-7's surviving half. See [tech-docs](./tech-docs.md#design-decisions). |
| A course-surgery change in the upstream plan silently breaks a manifest here.                                | DD-28's binding rule: every surgery states its blast radius across all four manifests before it is applied, and every affected manifest is re-verified prerequisite-consistent afterward. This plan re-runs both gates whenever a band lands.                                                   |
| The four path landings regress the paths hub or the rendering components this plan does not own.             | This plan writes content and data only — no component file is touched. The Rule-15 three-tester retest runs against all four landings plus the hub, and every defect finding is fixed before archival.                                                                                          |
| Cross-plan `syllabus/` links break when the schema plan archives ahead of this plan.                         | That plan's archival phase repoints all four surviving plans' links in the same commit as its `git mv`; this plan additionally carries a pre-archival link-validation gate scoped to its own folder. Both checks are required — neither alone is sufficient.                                    |
