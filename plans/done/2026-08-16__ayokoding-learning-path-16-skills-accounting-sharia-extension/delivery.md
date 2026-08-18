# Delivery Checklist — Skills Paths: Accounting Sharia Extension

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`). `[HUMAN]`:
> only a human can do it (physical action, out-of-band approval, real-secret or privileged-credential
> handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate`: a must-pass verification checklist plus
> a **Pause Safety** note. A phase is **not complete until its gate is green**; do not start phase N+1
> while any check in phase N's gate is failing.

## One-PR delivery contract (binding, 2026-08-01)

This 5-course plan is one inseparable delivery unit: every Phase 1–8 change lands in **one
worktree, one branch, and exactly one draft PR**. Courses may still be authored, checked, and
committed in their dependency order, but no intermediate phase may push, open a PR, run the PR
merge, deploy, or record a merge SHA. Only Phase 8 opens the draft PR, after all
course work, verification, and Knowledge Capture are green; it includes the archival move to
`plans/done/`, then runs the secret scan, local quality checks, and PR quality-gate verification, CI verification, ready-for-review
transition, and the normal `[AI]` merge/deploy protocol. No earlier stage or delivery boundary opens
a PR.

The `worktrees/ayokoding-learning-path-16-skills-accounting-sharia-extension/` path below is this
plan's only worktree; no per-course, stage, phase, or closeout worktree is created.

## Worktree

Worktree path: `worktrees/ayokoding-learning-path-16-skills-accounting-sharia-extension/`

Provision this path exactly once with `claude --worktree ayokoding-learning-path-16-skills-accounting-sharia-extension` (or `git worktree add -b worktree/ayokoding-learning-path-16-skills-accounting-sharia-extension worktrees/ayokoding-learning-path-16-skills-accounting-sharia-extension origin/main` when provisioning manually). Both forms designate the same one worktree; never create a second path for a phase, course, or closeout.

Final-delivery branch: `ayokoding-learning-path-16-skills-accounting-sharia-extension/final-delivery`

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
`final-delivery` branch in the declared worktree. Phases before 8 must not push, open
a PR, start an external merge, deploy, or record an in-repository merge SHA. Phase 8 first
commits the archival move and index updates, then opens the sole draft PR, runs the secret scan, local quality checks, and PR quality-gate verification plus local and CI gates, marks it ready, merges under the hardened
preconditions, and deploys once.

## Content-only delivery safeguards

This plan produces content only and has exactly one final PR. It has no review-cycle requirement. Before pushing that PR:

- [x] [AI] Inspect the staged diff and confirm it contains no machine-secret value.
- [x] [AI] Use a scoped Conventional Commit (for example, `docs(plans): refresh course-preparation backlog`).
- [x] [AI] Run `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`; acceptance: exits 0 for the affected scope.
- [x] [AI] Push the single branch, then wait for `.github/workflows/pr-quality-gate.yml`; acceptance: the PR quality gate is green before merge.

## Depends-on

| Relation      | Plan (full folder name)                                             | Nature                                                                                                                                                                                                                         |
| ------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **blockedBy** | `ayokoding-learning-path-15-skills-accounting-enterprise-reporting` | **Hard; sole direct execution prerequisite.** It must be fully merged and archived on `origin/main` before Phase 0. All earlier completion and repository-baseline facts are transitive context, not extra plan prerequisites. |

**Phase 0 start check:** `git ls-tree -r --name-only origin/main plans/done | rg -q "__ayokoding-learning-path-15-skills-accounting-enterprise-reporting/README\.md$"` exits 0. This is this plan's only plan-level start gate.

## Parallelization Model

Course #20 has no in-range prerequisite (its prerequisites, #5 and #14, are already merged from
plans 14/15) and authors first; #21 waits on #20; #22 waits on #21; #23 waits on #21 (its other
prerequisite, #12, is already merged); #24 waits on #21 (its other prerequisite, #19, is already
merged). This range is therefore mostly **sequential** — #20 → #21 → {#22, #23, #24} in parallel.
The manifest-growth TDD cycle is one sub-phase, run once all five bodies exist.

### Delivery Boundaries

| Phase(s) | Delivery unit                                               | Worktree / branch                                                         | PR opens                           |
| -------- | ----------------------------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------- |
| 0        | Setup and baseline                                          | No delivery worktree or PR                                                | no                                 |
| 1–7      | Intermediate authoring, verification, and Knowledge Capture | This plan's single declared worktree and persistent final-delivery branch | no — commit only                   |
| 8        | Final archival and integration                              | The same worktree and branch; archive before opening the PR               | yes — exactly once, after archival |

No phase may create an additional worktree or branch. The final phase is the only delivery boundary.

## Path constants

```bash
if [ -d "plans/backlog/ayokoding-learning-path-16-skills-accounting-sharia-extension" ]; then
  PLANDIR="plans/backlog/ayokoding-learning-path-16-skills-accounting-sharia-extension/"
elif [ -d "plans/in-progress/ayokoding-learning-path-16-skills-accounting-sharia-extension" ]; then
  PLANDIR="plans/in-progress/ayokoding-learning-path-16-skills-accounting-sharia-extension/"
else
  PLANDIR=$(find plans/done -maxdepth 1 -type d -name "*ayokoding-learning-path-16-skills-accounting-sharia-extension" | head -1)/
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
ACCT_SHARED=(accounting-foundations chart-of-accounts-and-data-modeling financial-statements-and-close-cycle \
  journal-entries-and-posting-mechanics accrual-accounting-and-revenue-recognition \
  accounts-payable-and-procure-to-pay accounts-receivable-and-order-to-cash \
  managerial-and-cost-accounting fixed-assets-and-depreciation inventory-and-cogs-accounting \
  lease-and-intangible-asset-accounting multi-currency-accounting-and-fx-translation \
  consolidation-and-multi-entity-accounting financial-reporting-standards-ifrs-vs-gaap \
  audit-controls-and-compliance payroll-and-tax-accounting-essentials \
  treasury-and-cash-management financial-reporting-and-xbrl \
  general-ledger-system-architecture)                                         # 19 — inherited from plans 14+15

ACCT_P16=(sharia-accounting-and-aaoifi-standards islamic-contract-modeling-for-systems \
  zakah-computation-and-reporting-for-systems sukuk-and-islamic-capital-markets-accounting \
  sharia-ledger-system-architecture)                                          # 5 — this plan's own range

ACCT_SA_FULL=("${ACCT_SHARED[@]}" "${ACCT_P16[@]}")   # 24 — sharia-accounting's full courseOrder at this plan's end
ACCT_SILENT_P16=("${ACCT_P16[@]}")                     # 5 — this plan's own silent-failure-carrying courses
```

