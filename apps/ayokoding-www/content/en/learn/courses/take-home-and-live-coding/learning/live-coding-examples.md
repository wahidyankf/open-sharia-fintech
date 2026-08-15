---
title: "Live-coding examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 20
---

In a live round, the interviewer is a partner with more context, not an adversary to outguess. These examples make the process visible without endorsing a specific editor, screen-sharing product, or timer. `ex-26` through `ex-50` continue the course sequence.

| Example                                        | Artifact                                                                             | Verify                                                                           | Concepts            |
| ---------------------------------------------- | ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------- | ------------------- |
| **ex-26 · open with questions**                | Ask expected input size, invalid-input policy, and output shape.                     | Assumptions are stated before implementation.                                    | co-19               |
| **ex-27 · restate the shared goal**            | “I will parse records, validate them, then summarize by owner.”                      | Partner can correct the goal before code starts.                                 | co-13, co-14        |
| **ex-28 · state a first slice**                | A function returning an empty summary for an empty sequence.                         | Code runs before full parsing exists.                                            | co-16, co-20        |
| **ex-29 · narrate intent**                     | Say why a dictionary is the right short-lived state.                                 | Each non-obvious edit has a spoken reason.                                       | co-14               |
| **ex-30 · show the terminal loop**             | Edit, run one focused test, inspect output, repeat.                                  | A partner sees the result of each meaningful increment.                          | co-17, co-16        |
| **ex-31 · accept a constraint**                | Interviewer says duplicate owners should accumulate; repeat it and adjust.           | The change is acknowledged rather than silently absorbed.                        | co-15               |
| **ex-32 · use a baseline**                     | Start with a direct loop before a utility abstraction.                               | A correct executable form exists before generalization.                          | co-16, co-20        |
| **ex-33 · test while speaking**                | Run the happy path and describe what assertion protects.                             | The test result is interpreted, not merely displayed.                            | co-14, co-17        |
| **ex-34 · pause at ambiguity**                 | Ask whether whitespace-only owner names are valid.                                   | Code does not invent a policy.                                                   | co-19               |
| **ex-35 · take the steer**                     | Partner suggests a `ValueError` instead of a sentinel.                               | Candidate explains the user-facing benefit and pivots.                           | co-15, co-10        |
| **ex-36 · keep a green checkpoint**            | Commit or label a passing parser before aggregation changes.                         | Tests are green at the checkpoint.                                               | co-16               |
| **ex-37 · read failure aloud**                 | Quote the expected versus actual output before changing code.                        | The repair follows evidence rather than guessing.                                | co-18               |
| **ex-38 · form a hypothesis**                  | “The blank line is being parsed as a record; I will reproduce it.”                   | A failing test exists before the fix.                                            | co-18               |
| **ex-39 · isolate the smallest input**         | Reduce a failure to one blank owner record.                                          | The scenario explains only one behavior.                                         | co-18, co-11        |
| **ex-40 · repair the boundary**                | Reject whitespace owner before aggregation.                                          | Existing happy path and new failure path pass.                                   | co-10, co-16        |
| **ex-41 · avoid a silent dead end**            | Say “I do not recall that library option; I would consult its docs after the round.” | Recovery names the exact lookup and proposes a standard-library alternative.     | co-21               |
| **ex-42 · protect time**                       | Announce remaining time and choose test completion over an optional flag.            | Core contract remains finished.                                                  | co-02, co-12        |
| **ex-43 · request feedback**                   | Ask whether the partner wants a faster path or more edge cases next.                 | Interviewer has a clear chance to steer.                                         | co-13, co-15        |
| **ex-44 · narrate an invariant**               | “Every parsed record is either rejected or contributes once.”                        | Test cases map to the two branches.                                              | co-14, co-16        |
| **ex-45 · use editor fluency proportionately** | Navigate to the focused test and rerun it without a broad command.                   | The loop is fast and observable, not a performance act.                          | co-17               |
| **ex-46 · recover from wrong shape**           | Change a list of tuples to a typed record when error fields need names.              | Refactor preserves behavior at a green checkpoint.                               | co-18, co-20        |
| **ex-47 · listen after talking**               | Explain a design in two sentences, then pause.                                       | The transcript contains a partner response before the next choice.               | co-13, co-14        |
| **ex-48 · close a live slice**                 | Summarize behavior, validation, tests, and one deferred item.                        | Closeout is intelligible without rereading code.                                 | co-09, co-22        |
| **ex-49 · live self-score**                    | Rate clarity, collaboration, correctness, and recovery.                              | Each rating names a timestamp or artifact.                                       | co-13 through co-21 |
| **ex-50 · mini mock pairing**                  | Build a tiny parser from brief through error path in one sitting.                    | The transcript stays narrated and tests remain green at every stated checkpoint. | co-13 through co-22 |

The local `live/transcript.md` and `live/code/` capstone artifacts show a compact, tool-agnostic version of this loop.

← Previous: [Take-home examples](./take-home-examples.md) · Next: [Review and recovery examples](./review-and-recovery-examples.md) →
