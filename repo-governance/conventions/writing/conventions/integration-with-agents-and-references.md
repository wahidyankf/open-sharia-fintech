---
title: "Convention Writing Convention — Integration with Agents and References"
description: Which agents create and consume convention documents, the agent-integration checklist, and cross-references to related meta-documentation.
when_to_use: Use when wiring a new convention into agent prompts or looking up related meta-conventions and governance documents.
category: explanation
subcategory: conventions
tags:
  - meta
  - conventions
  - standards
  - documentation
created: 2025-12-07
---

# Integration with Agents and References

## Integration with Agents

Conventions are most effective when enforced or assisted by agents:

### Agents That Create Conventions

- **docs-maker** - Creates convention documents following this meta-convention
- **rules-maker** - Propagates convention changes across repository

### Agents That Use Conventions

- **docs-checker** - Validates documentation follows conventions
- **docs-link-checker** - Enforces linking convention
- **apps-ayokoding-www-general-checker** - Validates general ayokoding-web content conventions
- **apps-ayokoding-www-by-example-checker** - Validates by-example tutorial conventions
- **rules-checker** - Audits convention compliance

### Agent Integration Checklist

When creating a convention:

- [ ] Identify which agents should reference this convention
- [ ] Update agent prompts if needed to reference new convention
- [ ] Add convention to agent's "References" section
- [ ] Test that agents correctly apply the convention

## References

**Related Meta-Documentation:**

- [Content Quality Principles](../quality.md) — Universal quality standards for all markdown content
- [Diátaxis Framework](../../structure/diataxis-framework.md) — Four-category documentation organization framework

**File Conventions:**

- [File Naming Convention](../../structure/file-naming.md) — Kebab-case file naming rules
- [Linking Convention](../../formatting/linking.md) — How to link between documentation files

**Development Practices:**

- [AI Agents Convention](../../../development/agents/ai-agents.md) — How to create AI agents (parallel meta-doc for development/)

**Repository Guidance:**

- [AGENTS.md](../../../../AGENTS.md) — Project-wide guidance for AI agents
- [Conventions Index](../../README.md) — Index of all convention documents

**Agents:**

- `docs-maker` - Creates convention documents following this structure
- `rules-maker` - Propagates convention changes
- `rules-checker` - Validates convention compliance
