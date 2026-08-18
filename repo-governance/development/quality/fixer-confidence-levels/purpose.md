---
title: "Purpose"
description: "Why this convention exists."
category: explanation
subcategory: development
tags:
  - fixer-agents
  - confidence-levels
  - validation
  - automation
  - quality-assurance
created: 2025-12-14
when_to_use: "Use when orienting to why fixer confidence levels exist."
---

# Purpose

Confidence levels serve multiple critical purposes:

## 1. Automated Fixing Safety

**Problem:** Checkers sometimes flag legitimate content as violations or suggest inappropriate fixes.

**Solution:** Re-validate findings and apply fixes only when confidence is HIGH.

**Benefit:** Prevents automated tools from making inappropriate changes.

## 2. Human Judgment Recognition

**Problem:** Many quality issues are subjective and context-dependent (narrative flow, tone, engagement, word choice).

**Solution:** Flag subjective improvements as MEDIUM confidence requiring manual review.

**Benefit:** Respects the human element in quality assessment while automating objective fixes.

## 3. Checker Quality Improvement

**Problem:** Checkers can have detection logic flaws that produce false positives.

**Solution:** Identify false positives through re-validation and report them with suggested improvements.

**Benefit:** Creates feedback loop that continuously improves checker accuracy.

## 4. Audit Trail and Transparency

**Problem:** Users need to understand what was fixed, what was skipped, and why.

**Solution:** Document all confidence assessments in fix reports with detailed reasoning.

**Benefit:** Builds trust and provides clear path for manual review.
