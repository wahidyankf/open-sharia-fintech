# Delivery Checklist — Skills Path: ERP Enterprise Depth (Stage B + Stage C)

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
> Git-mechanical steps (worktree create/remove, branch, commit, push, merge) are `[AI]`.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note. The sole PR opens only at the terminal archival boundary — see
> [Parallelization Model §Delivery Boundaries](#delivery-boundaries).

Three standing constraints govern every step below.

> **Cross-plan source of truth**: this plan's 15-course slice, the `ACCT_GATE_*` re-pointing, and the
> exact `courseOrder` growth positions are settled in
> [tech-docs.md](./tech-docs.md#the-erp-catalog-this-plans-15-course-slice). Transcribe them; do not
> re-derive them. Plan 17's own 15 syllabus files are **read-only** — this plan's steps never write to
> `../../done/2026-08-16__ayokoding-learning-path-17-skills-erp-foundations/syllabus/`.
>
> **The category ownership invariant (binding)**: this plan owns 15 new course bundles, its own
> `syllabus/`, and is explicitly authorized to **grow** `<CONVMAN>`, `<SHARMAN>`, `<MTEST_CE>`,
> `<MTEST_SE>`, `<CONVLANDING>`, `<SHARLANDING>`, the feature file, and its step-definition file (all
> created fresh by plan 17). It never writes an accounting file, a careers manifest, a component, a
> design asset, a structural `_index.md`, or a plan-17 Stage-A course body.
>
> **Id-shape rule (schema-owner ruling, inherited)**: every URL/id match below is a **full-string
> literal** (`grep -F -q`).

## One-PR delivery contract (binding, 2026-08-01)

This 15-course plan is one inseparable delivery unit: every Phase 1–9 change lands in **one
worktree, one branch, and exactly one draft PR**. Courses may still be authored, checked, and
committed in their dependency order, but no intermediate phase may push, open a PR, run the PR
merge, deploy, or record a merge SHA. Only Phase 9 opens the draft PR, after all
course work, verification, and Knowledge Capture are green; it includes the archival move to
`plans/done/`, then runs the secret scan, local quality checks, and PR quality-gate verification, CI verification, ready-for-review
transition, and the normal `[AI]` merge/deploy protocol. No earlier stage or delivery boundary opens
a PR.

The `worktrees/ayokoding-learning-path-18-skills-erp-enterprise-depth/` path below is this plan's
only worktree; no per-course, stage, phase, or closeout worktree is created.

## Worktree

Worktree path: `worktrees/ayokoding-learning-path-18-skills-erp-enterprise-depth/`

Provision this path exactly once with `claude --worktree ayokoding-learning-path-18-skills-erp-enterprise-depth` (or `git worktree add -b worktree/ayokoding-learning-path-18-skills-erp-enterprise-depth worktrees/ayokoding-learning-path-18-skills-erp-enterprise-depth origin/main` when provisioning manually). Both forms designate the same one worktree; never create a second path for a phase, course, or closeout.

Final-delivery branch: `ayokoding-learning-path-18-skills-erp-enterprise-depth/final-delivery`

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
`final-delivery` branch in the declared worktree. Phases before 9 must not push, open
a PR, start an external merge, deploy, or record an in-repository merge SHA. Phase 9 first
commits the archival move and index updates, then opens the sole draft PR, runs the secret scan, local quality checks, and PR quality-gate verification plus local and CI gates, marks it ready, merges under the hardened
preconditions, and deploys once.

## Content-only delivery safeguards

This plan produces content only and has exactly one final PR. It has no review-cycle requirement. Before pushing that PR:

- [x] [AI] Inspect the staged diff and confirm it contains no machine-secret value.
- [x] [AI] Use a scoped Conventional Commit (for example, `docs(plans): refresh course-preparation backlog`).
- [x] [AI] Run `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`; acceptance: exits 0 for the affected scope.
- [x] [AI] Push the single branch, then wait for `.github/workflows/pr-quality-gate.yml`; acceptance: the PR quality gate is green before merge.

## Depends-on

| Relation      | Plan (full folder name)                             | Nature                                                                                                                                                                                                                         |
| ------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **blockedBy** | `ayokoding-learning-path-17-skills-erp-foundations` | **Hard; sole direct execution prerequisite.** It must be fully merged and archived on `origin/main` before Phase 0. All earlier completion and repository-baseline facts are transitive context, not extra plan prerequisites. |

**Phase 0 start check:** `git ls-tree -r --name-only origin/main plans/done | rg -q "__ayokoding-learning-path-17-skills-erp-foundations/README\.md$"` exits 0. This is this plan's only plan-level start gate.

## Parallelization Model

Stage B's 12 courses have edges into plan 17's corpus and into each other (see
[tech-docs.md §Cross-plan prerequisite edges](./tech-docs.md#cross-plan-prerequisite-edges-into-plan-17)
and the in-plan edges noted there); courses with no edge between them author concurrently up to the
concurrency cap, courses with an edge serialize. Stage C's 3 courses serialize entirely (28 → 29, 28 → 30) and cannot start until Stage B's `multi-company-and-multi-currency-erp` (25) and
`erp-security-and-controls` (26) exist, since courses 28 and 30 cite them. The two manifests' TDD
growth cycles are parallelizable once their shared courses exist: `<CONVMAN>` stops growing at 27
while `<SHARMAN>` continues to 30, so after Stage B's §2.2 they no longer contend.

### Delivery Boundaries

| Phase(s) | Delivery unit                                               | Worktree / branch                                                         | PR opens                           |
| -------- | ----------------------------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------- |
| 0        | Setup and baseline                                          | No delivery worktree or PR                                                | no                                 |
| 1–8      | Intermediate authoring, verification, and Knowledge Capture | This plan's single declared worktree and persistent final-delivery branch | no — commit only                   |
| 9        | Final archival and integration                              | The same worktree and branch; archive before opening the PR               | yes — exactly once, after archival |

No phase may create an additional worktree or branch. The final phase is the only delivery boundary.

## Shell constants (reused across phases)

```bash
if [ -d "plans/backlog/ayokoding-learning-path-18-skills-erp-enterprise-depth" ]; then
  PLANDIR="plans/backlog/ayokoding-learning-path-18-skills-erp-enterprise-depth/"
elif [ -d "plans/in-progress/ayokoding-learning-path-18-skills-erp-enterprise-depth" ]; then
  PLANDIR="plans/in-progress/ayokoding-learning-path-18-skills-erp-enterprise-depth/"
else
  PLANDIR=$(find plans/done -maxdepth 1 -type d -name "*ayokoding-learning-path-18-skills-erp-enterprise-depth" | head -1)/
fi
echo "PLANDIR=$PLANDIR"
[ -d "$PLANDIR" ] || { echo "PLANDIR-UNRESOLVED — every sweep below would pass vacuously"; }

# Plan 17's PLANDIR — resolved the same way, needed only to confirm its 15 ids exist; never written to.
if [ -d "plans/backlog/ayokoding-learning-path-17-skills-erp-foundations" ]; then
  PLAN17DIR="plans/backlog/ayokoding-learning-path-17-skills-erp-foundations/"
elif [ -d "plans/in-progress/ayokoding-learning-path-17-skills-erp-foundations" ]; then
  PLAN17DIR="plans/in-progress/ayokoding-learning-path-17-skills-erp-foundations/"
else
  PLAN17DIR=$(find plans/done -maxdepth 1 -type d -name "*ayokoding-learning-path-17-skills-erp-foundations" | head -1)/
fi

COURSES="apps/ayokoding-www/content/en/learn/courses/"
PATHS="apps/ayokoding-www/content/en/learn/paths/"
MANIFESTS="apps/ayokoding-www/src/features/course-paths/manifests/"
CONVMAN="${MANIFESTS}skills/conventional-erp.json"
SHARMAN="${MANIFESTS}skills/sharia-erp.json"
MTEST_CE="${MANIFESTS}skills/conventional-erp-manifest.unit.test.ts"
MTEST_SE="${MANIFESTS}skills/sharia-erp-manifest.unit.test.ts"
CONVLANDING="${PATHS}skills/conventional-erp/_index.md"
SHARLANDING="${PATHS}skills/sharia-erp/_index.md"
SYL="${PLANDIR}syllabus/courses/"
SYL17="${PLAN17DIR}syllabus/courses/"

# Plan 17's 15 ids — read-only reference, used only for existence/collision checks, never authored here.
ERP_STAGE_A=(
  erp-foundations-and-history erp-conceptual-data-model erp-module-map-and-architecture
  erp-document-lifecycle-and-state-machines erp-posting-rules-and-account-determination
  erp-subledger-to-gl-architecture erp-fiscal-calendar-and-period-close
  erp-numbering-sequences-and-uom-conversion erp-audit-trail-and-change-tracking
  procure-to-pay-systems order-to-cash-systems erp-procurement-and-fulfillment-exceptions
  erp-bom-and-routing-architecture erp-extension-and-customization erp-integration-patterns
)

# This plan's 12 Stage B ids, checked against ACCT_GATE_B course ids
ERP_STAGE_B=(
  record-to-report-systems inventory-and-warehouse-management erp-inventory-costing-methods
  erp-inventory-integrity-and-concurrency production-planning-and-mrp demand-and-supply-planning
  erp-availability-and-reservations quality-management-and-inspection
  human-capital-management-and-hire-to-retire
  multi-company-and-multi-currency-erp erp-security-and-controls erp-analytics-and-reporting
)

# This plan's 3 Stage C ids, sharia-erp only, checked against ACCT_GATE_C course ids
ERP_STAGE_C=(
  sharia-compliant-erp-design islamic-contract-based-transaction-flows
  zakat-and-sharia-compliance-modules
)

ERP_THIS_PLAN=("${ERP_STAGE_B[@]}" "${ERP_STAGE_C[@]}")
ERP_ALL=("${ERP_STAGE_A[@]}" "${ERP_THIS_PLAN[@]}")

# Accounting gates — course ids unchanged from the retired source plan; only the historical repository context plan
# target is re-pointed (see tech-docs.md §Accounting-split gates, re-pointed).
ACCT_GATE_B=(
  financial-statements-and-close-cycle inventory-and-cogs-accounting
  payroll-and-tax-accounting-essentials consolidation-and-multi-entity-accounting
  audit-controls-and-compliance
)
ACCT_GATE_C=(
  islamic-contract-modeling-for-systems sharia-accounting-and-aaoifi-standards
)
```

## Phase 0: Environment Setup

- [x] [AI] **Promote out of `plans/backlog/` first — on the local `main` checkout, before any worktree exists.**
      Run `git mv plans/backlog/ayokoding-learning-path-18-skills-erp-enterprise-depth/ plans/in-progress/ayokoding-learning-path-18-skills-erp-enterprise-depth/`
      (a pure move — neither stage carries a date prefix), update `plans/backlog/README.md` and
      `plans/in-progress/README.md`, commit on the plan branch and include the move in the one final PR — acceptance:
      `git ls-tree -r --name-only origin/main -- plans/in-progress/ayokoding-learning-path-18-skills-erp-enterprise-depth/README.md | grep -c .`
      returns **1** and the same query against `plans/backlog/ayokoding-learning-path-18-skills-erp-enterprise-depth/README.md` returns **0**.
      Falsifiable both ways: before the push lands, the first query returns 0 and the second
      returns 1. Execution never runs out of `plans/backlog/` — this push is a mandatory
      precondition, not a courtesy. See
      [plan-execution → Execute Plan from Backlog](../../../repo-governance/workflows/plan/plan-execution/example-usage-and-iteration-example.md#execute-plan-from-backlog).
- [x] [AI] Plan 17 is archived on `origin/main` per [§Depends-on](#depends-on); repository baseline checks are informational — acceptance:
      empty output.
- [x] [AI] Install dependencies: `npm install`.
- [x] [AI] Run doctor to verify tooling: `npm run doctor -- --fix`.
- [x] [AI] Verify dev server starts: `nx dev ayokoding-www`.
- [x] [AI] Verify existing tests pass: `npm exec nx run ayokoding-www:test:quick`.
- [x] [AI] **Cardinality guard**:
      `[ "${#ERP_THIS_PLAN[@]}" -eq 15 ] && [ "${#ERP_ALL[@]}" -eq 30 ] && [ "${#ACCT_GATE_B[@]}" -eq 5 ] && [ "${#ACCT_GATE_C[@]}" -eq 2 ] && echo GUARD-OK || echo GUARD-FAIL`
      — acceptance: `GUARD-OK`.
- [x] [AI] Verify plan 17's 15 ids actually exist under `<COURSES>` on `origin/main` (the historical repository context
      check above confirms the plan merged; this confirms its content landed):
      `for id in "${ERP_STAGE_A[@]}"; do test -d "${COURSES}${id}" || echo "MISSING-FROM-PLAN-17: $id"; done | grep -q . && echo FAIL || echo PASS`
      — acceptance: `PASS`.
- [x] [AI] Verify both manifests exist at exactly 15 ids (plan 17's published state):
      `grep -cE '^  - ' "${CONVMAN}"` and `grep -cE '^  - ' "${SHARMAN}"` both print `15`.
- [x] [AI] Verify no id in `ERP_THIS_PLAN` already exists under `<COURSES>`:
      `for id in "${ERP_THIS_PLAN[@]}"; do test -d "${COURSES}${id}" && echo "COLLISION: $id"; done | grep -q . && echo FAIL || echo PASS`
      — acceptance: `PASS`.
- [x] [AI] Verify no id in `ERP_ALL` is a substring of another:
      `for a in "${ERP_ALL[@]}"; do for b in "${ERP_ALL[@]}"; do [ "$a" != "$b" ] && case "$b" in *"$a"*) echo "SUBSTRING: $a ⊂ $b";; esac; done; done | grep -q . && echo FAIL || echo PASS`
      — acceptance: `PASS`. **Control probe**: append a known-colliding id to a scratch copy and
      re-run — it must print `FAIL`.
- [x] [AI] Verify no id in `ERP_THIS_PLAN` collides with an accounting id:
      `comm -12 <(printf '%s\n' "${ERP_THIS_PLAN[@]}" | sort) <(printf '%s\n' "${ACCT_GATE_B[@]}" "${ACCT_GATE_C[@]}" | sort)`
      — acceptance: empty output.

### Phase 0 Gate

- [x] [AI] All checks above pass; `npm exec nx run ayokoding-www:test:quick` is green on a clean tree.

> **Pause Safety**: no plan file yet modified. Safe to stop. To resume: re-run
> `npm exec nx run ayokoding-www:test:quick`.

## Phase 1: Syllabus Authoring and Verification

Authoring precedes confirmation, and confirmation is coverage-only (`A12`). Not gated on any
accounting plan — domain reasoning for these 15 courses needs no accounting course to exist yet.

### 1.1 — Author all 15 syllabus specs (Stage B's 12 + Stage C's 3)

- [x] [AI] Create `${PLANDIR}syllabus/README.md`, `${SYL}README.md`, and all 15 `<SYL><id>.md` files
      per the [Learning-Plan Syllabus Convention](../../../repo-governance/conventions/structure/learning-plan-syllabus/copy-paste-course-template.md#copy-paste-course-template).
      Every syllabus file citing a plan-17 course id (per
      [tech-docs.md §Cross-plan prerequisite edges](./tech-docs.md#cross-plan-prerequisite-edges-into-plan-17))
      links to `../../../done/2026-08-16__ayokoding-learning-path-17-skills-erp-foundations/syllabus/courses/<id>.md`
      rather than restating that file's content. Verify:

  ```bash
  test -f "${PLANDIR}syllabus/README.md" || echo "MISSING: syllabus/README.md"
  test -f "${SYL}README.md" || echo "MISSING: syllabus/courses/README.md"
  for id in "${ERP_THIS_PLAN[@]}"; do test -f "${SYL}${id}.md" || echo "MISSING: $id"; done
  ```

  Acceptance: **empty output**. Guard first —
  `[ "${#ERP_THIS_PLAN[@]}" -eq 15 ] && echo GUARD-OK` must print `GUARD-OK`.

- [x] [AI] Verify every syllabus file citing a plan-17 id actually links into plan 17's corpus (not a
      copy):
      `for id in record-to-report-systems inventory-and-warehouse-management production-planning-and-mrp quality-management-and-inspection human-capital-management-and-hire-to-retire erp-security-and-controls islamic-contract-based-transaction-flows; do grep -qF "ayokoding-learning-path-17-skills-erp-foundations/syllabus/courses/" "${SYL}${id}.md" || echo "MISSING-CROSS-LINK: $id"; done | grep -q . && echo FAIL || echo PASS`
      — acceptance: `PASS`.
- [x] [AI] Author `${PLANDIR}syllabus/paths/README.md`,
      `${PLANDIR}syllabus/paths/manifest-skills-conventional-erp.md`, and
      `${PLANDIR}syllabus/paths/manifest-skills-sharia-erp.md` — full 27/30-id orderings, positions
      1-15 referencing plan 17's ids by link, positions 16-30 this plan's own courses. Verify:

  ```bash
  SYLPATHS="${PLANDIR}syllabus/paths/"
  conv=$(grep -cE '^[0-9]+\. `' "${SYLPATHS}manifest-skills-conventional-erp.md")
  shar=$(grep -cE '^[0-9]+\. `' "${SYLPATHS}manifest-skills-sharia-erp.md")
  echo "conv=$conv shar=$shar"
  [ "$conv" -eq 27 ] && [ "$shar" -eq 30 ] && echo PASS || echo FAIL
  ```

  Acceptance: prints `conv=27 shar=30` then `PASS`.

### 1.2 — The A4 verification pass before any spec asserts a fact

- [x] [AI] **Cardinality guard first**:
      `[ "$(find "${SYL}" -maxdepth 1 -name '*.md' ! -name 'README.md' | wc -l)" -eq 15 ] && echo GUARD-OK || echo GUARD-FAIL`
      — acceptance: `GUARD-OK`.
- [x] [AI] For every syllabus's Accuracy notes section, confirm every marker is current and no
      `[Unverified]`/`[Needs Verification]` claim is restated as fact:
      `for f in $(find "${SYL}" -maxdepth 1 -name '*.md' ! -name 'README.md'); do grep -qE '\[(Verified|Unverified|Needs Verification|Judgment call)\]' "$f" && continue; grep -qF 'has not yet run' "$f" && continue; echo "NO-MARKER-AND-NOT-PENDING: $f"; done | grep -c .`
      returns **0**. Do **not** use `grep -L`. **Control probe**: append `x` to both patterns and
      re-run — the count must jump to 15.

### 1.2a — `web-researcher` confirmation pass (`A12`, coverage-only)

- [x] [AI] Dispatch `web-researcher` once per syllabus (15 dispatches) asking exactly: "does
      APICS/ASCM's CPIM or CSCP topic outline (planning/operations content) or the named open-source
      system's own published module structure (architecture/module-map content, nominative reference
      only) suggest a topic this syllabus's module list omits, or include a topic the field does not
      recognise?" — never "how should these modules be ordered".
- [x] [AI] For each finding, add the missing topic in this plan's own words, citing the confirming
      body nominatively — never quoting or reproducing its text.
- [x] [AI] Resolve every `[Needs Verification]` tag left in a syllabus's Concepts/module list.
- [x] [AI] **Re-verify the two open Sharia-specific items** (PSAK-numbering, AAOIFI/PSAK/MASB
      jurisdictional-model table) before Phase 3 begins — dispatch `web-researcher` against AAOIFI's
      and IAI's own published standards indexes; update `sharia-compliant-erp-design.md`'s Accuracy
      notes with the verified answer or an explicit `[Needs Verification]` carry-forward.

### Phase 1 Gate

- [x] [AI] `npm run lint:md` is green on all `syllabus/**` files.
- [x] [AI] Every syllabus file's Accuracy notes section reflects the Phase 1.2/1.2a pass results.
- [x] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance:
      no PR, merge, deployment, or merge-commit record occurs before Phase 9.

> **Pause Safety**: `syllabus/` is fully authored and confirmed; no `<COURSES>` entry yet created and
> both manifests remain at plan 17's 15-id state. Safe to stop. To resume: re-derive `PLANDIR`/`SYL`
> from the Shell constants block above, then
> `test -f "${SYL}erp-analytics-and-reporting.md" && echo READY`.

## Phase 2: Stage B — Conventional Enterprise Depth

12 courses, with the required accounting course ids verified on `origin/main`. `conventional-erp` reaches its terminal
27-id state at the end of this phase.

### 2.0 — Gate check

- [x] [AI] Mechanical id-level availability check:
      `for id in "${ACCT_GATE_B[@]}"; do git fetch origin main -q; git show "origin/main:${COURSES}${id}/_index.md" >/dev/null 2>&1 || echo "WAITING: $id"; done | grep -q . && echo WAIT || echo READY` —
      if `WAIT`, poll every 2 minutes; do not begin 2.1 until `READY`.

### 2.1 — Author all 12 Stage B course bodies (maker-checker-fixer, per format)

For each `id` in `ERP_STAGE_B`, following the seven-step NEW-course authoring cycle (accuracy
pre-verify → skeleton → learning track → drilling track → checkers → fixers → re-verify — same cycle
as plan 17's own
[§2.1](../../done/2026-08-16__ayokoding-learning-path-17-skills-erp-foundations/delivery.md#21--author-all-15-stage-a-course-bodies-maker-checker-fixer-per-format)),
transcribing from `<SYL>${id}.md` (this plan's own corpus) or, where the course's frontmatter cites a
plan-17 id, from plan 17's `<SYL17>${id}.md` for the cited concept only (never copying the file
wholesale):

- [x] [AI] Accuracy pre-verify: re-check every marker in `<SYL>${id}.md`'s Accuracy notes is current —
      acceptance: every marker re-confirmed or updated, and zero `[Unverified]`/`[Needs Verification]`
      claims restated as settled fact elsewhere in `<SYL>${id}.md`.
- [x] [AI] Skeleton: create `<COURSES>${id}/_index.md` with frontmatter (`title`, `format`,
      `prerequisites: [...]` transcribed verbatim from `tech-docs.md`'s catalog table) and the section
      scaffold — acceptance:
      `test -f "${COURSES}${id}/_index.md" && grep -qE '^(title|format|prerequisites):' "${COURSES}${id}/_index.md" && echo PASS`
      prints `PASS`, confirming the file exists and all three frontmatter fields are present.
- [x] [AI] Learning track: dispatch `apps-ayokoding-www-annotated-concept-maker` (Annotated-concept
      ids) or `apps-ayokoding-www-by-example-maker` (By Example ids), transcribing every `co-NN` from
      the syllabus — acceptance:
      `grep -oE 'co-[0-9]+' "${COURSES}${id}/_index.md" | sort -u | wc -l` equals
      `grep -oE 'co-[0-9]+' "${SYL}${id}.md" | sort -u | wc -l` and is **at least 8**.
- [x] [AI] Drilling track: for By Example ids, author worked examples from the syllabus's `ex-NN` list
      (prose worked scenarios, never runnable code standing up a system — A6). For Annotated-concept
      ids, author equivalent worked-scenario drills — acceptance: for By Example ids,
      `grep -oE 'ex-[0-9]+' "${COURSES}${id}/_index.md" | sort -u | wc -l` equals the syllabus count;
      for Annotated-concept ids, every drill traces to a `co-NN` already present.
- [x] [AI] Checkers: dispatch `apps-ayokoding-www-annotated-concept-checker` or
      `apps-ayokoding-www-by-example-checker` plus `apps-ayokoding-www-facts-checker` and
      `apps-ayokoding-www-link-checker` — acceptance: zero CRITICAL and zero HIGH findings. For the
      two scope-boundary-risk ids in this stage (`erp-security-and-controls`,
      `erp-analytics-and-reporting`), additionally confirm the scope-boundary self-check worked
      example is present and reviewed by `apps-ayokoding-www-facts-checker`.
- [x] [AI] Fixers: dispatch `apps-ayokoding-www-general-fixer`-family agents for every finding —
      acceptance: zero unresolved CRITICAL/HIGH findings on re-check.
- [x] [AI] Re-verify: `test -d "${COURSES}${id}" && test -f "${COURSES}${id}/_index.md" && echo PASS`
      — acceptance: prints `PASS` for every id in `ERP_STAGE_B`.

- [x] [AI] `for id in "${ERP_STAGE_B[@]}"; do test -d "${COURSES}${id}" || echo "MISSING: $id"; done | grep -q . && echo FAIL || echo PASS` prints `PASS`.

### 2.2 — TDD: grow both manifests to 27 ids

**Gherkin (binds) →** "the shared 27 courses are identical bodies referenced from both manifests"

```gherkin
Scenario: the shared 27 courses are identical bodies referenced from both manifests
  Given a course id present in both "skills/conventional-erp" and "skills/sharia-erp" courseOrder
  When the reader visits that course under either path context
  Then the rendered body content is byte-identical
  And no second copy of the course file exists on disk
```

- [x] [AI] **RED** — Extend `<MTEST_CE>` and `<MTEST_SE>` asserting each manifest contains all 27
      shared ids (plan 17's 15 plus this plan's 12, at the insertion positions in
      [tech-docs.md §courseOrder arrays](./tech-docs.md#courseorder-arrays-at-each-growth-boundary)),
      with every already-published id's relative order unchanged — run
      `npm exec nx run ayokoding-www:test:unit -- conventional-erp-manifest sharia-erp-manifest` and verify
      both **fail**.
- [x] [AI] **GREEN** — Grow `<CONVMAN>` and `<SHARMAN>` to 27 ids each — run the same command and
      verify both **pass**.
- [x] [AI] **REFACTOR** — Re-run `checkManifestIntegrity`/`checkPrerequisiteConsistency` against both;
      verify zero violations, including the hard edge (`record-to-report-systems` requiring
      `financial-statements-and-close-cycle` to exist under `<COURSES>` on `origin/main`).

### 2.3 — Deferral-check assertion (both directions)

- [x] [AI] Confirm the **before** half: `grep -F -q 'record-to-report-systems' <(git show HEAD~1:"${CONVMAN}")`
      against the pre-growth commit and verify it **fails**.
- [x] [AI] Confirm the **after** half: `grep -F -q 'record-to-report-systems' "${CONVMAN}"` **passes**.

### 2.4 — Landing update: Dangerous 2 and Dangerous 3 boundaries

- [x] [AI] Update `<CONVLANDING>` and `<SHARLANDING>` content to show the Dangerous 2 boundary
      (course 16) and, for `<CONVLANDING>`, the terminal Dangerous 3 boundary (course 27, "ENDS
      HERE") — acceptance: `grep -q 'Dangerous 2' "${CONVLANDING}" && grep -q 'Dangerous 2' "${SHARLANDING}" && grep -qF 'ENDS HERE' "${CONVLANDING}" && echo PASS`
      prints `PASS`.
- [x] [AI] Run `npm exec nx run ayokoding-www:generate-indexes`; do not manually populate `<COURSES>_index.md` (27 generated entries cumulative with plan 17's 15) —
      acceptance:
      `for id in "${ERP_STAGE_A[@]}" "${ERP_STAGE_B[@]}"; do grep -qF "(/en/learn/courses/${id})" "${COURSES}_index.md" || echo "MISSING: $id"; done | grep -q . && echo FAIL || echo PASS`
      prints `PASS`, confirming all 27 cumulative ids have a catalog entry.

### 2.5 — TDD: extend coverage to the Dangerous 2/3 boundaries

**Gherkin (binds) →** "conventional-erp landing renders with its full terminal course count"

```gherkin
Scenario: conventional-erp landing renders with its full terminal course count
  Given the reader navigates to "/en/learn/paths/skills/conventional-erp"
  When the landing page loads
  Then the landing renders 27 courses in courseOrder order
  And the landing displays the Dangerous 1, Dangerous 2, and Dangerous 3 boundaries
  And the landing states "ENDS HERE" at Dangerous 3
```

- [x] [AI] **RED** — add the `conventional-erp landing renders with its full terminal course count`
      scenario above to
      `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/course-paths/skills-erp-paths.feature`
      (created by plan 17, extended here), then extend
      `apps/ayokoding-www-fe-e2e/src/steps/skills-erp-paths.steps.ts` (created by plan 17) to assert
      the Dangerous 2 boundary on both landings and the terminal Dangerous 3 / "ENDS HERE" statement
      on `<CONVLANDING>` — command: `npm exec nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: the new
      scenario is picked up and its assertions **fail**.
- [x] [AI] **GREEN** — implement the step bindings against the grown landing content (from §2.4) —
      command: `npm exec nx run ayokoding-www:specs:behavior:coverage && npm exec nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: both exit 0.
- [x] [AI] **REFACTOR** — parameterize the helper on expected boundary count so §3.5 extends it
      without duplicating assertions — command: `npm exec nx run ayokoding-www-fe-e2e:test:e2e` — acceptance:
      exits 0, scenario count unchanged.

### Phase 2 Gate

- [x] [AI] `npm exec nx run ayokoding-www:test:unit -- conventional-erp-manifest sharia-erp-manifest` green.
- [x] [AI] `npm exec nx run ayokoding-www-fe-e2e:test:e2e` green for the extended feature file.
- [x] [AI] `npm exec nx run ayokoding-www:typecheck`, `:lint`, `:test:quick` all green.
- [x] [AI] `<CONVMAN>` has exactly 27 `courseOrder` entries; `<SHARMAN>` has exactly 27 (Stage C not
      yet grown) — `grep -cE '^  - ' "${CONVMAN}"` prints `27`.
- [x] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance:
      no PR, merge, deployment, or merge-commit record occurs before Phase 9.

> **Pause Safety**: `conventional-erp` is terminal (27/27); `sharia-erp` is mid-growth (27/30). Safe
> to stop. To resume: `grep -cE '^  - ' "${SHARMAN}"` and confirm it reads `27`.

## Phase 3: Stage C — Sharia-Compliant Design

3 courses, `sharia-erp` only, with the required accounting course ids verified on `origin/main`.

### 3.0 — Gate check

- [x] [AI] Mechanical id-level gate check:
      `for id in "${ACCT_GATE_C[@]}"; do git fetch origin main -q; git show "origin/main:${COURSES}${id}/_index.md" >/dev/null 2>&1 || echo "WAITING: $id"; done | grep -q . && echo WAIT || echo READY` —
      poll every 2 minutes if `WAIT`.
- [x] [AI] Complete Phase 1.2a's deferred re-verification of the PSAK-numbering and jurisdictional-model
      open items before authoring begins, if not already resolved.

### 3.1 — Author all 3 Stage C course bodies (maker-checker-fixer, per format)

For each `id` in `ERP_STAGE_C`, following the same seven-step NEW-course authoring cycle as §2.1
above (accuracy pre-verify → skeleton → learning track → drilling track → checkers → fixers →
re-verify — same cycle as plan 17's own
[§2.1](../../done/2026-08-16__ayokoding-learning-path-17-skills-erp-foundations/delivery.md#21--author-all-15-stage-a-course-bodies-maker-checker-fixer-per-format)),
transcribing from `<SYL>${id}.md`. Every claim in the jurisdictional-model table carries its A4
marker into the course body verbatim:

- [x] [AI] Accuracy pre-verify: re-check every marker in `<SYL>${id}.md`'s Accuracy notes is current,
      including the jurisdictional-model A4 markers — acceptance: every marker re-confirmed or
      updated, and zero `[Unverified]`/`[Needs Verification]` claims restated as settled fact
      elsewhere in `<SYL>${id}.md`.
- [x] [AI] Skeleton: create `<COURSES>${id}/_index.md` with frontmatter (`title`, `format`,
      `prerequisites: [...]` transcribed verbatim from `tech-docs.md`'s catalog table) and the section
      scaffold — acceptance:
      `test -f "${COURSES}${id}/_index.md" && grep -qE '^(title|format|prerequisites):' "${COURSES}${id}/_index.md" && echo PASS`
      prints `PASS`, confirming the file exists and all three frontmatter fields are present.
- [x] [AI] Learning track: dispatch `apps-ayokoding-www-annotated-concept-maker` (Annotated-concept
      ids) or `apps-ayokoding-www-by-example-maker` (By Example ids), transcribing every `co-NN` from
      the syllabus, carrying each A4 jurisdictional-model marker verbatim — acceptance:
      `grep -oE 'co-[0-9]+' "${COURSES}${id}/_index.md" | sort -u | wc -l` equals
      `grep -oE 'co-[0-9]+' "${SYL}${id}.md" | sort -u | wc -l` and is **at least 8**.
- [x] [AI] Drilling track: for By Example ids, author worked examples from the syllabus's `ex-NN` list
      (prose worked scenarios, never runnable code standing up a system — A6). For Annotated-concept
      ids, author equivalent worked-scenario drills — acceptance: for By Example ids,
      `grep -oE 'ex-[0-9]+' "${COURSES}${id}/_index.md" | sort -u | wc -l` equals the syllabus count;
      for Annotated-concept ids, every drill traces to a `co-NN` already present.
- [x] [AI] Checkers: dispatch `apps-ayokoding-www-annotated-concept-checker` or
      `apps-ayokoding-www-by-example-checker` plus `apps-ayokoding-www-facts-checker` and
      `apps-ayokoding-www-link-checker` — acceptance: zero CRITICAL and zero HIGH findings, and
      confirm no course body restates the riba doctrinal basis (`OI-2`) or a specific PPSAK/PSAK
      ratification date as settled fact (per the twelfth safe-authoring rule).
- [x] [AI] Fixers: dispatch `apps-ayokoding-www-general-fixer`-family agents for every finding —
      acceptance: zero unresolved CRITICAL/HIGH findings on re-check.
- [x] [AI] Re-verify: `test -d "${COURSES}${id}" && test -f "${COURSES}${id}/_index.md" && echo PASS`
      — acceptance: prints `PASS` for every id in `ERP_STAGE_C`.

- [x] [AI] `for id in "${ERP_STAGE_C[@]}"; do test -d "${COURSES}${id}" || echo "MISSING: $id"; done | grep -q . && echo FAIL || echo PASS` prints `PASS`.

### 3.2 — TDD: grow `<SHARMAN>` to 30 ids

**Gherkin (binds) →** "sharia-erp manifest validates against the PathManifest schema at its terminal 30 ids"

```gherkin
Scenario: sharia-erp manifest validates against the PathManifest schema at its terminal 30 ids
  Given the file "manifests/skills/sharia-erp.json"
  When the manifest is loaded and validated
  Then it parses against the PathManifest zod schema
  And its pathId equals "skills/sharia-erp"
  And its courseOrder contains exactly 30 unique course ids
  And its courseOrder position 27 equals "erp-analytics-and-reporting"
  And its courseOrder positions 28 to 30 are the 3 Sharia-exclusive ids in catalog order
  And its final courseOrder entry equals "zakat-and-sharia-compliance-modules"
```

- [x] [AI] **RED** — Extend `<MTEST_SE>` **only** (never `<MTEST_CE>`) asserting `<SHARMAN>` contains
      all 30 ids at the positions in
      [tech-docs.md §courseOrder arrays](./tech-docs.md#courseorder-arrays-at-each-growth-boundary),
      and confirm `<MTEST_CE>`'s existing assertions are untouched — run
      `npm exec nx run ayokoding-www:test:unit -- sharia-erp-manifest` and verify it **fails**. Assert the
      terminal id explicitly, not just the set.
- [x] [AI] **GREEN** — Grow `<SHARMAN>` to 30 ids — run the same command and verify it **passes**.
- [x] [AI] **REFACTOR** — Re-run integrity checks on `<SHARMAN>` only; verify zero violations. Confirm
      `npm exec nx run ayokoding-www:test:unit -- conventional-erp-manifest` is still green and unmodified.

### 3.3 — Deferral-check assertion (both directions)

- [x] [AI] Before/after check for `zakat-and-sharia-compliance-modules`, mirroring 2.3's pattern
      against `<SHARMAN>`.

### 3.4 — Landing update: Dangerous 4 boundary and the terminal L-5 statement

- [x] [AI] Update `<SHARLANDING>` to show the terminal Dangerous 4 boundary (course 30, "ENDS HERE")
      and to replace plan 17's "identical to conventional-erp" framing with the terminal "covers all
      the basics" statement (DD-9 in this plan's tech-docs.md) — acceptance:
      `grep -qF 'ENDS HERE' "${SHARLANDING}" && grep -qF 'covers all the basics' "${SHARLANDING}" && echo PASS`
      prints `PASS`.
- [x] [AI] Run `npm exec nx run ayokoding-www:generate-indexes`; do not manually populate `<COURSES>_index.md` (30 generated entries cumulative across both
      manifests) — acceptance:
      `for id in "${ERP_STAGE_C[@]}"; do grep -qF "(/en/learn/courses/${id})" "${COURSES}_index.md" || echo "MISSING: $id"; done | grep -q . && echo FAIL || echo PASS`
      prints `PASS`, confirming all 3 Stage C ids have a catalog entry.

### 3.5 — TDD: extend coverage to the terminal Dangerous 4 boundary

**Gherkin (binds) →** "sharia-erp landing renders with its full terminal course count and states it covers the basics"

```gherkin
Scenario: sharia-erp landing renders with its full terminal course count and states it covers the basics
  Given the reader navigates to "/en/learn/paths/skills/sharia-erp"
  When the landing page loads
  Then the landing renders 30 courses in courseOrder order
  And the landing displays the Dangerous 1 through Dangerous 4 boundaries
  And the landing states explicitly that the path covers all the basics without requiring
    "conventional-erp" first
```

- [x] [AI] **RED** — add the `sharia-erp landing renders with its full terminal course count and
states it covers the basics` scenario above to
      `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/course-paths/skills-erp-paths.feature`,
      then extend `apps/ayokoding-www-fe-e2e/src/steps/skills-erp-paths.steps.ts` to assert the
      Dangerous 4 boundary and the terminal "ENDS HERE" / "covers all the basics" statement on
      `<SHARLANDING>` **only** — command: `npm exec nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: the new
      scenario is picked up and its assertion **fails**.
- [x] [AI] **GREEN** — implement the step bindings against the grown `<SHARLANDING>` content (from
      §3.4) — command:
      `npm exec nx run ayokoding-www:specs:behavior:coverage && npm exec nx run ayokoding-www-fe-e2e:test:e2e` —
      acceptance: both exit 0.
- [x] [AI] **REFACTOR** — consolidate the four boundary assertions (Dangerous 1-4) into a single
      table-driven helper — command: `npm exec nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: exits 0,
      scenario count unchanged; this is the final growth of `skills-erp-paths.steps.ts`.

### Phase 3 Gate

- [x] [AI] All Phase 2 Gate checks re-run and still green; `<CONVMAN>` unchanged at 27.
- [x] [AI] `grep -cE '^  - ' "${SHARMAN}"` prints `30`.
- [x] [AI] Commit this phase's checked artifacts on the persistent final-delivery branch — acceptance:
      no PR, merge, deployment, or merge-commit record occurs before Phase 9.

> **Pause Safety**: both paths are terminal (27/27 and 30/30) and verified on the persistent branch.
> Safe to stop. To resume: `grep -cE '^  - ' "${SHARMAN}"` reads `30`.

## Phase 4: Cross-Path Integrity and Spec Coverage Verification

- [x] [AI] Reconcile the declared worktree non-destructively with current `origin/main` while staying
      on the persistent final-delivery branch. Any fix remains on that branch; no additional branch or
      PR is created.
- [x] [AI] Run `checkManifestIntegrity` and `checkPrerequisiteConsistency` against **both** final
      manifests together — acceptance: zero violations reported by each.
- [x] [AI] **A11 — one body, two references, across both plans.** Verify no shared course id has a
      second copy anywhere under `<COURSES>`:

  ```bash
  for id in "${ERP_ALL[@]}"; do
    n=$(find "${COURSES}" -type d -name "$id" | grep -c .)
    [ "$n" -eq 1 ] || echo "EXPECTED-1-GOT-$n: $id"
  done
  ```

  Acceptance: **empty output**. Guard first —
  `[ "${#ERP_ALL[@]}" -eq 30 ] && echo GUARD-OK` must print `GUARD-OK`. **Control probe**:
  `mkdir -p "${COURSES}sharia-erp/erp-foundations-and-history"` in a scratch checkout and re-run — it
  must print `EXPECTED-1-GOT-2`. Remove it afterwards.

- [x] [AI] `npm exec nx run ayokoding-www:specs:behavior:coverage` reports 100% for `skills-erp-paths.feature`.
- [x] [AI] `npm exec nx run ayokoding-www:test:unit` **and** `npm exec nx run ayokoding-www-fe-e2e:test:e2e` both green
      for the full 30-course corpus.

### Phase 4 Gate

- [x] [AI] All checks above pass. Commit any residual fixes to the persistent final-delivery branch;
      nothing opens or merges before Phase 9.

> **Pause Safety**: the full corpus is integrity-verified. Safe to stop. To resume: re-run
> `npm exec nx run ayokoding-www:specs:behavior:coverage`.

## Phase 5: Section and App Verification (Licensing and Trademark)

- [x] [AI] **No vendor name in any course id, path id, or product name**:
      `grep -riE 'sap|oracle|netsuite|erpnext|odoo' <(printf '%s\n' "${ERP_THIS_PLAN[@]}" skills/conventional-erp skills/sharia-erp)` —
      acceptance: **empty output**.
- [x] [AI] **No verbatim AAOIFI standards-text reproduction** (Stage C addendum): for each of the FAS
      numbers named in
      [tech-docs.md §AAOIFI FAS verbatim-reproduction rule](./tech-docs.md#aaoifi-fas-verbatim-reproduction-rule)
      (FAS 3, 4, 7, 9, 10, 28, 32, 33, 34), confirm no course body in `ERP_STAGE_C` contains a
      100+-character verbatim span matching AAOIFI's own published standard text — dispatch
      `web-researcher` to diff against the official AAOIFI standard for any course quoting a FAS
      number; acceptance: "no verbatim match found" for every quoted number, or the offending span is
      rewritten before this clause is marked complete.
- [x] [AI] **No screenshot of proprietary software** in this plan's 15 course bundles:
      `for id in "${ERP_THIS_PLAN[@]}"; do find "${COURSES}${id}" \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.gif' -o -iname '*.webp' \); done | grep -c .`
      — acceptance: returns **0**. Guard first:
      `[ "$(for id in "${ERP_THIS_PLAN[@]}"; do test -d "${COURSES}${id}" && echo x; done | grep -c .)" -eq 15 ] && echo GUARD-OK || echo GUARD-FAIL`
      must print `GUARD-OK`.
- [x] [AI] **No chart of accounts lifted from a reference implementation**: `apps-ayokoding-www-facts-checker`
      reviews every worked example's dataset in every By-Example course under `ERP_THIS_PLAN`;
      acceptance: zero matches.
- [x] [AI] **Every syllabus's Scope note ends with the inherited licence tag**:
      `for id in "${ERP_THIS_PLAN[@]}"; do grep -qF 'License-aware' "${SYL}${id}.md" || echo "MISSING TAG: $id"; done | grep -q . && echo FAIL || echo PASS` —
      acceptance: `PASS`.
- [x] [AI] Read both layers (15 syllabi + 15 course bodies, 30 files total, this plan's own) against
      the eleven safe-authoring rules plus the Stage C twelfth rule in
      [tech-docs §Licensing and IP Compliance](./tech-docs.md#licensing-and-ip-compliance--stage-c-addendum-a8):
      confirm none reproduces a standard's clause text, mirrors a commercial curriculum's sequence,
      pastes copyleft code, lifts a reference implementation's demo dataset, states a PPSAK
      ratification date, or uses a vendor name in a title. Cardinality guard first:
      `[ "$(find "${SYL}" -maxdepth 1 -name '*.md' ! -name 'README.md' | wc -l)" -eq 15 ] && echo GUARD-OK || echo GUARD-FAIL`
      must print `GUARD-OK` — acceptance: `GUARD-OK`, then zero violations across all 30 files.

### Phase 5 Gate

- [x] [AI] All six clauses above pass. Commit any residual fixes to the persistent final-delivery
      branch; nothing opens or merges before Phase 9.

> **Pause Safety**: licensing/trademark posture (including the Sharia addendum) is verified across
> this plan's corpus. Safe to stop. To resume: re-run the six clauses above.

## Phase 6: Manual UI Retest (Rule 15)

Per [tech-docs.md §R9 gate posture](./tech-docs.md#r9-gate-posture-declared-explicitly), this plan is
UI-gate-exempt. This is this plan's own retest at its terminal checkpoint — distinct from and not
redundant with plan 17's own Stage A retest (DD-8).

- [x] [AI] Dispatch `web-exploratory-tester` (spec-aware) against both live landings at their terminal
      state (`/en/learn/paths/skills/conventional-erp`, `/en/learn/paths/skills/sharia-erp`) in
      `delivery` mode — verify zero CRITICAL/HIGH findings.
- [x] [AI] Dispatch `web-usability-tester` (spec-blind) against both landings — verify zero
      CRITICAL/HIGH findings.
- [x] [AI] Dispatch `web-design-tester` (design-aware) against both landings — verify zero
      CRITICAL/HIGH findings, and specifically confirm the four-boundary Dangerous-N ramp table
      renders legibly and the color-blind-friendly palette is preserved.
- [x] [AI] **Capture the retest evidence**, per the
      [Evidence Capture Convention](../../../repo-governance/development/quality/evidence-capture.md)'s
      hyphenated `phase-{N}-{description}-{locale}-{breakpoint}px` naming pattern (this content
      sub-tree is English-only per `brd.md`'s declared Non-Goal, so `<locale>` is always `en` — never
      omitted). Each tester writes into `${PLANDIR}evidence/`:
  - each tester's report path recorded as `phase-6-<tester>-report.md`;
  - `browser_take_screenshot` of both landings at mobile 375px, tablet 768px, and desktop 1440px,
    named `phase-6-<path-id>-en-<width>px.png`.
    Acceptance: `ls "${PLANDIR}evidence/" | grep -c '^phase-6-'` returns **at least 9**, and each
    tester's verdict is zero CRITICAL and zero HIGH.

### Phase 6 Gate

- [x] [AI] All three testers report zero CRITICAL/HIGH findings, or every finding is fixed and
      re-verified.
- [x] [AI] Evidence captured under `${PLANDIR}evidence/`.
- [x] [AI] Evidence is committed to the persistent final-delivery branch; nothing opens or merges
      before Phase 9.

> **Pause Safety**: both landings are manually retested and clean at their terminal state. Safe to
> stop. To resume: re-dispatch the three testers.

## Phase 7: Full-Corpus Integration Verification

- [x] [AI] `npm exec nx run ayokoding-www:build` succeeds with both manifests at their terminal state (27/30)
      and all 30 course bundles present (across plans 17 and 18).
- [x] [AI] `npm exec nx affected -t build,test:quick,lint --base=main` is green for `ayokoding-www`.
- [x] [AI] End-to-end path-walk: navigate `/en/learn/paths/skills/conventional-erp`, step through
      prev/next across all 27 courses via Playwright MCP, verify no broken link and no console error;
      repeat for `/en/learn/paths/skills/sharia-erp` across all 30.
- [x] [AI] **Capture evidence for the walk**, using the same hyphenated
      `phase-{N}-{description}-{locale}-{breakpoint}px` naming pattern as Phase 6 (`<locale>` is
      always `en`). Write to `${PLANDIR}evidence/`:
  - `browser_take_screenshot` of each path landing at three breakpoints, named
    `phase-7-<path-id>-landing-en-<width>px.png`.
  - `browser_take_screenshot` of the first and last course page of each walk, named
    `phase-7-<path-id>-<position>-<course-id>-en.png` — for `sharia-erp` the last is
    `zakat-and-sharia-compliance-modules` (course 30), for `conventional-erp` it is
    `erp-analytics-and-reporting` (course 27).
  - `browser_console_messages` output for each walk saved as `phase-7-<path-id>-console.txt`.
    Acceptance: `ls "${PLANDIR}evidence/" | grep -c '^phase-7-'` returns **at least 11**, and every
    `phase-7-*-console.txt` contains zero lines matching `-iE 'error|warning'`.

### Phase 7 Gate

- [x] [AI] Build succeeds; affected checks green; both path-walks complete with zero errors. Commit
      the evidence to the persistent final-delivery branch; Phase 9 alone opens the terminal archival PR.

> **Pause Safety**: the full corpus builds and both paths are walkable end to end at their terminal
> state. Safe to stop. To resume: re-run the Playwright path-walk.

## Phase 8: Knowledge Capture

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)._

- [x] [AI] Apply the litmus test to every `learnings.md` entry.
- [x] [AI] Apply the secret/sensitivity gate.
- [x] [AI] Apply the repo-relevance gate.
- [x] [AI] Route each surviving learning to exactly one durable home per the open-ended routing
      matrix.
- [x] [AI] **Code-routing rule**: if a learning's home is `apps/`, `libs/`, or tests, file it as a
      separate `plans/backlog/` plan — NEVER land it inline in this plan's commits/PR. The sole
      carve-out is a bug/lint/test failure that blocks THIS plan's own scope — that is fixed inline as
      ordinary Root Cause Orientation work, not routed as a deferred learning.
- [x] [AI] For any entry routed to `plans/ideas/`, scan `plans/ideas/README.md` and the existing
      two-pagers FIRST for a brief already covering the same problem or area — fold the learning into
      that brief instead of creating a new file; only create a new `plans/ideas/<slug>.md` when the
      scan confirms no existing brief overlaps (see
      [Integrate Before You Add](../../../repo-governance/conventions/structure/plans/ideas-folder-overview-rationale-and-file-layout.md#integrate-before-you-add-no-duplicate-two-pagers))
      — acceptance: the entry's routing line names either the folded-into brief or confirms the
      overlap scan found nothing.
- [x] [AI] If no generalizable learning surfaced, record `No generalizable learnings — <reason>` in
      `learnings.md`.

### Phase 8 Gate

- [x] [AI] Every `learnings.md` entry is terminal, or the explicit "none" escape is recorded.
- [x] [AI] No code-homed learning landed inline in this plan's own commits/PR.
- [x] [AI] The triaged `learnings.md` is committed to the persistent final-delivery branch; no PR is
      open before archival.

> **Pause Safety**: `learnings.md` is fully triaged. Safe to stop. To resume: re-read `learnings.md`.

## Phase 9: Plan Archival

### Sole PR integration (binding)

- [x] [AI] Archive this plan on its persistent final-delivery branch before review — acceptance: the archive move and index updates are committed in the same branch.
- [x] [AI] Open exactly one draft PR from that branch and run the secret scan, local quality checks, and PR quality-gate verification plus every local and CI gate — acceptance: the PR is the only PR for this plan.
- [x] [AI] Mark the PR ready, merge under the hardened preconditions, and deploy once — acceptance: the merge/deploy record is the plan's sole delivery record.

- [x] [AI] `git mv plans/in-progress/ayokoding-learning-path-18-skills-erp-enterprise-depth plans/done/$(date +%Y-%m-%d)__ayokoding-learning-path-18-skills-erp-enterprise-depth`.
- [x] [AI] Update `plans/in-progress/README.md` to remove this plan's in-progress entry and reflect its
      completed status.
- [x] [AI] Commit the archival move to the persistent final-delivery branch before opening the only PR.
      Use a Conventional Commits message, e.g.
      `git commit -m "chore(plans): archive ayokoding-learning-path-18-skills-erp-enterprise-depth"`.
- [x] [AI] **Push it** — `git push origin HEAD` — acceptance: exits 0 and
      `git status -sb | grep -c 'ahead'` returns **0**.
- [x] [AI] **Monitor CI on the new head** — poll every 2 minutes, one
      `gh run view --json status,conclusion` per wakeup; never tight-loop, never `gh run watch`; on a
      403 rate-limit wait ~35 minutes. Acceptance: `status` is `completed` and `conclusion` is
      `success` **for the run whose head SHA equals `git rev-parse HEAD`**.
- [x] [AI] Re-confirm all five PR Merge Protocol preconditions on the new head, perform the `[AI]`
      merge, then deploy `ayokoding-www` to `prod-ayokoding-www`. These are the terminal steps.

### Phase 9 Gate

- [x] [AI] The plan folder exists under `plans/done/` with the date prefix; no reference to it remains
      under `plans/backlog/`.
- [x] [AI] The archival commit landed **inside** the merged PR:
      `gh pr list --head "$(git rev-parse --abbrev-ref HEAD)" --state merged --json number,mergeCommit`
      returns this plan's PR. Use `gh pr list --head`, not `git merge-base --is-ancestor` (this repo
      squash-merges).
- [x] [AI] **Integration**: this phase opens, reviews, and merges the plan's sole terminal archival PR,
      then deploys `ayokoding-www` to `prod-ayokoding-www`. Both `skills/` ERP paths are complete end
      to end across plans 17 and 18.

> **Pause Safety**: the plan is archived. Terminal state — no further resume needed. Both
> `skills/conventional-erp` and `skills/sharia-erp` are complete in production.

## File impact and rollback

See [tech-docs.md §File impact](./tech-docs.md#file-impact-analysis) and [§Rollback](./tech-docs.md#rollback)
— this delivery checklist implements exactly that file set, phase by phase, with no step outside it.
