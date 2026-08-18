---
title: "Agent File Structure — Document Structure"
description: "Defines the required document structure sections for an agent definition file's body."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use when laying out the body sections of a new agent definition file.
---

# Agent File Structure — Document Structure

After frontmatter, agents should follow this structure:

```markdown
# [Agent Name] Agent

## Agent Metadata

- **Role**: [Maker (blue) / Checker (green) / Fixer (yellow) / Implementor (purple)]

[One-paragraph introduction describing the agent's role]

## Core Expertise / Core Responsibility

[Clear statement of the agent's primary purpose and capabilities]

## [Domain-Specific Sections]

[Detailed guidelines, standards, checklists, examples specific to this agent]

## Reference Documentation

[Links to AGENTS.md, conventions, and related documentation]
```

**Required Sections:**

1. **Title (H1)**: Must follow pattern `# [Name] Agent`. Exception: App-scoped agents may use `# [Role] for [app-name]` (e.g., `# Content Checker for ose-www`)
2. **Core Expertise/Responsibility (H2)**: Clear purpose statement
3. **Reference Documentation (H2)**: Links to relevant conventions and guidance

**Optional Sections:**

- Detailed guidelines
- Examples and anti-patterns
- Checklists
- Decision trees
- Troubleshooting
