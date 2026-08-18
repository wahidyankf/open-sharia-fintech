---
title: "Purpose and Scope"
description: Why this convention exists, its target audience, and exactly what it covers versus what it defers to companion conventions.
category: explanation
subcategory: development
tags:
  - ci
  - github-actions
  - rate-limiting
  - monitoring
  - workflow
when_to_use: Use when checking whether a CI-monitoring question is in scope for this convention or belongs to a companion convention instead.
---

# Purpose and Scope

This convention exists to prevent GitHub API rate limit exhaustion during CI monitoring in plan execution and manual development workflows. The rate limit is a shared resource across all authenticated `gh` commands in the same hour window. Burning it on tight-poll loops blocks the entire toolchain — not just CI monitoring — for up to an hour.

The target audience is any agent or developer performing the post-push CI verification step described in the [CI Post-Push Verification Convention](../ci-post-push-verification.md).

## What This Convention Covers

- Correct tool selection for watching CI runs to completion
- Minimum poll intervals when manual polling is unavoidable
- Trigger discipline to avoid redundant concurrent runs
- Rate limit budget facts and window behavior
- Recovery procedure when rate-limited (HTTP 403 from `gh`)
- Runner/action contention across the shared, limited OSE runner pools (free hosted + self-hosted) and the wait-and-check response
- Retriggering a genuinely stuck run (no contention) via rebase-and-push
- Application of these rules in plan execution (Step 2c of `plan-execution.md`)

## What This Convention Does NOT Cover

- Which workflows to trigger after a push (see [CI Post-Push Verification Convention](../ci-post-push-verification.md))
- How to investigate and fix a failed CI run (see [CI Blocker Resolution Convention](../../quality/ci-blocker-resolution.md))
- GitHub Actions workflow authoring standards (see [CI/CD Conventions](../../infra/ci-conventions.md))
