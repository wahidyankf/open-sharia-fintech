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

**For agent-maker**:

1. After creating agent file, count lines and characters
2. Compare to tier limits based on agent type
3. Warn if approaching warning threshold
4. Suggest condensation if near limit

**For repo-rules-maker**:

1. When updating agents, check file size before/after
2. If agent crosses warning threshold, notify user
3. Suggest condensation strategies

**For all agent authors**:

1. Before committing agent changes, verify size
2. If approaching limits, review for redundancy
3. Consider moving details to convention docs
4. Link to detailed docs rather than duplicating

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
