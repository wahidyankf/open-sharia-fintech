# Business Requirements — Learning Path Schema and Prerequisite DAG

## Business Goal

Build the **data layer** that makes a shared course library possible: a machine-readable
`PathManifest` schema, a course-prerequisite contract that turns the library into a **prerequisite
DAG**, and a set of **pure resolvers** over both — so that one canonical course body can be composed
into four different learning paths without any body being forked.

The business claim of the parent architecture is that **one content investment serves four
audiences**. That claim is only true if order lives outside the body. This plan is the piece that
moves it there, and the piece that makes "does this path read smoothly?" a **machine-checkable
invariant** instead of a recurring editorial judgment call.

Nothing user-facing ships here. That is the point: the data layer is extracted into its own Wave-1
plan precisely so that the two Wave-2 plans (`ayokoding-learning-path-03-navigation-ui` and
`ayokoding-learning-path-04-course-authoring`) can both start against a settled, merged contract
rather than racing each other to invent one.

## Why this is its own plan, and its own wave

Three business reasons, in descending order of cost avoided:

1. **It unblocks two plans at once.** Both Wave-2 plans consume this plan's output — the UI plan
   imports the five pure `core/` modules; the authoring plan authors against the `syllabus/` specs
   and declares the `prerequisites:` contract. Landing the data layer first converts a serial chain
   into a two-wide fan-out.
2. **A pure functional core is cheap to get right and expensive to get wrong late.** Every module in
   this plan is IO-free and unit-testable without a browser, a server, or a fixture site. Discovering
   a schema flaw here costs one PR; discovering it after four manifests, 90 course bodies and a
   rendered path rail exist costs a coordinated change across three plans.
3. **It gives the `syllabus/` corpus a single, stable, versioned home** before either of its two real
   consumers starts reading from it. A corpus with two owners forks; a corpus with no owner rots.

## Business Impact

**Pain points addressed:**

- **Order is trapped in the body.** Reading order is carried today by a single `weight` frontmatter
  value per page [Repo-grounded — `computePrevNext` in
  `apps/ayokoding-www/src/features/content/core/tree-builder.ts` sorts siblings by `weight`]. One
  body physically cannot encode four orders, so without this plan the four-path product is
  unbuildable except by duplicating content.
- **Path smoothness is an unfalsifiable claim.** Without a declared prerequisite graph there is no
  way to state, let alone check, that a path never presents a course before its prerequisites. The
  question degrades to "does this order feel right?" — re-litigated every time a manifest changes.
- **A manifest can silently reference a course that does not exist.** With no integrity check, a
  renamed or not-yet-authored course ID produces a dead entry that surfaces as a broken page rather
  than a build failure.
- **Two Wave-2 plans would otherwise invent the same contract twice.** The `prerequisites:`
  frontmatter shape is written by one plan and read by another; without a single canonical owner the
  two definitions drift, and the drift is silent (see the risk table below).

**Expected benefits** (qualitative reasoning; no fabricated metrics):

- A reusable **course-library + path-manifest + prerequisite-DAG** capability in `ayokoding-www` that
  a future track can compose for the marginal cost of one more manifest.
- **Smoothness becomes a gate, not an opinion.** `checkPrerequisiteConsistency` converts the
  most-argued property of a learning path into a boolean a phase gate can assert.
- **Manifest drift becomes a build failure, not a broken page.** `checkManifestIntegrity` catches a
  dangling or duplicated `courseOrder` entry before it can ship.
- **Two downstream plans start in parallel** against one settled, merged contract instead of
  serialising behind an unwritten one.

## Affected Roles

Solo-maintainer repo — no sign-off ceremony. The maintainer wears:

- **Architect** — owns the manifest schema, the prerequisite DAG model, and the functional-core
  boundary.
- **Frontend engineer** — implements the pure `core/` modules and extends `content-url.ts`.
- **Spec author** (via `specs-maker`) — writes the `course-paths` Gherkin companion.
- **Corpus custodian** — keeps `syllabus/` intact and linkable for the two downstream plans that
  actually read it.

Consuming agents: `swe-typescript-dev` (core logic), `specs-maker` (Gherkin companion),
`repo-setup-manager` (Phase 0) [Repo-grounded — all three exist under `.claude/agents/`].

## Business-Level Success Metrics

Every metric below is an **observable check**, not a projected number.

- **The pure core exists and is IO-free** (observable): `test -d
apps/ayokoding-www/src/features/course-paths/core` returns 0, and no file under `core/` imports
  `fs`, `path`, or React. Falsifiable in both directions — the directory does not exist today, and a
  single stray `import fs` fails the check.
- **Order lives in the manifest** (observable): a `PathManifest` parsed from the zod schema carries
  a `courseOrder` array, and `resolvePathNav(manifest, courseId)` returns that manifest's
  neighbours — not `weight` neighbours. Verified by unit test.
- **Prerequisite consistency is machine-checkable** (observable):
  `checkPrerequisiteConsistency(manifest, prerequisitesByCourse, libraryCourseIds)` reports any
  course whose declared, in-library prerequisite appears later in `courseOrder` than the course
  itself. Verified by unit test with both a passing and a deliberately-violating fixture.
- **Manifest integrity is machine-checkable** (observable): `checkManifestIntegrity(manifest,
libraryCourseIds)` reports every unresolved ID and every duplicated ID. Verified by unit test with
  both a clean and a deliberately-broken fixture.
- **Path context degrades gracefully** (observable): `parsePathContext` returns `null` for an
  unknown path ID and for an absent param, never throws. Verified by unit test.
