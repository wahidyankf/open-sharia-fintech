---
name: plan-multi-repo-parity-planning
title: "plan-multi-repo-parity-planning"
goal: Author aligned-but-deliberately-divergent plans across multiple sibling repositories for a shared objective, with every cross-repo deviation grilled, decided, and durably documented
termination: "One plan per target repo exists, each passes plan-quality-gate (double-zero), every deviation-matrix cell carries a recorded decision, research findings are incorporated or skipped with justification, and delivery completed per the selected mode"
inputs:
  - name: objective
    type: string
    description: "The shared topic to standardize or align across repos (e.g., 'standardize markdown gates', 'align agent catalogs')"
    required: true
  - name: repos
    type: string
    description: "Comma-separated target repository names or absolute paths in the parity set (e.g., 'ose-public, ose-primer, ose-infra')"
    required: false
    default: "ose-public, ose-primer, ose-infra"
  - name: mode
    type: enum
    values: [main-to-origin-main, worktree-to-origin-main, worktree-to-pr]
    description: "Where plans are authored and how they are delivered (see Modes section)"
    required: false
    default: worktree-to-pr
  - name: stage
    type: enum
    values: [in-progress, backlog]
    description: "Plan stage folder in each target repo"
    required: false
    default: in-progress
  - name: gate-mode
    type: enum
    values: [lax, normal, strict, ocd]
    description: "Mode passed through to plan-quality-gate for each plan"
    required: false
    default: strict
  - name: max-concurrency
    type: number
    description: "Background agents run concurrently — the N in the N+1 model (1 main thread + N background agents = N+1 total). Raise only when independent work, machine capacity, and budget headroom all allow; lower under budget, runner, or disk pressure. Never self-promoted beyond the declared value."
    required: false
    default: 3
outputs:
  - name: plans-created
    type: file-list
    description: One plan folder path per target repo
  - name: deviation-matrix
    type: file
    description: "Cross-repo decision matrix (every gap mapped to an align/deviate decision with justification), embedded in each plan's tech-docs.md and mirrored in each repo's explanation rationale doc"
  - name: gate-results
    type: string
    description: "plan-quality-gate final status per plan (pass/partial/fail)"
  - name: delivery-refs
    type: string
    description: "Commits pushed to origin main (main-push modes) or PR URLs (worktree-to-pr)"
---

# Plan Multi-Repo Parity Planning Workflow

**Purpose**: Orchestrate the creation of parallel plans across multiple sibling repositories for a
shared objective (such as standardizing commands, aligning agent catalogs, or expanding CI gates),
grilling the invoker relentlessly about cross-repo gaps and deviations so that every difference
between the resulting plans is intentional, decided, and durably recorded. The defining
characteristic of this workflow is its grilling contract: no plan authoring begins while any
cross-repo difference remains unexamined. The result is NOT a set of 1-to-1 identical plans
— it is a set of plans whose every divergence from each other is intended and documented.

**Motivating precedent**: The markdown-gate-coverage-expansion parity effort (2026) produced plans
in three sibling repositories. Each repo had a different starting state: different CI configurations,
different gate coverage, different toolchain constraints. The aligned-but-divergent plans that
resulted from that effort — each tuned to its repo's reality, each cross-linking the others, each
documenting why it differed — demonstrated the pattern this workflow formalizes.

**When to use**:

- When the same structural improvement is needed across multiple sibling repos but each repo may
  need a different implementation path
- When you want to avoid silent drift between repos that are supposed to move in parallel
- When the cross-repo decision surface is large enough that ad-hoc grilling would miss cells
- When the invoker can be in any one of the parity repos at invocation time

## Execution Mode

**Preferred Mode**: Agent Delegation — invoke `plan-maker` for authoring each plan (Step 6) and
delegate `plan-quality-gate` for each gated plan (Step 7) via the Agent tool with `subagent_type`.
`plan-maker`, `plan-checker`, and `plan-fixer` run as delegated agents; file changes persist to the
actual filesystem. See [Workflow Execution Modes Convention](../meta/execution-modes.md).

**Fallback Mode**: Manual Orchestration — execute workflow logic directly using Read/Write/Edit
tools in the main context when Agent Delegation is unavailable. Manually follow the plan-quality-gate
steps for each plan.

**How to Execute**:

```
User: "Run plan-multi-repo-parity-planning for objective: standardize markdown gates"
```

The orchestrator:

1. Surveys each target repo's current state relative to the objective
2. Builds and presents the deviation matrix
3. Grills the invoker until every matrix cell has a recorded decision; establishes the
   research-needed flag
