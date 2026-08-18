---
title: "Principles Implemented/Respected"
description: "Lists the core repository principles this convention implements and respects."
category: explanation
subcategory: development
tags:
  - ai-agents
  - agent-skills
  - architecture
  - development
created: 2025-11-23
when_to_use: Use when checking which principles justify a rule about Skill context architecture.
---

# Principles Implemented/Respected

This convention respects the following core principles:

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Explicitly documents the architectural constraint preventing delegated agents from spawning other delegated agents. Makes the limitation visible and provides clear guidance on skill design decisions.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: Single-level delegated agent spawning prevents complex nested agent hierarchies. Agent skills remain simple knowledge containers that work everywhere, avoiding architectural complexity.
