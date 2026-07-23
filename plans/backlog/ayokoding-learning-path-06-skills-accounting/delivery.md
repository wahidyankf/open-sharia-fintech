# Delivery Checklist — Skills Paths: Accounting

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`). `[HUMAN]`:
> only a human can do it (physical action, out-of-band approval, real-secret or privileged-credential
> handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate`: a must-pass verification checklist plus
> a **Pause Safety** note (the safe-to-stop state after the phase and the single command to resume). A
> phase is **not complete until its gate is green**; do not start phase N+1 while any check in phase
> N's gate is failing.

## Worktree

**One worktree per parallel unit — strict 1 PR ↔ 1 worktree.** Git permits exactly one checked-out
branch per worktree, so the N concurrent course PRs this plan declares below require N worktrees; a
single shared worktree cannot host them. The base worktree carries the sequential phases; each
parallel authoring leaf gets its own. All paths follow the
[Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md)
(`worktrees/<name>/`, routed by the repo-local `WorktreeCreate` hook); names stay lowercase
kebab-case, so the per-unit suffix is `-unit-<unit-id>`, never an underscore separator.

Base worktree — sequential phases (0, 1, 4, 6-10):

```
worktrees/ayokoding-learning-path-06-skills-accounting/
```

Per-unit worktrees — one per course-authoring leaf and per manifest-growth cycle in Phases 2, 3, 5,
where `<unit-id>` is the course id (or `manifest-conventional` / `manifest-sharia`):

```
worktrees/ayokoding-learning-path-06-skills-accounting-unit-<unit-id>/
```

```bash
claude --worktree ayokoding-learning-path-06-skills-accounting
# and, per parallel unit:
claude --worktree ayokoding-learning-path-06-skills-accounting-unit-<unit-id>
```

> Provision the base worktree before Phase 0. Do not begin Phase 0 outside it. Provision a per-unit
> worktree at the start of each parallel unit and remove it once that unit's PR has merged — worktree
> removal is the terminal cleanup node of each parallel phase, per
> [Worktree and Artifact Cleanup](../../../repo-governance/development/workflow/worktree-and-artifact-cleanup.md).
> Never exceed the in-force concurrency cap in live worktrees.

## Delivery Mode: worktree-to-pr

