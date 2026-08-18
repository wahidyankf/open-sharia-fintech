---
title: "Purpose"
description: "States why this convention defines a context architecture for agent skills."
category: explanation
subcategory: development
tags:
  - ai-agents
  - agent-skills
  - architecture
  - development
created: 2025-11-23
when_to_use: Use when explaining why a Skill's context mode matters.
---

# Purpose

This architectural decision establishes that all skills stored in the `.claude/skills/` directory must remain compatible with both main conversation agents and delegated agents. Since delegated agents cannot spawn other delegated agents (architectural constraint of AI coding agents), skills with `context: fork` would be unusable in delegated agent contexts.

**Target Audience**:

- Agent developers creating or maintaining skills
- Repository maintainers reviewing skill contributions
- Anyone designing agent workflows involving skills
