---
title: "Agent-Skill Separation — When to Use agent skills vs. Agent Content"
description: "Defines when to use agent skills versus inline agent content, and what belongs in each."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use when deciding whether new knowledge should live in an agent skill or directly in an agent's body.
---

# Agent-Skill Separation — When to Use agent skills vs. Agent Content

**Purpose**: Eliminate duplication between agents by extracting reusable knowledge into agent skills. Agents remain focused on task-specific workflows while agent skills provide shared domain expertise.

## When to Use agent skills vs. Agent Content

Use this decision tree to determine where knowledge belongs:

```
Is this knowledge...

└─ Used by 3+ agents?
   ├─ YES → Extract to Skill
   └─ NO → Keep in agent

└─ Reusable domain expertise? (color palettes, validation standards, report formats)
   ├─ YES → Create/extend Skill
   └─ NO → Keep in agent

└─ Agent-specific workflow? (task sequence, unique logic, custom decisions)
   ├─ YES → Keep in agent
   └─ NO → Consider Skill

└─ Convention details? (standards, rules, formats)
   ├─ YES → Link to convention document, optionally reference Skill
   └─ NO → Evaluate based on above criteria
```

## What Belongs in agent skills

**Extract to agent skills** (reusable knowledge):

1. **Validation Standards**
   - UUID chain generation logic
   - Progressive writing methodology
   - Report file naming patterns
   - Timestamp generation (UTC+7)
   - Criticality level definitions
   - Confidence assessment criteria

2. **Domain Expertise**
   - Content quality principles
   - Color accessibility palettes
   - Annotation density standards
   - Diátaxis framework application
   - Gherkin syntax rules

3. **Shared Workflows**
   - Maker-Checker-Fixer pattern
   - Link validation methodology
   - Factual accuracy verification
   - Mode parameter handling
   - Report discovery logic

## What Belongs in Agents

**Keep in Agents** (task-specific content):

1. **Task Workflows**
   - Step-by-step execution sequence
   - Agent-specific validation logic
   - Custom decision trees
   - Unique processing rules

2. **Scope Definitions**
   - What files/directories to validate
   - What to include/exclude
   - Agent mission and responsibilities
   - Collaboration with other agents

3. **Tool Usage Patterns**
   - How to use Read/Write/Bash/etc.
   - Tool combinations for specific tasks
   - Error handling strategies

4. **Output Formats**
   - Agent-specific report structures
   - Custom finding categories
   - Unique recommendation formats
