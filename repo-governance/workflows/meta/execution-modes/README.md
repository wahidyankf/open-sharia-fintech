---
title: "Workflow Execution Mode Convention"
description: "Defines execution modes for workflows — Agent Delegation (preferred) and Manual Orchestration (fallback) — explaining how to use the Agent tool for delegated agent invocation and when to fall back to direct execution"
when_to_use: "Read this index to find the right Workflow Execution Mode Convention child document."
---

# Workflow Execution Mode Convention

- [Overview](./overview.md) — Summarizes the two workflow execution modes — Agent Delegation and Manual Orchestration — and why both matter for persistent file changes. Use when orienting to why this convention exists before reading the mode-specific details.
- [The Core Challenge](./the-core-challenge.md) — States the core problem execution modes solve — workflow file changes must persist to the actual filesystem — and the two solutions. Use when explaining why workflows need a defined execution mode at all.
- [Agent Delegation Mode (Preferred)](./agent-delegation-mode.md) — Defines Agent Delegation mode — invoking specialized agents via the Agent tool with subagent_type so file changes persist to the filesystem. Use when a workflow step references a named agent that exists as a defined delegated agent type and the step requires persistent file changes.
- [Manual Orchestration Mode (Fallback)](./manual-orchestration-mode.md) — Defines Manual Orchestration mode — executing workflow logic directly with Read/Write/Edit/Bash tools when agents aren't available as delegated agent types. Use when workflow agents are not available as defined delegated agent types, or when step-by-step visibility and manual iteration control are wanted.
- [Execution Mode Decision Flow](./execution-mode-decision-flow.md) — A decision tree for choosing Agent Delegation vs. Manual Orchestration for a given workflow step. Use when deciding, step by step, which execution mode applies to a specific workflow step reference.
- [Manual Mode Execution Pattern](./manual-mode-execution-pattern.md) — The six-step procedure (initialize, check, terminate?, fix, iterate, finalize) for running a workflow manually without agent delegation. Use when actually executing a workflow in Manual Orchestration mode and needing the concrete step sequence.
- [Implementation Example](./implementation-example.md) — Shows the "Execution Mode" section every workflow document should include, with a worked template. Use when authoring a new workflow document and needing a template for its Execution Mode section.
- [Future Considerations](./future-considerations.md) — Notes potential future automation via a workflow runner, and the compatibility constraints it would need to respect. Use when evaluating or designing a future automated workflow runner.
- [Tool Usage Rules](./tool-usage-rules.md) — What tools the AI assistant uses under Agent Delegation vs. Manual Orchestration. Use when checking which tool calls are correct for the active execution mode.
- [Common Pitfalls](./common-pitfalls.md) — Four recurring mistakes when choosing or executing an execution mode, each with the wrong and right pattern. Use when debugging why a workflow's file changes didn't persist or iteration behaved unexpectedly.
- [Principles Implemented/Respected](./principles-implemented-respected.md) — Traces this convention's execution-mode design back to the foundational principles it respects. Use when auditing this convention for traceability back to foundational principles.
- [Related Documentation](./related-documentation.md) — Links from the Execution Mode convention to the workflow pattern convention, an example workflow, and the AI agents convention. Use when navigating from this convention to the workflow pattern it composes with.
