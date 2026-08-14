---
title: "Common Mistakes"
description: "Lists common mistakes made when selecting a model tier for an agent."
category: explanation
subcategory: development
tags:
  - ai-agents
  - model-selection
  - development
  - standards
created: 2025-11-23
when_to_use: Use when reviewing an agent's model-tier choice for a common mistake.
---

# Common Mistakes

| Mistake                                           | Problem                                                                          | Correction                                                          |
| ------------------------------------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Using opus for validation tasks                   | Wastes resources; opus may over-interpret instead of checking                    | Use execution-grade tier for checkers and fixers                    |
| Using fast tier for content creation              | Fast tier lacks reasoning depth for original content                             | Use planning-grade (inherit) for makers and developers              |
| Using execution-grade tier for deployment scripts | Execution-grade tier is overqualified for deterministic command sequences        | Use fast tier for deployers and link checkers                       |
| Omitting model justification                      | Future maintainers cannot assess whether the tier is appropriate                 | Always include Model Selection Justification block                  |
| Defaulting to planning-grade "just in case"       | Violates Simplicity Over Complexity principle                                    | Analyze task requirements; use the simplest adequate tier           |
| Using fast tier for tasks with error handling     | Fast tier cannot reason about unexpected states                                  | Use execution-grade or planning-grade depending on error complexity |
| Adding `model: opus` to planning-grade agents     | Bypasses budget-adaptive inheritance; forces planning-grade API charges on users | Omit the field — inherit session model to match user's tier         |
