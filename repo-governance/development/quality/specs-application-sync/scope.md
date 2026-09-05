---
title: "Scope"
description: "What this convention applies to, and its boundary with other conventions."
category: explanation
subcategory: development
tags:
  - specs
  - architecture
  - c4-diagrams
  - gherkin
  - synchronization
  - quality
created: 2026-03-24
when_to_use: "Use when checking whether this convention applies to a specific kind of change."
---

# Scope

This convention applies to:

- All directories under `apps/`
- All directories under `libs/`
- All directories under `specs/`

It does not apply to:

- `docs/` — documentation follows its own conventions; spec synchronization is a code-and-architecture concern
- `repo-governance/` — governance documents are not application code or acceptance specs
- `plans/` — planning documents describe intentions, not observable system behaviour
- `generated-contracts/` — auto-generated code is not maintained manually; update the source spec instead
