---
description: "Defines Separation Pattern D, for knowledge that must stay inline in the agent rather than move to a Skill."
when_to_use: Use when deciding that a piece of task-specific logic should remain in the agent body rather than become a Skill.
---

# Agent-Skill Separation — Pattern D: Retain Task-Specific Logic

**Use when**: Content is genuinely agent-specific and not reusable.

**Keep in agent**:

- Agent's core responsibility description
- Task-specific workflows ("Step 1: Discovery Phase...")
- Agent-specific tool usage patterns
- Domain-specific validation logic
- Decision criteria unique to this agent
- Examples of when/when-not to use this agent

**Examples of task-specific content**:

- `docs-maker`: File naming logic for Diátaxis categories
- `docs-checker`: What specific validations to perform
- `docs-fixer`: How to assess confidence levels for doc fixes
- `plan-execution-checker`: Post-execution validation against plan requirements

**Rationale**: Agents remain self-contained for their specific task while delegating reusable knowledge to agent skills/Conventions.
