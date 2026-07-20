---
title: "Workflow Development"
description: "Development workflow conventions governing how contributors and agents execute work — TDD, commits, branching, environment reproducibility, grilling, and CI."
category: explanation
subcategory: development
tags: []
created: 2026-05-12
---

# Workflow Development

Development workflow standards covering implementation methodology, git workflows, commit messages, and reproducible environments.

## Purpose

These standards define **HOW to execute development workflows**, covering the three-stage implementation workflow (make it work, make it right, make it fast), Trunk Based Development for git, Conventional Commits for messages, and reproducible environment practices.

## Scope

**✅ Belongs Here:**

- Development workflow methodologies
- Git workflow standards (TBD, commits)
- Implementation progression (work → right → fast)
- Environment reproducibility practices
- Development process standards

**❌ Does NOT Belong:**

- Why we automate workflows (that's a principle)
- Multi-agent orchestration (that's workflows/)
- Code quality tools (that's quality/)

## Documents

- [Commit Message Convention](./commit-messages.md) - Understanding Conventional Commits, commit granularity, and why we use them
- [Implementation Workflow Convention](./implementation.md) - Three-stage development workflow: make it work, make it right, make it fast. Includes surgical changes (touch only what you must) and goal-driven execution (define success criteria, loop until verified)
- [Reproducible Environments Convention](./reproducible-environments.md) - Practices for creating consistent, reproducible development and build environments
- [Trunk Based Development Convention](./trunk-based-development.md) - Git workflow using Trunk Based Development for continuous integration
- [Worktree Toolchain Initialization](./worktree-setup.md) - Mandatory two-step init (`npm install` then `npm run doctor -- --fix`) in the root repository worktree after creating or entering a git worktree. The first step keeps `node_modules/` consistent with `package-lock.json`; the second actively converges the polyglot toolchains (Rust, .NET/F#, TypeScript/Node) managed by `rhino-cli doctor` — required because `package.json`'s `postinstall` hook swallows doctor failures with `|| true`
- [Git Push Default Convention](./git-push-default.md) - Default push behavior: the repo-wide default integration target is a PR branch opened against `main` (`worktree-to-pr`); the direct-push modes remain fully available where a plan declares them. Covers linear history requirement (rebase before push), proactive retroactive compliance, worktree execution, and agent responsibilities — the push itself is always `[AI]` in every mode, and no "review the diff and approve push" gate belongs in a delivery checklist, since pushing to a PR branch is not a merge
- [CI Post-Push Verification Convention](./ci-post-push-verification.md) - After pushing app or lib code — to a PR branch under the default `worktree-to-pr`, or to `origin main` under the direct-push modes — manually trigger all related GitHub CI workflows and verify they pass before declaring work done. Maps changed apps to their workflow files, covers the gap between what the pre-push hook validates (typecheck, lint, test:quick) and what only CI covers (integration tests, E2E tests, deployment workflows)
- [Git Push Safety Convention](./git-push-safety.md) - Requires explicit per-instance user approval before any AI agent or automation executes `git push --force`, `--force-with-lease`, or `--no-verify`; prior approval does not carry forward
- [No Destructive Git Operations Convention](./no-destructive-git-operations.md) - The local-side companion to Git Push Safety, forbidding operations that discard a concurrent actor's uncommitted work on the shared machine (hard reset, recursive clean, `branch -D`, unconditional stash removal, immediate reflog expiry plus object pruning, forced worktree removal, `rm -rf` of a worktree) and prescribing the non-destructive equivalent for each. Also carries the whole-tree-staging prohibition stated as a shape rather than one flag spelling, and the no-corner-cutting rule binding root-cause orientation to failing gates
- [Worktree and Artifact Cleanup Convention](./worktree-and-artifact-cleanup.md) - The teardown sibling of Worktree Toolchain Initialization, making plan-end cleanup a mandatory gate across three artifact classes (worktrees, branches local and remote, build output). Specifies five pre-removal checks — merge state via `gh pr list` rather than ancestry (squash-merge makes ancestry tests report NOT-MERGED for every merged branch), the worktree's dirty diff, unpushed commits, non-force removal, and never removing a worktree you did not create — plus the shared-cache carve-out that keeps the shared cargo `target/` intact
- [Git Hook Lifecycle](./git-hook-lifecycle.md) - Canonical reference for the three Husky git hooks — commit-msg, pre-commit, and pre-push — their step order, failure modes, and relationship to CI
- [PR Merge Protocol](./pr-merge-protocol.md) - Gates every PR merge on five hardened preconditions (review cycles complete, no CRITICAL/HIGH outstanding, branch non-destructively up to date with `origin/main`, all quality gates green, tester gates run or exemption recorded) rather than a per-instance prompt. `[AI]` merges once they hold; a `[HUMAN]` merge gate is an explicit per-plan opt-in with identical preconditions. Bypassing a quality gate still requires explicit user permission, per instance
- [Dependency Bump Stability & Safety Policy](./dependency-bump-policy.md) - Three-path decision tree (LTS, 60-day soak, security waiver) governing every dependency bump across the polyglot monorepo. Mandates exact pinning, CVE clearance via five sources (NVD, GitHub Security Advisories, Snyk DB, project security page, CISA KEV feed), KEV Fast-Track (confirmed-exploited CVEs bypass 60-day soak), EPSS Escalation (score ≥ 0.5 triggers Path C urgency), cutoff-date computation in writing, selecting the most recent eligible version, rejecting versions with known fatal functional defects (yanked / release-blocker), and waiver documentation in `tech-docs.md` for Path C overrides
- [Native-First Toolchain Management](./native-first-toolchain.md) - Architectural decision to use native package managers and `rhino-cli doctor` instead of Terraform, Ansible, or Docker Dev Containers for development environment setup
- [Test-Driven Development Convention](./test-driven-development.md) - Mandates TDD (Red→Green→Refactor) as the required practice for all code changes; defines TDD across all test levels (unit, integration, E2E), the TDD Shape for Delivery Checklists (explicit RED/GREEN/REFACTOR three-substep template with file path, verbatim command, and acceptance criterion per substep), plan-checker enforcement of TDD-shaped delivery checklist items, and the chain from Gherkin acceptance criteria to first failing test
- [CI Monitoring Convention](./ci-monitoring.md) - Standards for monitoring GitHub Actions CI runs without exhausting the GitHub API rate limit — required tooling, poll intervals, trigger discipline, and recovery procedures
- [Git Identity From Global Config Convention](./git-identity-from-global-config.md) - Prohibits `[user]` overrides in any subrepo's `.git/config`; git author identity must come exclusively from the developer's global `~/.gitconfig`. Enforced by `scripts/git-identity-check.sh` invoked as the first step of the Husky pre-commit hook
- [Grilling-With-Options Convention](./grilling-with-options.md) - Every grill question (in plan creation, plan establishment, and plan execution contexts) MUST present 2-4 concrete options with trade-off descriptions; open-ended questions without options are FORBIDDEN; interactive multiple-choice UI preferred when the coding agent supports it; one option marked as recommended

## Companion Documents

- [Anti-Patterns](./anti-patterns.md) - Common workflow mistakes to avoid (with examples and corrections)
- [Best Practices](./best-practices.md) - Recommended workflow patterns and techniques

## Related Documentation

- [Development Index](../README.md) - All development practices
- [Simplicity Over Complexity Principle](../../principles/general/simplicity-over-complexity.md) - Why we start simple
- [Reproducibility First Principle](../../principles/software-engineering/reproducibility.md) - Why environments matter
- [Repository Architecture](../../repository-governance-architecture.md) - Six-layer governance model

## Principles Implemented/Respected

This set of development practices implements/respects the following core principles:

- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: Trunk Based Development and Implementation Workflow start simple, avoiding over-engineering with complex branching or premature optimization.

- **[Reproducibility First](../../principles/software-engineering/reproducibility.md)**: Reproducible environments convention ensures consistent development and build environments across machines and team members.

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: Runtime versions pinned explicitly (Volta), required setup steps codified as deliberate actions rather than assumed side effects.

- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)**: Automated CI triggers on every commit, automated environment setup through version managers, and codified worktree procedures replace manual, error-prone steps.

## Conventions Implemented/Respected

This set of development practices respects the following conventions:

- **[Commit Message Convention](./commit-messages.md)**: Conventional Commits format provides explicit commit metadata for automated changelog generation and version control.

- **[Nested Code Fences Convention](../../conventions/formatting/nested-code-fences.md)**: Workflow documentation uses proper code fence nesting when documenting markdown structure and patterns.
