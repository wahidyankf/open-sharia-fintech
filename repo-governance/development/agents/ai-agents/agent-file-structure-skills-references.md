---
title: "Agent File Structure — Agent skills References"
description: "Defines the agent skills frontmatter field format and when to reference a Skill instead of inlining knowledge."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use when deciding whether an agent should reference a Skill via frontmatter or document knowledge inline.
---

# Agent File Structure — Agent skills References

**REQUIRED FIELD**: All agents MUST include a `skills:` frontmatter field for composability and consistency.

**Purpose:** The `skills:` field declares which agent skills (knowledge packages in the platform binding skills directory) the agent leverages. This enables:

- **Composability**: Explicit declarations of knowledge dependencies
- **Consistency**: All agents follow same structure (no special cases)
- **Discoverability**: Easy to see which agents use which agent skills
- **Validation**: Checkers can enforce field presence and validate references

## Agent skills Field Format

The `skills` field (already defined as field 6 in Required Frontmatter above) has the following detailed characteristics:

- **Format**: YAML array of strings
- **Required**: Yes (can be empty `[]`)
- **Values**: Skill names matching folder names in the platform binding skills directory
- **Auto-loading**: agent skills load when agent invoked AND task matches Skill description
- **Validation**: Referenced agent skills must exist in the platform binding skills directory
- **Example**: `skills: [docs-creating-accessible-diagrams, repo-applying-maker-checker-fixer]`

## When to Reference agent skills vs. Inline Knowledge

**Use agent skills references when:**

- PASS: Knowledge is specialized and deep (e.g., accessible color palettes, Gherkin syntax)
- PASS: Knowledge is shared across multiple agents (e.g., Maker-Checker-Fixer pattern)
- PASS: Knowledge requires progressive disclosure (overview at startup, details on-demand)
- PASS: Knowledge is frequently updated (agent skills centralize updates)
- PASS: Knowledge has multiple aspects (Skill can have reference.md, examples.md)

**Use inline knowledge when:**

- PASS: Knowledge is agent-specific and not shared
- PASS: Knowledge is simple and fits in a few paragraphs
- PASS: Knowledge is critical for agent's core operation (always needed)
- PASS: Knowledge is stable and rarely changes

## Agent skills Field Examples

**Agent using agent skills:**

```yaml
---
name: docs-maker
description: Expert documentation writer specializing in GitHub-compatible markdown and Diátaxis framework. Use when creating, editing, or organizing project documentation.
tools: Read, Write, Edit, Glob, Grep
model: sonnet
color: blue
skills:
  - docs-creating-accessible-diagrams
  - docs-applying-content-quality
  - docs-applying-diataxis-framework
---
```

**Agent not using agent skills:**

```yaml
---
name: simple-helper
description: Simple helper agent for basic tasks.
tools: Read
model: haiku
color: green
skills: []
---
```

## Agent skills Composition Pattern

Agents can reference multiple agent skills that work together:

```yaml
---
name: apps-ayokoding-www-general-maker
description: Expert at creating general Next.js content for ayokoding-www. Use when creating or updating general content pages for the AyoKoding website.
tools: Read, Write, Edit, Glob, Grep
model: sonnet
color: blue
skills:
  - apps-ayokoding-www-developing-content
  - docs-creating-accessible-diagrams
  - docs-validating-factual-accuracy
---
```

When this agent is invoked, all three agent skills auto-load if the task description matches their triggers. Agent skills compose seamlessly to provide comprehensive knowledge.
