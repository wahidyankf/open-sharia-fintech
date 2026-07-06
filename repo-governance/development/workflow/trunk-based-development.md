---
title: "Trunk Based Development Convention"
description: Git workflow using Trunk Based Development (TBD) for continuous integration and rapid delivery
category: explanation
subcategory: development
tags:
  - trunk-based-development
  - git
  - workflow
  - development
  - continuous-integration
created: 2025-11-26
---

# Trunk Based Development Convention

<!--
  MAINTENANCE NOTE: Master reference for TBD workflow
  This is duplicated (intentionally) in multiple files for different audiences:
  1. repo-governance/development/workflow/trunk-based-development.md (this file - comprehensive reference)
  2. AGENTS.md (summary for AI agents)
  3. .opencode/agents/plan-maker.md (context for plan creation)
  4. repo-governance/workflows/plan/plan-execution.md (context for plan execution — orchestrated by the calling context)
  When updating, synchronize all four locations.
-->

This document defines the **Trunk Based Development (TBD)** workflow used in the open-sharia-enterprise project. TBD is a branching strategy where developers commit directly to a single branch (the trunk), enabling continuous integration, rapid feedback, and simplified collaboration.

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: Single branch (`main`) instead of complex GitFlow with multiple long-lived branches (develop, release, hotfix). Small, frequent commits instead of large, delayed integrations. Flat workflow reduces merge conflicts and coordination overhead.

- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)**: Every commit to `main` triggers automated CI testing. Integration issues caught immediately by machines, not discovered weeks later through manual testing. Continuous automated validation replaces manual integration phases.

## Conventions Implemented/Respected

**REQUIRED SECTION**: All development practice documents MUST include this section to ensure traceability from practices to documentation standards.

This practice implements/respects the following conventions:

- **[Commit Message Convention](./commit-messages.md)**: TBD workflow requires small, frequent commits with clear conventional commit messages to maintain navigable history.

- **[Code Quality Convention](../quality/code.md)**: Pre-push hooks run affected tests before pushing to main, enforcing quality gates in the TBD workflow.

## What is Trunk Based Development?

**Trunk Based Development** is a source control branching model where developers work primarily on a single branch called the "trunk" (in Git, this is typically the `main` branch). Unlike feature-branch workflows, TBD minimizes long-lived branches and emphasizes frequent integration.

### Core Characteristics

1. **Single source of truth**: All work converges on one branch (`main`)
2. **Short-lived branches** (if any): Branches exist for < 1-2 days maximum
3. **Frequent commits**: Multiple commits per day to `main`
4. **Feature flags**: Hide incomplete work using toggles, not branches
5. **Continuous integration**: Every commit triggers automated testing
6. **Small changes**: Break work into tiny, mergeable increments

### TBD and the Short-Lived Branch-via-PR Flavor

