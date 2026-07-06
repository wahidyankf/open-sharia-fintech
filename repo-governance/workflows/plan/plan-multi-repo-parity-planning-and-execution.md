---
name: plan-multi-repo-parity-planning-and-execution
title: "plan-multi-repo-parity-planning-and-execution"
goal: Author aligned-but-deliberately-divergent plans across sibling repositories for a shared objective, then execute every resulting plan to zero-findings completion and archival — one end-to-end orchestration from idea to delivered parity
termination: "Every parity plan passes plan-quality-gate (double-zero), every plan executes to zero findings via plan-execution, every plan is archived to plans/done/ in its repo with all work pushed, and every plan worktree is cleaned up (or retained by explicit user choice)"
inputs:
  - name: objective
    type: string
    description: "The shared topic to standardize or align across repos (e.g., 'standardize markdown gates', 'align agent catalogs')"
    required: true
  - name: repos
    type: string
    description: "Comma-separated target repository names or absolute paths in the parity set"
    required: false
    default: "ose-public, ose-primer, ose-infra"
  - name: mode
    type: enum
    values: [main-to-main, worktree-to-main]
    description: "Planning-phase delivery mode passed to plan-multi-repo-parity-planning. worktree-to-pr is NOT supported by this composite — execution cannot start on plans that are awaiting PR review (use the planning workflow alone for that)"
    required: false
    default: worktree-to-main
  - name: gate-mode
    type: enum
    values: [lax, normal, strict, ocd]
    description: "Mode passed through to plan-quality-gate for each plan"
    required: false
    default: strict
  - name: max-iterations
    type: number
    description: Maximum execute-check cycles per plan during the execution phase (passed to plan-execution)
    required: false
    default: 10
  - name: max-concurrency
    type: number
    description: Maximum concurrent agents during gate runs
    required: false
    default: 2
  - name: execution-order
    type: string
    description: "Repo execution order for the execution phase; confirmed in the pre-execution grill"
    required: false
    default: "as listed in repos"
outputs:
  - name: plans-created
    type: file-list
    description: One plan folder path per target repo (archived to plans/done/ on success)
  - name: gate-results
    type: string
    description: "plan-quality-gate final status per plan (pass/partial/fail)"
  - name: execution-results
    type: string
    description: "plan-execution final status per repo (pass/partial/fail) with iterations-completed"
  - name: delivery-refs
    type: string
    description: "Commits pushed to each repo's origin main during planning and execution phases"
---

# Plan Multi-Repo Parity Planning and Execution Workflow

**Purpose**: Run the full parity lifecycle end-to-end: first orchestrate
[plan-multi-repo-parity-planning](./plan-multi-repo-parity-planning.md) to survey the parity set,
grill every cross-repo gap to a recorded decision, and author one gated plan per repo — then
continue WITHOUT a separate invocation into [plan-execution](./plan-execution.md) for each
resulting plan, executing every delivery checklist to zero findings and archiving each plan to its
repo's `plans/done/`. The composite exists so "plan it across the repos AND do it" is a single
orchestrated request instead of four manual hand-offs.

This workflow composes its two constituents **by reference**: every rule of
plan-multi-repo-parity-planning governs the planning phase, and every rule of plan-execution
(worktree gate, Iron Rules, Atomic Sync Ritual, CI verification, archival, prompted worktree
cleanup) governs the execution phase. This document defines only the glue: the phase gate between
them, the third (pre-execution) grill, the composite Task list contract, and cross-repo
finalization.

**When to use**:

- When the same structural improvement is needed across sibling repos and the invoker wants it
  planned AND delivered in one orchestrated run
- When the cross-repo decision surface needs the parity grilling discipline, and the resulting
  plans should not sit unexecuted
- When you want one continuous observability surface (a single live Task list) covering planning
  and execution across all repos

**When NOT to use**:

