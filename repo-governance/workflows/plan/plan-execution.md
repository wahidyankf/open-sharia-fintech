---
name: plan-execution
title: "plan-execution"
goal: Execute a project plan, validate its completion and quality, then iteratively continue until all requirements are met and archive to plans/done/
termination: Zero findings remain after validation and plan moved to done/
inputs:
  - name: plan-path
    type: string
    description: Path to the plan file to execute (e.g., "plans/in-progress/new-feature/plan.md")
    required: true
  - name: max-iterations
    type: number
    description: Maximum number of execute-check cycles to prevent infinite loops
    required: false
    default: 10
  - name: max-concurrency
    type: number
    description: "Background agents run concurrently — the N in the N+1 model (1 main thread + N background agents = N+1 total). Raise only when independent work, machine capacity, and budget headroom all allow; lower under budget, runner, or disk pressure. Never self-promoted beyond the declared value."
    required: false
    default: 3
outputs:
  - name: final-status
    type: enum
    values: [pass, partial, fail]
    description: Final execution and validation status
  - name: iterations-completed
    type: number
    description: Number of execute-check cycles performed
  - name: final-report
    type: file
    pattern: generated-reports/plan-execution__*__validation.md
    description: Final validation report from plan-execution-checker
---

# Plan Execution Workflow

**Purpose**: Automatically execute a project plan, validate its completion and quality, then iteratively continue execution until all requirements are met. Upon success, move the plan to `plans/done/`.

**When to use**:

- When you want to execute a plan from start to finish with automated quality validation
- After creating a new plan and want immediate implementation
- For plans that require iterative refinement to meet all requirements
- When you need automated archival of completed plans to done/ folder
- For systematic plan completion with zero-findings quality standard

> **Pre-Execution Requirement**: Before executing, invoke the `grill-me` skill
> (`.claude/skills/grill-me/SKILL.md`) to stress-test any unresolved design decisions in
> the plan. Every question must present 2-4 concrete options (use an interactive
> multiple-choice tool when available, or the markdown question format). See
> [Grilling-With-Options Convention](../../development/workflow/grilling-with-options.md).

## Execution Mode

**Direct Orchestration** — the calling context (the top-level assistant session that received the "Execute plan …" request) is the orchestrator. It reads this workflow, parses the plan's delivery checklist, manages the live Task list via `TaskCreate` / `TaskUpdate`, performs the Atomic Sync Ritual against `delivery.md`, and delegates each checklist item to the appropriate specialized agent via the Agent tool (see Agent Selection below).

The calling context invokes `plan-execution-checker` as a delegated agent for independent validation (Step 3 and Step 6 below). Validation must run in an isolated context so the checker's judgment is not biased by the orchestrator's execution memory.

