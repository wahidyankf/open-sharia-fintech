---
title: "Best Practices for AI Agents Development"
description: "Proven practices for developing maintainable, secure, and effective AI agents in the .claude/agents/ directory."
category: explanation
subcategory: development
tags:
  - ai-agents
  - best-practices
  - development
  - standards
created: 2026-05-12
when_to_use: Use when authoring a new agent and checking it against proven practices, or citing a best practice in a review.
---

# Best Practices for AI Agents Development

> **Companion Document**: For common mistakes to avoid, see [Anti-Patterns](../agents/anti-patterns.md)

This document outlines best practices for developing AI agents in the `.claude/agents/` directory. Following these practices ensures agents are maintainable, secure, and effective at automating repository tasks.

## Contents

- [Single Responsibility, Minimum Tools, Model Choice, and Descriptions](./best-practices/best-practices-1-to-4.md) — practices 1-4.
- [Tool Usage Docs, Testing, Frontmatter Context, Naming, and Dependencies](./best-practices/best-practices-5-to-9.md) — practices 5-9.
- [Summary](./best-practices/summary.md) — quick-reference table.

## Conventions Implemented/Respected

- **[File Naming Convention](../../conventions/structure/file-naming.md)**: Agent files follow kebab-case naming
- **[Content Quality Principles](../../conventions/writing/quality.md)**: Active voice, clear headings

## Overview

This document outlines best practices for developing AI agents in the `.claude/agents/` directory. Following these practices ensures agents are maintainable, secure, and effective at automating repository tasks.

## Principles Implemented/Respected

This companion document respects:

- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)**: Agents automate repetitive tasks, reducing manual effort.
- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: Clear permissions and behaviour — minimum necessary tool access.
- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: Single responsibility, focused agents.
- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: Test edge cases and verify behaviour before declaring agents production-ready.

## Purpose

Provide actionable guidance for:

- Agent design and architecture
- Tool permission management
- Model selection
- Testing and validation
- Documentation standards

## Related Documentation

- [AI Agents Convention](./ai-agents.md) - Complete agent development standards
- [Anti-Patterns](./anti-patterns.md) - Common mistakes to avoid
- [Skill Context Architecture](./skill-context-architecture.md) - Skill integration patterns
- [Agent Workflow Orchestration Convention](./agent-workflow-orchestration.md) - How agents plan, verify, and self-improve during multi-step tasks
- [Agents Index](../../../.claude/agents/README.md) - All available agents
