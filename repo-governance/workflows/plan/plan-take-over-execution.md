---
name: plan-take-over-execution
title: "plan-take-over-execution"
goal: Given a path to a plan, discover its true execution state across every candidate repository — local worktrees, local and remote branches, and GitHub PRs — reconcile that state into one authoritative picture, take over any in-flight implementation found rather than restarting it, remove confirmed-stale leftover worktrees/branches/build artifacts, and hand off to plan-execution.md against the reconciled state
termination: Every candidate repo's plan state is classified, all confirmed-stale leftovers are removed (or explicitly held with a reason), and each live or fresh target has been handed to plan-execution.md, which reaches its own termination for that repo
inputs:
  - name: plan-path
    type: string
    description: Path to the plan folder (in plans/backlog/, plans/in-progress/, or plans/done/) in the current repo, or a bare plan-identifier slug when no local folder exists at all (e.g., the plan was only ever committed on a branch or in a sibling repo).
    required: true
  - name: repos
    type: list
    description: >-
      Explicit override of the candidate repo set Phase A1 probes. Default (when omitted): the
      current repo, plus `ose-primer` and `ose-private` whenever they exist as sibling checkouts
      reachable from the same parent directory — this default is a FLOOR, never narrowed below the
      current repo, and widened automatically when the plan's own docs name additional repos in
      scope.
    required: false
  - name: max-concurrency
    type: number
    description: "Background agents run concurrently — the N in the N+1 model (1 main thread + N background agents = N+1 total). Independent repos' discovery probes may fan out up to this bound. Never self-promoted beyond the declared value."
    required: false
    default: 3
outputs:
  - name: takeover-report
    type: file
    pattern: generated-reports/plan-take-over-execution__*__discovery.md
    description: Per-repo raw findings, bucket classification, adopted targets, removed leftovers, and any anomalies escalated (with their resolution, if resolved during the run)
  - name: reconciled-targets
    type: map
    description: Per-repo bucket assignment (nothing-found / already-delivered / live-in-flight / anomaly) and, for live-in-flight repos, the adopted worktree path, branch, and PR number if one exists
  - name: plan-execution-outputs
    type: map
    description: Every output plan-execution.md itself defines, produced once per repo this workflow hands off to
---

# Plan Take-Over Execution Workflow

**Purpose**: Before executing a plan, find out whether it has already been worked — anywhere. This
workflow probes for existing worktrees, branches, and PRs across the current repo and its siblings,
reconciles whatever it finds into one authoritative picture, adopts real in-flight work instead of
reprovisioning over it, cleans up confirmed-stale leftovers, and only then hands off to
[`plan-execution.md`](./plan-execution.md) for the actual remaining delivery work.

**When to use**:

- Resuming a plan after a session boundary, a crash, or a handoff, where it is unknown whether the
  plan already has partial implementation somewhere.
- A plan is suspected to have been worked concurrently by another agent, session, or human — possibly
  in a different repo, since `ose-primer` and `ose-private` are siblings that can carry the same
  plan-identifier.
- Before running `plan-execution.md` cold on a plan-identifier that might already have an open PR, an
  orphaned worktree, or a `delivery.md` copy sitting in more than one location.

**When NOT to use**:

- A brand-new plan that has never been worked — discovery is a guaranteed no-op; invoke
  `plan-execution.md` directly and skip the overhead.
- A plan already confirmed executing in the current, correct worktree with a live Task list in this
  same session — there is nothing to take over; continue in place.

## Relationship to plan-execution.md (no duplication)

