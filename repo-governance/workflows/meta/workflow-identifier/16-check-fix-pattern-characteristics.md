---
title: "*-check-fix Workflow Pattern — Pattern Characteristics"
description: Introduces the *-check-fix pattern that achieves perfect quality by fixing ALL findings and iterating to zero, and lists when to use it and its key differentiators.
category: explanation
subcategory: workflows
tags:
  - workflows
  - agents
  - orchestration
  - patterns
created: 2025-12-23
when_to_use: Use when deciding whether a new quality-gate workflow should follow the *-check-fix pattern.
---

# \*-check-fix Workflow Pattern — Pattern Characteristics

A specialized workflow pattern that achieves **perfect quality state** by fixing ALL findings (CRITICAL, HIGH, MEDIUM, LOW criticality levels) and iterating until ZERO findings remain.

**Purpose**: Achieve zero findings across all confidence levels, not "good enough" state.

**When to use**:

- Repository-wide validation (repo-rules-quality-gate)
- Content quality assurance (plan-quality-gate, ayokoding-web-content-quality-gate)
- Pre-release quality gates
- Periodic health checks

**Key Differentiators**:

1. **ALL findings count** - Not just CRITICAL or HIGH criticality, includes MEDIUM and LOW (style, formatting)
2. **Zero findings goal** - Terminates with SUCCESS only when zero findings of any level
3. **Iterative fixing** - Continues check-fix cycles until perfect state or max-iterations
4. **Perfect quality state** - Achieves comprehensive quality, not minimal compliance
