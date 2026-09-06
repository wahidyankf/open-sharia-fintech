---
title: "Platform Binding Examples"
description: "Covers the per-harness model-ID mapping tables for all four grades, the secondary binding's tier collapse, and the caveats that make a grade mean different things per vendor."
category: explanation
subcategory: development
tags:
  - ai-agents
  - model-selection
  - development
  - standards
created: 2025-11-23
when_to_use: Use when translating a model grade to a concrete model ID for a specific harness.
---

# Platform Binding Examples

Agents in the primary binding directory are auto-synced to every generated binding by rhino-cli
(`npm run generate:bindings`). The sync translates the primary binding's grade alias into whatever
each harness expects. Never hand-edit a generated binding — change the grade in `.claude/` and
regenerate.

## Model ID Mapping

| Grade     | Claude Code (`.claude/agents/`) | OpenCode (`.opencode/agents/`) | Codex (`.codex/agents/*.toml`) |
| --------- | ------------------------------- | ------------------------------ | ------------------------------ |
| Ultra     | `model: fable`                  | `zai-coding-plan/glm-5.2`      | `model = "gpt-6-astra"`        |
| Planning  | `model: opus`                   | `zai-coding-plan/glm-5.2`      | `model = "gpt-5.6-sol"`        |
| Execution | `model: sonnet`                 | `zai-coding-plan/glm-5.2`      | `model = "gpt-5.6-terra"`      |
| Fast      | `model: haiku`                  | `zai-coding-plan/glm-5.2`      | `model = "gpt-5.6-luna"`       |
| `inherit` | `model: inherit`                | `zai-coding-plan/glm-5.2`      | key omitted — vendor default   |

The Codex column pairs each grade with the model the vendor's own catalog positions at that level:
its top-of-lineup model for ultra, its most capable current-generation model for planning, its
"balanced, everyday work" model for execution, and its "lowest cost in the family" model for fast.
Verified against the vendor's published model catalog on 2026-09-06.

## Effort Mapping

Claude Code's `effort` also reaches the Codex binding, as `model_reasoning_effort`:

| Claude `effort` | Codex `model_reasoning_effort`     |
| --------------- | ---------------------------------- |
| `low`           | `low`                              |
| `medium`        | `medium`                           |
| `high`          | `high`                             |
| `xhigh`         | `xhigh`                            |
| `max`           | `xhigh` — saturates at the ceiling |

Codex additionally accepts `minimal`, which has no Claude Code counterpart and is never emitted.
OpenCode declares no per-agent effort, so the field is dropped there.

## Tier Collapse on the Secondary Binding

The secondary binding's `convertModel` maps all four grades to `zai-coding-plan/glm-5.2` via the
GLM Coding Plan primary provider. This is an intentional full-grade collapse, not an oversight: that
plan exposes one model. Grade assignments therefore govern behaviour on the primary and Codex
bindings, where a grade genuinely resolves to a different model. The `opencode-go` provider remains
configured in `.opencode/opencode.json` for `/models` roster access but takes no part in grade
mapping.

If the provider or model changes, update `convertModel` in
`apps/rhino-cli/src/RhinoCli.Application/src/HarnessRuntime.fs` and re-run
`npm run generate:bindings`.

## Where a Grade Does Not Mean the Same Thing

A grade names a _role in this repository_, not a guaranteed cost or context window. Three
cross-vendor mismatches are known and must not be papered over:

- **Fast is not like-for-like.** The Codex fast model is roughly five times cheaper per token than
  the Claude fast model and carries a ~1M-token context against 200k. An agent placed at fast for
  context reasons on one harness is not constrained the same way on the other.
- **Planning-grade cost parity is promotional.** The Codex planning model's list output price is
  currently discounted; at base rate it is more expensive per output token than its Claude
  counterpart.
- **The ultra Codex model may not be reachable.** The vendor is staging its rollout through a
  restricted-access programme, so `model = "gpt-6-astra"` can fail on an account without that
  access. This costs nothing today because no agent declares the ultra grade — but the first ultra
  agent must be smoke-tested on the Codex binding before it lands, not after.
