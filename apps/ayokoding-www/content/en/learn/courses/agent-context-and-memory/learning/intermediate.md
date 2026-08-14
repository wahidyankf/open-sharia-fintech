---
title: "Compaction and Summarization"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 20
---

Theme B is the source-defined compaction level: Examples 13–22. Each entry has brief purpose, a compact
strategy diagram, annotated local code, takeaway, and production boundary in its linked artifact.

| Example                    | Brief / diagram             | Artifact                                                         | Key takeaway                                                 |
| -------------------------- | --------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------ | --------------------------- |
| 13. Summarize history span | `old turns → summary`       | [ex-13](code/ex-13-summarize-a-history-span/example.py)          | Preserve decisions.                                          |
| 14. Rolling window summary | `summary + recent turns`    | [ex-14](code/ex-14-rolling-window-plus-summary/example.py)       | Bound verbatim history.                                      |
| 15. Preserve open threads  | `unresolved → summary`      | [ex-15](code/ex-15-compaction-preserves-open-threads/example.py) | Keep pending work.                                           |
| 16. Lossy failure          | `loss → fix`                | [ex-16](code/ex-16-lossy-compaction-failure/example.py)          | Test dropped details.                                        |
| 17. Trigger on budget      | `threshold → compact`       | [ex-17](code/ex-17-trigger-compaction-on-budget/example.py)      | Compact before overflow.                                     |
| 18. Summary quality        | `original ↔ summary`        | [ex-18](code/ex-18-summary-quality-check/example.py)             | Detect omissions.                                            |
| 19. Incremental summary    | `turn → update`             | [ex-19](code/ex-19-incremental-summary-update/example.py)        | Avoid full resummaries.                                      |
| 20. Compaction in loop     | `loop → compact → continue` | [ex-20](code/ex-20-compaction-in-the-loop/example.py)            | Context fits the loop.                                       |
| 21. Compaction diagram     | `summary + window`          | [ex-21](code/ex-21-compaction-diagram/example.py)                | Make state flow visible.                                     |
| 22. Compare strategies     | `truncate                   | summarize`                                                       | [ex-22](code/ex-22-compare-compaction-strategies/example.py) | Quality and cost trade off. |
