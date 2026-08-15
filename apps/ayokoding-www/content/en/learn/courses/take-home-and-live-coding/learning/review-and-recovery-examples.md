---
title: "Review and recovery examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 30
---

These advanced rehearsals extend the syllabus’s 50 examples to the By-Example volume floor of 75. They deliberately connect a reviewer’s asynchronous view with the live partner’s synchronous view. `ex-51` through `ex-75` complete the contiguous sequence.

| Example                                   | Artifact                                                                                          | Verify                                                              | Concepts                   |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- | -------------------------- |
| **ex-51 · reviewer-first opening**        | A README whose first screen contains purpose, run, test, and decisions.                           | A reviewer can execute before studying internals.                   | co-03, co-04               |
| **ex-52 · requirement-to-test map**       | A table mapping each brief bullet to a test or manual check.                                      | No required row is blank.                                           | co-01, co-06               |
| **ex-53 · clean-room run**                | A new temporary virtual environment or shell invocation.                                          | Only documented commands are needed.                                | co-05                      |
| **ex-54 · dependency challenge**          | A written answer for every non-standard dependency: why, pin, and alternative.                    | An unjustified library is removed.                                  | co-08                      |
| **ex-55 · scope-cut defense**             | A README paragraph declining pagination for a bounded input brief.                                | The core outcome remains complete and the cut is explicit.          | co-02, co-09, co-12        |
| **ex-56 · failure-path walkthrough**      | A terminal transcript feeding a malformed record.                                                 | Error reports the line and remediation.                             | co-06, co-10               |
| **ex-57 · readability pass**              | Replace hidden mutation and shorthand names with direct code.                                     | Review takes fewer mental jumps without changing tests.             | co-11                      |
| **ex-58 · history narrative**             | A three-commit sequence: docs, core, tests.                                                       | Each commit is cohesive and builds.                                 | co-07                      |
| **ex-59 · mid-history check**             | Check out the core commit and run its test command.                                               | It remains runnable rather than relying on a later rescue.          | co-07, co-16               |
| **ex-60 · final diff audit**              | Search for secrets, generated files, debug prints, and unrelated changes.                         | The submission contains none.                                       | co-22                      |
| **ex-61 · review a negative test**        | Explain why malformed input should error rather than silently skip.                               | Contract and test agree.                                            | co-06, co-10               |
| **ex-62 · live wrong-turn recovery**      | A transcript dropping an over-general class hierarchy.                                            | Candidate states why the first path cost more than it returned.     | co-02, co-18               |
| **ex-63 · incremental refactor**          | Extract a parser after its behavior is captured by tests.                                         | Tests pass before and after every small extraction.                 | co-16, co-20               |
| **ex-64 · uncertainty without bluffing**  | “I would verify Python’s CSV dialect behavior; for this line-only brief I will not introduce it.” | The response names a lookup and preserves scope.                    | co-21, co-08               |
| **ex-65 · interviewer hint as data**      | Partner points out an omitted empty input; candidate adds a test.                                 | The resulting behavior is visible and acknowledged.                 | co-15, co-18               |
| **ex-66 · narration-to-listening rhythm** | A transcript alternating intent, edit, result, and pause.                                         | Neither party is excluded by a monologue.                           | co-13, co-14               |
| **ex-67 · time-box triage**               | With ten minutes left, choose documentation and validation over an optional exporter.             | The decision names the trade-off.                                   | co-02, co-09, co-12        |
| **ex-68 · reproducible bug report**       | Record command, minimal input, observed output, expected output.                                  | Another person can reproduce without narration.                     | co-05, co-18               |
| **ex-69 · small observability note**      | Add one proportionate `--verbose` design note rather than telemetry.                              | No personal data or unnecessary operational surface is added.       | co-02, co-09               |
| **ex-70 · reviewer question response**    | Explain why aggregation uses a dict and output sorting is separate.                               | Answer refers to a stated decision and test.                        | co-09, co-11               |
| **ex-71 · live extension request**        | Partner asks for totals; add the feature after restating its contract.                            | Existing output stays stable and the new test passes.               | co-15, co-19, co-20        |
| **ex-72 · pair-debug a regression**       | Reproduce, hypothesize, isolate, repair, then rerun the full focused suite.                       | Transcript names evidence at each stage.                            | co-18                      |
| **ex-73 · submission scorecard**          | Rate scope, correctness, tests, docs, readability, history, and trade-offs.                       | Every axis has evidence plus a next action.                         | co-01 through co-12, co-22 |
| **ex-74 · full mock take-home**           | Brief → checklist → README → code → tests → clean run → score.                                    | Every stage has a saved artifact and no hidden setup.               | co-01 through co-12        |
| **ex-75 · full mock live round**          | Clarify → narrated minimal slice → hint → bug recovery → closeout.                                | Code remains runnable and the transcript records green checkpoints. | co-13 through co-22        |

← Previous: [Live-coding examples](./live-coding-examples.md) · Next: [Capstone](./capstone/overview.md) →
