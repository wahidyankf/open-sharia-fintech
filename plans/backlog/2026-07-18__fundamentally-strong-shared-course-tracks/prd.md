# Product Requirements — Fundamentally Strong Shared Course Library, Two Tracks

## Product Overview

The "Fundamentally Strong" curriculum becomes a **shared course library** (one canonical body per
course, keyed by a stable course ID) consumed by **two learning paths**:

- **`software-engineer`** — the **shipping-first** arc: editor/tooling → one language end-to-end →
  **build a real app first** → then CS fundamentals / data structures / algorithms / systems depth.
- **`job-seeking-software-engineer`** — the **interview-first** arc for an experienced engineer
  re-entering the job market.

A **path is an ordered manifest** referencing course IDs. Courses are shared with **omit-or-create**
semantics; no body is duplicated or forked per path. This plan also delivers the **ayokoding-www
path-aware navigation UI** that makes one canonical course URL behave differently under each path's
context. The library body is largely content (exempt from `specs:coverage`); the **navigation feature
is app code** and carries a `specs/` Gherkin companion and three-level tests.

The topic content of the 97 existing courses (94 topics + 3 existing capstones) is unchanged — they
are **re-homed** (moved to
`courses/<course-id>/` with redirects) and **re-framed** (referenced by two manifests), not rewritten.
This plan additionally **authors fourteen NEW courses + three NEW capstones** the interview and
productivity/harness/security clusters need.

## Personas

- **Experienced engineer re-entering the job market (north-star for the `job-seeking` path)** —
  recently laid off, returning from a gap/sabbatical, or an employed senior wanting to switch. Already
  owns the editor workflow and deep fundamentals; needs to **refresh breadth fast, relearn interview
  technique** at mid/senior/staff level, and handle a **layoff / employment-gap narrative** — without
  walking a from-scratch curriculum.
- **A builder who wants to be effective fast (north-star for the `software-engineer` path)** — wants
  "immediately effective" SWE: set up the editor, learn one language end-to-end, **ship a real app
  early**, then deepen into CS fundamentals, DS&A, algorithms, and systems. Serves both a from-scratch
  learner and a mid-career switcher.
- **A reader who lands on a shared course by deep-link / share** — arrives at a course URL without a
  path context and must get a coherent standalone view plus an obvious way to enter a path.
- **Maintainer (content strategist / frontend engineer / content author / reviewer)** — owns the
  two-path architecture, builds the navigation feature, and authors the NEW courses via the ayokoding
  maker agents.

## User Stories

- As a **builder new to software engineering**, I want a shipping-first path that gets me productive
  and shipping a real app fast before deep theory, so that I stay motivated and learn depth once I
  feel the payoff.
- As an **experienced engineer re-entering the market**, I want an interview-first path with real
  technique modules and a layoff/gap-narrative section, so that I get interview-ready fast at my
  level.
- As a **reader on the shipping-first `software-engineer` path who decides to job-hunt**, I want an
  optional "ready to job-hunt?" bridge at the end of my path that flows me into the interview-technique
  courses, so that I can pivot to interview prep without leaving my path or duplicating any course.
- As a **reader on either path**, I want prev/next and the breadcrumb to follow **my path's order**,
  so that "next" always means the next course in the arc I chose.
- As a **reader who shares or deep-links a course**, I want the course to render coherently with no
  path context, so that a shared link never breaks — and to see which paths include this course.
- As the **maintainer**, I want each course authored **once** and referenced by both paths, so that
  a fix or update benefits both paths with zero duplication.
- As the **maintainer**, I want a path to **omit** a course that does not fit and **create** a new
  course only for a real gap, so that each path stays coherent without forking bodies.
- As a **reader targeting an AI-agent-infra or security codebase**, I want the async-Python/FastAPI,
  CDP, MCP/harness, C++, and detection-engineering courses available in the library, so that either
  path can lead me to the stack skills those codebases need.
- As a **screen-reader / keyboard user**, I want the path banner, breadcrumb, and prev/next to be
  fully accessible, so that path-aware navigation works without a mouse.

## UI-Design-Funnel (Path-Aware Navigation Screens)

The path-aware navigation adds/changes **three user-facing screens** in `ayokoding-www` (a Next.js
app). Each screen runs the diverge → narrow → select → justify funnel. Low-fidelity wireframes are
authored below; the two high-fidelity finalists per screen are produced as `.excalidraw.png` assets
under this plan's `assets/` during Group A (delivery steps emit them) and embedded here.

