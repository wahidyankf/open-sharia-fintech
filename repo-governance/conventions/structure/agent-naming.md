---
title: "Agent Naming Convention"
description: Single rule for agent filename structure across .claude/agents and .opencode/agent
when_to_use: Use when naming or renaming an agent definition file.
category: explanation
subcategory: conventions
tags:
  - agents
  - naming
  - conventions
created: 2026-04-17
---

# Agent Naming Convention

Agents in this repository follow a **single filename rule with no exceptions**. The rule covers every agent file in `.claude/agents/` and its auto-generated mirror in `.opencode/agents/`.

## Children

- [Why This Rule Exists](./agent-naming/01-why-this-rule-exists.md) — the three guarantees a uniform, exception-free rule provides.
- [The Rule](./agent-naming/02-the-rule.md) — the scope-qualifier-role filename structure every agent filename must match.
- [Scope Vocabulary](./agent-naming/03-scope-vocabulary.md) — the closed set of scope tokens allowed as the first filename token.
- [Role Vocabulary](./agent-naming/04-role-vocabulary.md) — the closed set of role tokens allowed as the last filename token.
- [Applies To and Enforcement](./agent-naming/05-applies-to-and-enforcement.md) — which directories this convention governs and the audit command that enforces it.
- [Examples](./agent-naming/06-examples.md) — current agents grouped by role, illustrating scope/qualifier/role decomposition.

## Related

- [`.claude/agents/README.md`](../../../.claude/agents/README.md) — Operational catalog of agents (source of truth).
- `.opencode/agents/` — Auto-synced agent files (no README index); use [`.claude/agents/README.md`](../../../.claude/agents/README.md) as authoritative catalog for both bindings.
- [File Naming Convention](../structure/file-naming.md) — Sibling filename rule for non-agent files in `docs/`, `repo-governance/`, and plans.

## Principles Implemented/Respected

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)** — The scope and role of every agent are explicit in its filename; no convention-by-tribal-knowledge.
- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)** — One rule, one suffix list, one regex. No exceptions to memorize.
- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)** — A single-line `grep` decides conformance, enabling mechanical enforcement by `repo-rules-checker`.
