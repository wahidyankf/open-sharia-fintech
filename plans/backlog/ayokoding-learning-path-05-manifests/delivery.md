# Delivery Checklist — Learning Path Manifests

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
> Git-mechanical steps (worktree create/remove, branch, push, merge) are `[AI]`.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (safe-to-stop state + resume command). Each gate covers the phase's
> **content/data correctness** (tests, checkers, build) and its **integration** (draft PR opened,
> 3-cycle PR-Review, CI green, `[AI]` merge, `ayokoding-www` deployed). A phase is not complete until
> every gate check is green.

Two standing constraints govern every step below.

> **Cross-plan source of truth**: the authoritative per-course and per-path specs live in
> `plans/backlog/ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/`. Do not copy
> them; do not author from any other source.
>
> **The manifest ownership invariant (binding)**: this plan owns **every** file under `<MANIFESTS>`
> and every step that creates, appends to, reorders, or re-verifies one.
> `ayokoding-learning-path-04-course-authoring` owns course **bodies only** and never edits a
> manifest. A step here that authors a course body is a boundary violation in the other direction and
> is equally forbidden.

## Worktree

Worktree path: `worktrees/ayokoding-learning-path-05-manifests/`

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree ayokoding-learning-path-05-manifests
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the latest
`origin/main` when missing, syncs with `origin/main` before implementing, and prompts before deleting
the worktree after the plan is archived and pushed.

Every phase branches from the **latest `origin/main`** inside this one shared worktree
(`git fetch origin && git checkout main && git pull && git checkout -b ayokoding-learning-path-05-manifests/<phase-slug>`),
authors its work there, commits, pushes that branch, and opens **its own draft PR**.

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
   `git fetch origin && git checkout main && git pull && git checkout -b ayokoding-learning-path-05-manifests/<phase-slug>`.
2. [AI] Stage only this phase's paths (`git add <explicit paths>` — never `git add -A`), commit
   thematically (Conventional Commits, imperative, no period), push the branch, open a **draft PR**
   against `main` (`gh pr create --draft --base main ...`) — CI runs on the PR.
3. [AI] Run the **PR-Review Maker→Fixer Cycle** (3 sequential CI-gated cycles), resolve every finding,
   then `gh pr ready`.
4. [AI] **Merge** once all quality gates are green (typecheck, lint, `test:quick`, `test:unit`,
   `test:e2e` where affected, `specs:behavior:coverage`, CI, the 3-cycle review) — `[AI]` auto-merge
   per DN-11.
5. [AI] Dispatch `apps-ayokoding-www-deployer` to deploy `ayokoding-www` to `prod-ayokoding-www` — a
   no-op redeploy for plan-side-only phases.

## Depends-on and start preconditions

This plan is **Wave 3** and is **blocked by both Wave-2 plans**, not by the navigation plan alone.
Full rationale in
[README §The manifest ownership invariant](./README.md#the-manifest-ownership-invariant-now-scoped-per-category).

| Direction   | Plan (full folder name)                                               |
| ----------- | --------------------------------------------------------------------- |
| `blockedBy` | `ayokoding-learning-path-03-navigation-ui`                            |
| `blockedBy` | `ayokoding-learning-path-04-course-authoring`                         |
| `blockedBy` | `ayokoding-learning-path-01-url-restructure` (transitive)             |
| `blockedBy` | `ayokoding-learning-path-02-schema-and-prerequisite-dag` (transitive) |
| `blocks`    | _(none — terminal plan)_                                              |

All five start preconditions are verified in Phase 0 before any manifest work begins.

## Parallelization Model

**Cap**: honor the in-force subagent/PR-review concurrency cap (parallel-by-default, background
subagents capped per the orchestration convention). The main thread self-promotes nothing.

- **Phases 1 → 4 are strictly serial** and in DD-27's locked order (interview-ready → AI path →
  immediately-effective → fundamentally-strong). Each is a manifest+landing sync point, and each
  later phase's gate re-verifies every manifest published so far.
- **Phase 5 is serial per band** — each band's growth is a sync point (append + re-run
  prerequisite-consistency + integrity + no-forked-body).
- **Phases 6 → 10 are serial.**

**DAG width inside this plan is 1.** There is no fan-out here: every phase mutates or re-verifies the
same four data files. The parallelism the five-way split bought is _between_ plans, not within this
one.

## Path constants

Reproduced verbatim from the source plan. A plan missing this table is literally unreadable — every
acceptance clause below degrades to an unresolvable placeholder.

- `<COURSES>` = `apps/ayokoding-www/content/en/learn/courses/` (course bundles; served at `/en/learn/courses/<course-id>`)
- `<PATHS>` = `apps/ayokoding-www/content/en/learn/paths/` (thin path-landing anchors; served at `/en/learn/paths/<path-id>`)
- `<SE_OLD>` = `apps/ayokoding-www/content/en/learn/fundamentally-strong/software-engineer/` (legacy home of the 33 shipped topics + 4 existing capstones, incl. `capstone-solid-core` — the re-home source)
- `<FEAT>` = `apps/ayokoding-www/src/features/course-paths/`
- `<MANIFESTS>` = `<FEAT>manifests/` (standalone YAML data files, nested to mirror slash path ids — `<MANIFESTS><path-id>.yaml`)
- `<LEGACY>` = `apps/ayokoding-www/content/en/learn/legacy/` (**new bucket**, scope extension; served at `/en/learn/legacy/<domain>/…`)
- `<REDIR>` = `apps/ayokoding-www/src/redirects/`
- `<SPECS>` = `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/course-paths/`
- `<NAVSPECS>` = `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/navigation/` (existing domain — the three-bucket Gherkin lands beside `content-namespace-redirects.feature`)
- Path ids: `careers/interview-ready/software-engineer`, `careers/immediately-effective/software-engineer`, `careers/fundamentally-strong/software-engineer`, `careers/immediately-effective/ai-engineer` (fourth path, manifest at `<MANIFESTS>careers/immediately-effective/ai-engineer.yaml`)

One additional constant is owned by this plan: `<MANIFESTS>published-manifests.unit.test.ts` — the
unit-test file that asserts every published manifest's shape, integrity, and growth state. It lives
inside `<MANIFESTS>` because this plan owns that directory outright.

---

## Phase 0: Environment Setup and Baseline

