# Delivery Checklist — Learning Path Course Authoring

This checklist authors **90 course bodies** into
`apps/ayokoding-www/content/en/learn/courses/<course-id>/`: the **6 net-new AI-engineering courses**,
the **61 transferred FS-SE topics**, the **10 remaining new courses**, the **8 remaining capstones**,
and the **5 deferred interview-technique bodies** (Band 9). It also locks the three **course-surgery
contracts** (evals forward-link, D9 naming/citation, D11 concept additions) so Band 5 applies them by
construction rather than as a retrofit.

> **This plan never edits a manifest file.** Every file under `<MANIFESTS>` belongs to
> [`ayokoding-learning-path-05-manifests`](../ayokoding-learning-path-05-manifests/README.md). This
> plan's only outbound artefact is the **band-completion signal** recorded at the end of each band
> phase. See
> [README §The manifest ownership invariant](./README.md#the-manifest-ownership-invariant-binding)
> and
> [tech-docs §The manifest ownership invariant](./tech-docs.md#the-manifest-ownership-invariant-binding).
>
> **Cross-plan source of truth** — the 128-file `syllabus/` detail layer lives in
> [`../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/README.md).
> Every course body is authored **from** its `syllabus/courses/<course-id>.md` spec. **Never copy
> those files into this plan** — a copy forks the source of truth for 121 course specs.
>
> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
> Git-mechanical steps (worktree create/remove, branch, push, merge) are `[AI]`. **This plan contains
> no `[HUMAN]` step.**
>
> **Phase Gate** — every phase ends with a `### Phase N Gate` (must-pass verification) plus a
> `> **Pause Safety**:` note (safe-to-stop state + resume command). Every gate covers the phase's
> **content correctness** (checkers, build, lint). A gate in a phase named as a delivery boundary in
> the [`### Delivery Boundaries`](#delivery-boundaries) table additionally covers **integration**
> (draft PR opened, 3-cycle PR-Review, CI green, `[AI]` merge, `ayokoding-www` deployed); a gate in an
> **intermediate** phase instead confirms the work is committed to its delivery unit's branch with
> nothing pushed for review yet — see [Plans Organization Convention §PRs Open at Delivery
> Boundaries](../../../repo-governance/conventions/structure/plans.md#prs-open-at-delivery-boundaries-not-every-phase-hard-rule).
> A phase is not complete until every gate check is green.
>
> **Executor environment note — RTK-wrapped commands emit an empty-output marker, not true
> emptiness**: this repo routes `git` (and other commands) through RTK via a Claude Code hook (see
> `CLAUDE.md` §RTK), and RTK rewrites the output it filters. For `git diff` it appends a three-line
> trailer — blank, `--- Changes ---`, blank — whenever the result is **non-empty**. So for `N` changed
> paths, `| wc -l` prints `N + 3` and `| grep -c .` prints `N + 1`. In the **clean** state the two
> forms **diverge**: `| grep -c .` prints `0`, but `| wc -l` prints `1`, because RTK emits a lone
> newline as an empty-output marker rather than true zero-byte emptiness — precisely the behaviour
> this note is named after. That divergence is the whole reason `grep -c .` is the sanctioned
> zero-assertion form here and `wc -l` is never used for one.
> [Repo-grounded — measured on this tree 2026-07-22, each command issued alone as the whole content of
>
> > one call: 12 changed files gave **15** and **13** respectively; a clean path gave **1** under
> > `wc -l` and **0** under `grep -c .`. An earlier revision of this line claimed the clean state gave
> > "0 and 0"; the `wc -l` half of that was wrong.]
>
> **Every `git diff --name-only …` clause in this plan asserts `0`**, and for that assertion the
> sanctioned form **`| grep -c .`** is exact: the trailer is absent in the clean state, which is the
> only state these clauses accept. The form is **not** exact for a non-zero assertion — do not reuse
> it to count changed files. A clause needing a real count must interpose a `grep -F …` / `grep -E …`
> path filter (the literal `--- Changes ---` matches no path pattern and is dropped) or read the
> command through `rtk proxy git diff …`.
>
> None of this generalizes to `ls` — **never use an `ls`-based emptiness assertion** (an
> `ls <dir> | wc -l` clause asserting 0 is unreliable under RTK).

## Worktree

Worktree path: `worktrees/ayokoding-learning-path-04-course-authoring/`

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree ayokoding-learning-path-04-course-authoring
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the latest
`origin/main` when missing, syncs with `origin/main` before implementing, and prompts before deleting
the worktree after the plan is archived and pushed.

Every phase branches from the **latest `origin/main`** inside this one shared worktree
(`git fetch origin && git checkout main && git pull && git checkout -b ayokoding-learning-path-04-course-authoring/<phase-slug>`)
and authors its work there, committing as it goes. Only the phase(s) named as a **delivery boundary**
in the [`### Delivery Boundaries`](#delivery-boundaries) table push that branch and open **their own
draft PR**; an **intermediate** phase commits (and may push the branch for durability) without opening
one, per [Plans Organization Convention §PRs Open at Delivery
Boundaries](../../../repo-governance/conventions/structure/plans.md#prs-open-at-delivery-boundaries-not-every-phase-hard-rule).
**Phase 0 is excluded from opening a PR under any circumstance**: it is setup and baseline, pushes no
branch and opens no PR, and its evidence artifacts ride the Phase 1 PR.

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans.md#worktree-specification).

## Delivery Mode: worktree-to-pr

Each **delivery boundary** named in the [`### Delivery Boundaries`](#delivery-boundaries) table —
**Phase 1 onward**; Phase 0 opens none — works in the shared worktree on its **own branch**, opens a
**draft PR** against `main`,
runs the **PR-Review Maker→Fixer Cycle** (fan-out → `pr-review-synthesis-maker` → `pr-review-fixer`, 3 sequential
CI-gated cycles), flips the PR to ready, and `[AI]` **merges it automatically once all quality gates
are green** — then `[AI]` **deploys `ayokoding-www` to `prod-ayokoding-www` after every merge** (this
plan ships to ayokoding.com). An **intermediate** phase inside a delivery unit instead commits (and may
push for durability) to that unit's branch without opening a PR of its own. See
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
>
> **`DL-11` does not exist.** The slot is `DN-11`, a Delivery Note. The Decisions-Locked register runs
> DL-1…DL-17 with **17** entries, not 25. Never renumber to close the apparent gap.

**Delivery-Boundary Integration Protocol** (each delivery boundary's gate lists these as must-pass —
see the [`### Delivery Boundaries`](#delivery-boundaries) table, in `## Parallelization Model` below,
for which phase(s) land in each boundary; these steps fire once per **delivery boundary**, not once
per phase — an intermediate phase inside a unit commits without running them, and a band phase's
course-level sub-phases each run this same five-step protocol at their own narrower per-course
granularity, per the NEW-course authoring convention). **Phase 0 is excluded**: it is Environment
Setup and Baseline, opens no PR, pushes no branch, runs no review cycle, and merges nothing; its
evidence artifacts ride the Phase 1 PR
([§Phase 0 Opens No PR](../../../repo-governance/conventions/structure/plans.md#phase-0-opens-no-pr--the-earliest-pr-is-phase-1-hard-rule)).

1. [AI] Sync the worktree to latest `origin/main` and branch:
   `git fetch origin && git checkout main && git pull && git checkout -b ayokoding-learning-path-04-course-authoring/<phase-slug>`.
2. [AI] Stage only this phase's paths (`git add <explicit paths>` — never `git add -A`), commit
   thematically (Conventional Commits, imperative, no period), push the branch, open a **draft PR**
   against `main` (`gh pr create --draft --base main ...`) — CI runs on the PR.
3. [AI] Run the **PR-Review Maker→Fixer Cycle** (3 sequential CI-gated cycles), resolve every finding,
   then `gh pr ready`.
4. [AI] **Merge** once all quality gates are green (typecheck, lint, `test:quick`, `test:unit`,
   `specs:behavior:coverage`, CI, the 3-cycle review) — `[AI]` auto-merge per DN-11.
5. [AI] Dispatch `apps-ayokoding-www-deployer` to deploy `ayokoding-www` to `prod-ayokoding-www`.

## Depends-on

| Relation        | Plan (full folder name)                                  | Nature                                                                                                          |
| --------------- | -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| **blockedBy**   | `ayokoding-learning-path-01-url-restructure`             | **Hard.** Creates the flat `<COURSES>` bucket + `<COURSES>_index.md` + the 37 re-homed bundles this plan joins. |
| **blockedBy**   | `ayokoding-learning-path-02-schema-and-prerequisite-dag` | **Hard.** Owns `syllabus/` (every authoring source spec) and the `prerequisites` frontmatter contract.          |
| **blocks**      | `ayokoding-learning-path-05-manifests`                   | The manifest plan's `courseOrder` IDs resolve only after this plan's bands land; it consumes the band signals.  |
| **independent** | `ayokoding-learning-path-03-navigation-ui`               | Same Wave 2. Touches `<FEAT>` app code only; this plan touches content only. No shared file.                    |

**Start precondition (hard gate, checked in Phase 0)**: both blocking plans are **merged to
`origin/main`**. This plan does not start on a promise.

## Parallelization Model

**Cap**: honor the in-force subagent/PR-review concurrency cap (parallel-by-default, background
subagents capped per the orchestration convention). The main thread self-promotes nothing.

- **Phase 0** is a single serial baseline.
- **Phase 1 (six AI courses)** — content-independent bodies (each writes only its own
  `<COURSES><id>/` subtree) that **pipeline concurrently** through review, bounded by the cap. One
  ordering constraint: `statistics-for-evaluation` is a **hard prerequisite** of
  `evaluating-ai-systems-in-depth`, so it is authored before (or in the same review cycle as) the
  deep-evals course.
- **Phase 2 (surgery contracts)** is a serial sync point — documentation-only, but every Band 5/8
  acceptance criterion derives from it.
- **Phases 3–11 (Bands 1–9)** — bodies within a band are content-independent and pipeline
  concurrently, bounded by the cap. Band ordering is fixed only where content depends on content:
  **Band 5 after Phase 2** (the contracts it applies by construction), **Band 8 after Band 5** (the
  coding-agent capstone assembles the harness cluster). Bands 1–4, 6, 7, and 9 are mutually
  independent; their listed order is convenience.
- **Phases 12–16 (finalization)** is serial.

**Path constants** (referenced throughout):

- `<COURSES>` = `apps/ayokoding-www/content/en/learn/courses/` (course bundles; served at `/en/learn/courses/<course-id>`)
- `<PATHS>` = `apps/ayokoding-www/content/en/learn/paths/` (path-landing anchors — **read-only here**)
- `<SE_OLD>` = `apps/ayokoding-www/content/en/learn/fundamentally-strong/software-engineer/` (legacy home of the 33 shipped topics + 4 existing capstones — **read-only here**; the re-home is the URL-restructure plan's work)
- `<FEAT>` = `apps/ayokoding-www/src/features/course-paths/` (**never written here**)
- `<MANIFESTS>` = `<FEAT>manifests/` (**never written here** — manifest-plan property; read-only reference only)
- `<SYLLABUS>` = `../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/` (cross-plan authoring source of truth — **never copied**)

### Delivery Boundaries

| Phase(s) | Delivery unit                                                                                                | Worktree / branch                                                                                                                                                     | PR opens                                  |
| -------- | ------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| 0        | — (setup and baseline)                                                                                       | —                                                                                                                                                                     | no                                        |
| 1        | AI-engineering courses (6 bodies)                                                                            | shared worktree; one branch + draft PR per course (6 independent DAG-leaf PRs; see NEW-course authoring convention)                                                   | yes — per course, as each of the 6 lands  |
| 2, 7     | Band 5 — Architecture, distributed & AI/harness (+ Phase 2 surgery-contract lock, 15 bodies)                 | shared worktree; one branch + draft PR per course (15 independent DAG-leaf PRs); Phase 2's contract text rides the first Band-5 course's PR (`software-architecture`) | yes — per course, as each of the 15 lands |
| 3        | Band 1 — Data depth (5 bodies)                                                                               | shared worktree; one branch + draft PR per course (5 independent DAG-leaf PRs)                                                                                        | yes — per course, as each of the 5 lands  |
| 4        | Band 2 — Web, backend & platform productivity (10 bodies)                                                    | shared worktree; one branch + draft PR per course (10 independent DAG-leaf PRs)                                                                                       | yes — per course, as each of the 10 lands |
| 5        | Band 3 — Mobile & desktop platforms (10 bodies)                                                              | shared worktree; one branch + draft PR per course (10 independent DAG-leaf PRs)                                                                                       | yes — per course, as each of the 10 lands |
| 6        | Band 4 — Concurrency languages (4 bodies)                                                                    | shared worktree; one branch + draft PR per course (4 independent DAG-leaf PRs)                                                                                        | yes — per course, as each of the 4 lands  |
| 8        | Band 6 — Low-level systems, JVM & languages, internals builds (16 bodies)                                    | shared worktree; one branch + draft PR per course (16 independent DAG-leaf PRs)                                                                                       | yes — per course, as each of the 16 lands |
| 9        | Band 7 — Security, ops, quality & delivery (11 bodies)                                                       | shared worktree; one branch + draft PR per course (11 independent DAG-leaf PRs)                                                                                       | yes — per course, as each of the 11 lands |
| 10       | Band 8 — Remaining capstones (8 bodies)                                                                      | shared worktree; one branch + draft PR per course (8 independent DAG-leaf PRs)                                                                                        | yes — per course, as each of the 8 lands  |
| 11       | Band 9 — Interview-technique courses (5 bodies)                                                              | shared worktree; one branch + draft PR per course (5 independent DAG-leaf PRs)                                                                                        | yes — per course, as each of the 5 lands  |
| 12       | Final content-correctness sweep (structural verification + supersession sweep)                               | `ayokoding-learning-path-04-course-authoring/phase-12-verification`                                                                                                   | yes — at Phase 12                         |
| 13-16    | Plan closeout (manual verification evidence, final `main`/CI integration check, Knowledge Capture, archival) | `ayokoding-learning-path-04-course-authoring/phase-16-closeout`                                                                                                       | yes — at Phase 16                         |

Every band (Phases 1, 3–11) is already a genuine boundary at the **course-level** granularity the
NEW-course authoring convention uses: each course is a content-independent DAG leaf, so "one PR per
course" is the sanctioned DAG-leaf-per-PR pattern
([AGENTS.md §Delivery Mode](../../../AGENTS.md#delivery-mode): "each change-producing DAG leaf gets
its own worktree and PR (strict 1-PR ↔ 1-worktree)"), not a phase-wide PR — no band needed to change.
**Phase 2 is intermediate**:
it locks the evals/D9/D11 contracts into this checklist's own text so Band 5 (Phase 7) applies them
**by construction**, and ships no content of its own, so its edits ride the first Band-5 course PR
rather than opening a standalone PR. **Phase 12 stays its own boundary**: unlike Phases 13–15, it lands
a real content fix (the supersession sweep) plus the plan-wide structural/build/link verification, and
already passes all four boundary-test criteria standalone — deferring it into the closeout unit would
defer an already-reached boundary, which the convention forbids. **Phases 13, 14, and 15 are
intermediate**: Phase 13's screenshots and Phase 15's `learnings.md` triage are evidence the Phase 16
archival gate itself reads and verifies as a precondition (the textbook "a later phase consumes it"
signature of scaffolding), and Phase 14 makes no routine change at all (verification/CI-monitoring
only) — all three fold into the Phase 16 closeout PR, which is the plan's last change-producing phase
and therefore always a boundary.

---

## Phase 0: Environment Setup & Baseline

> _Executor: repo-setup-manager_
>
> **Cross-plan precondition (hard).** Unlike the source plan, this plan has two blocking predecessors.
> Both must be merged to `origin/main` before any authoring begins — a body authored into a
> `<COURSES>` bucket that does not yet exist lands in the wrong place, and a body authored from a
> `syllabus/` spec that has not landed is authored from nothing.

- [ ] [AI] Enter/provision the worktree and install dependencies: `npm install`
      — acceptance: exits 0, `node_modules/` synchronized.
- [ ] [AI] Converge the toolchain: `npm run doctor -- --fix`
      — acceptance: exits 0 with no unresolved drift.
- [ ] [AI] **Verify blocking plan #1 merged** — the `<COURSES>` bucket exists and holds the 37 re-homed
      bundles — command (single line):
      `test -d apps/ayokoding-www/content/en/learn/courses && test -f apps/ayokoding-www/content/en/learn/courses/_index.md && git ls-files -- 'apps/ayokoding-www/content/en/learn/courses/*/_index.md' | grep -c .`
      — acceptance: both `test` commands exit 0 and the count returns **37** (one `_index.md` per
      re-homed bundle; the bucket's own top-level `_index.md` sits one level up and is not matched).
      **Count with `git ls-files` here**, because it expands its own quoted pathspec so zsh never sees
      the `*` and the `*/` segment stays a single directory level. **The RTK routing rule, stated
      accurately.** The Claude Code hook rewrites a **bare** `find` — one whose output is not piped —
      to `rtk find`, which reformats the file list into a compact report (`2F 1D:`, a blank line, then
      `./ a.yaml b.yaml`; or the single line `0 for '<pattern>'` when nothing matches) and drops flags
      it does not know, such as `-mindepth`. A line count over that reads _format_ lines, not matches.
      A **piped** `find … | wc -l` is not rewritten and returns real output. Earlier revisions of this
      note claimed the routing was unpredictable; it is not — it is decided by the invocation shape.
      [Repo-grounded — measured 2026-07-22, each command issued **alone as the whole content of one
      call**: piped `find <dir> -name '*.yaml' | wc -l` read the true **2**, and the same query over an
      empty directory read the true **0**. The reformatted report reproduces under a bare `find` or an
      explicit `rtk find`. **Measurement caveat**: an earlier revision cited "10 of 10" and "40 of 40"
      runs collected inside `for` loops — a loop, a `$(…)` substitution, a subshell `( … )`, and a
      redirection to a file each **suppress** the hook, so those counts described the wrapper rather
      than the clause. `git diff` does **not** share this behaviour — its filter fires even when piped
      — so the two commands must never be reasoned about as one rule.] Falsifiable both ways:
      before the URL-restructure plan merges the leading `test -d` exits non-zero, the `&&` chain
      short-circuits so the `git ls-files` count never runs and no number is printed at all; a count
      other than 37
      means the re-home is incomplete and this plan must not start.
- [ ] [AI] **Verify blocking plan #2 merged** — the cross-plan syllabus layer is on `origin/main`.
      Locate it with a command that neither zsh nor RTK can distort — command (single line):
      `git ls-files -- 'plans/done/*ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/courses/README.md'`
      — acceptance: three checks, all required. (a) It prints **exactly one** path — pipe it to
      `grep -c .` and read **1**. Its directory is `<SYLLABUS_ROOT>`. (b) `test -d "<SYLLABUS_ROOT>"`
      exits 0. (c) `git ls-files -- '<SYLLABUS_ROOT>/*.md' | grep -c .` returns **122**. Record the printed path
      to `evidence/phase-0-snapshot.txt` as `SYLLABUS_ROOT=<path>` — every later authoring step reads
      from that recorded root, never from a copy.
      **Do not write this as `test -d plans/done/*__…/syllabus/courses || test -d plans/in-progress/…`.**
      This harness runs **zsh**, where an unmatched glob is a fatal error rather than a literal:
      whenever the referenced plan is still in-progress (as plan 02 was when this check was
      authored; it is now archived), the `plans/done/*__…` pattern matches nothing, zsh aborts the
      whole command line with `no matches found`, and the `||` fallback **never runs** — a false red
      in the single most likely state at authoring time. Were the glob instead to match two archived
      copies, `test -d` would
      receive two arguments and exit **2** (`too many arguments`). Both measured on this machine
      2026-07-22. **`find` is also the wrong instrument for this particular check** — not because a
      piped `find … | wc -l` miscounts (it does not; see the bare-versus-piped rule in the previous
      step), but because locating a stage-ambiguous path needs a pathspec that `git ls-files` expands
      itself, and because the **bare** form of `find` — the one an executor is most likely to run
      interactively while debugging this step — is rewritten to `rtk find`, which reformats the result
      and drops flags it does not know. An explicit `rtk find` on this very query printed the single
      **stdout** line `0 for '<pattern>'` for the nothing-landed case, which `| grep -c .` reads as
      **1** — the exact inversion of the answer, and the reason `find` is not used here.
      `ls … | wc -l` is unreliable for the same family of reasons (see this file's Phase 0 preamble).
      `git ls-files` is unfiltered and expands its own quoted patterns, so neither zsh nor RTK ever
      sees the `*`.
      [Repo-grounded — measured 2026-07-22, each command issued alone as the whole content of one call:
      `rtk find … -path '<pattern>'` wrote `0 for '<root>'` to stdout and **nothing to stderr**, so
      both the stdout-only and the `2>&1`-merged forms of `| grep -c .` read **1**. An earlier revision
      of this passage claimed `-path` emits `rtk find: unknown flag '-path', ignored` on stderr, that
      the merged form therefore reads **2**, and that the dropped flag makes `rtk find` "list the search
      roots wholesale" — **none of those three reproduced**. They appear to have been generalised from
      `-mindepth`, which genuinely does emit that warning. The inversion-to-**1** point, which is what
      actually justifies avoiding `find` here, is unaffected.]
      Falsifiable both ways: before plan 02 lands in either stage the `git ls-files` locate step
      matches no path and check (a) reads **0** (`grep -c` also exits 1 on a zero count — read the
      printed number, never `&&`-chain it); **2** means the corpus was archived twice and the root is ambiguous; and a
      folder that exists but whose `syllabus/courses/` holds a count other than 122 fails check (c).
- [ ] [AI] Establish content baselines: `npx nx run ayokoding-www:build` and
      `npx nx run ayokoding-www:test:unit`
      — acceptance: both exit 0; record pass state in `evidence/phase-0-snapshot.txt`.
- [ ] [AI] **Confirm all twenty-nine NEW slugs are absent (no collision)** under `<SE_OLD>` and
      `<COURSES>` (six net-new AI-engineering courses + fourteen new courses + nine new capstones:
      three original plus six **DD-20** inter-topic capstones):

  ```bash
  for s in evaluating-ai-output-essentials evaluating-ai-systems-in-depth statistics-for-evaluation \
    product-patterns-for-probabilistic-systems inference-serving-and-model-deployment \
    fine-tuning-and-adaptation \
    coding-interview take-home-and-live-coding system-design-interview \
    behavioral-and-leadership-interviews capstone-interview-loop \
    async-python-and-fastapi-services self-hosting-essentials browser-automation-with-cdp \
    the-agent-loop agent-tools-and-mcp agent-context-and-memory \
    agent-permissions-and-sandboxing agent-orchestration-subagents-and-observability \
    capstone-build-your-own-coding-agent just-enough-cpp \
    detection-engineering-and-siem-operations capstone-build-your-own-pentest-engine \
    capstone-real-world-delivery capstone-secure-service capstone-data-pipeline \
    capstone-concurrency-and-systems capstone-concurrency-showdown capstone-lead-at-altitude; do
    test -e "apps/ayokoding-www/content/en/learn/fundamentally-strong/software-engineer/$s" && echo "EXISTS SE_OLD $s"
    test -e "apps/ayokoding-www/content/en/learn/courses/$s" && echo "EXISTS COURSES $s"
  done
  ```

  — acceptance: **zero** output lines. Falsifiable both ways: `mkdir -p apps/ayokoding-www/content/en/learn/courses/just-enough-cpp`
  makes the loop print `EXISTS COURSES just-enough-cpp`, proving the check fires.

- [ ] [AI] **Create the authored-body slug register** — write the 90 slugs this plan authors, one per
      line, to `evidence/authored-body-slugs.txt` (6 AI + Bands 1–9), transcribed from this
      checklist's own phase sections:

  ```bash
  cat > evidence/authored-body-slugs.txt <<'EOF'
  evaluating-ai-output-essentials
  evaluating-ai-systems-in-depth
  statistics-for-evaluation
  product-patterns-for-probabilistic-systems
  inference-serving-and-model-deployment
  fine-tuning-and-adaptation
  nosql-databases
  graph-databases
  database-internals-and-storage-engines
  data-engineering
  search-and-information-retrieval
  api-design
  advanced-frontend
  backend-at-scale
  async-python-and-fastapi-services
  self-hosting-essentials
  containers-and-orchestration
  cloud-and-iac
  cicd-and-release-engineering
  build-automation-and-task-runners
  information-architecture-and-seo
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
  software-architecture
  domain-driven-design
  system-design
  event-driven-architecture
  distributed-systems
  build-your-own-web-framework
  build-your-own-reactive-ui
  creating-ai-powered-apps
  agentic-ai
  browser-automation-with-cdp
  the-agent-loop
  agent-tools-and-mcp
  agent-context-and-memory
  agent-permissions-and-sandboxing
  agent-orchestration-subagents-and-observability
  just-enough-c
  just-enough-cpp
  linux-os
  windows-os
  system-programming
  just-enough-rust
  modern-system-programming
  just-enough-java
  enterprise-java-and-the-jvm
  lisp
  just-enough-fsharp
  type-systems
  compilers-parsers-and-transpilers
  build-your-own-git
  build-your-own-database
  build-your-own-raft
  it-and-application-security
  offensive-security
  defensive-security
  detection-engineering-and-siem-operations
  vulnerability-management-and-assessment
  it-governance-grc
  bare-metal-virtualization
  self-managed-kubernetes-and-gitops
  platform-engineering-and-devex
  site-reliability-engineering
  analytics-and-experimentation
  capstone-build-your-own-coding-agent
  capstone-build-your-own-pentest-engine
  capstone-real-world-delivery
  capstone-secure-service
  capstone-data-pipeline
  capstone-concurrency-and-systems
  capstone-concurrency-showdown
  capstone-lead-at-altitude
  coding-interview
  take-home-and-live-coding
  system-design-interview
  behavioral-and-leadership-interviews
  capstone-interview-loop
  EOF
  ```

  — acceptance: `wc -l < evidence/authored-body-slugs.txt` returns **90**, and
  `sort evidence/authored-body-slugs.txt | uniq -d | wc -l` returns **0** (no duplicate slug).
  Falsifiable both ways: deleting one line makes the first check return 89; duplicating one makes
  the second return 1.

- [ ] [AI] **Record the authored-body baseline (the falsifiable-both-ways anchor for archival)** —
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done < evidence/authored-body-slugs.txt | wc -l`
      — acceptance: returns **90** today (none authored yet) and is recorded in
      `evidence/phase-0-snapshot.txt`. The same command must return **0** at archival (Phase 16). This
      is this plan's own assertion; the 127-course catalog total is asserted by
      `ayokoding-learning-path-05-manifests`, never here.
- [ ] [AI] Confirm `learnings.md` exists in the plan folder with its H1 — command:
      `test -f learnings.md && head -1 learnings.md` — acceptance: file present and the first line is
      `# Learnings: ayokoding-learning-path-04-course-authoring`.
- [ ] [AI] **Cross-plan link gate (BF-8)** — confirm every `../ayokoding-learning-path-*` reference
      in this plan's own files resolves:

  ```bash
  cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate \
    --quiet \
    --exclude plans/done \
    --exclude apps/ayokoding-www/content \
    --exclude apps/ose-www/content 2>&1 | grep -F "ayokoding-learning-path-04-course-authoring"
  ```

  — acceptance: the `grep` finds **no** matching line (exits 1). Falsifiable both ways: adding one
  bad `../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/nope.md` link makes the
  same command print that file and exit 0. `md links validate` accepts **no positional path**
  (passing one errors out) and the bare repo-wide form is unsatisfiable (a pre-existing, non-zero
  backlog of broken links, nearly all under `plans/done/`, unrelated to this work — 137 of 138
  repo-wide as of 2026-07-22) — use this exact form.

- [ ] [AI] **Confirm no manifest file changed in this phase** — this phase only writes
      `evidence/` toolchain-baseline files, and it opens **no** PR (the Delivery-Boundary Integration
      Protocol applies from Phase 1 onward), but the manifest-isolation assertion still holds here:
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**. Falsifiable both ways: touching any file under that path makes the
      command return ≥1 and the phase gate fails.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [ ] [AI] `npm install` exited 0 and `npm run doctor -- --fix` reports no unresolved drift.
- [ ] [AI] Both blocking plans verified merged: `<COURSES>` holds exactly 37 re-homed bundles; the
      cross-plan `syllabus/courses/` holds 122 entries and its root is recorded as `SYLLABUS_ROOT`.
- [ ] [AI] `ayokoding-www:build` + `test:unit` baselines recorded green.
- [ ] [AI] All 29 new slugs confirmed absent (zero `EXISTS` lines).
- [ ] [AI] `evidence/authored-body-slugs.txt` holds 90 unique slugs; the ABSENT-count baseline of 90 is
      recorded in `evidence/phase-0-snapshot.txt`.
- [ ] [AI] Cross-plan link gate green (no line naming this plan's folder).
- [ ] [AI] Zero manifest files touched (`git diff --name-only ... | grep -c .` returns 0).
- [ ] [AI] **No PR was opened for this phase and nothing was pushed** — the Delivery-Boundary Integration
      Protocol applies from **Phase 1 onward** and explicitly excludes Phase 0. Read the printed
      number from each (never `&&`-chained, since `grep -c` exits 1 on a zero count):
      `git ls-remote --heads origin "$(git branch --show-current)" | grep -c .` returns **0**, and
      `gh pr list --head "$(git branch --show-current)" --json number --jq 'length'` returns **0**.
      Falsifiable both ways: pushing this branch makes the first return **1**; opening a PR for it
      makes the second return **1** — either fails the gate. The `evidence/` baseline and slug
      register written here ride the **Phase 1** PR
      ([§Phase 0 Opens No PR](../../../repo-governance/conventions/structure/plans.md#phase-0-opens-no-pr--the-earliest-pr-is-phase-1-hard-rule)).

> **Pause Safety**: only the toolchain, the two upstream preconditions, and the slug register were
> established — no course body exists yet, nothing is pushed, and no PR exists. Safe to stop
> indefinitely. To resume: re-run the two blocking-plan verification commands and the baseline build.

---

## Phase 1: Author the six net-new AI-engineering courses

> Each NEW course is authored as a full page-bundle into `<COURSES><course-id>/`. These six bodies are
> content-independent (each writes only its own subtree) and **pipeline concurrently** through review
> (bounded by the cap). Per-course concept/example/prerequisite/capstone detail is **already settled**
> in the cross-plan
> [`syllabus/courses/`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/courses/README.md) —
> each of the six has a complete 295–425-line spec file with concrete `co-NN` concept enumeration,
> `ex-NN` worked examples, a concrete prerequisite chain, and a capstone spec. **Author each course
> body from its `$SYLLABUS_ROOT/<id>.md` spec, not from a fresh judgment call.**
>
> Every course is split into a **stable spine** and **dated accuracy-note sidebars** (volatile
> SDK/model/pricing/framework specifics), matching the pattern the existing AI-band courses use
> (DD-28's durability constraint) — an explicit authoring requirement, not optional polish.

### NEW-course authoring convention (applies to every authoring step in Phases 1 and 3–11)

1. [AI] **V (accuracy pre-verify)** — spot-check version-pinned / market / pre-1.0-stack facts via
   `web-researcher` — acceptance: no version-pinned claim written `[Unverified]`; every volatile fact
   sits in a dated accuracy-note sidebar, not the stable spine.
2. [AI] **Skeleton** — create `<COURSES><course-id>/` (`_index.md` with `prerequisites: [...]` +
   `overview.md` + `learning/_index.md` + `drilling/_index.md`), mirroring the sibling bundle shape;
   the `course-id` slug and the prerequisite chain are **settled** — use the exact values declared in
   `$SYLLABUS_ROOT/<course-id>.md`, not a fresh decision — acceptance: `test -d "<COURSES><course-id>"`,
   `test -d "<COURSES><course-id>/learning"`, and `test -d "<COURSES><course-id>/drilling"` all exit 0,
   and `grep -F -q 'prerequisites:' "<COURSES><course-id>/_index.md"` exits 0.
3. [AI] **Author learning track** — `overview.md` (purpose + `## Prerequisites` naming only earlier
   library courses + register per `prd.md`), concept coverage, example/scenario pages + colocated
   `code/` where code-bearing, and `learning/capstone/`; the concept-coverage floor and example volume
   are **settled** in the spec's `co-NN`/`ex-NN` enumeration — acceptance: the course's own
   `overview.md` states its scope boundary against any sibling course it could be confused with.
4. [AI] **Author drilling track** — `drilling/<course-id>.md` + `drilling/overview.md` in the fixed
   five-section order — acceptance: all five sections present.
5. [AI] **Run content checkers** — the matching learning checker, `apps-ayokoding-www-facts-checker`,
   and `apps-ayokoding-www-link-checker` (plus `apps-ayokoding-www-general-checker` on
   `drilling/overview.md`) — acceptance: findings recorded. _(Content authoring is a
   maker-checker-fixer cycle, not code TDD — no RED/GREEN/REFACTOR labels; see steps 6–7 and
   [tech-docs §TDD exemption](./tech-docs.md#tdd-exemption-this-plan-ships-no-application-code).)_
6. [AI] **Apply content fixers** — resolve every CRITICAL/HIGH/MEDIUM finding via the matching fixer —
   acceptance: every finding addressed.
7. [AI] **Re-verify** — re-run checkers + `npx nx run ayokoding-www:build` + `npm run lint:md` —
   acceptance: zero CRITICAL/HIGH/MEDIUM remain; build + lint exit 0.
8. [AI] **Confirm no manifest file changed in this course's own diff** — the per-band and per-phase
   manifest checks elsewhere in this file each branch fresh from `origin/main` and so can only see
   their own diff, never an already-merged sub-phase's diff (same reasoning as every other individual
   check in this file); this course's own sub-phase branch needs its own check for the same reason:
   `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
   — acceptance: returns **0** on this course's own branch before it merges. Falsifiable both ways:
   touching any file under that path makes the command return ≥1.
9. [AI] **Licensing self-check (programme
   [`A8`](./tech-docs.md#programme-decisions))** — grep this course's
   own worked-example code for the CC-BY-SA Stack Overflow hazard `A8` names explicitly:
   `grep -rn 'stackoverflow\.com\|reddit\.com' "<COURSES><course-id>/learning/code/" 2>/dev/null | grep -c .`
   — acceptance: prints `0` (a zero-count `grep -c` exits 1 under every grep engine this harness may
   use — do not chain with `&&`; read the printed output). Falsifiable both ways: pasting an SO/Reddit URL into any file under that directory makes
   the count ≥1 today, before this step is satisfied. This is a targeted heuristic, not a full
   copyright audit — the maker-checker-fixer content checkers (step 5) and the human author's own
   judgment remain the primary `A8` control for prose, figures, and structure.

Each course below is its own sub-phase (own branch → draft PR → 3-cycle review → `[AI]` merge →
deploy), applying the convention:

- [ ] [AI] Light eval gate (`evaluating-ai-output-essentials` — Annotated-concept, Python, settled per
      `$SYLLABUS_ROOT/evaluating-ai-output-essentials.md`, 295 lines) — sits right after the first
      working LLM call, before RAG/agents; answers "how will you know this works?" (DD-25) —
      acceptance: all 9 convention steps complete; checkers report zero CRITICAL/HIGH/MEDIUM;
      `grep -F -q 'evaluating-ai-systems-in-depth' "<COURSES>evaluating-ai-output-essentials/overview.md"`
      exits 0 (the scope boundary against the deep-evals course is stated). Falsifiable both ways: the
      same command exits **2** today, because `overview.md` does not exist yet: `grep` exits 2 on a
      missing path and 1 only on a genuine no-match (measured 2026-07-22, and true under both the ugrep
      and BSD `grep` engines this harness may route to) — the two are never the same observation; and once the file exists it exits **1** if the boundary line is
      dropped. Only exit 0 satisfies this clause, so either failure mode fails it.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] Statistics for evals (`statistics-for-evaluation` — Annotated-concept, code-bearing, Python,
      settled per `$SYLLABUS_ROOT/statistics-for-evaluation.md`, 368 lines) — scoped tightly to what
      evals demand (judge concordance, significance testing), not a general statistics survey (DD-26);
      it is a **hard prerequisite** of `evaluating-ai-systems-in-depth`, so it is authored before (or
      in the same review cycle as) the deep-evals course — acceptance: all 9 convention steps complete;
      checkers report zero CRITICAL/HIGH/MEDIUM;
      `grep -F -q 'analytics-and-experimentation' "<COURSES>statistics-for-evaluation/overview.md"`
      exits 0 (the scope boundary against classical A/B testing is stated).

  **Gherkin (binds) →** "The statistics-for-evals course stays scoped to what evals demand"

  ```gherkin
  Scenario: The statistics-for-evals course stays scoped to what evals demand
    Given the statistics-for-evals course is authored
    When a reader compares it with analytics-and-experimentation
    Then it covers judge concordance and significance testing for evals only
    And it does not re-teach general product A/B testing, which stays analytics-and-experimentation's scope
  ```

  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_

- [ ] [AI] Deep evals (`evaluating-ai-systems-in-depth` — By Example, Python, settled per
      `$SYLLABUS_ROOT/evaluating-ai-systems-in-depth.md`, 384 lines) — sits after agents; error
      analysis, task-specific criteria, LLM-as-judge with measured human agreement, CI gating,
      judge-scope reliability (DD-25); declares `statistics-for-evaluation` a **hard prerequisite** —
      acceptance: all 9 convention steps complete; checkers report zero CRITICAL/HIGH/MEDIUM;
      `grep -F -q 'statistics-for-evaluation' "<COURSES>evaluating-ai-systems-in-depth/_index.md"`
      exits 0 (the hard prerequisite is declared) **and**
      `grep -F -q 'evaluating-ai-output-essentials' "<COURSES>evaluating-ai-systems-in-depth/overview.md"`
      exits 0 (the scope boundary against the light gate is stated).

  **Gherkin (binds) →** "The light eval gate and deep evals course do not overlap"

  ```gherkin
  Scenario: The light eval gate and deep evals course do not overlap
    Given the light-eval-gate course and the deep-evals course are authored
    When a reader compares their overviews
    Then each overview states an explicit scope boundary against the other
    And neither course re-teaches the material the other owns
  ```

  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

- [ ] [AI] Product patterns for probabilistic systems (`product-patterns-for-probabilistic-systems` —
      Annotated-concept, no code, settled per
      `$SYLLABUS_ROOT/product-patterns-for-probabilistic-systems.md`, 370 lines) — product design
      patterns for probabilistic (not deterministic) outputs; no course owns this today (DD-28) —
      acceptance: all 9 convention steps complete; checkers report zero CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] Inference serving and model deployment (`inference-serving-and-model-deployment` — By
      Example, Python, settled per `$SYLLABUS_ROOT/inference-serving-and-model-deployment.md`, 405
      lines) — vLLM/TGI, KV-cache, batching, GPU considerations; entirely absent from the library today
      (DD-28) — acceptance: all 9 convention steps complete; checkers report zero CRITICAL/HIGH/MEDIUM;
      every vLLM/TGI version claim sits in a dated accuracy-note sidebar, verified by the facts checker.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Fine-tuning and adaptation (`fine-tuning-and-adaptation` — By Example, Python, settled per
      `$SYLLABUS_ROOT/fine-tuning-and-adaptation.md`, 423 lines) — fine-tuning/LoRA/PEFT versus RAG as
      a foil (DD-28) — acceptance: all 9 convention steps complete; checkers report zero
      CRITICAL/HIGH/MEDIUM.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] **Add catalog rows** — replace the "per its settled spec" prerequisite cells in
      [tech-docs §AI-engineering specialization](./tech-docs.md#ai-engineering-specialization-the-fourth-paths-six-net-new-courses)
      with the chains transcribed from each course's `_index.md`, and add all six course IDs to
      `<COURSES>_index.md` — acceptance:
      `for s in evaluating-ai-output-essentials evaluating-ai-systems-in-depth statistics-for-evaluation product-patterns-for-probabilistic-systems inference-serving-and-model-deployment fine-tuning-and-adaptation; do grep -F -q "$s" apps/ayokoding-www/content/en/learn/courses/_index.md || echo "MISSING $s"; done | wc -l`
      returns **0** (returns 6 before this step); `apps-ayokoding-www-link-checker` green on
      `<COURSES>_index.md`.
- [ ] [AI] **Record the band-completion signal** for the AI-engineering set in this file (see
      [README §Band-completion signal contract](./README.md#band-completion-signal-contract)) — all
      five fields present: `BAND`, `PLAN`, `LANDED_COURSE_IDS` (the six IDs), `GROW_MANIFESTS`
      (`<MANIFESTS>careers/immediately-effective/ai-engineer.yaml` — the AI path only),
      `MERGED_COMMIT` — acceptance: the signal block is present in this file with all five fields
      populated and `MERGED_COMMIT` a real 40-char SHA on `origin/main`
      (`git cat-file -e <sha>^{commit}` exits 0). Falsifiable both ways: a placeholder SHA fails
      `git cat-file -e`.
- [ ] [AI] **Confirm no manifest file changed in this phase** — this phase authors six course bodies
      via the same mechanism Bands 1–9 use, so it gets the identical individual gate every band
      already carries via its own "per-band closing steps" step 3:
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**. Falsifiable both ways: touching any file under that path makes the
      command return ≥1 and the phase gate fails.

### Phase 1 Gate

- [ ] [AI] All six AI courses live under `<COURSES>` with declared prerequisites; each passed its
      checker + facts + link checkers; each states its scope boundary against any course it could be
      confused with.
- [ ] [AI] Every course's volatile facts sit in dated accuracy-note sidebars, not the stable spine
      (DD-28 durability constraint) — verified by `apps-ayokoding-www-facts-checker`.
- [ ] [AI] `evaluating-ai-systems-in-depth/_index.md` declares `statistics-for-evaluation` as a
      prerequisite (`grep -F -q` exits 0).
- [ ] [AI] Six catalog rows completed in `tech-docs.md`; `<COURSES>_index.md` lists all six
      (the MISSING loop returns 0).
- [ ] [AI] `npx nx run ayokoding-www:build` + `npm run lint:md` +
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md heading-hierarchy validate`
      all exit 0.
- [ ] [AI] Band-completion signal recorded with all five fields; `MERGED_COMMIT` verified real.
- [ ] [AI] Zero manifest files touched (`git diff --name-only ... | grep -c .` returns 0).
- [ ] [AI] Every course sub-phase PR is `[AI]`-merged and deployed.

> **Pause Safety**: the library holds the 37 re-homed bundles plus six new AI courses, all at canonical
> URLs and all rendering. No manifest references them yet, so nothing downstream can break. Safe to
> stop. To resume: re-run the section build + link validation.

---

## Phase 2: Course-surgery contracts — evals scope, D9 naming/citation, D11 concept additions

> **Sequencing note (inherited, not invented here):** the evals donor courses
> (`creating-ai-powered-apps`, `agentic-ai`, `agent-orchestration-subagents-and-observability`) and the
> D9/D11 target courses (the harness cluster plus `capstone-build-your-own-coding-agent`) are **not yet
> authored anywhere** at this point in the build order — they are native-authored in Phase 7 (Band 5)
> and Phase 10 (Band 8). DD-28's "trim the three donors to forward-links" therefore cannot be a
> file-edit action here; there is nothing yet to edit. This phase **locks the contract** those future
> authoring steps must honor and **bakes its acceptance criteria into Bands 5 and 8**, so the surgery is
> applied **by construction** rather than retrofitted across six bodies afterwards.
>
> **Manifest boundary.** The source plan closed this phase by re-running manifest integrity across
> every published manifest. That step **is not here** — it inverts the wave order (this plan is Wave 2;
> no manifest exists until Wave 3) and it is manifest-plan property either way. See
> [README §The manifest ownership invariant](./README.md#the-manifest-ownership-invariant-binding--read-before-anything-else),
> whose table lists every step that left this plan for the manifest plan.

- [ ] [AI] **State the four-path blast radius (DD-28 binding rule)** — for the evals extraction, the D9
      naming/citation additions, and the D11 concept additions, name every course and every manifest
      each touches: the evals extraction touches `evaluating-ai-systems-in-depth` (Phase 1, done) plus
      the three not-yet-authored donor courses (Band 5), and the `fundamentally-strong` and
      `immediately-effective` manifests that will carry those donors once grown (the AI path's manifest
      already carries the deep-evals course from its own plan's smoke-test spine); the D9/D11 additions
      touch only the harness cluster (Band 5) + `capstone-build-your-own-coding-agent` (Band 8) and
      every manifest carrying those IDs — the same two software-engineer-role manifests plus the fourth
      path's manifest once Bands 5/8 grow it to include the harness cluster (DD-33) — acceptance: the
      blast radius is written into this checklist (the two clauses above) before any of the three
      surgeries is considered "applied". **Naming a manifest is not editing one** — the growth is
      performed by `ayokoding-learning-path-05-manifests`.
- [ ] [AI] **Lock the evals forward-link contract** — record, for Band 5's authoring of
      `creating-ai-powered-apps`, `agentic-ai`, and `agent-orchestration-subagents-and-observability`,
      that each course's evals-adjacent material MUST forward-link to `evaluating-ai-systems-in-depth`
      rather than re-teaching it, in the style of the AI-band scope-guard (DD-11) — acceptance: this
      requirement appears verbatim as an acceptance criterion on each of the three courses' Band 5
      checklist items (verify by reading Phase 7 below), and
      `grep -F -q 'evaluating-ai-systems-in-depth' "<COURSES>creating-ai-powered-apps/overview.md"`
      exits **2** today (that course does not exist yet, and `grep` exits 2 on a missing path — 1 is
      reserved for a genuine no-match against a file that _does_ exist, per the rule stated at the
      light-eval gate in Phase 3) and must exit **0** once Band 5 lands it. The intermediate **1** is
      reachable only in the window where `overview.md` exists but omits the boundary line — which is
      itself a real failure state, so all three exit codes are distinguishable here.
      [Repo-grounded — measured 2026-07-22: the exact command above exited **2** with
      `No such file or directory`. An earlier revision claimed 1, contradicting this file's own
      correctly-measured rule.]
- [ ] [AI] **Lock the D9 naming/citation contract** — record, for Band 5's authoring of
      `agent-context-and-memory`, that it MUST include a context-engineering naming/lineage line citing
      Lütke (2025-06-19), Karpathy (2025-06-25), Willison (2025-06-27), and Anthropic's Effective
      Context Engineering methodology; and for the harness cluster (Band 5) plus
      `capstone-build-your-own-coding-agent` (Band 8), that they MUST include the harness-engineering
      equivalent citing Anthropic (2025-11-26) and Böckeler/Thoughtworks (2026-02-17) — **no course is
      renamed** (D9 is explicit: "harness engineering" is unsettled terminology; cite the disagreement,
      do not resolve it or adopt a side as structure) — acceptance: these citation requirements appear
      as explicit acceptance criteria on the relevant Band 5 and Band 8 items below.
      **Citation caveat carried forward**: the "OpenAI" attribution in the inherited D9 text is
      `[Unverified]`. A candidate OpenAI publication exists at
      `https://openai.com/index/harness-engineering/` ("Harness engineering: leveraging Codex in an
      agent-first world," reported 2026-02-11), but the primary page returned **HTTP 403** and was not
      read at verification time (2026-07-22) — the date/content rest on third-party summaries only, so
      this stays `[Unverified]` pending a primary-source read (do not upgrade to fact). The reported
      date is **early 2026**, later than the "late 2025" framing; that onset is therefore conditional on
      the OpenAI lead. Band 5/8 authoring cites Anthropic and Böckeler only, and omits the OpenAI
      attribution unless the primary page is read and a specific URL confirmed.
- [ ] [AI] **Lock the D11 concept-addition contract** — record, for Band 5's authoring, the four
      concept-level additions: cache-aware prefix ordering (framed as a general stable-before-variable
      principle, not tied to one vendor's mechanism) → `agent-context-and-memory`; tool-count
      degradation **and** tool-result token efficiency → `agent-tools-and-mcp`; train-vs-production
      permission asymmetry (framed as a risk distinction, not a capability distinction) →
      `agent-permissions-and-sandboxing` — acceptance: each concept appears as an explicit acceptance
      criterion on the relevant Band 5 item below, naming the concept and its target course.
- [ ] [AI] **Confirm no manifest file changed in this phase** —
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**. Falsifiable both ways: touching any file under that path makes the
      command return ≥1 and the phase gate fails.

### Phase 2 Gate

- [ ] [AI] Four-path blast radius stated for all three surgeries; forward-link, citation, and
      concept-addition contracts locked as explicit Band 5 / Band 8 acceptance criteria.
- [ ] [AI] "Harness engineering" is cited, not adopted as structure — no course renamed (D9); the
      unverified OpenAI attribution is excluded.
- [ ] [AI] Zero manifest files touched (`git diff --name-only ... | grep -c .` returns 0).
- [ ] [AI] **No PR opens for this phase** — Phase 2 is intermediate (see the
      [`### Delivery Boundaries`](#delivery-boundaries) table): the contract-lock edits are committed
      on the shared worktree, this phase's own gate above is green, and nothing is pushed for review
      yet — the edits ride the first Band-5 course PR (`software-architecture`, Phase 7) rather than
      opening a standalone PR of their own.

> **Pause Safety**: the evals/D9/D11 contracts are locked and will be enforced when Band 5 and Band 8
> author their target courses; no app content changed. Safe to stop. To resume: re-read this phase's
> four bullets and confirm Phases 7 and 10 still carry the matching acceptance criteria.

---

## Phases 3–11: Author the 84 native bodies, band by band

Every body is authored NATIVE into `<COURSES><course-id>/` (no legacy home, no re-home) per the
**NEW-course authoring convention** in Phase 1. Bodies within a band are content-independent and
**pipeline concurrently** through review, bounded by the cap. Per-course detail:
`$SYLLABUS_ROOT/<course-id>.md` and the tracked
[Course Library Catalog](./tech-docs.md#course-library-catalog). Each band authors its own catalog
rows as part of "convention complete".

**Reconciliation rulings baked into authoring** (locked):

- `defensive-security` is **By-Example hands-on** (Sigma/ELK/OpenSearch + IR + hardening) — author it
  that way; the catalog's original "(concept)" label was WRONG and is corrected (DD-12).
  `detection-engineering-and-siem-operations` owns the deep Wazuh decoder/rule/FP-tuning/dashboard
  tier and declares `defensive-security` a prerequisite; draw the scope line explicitly in both.
- **AI-band scope-guard** (DD-11): `creating-ai-powered-apps` (use-an-LLM-in-an-app) → `agentic-ai` (a
  single survey that **forward-links each primitive to its harness-cluster course** and does NOT
  re-teach at build-your-own depth) → the 5-course harness cluster (build-your-own depth). Bake the
  cross-reference contract in.
- `async-python-and-fastapi-services` stays framework-concrete: defer async _concepts_ to
  `concurrency-and-parallelism` and framework _internals_ to `build-your-own-web-framework`;
  cross-link both.

**Per-band closing steps** (identical for every band; listed once, applied in each phase's gate):

1. [AI] Add each landed course's row to
   [tech-docs §Course Library Catalog](./tech-docs.md#course-library-catalog) and its ID to
   `<COURSES>_index.md`.
2. [AI] Record the band-completion signal in this file with all five fields (`BAND`, `PLAN`,
   `LANDED_COURSE_IDS`, `GROW_MANIFESTS`, `MERGED_COMMIT`) per
   [README §Band-completion signal contract](./README.md#band-completion-signal-contract).
3. [AI] Confirm zero manifest files were touched:
   `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
   returns **0**.

---

## Phase 3: Band 1 — Data depth (5 bodies)

- [ ] [AI] `nosql-databases` (By Example · Python) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `graph-databases` (By Example · Cypher + Python) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `database-internals-and-storage-engines` (By Example · Python) — convention complete;
      checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `data-engineering` (Annotated-concept · Python) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] `search-and-information-retrieval` (By Example · Python) — convention complete; checkers
      clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Apply the three per-band closing steps (catalog rows, band signal, zero-manifest check).
      `GROW_MANIFESTS` for this band = the three software-engineer-role manifests.

### Phase 3 Gate

- [ ] [AI] All 5 Band-1 bodies exist with declared prerequisites:
      `for s in nosql-databases graph-databases database-internals-and-storage-engines data-engineering search-and-information-retrieval; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done | wc -l`
      returns **0** (returns 5 before this phase).
- [ ] [AI] Every body passed its learning checker + facts checker + link checker with zero
      CRITICAL/HIGH/MEDIUM.
- [ ] [AI] `npx nx run ayokoding-www:build` + `npm run lint:md` exit 0.
- [ ] [AI] Catalog rows added; `<COURSES>_index.md` lists all 5; band signal recorded with all five
      fields; zero manifest files touched.
- [ ] [AI] Every sub-phase PR is `[AI]`-merged and deployed.

> **Pause Safety**: five self-contained data-depth bodies are live at canonical URLs; no manifest
> references them, so no path can break. Safe to stop. To resume: re-run the section build.

---

## Phase 4: Band 2 — Web, backend & platform productivity (10 bodies)

- [ ] [AI] `api-design` (By Example · Python) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `advanced-frontend` (By Example · TypeScript) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `backend-at-scale` (By Example · Python) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `async-python-and-fastapi-services` (By Example · Python) — convention complete; checkers
      clean; **framework-concrete scope note applied**: async concepts deferred to
      `concurrency-and-parallelism`, framework internals to `build-your-own-web-framework`, both
      cross-linked — acceptance:
      `grep -F -q 'concurrency-and-parallelism' "<COURSES>async-python-and-fastapi-services/overview.md"`
      exits 0 **and**
      `grep -F -q 'build-your-own-web-framework' "<COURSES>async-python-and-fastapi-services/overview.md"`
      exits 0.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `self-hosting-essentials` (By Example · ops/config) — convention complete; checkers clean —
      scope-boundary acceptance: the course teaches running one box, containerizing a service, a
      reverse proxy, and PaaS git-push deploy; its `overview.md` **explicitly excludes** clusters,
      Terraform/Packer/Ansible IaC, and Proxmox. Verify each exclusion is **stated** (not merely
      absent):
      `for w in cluster Terraform Packer Ansible Proxmox; do grep -F -q -i "$w" "<COURSES>self-hosting-essentials/overview.md" || echo "MISSING $w"; done | wc -l`
      returns **0**, and no lesson body under `<COURSES>self-hosting-essentials/learning/` teaches
      them. Falsifiable both ways: the loop returns 5 today (no such file) and returns ≥1 if any
      exclusion is dropped.

  **Gherkin (binds) →** "The light self-hosting course stays below clusters and IaC"

  ```gherkin
  Scenario: The light self-hosting course stays below clusters and IaC
    Given the self-hosting-essentials course is authored
    When a reader compares it with containers-and-orchestration and cloud-and-iac
    Then it teaches running one box, containerizing a service, a reverse proxy, and PaaS git-push deploy
    And its overview explicitly excludes clusters, Terraform/Packer/Ansible IaC, and Proxmox
  ```

  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

- [ ] [AI] `containers-and-orchestration` (By Example · YAML/CLI) — convention complete; checkers
      clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `cloud-and-iac` (Annotated-concept · HCL/YAML) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] `cicd-and-release-engineering` (By Example · YAML + Python) — convention complete; checkers
      clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `build-automation-and-task-runners` (By Example · multi-tool) — convention complete;
      checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `information-architecture-and-seo` (Annotated-concept · HTML) — convention complete;
      checkers clean.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] Apply the three per-band closing steps. `GROW_MANIFESTS` = the three software-engineer-role
      manifests.

### Phase 4 Gate

- [ ] [AI] All 10 Band-2 bodies exist:
      `for s in api-design advanced-frontend backend-at-scale async-python-and-fastapi-services self-hosting-essentials containers-and-orchestration cloud-and-iac cicd-and-release-engineering build-automation-and-task-runners information-architecture-and-seo; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done | wc -l`
      returns **0** (returns 10 before this phase).
- [ ] [AI] The `self-hosting-essentials` exclusion loop returns 0 and the
      `async-python-and-fastapi-services` two cross-links both exit 0.
- [ ] [AI] Every body passed its checkers with zero CRITICAL/HIGH/MEDIUM; build + `lint:md` exit 0.
- [ ] [AI] Catalog rows added; band signal recorded; zero manifest files touched.
- [ ] [AI] Every sub-phase PR is `[AI]`-merged and deployed.

> **Pause Safety**: the web/platform productivity band is live and self-contained. Safe to stop. To
> resume: re-run the section build.

---

## Phase 5: Band 3 — Mobile & desktop platforms (10 bodies)

- [ ] [AI] `just-enough-kotlin` (Primer · Kotlin) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_
- [ ] [AI] `android-app-development` (By Example · Kotlin) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `just-enough-swift` (Primer · Swift) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_
- [ ] [AI] `ios-app-development` (By Example · Swift) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `just-enough-dart` (Primer · Dart) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_
- [ ] [AI] `hybrid-app-development` (By Example · Dart) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `just-enough-csharp` (Primer · C#) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_
- [ ] [AI] `windows-app-development` (By Example · C#) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `linux-app-development` (By Example · Python) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `building-production-cli-tools` (By Example · Go + Rust) — convention complete; checkers
      clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Apply the three per-band closing steps. `GROW_MANIFESTS` = the three software-engineer-role
      manifests.

### Phase 5 Gate

- [ ] [AI] All 10 Band-3 bodies exist:
      `for s in just-enough-kotlin android-app-development just-enough-swift ios-app-development just-enough-dart hybrid-app-development just-enough-csharp windows-app-development linux-app-development building-production-cli-tools; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done | wc -l`
      returns **0** (returns 10 before this phase).
- [ ] [AI] Every primer passed `apps-ayokoding-www-primer-checker`; every By-Example body passed
      `apps-ayokoding-www-by-example-checker`; facts + link checkers clean.
- [ ] [AI] `npx nx run ayokoding-www:build` + `npm run lint:md` exit 0.
- [ ] [AI] Catalog rows added; band signal recorded; zero manifest files touched.
- [ ] [AI] Every sub-phase PR is `[AI]`-merged and deployed.

> **Pause Safety**: five primer/platform pairs are live; each `just-enough-*` primer resolves the
> prerequisite its paired platform course declares, so no dangling edge exists. Safe to stop. To
> resume: re-run the section build.

---

## Phase 6: Band 4 — Concurrency languages (4 bodies)

- [ ] [AI] `just-enough-go` (Primer · Go) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_
- [ ] [AI] `csp-style-concurrency` (By Example · Go) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `just-enough-elixir` (Primer · Elixir) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_
- [ ] [AI] `actor-model-concurrency` (By Example · Elixir) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Apply the three per-band closing steps. `GROW_MANIFESTS` = the three software-engineer-role
      manifests.

### Phase 6 Gate

- [ ] [AI] All 4 Band-4 bodies exist:
      `for s in just-enough-go csp-style-concurrency just-enough-elixir actor-model-concurrency; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done | wc -l`
      returns **0** (returns 4 before this phase).
- [ ] [AI] Both By-Example bodies declare `concurrency-and-parallelism` as a prerequisite:
      `for s in csp-style-concurrency actor-model-concurrency; do grep -F -q 'concurrency-and-parallelism' "apps/ayokoding-www/content/en/learn/courses/$s/_index.md" || echo "MISSING $s"; done | wc -l`
      returns **0**.
- [ ] [AI] Checkers clean; build + `lint:md` exit 0.
- [ ] [AI] Catalog rows added; band signal recorded; zero manifest files touched.
- [ ] [AI] Every sub-phase PR is `[AI]`-merged and deployed.

> **Pause Safety**: the two concurrency-paradigm tracks are live and complete; `Band 8`'s
> `capstone-concurrency-showdown` and `capstone-concurrency-and-systems` now have their prerequisite
> bodies present. Safe to stop. To resume: re-run the section build.

---

## Phase 7: Band 5 — Architecture, distributed & AI/harness (15 bodies)

> **This band applies the three contracts Phase 2 locked** (evals forward-link, D9 naming/citation,
> D11 concept additions), by construction. Each target course below carries the contract as an
> explicit acceptance criterion.

- [ ] [AI] `software-architecture` (Annotated-concept · Python) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] `domain-driven-design` (By Example · Python) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `system-design` (Annotated-concept · Python) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] `event-driven-architecture` (By Example · Python) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `distributed-systems` (By Example · Python) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `build-your-own-web-framework` (By Example · Python) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `build-your-own-reactive-ui` (By Example · TypeScript) — convention complete; checkers
      clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `creating-ai-powered-apps` (By Example · Python; use-an-LLM scope) — convention complete;
      checkers clean; **Phase 2 evals forward-link contract applied**:
      `grep -F -q 'evaluating-ai-systems-in-depth' "<COURSES>creating-ai-powered-apps/overview.md"`
      exits **0** (its evals material forward-links rather than re-teaching, DD-25/DD-28). Falsifiable
      both ways: exits 1 before this step and exits 1 again if the forward-link is removed.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `agentic-ai` (By Example · Python; survey + forward-links, no build-your-own depth) —
      convention complete; checkers clean; **Phase 2 evals forward-link contract applied**:
      `grep -F -q 'evaluating-ai-systems-in-depth' "<COURSES>agentic-ai/overview.md"` exits **0** —
      forward-link acceptance: `agentic-ai/overview.md` names and links **each** of the five
      harness-cluster courses:
      `for s in the-agent-loop agent-tools-and-mcp agent-context-and-memory agent-permissions-and-sandboxing agent-orchestration-subagents-and-observability; do grep -F -q "$s" "apps/ayokoding-www/content/en/learn/courses/agentic-ai/overview.md" || echo "MISSING $s"; done | wc -l`
      returns **0** (returns 5 before this step), and no lesson under `<COURSES>agentic-ai/learning/`
      builds a working agent-loop / tool / memory / permission / orchestration implementation — that
      depth stays in the cluster courses (DD-11).

  **Gherkin (binds) →** "The agentic-ai survey forward-links each primitive without re-teaching it"

  ```gherkin
  Scenario: The agentic-ai survey forward-links each primitive without re-teaching it
    Given the agentic-ai survey course and the five harness-cluster courses are authored
    When a reader reads the agentic-ai survey
    Then it previews the agent loop, tools/MCP, memory/context, and evals and forward-links each to its cluster course
    And it does not re-teach any primitive at build-your-own depth
  ```

  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

- [ ] [AI] `browser-automation-with-cdp` (By Example · Python/CDP) — convention complete; checkers
      clean; `remotebrowser` named only as an illustrative pickup, never a required dependency.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `the-agent-loop` (By Example · Python) — convention complete; checkers clean; **Phase 2 D9
      citation contract applied**: a harness-engineering naming/lineage line is present citing Anthropic
      (2025-11-26) and Böckeler/Thoughtworks (2026-02-17), presenting the containment dispute as
      unresolved — no rename. Acceptance:
      `for w in "harness engineering" "2025-11-26" "2026-02-17"; do grep -F -q -i "$w" "apps/ayokoding-www/content/en/learn/courses/the-agent-loop/overview.md" || echo "MISSING $w"; done | wc -l`
      returns **0**.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `agent-tools-and-mcp` (By Example · Python) — convention complete; checkers clean; **Phase 2
      D9 + D11 contracts applied**: the harness-engineering citation line is present, and concept
      coverage includes **tool-count degradation** (Berkeley Function-Calling Leaderboard + the
      GeoEngine 46-vs-19-tool evidence) **and** **tool-result token efficiency**. Acceptance:
      `for w in "harness engineering" "tool-count" "token efficiency"; do grep -F -q -i "$w" "apps/ayokoding-www/content/en/learn/courses/agent-tools-and-mcp/overview.md" || echo "MISSING $w"; done | wc -l`
      returns **0**.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `agent-context-and-memory` (Annotated-concept · Python) — convention complete; checkers
      clean; **Phase 2 D9 + D11 contracts applied**: a context-engineering naming/lineage line is
      present citing Lütke (2025-06-19), Karpathy (2025-06-25), Willison (2025-06-27), and Anthropic's
      Effective Context Engineering methodology; concept coverage includes **cache-aware prefix
      ordering**, framed as a general stable-before-variable principle, not tied to one vendor's
      mechanism. Acceptance:
      `for w in "context engineering" "2025-06-19" "2025-06-25" "2025-06-27" "prefix"; do grep -F -q -i "$w" "apps/ayokoding-www/content/en/learn/courses/agent-context-and-memory/overview.md" || echo "MISSING $w"; done | wc -l`
      returns **0**.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] `agent-permissions-and-sandboxing` (By Example · Python) — convention complete; checkers
      clean; **Phase 2 D11 contract applied**: concept coverage includes the **train-vs-production
      permission asymmetry**, framed as a risk distinction, not a capability distinction. Acceptance:
      `grep -F -q -i "permission asymmetry" "apps/ayokoding-www/content/en/learn/courses/agent-permissions-and-sandboxing/overview.md"`
      exits 0.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `agent-orchestration-subagents-and-observability` (Annotated-concept · Python) — convention
      complete; checkers clean; **Phase 2 evals forward-link contract applied**:
      `grep -F -q 'evaluating-ai-systems-in-depth' "<COURSES>agent-orchestration-subagents-and-observability/overview.md"`
      exits **0** — runnable-example acceptance: each of the five harness-cluster courses ships a
      runnable typed-Python worked example covering its slice of the loop / tools / memory /
      permissions / orchestration, and each names `remotebrowser`'s bundled MCP or CDP browser only as
      an illustrative pickup, never a required dependency (verified during each course's checker pass;
      the by-example / annotated-concept maker conventions already require runnable examples — this
      bind adds the remotebrowser-scope check).

  **Gherkin (binds) →** "The harness cluster builds a working agent from runnable code"

  ```gherkin
  Scenario: The harness cluster builds a working agent from runnable code
    Given the five harness-engineering courses are authored
    When a reader builds an agent from them
    Then the agent loop, tools/MCP, memory, permissions, and orchestration each ship runnable typed-Python examples
    And each course names remotebrowser's bundled MCP or CDP browser only as an illustrative pickup
  ```

  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_

- [ ] [AI] Apply the three per-band closing steps. `GROW_MANIFESTS` for this band = the three
      software-engineer-role manifests **plus**
      `<MANIFESTS>careers/immediately-effective/ai-engineer.yaml` (DD-33 — this band lands
      eight of the nine courses that manifest walks). Name all four paths explicitly in the signal; a
      signal that omits the AI path leaves it stuck on its six-course smoke-test spine.

### Phase 7 Gate

- [ ] [AI] All 15 Band-5 bodies exist:
      `for s in software-architecture domain-driven-design system-design event-driven-architecture distributed-systems build-your-own-web-framework build-your-own-reactive-ui creating-ai-powered-apps agentic-ai browser-automation-with-cdp the-agent-loop agent-tools-and-mcp agent-context-and-memory agent-permissions-and-sandboxing agent-orchestration-subagents-and-observability; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done | wc -l`
      returns **0** (returns 15 before this phase).
- [ ] [AI] All three Phase-2 contracts verified applied: the three evals donors each forward-link
      (`grep -F -q` exits 0 for each); the D9 citation loops return 0 for `the-agent-loop`,
      `agent-tools-and-mcp`, and `agent-context-and-memory`; the D11 concept checks return 0 for
      `agent-tools-and-mcp`, `agent-context-and-memory`, and `agent-permissions-and-sandboxing`.
- [ ] [AI] `agentic-ai`'s five-forward-link loop returns 0 and no `agentic-ai` lesson implements a
      cluster primitive at build-your-own depth (DD-11 scope-guard held).
- [ ] [AI] Checkers clean across all 15; build + `lint:md` exit 0.
- [ ] [AI] Catalog rows added; band signal recorded naming **four** manifests; zero manifest files
      touched by this plan.
- [ ] [AI] Every sub-phase PR is `[AI]`-merged and deployed.

> **Pause Safety**: the architecture band and the complete AI/harness cluster are live; the three
> course surgeries are applied by construction rather than pending as retrofits. Safe to stop. To
> resume: re-run the section build and re-verify the three contract loops.

---

## Phase 8: Band 6 — Low-level systems, JVM & languages, internals builds (16 bodies)

- [ ] [AI] `just-enough-c` (Primer · C) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_
- [ ] [AI] `just-enough-cpp` (Primer · C++; declares `just-enough-c` a prerequisite) — convention
      complete; checkers clean — acceptance:
      `grep -F -q 'just-enough-c' "apps/ayokoding-www/content/en/learn/courses/just-enough-cpp/_index.md"`
      exits 0.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_
- [ ] [AI] `linux-os` (By Example · C + shell) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `windows-os` (By Example · C + PowerShell) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `system-programming` (By Example · C) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `just-enough-rust` (Primer · Rust) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_
- [ ] [AI] `modern-system-programming` (By Example · Rust) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `just-enough-java` (Primer · Java) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_
- [ ] [AI] `enterprise-java-and-the-jvm` (By Example · Java) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `lisp` (By Example · Scheme + Clojure) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `just-enough-fsharp` (Primer · F#) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-primer-maker`_
- [ ] [AI] `type-systems` (By Example · OCaml + Haskell + F#) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `compilers-parsers-and-transpilers` (By Example · F#) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `build-your-own-git` (By Example · Python) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `build-your-own-database` (By Example · Python) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `build-your-own-raft` (By Example · Go) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Apply the three per-band closing steps. `GROW_MANIFESTS` = the three software-engineer-role
      manifests.

### Phase 8 Gate

- [ ] [AI] All 16 Band-6 bodies exist:
      `for s in just-enough-c just-enough-cpp linux-os windows-os system-programming just-enough-rust modern-system-programming just-enough-java enterprise-java-and-the-jvm lisp just-enough-fsharp type-systems compilers-parsers-and-transpilers build-your-own-git build-your-own-database build-your-own-raft; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done | wc -l`
      returns **0** (returns 16 before this phase).
- [ ] [AI] `just-enough-cpp` declares `just-enough-c` as its prerequisite (DD-14's dedicated on-ramp).
- [ ] [AI] Checkers clean across all 16; build + `lint:md` exit 0.
- [ ] [AI] Catalog rows added; band signal recorded; zero manifest files touched.
- [ ] [AI] Every sub-phase PR is `[AI]`-merged and deployed.

> **Pause Safety**: the low-level/languages band is live; `build-your-own-raft`'s and
> `build-your-own-database`'s prerequisite bodies (Bands 4 and 1) are already present, so no dangling
> edge exists. Safe to stop. To resume: re-run the section build.

---

## Phase 9: Band 7 — Security, ops, quality & delivery (11 bodies)

- [ ] [AI] `it-and-application-security` (Annotated-concept · Python) — convention complete; checkers
      clean.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] `offensive-security` (By Example · Python + shell) — convention complete; checkers clean;
      the body states its **lab-local, authorized-scope-only** rules of engagement — acceptance:
      `for w in "authorized" "lab"; do grep -F -q -i "$w" "apps/ayokoding-www/content/en/learn/courses/offensive-security/overview.md" || echo "MISSING $w"; done | wc -l`
      returns **0**.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `defensive-security` (By Example · Python + shell — **hands-on, NOT concept**, DD-12) —
      convention complete; checkers clean; the body delivers Sigma-on-ELK/OpenSearch + the IR lifecycle + hardening as generalist blue-team breadth.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `detection-engineering-and-siem-operations` (By Example · XML/rules + config + Python;
      declares `defensive-security` a prerequisite) — convention complete; checkers clean —
      distinctness acceptance: this course has the reader author working Wazuh decoders, correlation
      rules, and a dashboard with false-positive tuning; `defensive-security` retains the generalist
      Sigma/ELK breadth, IR, and hardening as its distinct scope. Verify the prerequisite
      (`grep -F -q 'defensive-security' "<COURSES>detection-engineering-and-siem-operations/_index.md"`
      exits 0) and verify **no lesson title is duplicated** across the two courses' syllabi:
      `comm -12 <(grep -h '^# ' apps/ayokoding-www/content/en/learn/courses/defensive-security/learning/*.md | sort -u) <(grep -h '^# ' apps/ayokoding-www/content/en/learn/courses/detection-engineering-and-siem-operations/learning/*.md | sort -u) | wc -l`
      returns **0**. Falsifiable both ways: copying one lesson title between the two courses makes it
      return 1.
      **The two `<(...)` process substitutions are load-bearing — never unwrap them.** The flag `-h`
      collides with `rtk grep --help`: a bare `grep -h '^# ' <file>` is rewritten by the harness hook
      to an `rtk grep -h` call, which prints a ~19-line usage banner and exits **0**, so a line count
      taken over it reads 19 no matter what the file contains. Inside `<(...)` the hook does not
      rewrite the call, so real grep semantics apply. [Repo-grounded — measured 2026-07-22:
      `cat <(grep -h '^# ' plans/backlog/ayokoding-learning-path-04-course-authoring/README.md) | wc -l`
      returns **1**, that README's single `#` heading, while the same grep issued bare returns the
      banner.] If this clause is ever restructured out of the wrappers, use `command grep -h`, or drop
      `-h` altogether and strip the `filename:` prefix with `sed 's/^[^:]*://'`.

  **Gherkin (binds) →** "Hands-on detection engineering stays distinct from generalist defensive security"

  ```gherkin
  Scenario: Hands-on detection engineering stays distinct from generalist defensive security
    Given the detection-engineering-and-siem-operations course is authored
    When a reader compares it with the hands-on defensive-security course
    Then it has the reader author working Wazuh decoders, correlation rules, and a dashboard with false-positive tuning
    And defensive-security keeps the generalist Sigma/ELK breadth, IR, and hardening as its distinct scope
  ```

  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

- [ ] [AI] `vulnerability-management-and-assessment` (By Example · Python) — convention complete;
      checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `it-governance-grc` (Annotated-concept · no code) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] `bare-metal-virtualization` (By Example · HCL/YAML/shell) — convention complete; checkers
      clean; its `overview.md` states the two-altitude boundary against `self-hosting-essentials`
      (DD-14) — acceptance:
      `grep -F -q 'self-hosting-essentials' "apps/ayokoding-www/content/en/learn/courses/bare-metal-virtualization/overview.md"`
      exits 0.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `self-managed-kubernetes-and-gitops` (By Example · YAML/CLI) — convention complete; checkers
      clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `platform-engineering-and-devex` (Annotated-concept · no code) — convention complete;
      checkers clean.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] `site-reliability-engineering` (Annotated-concept · Python) — convention complete; checkers
      clean.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] `analytics-and-experimentation` (By Example · Python) — convention complete; checkers clean;
      its `overview.md` states the boundary against `statistics-for-evaluation` (DD-26) — acceptance:
      `grep -F -q 'statistics-for-evaluation' "apps/ayokoding-www/content/en/learn/courses/analytics-and-experimentation/overview.md"`
      exits 0.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Apply the three per-band closing steps. `GROW_MANIFESTS` = the three software-engineer-role
      manifests.

### Phase 9 Gate

- [ ] [AI] All 11 Band-7 bodies exist:
      `for s in it-and-application-security offensive-security defensive-security detection-engineering-and-siem-operations vulnerability-management-and-assessment it-governance-grc bare-metal-virtualization self-managed-kubernetes-and-gitops platform-engineering-and-devex site-reliability-engineering analytics-and-experimentation; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done | wc -l`
      returns **0** (returns 11 before this phase).
- [ ] [AI] `defensive-security` is authored By-Example hands-on (DD-12 label correction applied);
      `detection-engineering-and-siem-operations` declares it as a prerequisite; the duplicate-lesson-title
      `comm` check returns 0.
- [ ] [AI] Both two-altitude boundaries stated (`bare-metal-virtualization` ↔ `self-hosting-essentials`;
      `analytics-and-experimentation` ↔ `statistics-for-evaluation`).
- [ ] [AI] `offensive-security` states its lab-local, authorized-scope-only rules of engagement.
- [ ] [AI] Checkers clean across all 11; build + `lint:md` exit 0.
- [ ] [AI] Catalog rows added; band signal recorded; zero manifest files touched.
- [ ] [AI] Every sub-phase PR is `[AI]`-merged and deployed.

> **Pause Safety**: the security/ops band is live; Band 8's `capstone-secure-service`,
> `capstone-data-pipeline`, and `capstone-build-your-own-pentest-engine` now have their prerequisite
> bodies present. Safe to stop. To resume: re-run the section build.

---

## Phase 10: Band 8 — Remaining capstones (8 bodies)

> **Ordering constraint**: this band follows Band 5 because `capstone-build-your-own-coding-agent`
> assembles the harness cluster, and follows Bands 4/7 because the concurrency and security capstones
> assemble those bands' bodies.

- [ ] [AI] `capstone-build-your-own-coding-agent` (Python; assembles the harness cluster) — convention
      complete; checkers clean; **Phase 2 D9 citation contract applied**: a harness-engineering
      naming/lineage line is present citing Anthropic (2025-11-26) and Böckeler/Thoughtworks
      (2026-02-17) — no rename. Assembly acceptance: the capstone's done-bar produces a runnable
      coding-agent CLI composed from the five cluster courses; a disallowed action **fails closed** and
      every run emits a trace — verify the capstone's own runnable acceptance-criteria checklist names
      all five source courses:
      `for s in the-agent-loop agent-tools-and-mcp agent-context-and-memory agent-permissions-and-sandboxing agent-orchestration-subagents-and-observability; do grep -F -q "$s" "apps/ayokoding-www/content/en/learn/courses/capstone-build-your-own-coding-agent/overview.md" || echo "MISSING $s"; done | wc -l`
      returns **0** (returns 5 before this step).

  **Gherkin (binds) →** "The coding-agent capstone assembles the harness cluster into a working CLI"

  ```gherkin
  Scenario: The coding-agent capstone assembles the harness cluster into a working CLI
    Given the harness cluster and the build-your-own-coding-agent capstone are authored
    When a reader completes the capstone
    Then they have a runnable coding-agent CLI built from the agent loop, tools/MCP, memory, permissions, and orchestration courses
    And a disallowed action fails closed while every run emits a trace
  ```

  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

- [ ] [AI] `capstone-build-your-own-pentest-engine` (TypeScript; swarm + MCP + CDP + security chaining)
      — convention complete; checkers clean. Assembly acceptance: the done-bar produces a runnable
      engine composed from swarm orchestration, MCP tooling, CDP browser driving, and
      security-tool-chaining; **scope enforcement refuses an out-of-scope target**; the body restates
      the lab-local, authorized-scope-only limits it inherits from `offensive-security`; and
      `vacti-pentest-engine` is named only as an illustration, never a required dependency — verify:
      `for w in "authorized" "out-of-scope"; do grep -F -q -i "$w" "apps/ayokoding-www/content/en/learn/courses/capstone-build-your-own-pentest-engine/overview.md" || echo "MISSING $w"; done | wc -l`
      returns **0**.

  **Gherkin (binds) →** "The pentest-engine capstone assembles the convergence track into a scoped engine"

  ```gherkin
  Scenario: The pentest-engine capstone assembles the convergence track into a scoped engine
    Given the harness cluster, the CDP course, the security suite, and detection-engineering are authored
    When a reader completes the build-your-own-pentest-engine capstone
    Then they have a runnable engine from swarm orchestration, MCP tooling, CDP browser driving, and security-tool-chaining
    And scope enforcement refuses an out-of-scope target while the capstone uses vacti-pentest-engine only as an illustration
  ```

  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_

- [ ] [AI] `capstone-real-world-delivery` (Python + TS + IaC; DD-20 — embedded spec in
      `$SYLLABUS_ROOT/defensive-security.md`) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `capstone-secure-service` (Python + shell; DD-20 — embedded spec in
      `$SYLLABUS_ROOT/defensive-security.md`) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `capstone-data-pipeline` (SQL + Python; DD-20 — embedded spec in
      `$SYLLABUS_ROOT/defensive-security.md`) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `capstone-concurrency-and-systems` (Go or Elixir + C; DD-20 — embedded spec in
      `$SYLLABUS_ROOT/compilers-parsers-and-transpilers.md`) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `capstone-concurrency-showdown` (Go + Elixir; DD-20 — embedded spec in
      `$SYLLABUS_ROOT/compilers-parsers-and-transpilers.md`) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `capstone-lead-at-altitude` (polyglot + prose; DD-20 — embedded spec in
      `$SYLLABUS_ROOT/site-reliability-engineering.md`) — convention complete; checkers clean.
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] Apply the three per-band closing steps. `GROW_MANIFESTS` for this band = the three
      software-engineer-role manifests **plus**
      `<MANIFESTS>careers/immediately-effective/ai-engineer.yaml` (DD-33 —
      `capstone-build-your-own-coding-agent` is the ninth of the nine courses that manifest walks).

### Phase 10 Gate

- [ ] [AI] All 8 Band-8 capstones exist:
      `for s in capstone-build-your-own-coding-agent capstone-build-your-own-pentest-engine capstone-real-world-delivery capstone-secure-service capstone-data-pipeline capstone-concurrency-and-systems capstone-concurrency-showdown capstone-lead-at-altitude; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done | wc -l`
      returns **0** (returns 8 before this phase).
- [ ] [AI] Each of the six DD-20 inter-topic capstones was authored from its **embedded spec** in the
      named `$SYLLABUS_ROOT` file, not invented — the goal, integrated-concepts checklist, ordered
      steps, acceptance criteria, and done bar all trace to that spec.
- [ ] [AI] The coding-agent capstone's five-source-course loop returns 0; the pentest capstone's
      authorization/scope loop returns 0.
- [ ] [AI] Checkers clean across all 8; build + `lint:md` exit 0.
- [ ] [AI] Catalog rows added; band signal recorded naming **four** manifests; zero manifest files
      touched.
- [ ] [AI] Every sub-phase PR is `[AI]`-merged and deployed.

> **Pause Safety**: every capstone this plan owns is live; the AI path's full nine-course harness walk
> now has all its bodies present, so the manifest plan can grow that path to its full DD-35-governed
> composition (no longer a fixed 15-course figure — DD-35 superseded DD-33's original 6→15 math).
> Safe to stop. To resume: re-run the section build.

---

## Phase 11: Band 9 — Interview-technique courses (5 bodies)

> These five were **deferred from the interview-ready MVP gate** (DD-27) so they never blocked the AI
> path's authoring start. All four courses are written in a **refresh register** — they assume prior
> professional experience (DL-6).

- [ ] [AI] `coding-interview` (By Example · Python) — convention complete; checkers clean; refresh
      register applied.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `take-home-and-live-coding` (By Example · Python) — convention complete; checkers clean;
      refresh register applied.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] `system-design-interview` (Annotated-concept · no code; forward-links `system-design`) —
      convention complete; checkers clean; refresh register applied — acceptance:
      `grep -F -q 'system-design' "apps/ayokoding-www/content/en/learn/courses/system-design-interview/overview.md"`
      exits 0 (the rubric course forward-links the depth course rather than re-teaching it, DD-10).
  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_
- [ ] [AI] `behavioral-and-leadership-interviews` (Annotated-concept · no code) — convention complete;
      checkers clean — coverage acceptance: the learning track explicitly covers framing an employment
      gap, a layoff, and a re-entry story, and treats senior/staff/EM leadership rounds as core (not
      optional) material. Verify:
      `for w in "employment gap" "layoff" "re-entry"; do grep -F -q -r -i "$w" "apps/ayokoding-www/content/en/learn/courses/behavioral-and-leadership-interviews/learning/" || echo "MISSING $w"; done | wc -l`
      returns **0** (returns 3 before this step).

  **Gherkin (binds) →** "The behavioral course covers the layoff and employment-gap narrative"

  ```gherkin
  Scenario: The behavioral course covers the layoff and employment-gap narrative
    Given the behavioral-and-leadership-interviews course is authored
    When an experienced re-entrant reads its learning track
    Then it explicitly covers framing an employment gap, a layoff, or a re-entry story
    And it treats senior/staff/EM leadership rounds as core material
  ```

  - _Suggested executor: `apps-ayokoding-www-annotated-concept-maker`_

- [ ] [AI] **Verify the refresh register across all four interview courses** — each course's
      `overview.md` states it assumes prior professional experience and frames the material as
      technique/breadth refresh, never a from-zero concept teach. Verify:
      `for s in coding-interview take-home-and-live-coding system-design-interview behavioral-and-leadership-interviews; do grep -F -q -i "assumes" "apps/ayokoding-www/content/en/learn/courses/$s/overview.md" || echo "MISSING $s"; done | wc -l`
      returns **0** (returns 4 before this phase, since none of the four directories exists yet).

  **Gherkin (binds) →** "Interview courses are written in a refresh register"

  ```gherkin
  Scenario: Interview courses are written in a refresh register
    Given the four new interview-technique courses are authored
    When an experienced engineer reads them
    Then each assumes prior professional experience and focuses on interview technique and breadth refresh
    And none teaches core concepts from zero
  ```

- [ ] [AI] `capstone-interview-loop` (Python + prose; full mock loop: coding + system-design +
      behavioral) — convention complete; checkers clean — acceptance: its `_index.md` declares all four
      interview courses as prerequisites:
      `for s in coding-interview take-home-and-live-coding system-design-interview behavioral-and-leadership-interviews; do grep -F -q "$s" "apps/ayokoding-www/content/en/learn/courses/capstone-interview-loop/_index.md" || echo "MISSING $s"; done | wc -l`
      returns **0**.
  - _Suggested executor: `apps-ayokoding-www-by-example-maker`_
- [ ] [AI] Apply the three per-band closing steps. **`GROW_MANIFESTS` for this band is only two
      manifests**: `<MANIFESTS>careers/interview-ready/software-engineer.yaml` and
      `<MANIFESTS>careers/fundamentally-strong/software-engineer.yaml`.
      `careers/immediately-effective/software-engineer` does **not** grow — that path omits the
      interview-technique band from its `courseOrder` by design (its reader reaches these courses via
      their canonical pages). The signal MUST name exactly these two; naming three would cause the
      manifest plan to grow a path the design excludes.

### Phase 11 Gate

- [ ] [AI] All 5 Band-9 bodies exist:
      `for s in coding-interview take-home-and-live-coding system-design-interview behavioral-and-leadership-interviews capstone-interview-loop; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done | wc -l`
      returns **0** (returns 5 before this phase).
- [ ] [AI] The refresh-register loop returns 0 across all four interview courses; the
      employment-gap/layoff/re-entry loop returns 0; `capstone-interview-loop` declares all four as
      prerequisites.
- [ ] [AI] `system-design-interview` forward-links `system-design` rather than re-teaching depth
      (DD-10).
- [ ] [AI] Checkers clean across all 5; build + `lint:md` exit 0.
- [ ] [AI] Catalog rows added; band signal recorded naming **exactly two** manifests; zero manifest
      files touched.
- [ ] [AI] Every sub-phase PR is `[AI]`-merged and deployed.

> **Pause Safety**: all 90 authored bodies are now live. The library is content-complete from this
> plan's side; every downstream signal is recorded. Safe to stop. To resume: re-run the section build
> and the 90-slug presence check.

---

## Phase 12: Section & Authored-Tree Verification

- [ ] [AI] **Verify all 90 authored bodies are present** —
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done < evidence/authored-body-slugs.txt | wc -l`
      — acceptance: returns **0**. Falsifiable both ways: this returned **90** at the Phase-0 baseline,
      and removing any one bundle makes it return 1.
- [ ] [AI] **Verify every authored body declares prerequisites** —
      `while read -r s; do grep -F -q 'prerequisites:' "apps/ayokoding-www/content/en/learn/courses/$s/_index.md" || echo "MISSING $s"; done < evidence/authored-body-slugs.txt | wc -l`
      — acceptance: returns **0** (returns 90 at baseline).
- [ ] [AI] **Verify every authored body has both tracks** —
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s/learning" && test -d "apps/ayokoding-www/content/en/learn/courses/$s/drilling" || echo "INCOMPLETE $s"; done < evidence/authored-body-slugs.txt | wc -l`
      — acceptance: returns **0**.
- [ ] [AI] **Supersession sweep (Q-A-conditional)** — this plan's hard `blockedBy` on
      `ayokoding-learning-path-01-url-restructure` guarantees Q-A is ruled (not left
      "Recommendation") by the time this phase runs: Phase 0 already verified that plan is merged to
      `origin/main`, and its own archival gate requires all six Q-A…Q-F rulings recorded in its
      `tech-docs.md`. Read the ruled option in the
      [Q-A record](../ayokoding-learning-path-01-url-restructure/tech-docs.md#q-a--is-legacy-a-staging-pen-or-a-permanent-archive)
      before branching:
  - **If ruled A (staging pen) or C (hybrid, for the overlapping subjects)**: for every course in
    `evidence/authored-body-slugs.txt` whose subject overlaps a remaining
    `apps/ayokoding-www/content/en/learn/legacy/` page, append a `Superseded by:` line naming that
    page to the course's own `<COURSES><course-id>/overview.md`, and record the identified slug list
    (one per line) to `evidence/supersession-sweep-slugs.txt` — acceptance:
    `grep -lF 'Superseded by:' <COURSES>*/overview.md | wc -l` equals
    `wc -l < evidence/supersession-sweep-slugs.txt`. Falsifiable both ways: before this step runs,
    `grep -lF 'Superseded by:' <COURSES>*/overview.md | wc -l` returns **0**; after this step, both
    counts are equal (non-zero unless the overlap set is genuinely empty, in which case both are 0
    and this branch's outcome matches ruling B's).
  - **If ruled B (permanent archive)**: edit no `overview.md`; record
    `Q-A ruled B — no supersession sweep performed` in `learnings.md` — acceptance:
    `grep -lF 'Superseded by:' <COURSES>*/overview.md | wc -l` returns **0**.
  - Either branch commits on this phase's own branch, ahead of this phase's existing
    manifest-ownership check below and its own draft PR — no separate branch or PR is opened for the
    sweep. The sweep only ever touches `<COURSES>*/overview.md`, never a `<MANIFESTS>` path, so it is
    already covered by this phase's manifest-ownership check, which runs on this same branch before
    the phase merges.
- [ ] [AI] Run affected quality gates from the worktree:
      `npx nx affected -t typecheck lint test:quick test:unit specs:behavior:coverage`
      — acceptance: exits 0. Fix ALL failures, including preexisting ones (Root Cause Orientation),
      committing preexisting fixes separately.
- [ ] [AI] Build the site: `npx nx run ayokoding-www:build` — acceptance: exits 0.
- [ ] [AI] Run link + heading-hierarchy + markdown validation:
      `cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md heading-hierarchy validate` +
      `npm run lint:md`, plus the scoped link gate:

  ```bash
  cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate \
    --quiet \
    --exclude plans/done \
    --exclude apps/ose-www/content 2>&1 | grep -F "learn/courses/"
  ```

  — acceptance: the first two exit 0 and the `grep` finds **no** line naming a `learn/courses/`
  path (exits 1). Note the content exclusion is narrowed here (only `ose-www` content is excluded)
  precisely so this plan's own authored bodies are validated; `plans/done` stays excluded because
  the repo carries a pre-existing, non-zero backlog of broken links there, unrelated to this work
  (137 as of 2026-07-22, and drifts as more plans archive).

  **Gherkin (binds) →** "The authored course library builds and validates green"

  ```gherkin
  Scenario: The authored course library builds and validates green
    Given every course body this plan authors has landed under the courses bucket
    When the ayokoding-www build, markdownlint, link validation, and heading-hierarchy validation run
    Then the build succeeds over the authored tree
    And link, heading-hierarchy, and markdownlint validation report no errors across the authored course bodies
  ```

- [ ] [AI] **Verify zero manifest files were touched by this entire plan** — every phase before this
      one, whether or not it opens its own PR, carries the identical individual check on its own diff
      before that phase merges or folds into its delivery unit's PR (Phase 0's check, Phase 1's check,
      Phase 2's check, and every "per-band closing steps" step 3, Phases 3–11); each of the **90
      individual course sub-phases** nested inside Phase 1
      and Bands 1–9 additionally carries its own instance of this check as **convention step 8** (see the
      "NEW-course authoring convention"), asserted on that course's own branch before it merges — the
      closing-steps checks alone branch fresh from `origin/main` after every course in that band has
      already merged, so they can only ever see their own diff, never the already-merged course diffs;
      only each course's own convention step 8 can see that. Re-assert the same sound mechanism here on
      this phase's own branch. A commit-message `--grep` filter is unsound for this purpose: nothing in
      this plan mandates the plan identifier appear in commit messages (the Commit Guidelines example
      below, `feat(ayokoding-www): add nosql-databases course body`, does not contain it), and a filter
      that matches zero commits exits 0 and looks like success whether or not the invariant actually
      held:
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**. Falsifiable both ways: touching any file under that path on this
      branch makes it return ≥1; this check, plus every one of the 90 course sub-phases' own
      convention-step-8 check, plus every prior phase's own already-passed individual check, together
      constitute the ownership invariant's terminal proof for Phases 0–12 (Phase 13, 14, and 15 each
      carry — or, for Phase 14, do not need, since it commits nothing of its own — the same individual
      check on their own diffs; Phase 16 re-asserts once more for its own diff).
- [ ] [AI] **Verify every band-completion signal is complete** — each of the ten signals in this file
      (Phase 1 + Bands 1–9) carries all five fields and a `MERGED_COMMIT` that resolves. Anchor the
      count on the field's line-start form (`MERGED_COMMIT: <sha>` alone on its own line inside the
      fenced signal block per the [band-completion signal contract](./README.md#band-completion-signal-contract))
      so the checklist's own prose mentions of the bare substring `MERGED_COMMIT:` (this explanation,
      the command below, and Phase 14's downstream-notification check all mention the literal
      substring in prose) are never counted:
      `for c in $(grep -oE '^MERGED_COMMIT: [0-9a-f]{7,40}$' delivery.md | awk '{print $NF}'); do git cat-file -e "$c^{commit}" || echo "BAD $c"; done | wc -l`
      — acceptance: returns **0**, and `grep -cE '^MERGED_COMMIT: [0-9a-f]{7,40}$' delivery.md` returns
      **10** (`-c` counts matching _lines_ here, which is exactly one per genuine signal block, not
      substring occurrences — unlike the bare-substring form `grep -cF 'MERGED_COMMIT:' delivery.md`,
      which overcounts by however many prose lines in this checklist happen to mention the literal
      substring at the time; that count drifts as the checklist itself is edited, so do not trust a
      fixed number here — run `grep -nF 'MERGED_COMMIT:' delivery.md` to see the live count before
      reasoning about the bare-substring form). Falsifiable both ways: today, before any band lands,
      both commands return **0** (not 10); once all ten signals are genuinely recorded, the second
      returns exactly **10**.

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes
> (Root Cause Orientation). Commit preexisting fixes separately with conventional-commit messages.

### Phase 12 Gate

- [ ] [AI] All three 90-body structural loops (presence, prerequisites, both tracks) return 0.
- [ ] [AI] Supersession sweep resolved one way or the other: either the `Superseded by:` count in
      `<COURSES>*/overview.md` matches `evidence/supersession-sweep-slugs.txt`, or Q-A ruled B and
      `learnings.md` records the no-op — never left unresolved.
- [ ] [AI] Affected `typecheck / lint / test:quick / test:unit / specs:behavior:coverage` exit 0.
- [ ] [AI] Build + heading-hierarchy + markdownlint green; the scoped link gate finds no
      `learn/courses/` failure.
- [ ] [AI] Zero manifest files touched across the whole plan's history; all ten band signals complete
      with resolvable `MERGED_COMMIT` SHAs.
- [ ] [AI] Draft PR opened at Phase 12 — this unit's own boundary (see the
      [`### Delivery Boundaries`](#delivery-boundaries) table); 3-cycle PR-Review complete; CI green;
      PR `[AI]`-merged; deployed.

> **Pause Safety**: the authored library passes every automated gate. Safe to stop. To resume: re-run
> the affected quality gates + build.

---

## Phase 13: Manual Content Verification (Playwright MCP)

> **Locale scope**: this plan's course content is authored `en`-only — per
> [brd.md §Business-Scope Non-Goals](./brd.md#business-scope-non-goals), an Indonesian content mirror
> is explicitly deferred. Verify the authored course pages in `en` only; do not fabricate an `id`
> walk-through for content that does not exist. This is a content-availability fact, not a code
> limitation.
>
> **Rule-15 exemption (recorded, not silently omitted)**: the three live-site testers
> (`web-exploratory-tester` / `web-usability-tester` / `web-design-tester`) are **exempt for this
> plan**, for three reasons: (1) it ships no screen or component — every artefact is a markdown page
> bundle rendered by components owned by
> [`ayokoding-learning-path-03-navigation-ui`](../ayokoding-learning-path-03-navigation-ui/README.md);
> (2) its output surface is already covered by the ayokoding content checkers, which are
> content-specific where the triad is UI-specific; (3) running the triad here would test the other
> plan's navigation surface and file its defects against the wrong plan. See
> [README §Rule-15](./README.md#rule-15-three-tester-retest--exemption-recorded). **The exemption is
> narrow** — the Playwright manual behavioural verification below is mandatory and performed, with
> committed evidence.

- [ ] [AI] Confirm `en` is the content locale for the course library — command:
      `test -d apps/ayokoding-www/content/en/learn/courses && test ! -d apps/ayokoding-www/content/id/learn/courses`
      — acceptance: exits 0 (the `en` bucket exists; no `id` mirror is expected or required).
- [ ] [AI] Start dev server: `npx nx dev ayokoding-www` — acceptance: server up on port 3101.
- [ ] [AI] **Sample-verify authored course pages** — for a sample of **nine** authored courses (one per
      band) plus **two** AI-engineering courses, at breakpoints 375 / 768 / 1280 px, via Playwright MCP:
      `browser_navigate` to `/en/learn/courses/<course-id>`, `browser_resize`, then `browser_snapshot`
      — acceptance: each page renders its overview, learning track, and drilling track; `html[lang]` is
      `en`; `browser_console_messages` reports **zero** errors per page per breakpoint.
- [ ] [AI] **Verify prerequisite rendering** — on a course with a declared prerequisite chain (e.g.
      `evaluating-ai-systems-in-depth`, which declares `statistics-for-evaluation`), confirm the
      prerequisite is displayed and its link resolves to the prerequisite's canonical page —
      acceptance: the link target returns 200 and the landed page is the named prerequisite.
- [ ] [AI] **Verify a drilling track renders** — open one authored `drilling/<course-id>.md` page and
      confirm all five fixed sections are present in the rendered output — acceptance: five section
      headings visible in `browser_snapshot`.
- [ ] [AI] Capture one screenshot per sampled course per breakpoint to
      `evidence/phase-13-<course-id>-en-<breakpoint>px.png` — acceptance:
      `git ls-files -- 'evidence/phase-13-*-en-*px.png' | grep -c .` returns **33** (11 courses × 3
      breakpoints), once the captures are staged or committed with the rest of this phase's evidence.
      Counting with `git ls-files` rather than `find … | wc -l` keeps the number immune to RTK's
      `find` reformatting (see Phase 0's blocking-plan checks for the measurement).
      Falsifiable both ways: returns 0 before this step and a number below 33 if any capture is skipped.
- [ ] [AI] Document the evidence in this checklist: reference each screenshot
      (`![alt](./evidence/...)`) and note the console/network status per sampled course — acceptance:
      every captured file is referenced.
- [ ] [AI] **Record the rule-15 exemption in `learnings.md`** with its three reasons and a pointer to
      the navigation-UI plan that carries the triad — acceptance: the exemption entry is present, so
      the archival gate can verify it was recorded rather than forgotten.
- [ ] [AI] **Confirm no manifest file changed in this phase** — Phase 13 is intermediate (see the
      [`### Delivery Boundaries`](#delivery-boundaries) table): its evidence commits fold into the
      Phase 16 closeout PR rather than opening one of their own, so this phase still needs its own
      individual gate on this phase's own diff before that PR opens:
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**. Falsifiable both ways: touching any file under that path makes the
      command return ≥1 and the phase gate fails.

### Phase 13 Gate

- [ ] [AI] Eleven sampled courses verified across three breakpoints in `en`; zero console errors;
      prerequisite display and drilling-track rendering confirmed.
- [ ] [AI] 33 screenshots present under `evidence/` and referenced in this checklist.
- [ ] [AI] The rule-15 exemption is recorded with reasons (not silently omitted); the triad itself is
      **not** run here.
- [ ] [AI] Zero manifest files touched (`git diff --name-only ... | grep -c .` returns 0).
- [ ] [AI] **No PR opens for this phase** (intermediate — see the
      [`### Delivery Boundaries`](#delivery-boundaries) table): the evidence commits are on the shared
      worktree, this phase's own gate above is green, and nothing is pushed for review yet — the
      closeout PR for Phases 13–16 opens at Phase 16.

> **Pause Safety**: the authored library is verified live and defect-clean in `en`. Safe to stop. To
> resume: restart the dev server and re-open one sampled course per band.

---

## Phase 14: Final `origin/main` Integration & CI Verification

- [ ] [AI] Confirm no plan PR is still open:
      `gh pr list --search "ayokoding-learning-path-04-course-authoring" --state open --json number --jq 'length'`
      — acceptance: returns **0**. Falsifiable both ways: an open PR makes it return ≥1.
- [ ] [AI] Sync the worktree to latest `origin/main` and run the full affected suite:
      `npx nx affected -t typecheck lint test:quick test:unit specs:behavior:coverage` +
      `npx nx run ayokoding-www:build` — acceptance: all exit 0 on the integrated `main`.
- [ ] [AI] Monitor the final `main` CI run (poll every ~2 min; one
      `gh run view --json status,conclusion` per wakeup; never `gh run watch`) — acceptance: all GitHub
      Actions green; fix root causes and push follow-ups (own PR → review → `[AI]` merge) until green.
      **Any follow-up PR opened here carries the identical individual manifest-diff check on its own
      branch before it merges** — this hypothetical path has no dedicated content-authoring convention
      to inherit the check from (unlike the 90 course sub-phases), so it is stated explicitly here:
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      returns **0** on the follow-up branch before merge. Falsifiable both ways: touching any file
      under that path makes it return ≥1.
- [ ] [AI] Confirm `prod-ayokoding-www` serves the authored bodies — spot-check five canonical course
      URLs across five different bands — acceptance: each returns 200 with the expected course title.
      Re-dispatch `apps-ayokoding-www-deployer` if any earlier deploy lagged.
- [ ] [AI] **Notify the downstream manifest plan** — confirm all ten band-completion signals are
      present in this file on `origin/main` and reachable by
      [`ayokoding-learning-path-05-manifests`](../ayokoding-learning-path-05-manifests/delivery.md)
      — acceptance: two steps. (a) Resolve the literal path on `origin/main` — command (single line):
      `git ls-tree -r --name-only origin/main -- plans | grep -F 'ayokoding-learning-path-04-course-authoring/delivery.md'`
      — it prints **exactly one** path. (b) Feed that literal path to `git show` — command (single line):
      `git show "origin/main:<the printed path>" | grep -cE '^MERGED_COMMIT: [0-9a-f]{7,40}$'`
      returns **10**.
      **Never put a glob in a `git show <rev>:<path>` argument.** Unquoted,
      `plans/*/ayokoding-…/delivery.md` is a zsh pattern, and whenever it matches nothing zsh aborts
      the whole command line with `no matches found` before `git show` runs. Quoted, it fares no
      better: `git show` does **not** glob-expand its path argument, so it returns **zero bytes and
      exits 0**, making the acceptance value of 10 silently unreachable. [Repo-grounded — both
      measured 2026-07-22.] Uses the same anchored line-start form as Phase 12's band-completion-signal
      check; the bare-substring form (`grep -cF 'MERGED_COMMIT:'`) is unreachable here too, for the
      same reason — it also matches this checklist's own prose mentions of the literal substring, so
      it overcounts by however many such prose lines exist at the time (that count drifts as the
      checklist is edited; re-run `grep -nF 'MERGED_COMMIT:' delivery.md` for the live figure rather
      than trusting a fixed number here). Falsifiable both ways: today, before any band lands, this
      returns **0**.

### Phase 14 Gate

- [ ] [AI] Zero open plan PRs; every prior phase merged to `main`.
- [ ] [AI] Full affected suite + build green on integrated `main`; final `main` CI run green.
- [ ] [AI] `prod-ayokoding-www` serving the authored bodies (five spot-checks return 200).
- [ ] [AI] All ten band signals present on `origin/main` and reachable downstream.

> **Pause Safety**: the whole plan is integrated on `main`, green in CI, and live in production; the
> downstream manifest plan has everything it needs. Safe to stop. To resume: re-run the affected suite
> on `main` and check CI/prod status.

---

## Phase 15: Knowledge Capture

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)._

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only if a durable surface would
      catch this automatically next time; discard the rest with a one-line reason — acceptance: every
      entry has a route or a discard reason.
- [ ] [AI] Apply the **secret/sensitivity gate** to every surviving entry — sanitize any secret,
      credential, token, or private hostname to a `<placeholder>` token, or discard if unsanitizable —
      acceptance: `learnings.md` contains no raw secret.
- [ ] [AI] Apply the **repo-relevance gate** — infra-private content (Terraform, k3s, Proxmox, real
      hostnames/inventories) stays in `ose-infra` only and is NEVER cross-routed into
      `ose-public`/`ose-primer`; public-governance content may propagate via the existing parity loop —
      acceptance: no infra-private content appears in this repo's routed output.
- [ ] [AI] Route each surviving learning to exactly one durable home per the open-ended routing matrix
      — non-code homes may land inline (small edit) or as a `plans/backlog/` follow-up (large); **code
      homes (`apps/`, `libs/`, tests) are ALWAYS filed as a separate `plans/backlog/<slug>/` plan and
      NEVER landed inline**. Note this plan's own artefacts are content, not code — a learning about
      the `course-paths` feature code is code-homed and goes to backlog — acceptance: every entry
      records its terminal routing state.
- [ ] [AI] If no generalizable learning surfaced, record `No generalizable learnings — <reason>` in
      `learnings.md` — acceptance: `learnings.md` is never silently empty.
- [ ] [AI] **Confirm no manifest file changed in this phase** — Phase 15 is intermediate (see the
      [`### Delivery Boundaries`](#delivery-boundaries) table): it commits the `learnings.md` triage
      and any inline non-code fixes on the shared closeout branch and folds into the Phase 16 PR
      rather than opening one of its own, so this phase still gets the same individual gate on its own
      diff (the code-routing rule above already forbids landing a manifest-touching fix inline; this
      re-asserts it mechanically rather than trusting the routing rule alone):
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      — acceptance: returns **0**. Falsifiable both ways: touching any file under that path makes the
      command return ≥1 and the phase gate fails.

### Phase 15 Gate

- [ ] [AI] Every `learnings.md` entry is terminal (routed inline / filed as backlog / discarded with
      reason) or the explicit "none" escape is present.
- [ ] [AI] No code-homed learning landed inline in this plan's own commits/PRs.
- [ ] [AI] Zero manifest files touched (`git diff --name-only ... | grep -c .` returns 0).
- [ ] [AI] **No PR opens for this phase** (intermediate — see the
      [`### Delivery Boundaries`](#delivery-boundaries) table): the `learnings.md` triage is committed
      on the shared closeout branch, this phase's own gate above is green, and nothing is pushed for
      review yet — the closeout PR for Phases 13–16 opens at Phase 16.

> **Pause Safety**: `learnings.md` is fully triaged; nothing depends on querying it later. Safe to
> stop. To resume: re-read `learnings.md` and confirm every entry is terminal.

---

## Phase 16: Plan Archival

- [ ] [AI] Verify ALL delivery checklist items are ticked.
- [ ] [AI] Verify the Knowledge Capture phase is complete (every entry terminal or the explicit "none"
      escape present; both safety gates applied to every surviving entry).
- [ ] [AI] Verify ALL quality gates pass (local + CI) and the build is green.
- [ ] [AI] Verify ALL manual assertions pass (Playwright MCP) with committed evidence in `evidence/`;
      the `en` content locale exercised (per the Indonesian-mirror-deferred non-goal).
- [ ] [AI] Verify the **rule-15 exemption is recorded with reasons** in `learnings.md` and in Phase 13
      — acceptance: `grep -F -q 'rule-15' learnings.md` exits 0. The triad itself is exempt here; the
      navigation-UI plan runs it against the surface it owns.
- [ ] [AI] **Verify this plan's authored-body assertion** —
      `while read -r s; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done < evidence/authored-body-slugs.txt | wc -l`
      returns **0**, and `wc -l < evidence/authored-body-slugs.txt` returns **90** — acceptance: both
      hold. **This plan asserts 90, not 127.** The 127-course catalog total is
      `ayokoding-learning-path-05-manifests`'s terminal assertion (90 authored here + 37 re-homed by
      `ayokoding-learning-path-01-url-restructure`).
- [ ] [AI] **Verify the ownership invariant held** — re-assert the same sound diff-based mechanism used
      by every prior commit-producing phase's own individual check (Phase 0, Phase 1, Phase 2, every
      band's per-band closing steps, every one of the 90 individual course sub-phases' own convention
      step 8, Phase 12, Phase 13, and Phase 15), on this phase's own diff (a commit-message `--grep`
      filter is unsound: nothing mandates the plan identifier appear in commit messages, and a filter
      matching zero commits exits 0 and looks like success regardless of whether the invariant actually
      held):
      `git diff --name-only origin/main...HEAD -- 'apps/ayokoding-www/src/features/course-paths/manifests/' | grep -c .`
      returns **0** — acceptance: no manifest file was touched on this branch. Falsifiable both ways:
      touching any file under that path makes it return ≥1.
- [ ] [AI] **Verify every cross-plan reference still resolves after upstream archival** — the schema
      plan archives to `plans/done/YYYY-MM-DD__…` while this plan runs, so re-run the BF-8 link gate:

  ```bash
  cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate \
    --quiet \
    --exclude plans/done \
    --exclude apps/ayokoding-www/content \
    --exclude apps/ose-www/content 2>&1 | grep -F "ayokoding-learning-path-04-course-authoring"
  ```

  — acceptance: the `grep` finds **no** matching line (exits 1). If the schema plan's reciprocal
  repoint step has not landed, fix the references in **this plan's own files** and record it —
  never edit the other plan's folder.

- [ ] [AI] Move: `git mv plans/in-progress/ayokoding-learning-path-04-course-authoring/ plans/done/YYYY-MM-DD__ayokoding-learning-path-04-course-authoring/`
      using today's **completion** date, not the creation date (the `evidence/` subfolder moves with it).
- [ ] [AI] Update `plans/in-progress/README.md` — remove the plan entry.
- [ ] [AI] Update `plans/done/README.md` — add the plan entry with completion date.
- [ ] [AI] Update any other READMEs that reference this plan (`plans/README.md`,
      `plans/backlog/README.md`) and notify the four sibling split plans whose `Depends-on` tables name
      this plan by folder path — acceptance: no sibling plan's link to this folder is left dangling
      (re-run the BF-8 gate with each sibling's folder name substituted in the `grep -F`).
- [ ] [AI] Commit the archival:
      `chore(plans): move ayokoding-learning-path-04-course-authoring to done`.

### Phase 16 Gate

- [ ] [AI] All 90 authored bodies present (the ABSENT loop returns 0, down from the Phase-0 baseline of
      90); the slug register holds 90 unique lines.
- [ ] [AI] Zero manifest files touched across the plan's entire history.
- [ ] [AI] The BF-8 cross-plan link gate is green after the schema plan's archival.
- [ ] [AI] Plan folder is under `plans/done/YYYY-MM-DD__ayokoding-learning-path-04-course-authoring/`;
      all READMEs updated; archival committed.
- [ ] [AI] Draft PR opened for the Phase 13–16 closeout unit (manual verification evidence,
      `learnings.md` triage, and the archival move — this unit's own boundary; see the
      [`### Delivery Boundaries`](#delivery-boundaries) table); 3-cycle PR-Review complete; CI green;
      PR `[AI]`-merged; deployed (no-op).

> **Pause Safety**: the plan is archived and its final PR `[AI]`-merged to `main`. Terminal state. To
> resume: nothing — the plan is complete.

---

### Commit Guidelines (all phases)

- [ ] [AI] Commit changes thematically — group related changes into logically cohesive commits (one
      course bundle per commit is the natural unit here).
- [ ] [AI] Follow Conventional Commits: `<type>(<scope>): <description>` (imperative, no period) —
      e.g. `feat(ayokoding-www): add nosql-databases course body`.
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

This plan is created in `plans/backlog/ayokoding-learning-path-04-course-authoring/`. When work
starts it is promoted to `plans/in-progress/ayokoding-learning-path-04-course-authoring/` (no date
prefix on either); the `git mv` in Phase 16 then archives it to
`plans/done/YYYY-MM-DD__ayokoding-learning-path-04-course-authoring/` using the completion date.
