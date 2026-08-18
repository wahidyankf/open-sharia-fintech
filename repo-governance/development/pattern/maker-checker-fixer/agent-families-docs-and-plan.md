---
title: "Agent Families — docs and plan"
description: "Two agent families using this pattern."
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
when_to_use: "Use for documentation accuracy or plan completeness."
---

# Agent Families — docs and plan

## 6. docs-\* (Documentation Factual Accuracy)

**Domain**: Documentation factual correctness, technical accuracy, code examples, contradictions

**Agents**:

- **docs-maker** (🟦 Maker) - Creates and edits documentation following conventions
- **docs-checker** (🟩 Checker) - Validates factual accuracy using WebSearch/WebFetch
- **docs-fixer** (🟨 Fixer) - Applies validated factual accuracy fixes

**Use Case**: Ensuring documentation is technically accurate and current

**Example**:

```
1. docs-maker: Create API documentation with code examples
2. docs-checker: Validate command syntax, version numbers, API methods against authoritative sources
3. docs-fixer: Fix incorrect command flags, update outdated versions, correct broken links
```

**Note**: docs-fixer distinguishes objective factual errors (command syntax, version numbers - apply automatically) from subjective improvements (narrative quality, terminology - manual review)

## 7. plan-\* (Plan Completeness and Structure)

**Domain**: Project plan structure, completeness, codebase alignment, technical accuracy

**Agents**:

- **plan-maker** (🟦 Maker) - Creates project planning documents
- **plan-checker** (🟩 Checker) - Validates plan readiness for implementation
- **plan-fixer** (🟨 Fixer) - Applies validated structural/format fixes

**Use Case**: Ensuring plans are complete and accurate before implementation

**Example**:

```
1. plan-maker: Create project plan with requirements, tech-docs, delivery checklist
2. plan-checker: Validate required sections exist, verify codebase assumptions, check technology choices
3. plan-fixer: Add missing sections, fix broken file references, correct format violations
```

**Note**: plan-fixer distinguishes structural/format issues (missing sections, broken links - apply automatically) from strategic decisions (technology choices, scope, architecture - manual review)