- **The `course-paths` Gherkin companion exists** (observable): the feature files land under
  `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/course-paths/`, and
  `npx nx run ayokoding-www:specs:behavior:coverage` reports the coverage delta rather than an
  unknown-domain error.
- **The `syllabus/` corpus is intact and linkable** (observable): the folder holds exactly 128 files
  at archival, and the pre-push-hook form of `md links validate` prints
  `All links valid! No broken links found.` after the archival repoint.
- **No rendered surface regresses** (observable): after `content-url.ts` gains the optional `pathId`
  param and the canonical `/en/c/learn/courses/<course-id>` shape, existing learn pages in **both**
  supported locales (`en` and `id` [Repo-grounded — `SUPPORTED_LOCALES` in
  `apps/ayokoding-www/src/features/i18n/core/config.ts`]) render exactly as before, with a clean
  browser console. Verified by the Phase 4 no-regression sweep with committed screenshot evidence.
- **No regressions overall** (observable): `npx nx affected -t typecheck lint test:quick test:unit
test:integration test:e2e specs:behavior:coverage` exits 0, and
  `npx nx run ayokoding-www:build` exits 0.

## Business-Scope Non-Goals

- **Authoring any manifest `.yaml` file.** Every file under
  `apps/ayokoding-www/src/features/course-paths/manifests/` is owned by
  `ayokoding-learning-path-05-manifests`. This plan creates the **directory and its `README.md`**,
  and nothing else in it.
- **Authoring or editing any course body.** Course bodies belong to
  `ayokoding-learning-path-04-course-authoring`.
- **Editing any file under `syllabus/`.** The corpus is custodied here, not maintained here.
- **Building any component, route, or rendered page.** Everything under `shell/`, the `?path=` route
  wiring, and the whole UI design funnel belong to `ayokoding-learning-path-03-navigation-ui`.
- **Creating the `<COURSES>_index.md` / `<PATHS>_index.md` content homes.** They belong to
  `ayokoding-learning-path-01-url-restructure`.
- **Writing `prerequisites:` frontmatter into the 37 re-homed course bundles.** This plan defines the
  field's shape; `ayokoding-learning-path-01-url-restructure` writes the values.
- **Extending anything to the `id` locale's content.** The parent architecture's Indonesian content
  mirror is deferred. This plan's code is locale-neutral and is verified against **both** locales,
  but authors no `id` content.

## Business Risks and Mitigations

| Risk                                                                                                                                               | Mitigation                                                                                                                                                                                                                                                                                                                        |
| -------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **The `prerequisites:` frontmatter contract drifts between this plan and `ayokoding-learning-path-01-url-restructure` — and the drift is silent.** | Both plans are Wave 1 and merge independently, so nothing serialises them. The contract is therefore **reproduced verbatim in both plans' `tech-docs.md`, with this plan canonical**. The failure mode is 37 empty prerequisite lists with a green build, surfacing only in Wave 2 — which is why duplication beats linking here. |
| A path manifest violates the prerequisite DAG (a course precedes its prerequisite).                                                                | `checkPrerequisiteConsistency` runs as a phase gate and a unit test in every consuming plan; course IDs are stable slugs, never renumbered.                                                                                                                                                                                       |
| Four manifests drift or reference a missing/renamed course ID.                                                                                     | `checkManifestIntegrity` (every `courseOrder` ID resolves to a library course; no ID appears twice) runs as a phase gate and a unit test.                                                                                                                                                                                         |
| Path context lost on share/deep-link degrades the reading experience.                                                                              | Graceful canonical fallback is a first-class design requirement in the core: `parsePathContext` returns `null` for unknown or absent path IDs and never throws. Covered by Gherkin + unit test; the rendered half is `ayokoding-learning-path-03-navigation-ui`'s.                                                                |
| Duplication creeps in (a path forks a body for its framing).                                                                                       | The manifest format admits only a course-ID string or `{ id, framing }` — there is no field in which a forked body could be expressed. Framing is a callout applied by the path layer, never a body copy.                                                                                                                         |
| **The `syllabus/` corpus is copied into a consuming plan instead of linked, forking 121 specs.**                                                   | The custody rule is stated in this plan's `README.md` and restated as a `> **Cross-plan source of truth**` blockquote in each of the other four plans' READMEs. A copy is a boundary violation, not a convenience.                                                                                                                |
| **This plan archives (Wave 1) while four plans still link into `syllabus/`, breaking 34 links.**                                                   | The `Plan Archival` phase carries a reciprocal repoint step that rewrites every inbound cross-plan link in the **same commit** as the `git mv`, then runs the pre-push hook's own form of `md links validate`. Without it the next push from any surviving plan fails for an unrelated reason.                                    |
| The DD-34 / DD-35 / DD-39 numbering gap is "fixed" by a future reader, corrupting 276 in-corpus tokens.                                            | The source plan's explanatory passage is restated **verbatim** in this plan's `README.md` and `tech-docs.md`, with an explicit "never renumber" instruction and the post-split verification command.                                                                                                                              |
| `content-url.ts`'s new canonical shape regresses existing learn pages.                                                                             | The change is additive (an optional `pathId` param) and is covered by the existing `content-url` unit tests, updated in the same commit; Phase 4 runs a live no-regression sweep across **both** supported locales at three breakpoints with committed screenshot evidence.                                                       |
| The pure core acquires IO and stops being unit-testable without a harness.                                                                         | A REFACTOR step asserts `core/` imports no `fs` and no React; the functional-core/imperative-shell boundary is DD-9, restated in `tech-docs.md`.                                                                                                                                                                                  |
