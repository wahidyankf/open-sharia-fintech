# Delivery Checklist — Learning Path Manifests (software-engineer-role)

> **Programme decisions** — the `R*`/`A*` ids cited below are defined in
> [tech-docs §Programme decisions](./tech-docs.md#programme-decisions).
>
> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it. `[AI+HUMAN]`: agent prepares, human approves or finishes.
> Git-mechanical steps (worktree create/remove, branch, push, merge) are `[AI]`.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` plus a `> **Pause Safety**:` note. Only
> Phase 10 integrates the delivery unit; all earlier phases remain local to `final-delivery`.
>
> **Cross-plan source of truth**: `plans/done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/`.
> Do not copy; do not author from any other source.
>
> **The manifest ownership invariant (binding)**: this plan owns exactly the three manifest files named
> in [tech-docs §What this plan writes](./tech-docs.md#what-this-plan-writes) and every step that
> mutates or re-verifies one of them. The sibling plan
> `ayokoding-learning-path-13-careers-ai-manifest` owns exactly its one `ai-engineer.yaml` file. Neither
> plan edits the other's manifest. The seven course-authoring successor plans own course **bodies
> only**.

## One-PR delivery contract (binding, 2026-08-01)

This three-manifest plan is one inseparable delivery unit: every Phase 1–10 change lands in **one
worktree, one branch, and exactly one draft PR**. Manifests may still be authored, checked, and
committed in their dependency order, but no intermediate phase may push, open a PR, run the PR
review cycle, merge, deploy, or record a merge SHA. Only Phase 10 opens the draft PR, after all
manifest work, verification, and Knowledge Capture are green; it includes the archival move to
`plans/done/`, then runs the PR-Review Maker→Fixer Cycle, CI verification, ready-for-review
transition, and the normal `[AI]` merge/deploy protocol. The former intermediate Plan 12→13
handoff is removed: Plan 13 delivers its independent manifest first, then this plan consumes that
merged state for its four-manifest validation before Phase 10. This contract supersedes every older
manifest-unit or delivery-boundary PR reference below.

The `worktrees/ayokoding-learning-path-12-careers-se-manifests/` path below is this plan's only
worktree; no per-manifest, phase, or closeout worktree is created.

## Worktree

Worktree path: `worktrees/ayokoding-learning-path-12-careers-se-manifests/`

This path is the one and only worktree for the entire plan. Provision it once from current
`origin/main`, create the persistent `final-delivery` branch after Phase 0, and use neither
per-course/cohort/stage worktrees nor per-phase branches. Remove it only after the final PR merges.

## Delivery Mode: worktree-to-pr

This plan has one delivery unit: all change-producing work is committed on the persistent
`final-delivery` branch in the declared worktree. Phases before 10 must not push, open
a PR, run PR review, merge, deploy, or record an in-repository merge SHA. Phase 10 first
commits the archival move and index updates, then opens the sole draft PR, runs the three-cycle
PR-Review Maker→Fixer Cycle plus local and CI gates, marks it ready, merges under the hardened
preconditions, and deploys once.

## Depends-on and start preconditions

| Direction   | Plan                                                                                                                                                  |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `blockedBy` | `ayokoding-learning-path-03-navigation-ui` (done)                                                                                                     |
| `blockedBy` | `ayokoding-learning-path-01-url-restructure` (done, transitive)                                                                                       |
| `blockedBy` | `ayokoding-learning-path-02-schema-and-prerequisite-dag` (done, transitive)                                                                           |
| `blockedBy` | `vercel-function-cost-reduction` (`ayokoding-www` unit merged)                                                                                        |
| `blockedBy` | seven course-authoring successor plans, per phase (see [Phase 4](#phase-4-manifest-growth-as-backfill-lands))                                         |
| `blockedBy` | `ayokoding-learning-path-13-careers-ai-manifest`, **whole-plan**, for **Phase 8 only**                                                                |
| `blocks`    | no direct start edge to `ayokoding-learning-path-13-careers-ai-manifest`; Plan 13 delivers first, then this plan consumes its merged state in Phase 8 |

See [README §Depends-on](./README.md#depends-on) for the full table including the disjoint-subtree
confirmation against the `skills/` split plans.

## Parallelization Model

**Cap**: honor the in-force subagent/PR-review concurrency cap.

- **Phases 1 → 3 are strictly serial**, in DD-27's locked order.
- **Phase 4 is serial per source-plan signal** — each of the six-or-seven contributing source plans is
  its own sync point (append + re-run integrity + prerequisite-consistency + no-forked-body).
- **Phases 5 → 10 are serial.**
- **This plan's own phases have DAG width 1** — every phase mutates or re-verifies the same three data
  files (plus, at Phase 8, reads the sibling's fourth). Plan 13's independent final delivery must
  merge before Phase 8; this avoids a partial-PR handoff and keeps the four-manifest check coherent.

### Delivery Boundaries

| Phase(s) | Delivery unit                                               | Worktree / branch                                                         | PR opens                           |
| -------- | ----------------------------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------- |
| 0        | Setup and baseline                                          | No delivery worktree or PR                                                | no                                 |
| 1–9      | Intermediate authoring, verification, and Knowledge Capture | This plan's single declared worktree and persistent final-delivery branch | no — commit only                   |
| 10       | Final archival and integration                              | The same worktree and branch; archive before opening the PR               | yes — exactly once, after archival |

No phase may create an additional worktree or branch. The final phase is the only delivery boundary.

## Path constants

- `<COURSES>` = `apps/ayokoding-www/content/en/learn/courses/`
- `<PATHS>` = `apps/ayokoding-www/content/en/learn/paths/`
- `<FEAT>` = `apps/ayokoding-www/src/features/course-paths/`
- `<MANIFESTS>` = `<FEAT>manifests/`
- `<SPECS>` = `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/course-paths/`
- This plan's path ids: `careers/interview-ready/software-engineer`,
  `careers/immediately-effective/software-engineer`, `careers/fundamentally-strong/software-engineer`.
- Sibling's path id (read-only reference at Phase 8 only): `careers/immediately-effective/ai-engineer`.
- Band-9 IDs: `coding-interview`, `take-home-and-live-coding`, `system-design-interview`,
  `behavioral-and-leadership-interviews`, `capstone-interview-loop`.

One additional constant this plan owns: `<MANIFESTS>careers/careers-se-manifests.unit.test.ts` — the
unit-test file covering this plan's three manifests. It is **not** shared with the sibling plan, which
owns its own `<MANIFESTS>careers/careers-ai-manifest.unit.test.ts`.

---

## Phase 0: Environment Setup and Baseline

> _Executor: `repo-setup-manager`_

- [ ] [AI] Enter/provision the worktree and install dependencies: `npm install` — acceptance: exits 0.
- [ ] [AI] Converge the toolchain: `npm run doctor -- --fix` — acceptance: exits 0.
- [ ] [AI] **Precondition 1** — confirm navigation-ui is merged:
      `gh pr list --search "ayokoding-learning-path-03-navigation-ui" --state merged --json number --jq 'length'`
      — acceptance: returns a value ≥ 1.
- [ ] [AI] **Precondition 2** — confirm the `vercel-function-cost-reduction` `ayokoding-www` unit is
      merged:
      `gh pr list --search "vercel-function-cost-reduction" --state merged --json number --jq 'length'`
      — acceptance: returns a value ≥ 1. Falsifiable both ways: returns `0` while that unit is still
      open.
- [ ] [AI] **Precondition 3** — confirm the manifest repository and directory exist:
      `test -f <FEAT>shell/manifest-repository.ts && test -d <MANIFESTS>` — acceptance: exits 0.
- [ ] [AI] **Precondition 4** — confirm the re-homed 33 topics + 4 capstones this plan's Phase 1 needs
      already resolve: `find <COURSES> -maxdepth 1 -mindepth 1 -type d | wc -l` — acceptance: returns
      **≥ 37** (the growth phase later brings this to the full catalog; Phase 1 needs only the
      already-live re-homed set, not the full 127).
- [ ] [AI] Establish baselines: `npx nx run ayokoding-www:build`, `:test:unit`,
      `ayokoding-www-fe-e2e:test:e2e` — acceptance: all exit 0; record pass counts in
      `evidence/phase-0-snapshot.txt`.
- [ ] [AI] **Manifest baseline snapshot** —
      `find <MANIFESTS>careers/interview-ready <MANIFESTS>careers/immediately-effective/software-engineer.yaml <MANIFESTS>careers/fundamentally-strong 2>/dev/null`
      recorded to `evidence/phase-0-snapshot.txt` — acceptance: prints nothing (none of this plan's
      three files exists yet).
- [ ] [AI] **Hub baseline snapshot** — record this plan's own three intended hrefs' absence:
      `grep -cF '/en/learn/paths/careers/interview-ready/software-engineer' <PATHS>_index.md` (and the
      other two hrefs) each recorded to `evidence/phase-0-snapshot.txt` — acceptance: each returns
      **0**.
- [ ] [AI] Resolve every preexisting failure before proceeding.
- [ ] [AI] Confirm `learnings.md` scaffold exists.

### Phase 0 Gate

- [ ] [AI] `npm install` and `npm run doctor -- --fix` exit 0.
- [ ] [AI] Preconditions 1-4 all hold.
- [ ] [AI] Baselines recorded green; zero preexisting failures unresolved.
- [ ] [AI] This plan's three manifest paths recorded absent; the three intended hrefs recorded absent.
- [ ] [AI] **No PR opened, nothing pushed** —
      `git ls-remote --heads origin "$(git branch --show-current)" | grep -c .` returns **0**, and
      `gh pr list --head "$(git branch --show-current)" --json number --jq 'length'` returns **0**.

> **Pause Safety**: only the toolchain was verified and the current state snapshotted. Safe to stop
> indefinitely. To resume: re-run the four precondition checks and the baselines.

---

## Phase 1: Author the interview-ready manifest, landing, and smoothness audit

> _Suggested executor: `apps-ayokoding-www-general-maker` + `web-researcher`._
>
> The **architecture smoke test** (DD-27). Ships against the 33 re-homed topics + 4 existing capstones.
> The four interview-technique courses + `capstone-interview-loop` are **deliberately deferred** to
> [Phase 4.2](#42--band-9-growth-two-of-three). Plan 13 has no start dependency on this phase: its
> manifest occupies a disjoint file subtree and delivers independently before this plan's Phase 8
> four-manifest validation.

### 1.1 · TDD cycle — publish the manifest data file

- [ ] [AI] **RED** — create `<MANIFESTS>careers/careers-se-manifests.unit.test.ts` _(new file)_ with a
      failing assertion that `<MANIFESTS>careers/interview-ready/software-engineer.yaml` loads,
      zod-validates, and passes `checkManifestIntegrity` + `checkPrerequisiteConsistency` — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: fails with a module-not-found/empty-glob
      error. Also create `<SPECS>path-composition.feature` _(new file)_ with the scenario below, and a
      matching failing step in `apps/ayokoding-www-fe-e2e/src/steps/path-composition.steps.ts` _(new
      file)_ — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: fails.

  **Gherkin (binds) →** "The interview-ready MVP proves the architecture"

  ```gherkin
  Scenario: The interview-ready MVP proves the architecture
    Given the careers/interview-ready/software-engineer MVP (an architecture smoke test over already-live topics 1-33) is delivered end-to-end
    When its delivery unit is merged to origin/main
    Then the interview-ready MVP's landing page, manifest, and path-aware nav are verified on final-delivery
    And Plan 13 remains independent until this plan's Phase 8 consumes Plan 13's final merged delivery
  ```

- [ ] [AI] **GREEN** — author `<MANIFESTS>careers/interview-ready/software-engineer.yaml` _(new file)_
      with `pathId: careers/interview-ready/software-engineer`, a `title`, a `description`, and
      `courseOrder` transcribed from
      [`manifest-interview-ready-software-engineer.md`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/paths/manifest-interview-ready-software-engineer.md),
      restricted to the 33 re-homed topics + 4 existing capstones — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: exits 0, AND
      `grep -oE 'coding-interview|take-home-and-live-coding|system-design-interview|behavioral-and-leadership-interviews|capstone-interview-loop' <MANIFESTS>careers/interview-ready/software-engineer.yaml | sort -u | wc -l`
      returns **0**. Falsifiable both ways: after Phase 4.2 the same command must return **5**.
- [ ] [AI] **REFACTOR** — align YAML key order with the schema plan's example; factor a shared
      load-and-validate helper in the test file — command:
      `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:lint` — acceptance: both exit 0.
- [ ] [AI] **Fix stale ownership doc** — this is the first step in either this plan or the sibling
      `ayokoding-learning-path-13-careers-ai-manifest` that writes under `<MANIFESTS>careers/`, so
      correct the pre-existing stale ownership paragraph here. Edit
      `apps/ayokoding-www/src/features/course-paths/manifests/README.md`: replace "Ownership is split
      per category, not directory-wide: `ayokoding-learning-path-05-manifests` owns every `.yaml`
      under `careers/`; `ayokoding-learning-path-06-skills-accounting` and
      `ayokoding-learning-path-07-skills-erp` together own the sibling `skills/` subtree. See
      `ayokoding-learning-path-05-manifests`'s own README for the full, authoritative ruling." with
      wording naming `ayokoding-learning-path-12-careers-se-manifests` +
      `ayokoding-learning-path-13-careers-ai-manifest` as the joint owners of `careers/`, and
      `ayokoding-learning-path-14` through `ayokoding-learning-path-18` (per this plan's own
      Depends-on table) as the owners of the sibling `skills/` subtree — acceptance:
      `grep -cE 'ayokoding-learning-path-(05-manifests|06-skills-accounting|07-skills-erp)' apps/ayokoding-www/src/features/course-paths/manifests/README.md`
      returns **0**, AND
      `grep -cF 'ayokoding-learning-path-12-careers-se-manifests' apps/ayokoding-www/src/features/course-paths/manifests/README.md`
      returns **1** or more.

### 1.2 · The landing anchor (content — maker/checker/fixer)

- [ ] [AI] Author `<PATHS>careers/interview-ready/software-engineer/_index.md` _(new file)_ — prose and
      SEO only: the arc narrative, the "experienced and job-hunting? start at Phase 1" fast-path
      affordance — acceptance:
      `grep -cF 'courseOrder' <PATHS>careers/interview-ready/software-engineer/_index.md` returns **0**.
- [ ] [AI] Run `apps-ayokoding-www-link-checker` + `apps-ayokoding-www-general-checker`; apply the
      matching fixer to every CRITICAL/HIGH/MEDIUM finding — acceptance: zero remain on re-run.
- [ ] [AI] **A8 clean-room licensing self-check** — confirm no sentence, heading, or ordered list was
      lifted or closely paraphrased from a third-party curriculum, per `A8` — acceptance: this
      checklist records the sources consulted and an explicit originality statement.
- [ ] [AI] Populate this plan's **first** paths-hub card in `<PATHS>_index.md` — acceptance:
      `grep -cF '/en/learn/paths/careers/interview-ready/software-engineer' <PATHS>_index.md` returns
      **1**.

### 1.3 · Architecture smoke test and smoothness audit

- [ ] [AI] **Architecture smoke test** — routing resolves, the manifest loads, `?path=` context
      propagates, prev/next walks the order, breadcrumb shows the path, course pages show
      prerequisites — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: passes in `en`.
- [ ] [AI] **Progression smoothness audit (smoke-test-scoped)** — prereq-chaining, monotonic-ish
      difficulty, skip/fast-path affordance verified per
      [tech-docs's smoothness levers, inherited from DD-16](./tech-docs.md#design-decisions) —
      acceptance: every assessable lever verified. The **refresh-register** lever is not yet assessable
      (lives inside the four deferred interview courses) — record the deferral, closed at Phase 4.3.

### Phase 1 Gate

- [ ] [AI] `find <MANIFESTS>careers/interview-ready -name '*.yaml' | wc -l` returns **1**.
- [ ] [AI] `npx nx run ayokoding-www:test:unit` exits 0.
- [ ] [AI] The five-ID deferral grep returns **0**.
- [ ] [AI] `npx nx run ayokoding-www:build` + `:specs:behavior:coverage` +
      `ayokoding-www-fe-e2e:test:e2e` exit 0.
- [ ] [AI] Hub-card href check returns **1**.
- [ ] [AI] Smoothness audit passes for every assessable lever; the refresh-register deferral is
      recorded.
- [ ] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance:
      no PR, merge, or deployment occurs before Phase 10.

> **Pause Safety**: `interview-ready` is verified end-to-end on `final-delivery`; it is not yet a
> sibling-plan precondition. Safe to stop indefinitely. To resume:
> `npx nx run ayokoding-www-fe-e2e:test:e2e`.

---

## Phase 2: Author the immediately-effective manifest, landing, and smoothness audit

> Adds **no new course body**. Composed over the currently-landed library; grown through Phase 4's
> six-source-plan sub-phases — but **never** through Band 9 (DD-41).

### 2.1 · TDD cycle — publish the manifest data file

- [ ] [AI] **RED** — extend `<MANIFESTS>careers/careers-se-manifests.unit.test.ts` with a failing
      assertion that `<MANIFESTS>careers/immediately-effective/software-engineer.yaml` loads,
      zod-validates, passes both integrity gates, and places the build-a-real-app capstone before every
      pure-theory course — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails; Phase 1's
      assertions still pass. Extend `<SPECS>path-composition.feature` and the matching e2e step with
      the scenario below — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: fails.

  **Gherkin (binds) →** "The immediately-effective path is build-app-first"

  ```gherkin
  Scenario: The immediately-effective path is build-app-first
    Given the careers/immediately-effective/software-engineer path manifest is published
    When a reader walks the path
    Then editor/tooling, one language end-to-end, and building a real app precede the CS-fundamentals and DS&A courses
    And the reader ships a real deployed app before any pure-theory course
  ```

- [ ] [AI] **GREEN** — author `<MANIFESTS>careers/immediately-effective/software-engineer.yaml` _(new
      file)_ with `courseOrder` transcribed from
      [`manifest-immediately-effective-software-engineer.md`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/paths/manifest-immediately-effective-software-engineer.md),
      restricted to the mirror's main body (114 courses), **excluding** the five Band-9 IDs — this
      manifest **never** receives them (DD-41), unlike `interview-ready` and `fundamentally-strong` —
      command: `npx nx run ayokoding-www:test:unit` — acceptance: exits 0, AND
      `awk '/^courseOrder:/{f=1;next} f&&/^ *- /{n++; if ($2=="capstone-full-stack-app") print "app@"n; if ($2=="computer-science-foundations") print "theory@"n}' <MANIFESTS>careers/immediately-effective/software-engineer.yaml`
      prints `app@` before `theory@`, AND the five-ID grep returns **0** — permanently, per DD-41, not
      only until Phase 4.
- [ ] [AI] **REFACTOR** — deduplicate the load-and-validate helper now that two manifests share it —
      command: `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:lint` — acceptance: both
      exit 0.

### 2.2 · The landing anchor and hub card

- [ ] [AI] Author `<PATHS>careers/immediately-effective/software-engineer/_index.md` _(new file)_ —
      including the "already know a language? jump to Build A Real App" fast-path and the
      shipping→CS-depth bridge — acceptance: no `courseOrder` key.
- [ ] [AI] Run link + general checkers; apply matching fixer to CRITICAL/HIGH/MEDIUM — acceptance: zero
      remain.
- [ ] [AI] **A8 clean-room licensing self-check** — acceptance: sources and originality statement
      recorded.
- [ ] [AI] Populate the **second** hub card — acceptance:
      `grep -cF '/en/learn/paths/careers/immediately-effective/software-engineer' <PATHS>_index.md`
      returns **1** (this href specifically — not a whole-file count, since the sibling plan may have
      already added its own `ai-engineer` card to the same shared file by this point).

### 2.3 · Verification and smoothness

- [ ] [AI] Verify path-aware nav; a course shared with `interview-ready` shows the correct neighbour
      **per active path** — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: passes.
- [ ] [AI] **Re-verify all manifests published so far** — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: exits 0.
- [ ] [AI] **Progression smoothness audit (shipping-first)** — acceptance: levers verified; any
      regression fixed by softening/bridging in place, never reordering.

### Phase 2 Gate

- [ ] [AI] `find <MANIFESTS>careers/immediately-effective -name '*.yaml' | wc -l` returns **1**.
- [ ] [AI] The build-before-theory ordering check prints `app@` before `theory@`.
- [ ] [AI] `npx nx run ayokoding-www:test:unit` exits 0 across both published manifests.
- [ ] [AI] The five-ID grep against `immediately-effective/software-engineer.yaml` returns **0**.
- [ ] [AI] `npx nx run ayokoding-www:build` + `:specs:behavior:coverage` +
      `ayokoding-www-fe-e2e:test:e2e` exit 0.
- [ ] [AI] The second hub-card href returns **1**.

- [ ] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance:
      no PR, merge, or deployment occurs before Phase 10.

> **Pause Safety**: two of this plan's three paths are verified on `final-delivery` over one shared library. Safe to stop
> indefinitely. To resume: re-run both path-walk e2e specs.

---

## Phase 3: Author the fundamentally-strong manifest, landing, and smoothness audit

> The university-style path. Adds **no new course body**. **This is the first point at which all three
> software-engineer manifests exist**, so the no-forked-body scenario is anchored here.

### 3.1 · TDD cycle A — publish the manifest data file

- [ ] [AI] **RED** — extend the test file with a failing assertion that
      `<MANIFESTS>careers/fundamentally-strong/software-engineer.yaml` loads, zod-validates, and places
      CS foundations/architecture/paradigms/DS&A before build-real-software courses — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: fails; prior assertions still pass. Extend the
      spec/step files with the scenario below — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` —
      acceptance: fails.

  **Gherkin (binds) →** "The fundamentally-strong path is fundamentals-first"

  ```gherkin
  Scenario: The fundamentally-strong path is fundamentals-first
    Given the careers/fundamentally-strong/software-engineer path manifest is published
    When a reader walks the path
    Then CS foundations, computer architecture, paradigms, and DS&A precede the build-real-software courses
    And the ordering is a valid topological entry into the prerequisite DAG
  ```

- [ ] [AI] **GREEN** — author `<MANIFESTS>careers/fundamentally-strong/software-engineer.yaml` _(new
      file)_ from
      [`manifest-fundamentally-strong-software-engineer.md`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/paths/manifest-fundamentally-strong-software-engineer.md),
      restricted to the main body (116 courses), excluding the five Band-9 IDs (deferred to
      [Phase 4.2](#42--band-9-growth-two-of-three)) — command: `npx nx run ayokoding-www:test:unit` —
      acceptance: exits 0, AND the theory-first check prints `theory@` before `app@` — the exact
      inverse of Phase 2's check — AND the five-ID grep returns **0**. Falsifiable both ways: after
      Phase 4.2 the grep must return **5** here (unlike `immediately-effective`, which stays at 0
      permanently).
- [ ] [AI] **REFACTOR** — assert the two orderings (this and Phase 2's) are inverses in a shared helper
      — command: `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:lint` — acceptance:
      both exit 0.

### 3.2 · TDD cycle B — no forked body across the three software-engineer paths

- [ ] [AI] **RED** — add the shared-course scenario and a failing assertion that every course ID
      appearing in more than one of this plan's three manifests resolves to exactly one directory
      under `<COURSES>` — command: `npx nx run ayokoding-www:test:unit` — acceptance: fails before the
      check is implemented.

  **Gherkin (binds) →** "The three software-engineer paths reference a shared course with no body
  duplication"

  ```gherkin
  Scenario: The three software-engineer paths reference a shared course with no body duplication
    Given a course appears in all three of the interview-ready, immediately-effective/software-engineer, and fundamentally-strong/software-engineer manifests
    When the course library is inspected
    Then exactly one canonical path-neutral body exists for that course
    And each manifest references the course by its stable course ID
  ```

- [ ] [AI] **GREEN** — implement the check — command: `npx nx run ayokoding-www:test:unit` —
      acceptance: exits 0, AND the shell equivalent
      `for id in $(cat <MANIFESTS>careers/interview-ready/software-engineer.yaml <MANIFESTS>careers/immediately-effective/software-engineer.yaml <MANIFESTS>careers/fundamentally-strong/software-engineer.yaml | grep -oE '^ *- [a-z0-9-]+' | sed 's/^ *- //' | sort -u); do find <COURSES> -maxdepth 1 -mindepth 1 -type d -name "$id" | wc -l; done | sort -u`
      prints exactly `1`.
- [ ] [AI] **REFACTOR** — move the shell equivalent into the test as a documented comment — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: exits 0.

### 3.3 · Landing, hub card, verification, and smoothness

- [ ] [AI] Author `<PATHS>careers/fundamentally-strong/software-engineer/_index.md` _(new file)_ —
      including "have a CS degree? skim Stage 2" and the theory→application bridge — acceptance: no
      `courseOrder` key.
- [ ] [AI] Run link + general checkers; apply matching fixer — acceptance: zero CRITICAL/HIGH/MEDIUM
      remain.
- [ ] [AI] **A8 clean-room licensing self-check** — acceptance: sources and originality statement
      recorded.
- [ ] [AI] Populate the **third** hub card — acceptance:
      `grep -cF '/en/learn/paths/careers/fundamentally-strong/software-engineer' <PATHS>_index.md`
      returns **1**.
- [ ] [AI] Verify path-aware nav; a shared course shows the correct neighbour per active path —
      command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: passes.
- [ ] [AI] **Progression smoothness audit (fundamentals-first)** — acceptance: levers verified;
      regressions fixed by softening/bridging in place, never reordering.

### Phase 3 Gate

- [ ] [AI] `find <MANIFESTS>careers/interview-ready <MANIFESTS>careers/immediately-effective/software-engineer.yaml <MANIFESTS>careers/fundamentally-strong -name '*.yaml' | wc -l`
      returns **3** — all three of this plan's manifests published.
- [ ] [AI] The theory-first check prints `theory@` before `app@`; Phase 2's inverse still prints `app@`
      before `theory@`.
- [ ] [AI] The no-forked-body shell check prints exactly `1`.
- [ ] [AI] `npx nx run ayokoding-www:test:unit` exits 0 across all three manifests.
- [ ] [AI] The five-ID grep against `fundamentally-strong/software-engineer.yaml` returns **0**.
- [ ] [AI] `npx nx run ayokoding-www:build` + `:specs:behavior:coverage` +
      `ayokoding-www-fe-e2e:test:e2e` exit 0.
- [ ] [AI] The third hub-card href returns **1**.

- [ ] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance:
      no PR, merge, or deployment occurs before Phase 10.

> **Pause Safety**: all three of this plan's manifests are verified on `final-delivery` over one shared library with zero body
> duplication among them. Safe to stop indefinitely. To resume: re-run all three path-walk e2e specs.

---

## Phase 4: Manifest growth as backfill lands

> **Trigger**: each source plan's own band-completion signal, recorded in that plan's own
> `delivery.md`, naming every manifest that must grow. Processed **as each arrives** — one sub-phase
> per source plan — per [tech-docs §Growth signal routing](./tech-docs.md#growth-signal-routing-from-the-seven-course-authoring-successor-plans).

### 4.1 · Bands 1-8-equivalent growth (six source plans, all three manifests)

- [ ] [AI] On `ayokoding-learning-path-04-course-authoring`'s Bands 1-2 signal landing, append the
      newly-available course IDs into all three of this plan's manifests at each path's correct
      topological position, then re-run integrity + prerequisite-consistency + no-forked-body —
      command: `npx nx run ayokoding-www:test:unit` — acceptance: exits 0.
- [ ] [AI] On [`ayokoding-learning-path-05-course-authoring-platform-and-concurrency`](../../done/2026-08-04__ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md)'s Band 3+4 signal, after verifying terminal PR #133 is merged,
      repeat the same append-and-reverify — acceptance: exits 0.
- [ ] [AI] On `ayokoding-learning-path-06-course-authoring-architecture-and-ai-harness`'s signal
      landing, append **only its SE-manifest-growth slice** (never the AI/harness-cluster courses,
      which grow the sibling plan's manifest independently) — acceptance: exits 0.
- [ ] [AI] On `ayokoding-learning-path-07-course-authoring-low-level-systems`'s signal landing, repeat
      — acceptance: exits 0.
- [ ] [AI] On `ayokoding-learning-path-08-course-authoring-security-and-ops`'s signal landing, repeat —
      acceptance: exits 0.
- [ ] [AI] On `ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own`'s signal landing,
      repeat — acceptance: exits 0.
- [ ] [AI] On `ayokoding-learning-path-11-course-authoring-capstones`'s signal landing, append its
      SE-manifest-growth slice (six of the seven promoted capstones; `capstone-solid-core` is already
      live via the original re-home) — acceptance: exits 0. A band whose append breaks
      prerequisite-consistency fails at that band's own step, identifying the offending band.

### 4.2 · Band 9 growth (two-of-three)

> **The one exception to this phase's data-edit exemption** (see
> [tech-docs §Testing Strategy](./tech-docs.md#testing-strategy)) — carries a real RED, per DD-41.

- [ ] [AI] **RED** — extend the test file with a persisted assertion: `interview-ready` and
      `fundamentally-strong` each have all five Band-9 IDs in `courseOrder`, AND
      `immediately-effective/software-engineer` has **none** of them — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: fails, naming which manifests do not yet match
      the expected two-of-three state.

  **Gherkin (underpins) →** "The interview-ready MVP proves the architecture and unblocks the sibling
  AI-manifest plan" ([prd.md](./prd.md#acceptance-criteria-gherkin)) — this cycle closes the deferral
  the Phase 1 scenario named.

  ```gherkin
  Scenario: Band 9 grows exactly two of the three software-engineer manifests, never the third
    Given the five Band-9 interview-technique course IDs have landed as authored bodies
    When the growth phase appends them to this plan's manifests
    Then interview-ready and fundamentally-strong each carry all five IDs in courseOrder
    And immediately-effective/software-engineer carries none of the five, by design
  ```

- [ ] [AI] **GREEN** — on `ayokoding-learning-path-09-course-authoring-interview-technique`'s signal
      landing, insert the five IDs into `interview-ready/software-engineer.yaml` (closing Phase 1's
      deferral) and into `fundamentally-strong/software-engineer.yaml` (its trailing optional interview
      band), at each manifest's correct topological position — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: exits 0, AND the five-ID grep returns **5**
      against both files, AND the same grep against `immediately-effective/software-engineer.yaml`
      still returns **0**. All three checks are required in the same step.
- [ ] [AI] **REFACTOR** — fold the two-of-three assertion into the test's table-driven shape —
      command: `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:lint` — acceptance: both
      exit 0.

### 4.3 · Interview-ready refresh-register smoothness re-audit

- [ ] [AI] With the five interview-technique courses now in `courseOrder`, re-run the refresh-register
      lever Phase 1 deferred — confirm each course is pitched as technique/breadth refresh for a
      working engineer, never a from-zero teach — acceptance: the lever is verified; the Phase-1
      deferral note is updated from "deferred" to "closed".

### 4.4 · Final three-manifest arc confirmation

- [ ] [AI] Confirm all three manifests reference their intended full arcs and this plan's own catalog
      contribution resolves — command: `npx nx run ayokoding-www:build` — acceptance: exits 0, AND
      every `courseOrder` ID across the three manifests resolves under `<COURSES>`.

### Phase 4 Gate

- [ ] [AI] Six-source-plan growth applied to all three manifests; `test:unit` exited 0 after each.
- [ ] [AI] Band-9 check passes all three ways in one step: **5** / **5** / **0**.
- [ ] [AI] The refresh-register lever is verified; the Phase-1 deferral is marked closed.
- [ ] [AI] `npx nx run ayokoding-www:test:unit` and `:build` exit 0 across all three manifests.
- [ ] [AI] `npx nx run ayokoding-www-fe-e2e:test:e2e` exits 0 across all three grown paths.

- [ ] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance:
      no PR, merge, or deployment occurs before Phase 10.

> **Pause Safety**: all three of this plan's manifests are at their full composition. The two smoke-test
> deferrals (interview-ready's initial narrowing, and both software-engineer manifests' Band-9
> deferral) are provably closed. Safe to stop indefinitely. To resume:
> `npx nx run ayokoding-www:build && npx nx run ayokoding-www:test:unit`.

---

## Phase 5: Section and app verification

- [ ] [AI] Run affected quality gates: `npx nx affected -t typecheck lint test:quick test:unit specs:behavior:coverage`
      — acceptance: exits 0. Fix ALL failures, including preexisting ones.
- [ ] [AI] Run e2e: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: exits 0.
- [ ] [AI] Build: `npx nx run ayokoding-www:build` — acceptance: exits 0.
- [ ] [AI] Link + heading + markdown validation:
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate --exclude plans/done --exclude apps/ayokoding-www/content --exclude apps/ose-www/content` +
      `... md heading-hierarchy validate` + `npm run lint:md` — acceptance: the link validator prints
      `All links valid! No broken links found.`; the other two exit 0.
- [ ] [AI] **Manifest-integrity + prerequisite-consistency sweep** across this plan's three manifests —
      command: `npx nx run ayokoding-www:test:unit` — acceptance: zero violations.
- [ ] [AI] **All-path smoothness re-check** — acceptance: all three pass; regressions fixed in place.
- [ ] [AI] **Ownership boundary check (scoped to this plan's three files)** —
      `test -f <MANIFESTS>careers/interview-ready/software-engineer.yaml && test -f <MANIFESTS>careers/immediately-effective/software-engineer.yaml && test -f <MANIFESTS>careers/fundamentally-strong/software-engineer.yaml`
      — acceptance: exits 0. This is a presence check on this plan's own three named files, not a
      directory-wide count — a directory-wide count would be affected by whether the sibling plan's
      `ai-engineer.yaml` has landed yet, which this plan's own gate must not depend on.
- [ ] [AI] **Scoped cross-plan link check** —
      `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate --exclude plans/done --exclude apps/ayokoding-www/content --exclude apps/ose-www/content 2>&1 | grep -F "ayokoding-learning-path-12-careers-se-manifests"`
      — acceptance: no matching line (exit 1).

### Phase 5 Gate

- [ ] [AI] Affected `typecheck`/`lint`/`test:quick`/`test:unit`/`specs:behavior:coverage` exit 0;
      `ayokoding-www-fe-e2e:test:e2e` exits 0.
- [ ] [AI] Build + link + heading + markdown validation green.
- [ ] [AI] Manifest integrity + prerequisite-consistency + smoothness report zero violations.
- [ ] [AI] All three of this plan's own manifest files present.
- [ ] [AI] Scoped cross-plan link check finds no line naming this plan's folder.
- [ ] [AI] Work committed to `final-delivery`; nothing pushed for review yet — the unit's PR opens only
      at Phase 10.

> **Pause Safety**: this plan's three-path composition passes every automated gate. Safe to stop
> indefinitely. To resume: re-run the affected quality gates and the build.

---

## Phase 6: Manual UI verification and Rule-15 three-tester retest

> This plan ships three user-visible path landings plus its own three-card slice of the paths hub, so
> the **Rule-15 three-tester retest is mandatory**, scoped to this plan's own surfaces.

- [ ] [AI] Confirm `en` is the only content locale — command:
      `test -d <PATHS> && test ! -d apps/ayokoding-www/content/id/belajar/paths` — acceptance: exits 0.
- [ ] [AI] Start the dev server: `npx nx dev ayokoding-www`.
- [ ] [AI] For `en` × breakpoints (375/768/1280px), via Playwright MCP: open the paths hub, confirm this
      plan's three cards render correctly inside the category-grouped `careers/` group, then each of
      this plan's three landings, walking 2-3 courses per path via prev/next confirming `?path=`
      persists — acceptance: all correct at all three breakpoints.
- [ ] [AI] Deep-link a course shared across this plan's own three manifests with **no** `?path=` and
      confirm the "this course is part of" affordance lists every one of this plan's own paths that
      include it (the sibling's `ai-engineer` path is intentionally excluded until Plan 13's terminal
      archival PR has merged; the definitive four-way check is Phase 8's) — acceptance: at minimum,
      every one of this plan's own paths that includes the
      course is listed.
- [ ] [AI] Verify `html[lang]` is `en` and console is clean on every screen — acceptance: both hold.
- [ ] [AI] Capture one screenshot per screen per breakpoint to
      `evidence/phase-6-<screen>-en-<breakpoint>px.png` — acceptance:
      `find evidence -name 'phase-6-*-en-*px.png' | wc -l` returns **12** (4 screens — hub plus this
      plan's 3 landings — × 3 breakpoints).
- [ ] [AI] Run `web-exploratory-tester` + `web-usability-tester` + `web-design-tester` against the hub
      and this plan's three landings — acceptance: findings recorded.
- [ ] [AI] Append each finding as a new unchecked checkbox (`EWT-NNN`/`UWT-NNN`/`DWT-NNN`).

### Rule-15 retest follow-ups

- [ ] [AI] _(populated during the retest — every defect finding must be fixed and ticked before
      archival)_

### Phase 6 Gate

- [ ] [AI] Hub (this plan's 3 cards) + 3 landings + sample courses verified in `en` at all three
      breakpoints; console clean.
- [ ] [AI] `find evidence -name 'phase-6-*-en-*px.png' | wc -l` returns **12**.
- [ ] [AI] Every Rule-15 defect finding is fixed and ticked, or explicitly permitted to defer.

- [ ] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance:
      no PR, merge, or deployment occurs before Phase 10.

> **Pause Safety**: this plan's three-path UI is verified on `final-delivery` and defect-clean in `en`, with committed
> evidence. Safe to stop indefinitely. To resume: re-run the three testers against the running app.

---

## Phase 7: Final origin main integration and CI verification

- [ ] [AI] Confirm no plan PR is still open:
      `gh pr list --search "ayokoding-learning-path-12-careers-se-manifests" --state open --json number --jq 'length'`
      — acceptance: returns **0**.
- [ ] [AI] Run the full affected suite + e2e + build on `final-delivery` — acceptance: all exit 0.
      Do not push or open a PR in this phase.

### Phase 7 Gate

- [ ] [AI] Full affected suite + e2e + build are green on `final-delivery`.
- [ ] [AI] Work committed to `final-delivery`; nothing pushed for review yet — the unit's PR opens only
      at Phase 10.

> **Pause Safety**: this plan's own three-manifest product is green on `final-delivery` and not yet
> integrated or deployed. Safe to stop indefinitely. To resume: re-run the affected suite.

---

## Phase 8: Four-manifest cross-check (needs the sibling plan fully merged)

> **This phase's start condition, checked explicitly rather than assumed**:
> `gh pr list --search "ayokoding-learning-path-13-careers-ai-manifest" --state merged --json number --jq 'length'`
> returns a value ≥ 1, AND `test -f <MANIFESTS>careers/immediately-effective/ai-engineer.yaml` returns 0. If either check fails, this phase **blocks** and this plan pauses here — it does not proceed on an
> assumption that the sibling plan "should" be done by now. See
> [README §The plan-12 / plan-13 coupling](./README.md#the-plan-12--plan-13-coupling-non-circular-by-construction)
> for why this is this plan's own later phase, not a dependency loop.

- [ ] [AI] **Verify the sibling plan's whole-plan merge** — run both checks in the block above —
      acceptance: both hold. Falsifiable both ways: either check failing blocks this phase.

### 8.1 · TDD cycle — a shared course names every published `careers/` path

- [ ] [AI] **RED** — add the four-manifest affordance scenario to `<SPECS>path-composition.feature` and
      a failing e2e step asserting that a course present in more than one of the **four** published
      `careers/` manifests, opened with **no** `?path=`, lists every including path — command:
      `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: fails because the affordance currently
      enumerates fewer paths than are now published (three, not four).

  **Gherkin (binds) →** "A shared course names every published careers/ path that includes it"

  ```gherkin
  Scenario: A shared course names every published careers/ path that includes it (needs all four manifests)
    Given all four careers/ path manifests are published — this plan's three plus the sibling plan's ai-engineer manifest — and a course appears in more than one of them
    When a reader opens that course's canonical URL with no path context
    Then the "this course is part of" affordance lists every published path whose manifest includes the course
    And each listed path links to its own path landing page
  ```

- [ ] [AI] **GREEN** — implement the step bindings against all four published manifests — command:
      `npx nx run ayokoding-www:specs:behavior:coverage && npx nx run ayokoding-www-fe-e2e:test:e2e` —
      acceptance: both exit 0. The affordance enumerates published manifests at build time, not a
      hand-written list.
- [ ] [AI] **REFACTOR** — remove duplication with this plan's own Phase 3.2 no-forked-body helper —
      command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: exits 0.

### 8.2 · Terminal four-manifest and catalog assertion

- [ ] [AI] Confirm all four `careers/` manifests are published and at full composition, all four
      landings are live, the paths hub's `careers/` group shows all four cards, and the catalog
      resolves — command:
      `find <MANIFESTS>careers/ -name '*.yaml' | wc -l` returns **4**, AND
      `grep -oE '/en/learn/paths/careers/[a-z-]+/[a-z0-9-]+' <PATHS>_index.md | sort -u | wc -l`
      returns **4**, AND `find <COURSES> -maxdepth 1 -mindepth 1 -type d | wc -l` returns **127**, AND
      `npx nx run ayokoding-www:test:unit` exits 0 — acceptance: all four hold.
- [ ] [AI] **Re-scope the ownership boundary check to the whole `careers/` subtree** now that both
      plans have merged — `find <MANIFESTS>careers/ -name '*.yaml' | sort` — acceptance: lists exactly
      the four declared path IDs (this plan's three plus the sibling's one) and nothing else.

### Phase 8 Gate

- [ ] [AI] The sibling plan's whole-plan-merged start condition holds.
- [ ] [AI] The four-manifest affordance scenario passes.
- [ ] [AI] The terminal four-manifest / 127-catalog assertion holds in full.
- [ ] [AI] `npx nx run ayokoding-www:build` + `:test:unit` + `ayokoding-www-fe-e2e:test:e2e` exit 0.

- [ ] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance:
      no PR, merge, or deployment occurs before Phase 10.

> **Pause Safety**: the whole four-path `careers/` product is cross-verified on `final-delivery` after
> Plan 13's terminal archival PR merged. This plan is not yet integrated or deployed. Safe to stop.
> To resume: re-run the four-manifest assertion.

---

## Phase 9: Knowledge Capture

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)._

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only if a durable surface would
      catch this automatically next time; discard the rest with a one-line reason.
- [ ] [AI] Apply the secret/sensitivity gate to every surviving entry.
- [ ] [AI] Apply the repo-relevance gate.
- [ ] [AI] Route each surviving learning to exactly one durable home — code homes are ALWAYS filed as a
      separate `plans/backlog/<slug>/` plan, never landed inline.
- [ ] [AI] If no generalizable learning surfaced, record `No generalizable learnings — <reason>`.

### Phase 9 Gate

- [ ] [AI] Every `learnings.md` entry is terminal, or the file records the explicit "none" escape.
- [ ] [AI] No code-homed learning landed inline.
- [ ] [AI] Work committed to `final-delivery`; the unit's PR opens only at Phase 10.

> **Pause Safety**: `learnings.md` is fully triaged. Safe to stop. To resume: re-read `learnings.md`.

---

## Phase 10: Plan Archival

### Sole PR integration (binding)

- [ ] [AI] Archive this plan on its persistent final-delivery branch before review — acceptance: the archive move and index updates are committed in the same branch.
- [ ] [AI] Open exactly one draft PR from that branch and run the PR-Review Maker→Fixer Cycle plus every local and CI gate — acceptance: the PR is the only PR for this plan.
- [ ] [AI] Mark the PR ready, merge under the hardened preconditions, and deploy once — acceptance: the merge/deploy record is the plan's sole delivery record.

- [ ] [AI] Verify ALL delivery checklist items are ticked.
- [ ] [AI] Verify Knowledge Capture is complete.
- [ ] [AI] Verify ALL quality gates pass and the build is green.
- [ ] [AI] Verify ALL manual assertions pass with committed evidence.
- [ ] [AI] Verify every Rule-15 defect finding is fixed.
- [ ] [AI] **Final re-confirmation of the terminal four-manifest and 127-catalog assertion** (Phase 8.2,
      re-run once more immediately before archival to catch any drift since Phase 8 merged) —
      acceptance: identical to Phase 8.2's result.
- [ ] [AI] Move: `git mv plans/backlog/ayokoding-learning-path-12-careers-se-manifests plans/done/YYYY-MM-DD__ayokoding-learning-path-12-careers-se-manifests`.
- [ ] [AI] Update `plans/backlog/README.md` and `plans/done/README.md`.
- [ ] [AI] Update the sibling plan's cross-references to this plan's archived path, in the same commit.
- [ ] [AI] Commit: `chore(plans): move ayokoding-learning-path-12-careers-se-manifests to done`.

### Phase 10 Gate

- [ ] [AI] All four manifests published at full composition; hub shows four cards; 127-course catalog
      resolves.
- [ ] [AI] Plan folder is under `plans/done/YYYY-MM-DD__ayokoding-learning-path-12-careers-se-manifests`.
- [ ] [AI] Draft PR opened for Phases 9-10; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged;
      deployed (no-op).

> **Pause Safety**: the plan is archived and its final PR `[AI]`-merged. Terminal state. To resume:
> nothing.

---

## Commit Guidelines (all phases)

- [ ] [AI] Commit changes thematically; Conventional Commits; split domains/concerns; preexisting fixes
      get their own commits; never bundle unrelated changes.

## Local Quality Gates (before every push)

- [ ] [AI] `npx nx affected -t typecheck lint test:quick test:unit specs:behavior:coverage` exits 0.
- [ ] [AI] `npx nx run ayokoding-www-fe-e2e:test:e2e` exits 0 for any phase touching a manifest or
      landing.
- [ ] [AI] Fix ALL failures, including preexisting ones (Root Cause Orientation).
