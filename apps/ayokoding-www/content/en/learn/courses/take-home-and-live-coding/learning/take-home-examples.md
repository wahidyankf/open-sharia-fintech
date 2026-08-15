---
title: "Take-home examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 10
---

These examples use a fictional brief: “summarize newline-delimited task records by owner.” The point is not the domain; it is making the requested slice complete, runnable, and reviewable. `ex-01` through `ex-25` are contiguous with the live sequence that follows.

| Example                              | Artifact                                                                                           | Verify                                                                  | Concepts            |
| ------------------------------------ | -------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ------------------- |
| **ex-01 · restate the brief**        | A checklist: read input, summarize by owner, print deterministic output, reject malformed records. | Every sentence in the brief has one checklist item.                     | co-01               |
| **ex-02 · mark scope**               | A two-column “required / explicitly deferred” note.                                                | No unrequested web UI, database, or authentication appears in the plan. | co-02               |
| **ex-03 · choose the first slice**   | A CLI that accepts one file and prints one summary.                                                | The smallest slice can run before formatting extras exist.              | co-02, co-20        |
| **ex-04 · make a reviewable tree**   | `briefcheck.py`, `tests/`, and `README.md`.                                                        | A reader can locate entry point, behavior, and tests at a glance.       | co-03               |
| **ex-05 · README quickstart first**  | Run, test, decisions, and trade-offs headings before feature code.                                 | All four headings are present and commands are copyable.                | co-04               |
| **ex-06 · dependency inventory**     | A note that this parser needs only the standard library.                                           | Dependency list is empty or every dependency has a reason.              | co-08               |
| **ex-07 · clean command**            | `python briefcheck.py sample.txt` documented from repository root.                                 | A new shell follows only README steps to output.                        | co-05               |
| **ex-08 · happy-path test**          | A fixture with two owners and asserted totals.                                                     | The core expected output passes before refinements.                     | co-06               |
| **ex-09 · empty-input test**         | An empty file case with an intentional result or clear error.                                      | Behavior is defined instead of accidental.                              | co-06, co-10        |
| **ex-10 · malformed-line test**      | A test for a missing separator and line number in the message.                                     | The failure explains how and where to repair input.                     | co-06, co-10        |
| **ex-11 · validate at boundary**     | A parser guard rejects blank owners and negative counts.                                           | Invalid values never reach aggregation.                                 | co-10               |
| **ex-12 · name the domain**          | `TaskRecord` and `summarize_by_owner`, not `x` and `do_it`.                                        | A reviewer can infer purpose without tracing every branch.              | co-11               |
| **ex-13 · split one long function**  | Parse, validate, aggregate, and format as separate functions.                                      | Each function has one testable responsibility.                          | co-03, co-11        |
| **ex-14 · first cohesive commit**    | `docs: add execution guide` after README quickstart is correct.                                    | Commit message says what changed and diff has one theme.                | co-07               |
| **ex-15 · second cohesive commit**   | `feat: summarize task records` after a working core exists.                                        | Checking out the commit leaves a runnable program.                      | co-07, co-16        |
| **ex-16 · test commit**              | `test: cover malformed task records`.                                                              | The test explains a user-visible boundary rather than coverage alone.   | co-06, co-07        |
| **ex-17 · document a cut**           | A README note deferring CSV quoting because the brief specifies lines.                             | The note names the alternative and why it was not built.                | co-09               |
| **ex-18 · time-box**                 | A 90-minute plan with a 15-minute final review reserve.                                            | Optional polishing cannot consume core-completion time.                 | co-12               |
| **ex-19 · compare two designs**      | A list aggregation versus SQLite note for tiny input.                                              | The selected standard-library list is justified by the brief.           | co-02, co-08, co-09 |
| **ex-20 · deterministic output**     | Sorted owner rows.                                                                                 | The same input produces byte-for-byte stable output.                    | co-05, co-11        |
| **ex-21 · error for humans**         | `line 3: count must be a non-negative integer`.                                                    | The message identifies bad input and a corrective action.               | co-10, co-11        |
| **ex-22 · run the documented tests** | A command block using `pytest -q`.                                                                 | Command exits zero from the documented directory.                       | co-04, co-05        |
| **ex-23 · inspect the diff**         | A submission checklist: brief, tests, README, dependencies, diff.                                  | No generated cache, secret, or unrelated formatting change remains.     | co-07, co-22        |
| **ex-24 · fresh-reader rehearsal**   | A colleague or second shell follows only the README.                                               | It reaches a successful run without tribal knowledge.                   | co-04, co-05        |
| **ex-25 · take-home self-score**     | A five-axis score for scope, tests, docs, readability, and history.                                | Every score cites visible evidence and one next action.                 | co-01 through co-12 |

The runnable capstone take-home is intentionally small. From `learning/capstone/take-home`, run `pytest -q` before treating its README as complete.

← Previous: [Learning overview](./overview.md) · Next: [Live-coding examples](./live-coding-examples.md) →
