---
title: "Git Push Default Convention"
description: Default git push behavior — the repo-wide default integration target is a PR branch opened against main (worktree-to-pr), with direct push to origin main available via the worktree-to-origin-main and main-to-origin-main modes when explicitly selected. Covers linear history requirement and proactive preexisting compliance. Governs plan-maker, plan-checker, plan-fixer, and the plan-execution workflow behavior.
category: explanation
subcategory: development
tags:
  - git
  - workflow
  - push
  - trunk-based-development
  - ai-agents
created: 2026-04-25
---

# Git Push Default Convention

The repo-wide default integration target for every push is a **PR branch opened against `main`**
(the `worktree-to-pr` delivery mode). Direct push to `origin main` remains fully available — through
the `worktree-to-origin-main` and `main-to-origin-main` modes — but it is an explicit selection, never
an inferred one. This applies to all contexts: general work, plan creation, plan checking, plan fixing,
and plan execution. The canonical four-mode vocabulary and the three-tier precedence that resolves
which mode is active live in the
[Plans Organization Convention — Delivery Mode](../../conventions/structure/plans.md#delivery-mode);
this convention governs the push mechanics for each mode.

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: A single,
  deterministic three-tier precedence (invocation argument > plan field > default) resolves the active
  delivery mode in every context. There is exactly one default (`worktree-to-pr`) and exactly one way
  to override it — no ambiguity about which push target applies.

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: The
  default must be stated, not assumed. `worktree-to-pr` is the stated repo-wide default; the
  direct-push modes (`worktree-to-origin-main`, `main-to-origin-main`) are explicit opt-ins, declared
  via an invocation argument or a plan's `## Delivery Mode` field — never inferred from execution
  context, change size, or past sessions.

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: Before
  pushing directly to `origin main`, an agent must confirm a direct-push mode was actually selected
  (invocation argument or plan field). Pushing directly on the assumption that "no PR was mentioned" is
  a failure of deliberate problem-solving — the default is a PR branch, not direct push.

- **[Root Cause Orientation](../../principles/general/root-cause-orientation.md)**: When preexisting
  plan documents still assume the old direct-push-only posture, fixing them immediately is the
  root-cause-oriented choice. Deferring known mismatches accumulates governance debt.

## Conventions Implemented/Respected

This practice implements/respects the following conventions:

- **[Trunk Based Development Convention](./trunk-based-development.md)**: TBD establishes `main` as the
  trunk and recognizes short-lived-branch-via-PR as a valid TBD flavor alongside direct commit. This
  convention makes the push mechanics of each delivery mode explicit for AI agents.

- **[Plans Organization Convention](../../conventions/structure/plans.md)**: Plan documents declare
  their delivery mode via an optional `## Delivery Mode` field; absent that field (and absent an
  overriding invocation argument), `worktree-to-pr` applies. This convention governs how agents read
  and execute delivery checklists under each mode.

- **[Proactive Preexisting Error Resolution](../practice/proactive-preexisting-error-resolution.md)**:
  When a preexisting violation of this convention surfaces during work — such as a delivery checklist
  still tagging the merge step `[AI]` under a `*-to-pr` mode, or a checklist assuming direct push
  without declaring a mode — fix it immediately. This convention operationalizes that practice for
  git-push violations.

## Scope

### What This Convention Covers

- Default push and PR-opening behavior for every delivery mode.
- Linear history maintenance before every push, whether to a PR branch or to `origin main`.
- Agent behavior in all plan contexts: `plan-maker`, `plan-checker`, `plan-fixer`, and the
  plan-execution workflow.
- Delivery checklist authoring — plan documents must declare a `## Delivery Mode` field only when
  overriding the default, and must tag git-mechanical steps correctly for the resolved mode.
- Retroactive compliance — preexisting violations fixed when encountered.

### What This Convention Does NOT Cover

- Force-push and `--no-verify` safety rules: governed by the
  [Git Push Safety Convention](./git-push-safety.md).
- PR merge approval, the PR-Review Maker→Fixer Cycle, and the done-definition once a PR is opened:
  governed by the [PR Merge Protocol Convention](./pr-merge-protocol.md).
- The full four-mode vocabulary and the precedence algorithm itself: defined once, canonically, in the
  [Plans Organization Convention — Delivery Mode](../../conventions/structure/plans.md#delivery-mode).

## Standards

### Standard 1: Default Integration Target Is a PR Branch

Absent an explicit override, every delivery uses `worktree-to-pr`: work happens on a plan-scoped branch
inside a disposable worktree, and the integration target is a draft PR opened against `main`.

```bash
# Default workflow — worktree-to-pr
git worktree add worktrees/<plan-id> -b <plan-id>
cd worktrees/<plan-id>
git add <files>
git commit -m "feat(scope): description"
git push origin <plan-id>
gh pr create --draft --base main --title "feat(scope): description"
```

This is the correct behavior in all of the following situations, absent an explicit mode override:

- General development work.
- Plan creation, plan quality-gate runs, and plan archival.
- Governance convention and workflow authoring.
- Agent definition updates under `.claude/agents/`.
- Any other change not explicitly assigned a direct-push mode.

### Standard 2: Direct Push Modes Are Explicit Selections, Not Inferred

`worktree-to-origin-main` and `main-to-origin-main` push directly to `origin main` with no PR. Either
mode applies only when explicitly selected — via an invocation argument or a plan's `## Delivery Mode`
field. Absent that explicit selection, the agent uses the `worktree-to-pr` default.

```bash
# worktree-to-origin-main — explicit selection only
git worktree add worktrees/<plan-id> -b <plan-id>
cd worktrees/<plan-id>
git add <files>
git commit -m "fix(scope): description"
git push origin main
```

Signals that constitute an explicit direct-push selection:

- An invocation argument naming `worktree-to-origin-main` or `main-to-origin-main`.
- A `## Delivery Mode` field in the plan declaring one of those two modes.

No other signal constitutes an implicit selection of a direct-push mode. The agent must not infer a
direct-push intent from:

- The size or risk of the change.
- A desire to "save time" or "skip review".
- Past sessions in which direct push was used.

### Standard 3: Plans Must Declare a Delivery Mode Only to Override the Default

When `plan-maker` authors a plan, it does not need to add a `## Delivery Mode` field for the default
case — `worktree-to-pr` applies automatically. `plan-maker` adds an explicit `## Delivery Mode` field
only when the plan calls for a different mode (`worktree-to-origin-main`, `main-to-origin-main`, or
`main-to-pr`), and must state the justification alongside it.

`plan-checker` must flag any plan whose delivery checklist assumes a direct push to `origin main`
without a corresponding `## Delivery Mode` field declaring one of the direct-push modes. `plan-fixer`
must either add the missing field (if a direct-push mode is genuinely warranted) or correct the
checklist to the `worktree-to-pr` default.

The plan-execution workflow resolves the active mode once, at Step 0, per the three-tier precedence,
and uses that resolution for every subsequent git-mechanical step in the plan.

### Standard 4: Maintain Linear History Before Pushing

Before pushing — whether to a PR branch or to `origin main` — ensure the local branch has a linear
history with respect to its remote counterpart. If the remote has moved forward since the last pull or
push, rebase rather than merge:

```bash
# If remote has new commits since last pull, rebase first
git pull --rebase origin <target-branch>
# Then push
git push origin <target-branch>
```

Never create merge commits when pushing to `main` or to a PR branch. A merge commit in the history
violates this standard. If a merge commit appears locally, squash or rebase it before pushing. When a
PR is ready to land, prefer GitHub's squash or rebase merge over a local `git merge` — the
[PR Merge Protocol](./pr-merge-protocol.md) governs that final step.

### Standard 5: Proactively Fix Delivery-Mode Mismatches

When working on plans or performing any task that involves reading delivery checklists, and you
encounter an existing checklist that mis-tags the merge step, omits a required `## Delivery Mode`
override, or otherwise assumes a stale push default, fix it as part of your current work. Do not defer
it.

This applies Standard 4 of
[Proactive Preexisting Error Resolution](../practice/proactive-preexisting-error-resolution.md) to this
convention specifically: a delivery-mode mismatch in a plan you touch is an error to fix now, not flag
for later.

**Scope of "fix now"**: correct the mismatch in the checklist and, if the plan is in
`plans/in-progress/`, note the fix in the same commit message. If the plan is in `plans/done/`
(archived), leave it — historical records are read-only.

### Standard 6: Worktree Execution Does Not Determine the Mode by Itself

Running from inside a git worktree does not, by itself, select a push target. Work location (worktree
vs. primary checkout) and integration target (PR vs. direct push) are independent axes — the active
mode is whichever the three-tier precedence resolves to.

This standard covers all worktree execution patterns:

- An AI agent using `isolation: "worktree"` in the Agent tool.
- An agent or developer session started inside a path created by `git worktree add`.
- Any working directory under `worktrees/` or any other `git worktree add` target.

Running from a worktree resolves to `worktree-to-pr` (the default) unless an invocation argument or the
plan's `## Delivery Mode` field explicitly selects `worktree-to-origin-main`. Running from the primary
checkout (no worktree) resolves to `main-to-origin-main` or `main-to-pr` under the same precedence —
never inferred from the mere absence of a worktree.

## Examples

### PASS: Correct behavior — default worktree-to-pr

```
Plan executor: Delivering governance convention update via the default mode.

  git worktree add worktrees/git-push-default-update -b git-push-default-update
  cd worktrees/git-push-default-update
  git add repo-governance/development/workflow/git-push-default.md
  git commit -m "feat(governance): update git push default convention"
  git push origin git-push-default-update
  gh pr create --draft --base main --title "feat(governance): update git push default convention"

Draft PR opened. Iterating until the done-definition is met, then handing off for human merge.
```

### FAIL: Incorrect behavior — pushing directly without an explicit mode selection

```
Plan executor: Committing governance convention.

  git add repo-governance/development/workflow/git-push-default.md
  git commit -m "feat(governance): add git push default convention"
  git push origin main

Done. Convention is now on main.
```

No `## Delivery Mode` field and no invocation argument selected a direct-push mode. The default is
`worktree-to-pr`; pushing straight to `origin main` here is wrong.

### PASS: Correct behavior when a direct-push mode is explicitly selected

Plan's `## Delivery Mode` field: `worktree-to-origin-main` — "single-line config fix, no review
warranted."

```
Plan executor: Delivering per the plan's declared worktree-to-origin-main mode.

  git worktree add worktrees/fix-config-typo -b fix-config-typo
  cd worktrees/fix-config-typo
  git add config/settings.json
  git commit -m "fix(config): correct typo in feature flag name"
  git push origin main
  git worktree remove worktrees/fix-config-typo

Pushed directly to origin main per the plan's declared delivery mode.
```

### FAIL: Incorrect plan-maker behavior — assuming direct push without declaring the mode

User prompt: "Plan a governance update for Y."

```markdown
<!-- In delivery.md — WRONG -->

- [ ] [AI] Create convention file
- [ ] [AI] Update README index
- [ ] [AI] git add, commit, and push directly to origin main ← no ## Delivery Mode field declares this
```

No `## Delivery Mode` field justifies skipping the `worktree-to-pr` default. `plan-checker` must flag
this. `plan-fixer` must either add a justified `## Delivery Mode` override or correct the checklist to
the default PR-branch flow.

### FAIL: Incorrect plan-maker behavior — `[HUMAN]` tag on a git-mechanical step

User prompt: "Plan a feature for Z." (default `worktree-to-pr` mode applies; no direct-push override)

```markdown
<!-- In delivery.md — WRONG -->

- [ ] [HUMAN] Create worktree: `git worktree add worktrees/feature-z -b feature-z`
- [ ] [HUMAN] Review the diff and approve push to the PR branch
- [ ] [HUMAN] Remove the worktree: `git worktree remove worktrees/feature-z`
```

All three are plain git-mechanical steps an agent performs directly. Under `worktree-to-pr`, the only
step that is legitimately `[HUMAN]` is the final PR merge itself — everything up to and including
opening/flipping the PR is `[AI]`. These are mis-tags per
[Plans Organization Convention §Executor Tagging](../../conventions/structure/plans.md#executor-tagging--ai-vs-human-hard-rule).
`plan-checker` flags them; `plan-fixer` retags them `[AI]`.

### PASS: Correct plan-maker behavior — git-mechanical steps tagged `[AI]`, merge tagged `[HUMAN]`

```markdown
<!-- In delivery.md — RIGHT -->

- [ ] [AI] Create worktree: `git worktree add worktrees/feature-z -b feature-z`
- [ ] [AI] Commit, push, and open a draft PR against `main`
- [ ] [AI] Run the PR-Review Maker→Fixer Cycle until the done-definition is met, then flip to ready
- [ ] [HUMAN] Merge the PR
- [ ] [AI] Remove the worktree: `git worktree remove worktrees/feature-z`
```

### PASS: Correct linear history before push

```bash
# Remote moved forward — rebase first
git pull --rebase origin <target-branch>
git push origin <target-branch>
```

### FAIL: Merge commit created on push

```bash
# Wrong — creates merge commit
git pull origin <target-branch>       # produces merge commit
git push origin <target-branch>       # pushes linear-history violation
```

Use `--rebase` instead.

### PASS: Proactive fix of preexisting mismatch

While executing Plan A, the plan-execution workflow reads `plans/in-progress/feature-x/delivery.md` and
finds:

```markdown
- [x] Implement feature
- [ ] [HUMAN] Commit and push to origin main ← no ## Delivery Mode field; default worktree-to-pr applies
```

Correct behavior: retag the step `[AI]`, route it through the default `worktree-to-pr` flow (branch,
PR, review cycle, human merge), and include the fix in the same commit as the plan work.

## Agent Responsibilities

| Agent                                       | Responsibility                                                                                                                                                                              |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plan-maker`                                | Applies `worktree-to-pr` by default; adds a justified `## Delivery Mode` field only when overriding it.                                                                                     |
| `plan-checker`                              | Flags delivery checklists that assume direct push without a declared override, and mis-tagged `[HUMAN]`/`[AI]` git-mechanical steps.                                                        |
| `plan-fixer`                                | Corrects mode-mismatched checklists and retags mis-tagged git-mechanical steps.                                                                                                             |
| plan-execution workflow                     | Resolves the delivery mode once at Step 0 via the three-tier precedence; pushes to the resolved integration target; rebases to maintain linear history; fixes preexisting mismatches found. |
| plan-execution workflow in worktree context | Same as above — worktree execution is one axis of the mode, not the whole mode; resolves per the precedence, not by inference from context.                                                 |

## Related Documentation

- [Trunk Based Development Convention](./trunk-based-development.md) — Git workflow establishing `main`
  as the trunk and short-lived-branch-via-PR as the default TBD flavor.
- [Git Push Safety Convention](./git-push-safety.md) — Approval rules for force-push and `--no-verify`,
  applicable to both PR-branch and direct pushes.
- [PR Merge Protocol Convention](./pr-merge-protocol.md) — The PR-Review Maker→Fixer Cycle, done-
  definition, and approval rules once a PR is opened under `*-to-pr` modes.
- [CI Post-Push Verification Convention](./ci-post-push-verification.md) — CI post-push verification
  applies to pushes on both PR branches and `origin main`.
- [Proactive Preexisting Error Resolution](../practice/proactive-preexisting-error-resolution.md) —
  Practice governing proactive fixes of discovered violations.
- [Plans Organization Convention — Delivery Mode](../../conventions/structure/plans.md#delivery-mode) —
  The canonical four-mode vocabulary, the `## Delivery Mode` field syntax, and the three-tier
  precedence algorithm this convention's push mechanics implement.
