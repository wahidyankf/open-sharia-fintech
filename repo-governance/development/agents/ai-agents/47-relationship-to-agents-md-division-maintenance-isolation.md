---
title: "Relationship to AGENTS.md — Division, Maintenance, and Isolation"
description: "Defines the division of responsibilities between AGENTS.md and individual agents, AGENTS.md maintenance standards, and the agent isolation and delivery pattern."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use when deciding whether new guidance belongs in AGENTS.md or in an individual agent definition.
---

# Relationship to AGENTS.md — Division, Maintenance, and Isolation

## Division of Responsibilities

**AGENTS.md provides:**

- PASS: Project-wide guidance for ALL agents
- PASS: Project overview and context
- PASS: Environment setup (Volta, Node.js, npm)
- PASS: Git hooks and commit conventions
- PASS: High-level documentation organization
- PASS: Reference to this AI agents convention

**Individual agents provide:**

- PASS: Specialized domain expertise
- PASS: Specific task instructions
- PASS: Detailed guidelines for their area
- PASS: Examples and checklists for their domain

**This convention (ai-agents.md) provides:**

- PASS: Standards for how agents are structured
- PASS: Agent creation guidelines
- PASS: Tool and model selection criteria
- PASS: Convention referencing requirements

## AGENTS.md Maintenance Standards

**CRITICAL:** AGENTS.md is a navigation document, not a knowledge dump. All agents must help maintain its conciseness.

**Size Limits:**

- **Hard limit:** 40,000 characters (performance threshold - DO NOT EXCEED)
- **Target limit:** 30,000 characters (provides 25% headroom)
- **Warning threshold:** 35,000 characters (time to review and condense)

**Agent Responsibilities:**

1. **repo-rules-maker:**
   - MUST check AGENTS.md size when adding rules
   - Warn user if file exceeds 35,000 characters
   - Suggest condensation strategies (move details to convention docs)
   - Add only 2-5 line summaries to AGENTS.md, link to detailed docs

2. **docs-maker and related content agents:**
   - MUST NOT add verbose content to AGENTS.md
   - When adding conventions, create detailed doc first, then brief AGENTS.md summary
   - Maximum AGENTS.md section length: 3-5 lines + link

3. **All agents:**
   - When in doubt, link to detailed docs rather than duplicate content
   - Each AGENTS.md section should answer "what, where, why" but link to "how"
   - Comprehensive details belong in convention docs, not AGENTS.md

## Agent Isolation and Delivery Pattern

```
Startup: AGENTS.md ──loaded──> Orchestrator (main conversation)
Runtime: Orchestrator ──spawns──> Agents (isolated contexts)
        agent skills ──delivers via skills: field──> Agents
         Conventions ──explicit references──> Agents
```

**Critical Understanding:**

1. **Agents have isolated contexts** - They do NOT inherit AGENTS.md
2. **Agent skills deliver explicitly** - OnlySkills listed in agent's `skills:` field are available
3. **References are explicit** - Agents link to specific conventions they need
4. **Orchestrator has AGENTS.md** - Main conversation loads AGENTS.md, not agents

**Rules:**

1. **Don't duplicate** - Agents should reference conventions, not repeat content
2. **Do specialize** - Agents add domain expertise through agent skills and explicit knowledge
3. **Follow conventions** - All agents must comply with this convention
4. **Declare skills explicitly** - Every agent must have non-empty `skills:` field