> _Executor: `repo-setup-manager`_
>
> This phase verifies the **five start preconditions** as well as the toolchain. Unlike the other
> four split plans, this one cannot begin until **both** Wave-2 plans are merged — the navigation
> plan for the renderer and the course-authoring plan for the bodies. See
> [README §Implementation Sequence and Prerequisites](./README.md#implementation-sequence-and-prerequisites).

- [ ] [AI] Enter/provision the worktree and install dependencies in the root worktree: `npm install`
      — acceptance: exits 0, `node_modules/` synchronized.
- [ ] [AI] Converge the toolchain in the root worktree: `npm run doctor -- --fix`
      — acceptance: exits 0 with no unresolved drift.
- [ ] [AI] **Start precondition 1** — confirm the navigation plan is merged:
      `gh pr list --search "ayokoding-learning-path-03-navigation-ui" --state merged --json number --jq 'length'`
      — acceptance: returns a value ≥ 1. Falsifiable both ways: it returns `0` while that plan is
      still open.
- [ ] [AI] **Start precondition 2** — confirm the course-authoring plan is merged:
      `gh pr list --search "ayokoding-learning-path-04-course-authoring" --state merged --json number --jq 'length'`
      — acceptance: returns a value ≥ 1; returns `0` while that plan is still open.
- [ ] [AI] **Start precondition 3** — confirm the manifest repository exists:
      `test -f <FEAT>shell/manifest-repository.ts` — acceptance: exits 0 (returns non-zero on the
      current tree, where `<FEAT>` does not exist at all).
- [ ] [AI] **Start precondition 4** — confirm the manifest directory exists: `test -d <MANIFESTS>`
      — acceptance: exits 0; returns non-zero before the schema plan lands.
- [ ] [AI] **Start precondition 5** — confirm the full `careers/`-software-engineering catalog
      resolves (R5: 127 is the `careers/` catalog total, not a whole-programme total — the sibling
      `skills/` corpus is a separate corpus owned by `ayokoding-learning-path-06-skills-paths` and is
      not counted here): `find <COURSES> -maxdepth 1 -mindepth 1 -type d | wc -l`
      — acceptance: returns **127**. Falsifiable both ways: it returns **37** after the
      url-restructure plan's re-home alone, and the `find` fails outright before `<COURSES>` exists.
- [ ] [AI] Establish baselines: `npx nx run ayokoding-www:build` and
      `npx nx run ayokoding-www:test:unit` and `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: all exit 0; record the pass counts in `evidence/phase-0-snapshot.txt`.
- [ ] [AI] **Manifest baseline snapshot** — record the current manifest inventory to
      `evidence/phase-0-snapshot.txt` via
      `find <MANIFESTS>careers/ -name '*.yaml' | sort` — acceptance: the command prints **nothing** (no
      manifest exists yet) and the empty result is recorded. Falsifiable both ways: after Phase 4 the
      same command prints four paths.
- [ ] [AI] **Paths-hub baseline snapshot** — record the current `careers/` card count to
      `evidence/phase-0-snapshot.txt` via
      `grep -oE '/en/learn/paths/careers/[a-z-]+/[a-z0-9-]+' <PATHS>_index.md | sort -u | wc -l`
      — acceptance: returns **0** (the hub exists with an empty, category-grouped layout, created by
      the url-restructure plan); returns **4** after Phase 4. Scoped to `careers/` per R4, so a
      concurrent `skills/` card from `ayokoding-learning-path-06-skills-paths` cannot change this
      count. **Not** the older 2-segment pattern (`[a-z-]+/[a-z0-9-]+` with no `careers/` anchor) —
      that pattern under-counts because it stops matching at the first `/` inside a 3-segment
      `careers/<arc>/<role>` URL and collapses two different `immediately-effective/*` cards
      (`software-engineer` and `ai-engineer`) into one match under `sort -u` (DD-34).
- [ ] [AI] **Syllabus mirror reachability** — confirm the four authoritative orderings are readable
      at their cross-plan path:
      `ls ../ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/paths/manifest-*.md | wc -l`
      run from this plan's folder — acceptance: returns **4**. If the schema plan has archived,
      re-resolve the path under `plans/done/YYYY-MM-DD__…` and update every reference in this folder
      in the same commit.
- [ ] [AI] Resolve every preexisting failure before proceeding — acceptance: zero unresolved
      failures remain; each fix committed separately with its own conventional-commit message.
- [ ] [AI] Confirm `learnings.md` scaffold exists in the plan folder — acceptance: file present with
      its H1.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [ ] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift.
- [ ] [AI] All five start preconditions hold — both Wave-2 PRs merged, `manifest-repository.ts`
      present, `<MANIFESTS>` present, and `<COURSES>` holding **127** bundles.
- [ ] [AI] `ayokoding-www:build` + `:test:unit` + `ayokoding-www-fe-e2e:test:e2e` baselines recorded
      green in `evidence/phase-0-snapshot.txt`; zero preexisting failures unresolved.
- [ ] [AI] Manifest inventory recorded as empty; hub card count recorded as **0**; the four syllabus
      mirrors reachable at their cross-plan path.
- [ ] [AI] Draft PR opened; CI triggered; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged;
      `ayokoding-www` deployed (no-op redeploy).

> **Pause Safety**: only the toolchain was verified and the current state snapshotted — no manifest,
> landing, or hub change exists. Safe to stop indefinitely. To resume: re-run the five precondition
> checks and the three baselines.

---

## Phase 1: Author the interview-ready manifest, landing, and smoothness audit

> _Suggested executor: `apps-ayokoding-www-general-maker` (manifest + landing) + `web-researcher`
> (smoothness facts)._
>
> The **architecture smoke test** (DD-27). It ships against the 33 re-homed topics + 4 existing
> capstones already live under `<COURSES>`, proving routing, manifest loading, `?path` context
> propagation, prev/next, breadcrumb, and prerequisite display against real content. The four
> interview-technique courses (`coding-interview`, `take-home-and-live-coding`,
> `system-design-interview`, `behavioral-and-leadership-interviews`) plus `capstone-interview-loop`
> are **deliberately deferred** out of this manifest's published `courseOrder` and inserted in
> [Phase 5](#phase-5-manifest-growth-as-backfill-lands) — recorded here as a documented gap, not an
> oversight.

### 1.1 · TDD cycle A — publish the manifest data file

- [ ] [AI] **RED** — create `<MANIFESTS>published-manifests.unit.test.ts` _(new file, this plan owns
      `<MANIFESTS>`)_ with a failing assertion that
      `<MANIFESTS>careers/interview-ready/software-engineer.yaml` loads, zod-validates against
      `<FEAT>core/schemas.ts`, and passes `checkManifestIntegrity` +
      `checkPrerequisiteConsistency` — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the new assertion **fails** with a module-not-found or empty-glob error naming
      `careers/interview-ready/software-engineer.yaml`. A failure for any other reason (a missing
      `schemas.ts` import, for instance) means a start precondition was not honoured — stop and
      re-check Phase 0.

  **Gherkin (binds) →** "The interview-ready MVP proves the architecture before other path work begins"

  ```gherkin
  Scenario: The interview-ready MVP proves the architecture before other path work begins
    Given the careers/interview-ready/software-engineer MVP (an architecture smoke test over already-live topics 1-33) is delivered end-to-end
    When the careers/immediately-effective/ai-engineer path's authoring begins
    Then the interview-ready MVP's landing page, manifest, and path-aware nav are already live in production
    And the interview cluster's remaining NEW courses are not required for that MVP to be considered shipped
  ```

- [ ] [AI] **GREEN** — author `<MANIFESTS>careers/interview-ready/software-engineer.yaml` _(new file)_ with
      `pathId: careers/interview-ready/software-engineer`, a `title`, a `description`, and an ordered
      `courseOrder` transcribed from
      [`../ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/paths/manifest-interview-ready-software-engineer.md`](../ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/paths/manifest-interview-ready-software-engineer.md),
      **restricted to the 33 re-homed topics + 4 existing capstones already live under `<COURSES>`**
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0, AND the five deferred IDs are absent —
      `grep -oE 'coding-interview|take-home-and-live-coding|system-design-interview|behavioral-and-leadership-interviews|capstone-interview-loop' <MANIFESTS>careers/interview-ready/software-engineer.yaml | sort -u | wc -l`
      returns **0**. Falsifiable both ways: after Phase 5's Band-9 growth the same command must
      return **5**.
- [ ] [AI] **REFACTOR** — align the YAML's key order and comment style with the schema plan's
      documented example, and factor the shared load-and-validate helper in
      `<MANIFESTS>published-manifests.unit.test.ts` so each later manifest adds one line rather than a
      copied block — command: `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:lint`
      — acceptance: both exit 0 and no assertion was weakened (the deferred-ID check still returns 0).

### 1.2 · The landing anchor (content — maker/checker/fixer, not TDD)

- [ ] [AI] Author `<PATHS>careers/interview-ready/software-engineer/_index.md` _(new file)_ — prose and SEO
      only: the arc narrative, the persona fast-path affordance ("experienced and job-hunting? start
      at Phase 1"), and the phase-boundary bridge paragraph. **No `courseOrder` in the landing** — the
      ordered list renders from the loaded manifest — acceptance: the file contains no `courseOrder`
      key (`grep -oE 'courseOrder' <PATHS>careers/interview-ready/software-engineer/_index.md | wc -l` returns
      **0**, and returns **1** if one is mistakenly added), and the landing renders the
      manifest-ordered list.
  - _Suggested executor: `apps-ayokoding-www-general-maker`_
- [ ] [AI] Run `apps-ayokoding-www-link-checker` and `apps-ayokoding-www-general-checker` over the new
      landing — acceptance: findings recorded.
- [ ] [AI] Apply the matching fixer to every CRITICAL/HIGH/MEDIUM finding — acceptance: zero
      CRITICAL/HIGH/MEDIUM remain on re-run.
- [ ] [AI] Populate the first paths-hub card in `<PATHS>_index.md` _(existing file, created by
      `ayokoding-learning-path-01-url-restructure`)_ — add the `interview-ready` card to the 2×2
      grid, leaving the remaining three slots present but unpopulated — acceptance:
      `grep -oE '/en/learn/paths/careers/[a-z-]+/[a-z0-9-]+' <PATHS>_index.md | sort -u | wc -l` returns
      **1** (returns **0** before this step).

### 1.3 · TDD cycle B — old-way and new-way coexistence

- [ ] [AI] **RED** — add the coexistence scenario to
      `<SPECS>path-composition.feature` _(new file)_ and a failing e2e step in
      `apps/ayokoding-www-fe-e2e/src/steps/course-paths.steps.ts` _(existing file, created by
      `ayokoding-learning-path-03-navigation-ui`)_ asserting that a course reached from this path's
      landing and the same course reached through the legacy section-index browse resolve to one
      canonical body — command: `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: the new spec **fails** because the path landing does not yet link that course.

  **Gherkin (binds) →** "A path landing and the legacy browse resolve to the same canonical body"

  ```gherkin
  Scenario: A path landing and the legacy browse resolve to the same canonical body
    Given a course lives at its canonical /en/learn/courses/<course-id> URL and appears in a published path manifest
    When a reader reaches that course from the path landing at /en/learn/paths/<path-id>
    And another reader reaches it through the legacy section-index browse
    Then both routes resolve to the same single canonical course body
    And neither route serves a duplicated or forked copy of that body
  ```

- [ ] [AI] **GREEN** — implement the step bindings against the published manifest and the live
      landing — command:
      `npx nx run ayokoding-www:specs:behavior:coverage && npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: both exit 0.
- [ ] [AI] **REFACTOR** — extract the repeated "resolve a course two ways" helper into a single step
      definition reused by later phases — command: `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: exits 0 and the scenario count is unchanged.

### 1.4 · Architecture smoke test and smoothness audit

- [ ] [AI] **Architecture smoke test** — against this real manifest verify the six things DD-27
      names: routing resolves, the manifest loads, `?path=careers/interview-ready/software-engineer` context
      propagates, prev/next walks the manifest order, the breadcrumb shows the path, and course pages
      show their prerequisites — command: `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: the path-walk e2e spec passes in `en` (this plan's content locale).
- [ ] [AI] **Progression smoothness audit (interview-first, DD-16, smoke-test-scoped)** — walk the
      published `courseOrder` and confirm the levers hold (prereq-chaining; monotonic-ish difficulty;
      skip/fast-path affordance on the landing) per
      [tech-docs §Smoothness Architecture](./tech-docs.md#smoothness-architecture-per-path)
      — acceptance: every lever assessable over the current `courseOrder` is verified; any regression
      is fixed by softening or bridging **in place, never by reordering**. The **refresh-register**
      lever lives inside the four deferred interview courses and is **not yet assessable** — it is
      audited in Phase 5, not fabricated here. Record the deferral in this checklist.
  - _Suggested executor: `web-researcher` for any external claim in the bridge prose_

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [ ] [AI] `find <MANIFESTS>careers/ -name '*.yaml' | wc -l` returns **1** (returns **0** before this phase).
- [ ] [AI] `npx nx run ayokoding-www:test:unit` exits 0 — manifest loads, zod-validates, integrity and
      prerequisite-consistency green.
- [ ] [AI] `grep -oE 'coding-interview|take-home-and-live-coding|system-design-interview|behavioral-and-leadership-interviews|capstone-interview-loop' <MANIFESTS>careers/interview-ready/software-engineer.yaml | sort -u | wc -l`
      returns **0** — the deferral is real and is recorded, not silently closed.
- [ ] [AI] `npx nx run ayokoding-www:build` + `:specs:behavior:coverage` **and**
      `npx nx run ayokoding-www-fe-e2e:test:e2e` exit 0. (`ayokoding-www:test:e2e` and
      `:test:integration` are no-op echoes and can never fail — omitted deliberately.)
- [ ] [AI] `grep -oE '/en/learn/paths/careers/[a-z-]+/[a-z0-9-]+' <PATHS>_index.md | sort -u | wc -l`
      returns **1**.
- [ ] [AI] Smoothness audit passes for every assessable lever; the refresh-register deferral is
      written into this checklist.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the `careers/interview-ready/software-engineer` path is live end-to-end in production over
> its smoke-test-scoped `courseOrder` — **the architecture is proven against real content**. The other
> three manifests do not exist and nothing references them, so the hub and every course page are
> coherent. Safe to stop indefinitely. To resume: `npx nx run ayokoding-www-fe-e2e:test:e2e`.

---

## Phase 2: Author the AI-path manifest, landing, and smoothness audit

> _Suggested executor: `apps-ayokoding-www-general-maker` (manifest + landing) + `web-researcher`
> (smoothness facts)._
>
> `careers/immediately-effective/ai-engineer` — **authoring priority #1** behind the
> smoke-test MVP (DD-27). This path is **from-scratch** (DD-35, 2026-07-21 ruling): it assumes **no**
> prior software-engineering competence, so its shared SWE-**fundamentals** prerequisites are
> **included** at the head of `courseOrder`, not linked out (DD-24's "linked, not included" framing is
> superseded for this path). Per **DD-33** (still holding in scope) this path's `courseOrder` also
> **walks**, never links, the existing nine-course AI/harness cluster, plus the six new
> AI-engineer-role courses. The path's **full** composition is therefore no longer a fixed "15
> courses" figure — it is the (still-being-ordered) included SWE-fundamentals set **plus** the
> walked AI/harness cluster **plus** the six new AI-engineer-role courses; see DD-35 for why this
> plan does not fabricate a total.
>
> **Cross-plan dependency (new, 2026-07-21):** the prerequisite-consistent stage-by-stage ordering of
> the included SWE-fundamentals set is authored by
> `ayokoding-learning-path-02-schema-and-prerequisite-dag`'s own delivery Phase 1.4, not this plan's.
> This phase's GREEN step **transcribes** that ordering from the corrected syllabus mirror once Phase
> 1.4 lands it; if Phase 1.4 has not landed by the time this phase is reached, this phase blocks on it
> rather than inventing an order — the same transcribe-never-re-derive rule this plan applies to every
> other manifest.
>
> This phase also **absorbs the manifest re-verification step** the source plan placed in its
> course-surgery phase. That step was read-only by its own acceptance text, but it re-verifies a
> manifest this plan authored and would invert the wave order if left upstream. It is folded into
> this phase's gate rather than duplicated, because the gate already re-runs both integrity checks
> across every manifest published so far.

### 2.1 · TDD cycle — publish the manifest data file

- [ ] [AI] **RED** — extend `<MANIFESTS>published-manifests.unit.test.ts` with a failing assertion
      that `<MANIFESTS>careers/immediately-effective/ai-engineer.yaml` loads, zod-validates, and
      contains the shared SWE-fundamentals prerequisite course IDs **at the head of** `courseOrder`
      (present, not absent — inverted 2026-07-21, DD-35) — command:
      `npx nx run ayokoding-www:test:unit`
      — acceptance: the new assertion **fails** because the manifest file does not exist; the Phase-1
      assertions still pass in the same run.

  **Gherkin (binds) →** "The AI-engineer path includes its software-engineering prerequisites instead
  of linking them"

  ```gherkin
  Scenario: The AI-engineer path includes its software-engineering prerequisites instead of linking them
    Given the careers/immediately-effective/ai-engineer path manifest is published
    When a reader with no prior software-engineering competence inspects its courseOrder
    Then the shared software-engineering-fundamentals courses this path's AI-specific spine depends on are present at the head of courseOrder, ordered prerequisite-consistently
    And that reader can start at courseOrder[0] and finish the whole path from this one manifest, with no external prerequisite link required
  ```

- [ ] [AI] **GREEN** — author
      `<MANIFESTS>careers/immediately-effective/ai-engineer.yaml` _(new file)_ with
      `pathId: careers/immediately-effective/ai-engineer`, a `title`, a `description`, and an ordered
      `courseOrder` whose **head** is the prerequisite-consistent ordering of the included
      SWE-fundamentals set — transcribed verbatim (never re-derived) from
      [`../ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/paths/manifest-immediately-effective-ai-engineer.md`](../ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/paths/manifest-immediately-effective-ai-engineer.md)'s
      Stage 0 once that plan's own Phase 1.4 lands it — at minimum the 11 named courses
      `just-enough-python`, `software-testing`, `cicd-and-release-engineering`, `backend-at-scale`,
      `containers-and-orchestration`, `computer-architecture`, `site-reliability-engineering`,
      `data-engineering`, `data-structures-and-algorithms-essentials`, `software-product-engineering`,
      `frontend-essentials` (the mirror itself notes the closure is likely larger once each course's
      own transitive prerequisites are added) — **followed by** the six net-new AI-engineer-role
      courses in the previously established order (light eval gate → statistics for evals → deep
      evals → product patterns for probabilistic systems → inference serving and model deployment →
      fine-tuning and adaptation) — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0, AND all 11 named SWE-fundamentals IDs are present —
      `grep -oE 'just-enough-python|software-testing|cicd-and-release-engineering|backend-at-scale|containers-and-orchestration|computer-architecture|site-reliability-engineering|data-engineering|data-structures-and-algorithms-essentials|software-product-engineering|frontend-essentials' <MANIFESTS>careers/immediately-effective/ai-engineer.yaml | sort -u | wc -l`
      returns **11** or more (returns **0** before this step — inverted from the pre-2026-07-21 "must
      return 0" acceptance), AND all six AI-engineer-role spine members are present —
      `grep -oE 'evaluating-ai-output-essentials|statistics-for-evaluation|evaluating-ai-systems-in-depth|product-patterns-for-probabilistic-systems|inference-serving-and-model-deployment|fine-tuning-and-adaptation' <MANIFESTS>careers/immediately-effective/ai-engineer.yaml | sort -u | wc -l`
      returns **6**, AND `checkPrerequisiteConsistency` passes over the combined order (the automated
      topological check, not a manual grep, is authoritative for inter-course ordering). If plan 02's
      Phase 1.4 has not landed the Stage 0 ordering yet, this step blocks rather than inventing one.
- [ ] [AI] **REFACTOR** — record inline in the YAML, as a comment, that the nine AI/harness-cluster
      IDs are deliberately absent pending Phase 5 growth (DD-33), naming the phase — command:
      `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:lint`
      — acceptance: both exit 0 and the SWE-fundamentals-present and six-AI-member checks above still
      hold.

### 2.2 · The landing anchor (content — maker/checker/fixer, not TDD)

- [ ] [AI] Author `<PATHS>careers/immediately-effective/ai-engineer/_index.md`
      _(new file)_ — prose and SEO only, framing the path as **from-scratch**: no prior
      software-engineering competence assumed, and the SWE-fundamentals courses a reader needs are
      already the first courses in this path's own `courseOrder` (DD-35, inverted 2026-07-21 — the
      landing no longer needs to link out to those prerequisites, since the manifest includes them) —
      acceptance: the landing prose describes the path's endpoint (**building AI systems**) without
      naming or assuming an already-working-software-engineer starting persona
      (`grep -c -i 'already[- ]working\|transitioning\|role transition\|switcher' <PATHS>careers/immediately-effective/ai-engineer/_index.md`
      returns **0**), and it contains no `courseOrder` key.
  - _Suggested executor: `apps-ayokoding-www-general-maker`_
- [ ] [AI] Run `apps-ayokoding-www-link-checker` and `apps-ayokoding-www-general-checker` over the new
      landing; apply the matching fixer to every CRITICAL/HIGH/MEDIUM finding — acceptance: zero
      CRITICAL/HIGH/MEDIUM remain on re-run.
- [ ] [AI] Populate the second paths-hub card (`AI Engineer` — endpoint-named, not
      `SWE → AI Engineer`, per the 2026-07-21 rename: the path no longer assumes a starting role, so
      it is described by its endpoint only) in `<PATHS>_index.md` —
      acceptance: `grep -oE '/en/learn/paths/careers/[a-z-]+/[a-z0-9-]+' <PATHS>_index.md | sort -u | wc -l`
      returns **2** (returned **1** after Phase 1).

### 2.3 · Verification, build order, and smoothness

- [ ] [AI] Verify path-aware nav end-to-end for this path: from the landing, prev/next walks the
      manifest order and preserves `?path=careers/immediately-effective/ai-engineer`;
      the breadcrumb shows the path; course pages show their prerequisites — command:
      `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: the path-walk e2e spec passes in `en`.
- [ ] [AI] **Record the build-order assertion (documentation-verified, not harness-executable).**
      Confirm by reading this checklist that Phase 1 (interview-ready MVP) precedes this phase, and
      that Phases 3 and 4 (the `immediately-effective` and `fundamentally-strong` manifests) follow
      it — acceptance: the phase ordering in this file matches DD-27, stated here in writing. This is
      a build-order claim about this plan's own delivery sequence; no test harness can execute it,
      and it is kept deliberately per
      [README §JC-1](./README.md#jc-1-the-build-order-scenario-is-kept-not-deleted).

  **Gherkin (binds) →** "The AI path is authored before the other two manifests are composed"

  ```gherkin
  Scenario: The AI path is authored before the other two manifests are composed
    Given the interview-ready MVP has shipped
    When authoring effort is allocated across the remaining paths
    Then the careers/immediately-effective/ai-engineer path's six net-new AI-engineer-role courses (DD-28) and manifest are authored first
    And the careers/immediately-effective/software-engineer and careers/fundamentally-strong/software-engineer manifests are composed only afterward
  ```

- [ ] [AI] **Progression smoothness audit (from-scratch-first, DD-16, re-labeled 2026-07-21 — was
      "AI-transition-first")** — walk the manifest order and
      confirm the levers hold (prereq-chaining; monotonic-ish difficulty; the light-eval-gate versus
      deep-evals scope boundary is not itself a smoothness break) per
      [tech-docs §Smoothness Architecture](./tech-docs.md#smoothness-architecture-per-path)
      — acceptance: all assessable levers verified; any regression fixed by softening or bridging in
      place, never by reordering.
- [ ] [AI] **Absorbed step — re-verify every manifest published so far.** Re-run
      `checkManifestIntegrity` + `checkPrerequisiteConsistency` across both published manifests
      (`careers/interview-ready/software-engineer` and this one) — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: exits 0. This closes the re-verification the
      source plan placed in its course-surgery phase; it lands here because it re-verifies manifests
      this plan authored and would otherwise invert the wave order.

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [ ] [AI] `find <MANIFESTS>careers/ -name '*.yaml' | wc -l` returns **2**.
- [ ] [AI] The six-AI-member spine check returns **6** and the SWE-fundamentals-presence check returns
      **11 or more** (inverted 2026-07-21 — the old "leak check returns 0" acceptance is superseded).
- [ ] [AI] `npx nx run ayokoding-www:test:unit` exits 0 — integrity and prerequisite-consistency green
      across **both** published manifests, not only the new one.
- [ ] [AI] `npx nx run ayokoding-www:build` + `:specs:behavior:coverage` **and**
      `npx nx run ayokoding-www-fe-e2e:test:e2e` exit 0.
- [ ] [AI] Hub card count returns **2**; the landing frames the path as from-scratch with no
      already-working-software-engineer persona named (the SWE-fundamentals-leak-of-persona-language
      grep above returns **0**).
- [ ] [AI] The build-order assertion is recorded in writing, with its non-executability stated.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the AI path is live end-to-end in production over its smoke-test-scoped starting
> composition (included SWE-fundamentals prerequisites at the head of `courseOrder`, plus whichever
> of the six new AI-engineer-role courses exist by this point) — DD-27's authoring priority #1 is
> delivered. Both published manifests validate; the hub shows two of four cards and no placeholder.
> Safe to stop indefinitely. To resume:
> `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www-fe-e2e:test:e2e`.

---

## Phase 3: Author the immediately-effective manifest, landing, and smoothness audit

> _Suggested executor: `apps-ayokoding-www-general-maker`._
>
> Adds **no new course body** — it composes existing library courses into the immediately-effective
> arc (editor → one language → **build a real app first** → then deepen). Authored over the
> currently-available library and grown through Bands 1–8 in Phase 5. This manifest **omits the
> interview-technique band by design** (DL-13) and therefore does **not** grow at Band 9.

### 3.1 · TDD cycle — publish the manifest data file

- [ ] [AI] **RED** — extend `<MANIFESTS>published-manifests.unit.test.ts` with a failing assertion
      that `<MANIFESTS>careers/immediately-effective/software-engineer.yaml` loads, zod-validates, passes both
      integrity gates, and places the build-a-real-app capstone before every pure-theory course —
      command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the new assertion **fails** because the manifest file does not exist; the Phase-1
      and Phase-2 assertions still pass in the same run.

  **Gherkin (binds) →** "The immediately-effective path is build-app-first"

  ```gherkin
  Scenario: The immediately-effective path is build-app-first
    Given the careers/immediately-effective/software-engineer path manifest is published
    When a reader walks the path
    Then editor/tooling, one language end-to-end, and building a real app precede the CS-fundamentals and DS&A courses
    And the reader ships a real deployed app before any pure-theory course
  ```

- [ ] [AI] **GREEN** — author `<MANIFESTS>careers/immediately-effective/software-engineer.yaml` _(new file)_
      with `pathId: careers/immediately-effective/software-engineer`, a `title`, a `description`, and an
      ordered `courseOrder` transcribed from
      [`../ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/paths/manifest-immediately-effective-software-engineer.md`](../ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/paths/manifest-immediately-effective-software-engineer.md)
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0, AND the build-before-theory ordering holds:
      `awk '/^courseOrder:/{f=1;next} f&&/^ *- /{n++; if ($2=="capstone-full-stack-app") print "app@"n; if ($2=="computer-science-foundations") print "theory@"n}' <MANIFESTS>careers/immediately-effective/software-engineer.yaml`
      prints the `app@` line **before** the `theory@` line. Falsifiable both ways: a theory-first
      ordering prints them in the opposite order, and the command prints nothing at all if either ID
      is missing (which itself fails the check).
- [ ] [AI] **REFACTOR** — deduplicate the load-and-validate helper now that three manifests share it,
      and confirm no assertion was weakened — command:
      `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:lint`
      — acceptance: both exit 0 and all three manifests' assertions still run.

### 3.2 · The landing anchor and hub card (content — maker/checker/fixer)

- [ ] [AI] Author `<PATHS>careers/immediately-effective/software-engineer/_index.md` _(new file)_ — prose and
      SEO only, including the "already know a language? jump to Build A Real App" fast-path affordance
      and the "you shipped; now understand why it worked" bridge paragraph at the shipping → CS-depth
      boundary — acceptance: the landing contains no `courseOrder` key and renders the
      manifest-ordered arc.
  - _Suggested executor: `apps-ayokoding-www-general-maker`_
- [ ] [AI] Run `apps-ayokoding-www-link-checker` and `apps-ayokoding-www-general-checker`; apply the
      matching fixer to every CRITICAL/HIGH/MEDIUM finding — acceptance: zero CRITICAL/HIGH/MEDIUM
      remain on re-run.
- [ ] [AI] Populate the third paths-hub card in `<PATHS>_index.md` — acceptance:
      `grep -oE '/en/learn/paths/careers/[a-z-]+/[a-z0-9-]+' <PATHS>_index.md | sort -u | wc -l` returns
      **3** (returned **2** after Phase 2).

### 3.3 · Verification and smoothness

- [ ] [AI] Verify path-aware nav: prev/next walks the immediately-effective order and preserves
      `?path=careers/immediately-effective/software-engineer`; a course shared with `interview-ready` shows the
      correct neighbour **per active path** — command: `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: e2e passes in `en`, and a shared course's prev/next differs by active path
      (asserting the same neighbour under both paths would fail the spec).
- [ ] [AI] **Manifest integrity + prerequisite-consistency + no-forked-body check** across all three
      published manifests — command: `npx nx run ayokoding-www:test:unit` — acceptance: exits 0.
- [ ] [AI] **Progression smoothness audit (shipping-first, DD-16)** — build-a-real-app precedes CS
      depth; the bridge is present on the landing; prereq-chaining holds — acceptance: levers verified;
      regressions fixed by softening or bridging in place, never by reordering.

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [ ] [AI] `find <MANIFESTS>careers/ -name '*.yaml' | wc -l` returns **3**.
- [ ] [AI] The build-before-theory ordering check prints `app@` before `theory@`.
- [ ] [AI] `npx nx run ayokoding-www:test:unit` exits 0 — integrity, prerequisite-consistency, and
      no-forked-body green across all three published manifests.
- [ ] [AI] `npx nx run ayokoding-www:build` + `:specs:behavior:coverage` **and**
      `npx nx run ayokoding-www-fe-e2e:test:e2e` exit 0.
- [ ] [AI] Hub card count returns **3**; a shared course's prev/next provably differs by active path.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: three of the four paths are live over one shared library with zero body
> duplication. Every published manifest validates. Safe to stop indefinitely. To resume: re-run all
> path-walk e2e specs published so far.

---

## Phase 4: Author the fundamentally-strong manifest, landing, and smoothness audit

> _Suggested executor: `apps-ayokoding-www-general-maker`._
>
> The university-style path (fundamentals / CS-theory FIRST → deeper). Adds **no new course body**.
> This is the **first point at which all three software-engineer manifests exist**, so it is where the
> shared-course/no-duplication scenario and the "names every path that includes it" scenario become
> satisfiable — both are anchored at this phase's gate.

### 4.1 · TDD cycle A — publish the manifest data file

- [ ] [AI] **RED** — extend `<MANIFESTS>published-manifests.unit.test.ts` with a failing assertion
      that `<MANIFESTS>careers/fundamentally-strong/software-engineer.yaml` loads, zod-validates, and places
      CS foundations / computer architecture / paradigms / DS&A before the build-real-software courses
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the new assertion **fails** because the manifest file does not exist; the three
      prior manifests' assertions still pass in the same run.

  **Gherkin (binds) →** "The fundamentally-strong path is fundamentals-first"

  ```gherkin
  Scenario: The fundamentally-strong path is fundamentals-first
    Given the careers/fundamentally-strong/software-engineer path manifest is published
    When a reader walks the path
    Then CS foundations, computer architecture, paradigms, and DS&A precede the build-real-software courses
    And the ordering is a valid topological entry into the prerequisite DAG
  ```

- [ ] [AI] **GREEN** — author `<MANIFESTS>careers/fundamentally-strong/software-engineer.yaml` _(new file)_
      with `pathId: careers/fundamentally-strong/software-engineer`, a `title`, a `description`, and an
      ordered `courseOrder` transcribed from
      [`../ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/paths/manifest-fundamentally-strong-software-engineer.md`](../ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/paths/manifest-fundamentally-strong-software-engineer.md)
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0, AND the theory-first ordering holds:
      `awk '/^courseOrder:/{f=1;next} f&&/^ *- /{n++; if ($2=="computer-science-foundations") print "theory@"n; if ($2=="capstone-full-stack-app") print "app@"n}' <MANIFESTS>careers/fundamentally-strong/software-engineer.yaml`
      prints the `theory@` line **before** the `app@` line — the exact inverse of Phase 3's check
      against the same two IDs, so a copy-paste of the wrong arc fails immediately.
- [ ] [AI] **REFACTOR** — assert the two orderings are inverses of each other in a single shared test
      helper, so a future edit to either manifest that collapses the distinction fails loudly —
      command: `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:lint`
      — acceptance: both exit 0.

### 4.2 · TDD cycle B — no forked body across the three software-engineer paths

- [ ] [AI] **RED** — add the shared-course scenario to `<SPECS>path-composition.feature` and a failing
      assertion in `<MANIFESTS>published-manifests.unit.test.ts` that every course ID appearing in
      more than one of the three software-engineer manifests resolves to **exactly one** directory
      under `<COURSES>` — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the new assertion **fails** before the check is implemented.

  **Gherkin (binds) →** "The three software-engineer paths reference a shared course with no body
  duplication"

  ```gherkin
  Scenario: The three software-engineer paths reference a shared course with no body duplication
    Given a course appears in all three of the interview-ready, careers/immediately-effective/software-engineer, and careers/fundamentally-strong/software-engineer manifests
    When the course library is inspected
    Then exactly one canonical path-neutral body exists for that course
    And each manifest references the course by its stable course ID
  ```

- [ ] [AI] **GREEN** — implement the no-forked-body check — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: exits 0, AND the shell equivalent agrees:
      `for id in $(cat <MANIFESTS>*/*.yaml | grep -oE '^ *- [a-z0-9-]+' | sed 's/^ *- //' | sort -u); do find <COURSES> -maxdepth 1 -mindepth 1 -type d -name "$id" | wc -l; done | sort -u`
      prints exactly the single line `1`. Falsifiable both ways: a dangling ID prints a `0` line and a
      forked body prints a `2` line, so any output other than a lone `1` fails.
- [ ] [AI] **REFACTOR** — move the shell equivalent into the test as a documented comment so the two
      checks cannot drift — command: `npx nx run ayokoding-www:test:unit` — acceptance: exits 0.

### 4.3 · TDD cycle C — a shared course names every path that includes it

- [ ] [AI] **RED** — add the affordance scenario to `<SPECS>path-composition.feature` and a failing
      e2e step in `apps/ayokoding-www-fe-e2e/src/steps/course-paths.steps.ts` asserting that a course
      present in more than one manifest, opened with **no** `?path=`, lists every including path in
      the "this course is part of" affordance — command: `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: the new spec **fails** because the affordance currently enumerates fewer paths
      than are published.

  **Gherkin (binds) →** "A shared course names every path that includes it"

  ```gherkin
  Scenario: A shared course names every path that includes it
    Given all four path manifests are published and a course appears in more than one of them
    When a reader opens that course's canonical URL with no path context
    Then the "this course is part of" affordance lists every published path whose manifest includes the course
    And each listed path links to its own path landing page
  ```

