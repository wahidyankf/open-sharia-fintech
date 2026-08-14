---
title: "Tier Comparison Summary"
description: "Summarizes the three model tiers in one comparison table."
category: explanation
subcategory: development
tags:
  - ai-agents
  - model-selection
  - development
  - standards
created: 2025-11-23
when_to_use: Use when you need a quick side-by-side comparison of the three model tiers.
---

# Tier Comparison Summary

| Dimension              | Planning-Grade (inherit)                                                                       | Execution-Grade                                                                                  | Fast                                                                                            |
| ---------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| **Reasoning depth**    | Deep, multi-step                                                                               | Moderate, rule-based                                                                             | Minimal, mechanical                                                                             |
| **Creativity**         | High (novel solutions)                                                                         | Low (follows templates)                                                                          | None (fixed procedures)                                                                         |
| **Task ambiguity**     | Handles open-ended problems                                                                    | Handles structured problems                                                                      | Requires deterministic flow                                                                     |
| **Output originality** | Creates new content/code                                                                       | Transforms per rules                                                                             | Executes predefined steps                                                                       |
| **Error recovery**     | Adapts to unexpected states                                                                    | Follows fallback rules                                                                           | Fails or retries                                                                                |
| **Typical agents**     | Creative makers, developers                                                                    | Checkers, fixers, structured makers                                                              | Deployers, link checkers, file manager                                                          |
| **SWE-bench Verified** | [87.6%](../../../../docs/reference/ai-model-benchmarks.md#claude-opus-47) (Verified, Apr 2026) | [79.6%](../../../../docs/reference/ai-model-benchmarks.md#claude-sonnet-46) (Verified, Feb 2026) | [73.3%](../../../../docs/reference/ai-model-benchmarks.md#claude-haiku-45) (Verified, Oct 2025) |