4. Delegates external research to `web-researcher` (conditional on research-needed flag)
5. Grills the invoker again with research findings to validate and close any new decision branches
6. Delegates plan authoring to `plan-maker` per repo
7. Runs `plan-quality-gate` per plan until double-zero
8. Delivers per the selected mode and reports outcomes

### Parallel Propagation Shape

The repos form a propagation fan-out, not a chain: **`ose-public` is the source of truth**, and
`ose-primer` and `ose-infra` are independent downstream targets. Once the upstream decision is
recorded, the two downstream repos are **independent DAG nodes** — author and deliver them in
parallel under the N+1 model (`1 main thread + N background agents`, default **N=3**), never
serialized behind one another. `ose-infra` does not participate in the parity loop for content it
does not carry.

The one hard serialization: **`apps/rhino-cli` must stay byte-identical across all three repos**, so
plans touching it propagate one repo at a time rather than concurrently.

### Delivery Shape Per Repo

Each repo's plan is authored to the `worktree-to-pr` default, and each independent phase lands as
its **own PR** — a strict **one worktree → one branch → one PR → one node** mapping, merged
per-phase rather than batched at the end. Partial work reaches `main` merged-but-dark behind a
**feature flag**; a phase lands unflagged only when it ships no user-reachable behaviour change and
the step names that exemption. See
[plan-planning §Planning Granularity](./plan-planning.md#planning-granularity) for the full rule,
including per-phase PR granularity and the named flag-removal step.

### Shared-Machine Safety

All three repos share one machine's disk and git object store, and two of them are bare repos driven
through worktrees. Every git action here is therefore bound by the **no-destructive-git** rule:
never run an operation that discards a concurrent actor's uncommitted work, and never remove a
worktree or branch you did not create. See
[No Destructive Git Operations](../../development/workflow/no-destructive-git-operations.md) and
[Worktree and Artifact Cleanup](../../development/workflow/worktree-and-artifact-cleanup.md).

## Invocation Point

This workflow runs from the anchor repo — whichever repo in the parity set the invoker is
currently working in. The other repos are sibling repos discovered relative to the anchor. The
workflow discovers sibling repo paths from the invoker's environment (absolute paths, a shared
parent directory, or an explicit `repos` input). When paths are ambiguous, the first grilling
round confirms them before any repo is accessed.

All steps treat every target repo identically regardless of which repo anchors the run. The
anchor repo has no special authority over other repos' plans.

## Modes

### `main-to-origin-main`