TBD's defining tenet is avoiding **long-lived** branches — not avoiding branches altogether.
[TrunkBasedDevelopment.com](https://trunkbaseddevelopment.com/) documents short-lived branches reviewed
via pull request as an accepted TBD flavor alongside pure direct-commit, provided branches stay
short-lived (merged per the lifespan rules below — ideally same day, 1-2 days maximum) and integration
into `main` stays frequent. Routing a short-lived, single-purpose plan branch through a PR before it
lands on `main` therefore does not contradict TBD; it is one of TBD's recognized shapes.

This repository's **repo-wide default delivery mode is `worktree-to-pr`**: a short-lived plan branch
inside a disposable git worktree, pushed to a PR, driven to a green and fully-reviewed state, then
merged by a human. Pure direct-commit-to-`main` remains a fully supported alternative mode. See
[Default Push and Worktree Execution](#default-push-and-worktree-execution) below for the mechanics of
all four delivery modes, and the
[Plans Organization Convention — Delivery Mode](../../conventions/structure/plans.md#delivery-mode) for
the canonical four-mode vocabulary and the three-tier precedence that resolves which mode is active.

### Why We Use TBD

TBD addresses common problems with long-lived feature branches:

| Problem with Feature Branches           | TBD Solution                                      |
| --------------------------------------- | ------------------------------------------------- |
| FAIL: Merge conflicts after weeks       | PASS: Daily integration prevents large conflicts  |
| FAIL: Stale branches diverge from trunk | PASS: Always working on current codebase          |
| FAIL: Integration testing delayed       | PASS: Continuous integration catches issues early |
| FAIL: Code review bottlenecks           | PASS: Small, frequent reviews are faster          |
| FAIL: "Integration hell" before release | PASS: Code is always in releasable state          |
| FAIL: Hard to coordinate teams          | PASS: Everyone sees changes immediately           |
| FAIL: Feature branches hide WIP         | PASS: Feature flags make incompleteness explicit  |
| FAIL: Delayed feedback from CI          | PASS: Immediate CI feedback on every commit       |

**Reference**: [TrunkBasedDevelopment.com](https://trunkbaseddevelopment.com/)

## Our TBD Implementation

### Default Branch: `main`

- **The trunk is `main`**: All development happens on `main` branch
- **No `develop` branch**: We don't use GitFlow or similar multi-branch strategies
- **No release branches**: Releases are tagged commits on `main`
- **No hotfix branches**: Hotfixes commit directly to `main` (or very short-lived branches)

### Working on `main` Directly

> This subsection describes TBD's classic direct-commit-to-trunk shape — one of the two direct-push
> delivery modes available in this repo (`worktree-to-origin-main`, `main-to-origin-main`). This
> repository's own **repo-wide default** is the short-lived-branch-via-PR shape (`worktree-to-pr`) —
> see [Default Push and Worktree Execution](#default-push-and-worktree-execution) below.

**One available workflow**: commit directly to `main` when:

PASS: **You should commit directly to `main` when**:

- Change is small and well-tested
- You're confident tests will pass
- Change won't break others' work
- Feature flags hide incomplete functionality
- You can commit and push multiple times per day

**Example workflow**:

```bash
# Work on main branch
git checkout main
git pull origin main

# Make small change
# ... edit files ...

# Test locally
npm test

# Commit directly to main
git add .
git commit -m "feat(auth): add email validation helper"
git push origin main

# CI runs automatically
# Change is now visible to entire team
```

### Short-Lived Branches (the Default Shape)

Under the repo-wide `worktree-to-pr` default, a short-lived plan branch is the norm, not the exception.
Direct commit to `main` (`worktree-to-origin-main`, `main-to-origin-main`) remains the norm only for
small, well-understood changes -- see [Direct-Push Modes Remain Fully Available](#direct-push-modes-remain-fully-available)
below.

Branches are also used, as they always have been, for:

- **External contribution**: Outside contributor submitting a PR (fork-based, not a plan branch).
- **Regulatory requirement**: Compliance mandates review before merge.
- **Pair/mob programming**: Collaborating on a branch before merging.

**Branch workflow**:

```bash
# Create short-lived plan branch inside a worktree
git worktree add worktrees/feature-user-login -b feature-user-login
cd worktrees/feature-user-login

# Make changes
# ... edit files ...
git commit -m "feat(auth): implement login endpoint"

# Push frequently
git push origin feature-user-login

# Open the PR as a draft immediately
gh pr create --draft --base main --title "feat(auth): implement login endpoint"

# Get review within hours (not days), run the PR-Review Maker->Fixer Cycle

# When the done-definition is met, flip to ready and let a human merge via GitHub
# (squash or rebase merge -- never a local `git merge`, to preserve linear history):
gh pr ready

# After merge, remove the worktree
git worktree remove worktrees/feature-user-login
```

**Branch lifespan rules**:

- PASS: **< 1 day**: Ideal - merge same day you created it
- **1-2 days**: Acceptable maximum
- FAIL: **> 2 days**: Too long - branch is stale, rebase or abandon

### Feature Flags for Incomplete Work

**Instead of hiding incomplete features in branches, use feature flags (toggles) to hide them in production.**

**Why feature flags?**

- Code is integrated immediately (prevents merge conflicts)
- Incomplete features don't affect production users
- Can toggle features on/off without deployments
- Enables testing in production environments
- Allows gradual rollouts and A/B testing

**Feature flag patterns**:

#### Simple Boolean Flag

```javascript
// config/features.js
const FEATURES = {
  NEW_DASHBOARD: process.env.ENABLE_NEW_DASHBOARD === "true",
  ADVANCED_SEARCH: process.env.ENABLE_ADVANCED_SEARCH === "true",
};

// In code
if (FEATURES.NEW_DASHBOARD) {
  // Show new dashboard (incomplete, under development)
  return renderNewDashboard();
} else {
  // Show old dashboard (production-ready)
  return renderOldDashboard();
}
```

#### Environment-Based Flags

```javascript
// Only enable in development/staging
const FEATURE_ENABLED = ["development", "staging"].includes(process.env.NODE_ENV);

if (FEATURE_ENABLED) {
  // New feature code (not ready for production)
}
```

#### User-Based Flags

```javascript
// Enable for specific users (beta testers)
const betaUsers = ["user1@example.com", "user2@example.com"];

if (betaUsers.includes(currentUser.email)) {
  // Show beta feature
}
```

**Feature flag lifecycle**:

1. **Add flag**: Create flag for new feature
2. **Develop with flag OFF in prod**: Commit to `main`, flag hides feature in production
3. **Test with flag ON in staging**: Verify feature works in non-production
4. **Enable in production**: Flip flag when feature is complete
5. **Remove flag**: After feature is stable, remove flag and old code path

**Important**: Feature flags are temporary. Once a feature is stable, remove the flag and delete the old code path. Don't accumulate flags indefinitely.

### Continuous Integration

**Every commit to `main` triggers CI/CD**:

1. **Automated tests** run on every push
2. **Build verification** ensures code compiles
3. **Linting and formatting** checks pass
4. **Deployment to staging** (optional, project-specific)

**CI failure is a high priority**:

- FAIL: **Never commit code that breaks CI**
- **If CI fails**, fix immediately (highest priority)
- **Broken `main` blocks everyone** - fix or revert

**Pre-push checklist**:

- [ ] All tests pass locally (`npm test`)
- [ ] Linting passes (`npm run lint`)
- [ ] Build succeeds (`npm run build`)
- [ ] Feature flags hide incomplete work
- [ ] Commit message follows [Conventional Commits](./commit-messages.md)

### Small, Incremental Changes

**TBD requires breaking work into small chunks**:

PASS: **Good incremental changes**:

- Add a utility function (commit 1)
- Add tests for the function (commit 2)
- Use function in one component (commit 3)
- Extend function for new use case (commit 4)

FAIL: **Bad large changes**:

- Rewrite entire authentication system in one commit
- Implement 5 features together in one PR
- Refactor + add features in same commit

**Benefits of small changes**:

- **Faster reviews**: Reviewing 50 lines vs 5000 lines
- **Easier to revert**: If something breaks, revert is surgical
- **Clearer history**: Each commit has single, clear purpose
- **Reduced conflicts**: Less time diverged = fewer conflicts
- **Earlier feedback**: Team sees your work immediately

**How to break down work**:

1. **Identify smallest deliverable**: What's the tiniest useful piece?
2. **Commit that piece**: Push to `main`
3. **Repeat**: Build on top of previous work
4. **Use feature flags**: Hide incomplete full features

**Example - "Add user login" broken down**:

```
Commit 1: feat(auth): add User model with email field
Commit 2: feat(auth): add password hashing utility
Commit 3: feat(auth): add login endpoint (feature flag OFF)
Commit 4: feat(auth): add login UI component (feature flag OFF)
Commit 5: feat(auth): connect UI to endpoint (feature flag OFF)
Commit 6: test(auth): add integration tests for login
Commit 7: feat(auth): enable login feature flag in staging
Commit 8: feat(auth): enable login feature flag in production
Commit 9: refactor(auth): remove old login code and feature flag
```

Each commit is small, tested, and doesn't break `main`.

## Default Push and Worktree Execution

This section clarifies the default delivery mode and how git worktrees relate to it. The default is
consistent across all execution contexts and is defined once, canonically, in the
[Plans Organization Convention — Delivery Mode](../../conventions/structure/plans.md#delivery-mode):
four modes (`worktree-to-pr` **(default)**, `worktree-to-origin-main`, `main-to-origin-main`,
`main-to-pr`), each fixing a work location, an integration target, and a merge authority, resolved by
a three-tier precedence (invocation argument > plan field > default). This document does not redefine
that vocabulary — it explains how each mode plays out for TBD and for worktree execution specifically.

### Default Delivery Mode: `worktree-to-pr`

**The repo-wide default for all development -- including when running from a git worktree -- is
`worktree-to-pr`: a short-lived, single-purpose plan branch inside a disposable git worktree, pushed
to a draft PR opened against `main`, driven through review and CI to a fully green state, then merged
by a human.**

- **Work location**: `worktrees/<plan-identifier>/`, on a plan-scoped branch.
- **Integration target**: a PR opened against `main` (opened as a GitHub **draft**; see Why Draft below).
- **Merge authority**: `[HUMAN]` -- the AI drives the branch, the push, the review cycle, and the
  quality gates; a human performs the actual merge, on their own schedule. This mirrors the
  [PR Merge Protocol](./pr-merge-protocol.md) done-boundary: the AI hands off a green, fully-reviewed
  PR; "done" (for the AI) is not "merged".
- Quality gates run on every push to the PR branch via the pre-push hook (typecheck, lint, test:quick,
  specs:coverage) AND on the PR itself via CI.
- `*-to-pr` deliveries additionally run the **PR-Review Maker→Fixer Cycle**
  (`repo-governance/workflows/pr/pr-review-quality-gate.md`) before the PR is considered done --
  see that workflow doc and the [PR Merge Protocol](./pr-merge-protocol.md) for the full cycle and
  done-definition.

This applies to all routine development: features, bug fixes, refactors, documentation, governance
changes, and work executed inside a git worktree -- the default is the same regardless of context.

```bash
# Default workflow -- worktree-to-pr (applies in worktrees, which is now the norm)
git worktree add worktrees/<plan-id> -b <plan-id>
cd worktrees/<plan-id>
# ... make changes ...
git add .
git commit -m "feat(auth): add email validation"
git push origin <plan-id>

# Open as a draft -- not yet soliciting review
gh pr create --draft --base main --title "feat(auth): add email validation"

# Iterate: push follow-up commits, run the PR-Review Maker->Fixer Cycle, keep CI green

# When the done-definition is met (see PR Merge Protocol), flip to ready:
gh pr ready
# A human reviews and merges -- outside the AI's done-boundary
```

### Why Draft, Not Ready-for-Review, on Open

Opening every `worktree-to-pr` branch as a draft is deliberate:

- **Signals in-progress status** to humans and CI -- the branch is not yet soliciting review.
- **Prevents accidental auto-merge paths** that some "ready" PRs can trigger.
- **Preserves the explicit human moment** when the AI flips the PR to ready after meeting the
  done-definition, which is the natural place for the [PR Merge Protocol](./pr-merge-protocol.md)
  approval prompt to fire.

### Direct-Push Modes Remain Fully Available

Two modes commit and push directly to `origin main`, with `[AI]` performing the push itself -- no
branch, no PR, no review gate:

- **`worktree-to-origin-main`** -- work happens in a disposable worktree, but pushes land directly on
  `origin main`.
- **`main-to-origin-main`** -- work happens in the primary checkout (no worktree), pushing directly to
  `origin main`.

Both remain fully valid TBD flavors -- they are TBD's classic direct-commit shape. Select one of these
over the default when the change is small, well-understood, and does not warrant a review pass -- for
example, a single-line typo fix or a mechanical rename. See the
[Git Push Default Convention](./git-push-default.md) for the full push mechanics of these two modes,
including the linear-history and rebase requirements.

**A fourth mode, `main-to-pr`,** uses the primary checkout (no worktree) but still routes through a PR
-- useful when isolation via worktree is unnecessary but review is still wanted.

**Plan delivery checklist tagging**: the git-mechanical lifecycle steps -- create worktree, commit,
push (to the PR branch or to `origin main`, depending on mode), open/flip the PR, and remove worktree
-- MUST be tagged `[AI]`, never `[HUMAN]`, in plan delivery checklists. The one step that is
legitimately `[HUMAN]` under `*-to-pr` modes is the merge itself. See
[Plans Organization Convention §Executor Tagging](../../conventions/structure/plans.md#executor-tagging--ai-vs-human-hard-rule)
and the [Git Push Default Convention §Examples](./git-push-default.md#examples) for the FAIL/PASS
examples.

### Mode Selection Does Not Depend on Execution Context Alone

Running from inside a git worktree does not, by itself, force a PR -- a plan may still declare
`worktree-to-origin-main` and push directly. Conversely, running from the primary checkout does not
force direct push either -- `main-to-pr` uses the primary checkout while still routing through a PR.
Work location (worktree vs. primary checkout) and integration target (PR vs. direct push) are
independent axes; the active mode is whichever the three-tier precedence resolves to (invocation
argument > plan field > default `worktree-to-pr`), never inferred from execution context alone.

### Decision Table

| Situation                               | Resolved Delivery Mode (absent an explicit override)    |
| --------------------------------------- | ------------------------------------------------------- |
| Routine development, no mode specified  | `worktree-to-pr` (repo-wide default)                    |
| Plan declares `worktree-to-origin-main` | Worktree work location, direct push to `origin main`    |
| Plan declares `main-to-origin-main`     | Primary checkout, direct push to `origin main`          |
| Plan declares `main-to-pr`              | Primary checkout, PR opened against `main`              |
| Invocation argument names a valid mode  | The named mode overrides the plan field and the default |
| External contribution                   | Fork + PR (follows the `*-to-pr` review/merge protocol) |

### Key Principle

The active delivery mode is resolved deterministically, never inferred from execution context alone:

- **Tier 1 (highest)**: an explicit invocation argument naming a valid mode.
- **Tier 2**: a `## Delivery Mode` field declared in the plan's own docs.
- **Tier 3 (default)**: `worktree-to-pr`.

See the [Plans Organization Convention — Delivery Mode](../../conventions/structure/plans.md#delivery-mode)
for the full algorithm and the [plan-execution workflow](../../workflows/plan/plan-execution.md) for
how each mode changes Step 0 (worktree entry), the per-phase push target, and Step 8 (finalization and
merge hand-off).

Note: this does **not** affect environment branches (`prod-ayokoding-www`, `prod-ose-www`, `stag-organiclever-app-web`, `stag-organiclever-be`). Those follow their own documented deployment workflows. The OrganicLever app staging branches (`stag-organiclever-app-web`, `stag-organiclever-be`) are CI-automated by `organiclever-app-test-local-deploy-stag.yml`. Production promotion for the OrganicLever app is **deferred** to a separate plan — no production-CD workflow exists yet.

## When Branches Are Appropriate

Under the repo-wide `worktree-to-pr` default, a short-lived branch is the norm for routine development,
not an exception carved out from an otherwise branchless workflow. The cases below describe situations
where a branch (via a plan's `worktree-to-pr` mode, or an external fork) has always been the natural
fit -- they remain equally valid today, just no longer framed as rare deviations:

### Code Review Requirement

If your team/organization mandates peer review via Pull Requests:

- PASS: **Create branch** for PR workflow
- PASS: **Get review within 24 hours** (not days)
- PASS: **Merge immediately** after approval
- PASS: **Delete branch** right after merge

**Minimize branch lifespan**: The goal is still rapid integration.

### Experimental/Spike Work

When exploring a new approach with high uncertainty:

- PASS: **Create branch** for experimentation
- PASS: **Set time limit** (e.g., "1 day to spike this approach")
- PASS: **Decision point**: Keep and merge, or discard entirely
- PASS: **Don't let spikes become features**: Decide quickly

### External Contributors

When accepting contributions from outside the team:

- PASS: **Fork + PR workflow** is standard
- PASS: **Review and merge quickly** to reduce staleness
- PASS: **Guide contributor** to make small, focused PRs

### Regulatory/Compliance

If industry regulations require documented review:

- PASS: **Use branches + PRs** for audit trail
- PASS: **Still minimize branch lifespan** (review quickly)
- PASS: **Automate compliance checks** in CI

### Environment/Deployment Branches

**Long-lived environment branches are explicitly allowed in TBD.** These are NOT feature branches.

Environment branches serve deployment purposes, not feature isolation:

- PASS: **Production branches**: Trigger deployment to production environment
- PASS: **Staging branches**: Trigger deployment to staging environment
- PASS: **Environment-specific configuration**: Different settings per environment

**Key distinction**: Environment branches reflect deployment state, not development work.

**Example in this repository: `prod-ayokoding-www`**

The `apps/ayokoding-www/` project uses a production deployment branch:

- **Branch**: `prod-ayokoding-www`
- **Purpose**: Triggers automatic deployment to ayokoding.com via Vercel
- **Location**: Deploys `apps/ayokoding-www/` (Next.js 16 application)
- **Workflow** (automated):
  1. All development happens in `main`
  2. The `ayokoding-www-test-local-deploy-prod.yml` GitHub Actions workflow runs at 6 AM and 6 PM WIB, detects changes in `apps/ayokoding-www/`, builds, then force-pushes `main` to `prod-ayokoding-www`
  3. Push to `prod-ayokoding-www` triggers production deployment via Vercel
- **Important**: Never commit directly to `prod-ayokoding-www` outside the CI automation

**Why this is TBD-compliant**:

- Development still happens on `main` (trunk)
- No feature isolation in branches
- `prod-ayokoding-www` is a deployment trigger, not a development workspace
- Changes flow from `main` to `prod-ayokoding-www`, never the reverse
- Consistent with TBD principles: environment branches are for release management, not feature development

**Reference**: [TrunkBasedDevelopment.com - Branch for Release](https://trunkbaseddevelopment.com/branch-for-release/) explicitly describes release branches as acceptable in TBD.

## What NOT to Do

| FAIL: Anti-Pattern                   | PASS: TBD Approach                                                                          |
| ------------------------------------ | ------------------------------------------------------------------------------------------- |
| Long-lived feature branches          | Commit to `main` with feature flags                                                         |
| Branches per developer               | All developers commit to `main`                                                             |
| Delaying integration for weeks       | Integrate multiple times per day                                                            |
| Large, infrequent commits            | Small, frequent commits (see [Commit Granularity](./commit-messages.md#commit-granularity)) |
| Keeping branches "just in case"      | Delete branches immediately after merge                                                     |
| Using branches to hide WIP           | Use feature flags to hide WIP                                                               |
| Merging without CI passing           | CI must be green before merge                                                               |
| Long-lived branches surviving days   | Branches (if used) stay short-lived -- merge within 1-2 days                                |
| Waiting for "perfect" code to commit | Commit working code, iterate in subsequent commits                                          |
| Feature branches lasting weeks       | Branches (if used) last < 2 days                                                            |

## TBD and Project Planning

### Plans Declare a Delivery Mode

When creating project plans in `plans/` folder:

- PASS: **Default assumption**: `worktree-to-pr` (repo-wide default) -- a short-lived plan branch in a
  disposable worktree, pushed to a draft PR, merged by a human after the done-definition is met.
- PASS: **Declare the mode explicitly** using a `## Delivery Mode` field only when overriding the
  default (see the [Plans Organization Convention — Delivery Mode](../../conventions/structure/plans.md#delivery-mode)
  for the field syntax and the three-tier precedence).
- **If a direct-push mode is chosen** (`worktree-to-origin-main`, `main-to-origin-main`): document why
  in the plan (e.g., "single-line config fix, no review warranted").

**Example plan delivery.md (default mode, no field needed)**:

```markdown
## Overview

All implementation happens on a `worktree-to-pr` plan branch (the repo-wide default -- no
`## Delivery Mode` field needed) using feature flags to hide incomplete work.

**Feature flags**:

- `ENABLE_NEW_PAYMENT_FLOW` - Hides new payment integration until ready

**Phases**:

1. Phase 1: Add payment models
2. Phase 2: Add payment API (flag OFF)
3. Phase 3: Add payment UI (flag OFF)
4. Phase 4: Integration testing (flag ON in staging)
5. Phase 5: Production rollout (flag ON in production) -- PR merged by a human once green
```

### When Plans Override the Default Mode

Specify a non-default `## Delivery Mode` field in a plan if:

- **Trivial, well-understood change**: A single-line fix or mechanical rename that does not warrant a
  review pass -- use `worktree-to-origin-main` or `main-to-origin-main`.
- **External integration**: Working with a third party that requires a specific branch/PR shape.
- **Compliance**: A regulatory requirement changes the review process beyond the standard PR-review
  cycle.

**Example plan overriding the default**:

```markdown
## Delivery Mode

`worktree-to-origin-main`

**Justification**: This plan fixes a single typo in a config comment. The change is trivial and
well-understood; a full PR-review cycle is unnecessary overhead.
```

## TBD Benefits for This Project

### For Solo/Small Team Development

Even with a small team, TBD provides benefits:

- PASS: **Simplified workflow**: No mental overhead of managing multiple branches
- PASS: **No merge conflicts**: Less time diverged = fewer conflicts
- PASS: **Faster feedback**: CI runs on every commit
- PASS: **Clear history**: Linear commit history is easy to understand
- PASS: **No stale code**: Everything is current

### For Scaling the Team

As the team grows, TBD prevents common scaling problems:

- PASS: **Coordination**: Everyone works on same codebase, sees changes immediately
- PASS: **Onboarding**: Simpler workflow for new contributors
- PASS: **Accountability**: Commits are visible, encouraging quality
- PASS: **Release readiness**: `main` is always releasable

### For Continuous Deployment

TBD enables automated deployment:

- PASS: **Deployment from `main`**: Every commit can deploy to staging
- PASS: **Feature flags**: Control production rollouts without branches
- PASS: **Rapid fixes**: Hotfixes commit to `main` and deploy immediately
- PASS: **Rollback**: Revert commit or toggle flag off

## Migration from Feature Branches

If you're used to feature-branch workflows (GitFlow, GitHub Flow), here's how to transition:

### Mindset Shifts

| Feature Branch Mindset              | TBD Mindset                                             |
| ----------------------------------- | ------------------------------------------------------- |
| "I'll merge when feature is done"   | "I'll commit daily, hide with feature flag until done"  |
| "My branch is my workspace"         | "`main` is everyone's workspace"                        |
| "Integration happens at merge time" | "Integration happens continuously"                      |
| "Branches isolate risk"             | "Feature flags and tests manage risk"                   |
| "Review before merge"               | "Review can happen post-commit (or via short-lived PR)" |

### Transition Steps

1. **Start small**: Pick a simple task, commit directly to `main`
2. **Use feature flags**: Hide incomplete work, not branches
3. **Commit frequently**: Push to `main` multiple times per day
4. **Keep CI green**: Fix failures immediately
5. **Review old habits**: Notice when you create unnecessary branches

### Common Concerns Addressed

**"What if I break `main`?"**

- PASS: Tests and CI catch most issues before push
- PASS: Rapid revert if something slips through
- PASS: Feature flags hide incomplete features

**"What if I need to work on multiple things?"**

- PASS: Finish one thing before starting another
- PASS: Use feature flags to work incrementally
- PASS: Commit small pieces, don't wait for "done"

**"What about code review?"**

- PASS: Review can happen post-commit (async)
- PASS: Or use very short-lived PR branches (< 1 day)
- PASS: Pair/mob programming provides real-time review

**"What if I'm not confident in my code?"**

- PASS: Write tests first (TDD)
- PASS: Use feature flags to isolate risk
- PASS: Commit small changes, easier to verify

## Related Practices

TBD works best when combined with:

- **Continuous Integration**: [See CI/CD section in this doc]
- **Feature Flags/Toggles**: [See Feature Flags section in this doc]
- **Automated Testing**: High test coverage enables confident commits
- **Small Commits**: [Conventional Commits](./commit-messages.md)
- **Pair/Mob Programming**: Real-time collaboration and review
- **PR Merge Protocol**: [PR Merge Protocol](./pr-merge-protocol.md) - Required approval workflow, PR-Review Maker→Fixer Cycle, and done-boundary for `worktree-to-pr` PRs
- **Git Push Default Convention**: [Git Push Default Convention](./git-push-default.md) — Defines the PR-branch-as-default push target and the direct-push modes as explicit selections; governs plan-maker, plan-checker, plan-fixer, and the plan-execution workflow behavior
- **CI Post-Push Verification**: [CI Post-Push Verification Convention](./ci-post-push-verification.md) — Mandatory verification step after every push to main covering integration tests, E2E tests, and deployment workflows
- **Worktree Toolchain Initialization**: [Worktree Toolchain Initialization](./worktree-setup.md) - Mandatory two-step init (`npm install` + `npm run doctor -- --fix`) after creating or entering a worktree

## References and Further Reading

- **[TrunkBasedDevelopment.com](https://trunkbaseddevelopment.com/)** - Official TBD resource with detailed guides
- **Conventional Commits**: [Commit Message Convention](./commit-messages.md)
- **Development Practices**: [Development Index](../README.md)
