---
title: "Motivating Example"
description: "The incident that motivated the six forcing-functions."
category: explanation
subcategory: development
tags:
  - testing
  - live-testing
  - usability
  - ux
  - quality
  - systematic
created: 2026-06-22
when_to_use: "Use when you need the rationale behind these forcing-functions."
---

# Motivating Example

The cost-of-living calculator work illustrates each forcing-function in the negative:

- The shared-control x surface matrix was not built, so the city filter's no-op on the savings
  tab was never observed (FF1).
- The URL round-trip was not verified for every input, so the reload-discards-state defect was
  not found (FF2).
- The "URL is the single source of truth" source comment was never extracted as an invariant to
  check, so its violations went undetected (FF3).
- The cross-surface styling matrix was not built, so raw native elements coexisting with
  design-system components were not flagged (FF4).
- The jargon scan and hidden-control probe were run selectively rather than exhaustively (FF5).
- Prior defect classes were not carried forward as mandatory re-checks in later rounds (FF6).

Applying all six forcing-functions on the first run would have surfaced all of these findings.
