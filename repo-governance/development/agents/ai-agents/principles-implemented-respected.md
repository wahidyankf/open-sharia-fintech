---
title: "Principles Implemented/Respected"
description: "Lists the core repository principles this convention implements and respects."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use when checking which principles justify a rule in the AI Agents Convention.
---

# Principles Implemented/Respected

**REQUIRED SECTION**: All development practice documents MUST include this section to ensure traceability from practices back to foundational values.

This practice respects the following core principles:

- **[Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md)**: Agents must verify assumptions using Read, Grep, and Glob tools before acting. When multiple valid approaches exist (e.g., different markdown formatting options), agents present options rather than choosing silently. Agents stop and ask questions when requirements are unclear, rather than guessing implementation details. Agents advocate for simpler solutions when appropriate (e.g., suggesting flat structure over nested hierarchy). All agents follow the "Information Accuracy and Verification" requirements: verify facts with tools, state confidence levels explicitly, ask when uncertain.

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Agent tool permissions are explicitly whitelisted in frontmatter (not implicitly granted). Each agent declares exactly which tools it can access. Agent responsibilities are explicitly documented, not inferred. Frontmatter fields (name, description, tools, model, color) make agent capabilities transparent and discoverable through simple grep operations.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: Agents follow single-responsibility principle - one clear, focused purpose per agent. Flat directory structure (no subdirectories). Simple naming convention (kebab-case). Standard document structure across all agents. Rather than creating "Swiss Army knife" agents with dozens of capabilities, we create focused agents that do one thing well. See the principle's "For AI Agents" section for implementation guidelines on avoiding over-engineering:
  - Only implement what was requested (no speculative features)
  - Avoid premature abstractions (inline first, extract when needed)
  - Trust type systems and frameworks (no defensive code for guaranteed scenarios)
  - Apply the senior engineer test (question complexity proactively)
  - Prefer boring solutions (battle-tested patterns over clever code)

- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**: Agents transform manual processes into automated workflows. Instead of manually validating 200+ markdown files, `rules-checker` automates validation. Agents transform manual processes into repeatable, consistent automated workflows.
