---
title: "UI Quality Gate Workflow"
description: "Validates UI component quality against frontend conventions and applies fixes iteratively until zero findings are confirmed twice."
when_to_use: "Read this index to find the right UI Quality Gate Workflow child document."
---

# UI Quality Gate Workflow

- [Execution Mode](./01-execution-mode.md) — Preferred and fallback execution modes for the UI quality gate, and example invocations. Use when starting the UI quality gate, to decide between Agent Delegation and Manual Orchestration.
- [Steps](./02-steps.md) — The six sequential steps of the UI quality gate's check-fix-recheck loop, from initial validation through finalization. Use when executing or auditing the UI quality gate's step-by-step logic.
- [Safety Features](./03-safety-features.md) — The four safeguards that keep the UI quality gate's check-fix loop bounded and reliable. Use when explaining what protects the UI quality gate from infinite loops or regressions.
- [Example Usage](./04-example-usage.md) — A worked transcript of the UI quality gate running end to end in strict mode. Use when you want to see what a UI quality gate run looks like in practice.
- [Related Documentation](./05-related-documentation.md) — Cross-references from the UI quality gate to its checker, fixer, and maker agents, and to frontend conventions. Use when looking for documentation related to the UI quality gate.
