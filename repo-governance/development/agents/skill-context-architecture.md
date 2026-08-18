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

- [Principles Implemented/Respected](./skill-context-architecture/principles-implemented-respected.md) — principle list.
- [Conventions Implemented/Respected](./skill-context-architecture/conventions-implemented-respected.md) — sibling conventions.
- [Purpose](./skill-context-architecture/purpose.md) — why this matters.
- [The Architectural Constraint](./skill-context-architecture/the-architectural-constraint.md) — core limitation.
- [The Repository Standard](./skill-context-architecture/the-repository-standard.md) — context modes, inline mode.
- [Fork agent skills: Main Conversation Only](./skill-context-architecture/fork-agent-skills-main-conversation-only.md) — fork use cases.
- [Validation and Compliance](./skill-context-architecture/validation-and-compliance.md) — checklist, mistakes.
- [Architecture Diagram](./skill-context-architecture/architecture-diagram.md) — visual reference.
- [Related Documentation](./skill-context-architecture/related-documentation.md) — further reading.
- [Enforcement](./skill-context-architecture/enforcement.md) — code-review checklist.
- [Summary](./skill-context-architecture/summary.md) — closing recap.