Author plans directly in the `main` working tree of each repo. Commit and push to `origin main`
of each repo. Use when worktrees are not needed and direct main-branch access is acceptable for
all repos in the parity set. **Unavailable for any bare-repo parity target** (`ose-primer`,
`ose-infra` today) — a bare repo has no `main` working tree to author directly in. See
[Note on bare-repo parity targets](#worktree-to-pr-default) below for the worktree-based
alternative and the full rationale.

### `worktree-to-origin-main`

Author plans in a worktree per repo. If the invoker is not already in a worktree when the
workflow starts, provision one for each target repo:

```bash
# Per repo: from repo root
git worktree add worktrees/<objective-slug> main
cd worktrees/<objective-slug>
npm install
npm run doctor -- --fix
```

Worktrees land at `worktrees/<objective-slug>/` per the
[Worktree Path Convention](../../conventions/structure/worktree-path.md). The two-step toolchain
initialization (`npm install` then `npm run doctor -- --fix`) is required per the
[Worktree Toolchain Initialization](../../development/workflow/worktree-setup.md)
practice. Commit in the worktree branch, push to `origin main` of each repo, then remove the
worktree after delivery.

### `worktree-to-pr` (Default)

Same worktree provisioning as `worktree-to-origin-main`, but commit to a branch
`plan/<objective-slug>` and push that branch. Create a PR per repo with `gh pr create` only if no
open PR for that branch exists yet; otherwise push to the existing PR branch:

```bash
# Check for existing PR
gh pr list --head plan/<objective-slug>

# Create if none exists
gh pr create --title "plan: <objective> parity" --body "..." --draft
```

This is the repo-wide default (see
[AGENTS.md §Git Workflow §Delivery Mode](../../../AGENTS.md#delivery-mode)): a formal review step
happens before plans land on `main`, mirroring the same rationale for the sibling per-plan
`## Delivery Mode` field these plans separately declare (see
[Relationship to Each Repo's Own `## Delivery Mode`](#relationship-to-each-repos-own--delivery-mode)
below).

**Note on bare-repo parity targets (`ose-primer`, `ose-infra`)**: When a bare repo is a parity
target, propagation to it can be delivered EITHER as a draft PR OR as a direct push to its `main`,
both through a worktree. The delivery mode is the caller's per-run choice, independent of this
workflow's own `worktree-to-pr` default, so selecting `worktree-to-origin-main` for a bare target is
a first-class choice, not a deviation. `ose-primer` and `ose-infra` are both **bare** repositories
with no primary checkout, so the two `main-to-*` modes (`main-to-origin-main`, `main-to-pr`) are
unavailable for either — every mutation against a bare target flows through a worktree, per the
[Bare-Repo Base-Worktree Landing Method](../../development/workflow/bare-repo-landing-method.md).
The grilling in Step 3 MUST surface the delivery-mode choice explicitly and record the invoker's
decision before proceeding.

### Relationship to Each Repo's Own `## Delivery Mode`

The three modes above govern how THIS workflow delivers the **plan documents** it authors — a
planning-phase concern. They are distinct from the
[Plans Organization Convention §Delivery Mode](../../conventions/structure/plans.md#delivery-mode)
field (`worktree-to-pr`, `worktree-to-origin-main`, `main-to-origin-main`, `main-to-pr`) that each
authored plan separately declares for its own **future execution** by
[plan-execution](./plan-execution.md) — an execution-phase concern layered on top of whichever mode
delivered the plan document itself.

Because this workflow produces one independent plan document per repo, each repo's own
`## Delivery Mode` is resolved independently, per that repo's own plan and its own
`## Worktree`/`## Delivery Mode` declaration, using the standard three-tier precedence (invocation
argument > plan field > `worktree-to-pr` default). Repos in the same parity set are free to diverge
here — for example, `ose-infra` may resolve to `worktree-to-origin-main` (the only direct-push mode
a bare repo can use — `main-to-origin-main` needs a primary checkout `ose-infra` does not have)
while `ose-public` resolves to `worktree-to-pr` — exactly like any other per-repo deviation this
workflow grills and records in the deviation matrix (Step 2). See Step 6 item 8 below for how
`plan-maker` receives this instruction per repo.

## Steps

### Step 1 — Parity-Set Survey (Per Repo, Parallelizable)

Survey each target repo's current state relevant to the objective. Work empirically: read the
configs, grep the files, run the tools — do not trust docs alone.

**Scope of survey** (adapt to the objective's domain):

- Relevant commands (package.json scripts, Nx targets, Makefile rules, shell scripts)
- Configuration files that govern the objective's domain (CI YAML, lint configs, markdownlint,
  prettier, etc.)
- Agent definitions and workflow files that touch the objective's domain
- Plans already in `plans/in-progress/` or `plans/backlog/` addressing the same area
- Governance docs (conventions, development practices) the objective would affect
- Repo-specific constraints: CI runner type (self-hosted vs GitHub-hosted), private vs public
  visibility, language stack, existing toolchain, dual-CLI parity guards
- **rhino-cli byte-identity check** (whenever the objective touches `apps/rhino-cli` or its Gherkin
  behavior tree): diff the `md5` manifest of `apps/rhino-cli`'s tracked files plus every
  `.feature`/`README.md` under `specs/apps/rhino/behavior/rhino-cli/gherkin/**` across all three
  repos —

  ```bash
  git -C ose-public ls-files apps/rhino-cli specs/apps/rhino/behavior/rhino-cli/gherkin \
    | grep -E '(apps/rhino-cli/.*|gherkin/.*\.feature$|gherkin/.*README\.md$)' | sort \
    | xargs md5 -q > /tmp/public.md5
  git -C ose-primer ls-files apps/rhino-cli specs/apps/rhino/behavior/rhino-cli/gherkin \
    | grep -E '(apps/rhino-cli/.*|gherkin/.*\.feature$|gherkin/.*README\.md$)' | sort \
    | xargs md5 -q > /tmp/primer.md5
  git -C ose-infra ls-files apps/rhino-cli specs/apps/rhino/behavior/rhino-cli/gherkin \
    | grep -E '(apps/rhino-cli/.*|gherkin/.*\.feature$|gherkin/.*README\.md$)' | sort \
    | xargs md5 -q > /tmp/infra.md5
  diff /tmp/public.md5 /tmp/primer.md5
  diff /tmp/public.md5 /tmp/infra.md5
  ```

  (or compare directly against the frozen `plans/done/*/audit/06-canonical-manifest.md` if one
  exists). Any diff is drift that MUST become its own deviation-matrix row in Step 2 — surface it
  before grilling, never silently re-sync it.

**Output**: A per-repo state inventory. Every dimension the objective touches is inventoried for
every repo. Document what exists, what is absent, and any repo-specific constraint that will
affect what the plan must contain.

**Success criteria**: Every target repo has a state inventory covering all dimensions the
objective touches.

**On failure**: Surface the dimension or repo where the survey failed. Do not proceed to Step 2
until all inventories are complete.

### Step 2 — Gap and Deviation Matrix Construction

Diff the per-repo inventories dimension-by-dimension. Build the deviation matrix.

Each row represents one dimension where repos differ or where the objective forces a choice. Row
schema:

| Dimension | Current state per repo | Candidate resolutions                                 |
| --------- | ---------------------- | ----------------------------------------------------- |
| `<name>`  | `repo-A: X, repo-B: Y` | `align-to-X / align-to-Y / per-repo-deviation / drop` |

**Hard rule**: No dimension may be left out of the matrix because it seems obvious or minor.
Every cross-repo difference is a matrix row. Implicit alignment is a workflow failure.

Meta-dimensions to include alongside technical dimensions:

- **Rationale doc location**: where each repo's `docs/explanation/<objective-slug>-parity-decisions.md`
  (or closest equivalent) will be created (app-scoped `apps/<app>/docs/`, lib-scoped
  `libs/<lib>/docs/`, repo governance tree, etc.)
- **ose-primer delivery mode**: which delivery mode (draft PR vs. direct push to `ose-primer:main`)
  the selected parity mode implies for the primer — both are first-class, caller-chosen, neither
  default (applies when ose-primer is in the parity set)
- **Repo-specific constraints**: any repo constraint (private visibility, self-hosted CI runner,
  dual-CLI parity guard, missing toolchain) that forces a per-repo deviation

**Output**: A complete deviation matrix. Every row has a dimension name, the current state per
repo, and candidate resolutions. No row is decided yet — decisions happen in Step 3.

**Success criteria**: Matrix covers every cross-repo difference and every meta-dimension above.

**On failure**: Return to Step 1 and extend the survey for the missing dimension.

### Step 3 — First Grill (Iterative, Blocking, Hard Gate)

Present the deviation matrix to the invoker. Grill every matrix row to a recorded decision.

**Grilling protocol** (per the
[Grilling-With-Options Convention](../../development/workflow/grilling-with-options.md)):

- Each question presents **2-4 concrete options** with trade-off descriptions. One option is
  marked **(Recommended)**.
- Options are grounded in the inventories from Step 1. No invented options.
- One question per message. Fully resolve each before the next.
- Use an interactive multiple-choice tool (e.g., `AskUserQuestion`) when available; fall back
  to the markdown format only when the tool is unavailable.

**For each matrix row, record**:

- The chosen resolution (align-to-X / per-repo-deviation / drop)
- For deviations: the justification (why this repo differs from the others)
- For alignment: which repo's approach becomes the standard and why

**Iterative**: Answers in round N may open new rows. Grill again. Continue until every row is
resolved and no new rows remain.

**Hard gate**: The workflow MUST NOT proceed to Step 6 while any matrix cell lacks a recorded
decision. "We didn't discuss it" is a workflow failure.

**Research-needed flag**: Before closing this grill, establish whether external research is
required before authoring. Ask explicitly: are there harness or vendor conventions, library or
tool behavior claims, or cross-repo prior art that need verification? Record the invoker's answer
as the research-needed flag (yes / no). This flag governs whether Step 4 runs or is skipped.

**Mandatory meta-questions** (surface these explicitly regardless of mode):

1. If any bare repo with no primary checkout — currently `ose-primer` and `ose-infra` — is in the
   parity set: "The bare-repo sync convention allows EITHER a draft PR OR a direct push to
   `<repo>:main`, both delivered through a worktree since the target has no primary checkout to work
   in directly — that per-destination choice is not settled by this workflow's own `worktree-to-pr`
   default, so it must be chosen explicitly. The selected parity mode implies {draft PR | direct push
   to main}. Please confirm the delivery mode for `<repo>`."
   Options: (A) Direct push to `main` via a worktree (`worktree-to-origin-main`). (B) Draft PR
   (`worktree-to-pr`). `main-to-origin-main` is never offered here — it requires a primary checkout
   the bare target does not have. Record the chosen mode.
2. Rationale doc location per repo (where does `<objective-slug>-parity-decisions.md` live in
   each repo?).
3. Any repo-specific constraint flagged in Step 2 that forces a deviation.
4. Research-needed flag: are there external claims (harness/vendor conventions, library/tool
   behavior, prior art) that require verification before authoring the plans?

**Output**: A fully resolved deviation matrix. Every row has a recorded decision and — for
deviations — a recorded justification. Research-needed flag recorded. This matrix is the source
of truth for all authoring in Step 6.

**On invoker abandonment**: Terminate workflow with status `fail`. Partial grilling produces no
value; do not author plans with unresolved matrix rows.

### Step 4 — Web Research (Sequential, Conditional)

Delegate external research to `web-researcher` to verify claims and gather authoritative
sources before plan authoring begins.

**Skip condition**: Skip if ALL hold:

1. The objective is a purely internal governance or structural change with no external claims
2. No harness/vendor conventions, library versions, tool behavior, or cross-repo prior art need
   verification
3. The invoker confirmed in Step 3 that no research is needed (research-needed flag = no)

If skipping: emit `Step 4 skipped — no external research needed (confirmed in Step 3).`

**If NOT skipping**:

Invoke `web-researcher` via the Agent tool. Provide a focused research prompt covering:

- Vendor or harness conventions the objective touches (e.g., CI runner behavior, tool API
  contracts, platform-specific constraints)
- Prior art: has anyone formalized this cross-repo alignment pattern? Known failure modes?
- Library or tool behavior referenced in the objective (versions, API signatures, caveats)
- Risks or caveats not surfaced in the Step 1 inventories

**Agent**: `web-researcher`

**Output**: Cited, structured research findings. Passed to Step 5 grill and included in the
`plan-maker` handoffs in Step 6. If skipped, the skip line is included in Step 6 handoffs
in place of research findings.

### Step 5 — Second Grill (Post-Research, Sequential)

Present research findings and grill again to validate direction and close any new decision
branches opened by the research.

**Orchestrator action**:

1. Summarize research findings from Step 4 (or confirm skipped)
2. Invoke the grilling protocol. Every question MUST follow the
   [Grilling-With-Options Convention](../../development/workflow/grilling-with-options.md):
   2-4 concrete options, explicit trade-offs, exactly one Recommended, native interactive tool
   when available. Cover:
   - Do the research findings change any decision from Step 3? (options: yes — which decision /
     no — proceed as agreed / partial — one or more decisions need refinement)
   - Are there new constraints or trade-offs surfaced by the research that apply to one or more
     repos differently?
   - Does the proposed cross-repo alignment approach still hold after checking authoritative
     sources?
   - Are there risks the invoker wants to explicitly accept or mitigate in the plans?
3. Matrix rows may be added or updated based on findings — every new or changed row requires a
   recorded decision before proceeding
4. Confirm the updated direction before proceeding to Step 6

**Do NOT proceed to Step 6** until all branches from this grill are resolved and mutual
understanding is confirmed incorporating research.

**Notes**:

- If research was skipped in Step 4, this is a brief confirmation pass, not a full grill session
- All new branches must be resolved before invoking `plan-maker`

**Output**: Final direction confirmed. Research findings integrated into the deviation matrix.
Every matrix row (original and new) carries a recorded decision.

### Step 6 — Plan Authoring (One Plan Per Repo)

Author a five-document plan (`README.md`, `brd.md`, `prd.md`, `tech-docs.md`, `delivery.md`)
in each target repo per the
[Plans Organization Convention](../../conventions/structure/plans.md).

**Stage-aware folder naming**:

- `stage=in-progress` → `plans/in-progress/<objective-slug>/` (no date prefix)
- `stage=backlog` → `plans/backlog/<objective-slug>/` (no date prefix)

**Agent**: `plan-maker` (invoked per repo via the Agent tool)

Provide a self-contained handoff prompt per repo covering:

1. Objective (verbatim from input)
2. Resolved decisions from Steps 3 and 5 (the full deviation matrix with recorded decisions)
3. Research findings from Step 4 (cited) — or note that research was skipped
4. This repo's specific deviations and their justifications
5. Confirmed plan folder path (per stage above)
6. Cross-links to the sibling plans in the other repos (even if those plans are not yet
   authored — use the expected paths)
7. Delivery mode (from `mode` input) — this governs how the **plan document** itself is delivered
   (see [Modes](#modes) above), distinct from the plan's own `## Delivery Mode` declaration below
8. **Instruction for `plan-maker`** to declare this repo's own
   [`## Delivery Mode`](../../conventions/structure/plans.md#delivery-mode) field in the authored
   plan — the four-mode vocabulary (`worktree-to-pr` default, `worktree-to-origin-main`,
   `main-to-origin-main`, `main-to-pr`) governing that plan's own future execution, resolved
   independently per repo through the standard three-tier precedence (invocation argument > plan
   field > default) and recorded as its own deviation-matrix row when it diverges from sibling
   repos. For a bare-repo target (`ose-primer`, `ose-infra` today), the two `main-to-*` values are
   unavailable — see
   [Plans Organization Convention §Delivery Mode](../../conventions/structure/plans.md#delivery-mode)
   for the authoritative restriction, which governs this field independently of the restriction
   [Modes](#modes) above places on this workflow's own 3-value vocabulary. A repo whose plan
   resolves to a `*-to-pr` mode additionally runs the
   [PR-Review Maker→Fixer Cycle](../pr/pr-review-quality-gate.md) during its own execution.

Each plan MUST include:

**(a) Full deviation matrix** with justifications in `tech-docs.md`. Every row from the Steps 3
and 5 output appears verbatim, including the chosen resolution and justification for any
deviation.

**(b) Cross-links to sibling plans** in each of the other target repos. Use the expected paths
at the agreed stage. Example (from a plan at `plans/in-progress/foo/README.md`):

```markdown
## Sibling Plans

This plan is part of a parity set. See sibling plans for context:

- `ose-primer`: `plans/in-progress/foo/README.md`
- `ose-infra`: `plans/in-progress/foo/README.md`
```

**(c) Delivery checklist item** to write a decision-rationale document at the agreed location per
Step 3 (e.g., `docs/explanation/<objective-slug>-parity-decisions.md`) explaining why each
decision was taken — especially deviations. The exact path is the grilled value from Step 3.

**(d) Delivery checklist item** to update any governance or convention docs the decisions touch
(e.g., if a decision changes a CI gate threshold, the relevant convention doc must be updated
as part of executing the plan).

**(e) Knowledge Capture phase**: `plan-maker` emits the standard Knowledge Capture phase plus a
`learnings.md` scaffold per repo plan, exactly as it does for single-repo plans. Any learning
surfaced during THIS parity-planning process itself (survey, grilling, research) that is
generalizable also flows through the triage rubric in the
[Knowledge Capture Convention](../../development/quality/knowledge-capture.md) before the
corresponding plan is archived.

**Plans are plans only**. This workflow never implements the objective. The type `planning`
means the terminal deliverable is a validated plan document in `plans/` — not code, not config
changes, not convention edits. Execution of the objective is downstream work performed later by
the [plan-execution workflow](./plan-execution.md).

**Agent**: `plan-maker`

**Success criteria**: Five-document plan exists at the resolved path in each target repo.

**On failure**: Surface the error. Do not proceed to Step 7 for the failing repo until the plan
is authored.

### Step 7 — Quality Gate (Per Plan, Nested Workflow)

Run [plan-quality-gate](./plan-quality-gate.md) for each created plan in its own repo.

**Workflow**: `plan/plan-quality-gate`

- **Args**: `scope: <plan-folder-path>, mode: {input.gate-mode}, max-concurrency: {input.max-concurrency}`
- **Output**: `final-status` (pass / partial / fail), `final-report`
- **Run**: one gate per plan, up to `max-concurrency` gates in parallel

Each plan must reach `pass` (double-zero: zero CRITICAL/HIGH/MEDIUM findings on two consecutive
checks at the default `strict` gate-mode, or the invoker-specified gate-mode).

**On `partial` or `fail`**: Fix the plan using `plan-fixer` and re-run the gate. Do not deliver
un-gated plans. A plan in `partial` or `fail` state after two re-gate attempts is a blocking
issue — surface it to the invoker before proceeding with delivery of the passing plans.

**Success criteria**: Every plan in the parity set reaches `pass`.

### Step 8 — Delivery and Finalization (Per Mode)

#### Part A — Delivery

Commit and deliver per the selected mode.

**Commit guidance** (per [Commit Messages Convention](../../development/workflow/commit-messages.md)):
Use Conventional Commits format. Split thematically — plan files and rationale docs may be
separate commits. Never commit secrets. Respect each repo's pre-commit and pre-push hooks; do not
bypass them.

Example commit messages:

```
chore(plans): add <objective-slug> parity plan (ose-public)
docs(explanation): add <objective-slug> parity decisions rationale
```

**Per mode**:

- `main-to-origin-main`: Push each repo's commits to `origin main` directly. Not available for any
  bare repo in the set (`ose-primer`, `ose-infra` today) — a bare repo has no primary checkout to
  push from directly; those targets deliver via `worktree-to-origin-main` instead.
- `worktree-to-origin-main`: Push each repo's worktree commits to `origin main`. Remove worktrees
  after delivery: `git worktree remove worktrees/<objective-slug> && git worktree prune`.
- `worktree-to-pr` (default): Push branch `plan/<objective-slug>` to each repo. Create or update a
  draft PR per repo via `gh pr create --draft` (skip creation if a PR for that branch already
  exists).

**Success criteria**: All commits land at the intended targets; hooks pass; no secrets committed.

**On push failure**: Surface the error. Do not retry automatically — conflicts require invoker
resolution.

#### Part B — Finalization

Report outcomes.

**Output**:

- `plans-created`: One path per target repo
- `gate-results`: plan-quality-gate status per plan (pass / partial / fail)
- `delivery-refs`: Commit SHAs pushed to `origin main` (main modes) or PR URLs (worktree-to-pr)
- Deviation count summary: "N deliberate deviations recorded; 0 silent deviations"

The deviation count summary is the key quality signal. A workflow run that produces zero
deliberate deviations and zero silent deviations has done nothing useful. A run with N deliberate
deviations and zero silent deviations has done exactly what this workflow exists to do.

## Termination Criteria

**Success** (`pass`):

- Every plan reaches `pass` on plan-quality-gate (double-zero at the specified gate-mode)
- Every plan is delivered per the selected mode
- Zero undecided matrix rows (every deviation has a recorded decision and justification)

**Partial** (`partial`):

- Some plans gated and delivered; at least one plan is in `partial` or `fail` gate state, or
  at least one delivery target was not reached

**Failure** (`fail`):

- Technical errors that prevent step completion, or the invoker abandons grilling (Step 3 or
  Step 5) before all matrix rows are resolved — partial grilling produces no valid plans

## Grilling Contract

This workflow is intentionally exhaustive in its grilling. The invoker should expect multiple
AskUserQuestion-style multiple-choice rounds per the
[Grilling-With-Options Convention](../../development/workflow/grilling-with-options.md).

The workflow's value proposition is precisely that no cross-repo difference survives unexamined.
The grilling is not bureaucratic overhead — it is the core mechanism that transforms an ad-hoc
"let's do the same thing in each repo" impulse into a durable, auditable set of decisions.

The result is NOT a set of 1-to-1 identical repos. It is a set of repos whose every difference
from each other is intended. A repo that deviates from the others because of a real constraint
(private CI, different language stack, existing convention) and records that deviation is a
healthy outcome. A repo that deviates silently — because the grilling skipped the row — is a
workflow failure.

Every deviation requires:

1. A recorded resolution in the deviation matrix (in each plan's `tech-docs.md`)
2. A recorded justification (why this repo differs)
3. A rationale doc in the repo's `docs/explanation/` tree (or equivalent location) describing
   the decision in plain language for future contributors

"We didn't discuss it" is never an acceptable justification.

## Example Usage

### Default: All Three Repos, worktree-to-pr, in-progress

```
User: "Run plan-multi-repo-parity-planning for objective: standardize markdown gates across
       ose-public, ose-primer, and ose-infra"
```

The orchestrator surveys each repo, builds the deviation matrix, grills the invoker (Step 3),
optionally delegates research to `web-researcher` (Step 4), grills again post-research
(Step 5), authors three plans (one per repo) in `plans/in-progress/standardize-markdown-gates/`,
gates each plan, and opens a draft PR per repo rather than pushing directly to `origin main` —
the repo-wide `worktree-to-pr` default.

### Direct push with backlog stage

```
User: "Run plan-multi-repo-parity-planning for objective: align agent catalogs
       mode: worktree-to-origin-main stage: backlog"
```

Creates three backlog plans at `plans/backlog/align-agent-catalogs/`, gates
each, and pushes each plan directly to its repo's `origin main` via worktrees instead of opening
a PR. Useful when the invoker wants to skip the formal review step for low-risk plan documents.

### Subset of Two Repos

```
User: "Run plan-multi-repo-parity-planning for objective: add specs:coverage gate
       repos: ose-public, ose-primer"
```

Surveys only `ose-public` and `ose-primer`, builds a two-column deviation matrix, grills the
invoker, authors two plans, and delivers both. `ose-infra` is excluded from this run.

## Safety Features

**Worktree isolation** (default mode): plan authoring happens in a dedicated worktree per repo,
keeping `main` clean until delivery. The worktree is provisioned fresh and initialized with the
full two-step toolchain sequence (`npm install` + `npm run doctor -- --fix`) per the
[Worktree Toolchain Initialization](../../development/workflow/worktree-setup.md)
practice.

**Gate-before-delivery**: No plan is pushed until it reaches `pass` on plan-quality-gate. An
un-gated plan is a blocked delivery, not an exception.

**No implementation**: This workflow is type `planning`. It produces plans, not code, not
config changes. Execution of the objective happens downstream via the
[plan-execution workflow](./plan-execution.md) after the plans are established.

**Hook compliance**: Every delivery commit passes pre-commit and pre-push hooks of the target
repo. No hook bypassing; no `--no-verify`.

**Secrets rule**: The
[No Secrets in Git convention](../../conventions/security/no-secrets-in-committed-files.md) applies in full.
No system secret (key, password, API token, connection string) enters any plan file.

**PR mode for review**: When the invoker wants formal review of plans before they go active,
select `worktree-to-pr`. The PRs remain in draft until the invoker promotes them.

## Related Workflows

- [Plan Quality Gate](./plan-quality-gate.md) — nested workflow called in Step 7 for each plan
- [Plan Planning](./plan-planning.md) — single-repo sibling; this workflow
  is its multi-repo analogue (one plan per repo, one grill session across all repos)
- [Plan Execution](./plan-execution.md) — downstream workflow that executes the plans this
  workflow creates; runs after plans are established and promoted to `in-progress/`
- [Plan Multi-Repo Parity Planning and Execution](./plan-multi-repo-parity-planning-and-execution.md) —
  end-to-end composite that runs this workflow as its planning phase and continues directly into
  plan-execution for every resulting plan
- [PR-Review Maker→Fixer Cycle](../pr/pr-review-quality-gate.md) — runs during each repo's
  execution phase when that repo's authored plan resolves to a `*-to-pr` delivery mode

## Principles Implemented/Respected

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**:
  Every cross-repo deviation is explicitly surfaced, decided, and recorded. No implicit alignment
  is permitted.
- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**:
  Two grill sessions and an optional research step before authoring ensure plans are built on
  verified, negotiated decisions rather than assumptions about what other repos need.
- **[Documentation First](../../principles/content/documentation-first.md)**:
  Plans are the terminal deliverable. The rationale doc in each repo's `docs/explanation/` tree
  makes every decision inspectable by future contributors.
- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)**:
  Survey, matrix construction, research, plan authoring, and quality gating are all orchestrated
  steps, not manual handoffs.
- **[No Time Estimates](../../principles/content/no-time-estimates.md)**: Workflow describes
  what is produced and what decisions are required, never how long each step takes.

## Conventions Implemented/Respected

- **[Workflow Naming Convention](../../conventions/structure/workflow-naming.md)**: Filename
  `plan-multi-repo-parity-planning` — scope `plan`, qualifiers `multi-repo` + `parity`, type
  `planning` (surveys repo state, produces plans, never implements).
- **[Plans Organization Convention](../../conventions/structure/plans.md)**: Five-document
  multi-file layout; stage-aware folder naming (no date prefix in `backlog/` or
  `in-progress/`; completion-date prefix in `done/` only); worktree specification in each plan's
  `delivery.md`.
- **[Worktree Path Convention](../../conventions/structure/worktree-path.md)**: Worktrees land
  at `worktrees/<objective-slug>/` in the repo root.
- **[Grilling-With-Options Convention](../../development/workflow/grilling-with-options.md)**:
  Steps 3 and 5 grill sessions present 2-4 concrete options per question; one option is marked
  Recommended; open-ended questions without options are forbidden.
- **[Commit Messages Convention](../../development/workflow/commit-messages.md)**: Conventional
  Commits format; thematic splits; imperative mood; no period at end.
- **[Linking Convention](../../conventions/formatting/linking.md)**: All cross-references use
  GitHub-compatible markdown with `.md` extensions and relative paths.
- **[File Naming Convention](../../conventions/structure/file-naming.md)**: Lowercase kebab-case
  for all plan files and rationale docs created by this workflow.
- **[No Secrets in Git Convention](../../conventions/security/no-secrets-in-committed-files.md)**: No
  system secret enters any plan file or rationale doc created by this workflow.
- **[Web Research Delegation Convention](../../conventions/writing/web-research-delegation.md)**:
  External research delegated to `web-researcher` in Step 4 when the research-needed flag
  is set.
- **[Plans Organization Convention §Delivery Mode](../../conventions/structure/plans.md#delivery-mode)**:
  each per-repo plan authored in Step 6 declares its own `## Delivery Mode` field, resolved
  independently per repo via the three-tier precedence; divergence across repos is recorded as a
  deviation-matrix row like any other per-repo difference — distinct from this workflow's own
  planning-phase `mode` input.
