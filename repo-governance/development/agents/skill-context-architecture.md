---
title: "Skill Context Architecture"
description: "Architectural guidance on skill context modes in `.claude/skills/`. Inline skills work universally; fork skills work from main conversation only."
category: explanation
subcategory: development
tags:
  - ai-agents
  - skills
  - architecture
  - constraints
  - delegated-agents
created: 2026-01-22
when_to_use: Use when authoring a Skill and deciding its context mode, or when a Skill needs to spawn or delegate work.
---

# Skill Context Architecture

This document defines the architectural constraint governing skill context modes in `.claude/skills/`. Inline skills work universally; fork skills work from main conversation only. Both modes are supported in `.claude/skills/`.

## Contents

- [The Architectural Constraint](./skill-context-architecture/the-architectural-constraint.md) — core limitation.
- [The Repository Standard](./skill-context-architecture/the-repository-standard.md) — context modes, inline mode.
- [Fork agent skills: Main Conversation Only](./skill-context-architecture/fork-agent-skills-main-conversation-only.md) — fork use cases.
- [Validation and Compliance](./skill-context-architecture/validation-and-compliance.md) — checklist, mistakes.
- [Architecture Diagram](./skill-context-architecture/architecture-diagram.md) — visual reference.
- [Related Documentation](./skill-context-architecture/related-documentation.md) — further reading.
- [Enforcement](./skill-context-architecture/enforcement.md) — code-review checklist.
- [Summary](./skill-context-architecture/summary.md) — closing recap.

## Conventions Implemented/Respected

This development practice implements/respects the following conventions:

- **[AI Agents Convention](./ai-agents.md)**: By establishing the architectural constraint that skills must be inline-compatible, this practice ensures agents can reliably compose skills without runtime failures. The AI Agents Convention defines agent structure and tool usage; this architecture ensures skills integrate seamlessly with that structure across both main conversation and delegated agent contexts.

## Principles Implemented/Respected

This convention respects the following core principles:

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: Explicitly documents the architectural constraint preventing delegated agents from spawning other delegated agents. Makes the limitation visible and provides clear guidance on skill design decisions.

- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: Single-level delegated agent spawning prevents complex nested agent hierarchies. Agent skills remain simple knowledge containers that work everywhere, avoiding architectural complexity.

## Purpose

This architectural decision establishes that all skills stored in the `.claude/skills/` directory must remain compatible with both main conversation agents and delegated agents. Since delegated agents cannot spawn other delegated agents (architectural constraint of AI coding agents), skills with `context: fork` would be unusable in delegated agent contexts.

**Target Audience**:

- Agent developers creating or maintaining skills
- Repository maintainers reviewing skill contributions
- Anyone designing agent workflows involving skills
