---
title: "Scope"
description: "Defines what this convention covers and does not cover regarding subagent orchestration."
category: explanation
subcategory: development
tags:
  - ai-agents
  - subagents
  - orchestration
  - development
created: 2025-11-23
when_to_use: Use when checking whether a subagent-orchestration question is in scope for this convention.
---

# Scope

## Scope

### What This Convention Covers

- Maximum concurrent Agent-tool spawns from a single main agent
- Polling cadence and signals for stuck detection
- How to identify healthy vs. stalled subagent output
- Relaunch procedure when a stuck agent is detected
- Chunk sizing guidance to fit within healthy runtimes
- Per-session override rules

### What This Convention Does NOT Cover

- Subagent internal behavior (covered by [Agent Workflow Orchestration Convention](../agent-workflow-orchestration.md))
- Agent frontmatter or file structure (covered by [AI Agents Convention](../ai-agents.md))
- Workflows that call agents sequentially rather than in background (no special rules needed)
- Bash-based tool parallelism (distinct from Agent-tool spawning)

## Standards