> **Pending assets note**: this plan is in `backlog/` — the six `![]()` hi-fi finalist image links
> below (two per screen, Screens 1-3) intentionally do not resolve yet. `delivery.md` Phase 1
> ("Produce hi-fi finalists") produces the `.excalidraw.png` files into `assets/` before Phase 2 code
> work begins. A broken link here today is expected, not a mistake.

**R5 grounding note (all screens)** — before drafting, survey the existing UI to reuse rather than
reinvent: `libs/web-ui` component inventory + tokens + Storybook; the ayokoding app-shell
(`apps/ayokoding-www/src/features/app-shell/`); the existing `sidebar-tree`, `breadcrumb`,
`prev-next`, and `section-card` components [Repo-grounded —
`apps/ayokoding-www/src/features/navigation/shell/` and `.../content/shell/section-card.tsx`].
Reference the `swe-developing-frontend-ui` skill. **Net-new components**: `PathCard`, `PathLanding`,
`PathBanner`, `PathCourseLinks` — all composed from existing `libs/web-ui` primitives; named in
[tech-docs §New feature: `course-paths`](./tech-docs.md#new-feature-course-paths-functional-core--imperative-shell).

**R7 prior-art citation (all screens)** — consult, via `web-researcher` at Group-A authoring time,
how comparable learning platforms present a "track/path over shared lessons" (e.g. roadmap.sh track
pages, Exercism tracks, freeCodeCamp curriculum, Coursera specialization/path pages) so the
alternatives are informed rather than invented. [Needs Verification — delegate before authoring.]

> **Provisional-diverge note**: the R7 prior-art survey has **not** run yet — it is scheduled as a
> `delivery.md` Phase 1 step (`delivery.md` §Phase 1, `web-researcher` delegation). The Screens 1-3
> low-fi alternatives, selections, and rationales below were therefore drafted **without** prior-art
> input and are **provisional**: Phase 1 re-runs the diverge/select stages against the R7 findings
> before the hi-fi finalists are produced, and may replace an alternative, change the selection, or
> add a new option if the survey surfaces a materially better pattern. Do not treat the "Selected:"
> lines below as prior-art-informed until Phase 1's R7 sweep lands (with inline excerpt + URL +
> access date per the Anti-Hallucination convention).

### Screen 1 · Paths hub ("choose your path")

Entry screen at `/fundamentally-strong` (or `/fundamentally-strong/paths`) offering the two paths.

**Low-fi Option A — Two side-by-side path cards (Recommended)**

```text
┌───────────────────────── Fundamentally Strong ─────────────────────────┐
│  Choose your path. Same course library, two orders.                     │
│                                                                          │
│  ┌───────────────────────────┐   ┌───────────────────────────┐          │
│  │ Software Engineer          │   │ Job-Seeking Software Eng. │          │
│  │ Shipping-first             │   │ Interview-first            │          │
│  │ Ship a real app fast, then │   │ Get interview-ready fast   │          │
│  │ go deep.                   │   │ (experienced re-entrant).  │          │
│  │ ~N courses · 4 stages      │   │ ~N courses · prologue+3    │          │
│  │ [ Start this path → ]      │   │ [ Start this path → ]      │          │
│  └───────────────────────────┘   └───────────────────────────┘          │
│                                                                          │
│  Or browse the full course library →                                     │
└──────────────────────────────────────────────────────────────────────────┘
```

**Low-fi Option B — Stacked comparison rows**

```text
┌───────────────── Fundamentally Strong · Two Paths ─────────────────┐
│ Software Engineer (shipping-first)   [ Start → ]  ~N courses        │
│   editor → one language → BUILD APP → CS depth                     │
│ ─────────────────────────────────────────────────────────────────  │
│ Job-Seeking SWE (interview-first)    [ Start → ]  ~N courses        │
│   prologue → interview prep → platforms → deepening                │
└─────────────────────────────────────────────────────────────────────┘
```

**Responsive (mobile ↔ desktop)** — Option A shows two cards side-by-side at `lg` (≥1024px) and
`md` (≥768px, two columns), and **stacks to one column** below `sm`. The "Start this path" CTA is a
full-width tap target on mobile.

