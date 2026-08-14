---
title: "Agent Families — se-separation and repo-workflow"
description: "The remaining two agent families using this pattern."
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
when_to_use: "Use for SE-doc separation or workflow docs."
---

# Agent Families — se-separation and repo-workflow

## 8. docs-software-engineering-separation-\* (SE Doc Separation)

**Domain**: Software engineering documentation separation between language-agnostic and language-specific content

**Agents**:

- **docs-software-engineering-separation-checker** (🟩 Checker) - Validates separation of SE content by language specificity
- **docs-software-engineering-separation-fixer** (🟨 Fixer) - Applies validated fixes to SE doc separation issues

**Use Case**: Ensuring programming language tutorials are properly separated between general SE concepts and language-specific implementations

**Example**:

```
1. docs-software-engineering-separation-checker: Validate docs/explanation/software-engineering/ separation
2. docs-software-engineering-separation-fixer: Move language-specific content to correct location
```

## 9. repo-workflow-\* (Workflow Documentation)

**Domain**: Workflow documentation in `repo-governance/workflows/` — completeness, agent references, trigger conditions

**Agents**:

- **repo-workflow-maker** (🟦 Maker) - Creates workflow documentation following workflow pattern convention
- **repo-workflow-checker** (🟩 Checker) - Validates workflow documentation quality and compliance with workflow pattern convention
- **repo-workflow-fixer** (🟨 Fixer) - Applies validated fixes from workflow-checker audit reports

**Use Case**: Maintaining accurate and complete governance workflow documentation

**Example**:

```
1. repo-workflow-maker: Create new maker-checker-fixer workflow document
2. repo-workflow-checker: Validate completeness, agent references, trigger conditions
3. repo-workflow-fixer: Apply validated fixes to workflow documentation
```
