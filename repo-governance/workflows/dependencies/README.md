---
description: Workflows for dependency inventory, security and compatibility clearance, and upgrade planning
when_to_use: Use when routing to a workflow that surveys or plans dependency changes across the monorepo.
---

# Dependency Workflows

Use these workflows when dependency changes need repository-wide inventory, security research,
compatibility clearance, or coordinated upgrade planning.

## Available Workflows

- [dependency-bump-planning](dependency-bump-planning.md) — Surveys dependency manifests across
  the monorepo, classifies candidate bumps under the dependency policy, and produces a validated
  backlog plan without modifying manifests or lockfiles.
