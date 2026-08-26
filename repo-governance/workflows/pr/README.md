---
title: "PR Review Workflows"
description: Orchestrated workflows for reviewing and finishing off pull requests before merge
when_to_use: Use when routing to a workflow that runs the specialist review cycle against an open pull request.
category: explanation
subcategory: workflows
tags:
  - index
  - workflows
  - pr
  - review
created: 2026-08-14
---

# PR Review Workflows

Use these workflows when a pull request needs a structured specialist review before it merges. They classify the PR, run the appropriate review depth, and drive every thread to resolution.

## Available Workflows

- [pr-review-quality-gate](./pr-review-quality-gate.md) — Classify every PR by changed-artifact
  behavior; eligible PRs target 1–3 cycles, use 4–5 for focused recovery, and allow later ordinals
  only within an authenticated per-PR configured-ceiling extension. Use before merge to decide the
  route and preserve a readable audit.

## Related Documentation

- [API Workflows](../api/README.md) — The API gate the pr-review-quality-gate consumes as a merge precondition
- [Maker-Checker-Fixer Pattern](../../development/pattern/maker-checker-fixer.md) — Core workflow pattern
- [Workflows Index](../README.md) — All available workflows
