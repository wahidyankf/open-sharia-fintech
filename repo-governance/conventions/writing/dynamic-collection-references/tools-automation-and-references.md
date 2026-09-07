---
title: "Dynamic Collection References — Tools, Automation, and References"
description: The agents that check and enforce this convention, and links to related conventions, development practices, and agents.
when_to_use: Use when looking up which agent enforces this convention or which related documents to cross-reference.
category: explanation
subcategory: conventions
tags:
  - conventions
  - documentation
  - maintenance
  - collections
created: 2026-02-22
---

# Tools, Automation, and References

## Tools and Automation

The following agents check and enforce this convention:

- **rules-checker** - Validates repository-wide consistency including hardcoded counts
- **rules-propagation** - Applies fixes for governance violations including count removal

## References

**Related Conventions:**

- [Content Quality Principles](../quality.md) — Universal quality standards; accuracy is a quality requirement
- [Conventions Writing Convention](../conventions.md) — Meta-convention for writing convention documents

**Related Development Practices:**

- [AI Agents Convention](../../../development/agents/ai-agents.md) — Defines how agents are structured and maintained

**Agents:**

- `rules-maker` - Creates governance documents following this convention
- `rules-checker` - Validates convention compliance across the repository
- `rules-propagation` - Fixes convention violations
