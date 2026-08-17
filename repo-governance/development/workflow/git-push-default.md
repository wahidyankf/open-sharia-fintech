---
title: "Git Push Default Convention"
description: Default git push behavior — every plan uses worktree-to-pr; direct push to origin main is unavailable or restricted per-repo.
category: explanation
subcategory: development
tags:
  - git
  - workflow
  - push
  - trunk-based-development
  - ai-agents
created: 2026-04-25
when_to_use: Use before pushing anything, or when a plan needs to override the worktree-to-pr default.
---

# Git Push Default Convention

The repo-wide default integration target for every push is a **PR branch opened against `main`**
(the `worktree-to-pr` delivery mode). Direct push to `origin main` has **no executable path at all
in `ose-public`** — `main` is branch-protected against direct pushes for every
actor, including admins. In `ose-private`, the direct-push modes remain available only for an
explicitly selected infrastructure-as-code plan; `main-to-origin-main` further requires an
`.md`-only change set or explicit user go-ahead (Standard 2). This applies to general work and
every plan-lifecycle context. The canonical four-mode vocabulary and three-tier precedence live in
the
[Plans Organization Convention — Delivery Mode](../../conventions/structure/plans/32-delivery-mode-the-four-modes.md#delivery-mode);
this convention governs the push mechanics for each mode.

## Contents

- [Principles and Conventions Implemented](./git-push-default/01-principles-and-conventions-implemented.md) — Why this convention exists.
- [Scope](./git-push-default/02-scope.md) — What is and is not covered.
- [Standard 1: Default Integration Target Is a PR Branch](./git-push-default/03-standard-1-default-integration-target-is-a-pr-branch.md) — The worktree-to-pr default and the Phase 0 exception.
- [Standard 2: Direct Push Modes Are Explicit Selections, Not Inferred — and Are Repo-Restricted](./git-push-default/04-standard-2-direct-push-modes-are-explicit-selections-not-inferred-and-are-repo-restricted.md) — Per-repository availability and selection signals.
- [Standard 3: Plans Must Declare a Delivery Mode Only to Override the Default](./git-push-default/05-standard-3-plans-must-declare-a-delivery-mode-only-to-override-the-default.md) — plan-maker/checker/fixer responsibilities.
- [Standard 4: Maintain Linear History Before Pushing](./git-push-default/06-standard-4-maintain-linear-history-before-pushing.md) — Rebase, never merge commit.
- [Standard 5: Proactively Fix Delivery-Mode Mismatches](./git-push-default/07-standard-5-proactively-fix-delivery-mode-mismatches.md) — Fix now, don't defer.
- [Standard 6: Worktree Execution Does Not Determine the Mode by Itself](./git-push-default/08-standard-6-worktree-execution-does-not-determine-the-mode-by-itself.md) — Work location and integration target are independent axes.
- [Examples — Default and Direct-Push Selection](./git-push-default/09-examples-default-and-direct-push-selection.md) — PASS/FAIL for the base flow and an explicit override.
- [Examples — Plan-Maker Delivery-Mode Tagging](./git-push-default/10-examples-plan-maker-delivery-mode-tagging.md) — FAIL/PASS for `[AI]`/`[HUMAN]` tagging.
- [Examples — Linear History and Proactive Fixes](./git-push-default/11-examples-linear-history-and-proactive-fixes.md) — PASS/FAIL for rebasing and a fixed mismatch.
- [Agent Responsibilities](./git-push-default/12-agent-responsibilities.md) — Per-agent responsibility table.

## Related Documentation

- [Trunk Based Development Convention](../workflow/trunk-based-development.md) — `main` as the trunk.
- [Git Push Safety Convention](../workflow/git-push-safety.md) — Force-push and `--no-verify` approval.
- [PR Merge Protocol Convention](../workflow/pr-merge-protocol.md) — The review cycle and done-definition.
- [CI Post-Push Verification Convention](../workflow/ci-post-push-verification.md) — Post-push CI checks.
- [Proactive Preexisting Error Resolution](../practice/proactive-preexisting-error-resolution.md) — Fixing discovered violations.
