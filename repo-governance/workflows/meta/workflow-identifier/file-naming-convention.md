---
title: "File Naming Convention"
description: Workflow files use plain kebab-case names (no prefix) in the subdirectory that encodes their category.
category: explanation
subcategory: workflows
tags:
  - workflows
  - agents
  - orchestration
  - patterns
created: 2025-12-23
when_to_use: Use when naming a new workflow file or its subdirectory location.
---

# File Naming Convention

All workflow files follow the plain-name pattern (no prefix), organized by subdirectory:

```
[workflow-identifier].md
```

- **No prefix**: Workflow files use plain descriptive names
- **Subdirectory**: Location in `repo-governance/workflows/[category]/` encodes the context
- **Identifier**: Lowercase, hyphen-separated
- **Extension**: `.md`

**Examples**:

- `repo-rules-quality-gate.md` (in `repo-governance/workflows/repo/`)
- `plan-quality-gate.md` (in `repo-governance/workflows/plan/`)
- `docs-quality-gate.md` (in `repo-governance/workflows/docs/`)

**Note**: Workflow files use plain kebab-case names in their respective subdirectories. See [File Naming Convention](../../../conventions/structure/file-naming.md) for the current naming rules.
