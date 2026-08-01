# Delivery Checklist — Course Authoring: Platform & Concurrency Languages

This checklist authors **14 course bodies** into
`apps/ayokoding-www/content/en/learn/courses/<course-id>/`: plan04's **Band 3 — Mobile & desktop
platforms** (10 bodies) and **Band 4 — Concurrency languages** (4 bodies), merged into one plan.

> **This plan never edits a manifest file.** Every file under `<MANIFESTS>` belongs to the
> manifest-growth plan (`ayokoding-learning-path-12-careers-se-manifests` — the successor to
> plan04's original, since-renamed/split `ayokoding-learning-path-05-manifests` name). This plan's
> only outbound artefact is the **band-completion signal** recorded at the end of each band phase. See
> [README §The manifest ownership invariant](./README.md#the-manifest-ownership-invariant-binding--read-before-anything-else) and
> [tech-docs §The manifest ownership invariant](./tech-docs.md#the-manifest-ownership-invariant-binding).
>
> **Cross-plan source of truth** — the `syllabus/` detail layer lives in
> [`../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/README.md).
> Every course body is authored **from** its `syllabus/courses/<course-id>.md` spec. **Never copy
> those files into this plan** — a copy forks the source of truth for 122 course specs.
>
> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
> Git-mechanical steps (worktree create/remove, branch, push, merge) are `[AI]`. **This plan contains
> no `[HUMAN]` step.**
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (safe-to-stop state + resume command). A gate in a phase named as a
> delivery boundary in the [`### Delivery Boundaries`](#delivery-boundaries) table additionally covers
> **integration** (draft PR opened, 3-cycle PR-Review, CI green, `[AI]` merge, `ayokoding-www`
> deployed); a gate in an **intermediate** phase instead confirms the work is committed to its
> delivery unit's branch with nothing pushed for review yet.
>
> **Executor environment note — RTK-wrapped commands emit an empty-output marker, not true
> emptiness** (inherited verbatim from plan04's own note; see `CLAUDE.md` §RTK): `git diff` appends a
> three-line trailer whenever the result is non-empty, so `| wc -l` prints `N + 3` and `| grep -c .`
> prints `N + 1` for `N` changed paths, and in the clean state the two forms **diverge** (`grep -c .`
> reads `0`; `wc -l` reads `1`). **Every `git diff --name-only …` clause in this plan asserts `0`**,
> and for that assertion the sanctioned form is **`| grep -c .`**. Never use an `ls`-based emptiness
> assertion.

## Worktree

Worktree path: `worktrees/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/`

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree ayokoding-learning-path-05-course-authoring-platform-and-concurrency
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the latest
`origin/main` when missing, syncs with `origin/main` before implementing, and prompts before deleting
the worktree after the plan is archived and pushed.

Every phase branches from the **latest `origin/main`** inside this one shared worktree
(`git fetch origin && git checkout main && git pull && git checkout -b ayokoding-learning-path-05-course-authoring-platform-and-concurrency/<phase-slug>`)
and authors its work there, committing as it goes. Only the phase(s) named as a **delivery boundary**
in the [`### Delivery Boundaries`](#delivery-boundaries) table push that branch and open **their own
draft PR**; an **intermediate** phase commits (and may push the branch for durability) without opening
one. **Phase 0 is excluded from opening a PR under any circumstance.**

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans.md#worktree-specification).

## Delivery Mode: worktree-to-pr

Each **delivery boundary** named in the [`### Delivery Boundaries`](#delivery-boundaries) table works
in the shared worktree on its **own branch**, opens a **draft PR** against `main`, runs the
**PR-Review Maker→Fixer Cycle** (fan-out → `pr-review-synthesis-maker` → `pr-review-fixer`, 3
sequential CI-gated cycles), flips the PR to ready, and `[AI]` **merges it automatically once all
quality gates are green** — then `[AI]` **deploys `ayokoding-www` to `prod-ayokoding-www` after every
merge**. An **intermediate** phase inside a delivery unit instead commits (and may push for
durability) to that unit's branch without opening a PR of its own.

> **Inherited execution policy — grouped-cohort cadence (per plan04's 2026-07-31 amendment,
> re-grouped by band).** Plan04 established sequential five-course PR cohorts for its own remaining
> course bodies; this plan inherits that cadence as its execution policy but groups by the two
> original bands (10 + 4) rather than a mechanical 5-course slice, because a mechanical slice would
> split the `just-enough-dart` / `hybrid-app-development` pair across two PRs. See
> [README §Delivery Mode](./README.md#delivery-mode-worktree-to-pr) for the full reasoning — this is a
> stated **[Judgment call]**, not a re-derivation of plan04's own decision.
>
> **DN-11 — `[AI]` auto-merge (repo default), cited unchanged.** The repo's
> [PR Merge Protocol](../../../repo-governance/development/workflow/pr-merge-protocol.md) has `[AI]`
> merge each PR once its five hardened preconditions hold; this plan does not opt into a `[HUMAN]`
> merge gate.

**Delivery-Boundary Integration Protocol** (fires once per **delivery boundary**, not once per phase):

1. [AI] Sync the worktree to latest `origin/main` and branch:
   `git fetch origin && git checkout main && git pull && git checkout -b ayokoding-learning-path-05-course-authoring-platform-and-concurrency/<phase-slug>`.
2. [AI] Stage only this phase's paths (`git add <explicit paths>` — never `git add -A`), commit
   thematically (Conventional Commits, imperative, no period), push the branch, open a **draft PR**
   against `main` (`gh pr create --draft --base main ...`) — CI runs on the PR.
3. [AI] Run the **PR-Review Maker→Fixer Cycle** (3 sequential CI-gated cycles), resolve every finding,
   then `gh pr ready`.
4. [AI] **Merge** once all quality gates are green (typecheck, lint, `test:quick`, `test:unit`,
   `specs:behavior:coverage`, CI, the 3-cycle review) — `[AI]` auto-merge per DN-11.
5. [AI] Dispatch `apps-ayokoding-www-deployer` to deploy `ayokoding-www` to `prod-ayokoding-www`.

## Depends-on

| Relation        | Plan (full folder name)                                                                                           | Nature                                                                                                                                                                                        |
| --------------- | ----------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **blockedBy**   | `ayokoding-learning-path-01-url-restructure`                                                                      | Hard, transitive via 04. Populated flat `<COURSES>` bucket + `<COURSES>_index.md`.                                                                                                            |
| **blockedBy**   | `ayokoding-learning-path-02-schema-and-prerequisite-dag`                                                          | Hard, transitive via 04. `syllabus/` specs + the `prerequisites` frontmatter contract.                                                                                                        |
| **blockedBy**   | `ayokoding-learning-path-04-course-authoring`                                                                     | Hard. Its Phase 0 baseline + populated `<COURSES>` namespace — not Band 2 specifically.                                                                                                       |
| **blockedBy**   | `vercel-function-cost-reduction`                                                                                  | Hard, new. Root layout + middleware fix landed against the same `apps/ayokoding-www` app/route tree.                                                                                          |
| **blocks**      | [`ayokoding-learning-path-12-careers-se-manifests`](../ayokoding-learning-path-12-careers-se-manifests/README.md) | Needs this plan's band-completion signals to grow the three `software-engineer`-role manifests.                                                                                               |
| **blocks**      | `ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own`                                              | Needs `just-enough-go` (Band 4) as `build-your-own-raft`'s declared prerequisite (verified against plan04's own catalog row and independently confirmed by that plan's own dependency table). |
| **independent** | Every other new sibling splitting plan04's remaining scope                                                        | No shared file, no shared prerequisite edge. Bands are mutually content-independent per plan04's own finding.                                                                                 |

**Start precondition (hard gate, checked in Phase 0)**: `ayokoding-learning-path-01-url-restructure`,
`ayokoding-learning-path-02-schema-and-prerequisite-dag`, and `vercel-function-cost-reduction` are all
merged to `origin/main`; `ayokoding-learning-path-04-course-authoring`'s Phase 0 baseline has been
established (toolchain converged, both its own blocking plans verified merged, its `<COURSES>`
namespace populated). This plan does not start on a promise.

## Parallelization Model

**Cap**: honor the in-force subagent/PR-review concurrency cap.

- **Phase 0** is a single serial baseline.
- **Phase 1 (Band 3, 10 bodies)** — content-independent bodies (each writes only its own
  `<COURSES><id>/` subtree) that **pipeline concurrently** through review, bounded by the cap. One
  intra-band ordering note: each `just-enough-<language>` primer is authored before or alongside its
  paired platform course, since the platform course's `_index.md` declares the primer as a
  prerequisite.
- **Phase 2 (Band 4, 4 bodies)** — same content-independence and concurrency-bounded pipelining as
  Phase 1; `just-enough-go` before or alongside `csp-style-concurrency`, `just-enough-elixir` before
  or alongside `actor-model-concurrency`.
- **Phases 3–7 (finalization)** are serial.
- **Cleanup is the terminal node** (Phase 7's archival), depending on every delivery node above so it
  can never remove the worktree or branch while an earlier node's work is still in flight.

Phase 1 and Phase 2 are mutually content-independent (per plan04's own finding for Bands 3 and 4) and
could in principle run concurrently; they are sequenced here — Phase 1 then Phase 2 — purely to keep
each phase's review scope to one coherent PR, per the grouped-cohort delivery-mode decision above.

**Path constants** (referenced throughout):

- `<COURSES>` = `apps/ayokoding-www/content/en/learn/courses/` (course bundles; served at `/en/learn/courses/<course-id>`)
- `<PATHS>` = `apps/ayokoding-www/content/en/learn/paths/` (path-landing anchors — **read-only here**)
- `<FEAT>` = `apps/ayokoding-www/src/features/course-paths/` (**never written here**)
- `<MANIFESTS>` = `<FEAT>manifests/` (**never written here** — manifest-growth-plan property; read-only reference only)
- `<SYLLABUS>` = `../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/` (cross-plan authoring source of truth — **never copied**)

### Delivery Boundaries

| Phase(s) | Delivery unit                                                                                                | Worktree / branch                                                                                                    | PR opens         |
| -------- | ------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------- | ---------------- |
| 0        | — (setup and baseline)                                                                                       | —                                                                                                                    | no               |
| 1        | Band 3 — Mobile & desktop platforms (10 bodies)                                                              | shared worktree; `ayokoding-learning-path-05-course-authoring-platform-and-concurrency/band-3-mobile-desktop`        | yes — at Phase 1 |
| 2        | Band 4 — Concurrency languages (4 bodies)                                                                    | shared worktree; `ayokoding-learning-path-05-course-authoring-platform-and-concurrency/band-4-concurrency-languages` | yes — at Phase 2 |
| 3        | Final content-correctness sweep (structural verification + build-green)                                      | shared worktree; `ayokoding-learning-path-05-course-authoring-platform-and-concurrency/phase-3-verification`         | yes — at Phase 3 |
| 4-7      | Plan closeout (manual verification evidence, final `main`/CI integration check, Knowledge Capture, archival) | shared worktree; `ayokoding-learning-path-05-course-authoring-platform-and-concurrency/phase-7-closeout`             | yes — at Phase 7 |

Each course inside Phase 1 and Phase 2 is a content-independent DAG leaf that could, per the general
sanctioned pattern, take its own PR; this plan instead follows the grouped-cohort cadence (one PR per
band) inherited from plan04's own 2026-07-31 amendment, re-grouped as stated above. **Phase 3 stays
its own boundary**: it lands the plan-wide structural/build/link verification sweep over all 14
bodies and already passes all four boundary-test criteria standalone. **Phases 4, 5, and 6 are
intermediate**: Phase 4's screenshots and Phase 6's `learnings.md` triage are evidence the Phase 7
archival gate itself reads and verifies as a precondition, and Phase 5 makes no routine change at all
(verification/CI-monitoring only) — all three fold into the Phase 7 closeout PR, which is the plan's
last change-producing phase and therefore always a boundary.

---

## Phase 0: Environment Setup & Baseline

> _Executor: repo-setup-manager_

- [ ] [AI] Enter/provision the worktree and install dependencies: `npm install`
      — acceptance: exits 0, `node_modules/` synchronized.
- [ ] [AI] Converge the toolchain: `npm run doctor -- --fix`
      — acceptance: exits 0 with no unresolved drift.
- [ ] [AI] **Verify `ayokoding-learning-path-01-url-restructure` merged** — command (single line):
      `test -d apps/ayokoding-www/content/en/learn/courses && test -f apps/ayokoding-www/content/en/learn/courses/_index.md`
      — acceptance: both exit 0.
- [ ] [AI] **Verify `ayokoding-learning-path-02-schema-and-prerequisite-dag` merged** — command:
      `test -d plans/done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/courses`
      — acceptance: exits 0.
- [ ] [AI] **Verify `ayokoding-learning-path-04-course-authoring`'s Phase 0 baseline is established** —
      command: `test -f plans/in-progress/ayokoding-learning-path-04-course-authoring/evidence/phase-0-snapshot.txt`
      — acceptance: exits 0. This confirms plan04's own toolchain-convergence and upstream-verification
      baseline exists; this plan does not need Band 2 or any other band of plan04 to have landed —
      only its Phase 0 baseline and its populated `<COURSES>` namespace (already checked above).
- [ ] [AI] **Verify `vercel-function-cost-reduction`'s checkable precondition holds** — command
      (single line):
      `test ! -f apps/ayokoding-www/src/app/layout.tsx && test ! -f apps/ayokoding-www/src/middleware.ts`
      — acceptance: both `test` conditions pass (both files absent — `app/layout.tsx` deleted with its
      contents merged into `app/[locale]/layout.tsx`; `src/middleware.ts` deleted). Falsifiable both
      ways: [Repo-grounded] as of this plan's authoring date, `apps/ayokoding-www/src/middleware.ts`
      **still exists**, so this exact command fails today; once
      `vercel-function-cost-reduction` lands, both files are gone and the command passes. Do not
      proceed past this check if it fails — this plan does not start on a promise.
- [ ] [AI] Establish content baselines: `npx nx run ayokoding-www:build` and
      `npx nx run ayokoding-www:test:unit`
      — acceptance: both exit 0; record pass state in `evidence/phase-0-snapshot.txt`.
- [ ] [AI] **Confirm all fourteen course slugs are absent (no collision)** under `<COURSES>`:

  ```bash
  for s in just-enough-kotlin android-app-development just-enough-swift ios-app-development \
    just-enough-dart hybrid-app-development just-enough-csharp windows-app-development \
    linux-app-development building-production-cli-tools just-enough-go csp-style-concurrency \
    just-enough-elixir actor-model-concurrency; do
    test -e "apps/ayokoding-www/content/en/learn/courses/$s" && echo "EXISTS $s"
  done
  ```

  — acceptance: **zero** output lines. Falsifiable both ways:
  `mkdir -p apps/ayokoding-www/content/en/learn/courses/just-enough-kotlin` makes the loop print
  `EXISTS just-enough-kotlin`.

- [ ] [AI] **Create the authored-body slug register** — write the 14 slugs this plan authors, one per
      line, to `evidence/authored-body-slugs.txt`:

  ```bash
  cat > evidence/authored-body-slugs.txt <<'EOF'
  just-enough-kotlin
  android-app-development
  just-enough-swift
  ios-app-development
  just-enough-dart
  hybrid-app-development
  just-enough-csharp
  windows-app-development
  linux-app-development
  building-production-cli-tools
  just-enough-go
  csp-style-concurrency
  just-enough-elixir
  actor-model-concurrency
  EOF
  ```

  — acceptance: `wc -l < evidence/authored-body-slugs.txt` returns **14**, and
  `sort evidence/authored-body-slugs.txt | uniq -d | wc -l` returns **0**.

- [ ] [AI] **Record the authored-body baseline** —
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done < evidence/authored-body-slugs.txt | wc -l`
      — acceptance: returns **14** today (none authored yet); record in `evidence/phase-0-snapshot.txt`.
      The same command must return **0** at archival (Phase 7).
- [ ] [AI] Confirm `learnings.md` exists in the plan folder with its H1 — command:
      `test -f learnings.md && head -1 learnings.md` — acceptance: file present and the first line is
      `# Learnings: ayokoding-learning-path-05-course-authoring-platform-and-concurrency`.
- [ ] [AI] **Cross-plan link gate** — confirm every `../ayokoding-learning-path-*` reference in this
      plan's own files resolves:

  ```bash
  cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate \
    --quiet \
    --exclude plans/done \
    --exclude apps/ayokoding-www/content \
    --exclude apps/ose-www/content 2>&1 | grep -F "ayokoding-learning-path-05-course-authoring-platform-and-concurrency"
  ```

  — acceptance: the `grep` finds **no** matching line (exits 1).

- [ ] [AI] **Confirm no manifest file changed in this phase** —
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [ ] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift.
- [ ] [AI] All four upstream plans verified: URL-restructure merged (populated `<COURSES>`), schema
      plan merged (`syllabus/courses/` present), plan04's Phase 0 baseline present, and the
      `vercel-function-cost-reduction` checkable precondition (both files absent) holds.
- [ ] [AI] `ayokoding-www:build` + `test:unit` baselines recorded green.
- [ ] [AI] All 14 slugs confirmed absent (zero `EXISTS` lines).
- [ ] [AI] `evidence/authored-body-slugs.txt` holds 14 unique slugs; the ABSENT-count baseline of 14
      is recorded in `evidence/phase-0-snapshot.txt`.
- [ ] [AI] Cross-plan link gate green.
- [ ] [AI] Zero manifest files touched.
- [ ] [AI] **No PR was opened for this phase and nothing was pushed** —
      `git ls-remote --heads origin "$(git branch --show-current)" | grep -c .` returns **0**, and
      `gh pr list --head "$(git branch --show-current)" --json number --jq 'length'` returns **0**.

> **Pause Safety**: only the toolchain, the four upstream preconditions, and the slug register were
> established — no course body exists yet, nothing is pushed, and no PR exists. Safe to stop
> indefinitely. To resume: re-run the four blocking-plan verification commands and the baseline build.

---

## Phase 1: Band 3 — Mobile & desktop platforms (10 bodies)

> Each course is authored as a full page-bundle into `<COURSES><course-id>/`. These ten bodies are
> content-independent (each writes only its own subtree) and **pipeline concurrently** through review
> (bounded by the cap). Per-course concept/example/prerequisite/capstone detail is **settled** in the
> cross-plan
> [`syllabus/courses/`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/courses/README.md).
> **Author each course body from its `<SYLLABUS>courses/<id>.md` spec, not from a fresh judgment call.**

### Course authoring convention (applies to every step in Phases 1 and 2)

1. [AI] **V (accuracy pre-verify)** — spot-check version-pinned / market facts via `web-researcher` —
   acceptance: no version-pinned claim written `[Unverified]`.
2. [AI] **Skeleton** — create `<COURSES><course-id>/` (`_index.md` with `prerequisites: [...]` +
   `overview.md` + `learning/_index.md` + `drilling/_index.md`); the `course-id` slug and the
   prerequisite chain are **settled** — use the exact values declared in
   `<SYLLABUS>courses/<course-id>.md` — acceptance: `test -d "<COURSES><course-id>"`,
   `test -d "<COURSES><course-id>/learning"`, and `test -d "<COURSES><course-id>/drilling"` all exit
   0, and `grep -F -q 'prerequisites:' "<COURSES><course-id>/_index.md"` exits 0.
3. [AI] **Author learning track** — `overview.md` (purpose + `## Prerequisites` naming only earlier
   library courses + register per `prd.md`), concept coverage, example/scenario pages + colocated
   `code/` where code-bearing, and `learning/capstone/` — acceptance: the course's own `overview.md`
   states its scope boundary against any sibling course it could be confused with.
4. [AI] **Author drilling track** — `drilling/overview.md` in the fixed five-section order —
   acceptance: all five sections present.
5. [AI] **Run content checkers** — the matching primer or by-example checker,
   `apps-ayokoding-www-facts-checker`, and `apps-ayokoding-www-link-checker` (plus
   `apps-ayokoding-www-general-checker` on `drilling/overview.md`) — acceptance: findings recorded.
6. [AI] **Apply content fixers** — resolve every CRITICAL/HIGH/MEDIUM finding via the matching fixer —
   acceptance: every finding addressed.
7. [AI] **Re-verify** — re-run checkers + `npx nx run ayokoding-www:build` + `npm run lint:md` —
   acceptance: zero CRITICAL/HIGH/MEDIUM remain; build + lint exit 0.
8. [AI] **Confirm no manifest file changed in this course's own diff** —
   `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
   — acceptance: returns **0** on this course's own branch before it merges.
9. [AI] **Licensing self-check (programme `A8`)** — grep this course's own worked-example code for the
   CC-BY-SA Stack Overflow hazard:
   `grep -rn 'stackoverflow\.com\|reddit\.com' "<COURSES><course-id>/learning/code/" 2>/dev/null | grep -c .`
   — acceptance: prints `0` (read the printed output; do not chain with `&&`).

Each course below is its own sub-step inside this phase's single delivery unit (Band 3 lands as one
PR at the end of Phase 1, per the grouped-cohort delivery mode above), applying the convention:

- [ ] [AI] `just-enough-kotlin` (Primer · Kotlin, `<SYLLABUS>courses/just-enough-kotlin.md`) — Kotlin
      syntax, null-safety, coroutines — all 9 convention steps complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_

  **Gherkin (underpins) →** "Each just-enough primer correctly unlocks its paired platform course"

  ```gherkin
  Scenario: Each just-enough primer correctly unlocks its paired platform course
    Given a just-enough-<language> primer and its paired platform course are both authored
    When a reader completes the primer and starts the platform course
    Then the platform course's own _index.md declares the primer's exact course-id as a prerequisite
    And the platform course does not re-teach the language syntax its paired primer already covers
  ```

- [ ] [AI] `android-app-development` (By Example · Kotlin, `<SYLLABUS>courses/android-app-development.md`)
      — native Android with the SDK — all 9 convention steps complete; checkers clean; additionally:
      `grep -F -q 'just-enough-kotlin' "<COURSES>android-app-development/_index.md"` exits 0 (the
      paired-primer prerequisite is declared).
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `just-enough-swift` (Primer · Swift, `<SYLLABUS>courses/just-enough-swift.md`) — Swift syntax,
      optionals — all 9 convention steps complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_
- [ ] [AI] `ios-app-development` (By Example · Swift, `<SYLLABUS>courses/ios-app-development.md`) — native
      iOS with the SDK — all 9 convention steps complete; checkers clean; additionally:
      `grep -F -q 'just-enough-swift' "<COURSES>ios-app-development/_index.md"` exits 0.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `just-enough-dart` (Primer · Dart, `<SYLLABUS>courses/just-enough-dart.md`) — Dart syntax,
      async, Flutter idioms — all 9 convention steps complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_
- [ ] [AI] `hybrid-app-development` (By Example · Dart, `<SYLLABUS>courses/hybrid-app-development.md`) —
      cross-platform from one Dart codebase — all 9 convention steps complete; checkers clean;
      additionally: `grep -F -q 'just-enough-dart' "<COURSES>hybrid-app-development/_index.md"` exits 0.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `just-enough-csharp` (Primer · C#, `<SYLLABUS>courses/just-enough-csharp.md`) — C# syntax,
      LINQ, async, .NET — all 9 convention steps complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_
- [ ] [AI] `windows-app-development` (By Example · C#, `<SYLLABUS>courses/windows-app-development.md`) —
      native Windows desktop — all 9 convention steps complete; checkers clean; additionally:
      `grep -F -q 'just-enough-csharp' "<COURSES>windows-app-development/_index.md"` exits 0.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `linux-app-development` (By Example · Python, `<SYLLABUS>courses/linux-app-development.md`) —
      native Linux desktop, packaging — all 9 convention steps complete; checkers clean; additionally:
      `grep -F -q 'just-enough-python' "<COURSES>linux-app-development/_index.md"` exits 0 (builds on
      the existing library primer without re-teaching it).
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

  **Gherkin (binds) →** "linux-app-development builds on the existing Python primer without re-teaching it"

  ```gherkin
  Scenario: linux-app-development builds on the existing Python primer without re-teaching it
    Given linux-app-development is authored
    When a reader who already completed just-enough-python starts it
    Then it declares just-enough-python as its prerequisite
    And it teaches native Linux desktop development and packaging without repeating Python syntax
  ```

- [ ] [AI] `building-production-cli-tools` (By Example · Go + Rust,
      `<SYLLABUS>courses/building-production-cli-tools.md`) — distributable CLI tools — all 9 convention
      steps complete; checkers clean; additionally both prerequisites are declared:
      `grep -F -q 'just-enough-go' "<COURSES>building-production-cli-tools/_index.md"` exits 0 **and**
      `grep -F -q 'just-enough-rust' "<COURSES>building-production-cli-tools/_index.md"` exits 0.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

  **Gherkin (binds) →** "building-production-cli-tools builds on both Go and Rust primers"

  ```gherkin
  Scenario: building-production-cli-tools builds on both Go and Rust primers
    Given building-production-cli-tools is authored
    When a reader inspects its prerequisites and its worked examples
    Then it declares both just-enough-go and just-enough-rust as prerequisites
    And its worked examples cover distributable CLI packaging concerns neither primer alone teaches
  ```

**Per-band closing steps** (applied once, in this phase's own gate):

- [ ] [AI] Add each landed course's row to
      [tech-docs §Course Library Catalog](./tech-docs.md#course-library-catalog) (already present at
      authoring time; confirm no drift against the settled spec) and its ID to `<COURSES>_index.md`.
- [ ] [AI] Record the band-completion signal in this file with all five fields — `GROW_MANIFESTS` is
      the three software-engineer-role manifests:

  ```text
  BAND: Band 3 — Mobile & desktop platforms
  PLAN: ayokoding-learning-path-05-course-authoring-platform-and-concurrency
  LANDED_COURSE_IDS:
  just-enough-kotlin
  android-app-development
  just-enough-swift
  ios-app-development
  just-enough-dart
  hybrid-app-development
  just-enough-csharp
  windows-app-development
  linux-app-development
  building-production-cli-tools
  GROW_MANIFESTS:
  apps/ayokoding-www/src/features/course-paths/manifests/careers/interview-ready/software-engineer.yaml
  apps/ayokoding-www/src/features/course-paths/manifests/careers/immediately-effective/software-engineer.yaml
  apps/ayokoding-www/src/features/course-paths/manifests/careers/fundamentally-strong/software-engineer.yaml
  MERGED_COMMIT: <fill in with this phase's PR merge commit SHA at execution time>
  ```

- [ ] [AI] Confirm zero manifest files were touched:
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      returns **0**.

### Phase 1 Gate

- [ ] [AI] All 10 Band-3 bodies exist:
      `for s in just-enough-kotlin android-app-development just-enough-swift ios-app-development just-enough-dart hybrid-app-development just-enough-csharp windows-app-development linux-app-development building-production-cli-tools; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done | wc -l`
      returns **0** (returns 10 before this phase).
- [ ] [AI] Every primer passed `apps-ayokoding-www-primer-checker`; every By-Example body passed
      `apps-ayokoding-www-by-example-checker`; facts + link checkers clean.
- [ ] [AI] Every primer/platform pair's prerequisite grep passes (6 pairing checks: kotlin→android,
      swift→ios, dart→hybrid, csharp→windows, plus linux-app-development→just-enough-python and
      building-production-cli-tools→{just-enough-go, just-enough-rust}).
- [ ] [AI] `npx nx run ayokoding-www:build` + `npm run lint:md` exit 0.
- [ ] [AI] Catalog rows added; band signal recorded with all five fields; zero manifest files touched.
- [ ] [AI] Draft PR opened at Phase 1 (this unit's own boundary); 3-cycle PR-Review complete; CI
      green; PR `[AI]`-merged; deployed. Record the merge commit SHA into the `MERGED_COMMIT` field
      of this phase's band-completion signal above.

> **Pause Safety**: all four primer/platform pairs plus the two standalone platform courses are live;
> every pairing's prerequisite resolves. Safe to stop. To resume: re-run the section build.

---

## Phase 2: Band 4 — Concurrency languages (4 bodies)

> These four bodies are content-independent and **pipeline concurrently** through review, bounded by
> the cap. Applies the same **Course authoring convention** defined in Phase 1.

- [ ] [AI] `just-enough-go` (Primer · Go, `<SYLLABUS>courses/just-enough-go.md`) — Go syntax, goroutines
      — all 9 convention steps complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_
- [ ] [AI] `csp-style-concurrency` (By Example · Go, `<SYLLABUS>courses/csp-style-concurrency.md`) —
      channels, CSP concurrency — all 9 convention steps complete; checkers clean; additionally both
      prerequisites are declared: `grep -F -q 'just-enough-go' "<COURSES>csp-style-concurrency/_index.md"`
      exits 0 **and**
      `grep -F -q 'concurrency-and-parallelism' "<COURSES>csp-style-concurrency/_index.md"` exits 0.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `just-enough-elixir` (Primer · Elixir, `<SYLLABUS>courses/just-enough-elixir.md`) — Elixir
      syntax, pattern matching — all 9 convention steps complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_
- [ ] [AI] `actor-model-concurrency` (By Example · Elixir, `<SYLLABUS>courses/actor-model-concurrency.md`)
      — actors, supervision trees — all 9 convention steps complete; checkers clean; additionally both
      prerequisites are declared:
      `grep -F -q 'just-enough-elixir' "<COURSES>actor-model-concurrency/_index.md"` exits 0 **and**
      `grep -F -q 'concurrency-and-parallelism' "<COURSES>actor-model-concurrency/_index.md"` exits 0.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

  **Gherkin (binds) →** "The two concurrency-paradigm courses each build on the shared foundation, not on each other"

  ```gherkin
  Scenario: The two concurrency-paradigm courses each build on the shared foundation, not on each other
    Given csp-style-concurrency and actor-model-concurrency are both authored
    When a reader compares their prerequisite chains
    Then each declares concurrency-and-parallelism as a shared prerequisite
    And neither declares the other as a prerequisite, since they teach independent paradigms
  ```

**Per-band closing steps**:

- [ ] [AI] Add each landed course's row to
      [tech-docs §Course Library Catalog](./tech-docs.md#course-library-catalog) and its ID to
      `<COURSES>_index.md`.
- [ ] [AI] Record the band-completion signal:

  ```text
  BAND: Band 4 — Concurrency languages
  PLAN: ayokoding-learning-path-05-course-authoring-platform-and-concurrency
  LANDED_COURSE_IDS:
  just-enough-go
  csp-style-concurrency
  just-enough-elixir
  actor-model-concurrency
  GROW_MANIFESTS:
  apps/ayokoding-www/src/features/course-paths/manifests/careers/interview-ready/software-engineer.yaml
  apps/ayokoding-www/src/features/course-paths/manifests/careers/immediately-effective/software-engineer.yaml
  apps/ayokoding-www/src/features/course-paths/manifests/careers/fundamentally-strong/software-engineer.yaml
  MERGED_COMMIT: <fill in with this phase's PR merge commit SHA at execution time>
  ```

- [ ] [AI] Confirm zero manifest files were touched:
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      returns **0**.

  **Gherkin (binds) →** "just-enough-go is ready as build-your-own-raft's declared prerequisite"

  ```gherkin
  Scenario: just-enough-go is ready as build-your-own-raft's declared prerequisite
    Given just-enough-go is authored and merged to origin/main
    When ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own's build-your-own-raft authoring begins
    Then the just-enough-go course body resolves under the courses bucket
    And the band-completion signal naming just-enough-go among the Band-4 IDs is present on origin/main
  ```

### Phase 2 Gate

- [ ] [AI] All 4 Band-4 bodies exist:
      `for s in just-enough-go csp-style-concurrency just-enough-elixir actor-model-concurrency; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done | wc -l`
      returns **0** (returns 4 before this phase).
- [ ] [AI] Both By-Example bodies declare `concurrency-and-parallelism` and their paired primer as
      prerequisites (4 pairing checks total).
- [ ] [AI] Checkers clean; build + `lint:md` exit 0.
- [ ] [AI] Catalog rows added; band signal recorded with all five fields; zero manifest files touched.
- [ ] [AI] Draft PR opened at Phase 2 (this unit's own boundary); 3-cycle PR-Review complete; CI
      green; PR `[AI]`-merged; deployed. Record the merge commit SHA into the `MERGED_COMMIT` field
      of this phase's band-completion signal above.

> **Pause Safety**: both concurrency-paradigm tracks are live and complete;
> `ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own`'s `build-your-own-raft`
> prerequisite (`just-enough-go`) is now present. Safe to stop. To resume: re-run the section build.

---

## Phase 3: Section & Authored-Tree Verification

- [ ] [AI] **Verify all 14 authored bodies are present** —
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done < evidence/authored-body-slugs.txt | wc -l`
      — acceptance: returns **0**. Falsifiable both ways: this returned **14** at the Phase-0 baseline,
      and removing any one bundle makes it return 1.
- [ ] [AI] **Verify every authored body declares prerequisites** —
      `while read -r s; do grep -F -q 'prerequisites:' "apps/ayokoding-www/content/en/learn/courses/$s/_index.md" || echo "MISSING $s"; done < evidence/authored-body-slugs.txt | wc -l`
      — acceptance: returns **0** (returns 14 at baseline).
- [ ] [AI] **Verify every authored body has both tracks** —
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s/learning" && test -d "apps/ayokoding-www/content/en/learn/courses/$s/drilling" || echo "INCOMPLETE $s"; done < evidence/authored-body-slugs.txt | wc -l`
      — acceptance: returns **0**.
- [ ] [AI] Run affected quality gates from the worktree:
      `npx nx affected -t typecheck lint test:quick test:unit specs:behavior:coverage`
      — acceptance: exits 0. Fix ALL failures, including preexisting ones (Root Cause Orientation).
- [ ] [AI] Build the site: `npx nx run ayokoding-www:build` — acceptance: exits 0.
- [ ] [AI] Run link + heading-hierarchy + markdown validation:
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md heading-hierarchy validate` + `npm run lint:md`, plus the scoped link gate:

  ```bash
  cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate \
    --quiet \
    --exclude plans/done \
    --exclude apps/ose-www/content 2>&1 | grep -F "learn/courses/"
  ```

  — acceptance: the first two exit 0 and the `grep` finds **no** line naming a `learn/courses/` path
  belonging to one of these 14 slugs (exits 1; a hit naming another plan's course is out of this
  plan's scope and is not this plan's own failure — re-run scoped to the 14 slugs in
  `evidence/authored-body-slugs.txt` if ambiguity arises).

  **Gherkin (binds) →** "The authored platform-and-concurrency course library builds and validates green"

  ```gherkin
  Scenario: The authored platform-and-concurrency course library builds and validates green
    Given all 14 course bodies this plan authors have landed under the courses bucket
    When the ayokoding-www build, markdownlint, link validation, and heading-hierarchy validation run
    Then the build succeeds over the authored tree
    And link, heading-hierarchy, and markdownlint validation report no errors across the 14 course bodies
  ```

- [ ] [AI] **Verify zero manifest files were touched by this entire plan** —
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0** on this phase's own branch.
- [ ] [AI] **Verify both band-completion signals are complete** — anchor the count on the field's
      line-start form so this checklist's own prose mentions of the bare substring `MERGED_COMMIT:`
      are never counted:
      `for c in $(grep -oE '^MERGED_COMMIT: [0-9a-f]{7,40}$' delivery.md | awk '{print $NF}'); do git cat-file -e "$c^{commit}" || echo "BAD $c"; done | wc -l`
      — acceptance: returns **0**, and `grep -cE '^MERGED_COMMIT: [0-9a-f]{7,40}$' delivery.md`
      returns **2** (one genuine signal block per band).

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes
> (Root Cause Orientation). Commit preexisting fixes separately with conventional-commit messages.

### Phase 3 Gate

- [ ] [AI] All three 14-body structural loops (presence, prerequisites, both tracks) return 0.
- [ ] [AI] Affected `typecheck / lint / test:quick / test:unit / specs:behavior:coverage` exit 0.
- [ ] [AI] Build + heading-hierarchy + markdownlint green; the scoped link gate finds no failure among
      this plan's 14 course paths.
- [ ] [AI] Zero manifest files touched across the whole plan's history; both band signals complete
      with resolvable `MERGED_COMMIT` SHAs.
- [ ] [AI] Draft PR opened at Phase 3 (this unit's own boundary); 3-cycle PR-Review complete; CI
      green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the authored library passes every automated gate. Safe to stop. To resume: re-run
> the affected quality gates + build.

---

## Phase 4: Manual Content Verification (Playwright MCP)

> **Locale scope**: this plan's content is authored `en`-only — an Indonesian content mirror is
> explicitly deferred. Verify the authored course pages in `en` only.
>
> **Rule-15 exemption (recorded, not silently omitted)**: the three live-site testers are **exempt for
> this plan**, for the same three reasons plan04 recorded — see
> [README §Rule-15](./README.md#rule-15-three-tester-retest--exemption-recorded). **The exemption is
> narrow** — the Playwright manual behavioural verification below is mandatory and performed, with
> committed evidence.

- [ ] [AI] Confirm `en` is the content locale for this plan's course bodies — command:
      `test -d apps/ayokoding-www/content/en/learn/courses/just-enough-kotlin && test ! -d apps/ayokoding-www/content/id/learn/courses/just-enough-kotlin`
      — acceptance: exits 0.
- [ ] [AI] Start dev server: `npx nx dev ayokoding-www` — acceptance: server up on port 3101.
- [ ] [AI] **Sample-verify authored course pages** — for a sample of **six** authored courses (each
      primer/platform pair once, plus `linux-app-development`), at breakpoints 375 / 768 / 1280 px,
      via Playwright MCP: `browser_navigate` to `/en/learn/courses/<course-id>`, `browser_resize`,
      then `browser_snapshot` — acceptance: each page renders its overview, learning track, and
      drilling track; `html[lang]` is `en`; `browser_console_messages` reports **zero** errors per
      page per breakpoint.
- [ ] [AI] **Verify prerequisite rendering** — on `android-app-development`, confirm the declared
      `just-enough-kotlin` prerequisite is displayed and its link resolves to that primer's canonical
      page — acceptance: the link target returns 200 and the landed page is `just-enough-kotlin`.
- [ ] [AI] **Verify a drilling track renders** — open `csp-style-concurrency/drilling/overview.md` and
      confirm all five fixed sections are present in the rendered output — acceptance: five section
      headings visible in `browser_snapshot`.
- [ ] [AI] Capture one screenshot per sampled course per breakpoint to
      `evidence/phase-4-<course-id>-en-<breakpoint>px.png` — acceptance:
      `git ls-files -- 'evidence/phase-4-*-en-*px.png' | grep -c .` returns **18** (6 courses × 3
      breakpoints), once the captures are staged or committed.
- [ ] [AI] Document the evidence in this checklist: reference each screenshot
      (`![alt](./evidence/...)`) and note the console/network status per sampled course.
- [ ] [AI] **Record the rule-15 exemption in `learnings.md`** with its three reasons and a pointer to
      the navigation-UI plan that carries the triad.
- [ ] [AI] **Confirm no manifest file changed in this phase** —
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**.

### Phase 4 Gate

- [ ] [AI] Six sampled courses verified across three breakpoints in `en`; zero console errors;
      prerequisite display and drilling-track rendering confirmed.
- [ ] [AI] 18 screenshots present under `evidence/` and referenced in this checklist.
- [ ] [AI] The rule-15 exemption is recorded with reasons; the triad itself is **not** run here.
- [ ] [AI] Zero manifest files touched.
- [ ] [AI] **No PR opens for this phase** (intermediate): the evidence commits are on the shared
      worktree, this phase's own gate above is green, and nothing is pushed for review yet — the
      closeout PR for Phases 4–7 opens at Phase 7.

> **Pause Safety**: the authored library is verified live and defect-clean in `en`. Safe to stop. To
> resume: restart the dev server and re-open the six sampled courses.

---

## Phase 5: Final `origin/main` Integration & CI Verification

- [ ] [AI] Confirm no plan PR is still open:
      `gh pr list --search "ayokoding-learning-path-05-course-authoring-platform-and-concurrency" --state open --json number --jq 'length'`
      — acceptance: returns **0**.
- [ ] [AI] Sync the worktree to latest `origin/main` and run the full affected suite:
      `npx nx affected -t typecheck lint test:quick test:unit specs:behavior:coverage` +
      `npx nx run ayokoding-www:build` — acceptance: all exit 0 on the integrated `main`.
- [ ] [AI] Monitor the final `main` CI run (poll every ~2 min; one
      `gh run view --json status,conclusion` per wakeup; never `gh run watch`) — acceptance: all
      GitHub Actions green; fix root causes and push follow-ups until green. Any follow-up PR carries
      the identical individual manifest-diff check on its own branch before it merges.
- [ ] [AI] Confirm `prod-ayokoding-www` serves the authored bodies — spot-check four canonical course
      URLs across both bands — acceptance: each returns 200 with the expected course title.
      Re-dispatch `apps-ayokoding-www-deployer` if any earlier deploy lagged.
- [ ] [AI] **Notify the downstream plans** — confirm both band-completion signals are present in this
      file on `origin/main` and reachable by the manifest-growth plan and
      `ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own` — command (single line):
      `git ls-tree -r --name-only origin/main -- plans | grep -F 'ayokoding-learning-path-05-course-authoring-platform-and-concurrency/delivery.md'`
      prints **exactly one** path, and
      `git show "origin/main:<the printed path>" | grep -cE '^MERGED_COMMIT: [0-9a-f]{7,40}$'`
      returns **2**. **Never put a glob in a `git show <rev>:<path>` argument** — see plan04's own
      note for why this fails silently under zsh and under `git show`.

### Phase 5 Gate

- [ ] [AI] Zero open plan PRs; every prior phase merged to `main`.
- [ ] [AI] Full affected suite + build green on integrated `main`; final `main` CI run green.
- [ ] [AI] `prod-ayokoding-www` serving the authored bodies (four spot-checks return 200).
- [ ] [AI] Both band signals present on `origin/main` and reachable downstream.
- [ ] [AI] **No PR opens for this phase** (intermediate): the verification above runs directly
      against the already-integrated `main`, this phase's own gate is green, and nothing new is
      pushed for review — the closeout PR for Phases 4–7 opens at Phase 7.

> **Pause Safety**: the whole plan is integrated on `main`, green in CI, and live in production; the
> downstream plans have everything they need. Safe to stop. To resume: re-run the affected suite on
> `main` and check CI/prod status.

---

## Phase 6: Knowledge Capture

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)._

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only entries where a durable
      surface would catch this automatically next time; discard the rest with a one-line reason.
- [ ] [AI] Apply the **secret/sensitivity gate** to every surviving entry — sanitize to `<placeholder>`
      tokens or discard if the entry cannot be sanitized without losing its meaning.
- [ ] [AI] Apply the **repo-relevance gate** to every surviving entry — infra-private content stays in
      `ose-private` only.
- [ ] [AI] Route each surviving entry to exactly one durable home. **Code homes (`apps/`, `libs/`,
      tests) are ALWAYS filed as a separate `plans/backlog/<slug>/` plan and NEVER landed inline.**
- [ ] [AI] If execution genuinely surfaced no generalizable learning, record the explicit escape
      `No generalizable learnings — <reason>` instead of individual entries.
- [ ] [AI] **Confirm no manifest file changed in this phase** —
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**.

### Phase 6 Gate

- [ ] [AI] Every `learnings.md` entry is terminal (routed inline / filed as backlog / discarded with
      reason) or the explicit "none" escape is present.
- [ ] [AI] No code-homed learning landed inline in this plan's own commits/PRs.
- [ ] [AI] Zero manifest files touched.
- [ ] [AI] **No PR opens for this phase** (intermediate): the `learnings.md` triage is committed on
      the shared closeout branch, this phase's own gate above is green, and nothing is pushed for
      review yet — the closeout PR for Phases 4–7 opens at Phase 7.

> **Pause Safety**: `learnings.md` is fully triaged; nothing depends on querying it later. Safe to
> stop. To resume: re-read `learnings.md` and confirm every entry is terminal.

---

## Phase 7: Plan Archival

- [ ] [AI] Verify ALL delivery checklist items are ticked.
- [ ] [AI] Verify the Knowledge Capture phase is complete (every entry terminal or the explicit "none"
      escape present; both safety gates applied to every surviving entry).
- [ ] [AI] Verify ALL quality gates pass (local + CI) and the build is green.
- [ ] [AI] Verify ALL manual assertions pass (Playwright MCP) with committed evidence in `evidence/`;
      the `en` content locale exercised.
- [ ] [AI] Verify the **rule-15 exemption is recorded with reasons** in `learnings.md` and in Phase 4 —
      acceptance: `grep -F -q 'rule-15' learnings.md` exits 0.
- [ ] [AI] **Verify this plan's authored-body assertion** —
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done < evidence/authored-body-slugs.txt | wc -l`
      returns **0**, and `wc -l < evidence/authored-body-slugs.txt` returns **14** — acceptance: both
      hold. **This plan asserts 14, not 90 and not 127.**
- [ ] [AI] **Verify the ownership invariant held** —
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      returns **0** on this phase's own diff.
- [ ] [AI] **Verify every cross-plan reference still resolves** — re-run the cross-plan link gate:

  ```bash
  cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate \
    --quiet \
    --exclude plans/done \
    --exclude apps/ayokoding-www/content \
    --exclude apps/ose-www/content 2>&1 | grep -F "ayokoding-learning-path-05-course-authoring-platform-and-concurrency"
  ```

  — acceptance: the `grep` finds **no** matching line (exits 1).

- [ ] [AI] Move: `git mv plans/backlog/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/ plans/done/YYYY-MM-DD__ayokoding-learning-path-05-course-authoring-platform-and-concurrency/`
      using today's **completion** date, not the creation date (the `evidence/` subfolder moves with
      it).
- [ ] [AI] Update `plans/backlog/README.md` and `plans/in-progress/README.md` — remove the plan entry
      from whichever holds it at that point.
- [ ] [AI] Update `plans/done/README.md` — add the plan entry with completion date.
- [ ] [AI] Update any other READMEs that reference this plan and notify
      `ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own` and the manifest-growth
      plan, whose `Depends-on` tables name this plan by folder path — acceptance: no sibling plan's
      link to this folder is left dangling.
- [ ] [AI] Commit the archival:
      `chore(plans): move ayokoding-learning-path-05-course-authoring-platform-and-concurrency to done`.

### Phase 7 Gate

- [ ] [AI] All 14 authored bodies present (the ABSENT loop returns 0, down from the Phase-0 baseline
      of 14); the slug register holds 14 unique lines.
- [ ] [AI] Zero manifest files touched across the plan's entire history.
- [ ] [AI] The cross-plan link gate is green.
- [ ] [AI] Plan folder is under
      `plans/done/YYYY-MM-DD__ayokoding-learning-path-05-course-authoring-platform-and-concurrency/`;
      all READMEs updated; archival committed.
- [ ] [AI] Draft PR opened for the Phase 4–7 closeout unit (manual verification evidence,
      `learnings.md` triage, and the archival move — this unit's own boundary); 3-cycle PR-Review
      complete; CI green; PR `[AI]`-merged; deployed (no-op).

> **Pause Safety**: the plan is archived and its final PR `[AI]`-merged to `main`. Terminal state. To
> resume: nothing — the plan is complete.

---

### Commit Guidelines (all phases)

- [ ] [AI] Commit changes thematically — group related changes into logically cohesive commits (one
      course bundle per commit is the natural unit here).
- [ ] [AI] Follow Conventional Commits: `<type>(<scope>): <description>` (imperative, no period) —
      e.g. `feat(ayokoding-www): add just-enough-kotlin course body`.
- [ ] [AI] Split domains/concerns into separate commits; preexisting fixes get their own commits.
- [ ] [AI] Do NOT bundle unrelated changes into a single commit.
- [ ] [AI] Stage only this plan's paths (`git add <explicit paths>`) — **never** `git add -A`; sibling
      split plans are being authored concurrently in the same repo.

### Local Quality Gates (Before Every Push)

- [ ] [AI] `npx nx affected -t typecheck` exits 0.
- [ ] [AI] `npx nx affected -t lint` exits 0.
- [ ] [AI] `npx nx affected -t test:quick test:unit` exits 0.
- [ ] [AI] `npx nx affected -t specs:behavior:coverage` exits 0.
- [ ] [AI] `npm run lint:md` exits 0.
- [ ] [AI] Fix ALL failures — including preexisting issues not caused by your changes (Root Cause
      Orientation).

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes.
> This follows the root cause orientation principle — proactively fix preexisting errors encountered
> during work. Commit preexisting fixes separately with appropriate conventional-commit messages.

### Note: plan location at archival time

This plan is created in `plans/backlog/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/`.
When work starts it is promoted to
`plans/in-progress/ayokoding-learning-path-05-course-authoring-platform-and-concurrency/` (no date
prefix on either); the `git mv` in Phase 7 then archives it to
`plans/done/YYYY-MM-DD__ayokoding-learning-path-05-course-authoring-platform-and-concurrency/` using
the completion date.
