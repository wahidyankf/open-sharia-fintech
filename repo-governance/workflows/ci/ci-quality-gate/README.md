---
title: "CI Quality Gate Workflow"
description: "Validates all projects conform to CI/CD standards and iteratively fixes non-compliance until zero findings are confirmed twice."
when_to_use: "Read this index to find the right CI Quality Gate Workflow child document."
---

# CI Quality Gate Workflow

- [When to Use](./when-to-use.md) — The four triggers for running the CI quality gate. Use when deciding whether the CI quality gate should be run right now.
- [Execution Mode](./execution-mode.md) — Preferred and fallback execution modes for the CI quality gate. Use when starting the CI quality gate, to decide between Agent Delegation and Manual Orchestration.
- [Steps](./steps.md) — The five sequential steps of the CI quality gate's check-fix-recheck loop, from initial check through finalization. Use when executing or auditing the CI quality gate's step-by-step logic.
- [Related Workflows](./related-workflows.md) — Workflows that share the CI quality gate's iterative check-fix pattern. Use when looking for other workflows structured similarly to the CI quality gate.
- [Principles Implemented/Respected](./principles-implemented-respected.md) — The three repository principles the CI quality gate embodies. Use when explaining which platform principles the CI quality gate satisfies.
- [Conventions Implemented/Respected](./conventions-implemented-respected.md) — The governance conventions that define the standards the CI quality gate validates against. Use when tracing which conventions the CI quality gate enforces.
- [Agents](./agents.md) — The two agents the CI quality gate invokes to check and fix CI/CD compliance. Use when identifying which agent to invoke for a CI quality gate step.
