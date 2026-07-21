# Delivery Checklist — ayokoding-www Learning-Path URL Restructure

Executable checklist for the **URL and IA layer**: the `courses/` and `paths/` content homes, the
re-home of 37 shipped bundles with their per-course 308s, the six-domain relocation into `legacy/`
with its 12-rule redirect module, and Screen 4's design funnel. Requirements live in
[brd.md](./brd.md) and [prd.md](./prd.md); the technical approach, all ten owned design decisions,
and the six open questions live in [tech-docs.md](./tech-docs.md).

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
>
> **This plan uses no `[HUMAN]` steps.** Every step below is `[AI]`, including worktree
> provisioning, commit, push, PR merge, and worktree removal.

## Worktree

Worktree path: `worktrees/ayokoding-learning-path-01-url-restructure/`

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree ayokoding-learning-path-01-url-restructure
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the latest
`origin/main` when missing, syncs with `origin/main` before implementing, and prompts before deleting
the worktree after the plan is archived and pushed.

Every phase branches from the **latest `origin/main`** inside this worktree
(`git fetch origin && git checkout main && git pull && git checkout -b ayokoding-learning-path-01-url-restructure/<phase-slug>`),
authors its work there, commits, pushes that branch, and opens **its own draft PR**.

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans.md#worktree-specification).

## Delivery Mode: worktree-to-pr

Each phase works in this worktree on its **own branch**, opens a **draft PR** against `main`, runs the
**PR-Review Maker→Fixer Cycle** (`pr-review-maker` / `pr-review-fixer`, 3 sequential CI-gated cycles),
flips the PR to ready, and `[AI]` **merges it automatically once all quality gates are green** — then
`[AI]` **deploys `ayokoding-www` to `prod-ayokoding-www` after every merge** (this plan ships to
ayokoding.com). See
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
   `git fetch origin && git checkout main && git pull && git checkout -b ayokoding-learning-path-01-url-restructure/<phase-slug>`.
2. [AI] Stage only this phase's paths (`git add <explicit paths>` — never `git add -A`), commit
   thematically (Conventional Commits, imperative, no period), push the branch, open a **draft PR**
   against `main` (`gh pr create --draft --base main ...`) — CI runs on the PR.
3. [AI] Run the **PR-Review Maker→Fixer Cycle** (3 sequential CI-gated cycles), resolve every finding,
   then `gh pr ready`.
4. [AI] **Merge** once all quality gates are green (typecheck, lint, `test:quick`, `test:unit`,
   `test:e2e` in the paired `ayokoding-www-fe-e2e` project, `specs:behavior:coverage`, CI, the 3-cycle
   review) — `[AI]` auto-merge per DN-11.
5. [AI] Dispatch `apps-ayokoding-www-deployer` to deploy `ayokoding-www` to `prod-ayokoding-www` — a
   no-op redeploy for plan-side-only phases.

## Cross-plan sequencing

This plan is **Wave 1** with **no upstream prerequisite** — it may start immediately. Its downstream
consumers, its handoff signal, and the Wave-1 sibling coordination note are in
[README §Implementation Sequence and Prerequisites](./README.md#implementation-sequence-and-prerequisites).

> **Concurrency note.** `ayokoding-learning-path-02-schema-and-prerequisite-dag` runs in the same
> wave and touches `apps/ayokoding-www/src/features/course-paths/` — a subtree this plan never
> touches. The two plans' file sets are disjoint, so their PRs merge in either order. Both plans do
> edit the **prerequisite frontmatter contract's meaning**: this plan writes the field into 37
> `_index.md` files while the sibling writes its parser. If the two disagree, **the sibling's shape
> wins** — see [tech-docs §Prerequisite frontmatter contract](./tech-docs.md#prerequisite-frontmatter-contract-reproduced-verbatim-canonical-owner-is-the-schema-plan).

## Parallelization Model

**Cap**: honor the in-force subagent/PR-review concurrency cap (parallel-by-default, background
subagents capped per the orchestration convention). The main thread self-promotes nothing.

- **Phases 0 → 1 → 2 → 3 are strictly serial.** Each is a sync point for the next: Phase 1 creates the
  namespace Phase 2 moves bodies into; Phase 2 must land so `en/learn/` is never transiently
  `legacy/`-only; Phase 3's six `git mv`s and its redirect module must land together (a live 308
  pointing at a not-yet-moved path 404s, and a moved path with no 308 breaks ~1,148 URLs — neither
  half is a safe stopping state).
- **Phases 4 → 5 → 6 → 7 → 8 are serial finalization.**
- **No phase in this plan fans out.** The work is one content tree and one redirect chain; splitting a
  phase across concurrent agents would produce merge conflicts in `next.config.ts` and in the same
  `_index.md` files for no throughput gain.

**Path constants** (referenced throughout — reproduced **verbatim** from the source plan so the
constant vocabulary is byte-identical across all five split plans; entries this plan does not itself
use are retained deliberately, not pruned):

- `<COURSES>` = `apps/ayokoding-www/content/en/learn/courses/` (course bundles; served at `/en/learn/courses/<course-id>`)
- `<PATHS>` = `apps/ayokoding-www/content/en/learn/paths/` (thin path-landing anchors; served at `/en/learn/paths/<path-id>`)
- `<SE_OLD>` = `apps/ayokoding-www/content/en/learn/fundamentally-strong/software-engineer/` (legacy home of the 33 shipped topics + 4 existing capstones, incl. `capstone-solid-core` — the re-home source)
- `<FEAT>` = `apps/ayokoding-www/src/features/course-paths/`
- `<MANIFESTS>` = `<FEAT>manifests/` (standalone YAML data files, nested to mirror slash path ids — `<MANIFESTS><path-id>.yaml`)
- `<LEGACY>` = `apps/ayokoding-www/content/en/learn/legacy/` (**new bucket**, scope extension; served at `/en/learn/legacy/<domain>/…`)
- `<REDIR>` = `apps/ayokoding-www/src/redirects/`
- `<SPECS>` = `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/course-paths/`
- `<NAVSPECS>` = `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/navigation/` (existing domain — the three-bucket Gherkin lands beside `content-namespace-redirects.feature`)
- Path ids: `careers/interview-ready/software-engineer`, `careers/immediately-effective/software-engineer`, `careers/fundamentally-strong/software-engineer`, `careers/immediately-effective/ai-engineer` (fourth path — id renamed from the dead `software-engineer-to-ai-engineer` 2026-07-21; no longer assumes a prior software-engineering role, so a role-transition-shaped id was factually wrong; manifest at `<MANIFESTS>careers/immediately-effective/ai-engineer.yaml`)

---

## Phase 0: Environment Setup & Baseline

> _Executor: repo-setup-manager_
>
> **No cross-plan precondition.** This plan is Wave 1 with no upstream. The sibling FS-SE plan is
> CLOSED (`plans/done/2026-07-19__fundamentally-strong-software-engineer/`); there is **no "FS-SE must
> be DONE first" gate**. Only the 33 shipped topics (1–33) + 4 existing capstones (incl.
> `capstone-solid-core`, per **DD-20**) live under `<SE_OLD>` and are re-homed in Phase 2 — the other
> 61 transferred topics have no legacy home and are authored NATIVE by
> `ayokoding-learning-path-04-course-authoring`.

- [ ] [AI] Enter/provision the worktree and install dependencies in the root worktree: `npm install`
      — acceptance: exits 0, `node_modules/` synchronized.
- [ ] [AI] Converge the toolchain in the root worktree: `npm run doctor -- --fix`
      — acceptance: exits 0 with no unresolved drift.
- [ ] [AI] Establish baselines: `npx nx run ayokoding-www:build` and
      `npx nx run ayokoding-www:test:unit`
      — acceptance: both exit 0; record the pass state and any preexisting failure in
      `evidence/phase-0-snapshot.txt`. Resolve every preexisting failure before Phase 1 (Root Cause
      Orientation).