**Hi-fi finalists**: `![Paths hub — side-by-side cards](./assets/paths-hub-option-a.excalidraw.png)`
and `![Paths hub — stacked comparison](./assets/paths-hub-option-b.excalidraw.png)`.

**Selected: Option A — Two side-by-side path cards.**

| Design                    | Why it won / lost                                                                      |
| ------------------------- | -------------------------------------------------------------------------------------- |
| A — side-by-side cards ✅ | Two equal, scannable choices; reuses `section-card`; reflows cleanly to stacked mobile |
| B — stacked comparison    | Denser, but buries the second path below the fold on mobile and reads as a ranking     |

### Screen 2 · Path landing page

At `/fundamentally-strong/paths/<path-id>` — the manifest rendered as an ordered, phase-grouped
course list; every course link carries `?path=<path-id>`.

**Low-fi Option A — Phase-grouped numbered syllabus (Recommended)**

```text
┌──────────── Job-Seeking Software Engineer · interview-first ────────────┐
│ Experienced & job-hunting? Skip the prologue → jump to Phase 1.          │
│                                                                          │
│ Prologue · Editor Foundations (skippable)                                │
│   1. Just Enough Nvim        2. Just Enough Lua     3. Extending Neovim   │
│   ▸ Capstone · Forge-Ready                                                │
│ Phase 1 · Interview Preparation                                          │
│   4. Just Enough Python …  9. Coding Interview  … 16. Behavioral         │
│   ▸ Capstone · Interview Loop                                            │
│ Phase 2 · Multi-Platform Productivity …                                  │
│ Phase 3 · Deepening …                                                    │
└──────────────────────────────────────────────────────────────────────────┘
```

**Low-fi Option B — Collapsible phase accordion**

```text
┌──────────── Software Engineer · shipping-first ────────────┐
│ ▼ Stage 1 · Editor & tooling            (7 courses)         │
│ ▼ Stage 2 · One language → BUILD A REAL APP  (11 courses)   │
│ ▶ Stage 3 · CS fundamentals, DS&A, algorithms (collapsed)   │
│ ▶ Stage 4 · Systems, data, security, ops (collapsed)        │
└─────────────────────────────────────────────────────────────┘
```

**Responsive (mobile ↔ desktop)** — Option A renders the numbered list full-width single-column on
mobile (each course a full-width row) and a comfortable reading column on desktop; the fast-path
callout stays pinned at the top. Phase headings are sticky sub-headers on desktop, inline on mobile.
Option B's accordion collapses all but the first stage on mobile to keep the list short.

**Hi-fi finalists**: `![Path landing — numbered syllabus](./assets/path-landing-option-a.excalidraw.png)`
and `![Path landing — phase accordion](./assets/path-landing-option-b.excalidraw.png)`.

**Selected: Option A — Phase-grouped numbered syllabus.**

| Design                   | Why it won / lost                                                                   |
| ------------------------ | ----------------------------------------------------------------------------------- |
| A — numbered syllabus ✅ | Shows the whole ordered arc at a glance; the number IS the path order; SEO-friendly |
| B — phase accordion      | Compact, but hides the arc behind collapsed sections and adds interaction cost      |

### Screen 3 · Course page in path context

A shared course body rendered with the active path's affordances: a top **path banner** (path name +
position), a path breadcrumb, and manifest-driven prev/next. Without `?path=` → canonical view.

**Low-fi Option A — Top path banner + path breadcrumb + bottom prev/next (Recommended)**

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ ▸ On path: Job-Seeking SWE · course 9 of N          [ view full path ]    │
│ Home / Fundamentally Strong / Job-Seeking SWE / Coding Interview          │
│                                                                          │
│ # Coding Interview                                                        │
│ …course body (unchanged, canonical)…                                      │
│                                                                          │
│ ← Prev: Advanced Algorithms        Next: Take-Home & Live Coding →        │
│   (both links keep ?path=job-seeking-software-engineer)                    │
└──────────────────────────────────────────────────────────────────────────┘
```

Canonical fallback (no `?path=`):

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ Home / Fundamentally Strong / Courses / Coding Interview                   │
│ # Coding Interview … body …                                               │
│ This course is part of: [ Software Engineer ] · [ Job-Seeking SWE ]       │
└──────────────────────────────────────────────────────────────────────────┘
```

**Low-fi Option B — Left path rail replacing the sidebar**

