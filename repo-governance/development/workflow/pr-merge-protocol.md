---
title: "PR Merge Protocol"
description: Practice governing pull-request merges — merge authority is granted by hardened preconditions rather than a per-instance prompt, `[AI]` merges by default, and all quality gates must pass before merge
category: explanation
subcategory: development
tags:
  - pull-request
  - merge
  - quality-gates
  - workflow
  - merge-preconditions
created: 2026-04-04
---

# PR Merge Protocol

Merging a pull request requires a set of hardened preconditions to hold — not a per-instance prompt. Once they hold, `[AI]` merges by default; a `[HUMAN]` merge gate applies only where a plan's own step says so explicitly. All quality gates must pass before merge, and bypassing them without explicit user permission is forbidden.

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: Merging a PR is an irreversible integration action that changes the state of the trunk for every contributor. It demands a deliberate readiness judgment -- which this protocol makes explicit and checkable as preconditions, rather than leaving it to an agent's discretion in the moment.

- **[Root Cause Orientation](../../principles/general/root-cause-orientation.md)**: When quality gates fail, the correct response is to investigate and fix the root cause, not to bypass the gate and merge anyway. This convention ensures that failing gates are treated as problems to solve, not obstacles to circumvent.

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: Merge authority must rest on explicit, checkable state. "The review cycles felt thorough enough" -- an agent's implicit readiness judgment substituting for the stated preconditions -- is the silent assumption this convention forbids. The merge actor is likewise explicit: `[AI]` by default, `[HUMAN]` only where a plan says so.

- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)**: Quality gates (typecheck, lint, test:quick, specs:coverage, CI workflows) run automatically, and the merge decision is derived from their outcome rather than re-litigated by hand each time. Encoding readiness as preconditions is what makes automating the merge safe.

## Conventions Implemented/Respected

This practice implements/respects the following conventions:

- **[Code Quality Convention](../quality/code.md)**: The quality gates enforced by this protocol (typecheck, lint, test:quick, specs:coverage) are the same gates enforced by the pre-push hook. This convention extends the same standard to the PR merge boundary.

- **[Trunk Based Development Convention](./trunk-based-development.md)**: `worktree-to-pr` -- a short-lived plan branch pushed to a PR -- is the repo-wide default TBD flavor. PRs also exist for `main-to-pr`, code review, and external contributions. This protocol governs the merge step for all of them.

- **[Git Push Safety Convention](./git-push-safety.md)**: Both conventions treat irreversible git operations as gated rather than routine. They differ in the gate: `git push --force` and friends require explicit, per-instance user approval because no automated check can establish their safety, whereas a PR merge's safety **is** mechanically checkable -- so this convention gates on preconditions instead of a prompt.

## The Rule

**AI agents and automation MUST NOT merge a pull request until the hardened preconditions hold.**

A PR merges only when **all five** hold:

- **(a)** the PR's behavior route is complete — an eligible PR reached the first completed specialist
  cycle with zero code-related MEDIUM/HIGH/CRITICAL findings within the default maximum of seven,
  while a noneligible PR has recorded classifier evidence and a green
  `.github/workflows/pr-quality-gate.yml` run. A `blocked` route status prevents merge;
- **(b)** 0 code-related CRITICAL, HIGH, and MEDIUM findings are outstanding;
- **(c)** the branch is up-to-date with the latest `origin/main`, brought forward
  **non-destructively** if behind (never a shared-history rewrite);
- **(d)** the route-required quality gate is green: all applicable local and CI gates for an eligible
  PR; `.github/workflows/pr-quality-gate.yml` for a noneligible PR;
- **(e)** the surface-conditional tester gates have been run and their defect findings resolved for
  an eligible PR. A noneligible PR has no reachable behavior and does not run those tester gates.

For every PR merge -- without exception -- the agent must:

1. Confirm all five preconditions hold.
2. Surface the PR status, including which gates passed and how each precondition was satisfied.
3. Execute the merge -- `[AI]` is the default actor.

