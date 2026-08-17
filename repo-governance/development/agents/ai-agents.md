---
title: "AI Agents Convention"
description: "Standards for creating and managing AI agents in the platform binding directory (primary) and secondary agent directories"
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use when authoring, reviewing, or restructuring an agent definition file in .claude/agents/, or when deciding which sub-topic of agent standards applies.
---

# AI Agents Convention

Standards for creating, structuring, and managing AI agents in the platform binding directory (primary source of truth) and secondary agent directories (auto-generated). **Edit the primary platform binding directory first, then sync to secondary directories.**

## Overview, Principles, and File Structure

- [Overview](./ai-agents/01-overview.md) — what agents are.
- [Principles](./ai-agents/02-principles-implemented-respected.md) — principle list.
- [Token Budget](./ai-agents/03-token-budget-philosophy.md) — budget mindset.
- [Conventions](./ai-agents/04-conventions-implemented-respected.md) — sibling conventions.
- [Required Frontmatter](./ai-agents/05-agent-file-structure-required-frontmatter.md) — six fields.
- [Optional Frontmatter](./ai-agents/06-agent-file-structure-optional-frontmatter-fields.md) — optional fields.
- [Agent skills References](./ai-agents/07-agent-file-structure-skills-references.md) — skills field format.
- [Agent skills References (Continued)](./ai-agents/08-agent-file-structure-skills-references-continued.md) — DRY rule.
- [Document Structure](./ai-agents/09-agent-file-structure-document-structure.md) — body layout.

## Naming and Tool Access

- [Naming Conventions](./ai-agents/10-agent-naming-conventions.md) — file naming.
- [Naming Guidelines](./ai-agents/11-agent-naming-conventions-guidelines-and-name-vs-description.md) — name vs. desc.
- [Tool Access Patterns](./ai-agents/12-tool-access-patterns.md) — four patterns.
- [Report-Generating Agents](./ai-agents/13-tool-access-patterns-report-generating-agents.md) — Write+Bash rule.
- [Report-Generating (Continued)](./ai-agents/14-tool-access-patterns-report-generating-agents-continued.md) — progressive write.
- [Writing to Bindings](./ai-agents/15-tool-access-patterns-writing-to-platform-binding-directories.md) — binding-dir tools.

## Model Selection and Color

- [Model Selection](./ai-agents/16-model-selection-guidelines.md) — model tiers.
- [Color Categorization](./ai-agents/17-agent-color-categorization.md) — color field.
- [Color Translation Table](./ai-agents/18-platform-binding-examples-color-translation-table.md) — full table.
- [Categorization Rationale](./ai-agents/19-platform-binding-examples-categorization-rationale-and-notes.md) — rationale note.
- [Research Agent Note](./ai-agents/20-platform-binding-examples-research-agent-note.md) — research note.
- [Assigning Colors](./ai-agents/21-platform-binding-examples-assigning-colors-to-new-agents.md) — assignment.
- [Color Accessibility](./ai-agents/22-platform-binding-examples-color-accessibility.md) — accessibility.
- [Identification Example](./ai-agents/23-platform-binding-examples-color-accessibility-continued.md) — example.
- [Colors in Documentation](./ai-agents/24-platform-binding-examples-using-colors-in-documentation.md) — usage.

## Responsibility, Invocation, and Referencing

- [Responsibility Boundaries](./ai-agents/25-agent-responsibility-boundaries.md) — responsibility.
- [Invocation Patterns](./ai-agents/26-agent-invocation-patterns-and-decision-matrix.md) — Task vs. direct.
- [Invocation Limitation](./ai-agents/27-agent-invocation-patterns-limitation-and-examples.md) — isolation.
- [Referencing Standards](./ai-agents/28-convention-referencing-standards.md) — reference.

## Complexity, Size, and Agent-Skill Separation

- [Complexity Tiers](./ai-agents/29-agent-complexity-tiers.md) — tier taxonomy.
- [Condensing and Splitting](./ai-agents/30-condensing-and-splitting-agents.md) — condensing.
- [Size Checking](./ai-agents/31-agent-size-checking-and-content-philosophy.md) — the gate reports it.
- [Skill Separation Purpose](./ai-agents/32-agent-skill-separation-purpose-and-knowledge-classification.md) — rationale.
- [Separation Patterns A-C](./ai-agents/33-agent-skill-separation-patterns-a-b-c.md) — patterns A-C.
- [Pattern D](./ai-agents/34-agent-skill-separation-pattern-d.md) — task logic.
- [Guidelines and Validation](./ai-agents/35-agent-skill-separation-guidelines-validation-frontmatter.md) — guidelines.
- [Duplication Patterns](./ai-agents/36-agent-skill-separation-duplication-and-example.md) — duplication.
- [Separation Benefits](./ai-agents/37-agent-skill-separation-benefits.md) — rationale.

## Documentation, Verification, and Creating Agents

- [Documentation Standards](./ai-agents/38-agent-documentation-standards.md) — elements.
- [Verification Principles](./ai-agents/39-information-accuracy-verification-principles.md) — principles.
- [Worktree Awareness](./ai-agents/40-information-accuracy-verification-git-worktree-awareness.md) — rel. paths.
- [Toolchain Init Rule](./ai-agents/41-information-accuracy-verification-git-worktree-toolchain-init.md) — init rule.
- [Default Push Behavior](./ai-agents/42-information-accuracy-verification-git-worktree-awareness-continued.md) — push rule.
- [Verification Checklist](./ai-agents/43-information-accuracy-verification-checklist.md) — checklist.
- [When to Create](./ai-agents/44-creating-new-agents-when-to-create.md) — criteria.
- [Creation Checklist](./ai-agents/45-creating-new-agents-checklist.md) — checklist.
- [Agent Template](./ai-agents/46-creating-new-agents-template.md) — boilerplate.

## Relationship to AGENTS.md and Special Cases

- [Division of Responsibility](./ai-agents/47-relationship-to-agents-md-division-maintenance-isolation.md) — split.
- [What Belongs Where](./ai-agents/48-relationship-to-agents-md-what-belongs-where.md) — vs. agent.
- [Special Cases](./ai-agents/49-special-cases.md) — versioning.
- [Anti-Patterns](./ai-agents/50-anti-patterns.md) — mistakes.
- [Validation Compliance](./ai-agents/51-validation-and-compliance.md) — integration.

## Agent-Skill Separation in Practice

- [When to Use agent skills](./ai-agents/52-agent-skill-separation-when-and-what-belongs.md) — decision.
- [Separation Examples](./ai-agents/53-agent-skill-separation-examples-and-decision-tree.md) — examples.
- [Benefits and Metrics](./ai-agents/54-agent-skill-separation-benefits-implementation-measurement-vigilance.md) — metrics.
- [Related Documentation](./ai-agents/55-related-documentation.md) — reading.

## Multi-Harness Binding Operation

- [Multi-Harness Directory](./ai-agents/56-multi-harness-binding-directory-hierarchy-format.md) — directory.
- [Multi-Harness Sync](./ai-agents/57-multi-harness-binding-sync-references-history-troubleshooting.md) — sync.
