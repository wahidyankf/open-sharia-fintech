---
description: Workflows for checking that reader-facing documentation remains accurate and navigable
when_to_use: Use when routing to a workflow that validates docs/ content quality or its style-guide separation.
---

# Documentation Workflows

Use these workflows when reader-facing documentation needs a systematic quality pass. They help keep tutorials, explanations, and reference pages accurate, learnable, and connected.

## Purpose

These workflows define **WHEN and HOW to validate documentation**, orchestrating multiple checker and fixer agents in sequence to ensure factual accuracy, pedagogical structure, and link validity across all docs/ content.

## Scope

**✅ Workflows Here:**

- Documentation quality validation
- Tutorial quality validation
- Link validity checking
- Multi-agent orchestration for docs/
- Iterative check-fix-verify cycles

**❌ Not Included:**

- ayokoding-web content validation (that's ayokoding-web/)
- README validation (that's separate workflow)
- Single-agent operations (use agents directly)

## Workflows

- [docs-quality-gate](./docs-quality-gate.md) — Validates all docs/ content (factual accuracy, pedagogical structure, link validity) and applies fixes iteratively via Maker-Checker-Fixer. Use after creating/updating documentation, before releases, periodically, or after bulk restructuring.
- [docs-software-engineering-separation-quality-gate](./docs-software-engineering-separation-quality-gate.md) — Validates separation between OSE Platform style guides and AyoKoding educational content, then fixes violations iteratively. Use after adding/updating prerequisite relationships or style-guide/AyoKoding content, or periodically for compliance.

## Related Documentation

- [Workflows Index](../README.md) - All orchestrated workflows
- [Content Quality Principles](../../conventions/writing/quality.md) - Quality standards these workflows enforce
- [Tutorial Convention](../../conventions/tutorials/general.md) - Tutorial standards
- [Maker-Checker-Fixer Pattern](../../development/pattern/maker-checker-fixer.md) - Core workflow pattern
