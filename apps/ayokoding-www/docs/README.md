---
title: "AyoKoding — App Docs"
description: Index of feature data-sourcing runbooks and in-app documentation for ayokoding-www.
category: reference
---

# AyoKoding — App Docs

Feature data-sourcing runbooks and in-app documentation for `ayokoding-www`. Each runbook holds the
copy-paste prompts used to (re)source a feature's hand-curated dataset so the result drops straight
into that feature's schema.

## Data-sourcing runbooks

| Feature                   | Dataset module                                                                                                                                           | Runbook                                                                        |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Cost-of-Living Calculator | [`cost-of-living-calculator/core/data/{fx,cities,roles}.ts`](../src/features/cost-of-living-calculator/core/data/)                                       | [data-sourcing-prompt.md](./cost-of-living-calculator/data-sourcing-prompt.md) |
| AI Benchmark              | [`ai-benchmark/core/data/models.ts`](../src/features/ai-benchmark/core/data/models.ts) (single source of truth for the page and the generated reference) | [data-sourcing-prompt.md](./ai-benchmark/data-sourcing-prompt.md)              |

## See also

- Schema and design decisions live beside each dataset module (see the runbook's "See also" section).
- The reference document the AI Benchmark dataset generates:
  [`docs/reference/ai-model-benchmarks.md`](../../../docs/reference/ai-model-benchmarks.md).
