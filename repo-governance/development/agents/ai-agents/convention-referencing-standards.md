---
description: "Defines the required Reference Documentation section, its categories, and the link format agents must use."
when_to_use: Use when writing or validating an agent's Reference Documentation section.
---

# Convention Referencing Standards

## Required Section: Reference Documentation

**Every agent MUST include a "Reference Documentation" section** at the end. See the [Document Structure](./agent-file-structure-document-structure.md) section below for the complete format.

## Reference Categories

Organize references into clear categories:

1. **Project Guidance** - Always reference `AGENTS.md`
2. **Agent Conventions** - Always reference this document (`ai-agents.md`)
3. **Domain-Specific Conventions** - Reference relevant conventions
4. **Related Agents** - Cross-reference complementary agents

## Link Format

Use GitHub-compatible markdown with relative paths:

```markdown
PASS: Good:

- `repo-governance/development/agents/ai-agents.md` - AI agents convention

FAIL: Bad:

- [[ai-agents]] - Wiki-link syntax (GitHub does not render these)
- `/repo-governance/development/agents/ai-agents.md` - Absolute path
- `repo-governance/development/agents/ai-agents` - Missing .md extension
```

See [Linking Convention](../../../conventions/formatting/linking.md) for details.
