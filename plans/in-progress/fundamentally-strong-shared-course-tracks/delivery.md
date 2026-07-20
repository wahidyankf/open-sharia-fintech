# Delivery Checklist — Fundamentally Strong Shared Course Library, Three Paths

This checklist delivers a **shared course library + three composing paths** over the existing ayokoding
`/c/[...slug]` content route. A **course** is a standalone, path-neutral building block served at
`/en/c/learn/courses/<course-id>`; a **path** is an ordered manifest composing a curated subset of
course-ids, landing at `/en/c/learn/paths/<path-id>`. The three paths all converge on the same deep
mastery — only the entry point, ordering, and teaching emphasis differ:

1. `interview-ready/software-engineer` — experienced SWE re-entering the market: interview/job prep FIRST → production-effective → deeper.
2. `immediately-effective/software-engineer` — editor → one language → build a real app FIRST → then deepen.
3. `fundamentally-strong/software-engineer` — university-style: fundamentals/CS-theory FIRST → deeper.

Navigation is **additive** — after re-homing, a reader can still browse the material **the old way**
(the legacy hand-curated, spiral-ordered `_index.md` section tree, re-pointed to the new course URLs)
IN ADDITION to the new way (`/en/c/learn/paths/<path-id>` path landings + `/en/c/learn/courses/<course-id>`
canonical course pages); both coexist (§5a, enforced in Phase 5).

