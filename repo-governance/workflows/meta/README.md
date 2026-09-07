---
description: Reference material for designing workflows that are understandable and reusable
when_to_use: Use when routing to reference material about how workflows are structured or executed.
---

# Workflow Meta Documentation

Use this reference when you are creating or reshaping a workflow. It explains the shared structure that makes workflows understandable, composable, and reviewable.

## Purpose

This documentation defines **HOW workflows should be designed and documented**, covering the workflow pattern convention that all workflows must follow including structure, frontmatter requirements, and composition patterns.

## Scope

**✅ Belongs Here:**

- Workflow pattern definitions
- Workflow structure conventions
- Workflow frontmatter schema
- Workflow composition rules
- Meta-workflow documentation

**❌ Does NOT Belong:**

- Specific workflow implementations (those are in domain folders)
- Agent development standards (that's development/agents/)
- General development patterns (that's development/pattern/)

## Documents

- [Workflow Pattern Convention](./workflow-identifier.md) — Standards for creating orchestrated multi-step processes that compose agents, procedures, and/or other workflows. Use when defining, structuring, or validating a new workflow document, or when deciding whether a task should become a workflow at all.
- [Workflow Execution Mode Convention](./execution-modes.md) — Defines execution modes for workflows — Agent Delegation (preferred) and Manual Orchestration (fallback) — explaining how to use the Agent tool for delegated agent invocation and when to fall back to direct execution. Use when a workflow step needs to invoke an agent or run its logic directly, and you need to decide which execution mode applies and how to execute it correctly.

## Related Documentation

- [Workflows Index](../README.md) - All orchestrated workflows
- [Maker-Checker-Fixer Pattern](../../development/pattern/maker-checker-fixer.md) - Core quality workflow pattern
- [AI Agents Convention](../../development/agents/ai-agents.md) - Agent standards workflows orchestrate
- [Repository Architecture](../../repository-governance-architecture.md) - Six-layer governance model (Layer 5: Workflows)
