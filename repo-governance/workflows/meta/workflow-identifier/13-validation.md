---
title: "Validation"
description: The six checks a workflow document must pass before execution — frontmatter schema, agent references, input/output types, dependencies, state references, and file naming.
category: explanation
subcategory: workflows
tags:
  - workflows
  - agents
  - orchestration
  - patterns
created: 2025-12-23
when_to_use: Use when checking whether a workflow document is ready for execution.
---

# Validation

Workflows must be validated before execution:

- PASS: **Frontmatter schema**: All required fields present
- PASS: **Agent references**: All agents exist in the primary binding directory (e.g., `.claude/agents/`) or secondary directories (e.g., `.opencode/agents/`)
- PASS: **Input/output types**: Valid type declarations
- PASS: **Step dependencies**: No circular dependencies
- PASS: **State references**: All references resolve
- PASS: **File naming**: Plain name in correct subdirectory of `repo-governance/workflows/`

Validation performed by `workflow-validator` (future agent).
