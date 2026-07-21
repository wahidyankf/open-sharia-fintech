# Delivery Checklist — Skills Path: Enterprise Resource Planning

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
> Git-mechanical steps (worktree create/remove, branch, commit, push, merge) are `[AI]`.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (safe-to-stop state + resume command). Each gate covers the phase's
> **content/data correctness** (checkers, tests, build) and its **integration** (draft PR opened,
> 3-cycle PR-Review, CI green, `[AI]` merge, `ayokoding-www` deployed). A phase is not complete until
> every gate check is green.

Three standing constraints govern every step below.

> **Cross-plan source of truth**: the ERP catalog — course ids, formats, prerequisite edges, ramp
> order — is settled in
> [tech-docs §The ERP catalog](./tech-docs.md#the-erp-catalog-20-courses-settled). Transcribe it; do
> not re-derive it.
>
> **The category ownership invariant (binding)**: this plan owns `<ERPMAN>`, `<ERPLANDING>`, the
> twenty ERP course bundles, and `<SYL>`. It **never** writes an accounting file, a careers manifest,
> a component, a design asset, or a structural `_index.md`. A step here that authors accounting
> material is a boundary violation and is equally forbidden in the other direction.
>
> **Verification hygiene (A4)**: the ERP research is almost entirely `[Unverified]`. No claim marked
> `[Unverified]` or `[Needs Verification]` may be written as fact. See
> [tech-docs §Verification status carried forward](./tech-docs.md#verification-status-carried-forward-a4).
>
> **Id-shape rule (schema-owner ruling, DD-21)**: the path id is the **full** string
> `skills/enterprise-resource-planning` — no separate `category` field, and **nothing keys on segment
> count**, because `pathId` is variable-depth by design (careers = 3 segments, skills = 2). Every
> URL/id match below is a **full-string literal** (`grep -F -q`) rather than a segment-shaped regex;
> a pattern such as `grep -oE '/en/learn/paths/[a-z-]+/[a-z0-9-]+'` stops at the first `/` inside a
> three-segment careers URL and undercounts. **Course ids are a different namespace and carry no
> category prefix** — every accounting and existing-library id below is written bare.

## Worktree

Worktree path: `worktrees/ayokoding-learning-path-07-skills-erp/`

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree ayokoding-learning-path-07-skills-erp
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the latest
`origin/main` when missing, syncs with `origin/main` before implementing, and prompts before deleting
the worktree after the plan is archived and pushed.

Every phase branches from the **latest `origin/main`** inside this one shared worktree
(`git fetch origin && git checkout main && git pull && git checkout -b ayokoding-learning-path-07-skills-erp/<phase-slug>`),
authors its work there, commits, pushes that branch, and opens **its own draft PR**.

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans.md#worktree-specification).

## Delivery Mode: worktree-to-pr

Each phase works in the shared worktree on its **own branch**, opens a **draft PR** against `main`,
runs the **PR-Review Maker→Fixer Cycle** (`pr-review-maker` / `pr-review-fixer`, 3 sequential CI-gated
cycles), flips the PR to ready, and `[AI]` **merges it once all quality gates are green** — then
`[AI]` **deploys `ayokoding-www` to `prod-ayokoding-www` after every merge** (this plan ships to
ayokoding.com). This plan declares **no** `[HUMAN]` merge gate. See
[Plans Organization Convention §Delivery Mode](../../../repo-governance/conventions/structure/plans.md#delivery-mode)
and the [PR Review Quality Gate workflow](../../../repo-governance/workflows/pr/pr-review-quality-gate.md).

**Per-Phase Integration Protocol** (each phase's gate lists these as must-pass):

1. [AI] Sync the shared worktree to latest `origin/main` and branch:
   `git fetch origin && git checkout main && git pull && git checkout -b ayokoding-learning-path-07-skills-erp/<phase-slug>`.
2. [AI] Stage only this phase's paths (`git add <explicit paths>` — never `git add -A`), commit
   thematically (Conventional Commits, imperative, no period), push the branch, open a **draft PR**
   against `main` (`gh pr create --draft --base main ...`) — CI runs on the PR.
3. [AI] Run the **PR-Review Maker→Fixer Cycle** (3 sequential CI-gated cycles), resolve every finding,
   then `gh pr ready`.
4. [AI] **Merge** once all quality gates are green (typecheck, lint, `test:quick`, `test:unit`,
   `test:e2e` where affected, `specs:behavior:coverage`, CI, the 3-cycle review).
5. [AI] Dispatch `apps-ayokoding-www-deployer` to deploy `ayokoding-www` to `prod-ayokoding-www` — a
   no-op redeploy for plan-side-only phases.

## Depends-on and start preconditions

| Direction   | Plan (full folder name)                                  | Strength                                        |
| ----------- | -------------------------------------------------------- | ----------------------------------------------- |
| `blockedBy` | `ayokoding-learning-path-01-url-restructure`             | hard                                            |
| `blockedBy` | `ayokoding-learning-path-02-schema-and-prerequisite-dag` | hard                                            |
| `blockedBy` | `ayokoding-learning-path-03-navigation-ui`               | hard                                            |
| `blockedBy` | `ayokoding-learning-path-06-skills-accounting`           | **soft overall — hard at the Wave B/C/D gates** |
| `blocks`    | _(none)_                                                 | terminal within the `skills/` category          |

**The plan-06 dependency is not a start precondition.** Phases 0, 1, and 2 declare **zero**
accounting checks — that absence is deliberate and is the mechanical expression of DD-4. The
accounting gates appear for the first time in Phase 3, and again in Phases 4 and 5.

## Parallelization Model

**Cap**: honor the in-force subagent/PR-review concurrency cap (parallel-by-default, background
subagents capped per the orchestration convention). The main thread self-promotes nothing.

- **Phases 0 → 1 → 2 → 3 → 4 → 5 are serial.** Each is a manifest state transition or its
  precondition, and each later phase's gate re-verifies the manifest published so far.
- **Inside a body-authoring phase, the bodies fan out.** Every course writes only its own subtree
  under `<COURSES>`, so a wave's bodies pipeline concurrently through maker → checker → fixer,
  bounded by the cap. Wave A's DAG width is 10, Wave B's is 5, Wave C's is 3, Wave D's is 2.
- **Phases 6 → 10 are serial.**
- **Across plans**, Phases 0-2 run fully concurrently with
  `ayokoding-learning-path-06-skills-accounting`. That is the parallelism the 06/07 split bought.

## Path constants

- `<COURSES>` = `apps/ayokoding-www/content/en/learn/courses/`
- `<PATHS>` = `apps/ayokoding-www/content/en/learn/paths/`
- `<ERPLANDING>` = `<PATHS>skills/enterprise-resource-planning/_index.md`
- `<FEAT>` = `apps/ayokoding-www/src/features/course-paths/`
- `<MANIFESTS>` = `<FEAT>manifests/`
- `<ERPMAN>` = `<MANIFESTS>skills/enterprise-resource-planning.yaml`
- `<SYL>` = `plans/backlog/ayokoding-learning-path-07-skills-erp/syllabus/courses/`
- `<SYLPATHS>` = `plans/backlog/ayokoding-learning-path-07-skills-erp/syllabus/paths/` — holds
  exactly one file, `manifest-skills-enterprise-resource-planning.md` (DD-22)
- `<SPECS>` = `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/course-paths/`
- Path id: `skills/enterprise-resource-planning` · URL: `/en/learn/paths/skills/enterprise-resource-planning`

### Course id lists (export once per shell; every acceptance clause below uses them)

**These are shell ARRAYS, not space-separated strings, and every loop below iterates
`"${NAME[@]}"`.** The interactive shell in this repo is **zsh**, which does **not** word-split an
unquoted parameter expansion: `for id in "${ERP_ALL[@]}"` would iterate exactly **once**, over the whole
string, and every derived count would silently read `1` instead of `20`. The array form iterates
correctly under both zsh and bash.

```bash
ERP_WAVE_A=(erp-foundations-and-history erp-conceptual-data-model erp-platform-landscape
  capstone-stand-up-and-integrate-an-open-source-erp procure-to-pay-systems order-to-cash-systems
  erp-extension-and-customization erp-integration-patterns erp-implementation-methodology
  evaluating-and-selecting-an-erp)

ERP_WAVE_B=(record-to-report-systems inventory-and-warehouse-management production-planning-and-mrp
  demand-and-supply-planning erp-analytics-and-reporting)

ERP_WAVE_C=(human-capital-management-and-hire-to-retire multi-company-and-multi-currency-erp
  erp-security-and-controls)

ERP_WAVE_D=(sharia-compliant-erp-design capstone-build-a-minimal-erp-core)

ERP_ALL=("${ERP_WAVE_A[@]}" "${ERP_WAVE_B[@]}" "${ERP_WAVE_C[@]}" "${ERP_WAVE_D[@]}")

ACCT_GATE_B=(financial-statements-and-close-cycle inventory-and-cogs-accounting)
ACCT_GATE_C=(consolidation-and-multi-entity-accounting audit-controls-and-compliance
  payroll-and-tax-accounting-essentials)
ACCT_GATE_D=(sharia-accounting-and-aaoifi-standards islamic-contract-modeling-for-systems
  capstone-build-a-general-ledger-system)
```

Counts: `ERP_WAVE_A` = 10, `ERP_WAVE_B` = 5, `ERP_WAVE_C` = 3, `ERP_WAVE_D` = 2, `ERP_ALL` = 20.
Verify the arrays loaded before trusting any clause below:
`for id in "${ERP_ALL[@]}"; do echo "$id"; done | wc -l` must return **20**; if it returns **1**, the
lists were pasted as strings rather than arrays and every count in this file is meaningless.
No id in `ERP_ALL` is a substring of another, so a plain `grep -F -q "$id"` against `<ERPMAN>` is an
exact membership test.

> **Shell-tooling notes for every acceptance clause below.** `grep` here is **ugrep**: `grep -c`
> counts **lines**, not matches, and `grep -L` means files-WITHOUT-match and exits 0 — neither is used
> anywhere in this file. `--glob` is unsupported; use `--exclude-dir`. `find -newermt` is GNU syntax
> and fails on this BSD `find` — it is not used. `md links validate` takes **no positional path**;
> only the exclude form appears here.

## The seven-step course-body authoring convention (DD-17)

Applies to **every** course-body step in Phases 2-5. Restated in full rather than cross-referenced,
because a plan whose authoring contract lives in a sibling folder cannot be executed standalone.

1. [AI] **V (accuracy pre-verify)** — spot-check every version-pinned, market-positioning, or
   integration-surface claim via `web-researcher` against a primary source — acceptance: no
   version-pinned or analyst-positioning claim is written unqualified; every volatile fact sits in a
   dated accuracy-note sidebar, never the stable spine. This step is **not optional for this corpus**
   — the research is `[Unverified]` by default (A4).
2. [AI] **Skeleton** — create `<COURSES><course-id>/` (`_index.md` carrying `prerequisites: [...]`
   transcribed verbatim from `<SYL><course-id>.md`, plus `overview.md`, `learning/_index.md`,
   `drilling/_index.md`), mirroring the sibling bundle shape — acceptance:
   `test -d "<COURSES><course-id>"`, `test -d "<COURSES><course-id>/learning"`, and
   `test -d "<COURSES><course-id>/drilling"` all exit 0, and
   `grep -F -q 'prerequisites:' "<COURSES><course-id>/_index.md"` exits 0.
3. [AI] **Author the learning track** — `overview.md` (purpose, `## Prerequisites` naming only
   already-authored library or ERP courses, and the scope-boundary statement where one is required),
   concept coverage, worked examples with colocated `code/` where code-bearing, and
   `learning/capstone/` — acceptance: the concept and example enumeration in `<SYL><course-id>.md` is
   fully covered.
4. [AI] **Author the drilling track** — `drilling/<course-id>.md` + `drilling/overview.md` in the
   fixed five-section order — acceptance: all five sections present.
5. [AI] **Run content checkers** — the format-matching learning checker
   (`apps-ayokoding-www-by-example-checker` or `apps-ayokoding-www-annotated-concept-checker`),
   `apps-ayokoding-www-facts-checker`, and `apps-ayokoding-www-link-checker`, plus
   `apps-ayokoding-www-general-checker` on `drilling/overview.md` — acceptance: findings recorded.
6. [AI] **Apply content fixers** — resolve every CRITICAL/HIGH/MEDIUM finding via the matching fixer —
   acceptance: every finding addressed.
7. [AI] **Re-verify** — re-run the checkers plus `npx nx run ayokoding-www:build` and
   `npm run lint:md` — acceptance: zero CRITICAL/HIGH/MEDIUM remain; build and lint exit 0.

_Content authoring is a maker-checker-fixer cycle, not code TDD — no RED/GREEN/REFACTOR labels
(DD-18). The manifest, Gherkin, and e2e steps in the same phases **are** code-bearing and do use the
full three-substep cycle._

---

## Phase 0: Environment Setup and Baseline

> _Executor: `repo-setup-manager`_
>
> This phase verifies the toolchain and the **five start preconditions**. It deliberately contains
> **no accounting check** — Waves A's ten courses need nothing from
> `ayokoding-learning-path-06-skills-accounting` (DD-4).

- [ ] [AI] Enter/provision the worktree and install dependencies in the root worktree: `npm install`
      — acceptance: exits 0, `node_modules/` synchronized.
- [ ] [AI] Converge the toolchain in the root worktree: `npm run doctor -- --fix`
      — acceptance: exits 0 with no unresolved drift.
- [ ] [AI] **Start precondition 1** — confirm the URL restructure is merged:
      `gh pr list --search "ayokoding-learning-path-01-url-restructure" --state merged --json number --jq 'length'`
      — acceptance: returns a value ≥ 1. Falsifiable both ways: it returns `0` while that plan is
      still open.
- [ ] [AI] **Start precondition 2** — confirm the schema plan is merged and the manifest directory
      exists: `test -d <MANIFESTS>` — acceptance: exits 0; returns non-zero on the current tree, where
      `<FEAT>` does not exist at all.
- [ ] [AI] **Start precondition 3** — confirm the renderer exists:
      `test -f <FEAT>shell/manifest-repository.ts` — acceptance: exits 0; returns non-zero before
      `ayokoding-learning-path-03-navigation-ui` lands.
- [ ] [AI] **Start precondition 4** — confirm the structural skills index exists and is **not** this
      plan's to create (A3 / DD-15): `test -f <PATHS>skills/_index.md` — acceptance: exits 0. If it
      returns non-zero, **stop**: plan 01 has not landed and creating it here would be a boundary
      violation.
- [ ] [AI] **Start precondition 5** — confirm the eight existing-library prerequisites resolve as
      course bundles:
      `for id in backend-essentials api-design event-driven-architecture networking-essentials security-essentials data-engineering analytics-and-experimentation project-management; do test -d "<COURSES>$id" || echo "MISSING $id"; done | wc -l`
      — acceptance: returns **0**. Falsifiable both ways: it returns **8** before plan 01's re-home,
      and a single missing course makes it **1**.
- [ ] [AI] **ERP baseline snapshot** — record that no ERP material exists yet:
      `for id in "${ERP_ALL[@]}"; do test -d "<COURSES>$id" && echo "PRESENT $id"; done | wc -l`
      — acceptance: returns **0**, recorded in `evidence/phase-0-snapshot.txt`. Falsifiable both ways:
      after Phase 5 the inverse check (`|| echo MISSING`) returns 0 instead.
- [ ] [AI] **Manifest baseline snapshot** — `test -f <ERPMAN>` — acceptance: returns **non-zero** (no
      manifest yet); recorded in `evidence/phase-0-snapshot.txt`. It exits 0 from Phase 2 onward.
- [ ] [AI] **Card baseline snapshot** —
      `grep -F -q 'skills/enterprise-resource-planning' <PATHS>skills/_index.md`
      — acceptance: exits **1** (no ERP card yet); recorded. It exits 0 from Phase 2 onward.
- [ ] [AI] Establish baselines: `npx nx run ayokoding-www:build`,
      `npx nx run ayokoding-www:test:unit`, and `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: all exit 0; record the pass counts in `evidence/phase-0-snapshot.txt`.
- [ ] [AI] Resolve every preexisting failure before proceeding — acceptance: zero unresolved failures
      remain; each fix committed separately with its own conventional-commit message.
- [ ] [AI] Confirm the `learnings.md` scaffold exists in the plan folder — acceptance: file present
      with its H1.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [ ] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift.
- [ ] [AI] All five start preconditions hold — plan 01 merged, `<MANIFESTS>` present,
      `manifest-repository.ts` present, `<PATHS>skills/_index.md` present, and all eight
      existing-library prerequisites resolving.
- [ ] [AI] `ayokoding-www:build` + `:test:unit` + `ayokoding-www-fe-e2e:test:e2e` baselines recorded
      green in `evidence/phase-0-snapshot.txt`; zero preexisting failures unresolved.
- [ ] [AI] Zero ERP bundles present; no `<ERPMAN>`; no ERP card — all three recorded as the "before"
      side of this plan's falsifiable checks.
- [ ] [AI] Draft PR opened; CI triggered; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged;
      `ayokoding-www` deployed (no-op redeploy).

> **Pause Safety**: only the toolchain was verified and the current state snapshotted — no ERP
> content, manifest, or card exists. Safe to stop indefinitely. To resume: re-run the five
> precondition checks and the three baselines.

---

## Phase 1: The twenty syllabus specs and the A4 verification pass

> _Suggested executor: `web-researcher` (the verification pass) + `docs-maker` (the spec files)._
>
> This phase produces the **authoring contract** for all twenty bodies, inside this plan's own folder
> (DD-2). No user-visible content ships here, and no accounting file is read or written. Twenty
> courses' concepts, worked examples, prerequisite chains, and capstone specs are settled once, so
> every later authoring step transcribes rather than decides.
>
> It is also the phase where the research's `[Unverified]` markers are carried forward rather than
> laundered (A4 / DD-11).

### 1.1 · Scaffold the syllabus corpus

- [ ] [AI] Create `<SYL>` and author `<SYL>README.md` _(new files)_ — the ERP catalog index: the
      twenty rows transcribed verbatim from
      [tech-docs §The ERP catalog](./tech-docs.md#the-erp-catalog-20-courses-settled), each with its
      course id, format, prerequisite sets, wave, and ramp band; plus the explicit
      `[Judgment call]` label on the 20-course count — acceptance: `test -f <SYL>README.md` exits 0
      (non-zero before this step), and
      `for id in "${ERP_ALL[@]}"; do grep -F -q "$id" <SYL>README.md || echo "MISSING $id"; done | wc -l`
      returns **0** (returns **20** before this step).
  - _Suggested executor: `docs-maker`_
- [ ] [AI] Create `<SYLPATHS>` and author
      `<SYLPATHS>manifest-skills-enterprise-resource-planning.md` _(new file)_ — the authoritative
      ordering this plan's `courseOrder` is transcribed from, recording
      `pathId: skills/enterprise-resource-planning` (the **full** string, no separate `category`
      field) and `arc: immediately-effective` as explicit data, plus the twenty ids in ramp order
      annotated with their wave and ramp band. **The filename carries the `skills-` marker (DD-22)**
      — a bare `manifest-enterprise-resource-planning.md` is wrong — acceptance:
      `test -f <SYLPATHS>manifest-skills-enterprise-resource-planning.md` exits 0 (non-zero before
      this step), AND `test -f <SYLPATHS>manifest-enterprise-resource-planning.md` exits **non-zero**
      (the un-prefixed name must not exist), AND
      `grep -F -q 'skills/enterprise-resource-planning' <SYLPATHS>manifest-skills-enterprise-resource-planning.md`
      exits 0, AND
      `grep -F -q 'arc: immediately-effective' <SYLPATHS>manifest-skills-enterprise-resource-planning.md`
      exits 0.
  - _Suggested executor: `docs-maker`_

### 1.2 · The A4 verification pass (before any spec asserts a fact)

- [ ] [AI] Close the **SAP source gap** — the research's direct SAP-owned source returned HTTP 403;
      obtain a working **SAP Help Portal** URL covering the integration-surface claims (IDoc status in
      SAP Cloud ERP Public Cloud, OData generations) — acceptance: either a fetched SAP Help Portal
      URL with an inline excerpt and access date is recorded in `<SYL>README.md`, **or** the gap is
      recorded as unresolved and every affected claim is marked `[Unverified]` with its provenance.
      Falsifiable both ways: `grep -F -q 'help.sap.com' <SYL>README.md` exits 1 today.
  - _Suggested executor: `web-researcher`_
- [ ] [AI] Re-verify the **Dataverse dual-write** and **OData generation** claims against vendor
      documentation — acceptance: each claim is either `[Verified]` with URL + excerpt + access date,
      or carried as `[Unverified]` into a dated accuracy-note sidebar. No claim is promoted silently.
  - _Suggested executor: `web-researcher`_
- [ ] [AI] Record the **analyst-positioning** constraint — Gartner MQ positioning is paywalled and was
      triangulated from vendor and analyst coverage only, so it is **weakly sourced** — acceptance:
      `<SYL>erp-platform-landscape.md` and `<SYL>evaluating-and-selecting-an-erp.md` both state that
      no analyst ranking may be presented as fact, and frame market position as commentary with its
      provenance or omit it.
- [ ] [AI] Resolve the **Indonesian PSAK numbering** conflict ("PSAK 59 / SIFAS 101-109" versus "PSAK
      101-110") against IAI's published list — acceptance: either the resolved series is recorded with
      a cited URL and access date in `<SYL>sharia-compliant-erp-design.md`, or the spec forbids
      writing any PSAK number and refers to the series by name only. Falsifiable both ways: a spec
      that names a numbered standard with no citation fails this check.
  - _Suggested executor: `web-researcher`_
- [ ] [AI] Record the **stable-versus-volatile** split in `<SYL>README.md` — stable and safe to assert:
      module names (FI/CO/MM/SD/PP), process names (P2P/O2C/R2R/H2R), the MRP algorithm, double-entry;
      volatile and sidebar-only: platform version pins, integration surfaces, analyst positioning —
      acceptance: both lists present; `grep -F -q 'accuracy-note sidebar' <SYL>README.md` exits 0.

### 1.3 · Author the twenty specs

- [ ] [AI] Author `<SYL><course-id>.md` for each of the ten **Wave A** ids in the `ERP_WAVE_A` list _(new
      files)_ — each carrying, in the sibling-corpus section order: title line with course id, format
      and language; "Why this exists · the big idea"; "Prerequisites" (ERP, existing-library, and
      accounting sets transcribed from the catalog); "Accuracy notes" carrying every applicable A4
      marker; enumerated concepts; enumerated worked examples; a capstone spec; and "In which paths"
      — acceptance:
      `for id in "${ERP_WAVE_A[@]}"; do test -f "<SYL>$id.md" || echo "MISSING $id"; done | wc -l` returns
      **0** (returns **10** before this step).
  - _Suggested executor: `docs-maker`_
- [ ] [AI] Author the five **Wave B** specs in the `ERP_WAVE_B` list _(new files)_ — same shape.
      `<SYL>record-to-report-systems.md` must state the **hard** cross-domain edge explicitly: it
      requires `financial-statements-and-close-cycle` because subledger→GL posting is meaningless
      without a balanced ledger — acceptance:
      `for id in "${ERP_WAVE_B[@]}"; do test -f "<SYL>$id.md" || echo "MISSING $id"; done | wc -l` returns
      **0**, AND `grep -F -q 'financial-statements-and-close-cycle' <SYL>record-to-report-systems.md`
      exits 0.
- [ ] [AI] Author the three **Wave C** specs in the `ERP_WAVE_C` list _(new files)_ — same shape.
      `<SYL>erp-security-and-controls.md` must state its scope boundary against `it-governance-grc`
      (keep to RBAC/SoD and COSO-SOX specifics) — acceptance:
      `for id in "${ERP_WAVE_C[@]}"; do test -f "<SYL>$id.md" || echo "MISSING $id"; done | wc -l` returns
      **0**, AND `grep -F -q 'it-governance-grc' <SYL>erp-security-and-controls.md` exits 0.
- [ ] [AI] Author the two **Wave D** specs in the `ERP_WAVE_D` list _(new files)_ — same shape.
      `<SYL>sharia-compliant-erp-design.md` must name all three jurisdictional models and make
      **jurisdictional pluggability** the stated engineering lesson (DD-12) — acceptance:
      `for id in "${ERP_WAVE_D[@]}"; do test -f "<SYL>$id.md" || echo "MISSING $id"; done | wc -l` returns
      **0**, AND
      `for s in AAOIFI 'PSAK Syariah' MFRS 'Bank Negara'; do grep -F -q "$s" <SYL>sharia-compliant-erp-design.md || echo "MISSING $s"; done | wc -l`
      returns **0**.
- [ ] [AI] State the two remaining **scope boundaries** in their specs —
      `<SYL>erp-analytics-and-reporting.md` names `data-engineering` and keeps to ERP-specific CDC and
      delta extraction; `<SYL>erp-implementation-methodology.md` names `project-management` and keeps
      to fit-gap, cutover, and migration (DD-10) — acceptance:
      `grep -F -q 'data-engineering' <SYL>erp-analytics-and-reporting.md` exits 0 AND
      `grep -F -q 'project-management' <SYL>erp-implementation-methodology.md` exits 0. Both exit 1
      before this step.
- [ ] [AI] **Canonical path id in every spec (DD-23)** — every spec's "In which paths" section names
      the path as the full `skills/enterprise-resource-planning`, never a bare
      `enterprise-resource-planning` — acceptance:
      `for id in "${ERP_ALL[@]}"; do grep -F -q 'skills/enterprise-resource-planning' "<SYL>$id.md" || echo "MISSING $id"; done | wc -l`
      returns **0** (returns **20** before the specs are authored). **Do NOT edit plan 02's 121
      existing course specs** — they carry stale un-prefixed path ids that plan 02 deliberately left
      as custody-protected informational metadata; touching them is a boundary violation.
- [ ] [AI] **No category prefix on course ids (DD-21)** — the eight accounting prerequisites and the
      eight existing-library prerequisites are written **bare** in every spec, never prefixed with a
      category — acceptance:
      `grep -rF -l 'skills/financial-statements-and-close-cycle' <SYL> | wc -l` returns **0**, and the
      same for any other `skills/<course-id>` or `careers/<course-id>` form. Falsifiable both ways:
      writing one prefixed course id makes the count **1**.
- [ ] [AI] Verify the specs' internal prerequisite graph is acyclic and complete — every ERP
      prerequisite named in a spec is itself one of the twenty ids, every existing-library
      prerequisite resolves under `<COURSES>`, and every accounting prerequisite is one of the eight
      ids across the `ACCT_GATE_B`, `ACCT_GATE_C`, and `ACCT_GATE_D` lists — acceptance: no unknown id remains; the check
      is recorded in `<SYL>README.md`.
- [ ] [AI] Run `md links validate` and `md heading-hierarchy validate` plus `npm run lint:md` over the
      new plan folder:
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md links validate --exclude plans/done --exclude apps/ayokoding-www/content --exclude apps/ose-www/content 2>&1 | grep -F "ayokoding-learning-path-07-skills-erp"`
      — acceptance: the `grep` finds **no** matching line (exit 1). Falsifiable the other way:
      introduce one bad relative link into a spec and the same command prints that file and exits 0.

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [ ] [AI] `for id in "${ERP_ALL[@]}"; do test -f "<SYL>$id.md" || echo "MISSING $id"; done | wc -l` returns
      **0** (returned **20** before this phase).
- [ ] [AI] `<SYL>README.md` exists and names all twenty ids; the 20-course count is labelled
      `[Judgment call]`.
- [ ] [AI] `<SYLPATHS>manifest-skills-enterprise-resource-planning.md` exists, records the full
      `pathId` and the explicit `arc`, and the un-prefixed filename does **not** exist (DD-22).
- [ ] [AI] Every spec names the full `skills/enterprise-resource-planning` path id; no course id
      anywhere in `<SYL>` carries a category prefix; plan 02's 121 specs are untouched —
      `git diff --name-only origin/main...HEAD | grep -F 'ayokoding-learning-path-02-schema-and-prerequisite-dag' | wc -l`
      returns **0**.
- [ ] [AI] The SAP source gap is either closed with a cited SAP Help Portal URL **or** recorded
      unresolved with every affected claim marked `[Unverified]`.
- [ ] [AI] The PSAK numbering conflict is either resolved with a citation or the spec forbids naming a
      numbered standard.
- [ ] [AI] The three scope-boundary specs each name their neighbouring existing course; the Sharia
      spec names all three jurisdictional models.
- [ ] [AI] The filtered link check finds no line naming this plan's folder; `md heading-hierarchy
validate` and `npm run lint:md` exit 0.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed (no-op).

> **Pause Safety**: the design surface is complete and lives entirely inside this plan folder — no
> user-visible content, manifest, or card exists, and nothing in the app changed. Safe to stop
> indefinitely. To resume: re-run the twenty-spec presence check and the filtered link check.

---

## Phase 2: Wave A — ten bodies, the landing, and manifest publication (boundary 1)

> _Suggested executors: `apps-ayokoding-www-by-example-maker` (5 bodies) and
> `apps-ayokoding-www-annotated-concept-maker` (5 bodies) for the corpus;
> `apps-ayokoding-www-general-maker` for the landing._
>
> **Zero accounting preconditions.** All ten Wave-A courses' prerequisites resolve inside the ERP
> corpus plus the existing software-engineering library (DD-4). This phase runs fully concurrently
> with `ayokoding-learning-path-06-skills-accounting`.
>
> It closes at **ramp boundary 1**: a reader who finishes course #4 can install, configure, and
> integrate a real ERP through its API. The path becomes a live, standalone-useful product here, not
> at the end.

### 2.1 · Author the ten Wave-A bodies

Each body applies the [seven-step convention](#the-seven-step-course-body-authoring-convention-dd-17)
and is authored from its `<SYL><course-id>.md` spec, not from a fresh judgment call. The ten fan out
concurrently, bounded by the cap.

- [ ] [AI] `erp-foundations-and-history` (Annotated-concept) — acceptance: all seven convention steps
      complete; checkers report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] `erp-conceptual-data-model` (Annotated-concept) — master versus transactional data, the
      abstraction whose absence causes the silent corruption this path exists to prevent — acceptance:
      all seven steps complete; zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] `erp-platform-landscape` (Annotated-concept) — acceptance: all seven steps complete; zero
      CRITICAL/HIGH/MEDIUM; **and** no analyst ranking is stated as fact —
      `grep -F -q 'Magic Quadrant' "<COURSES>erp-platform-landscape/overview.md"` either exits 1, or
      exits 0 only on a line that also carries the provenance qualifier recorded in Phase 1.2.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] `capstone-stand-up-and-integrate-an-open-source-erp` (By Example) — **boundary 1, the first
      payoff.** Stands up a **containerised or fixtured** open-source ERP; per DD-14 **no code sample
      may depend on a live network call to a third-party ERP** — acceptance: all seven steps complete;
      zero CRITICAL/HIGH/MEDIUM; **and** the bundle declares its two existing-library prerequisites —
      `for id in backend-essentials api-design; do grep -F -q "$id" "<COURSES>capstone-stand-up-and-integrate-an-open-source-erp/_index.md" || echo "MISSING $id"; done | wc -l`
      returns **0**.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `procure-to-pay-systems` (By Example) — acceptance: all seven steps complete; zero
      CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `order-to-cash-systems` (By Example) — acceptance: all seven steps complete; zero
      CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `erp-extension-and-customization` (By Example) — acceptance: all seven steps complete; zero
      CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `erp-integration-patterns` (By Example) — every integration-surface claim (IDoc status,
      Dataverse dual-write, OData generations) sits in a **dated accuracy-note sidebar** carrying its
      Phase-1.2 verification state; per DD-14 no code sample calls a live third-party ERP —
      acceptance: all seven steps complete; zero CRITICAL/HIGH/MEDIUM; **and**
      `grep -F -q 'accuracy note' "<COURSES>erp-integration-patterns/overview.md"` exits 0 (exits 1
      before this step).
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `erp-implementation-methodology` (Annotated-concept) — states its scope boundary against
      `project-management`: fit-gap, cutover, and data migration only (DD-10) — acceptance: all seven
      steps complete; zero CRITICAL/HIGH/MEDIUM; **and**
      `grep -F -q 'project-management' "<COURSES>erp-implementation-methodology/overview.md"` exits 0
      (exits 1 before this step, and exits 1 again if the boundary line is later dropped).
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] `evaluating-and-selecting-an-erp` (Annotated-concept) — acceptance: all seven steps
      complete; zero CRITICAL/HIGH/MEDIUM; no analyst ranking stated as fact.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] Add all ten ids to `<COURSES>_index.md` — acceptance:
      `for id in "${ERP_WAVE_A[@]}"; do grep -F -q "$id" <COURSES>_index.md || echo "MISSING $id"; done | wc -l`
      returns **0** (returns **10** before this step); `apps-ayokoding-www-link-checker` green on
      `<COURSES>_index.md`.

### 2.2 · TDD cycle A — publish the manifest

- [ ] [AI] **RED** — add the ERP manifest assertions to `<MANIFESTS>published-manifests.unit.test.ts`
      _(existing file, owned by `ayokoding-learning-path-05-manifests` — append only)_; **if that file
      does not exist**, create `<MANIFESTS>skills/erp-manifest.unit.test.ts` _(new file)_ scoped to
      this manifest alone. The assertion: `<ERPMAN>` loads, zod-validates against `<FEAT>core/schemas.ts`,
      carries `arc: immediately-effective`, and passes `checkManifestIntegrity` +
      `checkPrerequisiteConsistency` — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the new assertion **fails** with a module-not-found or empty-glob error naming
      `skills/enterprise-resource-planning.yaml`. A failure for any other reason means a Phase-0
      precondition was not honoured — stop and re-check.

  **Gherkin (binds) →** "The ERP path publishes before the accounting corpus is complete"

  ```gherkin
  Scenario: The ERP path publishes before the accounting corpus is complete
    Given the ten accounting-independent ERP courses are authored and the accounting corpus is still in progress
    When the ERP path manifest is published
    Then the manifest validates, the landing renders, and the path is reachable in production
    And no course in the published courseOrder declares an accounting prerequisite
  ```

- [ ] [AI] **GREEN** — author `<ERPMAN>` _(new file)_ with
      `pathId: skills/enterprise-resource-planning` (the **full** string including the category
      segment — no separate `category` field, DD-21), the separate required field
      `arc: immediately-effective` (DD-7), a `title`, a
      `description`, and `courseOrder` holding exactly the ten Wave-A ids **in ramp order**
      (`erp-foundations-and-history`, `erp-conceptual-data-model`, `erp-platform-landscape`,
      `capstone-stand-up-and-integrate-an-open-source-erp`, `procure-to-pay-systems`,
      `order-to-cash-systems`, `erp-extension-and-customization`, `erp-integration-patterns`,
      `erp-implementation-methodology`, `evaluating-and-selecting-an-erp`) — command:
      `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0, AND every Wave-A id is present —
      `for id in "${ERP_WAVE_A[@]}"; do grep -F -q "$id" <ERPMAN> || echo "MISSING $id"; done | wc -l`
      returns **0**, AND every deferred id is absent —
      `for id in "${ERP_WAVE_B[@]}" "${ERP_WAVE_C[@]}" "${ERP_WAVE_D[@]}"; do grep -F -q "$id" <ERPMAN> && echo "PRESENT $id"; done | wc -l`
      returns **0**. Both halves are required; the second is the falsifiable deferral check that
      inverts in Phases 3-5.

  **Gherkin (binds) →** "The manifest records its arc even though the URL omits it"

  ```gherkin
  Scenario: The manifest records its arc even though the URL omits it
    Given the skills URL grammar has no arc segment
    When the enterprise-resource-planning manifest is loaded and validated
    Then the manifest carries the field arc set to immediately-effective
    And the path id validates on its first segment skills and on resolving to an existing manifest, never on its segment count
  ```

- [ ] [AI] **REFACTOR** — align the YAML's key order and comment style with the schema plan's
      documented example, and assert the structural invariant that `courseOrder` is the file's **only**
      YAML sequence, so a list-item count is an exact `courseOrder` length — command:
      `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:lint`
      — acceptance: both exit 0; `grep -oE '^ *- ' <ERPMAN> | wc -l` returns **10**, matching the
      Wave-A id count exactly, and no assertion was weakened (the deferral check still returns 0).

### 2.3 · The landing and the cards (content — maker/checker/fixer, not TDD)

- [ ] [AI] Author `<ERPLANDING>` _(new file — this is the **path landing**, not a structural index;
      see DD-15)_ — prose and SEO only, satisfying the four landing content requirements in
      [tech-docs §Landing content requirements](./tech-docs.md#landing-content-requirements-what-plan-03-cannot-infer):
      **L-1** all three ramp boundaries as can/cannot pairs; **L-2** the three-course runway with its
      reason (without the data model and the platform landscape a reader integrates against the wrong
      abstractions and silently corrupts state); **L-3** the immediately-effective arc stated once,
      with no arc chooser; **L-4** outbound canonical links to the linked-not-walked prerequisites.
      **No `courseOrder` in the landing** — the ordered list renders from the loaded manifest —
      acceptance: `grep -F -q 'courseOrder' <ERPLANDING>` exits **1** (and exits 0 if one is mistakenly
      added), AND
      `for s in 'after the fourth' 'after the tenth' 'silently corrupts state'; do grep -F -q "$s" <ERPLANDING> || echo "MISSING $s"; done | wc -l`
      returns **0**, AND
      `for id in backend-essentials api-design financial-statements-and-close-cycle; do grep -F -q "$id" <ERPLANDING> || echo "MISSING $id"; done | wc -l`
      returns **0** (the sample of linked-not-walked prerequisites resolves).
  - _Suggested executor: `apps-ayokoding-www-general-maker`_
- [ ] [AI] Run `apps-ayokoding-www-link-checker` and `apps-ayokoding-www-general-checker` over the new
      landing — acceptance: findings recorded.
- [ ] [AI] Apply the matching fixer to every CRITICAL/HIGH/MEDIUM finding — acceptance: zero
      CRITICAL/HIGH/MEDIUM remain on re-run.
- [ ] [AI] Populate the ERP card in `<PATHS>skills/_index.md` _(existing file, created by
      `ayokoding-learning-path-01-url-restructure` — **populate only, never create**)_ — acceptance:
      `grep -F -q 'skills/enterprise-resource-planning' <PATHS>skills/_index.md` exits **0** (exited 1
      at the Phase-0 snapshot). The check is scoped to **this plan's own card**, so a sibling
      accounting card landing before or after never affects it.
- [ ] [AI] Populate the ERP card in the paths hub `<PATHS>_index.md` _(existing file, created by plan
      01 — populate only)_ — acceptance:
      `grep -F -q 'skills/enterprise-resource-planning' <PATHS>_index.md` exits **0** (exited 1
      before).

### 2.4 · TDD cycle B — the landing renders the ramp

- [ ] [AI] **RED** — add `<SPECS>skills-erp-path.feature` _(new file)_ and a failing e2e step in
      `apps/ayokoding-www-fe-e2e/src/steps/course-paths.steps.ts` _(existing file, created by
      `ayokoding-learning-path-03-navigation-ui`)_ asserting that the ERP landing states boundary 1's
      can/cannot pair — command: `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: the new spec **fails** because the assertion is not yet bound.

  **Gherkin (binds) →** "A reader is dangerous after the fourth course"

  ```gherkin
  Scenario: A reader is dangerous after the fourth course
    Given a reader has completed the first four ERP courses
    When they open the path landing
    Then the landing states that they can now install, configure, and integrate a real ERP through its API
    And it states plainly that they cannot yet design correct procure-to-pay, order-to-cash, or record-to-report flows
  ```

- [ ] [AI] **GREEN** — implement the step bindings against the published landing — command:
      `npx nx run ayokoding-www:specs:behavior:coverage && npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: both exit 0.
- [ ] [AI] **REFACTOR** — extract a reusable "landing states a ramp boundary" step definition
      parameterised by boundary number, so Phases 3 and 5 add one line rather than a copied block —
      command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: exits 0 and the scenario count
      is unchanged.

### 2.5 · TDD cycle C — the runway justification

- [ ] [AI] **RED** — add a failing e2e assertion that the landing states the three-course runway
      **and** its reason — command: `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: the new spec **fails**.

  **Gherkin (binds) →** "The landing justifies the longer runway instead of hiding it"

  ```gherkin
  Scenario: The landing justifies the longer runway instead of hiding it
    Given the ERP path takes three orientation courses before its first useful capstone
    When a reader reads the landing before committing to the path
    Then the landing names the runway explicitly and gives its reason
    And the reason states that without the data model and the platform landscape a reader integrates against the wrong abstractions and silently corrupts state
  ```

- [ ] [AI] **GREEN** — bind the assertion against the landing copy — command:
      `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: exits 0.
- [ ] [AI] **REFACTOR** — fold the runway assertion into the parameterised landing-copy step group —
      command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: exits 0, scenario count
      unchanged.

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [ ] [AI] `for id in "${ERP_WAVE_A[@]}"; do test -d "<COURSES>$id" || echo "MISSING $id"; done | wc -l`
      returns **0** (returned **10** before this phase).
- [ ] [AI] `test -f <ERPMAN>` exits 0 (exited non-zero at the Phase-0 snapshot);
      `grep -oE '^ *- ' <ERPMAN> | wc -l` returns **10**.
- [ ] [AI] The deferral check
      `for id in "${ERP_WAVE_B[@]}" "${ERP_WAVE_C[@]}" "${ERP_WAVE_D[@]}"; do grep -F -q "$id" <ERPMAN> && echo "PRESENT $id"; done | wc -l`
      returns **0** — the truncation is deliberate, recorded, and provable.
- [ ] [AI] `npx nx run ayokoding-www:test:unit` exits 0 — the manifest loads, zod-validates, carries
      `arc: immediately-effective`, and passes integrity plus prerequisite-consistency.
- [ ] [AI] `npx nx run ayokoding-www:build` + `:specs:behavior:coverage` **and**
      `npx nx run ayokoding-www-fe-e2e:test:e2e` exit 0. (`ayokoding-www:test:e2e` and
      `:test:integration` are no-op echo targets and can never fail — omitted deliberately.)
- [ ] [AI] `grep -F -q 'courseOrder' <ERPLANDING>` exits **1**; the landing's L-1/L-2/L-4 string checks
      each return **0** missing.
- [ ] [AI] `grep -F -q 'skills/enterprise-resource-planning' <PATHS>skills/_index.md` and the same
      against `<PATHS>_index.md` both exit **0**.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: **ramp boundary 1 is live in production.** A reader can walk ten courses and come
> out able to install, configure, and integrate a real ERP — the immediately-effective promise is
> already kept. The manifest is deliberately scoped to Wave A and its truncation is provable in both
> directions, so nothing looks finished that is not. Safe to stop indefinitely, including
> indefinitely long, while `ayokoding-learning-path-06-skills-accounting` finishes. To resume:
> `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www-fe-e2e:test:e2e`.

---

## Phase 3: Wave B — five bodies and growth to fifteen (boundary 2)

> _Suggested executors: `apps-ayokoding-www-by-example-maker` (4 bodies) and
> `apps-ayokoding-www-annotated-concept-maker` (1 body)._
>
> **This is where the accounting dependency first bites.** `record-to-report-systems` requires
> `financial-statements-and-close-cycle`, because subledger→GL posting is meaningless without a
> balanced ledger. `inventory-and-warehouse-management` requires `inventory-and-cogs-accounting`, and
> `production-planning-and-mrp`, `demand-and-supply-planning`, and `erp-analytics-and-reporting`
> inherit those gates transitively (see
> [tech-docs §Authoring waves](./tech-docs.md#authoring-waves-vs-reading-ramp-dd-3)).
>
> It closes at **ramp boundary 2**: courses #1-#10 all exist, so a reader can design correct core
> process flows, extend safely, and pick the right integration pattern.

### 3.1 · Accounting gate (hard — the plan-06 dependency)

- [ ] [AI] **Wave-B accounting gate** — confirm both accounting bundles resolve on `origin/main`:
      `git fetch origin && git checkout main && git pull` then
      `for id in "${ACCT_GATE_B[@]}"; do test -d "<COURSES>$id" || echo "MISSING $id"; done | wc -l`
      — acceptance: returns **0**. Falsifiable both ways: it returns **2** today and **1** if only one
      accounting body has landed. **If it does not return 0, stop and wait** — poll rather than
      author around the gap; authoring `record-to-report-systems` against a guessed general ledger is
      the failure this gate exists to prevent.

  **Gherkin (binds) →** "The record-to-report course waits for its accounting prerequisite"

  ```gherkin
  Scenario: The record-to-report course waits for its accounting prerequisite
    Given the record-to-report-systems course has not been authored
    When the authoring wave containing it is about to start
    Then the financial-statements-and-close-cycle course bundle must already resolve on origin main
    And the wave does not start while that bundle is absent
  ```

### 3.2 · Author the five Wave-B bodies

Each applies the [seven-step convention](#the-seven-step-course-body-authoring-convention-dd-17) from
its `<SYL><course-id>.md` spec. The five fan out concurrently, bounded by the cap.

- [ ] [AI] `record-to-report-systems` (By Example) — the hard cross-domain edge; the body declares
      `financial-statements-and-close-cycle` as a prerequisite and explains **why** subledger→GL
      posting needs a balanced ledger — acceptance: all seven steps complete; zero CRITICAL/HIGH/MEDIUM;
      **and** `grep -F -q 'financial-statements-and-close-cycle' "<COURSES>record-to-report-systems/_index.md"`
      exits 0 (exits 1 before this step).
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `inventory-and-warehouse-management` (By Example) — declares
      `inventory-and-cogs-accounting` — acceptance: all seven steps complete; zero
      CRITICAL/HIGH/MEDIUM; **and**
      `grep -F -q 'inventory-and-cogs-accounting' "<COURSES>inventory-and-warehouse-management/_index.md"`
      exits 0.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `production-planning-and-mrp` (By Example) — the MRP algorithm is **stable and safe to
      assert** (A4), so it belongs in the stable spine rather than an accuracy-note sidebar —
      acceptance: all seven steps complete; zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `demand-and-supply-planning` (Annotated-concept) — acceptance: all seven steps complete;
      zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] `erp-analytics-and-reporting` (By Example) — states its scope boundary against
      `data-engineering`: ERP-specific CDC and delta extraction only (DD-10) — acceptance: all seven
      steps complete; zero CRITICAL/HIGH/MEDIUM; **and**
      `grep -F -q 'data-engineering' "<COURSES>erp-analytics-and-reporting/overview.md"` exits 0
      (exits 1 before this step, and exits 1 again if the boundary line is later dropped).
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Add all five ids to `<COURSES>_index.md` — acceptance:
      `for id in "${ERP_WAVE_B[@]}"; do grep -F -q "$id" <COURSES>_index.md || echo "MISSING $id"; done | wc -l`
      returns **0** (returns **5** before this step).

### 3.3 · TDD cycle — grow the manifest to fifteen

- [ ] [AI] **RED** — extend the manifest unit test with an assertion that `courseOrder` contains all
      fifteen ids of `ERP_WAVE_A` plus `ERP_WAVE_B` in ramp order — command:
      `npx nx run ayokoding-www:test:unit`
      — acceptance: the assertion **fails**, naming the five absent Wave-B ids.

  **Gherkin (binds) →** "An early-published manifest cannot pass as complete"

  ```gherkin
  Scenario: An early-published manifest cannot pass as complete
    Given the manifest is published with only the accounting-independent courses
    When the deferred course ids are checked against the manifest file
    Then every deferred id is provably absent at publication time
    And the same check returns the full set once the growth waves have landed
  ```

- [ ] [AI] **GREEN** — insert the five Wave-B ids into `<ERPMAN>` at their correct ramp positions
      (`record-to-report-systems` and `inventory-and-warehouse-management` after
      `order-to-cash-systems`; `production-planning-and-mrp` and `demand-and-supply-planning` after
      `erp-integration-patterns`; `erp-analytics-and-reporting` before `erp-implementation-methodology`)
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0, AND
      `for id in "${ERP_WAVE_B[@]}"; do grep -F -q "$id" <ERPMAN> || echo "MISSING $id"; done | wc -l`
      returns **0** (returned **5** at the Phase-2 gate), AND `grep -oE '^ *- ' <ERPMAN> | wc -l`
      returns **15** (returned **10**), AND the remaining deferral still holds —
      `for id in "${ERP_WAVE_C[@]}" "${ERP_WAVE_D[@]}"; do grep -F -q "$id" <ERPMAN> && echo "PRESENT $id"; done | wc -l`
      returns **0**. All three halves are required: a growth that pulled in Wave C would pass the
      first two and fail the third.
- [ ] [AI] **REFACTOR** — re-run prerequisite-consistency and confirm no reordering was needed to
      satisfy it; any smoothness regression is fixed by bridging prose **in place, never by
      reordering** — command: `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:lint`
      — acceptance: both exit 0 and no assertion was weakened.

### 3.4 · Boundary 2 on the landing

- [ ] [AI] **RED** — add a failing e2e assertion for boundary 2's can/cannot pair, using the
      parameterised step extracted in Phase 2.4 — command: `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: the new spec **fails**.

  **Gherkin (binds) →** "A reader is dangerous again after the tenth course"

  ```gherkin
  Scenario: A reader is dangerous again after the tenth course
    Given a reader has completed the first ten ERP courses
    When they open the path landing
    Then the landing states that they can now design correct core process flows, extend safely, and pick the right integration pattern
    And it states plainly that they cannot yet do production planning, multi-entity work, segregation-of-duties enforcement, or run a rollout
  ```

- [ ] [AI] **GREEN** — update `<ERPLANDING>` so boundary 2 is stated as reached, and bind the
      assertion — command:
      `npx nx run ayokoding-www:specs:behavior:coverage && npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: both exit 0.
- [ ] [AI] **REFACTOR** — deduplicate the boundary copy so the three boundaries share one prose
      pattern — command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: exits 0, scenario
      count unchanged.

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [ ] [AI] The Wave-B accounting gate returned **0** before any body was authored.
- [ ] [AI] `for id in "${ERP_WAVE_B[@]}"; do test -d "<COURSES>$id" || echo "MISSING $id"; done | wc -l`
      returns **0** (returned **5** before this phase).
- [ ] [AI] `grep -oE '^ *- ' <ERPMAN> | wc -l` returns **15**; the Wave-C/D deferral check returns
      **0**.
- [ ] [AI] `record-to-report-systems` declares `financial-statements-and-close-cycle`;
      `inventory-and-warehouse-management` declares `inventory-and-cogs-accounting`;
      `erp-analytics-and-reporting` names `data-engineering`.
- [ ] [AI] `npx nx run ayokoding-www:test:unit` + `:build` + `:specs:behavior:coverage` **and**
      `npx nx run ayokoding-www-fe-e2e:test:e2e` exit 0.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: **ramp boundary 2 is live.** Courses #1-#10 all exist, so the path delivers correct
> core process flows, safe extension, and the right integration pattern — a coherent product even if
> nothing further ships. The remaining five ids are deferred with a provable check. Safe to stop
> indefinitely. To resume: `npx nx run ayokoding-www:test:unit`.

---

## Phase 4: Wave C — three bodies and growth to eighteen

> _Suggested executors: `apps-ayokoding-www-by-example-maker` (1 body) and
> `apps-ayokoding-www-annotated-concept-maker` (2 bodies)._
>
> Enterprise-scale concerns: payroll and hire-to-retire, multi-company and multi-currency, and
> security and controls. Each carries a direct accounting edge.

### 4.1 · Accounting gate (hard)

- [ ] [AI] **Wave-C accounting gate** — sync to `origin/main` and confirm all three accounting bundles
      resolve: `for id in "${ACCT_GATE_C[@]}"; do test -d "<COURSES>$id" || echo "MISSING $id"; done | wc -l`
      — acceptance: returns **0**. Falsifiable both ways: it returns **3** today. If it does not
      return 0, **stop and wait**.

### 4.2 · Author the three Wave-C bodies

- [ ] [AI] `human-capital-management-and-hire-to-retire` (Annotated-concept) — declares
      `payroll-and-tax-accounting-essentials` — acceptance: all seven convention steps complete; zero
      CRITICAL/HIGH/MEDIUM; **and**
      `grep -F -q 'payroll-and-tax-accounting-essentials' "<COURSES>human-capital-management-and-hire-to-retire/_index.md"`
      exits 0.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] `multi-company-and-multi-currency-erp` (By Example) — declares
      `consolidation-and-multi-entity-accounting` and `record-to-report-systems` — acceptance: all
      seven steps complete; zero CRITICAL/HIGH/MEDIUM; **and**
      `for id in consolidation-and-multi-entity-accounting record-to-report-systems; do grep -F -q "$id" "<COURSES>multi-company-and-multi-currency-erp/_index.md" || echo "MISSING $id"; done | wc -l`
      returns **0**.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `erp-security-and-controls` (Annotated-concept) — states its scope boundary against
      `it-governance-grc`: RBAC/SoD and COSO-SOX specifics only (DD-10) — acceptance: all seven steps
      complete; zero CRITICAL/HIGH/MEDIUM; **and**
      `grep -F -q 'it-governance-grc' "<COURSES>erp-security-and-controls/overview.md"` exits 0 (exits
      1 before this step).
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] Add all three ids to `<COURSES>_index.md` — acceptance:
      `for id in "${ERP_WAVE_C[@]}"; do grep -F -q "$id" <COURSES>_index.md || echo "MISSING $id"; done | wc -l`
      returns **0** (returns **3** before this step).

### 4.3 · TDD cycle — grow the manifest to eighteen

- [ ] [AI] **RED** — extend the manifest unit test to assert all eighteen ids of
      `ERP_WAVE_A` plus `ERP_WAVE_B` plus `ERP_WAVE_C` — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the assertion **fails**, naming the three absent Wave-C ids.

  **Gherkin (binds) →** "Each boundary-risk course states its scope boundary"

  ```gherkin
  Scenario: Each boundary-risk course states its scope boundary
    Given the analytics, security, and implementation-methodology ERP courses are authored
    When a reader compares each with the existing library course it abuts
    Then each course overview names the neighbouring course explicitly
    And each states what it deliberately leaves to that neighbour
  ```

- [ ] [AI] **GREEN** — insert the three Wave-C ids at their correct ramp positions
      (`human-capital-management-and-hire-to-retire` and `multi-company-and-multi-currency-erp` and
      `erp-security-and-controls` between `demand-and-supply-planning` and
      `erp-analytics-and-reporting`) — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0, AND
      `for id in "${ERP_WAVE_C[@]}"; do grep -F -q "$id" <ERPMAN> || echo "MISSING $id"; done | wc -l`
      returns **0** (returned **3** at the Phase-3 gate), AND `grep -oE '^ *- ' <ERPMAN> | wc -l`
      returns **18** (returned **15**), AND
      `for id in "${ERP_WAVE_D[@]}"; do grep -F -q "$id" <ERPMAN> && echo "PRESENT $id"; done | wc -l`
      returns **0**.
- [ ] [AI] **REFACTOR** — re-run prerequisite-consistency; fix any smoothness regression by bridging
      prose in place, never by reordering — command:
      `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:lint` — acceptance: both exit 0.
- [ ] [AI] **All-three-boundaries check** — confirm every scope-boundary body names its neighbour:
      `grep -F -q 'data-engineering' "<COURSES>erp-analytics-and-reporting/overview.md" && grep -F -q 'it-governance-grc' "<COURSES>erp-security-and-controls/overview.md" && grep -F -q 'project-management' "<COURSES>erp-implementation-methodology/overview.md"`
      — acceptance: the chain exits **0**. Falsifiable both ways: dropping any one boundary line makes
      the chain exit non-zero.

### Phase 4 Gate

> All checks below must pass before starting Phase 5.

- [ ] [AI] The Wave-C accounting gate returned **0** before any body was authored.
- [ ] [AI] `for id in "${ERP_WAVE_C[@]}"; do test -d "<COURSES>$id" || echo "MISSING $id"; done | wc -l`
      returns **0**.
- [ ] [AI] `grep -oE '^ *- ' <ERPMAN> | wc -l` returns **18**; the Wave-D deferral check returns **0**.
- [ ] [AI] The all-three-boundaries chained check exits **0**.
- [ ] [AI] `npx nx run ayokoding-www:test:unit` + `:build` + `:specs:behavior:coverage` **and**
      `npx nx run ayokoding-www-fe-e2e:test:e2e` exit 0.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: eighteen of twenty courses are live and the manifest is prerequisite-consistent
> over all of them; the two remaining ids are deferred with a provable check. The path covers every
> conventional ERP concern — only the Sharia design course and the terminal capstone remain. Safe to
> stop indefinitely. To resume: `npx nx run ayokoding-www:test:unit`.

---

## Phase 5: Wave D — two bodies and growth to twenty (boundary 3)

> _Suggested executors: `apps-ayokoding-www-annotated-concept-maker` (1 body) and
> `apps-ayokoding-www-by-example-maker` (1 body), with `web-researcher` for the jurisdictional
> standards facts._
>
> The Sharia design course and the terminal capstone. This phase closes **ramp boundary 3**: full
> competence across the corpus.

### 5.1 · Accounting gate (hard)

- [ ] [AI] **Wave-D accounting gate** — sync to `origin/main` and confirm all three accounting bundles
      resolve: `for id in "${ACCT_GATE_D[@]}"; do test -d "<COURSES>$id" || echo "MISSING $id"; done | wc -l`
      — acceptance: returns **0**. Falsifiable both ways: it returns **3** today. If it does not
      return 0, **stop and wait** — `sharia-compliant-erp-design` written without
      `sharia-accounting-and-aaoifi-standards` and `islamic-contract-modeling-for-systems` would
      re-derive accounting doctrine inside an ERP course, which is exactly the duplication the
      cross-domain edges exist to prevent.

### 5.2 · Author the two Wave-D bodies

- [ ] [AI] `sharia-compliant-erp-design` (Annotated-concept) — the engineering lesson is
      **jurisdictional pluggability**: the chart of accounts, recognition rules, and disclosure set are
      configuration, not hardcoded constants (DD-12). The body names all three models — AAOIFI
      (Bahrain), Indonesia's PSAK Syariah (AAOIFI as _basis_, not adopted), and Malaysia's MFRS plus
      the Bank Negara Malaysia Shariah Governance Policy 2019 — and states that **Malaysia is not on
      AAOIFI's mandatory-adoption list**. Any numbered PSAK standard obeys the Phase-1.2 resolution —
      acceptance: all seven convention steps complete; zero CRITICAL/HIGH/MEDIUM; **and**
      `for s in AAOIFI 'PSAK Syariah' MFRS 'Bank Negara'; do grep -F -q "$s" "<COURSES>sharia-compliant-erp-design/overview.md" || echo "MISSING $s"; done | wc -l`
      returns **0** (returns **4** before this step); **and** the two accounting prerequisites are
      declared —
      `for id in islamic-contract-modeling-for-systems sharia-accounting-and-aaoifi-standards; do grep -F -q "$id" "<COURSES>sharia-compliant-erp-design/_index.md" || echo "MISSING $id"; done | wc -l`
      returns **0**.

  **Gherkin (binds) →** "The Sharia ERP course is jurisdiction-plural"

  ```gherkin
  Scenario: The Sharia ERP course is jurisdiction-plural
    Given the sharia-compliant-erp-design course is authored
    When a reader looks for the applicable accounting standard
    Then the course names AAOIFI, Indonesia's PSAK Syariah, and Malaysia's MFRS with the Bank Negara Shariah Governance Policy
    And it presents jurisdictional pluggability as the engineering requirement rather than naming one standard as canonical
  ```

  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker` + `web-researcher`_

- [ ] [AI] `capstone-build-a-minimal-erp-core` (By Example) — the terminal capstone; declares
      `capstone-build-a-general-ledger-system` plus the five ERP prerequisites (#19, #9, #5, #6, #8).
      Per DD-14 no code sample depends on a live third-party ERP — acceptance: all seven steps
      complete; zero CRITICAL/HIGH/MEDIUM; **and**
      `for id in capstone-build-a-general-ledger-system sharia-compliant-erp-design erp-extension-and-customization procure-to-pay-systems order-to-cash-systems inventory-and-warehouse-management; do grep -F -q "$id" "<COURSES>capstone-build-a-minimal-erp-core/_index.md" || echo "MISSING $id"; done | wc -l`
      returns **0**.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Add both ids to `<COURSES>_index.md` — acceptance:
      `for id in "${ERP_WAVE_D[@]}"; do grep -F -q "$id" <COURSES>_index.md || echo "MISSING $id"; done | wc -l`
      returns **0** (returns **2** before this step).

### 5.3 · TDD cycle — grow the manifest to twenty

- [ ] [AI] **RED** — extend the manifest unit test to assert all twenty ids of `ERP_ALL` in ramp
      order — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the assertion **fails**, naming the two absent Wave-D ids.

  **Gherkin (binds) →** "The path links cross-domain prerequisites instead of walking them"

  ```gherkin
  Scenario: The path links cross-domain prerequisites instead of walking them
    Given the ERP path manifest is published
    When a reader inspects its courseOrder
    Then no existing software-engineering course and no accounting course appears in courseOrder
    And the landing links out to those courses' canonical pages instead
  ```

- [ ] [AI] **GREEN** — append the two Wave-D ids at the ramp tail — command:
      `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0, AND
      `for id in "${ERP_ALL[@]}"; do grep -F -q "$id" <ERPMAN> || echo "MISSING $id"; done | wc -l` returns
      **0** (returned **2** at the Phase-4 gate), AND `grep -oE '^ *- ' <ERPMAN> | wc -l` returns
      **20** (returned **18**).
- [ ] [AI] **Cross-domain exclusion check** — confirm no existing-library and no accounting id leaked
      into `courseOrder`:
      `for id in backend-essentials api-design event-driven-architecture networking-essentials security-essentials data-engineering analytics-and-experimentation project-management "${ACCT_GATE_B[@]}" "${ACCT_GATE_C[@]}" "${ACCT_GATE_D[@]}"; do grep -F -q "$id" <ERPMAN> && echo "LEAKED $id"; done | wc -l`
      — acceptance: returns **0** at every phase from 2 onward. Falsifiable both ways: adding one
      linked-not-walked id to `courseOrder` makes it **1**.
- [ ] [AI] **REFACTOR** — final prerequisite-consistency and smoothness pass over the full twenty-course
      ramp; fix any regression by bridging prose in place, never by reordering — command:
      `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:lint` — acceptance: both exit 0.

### 5.4 · Boundary 3 and the acyclicity check

- [ ] [AI] **RED** — add a failing e2e assertion for boundary 3 on the landing — command:
      `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: the new spec **fails**.
- [ ] [AI] **GREEN** — update `<ERPLANDING>` so boundary 3 is stated as reached and bind the assertion
      — command:
      `npx nx run ayokoding-www:specs:behavior:coverage && npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: both exit 0.
- [ ] [AI] **REFACTOR** — collapse the three boundary assertions into the parameterised step group —
      command: `npx nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: exits 0, scenario count
      unchanged.
- [ ] [AI] **Acyclicity check** — confirm no accounting course declares an ERP course as a
      prerequisite:
      `for id in "${ERP_ALL[@]}"; do for a in "${ACCT_GATE_B[@]}" "${ACCT_GATE_C[@]}" "${ACCT_GATE_D[@]}"; do grep -F -q "$id" "<COURSES>$a/_index.md" && echo "CYCLE $a -> $id"; done; done | wc -l`
      — acceptance: returns **0**. Falsifiable both ways: an accounting `_index.md` naming any ERP id
      would make it ≥ 1.

  **Gherkin (binds) →** "No ERP course is a prerequisite of any accounting course"

  ```gherkin
  Scenario: No ERP course is a prerequisite of any accounting course
    Given both skills corpora are published
    When the prerequisite graph is inspected
    Then no accounting course declares an ERP course as a prerequisite
    And the ERP subgraph is downstream-only, so the two corpora form no cycle
  ```

### Phase 5 Gate

> All checks below must pass before starting Phase 6.

- [ ] [AI] The Wave-D accounting gate returned **0** before any body was authored.
- [ ] [AI] `for id in "${ERP_ALL[@]}"; do test -d "<COURSES>$id" || echo "MISSING $id"; done | wc -l` returns
      **0** (returned **20** at the Phase-0 snapshot).
- [ ] [AI] `grep -oE '^ *- ' <ERPMAN> | wc -l` returns **20**; the cross-domain exclusion check
      returns **0**; the acyclicity check returns **0**.
- [ ] [AI] `sharia-compliant-erp-design` names all three jurisdictional models.
- [ ] [AI] `npx nx run ayokoding-www:test:unit` + `:build` + `:specs:behavior:coverage` **and**
      `npx nx run ayokoding-www-fe-e2e:test:e2e` exit 0.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: **ramp boundary 3 is live** — the ERP path is content-complete at twenty courses,
> the manifest is at full composition, and no deferral remains open. Safe to stop indefinitely. To
> resume: `npx nx run ayokoding-www:build && npx nx run ayokoding-www:test:unit`.

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
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md heading-hierarchy validate` +
      `npm run lint:md` (the actual mechanism — **not** `nx run` targets) — acceptance: the link
      validator prints `All links valid! No broken links found.`; the other two exit 0.

  **Gherkin (binds) →** "The ERP skills path builds and validates green"

  ```gherkin
  Scenario: The ERP skills path builds and validates green
    Given the ERP manifest, its landing, and its twenty course bodies are published
    When the app build, the affected test tiers, and the link and heading validators run
    Then the build and every affected tier succeed
    And manifest integrity and prerequisite consistency report zero violations for the ERP manifest
  ```

- [ ] [AI] **Manifest integrity + prerequisite-consistency sweep** — every `courseOrder` id resolves to
      a bundle under `<COURSES>`; no duplicate id; prerequisite-consistency holds; no forked body —
      command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the integrity check reports **zero** violations for `<ERPMAN>`.
- [ ] [AI] **Verification-hygiene sweep (A4)** — run `apps-ayokoding-www-facts-checker` across all
      twenty ERP bundles — acceptance: zero CRITICAL/HIGH findings; every remaining volatile claim sits
      in a dated accuracy-note sidebar rather than a stable spine.

  **Gherkin (binds) →** "No unverified research claim is published as fact"

  ```gherkin
  Scenario: No unverified research claim is published as fact
    Given the corpus research marks integration surfaces, analyst positioning, and platform versions as unverified
    When any of those claims appears in an authored course body
    Then the claim sits in a dated accuracy-note sidebar or carries an explicit verification marker
    And no such claim appears unqualified in a course's stable spine
  ```

  - _Suggested executor: `apps-ayokoding-www-facts-checker`, then `apps-ayokoding-www-facts-fixer`_

- [ ] [AI] **Ownership boundary check** — confirm this plan wrote nothing outside its own surface:
      `git diff --name-only origin/main...HEAD | grep -E 'manifests/careers/|manifests/skills/accounting' | wc -l`
      returns **0**, AND
      `git diff --name-only origin/main...HEAD | grep -E 'features/course-paths/(shell|core)/' | wc -l`
      returns **0**, AND no structural `_index.md` was created —
      `git diff --name-only --diff-filter=A origin/main...HEAD | grep -E 'paths/(_index|skills/_index|careers/)' | wc -l`
      returns **0** — acceptance: all three return **0**. Falsifiable both ways: touching a careers
      manifest or creating `paths/skills/_index.md` makes the corresponding count ≥ 1.
- [ ] [AI] **Cross-plan link check (this plan's own folder)** —
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md links validate --exclude plans/done --exclude apps/ayokoding-www/content --exclude apps/ose-www/content 2>&1 | grep -F "ayokoding-learning-path-07-skills-erp"`
      — acceptance: the `grep` finds **no** matching line (exit 1). Falsifiable the other way:
      introduce one bad relative link into this folder and the same command prints that file and
      exits 0. `md links validate` accepts **no positional path** and always walks the repo, so "run
      it in this plan's folder" is not expressible — the filter above is the scoped form.

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes
> (Root Cause Orientation). Commit preexisting fixes separately with conventional-commit messages.

### Phase 6 Gate

> All checks below must pass before starting Phase 7.

- [ ] [AI] Affected `typecheck` / `lint` / `test:quick` / `test:unit` / `specs:behavior:coverage`
      exit 0; `ayokoding-www-fe-e2e:test:e2e` exits 0.
- [ ] [AI] Build + link + heading + markdown validation green; the link validator prints
      `All links valid! No broken links found.`
- [ ] [AI] Manifest integrity and prerequisite-consistency report zero violations for `<ERPMAN>`.
- [ ] [AI] The facts checker reports zero CRITICAL/HIGH across all twenty bundles.
- [ ] [AI] All three ownership boundary counts return **0**.
- [ ] [AI] The scoped cross-plan link check finds no line naming this plan's folder.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the whole ERP path passes every automated gate and provably stayed inside its
> ownership boundary. Safe to stop indefinitely. To resume: re-run the affected quality gates and the
> build.

---

## Phase 7: Manual UI verification and Rule-15 three-tester retest

> This plan ships a user-visible path landing plus two populated cards, so the **Rule-15 three-tester
> retest is mandatory** before archival. The **UI-design-funnel is exempt** — no net-new screen or
> component is added here and every design asset is owned by
> `ayokoding-learning-path-03-navigation-ui`; see
> [tech-docs §UI-design-funnel exemption](./tech-docs.md#ui-design-funnel-exemption-recorded-explicitly).
> The **UI gate itself is exempt** with its reason recorded (DD-13), and the **API gate is NOT
> exempt** — the manifest is reachable behavior exercised by the integrity checks and the path-walk
> e2e named above (DD-14).
>
> **Locale scope**: `en` only. `apps/ayokoding-www/content/id/belajar/` holds zero courses and zero
> paths [Repo-grounded], so an `id` walk-through would be fabricated rather than verified (DD-20).

- [ ] [AI] Confirm `en` is the only content locale for the path library — command:
      `test -d apps/ayokoding-www/content/en/learn/paths && test ! -d apps/ayokoding-www/content/id/belajar/paths`
      — acceptance: exits 0 (the `en` paths bucket exists and no `id` sibling exists).
- [ ] [AI] Start the dev server: `npx nx dev ayokoding-www` — acceptance: server up on the app's
      configured port.
- [ ] [AI] For `en` × breakpoints (375 / 768 / 1280 px), via Playwright MCP `browser_navigate` +
      `browser_resize`: open the skills category landing `/en/learn/paths/skills`, confirm the ERP card
      is present and no longer an empty slot; open the ERP landing
      `/en/learn/paths/skills/enterprise-resource-planning` and confirm all three ramp boundaries and
      the runway justification render; then walk 3-4 courses via prev/next confirming `?path=` persists
      and the order matches the manifest — acceptance: all behaviours correct at all three breakpoints.
- [ ] [AI] Deep-link an ERP course with **no** `?path=` and confirm the canonical view renders with the
      "this course is part of" affordance naming the ERP path; then hit an invalid `?path=` and confirm
      the canonical view renders with no error — acceptance: both hold.
- [ ] [AI] Confirm the landing's outbound linked-not-walked prerequisite links resolve — every
      `/en/learn/courses/<id>` link on `<ERPLANDING>` returns 200 — acceptance: zero non-200 responses.
- [ ] [AI] Verify `html[lang]` is `en` and `browser_console_messages` is clean on every screen —
      acceptance: correct lang attribute; **zero** console errors.
- [ ] [AI] Capture one screenshot per screen per breakpoint via `browser_take_screenshot` to
      `evidence/phase-7-<screen>-en-<breakpoint>px.png` — acceptance: files exist in `evidence/`;
      `find evidence -name 'phase-7-*-en-*px.png' | wc -l` returns **6** (2 screens — the skills
      category landing and the ERP path landing — × 3 breakpoints). Falsifiable both ways: a missed
      breakpoint or screen returns fewer.
- [ ] [AI] Document the evidence in this checklist: reference each screenshot
      (`![alt](./evidence/...)`) and note the console/network status per screen.
- [ ] [AI] Run the three live-site testers (the `web-ux-test-fixing-planning` workflow:
      `web-exploratory-tester` + `web-usability-tester` + `web-design-tester`) against the running ERP
      landing, the skills category landing, and sample ERP courses reached from the landing in path
      context — acceptance: EWT/UWT/DWT findings and spec-gaps recorded.
- [ ] [AI] Append each finding below as a new unchecked checkbox, source-attributed
      (`- [ ] EWT-NNN:` / `- [ ] UWT-NNN:` / `- [ ] DWT-NNN: <defect> — fix before archival`); append
      any SG-###/USS-### items to the relevant spec step in Phases 1-5.

### Rule-15 retest follow-ups

- [ ] [AI] _(populated during the retest — every EWT/UWT/DWT defect finding must be fixed and ticked
      before archival; deferral of a defect requires explicit user permission and only when genuinely
      impossible; SG-###/USS-### may be triaged or deferred with written rationale)_

### Phase 7 Gate

> All checks below must pass before starting Phase 8.

- [ ] [AI] The skills category landing shows the ERP card; the ERP landing renders all three ramp
      boundaries and the runway justification; the path walk, the deep-link affordance, and the
      outbound prerequisite links all verified in `en` at 375 / 768 / 1280 px; console clean.
- [ ] [AI] `find evidence -name 'phase-7-*-en-*px.png' | wc -l` returns **6**; each screenshot is
      referenced from this checklist.
- [ ] [AI] Every rule-15 EWT/UWT/DWT defect finding is fixed and ticked, or explicitly permitted to
      defer by the user.
- [ ] [AI] Draft PR opened (retest evidence and any fixes); 3-cycle PR-Review complete; CI green; PR
      `[AI]`-merged; deployed.

> **Pause Safety**: the ERP path UI is verified live and defect-clean in `en`, with committed
> evidence. Safe to stop indefinitely. To resume: re-run the three testers against the running app.

---

## Phase 8: Final origin main integration and CI verification

- [ ] [AI] Confirm no plan PR is still open:
      `gh pr list --search "ayokoding-learning-path-07-skills-erp" --state open --json number --jq 'length'`
      — acceptance: returns **0**; every prior phase branch has been `[AI]`-merged to `main`.
- [ ] [AI] Sync the shared worktree to the latest `origin/main` and run the full affected suite:
      `npx nx affected -t typecheck lint test:quick test:unit specs:behavior:coverage` +
      `npx nx run ayokoding-www-fe-e2e:test:e2e` + `npx nx run ayokoding-www:build`
      — acceptance: all exit 0 on the integrated `main`.
- [ ] [AI] Monitor the final `main` CI run — poll every ~2 minutes with one
      `gh run view --json status,conclusion` per wakeup; never `gh run watch`, never a tight loop
      — acceptance: all GitHub Actions green; fix root causes and push follow-ups (own PR → review →
      `[AI]` merge) until green.
- [ ] [AI] Confirm `prod-ayokoding-www` serves the ERP landing, the twenty course pages, and the ERP
      card on the skills category landing; re-dispatch `apps-ayokoding-www-deployer` if any earlier
      deploy lagged — acceptance: production serves the ERP path end to end.

### Phase 8 Gate

> All checks below must pass before starting Phase 9.

- [ ] [AI] Zero open plan PRs; every prior phase merged to `main`.
- [ ] [AI] Full affected suite + e2e + build green on the integrated `main`; the final `main` CI run is
      green.
- [ ] [AI] `prod-ayokoding-www` serves the ERP path landing and all twenty course pages.

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
- [ ] [AI] **Terminal twenty-course assertion** — verify the ERP path is complete and the manifest is
      at full composition: `for id in "${ERP_ALL[@]}"; do test -d "<COURSES>$id" || echo "MISSING $id"; done | wc -l`
      returns **0**, AND `for id in "${ERP_ALL[@]}"; do grep -F -q "$id" <ERPMAN> || echo "MISSING $id"; done | wc -l`
      returns **0**, AND `grep -oE '^ *- ' <ERPMAN> | wc -l` returns **20**, AND
      `for id in "${ERP_ALL[@]}"; do test -f "<SYL>$id.md" || echo "MISSING $id"; done | wc -l` returns **0**,
      AND `test -f <SYLPATHS>manifest-skills-enterprise-resource-planning.md` exits 0,
      AND `npx nx run ayokoding-www:test:unit` exits 0 — acceptance: all six hold. Falsifiable both
      ways: each returned **20** (or non-zero) at the Phase-0 snapshot.
      **The careers 127-course figure is not asserted here** — it is careers-only (R5 / DD-19) and this
      corpus is additional.
- [ ] [AI] **Scoped cross-plan link check** — re-run the Phase 6 filtered link validation and confirm
      it still finds no line naming this plan's folder. If a referenced sibling plan has archived
      since, confirm every reference in this folder points at its `plans/done/YYYY-MM-DD__…` path —
      acceptance: the filtered `grep` exits 1 and the repo-wide filtered validator prints
      `All links valid! No broken links found.`
- [ ] [AI] Move:
      `git mv plans/in-progress/ayokoding-learning-path-07-skills-erp plans/done/YYYY-MM-DD__ayokoding-learning-path-07-skills-erp`
      using today's completion date (the `evidence/` and `syllabus/` subfolders move with it).
- [ ] [AI] Update `plans/in-progress/README.md` — remove the plan entry.
- [ ] [AI] Update `plans/done/README.md` — add the plan entry with its completion date.
- [ ] [AI] Update any other READMEs that reference this plan (`plans/README.md`,
      `plans/backlog/README.md`), and update the sibling programme plans' cross-references to this
      plan's new archived path in the **same commit** as the `git mv`.
- [ ] [AI] Commit the archival: `chore(plans): move ayokoding-learning-path-07-skills-erp to done`.

### Phase 10 Gate

> All checks below must pass. This is the terminal gate of the `skills/` category.

- [ ] [AI] All twenty ERP bundles exist, all twenty ids are in `<ERPMAN>`, the manifest holds exactly
      twenty list entries, all twenty syllabus specs exist, and `test:unit` and `build` exit 0.
- [ ] [AI] The filtered link check finds no line naming this plan's folder, and the repo-wide filtered
      validator prints `All links valid! No broken links found.`
- [ ] [AI] Plan folder is under `plans/done/YYYY-MM-DD__ayokoding-learning-path-07-skills-erp`; every
      referencing README is updated; the archival is committed.
- [ ] [AI] Draft PR opened (archival move); 3-cycle PR-Review complete; CI green; PR `[AI]`-merged;
      deployed (no-op).

> **Pause Safety**: the plan is archived and its final PR `[AI]`-merged to `main`. Terminal state — and
> once the sibling accounting plan archives too, the whole `skills/` category is complete. To resume:
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
- [ ] [AI] `npx nx run ayokoding-www-fe-e2e:test:e2e` exits 0 for any phase touching the manifest, the
      landing, or a course bundle.
- [ ] [AI] Fix ALL failures — including preexisting issues not caused by your changes (Root Cause
      Orientation).

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes.
> Commit preexisting fixes separately with appropriate conventional-commit messages.
