# Delivery Checklist — Learning Path Schema and Prerequisite DAG

This checklist delivers the **data layer** of the shared-course-library architecture: the
course-prerequisite frontmatter contract, the `PathManifest` zod schema, the `<MANIFESTS>` directory,
the pure `course-paths` functional core, and the `course-paths` Gherkin companion. It ships **no
component, no route, no rendered page, no manifest data file, and no course body** — each of those
has a named owner in [README.md](./README.md#what-this-plan-owns).

It also **custodies** the `syllabus/` detail layer (128 files). **No step in this checklist edits any
file under `syllabus/`.** The corpus arrived settled; this plan keeps it intact, keeps it linkable,
and repoints its inbound cross-plan links at archival.

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
> Git-mechanical steps (worktree create/remove, branch, push, merge) are `[AI]`.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (safe-to-stop state + resume command). Each gate covers the phase's
> **code correctness** (tests, checkers, build) and its **integration** (draft PR opened, 3-cycle
> PR-Review, CI green, `[AI]` merge). A phase is not complete until every gate check is green, and
> phase N+1 does not start while any phase N gate check is failing.

## Worktree

Worktree path: `worktrees/ayokoding-learning-path-02-schema-and-prerequisite-dag/`

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree ayokoding-learning-path-02-schema-and-prerequisite-dag
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the latest
`origin/main` when missing, syncs with `origin/main` before implementing, and prompts before deleting
the worktree after the plan is archived and pushed.

Every phase branches from the **latest `origin/main`** inside this one worktree
(`git fetch origin && git checkout main && git pull && git checkout -b
ayokoding-learning-path-02-schema-and-prerequisite-dag/<phase-slug>`), authors its work there,
commits, pushes that branch, and opens **its own draft PR**.

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans.md#worktree-specification).

## Delivery Mode: worktree-to-pr

Each phase works in the worktree on its **own branch**, opens a **draft PR** against `main`, runs the
**PR-Review Maker→Fixer Cycle** (`pr-review-maker` / `pr-review-fixer`, 3 sequential CI-gated
cycles), flips the PR to ready, and `[AI]` **merges it automatically once all quality gates are
green**. Mode inherited from the source plan at tier-2 ("plan field") precedence — not re-derived.
See
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

1. [AI] Sync the worktree to latest `origin/main` and branch:
   `git fetch origin && git checkout main && git pull && git checkout -b
ayokoding-learning-path-02-schema-and-prerequisite-dag/<phase-slug>`.
2. [AI] Stage only this phase's paths (`git add <explicit paths>` — never `git add -A`), commit
   thematically (Conventional Commits, imperative, no period), push the branch, open a **draft PR**
   against `main` (`gh pr create --draft --base main ...`) — CI runs on the PR.
3. [AI] Run the **PR-Review Maker→Fixer Cycle** (3 sequential CI-gated cycles), resolve every finding,
   then `gh pr ready`.
4. [AI] **Merge** once all quality gates are green (typecheck, lint, `test:quick`, `test:unit`,
   `test:integration`, `test:e2e` where affected, `specs:behavior:coverage`, CI, the 3-cycle review) —
   `[AI]` auto-merge per DN-11.

No deploy step is dispatched by this plan: it ships no rendered surface, so a `prod-ayokoding-www`
deploy would be a pure no-op. The first split plan to change a rendered surface owns the deploy.

## Depends-on

- **Upstream (`blockedBy`): none.** Wave 1. Start immediately.
- **Downstream (`blocks`)**: `ayokoding-learning-path-03-navigation-ui` (Wave 2),
  `ayokoding-learning-path-04-course-authoring` (Wave 2), and — transitively —
  `ayokoding-learning-path-05-manifests` (Wave 3).
- **Wave-1 sibling, soft coupling, NOT a blocking edge**:
  `ayokoding-learning-path-01-url-restructure`. It writes `prerequisites:` frontmatter into 37
  re-homed `_index.md` files; **this plan owns that field's shape**, canonically. Phase 1 carries an
  explicit contract-agreement check against that plan's copy.

## Parallelization Model

**Cap**: honor the in-force subagent/PR-review concurrency cap (parallel-by-default, background
subagents capped per the orchestration convention). The main thread self-promotes nothing.

- **Phases 0 → 1 → 2 are serial.** Phase 1 defines the schema Phase 2's core is written against;
  Phase 2's every RED step imports from what Phase 1 created.
- **Inside Phase 2, the seven TDD cycles are serial by convention, not by necessity.** Cycles 2
  (`path-nav`), 3 (`path-context`), 4 (`content-url`) and 5 (`resolvePrerequisites`) touch disjoint
  files and could pipeline through review under the cap; cycles 6 and 7 depend on cycle 1's
  normalized course-ref shape. Keep them serial unless the cap has genuine headroom — the phase is
  one PR either way.
- **Phases 3 → 4 → 5 → 6 → 7 are serial.**
- **This plan runs in parallel with `ayokoding-learning-path-01-url-restructure`** (the other Wave-1
  plan). Do not serialize them for convenience — the split exists to buy that parallelism.

## Path constants

Reproduced verbatim in all five split plans. A checklist whose `<FEAT>` placeholders cannot be
expanded is not executable.

- `<COURSES>` = `apps/ayokoding-www/content/en/learn/courses/` (course bundles; served at `/en/c/learn/courses/<course-id>`)
- `<PATHS>` = `apps/ayokoding-www/content/en/learn/paths/` (thin path-landing anchors; served at `/en/c/learn/paths/<path-id>`)
- `<SE_OLD>` = `apps/ayokoding-www/content/en/learn/fundamentally-strong/software-engineer/` (legacy home of the 33 shipped topics + 4 existing capstones, incl. `capstone-solid-core` — the re-home source)
- `<FEAT>` = `apps/ayokoding-www/src/features/course-paths/`
- `<MANIFESTS>` = `<FEAT>manifests/` (standalone YAML data files, nested to mirror slash path ids — `<MANIFESTS><path-id>.yaml`)
- `<LEGACY>` = `apps/ayokoding-www/content/en/learn/legacy/` (**new bucket**, scope extension; served at `/en/c/learn/legacy/<domain>/…`)
- `<REDIR>` = `apps/ayokoding-www/src/redirects/`
- `<SPECS>` = `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/course-paths/`
- `<NAVSPECS>` = `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/navigation/` (existing domain — the three-bucket Gherkin lands beside `content-namespace-redirects.feature`)
- Path ids: `interview-ready/software-engineer`, `immediately-effective/software-engineer`, `fundamentally-strong/software-engineer`, `immediately-effective/software-engineer-to-ai-engineer` (fourth path, manifest at `<MANIFESTS>immediately-effective/software-engineer-to-ai-engineer.yaml`)

## Phase provenance

This plan's phases are renumbered from 0 to 7 so that "phase N+1" reads correctly. The mapping back
to the source plan is recorded here so a reader auditing the split can trace every step.

| This plan | Source plan                                           | Note                                                                                                         |
| --------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Phase 0   | Phase 0 (`delivery.md:177-234`), scoped               | Generic steps kept; re-home / component / collision / legacy inventories dropped (they route to other plans) |
| Phase 1   | Phase 1 partial (`delivery.md:314-327`)               | The three schema step blocks only. `:310-313` → url-restructure; `:244-309` → navigation-ui                  |
| Phase 2   | Phase 2 (`delivery.md:343-502`) in full               | Split into seven explicit RED/GREEN/REFACTOR cycles                                                          |
| Phase 3   | Phase 13 (`delivery.md:1973-2026`), scoped            | Manifest / three-bucket / redirect sweeps dropped — not this plan's surface                                  |
| Phase 4   | Phase 14 (`delivery.md:2029-2105`), scoped + inverted | Feature walk-through replaced by a no-regression sweep; Rule-15 exemption recorded                           |
| Phase 5   | Phase 15 (`delivery.md:2108-2130`), scoped            | Deploy confirmation dropped — no rendered surface ships                                                      |
| Phase 6   | Phase 16 (`delivery.md:2133-2161`)                    | Knowledge Capture, carried whole                                                                             |
| Phase 7   | Phase 17 (`delivery.md:2164-2199`) + BF-8 step 5      | Archival plus the reciprocal cross-plan link repoint                                                         |

---

## Phase 0: Environment Setup and Baseline

> _Executor: repo-setup-manager_
>
> **No cross-plan precondition.** This plan is Wave 1 with no plan-level prerequisite. The only
> start precondition is that `origin/main` is green and the `course-paths` feature does not yet
> exist.

- [ ] [AI] Enter/provision the worktree and install dependencies in the root worktree: `npm install`
      — acceptance: exits 0, `node_modules/` synchronized.
- [ ] [AI] Converge the toolchain in the root worktree: `npm run doctor -- --fix`
      — acceptance: exits 0 with no unresolved drift.
- [ ] [AI] Establish baselines: `npx nx run ayokoding-www:build`, `npx nx run ayokoding-www:test:unit`,
      and `npx nx run ayokoding-www:specs:behavior:coverage`
      — acceptance: all three exit 0; record the pass state and the current specs-coverage summary in
      `evidence/phase-0-baseline.txt`. Any preexisting failure is resolved before Phase 1 starts, not
      deferred (Root Cause Orientation).
- [ ] [AI] **Confirm the `course-paths` feature does not exist yet** (the start precondition):
      `test -d apps/ayokoding-www/src/features/course-paths`
      — acceptance: returns **non-zero**. Falsifiable both ways: it returns 0 the moment Phase 1
      creates the directory, so this check only passes before any work has landed. Record the result
      in `evidence/phase-0-baseline.txt`.
- [ ] [AI] **Snapshot the `content-url.ts` baseline** — record the current exported signature and the
      current test names from
      `apps/ayokoding-www/src/features/content/core/content-url.ts` and its `.test.ts` sibling into
      `evidence/phase-0-baseline.txt` via
      `grep -n "export" apps/ayokoding-www/src/features/content/core/content-url.ts` and
      `grep -n "it(\|describe(" apps/ayokoding-www/src/features/content/core/content-url.test.ts`
      — acceptance: both commands print at least one line and the output is committed. This is the
      before-picture the Phase 2 cycle-4 change is diffed against.
- [ ] [AI] **Confirm the `syllabus/` corpus is intact and untouched** —
      `find plans/backlog/ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus -type f | wc -l`
      — acceptance: returns **128**. Falsifiable both ways: a deletion or an addition changes the
      number. Record it in `evidence/phase-0-baseline.txt`.
- [ ] [AI] **Confirm the `<SPECS>` domain folder does not exist yet** —
      `test -d specs/apps/ayokoding/behavior/ayokoding-www/gherkin/course-paths`
      — acceptance: returns **non-zero** (Phase 2 creates it).
- [ ] [AI] Confirm `learnings.md` exists in the plan folder with its H1 —
      `test -f plans/backlog/ayokoding-learning-path-02-schema-and-prerequisite-dag/learnings.md`
      — acceptance: returns 0 and the file's first content line is
      `# Learnings: ayokoding-learning-path-02-schema-and-prerequisite-dag`.
- [ ] [AI] Create the evidence folder: `mkdir -p plans/backlog/ayokoding-learning-path-02-schema-and-prerequisite-dag/evidence`
      — acceptance: `test -d …/evidence` returns 0.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [ ] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift.
- [ ] [AI] `ayokoding-www` `build` + `test:unit` + `specs:behavior:coverage` baselines recorded green
      in `evidence/phase-0-baseline.txt`; zero unresolved preexisting failures.
- [ ] [AI] `test -d apps/ayokoding-www/src/features/course-paths` returns non-zero and
      `test -d specs/apps/ayokoding/behavior/ayokoding-www/gherkin/course-paths` returns non-zero —
      both surfaces confirmed absent.
- [ ] [AI] `find …/syllabus -type f | wc -l` returns **128**.
- [ ] [AI] Draft PR opened; CI triggered; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged.

> **Pause Safety**: only the toolchain was verified and the current state snapshotted — no code, no
> schema, no spec exists yet. Safe to stop indefinitely. To resume: re-run
> `npx nx run ayokoding-www:build && npx nx run ayokoding-www:test:unit` and confirm both still exit 0.

---

## Phase 1: Schema Foundation — prerequisite contract, `PathManifest`, `<MANIFESTS>`

> _Suggested executor: `swe-typescript-dev`_
>
> Source: `delivery.md:314-327` of `shared-course-library-and-learning-paths` — the three schema step
> blocks of its Phase 1. The `_index.md` content-homes step (`:310-313`) belongs to
> `ayokoding-learning-path-01-url-restructure`; the design-funnel steps (`:244-309`) belong to
> `ayokoding-learning-path-03-navigation-ui`. Phase 1 was a **three-way** split, not two.

### 1.1 Course-prerequisite metadata contract (canonical here)

- [ ] [AI] Verify the canonical contract is stated in this plan's
      `tech-docs.md` under `## The prerequisite frontmatter contract (canonical here)`, naming the
      key `prerequisites`, the YAML-sequence-of-course-ID-strings value, and the six binding rules
      — command:
      `grep -qF "The prerequisite frontmatter contract (canonical here)" plans/backlog/ayokoding-learning-path-02-schema-and-prerequisite-dag/tech-docs.md`
      — acceptance: exits 0. Falsifiable both ways: renaming or deleting the heading makes it exit 1.
- [ ] [AI] **Verify the Wave-1 sibling's copy agrees** — read
      `plans/backlog/ayokoding-learning-path-01-url-restructure/tech-docs.md` and compare its
      reproduction of the `prerequisites:` frontmatter contract against this plan's canonical
      statement, clause by clause (key name, value type, empty-list rule, ID referent, unordered
      rule, resolver-miss rule) — acceptance: the two statements agree on all six clauses. **If they
      diverge, this plan's wins**: correct the sibling plan's copy in this phase's commit and note
      the correction in `learnings.md`. Falsifiable both ways: introducing a deliberate one-word
      change in either copy makes the comparison fail.
  - _Suggested executor: `plan-fixer` (if a correction to the sibling plan doc is needed)_
- [ ] [AI] Record in `evidence/phase-1-contract-agreement.txt` the exact six-clause comparison result
      and the commit SHA of the sibling plan folder at the time of comparison (`git log -1
--format=%H -- plans/backlog/ayokoding-learning-path-01-url-restructure`)
      — acceptance: file exists and names a SHA. This is the audit trail for failure mode F-6, whose
      symptom (37 empty prerequisite lists, green build) is otherwise invisible until Wave 2.

### 1.2 `PathManifest` zod schema — TDD cycle

- [ ] [AI] **RED** — write a failing unit test in
      `apps/ayokoding-www/src/features/course-paths/core/schemas.test.ts` _(new test)_ asserting that
      `PathManifestSchema.safeParse(...)` **accepts** a manifest carrying `pathId`, `title`,
      `description`, and a `courseOrder` mixing bare course-ID strings with
      `{ id, framing: { intro, outro } }` objects, and **rejects** a manifest missing `courseOrder`
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the run fails with a module-resolution error naming `./schemas` (the file does
      not exist yet). Falsifiable both ways: once `schemas.ts` exists and is correct, this exact test
      passes.
- [ ] [AI] **GREEN** — implement the `PathManifest` zod schema in
      `apps/ayokoding-www/src/features/course-paths/core/schemas.ts` _(new file)_ using **zod 4.3.6**
      [Repo-grounded — `apps/ayokoding-www/package.json`], per
      [tech-docs §The `PathManifest` zod schema](./tech-docs.md#the-pathmanifest-zod-schema): `pathId`
      string, `title` string, `description` string, `courseOrder` array of (course-ID string) or
      (object with `id` plus optional `framing` carrying optional `intro` / `outro`)
      — command: `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:typecheck`
      — acceptance: both exit 0; the new `schemas.test.ts` assertions pass and no previously-passing
      test regresses.
- [ ] [AI] **REFACTOR** — export the inferred `PathManifest` and `CourseRef` types from `schemas.ts`
      so no downstream module re-declares them, and confirm the file imports nothing but `zod`
      — command:
      `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:lint && grep -n "^import" apps/ayokoding-www/src/features/course-paths/core/schemas.ts`
      — acceptance: the first two exit 0 and the `grep` prints exactly one line, importing from
      `zod`. Falsifiable both ways: adding a second import makes the `grep` print two lines.

### 1.3 `<MANIFESTS>` directory and its README

- [ ] [AI] Create the manifest data-file home:
      `mkdir -p apps/ayokoding-www/src/features/course-paths/manifests`
      — acceptance: `test -d apps/ayokoding-www/src/features/course-paths/manifests` returns 0
      (returns non-zero before this step).
- [ ] [AI] Author `apps/ayokoding-www/src/features/course-paths/manifests/README.md` _(new file)_
      stating: (a) that nested `<path-id>.yaml` data files land here, one per path, with a slash in
      a path ID becoming a nested directory; (b) that **every** `.yaml` file in this directory is
      owned by `ayokoding-learning-path-05-manifests` and by no other plan; (c) that this plan
      creates the directory and nothing else in it
      — command:
      `test -f apps/ayokoding-www/src/features/course-paths/manifests/README.md && grep -qF "ayokoding-learning-path-05-manifests" apps/ayokoding-www/src/features/course-paths/manifests/README.md`
      — acceptance: exits 0. Falsifiable both ways: omitting the ownership sentence makes the `grep`
      exit 1.
- [ ] [AI] Confirm the directory ships **empty of manifest data files** —
      `find apps/ayokoding-www/src/features/course-paths/manifests -name '*.yaml' | wc -l`
      — acceptance: returns **0**. Falsifiable both ways: authoring any `.yaml` here (a boundary
      violation against the manifest-ownership invariant) makes it return a non-zero count.

### Local Quality Gates (Before Push)

- [ ] [AI] `npx nx affected -t typecheck` — acceptance: exits 0.
- [ ] [AI] `npx nx affected -t lint` — acceptance: exits 0.
- [ ] [AI] `npx nx affected -t test:quick test:unit` — acceptance: exits 0.
- [ ] [AI] `npx nx affected -t specs:behavior:coverage` — acceptance: exits 0.
- [ ] [AI] Fix ALL failures — including preexisting issues not caused by this phase's changes.

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes.
> This follows Root Cause Orientation — proactively fix preexisting errors encountered during work.
> Commit preexisting fixes separately with appropriate conventional-commit messages.

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [ ] [AI] `test -f apps/ayokoding-www/src/features/course-paths/core/schemas.ts` returns 0 and
      `npx nx run ayokoding-www:typecheck` exits 0.
- [ ] [AI] `npx nx run ayokoding-www:test:unit` exits 0 with the new `schemas.test.ts` accept-case and
      reject-case both passing.
- [ ] [AI] `test -d apps/ayokoding-www/src/features/course-paths/manifests` returns 0,
      `test -f …/manifests/README.md` returns 0, and
      `find …/manifests -name '*.yaml' | wc -l` returns **0**.
- [ ] [AI] The six-clause contract-agreement comparison against
      `ayokoding-learning-path-01-url-restructure` is recorded in
      `evidence/phase-1-contract-agreement.txt` with a SHA, and any divergence was corrected in
      favour of this plan.
- [ ] [AI] `find …/syllabus -type f | wc -l` still returns **128** — the corpus was not touched.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged.

> **Pause Safety**: the manifest schema compiles and the empty `<MANIFESTS>` home exists; no resolver
> consumes them yet and no rendered behaviour changed anywhere. Safe to stop indefinitely. To resume:
> `npx nx run ayokoding-www:typecheck && npx nx run ayokoding-www:test:unit`.

---

## Phase 2: `course-paths` Pure Core — TDD + specs RED

> _Suggested executor: `swe-typescript-dev` (core logic) + `specs-maker` (Gherkin)._
>
> Source: `delivery.md:343-502` of `shared-course-library-and-learning-paths`, expanded from four
> combined RED steps into **seven explicit RED/GREEN/REFACTOR cycles** plus a closing purity refactor.
> This is the most code-heavy phase in the whole five-way split.

### 2.0 Specs RED — the `course-paths` Gherkin companion

- [ ] [AI] Author the `course-paths` Gherkin companion under
      `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/course-paths/` _(new directory)_ — one
      `.feature` file per behaviour (path-order nav, breadcrumb, canonical fallback, invalid-path
      fallback, omitted course, manifest integrity, prerequisite display,
      prerequisite-consistent ordering) plus a `README.md`, sourced from
      [prd.md §Acceptance Criteria](./prd.md#acceptance-criteria-gherkin) and from the
      downstream-owned scenarios listed in
      [prd.md §Scenarios owned by downstream plans](./prd.md#scenarios-owned-by-downstream-plans-that-this-plans-resolvers-underpin)
      — command: `npx nx run ayokoding-www:specs:behavior:coverage`
      — acceptance: the command **fails**, reporting the new `course-paths` domain as uncovered (no
      step bindings exist yet). Falsifiable both ways: it exits 0 today, before the folder exists.
  - _Suggested executor: `specs-maker`_
- [ ] [AI] Record the resulting coverage delta and name its closing plan explicitly in
      `evidence/phase-2-specs-coverage-delta.txt`: _"the `course-paths` step bindings are authored by
      `ayokoding-learning-path-03-navigation-ui`; this delta closes there, not here"_
      — acceptance: file exists and names that plan by full folder name.
- [ ] [AI] Verify every scenario in the new `.feature` files satisfies the step-keyword cardinality
      rule (exactly one primary `Given`, one `When`, one `Then`; extras chained with `And` / `But`)
      — command:
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- repo-governance gherkin-keyword-cardinality`
      — acceptance: exits 0 with no finding against any file under `<SPECS>`. Falsifiable both ways:
      a deliberate second primary `When` in any scenario makes it report that file.

### 2.1 TDD cycle 1 — course-ref normalization (`manifest.ts`)

- [ ] [AI] **RED** — write a failing unit test in
      `apps/ayokoding-www/src/features/course-paths/core/manifest.test.ts` _(new test)_ for
      `normalizeCourseRef(ref)`: a bare string `"just-enough-python"` normalizes to
      `{ id: "just-enough-python" }` with no framing; an object
      `{ id: "x", framing: { intro: "i" } }` normalizes to the same shape preserving `framing`
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the run fails because `normalizeCourseRef` is undefined. Falsifiable both ways:
      after the GREEN step this exact test passes.

  **Gherkin (underpins) →** the `courseOrder` element shape asserted by "A path manifest is a valid
  topological entry into the prerequisite DAG" and "Every manifest course reference resolves to a
  real course" (both in [prd.md](./prd.md#acceptance-criteria-gherkin)); the binding cycles are 2.6
  and 2.7 below.

- [ ] [AI] **GREEN** — implement `normalizeCourseRef` and re-export the `PathManifest` /
      `CourseRef` types in `apps/ayokoding-www/src/features/course-paths/core/manifest.ts`
      _(new file)_, importing the types from `./schemas`
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0; the two new assertions pass and no previously-passing test regresses.
- [ ] [AI] **REFACTOR** — make `normalizeCourseRef` total (never throws on a well-typed input) and
      confirm `manifest.ts` imports only from `./schemas` and `zod`
      — command:
      `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:lint && grep -n "^import" apps/ayokoding-www/src/features/course-paths/core/manifest.ts`
      — acceptance: the first two exit 0 and every printed import line names `./schemas` or `zod`.

### 2.2 TDD cycle 2 — `resolvePathNav` (`path-nav.ts`)

- [ ] [AI] **RED** — write failing unit tests in
      `apps/ayokoding-www/src/features/course-paths/core/path-nav.test.ts` _(new test)_ for
      `resolvePathNav(manifest, courseId)`: middle course returns both neighbours; **first** course
      returns `prev: null`; **last** course returns `next: null`; a course absent from `courseOrder`
      returns `{ prev: null, next: null }`
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the run fails because `resolvePathNav` is undefined. Falsifiable both ways: after
      GREEN all four assertions pass.

  **Gherkin (underpins) →** "Prev and next follow the active path's order"; "A course omitted from a
  path shows no path nav for that path"; "The path rail shows the whole ordered arc beside a course
  at desktop width"; "The path rail collapses into the existing navigation drawer on a phone".
  **These four scenarios are owned by `ayokoding-learning-path-03-navigation-ui`'s `prd.md`**, not
  by this plan; they are reproduced here so the RED signal names the behaviour it ultimately serves.

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
    And neither the path rail nor the path banner is shown for that path

  Scenario: The path rail shows the whole ordered arc beside a course at desktop width
    Given a reader opens a course in path context on a desktop-width viewport
    When the page renders
    Then the left rail lists that path's courses in manifest order with the current course marked
    And the current course is distinguished by a marker and weight, not by colour alone
    And the rail offers a link back to the full path and to the whole course library

  Scenario: The path rail collapses into the existing navigation drawer on a phone
    Given a reader opens a course in path context on a phone-width viewport
    When they activate the path readout's "open path course list" control
    Then the existing left navigation drawer opens showing that path's ordered courses
    And focus moves into the drawer and returns to the control when the drawer is dismissed
  ```

- [ ] [AI] **GREEN** — implement `resolvePathNav(manifest, courseId)` in
      `apps/ayokoding-www/src/features/course-paths/core/path-nav.ts` _(new file)_: locate `courseId`
      in the normalized `courseOrder`, return the neighbouring refs, return nulls at both boundaries
      and for an absent course
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0; all four assertions pass and no previously-passing test regresses.
- [ ] [AI] **REFACTOR** — replace any repeated linear scan with a single index lookup and confirm
      `path-nav.ts` performs no IO
      — command:
      `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:typecheck && npx nx run ayokoding-www:lint`
      — acceptance: all three exit 0 and the four assertions still pass.

### 2.3 TDD cycle 3 — `parsePathContext` (`path-context.ts`)

- [ ] [AI] **RED** — write failing unit tests in
      `apps/ayokoding-www/src/features/course-paths/core/path-context.test.ts` _(new test)_ for
      `parsePathContext(searchParams, manifests)`: a `path` param naming a loaded manifest returns
      that `pathId`; a `path` param naming **no** loaded manifest returns `null`; an **absent** `path`
      param returns `null`; and none of the three throws
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the run fails because `parsePathContext` is undefined.

  **Gherkin (underpins) →** "A course deep-linked without path context renders the canonical view";
  "An invalid path context falls back to the canonical view"; "A course opened without path context
  renders the generic sidebar unchanged". **Owned by
  `ayokoding-learning-path-03-navigation-ui`'s `prd.md`**; reproduced here for the RED signal.

  ```gherkin
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

  Scenario: A course opened without path context renders the generic sidebar unchanged
    Given a reader opens a canonical course URL with no path context query parameter
    When the page renders
    Then the left sidebar shows the generic content tree exactly as it does elsewhere in the site
    And no path rail, path readout, or path breadcrumb segment appears
  ```

- [ ] [AI] **GREEN** — implement `parsePathContext(searchParams, manifests)` in
      `apps/ayokoding-www/src/features/course-paths/core/path-context.ts` _(new file)_: read the
      `path` search param, return the matching `pathId` **only** when it names a loaded manifest,
      else `null`
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0; all four assertions pass.
- [ ] [AI] **REFACTOR** — make the validation gate explicit (a single membership test against the
      loaded manifest IDs) and confirm no code path throws
      — command: `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:lint`
      — acceptance: both exit 0; the "never throws" assertion still passes for all three input
      shapes.

### 2.4 TDD cycle 4 — `contentUrl` gains path context (`content-url.ts`)

> This is the **only** cycle in this plan that modifies shipped code. It is what makes the Phase 4
> no-regression sweep necessary.

- [ ] [AI] **RED** — extend
      `apps/ayokoding-www/src/features/content/core/content-url.test.ts` _(existing test file,
      Repo-grounded)_ with failing assertions that `contentUrl("en", "learn/courses/x", "interview-ready/software-engineer")`
      appends `?path=interview-ready/software-engineer`, and that
      `contentUrl("en", "learn/courses/x")` (no third argument) still returns
      `/en/c/learn/courses/x` unchanged
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the new `?path=` assertion **fails** (the parameter is not supported) while the
      no-argument assertion **passes** (existing behaviour). Falsifiable both ways: after GREEN both
      pass, and reverting GREEN makes only the first fail again.

  **Gherkin (underpins) →** "A path landing page lists its courses in manifest order"; "The
  breadcrumb reflects the active path"; "A legacy fundamentally-strong URL redirects to the canonical
  course URL". **The first two are owned by `ayokoding-learning-path-03-navigation-ui`; the third by
  `ayokoding-learning-path-01-url-restructure`.** Reproduced here for the RED signal.

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

- [ ] [AI] **GREEN** — extend `contentUrl` in
      `apps/ayokoding-www/src/features/content/core/content-url.ts` _(existing file, Repo-grounded)_
      with an **optional** third `pathId` parameter appending `?path=<path-id>`, preserving the
      canonical `/en/c/learn/courses/<course-id>` shape when it is omitted
      — command: `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:typecheck`
      — acceptance: both exit 0; the new assertion passes and **every** pre-existing `content-url`
      assertion recorded in `evidence/phase-0-baseline.txt` still passes (or is updated for the
      canonical shape in this same commit, with the update named explicitly in the commit body).
- [ ] [AI] **REFACTOR** — ensure the parameter is genuinely optional at the type level (no call site
      elsewhere in the app needs updating) and that the query string is built once, not concatenated
      ad hoc
      — command:
      `npx nx run ayokoding-www:typecheck && npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:lint`
      — acceptance: all three exit 0 with **no** change required to any existing `contentUrl` call
      site. Falsifiable both ways: making the parameter required breaks `typecheck` at existing call
      sites.

### 2.5 TDD cycle 5 — `resolvePrerequisites` (`prerequisites.ts`)

- [ ] [AI] **RED** — write failing unit tests in
      `apps/ayokoding-www/src/features/course-paths/core/prerequisites.test.ts` _(new test)_ for
      `resolvePrerequisites(courseId, prerequisitesByCourse)`: a course with two declared
      prerequisites returns both IDs in declaration order; a course declaring `[]` returns an empty
      array; a course **absent** from the index returns an empty array (not `undefined`, not a throw)
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the run fails because `resolvePrerequisites` is undefined.

  **Gherkin (underpins) →** "A course page surfaces its declared prerequisites". **Owned by
  `ayokoding-learning-path-03-navigation-ui`'s `prd.md`**; reproduced here for the RED signal.

  ```gherkin
  Scenario: A course page surfaces its declared prerequisites
    Given a course declares prerequisites in its canonical metadata
    When a reader opens the course page with or without a path context
    Then the page lists each prerequisite course with a link to its canonical URL
    And the prerequisite list renders even in the canonical no-path view
  ```

- [ ] [AI] **GREEN** — implement `resolvePrerequisites(courseId, prerequisitesByCourse)` in
      `apps/ayokoding-www/src/features/course-paths/core/prerequisites.ts` _(new file)_, pure and
      IO-free, treating an absent entry and an empty declaration identically
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0; all three assertions pass.
- [ ] [AI] **REFACTOR** — extract the "declared prerequisite IDs for a course" lookup so cycle 2.6
      reuses it rather than re-implementing the traversal
      — command: `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:lint`
      — acceptance: both exit 0 and the three assertions still pass.

### 2.6 TDD cycle 6 — `checkPrerequisiteConsistency` (`prerequisites.ts`)

- [ ] [AI] **RED** — write failing unit tests in
      `apps/ayokoding-www/src/features/course-paths/core/prerequisites.test.ts` _(existing test file
      from cycle 2.5)_ for
      `checkPrerequisiteConsistency(manifest, prerequisitesByCourse, libraryCourseIds)`: a **clean**
      fixture manifest whose `courseOrder` places every in-manifest prerequisite before its dependent
      reports **zero** violations; a **deliberately-violating** fixture that places
      `advanced-algorithms` before its declared prerequisite
      `data-structures-and-algorithms-essentials` reports **exactly one** violation naming that
      course; and a prerequisite that is declared but **omitted from the manifest** is **not**
      reported
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the run fails because `checkPrerequisiteConsistency` is undefined. Falsifiable
      both ways: the clean and violating fixtures must produce **different** results after GREEN, so
      an implementation that always returns zero violations fails the second assertion.

  **Gherkin (binds) →** "A path manifest is a valid topological entry into the prerequisite DAG"

  ```gherkin
  Scenario: A path manifest is a valid topological entry into the prerequisite DAG
    Given a path manifest lists a courseOrder of course IDs
    When the manifest-integrity check runs
    Then no course appears before any of its declared prerequisites that are also in the manifest
    And every listed course ID resolves to an existing course in the library
  ```

- [ ] [AI] **GREEN** — implement `checkPrerequisiteConsistency` in
      `apps/ayokoding-www/src/features/course-paths/core/prerequisites.ts` _(existing file from cycle
      2.5)_: for each course in `courseOrder`, report every declared prerequisite that is present in
      `libraryCourseIds` **and** in the manifest but appears at a later index
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0; the clean fixture reports zero violations and the violating fixture
      reports exactly one, naming `advanced-algorithms`.
- [ ] [AI] **REFACTOR** — return a structured violation record (`{ courseId, missingPrerequisiteId,
courseIndex, prerequisiteIndex }`) rather than a string, so a downstream gate can render a
      precise message
      — command: `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:typecheck`
      — acceptance: both exit 0 and the violating fixture's single record carries all four fields.

### 2.7 TDD cycle 7 — `checkManifestIntegrity` (`manifest-integrity.ts`)

- [ ] [AI] **RED** — write failing unit tests in
      `apps/ayokoding-www/src/features/course-paths/core/manifest-integrity.test.ts` _(new test)_ for
      `checkManifestIntegrity(manifest, libraryCourseIds)`: a **clean** fixture reports no unresolved
      and no duplicate IDs; a fixture whose `courseOrder` names a course absent from
      `libraryCourseIds` reports **exactly that ID** as unresolved; a fixture listing one ID twice
      reports **exactly that ID** as duplicated
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the run fails because `checkManifestIntegrity` is undefined. Falsifiable both
      ways: an implementation returning empty sets unconditionally fails the second and third
      assertions.

  **Gherkin (binds) →** "Every manifest course reference resolves to a real course"

  ```gherkin
  Scenario: Every manifest course reference resolves to a real course
    Given a path manifest lists a courseOrder of course IDs
    When the manifest-integrity check runs
    Then every listed course ID resolves to an existing course in the library
    And no course ID appears more than once in the manifest
  ```

- [ ] [AI] **GREEN** — implement `checkManifestIntegrity(manifest, libraryCourseIds)` in
      `apps/ayokoding-www/src/features/course-paths/core/manifest-integrity.ts` _(new file)_, pure,
      returning the unresolved-ID set and the duplicate-ID set
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0; all three assertions pass.
- [ ] [AI] **REFACTOR** — normalize each `courseOrder` entry through `normalizeCourseRef` (cycle 2.1)
      instead of branching on the string-or-object shape inline
      — command: `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:typecheck`
      — acceptance: both exit 0; the object-form `courseOrder` fixture is handled identically to the
      string form.

### 2.8 Closing REFACTOR — the purity guard

- [ ] [AI] **REFACTOR** — extract any shared course-ref type still declared in more than one module
      into `manifest.ts`, and confirm the core is IO-free
      — command:
      `grep -rnE "from ['\"](node:)?(fs|path)['\"]|from ['\"]react['\"]" apps/ayokoding-www/src/features/course-paths/core`
      — acceptance: the command prints **nothing** and exits 1. Falsifiable both ways: adding a
      single `import fs from "fs"` to any file under `core/` makes it print that line and exit 0.
- [ ] [AI] Confirm the whole core still passes after the extraction —
      command:
      `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:typecheck && npx nx run ayokoding-www:lint`
      — acceptance: all three exit 0.

### Local Quality Gates (Before Push)

- [ ] [AI] `npx nx affected -t typecheck` — acceptance: exits 0.
- [ ] [AI] `npx nx affected -t lint` — acceptance: exits 0.
- [ ] [AI] `npx nx affected -t test:quick test:unit test:integration test:e2e` — acceptance: exits 0.
      `test:integration` and `test:e2e` author nothing new here; they run to prove the
      `content-url.ts` change regresses no existing journey.
- [ ] [AI] `npx nx affected -t specs:behavior:coverage` — acceptance: reports the recorded
      `course-paths` delta and **no other** delta. The `course-paths` delta is expected and its
      closing plan is named in `evidence/phase-2-specs-coverage-delta.txt`.
- [ ] [AI] Fix ALL failures — including preexisting issues not caused by this phase's changes.

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes.
> This follows Root Cause Orientation. Commit preexisting fixes separately with appropriate
> conventional-commit messages.

### Commit Guidelines

- [ ] [AI] Commit changes thematically — group related changes into logically cohesive commits
      (one per TDD cycle is the natural grain here).
- [ ] [AI] Follow Conventional Commits: `<type>(<scope>): <description>` (imperative, no period).
- [ ] [AI] Keep the `content-url.ts` change (cycle 2.4) in its **own** commit — it is the only shipped-code
      change in the plan and must be revertable in isolation.
- [ ] [AI] Preexisting fixes get their own commits, separate from plan work.
- [ ] [AI] Do NOT bundle unrelated changes into a single commit.

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [ ] [AI] All six core modules exist:
      `test -f` returns 0 for each of `schemas.ts`, `manifest.ts`, `path-nav.ts`, `path-context.ts`,
      `prerequisites.ts`, `manifest-integrity.ts` under
      `apps/ayokoding-www/src/features/course-paths/core/`.
- [ ] [AI] `resolvePathNav`, `parsePathContext`, `resolvePrerequisites`,
      `checkPrerequisiteConsistency`, `checkManifestIntegrity`, `normalizeCourseRef` and
      `contentUrl(locale, slug, pathId)` are all implemented with green unit tests —
      `npx nx run ayokoding-www:test:unit` exits 0.
- [ ] [AI] Both integrity checks are falsifiable in both directions: the clean fixture reports zero
      findings AND the deliberately-violating fixture reports exactly the expected finding, for
      `checkPrerequisiteConsistency` **and** `checkManifestIntegrity`.
- [ ] [AI] The purity guard prints nothing:
      `grep -rnE "from ['\"](node:)?(fs|path)['\"]|from ['\"]react['\"]" apps/ayokoding-www/src/features/course-paths/core`
      exits 1.
- [ ] [AI] `course-paths` Gherkin authored under `<SPECS>`; the
      `repo-governance gherkin-keyword-cardinality` audit exits 0; the coverage delta is recorded in
      `evidence/phase-2-specs-coverage-delta.txt` naming
      `ayokoding-learning-path-03-navigation-ui` as its closing plan.
- [ ] [AI] `npx nx run ayokoding-www:typecheck` + `:lint` + `:build` exit 0.
- [ ] [AI] `find …/syllabus -type f | wc -l` still returns **128** — the corpus was not touched.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged.

> **Pause Safety**: the pure ordering, context, prerequisite and integrity logic is implemented and
> unit-tested; no route or component consumes it, so the only shipped-behaviour change is
> `contentUrl`'s optional parameter, which is additive and covered by its existing tests. Safe to
> stop indefinitely. To resume: `npx nx run ayokoding-www:test:unit`.
>
> **This is the handoff point.** Once this phase's PR is merged, both Wave-2 plans
> (`ayokoding-learning-path-03-navigation-ui` and
> `ayokoding-learning-path-04-course-authoring`) have their start precondition from this plan
> satisfied.

---

## Phase 3: Section and App Verification

> Source: Phase 13 of `shared-course-library-and-learning-paths`, scoped. Its manifest-integrity
> sweep, all-path smoothness sweep, three-bucket structural sweep, and redirect-order regression
> check are **not** carried here — none of those artefacts exists in this plan's surface. They belong
> to `ayokoding-learning-path-05-manifests` and `ayokoding-learning-path-01-url-restructure`.

- [ ] [AI] Run affected quality gates from the worktree:
      `npx nx affected -t typecheck lint test:quick test:unit test:integration test:e2e specs:behavior:coverage`
      — acceptance: exits 0, with the single expected `course-paths` specs delta recorded in
      `evidence/phase-2-specs-coverage-delta.txt`. Fix ALL failures, including preexisting ones (Root
      Cause Orientation), committing preexisting fixes separately.
- [ ] [AI] Build the site: `npx nx run ayokoding-www:build` — acceptance: exits 0.
- [ ] [AI] Run link + heading-hierarchy + markdown validation:
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md links validate --exclude plans/done --exclude apps/ayokoding-www/content --exclude apps/ose-www/content`
      then
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md heading-hierarchy validate`
      then `npm run lint:md`
      — acceptance: the first prints `All links valid! No broken links found.`; the other two exit 0.
      **Note**: `md links validate` accepts **no positional path** and always walks the repo — the
      three `--exclude` flags are the pre-push hook's own form, and the bare repo-wide command is
      unsatisfiable because the repo carries 93 pre-existing broken links under `plans/done/`.

  **Gherkin (binds) →** "The schema and prerequisite-DAG surface builds and validates green"

  ```gherkin
  Scenario: The schema and prerequisite-DAG surface builds and validates green
    Given the course-paths pure core and the PathManifest schema are complete
    When nx run ayokoding-www:build, the affected test tiers, and the link and heading validators run
    Then the build and all affected tiers succeed
    And link, heading-hierarchy, and markdownlint validation report no errors
  ```

- [ ] [AI] **Verify the plan's own boundary held** — confirm no manifest data file, no `shell/`
      component, no course body and no `syllabus/` file was created or modified by this plan:
      `find apps/ayokoding-www/src/features/course-paths/manifests -name '*.yaml' | wc -l` returns
      **0**; `test -d apps/ayokoding-www/src/features/course-paths/shell` returns **non-zero**;
      `find plans/backlog/ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus -type f | wc -l`
      returns **128**
      — acceptance: all three hold. Falsifiable both ways: creating any one of those artefacts flips
      the corresponding check.

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes
> (Root Cause Orientation). Commit preexisting fixes separately with conventional-commit messages.

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [ ] [AI] Affected `typecheck` / `lint` / `test:quick` / `test:unit` / `test:integration` /
      `test:e2e` / `specs:behavior:coverage` exit 0, with only the recorded `course-paths` delta.
- [ ] [AI] `npx nx run ayokoding-www:build` exits 0; the pre-push form of `md links validate` prints
      `All links valid! No broken links found.`; `md heading-hierarchy validate` and `npm run lint:md`
      exit 0.
- [ ] [AI] Boundary check green: zero `.yaml` under `<MANIFESTS>`, no `<FEAT>shell/` directory, 128
      files under `syllabus/`.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged.

> **Pause Safety**: the whole data layer passes every automated gate and the plan's ownership
> boundary is proven intact. Safe to stop indefinitely. To resume: re-run the affected quality gates
> plus `npx nx run ayokoding-www:build`.

---

## Phase 4: Manual No-Regression Verification and Rule-15 Exemption Record

> Source: Phase 14 of `shared-course-library-and-learning-paths`, **scoped and inverted**. That phase
> walked a new user-facing feature. This plan ships none — so the manual step here is a targeted
> **no-regression sweep** proving the one shipped-code change (`contentUrl`'s optional `pathId`
> parameter and canonical URL shape, cycle 2.4) broke nothing that already renders.
>
> **Locale scope**: `ayokoding-www` supports **two** locales, `en` and `id` [Repo-grounded —
>
> > `SUPPORTED_LOCALES` in `apps/ayokoding-www/src/features/i18n/core/config.ts`]. `contentUrl` is
> > locale-parameterized, so a regression would hit **both**. Both are therefore verified. This is a
> > code-surface check, not a content walk-through — no `id` course content exists and none is expected.

- [ ] [AI] Confirm the supported locale set —
      `grep -n "SUPPORTED_LOCALES" apps/ayokoding-www/src/features/i18n/core/config.ts`
      — acceptance: prints a line declaring `["en", "id"]`; both locales are named in this phase's
      evidence filenames.
- [ ] [AI] Start dev server: `npx nx dev ayokoding-www` — acceptance: server up on its configured
      port (3101 per the repo's Web Sites table).
- [ ] [AI] For **each** locale (`en`, `id`) × **each** breakpoint (375 / 768 / 1280 px), via
      Playwright MCP `browser_navigate` + `browser_resize`: open the locale's learn section root
      (`/en/c/learn` and `/id/c/belajar`), open one existing content page beneath it, and follow its
      prev/next and breadcrumb links one hop each
      — acceptance: every page renders; every followed link resolves (no 404); `html[lang]` matches
      the locale under test.
- [ ] [AI] Check `browser_console_messages` on every page opened above
      — acceptance: **zero** console errors per locale per breakpoint. Falsifiable both ways: a
      single thrown error in link construction would surface here.
- [ ] [AI] Check `browser_network_requests` on the same pages
      — acceptance: no request returns 4xx or 5xx.
- [ ] [AI] Capture one screenshot per locale per breakpoint via `browser_take_screenshot`, saved to
      `evidence/phase-4-no-regression-<locale>-<breakpoint>px.png` (six files:
      `en`/`id` × 375/768/1280)
      — acceptance: `find plans/backlog/ayokoding-learning-path-02-schema-and-prerequisite-dag/evidence -name 'phase-4-no-regression-*.png' | wc -l`
      returns **6**. Falsifiable both ways: it returns 0 before this step.
- [ ] [AI] Reference each screenshot inline in this checklist as
      `![Learn section, <locale>, <breakpoint>px, unchanged after the contentUrl change](./evidence/phase-4-no-regression-<locale>-<breakpoint>px.png)`
      and note the console and network status per locale
      — acceptance: six image references present in this file, each with descriptive alt text.

### Rule-15 three-tester retest — exemption recorded

- [ ] [AI] **Record the Rule-15 exemption explicitly, with its reason**, in this checklist and in
      `evidence/phase-4-rule-15-exemption.txt`: _"This plan ships no rendered surface — six pure
      TypeScript modules, one directory with a README, one additive optional parameter on an existing
      pure function. There is no new screen, component, or user-facing flow for
      `web-exploratory-tester`, `web-usability-tester` or `web-design-tester` to explore. The
      three-tester retest is therefore not run. The no-regression sweep above is run instead and is
      not offered as a substitute for a retest of a surface this plan does not ship. The retest
      obligation for the path-aware navigation UI belongs to
      `ayokoding-learning-path-03-navigation-ui`."_
      — acceptance: the file exists, states the reason, and names the plan that carries the
      obligation instead. **The exemption is recorded, never silently omitted.**
- [ ] [AI] **Record the Rule-16 non-applicability** in the same file: this plan exposes no REST or
      GraphQL endpoint and adds no HTTP surface, so `api-exploratory-tester` is not applicable
      — acceptance: the statement is present in `evidence/phase-4-rule-15-exemption.txt`.

### Phase 4 Gate

> All checks below must pass before starting Phase 5.

- [ ] [AI] Both supported locales (`en`, `id`) verified at all three breakpoints; six screenshots
      present under `evidence/` and referenced inline with descriptive alt text.
- [ ] [AI] Zero console errors and zero 4xx/5xx responses across all twelve locale × breakpoint page
      loads.
- [ ] [AI] The Rule-15 exemption **and** the Rule-16 non-applicability are recorded with reasons in
      `evidence/phase-4-rule-15-exemption.txt`, each naming the plan that carries the obligation
      instead (or stating that none does).
- [ ] [AI] Draft PR opened (evidence + any fixes); 3-cycle PR-Review complete; CI green; PR
      `[AI]`-merged.

> **Pause Safety**: the one shipped-code change is proven non-regressive against both locales at
> three breakpoints, with committed evidence, and the tester exemptions are on the record rather than
> implied. Safe to stop indefinitely. To resume: restart `npx nx dev ayokoding-www` and re-open one
> page per locale.

---

## Phase 5: Final `origin/main` Integration and CI Verification

- [ ] [AI] Confirm no plan PR is still open —
      `gh pr list --search "ayokoding-learning-path-02-schema-and-prerequisite-dag" --state open`
      — acceptance: returns zero rows; every prior phase branch has been `[AI]`-merged to `main`.
- [ ] [AI] Sync the worktree to latest `origin/main` and run the full affected suite:
      `git fetch origin && git checkout main && git pull` then
      `npx nx affected -t typecheck lint test:quick test:unit test:integration test:e2e specs:behavior:coverage`
      and `npx nx run ayokoding-www:build`
      — acceptance: all exit 0 on the integrated `main`.
- [ ] [AI] Monitor the final `main` CI run — poll every ~2 minutes with one
      `gh run view --json status,conclusion` per wakeup; never tight-loop and never `gh run watch`
      — acceptance: all GitHub Actions green. Fix root causes and push follow-ups (own PR → 3-cycle
      review → `[AI]` merge) until green; never bypass a failing check.
- [ ] [AI] Confirm the downstream handoff signal holds on integrated `main` —
      `test -f apps/ayokoding-www/src/features/course-paths/core/schemas.ts` returns 0 AND
      `npx nx run ayokoding-www:typecheck` exits 0
      — acceptance: both hold. This is the exact precondition
      `ayokoding-learning-path-03-navigation-ui` and
      `ayokoding-learning-path-04-course-authoring` check before they start.

### Phase 5 Gate

> All checks below must pass before starting Phase 6.

- [ ] [AI] Zero open plan PRs; every prior phase merged to `main`.
- [ ] [AI] Full affected suite + `ayokoding-www:build` green on integrated `main`; final `main` CI run
      green.
- [ ] [AI] The downstream handoff signal (`schemas.ts` present AND `typecheck` exits 0) holds on
      `main`.

> **Pause Safety**: the whole data layer is integrated on `main` and green in CI, and the two Wave-2
> plans' start preconditions are satisfied. Safe to stop indefinitely. To resume: re-run the affected
> suite on `main` and check CI status.

---

## Phase 6: Knowledge Capture

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)._

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only if a durable surface would
      catch this automatically next time; discard the rest with a one-line reason
      — acceptance: every entry has either a route or a discard reason.
- [ ] [AI] Apply the **secret/sensitivity gate** to every surviving entry — sanitize any secret,
      credential, token, or private hostname to a `<placeholder>` token, or discard if unsanitizable
      — acceptance: `learnings.md` contains no raw secret.
- [ ] [AI] Apply the **repo-relevance gate** to every surviving entry — infra-private content
      (Terraform, k3s, Proxmox, real hostnames/inventories) stays in `ose-infra` only and is NEVER
      cross-routed into `ose-public`/`ose-primer`; public-governance content may propagate via the
      existing parity loop
      — acceptance: no infra-private content appears in this repo's routed output.
- [ ] [AI] Route each surviving learning to exactly one durable home per the open-ended routing
      matrix — non-code homes (`repo-governance/`, `docs/`, `.claude/agents/`, `.claude/skills/`, a
      post-mortem, or any other durable surface) may land inline for a small edit or as a
      `plans/backlog/` follow-up for a large one; **code homes (`apps/`, `libs/`, tests) are ALWAYS
      filed as a separate `plans/backlog/<slug>/` plan and NEVER landed inline** in this plan's own
      commits or PR. The sole carve-out is a blocker genuinely required to finish this plan's own
      scope, which is fixed inline as ordinary Root Cause Orientation work
      — acceptance: every `learnings.md` entry records its terminal routing state.
- [ ] [AI] If no generalizable learning surfaced, record the explicit escape in `learnings.md`:
      `No generalizable learnings — <one-line reason>`
      — acceptance: `learnings.md` is never silently empty.

### Phase 6 Gate

> All checks below must pass before starting Phase 7.

- [ ] [AI] Every `learnings.md` entry is in a terminal state (routed inline, filed as a
      `plans/backlog/` plan, or discarded with a reason), or the file records the explicit "none"
      escape.
- [ ] [AI] No code-homed learning landed inline in this plan's own commits or PR.
- [ ] [AI] Draft PR opened (`learnings.md` triage); 3-cycle PR-Review complete; CI green; PR
      `[AI]`-merged.

> **Pause Safety**: `learnings.md` is fully triaged (or explicitly recorded as empty); no future
> process depends on querying it later. Safe to stop indefinitely. To resume: re-read `learnings.md`
> and confirm every entry is terminal.

---

## Phase 7: Plan Archival and cross-plan link repoint

> **This archival is not routine.** This plan is Wave 1 and archives long before
> `ayokoding-learning-path-05-manifests` and `ayokoding-learning-path-04-course-authoring` finish.
> Its `git mv` relocates the target of every inbound cross-plan `syllabus/` link held by the other
> four plan folders — inherited from the source plan as **34** references across five files (README 8,
> `brd.md` 1, `prd.md` 2, `tech-docs.md` 8, `delivery.md` 15; **13 unique targets**), redistributed
> across those four folders by the split.
>
> **The repoint must land in the SAME commit as the `git mv`.** Nothing fails at commit time if it
> does not: `md links validate` does **not** run pre-commit. The `lint-staged` `*.md` chain is
> `prettier --write`, `markdownlint-cli2`, `md mermaid validate`, `md heading-hierarchy validate`,
> `md naming validate`, `md frontmatter validate` — **no link validation**. Link validation runs in
> the **pre-push** hook. So the blast radius is: the **next push** from any of the four surviving
> plans fails, for a reason having nothing to do with that push.

### 7.1 Pre-archival verification

- [ ] [AI] Verify ALL delivery checklist items in this file are ticked
      — acceptance: no unticked `- [ ]` remains outside this archival section.
- [ ] [AI] Verify the Knowledge Capture phase is complete — every `learnings.md` entry reached a
      terminal state or the explicit "none" escape is present; both safety gates were applied
      — acceptance: Phase 6 gate is fully ticked.
- [ ] [AI] Verify ALL quality gates pass (local + CI) and `npx nx run ayokoding-www:build` exits 0.
- [ ] [AI] Verify the manual no-regression evidence is committed —
      `find plans/backlog/ayokoding-learning-path-02-schema-and-prerequisite-dag/evidence -name 'phase-4-no-regression-*.png' | wc -l`
      returns **6**, covering both supported locales at all three breakpoints
      — acceptance: returns 6.
- [ ] [AI] Verify the Rule-15 exemption and Rule-16 non-applicability are on the record —
      `test -f plans/backlog/ayokoding-learning-path-02-schema-and-prerequisite-dag/evidence/phase-4-rule-15-exemption.txt`
      — acceptance: returns 0 and the file states both, with reasons. **There are no rule-15
      EWT/UWT/DWT findings to fix because the retest was exempted, not skipped** — the exemption is
      the artefact this check asserts.
- [ ] [AI] Verify the `syllabus/` corpus is byte-intact —
      `find plans/backlog/ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus -type f | wc -l`
      returns **128** AND
      `git diff --stat origin/main -- plans/backlog/ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus`
      prints nothing
      — acceptance: both hold. Falsifiable both ways: any edit under `syllabus/` makes the `git diff`
      print a stat line.
- [ ] [AI] Verify the plan's ownership boundary held to the end —
      `find apps/ayokoding-www/src/features/course-paths/manifests -name '*.yaml' | wc -l` returns
      **0** and `test -d apps/ayokoding-www/src/features/course-paths/shell` returns non-zero
      — acceptance: both hold.

### 7.2 Count the inbound cross-plan links (before the move)

- [ ] [AI] Record the pre-move inbound-link inventory to
      `evidence/phase-7-inbound-links-before.txt` via
      `grep -rn "ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus" plans/backlog plans/in-progress`
      — acceptance: the command prints **at least one** line (exit 0), and the captured line count is
      recorded as `N_BEFORE`. Falsifiable both ways: if it printed nothing, either the four sibling
      plans do not exist yet or they never linked in — both are conditions to investigate before
      moving, not to move through.
- [ ] [AI] Record the per-file breakdown by sibling plan folder in the same evidence file, so a
      reviewer can see all four plans are represented
      — acceptance: the evidence file names each sibling plan folder that holds at least one link.

### 7.3 Move and repoint — one commit

- [ ] [AI] Move the plan folder using today's completion date:
      `git mv plans/backlog/ayokoding-learning-path-02-schema-and-prerequisite-dag plans/done/YYYY-MM-DD__ayokoding-learning-path-02-schema-and-prerequisite-dag`
      (substitute today's date; the `evidence/` and `syllabus/` subfolders move with it)
      — acceptance: `test -d plans/done/YYYY-MM-DD__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus`
      returns 0 and `test -d plans/backlog/ayokoding-learning-path-02-schema-and-prerequisite-dag`
      returns non-zero.
- [ ] [AI] **In the same commit**, repoint every inbound cross-plan link in the other four plan
      folders from the sibling form
      `../ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/…`
      to the archived form
      `../../done/YYYY-MM-DD__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/…`
      (adjust the `../` depth if a sibling sits in `plans/in-progress/` rather than `plans/backlog/` —
      both are one level under `plans/`, so the depth is the same)
      — acceptance: `grep -rn "\.\./ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus" plans/backlog plans/in-progress`
      prints **nothing** and exits 1, AND
      `grep -rn "done/YYYY-MM-DD__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus" plans/backlog plans/in-progress`
      prints exactly `N_BEFORE` lines. Falsifiable both ways: leaving one link unrewritten makes the
      first command print it and exit 0.
- [ ] [AI] Run the link validator in **the pre-push hook's exact form** — command (single line):
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md links validate --exclude plans/done --exclude apps/ayokoding-www/content --exclude apps/ose-www/content`
      — acceptance: prints `All links valid! No broken links found.`
      **Two corrections, both verified.** (a) `md links validate` accepts **no positional path** —
      passing one fails with `error: unexpected argument '<path>' found` — and it cannot be scoped by
      `cd`-ing into a folder; it always walks the repo, so "run it in this plan's folder" is not
      expressible. (b) The bare repo-wide form is **unsatisfiable**: the repo carries **93
      pre-existing broken links**, all under `plans/done/`, unrelated to this work, so the unfiltered
      command always fails and this clause would block archival forever. The three `--exclude` flags
      above are the pre-push hook's own form, which is what actually gates a push.
      Note this excludes `plans/done`, so it does **not** catch a link pointing _into_ the new
      archived location being wrong; the two `grep` checks in the previous step are what catch that.
      **Both checks are required — neither alone is sufficient.**
- [ ] [AI] Update `plans/backlog/README.md` — remove this plan's entry
      — acceptance: `grep -qF "ayokoding-learning-path-02-schema-and-prerequisite-dag" plans/backlog/README.md`
      exits **1**.
- [ ] [AI] Update `plans/done/README.md` — add this plan's entry with today's completion date
      — acceptance: `grep -qF "ayokoding-learning-path-02-schema-and-prerequisite-dag" plans/done/README.md`
      exits **0**.
- [ ] [AI] Update any other README that references this plan (e.g. `plans/README.md`)
      — acceptance: the pre-push form of `md links validate` still prints
      `All links valid! No broken links found.`
- [ ] [AI] Commit the archival **and the repoint together**:
      `chore(plans): move ayokoding-learning-path-02-schema-and-prerequisite-dag to done`
      — acceptance: `git show --stat HEAD` lists both the moved plan folder **and** modified files in
      at least one sibling plan folder. Falsifiable both ways: a commit touching only the moved
      folder means the repoint was split out, which is exactly the failure this step exists to
      prevent.

### Phase 7 Gate

> All checks below must pass before the plan is considered complete.

- [ ] [AI] The plan folder is under `plans/done/YYYY-MM-DD__ayokoding-learning-path-02-schema-and-prerequisite-dag/`
      and its `syllabus/` still holds **128** files.
- [ ] [AI] Zero occurrences of the old sibling link form remain under `plans/backlog` or
      `plans/in-progress`, and the archived form appears exactly `N_BEFORE` times.
- [ ] [AI] The pre-push form of `md links validate` prints `All links valid! No broken links found.`
- [ ] [AI] `git show --stat HEAD` proves the `git mv` and the repoint landed in **one** commit.
- [ ] [AI] `plans/backlog/README.md`, `plans/done/README.md` and any other referencing README are
      updated.
- [ ] [AI] Draft PR opened (archival move + repoint); 3-cycle PR-Review complete; CI green; PR
      `[AI]`-merged.
- [ ] [AI] After the archival PR merges, prompt the user before deleting
      `worktrees/ayokoding-learning-path-02-schema-and-prerequisite-dag/`.

> **Pause Safety**: the plan is archived, its final PR is `[AI]`-merged to `main`, and every inbound
> cross-plan `syllabus/` link resolves to the new archived path. Terminal state. To resume: nothing —
> the plan is complete. To verify later: re-run the pre-push form of `md links validate` and confirm
> it still prints `All links valid! No broken links found.`

---

### Local Quality Gates (Before Every Push)

- [ ] [AI] `npx nx affected -t typecheck` exits 0.
- [ ] [AI] `npx nx affected -t lint` exits 0.
- [ ] [AI] `npx nx affected -t test:quick test:unit` exits 0 (add `test:integration test:e2e` for the
      phases touching `content-url.ts`).
- [ ] [AI] `npx nx affected -t specs:behavior:coverage` exits 0, or reports only the recorded
      `course-paths` delta.
- [ ] [AI] Fix ALL failures — including preexisting issues not caused by your changes (Root Cause
      Orientation).

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes.
> Commit preexisting fixes separately with appropriate conventional-commit messages.

### Note: plan location at archival time

This plan is created in `plans/backlog/ayokoding-learning-path-02-schema-and-prerequisite-dag/`.
When work starts it is promoted to
`plans/in-progress/ayokoding-learning-path-02-schema-and-prerequisite-dag/` — a pure move, no date
prefix on either stage. The `git mv` in Phase 7 then archives from wherever it sits to
`plans/done/YYYY-MM-DD__ayokoding-learning-path-02-schema-and-prerequisite-dag/` using the
completion date. Every path in Phase 7's steps is written against `plans/backlog/`; substitute
`plans/in-progress/` if the plan has been promoted by then.