This workflow is a **discovery-and-reconciliation layer in front of**
[`plan-execution.md`](./plan-execution.md) — the same relationship
[`multi-plans-execution.md`](./multi-plans-execution.md) has to it as a scheduling layer. Everything
about how a plan executes once its worktree is resolved — [Step 0's freshness
gate](./plan-execution.md#0-enter-the-designated-worktree-sequential-hard-gate), the [Task-Checklist
Synchronization model](./plan-execution.md#task-checklist-synchronization), the [Atomic Sync
Ritual](./plan-execution.md#atomic-sync-ritual), [Resume Reconciliation](./plan-execution.md#resume-reconciliation-disk-is-truth),
the [Iron Rules](./plan-execution.md#iron-rules-non-negotiable), the PR-review cycle, and archival —
is inherited verbatim once handoff happens (Phase E). This document specifies only what a scattered,
possibly-multi-repo, possibly-already-started plan needs before that: a wider-than-single-worktree
search (Phase A), a reconciliation decision procedure (Phase B), takeover of what's found (Phase C),
and a leftover-cleanup pass (Phase D).

## Why This Workflow Exists

Two failure modes already documented elsewhere in this repo's governance motivate it directly:

- A plan's worktree can hold **uncommitted evidence a merged PR doesn't reveal** — a merged PR proves
  the branch landed, not that the working tree is empty (see the [Worktree and Artifact Cleanup
  Convention](../../development/workflow/worktree-and-artifact-cleanup.md#mandatory-pre-removal-checks)'s
  second mandatory check). Starting `plan-execution.md` cold with a freshly-provisioned worktree over
  the same plan-identifier would silently discard that work instead of continuing it.
- Concurrent work on the **same plan-identifier from a different location** — a sibling repo, a
  different worktree, or the primary checkout — is exactly the same-machine assumption every other
  governance doc here treats as ambient truth (see the [No Destructive Git Operations
  Convention](../../development/workflow/no-destructive-git-operations.md#the-same-machine-assumption)).
  `plan-execution.md`'s own Resume Reconciliation item 6 already handles "same repo, two locations
  (primary checkout vs. worktree)"; this workflow generalizes that to "same plan, N repos, unknown
  locations."

Skipping this discovery and starting `plan-execution.md` directly against a bare `plan-path` risks
three concrete outcomes this workflow exists to prevent: (1) **re-implementing** work that already
landed, wasting the effort and creating avoidable merge conflicts against it later; (2)
**abandoning** real uncommitted work in a stale worktree by provisioning a fresh one over it; (3)
**accumulating orphans** — worktrees, branches, and build output left behind by an earlier,
interrupted attempt that nobody ever closed the loop on.

## Execution Mode

**Direct Orchestration** — the calling context is the orchestrator throughout discovery,
reconciliation, cleanup, and handoff, exactly as in `plan-execution.md` and
`multi-plans-execution.md`. There is no delegated discovery agent: the git/`gh` probes in Phase A are
read-only and cheap enough to run directly, and delegating them would add a context hop without
adding judgment.

## Concurrency Model

The same **N+1 model** applies — `1 main thread + N background agents = N+1 total`, default **N=3**,
per the [Agent Workflow Orchestration Convention](../../development/agents/agent-workflow-orchestration.md).
Within one repo, discovery is largely sequential: a found branch name changes what the next probe
searches for (e.g., a discovered PR's `headRefName` narrows the branch-list query), so probes run in
the stated order rather than all at once. Across repos, independent repos' probe sets MAY fan out as
parallel background Tasks up to N when `repos` resolves to more than one entry. Phase D's cleanup
candidates are independent of each other by construction (each is a distinct worktree/branch) and may
also fan out up to N.

## Task List Discipline for This Workflow

The same granular, 1:1 Task-list mapping `plan-execution.md` requires for delivery-checklist items
(see its [Iron Rule 1](./plan-execution.md#iron-rules-non-negotiable)) extends to the phases this
workflow adds before that checklist even loads:

- **One Task per (repo × artifact-class) discovery probe** in Phase A — never one coarse "discover
  state" task. Six artifact classes × N repos is 6N tasks, not one.
- **One Task per Bucket-4 anomaly** raised in Phase B, closed only once the user's resolution is
  recorded (see Phase C step 5) — an anomaly is never silently dropped from the live list.
- **One Task per cleanup candidate** in Phase D — never a single "cleanup" task covering several
  worktrees or branches.
- **Every checkbox Phase C step 5 ticks from discovered evidence gets its own Task too.** If no Task
  yet exists for that checkbox (the common case — discovery runs before any delivery-checklist Task
  list has been materialized), create one, then immediately complete it in the same breath as the
  `delivery.md` edit — the identical pairing `plan-execution.md`'s Atomic Sync Ritual requires mid-execution, applied here at takeover time instead.
- **Phase E rebuilds and resumes `plan-execution.md`'s own per-checkbox Task list per its Step 1**,
  unchanged — this workflow's own discovery/cleanup/reconciliation tasks close out as Phase E's
  handoff begins, not before, and never get silently merged into the delivery-checklist tasks Phase E
  creates next.

**This is harness-agnostic.** Per the [multi-harness binding
model](../../conventions/structure/multi-harness-binding.md), this document is vendor-neutral: "Task
list" here means whatever live task/todo-tracking primitive the executing session's harness exposes
(`TaskCreate`/`TaskUpdate`, or an equivalent primitive under another platform binding). Only the
concrete tool name varies by harness — the 1:1-mapping and immediate-sync requirements above bind
identically regardless of which one is in use.

Sync every task to completion immediately, matching the cadence `plan-execution.md` itself enforces
— no batching several probes', anomalies', or reconciled checkboxes' worth of task closes into one
update.

## Steps

### Phase A — Discover Every Trace of This Plan (Sequential per Repo, Hard Gate)

**A0. Resolve the plan-identifier.** `plan-path` may point at `plans/backlog/<slug>/`,
`plans/in-progress/<slug>/`, a dated `plans/done/<date>__<slug>/`, or — if no local folder exists at
all in the current repo — a bare slug/plan-identifier string. The plan-identifier is the folder's
bare slug (no date prefix), the same string that builds the `worktrees/<plan-identifier>/` path per
the [Worktree Path Convention](../../conventions/structure/worktree-path.md) and, by the convention
already used in multi-repo-parity plans, branch names across repos.

**A1. Resolve the candidate repo set.** Always include: the current repo, plus `ose-primer` and
`ose-private` whenever they exist as sibling checkouts reachable from the same parent directory as
this repo (per [Related Repositories](../../../docs/reference/related-repositories.md)) — this is a
**floor, not a ceiling**. If the plan's own `README.md`/`delivery.md` names other repos in its scope
(an explicit "Affected subrepos and apps" table, or a multi-repo-parity companion plan), add those
too. `beaver-nest`, if present as a sibling checkout, is probed only when the plan or the user names
it explicitly — it sits outside the generic-content parity loop by convention. `TaskCreate` one
discovery task per (repo × artifact-class) pair before probing begins.

**A2. Per repo, in this order, log every hit verbatim** — never summarize a hit away as "probably
stale" at discovery time; that judgment belongs to Phase B, with evidence in hand:

1. **Local worktrees**: `git worktree list --porcelain` from the repo's primary checkout; grep for
   `<plan-identifier>` in the path or branch name.
2. **Local branches**: `git branch --list '*<plan-identifier>*'`.
3. **Remote branches**: `git ls-remote --heads origin '*<plan-identifier>*'` — this finds a pushed
   branch even without a local fetch of that ref.
4. **PRs, open and closed**: `gh pr list --repo <owner>/<repo> --search "<plan-identifier> in:title,body,head" --state all --json number,state,headRefName,mergedAt,url`.
5. **Plan-folder location on `origin/main`**: `git ls-tree -r origin/main --name-only -- 'plans/*<slug>*'` —
   does the folder live in `backlog/`, `in-progress/`, or an already-dated `done/` entry?
6. **On any found worktree or branch**: read its copy of `delivery.md` (if present) and record every
   `- [x]` count plus that location's own `git status --porcelain` output. Never assume a found
   worktree is clean just because it exists.

**A3. Persist raw findings to the takeover-report as they're gathered**, not held in memory only —
this file is the recovery point if the session is interrupted mid-discovery, consistent with the
scratchpad-first defensive posture this repo's own incident history recommends for multi-step work in
a shared checkout.

### Phase B — Reconcile Findings Into One Decision (Sequential, Hard Gate)

For each repo, classify Phase A's findings into exactly **one** bucket. A repo whose evidence matches
more than one bucket, or contradicts itself, is a **hard anomaly** — stop and escalate to the user
with the raw evidence attached; never guess past it.

- **Bucket 1 — Nothing found.** No worktree, branch, PR, or plan-folder trace anywhere. Nothing to
  take over in this repo; Phase E starts it fresh via `plan-execution.md`'s own Step 0 provisioning.
- **Bucket 2 — Already delivered.** The plan folder lives under `plans/done/` on `origin/main`, and
  every PR found (if any) shows `MERGED`. Nothing to take over — surface this to the user, since the
  current invocation may itself be stale (the plan may need no further execution here at all).
- **Bucket 3 — Live in-flight work.** A worktree and/or branch and/or open PR exists, the found
  `delivery.md` shows partial `- [x]` progress, and no signal contradicts another. This is the
  **takeover target** for that repo.
- **Bucket 4 — Anomaly.** Any of: a worktree with no matching branch (orphaned by an earlier
  `git branch -D`); a pushed branch with no worktree and no PR (provisioned, worked, then abandoned
  mid-session); two or more independent worktrees/branches for the same plan-identifier in one repo;
  or a plan folder present in `plans/in-progress/` on `origin/main` with no worktree, branch, or PR
  referencing it anywhere (this can legitimately be plan-docs-only work committed straight to `main`
  under the plan-docs-on-main carve-out — confirm that reading with the user before treating it as an
  anomaly, since it may simply be correct).

More than one repo landing in Bucket 3 is not itself an anomaly — a multi-repo-parity-style plan can
have genuinely independent per-repo progress. Record each repo's takeover target independently; Phase
E hands off to `plan-execution.md` once per Bucket-3 (or fresh Bucket-1) repo.

Emit the full reconciliation table (repo → bucket → evidence) to the user and to the takeover-report
before Phase C begins.

### Phase C — Take Over the Live Work (Sequential per Bucket-3 Repo)

For each repo classified Bucket 3:

1. **Adopt, never reprovision.** If a worktree already exists at `worktrees/<plan-identifier>/`,
   enter it directly — this satisfies `plan-execution.md` Step 0's "if it exists, make it the
   execution root" branch; do not run `git worktree add` again over it. If only a branch or PR exists
   with no local worktree, provision the worktree **from that existing branch**
   (`git worktree add worktrees/<plan-identifier> <branch>`) — never from `origin/main`, which would
   silently discard the branch's real content by starting a sibling history instead of continuing it.
2. **Apply the freshness gate exactly as `plan-execution.md` Step 0.5 states it**: `git fetch origin`;
   if the adopted worktree has uncommitted changes, do NOT auto-stash or discard — surface the dirty
   state and STOP for the user's explicit direction (commit, stash, or hold as-is), per [No
   Destructive Git Operations](../../development/workflow/no-destructive-git-operations.md). If the
   branch carries commits not yet on `origin/main`, `git rebase origin/main`; on conflict, abort and
   surface the conflicting files rather than auto-resolving — identical to `plan-execution.md`'s own
   rule.
3. **Rebuild the file-touch ledger from the adopted branch**, per `plan-execution.md`'s own [Resume
   Reconciliation item 7](./plan-execution.md#resume-reconciliation-disk-is-truth): reconstruct it
   from the branch's `git log` commit list, each ticked checkbox's implementation-notes `Files
Changed` block, and (if recoverable) a prior session's transcript. Until the ledger is rebuilt,
   every modified or untracked path in the adopted worktree is treated as foreign, per [File-Touch
   Discipline](../../development/practice/file-touch-discipline.md).
4. **If a PR already exists for this branch**, record its number, state, and CI status
   (`gh pr checks <number>`) — `plan-execution.md`'s Step 2b/2c push-and-CI logic resumes against
   this PR at the plan's next delivery boundary rather than opening a duplicate one.
5. **Reconcile `delivery.md` to the discovered ground truth before Phase E hands off.** The adopted
   copy's `delivery.md` is the resume basis, but Phase A's cross-repo search can surface completed
   work that copy doesn't yet reflect — a further-along PR found in a different repo for the same
   multi-repo-parity plan, a sibling worktree whose `delivery.md` has more `- [x]` items ticked for a
   shared checkbox, or a change that plainly landed (verified in Phase A2's diff/PR read) without its
   Atomic Sync Ritual ever completing. For every such discovered fact, apply the identical [Atomic
   Sync Ritual](./plan-execution.md#atomic-sync-ritual) `plan-execution.md` uses mid-execution — tick
   the checkbox, add an implementation-notes block citing the discovery evidence (which repo, branch,
   commit, or PR it came from), matching `TaskUpdate` — rather than leaving `delivery.md` stale and
   letting `plan-execution.md`'s own Resume Reconciliation under-count progress at Step 1. **Tick only
   from positive evidence gathered in Phase A** (a `MERGED` PR, a `- [x]` line actually present in a
   discovered copy, a diff that proves the described change already landed) — never from inference.
   A Bucket-4 anomaly the user resolved during Phase B also gets a note here, so a future resume sees
   why the state looks the way it does rather than re-discovering the same anomaly cold.

### Phase D — Clean Up Confirmed-Stale Leftovers (Sequential, After Every Repo Is Classified)

This phase runs only **after** Phase B has classified every candidate repo — cleaning up before
reconciliation completes risks removing evidence Phase B still needs. Bucket-4 anomalies are excluded
from this phase entirely; an anomaly is resolved with the user first and never auto-cleaned.

For every worktree/branch Phase A found that is **not** the Bucket-3 target Phase C adopted:

1. Run the full [Worktree and Artifact Cleanup Convention](../../development/workflow/worktree-and-artifact-cleanup.md#mandatory-pre-removal-checks)
   five-check pre-removal sequence per candidate, without shortcuts: merge-state via
   `gh pr list --head <branch> --state all --json number,state,mergedAt` (never ancestry — squash
   merges make ancestry report false negatives), a read of the worktree's own dirty diff, an
   unpushed-commit check (`git log origin/<branch>..<branch>`), confirmation this workflow — not
   another live actor — has grounds to call it idle, and only then a non-force `git worktree remove`.
2. Branch deletion follows the same convention's [Branch
   Cleanup](../../development/workflow/worktree-and-artifact-cleanup.md#branch-cleanup) section —
   `git branch -d` (never `-D`) locally, `git push origin --delete` remotely, and only once the check
   above confirms `MERGED` or the user has explicitly signed off on abandoning it.
3. Build-artifact cleanup is scoped to output produced **inside the removed worktree only**
   (`target/`, `dist/`, `.next/`) — never a shared cache. See the same convention's
   [Build-Artifact Cleanup](../../development/workflow/worktree-and-artifact-cleanup.md#build-artifact-cleanup)
   section and the [Build-Artifact Sweeper Convention](../../development/infra/build-artifact-sweeper.md)
   for what the environment already reclaims on its own schedule — do not rebuild output solely to
   delete it if it is already gone.
4. `TaskCreate`/`TaskUpdate` one task per candidate, per the granularity rule stated above.
5. Log every removal (or explicit skip, with a stated reason) to the takeover-report.

A candidate this phase cannot positively confirm idle — the Cleanup Convention's fifth check, "no
positive evidence, only absence of evidence of activity" — is left in place and reported to the user,
never removed on a default-to-delete basis.

### Phase E — Hand Off to plan-execution.md (Sequential)

1. For each repo with a resolved Bucket-3 target (or a fresh Bucket-1 start), invoke
   [`plan-execution.md`](./plan-execution.md) with `plan-path` set to that repo's plan folder and the
   work branch/worktree already entered per Phase C. This satisfies its Step 0 entirely — the
   worktree gate has already passed and the freshness gate has already been applied — so execution
   begins directly at its [Step 1 (Load Delivery Checklist and Materialize Task
   List)](./plan-execution.md#1-load-delivery-checklist-and-materialize-task-list-sequential), which
   performs its own Resume Reconciliation against the now-current `delivery.md`.
2. If more than one repo resolved to Bucket 3 (or Bucket 1), run each repo's `plan-execution.md`
   invocation as an independent branch of work — the same DAG-first, N+1-bounded fan-out
   `plan-execution.md` and `multi-plans-execution.md` already use, since each repo's execution is
   independent of the others' once its own worktree is adopted.
3. Close the takeover-report with a final summary: repos probed, buckets assigned, worktrees/branches
   adopted, worktrees/branches/artifacts removed, and any anomalies escalated together with their
   resolution (if resolved during this run). This report is this workflow's terminal deliverable,
   alongside whatever `plan-execution.md` itself produces per repo handed off.

## Related Documentation

- [Plan Execution](./plan-execution.md) — the workflow this one hands off to; owns everything about
  single-plan delivery once the worktree is resolved.
- [Multi-Plans Execution](./multi-plans-execution.md) — the sibling scheduling-layer workflow, for
  executing several distinct plans together rather than reconciling one plan's scattered state.
- [Worktree and Artifact Cleanup Convention](../../development/workflow/worktree-and-artifact-cleanup.md) —
  the five-check pre-removal sequence and branch/build-artifact cleanup rules Phase D applies without
  modification.
- [No Destructive Git Operations Convention](../../development/workflow/no-destructive-git-operations.md) —
  bounds every action Phase C and Phase D may take; the "verify, never assume idle" standard both
  phases inherit.
- [File-Touch Discipline](../../development/practice/file-touch-discipline.md) — the ledger-rebuild
  method Phase C.3 applies.
- [Worktree Path Convention](../../conventions/structure/worktree-path.md) — the
  `worktrees/<plan-identifier>/` layout Phase A's search and Phase C's adoption both depend on.
- [Related Repositories](../../../docs/reference/related-repositories.md) — the sibling-repo set
  Phase A1's floor is drawn from.
- [Agent Workflow Orchestration Convention](../../development/agents/agent-workflow-orchestration.md) —
  the N+1 model and same-machine assumption this workflow's cross-repo probing and cleanup both
  operate under.
- [Plans Organization Convention](../../conventions/structure/plans.md) — plan folder structure,
  worktree specification, and delivery-mode definitions this workflow reads to resolve `plan-path`.
