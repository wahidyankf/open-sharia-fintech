# Product Requirements — Fundamentally Strong Shared Course Library, Four Paths

## Product Overview

The "Fundamentally Strong" curriculum becomes a **shared course library** (one canonical, path-neutral
body per course, keyed by a stable course ID) composed by **four learning paths**. The three
`software-engineer` paths converge on the same software-engineering deep mastery; the fourth path
converges on a distinct AI-engineering deep mastery — convergence is a **per-role** property, not a
library-wide axiom (see [tech-docs.md DD-22](./tech-docs.md#design-decisions)):

- **`interview-ready/software-engineer`** — the **interview/job-prep-first** arc for an experienced
  engineer re-entering the market: interview prep FIRST → production-effective → deeper.
- **`immediately-effective/software-engineer`** — the **immediately-effective** arc: editor/tooling →
  one language end-to-end → **build a real app first** → then deepen.
- **`fundamentally-strong/software-engineer`** — the **university-style, fundamentals-first** arc:
  CS foundations / theory first → deeper.
- **`immediately-effective/software-engineer-to-ai-engineer`** (added 2026-07-20) — the
  **immediately-effective** arc applied to a **role transition**: assumes an already-working software
  engineer; prerequisite courses are **linked, not included**; teaches **building** AI systems (models,
  agents, evals, inference serving), not driving them (`agentic-coding` stays a separate, unrelated
  axis).

A **path is an ordered manifest** composing a **curated subset** of course IDs — not every course is in
every path, and each manifest must be a valid topological entry into the library's **prerequisite
DAG**. Courses are shared with **omit-or-create** semantics, and — as of 2026-07-20 — **course surgery**
(update/merge/split/create) is also permitted, subject to a four-path blast-radius statement per
surgery (see [tech-docs.md DD-28](./tech-docs.md#design-decisions)); a genuinely different teaching
approach is still met by a distinct **course variant**, not a body fork. This plan also delivers the
**ayokoding-www path-aware navigation UI** that makes one canonical course URL behave differently under
each path's context, under the `/en/c/learn` URL model. The library body is largely content (exempt
from `specs:coverage`); the **navigation feature is app code** and carries a `specs/` Gherkin companion
and three-level tests.

**Whole-section IA (scope extension, 2026-07-21).** The plan no longer converts only the
`fundamentally-strong` domain and leaves the rest of the learn section alone. When it lands,
`/{locale}/c/learn/` has **exactly three** structural buckets and nothing else: `paths/`, `courses/`,
and a **new `legacy/`** bucket holding everything that is not yet a course or a path — the six
remaining `en/learn/` domains (`software-engineering`, `artificial-intelligence`,
`information-security`, `personal-development`, `it-governance`, `business`; **1,148** `.md` files
[Repo-grounded]). The relocation is a **prefix move that preserves each domain's sub-taxonomy
verbatim** — no page is rewritten — and every relocated URL keeps working through a per-domain 308
redirect. Design, redirect mechanics, IA consequences, and the six unresolved questions are in
[tech-docs §Learn-Section IA](./tech-docs.md#learn-section-ia--the-three-bucket-model-scope-extension-2026-07-21)
and [tech-docs §Open Questions](./tech-docs.md#open-questions--learn-section-scope-extension-unresolved)
(DD-40 through DD-45).

The topic content of the existing courses is unchanged — the 33 shipped topics (1–33) are **re-homed**
(moved to `courses/<course-id>/` with redirects) and the 61 transferred topics (34–94) are authored
**native** into `courses/`; all are **re-framed** (referenced by four manifests), not rewritten. This
plan additionally **authors fourteen NEW courses + nine NEW capstones** (three original plus six
DD-20 inter-topic capstones) the interview and productivity/harness/security clusters need, plus **six
further NEW AI-specific courses** (2026-07-20) the fourth path needs, for a **127-course** catalog
(121 software-engineer-role baseline + 6 AI-specific; course surgery permitted per DD-28).

## Personas (one per path)

- **Experienced engineer re-entering the job market (north-star for the
  `interview-ready/software-engineer` path)** — recently laid off, returning from a gap/sabbatical, or
  an employed senior wanting to switch. Already owns the editor workflow and deep fundamentals; needs
  to **refresh breadth fast, relearn interview technique** at mid/senior/staff level, and handle a
  **layoff / employment-gap narrative** — without walking a from-scratch curriculum. Interview/job prep
  FIRST.
- **A builder who wants to be effective fast (north-star for the
  `immediately-effective/software-engineer` path)** — wants "immediately effective" SWE: set up the
  editor, learn one language end-to-end, **ship a real app early**, then deepen into CS fundamentals,
  DS&A, algorithms, and systems. Serves both a from-scratch learner and a mid-career switcher.
- **A university-style, fundamentals-first learner (north-star for the
  `fundamentally-strong/software-engineer` path)** — wants the rigorous bottom-up route: CS
  foundations, computer architecture, paradigms, and data structures & algorithms **before** building
  apps at scale. Prefers to understand the machine and the theory first, then apply it.
- **An already-working software engineer transitioning to AI engineering (north-star for the
  `immediately-effective/software-engineer-to-ai-engineer` path, added 2026-07-20)** — already owns the
  SWE fundamentals the other three paths teach; wants to become immediately effective at **building**
  AI systems (models, agents, evals, inference serving), not at driving coding agents. Prerequisite
  courses are **linked, not included** in this path's manifest. Converges on a distinct AI-engineering
  endpoint, not the other three paths' shared software-engineering endpoint.
- **A reader who lands on a shared course by deep-link / share** — arrives at a course URL without a
  path context and must get a coherent standalone view (with its prerequisites surfaced) plus an
  obvious way to enter a path.
- **Maintainer (content strategist / frontend engineer / content author / reviewer)** — owns the
  four-path architecture, builds the navigation feature, and authors the NEW courses via the ayokoding
  maker agents.

## User Stories

- As a **builder new to software engineering**, I want an immediately-effective path that gets me
  productive and shipping a real app fast before deep theory, so that I stay motivated and learn depth
  once I feel the payoff.
- As an **experienced engineer re-entering the market**, I want an interview-ready path with real
  technique modules and a layoff/gap-narrative section, so that I get interview-ready fast at my level.
- As a **university-style learner**, I want a fundamentally-strong path that teaches CS foundations,
  architecture, paradigms, and DS&A before app-building, so that I understand the theory before I apply
  it — the same software-engineering endpoint the other two SWE paths reach, reached bottom-up.
- As an **already-working software engineer**, I want a path into AI engineering that **links** rather
  than re-teaches the SWE fundamentals I already have, so that I get straight to **building** AI
  systems without walking material I've already mastered.
- As a **reader on any path**, I want prev/next and the breadcrumb to follow **my path's order**, so
  that "next" always means the next course in the arc I chose.
- As a **reader on any course page**, I want to see the course's **prerequisites**, so that I know what
  to complete first regardless of which path (or no path) I entered from.
- As a **reader who shares or deep-links a course**, I want the course to render coherently with no
  path context, so that a shared link never breaks — and to see which paths include this course.
- As the **maintainer**, I want each course authored **once**, path-neutral, and referenced by every
  path that needs it, so that a fix or update benefits every referencing path with zero duplication.
- As the **maintainer**, I want a path to **omit** a course that does not fit and **create** a new
  course (or a distinct **variant** when a path needs a different teaching approach) only for a real
  gap, so that each path stays coherent without forking bodies.
- As the **maintainer**, I want to perform **course surgery** (update/merge/split/create) on a shared
  course when needed, stating its blast radius across all four manifests up front, so that the library
  stays coherent as it grows without silently breaking another path.
- As a **reader targeting an AI-agent-infra or security codebase**, I want the async-Python/FastAPI,
  CDP, MCP/harness, C++, and detection-engineering courses available in the library, so that any path
  can lead me to the stack skills those codebases need.
- As a **screen-reader / keyboard user**, I want the path rail, banner, breadcrumb, prerequisite
  list, and prev/next to be fully accessible, so that path-aware navigation works without a mouse.
- As a **reader browsing `/en/c/learn`**, I want the section to offer exactly three understandable
  choices — follow a path, browse the course library, or dig into the older material — so that I am
  not handed a mixed taxonomy of two structural buckets sitting beside six subject domains.
- As a **reader who bookmarked or search-landed on an older learn page**, I want my URL to keep
  working after the section is reorganized, so that no link I hold or that Google holds ever 404s.
- As a **reader who lands on an older, not-yet-converted page**, I want to see that it is legacy
  material and where the canonical course lives (if one exists), so that I do not study a superseded
  page believing it is current.
- As the **maintainer**, I want the legacy relocation to be a pure prefix move that rewrites no page
  bodies, so that a 1,148-file change stays reviewable as a rename diff and carries no content risk.

## Learner Journey (End-to-End)

The design screens are not judged in isolation — they must make the **whole learner arc** smooth, from
the first cold visit through returning months later. This section maps the five journey stages to the
screens/affordances that serve them, the ergonomics principle behind each, and — critically — the
**scope tag** separating what **this plan builds** from **[Future]** enhancements it deliberately
leaves for a follow-up (this plan ships _path-aware navigation_, not a per-user progress backend). It
is grounded in a `web-researcher` window-shop of ~14 platforms on **2026-07-21** (sources in
[R7 Prior-Art Findings](#r7-prior-art-findings-window-shopped-2026-07-21)).

| Stage           | Learner's need                               | Design response (screen / affordance)                                                                                                                           | Scope    |
| --------------- | -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| **1 Landing**   | "Where do I even start?"                     | **Screen 0** hero surfaces the 4 goal cards + "Compare all paths" escape hatch                                                                                  | In-scope |
| **2 Discovery** | "Which path fits me? what's shared?"         | **Screen 1** paths hub (compare paths, course counts); "Browse the full library" for topic-led seekers                                                          | In-scope |
| **3 Before**    | "Am I ready? can I skip ahead?"              | **Screen 2** syllabus preview + advisory `PrerequisiteList` + fast-path "skip the prologue" callout                                                             | In-scope |
| **4 During**    | "Keep me oriented and moving"                | **Screen 3** `PathRail` (whole ordered arc, current course marked) + `PathBanner` readout (step k of N) + path breadcrumb + manifest prev/next keeping `?path=` | In-scope |
| **5 After**     | "I finished — what now? where else is this?" | **Screen 3** `PathCourseLinks` ("this course is also in …") + manifest next → capstone framing                                                                  | In-scope |

**Stage-by-stage smoothness**

- **1 · Landing** — the failure mode today is a hero that dumps a goal-driven learner into a recall-heavy
  browse index. Screen 0 replaces that with four **goal-labeled** cards. Because the labels are the
  learner's own goal ("pass an interview soon"), the four options are trivially comparable and carry a
  built-in heuristic — the exact condition under which choice-overload does **not** bite (see the
  ergonomics note below), and the "Compare all paths" link is the Codecademy-style escape hatch for the
  genuinely undecided. **[Future]** a `localStorage`-read "welcome back — resume _Coding Interview_"
  banner would close the industry's weakest seam (cold returning visitor); noted, not built here.
- **2 · Discovery** — the seam from Landing must not "bait-and-switch": the hub the "Compare all paths"
  link opens shows the _same four paths_ with more detail (course counts, one-line arcs), not a
  different taxonomy. Topic-led seekers who don't want a path get "Browse the full library" → the course
  index. A shared course legitimately has several parent paths — a **polyhierarchy** — applied with
  restraint (a course appears only in the paths whose manifest actually lists it, not every path).
- **3 · Before** — readiness is **advisory, never gated**: prerequisites render as an inline list that
  points sideways ("take X first"), and experienced/re-entrant learners get an explicit skip-ahead
  (the fast-path callout lands them further down the _same_ ordered syllabus, not a separate stripped
  variant). No quiz-wall, no lock.
- **4 · During** — orientation without a login: the `PathRail` keeps the whole ordered arc beside the
  body (in the shipped drawer below `md`) with the current course marked, the `PathBanner` readout shows
  "on path: … · course k of N", the
  breadcrumb and prev/next all keep `?path=`, so the learner never falls out of path context by
  clicking forward. Deep-links/shares keep the path via the query param; opening a course with no
  `?path=` degrades to the canonical view. **[Future]** a client-only `localStorage` "mark done" +
  "k of N done" indicator (Zeigarnik re-engagement) — keyed by **course-ID alone** so completion
  **carries across every path** that shares the course (DataCamp's cross-track carry-over, done
  no-login); noted, not built here.
- **5 · After** — close the loop, don't dead-end: manifest `next` hands off to the following course;
  the terminal node is a **capstone** framed as a portfolio artifact (distinct treatment from a
  mid-path course); and `PathCourseLinks` answers "where else does this course live?" — a
  cross-path-continuity affordance the survey found **no platform** ships, so it is a deliberate
  differentiator here. **[Future]** a peak-end completion celebration (with an `aria-live`
  announcement, not color/confetti alone).

**The seams** (where journeys usually break) — Landing→Discovery keeps the same four paths visible so
information scent is preserved; Before→During turns "skip ahead" into a starting offset in the _same_
structure, not a forked variant to maintain; During→After uses one boolean per course-ID so "in
progress" and "done" are the same data model, and finishing a course in Path A registers when it
reappears in Path B; After→re-entry is the industry's weakest seam and is explicitly parked as
**[Future]** rather than hand-waved.

**Ergonomics principles (evidence-backed, applied across the journey)**

- **Choice overload is contextual, not automatic.** The canonical jam study (24 vs. 6 options) is real,
  but the largest meta-analysis ([Scheibehenne, Greifeneder & Todd 2010](https://www.psychologytoday.com/us/blog/pop-psych/201602/is-choice-overload-real-thing),
  50 studies) found a near-zero _average_ effect — overload bites mainly when the user has **no
  preexisting preference, options are hard to compare, and no heuristic/filter exists**. Screen 0's
  goal-labeled cards + escape hatch neutralize all three, so four cards in the hero is safe.
- **Hick's Law is logarithmic** (`RT = a + b·log₂n`), with **no magic-number cutoff** — the "7±2" figure
  is Miller's working-memory law, a different construct, and is not used here. [lawsofux.com/hicks-law](https://lawsofux.com/hicks-law/).
- **Polyhierarchy** — one course, a _few restrained_ parent paths, not cross-listed everywhere. [NN/g](https://www.nngroup.com/articles/polyhierarchy/).
- **Breadcrumb = location, not history** ([NN/g](https://www.nngroup.com/articles/breadcrumbs/)). NN/g's
  default is a single canonical parent; our path-aware breadcrumb is a **deliberate, documented
  departure** — justified because the active path is explicit and shareable in the URL (`?path=`), so
  the trail is deterministic _given the URL_ rather than silently referrer-driven.
- **Recognition over recall / information scent** — persistent path banner + breadcrumb so the learner
  never has to remember which path they're in. [NN/g recognition](https://www.nngroup.com/articles/recognition-and-recall/),
  [NN/g scent](https://www.nngroup.com/articles/information-scent/).
- **Zeigarnik & peak-end** (both **[Future]**) — an unfinished-count indicator drives return visits;
  completion should end on a rewarding note without an upsell. [NN/g Zeigarnik](https://www.nngroup.com/videos/zeigarnik-effect/),
  [NN/g peak-end](https://www.nngroup.com/articles/peak-end-rule/).
- **Mobile & a11y per stage** — advisory-vs-hard signifiers never color-only; tap targets ≥44px (above
  the [WCAG 2.2 §2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) 24px
  floor); no multi-line breadcrumb wrap on small screens; completion state announced via `aria-live`.

## UI-Design-Funnel (Path-Aware Navigation Screens)

The path-aware navigation adds/changes **five user-facing screens** in `ayokoding-www` (a Next.js
app): **Screen 0** is the site **landing hero** at `/en` (where a first-time visitor first meets the
paths); **Screens 1-3** live under the `/en/c/learn` URL model (paths hub, path landing,
course-in-path); **Screen 4** (added by the 2026-07-21 scope extension) is the **legacy-bucket
landing and page banner**, whose selection is pending the
[Q-D](./tech-docs.md#q-d--seo-treatment-of-legacy) ruling. Each screen runs the diverge → narrow →
select → justify funnel. Low-fidelity
wireframes are authored below; the two high-fidelity finalists per screen are rendered as `.png`
assets under this plan's [`assets/`](./assets/) and embedded inline here. Repo-grounded **textual**
hi-fi specifications for each chosen screen are authored in
[Hi-Fi Specifications](#hi-fi-specifications-textual-repo-grounded) below and are the source of truth
those PNGs render. The screens are sequenced along the [Learner Journey](#learner-journey-end-to-end)
— landing → discovery → before → during → after — so the funnel optimizes the _whole_ arc, not each
screen in isolation.

> **Assets note**: the eight hi-fi finalist PNGs (two per screen, Screens 0-3) are **already produced**
> and embedded below. They are rendered from self-contained HTML mockups (kept alongside as
> [`assets/src/*.html`](./assets/src/)) styled with the **exact AyoKoding token palette**
> (`libs/web-ui-token/src/ayokoding.css` — the same `oklch` hues, `--warm-*` neutral scale, radius,
> and shadow tokens the running app uses), so the mockups are colour- and spacing-accurate rather than
> sketches. To regenerate: serve `assets/src/` over HTTP and full-page-screenshot each page.

**R5 grounding note (all screens)** — before drafting, survey the existing UI to reuse rather than
reinvent: `libs/web-ui` component inventory + tokens + Storybook; the ayokoding app-shell
(`apps/ayokoding-www/src/features/app-shell/`); the existing `sidebar-tree`, `breadcrumb`, `prev-next`,
and `section-card` components [Repo-grounded — `apps/ayokoding-www/src/features/navigation/shell/` and
`.../content/shell/section-card.tsx`]. Reference the `swe-developing-frontend-ui` skill. **Net-new
components**: `PathCard`, `PathLanding`, `PathRail`, `PathBanner`, `PathCourseLinks`,
`PrerequisiteList` — all
composed from existing `libs/web-ui` primitives; named in
[tech-docs §New feature: `course-paths`](./tech-docs.md#new-feature-course-paths-functional-core--imperative-shell).

**R7 prior-art survey (all screens) — COMPLETE.** A `web-researcher` window-shop of 13 learning
platforms ran on **2026-07-21**; the selections below are now **prior-art-informed** (this discharges
the earlier provisional-diverge caveat). Sources and the full adopt/adapt/avoid mapping are in
[R7 Prior-Art Findings](#r7-prior-art-findings-window-shopped-2026-07-21) below. Headline results that
drove the selections:

- **No platform puts more than 3-4 large path choices in/near the hero** — the dense catalog is always
  one click deeper (roadmap.sh's 92-roadmap catalog, Codecademy's 12-path center). Our four
  goal-labeled paths sit safely under every choice-overload threshold ([Hick's Law](https://lawsofux.com/hicks-law/);
  Iyengar & Lepper's jam study), so Screen 0 puts the **4 goal cards directly in the hero** with an
  "Not sure? Compare paths" escape hatch (Boot.dev + Codecademy model).
- **Path landings are numbered flat lists + an advisory "take in order, content builds" note**, never
  a DAG diagram or 3-level nesting ([Coursera](https://www.coursera.org/professional-certificates/google-data-analytics);
  NN/g caps disclosure at [two levels](https://www.nngroup.com/articles/progressive-disclosure/)) —
  validates Screen 2 Option A.
- **Prerequisites are advisory prose, not hard gates** across every platform (Scrimba, DataCamp,
  Pluralsight's "skip modules you already know") — validates our advisory `PrerequisiteList` + the
  fast-path "skip the prologue" callout for re-entrant users.
- **A course-page path banner and a "this course is in N paths" affordance are an industry-wide
  whitespace** — no surveyed platform surfaces them ([Boot.dev](https://www.boot.dev/paths/backend-python-golang)
  path pages have no breadcrumb; Frontend Masters shows no cross-path indicator). Our `PathRail`,
  `PathBanner`, and `PathCourseLinks` are therefore **net-new differentiators**, built on the nearest
  adjacent precedents (Coursera's program breadcrumb; the persistent lesson rail every docs-style site
  ships) rather than copied.

### Screen 0 · Landing hero (path entry)

The site landing hero at `/en` ([`app-shell/shell/hero.tsx`](../../../apps/ayokoding-www/src/features/app-shell/shell/hero.tsx)

- [`landing.tsx`](../../../apps/ayokoding-www/src/features/app-shell/shell/landing.tsx)). **Today** it
  offers only two generic CTAs — **Start learning** → `/en/c` (a recall-heavy browse index of sections)
  and **Explore tools** — so a goal-driven learner ("I want to get interview-ready") has **zero path
  scent** above the fold. This screen fixes that: the hero must **surface `/paths` directly**, turning
  the landing page into the first step of the learner journey rather than a dead-drop into a taxonomy.

**Low-fi Option A — Four goal cards in the hero (Recommended)**

_Mobile — 375 px (`<sm`): one column, cards full-width_

```text
┌────────────────────────────────────┐
│ ☰  AyoKoding            ⌕  ☾       │
├────────────────────────────────────┤
│ Learn to build software,           │
│ the clear way.                     │
│ Start from your goal — every path  │
│ is one route through one library.  │
│ CHOOSE YOUR PATH                   │
│ ┌────────────────────────────────┐ │
│ │ Pass a SWE interview soon      │ │
│ │ Interview-Ready SWE      ~119  │ │
│ └────────────────────────────────┘ │
│ ┌────────────────────────────────┐ │
│ │ Get productive & ship fast     │ │
│ │ Immediately-Effective    ~116  │ │
│ └────────────────────────────────┘ │
│ ┌────────────────────────────────┐ │
│ │ Build durable fundamentals     │ │
│ │ Fundamentally Strong     ~121  │ │
│ └────────────────────────────────┘ │
│ ┌────────────────────────────────┐ │
│ │ Move from SWE into AI          │ │
│ │ SWE → AI Engineer         ~15  │ │
│ └────────────────────────────────┘ │
│ Compare all paths →                │
│ Browse the full library →          │
└────────────────────────────────────┘
```

_Tablet — 768 px (`md`): the 2×2 grid turns on (`md:grid-cols-2`)_

```text
┌────────────────────── AyoKoding · /en ───────────────────────┐
│ Learn to build software, the clear way.                       │
│ Start from your goal — one route through one library.         │
│ CHOOSE YOUR PATH                                              │
│  ┌────────────────────────┐  ┌────────────────────────┐      │
│  │ Pass a SWE interview   │  │ Get productive & ship  │      │
│  │ Interview-Ready   ~119 │  │ Immediately-Eff.  ~116 │      │
│  └────────────────────────┘  └────────────────────────┘      │
│  ┌────────────────────────┐  ┌────────────────────────┐      │
│  │ Build fundamentals     │  │ Move from SWE into AI  │      │
│  │ Fundamentally S.  ~121 │  │ SWE → AI Eng.      ~15 │      │
│  └────────────────────────┘  └────────────────────────┘      │
│  Compare all paths →        Browse the full library →         │
└───────────────────────────────────────────────────────────────┘
```

_Desktop — 1280 px (`xl`)_

```text
┌──────────────────────────── AyoKoding · /en ─────────────────────────────┐
│ Learn to build software, the clear way.                                   │
│ Start from your goal — every path is one route through one library.       │
│ CHOOSE YOUR PATH                                                          │
│  ┌───────────────────────────┐  ┌───────────────────────────┐            │
│  │ Pass a SWE interview soon │  │ Get productive & ship fast │           │
│  │ Interview-Ready SWE  ~119 │  │ Immediately-Effective ~116 │           │
│  └───────────────────────────┘  └───────────────────────────┘            │
│  ┌───────────────────────────┐  ┌───────────────────────────┐            │
│  │ Build durable fundamentals│  │ Move from SWE into AI      │           │
│  │ Fundamentally Strong ~121 │  │ SWE → AI Engineer     ~15  │           │
│  └───────────────────────────┘  └───────────────────────────┘            │
│  Not sure which fits? Compare all paths →     Browse the full library →   │
└────────────────────────────────────────────────────────────────────────────┘
```

**Low-fi Option B — Goal-question strip below a single-CTA hero (Coursera model)**

_Mobile — 375 px: the two CTAs stack, so all four goals sit below the fold_

```text
┌────────────────────────────────────┐
│ Learn to build software,           │
│ the clear way.                     │
│ [ Start learning →              ]  │
│ [ Explore tools                 ]  │
│ ────────────────────────────────── │
│ What brings you here today?        │  ← typically below the fold
│  • Pass a SWE interview soon →     │
│  • Get productive & ship fast →    │
│  • Build durable fundamentals →    │
│  • Move from SWE into AI →         │
└────────────────────────────────────┘
```

_Tablet — 768 px: CTAs sit inline; the goal strip becomes two columns_

```text
┌────────────────────── AyoKoding · /en ───────────────────────┐
│ Learn to build software, the clear way.                       │
│ [ Start learning → ]   [ Explore tools ]                      │
│ ───────────────────────────────────────────────────────────── │
│ What brings you here today?                                   │
│  • Pass a SWE interview soon →   • Get productive & ship →     │
│  • Build durable fundamentals →  • Move from SWE into AI →     │
└───────────────────────────────────────────────────────────────┘
```

_Desktop — 1280 px_

```text
┌──────────────────────────── AyoKoding · /en ─────────────────────────────┐
│ Learn to build software, the clear way.                                   │
│ [ Start learning → ]   [ Explore tools ]                                  │
│ ───────────────────────────────────────────────────────────────────────  │
│ What brings you here today?                                               │
│  • Pass a SWE interview soon →     • Get productive & ship fast →         │
│  • Build durable fundamentals →    • Move from SWE into AI →              │
└────────────────────────────────────────────────────────────────────────────┘
```

**Low-fi Option C — Single "Find your path" CTA + guided quiz (edX/Educative model)**

_Mobile — 375 px_

```text
┌────────────────────────────────────┐
│ Learn to build software,           │
│ the clear way.                     │
│ [ Find your path →              ]  │
│ (answer 3 questions)               │
│ or browse all paths →              │
└────────────────────────────────────┘
```

_Tablet — 768 px_

```text
┌────────────────────── AyoKoding · /en ───────────────────────┐
│ Learn to build software, the clear way.                       │
│ [ Find your path → ]  (answer 3 questions)                    │
│ or browse all paths →                                         │
└───────────────────────────────────────────────────────────────┘
```

_Desktop — 1280 px_

```text
┌──────────────────────────── AyoKoding · /en ─────────────────────────────┐
│ Learn to build software, the clear way.                                   │
│ [ Find your path → ]  (answer 3 questions)      or browse all paths →     │
└────────────────────────────────────────────────────────────────────────────┘
```

**Responsive (mobile ↔ desktop)** — Option A shows a **2×2 card grid** at `md+` and **stacks to one
column** below `md`; each card is a full-width tap target (≥ the WCAG 2.2 §2.5.8 24px floor, sized to
the ~48px comfort target). The "Compare all paths" / "Browse library" links wrap under the grid on
mobile. The four cards fit above the fold on desktop and within one short scroll on mobile — no card is
pushed below a fold-and-a-half the way Option B's strip is once the primary CTAs precede it.

**Hi-fi finalists** (rendered from the token-accurate HTML mockups):

![Landing hero, Option A — the AyoKoding landing page with the brand headline and tagline, then a "Choose your path" label above a 2×2 grid of four goal-led cards (Pass a SWE interview soon, Get productive and ship fast, Build durable fundamentals, Move from SWE into AI), each hue-coded with the formal path name and course count and a Start action, and a subordinate "Not sure which fits? Compare all paths" link beside "Browse the full course library"](./assets/landing-hero-option-a-desktop.png)

![Landing hero, Option B — the landing page with a single "Start learning" primary CTA and an "Explore tools" secondary button, and below a divider a "What brings you here today?" strip of four goal options each with a hue dot, following the Coursera goal-question pattern](./assets/landing-hero-option-b-desktop.png)

**Selected: Option A — four goal cards in the hero.**

| Design                      | Why it won / lost                                                                                                     |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| A — 4 goal cards in hero ✅ | Zero clicks/scroll to the core decision; strongest information scent (goal verbs + course counts); 4 ≪ overload cap   |
| B — goal-question strip     | Proven (Coursera), but the primary CTA precedes it, so path choice needs a scroll and competes with "Start learning"  |
| C — guided quiz             | Best only when paths are ambiguous; ours are already goal-labeled, and no surveyed platform uses a quiz as sole entry |

**Ergonomics rationale** — our four paths are **already goal-labeled**, so no quiz is needed to
translate intent into a route (avoids Option C's mandatory extra step). Four cards is at the low end of
every threshold surveyed ([Hick's Law](https://lawsofux.com/hicks-law/); Iyengar & Lepper 2000 jam
study; NN/g "show a few of the most important options"), so putting them **in** the hero — not one
scroll below it like Option B — removes the single friction point every "goal-question-then-cards"
platform still has. The subordinate **"Compare all paths →"** link (→ Screen 1) is the escape hatch for
undecided visitors (Codecademy's "sorting quiz alongside the grid" pattern) without diluting the
four-card decision; **"Browse the full library →"** preserves the non-path, self-directed entry
(recognition-over-recall for learners who know the topic they want). The existing **Start learning /
Explore tools** buttons are **not deleted** — they move into the global nav so the hero's primary
visual weight is the path decision.

### Screen 1 · Paths hub ("choose your path")

Entry screen at `/en/c/learn/paths` (the paths hub) offering the four paths. The fourth path converges
on a different endpoint than the other three (per-role convergence, DD-22), so the hub's copy states
"converging within your role" rather than the earlier single-endpoint framing.

**Low-fi Option A — Path cards, 2×2 grid (Recommended)**

_Mobile — 375 px (`<sm`): one column; no sidebar (it is `hidden` below `md`)_

```text
┌────────────────────────────────────┐
│ ☰  AyoKoding            ⌕  ☾       │
├────────────────────────────────────┤
│ Choose your path.                  │
│ One library, converging within     │
│ your role.                         │
│ ┌────────────────────────────────┐ │
│ │ Interview-Ready SWE            │ │
│ │ interview-first · ~N courses   │ │
│ │ [ Start →                    ] │ │
│ └────────────────────────────────┘ │
│ ┌────────────────────────────────┐ │
│ │ Immediately-Effective          │ │
│ │ build-app-first · ~N courses   │ │
│ │ [ Start →                    ] │ │
│ └────────────────────────────────┘ │
│ ┌────────────────────────────────┐ │
│ │ Fundamentally Strong           │ │
│ │ fundamentals-first · ~N        │ │
│ │ [ Start →                    ] │ │
│ └────────────────────────────────┘ │
│ ┌────────────────────────────────┐ │
│ │ SWE → AI Engineer              │ │
│ │ AI-transition-first · ~N       │ │
│ │ [ Start →                    ] │ │
│ └────────────────────────────────┘ │
│ Or browse the full library →       │
└────────────────────────────────────┘
```

_Tablet — 768 px (`md`): sidebar appears; grid goes two-up_

```text
┌── Sidebar ───┬────────────────────────────────────────────────┐
│ ▸ Learn      │ Choose your path. One library, converging       │
│   ▸ Paths    │ within your role.                               │
│   ▸ Courses  │ ┌──────────────────┐ ┌──────────────────┐      │
│   ▸ Legacy   │ │ Interview-Ready  │ │ Immediately-Eff. │      │
│              │ │ ~N · [ Start → ] │ │ ~N · [ Start → ] │      │
│              │ └──────────────────┘ └──────────────────┘      │
│              │ ┌──────────────────┐ ┌──────────────────┐      │
│              │ │ Fundamentally S. │ │ SWE → AI Eng.    │      │
│              │ │ ~N · [ Start → ] │ │ ~N · [ Start → ] │      │
│              │ └──────────────────┘ └──────────────────┘      │
│              │ Or browse the full course library →             │
└──────────────┴────────────────────────────────────────────────┘
```

_Desktop — 1280 px (`xl`)_

```text
┌────────────────────────── Fundamentally Strong · Learn ──────────────────────────┐
│  Choose your path. One library, converging within your role.                      │
│                                                                                    │
│  ┌────────────────────┐  ┌────────────────────┐                                   │
│  │ Interview-Ready SWE │  │ Immediately-Effect. │                                  │
│  │ Interview-first     │  │ Build-app-first     │                                  │
│  │ Get interview-ready │  │ Ship a real app     │                                  │
│  │ fast (re-entrant).  │  │ fast, then deepen.  │                                  │
│  │ ~N courses          │  │ ~N courses          │                                  │
│  │ [ Start → ]         │  │ [ Start → ]         │                                  │
│  └────────────────────┘  └────────────────────┘                                   │
│  ┌────────────────────┐  ┌────────────────────┐                                   │
│  │ Fundamentally Strong│  │ SWE → AI Engineer   │                                  │
│  │ Fundamentals-first  │  │ AI-transition-first │                                  │
│  │ CS theory first,    │  │ Already a SWE? Build│                                  │
│  │ then deepen.        │  │ AI systems, fast.    │                                 │
│  │ ~N courses          │  │ ~N courses           │                                 │
│  │ [ Start → ]         │  │ [ Start → ]          │                                 │
│  └────────────────────┘  └────────────────────┘                                   │
│                                                                                    │
│  Or browse the full course library →                                               │
└────────────────────────────────────────────────────────────────────────────────────┘
```

**Low-fi Option B — Stacked comparison rows**

_Mobile — 375 px: each row wraps to three lines, pushing the fourth path far below the fold_

```text
┌────────────────────────────────────┐
│ Interview-Ready SWE                │
│ interview-first · ~N courses       │
│ [ Start → ]                        │
│ ────────────────────────────────── │
│ Immediately-Effective              │
│ build-app-first · ~N courses       │
│ [ Start → ]                        │
│ ────────────────────────────────── │
│ Fundamentally Strong               │
│ fundamentals-first · ~N courses    │
│ [ Start → ]                        │
│ ────────────────────────────────── │
│ SWE → AI Engineer                  │  ← ~3 screens down
│ AI-transition-first · ~N courses   │
│ [ Start → ]                        │
└────────────────────────────────────┘
```

_Tablet — 768 px: rows fit on two lines each; still a vertical ranking_

```text
┌── Sidebar ───┬────────────────────────────────────────────────┐
│ ▸ Learn      │ Interview-Ready SWE (interview-first)  ~N       │
│              │   interview prep → production → deeper  [Start]│
│              │ ──────────────────────────────────────────────  │
│              │ Immediately-Effective (build-app-first) ~N      │
│              │   editor → one language → BUILD → deepen [Start]│
│              │ ──────────────────────────────────────────────  │
│              │ Fundamentally Strong … / SWE → AI Engineer …    │
└──────────────┴────────────────────────────────────────────────┘
```

_Desktop — 1280 px_

```text
┌───────────────── Fundamentally Strong · Four Paths ──────────────────┐
│ Interview-Ready SWE (interview-first) [ Start → ]  ~N courses         │
│   interview prep → production-effective → deeper                      │
│ ────────────────────────────────────────────────────────────────────│
│ Immediately-Effective (build-app-first) [ Start → ]  ~N courses      │
│   editor → one language → BUILD APP → deepen                         │
│ ────────────────────────────────────────────────────────────────────│
│ Fundamentally Strong (fundamentals-first) [ Start → ]  ~N courses    │
│   CS foundations → architecture → paradigms → DS&A → build           │
│ ────────────────────────────────────────────────────────────────────│
│ SWE → AI Engineer (AI-transition-first) [ Start → ]  ~N courses      │
│   already a SWE → build AI systems (models, agents, evals) fast      │
└───────────────────────────────────────────────────────────────────────┘
```

**Responsive (mobile ↔ desktop)** — Option A shows a **2×2 grid** of four cards at `lg` (≥1024px),
two-up at `md` (≥768px), and **stacks to one column** below `sm`. The "Start" CTA is a full-width tap
target on mobile.

**Hi-fi finalists** (rendered from the token-accurate HTML mockups):

![Paths hub, Option A — four equal path cards in a 2×2 grid, each with a hue-coded top border, a kind badge, the path name, its one-line arc, a course-count badge, and a Start call-to-action](./assets/paths-hub-option-a-desktop.png)

![Paths hub, Option B — the four paths as stacked full-width comparison rows, each with a hue accent bar, name, kind badge, arc summary, course count, and Start action](./assets/paths-hub-option-b-desktop.png)

**Selected: Option A — Path cards, 2×2 grid.**

| Design                 | Why it won / lost                                                                          |
| ---------------------- | ------------------------------------------------------------------------------------------ |
| A — 2×2 card grid ✅   | Four equal, scannable choices; reuses `section-card`; reflows cleanly to stacked mobile    |
| B — stacked comparison | Denser, but buries the fourth path further below the fold on mobile and reads as a ranking |

### Screen 2 · Path landing page

At `/en/c/learn/paths/<path-id>` — the manifest rendered as an ordered, phase-grouped course list;
every course link carries `?path=<path-id>`. The ordering is a valid topological entry into the
prerequisite DAG.

**Low-fi Option A — Phase-grouped numbered syllabus (Recommended)**

_Mobile — 375 px: one course per row, phase headings inline (never sticky — sticky is `lg+`)_

```text
┌────────────────────────────────────┐
│ ☰  AyoKoding            ⌕  ☾       │
├────────────────────────────────────┤
│ Interview-Ready SWE                │
│ interview-first                    │
│ ⓘ Experienced & job-hunting?       │
│   Skip the prologue → Phase 1.     │
│ PROLOGUE · EDITOR (skippable)      │
│   1. Just Enough Nvim              │
│   2. Just Enough Lua               │
│   3. Extending Neovim              │
│   ▸ Capstone · Forge-Ready         │
│ PHASE 1 · INTERVIEW PREPARATION    │
│   4. Just Enough Python            │
│   …                                │
│   9. Coding Interview              │
└────────────────────────────────────┘
```

_Tablet — 768 px: sidebar returns; list stays one column, phase headings still inline_

```text
┌── Sidebar ───┬────────────────────────────────────────────────┐
│ ▸ Learn      │ Interview-Ready SWE · interview-first           │
│   ▾ Paths    │ ⓘ Skip the prologue → jump to Phase 1.          │
│   ▸ Courses  │ PROLOGUE · EDITOR FOUNDATIONS (skippable)        │
│              │   1. Just Enough Nvim   2. Just Enough Lua      │
│              │   3. Extending Neovim   ▸ Capstone · Forge-Ready│
│              │ PHASE 1 · INTERVIEW PREPARATION                  │
│              │   4. Just Enough Python … 9. Coding Interview   │
└──────────────┴────────────────────────────────────────────────┘
```

_Desktop — 1280 px: `max-w-3xl` reading column; phase headings sticky (`lg:sticky lg:top-16`)_

```text
┌──────────── Interview-Ready Software Engineer · interview-first ─────────┐
│ Experienced & job-hunting? Skip the prologue → jump to Phase 1.          │
│                                                                          │
│ Prologue · Editor Foundations (skippable)                               │
│   1. Just Enough Nvim        2. Just Enough Lua     3. Extending Neovim  │
│   ▸ Capstone · Forge-Ready                                               │
│ Phase 1 · Interview Preparation                                         │
│   4. Just Enough Python …  9. Coding Interview  … 16. Behavioral        │
│   ▸ Capstone · Interview Loop                                           │
│ Phase 2 · Production-Effective …                                        │
│ Phase 3 · Deepening …                                                   │
└──────────────────────────────────────────────────────────────────────────┘
```

**Low-fi Option B — Collapsible phase accordion**

_Mobile — 375 px: all stages collapsed except the first — the arc is hidden_

```text
┌────────────────────────────────────┐
│ Fundamentally Strong SWE           │
│ ▼ Stage 1 · CS foundations   (N)   │
│     1. Just Enough Git             │
│     2. Computer Systems            │
│ ▶ Stage 2 · Paradigms, DS&A  (N)   │
│ ▶ Stage 3 · Build real SW    (N)   │
│ ▶ Stage 4 · Systems & ops    (N)   │
└────────────────────────────────────┘
```

_Tablet — 768 px: two stages expanded_

```text
┌── Sidebar ───┬────────────────────────────────────────────────┐
│ ▸ Learn      │ ▼ Stage 1 · CS foundations & architecture  (N)  │
│              │ ▼ Stage 2 · Paradigms, DS&A, algorithms    (N)  │
│              │ ▶ Stage 3 · Build real software (collapsed)     │
│              │ ▶ Stage 4 · Systems, data, security, ops        │
└──────────────┴────────────────────────────────────────────────┘
```

_Desktop — 1280 px_

```text
┌──────────── Fundamentally Strong SWE · fundamentals-first ──────────────┐
│ ▼ Stage 1 · CS foundations & architecture       (N courses)             │
│ ▼ Stage 2 · Paradigms, DS&A, algorithms          (N courses)            │
│ ▶ Stage 3 · Build real software (collapsed)                             │
│ ▶ Stage 4 · Systems, data, security, ops (collapsed)                    │
└──────────────────────────────────────────────────────────────────────────┘
```

**Responsive (mobile ↔ desktop)** — Option A renders the numbered list full-width single-column on
mobile (each course a full-width row) and a comfortable reading column on desktop; the fast-path
callout stays pinned at the top. Phase headings are sticky sub-headers on desktop, inline on mobile.
Option B's accordion collapses all but the first stage on mobile to keep the list short.

**Hi-fi finalists** (rendered from the token-accurate HTML mockups):

![Path landing, Option A — a hue strip header with the path title and arc, an info callout to skip the prologue, then phase-grouped sections each rendering a numbered ordered list of course rows where the number is the path order, with capstone markers](./assets/path-landing-option-a-desktop.png)

![Path landing, Option B — the syllabus as collapsible phase accordions, the first two stages expanded to show course rows and the remaining stages collapsed with course counts](./assets/path-landing-option-b-desktop.png)

**Selected: Option A — Phase-grouped numbered syllabus.**

| Design                   | Why it won / lost                                                                   |
| ------------------------ | ----------------------------------------------------------------------------------- |
| A — numbered syllabus ✅ | Shows the whole ordered arc at a glance; the number IS the path order; SEO-friendly |
| B — phase accordion      | Compact, but hides the arc behind collapsed sections and adds interaction cost      |

### Screen 3 · Course page in path context

A shared course body rendered with the active path's affordances: the active path's **ordered course
list** as the left rail, a path breadcrumb, a **prerequisite list**, and manifest-driven prev/next.
Without `?path=` → canonical view (generic content-tree sidebar, which still surfaces prerequisites).

**Low-fi Option A — Top path banner + path breadcrumb + prerequisites + bottom prev/next**

_Mobile — 375 px (`<sm`)_

```text
┌────────────────────────────────────┐
│ ☰  AyoKoding            ⌕  ☾       │
├────────────────────────────────────┤
│ ▸ On path: Interview-Ready SWE     │
│   course 9 of N   [view full path] │
│ Home / … / Coding Interview        │
│ Prereqs: DS&A · Advanced Algos     │
│                                    │
│ # Coding Interview                 │
│ …body (unchanged, path-neutral)…   │
│                                    │
│ ← Prev: Advanced Algorithms        │
│ Next: Take-Home & Live Coding →    │
└────────────────────────────────────┘
```

_Tablet — 768 px (`md`)_

```text
┌── Sidebar (content tree) ─┬──────────────────────────────────────┐
│ ▸ Learn                   │ ▸ On path: Interview-Ready SWE ·      │
│   ▸ Paths                 │   course 9 of N     [view full path] │
│   ▾ Courses               │ Home / … / Coding Interview           │
│     · Advanced Algorithms │ Prereqs: DS&A · Advanced Algorithms   │
│     · Coding Interview    │ # Coding Interview … body …           │
│   ▸ Legacy                │ ← Prev: Advanced Algos   Next: … →    │
└───────────────────────────┴──────────────────────────────────────┘
```

_Desktop — 1280 px (`xl`)_

```text
┌── Sidebar ────┬──────────────────────────────────────────────────────────────────────────┐
│ ▸ Learn       │ ▸ On path: Interview-Ready SWE · course 9 of N       [ view full path ]   │
│   ▸ Paths     │ Home / Learn / Interview-Ready SWE / Coding Interview                     │
│   ▾ Courses   │ Prerequisites: Data Structures & Algorithms · Advanced Algorithms         │
│     · Adv Alg │                                                                          │
│     · Coding  │ # Coding Interview                                                        │
│   ▸ Legacy    │ …course body (unchanged, canonical, path-neutral)…                        │
│               │                                                                          │
│               │ ← Prev: Advanced Algorithms        Next: Take-Home & Live Coding →        │
│               │   (both links keep ?path=interview-ready/software-engineer)               │
└───────────────┴──────────────────────────────────────────────────────────────────────────┘
```

**Low-fi Option B — Left path rail replacing the sidebar (SELECTED)**

The rail is the same `<aside>` slot the generic content-tree sidebar occupies today; only its
**contents** swap when `?path=` is present. Below `md` that slot does not exist at all — the tree
already lives in the shipped left `Sheet` drawer — so the rail collapses into the **same drawer**, and
the banner strip is retained as its always-visible compact readout.

_Mobile — 375 px (`<sm`): rail collapsed into the shipped drawer; banner strip is the readout_

```text
┌────────────────────────────────────┐
│ ☰  AyoKoding            ⌕  ☾       │   ← ☰ = "Open navigation menu"
├────────────────────────────────────┤
│ ▸ Interview-Ready SWE · 9 of N  ⌄  │   ← tap ⌄ = "Open path course list"
│ Home / … / Coding Interview        │
│ Prereqs: DS&A · Advanced Algos     │
│ # Coding Interview  …body…         │
│ ← Prev …            Next … →       │
└────────────────────────────────────┘
  ⌄ opens the SAME left drawer, path-scoped:
┌──────────────────────┬─────────────┐
│ Interview-Ready SWE ✕│  (scrim)    │
│  8  Data Structures  │             │
│ ▸9  Coding Interview │             │
│ 10  Take-Home & Live │             │
│ 11  System Design    │             │
│  [ view full path → ]│             │
└──────────────────────┴─────────────┘
```

_Tablet — 768 px (`md`): rail present at the panel's 15 % floor (~115 px) — number + truncated title_

```text
┌── Path rail ─┬───────────────────────────────────────────────────┐
│ Interview-R… │ Home / Learn / Interview-Ready SWE / Coding Int…   │
│  8 Data Str… │ Prereqs: DS&A · Advanced Algorithms                │
│ ▸9 Coding I… │ # Coding Interview … body …                        │
│ 10 Take-Hom… │ ← Prev: Advanced Algos        Next: Take-Home →    │
│ 11 System D… │   (both links keep ?path=…)                        │
│ [full path →]│                                                    │
└──────────────┴───────────────────────────────────────────────────┘
```

_Desktop — 1280 px (`xl`): rail at its resizable default; full titles + phase grouping_

```text
┌── Path rail ───────────┬─────────────────────────────────────────────────────────┐
│ Interview-Ready SWE    │ Home / Learn / Interview-Ready SWE / Coding Interview    │
│ course 9 of N          │ Prerequisites: Data Structures & Algorithms ·            │
│ ── PHASE 2 · PRACTICE ─│               Advanced Algorithms                        │
│   8  Data Structures   │                                                         │
│ ▸ 9  Coding Interview ●│ # Coding Interview                                       │
│  10  Take-Home & Live  │ …course body (unchanged, canonical, path-neutral)…       │
│ ── PHASE 3 · DESIGN ───│                                                         │
│  11  System Design     │ ← Prev: Advanced Algorithms   Next: Take-Home & Live →   │
│ [ view full path → ]   │   (both links keep ?path=interview-ready/software-engineer)│
└────────────────────────┴─────────────────────────────────────────────────────────┘
```

Canonical fallback (no `?path=`, all breakpoints) — the rail slot reverts to the **generic
content-tree sidebar exactly as it renders today**; nothing about the no-path reader's experience
changes:

```text
┌── Sidebar (unchanged) ─┬─────────────────────────────────────────────────────────┐
│ ▸ Learn                │ Home / Learn / Courses / Coding Interview                │
│   ▸ Paths              │ Prerequisites: Data Structures & Algorithms ·            │
│   ▾ Courses            │               Advanced Algorithms                        │
│   ▸ Legacy             │ # Coding Interview … body …                              │
│                        │ This course is part of: [ Interview-Ready ] ·            │
│                        │   [ Immediately-Effective ] · [ Fundamentally Strong ]   │
└────────────────────────┴─────────────────────────────────────────────────────────┘
```

`coding-interview` shows only three badges because the `software-engineer-to-ai-engineer` path
**links** rather than includes SWE-fundamentals courses in its manifest (DD-24); the affordance
generically renders **one badge per path whose `courseOrder` actually lists the course**, so an
AI-specific course would instead show a single `[ SWE → AI Engineer ]` badge.

#### Screen 3 responsive specification (the selected Option B, breakpoint by breakpoint)

Choosing B **obligates this plan to design the very thing the earlier rationale used to reject it**.
That specification is below; the accepted cost is recorded in the decision table that follows.

| Breakpoint                      | What the path rail does                                                                                                                                                                                                                                                                                                                                                                                                               |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mobile `<md`** (<768)         | The `<aside>` is `hidden` [Repo-grounded — `resizable-sidebar.tsx` L46 `hidden … md:block`], so there is **no rail**. The path's ordered list moves into the **already-shipped left `Sheet` drawer** that renders `SidebarTree` today; the `PathBanner` strip stays as the always-visible readout and gains a disclosure trigger.                                                                                                     |
| **Tablet `md`–`lg`** (768-1023) | Rail occupies the `<aside>`, which is live from `md` up. `ResizablePanel`'s band is **15 %-35 % of viewport** [Repo-grounded — `MIN_WIDTH_PCT`/`MAX_WIDTH_PCT`], i.e. **~115-269 px** at 768: rows render as `<number> <truncated title>` with the full title in the link's `aria-label`. Phase separators collapse to a thin rule (no phase label). The right TOC rail is `hidden xl:block`, so there is never a three-column crush. |
| **Desktop `lg+`** (≥1024)       | Rail at the reader's persisted width (**~192-448 px** at 1280): full course titles, phase-group separators with labels, `course k of N` header, and the `view full path →` footer link.                                                                                                                                                                                                                                               |

**Collapse affordance below `md` — the shipped left drawer, not a new pattern.** This is the single
decisive fact that overturns the old objection: the "mobile sheet" B was rejected for needing **already
exists and is in production** — `apps/ayokoding-www/src/features/app-shell/shell/mobile-nav.tsx` renders
`SidebarTree` inside `Sheet` / `SheetContent side="left"` with persisted preset widths, opened from the
header's `aria-label="Open navigation menu"` button [Repo-grounded — `mobile-nav.tsx`, `header.tsx` L34].
The path rail therefore reuses that drawer with a **content swap**, exactly as it reuses the desktop
`<aside>`. Chosen over the two alternatives:

- **Bottom sheet** (a second, different overlay) — rejected: a second sheet idiom in one app, and the
  existing `Sheet` is already `side="left"`.
- **In-flow disclosure under the banner** — rejected: it would push the H1 below the fold on a phone
  when the path has 20+ courses, and it duplicates a list the drawer already shows.

**Trigger** — a `<button>` inside the `PathBanner` strip, accessible name **"Open path course list —
Interview-Ready SWE, course 9 of N"**, carrying `aria-expanded` + `aria-controls` pointed at the drawer;
the existing header `☰` continues to open the same drawer (path-scoped when `?path=` is present, generic
otherwise). **Dismiss** — Radix `Dialog` semantics inherited from `Sheet`: `Esc`, scrim click, the
drawer's own `✕`, and route change (`onOpenChange(false)` on link click, as `MobileNav` already does).
**Focus** — also inherited: focus moves into the drawer on open, is trapped while open, and returns to
the trigger on close; no new focus machinery is written.

**Reconciliation with the shipped `ResizableSidebar` — reuse, not replace, not coexist.** "Replacing the
sidebar" means replacing its **contents**, not the component. `ResizableSidebar` keeps owning the
`<aside>` shell, the `md:block` gate, the drag/keyboard resize handle, and the persisted width; only its
`children` change from `<Sidebar>` (content tree) to `<PathRail>` when a `?path=` is present. Consequences,
stated explicitly:

- **With `?path=`** — the reader sees the path's ordered courses **instead of** the content tree, at the
  same width, with the same resize handle and the same `localStorage` width key.
- **Without `?path=`** — byte-identical to today: `ResizableSidebar` + `Sidebar` + `SidebarTree`. No
  regression surface for the majority of pages.
- **Escape hatch** — the rail footer carries `view full path →` (→ the path landing) and
  `browse all courses →` (→ `/en/c/learn/courses`), so a reader is never trapped inside a path with no
  route back to the generic tree.

**A11y (the rail is a navigation landmark).** `<nav aria-label="Interview-Ready SWE course list">`
wrapping a semantic `<ol>` — the visible number **is** the list semantics, matching Screen 2's syllabus.
The current course carries `aria-current="page"` **and** a text/shape signal, never colour alone (WCAG AA
1.4.1): a `▸` marker plus `font-semibold` plus the `bg-accent` row fill. Keyboard order is
header → rail (`<nav>` in DOM order before `<article>`, reachable by the existing skip-link's sibling
route) → content → prev/next; within the rail, plain `Tab` order follows course order with the canonical
`focus-visible:ring-2 focus-visible:ring-ring`. The mobile trigger's accessible name is the full string
above (not "Menu" or an icon alone), and the drawer's `SheetTitle` becomes the path name so the dialog is
announced with a meaningful label.

**Hi-fi finalists** (desktop renders; the mobile and tablet renders are produced by the delivery steps in
[Phase 1 · Design assets](./delivery.md) — see the [asset matrix](#hi-fi-asset-matrix-screen--option--viewport)):

![Course in path, Option A at desktop width — a hue-washed top path banner reading On path with course position and a view-full-path link, a path breadcrumb, an inline prerequisites line with linked prerequisites, the unchanged course body, and a manifest-driven prev/next pair that keeps the path query parameter](./assets/course-path-option-a-desktop.png)

![Course in path, Option B at desktop width — a left path rail in the resizable sidebar slot listing the path's ordered courses grouped by phase, the current course marked with a triangle and a filled row, alongside the course body, breadcrumb, prerequisites, and prev/next](./assets/course-path-option-b-desktop.png)

**Selected: Option B — Left path rail replacing the sidebar.**

The earlier draft of this plan selected Option A and rejected B on mobile-first grounds, in these words:
_"Option B's left rail is desktop-only and would need to collapse into a top sheet on mobile — extra
complexity, so Option A wins on mobile-first grounds."_ That objection is **not deleted here** — it is
**answered and its residual cost accepted deliberately**: (a) the mobile sheet is not extra complexity
because it is already shipped and already renders the same tree component, so the collapse is a content
swap rather than new overlay machinery; (b) what remains genuinely more expensive than A is the rail
itself (a net-new `PathRail` component, a conditional `ResizableSidebar` child, and truncation behaviour
at the 15 % width floor) — that cost is accepted in exchange for continuous path orientation instead of a
one-line position readout. A later reader should see this as a trade made with eyes open, not as an
objection that was quietly dropped.

| Design                | Why it won / lost                                                                                                                                                                                                                   |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| B — left path rail ✅ | The **whole ordered arc stays visible** while reading, so "where am I / what's next / what did I skip" needs no navigation; reuses the shipped `ResizableSidebar` shell **and** the shipped mobile `Sheet` — no new overlay pattern |
| A — top banner        | Cheaper and untouched-layout, but a one-line "course 9 of N" readout gives position without context; the reader must leave the page to see the arc. Its banner strip survives inside B as the rail's compact readout                |

**What B inherits from A (recorded explicitly, so the selection is not read as a clean sweep).** B keeps
A's `PathBanner` strip, path-aware `Breadcrumb`, `PrerequisiteList`, and manifest-driven `PrevNext`
verbatim. The strip is demoted from "the design" to "the rail's always-visible compact readout", which is
what makes B viable below `md`. Net component delta versus A: **one** net-new component (`PathRail`) plus
one conditional prop on `ResizableSidebar`.

### Screen 4 · Legacy-bucket landing and page banner (scope extension)

**Added 2026-07-21 by the whole-section IA revamp.** The `legacy/` bucket introduces one new landing
(`/en/c/learn/legacy`) and, under [Q-D](./tech-docs.md#q-d--seo-treatment-of-legacy)'s recommended
answer, a per-page **"legacy / superseded"** banner on relocated pages. Both are user-facing, so they
run the funnel like Screens 0-3 — with one honest difference recorded up front: **the selection is
pending the Q-D ruling.** The low-fi alternatives below map 1:1 to Q-D's options, and the two hi-fi
finalists are produced by a `delivery.md` Phase 5A step (matching the pattern Phase 1 uses for
Screens 0-3), not fabricated here for an undecided design.

**R5 grounding note** — no net-new component is required. The banner is the existing composite
`Alert` (`Alert` / `AlertTitle` / `AlertDescription` from `@open-sharia-enterprise/web-ui`, the same
primitive [Screen 2's fast-path callout](#screen-2--path-landing-page) uses); the landing is an
ordinary content `_index.md` rendered by the existing `/c/[...slug]` route with the existing
`Breadcrumb` + `MarkdownRenderer` [Repo-grounded — `apps/ayokoding-www/src/app/[locale]/(content)/c/[...slug]/page.tsx`].
**Zero new components; zero navigation code changes** (DD-44).

**Low-fi Option A — Indexed, with a landing notice + a per-page banner (Recommended; Q-D option A)**

_Mobile — 375 px: domain links single-column; banner above the H1 so it survives the fold_

```text
┌────────────────────────────────────┐
│ Home / … / Legacy                  │
│ # Legacy material                  │
│ ⓘ Older material kept for          │
│   reference while the course       │
│   library fills. Where a course    │
│   exists, it supersedes this.      │
│   → Browse the course library      │
│   → Choose a path                  │
│ • Software Engineering             │
│ • Artificial Intelligence          │
│ • Information Security             │
│ • Personal Development             │
│ • IT Governance                    │
│ • Business                         │
└────────────────────────────────────┘
┌──── a relocated page (375 px) ─────┐
│ Home / … / Business / <title>      │
│ ⓘ Legacy — superseded by           │
│   [Course Name]                    │  ← link wraps to its own line
│ # <title>   …body unchanged…       │
└────────────────────────────────────┘
```

_Tablet — 768 px: two-column domain list (`md:grid-cols-2`); notice on two lines_

```text
┌── Sidebar ───┬────────────────────────────────────────────────┐
│ ▸ Learn      │ Home / Browse / Learn / Legacy                  │
│   ▸ Paths    │ # Legacy material                               │
│   ▸ Courses  │ ⓘ Older material kept for reference while the   │
│   ▾ Legacy   │   library fills. → library   → paths            │
│              │ • Software Engineering   • Personal Development │
│              │ • Artificial Intelligence • IT Governance       │
│              │ • Information Security   • Business             │
└──────────────┴────────────────────────────────────────────────┘
```

_Desktop — 1280 px_

```text
┌──────────────── /en/c/learn/legacy ─────────────────────────────────────┐
│ Home / Browse / Learn / Legacy                                           │
│ # Legacy material                                                        │
│ ⓘ Older material kept for reference while the course library fills.      │
│   Where a canonical course exists, it supersedes the page here.          │
│   → Browse the course library   → Choose a path                          │
│ • Software Engineering   • Artificial Intelligence  • Information Sec.   │
│ • Personal Development   • IT Governance            • Business           │
└──────────────────────────────────────────────────────────────────────────┘
┌──────────── a relocated page, e.g. …/legacy/business/… ─────────────────┐
│ Home / Browse / Learn / Legacy / Business / <title>                      │
│ ⓘ Legacy — superseded by [Course Name] ·  (link omitted when none)       │
│ # <title>   …body unchanged…                                            │
└──────────────────────────────────────────────────────────────────────────┘
```

**Low-fi Option B — Indexed, landing notice only, no per-page banner (Q-D option B)**

_Mobile — 375 px: a search-landed reader sees no signal at all on the page they arrive at_

```text
┌────────────────────────────────────┐
│ # Legacy material                  │
│ ⓘ Older material kept for          │
│   reference.                       │
│ • Software Engineering             │
│ • Artificial Intelligence  • …     │
└────────────────────────────────────┘
┌──── a relocated page (375 px) ─────┐
│ Home / … / Business / <title>      │
│ # <title>   …body, no banner…      │  ← no legacy signal
└────────────────────────────────────┘
```

_Tablet — 768 px_

```text
┌── Sidebar ───┬────────────────────────────────────────────────┐
│ ▾ Legacy     │ # Legacy material                               │
│              │ ⓘ Older material kept for reference.            │
│              │ • Software Engineering   • Personal Development │
│              │ • Artificial Intelligence • …                   │
└──────────────┴────────────────────────────────────────────────┘
```

_Desktop — 1280 px_

```text
┌──────────────── /en/c/learn/legacy ─────────────────────────────────────┐
│ # Legacy material                                                        │
│ ⓘ Older material kept for reference.                                     │
│ • Software Engineering   • Artificial Intelligence  • …                  │
└──────────────────────────────────────────────────────────────────────────┘
┌──────────── a relocated page ───────────────────────────────────────────┐
│ Home / Browse / Learn / Legacy / Business / <title>                      │
│ # <title>   …body unchanged, no banner…                                 │
└──────────────────────────────────────────────────────────────────────────┘
```

**Low-fi Option C — `noindex` the bucket, minimal landing (Q-D option C)**

_Mobile — 375 px_

```text
┌────────────────────────────────────┐
│ # Legacy material                  │
│ (not indexed; reachable from       │
│  in-site nav only)                 │
│ • Software Engineering             │
│ • Artificial Intelligence  • …     │
└────────────────────────────────────┘
```

_Tablet — 768 px_

```text
┌── Sidebar ───┬────────────────────────────────────────────────┐
│ ▾ Legacy     │ # Legacy material  (robots: noindex)            │
│              │ • Software Engineering   • Personal Development │
│              │ • Artificial Intelligence • …                   │
└──────────────┴────────────────────────────────────────────────┘
```

_Desktop — 1280 px_

```text
┌──────────────── /en/c/learn/legacy  (robots: noindex) ──────────────────┐
│ # Legacy material  (not indexed; reachable from in-site nav only)        │
│ • Software Engineering   • …                                            │
└──────────────────────────────────────────────────────────────────────────┘
```

**Responsive (mobile ↔ desktop)** — mobile-first. The landing's six domain links render as a
**single-column stacked list** below `md` and a **two-column list** at `md+` (≥768 px); they never
become a card grid, because they are navigational links into an archive, not promoted destinations
competing with the four path cards. The `Alert` notice is full-width at every breakpoint, wrapping to
three lines on mobile and one to two on desktop. The per-page banner (Option A) sits **above** the H1
and **below** the breadcrumb at every breakpoint, so it is never pushed off a phone's first screen;
its "superseded by" link wraps to its own line below `sm` rather than truncating. The breadcrumb gains
one segment (`Legacy`) — on mobile the existing `Breadcrumb` already handles overflow, and the
verification step in Phase 5A explicitly checks for **no multi-line breadcrumb wrap at 375 px**
(the ergonomics constraint already stated in the [Learner Journey](#learner-journey-end-to-end)).

**Hi-fi finalists** — produced by `delivery.md` Phase 5A as **six** files following the
[asset matrix](#hi-fi-asset-matrix-screen--option--viewport) scheme —
`assets/legacy-landing-option-{a,b}-{mobile,tablet,desktop}.png`, rendered at 375 / 768 / 1280 px from
token-accurate HTML mockups under [`assets/src/`](./assets/src/), exactly as the Screen 0-3 finalists
are. Option C is not carried to hi-fi: it is Option B's landing with a `robots` metadata change, which
a mockup cannot show.

**Selection: PENDING the [Q-D](./tech-docs.md#q-d--seo-treatment-of-legacy) ruling.** Option A is the
recommendation carried into Phase 5A. The rationale table records why each option would win or lose,
so an overturned ruling is a bounded edit rather than a re-run of the funnel:

| Design                                        | Why it would win / lose                                                                                                                                          |
| --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A — indexed + landing notice + page banner ⭐ | Preserves ~1,148 pages of search surface **and** warns the reader per page; reuses `Alert`; reversible to C in one metadata change                               |
| B — indexed, landing notice only              | Cheapest, but a search-landed reader never reaches the landing, so the one place the warning lives is the one place they never see                               |
| C — `noindex` the bucket                      | Cleanest signal that the material is superseded, but discards the app's largest search surface **before** the 127-course catalog exists (~37 bodies built today) |

**A11y (all options)** — the notice and banner are semantic `Alert` regions with real text, never
colour alone; "Legacy" is a text breadcrumb segment, not an icon; the "superseded by" link names the
destination course explicitly rather than reading "here".

### Hi-fi asset matrix (screen × option × viewport)

Every screen's every option carries a wireframe **and** a rendered mockup at **three viewports** —
mobile-first, not one desktop drawing with a prose footnote about phones.

**Naming scheme** — `assets/<screen>-option-<a|b>-<mobile|tablet|desktop>.png`, rendered from a
token-accurate source at `assets/src/<same-stem>.html`. Screen slugs: `landing-hero` (0), `paths-hub`
(1), `path-landing` (2), `course-path` (3), `legacy-landing` (4). The eight pre-existing desktop
renders were renamed into this scheme (`…-option-a.png` → `…-option-a-desktop.png`) so the set is
uniform; every `![]()` reference was updated with them.

**Render widths** — exactly the three in the shared design legend: **375 px** (mobile, below `sm`),
**768 px** (tablet, `md`), **1280 px** (desktop, `xl`). Identical across all five screens, and identical
to the widths the plan's Playwright verification steps resize to.

**Format** — `.png` only, per the
[UI Mockups convention](../../../repo-governance/conventions/formatting/diagrams/ui-mockups-principles-and-scope.md#ui-mockups-in-plan-docs-principles-in-practice-and-scope):
`.excalidraw.svg` is ruled out (GitHub blocks the Excalidraw font) and inline HTML+CSS is ruled out
(GitHub strips styles). The `.html` sources are build inputs, never the embedded artefact.

**Alt text** — each image gets its own descriptive alt text naming **what differs at that width**
(stacked vs. 2×2, rail present vs. collapsed-into-drawer, truncated vs. full titles). Copying the
desktop alt text onto the mobile render is a defect, not a shortcut.

| Screen           | Option A stem               | Option B stem               | Viewports produced        | Status                               |
| ---------------- | --------------------------- | --------------------------- | ------------------------- | ------------------------------------ |
| 0 Landing hero   | `landing-hero-option-a-*`   | `landing-hero-option-b-*`   | mobile / tablet / desktop | desktop on disk; 2 pending (Phase 1) |
| 1 Paths hub      | `paths-hub-option-a-*`      | `paths-hub-option-b-*`      | mobile / tablet / desktop | desktop on disk; 2 pending (Phase 1) |
| 2 Path landing   | `path-landing-option-a-*`   | `path-landing-option-b-*`   | mobile / tablet / desktop | desktop on disk; 2 pending (Phase 1) |
| 3 Course in path | `course-path-option-a-*`    | `course-path-option-b-*`    | mobile / tablet / desktop | desktop on disk; 2 pending (Phase 1) |
| 4 Legacy landing | `legacy-landing-option-a-*` | `legacy-landing-option-b-*` | mobile / tablet / desktop | all 6 pending (Phase 5A)             |

**Total: 5 screens × 2 options × 3 viewports = 30 `.png`** — 8 on disk, 16 produced in
[Phase 1](./delivery.md), 6 in Phase 5A. The delivery checklist enumerates them **one checkbox per
asset** rather than one coarse "render all mockups" step, because the volume is large enough that a
single checkbox could be ticked with most of the set missing.

### Hi-Fi Specifications (Textual, Repo-Grounded)

These **textual hi-fi specifications** are the source of truth the embedded `.png` finalists render —
they pin the **selected option of each screen** to concrete, existing design-system facts so both the
mockups and the Group-A/B build have an unambiguous target. The selections are **not uniformly Option
A**: Screens 0, 1, and 2 selected Option A; **Screen 3 selected Option B** (left path rail — see
[Screen 3](#screen-3--course-page-in-path-context)); Screen 4's selection is pending the
[Q-D](./tech-docs.md#q-d--seo-treatment-of-legacy) ruling. Every primitive, token, and class named
below is **repo-grounded** in `@open-sharia-enterprise/web-ui` (barrel) /
`@open-sharia-enterprise/web-ui/primitives` and the AyoKoding token layer (`libs/web-ui-token`,
`apps/ayokoding-www/src/app/globals.css`), verified against the existing `prev-next`, `breadcrumb`,
`section-card`, and `hero`/`landing` components — nothing here invents a primitive or token.

#### Shared design legend (all five screens)

- **Import surface**: `@open-sharia-enterprise/web-ui` (composite `Button`, `Badge`, `Card*`,
  `Alert*`) and `@open-sharia-enterprise/web-ui/primitives` where a primitive is required — **not**
  `ts-web-ui`.
- **Color tokens** (Tailwind classes): surfaces `bg-background` / `bg-card` / `bg-accent`; text
  `text-foreground` / `text-muted-foreground` / `text-card-foreground` / `text-primary`; borders
  `border-border`; focus `ring-ring`. AyoKoding brand primary is **honey/amber**
  (`--color-primary: var(--hue-honey)`).
- **Per-path accent hue** (the 6-hue system with `-wash` fill / `-ink` text variants): interview-ready
  → `honey`, immediately-effective → `teal`, fundamentally-strong → `sage`,
  swe→ai-engineer → `plum` — used as `bg-[var(--hue-<h>-wash)]` fills and `text-[var(--hue-<h>-ink)]`
  accents so the four paths are colour-coded consistently across hub, landing, and banner. Hue is
  **never the sole signal** (always paired with the path name/number/icon); the final hue↔path map is
  confirmed at draw time and must hold WCAG-AA for `-ink` text on `-wash`.
- **Radius / elevation**: cards `rounded-xl` (20px on the AyoKoding scale); insets `rounded-lg`;
  `shadow-sm` at rest → `shadow-md` on hover.
- **Breakpoints**: `sm` 640 / `md` 768 / `lg` 1024 / `xl` 1280 — the only prefixes this app uses. The
  content column stays fluid `flex-1 px-6 py-8 lg:px-8` inside the `max-w-screen-2xl` content shell;
  the right TOC rail (`w-[200px]`, `hidden xl:block`) and resizable sidebar (`hidden md:block`) are
  untouched **except** for the Screen 3 `<aside>` content swap (`ResizableSidebar` keeps its shell,
  gate, handle, and persisted width — only its `children` change).
- **The three render viewports** (used by every lo-fi wireframe and every hi-fi `.png`, identical across
  all five screens): **mobile 375 px** (below `sm` 640), **tablet 768 px** (exactly `md`), **desktop
  1280 px** (exactly `xl`). These are Tailwind's default breakpoints [Web-cited —
  <https://tailwindcss.com/docs/responsive-design>, accessed 2026-07-21: `sm` 40rem/640px, `md`
  48rem/768px, `lg` 64rem/1024px, `xl` 80rem/1280px], and 375/768/1280 are already the widths this
  plan's Playwright verification steps resize to, so mockups and verification agree by construction.
- **A11y baseline** (mirrors existing components): each new navigation region is a
  `<nav aria-label="…">`; lists are semantic `<ol>`/`<ul>` (this app uses semantic lists, not
  `role="list"`); the canonical focus ring is `focus-visible:ring-2 focus-visible:ring-ring`; the
  current location uses `aria-current="page"`; the global skip-link → `#main-content` is unchanged.

#### Screen 0 hi-fi — Landing hero (`/en`), Option A (four goal cards in the hero)

- **Where it lands**: extends [`app-shell/shell/hero.tsx`](../../../apps/ayokoding-www/src/features/app-shell/shell/hero.tsx)
  (currently H1 + tagline + `Button` Learn/Tools). The two existing CTAs move into the global nav; the
  hero's primary visual weight becomes the path decision.
- **Container**: keep the existing `<section className="px-6 pt-12 pb-10 lg:px-8 lg:pt-16">` with the
  inner `mx-auto max-w-6xl`. H1 unchanged (`text-4xl … sm:text-5xl lg:text-6xl font-extrabold`,
  `t(locale,"heroHeading")`); tagline `mt-5 max-w-2xl text-lg text-muted-foreground` (goal-framed copy).
- **"Choose your path" eyebrow**: `<p className="mt-8 text-sm font-semibold uppercase tracking-wide text-muted-foreground">`.
- **Grid**: `<ul className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2">` — 2×2 at `md+`, single column
  below. Each `<li>` a **`PathCard`** (same net-new component as Screen 1, `context="hero"` variant):
  the whole card is one `<Link href={`/${locale}/c/learn/paths/${pathId}`}>` (SectionCard pattern, no
  link-in-link). Card = `Card` (`rounded-lg border-border shadow-sm hover:bg-accent hover:shadow-md`,
  `border-l-4` in the path hue `border-[var(--hue-<h>)]`). Contents — **goal phrase** as the prominent
  line (`text-lg font-semibold`), the **formal path name** beneath (`text-xs text-muted-foreground`), a
  course-count `Badge` (`variant="secondary" size="sm"` + hue wash), and a "Start →" `meta`
  (`text-sm font-medium text-primary`, lucide `ArrowRight`).
- **Escape hatch row**: below the grid, `<div className="mt-6 flex flex-wrap items-center gap-x-5 gap-y-2">`
  — a primary-weight `<Link className="text-sm font-medium text-[var(--hue-honey-ink)]">` "Not sure
  which fits? Compare all paths →" (→ `/en/c/learn/paths`, Screen 1) and a subordinate
  `text-sm text-muted-foreground` "Browse the full course library →" (→ `/en/c/learn/courses`).
- **States**: card hover `bg-accent shadow-md`, arrow nudges `group-hover:translate-x-0.5`;
  focus-visible `ring-2 ring-ring` on the card. All four cards equal weight — none de-ranked.
- **Responsive**: 2×2 `md+`; single column `<md` (full-width cards, ≥44px tap height); escape-hatch
  links wrap under the grid on mobile; four cards + eyebrow stay within one short scroll on a phone.
- **A11y**: `<ul>`/`<li>`; each card `<a aria-label="Start the {path} path — {goal}, ~{N} courses">`;
  hue is decorative (goal phrase + path name carry meaning); eyebrow is a real heading landmark, not
  styled text alone if it introduces the list.

#### Screen 1 hi-fi — Paths hub (`/en/c/learn/paths`), Option A (2×2 card grid)

- **Container**: content column; inner `<section className="mx-auto max-w-6xl px-6 py-8 lg:px-8">`.
  Header: `<h1 className="text-4xl font-extrabold tracking-tight">` "Choose your path" +
  `<p className="mt-2 text-muted-foreground">` "One library, converging within your role."
- **Grid**: `<ul className="mt-8 grid grid-cols-1 gap-6 md:grid-cols-2">` — one column `<md`, **2×2** at
  `md+`; four `<li>`.
- **`PathCard`** (net-new, composes the existing **`SectionCard` pattern** — the whole card is a single
  `<Link className="group block focus-visible:outline-none">`, so there is **no** nested button and no
  link-in-link trap): wraps `Card`
  (`h-full rounded-xl transition-colors hover:bg-accent hover:shadow-md group-focus-visible:ring-2 group-focus-visible:ring-ring`).
  Contents — a kind `Badge` (`variant="outline"` + `hue`), `CardTitle` (`text-lg font-semibold`) = path
  name, `CardDescription` (`text-sm text-muted-foreground`) = the one-line arc
  ("interview prep → production-effective → deeper"), a course-count `Badge`
  (`variant="secondary" size="sm"`) "~N courses", and the `meta` affordance "Start →"
  (`text-sm font-medium text-primary` + lucide `ArrowRight h-3.5 w-3.5`) exactly as `SectionCard`.
- **States**: default (`bg-card border-border shadow-sm`); hover (`bg-accent shadow-md`, arrow nudges
  `group-hover:translate-x-0.5`); focus-visible (`ring-2 ring-ring` on the card). The fourth card is
  never visually de-ranked — equal weight is why Option A beat B.
- **Below the grid**: a tertiary
  `<a className="mt-6 inline-flex text-sm text-muted-foreground hover:text-foreground">` "Browse the
  full course library →" → `/en/c/learn/courses`.
- **Responsive**: 2×2 `md+`; single column `<md` (full-width cards, comfortable tap height; the "Start"
  affordance lives inside the full-card tap target).
- **A11y**: `<ul>`/`<li>`; each card `<a aria-label="Start the {path} path — {N} courses">`; the hue is
  decorative (path name carries the meaning).

#### Screen 2 hi-fi — Path landing (`/en/c/learn/paths/<path-id>`), Option A (phase-grouped numbered syllabus)

- **Container**: content column `flex-1 px-6 py-8 lg:px-8`; inner reading column `max-w-3xl`. A
  path-aware `Breadcrumb` (`Home / Learn / <Path Title>`), `<h1 className="text-4xl font-extrabold tracking-tight">`
  = path title, `<p className="text-muted-foreground">` = arc summary, framed by a hue strip
  (`bg-[var(--hue-<h>-wash)]`) matching the path's hub card.
- **Fast-path callout** (interview-ready etc.): `Alert variant="info"` above the list — "Experienced &
  job-hunting? Skip the prologue → jump to Phase 1." with an in-page anchor.
- **Syllabus**: each phase is a `<section>` with heading
  `<h2 className="mt-8 text-sm font-semibold uppercase tracking-wide text-muted-foreground">`
  (`lg:sticky lg:top-16` on desktop, inline on mobile). Courses are a **semantic ordered list**
  `<ol className="mt-3 space-y-1">` where the visible number **is** the path order; each row is a
  `<Link>` (carrying `?path=<path-id>`) styled like the sidebar-tree link
  (`rounded-md px-2 py-1 text-sm hover:bg-accent hover:text-foreground`). Capstone rows carry a `▸`
  marker + a `Badge variant="outline" hue` "Capstone".
- **States**: rows are **stateless links** (no per-user progress store in scope); the skippable prologue
  phase is dimmed (`text-muted-foreground`) with a `Badge size="sm"` "skippable".
- **Responsive**: full-width single column `<lg`; `max-w-3xl` reading column `lg+`; phase headings
  sticky only where there is vertical room (`lg+`).
- **A11y**: `<nav aria-label="{Path} syllabus">` around the phases; each phase an `<ol>` so reading
  order and "course k of N" are programmatically derivable — numbers are list semantics, not decoration.

#### Screen 3 hi-fi — Course page in path context, Option B (left path rail + banner readout + prereqs + prev/next)

The **unchanged, path-neutral course body** renders as today (`article className="min-w-0 flex-1 px-6 py-8 lg:px-8"`,
`h1 text-4xl font-extrabold`, `MarkdownRenderer`) with the path rail beside it and four affordances
layered around it.

- **`PathRail`** (net-new — the selected Option B's centrepiece; rendered as `ResizableSidebar`'s
  `children` instead of `<Sidebar>` when `?path=` is present, and inside `MobileNav`'s `SheetContent`
  below `md`): `<nav aria-label="{Path} course list">` wrapping a header block (path title
  `text-sm font-semibold`, `course k of N` `text-xs text-muted-foreground`, a
  `bg-[var(--hue-<h>-wash)]` tint tying it to the hub card) and a semantic
  `<ol className="mt-3 space-y-0.5">`. Each row is a `<Link>` carrying `?path=<path-id>`, styled like
  `sidebar-tree`'s links (`rounded-md px-2 py-1 text-sm hover:bg-accent hover:text-foreground`) with
  the order number in a fixed-width `<span className="tabular-nums text-muted-foreground">`. Phase
  groups are `<li>` separators (`mt-3 border-t pt-2 text-xs uppercase tracking-wide text-muted-foreground`)
  at `lg+`, degrading to a bare `border-t` rule at `md`. **Current row**: `aria-current="page"` plus a
  `▸` marker plus `font-semibold` plus `bg-accent` — never hue alone. **Footer**: `view full path →`
  and `browse all courses →` links (`text-xs`), so the generic tree is always one click away.
  **Truncation**: rows are `truncate` with the full title in the link's `aria-label`, which is what the
  `~115 px` 15 %-floor width at `md` requires.
- **`PathBanner`** (net-new, above the breadcrumb, only when `?path=` is present; **retained from
  Option A as the rail's compact readout** — it is the only path affordance visible below `md` before
  the drawer is opened): full-width strip
  `<div className="mb-4 flex items-center justify-between rounded-lg bg-[var(--hue-<h>-wash)] px-4 py-2 text-sm">`
  — left `▸ On path: <Path> · course <k> of <N>` (`text-[var(--hue-<h>-ink)] font-medium`), right a
  "view full path" `<Link>` (`underline-offset-2 hover:underline`) → the path landing, and — below
  `md` only (`md:hidden`) — a disclosure `<button aria-expanded aria-controls>` with accessible name
  `Open path course list — {Path}, course {k} of {N}` that opens the shipped left drawer.
- **Path-aware `Breadcrumb`**: `Home / Learn / <Path Title> / <Course Title>` (the `<Path Title>` crumb
  links to the landing with `?path=`), via the extended component below.
- **`PrerequisiteList`** (net-new, shown in **both** path and canonical views):
  `<p className="text-sm text-muted-foreground"><span className="font-medium text-foreground">Prerequisites:</span> …</p>`
  where each prerequisite is a `<Link>` (carrying `?path=` in path context) separated by `·`. **Empty
  state**: the whole line is omitted when the course has no prerequisites (never an empty
  "Prerequisites:").
- **`PrevNext` (path-aware)**: existing component, markup unchanged; `prev`/`next` come from the
  **manifest** (not `weight`) and both hrefs keep `?path=<path-id>`; bottom of article as today
  (`mt-12 border-t pt-6`).
- **Canonical fallback (no `?path=`)**: no rail (the `<aside>` reverts to `<Sidebar>` / `SidebarTree`,
  and `MobileNav`'s drawer stays generic — byte-identical to today); no banner; breadcrumb
  `Home / Learn / Courses / <Course Title>`;
  `PrerequisiteList` still shows; and a **`PathCourseLinks`** (net-new) affordance renders below the
  body: `<div className="mt-8 text-sm"><span className="text-muted-foreground">This course is part of:</span> …</div>`
  with **one `Badge` link per path whose manifest `courseOrder` actually lists this course** (hue per
  path, `variant="outline"`, wrapped in a `<Link>` to that path's landing). A course a path only
  **links** (not includes) shows no badge for it (DD-24) — `coding-interview` shows three badges; an
  AI-specific course shows a single `SWE → AI Engineer` badge.
- **States**: with-path (rail + banner readout + path breadcrumb + manifest prev/next); without-path
  (generic sidebar + canonical breadcrumb + `PathCourseLinks` + canonical neighbours or omitted
  prev/next); no-prereq (list omitted); single-path course (one `PathCourseLinks` badge); rail-in-drawer
  (below `md`, opened from either the header `☰` or the banner disclosure).
- **Responsive** (full breakpoint-by-breakpoint contract in
  [Screen 3 responsive specification](#screen-3-responsive-specification-the-selected-option-b-breakpoint-by-breakpoint)):
  rail hidden `<md` → drawer; rail truncated at the 15 % floor `md`-`lg`; rail full-width-of-panel with
  phase labels `lg+`. Banner full-width at all breakpoints (with the `md:hidden` disclosure button);
  `PrevNext` stacks `<sm`, left/right `sm+` (unchanged); `PathCourseLinks` badges wrap.
- **A11y**: rail is `<nav aria-label="{Path} course list">` over a semantic `<ol>` with
  `aria-current="page"` + `▸` + `font-semibold` on the current row (never colour alone, WCAG AA 1.4.1);
  banner is a `<nav aria-label="Path position">`; "course k of N" is real text; the mobile disclosure
  button carries the full accessible name and `aria-expanded`/`aria-controls`; the drawer inherits Radix
  `Dialog` focus trap / restore / `Esc` from the shipped `Sheet`, and its `SheetTitle` becomes the path
  name; prerequisite and path-course affordances are semantic inline link lists; hue badges always carry
  the path name as text.

#### Extended existing components (additive props, no fork)

- **`PrevNext`** (`apps/ayokoding-www/src/features/navigation/shell/prev-next.tsx`): markup unchanged
  (`<nav aria-label="Page navigation">`, `ChevronLeft/Right`, eyebrow + title). Change is
  **data-source only** — `prev`/`next` resolve from the active path manifest and both `<Link>` hrefs
  append `?path=<path-id>`; with no path context they fall back to canonical neighbours (or render
  `null` when both are null, as today).
- **`Breadcrumb`** (`.../navigation/shell/breadcrumb.tsx`): reuse `segments` + `contentHrefs` as-is; add
  optional path context so a `<Path Title>` segment is injected (linking to the landing with `?path=`)
  and downstream `href`s carry `?path=`. `showCurrent` / `aria-current="page"` behaviour unchanged.
- **`contentUrl()`** (`.../content/core/content-url.ts`): add an optional `pathId` that appends
  `?path=<path-id>`, so breadcrumb, prev/next, and prerequisite link builders all produce
  path-preserving URLs from one place.
- **`ResizableSidebar`** (`.../navigation/shell/resizable-sidebar.tsx`) — **selected Option B's only
  change to an existing shell**: the `<aside>`, the `hidden … md:block` gate, `ResizablePanel`, the
  15 %-35 % band, the drag/keyboard handle, and the `ayokoding-sidebar-width` `localStorage` key are all
  unchanged [Repo-grounded]. Only the `children` passed by `ContentLayout` change — `<PathRail>` when
  the request carries `?path=`, `<Sidebar>` otherwise. No fork, no second `<aside>`, no second width key.
- **`MobileNav`** (`.../app-shell/shell/mobile-nav.tsx`): same content swap inside the already-shipped
  `Sheet` / `SheetContent side="left"` — `<SidebarTree>` is replaced by `<PathRail>` when a path context
  is active, and `SheetTitle` becomes the path name. The preset-width `fieldset`, the `PRIMARY_NAV_LINKS`
  menu, the tRPC tree fetch, and `onOpenChange(false)`-on-link-click all stay as they are
  [Repo-grounded]. The component additionally accepts the banner's disclosure button as a second opener,
  so `open` state stays single-sourced in `header.tsx`.

### R7 Prior-Art Findings (window-shopped 2026-07-21)

A `web-researcher` surveyed 13 learning platforms on 2026-07-21 for how a "path/track over a shared
library" is presented end-to-end. Every claim below carries a source URL (access date 2026-07-21).

**Per-platform highlights**

- **roadmap.sh** — the home page _is_ the catalog: role-based + skill-based roadmaps as chunked text
  links, 92-item catalog one level deep; deliberately not a hero-style chooser.
  [roadmap.sh](https://roadmap.sh/), [/roadmaps](https://roadmap.sh/roadmaps).
- **Coursera** — generic value-prop hero + single CTA; a **4-option goal-question** ("What brings you
  to Coursera today?") sits _below_ the hero; Professional-Certificate landings use a **numbered
  "Course 1 of 9" list + advisory "take in order, content builds"** note, with a breadcrumb.
  [home](https://www.coursera.org/), [Google Data Analytics cert](https://www.coursera.org/professional-certificates/google-data-analytics).
- **Boot.dev** — generic hero → **"Pick a Learning Path" section with 3 cards**; path landing is a
  **flat numbered list (1-23)**, no breadcrumb/banner. [boot.dev](https://www.boot.dev/),
  [backend path](https://www.boot.dev/paths/backend-python-golang).
- **Codecademy** — Career Center shows **12 path cards + a "sorting quiz" alongside** (not gating);
  two-tier syllabus (path → unit). [career-center](https://www.codecademy.com/career-center).
- **Pluralsight** — optional **Skill IQ** entry; once inside a path you **"skip modules you already
  know"** (advisory, not gated). [product/paths](https://www.pluralsight.com/product/paths).
- **Exercism** — join a track, **completion unlocks** more; **Practice-Mode opt-out** unlocks
  everything for experienced users. [getting-started](https://exercism.org/docs/using/getting-started).
- **Scrimba / DataCamp** — prerequisites shown as **advisory prose** ("for intermediate devs; if not,
  do X first" / "no prerequisites for this track"), never a gate or DAG. [Scrimba AI path](https://scrimba.com/the-ai-engineer-path-c02v),
  [DataCamp track](https://www.datacamp.com/tracks/associate-data-scientist-in-python).
- **edX / Educative** — "answer a few questions" quiz offered as an **alternative** route, never the
  sole entry. [edX find-your-path](https://www.edx.org/find-your-path), [Educative paths](https://www.educative.io/paths).
- **Frontend Masters / Khan Academy** — level-tiered path cards with **no cross-path overlap
  indicator**; Khan's mastery model is the strongest "what's next" precedent. [FEM learn](https://frontendmasters.com/learn/),
  [Khan mastery](https://support.khanacademy.org/hc/en-us/articles/115002552631-What-are-Course-and-Unit-Mastery).

**Adopt / adapt / avoid (mapped to our screens)**

| Pattern (source)                                                    | Screen           | Verdict                                                       |
| ------------------------------------------------------------------- | ---------------- | ------------------------------------------------------------- |
| 3-4 path cards under a value-prop hero (Boot.dev)                   | 0 Landing hero   | **Adopt** — extend 3→4; put the cards _in_ the hero           |
| 4-option goal-question (Coursera)                                   | 0 (Option B)     | **Adapt** — kept as the runner-up; goal verbs reused on cards |
| Guided quiz as sole entry (edX/Educative)                           | 0 (Option C)     | **Avoid** — our paths are already goal-labeled                |
| Filterable card grid w/ course-count metadata (DataCamp)            | 1 Paths hub      | **Adopt** — differentiate overlapping paths without a table   |
| Full categorized catalog, dense (roadmap.sh)                        | 1 (browse all)   | **Adopt for hub, avoid for hero**                             |
| Sorting quiz _alongside_ direct cards (Codecademy)                  | 0→1 escape hatch | **Adapt** — "Compare all paths" link, never a gate            |
| Numbered list + advisory "builds on earlier" (Coursera)             | 2 Path landing   | **Adopt** — validates Option A over the accordion             |
| Two-level syllabus, max 2 disclosure levels (Codecademy + NN/g)     | 2                | **Adopt** — phase → course, never phase → unit → lesson       |
| Advisory prereqs + skip-ahead for experienced (Scrimba/Pluralsight) | 2, 3             | **Adopt** — `PrerequisiteList` + fast-path callout            |
| Breadcrumb on a nested/shared page (Coursera)                       | 3 Course-in-path | **Adopt** — nearest precedent for `PathBanner`                |
| Course-page path banner + "in N paths" affordance                   | 3                | **Build net-new** — industry-wide whitespace, no precedent    |
| Undifferentiated role+skill list (LinkedIn Learning)                | 1                | **Avoid** — keep path types legible                           |

**Evidence-backed UX principles applied** (each drives a selection above)

- **Hick's Law** — decision time grows with the number/complexity of choices; minimize and highlight a
  recommended option. [lawsofux.com/hicks-law](https://lawsofux.com/hicks-law/). → 4 cards, not 12.
- **Choice overload (Iyengar & Lepper 2000, "jam study")** — 6 options converted ~10× better than 24.
  [study summary](https://www.researchgate.net/publication/12189991_When_Choice_is_Demotivating_Can_One_Desire_Too_Much_of_a_Good_Thing).
  → dense catalog deferred to the hub.
- **Progressive disclosure** — show a few key options first; **more than two levels hurts usability**.
  [NN/g](https://www.nngroup.com/articles/progressive-disclosure/). → phase → course only.
- **Information scent** — cue value before the click. [NN/g](https://www.nngroup.com/articles/information-scent/).
  → goal verbs + course counts on cards.
- **Recognition over recall** — show, don't make them remember. [NN/g](https://www.nngroup.com/articles/recognition-and-recall/).
  → persistent path banner/breadcrumb on the course page.
- **Target size** — WCAG 2.2 §2.5.8 AA floor 24×24px; ~48px comfort. [W3C](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html).
  → full-card tap targets on mobile.

**Whitespace / gaps** — no surveyed platform surfaces "this course is in N paths" or a course-page
path banner; both are **net-new** here (built on Coursera's breadcrumb as the nearest analog). Freshness
caveats: Codecademy/DataCamp homepages returned 403 and Scrimba's exact prereq wording is search-derived
— re-verify verbatim before quoting in shipped UI copy.

## Acceptance Criteria (Gherkin)

Navigation-feature scenarios are the source of the `specs/` Gherkin companion (app code). Content and
path-ordering scenarios document behavior. Each scenario uses exactly one primary Given/When/Then;
extras chain with And. The scenarios below cover the `course-paths` navigation feature; course-specific
acceptance scenarios appear further down, under
[NEW Course & Capstone Specifications](#new-course--capstone-specifications).

```gherkin
Scenario: The landing hero surfaces the four goal paths directly
  Given a first-time visitor opens the site landing page at /en
  When the hero section renders
  Then the hero shows a goal-labeled path card for each published path
  And a "Compare all paths" link to /en/c/learn/paths is visible below the cards
```

```gherkin
Scenario: A path landing page lists its courses in manifest order
  Given the interview-ready/software-engineer path manifest is published
  When a reader opens the path landing page at /en/c/learn/paths/interview-ready/software-engineer
  Then the courses appear in the manifest's courseOrder
  And every course link carries the path context query parameter
```

```gherkin
Scenario: A path manifest is a valid topological entry into the prerequisite DAG
  Given a path manifest lists a courseOrder of course IDs
  When the manifest-integrity check runs
  Then no course appears before any of its declared prerequisites that are also in the manifest
  And every listed course ID resolves to an existing course in the library
```

```gherkin
Scenario: Every manifest course reference resolves to a real course
  Given a path manifest lists a courseOrder of course IDs
  When the manifest-integrity check runs
  Then every listed course ID resolves to an existing course in the library
  And no course ID appears more than once in the manifest
```

```gherkin
Scenario: A course page surfaces its declared prerequisites
  Given a course declares prerequisites in its canonical metadata
  When a reader opens the course page with or without a path context
  Then the page lists each prerequisite course with a link to its canonical URL
  And the prerequisite list renders even in the canonical no-path view
```

```gherkin
Scenario: Prev and next follow the active path's order
  Given a reader is on a course with an active path context
  When the reader reads the prev/next navigation
  Then prev and next are the neighboring courses in that path's manifest
  And both links preserve the path context query parameter
```

```gherkin
Scenario: The breadcrumb reflects the active path
  Given a reader is on a course with an active path context
  When the breadcrumb renders
  Then it shows Home, Learn, the path title, and the course title
  And the path crumb links to the path landing page /en/c/learn/paths/<path-id> with the path context preserved
```

```gherkin
Scenario: A course deep-linked without path context renders the canonical view
  Given a reader opens a course URL /en/c/learn/courses/<course-id> with no path context query parameter
  When the course page renders
  Then the course body renders in full with the content-tree breadcrumb and its prerequisite list
  And a "this course is part of" affordance lists every path that includes the course
```

```gherkin
Scenario: An invalid path context falls back to the canonical view
  Given a reader opens a course URL with a path context that names no known path
  When the course page renders
  Then the course renders the canonical standalone view
  And no error is shown
```

```gherkin
Scenario: A course omitted from a path shows no path nav for that path
  Given a course is not listed in a given path's manifest
  When a reader opens that course with that path's context
  Then the course renders the canonical standalone view
  And neither the path rail nor the path banner is shown for that path
```

```gherkin
Scenario: The path rail shows the whole ordered arc beside a course at desktop width
  Given a reader opens a course in path context on a desktop-width viewport
  When the page renders
  Then the left rail lists that path's courses in manifest order with the current course marked
  And the current course is distinguished by a marker and weight, not by colour alone
  And the rail offers a link back to the full path and to the whole course library
```

```gherkin
Scenario: The path rail collapses into the existing navigation drawer on a phone
  Given a reader opens a course in path context on a phone-width viewport
  When they activate the path readout's "open path course list" control
  Then the existing left navigation drawer opens showing that path's ordered courses
  And focus moves into the drawer and returns to the control when the drawer is dismissed
```

```gherkin
Scenario: A course opened without path context renders the generic sidebar unchanged
  Given a reader opens a canonical course URL with no path context query parameter
  When the page renders
  Then the left sidebar shows the generic content tree exactly as it does elsewhere in the site
  And no path rail, path readout, or path breadcrumb segment appears
```

```gherkin
Scenario: A legacy fundamentally-strong URL redirects to the canonical course URL
  Given a re-homed course previously lived under the legacy fundamentally-strong/software-engineer content path
  When a reader requests the legacy URL
  Then the app redirects to the course's canonical /en/c/learn/courses/<course-id> URL
  And the redirect preserves any path context query parameter
```

```gherkin
Scenario: The legacy section-index browse still resolves after re-homing
  Given the 33 shipped topics have been re-homed into the course library
  When a reader browses the legacy fundamentally-strong software-engineer section index the old way
  Then every section-index entry links to live content at its /en/c/learn/courses/<course-id> URL or via a redirect
  And no legacy section-index entry resolves to a drained or missing location
```

```gherkin
Scenario: Old-way and new-way navigation coexist
  Given a course now lives at its canonical /en/c/learn/courses/<course-id> URL
  When a reader reaches it via the legacy section-index browse
  And another reader reaches it via a /en/c/learn/paths/<path-id> path landing
  Then both navigations resolve to the same single canonical course body
```

```gherkin
Scenario: The three software-engineer paths reference a shared course with no body duplication
  Given a course appears in all three of the interview-ready, immediately-effective/software-engineer, and fundamentally-strong/software-engineer manifests
  When the course library is inspected
  Then exactly one canonical path-neutral body exists for that course
  And each manifest references the course by its stable course ID
```

```gherkin
Scenario: The interview-ready MVP proves the architecture before other path work begins
  Given the interview-ready/software-engineer MVP (an architecture smoke test over already-live topics 1-33) is delivered end-to-end
  When the software-engineer-to-ai-engineer path's authoring begins
  Then the interview-ready MVP's landing page, manifest, and path-aware nav are already live in production
  And the interview cluster's remaining NEW courses are not required for that MVP to be considered shipped
```

```gherkin
Scenario: The AI path is authored before the other two manifests are composed
  Given the interview-ready MVP has shipped
  When authoring effort is allocated across the remaining paths
  Then the software-engineer-to-ai-engineer path's six net-new courses and manifest are authored first
  And the immediately-effective/software-engineer and fundamentally-strong/software-engineer manifests are composed only afterward
```

```gherkin
Scenario: The immediately-effective path is build-app-first
  Given the immediately-effective/software-engineer path manifest is published
  When a reader walks the path
  Then editor/tooling, one language end-to-end, and building a real app precede the CS-fundamentals and DS&A courses
  And the reader ships a real deployed app before any pure-theory course
```

```gherkin
Scenario: The fundamentally-strong path is fundamentals-first
  Given the fundamentally-strong/software-engineer path manifest is published
  When a reader walks the path
  Then CS foundations, computer architecture, paradigms, and DS&A precede the build-real-software courses
  And the ordering is a valid topological entry into the prerequisite DAG
```

```gherkin
Scenario: The software-engineer-to-ai-engineer path links prerequisites instead of including them
  Given the immediately-effective/software-engineer-to-ai-engineer path manifest is published
  When a reader inspects its courseOrder
  Then no shared software-engineering-fundamentals course from the other three manifests is included in courseOrder
  And the path landing page links out to those prerequisite courses' canonical pages instead
```

```gherkin
Scenario: The behavioral course covers the layoff and employment-gap narrative
  Given the behavioral-and-leadership-interviews course is authored
  When an experienced re-entrant reads its learning track
  Then it explicitly covers framing an employment gap, a layoff, or a re-entry story
  And it treats senior/staff/EM leadership rounds as core material
```

```gherkin
Scenario: The navigation feature meets accessibility requirements
  Given a reader uses a keyboard and a screen reader on a course in path context
  When they navigate the path rail, banner, breadcrumb, prerequisite list, and prev/next
  Then each is a labelled landmark reachable and operable by keyboard with visible focus
  And the document language attribute matches the active locale
```

```gherkin
Scenario: The app builds and validates green
  Given the navigation feature and the interview-ready path are complete
  When nx run ayokoding-www:build, the three test tiers, and the link/heading validators run
  Then the build and all tiers succeed
  And link, heading-hierarchy, and markdownlint validation report no errors
```

### Three-bucket learn-section IA (scope extension, 2026-07-21)

```gherkin
Scenario: The learn section exposes exactly three structural buckets
  Given the learn-section IA revamp has landed
  When the content tree under the en learn section is inspected
  Then its only structural buckets are paths, courses, and legacy
  And no former subject domain remains as a direct child of the learn section
  And the section keeps its own index and overview hub pages
```

```gherkin
Scenario: A relocated legacy domain URL redirects to its legacy address
  Given a page previously lived at a learn-section domain that is not a course or a path
  When a reader requests that page's old URL
  Then the app permanently redirects to the same page under the legacy bucket
  And the rest of the path after the domain segment is preserved unchanged
```

```gherkin
Scenario: A deep legacy path keeps its sub-taxonomy verbatim
  Given a legacy page previously lived several levels below its domain
  When a reader follows the redirect to its new legacy address
  Then every path segment below the domain is unchanged
  And the page body is byte-identical to the body served before the relocation
```

```gherkin
Scenario: The legacy redirect never swallows the courses or paths buckets
  Given the legacy bucket redirect rules are configured
  When a reader requests a canonical course URL or a path landing URL
  Then the app serves the page without redirecting it
  And no redirect rule declares a bucket-wide learn-section wildcard source
```

```gherkin
Scenario: A re-homed fundamentally-strong course is not routed into the legacy bucket
  Given the fundamentally-strong topic directories were collapsed into flat course bodies
  When a reader requests a legacy fundamentally-strong course URL
  Then the app redirects to that course's canonical course URL
  And no legacy-bucket rule matches the fundamentally-strong prefix
```

```gherkin
Scenario: The relocation rewrites no page content
  Given the six non-course learn-section domains have been relocated
  When the relocation commit's diff is inspected
  Then every relocated file appears as a pure rename with no content change
  And the only edited content files are the section overview and the new legacy bucket index
```

```gherkin
Scenario: Navigation surfaces follow the relocated tree with no code change
  Given the six domains now live under the legacy bucket
  When the sidebar tree, browse index, sitemap, feed, and search data are regenerated
  Then each lists every relocated page at its new legacy URL
  And no navigation source file required a hardcoded domain slug to be edited
```

```gherkin
Scenario: The legacy bucket landing tells a reader what the bucket is
  Given a reader opens the legacy bucket landing page
  When the page renders
  Then it states that the material is older and kept for reference while the course library fills
  And it links onward to the course library and to the paths hub
```

```gherkin
Scenario: The Indonesian locale is left unchanged and the deferral is recorded
  Given the learn-section IA revamp is scoped to the English locale
  When the Indonesian content tree is inspected after the revamp
  Then its section is unchanged with no bucket directories and no relocation
  And the plan records the Indonesian deferral explicitly as a non-goal
```

## NEW Course & Capstone Specifications

This plan authors **twenty NEW courses + nine NEW capstones** into the library — the original
fourteen (interview + productivity/harness/security clusters) plus **six further NEW AI-specific
courses** added 2026-07-20 for the `software-engineer-to-ai-engineer` path — plus nine capstones
(three original plus six DD-20 inter-topic capstones). Full specs for the three original capstones
follow later in this section; the six DD-20 inter-topic capstones are specified inline within their
host course files per `delivery.md` Phase 10, Band 8. Each course is a full page-bundle (learning
track + drilling track) matching the sibling plan's per-topic anatomy and inheriting its cross-cutting
authoring guarantees verbatim (accuracy-verified via `web-researcher` before authoring;
follow-along-complete; typed-Python where Python; colocated runnable `code/`; exhaustive
`co-NN`/`ex-NN` enumeration; `prerequisites` metadata + navigation). Every course declares its
`prerequisites` so it takes its place in the library's prerequisite DAG. Full per-course
concept/example/capstone detail lives in the
[`syllabus/courses/` catalog](./syllabus/courses/README.md) (one file per course ID); the specs below
fix each course's purpose, register, and acceptance shape.

**Register.** The four interview-technique courses use a **refresh register** (assume prior
professional experience; reload technique, do not teach from zero). The ten productivity/harness/
security courses and the six AI-specific courses (2026-07-20) use the normal **first-learn By-Example
register**; `just-enough-cpp` is primer scope. The AI-specific courses additionally use the
**links-not-included** entry model: they assume the reader already has the SWE fundamentals the other
three paths teach (DD-24) — the courses themselves teach AI material only, they do not re-teach the
linked prerequisites.

**Principle-first framing (HARD).** Every course teaches a durable **principle**; target codebases
(`remotebrowser`, `wazuh`, `vacti*`, the ose family) are **illustrative worked-examples**, never the
subject.

**Volume-target bands** (inherited from the sibling; floor not cap):

| Course shape                                  | Concept floor (`co-NN`) | Worked-example band (`ex-NN`)         |
| --------------------------------------------- | ----------------------- | ------------------------------------- |
| By Example                                    | ≥ 10                    | 75–85 code examples                   |
| Primer (_Just Enough X_)                      | ≥ 8                     | 75–85 code examples (By-Example pace) |
| Annotated-concept, code-bearing               | ≥ 10                    | 45–60 worked examples                 |
| Annotated-concept, no-code (refresh register) | ≥ 8                     | 30–60 worked scenarios                |

### Interview-technique courses (refresh register)

- **`coding-interview`** (By Example · Python, patterns language-agnostic) — reload LeetCode-style
  pattern recognition + time-boxed problem-solving; hosts the 2026 senior interview-loop-map.
- **`take-home-and-live-coding`** (By Example · Python) — time-boxed take-home + observed live/pair
  technique: scope, test, README hygiene, thinking aloud.
- **`system-design-interview`** (Annotated-concept · no code) — the senior/staff system-design
  interview rubric + whiteboard flow; forward-links the depth course `system-design`.
- **`behavioral-and-leadership-interviews`** (Annotated-concept · no code) — STAR + senior/staff/EM
  rounds AND framing an **employment-gap / layoff / re-entry** narrative.

```gherkin
Scenario: Interview courses are written in a refresh register
  Given the four new interview-technique courses are authored
  When an experienced engineer reads them
  Then each assumes prior professional experience and focuses on interview technique and breadth refresh
  And none teaches core concepts from zero
```

### Productivity & self-hosting courses (first-learn By-Example)

- **`async-python-and-fastapi-services`** (By Example · Python) — async Python, FastAPI/Uvicorn,
  Pydantic, `uv`/`ruff`/`pyright`/`pytest-asyncio` — the `remotebrowser` + FastAPI-backend stack.
  Scoped tightly to the concrete framework + toolchain: async _concepts_ stay in
  `concurrency-and-parallelism`, framework _internals_ in `build-your-own-web-framework` — cross-linked,
  not re-derived.
- **`self-hosting-essentials`** (By Example · ops/config) — **light** on-ramp: one box, containerize,
  reverse proxy + TLS, systemd/ports, env/secrets, backups, PaaS git-push. Strictly below
  `containers-and-orchestration` / `cloud-and-iac`; distinct from `bare-metal-virtualization`.
- **`browser-automation-with-cdp`** (By Example · Python) — Chrome DevTools Protocol browser
  automation (port 9222; nodriver/zendriver family) — the core `remotebrowser` skill. Distinct from
  `software-testing`'s Playwright E2E: raw CDP automation, not a test runner.

```gherkin
Scenario: The light self-hosting course stays below clusters and IaC
  Given the self-hosting-essentials course is authored
  When a reader compares it with containers-and-orchestration and cloud-and-iac
  Then it teaches running one box, containerizing a service, a reverse proxy, and PaaS git-push deploy
  And its overview explicitly excludes clusters, Terraform/Packer/Ansible IaC, and Proxmox
```

### Harness-engineering cluster (first-learn By-Example · Python)

The five build-your-own-agentic-coding-tool courses; the MCP built in `agent-tools-and-mcp` is the same
MCP `remotebrowser` exposes; all feed `capstone-build-your-own-coding-agent`. **AI-band scope-guard**:
these build the primitives at build-your-own depth; the survey course `agentic-ai` (57) previews and
**forward-links** each primitive here and does NOT re-teach at cluster depth, and
`creating-ai-powered-apps` (56) stays at the _use-an-LLM-in-an-app_ altitude.

- **`the-agent-loop`** — the LLM read-eval-act tool-use loop, streaming, stop conditions.
- **`agent-tools-and-mcp`** — tool/function schema design; an MCP server + client; resources/prompts.
- **`agent-context-and-memory`** (Annotated-concept) — context budgeting, compaction, retrieval,
  persistent memory.
- **`agent-permissions-and-sandboxing`** — approval models, sandboxed execution, guardrails,
  fail-closed defaults.
- **`agent-orchestration-subagents-and-observability`** (Annotated-concept) — subagents, background
  tasks, hooks/skills systems, a TUI, evals + tracing/telemetry.

```gherkin
Scenario: The harness cluster builds a working agent from runnable code
  Given the five harness-engineering courses are authored
  When a reader builds an agent from them
  Then the agent loop, tools/MCP, memory, permissions, and orchestration each ship runnable typed-Python examples
  And each course names remotebrowser's bundled MCP or CDP browser only as an illustrative pickup
```

```gherkin
Scenario: The agentic-ai survey forward-links each primitive without re-teaching it
  Given the agentic-ai survey course and the five harness-cluster courses are authored
  When a reader reads the agentic-ai survey
  Then it previews the agent loop, tools/MCP, memory/context, and evals and forward-links each to its cluster course
  And it does not re-teach any primitive at build-your-own depth
```

### AI-engineering specialization courses (`software-engineer-to-ai-engineer` path, added 2026-07-20)

Six NEW courses for the fourth path, teaching **building** AI systems (not driving coding agents —
`agentic-coding` stays a separate axis, DD-21). Each is split into a **stable spine** (durable
principles) and **dated accuracy-note sidebars** (volatile SDK/model/pricing/framework specifics),
matching the pattern the existing AI-band courses already use (DD-28). **These six courses' specs are
now settled** — full concept (`co-NN`), worked-example (`ex-NN`), prerequisite-chain, and capstone
specs exist at [`syllabus/courses/`](./syllabus/README.md) (one 295-425-line file per course); the
format/language/prerequisite summaries below are drawn from those settled files, not first-pass
guesses. Author each course body **from** its `syllabus/courses/<id>.md` spec (per DD-27's build
order, this is authoring priority #1 behind the interview-ready MVP).

- **Light eval gate** (`evaluating-ai-output-essentials` — Annotated-concept, Python) — a small, early
  course sitting right after the first working LLM call and before RAG/agents; answers "how will you
  know this works?" (DD-25).
- **Statistics for evals** (`statistics-for-evaluation` — Annotated-concept, code-bearing, Python) —
  scoped tightly to what evals demand (judge concordance, significance testing), not a general
  statistics survey; `analytics-and-experimentation` (classical product A/B testing) stays a scope
  mismatch and a candidate sibling/prerequisite rather than a merge target (DD-26). Declared a **hard
  prerequisite** of deep evals, so it is authored/placed before that course (see the manifest mirror at
  `syllabus/paths/manifest-immediately-effective-software-engineer-to-ai-engineer.md`).
- **Deep evals** (`evaluating-ai-systems-in-depth` — By Example, Python) — sits after agents; error
  analysis, task-specific criteria, LLM-as-judge with measured human agreement, CI gating, judge-scope
  reliability. Absorbs the three scattered evals treatments in `creating-ai-powered-apps`, `agentic-ai`,
  and `agent-orchestration-subagents-and-observability`, which are trimmed to forward-links rather than
  duplicating a fourth treatment (DD-25, DD-28).
- **Product patterns for probabilistic systems** (`product-patterns-for-probabilistic-systems` —
  Annotated-concept, no code) — product design patterns for systems whose outputs are probabilistic
  rather than deterministic; no course owns this today (DD-28).
- **Inference serving and model deployment** (`inference-serving-and-model-deployment` — By Example,
  Python) — vLLM/TGI, KV-cache, batching, GPU considerations; entirely absent from the library today
  (DD-28).
- **Fine-tuning and adaptation** (`fine-tuning-and-adaptation` — By Example, Python) —
  fine-tuning/LoRA/PEFT versus RAG as a foil; `fine-tun*` appears once library-wide today, as a RAG
  comparison point, never its own course (DD-28).

The scope boundary between the light eval gate and deep evals is stated explicitly in both courses'
overviews, in the style of the existing AI-band scope-guard (DD-10/DD-11), to avoid reproducing that
cluster's overlap problem.

```gherkin
Scenario: The light eval gate and deep evals course do not overlap
  Given the light-eval-gate course and the deep-evals course are authored
  When a reader compares their overviews
  Then each overview states an explicit scope boundary against the other
  And neither course re-teaches the material the other owns
```

```gherkin
Scenario: The statistics-for-evals course stays scoped to what evals demand
  Given the statistics-for-evals course is authored
  When a reader compares it with analytics-and-experimentation
  Then it covers judge concordance and significance testing for evals only
  And it does not re-teach general product A/B testing, which stays analytics-and-experimentation's scope
```

### Security & systems gap-closers

- **`just-enough-cpp`** (Primer · C++) — systems-language principle on-ramp (RAII, templates/generics,
  STL, smart pointers, manual memory); prereq `just-enough-c`; Wazuh's C++ core is one illustration.
- **`detection-engineering-and-siem-operations`** (By Example · XML/rules + config + Python) —
  decoders, correlation rules, log parsing/normalization, FP tuning, dashboards, alert triage; Wazuh
  XML is the worked example. Distinct from `defensive-security` (which is **hands-on By-Example**
  generalist blue-team breadth — Sigma/ELK + IR + hardening, **not** concept-level); prereq
  `defensive-security`.

```gherkin
Scenario: Hands-on detection engineering stays distinct from generalist defensive security
  Given the detection-engineering-and-siem-operations course is authored
  When a reader compares it with the hands-on defensive-security course
  Then it has the reader author working Wazuh decoders, correlation rules, and a dashboard with false-positive tuning
  And defensive-security keeps the generalist Sigma/ELK breadth, IR, and hardening as its distinct scope
```

### NEW capstones

Capstones follow the sibling's capstone-policy shape (goal/outcome, concepts-exercised checklist,
ordered step outline, testable acceptance criteria, done bar = runnable end-to-end + web-verified).

- **`capstone-interview-loop`** (Python + prose) — a full mock interview loop (coding + system-design +
  behavioral incl. gap narrative), each round self-scored against its module rubric.
- **`capstone-build-your-own-coding-agent`** (Python) — assemble the harness cluster into a working
  minimal coding-agent CLI; bonus path drives `remotebrowser` over MCP.
- **`capstone-build-your-own-pentest-engine`** (TypeScript default) — assemble swarm orchestration +
  MCP tool arsenal + CDP browser driving + security-tool-chaining + evidence pipeline + scope
  enforcement + deterministic-prober-vs-AI-verifier into a working engine; `vacti-pentest-engine` is
  the illustration.

```gherkin
Scenario: The coding-agent capstone assembles the harness cluster into a working CLI
  Given the harness cluster and the build-your-own-coding-agent capstone are authored
  When a reader completes the capstone
  Then they have a runnable coding-agent CLI built from the agent loop, tools/MCP, memory, permissions, and orchestration courses
  And a disallowed action fails closed while every run emits a trace
```

```gherkin
Scenario: The pentest-engine capstone assembles the convergence track into a scoped engine
  Given the harness cluster, the CDP course, the security suite, and detection-engineering are authored
  When a reader completes the build-your-own-pentest-engine capstone
  Then they have a runnable engine from swarm orchestration, MCP tooling, CDP browser driving, and security-tool-chaining
  And scope enforcement refuses an out-of-scope target while the capstone uses vacti-pentest-engine only as an illustration
```

## Product Scope

**In-scope features**:

- The `course-paths` ayokoding-www feature: path manifests, path-aware prev/next + breadcrumb,
  `?path=` context, prerequisite display, graceful fallback, path landing pages, a paths hub,
  redirects, accessibility — all under the `/en/c/learn` URL model.
- Re-homing the 33 shipped topics (1–33) into `courses/<course-id>/` with redirects; native-authoring
  the 61 transferred topics (34–94) into `courses/<course-id>/`.
- The four path manifests (`interview-ready/software-engineer` interview-first,
  `immediately-effective/software-engineer` build-app-first,
  `fundamentally-strong/software-engineer` fundamentals-first, and
  `immediately-effective/software-engineer-to-ai-engineer` AI-transition-first, added 2026-07-20) as
  ordered, prerequisite-consistent course-ID lists over the library. The first three converge on the
  same software-engineering endpoint; the fourth converges on a distinct AI-engineering endpoint
  (DD-22).
- Twenty NEW courses (the original fourteen plus six AI-specific, 2026-07-20) + nine NEW capstones
  (three original plus six DD-20 inter-topic capstones) authored into the library (learning + drilling
  each), for a **127-course catalog** (121 software-engineer-role baseline + 6 AI-specific).
- Course variants authored on demand only, where a path needs a genuinely different teaching approach;
  **course surgery** (update/merge/split/create, added 2026-07-20) permitted subject to a four-path
  blast-radius statement per surgery (DD-28).
- Three-level tests (unit/integration/e2e) + a `specs/` Gherkin companion for the nav feature.
- Per-path progression-smoothness audits.
- **The whole-section IA revamp (scope extension, 2026-07-21)**: prefix-relocating the six non-course
  `en/learn/` domains (1,148 `.md`) into a new `legacy/` bucket so `/{locale}/c/learn/` closes at
  exactly three structural buckets (DD-40/DD-41); a new per-domain 308 redirect module
  (`src/redirects/learn-three-bucket.ts`) with its unit test (DD-42); the authored
  `legacy/_index.md` landing (DD-44); the rewritten hand-authored `en/learn/overview.md` (DD-45/Q-F);
  regeneration of `en/learn/_index.md` and `generated/search-data.json`; and the Screen 4 design
  funnel for the legacy landing/banner.

**Out-of-scope features**:

- Rewriting any existing course's subject content.
- Indonesian mirror of the section content.
- Path progress persistence, accounts, or bookmarking.
- Interactive flashcards.
- Speculative enumeration of course variants (authored on demand only).
- Teaching how to **drive** AI coding agents — that stays `agentic-coding`'s existing, unrelated scope
  (DD-21).
- **Rewriting, merging, re-titling, or re-sequencing any legacy page** (scope extension) — the move is
  a prefix relocation only (DD-41).
- **Promoting legacy pages into real `courses/` bodies** — that is later work, tracked per
  [Q-A](./tech-docs.md#q-a--is-legacy-a-staging-pen-or-a-permanent-archive), not delivered here.
- **Extending the three-bucket shape to the `id` locale** — deferred and recorded explicitly (DD-45,
  [Q-B](./tech-docs.md#q-b--does-the-id-locale-get-the-same-three-bucket-shape-now)).

## Product-Level Risks

- **Order/manifest drift**: a manifest references a missing/renamed course ID, or orders a course
  before its prerequisite → broken nav / invalid DAG entry. Mitigated by a manifest-integrity check
  (gate + unit test) that validates both ID resolution and topological consistency, plus stable
  course-ID slugs.
- **Deep-link fallback gap**: a course without path context renders poorly. Mitigated by a first-class
  canonical view (with prerequisites surfaced) + Gherkin scenario + e2e test.
- **Path rail regresses the generic sidebar** (Screen 3 Option B, DD-46): the rail shares the shipped
  `ResizableSidebar` shell, so a careless implementation could change width persistence, the resize
  handle, or the `md:block` gate for **every** content page, not just courses in path context.
  Mitigated by making the change a **`children` swap only** (no fork, no second `<aside>`, no second
  `localStorage` key), a no-path regression guard test asserting both directions, and a Phase 14
  no-path sweep at all three breakpoints.
- **Rail unusable at the tablet width floor**: at 768 px the `ResizablePanel` 15 % floor is ~115 px, so
  long course titles truncate hard and could make the rail unreadable. Mitigated by the specified
  truncation contract (number + ellipsised title, full title in `aria-label`, phase labels dropped to
  bare rules) and by a dedicated 768 px verification step and hi-fi render.
- **Mobile path context invisible until the drawer is opened**: below `md` the rail is not on screen.
  Mitigated by retaining the `PathBanner` readout at every breakpoint as the always-visible
  "course k of N" signal, with the drawer as the on-demand expansion.
- **URL breakage on re-home**: mitigated by a redirect per re-homed course + redirect specs.
- **Duplication creep**: a path forks a body for framing. Mitigated by callout-only framing, a distinct
  course variant for genuine pedagogy differences, and a no-forked-body check.
- **AI-band duplication creep**: `agentic-ai` and the harness cluster re-teach the same primitives.
  Mitigated by the AI-band scope-guard cross-reference contract.
- **NEW-course quality**: interview modules must meet ayokoding pace/accuracy bars. Mitigated by the
  maker → checker → facts-checker → link-checker pipeline per course.
- **Per-role convergence confusion** (added 2026-07-20): a reader or a future author assumes the
  fourth path converges with the other three, since the plan previously asserted one global endpoint.
  Mitigated by the explicit DD-22 amendment record, cross-referenced from every prose and diagram site
  that made the original single-endpoint claim.
- **Course-surgery blast radius** (added 2026-07-20): a surgery on a shared course (e.g. trimming
  `creating-ai-powered-apps`'s evals section to a forward-link) silently breaks another path's manifest
  or prerequisite chain. Mitigated by DD-28's binding rule: every surgery states its blast radius
  across all four manifests before it is applied, and every affected manifest is re-verified
  prerequisite-consistent afterward.
- **Blanket-redirect swallow / self-recursion** (scope extension): a single
  `/en/c/learn/:path*` → `/en/c/learn/legacy/:path*` rule would swallow `courses/` and `paths/` and
  re-match its own destination. Mitigated by DD-42's explicit per-domain enumeration plus a unit-test
  assertion that no such blanket source exists — the same guard `content-namespace.ts` already carries
  in prose.
- **Redirect-order regression** (scope extension): moving `learnThreeBucketRedirects` in
  `next.config.ts` would either strand historical renames under their pre-rename names or restore a
  three-hop chain. Mitigated by DD-42's stated ordering plus e2e coverage of both the bare and `/c`
  inbound forms and of the `learn-reorg` → bucket chain (URL-mapping row 9).
- **Feed churn on relocation** (scope extension): every relocated item's RSS `<guid>` changes with its
  URL, so subscribers may see ~1,148 items re-surface as new. Accepted as a one-time cost of the move
  and called out in the IA-consequence table; no mitigation exists short of not moving the content.
- **Missing `legacy/_index.md`** (scope extension): without it, `generate-indexes` produces no child
  list and `buildTreeForLocale` synthesizes a `weight: 0` "Legacy" node that sorts **first** in the
  sidebar, ahead of `courses/` and `paths/`. Mitigated by making the authored `_index.md` (with an
  explicit `weight`) a delivery step and a phase-gate check (DD-44).
- **Legacy/course duplication confusion** (scope extension): a reader finds both a legacy page and a
  canonical course on the same subject and cannot tell which is current. Mitigated by
  [Q-D](./tech-docs.md#q-d--seo-treatment-of-legacy)'s recommended per-page "superseded by" banner
  (prd Screen 4); the residual risk is that the banner is only as good as the superseded-by mapping,
  which is why [Q-A](./tech-docs.md#q-a--is-legacy-a-staging-pen-or-a-permanent-archive) recommends
  recording it in the surviving course's `overview.md` rather than in a separate ledger.
