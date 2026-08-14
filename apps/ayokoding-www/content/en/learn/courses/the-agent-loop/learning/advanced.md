---
title: "Advanced Examples"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 30
---

Examples 35–48 complete the authoritative loop syllabus with bounded coding tools, streaming parity,
combined limits, recovery, traces, testing, stop policy, approval, resumption, concurrency, browser use,
and a mini coding-agent capstone. Each artifact is typed, local, and credential-free.

| Example                   | Brief / state diagram            | Artifact                                                                | Key takeaway                             |
| ------------------------- | -------------------------------- | ----------------------------------------------------------------------- | ---------------------------------------- |
| 35. File editing agent    | `read → write → verify`          | [ex-35](learning/code/ex-35-file-editing-agent/example.py)              | File changes need evidence.              |
| 36. Shell running agent   | `command → result`               | [ex-36](learning/code/ex-36-shell-running-agent/example.py)             | Shell actions are bounded tools.         |
| 37. TDD driving agent     | `red → green`                    | [ex-37](learning/code/ex-37-tdd-driving-agent/example.py)               | Tests provide goal evidence.             |
| 38. Streaming full loop   | `deltas + call → final`          | [ex-38](learning/code/ex-38-streaming-full-loop/example.py)             | Streaming preserves loop correctness.    |
| 39. Budget and turns      | `first limit → stop`             | [ex-39](learning/code/ex-39-budget-and-turn-limits-together/example.py) | Enforce every limit.                     |
| 40. Robust recovery       | `failure → feedback → retry`     | [ex-40](learning/code/ex-40-robust-error-recovery/example.py)           | Failures are observations.               |
| 41. Observable run        | `events → summary`               | [ex-41](learning/code/ex-41-observable-agent-run/example.py)            | Runs need traces.                        |
| 42. Deterministic suite   | `fake → tests`                   | [ex-42](learning/code/ex-42-deterministic-test-suite/example.py)        | No live calls in tests.                  |
| 43. Pluggable stop policy | `policy → halt`                  | [ex-43](learning/code/ex-43-pluggable-stop-policy/example.py)           | Stops are swappable policy.              |
| 44. Human gate            | `approval → tool`                | [ex-44](learning/code/ex-44-human-in-the-loop-gate/example.py)          | Risky work waits.                        |
| 45. Resumable session     | `history → resume`               | [ex-45](learning/code/ex-45-resumable-session/example.py)               | Session state is replayable.             |
| 46. Concurrent agents     | `loops → isolated joins`         | [ex-46](learning/code/ex-46-concurrent-agents/example.py)               | Isolate loop state.                      |
| 47. Agent browser tool    | `agent → CDP tool`               | [ex-47](learning/code/ex-47-agent-with-browser-tool/example.py)         | Browser access remains a tool boundary.  |
| 48. Mini coding agent     | `prompt → tools → verified task` | [ex-48](learning/code/ex-48-capstone-mini-coding-agent/example.py)      | A complete agent is bounded composition. |
