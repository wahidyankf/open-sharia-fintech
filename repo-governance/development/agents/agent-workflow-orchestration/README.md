---
title: "Agent Workflow Orchestration Convention"
description: "Standards for how AI agents plan, execute, verify, and self-improve during multi-step tasks"
when_to_use: "Read this index to find the right Agent Workflow Orchestration Convention child document."
---

# Agent Workflow Orchestration Convention

- [Principles Implemented/Respected](./01-principles-implemented-respected.md) — Lists the core repository principles this convention implements and respects. Use when checking which principles justify a rule in the Agent Workflow Orchestration Convention.
- [Conventions Implemented/Respected](./02-conventions-implemented-respected.md) — Lists the related repository conventions this convention implements and respects. Use when checking which sibling conventions govern agent workflow orchestration.
- [When to Plan](./03-when-to-plan.md) — Defines when an agent should produce an explicit plan before acting, the plan format, and how to re-plan when things go wrong. Use when deciding whether a task needs an upfront plan before execution starts.
- [Delegated Agent Strategy](./04-delegated-agent-strategy.md) — Defines when to use delegated (sub)agents, the rules for delegating, and when not to delegate. Use when deciding whether to hand a piece of work off to a delegated agent.
- [Operating Budgets — Authoring and Propagating Repository Rules](./05-operating-budgets-authoring-repository-rules.md) — Covers the operating-budget rule for authoring and propagating repository-wide rule changes. Use when a rule change needs to be authored and propagated across the repository.
- [Operating Budgets — Parallelism Budget](./06-operating-budgets-parallelism-budget.md) — Defines the parallelism budget for how many concurrent work streams an orchestrating agent may run. Use when deciding how many parallel work streams to run at once.
- [Operating Budgets — DAG-First Orchestration and Background-Slot Preference](./07-operating-budgets-dag-first-and-background-slot.md) — Covers DAG-first orchestration and the preference for background slots over serial execution. Use when sequencing dependent work or deciding whether to run a task in the background.
- [Operating Budgets — Harness Capability Gating](./08-operating-budgets-harness-capability-gating.md) — Defines how orchestration behavior is gated by the current harness's capabilities. Use when an orchestration behavior depends on whether the current harness supports it.
- [Operating Budgets — The PR Is the Independent Merge Point](./09-operating-budgets-pr-independent-merge-point.md) — Explains why worktree-to-pr isolates edits and why every DAG leaf that produces changes gets its own branch and PR. Use when deciding whether two pieces of concurrent work need separate worktrees and PRs.
- [Operating Budgets — The PR Is the Independent Merge Point (Continued)](./10-operating-budgets-pr-independent-merge-point-continued.md) — Continues the independent-merge-point rule: why the worktree is a per-repository unit rather than a per-PR unit. Use when reasoning about worktree scope relative to a repository versus a single PR.
- [Operating Budgets — CI and GitHub Actions Monitoring Cadence](./11-operating-budgets-ci-monitoring-cadence.md) — Defines the cadence for monitoring CI and GitHub Actions while an orchestrated task runs. Use when deciding how often to poll CI status during an orchestrated multi-step task.
- [Verification Before Done](./12-verification-before-done.md) — Defines the verification requirements before marking a task done, for different task types, and how to compare diffs and behavior. Use before reporting any task complete, to confirm what still needs verifying.
- [Autonomous Bug Fixing](./13-autonomous-bug-fixing.md) — Defines the expected behavior for autonomous bug fixing, what autonomous means, handling failing CI tests, and preexisting errors found during other work. Use when an agent discovers a bug or a failing test while doing unrelated work and must decide whether to fix it autonomously.
- [Demand Elegance (Balanced)](./14-demand-elegance-balanced.md) — States the balanced standard for code elegance an agent should hold itself to. Use when deciding how much polish a change needs before it is considered done.
- [Self-Improvement Loop](./15-self-improvement-loop.md) — Defines the self-improvement process, the lessons file format, and what makes a good lesson. Use when an agent wants to record a lesson learned from a mistake or a surprising result.
- [Task Management](./16-task-management.md) — Covers planning first, tracking progress, granular task items, using the Task tool for multi-step work, documenting results, and capturing lessons. Use when managing the task list for a multi-step piece of work.
- [Anti-Patterns](./17-anti-patterns.md) — Lists orchestration anti-patterns: pushing through when lost, premature completion, context bloat, and vague lessons. Use when reviewing an agent's workflow for common orchestration mistakes.
- [References](./18-references.md) — Links to related conventions and workflows referenced throughout this convention. Use when looking for further reading on agent workflow orchestration.