- [ ] [AI] **Re-home source inventory (non-blocking snapshot)** — record the 33 shipped topics + 4
      existing capstones present under `<SE_OLD>` to `evidence/phase-0-snapshot.txt` via:
      `for s in just-enough-nvim just-enough-lua extending-neovim just-enough-python just-enough-bash version-control-and-git data-structures-and-algorithms-essentials advanced-algorithms object-oriented-programming-essentials object-oriented-design-and-patterns sql-essentials technical-communication just-enough-typescript frontend-essentials backend-essentials networking-essentials computer-science-foundations computer-architecture programming-paradigms functional-programming concurrency-and-parallelism advanced-networking advanced-sql-and-query-performance data-access-orms-and-query-builders build-your-own-orm-and-query-builder software-engineering-practices agentic-coding security-essentials software-testing debugging-and-profiling software-product-engineering engineering-management project-management capstone-forge-ready capstone-first-working-software capstone-full-stack-app capstone-solid-core; do test -d "<SE_OLD>$s" || echo "ABSENT $s"; done`
      — acceptance: snapshot committed. Any `ABSENT` line is recorded (not a hard stop) and reconciled
      against [tech-docs §Ground-truth inventory](./tech-docs.md#ground-truth-inventory-measured-2026-07-21-re-verified-at-authoring)
      before Phase 2. **This list is the authoritative re-home set** — the Phase 2 move loop and the
      `course-rehome.ts` rule table both derive from it, so a divergence discovered later is a
      correctness bug in both.
- [ ] [AI] Confirm the source directory holds exactly the expected shape —
      `ls apps/ayokoding-www/content/en/learn/fundamentally-strong/software-engineer | wc -l`
      — acceptance: returns **39** (`_index.md` + `overview.md` + 37 course-shaped directories). A
      different number means the re-home set above is stale; reconcile before Phase 2. Falsifiable
      both ways: after Phase 2 the same command returns **2**.
- [ ] [AI] **Freeze the re-home set as a machine-readable list** — write the reconciled 37 slugs, one
      per line, to `evidence/phase-0-rehome-slugs.txt` via
      `ls -d apps/ayokoding-www/content/en/learn/fundamentally-strong/software-engineer/*/ | xargs -n1 basename > evidence/phase-0-rehome-slugs.txt`
      — acceptance: `wc -l < evidence/phase-0-rehome-slugs.txt` returns **37**, and every line also
      appears in the inventory loop above. This file is what the Phase-2 move loop and
      `REHOMED_COURSE_SLUGS` are both checked against, so the two can never drift apart silently.
- [ ] [AI] Snapshot the existing `content-url.ts` / `prev-next.tsx` / `breadcrumb.tsx` /
      `tree-builder.ts` behavior and the current `next.config.ts` redirect spread order into
      `evidence/phase-0-snapshot.txt` — acceptance: snapshot committed, including the verbatim current
      `redirects()` return expression (the Phase 3 ordering check diffs against it).
- [ ] [AI] **Legacy-bucket source inventory (DD-40)** — record the per-domain `.md` counts under
      `apps/ayokoding-www/content/en/learn/` to `evidence/phase-0-snapshot.txt` via:
      `for d in fundamentally-strong software-engineering artificial-intelligence information-security personal-development it-governance business; do printf '%s %s\n' "$d" "$(find apps/ayokoding-www/content/en/learn/$d -name '*.md' | wc -l)"; done`
      — acceptance: snapshot committed and matches the stated baseline (563 / 979 / 55 / 51 / 50 / 9 /
      4; the six relocated domains sum to **1,148**). A divergence is recorded and reconciled against
      [tech-docs §Ground-truth inventory](./tech-docs.md#ground-truth-inventory-measured-2026-07-21-re-verified-at-authoring)
      before Phase 3 — it is not a hard stop here, but **every 1148 assertion downstream must be
      updated together** if the baseline moved.
- [ ] [AI] **Collision + `id` baseline check** —
      `test -e apps/ayokoding-www/content/en/learn/legacy && echo "EXISTS legacy"; test -e apps/ayokoding-www/content/en/learn/courses && echo "EXISTS courses"; test -e apps/ayokoding-www/content/en/learn/paths && echo "EXISTS paths"; test -e apps/ayokoding-www/src/redirects/learn-three-bucket.ts && echo "EXISTS bucket-module"; test -e apps/ayokoding-www/src/redirects/course-rehome.ts && echo "EXISTS rehome-module"; find apps/ayokoding-www/content/id/belajar -name '*.md' | wc -l`
      — acceptance: zero `EXISTS` lines (no bucket, no content home, neither redirect module exists
      yet), and the `id/belajar` count (**53** today) is recorded so the `en`-only scoping (DD-45) is
      verifiable as unchanged at archival. Falsifiable both ways: after Phase 3 the first three
      `test -e` checks all print their `EXISTS` line.
- [ ] [AI] Confirm `learnings.md` scaffold exists in the plan folder — acceptance:
      `test -f plans/backlog/ayokoding-learning-path-01-url-restructure/learnings.md` returns 0 and
      the file opens with its H1.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [ ] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift.
- [ ] [AI] `npx nx run ayokoding-www:build` and `:test:unit` exit 0; every preexisting failure is
      resolved (zero unresolved).
- [ ] [AI] `evidence/phase-0-snapshot.txt` is committed and carries: the 37-slug re-home inventory
      (zero unreconciled `ABSENT` lines), the seven per-domain `.md` counts summing the six relocated
      domains to **1148**, the `id/belajar` count of **53**, and the verbatim current `redirects()`
      spread order.
- [ ] [AI] Zero collision lines: neither content home, neither redirect module, and no `legacy/`
      bucket exists yet.

> **Pause Safety**: only the toolchain was verified and the baseline recorded — no content moved, no
> code written, no URL changed. Safe to stop indefinitely. To resume:
> `npx nx run ayokoding-www:build && npx nx run ayokoding-www:test:unit` and re-read
> `evidence/phase-0-snapshot.txt`.

---

## Phase 1: Library + paths content homes

> _Suggested executor: `apps-ayokoding-www-content-maker`_ (two `_index.md` section landings mirroring
> an existing section index).
>
> **Boundary note (BF-3).** This step is **owned by this plan**, not by the schema or navigation-ui
> plans. The source plan located it inside a phase that otherwise belongs to
> `ayokoding-learning-path-02-schema-and-prerequisite-dag`; as written, Phase 2's re-home would have
> had nowhere to move bodies into and Phase 3's structural gate would have been unsatisfiable. See
> [README §Provenance](./README.md#provenance--where-this-plan-came-from).

- [ ] [AI] **Library + paths content homes** — create `<COURSES>_index.md` _(New file)_ (library
      landing, `title` + `weight` + `date` + `draft: false`) and `<PATHS>_index.md` _(New file)_ (paths
      hub / choose-a-path landing whose 2×2-grid layout has room for **all four** paths, populated as
      each ships), both mirroring the frontmatter shape of an existing section `_index.md` such as
      `apps/ayokoding-www/content/en/learn/_index.md` — acceptance: `test -f <COURSES>_index.md` and
      `test -f <PATHS>_index.md` both return 0 (both return non-zero before this step, verified in
      Phase 0's collision check), and `npx nx run ayokoding-www:build` exits 0.
- [ ] [AI] **Set explicit weights so the bucket order is `paths`, `courses`, `legacy`** — give
      `<PATHS>_index.md` the lowest `weight` and `<COURSES>_index.md` the next, leaving headroom above
      both for the Phase 3 `<LEGACY>_index.md` — acceptance: the two `weight` values are present,
      distinct, and both strictly less than the value Phase 3 will assign to `legacy`. Rationale:
      `buildTreeForLocale` sorts siblings by `weight` and synthesizes `weight: 0` for any missing
      ancestor [Repo-grounded — `apps/ayokoding-www/src/features/content/core/tree-builder.ts`], so
      leaving weights implicit makes sidebar order an accident of file order.
- [ ] [AI] Regenerate the derived indexes so the two new sections enter the tree:
      `npx nx run ayokoding-www:generate-indexes` then `npx nx run ayokoding-www:validate-indexes`
      — acceptance: both exit 0 (the second proves regeneration converged).
- [ ] [AI] Run the local quality gates and the [Per-Phase Integration Protocol](#delivery-mode-worktree-to-pr)
      — acceptance: gates green; draft PR opened, reviewed, merged, deployed.

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [ ] [AI] `test -f apps/ayokoding-www/content/en/learn/courses/_index.md` and
      `test -f apps/ayokoding-www/content/en/learn/paths/_index.md` both return 0 — both returned
      non-zero at Phase 0.
- [ ] [AI] Both files carry explicit, distinct `weight` values leaving headroom for `legacy`.
- [ ] [AI] `npx nx run ayokoding-www:build` + `:typecheck` + `:validate-indexes` exit 0.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: two empty section landings exist and render; no body moved, no URL changed, no
> redirect added. Production serves the same content it served before, plus two new (empty) landing
> pages. Safe to stop indefinitely. To resume: `npx nx run ayokoding-www:build`.

---

## Phase 2: Re-home the 33 shipped topics + 4 existing capstones into `courses/`

> _Suggested executor: `swe-typescript-dev`_ (mechanical `apps/ayokoding-www/content/` moves + the
> redirect module and its unit test — `docs-file-manager` is scoped to `docs/` only and does not cover
> app content).
>
> Only the **shipped** legacy bodies move here (33 topics + 4 existing capstones, incl.
> `capstone-solid-core` per **DD-20**). Topics with no legacy home are authored NATIVE by
> `ayokoding-learning-path-04-course-authoring`.
>
> **Boundary note (BF-1).** The per-course redirect table below was located in a
> `ayokoding-learning-path-03-navigation-ui` phase in the source plan, while this plan's gate
> required it. It is **moved here**. The table is a pure `<REDIR>` module plus a unit test with **zero**
> dependency on the `course-paths` feature, so nothing about the move is contrived. The "confirm each
> re-homed course has its redirect" step below therefore names **this plan's own RED/GREEN steps**,
> not "(Phase 3)".

### 2.1 · Per-course re-home redirects (TDD)

- [ ] [AI] **RED** — write a failing unit test at `<REDIR>course-rehome.unit.test.ts` _(New test)_,
      mirroring the existing `<REDIR>content-namespace.unit.test.ts` structure [Repo-grounded],
      asserting: (a) exactly **37** rules, one per slug in the Phase-0 re-home inventory; (b) every
      rule `permanent: true` with non-empty `source`/`destination`; (c) each rule's source is
      `/en/learn/fundamentally-strong/software-engineer/<slug>` and its destination is
      `/en/learn/courses/<slug>` for the **same** `<slug>`; (d) the rule set's slug list equals the
      Phase-0 inventory exactly (no extra, no missing) — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: the suite fails with `course-rehome` module
      not found. Falsifiable both ways:
      `test -f apps/ayokoding-www/src/redirects/course-rehome.ts` returns non-zero today (verified in
      Phase 0) and returns 0 after the GREEN step below.

  **Gherkin (binds) →** "A legacy fundamentally-strong URL redirects to the canonical course URL"

  ```gherkin
  Scenario: A legacy fundamentally-strong URL redirects to the canonical course URL
    Given a re-homed course previously lived under the legacy fundamentally-strong/software-engineer content path
    When a reader requests the legacy URL
    Then the app redirects to the course's canonical /en/learn/courses/<course-id> URL
    And the redirect preserves any path context query parameter
  ```

- [ ] [AI] **GREEN** — author `<REDIR>course-rehome.ts` _(New file)_ exporting `courseRehomeRedirects`,
      built by mapping **one exported `REHOMED_COURSE_SLUGS` array** (the Phase-0 inventory) into the
      37 rules, each `permanent: true`. Carry a header comment stating that `course-id === slug` and
      that this module — never a `fundamentally-strong` prefix rule — owns that namespace (DD-43), in
      the style of `content-namespace.ts` — command: `npx nx run ayokoding-www:test:unit` —
      acceptance: the new suite passes and no existing redirect test breaks.
- [ ] [AI] **GREEN** — wire the module into `apps/ayokoding-www/next.config.ts` `redirects()` as
      `return [...learnReorgRedirects, ...courseRehomeRedirects, ...contentNamespaceRedirects];`
      (a temporary intermediate order; `content-namespace.ts` is still forward-direction and last —
      Phase 3.0 inverts it in place and moves it to the **front** of the array (DD-48), and Phase 3.1
      inserts `learnThreeBucketRedirects` after `courseRehome`, giving the final order
      `[...contentNamespaceRedirects, ...learnReorgRedirects, ...courseRehomeRedirects, ...learnThreeBucketRedirects]`) —
      command: `npx nx run ayokoding-www:typecheck && npx nx run ayokoding-www:build` — acceptance:
      both exit 0, and `grep -F "courseRehomeRedirects" apps/ayokoding-www/next.config.ts` prints
      exactly two lines (the import and the spread) — it prints nothing today, verified against the
      Phase-0 snapshot of the current `redirects()` expression.
- [ ] [AI] **REFACTOR** — confirm `REHOMED_COURSE_SLUGS` is the module's single source of truth: the
      rule builder derives both source and destination from one array element, so a slug typo cannot
      produce a half-correct rule — command:
      `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:lint` — acceptance: both exit 0
      and the 37-rule assertion still passes.

### 2.2 · Move the bundles

- [ ] [AI] For **every** slug in `REHOMED_COURSE_SLUGS`, `git mv <SE_OLD><slug>/ <COURSES><slug>/`
      (course-id = slug; no rename), preserving the full page bundle (`_index.md` + `overview.md` +
      `learning/` + `drilling/`) — acceptance:
      `ls apps/ayokoding-www/content/en/learn/fundamentally-strong/software-engineer | wc -l` returns
      **2** (only `_index.md` and `overview.md` remain; it returned **39** at Phase 0, verified), AND
      `for s in $(cat evidence/phase-0-rehome-slugs.txt); do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "MISSING $s"; done`
      prints nothing.
- [ ] [AI] **Prove the move rewrote nothing** —
      `git diff --cached --summary -M -- apps/ayokoding-www/content/en/learn/courses` — acceptance:
      every moved file appears as a pure rename; a content-modifying hunk here is a defect, not a
      cleanup. (The `prerequisites` frontmatter edit below is a **separate, later commit** precisely so
      this proof stays clean.)
- [ ] [AI] Regenerate and validate the derived indexes:
      `npx nx run ayokoding-www:generate-indexes && npx nx run ayokoding-www:validate-indexes && npx nx run ayokoding-www:build`
      — acceptance: all three exit 0.

### 2.3 · Prerequisite frontmatter (TDD)

- [ ] [AI] **RED** — write a failing unit test asserting that **every** directory under `<COURSES>`
      has an `_index.md` whose frontmatter declares a `prerequisites` array, that every named
      prerequisite resolves to another directory under `<COURSES>`, and that an empty array is
      accepted only where no library prerequisite exists — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: the suite fails, naming 37 courses with no
      `prerequisites` key. Falsifiable both ways: after the GREEN step the same command exits 0, and
      deleting the key from any one course re-fails it naming exactly that course.

  **Gherkin (binds) →** "Every re-homed course declares its prerequisites"

  ```gherkin
  Scenario: Every re-homed course declares its prerequisites
    Given the thirty-seven shipped topics and existing capstones have been re-homed into the course library
    When each re-homed course's canonical metadata is inspected
    Then every one declares a prerequisites list of course IDs
    And an empty list is accepted only for a course with no library prerequisite
    And every named prerequisite resolves to another course in the library
  ```

- [ ] [AI] **GREEN** — add `prerequisites: [course-id, ...]` to each re-homed `_index.md` frontmatter,
      naming only other library course IDs, per the shape reproduced in
      [tech-docs §Prerequisite frontmatter contract](./tech-docs.md#prerequisite-frontmatter-contract-reproduced-verbatim-canonical-owner-is-the-schema-plan)
      (the canonical owner is `ayokoding-learning-path-02-schema-and-prerequisite-dag`; if the two
      statements ever diverge, **the sibling's shape wins**) — command:
      `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:build` — acceptance: both exit 0;
      every re-homed course declares `prerequisites` (an empty list is allowed for roots).
- [ ] [AI] **REFACTOR** — re-read the declared edges as a set and confirm the graph is acyclic and that
      no course names itself — command: `npx nx run ayokoding-www:test:unit` — acceptance: exits 0
      with a cycle-detection assertion present in the suite. (The full DAG **resolver** is the sibling
      plan's; this is a data-shape guard on the 37 rows this plan authors.)

### 2.4 · Confirm the redirects resolve, and update the catalog

- [ ] [AI] **Confirm each re-homed course has its redirect** — the per-course rules authored in **§2.1
      of this phase** resolve old-URL → new-URL for all 37 moved courses — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: the `course-rehome` suite is green and its
      slug list equals the set of directories now under `<COURSES>`, checked in the same assertion.
      _(This step deliberately names §2.1 above and not a sibling plan's phase — the redirect table is
      owned here.)_
- [ ] [AI] Update `<COURSES>_index.md` (library landing) to list the re-homed catalog by course ID —
      acceptance: every catalog entry links to `/en/learn/courses/<course-id>` and the link validator
      below reports no broken link.
- [ ] [AI] Sweep any intra-course cross-links that referenced the old
      `fundamentally-strong/software-engineer/<slug>` path and repoint them to
      `/en/learn/courses/<course-id>` (Root Cause Orientation) — command:
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md links validate --exclude plans/done --exclude apps/ose-www/content`
      (the actual link-validation mechanism — **not** an `nx run` target; it also runs pre-commit via
      `lint-staged` for staged `.md` files). Note this form deliberately does **not** exclude
      `apps/ayokoding-www/content`, because that tree is exactly what this step changes — acceptance:
      zero broken links reported under `apps/ayokoding-www/content`.

### 2.5 · Preserve the "old-way" `_index.md` section browse (ADDITIVE model, DD-19)

The library/paths model is additive: a reader must keep navigating the material **the old way** (the
legacy hand-curated, spiral-ordered `_index.md` section tree) IN ADDITION to the new way (canonical
course pages, and later the path landings). Every impacted legacy section index is UPDATED (not
deleted), re-pointing each entry to wherever the content now lives.

- [ ] [AI] **RED** — write a failing e2e nav check in the paired `ayokoding-www-fe-e2e` project
      asserting the legacy ordered browse resolves end-to-end: from
      `.../fundamentally-strong/software-engineer/_index.md` (and the `fundamentally-strong/_index.md`
      parent + each per-topic `_index.md`), every listed entry link resolves to live content (the
      re-homed `/en/learn/courses/<course-id>` URL or a working redirect) — command:
      `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: the legacy-browse nav spec fails (links
      still point at drained `<SE_OLD>` locations). **Do NOT target `ayokoding-www:test:e2e`** — that
      target is `echo 'no-op: target not applicable for this project'` and always exits 0
      [Repo-grounded — `apps/ayokoding-www/project.json`], so a RED clause pointed at it can never
      fail.
  - _Suggested executor: `swe-e2e-dev`_

  **Gherkin (binds) →** "The legacy section-index browse still resolves after re-homing"

  ```gherkin
  Scenario: The legacy section-index browse still resolves after re-homing
    Given the 33 shipped topics have been re-homed into the course library
    When a reader browses the legacy fundamentally-strong software-engineer section index the old way
    Then every section-index entry links to live content at its /en/learn/courses/<course-id> URL or via a redirect
    And no legacy section-index entry resolves to a drained or missing location
  ```

- [ ] [AI] **RED** — write a failing e2e nav check asserting that a course reached via the legacy
      section-index browse resolves to the **single canonical course body** (same rendered content,
      same canonical URL) with no forked or duplicated body served for the legacy route — command:
      `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: the canonical-body spec fails (no
      assertion yet ties the legacy route to the canonical body).
  - _Suggested executor: `swe-e2e-dev`_

  **Gherkin (binds) →** "The legacy section-index browse resolves to the canonical course body"

  ```gherkin
  Scenario: The legacy section-index browse resolves to the canonical course body
    Given a course now lives at its canonical /en/learn/courses/<course-id> URL
    When a reader reaches it via the legacy section-index browse
    Then the browse resolves to that single canonical course body
    And no forked or duplicated body is served for the legacy route
  ```

  > **Split-time narrowing.** The source plan's scenario also asserted a
  > `/en/learn/paths/<path-id>` path landing resolves to the same body. Path landings are authored by
  > `ayokoding-learning-path-05-manifests` and do not exist when this plan runs, so that half was
  > unverifiable here and is carried by that plan instead. See
  > [prd.md §Acceptance Criteria](./prd.md#acceptance-criteria-gherkin).

- [ ] [AI] **GREEN** — enumerate every impacted `_index.md` under
      `apps/ayokoding-www/content/en/learn/fundamentally-strong/**`
      (`find apps/ayokoding-www/content/en/learn/fundamentally-strong -name _index.md` — esp.
      `.../software-engineer/_index.md`, each per-topic `_index.md`, and the
      `fundamentally-strong/_index.md` parent) and update each so every entry it lists is re-pointed to
      the new `/en/learn/courses/<course-id>` URL (or resolves via the redirect) — the legacy
      sections stay preserved and ordered, with no dead link and no orphaned section — command:
      `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: both e2e specs above now pass.
- [ ] [AI] **REFACTOR** — run
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md links validate --exclude plans/done --exclude apps/ose-www/content` + `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md heading-hierarchy validate` + `npm run lint:md` over the updated legacy `_index.md` tree (the heading-hierarchy validator
      already runs automatically pre-commit via `lint-staged` for every staged `.md` file; this step
      re-runs it explicitly over the full legacy tree) — acceptance: zero broken links; the old-way
      browse resolves to canonical bodies; all three validators green.
- [ ] [AI] **Preserve Q-E's three residual index pages and their redirect targets** — do **not** delete
      `fundamentally-strong/_index.md`, `software-engineer/_index.md`, or
      `software-engineer/overview.md`; the ruled fold-in (Q-E recommended answer A) targets a path
      landing authored by `ayokoding-learning-path-05-manifests`, so this plan hands the fold forward
      — acceptance: all three files still exist
      (`test -f apps/ayokoding-www/content/en/learn/fundamentally-strong/software-engineer/overview.md`
      returns 0) and each carries a note naming the ruled destination. See
      [tech-docs Q-E](./tech-docs.md#q-e--what-happens-to-fundamentally-strongs-three-residual-index-pages).

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [ ] [AI] `ls apps/ayokoding-www/content/en/learn/fundamentally-strong/software-engineer | wc -l`
      returns **2** (it returned **39** at Phase 0); every one of the 37 slugs resolves under
      `<COURSES>`.
- [ ] [AI] The bundle move is a pure-rename diff — no content-modifying hunk under `<COURSES>` in the
      move commit (DD-2/DD-41 discipline).
- [ ] [AI] `<REDIR>course-rehome.ts` exports **37** rules derived from one `REHOMED_COURSE_SLUGS`
      array; `course-rehome.unit.test.ts` is green including the slug-set equality assertion;
      `next.config.ts` spreads it after `learnReorgRedirects`.
- [ ] [AI] Every re-homed course declares `prerequisites`; the declared edge set is acyclic and
      self-reference-free.
- [ ] [AI] Both e2e old-way-browse specs pass; every impacted legacy `_index.md` is updated, not
      deleted; Q-E's three residual pages still exist with their ruled destination noted.
- [ ] [AI] `npx nx run ayokoding-www:build` + `:typecheck` + `:lint` + `:test:unit` +
      `:validate-indexes` and `npx nx run ayokoding-www-fe-e2e:test:e2e` exit 0.
- [ ] [AI] `md links validate` (excluding `plans/done` and `apps/ose-www/content`) and
      `md heading-hierarchy validate` report no error over the changed tree.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: every shipped course lives at its canonical `/en/learn/courses/<id>` URL with a
> working 308 and declared prerequisites, and the legacy `_index.md` section browse still resolves the
> old way (additive). No manifest exists yet, so every course renders its canonical view. Production
> serves a coherent site. Safe to stop indefinitely. To resume:
> `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www-fe-e2e:test:e2e`.

---

## Phase 3: Relocate the six non-course domains into `legacy/` + per-domain 308 redirects

> _Suggested executor: `swe-typescript-dev`_ (redirect module + unit test + `next.config.ts` wiring)
> _plus `apps-ayokoding-www-content-fixer`_ for the two hub-file rewrites.
>
> **Why this is one phase, not two.** The six `git mv`s and the redirect module must land **together**:
> a live 308 pointing at a not-yet-moved path 404s, and a moved path with no 308 breaks ~1,148 URLs.
> Neither half is a safe stopping state, so the phase boundary sits after both.
>
> **Why it sits here.** After Phase 2 (so `courses/` already exists and `en/learn/` is never
> transiently `legacy/`-only) and before every downstream plan's manual verification (so they see the
> final three-bucket shape rather than a hybrid one). See
> [tech-docs §Learn-Section IA](./tech-docs.md#learn-section-ia--the-three-bucket-model), DD-40 through
> DD-45, and the BEFORE/AFTER trees at
> [tech-docs §Content tree — AFTER](./tech-docs.md#content-tree--after-target-state).
>
> **Open questions.** Every step below executes the **recommended default** of its governing question
> and names the alternative inline, so an overturned ruling is a bounded edit:
> [Q-A](./tech-docs.md#q-a--is-legacy-a-staging-pen-or-a-permanent-archive) (staging pen),
> [Q-B](./tech-docs.md#q-b--does-the-id-locale-get-the-same-three-bucket-shape-now) (`id` out of
> scope), [Q-C](./tech-docs.md#q-c--if-id-is-in-scope-are-the-bucket-segments-translated) (moot while
> Q-B = A), [Q-D](./tech-docs.md#q-d--seo-treatment-of-legacy) (indexed + banner),
> [Q-E](./tech-docs.md#q-e--what-happens-to-fundamentally-strongs-three-residual-index-pages) (fold
> into the path landing — handed forward by Phase 2),
> [Q-F](./tech-docs.md#q-f--what-happens-to-enlearnoverviewmd) (keep `overview.md`, rewritten).

### 3.0 · De-namespacing — retire the `/c/` content route (DD-48)

> **Site-wide scope, distinct from DD-45.** This sub-phase covers every namespaced section — `en/learn`,
> `en/rants`, `id/belajar`, `id/celoteh`, `id/konten-video` — not just `learn`. It does **not** extend
> the three-bucket IA shape to `id` (DD-45 stays deferred); it only removes the `/c/` URL segment for
> `id`'s existing sections. See
> [tech-docs.md's De-namespacing section](./tech-docs.md#de-namespacing--retiring-the-c-content-route-dd-48)
> for the full file inventory, the collision verdict, and the churn-sequencing reasoning. **This
> sub-phase runs FIRST in Phase 3**, before §3.1, because §3.1's redirect-module wiring order assumes
> `content-namespace.ts` already runs first (DD-48).

- [ ] [AI] **RED (unit)** — invert the five assertions in
      `<REDIR>content-namespace.unit.test.ts` in place: each currently asserts a bare source
      (`/en/learn`, `/en/rants`, `/id/belajar`, `/id/celoteh`, `/id/konten-video`) redirects to its
      `/c/`-prefixed destination; rewrite each to assert the **opposite** — a `/c/`-prefixed source
      redirects to its bare destination — and add a sixth, negative assertion that no rule in the
      module has a `/c/`-containing destination — command: `npx nx run ayokoding-www:test:unit` —
      acceptance: the suite fails (the still-forward `content-namespace.ts` does not satisfy the
      inverted assertions). Falsifiable both ways: the pre-inversion suite passes against today's
      `content-namespace.ts` (verified in Phase 0), and fails the moment these assertions are rewritten.

  **Gherkin (binds) →** every scenario in `content-namespace-redirects.feature` (filename kept; see
  [Naming decisions](./tech-docs.md#naming-decisions-so-sibling-plans-are-not-silently-broken)) —
  invert each scenario's Given/When/Then to assert a stale `/c/`-prefixed bookmark 308s to the bare
  URL, not the reverse.

- [ ] [AI] **RED (specs)** — invert the Gherkin content of `content-namespace-redirects.feature` in
      place (filename kept) and update its paired `content-namespace.steps.ts` step definitions to
      match — command: `npx nx run ayokoding-www:specs:behavior:coverage` — acceptance: fails (step
      bindings still assert the old forward direction against the still-forward production code).
  - _Suggested executor: `specs-maker`_

- [ ] [AI] **GREEN** — invert `<REDIR>content-namespace.ts` in place: for all five rules
      (`en/learn`, `en/rants`, `id/belajar`, `id/celoteh`, `id/konten-video`), swap `source` and
      `destination` so the `/c/`-prefixed form becomes the source (the stale bookmark) and the bare form
      becomes the destination (the canonical URL) — command: `npx nx run ayokoding-www:test:unit` —
      acceptance: the inverted unit suite passes.

- [ ] [AI] **GREEN** — delete the retired content-tree route:
      `git rm "apps/ayokoding-www/src/app/[locale]/(content)/c/[...slug]/page.tsx" "apps/ayokoding-www/src/app/[locale]/(content)/c/[...slug]/page.unit.test.ts"`
      — acceptance: both `test -e` checks return non-zero (they returned 0 in Phase 0).

- [ ] [AI] **GREEN** — relocate the browse index (no bare home to inherit — see
      [tech-docs.md](./tech-docs.md#the-c-browse-index-has-no-bare-home-to-inherit)):
      `git mv "apps/ayokoding-www/src/app/[locale]/(content)/c/page.tsx" "apps/ayokoding-www/src/app/[locale]/(content)/browse/page.tsx"`,
      then repoint its own internal canonical-URL string from `` `/${locale}/c` `` to
      `` `/${locale}/browse` `` — acceptance: `test -f "apps/ayokoding-www/src/app/[locale]/(content)/browse/page.tsx"`
      returns 0; `test -e "apps/ayokoding-www/src/app/[locale]/(content)/c/page.tsx"` returns non-zero.

- [ ] [AI] **GREEN** — widen `[...slug]/page.tsx` to serve both loose pages and the full content tree:
      merge the deleted `c/[...slug]/page.tsx`'s content-tree lookup, `generateStaticParams`, and
      `generateMetadata`/canonical-URL logic into the surviving bare `[...slug]/page.tsx`, and merge its
      test file (`c/[...slug]/page.unit.test.ts`'s assertions, before its own deletion above, into
      `[...slug]/page.unit.test.ts`) — command: `npx nx run ayokoding-www:test:unit` — acceptance: the
      merged suite passes, covering both loose-page and content-tree slugs in one route.

- [ ] [AI] **GREEN — collision negative check** — confirm the widened route introduces no routing
      collision, per the verdict in
      [tech-docs.md's Collision verdict](./tech-docs.md#collision-verdict--widening-slug-against-tools-and-the-locale-root):
      `grep -E '"tools"|"browse"' apps/ayokoding-www/src/features/content/core/content-url.ts`
      prints nothing (no `LOOSE_PAGE_ALLOWLIST` entry is `tools` or `browse`), AND
      `find apps/ayokoding-www/content/en apps/ayokoding-www/content/id -maxdepth 1 -type d \( -name 'tools' -o -name 'browse' \)`
      prints nothing (no top-level content directory is named `tools` or `browse`) — acceptance: both
      checks print nothing, as they do today (verified in Phase 0); either printing a match would mean
      the collision verdict no longer holds and this step must halt before proceeding.

- [ ] [AI] **GREEN** — update `contentUrl()` in `features/content/core/content-url.ts`: delete the
      `/c/`-prefix branch so it uniformly returns `/{locale}` for the root slug and
      `/{locale}/{normalizeSlug(slug)}` otherwise — command: `npx nx run ayokoding-www:test:unit` —
      acceptance: `content-url.test.ts` passes with the updated uniform-join assertions.
- [ ] [AI] **GREEN — resolve the `LOOSE_PAGE_ALLOWLIST` open question (delivery-time verification, not
      an assumed fact)** — read `generateStaticParams` in the merged `[...slug]/page.tsx` and the
      content indexer it calls (`index.contentMap` construction) to determine whether the two loose
      pages (`about-ayokoding`/`terms-and-conditions` for `en`, `tentang-ayokoding`/`syarat-dan-ketentuan`
      for `id`) are already members of `index.contentMap` for their locale: if yes, remove
      `LOOSE_PAGE_ALLOWLIST` and the now-fully-dead `isLoosePage()` entirely; if no, keep
      `LOOSE_PAGE_ALLOWLIST` and union it into `generateStaticParams`, and still remove `isLoosePage()`
      (dead regardless, per [tech-docs.md](./tech-docs.md#contenturl-and-loose_page_allowlist-after-the-merge))
      — acceptance: the chosen outcome is recorded in a one-line code comment at
      `LOOSE_PAGE_ALLOWLIST`'s declaration (or at its removal site, in the commit message) stating which
      branch was taken and why; `npx nx run ayokoding-www:test:unit` passes either way.
- [ ] [AI] **GREEN** — update `features/content/core/slug.ts` and
      `features/content/core/content-link-rewrite.ts`'s `resolveContentHref()` doc comments and any
      `/c/`-namespace-aware logic to reflect the uniform bare join — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: both files' test suites pass.
- [ ] [AI] **GREEN** — collapse `breadcrumb.tsx`'s `contentHrefs` prop: `hrefFor` always resolves
      through `contentUrl()`; remove the prop and its call-site plumbing in `sidebar-tree.tsx`,
      `resizable-sidebar.tsx`, and `prev-next.tsx` (test fixtures `breadcrumb.test.tsx`,
      `prev-next.test.tsx`, `sidebar-tree.test.tsx`, `resizable-sidebar.test.tsx` updated to match) —
      command: `npx nx run ayokoding-www:test:unit` — acceptance: all four suites pass with the prop
      removed.
- [ ] [AI] **GREEN** — update `browse-index.tsx` to link to the relocated `browse/` route instead of
      `/c`, and update its and `section-card.tsx`'s test fixtures (`browse-index.test.tsx`,
      `section-card.test.tsx`) to bare URLs — command: `npx nx run ayokoding-www:test:unit` —
      acceptance: both suites pass.
- [ ] [AI] **GREEN** — update the four test-fixture-only files' expected URLs to the bare form —
      `app/sitemap.unit.test.ts`, `app/feed.xml/route.unit.test.ts`,
      `features/search/shell/search-dialog.test.tsx`, `features/app-shell/shell/landing.test.tsx` —
      production `sitemap.ts`/`feed.xml/route.ts` already derive every URL from `contentUrl()` (DD-44),
      so no production code changes here — command: `npx nx run ayokoding-www:test:unit` — acceptance:
      all four suites pass, and the regenerated sitemap/feed now emit bare canonical URLs (verified by
      the same test), avoiding a **second, avoidable** disagreement between the sitemap/feed and the
      live URLs on top of the one-time `<guid>` churn already accounted for in
      [prd.md's Product-Level Risks](./prd.md#product-level-risks).
- [ ] [AI] **GREEN** — invert `ia-navigation-revamp.feature` and `learn-reorg-redirects.feature`'s
      scenario content in place (filenames kept) and update their paired
      `ia-navigation-revamp.steps.ts` / `landing.steps.ts` step definitions to match — command:
      `npx nx run ayokoding-www:specs:behavior:coverage` — acceptance: exits 0, all three feature files'
      scenarios pass against the now-inverted production code.
- [ ] [AI] **GREEN** — reorder `apps/ayokoding-www/next.config.ts` `redirects()` to place
      `contentNamespaceRedirects` **first**: `return [...contentNamespaceRedirects, ...learnReorgRedirects, ...courseRehomeRedirects];`
      — this sub-step's own intermediate order (§3.1 below appends `learnThreeBucketRedirects` last) —
      command: `npx nx run ayokoding-www:typecheck && npx nx run ayokoding-www:build` — acceptance: both
      exit 0.
- [ ] [AI] **REFACTOR — loop-safety invariant, falsifiable both ways** —
      `grep -rn '"/[a-z][a-z]/c/' apps/ayokoding-www/src/redirects/` — acceptance: empty (no currently-
      wired module redirects a bare URL back into `/c/`). Falsifiable the other way: temporarily
      restoring the pre-inversion `content-namespace.ts` makes this command print 5 matching lines
      (verified in Phase 0 before this sub-phase started).
- [ ] [AI] **REFACTOR** — run the full affected suite over everything touched this sub-phase:
      `npx nx affected -t typecheck lint test:unit specs:behavior:coverage` — acceptance: all exit 0.

### 3.1 · Redirect module (TDD)

- [ ] [AI] **RED** — write a failing unit test at `<REDIR>learn-three-bucket.unit.test.ts`
      _(New test)_, mirroring the existing `<REDIR>content-namespace.unit.test.ts` structure
      [Repo-grounded], asserting all six properties: (a) exactly **6** rules, single tier — one per
      relocated domain, not 12 (the `/c`-form tier is unreachable dead code once §3.0's
      `content-namespace.ts` inversion always strips `/c/` first — see
      [tech-docs.md's Module 2](./tech-docs.md#module-2--learn-three-bucketts-per-domain-dd-42-collapsed-to-one-tier-by-dd-48));
      (b) every rule `permanent: true` with non-empty `source`/`destination`; (c) each destination
      equals its source with `legacy/` inserted at the bucket position; (d) **no** rule whose source
      matches `/^\/en\/learn\/:path\*$/` (the self-recursing blanket, DD-42); (e) **no** rule whose
      first path segment after `learn/` is `courses`, `paths`, or `fundamentally-strong`
      (DD-42/DD-43); (f) **no** rule's `source` or `destination` contains a `/c/` segment (loop-safety
      invariant, DD-48); (g) the six expected domain names are all covered — command:
      `npx nx run ayokoding-www:test:unit` — acceptance: the suite fails with `learn-three-bucket`
      module not found. Falsifiable both ways: the module does not exist today
      (`test -f apps/ayokoding-www/src/redirects/learn-three-bucket.ts` returns non-zero, verified in
      Phase 0) and returns 0 after the GREEN step.

  **Gherkin (binds) →** "The legacy redirect never swallows the courses or paths buckets"; "A
  re-homed fundamentally-strong course is not routed into the legacy bucket"

  ```gherkin
  Scenario: The legacy redirect never swallows the courses or paths buckets
    Given the legacy bucket redirect rules are configured
    When a reader requests a canonical course URL or a path landing URL
    Then the app serves the page without redirecting it
    And no redirect rule declares a bucket-wide learn-section wildcard source

  Scenario: A re-homed fundamentally-strong course is not routed into the legacy bucket
    Given the fundamentally-strong topic directories were collapsed into flat course bodies
    When a reader requests a legacy fundamentally-strong course URL
    Then the app redirects to that course's canonical course URL
    And no legacy-bucket rule matches the fundamentally-strong prefix
  ```

- [ ] [AI] **GREEN** — author `<REDIR>learn-three-bucket.ts` _(New file)_ exporting
      `learnThreeBucketRedirects` with **6** rules, single tier — one bare rule per domain,
      `/en/learn/<domain>/:path*` → `/en/learn/legacy/<domain>/:path*`, each `permanent: true`, for
      `software-engineering`, `artificial-intelligence`, `information-security`,
      `personal-development`, `it-governance`, `business`. No `/c`-form tier — it would be unreachable
      dead code, since §3.0's inverted `content-namespace.ts` (wired first — see below) already strips
      any `/c/`-prefixed request down to its bare form before this module ever runs. Carry a header
      comment stating the blanket ban, the tier collapse and why (DD-48), and the ordering requirement,
      in the style of `content-namespace.ts` — command: `npx nx run ayokoding-www:test:unit` —
      acceptance: the new suite passes; no existing redirect test breaks.
- [ ] [AI] **GREEN** — wire the module into `apps/ayokoding-www/next.config.ts` `redirects()`,
      completing the array §3.0 started, as:
      `return [...contentNamespaceRedirects, ...learnReorgRedirects, ...courseRehomeRedirects, ...learnThreeBucketRedirects];`
      — the order is load-bearing (DD-48, re-derived from first principles, not the pre-inversion
      order): `contentNamespace` **first** so any stale `/c/`-prefixed request is stripped to its bare
      form before any other rule evaluates (a rule positioned after it would never see a `/c/`-prefixed
      URL, since bare-only rules can't match one) — omitting this would leave `/c/`-prefixed requests
      for renamed/relocated domains unresolved, since none of the other three modules match a
      `/c/`-prefixed source; `learnReorg` next so historical within-`/en/learn/` renames resolve to
      their canonical domain; `courseRehome` before `learnThreeBucket` so the more specific per-course
      rules win — command: `npx nx run ayokoding-www:typecheck && npx nx run ayokoding-www:build` —
      acceptance: both exit 0, and `grep -F "learnThreeBucketRedirects" apps/ayokoding-www/next.config.ts`
      prints exactly two lines (the import and the spread) — it prints nothing before this step,
      verified.
- [ ] [AI] **REFACTOR** — extract the six domain names into one exported `RELOCATED_DOMAINS` array the
      single tier maps over, so a seventh domain cannot be added and forgotten — command:
      `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:lint` — acceptance: both exit 0;
      the 6-rule assertion still passes.

### 3.2 · Relocate the six domains (pure `git mv`, DD-41)

- [ ] [AI] Create the bucket root and `git mv` each domain, preserving its sub-taxonomy verbatim:
      `mkdir -p apps/ayokoding-www/content/en/learn/legacy && for d in software-engineering artificial-intelligence information-security personal-development it-governance business; do git mv "apps/ayokoding-www/content/en/learn/$d" "apps/ayokoding-www/content/en/learn/legacy/$d"; done`
      — acceptance: `find apps/ayokoding-www/content/en/learn/legacy -name '*.md' | wc -l` returns
      **1148**, and
      `for d in software-engineering artificial-intelligence information-security personal-development it-governance business; do test -e "apps/ayokoding-www/content/en/learn/$d" && echo "STILL AT ROOT $d"; done`
      prints nothing. Falsifiable both ways: that second command prints all six lines today, and the
      `find` fails outright because the directory does not exist yet (verified in Phase 0).
- [ ] [AI] **Prove the move rewrote nothing** —
      `git diff --cached --stat -M --diff-filter=M -- apps/ayokoding-www/content/en/learn/legacy` —
      acceptance: **no** modified (`M`) content file under `<LEGACY>` other than files this phase
      explicitly authors; `git diff --cached --summary -M` shows the relocated files as pure renames
      (DD-41). A content-modifying hunk here is a defect, not a cleanup.

  **Gherkin (binds) →** "The relocation rewrites no page content"

  ```gherkin
  Scenario: The relocation rewrites no page content
    Given the six non-course learn-section domains have been relocated
    When the relocation commit's diff is inspected
    Then every relocated file appears as a pure rename with no content change
    And the only edited content files are the section overview and the new legacy bucket index
  ```

- [ ] [AI] Author `<LEGACY>_index.md` _(New file)_ — **required**, not optional: `generate-indexes`
      only rewrites `_index.md` files that already exist
      [Repo-grounded — `processAllIndexFiles` filters `allContent.filter(c => c.isSection)` in
      `apps/ayokoding-www/src/features/content/shell/index-generator.ts`], and without it
      `buildTreeForLocale` synthesizes a `weight: 0` "Legacy" node that would sort **first** in the
      sidebar, ahead of `courses/` and `paths/`
      [Repo-grounded — `apps/ayokoding-www/src/features/content/core/tree-builder.ts`]. Give it
      `title`, `date`, `draft: false`, and an explicit `weight` **greater** than the `courses/` and
      `paths/` weights set in Phase 1, plus the Q-D landing notice per
      [prd.md Screen 4](./prd.md#ui-design-funnel--screen-4--legacy-bucket-landing-and-page-banner) —
      acceptance: `test -f apps/ayokoding-www/content/en/learn/legacy/_index.md` returns 0 (returns
      non-zero before this step, verified), its `weight` is numerically greater than both Phase-1
      weights, and after `npx nx run ayokoding-www:build` the sidebar order under `learn` is `paths`,
      `courses`, `legacy` (confirmed in §3.5's Playwright pass, not asserted by grep).

  **Gherkin (binds) →** "The legacy bucket landing tells a reader what the bucket is"

  ```gherkin
  Scenario: The legacy bucket landing tells a reader what the bucket is
    Given a reader opens the legacy bucket landing page
    When the page renders
    Then it states that the material is older and kept for reference while the course library fills
    And it links onward to the course library and to the paths hub
  ```

- [ ] [AI] Rewrite the hand-authored `apps/ayokoding-www/content/en/learn/overview.md` so its inventory
      names the **three buckets** instead of the six domains (Q-F recommended answer A — keep it as the
      section hub page; do **not** move its prose into `_index.md`, which `generate-indexes`
      machine-rewrites and would clobber) — acceptance:
      `grep -oE '/en/learn/(paths|courses|legacy)' apps/ayokoding-www/content/en/learn/overview.md | sort -u | wc -l`
      returns **3**, AND
      `grep -oE '\(/en/learn/(software-engineering|artificial-intelligence|information-security|personal-development|it-governance|business)' apps/ayokoding-www/content/en/learn/overview.md | wc -l`
      returns **0**. Falsifiable both ways: today the first returns **0** and the second returns **6**
      (the file links all six domains at their bare pre-`/c` URLs, verified).
- [ ] [AI] Regenerate the derived artifacts: `npx nx run ayokoding-www:generate-indexes` then
      `npx nx run ayokoding-www:generate-search-data` — acceptance: both exit 0;
      `npx nx run ayokoding-www:validate-indexes` exits 0 afterward (proving regeneration converged);
      `generated/search-data.json` is rewritten and every relocated doc's `slug` now begins
      `learn/legacy/`.

  **Gherkin (binds) →** "The learn section exposes exactly three structural buckets"; "Navigation
  surfaces follow the relocated tree with no code change"

  ```gherkin
  Scenario: The learn section exposes exactly three structural buckets
    Given the learn-section IA revamp has landed
    When the content tree under the en learn section is inspected
    Then its only structural buckets are paths, courses, and legacy
    And no former subject domain remains as a direct child of the learn section
    And the section keeps its own index and overview hub pages

  Scenario: Navigation surfaces follow the relocated tree with no code change
    Given the six domains now live under the legacy bucket
    When the sidebar tree, browse index, sitemap, feed, and search data are regenerated
    Then each lists every relocated page at its new legacy URL
    And no navigation source file required a hardcoded domain slug to be edited
  ```

- [ ] [AI] **Prove DD-44's zero-code-change claim — scoped to the six-domain relocation (§3.2), not
      the whole phase** — confirm this sub-step's own staged diff touches no production navigation
      source file:
      `git diff --cached --name-only -- apps/ayokoding-www/src/features/navigation apps/ayokoding-www/src/features/content apps/ayokoding-www/src/app` —
      acceptance: prints nothing at this point in the phase. Falsifiable both ways: touching any of
      those files in this sub-step's own commit makes it print that path. **DD-44's claim is narrower
      than "Phase 3 makes no production code changes"** — §3.0's DD-48 de-namespacing work legitimately
      edits files under all three of these directories (`c/[...slug]/page.tsx` deletion,
      `[...slug]/page.tsx` widening, `content-url.ts`, `breadcrumb.tsx`, and others per the
      [tech-docs.md file inventory](./tech-docs.md#file-inventory-measured-do-not-re-derive-re-verify-what-an-acceptance-clause-cites)) in its **own**, earlier
      commit(s); this check runs after that work is already committed (not staged), so it verifies only
      that the relocation itself (§3.2) adds no further navigation-code edits on top of DD-48's
      explicitly-scoped ones.

### 3.3 · Specs + e2e (Gherkin-bound)

- [ ] [AI] **RED (specs)** — author `<NAVSPECS>learn-three-bucket.feature` _(New file)_ beside the
      existing `content-namespace-redirects.feature` [Repo-grounded], carrying the three-bucket
      scenarios from [prd.md](./prd.md#three-bucket-learn-section-ia) — command:
      `npx nx run ayokoding-www:specs:behavior:coverage` — acceptance: fails (no step bindings yet).
  - _Suggested executor: `specs-maker`_
- [ ] [AI] **RED (e2e)** — write failing Playwright specs in the paired `ayokoding-www-fe-e2e` project
      asserting: one relocated URL per domain 308s to its `legacy/` address in **both** inbound forms
      (bare `/en/learn/<domain>/…` in one hop, and a stale `/c`-bookmark `/en/c/learn/<domain>/…` in
      two hops); the deep path
      `/en/learn/software-engineering/programming-languages/python/by-example/advanced` lands at its
      `legacy/` twin with every segment below the domain unchanged; a historical `learn-reorg` source
      (`/en/learn/human/…`) chains to `/en/learn/legacy/personal-development/…`; a `courses/` URL and
      a `paths/` URL are **not** rewritten; and an old `fundamentally-strong` course URL still resolves
      to `/en/learn/courses/<id>` (DD-43) — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` —
      acceptance: the new specs fail. **Do NOT target `ayokoding-www:test:e2e`** — that target is
      `echo 'no-op: target not applicable for this project'` and always exits 0
      [Repo-grounded — `apps/ayokoding-www/project.json`], so a RED clause pointed at it can never
      fail.
  - _Suggested executor: `swe-e2e-dev`_

  **Gherkin (binds) →** "A relocated legacy domain URL redirects to its legacy address"; "A deep
  legacy path keeps its sub-taxonomy verbatim"

  ```gherkin
  Scenario: A relocated legacy domain URL redirects to its legacy address
    Given a page previously lived at a learn-section domain that is not a course or a path
    When a reader requests that page's old URL
    Then the app permanently redirects to the same page under the legacy bucket
    And the rest of the path after the domain segment is preserved unchanged

  Scenario: A deep legacy path keeps its sub-taxonomy verbatim
    Given a legacy page previously lived several levels below its domain
    When a reader follows the redirect to its new legacy address
    Then every path segment below the domain is unchanged
    And the page body is byte-identical to the body served before the relocation
  ```

- [ ] [AI] **GREEN (specs + e2e)** — implement the step bindings so both the `<NAVSPECS>` scenarios and
      the e2e specs execute against the landed module and moved tree — command:
      `npx nx run ayokoding-www:specs:behavior:coverage && npx nx run ayokoding-www-fe-e2e:test:e2e` —
      acceptance: both exit 0.
- [ ] [AI] **REFACTOR** — run
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md links validate --exclude plans/done --exclude apps/ose-www/content` + `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md heading-hierarchy validate` + `npm run lint:md` over the relocated tree and the two rewritten hub files (the actual
      link/heading mechanism — **not** `nx run` targets; both also run pre-commit via `lint-staged` for
      staged `.md`) — acceptance: zero broken links; all validators green.

### 3.4 · Screen 4 design funnel (Q-D)

> **This plan's slice of the DD-47 matrix is six renders.** Two options × three viewports at
> 375 / 768 / 1280 px, named per
> [prd.md §Hi-fi asset matrix](./prd.md#hi-fi-asset-matrix--this-plans-slice), each rendered from its
> own `assets/src/<stem>.html`. Enumerated per asset — a single "render the Screen 4 mockups" checkbox
> could be ticked with four of six missing. Option C is deliberately **not** rendered: it is Option B's
> landing plus a `robots` metadata change, which a mockup cannot depict.
>
> **Cross-plan note on DD-47.** DD-47's full matrix is **30** renders (5 screens × 2 options × 3
> viewports) spread across **two** plans — **6 here** and **24 in
> `ayokoding-learning-path-03-navigation-ui`** (Screens 0–3). Every asset clause in this plan
> therefore asserts **6**, scoped to this plan's own `assets/` folder, and never 30. A reader auditing
> DD-47 against this plan alone must not read 6 as under-delivery.

- [ ] [AI] Author the six render sources under `assets/src/` _(New files)_ —
      `legacy-landing-option-{a,b}-{mobile,tablet,desktop}.html`, each a static HTML+CSS mock at its
      target width, reusing the app's existing token palette — acceptance:
      `find assets/src -name 'legacy-landing-option-*.html' | wc -l` returns **6** (returns 0 before
      this step — the `assets/` folder does not exist yet, verified).
- [ ] [AI] Render `assets/legacy-landing-option-a-mobile.png` from
      `assets/src/legacy-landing-option-a-mobile.html` at 375 px — acceptance: file exists; the render
      shows a single-column domain list with the per-page banner above the H1.
- [ ] [AI] Render `assets/legacy-landing-option-a-tablet.png` from
      `assets/src/legacy-landing-option-a-tablet.html` at 768 px — acceptance: file exists; the render
      shows a two-column domain list with the sidebar column present.
- [ ] [AI] Render `assets/legacy-landing-option-a-desktop.png` from
      `assets/src/legacy-landing-option-a-desktop.html` at 1280 px — acceptance: file exists.
- [ ] [AI] Render `assets/legacy-landing-option-b-mobile.png` from
      `assets/src/legacy-landing-option-b-mobile.html` at 375 px — acceptance: file exists; the
      relocated page shows **no** banner (the option's defining absence).
- [ ] [AI] Render `assets/legacy-landing-option-b-tablet.png` from
      `assets/src/legacy-landing-option-b-tablet.html` at 768 px — acceptance: file exists.
- [ ] [AI] Render `assets/legacy-landing-option-b-desktop.png` from
      `assets/src/legacy-landing-option-b-desktop.html` at 1280 px — acceptance: file exists.
- [ ] [AI] **Embed all six in `prd.md`'s Screen 4 funnel** with viewport-specific descriptive alt text
      (each naming what differs at that width, never a copy of the desktop text) — acceptance:
      `grep -o "assets/legacy-landing-option-[ab]-[a-z]*\.png" prd.md | sort -u | wc -l` returns **6**
      (returns **0** before this step, verified — the prose mentions of the naming convention use brace
      notation and do not match this pattern), AND
      `find assets -name 'legacy-landing-option-*-*.png' | wc -l` returns **6** — this plan's complete
      slice, AND
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md links validate --exclude plans/done --exclude apps/ayokoding-www/content --exclude apps/ose-www/content`
      resolves every new `![]()` target.
- [ ] [AI] **Record the Screen 4 selection** — replace `prd.md`'s
      "**Selection: PENDING…**" line with the ruled answer once Q-D is settled; under the recommended
      default (option A) that is "**Selected: Option A — indexed + landing notice + per-page banner**"
      — acceptance: `grep -F "Selection: PENDING" prd.md` prints nothing (it prints exactly one line
      today, verified) AND `grep -F "Selected: Option A" prd.md` prints at least one line (it prints
      nothing today, verified — this plan authored no selection line).
- [ ] [AI] Apply the ruled Q-D treatment: under option A, add the `Alert`-based "legacy / superseded"
      notice to `<LEGACY>_index.md` and the per-page banner affordance; under option C instead set
      `robots: noindex` metadata for the bucket. Reuse the existing composite `Alert` primitive — **no
      net-new component** (DD-44) — acceptance: the ruled treatment is present, `grep -rF "Alert"`
      finds the reused primitive rather than a new component file, and
      `npx nx run ayokoding-www:build` exits 0.

### 3.5 · Manual verification (`en`, all breakpoints)

- [ ] [AI] Confirm the locale scope: this plan's content changes are `en`-only per DD-45, and
      `id/belajar/` is untouched — command:
      `find apps/ayokoding-www/content/id/belajar -name '*.md' | wc -l` — acceptance: returns **53**
      (its Phase-0 baseline). No `id` walk-through is fabricated for content that does not exist.
- [ ] [AI] Start the dev server (`npx nx dev ayokoding-www`) and, via Playwright MCP at
      375 / 768 / 1280 px, open `/en/learn`, `/en/learn/legacy`, one relocated page per domain, and
      one deep relocated page; confirm the sidebar shows `learn` with exactly `paths`, `courses`,
      `legacy` (in that order); confirm the legacy page breadcrumb reads
      `Home / Browse / Learn / Legacy / <domain> / <title>` and — per the
      [prd Screen 4 responsive strategy](./prd.md#responsive-strategy-mobile--tablet--desktop-mobile-first)
      — **does not wrap to multiple lines at 375 px**; confirm `browser_console_messages` is clean —
      acceptance: all behaviors correct; zero console errors at every breakpoint.
- [ ] [AI] Capture one screenshot per screen per breakpoint to
      `evidence/phase-3-<screen>-en-<breakpoint>px.png` — acceptance: the files exist in `evidence/`
      and are referenced from this checklist by `![alt](./evidence/…)` links.
- [ ] [AI] **De-namespacing sweep across every namespaced section, `en` and `id` alike (DD-48) — a
      URL-layer check, distinct from DD-45's content-structure deferral below.** Via Playwright MCP,
      open a bare URL under each of the five sections — `/en/learn/…`, `/en/rants/…`, `/id/belajar/…`,
      `/id/celoteh/…`, `/id/konten-video/…` — and confirm each renders directly with no redirect, AND
      request the equivalent stale `/c`-prefixed bookmark for each (`/en/c/learn/…`, `/en/c/rants/…`,
      `/id/c/belajar/…`, `/id/c/celoteh/…`, `/id/c/konten-video/…`) and confirm each 308s to its bare
      form — acceptance: all five bare URLs render with zero redirect, all five stale-`/c` URLs 308 to
      their bare form, and no request loops. This confirms de-namespacing is site-wide, not
      `en/learn`-only, and confirms `id`'s de-namespacing is live even though `id`'s three-bucket IA
      shape stays deferred (DD-45, checked separately below — these are different axes, per
      [tech-docs.md's scope note](./tech-docs.md#de-namespacing--retiring-the-c-content-route-dd-48)).
- [ ] [AI] **Record the `id` deferral explicitly (DD-45 / Q-B)** — confirm
      `test -e apps/ayokoding-www/content/id/belajar/legacy` returns non-zero and
      `test -e apps/ayokoding-www/content/id/belajar/kursus` returns non-zero; then write the deferral
      note into this checklist naming Q-B's recommended answer — acceptance: both checks hold and the
      note is written here, not left implicit.

  **Gherkin (binds) →** "The Indonesian locale is left unchanged and the deferral is recorded"

  ```gherkin
  Scenario: The Indonesian locale is left unchanged and the deferral is recorded
    Given the learn-section IA revamp is scoped to the English locale
    When the Indonesian content tree is inspected after the revamp
    Then its section is unchanged with no bucket directories and no relocation
    And the plan records the Indonesian deferral explicitly as a non-goal
  ```

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [ ] [AI] `ls apps/ayokoding-www/content/en/learn` lists exactly `_index.md`, `courses`, `legacy`,
      `overview.md`, `paths` — the three structural buckets plus the two hub files (DD-40/DD-45).
      Falsifiable both ways: it lists seven domain directories plus the two hub files today.
- [ ] [AI] `find apps/ayokoding-www/content/en/learn/legacy -name '*.md' | wc -l` returns **1148**, and
      the relocation diff shows pure renames with no content-modifying hunk under `<LEGACY>` (DD-41).
- [ ] [AI] `<REDIR>learn-three-bucket.ts` exports **6** rules, single tier, from one
      `RELOCATED_DOMAINS` array (DD-42, collapsed by DD-48); `learn-three-bucket.unit.test.ts` is green
      **including** the negative assertions (no blanket source; no `courses`/`paths`/
      `fundamentally-strong` source prefix; no rule's source or destination contains `/c/`).
- [ ] [AI] `next.config.ts`'s `redirects()` array is, in order:
      `[...contentNamespaceRedirects, ...learnReorgRedirects, ...courseRehomeRedirects, ...learnThreeBucketRedirects]`
      — `contentNamespaceRedirects` **first** (DD-48, re-derived order, not the pre-inversion order).
- [ ] [AI] **DD-48's de-namespacing file inventory is complete** — every disposition in
      [tech-docs.md's File inventory](./tech-docs.md#file-inventory-measured-do-not-re-derive-re-verify-what-an-acceptance-clause-cites) is applied:
      `test -e "apps/ayokoding-www/src/app/[locale]/(content)/c/[...slug]/page.tsx"` returns non-zero
      (route deleted); `test -e "apps/ayokoding-www/src/app/[locale]/(content)/c/page.tsx"` returns
      non-zero AND `test -f "apps/ayokoding-www/src/app/[locale]/(content)/browse/page.tsx"` returns 0
      (browse index relocated); `grep -F "/c/" apps/ayokoding-www/src/features/content/core/content-url.ts`
      prints nothing (uniform bare join); `content-namespace.ts`'s five rules are inverted (`/c/`-prefixed
      sources, bare destinations); the collision negative check from §3.0 still holds.
- [ ] [AI] **Loop-safety invariant (DD-48), falsifiable both ways** —
      `grep -rn '"/[a-z][a-z]/c/' apps/ayokoding-www/src/redirects/` is empty; reintroducing a forward
      rule in any module makes it non-empty.
- [ ] [AI] **DD-48 covers every namespaced section, not just `en/learn`** — `content-namespace.ts`'s
      inverted rule set still names all five: `en/learn`, `en/rants`, `id/belajar`, `id/celoteh`,
      `id/konten-video`; this is a **URL-layer** check, distinct from DD-45's content-structure deferral
      check below.
- [ ] [AI] No production navigation source file was edited **by the six-domain relocation itself**
      (DD-44, scoped to §3.2 — see
      [§3.2's scoped re-statement](#32--relocate-the-six-domains-pure-git-mv-dd-41)) — the staged-name
      check under `src/features/navigation`, `src/features/content`, and `src/app`, run at that
      sub-step, printed nothing; DD-48's own production-code edits (§3.0) are accounted for separately
      and are not a DD-44 violation.
- [ ] [AI] `npx nx run ayokoding-www:build` + `:typecheck` + `:lint` + `:test:unit` +
      `:validate-indexes` + `:specs:behavior:coverage` **and**
      `npx nx run ayokoding-www-fe-e2e:test:e2e` exit 0. (`ayokoding-www:test:e2e` and
      `:test:integration` are no-op echoes — omitted deliberately.)
- [ ] [AI] `md links validate` (excluding `plans/done` and `apps/ose-www/content`) and
      `md heading-hierarchy validate` are green over the relocated tree.
- [ ] [AI] All six Screen 4 renders exist in `assets/` and are embedded in `prd.md` with
      viewport-specific alt text; `find assets -name 'legacy-landing-option-*-*.png' | wc -l` returns
      **6** (this plan's DD-47 slice; the other 24 belong to
      `ayokoding-learning-path-03-navigation-ui`); the Q-D selection is recorded and no
      "Selection: PENDING" line remains.
- [ ] [AI] `id/belajar` still holds **53** `.md` with no bucket directory; the deferral note is written
      into this checklist (DD-45).
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: `/en/learn/` is at its final three-bucket shape, every relocated URL 308s to its
> new address in both inbound forms, `courses/` and `paths/` are provably unaffected, and no page body
> was edited. Production serves a coherent section. Safe to stop indefinitely. To resume:
> `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www-fe-e2e:test:e2e`.

---

## Phase 4: Section & App Verification

- [ ] [AI] Run the affected quality gates from the worktree:
      `npx nx affected -t typecheck lint test:quick test:unit test:e2e specs:behavior:coverage`
      — acceptance: exits 0. Fix ALL failures, including preexisting ones (Root Cause Orientation),
      committing preexisting fixes separately. (`ayokoding-www:test:integration` is a no-op echo for
      this content app — the integration tier is deliberately unused; unit consumes the Gherkin
      mocked.)
- [ ] [AI] Build the site: `npx nx run ayokoding-www:build` — acceptance: exits 0.
- [ ] [AI] Run link + heading-hierarchy + markdown validation:
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md links validate --exclude plans/done --exclude apps/ose-www/content` + `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md heading-hierarchy validate` + `npm run lint:md` (the actual mechanism — **not** `nx run` targets; both `md` subcommands also
      run automatically pre-commit via `lint-staged` for every staged `.md` file) — acceptance: all
      green.

  **Gherkin (binds) →** "The relocated tree builds and validates green"

  ```gherkin
  Scenario: The relocated tree builds and validates green
    Given the re-home, the six-domain relocation, and both redirect modules have landed
    When the ayokoding-www build, the unit and e2e tiers, and the link and heading validators run
    Then the build and every tier succeed
    And link, heading-hierarchy, and markdownlint validation report no errors
  ```

- [ ] [AI] **Three-bucket structural sweep (DD-40)** — `ls apps/ayokoding-www/content/en/learn` lists
      exactly `_index.md`, `courses`, `legacy`, `overview.md`, `paths` and nothing else, AND
      `find apps/ayokoding-www/content/en/learn/legacy -name '*.md' | wc -l` still returns **1148**,
      AND `find apps/ayokoding-www/content/id/belajar -name '*.md' | wc -l` still returns **53** with
      no bucket directory (`test -e apps/ayokoding-www/content/id/belajar/legacy` returns non-zero,
      DD-45) — acceptance: all four checks hold. Falsifiable both ways: before Phase 3 the `ls` lists
      seven domain directories and the `find` under `legacy/` fails outright.
- [ ] [AI] **Redirect-order regression check (DD-42/DD-43/DD-48)** —
      `apps/ayokoding-www/next.config.ts` still spreads the four rule sets in the order
      `contentNamespaceRedirects` → `learnReorgRedirects` → `courseRehomeRedirects` →
      `learnThreeBucketRedirects` (DD-48's re-derived order — `contentNamespace` **first**, not last),
      and `npx nx run ayokoding-www:test:unit` passes all modules' negative assertions (no blanket
      source; no `courses`/`paths`/`fundamentally-strong` source prefix in the bucket module; no rule
      anywhere has a `/c/`-containing destination; the rule sets' source prefixes are disjoint) —
      acceptance: all hold. Falsifiable both ways: swapping any adjacent pair in the spread makes the
      deep-path, historical-rename, or loop-safety e2e/unit assertion fail — in particular, moving
      `contentNamespaceRedirects` off the front reintroduces the coexistence hazard DD-48 forbids.
- [ ] [AI] **Re-home completeness re-check (DD-2)** —
      `ls apps/ayokoding-www/content/en/learn/courses | wc -l` returns **38** (37 course directories +
      `_index.md`), and every directory name appears in `REHOMED_COURSE_SLUGS` — acceptance: both hold.
      Falsifiable both ways: the directory did not exist before Phase 1 and held only `_index.md`
      (count 1) after it.

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes
> (Root Cause Orientation). Commit preexisting fixes separately with conventional-commit messages.

### Phase 4 Gate

> All checks below must pass before starting Phase 5.

- [ ] [AI] Affected `typecheck` / `lint` / `test:quick` / `test:unit` / `test:e2e` /
      `specs:behavior:coverage` exit 0.
- [ ] [AI] Build + link + heading + markdown validation green.
- [ ] [AI] Three-bucket structural sweep green (exactly three buckets + two hub files; 1148 legacy
      `.md`; `id/belajar` untouched at 53) and the four-way redirect ordering + both negative
      assertion sets still hold.
- [ ] [AI] `courses/` holds 37 course directories + `_index.md`, all named in `REHOMED_COURSE_SLUGS`.
- [ ] [AI] **UI Quality Gate (R9)** — run
      [`ui-quality-gate`](../../../repo-governance/workflows/ui/ui-quality-gate.md) (`swe-ui-checker`
      → `swe-ui-fixer`, `mode=strict`) over the component source DD-48 edits. This plan is **not**
      UI-gate-exempt: DD-48 modifies `breadcrumb.tsx`, `browse-index.tsx`, and three route
      `page.tsx` files, and `swe-ui-checker` audits `.tsx` source statically. — acceptance: the gate
      reports 0 CRITICAL and 0 HIGH findings outstanding. Falsifiable both ways: the gate is capable
      of reporting findings against these files (they exist and are `.tsx`), so a clean result is
      evidence rather than a vacuous pass. Note this gate audits **source**; it is not a live-site
      check and does not replace Phase 5's Playwright MCP verification or the Rule-15 retest.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the whole URL/IA layer passes every automated gate on a clean tree. Safe to stop.
> To resume: re-run the affected quality gates + build.

---

## Phase 5: Manual UI Verification + Rule-15 Three-Tester Retest

> The legacy landing and its per-page banner are a user-facing change, so a live-site retest is
> required before archival. **Locale scope**: this plan's content changes are `en`-only per DD-45 —
> see [brd.md §Business-Scope Non-Goals](./brd.md#business-scope-non-goals). Retest the `en` learn
> section only; do not fabricate an `id` walk-through for a locale this plan deliberately did not
> touch. The relocation mechanism itself is locale-neutral, so this scoping is a content-scope fact,
> not a code limitation.

- [ ] [AI] Confirm `en` is the affected locale — command:
      `test -d apps/ayokoding-www/content/en/learn/legacy && test ! -e apps/ayokoding-www/content/id/belajar/legacy`
      — acceptance: exits 0 (the `en` bucket exists, the `id` one deliberately does not).
- [ ] [AI] Start the dev server: `npx nx dev ayokoding-www` — acceptance: server up.
- [ ] [AI] **Three-bucket learn-section walk** — at 375 / 768 / 1280 px via Playwright MCP, open
      `/en/learn` (sidebar shows exactly `paths`, `courses`, `legacy`, in that weight order),
      `/en/learn/legacy` (landing renders with the Q-D-ruled notice), one relocated page per domain,
      and one deep relocated page; confirm the bare inbound form of a relocated URL lands in **one**
      hop and a stale `/c`-bookmark form of the same URL lands in **two** hops (DD-48's inversion adds
      one hop for the stale form, never a loop), and that a `courses/` URL and a `paths/` URL are
      **not** rewritten — acceptance: all correct; zero console errors; the legacy breadcrumb does not
      wrap to multiple lines at 375 px.
- [ ] [AI] **Re-home walk** — at the same three breakpoints, open an old
      `fundamentally-strong/software-engineer/<slug>` URL and confirm it lands on
      `/en/learn/courses/<id>`, that the same URL with a `?path=` query preserves that query through
      the redirect, and that the course page renders its `prerequisites` metadata — acceptance: all
      three behaviors correct at every breakpoint.
- [ ] [AI] **Old-way browse walk** — navigate from `/en/learn/legacy` and from the preserved
      `fundamentally-strong` section index to a re-homed course entirely by clicking, with no typed
      URL — acceptance: every hop resolves; no dead link; the destination is the canonical course body.
- [ ] [AI] Verify `html[lang]` is `en` on every page opened and `browser_console_messages` is clean —
      acceptance: correct lang attribute; zero console errors.
- [ ] [AI] Capture one screenshot per screen per breakpoint to
      `evidence/phase-5-<screen>-en-<breakpoint>px.png` — acceptance: the files exist in `evidence/`
      and each is referenced from this checklist by an `![alt](./evidence/…)` link.
- [ ] [AI] Run the three live-site testers (the `web-ux-test-fixing-planning` workflow:
      `web-exploratory-tester` + `web-usability-tester` + `web-design-tester`) against the running
      three-bucket learn section — `/en/learn`, the `/en/learn/legacy` landing, a relocated legacy
      page carrying the Q-D-ruled banner, and a re-homed course page reached through a legacy URL
      (`en` content) — acceptance: EWT/UWT/DWT findings + spec gaps recorded.
- [ ] [AI] Append each finding below as a new unchecked checkbox, source-attributed
      (`- [ ] EWT-NNN:` / `- [ ] UWT-NNN:` / `- [ ] DWT-NNN: <defect> — fix before archival`); append
      any SG-### / USS-### items to the relevant spec or content step in Phase 3.

### Rule-15 retest follow-ups

- [ ] [AI] _(populated during the retest — every EWT/UWT/DWT defect finding must be fixed/ticked before
      archival; deferral of a defect requires explicit user permission and only when genuinely
      impossible; SG-### / USS-### may be triaged or deferred with written rationale)_

### Phase 5 Gate

> All checks below must pass before starting Phase 6.

- [ ] [AI] The three-bucket walk, the re-home walk, and the old-way browse walk are all verified in
      `en` across 375 / 768 / 1280 px; screenshots committed under `evidence/`; console clean at every
      breakpoint.
- [ ] [AI] All rule-15 EWT/UWT/DWT defect findings are fixed (ticked), or explicitly permitted to
      defer by the user.
- [ ] [AI] Draft PR opened (retest evidence + any fixes); 3-cycle PR-Review complete; CI green; PR
      `[AI]`-merged; deployed.

> **Pause Safety**: the relocated section is verified live and defect-clean in `en` (this plan's only
> content locale; the relocation mechanism is locale-neutral). Safe to stop. To resume: re-run the
> three testers against the running app.

---

## Phase 6: Final `origin/main` Integration & CI Verification

- [ ] [AI] Confirm no plan PR is still open — every prior phase branch has been `[AI]`-merged to
      `main`: `gh pr list --search "ayokoding-learning-path-01-url-restructure" --state open` —
      acceptance: returns zero rows.
- [ ] [AI] Sync the worktree to latest `origin/main` and run the full affected suite:
      `npx nx affected -t typecheck lint test:quick test:unit test:e2e specs:behavior:coverage` +
      `npx nx run ayokoding-www:build` — acceptance: all exit 0 on the integrated `main`.
- [ ] [AI] Monitor the final `main` CI run — poll every ~2 min, one
      `gh run view --json status,conclusion` per wakeup; never `gh run watch` — acceptance: all GitHub
      Actions green; fix root causes and push follow-ups (own PR → review → `[AI]` merge) until green.
- [ ] [AI] Confirm `prod-ayokoding-www` serves the three-bucket learn section: spot-check one relocated
      URL per domain and one re-homed course URL against production; re-dispatch
      `apps-ayokoding-www-deployer` if any earlier deploy lagged — acceptance: every spot-checked old
      URL 308s to its new address in production.

### Phase 6 Gate

> All checks below must pass before starting Phase 7.

- [ ] [AI] Zero open plan PRs; every prior phase merged to `main`.
- [ ] [AI] Full affected suite + build green on integrated `main`; the final `main` CI run is green.
- [ ] [AI] `prod-ayokoding-www` serves the three-bucket section and every spot-checked redirect
      resolves in production.

> **Pause Safety**: the whole plan is integrated on `main`, green in CI, and live in production. Safe
> to stop. To resume: re-run the affected suite on `main` and check CI/prod status.

---

## Phase 7: Knowledge Capture

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)._

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only if a durable surface would
      catch this automatically next time; discard the rest with a one-line reason — acceptance: every
      entry has a route or a discard reason.
- [ ] [AI] Apply the **secret/sensitivity gate** to every surviving entry — sanitize any secret,
      credential, token, or private hostname to a `<placeholder>` token, or discard if unsanitizable —
      acceptance: `learnings.md` contains no raw secret.
- [ ] [AI] Apply the **repo-relevance gate** — infra-private content (Terraform, k3s, Proxmox, real
      hostnames/inventories) stays in `ose-infra` only and is never cross-routed here; public-governance
      content may propagate via the existing parity loop — acceptance: no infra-private content appears
      in this repo's routed output.
- [ ] [AI] Route each surviving learning to exactly one durable home per the open-ended routing matrix;
      **code-homed** learnings (any `apps/`- or `libs/`-homed learning, or tests) are ALWAYS filed as a
      separate `plans/backlog/<slug>/` plan and NEVER landed inline in this plan's commits/PR —
      acceptance: every entry records its terminal routing state.
- [ ] [AI] If no generalizable learning surfaced, record `No generalizable learnings — <reason>` in
      `learnings.md` — acceptance: `learnings.md` is never silently empty.

### Phase 7 Gate

> All checks below must pass before Plan Archival.

- [ ] [AI] Every `learnings.md` entry is terminal (routed inline / filed as backlog / discarded with
      reason), or the explicit "none" escape is present.
- [ ] [AI] No code-homed learning landed inline in this plan's own commits/PR.
- [ ] [AI] Draft PR opened (`learnings.md` triage); 3-cycle PR-Review complete; CI green; PR
      `[AI]`-merged; deployed (no-op).

> **Pause Safety**: `learnings.md` is fully triaged; nothing depends on querying it later. Safe to
> stop. To resume: re-read `learnings.md` and confirm every entry is terminal.

---

## Phase 8: Plan Archival

- [ ] [AI] Verify ALL delivery checklist items are ticked.
- [ ] [AI] Verify the Knowledge Capture phase is complete (every entry terminal or the explicit "none"
      escape; both safety gates applied).
- [ ] [AI] Verify ALL quality gates pass (local + CI) and the build is green.
- [ ] [AI] Verify ALL manual assertions pass (Playwright MCP) with committed evidence in `evidence/`;
      the `en` locale exercised (per brd.md's recorded `id` deferral, DD-45).
- [ ] [AI] Verify every rule-15 EWT/UWT/DWT defect finding is fixed (ticked) — deferral requires
      explicit user permission (only when genuinely impossible); SG-### / USS-### may be triaged or
      deferred with rationale.
- [ ] [AI] **Verify the three-bucket learn section is final and `id` is untouched** —
      `ls apps/ayokoding-www/content/en/learn` lists exactly `_index.md`, `courses`, `legacy`,
      `overview.md`, `paths`; `find apps/ayokoding-www/content/en/learn/legacy -name '*.md' | wc -l`
      returns **1148**; `ls apps/ayokoding-www/content/en/learn/courses | wc -l` returns **38**;
      `find apps/ayokoding-www/content/id/belajar -name '*.md' | wc -l` returns **53** and
      `test -e apps/ayokoding-www/content/id/belajar/legacy` returns non-zero (DD-45's deferral held);
      and all six Q-A…Q-F rulings are recorded in `tech-docs.md` rather than left "Recommendation".
- [ ] [AI] **Verify this plan's design-funnel slice is complete (DD-47)** —
      `find assets -name 'legacy-landing-option-*-*.png' | wc -l` returns **6** (2 options × 3
      viewports for Screen 4); every one is embedded in `prd.md` with viewport-specific alt text; the
      Q-D selection is recorded and `grep -F "Selection: PENDING" prd.md` prints nothing. **The other
      24 renders of DD-47's 30-render matrix belong to
      `ayokoding-learning-path-03-navigation-ui`** — 6 here is the complete slice, not an
      under-delivery.
- [ ] [AI] **Cross-plan link gate (BF-8)** — confirm no reference in this plan folder points at a
      stale `syllabus/` location:

  ```bash
  cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md links validate \
    --exclude plans/done \
    --exclude apps/ayokoding-www/content \
    --exclude apps/ose-www/content 2>&1 | grep -F "ayokoding-learning-path-01-url-restructure"
  ```

  — acceptance: the `grep` finds **no** matching line (exit 1). Falsifiable the other way too:
  introduce one bad `./syllabus/` link in this folder and the same command prints that file and
  exits 0.

- [ ] [AI] **Repo-wide link gate (BF-8, pre-push hook's own form)** — run:

  ```bash
  cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md links validate \
    --exclude plans/done --exclude apps/ayokoding-www/content --exclude apps/ose-www/content
  ```

  — acceptance: prints `All links valid! No broken links found.` The bare repo-wide form is
  **unsatisfiable** (the repo carries 93 pre-existing broken links, all under `plans/done/`,
  unrelated to this work), so this exclusion form — which is exactly what the pre-push hook runs
  — is the binding check. Both this and the previous gate are required; neither alone suffices.

- [ ] [AI] Move: `git mv plans/in-progress/ayokoding-learning-path-01-url-restructure/ plans/done/YYYY-MM-DD__ayokoding-learning-path-01-url-restructure/`
      using today's completion date (the `assets/` and `evidence/` subfolders move with it) —
      acceptance: the folder resolves under `plans/done/` and no longer under `plans/in-progress/`.
- [ ] [AI] Update `plans/in-progress/README.md` — remove the plan entry.
- [ ] [AI] Update `plans/done/README.md` — add the plan entry with its completion date.
- [ ] [AI] Update any other READMEs that reference this plan (e.g. `plans/README.md`,
      `plans/backlog/README.md`) — acceptance:
      `grep -rF "ayokoding-learning-path-01-url-restructure" plans --include=README.md` shows every
      hit pointing at the new `plans/done/YYYY-MM-DD__…` path.
- [ ] [AI] Repoint the four sibling plans' references to this plan's new archived path — acceptance:
      `grep -rF "plans/in-progress/ayokoding-learning-path-01-url-restructure" plans` prints nothing.
- [ ] [AI] Commit the archival:
      `chore(plans): move ayokoding-learning-path-01-url-restructure to done`.
- [ ] [AI] Remove the worktree once the archival PR is merged:
      `git worktree remove worktrees/ayokoding-learning-path-01-url-restructure` — acceptance:
      `git worktree list` no longer names it.

### Phase 8 Gate

- [ ] [AI] Three-bucket learn section final (exactly three buckets + two hub files, 1148 legacy `.md`,
      37 courses + `_index.md`, `id/belajar` untouched at 53); all six Screen 4 renders present and
      embedded; the Q-D selection recorded.
- [ ] [AI] Both BF-8 link gates pass (the per-plan `grep` finds nothing; the hook-form repo-wide run
      prints `All links valid! No broken links found.`).
- [ ] [AI] Plan folder is under `plans/done/YYYY-MM-DD__…`; all READMEs updated; sibling references
      repointed; archival committed.
- [ ] [AI] Draft PR opened (archival move); 3-cycle PR-Review complete; CI green; PR `[AI]`-merged;
      deployed (no-op). Worktree removed.

> **Pause Safety**: the plan is archived and its final PR `[AI]`-merged to `main`. Terminal state. To
> resume: nothing — the plan is complete.

---

### Commit Guidelines (all phases)

- [ ] [AI] Commit changes thematically — group related changes into logically cohesive commits.
- [ ] [AI] Follow Conventional Commits: `<type>(<scope>): <description>` (imperative, no period).
- [ ] [AI] Split domains/concerns into separate commits; preexisting fixes get their own commits.
- [ ] [AI] Keep each `git mv` batch in its **own** commit, separate from any frontmatter or prose edit,
      so the pure-rename proof (`git diff --summary -M`) stays readable.
- [ ] [AI] Do NOT bundle unrelated changes into a single commit.

### Local Quality Gates (Before Every Push)

- [ ] [AI] `npx nx affected -t typecheck` exits 0.
- [ ] [AI] `npx nx affected -t lint` exits 0.
- [ ] [AI] `npx nx affected -t test:quick test:unit` exits 0 (add `test:e2e` for the phases that touch
      routing or content trees — Phases 2, 3, 4, 5).
- [ ] [AI] `npx nx affected -t specs:behavior:coverage` exits 0.
- [ ] [AI] Fix ALL failures — including preexisting issues not caused by your changes (Root Cause
      Orientation).

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes.
> Commit preexisting fixes separately with appropriate conventional-commit messages.
