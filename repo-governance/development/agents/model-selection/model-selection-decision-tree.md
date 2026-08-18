---
title: "Model Selection Decision Tree"
description: "Gives the decision tree for walking from a task's characteristics to the correct model tier."
category: explanation
subcategory: development
tags:
  - ai-agents
  - model-selection
  - development
  - standards
created: 2025-11-23
when_to_use: Use when unsure which model tier a new agent should declare.
---

# Model Selection Decision Tree

```
Start: Choosing Agent Model
    |
    +-- Does the task require creative reasoning, code generation,
    |   architectural decisions, or nuanced content creation?
    |   |
    |   +-- Yes --> Opus (omit model field)
    |   |
    |   +-- No --> Does the task require applying rules, validating
    |              against checklists, or following structured procedures?
    |              |
    |              +-- Yes --> Sonnet (model: sonnet)
    |              |
    |              +-- No --> Is the task purely mechanical with
    |                         no reasoning required?
    |                         |
    |                         +-- Yes --> Haiku (model: haiku)
    |                         |
    |                         +-- No --> Default to Sonnet
    |                                    (safer than haiku for
    |                                     ambiguous cases)
```
