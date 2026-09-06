---
title: "Tier Comparison Summary"
description: "Summarizes the four model grades in one comparison table, including the effort each grade declares."
category: explanation
subcategory: development
tags:
  - ai-agents
  - model-selection
  - development
  - standards
created: 2025-11-23
when_to_use: Use when you need a quick side-by-side comparison of the four model grades, or the effort a grade requires.
---

# Tier Comparison Summary

| Dimension              | Ultra                                   | Planning-Grade              | Execution-Grade                     | Fast                                   |
| ---------------------- | --------------------------------------- | --------------------------- | ----------------------------------- | -------------------------------------- |
| **Alias**              | `fable`                                 | `opus`                      | `sonnet`                            | `haiku`                                |
| **Reasoning depth**    | Frontier, long-horizon                  | Deep, multi-step            | Moderate, rule-based                | Minimal, mechanical                    |
| **Creativity**         | Highest (no prior art)                  | High (novel solutions)      | Low (follows templates)             | None (fixed procedures)                |
| **Task ambiguity**     | Handles problems with no known approach | Handles open-ended problems | Handles structured problems         | Requires deterministic flow            |
| **Output originality** | Invents the approach itself             | Creates new content/code    | Transforms per rules                | Executes predefined steps              |
| **Error recovery**     | Recovers from unfamiliar states         | Adapts to unexpected states | Follows fallback rules              | Fails or retries                       |
| **Typical agents**     | None yet — see the admission bar        | Creative makers, developers | Checkers, fixers, structured makers | Deployers, link checkers, file manager |
| **Relative cost**      | 2× planning                             | 2.5× execution              | 2× fast                             | Baseline                               |
| **Effort**             | `high`                                  | `high`                      | `xhigh`                             | `xhigh`                                |

Effort is a property of the grade, not of the individual agent: a weaker model is compensated with
more reasoning effort, so the pairing is a repository-wide rule rather than a per-agent judgement.
An agent MUST declare the `effort` its grade declares. The pairing above is not restated in code —
it is read from the `model-grades:` block in `repo-config.yml`, and `harness-claude` fails any agent
whose `effort` contradicts its grade. An agent naming no grade (`inherit`, or a pinned `claude-*`
ID) is skipped, because there is no grade whose effort it could contradict.

Cost multipliers are derived from the list prices in
[Current Model Versions](./current-model-versions.md) and are the reason each grade must be argued
for rather than assumed. Ultra currently has no members; see
[Model Tiers — Ultra](./model-tiers-ultra.md) for what admitting the first one requires.
