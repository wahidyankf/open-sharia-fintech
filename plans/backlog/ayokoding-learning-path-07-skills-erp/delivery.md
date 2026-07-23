# Delivery Checklist — Skills Paths: Enterprise Resource Planning

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

Four standing constraints govern every step below.

> **Cross-plan source of truth**: the ERP catalog — course ids, formats, prerequisite edges, ramp
> order — is settled in
> [tech-docs.md §The ERP catalog](./tech-docs.md#the-erp-catalog-30-courses-settled). Transcribe it;
> do not re-derive it. The syllabus module/topic content is settled in
> [`syllabus/courses/`](./syllabus/README.md). Transcribe it into course bodies; do not re-derive it.
>
> **The category ownership invariant (binding)**: this plan owns `<CONVMAN>`, `<SHARMAN>`,
> `<CONVLANDING>`, `<SHARLANDING>`, the thirty ERP course bundles, and `<SYL>`/`<SYLPATHS>`. It
> **never** writes an accounting file, a careers manifest, a component, a design asset, or a
> structural `_index.md`. A step here that authors accounting material is a boundary violation and is
> equally forbidden in the other direction.
>
> **Verification hygiene (A4/A12)**: the ERP research is almost entirely `[Unverified]`. No claim
> marked `[Unverified]` or `[Needs Verification]` may be written as fact. Syllabus confirmation
> (Phase 1.2a) is coverage-only and never reorders a syllabus's structure — see
> [tech-docs.md §Syllabus confirmation order](./tech-docs.md#syllabus-confirmation-order-a12).
>
> **Id-shape rule (schema-owner ruling, DD-21)**: each path id is the **full** string
> (`skills/conventional-erp` or `skills/sharia-erp`) — no separate `category` field, and **nothing
> keys on segment count**. Every URL/id match below is a **full-string literal** (`grep -F -q`) rather
> than a segment-shaped regex. Course ids carry no category prefix.

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
authors its work there, commits, pushes that branch, and opens **its own draft PR** — from
**Phase 1 onward**. **Phase 0 is excluded**: it is setup and baseline, pushes no branch and opens no
PR, and its evidence artifacts ride the Phase 1 PR.

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans.md#worktree-specification).

## Delivery Mode: worktree-to-pr

Each **delivery** phase — **Phase 1 onward**; Phase 0 opens none — works in the shared worktree on
its **own branch**, opens a **draft PR** against `main`,
runs the **PR-Review Maker→Fixer Cycle** (fan-out → `pr-review-synthesis-maker` → `pr-review-fixer`, 3 sequential CI-gated
cycles), flips the PR to ready, and `[AI]` **merges it once all quality gates are green** — then
`[AI]` **deploys `ayokoding-www` to `prod-ayokoding-www` after every merge** (this plan ships to
ayokoding.com). This plan declares **no** `[HUMAN]` merge gate. See
[Plans Organization Convention §Delivery Mode](../../../repo-governance/conventions/structure/plans.md#delivery-mode)
and the [PR Review Quality Gate workflow](../../../repo-governance/workflows/pr/pr-review-quality-gate.md).

**Per-Phase Integration Protocol — Phase 1 onward** (each delivery phase's gate lists these as
must-pass). **Phase 0 is excluded**: it is Environment Setup and Baseline, opens no PR, pushes no
branch, runs no review cycle, and merges nothing; its evidence artifacts ride the Phase 1 PR
([§Phase 0 Opens No PR](../../../repo-governance/conventions/structure/plans.md#phase-0-opens-no-pr--the-earliest-pr-is-phase-1-hard-rule)).

1. [AI] Sync the shared worktree to latest `origin/main` and branch:
   `git fetch origin && git checkout main && git pull && git checkout -b ayokoding-learning-path-07-skills-erp/<phase-slug>`.
2. [AI] Stage only this phase's paths (`git add <explicit paths>` — never `git add -A`), commit
   thematically (Conventional Commits, imperative, no period), push the branch, open a **draft PR**
   against `main` (`gh pr create --draft --base main ...`) — CI runs on the PR.
3. [AI] Run the **PR-Review Maker→Fixer Cycle** (3 sequential CI-gated cycles), resolve every finding,
   then `gh pr ready`.
4. [AI] **Merge** once all quality gates are green (typecheck, lint, `test:quick`, `test:unit`,
   `ayokoding-www-fe-e2e:test:e2e` where affected — **not** `ayokoding-www:test:e2e`, which is a
   no-op echo stub — `specs:behavior:coverage`, CI, the 3-cycle review).
5. [AI] Dispatch `apps-ayokoding-www-deployer` to deploy `ayokoding-www` to `prod-ayokoding-www` — a
   content/data-only plan still deploys, since the manifests and course bundles are reachable
   behavior. Verify the deploy via `curl -sf https://ayokoding.com/en/learn/paths/skills/conventional-erp | grep -qi "conventional"`
   (after Phase 2) or the equivalent `sharia-erp` URL (after Phase 4).

> **Important — fix ALL failures found during quality gates, not just those caused by your changes.**
> This is the Root Cause Orientation principle applied to every phase's typecheck/lint/`test:quick`
> run above (step 4): a preexisting failure encountered while running an affected quality gate is
> fixed inline as part of this plan's own work, never deferred or mentioned-and-skipped.

## Depends-on and start preconditions

- **`blockedBy` (hard, must be merged before Phase 0 completes)**:
  `ayokoding-learning-path-01-url-restructure` (the `paths/skills/…` URL grammar and `<COURSES>`
  namespace), `ayokoding-learning-path-02-schema-and-prerequisite-dag` (the `PathManifest` zod schema
  with `arc` and variable-depth `pathId`, the integrity functions), and
  `ayokoding-learning-path-03-navigation-ui` (`path-landing.tsx`, `path-card.tsx`,
  `manifest-repository.ts`, the `?path=` wiring — see
  [tech-docs §Landing content requirements](./tech-docs.md#landing-content-requirements-what-plan-03-cannot-infer)).
  A manifest with no renderer is invisible, so without plan 03 this plan's landings cannot be verified
  at Phase 7 at all.
- **`blockedBy` (soft overall, hard at two stage gates)**:
  `ayokoding-learning-path-06-skills-accounting`, expressed at **stage granularity** — see
  [tech-docs §The 06→07 dependency edge](./tech-docs.md#the-0607-dependency-edge-stage-granularity-not-course-numbers)
  and `DD-4`. Stage A needs nothing from plan 06; Stage B waits on `ACCT_GATE_B` and Stage C on
  `ACCT_GATE_C`, both checked mechanically in Phases 3 and 4 rather than here.
- Start precondition: plans 01, 02 and 03 merged to `origin/main`. Verify each **independently**, so a
  missing plan cannot hide behind another's commits:

  ```bash
  for n in 01-url-restructure 02-schema-and-prerequisite-dag 03-navigation-ui; do
    git log origin/main --oneline | grep -q "ayokoding-learning-path-${n}" \
      || echo "NOT MERGED: ayokoding-learning-path-${n}"
  done
  ```

  Acceptance: **empty output**. An aggregate `grep -c "…-0[123]"` returning ≥ 1 is **not** sufficient —
  it passes when only one of the three has merged. Plan 06 is deliberately **not** in this loop: its
  gating is per-stage and belongs to the `ACCT_GATE_*` checks, not to a start precondition that would
  needlessly block Stage A.

## Parallelization Model

Two manifests share one 27-course corpus, so the corpus is the constraint and the manifests are not.
Within a stage, courses with no prerequisite edge between them author in parallel up to the
concurrency cap; courses with an edge serialize. **Stage A (15 courses) carries no accounting
precondition and runs fully concurrently with plan 06** — only Stage B and Stage C wait on their
`ACCT_GATE_*` checks, which is what makes the 06→07 edge soft overall and hard only at those two
gates. The two manifests' TDD growth cycles are separate, parallelizable sub-phases once their shared
courses exist: `<CONVMAN>` stops growing at 27 while `<SHARMAN>` continues to 30, so after §3.2 they
no longer contend. See
[tech-docs §Authoring stages vs reading ramp](./tech-docs.md#authoring-stages-vs-reading-ramp-dd-3)
for the topological ordering this parallelization respects.

## Shell constants (reused across phases)

```bash
# Run from the repo root. Detects this plan's current lifecycle stage and re-derives every path.
# Never hardcode `plans/backlog/…`: this plan is archived with a `git mv` in Phase 7, and any
# clause still pointing at the old folder sweeps a path that no longer exists, returns empty, and
# passes vacuously. Mirrors plan 06's own PLANDIR block.
if [ -d "plans/backlog/ayokoding-learning-path-07-skills-erp" ]; then
  PLANDIR="plans/backlog/ayokoding-learning-path-07-skills-erp/"
elif [ -d "plans/in-progress/ayokoding-learning-path-07-skills-erp" ]; then
  PLANDIR="plans/in-progress/ayokoding-learning-path-07-skills-erp/"
else
  PLANDIR=$(find plans/done -maxdepth 1 -type d -name "*ayokoding-learning-path-07-skills-erp" | head -1)/
fi
echo "PLANDIR=$PLANDIR"
[ -d "$PLANDIR" ] || { echo "PLANDIR-UNRESOLVED — every sweep below would pass vacuously"; }

COURSES="apps/ayokoding-www/content/en/learn/courses/"
PATHS="apps/ayokoding-www/content/en/learn/paths/"
MANIFESTS="apps/ayokoding-www/src/features/course-paths/manifests/"
CONVMAN="${MANIFESTS}skills/conventional-erp.yaml"
SHARMAN="${MANIFESTS}skills/sharia-erp.yaml"
MTEST_CE="${MANIFESTS}skills/conventional-erp-manifest.unit.test.ts"
MTEST_SE="${MANIFESTS}skills/sharia-erp-manifest.unit.test.ts"
CONVLANDING="${PATHS}skills/conventional-erp/_index.md"
SHARLANDING="${PATHS}skills/sharia-erp/_index.md"
SYL="${PLANDIR}syllabus/courses/"

# Stage A — 15 ids, no accounting precondition
ERP_STAGE_A=(
  erp-foundations-and-history erp-conceptual-data-model erp-module-map-and-architecture
  erp-document-lifecycle-and-state-machines erp-posting-rules-and-account-determination
  erp-subledger-to-gl-architecture erp-fiscal-calendar-and-period-close
  erp-numbering-sequences-and-uom-conversion erp-audit-trail-and-change-tracking
  procure-to-pay-systems order-to-cash-systems erp-procurement-and-fulfillment-exceptions
  erp-bom-and-routing-architecture erp-extension-and-customization erp-integration-patterns
)

# Stage B — 12 ids, gated on ACCT_GATE_B
ERP_STAGE_B=(
  record-to-report-systems inventory-and-warehouse-management erp-inventory-costing-methods
  erp-inventory-integrity-and-concurrency production-planning-and-mrp demand-and-supply-planning
  erp-availability-and-reservations quality-management-and-inspection
  human-capital-management-and-hire-to-retire
  multi-company-and-multi-currency-erp erp-security-and-controls erp-analytics-and-reporting
)

# Stage C — 3 ids, sharia-erp only, gated on ACCT_GATE_C
ERP_STAGE_C=(
  sharia-compliant-erp-design islamic-contract-based-transaction-flows
  zakat-and-sharia-compliance-modules
)

ERP_ALL=("${ERP_STAGE_A[@]}" "${ERP_STAGE_B[@]}" "${ERP_STAGE_C[@]}")

# Accounting gates — mechanical test -d checks against ayokoding-learning-path-06-skills-accounting's
# own course bundles on origin/main. See tech-docs.md's cross-plan coordination-risk note: these ids
# are as named in plan 06's own in-flight rewrite as of 2026-07-22 and must be re-verified before use.
ACCT_GATE_B=(
  financial-statements-and-close-cycle inventory-and-cogs-accounting
  payroll-and-tax-accounting-essentials consolidation-and-multi-entity-accounting
  audit-controls-and-compliance
)
ACCT_GATE_C=(
  islamic-contract-modeling-for-systems sharia-accounting-and-aaoifi-standards
)

# No id in ERP_ALL is a substring of another, and none collides with an accounting or
# existing-library course id — verified at Phase 0.
```

## Phase 0: Environment Setup

- [ ] [AI] All three hard blocking plans (01, 02, 03) merged to `origin/main` — run the per-plan loop
      in [§Depends-on](#depends-on-and-start-preconditions); acceptance: empty output. Plan 06 is
      gated per-stage in Phases 3 and 4, not here.
- [ ] [AI] Install dependencies: `npm install`.
- [ ] [AI] Run doctor to verify tooling: `npm run doctor -- --fix`.
- [ ] [AI] Verify dev server starts: `nx dev ayokoding-www`.
- [ ] [AI] Verify existing tests pass before making changes:
      `nx run ayokoding-www:test:quick`.
- [ ] [AI] **Cardinality guard — run before the three checks below, which are all vacuous against an
      unset array**:
      `[ "${#ERP_ALL[@]}" -eq 30 ] && [ "${#ACCT_GATE_B[@]}" -eq 5 ] && [ "${#ACCT_GATE_C[@]}" -eq 2 ] && echo GUARD-OK || echo GUARD-FAIL`
      — acceptance: prints `GUARD-OK`. If the constants block above was not sourced, every `for … in
"${ERP_ALL[@]}"` sweep in this plan iterates zero times and reports success.
- [ ] [AI] Verify no id in `ERP_ALL` already exists under `<COURSES>`:
      `for id in "${ERP_ALL[@]}"; do test -d "${COURSES}${id}" && echo "COLLISION: $id"; done | grep -q . && echo FAIL || echo PASS`
      — acceptance: prints `PASS`.
- [ ] [AI] Verify **no id in `ERP_ALL` is a substring of another** — this is a separate check from the
      one above, which only tests for pre-existing directories and cannot detect substring overlap:
      `for a in "${ERP_ALL[@]}"; do for b in "${ERP_ALL[@]}"; do [ "$a" != "$b" ] && case "$b" in *"$a"*) echo "SUBSTRING: $a ⊂ $b";; esac; done; done | grep -q . && echo FAIL || echo PASS`
      — acceptance: prints `PASS`.
      **Control probe before believing the `PASS`**: temporarily append a known-colliding id (e.g.
      `erp-security`) to a copy of the array and re-run — it must print `FAIL`. A check that cannot be
      made to fail is not measuring anything.
- [ ] [AI] Verify no id collides with an accounting id: `comm -12 <(printf '%s\n' "${ERP_ALL[@]}" | sort) <(printf '%s\n' "${ACCT_GATE_B[@]}" "${ACCT_GATE_C[@]}" | sort)` — acceptance: empty output.

### Phase 0 Gate

- [ ] [AI] All four checks above pass; `nx run ayokoding-www:test:quick` is green on a clean tree.

> **Pause Safety**: no plan file yet modified. Safe to stop. To resume: re-run
> `nx run ayokoding-www:test:quick`.

## Phase 1: Syllabus Authoring and Verification

Per [tech-docs.md §Syllabus layer](./tech-docs.md#syllabus-layer--custody-and-shape-dd-31), authoring
precedes confirmation, and confirmation is coverage-only (`A12`).

### 1.1 — Author all 30 syllabus specs (already drafted; this step verifies, not re-authors)

- [x] [AI] `${PLANDIR}syllabus/README.md` (the index sits one level **above** `<SYL>`, not inside it)
      and all 30 `<SYL><id>.md` files exist, each with the required section set (header block, Scope
      note ending `License-aware (DD-15)`, Why this exists, Prerequisites, Accuracy notes, Concepts,
      Worked examples, Synthesis exercise, Read more, In which paths). Verify:

  ```bash
  test -f "${PLANDIR}syllabus/README.md" || echo "MISSING: syllabus/README.md"
  for id in "${ERP_ALL[@]}"; do test -f "${SYL}${id}.md" || echo "MISSING: $id"; done
  ```

  Acceptance: **empty output**. Guard first — `[ "${#ERP_ALL[@]}" -eq 30 ] && echo GUARD-OK` must
  print `GUARD-OK`, or the loop iterates zero times and the emptiness means nothing.

- [x] [AI] Both path mirrors exist and **each** enumerates its own full `courseOrder` — the previous
      version of this clause checked only the Sharia mirror while claiming to check both, and its
      command was corrupted by an unescaped backtick. `conventional-erp` carries 27 ids and
      `sharia-erp` carries 30; together they cover all 30 distinct ids (27 shared + 3
      Sharia-exclusive):

  ```bash
  SYLPATHS="${PLANDIR}syllabus/paths/"
  conv=$(grep -cE '^[0-9]+\. `' "${SYLPATHS}manifest-skills-conventional-erp.md")
  shar=$(grep -cE '^[0-9]+\. `' "${SYLPATHS}manifest-skills-sharia-erp.md")
  union=$(cat "${SYLPATHS}manifest-skills-conventional-erp.md" "${SYLPATHS}manifest-skills-sharia-erp.md" \
    | grep -oE '^[0-9]+\. `[a-z0-9-]+`' | sed 's/^[0-9]*\. //; s/`//g' | sort -u | grep -c .)
  echo "conv=$conv shar=$shar union=$union"
  [ "$conv" -eq 27 ] && [ "$shar" -eq 30 ] && [ "$union" -eq 30 ] && echo PASS || echo FAIL
  ```

  Acceptance: prints `conv=27 shar=30 union=30` then `PASS`. **Control probe**: delete one id line
  from a scratch copy and re-run — it must print `FAIL`.

### 1.2 — The A4 verification pass before any spec asserts a fact

- [ ] [AI] **Cardinality guard first — this clause is meaningless without it.**
      `[ "$(find "${SYL}" -maxdepth 1 -name '*.md' ! -name 'README.md' | wc -l)" -eq 30 ] && echo GUARD-OK || echo GUARD-FAIL`
      — acceptance: prints `GUARD-OK`. A wrong `$SYL` (for example, one still pointing at a lifecycle
      folder the plan has moved out of) makes every sweep below return empty and pass vacuously; this
      guard is what makes the emptiness meaningful. The count excludes `syllabus/courses/README.md`
      (required by the Learning-Bearing Syllabus Completeness convention) — a naive
      `ls "${SYL}"*.md | wc -l` would match the README too and return 31, misfiring on the very state
      this check is meant to confirm as correct.
- [ ] [AI] For every syllabus's "Accuracy notes" section, confirm every `[Verified]` claim traces to
      the domain reasoning already recorded in `tech-docs.md` or a fetched primary source, and every `[Unverified]` /
      `[Needs Verification]` claim is **not** restated as fact elsewhere in the same file — verify
      every file carries at least one A4 marker **or** legitimately states the Phase 1.2a confirmation
      pass has not yet run for that course, per
      [tech-docs.md §Syllabus layer](./tech-docs.md#syllabus-layer--custody-and-shape-dd-31)'s own
      authoring rule that Accuracy notes honestly record a pending confirmation pass rather than
      fabricate a verification date. Honest "has not yet run" prose is not a stray anti-hallucination
      bracket and is not itself an A4 violation — the invariant this clause enforces is **no unmarked
      claim**, not **every file marked**:
      `for f in $(find "${SYL}" -maxdepth 1 -name '*.md' ! -name 'README.md'); do grep -qE '\[(Verified|Unverified|Needs Verification|Judgment call)\]' "$f" && continue; grep -qF 'has not yet run' "$f" && continue; echo "NO-MARKER-AND-NOT-PENDING: $f"; done | grep -c .`
      returns **0**. Do **not** use `grep -L` here: it lists files _without_ a match and exits 0 when
      it finds one, so the clause would be unfalsifiable.
      **Control probe before believing the zero**: append `x` to **both** patterns (making neither
      match) and re-run — the count must jump to 30. If it does not, the sweep is not measuring what
      it claims and the zero is false.
      A file whose Accuracy notes section is present but **empty** — carrying neither a marker nor the
      "has not yet run" pending statement anywhere in the file — fails this clause even if a marker
      appears elsewhere in the file; check that section specifically.
- [ ] [AI] Re-verify the two open items named in `tech-docs.md` before Phase 4 begins (they gate
      Stage C, not Stage A/B): the PSAK-numbering question in
      `sharia-compliant-erp-design.md`, and the AAOIFI/PSAK/MASB jurisdictional-model table. Dispatch
      `web-researcher` against AAOIFI's and IAI's own published standards indexes; update the syllabus
      files' Accuracy notes with the verified answer or an explicit `[Needs Verification]` carry-
      forward — never silently drop the marker.

### 1.2a — `web-researcher` confirmation pass (`A12`)

> Coverage-only. Never reorders a syllabus's modules or adopts a curriculum's sequence.

- [ ] [AI] Dispatch `web-researcher` once per syllabus (30 dispatches, or batched by module-family
      where the underlying topic overlaps) asking exactly: "does APICS/ASCM's CPIM or CSCP topic
      outline (for planning/operations content) or the named open-source system's own published
      module structure (for architecture/module-map content, nominative reference only) suggest a
      topic this syllabus's module list omits, or include a topic the field does not recognise?" —
      never "how should these modules be ordered".
- [ ] [AI] For each finding returned, add the missing topic to the relevant module in the syllabus
      file, in this plan's own words, citing the confirming body nominatively (e.g. "corroborated
      against ASCM's CPIM topic outline") — never quoting or reproducing the outline's own text.
- [ ] [AI] Resolve every `[Needs Verification]` tag left in a syllabus's Concepts/module list: either
      confirm and relabel `[Verified]`/`[Repo-grounded]`, or leave `[Needs Verification]` explicitly
      if the pass could not resolve it — never silently drop the tag.

### Phase 1 Gate

- [ ] [AI] `npm run lint:md` is green on all `syllabus/**` files.
- [ ] [AI] Every syllabus file's Accuracy notes section reflects the Phase 1.2/1.2a pass results (no
      file still reads "has not yet run for this course" after this phase completes).
- [ ] [AI] **Integration**: draft PR opened for `syllabus/**` changes only, 3-cycle PR-Review complete,
      CI green, `[AI]` merge, no deploy needed (plan-folder-only change, not a build input).

> **Pause Safety**: `syllabus/` is fully authored and confirmed; no `<COURSES>` or manifest file yet
> exists. Safe to stop. To resume: re-derive `PLANDIR`/`SYL` from the Shell constants block above,
> then `test -f "${SYL}zakat-and-sharia-compliance-modules.md" && echo READY`. Do not hardcode
> `plans/backlog/…` here — this plan is moved with `git mv` in Phase 7, and a hardcoded resume check
> would
> report absence after the move.

## Phase 2: Stage A — Foundations and Architecture

15 courses, no accounting precondition — fully concurrent with `ayokoding-learning-path-06-skills-accounting`.

### 2.1 — Author all 15 Stage A course bodies (maker-checker-fixer, per format)

For each `id` in `ERP_STAGE_A`, following the seven-step NEW-course authoring convention (DD-17:
accuracy pre-verify → skeleton → learning track → drilling track → checkers → fixers → re-verify),
transcribing the module/topic content from `<SYL>${id}.md`:

- [ ] [AI] Accuracy pre-verify: re-check every `[Verified]`/`[Unverified]` claim in
      `<SYL>${id}.md`'s Accuracy notes is current (no drift since Phase 1.2a) — acceptance: every
      marker (`[Verified]`/`[Unverified]`/`[Needs Verification]`/`[Judgment call]`) in that section is
      re-confirmed correct or updated, and zero `[Unverified]`/`[Needs Verification]` claims appear
      restated as settled fact anywhere else in `<SYL>${id}.md`.
- [ ] [AI] Skeleton: create `<COURSES>${id}/_index.md` with frontmatter (`title`, `format`,
      `prerequisites: [...]` transcribed verbatim from the catalog table in `tech-docs.md`) and the
      section scaffold.
- [ ] [AI] Learning track: dispatch `apps-ayokoding-www-annotated-concept-maker` (Annotated-concept
      ids) or `apps-ayokoding-www-by-example-maker` (By Example ids) to author the concept
      explanations, transcribing every `co-NN` from the syllabus — acceptance:
      `grep -oE 'co-[0-9]+' "${COURSES}${id}/_index.md" | sort -u | wc -l` equals
      `grep -oE 'co-[0-9]+' "${SYL}${id}.md" | sort -u | wc -l` (no concept dropped in transcription)
      and is **at least 8** (the DD-35 concept floor).
- [ ] [AI] Drilling track: for By Example ids, author the worked examples transcribed from the
      syllabus's `ex-NN` list (prose worked scenarios, never runnable code standing up a system —
      A6). For Annotated-concept ids, author the equivalent worked-scenario drills — acceptance: for
      By Example ids, `grep -oE 'ex-[0-9]+' "${COURSES}${id}/_index.md" | sort -u | wc -l` equals
      `grep -oE 'ex-[0-9]+' "${SYL}${id}.md" | sort -u | wc -l` (no worked example dropped); for
      Annotated-concept ids, every worked-scenario drill traces to a `co-NN` already present in the
      authored file.
- [ ] [AI] Checkers: dispatch `apps-ayokoding-www-annotated-concept-checker` or
      `apps-ayokoding-www-by-example-checker` plus `apps-ayokoding-www-facts-checker` and
      `apps-ayokoding-www-link-checker` — acceptance: each checker's audit report shows zero
      CRITICAL and zero HIGH findings for `<COURSES>${id}`.
- [ ] [AI] Fixers: dispatch `apps-ayokoding-www-general-fixer`-family agents for every finding —
      acceptance: the fixer report shows zero unresolved CRITICAL/HIGH findings, and a re-run of the
      Checkers step above confirms zero CRITICAL/HIGH findings remain.
- [ ] [AI] Re-verify: `test -d "${COURSES}${id}" && test -f "${COURSES}${id}/_index.md" && echo PASS` —
      acceptance: prints `PASS` for every id in `ERP_STAGE_A`.

### 2.2 — TDD: publish both manifests at 15 ids

**Gherkin (binds) →** "conventional-erp manifest validates against the PathManifest schema"

```gherkin
Scenario: conventional-erp manifest validates against the PathManifest schema
  Given the file "manifests/skills/conventional-erp.yaml"
  When the manifest is loaded and validated
  Then it parses against the PathManifest zod schema
  And its pathId equals "skills/conventional-erp"
  And its arc equals "immediately-effective"
  And its courseOrder contains exactly 27 unique course ids
```

The 27-id assertion is this scenario's **terminal** state, reached at §3.2; this sub-phase publishes
the manifest at 15 ids and the scenario goes green once Stage B growth completes. `<SHARMAN>`'s own
schema scenario is bound separately at §4.2 — one scenario per tag.

- [ ] [AI] **RED** — Write `<MTEST_CE>` and `<MTEST_SE>` _(two new files; this plan owns both)_, each
      asserting its own manifest (`<CONVMAN>` / `<SHARMAN>` respectively) parses against the
      `PathManifest` zod schema, has `pathId` equal to `skills/conventional-erp` /
      `skills/sharia-erp` respectively, `arc: immediately-effective`, and `courseOrder` containing
      exactly the 15 `ERP_STAGE_A` ids in order — run
      `nx run ayokoding-www:test:unit -- conventional-erp-manifest sharia-erp-manifest` and verify
      both **fail** (files do not exist yet).
- [ ] [AI] **GREEN** — Create `<CONVMAN>` and `<SHARMAN>` (both identical at this stage — 15 ids,
      transcribed from `syllabus/paths/manifest-skills-conventional-erp.md` Stage A section) — run
      `nx run ayokoding-www:test:unit -- conventional-erp-manifest sharia-erp-manifest` and verify
      both **pass**.
- [ ] [AI] **REFACTOR** — Run `checkManifestIntegrity` and `checkPrerequisiteConsistency` (from
      `ayokoding-learning-path-02-schema-and-prerequisite-dag`'s `course-paths` core) against both
      manifests; factor a shared load-and-validate test helper so `<MTEST_CE>`/`<MTEST_SE>` and their
      §3.2/§4.2 extensions add assertions, not copied blocks — verify both manifests return zero
      violations.

### 2.3 — Create both path landings and populate cards

- [ ] [AI] Create `<CONVLANDING>` and `<SHARLANDING>` with the content spec from
      [tech-docs.md §Landing content requirements](./tech-docs.md#landing-content-requirements-what-plan-03-cannot-infer)
      (the Dangerous-N ramp table, the L-2 runway justification, and — for `<SHARLANDING>` — the L-5
      "covers all the basics" statement) — using the design system components
      `ayokoding-learning-path-03-navigation-ui` already ships; author **content only**, no new
      component.
- [ ] [AI] Populate two cards each in `<PATHS>_index.md` and `<PATHS>skills/_index.md` (four
      insertions total) — edit only, these files already exist (A3).
- [ ] [AI] Populate 15 rows in `<COURSES>_index.md` — edit only, file already exists (A3).

### 2.4 — TDD: Stage A path-walk coverage

**Gherkin (binds) →** "Stage A landings render and both manifests validate at 15 courses"

```gherkin
Scenario: Stage A landings render and both manifests validate at 15 courses
  Given both manifests are published with courseOrder containing the 15 Stage A ids
  When a reader opens either the conventional-erp or sharia-erp path landing
  Then both landings render and both manifests validate against the PathManifest schema
  And the Dangerous-1 boundary appears correctly on both landings
  And the sharia-erp landing states it "covers all the basics"
```

- [ ] [AI] **RED** — add
      `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/course-paths/skills-erp-paths.feature`
      _(new file)_ carrying the scenario above, plus failing step definitions at
      `apps/ayokoding-www-fe-e2e/src/steps/skills-erp-paths.steps.ts` _(new file, pairing 1:1)_ —
      command: `nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: the new spec **fails** (the feature
      and step-definition files did not exist before this step).
- [ ] [AI] **GREEN** — implement the step bindings against the already-published `<CONVLANDING>` /
      `<SHARLANDING>` and `<CONVMAN>` / `<SHARMAN>` (from §2.2/§2.3) — command:
      `nx run ayokoding-www:specs:behavior:coverage && nx run ayokoding-www-fe-e2e:test:e2e` —
      acceptance: both exit 0, and `specs:behavior:coverage` reports 100% for the new feature file.
- [ ] [AI] **REFACTOR** — extract a reusable "assert a Dangerous-N boundary on a path landing" helper
      step definition, parameterized on path id and boundary number, so §3.5 and §4.5 extend it
      without duplicating step bindings — command: `nx run ayokoding-www-fe-e2e:test:e2e` —
      acceptance: exits 0, scenario count unchanged.

### Phase 2 Gate

- [ ] [AI] `nx run ayokoding-www:test:unit -- conventional-erp-manifest sharia-erp-manifest` green
      (both manifest test suites).
- [ ] [AI] `nx run ayokoding-www-fe-e2e:test:e2e` green for the new feature file. **Not
      `ayokoding-www:test:e2e`** — that target is an `echo 'no-op: target not applicable for this
project'` stub and can never fail, so citing it would make this checkbox vacuous. The real
      Playwright suite carrying this plan's step definitions lives on the sibling
      `ayokoding-www-fe-e2e` project, which is also what plan 06 cites.
- [ ] [AI] `nx run ayokoding-www:typecheck`, `:lint`, `:test:quick` all green.
- [ ] [AI] `for id in "${ERP_STAGE_A[@]}"; do test -d "${COURSES}${id}" || echo "MISSING: $id"; done | grep -q . && echo FAIL || echo PASS` prints `PASS`.
- [ ] [AI] **Integration**: draft PR opened, 3-cycle PR-Review complete, CI green, `[AI]` merge,
      `ayokoding-www` deployed, post-deploy curl check (Per-Phase Integration Protocol step 5) passes
      for both `<CONVLANDING>` and `<SHARLANDING>`.

> **Pause Safety**: both manifests exist at 15 ids; both landings render; Dangerous 1 is live for
> both paths. Safe to stop — a reader visiting either path today gets a coherent, if smaller,
> experience. To resume: `curl -sf https://ayokoding.com/en/learn/paths/skills/conventional-erp | grep -q "Dangerous"`.

## Phase 3: Stage B — Conventional Enterprise Depth

12 courses, gated on `ACCT_GATE_B` resolving on `origin/main`. `conventional-erp` reaches its terminal
27-id state at the end of this phase.

### 3.0 — Gate check (mechanical, independent of plan 06's own delivery tracking)

- [ ] [AI] `for id in "${ACCT_GATE_B[@]}"; do git -C worktrees/ayokoding-learning-path-07-skills-erp fetch origin main -q; git -C worktrees/ayokoding-learning-path-07-skills-erp show "origin/main:${COURSES}${id}/_index.md" >/dev/null 2>&1 || echo "WAITING: $id"; done | grep -q . && echo WAIT || echo READY` —
      if `WAIT`, poll every 2 minutes (per CI-monitoring convention's cadence) rather than
      tight-looping; do not begin 3.1 until `READY`.

### 3.1 — Author all 12 Stage B course bodies

Repeat the 2.1 seven-step cycle for each `id` in `ERP_STAGE_B`, transcribing from `<SYL>${id}.md`.
Two of these ids (`erp-security-and-controls`, `erp-analytics-and-reporting`) additionally require the
scope-boundary self-check worked example (DD-10) to be present and reviewed by
`apps-ayokoding-www-facts-checker` for accuracy against the stated boundary claim.

- [ ] [AI] `for id in "${ERP_STAGE_B[@]}"; do test -d "${COURSES}${id}" || echo "MISSING: $id"; done | grep -q . && echo FAIL || echo PASS` prints `PASS`.

### 3.2 — TDD: grow both manifests to 27 ids

**Gherkin (binds) →** "the shared 27 courses are identical bodies referenced from both manifests"

```gherkin
Scenario: the shared 27 courses are identical bodies referenced from both manifests
  Given a course id present in both "skills/conventional-erp" and "skills/sharia-erp" courseOrder
  When the reader visits that course under either path context
  Then the rendered body content is byte-identical
  And no second copy of the course file exists on disk
```

This is `A11`'s one-body-two-references rule made reachable. `conventional-erp` reaches its terminal
27 ids here and stops at `erp-analytics-and-reporting`.

- [ ] [AI] **RED** — Extend both `<MTEST_CE>` and `<MTEST_SE>` asserting each manifest (`<CONVMAN>` /
      `<SHARMAN>` respectively) contains all 27 shared ids (Stage A's 15 plus Stage B's 12, at the
      insertion positions in
      [tech-docs.md §courseOrder arrays](./tech-docs.md#courseorder-arrays-at-each-growth-boundary)),
      with every Stage A id's relative order unchanged — run
      `nx run ayokoding-www:test:unit -- conventional-erp-manifest sharia-erp-manifest` and verify
      both **fail**.
- [ ] [AI] **GREEN** — Grow `<CONVMAN>` and `<SHARMAN>` to 27 ids each — run
      `nx run ayokoding-www:test:unit -- conventional-erp-manifest sharia-erp-manifest` and verify
      both **pass**.
- [ ] [AI] **REFACTOR** — Re-run `checkManifestIntegrity`/`checkPrerequisiteConsistency` against both
      `<MTEST_CE>` and `<MTEST_SE>`; verify zero violations, including the hard edge
      (`record-to-report-systems` requiring `financial-statements-and-close-cycle` to exist under
      `<COURSES>` on `origin/main`).

### 3.3 — Deferral-check assertion (both directions)

- [ ] [AI] Confirm the **before** half of the falsifiable check recorded in Phase 2: re-run
      `grep -F -q 'record-to-report-systems' <(git show HEAD~1:"${CONVMAN}")` against the pre-growth
      commit and verify it **fails** (the id was genuinely absent before this phase).
- [ ] [AI] Confirm the **after** half: `grep -F -q 'record-to-report-systems' "${CONVMAN}"` **passes**.

### 3.4 — Landing update: Dangerous 2 and Dangerous 3 boundaries

- [ ] [AI] Update `<CONVLANDING>` and `<SHARLANDING>` content to show the Dangerous 2 boundary
      (course 16) and, for `<CONVLANDING>`, the terminal Dangerous 3 boundary (course 27, "ENDS
      HERE").
- [ ] [AI] Populate 12 more rows in `<COURSES>_index.md` (27 total).

### 3.5 — TDD: extend Stage A coverage to the Dangerous 2/3 boundaries

**Gherkin (binds) →** "conventional-erp landing renders with its full course count" — the same
terminal-state scenario `prd.md` already declares, reached here as `conventional-erp` completes its
27-course growth (mirrors plan 06's §2.4→§3.5 progressive-rebind idiom of reusing one pre-existing
`prd.md` scenario across growth stages)

```gherkin
Scenario: conventional-erp landing renders with its full course count
  Given the reader navigates to "/en/learn/paths/skills/conventional-erp"
  When the landing page loads
  Then the landing renders 27 courses in courseOrder order
  And the landing displays the Dangerous 1, Dangerous 2, and Dangerous 3 boundaries
```

- [ ] [AI] **RED** — extend the reusable boundary helper (from §2.4's REFACTOR) in
      `apps/ayokoding-www-fe-e2e/src/steps/skills-erp-paths.steps.ts` to assert the Dangerous 2
      boundary on both landings and the terminal Dangerous 3 / "ENDS HERE" statement on
      `<CONVLANDING>` — command: `nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: the new
      assertions **fail** (only the Dangerous-1 boundary was asserted before this phase).
- [ ] [AI] **GREEN** — implement the step bindings against the grown `<CONVLANDING>` / `<SHARLANDING>`
      content (from §3.4) — command:
      `nx run ayokoding-www:specs:behavior:coverage && nx run ayokoding-www-fe-e2e:test:e2e` —
      acceptance: both exit 0.
- [ ] [AI] **REFACTOR** — parameterize the helper on expected boundary count so §4.5 extends it
      without duplicating assertions — command: `nx run ayokoding-www-fe-e2e:test:e2e` —
      acceptance: exits 0, scenario count unchanged.

### Phase 3 Gate

- [ ] [AI] All Phase 2 Gate checks re-run and still green.
- [ ] [AI] `<CONVMAN>` has exactly 27 `courseOrder` entries; `<SHARMAN>` has exactly 27 (Stage C not
      yet grown) — `grep -cE '^  - ' "${CONVMAN}"` prints `27`.
- [ ] [AI] **Integration**: draft PR opened, 3-cycle PR-Review complete, CI green, `[AI]` merge,
      `ayokoding-www` deployed, post-deploy curl check confirms `<CONVLANDING>` shows "ENDS HERE".

> **Pause Safety**: `conventional-erp` is terminal (27/27); `sharia-erp` is mid-growth (27/30). Safe
> to stop — `conventional-erp` readers get the complete path today. To resume:
> `grep -cE '^  - ' worktrees/ayokoding-learning-path-07-skills-erp/${SHARMAN}` and confirm
> it reads `27`.

## Phase 4: Stage C — Sharia-Compliant Design

3 courses, `sharia-erp` only, gated on `ACCT_GATE_C` resolving on `origin/main`.

### 4.0 — Gate check

- [ ] [AI] `for id in "${ACCT_GATE_C[@]}"; do git -C worktrees/ayokoding-learning-path-07-skills-erp fetch origin main -q; git -C worktrees/ayokoding-learning-path-07-skills-erp show "origin/main:${COURSES}${id}/_index.md" >/dev/null 2>&1 || echo "WAITING: $id"; done | grep -q . && echo WAIT || echo READY` —
      poll every 2 minutes if `WAIT`.
- [ ] [AI] Complete Phase 1.2's deferred re-verification of the PSAK-numbering and jurisdictional-model
      open items before authoring begins, if not already resolved.

### 4.1 — Author all 3 Stage C course bodies

Repeat the 2.1 seven-step cycle for each `id` in `ERP_STAGE_C`, transcribing from `<SYL>${id}.md`.
Every claim in the jurisdictional-model table carries its A4 marker into the course body verbatim
(never restated as settled fact if still `[Unverified]`).

- [ ] [AI] `for id in "${ERP_STAGE_C[@]}"; do test -d "${COURSES}${id}" || echo "MISSING: $id"; done | grep -q . && echo FAIL || echo PASS` prints `PASS`.

### 4.2 — TDD: grow `<SHARMAN>` to 30 ids

**Gherkin (binds) →** "sharia-erp manifest validates against the PathManifest schema"

```gherkin
Scenario: sharia-erp manifest validates against the PathManifest schema
  Given the file "manifests/skills/sharia-erp.yaml"
  When the manifest is loaded and validated
  Then it parses against the PathManifest zod schema
  And its pathId equals "skills/sharia-erp"
  And its courseOrder contains exactly 30 unique course ids
  And its courseOrder position 27 equals "erp-analytics-and-reporting"
  And its courseOrder positions 28 to 30 are the 3 Sharia-exclusive ids in catalog order
  And its final courseOrder entry equals "zakat-and-sharia-compliance-modules"
```

The last three steps are load-bearing, not decorative: a set-membership assertion alone holds under
both the correct ordering and the superseded "insert before `erp-security-and-controls`" rule, so
without them this scenario could not regression-guard the terminal boundary.

- [ ] [AI] **RED** — Extend `<MTEST_SE>` **only** (never `<MTEST_CE>`) asserting `<SHARMAN>` contains
      all 30 ids at the positions in
      [tech-docs.md §courseOrder arrays](./tech-docs.md#courseorder-arrays-at-each-growth-boundary)
      (the 3 Sharia-exclusive ids **appended after the complete 27-id shared corpus**, i.e. after
      `erp-analytics-and-reporting`, occupying positions 28-30 with
      `zakat-and-sharia-compliance-modules` terminal), and confirm `<MTEST_CE>`'s existing assertions
      are untouched (`<CONVMAN>` stays **unaffected**, still 27) — run
      `nx run ayokoding-www:test:unit -- sharia-erp-manifest` and verify it **fails**.
      Assert the terminal id explicitly, not just the set: the test must fail if
      `<SHARMAN>[28]` is anything other than `zakat-and-sharia-compliance-modules`. A set-membership
      assertion alone passes under both the correct and the superseded ordering and cannot
      regression-guard this.
- [ ] [AI] **GREEN** — Grow `<SHARMAN>` to 30 ids — run
      `nx run ayokoding-www:test:unit -- sharia-erp-manifest` and verify it **passes**.
- [ ] [AI] **REFACTOR** — Re-run integrity checks on `<SHARMAN>` only via `<MTEST_SE>`; verify zero
      violations. Confirm `nx run ayokoding-www:test:unit -- conventional-erp-manifest` is still green
      and unmodified.

### 4.3 — Deferral-check assertion (both directions)

- [ ] [AI] Before/after check for `zakat-and-sharia-compliance-modules`, mirroring 3.3's pattern
      against `<SHARMAN>`.

### 4.4 — Landing update: Dangerous 4 boundary

- [ ] [AI] Update `<SHARLANDING>` to show the terminal Dangerous 4 boundary (course 30, "ENDS HERE").
- [ ] [AI] Populate the final 3 rows in `<COURSES>_index.md` (30 total).

### 4.5 — TDD: extend coverage to the terminal Dangerous 4 boundary

**Gherkin (binds) →** "sharia-erp landing renders with its full course count and states it covers the
basics" — the same terminal-state scenario `prd.md` already declares, reached here as `sharia-erp`
completes its 30-course growth (mirrors plan 06's progressive-rebind idiom, the second of plan 07's
two pre-existing terminal-state `prd.md` scenarios)

```gherkin
Scenario: sharia-erp landing renders with its full course count and states it covers the basics
  Given the reader navigates to "/en/learn/paths/skills/sharia-erp"
  When the landing page loads
  Then the landing renders 30 courses in courseOrder order
  And the landing displays the Dangerous 1 through Dangerous 4 boundaries
  And the landing states explicitly that the path covers all the basics without requiring
    "conventional-erp" first
```

- [ ] [AI] **RED** — extend the reusable boundary helper in
      `apps/ayokoding-www-fe-e2e/src/steps/skills-erp-paths.steps.ts` to assert the Dangerous 4
      boundary and the terminal "ENDS HERE" statement on `<SHARLANDING>` **only** (never
      `<CONVLANDING>`, already terminal from §3.5) — command: `nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: the new assertion **fails** (only Dangerous 1-3 were asserted before this phase).
- [ ] [AI] **GREEN** — implement the step bindings against the grown `<SHARLANDING>` content (from
      §4.4) — command:
      `nx run ayokoding-www:specs:behavior:coverage && nx run ayokoding-www-fe-e2e:test:e2e` —
      acceptance: both exit 0.
- [ ] [AI] **REFACTOR** — consolidate the four boundary assertions (Dangerous 1-4) into a single
      table-driven helper — command: `nx run ayokoding-www-fe-e2e:test:e2e` — acceptance: exits 0,
      scenario count unchanged; this is the final growth of `skills-erp-paths.steps.ts` — Phase 5 only
      re-runs coverage, it never extends the file further.

### Phase 4 Gate

- [ ] [AI] All Phase 3 Gate checks re-run and still green; `<CONVMAN>` unchanged at 27.
- [ ] [AI] `grep -cE '^  - ' "${SHARMAN}"` prints `30`.
- [ ] [AI] **Integration**: draft PR opened, 3-cycle PR-Review complete, CI green, `[AI]` merge,
      `ayokoding-www` deployed, post-deploy curl check confirms `<SHARLANDING>` shows "ENDS HERE".

> **Pause Safety**: both paths are terminal (27/27 and 30/30). The full corpus is live. Safe to stop.
> To resume: `grep -cE '^  - ' ${SHARMAN}` reads `30` and
> `curl -sf https://ayokoding.com/en/learn/paths/skills/sharia-erp | grep -qi "covers all the basics"`.

## Phase 5: Cross-Path Integrity and Spec Coverage Verification

- [ ] [AI] Run `checkManifestIntegrity` and `checkPrerequisiteConsistency` against **both** final
      manifests together — acceptance: zero violations reported by each.
- [ ] [AI] **A11 — one body, two references.** Verify no shared course id has a second copy anywhere
      under `<COURSES>`, which is the only way a body could diverge between the two manifests. Search
      the whole tree by id rather than a name glob over the top level:

  ```bash
  for id in "${ERP_ALL[@]}"; do
    n=$(find "${COURSES}" -type d -name "$id" | grep -c .)
    [ "$n" -eq 1 ] || echo "EXPECTED-1-GOT-$n: $id"
  done
  ```

  Acceptance: **empty output**. Guard first — `[ "${#ERP_ALL[@]}" -eq 30 ] && echo GUARD-OK` must
  print `GUARD-OK`.

  Three notes on why this replaces the previous clause, which could not fail:
  - `find … -maxdepth 1 … | sort | uniq -d` was **vacuous by construction** — `find` lists each
    directory exactly once, so `uniq -d` had nothing to emit no matter what the tree contained.
  - Its name globs (`erp-*`, `*-to-*-systems`, `*-erp*`) also missed 6 of the 30 ids outright,
    including `production-planning-and-mrp`, `demand-and-supply-planning`,
    `inventory-and-warehouse-management`, `human-capital-management-and-hire-to-retire`,
    `islamic-contract-based-transaction-flows` and `zakat-and-sharia-compliance-modules`.
  - `git log --follow` on a single hardcoded id was not a corpus-wide check and is dropped.

  **Control probe**: `mkdir -p "${COURSES}sharia-erp/erp-foundations-and-history"` in a scratch
  checkout and re-run — it must print `EXPECTED-1-GOT-2`. Remove it afterwards.

- [ ] [AI] `nx run ayokoding-www:specs:behavior:coverage` reports 100% for `skills-erp-paths.feature`.
- [ ] [AI] `nx run ayokoding-www:test:unit` **and** `nx run ayokoding-www-fe-e2e:test:e2e` both green
      for the full corpus — acceptance: both exit 0. The e2e target must be the `-fe-e2e` project's;
      `ayokoding-www:test:e2e` is a no-op echo stub and would pass unconditionally.

### Phase 5 Gate

- [ ] [AI] All checks above pass. **Integration**: draft PR (if any residual changes), 3-cycle
      PR-Review, CI green, `[AI]` merge.

> **Pause Safety**: the full corpus is integrity-verified. Safe to stop. To resume: re-run
> `nx run ayokoding-www:specs:behavior:coverage`.

## Phase 6: Section and App Verification

Grep-checkable licensing and trademark acceptance clauses (A8) — each clause fails when violated,
never passes vacuously.

- [ ] [AI] **No vendor name in any course id, path id, or product name**:
      `grep -riE 'sap|oracle|netsuite|erpnext|odoo' <(printf '%s\n' "${ERP_ALL[@]}" skills/conventional-erp skills/sharia-erp)` —
      acceptance: **empty output** (a non-empty match is a trademark-rule violation and fails this
      clause).
- [ ] [AI] **No verbatim standards-text reproduction**: for each of the `[Verified]` AAOIFI FAS
      numbers named in
      [plan 06's verification log §Verified facts carried in](../ayokoding-learning-path-06-skills-accounting/verification-log.md#verified-facts-carried-in-do-not-re-litigate-do-re-confirm-at-authoring)
      (FAS 3, 4, 7, 9, 10, 28, 32, 33, 34 — the same list this plan's own
      [tech-docs.md §Load-bearing for courses 28–30](./tech-docs.md#load-bearing-for-courses-2830--there-is-no-single-sharia-accounting-standard)
      already cites that log for the adjacent PSAK/OI-1 claim), confirm no course body contains a
      100+-character verbatim span matching AAOIFI's own published standard text — this requires a
      `web-researcher`-assisted diff against the official AAOIFI standard for any course quoting a
      FAS number; **acceptance**: for every quoted FAS number, the confirming dispatch reports "no
      verbatim match found", or the offending span is rewritten before this clause is marked
      complete.
- [ ] [AI] **No screenshot of proprietary software.** Sweep the course bundles this plan actually
      authored, by id, rather than by a path glob over a tree that may not exist yet:
      `for id in "${ERP_ALL[@]}"; do find "${COURSES}${id}" \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.gif' -o -iname '*.webp' \); done | grep -c .`
      — acceptance: returns **0**.
      Note three things this clause deliberately does **not** do, each of which silently broke the
      previous version: it does not pipe paths into a second `find`; it does not redirect stderr to
      `/dev/null` (a missing directory must surface as an error, not as a passing empty result); and
      it parenthesises the `-o` alternation so the implicit `-print` applies to every branch rather
      than only the last.
      **This clause is only meaningful once the bundles exist** — run it after the Phase 5 authoring
      steps, never before, or it measures an empty tree. Guard:
      `[ "$(for id in "${ERP_ALL[@]}"; do test -d "${COURSES}${id}" && echo x; done | grep -c .)" -eq 30 ] && echo GUARD-OK || echo GUARD-FAIL`
      must print `GUARD-OK` first.
      Expected steady state is zero matches (this corpus ships no binary image assets, per its
      no-net-new-screen exemption); any match fails the clause and must be investigated.
- [ ] [AI] **No chart of accounts lifted from a reference implementation**: manual review confirms
      every worked example's dataset in every By-Example course under `ERP_ALL` uses an
      originally-authored account/item/customer/vendor naming scheme, cross-checked against no known
      reference implementation's public sample-data set names (Odoo demo data, ERPNext demo data) —
      `apps-ayokoding-www-facts-checker` performs this check per course; **acceptance**: checker
      reports zero matches for every course.
- [ ] [AI] **Every syllabus's Scope note ends with the inherited licence tag**:
      `for id in "${ERP_ALL[@]}"; do grep -qF 'License-aware (DD-15)' "${SYL}${id}.md" || echo "MISSING TAG: $id"; done | grep -q . && echo FAIL || echo PASS` —
      acceptance: prints `PASS`.

### Licensing reading audit — course bodies **and** syllabus artifacts (A8 + A12)

> `A8` binds both layers. The clauses above that carry real substance — verbatim standards text,
> chart-of-accounts provenance — read **course bodies only**, and the syllabus layer gets nothing
> beyond a tag-presence check. That is a gap: the syllabi are where standards bodies and reference
> implementations are actually cited, so they carry at least as much exposure as the bodies do.
> This clause closes it, mirroring plan 06's own combined audit.

- [ ] [AI] Read **both** layers against the eleven safe-authoring rules in
      [tech-docs §Licensing and IP Compliance](./tech-docs.md#licensing-and-ip-compliance-a8): every
      file in `"${SYL}"` (30 syllabi) **and** every `_index.md` under `"${COURSES}"` for `ERP_ALL`
      (30 course bodies) — 60 files total. Confirm none reproduces a standard's clause text or
      numbering layout, mirrors a commercial curriculum's module sequence (ASCM/APICS CPIM and CSCP
      outlines are copyrighted products — naming one as corroboration is nominative use and fine,
      transcribing or re-ordering to match it is not, per `A12`), pastes copyleft code, lifts a
      reference implementation's demo dataset, or uses a vendor name in a title.
      Cardinality guard first:
      `[ "$(find "${SYL}" -maxdepth 1 -name '*.md' ! -name 'README.md' | wc -l)" -eq 30 ] && echo GUARD-OK || echo GUARD-FAIL`
      must print `GUARD-OK` — acceptance: `GUARD-OK`, then zero violations found across all 60 files;
      any finding is fixed before this gate closes. The count excludes `syllabus/courses/README.md`
      (required by the Learning-Bearing Syllabus Completeness convention) — a naive
      `ls "${SYL}"*.md | wc -l` would match the README too and return 31.

### Phase 6 Gate

- [ ] [AI] All five clauses above pass (not vacuously — each has a real failure mode that was
      checked, not merely a command that could never fail).
- [ ] [AI] **Integration**: draft PR opened, 3-cycle PR-Review complete, CI green, `[AI]` merge,
      `ayokoding-www` deployed.

> **Pause Safety**: licensing/trademark posture is verified across the full corpus. Safe to stop. To
> resume: re-run the five clauses above.

## Phase 7: Manual UI Retest (Rule 15)

Per [tech-docs.md §R9 gate posture](./tech-docs.md#r9-gate-posture-declared-explicitly), this plan is
UI-gate-exempt; the three-tester retest is the mandatory non-vacuous substitute.

- [ ] [AI] Dispatch `web-exploratory-tester` (spec-aware) against both live landings
      (`/en/learn/paths/skills/conventional-erp`, `/en/learn/paths/skills/sharia-erp`) in `delivery`
      mode — verify zero CRITICAL/HIGH findings.
- [ ] [AI] Dispatch `web-usability-tester` (spec-blind) against both landings — verify zero
      CRITICAL/HIGH findings.
- [ ] [AI] Dispatch `web-design-tester` (design-aware) against both landings — verify zero
      CRITICAL/HIGH findings, and specifically confirm the Dangerous-N ramp table renders
      legibly and the color-blind-friendly palette (inherited from plan 03's design system) is
      preserved.
- [ ] [AI] **Capture the retest evidence — three "zero findings" reports with no artefact are
      unauditable**, and this is the mandatory substitute for a UI gate, so its evidence carries more
      weight here than it would on a UI-gated plan. Each tester runs in `delivery` mode and writes its
      report into this plan; additionally save to `${PLANDIR}evidence/`:
  - each tester's report path recorded as `phase7__<tester>__report.md` (or a link to it if the
    tester wrote elsewhere);
  - `browser_take_screenshot` of both landings at mobile 375px, tablet 768px and desktop 1440px,
    using `browser_resize` between each, named `phase7__<path-id>__<width>.png`.
    Acceptance: `ls "${PLANDIR}evidence/" | grep -c '^phase7__'` returns **at least 9** (6
    screenshots + 3 tester reports), **and** each tester's recorded verdict is zero CRITICAL and
    zero HIGH. Do not suppress stderr — a missing evidence directory must surface as an error
    rather than as a passing empty result.

### Phase 7 Gate

- [ ] [AI] All three testers report zero CRITICAL/HIGH findings, or every finding is fixed and
      re-verified.
- [ ] [AI] Evidence captured under `${PLANDIR}evidence/` per the capture step above.
- [ ] [AI] **Integration**: draft PR opened, 3-cycle PR-Review complete, CI green, `[AI]` merge,
      `ayokoding-www` deployed.

> **Pause Safety**: both landings are manually retested and clean. Safe to stop. To resume: re-dispatch
> the three testers.

## Phase 8: Full-Corpus Integration Verification

- [ ] [AI] `nx run ayokoding-www:build` succeeds with both manifests and all 30 course bundles
      present.
- [ ] [AI] `nx affected -t build,test:quick,lint --base=main` is green for `ayokoding-www`.
- [ ] [AI] End-to-end path-walk: navigate `/en/learn/paths/skills/conventional-erp`, step through
      prev/next across all 27 courses via Playwright MCP, verify no broken link and no console error;
      repeat for `/en/learn/paths/skills/sharia-erp` across all 30.
- [ ] [AI] **Capture evidence for the walk — a walk with no artefact is unauditable.** Write to
      `${PLANDIR}evidence/`:
  - `browser_take_screenshot` of each path landing at three breakpoints (mobile 375px, tablet 768px,
    desktop 1440px), using `browser_resize` between each, named
    `phase8__<path-id>__<width>__landing.png`.
  - `browser_take_screenshot` of the first and last course page of each walk, named
    `phase8__<path-id>__<position>__<course-id>.png` — for `sharia-erp` the last is
    `zakat-and-sharia-compliance-modules` (course 30), for `conventional-erp` it is
    `erp-analytics-and-reporting` (course 27).
  - `browser_console_messages` output for each walk saved as
    `phase8__<path-id>__console.txt`.
    Acceptance: `ls "${PLANDIR}evidence/" | grep -c '^phase8__'` returns **at least 11** (6
    landing screenshots + 4 course screenshots + 2 console logs is 12; the floor allows one
    combined console capture), **and** every `phase8__*__console.txt` contains zero lines matching
    `-iE 'error|warning'`:
    `grep -ilE 'error|warning' "${PLANDIR}evidence/"phase8__*__console.txt | grep -c .` returns
    **0**. Do not redirect stderr here — a missing evidence directory must surface as an error
    rather than as a passing empty result.

### Phase 8 Gate

- [ ] [AI] Build succeeds; affected checks green; both path-walks complete with zero errors.
      **Integration**: final draft PR opened with all preconditions confirmed — but **not merged
      here**. The PR stays open through Phases 9 and 10 so Knowledge Capture and the archival move are
      committed to this same branch and land inside this PR, as the merge protocol requires. The
      `[AI]` merge and the `ayokoding-www` deploy are the terminal steps of Phase 10.

> **Pause Safety**: the full corpus builds and both paths are walkable end to end. Safe to stop. To
> resume: re-run the Playwright path-walk.

## Phase 9: Knowledge Capture

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)._

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only if a durable surface would
      catch this automatically next time; discard the rest with a one-line reason.
- [ ] [AI] Apply the secret/sensitivity gate — sanitize or discard any entry naming a real credential
      or private hostname.
- [ ] [AI] Apply the repo-relevance gate — infra-private content (none expected in this plan) stays
      out of `ose-public`.
- [ ] [AI] Route each surviving learning to exactly one durable home per the open-ended routing
      matrix; a code-homed learning is filed as a separate `plans/backlog/<slug>/` plan, never landed
      inline.
- [ ] [AI] If no generalizable learning surfaced, record `No generalizable learnings — <reason>` in
      `learnings.md`.

### Phase 9 Gate

- [ ] [AI] Every `learnings.md` entry is terminal (routed, filed as backlog, discarded with reason),
      or the explicit "none" escape is recorded.
- [ ] [AI] No code-homed learning landed inline in this plan's own commits/PR.
- [ ] [AI] **Integration**: the triaged `learnings.md` is committed to the still-open PR branch from
      Phase 8 (no separate PR), CI green.

> **Pause Safety**: `learnings.md` is fully triaged. Safe to stop. To resume: re-read `learnings.md`
> and confirm every entry is terminal.

## Phase 10: Plan Archival

- [ ] [AI] `git mv plans/backlog/ayokoding-learning-path-07-skills-erp plans/done/$(date +%Y-%m-%d)__ayokoding-learning-path-07-skills-erp`.
- [ ] [AI] Update `plans/backlog/README.md` to remove this plan's backlog entry and reflect its
      completed status.
- [ ] [AI] Commit the archival move **to the still-open PR branch from Phase 8** — no dedicated
      follow-up archival PR. Phase 8 deliberately left the PR unmerged precisely so this commit lands
      inside it; the merge protocol requires archival committed in the PR **before** the merge, and a
      PR that has already merged cannot receive it. Use a Conventional Commits message, e.g.
      `git commit -m "chore(plans): archive ayokoding-learning-path-07-skills-erp"`.
- [ ] [AI] **Push it** — `git push origin HEAD` — acceptance: exits 0 and
      `git status -sb | grep -c 'ahead'` returns **0**. Committing without pushing would leave the
      archival move out of the PR while every later check still appeared to pass.
- [ ] [AI] **Monitor CI on the new head** — poll every 2 minutes, one
      `gh run view --json status,conclusion` per wakeup; never tight-loop, never `gh run watch`; on a
      403 rate-limit wait ~35 minutes. Acceptance: `status` is `completed` **and** `conclusion` is
      `success` **for the run whose head SHA equals `git rev-parse HEAD`** — confirm the SHA matches
      rather than reading whichever run is newest, or a stale green run from before the archival
      commit will be mistaken for a pass.
- [ ] [AI] Re-confirm all five PR Merge Protocol preconditions on the new head, perform the `[AI]`
      merge, then deploy `ayokoding-www` to `prod-ayokoding-www`. These are the terminal steps.

### Phase 10 Gate

- [ ] [AI] The plan folder exists under `plans/done/` with the date prefix; no reference to it remains
      under `plans/backlog/`.
- [ ] [AI] The archival commit landed **inside** the merged PR rather than in a follow-up:
      `gh pr list --head "$(git rev-parse --abbrev-ref HEAD)" --state merged --json number,mergeCommit`
      returns this plan's PR. Use `gh pr list --head`, not `git merge-base --is-ancestor`: this repo
      squash-merges, so ancestry checks false-negative on every merged PR.
- [ ] [AI] **Integration**: PR merged, `ayokoding-www` deployed to `prod-ayokoding-www`.

> **Pause Safety**: the plan is archived. Terminal state — no further resume needed.

## File impact and rollback

See [tech-docs.md §File impact](./tech-docs.md#file-impact) and
[§Rollback](./tech-docs.md#rollback) — this delivery checklist implements exactly that file set,
phase by phase, with no step outside it.
