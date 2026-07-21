# Delivery Checklist — Skills Path: Accounting

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
> Git-mechanical steps (worktree create/remove, branch, commit, push, merge) are `[AI]`.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (safe-to-stop state + resume command). Each gate covers the phase's
> **content/data correctness** and its **integration** (draft PR opened, 3-cycle PR-Review, CI green,
> `[AI]` merge, `ayokoding-www` deployed). A phase is not complete until every gate check is green.

Four standing constraints govern every step below.

> **Ownership**: this plan owns exactly **one** manifest file (`<MANIFEST>`), **one** path landing
> bundle (`<LANDING>`), **twenty** course bundles, and **twenty** syllabus specs inside this plan
> folder. It creates **no `_index.md` under `<PATHS>`** other than its own landing (A3 — plan 01 owns
> every structural index), authors **no ERP content** (plan 07's), and edits **no existing library
> course**.
>
> **Verification hygiene**: no `[Unverified]` research claim is ever restated as fact. Every external
> claim carries a confidence marker or a primary-source citation. See
> [tech-docs §Open verification items](./tech-docs.md#open-verification-items-oi-1-through-oi-4).
>
> **Mixed TDD posture (DD-612)**: manifest publication and growth are RED → GREEN → REFACTOR cycles.
> Course bodies and landing prose are **maker-checker-fixer**, with no RED/GREEN/REFACTOR labels —
> there is no failing assertion to write first for prose.
>
> **Falsifiability**: every acceptance clause states its before value and its after value. A clause
> that would return the same thing whether or not the work was done is not a clause.

## Worktree

Worktree path: `worktrees/ayokoding-learning-path-06-skills-accounting/`

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree ayokoding-learning-path-06-skills-accounting
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the latest
`origin/main` when missing, syncs with `origin/main` before implementing, and prompts before deleting
the worktree after the plan is archived and pushed.

Every phase branches from the **latest `origin/main`** inside this one shared worktree
(`git fetch origin && git checkout main && git pull && git checkout -b ayokoding-learning-path-06-skills-accounting/<phase-slug>`),
authors its work there, commits, pushes that branch, and opens **its own draft PR**.

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans.md#worktree-specification).

## Delivery Mode: worktree-to-pr

Each phase — and each course sub-phase inside an authoring phase — works in the shared worktree on
its **own branch**, opens a **draft PR** against `main`, runs the **PR-Review Maker→Fixer Cycle**
(`pr-review-maker` / `pr-review-fixer`, 3 sequential CI-gated cycles), flips the PR to ready, and
`[AI]` **merges it once all quality gates are green** — then `[AI]` **deploys `ayokoding-www` to
`prod-ayokoding-www`**. This plan declares **no `[HUMAN]` merge gate**; it inherits the repo-default
`[AI]` merge from the
[PR Merge Protocol](../../../repo-governance/development/workflow/pr-merge-protocol.md), whose five
hardened preconditions are unchanged. See
[Plans Organization Convention §Delivery Mode](../../../repo-governance/conventions/structure/plans.md#delivery-mode)
and the [PR Review Quality Gate workflow](../../../repo-governance/workflows/pr/pr-review-quality-gate.md).

**Per-Phase Integration Protocol** (each phase's gate lists these as must-pass):

1. [AI] Sync the shared worktree to latest `origin/main` and branch:
   `git fetch origin && git checkout main && git pull && git checkout -b ayokoding-learning-path-06-skills-accounting/<phase-slug>`.
2. [AI] Stage only this phase's paths (`git add <explicit paths>` — never `git add -A`), commit
   thematically (Conventional Commits, imperative, no period), push the branch, open a **draft PR**
   against `main` (`gh pr create --draft --base main ...`) — CI runs on the PR.
3. [AI] Run the **PR-Review Maker→Fixer Cycle** (3 sequential CI-gated cycles), resolve every
   finding, then `gh pr ready`.
4. [AI] **Merge** once all quality gates are green (typecheck, lint, `test:quick`, `test:unit`,
   `test:e2e` where affected, `specs:behavior:coverage`, CI, the 3-cycle review).
5. [AI] Dispatch `apps-ayokoding-www-deployer` to deploy `ayokoding-www` to `prod-ayokoding-www` — a
   no-op redeploy for plan-side-only phases.

## Depends-on and start preconditions

| Direction   | Plan (full folder name)                                  | Strength                                           |
| ----------- | -------------------------------------------------------- | -------------------------------------------------- |
| `blockedBy` | `ayokoding-learning-path-01-url-restructure`             | **hard**                                           |
| `blockedBy` | `ayokoding-learning-path-02-schema-and-prerequisite-dag` | **hard**                                           |
| `blockedBy` | `ayokoding-learning-path-03-navigation-ui`               | **hard**                                           |
| `blocks`    | `ayokoding-learning-path-07-skills-erp`                  | soft overall, **hard from ERP #7**                 |
| _(no edge)_ | `ayokoding-learning-path-04-course-authoring`            | verified — both linked prerequisites are plan 01's |
| _(no edge)_ | `ayokoding-learning-path-05-manifests`                   | disjoint manifest subtrees                         |

All start preconditions are verified in Phase 0 before any authoring begins.

## Parallelization Model

**Cap**: honour the in-force subagent / PR-review concurrency cap (parallel-by-default, background
subagents capped per the orchestration convention). The main thread self-promotes nothing.

- **Phases are strictly serial.** Each later phase's gate re-verifies the manifest published so far.
- **Inside an authoring phase, course sub-phases pipeline concurrently** up to the cap. Every course
  writes only its own subtree under `<COURSES>`, so bodies are content-independent (DD-613).
- **The manifest mutation is the only serial sync point per phase**, and it happens once, at the end.

**DAG width inside this plan** is the number of courses in the current stage, capped by the in-force
concurrency limit: 3 in Phase 2, 13 in Phase 3, 4 in Phase 5, and 1 everywhere else.

## Path constants

- `<COURSES>` = `apps/ayokoding-www/content/en/learn/courses/`
- `<PATHS>` = `apps/ayokoding-www/content/en/learn/paths/`
- `<LANDING>` = `<PATHS>skills/accounting/`
- `<FEAT>` = `apps/ayokoding-www/src/features/course-paths/`
- `<MANIFESTS>` = `<FEAT>manifests/`
- `<MANIFEST>` = `<MANIFESTS>skills/accounting.yaml`
- `<MTEST>` = `<MANIFESTS>skills/accounting-manifest.unit.test.ts` _(new file; matches the vitest
  `unit` project's `**/*.unit.{test,spec}.{ts,tsx}` include)_
- `<SPEC>` = `plans/backlog/ayokoding-learning-path-06-skills-accounting/syllabus/courses/`
- `<SPECPATHS>` = `plans/backlog/ayokoding-learning-path-06-skills-accounting/syllabus/paths/`
- `<MIRROR>` = `<SPECPATHS>manifest-skills-accounting.md` — filename fixed by plan 02's ruling; a bare
  `manifest-accounting.md` is **not** acceptable
- `<SPECS>` = `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/course-paths/`
- `<VLOG>` = `plans/backlog/ayokoding-learning-path-06-skills-accounting/verification-log.md`
- Path ID: **`skills/accounting`** — the full slash string including the category segment; no separate
  `category` field, no bare `accounting`. Arc: `immediately-effective` — a separate **required**
  manifest field, recorded as data, omitted from the URL.

> **No clause below keys on `pathId` segment count.** `pathId` is variable-depth by design (careers =
> 3 segments, skills = 2) and validation is first-segment literal plus resolvability, never arity.
> Every pattern here matches the **full id**. A sibling plan shipped a clause using a two-group path
> regex (`/en/learn/paths/[a-z-]+/[a-z0-9-]+`) that silently stopped at the first `/` inside a
> 3-segment careers URL and undercounted by one under `sort -u` — that shape appears nowhere in this
> file. An unresolvable or malformed id is a hard `safeParse` rejection: no coercion, no alias, no
> normalization, no nearest-match fallback. See
> [tech-docs §`pathId` conformance rules](./tech-docs.md#pathid-conformance-rules-plan-02s-ruling--binding-not-re-derived-here).

## Course ID lists (define once, reuse in every clause)

Define these in the shell before running any looping acceptance clause below. They are the exact IDs
from [tech-docs §The twenty-course catalog](./tech-docs.md#the-twenty-course-catalog); no clause
re-types them.

> **HARD — arrays, never space-separated strings.** This repo's shell is **zsh**
> [Repo-grounded — `$ZSH_VERSION` is `5.9`; `$BASH_VERSION` is unset], and **zsh does not word-split
> an unquoted parameter**. `X="a b c"; for i in $X` iterates **once** with `i="a b c"`, so every
> derived count silently reads **1** instead of 20 — while still exiting 0 and still looking green.
> That is the worst failure mode available: a check that passes while measuring nothing. Store every
> id list as a shell **array** and iterate as `"${NAME[@]}"`. The self-check in
> [Phase 0](#phase-0-environment-setup-and-baseline) asserts the list lengths and is what makes every
> other count in this file trustworthy — do not skip it.

```bash
ACCT_S1=(accounting-foundations chart-of-accounts-and-data-modeling financial-statements-and-close-cycle)
ACCT_S2=(accrual-accounting-and-revenue-recognition accounts-payable-and-procure-to-pay accounts-receivable-and-order-to-cash managerial-and-cost-accounting fixed-assets-and-depreciation inventory-and-cogs-accounting lease-and-intangible-asset-accounting consolidation-and-multi-entity-accounting financial-reporting-standards-ifrs-vs-gaap audit-controls-and-compliance payroll-and-tax-accounting-essentials treasury-and-cash-management financial-reporting-and-xbrl)
ACCT_S3=(sharia-accounting-and-aaoifi-standards islamic-contract-modeling-for-systems capstone-build-a-general-ledger-system capstone-sharia-compliant-ledger)
ACCT_ALL=("${ACCT_S1[@]}" "${ACCT_S2[@]}" "${ACCT_S3[@]}")
ACCT_SILENT=("${ACCT_S2[@]}" "${ACCT_S3[@]}")
```

Alternation forms, **derived from the arrays** so they cannot drift, for manifest-content greps
(`grep -oE` prints each match; `sort -u | wc -l` gives the distinct count):

```bash
ACCT_S2_ALT=$(printf '%s|' "${ACCT_S2[@]}" | sed 's/|$//')
ACCT_S3_ALT=$(printf '%s|' "${ACCT_S3[@]}" | sed 's/|$//')
```

> **Why loops and derived alternations rather than `grep -c` or `grep -L`**: `grep` in this repo is
> **ugrep**. `grep -c` counts **lines**, not matches, and `grep -L` means files-**without**-match and
> exits 0 — neither is safe in an acceptance clause. `--glob` is unsupported; `--exclude-dir` is the
> supported form. No clause below uses `find -newermt` either, which is GNU syntax and fails on this
> BSD `find`. No course ID is a substring of another, which is what makes the alternation counts
> sound.

---

## Phase 0: Environment Setup and Baseline

> _Executor: `repo-setup-manager`_
>
> This phase verifies the **three hard start preconditions** and the two facts that keep this plan
> off plan 04's critical path, then records a baseline that makes every later clause falsifiable.

- [ ] [AI] Enter/provision the worktree and install dependencies in the root worktree: `npm install`
      — acceptance: exits 0, `node_modules/` synchronized.
- [ ] [AI] Converge the toolchain in the root worktree: `npm run doctor -- --fix`
      — acceptance: exits 0 with no unresolved drift.
- [ ] [AI] **Start precondition 1** — the URL-restructure plan is merged:
      `gh pr list --search "ayokoding-learning-path-01-url-restructure" --state merged --json number --jq 'length'`
      — acceptance: returns a value ≥ 1. Falsifiable both ways: returns `0` while that plan is open.
- [ ] [AI] **Start precondition 2** — the schema plan is merged and the manifest directory exists:
      `gh pr list --search "ayokoding-learning-path-02-schema-and-prerequisite-dag" --state merged --json number --jq 'length'`
      and `test -d <MANIFESTS>` — acceptance: the first returns ≥ 1 and the second exits 0. `test -d`
      returns non-zero on the current tree, where `<FEAT>` does not exist at all.
- [ ] [AI] **Start precondition 3** — the navigation plan is merged and the renderer exists:
      `gh pr list --search "ayokoding-learning-path-03-navigation-ui" --state merged --json number --jq 'length'`
      and `test -f <FEAT>shell/manifest-repository.ts` — acceptance: the first returns ≥ 1 and the
      second exits 0; the second returns non-zero before that plan lands.
- [ ] [AI] **DD-605 verification — the two linked prerequisites already resolve**, proving this plan
      is not blocked by `ayokoding-learning-path-04-course-authoring`:
      `test -d <COURSES>sql-essentials && test -d <COURSES>backend-essentials`
      — acceptance: exits 0. Falsifiable both ways: it exits non-zero before plan 01's re-home, and
      it would exit non-zero if either slug were renamed — in which case this plan's dependency
      analysis is wrong and must be re-done before proceeding, not worked around.
- [ ] [AI] **Skills bucket exists and is plan 01's** — `test -f <PATHS>skills/_index.md`
      — acceptance: exits 0. **Do not create this file if it is missing** (A3): record the gap and
      stop, because a missing structural index means plan 01 did not ship its A3 scope.
- [ ] [AI] **Course-ID array self-check (run this BEFORE any other looping clause in this file).**
      Define the five arrays from
      [§Course ID lists](#course-id-lists-define-once-reuse-in-every-clause) exactly as written, then
      assert their lengths:
      `printf '%s\n' "${ACCT_S1[@]}" | wc -l` returns **3**,
      `printf '%s\n' "${ACCT_S2[@]}" | wc -l` returns **13**,
      `printf '%s\n' "${ACCT_S3[@]}" | wc -l` returns **4**,
      `printf '%s\n' "${ACCT_ALL[@]}" | wc -l` returns **20**, and
      `printf '%s\n' "${ACCT_SILENT[@]}" | wc -l` returns **17**
      — acceptance: all five hold. **If any returns 1, the lists were pasted as space-separated
      strings instead of arrays and EVERY downstream count in this file is invalid** — this shell is
      zsh, which does not word-split an unquoted parameter, so a string-backed loop iterates once and
      still exits 0. Stop and re-define the arrays before proceeding. Also confirm the derived
      alternations are non-degenerate: `printf '%s\n' "$ACCT_S2_ALT" | tr '|' '\n' | wc -l` returns
      **13** and `printf '%s\n' "$ACCT_S3_ALT" | tr '|' '\n' | wc -l` returns **4**.
- [ ] [AI] **Baseline: none of the twenty courses exists yet** —
      `for c in "${ACCT_ALL[@]}"; do test -d "<COURSES>$c" && echo "PRESENT $c"; done | wc -l`
      — acceptance: returns **0**. Falsifiable both ways: after Phase 5 the mirrored miss-count
      clause returns 0 while this one returns 20. _(This clause is only meaningful once the array
      self-check above has passed.)_
- [ ] [AI] **Baseline: no accounting manifest exists** — `test -f <MANIFEST>`
      — acceptance: exits **non-zero**; exits 0 after Phase 2.
- [ ] [AI] Establish tool baselines: `npx nx run ayokoding-www:build`,
      `npx nx run ayokoding-www:test:unit`, and `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: all exit 0; record pass counts in `evidence/phase-0-snapshot.txt`.
- [ ] [AI] **Route OI-4** — record the plan-02 wording seam (its doc-level prerequisite-omission rule
      versus this plan's link-don't-walk manifest) in `<VLOG>` by changing the `OI-4:` line from
      `OPEN` to `ROUTED`, with a one-line note naming plan 02's `tech-docs.md §Manifest integrity
invariants` as the sentence needing a cross-domain carve-out. **Do not edit plan 02's folder.**
      — acceptance: `grep -oE '^OI-4: ROUTED' <VLOG> | wc -l` returns **1** (returns **0** before this
      step).
- [ ] [AI] Resolve every preexisting failure before proceeding — acceptance: zero unresolved failures
      remain; each fix committed separately with its own conventional-commit message.
- [ ] [AI] Confirm the `learnings.md` scaffold exists in the plan folder — acceptance: file present
      with its H1.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [ ] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift.
- [ ] [AI] All three start preconditions hold — plans 01, 02 and 03 merged; `<MANIFESTS>` present;
      `manifest-repository.ts` present.
- [ ] [AI] `test -d <COURSES>sql-essentials && test -d <COURSES>backend-essentials` exits 0, and
      `test -f <PATHS>skills/_index.md` exits 0.
- [ ] [AI] The twenty-course PRESENT count is **0** and `test -f <MANIFEST>` exits non-zero — the
      baseline is genuinely empty.
- [ ] [AI] `ayokoding-www:build` + `:test:unit` + `ayokoding-www-fe-e2e:test:e2e` baselines recorded
      green in `evidence/phase-0-snapshot.txt`; zero preexisting failures unresolved.
- [ ] [AI] `grep -oE '^OI-4: ROUTED' <VLOG> | wc -l` returns **1**.
- [ ] [AI] Draft PR opened; CI triggered; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged;
      `ayokoding-www` deployed (no-op redeploy).

> **Pause Safety**: only the toolchain and the upstream preconditions were verified and the empty
> baseline snapshotted — no spec, body, landing, or manifest exists. Safe to stop indefinitely.
> To resume: re-run the three precondition checks and the two baseline clauses.

---

## Phase 1: The twenty syllabus specs

> _Suggested executor: `web-researcher` (per-course accuracy pre-verify) + `apps-ayokoding-www-general-maker`
> (spec prose)._
>
> The **contract layer**. Every downstream authoring step transcribes from these specs rather than
> re-deciding. Specs live in **this plan's own folder** (DD-601) — plan 02's `syllabus/` corpus is
> frozen under a binding custody rule and is never written to here.
>
> Verification markers from the seeding research are carried **verbatim** into the specs for #17,
> #18 and #20. Nothing is promoted to fact in this phase; that is Phase 4's job.

- [ ] [AI] Create the spec folder and its index: `<SPEC>../README.md` _(new file)_ listing all 20
      course IDs, their formats, their stage, and their prerequisite edges, transcribed from
      [tech-docs §The twenty-course catalog](./tech-docs.md#the-twenty-course-catalog)
      — acceptance: `test -f <SPEC>../README.md` exits 0, and
      `for c in "${ACCT_ALL[@]}"; do grep -F -q "$c" <SPEC>../README.md || echo "MISSING $c"; done | wc -l`
      returns **0** (returns **20** before this step).
  - _Suggested executor: `apps-ayokoding-www-general-maker`_
- [ ] [AI] Author one `<SPEC><course-id>.md` per course, for all 20, each carrying the seven required
      sections from
      [tech-docs §Syllabus spec layer](./tech-docs.md#syllabus-layer--custody-and-shape): top
      matter, scope note, why-this-exists, prerequisites (verbatim, including any `(SWE)` edge),
      scope boundary against its confusable sibling, silent-failure modes (**courses #4–#20 only**),
      and verification markers
      — acceptance: `for c in "${ACCT_ALL[@]}"; do test -f "<SPEC>$c.md" || echo "MISSING $c"; done | wc -l`
      returns **0** (returns **20** before this step).
- [ ] [AI] Author the path mirror `<MIRROR>` _(new file)_ — the human-readable twenty-course ordering
      this plan later transcribes into `<MANIFEST>`'s `courseOrder`, declaring
      `pathId: skills/accounting` and `arc: immediately-effective`. **The filename is fixed by plan
      02's ruling** (`manifest-skills-accounting.md`, with the `skills-` category marker); a bare
      `manifest-accounting.md` is not acceptable
      — acceptance: `test -f <MIRROR>` exits 0 **and**
      `find <SPECPATHS> -name 'manifest-*.md' | grep -vF 'manifest-skills-accounting.md' | wc -l`
      returns **0** (returns **1** if a bare or otherwise-named mirror is created alongside it), AND
      `grep -F -q 'skills/accounting' <MIRROR>` exits 0, AND `grep -F -q 'immediately-effective' <MIRROR>`
      exits 0. All four exit non-zero / return non-zero before this step, since `<SPECPATHS>` does not
      exist.
  - _Suggested executor: `apps-ayokoding-www-general-maker`_
- [ ] [AI] **Canonical prefixed path-id check** — every path id this plan writes uses the full
      `skills/accounting` form, never a bare `accounting`. Plan 02's 121 existing course specs still
      carry stale un-prefixed ids in their "In which paths" sections; they are custody-protected and
      **must not be edited** — this check exists so this plan adds nothing to that debt
      — acceptance: `grep -rnE '^(In which paths|Paths?):[[:space:]]*accounting[[:space:]]*$' <SPEC> <SPECPATHS> | wc -l`
      returns **0**, AND
      `for f in <MIRROR>; do grep -F -q 'skills/accounting' "$f" || echo "MISSING $f"; done | wc -l`
      returns **0**. Falsifiable both ways: writing a bare `Paths: accounting` line into any spec
      makes the first clause **1**.
- [ ] [AI] **Plan-02 custody check** — confirm this phase touched nothing inside the sibling plan's
      frozen corpus:
      `git diff --name-only origin/main...HEAD -- plans/backlog/ayokoding-learning-path-02-schema-and-prerequisite-dag | wc -l`
      — acceptance: returns **0**. Falsifiable both ways: editing one of the 121 plan-02 specs makes
      it **1**.
- [ ] [AI] **Prerequisite transcription check** — every spec's `## Prerequisites` section matches the
      catalog table exactly, including the two linked `(SWE)` edges
      — acceptance: `grep -F -q 'sql-essentials' "<SPEC>chart-of-accounts-and-data-modeling.md"`
      exits 0 **and** `grep -F -q 'backend-essentials' "<SPEC>capstone-build-a-general-ledger-system.md"`
      exits 0. Falsifiable both ways: both exit 1 if the edge is dropped, and a third clause below
      catches the opposite error (walking them into `courseOrder`).
- [ ] [AI] **Silent-failure coverage check** — every spec for a course from #4 onward names at least
      one outcome that still balances while being substantively wrong (DD-609)
      — acceptance:
      `for c in "${ACCT_SILENT[@]}"; do grep -F -q '## Silent failure modes' "<SPEC>$c.md" || echo "MISSING $c"; done | wc -l`
      returns **0** (returns **17** before this step). Courses #1–#3 are deliberately exempt and must
      **not** carry the section:
      `for c in "${ACCT_S1[@]}"; do grep -F -q '## Silent failure modes' "<SPEC>$c.md" && echo "UNEXPECTED $c"; done | wc -l`
      returns **0**.
- [ ] [AI] **Verification markers carried, not laundered** — the specs for #17, #18 and #20 carry the
      research's markers verbatim and cite no PSAK standard number and no doctrinal derivation as fact
      — acceptance:
      `for c in sharia-accounting-and-aaoifi-standards islamic-contract-modeling-for-systems capstone-sharia-compliant-ledger; do grep -F -q 'Needs Verification' "<SPEC>$c.md" || echo "MISSING $c"; done | wc -l`
      returns **0** (returns **3** before this step).
- [ ] [AI] **Scope-boundary check** — each spec names the sibling course it could be confused with
      (accounting, library, or ERP) and states the line between them
      — acceptance:
      `for c in "${ACCT_ALL[@]}"; do grep -F -q '## Scope boundary' "<SPEC>$c.md" || echo "MISSING $c"; done | wc -l`
      returns **0** (returns **20** before this step). Spot-verify the three highest-risk pairs by
      reading them: #2 versus `sql-essentials`, #13 versus `it-governance-grc`, #19 versus
      `backend-essentials`.
- [ ] [AI] **DD-620 check — no accounting spec declares an ERP prerequisite**:
      `grep -rlE 'erp-|record-to-report-systems|procure-to-pay-systems|order-to-cash-systems' <SPEC> | wc -l`
      — acceptance: returns **0**. Falsifiable both ways: adding one ERP prerequisite to any spec
      makes it **1**. (Prose that _mentions_ ERP as a scope boundary must therefore avoid these
      tokens, or be reworded — the check is deliberately strict.)
- [ ] [AI] Run `npm run lint:md` and
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md heading-hierarchy validate`
      over the new spec folder — acceptance: both exit 0.

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [ ] [AI] All 20 spec files exist and the folder README lists all 20 IDs — both miss-count clauses
      return **0**.
- [ ] [AI] `<MIRROR>` exists under its plan-02-mandated name, declares the full `skills/accounting`
      id and `arc: immediately-effective`, and is the **only** `manifest-*.md` under `<SPECPATHS>`.
- [ ] [AI] The canonical prefixed path-id check returns **0**, and the plan-02 custody check returns
      **0** — nothing inside the sibling plan's frozen corpus was touched.
- [ ] [AI] Both linked `(SWE)` prerequisite edges are transcribed; the silent-failure section is
      present for #4–#20 and absent for #1–#3; all 20 carry a scope boundary.
- [ ] [AI] The three Sharia specs carry `Needs Verification` markers verbatim and state no PSAK
      number or doctrinal derivation as fact.
- [ ] [AI] The ERP-prerequisite check returns **0**.
- [ ] [AI] `npm run lint:md` and `md heading-hierarchy validate` exit 0.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed (no-op).

> **Pause Safety**: only plan-side documentation exists — 20 specs plus one path mirror inside this
> plan folder. Nothing under `apps/` changed, no manifest exists, and no reader-visible surface moved.
> Safe to stop indefinitely. To resume: re-run the spec-existence, mirror-name, and marker clauses.

---

## Phase 2: Stage 1 — courses #1–#3, the manifest, and the landing

> _Suggested executor: `apps-ayokoding-www-by-example-maker` (all three bodies are By Example) +
> `apps-ayokoding-www-general-maker` (landing) + `web-researcher` (accuracy pre-verify)._
>
> **The first ramp boundary and the architecture smoke test in one phase.** At its end a reader can
> build a correctly balancing ledger — and the platform has its **first 2-segment `pathId`** resolving
> end-to-end (DD-603). It also emits the **Stage-1 signal** that clears ERP #7, the hard cross-plan
> edge.

### 2.1 · Author the three Stage-1 bodies (maker-checker-fixer, not TDD)

Apply the seven-step per-course convention to each course; each course is its own sub-phase (own
branch → draft PR → 3-cycle review → `[AI]` merge → deploy), pipelining up to the in-force cap.

1. [AI] **Accuracy pre-verify** — spot-check every external claim via `web-researcher`; volatile
   facts go in a dated accuracy-note sidebar, never the stable spine — acceptance: no claim written
   without a marker or a citation.
2. [AI] **Skeleton** — create `<COURSES><course-id>/` (`_index.md` with `prerequisites: [...]`,
   `overview.md`, `learning/_index.md`, `drilling/_index.md`), mirroring the sibling bundle shape;
   the slug and the prerequisite chain are **settled** in `<SPEC><course-id>.md` — acceptance:
   `test -d`, `test -d .../learning`, `test -d .../drilling` all exit 0 and
   `grep -F -q 'prerequisites:' "<COURSES><course-id>/_index.md"` exits 0.
3. [AI] **Author learning track** from the spec's concept and example enumeration, plus
   `learning/capstone/` — acceptance: the `overview.md` states the course's scope boundary against
   its confusable sibling.
4. [AI] **Author drilling track** — `drilling/<course-id>.md` + `drilling/overview.md` in the fixed
   five-section order — acceptance: all five sections present.
5. [AI] **Run content checkers** — `apps-ayokoding-www-by-example-checker`,
   `apps-ayokoding-www-facts-checker`, `apps-ayokoding-www-link-checker` — acceptance: findings
   recorded.
6. [AI] **Apply content fixers** — acceptance: every CRITICAL/HIGH/MEDIUM finding addressed.
7. [AI] **Re-verify** — checkers + `npx nx run ayokoding-www:build` + `npm run lint:md` —
   acceptance: zero CRITICAL/HIGH/MEDIUM remain; both commands exit 0.

- [ ] [AI] Course #1 `accounting-foundations` (By Example, no prerequisites) — the entry point for a
      reader with **neither** accounting **nor** SQL background. Mines
      `apps/ayokoding-www/content/en/legacy/business/accounting.md` per **DD-606**: harvest the
      running example and the narrative sequencing, discard the small-business-owner register, and
      leave the schema/data-modelling layer to course #2 — acceptance: all 7 convention steps
      complete; checkers report zero CRITICAL/HIGH/MEDIUM;
      `grep -F -q 'chart-of-accounts-and-data-modeling' "<COURSES>accounting-foundations/overview.md"`
      exits 0 (the forward boundary to #2 is stated). Falsifiable both ways: exits 1 today (no such
      directory) and exits 1 again if the boundary line is dropped. **No paragraph from the legacy
      article moves verbatim** — verified by reading the diff, not by grep.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Course #2 `chart-of-accounts-and-data-modeling` (By Example; prerequisites: #1 and the
      **linked** `sql-essentials`) — the course that turns a chart of accounts into a schema; this is
      the material `legacy/business/accounting.md` never had — acceptance: all 7 convention steps
      complete; `grep -F -q 'sql-essentials' "<COURSES>chart-of-accounts-and-data-modeling/_index.md"`
      exits 0 (the linked edge is declared) **and**
      `grep -F -q 'sql-essentials' "<COURSES>chart-of-accounts-and-data-modeling/overview.md"` exits 0
      (the scope boundary against it is stated — this course models ledgers, it does not teach SQL).
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Course #3 `financial-statements-and-close-cycle` (By Example; prerequisite: #2) — **the
      cross-plan hard edge**: ERP #7 `record-to-report-systems` is unblocked by this course and
      nothing else — acceptance: all 7 convention steps complete; checkers report zero
      CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] **Stage-1 body check** —
      `for c in "${ACCT_S1[@]}"; do test -d "<COURSES>$c" || echo "MISSING $c"; done | wc -l`
      — acceptance: returns **0** (returns **3** before this sub-phase).
- [ ] [AI] Append the three catalog rows to `<COURSES>_index.md` _(existing file, created by plan 01)_
      — acceptance:
      `for c in "${ACCT_S1[@]}"; do grep -F -q "$c" <COURSES>_index.md || echo "MISSING $c"; done | wc -l`
      returns **0** (returns **3** before this step); `apps-ayokoding-www-link-checker` green on
      `<COURSES>_index.md`.

### 2.2 · TDD cycle — publish the manifest

- [ ] [AI] **RED** — create `<MTEST>` _(new file; this plan owns it)_ with failing assertions that
      `<MANIFEST>` loads, zod-validates against `<FEAT>core/schemas.ts`, declares `pathId` equal to
      the **exact full string** `skills/accounting` (asserted by string equality, **never** by
      splitting on `/` or counting segments) and `arc` equal to `immediately-effective` as a separate
      field, has a `courseOrder` of **length 3** equal to the Stage-1 IDs in order, and passes
      `checkManifestIntegrity` + `checkPrerequisiteConsistency`; plus one negative assertion that a
      malformed id (`accounting`, with no category segment) is **rejected by `safeParse`** rather than
      coerced, aliased, or normalized — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the new assertions **fail** with a module-not-found or empty-glob error naming
      `skills/accounting.yaml`. A failure for any other reason (a missing `schemas.ts` import, say)
      means a start precondition was not honoured — stop and re-check Phase 0.

  **Gherkin (binds) →** "A two-segment skills path ID resolves end to end"

  ```gherkin
  Scenario: A two-segment skills path ID resolves end to end
    Given the manifest declares pathId skills/accounting and arc immediately-effective
    When a reader walks the path from its landing
    Then the landing, the prev and next controls, and the breadcrumb all resolve against the two-segment path ID
    And the ?path=skills/accounting context persists across every course in the walk
    And no resolver assumes a three-segment path ID
  ```

- [ ] [AI] **GREEN** — author `<MANIFEST>` _(new file)_ with `pathId: skills/accounting`,
      `arc: immediately-effective`, a title, a description, and a 3-entry `courseOrder` **transcribed
      from `<MIRROR>`** (never re-derived), entries as **plain ID strings** with no `framing`
      mappings (DD-619)
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0, AND `grep -E '^  - [a-z0-9-]+$' <MANIFEST> | wc -l` returns **3**, AND
      the 17 deferred IDs are absent —
      `grep -oE "$ACCT_S2_ALT|$ACCT_S3_ALT" <MANIFEST> | sort -u | wc -l` returns **0**. Falsifiable
      both ways: after Phase 3 the same alternation returns **13**, and after Phase 5 it returns
      **17**.
- [ ] [AI] **REFACTOR** — align the YAML key order and comment style with plan 02's documented
      example, and factor the load-and-validate helper in `<MTEST>` so each later growth step adds one
      assertion rather than a copied block
      — command: `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:lint`
      — acceptance: both exit 0 and no assertion was weakened (the deferred-ID clause still returns 0
      and the length clause still returns 3).

- [ ] [AI] **Link-don't-walk check (DD-602)** — assert **both** halves, so neither "walked" nor
      "forgotten" passes: `grep -oE 'sql-essentials|backend-essentials' <MANIFEST> | wc -l` returns
      **0**, AND `grep -F -q 'sql-essentials' "<COURSES>chart-of-accounts-and-data-modeling/_index.md"`
      exits 0 — acceptance: both hold. Falsifiable both ways: walking either ID into `courseOrder`
      makes the first clause ≥ 1; dropping the frontmatter edge makes the second exit 1.

  **Gherkin (binds) →** "The accounting manifest links its software-engineering prerequisites instead of walking them"

  ```gherkin
  Scenario: The accounting manifest links its software-engineering prerequisites instead of walking them
    Given the accounting path manifest is published
    When a reader inspects its courseOrder
    Then neither sql-essentials nor backend-essentials appears in courseOrder
    And the chart-of-accounts course declares sql-essentials in its prerequisites frontmatter
    And the general-ledger capstone declares backend-essentials in its prerequisites frontmatter
    And the landing links both prerequisite courses at their canonical /en/learn/courses/ URLs
  ```

### 2.3 · The landing (content — maker-checker-fixer, not TDD)

- [ ] [AI] Author `<LANDING>_index.md` _(new file — this plan's **only** file under `<PATHS>`)_ per
      [tech-docs §Landing content contract](./tech-docs.md#landing-content-contract--what-it-must-convey):
      the arc promise stated once (no arc chooser), all three ramp boundaries with both their
      capability and their ceiling, the one-paragraph explanation of why the ramp slows after #3, and
      the two linked prerequisites at their canonical `/en/learn/courses/<id>` URLs
      — acceptance: `grep -oE 'courseOrder' <LANDING>_index.md | wc -l` returns **0** (returns **1**
      if one is mistakenly added), AND
      `for t in 'Dangerous 1' 'Dangerous 2' 'Dangerous 3'; do grep -F -q "$t" <LANDING>_index.md || echo "MISSING $t"; done | wc -l`
      returns **0** (returns **3** before this step), AND
      `for t in '/en/learn/courses/sql-essentials' '/en/learn/courses/backend-essentials'; do grep -F -q "$t" <LANDING>_index.md || echo "MISSING $t"; done | wc -l`
      returns **0**.
  - _Suggested executor: `apps-ayokoding-www-general-maker`_

  **Gherkin (binds) →** "The landing states the arc and the ramp before the course list"

  ```gherkin
  Scenario: The landing states the arc and the ramp before the course list
    Given the accounting path landing is published
    When a reader opens /en/learn/paths/skills/accounting
    Then the immediately-effective promise and all three dangerous-by-here boundaries appear before the ordered course list
    And each boundary names both what the reader can do and what the reader cannot yet do
    And the ordered course list is rendered from the manifest rather than hand-listed in the landing
  ```

- [ ] [AI] **Ordering check — arc and ramp precede the list.** The ordered course list is rendered by
      plan 03's component from the loaded manifest, so "before the list" means the landing's prose
      ends before the render slot. Verify by reading the rendered page in
      [Phase 7](#phase-7-manual-ui-verification-and-rule-15-three-tester-retest), and mechanically
      here by confirming the landing contains no list of course IDs at all:
      `grep -oE "$ACCT_S2_ALT|$ACCT_S3_ALT" <LANDING>_index.md | sort -u | wc -l` returns **0**
      — acceptance: holds. Falsifiable both ways: hand-listing the corpus in the landing makes it
      ≥ 1.
- [ ] [AI] Run `apps-ayokoding-www-link-checker` and `apps-ayokoding-www-general-checker` over the
      landing — acceptance: findings recorded; then apply the matching fixers — acceptance: zero
      CRITICAL/HIGH/MEDIUM remain on re-run.

### 2.4 · TDD cycle — the path-walk e2e

- [ ] [AI] **RED** — add `<SPECS>skills-path-composition.feature` _(new file)_ carrying the
      two-segment-`pathId` scenario, plus a failing e2e step in
      `apps/ayokoding-www-fe-e2e/src/steps/course-paths.steps.ts` _(existing file, created by
      `ayokoding-learning-path-03-navigation-ui`)_ that opens `/en/learn/paths/skills/accounting`,
      walks all three courses via prev/next, and asserts `?path=skills/accounting` persists
      — command: `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: the new spec **fails** because the landing does not yet render an ordered list.
- [ ] [AI] **GREEN** — implement the step bindings against the published manifest and live landing
      — command:
      `npx nx run ayokoding-www:specs:behavior:coverage && npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: both exit 0.
- [ ] [AI] **REFACTOR** — extract a reusable "walk a skills path" helper step definition that Phase 3
      and Phase 5 reuse without duplication
      — command: `npx nx run ayokoding-www-fe-e2e:test:e2e`
      — acceptance: exits 0 and the scenario count is unchanged.

### 2.5 · Stage-1 signal

- [ ] [AI] **Record the Stage-1 signal** in this file, with all five fields from
      [tech-docs §Stage-signal contract](./tech-docs.md#stage-signal-contract-the-plan-07-handoff):
      `STAGE: 1`, `PLAN: ayokoding-learning-path-06-skills-accounting`, `LANDED_COURSE_IDS:` the
      three Stage-1 IDs, `UNBLOCKS_ERP_COURSES: 7`, `MERGED_COMMIT:` the real merge SHA
      — acceptance: the signal block is present with all five fields populated and
      `git cat-file -e <sha>^{commit}` exits 0. Falsifiable both ways: a placeholder SHA fails
      `git cat-file -e`.

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [ ] [AI] `for c in "${ACCT_S1[@]}"; do test -d "<COURSES>$c" || echo "MISSING $c"; done | wc -l`
      returns **0** (returned **3** at Phase 0).
- [ ] [AI] `test -f <MANIFEST>` exits 0 and `npx nx run ayokoding-www:test:unit` exits 0 — the
      manifest loads, zod-validates, and passes integrity + prerequisite-consistency.
- [ ] [AI] `grep -E '^  - [a-z0-9-]+$' <MANIFEST> | wc -l` returns **3**, and
      `grep -oE "$ACCT_S2_ALT|$ACCT_S3_ALT" <MANIFEST> | sort -u | wc -l` returns **0** — the deferral
      is real and recorded, not silently closed.
- [ ] [AI] The link-don't-walk clause holds in both directions.
- [ ] [AI] The landing carries all three ramp boundaries, both prerequisite links, and no
      `courseOrder`.
- [ ] [AI] `npx nx run ayokoding-www:build` + `:specs:behavior:coverage` **and**
      `npx nx run ayokoding-www-fe-e2e:test:e2e` exit 0. (`ayokoding-www:test:e2e` and
      `:test:integration` are no-op echoes and can never fail — omitted deliberately.)
- [ ] [AI] The Stage-1 signal is recorded with a real `MERGED_COMMIT`.
- [ ] [AI] Draft PRs opened per sub-phase; 3-cycle PR-Review complete on each; CI green; PRs
      `[AI]`-merged; deployed.

> **Pause Safety**: `/en/learn/paths/skills/accounting` is **live end-to-end in production** over its
> three-course Stage-1 `courseOrder` — the first 2-segment `pathId` on the platform, and a reader can
> build a balancing ledger. ERP #7 is unblocked. Nothing references the 17 deferred courses, so every
> surface is coherent. Safe to stop indefinitely. To resume: `npx nx run ayokoding-www-fe-e2e:test:e2e`.

---

## Phase 3: Stage 2 — courses #4–#16 and manifest growth to sixteen

> _Suggested executor: `apps-ayokoding-www-by-example-maker` (10 bodies) +
> `apps-ayokoding-www-annotated-concept-maker` (#12, #13, #16) + `web-researcher` (accuracy
> pre-verify)._
>
> **This is where the ramp deliberately slows.** Every course in this phase is past the point where
> mistakes fail loudly, so **every one of them carries the mandatory "what still balances while being
> wrong" section (DD-609)**. A course that cannot name a plausible-but-wrong outcome in its own
> subject has not identified what it is teaching.

- [ ] [AI] Author all 13 Stage-2 bodies, applying the seven-step convention from
      [§2.1](#21--author-the-three-stage-1-bodies-maker-checker-fixer-not-tdd) to each, one course per
      sub-phase, pipelining up to the in-force cap. Formats are settled: **By Example** for #4–#11,
      #14, #15; **Annotated-concept** for #12 `financial-reporting-standards-ifrs-vs-gaap`, #13
      `audit-controls-and-compliance`, #16 `financial-reporting-and-xbrl`
      — acceptance:
      `for c in "${ACCT_S2[@]}"; do test -d "<COURSES>$c" || echo "MISSING $c"; done | wc -l` returns
      **0** (returns **13** before this phase); every course's checkers report zero
      CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker` for #4–#11, #14, #15;
    `apps-ayokoding-www-annotated-concept-maker` for #12, #13, #16_
- [ ] [AI] **Silent-failure section present in every Stage-2 body (DD-609)** — each `overview.md`
      carries the literal heading `## What still balances while being wrong`, naming at least one
      plausible-but-wrong outcome and the observable signal (if any) that would reveal it
      — acceptance:
      `for c in "${ACCT_S2[@]}"; do grep -F -q '## What still balances while being wrong' "<COURSES>$c/overview.md" || echo "MISSING $c"; done | wc -l`
      returns **0** (returns **13** before this phase, and returns **1** if a single body drops the
      section).

  **Gherkin (binds) →** "Every post-foundations course names what still balances while being wrong"

  ```gherkin
  Scenario: Every post-foundations course names what still balances while being wrong
    Given a course from number four onward is authored
    When its overview is inspected
    Then it contains an explicit section naming at least one outcome that still balances while being substantively wrong
    And that section names the observable signal, if any, that would reveal the error
  ```

- [ ] [AI] **Scope-boundary check against the library and ERP** — the three highest-risk bodies state
      their boundary explicitly: #13 `audit-controls-and-compliance` against `it-governance-grc`
      (COSO/SOX specifics stay here, GRC frameworks stay there), #9 `inventory-and-cogs-accounting`
      against the ERP inventory course, and #11 `consolidation-and-multi-entity-accounting` against
      the ERP multi-company course
      — acceptance: `grep -F -q 'it-governance-grc' "<COURSES>audit-controls-and-compliance/overview.md"`
      exits 0, and both other bodies state their boundary in prose (verified by reading, since
      DD-620's ERP-token check forbids naming the ERP course IDs).

  **Gherkin (binds) →** "The accounting corpus never re-teaches a linked library course"

  ```gherkin
  Scenario: The accounting corpus never re-teaches a linked library course
    Given the accounting corpus is authored
    When a course's scope is compared with the library course it links as a prerequisite
    Then the course states its scope boundary against that library course explicitly
    And no accounting course teaches relational modelling, query performance, or HTTP service construction as its own subject
  ```

- [ ] [AI] Append the 13 catalog rows to `<COURSES>_index.md` — acceptance:
      `for c in "${ACCT_S2[@]}"; do grep -F -q "$c" <COURSES>_index.md || echo "MISSING $c"; done | wc -l`
      returns **0** (returns **13** before this step).

### 3.1 · TDD cycle — grow the manifest to sixteen

- [ ] [AI] **RED** — extend `<MTEST>` with a failing assertion that `courseOrder` has **length 16**
      and contains all 13 Stage-2 IDs in catalog order after the three Stage-1 IDs
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the new assertion **fails**, reporting an actual length of **3**.
- [ ] [AI] **GREEN** — append the 13 Stage-2 IDs to `<MANIFEST>` in catalog order
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0, AND `grep -E '^  - [a-z0-9-]+$' <MANIFEST> | wc -l` returns **16**, AND
      `grep -oE "$ACCT_S2_ALT" <MANIFEST> | sort -u | wc -l` returns **13** (returned **0** at the
      Phase 2 gate), AND `grep -oE "$ACCT_S3_ALT" <MANIFEST> | sort -u | wc -l` still returns **0**.
- [ ] [AI] **REFACTOR** — collapse the repeated per-stage assertions in `<MTEST>` into one
      table-driven assertion over a stage→expected-IDs map, so Phase 5 adds one row
      — command: `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:typecheck`
      — acceptance: both exit 0 and no assertion was weakened (all three count clauses above still
      hold).

### 3.2 · Stage-2 signal

- [ ] [AI] **Record the Stage-2 signal** in this file with all five fields — `STAGE: 2`,
      `LANDED_COURSE_IDS:` the 13 Stage-2 IDs, `UNBLOCKS_ERP_COURSES: 8, 13, 14, 15`,
      `MERGED_COMMIT:` the real merge SHA — acceptance: all five fields populated and
      `git cat-file -e <sha>^{commit}` exits 0.

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [ ] [AI] All 13 Stage-2 bodies exist; the miss-count clause returns **0**.
- [ ] [AI] Every Stage-2 `overview.md` carries `## What still balances while being wrong` — the
      miss-count clause returns **0**.
- [ ] [AI] `grep -E '^  - [a-z0-9-]+$' <MANIFEST> | wc -l` returns **16**; the Stage-2 alternation
      returns **13**; the Stage-3 alternation still returns **0**.
- [ ] [AI] `npx nx run ayokoding-www:test:unit` exits 0 — integrity and prerequisite-consistency green
      across all 16 entries.
- [ ] [AI] `npx nx run ayokoding-www:build` + `:specs:behavior:coverage` +
      `npx nx run ayokoding-www-fe-e2e:test:e2e` exit 0.
- [ ] [AI] The Stage-2 signal is recorded with a real `MERGED_COMMIT`.
- [ ] [AI] Draft PRs opened per sub-phase; 3-cycle PR-Review complete; CI green; PRs `[AI]`-merged;
      deployed.

> **Pause Safety**: the path is live at 16 courses — a reader can model most conventional systems a
> mid-size company runs, and the landing already tells them they cannot yet build a Sharia-compliant
> ledger. ERP #8, #13, #14 and #15 are unblocked. The four Sharia courses are absent and nothing
> references them. Safe to stop indefinitely. To resume: `npx nx run ayokoding-www:test:unit` and the
> three manifest count clauses.

---

## Phase 4: Resolve the carried verification debt (OI-1, OI-2, OI-3)

> _Suggested executor: `web-researcher`._
>
> **This phase gates the entire Sharia stage** and exists because A4 forbids laundering the research's
> verification status. It sits here rather than up front (DD-607): OI-1 and OI-2 bite only at
> #17–#20, so front-loading them would have delayed the first ramp boundary — and ERP's unblock — for
> claims Stages 1 and 2 never make.
>
> **Refusing to write a claim is always available and always preferred over writing it unlabelled.**

- [ ] [AI] **OI-1 — Indonesian PSAK numbering.** Resolve the "PSAK 59 / SIFAS 101-109" versus
      "PSAK 101-110" conflict against the **named primary source: IAI's published PSAK Syariah
      standard list** (`iaiglobal.or.id`), re-read for the current numbering generation and its
      effective dates. Record the outcome in `<VLOG>` as `OI-1: RESOLVED — <source URL> — <access
date> — <the numbering that is current>`, **or** as
      `OI-1: SCOPED-AROUND — <reason>` if the primary source cannot be reached, in which case course
      #17 teaches the structure (a parallel standard series exists, DSAS proposes and DSN-MUI
      ratifies) **without publishing a specific standard number**
      — acceptance: `grep -oE '^OI-1: (RESOLVED|SCOPED-AROUND)' <VLOG> | wc -l` returns **1**
      (returns **0** before this step).
  - _Suggested executor: `web-researcher`_
- [ ] [AI] **OI-2 — riba doctrinal basis.** Re-ground the currently-Wikipedia-sourced claim in an
      **AAOIFI Shari'ah Standard** or an **IFSB publication**. The _practical_ consequence is
      well-attested and may be stated (profit must arise from trade, leasing, partnership or service
      risk, never a predetermined return on a pure loan); the **minority time-value-of-money position
      is not settled and is not this corpus's to settle** — it is either omitted or presented
      explicitly as a minority position. Record in `<VLOG>` as
      `OI-2: RESOLVED — <source> — <access date>` or `OI-2: SCOPED-AROUND — <reason>`
      — acceptance: `grep -oE '^OI-2: (RESOLVED|SCOPED-AROUND)' <VLOG> | wc -l` returns **1**.
  - _Suggested executor: `web-researcher`_
- [ ] [AI] **OI-3 — the three-jurisdiction model beyond the fetched indexes.** Ground the governance
      mechanics against the three fetched indexes plus **Bank Negara Malaysia's Shariah Governance
      Policy 2019** document itself. Two facts must be verified specifically because both are
      commonly got wrong: **Malaysia is not on AAOIFI's mandatory-adoption list**, and **Indonesia
      uses AAOIFI as a basis rather than adopting it**. Record in `<VLOG>` as
      `OI-3: RESOLVED — <sources> — <access date>` or `OI-3: SCOPED-AROUND — <reason>`
      — acceptance: `grep -oE '^OI-3: (RESOLVED|SCOPED-AROUND)' <VLOG> | wc -l` returns **1**.
  - _Suggested executor: `web-researcher`_
- [ ] [AI] **Re-verify the AAOIFI FAS numbers** this corpus will publish — FAS 3, 4, 7, 9, 10, 28 and
      32–34 — against AAOIFI's own Financial Accounting Standards index, and confirm the FAS series is
      still distinct from the Shari'ah Standards series
      — acceptance: each number carries a `[Verified]` marker with its URL and access date in
      `<VLOG>`; any number that cannot be re-confirmed is dropped from the corpus rather than
      published `[Unverified]`.
  - _Suggested executor: `web-researcher`_
- [ ] [AI] **Propagate every resolution back into the three Sharia specs** (`<SPEC>sharia-accounting-and-aaoifi-standards.md`,
      `<SPEC>islamic-contract-modeling-for-systems.md`, `<SPEC>capstone-sharia-compliant-ledger.md`),
      replacing each carried `Needs Verification` marker with either a cited fact or an explicit
      scoped-around note — acceptance: for each of the three specs, every remaining occurrence of
      `Needs Verification` is accompanied on the same line by `SCOPED-AROUND`, verified by reading;
      and `grep -oE '^OI-[0-9]+: OPEN' <VLOG> | wc -l` returns **0**.

  **Gherkin (binds) →** "No unverified claim is published as fact"

  ```gherkin
  Scenario: No unverified claim is published as fact
    Given the research seeding this plan marked items as Unverified or Needs Verification
    When a syllabus spec or a course body states a standard number or a doctrinal position
    Then the claim carries either a primary-source citation or an explicit confidence marker
    And no item marked Needs Verification remains open when the Sharia stage begins
  ```

### Phase 4 Gate

> All checks below must pass before starting Phase 5. **No Sharia body may be authored while any
> item is still `OPEN`.**

- [ ] [AI] `grep -oE '^OI-[0-9]+: OPEN' <VLOG> | wc -l` returns **0**. Falsifiable both ways: it
      returns **3** at the Phase 3 gate (OI-1, OI-2, OI-3 open; OI-4 was routed in Phase 0).
- [ ] [AI] Each of OI-1, OI-2 and OI-3 carries exactly one `RESOLVED` or `SCOPED-AROUND` line with a
      source and an access date, or a stated reason.
- [ ] [AI] Every AAOIFI FAS number the corpus will publish is re-verified with a URL and access date,
      or dropped.
- [ ] [AI] The three Sharia specs carry no unaccompanied `Needs Verification` marker.
- [ ] [AI] `npm run lint:md` exits 0.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed (no-op).

> **Pause Safety**: the corpus is unchanged from the Phase 3 state (16 live courses); only this
> plan's research ledger and three spec files moved. Nothing user-visible changed. Safe to stop
> indefinitely. To resume: re-read `<VLOG>` and confirm no line reads `OPEN`.

---

## Phase 5: Stage 3 — courses #17–#20 and manifest growth to twenty

> _Suggested executor: `apps-ayokoding-www-annotated-concept-maker` (#17) +
> `apps-ayokoding-www-by-example-maker` (#18, #19, #20) + `apps-ayokoding-www-facts-checker`._
>
> **Three models, never one.** Courses #17, #18 and #20 each present AAOIFI, PSAK Syariah, and
> MFRS-plus-BNM as three structurally different coexisting models (DD-608). A course presenting AAOIFI
> as "the" Sharia accounting standard would be wrong.

- [ ] [AI] Course #17 `sharia-accounting-and-aaoifi-standards` (Annotated-concept; prerequisites: #4,
      #12) — the standards landscape. Authored **only** against Phase 4's resolved ledger
      — acceptance: all 7 convention steps complete; the three-model clause below holds for this
      course; `grep -F -q 'not on' "<COURSES>sharia-accounting-and-aaoifi-standards/overview.md"` is
      **not** sufficient on its own — verify by reading that the overview states Malaysia's absence
      from AAOIFI's mandatory-adoption list and Indonesia's basis-not-adoption relationship in full
      sentences.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] Course #18 `islamic-contract-modeling-for-systems` (By Example; prerequisites: #17, #2) —
      **the corpus's sharpest instance of the silent-failure property**: a murabaha receivable
      schedule and a conventional amortising loan schedule can look numerically similar and must be
      modelled and recognised completely differently. The markup is fixed and disclosed at the point
      of sale in a trade with an underlying asset changing hands; AAOIFI FAS 28 treats it as a
      trading transaction — a receivable and revenue from a sale, **not** interest income
      — acceptance: all 7 convention steps complete;
      `for t in murabaha ijara mudaraba musharaka; do grep -F -q "$t" "<COURSES>islamic-contract-modeling-for-systems/overview.md" || echo "MISSING $t"; done | wc -l`
      returns **0** (returns **4** before this step).

  **Gherkin (binds) →** "A murabaha is modelled as a trade rather than as a loan"

  ```gherkin
  Scenario: A murabaha is modelled as a trade rather than as a loan
    Given the Islamic contract modelling course is authored
    When a reader compares a murabaha receivable schedule with a conventional amortising loan schedule
    Then the course shows the two schedules can look numerically similar and must be modelled differently
    And the markup is presented as fixed and disclosed at the point of sale in a trade with an underlying asset
    And the recognition is presented as a receivable and revenue from a sale rather than interest income
  ```

  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

- [ ] [AI] Course #19 `capstone-build-a-general-ledger-system` (By Example; prerequisites: #2, #3, and
      the **linked** `backend-essentials`) — the conventional ledger the Sharia capstone contrasts
      against — acceptance: all 7 convention steps complete;
      `grep -F -q 'backend-essentials' "<COURSES>capstone-build-a-general-ledger-system/_index.md"`
      exits 0 (the linked edge is declared) **and**
      `grep -F -q 'backend-essentials' "<COURSES>capstone-build-a-general-ledger-system/overview.md"`
      exits 0 (the scope boundary is stated — this capstone builds a ledger, it does not teach HTTP
      services).
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Course #20 `capstone-sharia-compliant-ledger` (By Example; prerequisites: #18, #19) — the
      terminal capstone — acceptance: all 7 convention steps complete; the three-model clause holds.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] **Three-model clause (DD-608)** — each of #17, #18 and #20 names all three jurisdictional
      models — acceptance:
      `for c in "${ACCT_S3[@]}"; do case "$c" in capstone-build-a-general-ledger-system) continue;; esac; for t in AAOIFI 'PSAK Syariah' MFRS 'Bank Negara'; do grep -F -q "$t" "<COURSES>$c/overview.md" || echo "MISSING $c $t"; done; done | wc -l`
      returns **0** (returns **12** before this phase — three courses × four tokens). Course #19 is
      deliberately skipped: it is the conventional ledger.
- [ ] [AI] **"The standard" prohibition** — no Sharia course describes AAOIFI as the single standard
      — acceptance:
      `grep -rniE 'the (single |sole |one )?sharia (accounting )?standard' <COURSES>sharia-accounting-and-aaoifi-standards <COURSES>islamic-contract-modeling-for-systems <COURSES>capstone-sharia-compliant-ledger | wc -l`
      returns **0**. Falsifiable both ways: writing "the Sharia accounting standard" into any of the
      three makes it ≥ 1. Prose using the phrase to **negate** it must be reworded, since the check
      is deliberately blunt.

  **Gherkin (binds) →** "The Sharia stage presents three jurisdictional models"

  ```gherkin
  Scenario: The Sharia stage presents three jurisdictional models
    Given the Sharia-standards, contract-modelling, and Sharia-ledger courses are authored
    When a reader compares their treatment of standards
    Then each names AAOIFI, PSAK Syariah, and MFRS with the Bank Negara Malaysia Shariah Governance Policy as three structurally different coexisting models
    And none of them describes AAOIFI as the single Sharia accounting standard
    And each states that Malaysia is not on AAOIFI's mandatory-adoption list
    And each states that Indonesia uses AAOIFI as a basis rather than adopting it
  ```

- [ ] [AI] **Silent-failure section present in every Stage-3 body (DD-609)** — acceptance:
      `for c in "${ACCT_S3[@]}"; do grep -F -q '## What still balances while being wrong' "<COURSES>$c/overview.md" || echo "MISSING $c"; done | wc -l`
      returns **0** (returns **4** before this phase).
- [ ] [AI] Append the four catalog rows to `<COURSES>_index.md` — acceptance:
      `for c in "${ACCT_S3[@]}"; do grep -F -q "$c" <COURSES>_index.md || echo "MISSING $c"; done | wc -l`
      returns **0**.

### 5.1 · TDD cycle — grow the manifest to twenty

- [ ] [AI] **RED** — add the Stage-3 row to `<MTEST>`'s table-driven assertion: `courseOrder` has
      **length 20** and contains all four Stage-3 IDs in catalog order after the sixteen
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: the new assertion **fails**, reporting an actual length of **16**.
- [ ] [AI] **GREEN** — append the four Stage-3 IDs to `<MANIFEST>` in catalog order
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: exits 0, AND `grep -E '^  - [a-z0-9-]+$' <MANIFEST> | wc -l` returns **20**, AND
      `grep -oE "$ACCT_S3_ALT" <MANIFEST> | sort -u | wc -l` returns **4** (returned **0** at the
      Phase 3 gate), AND `grep -oE 'sql-essentials|backend-essentials' <MANIFEST> | wc -l` still
      returns **0**.

  **Gherkin (binds) →** "The manifest grows in recorded stages rather than shipping truncated"

  ```gherkin
  Scenario: The manifest grows in recorded stages rather than shipping truncated
    Given the manifest is first published with only the three Stage 1 courses
    When each later authoring stage completes
    Then the manifest grows to sixteen and then to twenty course IDs
    And every deferred course ID is recorded as absent at publication and asserted present after its growth step
  ```

- [ ] [AI] **REFACTOR** — remove any assertion the table-driven form made redundant, without
      weakening coverage — command:
      `npx nx run ayokoding-www:test:unit && npx nx run ayokoding-www:typecheck && npx nx run ayokoding-www:lint`
      — acceptance: all exit 0 and the three count clauses above still hold.

### 5.2 · Stage-3 signal and the full-ramp confirmation

- [ ] [AI] **Record the Stage-3 signal** with all five fields — `STAGE: 3`, `LANDED_COURSE_IDS:` the
      four Stage-3 IDs, `UNBLOCKS_ERP_COURSES: 19, 20`, `MERGED_COMMIT:` the real merge SHA
      — acceptance: all five fields populated and `git cat-file -e <sha>^{commit}` exits 0.
- [ ] [AI] **Full-ramp confirmation** — all twenty bodies resolve and the landing's three boundaries
      now each describe a reachable state — acceptance:
      `for c in "${ACCT_ALL[@]}"; do test -d "<COURSES>$c" || echo "MISSING $c"; done | wc -l` returns **0**
      (returned **20** at Phase 0), and the landing still carries all three `Dangerous N` markers.

  **Gherkin (binds) →** "The first ramp boundary is reachable in three courses"

  ```gherkin
  Scenario: The first ramp boundary is reachable in three courses
    Given the accounting path manifest is published with courses 1 through 3 in courseOrder
    When a reader finishes the third course
    Then the reader can build a correctly balancing ledger and produce the three statements for a single entity
    And the landing states that the reader cannot yet safely handle revenue recognition, inventory costing, leases, consolidation, or dual IFRS-and-GAAP reporting
  ```

### Phase 5 Gate

> All checks below must pass before starting Phase 6.

- [ ] [AI] All 20 bodies exist; the miss-count clause returns **0**.
- [ ] [AI] `grep -E '^  - [a-z0-9-]+$' <MANIFEST> | wc -l` returns **20**; the Stage-3 alternation
      returns **4**; the linked-prerequisite clause still returns **0**.
- [ ] [AI] The three-model clause returns **0** and the "the standard" prohibition returns **0**.
- [ ] [AI] Every Stage-3 `overview.md` carries `## What still balances while being wrong`.
- [ ] [AI] `npx nx run ayokoding-www:test:unit` + `:build` + `:specs:behavior:coverage` +
      `npx nx run ayokoding-www-fe-e2e:test:e2e` all exit 0.
- [ ] [AI] The Stage-3 signal is recorded with a real `MERGED_COMMIT`; plan 07's ERP #19 and #20 are
      unblocked.
- [ ] [AI] Draft PRs opened per sub-phase; 3-cycle PR-Review complete; CI green; PRs `[AI]`-merged;
      deployed.

> **Pause Safety**: the accounting path is complete at twenty courses and live in production; all
> three stage signals are emitted, so plan 07 is fully unblocked. Safe to stop indefinitely. To
> resume: re-run the manifest count clauses and the full-ramp confirmation.

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
      validator prints `All links valid! No broken links found.`; the other two exit 0. `md links
validate` takes **no positional path**, so the exclude form above is the only meaningful one.

  **Gherkin (binds) →** "The accounting path builds and validates green"

  ```gherkin
  Scenario: The accounting path builds and validates green
    Given the manifest is at its full twenty-course composition and every body is authored
    When the app build, the affected test tiers, and the link and heading validators run
    Then the build and every affected tier succeed
    And manifest integrity and prerequisite consistency report zero violations for the accounting manifest
    And the manifests directory contains exactly one file this plan owns
  ```

- [ ] [AI] **Manifest integrity + prerequisite-consistency sweep** — every `courseOrder` ID resolves;
      no duplicate ID; prerequisite-consistency holds across all 20 entries; no forked body
      — command: `npx nx run ayokoding-www:test:unit`
      — acceptance: zero violations reported.
- [ ] [AI] **Ownership boundary check — manifests.** Confirm this plan's commits touched exactly one
      file under `<MANIFESTS>`:
      `git diff --name-only origin/main...HEAD -- <MANIFESTS> | grep -vF 'skills/accounting.yaml' | wc -l`
      — acceptance: returns **0**. Falsifiable both ways: a step that touched `manifests/careers/**`
      or plan 07's ERP manifest makes it ≥ 1. _(A count of all `.yaml` files under `<MANIFESTS>` is
      deliberately **not** used: plans 05 and 07 land their own manifests concurrently, so a fixed
      total would be a false failure.)_
- [ ] [AI] **Ownership boundary check — `<PATHS>`.** Confirm this plan created no structural
      `_index.md` (A3):
      `git diff --name-only origin/main...HEAD -- <PATHS> | grep -vF 'paths/skills/accounting/_index.md' | wc -l`
      — acceptance: returns **0**. Falsifiable both ways: creating `paths/skills/_index.md` makes it
      **1**.
- [ ] [AI] **Ramp-smoothness audit** — walk the published `courseOrder` and confirm the three
      boundaries hold against the landed content: #1–#3 genuinely produce a balancing ledger, #16
      genuinely covers conventional systems, and every course from #4 onward names its silent failure
      — acceptance: every boundary is supportable by the bodies that precede it; **a regression is
      fixed by softening or bridging a body in place, never by reordering the manifest** (reordering
      can silently break prerequisite-consistency).
- [ ] [AI] **Cross-plan link check (this plan's own folder)** —
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md links validate --exclude plans/done --exclude apps/ayokoding-www/content --exclude apps/ose-www/content 2>&1 | grep -F "ayokoding-learning-path-06-skills-accounting"`
      — acceptance: the `grep` finds **no** matching line (exit 1). Falsifiable the other way too:
      introduce one bad relative link into this folder and the same command prints that file and
      exits 0.

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes
> (Root Cause Orientation). Commit preexisting fixes separately with conventional-commit messages.

### Phase 6 Gate

> All checks below must pass before starting Phase 7.

- [ ] [AI] Affected `typecheck` / `lint` / `test:quick` / `test:unit` / `specs:behavior:coverage`
      exit 0; `ayokoding-www-fe-e2e:test:e2e` exits 0; the build exits 0.
- [ ] [AI] Link + heading + markdown validation green; the link validator prints
      `All links valid! No broken links found.`
- [ ] [AI] Manifest integrity + prerequisite-consistency report zero violations across all 20 entries.
- [ ] [AI] Both ownership boundary checks return **0**.
- [ ] [AI] The ramp-smoothness audit passes for all three boundaries.
- [ ] [AI] The scoped cross-plan link check finds no line naming this plan's folder.
- [ ] [AI] Draft PR opened; 3-cycle PR-Review complete; CI green; PR `[AI]`-merged; deployed.

> **Pause Safety**: the whole twenty-course composition passes every automated gate and the ownership
> boundary is provably intact. Safe to stop indefinitely. To resume: re-run the affected quality gates
> and both boundary checks.

---

## Phase 7: Manual UI verification and Rule-15 three-tester retest

> This plan ships one user-visible path landing plus twenty user-visible course pages, so the
> **Rule-15 three-tester retest is mandatory** before archival. The **UI-design-funnel is exempt** —
> no net-new screen or component is added here, and every design asset belongs to
> `ayokoding-learning-path-03-navigation-ui`; see
> [prd.md §UI-design-funnel disposition](./prd.md#ui-design-funnel-disposition).
>
> **Locale scope**: `en` only. The supported-locale set is `["en", "id"]` [Repo-grounded —
>
> > `apps/ayokoding-www/src/features/i18n/core/config.ts`], but `id/belajar/` holds zero courses and
> > zero paths, so an `id` walk-through would be fabricated rather than verified. Recorded as a non-goal
> > in [brd.md §Business-Scope Non-Goals](./brd.md#business-scope-non-goals), not a skipped locale.

- [ ] [AI] Confirm `en` is the only content locale for this path — command:
      `test -d <LANDING> && test ! -d apps/ayokoding-www/content/id/belajar/paths`
      — acceptance: exits 0 (the `en` landing exists and no `id` path bucket exists).
- [ ] [AI] Start the dev server: `npx nx dev ayokoding-www` — acceptance: server up on the app's
      configured port (3101).
- [ ] [AI] For `en` × breakpoints (375 / 768 / 1280 px), via Playwright MCP `browser_navigate` +
      `browser_resize`: open `/en/learn/paths/skills/accounting` and confirm the arc promise and all
      three ramp boundaries render **above** the ordered course list, that each boundary shows both
      its capability and its ceiling, and that the list shows all twenty courses in manifest order
      — acceptance: all behaviours correct at all three breakpoints.
- [ ] [AI] Walk courses #1 → #4 via prev/next and confirm `?path=skills/accounting` persists, the
      breadcrumb shows the two-segment path, and each course page shows its prerequisites — including
      `sql-essentials` on course #2 — acceptance: all four hold.
- [ ] [AI] Confirm the skills category landing `/en/learn/paths/skills/` (plan 01's index) now lists
      this path rather than rendering empty — acceptance: the accounting path appears. If it does not,
      **record the gap and route it to plan 01 or 03** rather than creating or editing that
      `_index.md` here (A3).
- [ ] [AI] Deep-link course #2 with **no** `?path=` and confirm the canonical view renders with its
      prerequisites surfaced and an obvious way into the path. Then exercise **hard rejection** of a
      malformed id: hit `?path=skills/nonexistent` (unresolvable) and `?path=accounting` (missing the
      category segment) and confirm each is **rejected outright** — no manifest resolves, **no
      coercion to `skills/accounting`, no alias, no normalization, no nearest-match fallback** — and
      the course falls back to its own canonical no-path view with no error — acceptance: all three
      hold. Falsifiable both ways: if either malformed id renders the accounting path context, the
      resolver is lenient and that is a defect to raise against plan 02, not to accept here.
- [ ] [AI] Confirm the landing's two outbound prerequisite links resolve — acceptance:
      `/en/learn/courses/sql-essentials` and `/en/learn/courses/backend-essentials` both return 200.
- [ ] [AI] Verify `html[lang]` is `en` and `browser_console_messages` is clean on every screen —
      acceptance: correct lang attribute; **zero** console errors.
- [ ] [AI] Capture one screenshot per screen per breakpoint via `browser_take_screenshot` to
      `evidence/phase-7-<screen>-en-<breakpoint>px.png`, for 5 screens (the landing, the skills
      category index, and courses #1, #2, #4) — acceptance:
      `find evidence -name 'phase-7-*-en-*px.png' | wc -l` returns **15** (5 screens × 3 breakpoints).
      Falsifiable both ways: a missed breakpoint or screen returns fewer.
- [ ] [AI] Document the evidence in this checklist: reference each screenshot
      (`![alt](./evidence/...)`) and note the console/network status per screen.
- [ ] [AI] Run the three live-site testers (the `web-ux-test-fixing-planning` workflow:
      `web-exploratory-tester` + `web-usability-tester` + `web-design-tester`) against the running
      landing, the skills category index, and a sample walk of the first four courses in path context.
      **Direct the usability tester specifically at the ramp**: does a reader learn how far in they
      become useful, and what they still cannot do, without reading the course list?
      — acceptance: EWT/UWT/DWT findings and spec-gaps recorded.
- [ ] [AI] Append each finding below as a new unchecked checkbox, source-attributed
      (`- [ ] EWT-NNN:` / `- [ ] UWT-NNN:` / `- [ ] DWT-NNN: <defect> — fix before archival`); append
      any SG-###/USS-### items to the relevant spec step in Phases 1–5.

### Rule-15 retest follow-ups

- [ ] [AI] _(populated during the retest — every EWT/UWT/DWT defect finding must be fixed and ticked
      before archival; deferral of a defect requires explicit user permission and only when genuinely
      impossible; SG-###/USS-### may be triaged or deferred with written rationale)_

### Phase 7 Gate

> All checks below must pass before starting Phase 8.

- [ ] [AI] Landing + skills index + sample course walk + prerequisite display verified in `en` at
      375 / 768 / 1280 px; console clean on every screen.
- [ ] [AI] The arc promise and all three ramp boundaries render above the ordered course list at every
      breakpoint.
- [ ] [AI] `find evidence -name 'phase-7-*-en-*px.png' | wc -l` returns **15**; each screenshot is
      referenced from this checklist.
- [ ] [AI] Every rule-15 EWT/UWT/DWT defect finding is fixed and ticked, or explicitly permitted to
      defer by the user.
- [ ] [AI] Draft PR opened (retest evidence and any fixes); 3-cycle PR-Review complete; CI green; PR
      `[AI]`-merged; deployed.

> **Pause Safety**: the accounting path is verified live and defect-clean in `en`, with committed
> evidence. Safe to stop indefinitely. To resume: re-run the three testers against the running app.

---

## Phase 8: Final origin main integration and CI verification

- [ ] [AI] Confirm no plan PR is still open:
      `gh pr list --search "ayokoding-learning-path-06-skills-accounting" --state open --json number --jq 'length'`
      — acceptance: returns **0**; every prior phase and sub-phase branch has been `[AI]`-merged.
- [ ] [AI] Sync the shared worktree to the latest `origin/main` and run the full affected suite:
      `npx nx affected -t typecheck lint test:quick test:unit specs:behavior:coverage` +
      `npx nx run ayokoding-www-fe-e2e:test:e2e` + `npx nx run ayokoding-www:build`
      — acceptance: all exit 0 on the integrated `main`.
- [ ] [AI] Monitor the final `main` CI run — poll every ~2 minutes with one
      `gh run view --json status,conclusion` per wakeup; never `gh run watch`, never a tight loop
      — acceptance: all GitHub Actions green; fix root causes and push follow-ups (own PR → review →
      `[AI]` merge) until green.
- [ ] [AI] Confirm `prod-ayokoding-www` serves `/en/learn/paths/skills/accounting` with all twenty
      courses; re-dispatch `apps-ayokoding-www-deployer` if any earlier deploy lagged — acceptance:
      production serves the complete path.
- [ ] [AI] **Confirm all three stage signals are readable in this file** with real merged SHAs, so
      plan 07 can consume them without asking — acceptance:
      `grep -oE '^STAGE: [123]$' delivery.md | wc -l` returns **3**, and each block's `MERGED_COMMIT`
      passes `git cat-file -e <sha>^{commit}`.

### Phase 8 Gate

> All checks below must pass before starting Phase 9.

- [ ] [AI] Zero open plan PRs; every prior phase merged to `main`.
- [ ] [AI] Full affected suite + e2e + build green on the integrated `main`; the final `main` CI run
      is green.
- [ ] [AI] `prod-ayokoding-www` serves the twenty-course accounting path.
- [ ] [AI] All three stage signals present with verifiable merged SHAs.

> **Pause Safety**: the whole plan is integrated on `main`, green in CI, and live in production; plan
> 07 has everything it needs. Safe to stop indefinitely. To resume: re-run the affected suite on
> `main` and check CI and prod status.

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
      post-mortem) may land inline for a small edit or as a `plans/backlog/` follow-up for a large
      one; **code homes (`apps/`, `libs/`, tests) are ALWAYS filed as a separate `plans/backlog/<slug>/`
      plan and NEVER landed inline in this plan's own commits or PR** — acceptance: every
      `learnings.md` entry records its terminal routing state.
- [ ] [AI] **Two routing candidates to expect from this plan specifically** (record whichever
      actually surfaced, discard the other): the **cross-domain linked-prerequisite pattern** (a
      subject path linking rather than walking library prerequisites) is a candidate for
      `repo-governance/`; and the **OI-4 wording seam** in plan 02's prerequisite-omission rule is a
      candidate for a `plans/backlog/` follow-up if it was never amended — acceptance: each is either
      routed or discarded with a reason.
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
- [ ] [AI] **Rule-16 API exploratory retest — not applicable**, recorded rather than skipped: this
      plan changes no REST or GraphQL endpoint and ships no API contract, so `api-exploratory-tester`
      has nothing to exercise. The plan's API-gate posture (**NOT exempt**, exercised via manifest
      integrity) is declared in
      [tech-docs §UI-gate and API-gate posture](./tech-docs.md#ui-gate-and-api-gate-posture-r9).
- [ ] [AI] **Terminal twenty-course assertion** — all twenty bodies resolve, the manifest is at its
      full composition, and the linked prerequisites are still linked:
      `for c in "${ACCT_ALL[@]}"; do test -d "<COURSES>$c" || echo "MISSING $c"; done | wc -l` returns **0**,
      AND `grep -E '^  - [a-z0-9-]+$' <MANIFEST> | wc -l` returns **20**, AND
      `grep -oE 'sql-essentials|backend-essentials' <MANIFEST> | wc -l` returns **0**, AND
      `npx nx run ayokoding-www:test:unit` exits 0 — acceptance: all four hold. **No global
      `<COURSES>` directory count is asserted** (DD-618): plan 04 authors concurrently, so the total
      is a moving target and the 127-course figure remains the careers-only catalog total.
- [ ] [AI] **Scoped cross-plan link check** — re-run the Phase 6 filtered link validation and confirm
      it still finds no line naming this plan's folder. If any upstream plan has archived since,
      confirm every cross-plan reference in this folder points at its `plans/done/YYYY-MM-DD__…` path
      — acceptance: the filtered `grep` exits 1 and the repo-wide filtered validator prints
      `All links valid! No broken links found.`
- [ ] [AI] Move: `git mv plans/in-progress/ayokoding-learning-path-06-skills-accounting plans/done/YYYY-MM-DD__ayokoding-learning-path-06-skills-accounting`
      using today's completion date (the `evidence/`, `syllabus/` and `verification-log.md` artefacts
      move with it).
- [ ] [AI] Update `plans/in-progress/README.md` — remove the plan entry.
- [ ] [AI] Update `plans/done/README.md` — add the plan entry with its completion date.
- [ ] [AI] Update any other READMEs that reference this plan (`plans/README.md`,
      `plans/backlog/README.md`), and update `ayokoding-learning-path-07-skills-erp`'s
      cross-references to this plan's new archived path in the **same commit** as the `git mv`.
- [ ] [AI] Commit the archival:
      `chore(plans): move ayokoding-learning-path-06-skills-accounting to done`.

### Phase 10 Gate

> All checks below must pass. This is the terminal gate of the accounting half of the skills
> category.

- [ ] [AI] Twenty bodies resolve; the manifest holds twenty IDs; the linked prerequisites are still
      linked; `test:unit` and `build` exit 0.
- [ ] [AI] The filtered link check finds no line naming this plan's folder, and the repo-wide filtered
      validator prints `All links valid! No broken links found.`
- [ ] [AI] Plan folder is under `plans/done/YYYY-MM-DD__ayokoding-learning-path-06-skills-accounting`;
      every referencing README is updated; plan 07's cross-references are repointed in the same
      commit; the archival is committed.
- [ ] [AI] Draft PR opened (archival move); 3-cycle PR-Review complete; CI green; PR `[AI]`-merged;
      deployed (no-op).

> **Pause Safety**: the plan is archived and its final PR `[AI]`-merged to `main`. Terminal state.
> `ayokoding-learning-path-07-skills-erp` is unblocked end-to-end. To resume: nothing.

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
- [ ] [AI] `npx nx run ayokoding-www-fe-e2e:test:e2e` exits 0 for any phase touching the manifest or
      the landing.
- [ ] [AI] `npm run lint:md` exits 0 for any phase touching markdown.
- [ ] [AI] Fix ALL failures — including preexisting issues not caused by your changes (Root Cause
      Orientation).

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes.
> Commit preexisting fixes separately with appropriate conventional-commit messages.