- Plans should be reviewed via PR before execution → run
  [plan-multi-repo-parity-planning](./plan-multi-repo-parity-planning.md) alone with
  `mode: worktree-to-pr`, then run [plan-execution](./plan-execution.md) per repo after merge
- Single-repo work → [plan-planning](./plan-planning.md) followed by
  [plan-execution](./plan-execution.md)

## Execution Mode

**Direct Orchestration** — the calling context (the top-level assistant session) is the
orchestrator for the whole composite. This is mandatory, not preferred: plan-execution requires
calling-context orchestration so the live Task list stays visible to the user in real time.
Within the planning phase, the orchestrator delegates exactly as
plan-multi-repo-parity-planning specifies (`plan-maker`, `web-researcher`, `plan-checker`,
`plan-fixer` via the Agent tool). Within the execution phase, it delegates per-item work to
specialized agents exactly as plan-execution specifies, and invokes `plan-execution-checker` for
independent validation.

**How to Execute**:

```
User: "Run plan-multi-repo-parity-planning-and-execution for objective: standardize markdown gates"
```

## Granular Task List Contract (Composite-Wide, Non-Negotiable)

The harness Task list (`TaskCreate` / `TaskUpdate`) is the user's only real-time view of this
long-running composite. It MUST stay granular, current, and in sync from the first survey to the
last worktree cleanup prompt.

**Composite-level tasks** (created at workflow start):

- `TaskCreate` exactly one task per composite step: each planning step (survey, matrix, first
  grill, research, second grill, authoring per repo, gate per plan, delivery), the phase gate,
  the pre-execution grill, one execution placeholder per repo, and cross-repo finalization.
- At most ONE task `in_progress` at any moment, across the entire composite.
- Mark a task `in_progress` BEFORE the first tool call advancing it; mark `completed` only when
  its output criterion is met.