There is no dedicated `plan-executor` delegated agent. Executor logic lives in this workflow document; the calling context follows it directly. This keeps the live Task list visible to the user in real time (a delegated agent's tasks are isolated to its own context) and eliminates a redundant router hop.

**How to Execute**:

```
User: "Execute plan plans/in-progress/new-feature/plan.md"
```

The calling context will:

1. **Enter the work branch** (Step 0): the work branch is whatever the user specifies at invocation (a dedicated worktree, the `main` checkout, or any existing branch); if unspecified, the plan docs win (the `## Worktree` section, defaulting to a worktree provisioned from `origin/main`) — refuse to start only when neither the user nor the plan specifies one. Then, by default, pull the latest `origin/main` into the work branch first — before any implementation — to minimize merge collisions
2. Read the delivery checklist from the plan's `delivery.md` to understand all items
3. Create granular tasks using `TaskCreate` — one per remaining checkbox (including nested sub-bullets)
4. For each item: mark `in_progress`, **repo-ground its file paths and commands** (refuse-on-uncertainty if grounding fails), analyze it, **prefer the `_Suggested executor:_` annotation** if present (else fall back to Agent Selection heuristics), delegate to the chosen agent (or execute directly for trivial edits), verify the result
5. Perform the Atomic Sync Ritual after each item — tick `- [ ]` → `- [x]` in `delivery.md`, add implementation notes, `TaskUpdate completed`
6. Invoke `plan-execution-checker` via the Agent tool to validate the implementation
7. Iterate execution and validation until zero findings achieved
8. Move plan folder to plans/done/ using git mv
9. Show git status with modified files
10. Wait for user commit approval
11. After the archival is pushed to `origin main`, prompt the user to delete the plan's worktree (Step 8 worktree cleanup — never deletes without explicit confirmation)

## Orchestration Model

The **calling context** (top-level assistant session) acts as the orchestrator, following this workflow as its procedure. It reads the delivery checklist, determines which specialized agent is best suited for each item, delegates implementation to that agent via the Agent tool, verifies completion, and performs the Atomic Sync Ritual.

The orchestrator never implements code or documentation in bulk by itself — it routes each non-trivial item to the domain expert agent and collects results. Trivial text edits (e.g., a single-line update to a governance doc) MAY be executed directly via `Edit` without delegating, when delegation would add overhead without adding value.

### Agent Selection

The orchestrator selects the best agent for each delivery checklist item using these rules, applied in priority order:

0. **Suggested-executor annotation (HIGHEST priority)**: If the checkbox carries a `_Suggested executor: <agent-name>_` annotation per [Plan Anti-Hallucination Convention §Specialized-Agent Delegation](../../development/quality/plan-anti-hallucination.md#specialized-agent-delegation-hallucination-reduction), verify the agent file exists at `.claude/agents/<name>.md` and use that agent. The annotation is the plan author's explicit choice — it overrides heuristics 1–4 below. If the annotated agent does not exist, terminate the item with status `fail` and surface the missing-agent error to the user (do not silently fall back).

1. **Match by project/app name**: If the checklist item names a specific app (e.g., `organiclever-be`), use the agent for that app's language (e.g., `swe-rust-dev`). Refer to [CLAUDE.md](../../../CLAUDE.md) for the full app list and their tech stacks.

2. **Match by file extension**: If the item references files with a recognizable extension (`.ts`, `.java`, `.py`, `.go`, `.kt`, `.fs`, `.cs`, `.clj`, `.ex`, `.rs`, `.dart`), use the corresponding `swe-{language}-dev` agent.

3. **Match by content type**: If the item involves documentation (`docs/`, `README.md`), governance (`repo-governance/`), specs (`specs/`), or E2E tests (`*-e2e`, Playwright), use the appropriate content agent (`docs-maker`, `repo-rules-maker`, `readme-maker`, `specs-maker`, `swe-e2e-dev`).

4. **Match by framework/tool keywords**: If the item mentions a framework (Spring Boot, Ktor, FastAPI, Gin, Phoenix, Giraffe, Axum, Pedestal, Next.js, Flutter), use the agent for that framework's language.

5. **Fallback (direct execution)**: If no specialized agent cleanly matches — e.g., a one-line edit to a governance doc, a grep or file-move operation, an `npm` command — the orchestrator executes the item directly via `Edit` / `Bash` without delegating. Direct execution is only for trivial, context-bounded work; substantive changes always route through an agent.

**Rationale**: Domain-specialized agents hallucinate less than generic orchestration because they carry deeper language and framework context. The Suggested-executor annotation is the plan author's hallucination-reduction lever; respect it before falling back to heuristics.

**The above are heuristics, not a closed list.** As new agents or apps are added to the repository, the orchestrator adapts automatically by reading the available agent list from the agent definition directory and matching based on the agent's description and the checklist item's content. The orchestrator should always check what agents are currently available rather than relying on a static table.

**Multi-concern items**: When a delivery checklist item spans multiple task types (e.g., a
TypeScript backend change that also requires a README update), delegate each concern separately
to its appropriate agent. Execute the implementation agent first, then the documentation agent.

### Fan-Out, Ordering, and Delivery Shape

**Fan-out follows the N+1 model**: `1 main thread + N background agents = N+1 total`, default
**N=3**. The orchestrator keeps the main thread vacant and responsive — filling background slots
first — and never silently self-promotes beyond the plan's declared N. See the
[Agent Workflow Orchestration Convention](../../development/agents/agent-workflow-orchestration.md).

**Ordering is DAG-first**: the plan's `## Parallelization Model` declares which nodes are
independent. Independent nodes fan out up to N; dependent nodes serialize; **sequence is not
dependency**. The DAG's independent-node width is the fan-out — N only caps it.

**Delivery is 1-PR↔1-worktree**: each independent DAG node gets its own worktree, branch, and PR,
merged per-phase as it completes rather than batched at plan end. Cleanup is the terminal DAG node,
so a worktree is removed only once its own PR has landed and no in-flight node still needs it.

**Git operations stay non-destructive and self-scoped**: assume other agents and engineers share
this machine's disk, git object store, and worktrees. Never run an operation that discards a
concurrent actor's uncommitted work, and never remove a worktree or branch you did not create. See
[No Destructive Git Operations](../../development/workflow/no-destructive-git-operations.md) and
[Worktree and Artifact Cleanup](../../development/workflow/worktree-and-artifact-cleanup.md).

**Status cadence**: while checklist items are active, update the user every **3-5 minutes — not
faster**, anchored to meaningful state changes rather than a timer.

### Surface-Conditional Tester Gates

Which quality gates this execution must run depends on **what surface the plan ships**. The rule
binds here at execution, exactly as it bound at authoring time (see
[plan-planning §Surface-Conditional Tester Gates](./plan-planning.md#surface-conditional-tester-gates)),
and again as a merge precondition — clause (e) of the
[PR Review Quality Gate](../pr/pr-review-quality-gate.md)'s hardened preconditions.

- **UI-bearing plan** → run **both** [`ui/ui-quality-gate.md`](../ui/ui-quality-gate.md) (static)
  and [`web/web-ux-test-fixing-planning.md`](../web/web-ux-test-fixing-planning.md) (running triad).
- **API- or backend-bearing plan** → run [`api/api-quality-gate.md`](../api/api-quality-gate.md).
- **Both** → run both sets. **Neither** → the plan MUST state the exemption explicitly in
  `tech-docs.md`; an executor that finds no such statement treats it as a gap, not as a pass.

**The three UI gates are complementary, never substitutes**: `plan-checker` **Step 5k** gates the
UI **design funnel** in `prd.md` (pre-build); `ui/ui-quality-gate.md` gates the **built components**
statically via `swe-ui-checker` / `swe-ui-fixer` (no browser); and
`web/web-ux-test-fixing-planning.md` gates the **running UI** via the EWT/UWT/DWT triad in a real
browser. Passing one never discharges another.

## Task-Checklist Synchronization

The live Task list (`TaskCreate` / `TaskUpdate`) and the on-disk delivery checklist (`delivery.md`) are two views of the same state. They MUST agree at every moment of execution. Disagreement is a bug the orchestrator MUST detect and fix immediately.

- **Task list** — ephemeral, in-conversation. Its role is **real-time progress visibility for the user**. A reader watching the Task list is watching execution happen.
- **Delivery checklist** — persistent, on-disk. Its role is **survival across conversations**. It is the source of truth for plan completion state.

### 1:1 Mapping (strict)

Every checkbox on disk has exactly ONE matching task in the live list. Every task has exactly ONE matching checkbox on disk. This includes nested `- [ ]` sub-bullets — each sub-bullet is its own task, not rolled into its parent. Task titles short-form the checkbox text so reader sees consistent wording in both views.

Forbidden: coarse tasks ("Execute Phase 2", "Update all agents"), bulk creation ("one task for every phase"), silent completion ("ticked three boxes in one Edit, one `TaskUpdate` at the end"). Each of these breaks the user's monitoring view.

### Harness Task List as Primary Observability Surface

The harness task list (`TaskCreate` to add, `TaskUpdate` to mutate) is the user's only real-time view of execution. It is the **primary observability surface**, not a side artifact. The on-disk `delivery.md` checklist is the persistent source of truth; the harness list is its live mirror.

**Non-negotiable invariants**:

- **One checkbox = one harness task**. Every `- [ ]` in `delivery.md` (including every nested sub-bullet) maps to exactly one harness task created via `TaskCreate`. Every harness task maps back to exactly one checkbox.
- **Title short-form rule**. The task `subject` is a short-form of the checkbox prose: drop articles, keep verb + object, ≤80 characters. The reader watching the spinner MUST recognize the checkbox at a glance.
- **At most one `in_progress` task at any time**. Multiple `in_progress` tasks indicate the orchestrator is interleaving items — forbidden.
- **Sync lag ≤ one Edit call**. The on-disk checkbox state never lags more than a single `Edit` call behind the harness task state. If `TaskUpdate completed` fires before the matching `Edit` ticks the checkbox, the system is in an inconsistent state — roll back per the Atomic Sync Ritual below.

**Forbidden patterns** (violations of the above):

- Coarse tasks ("Execute Phase 2", "Update all agents", "Apply fixes")
- Bulk creation ("one task per phase" instead of one task per checkbox)
- Silent batch completion (multiple checkboxes ticked in one `Edit` while only one `TaskUpdate completed` fires)
- Late notes (closing a task before its implementation-notes block lands on disk under the ticked checkbox)
- Renaming a task to summarize multiple done items instead of leaving the original 1:1 mapping

If any of the above occur, the orchestrator MUST stop, reconcile (disk wins per the Resume Reconciliation rule below), and resume one checkbox at a time.

### Atomic Sync Ritual

For each checklist item, the following three steps happen together, in this order, without interleaving other items' work:

1. **Tick the checkbox**: `Edit` delivery.md to change `- [ ]` → `- [x]` for THIS one item (context-unique `old_string`, never `replace_all` on the whole file).
2. **Persist implementation notes** under the ticked checkbox in the same or an immediately-following `Edit` call — Date, Status, Files Changed, brief notes on what was done.
3. **`TaskUpdate completed`** the matching task. The live list now matches disk truth.

If any step fails, roll back the other two: untick the checkbox, remove the notes, leave the task in `in_progress`. The item is treated as incomplete.

### Resume Reconciliation (disk is truth)

When execution begins (or re-begins in a new conversation), disk state wins:

1. Read delivery.md top-to-bottom FIRST.
2. For every `- [x]` — skip, count as done.
3. For every `- [ ]` — `TaskCreate` one task in reading order.
4. If stale tasks from a prior run disagree with disk (e.g., task `completed` but checkbox `- [ ]`), delete the stale list and rebuild from current delivery.md.
5. Flag any `- [x]` lacking implementation notes — possible silent batch-tick; the user may want to audit before continuing.
6. **Resolve the plan path against the worktree, not the primary checkout.** For any plan whose delivery mode provisions a dedicated worktree (`worktree-to-pr`, `worktree-to-origin-main`), the worktree's copy of the plan folder is the ONLY authoritative on-disk location — it is the copy on the branch that becomes the PR. A same-named plan folder may still exist under the primary checkout's `plans/in-progress/` (e.g., left over from before the worktree was provisioned); reading or editing that copy instead is a silent-divergence trap — edits there never reach the branch, since the primary checkout isn't what gets pushed. If the same plan folder exists with uncommitted changes in BOTH the primary checkout and the worktree, treat it as a hard anomaly: stop, reconcile which content is accurate (verify independently against commit history / PR state, don't assume either copy), merge the genuinely-verified content into the worktree's copy, and flag the primary checkout's stray copy to the user for cleanup.

### Divergence handling

If a task is `completed` but the checkbox is `- [ ]`, OR a checkbox is `- [x]` but the matching task is not `completed`, state is inconsistent. Stop, reconcile disk vs list (disk wins), then resume.

## Iron Rules (Non-Negotiable)

These rules govern ALL execution steps. No exception. No shortcut.

1. **Granular Task Tracking (1:1 with delivery.md) — NON-NEGOTIABLE**: The harness task list IS the user's primary observability surface (see [Harness Task List as Primary Observability Surface](#harness-task-list-as-primary-observability-surface) above). Exactly ONE `TaskCreate` per delivery checklist item, including every nested `- [ ]` sub-bullet — sub-bullets are NEVER rolled into their parent. Task `subject` MUST short-form the checkbox text (drop articles, keep verb + object, ≤80 chars). At most ONE task in `in_progress` at any moment. Mark `in_progress` BEFORE any tool call advancing that item. Mark `completed` ONLY after the checkbox is ticked on disk AND the implementation-notes block is persisted under the ticked checkbox. FORBIDDEN: coarse tasks ("Execute Phase 2", "Apply fixes"), bulk creation ("one task per phase"), silent batch-completion (multiple checkboxes ticked in one `Edit` while one `TaskUpdate` closes), speculative completion (closing a task before disk reflects done state), title rewriting (renaming a task to summarize multiple items). Violations corrupt the user's view of execution and MUST trigger immediate rollback + reconciliation (disk wins).
2. **Never Stop Before All Done (except [HUMAN] gates)**: Execute ALL `[AI]` items from first to last without stopping. No pauses between phases for `[AI]` work. No skipping items. The acceptable stops are: a hard technical blocker, OR a `[HUMAN]` / `[AI+HUMAN]` checkbox (including a `[HUMAN]` phase gate). At a `[HUMAN]` item the orchestrator STOPS, surfaces the item to the user with its acceptance criterion, and waits for the human to confirm completion before resuming — this is a legitimate, expected stop per [Plans Organization Convention §Executor Tagging](../../conventions/structure/plans.md#executor-tagging--ai-vs-human-hard-rule). Unmarked checkboxes are treated as `[AI]`.
3. **Fix ALL Issues — Including Preexisting**: When ANY test, lint, typecheck, or quality gate fails — fix it. Even if it existed before your changes. Do NOT defer. Do NOT skip. Commit preexisting fixes separately.
4. **Delivery.md Is Sacred — Atomic Sync Ritual**: After each item's work is done, run the three-step ritual before touching the next item: (a) `Edit` checkbox `- [ ]` → `- [x]` for THIS one item (no `replace_all`), (b) `Edit` implementation-notes block under the ticked checkbox (Date, Status, Files Changed, brief notes), (c) `TaskUpdate completed`. All three MUST land before moving on. If any step fails, roll back the others and leave the task in `in_progress`. Ticking multiple checkboxes in one Edit or deferring notes to end-of-phase is forbidden.
5. **Local Quality Gates Before Push**: Run `npx nx affected -t typecheck lint test:quick specs:coverage` before every push. Fix ALL failures. Do NOT push with any failing check.
6. **Post-Push CI Verification**: After every push, monitor ALL GitHub Actions workflows. Fix ALL failures (including preexisting). Do NOT proceed until CI is fully green.
7. **Thematic Commits**: Group related changes. Split different concerns. Follow Conventional Commits. Preexisting fixes get their own commits.
8. **Manual Behavioral Assertions**: After quality gates pass, use Playwright MCP for web UI verification and curl for API verification. Fix any broken behavior before proceeding.
9. **Progress Streaming (Observability)**: The live Task list is the user's monitoring window — keep it fresh in real time. Never run silent for more than one checkbox. After each phase completes, emit a one-line user-visible status: phase name, items ticked / total, files changed, any preexisting fixes.
10. **Resume Reconciliation (Disk Is Truth)**: When starting or re-entering execution, read delivery.md first. Rebuild the Task list from disk state. If in-memory tasks disagree with disk checkboxes, delete them and rebuild. Never trust in-memory state over disk.

## Steps

### 0. Enter the Designated Worktree (Sequential, Hard Gate)

Plan execution happens on the plan's **work branch**, synced to the latest `origin/main`. The work branch is chosen by precedence: (1) a branch the **user explicitly specifies at invocation** — a dedicated worktree, the `main` checkout, or any other existing branch — wins; (2) if the user specifies nothing, the **plan docs win** — the plan's `## Worktree` section (or declared work branch) governs, and absent any override that defaults to a dedicated worktree provisioned from `origin/main`. Whichever branch is selected, the executor's **default first action is to pull the latest `origin/main` into that work branch** before any implementation, to minimize merge collisions later at push time. Executing a plan from a **stale** work branch — one not synced to the latest `origin/main` — is forbidden.

**Delivery-mode resolution (same three-tier precedence)**: alongside the work-branch precedence above, the executor also resolves the plan's active **delivery mode**, using the identical three-tier pattern: (1) a mode given as an **invocation argument** wins; (2) if none is given, the plan's own `## Delivery Mode` declaration wins; (3) absent either, the default is **`worktree-to-pr`**. See [Plans Organization Convention §Delivery Mode](../../conventions/structure/plans.md#delivery-mode) for the full four-mode table and the precedence algorithm. The resolved mode determines which work-location branch below applies:

- `worktree-to-pr` and `worktree-to-origin-main` — work happens in a dedicated **worktree**; follow the worktree provisioning and entry steps below.
- `main-to-origin-main` and `main-to-pr` — work happens directly in the **primary checkout**; skip worktree provisioning entirely per the "Work-branch provisioning vs. entry" note immediately below, and apply the freshness gate (step 5) directly to the primary checkout.

The resolved delivery mode also determines the per-phase push target (Steps 2b/2c) and the finalization/archival path (Step 8) — each of those steps documents its mode-specific behavior.

**Work-branch provisioning vs. entry**: when the work branch is a dedicated worktree (the default-when-unspecified case), follow the provisioning and entry steps below. When the user specifies the `main` checkout or another existing branch, skip provisioning (orchestrator-action steps 1–4): confirm you are on that branch, then apply the freshness gate (step 5) directly to it.

**Orchestrator action**:

1. **Locate the `## Worktree` section** in the plan:
   - **Multi-file plans**: in `delivery.md` (top-level `## Worktree` heading, before any phase).
   - **Single-file plans**: in `README.md` (top-level `## Worktree` heading, before `## Delivery Checklist`).
2. **If the section is missing AND the user specified no work branch at invocation**: terminate immediately with status `fail`. Emit a single user-visible line: `Worktree specification missing — add a "## Worktree" section to <delivery.md|README.md> per repo-governance/conventions/structure/plans.md#worktree-specification before re-invoking plan execution.` (If the user specified a work branch — a worktree, `main`, or any existing branch — that selection wins per the precedence above and a missing `## Worktree` section is not a failure; skip provisioning and apply the freshness gate to that branch.)
3. **Parse the declared worktree path** (format: `worktrees/<plan-identifier>/`).
4. **Go to the designated worktree — navigate or provision** (default behavior; no user prompt needed):
   - Check whether the worktree is already registered: `git worktree list --porcelain` from the repo root, and confirm the directory `<repo-root>/worktrees/<plan-identifier>` exists.
   - **If it exists**: make it the execution root. If the current working directory is not already inside it, switch to it (e.g., `cd <repo-root>/worktrees/<plan-identifier>` or the harness's worktree-entry tool). Emit: `Worktree gate: entering existing worktree at worktrees/<plan-identifier>/`.
   - **If it does not exist**: auto-provision it from the latest `origin/main`:
     1. Emit a user-visible line: `Auto-provisioning worktree at worktrees/<plan-identifier>/…`
     2. From the repo root run:

        ```bash
        git fetch origin
        git worktree add -b <plan-identifier> worktrees/<plan-identifier> origin/main
        ```

        If the branch `<plan-identifier>` already exists (e.g., a prior worktree was removed but its branch kept), reuse it instead: `git worktree add worktrees/<plan-identifier> <plan-identifier>`.

     3. If `git worktree add` fails (e.g., path already exists as a stale entry), run `git worktree prune` and retry once; if it still fails, terminate with status `fail` and emit the error output verbatim.
     4. Run `npm install && npm run doctor -- --fix` in the root repository worktree to initialize the toolchain, per [Worktree Toolchain Initialization](../../development/workflow/worktree-setup.md).
     5. Emit a user-visible line: `Worktree provisioned at worktrees/<plan-identifier>/ — continuing execution.`

5. **Freshness gate — pull latest `origin/main` into the work branch FIRST, by default (MANDATORY)**: before ANY implementation work, bring the work branch up to date by pulling the newest `origin/main`. Pulling latest trunk first is the default — it minimizes merge collisions at push time:
   1. `git fetch origin` (from inside the work branch).
   2. If the work branch has uncommitted changes (`git status --porcelain` non-empty): do NOT auto-stash or discard. Surface the dirty state to the user and STOP until they decide (commit, stash, or discard explicitly).
   3. If the work branch has no local commits ahead of `origin/main`: `git merge --ff-only origin/main`.
   4. If the work branch has local commits not yet on `origin/main` (a resumed plan): `git rebase origin/main`. On conflict: `git rebase --abort`, surface the conflicting files to the user, and STOP — never auto-resolve.
   5. Verify sync: `git merge-base --is-ancestor origin/main HEAD` must succeed.
6. **Confirm gate passed**: emit `Worktree gate: passed (worktrees/<plan-identifier>/ @ <short-sha>, up to date with origin/main)` and proceed to Step 1. All subsequent steps run with the worktree as the execution root.

**Secret/State-Dependent Infrastructure Operations Run from the Primary Checkout**

A worktree provisioned from `origin/main` contains no gitignored secrets or local infrastructure state. Credential files (`.env` and similar) and any local-backend infrastructure-state file (for example a Terraform state file) are gitignored and exist only in the primary checkout. Because of this, secret- or state-dependent infrastructure operations — `terraform apply`, a live Ansible converge (`ansible-playbook` against real hosts), or any equivalent state-changing infra operation — MUST run from the primary checkout as `[HUMAN]` / operator steps, never from the plan's worktree. Running `terraform apply` from a worktree that has no state causes Terraform to see an empty state and attempt to recreate the entire managed estate; copying state into a worktree creates split-brain, with two checkouts mutating real infrastructure against divergent state copies. Keeping these operations in the primary checkout keeps all secret-bearing, state-changing work in a single location.

Mark such steps `[HUMAN]` in the delivery checklist (per [Plans Organization Convention §Executor Tagging](../../conventions/structure/plans.md#executor-tagging--ai-vs-human-hard-rule)) and instruct the operator to run them from the primary checkout where the secrets and state reside.

**Output**: Execution running inside the designated worktree, up to date with the latest `origin/main` (provisioned if needed).

**Why this is a hard gate**: A missing `## Worktree` section is a hard-fail **only when the user has not specified a work branch at invocation** — in that case there is no declared path to provision, so the plan is incomplete and must be fixed by the author before execution can proceed. A CWD mismatch, by contrast, is recoverable: the executor knows the target path and navigates to or provisions the worktree automatically. Running outside a worktree without a declared path would pollute the main checkout with in-flight work, break the parallel-safety guarantee, and risk dirty-gitlink hazards in any subrepo context. The freshness sync is equally mandatory: implementing against a stale base invites merge conflicts at push time and validates the plan against code that no longer matches `origin/main`.

### 1. Load Delivery Checklist and Materialize Task List (Sequential)

Read the plan in full, reconcile against any prior run's state, and build the live Task list to mirror disk truth — before any implementation work begins.

**Orchestrator action**:

- Read the plan at `{input.plan-path}` — all five docs if present (`README.md`, `brd.md`, `prd.md`, `tech-docs.md`, `delivery.md`) or the legacy four-doc layout (`requirements.md` in place of `brd.md` + `prd.md`).
- Locate the delivery checklist — typically `delivery.md` adjacent to the plan, or embedded in a single-file plan's `README.md`.
- **Resume Reconciliation (Iron Rule 10)**: parse every checkbox top-to-bottom. For each `- [x]`, count it as done and skip it. For each `- [ ]`, queue it for task creation in reading order. If a stale Task list from a prior run disagrees with disk, delete it and rebuild.
- **Full granularity parsing (Iron Rule 1)**: identify every `- [ ]` AND every nested `- [ ]` sub-bullet. Nested sub-bullets are NOT rolled into their parent — each gets its own task.
- **`TaskCreate` one task per remaining checkbox**, in reading order. Task titles short-form the checkbox text for monitoring parity.
- **Verify 1:1 mapping** before moving on: `count(remaining - [ ] in delivery.md) == count(newly-created tasks)`. Diverging counts indicate a parsing bug — stop and reconcile.
- Do NOT call `TaskUpdate in_progress` yet; that happens at Step 2 when the loop actually begins on an item.

**Output**: Live Task list mirrors delivery.md remaining items 1:1, plan context loaded.

**On failure**: Terminate workflow with status `fail`.

**Notes**:

- Tasks map 1:1 to checkboxes, including nested sub-bullets — NEVER group multiple items into one task, NEVER roll sub-bullets into their parent.
- Tasks must be granular — one concrete action per task.
- Preserve the exact phase and item ordering from delivery.md in the Task list.
- Already-ticked items are skipped — the plan is resumable across conversations; disk is truth.

### 1b. Environment Setup (Sequential)

Before implementing anything, ensure the development environment is ready.

**Note**: The first phase of every delivery checklist must be **Phase 0: Environment Setup and Baseline**, executed by the `repo-setup-manager` agent. Phase 0 covers `npm install`, `npm run doctor -- --fix`, a baseline test run, and preexisting failure resolution. If the delivery checklist contains a Phase 0, delegate it to `repo-setup-manager` before proceeding to Step 2. The steps below are the orchestrator-level mirror of Phase 0 — they describe what must be true before any plan work begins.

**Orchestrator action**:

- Run `npm install` to ensure dependencies are current
- Run `npm run doctor` to verify all tooling is installed
- Set up project-specific requirements (env vars, DB, Docker, etc.) as specified in the plan
- Verify dev server starts for affected projects
- Run existing quality gates to establish a baseline: `npx nx affected -t typecheck lint test:quick`
- Note any preexisting failures — these MUST be fixed during execution (Iron Rule 3)

**Output**: Environment ready, baseline failures identified

**On failure**: If environment cannot be set up, terminate with status `fail`.

### 2. Initial Execution (Sequential, Continuous)

Execute all delivery checklist items sequentially, delegating each to the appropriate specialized agent.

**Orchestrator**: calling context (top-level assistant session)

**Execution loop** — single-item, strictly sequential. Rule 1 (granularity) and Rule 4 (atomic sync ritual) are enforced in this loop:

For each checklist item in reading order (phase by phase, item by item, including nested sub-bullets):

1. **`TaskUpdate in_progress`** on the matching task. At most ONE `in_progress` at a time.
2. **Pre-Item Repo-Grounding (HARD GATE — Anti-Hallucination)**: before delegating, repo-ground every claim in the checkbox per the [Plan Anti-Hallucination Convention §Repo-Grounding Rule](../../development/quality/plan-anti-hallucination.md#repo-grounding-rule-hard):
   - For each cited file path: `Bash test -f <path>`. If missing AND not marked `_New file_`: HALT the item, escalate to user with the failing path (do not invent a substitute).
   - For each cited Nx target: `jq -r '.targets | keys[]' apps/<project>/project.json | grep -qx '<target>'`. If missing AND not marked `_New target_`: HALT the item.
   - For each cited agent: `test -f .claude/agents/<name>.md`. If missing: HALT (no fabricating).
   - For each cited symbol: `Grep` for evidence. Missing AND not marked `_New symbol_`: HALT.
   - **Refuse-on-uncertainty**: if a cited fact cannot be grounded and the checkbox does not mark it as new, the orchestrator MUST escalate rather than guess. Surface the failure to the user with the specific claim and the missing artifact.
3. **Analyze the item** to determine whether to delegate to a specialized agent (see Agent Selection) or execute directly. If the checkbox carries a `_Suggested executor:_` annotation, use that agent (Priority 0). If the checklist text is otherwise ambiguous, the orchestrator MAY consult the plan's `brd.md` / `prd.md` / `tech-docs.md` for additional context — business intent lives in `brd.md`, product scope and Gherkin acceptance criteria in `prd.md`, architecture decisions in `tech-docs.md`.
4. **Execution-marker check (`[AI]`/`[HUMAN]`)** — read the checkbox's execution marker (per [Plans Organization Convention §Executor Tagging](../../conventions/structure/plans.md#executor-tagging--ai-vs-human-hard-rule)). `[AI]` or unmarked → execute normally (next bullet). `[HUMAN]` (or the human portion of an `[AI+HUMAN]` item) → the orchestrator MUST NOT attempt it: surface the item to the user verbatim with its acceptance criterion and any context they need, then STOP and wait for the user to confirm it is done before ticking the checkbox and continuing. For `[AI+HUMAN]`, perform the agent-preparable portion first, then hand off the human portion. This is a sanctioned stop (see Stopping rules) — not a violation of "never stop between phases."
5. **Execute the item** — delegate to that agent via the Agent tool, or perform the edit/command directly. Only for THIS one checkbox.
6. **Verify the work succeeded** — read the produced file, run the command, check the agent's output. The verification MUST match the acceptance criterion stated in the checkbox (Execution-Grade Clarity rule from the plans convention).
7. **Knowledge Capture — running log (as-you-go)**: append a sanitized entry to `learnings.md`
   whenever this item surfaces a generalizable learning.
   - A workaround invented, a wrong assumption corrected, a tool/CLI quirk discovered, or any
     insight passing the "would the system catch this next time?" litmus qualifies; skip silently
     when no such learning surfaces from this item.
   - Create `learnings.md` (sibling of `delivery.md`) on first use if it does not yet exist.
   - See the [Knowledge Capture Convention](../../development/quality/knowledge-capture.md) for
     entry shape and the secret/sensitivity sanitization rule.
8. **Atomic Sync Ritual** — all three steps before any next-item work:
   a. `Edit` delivery.md to change `- [ ]` → `- [x]` for THIS one item (context-unique `old_string`; never `replace_all`; never tick multiple items in one Edit call).
   b. `Edit` delivery.md to add the implementation-notes block (Date, Status, Files Changed, brief notes) under the ticked checkbox. Notes MUST themselves be repo-grounded — only state files actually modified, only quote commands actually run.
   c. `TaskUpdate completed` on the matching task.
9. Proceed IMMEDIATELY to the next item — no pausing, no waiting for approval, no deferring notes.

Nested sub-checkboxes iterate the same loop. A parent `- [ ]` can only be ticked after all its sub-`- [ ]` items have each completed steps 1–6 of the loop.

**Progress streaming**: keep the live Task list fresh by executing the ritual after every item. Never queue up two or three item's worth of `completed` updates. After each phase boundary, emit a one-line user-visible status (phase, items ticked / total, files changed, preexisting fixes).

**Output**: `{execution-started}` — all delivery checklist items completed, checklist updated, Task list shows disk truth.

**Success criteria**: Every `- [ ]` that started the phase is now `- [x]` with implementation notes; every matching task is `completed`.

**On failure**: If a delegated agent fails and cannot resolve the issue, terminate with status `fail`. If the failure is recoverable, retry once before escalating. If the ritual partially lands (checkbox ticked but notes missing, or task marked completed but checkbox still `- [ ]`), roll back and treat the item as incomplete.

**Stopping rules**:

- Stop ONLY if a task fails and CANNOT be resolved after retry.
- Stop ONLY if a critical decision requires user input that cannot be inferred.
- Stop at a `[HUMAN]` step (sanctioned) — surface the action to the user and resume on confirmation per the Execution-marker check above. This is the one routine non-technical stop and does NOT violate "never stop between phases."
- Stop ONLY when ALL items are complete.
- NEVER stop between phases for approval — but DO verify the phase's `### Phase N Gate` is green before starting the next phase (a self-run verification checkpoint, not a wait-for-user pause); fix any failing gate check within the current phase first.
- NEVER batch-tick checkboxes, batch-complete tasks, or defer implementation notes.
- NEVER skip an item — if genuinely not applicable, add a note explaining why and tick it.

### 2b. Per-Phase Quality Gate (Sequential, After Each Phase)

After completing all items in a delivery phase, verify the phase's authored gate and run quality gates before proceeding.

**Orchestrator action**:

0. **Verify the phase's `### Phase N Gate` (barrier)**: run every check listed under the phase's `### Phase N Gate` heading and confirm each passes its stated acceptance. A phase is **not complete until its gate is green** — do NOT start phase N+1 while any gate check is failing; fix it within the current phase first. If the gate carries a **Pause Safety** note, the post-gate state is a sanctioned safe-to-stop point. (Gate checks assert on patterns/placeholders, never a real secret literal.) See [Plans Organization Convention §Phases as Natural Pauses With Clear Gates](../../conventions/structure/plans.md#phases-as-natural-pauses-with-clear-gates-hard-rule).
1. Run local quality gates:

   ```bash
   npx nx affected -t typecheck
   npx nx affected -t lint
   npx nx affected -t test:quick
   npx nx affected -t specs:coverage
   ```

2. If the plan involves integration or e2e tests, also run:

   ```bash
   npx nx affected -t test:integration
   npx nx affected -t test:e2e
   ```

3. **Fix ALL failures** — including preexisting ones (Iron Rule 3)
4. Re-run failing checks to confirm resolution
5. Commit thematically (Iron Rule 7) — separate plan work from preexisting fixes
6. Push to the resolved delivery mode's target (Iron Rule 5), only after ALL local quality gates pass. The push target depends on the delivery mode resolved in Step 0:
   - **`worktree-to-origin-main` / `main-to-origin-main`** (direct-push modes): push directly to `origin main`.
   - **`worktree-to-pr` / `main-to-pr`** (`*-to-pr` modes): push to the **PR branch of the DAG node being delivered**. Each independent node gets its own worktree, branch, and PR — a strict **one worktree → one branch → one PR → one node** mapping (see [plan-planning §Planning Granularity](./plan-planning.md#planning-granularity)). If no PR exists yet for this branch, open one on its first push (`gh pr create --base main --head <branch> --title "<plan-identifier>: <node>" --body "<summary>"`, draft or non-draft per plan/user preference). Genuinely dependent phases that cannot be separated share one PR; independent ones do not. CI is monitored on the PR itself, not on `main` — see Step 2c.

   **Per-phase merging (not batch merging)**: each phase PR is **opened and merged** as that phase completes, once the hardened merge preconditions hold. Do **not** hold phase PRs open for a batch merge at plan end — that re-serialises work the DAG declared independent and grows the divergence each PR must reconcile. The **merge actor** is `[AI]` by default; `[HUMAN]` applies only where the plan's own step declares that gate. Partial work reaches `main` **merged but dark** behind a feature flag rather than waiting on a long-lived branch.

   **The worktree is the unit of cleanup**: because the mapping is one worktree per PR, a node's worktree is removed when **its** PR lands — not deferred to plan end. Cleanup is the terminal node of the DAG and depends on every delivery node, so it can never remove a worktree an in-flight node still needs. See [Worktree and Artifact Cleanup](../../development/workflow/worktree-and-artifact-cleanup.md).

**Output**: All quality gates passing, changes pushed

**On failure**: Fix failures and retry. Do NOT proceed to next phase with failures.

### 2c. Post-Push CI Verification (Sequential, After Each Push)

After every push, verify CI on the resolved delivery mode's target — `origin main` for the direct-push modes (`worktree-to-origin-main`, `main-to-origin-main`), the PR branch for the `*-to-pr` modes (`worktree-to-pr`, `main-to-pr`).

**Monitoring tool**: The required default for standard CI jobs (10–35 min) is `ScheduleWakeup` + a single `gh run view` (direct-push modes) or `gh pr checks` (`*-to-pr` modes) call on wakeup (2 API calls total per run). Use `gh run watch <run-id>` (or tight polling of `gh pr checks`) only if the job is expected to complete in under 5 minutes — both poll every ~3 s and exhaust the GitHub API rate limit (5,000 req/hour) on any job longer than ~5 min. Manual tight-loop polling without a sleep interval is also **forbidden**. See [CI Monitoring Convention](../../development/workflow/ci-monitoring.md) for required tooling, minimum poll intervals, trigger discipline, and rate-limit recovery procedures.

**Orchestrator action — `worktree-to-origin-main` / `main-to-origin-main` (direct push to `origin main`)**:

1. Identify which GitHub Actions workflows were triggered by the push
2. Find the run ID: `gh run list --workflow=<workflow-file> --limit=3`
3. Monitor to completion using the correct approach for the job duration:
   - **Standard jobs (10–35 min, required default)**: `ScheduleWakeup(delaySeconds=120)` (2 min), check with one `gh run view <run-id> --json conclusion,status,jobs`, repeat every 2-5 min until complete
   - **Short jobs (<5 min only)**: `gh run watch <run-id>` — do NOT use for 20–35 min CI jobs
   - Never use `gh run watch` on jobs expected to take 20–35 min — it polls every ~3s and exhausts API quota
4. If ANY workflow fails:
   - Pull failure logs and diagnose the root cause: `gh run view <run-id> --log-failed`
   - Fix locally (including preexisting CI failures — Iron Rule 3)
   - Run local quality gates again (Step 2b)
   - Push fix commit
   - Monitor CI again with `ScheduleWakeup` + single `gh run view` (or `gh run watch` if <5 min)
5. Repeat until ALL GitHub Actions workflows pass with zero failures
6. Do NOT proceed to the next delivery phase until CI is fully green
7. If rate-limited (HTTP 403 from `gh`): stop all `gh` calls immediately, use `ScheduleWakeup(delaySeconds=2100)` (35 min) to resume after the rolling window clears — do NOT spin in a retry loop

**Orchestrator action — `worktree-to-pr` / `main-to-pr` (PR branch)**:

1. Identify the PR: `gh pr view <PR> --json number,url,headRefName` (the PR opened in Step 2b for this plan's branch)
2. Check status: `gh pr checks <PR>` — lists every required check and its conclusion for the PR's current head commit
3. Monitor to completion using the correct approach for the job duration:
   - **Standard jobs (10–35 min, required default)**: `ScheduleWakeup(delaySeconds=120)` (2 min), check with one `gh pr checks <PR>` call, repeat every 2-5 min until every check reports a conclusion
   - **Short jobs (<5 min only)**: poll `gh pr checks <PR>` at short intervals — do NOT use for 20–35 min CI jobs
   - Never tight-loop `gh pr checks` without a sleep interval — it exhausts the GitHub API rate limit the same way `gh run watch` does
4. If ANY check fails:
   - Pull failure logs for the failing run (`gh run view <run-id> --log-failed`, with `<run-id>` found via the failing check's linked run in `gh pr checks <PR>` output)
   - Fix locally (including preexisting CI failures — Iron Rule 3)
   - Run local quality gates again (Step 2b)
   - Push the fix commit to the **PR branch** (never to `main`)
   - Monitor again with `ScheduleWakeup` + a single `gh pr checks <PR>` call
5. Repeat until ALL checks on the PR pass with zero failures
6. Do NOT proceed to the next delivery phase until the PR's CI is fully green
7. If rate-limited (HTTP 403 from `gh`): identical recovery to the direct-push path — `ScheduleWakeup(delaySeconds=2100)` (35 min), no retry loop

**Output**: All CI checks passing on the resolved target (`origin main` or the PR)

**On failure**: Keep fixing and pushing until CI is green. If stuck after 3 attempts on the same failure, escalate to user.

### 2d. Manual Behavioral Assertions (Sequential, After Each Phase)

After CI is green, manually verify actual application behavior using Playwright MCP and curl.
Evidence MUST be captured: screenshots committed to the plan's `evidence/` subfolder and
referenced in `delivery.md`; curl responses inlined as fenced code blocks. "Verified manually"
without evidence is incomplete. See [Evidence Capture Convention](../../development/quality/evidence-capture.md).

**Orchestrator action**:

1. **For Web UI changes** — use Playwright MCP tools across ALL supported locales and breakpoints:
   - Discover supported locales: read `apps/<app>/src/features/i18n/` or `apps/<app>/next.config.ts`
   - Start dev server: `nx dev [project-name]`
   - For EACH locale (e.g., `en`, `id`) × EACH breakpoint (375 px, 768 px, 1280 px):
     - `browser_resize(width, 900)`
     - `browser_navigate` to the locale-prefixed URL (e.g., `/en/page`, `/id/page`)
     - `browser_snapshot` to inspect rendered DOM; verify `html[lang]` matches the locale
     - `browser_console_messages` to check for JS errors
     - `browser_network_requests` to verify API calls
     - `browser_take_screenshot` — save to `evidence/phase-{N}-{description}-{locale}-{breakpoint}px.png`
   - `browser_click`, `browser_fill_form` to test interactive flows (any locale sufficient for flow)
   - Record screenshot paths in `delivery.md` under the relevant checkbox per the Evidence Capture Convention
2. **For API changes** — use curl via Bash:
   - Start backend server: `nx dev [project-name]`
   - Hit affected endpoints with curl and verify response status, shape, and data
   - Test error cases with invalid payloads
   - For locale-sensitive APIs (localized messages, locale-dependent formatting), verify with
     `Accept-Language` header for EACH supported locale
   - Inline the command, HTTP status, and response body (or first 20 lines) in `delivery.md` as
     fenced code blocks; save long responses (> 20 lines) to `evidence/phase-{N}-{endpoint}.txt`
3. **For full-stack changes** — run BOTH Playwright MCP and curl:
   - Verify UI renders correctly in ALL locales at ALL breakpoints
   - Verify API responds correctly
   - Verify the full flow (UI action → API call → response → UI update)
4. **Fix any broken behavior** — including preexisting issues (Iron Rule 3)
5. **Document evidence** in `delivery.md` under each ticked checkbox:
   - Screenshot references via Markdown image syntax pointing at `./evidence/phase-N-...-{locale}-{breakpoint}px.png`
   - curl commands, status codes, response bodies as fenced code blocks
   - Console-clean confirmation per locale

**Output**: All manual assertions pass, application behavior verified, evidence committed in
`evidence/` with `delivery.md` references

**On failure**: Fix broken behavior, re-run assertions. Do NOT proceed to next phase with broken UI or API.

**Notes**:

- This step is MANDATORY when the plan touches web UI or API code
- Skip ONLY if the plan touches no UI and no API (e.g., pure documentation or governance changes)
- For multi-locale apps, testing ONLY the default locale is INCOMPLETE — verify ALL locales
- Playwright MCP provides real browser interaction — use it to catch rendering, JS, and integration issues that automated tests may miss
- curl provides direct HTTP verification — use it to catch response format, status code, and data issues
- See [Evidence Capture Convention](../../development/quality/evidence-capture.md) for screenshot naming, locale requirements, and delivery.md format

### 3. Validation (Sequential)

Validate the implementation against plan requirements.

**Agent**: `plan-execution-checker`

- **Args**: `plan: {input.plan-path}`
- **Output**: `{audit-report-1}` — Initial validation report in `generated-reports/`
- **Depends on**: Step 2 completion

**Success criteria**: Checker completes and generates validation report.

**On failure**: Terminate workflow with status `fail`.

**Notes**:

- Validates implementation against plan requirements
- Checks all deliverables meet quality standards
- Verifies delivery checklist completion
- Generates progressive report with all findings (CRITICAL, HIGH, MEDIUM, LOW)

### 4. Check for Findings (Sequential)

Analyze validation report to determine if further execution is needed.

**Condition Check**: Count ALL findings (CRITICAL, HIGH, MEDIUM, and LOW) in `{step3.outputs.audit-report-1}`

- If findings > 0: Proceed to step 5 (Continue Execution)
- If findings = 0: Skip to step 8 (Finalization - Success)

**Depends on**: Step 3 completion

**Notes**:

- Includes all finding levels — missing requirements, incomplete deliverables, quality issues
- Zero findings required for success (perfect quality standard)
- Reports which requirements still need work

### 5. Continue Execution (Sequential, Conditional)

Address findings and continue implementation by delegating to appropriate specialized agents.

**Orchestrator**: calling context (top-level assistant session)

- **Inputs**: `{plan: {input.plan-path}, focus: {findings-from-latest-report}}`
- **Output**: `{additional-work-completed}` — More checklist items completed, findings addressed
- **Condition**: Findings exist from step 4 or step 7
- **Depends on**: Step 4 completion (first iteration) or Step 7 completion (subsequent iterations)

**Execution loop** (same rules as Step 2):

For each finding from the latest validation report:

1. Analyze the finding to determine the correct specialized agent
2. Delegate the remediation to that agent via the Agent tool
3. Verify the agent resolved the finding successfully
4. **Atomic sync**: If the finding corresponds to an unchecked item, tick BOTH the delivery
   checklist (`- [x]`) and the task (`completed`) in the same step
5. Proceed immediately to the next finding

**Success criteria**: The orchestrator addresses all findings without stopping between them.

**On failure**: Log errors, proceed to step 6 for verification.

**Notes**:

- Orchestrator focuses on addressing specific findings while continuing overall plan execution
- Updates delivery checklist with resolved items
- May delegate to new requirements or fix quality issues
- Continues from previous work, does not restart from scratch

### 6. Re-validate (Sequential)

Run validation again to verify findings resolved and no new issues introduced.

**Agent**: `plan-execution-checker`

- **Args**: `plan: {input.plan-path}`
- **Output**: `{audit-report-N}` — Verification validation report
- **Depends on**: Step 5 completion

**Success criteria**: Checker completes validation.

**On failure**: Terminate workflow with status `fail`.

**Notes**:

- Verifies all findings from previous report are resolved
- Checks no new issues were introduced during fixes
- Generates fresh validation report with current status

### 7. Iteration Control (Sequential)

Determine whether to continue execution or terminate.

**Logic**:

- Count ALL findings in `{step6.outputs.audit-report-N}` (CRITICAL, HIGH, MEDIUM, LOW)
- If findings = 0: Proceed to step 8 (Finalization - Success)
- If findings > 0 AND iterations < max-iterations: Loop back to step 5 with new report
- If findings > 0 AND iterations >= max-iterations: Proceed to step 8 (Finalization - Partial)

**Depends on**: Step 6 completion

**Notes**:

- Prevents infinite loops with max-iterations limit
- Continues until ZERO findings of any criticality level
- Each iteration uses the latest validation report
- Tracks iteration count for observability

### 8. Finalization and Archival (Sequential)

Report final status, archive plan if successful, and update all related READMEs.

**UI-bearing plan pre-archival gate (rules 1, 10, 15)**: For plans that add or change user-facing
screens or components, archival MUST NOT proceed until the production visual sign-off is confirmed
(rule 1 — a human or Playwright observer verifies rendered output against the design mockups in the
live or staging environment). Zero automated-gate findings are necessary but not sufficient. See
[User-Facing Delivery Hardening Convention](../../development/quality/user-facing-delivery-hardening.md)
rules 1, 10, and 15.

**API-bearing plan pre-archival gate (rule 16)**: For API feature-change plans (REST or GraphQL
endpoints in a backend or tRPC app), archival MUST NOT proceed until the near-end
`api-exploratory-tester` retest has run against the running endpoint(s) and every resulting `AET-###`
defect checkbox in `delivery.md` is `- [x]` (fixed) — exactly as the rule-15 retest gates UI plans. See
[User-Facing Delivery Hardening Convention](../../development/quality/user-facing-delivery-hardening.md)
rule 16.

**Rule-15 web-UI three-tester retest (near-end, before archival)**: For **web-UI feature-change**
plans specifically, after the implementation lands and the rule-1 visual sign-off is recorded, run a
**three-tester** round against the running target URL(s) across all supported locales — the
[`web-ux-test-fixing-planning`](../web/web-ux-test-fixing-planning.md) workflow:
`web-exploratory-tester` (correctness), `web-usability-tester` (usability), and `web-design-tester`
(design fidelity). Invoke each tester with **`output-mode: delivery`** and the executing plan's
`plan-path`; this is the unified mechanism that appends findings directly into THIS plan's
`delivery.md` rather than filing a separate plan. Its output is folded back into THIS plan, not a separate plan:

1. Each tester with `output-mode: delivery` appends each finding to `delivery.md` as a **new
   unchecked task-list checkbox**, source-attributed (`- [ ] EWT-NNN:` / `- [ ] UWT-NNN:` /
   `- [ ] DWT-NNN: <defect> — fix before archival`), and each SG-### spec-gap / USS-### spec-suggestion
   as its own unchecked checkbox folded into the specs/\*\* coverage steps. Findings land in a clearly
   labelled "Rule-15 three-tester retest follow-ups" section at the end of the checklist.
2. Each new checkbox materializes as exactly one harness task per the
   [Task-Checklist Synchronization](#task-checklist-synchronization) 1:1 mapping, giving the user
   live visibility of the retest backlog.
3. Loop back into execution (Steps 2–7) to fix each finding and tick its checkbox via the Atomic
   Sync Ritual. Every EWT-NNN/UWT-NNN/DWT-NNN defect finding MUST be fixed and ticked — deferral
   of a defect finding requires explicit user permission and is allowed only when the fix is genuinely impossible. (`SG-###` spec-gap proposals and `USS-###` spec-suggestions
   are proposals, not defects, and may be triaged or deferred with written rationale recorded under
   the checkbox.)
4. Archival is blocked until every rule-15 EWT/UWT/DWT defect checkbox is `- [x]` (fixed).

**Rule-16 API exploratory retest (near-end, before archival)**: For **API feature-change** plans
specifically (REST or GraphQL endpoints in a backend or tRPC app), after the implementation lands and
the contract (OpenAPI 3.x / GraphQL SDL) is updated, run a near-end `api-exploratory-tester` round
against the running endpoint(s). This is the API-surface counterpart to the rule-15 web triad — a
**single specialist tester**, no dedicated workflow, because the API surface has one exploratory lens.
Invoke it with **`output-mode: delivery`** and the executing plan's `plan-path`; its output is folded
back into THIS plan's `delivery.md`, not a separate plan, by the same mechanism as Rule 15:

1. `api-exploratory-tester` with `output-mode: delivery` appends each finding to `delivery.md` as a
   **new unchecked task-list checkbox**, source-attributed (`- [ ] AET-NNN: <defect> — fix before
archival`), and each `SG-###` spec-gap as its own unchecked checkbox folded into the specs/\*\*
   coverage steps. Findings land in a clearly labelled "Rule-16 API exploratory-test retest follow-ups"
   section at the end of the checklist.
2. Each new checkbox materializes as exactly one harness task per the
   [Task-Checklist Synchronization](#task-checklist-synchronization) 1:1 mapping, giving the user live
   visibility of the retest backlog.
3. Loop back into execution (Steps 2–7) to fix each finding and tick its checkbox via the Atomic Sync
   Ritual. **Exactly as with the rule-15 web-triad findings, every `AET-NNN` defect finding MUST be
   fixed and ticked during execution** — deferral of a defect finding requires explicit user permission
   and is allowed only when the fix is genuinely impossible. (`SG-###` spec-gap proposals are proposals,
   not defects, and may be triaged or deferred with written rationale recorded under the checkbox.)
4. Archival is blocked until every rule-16 `AET-###` defect checkbox is `- [x]` (fixed).

A plan that changes BOTH a web UI and its API runs both the rule-15 and the rule-16 rounds, and both
sets of defect checkboxes must be fixed before archival.

If defects surface after archival, use the reopen path (rule 14) — move the folder back from
`done/` to `in-progress/`, strip the completion-date prefix, and note the defect in `README.md`.

**Knowledge Capture pre-archival gate (mandatory, before any archival step)**: Archival MUST NOT
proceed until the plan's Knowledge Capture phase is complete.

- Every entry in `learnings.md` (or the explicit "none" escape) reaches a terminal state: routed
  inline, filed as a `plans/backlog/` follow-up, or discarded with a one-line reason — zero entries
  left in an open, undecided state.
- Both the secret/sensitivity gate and the repo-relevance gate have been applied to every
  surviving entry before it was routed.
- See the [Knowledge Capture Convention](../../development/quality/knowledge-capture.md) for the
  full triage rubric, the litmus test, and both safety gates — this gate references that
  convention rather than repeating its rubric.
- A plan with no Knowledge Capture phase and no explicit "none" record in `learnings.md` is
  incomplete for archival purposes.

**PR-Review Maker→Fixer Cycle gate (mandatory for `*-to-pr` modes, before archival and before the
merge)**: When the delivery mode resolved in Step 0 is `worktree-to-pr` or `main-to-pr`,
archival additionally requires the
[PR-Review Maker→Fixer Cycle](../pr/pr-review-quality-gate.md) workflow to run to completion
against the plan's PR before any archival step below. This gate does not apply to the direct-push
modes (`worktree-to-origin-main`, `main-to-origin-main`), which carry no PR and no review cycle.

- Run the workflow's strictly sequential N-cycle loop (default **N = 3**): each cycle, a fresh
  `pr-review-maker` posts line-anchored findings against the PR's current head commit via the
  GitHub Reviews API, a `pr-review-fixer` triages and resolves every unresolved thread, and CI on
  the PR must be GREEN before the next cycle starts. See the linked workflow for the full Loop
  Algorithm, posting mechanics, and escalation rules.
- **Done-definition for `*-to-pr` modes** (all four items required):
  1. **N review cycles complete** (default 3).
  2. **Every inline review comment is answered** — a fix applied and pushed, or a reasoned reject,
     on every thread.
  3. **All PR quality gates are GREEN** — both the local gates (Step 2b) and CI on the PR (Step 2c),
     as of the PR's current head commit.
  4. **Archival-in-PR is committed** — see below.
- **Archival-in-PR**: for `*-to-pr` modes, the `git mv plans/in-progress/... plans/done/...` move
  (and the accompanying README index updates) is committed **inside the delivering PR itself**, as a
  normal commit on the PR branch pushed before the merge — not as a separate commit landed
  on `main` after merge. This keeps the archival move inside the same review cycle as the rest of the
  plan's changes, so the merged PR already contains the finished, archived plan.
- The merge sits **outside** this AI done-boundary: once all four done-definition items
  are satisfied, the orchestrator holds a green, fully-reviewed, archival-included PR, and the merge
  follows — "done" is not the same as "merged" (see
  [Executor Tagging](../../conventions/structure/plans.md#executor-tagging--ai-vs-human-hard-rule)).
  **`[AI]` merges by default** once the hardened preconditions hold; a `[HUMAN]` merge gate applies
  only where a plan's own step says so explicitly, and the preconditions are identical either way —
  only the actor differs. See
  [Delivery Mode](../../conventions/structure/plans.md#delivery-mode).
  Worktree cleanup for `*-to-pr` modes happens **after** the merge completes (see the
  archival Logic below) — in contrast to the direct-push modes, where cleanup already correctly
  happens right after the push is confirmed green, because those modes have no separate merge step.

**Logic**:

- If status is `pass` (zero findings):

  **Infra-Execution Gate (precondition before archival)**: Before running `git mv`, check whether the plan's delivery checklist contains any infrastructure-apply step — `terraform apply`, `terraform destroy`, a live Ansible converge (`ansible-playbook` against real hosts), or any equivalent state-changing infra operation per the [Step 0 policy note](#0-enter-the-designated-worktree-sequential-hard-gate). If any such step is present but has NOT been verified-executed from the primary checkout (i.e., its checkbox remains unticked, or its implementation notes show it was deferred rather than genuinely run and confirmed), the workflow MUST NOT archive. Instead:
  1. Set status to `partial`.
  2. Leave the plan in `plans/in-progress/`.
  3. Retain the worktree.
  4. Surface to the user the exact infra step(s) that remain unexecuted, quoting the checkbox text and acceptance criterion verbatim.
  5. Stop. Do not proceed to any archival step.

  Zero validation findings alone is NOT sufficient for archival when an infra-apply step is still pending — the apply must be genuinely performed and its acceptance criterion verified (the provisioned resource exists and the target service responds), not merely reviewed or deferred. Only when all infra-apply steps in the delivery checklist are confirmed executed from the primary checkout may archival proceed.

  When the gate passes, proceed with archival. The remaining steps branch by the delivery mode
  resolved in Step 0.

  **`worktree-to-origin-main` / `main-to-origin-main` (direct-push modes)** — archival lands as a
  direct commit pushed to `origin main`, matching the default flow:
  1. Move entire plan folder from current location to `plans/done/`:

     ```bash
     git mv plans/in-progress/plan-name/ plans/done/YYYY-MM-DD__plan-name/
     ```

  2. **Update `plans/in-progress/README.md`** — remove the plan entry from the list
  3. **Update `plans/done/README.md`** — add the plan entry with completion date and brief summary:

     ```markdown
     - [Plan Name](./YYYY-MM-DD__plan-name/) — Brief description. Completed YYYY-MM-DD.
     ```

  4. **Update any other READMEs** that reference this plan (e.g., `plans/README.md`, project READMEs that link to the plan)
  5. **Search for orphaned references** to the old `plans/in-progress/[plan-name]` path and fix them
  6. **Commit the archival**:

     ```
     chore(plans): move [plan-identifier] to done
     ```

  7. **Worktree cleanup — prompted (after archival pushed)**: once the archival commit is pushed to `origin main` and CI is green, offer to delete the plan's worktree so worktrees do not accumulate:
     1. **Verify nothing unpushed** (safety precondition — both checks MUST pass before offering deletion):

        ```bash
        git -C worktrees/<plan-identifier> status --porcelain   # must be empty
        git fetch origin
        git merge-base --is-ancestor "$(git -C worktrees/<plan-identifier> rev-parse HEAD)" origin/main   # must succeed
        ```

        If either check fails, do NOT offer deletion — surface what is uncommitted or unpushed and keep the worktree.

     2. **Prompt the user** (interactive question — this is a sanctioned stop): `Plan complete and pushed to origin main. Delete worktree worktrees/<plan-identifier>/ and its local branch?` NEVER delete the worktree without explicit user confirmation.
     3. **On approval**, from the repo root:

        ```bash
        git worktree remove worktrees/<plan-identifier>
        git worktree prune
        git branch -d <plan-identifier> 2>/dev/null || true   # safe delete; only succeeds when fully merged
        ```

        If `git worktree remove` refuses (unexpected dirty state), do NOT force — re-run the safety precondition and escalate to the user.

     4. **On decline**: keep the worktree and emit one line: `Worktree retained at worktrees/<plan-identifier>/ per user choice.`

  **`worktree-to-pr` / `main-to-pr` (`*-to-pr` modes)** — archival-in-PR: the plan-folder move lands
  inside the delivering PR itself, gated by the PR-Review Maker→Fixer Cycle, before the merge
  (`[AI]` by default; `[HUMAN]` only where the plan's own step says so):
  1. Move entire plan folder from current location to `plans/done/` (same command as the direct-push
     path):

     ```bash
     git mv plans/in-progress/plan-name/ plans/done/YYYY-MM-DD__plan-name/
     ```

  2. **Update `plans/in-progress/README.md`** — remove the plan entry from the list
  3. **Update `plans/done/README.md`** — add the plan entry with completion date and brief summary
     (same format as above)
  4. **Update any other READMEs** that reference this plan
  5. **Search for orphaned references** to the old `plans/in-progress/[plan-name]` path and fix them
  6. **Commit the archival and push to the PR branch** (never to `main` directly):

     ```
     chore(plans): move [plan-identifier] to done
     ```

  7. **Run or complete the PR-Review Maker→Fixer Cycle** against the PR (see the gate above) — because
     each cycle's `pr-review-maker` reviews the full current state of the PR, its final pass also
     covers this archival commit. Confirm all four done-definition items are satisfied: N cycles
     complete, every comment answered, all gates GREEN (including CI on this last push), and the
     archival commit present on the PR branch.
  8. **Merge — `[AI]` by default**: once the done-definition is fully satisfied and the hardened
     merge preconditions (a)-(e) hold, surface the PR URL and the done-definition checklist, then
     merge. A `[HUMAN]` merge gate applies only where the plan's own step says so explicitly — in
     that case, hand off the ready-to-merge PR and STOP instead of merging. The preconditions are
     identical in both cases; only the actor differs. See
     [Delivery Mode](../../conventions/structure/plans.md#delivery-mode).
  9. **Worktree cleanup — prompted (after the merge completes)**: once the PR is confirmed
     merged, offer to delete the plan's worktree, using the same safety preconditions and
     prompt mechanics as the direct-push path, but gated on merge completion instead of push
     completion:
     1. **Verify nothing unpushed and the merge landed** (safety precondition):

        ```bash
        git -C worktrees/<plan-identifier> status --porcelain   # must be empty
        git fetch origin
        git merge-base --is-ancestor "$(git -C worktrees/<plan-identifier> rev-parse HEAD)" origin/main   # must succeed, post-merge
        ```

        If either check fails, do NOT offer deletion — surface what is uncommitted or unmerged and keep the worktree.

     2. **Prompt the user** (interactive question — this is a sanctioned stop): `PR merged. Delete worktree worktrees/<plan-identifier>/ and its local branch?` NEVER delete the worktree without explicit user confirmation, and never before the merge is confirmed.
     3. **On approval**, from the repo root:

        ```bash
        git worktree remove worktrees/<plan-identifier>
        git worktree prune
        git branch -d <plan-identifier> 2>/dev/null || true   # safe delete; only succeeds when fully merged
        ```

        If `git worktree remove` refuses (unexpected dirty state), do NOT force — re-run the safety precondition and escalate to the user.

     4. **On decline**: keep the worktree and emit one line: `Worktree retained at worktrees/<plan-identifier>/ per user choice.`

- If status is `partial` or `fail`: Leave plan in current location, do NOT archive, and do NOT delete the worktree — in-flight work stays available for the next execution attempt

**Output**: `{final-status}`, `{iterations-completed}`, `{final-report}`

**Status determination**:

- PASS: **Success** (`pass`): Zero findings after validation, all requirements met, AND all infrastructure-apply steps in the delivery checklist (`terraform apply`, live Ansible converge, or equivalent) are verified-executed from the primary checkout — plan moved to `plans/done/`
- **Partial** (`partial`): Findings remain after max-iterations, OR an infrastructure-apply step (`terraform apply`, live Ansible converge, or equivalent per the Step 0 policy) remains unexecuted from the primary checkout — plan stays in current location
- FAIL: **Failure** (`fail`): Technical errors during execution or checking, plan stays in current location

**Depends on**: Reaching this step from step 4, 6, or 7

## Task Management Rules

The orchestrator MUST follow these task management rules throughout execution:

### Create Tasks Before Starting

Before beginning Step 2 execution, create one task per delivery checklist item using
`TaskCreate`. Tasks must be granular — one concrete action per task. Never bundle multiple
steps behind a single task.

### Update Task Status Progressively

As each item begins, call `TaskUpdate` to set status `in_progress`. When done, call
`TaskUpdate` to set status `completed`. Never mark a task complete without having delegated
it and verified the agent completed the work.

### Tick Checkboxes Immediately

Update `delivery.md` immediately after each item completes — before moving to the next
item. Never batch-update checkboxes at the end of a phase. The delivery checklist must
reflect actual completion state at all times.

### Never Skip Items

Every delivery checklist item must be executed in order. The orchestrator may not skip an item
because it seems redundant or out of scope. If an item is genuinely irrelevant, mark it
with a note explaining why it was skipped rather than silently omitting it.

## Termination Criteria

- PASS: **Success** (`pass`): Zero findings of ANY criticality level (CRITICAL, HIGH, MEDIUM, LOW) in final validation, all deliverables complete, all infrastructure-apply steps verified-executed from the primary checkout, plan archived to `plans/done/`
- **Partial** (`partial`): Findings remain after max-iterations cycles, OR an infrastructure-apply step remains unexecuted from the primary checkout — plan requires manual intervention
- FAIL: **Failure** (`fail`): Orchestrator or checker encountered technical errors preventing completion

## Example Usage

### Execute Plan with Default Settings

```
User: "Execute plan plans/in-progress/new-feature/plan.md"
```

The calling context orchestrates directly and invokes specialized agents via the Agent tool (default max 10 iterations):

- Read delivery checklist and materialize 1:1 Task list in the calling context
- Delegate each item to the appropriate specialized agent (e.g., `swe-typescript-dev`)
- Tick checkboxes progressively as each item completes (Atomic Sync Ritual)
- Validate implementation by invoking `plan-execution-checker` delegated agent
- Iterate until zero findings and all deliverables complete
- Move plan folder to plans/done/ on success

### Execute with Extended Iterations

```
User: "Execute plan plans/in-progress/complex-migration/plan.md with max-iterations=15"
```

The AI will invoke agents with extended iteration limit:

- Allow up to 15 execute-validate cycles for complex plans
- Suitable for large migrations or multi-phase implementations

### Execute Plan from Backlog

```
User: "Execute plan plans/backlog/2025-02-01__future-feature/plan.md"
```

The AI will invoke agents regardless of folder location:

- Implement plan requirements via orchestrated specialized agents
- Won't move to done until zero findings achieved
- Plan archived to plans/done/ only on complete success

### Quick Validation Only

```
User: "Execute plan plans/in-progress/new-feature/plan.md with max-iterations=1"
```

The AI will invoke agents for a single cycle:

- Single execute-validate cycle
- Reports findings without further iteration
- Useful for quick validation pass

## Iteration Example

Typical execution flow:

```
Step 1: Load checklist — 12 items across 3 phases, 12 tasks created

Step 2: Execute all items sequentially
  Phase 1 (Infrastructure):
    Item 1 → swe-typescript-dev → checkbox ticked
    Item 2 → swe-typescript-dev → checkbox ticked
    Item 3 → docs-maker              → checkbox ticked
  Phase 2 (Implementation):
    Item 4 → swe-typescript-dev → checkbox ticked
    Item 5 → swe-e2e-dev   → checkbox ticked
    Item 6 → swe-golang-dev     → checkbox ticked
    ...and so on without stopping between phases

Step 3: Validate → 4 findings (quality issues, missing tests)

Step 5: Address findings
  Finding 1 → swe-typescript-dev → resolved
  Finding 2 → swe-e2e-dev   → resolved
  Finding 3 → docs-maker               → resolved
  Finding 4 → swe-typescript-dev → resolved

Step 6: Re-validate → 0 findings

Result: SUCCESS → Plan moved to plans/done/
```

## Safety Features

**Infinite Loop Prevention**:

- Max-iterations parameter (default: 10)
- Workflow terminates with `partial` if limit reached
- Tracks iteration count for monitoring

**Progressive Updates**:

- Delivery checklist items ticked individually throughout execution
- Task status updated in real time via TaskCreate/TaskUpdate
- Each iteration builds on previous work
- Validation history preserved in generated-reports/

**Error Recovery**:

- Continues to verification even if some execution steps encounter issues
- Reports which requirements succeeded/failed
- Generates final report regardless of status

**Plan Preservation**:

- Only moves plan to done/ on complete success (zero findings)
- Partial completion keeps plan in current location for manual review
- Uses git mv to preserve commit history when archiving

**Worktree Lifecycle**:

- Execution always enters the plan's designated worktree (Step 0) — navigating to it when it exists, provisioning it from the latest `origin/main` when it does not
- The worktree is synced with `origin/main` (ff-merge or rebase) before any implementation; dirty state or rebase conflicts stop execution for user decision
- On `pass`, after the archival commit is pushed, the orchestrator prompts the user before deleting the worktree (Step 8 cleanup) — worktrees never accumulate silently, and are never deleted without explicit confirmation
- On `partial` or `fail`, the worktree is always retained for the next execution attempt

## Plan-Specific Validation

The plan-execution-checker validates:

- **Requirements Coverage**: All requirements from plan implemented
- **Deliverables Completeness**: All deliverables created and meet quality standards
- **Checklist Completion**: All delivery checklist items marked as completed with implementation notes
- **Quality Standards**: Implementation follows repository conventions and best practices
- **Testing Requirements**: Tests written and passing as specified in plan
- **Documentation**: Required documentation created and accurate
- **Operational Readiness** (CRITICAL): The checker verifies ALL of the following were executed:
  - **Local quality gates passed**: `nx affected -t typecheck lint test:quick specs:coverage` was run and passed with zero failures before every push
  - **CI/CD fully green**: All GitHub Actions workflows passed after every push — no exceptions
  - **Preexisting issues fixed**: All encountered failures were fixed, including those not caused by the plan's changes (root cause orientation)
  - **Delivery.md updated progressively**: Checkboxes ticked sequentially with implementation notes, not batch-ticked at the end (verified via git history)
  - **Thematic commits**: Changes committed in logically cohesive groups following Conventional Commits, not monolithic dumps
  - **Environment setup performed**: Evidence that dev environment was set up before implementation began
  - **Manual behavioral assertions**: Playwright MCP was used to verify web UI changes (navigation, DOM, console errors, screenshots); curl was used to verify API changes (status codes, response shapes, error cases). Documented in delivery.md.

## Related Workflows

This workflow can be composed with:

- **plan-quality-gate**: Validate plan quality before executing (recommended pre-step)
- **[plan-multi-repo-parity-planning-and-execution](./plan-multi-repo-parity-planning-and-execution.md)**: composite that nests this workflow per repo after a multi-repo parity planning phase
- Content creation workflows: Execute content-focused plans
- Release workflows: Execute release plans with deployment
- **repo-rules-quality-gate**: Validate repository consistency after plan execution

**Recommended Workflow Sequence**:

```
1. plan-quality-gate → Validate plan completeness and accuracy
2. plan-execution    → Execute validated plan
3. repo-rules-quality-gate → Ensure repository consistency
```

## Success Metrics

Track across executions:

- **Average iterations to completion**: How many cycles typically needed for different plan types
- **Success rate**: Percentage of plans reaching zero findings and moving to done/
- **Common finding categories**: What issues appear most often during execution
- **Execution success rate**: Percentage of requirements implemented without errors
- **Archival rate**: Percentage of plans successfully moved to done/
- **Agent delegation accuracy**: How often the correct specialized agent was selected per task type

## Notes

- **Orchestrator model**: calling context (top-level assistant session) coordinates specialized agents per the rules in this workflow, never implementing substantive changes directly
- **Semi-automated**: calling context may request user input for critical decisions, but execution continues autonomously otherwise
- **Idempotent**: Safe to re-run on partially completed plans, won't duplicate work
- **Progressive**: Each iteration builds on previous work, continuously updating checklists and task status
- **Observable**: Generates validation reports for every validation cycle; task status visible in real time
- **Bounded**: Max-iterations prevents runaway execution
- **Archival**: Automatically moves successfully completed plans to done/ folder
- **History-preserving**: Uses git mv to maintain commit history when archiving

**Key Differences from plan-quality-gate**:

1. **Execution-focused**: Orchestrated directly by the calling context (which delegates per-item work to specialized agents) instead of by `plan-fixer` (which edits plan documents)
2. **End-to-end**: Covers full plan lifecycle from execution through validation to archival
3. **Progressive delivery**: Continuously ticks delivery checklist items and updates task status throughout execution
4. **Archival automation**: Moves completed plans to plans/done/ automatically
5. **Higher default iterations**: Default 10 (vs 5) since implementation is more complex than document fixes
6. **Delegation model**: Routes each item to the domain-appropriate specialized agent

This workflow ensures complete plan execution with validated quality, making it ideal for systematically implementing project plans from start to archive.

## Test-Driven Development

When implementing delivery checklist items that ship code, the orchestrator and all delegated
`swe-*-dev` agents follow TDD: write a failing test first, confirm it fails for the right reason,
write the minimum code to pass, then refactor. Mini-TDD passes are encouraged — split a feature
into multiple small Red→Green→Refactor cycles rather than one large test up front. Gherkin
acceptance criteria in `prd.md` are the natural source of the first failing tests.

**See**: [Test-Driven Development Convention](../../development/workflow/test-driven-development.md) — in particular, the
[TDD Shape for Delivery Checklists](../../development/workflow/test-driven-development.md#tdd-shape-for-delivery-checklists)
section for the required RED/GREEN/REFACTOR three-substep template (explicit file path, verbatim command, acceptance criterion per substep).

## Principles Implemented/Respected

- PASS: **Explicit Over Implicit**: All steps, conditions, termination criteria, and agent selection rules clearly defined
- PASS: **Automation Over Manual**: Fully automated execution, validation, and archival with specialized agent delegation
- PASS: **Simplicity Over Complexity**: Clear linear flow with loop control, bounded iterations, and domain-specific agents
- PASS: **Accessibility First**: Generates human-readable validation reports for transparency
- PASS: **Progressive Disclosure**: Configurable iterations and plan paths for different use cases
- PASS: **No Time Estimates**: Focus on quality outcomes and completion criteria, not duration

## Conventions Implemented/Respected

- **[File Naming Convention](../../conventions/structure/file-naming.md)**: Workflow file follows plain name convention for workflows
- **[Linking Convention](../../conventions/formatting/linking.md)**: All cross-references use GitHub-compatible markdown with `.md` extensions
- **[Content Quality Principles](../../conventions/writing/quality.md)**: Active voice, proper heading hierarchy, single H1
- **[Grilling-With-Options Convention](../../development/workflow/grilling-with-options.md)**:
  Pre-execution grill MUST present 2-4 concrete options per question; open-ended questions
  without options are FORBIDDEN

## Agents

- [plan-execution-checker](../../../.claude/agents/plan-execution-checker.md) — validates plan execution completeness and quality
