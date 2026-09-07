---
title: "Agent Color Categorization"
description: "Defines the color field and its role-to-category mapping for agent definitions."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use when assigning or validating the color field on an agent definition.
---

# Agent Color Categorization

## Color Field (Required)

The `color` frontmatter field provides visual categorization for agents based on their **primary role**. This helps users quickly identify agent types and understand their capabilities at a glance.

**Format:**

```yaml
---
name: agent-name
description: Expert in X specializing in Y. Use when Z.
tools: Read, Glob, Grep
model:
color: blue
---
```

**Field Definition:**

- **`color`** (required)
  - Values: `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan`
  - Indicates the agent's primary role category
  - Used for visual identification in agent listings
  - Helps users choose the right agent type

## Color-to-Role Mapping

Agents are categorized by their **primary role** which aligns with naming suffixes and tool permissions:

| Color         | Role             | Purpose                               | Tool Pattern                            | Agents                                                                                                        |
| ------------- | ---------------- | ------------------------------------- | --------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| 🟦 **Blue**   | **Makers**       | Create new content from scratch       | Has `Write` tool                        | docs-maker<br>plan-maker<br>docs-tutorial-maker<br>rules-maker                                                |
| 🟩 **Green**  | **Checkers**     | Validate and generate reports         | Has `Write`, `Bash` (no `Edit`)\*\*     | rules-checker<br>plan-checker<br>docs-checker<br>docs-link-checker\*\*<br>apps-ayokoding-www-link-checker\*\* |
| 🟨 **Yellow** | **Fixers**       | Modify and propagate existing content | Has `Edit` (usually not `Write`)        | docs-file-manager<br>readme-fixer<br>repo-workflow-fixer                                                      |
| 🟪 **Purple** | **Implementors** | Execute plans with full tool access   | Has `Write`, `Edit`, `Bash` (or Bash)\* | deployers\*<br>swe-\*-dev agents                                                                              |

## Platform Binding Color Translation

The named color (`blue`, `green`, etc.) written by hand in `.claude/agents/*.md` is the **source of truth**. Authors never touch `.opencode/agents/*.md` directly — those are regenerated artefacts.

When the sync tool writes secondary binding files, it translates the named color to a platform-compatible value. Some secondary platforms enforce a schema that accepts only hex codes or a fixed set of theme tokens; named colors such as `blue` are rejected by those platforms.
