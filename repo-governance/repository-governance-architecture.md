---
title: "Repository Governance Architecture"
description: Six-layer governance hierarchy defining how repository rules, conventions, and practices are organized
category: explanation
subcategory: architecture
tags:
  - architecture
  - governance
  - six-layer
  - structure
created: 2026-02-09
when_to_use: Use when you need the full six-layer governance model — how vision, principles, conventions, development, agents, and workflows relate and trace to each other.
---

# Repository Governance Architecture

## Contents

- [Overview](./repository-governance-architecture/overview.md) — What each governance layer answers and how traceability flows Use when orienting to what each layer is for.
- [Architectural Principles](./repository-governance-architecture/architectural-principles.md) — How this architecture follows the repository's own core principles Use when checking a change to the architecture stays principle-aligned.
- [The Six Layers](./repository-governance-architecture/the-six-layers.md) — The six-layer diagram and quick-reference table Use for an at-a-glance view of all six layers.
- [Layer 0: Vision (WHY WE EXIST)](./repository-governance-architecture/layer-0-vision.md) — The foundational-purpose layer: location, vision statement, pillars Use for Layer 0's scope and relationship to Layer 1.
- [Layer 1: Principles (WHY - Values)](./repository-governance-architecture/layer-1-principles.md) — The foundational-values layer: location, principle roster, requirements Use for Layer 1's scope and traceability requirements.
- [Layer 2: Conventions (WHAT - Documentation Rules)](./repository-governance-architecture/layer-2-conventions.md) — The documentation-standards layer: scope, categories, requirements Use for Layer 2's scope and governance relationships.
- [Layer 3: Development (HOW - Software Practices)](./repository-governance-architecture/layer-3-development.md) — The software-practices layer: scope, categories, requirements Use for Layer 3's scope and governance relationships.
- [Layer 4: AI Agents (WHO - Executors)](./repository-governance-architecture/layer-4-ai-agents.md) — The automated-implementer layer: color families, requirements Use for Layer 4's scope and agent requirements.
- [Layer 5: Workflows (WHEN - Multi-Step Processes)](./repository-governance-architecture/layer-5-workflows.md) — The orchestration layer: workflow families, requirements Use for Layer 5's scope and workflow requirements.
- [Agent skills: Delivery Infrastructure (Not a Governance Layer)](./repository-governance-architecture/agent-skills-inline-delivery.md) — Why agent skills aren't a governance layer, and inline delivery Use when explaining inline skill delivery.
- [Agent skills: Fork Delivery and Layer Comparison](./repository-governance-architecture/agent-skills-fork-delivery.md) — Fork-mode skill delegation and the skill-prefix catalog Use when explaining fork-mode skill delegation.
- [Governance Test and Delivery Mechanisms Comparison](./repository-governance-architecture/governance-test-and-delivery-mechanisms.md) — Checklist for whether a mechanism governs agents, plus a delivery-mechanism comparison Use when deciding if a new mechanism counts as governance.
- [Complete Traceability Example](./repository-governance-architecture/complete-traceability-example.md) — A full worked example tracing Color Accessibility across all six layers Use for a concrete end-to-end traceability example.
- [Governance Relationships](./repository-governance-architecture/governance-relationships.md) — How governance flows downward, cross-layer relationships, and per-layer traceability requirements Use to check which layer governs which.
- [Best Practices](./repository-governance-architecture/best-practices.md) — Checklists for creating conventions, practices, agents, workflows, and skills Use before creating a new convention, practice, agent, workflow, or skill.
- [Common Misconceptions](./repository-governance-architecture/common-misconceptions.md) — Five common misconceptions about the architecture, corrected Use when you suspect a misunderstanding about the layers.
- [Future Evolution](./repository-governance-architecture/future-evolution.md) — Potential future layers, skill-growth patterns, and growth expectations Use when considering a structural change against the anticipated growth path.
- [Principles Implemented/Respected (Architecture Document)](./repository-governance-architecture/principles-implemented-respected.md) — Which core principles this document itself implements Use when auditing this document's traceability to Layer 1.
- [Conventions Implemented/Respected (Architecture Document)](./repository-governance-architecture/conventions-implemented-respected.md) — Which conventions this document itself implements Use when auditing this document's traceability to Layer 2.