**Execution-phase expansion (flattened delivery checklist)**: when the execution phase reaches
repo R, the orchestrator expands R's placeholder by reading R's `delivery.md` and appending the
delivery checklist to the live Task list as a **flattened** set of tasks — exactly as
[plan-execution §Task-Checklist Synchronization](./plan-execution.md#task-checklist-synchronization)
mandates:

- One `TaskCreate` per remaining `- [ ]` checkbox, INCLUDING every nested sub-bullet — each
  sub-bullet is its own task, never rolled into its parent. Nesting on disk becomes a flat,
  reading-order sequence of tasks in the list (prefix titles with the repo name for parity runs,
  e.g., `ose-primer: add markdownlint gate to CI`).
- Strict 1:1 mapping both directions: every checkbox has exactly one task; every task has exactly
  one checkbox. Verify `count(remaining checkboxes) == count(created tasks)` before starting.
- The Atomic Sync Ritual governs every completion: tick the checkbox on disk, persist
  implementation notes under it, `TaskUpdate completed` — all three together, never batched,
  never deferred. The on-disk checkbox state never lags more than one `Edit` call behind the
  task state.
- Disk is truth on resume: re-entering the composite rebuilds the Task list from each
  `delivery.md`, never from memory.

**Forbidden** (inherited verbatim from plan-execution Iron Rule 1): coarse tasks ("Execute
Phase 2", "Run repo B"), bulk creation, silent batch completion, speculative completion, title
rewriting. A violation triggers immediate stop, reconciliation (disk wins), and resume one
checkbox at a time.

## Steps

### Step 1 — Planning Phase (Nested Workflow, Sequential)

Run [plan-multi-repo-parity-planning](./plan-multi-repo-parity-planning.md) in full, with
passthrough inputs:

- **Args**: `objective: {input.objective}, repos: {input.repos}, mode: {input.mode},
stage: in-progress, gate-mode: {input.gate-mode}, max-concurrency: {input.max-concurrency}`

All of its steps apply unchanged: parity-set survey, deviation-matrix construction, **first grill
(hard gate — every matrix cell decided)**, conditional web research, **second grill
(post-research)**, per-repo plan authoring via `plan-maker`, per-plan
[plan-quality-gate](./plan-quality-gate.md) to double-zero, and delivery per mode.

**Composite constraints on the nested run**:

- `stage` is fixed to `in-progress` — execution follows immediately, so plans must land in
  `plans/in-progress/<objective-slug>/` in each repo. A backlog parity run does not belong in
  this composite.
- `mode` is restricted to the main-push modes (`main-to-main`, `worktree-to-main`). The
  `worktree-to-pr` mode leaves plans unmerged and execution MUST NOT start on them; if the
  invoker wants PR review, terminate after the planning phase and direct them to the standalone
  workflows.
- Each authored plan MUST carry its `## Worktree` section (the planning workflow's plan-checker
  gate enforces this) — the execution phase depends on it.

**Output**: One gated, delivered plan per target repo at `plans/in-progress/<objective-slug>/`.

**On failure**: Terminate with status `fail`. Do not start the execution phase with a missing or
un-gated plan.

### Step 2 — Phase Gate: Plans Ready for Execution (Sequential, Hard Gate)

Before any execution, verify for EVERY target repo:

1. The plan folder exists at `plans/in-progress/<objective-slug>/` with the five-document layout.
2. The plan reached `pass` on plan-quality-gate (double-zero at the selected gate-mode).
3. The planning-phase commits are on that repo's `origin main` (`git fetch origin && git log
origin/main --oneline -5` shows the plan delivery commits).
4. The plan declares its `## Worktree` section per
   [Plans Organization Convention §Worktree Specification](../../conventions/structure/plans.md#worktree-specification).

**If any check fails for any repo**: STOP. Surface the failing repo and check. Do not execute a
subset silently — the invoker decides whether to fix and re-gate or abandon.

**Output**: All plans verified execution-ready.

### Step 3 — Pre-Execution Grill (Third Grill, Sequential, Hard Gate)

The composite grills three times: the planning phase's matrix grill and post-research grill, then
this pre-execution grill. Invoke the `grill-me` skill per the
[Grilling-With-Options Convention](../../development/workflow/grilling-with-options.md) — every
question presents 2-4 concrete options with trade-offs and exactly one **(Recommended)**; one
question per message; interactive multiple-choice tool when available.

**Mandatory questions** (plus any opened by the answers):

1. **Execution order**: which repo executes first/next/last? Options grounded in the deviation
   matrix (e.g., anchor repo first as reference implementation **(Recommended)** / riskiest repo
   first to surface unknowns early / `{input.execution-order}` as given).
2. **Failure policy**: if repo N's execution ends `partial`/`fail`, do we stop the composite
   **(Recommended)** or continue to repo N+1 and report at the end?
3. **Unresolved design decisions**: per plan-execution's pre-execution requirement, stress-test
   any decision the plans left open — one question per open decision, options from the plan's
   tech-docs.
4. **`[HUMAN]` step availability**: the delivery checklists may contain `[HUMAN]` gates; is the
   invoker available to confirm them during this run, or should execution stop at the first
   `[HUMAN]` item and resume later?
5. **Worktree cleanup preference**: after each repo's archival, plan-execution prompts before
   deleting the plan worktree. Confirm the invoker wants the per-repo prompt (default) or wants
   to pre-decline cleanup for all repos (worktrees retained). Pre-approving silent deletion is
   NOT offered — deletion always requires the per-repo prompt.

**Hard gate**: execution does not begin while any question is unresolved. On invoker abandonment,
terminate with status `fail` — the gated plans remain in `plans/in-progress/` for a later
standalone plan-execution run.

**Output**: Confirmed execution order, failure policy, and resolved open decisions.

### Step 4 — Execution Phase (Per Repo, Sequential, Nested Workflow)

For each repo in the confirmed order, run [plan-execution](./plan-execution.md) in FULL for
`plans/in-progress/<objective-slug>/` in that repo:

- **Args**: `plan-path: plans/in-progress/<objective-slug>/, max-iterations:
{input.max-iterations}, max-concurrency: {input.max-concurrency}`

Every plan-execution rule applies unchanged, including:

- **Per-repo Delivery Mode resolution**: each repo's plan resolves its own
  [`## Delivery Mode`](../../conventions/structure/plans.md#delivery-mode) independently, via the
  standard three-tier precedence (invocation argument > plan field > `worktree-to-pr` default) —
  distinct from this composite's own `mode` input, which governs only the planning-phase delivery
  of the plan **documents** (Step 1). A repo whose plan resolves to a `*-to-pr` delivery mode
  additionally runs the [PR-Review Maker→Fixer Cycle](../pr/pr-review-quality-gate.md) inside
  plan-execution's Step 8 before that repo's `[HUMAN]` merge — its "done" for that repo is a green,
  fully-reviewed, archival-included PR handed off to the human, not a direct push to `origin main`.
  See [plan-execution.md Step 8](./plan-execution.md).
- **Step 0 worktree gate**: enter the plan's designated worktree (provision from the latest
  `origin/main` if missing), sync it with `origin/main` before any implementation.
- **Task list expansion**: append the repo's delivery checklist to the live Task list as
  flattened tasks per the [Granular Task List Contract](#granular-task-list-contract-composite-wide-non-negotiable)
  above, then keep it in sync via the Atomic Sync Ritual for every item.
- **Iron Rules**: granular 1:1 tracking, never stop before all done (except `[HUMAN]` gates),
  fix ALL issues including preexisting, sacred delivery.md, local quality gates before push,
  post-push CI verification, thematic commits, manual behavioral assertions, progress streaming,
  disk-is-truth reconciliation.
- **Validation loop**: `plan-execution-checker` to zero findings (CRITICAL through LOW).
- **Knowledge Capture pre-archival gate**: each repo's plan-execution phase blocks its own
  archival until every `learnings.md` entry is routed-inline, filed-as-backlog-plan, or
  discarded-with-reason and both safety gates pass, per the
  [Knowledge Capture Convention](../../development/quality/knowledge-capture.md) — an attention
  point per repo, not a composite-wide one.
- **Archival**: move the plan to `plans/done/YYYY-MM-DD__<objective-slug>/`, update plan READMEs,
  commit and push.
- **Prompted worktree cleanup**: after the archival commit is pushed and CI is green, verify
  nothing is uncommitted or unpushed, then prompt the user before deleting the worktree —
  honoring the Step 3 cleanup preference.

**Sequencing rule**: one repo at a time. Repo N+1's execution does not start until repo N reaches
`pass` (archived, pushed, CI green) — or, under a continue-on-failure policy from Step 3, until
repo N is explicitly recorded as `partial`/`fail` and the invoker's policy says continue.

**Output per repo**: plan-execution `final-status`, `iterations-completed`, final validation
report.

**On failure**: apply the Step 3 failure policy. Under the default stop policy, terminate the
composite with status `partial` (completed repos stay archived; the failing repo's plan stays in
`plans/in-progress/` with its worktree retained).

### Step 5 — Cross-Repo Finalization (Sequential)

After the last repo's execution completes:

1. **Repair sibling cross-links**: each plan's `## Sibling Plans` section references the other
   repos' plans at `plans/in-progress/<objective-slug>/…`. Archival moved every plan to
   `plans/done/<YYYY-MM-DD>__<objective-slug>/…`. Update each archived plan's sibling links to
   the final `plans/done/` paths, commit per repo
   (`chore(plans): repoint <objective-slug> sibling links to done paths`), and push.
2. **Verify parity outcome**: confirm every repo's plan is archived, every deviation-matrix
   decision was honored in execution (spot-check deviations against the delivered state), and
   each repo's rationale doc landed at the location grilled during planning.
3. **Report**:
   - `plans-created` — final `plans/done/` path per repo
   - `gate-results` — plan-quality-gate status per plan
   - `execution-results` — plan-execution status + iterations per repo
   - `delivery-refs` — commits pushed per repo across both phases
   - Deviation summary — "N deliberate deviations recorded; 0 silent deviations"
   - Worktree disposition per repo — deleted (user-approved) or retained (user choice /
     non-pass status)

**Output**: Composite outcome report. Live Task list fully `completed` and matching disk truth in
every repo.

## Termination Criteria

- **Success** (`pass`): every plan gated to double-zero, executed to zero findings, archived,
  pushed, CI green in every repo; sibling links repaired; every worktree cleaned up or retained
  by explicit user choice
- **Partial** (`partial`): planning phase succeeded but at least one repo's execution ended
  `partial`/`fail`, or a delivery target was not reached; completed repos remain archived,
  failing repos keep their plan in `plans/in-progress/` and their worktree intact
- **Failure** (`fail`): the planning phase failed, the phase gate found a repo not
  execution-ready, or the invoker abandoned any of the three grills

**Per-repo Delivery Mode note**: "archived, pushed" above means a different concrete outcome per
repo depending on that repo's resolved
[`## Delivery Mode`](../../conventions/structure/plans.md#delivery-mode) — a direct push of the
archival commit to `origin main` for the direct-push modes (`worktree-to-origin-main`,
`main-to-origin-main`), or a green, fully-reviewed PR with the archival move committed inside it,
awaiting the `[HUMAN]` merge outside the AI done-boundary, for the `*-to-pr` modes
(`worktree-to-pr`, `main-to-pr`) — see the
[PR-Review Maker→Fixer Cycle](../pr/pr-review-quality-gate.md) done-definition. Because each
repo resolves its delivery mode independently, a single composite run may end with some repos
merged directly and others handed off as open PRs.

## Grilling Contract

This composite is intentionally exhaustive: **three grill sessions, all hard gates**.

1. **Matrix grill** (planning Step 3): every cross-repo deviation decided and justified — no
   authoring with undecided cells.
2. **Post-research grill** (planning Step 5): research findings validated against the decisions —
   no authoring on stale assumptions.
3. **Pre-execution grill** (composite Step 3): execution order, failure policy, open design
   decisions, `[HUMAN]` availability, and worktree cleanup preference — no execution on
   unconfirmed operational decisions.

Every question follows the
[Grilling-With-Options Convention](../../development/workflow/grilling-with-options.md). "We
didn't discuss it" is a workflow failure at every gate.

## Example Usage

### Default: All Three Repos, Plan Then Execute

```
User: "Run plan-multi-repo-parity-planning-and-execution for objective: standardize markdown
       gates across ose-public, ose-primer, and ose-infra"
```

The orchestrator surveys the three repos, builds and grills the deviation matrix, researches and
re-grills, authors and gates three plans, pushes them to each repo's `origin main`, grills the
execution specifics, then executes each plan in its repo's designated worktree (synced to
`origin/main`) one repo at a time — archiving each plan, repairing sibling links, and prompting
before each worktree deletion.

### Two Repos, Custom Order

```
User: "Run plan-multi-repo-parity-planning-and-execution for objective: align agent catalogs
       repos: ose-public, ose-infra"
```

Plans and executes only the two listed repos; the pre-execution grill confirms which runs first.

## Safety Features

- **Everything its constituents guarantee**: gate-before-delivery and no-silent-deviation from
  the planning workflow; worktree isolation + freshness sync, Iron Rules, CI verification, and
  prompted worktree cleanup from the execution workflow
- **Hard phase gate**: no execution on missing, un-gated, undelivered, or worktree-less plans
- **Sequential by default**: one repo executes at a time; cross-repo blast radius is bounded to
  the repo currently in flight
- **Stop-on-failure default**: a failing repo halts the composite unless the invoker explicitly
  chose continue-on-failure in the pre-execution grill
- **No PR-mode execution**: plans awaiting review are never executed by this composite
- **Hook compliance and secrets rule**: every commit in every repo passes that repo's hooks; the
  [No Secrets in Git convention](../../conventions/security/no-secrets-in-committed-files.md) applies in full

## Related Workflows

- [Plan Multi-Repo Parity Planning](./plan-multi-repo-parity-planning.md) — nested as the
  planning phase (Step 1); use it alone when execution should not follow immediately
- [Plan Execution](./plan-execution.md) — nested per repo as the execution phase (Step 4); use it
  alone for plans that already exist
- [Plan Quality Gate](./plan-quality-gate.md) — nested inside the planning phase per plan
- [Plan Planning](./plan-planning.md) — the single-repo analogue of the
  planning phase
- [PR-Review Maker→Fixer Cycle](../pr/pr-review-quality-gate.md) — nested inside
  plan-execution's Step 8 for any repo whose plan resolves to a `*-to-pr` delivery mode

## Principles Implemented/Respected

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**:
  Three hard-gated grills make every cross-repo decision and every operational execution decision
  explicit before work proceeds.
- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**:
  Survey → matrix → grill → research → grill → author → gate → grill → execute is deliberate
  sequencing by construction.
- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)**:
  The full idea-to-archived-parity lifecycle runs as one orchestration instead of four manual
  hand-offs.
- **[Root Cause Orientation](../../principles/general/root-cause-orientation.md)**: The execution
  phase inherits plan-execution's fix-all-issues-including-preexisting rule in every repo.
- **[No Time Estimates](../../principles/content/no-time-estimates.md)**: Describes outcomes and
  gates, never durations.

## Conventions Implemented/Respected

- **[Workflow Naming Convention](../../conventions/structure/workflow-naming.md)**: Filename
  `plan-multi-repo-parity-planning-and-execution` — scope `plan`, qualifiers `multi-repo` +
  `parity` + `planning` + `and`, type `execution` (the composite's terminal deliverable is
  executed, archived plans).
- **[Plans Organization Convention](../../conventions/structure/plans.md)**: Five-document
  layout, `in-progress` staging, worktree specification, executor tagging, and phase gates all
  enforced through the nested workflows.
- **[Worktree Path Convention](../../conventions/structure/worktree-path.md)** and
  **[Worktree Toolchain Initialization](../../development/workflow/worktree-setup.md)**: Every
  worktree lands at `worktrees/<name>/` and is initialized with the two-step toolchain sequence.
- **[Grilling-With-Options Convention](../../development/workflow/grilling-with-options.md)**:
  All three grill sessions present 2-4 concrete options per question; open-ended questions are
  forbidden.
- **[Commit Messages Convention](../../development/workflow/commit-messages.md)**: Conventional
  Commits, thematic splits, in every repo.
- **[CI Monitoring Convention](../../development/workflow/ci-monitoring.md)**: Post-push CI
  verification in the execution phase uses scheduled wake-ups, never tight-loop polling.
- **[Linking Convention](../../conventions/formatting/linking.md)**: GitHub-compatible markdown
  links with `.md` extensions throughout.
- **[Plans Organization Convention §Delivery Mode](../../conventions/structure/plans.md#delivery-mode)**:
  each repo's plan resolves its own delivery mode independently in the execution phase (Step 4),
  distinct from this composite's own planning-phase `mode` input (Step 1).

## Agents

- [plan-maker](../../../.claude/agents/plan-maker.md) — authors each repo's plan (planning phase)
- [plan-checker](../../../.claude/agents/plan-checker.md) /
  [plan-fixer](../../../.claude/agents/plan-fixer.md) — quality gate per plan (planning phase)
- [web-researcher](../../../.claude/agents/web-researcher.md) — conditional research
  (planning phase)
- [plan-execution-checker](../../../.claude/agents/plan-execution-checker.md) — independent
  validation per repo (execution phase)
- [repo-setup-manager](../../../.claude/agents/repo-setup-manager.md) — Phase 0 environment setup
  and baseline per repo (execution phase)
