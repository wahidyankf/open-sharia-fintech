---
name: plan-planning
title: "plan-planning"
goal: >
  Create a well-researched, grill-validated project plan in the resolved target stage
  (plans/in-progress/ by default, or plans/backlog/ when target-stage=backlog) from a user prompt
  describing a desired behavior or change, then push it to the confirmed target
termination: >
  Plan exists in the resolved target-stage directory, passes plan-quality-gate at strict mode, and
  is pushed to the confirmed target
inputs:
  - name: prompt
    type: string
    description: Description of the behavior, change, or convention to adopt in the repository
    required: true
  - name: push-target
    type: string
    description: "Git push destination (e.g., 'origin main'). Confirmed in the Step 1 grill if not provided."
    required: false
    default: "origin main"
  - name: target-stage
    type: enum
    values: [in-progress, backlog]
    description: >
      Which plans/ stage the finished plan lands in. `in-progress` (default) creates an immediately
      active plan at plans/in-progress/<identifier>/ (no date prefix). `backlog` creates a
      proposed-but-not-yet-scheduled plan at plans/backlog/<identifier>/ (no date prefix, per the
      Plans Organization Convention). Both stages stop at plan creation — neither
      executes the plan.
    required: false
    default: in-progress
outputs:
  - name: plan-path
    type: string
    description: >
      Path to the created plan in the resolved target stage (plans/in-progress/<identifier>/ or
      plans/backlog/<identifier>/)
  - name: final-status
    type: enum
    values: [pass, partial, fail]
    description: Final status after the quality gate
  - name: final-report
    type: file
    pattern: generated-reports/plan__*__audit.md
    description: Final audit report from plan-quality-gate
---

# Plan Establishment Workflow

**Purpose**: Transform a user prompt describing a desired behavior or change into a
production-ready plan in the resolved target stage (`plans/in-progress/` by default, or
`plans/backlog/` when `target-stage=backlog`), validated by `plan-quality-gate` and pushed to
the confirmed target.

## Stage Resolution

This workflow places the finished plan according to the `target-stage` input. Throughout the
steps below, `<plan-dir>` resolves as:

- **`target-stage=in-progress`** (default): `plans/in-progress/<identifier>/` — no date prefix;
  the plan is immediately active.
- **`target-stage=backlog`**: `plans/backlog/<identifier>/` — no date prefix, per the
  [Plans Organization Convention](../../conventions/structure/plans.md); the plan is a
  proposal awaiting promotion.

Both stages stop at plan creation. **Neither stage executes the plan** — execution is a separate
concern handled later by the [Plan Execution workflow](./plan-execution.md) after a backlog plan
is promoted to `in-progress/` (a pure move — neither stage carries a date prefix).

**When to use**:

- When the user describes a new behavior, pattern, or convention to adopt in the repository
- When a vague idea needs to become a structured, executable plan
- When research is needed before writing a plan (library versions, best practices, prior art)
- When the user wants the full plan-creation lifecycle orchestrated automatically
- When a parent workflow needs a validated plan produced into a specific stage — e.g.
  `repo-dependency-bump-planning` calls this with `target-stage=backlog`

## Execution Mode

**Direct Orchestration** — the calling context (the top-level assistant session) is the
orchestrator. It follows this workflow step-by-step: exploring the repo, conducting grill sessions
via the `grill-me` Skill, delegating research to `web-researcher` and plan writing to
`plan-maker` via the Agent tool, and running the `plan-quality-gate` workflow inline.

Grill sessions run in the calling context (not delegated) so the user's conversation is preserved
across all turns.

**Worktree default**: All plan authoring happens inside a dedicated worktree at
`worktrees/<identifier>/`. If the worktree does not already exist, provision it from the latest
`origin/main` before Step 4; if it exists, enter it and sync it with `origin/main` first:

```bash
git fetch origin
git worktree add -b <identifier> worktrees/<identifier> origin/main
cd worktrees/<identifier>
npm install
npm run doctor -- --fix
```

