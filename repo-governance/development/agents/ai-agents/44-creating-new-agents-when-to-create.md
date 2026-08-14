---
title: "Creating New Agents — When to Create a New Agent"
description: "States the criteria for deciding when a new agent should be created rather than extending an existing one."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use when deciding whether a new task needs a new agent or fits an existing agent's scope.
---

# Creating New Agents — When to Create a New Agent

## When to Create a New Agent

Create a new agent when:

1. PASS: **New domain or expertise** not covered by existing agents
2. PASS: **Different tool requirements** than existing agents
3. PASS: **Distinct user need** that would benefit from specialization
4. PASS: **Clear, single responsibility** that doesn't overlap

Don't create a new agent when:

1. FAIL: **Existing agent can be extended** with minor modifications
2. FAIL: **Responsibilities overlap** significantly with existing agents
3. FAIL: **Purpose is too vague** or general
4. FAIL: **Temporary or experimental** need (extend existing instead)
