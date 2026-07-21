# Business Requirements — Path-Aware Navigation UI

## Business Goal

Make one canonical course body behave correctly under **four different reading orders** within the
`careers/` category, so the shared-course-library architecture the sibling plans build is actually
usable by a reader. Without this plan the library is a folder of pages and the manifests are inert
data files: nothing renders a path, nothing carries path context between pages, and nothing tells a
reader where they are in an arc.

> **2026-07-21 category-split ruling.** The maintainer ruled a `careers/` + `skills/` category split
> (full record in [README.md §Category Split Ruling](./README.md#category-split-ruling-2026-07-21-r1r8)).
> This plan stays **careers-only** for content (four manifests, four personas), but its rendering
> components must be **category-agnostic** so a sibling plan can render the `skills/` category
> through the same code — that is why the paths hub and category landing below now speak of "the
> **six** paths in **two** categories" rather than "the four paths."

Concretely, this plan delivers the **ayokoding-www rendering layer** for the six-path, two-category
model (four `careers/` paths owned here; two `skills/` paths owned by a sibling plan and rendered
through this plan's category-agnostic components):

- the **site landing hero** at `/en` that surfaces the four **career**-goal paths directly, so a
  goal-driven visitor is not dropped into a recall-heavy browse index;
- the **category-grouped paths hub** at `/en/learn/paths` where all six paths, grouped into
  `careers/` and `skills/`, are compared and chosen;
- the **category landing** (`/en/learn/paths/careers/`, `/en/learn/paths/skills/`) and, for
  `careers/` only, the **arc landing** (`/en/learn/paths/careers/<arc>/`) — five new pages that make
  every URL segment a real, rendered page rather than a routing waypoint (see
  [README.md R7](./README.md#category-split-ruling-2026-07-21-r1r8));
- the **path landing** at `/en/learn/paths/<path-id>` (now a variable-depth id — 3 segments under
  `careers/`, 2 under `skills/`) that renders a manifest as an ordered, prerequisite-consistent
  syllabus;
- the **course page in path context** — a left path rail carrying the whole ordered arc, a compact
  position readout, a path-aware breadcrumb, a prerequisite list, and manifest-driven prev/next, all
  keeping `?path=`; and
- the **graceful canonical fallback** that makes a deep-linked or shared course URL render coherently
  with no path context at all.

## Why the navigation is a real UI change (not just content)

A single body served in four different orders cannot be expressed by the current model, where reading
order is carried by a single `weight` frontmatter value per page [Repo-grounded — `computePrevNext` in
`apps/ayokoding-www/src/features/content/core/tree-builder.ts` sorts siblings by `weight`]. Four
orders over one body require the **order to move out of the body and into the path manifest**, and the
course page's prev/next + breadcrumb to **resolve against the active path**. The course page must also
**surface each course's declared prerequisites**.

That is a genuine frontend change to `ayokoding-www` (a Next.js app) — routing under the
`/en/learn` URL model, a `?path=` context, manifest-driven navigation, prerequisite display, and a
graceful fallback when a course is deep-linked without path context. The maintainer explicitly asked
that this UI be **planned properly**, with a design funnel, accessibility, and unit/integration/e2e
tests plus a `specs/` Gherkin companion. This plan is where that request is discharged.

## Why the rendering layer is its own plan

The split that produced this plan exists to buy parallelism, and the rendering layer is the natural
seam:

- **It has exactly two upstream artefacts and one downstream consumer.** It needs the pure
  `course-paths/core/` modules (from `ayokoding-learning-path-02-schema-and-prerequisite-dag`) and
  the `courses/` + `paths/` content homes plus the re-home redirect table (from
  `ayokoding-learning-path-01-url-restructure`); it hands its components to
  `ayokoding-learning-path-05-manifests`. Nothing else touches it.
- **It is provable against a fixture, not against real content.** Every rendering behaviour this plan
  ships is verified against a **fixture manifest** with a handful of real course IDs. That is what
  lets the rendering layer merge in Wave 2, ahead of the Wave-3 plan that publishes real manifests,
  without any scenario whose `Given` cannot be met.
- **It is the only UI-bearing surface of the five.** Concentrating the design funnel, the
  accessibility contract, and the Rule-15 three-tester retest in one plan means one reviewer pass
  covers the whole user-facing change instead of four partial ones.

## Business Impact

**Pain points addressed**

- The library and the manifests are **invisible without a renderer**. A published `.yaml` manifest
  with no `manifest-repository.ts` to load it is never parsed, never validated, and never rendered —
  so every downstream path-completion claim would be unverifiable.
- Today's landing hero offers only two generic CTAs (**Start learning** → a browse index, and
  **Explore tools**), so a goal-driven learner has **zero path scent** above the fold
  [Repo-grounded — `apps/ayokoding-www/src/features/app-shell/shell/hero.tsx`].
- A reader inside a long path has no way to see the arc: without a rail, "where am I / what's next /
  what did I skip" costs a round trip to the path landing on every course.
- A shared or bookmarked course URL carries no path context, so without a first-class canonical
  fallback the most-shared kind of link would be the most broken one.
- Screen-reader and keyboard readers would be excluded from path-aware navigation entirely unless the
  rail, banner, breadcrumb, prerequisite list, and prev/next are labelled landmarks from the start.

**Expected benefits** (qualitative reasoning; no fabricated metrics)

- A **reusable path-rendering capability** in `ayokoding-www`: once the shell exists, a fifth or sixth
  path costs one more manifest and zero UI work.
- **Zero regression surface for the no-path reader.** Because the rail is a `children` swap in two
  already-shipped hosts, a course opened without `?path=` renders byte-identically to today — the
  majority of the site's pages are untouched by construction, and a guard test asserts it in both
  directions.
- **The design decision is auditable.** Every screen carries two named alternatives, two hi-fi
  finalists at three viewports each, a named selection, and a rationale table — so a later reader can
  see what was rejected and why, instead of inheriting a layout with no provenance.
- **Mobile is designed, not described.** The funnel renders every option at 375 / 768 / 1280 px, which
  is exactly what surfaced the Screen 3 reselection (DD-46) that a desktop-only artefact set had
  hidden behind a prose footnote.

## Affected Roles

Solo-maintainer repo — no sign-off ceremony. For this plan the maintainer wears:

- **Frontend engineer** — builds the `course-paths` shell, the route wiring, and the path rail.
- **Designer / content strategist** — runs the four-screen design funnel and records the selections.
- **Accessibility reviewer** — owns the landmark, focus, and non-colour-signal contract.
- **QA** — runs the fixture-manifest e2e suite, the Playwright breakpoint walk, and the Rule-15
  three-tester retest.

Consuming agents: `swe-typescript-dev` and `swe-e2e-dev` for the feature code; `web-researcher` for
the R7 prior-art survey; the `swe-developing-frontend-ui` skill for the R5 component survey;
`web-exploratory-tester`, `web-usability-tester`, and `web-design-tester` for the Rule-15 retest
[Repo-grounded — all exist under `.claude/agents/`].

## Business-Level Success Metrics

Every metric below is **observable** — a command or a rendered behaviour, not a projected number.

- **Path-aware navigation works** (observable): from a fixture path landing, a reader walks the course
  order; prev/next and breadcrumb follow the fixture manifest; a course deep-linked without `?path=`
  renders a coherent canonical view. Verified by unit + component + e2e tests and the `specs/` Gherkin
  companion.
- **The no-path reader has zero regression** (observable): with no `?path=`, `ResizableSidebar`
  receives `<Sidebar>` and `MobileNav` receives `<SidebarTree>`, exactly as today; a guard test fails
  if the rail renders without a path context **and** fails if the generic sidebar renders with one.
- **Prerequisites are surfaced on every course page** (observable): the prerequisite list renders in
  **both** the path-aware and the canonical view, each entry linking to its canonical course URL.
- **The landing hero surfaces the four career paths** (observable): the `/en` hero renders a
  goal-labelled path card per published **careers** path plus a "Compare all paths" link to
  `/en/learn/paths`, which routes into the category-grouped hub. Falsifiable in both directions —
  today's hero renders neither.
- **Every URL segment renders, none 404s** (observable, R7): the paths hub, both category landings
  (`careers/`, `skills/`), and all three `careers/` arc landings each render real page content — none
  is a bare routing waypoint. `careers/immediately-effective/` renders both its paths without reading
  as broken or empty; `skills/` renders its fixed-arc ramp statement with no arc chooser (R8).
- **The design funnel is complete for Screens 0–3 plus the two new screen types (1a, 1b)**
  (observable): this plan's `assets/` holds **36** `*-option-*-*.png` renders (8 before the funnel
  phase), each embedded in `prd.md` with viewport-specific alt text, and each screen's selection line
  names its selected finalist's three render files. `ayokoding-learning-path-01-url-restructure`'s
  Screen 4 share (6 renders) is unchanged.
- **Accessibility holds** (observable): the rail, banner, breadcrumb, prerequisite list, and prev/next
  are each a labelled landmark, keyboard-reachable with a visible focus ring; the current course
  carries `aria-current="page"` plus a non-colour signal; `html[lang]` matches the active locale.
- **The rail is usable at the tablet floor** (observable): at 768 px the rail renders as number +
  ellipsised title with the full title in the link's `aria-label`, verified by a dedicated Playwright
  step and a hi-fi render at that exact width.
- **No regressions** (observable): `npx nx run ayokoding-www:build`, `:typecheck`, `:lint`,
  `:test:unit`, `:specs:behavior:coverage` and `npx nx run ayokoding-www-fe-e2e:test:e2e` all exit 0;
  markdown link, heading-hierarchy, and markdownlint validation pass.

## Business-Scope Non-Goals

- **Publishing any real path manifest.** Every rendering behaviour here is proven against fixture
  manifests (including a `skills/`-shaped fixture, per R2). All four **careers** manifests belong to
  `ayokoding-learning-path-05-manifests`; the two **skills** manifests belong to a sibling plan (see
  [README.md R4](./README.md#category-split-ruling-2026-07-21-r1r8)).
- **Authoring or editing any course body**, careers or skills. That is
  `ayokoding-learning-path-04-course-authoring`'s scope for careers, and a sibling plan's scope for
  the ERP + accounting corpus.
- **Moving any content bundle, creating any content home, or writing any redirect rule.** The
  `courses/` and `paths/` `_index.md` homes (including the `careers/` category and arc landing
  `_index.md` files), the `legacy/` bucket, and both redirect modules belong to
  `ayokoding-learning-path-01-url-restructure`; the `skills/` category landing's `_index.md` belongs
  to the sibling skills-category plan.
- **Writing the pure `course-paths/core/` modules or the `PathManifest` schema.** Those belong to
  `ayokoding-learning-path-02-schema-and-prerequisite-dag`; this plan imports them.
- **Adding an Indonesian mirror of the section content** — deferred. The path-aware nav UI itself
  remains locale-neutral (it renders whatever locale-specific content exists), so this is a
  content-availability fact, not a code limitation. Manual verification therefore runs in `en` only;
  fabricating an `id` content walk-through for a feature with no `id` content would be evidence
  theatre.
- **Path-level progress persistence, accounts, or bookmarking.** Path context is URL and client state
  only for this plan. The `localStorage` "mark done" and "welcome back — resume" affordances are
  recorded as `[Future]` in the learner-journey record, not built.
- **Interactive/JS flashcards.** Drilling stays static markdown.
- **Screen 4 (the legacy-bucket landing and page banner).** Its funnel section, its six renders, and
  its pending Q-D-dependent selection belong to `ayokoding-learning-path-01-url-restructure`.

## Business Risks and Mitigations

Rows routed to this plan by surface, plus every cross-plan hazard that this plan's surface can cause
or must guard against.

| Risk                                                                                                      | Mitigation                                                                                                                                                                                                                                                          |
| --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Navigation UI regresses existing content nav for non-path readers.                                        | The canonical no-path view is the existing behaviour; the UI adds path-awareness without changing default nav. Covered by retained navigation specs, a two-directional guard test, and a Phase-5 no-path sweep at all three breakpoints.                            |
| The path rail regresses the generic sidebar for **every** content page, not just courses in path context. | The change is a `children` swap only — no fork of `ResizableSidebar`, no second `<aside>`, no second `localStorage` width key. Asserted by the guard test and by a check that exactly one `ResizableSidebar` component definition survives.                         |
| The rail is unreadable at the tablet width floor (~115 px at 768 px).                                     | A specified truncation contract — number plus ellipsised title, full title in the link's `aria-label`, phase labels degraded to bare rules — plus a dedicated 768 px verification step and a hi-fi render at that exact width.                                      |
| Mobile readers lose path context entirely, because the rail is not on screen below `md`.                  | The `PathBanner` readout is retained at every breakpoint as the always-visible "course k of N" signal, with the shipped left drawer as the on-demand expansion — not a new overlay pattern.                                                                         |
| Path context lost on share or deep-link degrades the reading experience.                                  | Graceful canonical fallback is a first-class design requirement (DD-4) plus a Gherkin scenario plus an e2e test; a course page always names the paths that include it and surfaces its prerequisites.                                                               |
| A second, divergent overlay idiom is introduced for the mobile rail.                                      | The rail reuses the shipped `MobileNav` `Sheet` (`side="left"`) with a content swap; bottom sheet and in-flow disclosure were both evaluated and rejected in writing (DD-46).                                                                                       |
| Building the renderer before the pure core merges destroys every RED signal.                              | The Wave-2 start precondition requires `schemas.ts` on disk and both Wave-1 PRs merged. A RED step that fails on an unresolved import proves nothing about the behaviour under test.                                                                                |
| The re-home redirect assertion in this plan's e2e can never go green.                                     | The per-course redirect table is owned and shipped by `ayokoding-learning-path-01-url-restructure` **before** this plan starts (its Wave-1 merge is a hard start precondition); this plan asserts the redirect as a regression guard, not as its own Gherkin.       |
| The DD-47 render matrix is read as under-delivered, or is "fixed" by duplicating renders across plans.    | The 24/6 split is stated in DL-17's amendment note, beside the Phase-1 gate clause, and again in the archival gate. Copying the other plan's six renders into this folder is explicitly forbidden — two copies of one matrix drift.                                 |
| Accessibility is retrofitted after the visual design lands, and ships incomplete.                         | The a11y scenario has its own RED step and its own `playwright-bdd` step definition, authored before the landmarks exist — it is not folded into a REFACTOR step where it would have no prior failing state.                                                        |
| A design alternative is silently discarded, so a later reader cannot tell what was considered.            | Every screen records two named alternatives (three for Screen 0), two hi-fi finalists, a drop reason per cut alternative, a named selection, and a rationale table. The superseded Screen 3 Option A objection is quoted verbatim and answered rather than deleted. |
| The `id` locale silently diverges, or an `id` verification walk is fabricated.                            | The `en`-only content scope is recorded as a Non-Goal here and restated in the manual-verification phase; the nav mechanism's locale-neutrality is stated separately so the scoping is not misread as a code limitation.                                            |