- [ ] [AI] **GREEN** — implement the step bindings against all four published manifests — command:
      `npx nx run ayokoding-www:specs:behavior:coverage && npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: both exit 0. The affordance must enumerate published manifests at build time, not
      a hand-written list — a hard-coded list passes today and goes stale at the first growth.
- [ ] [AI] **REFACTOR** — remove any duplication between this step definition and Phase 1's
      two-ways-to-one-body helper — command: `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: exits 0 and the scenario count is unchanged.

### 4.4 · Landing, hub completion, verification, and smoothness

- [ ] [AI] Author `<PATHS>careers/fundamentally-strong/software-engineer/_index.md` _(new file)_ — prose and
      SEO only, including the "have a CS degree? skim Stage 2" fast-path affordance and the
      theory → application bridge — acceptance: the landing contains no `courseOrder` key and renders
      the fundamentals-first arc.
  - _Suggested executor: `apps-ayokoding-www-general-maker`_
- [ ] [AI] Run `apps-ayokoding-www-link-checker` and `apps-ayokoding-www-general-checker`; apply the
      matching fixer to every CRITICAL/HIGH/MEDIUM finding — acceptance: zero CRITICAL/HIGH/MEDIUM
      remain on re-run.
- [ ] [AI] Populate the **fourth and final** paths-hub card in `<PATHS>_index.md`, completing the 2×2
      grid — acceptance:
      `grep -oE '/en/learn/paths/careers/[a-z-]+/[a-z0-9-]+' <PATHS>_index.md | sort -u | wc -l` returns
      **4** (returned **3** after Phase 3).
