---
title: "Scope"
description: "Which fixer agents this convention covers."
category: explanation
subcategory: development
tags:
  - fixer-agents
  - confidence-levels
  - validation
  - automation
  - quality-assurance
created: 2025-12-14
when_to_use: "Use when checking whether a fixer is in scope."
---

# Scope

## Agents Using This System

All fixer agents implement this confidence level system:

- **rules-fixer** - Repository-wide structural consistency fixes
- **apps-ayokoding-www-general-fixer** - ayokoding-www general content fixes
- **apps-ayokoding-www-by-example-fixer** - ayokoding-www by-example tutorial fixes
- **apps-ayokoding-www-facts-fixer** - ayokoding-www factual accuracy fixes
- **apps-ayokoding-www-in-the-field-fixer** - ayokoding-www in-the-field tutorial fixes
- **apps-ayokoding-www-link-fixer** - ayokoding-www link validation fixes
- **docs-tutorial-fixer** - Tutorial quality fixes
- **apps-ose-www-content-fixer** - ose-www Next.js content fixes
- **readme-fixer** - README quality fixes
- **docs-fixer** - Documentation factual accuracy fixes
- **plan-fixer** - Plan structural and format fixes
- **docs-software-engineering-separation-fixer** - Software engineering documentation separation fixes
- **repo-workflow-fixer** - Repository workflow structural consistency fixes

## Universal Application

The three confidence levels (HIGH, MEDIUM, FALSE_POSITIVE) are universal. Each agent:

1. **Reads audit reports** from corresponding checker agent
2. **Re-validates findings** using same patterns as checker
3. **Assesses confidence** using criteria defined in this convention
4. **Applies HIGH confidence fixes** automatically
5. **Skips MEDIUM and FALSE_POSITIVE** with explanations
6. **Generates fix reports** documenting all decisions
