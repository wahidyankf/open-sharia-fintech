---
title: "PR Merge Protocol"
description: Practice requiring explicit user approval before merging pull requests and mandating all quality gates pass before merge
category: explanation
subcategory: development
tags:
  - pull-request
  - merge
  - quality-gates
  - workflow
  - human-approval
created: 2026-04-04
---

# PR Merge Protocol

Merging a pull request requires explicit approval from the user every single time. No AI agent, automation script, or workflow may auto-merge a pull request. All quality gates must pass before merge, and bypassing them without explicit user permission is forbidden.

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: Merging a PR is an irreversible integration action that changes the state of the trunk for every contributor. It demands human judgment about timing, completeness, and readiness -- the kind of decision that must not be delegated to autonomous agents.

- **[Root Cause Orientation](../../principles/general/root-cause-orientation.md)**: When quality gates fail, the correct response is to investigate and fix the root cause, not to bypass the gate and merge anyway. This convention ensures that failing gates are treated as problems to solve, not obstacles to circumvent.

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: Merge approval must be an explicit, visible action from the user. Implicit approval -- "the user asked me to create a PR, so merging is also implied" -- is the silent assumption this convention forbids.

- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)**: Quality gates (typecheck, lint, test:quick, specs:coverage, CI workflows) run automatically. The automation validates; the human decides. This division is deliberate: machines check, humans approve.

## Conventions Implemented/Respected

This practice implements/respects the following conventions:

- **[Code Quality Convention](../quality/code.md)**: The quality gates enforced by this protocol (typecheck, lint, test:quick, specs:coverage) are the same gates enforced by the pre-push hook. This convention extends the same standard to the PR merge boundary.

- **[Trunk Based Development Convention](./trunk-based-development.md)**: `worktree-to-pr` -- a short-lived plan branch pushed to a PR -- is the repo-wide default TBD flavor. PRs also exist for `main-to-pr`, code review, and external contributions. This protocol governs the merge step for all of them.

- **[Git Push Safety Convention](./git-push-safety.md)**: Both conventions share the principle that destructive or irreversible git operations require explicit, per-instance user approval. This convention applies the same standard to PR merges.

## The Rule

**AI agents and automation MUST NOT merge a pull request without explicit user approval.**

For every PR merge -- without exception -- the agent must:

1. Confirm all quality gates have passed (see Quality Gates below).
2. Present the PR status to the user, including which gates passed and any open review comments.
3. Wait for the user to provide explicit confirmation to merge.
4. Execute the merge only after that confirmation is received.

**Prior approval does not carry forward.** If the user approved merging one PR, that approval covers only that one merge. The next PR merge starts from zero.

## Quality Gates

All of the following quality gates must pass before a PR is eligible for merge:

| Gate               | Tool           | What It Validates                                  |
| ------------------ | -------------- | -------------------------------------------------- |
| **typecheck**      | Nx affected    | Type correctness across affected projects          |
| **lint**           | Nx affected    | Static analysis, formatting, accessibility         |
| **test:quick**     | Nx affected    | Unit tests, build smoke tests, coverage thresholds |
| **specs:coverage** | Nx affected    | Gherkin step definitions match feature files       |
| **CI workflows**   | GitHub Actions | All configured CI checks for the repository        |

### No Bypass Without Explicit Permission

Bypassing any quality gate without explicit user permission is **forbidden**. This includes:

- Merging with failing CI checks
- Merging with unresolved review comments (unless the user explicitly dismisses them)
- Using admin override to bypass branch protection rules
- Merging with pending required status checks

If the user explicitly says "merge despite the failing lint check" (or equivalent), the agent may proceed -- but only for that specific instance and only for the specific gates the user named.

## When This Applies

This protocol applies whenever a pull request exists as part of the development workflow:

