---
title: "Intermediate Examples"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 20
---

Examples 17–34 extend the same local fake-backed loop with multiple tools, budgets, retries, streaming,
adapter boundaries, replay, idempotency, validated arguments, and multi-step tasks.

| Example                         | Brief / state diagram    | Artifact                                                      | Key takeaway                         |
| ------------------------------- | ------------------------ | ------------------------------------------------------------- | ------------------------------------ |
| 17. Multi-tool registry         | `name → tool`            | [ex-17](code/ex-17-multi-tool-registry/example.py)            | Dispatch remains typed.              |
| 18. Multi-tool turn             | `turn → calls`           | [ex-18](code/ex-18-multi-tool-turn/example.py)                | Preserve all results.                |
| 19. Concurrent tool calls       | `calls → join`           | [ex-19](code/ex-19-concurrent-tool-calls/example.py)          | Bound independent concurrency.       |
| 20. Budget ceiling stop         | `cost → halt`            | [ex-20](code/ex-20-budget-ceiling-stop/example.py)            | Spend limits agency.                 |
| 21. Retry model error           | `error → retry`          | [ex-21](code/ex-21-retry-model-error/example.py)              | Retry transient failures only.       |
| 22. Timeout a tool              | `tool → timeout`         | [ex-22](code/ex-22-timeout-a-tool/example.py)                 | Timeout becomes feedback.            |
| 23. Streaming final answer      | `deltas → final`         | [ex-23](code/ex-23-streaming-final-answer/example.py)         | Assemble in order.                   |
| 24. Assemble streamed tool call | `chunks → call`          | [ex-24](code/ex-24-assemble-streamed-tool-call/example.py)    | Execute complete calls only.         |
| 25. Provider adapter swap       | `loop → adapter`         | [ex-25](code/ex-25-provider-adapter-swap/example.py)          | Provider is a boundary.              |
| 26. Loop transcript log         | `events → record`        | [ex-26](code/ex-26-loop-transcript-log/example.py)            | Runs are inspectable.                |
| 27. Replay transcript           | `record → same run`      | [ex-27](code/ex-27-replay-a-transcript/example.py)            | Replay supports regression.          |
| 28. Idempotent tool effect      | `retry → once`           | [ex-28](code/ex-28-idempotent-tool-side-effect/example.py)    | Retries must not double-apply.       |
| 29. Tool args validation        | `args → validate → tool` | [ex-29](code/ex-29-tool-args-validation/example.py)           | Reject bad arguments.                |
| 30. Final versus tool ambiguity | `text + call → policy`   | [ex-30](code/ex-30-final-answer-vs-tool-ambiguity/example.py) | Resolve ambiguity deterministically. |
| 31. Conversation continuation   | `history → next turn`    | [ex-31](code/ex-31-conversation-continuation/example.py)      | Preserve scoped context.             |
| 32. Cost report                 | `usage → report`         | [ex-32](code/ex-32-cost-report/example.py)                    | Summarize operational cost.          |
| 33. Structured final output     | `final → schema`         | [ex-33](code/ex-33-structured-final-output/example.py)        | Validate final contracts.            |
| 34. Multi-step tool task        | `read → compute → write` | [ex-34](code/ex-34-multi-step-tool-task/example.py)           | Stop only after goal evidence.       |
