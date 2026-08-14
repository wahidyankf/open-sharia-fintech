---
title: "Context Budget Examples"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 10
---

Theme A is the source-defined first level: Examples 1–12. Each entry has five parts through its brief,
compact diagram, annotated local artifact, takeaway, and production boundary.

| Example                        | Brief / diagram                               | Artifact                                                            | Takeaway / why it matters                |
| ------------------------------ | --------------------------------------------- | ------------------------------------------------------------------- | ---------------------------------------- | ---------------------------------------------------------------- | ------------------------ |
| 1. Count tokens                | `messages → count`                            | [ex-01](learning/code/ex-01-count-tokens/example.py)                | Token counts make the budget measurable. |
| 2. Budget a context            | `sources → ceiling`                           | [ex-02](learning/code/ex-02-budget-a-context/example.py)            | Assembly must fit before sending.        |
| 3. Context composition diagram | `system + task + history + retrieval + tools` | [ex-03](learning/code/ex-03-context-composition-diagram/example.py) | Sources compete for finite space.        |
| 4. Overflow detection          | `candidate > window → guard`                  | [ex-04](learning/code/ex-04-overflow-detection/example.py)          | Detect before a provider rejects.        |
| 5. Lost in the middle          | `early                                        | middle                                                              | late`                                    | [ex-05](learning/code/ex-05-lost-in-the-middle-demo/example.py)  | Position affects recall. |
| 6. Prune stale messages        | `history → prune`                             | [ex-06](learning/code/ex-06-prune-stale-messages/example.py)        | Remove superseded state.                 |
| 7. Relevance inclusion         | `score → select`                              | [ex-07](learning/code/ex-07-relevance-scored-inclusion/example.py)  | Keep relevant evidence.                  |
| 8. Context cost report         | `tokens → cost`                               | [ex-08](learning/code/ex-08-cost-of-context-report/example.py)      | Context has explicit spend.              |
| 9. Latency versus size         | `size → latency`                              | [ex-09](learning/code/ex-09-latency-vs-size/example.py)             | Larger prompts cost time.                |
| 10. Budget allocation          | `memory                                       | retrieval                                                           | history`                                 | [ex-10](learning/code/ex-10-budget-allocation-policy/example.py) | Allocate deliberately.   |
| 11. Truncate tool results      | `result → truncate + note`                    | [ex-11](learning/code/ex-11-truncate-tool-results/example.py)       | Preserve truncation provenance.          |
| 12. Budgeted assembly pipeline | `sources → fit context`                       | [ex-12](learning/code/ex-12-budgeted-assembly-pipeline/example.py)  | The final invariant is fit.              |
