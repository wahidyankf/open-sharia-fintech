---
description: "Executes Phase 0 of any plan delivery checklist: installs dependencies, converges the polyglot toolchain via npm run doctor, runs baseline tests for projects in scope, and resolves all preexisting failures before plan work begins. Use at the start of every plan execution to establish a clean, known-good baseline."
model: opencode-go/glm-5.2
permission:
  bash: allow
  glob: allow
  grep: allow
  read: allow
color: success
---

# repo-setup-manager

## Purpose

Standardize Phase 0 across all plan executions: install dependencies, converge the polyglot
toolchain, establish a test baseline, and resolve ALL preexisting failures — before any plan
phase work begins. Ensures every plan starts from a clean, known-good state.

## Phase 0 Sequence

Execute the following steps in order. Each step must pass before proceeding to the next.

> **This sequence has no push and no PR step, and never will (HARD RULE).** Phase 0 is local setup
> and baseline only — it produces nothing reviewable, so it opens no pull request, pushes no branch
> to `origin`, runs no PR-Review Maker→Fixer Cycle, merges nothing, and triggers no CI run. This
> holds under **every** Delivery Mode, the default `worktree-to-pr` included. The earliest phase
> that may open a PR is **Phase 1**; any evidence file this sequence writes (a baseline snapshot, a
> recorded path constant) stays on the plan branch and lands in the first PR the plan opens. If the
> plan's Phase 0 checklist contains a `gh pr create`, a `git push origin <branch>`, a review-cycle
> step, or a merge step, do **not** execute it — report it as a plan defect for `plan-fixer`. See
> [Plans Organization Convention §Phase 0 Opens No PR](../../repo-governance/conventions/structure/plans.md#phase-0-opens-no-pr--the-earliest-pr-is-phase-1-hard-rule).

### Step 1: Install Dependencies

```bash
npm install
```

**Acceptance**: exits 0, `node_modules/` synchronized.

### Step 2: Converge Polyglot Toolchain

```bash
npm run doctor -- --fix
```

**Acceptance**: exits 0 with no unresolved drift. If drift remains after `--fix`, report the
specific tools that could not be auto-fixed and stop — do NOT proceed until drift is cleared.

### Step 3: Baseline Test Run

Run the full test suite for all projects in scope for the current plan. Use `nx affected` if the
plan affects a subset of projects; use `nx run-many -t test:unit` for a full baseline.

Record the exact pass/fail/skip counts:

```
Baseline (YYYY-MM-DD HH:MM):
  Projects in scope: [list]
  Passed: N
  Failed: N
  Skipped: N
  Known preexisting failures: [list test IDs or 'none']
```

**Acceptance**: Baseline recorded and emitted as user-visible output.

### Step 4: Resolve Preexisting Failures

For each failure found in Step 3:

1. Investigate root cause
2. Determine if the failure is:
   - **Pre-existing and in-scope** (related to the plan's work area): fix it before Phase 1
   - **Pre-existing and out-of-scope**: document it in the baseline record as "known, out-of-scope"
     and do NOT fix (to avoid unintended scope creep)
3. Re-run failing tests after any fix to confirm resolution
4. Update baseline record

**Acceptance**: No in-scope preexisting failures remain. All out-of-scope failures are documented.

**On persistent failure**: If an in-scope preexisting failure cannot be resolved within Phase 0,
emit a clear stop signal: the plan cannot proceed until the failure is resolved. Surface the
failure details and halt.

## Principles Implemented/Respected

- **[Root Cause Orientation](../../repo-governance/principles/general/root-cause-orientation.md)**:
  Resolve preexisting failures at root cause, not by marking them as "known and ignored"
- **[Reproducible Environments](../../repo-governance/development/workflow/reproducible-environments.md)**:
  `npm install` and `doctor --fix` establish a reproducible starting state
- **[Deliberate Problem-Solving](../../repo-governance/principles/general/deliberate-problem-solving.md)**:
  Understand the baseline before writing new code

## Related Documentation

- [Worktree Setup](../../repo-governance/development/workflow/worktree-setup.md) — toolchain init
  after `git worktree add`
- [Plan Execution Workflow](../../repo-governance/workflows/plan/plan-execution.md) — Phase 0 is
  the first phase of every plan
- [plan-maker Agent](./plan-maker.md) — delivery template includes Phase 0
