---
description: Orchestrated processes for UI component quality validation and remediation
when_to_use: Use when routing to a workflow that audits or fixes UI component quality.
---

# UI Workflows

Use these workflows when a UI component needs a repeatable quality pass. They connect source-level checks to the accessibility and consistency people notice in the product.

## Available Workflows

- [ui-quality-gate](./ui-quality-gate.md) — Runs one full UI audit, at most one fix pass, and one scoped verification over original findings and affected-component regressions. Use when auditing or fixing UI components for token compliance, accessibility, dark mode, and responsive design.

## Related Documentation

- [Frontend Development Conventions](../../development/frontend/README.md) — Standards these workflows enforce
- [Maker-Checker-Fixer Pattern](../../development/pattern/maker-checker-fixer.md) — Core workflow pattern
- [Workflows Index](../README.md) — All available workflows