Every course declares `prerequisites: [course-id, ...]` in its canonical metadata, forming a
**prerequisite DAG**; every path manifest is a valid prerequisite-consistent ordering/entry into that
DAG. The catalog of 121 courses (0 merges), the course-ID + manifest schema, the path-aware-navigation
UI design, and the three path orderings live in [tech-docs.md](./tech-docs.md) and the
[syllabus detail layer](./syllabus/README.md); the UI-design-funnel and NEW-course specs live in
[prd.md](./prd.md). The authoritative catalog baseline is the tracked
[Course Library Catalog](./tech-docs.md#course-library-catalog) (121 rows); it was originally derived
from a gitignored `local-temp/` scratch file, which must not be relied on during execution.

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
> Git-mechanical steps (worktree create/remove, branch, push, merge) are `[AI]`.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (safe-to-stop state + resume command). Each gate covers the phase's
> **content/code correctness** (tests, checkers, build) and its **integration** (draft PR opened,
> 3-cycle PR-Review, CI green, `[AI]` merge, `ayokoding-www` deployed). A phase is not complete until
> every gate check is green.

## Worktree

One **shared worktree** for the whole plan (one checkout, many branches, many PRs):

Worktree path: `worktrees/fundamentally-strong-shared-course-tracks/`

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree fundamentally-strong-shared-course-tracks
```

The plan-execution Step 0 gate enters this shared worktree by default: it auto-provisions from the
latest `origin/main` when missing, syncs with `origin/main` before implementing, and prompts before
deleting the worktree after the plan is archived and pushed.

Every phase branches from the **latest `origin/main`** inside this one shared worktree
(`git fetch origin && git checkout main && git pull && git checkout -b
fundamentally-strong-shared-course-tracks/<phase-slug>`), authors its work there, commits, pushes that
branch, and opens **its own draft PR**.

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans.md#worktree-specification).

## Delivery Mode: worktree-to-pr

Each phase works in the shared worktree on its **own branch**, opens a **draft PR** against `main`,
runs the **PR-Review Maker→Fixer Cycle** (`pr-review-maker` / `pr-review-fixer`, 3 sequential
CI-gated cycles), flips the PR to ready, and `[AI]` **merges it automatically once all quality gates
are green** — then `[AI]` **deploys `ayokoding-www` to `prod-ayokoding-www` after every merge** (this
plan ships to ayokoding.com). See
[Plans Organization Convention §Delivery Mode](../../../repo-governance/conventions/structure/plans.md#delivery-mode)
and the [PR Review Quality Gate workflow](../../../repo-governance/workflows/pr/pr-review-quality-gate.md).

> **DN-11 DECIDED — `[AI]` auto-merge (now the repo default)**: the repo's
> [PR Merge Protocol](../../../repo-governance/development/workflow/pr-merge-protocol.md) has `[AI]`
> merge the PR **by default** once its five hardened preconditions hold; a `[HUMAN]` merge gate is an
> explicit per-plan opt-in, and this plan does not opt in. When DN-11 was first recorded the protocol
> still defaulted to a `[HUMAN]` merge, so the maintainer authorized `[AI]` merge for this plan
> specifically (2026-07-18, in-session — modeled on the sibling plan
> `fundamentally-strong-software-engineer`'s own separately-recorded authorization) via two directives:
> (a) this plan uses the SAME delivery methods as the sibling plan, and (b) no maintainer permission is
> needed to merge a PR once it has passed 3 review cycles and the PR quality gate. The protocol has
> since been changed to match, so **DN-11 = AI-auto-merge** now simply confirms the repo default rather
> than deviating from it. The preconditions are unchanged either way — only the actor differs.

**Per-Phase Integration Protocol** (each phase's gate lists these as must-pass):

1. [AI] Sync the shared worktree to latest `origin/main` and branch:
   `git fetch origin && git checkout main && git pull && git checkout -b
fundamentally-strong-shared-course-tracks/<phase-slug>`.
2. [AI] Stage only this phase's paths (`git add <explicit paths>` — never `git add -A`), commit
   thematically (Conventional Commits, imperative, no period), push the branch, open a **draft PR**
   against `main` (`gh pr create --draft --base main ...`) — CI runs on the PR.
3. [AI] Run the **PR-Review Maker→Fixer Cycle** (3 sequential CI-gated cycles), resolve every finding,
   then `gh pr ready`.
4. [AI] **Merge** once all quality gates are green (typecheck, lint, `test:quick`, `test:unit`,
   `test:integration`, `test:e2e` where affected, `specs:behavior:coverage`, CI, the 3-cycle review) —
   `[AI]` auto-merge per DN-11.
5. [AI] Dispatch `apps-ayokoding-www-deployer` to deploy `ayokoding-www` to `prod-ayokoding-www` — a
   no-op redeploy for plan-side-only phases.

## Parallelization Model

**Cap**: honor the in-force subagent/PR-review concurrency cap (parallel-by-default, background
subagents capped per the orchestration convention). The main thread self-promotes nothing.

- **Group A (Phases 1–4)** is **serial** — each phase builds on the prior feature slice (schema →
  core → shell/route → landing/e2e). Group A is the **hard prerequisite** for every path.
- **interview-ready MVP (Phases 5–7)** is mostly serial (re-home is a sync point; the manifest depends
  on the courses existing) EXCEPT Phase 6's **five NEW interview bodies**, which are content-independent
  (each writes only its own `courses/<id>/` subtree) and **pipeline concurrently** through review,
  bounded by the cap.
- **immediately-effective manifest (Phase 8)** and **fundamentally-strong manifest (Phase 9)** are
  serial manifest+landing sync points authored over the currently-available library.
- **Backfill (Phase 10)** authors the 61 transferred topics + 10 remaining new courses + 8 remaining
  capstones (2 original + 6 DD-20 inter-topic capstones) **natively**; these bodies are mutually
  content-independent and **pipeline concurrently**
  through review (bounded by the cap). Each landed band **grows** the three manifests (append + re-run
  prerequisite-consistency + integrity) as a serial sync point.
- **Finalization (Phases 11–15)** is serial.

**Path constants** (referenced throughout):

- `<COURSES>` = `apps/ayokoding-www/content/en/learn/courses/` (course bundles; served at `/en/c/learn/courses/<course-id>`)
- `<PATHS>` = `apps/ayokoding-www/content/en/learn/paths/` (thin path-landing anchors; served at `/en/c/learn/paths/<path-id>`)
- `<SE_OLD>` = `apps/ayokoding-www/content/en/learn/fundamentally-strong/software-engineer/` (legacy home of the 33 shipped topics + 4 existing capstones, incl. `capstone-solid-core` — the re-home source)
- `<FEAT>` = `apps/ayokoding-www/src/features/course-paths/`
- `<MANIFESTS>` = `<FEAT>manifests/` (standalone YAML data files, nested to mirror slash path ids — `<MANIFESTS><path-id>.yaml`)
- `<SPECS>` = `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/course-paths/`
- Path ids: `interview-ready/software-engineer`, `immediately-effective/software-engineer`, `fundamentally-strong/software-engineer`

---

## Phase 0: Environment Setup & Baseline

> _Executor: repo-setup-manager_
>
> **No cross-plan precondition.** The sibling FS-SE plan is CLOSED
> (`plans/done/2026-07-19__fundamentally-strong-software-engineer/`) and its Passes 3–5 scope is
> absorbed here; there is **no "FS-SE must be DONE first" gate**. Topics 34–94 are authored NATIVE in
> Phase 10 (no legacy home, no re-home). Only the 33 shipped topics (1–33) + 4 existing capstones
> (incl. `capstone-solid-core`, per **DD-20**) live under `<SE_OLD>` and are re-homed in Phase 5.

- [ ] [AI] Enter/provision the worktree and install dependencies in the root worktree: `npm install`
      — acceptance: exits 0, `node_modules/` synchronized.
- [ ] [AI] Converge the toolchain in the root worktree: `npm run doctor -- --fix`
      — acceptance: exits 0 with no unresolved drift.
- [ ] [AI] Establish baselines: `npx nx run ayokoding-www:build` and
      `npx nx run ayokoding-www:test:unit`
      — acceptance: all exit 0; record pass state.
- [ ] [AI] **Re-home source inventory (non-blocking snapshot)** — record the 33 shipped topics + 4
      existing capstones present under `<SE_OLD>` to `evidence/phase-0-snapshot.txt` via:
      `for s in just-enough-nvim just-enough-lua extending-neovim just-enough-python just-enough-bash version-control-and-git data-structures-and-algorithms-essentials advanced-algorithms object-oriented-programming-essentials object-oriented-design-and-patterns sql-essentials technical-communication just-enough-typescript frontend-essentials backend-essentials networking-essentials computer-science-foundations computer-architecture programming-paradigms functional-programming concurrency-and-parallelism advanced-networking advanced-sql-and-query-performance data-access-orms-and-query-builders build-your-own-orm-and-query-builder software-engineering-practices agentic-coding security-essentials software-testing debugging-and-profiling software-product-engineering engineering-management project-management capstone-forge-ready capstone-first-working-software capstone-full-stack-app capstone-solid-core; do test -d "<SE_OLD>$s" || echo "ABSENT $s"; done`
      — acceptance: snapshot committed. Any `ABSENT` line is recorded (not a hard stop) and reconciled
      against the catalog before Phase 5.
- [ ] [AI] Also snapshot the existing `content-url.ts` / `prev-next.tsx` / `breadcrumb.tsx` /
      `tree-builder.ts` behavior and the current `next.config.ts` locale set into
      `evidence/phase-0-snapshot.txt` — acceptance: snapshot committed.
- [ ] [AI] Confirm the twenty-three NEW slugs are absent (no collision) under `<SE_OLD>` and `<COURSES>`
      (fourteen new courses + nine new capstones: three original plus six **DD-20** inter-topic
      capstones):
      `for s in coding-interview take-home-and-live-coding system-design-interview behavioral-and-leadership-interviews capstone-interview-loop async-python-and-fastapi-services self-hosting-essentials browser-automation-with-cdp the-agent-loop agent-tools-and-mcp agent-context-and-memory agent-permissions-and-sandboxing agent-orchestration-subagents-and-observability capstone-build-your-own-coding-agent just-enough-cpp detection-engineering-and-siem-operations capstone-build-your-own-pentest-engine capstone-real-world-delivery capstone-secure-service capstone-data-pipeline capstone-concurrency-and-systems capstone-concurrency-showdown capstone-lead-at-altitude; do test -e "<SE_OLD>$s" && echo "EXISTS SE_OLD $s"; test -e "<COURSES>$s" && echo "EXISTS COURSES $s"; done`
      — acceptance: zero `EXISTS` lines.
- [ ] [AI] Confirm `learnings.md` scaffold exists in the plan folder — acceptance: file present with its H1.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [ ] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift.
- [ ] [AI] `ayokoding-www:build` + `test:unit` + `test:integration` baselines recorded green.
- [ ] [AI] Re-home source inventory + component snapshot committed to `evidence/phase-0-snapshot.txt`; all 23 new slugs absent.
- [ ] [AI] Draft PR opened; CI triggered; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged;
      `ayokoding-www` deployed (no-op redeploy).

> **Pause Safety**: only the toolchain was verified and the current state snapshotted — no content or
> code changed. Safe to stop indefinitely. To resume: re-run the baselines.

---

## Group A — Architecture + path-aware navigation UI (hard prerequisite)

## Phase 1: UI design funnel + library/paths content homes + manifest & prerequisite schema

> _Suggested executor: `web-researcher` (R7 prior art) + `swe-developing-frontend-ui` skill for the
> funnel; `swe-typescript-dev` for the schema._

- [ ] [AI] **R5 survey** — read `libs/web-ui` component inventory + tokens + Storybook and the
      ayokoding app-shell + existing `sidebar-tree`/`breadcrumb`/`prev-next`/`section-card`
      [Repo-grounded] — acceptance: net-new components (`PathCard`, `PathLanding`, `PathBanner`,
      `PathCourseLinks`, `PrerequisiteList`) named in `tech-docs.md`; existing primitives to reuse listed.
  - _Suggested executor: `swe-developing-frontend-ui` skill_
- [ ] [AI] **R7 prior art** — delegate to `web-researcher` a survey of how comparable platforms present
      a track/path over shared lessons **with prerequisites** (roadmap.sh, Exercism, freeCodeCamp,
      Coursera) — acceptance: cited findings folded into `prd.md` funnel notes; no `[Unverified]` claim.
- [ ] [AI] **Produce hi-fi finalists** — author the 2 `.excalidraw.png` finalists per screen (paths
      hub with **three** path cards, path landing, course-in-path with **prerequisite display**) into
      `assets/` per [prd.md §UI-Design-Funnel](./prd.md#ui-design-funnel-path-aware-navigation-screens)
      and confirm the embedded `![]()` links resolve — acceptance: **all six files exist on disk** —
      `for f in paths-hub-option-a paths-hub-option-b path-landing-option-a path-landing-option-b course-path-option-a course-path-option-b; do test -f "assets/$f.excalidraw.png" || echo "MISSING $f"; done`
      prints nothing (today it prints all six: `assets/` does not exist yet — verified); AND each of
      the three screens' selection line is updated to name the finalist file it selects —
      `grep -c "Selected: .*excalidraw" prd.md` returns ≥3 (returns **0** today, verified).
      **The bare `grep -c "Selected:" prd.md` ≥ 3 MUST NOT be used**: it already returns **4** in the
      unexecuted plan (three authored design-intent selections plus one meta-reference at line 115),
      so it is pre-satisfied and contributes zero discriminating power to the conjunction.
      **Do not weaken this back to a `grep` over `prd.md`**: the prose already names the six files
      (`grep -c "excalidraw.png" prd.md` returns **8** and `grep -c "Selected:" prd.md` returns **4**
      in the current unexecuted state), so a prose-only check is pre-satisfied and can never go
      false→true as a result of this step's actual work. The artifacts are the deliverable, so the
      artifacts are what the acceptance must test.
- [ ] [AI] **Library + paths content homes** — create `<COURSES>_index.md` (library landing, weight +
      title) and `<PATHS>_index.md` (paths hub / choose-a-path landing listing **all three** paths)
      mirroring an existing section `_index.md` — acceptance: `test -f <COURSES>_index.md` and
      `test -f <PATHS>_index.md`; build green.
- [ ] [AI] **Course-prerequisite metadata contract** — document the canonical course metadata field
      `prerequisites: [course-id, ...]` (declared in each course `_index.md` frontmatter) in
      [tech-docs §Prerequisite DAG](./tech-docs.md#prerequisite-dag-illustrative-excerpt) — acceptance: contract documented;
      the field is the single source of truth for the prerequisite DAG surfaced on each course page.
- [ ] [AI] **Manifest data-file schema definition** — write the `PathManifest` zod schema (`pathId`,
      `title`, `description`, `courseOrder[]`, optional per-course `framing`) into `<FEAT>core/schemas.ts`,
      matching the standalone YAML data-file format (NOT `_index.md` frontmatter), per
      [tech-docs §Path = ordered manifest](./tech-docs.md#path--ordered-manifest-manifest-format)
      — acceptance: schema compiles (`npx nx run ayokoding-www:typecheck` exits 0).
- [ ] [AI] **Manifest data-file directory** — create `<MANIFESTS>` (the standalone-data-file home,
      source of truth) with a `README.md` note that nested `<path-id>.yaml` files land here in Phases
      7–10 — acceptance: `test -d <MANIFESTS>` and `test -f <MANIFESTS>README.md`.

### Phase 1 Gate

- [ ] [AI] Funnel finalists (three-path hub + prerequisite display) + selections + rationale present in `prd.md`; assets resolve.
- [ ] [AI] `<COURSES>_index.md` + `<PATHS>_index.md` created; prerequisite metadata contract documented; `PathManifest` schema compiles; `<MANIFESTS>` exists.
- [ ] [AI] `npx nx run ayokoding-www:build` + `:typecheck` exit 0.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the design is fixed and the empty library/paths homes + manifest/prerequisite
> schema exist; no bodies moved, no nav behavior changed. Safe to stop. To resume: re-run `:typecheck`.

---

## Phase 2: `course-paths` core (pure) — TDD + specs RED

> _Suggested executor: `swe-typescript-dev` (core logic) + `specs-maker` (Gherkin)._

- [ ] [AI] **Specs RED** — author the `course-paths` Gherkin companion under `<SPECS>` (one `.feature`
      per behavior: path-order nav, breadcrumb, canonical fallback, invalid-path fallback, omitted
      course, manifest integrity, prerequisite display, prerequisite-consistent ordering) from
      [prd.md §Acceptance Criteria](./prd.md#acceptance-criteria-gherkin) + a `<SPECS>README.md`
      — acceptance: `npx nx run ayokoding-www:specs:behavior:coverage` fails (no step bindings yet).
  - _Suggested executor: `specs-maker`_
- [ ] [AI] **RED** — write failing unit tests in `<FEAT>core/path-nav.test.ts` for
      `resolvePathNav(manifest, courseId)` (prev/next at both boundaries; course-missing → nulls) and
      `parsePathContext(searchParams, manifests)` (valid → pathId; unknown → null; absent → null)
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: tests fail (functions undefined).

  **Gherkin (underpins) →** "Prev and next follow the active path's order"; "A course omitted from a
  path shows no path nav for that path"; "A course deep-linked without path context renders the
  canonical view"; "An invalid path context falls back to the canonical view"

  ```gherkin
  Scenario: Prev and next follow the active path's order
    Given a reader is on a course with an active path context
    When the reader reads the prev/next navigation
    Then prev and next are the neighboring courses in that path's manifest
    And both links preserve the path context query parameter

  Scenario: A course omitted from a path shows no path nav for that path
    Given a course is not listed in a given path's manifest
    When a reader opens that course with that path's context
    Then the course renders the canonical standalone view
    And the path banner is not shown for that path

  Scenario: A course deep-linked without path context renders the canonical view
    Given a reader opens a course URL /en/c/learn/courses/<course-id> with no path context query parameter
    When the course page renders
    Then the course body renders in full with the content-tree breadcrumb and its prerequisite list
    And a "this course is part of" affordance lists every path that includes the course

  Scenario: An invalid path context falls back to the canonical view
    Given a reader opens a course URL with a path context that names no known path
    When the course page renders
    Then the course renders the canonical standalone view
    And no error is shown
  ```

- [ ] [AI] **GREEN** — implement `<FEAT>core/manifest.ts` (course-ref normalization `id | {id, framing}`),
      `<FEAT>core/path-nav.ts` (`resolvePathNav`), `<FEAT>core/path-context.ts` (`parsePathContext`)
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: the new tests pass; no others break.
- [ ] [AI] **RED** — write a failing unit test in
      `apps/ayokoding-www/src/features/content/core/content-url.test.ts` for
      `contentUrl(locale, slug, pathId)` appending `?path=<pathId>` and producing the
      `/en/c/learn/courses/<course-id>` shape — command: `npx nx run ayokoding-www:test:unit` —
      acceptance: fails (param + new URL shape not yet supported).

  **Gherkin (underpins) →** "A path landing page lists its courses in manifest order"; "The breadcrumb
  reflects the active path"; "A legacy fundamentally-strong URL redirects to the canonical course URL"

  ```gherkin
  Scenario: A path landing page lists its courses in manifest order
    Given the interview-ready/software-engineer path manifest is published
    When a reader opens the path landing page at /en/c/learn/paths/interview-ready/software-engineer
    Then the courses appear in the manifest's courseOrder
    And every course link carries the path context query parameter

  Scenario: The breadcrumb reflects the active path
    Given a reader is on a course with an active path context
    When the breadcrumb renders
    Then it shows Home, Learn, the path title, and the course title
    And the path crumb links to the path landing page /en/c/learn/paths/<path-id> with the path context preserved

  Scenario: A legacy fundamentally-strong URL redirects to the canonical course URL
    Given a re-homed course previously lived under the legacy fundamentally-strong/software-engineer content path
    When a reader requests the legacy URL
    Then the app redirects to the course's canonical /en/c/learn/courses/<course-id> URL
    And the redirect preserves any path context query parameter
  ```

- [ ] [AI] **GREEN** — extend `content-url.ts` with the optional `pathId` param appending `?path=` and
      the `/en/c/learn/courses/<course-id>` canonical shape
      [Repo-grounded — `apps/ayokoding-www/src/features/content/core/content-url.ts`] — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: the new test passes; existing `content-url`
      tests still pass (or are updated for the new canonical shape in the same commit).
- [ ] [AI] **RED** — write failing unit tests in `<FEAT>core/prerequisites.test.ts` for
      `resolvePrerequisites(courseId, prerequisitesByCourse)` (returns declared prereq IDs; missing →
      empty) and `checkPrerequisiteConsistency(manifest, prerequisitesByCourse, libraryCourseIds)`
      (reports any course whose declared, in-library prerequisite is absent-from or later-than the
      course in `courseOrder`) — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails
      (functions undefined).

  **Gherkin (underpins) →** "A course page surfaces its declared prerequisites"; "A path manifest is a
  valid topological entry into the prerequisite DAG"

  ```gherkin
  Scenario: A course page surfaces its declared prerequisites
    Given a course declares prerequisites in its canonical metadata
    When a reader opens the course page with or without a path context
    Then the page lists each prerequisite course with a link to its canonical URL
    And the prerequisite list renders even in the canonical no-path view

  Scenario: A path manifest is a valid topological entry into the prerequisite DAG
    Given a path manifest lists a courseOrder of course IDs
    When the manifest-integrity check runs
    Then no course appears before any of its declared prerequisites that are also in the manifest
    And every listed course ID resolves to an existing course in the library
  ```

- [ ] [AI] **GREEN** — implement `resolvePrerequisites` + `checkPrerequisiteConsistency` in
      `<FEAT>core/prerequisites.ts` (pure; no IO) — command: `npx nx run ayokoding-www:test:unit` —
      acceptance: the new tests pass.
- [ ] [AI] **RED** — write a failing unit test in `<FEAT>core/manifest-integrity.test.ts` for
      `checkManifestIntegrity(manifest, libraryCourseIds)` asserting it reports every `courseOrder`
      entry whose ID is absent from `libraryCourseIds` and every ID that appears more than once
      — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails (`checkManifestIntegrity` undefined).

  **Gherkin (underpins) →** "Every manifest course reference resolves to a real course"

  ```gherkin
  Scenario: Every manifest course reference resolves to a real course
    Given a path manifest lists a courseOrder of course IDs
    When the manifest-integrity check runs
    Then every listed course ID resolves to an existing course in the library
    And no course ID appears more than once in the manifest
  ```

- [ ] [AI] **GREEN** — implement `checkManifestIntegrity(manifest, libraryCourseIds)` in
      `<FEAT>core/manifest-integrity.ts` (pure; returns unresolved + duplicate ID sets) — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: the new test passes.
- [ ] [AI] **REFACTOR** — extract shared course-ref types; ensure `core/` stays IO-free (pure) —
      command: `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:typecheck` — acceptance:
      all green; no `fs`/React import in `core/`.

### Phase 2 Gate

- [ ] [AI] `resolvePathNav` + `parsePathContext` + `contentUrl(pathId)` + `resolvePrerequisites` + `checkPrerequisiteConsistency` + `checkManifestIntegrity` implemented; unit tests green.
- [ ] [AI] `course-paths` Gherkin authored under `<SPECS>`; `specs:behavior:coverage` maps the new features (step bindings land in Phase 3 — record the coverage delta).
- [ ] [AI] `npx nx run ayokoding-www:test:unit` + `:typecheck` + `:lint` exit 0.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the pure ordering + context + prerequisite logic is implemented and unit-tested; no
> route or component consumes it yet, so nav behavior is unchanged. Safe to stop. To resume: `:test:unit`.

---

## Phase 3: `course-paths` shell + route wiring + prerequisite display + redirects — integration TDD

> _Suggested executor: `swe-typescript-dev`._

- [ ] [AI] **RED** — write failing integration tests for `<FEAT>shell/manifest-repository.ts` (loads and
      validates each `<MANIFESTS>**/*.yaml` data file into a `PathManifest[]` via the `schemas.ts` zod
      schema, keyed by the nested path id) — command: `npx nx run ayokoding-www:test:unit` —
      acceptance: tests fail (repository wiring absent).

  **Gherkin (binds) →** "All three paths reference a shared course with no body duplication"

  ```gherkin
  Scenario: All three paths reference a shared course with no body duplication
    Given a course appears in all three path manifests
    When the course library is inspected
    Then exactly one canonical path-neutral body exists for that course
    And each manifest references the course by its stable course ID
  ```

- [ ] [AI] **RED** — write a failing integration test for the content service resolving
      `(courseId, activePath)` → path-aware prev/next — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: test fails (service wiring absent).

  **Gherkin (binds) →** "Prev and next follow the active path's order"

  ```gherkin
  Scenario: Prev and next follow the active path's order
    Given a reader is on a course with an active path context
    When the reader reads the prev/next navigation
    Then prev and next are the neighboring courses in that path's manifest
    And both links preserve the path context query parameter
  ```

- [ ] [AI] **Declare direct dependency** — `js-yaml` is currently only a nested transitive dependency
      (via `gray-matter`) and is not exact-pinned in `apps/ayokoding-www/package.json`; add it as a
      direct `dependencies` entry, exact-pinned per the
      [Dependency Bump Stability & Safety Policy](../../../repo-governance/development/workflow/dependency-bump-policy.md)
      (Path A: current LTS-compatible latest patch, CVE-clean) — acceptance: `js-yaml` appears in
      `apps/ayokoding-www/package.json` `dependencies` with an exact version; `npm install` resolves
      with no peer-dependency warning for it.
- [ ] [AI] **GREEN** — implement `<FEAT>shell/manifest-repository.ts` to read + parse each
      `<MANIFESTS>**/*.yaml` data file via the now-direct `js-yaml` dependency (manifest data files are
      always `.yaml`; no JSON fallback); extend the content index to carry loaded manifests +
      per-course `prerequisites` alongside `trees`/`prevNext`
      [Repo-grounded — `ContentIndex` in `apps/ayokoding-www/src/features/content/core/types.ts` and
      the service in `.../content/shell/service.ts`] — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: the new integration tests pass. Wire
      `checkManifestIntegrity` + `checkPrerequisiteConsistency` into the repository so a load with any
      unresolved/duplicate ID or prerequisite-order violation throws at build time.
- [ ] [AI] **GREEN** — wire the course route: in
      `apps/ayokoding-www/src/app/[locale]/(content)/c/[...slug]/page.tsx` [Repo-grounded] read
      `searchParams.path`, call `parsePathContext`, and render path-aware prev/next + breadcrumb when a
      valid path context resolves and the course is in that manifest; else render the canonical view.
      Extend `navigation/shell/prev-next.tsx` and `navigation/shell/breadcrumb.tsx` to accept an
      optional path context (links carry `?path=`) — command: `npx nx run ayokoding-www:build` —
      acceptance: build green; canonical (no-path) rendering unchanged for non-path routes.
- [ ] [AI] **GREEN** — author `<FEAT>shell/prerequisite-list.tsx` (**prerequisite display** — reads the
      course's `prerequisites` metadata, links each to its canonical `/en/c/learn/courses/<id>` URL),
      `<FEAT>shell/path-banner.tsx` (in-path affordance), and `<FEAT>shell/path-course-links.tsx`
      ("this course is part of: …") consumed by the course page — command:
      `npx nx run ayokoding-www:test:unit` (component tests) — acceptance: tests pass; prerequisite
      display renders declared prerequisites.
- [ ] [AI] **GREEN** — add redirects for re-homed courses: for every existing (topics 1–33 + 4
      capstones, incl. `capstone-solid-core`) course, a redirect from
      `.../fundamentally-strong/software-engineer/<slug>` to
      `/en/c/learn/courses/<course-id>` in `apps/ayokoding-www/src/redirects/` [Repo-grounded —
      precedent `.../gherkin/navigation/learn-reorg-redirects.feature`] — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: redirect resolution test passes.
- [ ] [AI] **GREEN (specs)** — implement the step bindings so the `<SPECS>` Gherkin scenarios execute —
      command: `npx nx run ayokoding-www:specs:behavior:coverage` — acceptance: exits 0.
- [ ] [AI] **REFACTOR** — deduplicate breadcrumb/prev-next path-vs-canonical branches; keep `shell/`
      the only IO — command:
      `npx nx run ayokoding-www:test:unit && :typecheck && :lint` — acceptance: all green. (`:test:integration` is a no-op echo for this content app — the integration tier is deliberately unused; unit consumes the Gherkin mocked.)

### Phase 3 Gate

- [ ] [AI] Manifest loading + path-aware route wiring + prerequisite display + redirects implemented; integration tests green.
- [ ] [AI] `specs:behavior:coverage` green; canonical (no-path) nav unchanged (retained nav specs pass).
- [ ] [AI] `npx nx run ayokoding-www:test:unit` + `:build` + `:typecheck` + `:lint` exit 0. (`:test:integration` is a no-op echo — omitted deliberately, not overlooked.)
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the feature resolves a manifest + path context + prerequisites end-to-end (no
> manifests published yet, so the canonical view is what renders); redirects are in place. Safe to
> stop. To resume: `npx nx run ayokoding-www:test:unit`.

---

## Phase 4: Path landing + paths hub (three cards) + e2e

> _Suggested executor: `swe-typescript-dev` + `swe-e2e-dev`._

- [ ] [AI] **GREEN** — author `<FEAT>shell/path-landing.tsx` (renders a manifest's ordered course list,
      links carry `?path=`) and `<FEAT>shell/path-card.tsx` (paths-hub card), rendered by
      `<PATHS>_index.md` / `<PATHS><path-id>/_index.md`, per
      [prd.md Screen 1/2 selected designs](./prd.md#ui-design-funnel-path-aware-navigation-screens) —
      command: `npx nx run ayokoding-www:build` — acceptance: build green; components render; the hub
      supports **three** path cards.
- [ ] [AI] **RED (e2e)** — write failing Playwright e2e specs in the ayokoding e2e suite for: path
      landing lists courses in manifest order; prev/next walks the path and preserves `?path=`;
      breadcrumb shows the path; a course page shows its prerequisites; deep-link without `?path=` →
      canonical view; invalid `?path=` → canonical view; old
      `fundamentally-strong/software-engineer/<slug>` URL → redirect to `/en/c/learn/courses/<id>` —
      command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: e2e specs fail (no published manifest yet).
  - _Suggested executor: `swe-e2e-dev`_

  **Gherkin (binds) →** "A path landing page lists its courses in manifest order"; "Prev and next
  follow the active path's order"; "The breadcrumb reflects the active path"; "A course page surfaces
  its declared prerequisites"; "A course deep-linked without path context renders the canonical view";
  "An invalid path context falls back to the canonical view"; "A legacy fundamentally-strong URL
  redirects to the canonical course URL"

  ```gherkin
  Scenario: A path landing page lists its courses in manifest order
    Given the interview-ready/software-engineer path manifest is published
    When a reader opens the path landing page at /en/c/learn/paths/interview-ready/software-engineer
    Then the courses appear in the manifest's courseOrder
    And every course link carries the path context query parameter

  Scenario: Prev and next follow the active path's order
    Given a reader is on a course with an active path context
    When the reader reads the prev/next navigation
    Then prev and next are the neighboring courses in that path's manifest
    And both links preserve the path context query parameter

  Scenario: The breadcrumb reflects the active path
    Given a reader is on a course with an active path context
    When the breadcrumb renders
    Then it shows Home, Learn, the path title, and the course title
    And the path crumb links to the path landing page /en/c/learn/paths/<path-id> with the path context preserved

  Scenario: A course page surfaces its declared prerequisites
    Given a course declares prerequisites in its canonical metadata
    When a reader opens the course page with or without a path context
    Then the page lists each prerequisite course with a link to its canonical URL
    And the prerequisite list renders even in the canonical no-path view

  Scenario: A course deep-linked without path context renders the canonical view
    Given a reader opens a course URL /en/c/learn/courses/<course-id> with no path context query parameter
    When the course page renders
    Then the course body renders in full with the content-tree breadcrumb and its prerequisite list
    And a "this course is part of" affordance lists every path that includes the course

  Scenario: An invalid path context falls back to the canonical view
    Given a reader opens a course URL with a path context that names no known path
    When the course page renders
    Then the course renders the canonical standalone view
    And no error is shown

  Scenario: A legacy fundamentally-strong URL redirects to the canonical course URL
    Given a re-homed course previously lived under the legacy fundamentally-strong/software-engineer content path
    When a reader requests the legacy URL
    Then the app redirects to the course's canonical /en/c/learn/courses/<course-id> URL
    And the redirect preserves any path context query parameter
  ```

**Gherkin (binds) →** "The navigation feature meets accessibility requirements"

```gherkin
Scenario: The navigation feature meets accessibility requirements
  Given a reader uses a keyboard and a screen reader on a course in path context
  When they navigate the path banner, breadcrumb, prerequisite list, and prev/next
  Then each is a labelled landmark reachable and operable by keyboard with visible focus
  And the document language attribute matches the active locale
```

- [ ] [AI] **RED (a11y)** — this suite is **playwright-bdd**, so the scenario above is authored as
      Gherkin under `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/` and bound by a step
      definition at `apps/ayokoding-www-fe-e2e/src/steps/course-paths-a11y.steps.ts` (follow the
      existing `accessibility.steps.ts` pattern). The steps assert, on a course rendered in path
      context: the path banner, path breadcrumb, prerequisite list, and prev/next controls are each a
      labelled landmark reachable and operable by keyboard with a visible focus ring; the current item
      carries `aria-current`; and `<html lang>` equals the active locale (`en`) — command:
      `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: the `course-paths-a11y` scenario fails (the path-aware navigation landmarks do not
      exist yet). This RED step exists because the a11y scenario was previously bound only by the
      REFACTOR step below, which gave it no prior failing state.
      **Do NOT target `ayokoding-www:test:e2e`**: that target is `echo 'no-op: target not applicable
for this project'` and always exits 0, so any RED clause pointed at it can never fail. E2E for
      this app lives entirely in the paired `ayokoding-www-fe-e2e` project (`npx bddgen && npx
playwright test`).
- [ ] [AI] **GREEN (a11y)** — add the landmark roles, accessible labels, `aria-current`, focus
      styling, and locale-correct `lang` attribute so the scenario passes — command:
      `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: the `course-paths-a11y` scenario passes.
- [ ] [AI] **GREEN (e2e fixtures)** — add a minimal fixture manifest (a few real course IDs with
      declared prerequisites) so the e2e specs exercise the real components — command:
      `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: all `course-paths` e2e specs pass in `en`
      (this plan's content locale; see [brd.md §Business-Scope Non-Goals](./brd.md#business-scope-non-goals)).
- [ ] [AI] **REFACTOR** — ensure the landing + hub reuse `libs/web-ui` primitives (no bespoke CSS where
      a token exists); a11y pass (labels, focus, `aria-current`) — command:
      `npx nx run ayokoding-www-fe-e2e:test:e2e && :lint` — acceptance: green; a11y assertions pass.

### Phase 4 Gate

- [ ] [AI] Path landing + three-card paths hub render from a manifest; prerequisite display verified; all `course-paths` e2e specs green in `en` (this plan's content locale).
- [ ] [AI] `npx nx run ayokoding-www:test:unit` + `:build` + `:lint` + `:specs:behavior:coverage` **and** `npx nx run ayokoding-www-fe-e2e:test:e2e` exit 0. (`ayokoding-www:test:e2e` and `:test:integration` are both no-op echoes — e2e lives in the paired `ayokoding-www-fe-e2e` project, and the integration tier is deliberately unused for content apps.)
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the full path-aware navigation UI (incl. prerequisite display + three-card hub) is
> implemented, tested (unit + integration + e2e + specs), and live — but no real path manifests are
> published yet, so production still shows the canonical library. **Group A (the hard prerequisite) is
> complete.** Safe to stop. To resume: `npx nx run ayokoding-www-fe-e2e:test:e2e`.

---

## Group B — interview-ready MVP (ships first, end-to-end)

## Phase 5: Re-home the 33 shipped topics + 4 existing capstones into `courses/`

> _Suggested executor: `swe-typescript-dev`_ (mechanical `apps/ayokoding-www/content/` moves +
> redirect wiring — `docs-file-manager` is scoped to `docs/` only and does not cover app content).
> Only the **shipped** legacy bodies move here (33 topics 1–33 + 4 existing capstones, incl.
> `capstone-solid-core` per **DD-20**). Topics 34–94 have no legacy home and are authored NATIVE in
> Phase 10.

- [ ] [AI] For **every** shipped topic + existing capstone, `git mv <SE_OLD><slug>/ <COURSES><slug>/`
      (course-id = slug; no rename), preserving the full page-bundle (`_index.md` + `overview.md` +
      `learning/` + `drilling/`) — acceptance: `<SE_OLD>` holds no course folders from the re-home set;
      every re-homed course resolves under `<COURSES>`; `npx nx run ayokoding-www:generate-indexes`
      succeeds and `:build` exits 0.
- [ ] [AI] **Add prerequisites to each re-homed course** — add `prerequisites: [course-id, ...]` to each
      re-homed `_index.md` frontmatter naming only earlier library courses, per the
      [prerequisite DAG](./tech-docs.md#prerequisite-dag-illustrative-excerpt) — command: `npx nx run ayokoding-www:build`
      — acceptance: every re-homed course declares `prerequisites` (empty list allowed for roots); build green.
- [ ] [AI] Confirm each re-homed course has its redirect (Phase 3) old-URL → new-URL resolving —
      command: `npx nx run ayokoding-www:test:unit` — acceptance: redirect specs green for all moved courses.
- [ ] [AI] Update `<COURSES>_index.md` (library landing) to list the re-homed catalog by course ID —
      acceptance: link-checker green; every catalog link resolves.
- [ ] [AI] Sweep any intra-course cross-links that referenced the old
      `fundamentally-strong/software-engineer/<slug>` path and repoint them to
      `/en/c/learn/courses/<course-id>` (Root Cause Orientation) — command:
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md links validate` (the actual
      link-validation mechanism — not an `nx run` target; runs pre-commit via `lint-staged` for staged
      `.md` files, and repo-wide in CI's `md-links` job, which currently excludes
      `apps/ayokoding-www/content`, so the Phase 5 e2e nav check below is the binding verification for
      this content tree) — acceptance: zero broken links.

**Preserve the "old-way" `_index.md` section browse (§5a — ADDITIVE model, required).** The
library/paths model is additive: a reader must keep navigating the material **the old way** (the legacy
hand-curated, spiral-ordered `_index.md` section tree) IN ADDITION to the new way (paths + canonical
course pages). Every impacted legacy section index is UPDATED (not deleted), re-pointing each entry to
wherever the content now lives.

- [ ] [AI] **RED** — write a failing integration/e2e nav check asserting the legacy ordered browse
      resolves end-to-end: from `.../fundamentally-strong/software-engineer/_index.md` (and the
      `fundamentally-strong/_index.md` parent + each per-topic `_index.md`), every listed entry link
      resolves to live content (the re-homed `/en/c/learn/courses/<course-id>` URL or a working
      redirect) — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: the legacy-browse nav spec
      fails (links still point at drained `<SE_OLD>` locations).

  **Gherkin (binds) →** "The legacy section-index browse still resolves after re-homing"

  ```gherkin
  Scenario: The legacy section-index browse still resolves after re-homing
    Given the 33 shipped topics have been re-homed into the course library
    When a reader browses the legacy fundamentally-strong software-engineer section index the old way
    Then every section-index entry links to live content at its /en/c/learn/courses/<course-id> URL or via a redirect
    And no legacy section-index entry resolves to a drained or missing location
  ```

- [ ] [AI] **RED** — write a failing integration/e2e nav check asserting that a course reached via the
      legacy section-index browse and the same course reached via its
      `/en/c/learn/paths/<path-id>` path landing resolve to the identical canonical course body (same
      rendered content, same canonical URL) — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` —
      acceptance: the coexistence nav spec fails (no assertion yet ties the two navigation routes to
      the same canonical body).

  **Gherkin (binds) →** "Old-way and new-way navigation coexist"

  ```gherkin
  Scenario: Old-way and new-way navigation coexist
    Given a course now lives at its canonical /en/c/learn/courses/<course-id> URL
    When a reader reaches it via the legacy section-index browse
    And another reader reaches it via a /en/c/learn/paths/<path-id> path landing
    Then both navigations resolve to the same single canonical course body
  ```

  _The two RED steps above are each bound to exactly one scenario per the Gherkin-Tagged Delivery
  Steps HARD rule; the GREEN and REFACTOR steps below are shared across both because the single fix
  (re-pointing every legacy `_index.md` entry to its canonical URL) satisfies both scenarios at once —
  the REFACTOR step's acceptance criterion explicitly re-asserts the old-way/new-way body-equivalence
  scenario._

- [ ] [AI] **GREEN** — enumerate every impacted `_index.md` under
      `apps/ayokoding-www/content/en/learn/fundamentally-strong/**` (`find apps/ayokoding-www/content/en/learn/fundamentally-strong -name _index.md`
      — esp. `.../software-engineer/_index.md`, each per-topic `_index.md`, and the
      `fundamentally-strong/_index.md` parent) and update each so every entry it lists is re-pointed to
      the new `/en/c/learn/courses/<course-id>` URL (or via the redirect) — the legacy sections are
      preserved and ordered, no dead links, no orphaned section — command:
      `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: both the legacy-browse nav spec and the
      coexistence nav spec now pass.
- [ ] [AI] **REFACTOR** — run
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md links validate` +
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md heading-hierarchy validate` + `npm run lint:md` over the updated legacy `_index.md` tree (the heading-hierarchy validator
      already runs automatically pre-commit via `lint-staged` for every staged `.md` file; this step
      re-runs it explicitly over the full legacy tree) — acceptance: zero broken links; both old-way
      and new-way navigations resolve to the same canonical bodies; validators green.

### Phase 5 Gate

- [ ] [AI] All 33 shipped topics + 4 existing capstones (incl. `capstone-solid-core`) live under `<COURSES>` with declared prerequisites; `<SE_OLD>` drained of the re-home set; redirects resolve; catalog updated.
- [ ] [AI] Every impacted legacy `_index.md` under `.../fundamentally-strong/**` updated; old-way section browse resolves end-to-end (link validator + e2e nav check green); old-way and new-way navigation coexist.
- [ ] [AI] `npx nx run ayokoding-www:build` + link + heading validation green.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: every shipped course now lives at its canonical `/en/c/learn/courses/<id>` URL with
> a redirect + declared prerequisites, AND the legacy `_index.md` section browse still resolves the old
> way (additive); no manifest exists yet, so all courses render the canonical view. Safe to stop. To
> resume: re-run link validation + the legacy-browse e2e + `:build`.

---

## Phase 6: Author the four interview courses + `capstone-interview-loop` into the library

> Each NEW course is authored as a full page-bundle into `<COURSES><course-id>/`. These five bodies are
> content-independent (each writes only its own subtree) and **pipeline concurrently** through review
> (bounded by the cap). Author each per the **NEW-course authoring convention** below; per-course
> concept/example detail is in the [syllabus courses layer](./syllabus/courses/README.md) and the
> [prd.md spec](./prd.md#new-course--capstone-specifications).

**NEW-course authoring convention** (apply to each course/capstone sub-phase):

1. [AI] **V (accuracy pre-verify)** — spot-check version-pinned / market / pre-1.0-stack facts via
   `web-researcher`; the two `vacti` repos stay unverified (never written as version-pinned facts) —
   acceptance: no version-pinned claim written `[Unverified]`.
2. [AI] **Skeleton** — create `<COURSES><course-id>/` (`_index.md` with `prerequisites: [...]` +
   `overview.md` + `learning/_index.md` + `drilling/_index.md`), mirroring the matching sibling bundle
   shape — acceptance: `test -d` passes for folder + `learning/` + `drilling/`; `prerequisites` declared.
3. [AI] **Author learning track** — `overview.md` (purpose + `## Prerequisites` naming only earlier
   library courses + register per prd), concept coverage (≥ floor `co-NN`), example/scenario pages
   (volume band `ex-NN`) + colocated `code/` where code-bearing, and `learning/capstone/` — acceptance:
   `grep -oh 'co-[0-9]\{2\}' … | sort -u | wc -l` ≥ floor; `ex-NN` count in band.
4. [AI] **Author drilling track** — `drilling/<course-id>.md` + `drilling/overview.md` in the fixed
   five-section order — acceptance: all five sections present.
5. [AI] **Run content checkers** — run the matching learning checker, `apps-ayokoding-www-facts-checker`,
   and `apps-ayokoding-www-link-checker` (plus `apps-ayokoding-www-general-checker` on
   `drilling/overview.md`) — acceptance: findings recorded. _(Content authoring is a
   maker-checker-fixer cycle, not code TDD — no RED/GREEN/REFACTOR labels; see steps 6-7.)_
6. [AI] **Apply content fixers** — resolve every CRITICAL/HIGH/MEDIUM finding via the matching fixer —
   acceptance: every finding addressed.
7. [AI] **Re-verify** — re-run checkers + `npx nx run ayokoding-www:build` + `npm run lint:md` —
   acceptance: zero CRITICAL/HIGH/MEDIUM remain; build + lint exit 0.

Each course below is its own sub-phase (own branch → draft PR → 3-cycle review → `[AI]` merge →
deploy), applying the convention:

- [ ] [AI] `coding-interview` (By Example · Python) — acceptance: all 7 convention steps complete; checkers report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `take-home-and-live-coding` (By Example · Python) — acceptance: all 7 convention steps complete; checkers report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `system-design-interview` (Annotated-concept · no code; forward-links `system-design`) — acceptance: all 7 convention steps complete; checkers report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] `behavioral-and-leadership-interviews` (Annotated-concept · no code) — acceptance: all 7 convention steps complete; checkers report zero CRITICAL/HIGH/MEDIUM.
      **Gherkin (binds) →** "The behavioral course covers the layoff and employment-gap narrative"
      — coverage acceptance: the learning track explicitly covers framing an employment gap, a layoff,
      and a re-entry story, and treats senior/staff/EM leadership rounds as core (not optional)
      material — verify with
      `grep -ciE 'employment gap|layoff|re-entry' <course>/**/*.md` (ERE alternation) returning ≥3 distinct lessons.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] `capstone-interview-loop` (Python + prose) — acceptance: all 7 convention steps complete; checkers report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

### Phase 6 Gate

- [ ] [AI] All 4 interview courses + `capstone-interview-loop` live under `<COURSES>` with declared prerequisites; each passed its checker + facts + link checkers.
- [ ] [AI] `<COURSES>_index.md` catalog updated to include the five new bodies.
- [ ] [AI] `npx nx run ayokoding-www:build` + link + heading + markdownlint green.
- [ ] [AI] Every NEW-course sub-phase PR is `[AI]`-merged and deployed.

> **Pause Safety**: the library now holds the 33 shipped topics + 4 existing capstones (incl.
> `capstone-solid-core`) + the 5 interview-technique bodies, all at canonical URLs; no manifest
> published yet, so all render the canonical view. Safe to stop. To resume: re-run the section build +
> link validation.

---

## Phase 7: Author the `interview-ready/software-engineer` manifest + landing + wire + smoothness (MVP ships)

> _Suggested executor: `apps-ayokoding-www-general-maker` (manifest/landing) + `web-researcher` (smoothness facts)._
> This is the **first shippable path**. It is authored over the currently-available library (33 topics
> plus 4 capstones plus 5 interview bodies) and **grows** during Phase 10 backfill as deeper courses
> land.

- [ ] [AI] Author the manifest **data file** `<MANIFESTS>interview-ready/software-engineer.yaml`
      (standalone data file): `pathId: interview-ready/software-engineer`, `title`, `description`, and
      the ordered `courseOrder` = the interview-first arc from
      [tech-docs §Path `interview-ready/software-engineer`](./tech-docs.md#path-interview-readysoftware-engineer-interview-first)
      and [syllabus/paths/README.md](./syllabus/paths/README.md) — acceptance: the manifest loads +
      validates (`npx nx run ayokoding-www:test:unit` exits 0); references only extant courses.
- [ ] [AI] Author the thin landing anchor `<PATHS>interview-ready/software-engineer/_index.md`
      (prose/SEO only — no `courseOrder`); the ordered course list renders from the loaded manifest per
      [prd.md Screen 2](./prd.md#screen-2--path-landing-page) — acceptance: landing renders the
      manifest-ordered list (phase-grouped, fast-path callout, interview-loop map).
- [ ] [AI] **Manifest integrity + prerequisite-consistency check** — every `courseOrder` ID resolves
      under `<COURSES>`; no duplicate ID; every in-library prerequisite of each listed course appears
      earlier in the ordering — command: `npx nx run ayokoding-www:test:unit` — acceptance: exits 0.
- [ ] [AI] Verify path-aware nav end-to-end for this path: from the landing, prev/next walks the
      manifest order and preserves `?path=interview-ready/software-engineer`; breadcrumb shows the path;
      course pages show their prerequisites — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance:
      the path-walk e2e spec passes in `en` (this plan's content locale).
- [ ] [AI] **Progression smoothness audit (interview-first, DD-16)** — walk the manifest order and
      confirm the levers hold (prereq-chaining with SF-1/SF-2 bridges; monotonic-ish difficulty;
      skip/fast-path affordances on the landing; refresh register in the four interview courses) per
      [tech-docs §Smoothness Architecture](./tech-docs.md#smoothness-architecture-per-path) —
      acceptance: all levers verified; any regression fixed by soften/bridge in place, never reorder.

### Phase 7 Gate

- [ ] [AI] `interview-ready/software-engineer` manifest published (seeded over the available library); integrity + prerequisite-consistency green; path-walk e2e + breadcrumb + prerequisite display green in `en` (this plan's content locale).
- [ ] [AI] Smoothness audit passes (levers, SF-1/SF-2 bridges, refresh register).
- [ ] [AI] `npx nx run ayokoding-www:build` + `:specs:behavior:coverage` **and** `npx nx run ayokoding-www-fe-e2e:test:e2e` exit 0 (e2e lives in the paired `ayokoding-www-fe-e2e` project — `ayokoding-www:test:e2e` is a no-op echo and can never fail).
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the `interview-ready/software-engineer` path is **live end-to-end** in production
> (landing + manifest + path-aware nav + prerequisites + smoothness) — the **interview-ready MVP is
> shipped**. This is a complete, shippable milestone. Safe to stop indefinitely. To resume: re-run the
> path-walk e2e.

---

## Group C — immediately-effective manifest

## Phase 8: Author the `immediately-effective/software-engineer` manifest + landing + smoothness (zero new bodies)

> _Suggested executor: `apps-ayokoding-www-general-maker`._
> Adds **no new course body** — it composes existing library courses into the immediately-effective
> arc (editor → one language → **build a real app first** → then deepen). Authored over the
> currently-available library and **grows** during Phase 10 backfill as deeper courses land.

- [ ] [AI] Author the manifest **data file** `<MANIFESTS>immediately-effective/software-engineer.yaml`:
      `pathId: immediately-effective/software-engineer`, `title`, `description`, and the ordered
      `courseOrder` = the shipping-first arc from
      [tech-docs §Path `immediately-effective/software-engineer`](./tech-docs.md#path-immediately-effectivesoftware-engineer-build-fast-first)
      and [syllabus/paths/README.md](./syllabus/paths/README.md) — the arc places editor/tooling → one
      language end-to-end → **build a real app first** ahead of CS-fundamentals/DS&A/systems depth —
      acceptance: body duplication = 0 (references shared course IDs only); references only extant
      courses; manifest loads + validates (`npx nx run ayokoding-www:test:unit` exits 0).
- [ ] [AI] Author the thin landing anchor `<PATHS>immediately-effective/software-engineer/_index.md`
      (prose/SEO only — no `courseOrder`); the ordered course list renders from the loaded manifest —
      acceptance: landing renders the manifest-ordered arc.
- [ ] [AI] Update `<PATHS>_index.md` (paths hub) so the `immediately-effective` card is present
      alongside `interview-ready` per [prd.md Screen 1](./prd.md#screen-1--paths-hub-choose-your-path)
      — acceptance: hub shows both published paths.
- [ ] [AI] **Manifest integrity + prerequisite-consistency + no-forked-body check** — every
      `courseOrder` ID resolves; no dup ID; prereq-consistency holds; no body duplicated across
      manifests (all reference by ID) — command: `npx nx run ayokoding-www:test:unit` — acceptance: exits 0.
- [ ] [AI] Verify path-aware nav: prev/next walks the immediately-effective order and preserves
      `?path=immediately-effective/software-engineer`; a course shared with `interview-ready` shows the
      correct neighbor per active path — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance:
      e2e passes in `en` (this plan's content locale); a shared course's prev/next differs by active path.
- [ ] [AI] **Progression smoothness audit (shipping-first, DD-16)** — build-a-real-app precedes CS
      depth; the "you shipped; now understand why" bridge is present on the landing; prereq-chaining
      holds — acceptance: levers verified; regressions fixed by soften/bridge, never reorder.

### Phase 8 Gate

- [ ] [AI] `immediately-effective/software-engineer` manifest published (zero duplicated bodies, seeded over the available library); paths hub shows both published paths.
- [ ] [AI] Integrity + prerequisite-consistency + no-forked-body checks green; per-path prev/next differs correctly for shared courses.
- [ ] [AI] Shipping-first smoothness audit passes.
- [ ] [AI] `npx nx run ayokoding-www:build` + `:specs:behavior:coverage` **and** `npx nx run ayokoding-www-fe-e2e:test:e2e` exit 0 (e2e lives in the paired `ayokoding-www-fe-e2e` project — `ayokoding-www:test:e2e` is a no-op echo and can never fail).
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: two paths are live over one shared library with zero body duplication. Safe to
> stop. To resume: re-run both path-walk e2e specs.

---

## Group D — fundamentally-strong manifest

## Phase 9: Author the `fundamentally-strong/software-engineer` manifest + landing + smoothness (zero new bodies)

> _Suggested executor: `apps-ayokoding-www-general-maker`._
> The NEW university-style path (fundamentals/CS-theory FIRST → deeper). Adds **no new course body** —
> composes existing library courses. Authored over the currently-available library and **grows** during
> Phase 10 backfill.

- [ ] [AI] Author the manifest **data file** `<MANIFESTS>fundamentally-strong/software-engineer.yaml`:
      `pathId: fundamentally-strong/software-engineer`, `title`, `description`, and the ordered
      `courseOrder` = the fundamentals-first arc from
      [tech-docs §Path `fundamentally-strong/software-engineer`](./tech-docs.md#path-fundamentally-strongsoftware-engineer-theory-first)
      and [syllabus/paths/README.md](./syllabus/paths/README.md) — the arc places
      CS-foundations/computer-architecture/paradigms/DS&A/theory FIRST, then systems/architecture depth
      — acceptance: body duplication = 0 (references shared course IDs only); references only extant
      courses; manifest loads + validates (`npx nx run ayokoding-www:test:unit` exits 0).
- [ ] [AI] Author the thin landing anchor `<PATHS>fundamentally-strong/software-engineer/_index.md`
      (prose/SEO only — no `courseOrder`); the ordered course list renders from the loaded manifest —
      acceptance: landing renders the fundamentals-first arc.
- [ ] [AI] Update `<PATHS>_index.md` (paths hub) so **all three** path cards are present per
      [prd.md Screen 1](./prd.md#screen-1--paths-hub-choose-your-path) — acceptance: hub shows all three paths.
- [ ] [AI] **Manifest integrity + prerequisite-consistency + no-forked-body check** across all three
      manifests — command: `npx nx run ayokoding-www:test:unit` — acceptance: exits 0.
- [ ] [AI] Verify path-aware nav: prev/next walks the fundamentals-first order and preserves
      `?path=fundamentally-strong/software-engineer`; a course shared across paths shows the correct
      neighbor per active path — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: e2e passes
      in `en` (this plan's content locale); a shared course's prev/next differs by active path.
- [ ] [AI] **Progression smoothness audit (fundamentals-first, DD-16)** — theory precedes application;
      the "why-before-how" bridges are present; prereq-chaining holds — acceptance: levers verified;
      regressions fixed by soften/bridge, never reorder.

### Phase 9 Gate

- [ ] [AI] `fundamentally-strong/software-engineer` manifest published (zero duplicated bodies, seeded over the available library); paths hub shows all three paths.
- [ ] [AI] Integrity + prerequisite-consistency + no-forked-body checks green across all three manifests; per-path prev/next differs correctly for shared courses.
- [ ] [AI] Fundamentals-first smoothness audit passes.
- [ ] [AI] `npx nx run ayokoding-www:build` + `:specs:behavior:coverage` **and** `npx nx run ayokoding-www-fe-e2e:test:e2e` exit 0 (e2e lives in the paired `ayokoding-www-fe-e2e` project — `ayokoding-www:test:e2e` is a no-op echo and can never fail).
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: all three paths are live over one shared library with zero body duplication (each
> seeded over the currently-available courses). The three-path product skeleton is complete. Safe to
> stop. To resume: re-run the three path-walk e2e specs.

---

## Group E — Backfill (topics 34–94 native + remaining new courses)

## Phase 10: Author the 61 transferred topics + 10 remaining new courses + 8 remaining capstones NATIVE; grow all three manifests

> Each body is authored NATIVE into `<COURSES><course-id>/` (no legacy home, no re-home) per the
> **NEW-course authoring convention** from Phase 6 (V → skeleton with `prerequisites` → learning →
> drilling → content checkers → content fixers → re-verify — see Phase 6's convention note on why
> this uses maker-checker-fixer labels, not RED/GREEN/REFACTOR). These 79 bodies are
> content-independent and **pipeline concurrently** through review (bounded by the cap). As each
> **band** lands, **grow** the
> three manifests (append the newly-available courses into whichever paths include them; re-run
> integrity + prerequisite-consistency) — a serial sync point per band. Per-course detail:
> [syllabus courses layer](./syllabus/courses/README.md) and the tracked
> [Course Library Catalog](./tech-docs.md#course-library-catalog) (the authoritative 121-row table —
> do **not** depend on any `local-temp/` scratch file here; those are gitignored and may be cleaned
> before this phase runs).
>
> **Reconciliation rulings baked into authoring** (locked):
>
> - `defensive-security` is **By-Example hands-on** (Sigma/ELK/OpenSearch + IR + hardening) — author
>   it that way; the catalog's "(concept)" label is WRONG. `detection-engineering-and-siem-operations`
>   owns the deep Wazuh decoder/rule/FP-tuning/dashboard tier and declares `defensive-security` a
>   prerequisite; draw the scope line explicitly.
> - **AI-band scope-guard**: `creating-ai-powered-apps` (use-an-LLM-in-an-app) → `agentic-ai` (a single
>   survey that **forward-links each primitive to its harness-cluster course** and does NOT re-teach at
>   build-your-own depth) → the 5-course harness cluster (build-your-own depth). Bake the cross-reference contract in.
> - `async-python-and-fastapi-services` stays framework-concrete: defer async _concepts_ to
>   `concurrency-and-parallelism` and framework _internals_ to `build-your-own-web-framework`; cross-link both.

**Band 1 — Data depth (T):**

- [ ] [AI] `nosql-databases` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `graph-databases` (By Example · Cypher + Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `database-internals-and-storage-engines` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `data-engineering` (Annotated-concept · Python) — convention complete; checkers clean. _annotated-concept-maker_
- [ ] [AI] `search-and-information-retrieval` (By Example · Python) — convention complete; checkers clean. _by-example-maker_

**Band 2 — Web, backend & platform productivity (T + N):**

- [ ] [AI] `api-design` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `advanced-frontend` (By Example · TypeScript) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `backend-at-scale` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `async-python-and-fastapi-services` (By Example · Python; framework-concrete scope note) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `self-hosting-essentials` (By Example · ops/config) — convention complete; checkers clean. _by-example-maker_
      **Gherkin (binds) →** "The light self-hosting course stays below clusters and IaC"
      — scope-boundary acceptance: the course teaches running one box, containerizing a service, a
      reverse proxy, and PaaS git-push deploy; and its overview **explicitly excludes** clusters,
      Terraform/Packer/Ansible IaC, and Proxmox — verify with
      `grep -ciE 'cluster|terraform|packer|ansible|proxmox' <course>/overview.md` (ERE alternation) returning ≥1
      (the exclusions must be _stated_, not merely absent), and no lesson body teaching them.
- [ ] [AI] `containers-and-orchestration` (By Example · YAML/CLI) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `cloud-and-iac` (Annotated-concept · HCL/YAML) — convention complete; checkers clean. _annotated-concept-maker_
- [ ] [AI] `cicd-and-release-engineering` (By Example · YAML + Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `build-automation-and-task-runners` (By Example · multi-tool) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `information-architecture-and-seo` (Annotated-concept · HTML) — convention complete; checkers clean. _annotated-concept-maker_

**Band 3 — Mobile & desktop platforms (T):**

- [ ] [AI] `just-enough-kotlin` (Primer · Kotlin) — convention complete; checkers clean. _primer-maker_
- [ ] [AI] `android-app-development` (By Example · Kotlin) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `just-enough-swift` (Primer · Swift) — convention complete; checkers clean. _primer-maker_
- [ ] [AI] `ios-app-development` (By Example · Swift) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `just-enough-dart` (Primer · Dart) — convention complete; checkers clean. _primer-maker_
- [ ] [AI] `hybrid-app-development` (By Example · Dart) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `just-enough-csharp` (Primer · C#) — convention complete; checkers clean. _primer-maker_
- [ ] [AI] `windows-app-development` (By Example · C#) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `linux-app-development` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `building-production-cli-tools` (By Example · Go + Rust) — convention complete; checkers clean. _by-example-maker_

**Band 4 — Concurrency languages (T):**

- [ ] [AI] `just-enough-go` (Primer · Go) — convention complete; checkers clean. _primer-maker_
- [ ] [AI] `csp-style-concurrency` (By Example · Go) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `just-enough-elixir` (Primer · Elixir) — convention complete; checkers clean. _primer-maker_
- [ ] [AI] `actor-model-concurrency` (By Example · Elixir) — convention complete; checkers clean. _by-example-maker_

**Band 5 — Architecture, distributed & AI/harness (T + N):**

- [ ] [AI] `software-architecture` (Annotated-concept · Python) — convention complete; checkers clean. _annotated-concept-maker_
- [ ] [AI] `domain-driven-design` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `system-design` (Annotated-concept · Python) — convention complete; checkers clean. _annotated-concept-maker_
- [ ] [AI] `event-driven-architecture` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `distributed-systems` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `build-your-own-web-framework` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `build-your-own-reactive-ui` (By Example · TypeScript) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `creating-ai-powered-apps` (By Example · Python; use-an-LLM scope) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `agentic-ai` (By Example · Python; survey + forward-links, no build-your-own depth) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `browser-automation-with-cdp` (By Example · Python/CDP) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `the-agent-loop` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `agent-tools-and-mcp` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `agent-context-and-memory` (Annotated-concept · Python) — convention complete; checkers clean. _annotated-concept-maker_
- [ ] [AI] `agent-permissions-and-sandboxing` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `agent-orchestration-subagents-and-observability` (Annotated-concept · Python) — convention complete; checkers clean. _annotated-concept-maker_

**Band 6 — Low-level systems, JVM & languages, internals builds (T + N):**

- [ ] [AI] `just-enough-c` (Primer · C) — convention complete; checkers clean. _primer-maker_
- [ ] [AI] `just-enough-cpp` (Primer · C++; prereq `just-enough-c`) — convention complete; checkers clean. _primer-maker_
- [ ] [AI] `linux-os` (By Example · C + shell) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `windows-os` (By Example · C + PowerShell) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `system-programming` (By Example · C) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `just-enough-rust` (Primer · Rust) — convention complete; checkers clean. _primer-maker_
- [ ] [AI] `modern-system-programming` (By Example · Rust) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `just-enough-java` (Primer · Java) — convention complete; checkers clean. _primer-maker_
- [ ] [AI] `enterprise-java-and-the-jvm` (By Example · Java) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `lisp` (By Example · Scheme + Clojure) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `just-enough-fsharp` (Primer · F#) — convention complete; checkers clean. _primer-maker_
- [ ] [AI] `type-systems` (By Example · OCaml + Haskell + F#) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `compilers-parsers-and-transpilers` (By Example · F#) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `build-your-own-git` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `build-your-own-database` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `build-your-own-raft` (By Example · Go) — convention complete; checkers clean. _by-example-maker_

**Band 7 — Security, ops, quality & delivery (T + N):**

- [ ] [AI] `it-and-application-security` (Annotated-concept · Python) — convention complete; checkers clean. _annotated-concept-maker_
- [ ] [AI] `offensive-security` (By Example · Python + shell) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `defensive-security` (By Example · Python + shell; hands-on, NOT concept) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `detection-engineering-and-siem-operations` (By Example · XML/rules + config + Python; prereq `defensive-security`) — convention complete; checkers clean. _by-example-maker_
      **Gherkin (binds) →** "Hands-on detection engineering stays distinct from generalist defensive security"
      — distinctness acceptance: this course has the reader author working Wazuh decoders, correlation
      rules, and a dashboard with false-positive tuning; and `defensive-security` retains the
      generalist Sigma/ELK breadth, IR, and hardening as its distinct scope — verify no lesson title
      is duplicated across the two courses' syllabi.
- [ ] [AI] `vulnerability-management-and-assessment` (By Example · Python) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `it-governance-grc` (Annotated-concept · no code) — convention complete; checkers clean. _annotated-concept-maker_
- [ ] [AI] `bare-metal-virtualization` (By Example · HCL/YAML/shell) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `self-managed-kubernetes-and-gitops` (By Example · YAML/CLI) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `platform-engineering-and-devex` (Annotated-concept · no code) — convention complete; checkers clean. _annotated-concept-maker_
- [ ] [AI] `site-reliability-engineering` (Annotated-concept · Python) — convention complete; checkers clean. _annotated-concept-maker_
- [ ] [AI] `analytics-and-experimentation` (By Example · Python) — convention complete; checkers clean. _by-example-maker_

**Band 8 — Remaining capstones (N, incl. six DD-20 inter-topic capstones):**

- [ ] [AI] `capstone-build-your-own-coding-agent` (Python; assembles the harness cluster) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `capstone-build-your-own-pentest-engine` (TypeScript; swarm + MCP + CDP + security chaining) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `capstone-real-world-delivery` (Python + TS + IaC; DD-20 — embedded spec in `defensive-security.md`) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `capstone-secure-service` (Python + shell; DD-20 — embedded spec in `defensive-security.md`) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `capstone-data-pipeline` (SQL + Python; DD-20 — embedded spec in `defensive-security.md`) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `capstone-concurrency-and-systems` (Go or Elixir + C; DD-20 — embedded spec in `compilers-parsers-and-transpilers.md`) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `capstone-concurrency-showdown` (Go + Elixir; DD-20 — embedded spec in `compilers-parsers-and-transpilers.md`) — convention complete; checkers clean. _by-example-maker_
- [ ] [AI] `capstone-lead-at-altitude` (polyglot + prose; DD-20 — embedded spec in `site-reliability-engineering.md`) — convention complete; checkers clean. _annotated-concept-maker_

**Manifest growth (serial sync point after each band):**

- [ ] [AI] After each band lands, append its newly-available courses into the three manifests
      (`<MANIFESTS>{interview-ready,immediately-effective,fundamentally-strong}/software-engineer.yaml`)
      per each path's arc, then re-run `checkManifestIntegrity` + `checkPrerequisiteConsistency` +
      no-forked-body — command: `npx nx run ayokoding-www:test:unit` — acceptance: exits 0 after each growth.
- [ ] [AI] After the final band, confirm all three manifests reference the intended full arcs (no
      omitted-by-mistake courses; omit-or-create honored) and the library holds the full **121-course**
      catalog — command: `npx nx run ayokoding-www:build` — acceptance: 121 course bundles resolve; all three manifests validate.

### Phase 10 Gate

- [ ] [AI] All 61 transferred topics + 10 remaining new courses + 8 remaining capstones (2 original + 6 DD-20 inter-topic capstones) authored NATIVE under `<COURSES>` with declared prerequisites; each passed its checker + facts + link checkers.
- [ ] [AI] Reconciliation rulings applied (defensive-security By-Example label; AI-band scope-guard; async-fastapi scope note).
- [ ] [AI] All three manifests grown to their full arcs; integrity + prerequisite-consistency + no-forked-body green; full 121-course library resolves.
- [ ] [AI] `<COURSES>_index.md` catalog updated to the full 121; `npx nx run ayokoding-www:build` + link + heading + markdownlint green.
- [ ] [AI] Every band/course sub-phase PR is `[AI]`-merged and deployed.

> **Pause Safety**: the full 121-course library exists and all three path manifests are complete over
> one shared library with zero body duplication. The whole three-path product is content-complete. Safe
> to stop. To resume: re-run the section build + integrity checks.

---

## Group Finalization

## Phase 11: Section & App Verification

- [ ] [AI] Run affected quality gates from the worktree:
      `npx nx affected -t typecheck lint test:quick test:unit test:integration test:e2e specs:behavior:coverage`
      — acceptance: exits 0. Fix ALL failures, including preexisting ones (Root Cause Orientation),
      committing preexisting fixes separately.
- [ ] [AI] Build the site: `npx nx run ayokoding-www:build` — acceptance: exits 0.
- [ ] [AI] Run link + heading-hierarchy + markdown validation:
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md links validate` +
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md heading-hierarchy validate` + `npm run lint:md` (the actual mechanism — not `nx run` targets; both `md` subcommands also run
      automatically pre-commit via `lint-staged` for every staged `.md` file) — acceptance: all green.
- [ ] [AI] **Manifest-integrity + prerequisite-consistency sweep** — all three manifests: every
      `courseOrder` ID resolves; no dup ID; prereq-consistency holds; no forked body across paths —
      acceptance: integrity check reports zero violations across all three.
- [ ] [AI] **All-path smoothness re-check (DD-16)** — re-verify the levers for each manifest in the
      landed content — acceptance: all three paths pass.

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes
> (Root Cause Orientation). Commit preexisting fixes separately with conventional-commit messages.

### Phase 11 Gate

- [ ] [AI] Affected `typecheck/lint/test:quick/test:unit/test:integration/test:e2e/specs:behavior:coverage` exit 0.
- [ ] [AI] Build + link + heading + markdown validation green; manifest integrity + prerequisite-consistency + all-path smoothness pass.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the whole three-path product passes all automated gates. Safe to stop. To resume:
> re-run the affected quality gates + build.

---

## Phase 12: Manual UI Verification + Rule-15 Three-Tester Retest

> Path-aware navigation is a user-facing change, so a live-site retest is required before archival.
> **Locale scope**: this plan's course/path content is authored `en`-only — per
> [brd.md §Business-Scope Non-Goals](./brd.md#business-scope-non-goals), an Indonesian content mirror
> is explicitly deferred. Retest content screens (paths hub, path landings, course pages) in `en`
> only; do not fabricate an `id` content walk-through for a feature with no `id` content. The
> path-aware nav UI code itself remains locale-neutral (it renders whatever locale-specific content
> exists), so this scoping is a content-availability fact, not a code limitation.

- [ ] [AI] Confirm `en` is the content locale for the course library (no `id` mirror exists for this
      feature) — command: `test -d apps/ayokoding-www/content/en/learn/courses` — acceptance: directory
      exists; no sibling `id/learn/courses` directory is expected or required.
- [ ] [AI] Start dev server: `npx nx dev ayokoding-www` — acceptance: server up.
- [ ] [AI] For `en` × breakpoints (375 / 768 / 1280 px), via Playwright MCP: open the paths hub
      (three cards), each of the three path landings, walk 2–3 courses via prev/next (confirm `?path=`
      persists + order + breadcrumb), open a course and confirm its **prerequisite display**, deep-link
      a course without `?path=` (canonical view + "part of paths" affordance), hit an invalid `?path=`
      (canonical view), and an old `fundamentally-strong/software-engineer/<slug>` URL (redirect to
      `/en/c/learn/courses/<id>`). Verify `html[lang]` is `en` and `browser_console_messages` is
      clean — acceptance: all behaviors correct; zero console errors.
- [ ] [AI] Capture one screenshot per screen per breakpoint to
      `evidence/phase-12-<screen>-en-<breakpoint>px.png` — acceptance: files exist in `evidence/`.
- [ ] [AI] Run the three live-site testers (the `web-ux-test-fixing-planning` workflow:
      `web-exploratory-tester` + `web-usability-tester` + `web-design-tester`) against the running
      paths hub, all three path landings, and sample courses (`en` content) — acceptance: EWT/UWT/DWT
      findings + spec-gaps recorded.
- [ ] [AI] Append each finding below as a new unchecked checkbox, source-attributed
      (`- [ ] EWT-NNN:` / `- [ ] UWT-NNN:` / `- [ ] DWT-NNN: <defect> — fix before archival`); append
      any SG-###/USS-### items to the relevant spec/content step.

### Rule-15 retest follow-ups

- [ ] [AI] _(populated during the retest — every EWT/UWT/DWT defect finding must be fixed/ticked before
      archival; deferral of a defect requires explicit user permission and only when genuinely
      impossible; SG-###/USS-### may be triaged or deferred with rationale)_

### Phase 12 Gate

- [ ] [AI] All screens (three-card hub + three landings + sample courses + prerequisite display) verified in `en` across all breakpoints; screenshots in `evidence/`; console clean.
- [ ] [AI] All rule-15 EWT/UWT/DWT defect findings fixed (ticked) or explicitly permitted to defer.
- [ ] [AI] Draft PR opened (retest evidence + any fixes); 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the three-path UI is verified live and defect-clean in `en` (this plan's content
> locale; the nav mechanism itself is locale-neutral). Safe to stop. To resume: re-run the three
> testers against the running app.

---

## Phase 13: Final `origin/main` Integration & CI Verification

- [ ] [AI] Confirm no plan PR is still open: every prior phase branch has been `[AI]`-merged to `main`
      (`gh pr list --search "fundamentally-strong-shared-course-tracks" --state open` returns zero) —
      acceptance: no open plan PRs remain.
- [ ] [AI] Sync the shared worktree to latest `origin/main` and run the full affected suite:
      `npx nx affected -t typecheck lint test:quick test:unit test:integration test:e2e specs:behavior:coverage` + `npx nx run ayokoding-www:build` — acceptance: all exit 0 on the integrated `main`.
- [ ] [AI] Monitor the final `main` CI run (poll every ~2 min; one `gh run view --json
status,conclusion` per wakeup; never `gh run watch`) — acceptance: all GitHub Actions green; fix root
      causes and push follow-ups (own PR → review → `[AI]` merge) until green.
- [ ] [AI] Confirm `prod-ayokoding-www` serves all three paths + the full library; re-dispatch
      `apps-ayokoding-www-deployer` if any earlier deploy lagged — acceptance: production serves the
      three-path product.

### Phase 13 Gate

- [ ] [AI] Zero open plan PRs; every prior phase merged to `main`.
- [ ] [AI] Full affected suite + build green on integrated `main`; final `main` CI run green.
- [ ] [AI] `prod-ayokoding-www` serving all three paths + the full library.

> **Pause Safety**: the whole plan is integrated on `main`, green in CI, and live in production. Safe
> to stop. To resume: re-run the affected suite on `main` and check CI/prod status.

---

## Phase 14: Knowledge Capture

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)._

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only if a durable surface would
      catch this automatically next time; discard the rest with a one-line reason — acceptance: every
      entry has a route or a discard reason.
- [ ] [AI] Apply the **secret/sensitivity gate** to every surviving entry — sanitize any secret to a
      `<placeholder>` token or discard if unsanitizable — acceptance: `learnings.md` contains no raw secret.
- [ ] [AI] Apply the **repo-relevance gate** — infra-private content stays in `ose-infra` only and is
      never cross-routed here; public-governance content may propagate via the parity loop —
      acceptance: no infra-private content in routed output.
- [ ] [AI] Route each surviving learning to exactly one durable home; **code-homed** learnings
      (any `apps/`- or `libs/`-homed learning, e.g. `course-paths`, or tests) are ALWAYS filed as a
      separate `plans/backlog/<slug>/` plan, never landed inline — acceptance: every entry records its
      terminal routing state.
- [ ] [AI] If no generalizable learning surfaced, record `No generalizable learnings — <reason>` in
      `learnings.md` — acceptance: `learnings.md` is never silently empty.

### Phase 14 Gate

- [ ] [AI] Every `learnings.md` entry is terminal (routed inline / filed as backlog / discarded) or the "none" escape is present.
- [ ] [AI] No code-homed learning landed inline in this plan's own commits/PR.
- [ ] [AI] Draft PR opened (`learnings.md` triage); 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed (no-op).

> **Pause Safety**: `learnings.md` is fully triaged; nothing depends on querying it later. Safe to
> stop. To resume: re-read `learnings.md` and confirm every entry is terminal.

---

## Phase 15: Plan Archival

- [ ] [AI] Verify ALL delivery checklist items are ticked.
- [ ] [AI] Verify the Knowledge Capture phase is complete (every entry terminal or explicit "none" escape; both safety gates applied).
- [ ] [AI] Verify ALL quality gates pass (local + CI) and the build is green.
- [ ] [AI] Verify ALL manual assertions pass (Playwright MCP) with committed evidence in `evidence/`; the `en` content locale exercised (per brd.md's Indonesian-mirror-deferred non-goal).
- [ ] [AI] Verify every rule-15 EWT/UWT/DWT defect finding is fixed (ticked) — deferral requires explicit user permission (only when genuinely impossible); SG-###/USS-### may be triaged/deferred.
- [ ] [AI] Verify all three path manifests are published, all three landings live, the paths hub shows all three paths, and the library holds the full 121 courses; every prior-phase PR `[AI]`-merged and deployed (Phase 13 checkpoint green).
- [ ] [AI] Move: `git mv plans/in-progress/fundamentally-strong-shared-course-tracks/
plans/done/YYYY-MM-DD__fundamentally-strong-shared-course-tracks/` using today's completion date (the
      `evidence/` subfolder moves with it).
- [ ] [AI] Update `plans/in-progress/README.md` — remove the plan entry.
- [ ] [AI] Update `plans/done/README.md` — add the plan entry with completion date.
- [ ] [AI] Update any other READMEs that reference this plan (e.g. `plans/README.md`, `plans/backlog/README.md`).
- [ ] [AI] Commit the archival: `chore(plans): move fundamentally-strong-shared-course-tracks to done`.

### Phase 15 Gate

- [ ] [AI] Plan folder is under `plans/done/YYYY-MM-DD__...`; all READMEs updated; archival committed.
- [ ] [AI] Draft PR opened (archival move); 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed (no-op).

> **Pause Safety**: the plan is archived and its final PR `[AI]`-merged to `main`. Terminal state. To
> resume: nothing — the plan is complete.

---

### Commit Guidelines (all phases)

- [ ] [AI] Commit changes thematically — group related changes into logically cohesive commits.
- [ ] [AI] Follow Conventional Commits: `<type>(<scope>): <description>` (imperative, no period).
- [ ] [AI] Split domains/concerns into separate commits; preexisting fixes get their own commits.
- [ ] [AI] Do NOT bundle unrelated changes into a single commit.

### Local Quality Gates (Before Every Push)

- [ ] [AI] `npx nx affected -t typecheck` exits 0.
- [ ] [AI] `npx nx affected -t lint` exits 0.
- [ ] [AI] `npx nx affected -t test:quick test:unit` exits 0 (add `test:integration test:e2e` for the nav-feature phases).
- [ ] [AI] `npx nx affected -t specs:behavior:coverage` exits 0.
- [ ] [AI] Fix ALL failures — including preexisting issues not caused by your changes (Root Cause Orientation).

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes.
> Commit preexisting fixes separately with appropriate conventional-commit messages.

### Note: plan location at archival time

This plan was promoted from `backlog/` to `in-progress/fundamentally-strong-shared-course-tracks/`
(date prefix stripped) on 2026-07-19, per the plan lifecycle. The `git mv` in Phase 15 therefore
archives from that `in-progress/` path to `done/YYYY-MM-DD__fundamentally-strong-shared-course-tracks/`
using the completion date.
