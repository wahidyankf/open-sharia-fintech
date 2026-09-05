---
title: "Model Tiers — Planning-Grade (Inherit / No Model Specified)"
description: "Defines the planning-grade tier: when to omit the model field for budget-adaptive inheritance."
category: explanation
subcategory: development
tags:
  - ai-agents
  - model-selection
  - development
  - standards
created: 2025-11-23
when_to_use: Use when deciding whether a new agent should omit its model field for planning-grade, budget-adaptive behaviour.
---

# Model Tiers — Planning-Grade (Inherit / No Model Specified)

## Planning-Grade (Inherit / No Model Specified)

**When to use**: Tasks requiring creative reasoning, architectural decisions, code generation, multi-step judgment calls, or nuanced content creation.

**Cognitive profile**: Deep analytical reasoning, novel problem-solving, multi-step planning, creative synthesis across domains, nuanced judgment under ambiguity.

**Task characteristics**:

- Open-ended problems without a single correct answer
- Architectural decisions requiring trade-off analysis
- Code generation across multiple languages and paradigms
- Content creation requiring domain expertise and originality
- Multi-step planning with conditional branching
- Tasks where the agent must invent approaches, not follow templates

**Agent examples**:

- **SWE developers** (all language-specific agents) -- generate and refactor production code across diverse language ecosystems, requiring deep understanding of idioms, patterns, and trade-offs
- **plan-maker** -- creates project plans requiring scope analysis, dependency mapping, and strategic sequencing
- **docs-tutorial-maker** -- produces tutorial content requiring pedagogical reasoning, narrative flow, and learning progression design
- **swe-ui-maker** -- creates UI components requiring CVA variants, Radix composition, accessibility, tests, and stories in one pass

**Frontmatter**: Omit the `model` field. This is intentional — the agent inherits the
session's active model.

```yaml
---
name: swe-typescript-dev
description: Expert TypeScript/Node.js developer...
tools: [Read, Write, Edit, Glob, Grep, Bash]
color: purple
---
```

**Budget-Adaptive Inheritance**: Omitting `model` is a deliberate design choice, not an
oversight. The agent inherits the calling session's model, which adapts to the user's
account tier and token budget:

| Session plan               | Inherited model | Output quality |
| -------------------------- | --------------- | -------------- |
| Max / Team Premium         | `Opus 4.7`      | Highest        |
| Pro / Standard / API       | `Sonnet 4.6`    | High           |
| Bedrock / Vertex / Foundry | `Sonnet 4.5`    | High           |

This means a Max-plan user gets planning-grade plans, architecture, and code generation,
while a Pro-plan user gets execution-grade output — proportional to their purchasing
decision. Do NOT add `model: opus` to these agents. Doing so overrides budget-adaptive
behaviour and forces planning-grade API charges regardless of the user's account tier (see Common
Mistakes).
