# Business Requirements — Fundamentally Strong Shared Course Library, Two Tracks

## Business Goal

Reframe the "Fundamentally Strong" curriculum as a **shared course library** consumed by **two
learning paths**, so one body of already-authored (and being-authored) content can serve two very
different readers without duplication:

- a **`software-engineer`** path that teaches SWE with an **"immediately effective"** principle —
  set up the editor, learn one language end-to-end, **build a real app first**, then deepen into CS
  fundamentals, data structures, algorithms, and systems; and
- a **`job-seeking-software-engineer`** path — the **interview-first** arc for an experienced
  engineer re-entering the job market.

Each course is a **building block** (one topic = one course, stable ID, single canonical body); each
path is an **ordered manifest** over the library. The business change is **architecture + framing +
a real navigation UI**, plus the thin layer of NEW courses the interview track and the productivity/
harness/security clusters need — not a rewrite of the 94 existing topics' subject content.

## Why a shared library instead of two curricula

The naive alternative — author two separate curricula — would duplicate ~94 topics, double the
maintenance surface, and let the two drift out of sync [Judgment call]. The shared-library model
avoids that entirely:

- **Single source of truth per course.** A course body is authored once and lives at one canonical
  URL. Fixing a typo, updating a version, or improving an example benefits **both** paths at once.
- **Zero duplication.** A path is a lightweight ordered list of course IDs — cheap to author, cheap
  to change, and impossible to fork a body through.
- **Omit-or-create keeps each path honest.** A path omits a course that does not fit its arc, and
  creates a new course only when nothing in the library covers a real need — and that new course is
  then available to the other path too. Growth is additive and shared.
- **Two audiences, one investment.** The maintainer already invested in ~94 topics for one arc;
  the shared-library model turns that single investment into two products (a from-scratch/productive
  builder track and a job-seeker track) for the marginal cost of two manifests plus the interview/
  productivity NEW courses.

## Why these two paths

The maintainer's read of how the material is actually consumed identifies two distinct, high-value
entry points [Judgment call]:

- **The builder who wants to be effective fast** (`software-engineer`). This reader does not want a
  spiral or a theory-first march; they want to set up their editor, pick up one language, **ship a
  real working app early**, and only then go deep. Shipping-first sequencing matches how motivated
  self-learners actually stay engaged — momentum from a working artifact, then depth once the payoff
  is felt.
- **The experienced engineer re-entering the job market** (`job-seeking-software-engineer`). This
  reader lands days-to-weeks before a senior loop, already owns the editor workflow and the deep
  fundamentals, and needs to **refresh breadth fast, relearn interview technique, and get
  interview-ready** at mid/senior/staff level — including framing a layoff / employment-gap
  narrative. The interview-first arc leads with the most time-pressured, highest-stakes use.

One library serves both because the underlying **principles are the same** — only the **order** and
the **thin framing** differ. That is exactly what a manifest expresses.

## Why the navigation is a real UI change (not just content)

A single body served in two different orders cannot be expressed by the current model, where reading
order is carried by a single `weight` frontmatter value per page [Repo-grounded — `computePrevNext`
in `apps/ayokoding-www/src/features/content/core/tree-builder.ts` sorts siblings by `weight`]. Two
orders over one body require the **order to move out of the body and into the path manifest**, and
the course page's prev/next + breadcrumb to **resolve against the active path**. That is a genuine
frontend change to ayokoding-www (a Next.js app) — routing, a `?path=` context, manifest-driven
navigation, and a graceful fallback when a course is deep-linked without path context. The maintainer
explicitly asked that this UI be **planned properly**, with a design funnel, accessibility, and
unit/integration/e2e tests plus a `specs/` Gherkin companion.

## Business Impact

**Pain points addressed**:

- Today the curriculum has exactly one arc; a job-seeker and a productive-builder are forced through
  the same order, and neither is optimally served.
- There is no interview-technique material and no shipping-first productive on-ramp as a first-class
  path.
- A second curriculum would duplicate content and double maintenance.

**Expected benefits** (qualitative reasoning; no fabricated metrics):

- Two audience-fit products from one content investment, with no duplication and one maintenance
  surface.
- A reusable **course-library + path-manifest** capability in ayokoding-www that future tracks
  (e.g. a security track, a data track) can reuse for the marginal cost of one more manifest.
- The interview track ships real technique modules; the software-engineer track ships a shipping-first
  productive arc — each with a coherent, path-aware reading experience.

## Affected Roles

Solo-maintainer repo — no sign-off ceremony. The maintainer wears:

