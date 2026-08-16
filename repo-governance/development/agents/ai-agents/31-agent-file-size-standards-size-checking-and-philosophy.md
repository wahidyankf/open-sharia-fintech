---
title: "Agent File Size Standards — Size Checking Process and Content Philosophy"
description: "Describes the size-checking process to run before finalizing an agent, and the content philosophy behind the size limits."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use when running the size-checking process on a new or edited agent, or explaining why the size limits exist.
---

# Agent File Size Standards — Size Checking Process and Content Philosophy

## Size Checking Process

Nobody counts by hand. The
[Governance Word-Budget Convention](../../../conventions/structure/governance-word-budget.md)
measures every agent definition deterministically at pre-push and in CI, so the only authoring
obligation is to respond to what the gate reports.

**For all agent authors**:

1. Let the gate report the size — do not estimate it
2. When it flags a file, review for redundancy against convention docs first
3. Remediate by progressive disclosure: move detail into a linked doc rather than compressing prose
4. Link to detailed docs rather than duplicating them

## Agent Content Philosophy

**Focus on single responsibility**:

- Each agent should do ONE thing well
- Complex workflows should compose multiple agents, procedures, and/or other workflows
- Don't create "Swiss Army knife" agents

**Detailed but targeted prompts**:

- Provide comprehensive guidance for the agent's domain
- Don't document unrelated concerns
- Link to convention docs instead of duplicating

**Avoid duplication with convention docs**:

- Convention docs are the source of truth
- Agents should reference conventions, not repeat them
- Exception: Agent-specific applications of conventions

**Balance comprehensiveness with conciseness**:

- Include essential decision logic and examples
- Remove tangential information
- Prefer structured formats (tables, checklists) over prose
