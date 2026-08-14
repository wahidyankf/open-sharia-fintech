---
title: "Beginner Examples"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 10
---

Examples 1–16 establish the provider-agnostic read-evaluate-act loop with typed local fakes. Each artifact
is credential-free and supplies the annotated code, executable assertion, takeaway, and production boundary.

| Example                  | Brief / state diagram   | Artifact                                                         | Key takeaway                                                  |
| ------------------------ | ----------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------- | ------------------- |
| 1. Model response        | `model → response`      | [ex-01](learning/code/ex-01-model-response/example.py)           | A response is typed state.                                    |
| 2. Message history list  | `system → user`         | [ex-02](learning/code/ex-02-message-history-list/example.py)     | History is loop state.                                        |
| 3. Fake model adapter    | `script → turn`         | [ex-03](learning/code/ex-03-fake-model-adapter/example.py)       | Fakes make behavior deterministic.                            |
| 4. Minimal loop no tools | `model → final`         | [ex-04](learning/code/ex-04-minimal-loop-no-tools/example.py)    | Stop on final output.                                         |
| 5. Detect tool call      | `turn → request`        | [ex-05](learning/code/ex-05-detect-tool-call/example.py)         | Parse before dispatch.                                        |
| 6. Execute one tool      | `request → result`      | [ex-06](learning/code/ex-06-execute-one-tool/example.py)         | Tools are registered callables.                               |
| 7. Append tool result    | `result → history`      | [ex-07](learning/code/ex-07-append-tool-result/example.py)       | Observations grow history.                                    |
| 8. Loop until final      | `model ↔ tool`          | [ex-08](learning/code/ex-08-loop-until-final/example.py)         | A stop path is mandatory.                                     |
| 9. Max turns guard       | `turns → cap`           | [ex-09](learning/code/ex-09-max-turns-guard/example.py)          | Bound nontermination.                                         |
| 10. Stop explicit tool   | `finish → stop`         | [ex-10](learning/code/ex-10-stop-on-explicit-tool/example.py)    | Stops can be typed.                                           |
| 11. System prompt effect | `prompt → behavior`     | [ex-11](learning/code/ex-11-system-prompt-effect/example.py)     | Instructions are state.                                       |
| 12. Tool registry        | `name → callable`       | [ex-12](learning/code/ex-12-tool-registry/example.py)            | Registry controls dispatch.                                   |
| 13. Tool error feedback  | `error → observation`   | [ex-13](learning/code/ex-13-tool-error-feedback/example.py)      | Errors inform the model.                                      |
| 14. Turn iteration log   | `user turn              | loop step`                                                       | [ex-14](learning/code/ex-14-turn-vs-iteration-log/example.py) | Measure both units. |
| 15. Token count turn     | `turn → usage`          | [ex-15](learning/code/ex-15-token-count-per-turn/example.py)     | Costs are control inputs.                                     |
| 16. Minimal agent        | `prompt → tool → final` | [ex-16](learning/code/ex-16-minimal-agent-end-to-end/example.py) | Composition remains small.                                    |