All subsequent file operations — including the plan files written by `plan-maker` — are relative
to the worktree root. The resolved `<plan-dir>` (e.g., `plans/in-progress/<identifier>/`) is a
path within that worktree. See the
[Worktree Path Convention](../../conventions/structure/worktree-path.md) for the canonical
worktree location and the
[Worktree Toolchain Initialization guide](../../development/workflow/worktree-setup.md) for the
full post-provisioning setup sequence.

```
User: "Establish a plan to [describe desired change]"
```

## Planning Granularity

How a plan is cut into phases determines how much of it can proceed in parallel and how early each
piece reaches `main`. These rules bind at authoring time, not merely at execution time.

### One Worktree, One Branch, One PR, One Delivery Unit (HARD RULE)

Each independent node of the plan's dependency DAG **that produces changes** lands as **its own
PR**. The mapping is strict and one-to-one: **one worktree → one branch → one PR → one delivery
unit**. Never open two PRs from one worktree, and never drive one PR from two worktrees.

A **delivery unit** is the contiguous run of phases ending at a **delivery boundary** — the phase
after which the accumulated work is independently shippable. The unit, not the individual phase, is
what maps to a PR: a plan opens a PR at its natural delivery points, which may be once at the very
end or several times through the plan. Phases inside a unit that are not its boundary still pass
their own `### Phase N Gate`, but open no PR and merge nothing. The boundary test, the required
`### Delivery Boundaries` declaration table, and the anti-batching counterweight are stated in
[Plans Organization Convention §PRs Open at Delivery Boundaries](../../conventions/structure/plans.md#prs-open-at-delivery-boundaries-not-every-phase-hard-rule).

Genuinely dependent phases stay a single delivery unit. The DAG governs, not the phase numbering:
phases that merely appear in sequence are not thereby dependent, and splitting **independent** work
into separate delivery units is the default. Sequence is not dependency — and neither is it a
licence to fold independent nodes together to reduce PR count.

**Phase 0 is not one of these nodes — the earliest PR is Phase 1 (HARD RULE)**. Phase 0 is
Environment Setup and Baseline: it installs dependencies, converges the toolchain, records the
baseline, and clears preexisting failures. It produces nothing reviewable, so it opens no PR, pushes
no branch, runs no review cycle, and merges nothing — under **every** delivery mode, the default
`worktree-to-pr` included. Author it as a local, gate-terminated phase whose evidence artifacts ride
the Phase 1 PR. A Phase 0 that genuinely produces reviewable changes is mis-scoped: move that work
into Phase 1. See
[Plans Organization Convention §Phase 0 Opens No PR](../../conventions/structure/plans.md#phase-0-opens-no-pr--the-earliest-pr-is-phase-1-hard-rule).

### Merge at Delivery Boundaries — Not Every Phase, and Not One Batch

Each delivery unit's PR is **opened and merged** as that unit's **delivery boundary** is reached. It
is neither opened early at every intermediate phase, nor held open for a **batch merge** at plan end.

Both failure modes cost something different. Opening a PR per phase spends a full review cycle on
scaffolding the next phase rewrites, and the review cannot judge intent that only lands two phases
later. Holding PRs for a batch merge serialises work the DAG already declared independent, and grows
the divergence each PR must reconcile against `main`.

Grouping **dependent** phases into one delivery unit is not batching. The prohibition targets
holding **independent, already-open** PRs — never the decision to review a dependent chain as one
complete thought.

The **merge actor** follows the inverted default in
[Plans Organization Convention §Delivery Mode](../../conventions/structure/plans.md#delivery-mode):
`[AI]` merges once the hardened preconditions hold, and `[HUMAN]` applies **only** where a plan's
own step states that gate explicitly.

### Feature Flags: Default, Escape, Removal

Partial work reaches `main` **merged but dark** behind a feature flag rather than waiting on a
long-lived branch. Flagging is the **default**.

- **Escape**: a phase lands **unflagged** only when it ships no **user-reachable** behaviour change
  — pure docs, governance, refactor, or test-only work — and the delivery step names which
  exemption applies. An unflagged phase with no named exemption is a defect.
- **Removal**: every flag introduced carries a named **flag removal step** in the plan's final
  phase. A flag with no removal step is an unbounded commitment, not a rollout mechanism.

### How the `worktree-to-pr` Default Binds at Each Plan Path

The default binds differently depending on what is being done:

- **Creating or updating a plan** binds it as a **design obligation**. The authoring edit itself may
  push direct to `main`, but the plan's phases MUST be authored so they group into **independently
  PR-able delivery units**, with each unit's boundary named in the `### Delivery Boundaries` table.
  A plan that genuinely cannot be decomposed that way records **why** in its `tech-docs.md` — the
  constraint is documented, not silently absorbed.
- **Executing a plan** binds it as the actual delivery route: worktree → PR, per the
  delivery-unit-to-PR mapping above.

### Surface-Conditional Tester Gates

Which quality gates a plan must run depends on **what surface it ships**. Decide this at authoring
time and write the result into the delivery checklist — it binds again at execution, and again as a
merge precondition.

The rule is: **a plan that changes behavior a user or caller can reach must exercise that behavior
before it merges.** The list below routes the common surfaces to their gates. It is a routing table,
never the boundary of the rule — a surface absent from it does not become exempt by omission.

- **UI-bearing plan** → run **both** UI gates: [`ui/ui-quality-gate.md`](../ui/ui-quality-gate.md)
  (static, over component source) **and**
  [`web/web-ux-test-fixing-planning.md`](../web/web-ux-test-fixing-planning.md) (the running-UI
  EWT/UWT/DWT triad).
- **API- or backend-bearing plan** → run [`api/api-quality-gate.md`](../api/api-quality-gate.md).
- **Several of these** → run each set.
- **A reachable surface with no gate listed above** — a CLI such as `apps/rhino-cli/**`, a library
  under `libs/`, a git hook, a CI workflow — is **not exempt**. The plan states in its `tech-docs.md`
  how the changed behavior will be exercised through its own interface (for a CLI: which subcommands
  get invoked and what output is recorded; for a library: which consuming caller exercises it, not
  only its unit tests), and the delivery checklist carries that as a step.
- **Genuinely no reachable behavior** — docs, comments, or a pure refactor with no behavioral delta —
  → the plan **MUST state the exemption explicitly in its `tech-docs.md`**, with the justification.
  An unstated exemption is indistinguishable from an oversight, which is exactly what this rule
  exists to prevent.

This wording is congruent with merge precondition (e) in
[the PR Review Quality Gate](../pr/pr-review-quality-gate.md#hardened-merge-preconditions); the two
must be edited together. An earlier revision let this authoring-time list stay in the
enumerate-then-exempt shape after the merge-time clause was fixed, so a plan could be authored exempt
and only discover at merge that it was not.

#### The Three UI Gates Are Complementary, Never Substitutes

They act at three different lifecycle stages, and passing one says nothing about the others:

- **`plan-checker` Step 5k** gates the UI **design funnel** in `prd.md` — **pre-build**, before any
  component exists.
- **`ui/ui-quality-gate.md`** gates the **built components** via `swe-ui-checker` / `swe-ui-fixer` —
  static analysis of source, no browser involved.
- **`web/web-ux-test-fixing-planning.md`** gates the **running UI** via the EWT/UWT/DWT triad — a
  real browser against a real deployment.

A component can satisfy Step 5k's design funnel, pass static token and accessibility checks, and
still be broken in the browser. Treating any one of the three as covering another is the failure
this distinction guards against.

### Vercel MCP Availability (Surface-Conditional)

A second surface-conditional gate, resolved at authoring time for the same reason the tester gates
are: the answer changes what the delivery checklist can contain.

**Trigger** — the plan touches a Vercel-deployed surface if a path it changes is covered by a
`vercel.json`, it names a `prod-*`/`stag-*` branch a Vercel project builds from, or a deployment
agent exists for an app it changes. Decide this mechanically (`git ls-files | grep 'vercel\.json$'`),
never from memory: the set drifts, and in some repositories of this ecosystem it is empty, which
makes every plan there out of scope.

**When triggered**, the author probes for a connected, authenticated Vercel MCP server and records
the result in `tech-docs.md`. That result decides executor tags:

- **Available** → deployment-observation steps are `[AI]`: deploy state and provenance, build logs,
  runtime errors, and runtime invocation counts grouped by source, route, or status code. This is
  what lets a plan assert its own effect — a measured before-and-after — instead of a single
  hand-checked URL.
- **Unavailable** → the plan degrades explicitly rather than quietly weakening a criterion. See
  [§Degraded Mode](../../development/infra/vercel-mcp.md#degraded-mode).

**The boundary is narrow, and over-assuming it is the common failure**: billing, usage, invoices,
Spend Management, Observability settings, firewall rulesets, the compute-model setting, and domain
configuration have **no** tool. Those steps stay `[HUMAN]` whatever the probe says. Group them into
Phase 0 so the human actions land in one sitting and the remaining phases stay `[AI]`.

Full rule, capability boundary, operational limits, and identifier hygiene:
[Vercel MCP Capability Convention](../../development/infra/vercel-mcp.md).

### The Plan-Docs-Only Carve-Out

A change touching **only** `plans/**`, with no `apps/` or `libs/` code, may push direct to `main`.
This **plan-docs-only** carve-out stands on its own footing as a general convention: such a change
ships no runtime behaviour, so the PR review cycle has no code surface to review.

It is stated here in its own right and is **not** derived from DD-11 of any individual plan, which
disclaims being a general precedent.

## Steps

### 0. Prompt Parsing and Repo Exploration (Sequential)

Before any user interaction, understand the current repo state relative to the prompt.

**Orchestrator action**:

1. Parse the prompt: extract the desired behavior, likely affected areas (governance files,
   agents, workflows, apps, libs), and any explicit constraints
2. Explore the repo:
   - Read relevant `repo-governance/` files (conventions, workflows, development practices that
     overlap with the prompt)
   - Search `plans/in-progress/`, `plans/backlog/`, `plans/done/` for related prior plans
   - `Grep` for existing conventions or code that may already address or conflict with the prompt
   - Read `AGENTS.md` for relevant agent and workflow references
3. Build a context summary: what already exists, what gaps remain, what conflicts with the prompt

**Output**: Repo context loaded. Related prior work and conflicts identified.

**Notes**:

- Purely exploratory — no user interaction in this step
- Thorough exploration reduces grill time in Step 1 (pre-read the repo so you can answer "does X
  already exist?" without asking the user)

### 1. First Grill — Scope, Constraints, Push Target (Sequential, Hard Gate)

Invoke the `grill-me` Skill to resolve all open design decisions before research begins.

**Orchestrator action**:

Invoke the `grill-me` Skill (`.claude/skills/grill-me/SKILL.md`). Present Step 0 findings.
Every question in this grill MUST follow the
[Grilling-With-Options Convention](../../development/workflow/grilling-with-options.md): present
2-4 concrete, mutually exclusive options with explicit trade-offs, mark exactly one option
Recommended, and use the harness's native interactive multiple-choice tool when available
(markdown fallback otherwise). Open-ended questions without options are FORBIDDEN.

Resolve ALL of the following:

1. **Scope**: What is the exact behavior to adopt? What is explicitly out-of-scope?
2. **Affected files**: Which governance files, agents, or workflows will change?
3. **Conflicts**: Does any current convention already address this, conflict with it, or need
   updating?
4. **Constraints**: Backwards compatibility, multi-harness binding implications (if the plan
   touches `.claude/agents/`, `.opencode/agents/`, or `repo-governance/` paths, confirm that
   changes remain vendor-neutral per the
   [Governance Vendor-Independence Convention](../../conventions/structure/governance-vendor-independence.md)),
   tool dependencies
5. **Plan identifier**: What slug should the plan folder use (e.g., `add-foo-convention`)?
6. **Target stage**: Confirm `target-stage` (default `in-progress`). If `backlog`, the plan lands
   at `plans/backlog/<identifier>/`; if `in-progress`, at
   `plans/in-progress/<identifier>/`. Skip this question if the caller already passed
   `target-stage` explicitly (e.g., a parent workflow). Record — resolves `<plan-dir>` for all
   later steps.
7. **Push target**: Confirm where the finished plan should be pushed (default: `origin main`).
   Record — used verbatim in Step 7 without re-asking.
8. **PR vs. direct push — Delivery Mode**: Confirm which of the four
   [Delivery Mode](../../conventions/structure/plans.md#delivery-mode) options — `worktree-to-pr`
   (default), `worktree-to-origin-main`, `main-to-origin-main`, or `main-to-pr` — governs this
   plan's own future execution. Record the answer so Step 4 instructs `plan-maker` to declare it
   explicitly in the plan's `## Delivery Mode` field; an unmarked field falls through to the
   three-tier precedence (invocation argument > plan field > `worktree-to-pr` default) resolved
   later by [plan-execution.md Step 0](./plan-execution.md#0-enter-the-designated-worktree-sequential-hard-gate).
   Choosing a `*-to-pr` mode means the plan's own execution runs the
   [PR-Review Maker→Fixer Cycle](../pr/pr-review-quality-gate.md) before archival.
9. **Definition of done**: What must the finished plan contain for the user to consider it ready?
10. **Research needed**: Are there external claims (library versions, third-party best practices,
    API behavior) that require verification before writing?

**Do NOT proceed to Step 2** until:

- All design-decision branches are resolved
- Push target, target stage, and plan identifier are explicitly confirmed
- Definition of done is agreed upon
- Whether research is needed is established (determines Step 2 skip condition)

**Output**: Push target confirmed. Target stage confirmed (`<plan-dir>` resolved). Plan identifier
confirmed. All decisions resolved. Research-needed flag set.

**On failure to resolve**: Do not proceed. Remain in grill until resolved or user cancels.

### 2. Web Research (Sequential, Conditional)

Delegate external research to `web-researcher` to verify claims and gather authoritative
sources.

**Skip condition**: Skip if ALL hold:

1. The prompt describes a purely internal governance or structural change with no external claims
2. No library versions, API signatures, tool behavior, or third-party conventions need verification
3. The user confirmed in Step 1 that no research is needed

If skipping: emit `Step 2 skipped — no external research needed (confirmed in Step 1).`

**If NOT skipping**:

Invoke `web-researcher` via the Agent tool. Provide a focused research prompt covering:

- Best practices or authoritative sources for the proposed approach
- Library or tool behavior referenced in the prompt (versions, API signatures, caveats)
- Prior art: has anyone formalized this pattern? Known failure modes?
- Risks or caveats not mentioned in the prompt

**Agent**: `web-researcher`

**Output**: Cited, structured research findings. Passed to Step 3 grill and included in the
plan-maker handoff in Step 4.

### 3. Second Grill — Post-Research Validation (Sequential)

Present research findings and grill again to validate direction and close new branches.

**Orchestrator action**:

1. Summarize research findings from Step 2 (or confirm skipped)
2. Invoke the `grill-me` Skill. Every question MUST follow the
   [Grilling-With-Options Convention](../../development/workflow/grilling-with-options.md):
   2-4 concrete options, explicit trade-offs, exactly one Recommended, native interactive tool
   when available. Cover:
   - Do the research findings change any decision from Step 1? (options: yes — which decision /
     no — proceed as agreed / partial — one or more decisions need refinement)
   - Are there new constraints or trade-offs surfaced by the research?
   - Does the proposed approach still hold after authoritative sources?
   - Are there risks the user wants to explicitly accept or mitigate in the plan?
3. Confirm the updated direction before proceeding

**Do NOT proceed to Step 4** until mutual understanding is confirmed, incorporating research.

**Notes**:

- If research was skipped in Step 2, this is a brief confirmation pass, not a full grill session
- All new branches must be resolved before calling `plan-maker`

**Output**: Final direction confirmed. Research findings integrated into design decisions.

### 4. Plan Creation (Sequential)

Invoke `plan-maker` to write the plan in the resolved `<plan-dir>` (see [Stage Resolution](#stage-resolution)).

**Agent**: `plan-maker`

Delegate via the Agent tool. Provide a self-contained handoff prompt containing ALL of:

1. Original user prompt (verbatim)
2. Resolved design decisions from Steps 1 and 3 (numbered decision list)
3. Research findings from Step 2 (cited) — or note that research was skipped
4. Confirmed plan identifier and resolved `<plan-dir>` (the exact target folder, relative to the
   worktree root at `worktrees/<identifier>/`)
5. Confirmed push target and delivery mode (Step 1 item 8)
6. Definition of done (from Step 1)
7. **Explicit instruction**: write the plan directly to the resolved `<plan-dir>` inside the
   worktree at `worktrees/<identifier>/`. For `target-stage=in-progress` this is
   `plans/in-progress/<identifier>/` (no date prefix); for `target-stage=backlog` this is
   `plans/backlog/<identifier>/` (also no date prefix). Do NOT place an
   `in-progress` plan under `backlog/` or vice versa.

`plan-maker` emits the final Knowledge Capture phase in `delivery.md` plus a `learnings.md`
scaffold in the plan folder as part of every generated plan, per the
[Knowledge Capture Convention](../../development/quality/knowledge-capture.md).

**Note on plan-maker's own grill protocol**: `plan-maker` mandates a pre-write grill (Step 1) and
a post-write grill (Step 8). When invoked by `plan-establishment`, these become
**validation passes** — macro-decisions are already resolved. Micro-decisions (exact Gherkin
phrasing, section ordering, step granularity) are still resolved by plan-maker's grills.

**Output**: Plan files created in the resolved `<plan-dir>`.

**On failure**: Terminate with status `fail`. Surface the error.

### 5. Plan Review (Sequential)

Read the created plan files and verify structural completeness before the quality gate.

**Orchestrator action**:

1. Read all plan files in the resolved `<plan-dir>`
2. Verify `## Worktree` section exists in `delivery.md` (multi-file) or `README.md` (single-file)
3. Verify delivery checklist has at least one `- [ ]` checkbox
4. Verify Gherkin acceptance criteria present in `prd.md` (multi-file) or condensed PRD
5. Verify the worktree path in the plan matches `<identifier>` confirmed in Step 1, and that the
   plan folder lives under the correct stage (`backlog/` and `in-progress/` both use a bare
   `<identifier>/` with no date prefix; only `done/` carries the `<YYYY-MM-DD>__` prefix) per the
   confirmed `target-stage`
6. Verify delivery checklist starts with **Phase 0: Environment Setup and Baseline**, and that
   Phase 0 contains **no** PR-creation, PR-review-cycle, push, or merge step — the earliest phase
   that may open a PR is Phase 1
   ([§Phase 0 Opens No PR](../../conventions/structure/plans.md#phase-0-opens-no-pr--the-earliest-pr-is-phase-1-hard-rule))
7. Verify the `## Parallelization Model` carries a `### Delivery Boundaries` table mapping **every**
   change-producing phase to a delivery unit, that the last change-producing phase is a boundary,
   and that PR-creation, review-cycle, and merge steps appear **only** in boundary phases — a PR per
   phase is a defect
   ([§PRs Open at Delivery Boundaries](../../conventions/structure/plans.md#prs-open-at-delivery-boundaries-not-every-phase-hard-rule))
8. Verify `delivery.md` opens with the `[AI]`/`[HUMAN]` executor legend and that every step only a human can perform is tagged `[HUMAN]`
9. Verify every phase ends with a `### Phase N Gate` (must-pass verification) followed by a `> **Pause Safety**:` note
10. If structural gaps found: provide a focused prompt to `plan-maker` or fix trivially via `Edit`

**Output**: Plan structurally complete. Ready for quality gate.

**On failure after one retry**: Terminate with status `fail`.

### 6. Quality Gate (Sequential)

Run the `plan-quality-gate` workflow at `strict` mode.

Follow the [plan-quality-gate workflow](./plan-quality-gate.md) with:

- **Input** `scope`: the resolved `<plan-dir>`
- **Input** `mode`: `strict`
- **Output**: `final-status`, `final-report`

**Success criteria**: `plan-quality-gate` returns `pass` (zero CRITICAL/HIGH/MEDIUM on two
consecutive checks).

**On `partial` or `fail`**: Investigate the final report. Apply targeted fixes. Re-run
`plan-quality-gate` up to 2 additional times. If still not `pass`, terminate with status
`partial` and surface the final report.

### 7. Push and Verify (Sequential)

Commit and push the plan to the confirmed target, then remove the worktree.

**Orchestrator action**:

1. From inside the worktree (`worktrees/<identifier>/`), stage all plan files:
   `git add <plan-dir>`
2. Commit inside the worktree: `chore(plans): establish <identifier> plan` (for
   `target-stage=backlog`, use `chore(plans): add <identifier> to backlog`)
3. Push from the worktree to the confirmed target (default `origin main`):
   `git push <confirmed-target> HEAD:main`
4. Monitor GitHub Actions: `gh run list --limit 5` — verify all triggered workflows complete
   with `completed/success` conclusion
5. If a CI workflow fails: diagnose root cause, fix, push a follow-up commit, re-monitor
6. After CI passes, remove the worktree from the repo root:

   ```bash
   git worktree remove worktrees/<identifier>
   git branch -d <identifier>
   ```

7. Emit a user-visible summary: plan path, quality gate status, push target, CI status

**Output**: `plan-path`, `final-status`, `final-report`.

**On push failure**: Surface the error. Do NOT retry automatically — conflicts require human
resolution.

## Principles Implemented/Respected

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**:
  Two grill sessions and a research step ensure the plan is built on verified understanding, not
  assumptions
- **[Root Cause Orientation](../../principles/general/root-cause-orientation.md)**: Repo
  exploration in Step 0 prevents duplicating existing conventions and surfaces conflicts early
- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)**:
  The full research → grill → write → validate → push lifecycle is orchestrated without manual
  intervention at each step
- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**:
  Push target, plan identifier, and definition of done are confirmed explicitly in Step 1 before
  any work begins

## Conventions Implemented/Respected

- **[Plans Organization Convention](../../conventions/structure/plans.md)**: Creates plans in
  `plans/in-progress/` (default) or `plans/backlog/<identifier>/` (when
  `target-stage=backlog`, also no date prefix) with correct identifier format and worktree specification
- **[Governance Vendor-Independence Convention](../../conventions/structure/governance-vendor-independence.md)**:
  Step 1 grill includes an explicit harness-neutrality checkpoint for plans touching agents,
  skills, or `repo-governance/` paths
- **[Web Research Delegation Convention](../../conventions/writing/web-research-delegation.md)**:
  External research delegated to `web-researcher`
- **[Commit Messages Convention](../../development/workflow/commit-messages.md)**: Conventional
  Commits format in Step 7
- **[CI Post-Push Verification Convention](../../development/workflow/ci-post-push-verification.md)**:
  Step 7 monitors GitHub Actions after push
- **[Grilling-With-Options Convention](../../development/workflow/grilling-with-options.md)**:
  Steps 1 and 3 grill sessions MUST present 2-4 concrete options with trade-offs, exactly one
  Recommended option, and use the harness's native interactive multiple-choice tool when available

## Related Workflows

- [Plan Quality Gate](./plan-quality-gate.md) — called in Step 6
- [Plan Execution](./plan-execution.md) — next workflow after plan-establishment

## Related Documentation

- [Plans Organization Convention](../../conventions/structure/plans.md)
- [Grilling-With-Options Convention](../../development/workflow/grilling-with-options.md) — format
  and mechanism for Steps 1 and 3 grill sessions
- [Governance Vendor-Independence Convention](../../conventions/structure/governance-vendor-independence.md)
- [grill-me Skill](../../../.claude/skills/grill-me/SKILL.md) — Steps 1 and 3
- [plan-maker Agent](../../../.claude/agents/plan-maker.md) — Step 4
- [web-researcher Agent](../../../.claude/agents/web-researcher.md) — Step 2
- [repo-setup-manager Agent](../../../.claude/agents/repo-setup-manager.md) — Phase 0 of plans
  created by this workflow
- [Plans Organization Convention §Delivery Mode](../../conventions/structure/plans.md#delivery-mode) —
  the four-mode vocabulary and three-tier precedence confirmed in Step 1 item 8
- [PR-Review Maker→Fixer Cycle](../pr/pr-review-quality-gate.md) — the review loop that runs
  during execution when the plan's confirmed delivery mode is `worktree-to-pr` or `main-to-pr`
