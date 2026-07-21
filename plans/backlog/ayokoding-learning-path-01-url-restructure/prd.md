# Product Requirements — ayokoding-www Learning-Path URL Restructure

## Product Overview

When this plan lands, `/{locale}/c/learn/` has **exactly three** structural buckets and nothing else:

- **`paths/`** — the ordered path manifests' landing anchors, served at
  `/en/c/learn/paths/<arc>/<role-or-subject>`. This plan creates the bucket and its 2×2-grid hub
  landing; the four path landings and the manifests behind them belong to sibling plans.
- **`courses/`** — canonical, path-neutral course bodies in a **flat** namespace, served at
  `/en/c/learn/courses/<course-id>`. This plan re-homes the **33 shipped topics + 4 existing
  capstones** into it, each with a per-course 308 redirect from its old URL, and each declaring
  `prerequisites: [course-id, ...]`.
- **`legacy/`** — everything under `/en/c/learn/` that is not yet a course or a path: the six
  remaining domains (`software-engineering`, `artificial-intelligence`, `information-security`,
  `personal-development`, `it-governance`, `business`; **1,148** `.md` [Repo-grounded]), relocated as
  a **prefix move that preserves each domain's sub-taxonomy verbatim** — no page is rewritten — with
  every relocated URL kept working by a per-domain 308.

Plus the section's own two hub files (`_index.md`, machine-generated; `overview.md`, hand-authored),
which are the section's landing prose, not a fourth taxonomy bucket (DD-40, Q-F).