Each course-authoring sub-phase (Phase 2, 3, 5) is its own **DAG leaf**: its own branch, its own draft
PR, its own 3-cycle fan-out → `pr-review-synthesis-maker` → `pr-review-fixer` review, its own `[AI]` merge — strict
1-PR-per-course, pipelined up to the in-force concurrency cap (N=3 unless the programme has since
escalated it — check the latest `AGENTS.md` §Agent Workflow Orchestration value before starting).
Manifest-growth TDD cycles and landing authoring are each their own PR too, sequenced after the
courses each phase's manifest step depends on. **Phase 0 is not a DAG leaf** — it is Environment
Setup and Baseline, so it opens no PR, pushes no branch, runs no review cycle, and merges nothing;
the earliest PR belongs to Phase 1
([§Phase 0 Opens No PR](../../../repo-governance/conventions/structure/plans.md#phase-0-opens-no-pr--the-earliest-pr-is-phase-1-hard-rule)).
See
[PR Review Quality Gate workflow](../../../repo-governance/workflows/pr/pr-review-quality-gate.md).

**Per-merge integration protocol.** After each `[AI]` merge above: confirm CI green on `origin/main`
for the merged SHA, then **dispatch `apps-ayokoding-www-deployer`** to deploy `ayokoding-www` to
`prod-ayokoding-www` — a no-op redeploy where a phase changed no app content. The deployer is a
declared dependency of this plan
([tech-docs §Dependencies](./tech-docs.md#dependencies)); a phase that merges app content without
dispatching it leaves production stale behind `origin/main`, and Phase 8's production check will
fail.

## Depends-on and start preconditions

- **`blockedBy`**: `ayokoding-learning-path-01-url-restructure` (the three-bucket URL grammar and
  `<COURSES>_index.md`), `ayokoding-learning-path-02-schema-and-prerequisite-dag` (the `PathManifest`
  schema, `course-paths` core, `<MANIFESTS>` directory), and
  `ayokoding-learning-path-03-navigation-ui` (`path-landing.tsx`, `path-card.tsx`,
  `manifest-repository.ts`, the `?path=` wiring) — **all three hard**, matching
  [README §Depends-on](./README.md#depends-on) and
  [tech-docs §Dependencies](./tech-docs.md#dependencies). Plan 03 is not optional: a manifest with no
  renderer is invisible, so without it this plan's landings cannot be verified at Phase 7 at all.
- **`blocks`**: `ayokoding-learning-path-07-skills-erp` at the stage granularity described in
  [tech-docs §Stage-signal contract](./tech-docs.md#stage-signal-contract-the-plan-07-handoff-stage-granularity).
- Start precondition: **all three** blocking plans merged to `origin/main` — 01, 02 **and 03**.
  Verify each independently rather than with one aggregate count, so a missing plan cannot hide behind
  another's commits:

  ```bash
  for n in 01-url-restructure 02-schema-and-prerequisite-dag 03-navigation-ui; do
    git log origin/main --oneline | grep -q "ayokoding-learning-path-${n}" \
      || echo "NOT MERGED: ayokoding-learning-path-${n}"
  done
  ```

  Acceptance: **empty output**. A single `grep -c "…-0[123]"` returning ≥ 1 is **not** sufficient — it
  passes when only one of the three has merged. Adjust the per-plan patterns if the actual
  merge-commit subjects differ, but keep the check one-per-plan.

## Parallelization Model

Two independent manifests share one course corpus. Within a stage, courses with no prerequisite edge
between them author in parallel up to the concurrency cap; courses with an edge serialize. The two
manifests' TDD growth cycles are two separate, parallelizable sub-phases once their shared courses
exist. See [tech-docs §The ramp order](./tech-docs.md#the-twenty-four-course-catalog) for the full
topological ordering this parallelization respects.

**Each parallel unit runs in its own worktree** (see [§Worktree](#worktree)) — the fan-out is bounded
by the concurrency cap, and the number of live per-unit worktrees never exceeds it.

## Path constants

```bash
# Run from the repo root. Detects this plan's current lifecycle stage and re-derives every path.
if [ -d "plans/backlog/ayokoding-learning-path-06-skills-accounting" ]; then
  PLANDIR="plans/backlog/ayokoding-learning-path-06-skills-accounting/"
elif [ -d "plans/in-progress/ayokoding-learning-path-06-skills-accounting" ]; then
  PLANDIR="plans/in-progress/ayokoding-learning-path-06-skills-accounting/"
else
  PLANDIR=$(find plans/done -maxdepth 1 -type d -name "*ayokoding-learning-path-06-skills-accounting" | head -1)/
fi
echo "PLANDIR=$PLANDIR"
```

- `COURSES="apps/ayokoding-www/content/en/learn/courses/"`
- `LANDING_CA="apps/ayokoding-www/content/en/learn/paths/skills/conventional-accounting/"`
- `LANDING_SA="apps/ayokoding-www/content/en/learn/paths/skills/sharia-accounting/"`
- `MANIFEST_CA="apps/ayokoding-www/src/features/course-paths/manifests/skills/conventional-accounting.yaml"`
- `MANIFEST_SA="apps/ayokoding-www/src/features/course-paths/manifests/skills/sharia-accounting.yaml"`
- `MTEST_CA="apps/ayokoding-www/src/features/course-paths/manifests/skills/conventional-accounting-manifest.unit.test.ts"`
- `MTEST_SA="apps/ayokoding-www/src/features/course-paths/manifests/skills/sharia-accounting-manifest.unit.test.ts"`
- `SPEC="${PLANDIR}syllabus/courses/"`
- `SPECPATHS="${PLANDIR}syllabus/paths/"`
- `SPECS="specs/apps/ayokoding/behavior/ayokoding-www/gherkin/course-paths/"`

## Course ID lists (define once, reuse in every clause — DD-622 HARD rule: shell ARRAYS only)

```bash
ACCT_S1=(accounting-foundations chart-of-accounts-and-data-modeling financial-statements-and-close-cycle)

ACCT_S2=(journal-entries-and-posting-mechanics accrual-accounting-and-revenue-recognition \
  accounts-payable-and-procure-to-pay accounts-receivable-and-order-to-cash \
  managerial-and-cost-accounting fixed-assets-and-depreciation inventory-and-cogs-accounting \
  lease-and-intangible-asset-accounting multi-currency-accounting-and-fx-translation \
  consolidation-and-multi-entity-accounting financial-reporting-standards-ifrs-vs-gaap \
  audit-controls-and-compliance payroll-and-tax-accounting-essentials treasury-and-cash-management \
  financial-reporting-and-xbrl general-ledger-system-architecture)

ACCT_S3=(sharia-accounting-and-aaoifi-standards islamic-contract-modeling-for-systems \
  zakah-computation-and-reporting-for-systems sukuk-and-islamic-capital-markets-accounting \
  sharia-ledger-system-architecture)

ACCT_SHARED=("${ACCT_S1[@]}" "${ACCT_S2[@]}")   # 19 — conventional-accounting.yaml's full courseOrder
ACCT_ALL=("${ACCT_SHARED[@]}" "${ACCT_S3[@]}")  # 24 — sharia-accounting.yaml's full courseOrder
ACCT_SILENT=("${ACCT_S2[@]}" "${ACCT_S3[@]}")   # 21 — every course from #4 on (DD-609)
```

**Never** iterate these as a space-separated string — zsh does not word-split unquoted parameters, and
a string form silently short-circuits to a single false-passing iteration (DD-622).

---

## Phase 0: Environment Setup and Baseline

> _Suggested executor: direct tool use, no content-authoring agent needed._

### Environment Setup

- [ ] [AI] Confirm the worktree is provisioned and current: `git worktree list | grep -F "ayokoding-learning-path-06-skills-accounting"` exits 0.
- [ ] [AI] Install dependencies: `npm install`.
- [ ] [AI] Run doctor to verify tooling: `npm run doctor -- --fix`.
- [ ] [AI] Verify dev server starts: `nx dev ayokoding-www` (start, confirm it serves, stop).
- [ ] [AI] Verify existing tests pass before making changes: `nx run ayokoding-www:test:quick`.

### Baseline (must all be true before any content is authored)

- [ ] [AI] All **three** blocking plans merged (01, 02, 03) — run the per-plan loop in
      [§Depends-on](#depends-on-and-start-preconditions); acceptance: empty output.
- [ ] [AI] `<PLANDIR>` resolves and the **pre-authored** syllabus corpus is present:
      `test -d "${SPEC}" && [ "$(find "${SPEC}" -maxdepth 1 -name '*.md' ! -name 'README.md' | wc -l)" -eq 24 ] && echo BASELINE-OK || echo BASELINE-FAIL`
      — acceptance: prints `BASELINE-OK`.
      This deliberately asserts **presence, not absence**. The 24 syllabus specs are authored ahead of
      execution (see §1.2, which re-verifies rather than authors), so a check asserting the folder
      does **not** exist could never pass and would deadlock the Phase 0 Gate. Falsifiable both ways:
      a missing folder or any count other than 24 prints `BASELINE-FAIL`. The count excludes
      `syllabus/courses/README.md` (required by the Learning-Bearing Syllabus Completeness
      convention) — a naive `ls "${SPEC}"*.md | wc -l` would match the README too and return 25,
      misfiring on the very state this check is meant to confirm as correct.
- [ ] [AI] Neither manifest exists yet:
      `test -f "$MANIFEST_CA" && echo FOUND || echo ABSENT` prints `ABSENT`, and the same for
      `$MANIFEST_SA` — acceptance: both print `ABSENT`. Falsifiable both ways: both flip to `FOUND`
      after Phase 2.
- [ ] [AI] No course in `ACCT_ALL` exists yet:
      `for c in "${ACCT_ALL[@]}"; do test -d "${COURSES}$c" && echo "FOUND $c"; done | wc -l` returns
      **0** — acceptance: returns 0 today, returns 19 after Phase 3, returns 24 after Phase 5.
- [ ] [AI] Neither landing exists yet: `test -d "$LANDING_CA" && echo FOUND || echo ABSENT` prints
      `ABSENT`, and the same for `$LANDING_SA`.
- [ ] [AI] `verification-log.md`'s `OI-2: OPEN` line is present and unmodified:
      `grep -c '^OI-2: OPEN$' "${PLANDIR}verification-log.md"` returns **1** — this is the gate that
      must still hold at the **end** of Phase 4, not just here.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [ ] [AI] `npm run doctor -- --fix` exits 0.
- [ ] [AI] `nx run ayokoding-www:test:quick` exits 0.
- [ ] [AI] Every Baseline check above holds.

> **Pause Safety**: no plan content exists yet; the worktree is clean and tooling-verified. Safe to
> stop. To resume: re-run `nx run ayokoding-www:test:quick` and confirm 0 exit before starting Phase 1.

---

## Phase 1: The twenty-four syllabus specs

> _Suggested executor: direct authoring (this plan's own maintainer), `web-researcher` (coverage
> pass only, per A12), then delegate content authoring per course to
> `apps-ayokoding-www-by-example-maker` / `apps-ayokoding-www-annotated-concept-maker` in Phases 2/3/5._
>
> **A12 order of operations, not optional.** Every syllabus below is authored **first**, from domain
> reasoning and this plan's own grounding file; only **after** a syllabus exists does step 1.3 dispatch
> `web-researcher`, and only to check coverage. See
> [tech-docs §Post-authoring verification](./tech-docs.md#syllabus-layer--custody-and-shape) and
> [tech-docs §Programme decisions — A12](./tech-docs.md#programme-decisions).

### 1.1 · Verify the spec folder (pre-authored — this sub-phase verifies, it does not scaffold)

- [ ] [AI] `"${SPEC}"` and `"${SPECPATHS}"` already exist and are populated — acceptance:
      `test -d "${SPEC}" && test -d "${SPECPATHS}" && [ "$(find "${SPEC}" -maxdepth 1 -name '*.md' ! -name 'README.md' | wc -l)" -eq 24 ] && [ "$(find "${SPECPATHS}" -maxdepth 1 -name '*.md' ! -name 'README.md' | wc -l)" -eq 2 ] && echo PASS || echo FAIL`
      prints `PASS`. Create either folder only if this check reports `FAIL`. Both counts exclude
      each folder's own `README.md` (required by the Learning-Bearing Syllabus Completeness
      convention) — a naive `ls *.md | wc -l` would match the README too and return 25/3 even in
      this fully-populated, correct state.
- [ ] [AI] Each subfolder's own index README exists individually, per the Learning-Bearing Syllabus
      Completeness convention's required-subfolder-README rule — acceptance:
      `test -f "${SPEC}README.md" && test -f "${SPECPATHS}README.md" && echo PASS || echo FAIL`
      prints `PASS`.
- [ ] [AI] Create `"${SPEC}../README.md"` _(new file)_ per
      [tech-docs §Syllabus layer](./tech-docs.md#syllabus-layer--custody-and-shape) with the course
      index table — acceptance: `test -f "${SPEC}../README.md"` exits 0, and
      `for c in "${ACCT_ALL[@]}"; do grep -F -q "$c" "${SPEC}../README.md" || echo "MISSING $c"; done | wc -l`
      returns **0**.

### 1.2 · Author every syllabus (already authored in this session; this sub-phase re-verifies)

- [ ] [AI] Confirm all 24 syllabus files exist, each following the plan-02-inherited shape (DD-627):
      `for c in "${ACCT_ALL[@]}"; do test -f "${SPEC}$c.md" || echo "MISSING $c"; done | wc -l` returns
      **0**. Falsifiable both ways: returns 24 before authoring, 0 after.
- [ ] [AI] Confirm every syllabus has no `## Capstone spec` section (A6) and does have
      `## Applied synthesis (no build — A6)`:
      `for c in "${ACCT_ALL[@]}"; do grep -q '^## Capstone spec' "${SPEC}$c.md" && echo "VIOLATION $c"; done | wc -l`
      returns **0**, AND
      `for c in "${ACCT_ALL[@]}"; do grep -q '^## Applied synthesis (no build — A6)' "${SPEC}$c.md" || echo "MISSING $c"; done | wc -l`
      returns **0**.
- [ ] [AI] Confirm every course from `ACCT_SILENT` carries a worked silent-failure example: for each
      `c` in `ACCT_SILENT`, `grep -c 'silent-failure' "${SPEC}$c.md"` returns ≥ 1 — acceptance:
      `for c in "${ACCT_SILENT[@]}"; do grep -q 'silent-failure' "${SPEC}$c.md" || echo "MISSING $c"; done | wc -l`
      returns **0** (21 courses checked).
- [ ] [AI] Confirm `#20` (`sharia-accounting-and-aaoifi-standards`) states OI-2 as `OPEN` and does not
      restate it as resolved:
      `grep -c 'OI-2 remains explicitly' "${SPEC}sharia-accounting-and-aaoifi-standards.md"` returns
      **1**, AND `grep -c 'OI-2.*RESOLVED' "${SPEC}sharia-accounting-and-aaoifi-standards.md"` returns
      **0**.

### 1.3 · Coverage pass (A12 step 2 — after authoring, never before)

- [ ] [AI] For each course, dispatch `web-researcher` (delegated, isolated context) with the question
      "what would a practitioner expect this syllabus's concept list to cover that it omits, and what
      does it include that the field does not recognise?" — never "does this match a named
      curriculum's structure." Record findings as `[Needs Verification]` annotations or new concept
      bullets **added to the existing syllabus**, never as a restructuring — acceptance: for every
      course, the syllabus's `## In which paths` section (the file's terminal, position-stable anchor)
      is unchanged by the coverage pass;
      `for f in $(find "${SPEC}" -maxdepth 1 -name '*.md' ! -name 'README.md'); do diff <(git show "HEAD:$f" | grep -E '^## ' | grep -vE '^## (Concepts|Worked examples|Accuracy notes)$') <(grep -E '^## ' "$f" | grep -vE '^## (Concepts|Worked examples|Accuracy notes)$') >/dev/null || echo "HEADINGS CHANGED $f"; done`
      returns empty — outside those three sections no heading is added, removed, or reordered. Excludes
      `README.md` (the folder's own index, not a course spec) from the iteration.
      Compares the two ordered heading lists directly instead of parsing diff output, so the verdict
      never depends on how `git diff` renders. The three excluded headings are the ones the coverage
      pass is allowed to create. Negative control: inserting or moving any other `##` heading in one
      syllabus makes it print that filename.
- [ ] [AI] Confirm no syllabus was rewritten to mirror an external curriculum's module titles or
      sequence — verify by reading the diff produced by this step, not by grep (a structural adoption
      would not leave a mechanically greppable signature).

### 1.4 · Licensing-sensitive-sources recording (DD-624)

- [ ] [AI] For each of the 24 syllabi, record which standard numbers it cites and whether it
      references any reference implementation, in a `## Accuracy notes` or a dedicated note — this is
      the list [Phase 6](#phase-6-section-and-app-verification)'s licensing reading audit checks
      against. Acceptance: every syllabus's `## Accuracy notes` section is non-empty:
      `for c in "${ACCT_ALL[@]}"; do grep -q '^## Accuracy notes' "${SPEC}$c.md" || echo "MISSING $c"; done | wc -l`
      returns **0**.
- [ ] [AI] Confirm the syllabus artifacts themselves — not only future course bodies — are in scope
      for the licensing acceptance clauses this plan carries: this is asserted mechanically at
      [Phase 6 §6.4](#64--licensing-reading-audit-a8--a12) below, which scans `"${SPEC}"` directly, not
      only `"${COURSES}"`.

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [ ] [AI] All 24 syllabus files exist, each with `## Applied synthesis (no build — A6)` and no
      `## Capstone spec`.
- [ ] [AI] All 21 `ACCT_SILENT` syllabi carry a worked silent-failure example.
- [ ] [AI] `#20`'s OI-2 framing holds (`OPEN`, not restated as resolved).
- [ ] [AI] Every syllabus has a non-empty `## Accuracy notes` licensing-sensitive-sources record.
- [ ] [AI] **Module-topic breakdown present in every syllabus** —
      `for f in $(find "${SPEC}" -maxdepth 1 -name '*.md' ! -name 'README.md'); do for h in '## Concepts' '## Worked examples' '## Prerequisites'; do grep -qF "$h" "$f" || echo "MISSING [$h] $(basename "$f")"; done; done | wc -l`
      returns **0**. Excludes `README.md` (the folder's own index, not a course spec) from the
      iteration. Negative control: deleting the `## Worked examples` heading from any one
      syllabus makes it return **1** (verified).
- [ ] [AI] **Concept floor holds ([DD-627](./tech-docs.md#design-decisions), ≥ 8)** —
      `for f in $(find "${SPEC}" -maxdepth 1 -name '*.md' ! -name 'README.md'); do n=$(grep -c '^- \*\*co-[0-9]' "$f"); [ "$n" -ge 8 ] || echo "UNDER-FLOOR $(basename "$f") = $n"; done | wc -l`
      returns **0**. Excludes `README.md` from the iteration. Negative control: several syllabi sit
      at exactly 8, so removing a single `- **co-NN` line from any of them makes it return **1**
      (verified) — the floor is tight, not slack.
- [ ] [AI] `npm run lint:md` exits 0 on the new `syllabus/` tree.
- [ ] [AI] **Every prerequisite edge is transcribed and resolves** — run the two commands in the
      fenced block below. Acceptance: the first returns **0** AND the second returns **34**. A zero
      from the first while the second is also 0 would be vacuous, so both are required. The `awk`
      range stops at the next `- **` bullet, so the `**Linked (SWE)**` edges (`sql-essentials`,
      `backend-essentials`) — deliberately external link-don't-walk references into plan 02's corpus
      — are excluded by construction rather than by an allowlist. Negative control: repointing one
      `**Prior courses**` id at a non-existent course makes the first return **1** (verified).

```bash
# (1) Unresolved prior-course edges. MUST print 0. Excludes README.md (find ! -name).
for f in $(find "${SPEC}" -maxdepth 1 -name '*.md' ! -name 'README.md'); do
  awk '/^- \*\*Prior courses\*\*/{p=1;print;next} p&&/^- \*\*/{p=0} p' "$f" \
    | grep -oE '`[a-z0-9-]+`' | tr -d '`' | while IFS= read -r id; do
        [ -f "${SPEC}${id}.md" ] || echo "UNRESOLVED $(basename "$f") -> $id"
      done
done | wc -l

# (2) Anti-vacuity companion: total edges examined. MUST print 34, never 0. Excludes README.md.
for f in $(find "${SPEC}" -maxdepth 1 -name '*.md' ! -name 'README.md'); do
  awk '/^- \*\*Prior courses\*\*/{p=1;print;next} p&&/^- \*\*/{p=0} p' "$f" \
    | grep -oE '`[a-z0-9-]+`'
done | wc -l
```

> **Pause Safety**: the full spec layer exists and is internally consistent; no course body or
> manifest exists yet. Safe to stop. To resume: re-run the Phase 1 Gate's `for`-loop checks and
> confirm 0 for each before starting Phase 2.

---

## Phase 2: Stage 1 — courses #1–#3, both manifests, both landings

> _Suggested executor: `apps-ayokoding-www-by-example-maker` (all three bodies are By Example) +
> `apps-ayokoding-www-general-maker` (both landings) + `web-researcher` (accuracy pre-verify)._
>
> **The first ramp boundary, the architecture smoke test, and the two-path split all land in one
> phase.** At its end a reader on either path can build a correctly balancing ledger, and the platform
> has its first two 2-segment `pathId`s resolving end to end.

### 2.1 · Author the three Stage-1 bodies (maker-checker-fixer, not TDD)

Apply the seven-step per-course convention to each course; each course is its own sub-phase (own
branch → draft PR → 3-cycle review → `[AI]` merge → deploy), pipelining up to the in-force cap.

1. [AI] **Accuracy pre-verify** — spot-check every external claim via `web-researcher`; volatile facts
   go in a dated accuracy-note sidebar, never the stable spine.
2. [AI] **Skeleton** — create `"${COURSES}<course-id>/"` (`_index.md` with `prerequisites: [...]`,
   `overview.md`, `learning/_index.md`, `drilling/_index.md`) from `"${SPEC}<course-id>.md"`.
3. [AI] **Author learning track** from the spec's `## Concepts` and `## Worked examples`, plus
   `learning/synthesis/` from `## Applied synthesis (no build — A6)` — **never** a `learning/capstone/`
   directory (A6).
4. [AI] **Author drilling track** — `drilling/<course-id>.md` + `drilling/overview.md`.
5. [AI] **Run content checkers** — `apps-ayokoding-www-by-example-checker`,
   `apps-ayokoding-www-facts-checker`, `apps-ayokoding-www-link-checker`.
6. [AI] **Apply content fixers** — every CRITICAL/HIGH/MEDIUM finding addressed.
7. [AI] **Re-verify** — checkers + `nx run ayokoding-www:build` + `npm run lint:md`.

- [ ] [AI] Course #1 `accounting-foundations` (By Example, no prerequisites) — mines the legacy
      accounting article per DD-626. **Resolve its path first, do not hardcode either location** —
      plan 01 relocates it and may or may not have merged when this step runs:
      `SRC=apps/ayokoding-www/content/en/legacy/business/accounting.md; [ -f "$SRC" ] || SRC=apps/ayokoding-www/content/en/learn/business/accounting.md; test -f "$SRC" && echo "MINING $SRC" || echo "SOURCE-MISSING"`
      — acceptance: prints `MINING <path>`, never `SOURCE-MISSING`. Then: all 7
      convention steps complete; checkers report zero CRITICAL/HIGH/MEDIUM;
      `grep -F -q 'chart-of-accounts-and-data-modeling' "${COURSES}accounting-foundations/overview.md"`
      exits 0 (forward boundary to #2 is stated). **No paragraph from the legacy article moves
      verbatim** — verified by reading the diff, not by grep.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Course #2 `chart-of-accounts-and-data-modeling` (By Example; prerequisites: #1 and the
      **linked** `sql-essentials`) — acceptance: all 7 steps complete;
      `grep -F -q 'sql-essentials' "${COURSES}chart-of-accounts-and-data-modeling/_index.md"` exits 0
      (linked edge declared) **and**
      `grep -F -q 'sql-essentials' "${COURSES}chart-of-accounts-and-data-modeling/overview.md"` exits 0
      (scope boundary stated — this course models ledgers, it does not teach SQL).
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Course #3 `financial-statements-and-close-cycle` (By Example; prerequisite: #2) — **the
      cross-plan hard edge**: ERP's record-to-report capability is unblocked by this course and
      nothing else — acceptance: all 7 steps complete; checkers report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] **Stage-1 body check** —
      `for c in "${ACCT_S1[@]}"; do test -d "${COURSES}$c" || echo "MISSING $c"; done | wc -l`
      — acceptance: returns **0** (returns **3** before this sub-phase).
- [ ] [AI] Append the three catalog rows to `"${COURSES}_index.md"` _(existing file, created by
      plan 01)_ — acceptance:
      `for c in "${ACCT_S1[@]}"; do grep -F -q "$c" "${COURSES}_index.md" || echo "MISSING $c"; done | wc -l`
      returns **0**; `apps-ayokoding-www-link-checker` green on `"${COURSES}_index.md"`.

### 2.2 · TDD cycle — publish BOTH manifests

- [ ] [AI] **RED** — create `$MTEST_CA` and `$MTEST_SA` _(new files; this plan owns both)_ with failing
      assertions that each manifest loads, zod-validates, declares `pathId` equal by **string
      equality** (never split-on-`/`) to `skills/conventional-accounting` / `skills/sharia-accounting`
      respectively, `arc` equal to `immediately-effective`, a `courseOrder` of **length 3** equal to
      `ACCT_S1` in order, and passes `checkManifestIntegrity` + `checkPrerequisiteConsistency`; plus
      one negative assertion per file that a malformed id is rejected by `safeParse`
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: both new test files **fail** with a module-not-found or empty-glob error naming
      their respective YAML file.

  **Gherkin (underpins) →** Outline "A two-segment skills path ID resolves end to end"
  (Examples: `skills/conventional-accounting`, `skills/sharia-accounting`)

  ```gherkin
  Scenario Outline: A two-segment skills path ID resolves end to end
    Given the manifest declares pathId <path_id> and arc immediately-effective
    When a reader walks the path from its landing
    Then the landing, the prev and next controls, and the breadcrumb all resolve against the two-segment path ID
    And the ?path=<path_id> context persists across every course in the walk
    And no resolver assumes a three-segment path ID

    Examples:
      | path_id                       |
      | skills/conventional-accounting |
      | skills/sharia-accounting       |
  ```

  Underpins only — supplies the manifest-field half for both Examples rows; §2.4's RED step carries the
  `binds` tag.

- [ ] [AI] **GREEN** — author `$MANIFEST_CA` and `$MANIFEST_SA` _(new files)_ each with its `pathId`,
      `arc: immediately-effective`, a title, a description, and a 3-entry `courseOrder`, **byte-identical
      to each other at this stage** (both hold exactly `ACCT_S1` in order), transcribed from
      `"${SPECPATHS}"`, entries as **plain ID strings**, no `framing` mappings (DD-606)
      — command: `nx run ayokoding-www:test:unit`
      — acceptance: both exit 0, AND
      `diff <(grep -E '^  - ' "$MANIFEST_CA") <(grep -E '^  - ' "$MANIFEST_SA" | head -3)` returns
      empty (the two manifests' first three entries are identical) — falsifiable both ways: after
      Phase 3 the two remain identical up to entry 19; after Phase 5 `$MANIFEST_SA` diverges by
      exactly the 5 `ACCT_S3` entries appended.
- [ ] [AI] **REFACTOR** — align YAML key order/comment style across both manifests; factor a shared
      load-and-validate helper in a common test utility so §3.2 and §5.2 add assertions, not copied
      blocks — command: `nx run ayokoding-www:test:unit && nx run ayokoding-www:lint` — acceptance:
      both exit 0; no assertion weakened.

- [ ] [AI] **Shared-course non-duplication check (A11)** — confirm no course file under `"${COURSES}"`
      is written twice and both manifests reference `ACCT_S1` by ID only:
      `for c in "${ACCT_S1[@]}"; do n=$(find "${COURSES}$c" -maxdepth 0 -type d | wc -l); [ "$n" -eq 1 ] || echo "DUPLICATE-OR-MISSING $c"; done | wc -l`
      returns **0**.

  **Gherkin (binds) →** "Shared courses are referenced by both manifests, never duplicated"

  ```gherkin
  Scenario: Shared courses are referenced by both manifests, never duplicated
    Given both accounting manifests are published
    When a reader inspects the courses/ directory for any of the nineteen shared course IDs
    Then exactly one course bundle exists per shared ID
    And both manifests' courseOrder reference that one ID
    And neither manifest's courseOrder contains a forked or renamed copy of it
  ```

### 2.3 · Both landings (content — maker-checker-fixer, not TDD)

- [ ] [AI] Author `"${LANDING_CA}_index.md"` _(new file)_ per
      [tech-docs §Landing content contract](./tech-docs.md#the-ramp-and-its-stages-per-path): the
      immediately-effective promise, the Dangerous-1 boundary, and the linked `sql-essentials` /
      `backend-essentials` prerequisites at their canonical URLs — acceptance:
      `grep -oE 'courseOrder' "${LANDING_CA}_index.md" | wc -l` returns **0**, AND
      `grep -F -q 'Dangerous 1' "${LANDING_CA}_index.md"` exits 0.
  - _Suggested executor: `apps-ayokoding-www-general-maker`_
- [ ] [AI] Author `"${LANDING_SA}_index.md"` _(new file)_ — same contract, plus a stated Sharia arc
      (the three-stage journey through Stage 3, even though only Stage 1 is published so far) and a
      **path-choice affordance note** distinguishing it from `conventional-accounting` — acceptance:
      `grep -F -q 'Dangerous 1' "${LANDING_SA}_index.md"` exits 0, AND
      `grep -F -q 'conventional-accounting' "${LANDING_SA}_index.md"` exits 0 (the path-choice note
      names its sibling).
  - _Suggested executor: `apps-ayokoding-www-general-maker`_

  **Gherkin (binds) →** Outline "A path landing states its arc and ramp before the course list"
  (Examples: `conventional-accounting`, `sharia-accounting`)

  ```gherkin
  Scenario Outline: A path landing states its arc and ramp before the course list
    Given the <path> path landing is published
    When a reader opens /en/learn/paths/skills/<path>
    Then the immediately-effective promise and the Dangerous-1 boundary appear before the ordered course list
    And the boundary names both what the reader can do and what the reader cannot yet do
    And the ordered course list is rendered from the manifest rather than hand-listed in the landing

    Examples:
      | path                    |
      | conventional-accounting |
      | sharia-accounting       |
  ```

- [ ] [AI] **Ordering check, both landings** —
      `for L in "$LANDING_CA" "$LANDING_SA"; do grep -oE 'journal-entries-and-posting-mechanics|sharia-accounting-and-aaoifi-standards' "${L}_index.md" | sort -u | wc -l; done`
      returns **0 0** (no later-stage course ID is hand-listed in either landing) — falsifiable both
      ways: hand-listing the corpus makes either count ≥ 1.
- [ ] [AI] Run `apps-ayokoding-www-link-checker` and `apps-ayokoding-www-general-checker` over both
      landings — apply fixers — acceptance: zero CRITICAL/HIGH/MEDIUM remain on re-run for both.

### 2.4 · TDD cycle — both path-walk e2e specs

- [ ] [AI] **RED** — add `"${SPECS}skills-path-composition.feature"` _(new
      file)_ carrying the two-Examples-row scenario above, plus failing e2e steps in
      `apps/ayokoding-www-fe-e2e/src/steps/skills-path-composition.steps.ts` _(new file, pairing 1:1)_
      that open each landing, walk all three courses via prev/next, assert `?path=` persistence, assert
      breadcrumb resolution, and assert a deliberately over-segmented id is hard-rejected — for **both**
      `pathId`s — command: `nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: the new spec **fails**
      for both Examples rows.

  **Gherkin (binds) →** Outline "A two-segment skills path ID resolves end to end"

  ```gherkin
  Scenario Outline: A two-segment skills path ID resolves end to end
    Given the manifest declares pathId <path_id> and arc immediately-effective
    When a reader walks the path from its landing
    Then the landing, the prev and next controls, and the breadcrumb all resolve against the two-segment path ID
    And the ?path=<path_id> context persists across every course in the walk
    And no resolver assumes a three-segment path ID

    Examples:
      | path_id                       |
      | skills/conventional-accounting |
      | skills/sharia-accounting       |
  ```

- [ ] [AI] **GREEN** — implement the step bindings against both published manifests and live landings
      — command:
      `nx run ayokoding-www:specs:behavior:coverage && nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: both exit 0.
- [ ] [AI] **REFACTOR** — extract a reusable "walk a skills path given a path id" helper step
      definition parameterized on `pathId`, so Phase 3 and Phase 5 reuse it without duplication
      — command: `nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: exits 0, scenario count
      unchanged.

### 2.5 · Stage-1 signal

- [ ] [AI] **Record the Stage-1 signal**, exact literal shape from
      [tech-docs §Stage-signal contract](./tech-docs.md#stage-signal-contract-the-plan-07-handoff-stage-granularity),
      each field anchored at column 0, outside any table/bullet/blockquote:

```
STAGE: 1
PLAN: ayokoding-learning-path-06-skills-accounting
LANDED_COURSE_IDS: accounting-foundations, chart-of-accounts-and-data-modeling, financial-statements-and-close-cycle
UNBLOCKS_ERP_CAPABILITY: the ERP stage delivering subledger-to-GL posting and record-to-report capability (the hard edge)
MERGED_COMMIT: <40-character SHA — fill in from the actual merge>
```

— acceptance: `git cat-file -e <sha>^{commit}` exits 0 once the real SHA is recorded, AND
`grep -c '^STAGE: 1$' delivery.md` returns **1** (the fenced block above must stay at column 0 —
indenting it under the bullet silently breaks the Phase 8 gate).

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [ ] [AI] All 3 Stage-1 course bodies exist, checkers green.
- [ ] [AI] Both manifests published, byte-identical at 3 entries, both pass `test:unit`.
- [ ] [AI] Both landings published, ordering check clean, checkers green.
- [ ] [AI] Both e2e walk specs green.
- [ ] [AI] Stage-1 signal recorded with a real, verifiable `MERGED_COMMIT`.
- [ ] [AI] `nx run ayokoding-www:build` exits 0.
- [ ] [AI] **The first ramp boundary is reachable in exactly three courses** — the composite claim
      that §2.2 (both manifests at 3), §2.3 (both landings state the Dangerous-1 boundary) and §2.4
      (the 3-course walk) jointly establish — acceptance: both `courseOrder`s hold exactly 3 entries,
      AND `grep -F -q 'Dangerous 1'` exits 0 against **both** landings, AND
      `nx run ayokoding-www-fe-e2e:test:e2e` exits 0. Negative control: a landing missing its
      not-yet-safe list fails the `Dangerous 1` check, so confirm each landing names what the reader
      **cannot** yet do, not merely the boundary label.

  **Gherkin (binds) →** "The first ramp boundary is reachable in three courses"

  ```gherkin
  Scenario: The first ramp boundary is reachable in three courses
    Given both accounting manifests are published with courses 1 through 3 in courseOrder
    When a reader finishes the third course
    Then the reader can build a correctly balancing ledger and produce the three statements for a single entity
    And both landings state that the reader cannot yet safely handle revenue recognition, inventory costing, multi-currency translation, leases, or consolidation
  ```

> **Pause Safety**: both paths have a working, correctly balancing three-course ledger and a live
> landing. Safe to stop — this is a genuinely shippable, if minimal, state. To resume: re-run
> `nx run ayokoding-www:test:unit && nx run ayokoding-www-fe-e2e:test:e2e` and confirm 0 exit before
> starting Phase 3.

---

## Phase 3: Stage 2 — courses #4–#19 and manifest growth to nineteen

> _Suggested executor: `apps-ayokoding-www-by-example-maker` / `apps-ayokoding-www-annotated-concept-maker`
> (per course's Format column) + `web-researcher` (accuracy pre-verify)._
>
> **The largest phase: sixteen courses, both manifests grown to nineteen, and `conventional-accounting`
> reaches its terminal state.** Apply the same seven-step convention from §2.1 to each course below;
> each is its own branch/PR/3-cycle-review/merge, pipelined up to the concurrency cap.

### 3.1 · Author the sixteen Stage-2 bodies

- [ ] [AI] Course #4 `journal-entries-and-posting-mechanics` (By Example; prerequisite: #3) — **first
      course carrying the formal silent-failure section (DD-609)** — acceptance: 7 steps complete;
      `grep -F -q 'What still balances while being wrong' "${COURSES}journal-entries-and-posting-mechanics/overview.md"`
      exits 0.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Course #5 `accrual-accounting-and-revenue-recognition` (By Example; prerequisite: #4) —
      acceptance: 7 steps complete; silent-failure section present.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Course #6 `accounts-payable-and-procure-to-pay` (By Example; prerequisite: #4) —
      acceptance: 7 steps complete; silent-failure section present.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Course #7 `accounts-receivable-and-order-to-cash` (By Example; prerequisites: #4, #5) —
      acceptance: 7 steps complete; silent-failure section present.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Course #8 `managerial-and-cost-accounting` (By Example; prerequisite: #3) — acceptance: 7
      steps complete; silent-failure section present.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Course #9 `fixed-assets-and-depreciation` (By Example; prerequisite: #2) — acceptance: 7
      steps complete; silent-failure section present.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Course #10 `inventory-and-cogs-accounting` (By Example; prerequisites: #2, #8) —
      acceptance: 7 steps complete; silent-failure section present.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Course #11 `lease-and-intangible-asset-accounting` (By Example; prerequisite: #9) — the
      corpus's headline "misclassified lease" example — acceptance: 7 steps complete; silent-failure
      section present.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Course #12 `multi-currency-accounting-and-fx-translation` (By Example; prerequisite: #3) —
      **NEW (A9)** — acceptance: 7 steps complete; silent-failure section present.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Course #13 `consolidation-and-multi-entity-accounting` (By Example; prerequisites: #2, #3,
      #12) — acceptance: 7 steps complete; silent-failure section present.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Course #14 `financial-reporting-standards-ifrs-vs-gaap` (Annotated-concept; prerequisites:
      #5, #11) — acceptance: 7 steps complete (adapted for Annotated-concept: themed grouping, no
      Beginner/Intermediate/Advanced bands); silent-failure section present.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] Course #15 `audit-controls-and-compliance` (Annotated-concept; prerequisite: #3) —
      acceptance: 7 steps complete; silent-failure section present.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] Course #16 `payroll-and-tax-accounting-essentials` (By Example; prerequisite: #2) —
      acceptance: 7 steps complete; silent-failure section present.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Course #17 `treasury-and-cash-management` (By Example; prerequisites: #6, #7) —
      acceptance: 7 steps complete; silent-failure section present.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Course #18 `financial-reporting-and-xbrl` (Annotated-concept; prerequisite: #14) —
      acceptance: 7 steps complete; silent-failure section present.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] Course #19 `general-ledger-system-architecture` (By Example; prerequisites: #2, #3, and the
      **linked** `backend-essentials`) — replaces the deleted
      `capstone-build-a-general-ledger-system` (A6/DD-607); carries the `DD-15` reference-implementation
      licensing note — acceptance: 7 steps complete; silent-failure section present;
      `grep -F -q 'backend-essentials' "${COURSES}general-ledger-system-architecture/_index.md"` exits
      0 (linked edge declared) **and**
      `grep -F -q 'backend-essentials' "${COURSES}general-ledger-system-architecture/overview.md"`
      exits 0 (scope boundary stated); **and no `learning/capstone/` directory exists**:
      `test -d "${COURSES}general-ledger-system-architecture/learning/capstone" && echo VIOLATION || echo OK`
      prints `OK`.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] **Stage-2 body check** —
      `for c in "${ACCT_S2[@]}"; do test -d "${COURSES}$c" || echo "MISSING $c"; done | wc -l`
      — acceptance: returns **0** (returns **16** before this sub-phase).
- [ ] [AI] Append all sixteen catalog rows to `"${COURSES}_index.md"` — acceptance:
      `for c in "${ACCT_S2[@]}"; do grep -F -q "$c" "${COURSES}_index.md" || echo "MISSING $c"; done | wc -l`
      returns **0**.

**Gherkin (binds) →** Outline "A manifest links its software-engineering prerequisites instead of
walking them" (Examples: `conventional-accounting`, `sharia-accounting`) — both `sql-essentials` (#2)
and `backend-essentials` (#19) are shared courses landing by end of this phase, so this is the
earliest point both Examples rows fully hold for both manifests.

```gherkin
Scenario Outline: A manifest links its software-engineering prerequisites instead of walking them
  Given the <path> path manifest is published with the full shared spine
  When a reader inspects its courseOrder
  Then neither sql-essentials nor backend-essentials appears in courseOrder
  And the chart-of-accounts course declares sql-essentials in its prerequisites frontmatter
  And the general-ledger-system-architecture course declares backend-essentials in its prerequisites frontmatter
  And the landing links both prerequisite courses at their canonical /en/learn/courses/ URLs

  Examples:
    | path                    |
    | conventional-accounting |
    | sharia-accounting       |
```

- [ ] [AI] **Link-don't-walk check, both manifests** —
      `for M in "$MANIFEST_CA" "$MANIFEST_SA"; do grep -oE 'sql-essentials|backend-essentials' "$M" | wc -l; done`
      returns **0 0**.

### 3.2 · TDD cycle — grow BOTH manifests to nineteen

- [ ] [AI] **RED** — extend `$MTEST_CA` and `$MTEST_SA` with failing assertions that each
      `courseOrder` grows from length 3 to length 19, appending `ACCT_S2` in order, still passing
      `checkManifestIntegrity` + `checkPrerequisiteConsistency` — command:
      `nx run ayokoding-www:test:unit` — acceptance: both new assertions fail (length still 3).

  **Gherkin (binds) →** "The conventional-accounting manifest completes and the Sharia-accounting
  manifest continues past it" — the `conventional-accounting`-terminal half of this scenario is
  provable here; the `sharia-accounting`-continues half is not provable until Phase 5, so this step
  records the first half and Phase 5 §5.2 completes the assertion.

  ```gherkin
  Scenario: The conventional-accounting manifest completes and the Sharia-accounting manifest continues past it
    Given both manifests have grown to include the full nineteen-course shared spine
    When a reader reaches the end of the conventional-accounting courseOrder
    Then the path landing states the path is complete
    And no further course is appended to conventional-accounting.yaml at any later phase
    But the sharia-accounting manifest's courseOrder continues past entry nineteen with five further ids
  ```

- [ ] [AI] **GREEN** — grow `$MANIFEST_CA` and `$MANIFEST_SA` to 19 entries each (both hold exactly
      `ACCT_SHARED` in order, still byte-identical to each other) — command:
      `nx run ayokoding-www:test:unit` — acceptance: exits 0; both files have exactly 19 `courseOrder`
      entries; `diff <(grep -E '^  - ' "$MANIFEST_CA") <(grep -E '^  - ' "$MANIFEST_SA")` returns empty
      (still fully identical — `$MANIFEST_SA`'s divergence does not begin until Phase 5).
- [ ] [AI] **REFACTOR** — command: `nx run ayokoding-www:test:unit && nx run ayokoding-www:lint` —
      acceptance: both exit 0.

### 3.3 · `conventional-accounting` reaches its terminal state — a genuine milestone

- [ ] [AI] Update `"${LANDING_CA}_index.md"` to state the path is **complete** at nineteen courses (no
      further growth is coming) — acceptance:
      `grep -F -q 'complete' "${LANDING_CA}_index.md"` exits 0.
- [ ] [AI] **Freeze check** — record, in this file, that `conventional-accounting.yaml` will receive no
      further `courseOrder` growth after this point; the only future touches to `$MANIFEST_CA` are
      Phase 6's re-verification sweeps, never a content change.
- [ ] [AI] Run `apps-ayokoding-www-link-checker` and `apps-ayokoding-www-general-checker` over the
      updated `$LANDING_CA` landing — apply fixers — acceptance: zero CRITICAL/HIGH/MEDIUM remain.

### 3.4 · Shared-spine non-duplication re-check

- [ ] [AI] `for c in "${ACCT_SHARED[@]}"; do n=$(find "${COURSES}$c" -maxdepth 0 -type d | wc -l); [ "$n" -eq 1 ] || echo "DUPLICATE-OR-MISSING $c"; done | wc -l`
      returns **0** (19 courses checked, extends §2.2's 3-course check to the full shared spine).

### 3.5 · TDD cycle — extend both path-walks to the full nineteen-course spine

> This phase is where `conventional-accounting` becomes production-serving, so this is where the
> delivered surface must be walked end to end. The walk cannot live in Phase 5: Phase 3's own Pause
> Safety note permits stopping here indefinitely, which would ship 19 courses having walked 3.

- [ ] [AI] **RED** — extend the reusable "walk a skills path given a path id" helper (from §2.4's
      REFACTOR) in `apps/ayokoding-www-fe-e2e/src/steps/skills-path-composition.steps.ts` so both
      `pathId`s walk all **19** published courses via prev/next, asserting `?path=` persistence and
      breadcrumb resolution at every step — command: `nx run ayokoding-www-fe-e2e:test:e2e` —
      acceptance: the new 19-course assertion **fails** for both Examples rows (only 3 courses were
      walked before this phase).

  **Gherkin (binds) →** Outline "A two-segment skills path ID resolves end to end" — the same Outline
  §2.4 bound, now exercised against the full nineteen-course shared spine

  ```gherkin
  Scenario Outline: A two-segment skills path ID resolves end to end
    Given the manifest declares pathId <path_id> and arc immediately-effective
    When a reader walks the path from its landing
    Then the landing, the prev and next controls, and the breadcrumb all resolve against the two-segment path ID
    And the ?path=<path_id> context persists across every course in the walk
    And no resolver assumes a three-segment path ID

    Examples:
      | path_id                       |
      | skills/conventional-accounting |
      | skills/sharia-accounting       |
  ```

- [ ] [AI] **GREEN** — implement against both grown manifests — command:
      `nx run ayokoding-www:specs:behavior:coverage && nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: both exit 0.
- [ ] [AI] **REFACTOR** — parameterize the walk on expected course count so Phase 5 extends it to 24
      without duplicating the helper — command: `nx run ayokoding-www-fe-e2e:test:e2e` — acceptance:
      exits 0, scenario count unchanged.

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [ ] [AI] All 16 Stage-2 course bodies exist, checkers green, every one carries a silent-failure
      section.
- [ ] [AI] **Both path-walk e2e specs walk all 19 courses, not 3** — command:
      `nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: exits 0. Negative control: this gate must
      fail if the helper is left at its §2.4 3-course bound, so confirm the walk asserts a
      19-course length for both `pathId`s before ticking.
- [ ] [AI] Both manifests grown to 19, still byte-identical, both pass `test:unit`.
- [ ] [AI] `conventional-accounting` landing states completeness.
- [ ] [AI] Both `sql-essentials` and `backend-essentials` link-don't-walk checks hold on both
      manifests.
- [ ] [AI] `nx run ayokoding-www:build` exits 0.

> **Pause Safety**: `conventional-accounting` is a genuinely complete, shippable 19-course path,
> **walked end to end by §3.5's e2e**; `sharia-accounting` is at the same 19-course state, one stage
> short of its own completion. Safe to stop indefinitely at this exact point if Stage 3 authoring is
> deferred — the pause is only safe because the delivered 19-course surface has been walked here
> rather than in a later phase this note permits skipping. To resume: re-run
> `nx run ayokoding-www:test:unit` and confirm 0 exit before starting Phase 4.

---

## Phase 4: Resolve the carried verification debt (OI-1, OI-2, OI-3)

> _Suggested executor: `web-researcher` (delegated, isolated context) for any residual re-verification;
> direct authoring for recording results._
>
> This phase gates **only** the Sharia stage (#20–#24) — `conventional-accounting` is already complete
> and unaffected by anything in this phase.

- [ ] [AI] Re-confirm `OI-1`'s residual (exact PPSAK ratification date) is either resolved via a fresh
      `web-researcher` fetch or explicitly left as "cite the series only" — acceptance:
      `verification-log.md`'s `OI-1` line states its residual explicitly, not silently.
- [ ] [AI] **`OI-2` gate check — must remain `OPEN`.** This phase does **not** attempt to resolve the
      riba doctrinal basis; it confirms the corpus's Stage-3 courses (already authored in Phase 1's
      syllabi) correctly state the practical consequence without overclaiming resolution — acceptance:
      `grep -c '^OI-2: OPEN$' "${PLANDIR}verification-log.md"` returns **1**, unchanged from Phase 0.
      **This check failing (a line reading `OI-2: RESOLVED`) is a blocking regression, not a pass.**
- [ ] [AI] Re-confirm `OI-3`'s residual (Bank Negara Malaysia's internal Shariah governance provisions,
      beyond the adoption-relationship claim already resolved) — either fetched and recorded, or
      explicitly left standing — acceptance: `verification-log.md`'s `OI-3` line states its residual.
- [ ] [AI] `OI-4` — confirm it remains routed/open per its existing record; this phase does not close
      it either — acceptance: `grep -c '^OI-4: OPEN$' "${PLANDIR}verification-log.md"` returns **1**.

### Phase 4 Gate

> All checks below must pass before starting Phase 5.

- [ ] [AI] `OI-1` residual explicitly stated.
- [ ] [AI] `OI-2` remains `OPEN` — verified, not merely assumed.
- [ ] [AI] `OI-3` residual explicitly stated.
- [ ] [AI] `OI-4` remains `OPEN`.
- [ ] [AI] **No retired `[Needs Verification]` placeholder remains, and the corpus's verification
      labelling is genuine (not merely unmarked).** An exhaustive grounding pass (2026-07-22) already
      resolved every placeholder in this corpus to `[Verified]`, `[Web-cited]`, or an
      honestly-retained `[Unverified]` tag — before Phase 1 even begins. Run the two commands in the
      fenced block below. Acceptance: the first returns **0** (no retired placeholder survives) AND
      the second returns a count **> 0** (the corpus carries genuine verification labelling, not
      silence). **Zero on command (1) is the correct target state here, not a vacuous pass** —
      command (2)'s non-zero count is the anti-vacuity proof that the corpus was substantively
      reviewed and tagged, rather than simply never labelled. Negative control: a corpus that never
      labelled anything would also make command (1) return 0, but command (2) would then return 0
      too — that (0, 0) combination is the void-check signal this gate watches for, not (0, >0).

  > **Historical note — do not re-derive stale expectations from earlier plan drafts.** Earlier
  > authoring-time snapshots of this note cited placeholder counts of 14/16 (later 15/17) across two
  > named files (`sharia-accounting-and-aaoifi-standards.md`,
  > `sharia-ledger-system-architecture.md`), describing an in-progress corpus mid-authoring. The
  > corpus has since been exhaustively resolved: a repo-wide `grep` across all 24
  > `syllabus/courses/*.md` files (excluding `README.md`) confirms **0** files carry
  > `[Needs Verification]`, while **48** `[Verified...]`, **18** `[Web-cited...]`, and **4**
  > `[Unverified...]` tagged claims remain — see `verification-log.md`'s `## Carried residuals`
  > section for the full breakdown and the four files that legitimately retain `[Unverified]`.
  > Re-measure rather than trusting any of these numbers, including this note's own — they are a
  > snapshot, and the whole point of the commands below is that they are cheap to re-run.

```bash
# (1) Syllabus files (excluding README.md) still carrying the retired [Needs Verification]
# placeholder. MUST print 0 — every course file was resolved during the grounding pass.
find "${SPEC}" -maxdepth 1 -name '*.md' ! -name 'README.md' -print0 \
  | xargs -0 grep -l '\[Needs Verification\]' 2>/dev/null | wc -l

# (2) Anti-vacuity companion: total genuine verification-labelling activity across the corpus
# ([Verified] + [Web-cited] + [Unverified] tags). MUST be > 0 (currently 70) — proves command (1)
# returning 0 reflects a resolved corpus, not an unmarked one.
find "${SPEC}" -maxdepth 1 -name '*.md' ! -name 'README.md' -print0 \
  | xargs -0 grep -oh '\[Verified\|\[Web-cited\|\[Unverified' 2>/dev/null | wc -l
```

> **Pause Safety**: the verification ledger is current and every open item's status is deliberate, not
> stale. Safe to stop. To resume: `grep -E '^OI-[1-4]: ' "${PLANDIR}verification-log.md"` and confirm
> the four lines match this gate's expectations before starting Phase 5.

---

## Phase 5: Stage 3 — courses #20–#24 and `sharia-accounting` growth to twenty-four

> _Suggested executor: `apps-ayokoding-www-by-example-maker` / `apps-ayokoding-www-annotated-concept-maker` /
> `web-researcher`._
>
> **Only `sharia-accounting.yaml` grows here — `conventional-accounting.yaml` is not touched.**

### 5.1 · Author the five Stage-3 bodies

- [ ] [AI] Course #20 `sharia-accounting-and-aaoifi-standards` (Annotated-concept; prerequisites: #5,
      #14) — presents the **three-jurisdiction landscape**; states `OI-2` as `OPEN` in its own body,
      never as resolved — acceptance: 7 steps complete;
      `grep -c 'OPEN' "${COURSES}sharia-accounting-and-aaoifi-standards/overview.md"` returns ≥ 1.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_

  **Gherkin (binds) →** "The Sharia stage presents three jurisdictional models"

  ```gherkin
  Scenario: The Sharia stage presents three jurisdictional models
    Given course #20 sharia-accounting-and-aaoifi-standards is published
    When a reader completes the course
    Then Indonesia's, Malaysia's, and the GCC's distinct relationships to AAOIFI are each named
    And no single jurisdiction's practice is presented as a universal rule
    And the riba doctrinal basis is stated as an open question, not settled fact
  ```

- [ ] [AI] Course #21 `islamic-contract-modeling-for-systems` (By Example; prerequisites: #20, #2) —
      acceptance: 7 steps complete; silent-failure section present.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

  **Gherkin (binds) →** "A murabaha is modelled as a trade rather than as a loan"

  ```gherkin
  Scenario: A murabaha is modelled as a trade rather than as a loan
    Given course #21 islamic-contract-modeling-for-systems is published
    When a reader compares the murabaha worked example against a conventional loan
    Then the murabaha is recorded as an asset purchase followed by a resale at a disclosed markup
    And the markup is recognised as deferred trade profit, never as interest income
    And the course names the asset-risk-transfer test that distinguishes a genuine murabaha from a disguised loan
  ```

- [ ] [AI] Course #22 `zakah-computation-and-reporting-for-systems` (By Example; prerequisite: #21) —
      **NEW (A9)** — acceptance: 7 steps complete; silent-failure section present.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

  **Gherkin (binds) →** "Zakah is computed and reported as its own obligation, not folded into tax"

  ```gherkin
  Scenario: Zakah is computed and reported as its own obligation, not folded into tax
    Given course #22 zakah-computation-and-reporting-for-systems is published
    When a reader computes both a tax liability and a Zakah liability for the same entity and period
    Then the Zakah liability is reported as its own disclosure or fund
    And it is never merged into or reported as a line item within the tax-expense account
    And the course names the observable signal that would reveal a folded-in Zakah figure
  ```

- [ ] [AI] Course #23 `sukuk-and-islamic-capital-markets-accounting` (Annotated-concept;
      prerequisites: #21, #12) — **NEW (A9)** — acceptance: 7 steps complete; silent-failure section
      present.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] Course #24 `sharia-ledger-system-architecture` (By Example; prerequisites: #21, #19) —
      replaces the deleted `capstone-sharia-compliant-ledger` (A6/DD-607); no separate linked SWE edge
      (inherited through #19) — acceptance: 7 steps complete; silent-failure section present; **and no
      `learning/capstone/` directory exists**:
      `test -d "${COURSES}sharia-ledger-system-architecture/learning/capstone" && echo VIOLATION || echo OK`
      prints `OK`.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] **Stage-3 body check** —
      `for c in "${ACCT_S3[@]}"; do test -d "${COURSES}$c" || echo "MISSING $c"; done | wc -l`
      — acceptance: returns **0** (returns **5** before this sub-phase).
- [ ] [AI] Append all five catalog rows to `"${COURSES}_index.md"` — acceptance:
      `for c in "${ACCT_S3[@]}"; do grep -F -q "$c" "${COURSES}_index.md" || echo "MISSING $c"; done | wc -l`
      returns **0**.

### 5.2 · TDD cycle — grow `sharia-accounting` ONLY, to twenty-four

- [ ] [AI] **RED** — extend `$MTEST_SA` **only** (never `$MTEST_CA`) with a failing assertion that
      `courseOrder` grows from 19 to 24, appending `ACCT_S3` in order, still passing both integrity
      checks — command: `nx run ayokoding-www:test:unit` — acceptance: fails (length still 19).

  **Gherkin (binds) →** "The conventional-accounting manifest completes and the Sharia-accounting
  manifest continues past it" — second half, completing Phase 3's first-half assertion.

  ```gherkin
  Scenario: The conventional-accounting manifest completes and the Sharia-accounting manifest continues past it
    Given both manifests have grown to include the full nineteen-course shared spine
    When a reader reaches the end of the conventional-accounting courseOrder
    Then the path landing states the path is complete
    And no further course is appended to conventional-accounting.yaml at any later phase
    But the sharia-accounting manifest's courseOrder continues past entry nineteen with five further ids
  ```

- [ ] [AI] **GREEN** — grow `$MANIFEST_SA` to 24 entries (19 shared + 5 Sharia-specific, in order) —
      command: `nx run ayokoding-www:test:unit` — acceptance: exits 0; `$MANIFEST_SA` has exactly 24
      `courseOrder` entries; `$MANIFEST_CA` **unchanged** —
      `git diff --quiet -- "$MANIFEST_CA"` **exits 0** (no diff at all since Phase 3's freeze). Exit
      code, not output — immune to any diff-rendering filter. Negative control: touching one line of
      `$MANIFEST_CA` makes it exit 1.
- [ ] [AI] **REFACTOR** — command: `nx run ayokoding-www:test:unit && nx run ayokoding-www:lint` —
      acceptance: both exit 0.

- [ ] [AI] **Completion-and-continuation assertion, both halves together**:
      `grep -cE '^  - ' "$MANIFEST_CA"` returns **19**, AND `grep -cE '^  - ' "$MANIFEST_SA"` returns
      **24**, AND `git diff --quiet origin/main -- "$MANIFEST_CA"` (measured from the Phase 3 merge
      point to now) **exits 0** — falsifiable both ways: any further edit to `$MANIFEST_CA` after
      Phase 3 makes the last check exit 1.

### 5.3 · Update the `sharia-accounting` landing to reflect all three stages

- [ ] [AI] Extend `"${LANDING_SA}_index.md"` with the Dangerous-2 and Dangerous-3 boundaries and the
      full 24-course ramp — acceptance:
      `for t in 'Dangerous 2' 'Dangerous 3'; do grep -F -q "$t" "${LANDING_SA}_index.md" || echo "MISSING $t"; done | wc -l`
      returns **0**.
- [ ] [AI] Run `apps-ayokoding-www-link-checker` and `apps-ayokoding-www-general-checker` — apply
      fixers — acceptance: zero CRITICAL/HIGH/MEDIUM remain.

### 5.4 · TDD cycle — extend the `sharia-accounting` path-walk e2e

- [ ] [AI] **RED** — extend the count-parameterized "walk a skills path" step (from §3.5's REFACTOR)
      with a 24-course walk for `skills/sharia-accounting`, plus an assertion that the
      `skills/conventional-accounting` walk is still exactly 19 courses (unaffected by this phase) —
      command:
      `nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: the new 24-course assertion fails (only 19
      published before this phase).

  **Gherkin (binds) →** Outline "A two-segment skills path ID resolves end to end" — same Outline
  §2.4 bound, now exercised against `sharia-accounting`'s full 24-course growth

  ```gherkin
  Scenario Outline: A two-segment skills path ID resolves end to end
    Given the manifest declares pathId <path_id> and arc immediately-effective
    When a reader walks the path from its landing
    Then the landing, the prev and next controls, and the breadcrumb all resolve against the two-segment path ID
    And the ?path=<path_id> context persists across every course in the walk
    And no resolver assumes a three-segment path ID

    Examples:
      | path_id                       |
      | skills/conventional-accounting |
      | skills/sharia-accounting       |
  ```

- [ ] [AI] **GREEN** — command: `nx run ayokoding-www:specs:behavior:coverage && nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: both exit 0.
- [ ] [AI] **REFACTOR** — command: `nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: exits 0,
      scenario count unchanged.

### 5.5 · Full-corpus silent-failure and Zakah/tax separation checks

- [ ] [AI] `for c in "${ACCT_SILENT[@]}"; do grep -q 'silent-failure\|What still balances while being wrong' "${COURSES}$c/overview.md" || echo "MISSING $c"; done | wc -l`
      returns **0** (all 21 checked, corpus-wide, both stages).

**Gherkin (binds) →** "Every post-foundations course names what still balances while being wrong"

```gherkin
Scenario: Every post-foundations course names what still balances while being wrong
  Given every course from #4 through #24 is published
  When a reader completes any one of those twenty-one courses
  Then the course states at least one outcome that remains internally consistent while being substantively wrong
  And it names the observable signal, if any, that would reveal the error
```

### Stage-3 signal

- [ ] [AI] **Record the Stage-3 signal**, exact literal shape:

```
STAGE: 3
PLAN: ayokoding-learning-path-06-skills-accounting
LANDED_COURSE_IDS: sharia-accounting-and-aaoifi-standards, islamic-contract-modeling-for-systems, zakah-computation-and-reporting-for-systems, sukuk-and-islamic-capital-markets-accounting, sharia-ledger-system-architecture
UNBLOCKS_ERP_CAPABILITY: the ERP stages delivering Sharia-compliant ERP capability and founding-architecture capability
MERGED_COMMIT: <40-character SHA — fill in from the actual merge>
```

— acceptance: `git cat-file -e <sha>^{commit}` exits 0, AND `grep -c '^STAGE: 3$' delivery.md`
returns **1** (the fenced block above must stay at column 0 — indenting it under the bullet silently
breaks the Phase 8 gate).

### Phase 5 Gate

> All checks below must pass before starting Phase 6.

- [ ] [AI] All 5 Stage-3 course bodies exist, checkers green, every one carries a silent-failure
      section.
- [ ] [AI] `sharia-accounting.yaml` grown to 24; `conventional-accounting.yaml` untouched since Phase 3.
- [ ] [AI] `sharia-accounting` landing reflects all three stages.
- [ ] [AI] Both e2e walk specs (19-course and 24-course) green.
- [ ] [AI] Stage-3 signal recorded with a real, verifiable `MERGED_COMMIT`.
- [ ] [AI] `nx run ayokoding-www:build` exits 0.

> **Pause Safety**: both paths are fully authored and independently shippable —
> `conventional-accounting` at 19, `sharia-accounting` at 24. Safe to stop. To resume:
> `nx run ayokoding-www:test:unit && nx run ayokoding-www-fe-e2e:test:e2e` and confirm 0 exit before
> starting Phase 6.

---

## Phase 6: Section and app verification

> _Suggested executor: direct verification; `apps-ayokoding-www-facts-checker` and
> `apps-ayokoding-www-link-checker` for the corpus-wide sweep._

### 6.1 · Manifest integrity, both manifests

- [ ] [AI] `nx run ayokoding-www:test:unit` (both `$MTEST_CA` and `$MTEST_SA`) exits 0.
- [ ] [AI] `checkManifestIntegrity` and `checkPrerequisiteConsistency` pass for both manifests as a
      standalone sweep, not only inside the unit-test run — command: re-run the same test target with
      `--verbose` and read the assertion count matches 24 (19 for CA, 24 for SA, no shared assertion
      double-counted incorrectly).

### 6.2 · Ownership footprint check (DD-615)

- [ ] [AI] Authorship-scoped commit-footprint check: `gh pr list --search "ayokoding-learning-path-06-skills-accounting" --state merged --json number,files` and confirm every touched path under `apps/ayokoding-www/src/features/course-paths/manifests/` is one of the two files this plan owns — acceptance: no path under `manifests/careers/`, `manifests/skills/conventional-erp.yaml`, or `manifests/skills/sharia-erp.yaml` appears; no `_index.md` under `paths/` (other than the two landings) appears.

### 6.3 · Shared-course non-duplication, final sweep

- [ ] [AI] `for c in "${ACCT_SHARED[@]}"; do n=$(find "${COURSES}$c" -maxdepth 0 -type d | wc -l); [ "$n" -eq 1 ] || echo "DUPLICATE-OR-MISSING $c"; done | wc -l`
      returns **0** (final confirmation, all 19).

### 6.4 · Licensing reading audit (A8 + A12)

> Covers **both** course bodies **and** syllabus artifacts — a clause limited to course bodies alone
> leaves the syllabus layer, which itself cites standards and reference implementations, unaudited.

- [ ] [AI] For every file in `"${SPEC}"` (24 syllabi) **and** every `overview.md` under
      `"${COURSES}"` for `ACCT_ALL` (24 course bodies) — 48 files total — read against the eleven
      safe-authoring rules in
      [tech-docs §Licensing and IP Compliance](./tech-docs.md#licensing-and-ip-compliance-a8): no
      standard's clause text or numbering layout reproduced, no chart of accounts copied, no copyleft
      code pasted, no vendor name used in a title. Cross-check against each file's own recorded
      licensing-sensitive-sources note (Phase 1 §1.4) — acceptance: zero violations found; any finding
      is fixed before this gate closes.
- [ ] [AI] **Every citation resolves to a full URL.** The corpus currently cites sources by bare
      domain or by unlinked source name (`## Read more` entries, and the grounding citations in
      `verification-log.md` and `tech-docs.md`). `A8`'s "describe, cite and link; never reproduce"
      posture depends on the **link** half: a reader sent to the source needs a resolvable address,
      and an unlinked name cannot be checked for licence terms.
      Add a full URL to every citation, then verify:

  ```bash
  # Excludes README.md (the folder's own index, not a course spec) from the iteration.
  for f in $(find "${SPEC}" -maxdepth 1 -name '*.md' ! -name 'README.md'); do
    awk '/^## Read more$/{flag=1;next}/^## /{flag=0}flag' "$f" \
      | grep -E '^\s*[-*] ' | grep -qv 'http' && echo "UNLINKED CITATION: $f"
  done
  ```

  Acceptance: **empty output**. Guard first —
  `[ "$(find "${SPEC}" -maxdepth 1 -name '*.md' ! -name 'README.md' | wc -l)" -eq 24 ] && echo GUARD-OK`
  must print `GUARD-OK` (the count excludes `syllabus/courses/README.md`; a naive
  `ls "${SPEC}"*.md | wc -l` would match the README too and return 25, never printing `GUARD-OK`).
  **Do not fabricate a URL to satisfy this clause.** Where a source is offline-only (a printed
  textbook, a paywalled standard), cite it nominatively and record it in that file's Accuracy notes as
  deliberately unlinked with the reason — that is a pass, not a violation. Where a URL is asserted,
  `apps-ayokoding-www-link-checker` must confirm it resolves; a dead or invented link fails this
  clause. `A4` markers on the underlying claims are unaffected — adding a link never upgrades an
  `[Unverified]` claim to `[Verified]`.

**Gherkin (binds) →** "No standard's text or proprietary structure is reproduced"

```gherkin
Scenario: No standard's text or proprietary structure is reproduced
  Given all twenty-four syllabi and all twenty-four course bodies are authored
  When each is read against the eleven safe-authoring rules
  Then no clause text, table, or numbering layout from any standard appears verbatim
  And no chart of accounts is copied from any textbook, standard, or reference implementation
  And every reference to a copyleft-licensed project is behavioural, never quoted code
  And no vendor or standards-body name appears in a course title, path segment, or endorsement-implying context
```

- [ ] [AI] Confirm no syllabus's `## Read more` section or course body reproduces a curriculum's module
      titles or sequence (A12) — verified by reading, not grep, per
      [tech-docs §Post-authoring verification](./tech-docs.md#syllabus-layer--custody-and-shape).

### 6.5 · Scope-boundary sweep — the corpus never re-teaches a linked library course

- [ ] [AI] Confirm neither manifest walks `sql-essentials` or `backend-essentials` into `courseOrder`
      (final sweep, extends §3.1's check) — `for M in "$MANIFEST_CA" "$MANIFEST_SA"; do grep -oE 'sql-essentials|backend-essentials' "$M" | wc -l; done` returns **0 0**.
- [ ] [AI] Confirm `#2` and `#19`'s overview files each state their scope boundary against the linked
      library course rather than re-teaching it — verified by reading (already checked mechanically in
      §2.1 and §3.1; this is the corpus-wide confirmation).

**Gherkin (binds) →** "The accounting corpus never re-teaches a linked library course"

```gherkin
Scenario: The accounting corpus never re-teaches a linked library course
  Given both manifests are fully published
  When a reader inspects sql-essentials and backend-essentials
  Then neither appears in either courseOrder
  And chart-of-accounts-and-data-modeling states it applies, not re-teaches, sql-essentials
  And general-ledger-system-architecture states it applies, not re-teaches, backend-essentials
```

### 6.6 · No-unverified-claim sweep

- [ ] [AI] `apps-ayokoding-www-facts-checker` run over all 24 course bodies and all 24 syllabi —
      acceptance: zero unmarked claims; every `[Unverified]` / `[Needs Verification]` claim is
      genuinely marked, not silently stated as fact.

**Gherkin (binds) →** "No unverified claim is published as fact"

```gherkin
Scenario: No unverified claim is published as fact
  Given the full twenty-four-course corpus is published
  When apps-ayokoding-www-facts-checker sweeps every course body and syllabus
  Then every claim not directly sourced from this plan's own grounding file carries a verification marker
  And OI-2's riba doctrinal basis is never restated as settled fact anywhere in the corpus
```

### Phase 6 Gate

> All checks below must pass before starting Phase 7.

- [ ] [AI] 6.1 through 6.6 all clean, zero unresolved findings.
- [ ] [AI] `nx run ayokoding-www:build` exits 0.
- [ ] [AI] `npm run lint:md` exits 0 across the whole plan folder and the whole `apps/ayokoding-www`
      content touched.

> **Pause Safety**: the corpus is verified, licensing-clean, and scope-consistent. Safe to stop. To
> resume: re-run 6.1's `test:unit` and 6.4's licensing sweep before starting Phase 7.

---

## Phase 7: Manual UI verification and Rule-15 three-tester retest

> _Suggested executor: Playwright MCP direct use; `web-exploratory-tester` /
> `web-usability-tester` / `web-design-tester` triad for the Rule-15 retest._

### Manual UI Verification (Playwright MCP) — three breakpoints

- [ ] [AI] Start dev server: `nx dev ayokoding-www`.
- [ ] [AI] For EACH breakpoint (375 / 768 / 1280 px): `browser_resize` to that width, then navigate to
      `/en/learn/paths/skills/conventional-accounting` via `browser_navigate`.
- [ ] [AI] Inspect DOM via `browser_snapshot` at every breakpoint — verify the arc promise, the
      completeness statement, and the rendered 19-course list all appear.
- [ ] [AI] For EACH breakpoint (375 / 768 / 1280 px): `browser_resize` to that width, then navigate to
      `/en/learn/paths/skills/sharia-accounting` — verify the arc promise, all three Dangerous-N
      boundaries, the path-choice note, and the rendered 24-course list.
- [ ] [AI] Walk both paths end to end via prev/next controls (`browser_click`) — verify breadcrumb and
      `?path=` persistence at every step.
- [ ] [AI] Check for JS errors via `browser_console_messages` on both landings and a sample of walked
      courses, at every breakpoint — zero errors.
- [ ] [AI] Take one screenshot per landing per breakpoint via `browser_take_screenshot`, saved to
      `evidence/phase-7-<landing>-en-<breakpoint>px.png` (e.g.
      `evidence/phase-7-conventional-accounting-en-375px.png`,
      `evidence/phase-7-sharia-accounting-en-1280px.png`) — commit as evidence.
- [ ] [AI] Document verification results in this checklist, referencing each committed screenshot.

### Rule-15 three-tester retest (both paths, both `pathId`s)

All three run in `delivery` mode so their findings land in this checklist rather than in a new backlog
plan. **Fold every finding in as its own checkbox**, prefixed with the issuing tester's id — `EWT-###`
(exploratory), `UWT-###` (usability), `DWT-###` (design) — so each is individually tickable and
auditable. A tester's summary verdict is not a substitute for the per-finding checkboxes.

- [ ] [AI] Dispatch `web-exploratory-tester` (**spec-aware** — it reads `specs/**` Gherkin and hunts
      functional/correctness defects) against both landings and a sample walk — record every finding
      as an `EWT-###` checkbox.
- [ ] [AI] Dispatch `web-usability-tester` (**spec-blind** — first-time-user comprehension, judged
      only on what the rendered page shows) against both landings — record every finding as a
      `UWT-###` checkbox.
- [ ] [AI] Dispatch `web-design-tester` (**design-aware**) against both landings — record every
      finding as a `DWT-###` checkbox.
- [ ] [AI] **Resolve every defect finding from the triad, at all severities** — not only CRITICAL and
      HIGH. Governance requires all defect findings fixed; a MEDIUM or LOW may be deferred **only**
      with explicit recorded permission naming the finding id and the reason. Re-run the affected
      tester(s) after fixing and confirm the finding no longer reproduces.

### Phase 7 Gate

> All checks below must pass before starting Phase 8.

- [ ] [AI] Both landings walked end to end with zero JS console errors.
- [ ] [AI] Screenshot evidence committed for both landings.
- [ ] [AI] Rule-15 triad complete for both paths; every `EWT-###`/`UWT-###`/`DWT-###` finding folded
      in as a checkbox and **resolved at every severity**, or explicitly deferred with a recorded
      permission naming the finding id and reason. Zero unresolved CRITICAL/HIGH is necessary but not
      sufficient.

> **Pause Safety**: both paths are manually verified end to end. Safe to stop. To resume: re-open both
> landings via `browser_navigate` and re-check `browser_console_messages` before starting Phase 8.

---

## Phase 8: Final origin main integration and CI verification

> _Suggested executor: direct git/CI operations._

### Local Quality Gates (Before Push)

- [ ] [AI] `nx affected -t typecheck,build,test:quick,lint` exits 0.
- [ ] [AI] `nx run ayokoding-www:specs:behavior:coverage` exits 0.
- [ ] [AI] `npm run lint:md` exits 0.

> **Important**: fix ALL failures found during these gates, not just those caused by this plan's own
> changes — proactively fix any preexisting error encountered, per the root-cause-orientation
> principle.

### Commit Guidelines

- [ ] [AI] Commit changes thematically — group related changes into logically cohesive commits.
- [ ] [AI] Follow Conventional Commits format: `<type>(<scope>): <description>`.
- [ ] [AI] Split different domains/concerns into separate commits (e.g. a syllabus-authoring commit
      separate from a manifest-growth commit).
- [ ] [AI] Do NOT bundle unrelated fixes into a single commit.

### Post-Push Verification

- [ ] [AI] Push the final integration branch, open the draft PR, run the 3-cycle
      fan-out → `pr-review-synthesis-maker` → `pr-review-fixer` review — acceptance: 0 CRITICAL + 0 HIGH outstanding, branch
      non-destructively up to date with `origin/main`, all quality gates green.
- [ ] [AI] Monitor GitHub Actions for this PR's check run — poll every 2 minutes, one
      `gh run view --json status,conclusion` per wakeup.
- [ ] [AI] Verify all CI checks pass; fix and push a follow-up commit for any failure.
- [ ] [AI] Confirm all five PR Merge Protocol preconditions hold (review cycles complete; 0
      CRITICAL/HIGH outstanding; branch current; gates green; tester gates run) — see
      [PR Merge Protocol](../../../repo-governance/development/workflow/pr-merge-protocol.md).
      **Do not merge here.** The PR stays open through Phases 9 and 10 so that Knowledge Capture and
      the archival move are committed to **this same branch** and land inside this PR, as the merge
      protocol requires. The `[AI]` merge is the terminal step of Phase 10.

**Gherkin (binds) →** "Both accounting paths build and validate green"

```gherkin
Scenario: Both accounting paths build and validate green
  Given both manifests, all twenty-four course bodies, and both landings are merged to origin/main
  When the full ayokoding-www CI suite runs
  Then build, typecheck, lint, test:quick, and specs:behavior:coverage all pass
  And both e2e path-walk specs pass
  And no CI check for this plan's changes fails
```

### Both stage-signal assertions, final confirmation

- [ ] [AI] `grep -c '^STAGE: 1$' "${PLANDIR}delivery.md"` returns **1**, AND
      `grep -c '^STAGE: 3$' "${PLANDIR}delivery.md"` returns **1** (Stage 2 carries no separate
      cross-plan signal — it is the `conventional-accounting`-completion milestone, recorded in §3.3,
      not a plan-07-facing signal), AND both `MERGED_COMMIT` values pass `git cat-file -e`.

### Phase 8 Gate

> All checks below must pass before starting Phase 9.
>
> **Two merge states coexist here, and the distinction is load-bearing.** Per
> [DD-613](./tech-docs.md#design-decisions), every **course and manifest** sub-phase already merged
> to `origin/main` on its own PR during Phases 2, 3 and 5 — so the corpus itself is live and CI-green
> by the time Phase 8 runs. What stays **open** is _this plan's own final PR_, carrying Knowledge
> Capture (Phase 9) and the archival move (Phase 10), which the merge protocol requires to land
> inside the same PR. "Do not merge here" refers to that final PR only; it does not contradict the
> corpus already being on `origin/main`.

- [ ] [AI] CI green on `origin/main` for this plan's **already-merged course and manifest changes**
      (the DD-613 per-course PRs) — verify against the run whose head SHA matches `origin/main`'s
      current tip, not merely "the latest run".
- [ ] [AI] Both stage signals present with real, verifiable commits.
- [ ] [AI] **Production serves both accounting paths.** Dispatch (or re-dispatch, if an earlier
      per-merge deploy lagged) `apps-ayokoding-www-deployer` to publish `ayokoding-www` to
      `prod-ayokoding-www` — acceptance: `https://ayokoding.com/en/learn/paths/skills/conventional-accounting`
      and `.../sharia-accounting` both return HTTP 200 and each renders its own `courseOrder` length
      (19 and 24 respectively). Negative control: a 404 on either landing, or a rendered course count
      that still matches a pre-merge value, means the deploy has not landed — that is a failure, not
      a pass.
- [ ] [AI] **This plan's final PR is still open**, containing Phases 8-10's commits —
      `gh pr list --head "$(git rev-parse --abbrev-ref HEAD)" --state open --json number --jq 'length'`
      returns **1**. Negative control: a value of **0** means the PR was merged early, which breaks
      the archival-inside-the-PR requirement and is a blocking regression, not a pass.

> **Pause Safety**: the authored corpus — both paths — is live on `origin/main` and CI-green, while
> this plan's final PR remains open by design. Safe to stop. To resume: confirm the `origin/main` run
> matching the current tip SHA is green, and that this plan's final PR is still open, before starting
> Phase 9.

---

## Phase 9: Knowledge Capture

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)._

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only if a durable surface would
      catch this automatically next time; discard the rest with a one-line reason.
- [ ] [AI] Apply the secret/sensitivity gate — sanitize any secret, credential, token, or private
      hostname, or discard if unsanitizable.
- [ ] [AI] Apply the repo-relevance gate — infra-private content stays in `ose-infra` only.
- [ ] [AI] Route each surviving learning to exactly one durable home; code-homed learnings are filed as
      a separate `plans/backlog/<slug>/` plan, never landed inline.
- [ ] [AI] If no generalizable learning surfaced, record `No generalizable learnings — <reason>` in
      `learnings.md`.

### Phase 9 Gate

> All checks below must pass before Plan Archival.

- [ ] [AI] Every `learnings.md` entry is terminal (routed / filed as backlog / discarded with reason),
      or the explicit "none" escape is recorded.
- [ ] [AI] No code-homed learning landed inline in this plan's own commits/PRs.

> **Pause Safety**: `learnings.md` is fully triaged. Safe to stop. To resume: re-read `learnings.md`
> and confirm every entry is terminal.

---

## Phase 10: Plan Archival

- [ ] [AI] `git mv plans/in-progress/ayokoding-learning-path-06-skills-accounting plans/done/$(date +%Y-%m-%d)__ayokoding-learning-path-06-skills-accounting`
      (or from `plans/backlog/…` if it was never promoted to `in-progress/`).
- [ ] [AI] Update `plans/in-progress/README.md` (or `plans/backlog/README.md` if it never promoted) —
      remove this plan's entry.
- [ ] [AI] Update `plans/done/README.md` — add this plan's entry with its completion date.
- [ ] [AI] Update `ayokoding-learning-path-07-skills-erp`'s own docs to note both stage signals are now
      available on `origin/main` for its independent `test -d` verification, per
      [tech-docs §Stage-signal contract](./tech-docs.md#stage-signal-contract-the-plan-07-handoff-stage-granularity) —
      this is a note only; plan 07 verifies readiness itself and never parses this file.
- [ ] [AI] Commit the archival move **to the still-open PR branch from Phase 8** — no dedicated
      follow-up archival PR. Phase 8 deliberately left the PR unmerged precisely so this commit lands
      inside it; the merge protocol requires archival committed in the PR **before** the merge, and a
      "same final PR" that has already merged cannot receive it.
      Commit with a Conventional Commits message, e.g.
      `git commit -m "chore(plans): archive ayokoding-learning-path-06-skills-accounting"`.
- [ ] [AI] **Push the archival commit** — `git push origin HEAD` — acceptance: exits 0 and
      `git status -sb` reports the branch is not ahead of its upstream:
      `git status -sb | grep -c 'ahead'` returns **0**. Committing without pushing would leave the
      archival move out of the PR entirely while every later check still appeared to pass.
- [ ] [AI] **Monitor CI on the new head** — poll every 2 minutes, one
      `gh run view --json status,conclusion` per wakeup, exactly as Phase 8 does. Never tight-loop and
      never use `gh run watch`; on a 403 rate-limit, wait ~35 minutes. Acceptance: `status` is
      `completed` **and** `conclusion` is `success` **for the run whose head SHA equals
      `git rev-parse HEAD`** — confirm the SHA matches rather than reading whichever run is newest, or
      a stale green run from before the archival commit will be mistaken for a pass.
- [ ] [AI] Re-confirm all five PR Merge Protocol preconditions still hold after the archival commit
      (the branch changed, so review state and CI must both be re-checked on the new head), then
      perform the `[AI]` merge. This is the terminal step of the plan.

### Phase 10 Gate

- [ ] [AI] `test -d plans/done/*__ayokoding-learning-path-06-skills-accounting` exits 0.
- [ ] [AI] `test -d plans/backlog/ayokoding-learning-path-06-skills-accounting` and
      `test -d plans/in-progress/ayokoding-learning-path-06-skills-accounting` both exit 1.
- [ ] [AI] The archival commit is an ancestor of the merged PR head — verify the archival landed
      inside the PR rather than in a follow-up:
      `gh pr list --head "$(git rev-parse --abbrev-ref HEAD)" --state merged --json number,mergeCommit`
      returns this plan's PR. Use `gh pr list --head`, not `git merge-base --is-ancestor`: this repo
      squash-merges, so ancestry checks false-negative on every merged PR.

> **Pause Safety**: plan complete and archived. Nothing further to resume.
