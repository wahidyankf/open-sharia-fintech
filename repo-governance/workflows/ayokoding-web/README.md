---
title: "AyoKoding Web Workflows"
description: Workflows for keeping AyoKoding learning content accurate, useful, and well structured
category: explanation
subcategory: workflows
tags: []
created: 2026-05-12
---

# AyoKoding Web Workflows

Use these workflows when AyoKoding learning content needs an independent quality pass. They connect a learning goal to checks for factual accuracy, clarity, and working links.

## Purpose

These workflows define **WHEN and HOW to validate ayokoding-web content**, orchestrating multiple agents in sequence to ensure content quality, factual accuracy, and link validity.

## Scope

**✅ Workflows Here:**

- General content quality validation (facts, links)
- By-example tutorial quality validation
- Annotated-concept tutorial quality validation (standard and leadership no-code sub-mode)
- Primer ("Just Enough X") tutorial quality validation
- Multi-agent orchestration for ayokoding-web
- Iterative check-fix-verify cycles

**❌ Not Included:**

- Single-agent operations (use agents directly)
- ose-web (has separate workflows)
- Non-workflow documentation (that's conventions/)

## Workflows

- [AyoKoding Web By-Example Quality Gate](./ayokoding-web-swe-by-example-quality-gate.md) - Validate by-example tutorial quality (95% coverage through 75-90 examples) and apply fixes iteratively until EXCELLENT status
- [AyoKoding Web Annotated-Concept Quality Gate](./ayokoding-web-annotated-concept-quality-gate.md) - Validate Annotated-concept tutorial quality (45-60 worked examples, or 20-30 scenarios for the leadership no-code sub-mode) and apply fixes iteratively until EXCELLENT status
- [AyoKoding Web Primer Quality Gate](./ayokoding-web-primer-quality-gate.md) - Validate Primer ("Just Enough X") tutorial quality (75-85 examples authored at By-Example pace, scope discipline) and apply fixes iteratively until EXCELLENT status
- [AyoKoding Web General Quality Gate](./ayokoding-web-general-quality-gate.md) - Validate all ayokoding-web content quality (factual accuracy, links), apply fixes iteratively until ZERO findings
- [AyoKoding Web In-the-Field Quality Gate](./ayokoding-web-in-the-field-quality-gate.md) - Validate in-the-field production guide quality and apply fixes iteratively until EXCELLENT status

## Related Documentation

- [Workflows Index](../README.md) - All orchestrated workflows
- [By Concept Tutorial Convention](../../conventions/tutorials/by-concept.md) - Content conventions these workflows enforce
- [By Example Tutorial Convention](../../conventions/tutorials/swe-by-example.md) - By-example standards
- [Maker-Checker-Fixer Pattern](../../development/pattern/maker-checker-fixer.md) - Core workflow pattern
