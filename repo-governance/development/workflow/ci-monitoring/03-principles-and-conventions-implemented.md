---
title: "Principles and Conventions Implemented"
description: The principles and companion conventions that safe CI monitoring respects.
category: explanation
subcategory: development
tags:
  - ci
  - github-actions
  - rate-limiting
  - monitoring
  - workflow
when_to_use: Use when tracing why this convention's monitoring rules exist back to the principles and conventions they respect.
---

# Principles and Conventions Implemented

## Principles Implemented/Respected

This convention implements the following core principles:

- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**: The required default approach for monitoring CI runs is `ScheduleWakeup` every 2 minutes (2-5 minutes acceptable) with a single `gh run view --json status,conclusion` check per wakeup — this replaces error-prone manual polling without exhausting the API rate limit. Stream-watching via `gh run watch` is prohibited for CI monitoring.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: `ScheduleWakeup` + a single `gh run view --json status,conclusion` is simpler than a while-loop, a sleep, a JSON parser, and retry logic. A scheduled wakeup removes code that must be written, debugged, and maintained — and avoids the rate limit hazard that stream-watching via `gh run watch` introduces on jobs longer than 5 minutes.

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Rate limit budget is a finite, shared resource. This convention makes its constraints explicit — quota size, window duration, recovery delay — so agents and developers can reason about impact before issuing commands rather than discovering exhaustion after the fact.

- **[Reproducibility First](../../../principles/software-engineering/reproducibility.md)**: A plan execution that burns the API rate limit mid-run is non-reproducible: repeating the same sequence on the same codebase produces a different outcome depending on how many prior API calls were made. Safe monitoring practices make CI verification a reliable, repeatable step.

## Conventions Implemented/Respected

This convention implements/respects the following development practices:

- **[CI Post-Push Verification Convention](../ci-post-push-verification.md)**: That convention mandates triggering and monitoring CI after every push. This convention specifies HOW to perform that monitoring safely — `ScheduleWakeup` every 2 minutes (default) as the required approach for standard CI jobs, `gh run watch` prohibited for CI monitoring, minimum 2-minute sleep if a manual poll loop is unavoidable, and recovery procedures when rate-limited.

- **[CI Blocker Resolution Convention](../../quality/ci-blocker-resolution.md)**: When a rate limit prevents CI verification, it is a blocker. This convention provides the correct recovery path (scheduled wakeup, not retry loop) rather than treating a 403 as a transient error and spinning.
