# Delivery Checklist — Fundamentally Strong Shared Course Library, Two Tracks

This checklist delivers the two-path shared-course-library in three groups (A architecture & UI, B
job-seeking path first, C software-engineer path) plus finalization. The catalog of courses, the
course-ID + manifest schema, the path-aware-navigation UI design, and both path orderings live in
[tech-docs.md](./tech-docs.md); the UI-design-funnel and NEW-course specs live in [prd.md](./prd.md).

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
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

> **DN-7 DECIDED — `[AI]` auto-merge (plan-scoped deviation)**: the repo's
> [PR Merge Protocol](../../../repo-governance/development/workflow/pr-merge-protocol.md) normally
> requires a `[HUMAN]` merge with explicit per-instance approval. For **this plan only**, the
> maintainer explicitly authorized (2026-07-18, in-session — modeled on the sibling plan
> `fundamentally-strong-software-engineer`'s own separately-recorded authorization) that `[AI]` merges
> automatically once the 3-cycle review and all quality gates are green, via two directives: (a) this
> plan uses the SAME delivery methods as the sibling plan, and (b) no maintainer permission is needed
> to merge a PR once it has passed 3 review cycles and the PR quality gate. This resolves
> **DN-7 = AI-auto-merge**; it does **not** amend `pr-merge-protocol.md` and applies to no other plan.

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
   `[AI]` auto-merge per DN-7.
5. [AI] Dispatch `apps-ayokoding-www-deployer` to deploy `ayokoding-www` to `prod-ayokoding-www` — a
   no-op redeploy for plan-side-only phases.

**Parallelization**: Group A phases are serial (each builds on the prior feature slice). Group B's
NEW-course authoring phases are mutually independent (each writes only its own `courses/<id>/`
subtree) and may pipeline through review concurrently, bounded by the in-force subagent/PR-review
concurrency cap; Group B's re-home and manifest phases are serial sync points. Group C is serial and
starts only after Group B has fully merged (job-seeking path live first).

**Path constants** (referenced throughout):

- `<COURSES>` = `apps/ayokoding-www/content/en/learn/fundamentally-strong/courses/`
- `<PATHS>` = `apps/ayokoding-www/content/en/learn/fundamentally-strong/paths/`
- `<SE_OLD>` = `apps/ayokoding-www/content/en/learn/fundamentally-strong/software-engineer/`
- `<FEAT>` = `apps/ayokoding-www/src/features/course-paths/`
- `<SPECS>` = `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/course-paths/`

---

## Phase 0: Environment Setup, Baseline & Precondition

> _Executor: repo-setup-manager_

- [ ] [AI] **Precondition gate** — confirm the sibling plan
      `plans/in-progress/fundamentally-strong-software-engineer/` is DONE: verify every existing course
      folder from the [Course Library Catalog](./tech-docs.md#course-library-catalog) exists under
      `<SE_OLD>` via the verbatim loop over all 97 existing course/capstone IDs:
      `for s in actor-model-concurrency advanced-algorithms advanced-frontend advanced-networking advanced-sql-and-query-performance agentic-ai agentic-coding analytics-and-experimentation android-app-development api-design backend-at-scale backend-essentials bare-metal-virtualization build-automation-and-task-runners build-your-own-database build-your-own-git build-your-own-orm-and-query-builder build-your-own-raft build-your-own-reactive-ui build-your-own-web-framework building-production-cli-tools capstone-first-working-software capstone-forge-ready capstone-full-stack-app cicd-and-release-engineering cloud-and-iac compilers-parsers-and-transpilers computer-architecture computer-science-foundations concurrency-and-parallelism containers-and-orchestration creating-ai-powered-apps csp-style-concurrency data-access-orms-and-query-builders data-engineering data-structures-and-algorithms-essentials database-internals-and-storage-engines debugging-and-profiling defensive-security distributed-systems domain-driven-design engineering-management enterprise-java-and-the-jvm event-driven-architecture extending-neovim frontend-essentials functional-programming graph-databases hybrid-app-development information-architecture-and-seo ios-app-development it-and-application-security it-governance-grc just-enough-bash just-enough-c just-enough-csharp just-enough-dart just-enough-elixir just-enough-fsharp just-enough-go just-enough-java just-enough-kotlin just-enough-lua just-enough-nvim just-enough-python just-enough-rust just-enough-swift just-enough-typescript linux-app-development linux-os lisp modern-system-programming networking-essentials nosql-databases object-oriented-design-and-patterns object-oriented-programming-essentials offensive-security platform-engineering-and-devex programming-paradigms project-management search-and-information-retrieval security-essentials self-managed-kubernetes-and-gitops site-reliability-engineering software-architecture software-engineering-practices software-product-engineering software-testing sql-essentials system-design system-programming technical-communication type-systems version-control-and-git vulnerability-management-and-assessment windows-app-development windows-os; do test -d <SE_OLD>$s || echo "MISSING $s"; done`
      — acceptance: zero `MISSING` lines; if any is missing, STOP — the dependency is not satisfied.
- [ ] [AI] Enter/provision the worktree and install dependencies in the root worktree: `npm install`
      — acceptance: exits 0, `node_modules/` synchronized.
- [ ] [AI] Converge the toolchain in the root worktree: `npm run doctor -- --fix`
      — acceptance: exits 0 with no unresolved drift.
- [ ] [AI] Establish baselines: `npx nx run ayokoding-www:build` and
      `npx nx run ayokoding-www:test:unit` and `npx nx run ayokoding-www:test:integration`
      — acceptance: all exit 0; record pass state.
- [ ] [AI] Snapshot current content + nav state to `evidence/phase-0-snapshot.txt`: the `<SE_OLD>`
      folder inventory, the existing `content-url.ts` / `prev-next.tsx` / `tree-builder.ts` behavior,
      and the current `next.config.ts` locale set — acceptance: snapshot committed.
- [ ] [AI] Confirm the seventeen NEW slugs are absent (no collision) under `<SE_OLD>` and `<COURSES>`:
      `for s in coding-interview take-home-and-live-coding system-design-interview behavioral-and-leadership-interviews capstone-interview-loop async-python-and-fastapi-services self-hosting-essentials browser-automation-with-cdp the-agent-loop agent-tools-and-mcp agent-context-and-memory agent-permissions-and-sandboxing agent-orchestration-subagents-and-observability capstone-build-your-own-coding-agent just-enough-cpp detection-engineering-and-siem-operations capstone-build-your-own-pentest-engine; do test -e <SE_OLD>$s && echo "EXISTS $s"; done`
      — acceptance: zero `EXISTS` lines.
- [ ] [AI] Confirm `learnings.md` scaffold exists in the plan folder — acceptance: file present with its H1.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [ ] [AI] Precondition met: all existing course folders exist (zero `MISSING`); all 17 new slugs absent.
- [ ] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift.
- [ ] [AI] `ayokoding-www:build` + `test:unit` + `test:integration` baselines recorded green.
- [ ] [AI] `evidence/phase-0-snapshot.txt` committed.
- [ ] [AI] Draft PR opened; CI triggered; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged;
      `ayokoding-www` deployed (no-op redeploy).

> **Pause Safety**: only the toolchain was verified and the current state snapshotted — no content or
> code changed. Safe to stop indefinitely. To resume: re-run the precondition gate and baselines.

---

## Group A — Architecture & UI foundation

## Phase 1: UI design funnel + library/paths content homes + manifest schema

> _Suggested executor: `web-researcher` (R7 prior art) + `swe-developing-frontend-ui` skill for the
> funnel; `swe-typescript-dev` for the schema._

- [ ] [AI] **R5 survey** — read `libs/web-ui` component inventory + tokens + Storybook and the
      ayokoding app-shell + existing `sidebar-tree`/`breadcrumb`/`prev-next`/`section-card`
      [Repo-grounded] — acceptance: net-new components (`PathCard`, `PathLanding`, `PathBanner`,
      `PathCourseLinks`) named in `tech-docs.md`; existing primitives to reuse listed in notes.
  - _Suggested executor: `swe-developing-frontend-ui` skill_
- [ ] [AI] **R7 prior art** — delegate to `web-researcher` a survey of how comparable platforms
      present a track/path over shared lessons (roadmap.sh, Exercism, freeCodeCamp, Coursera) —
      acceptance: cited findings folded into `prd.md` funnel notes; no `[Unverified]` prior-art claim.
- [ ] [AI] **Produce hi-fi finalists** — author the 2 `.excalidraw.png` finalists per screen (paths
      hub, path landing, course-in-path) into `assets/` per
      [prd.md §UI-Design-Funnel](./prd.md#ui-design-funnel-path-aware-navigation-screens) and confirm
      the embedded `![]()` links resolve — acceptance: `grep -c "excalidraw.png" prd.md` ≥ 6; each
      selection + rationale table present (`grep -c "Selected:" prd.md` ≥ 3).
- [ ] [AI] **Library + paths content homes** — create `<COURSES>_index.md` (library landing, weight +
      title) and `<PATHS>_index.md` (paths hub / choose-a-path landing) mirroring an existing section
      `_index.md` — acceptance: `test -f <COURSES>_index.md` and `test -f <PATHS>_index.md`; build green.
- [ ] [AI] **Manifest data-file schema definition** — write the `PathManifest` zod schema
      (`pathId`, `title`, `description`, `courseOrder[]`, optional per-course `framing`) into
      `<FEAT>core/schemas.ts`, matching the standalone YAML data-file format (RESOLVED, OQ-2 — NOT
      `_index.md` frontmatter), per
      [tech-docs §Path = ordered manifest](./tech-docs.md#path--ordered-manifest-manifest-format)
      — acceptance: schema compiles (`npx nx run ayokoding-www:typecheck` exits 0).
- [ ] [AI] **Manifest data-file directory** — create `<FEAT>manifests/` (the standalone-data-file home,
      source of truth) with a `README.md` note that `<path-id>.yaml` files land here in Groups B/C —
      acceptance: `test -d <FEAT>manifests` and `test -f <FEAT>manifests/README.md`.

### Phase 1 Gate

- [ ] [AI] Funnel finalists + selections + rationale present in `prd.md`; assets embedded and resolve.
- [ ] [AI] `<COURSES>_index.md` + `<PATHS>_index.md` created; `PathManifest` schema compiles;
      `<FEAT>manifests/` data-file directory exists.
- [ ] [AI] `npx nx run ayokoding-www:build` + `:typecheck` exit 0.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the design is fixed and the empty library/paths homes + manifest schema exist; no
> bodies moved, no nav behavior changed. Safe to stop. To resume: re-run `:typecheck`.

---

## Phase 2: `course-paths` core (pure) — TDD + specs RED

> _Suggested executor: `swe-typescript-dev` (core logic) + `specs-maker` (Gherkin)._

- [ ] [AI] **Specs RED** — author the `course-paths` Gherkin companion under `<SPECS>` (one `.feature`
      per behavior: path-order nav, breadcrumb, canonical fallback, invalid-path fallback, omitted
      course, manifest integrity) from
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
    Given a reader opens a course URL with no path context query parameter
    When the course page renders
    Then the course body renders in full with the content-tree breadcrumb
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
      `apps/ayokoding-www/src/features/content/core/content-url.test.ts` for `contentUrl(locale, slug,
pathId)` appending `?path=<pathId>` — command: `npx nx run ayokoding-www:test:unit` — acceptance:
      fails (param not yet supported).

  **Gherkin (underpins) →** "A path landing page lists its courses in manifest order"; "Prev and next
  follow the active path's order"; "The breadcrumb reflects the active path"; "An old
  software-engineer URL redirects to the canonical course URL"

  ```gherkin
  Scenario: A path landing page lists its courses in manifest order
    Given the job-seeking-software-engineer path manifest is published
    When a reader opens the path landing page
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
    Then it shows Home, Fundamentally Strong, the path title, and the course title
    And the path crumb links to the path landing page with the path context preserved

  Scenario: An old software-engineer URL redirects to the canonical course URL
    Given a re-homed course previously lived under the software-engineer content path
    When a reader requests the old URL
    Then the app redirects to the course's canonical /courses/<course-id> URL
    And the redirect preserves any path context query parameter
  ```

- [ ] [AI] **GREEN** — extend `content-url.ts` with the optional `pathId` param appending `?path=`
      [Repo-grounded — `apps/ayokoding-www/src/features/content/core/content-url.ts`] — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: the new test passes; existing `content-url`
      tests still pass.
- [ ] [AI] **REFACTOR** — extract shared course-ref types; ensure `core/` stays IO-free (pure) —
      command: `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:typecheck` — acceptance:
      all green; no `fs`/React import in `core/`.

### Phase 2 Gate

- [ ] [AI] `resolvePathNav` + `parsePathContext` + `contentUrl(pathId)` implemented; unit tests green.
- [ ] [AI] `course-paths` Gherkin authored under `<SPECS>`; `specs:behavior:coverage` now maps the
      new features (step bindings land in Phase 3 — record the coverage delta).
- [ ] [AI] `npx nx run ayokoding-www:test:unit` + `:typecheck` + `:lint` exit 0.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the pure ordering + context logic is implemented and unit-tested; no route or
> component consumes it yet, so nav behavior is unchanged. Safe to stop. To resume: `:test:unit`.

---

## Phase 3: `course-paths` shell + route wiring + redirects — integration TDD

> _Suggested executor: `swe-typescript-dev`._

- [ ] [AI] **RED** — write failing integration tests for `<FEAT>shell/manifest-repository.ts` (loads and
      validates each `<FEAT>manifests/<path-id>.yaml` data file into a `PathManifest[]` via the
      `schemas.ts` zod schema) — command:
      `npx nx run ayokoding-www:test:integration` — acceptance: tests fail (repository wiring absent).

  **Gherkin (underpins) →** "A path landing page lists its courses in manifest order"; "Both paths
  reference a shared course with no body duplication"

  ```gherkin
  Scenario: A path landing page lists its courses in manifest order
    Given the job-seeking-software-engineer path manifest is published
    When a reader opens the path landing page
    Then the courses appear in the manifest's courseOrder
    And every course link carries the path context query parameter

  Scenario: Both paths reference a shared course with no body duplication
    Given a course appears in both path manifests
    When the course library is inspected
    Then exactly one canonical body exists for that course
    And each manifest references the course by its stable course ID
  ```

- [ ] [AI] **RED** — write a failing integration test for the content service resolving
      `(courseId, activePath)` → path-aware prev/next — command:
      `npx nx run ayokoding-www:test:integration` — acceptance: test fails (service wiring absent).

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
      at authoring time (Path A: current LTS-compatible latest patch, CVE-clean) — acceptance:
      `js-yaml` appears in `apps/ayokoding-www/package.json` `dependencies` with an exact version; `npm
    install` resolves with no peer-dependency warning for it.
- [ ] [AI] **GREEN** — implement `<FEAT>shell/manifest-repository.ts` to read + parse each
      `<FEAT>manifests/<path-id>.yaml` data file via the now-direct `js-yaml` dependency (RESOLVED: the
      manifest data files are always `.yaml`; no JSON fallback); extend the content index to carry
      loaded manifests alongside `trees`/`prevNext`
      [Repo-grounded — `ContentIndex` in `apps/ayokoding-www/src/features/content/core/types.ts` and
      the service in `.../content/shell/service.ts`] — command:
      `npx nx run ayokoding-www:test:integration` — acceptance: the new integration tests pass.
- [ ] [AI] **RED** — write a failing unit test in `<FEAT>core/manifest-integrity.test.ts` for
      `checkManifestIntegrity(manifest, libraryCourseIds)` asserting it reports every `courseOrder`
      entry whose ID is absent from `libraryCourseIds` and every ID that appears more than once in
      the same manifest — command: `npx nx run ayokoding-www:test:unit` — acceptance: test fails
      (`checkManifestIntegrity` undefined).

  **Gherkin (binds) →** "Every manifest course reference resolves to a real course"

  ```gherkin
  Scenario: Every manifest course reference resolves to a real course
    Given a path manifest lists a courseOrder of course IDs
    When the manifest-integrity check runs
    Then every listed course ID resolves to an existing course in the library
    And no course ID appears more than once in the manifest
  ```

- [ ] [AI] **GREEN** — implement `checkManifestIntegrity(manifest, libraryCourseIds)` in
      `<FEAT>core/manifest-integrity.ts` (pure function; no IO) returning the set of unresolved and
      duplicate course IDs — command: `npx nx run ayokoding-www:test:unit` — acceptance: the new test
      passes; wire it into `manifest-repository.ts` so a load with any unresolved/duplicate ID throws
      at build time (this is the check Phase 7/8 invoke against each published manifest).
- [ ] [AI] **REFACTOR** — ensure `manifest-integrity.ts` stays IO-free (pure) alongside the rest of
      `<FEAT>core/` — command: `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:typecheck`
      — acceptance: all green; no `fs`/React import in `core/`.
- [ ] [AI] **GREEN** — wire the course route: in
      `apps/ayokoding-www/src/app/[locale]/(content)/c/[...slug]/page.tsx` [Repo-grounded] read
      `searchParams.path`, call `parsePathContext`, and render path-aware prev/next + breadcrumb when a
      valid path context resolves and the course is in that manifest; else render the canonical view.
      Extend `navigation/shell/prev-next.tsx` and `navigation/shell/breadcrumb.tsx` to accept an
      optional path context (links carry `?path=`) — command: `npx nx run ayokoding-www:build` —
      acceptance: build green; canonical (no-path) rendering unchanged for non-path routes.
- [ ] [AI] **GREEN** — author `<FEAT>shell/path-banner.tsx` (in-path affordance) and
      `<FEAT>shell/path-course-links.tsx` ("this course is part of: …") consumed by the course page —
      command: `npx nx run ayokoding-www:test:unit` (component tests) — acceptance: tests pass.
- [ ] [AI] **GREEN** — add redirects for re-homed courses: for every existing course, a redirect from
      `.../software-engineer/<slug>` to `.../courses/<course-id>` in
      `apps/ayokoding-www/src/redirects/` [Repo-grounded — precedent
      `.../gherkin/navigation/learn-reorg-redirects.feature`] — command:
      `npx nx run ayokoding-www:test:integration` — acceptance: redirect resolution test passes.
- [ ] [AI] **GREEN (specs)** — implement the step bindings so the `<SPECS>` Gherkin scenarios execute —
      command: `npx nx run ayokoding-www:specs:behavior:coverage` — acceptance: exits 0.
- [ ] [AI] **REFACTOR** — deduplicate breadcrumb/prev-next path-vs-canonical branches; keep `shell/`
      the only IO — command:
      `npx nx run ayokoding-www:test:unit && :test:integration && :typecheck && :lint` — acceptance: all green.

### Phase 3 Gate

- [ ] [AI] Manifest loading + path-aware route wiring + redirects implemented; integration tests green.
- [ ] [AI] `specs:behavior:coverage` green; canonical (no-path) nav unchanged (retained nav specs pass).
- [ ] [AI] `npx nx run ayokoding-www:test:unit` + `:test:integration` + `:build` + `:typecheck` + `:lint` exit 0.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the feature resolves a manifest + path context end-to-end (no manifests published
> yet, so the canonical view is what renders); redirects are in place. Safe to stop. To resume:
> `:test:integration`.

---

## Phase 4: Path landing + paths hub components + e2e

> _Suggested executor: `swe-typescript-dev` + `swe-e2e-dev`._

- [ ] [AI] **GREEN** — author `<FEAT>shell/path-landing.tsx` (renders a manifest's ordered, phase-grouped
      course list, links carry `?path=`) and `<FEAT>shell/path-card.tsx` (paths-hub card), rendered by
      `<PATHS>_index.md` / `<PATHS><path-id>/_index.md`, per
      [prd.md Screen 1/2 selected designs](./prd.md#ui-design-funnel-path-aware-navigation-screens) —
      command: `npx nx run ayokoding-www:build` — acceptance: build green; components render.
- [ ] [AI] **RED (e2e)** — write failing Playwright e2e specs in the ayokoding e2e suite for: path
      landing lists courses in manifest order; prev/next walks the path and preserves `?path=`;
      breadcrumb shows the path; deep-link without `?path=` → canonical view; invalid `?path=` →
      canonical view; old `software-engineer/<slug>` URL → redirect to `courses/<id>` — command:
      `npx nx run ayokoding-www:test:e2e` — acceptance: e2e specs fail (no published manifest/data yet).
  - _Suggested executor: `swe-e2e-dev`_

  **Gherkin (binds) →** "A path landing page lists its courses in manifest order"; "Prev and next
  follow the active path's order"; "The breadcrumb reflects the active path"; "A course deep-linked
  without path context renders the canonical view"; "An invalid path context falls back to the
  canonical view"; "An old software-engineer URL redirects to the canonical course URL"

  ```gherkin
  Scenario: A path landing page lists its courses in manifest order
    Given the job-seeking-software-engineer path manifest is published
    When a reader opens the path landing page
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
    Then it shows Home, Fundamentally Strong, the path title, and the course title
    And the path crumb links to the path landing page with the path context preserved

  Scenario: A course deep-linked without path context renders the canonical view
    Given a reader opens a course URL with no path context query parameter
    When the course page renders
    Then the course body renders in full with the content-tree breadcrumb
    And a "this course is part of" affordance lists every path that includes the course

  Scenario: An invalid path context falls back to the canonical view
    Given a reader opens a course URL with a path context that names no known path
    When the course page renders
    Then the course renders the canonical standalone view
    And no error is shown

  Scenario: An old software-engineer URL redirects to the canonical course URL
    Given a re-homed course previously lived under the software-engineer content path
    When a reader requests the old URL
    Then the app redirects to the course's canonical /courses/<course-id> URL
    And the redirect preserves any path context query parameter
  ```

- [ ] [AI] **GREEN (e2e fixtures)** — add a minimal fixture manifest (a few real course IDs) so the e2e
      specs exercise the real components — command: `npx nx run ayokoding-www:test:e2e` — acceptance:
      all `course-paths` e2e specs pass across all supported locales.
- [ ] [AI] **REFACTOR** — ensure the landing + hub reuse `libs/web-ui` primitives (no bespoke CSS where
      a token exists); a11y pass (labels, focus, `aria-current`) — command:
      `npx nx run ayokoding-www:test:e2e && :lint` — acceptance: green; a11y assertions pass.

### Phase 4 Gate

- [ ] [AI] Path landing + paths hub render from a manifest; all `course-paths` e2e specs green across locales.
- [ ] [AI] `npx nx run ayokoding-www:test:unit` + `:test:integration` + `:test:e2e` + `:build` + `:lint` + `:specs:behavior:coverage` exit 0.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the full path-aware navigation UI is implemented, tested (unit + integration + e2e
>
> - specs), and live — but no real path manifests are published yet, so production still shows the
>   canonical library. Safe to stop. To resume: `:test:e2e`.

---

## Group B — Job-Seeking-Software-Engineer path (delivered first, end-to-end)

## Phase 5: Re-home the shared course library into `courses/`

> _Suggested executor: `docs-file-manager` (mechanical moves) + `swe-typescript-dev` (redirect wiring)._
> The interview-first path spans the whole library, so Group B extracts **all** existing shared course
> bodies into `courses/` (Group C then reuses them with zero new bodies).

- [ ] [AI] For **every** existing course + capstone, `git mv <SE_OLD><slug>/ <COURSES><course-id>/`
      (course-id = slug; no rename of the slug itself), preserving the full page-bundle
      (`_index.md` + `overview.md` + `learning/` + `drilling/`) — acceptance: `<SE_OLD>` holds no course
      folders; every course resolves under `<COURSES>`; `npx nx run ayokoding-www:generate-indexes`
      succeeds and `:build` exits 0.
- [ ] [AI] Confirm each re-homed course has its redirect (Phase 3) old-URL → new-URL resolving —
      command: `npx nx run ayokoding-www:test:integration` — acceptance: redirect specs green for all moved courses.
- [ ] [AI] Update `<COURSES>_index.md` (library landing) to list the full catalog by course ID —
      acceptance: link-checker green; every catalog link resolves.
- [ ] [AI] Sweep any intra-course cross-links that referenced the old `software-engineer/<slug>` path
      and repoint them to `courses/<course-id>` (Root Cause Orientation) — command:
      `npx nx run rhino-cli:links:validation` — acceptance: zero broken links.

### Phase 5 Gate

- [ ] [AI] All existing courses live under `<COURSES>`; `<SE_OLD>` drained; redirects resolve; catalog updated.
- [ ] [AI] `npx nx run ayokoding-www:build` + link + heading validation green.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: every existing course now lives at its canonical `courses/<id>` URL with a redirect
> from its old URL; no manifest exists yet, so all courses render the canonical view. Safe to stop. To
> resume: re-run link validation + `:build`.

---

## Phase 6: Author the fourteen NEW courses + three NEW capstones into the library

> Each NEW course is authored as a full page-bundle into `<COURSES><course-id>/`. Because these
> phases are content-independent (each writes only its own subtree), they **pipeline concurrently**
> through review (bounded by the in-force concurrency cap). Author each per the **NEW-course
> authoring convention** below; per-course concept/example/capstone detail is in the
> [syllabus detail file](./syllabus/README.md) for that course ID and the
> [prd.md spec](./prd.md#new-course--capstone-specifications).

**NEW-course authoring convention** (apply to each course/capstone sub-phase):

1. [AI] **V (accuracy pre-verify)** — spot-check version-pinned / market / pre-1.0-stack facts via
   `web-researcher`; the two `vacti` repos stay unverified (never written as version-pinned facts) —
   acceptance: no version-pinned claim written `[Unverified]`.
2. [AI] **Skeleton** — create `<COURSES><course-id>/` (`_index.md` + `overview.md` +
   `learning/_index.md` + `drilling/_index.md`), mirroring the matching sibling bundle shape —
   acceptance: `test -d` passes for folder + `learning/` + `drilling/`.
3. [AI] **Author learning track** — `overview.md` (purpose + `## Prerequisites` naming only earlier
   library courses + register per prd), concept coverage (≥ floor `co-NN`), example/scenario pages
   (volume band `ex-NN`) + colocated `code/` where code-bearing, and `learning/capstone/` — acceptance:
   `grep -oh 'co-[0-9]\{2\}' … | sort -u | wc -l` ≥ floor; `ex-NN` count in band.
4. [AI] **Author drilling track** — `drilling/<course-id>.md` + `drilling/overview.md` in the fixed
   five-section order — acceptance: all five sections present.
5. [AI] **RED (checkers)** — run the matching learning checker + `apps-ayokoding-www-facts-checker` +
   `apps-ayokoding-www-link-checker` (+ `apps-ayokoding-www-general-checker` on `drilling/overview.md`)
   — acceptance: findings recorded.
6. [AI] **GREEN (fixers)** — resolve every CRITICAL/HIGH/MEDIUM finding via the matching fixer —
   acceptance: every finding addressed.
7. [AI] **REFACTOR** — re-run checkers + `npx nx run ayokoding-www:build` + `npm run lint:md` —
   acceptance: zero CRITICAL/HIGH/MEDIUM remain; build + lint exit 0.

Each course below is its own sub-phase (own branch → draft PR → 3-cycle review → `[AI]` merge →
deploy), applying the convention. Note: the NEW courses are added to the **library**; their position
in each path comes from the manifests (Phases 7 & 9), not from a body weight.

- [ ] [AI] `coding-interview` (By Example · Python) — acceptance: all 7 convention steps complete;
      checker/facts-checker/link-checker report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `take-home-and-live-coding` (By Example · Python) — acceptance: all 7 convention steps complete;
      checker/facts-checker/link-checker report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `system-design-interview` (Annotated-concept · no code) — acceptance: all 7 convention steps complete;
      checker/facts-checker/link-checker report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] `behavioral-and-leadership-interviews` (Annotated-concept · no code) — acceptance: all 7 convention steps complete;
      checker/facts-checker/link-checker report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] `async-python-and-fastapi-services` (By Example · Python) — acceptance: all 7 convention steps complete;
      checker/facts-checker/link-checker report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `self-hosting-essentials` (By Example · ops/config) — acceptance: all 7 convention steps complete;
      checker/facts-checker/link-checker report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `browser-automation-with-cdp` (By Example · Python) — acceptance: all 7 convention steps complete;
      checker/facts-checker/link-checker report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `the-agent-loop` (By Example · Python) — acceptance: all 7 convention steps complete;
      checker/facts-checker/link-checker report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `agent-tools-and-mcp` (By Example · Python) — acceptance: all 7 convention steps complete;
      checker/facts-checker/link-checker report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `agent-context-and-memory` (Annotated-concept · Python) — acceptance: all 7 convention steps complete;
      checker/facts-checker/link-checker report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] `agent-permissions-and-sandboxing` (By Example · Python) — acceptance: all 7 convention steps complete;
      checker/facts-checker/link-checker report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `agent-orchestration-subagents-and-observability` (Annotated-concept · Python) — acceptance: all 7 convention steps complete;
      checker/facts-checker/link-checker report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] `just-enough-cpp` (Primer · C++) — acceptance: all 7 convention steps complete;
      checker/facts-checker/link-checker report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_
- [ ] [AI] `detection-engineering-and-siem-operations` (By Example · XML/rules + Python) — acceptance: all 7 convention steps complete;
      checker/facts-checker/link-checker report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `capstone-interview-loop` (Python + prose) — acceptance: all 7 convention steps complete;
      checker/facts-checker/link-checker report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `capstone-build-your-own-coding-agent` (Python) — acceptance: all 7 convention steps complete;
      checker/facts-checker/link-checker report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `capstone-build-your-own-pentest-engine` (TypeScript) — acceptance: all 7 convention steps complete;
      checker/facts-checker/link-checker report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

### Phase 6 Gate

- [ ] [AI] All 14 NEW courses + 3 NEW capstones live under `<COURSES>`; each passed its checker + facts + link checkers.
- [ ] [AI] `<COURSES>_index.md` catalog updated to include the new courses.
- [ ] [AI] `npx nx run ayokoding-www:build` + link + heading + markdownlint green.
- [ ] [AI] Every NEW-course sub-phase PR is `[AI]`-merged and deployed.

> **Pause Safety**: the library now holds all existing + all new courses at their canonical URLs; no
> manifest published yet, so all render the canonical view. Safe to stop. To resume: re-run the
> section build + link validation.

---

## Phase 7: Author the `job-seeking-software-engineer` manifest + landing + wire + smoothness

> _Suggested executor: `apps-ayokoding-www-general-maker` (manifest/landing) + `web-researcher` (smoothness facts)._

- [ ] [AI] Author the manifest **data file** `<FEAT>manifests/job-seeking-software-engineer.yaml`
      (RESOLVED, OQ-2 — standalone data file, NOT `_index.md` frontmatter): `pathId`, `title`,
      `description`, and the ordered `courseOrder` list = the interview-first arc from
      [tech-docs §Path `job-seeking-software-engineer`](./tech-docs.md#path-job-seeking-software-engineer-interview-first)
      and [syllabus/manifest-job-seeking-software-engineer.md](./syllabus/manifest-job-seeking-software-engineer.md)
      — acceptance: the manifest loads + validates (`npx nx run ayokoding-www:test:integration` exits 0).
- [ ] [AI] Author the thin landing anchor `<PATHS>job-seeking-software-engineer/_index.md` (prose/SEO
      only — no `courseOrder`); the ordered course list renders from the loaded manifest per
      [prd.md Screen 2](./prd.md#screen-2--path-landing-page) — acceptance: landing renders the
      manifest-ordered list (phase-grouped, fast-path callout, interview-loop-map).
- [ ] [AI] **Manifest integrity check** — every `courseOrder` ID resolves under `<COURSES>`; no ID
      appears twice; no forked body — command: `npx nx run ayokoding-www:test:integration` (integrity
      test) — acceptance: exits 0.
- [ ] [AI] Verify path-aware nav end-to-end for this path: from the landing, prev/next walks the
      manifest order and preserves `?path=job-seeking-software-engineer`; breadcrumb shows the path —
      command: `npx nx run ayokoding-www:test:e2e` — acceptance: the path-walk e2e spec passes across locales.
- [ ] [AI] **Progression smoothness audit (interview-first, RD-16)** — walk the manifest order and
      confirm the four levers hold (prereq-chaining with SF-1/SF-2 bridges present in the re-homed
      bodies; monotonic-ish difficulty; skip/fast-path affordances on the landing; refresh register in
      the four interview courses) per
      [tech-docs §Smoothness Architecture](./tech-docs.md#smoothness-architecture-per-path) —
      acceptance: all four levers verified; any regression fixed by soften/bridge in place, never reorder.

### Phase 7 Gate

- [ ] [AI] Job-seeking manifest published; integrity check green; path-walk e2e + breadcrumb green across locales.
- [ ] [AI] Smoothness audit passes (four levers, SF-1/SF-2 bridges, refresh register).
- [ ] [AI] `npx nx run ayokoding-www:build` + `:test:e2e` + `:specs:behavior:coverage` exit 0.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the job-seeking-software-engineer path is **live end-to-end** in production
> (landing + manifest + path-aware nav + smoothness). This is a complete, shippable milestone. Safe to
> stop indefinitely. To resume: re-run the path-walk e2e.

---

## Group C — Software-Engineer path (shipping-first, reuses the library)

## Phase 8: Author the `software-engineer` manifest + landing + smoothness (zero new bodies)

> _Suggested executor: `apps-ayokoding-www-general-maker`._
> Group C starts only after Group B is fully merged (job-seeking path live). It adds **no new course
> body** — Group B already re-homed all ~97 existing courses and authored the 17 NEW courses/capstones
> (OQ-1), so the full 114-course library already exists and Group C only reorders it into the
> shipping-first arc, the strongest proof of the shared-course-library architecture.

- [ ] [AI] Author the manifest **data file** `<FEAT>manifests/software-engineer.yaml` (RESOLVED, OQ-2
      — standalone data file, NOT `_index.md` frontmatter): `pathId: software-engineer`, `title`,
      `description`, and the ordered `courseOrder` = the shipping-first arc from
      [tech-docs §Path `software-engineer`](./tech-docs.md#path-software-engineer-shipping-first) and
      [syllabus/manifest-software-engineer.md](./syllabus/manifest-software-engineer.md) — the arc
      places editor/tooling → one language end-to-end → **build a real app first** ahead of
      CS-fundamentals/DS&A/algorithms/systems depth, and **ends with the optional "ready to job-hunt?"
      bridge tail** (RESOLVED, OQ-3) referencing the four shared interview-technique courses +
      `capstone-interview-loop` by ID — acceptance: body duplication = 0 (references shared course IDs
      only, incl. the bridge tail); manifest loads + validates
      (`npx nx run ayokoding-www:test:integration` exits 0).
- [ ] [AI] Author the thin landing anchor `<PATHS>software-engineer/_index.md` (prose/SEO only — no
      `courseOrder`); the ordered course list + the optional job-hunt bridge section render from the
      loaded manifest — acceptance: landing renders the manifest-ordered arc with the bridge tail
      visibly marked optional.
- [ ] [AI] Update `<PATHS>_index.md` (paths hub) so both path cards are present per
      [prd.md Screen 1](./prd.md#screen-1--paths-hub-choose-your-path) — acceptance: hub shows both paths.
- [ ] [AI] **Manifest integrity + no-forked-body check** — every `courseOrder` ID resolves; no dup ID;
      no body duplicated between the two manifests (both reference by ID) — command:
      `npx nx run ayokoding-www:test:integration` — acceptance: exits 0.
- [ ] [AI] Verify path-aware nav for the software-engineer path: prev/next walks the shipping-first
      order and preserves `?path=software-engineer`; a course in **both** paths shows the correct
      neighbor per active path — command: `npx nx run ayokoding-www:test:e2e` — acceptance: e2e passes
      across locales; a shared course's prev/next differs by active path.
- [ ] [AI] **Optional job-hunt bridge check (RESOLVED, OQ-3)** — confirm the software-engineer manifest
      ends with the optional "ready to job-hunt?" bridge tail referencing the four interview-technique
      courses + `capstone-interview-loop` **by ID** (the same shared bodies job-seeking uses, zero new
      bodies); the landing renders the tail visibly marked optional and links carry
      `?path=software-engineer` — acceptance: bridge tail present in the data file; no new course body
      created for the bridge; e2e walks into the bridge courses.
- [ ] [AI] **Progression smoothness audit (shipping-first, RD-16)** — confirm the arc reads smoothly
      for the "productive fast" persona: build-a-real-app precedes CS depth; the Stage-2→Stage-3 bridge
      ("you shipped; now understand why") is present on the landing; prereq-chaining holds in this
      order — acceptance: four levers verified; regressions fixed by soften/bridge, never reorder.

### Phase 8 Gate

- [ ] [AI] Software-engineer manifest published (shipping-first, zero duplicated bodies); paths hub shows both paths.
- [ ] [AI] Optional job-hunt bridge tail present in the manifest (interview courses by ID, zero new bodies).
- [ ] [AI] Integrity + no-forked-body checks green; per-path prev/next differs correctly for shared courses.
- [ ] [AI] Shipping-first smoothness audit passes.
- [ ] [AI] `npx nx run ayokoding-www:build` + `:test:e2e` + `:specs:behavior:coverage` exit 0.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: both paths are live over one shared library with zero body duplication. The full
> two-path product is complete. Safe to stop. To resume: re-run both path-walk e2e specs.

---

## Group Finalization

## Phase 9: Section & App Verification

- [ ] [AI] Run affected quality gates from the worktree:
      `npx nx affected -t typecheck lint test:quick test:unit test:integration test:e2e specs:behavior:coverage`
      — acceptance: exits 0. Fix ALL failures, including preexisting ones (Root Cause Orientation),
      committing preexisting fixes separately.
- [ ] [AI] Build the site: `npx nx run ayokoding-www:build` — acceptance: exits 0.
- [ ] [AI] Run link + heading-hierarchy + markdown validation:
      `npx nx run rhino-cli:links:validation` + `npx nx run rhino-cli:headings:hierarchy-validation` +
      `npm run lint:md` — acceptance: all green.
- [ ] [AI] **Manifest-integrity sweep** — both manifests: every `courseOrder` ID resolves; no dup ID;
      no forked body across paths — acceptance: integrity script reports zero violations.
- [ ] [AI] **Both-path smoothness re-check (RD-16)** — re-verify the four levers for each manifest in
      the landed content — acceptance: both paths pass.

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes
> (Root Cause Orientation). Commit preexisting fixes separately with conventional-commit messages.

### Phase 9 Gate

- [ ] [AI] Affected `typecheck/lint/test:quick/test:unit/test:integration/test:e2e/specs:behavior:coverage` exit 0.
- [ ] [AI] Build + link + heading + markdown validation green; manifest integrity + both-path smoothness pass.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the whole two-path product passes all automated gates. Safe to stop. To resume:
> re-run the affected quality gates + build.

---

## Phase 10: Manual UI Verification + Rule-15 Three-Tester Retest

> Path-aware navigation is a user-facing change, so a live-site retest is required before archival.
> Discover the app's supported locales and retest each.

- [ ] [AI] Discover supported locales: read `apps/ayokoding-www/next.config.ts` / `src/features/i18n/`
      — acceptance: locale set recorded (e.g. `en`, `id`).
- [ ] [AI] Start dev server: `npx nx dev ayokoding-www` — acceptance: server up.
- [ ] [AI] For EACH locale × breakpoints (375 / 768 / 1280 px), via Playwright MCP: open the paths hub,
      each path landing, walk 2–3 courses via prev/next (confirm `?path=` persists + order + breadcrumb),
      deep-link a course without `?path=` (canonical view + "part of paths" affordance), hit an invalid
      `?path=` (canonical view), and an old `software-engineer/<slug>` URL (redirect). Verify `html[lang]`
      per locale and `browser_console_messages` is clean — acceptance: all behaviors correct; zero console errors.
- [ ] [AI] Capture one screenshot per screen per locale × breakpoint to
      `evidence/phase-10-<screen>-<locale>-<breakpoint>px.png` — acceptance: files exist in `evidence/`.
- [ ] [AI] Run the three live-site testers (the `web-ux-test-fixing-planning` workflow:
      `web-exploratory-tester` + `web-usability-tester` + `web-design-tester`) against the running
      paths hub, both path landings, and sample courses across all locales — acceptance: EWT/UWT/DWT
      findings + spec-gaps recorded.
- [ ] [AI] Append each finding below as a new unchecked checkbox, source-attributed
      (`- [ ] EWT-NNN:` / `- [ ] UWT-NNN:` / `- [ ] DWT-NNN: <defect> — fix before archival`); append
      any SG-###/USS-### items to the relevant spec/content step.

### Rule-15 retest follow-ups

- [ ] [AI] _(populated during the retest — every EWT/UWT/DWT defect finding must be fixed/ticked before
      archival; deferral of a defect requires explicit user permission and only when genuinely
      impossible; SG-###/USS-### may be triaged or deferred with rationale)_

### Phase 10 Gate

- [ ] [AI] All three screens verified across all locales × breakpoints; screenshots in `evidence/`; console clean.
- [ ] [AI] All rule-15 EWT/UWT/DWT defect findings fixed (ticked) or explicitly permitted to defer.
- [ ] [AI] Draft PR opened (retest evidence + any fixes); 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the two-path UI is verified live and defect-clean across locales. Safe to stop. To
> resume: re-run the three testers against the running app.

---

## Phase 11: Final `origin/main` Integration & CI Verification

- [ ] [AI] Confirm no plan PR is still open: every prior phase branch has been `[AI]`-merged to `main`
      (`gh pr list --search "fundamentally-strong-shared-course-tracks" --state open` returns zero) —
      acceptance: no open plan PRs remain.
- [ ] [AI] Sync the shared worktree to latest `origin/main` and run the full affected suite:
      `npx nx affected -t typecheck lint test:quick test:unit test:integration test:e2e specs:behavior:coverage` + `npx nx run ayokoding-www:build` — acceptance: all exit 0 on the integrated `main`.
- [ ] [AI] Monitor the final `main` CI run (poll every ~2 min; one `gh run view --json
status,conclusion` per wakeup; never `gh run watch`) — acceptance: all GitHub Actions green; fix root
      causes and push follow-ups (own PR → review → `[AI]` merge) until green.
- [ ] [AI] Confirm `prod-ayokoding-www` serves both paths + the re-homed library; re-dispatch
      `apps-ayokoding-www-deployer` if any earlier deploy lagged — acceptance: production serves the
      two-path product.

### Phase 11 Gate

- [ ] [AI] Zero open plan PRs; every prior phase merged to `main`.
- [ ] [AI] Full affected suite + build green on integrated `main`; final `main` CI run green.
- [ ] [AI] `prod-ayokoding-www` serving both paths + library.

> **Pause Safety**: the whole plan is integrated on `main`, green in CI, and live in production. Safe
> to stop. To resume: re-run the affected suite on `main` and check CI/prod status.

---

## Phase 12: Knowledge Capture

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

### Phase 12 Gate

- [ ] [AI] Every `learnings.md` entry is terminal (routed inline / filed as backlog / discarded) or the "none" escape is present.
- [ ] [AI] No code-homed learning landed inline in this plan's own commits/PR.
- [ ] [AI] Draft PR opened (`learnings.md` triage); 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed (no-op).

> **Pause Safety**: `learnings.md` is fully triaged; nothing depends on querying it later. Safe to
> stop. To resume: re-read `learnings.md` and confirm every entry is terminal.

---

## Phase 13: Plan Archival

- [ ] [AI] Verify ALL delivery checklist items are ticked.
- [ ] [AI] Verify the Knowledge Capture phase is complete (every entry terminal or explicit "none" escape; both safety gates applied).
- [ ] [AI] Verify ALL quality gates pass (local + CI) and the build is green.
- [ ] [AI] Verify ALL manual assertions pass (Playwright MCP) with committed evidence in `evidence/`; all supported locales exercised.
- [ ] [AI] Verify every rule-15 EWT/UWT/DWT defect finding is fixed (ticked) — deferral requires explicit user permission (only when genuinely impossible); SG-###/USS-### may be triaged/deferred.
- [ ] [AI] Verify both path manifests are published, both landings live, and the paths hub shows both paths; every prior-phase PR `[AI]`-merged and deployed (Phase 11 checkpoint green).
- [ ] [AI] Move: `git mv plans/in-progress/fundamentally-strong-shared-course-tracks/
plans/done/YYYY-MM-DD__fundamentally-strong-shared-course-tracks/` using today's completion date (the
      `evidence/` subfolder moves with it).
- [ ] [AI] Update `plans/in-progress/README.md` — remove the plan entry.
- [ ] [AI] Update `plans/done/README.md` — add the plan entry with completion date.
- [ ] [AI] Update any other READMEs that reference this plan (e.g. `plans/README.md`, `plans/backlog/README.md`).
- [ ] [AI] Commit the archival: `chore(plans): move fundamentally-strong-shared-course-tracks to done`.

### Phase 13 Gate

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

### Note: this plan does not start in `in-progress/`

The `git mv` in Phase 13 assumes the plan was promoted from `backlog/` to `in-progress/` (stripping
the date prefix) when work began, per the plan lifecycle. If still in `backlog/` at archival time,
adjust the source path accordingly.
