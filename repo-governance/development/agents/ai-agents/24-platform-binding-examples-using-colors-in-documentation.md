---
title: "Platform Binding Examples — Using Colors in Documentation and Examples"
description: "Shows how to reference agent colors in documentation and lists worked color-field examples."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use when documenting an agent's color in prose or when picking an example color-field value.
---

# Platform Binding Examples — Using Colors in Documentation and Examples

## Using Colors in Documentation

**Agent README Listings:**

When listing agents in the agent definition directory README (`.claude/agents/README.md` or equivalent), use the colored square emoji:

```markdown
### 🟦 `docs-maker.md`

Expert documentation writer specializing in GitHub-compatible markdown and Diátaxis framework.
```

**Consistency with Emoji Convention:**

Colored square emojis follow the [Emoji Usage Convention](../../../conventions/formatting/emoji.md):

- Use at the start of headings for visual categorization
- Maintain semantic consistency (same color = same role across all docs)
- Avoid overuse (1 emoji per agent listing)

## Color Field Examples

**Maker Agent (Blue):**

```yaml
---
name: docs-maker
description: Expert documentation writer specializing in GitHub-compatible markdown and Diátaxis framework. Use when creating, editing, or organizing project documentation.
tools: Read, Write, Edit, Glob, Grep
model: sonnet
color: blue
---
```

**Checker Agent (Green):**

```yaml
---
name: repo-rules-checker
description: Validates consistency between agents, AGENTS.md, conventions, and documentation. Use when checking for inconsistencies, contradictions, duplicate content, or verifying repository rule compliance.
tools: Read, Glob, Grep, Write, Bash
model: sonnet
color: green
---
```

**Fixer Agent (Yellow):**

```yaml
---
name: readme-fixer
description: Applies validated fixes from readme-checker audit reports. Re-validates README findings before applying changes. Use after reviewing readme-checker output.
tools: Read, Edit, Glob, Grep, Write, Bash
model: sonnet
color: yellow
---
```

**Implementor Agent (Purple):**

```yaml
---
name: swe-typescript-dev
description: Develops TypeScript applications following type safety principles, modern patterns, and platform coding standards. Use when implementing TypeScript code for OSE Platform.
tools: Read, Write, Edit, Glob, Grep, Bash
color: purple
---
```
