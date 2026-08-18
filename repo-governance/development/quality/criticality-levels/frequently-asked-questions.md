---
title: "Frequently Asked Questions"
description: "FAQ about the criticality-level system."
category: explanation
subcategory: development
tags:
  - criticality
  - validation
  - checker-agents
  - fixer-agents
  - quality-assurance
created: 2025-12-27
when_to_use: "Use for a quick answer about this system."
---

# Frequently Asked Questions

## Why four levels instead of three?

Three levels (Critical/Important/Minor) don't distinguish between "should fix soon" (HIGH) and "nice to have" (MEDIUM). Four levels provide clearer prioritization without overwhelming users.

## Why keep dual labels for some agents?

Verification status ([Verified]/[Error]) and link status ([OK]/[BROKEN]) serve different purposes than criticality. Example: `[Error] - HIGH` means "verified incorrect AND important to fix." Both dimensions provide valuable information.

## Can criticality and confidence ever contradict?

No - they measure different things. Criticality = importance, confidence = certainty. Example: CRITICAL + MEDIUM confidence means "very important issue but we're uncertain about the exact fix" → urgent manual review.

## What if an agent finds no CRITICAL/HIGH issues?

Report status: PASS or PASS WITH WARNINGS. MEDIUM/LOW issues don't block publication.

## Should all findings be auto-fixed?

No - only HIGH confidence findings. MEDIUM confidence requires manual review (too risky to auto-fix).

## How does this affect existing workflows?

Checkers generate reports with new sections. Fixers process findings in priority order. Users see clearer categorization. Core workflow unchanged.

## What about backward compatibility?

Fixers must handle both old and new report formats. Legacy severity terms (Critical/Important/Minor) map to new criticality levels (CRITICAL/HIGH/MEDIUM).

---