`[AI]` is the merge actor once the preconditions hold, unless a separate, explicitly authorized
exception says otherwise. This convergence plan has no human review or merge gate.

**Preconditions are evaluated per merge.** Satisfying them for one PR says nothing about the next;
each PR is assessed from zero against the full set.

## Quality Gates

An **eligible** PR must pass the applicable local and CI gates below. A **noneligible** PR requires
only a successful `.github/workflows/pr-quality-gate.yml` run for its current head; it does not run
the specialist cycle or surface tester gates. Both routes still require the shared preconditions,
including the universal secret check.

| Gate               | Tool           | What It Validates                                  |
| ------------------ | -------------- | -------------------------------------------------- |
| **typecheck**      | Nx affected    | Type correctness across affected projects          |
| **lint**           | Nx affected    | Static analysis, formatting, accessibility         |
| **test:quick**     | Nx affected    | Unit tests, build smoke tests, coverage thresholds |
| **specs:coverage** | Nx affected    | Gherkin step definitions match feature files       |
| **CI workflows**   | GitHub Actions | All configured CI checks for the repository        |

### Universal Secret Check

Before merging either route, inspect the PR diff and review evidence for a suspected secret exposure.
If one exists, stop normal merge handling, contain and rotate the credential, then follow the full
reachable-ref history-rewrite and replacement-PR procedure in
[Secrets and Environment Standards](../../conventions/security/secrets-and-env-standards.md). A
green quality gate, a noneligible classifier result, or a resolved review thread never authorizes
merging a contaminated PR.

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
- **A plan's Phase 0** (Environment Setup and Baseline) under any delivery mode -- it opens no PR, so there is nothing here to merge. The earliest phase that may open a PR, and therefore the earliest phase this protocol can govern, is **Phase 1**. See [Plans Organization Convention §Phase 0 Opens No PR](../../conventions/structure/plans/23-phase-0-opens-no-pr.md#phase-0-opens-no-pr--the-earliest-pr-is-phase-1-hard-rule).
- **A plan's intermediate phases** — those inside a delivery unit but not its **delivery boundary**. They open no PR, so this protocol has nothing to govern until the unit's boundary phase opens one. See [Plans Organization Convention §PRs Open at Delivery Boundaries](../../conventions/structure/plans/25-prs-open-at-delivery-boundaries-rules.md#prs-open-at-delivery-boundaries-not-every-phase-hard-rule).
- Environment branch deployments managed by CI (e.g., `prod-ayokoding-www`), which are governed by their own documented CI workflows.

## The `worktree-to-pr` Terminal Step

Under the repo-wide `worktree-to-pr` default (see the
[Plans Organization Convention — Delivery Mode](../../conventions/structure/plans/32-delivery-mode-the-four-modes.md#delivery-mode) and
the [Trunk Based Development Convention](./trunk-based-development.md#default-delivery-mode-worktree-to-pr)),
the AI's work on a plan branch does not end at "all commits pushed." The terminal step, run by `[AI]`,
is:

1. Run the **PR-Review Maker→Fixer Cycle**
   (`repo-governance/workflows/pr/pr-review-quality-gate.md`) -- first classify the open PR. Run
   sequential specialist review/fix cycles only for the eligible route; a noneligible route verifies
   the named `pr-quality-gate.yml` workflow instead.
2. Confirm the **done-definition** is met:
   - The eligible route stopped at its first clean cycle within the seven-cycle maximum, or the
     noneligible route has recorded classifier evidence and its `pr-quality-gate.yml` run is green.
   - Every inline review comment has a reply (resolved or explicitly addressed).
   - All quality gates are GREEN -- both local (pre-push hook) and CI.
   - Archival-in-PR is committed (ose-public only -- the plan folder's archival move lands in the same
     PR, since the plan folder lives solely in this repo).
3. Flip the PR from draft to ready for review (`gh pr ready`).

**This done-definition is the AI's done-boundary.** Meeting it means the AI's work on the plan is
complete -- it does **not** by itself mean the plan is merged. The merge is a separate, subsequent
action gated on the five preconditions in [The Rule](#the-rule) above and performed by `[AI]`.
"Done" is not "merged" -- the merge sits outside the done-boundary entirely.

### Draft PR Lifecycle

Per the [Trunk Based Development Convention](./trunk-based-development.md#why-draft-not-ready-for-review-on-open),
every PR opened under `worktree-to-pr` or `main-to-pr` is **opened as a GitHub draft**
(`gh pr create --draft`), not as a ready-for-review PR. This protocol's precondition gate fires at the
moment the AI flips the draft to ready for review (having met the done-definition above), not at PR
open time.

**Lifecycle**:

1. **Draft opened** -- `[AI]` runs `gh pr create --draft --base main ...`. No precondition gate yet. CI may still run on the draft.
2. **Iterate on the branch** -- `[AI]` pushes additional commits and runs the PR-Review Maker→Fixer Cycle. The PR stays in draft status throughout iteration. No precondition gate yet.
3. **`[AI]` flips to ready** -- once the done-definition is met, `[AI]` runs `gh pr ready` (or marks it ready in the GitHub UI). **This is where the PR Merge Protocol precondition gate fires.** The agent must:
   - Verify all quality gates have passed (see Quality Gates above).
   - Verify all five preconditions in [The Rule](#the-rule) hold.
   - Surface the PR status and how each precondition was satisfied.
4. **The merge** -- `[AI]`, once the preconditions hold. This step is outside the AI's done-boundary.

An agent that opens a draft PR is **not** authorized to merge it on readiness alone --
flipping to ready is the deliberate signal that the AI's own work is done, and the merge follows only
from the preconditions, never from the agent's own judgment that the PR looks finished.

## Agent Workflow

### Before Merging

Before merging, the agent must confirm **all five** hardened preconditions (a)-(e) hold, as stated in
[The Rule](#the-rule) above and defined normatively in
[the PR Review Quality Gate](../../workflows/pr/pr-review-quality-gate.md#hardened-merge-preconditions).
Do not substitute the shorter list that used to live here.

1. **(a)** The route is complete: eligible review stopped at its earliest clean cycle within seven;
   noneligible review has classification evidence plus a green `pr-quality-gate.yml` run. `blocked`
   never merges.
2. **(b)** 0 code-related CRITICAL, HIGH, and MEDIUM findings outstanding, verified against the PR's
   own diff rather than against thread-resolution state.
3. **(c)** The branch is non-destructively up to date with the target branch (no merge conflicts).
4. **(d)** The route-required quality gate is green as of the PR's current head: all applicable
   gates for eligible work, or the named `pr-quality-gate.yml` workflow for noneligible work.
5. **(e)** Eligible surface tester gates have run and their findings are resolved. A noneligible
   route is explicitly exempt because its classifier evidence shows no reachable behavior.

> **Why this list is spelled out in full.** It previously carried only three items — CI completed,
> review comments checked, branch up to date — because it ran immediately before a **human approval
> prompt**, and the human was the backstop for whatever the list omitted. Now that `[AI]` merges by
> default, that backstop is gone and this is the last checklist an autonomous merge passes through.
> An enumeration that was merely incomplete has become the thing standing in for a reviewer. Any
> future edit must keep it congruent with (a)-(e); never shorten it.

### Resolving Merge Conflicts in Generated Files

Precondition (c) requires resolving any conflict against the target branch before merging. A
`CONFLICTING` state after an otherwise-clean review cycle does not mean the PR's own work is
wrong — it can be pure divergence from unrelated concurrent activity on the target branch,
resolvable by a normal rebase or merge.

When the conflicting hunk falls inside a **marker-owned or generated file** (a block regenerated
by a registry/codegen command — e.g. `package.json`'s `lint-staged` block emitted from
`repo-config.yml` via `gate emit`, or any other file a `validate`/`sync` command checks for drift),
resolve the conflict at the **source** the generator reads from, then regenerate — never hand-resolve
directly in the generated artifact. A hand-resolution can satisfy `git` while still drifting from
what the generator would actually produce, and the repo's own drift-detection command (`gate validate`
or the equivalent) exists specifically to catch that class of silent divergence. Re-run the generator,
confirm the regenerated file is byte-identical to the hand-resolution (or replaces it), then re-run
the drift check before proceeding.

### The Precondition Summary

When all preconditions hold, the agent presents a clear summary, then merges:

```
PR #42: feat(auth): add email validation

Quality gates:
  typecheck:     PASSED
  lint:          PASSED
  test:quick:    PASSED
  specs:coverage: PASSED
  CI workflows:  PASSED

Preconditions:
  (a) review route:      eligible, clean at cycle 2 of 7
  (b) C/H/M:             0 / 0 / 0 outstanding
  (c) branch vs main:    up to date (fast-forwarded, no rewrite)
  (d) quality gates:     all green (above)
  (e) tester gates:      run, findings resolved

Merging PR #42.
```

### When Gates Fail

If any quality gate fails, the agent must:

1. Report which gate failed and the error details.
2. Investigate the root cause.
3. Fix the issue (not bypass the gate).
4. Re-run the gates.
5. Only then re-evaluate the merge preconditions.

```
PR #42: feat(auth): add email validation

Quality gates:
  typecheck:     PASSED
  lint:          FAILED (3 errors in auth-validator.ts)
  test:quick:    PASSED
  specs:coverage: PASSED

I will investigate and fix the lint errors before merging.
```

## Examples

### PASS: Correct agent behavior -- preconditions hold, `[AI]` merges

```
Agent: All five merge preconditions hold for PR #42:

  (a) review route:   eligible, clean at cycle 2 of 7
  (b) C/H/M:          0 / 0 / 0 outstanding
  (c) branch vs main: up to date
  (d) quality gates:  all green
  (e) tester gates:   run, findings resolved

Merging PR #42.
```

### FAIL: Incorrect agent behavior -- merging before the preconditions hold

```
Agent: I created PR #42 and CI is green. Merging now.
[merges before the eligible route reaches a clean cycle -- precondition (a) unmet]
```

### FAIL: Incorrect agent behavior -- merging with failing gates

```
Agent: PR #42 has a failing lint check, but the rest passed.
       Merging anyway to save time.
[merges despite failing gate -- precondition (d) unmet]
```

### FAIL: Incorrect agent behavior -- carrying a bypass forward

```
User: [earlier] Merge PR #42 anyway despite specs:coverage.
Agent: [later, different PR] Reusing that bypass to merge PR #43.
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

- [Git Push Safety Convention](./git-push-safety.md) -- Per-instance approval for destructive git operations; gated by a prompt because their safety is not mechanically checkable, unlike a PR merge's
- [Plans Organization Convention §Delivery Mode](../../conventions/structure/plans/32-delivery-mode-the-four-modes.md#delivery-mode) -- Establishes `[AI]` merge as the default and `[HUMAN]` as the explicit per-plan opt-in this protocol implements
- [Code Quality Convention](../quality/code.md) -- Quality gates enforced by git hooks
- [Trunk Based Development Convention](./trunk-based-development.md) -- The `worktree-to-pr` default delivery mode and how it relates to TBD
- [Worktree Toolchain Initialization](./worktree-setup.md) -- Mandatory two-step init (`npm install` + `npm run doctor -- --fix`) after creating or entering a worktree
- [Nx Target Standards](../infra/nx-targets.md) -- Canonical target names for quality gates
- [Git Push Default Convention](./git-push-default.md) -- Governs the default `worktree-to-pr` push target and the explicit direct-push modes; this convention governs what happens once a PR exists
- [Plans Organization Convention — Delivery Mode](../../conventions/structure/plans/32-delivery-mode-the-four-modes.md#delivery-mode) -- The four-mode vocabulary and three-tier precedence that determines when this protocol applies
- `repo-governance/workflows/pr/pr-review-quality-gate.md` -- The review/fix cycle that runs before a `worktree-to-pr` PR meets the done-definition described above
