# Delivery Checklist — Skills Paths: Accounting Enterprise Reporting & Architecture

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`). `[HUMAN]`:
> only a human can do it (physical action, out-of-band approval, real-secret or privileged-credential
> handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate`: a must-pass verification checklist plus
> a **Pause Safety** note. A phase is **not complete until its gate is green**; do not start phase N+1
> while any check in phase N's gate is failing.

## One-PR delivery contract (binding, 2026-08-01)

This 8-course plan is one inseparable delivery unit: every Phase 1–7 change lands in **one
worktree, one branch, and exactly one draft PR**. Courses may still be authored, checked, and
committed in their dependency order, but no intermediate phase may push, open a PR, run the PR
merge, deploy, or record a merge SHA. Only Phase 7 opens the draft PR, after all
course work, verification, and Knowledge Capture are green; it includes the archival move to
`plans/done/`, then runs the secret scan, local quality checks, and PR quality-gate verification, CI verification, ready-for-review
transition, and the normal `[AI]` merge/deploy protocol. No earlier stage or delivery boundary opens
a PR.

The `worktrees/ayokoding-learning-path-15-skills-accounting-enterprise-reporting/` path below is
this plan's only worktree; no per-course, stage, phase, or closeout worktree is created.

## Worktree

Worktree path: `worktrees/ayokoding-learning-path-15-skills-accounting-enterprise-reporting/`

Provision this path exactly once with `claude --worktree ayokoding-learning-path-15-skills-accounting-enterprise-reporting` (or `git worktree add -b worktree/ayokoding-learning-path-15-skills-accounting-enterprise-reporting worktrees/ayokoding-learning-path-15-skills-accounting-enterprise-reporting origin/main` when provisioning manually). Both forms designate the same one worktree; never create a second path for a phase, course, or closeout.

Final-delivery branch: `ayokoding-learning-path-15-skills-accounting-enterprise-reporting/final-delivery`

This path is the one and only worktree for the entire plan. Provision it once from current
`origin/main`, create the persistent `final-delivery` branch after Phase 0, and use neither
per-course/cohort/stage worktrees nor per-phase branches. Remove it only after the final PR merges.

