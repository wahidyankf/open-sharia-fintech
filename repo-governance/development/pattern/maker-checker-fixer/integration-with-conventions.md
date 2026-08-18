---
title: "Integration with Conventions"
description: "How this pattern integrates with other conventions."
category: explanation
subcategory: development
tags:
  - maker-checker-fixer
  - workflow
  - content-quality
  - agent-patterns
  - validation
  - automation
created: 2025-12-14
when_to_use: "Use to trace a convention into this workflow."
---

# Integration with Conventions

The maker-checker-fixer pattern integrates with repository conventions:

| Convention                                                                     | How Pattern Uses It                                             |
| ------------------------------------------------------------------------------ | --------------------------------------------------------------- |
| [AI Agents Convention](../../agents/ai-agents.md)                              | Defines agent structure, tool permissions, color coding         |
| [Criticality Levels Convention](../../quality/criticality-levels.md)           | Checkers categorize by criticality, fixers use for priority     |
| [Fixer Confidence Levels Convention](../../quality/fixer-confidence-levels.md) | Fixers assess confidence, combine with criticality for priority |
| [Repository Validation Methodology](../../quality/repository-validation.md)    | Standard validation patterns used by checker/fixer              |
| [Content Quality Principles](../../../conventions/writing/quality.md)          | What checkers validate (quality standards)                      |
| [Tutorial Convention](../../../conventions/tutorials/general.md)               | What docs-tutorial-maker/checker enforce                        |
| [README Quality Convention](../../../conventions/writing/readme-quality.md)    | What readme-maker/checker enforce                               |
| [Temporary Files Convention](../../infra/temporary-files.md)                   | Where checker/fixer reports are stored                          |

**Key Point**: The pattern is a **workflow framework**. The conventions define **what** to validate/enforce.
