---
title: "Governance Word-Budget Convention — Vision and Principles"
description: Vision alignment, principles implemented, and related conventions for the governance word-budget gate.
when_to_use: Use when you need the rationale (vision/principles) behind the word-budget convention, or its list of related conventions.
category: explanation
subcategory: conventions
tags:
  - instruction-files
  - agents-md
  - word-budget
  - governance
  - rhino-cli
created: 2026-06-27
---

# Governance Word-Budget Convention — Vision and Principles

## Vision Supported

This convention serves the [Open Sharia Enterprise Vision](../../../vision/open-sharia-enterprise.md)
by ensuring governance rules embedded in instruction files stay reliably loaded, not silently
dropped past a harness limit.

## Principles Implemented/Respected

- **[Progressive Disclosure](../../../principles/content/progressive-disclosure.md)**: the sole
  sanctioned remediation for word-budget violations.
- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**:
  thresholds are declared explicitly in `repo-config.yml`, not embedded in the validator binary.
- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**:
  every enforcement point is automated.
- **[Reproducibility First](../../../principles/software-engineering/reproducibility.md)**: the word
  count is deterministic.

## Related Conventions

- [Governance Word-Budget Remediation](../governance-word-budget-remediation.md) — enforcement
  points, the progressive-disclosure fix, and forbidden anti-fixes
- [Deterministic vs AI Validation Split](../deterministic-vs-ai-validation-split.md)
- [Governance Vendor-Independence Convention](../governance-vendor-independence.md)
- [Multi-Harness Binding Convention](../multi-harness-binding.md)