> **Worktree Cap conformance note (added when the rule landed):** this plan already declared a
> single, plan-wide worktree before the
> [Worktree Cap](../../../repo-governance/conventions/structure/plans/worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule)
> and
> [Per-Repository Delivery Mode Restrictions](../../../repo-governance/conventions/structure/plans/per-repository-delivery-mode-restrictions.md#per-repository-delivery-mode-restrictions-hard-rule)
> rules landed. Reviewed against both — already compliant, no change required.

## Delivery Mode: worktree-to-pr

**CI scope note**: "CI green"/"CI gates" below mean the PR's own check run
(`pr-quality-gate.yml`) — never `.github/workflows/main-ci.yml`, which is deprecated,
schedule-only, and must not be monitored or gated on.

This plan has one delivery unit: all change-producing work is committed on the persistent
`final-delivery` branch in the declared worktree. Phases before 7 must not push, open
a PR, start an external merge, deploy, or record an in-repository merge SHA. Phase 7 first
commits the archival move and index updates, then opens the sole draft PR, runs the secret scan, local quality checks, and PR quality-gate verification plus local and CI gates, marks it ready, merges under the hardened
preconditions, and deploys once.

## Content-only delivery safeguards

This plan produces content only and has exactly one final PR. It has no review-cycle requirement. Before pushing that PR:

- [x] [AI] Inspect the staged diff and confirm it contains no machine-secret value.
- [x] [AI] Use a scoped Conventional Commit (for example, `docs(plans): refresh course-preparation backlog`).
- [x] [AI] Run `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`; acceptance: exits 0 for the affected scope.
- [x] [AI] Push the single branch, then wait for `.github/workflows/pr-quality-gate.yml`; acceptance: the PR quality gate is green before merge.

## Depends-on

| Relation      | Plan (full folder name)                                    | Nature                                                                                                                                                                                                                         |
| ------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **blockedBy** | `ayokoding-learning-path-14-skills-accounting-foundations` | **Hard; sole direct execution prerequisite.** It must be fully merged and archived on `origin/main` before Phase 0. All earlier completion and repository-baseline facts are transitive context, not extra plan prerequisites. |

**Phase 0 start check:** `git ls-tree -r --name-only origin/main plans/done | rg -q "__ayokoding-learning-path-14-skills-accounting-foundations/README\.md$"` exits 0. This is this plan's only plan-level start gate.

## Parallelization Model

Courses #12, #15, #16 share only plan-14 prerequisites and can author in parallel with each other;
\#13 waits on #12; #14 waits on plan-14's #5/#11; #17 waits on plan-14's #6/#7; #18 waits on #14;
\#19 waits on plan-14's #2/#3. Both manifests' TDD growth cycle is one shared sub-phase.

### Delivery Boundaries

| Phase(s) | Delivery unit                                               | Worktree / branch                                                         | PR opens                           |
| -------- | ----------------------------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------- |
| 0        | Setup and baseline                                          | No delivery worktree or PR                                                | no                                 |
| 1–6      | Intermediate authoring, verification, and Knowledge Capture | This plan's single declared worktree and persistent final-delivery branch | no — commit only                   |
| 7        | Final archival and integration                              | The same worktree and branch; archive before opening the PR               | yes — exactly once, after archival |

No phase may create an additional worktree or branch. The final phase is the only delivery boundary.

## Path constants

```bash
if [ -d "plans/backlog/ayokoding-learning-path-15-skills-accounting-enterprise-reporting" ]; then
  PLANDIR="plans/backlog/ayokoding-learning-path-15-skills-accounting-enterprise-reporting/"
elif [ -d "plans/in-progress/ayokoding-learning-path-15-skills-accounting-enterprise-reporting" ]; then
  PLANDIR="plans/in-progress/ayokoding-learning-path-15-skills-accounting-enterprise-reporting/"
else
  PLANDIR=$(find plans/done -maxdepth 1 -type d -name "*ayokoding-learning-path-15-skills-accounting-enterprise-reporting" | head -1)/
fi
echo "PLANDIR=$PLANDIR"
```

- `COURSES="apps/ayokoding-www/content/en/learn/courses/"`
- `LANDING_CA="apps/ayokoding-www/content/en/learn/paths/skills/conventional-accounting/"`
- `LANDING_SA="apps/ayokoding-www/content/en/learn/paths/skills/sharia-accounting/"`
- `MANIFEST_CA="apps/ayokoding-www/src/features/course-paths/manifests/skills/conventional-accounting.json"`
- `MANIFEST_SA="apps/ayokoding-www/src/features/course-paths/manifests/skills/sharia-accounting.json"`
- `MTEST_CA="apps/ayokoding-www/src/features/course-paths/manifests/skills/conventional-accounting-manifest.unit.test.ts"`
- `MTEST_SA="apps/ayokoding-www/src/features/course-paths/manifests/skills/sharia-accounting-manifest.unit.test.ts"`
- `SPEC="${PLANDIR}syllabus/courses/"`
- `SPECPATHS="${PLANDIR}syllabus/paths/"`
- `SPECS="specs/apps/ayokoding/behavior/ayokoding-www/gherkin/course-paths/"`

## Course ID lists (shell ARRAYS only, HARD rule)

```bash
ACCT_P14=(accounting-foundations chart-of-accounts-and-data-modeling financial-statements-and-close-cycle \
  journal-entries-and-posting-mechanics accrual-accounting-and-revenue-recognition \
  accounts-payable-and-procure-to-pay accounts-receivable-and-order-to-cash \
  managerial-and-cost-accounting fixed-assets-and-depreciation inventory-and-cogs-accounting \
  lease-and-intangible-asset-accounting)                                    # 11 — inherited from plan 14

ACCT_P15=(multi-currency-accounting-and-fx-translation consolidation-and-multi-entity-accounting \
  financial-reporting-standards-ifrs-vs-gaap audit-controls-and-compliance \
  payroll-and-tax-accounting-essentials treasury-and-cash-management \
  financial-reporting-and-xbrl general-ledger-system-architecture)           # 8 — this plan's own range

ACCT_SHARED=("${ACCT_P14[@]}" "${ACCT_P15[@]}")   # 19 — both manifests' full courseOrder at this plan's end
ACCT_SILENT_P15=("${ACCT_P15[@]}")                 # 8 — this plan's own silent-failure-carrying courses
```

**Never** iterate these as a space-separated string.

---

## Phase 0: Environment Setup and Baseline

> _Suggested executor: direct tool use._

### Environment Setup

- [x] [AI] **Promote out of `plans/backlog/` first — on the local `main` checkout, before any worktree exists.**
      Run `git mv plans/backlog/ayokoding-learning-path-15-skills-accounting-enterprise-reporting/ plans/in-progress/ayokoding-learning-path-15-skills-accounting-enterprise-reporting/`
      (a pure move — neither stage carries a date prefix), update `plans/backlog/README.md` and
      `plans/in-progress/README.md`, commit on the plan branch and include the move in the one final PR — acceptance:
      `git ls-tree -r --name-only origin/main -- plans/in-progress/ayokoding-learning-path-15-skills-accounting-enterprise-reporting/README.md | grep -c .`
      returns **1** and the same query against `plans/backlog/ayokoding-learning-path-15-skills-accounting-enterprise-reporting/README.md` returns **0**.
      Falsifiable both ways: before the push lands, the first query returns 0 and the second
      returns 1. Execution never runs out of `plans/backlog/` — this push is a mandatory
      precondition, not a courtesy. See
      [plan-execution → Execute Plan from Backlog](../../../repo-governance/workflows/plan/plan-execution/example-usage-and-iteration-example.md#execute-plan-from-backlog).
- [x] [AI] Confirm the worktree is provisioned and current:
      `git worktree list | grep -F "ayokoding-learning-path-15-skills-accounting-enterprise-reporting"` exits 0.
- [x] [AI] Install dependencies: `npm install`.
- [x] [AI] Run doctor to verify tooling: `npm run doctor -- --fix`.
- [x] [AI] Verify dev server starts: `nx dev ayokoding-www`.
- [x] [AI] Verify existing tests pass before making changes: `npm exec nx run ayokoding-www:test:quick`.

### Baseline (must all be true before any content is authored)

- [x] [AI] Direct predecessor archival check passed; repository baseline facts checked — run the loop in
      [§Depends-on](#depends-on); acceptance: empty output.
- [x] [AI] Both manifests exist and hold exactly 11 entries, inherited from plan 14 — acceptance:
      `[ "$(grep -cE '^  - ' "$MANIFEST_CA")" -eq 11 ] && [ "$(grep -cE '^  - ' "$MANIFEST_SA")" -eq 11 ] && echo BASELINE-OK || echo BASELINE-FAIL`
      prints `BASELINE-OK`.
- [x] [AI] No course in `ACCT_P15` exists yet:
      `for c in "${ACCT_P15[@]}"; do test -d "${COURSES}$c" && echo "FOUND $c"; done | wc -l` returns
      **0** — acceptance: returns 0 today, returns 8 after Phase 2.
- [x] [AI] Both landings exist (inherited from plan 14) but neither states path completeness yet:
      `grep -F -q 'the path is complete' "${LANDING_CA}_index.md" && echo PREMATURE || echo OK` prints
      `OK`.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [x] [AI] `npm run doctor -- --fix` exits 0.
- [x] [AI] `npm exec nx run ayokoding-www:test:quick` exits 0.
- [x] [AI] Every Baseline check above holds.

> **Pause Safety**: plan 14's authored slice is confirmed present and correct; this plan's own
> content does not exist yet. Safe to stop. To resume: re-run `npm exec nx run ayokoding-www:test:quick` and
> confirm 0 exit before starting Phase 1.

---

## Phase 1: The eight syllabus specs

> _Suggested executor: direct authoring, `web-researcher` (coverage pass only, per A12), then
> delegate content authoring per course to `apps-ayokoding-www-by-example-maker` /
> `apps-ayokoding-www-annotated-concept-maker` in Phase 2._

### 1.1 · Create the spec folders

- [x] [AI] Create `"${SPEC}"` and `"${SPECPATHS}"` _(new directories)_ — acceptance: both
      `test -d` exit 0.
- [x] [AI] Create `"${SPEC}README.md"`, `"${SPECPATHS}README.md"`, and
      `"${PLANDIR}syllabus/README.md"` _(new files)_ with the
      `**Custodian**: ayokoding-learning-path-15-skills-accounting-enterprise-reporting` line —
      acceptance: `grep -q '\*\*Custodian\*\*: ayokoding-learning-path-15-skills-accounting-enterprise-reporting' "${PLANDIR}syllabus/README.md"`
      exits 0.

### 1.2 · Author all eight syllabi

- [x] [AI] Author `"${SPEC}<course-id>.md"` for each of the 8 courses in `ACCT_P15` — acceptance:
      `for c in "${ACCT_P15[@]}"; do test -f "${SPEC}$c.md" || echo "MISSING $c"; done | wc -l`
      returns **0**.
  - _Suggested executor: `apps-ayokoding-www-general-maker`_
- [x] [AI] Confirm every syllabus has no `## Capstone spec` section (A6) and does have
      `## Applied synthesis (no build — A6)` — acceptance: both checks return **0** violations,
      matching the pattern from plan 14's own §1.2.
- [x] [AI] Confirm all 8 courses in `ACCT_SILENT_P15` carry a worked silent-failure example:
      `for c in "${ACCT_SILENT_P15[@]}"; do grep -q 'silent-failure' "${SPEC}$c.md" || echo "MISSING $c"; done | wc -l`
      returns **0**.

### 1.3 · Coverage pass (A12 step 2)

- [x] [AI] For each course, dispatch `web-researcher` with the coverage-only question, never a
      curriculum-matching question — acceptance: each syllabus's `## In which paths` section is
      unchanged by the coverage pass.

### 1.4 · Licensing-sensitive-sources recording

- [x] [AI] For each of the 8 syllabi, record which standard numbers and XBRL taxonomy releases it
      cites — acceptance: `for c in "${ACCT_P15[@]}"; do grep -q '^## Accuracy notes' "${SPEC}$c.md" || echo "MISSING $c"; done | wc -l`
      returns **0**.

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [x] [AI] All 8 syllabus files exist, each with `## Applied synthesis (no build — A6)` and no
      `## Capstone spec`.
- [x] [AI] All 8 syllabi carry a worked silent-failure example.
- [x] [AI] Every syllabus has a non-empty `## Accuracy notes` licensing-sensitive-sources record.
- [x] [AI] **Concept floor holds (≥ 8)** —
      `for c in "${ACCT_P15[@]}"; do n=$(grep -c '^- \*\*co-[0-9]' "${SPEC}$c.md"); [ "$n" -ge 8 ] || echo "UNDER-FLOOR $c = $n"; done | wc -l`
      returns **0**.
- [x] [AI] **All REQUIRED template sections present** (the five sections not already covered by the
      checks above — `## Accuracy notes` and `## Concepts` are covered), per the
      [Learning-Plan `syllabus/` Folder Convention §Corpus Census and Section Tiering](../../../repo-governance/conventions/structure/learning-plan-syllabus/corpus-census-section-tiering.md#corpus-census-section-tiering-table):

```bash
for c in "${ACCT_P15[@]}"; do
  f="${SPEC}$c.md"
  grep -q '\*\*Course ID\*\*'    "$f" || echo "MISSING Course-ID $c"
  grep -q '^## Why this exists' "$f" || echo "MISSING Why-this-exists $c"
  grep -q '^## Prerequisites'   "$f" || echo "MISSING Prerequisites $c"
  grep -q '\*\*Scope note\*\*'  "$f" || echo "MISSING Scope-note $c"
  grep -q '^## In which paths'  "$f" || echo "MISSING In-which-paths $c"
done | wc -l
```

Acceptance: returns **0**.

- [x] [AI] `npm run lint:md` exits 0 on the new `syllabus/` tree.
- [x] [AI] **Every prerequisite edge is transcribed and resolves**, including edges reaching back
      into plan 14's already-merged courses:

```bash
# (1) Unresolved prior-course edges. MUST print 0. Resolves against this plan's own SPEC
# AND against plan 14's already-merged COURSES directory (the cross-plan-boundary edges).
for f in $(find "${SPEC}" -maxdepth 1 -name '*.md' ! -name 'README.md'); do
  awk '/^- \*\*Prior courses\*\*/{p=1;print;next} p&&/^- \*\*/{p=0} p' "$f" \
    | grep -oE '`[a-z0-9-]+`' | tr -d '`' | while IFS= read -r id; do
        [ -f "${SPEC}${id}.md" ] || [ -d "${COURSES}${id}" ] || [ "$id" = "backend-essentials" ] || echo "UNRESOLVED $(basename "$f") -> $id"
      done
done | wc -l

# (2) Anti-vacuity companion: total edges examined. MUST be > 0.
for f in $(find "${SPEC}" -maxdepth 1 -name '*.md' ! -name 'README.md'); do
  awk '/^- \*\*Prior courses\*\*/{p=1;print;next} p&&/^- \*\*/{p=0} p' "$f" \
    | grep -oE '`[a-z0-9-]+`'
done | wc -l
```

Acceptance: command (1) returns **0**; command (2) returns a count **> 0**.

> **Pause Safety**: the full spec layer for this plan's 8-course range exists and is internally
> consistent; no course body has been authored yet. Safe to stop. To resume: re-run the Phase 1
> Gate's checks before starting Phase 2.

---

## Phase 2: Stage 2 — courses #12–#19, both manifests grown to nineteen, conventional-accounting DONE

> _Suggested executor: `apps-ayokoding-www-by-example-maker` / `apps-ayokoding-www-annotated-concept-maker`
> (per course's Format column) + `web-researcher` (accuracy pre-verify)._
>
> **This phase completes `conventional-accounting`.**

### 2.1 · Author the eight Stage-2 bodies

- [x] [AI] Course #12 `multi-currency-accounting-and-fx-translation` (By Example; prerequisite:
      plan 14's #3) — acceptance: 7 steps complete (per plan 14's own §2.1 convention); silent-failure
      section present.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [x] [AI] Course #13 `consolidation-and-multi-entity-accounting` (By Example; prerequisites: plan
      14's #2, #3, this plan's #12) — acceptance: 7 steps complete; silent-failure section present.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [x] [AI] Course #14 `financial-reporting-standards-ifrs-vs-gaap` (Annotated-concept;
      prerequisites: plan 14's #5, #11) — acceptance: 7 steps complete (adapted for
      Annotated-concept: themed grouping, no Beginner/Intermediate/Advanced bands); silent-failure
      section present.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [x] [AI] Course #15 `audit-controls-and-compliance` (Annotated-concept; prerequisite: plan 14's
      #3) — acceptance: 7 steps complete; silent-failure section present.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [x] [AI] Course #16 `payroll-and-tax-accounting-essentials` (By Example; prerequisite: plan 14's
      #2) — acceptance: 7 steps complete; silent-failure section present.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [x] [AI] Course #17 `treasury-and-cash-management` (By Example; prerequisites: plan 14's #6, #7)
      — acceptance: 7 steps complete; silent-failure section present.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [x] [AI] Course #18 `financial-reporting-and-xbrl` (Annotated-concept; prerequisite: this plan's
      #14) — acceptance: 7 steps complete; silent-failure section present.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [x] [AI] Course #19 `general-ledger-system-architecture` (By Example; prerequisites: plan 14's
      #2, #3, and the **linked** `backend-essentials`) — replaces the retired single-path design's
      deleted capstone (A6); carries the `DD-15` reference-implementation licensing note —
      acceptance: 7 steps complete; silent-failure section present;
      `grep -F -q 'backend-essentials' "${COURSES}general-ledger-system-architecture/_index.md"`
      exits 0 **and**
      `grep -F -q 'backend-essentials' "${COURSES}general-ledger-system-architecture/overview.md"`
      exits 0; **and no `learning/capstone/` directory exists**:
      `test -d "${COURSES}general-ledger-system-architecture/learning/capstone" && echo VIOLATION || echo OK`
      prints `OK`.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [x] [AI] **Stage-2 body check** —
      `for c in "${ACCT_P15[@]}"; do test -d "${COURSES}$c" || echo "MISSING $c"; done | wc -l`
      returns **0**.
- [x] [AI] Append all eight catalog rows to `"${COURSES}_index.md"` — acceptance:
      `for c in "${ACCT_P15[@]}"; do grep -F -q "$c" "${COURSES}_index.md" || echo "MISSING $c"; done | wc -l`
      returns **0**.

  **Gherkin (binds) →** "A manifest links its software-engineering prerequisite instead of walking
  it" (Examples: `conventional-accounting`, `sharia-accounting`)

  ```gherkin
  Scenario Outline: A manifest links its software-engineering prerequisite instead of walking it
    Given the <path> manifest is grown to include general-ledger-system-architecture
    When a reader inspects its courseOrder
    Then backend-essentials does not appear in courseOrder
    And the general-ledger-system-architecture course declares backend-essentials in its prerequisites frontmatter
    And the <path> landing links that prerequisite course at its canonical /en/learn/courses/ URL

    Examples:
      | path                    |
      | conventional-accounting |
      | sharia-accounting       |
  ```

- [x] [AI] **Link-don't-walk check, both manifests** —
      `for M in "$MANIFEST_CA" "$MANIFEST_SA"; do grep -oE 'backend-essentials' "$M" | wc -l; done`
      returns **0 0**.

### 2.2 · TDD cycle — grow BOTH manifests to nineteen

- [x] [AI] **RED** — extend `$MTEST_CA` and `$MTEST_SA` with failing assertions that each
      `courseOrder` grows from length 11 to length 19, appending `ACCT_P15` in order, still passing
      both integrity checks — command: `npm exec nx run ayokoding-www:test:unit` — acceptance: both new
      assertions fail (length still 11).

  **Gherkin (binds) →** "Conventional-accounting reaches its terminal, complete state at course
  nineteen"

  ```gherkin
  Scenario: Conventional-accounting reaches its terminal, complete state at course nineteen
    Given both manifests have grown to include the full nineteen-course shared spine
    When a reader reaches the end of the conventional-accounting courseOrder
    Then the path landing states the path is complete
    And no further course is ever appended to conventional-accounting.json at any later phase or plan
    But the sharia-accounting manifest's courseOrder is left ready to continue past entry nineteen
  ```

- [x] [AI] **GREEN** — grow `$MANIFEST_CA` and `$MANIFEST_SA` to 19 entries each (both hold exactly
      `ACCT_SHARED` in order, still byte-identical to each other) — command:
      `npm exec nx run ayokoding-www:test:unit` — acceptance: exits 0; both files have exactly 19
      `courseOrder` entries; `diff <(grep -E '^  - ' "$MANIFEST_CA") <(grep -E '^  - ' "$MANIFEST_SA")`
      returns empty.
- [x] [AI] **REFACTOR** — command: `npm exec nx run ayokoding-www:test:unit && npm exec nx run ayokoding-www:lint` —
      acceptance: both exit 0.

- [x] [AI] **Shared-course non-duplication check (A11), full 19-course sweep** —
      `for c in "${ACCT_SHARED[@]}"; do n=$(find "${COURSES}$c" -maxdepth 0 -type d | wc -l); [ "$n" -eq 1 ] || echo "DUPLICATE-OR-MISSING $c"; done | wc -l`
      returns **0**.

### 2.3 · `conventional-accounting` reaches its terminal state — a genuine milestone

- [x] [AI] Update `"${LANDING_CA}_index.md"` to state the path is **complete** at nineteen courses
      (no further growth is coming) — acceptance: `grep -F -q 'complete' "${LANDING_CA}_index.md"`
      exits 0.
- [x] [AI] Update `"${LANDING_SA}_index.md"` to state the Dangerous-2 boundary, continuing to
      promise the not-yet-authored Sharia stage — acceptance:
      `grep -F -q 'Dangerous 2' "${LANDING_SA}_index.md"` exits 0.
- [x] [AI] **Freeze check** — record, in this file, that `conventional-accounting.json` will
      receive no further `courseOrder` growth after this point; the only future touches to
      `$MANIFEST_CA` (by plan 16 or any later plan) are re-verification sweeps, never a content
      change.
- [x] [AI] Run `apps-ayokoding-www-link-checker` and `apps-ayokoding-www-general-checker` over both
      updated landings — apply fixers — acceptance: zero CRITICAL/HIGH/MEDIUM remain.

  **Gherkin (binds) →** Outline "A path landing states its arc and ramp before the course list"

  ```gherkin
  Scenario Outline: A path landing states its arc and ramp before the course list
    Given the <path> landing is updated with the Dangerous-2 boundary
    When a reader opens /en/learn/paths/skills/<path>
    Then the Dangerous-2 boundary appears before the ordered course list
    And the boundary names both what the reader can do and what the reader cannot yet do
    And conventional-accounting's landing additionally states the path is complete

    Examples:
      | path                    |
      | conventional-accounting |
      | sharia-accounting       |
  ```

### 2.4 · TDD cycle — extend both path-walks to the full nineteen-course spine

- [x] [AI] **RED** — extend the count-parameterized "walk a skills path" step (inherited from plan
      14's own REFACTOR step) in `apps/ayokoding-www-fe-e2e/src/steps/skills-path-composition.steps.ts`
      so both `pathId`s walk all **19** published courses via prev/next — command:
      `npm exec nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: the new 19-course assertion **fails** for
      both Examples rows (only 11 courses were walked before this phase).
- [x] [AI] **GREEN** — implement against both grown manifests — command:
      `npm exec nx run ayokoding-www:specs:behavior:coverage && npm exec nx run ayokoding-www-fe-e2e:test:e2e` —
      acceptance: both exit 0.
- [x] [AI] **REFACTOR** — parameterize the walk on expected course count so plan 16 extends it to
      24 without duplicating the helper — command: `npm exec nx run ayokoding-www-fe-e2e:test:e2e` —
      acceptance: exits 0, scenario count unchanged.

### 2.5 · Full-corpus silent-failure check

- [x] [AI] `for c in "${ACCT_SILENT_P15[@]}"; do grep -q 'silent-failure\|What still balances while being wrong' "${COURSES}$c/overview.md" || echo "MISSING $c"; done | wc -l`
      returns **0**.

  **Gherkin (binds) →** "Every course from twelve through nineteen names what still balances while
  being wrong"

  ```gherkin
  Scenario: Every course from twelve through nineteen names what still balances while being wrong
    Given a course numbered twelve through nineteen is authored
    When its overview is inspected
    Then it contains an explicit section naming at least one outcome that still balances while being substantively wrong
    And that section names the observable signal, if any, that would reveal the error
  ```

### 2.6 · Stage-2 signal

- [x] [AI] **Record the Stage-2 signal**, exact literal shape from
      [tech-docs §Stage-signal contract](./tech-docs.md#stage-signal-contract-the-plan-18-handoff-stage-granularity),
      each field anchored at column 0, outside any table/bullet/blockquote:

```
STAGE: 2
PLAN: ayokoding-learning-path-15-skills-accounting-enterprise-reporting
LANDED_COURSE_IDS: multi-currency-accounting-and-fx-translation, consolidation-and-multi-entity-accounting, financial-reporting-standards-ifrs-vs-gaap, audit-controls-and-compliance, payroll-and-tax-accounting-essentials, treasury-and-cash-management, financial-reporting-and-xbrl, general-ledger-system-architecture
UNBLOCKS_ERP_CAPABILITY: the ERP stages delivering inventory-costing, multi-company/consolidation, hire-to-retire/payroll, and segregation-of-duties/security capability (Stage-B-equivalent) — and the whole conventional-accounting path is complete at this point
FINAL_DELIVERY_BRANCH: ayokoding-learning-path-15-skills-accounting-enterprise-reporting/final-delivery
```

— acceptance: `grep -c '^STAGE: 2$' delivery.md` returns **1** and the signal is committed on this
plan's persistent final-delivery branch. The terminal archival PR is the only merge record.

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [x] [AI] All 8 Stage-2 course bodies exist, checkers green, every one carries a silent-failure
      section.
- [x] [AI] Both manifests grown to 19, still byte-identical, both pass `test:unit`.
- [x] [AI] `conventional-accounting` landing states completeness; `sharia-accounting` landing
      states the Dangerous-2 boundary.
- [x] [AI] Both path-walk e2e specs walk all 19 courses, not 11.
- [x] [AI] Both `sql-essentials` and `backend-essentials` link-don't-walk checks hold on both
      manifests.
- [x] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance:
      no PR, merge, deployment, or merge-commit record occurs before Phase 7.
- [x] [AI] `npm exec nx run ayokoding-www:build` exits 0.

> **Pause Safety**: `conventional-accounting` is a genuinely complete, shippable 19-course path,
> **walked end to end by §2.4's e2e**; `sharia-accounting` is at the same 19-course state, one
> stage short of its own completion. Safe to stop indefinitely at this exact point. To resume:
> re-run `npm exec nx run ayokoding-www:test:unit` and confirm 0 exit before starting Phase 3.

---

## Phase 3: Section and app verification

> _Suggested executor: direct verification; `apps-ayokoding-www-facts-checker` and
> `apps-ayokoding-www-link-checker` for the corpus-wide sweep._

### 3.1 · Manifest integrity, both manifests

- [x] [AI] `npm exec nx run ayokoding-www:test:unit` (both `$MTEST_CA` and `$MTEST_SA`) exits 0.
- [x] [AI] `checkManifestIntegrity` and `checkPrerequisiteConsistency` pass for both manifests as a
      standalone sweep, assertion count matching 19 for both.

### 3.2 · Ownership footprint check

- [x] [AI] Authorship-scoped commit-footprint check:
      `gh pr list --search "ayokoding-learning-path-15-skills-accounting-enterprise-reporting" --state merged --json number,files` and
      confirm every touched path under `apps/ayokoding-www/src/features/course-paths/manifests/` is
      one of the two files this plan extends — acceptance: no path under `manifests/careers/`,
      `manifests/skills/conventional-erp.json`, or `manifests/skills/sharia-erp.json` appears; no
      `_index.md` under `paths/` appears.

### 3.3 · Shared-course non-duplication, final sweep

- [x] [AI] `for c in "${ACCT_SHARED[@]}"; do n=$(find "${COURSES}$c" -maxdepth 0 -type d | wc -l); [ "$n" -eq 1 ] || echo "DUPLICATE-OR-MISSING $c"; done | wc -l`
      returns **0** (all 19 checked).

### 3.4 · Licensing reading audit (A8)

- [x] [AI] For every file in `"${SPEC}"` (8 syllabi) **and** every `overview.md` under
      `"${COURSES}"` for `ACCT_P15` (8 course bodies) — 16 files total — read against the eleven
      safe-authoring rules — acceptance: zero violations found; any finding is fixed before this
      gate closes.
- [x] [AI] **Every citation resolves to a full URL**, including XBRL taxonomy release citations —
      same recipe as plan 14's own §4.4, scoped to this plan's own `"${SPEC}"`. Acceptance: empty
      output.

  **Gherkin (binds) →** "No standard's text or proprietary structure is reproduced"

  ```gherkin
  Scenario: No standard's text or proprietary structure is reproduced
    Given this plan's eight courses are authored under the licensing posture in tech-docs.md
    When any course body cites a standard, a chart of accounts, or a reference implementation
    Then the standard is restated in original words with only its number, title, and official link cited
    And every chart of accounts in this plan's courses is originally authored
  ```

### 3.5 · Terminal-freeze assertion

- [x] [AI] **`conventional-accounting.json` is unchanged since this plan's own Phase 2 merge** —
      `git diff --quiet -- "$MANIFEST_CA"` exits 0.

### 3.6 · Scope-boundary sweep and no-unverified-claim sweep

- [x] [AI] Confirm neither manifest walks `backend-essentials` — final sweep, extends §2.1's check.
- [x] [AI] `apps-ayokoding-www-facts-checker` run over all 8 course bodies and all 8 syllabi —
      acceptance: zero unmarked claims.

  **Gherkin (binds) →** "No unverified claim is published as fact"

  ```gherkin
  Scenario: No unverified claim is published as fact
    Given the research seeding this plan's syllabi marked items as Unverified or Needs Verification
    When a syllabus spec or a course body states a claim, including any XBRL taxonomy version or standard citation
    Then the claim carries either a primary-source citation or an explicit confidence marker
    And every item still marked Needs Verification when this plan's own gate runs is registered with a reason
  ```

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [x] [AI] 3.1 through 3.6 all clean, zero unresolved findings.
- [x] [AI] `npm exec nx run ayokoding-www:build` exits 0.
- [x] [AI] `npm run lint:md` exits 0 across the whole plan folder and the whole
      `apps/ayokoding-www` content touched.

> **Pause Safety**: the corpus is verified, licensing-clean, and scope-consistent; the terminal
> freeze on `conventional-accounting.json` holds. Safe to stop. To resume: re-run 3.1's `test:unit`
> and 3.5's freeze check before starting Phase 4.

---

## Phase 4: Manual UI verification and FULL Rule-15 retest (conventional-accounting)

> _Suggested executor: Playwright MCP direct use; `web-exploratory-tester` /
> `web-usability-tester` / `web-design-tester` triad for the Rule-15 retest._
>
> **This plan runs the full Rule-15 three-tester retest, for `conventional-accounting` only** — a
> deliberate choice, since that path reaches genuine production completeness at this plan's end.
> `sharia-accounting`'s own retest, covering plan 16's incremental delta, runs once in plan 16.

### Manual UI Verification (Playwright MCP) — three breakpoints

- [x] [AI] Start dev server: `nx dev ayokoding-www`.
- [x] [AI] For EACH breakpoint (375 / 768 / 1280 px): navigate to
      `/en/learn/paths/skills/conventional-accounting` via `browser_navigate` + `browser_resize`.
- [x] [AI] Inspect DOM via `browser_snapshot` at every breakpoint — verify the arc promise, the
      completeness statement, and the rendered 19-course list all appear.
- [x] [AI] For EACH breakpoint (375 / 768 / 1280 px): navigate to
      `/en/learn/paths/skills/sharia-accounting` — verify the arc promise, the Dangerous-2 boundary,
      the path-choice note, and the rendered 19-course list.
- [x] [AI] Walk `conventional-accounting` end to end via prev/next controls (`browser_click`) —
      verify breadcrumb and `?path=` persistence at every step across all 19 courses.
- [x] [AI] Check for JS errors via `browser_console_messages` on both landings and a sample of
      walked courses, at every breakpoint — zero errors.
- [x] [AI] Take one screenshot per landing per breakpoint via `browser_take_screenshot`, saved to
      `evidence/phase-4-<landing>-en-<breakpoint>px.png` — commit as evidence.
- [x] [AI] Document verification results in this checklist, referencing each committed screenshot.

### Rule-15 three-tester retest (`conventional-accounting` only)

All three run in `delivery` mode so their findings land in this checklist. **Fold every finding in
as its own checkbox**, prefixed with the issuing tester's id — `EWT-###` / `UWT-###` / `DWT-###`.

- [x] [AI] Dispatch `web-exploratory-tester` against `conventional-accounting`'s landing and full
      19-course walk — record every finding as an `EWT-###` checkbox.
- [x] [AI] Dispatch `web-usability-tester` against `conventional-accounting`'s landing — record
      every finding as a `UWT-###` checkbox.
- [x] [AI] Dispatch `web-design-tester` against `conventional-accounting`'s landing — record every
      finding as a `DWT-###` checkbox.
- [x] [AI] **Resolve every defect finding from the triad, at all severities.** A MEDIUM or LOW may
      be deferred **only** with explicit recorded permission naming the finding id and the reason.
      Re-run the affected tester(s) after fixing and confirm the finding no longer reproduces.

  **Gherkin (binds) →** "Conventional-accounting passes its full live-site retest"

  ```gherkin
  Scenario: Conventional-accounting passes its full live-site retest
    Given conventional-accounting is complete at nineteen courses and deployed to production
    When the web-exploratory-tester, web-usability-tester, and web-design-tester triad runs against it
    Then every finding is folded in as an individually tickable, source-attributed checkbox
    And every defect finding is resolved or explicitly deferred with recorded permission before archival
  ```

### Phase 4 Gate

> All checks below must pass before starting Phase 5.

- [x] [AI] Both landings walked end to end with zero JS console errors.
- [x] [AI] Screenshot evidence committed for both landings, all three breakpoints.
- [x] [AI] Rule-15 triad complete for `conventional-accounting`; every `EWT-###`/`UWT-###`/`DWT-###`
      finding folded in as a checkbox and **resolved at every severity**, or explicitly deferred
      with a recorded permission naming the finding id and reason.

> **Pause Safety**: `conventional-accounting` is manually verified end to end and has passed its
> full live-site retest. Safe to stop. To resume: re-open both landings via `browser_navigate` and
> re-check `browser_console_messages` before starting Phase 5.

---

## Phase 5: Final quality and archival-PR readiness

> _Suggested executor: direct git/CI operations._

### Local Quality Gates (Before archival)

- [x] [AI] `npm exec nx affected -t typecheck,build,test:quick,lint` exits 0.
- [x] [AI] `npm exec nx run ayokoding-www:specs:behavior:coverage` exits 0.
- [x] [AI] `npm run lint:md` exits 0.

> **Important**: fix ALL failures found during these gates, not just those caused by this plan's own
> changes.

### Commit Guidelines

- [x] [AI] Commit changes thematically. Follow Conventional Commits format. Split different
      domains/concerns into separate commits. Do NOT bundle unrelated fixes into a single commit.

### Pre-archival readiness

- [x] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch; acceptance:
      no PR, merge, deployment, or merge-commit record occurs before Phase 7.
- [x] [AI] Reconcile the persistent branch non-destructively with current `origin/main`, then re-run
      every local quality gate; acceptance: all gates are green.
- [x] [AI] Preserve Phase 4's local UI evidence. Open no PR until Phase 7 has committed the archival
      move and index updates.

  **Gherkin (binds) →** "This plan's authored slice builds and validates green"

  ```gherkin
  Scenario: This plan's authored slice builds and validates green
    Given both manifests hold nineteen entries and all eight of this plan's course bodies are authored
    When the app build, the affected test tiers, and the link and heading validators run
    Then the build and every affected tier succeed
    And manifest integrity and prerequisite consistency report zero violations for both manifests
  ```

### Stage-2 signal, final confirmation

- [x] [AI] `grep -c '^STAGE: 2$' "${PLANDIR}delivery.md"` returns **1**, and the signal is committed
      on the persistent final-delivery branch.

### Phase 5 Gate

> All checks below must pass before starting Phase 6.

- [x] [AI] Stage-2 signal is present and committed on the persistent final-delivery branch.
- [x] [AI] All local quality gates and Phase 4 evidence are green; no PR exists before Phase 7.

> **Pause Safety**: this plan's authored corpus is verified and committed on the persistent
> final-delivery branch. Safe to stop. To resume: re-run the local quality gates before Phase 6.

---

## Phase 6: Knowledge Capture

> _Triage every surviving `learnings.md` entry before archival._

- [x] [AI] Apply the litmus test to every `learnings.md` entry — keep only if a durable surface
      would catch this automatically next time; discard the rest with a one-line reason.
- [x] [AI] Apply the secret/sensitivity gate and the repo-relevance gate.
- [x] [AI] Route each surviving learning to exactly one durable home; code-homed learnings are
      filed as a separate `plans/backlog/<slug>/` plan, never landed inline.
- [x] [AI] For any entry routed to `plans/ideas/`, scan `plans/ideas/README.md` and the existing
      two-pagers FIRST for a brief already covering the same problem or area — fold the learning into
      that brief instead of creating a new file; only create a new `plans/ideas/<slug>.md` when the
      scan confirms no existing brief overlaps (see
      [Integrate Before You Add](../../../repo-governance/conventions/structure/plans/ideas-folder-overview-rationale-and-file-layout.md#integrate-before-you-add-no-duplicate-two-pagers))
      — acceptance: the entry's routing line names either the folded-into brief or confirms the
      overlap scan found nothing.
- [x] [AI] If no generalizable learning surfaced, record `No generalizable learnings — <reason>`.

### Phase 6 Gate

- [x] [AI] Every `learnings.md` entry is terminal, or the explicit "none" escape is recorded.
- [x] [AI] No code-homed learning landed inline in this plan's own commits/PRs.

> **Pause Safety**: `learnings.md` is fully triaged. Safe to stop. To resume: re-read
> `learnings.md` and confirm every entry is terminal.

---

## Phase 7: Plan Archival

### Sole PR integration (binding)

- [x] [AI] Archive this plan on its persistent final-delivery branch before review — acceptance: the archive move and index updates are committed in the same branch.
- [x] [AI] Open exactly one draft PR from that branch and run the secret scan, local quality checks, and PR quality-gate verification plus every local and CI gate — acceptance: the PR is the only PR for this plan.
- [x] [AI] Mark the PR ready, merge under the hardened preconditions, and deploy once — acceptance: the merge/deploy record is the plan's sole delivery record.

- [x] [AI] `git mv plans/in-progress/ayokoding-learning-path-15-skills-accounting-enterprise-reporting plans/done/$(date +%Y-%m-%d)__ayokoding-learning-path-15-skills-accounting-enterprise-reporting`
      (always from `plans/in-progress/` — Phase 0's promotion step is a mandatory precondition).
- [x] [AI] Update `plans/in-progress/README.md` — remove this
      plan's entry.
- [x] [AI] Update `plans/done/README.md` — add this plan's entry with its completion date.
- [x] [AI] Update `ayokoding-learning-path-16-skills-accounting-sharia-extension`'s own docs (if it
      exists at this point) to note this plan's merge and Stage-2 signal are now on `origin/main`.
- [x] [AI] Commit the archival move to the persistent final-delivery branch before opening the only PR —
      `git commit -m "chore(plans): archive ayokoding-learning-path-15-skills-accounting-enterprise-reporting"`.
- [x] [AI] **Push the archival commit** — `git push origin HEAD` — acceptance: exits 0 and
      `git status -sb | grep -c 'ahead'` returns **0**.
- [x] [AI] **Monitor CI on the new head** — poll every 2 minutes. Acceptance: `status` is
      `completed` **and** `conclusion` is `success` for the run whose head SHA equals
      `git rev-parse HEAD`.
- [x] [AI] Re-confirm all five PR Merge Protocol preconditions still hold, then perform the `[AI]`
      merge. This is the terminal step of the plan.

### Phase 7 Gate

- [x] [AI] `test -d plans/done/*__ayokoding-learning-path-15-skills-accounting-enterprise-reporting` exits 0.
- [x] [AI] `test -d plans/backlog/ayokoding-learning-path-15-skills-accounting-enterprise-reporting`
      and `test -d plans/in-progress/ayokoding-learning-path-15-skills-accounting-enterprise-reporting`
      both exit 1.
- [x] [AI] The archival commit is an ancestor of the merged PR head — verify with
      `gh pr list --head "$(git rev-parse --abbrev-ref HEAD)" --state merged --json number,mergeCommit`.

> **Pause Safety**: plan complete and archived. Plan 16 may now start. Nothing further to resume.
