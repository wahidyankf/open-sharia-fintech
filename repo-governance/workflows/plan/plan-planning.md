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
      proposed-but-not-yet-scheduled plan at plans/backlog/YYYY-MM-DD__<identifier>/ (creation-date
      prefix per the Plans Organization Convention). Both stages stop at plan creation — neither
      executes the plan.
    required: false
    default: in-progress
outputs:
  - name: plan-path
    type: string
    description: >
      Path to the created plan in the resolved target stage (plans/in-progress/<identifier>/ or
      plans/backlog/<YYYY-MM-DD>__<identifier>/)
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
- **`target-stage=backlog`**: `plans/backlog/<YYYY-MM-DD>__<identifier>/` — creation-date prefix
  per the [Plans Organization Convention](../../conventions/structure/plans.md); the plan is a
  proposal awaiting promotion. `<YYYY-MM-DD>` is the date the plan is created.

Both stages stop at plan creation. **Neither stage executes the plan** — execution is a separate
concern handled later by the [Plan Execution workflow](./plan-execution.md) after a backlog plan
is promoted to `in-progress/` (date prefix stripped on promotion).

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
   at `plans/backlog/<YYYY-MM-DD>__<identifier>/`; if `in-progress`, at
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
   `plans/backlog/<YYYY-MM-DD>__<identifier>/` (creation-date prefix). Do NOT place an
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
   plan folder lives under the correct stage (`backlog/` with a `<YYYY-MM-DD>__` prefix, or
   `in-progress/` with no date prefix) per the confirmed `target-stage`
6. Verify delivery checklist starts with **Phase 0: Environment Setup and Baseline**
7. Verify `delivery.md` opens with the `[AI]`/`[HUMAN]` executor legend and that every step only a human can perform is tagged `[HUMAN]`
8. Verify every phase ends with a `### Phase N Gate` (must-pass verification) followed by a `> **Pause Safety**:` note
9. If structural gaps found: provide a focused prompt to `plan-maker` or fix trivially via `Edit`

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
  `plans/in-progress/` (default) or `plans/backlog/<YYYY-MM-DD>__<identifier>/` (when
  `target-stage=backlog`) with correct identifier format and worktree specification
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
