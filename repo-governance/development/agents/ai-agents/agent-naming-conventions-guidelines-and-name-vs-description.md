---
title: "Agent Naming Conventions — Naming Guidelines and Agent Name vs. Description"
description: "Gives the general naming guidelines and explains the difference between an agent's name and its description."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use when choosing an agent's short name or writing its frontmatter description alongside its name.
---

# Agent Naming Conventions — Naming Guidelines and Agent Name vs. Description

## Naming Guidelines

1. **Be descriptive** - Name should indicate the agent's purpose
2. **Be concise** - Avoid unnecessary words
3. **Be action-oriented** - Use verbs when appropriate (`maker`, `checker`, `validator`, `fixer`, `deployer`)
4. **Avoid redundancy** - Don't add `-agent` suffix (implied by location)
5. **Match frontmatter** - `name` field must match filename exactly (including scope prefix)
6. **Use scope when appropriate** - Add `apps-[app-name]-` prefix for app-specific agents

## Agent Name vs Description

- **Name**: Short identifier used in file system and frontmatter (includes scope prefix if applicable)
- **Description**: Detailed explanation of when and how to use

Example - General agent:

```yaml
name: docs-maker # Short, kebab-case, no scope (general-purpose)
description: Expert documentation writer specializing in GitHub-compatible markdown and Diátaxis framework. Use when creating, editing, or organizing project documentation. # Detailed usage guidance
```

Example - App-scoped agent:

```yaml
name: apps-ayokoding-www-general-maker # Includes scope prefix
description: Expert at creating general Next.js content for ayokoding-www. Use when creating or updating general content pages for the AyoKoding website. # Detailed usage guidance
```
