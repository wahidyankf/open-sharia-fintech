---
title: "Current Model Versions (April 2026)"
description: "States the current model versions in use as of April 2026."
category: explanation
subcategory: development
tags:
  - ai-agents
  - model-selection
  - development
  - standards
created: 2025-11-23
when_to_use: Use when you need the current concrete model version string for a tier.
---

# Current Model Versions (April 2026)

| Agent config alias | Model ID                    | Context     | Notes                 | Benchmark                                                                        |
| ------------------ | --------------------------- | ----------- | --------------------- | -------------------------------------------------------------------------------- |
| `opus` (inherit)   | `claude-opus-4-7`           | 1M tokens   | Current top tier      | [Benchmarks](../../../../docs/reference/ai-model-benchmarks.md#claude-opus-47)   |
| `sonnet`           | `claude-sonnet-4-6`         | 1M tokens   | Daily driver          | [Benchmarks](../../../../docs/reference/ai-model-benchmarks.md#claude-sonnet-46) |
| `haiku`            | `claude-haiku-4-5-20251001` | 200k tokens | v3 retired 2026-04-19 | [Benchmarks](../../../../docs/reference/ai-model-benchmarks.md#claude-haiku-45)  |

Aliases (`opus`, `sonnet`, `haiku`) automatically track future model versions within each
tier. The model IDs above are current as of April 2026.