The product change is **URL topology and information architecture**. It ships one user-facing screen
of its own — **Screen 4**, the legacy-bucket landing and its per-page banner — which runs the full
design funnel below. It ships **no** navigation feature code: the `course-paths` pure core, the path
rail, the path landings, and the manifests all belong to the four sibling plans named in
[README §Depends-on](./README.md#depends-on).

## Personas

Reproduced verbatim from the source plan. All four path personas are carried, not just the ones whose
path this plan touches: every plan's surface is reached by readers of all four paths, and a plan whose
personas live in a sibling folder cannot be reviewed for fit-for-purpose.

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

The persona this plan serves most directly is a **sixth** one, and it is the one the whole plan is
built around:

- **A reader who bookmarked or search-landed on an older learn page** — holds a URL under one of the
  seven current domains, or under `fundamentally-strong/software-engineer/<slug>`. They have no idea a
  reorganization happened and must never discover it as a 404.

## User Stories

- As a **reader browsing `/en/c/learn`**, I want the section to offer exactly three understandable
  choices — follow a path, browse the course library, or dig into the older material — so that I am
  not handed a mixed taxonomy of two structural buckets sitting beside six subject domains.
- As a **reader who bookmarked or search-landed on an older learn page**, I want my URL to keep
  working after the section is reorganized, so that no link I hold or that Google holds ever 404s.
- As a **reader who bookmarked a `fundamentally-strong/software-engineer/<slug>` topic**, I want that
  URL to land me on the same material at its new canonical course address, so that the collapse into
  a flat course namespace is invisible to me.
- As a **reader who lands on an older, not-yet-converted page**, I want to see that it is legacy
  material and where the canonical course lives (if one exists), so that I do not study a superseded
  page believing it is current.
- As a **reader who navigated the material the old way**, I want the hand-curated, spiral-ordered
  section index to keep working after the topics move, so that the navigation I already know is not
  taken away from me by an additive change.
- As the **maintainer**, I want the legacy relocation to be a pure prefix move that rewrites no page
  bodies, so that a 1,148-file change stays reviewable as a rename diff and carries no content risk.
- As the **maintainer**, I want each course authored **once**, path-neutral, at one canonical URL, so
  that a fix or update benefits every referencing path with zero duplication.
- As the **maintainer**, I want every re-homed course to declare its prerequisites in its canonical
  metadata, so that the library forms a prerequisite DAG the manifest plan can validate against.
- As a **future author**, I want an unambiguous rule for where a new page belongs — a path, a course,
  or legacy — so that the section's shape does not drift one judgment call at a time.
- As the **maintainer**, I want the `id` locale's deferral recorded as a decision rather than left as
  an omission, so that a later reader of a bilingual app does not read the asymmetry as a bug.

Journey context: the end-to-end learner arc (Landing → Discovery → Before → During → After) is
documented by `ayokoding-learning-path-03-navigation-ui` in its `prd.md` §Learner Journey, the plan
that builds and populates that journey. This plan supplies the URL substrate the journey walks over
and does not restate it.

## UI-Design-Funnel — Screen 4 · Legacy-bucket landing and page banner

This plan is **UI-bearing**: it adds one user-facing screen (the `/en/c/learn/legacy` landing) and,
under [Q-D](./tech-docs.md#q-d--seo-treatment-of-legacy)'s recommended answer, a per-page
**"legacy / superseded"** banner on relocated pages. Both run the funnel — with one honest difference
recorded up front: **the selection is pending the Q-D ruling.** The low-fi alternatives below map 1:1
to Q-D's options, and the two hi-fi finalists are produced by a `delivery.md` Phase 3 step (matching
the pattern the source plan used for Screens 0–3), not fabricated here for an undecided design.

Screens 0–3 (landing hero, paths hub, path landing, course-in-path) belong to
`ayokoding-learning-path-03-navigation-ui` — that plan carries their funnel record and their 24
renders. This plan carries Screen 4 and its 6.

**R5 grounding note** — no net-new component is required. The banner is the existing composite
`Alert` (`Alert` / `AlertTitle` / `AlertDescription` from `@open-sharia-enterprise/web-ui`, the same
primitive the navigation plan's Screen 2 fast-path callout uses); the landing is an ordinary content
`_index.md` rendered by the existing `/c/[...slug]` route with the existing `Breadcrumb` +
`MarkdownRenderer` [Repo-grounded —
`apps/ayokoding-www/src/app/[locale]/(content)/c/[...slug]/page.tsx`]. **Zero new components; zero
navigation code changes** (DD-44).

**R7 prior-art citation** — the alternatives are informed by how comparable documentation and course
platforms signal superseded material: versioned-docs banners ("You are viewing the docs for an older
version"), archive notices on retired knowledge bases, and `noindex`-ed legacy trees. The source
plan's `web-researcher` window-shop of ~14 learning platforms (2026-07-21) is carried by
`ayokoding-learning-path-03-navigation-ui` in its R7 Prior-Art Findings section; the finding relevant
here is that **no surveyed platform de-indexes superseded material while the replacement is still
being written** — which is the decisive argument against Option C below.

### Low-fi Option A — Indexed, with a landing notice + a per-page banner (Recommended; Q-D option A)

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

### Low-fi Option B — Indexed, landing notice only, no per-page banner (Q-D option B)

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

### Low-fi Option C — `noindex` the bucket, minimal landing (Q-D option C)

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

### Responsive strategy (mobile ↔ tablet ↔ desktop, mobile-first)

Mobile-first. The landing's six domain links render as a **single-column stacked list** below `md`
and a **two-column list** at `md+` (≥768 px); they never become a card grid, because they are
navigational links into an archive, not promoted destinations competing with the four path cards. The
`Alert` notice is full-width at every breakpoint, wrapping to three lines on mobile and one to two on
desktop. The per-page banner (Option A) sits **above** the H1 and **below** the breadcrumb at every
breakpoint, so it is never pushed off a phone's first screen; its "superseded by" link wraps to its
own line below `sm` rather than truncating. The breadcrumb gains one segment (`Legacy`) — on mobile
the existing `Breadcrumb` already handles overflow, and the verification step in Phase 3 explicitly
checks for **no multi-line breadcrumb wrap at 375 px**.

| Breakpoint            | Domain list                     | Notice / banner                              | Sidebar                       |
| --------------------- | ------------------------------- | -------------------------------------------- | ----------------------------- |
| Mobile (`< md`, 375)  | single-column stacked list      | full-width, ~3 lines; link wraps to own line | drawer only (`MobileNav`)     |
| Tablet (`md`, 768)    | two-column (`md:grid-cols-2`)   | full-width, ~2 lines                         | `ResizableSidebar` visible    |
| Desktop (`lg+`, 1280) | two/three-column, single screen | full-width, 1–2 lines                        | `ResizableSidebar` full width |

A desktop-only design is not a valid finalist here: the decisive failure mode of Option B is
specifically the **mobile search-landed reader**, who never sees the landing and therefore never sees
the only place the warning lives.

### Hi-fi finalists

Produced by `delivery.md` Phase 3 as **six** files following the
[asset matrix](#hi-fi-asset-matrix--this-plans-slice) scheme —
`assets/legacy-landing-option-{a,b}-{mobile,tablet,desktop}.png`, rendered at 375 / 768 / 1280 px
from token-accurate HTML mockups under `assets/src/`, exactly as the navigation plan's Screen 0–3
finalists are. Option C is **not** carried to hi-fi: it is Option B's landing with a `robots` metadata
change, which a mockup cannot show.

The six `![]()` embeds are added by the Phase 3 embed step, not authored here — embedding a link to a
file that does not exist yet would fail link validation on this plan's first push.

### Selection and rationale

**Selection: PENDING the [Q-D](./tech-docs.md#q-d--seo-treatment-of-legacy) ruling.** Option A is the
recommendation carried into Phase 3. The rationale table records why each option would win or lose, so
an overturned ruling is a bounded edit rather than a re-run of the funnel:

| Design                                        | Why it would win / lose                                                                                                                                          |
| --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A — indexed + landing notice + page banner ⭐ | Preserves ~1,148 pages of search surface **and** warns the reader per page; reuses `Alert`; reversible to C in one metadata change                               |
| B — indexed, landing notice only              | Cheapest, but a search-landed reader never reaches the landing, so the one place the warning lives is the one place they never see                               |
| C — `noindex` the bucket                      | Cleanest signal that the material is superseded, but discards the app's largest search surface **before** the 127-course catalog exists (~37 bodies built today) |

**A11y (all options)** — the notice and banner are semantic `Alert` regions with real text, never
colour alone; "Legacy" is a text breadcrumb segment, not an icon; the "superseded by" link names the
destination course explicitly rather than reading "here".

### Hi-fi asset matrix — this plan's slice

Naming scheme (inherited, DD-47) — `assets/<screen>-option-<a|b>-<mobile|tablet|desktop>.png`,
rendered from a token-accurate source at `assets/src/<same-stem>.html`. Screen slugs: `landing-hero`
(0), `paths-hub` (1), `path-landing` (2), `course-path` (3), `legacy-landing` (4).

| Screen | Slug             | Option × viewport | Renders | Owning plan                                  |
| ------ | ---------------- | ----------------- | ------- | -------------------------------------------- |
| 0–3    | see scheme above | 2 × 3 each        | **24**  | `ayokoding-learning-path-03-navigation-ui`   |
| 4      | `legacy-landing` | 2 × 3             | **6**   | `ayokoding-learning-path-01-url-restructure` |

> **Cross-plan note on DD-47.** DD-47 mandates **30** renders (5 screens × 2 options × 3 viewports)
> across two plans — **6 here** and **24 in `ayokoding-learning-path-03-navigation-ui`**. A reader
> auditing DD-47 against this plan alone must not conclude the matrix was under-delivered. Every
> asset-count acceptance clause in this plan therefore asserts **6**, scoped to this plan's own
> `assets/` folder, and never 30.

## Acceptance Criteria (Gherkin)

Fourteen scenarios. Twelve are inherited whole from the source plan; two are additions made at split
time and flagged below. Each scenario uses exactly one primary `Given`/`When`/`Then`; extras chain
with `And`. Every scenario is bound to a delivery step in [delivery.md](./delivery.md) — none is left
unbound.

### Re-home and per-course redirects

```gherkin
Scenario: A legacy fundamentally-strong URL redirects to the canonical course URL
  Given a re-homed course previously lived under the legacy fundamentally-strong/software-engineer content path
  When a reader requests the legacy URL
  Then the app redirects to the course's canonical /en/c/learn/courses/<course-id> URL
  And the redirect preserves any path context query parameter
```

```gherkin
Scenario: Every re-homed course declares its prerequisites
  Given the thirty-seven shipped topics and existing capstones have been re-homed into the course library
  When each re-homed course's canonical metadata is inspected
  Then every one declares a prerequisites list of course IDs
  And an empty list is accepted only for a course with no library prerequisite
  And every named prerequisite resolves to another course in the library
```

> _Provenance_: the "Every re-homed course declares its prerequisites" scenario is **new at split
> time**. The source plan asserted the frontmatter contract only as a checklist acceptance clause,
> never as Gherkin, while the scenario that consumed it ("A course page surfaces its declared
> prerequisites") spanned three plans. That scenario was split three ways; this is this plan's share.

```gherkin
Scenario: The legacy section-index browse still resolves after re-homing
  Given the 33 shipped topics have been re-homed into the course library
  When a reader browses the legacy fundamentally-strong software-engineer section index the old way
  Then every section-index entry links to live content at its /en/c/learn/courses/<course-id> URL or via a redirect
  And no legacy section-index entry resolves to a drained or missing location
```

```gherkin
Scenario: The legacy section-index browse resolves to the canonical course body
  Given a course now lives at its canonical /en/c/learn/courses/<course-id> URL
  When a reader reaches it via the legacy section-index browse
  Then the browse resolves to that single canonical course body
  And no forked or duplicated body is served for the legacy route
```

> _Provenance_: the source plan's "Old-way and new-way navigation coexist" scenario asserted that the
> legacy browse **and** a `/en/c/learn/paths/<path-id>` path landing resolve to one canonical body.
> The path-landing half needs a published manifest and a landing renderer, neither of which exists in
> this plan. The scenario was therefore **split in two**: this plan keeps the narrowed legacy-browse
> half above, and `ayokoding-learning-path-05-manifests` gains the both-routes scenario at its
> first-manifest gate. Merging this plan with the navigation plan to keep the original whole was
> rejected: it would collapse Wave 1 into Wave 2 and destroy the parallelism the split exists to buy.

### Three-bucket learn-section IA

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

### Build health

```gherkin
Scenario: The relocated tree builds and validates green
  Given the re-home, the six-domain relocation, and both redirect modules have landed
  When the ayokoding-www build, the unit and e2e tiers, and the link and heading validators run
  Then the build and every tier succeed
  And link, heading-hierarchy, and markdownlint validation report no errors
```

> _Provenance_: the source plan carried one composite scenario, "The app builds and validates green",
> whose `Given` conjoined the navigation feature **and** the interview-ready path — a conjunction
> spanning two plans by construction, binding no delivery step. It was **decomposed** at split time:
> each of the five split plans writes its own scoped build-green scenario naming its own surface. The
> scenario above is this plan's.

## Product Scope

**In-scope features**:

- Re-homing the **33 shipped topics + 4 existing capstones** (including `capstone-solid-core`, DD-20)
  from `fundamentally-strong/software-engineer/<slug>/` into the flat `courses/<course-id>/`
  namespace, preserving each full page-bundle.
- A **per-course 308 redirect** for each of the 37 re-homed bundles, under
  `apps/ayokoding-www/src/redirects/`, with a unit test asserting all 37 mappings and the absence of
  any bucket rule for the `fundamentally-strong` prefix.
- Adding `prerequisites: [course-id, ...]` frontmatter to each re-homed course `_index.md`, in the
  shape owned by `ayokoding-learning-path-02-schema-and-prerequisite-dag`.
- Preserving the **additive "old-way" `_index.md` section browse** (DD-19): every impacted legacy
  section index is UPDATED, never deleted, re-pointing each entry at the canonical course URL.
- The two **content homes**: `courses/_index.md` (library landing) and `paths/_index.md` (paths hub /
  choose-a-path landing whose 2×2-grid layout has room for all four paths, populated as each ships).
- The **`legacy/` bucket**: prefix-relocating the six non-course `en/learn/` domains (1,148 `.md`) via
  a pure `git mv` per domain (DD-40/DD-41).
- A new **per-domain 308 redirect module** `src/redirects/learn-three-bucket.ts` (12 rules: 6 domains
  × 2 inbound tiers) with its unit test, wired into `next.config.ts` in the load-bearing order
  (DD-42).
- The authored **`legacy/_index.md`** landing (DD-44) and the rewritten hand-authored
  `en/learn/overview.md` (DD-45/Q-F); regeneration of `en/learn/_index.md` and
  `generated/search-data.json`.
- The **Screen 4 design funnel** for the legacy landing and per-page banner, with its 6 renders.
- A `specs/` Gherkin companion under the existing `navigation/` domain folder, plus e2e coverage of
  both inbound redirect forms and both negative cases.

**Out-of-scope features**:

- The `course-paths` feature — pure core (`schemas.ts`, `path-nav.ts`, `path-context.ts`,
  `prerequisites.ts`, `manifest-integrity.ts`) and shell (`manifest-repository.ts`,
  `path-landing.tsx`, `path-card.tsx`, `path-rail.tsx`, `path-banner.tsx`, `prerequisite-list.tsx`,
  `path-course-links.tsx`).
- The `PathManifest` zod schema, the `<MANIFESTS>` directory, and **every** manifest file.
- Path landing pages, the `?path=` route wiring, path-aware prev/next, and the path breadcrumb.
- Screens 0–3 of the design funnel and their 24 renders.
- Authoring **any** course body: the 61 transferred topics, the 6 net-new AI courses, the remaining
  new courses and capstones.
- Rewriting, merging, re-titling, or re-sequencing any legacy page — the move is a prefix relocation
  only (DD-41).
- Promoting legacy pages into real `courses/` bodies — later work, tracked per
  [Q-A](./tech-docs.md#q-a--is-legacy-a-staging-pen-or-a-permanent-archive).
- Extending the three-bucket shape to the `id` locale — deferred and recorded explicitly (DD-45,
  [Q-B](./tech-docs.md#q-b--does-the-id-locale-get-the-same-three-bucket-shape-now)).

## Product-Level Risks

- **URL breakage on re-home**: 37 live production URLs move at once. Mitigated by landing the
  per-course redirect table **in the same phase as the move**, asserted over all 37 mappings by a unit
  test before the phase gate closes, and by an e2e assertion on a real legacy URL.
- **Blanket-redirect swallow / self-recursion**: a single `/en/c/learn/:path*` →
  `/en/c/learn/legacy/:path*` rule would swallow `courses/` and `paths/` and re-match its own
  destination. Mitigated by DD-42's explicit per-domain enumeration plus a unit-test assertion that no
  such blanket source exists — the same guard `content-namespace.ts` already carries in prose.
- **`fundamentally-strong` shadowing**: a `fundamentally-strong` prefix rule in the bucket module
  would shadow the per-course rules for all 37 already-built directories, silently sending every
  re-homed course to a legacy URL that holds nothing. Mitigated by DD-43's explicit exclusion and a
  negative unit assertion — writable only because this plan owns both rule sets.
- **Redirect-order regression**: moving `learnThreeBucketRedirects` in `next.config.ts` would either
  strand historical renames under their pre-rename names or restore a three-hop chain. Mitigated by
  DD-42's stated ordering plus e2e coverage of both inbound forms and of the `learn-reorg` → bucket
  chain (URL-mapping row 9), re-asserted as a standing check in Phase 4.
- **Missing `legacy/_index.md`**: without it, `generate-indexes` produces no child list and
  `buildTreeForLocale` synthesizes a `weight: 0` "Legacy" node that sorts **first** in the sidebar,
  ahead of `courses/` and `paths/`. Mitigated by making the authored `_index.md` (with an explicit
  `weight`) a delivery step and a phase-gate check (DD-44).
- **Legacy/course duplication confusion**: a reader finds both a legacy page and a canonical course on
  the same subject and cannot tell which is current. Mitigated by
  [Q-D](./tech-docs.md#q-d--seo-treatment-of-legacy)'s recommended per-page "superseded by" banner
  (Screen 4); the residual risk is that the banner is only as good as the superseded-by mapping, which
  is why [Q-A](./tech-docs.md#q-a--is-legacy-a-staging-pen-or-a-permanent-archive) recommends
  recording it in the surviving course's `overview.md` rather than in a separate ledger.
- **Feed churn on relocation**: every relocated item's RSS `<guid>` changes with its URL, so
  subscribers may see ~1,148 items re-surface as new. Accepted as a one-time cost of the move and
  called out in the IA-consequence table; no mitigation exists short of not moving the content.
- **Navigation regresses for non-path readers**: the relocation is one of two ways the sidebar can
  regress. Mitigated by the IA being entirely tree-derived (DD-44 — zero production code edits beyond
  the redirect module) plus a no-path sweep at all three breakpoints in Phase 5. The **other** way —
  the path rail sharing the shipped `ResizableSidebar` — is guarded by
  `ayokoding-learning-path-03-navigation-ui`, which owns that component and that risk.
- **A prerequisite-frontmatter shape mismatch across Wave 1**: this plan writes
  `prerequisites:` into 37 files while the sibling schema plan writes the resolver that parses it.
  The field is inert until a Wave-2 consumer reads it, so **nothing fails in Wave 1** — a mismatch
  would surface later as an empty prerequisite list on 37 course pages with a green build. Mitigated
  by reproducing the contract verbatim in both plans' `tech-docs.md`, with the schema plan named
  canonical.
- **Q-D is overturned after the funnel is drawn**: the selection is recorded as PENDING and the
  rationale table names why each option would win or lose, so an overturned ruling is a bounded edit
  (a metadata change plus a notice edit) rather than a re-run of the funnel.
- **A DD-47 auditor reads this plan's 6 renders as under-delivery**: mitigated by the cross-plan note
  in the asset matrix above and by the same note repeated in the archival phase.