```text
┌── Path rail ──┬────────────────────────────────────────────────┐
│ Job-Seeking   │ Home / … / Coding Interview                     │
│ ▸ 9 Coding ●  │ # Coding Interview … body …                     │
│   10 Take-home│ ← Prev … Next → (?path kept)                    │
└───────────────┴──────────────────────────────────────────────────┘
```

**Responsive (mobile ↔ desktop)** — Option A's path banner is a full-width strip on all breakpoints;
prev/next stack vertically below `sm` and sit left/right at `sm+` (mirrors the existing `PrevNext`
component [Repo-grounded]). Option B's left rail is desktop-only and would need to collapse into a
top sheet on mobile — extra complexity, so Option A wins on mobile-first grounds.

**Hi-fi finalists**: `![Course in path — top banner](./assets/course-path-option-a.excalidraw.png)`
and `![Course in path — left rail](./assets/course-path-option-b.excalidraw.png)`.

**Selected: Option A — Top path banner + path breadcrumb + bottom prev/next.**

| Design             | Why it won / lost                                                                              |
| ------------------ | ---------------------------------------------------------------------------------------------- |
| A — top banner ✅  | Minimal change to the existing content layout; reuses `breadcrumb` + `prev-next`; mobile-first |
| B — left path rail | Rich, but a desktop-only pattern that fights the existing sidebar and needs a mobile sheet     |

## Acceptance Criteria (Gherkin)