- **Content strategist** — owns the two-path architecture and each path's arc/framing.
- **Frontend engineer** — builds the ayokoding-www path-aware navigation feature.
- **Content author** (via the `apps-ayokoding-www-*-maker` agents) — writes the NEW courses.
- **Content reviewer** (via the `apps-ayokoding-www-*-checker` + facts/link checkers) — validates.

Consuming agents: `apps-ayokoding-www-by-example-maker`, `apps-ayokoding-www-annotated-concept-maker`,
`apps-ayokoding-www-primer-maker` and their matching checkers, plus `apps-ayokoding-www-facts-checker`
and `apps-ayokoding-www-link-checker` [Repo-grounded]; `swe-typescript-dev` and `swe-e2e-dev` for the
navigation UI feature.

## Business-Level Success Metrics

- **One body, two orders, zero duplication** (observable, first-class signal): every course has
  exactly one canonical body; both path manifests reference courses **by ID**; a grep confirms no
  course body is duplicated per path. The
  [tech-docs §Course Library Catalog](./tech-docs.md#course-library-catalog) enumerates each course
  once.
- **Path-aware navigation works** (observable): from a path landing page, a reader walks the course
  order for that path; prev/next and breadcrumb follow the path manifest; a course deep-linked
  without `?path=` renders a coherent canonical view. Verified by unit + integration + e2e tests and
  the `specs/` Gherkin companion.
- **Job-seeking path ships first, end-to-end** (observable): the interview-first path — landing page,
  its NEW courses, its manifest, path-aware nav — is complete and deployed to production **before**
  the software-engineer path begins.
- **Software-engineer path is shipping-first** (observable): its manifest places editor/tooling → one
  language end-to-end → **build a real app** ahead of CS-fundamentals/DS&A/algorithms/systems depth;
  it reuses the shared courses with zero body duplication.
- **Interview coverage** (observable): the four NEW interview modules ship a learning + drilling
  track each, in a **refresh register**, and pass their checker + facts-checker + link-checker; the
  behavioral module covers the **layoff / employment-gap narrative**.
- **Productive in target codebases** (observable, retained from the prior scope): the productivity/
  harness/security NEW courses (`async-python-and-fastapi-services`, `browser-automation-with-cdp`,
  the harness cluster, `just-enough-cpp`, `detection-engineering-and-siem-operations`,
  build-your-own capstones) fill the stack gaps for the target codebases; see
  [tech-docs §Productive in Target Codebases](./tech-docs.md#productive-in-target-codebases-proof-of-transfer-outcome-anchor).
- **Progression smoothness** (observable): each path reads smoothly for its persona — prereq-chaining,
  monotonic-ish difficulty, skip/fast-path affordances, and (for the interview path) refresh register —
  verified by a per-path smoothness audit before archival.
- **No regressions** (observable): `nx run ayokoding-www:build` renders green; `test:unit` /
  `test:integration` / `test:e2e`, heading-hierarchy, markdownlint, and link validation pass across
  the app and the section; old `software-engineer/<topic>` URLs redirect to `courses/<course-id>`.

## Business-Scope Non-Goals

- Re-writing the pedagogy or depth of any existing topic (only re-homing + re-framing + re-ordering).
- Adding an Indonesian mirror of the section content — deferred (the nav UI still handles all app
  locales correctly).
- Building path-level progress persistence, accounts, or bookmarking — the path context is
  URL/client-state only for this plan (a future enhancement).
- Interactive/JS flashcards — drilling stays static markdown, matching the sibling.

## Business Risks and Mitigations

| Risk                                                                               | Mitigation                                                                                                                                                            |
| ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Dependency not actually done — building over a partially-authored tree breaks nav. | Group A precondition gate hard-blocks until the sibling plan is confirmed DONE (all 94 topics + 3 capstones live). See [delivery.md](./delivery.md) Phase 0.          |
| Re-homing bodies to `courses/` breaks live URLs.                                   | Every re-home lands with a redirect (`apps/ayokoding-www/src/redirects/`) from the old `software-engineer/<topic>` URL to the new `courses/<course-id>` URL.          |
| Path context lost on share/deep-link degrades the reading experience.              | Graceful canonical fallback is a first-class design requirement + a Gherkin scenario + an e2e test; a course page always names the paths that include it.             |
| Two manifests drift or reference a missing/renamed course ID.                      | A manifest-integrity check (every `courseOrder` ID resolves to a library course) runs as a phase gate and a unit test; course IDs are stable slugs, never renumbered. |
| Duplication creeps in (a path forks a body for its framing).                       | Framing is limited to an optional intro/outro callout applied by the path layer; the body is never copied — enforced by review + a no-duplicate-body check.           |
| Navigation UI regresses existing content nav (non-path readers).                   | The canonical (no-path) view is the existing behavior; the UI adds path-awareness without changing default nav — covered by retained navigation specs + tests.        |
