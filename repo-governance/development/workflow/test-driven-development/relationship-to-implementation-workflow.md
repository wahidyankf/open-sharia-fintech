---
title: "Relationship to Implementation Workflow"
description: How TDD's Red-Green-Refactor loop maps onto the Implementation Workflow's three stages, without adding a fourth stage.
category: explanation
subcategory: development
tags:
  - development
  - workflow
  - tdd
  - testing
  - red-green-refactor
created: 2026-05-02
when_to_use: Use when explaining how TDD and the three-stage Implementation Workflow fit together.
---

# Relationship to Implementation Workflow

TDD and the
[Implementation Workflow Convention](../implementation.md) are complementary, not competing:

| Implementation Stage    | TDD Role                                                                 |
| ----------------------- | ------------------------------------------------------------------------ |
| Make it work (Stage 1)  | Red→Green: write failing test, then minimum passing code                 |
| Make it right (Stage 2) | Refactor with tests green; add tests for edge cases found during cleanup |
| Make it fast (Stage 3)  | Optimize with tests green; add performance assertions if needed          |

TDD does not add a fourth stage. It is the mechanism that makes each stage of the Implementation
Workflow verifiable and safe.