**Never** iterate these as a space-separated string.

---

## Phase 0: Environment Setup and Baseline

> _Suggested executor: direct tool use._

### Environment Setup

- [x] [AI] **Promote out of `plans/backlog/` first — on the local `main` checkout, before any worktree exists.**
      Run `git mv plans/backlog/ayokoding-learning-path-16-skills-accounting-sharia-extension/ plans/in-progress/ayokoding-learning-path-16-skills-accounting-sharia-extension/`
      (a pure move — neither stage carries a date prefix), update `plans/backlog/README.md` and
      `plans/in-progress/README.md`, commit on the plan branch and include the move in the one final PR — acceptance:
      `git ls-tree -r --name-only origin/main -- plans/in-progress/ayokoding-learning-path-16-skills-accounting-sharia-extension/README.md | grep -c .`
      returns **1** and the same query against `plans/backlog/ayokoding-learning-path-16-skills-accounting-sharia-extension/README.md` returns **0**.
      Falsifiable both ways: before the push lands, the first query returns 0 and the second
      returns 1. Execution never runs out of `plans/backlog/` — this push is a mandatory
      precondition, not a courtesy. See
      [plan-execution → Execute Plan from Backlog](../../../repo-governance/workflows/plan/plan-execution/example-usage-and-iteration-example.md#execute-plan-from-backlog).
- [x] [AI] Confirm the worktree is provisioned and current:
      `git worktree list | grep -F "ayokoding-learning-path-16-skills-accounting-sharia-extension"` exits 0.
- [x] [AI] Install dependencies: `npm install`.
- [x] [AI] Run doctor to verify tooling: `npm run doctor -- --fix`.
- [x] [AI] Verify dev server starts: `nx dev ayokoding-www`.
- [x] [AI] Verify existing tests pass before making changes: `npm exec nx run ayokoding-www:test:quick`.

### Baseline (must all be true before any content is authored)

- [x] [AI] Direct predecessor archival check passed; repository baseline facts checked — run the loop in
      [§Depends-on](#depends-on); acceptance: empty output.
- [x] [AI] Both manifests exist; `MANIFEST_CA` holds exactly 19 entries (its terminal state) and
      `MANIFEST_SA` holds exactly 19 entries (its starting state for this plan) — acceptance:
      `[ "$(grep -cE '^  - ' "$MANIFEST_CA")" -eq 19 ] && [ "$(grep -cE '^  - ' "$MANIFEST_SA")" -eq 19 ] && echo BASELINE-OK || echo BASELINE-FAIL`
      prints `BASELINE-OK`.
- [x] [AI] No course in `ACCT_P16` exists yet:
      `for c in "${ACCT_P16[@]}"; do test -d "${COURSES}$c" && echo "FOUND $c"; done | wc -l` returns
      **0** — acceptance: returns 0 today, returns 5 after Phase 3.
- [x] [AI] `sharia-accounting`'s landing exists (inherited) but does not yet state full path
      completeness: `grep -F -q 'the path is complete' "${LANDING_SA}_index.md" && echo PREMATURE || echo OK`
      prints `OK`.
- [x] [AI] Record `MANIFEST_CA`'s current checksum for the terminal-freeze assertion used at every
      later gate: `git rev-parse HEAD:"$MANIFEST_CA" > /tmp/manifest-ca-baseline.sha` — acceptance:
      file written, non-empty.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [x] [AI] `npm run doctor -- --fix` exits 0.
- [x] [AI] `npm exec nx run ayokoding-www:test:quick` exits 0.
- [x] [AI] Every Baseline check above holds.

> **Pause Safety**: plan 15's authored slice is confirmed present and correct, and
> `conventional-accounting.json`'s baseline checksum is recorded; this plan's own content does not
> exist yet. Safe to stop. To resume: re-run `npm exec nx run ayokoding-www:test:quick` and confirm 0 exit
> before starting Phase 1.

---

## Phase 1: The five syllabus specs

> _Suggested executor: direct authoring, `web-researcher` (coverage pass only, per A12), then
> delegate content authoring per course to `apps-ayokoding-www-by-example-maker` /
> `apps-ayokoding-www-annotated-concept-maker` in Phase 3._

### 1.1 · Create the spec folders

- [x] [AI] Create `"${SPEC}"` and `"${SPECPATHS}"` _(new directories)_ — acceptance: both
      `test -d` exit 0.
- [x] [AI] Create `"${SPEC}README.md"`, `"${SPECPATHS}README.md"`, and
      `"${PLANDIR}syllabus/README.md"` _(new files)_ with the
      `**Custodian**: ayokoding-learning-path-16-skills-accounting-sharia-extension` line —
      acceptance: `grep -q '\*\*Custodian\*\*: ayokoding-learning-path-16-skills-accounting-sharia-extension' "${PLANDIR}syllabus/README.md"`
      exits 0.

### 1.2 · Author all five syllabi

- [x] [AI] Author `"${SPEC}<course-id>.md"` for each of the 5 courses in `ACCT_P16` — acceptance:
      `for c in "${ACCT_P16[@]}"; do test -f "${SPEC}$c.md" || echo "MISSING $c"; done | wc -l`
      returns **0**.
  - _Suggested executor: `apps-ayokoding-www-general-maker`_
- [x] [AI] Confirm every syllabus has no `## Capstone spec` section (A6) and does have
      `## Applied synthesis (no build — A6)` — acceptance: both checks return **0** violations.
- [x] [AI] Confirm all 5 courses in `ACCT_SILENT_P16` carry a worked silent-failure example:
      `for c in "${ACCT_SILENT_P16[@]}"; do grep -q 'silent-failure' "${SPEC}$c.md" || echo "MISSING $c"; done | wc -l`
      returns **0**.
- [x] [AI] Confirm course #20's syllabus states the OI-2 doctrinal boundary explicitly (the
      practical consequence, never the unsettled derivation):
      `grep -F -q 'OI-2' "${SPEC}sharia-accounting-and-aaoifi-standards.md"` exits 0.

### 1.3 · Coverage pass (A12 step 2)

- [x] [AI] For each course, dispatch `web-researcher` with the coverage-only question, never a
      curriculum-matching question — acceptance: each syllabus's `## In which paths` section is
      unchanged by the coverage pass.

### 1.4 · Licensing-sensitive-sources recording

- [x] [AI] For each of the 5 syllabi, record which standard numbers it cites (AAOIFI FAS numbers,
      PSAK series, MFRS/Bank Negara references) and any reference implementation, in
      `## Accuracy notes` — acceptance:
      `for c in "${ACCT_P16[@]}"; do grep -q '^## Accuracy notes' "${SPEC}$c.md" || echo "MISSING $c"; done | wc -l`
      returns **0**.

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [x] [AI] All 5 syllabus files exist, each with `## Applied synthesis (no build — A6)` and no
      `## Capstone spec`.
- [x] [AI] All 5 syllabi carry a worked silent-failure example.
- [x] [AI] Every syllabus has a non-empty `## Accuracy notes` licensing-sensitive-sources record.
- [x] [AI] **Concept floor holds (≥ 8)** —
      `for c in "${ACCT_P16[@]}"; do n=$(grep -c '^- \*\*co-[0-9]' "${SPEC}$c.md"); [ "$n" -ge 8 ] || echo "UNDER-FLOOR $c = $n"; done | wc -l`
      returns **0**.
- [x] [AI] `npm run lint:md` exits 0 on the new `syllabus/` tree.
- [x] [AI] **Every prerequisite edge is transcribed and resolves**, including edges reaching back
      into plans 14's and 15's already-merged courses:

```bash
# (1) Unresolved prior-course edges. MUST print 0.
for f in $(find "${SPEC}" -maxdepth 1 -name '*.md' ! -name 'README.md'); do
  awk '/^- \*\*Prior courses\*\*/{p=1;print;next} p&&/^- \*\*/{p=0} p' "$f" \
    | grep -oE '`[a-z0-9-]+`' | tr -d '`' | while IFS= read -r id; do
        [ -f "${SPEC}${id}.md" ] || [ -d "${COURSES}${id}" ] || echo "UNRESOLVED $(basename "$f") -> $id"
      done
done | wc -l

# (2) Anti-vacuity companion: total edges examined. MUST be > 0.
for f in $(find "${SPEC}" -maxdepth 1 -name '*.md' ! -name 'README.md'); do
  awk '/^- \*\*Prior courses\*\*/{p=1;print;next} p&&/^- \*\*/{p=0} p' "$f" \
    | grep -oE '`[a-z0-9-]+`'
done | wc -l
```

Acceptance: command (1) returns **0**; command (2) returns a count **> 0**. Unlike plans 14 and
15, no external `(SWE)` id is excluded here — this plan introduces no new linked prerequisite.

> **Pause Safety**: the full spec layer for this plan's 5-course range exists and is internally
> consistent; no course body has been authored yet. Safe to stop. To resume: re-run the Phase 1
> Gate's checks before starting Phase 2.

---

## Phase 2: Verification-debt resolution (OI-1 through OI-4)

> _Suggested executor: `web-researcher` for any residual re-check; direct authoring for the
> registry update._
>
> **This phase runs before any course in this plan's range is authored** — courses #20, #21, #24
> directly depend on OI-1/OI-2/OI-3's resolution state, per
> [tech-docs §Open verification items](./tech-docs.md#open-verification-items-oi-1-through-oi-4).

### 2.1 · Re-confirm each item's current status

- [x] [AI] Re-run a `web-researcher` check against OI-1's named primary source (IAI's published
      PSAK Syariah standard list) — acceptance: the `RESOLVED` status and its stated residual (the
      unconfirmed PPSAK ratification date) either hold unchanged or are updated with a dated new
      finding, never silently dropped.
- [x] [AI] Re-run a `web-researcher` check against OI-2's status — acceptance: OI-2's status line
      is confirmed to still read exactly `OI-2: OPEN`; if a primary AAOIFI Shari'ah Standard or IFSB
      publication is newly found, record it as a **new**, separately dated finding — **do not**
      promote OI-2 to `RESOLVED` on secondary-source or inferential grounds.
- [x] [AI] Re-run a `web-researcher` check against OI-3's named primary source (AAOIFI's
      adoption-by-country index) — acceptance: the `RESOLVED` status and its stated governance-
      mechanics residual either hold unchanged or are updated with a dated new finding.
- [x] [AI] Confirm OI-4's `ROUTED` status against plan 02's own dated ruling — acceptance: read
      plan 02's archived `tech-docs.md` ruling text directly (dated 2026-07-21), and record
      confirmation in this checklist.

### 2.2 · Update the registry

- [x] [AI] Update the status-line block in
      [tech-docs.md §Open verification items](./tech-docs.md#open-verification-items-oi-1-through-oi-4)
      in place — never delete a resolved line, rewrite its status — acceptance:
      `grep -c '^OI-1: ' "${PLANDIR}tech-docs.md"` returns **1**, and the same for `OI-2`, `OI-3`,
      `OI-4`.
- [x] [AI] **OI-2 falsifiable check** — `grep -F -q 'OI-2: OPEN' "${PLANDIR}tech-docs.md"` exits 0
      **and** `grep -F -q 'OI-2: RESOLVED' "${PLANDIR}tech-docs.md"` exits 1 — both directions
      checked, so a silent promotion to `RESOLVED` cannot pass unnoticed.

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [x] [AI] OI-1's and OI-3's `RESOLVED` status lines (with their stated residuals) are present.
- [x] [AI] OI-2's status line reads exactly `OI-2: OPEN`.
- [x] [AI] OI-4's `ROUTED` status is confirmed against plan 02's ruling.
- [x] [AI] No course body exists yet in `ACCT_P16` — this phase precedes authoring.

  **Gherkin (binds) →** "The verification-debt registry stays honest about the riba doctrinal
  basis" (checks the registry status line itself, not authored content — see the distinct,
  content-facing scenario of the same underlying concern bound later at §4.6)

  ```gherkin
  Scenario: The verification-debt registry stays honest about the riba doctrinal basis
    Given the research seeding this plan marked the riba doctrinal basis as an open item
    When this plan's Phase 2 gate runs
    Then OI-2's status line reads exactly OI-2: OPEN
    And no course body authored in a later phase restates the riba doctrinal derivation as settled fact
    And every item still marked Needs Verification when this gate runs is registered with a reason
  ```

> **Pause Safety**: the verification-debt registry is current and OI-2 is confirmed still open.
> Safe to stop. To resume: re-run 2.1's `web-researcher` checks before starting Phase 3.

---

## Phase 3: Stage 3 — courses #20–#24, sharia-accounting grown to twenty-four, CORPUS TERMINAL

> _Suggested executor: `apps-ayokoding-www-annotated-concept-maker` (courses #20, #23) +
> `apps-ayokoding-www-by-example-maker` (courses #21, #22, #24) + `web-researcher` (accuracy
> pre-verify)._
>
> **This phase completes `sharia-accounting`, and with it, the whole 24-course corpus.**

### 3.0 · Single-branch commit protocol

Phase 3 authors its five course bodies, manifest growth, landings, and E2E walk in the one declared
worktree. Commit complete, checked work on the persistent final-delivery branch in dependency order;
there is no per-course worktree, push, PR, review, merge, or deployment. These artifacts are reviewed
with the rest of the plan only when Phase 8 opens the sole final PR.

### 3.1 · Author the five Stage-3 bodies

- [x] [AI] Course #20 `sharia-accounting-and-aaoifi-standards` (Annotated-concept; prerequisites:
      plan 14's #5, plan 15's #14) — presents AAOIFI, PSAK Syariah, and MFRS-plus-BNM as three
      coexisting models; states OI-2's practical consequence without asserting its unsettled
      derivation — acceptance: 7 steps complete (per plan 14's own §2.1 convention, adapted for
      Annotated-concept per plan 15's own §2.1); silent-failure section present;
      `grep -F -q 'AAOIFI' "${COURSES}sharia-accounting-and-aaoifi-standards/overview.md"` exits 0
      **and** `grep -F -q 'PSAK Syariah' "${COURSES}sharia-accounting-and-aaoifi-standards/overview.md"`
      exits 0 **and**
      `grep -F -q 'MFRS' "${COURSES}sharia-accounting-and-aaoifi-standards/overview.md"` exits 0.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [x] [AI] Course #21 `islamic-contract-modeling-for-systems` (By Example; prerequisites: this
      plan's #20, plan 14's #2) — models murabaha as a trade, contrasted explicitly against a
      conventional amortising loan — acceptance: 7 steps complete; silent-failure section present;
      `grep -F -q 'murabaha' "${COURSES}islamic-contract-modeling-for-systems/overview.md"` exits 0
      **and**
      `grep -F -q 'amortising loan' "${COURSES}islamic-contract-modeling-for-systems/overview.md"`
      exits 0.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [x] [AI] Course #22 `zakah-computation-and-reporting-for-systems` (By Example; prerequisite: this
      plan's #21) — Zakah as its own obligation under AAOIFI FAS 9, distinct from income tax —
      acceptance: 7 steps complete; silent-failure section present;
      `grep -F -q 'FAS 9' "${COURSES}zakah-computation-and-reporting-for-systems/overview.md"`
      exits 0 **and**
      `grep -F -q 'not income tax' "${COURSES}zakah-computation-and-reporting-for-systems/overview.md"`
      exits 0.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [x] [AI] Course #23 `sukuk-and-islamic-capital-markets-accounting` (Annotated-concept;
      prerequisites: this plan's #21, plan 15's #12) — Sukuk accounting under AAOIFI FAS 32-34,
      distinct from conventional bond accounting — acceptance: 7 steps complete; silent-failure
      section present; `grep -F -q 'FAS 3' "${COURSES}sukuk-and-islamic-capital-markets-accounting/overview.md"`
      exits 0.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [x] [AI] Course #24 `sharia-ledger-system-architecture` (By Example; prerequisites: this plan's
      #21, plan 15's #19) — the corpus's terminal, architecture-closing course; replaces the
      retired plan's deleted `capstone-sharia-compliant-ledger` capstone (A6); no separate linked
      SWE prerequisite of its own — inherits `backend-essentials`'s grounding through its own
      prerequisite on plan 15's #19 — acceptance: 7 steps complete; silent-failure section present;
      **no `learning/capstone/` directory exists**:
      `test -d "${COURSES}sharia-ledger-system-architecture/learning/capstone" && echo VIOLATION || echo OK`
      prints `OK`.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [x] [AI] **Stage-3 body check** —
      `for c in "${ACCT_P16[@]}"; do test -d "${COURSES}$c" || echo "MISSING $c"; done | wc -l`
      returns **0**.
- [x] [AI] Append all five catalog rows to `"${COURSES}_index.md"` — acceptance:
      `for c in "${ACCT_P16[@]}"; do grep -F -q "$c" "${COURSES}_index.md" || echo "MISSING $c"; done | wc -l`
      returns **0**.

  **Gherkin (binds) →** "The Sharia stage presents three jurisdictional models"

  ```gherkin
  Scenario: The Sharia stage presents three jurisdictional models
    Given the Sharia-standards, contract-modelling, and Sharia-ledger-architecture courses are authored
    When a reader compares their treatment of standards
    Then each names AAOIFI, PSAK Syariah, and MFRS with the Bank Negara Malaysia Shariah Governance Policy as three structurally different coexisting models
    And none of them describes AAOIFI as the single Sharia accounting standard
    And each states that Malaysia is not on AAOIFI's mandatory-adoption list
    And each states that Indonesia uses AAOIFI as a basis rather than adopting it
  ```

  **Gherkin (binds) →** "A murabaha is modelled as a trade rather than as a loan"

  ```gherkin
  Scenario: A murabaha is modelled as a trade rather than as a loan
    Given the Islamic contract modelling course is authored
    When a reader compares a murabaha receivable schedule with a conventional amortising loan schedule
    Then the course shows the two schedules can look numerically similar and must be modelled differently
    And the markup is presented as fixed and disclosed at the point of sale in a trade with an underlying asset
    And the recognition is presented as a receivable and revenue from a sale rather than interest income
  ```

  **Gherkin (binds) →** "Zakah is computed and reported as its own obligation, not folded into tax"

  ```gherkin
  Scenario: Zakah is computed and reported as its own obligation, not folded into tax
    Given the Zakah computation and reporting course is authored
    When a reader compares its treatment with the conventional payroll-and-tax course from plan 15
    Then Zakah is presented as a distinct religious levy computed on a defined asset base under AAOIFI FAS 9
    And the course states explicitly that Zakah is not income tax and is not computed on the same base
    And no course folds a Zakah obligation into a payroll-and-tax course's scope
  ```

### 3.2 · TDD cycle — grow `sharia-accounting.json` ONLY, to twenty-four

- [x] [AI] **RED** — extend `$MTEST_SA` with failing assertions that `courseOrder` grows from
      length 19 to length 24, appending `ACCT_P16` in order, still passing both integrity checks —
      command: `npm exec nx run ayokoding-www:test:unit` — acceptance: the new assertion **fails** (length
      still 19). **`$MTEST_CA` receives no new assertion in this phase.**

  **Gherkin (binds) →** "Sharia-accounting reaches its terminal, complete state at course
  twenty-four"

  ```gherkin
  Scenario: Sharia-accounting reaches its terminal, complete state at course twenty-four
    Given sharia-accounting.json has grown to include all twenty-four courses
    When a reader reaches the end of the sharia-accounting courseOrder
    Then the path landing states the path is complete
    And no further course is ever appended to sharia-accounting.json at any later phase or plan
    And conventional-accounting.json remains exactly as it was at the end of plan 15
  ```

- [x] [AI] **GREEN** — grow `$MANIFEST_SA` to 24 entries (holds exactly `ACCT_SA_FULL` in order) —
      command: `npm exec nx run ayokoding-www:test:unit` — acceptance: exits 0; the file has exactly 24
      `courseOrder` entries.
- [x] [AI] **REFACTOR** — command: `npm exec nx run ayokoding-www:test:unit && npm exec nx run ayokoding-www:lint` —
      acceptance: exits 0.
- [x] [AI] **`conventional-accounting.json` untouched check, immediately after GREEN** —
      `git diff --quiet -- "$MANIFEST_CA"` exits 0 — falsifiable both ways: this check would fail
      if the growth step above had (incorrectly) touched the file, and must continue to pass at
      every later gate.
- [x] [AI] **Shared-course non-duplication check (A11), full 24-course sweep** —
      `for c in "${ACCT_SA_FULL[@]}"; do n=$(find "${COURSES}$c" -maxdepth 0 -type d | wc -l); [ "$n" -eq 1 ] || echo "DUPLICATE-OR-MISSING $c"; done | wc -l`
      returns **0**.

### 3.3 · `sharia-accounting` reaches its terminal state — the corpus's own final milestone

- [x] [AI] Update `"${LANDING_SA}_index.md"` to state the path is **complete** at twenty-four
      courses (no further growth is coming) — acceptance:
      `grep -F -q 'complete' "${LANDING_SA}_index.md"` exits 0.
- [x] [AI] **`conventional-accounting`'s landing is NOT touched** —
      `git diff --quiet -- "${LANDING_CA}_index.md"` exits 0.
- [x] [AI] Run `apps-ayokoding-www-link-checker` and `apps-ayokoding-www-general-checker` over the
      updated `sharia-accounting` landing — apply fixers — acceptance: zero
      CRITICAL/HIGH/MEDIUM remain.

  **Gherkin (binds) →** "The sharia-accounting landing states all three Dangerous boundaries"

  ```gherkin
  Scenario: The sharia-accounting landing states all three Dangerous boundaries
    Given the sharia-accounting landing is updated with all twenty-four courses
    When a reader opens /en/learn/paths/skills/sharia-accounting
    Then the Dangerous-1, Dangerous-2, and Dangerous-3 boundaries all appear before the ordered course list
    And each boundary names both what the reader can do and what the reader cannot yet do
    And the landing states the path is complete
  ```

### 3.4 · TDD cycle — extend the `sharia-accounting` path-walk to twenty-four courses

- [x] [AI] **RED** — extend the count-parameterized "walk a skills path" step (inherited from plan
      15's own REFACTOR step) in `apps/ayokoding-www-fe-e2e/src/steps/skills-path-composition.steps.ts`
      so `sharia-accounting`'s `pathId` walks all **24** published courses via prev/next — command:
      `npm exec nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: the new
      24-course assertion **fails** for `sharia-accounting` (only 19 courses were walked before this
      phase); `conventional-accounting`'s own 19-course walk assertion is **untouched** and
      continues to pass.
- [x] [AI] **GREEN** — implement against the grown manifest — command:
      `npm exec nx run ayokoding-www:specs:behavior:coverage && npm exec nx run ayokoding-www-fe-e2e:test:e2e` —
      acceptance: both exit 0.
- [x] [AI] **REFACTOR** — command: `npm exec nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: exits 0,
      scenario count unchanged for `conventional-accounting`'s own row.

### 3.5 · Full-corpus silent-failure check

- [x] [AI] `for c in "${ACCT_SILENT_P16[@]}"; do grep -q 'silent-failure\|What still balances while being wrong' "${COURSES}$c/overview.md" || echo "MISSING $c"; done | wc -l`
      returns **0**.

  **Gherkin (binds) →** "Every course from twenty through twenty-four names what still balances
  while being wrong"

  ```gherkin
  Scenario: Every course from twenty through twenty-four names what still balances while being wrong
    Given a course numbered twenty through twenty-four is authored
    When its overview is inspected
    Then it contains an explicit section naming at least one outcome that still balances while being substantively wrong
    And that section names the observable signal, if any, that would reveal the error
  ```

### 3.6 · No standard's text or proprietary structure is reproduced (this plan's own check)

- [x] [AI] Read all five course bodies against the eleven safe-authoring rules
      (see [tech-docs §Licensing](./tech-docs.md#licensing-and-ip-compliance-a8--the-full-four-body-posture-applying-in-full-for-the-first-time)) —
      acceptance: zero violations; every chart of accounts is confirmed originally authored, not
      transcribed from any textbook or reference implementation.

  **Gherkin (binds) →** "No standard's text or proprietary structure is reproduced"

  ```gherkin
  Scenario: No standard's text or proprietary structure is reproduced
    Given this plan's five courses are authored under the licensing posture in tech-docs.md
    When any course body cites AAOIFI, PSAK Syariah, or MFRS
    Then the standard is restated in original words with only its number, title, and official link cited
    And every chart of accounts in this plan's courses is originally authored
  ```

### 3.7 · Stage-3 signal

- [x] [AI] **Record the Stage-3 signal**, exact literal shape from
      [tech-docs §Stage-signal contract](./tech-docs.md#stage-signal-contract-the-plan-18-handoff-sharia-stage-granularity),
      each field anchored at column 0, outside any table/bullet/blockquote:

— acceptance: `grep -c '^STAGE: 3$' delivery.md` returns **1** and the signal is committed on this
plan's persistent final-delivery branch. The terminal archival PR is the only merge record.

STAGE: 3
PLAN: ayokoding-learning-path-16-skills-accounting-sharia-extension
LANDED_COURSE_IDS: sharia-accounting-and-aaoifi-standards, islamic-contract-modeling-for-systems, zakah-computation-and-reporting-for-systems, sukuk-and-islamic-capital-markets-accounting, sharia-ledger-system-architecture
UNBLOCKS_ERP_CAPABILITY: the Sharia-specific ERP stages delivering Sharia-compliant contract handling, Zakah/Sukuk reporting, and Sharia-ledger founding-architecture capability — and the whole sharia-accounting path, and the whole 24-course accounting corpus, are complete at this point
FINAL_DELIVERY_BRANCH: ayokoding-learning-path-16-skills-accounting-sharia-extension/final-delivery

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [x] [AI] All 5 Stage-3 course bodies exist, checkers green, every one carries a silent-failure
      section.
- [x] [AI] `sharia-accounting.json` grown to 24, passes `test:unit`.
- [x] [AI] **`conventional-accounting.json` byte-for-byte unchanged since plan 15's own merge** —
      `git diff --quiet -- "$MANIFEST_CA"` exits 0.
- [x] [AI] `sharia-accounting` landing states full path completeness; `conventional-accounting`'s
      landing is untouched.
- [x] [AI] `sharia-accounting`'s path-walk e2e walks all 24 courses; `conventional-accounting`'s own
      19-course walk assertion is unaffected.
- [x] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance:
      no PR, merge, deployment, or merge-commit record occurs before Phase 8.
- [x] [AI] `npm exec nx run ayokoding-www:build` exits 0.

> **Pause Safety**: `sharia-accounting` is a genuinely complete, shippable 24-course path, **walked
> end to end by §3.4's e2e**, and the whole 24-course corpus is authored. `conventional-accounting`
> is provably unchanged. Safe to stop indefinitely at this exact point. To resume: re-run
> `npm exec nx run ayokoding-www:test:unit` and confirm 0 exit before starting Phase 4.

---

## Phase 4: Section and app verification

> _Suggested executor: direct verification; `apps-ayokoding-www-facts-checker` and
> `apps-ayokoding-www-link-checker` for the corpus-wide sweep._

### 4.1 · Manifest integrity

- [x] [AI] `npm exec nx run ayokoding-www:test:unit` (both `$MTEST_CA` and `$MTEST_SA`) exits 0.
- [x] [AI] `checkManifestIntegrity` and `checkPrerequisiteConsistency` pass for `sharia-accounting`
      as a standalone sweep, assertion count matching 24.

### 4.2 · Ownership footprint check

- [x] [AI] Authorship-scoped commit-footprint check:
      `gh pr list --search "ayokoding-learning-path-16-skills-accounting-sharia-extension" --state merged --json number,files` and
      confirm every touched path under `apps/ayokoding-www/src/features/course-paths/manifests/` is
      `sharia-accounting.json` or its test — acceptance: `conventional-accounting.json` and its test
      appear in **zero** merged PR file lists for this plan; no path under `manifests/careers/`,
      `manifests/skills/conventional-erp.json`, or `manifests/skills/sharia-erp.json` appears; no
      `_index.md` under `paths/` appears; `<LANDING_CA>_index.md` appears in **zero** merged PR file
      lists for this plan.

### 4.3 · Shared-course non-duplication, final sweep

- [x] [AI] `for c in "${ACCT_SA_FULL[@]}"; do n=$(find "${COURSES}$c" -maxdepth 0 -type d | wc -l); [ "$n" -eq 1 ] || echo "DUPLICATE-OR-MISSING $c"; done | wc -l`
      returns **0** (all 24 checked).

### 4.4 · Licensing reading audit (A8) — the strictest posture in the corpus

- [x] [AI] For every file in `"${SPEC}"` (5 syllabi) **and** every `overview.md` under
      `"${COURSES}"` for `ACCT_P16` (5 course bodies) — 10 files total — read against the eleven
      safe-authoring rules, at the full four-body posture (IFRS Foundation, FASB, AAOIFI, IAI) —
      acceptance: zero violations found; any finding is fixed before this gate closes.
- [x] [AI] **Every citation resolves to a full URL** — same recipe as plan 14's own §4.4, scoped to
      this plan's own `"${SPEC}"`. Acceptance: empty output.

### 4.5 · Terminal-freeze assertion (repeat, final)

- [x] [AI] **`conventional-accounting.json` is unchanged since plan 15's own merge, re-confirmed** —
      `git diff --quiet -- "$MANIFEST_CA"` exits 0.
- [x] [AI] **`sharia-accounting.json` never grows past 24 from here** — recorded as this plan's own
      terminal-length assertion:
      `[ "$(grep -cE '^  - ' "$MANIFEST_SA")" -eq 24 ] && echo TERMINAL-OK || echo TERMINAL-FAIL`
      prints `TERMINAL-OK`.

### 4.6 · Scope-boundary sweep and no-unverified-claim sweep

- [x] [AI] `apps-ayokoding-www-facts-checker` run over all 5 course bodies and all 5 syllabi —
      acceptance: zero unmarked claims; OI-2's boundary is confirmed respected (no course states the
      riba doctrinal derivation as settled fact).

  **Gherkin (binds) →** "No unverified claim is published as fact, and the riba doctrinal basis
  stays open" (repeated at this later gate, over authored content this time)

  ```gherkin
  Scenario: No unverified claim is published as fact, and the riba doctrinal basis stays open
    Given the research seeding this plan marked the riba doctrinal basis as an open item
    When course twenty states any doctrinal position on profit and risk
    Then the practical consequence is stated (profit must arise from trade, leasing, partnership or service risk)
    And the specific doctrinal derivation is never asserted as settled fact
    And every item still marked Needs Verification when this plan's Phase 2 gate runs is registered with a reason
  ```

### Phase 4 Gate

> All checks below must pass before starting Phase 5.

- [x] [AI] 4.1 through 4.6 all clean, zero unresolved findings.
- [x] [AI] `npm exec nx run ayokoding-www:build` exits 0.
- [x] [AI] `npm run lint:md` exits 0 across the whole plan folder and the whole
      `apps/ayokoding-www` content touched.

> **Pause Safety**: the corpus is verified, licensing-clean, and scope-consistent; the terminal
> freeze on `conventional-accounting.json` holds; `sharia-accounting.json` holds at exactly 24. Safe
> to stop. To resume: re-run 4.1's `test:unit` and 4.5's freeze checks before starting Phase 5.

---

## Phase 5: Manual UI verification and FULL Rule-15 retest (sharia-accounting)

> _Suggested executor: Playwright MCP direct use; `web-exploratory-tester` /
> `web-usability-tester` / `web-design-tester` triad for the Rule-15 retest._
>
> **This plan runs the full Rule-15 three-tester retest, scoped to `sharia-accounting` only** —
> `conventional-accounting` was already fully retested at the end of plan 15.

### Manual UI Verification (Playwright MCP) — three breakpoints

- [x] [AI] Start dev server: `nx dev ayokoding-www`.
- [x] [AI] For EACH breakpoint (375 / 768 / 1280 px): navigate to
      `/en/learn/paths/skills/sharia-accounting` via `browser_navigate` + `browser_resize`.
- [x] [AI] Inspect DOM via `browser_snapshot` at every breakpoint — verify the arc promise, the full
      path-completeness statement, and the rendered 24-course list all appear.
- [x] [AI] Confirm `/en/learn/paths/skills/conventional-accounting` still renders its own unchanged
      19-course completeness state at one breakpoint (spot check, not a full re-verification).
- [x] [AI] Walk `sharia-accounting` end to end via prev/next controls (`browser_click`) — verify
      breadcrumb and `?path=` persistence at every step across all 24 courses.
- [x] [AI] Check for JS errors via `browser_console_messages` on the `sharia-accounting` landing and
      a sample of walked courses, at every breakpoint — zero errors.
- [x] [AI] Take one screenshot per breakpoint via `browser_take_screenshot`, saved to
      `evidence/phase-5-sharia-accounting-en-<breakpoint>px.png` — commit as evidence.
- [x] [AI] Document verification results in this checklist, referencing each committed screenshot.

### Rule-15 three-tester retest (`sharia-accounting` only)

All three run in `delivery` mode so their findings land in this checklist. **Fold every finding in
as its own checkbox**, prefixed with the issuing tester's id — `EWT-###` / `UWT-###` / `DWT-###`.

- [x] [AI] Dispatch `web-exploratory-tester` against `sharia-accounting`'s landing and full
      24-course walk — record every finding as an `EWT-###` checkbox.
- [x] [AI] Dispatch `web-usability-tester` against `sharia-accounting`'s landing — record every
      finding as a `UWT-###` checkbox.
- [x] [AI] Dispatch `web-design-tester` against `sharia-accounting`'s landing — record every finding
      as a `DWT-###` checkbox.
- [x] [AI] **Resolve every defect finding from the triad, at all severities.** A MEDIUM or LOW may
      be deferred **only** with explicit recorded permission naming the finding id and the reason.
      Re-run the affected tester(s) after fixing and confirm the finding no longer reproduces.

  **Gherkin (binds) →** "Sharia-accounting passes its full live-site retest"

  ```gherkin
  Scenario: Sharia-accounting passes its full live-site retest
    Given sharia-accounting is complete at twenty-four courses and deployed to production
    When the web-exploratory-tester, web-usability-tester, and web-design-tester triad runs against it
    Then every finding is folded in as an individually tickable, source-attributed checkbox
    And every defect finding is resolved or explicitly deferred with recorded permission before archival
  ```

### Phase 5 Gate

> All checks below must pass before starting Phase 6.

- [x] [AI] `sharia-accounting` landing walked end to end with zero JS console errors.
- [x] [AI] Screenshot evidence committed, all three breakpoints.
- [x] [AI] Rule-15 triad complete for `sharia-accounting`; every `EWT-###`/`UWT-###`/`DWT-###`
      finding folded in as a checkbox and **resolved at every severity**, or explicitly deferred
      with a recorded permission naming the finding id and reason.

> **Pause Safety**: `sharia-accounting` is manually verified end to end and has passed its full
> live-site retest. Safe to stop. To resume: re-open the landing via `browser_navigate` and re-check
> `browser_console_messages` before starting Phase 6.

---

## Phase 6: Final quality and archival-PR readiness

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
      no PR, merge, deployment, or merge-commit record occurs before Phase 8.
- [x] [AI] Reconcile the persistent branch non-destructively with current `origin/main`, then re-run
      every local quality gate; acceptance: all gates are green.
- [x] [AI] Preserve Phase 5's local UI evidence. Open no PR until Phase 8 has committed the archival
      move and index updates.

  **Gherkin (binds) →** "This plan's authored slice builds and validates green"

  ```gherkin
  Scenario: This plan's authored slice builds and validates green
    Given sharia-accounting.json holds twenty-four entries and all five of this plan's course bodies are authored
    When the app build, the affected test tiers, and the link and heading validators run
    Then the build and every affected tier succeed
    And manifest integrity and prerequisite consistency report zero violations
    And conventional-accounting.json is provably unchanged since plan 15's own merge
  ```

### Stage-3 signal, final confirmation

- [x] [AI] `grep -c '^STAGE: 3$' "${PLANDIR}delivery.md"` returns **1**, and the signal is committed
      on the persistent final-delivery branch.

### Phase 6 Gate

> All checks below must pass before starting Phase 7.

- [x] [AI] Stage-3 signal is present and committed on the persistent final-delivery branch.
- [x] [AI] All local quality gates and Phase 5 evidence are green; no PR exists before Phase 8.

> **Pause Safety**: this plan's authored corpus is verified and committed on the persistent
> final-delivery branch. Safe to stop. To resume: re-run the local quality gates before Phase 7.

---

## Phase 7: Knowledge Capture

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

### Phase 7 Gate

- [x] [AI] Every `learnings.md` entry is terminal, or the explicit "none" escape is recorded.
- [x] [AI] No code-homed learning landed inline in this plan's own commits/PRs.

> **Pause Safety**: `learnings.md` is fully triaged. Safe to stop. To resume: re-read
> `learnings.md` and confirm every entry is terminal.

---

## Phase 8: Plan Archival

### Sole PR integration (binding)

- [x] [AI] Archive this plan on its persistent final-delivery branch before review — acceptance: the archive move and index updates are committed in the same branch.
- [x] [AI] Open exactly one draft PR from that branch and run the secret scan, local quality checks, and PR quality-gate verification plus every local and CI gate — acceptance: the PR is the only PR for this plan.
- [x] [AI] Mark the PR ready, merge under the hardened preconditions, and deploy once — acceptance: the merge/deploy record is the plan's sole delivery record.

- [x] [AI] `git mv plans/in-progress/ayokoding-learning-path-16-skills-accounting-sharia-extension plans/done/$(date +%Y-%m-%d)__ayokoding-learning-path-16-skills-accounting-sharia-extension`
      (always from `plans/in-progress/` — Phase 0's promotion step is a mandatory precondition).
- [x] [AI] Update `plans/in-progress/README.md` — remove this
      plan's entry.
- [x] [AI] Update `plans/done/README.md` — add this plan's entry with its completion date.
- [x] [AI] Update `ayokoding-learning-path-18-skills-erp-enterprise-depth`'s
      own docs (if it exists at this point) to note this plan's merge and Stage-3 signal are now on
      `origin/main` — this is the **final** handoff of the three-plan accounting chain.
- [x] [AI] Commit the archival move to the persistent final-delivery branch before opening the only PR —
      `git commit -m "chore(plans): archive ayokoding-learning-path-16-skills-accounting-sharia-extension"`.
- [x] [AI] **Push the archival commit** — `git push origin HEAD` — acceptance: exits 0 and
      `git status -sb | grep -c 'ahead'` returns **0**.
- [x] [AI] **Monitor CI on the new head** — poll every 2 minutes. Acceptance: `status` is
      `completed` **and** `conclusion` is `success` for the run whose head SHA equals
      `git rev-parse HEAD`.
- [x] [AI] Re-confirm all five PR Merge Protocol preconditions still hold, then perform the `[AI]`
      merge. This is the terminal step of the plan, **and of the whole three-plan accounting
      chain**.

### Phase 8 Gate

- [x] [AI] `test -d plans/done/*__ayokoding-learning-path-16-skills-accounting-sharia-extension` exits 0.
- [x] [AI] `test -d plans/backlog/ayokoding-learning-path-16-skills-accounting-sharia-extension`
      and `test -d plans/in-progress/ayokoding-learning-path-16-skills-accounting-sharia-extension`
      both exit 1.
- [x] [AI] The archival commit is an ancestor of the merged PR head — verify with
      `gh pr list --head "$(git rev-parse --abbrev-ref HEAD)" --state merged --json number,mergeCommit`.
- [x] [AI] **Whole-chain completion check** — all three of plans 14, 15, and 16 have a merged entry
      under `plans/done/`, and `sharia-accounting.json` holds 24 entries while
      `conventional-accounting.json` holds 19, both on `origin/main`.

> **Pause Safety**: plan complete and archived. The whole three-plan accounting chain, and the
> whole 24-course, two-manifest corpus, is complete. Plan 18 may now build against both stage
> signals. Nothing further to resume.
