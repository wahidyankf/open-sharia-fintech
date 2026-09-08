---
description: "Covers guidelines for future agent creation, the validation checklist, and the agent skills frontmatter field."
when_to_use: Use when validating that a new agent correctly separates its knowledge from agent skills, or when filling in its agent skills frontmatter field.
---

# Agent-Skill Separation — Guidelines, Validation, and Frontmatter Field

## Guidelines for Future Agent Creation

When creating new agents:

1. **Start lean**: Write minimum viable agent with task-specific instructions only
2. **Reference early**: Link to agent skills/Conventions instead of duplicating
3. **Quick reference OK**: Brief 1-3 line summaries with Skill/Convention links acceptable
4. **Scan for duplication**: Before finalizing, check if content exists in other agents (use Grep)
5. **3+ agent rule**: If same content appears in 3+ agents, extract to Skill/Convention

## Validation Checklist

Before committing agent changes:

- [ ] No content duplicates agent skills (check the platform binding skills directory catalog)
- [ ] No content duplicates Conventions (check `repo-governance/conventions/`)
- [ ] All agent skills referenced exist in the platform binding skills directory (primary source of truth)
- [ ] All Convention links point to valid files
- [ ] Task-specific instructions retained (agent is self-contained for its job)
- [ ] Agent within tier limits (Simple <800, Standard <1,200, Complex <1,800)

## Agent skills Frontmatter Field

**REQUIRED**: All agents MUST include `skills:` field in frontmatter.

**Format**:

```yaml
---
name: agent-name
description: Brief description
tools: Read, Write, Edit
model:
color: blue
skills: [docs-applying-content-quality, docs-creating-accessible-diagrams]
created: YYYY-MM-DD
---
```

**Empty agent skills**: If agent doesn't use any agent skills yet, use empty list:

```yaml
skills: []
```

**Multiple agent skills**: List all agent skills the agent references:

```yaml
skills: [skill-one, skill-two, skill-three]
```
