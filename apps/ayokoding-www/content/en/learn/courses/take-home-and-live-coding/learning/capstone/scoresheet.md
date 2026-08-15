# Take-home and live-round score sheet

Use the scale `1 = absent`, `2 = partial`, `3 = reliable`, `4 = clear and reusable`. A completed sheet cites a command, diff, test, README section, or transcript checkpoint; confidence alone is not evidence.

## Take-home

| Axis                         | Score (1–4) | Evidence                                              | Next action                                                  |
| ---------------------------- | ----------: | ----------------------------------------------------- | ------------------------------------------------------------ |
| Brief and scope              |      _rate_ | Requirements checklist and explicit deferred work.    | Make any unstated assumption a question.                     |
| Structure and README         |      _rate_ | Entry point, tests, run/test/decision headings.       | Have a fresh shell follow the README.                        |
| Correctness and validation   |      _rate_ | Happy, empty, malformed, and negative tests.          | Add the riskiest missing boundary.                           |
| Readability and dependencies |      _rate_ | Named functions, types, standard-library-only design. | Remove or justify one unnecessary abstraction.               |
| History and review pass      |      _rate_ | Cohesive commits, clean diff, focused suite.          | Check a mid-history commit or write the missing final check. |

## Live round

| Axis                         | Score (1–4) | Evidence                                           | Next action                                        |
| ---------------------------- | ----------: | -------------------------------------------------- | -------------------------------------------------- |
| Clarification and framing    |      _rate_ | Transcript checkpoint 0.                           | Ask one constraint question before coding.         |
| Think-aloud collaboration    |      _rate_ | Checkpoints 1–3 with a pause for partner input.    | Shorten one monologue into intent → edit → pause.  |
| Green increments and fluency |      _rate_ | Focused `pytest -q` after each small slice.        | Preserve a runnable baseline before refactoring.   |
| Debugging and recovery       |      _rate_ | Checkpoints 4–5: hypothesis, reproduction, repair. | State the hypothesis before opening an editor.     |
| Honesty and closeout         |      _rate_ | Explicit trade-off and no-bluff lookup plan.       | Close with behavior, tests, and one deferred item. |

## Submission decision

- [ ] Both formats have a score and evidence in every row.
- [ ] Any score below 3 has one concrete repair and a retest or replay date.
- [ ] The final decision distinguishes “ready to submit” from “ready to practice again.”
