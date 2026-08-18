---
title: "Governance Test and Delivery Mechanisms Comparison"
description: Checklist for whether a mechanism governs agents, plus a delivery-mechanism comparison
category: explanation
subcategory: architecture
tags:
  - architecture
  - governance
  - agent-skills
created: 2026-02-09
when_to_use: Use when deciding if a new mechanism counts as governance.
---

# Governance Test and Delivery Mechanisms Comparison

**Governance test**:

- Conventions → Agents: Yes (agents MUST follow conventions)
- Development → Agents: Yes (agents MUST follow practices)
- agent skills (inline) → Agents: **No** (inject knowledge, serve agents)
- agent skills (fork) → Agents: **No** (delegate tasks, serve agents)

**Delivery Mechanisms Comparison**:

| Mechanism             | When Loaded              | Purpose                             | Authority |
| --------------------- | ------------------------ | ----------------------------------- | --------- |
| **AGENTS.md**         | Conversation startup     | Initial context and quick refs      | None      |
| **Inline skills**     | On-demand (progressive)  | Deep knowledge injection            | None      |
| **Fork skills**       | On-demand (delegation)   | Task delegation to delegated agents | None      |
| **Direct references** | Explicit document reads  | Authoritative source                | Full      |
| **Conventions (L2)**  | Via any above mechanisms | Governance rules                    | Full      |
| **Development (L3)**  | Via any above mechanisms | Governance practices                | Full      |
