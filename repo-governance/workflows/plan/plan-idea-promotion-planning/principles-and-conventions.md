---
description: The four general/software-engineering principles and six repo conventions this workflow implements.
when_to_use: Use when checking which cross-cutting principles or repo-governance conventions govern a specific rule in this workflow.
---

# Principles and Conventions Implemented/Respected

## Principles Implemented/Respected

- **[Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md)**: The ripeness gate and the deep prior-art study precede any plan; the checkpoint forces an explicit go/no-go.
- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Ripeness verdict, prior-art findings, and the promotion decision are recorded in writing before the plan is authored.
- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: The workflow composes existing pieces (`web-researcher`, `plan-planning`) rather than duplicating plan-authoring; the user is grilled once.
- **[No Time Estimates](../../../principles/content/no-time-estimates.md)**: Outcomes, not durations.

## Conventions Implemented/Respected

- **[Plans Organization Convention](../../../conventions/structure/plans.md)**: The backlog plan uses the `<identifier>/` folder form (no date prefix); the two-pager is deleted and de-indexed on promotion.
- **[Web Research Delegation Convention](../../../conventions/writing/web-research-delegation.md)**: The deep prior-art study is delegated to `web-researcher`.
- **[Subagent Orchestration Convention](../../../development/agents/subagent-orchestration.md)**: Research angles fan out under the N+1 model — `1 main thread + N background agents = N+1 total`, default N=3 — with the main thread kept vacant as orchestrator.
- **[Grilling-With-Options Convention](../../../development/workflow/grilling-with-options.md)**: The promotion checkpoint presents concrete options; open-ended questions are forbidden.
- **[Linking Convention](../../../conventions/formatting/linking.md)**: Cross-references use GitHub-compatible markdown with `.md` extensions.