Navigation-feature scenarios are the source of the `specs/` Gherkin companion (app code). Content and
path-ordering scenarios document behavior. Each scenario uses exactly one primary Given/When/Then;
extras chain with And. The 14 scenarios below cover the `course-paths` navigation feature; 6 more
course-specific acceptance scenarios appear further down, under
[NEW Course & Capstone Specifications](#new-course--capstone-specifications).

```gherkin
Scenario: A path landing page lists its courses in manifest order
  Given the job-seeking-software-engineer path manifest is published
  When a reader opens the path landing page
  Then the courses appear in the manifest's courseOrder
  And every course link carries the path context query parameter
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
  Then it shows Home, Fundamentally Strong, the path title, and the course title
  And the path crumb links to the path landing page with the path context preserved
```

```gherkin
Scenario: A course deep-linked without path context renders the canonical view
  Given a reader opens a course URL with no path context query parameter
  When the course page renders
  Then the course body renders in full with the content-tree breadcrumb
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
  And the path banner is not shown for that path
```

```gherkin
Scenario: An old software-engineer URL redirects to the canonical course URL
  Given a re-homed course previously lived under the software-engineer content path
  When a reader requests the old URL
  Then the app redirects to the course's canonical /courses/<course-id> URL
  And the redirect preserves any path context query parameter
```

```gherkin
Scenario: Both paths reference a shared course with no body duplication
  Given a course appears in both path manifests
  When the course library is inspected
  Then exactly one canonical body exists for that course
  And each manifest references the course by its stable course ID
```

```gherkin
Scenario: Every manifest course reference resolves to a real course
  Given a path manifest lists a courseOrder of course IDs
  When the manifest-integrity check runs
  Then every listed course ID resolves to an existing course in the library
  And no course ID appears more than once in the manifest
```

```gherkin
Scenario: The job-seeking path ships before the software-engineer path
  Given the job-seeking-software-engineer path is delivered end-to-end
  When the software-engineer path work begins
  Then the job-seeking path landing, courses, manifest, and nav are already live in production
  And the software-engineer path reuses the shared courses without duplicating any body
```

```gherkin
Scenario: The software-engineer path is shipping-first
  Given the software-engineer path manifest is published
  When a reader walks the path
  Then editor/tooling, one language end-to-end, and building a real app precede the CS-fundamentals and DS&A courses
  And the reader ships a real deployed app before any pure-theory course
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
  When they navigate the path banner, breadcrumb, and prev/next
  Then each is a labelled landmark reachable and operable by keyboard with visible focus
  And the document language attribute matches the active locale
```

```gherkin
Scenario: The app builds and validates green
  Given the navigation feature and both paths are complete
  When nx run ayokoding-www:build, the three test tiers, and the link/heading validators run
  Then the build and all tiers succeed
  And link, heading-hierarchy, and markdownlint validation report no errors
```

## NEW Course & Capstone Specifications

This plan authors **fourteen NEW courses + three NEW capstones** into the library. Each is a full
page-bundle (learning track + drilling track) matching the sibling plan's per-topic anatomy and
inheriting its cross-cutting authoring guarantees verbatim (accuracy-verified via `web-researcher`
before authoring; follow-along-complete; typed-Python where Python; colocated runnable `code/`;
exhaustive `co-NN`/`ex-NN` enumeration; prerequisites + navigation). Full per-course concept/example/
capstone detail lives in the [syllabus](./syllabus/overview.md) detail files (one file per course ID);
the specs below fix each course's purpose, register, and acceptance shape.

**Register.** The four interview-technique courses use a **refresh register** (assume prior
professional experience; reload technique, do not teach from zero). The ten productivity/harness/
security courses use the normal **first-learn By-Example register**; `just-enough-cpp` is primer scope.

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
- **`self-hosting-essentials`** (By Example · ops/config) — **light** on-ramp: one box, containerize,
  reverse proxy + TLS, systemd/ports, env/secrets, backups, PaaS git-push. Strictly below
  `containers-and-orchestration` / `cloud-and-iac`; distinct from `bare-metal-virtualization`.
- **`browser-automation-with-cdp`** (By Example · Python) — Chrome DevTools Protocol browser
  automation (port 9222; nodriver/zendriver family) — the core `remotebrowser` skill.

```gherkin
Scenario: The light self-hosting course stays below clusters and IaC
  Given the self-hosting-essentials course is authored
  When a reader compares it with containers-and-orchestration and cloud-and-iac
  Then it teaches running one box, containerizing a service, a reverse proxy, and PaaS git-push deploy
  And its overview explicitly excludes clusters, Terraform/Packer/Ansible IaC, and Proxmox
```

### Harness-engineering cluster (first-learn By-Example · Python)

The five build-your-own-agentic-coding-tool courses; the MCP built in `agent-tools-and-mcp` is the
same MCP `remotebrowser` exposes; all feed `capstone-build-your-own-coding-agent`.

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

### Security & systems gap-closers

- **`just-enough-cpp`** (Primer · C++) — systems-language principle on-ramp (RAII, templates/generics,
  STL, smart pointers, manual memory); prereq `just-enough-c`; Wazuh's C++ core is one illustration.
- **`detection-engineering-and-siem-operations`** (By Example · XML/rules + config + Python) —
  decoders, correlation rules, log parsing/normalization, FP tuning, dashboards, alert triage; Wazuh
  XML is the worked example; distinct from concept-level `defensive-security`; prereq
  `defensive-security`.

```gherkin
Scenario: Hands-on detection engineering stays distinct from concept-level defensive security
  Given the detection-engineering-and-siem-operations course is authored
  When a reader compares it with the concept-level defensive-security course
  Then it has the reader author working decoders, correlation rules, and a dashboard with false-positive tuning
  And it uses the Wazuh XML ruleset only as the worked example, not the subject
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
  `?path=` context, graceful fallback, path landing pages, a paths hub, redirects, accessibility.
- Re-homing the 94 existing topics + 3 existing capstones (97 existing courses) into
  `courses/<course-id>/` with redirects.
- The two path manifests (`job-seeking-software-engineer` interview-first,
  `software-engineer` shipping-first) as ordered course-ID lists over the library.
- Fourteen NEW courses + three NEW capstones authored into the library (learning + drilling each).
- Three-level tests (unit/integration/e2e) + a `specs/` Gherkin companion for the nav feature.
- Per-path progression-smoothness audits.

**Out-of-scope features**:

- Rewriting any existing course's subject content.
- Indonesian mirror of the section content.
- Path progress persistence, accounts, or bookmarking.
- Interactive flashcards.

## Product-Level Risks

- **Order/manifest drift**: a manifest references a missing/renamed course ID → broken nav. Mitigated
  by a manifest-integrity check (gate + unit test) and stable course-ID slugs.
- **Deep-link fallback gap**: a course without path context renders poorly. Mitigated by a
  first-class canonical view + Gherkin scenario + e2e test.
- **URL breakage on re-home**: mitigated by a redirect per re-homed course + redirect specs.
- **Duplication creep**: a path forks a body for framing. Mitigated by callout-only framing + a
  no-forked-body check.
- **NEW-course quality**: interview modules must meet ayokoding pace/accuracy bars. Mitigated by the
  maker → checker → facts-checker → link-checker pipeline per course.
