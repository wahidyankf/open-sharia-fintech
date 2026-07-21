---
name: plan-idea-promotion-planning
title: "plan-idea-promotion-planning"
goal: >
  Promote one ripe two-pager idea brief from plans/ideas/ into a full five-document backlog plan at
  plans/backlog/<identifier>/: gate the brief for completeness, run the deep prior-art study the
  capture phase deferred, then hand the enriched brief to plan-planning (target-stage=backlog) and
  retire the two-pager. The deliverable is the backlog plan, never any implementation.
termination: >
  Either (a) a grill-validated plan exists at plans/backlog/<identifier>/, passes plan-quality-gate
  at strict mode, is pushed to the confirmed target, and the source two-pager is deleted and removed
  from plans/ideas/README.md — promotion is atomic; or (b) the brief is judged not-yet-ripe, a
  readiness report naming the gaps is emitted, and NO plan is created (the legitimate "not promoted
  yet" state). No application or library code is modified either way.
inputs:
  - name: two-pager
    type: string
    description: >
      The idea brief to promote — a slug (e.g. `iam-service-module`) or a path under `plans/ideas/`.
      Must resolve to an existing `plans/ideas/<slug>.md` two-pager (not the folder README).
    required: true
  - name: plan-identifier
    type: string
    description: >
      Slug for the backlog plan folder at plans/backlog/<identifier>/. Defaults to the two-pager's
      own slug, so the idea keeps its name as it becomes a plan.
    required: false
  - name: push-target
    type: string
    description: "Git push destination for the backlog plan. Forwarded to plan-planning."
    required: false
    default: "origin main"
outputs:
  - name: prior-art-report
    type: file
    pattern: generated-reports/plan-idea-promotion-planning__*__report.md
    description: >
      The deep prior-art survey (precedents, standards, existing solutions) produced in Phase 2 and
      folded into the plan's brd.md / prd.md. Written whenever the brief passes the ripeness gate.
  - name: readiness-report
    type: file
    pattern: generated-reports/plan-idea-promotion-planning__*__readiness.md
    description: >
      Section-by-section completeness verdict. Written whenever the brief FAILS the ripeness gate,
      naming exactly which sections are stubs so the author can enrich the brief and retry.
  - name: plan-path
    type: string
    description: Path to the created backlog plan at plans/backlog/<identifier>/ (ripe path only).
  - name: final-status
    type: enum
    values: [pass, partial, fail, not-ripe]
    description: >
      Final status. `not-ripe` when the brief failed the completeness gate and no plan was authored;
      otherwise the status of the backlog plan's quality gate.
---

# Plan Idea Promotion Planning Workflow

**Purpose**: Turn one ripe two-pager in [`plans/ideas/`](../../conventions/structure/plans.md#ideas-folder-two-pagers)
into a full five-document backlog plan, operationalizing the four-step
[Promoting a Two-Pager to a Full Plan](../../conventions/structure/plans.md#promoting-a-two-pager-to-a-full-plan)
procedure end to end. It gates the brief for completeness, runs the deep `web-researcher` prior-art
study that the capture phase deliberately deferred, hands the enriched brief to
[`plan-planning`](./plan-planning.md) with `target-stage=backlog`, and retires the two-pager so the
idea now lives as a plan.

> **The outcome is the plan, not the implementation.** This workflow never writes application or
> library code, never runs a delivery checklist, and never touches `plans/in-progress/`. It produces
> a proposal in `plans/backlog/`. The actual work happens later, only after a human promotes the
> backlog plan to `plans/in-progress/` and runs the [Plan Execution workflow](./plan-execution.md).

This is a `planning`-type workflow: a single forward procedure whose terminal deliverable is a plan
document. It is **not** an iterative quality gate. Per the
[Workflow Naming Convention](../../conventions/structure/workflow-naming.md), the basename parses as
scope=`plan`, qualifier=`idea-promotion`, type=`planning`.

## Execution Mode

**Direct Orchestration** — the calling context (top-level assistant session) orchestrates the
phases, delegating the prior-art survey to `web-researcher` via the Agent tool, running the promotion
checkpoint inline (so the user's conversation is preserved), and invoking the
[plan-planning workflow](./plan-planning.md) for plan authoring. The deep design grill is left to
`plan-planning`'s own grill, seeded by this workflow's handoff, to avoid double-grilling the user.

## When to use

- A two-pager has matured — every section holds a real answer and the only open questions are ones
  that genuinely need a full plan's deeper design/research — and you want it scheduled as a plan.
- A Knowledge-Capture learning captured as a two-pager is now plan-ready.
- You want the deferred deep prior-art study run and folded into the plan as design input in one pass.

Do **not** use it to file a brand-new idea from a raw prompt (that is [`plan-planning`](./plan-planning.md)
directly), nor to execute a plan (that is [`plan-execution`](./plan-execution.md)).

## Phases

### 0. Pre-flight (Sequential)

**Actions**:

- Resolve the `two-pager` input to a concrete `plans/ideas/<slug>.md` path. Accept either a bare
  slug or a path; reject the folder `README.md` and any non-existent path.
- Resolve `plan-identifier` — default to `<slug>` so the idea keeps its name. Confirm no
  `plans/backlog/<identifier>/` already exists (a name clash aborts here).
- Resolve `push-target` (default `origin main`).
- Confirm the working tree is clean per the repo's git-ops method (a bare sibling uses the
  [bare-repo git-ops method](../../development/workflow/bare-repo-landing-method.md); never
  `git rev-parse --is-bare-repository`, in any topology, to answer whether a repository is bare).

**Output**: Resolved brief path, identifier, and push target.

**On failure**: If the brief does not exist or the backlog folder already exists, abort and report.

### 1. Ripeness / Completeness Gate (Sequential, Hard Gate)

Read the two-pager and verify **each** section holds a real answer, applying the convention's rule
that promotion is a **completeness gate, not a perfection gate** — a section may hold honest open
questions, but it may not be a stub, a placeholder, or a `TODO`:

1. Title + one-line summary — a real abstract, not a restated title.
2. Problem / context — a concrete specific example, not an abstract pain point.
3. Why now — a stated urgency/dependency/opportunity.
4. **Prior art / precedents** — at least two named precedents (tool/pattern/standard/prior plan),
   each with a resolving link. Zero prior art on a substantial idea is a smell.
5. Proposed direction (sketch) — core elements a reader immediately grasps.
6. Rough scope & non-goals — in-scope bullets **and** an explicit out-of-scope list.
7. Risks & open questions — named unknowns; **zero open questions is a smell** (over-specified or
   under-thought).
8. What success looks like + promotion signal — an observable/cited/labeled success condition (never
   a fabricated metric).

**If any section is a stub** → the brief is **not ripe**. Write a `readiness-report` to
`generated-reports/` naming exactly which sections fail and why, tell the user the brief needs
enriching first (the legitimate **"not promoted yet"** state, distinct from "rejected"), set
`final-status=not-ripe`, and **terminate without creating any plan**. Do not silently promote a thin
brief.

**Output**: Ripe → proceed. Not ripe → `readiness-report` written, workflow ends.

### 2. Deep Prior-Art Study (Parallel, delegated)

Run the deep prior-art survey the capture phase deferred (per the
[Prior art discipline](../../conventions/structure/plans.md#ideas-folder-two-pagers): "the deep
`web-researcher` prior-art study is deferred to promotion"). The two-pager's own _Prior art_ section
is the lightweight starting point; now the full plan can afford real research.

Delegate to `web-researcher` — the [default primitive for public-web information gathering](../../conventions/writing/web-research-delegation.md).
Fan out **by research angle**, not one agent per link, under the **N+1 model** — `1 main thread + N
background agents = N+1 total`, default **N=3** — per the
[Subagent Orchestration Convention](../../development/agents/subagent-orchestration.md). Angles are
independent DAG nodes (none reads another's output), so the number of angles is the fan-out and N
only caps it. Typical angles:

- **Precedents & patterns** — who has solved this before (named tools, libraries, prior in-repo plans)
  and how; where each falls short for this context.
- **Standards & specifications** — any formal standard, RFC, or convention the idea should conform to
  or deliberately diverge from.
- **Existing solutions & alternatives** — buy-vs-build options, their trade-offs, and licensing.

Each finding must carry a **verified** source (fetched, dated) or be cited name-only when no stable
URL exists — never a fabricated link, inheriting the repo's anti-fabrication rule.

Write the survey progressively to
`generated-reports/plan-idea-promotion-planning__<uuid>__<YYYY-MM-DD--HH-MM>__report.md`
(the `prior-art-report` output) per the [Temporary Files convention](../../development/infra/temporary-files.md).

**Agent**: `web-researcher` (one invocation per angle).

**Output**: `prior-art-report` written — the design input Phase 4 folds into the plan.

### 3. Promotion Checkpoint (Sequential, Hard Gate)

Present, inline: the ripeness confirmation, a digest of the `prior-art-report`, and the two-pager's
own open questions. Then use `AskUserQuestion` (options-first, per the
[Grilling-With-Options Convention](../../development/workflow/grilling-with-options.md)) to:

1. Confirm the `plan-identifier` (default `<slug>`).
2. Confirm the plan structure (default: the five-document multi-file layout).
3. Confirm the `push-target`.
4. **Explicitly approve** promoting this brief to a backlog plan now.

The deep design grilling — resolving the open questions into concrete plan requirements — is **not**
run here; it is left to `plan-planning`'s own grill in Phase 4, seeded by the handoff, so the user is
grilled once, not twice.

**Do NOT proceed to Phase 4** until the user approves. The user may defer (keep it as a two-pager) or
trim scope here.

**Output**: Confirmed identifier, structure, push target, and an explicit go.

### 4. Backlog Plan Establishment (Sequential, nested workflow)

Invoke the [plan-planning workflow](./plan-planning.md) with:

- **Input** `target-stage`: `backlog` (lands at `plans/backlog/<identifier>/`, no date prefix).
- **Input** `push-target`: forwarded from this workflow's input.
- **Input** `prompt`: a self-contained handoff containing —
  - the two-pager's full text (problem, why-now, direction sketch, scope & non-goals, risks & open
    questions, success + promotion signal) carried forward verbatim as the plan's seed;
  - a link to the `prior-art-report` plus its key findings, to be folded into the plan's `brd.md` /
    `prd.md` as design input;
  - the Phase 3 decisions (identifier, structure, scope trims);
  - this **Definition of Done** for the plan it must author: the problem, scope, and open questions
    are carried into `brd.md` / `prd.md`; the deep prior-art findings are folded in; the plan is the
    default five-document layout; it passes `plan-quality-gate` at strict mode.

Because `plan-planning` runs its own grill + research + `plan-maker` + `plan-quality-gate` + push
inside a dedicated worktree, this phase yields a strict-gate-passing backlog plan on the confirmed
target.

**Output**: `plan-path`, `final-status`, `final-report` (from the nested quality gate).

### 5. Two-Pager Retirement (Sequential)

Complete the promotion **move** so the idea now lives as a plan, not as both:

- On the **same branch/worktree** `plan-planning` authored the plan in — before that PR merges, so
  the promotion is **atomic** (the plan appears and the brief disappears together) — `git rm
plans/ideas/<slug>.md` and remove the brief's line from `plans/ideas/README.md`. Commit it as part
  of the plan's changeset.
- If the delivery mode already merged the plan before this step runs, land the deletion as a small
  follow-up commit to the same `push-target`.
- Verify on the target that `plans/ideas/<slug>.md` no longer exists and its README line is gone.

This is step 4 of the convention's promotion procedure. Retiring the brief is **not** optional: a
promoted idea that still sits in `plans/ideas/` is a duplicate.

**Output**: Two-pager deleted and de-indexed on the target.

### 6. Hand-back (Sequential)

Emit a user-visible summary: `plan-path`, the `prior-art-report` path, confirmation that the
two-pager is retired, and `final-status`. Remind the user that the plan is a **proposal in
`backlog/`**; scheduling it is a separate move to `plans/in-progress/` (a pure rename, no date
prefix) followed by the [Plan Execution workflow](./plan-execution.md).

## Gherkin Success Criteria

```gherkin
Feature: plan idea promotion planning

Scenario: A ripe two-pager becomes a backlog plan and is retired atomically
  Given plans/ideas/<slug>.md holds a real answer in every section
  When the workflow runs to completion with the user's approval
  Then a prior-art report appears under generated-reports/plan-idea-promotion-planning__*__report.md
  And a plan exists at plans/backlog/<identifier>/
  And the backlog plan passes plan-quality-gate at strict mode
  And plans/ideas/<slug>.md no longer exists on the push target
  And the brief's line is removed from plans/ideas/README.md
  And no application or library code is modified

Scenario: A thin two-pager is not promoted
  Given plans/ideas/<slug>.md has a stub Risks & open questions section
  When the workflow runs the ripeness gate
  Then a readiness report names the stub section
  And final-status is not-ripe
  And no plan is created
  And the two-pager is left untouched in plans/ideas/

Scenario: The user declines at the promotion checkpoint
  Given the ripeness gate passed and the prior-art report is presented
  When the user does not approve promotion
  Then no plan is authored
  And the two-pager remains in plans/ideas/
```

## Related Documents

- [Plans Organization Convention → Promoting a Two-Pager to a Full Plan](../../conventions/structure/plans.md#promoting-a-two-pager-to-a-full-plan) — the four-step procedure this workflow operationalizes.
- [Plans Organization Convention → Ideas Folder (Two-Pagers)](../../conventions/structure/plans.md#ideas-folder-two-pagers) — the two-pager format and the deferred deep prior-art rule.
- [plan-planning workflow](./plan-planning.md) — invoked in Phase 4 with `target-stage=backlog`.
- [plan-execution workflow](./plan-execution.md) — runs the plan later, after promotion to `in-progress/`.
- [web-researcher Agent](../../../.claude/agents/web-researcher.md) — Phase 2 deep prior-art survey.
- [Knowledge Capture Convention](../../development/quality/knowledge-capture.md) — routes future-work learnings into `plans/ideas/` as two-pagers this workflow later promotes.

## Principles Implemented/Respected

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: The ripeness gate and the deep prior-art study precede any plan; the checkpoint forces an explicit go/no-go.
- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: Ripeness verdict, prior-art findings, and the promotion decision are recorded in writing before the plan is authored.
- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: The workflow composes existing pieces (`web-researcher`, `plan-planning`) rather than duplicating plan-authoring; the user is grilled once.
- **[No Time Estimates](../../principles/content/no-time-estimates.md)**: Outcomes, not durations.

## Conventions Implemented/Respected

- **[Workflow Naming Convention](../../conventions/structure/workflow-naming.md)**: Basename `plan-idea-promotion-planning` parses as scope=`plan`, qualifier=`idea-promotion`, type=`planning`.
- **[Plans Organization Convention](../../conventions/structure/plans.md)**: The backlog plan uses the `<identifier>/` folder form (no date prefix); the two-pager is deleted and de-indexed on promotion.
- **[Web Research Delegation Convention](../../conventions/writing/web-research-delegation.md)**: The deep prior-art study is delegated to `web-researcher`.
- **[Subagent Orchestration Convention](../../development/agents/subagent-orchestration.md)**: Research angles fan out under the N+1 model — `1 main thread + N background agents = N+1 total`, default N=3 — with the main thread kept vacant as orchestrator.
- **[Grilling-With-Options Convention](../../development/workflow/grilling-with-options.md)**: The promotion checkpoint presents concrete options; open-ended questions are forbidden.
- **[Linking Convention](../../conventions/formatting/linking.md)**: Cross-references use GitHub-compatible markdown with `.md` extensions.
