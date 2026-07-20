---
title: "API Workflows"
description: Orchestrated processes for live REST and GraphQL API quality validation and remediation
category: explanation
subcategory: workflows/api
tags:
  - index
  - workflows
  - api
  - rest
  - graphql
created: 2026-07-20
---

# API Workflows

Orchestrated multi-step processes for API quality automation against a **running** service.

## Available Workflows

| Workflow                                  | Purpose                                                                                                  | Agents Used                         | Complexity |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------- | ----------------------------------- | ---------- |
| [API Quality Gate](./api-quality-gate.md) | Exercise a live REST/GraphQL API against its contract and specs, fix findings, re-test until none remain | api-exploratory-tester, `swe-*-dev` | Medium     |

Unlike the checker/fixer gates elsewhere in this directory tree, the API gate is **tester-driven**:
`api-exploratory-tester` emits `AET-###` findings against a live endpoint, and the `swe-*-dev` agent
matching the service's implementing language applies the fixes. There is no `api-checker` or
`api-fixer` agent.

## Related Documentation

- [UI Workflows](../ui/README.md) — The static component-source counterpart to this category
- [Web Workflows](../web/README.md) — The running-UI tester triad, this category's UI-side analogue
- [PR Review Quality Gate](../pr/pr-review-quality-gate.md) — Consumes the API gate as merge precondition clause (e)
- [Manual Behavioral Verification](../../development/quality/manual-behavioral-verification.md) — Standards these workflows enforce
- [Workflows Index](../README.md) — All available workflows