- [ ] [AI] Verify path-aware nav: prev/next walks the fundamentals-first order and preserves
      `?path=careers/fundamentally-strong/software-engineer`; a course shared across paths shows the correct
      neighbour per active path — command: `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: e2e passes in `en`.
- [ ] [AI] **Progression smoothness audit (fundamentals-first, DD-16)** — theory precedes application;
      the why-before-how bridges are present; prereq-chaining holds — acceptance: levers verified;
      regressions fixed by softening or bridging in place, never by reordering.

### Phase 4 Gate

> All checks below must pass before starting Phase 5.

- [ ] [AI] `find <MANIFESTS>careers/ -name '*.yaml' | wc -l` returns **4** — all four manifests published.
- [ ] [AI] The theory-first check prints `theory@` before `app@`, and Phase 3's inverse check still
      prints `app@` before `theory@` — the two arcs are provably distinct.
- [ ] [AI] The no-forked-body shell check prints exactly the single line `1`.
- [ ] [AI] `npx nx run ayokoding-www:test:unit` exits 0 — integrity, prerequisite-consistency, and
      no-forked-body green across **all four** manifests.
- [ ] [AI] `npx nx run ayokoding-www:build` + `:specs:behavior:coverage` **and**
      `npx nx run ayokoding-www-fe-e2e:test:e2e` exit 0.
- [ ] [AI] Hub card count returns **4** — the `careers/` group of the category-grouped hub is complete.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: all four paths are live over one shared library — zero body duplication among the
> three software-engineer paths; the AI path includes its SWE-fundamentals prerequisites at the head
> of `courseOrder` and walks its own spine (DD-35). Two manifests remain deliberately
> smoke-test-scoped and both carry a recorded, falsifiable deferral check, so the truncation is
> visible rather than silent. Safe to stop indefinitely. To resume:
> `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www-fe-e2e:test:e2e`.

---

## Phase 5: Manifest growth as backfill lands

> **Absorbed from `ayokoding-learning-path-04-course-authoring` per the manifest ownership
> invariant.** All four steps below genuinely mutate a `.yaml` under `<MANIFESTS>`; a Wave-2 plan
> cannot grow a Wave-3 plan's artefacts. The course **bodies** these growths depend on are authored by
> that plan and are already merged (Phase 0 precondition 2); what lands here is only their manifest
> consequence.
>
> **Trigger**: each band's **band-completion signal**, recorded in the course-authoring plan's own
> `delivery.md`, naming every manifest that must grow by full path. The routing rule is in
> [tech-docs §Which manifest grows when a band lands](./tech-docs.md#which-manifest-grows-when-a-band-lands).

### 5.1 · Bands 1–8 growth (the three software-engineer manifests)

- [ ] [AI] For each of Bands 1–8, append that band's newly-available course IDs into the three
      software-engineer-role manifests
      (`<MANIFESTS>careers/interview-ready/software-engineer.yaml`,
      `<MANIFESTS>careers/immediately-effective/software-engineer.yaml`,
      `<MANIFESTS>careers/fundamentally-strong/software-engineer.yaml`) at each path's correct topological
      position per its arc, then re-run integrity + prerequisite-consistency + no-forked-body —
      command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0 **after each band's append**, not only after the last one. A band whose
      append breaks prerequisite-consistency fails at that band, so the offending band is identifiable.

### 5.2 · Band 9 growth (interview-ready and fundamentally-strong only)

- [ ] [AI] Insert the five landed interview-technique courses (`coding-interview`,
      `take-home-and-live-coding`, `system-design-interview`,
      `behavioral-and-leadership-interviews`, `capstone-interview-loop`) into
      `<MANIFESTS>careers/interview-ready/software-engineer.yaml` — closing the gap Phase 1 deliberately left
      open — and into `<MANIFESTS>careers/fundamentally-strong/software-engineer.yaml` as its trailing
      optional interview band, each at its correct topological position.
      **`<MANIFESTS>careers/immediately-effective/software-engineer.yaml` does NOT grow here** — that path
      omits the interview-technique band by design (DL-13); its reader reaches these courses through
      their canonical pages, not the manifest — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0, AND the Phase-1 deferral check now closes the other way:
      `grep -oE 'coding-interview|take-home-and-live-coding|system-design-interview|behavioral-and-leadership-interviews|capstone-interview-loop' <MANIFESTS>careers/interview-ready/software-engineer.yaml | sort -u | wc -l`
      returns **5** (it returned **0** at Phase 1), AND the **same command against**
      `<MANIFESTS>careers/immediately-effective/software-engineer.yaml` still returns **0**. Both halves are
      required — a growth applied to all three manifests passes the first check and fails the second.

### 5.3 · Interview-ready refresh-register smoothness re-audit

- [ ] [AI] With the five interview-technique courses now in `courseOrder`, re-run the
      [smoothness audit](./tech-docs.md#smoothness-architecture-per-path)'s **refresh-register** lever
      that Phase 1 explicitly deferred — confirm each of the four interview-technique courses is
      pitched as technique and breadth refresh for a working engineer, never a from-zero concept teach
      — acceptance: the lever is verified and the Phase-1 deferral note in this checklist is updated
      from "deferred" to "closed", naming this step. Any regression is fixed by softening or bridging
      in place, never by reordering.
  - _Suggested executor: `web-researcher` for any external claim in the bridge prose_

### 5.4 · AI-path growth to its full composition (DD-33, amended in scope by DD-35 — no longer a

fixed "15-course" figure)

- [ ] [AI] Record the manifest's entry count immediately before this step —
      `grep -cE '^ *- [a-z0-9-]+' <MANIFESTS>careers/immediately-effective/ai-engineer.yaml` — and save
      it to `evidence/phase-5-4-pre-growth-count.txt` (this is the falsifiable "before" half of this
      step's before/after check; its value is whatever Phase 2 and any interim growth landed — an open
      figure, not fabricated as 6).
- [ ] [AI] Once the harness cluster (`creating-ai-powered-apps`, `agentic-ai`,
      `browser-automation-with-cdp`, `the-agent-loop`, `agent-tools-and-mcp`,
      `agent-context-and-memory`, `agent-permissions-and-sandboxing`,
      `agent-orchestration-subagents-and-observability`) and `capstone-build-your-own-coding-agent`
      have landed, insert all nine into
      `<MANIFESTS>careers/immediately-effective/ai-engineer.yaml` at their correct
      topological positions per the
      [manifest mirror](../ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/paths/manifest-immediately-effective-ai-engineer.md)
      (already renamed and corrected for the from-scratch model; this step only inserts the
      AI/harness cluster the mirror's "AI-specialization spine" section still names unchanged) —
      command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0, AND the nine cluster IDs are now present —
      `grep -oE 'creating-ai-powered-apps|agentic-ai|browser-automation-with-cdp|the-agent-loop|agent-tools-and-mcp|agent-context-and-memory|agent-permissions-and-sandboxing|agent-orchestration-subagents-and-observability|capstone-build-your-own-coding-agent' <MANIFESTS>careers/immediately-effective/ai-engineer.yaml | sort -u | wc -l`
      returns **9** (it returned **0** before this step), AND the entry count grew by **exactly 9**
      over the recorded pre-growth count —
      `grep -cE '^ *- [a-z0-9-]+' <MANIFESTS>careers/immediately-effective/ai-engineer.yaml`
      minus the value in `evidence/phase-5-4-pre-growth-count.txt` equals **9**. This before/after
      delta check replaces the pre-2026-07-21 fixed "returns 15" assertion, which assumed a fixed
      6-course starting spine that DD-35 superseded.
- [ ] [AI] Confirm the SWE-fundamentals **inclusion** survived the growth (inverted 2026-07-21 — the
      pre-ruling check asserted their **exclusion**) — command:
      `grep -oE 'just-enough-python|software-testing|cicd-and-release-engineering|backend-at-scale|containers-and-orchestration|computer-architecture|site-reliability-engineering|data-engineering|data-structures-and-algorithms-essentials|software-product-engineering|frontend-essentials' <MANIFESTS>careers/immediately-effective/ai-engineer.yaml | sort -u | wc -l`
      — acceptance: still returns **11 or more** (DD-35 holds; DD-33 widened the walk to the
      AI/harness cluster in addition to, never instead of, the now-included SWE-fundamentals set).

### 5.5 · Final arc confirmation

- [ ] [AI] Confirm all three software-engineer-role manifests reference their intended full arcs (no
      omitted-by-mistake course; omit-or-create honoured) and the library holds the full **127-course**
      catalog — command: `npx nx run ayokoding-www:build`
      — acceptance: exits 0, AND
      `find <COURSES> -maxdepth 1 -mindepth 1 -type d | wc -l` returns **127**, AND all four manifests
      validate against those bundles.

### Phase 5 Gate

> All checks below must pass before starting Phase 6.

- [ ] [AI] Bands 1–8 growth applied to all three software-engineer manifests; `test:unit` exited 0
      after each band's append.
- [ ] [AI] Band 9 check passes **both** ways: the five-ID check returns **5** against
      `careers/interview-ready/software-engineer.yaml` and **0** against
      `careers/immediately-effective/software-engineer.yaml`.
- [ ] [AI] The AI path's nine-cluster-ID check returns **9** and its entry count grew by exactly
      **9** over its recorded pre-growth count (5.4); the SWE-fundamentals **inclusion** check still
      returns **11 or more** (inverted 2026-07-21 — DD-35).
- [ ] [AI] The refresh-register lever is verified and the Phase-1 deferral note is marked closed.
- [ ] [AI] `find <COURSES> -maxdepth 1 -mindepth 1 -type d | wc -l` returns **127**;
      `npx nx run ayokoding-www:test:unit` and `:build` exit 0 with all four manifests validating.
- [ ] [AI] `npx nx run ayokoding-www-fe-e2e:test:e2e` exits 0 across all four grown paths.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: all four manifests are at their **full** composition over the complete 127-course
> library — no manifest is truncated, and the two smoke-test deferrals are provably closed in both
> directions. The four-path product is content-complete. Safe to stop indefinitely. To resume:
> `npx nx run ayokoding-www:build && npx nx run ayokoding-www:test:unit`.

---

## Phase 6: Section and app verification

- [ ] [AI] Run affected quality gates from the worktree:
      `npx nx affected -t typecheck lint test:quick test:unit specs:behavior:coverage`
      — acceptance: exits 0. Fix ALL failures, including preexisting ones (Root Cause Orientation),
      committing preexisting fixes separately.
- [ ] [AI] Run the e2e suite: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: exits 0.
      (`ayokoding-www:test:e2e` and `:test:integration` are no-op echo targets and can never fail —
      they are deliberately not cited as evidence anywhere in this plan.)
- [ ] [AI] Build the site: `npx nx run ayokoding-www:build` — acceptance: exits 0.
- [ ] [AI] Run link + heading-hierarchy + markdown validation:
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md links validate --exclude plans/done --exclude apps/ayokoding-www/content --exclude apps/ose-www/content` +
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md heading-hierarchy validate` + `npm run lint:md` (the actual mechanism — **not** `nx run` targets) — acceptance: the link
      validator prints `All links valid! No broken links found.`; the other two exit 0.

  **Gherkin (binds) →** "The manifest layer builds and validates green"

  ```gherkin
  Scenario: The manifest layer builds and validates green
    Given all four path manifests and their landing anchors are published
    When the app build, the affected test tiers, and the link and heading validators run
    Then the build and every affected tier succeed
    And manifest integrity and prerequisite consistency report zero violations across all four manifests
  ```

- [ ] [AI] **Manifest-integrity + prerequisite-consistency sweep** — all four manifests: every
      `courseOrder` ID resolves; no duplicate ID; prerequisite-consistency holds; no forked body across
      the three software-engineer-role paths (the AI path **includes**, not shares, its
      SWE-fundamentals prerequisite courses at the head of its own `courseOrder`, DD-35 — including
      the same course ID in two manifests is inclusion, not a fork, because neither manifest owns or
      duplicates the course **body**) — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the integrity check reports **zero** violations across all four.
- [ ] [AI] **All-path smoothness re-check (DD-16)** — re-verify the four levers for each manifest
      against the landed content — acceptance: all four paths pass; every regression fixed by
      softening or bridging in place, never by reordering.
- [ ] [AI] **Ownership boundary check (scoped to `careers/` per R4)** — confirm the `careers/`
      subdirectory of the manifest directory holds exactly the four YAML files this plan authored and
      nothing else: `find <MANIFESTS>careers/ -name '*.yaml' | wc -l` returns
      **4**, and `find <MANIFESTS>careers/ -name '*.yaml' | sort` lists exactly the four declared path IDs
      — acceptance: both hold. Scoped to `<MANIFESTS>careers/`, not the bare `<MANIFESTS>` root, so a
      sibling `skills/*.yaml` manifest landed concurrently by `ayokoding-learning-path-06-skills-paths`
      cannot change this count in either direction. Falsifiable both ways: a fifth `careers/` manifest
      added by any other plan makes the count **5**, and a deleted `careers/` manifest makes it **3**.
- [ ] [AI] **Cross-plan link check (this plan's own folder)** —
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md links validate --exclude plans/done --exclude apps/ayokoding-www/content --exclude apps/ose-www/content 2>&1 | grep -F "ayokoding-learning-path-05-manifests"`
      — acceptance: the `grep` finds **no** matching line (exit 1). Falsifiable the other way too:
      introduce one bad `./syllabus/` link into this folder and the same command prints that file and
      exits 0. `md links validate` accepts **no positional path** and always walks the repo, so
      "run it in this plan's folder" is not expressible — the filter above is the scoped form.

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes
> (Root Cause Orientation). Commit preexisting fixes separately with conventional-commit messages.

### Phase 6 Gate

> All checks below must pass before starting Phase 7.

- [ ] [AI] Affected `typecheck` / `lint` / `test:quick` / `test:unit` / `specs:behavior:coverage`
      exit 0; `ayokoding-www-fe-e2e:test:e2e` exits 0.
- [ ] [AI] Build + link + heading + markdown validation green; the link validator prints
      `All links valid! No broken links found.`
- [ ] [AI] Manifest integrity + prerequisite-consistency + all-path smoothness report zero violations
      across all four manifests.
- [ ] [AI] The ownership boundary check returns exactly **4** manifest files, matching the four
      declared path IDs.
- [ ] [AI] The scoped cross-plan link check finds no line naming this plan's folder.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the whole four-path composition passes every automated gate. Safe to stop
> indefinitely. To resume: re-run the affected quality gates and the build.

---

## Phase 7: Manual UI verification and Rule-15 three-tester retest

> This plan ships four user-visible path landings plus a paths hub that goes from zero to four
> populated cards, so the **Rule-15 three-tester retest is mandatory** before archival. The
> UI-design-funnel itself is exempt — no net-new screen or component is added here; see
> [tech-docs §UI-design-funnel exemption](./tech-docs.md#ui-design-funnel-exemption-recorded-explicitly).
>
> **Locale scope**: this plan's path content is authored `en`-only. `id/belajar/` holds zero courses
> and zero paths, so a manifest over it would compose nothing; an `id` walk-through would be
> fabricated, not verified. The navigation mechanism itself is locale-neutral — this is a
> content-availability fact, recorded as a non-goal in
> [brd.md §Business-Scope Non-Goals](./brd.md#business-scope-non-goals).

- [ ] [AI] Confirm `en` is the only content locale for the path library — command:
      `test -d apps/ayokoding-www/content/en/learn/paths && test ! -d apps/ayokoding-www/content/id/belajar/paths`
      — acceptance: exits 0 (the `en` paths bucket exists and no `id` sibling exists).
- [ ] [AI] Start the dev server: `npx nx dev ayokoding-www` — acceptance: server up on the app's
      configured port.
- [ ] [AI] For `en` × breakpoints (375 / 768 / 1280 px), via Playwright MCP `browser_navigate` +
      `browser_resize`: open the paths hub `/en/learn/paths` (category-grouped layout, **four**
      populated cards in the `careers/` group),
      then each of the four path landings, then walk 2–3 courses per path via prev/next confirming
      `?path=` persists and the order matches the manifest, then open a course and confirm its
      prerequisite display — acceptance: all behaviours correct at all three breakpoints.
- [ ] [AI] Deep-link a course with **no** `?path=` and confirm the canonical view renders with the
      "this course is part of" affordance naming **every** path whose manifest includes it; then hit an
      invalid `?path=` and confirm the canonical view renders with no error — acceptance: both hold.
- [ ] [AI] For the AI path landing specifically, confirm the outbound links to prerequisite
      software-engineer courses' canonical pages resolve (DD-24) — acceptance: every outbound
      `/en/learn/courses/<id>` link returns 200.
- [ ] [AI] Verify `html[lang]` is `en` and `browser_console_messages` is clean on every screen —
      acceptance: correct lang attribute; **zero** console errors.
- [ ] [AI] Capture one screenshot per screen per breakpoint via `browser_take_screenshot` to
      `evidence/phase-7-<screen>-en-<breakpoint>px.png` — acceptance: files exist in `evidence/`;
      `find evidence -name 'phase-7-*-en-*px.png' | wc -l` returns **15** (5 screens — hub plus four
      landings — × 3 breakpoints). Falsifiable both ways: a missed breakpoint or screen returns fewer.
- [ ] [AI] Document the evidence in this checklist: reference each screenshot
      (`![alt](./evidence/...)`) and note the console/network status per screen.
- [ ] [AI] Run the three live-site testers (the `web-ux-test-fixing-planning` workflow:
      `web-exploratory-tester` + `web-usability-tester` + `web-design-tester`) against the running
      paths hub and all four path landings, plus sample courses reached from each landing in path
      context — acceptance: EWT/UWT/DWT findings and spec-gaps recorded.
- [ ] [AI] Append each finding below as a new unchecked checkbox, source-attributed
      (`- [ ] EWT-NNN:` / `- [ ] UWT-NNN:` / `- [ ] DWT-NNN: <defect> — fix before archival`); append
      any SG-###/USS-### items to the relevant spec step in Phases 1–4.

### Rule-15 retest follow-ups

- [ ] [AI] _(populated during the retest — every EWT/UWT/DWT defect finding must be fixed and ticked
      before archival; deferral of a defect requires explicit user permission and only when genuinely
      impossible; SG-###/USS-### may be triaged or deferred with written rationale)_

### Phase 7 Gate

> All checks below must pass before starting Phase 8.

- [ ] [AI] Hub (four populated cards) + four landings + sample courses + prerequisite display + the
      part-of-paths affordance verified in `en` at 375 / 768 / 1280 px; console clean on every screen.
- [ ] [AI] `find evidence -name 'phase-7-*-en-*px.png' | wc -l` returns **15**; each screenshot is
      referenced from this checklist.
- [ ] [AI] Every rule-15 EWT/UWT/DWT defect finding is fixed and ticked, or explicitly permitted to
      defer by the user.
- [ ] [AI] Draft PR opened (retest evidence and any fixes); 3-cycle PR-Review complete; CI green; PR
      `[AI]`-merged; deployed.

> **Pause Safety**: the four-path UI is verified live and defect-clean in `en`, with committed
> evidence. Safe to stop indefinitely. To resume: re-run the three testers against the running app.

---

## Phase 8: Final origin main integration and CI verification

- [ ] [AI] Confirm no plan PR is still open:
      `gh pr list --search "ayokoding-learning-path-05-manifests" --state open --json number --jq 'length'`
      — acceptance: returns **0**; every prior phase branch has been `[AI]`-merged to `main`.
- [ ] [AI] Sync the shared worktree to the latest `origin/main` and run the full affected suite:
      `npx nx affected -t typecheck lint test:quick test:unit specs:behavior:coverage` +
      `npx nx run ayokoding-www-fe-e2e:test:e2e` + `npx nx run ayokoding-www:build`
      — acceptance: all exit 0 on the integrated `main`.
- [ ] [AI] Monitor the final `main` CI run — poll every ~2 minutes with one
      `gh run view --json status,conclusion` per wakeup; never `gh run watch`, never a tight loop
      — acceptance: all GitHub Actions green; fix root causes and push follow-ups (own PR → review →
      `[AI]` merge) until green.
- [ ] [AI] Confirm `prod-ayokoding-www` serves all four path landings and the four-card hub;
      re-dispatch `apps-ayokoding-www-deployer` if any earlier deploy lagged — acceptance: production
      serves the four-path product.

### Phase 8 Gate

> All checks below must pass before starting Phase 9.

- [ ] [AI] Zero open plan PRs; every prior phase merged to `main`.
- [ ] [AI] Full affected suite + e2e + build green on the integrated `main`; the final `main` CI run
      is green.
- [ ] [AI] `prod-ayokoding-www` serves all four paths and the complete `careers/` group of the hub.

> **Pause Safety**: the whole plan is integrated on `main`, green in CI, and live in production. Safe
> to stop indefinitely. To resume: re-run the affected suite on `main` and check CI and prod status.

---

## Phase 9: Knowledge Capture

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)._

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only if a durable surface would
      catch this automatically next time; discard the rest with a one-line reason — acceptance: every
      entry has either a route or a discard reason.
- [ ] [AI] Apply the **secret/sensitivity gate** to every surviving entry — sanitize any secret,
      credential, token, or private hostname to a `<placeholder>` token, or discard if unsanitizable
      — acceptance: `learnings.md` contains no raw secret.
- [ ] [AI] Apply the **repo-relevance gate** — infra-private content (Terraform, k3s, Proxmox, real
      hostnames or inventories) stays in `ose-infra` only and is NEVER cross-routed into
      `ose-public`/`ose-primer`; public-governance content may propagate via the existing parity loop
      — acceptance: no infra-private content appears in this repo's routed output.
- [ ] [AI] Route each surviving learning to exactly one durable home per the open-ended routing matrix
      — non-code homes (`repo-governance/`, `docs/`, `.claude/agents/`, `.claude/skills/`, a
      post-mortem) may land inline for a small edit or as a `plans/backlog/` follow-up for a large one;
      **code homes (`apps/`, `libs/`, tests) are ALWAYS filed as a separate `plans/backlog/<slug>/`
      plan and NEVER landed inline in this plan's own commits or PR** — acceptance: every
      `learnings.md` entry records its terminal routing state.
- [ ] [AI] If no generalizable learning surfaced, record the explicit escape in `learnings.md`:
      `No generalizable learnings — <one-line reason>` — acceptance: `learnings.md` is never silently
      empty.

### Phase 9 Gate

> All checks below must pass before Plan Archival.

- [ ] [AI] Every `learnings.md` entry is in a terminal state (routed inline, filed as backlog, or
      discarded with a reason), or the file records the explicit "none" escape.
- [ ] [AI] No code-homed learning landed inline in this plan's own commits or PR — every code-routed
      learning has a corresponding `plans/backlog/` folder.
- [ ] [AI] Draft PR opened (`learnings.md` triage); 3-cycle PR-Review complete; CI green; PR
      `[AI]`-merged; deployed (no-op).

> **Pause Safety**: `learnings.md` is fully triaged (or explicitly recorded as empty); no future
> process depends on querying it later. Safe to stop. To resume: re-read `learnings.md` and confirm
> every entry is terminal.

---

## Phase 10: Plan Archival

- [ ] [AI] Verify ALL delivery checklist items are ticked.
- [ ] [AI] Verify the Knowledge Capture phase is complete — every `learnings.md` entry reached a
      terminal state or the file records the explicit `No generalizable learnings — <reason>` escape;
      both the secret/sensitivity gate and the repo-relevance gate were applied to every surviving
      entry.
- [ ] [AI] Verify ALL quality gates pass (local + CI) and the build is green.
- [ ] [AI] Verify ALL manual assertions pass (Playwright MCP) with committed evidence in `evidence/`;
      the `en` content locale was exercised across all three breakpoints (the `id` deferral is a
      recorded non-goal, not a skipped locale).
- [ ] [AI] Verify every rule-15 EWT/UWT/DWT defect finding is fixed (ticked) — deferral requires
      explicit user permission and only when genuinely impossible; SG-###/USS-### may be triaged or
      deferred with written rationale.
- [ ] [AI] **Terminal four-manifest and 127-catalog assertion (R5: the 127 total is the `careers/`
      software-engineering catalog only, not a whole-programme total including `skills/`)** — verify
      all four `careers/` path manifests are published and at their **full** composition, all four
      landings are live, the paths hub's `careers/` group shows all four cards, and the
      `careers/`-scoped library holds the full 127-course catalog:
      `find <MANIFESTS>careers/ -name '*.yaml' | wc -l` returns **4**, AND
      `grep -oE '/en/learn/paths/careers/[a-z-]+/[a-z0-9-]+' <PATHS>_index.md | sort -u | wc -l` returns
      **4**, AND `find <COURSES> -maxdepth 1 -mindepth 1 -type d | wc -l` returns **127**, AND
      `npx nx run ayokoding-www:test:unit` exits 0 — acceptance: all four hold. This assertion spans
      this plan and `ayokoding-learning-path-04-course-authoring`, and it belongs **here**: that plan
      asserts only the count of bodies it itself authored, while the 127-catalog claim is only
      meaningful once every manifest resolves against it. `<COURSES>` today holds only the
      `careers/software-engineering` corpus — the `skills/` category's ERP + accounting corpus is a
      separate corpus authored by `ayokoding-learning-path-06-skills-paths` and is not counted by this
      `find`, so this assertion does not need to change when that sibling plan lands.
- [ ] [AI] **Scoped cross-plan link check** — re-run the Phase 6 filtered link validation and confirm
      it still finds no line naming this plan's folder. If
      `ayokoding-learning-path-02-schema-and-prerequisite-dag` has archived since, confirm every
      `syllabus/` reference in this folder points at its `plans/done/YYYY-MM-DD__…` path — acceptance:
      the filtered `grep` exits 1 and the repo-wide filtered validator prints
      `All links valid! No broken links found.`
- [ ] [AI] Move: `git mv plans/in-progress/ayokoding-learning-path-05-manifests plans/done/YYYY-MM-DD__ayokoding-learning-path-05-manifests`
      using today's completion date (the `evidence/` subfolder moves with it).
- [ ] [AI] Update `plans/in-progress/README.md` — remove the plan entry.
- [ ] [AI] Update `plans/done/README.md` — add the plan entry with its completion date.
- [ ] [AI] Update any other READMEs that reference this plan (`plans/README.md`,
      `plans/backlog/README.md`), and update the four sibling split plans' cross-references to this
      plan's new archived path in the **same commit** as the `git mv`.
- [ ] [AI] Commit the archival: `chore(plans): move ayokoding-learning-path-05-manifests to done`.

### Phase 10 Gate

> All checks below must pass. This is the terminal gate of the five-plan split.

- [ ] [AI] All four manifests published at full composition; hub shows four cards; 127-course catalog
      resolves; `test:unit` and `build` exit 0.
- [ ] [AI] The filtered link check finds no line naming this plan's folder, and the repo-wide filtered
      validator prints `All links valid! No broken links found.`
- [ ] [AI] Plan folder is under `plans/done/YYYY-MM-DD__ayokoding-learning-path-05-manifests`; every
      referencing README is updated; the archival is committed.
- [ ] [AI] Draft PR opened (archival move); 3-cycle PR-Review complete; CI green; PR `[AI]`-merged;
      deployed (no-op).

> **Pause Safety**: the plan is archived and its final PR `[AI]`-merged to `main`. Terminal state — and
> since this is the terminal plan of the five-way split, the whole split is complete. To resume:
> nothing.

---

## Commit Guidelines (all phases)

- [ ] [AI] Commit changes thematically — group related changes into logically cohesive commits.
- [ ] [AI] Follow Conventional Commits: `<type>(<scope>): <description>` (imperative, no period).
- [ ] [AI] Split domains and concerns into separate commits; preexisting fixes get their own commits.
- [ ] [AI] Do NOT bundle unrelated changes into a single commit.

## Local Quality Gates (before every push)

- [ ] [AI] `npx nx affected -t typecheck` exits 0.
- [ ] [AI] `npx nx affected -t lint` exits 0.
- [ ] [AI] `npx nx affected -t test:quick test:unit` exits 0.
- [ ] [AI] `npx nx affected -t specs:behavior:coverage` exits 0.
- [ ] [AI] `npx nx run ayokoding-www-fe-e2e:test:e2e` exits 0 for any phase touching a manifest or a
      landing.
- [ ] [AI] Fix ALL failures — including preexisting issues not caused by your changes (Root Cause
      Orientation).

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes.
> Commit preexisting fixes separately with appropriate conventional-commit messages.
