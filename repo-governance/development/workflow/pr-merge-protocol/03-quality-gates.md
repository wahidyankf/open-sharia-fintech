---
title: "Quality Gates"
description: The local and CI gates an eligible or noneligible PR must pass, the universal secret check, and the no-bypass-without-permission rule.
category: explanation
subcategory: development
tags:
  - pull-request
  - merge
  - quality-gates
  - workflow
  - merge-preconditions
created: 2026-04-04
when_to_use: Use when confirming which gates a PR must pass before merge, or when a secret exposure is suspected in a PR diff.
---

# Quality Gates

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

## Universal Secret Check

Before merging either route, inspect the PR diff and review evidence for a suspected secret exposure.
If one exists, stop normal merge handling, contain and rotate the credential, then follow the full
reachable-ref history-rewrite and replacement-PR procedure in
[Secrets and Environment Standards](../../../conventions/security/secrets-and-env-standards.md). A
green quality gate, a noneligible classifier result, or a resolved review thread never authorizes
merging a contaminated PR.

## No Bypass Without Explicit Permission

Bypassing any quality gate without explicit user permission is **forbidden**. This includes:

- Merging with failing CI checks
- Merging with unresolved review comments (unless the user explicitly dismisses them)
- Using admin override to bypass branch protection rules
- Merging with pending required status checks

If the user explicitly says "merge despite the failing lint check" (or equivalent), the agent may proceed -- but only for that specific instance and only for the specific gates the user named.
