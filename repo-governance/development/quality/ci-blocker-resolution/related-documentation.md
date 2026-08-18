---
title: "Related Documentation"
description: "Related quality-gate and debugging conventions."
category: explanation
subcategory: development
tags:
  - ci
  - quality-gates
  - root-cause
  - debugging
  - anti-pattern
  - preexisting-issues
created: 2026-04-04
when_to_use: "Use when you need a related convention on quality gates."
---

# Related Documentation

- [CI Monitoring Convention](../../workflow/ci-monitoring.md) -- Safe CI / GitHub Actions monitoring cadence: never poll faster than once every two minutes (2-minute operational default)
- [Code Quality Convention](.././code.md) -- Quality gates that this convention protects
- [Git Push Safety Convention](../../workflow/git-push-safety.md) -- Per-instance approval for `--no-verify`
- [Trunk Based Development Convention](../../workflow/trunk-based-development.md) -- Main must always be releasable
- [Root Cause Orientation Principle](../../../principles/general/root-cause-orientation.md) -- The foundational principle this convention implements
- [Commit Message Convention](../../workflow/commit-messages.md) -- Conventional commit format for preexisting fixes
- [Nx Target Standards](../infra/nx-targets.md) -- Canonical target names for quality gates