- **`worktree-to-pr` (repo-wide default)**: every plan delivered without an explicit mode override
  resolves to this mode -- a short-lived plan branch, a draft PR opened against `main`, and this
  protocol at merge time. See [the `worktree-to-pr` terminal step](#the-worktree-to-pr-terminal-step)
  below for the full terminal-step sequence.
- **`main-to-pr`**: primary-checkout work still routed through a PR follows the same protocol.
- **External contributions**: PRs from external contributors follow this protocol.
- **Code review workflow**: Any short-lived branch created for review purposes follows this protocol.

This protocol does **not** apply to:

- Direct commits under `worktree-to-origin-main` or `main-to-origin-main` (no PR exists to merge).
- Environment branch deployments managed by CI (e.g., `prod-ayokoding-www`), which are governed by their own documented CI workflows.

## The `worktree-to-pr` Terminal Step

Under the repo-wide `worktree-to-pr` default (see the
[Plans Organization Convention — Delivery Mode](../../conventions/structure/plans.md#delivery-mode) and
the [Trunk Based Development Convention](./trunk-based-development.md#default-delivery-mode-worktree-to-pr)),
the AI's work on a plan branch does not end at "all commits pushed." The terminal step, run by `[AI]`,
is:

1. Run the **PR-Review Maker→Fixer Cycle**
   (`repo-governance/workflows/pr/pr-review-quality-gate.md`) -- sequential review/fix cycles
   against the open PR, driving it toward a fully reviewed, green state.
2. Confirm the **done-definition** is met:
   - The review cycle has completed its configured number of passes.
   - Every inline review comment has a reply (resolved or explicitly addressed).
   - All quality gates are GREEN -- both local (pre-push hook) and CI.
   - Archival-in-PR is committed (ose-public only -- the plan folder's archival move lands in the same
     PR, since the plan folder lives solely in this repo).
3. Flip the PR from draft to ready for review (`gh pr ready`).

**This done-definition is the AI's done-boundary.** Meeting it means the AI's work on the plan is
complete -- it does **not** mean the plan is merged. The actual merge is a separate, subsequent action
performed by `[HUMAN]`, per the approval rule in [The Rule](#the-rule) above. "Done" (for the AI) is
not "merged" -- the merge sits outside the AI's done-boundary entirely, on the human's own schedule.

### Draft PR Lifecycle

Per the [Trunk Based Development Convention](./trunk-based-development.md#why-draft-not-ready-for-review-on-open),
every PR opened under `worktree-to-pr` or `main-to-pr` is **opened as a GitHub draft**
(`gh pr create --draft`), not as a ready-for-review PR. This protocol's approval gate fires at the
moment the AI flips the draft to ready for review (having met the done-definition above), not at PR
open time.

**Lifecycle**:

1. **Draft opened** -- `[AI]` runs `gh pr create --draft --base main ...`. No approval gate yet. CI may still run on the draft.
2. **Iterate on the branch** -- `[AI]` pushes additional commits and runs the PR-Review Maker→Fixer Cycle. The PR stays in draft status throughout iteration. No approval gate yet.
3. **`[AI]` flips to ready** -- once the done-definition is met, `[AI]` runs `gh pr ready` (or marks it ready in the GitHub UI). **This is where the PR Merge Protocol approval gate fires.** The agent must:
   - Verify all quality gates have passed (see Quality Gates above).
   - Present the approval prompt to the user.
   - Wait for explicit confirmation before merging.
4. **`[HUMAN]` merges** -- only after explicit user approval, per the rules above. This step is outside the AI's done-boundary.

An agent that opens a draft PR is **not** authorized to merge it without explicit user instruction --
flipping to ready is the deliberate signal that the AI's own work is done; the merge itself remains a
separate, human-owned action.

## Agent Workflow

### Before Proposing Merge

Before asking the user to approve a merge, the agent must:

1. Verify all CI checks have completed (not still running).
2. Check for unresolved review comments or requested changes.
3. Confirm the branch is up to date with the target branch (no merge conflicts).

### The Approval Prompt

When all gates pass, the agent presents a clear summary:

```
PR #42: feat(auth): add email validation

Quality gates:
  typecheck:     PASSED
  lint:          PASSED
  test:quick:    PASSED
  specs:coverage: PASSED
  CI workflows:  PASSED

No unresolved review comments.
Branch is up to date with main.

Do you want me to merge this PR? (yes/no)
```

### When Gates Fail

If any quality gate fails, the agent must:

1. Report which gate failed and the error details.
2. Investigate the root cause.
3. Fix the issue (not bypass the gate).
4. Re-run the gates.
5. Only then ask for merge approval.

```
PR #42: feat(auth): add email validation

Quality gates:
  typecheck:     PASSED
  lint:          FAILED (3 errors in auth-validator.ts)
  test:quick:    PASSED
  specs:coverage: PASSED

I will investigate and fix the lint errors before asking to merge.
```

## Examples

### PASS: Correct agent behavior

```
Agent: All quality gates have passed for PR #42. Here is the summary:

  typecheck:     PASSED
  lint:          PASSED
  test:quick:    PASSED
  specs:coverage: PASSED
  CI workflows:  PASSED

Do you want me to merge this PR?

User: Yes, merge it.

Agent: Merging PR #42...
```

### FAIL: Incorrect agent behavior -- auto-merging

```
Agent: I created PR #42 and all checks passed. Merging now.
[merges without asking]
```

### FAIL: Incorrect agent behavior -- merging with failing gates

```
Agent: PR #42 has a failing lint check, but the rest passed.
       Merging anyway to save time.
[merges despite failing gate]
```

### FAIL: Incorrect agent behavior -- reusing prior approval

```
User: [earlier] Yes, merge PR #42.
Agent: [later, different PR] Reusing your earlier approval to merge PR #43.
```

### PASS: User explicitly bypasses a gate

```
Agent: PR #42 has all gates passing except specs:coverage, which
       failed because the new endpoint's Gherkin scenario is still
       being drafted in a follow-up task.

User: Merge it anyway, I will add the Gherkin scenario in the next commit.

Agent: Understood. Merging PR #42 with your explicit approval to
       bypass the specs:coverage gate for this instance.
```

## Scope

This rule applies to:

- All AI agents defined in `.claude/agents/` and `.opencode/agents/`.
- All automation scripts, npm scripts, and CI workflows that could trigger a PR merge.
- All pull requests targeting any branch in the repository.

## Related Documentation

- [Git Push Safety Convention](./git-push-safety.md) -- Per-instance approval for destructive git operations
- [Code Quality Convention](../quality/code.md) -- Quality gates enforced by git hooks
- [Trunk Based Development Convention](./trunk-based-development.md) -- The `worktree-to-pr` default delivery mode and how it relates to TBD
- [Worktree Toolchain Initialization](./worktree-setup.md) -- Mandatory two-step init (`npm install` + `npm run doctor -- --fix`) after creating or entering a worktree
- [Nx Target Standards](../infra/nx-targets.md) -- Canonical target names for quality gates
- [Git Push Default Convention](./git-push-default.md) -- Governs the default `worktree-to-pr` push target and the explicit direct-push modes; this convention governs what happens once a PR exists
- [Plans Organization Convention — Delivery Mode](../../conventions/structure/plans.md#delivery-mode) -- The four-mode vocabulary and three-tier precedence that determines when this protocol applies
- `repo-governance/workflows/pr/pr-review-quality-gate.md` -- The review/fix cycle that runs before a `worktree-to-pr` PR meets the done-definition described above
