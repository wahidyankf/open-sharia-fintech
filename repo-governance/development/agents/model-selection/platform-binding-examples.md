---
title: "Platform Binding Examples"
description: "Covers the per-harness model-ID mapping tables, tier collapse, and why glm-5.2 is the default on one secondary harness."
category: explanation
subcategory: development
tags:
  - ai-agents
  - model-selection
  - development
  - standards
created: 2025-11-23
when_to_use: Use when translating a model tier to a concrete model ID for a specific harness.
---

# Platform Binding Examples

Agents in the primary binding directory are auto-synced to the secondary binding directory by rhino-cli
(`npm run generate:bindings`). The sync translates primary binding model aliases to
secondary binding model IDs.

## Model ID Mapping

| Primary binding                                  | Secondary binding         | Capability notes                                                                   |
| ------------------------------------------------ | ------------------------- | ---------------------------------------------------------------------------------- |
| `model: opus` (thinking-grade)                   | `zai-coding-plan/glm-5.2` | Zhipu GLM via GLM Coding Plan primary provider; all tiers map to the same model ID |
| omit (execution-grade inherit) / `model: sonnet` | `zai-coding-plan/glm-5.2` | Same model as thinking-grade (intentional full-tier collapse)                      |
| `model: haiku` (fast)                            | `zai-coding-plan/glm-5.2` | Fast tier also collapses onto glm-5.2 via the primary provider                     |

## Tier Collapse

The primary binding has three tiers (planning-grade/thinking > execution-grade > fast). The secondary
binding's `convert_model()` maps all three tiers to `zai-coding-plan/glm-5.2` via the GLM Coding Plan
primary provider. The `opencode-go` provider remains configured in `.opencode/opencode.json` for
`/models` roster access but is not used in agent tier mapping.

Tier assignments govern behavior in primary binding sessions (the primary runtime, where `opus`
genuinely resolves to a stronger model than `sonnet`). The secondary binding collapses every tier
onto the same GLM Coding Plan model.

## Why glm-5.2 as the Default

`zai-coding-plan/glm-5.2` is the GLM Coding Plan primary provider model for all agent tiers.
The `opencode-go` provider remains available for `/models` roster access. If the primary provider
or model changes, update `convert_model()` in `apps/rhino-cli/src/application/agents/converter.rs`
and re-run `npm run generate:bindings`.
