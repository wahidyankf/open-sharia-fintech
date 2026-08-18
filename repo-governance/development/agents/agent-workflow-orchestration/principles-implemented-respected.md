---
title: "Principles Implemented/Respected"
description: "Lists the core repository principles this convention implements and respects."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - workflow
  - orchestration
created: 2025-11-23
when_to_use: Use when checking which principles justify a rule in the Agent Workflow Orchestration Convention.
---

# Principles Implemented/Respected

This practice respects the following core principles:

- **[Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md)**: Plan mode requires agents to think before acting. Breaking complex tasks into steps with verification criteria prevents hidden confusion from propagating through multi-step work.

- **[Root Cause Orientation](../../../principles/general/root-cause-orientation.md)**: Verification before done enforces the senior engineer standard. The self-improvement loop demands root cause analysis after any mistake rather than moving on.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: Delegated agents keep the main context clean by offloading focused subtasks. One task per delegated agent prevents multi-purpose delegated agents that are harder to reason about.

- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**: Autonomous bug fixing eliminates unnecessary user hand-holding. Agents run tests, read logs, and resolve failures without requiring step-by-step instruction.
