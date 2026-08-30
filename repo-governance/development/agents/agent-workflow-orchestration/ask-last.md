---
title: "Ask Last"
description: Defines the evidence and authority boundary an agent must exhaust before asking the user.
category: explanation
subcategory: development
tags: [ai-agents, orchestration, questions, autonomy]
created: 2026-08-30
when_to_use: Use before asking the user for information, preference, or authority during repository work.
---

# Ask Last

## Purpose

Questions should protect user-owned decisions, not outsource repository discovery to the user.

## Standards

Before asking, exhaust the applicable instruction files, repository sources and indexes, version
history, safe read-only diagnostics, and bounded reversible assumptions. Reuse evidence already
collected in the current task or by a trusted delegated agent.

Ask only when the unavailable information or authority would materially change the outcome, make
the work unsafe, or authorize an irreversible or externally visible action. State the evidence,
the unresolved choice, and the consequence of each viable option.

Do not ask for a discoverable path, current implementation fact, documented default, or validation
command. Do not use this rule to guess security boundaries, destructive scope, product preference,
or authority to commit, push, deploy, publish, or create durable plan artifacts.

## Examples

- Search the repository and history for the existing storage abstraction before asking which one
  to use.
- Ask when two product behaviors remain equally supported by evidence and the choice changes the
  user-visible contract.

## Validation

This rule is unenforced by decision. Contextual review checks whether a question was necessary;
adding a mechanical gate would require encoding unbounded task context.
