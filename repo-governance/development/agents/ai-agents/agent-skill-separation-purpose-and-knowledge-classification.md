---
description: "Explains why agent content and agent skills content must stay separated and gives the knowledge-classification decision tree."
when_to_use: Use when deciding whether a piece of knowledge belongs in an agent's body or in a Skill.
---

# Agent-Skill Separation — Purpose and Knowledge Classification

## Purpose

This section defines how to properly separate reusable knowledge (agent skills) from agent-specific instructions (Agent files), ensuring maintainability, reducing duplication, and enabling effective knowledge delivery.

**Validated through**: agent skills Simplification pilot (2026-01-03) - docs family achieved 49.2% size reduction while maintaining 100% functionality.

## Knowledge Classification Decision Tree

When writing or updating an agent, use this decision tree to determine where content belongs:

```
Is this content reusable across 3+ agents?
│
├─ YES → Move to Skill or Convention Document
│   │
│   ├─ Is it actionable "how-to" guidance?
│   │   └─ YES → Create/update Skill in .claude/skills/
│   │       Examples: applying-content-quality, creating-accessible-diagrams
│   │
│   └─ Is it technical specification or standard?
│       └─ YES → Create/update Convention in repo-governance/conventions/
│           Examples: Color Accessibility Convention, Mathematical Notation Convention
│
└─ NO → Keep in Agent File
    │
    └─ Is it task-specific workflow, validation logic, or decision criteria?
        └─ YES → This is agent-specific knowledge, keep in agent
            Examples: "When to use this agent", validation workflow steps, tool usage patterns
```
