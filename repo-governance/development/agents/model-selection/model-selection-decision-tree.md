---
description: "Gives the decision tree for walking from a task's characteristics to the correct model grade."
when_to_use: Use when unsure which model grade a new agent should declare.
---

# Model Selection Decision Tree

The tree is entered from the bottom. Each grade must be argued past, never assumed.

```
Start: Choosing an Agent Grade
    |
    +-- Is the task purely mechanical, with no reasoning required?
    |   |
    |   +-- Yes --> Fast (model: haiku)
    |
    +-- Does the task apply rules, validate against checklists,
    |   or follow a structured procedure?
    |   |
    |   +-- Yes --> Execution-Grade (model: sonnet)
    |
    +-- Does the task require creative reasoning, code generation,
    |   architectural decisions, or nuanced content creation?
    |   |
    |   +-- Yes --> Planning-Grade (model: opus)
    |
    +-- Has this agent DEMONSTRABLY failed at the planning grade
    |   on a task that is expensive to detect and expensive to undo?
    |   |
    |   +-- Yes, with recorded evidence --> Ultra (model: fable)
    |   |
    |   +-- No, but it feels hard --> Planning-Grade
    |
    +-- None of the above / ambiguous --> Execution-Grade
                                          (safer than fast for
                                           ambiguous cases)
```

Ultra is the only grade that cannot be reached by prediction. It requires the recorded evidence
described in [Model Tiers — Ultra](./model-tiers-ultra.md#admission-evidence); anticipated
difficulty is not evidence.
