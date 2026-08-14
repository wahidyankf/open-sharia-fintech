---
title: "*-check-fix Workflow Pattern — Example Implementation and Key Differences"
description: Points to the canonical *-check-fix implementation and tabulates how it differs from a basic single-pass validation workflow.
category: explanation
subcategory: workflows
tags:
  - workflows
  - agents
  - orchestration
  - patterns
created: 2025-12-23
when_to_use: Use when comparing a proposed workflow against the *-check-fix pattern, or when looking for a canonical example to copy.
---

# \*-check-fix Workflow Pattern — Example Implementation and Key Differences

## Example Implementation

See [Repository Rules Validation Workflow](../../repo/repo-rules-quality-gate.md) for canonical implementation.

## Key Differences from Basic Validation Workflow

| Aspect             | Basic Validation Workflow        | \*-check-fix Workflow Pattern              |
| ------------------ | -------------------------------- | ------------------------------------------ |
| **Goal**           | Identify issues                  | Achieve zero findings                      |
| **Iteration**      | Single pass                      | Iterative until zero or max-limit          |
| **Findings Scope** | May focus on HIGH/MEDIUM only    | ALL findings (CRITICAL, HIGH, MEDIUM, LOW) |
| **Termination**    | After single check               | Zero findings or max-iterations            |
| **Quality Target** | Good enough (major issues fixed) | Perfect state (all issues fixed)           |
| **Human Approval** | May require checkpoints          | Fully automated                            |
| **Safety Limit**   | Not required                     | REQUIRED (max-iterations)                  |
